#!/usr/bin/env python3
"""Record an extraction in references/paper_tracking.csv -- manual §9.1 step 15.

This is the ROUTINE tool for the step this project has skipped more than any
other: ten consecutive papers in Phase C, then HYC-0007 and HYC-0024 one commit
after that was fixed. Each time the repair was a one-off migration, and
`scripts/sync_paper_tracking.py` refuses to run twice because it encodes one
specific backfill. After every extraction the project has therefore faced a
protected file, a routine update, and no routine tool. This is the tool.

Applies docs/migration_record_extraction_plan.md and nothing else: for ONE
paper, sets `extraction_status` and `extraction_date`, and optionally appends to
`notes`. No other row and no other column changes.

Reads and writes raw CSV lines rather than round-tripping through pandas, so
every line this script does not name is byte-identical by construction and
verify() asserts that as bytes, not as parsed cells.

Usage:
    python3 scripts/record_extraction.py --paper-id HYC-0031 --status extracted --dry-run
    python3 scripts/record_extraction.py --paper-id HYC-0031 --status extracted
    python3 scripts/record_extraction.py --paper-id HYC-0031 --status verified \\
        --verified-by "Agent B: 1856/1920 agreed, 8 disputed, 6 upheld"
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import shutil
import sys
from pathlib import Path

DEFAULT_TRACKING = Path("references/paper_tracking.csv")
DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_BACKUP_DIR = Path("/tmp")

EXPECTED_COLUMNS = 13
EXPECTED_HEADER = [
    "paper_id", "title", "authors", "year", "journal", "doi", "search_source",
    "screening_decision", "exclusion_reason", "pdf_obtained",
    "extraction_status", "extraction_date", "notes",
]

STATUSES = ("not_started", "extracted", "verified")


class MigrationError(RuntimeError):
    """Raised when a precondition or post-condition fails. Nothing is written."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def detect_format(path: Path) -> tuple[str, bool]:
    """This file's line terminator and whether it ends with one.

    CRLF with no trailing newline. csv.writer's defaults would rewrite every
    line's bytes while leaving each cell correct, which is the failure §6.7
    records. Detect and reproduce; never assume.
    """
    raw = path.read_bytes()
    return ("\r\n" if b"\r\n" in raw else "\n"), raw.endswith(b"\n")


def read_physical_lines(path: Path, terminator: str) -> list[str]:
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
    """Physical line n must hold data row n-1, or the byte check is unsound."""
    if len(lines) != n_rows + 1:
        raise MigrationError(
            f"{len(lines)} physical lines for {n_rows} data rows plus a header; "
            f"a row must span more than one line, so the byte-level check "
            f"would be comparing the wrong things"
        )


def dataset_row_count(dataset: Path, paper_id: str) -> int | None:
    """How many dataset rows this paper has. None if the dataset is missing."""
    if not dataset.exists():
        return None
    with dataset.open(encoding="utf-8", newline="") as handle:
        return sum(1 for r in csv.DictReader(handle) if r.get("paper_id") == paper_id)


def check_preconditions(
    header: list[str],
    rows: list[list[str]],
    lines: list[str],
    paper_id: str,
    status: str,
    date: str,
    n_dataset_rows: int | None,
) -> int:
    """Returns the index into `rows` of the target row."""
    if header != EXPECTED_HEADER:
        raise MigrationError(f"unexpected header: {header}")
    if status not in STATUSES:
        raise MigrationError(f"status {status!r} is not one of {STATUSES}")
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != EXPECTED_COLUMNS]
    if ragged:
        raise MigrationError(f"ragged rows at csv lines {ragged}")
    assert_line_mapping(lines, len(rows))

    idx = {name: header.index(name) for name in header}
    hits = [i for i, row in enumerate(rows) if row[idx["paper_id"]] == paper_id]
    if len(hits) != 1:
        raise MigrationError(
            f"{paper_id} appears {len(hits)} times in the tracking file; "
            f"expected exactly once"
        )
    target = hits[0]
    row = rows[target]

    decision = row[idx["screening_decision"]].strip().lower()
    if decision != "include":
        raise MigrationError(
            f"{paper_id} has screening_decision={decision!r}, not 'include'. A "
            f"paper excluded at screening cannot have been extracted; one of the "
            f"two records is wrong and this script will not paper over it"
        )

    obtained = row[idx["pdf_obtained"]].strip().lower()
    if obtained != "yes":
        raise MigrationError(
            f"{paper_id} has pdf_obtained={obtained!r}, not 'yes'. A full text "
            f"that was never retrieved cannot have been extracted"
        )

    if n_dataset_rows is not None and n_dataset_rows == 0:
        raise MigrationError(
            f"the dataset contains no rows for {paper_id}, so recording "
            f"{status!r} would assert an extraction that did not happen"
        )

    if (row[idx["extraction_status"]] == status
            and row[idx["extraction_date"]] == date):
        raise MigrationError(
            f"{paper_id} already reads extraction_status={status!r} and "
            f"extraction_date={date!r}. Refusing to run twice."
        )
    return target


def apply_change(
    header: list[str],
    rows: list[list[str]],
    target: int,
    status: str,
    date: str,
    append_note: str | None,
) -> tuple[list[list[str]], list[str]]:
    idx = {name: header.index(name) for name in header}
    new_rows = [list(row) for row in rows]
    row = new_rows[target]
    changes = []

    before_status = row[idx["extraction_status"]]
    if before_status != status:
        row[idx["extraction_status"]] = status
        changes.append(f"extraction_status {before_status!r} -> {status!r}")

    before_date = row[idx["extraction_date"]]
    if before_date != date:
        row[idx["extraction_date"]] = date
        changes.append(f"extraction_date {before_date!r} -> {date!r}")

    if append_note:
        note = row[idx["notes"]]
        if append_note not in note:
            row[idx["notes"]] = f"{note}; {append_note}" if note.strip() else append_note
            changes.append("notes += extraction record")
    return new_rows, changes


