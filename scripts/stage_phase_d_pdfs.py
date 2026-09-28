#!/usr/bin/env python3
"""Identify downloaded Phase D PDFs and rename them to the corpus convention.

The problem this solves: the manual's rule is that every paper's ID lives in its
filename (§6.3) -- an agent reads the ID, it never assigns one. But a PDF
downloaded from a publisher is called `1-s2.0-S0360319916303xxx-main.pdf` or
`nanomaterials-11-02173.pdf`, and renaming 35 of those by hand is 35 chances to
put the wrong ID on the wrong paper.

So this script does the matching instead. Point it at a folder of downloaded
PDFs; it identifies each one against `references/phase_d_screening.json` and
writes a correctly named copy to a staging folder, ready to upload.

Matching is by DOI first, read out of the PDF's own bytes, and by distinctive
title words only as a fallback. **Stdlib only** -- no third-party PDF library,
because the project's dependencies do not include one and this must run on a
fresh clone without installing anything.

It never renames in place, never deletes an input, and never overwrites an
existing output. A file it cannot identify with confidence is reported and left
alone, because a wrong ID on a PDF is worse than an unnamed one: it would send a
verifier to the wrong paper and every cell it checked would be wrong for a
reason nothing downstream could detect.

Usage:
    python3 scripts/stage_phase_d_pdfs.py ~/Downloads
    python3 scripts/stage_phase_d_pdfs.py ~/Downloads --out ~/Desktop/hycan-upload
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
import zlib
from pathlib import Path

DEFAULT_SCREENING = Path("references/phase_d_screening.json")
DEFAULT_OUT = Path.home() / "Desktop" / "hycan-upload"

DOI_RE = re.compile(rb"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")

# Keys a publisher writes its own DOI next to, in the Info dictionary or XMP.
# `/doi` is deliberately NOT a bare member of this list: every `https://doi.org/`
# in a reference list contains it, which leaked citations into the metadata
# signal and defeated the whole point of that signal. A PDF dictionary key is
# followed by its value, so it is matched separately with that requirement.
META_KEYS = (b"prism:doi", b"dc:identifier", b"/subject",
             b"citation_doi", b"xmp:identifier")
# `/DOI (10...)` or `/DOI<...>`: the key as a real dictionary entry.
META_DOI_KEY = re.compile(rb"/doi\s*[(<]", re.IGNORECASE)
META_WINDOW = 200

# A filename must share at least this many leading characters with a DOI's
# normalised suffix before that counts as evidence. Two IJHE DOIs from the same
# year share about twelve, so anything shorter is not discriminating.
MIN_FILENAME_KEY = 12
# A complete DOI suffix found in the name needs fewer characters than a leading
# portion does, because it is a whole identifier rather than a shared stem.
MIN_FILENAME_WHOLE = 8

# Words too common in this field to identify a paper by.
STOPWORDS = frozenset("""
a an and the of for in on with by from to at as is are be its their this that
hydrogen storage adsorption uptake sorption carbon carbons materials material
study effect effects high low new novel using via towards toward
""".split())

MIN_TITLE_TOKENS = 4

# Below this many recovered words, the file is an image-only scan and the title
# matcher has nothing to work with. The two scanned papers in the existing 23
# recover fewer than 20; every born-digital paper recovers hundreds.
MIN_TEXT_WORDS = 40

# A refusal below this title score showed no sign of being a corpus paper at
# all. Avin's Downloads folder held 1087 PDFs, of which about 30 were ours, so
# listing every refusal buries the handful worth looking at.
NEAR_MISS_SCORE = 0.5
NO_EVIDENCE = "no corpus evidence"


class StagingError(RuntimeError):
    """Raised on a condition that should stop the run."""


# --- PDF text, without a PDF library ---------------------------------------

def _inflate_streams(data: bytes) -> list[bytes]:
    """Return the inflated contents of every FlateDecode stream we can read.

    Deliberately forgiving: a PDF in the wild has broken streams, and one that
    fails to inflate is skipped rather than aborting the file.
    """
    out: list[bytes] = []
    for match in re.finditer(rb"stream\r?\n", data):
        start = match.end()
        end = data.find(b"endstream", start)
        if end == -1:
            continue
        chunk = data[start:end]
        for attempt in (chunk, chunk.lstrip(b"\r\n")):
            try:
                out.append(zlib.decompress(attempt))
                break
            except zlib.error:
                try:
                    out.append(zlib.decompressobj().decompress(attempt))
                    break
                except zlib.error:
                    continue
    return out


def _clean_doi(raw: bytes) -> str:
    """Trim a DOI-shaped match back to the DOI.

    The closing parenthesis is the awkward one. In PDF content a string literal
    ends with `)`, so a DOI printed as `(10.1016/j.carbon.2005.03.037)` has to
    stop there. But an older Elsevier DOI contains a balanced pair of its own --
    `10.1016/S0008-6223(01)00051-3` -- and cutting at the first `)` silently
    truncates it to `10.1016/s0008-6223(01`, which then matches nothing, or
    worse matches as a prefix of some other paper. Both HYC-0051 and HYC-0052
    are of that form. So parentheses are tracked, and only an unbalanced `)`
    ends the DOI.
    """
    text = raw.decode("latin-1")
    depth = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth == 0:
                text = text[:i]
                break
            depth -= 1
        elif ch in "]> \t\r\n":
            text = text[:i]
            break
    text = text.rstrip(".,;:")
    # A DOI captured out of running text can swallow the words that followed it.
    for junk in ("Get", "Downloaded", "http", "www", "Crossref", "PubMed"):
        cut = text.find(junk)
        if cut > 8:
            text = text[:cut]
    return text.lower()


def dois_in_pdf(path: Path) -> list[str]:
    """Every distinct DOI-shaped string in the file, raw bytes and streams."""
    return list(doi_counts(path)[0])


def doi_counts(path: Path) -> tuple[dict[str, int], set[str]]:
    """Return how often each DOI appears, and which appear in PDF metadata.

    Both are discriminators for the problem that broke the first version of
    this script: **a paper in a coherent corpus cites the other papers in it.**
    Five Phase D PDFs were refused as "ambiguous" because their reference lists
    contain the DOIs of papers already extracted, which is not ambiguity, it is
    the literature behaving normally.

    Measured on the 23 corpus PDFs, against their known DOIs:

    - A DOI sitting next to a metadata key is the paper's own in **13 of 13**
      files that carry one. No false positives, so this is the primary signal.
    - The paper's own DOI is strictly the most frequent in **19 of 20**. The
      exception is a file where its own DOI and one citation each appear once,
      which is a tie and must be refused rather than broken arbitrarily.

    Byte offset was tried first and rejected: the own DOI's position ranges
    from 0.003 to 0.915 of the file because a PDF's byte layout does not follow
    page order, so "the earliest DOI is the paper's own" is false.
    """
    data = path.read_bytes()
    counts: dict[str, int] = {}
    blobs = [data] + _inflate_streams(data)

    for blob in blobs:
        for raw in DOI_RE.findall(blob):
            doi = _clean_doi(raw)
            if 8 < len(doi) < 80:
                counts[doi] = counts.get(doi, 0) + 1

    meta: set[str] = set()

    def harvest(blob: bytes, at: int) -> None:
        for raw in DOI_RE.findall(blob[at:at + META_WINDOW]):
            doi = _clean_doi(raw)
            if 8 < len(doi) < 80:
                meta.add(doi)

    for blob in blobs:
        low = blob.lower()
        for key in META_KEYS:
            at = low.find(key)
            while at >= 0:
                harvest(blob, at)
                at = low.find(key, at + 1)
        for m in META_DOI_KEY.finditer(blob):
            harvest(blob, m.start())
    return counts, meta


def filename_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def doi_suffix_key(doi: str) -> str:
    _, _, suffix = doi.partition("/")
    return re.sub(r"[^a-z0-9]+", "", suffix.lower())


def text_of_pdf(path: Path, limit: int = 400_000) -> str:
    """A rough lowercase text blob, for title matching only.

    This is not a faithful extraction and must never be used to read a value.
    It exists so that a paper whose DOI is absent can still be identified by
    its title, and §3.4's prohibition on eyeballed values is unaffected: no
    number this function returns enters the dataset.
    """
    data = path.read_bytes()
    parts = [data]
    parts.extend(_inflate_streams(data))
    blob = b" ".join(parts)[:limit]
    text = blob.decode("latin-1", errors="ignore")
    # PDF text operators leave glyphs scattered across parentheses; flatten.
    text = re.sub(r"[^A-Za-z0-9]+", " ", text)
    return text.lower()


# --- matching ---------------------------------------------------------------

def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def title_tokens(title: str) -> list[str]:
    return [t for t in normalise(title).split() if t not in STOPWORDS and len(t) > 3]


def load_papers(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    papers = payload.get("papers")
    if not isinstance(papers, list) or not papers:
        raise StagingError(f"{path} has no 'papers' list")
    for entry in papers:
        for key in ("paper_id", "doi", "title", "authors", "year"):
            if not str(entry.get(key, "")).strip():
                raise StagingError(
                    f"{entry.get('paper_id', '?')} is missing {key!r}"
                )
    return papers


def target_name(entry: dict) -> str:
    """`HYC-0031_blankenship2017.pdf`, matching the existing 23 PDFs."""
    first = entry["authors"].split(";")[0].strip()
    # Take the last whitespace-separated token as the family name; strip
    # initials and punctuation. Good enough for a filename, and the paper_id
    # prefix is what actually identifies the file.
    surname = normalise(first).split()[-1] if normalise(first) else "unknown"
    return f"{entry['paper_id']}_{surname}{entry['year']}.pdf"


def filename_matches_doi(stem: str, doi: str) -> bool:
    """Does this filename contain enough of this DOI's suffix to identify it?

    Publishers name a download after the DOI's suffix (`c6ra06620h.pdf`) or,
    at Elsevier, after the PII, which for an older DOI is that suffix with the
    punctuation removed (`1-s2.0-S0008622301000513-main.pdf` for
    `10.1016/S0008-6223(01)00051-3`). Both are exact string matching against a
    DOI already held, not an inference drawn from the name.

    A leading portion counts too, because some filenames truncate
    (`BioRes_14_4_9755_...` for `10.15376/biores.14.4.9755-9765`), but it must
    be at least MIN_FILENAME_KEY characters: two IJHE DOIs from the same year
    share about twelve, so anything shorter does not discriminate.
    """
    key = filename_key(stem)
    suffix = doi_suffix_key(doi)
    if not key or not suffix:
        return False
    # The WHOLE suffix present in the name is the strong case: an RSC code like
    # `c6ra06620h` is only ten characters but it is a complete identifier, and
    # a filename containing one by coincidence is not a thing that happens.
    if len(suffix) >= MIN_FILENAME_WHOLE and suffix in key:
        return True
    # A leading portion is the weak case and needs more of it, because two IJHE
    # DOIs from the same year share about twelve characters.
    return len(suffix) > MIN_FILENAME_KEY and suffix[:MIN_FILENAME_KEY] in key


def match_pdf(path: Path, papers: list[dict]) -> tuple[dict | None, str]:
    """Return (entry, basis). entry is None when identification is not safe.

    Evidence is tried strongest first. Each rule must resolve to exactly one
    paper or it hands on to the next; a rule that resolves to several refuses
    outright rather than guessing, because a PDF filed under the wrong
    paper_id sends a verifier to the wrong source and every value it checks is
    then wrong in a way nothing downstream can detect.
    """
    by_doi = {p["doi"].strip().lower(): p for p in papers}
    counts, meta = doi_counts(path)
    known = {d: c for d, c in counts.items() if d in by_doi}

    # 1. The DOI the publisher wrote into the file's own metadata. 13/13 on the
    #    corpus, no false positives.
    meta_known = sorted(d for d in meta if d in by_doi)
    if len(meta_known) == 1:
        return by_doi[meta_known[0]], "doi-metadata"

    # 2. The filename. Publishers name a download after the DOI's suffix or, at
    #    Elsevier, after the PII, which for an older DOI *is* the suffix. This
    #    is deterministic string matching against a DOI we already hold, not an
    #    inference from the name.
    named = sorted({
        p["paper_id"] for p in papers
        if filename_matches_doi(path.stem, p["doi"])
    })
    if len(named) == 1:
        return next(p for p in papers if p["paper_id"] == named[0]), "filename"
    if len(named) > 1:
        return None, f"ambiguous: filename matches {named}"

    # 3. DOIs printed in the body.
    if len(known) == 1:
        return by_doi[next(iter(known))], "doi"
    if len(known) > 1:
        ranked = sorted(known.items(), key=lambda kv: -kv[1])
        (top, n_top), (_, n_next) = ranked[0], ranked[1]
        # A paper prints its own DOI in a running head; it cites another once.
        if n_top >= 2 and n_top >= 2 * n_next:
            return by_doi[top], f"doi-frequency ({n_top} vs {n_next})"
        return None, (
            f"ambiguous: {len(known)} corpus DOIs present with no clear "
            f"owner {[(d.split('/')[-1][:18], c) for d, c in ranked[:4]]}"
        )

    # 4. A DOI split across text runs leaves only a prefix.
    prefix_hits = {
        p["paper_id"]: p
        for d in counts
        for p in papers
        if len(d) > 18 and p["doi"].strip().lower().startswith(d)
    }
    if len(prefix_hits) == 1:
        return next(iter(prefix_hits.values())), "doi-prefix"
    if len(prefix_hits) > 1:
        return None, f"ambiguous: DOI prefix matches {sorted(prefix_hits)}"

    # 5. Title, for a paper that prints no DOI its text layer preserves.
    blob = text_of_pdf(path)
    words = sum(1 for tok in blob.split() if len(tok) >= 4 and tok.isalpha())
    if words < MIN_TEXT_WORDS:
        return None, (
            f"no text layer ({words} words recovered) -- a scan, so it needs "
            f"naming by hand"
        )

    scored: list[tuple[float, dict, int]] = []
    for entry in papers:
        tokens = title_tokens(entry["title"])
        if len(tokens) < MIN_TITLE_TOKENS:
            continue
        hits = sum(1 for t in tokens if t in blob)
        scored.append((hits / len(tokens), entry, hits))
    scored.sort(key=lambda row: -row[0])
    if not scored:
        return None, "no title long enough to match on"

    best, second = scored[0], (scored[1] if len(scored) > 1 else (0.0, None, 0))
    if best[0] >= 0.75 and best[2] >= MIN_TITLE_TOKENS and best[0] - second[0] >= 0.25:
        return best[1], f"title ({best[2]}/{len(title_tokens(best[1]['title']))} words)"
    if best[0] >= 0.75:
        return None, (
            f"ambiguous: {best[1]['paper_id']} and {second[1]['paper_id']} "
            f"score {best[0]:.2f} and {second[0]:.2f}"
        )
    if best[0] < NEAR_MISS_SCORE:
        return None, NO_EVIDENCE
    return None, f"no confident match (best {best[1]['paper_id']} at {best[0]:.2f})"


# --- driver -----------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="folder holding the downloads")
    parser.add_argument("--screening", type=Path, default=DEFAULT_SCREENING)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if not args.source.is_dir():
        print(f"error: {args.source} is not a folder", file=sys.stderr)
        return 1
    try:
        papers = load_papers(args.screening)
    except (StagingError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    pdfs = sorted(p for p in args.source.iterdir()
                  if p.suffix.lower() == ".pdf" and p.is_file())
    if not pdfs:
        print(f"No PDFs in {args.source}. Nothing to do.")
        return 0

    matched: list[tuple[Path, dict, str]] = []
    unmatched: list[tuple[Path, str]] = []
    claimed: dict[str, Path] = {}

    for pdf in pdfs:
        entry, basis = match_pdf(pdf, papers)
        if entry is None:
            unmatched.append((pdf, basis))
            continue
        pid = entry["paper_id"]
        if pid in claimed:
            unmatched.append(
                (pdf, f"{pid} already matched by {claimed[pid].name}")
            )
            continue
        claimed[pid] = pdf
        matched.append((pdf, entry, basis))

    matched.sort(key=lambda row: row[1]["paper_id"])

    print(f"{len(pdfs)} PDF(s) in {args.source}\n")
    if matched:
        print(f"IDENTIFIED ({len(matched)}):")
        for pdf, entry, basis in matched:
            print(f"  {target_name(entry):44s} <- {pdf.name[:46]:46s} [{basis}]")
    if unmatched:
        near = [(f, w) for f, w in unmatched if w != NO_EVIDENCE]
        none_at_all = len(unmatched) - len(near)
        if near:
            print(f"\nNOT IDENTIFIED, but look like corpus papers ({len(near)})"
                  f" -- left alone:")
            for pdf, why in near:
                print(f"  {pdf.name[:52]:52s} {why}")
        if none_at_all:
            print(f"\n{none_at_all} other PDF(s) showed no sign of being a "
                  f"corpus paper and are not listed.")

    still = [p["paper_id"] for p in papers if p["paper_id"] not in claimed]
    if still:
        print(f"\nSTILL MISSING ({len(still)} of {len(papers)}):")
        print("  " + ", ".join(still))

    if args.dry_run:
        print("\n--dry-run: nothing copied.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    copied = skipped = 0
    for pdf, entry, _ in matched:
        dest = args.out / target_name(entry)
        if dest.exists():
            skipped += 1
            continue
        shutil.copy2(pdf, dest)
        copied += 1

    print(f"\n{copied} copied to {args.out}"
          + (f", {skipped} already there" if skipped else ""))
    if unmatched:
        print(f"{len(unmatched)} not identified and not copied.")
    if still:
        print(f"{len(still)} paper(s) still to find.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
