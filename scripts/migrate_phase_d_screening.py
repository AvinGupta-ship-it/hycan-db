#!/usr/bin/env python3
"""Append the Phase D screening results to references/paper_tracking.csv.

Applies docs/migration_phase_d_screening_plan.md and nothing else: it appends 35
new rows, HYC-0031 through HYC-0065, and modifies no existing cell.

Reads and writes raw CSV lines rather than round-tripping through pandas, so
every line this script does not add is byte-identical by construction and
verify() asserts exactly that -- as raw bytes, not as parsed cells. A cell-level
check cannot see a line ending; manual section 6.7 records a migration that
passed one while rewriting the bytes of all 31 physical lines.

The 35 rows carry OpenAlex-verified metadata. Every title, author list, year and
journal below is the verbatim API field, confirmed by an agent that did not run
the search, with the returned title checked against the title the search agent
had recorded. See the plan, section 3.1.

Refuses to run twice.

Usage:
    python3 scripts/migrate_phase_d_screening.py --dry-run
    python3 scripts/migrate_phase_d_screening.py
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import shutil
import sys
from pathlib import Path

DEFAULT_TRACKING = Path("references/paper_tracking.csv")
DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_BACKUP_DIR = Path("/tmp")

DEFAULT_EXPECTED_ROWS = 30
EXPECTED_COLUMNS = 13
EXPECTED_HEADER = [
    "paper_id", "title", "authors", "year", "journal", "doi", "search_source",
    "screening_decision", "exclusion_reason", "pdf_obtained",
    "extraction_status", "extraction_date", "notes",
]

# Fixed for every row this migration adds (plan section 4).
SCREENING_DECISION = "include"
EXCLUSION_REASON = ""
PDF_OBTAINED = "no"
EXTRACTION_STATUS = "not_started"
EXTRACTION_DATE = ""

class MigrationError(RuntimeError):
    """Raised when a precondition or post-condition fails. Nothing is written."""


DEFAULT_SCREENING_JSON = Path("references/phase_d_screening.json")

REQUIRED_ENTRY_KEYS = (
    "paper_id", "title", "authors", "year", "journal", "doi", "cand_id", "notes",
)


def load_new_papers(path: Path) -> tuple[dict[str, str], ...]:
    """Load the verified screening records.

    The data lives in JSON rather than in this file so that the 35 records can
    be reviewed as data and diffed as data, following the pattern
    references/bibliography_sources.json already sets for
    scripts/build_bibliography.py.
    """
    import json

    payload = json.loads(path.read_text(encoding="utf-8"))
    papers = payload.get("papers")
    if not isinstance(papers, list) or not papers:
        raise MigrationError(f"{path} has no 'papers' list")
    for entry in papers:
        missing = [k for k in REQUIRED_ENTRY_KEYS if not str(entry.get(k, "")).strip()]
        if missing:
            raise MigrationError(
                f"{entry.get('paper_id', '?')}: missing or empty {missing}"
            )
        verdict = entry.get("provenance", {}).get("verdict")
        if verdict not in ("confirmed", "corrected"):
            raise MigrationError(
                f"{entry['paper_id']}: provenance.verdict is {verdict!r}; only a "
                f"DOI confirmed against the metadata service may enter the "
                f"tracking file (manual 3.5)"
            )
    return tuple(papers)



def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def detect_format(path: Path) -> tuple[str, bool]:
    """Return this file's line terminator and whether it ends with one.

    references/paper_tracking.csv is CRLF with no trailing newline. Writing it
    back with csv.writer's defaults changes the bytes of every existing line
    while leaving every cell correct. Detect and reproduce; never assume.
    """
    raw = path.read_bytes()
    terminator = "\r\n" if b"\r\n" in raw else "\n"
    return terminator, raw.endswith(b"\n")


def read_physical_lines(path: Path, terminator: str) -> list[str]:
    """Split on the file's own terminator, dropping a trailing empty element."""
    with path.open(encoding="utf-8", newline="") as handle:
        text = handle.read()
    lines = text.split(terminator)
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def read_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise MigrationError(f"{path} is empty")
    return rows[0], rows[1:]