def render(rows: list[list[str]]) -> list[str]:
    out: list[str] = []
    for row in rows:
        buf = io.StringIO()
        csv.writer(buf, lineterminator="").writerow(row)
        out.append(buf.getvalue())
    return out


def verify(
    path: Path,
    header: list[str],
    before: list[list[str]],
    original_lines: list[str],
    terminator: str,
    ends_with_terminator: bool,
    target: int,
    status: str,
    date: str,
    dataset_sha_before: str | None,
    dataset: Path,
) -> None:
    """Every post-condition in plan §4."""
    term_after, ends_after = detect_format(path)
    if term_after != terminator:
        raise MigrationError(f"terminator changed: {terminator!r} -> {term_after!r}")
    if ends_after != ends_with_terminator:
        raise MigrationError("final-newline state changed")

    lines_after = read_physical_lines(path, terminator)
    if len(lines_after) != len(original_lines):
        raise MigrationError(
            f"physical line count changed: {len(original_lines)} -> "
            f"{len(lines_after)}"
        )

    _, after = read_rows(path)
    if len(after) != len(before):
        raise MigrationError(f"row count changed: {len(before)} -> {len(after)}")

    if original_lines[0] != lines_after[0]:
        raise MigrationError("the header line changed")

    # Post-condition 2: every line but the target's is byte-identical.
    for i, (old_line, new_line) in enumerate(
        zip(original_lines[1:], lines_after[1:])
    ):
        if i == target:
            continue
        if old_line != new_line:
            raise MigrationError(
                f"csv line {i + 2} changed and is not the target row; the "
                f"guarantee is byte-identity, not cell-identity"
            )

    idx = {name: header.index(name) for name in header}
    allowed = {"extraction_status", "extraction_date", "notes"}
    for col, (a, b) in enumerate(zip(before[target], after[target])):
        if a != b and header[col] not in allowed:
            raise MigrationError(
                f"{header[col]} changed on the target row; outside the plan's scope"
            )

    row = after[target]
    if row[idx["extraction_status"]] != status:
        raise MigrationError(f"extraction_status reads {row[idx['extraction_status']]!r}")
    if row[idx["extraction_date"]] != date:
        raise MigrationError(f"extraction_date reads {row[idx['extraction_date']]!r}")

    bad = sorted({r[idx["extraction_status"]] for r in after
                  if r[idx["extraction_status"]] not in STATUSES})
    if bad:
        raise MigrationError(f"extraction_status holds values outside {STATUSES}: {bad}")

    if dataset_sha_before is not None and dataset.exists():
        if _sha256(dataset) != dataset_sha_before:
            raise MigrationError(
                "the dataset changed; this script must not touch it"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--status", required=True, choices=STATUSES)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--verified-by", default=None,
                        help="required with --status verified; the §3.2 record")
    parser.add_argument("--append-note", default=None)
    parser.add_argument("--tracking", type=Path, default=DEFAULT_TRACKING)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    # §5.2 defines `verified` as the §3.2 protocol completed with all disputes
    # resolved. The word is not written without the evidence that makes it true.
    if args.status == "verified" and not args.verified_by:
        print("error: --status verified requires --verified-by, which records the "
              "dual-agent outcome (manual §5.2, §3.2)", file=sys.stderr)
        return 1

    path = args.tracking
    if not path.exists():
        print(f"error: {path} does not exist", file=sys.stderr)
        return 1

    # Taken FIRST, before any other work, so the guard cannot hash an
    # already-corrupted file and compare it with itself.
    dataset_sha_before = _sha256(args.dataset) if args.dataset.exists() else None
    n_dataset_rows = dataset_row_count(args.dataset, args.paper_id)

    terminator, ends_with_terminator = detect_format(path)
    original_lines = read_physical_lines(path, terminator)
    header, rows = read_rows(path)

    note = args.append_note
    if args.verified_by and not note:
        note = args.verified_by

    try:
        target = check_preconditions(header, rows, original_lines, args.paper_id,
                                     args.status, args.date, n_dataset_rows)
    except MigrationError as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 1

    new_rows, changes = apply_change(header, rows, target, args.status,
                                     args.date, note)
    print(f"{path}: {args.paper_id} (csv line {target + 2})")
    print(f"  dataset rows for this paper: "
          f"{'unknown' if n_dataset_rows is None else n_dataset_rows}")
    for line in changes:
        print(f"  {line}")
    if not changes:
        print("  nothing to change")
    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return 0

    backup = args.backup_dir / f"paper_tracking.before_{args.paper_id}.{_sha256(path)[:12]}.csv"
    shutil.copy2(path, backup)
    print(f"  backup: {backup}")

    body = terminator.join([original_lines[0]] + render(new_rows))
    if ends_with_terminator:
        body += terminator
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(body)

    try:
        verify(path, header, rows, original_lines, terminator,
               ends_with_terminator, target, args.status, args.date,
               dataset_sha_before, args.dataset)
    except MigrationError as exc:
        shutil.copy2(backup, path)
        print(f"post-condition failed, original restored: {exc}", file=sys.stderr)
        return 1

    print("  verified: every other line byte-identical")
    print(f"  sha256: {_sha256(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
