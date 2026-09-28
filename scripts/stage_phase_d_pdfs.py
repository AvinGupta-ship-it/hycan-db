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
    text = raw.decode("latin-1")
    text = re.split(r"[)\]>\s]", text)[0].rstrip(".,;:")
    # A DOI captured out of running text can swallow the words that followed it.
    for junk in ("Get", "Downloaded", "http", "www", "Crossref", "PubMed"):
        cut = text.find(junk)
        if cut > 8:
            text = text[:cut]
    return text.lower()


def dois_in_pdf(path: Path) -> list[str]:
    """Every distinct DOI-shaped string in the file, raw bytes and streams."""
    data = path.read_bytes()
    found = list(DOI_RE.findall(data))
    for stream in _inflate_streams(data):
        found.extend(DOI_RE.findall(stream))
    seen: set[str] = set()
    out: list[str] = []
    for raw in found:
        doi = _clean_doi(raw)
        if 8 < len(doi) < 80 and doi not in seen:
            seen.add(doi)
            out.append(doi)
    return out


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


def match_pdf(path: Path, papers: list[dict]) -> tuple[dict | None, str]:
    """Return (entry, basis). entry is None when identification is not safe."""
    by_doi = {p["doi"].strip().lower(): p for p in papers}

    found = dois_in_pdf(path)
    exact = [by_doi[d] for d in found if d in by_doi]
    if exact:
        ids = {p["paper_id"] for p in exact}
        if len(ids) == 1:
            return exact[0], "doi"
        return None, f"ambiguous: DOIs for {sorted(ids)} all present"

    # A truncated DOI is common when the string was split across PDF text runs.
    prefix_hits = {
        p["paper_id"]: p
        for d in found
        for p in papers
        if len(d) > 14 and p["doi"].strip().lower().startswith(d)
    }
    if len(prefix_hits) == 1:
        return next(iter(prefix_hits.values())), "doi-prefix"
    if len(prefix_hits) > 1:
        return None, f"ambiguous: DOI prefix matches {sorted(prefix_hits)}"

    blob = text_of_pdf(path)
    # `blob` is never empty -- the PDF header alone survives as " pdf 1 7 eof" --
    # so emptiness is the wrong test for a scan. Count real words instead. A
    # paper with a text layer yields hundreds; an image-only scan yields a
    # handful of structural tokens. An earlier draft tested `not blob.strip()`
    # and was dead code that could never fire.
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
        print(f"\nNOT IDENTIFIED ({len(unmatched)}) -- left alone:")
        for pdf, why in unmatched:
            print(f"  {pdf.name[:52]:52s} {why}")

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