def assert_line_mapping(lines: list[str], n_rows: int) -> None:
    """Assert physical line n holds data row n-1, which the byte check needs.

    A newline inside a quoted `notes` cell makes one data row span two physical
    lines, and the byte-level comparison in verify() would then be comparing
    the wrong things. Copied from migrate_relabel.py, which added this
    precondition for exactly that reason.
    """
    if len(lines) != n_rows + 1:
        raise MigrationError(
            f"{len(lines)} physical lines for {n_rows} data rows plus a header; "
            f"a data row must span more than one line (an embedded newline in a "
            f"quoted cell), so physical line n does not hold data row n-1 and "
            f"the byte-level check would be unsound"
        )


def build_row(entry: dict[str, str]) -> list[str]:
    """Render one NEW_PAPERS entry into the tracking file's 13 columns."""
    return [
        entry["paper_id"],
        entry["title"],
        entry["authors"],
        entry["year"],
        entry["journal"],
        entry["doi"],
        f"phase_d:{entry['cand_id'].split('-')[0]}:{entry['cand_id']}",
        SCREENING_DECISION,
        EXCLUSION_REASON,
        PDF_OBTAINED,
        EXTRACTION_STATUS,
        EXTRACTION_DATE,
        entry["notes"],
    ]


def check_preconditions(
    header: list[str],
    rows: list[list[str]],
    lines: list[str],
    expected_rows: int,
    new_papers: tuple[dict[str, str], ...],
) -> None:
    """Plan section 5. Raises on any failure; nothing is written."""
    if header != EXPECTED_HEADER:
        raise MigrationError(f"unexpected header: {header}")
    if expected_rows >= 0 and len(rows) != expected_rows:
        raise MigrationError(
            f"expected {expected_rows} data rows, found {len(rows)}; "
            f"pass --expected-rows to override"
        )
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != EXPECTED_COLUMNS]
    if ragged:
        raise MigrationError(f"ragged existing rows at csv lines {ragged}")

    assert_line_mapping(lines, len(rows))

    idx = {name: header.index(name) for name in header}

    # Refuse to re-run.
    existing_ids = {row[idx["paper_id"]] for row in rows}
    new_ids = {e["paper_id"] for e in new_papers}
    clash = existing_ids & new_ids
    if clash:
        raise MigrationError(
            f"this migration has already been applied: {sorted(clash)} are "
            f"already in the tracking file. Refusing to run twice."
        )

    existing_dois = {row[idx["doi"]].strip().lower() for row in rows}
    dupe = sorted(
        e["doi"] for e in new_papers if e["doi"].strip().lower() in existing_dois
    )
    if dupe:
        raise MigrationError(f"DOIs already tracked: {dupe}")

    seen: set[str] = set()
    for e in new_papers:
        d = e["doi"].strip().lower()
        if d in seen:
            raise MigrationError(f"duplicate DOI within the new set: {d}")
        seen.add(d)

    for e in new_papers:
        row = build_row(e)
        if len(row) != EXPECTED_COLUMNS:
            raise MigrationError(
                f"{e['paper_id']} renders to {len(row)} fields, expected "
                f"{EXPECTED_COLUMNS}"
            )
        for col, value in zip(EXPECTED_HEADER, row):
            if any(ch in value for ch in "\r\n\t\x00"):
                raise MigrationError(
                    f"{e['paper_id']}.{col} contains a control character; a NUL "
                    f"would survive the append and then truncate the value when "
                    f"pandas reads it back on the default C engine"
                )
        for col in ("paper_id", "title", "authors", "year", "journal", "doi"):
            if not row[EXPECTED_HEADER.index(col)].strip():
                raise MigrationError(f"{e['paper_id']}.{col} is empty")


def render_new_lines(new_papers: tuple[dict[str, str], ...]) -> list[str]:
    """Render the new rows with csv quoting, without any line terminator."""
    out: list[str] = []
    for e in new_papers:
        buf = io.StringIO()
        csv.writer(buf, lineterminator="").writerow(build_row(e))
        out.append(buf.getvalue())
    return out


