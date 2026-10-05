#!/usr/bin/env python3
"""Generate references/bibliography.bib from references/bibliography_sources.json.

§3.5 requires every citation entering the bibliography to be resolved against a
record rather than recalled. This script makes that auditable: the sources file
carries, per paper, the value of every field **and where it came from**, and this
script only formats. It invents nothing, and it refuses to emit an entry whose
required fields are not present in the sources file.

Provenance rules encoded here, from the sources file's own `provenance` blocks:

* ``pdf``  -- read off the article's own pages (title block, byline, running
  header/footer). The primary record, and the only source used for author lists
  and page ranges where a PDF is held.
* ``openalex`` / ``semanticscholar`` -- a metadata service. Used for `number`
  (issue), which **no PDF in this corpus prints**, and for the three fields of
  HYC-0019, whose PDF carries no pagination at all.
* ``none`` -- absent everywhere. The field is omitted rather than guessed.

Author names are emitted in the form the article prints them, converted to
BibTeX's ``Family, Given`` order. A name whose family part cannot be identified
confidently is emitted brace-protected and verbatim, which tells BibTeX to leave
it alone -- see HYC-0011, whose byline is family-name-first while its own running
head treats the given name as the surname.

Usage:
    python3 scripts/build_bibliography.py --check   # verify, write nothing
    python3 scripts/build_bibliography.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_SOURCES = Path("references/bibliography_sources.json")
DEFAULT_OUTPUT = Path("references/bibliography.bib")

REQUIRED = ("authors", "title", "journal", "year", "doi")

# Dutch/Spanish/Portuguese particles BibTeX recognises as a "von part" when they
# appear lowercase before the family name. Listed so the surname split is
# explicit rather than accidental.
PARTICLES = (
    "van der", "van den", "van", "de la", "de los", "de", "den", "der",
    "von", "del",
)


class BibliographyError(RuntimeError):
    """Raised when the sources file cannot produce a complete entry."""


def split_name(name: str) -> str:
    """Return one BibTeX author in ``Family, Given`` order.

    A name already containing a comma is passed through: the sources file uses
    that form for a compound surname it has already resolved, such as
    ``Ramírez de la Piscina, Pilar``.

    A name wrapped in braces is passed through untouched. That is how the sources
    file marks a byline whose family/given split is genuinely unknown, and BibTeX
    treats a brace-protected string as a single indivisible family name.
    """
    name = name.strip()
    if name.startswith("{") and name.endswith("}"):
        return name
    if "," in name:
        return name

    lowered = name.lower()
    for particle in PARTICLES:
        marker = f" {particle} "
        if marker in lowered:
            index = lowered.index(marker)
            given = name[:index].strip()
            family = name[index + 1 :].strip()
            return f"{family}, {given}"

    parts = name.split()
    if len(parts) == 1:
        return f"{{{name}}}"

    # Consume EVERY leading initial as part of the given name, then take the
    # last remaining token as the family name.
    #
    # Two bugs lived here and both would have put a fabricated surname in a
    # published bibliography. Taking only ``parts[0]`` as the given name turned
    # "Y. Y. Fan" into "Y. Fan, Y."; consuming initials but then treating all the
    # rest as the family name turned "Barbara Panella" into "Barbara Panella,
    # Barbara" and "M. Sterlin Leo Hudson" into "Sterlin Leo Hudson, M." where
    # the surname is Hudson. Both cases are common in this corpus -- the older
    # papers print initials and the newer ones print full names -- so neither was
    # an edge case. ``test_bibliography.py`` checks every first author against the
    # `first_author` the dataset extracted independently from the same PDF.
    initials = 0
    while initials < len(parts) and parts[initials].endswith("."):
        initials += 1
    if initials == len(parts):  # every token is an initial; no surname to find
        return f"{{{name}}}"
    given, family = parts[:-1], parts[-1]
    return f"{family}, {' '.join(given)}" if given else f"{{{name}}}"


def format_entry(record: dict) -> str:
    missing = [f for f in REQUIRED if not record.get(f)]
    if missing:
        raise BibliographyError(
            f"{record.get('paper_id')}: cannot emit an entry, missing {missing}. "
            f"Resolve the field or record it as deliberately absent; this script "
            f"will not guess one."
        )

    entry_type = record.get("entry_type", "article")
    container = "booktitle" if entry_type == "incollection" else "journal"
    authors = " and ".join(split_name(a) for a in record["authors"])
    lines = [f"@{entry_type}{{{record['paper_id']},"]
    lines.append(f"  author       = {{{authors}}},")
    lines.append(f"  title        = {{{{{record['title']}}}}},")
    lines.append(f"  {container:<13}= {{{record['journal']}}},")
    if record.get("volume"):
        lines.append(f"  volume       = {{{record['volume']}}},")
    if record.get("number"):
        lines.append(f"  number       = {{{record['number']}}},")
    if record.get("pages"):
        lines.append(f"  pages        = {{{record['pages']}}},")
    lines.append(f"  year         = {{{record['year']}}},")
    lines.append(f"  doi          = {{{record['doi']}}},")
    if record.get("note"):
        lines.append(f"  note         = {{{record['note']}}},")
    lines.append("}")
    return "\n".join(lines)


def header(records: list[dict]) -> str:
    n_pdf = sum(1 for r in records if r["provenance"].get("authors") == "pdf")
    n_api = len(records) - n_pdf
    included = sum(1 for r in records if r.get("screening_decision") == "include")
    excluded = len(records) - included
    n_issue_pdf = sum(1 for r in records if r["provenance"].get("number") == "pdf")
    n_issue_openalex = sum(
        1 for r in records if r["provenance"].get("number") == "openalex"
    )
    n_issue_none = sum(1 for r in records if r["provenance"].get("number") == "none")
    return f"""% references/bibliography.bib -- HyCAN-DB
