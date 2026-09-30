#!/usr/bin/env python3
"""Record which Phase D full texts were obtained.

Applies docs/migration_pdf_obtained_plan.md and nothing else: 30 of the 35 Phase
D rows move `pdf_obtained` from `no` to `yes`, and the 5 that were not obtained
gain a note saying so, with the date and the reason.

All five are Royal Society of Chemistry titles, so this is a systematic
exclusion by publisher rather than a random loss, and three of them are the
`volumetric` papers. The plan's §3 says why that has to be reported rather than
absorbed. The note in the tracking file is what keeps it visible to anyone
reading the source of truth instead of the prose.

Reads and writes raw CSV lines rather than round-tripping through pandas, so
every line this script does not name is byte-identical by construction and
verify() asserts that as bytes, not as parsed cells.

Refuses to run twice.

Usage:
    python3 scripts/migrate_pdf_obtained.py --dry-run
    python3 scripts/migrate_pdf_obtained.py
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
DEFAULT_EXPECTED_ROWS = 65

EXPECTED_COLUMNS = 13
EXPECTED_HEADER = [
    "paper_id", "title", "authors", "year", "journal", "doi", "search_source",
    "screening_decision", "exclusion_reason", "pdf_obtained",
    "extraction_status", "extraction_date", "notes",
]

# The 30 whose full text is in the Project, verified against its file listing.
OBTAINED = (
    "HYC-0031", "HYC-0032", "HYC-0033", "HYC-0034", "HYC-0037", "HYC-0038",
    "HYC-0039", "HYC-0040", "HYC-0041", "HYC-0042", "HYC-0043", "HYC-0044",
    "HYC-0045", "HYC-0046", "HYC-0047", "HYC-0048", "HYC-0049", "HYC-0050",
    "HYC-0051", "HYC-0052", "HYC-0053", "HYC-0057", "HYC-0058", "HYC-0059",
    "HYC-0060", "HYC-0061", "HYC-0062", "HYC-0063", "HYC-0064", "HYC-0065",
)

# The 5 that were not, with the reason recorded against each.
NOT_OBTAINED_NOTE = (
    "full text not retrieved 2026-09-30 (RSC, no institutional access); "
    "screened in and still wanted"
)
NOT_OBTAINED = ("HYC-0035", "HYC-0036", "HYC-0054", "HYC-0055", "HYC-0056")

PHASE_D = tuple(sorted(OBTAINED + NOT_OBTAINED))


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
    """Physical line n must hold data row n-1, or the byte check is unsound.

    A newline inside a quoted cell breaks that mapping. Copied from
    migrate_relabel.py, which added this precondition for the same reason.
    """
    if len(lines) != n_rows + 1:
        raise MigrationError(
            f"{len(lines)} physical lines for {n_rows} data rows plus a header; "
            f"a row must span more than one line, so the byte-level check "
            f"would be comparing the wrong things"
        )


def check_preconditions(
    header: list[str], rows: list[list[str]], lines: list[str], expected_rows: int
) -> None:
    if header != EXPECTED_HEADER:
        raise MigrationError(f"unexpected header: {header}")
    if expected_rows >= 0 and len(rows) != expected_rows:
        raise MigrationError(
            f"expected {expected_rows} data rows, found {len(rows)}; "
            f"pass --expected-rows to override"
        )
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != EXPECTED_COLUMNS]
    if ragged:
        raise MigrationError(f"ragged rows at csv lines {ragged}")
    assert_line_mapping(lines, len(rows))

    idx = {name: header.index(name) for name in header}
    ids = [row[idx["paper_id"]] for row in rows]
    for pid in PHASE_D:
        if ids.count(pid) != 1:
            raise MigrationError(
                f"{pid} appears {ids.count(pid)} times; expected exactly once"
            )

    already = [
        row[idx["paper_id"]] for row in rows
        if row[idx["paper_id"]] in OBTAINED
        and row[idx["pdf_obtained"]].strip().lower() == "yes"
    ]
    if already:
        raise MigrationError(
            f"this migration has already been applied: {sorted(already)} "
            f"already read pdf_obtained='yes'. Refusing to run twice."
        )


def apply_changes(
    header: list[str], rows: list[list[str]]
) -> tuple[list[list[str]], list[str]]:
    idx = {name: header.index(name) for name in header}
    new_rows = [list(row) for row in rows]
    changes: list[str] = []
    for row in new_rows:
        pid = row[idx["paper_id"]]
        if pid in OBTAINED:
            before = row[idx["pdf_obtained"]]
            row[idx["pdf_obtained"]] = "yes"
            changes.append(f"{pid}: pdf_obtained {before!r} -> 'yes'")
        elif pid in NOT_OBTAINED:
            note = row[idx["notes"]]
            if NOT_OBTAINED_NOTE not in note:
                row[idx["notes"]] = (
                    f"{note}; {NOT_OBTAINED_NOTE}" if note.strip()
                    else NOT_OBTAINED_NOTE
                )
                changes.append(f"{pid}: notes += not-retrieved record")
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
    dataset_sha_before: str | None,
    dataset: Path,
) -> None:
    """Every post-condition in plan §5."""
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

    idx = {name: header.index(name) for name in header}

    # Post-condition 2: any row this migration does not name is byte-identical.
    for line_no, (old_line, new_line, old_row) in enumerate(
        zip(original_lines[1:], lines_after[1:], before), start=2
    ):
        if old_row[idx["paper_id"]] in PHASE_D:
            continue
        if old_line != new_line:
            raise MigrationError(
                f"csv line {line_no} changed and is outside the Phase D block; "
                f"the guarantee is byte-identity, not cell-identity"
            )
    if original_lines[0] != lines_after[0]:
        raise MigrationError("the header line changed")

    # Post-condition 6: only pdf_obtained and notes ever differ.
    allowed = {"pdf_obtained", "notes"}
    yes = no = 0
    for old, new in zip(before, after):
        pid = old[idx["paper_id"]]
        for col, (a, b) in enumerate(zip(old, new)):
            if a != b and header[col] not in allowed:
                raise MigrationError(
                    f"{pid}.{header[col]} changed; outside the plan's scope"
                )
        if pid in OBTAINED:
            if new[idx["pdf_obtained"]] != "yes":
                raise MigrationError(f"{pid} should read 'yes'")
            yes += 1
        elif pid in NOT_OBTAINED:
            if new[idx["pdf_obtained"]] != "no":
                raise MigrationError(f"{pid} should still read 'no'")
            if NOT_OBTAINED_NOTE not in new[idx["notes"]]:
                raise MigrationError(f"{pid} is missing its not-retrieved note")
            no += 1
    if (yes, no) != (len(OBTAINED), len(NOT_OBTAINED)):
        raise MigrationError(
            f"expected {len(OBTAINED)} obtained and {len(NOT_OBTAINED)} not, "
            f"got {yes} and {no}"
        )

    bad = sorted({
        row[idx["pdf_obtained"]] for row in after
        if row[idx["pdf_obtained"]] not in ("yes", "no")
    })
    if bad:
        raise MigrationError(f"pdf_obtained holds values outside yes/no: {bad}")

    if dataset_sha_before is not None and dataset.exists():
        if _sha256(dataset) != dataset_sha_before:
            raise MigrationError(
                "the dataset changed; this migration must not touch it"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracking", type=Path, default=DEFAULT_TRACKING)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument("--expected-rows", type=int, default=DEFAULT_EXPECTED_ROWS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    path = args.tracking
    if not path.exists():
        print(f"error: {path} does not exist", file=sys.stderr)
        return 1

    # Taken FIRST, before any other work, so the guard cannot hash an
    # already-corrupted file and compare it with itself.
    dataset_sha_before = _sha256(args.dataset) if args.dataset.exists() else None

    terminator, ends_with_terminator = detect_format(path)
    original_lines = read_physical_lines(path, terminator)
    header, rows = read_rows(path)

    try:
        check_preconditions(header, rows, original_lines, args.expected_rows)
    except MigrationError as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 1

    new_rows, changes = apply_changes(header, rows)
    print(f"{path}: {len(rows)} rows, {len(changes)} cell change(s)")
    print(f"  {len(OBTAINED)} obtained -> pdf_obtained='yes'")
    print(f"  {len(NOT_OBTAINED)} not obtained -> note recorded, stays 'no'")
    if args.dry_run:
        print("\n--dry-run: nothing written. Changes:")
        for line in changes:
            print(f"  {line}")
        return 0

    backup = args.backup_dir / f"paper_tracking.before_obtained.{_sha256(path)[:12]}.csv"
    shutil.copy2(path, backup)
    print(f"  backup: {backup}")

    body = terminator.join([original_lines[0]] + render(new_rows))
    if ends_with_terminator:
        body += terminator
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(body)

    try:
        verify(path, header, rows, original_lines, terminator,
               ends_with_terminator, dataset_sha_before, args.dataset)
    except MigrationError as exc:
        shutil.copy2(backup, path)
        print(f"post-condition failed, original restored: {exc}", file=sys.stderr)
        return 1

    print(f"  verified: rows outside the Phase D block byte-identical")
    print(f"  sha256: {_sha256(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