def verify(
    path: Path,
    original_lines: list[str],
    terminator: str,
    ends_with_terminator: bool,
    n_original_rows: int,
    new_papers: tuple[dict[str, str], ...],
    dataset_sha_before: str | None,
    dataset: Path,
) -> None:
    """Plan section 6. Raises on any failure."""
    term_after, ends_after = detect_format(path)
    if term_after != terminator:
        raise MigrationError(
            f"line terminator changed: {terminator!r} -> {term_after!r}"
        )
    if ends_after != ends_with_terminator:
        raise MigrationError(
            f"final-newline state changed: {ends_with_terminator} -> {ends_after}"
        )

    lines_after = read_physical_lines(path, terminator)
    expected_total = n_original_rows + 1 + len(new_papers)
    if len(lines_after) != expected_total:
        raise MigrationError(
            f"expected {expected_total} physical lines, found {len(lines_after)}"
        )

    # Post-condition 2: the original lines are byte-identical, compared raw.
    head_after = lines_after[: len(original_lines)]
    drifted = [
        i + 1
        for i, (a, b) in enumerate(zip(original_lines, head_after))
        if a != b
    ]
    if drifted:
        raise MigrationError(
            f"physical lines changed that this migration does not name, at "
            f"lines {drifted[:10]}; the guarantee is byte-identity, not "
            f"cell-identity"
        )

    header, rows = read_rows(path)
    if len(rows) != n_original_rows + len(new_papers):
        raise MigrationError(
            f"expected {n_original_rows + len(new_papers)} data rows, "
            f"found {len(rows)}"
        )
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != EXPECTED_COLUMNS]
    if ragged:
        raise MigrationError(f"ragged rows after append at csv lines {ragged}")

    idx = {name: header.index(name) for name in header}
    ids = [row[idx["paper_id"]] for row in rows]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise MigrationError(f"duplicate paper_id after append: {dupes}")
    for e in new_papers:
        if e["paper_id"] not in ids:
            raise MigrationError(f"{e['paper_id']} missing after append")

    dois = [row[idx["doi"]].strip().lower() for row in rows if row[idx["doi"]].strip()]
    if len(set(dois)) != len(dois):
        dupes = sorted({d for d in dois if dois.count(d) > 1})
        raise MigrationError(f"duplicate DOI after append: {dupes}")

    # Post-condition 7: this migration must not touch the dataset.
    if dataset_sha_before is not None and dataset.exists():
        if _sha256(dataset) != dataset_sha_before:
            raise MigrationError(
                "data/raw/measurements_v0.1.csv changed; this migration must "
                "not touch the dataset"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracking", type=Path, default=DEFAULT_TRACKING)
    parser.add_argument("--screening", type=Path, default=DEFAULT_SCREENING_JSON)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument("--expected-rows", type=int, default=DEFAULT_EXPECTED_ROWS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    path = args.tracking
    if not path.exists():
        print(f"error: {path} does not exist", file=sys.stderr)
        return 1

    # Taken FIRST, before any other work. An earlier draft took this baseline
    # just before the write, which meant post-condition 7 could not see the
    # dataset being touched by anything that ran before that point -- the guard
    # was hashing the already-corrupted file and comparing it with itself.
    dataset_sha_before = _sha256(args.dataset) if args.dataset.exists() else None

    try:
        new_papers = load_new_papers(args.screening)
    except (MigrationError, OSError) as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 1

    terminator, ends_with_terminator = detect_format(path)
    original_lines = read_physical_lines(path, terminator)
    header, rows = read_rows(path)

    try:
        check_preconditions(
            header, rows, original_lines, args.expected_rows, new_papers
        )
    except MigrationError as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 1

    new_lines = render_new_lines(new_papers)

    print(f"{path}: {len(rows)} rows -> {len(rows) + len(new_papers)}")
    print(f"  terminator {terminator!r}, trailing newline {ends_with_terminator}")
    print(f"  appending {len(new_papers)} rows, "
          f"{new_papers[0]['paper_id']}..{new_papers[-1]['paper_id']}")
    print("  modifying 0 existing cells")
    if args.dry_run:
        print("\n--dry-run: nothing written. First and last new lines:")
        print(f"  {new_lines[0][:150]}")
        print(f"  {new_lines[-1][:150]}")
        return 0

    backup = args.backup_dir / f"paper_tracking.before_phase_d.{_sha256(path)[:12]}.csv"
    shutil.copy2(path, backup)
    print(f"  backup: {backup}")

    body = terminator.join(original_lines + new_lines)
    if ends_with_terminator:
        body += terminator
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(body)

    try:
        verify(
            path, original_lines, terminator, ends_with_terminator, len(rows),
            new_papers, dataset_sha_before, args.dataset,
        )
    except MigrationError as exc:
        shutil.copy2(backup, path)
        print(f"post-condition failed, original restored: {exc}", file=sys.stderr)
        return 1

    print(f"  verified: lines 1-{len(original_lines)} byte-identical, "
          f"{len(new_papers)} rows appended")
    print(f"  sha256: {_sha256(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