%
% GENERATED FILE. Do not edit by hand.
%   Source:    references/bibliography_sources.json
%   Generator: scripts/build_bibliography.py
%   Regenerate: python3 scripts/build_bibliography.py
%   Verify:     python3 scripts/build_bibliography.py --check
%
% {len(records)} entries: {included} screened in, {excluded} screened out. The
% excluded papers are kept because PRISMA reporting has to cite what it excluded.
% Every entry's key is its HyCAN-DB paper_id, so a citation in the manuscript
% resolves directly to the rows it describes in data/raw/measurements_v0.1.csv.
%
% HOW THESE WERE RESOLVED (§3.5: a DOI or a citation recalled from model weights
% is not a citation).
%
% {n_pdf} entries have their author list, title, journal, volume, pages and year
% read off the article's OWN PAGES -- title block, byline, running header and
% footer -- from the PDF held in the project. That is the primary record.
% {n_api} entries have no PDF on hand and are resolved from metadata services,
% cross-checked between OpenAlex and Semantic Scholar where both responded.
% Per-field provenance is in the sources file.
%
% THREE THINGS A READER SHOULD KNOW, because each was a real error caught here.
%
% 1. `number` (ISSUE) IS THE WEAKEST FIELD IN THIS FILE. {n_issue_pdf} entries
%    take their issue from a PDF's own citation line (Science, JACS and J. Phys.
%    Chem. B among them); every Elsevier and Springer running head in this corpus
%    carries volume, year and pages only, so {n_issue_openalex} issue numbers come
%    from OpenAlex and {n_issue_none} are absent everywhere and omitted. A
%    corpus-wide OpenAlex backfill (2026-10-05) retrieved the issues that the
%    articles themselves do not print. An earlier draft of this header claimed no
%    PDF printed one; a test against the sources file caught it.
%
% 2. OPENALEX REPORTS ELSEVIER'S ONLINE-FIRST YEAR, NOT THE ISSUE YEAR. Six
%    entries would have carried a year one too low -- HYC-0009, HYC-0012,
%    HYC-0018, HYC-0019, HYC-0021, HYC-0029. Every one of their PDFs prints both
%    dates, and the `year` here is the issue year from the running head, which is
%    what a citation means. Semantic Scholar agreed with the issue year on all
%    five it could reach.
%
% 3. A METADATA SERVICE GAVE AN AUTHOR THE WRONG NAME. OpenAlex lists HYC-0002's
%    fourth author as "Huai-Ping Cong"; the article prints "H. T. Cong", and
%    Semantic Scholar expands it to "Hong-Tao Cong" -- a different person.
%    OpenAlex also has ONE author for HYC-0011 where the article prints four.
%    Author lists therefore come from the PDF wherever one is held.
%
% Journal names are normalised to their full published form; the house styling a
% PDF happens to use ("CARBON", "int. j. hydrogen energy") is not preserved.
% Titles are brace-protected to keep their capitalisation. Encoding is UTF-8.
%
"""


def build(records: list[dict]) -> str:
    seen: set[str] = set()
    for r in records:
        pid = r["paper_id"]
        if pid in seen:
            raise BibliographyError(f"duplicate paper_id {pid}")
        seen.add(pid)
    ordered = sorted(records, key=lambda r: r["paper_id"])
    body = "\n\n".join(format_entry(r) for r in ordered)
    return header(records) + "\n" + body + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in memory and fail if it differs from the file on disk",
    )
    args = parser.parse_args(argv)

    try:
        if not args.sources.exists():
            raise BibliographyError(f"{args.sources} does not exist")
        records = json.loads(args.sources.read_text(encoding="utf-8"))["papers"]
        text = build(records)

        if args.check:
            if not args.output.exists():
                raise BibliographyError(f"{args.output} does not exist")
            current = args.output.read_text(encoding="utf-8")
            if current != text:
                raise BibliographyError(
                    f"{args.output} is out of sync with {args.sources}. "
                    f"Run: python3 scripts/build_bibliography.py"
                )
            print(f"{args.output} matches {args.sources} ({len(records)} entries)")
            return 0

        args.output.write_text(text, encoding="utf-8")
        # Re-read and re-verify. A self-report is not evidence (§3.8).
        if args.output.read_text(encoding="utf-8") != text:
            raise BibliographyError("the file on disk does not match what was written")
        print(f"wrote {args.output}: {len(records)} entries, re-read and verified")
        return 0

    except BibliographyError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
