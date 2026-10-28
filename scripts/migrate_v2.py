#!/usr/bin/env python3
"""Apply schema v2 to data/raw/measurements_v0.1.csv (docs/migration_v2_plan.md).

Appends the 30 schema v2 columns at physical positions 68-97, every cell empty.
Empty means "not yet coded" (docs/data_dictionary.md, Schema v2 Fields), so no
existing row's meaning changes and no existing cell is touched. The v1.0
re-verification (docs/v1_protocol.md §9) fills these columns later, row by row,
from the source papers.

Reads and writes raw CSV cells through the csv module, reproduces the file's line
terminator and final-newline state, and checks after writing that every original
line survives byte-for-byte as a prefix of its new line. Refuses to run twice.

Usage:
    python3 scripts/migrate_v2.py --dry-run
    python3 scripts/migrate_v2.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import shutil
import sys
from pathlib import Path

DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_BACKUP_DIR = Path("/tmp")
EXPECTED_OLD_COLUMNS = 67
DEFAULT_EXPECTED_ROWS = 521

# Physical order of the appended columns (plan §1). Must match the order the
# fields are declared in src/hycan/schema.py's schema v2 block.
NEW_COLUMNS: list[str] = [
    "basis_stated",
    "basis_inferred",
    "basis_evidence",
    "wt_pct_convention",
    "wt_pct_convention_source",
    "value_kind",
    "isotherm_id",
    "isotherm_branch",
    "isotherm_point_count",
    "temperature_inferred",
    "data_location",
    "digitization_uncertainty_wt_pct",
    "surface_area_probe_gas",
    "bet_range_stated",
    "bet_consistency_criteria_stated",
    "area_same_sample",
    "degas_temperature_c",
    "degas_duration_h",
    "degas_end_pressure_pa",
    "sample_mass_mg",
    "h2_purity_pct",
    "free_volume_calibration",
    "instrument_identified",
    "calibration_described",
    "replicates_reported",
    "measuring_lab_id",
    "material_identity",
    "duplicate_of",
    "selection_route",
    "frame_id",
]
EXPECTED_NEW_COLUMNS = EXPECTED_OLD_COLUMNS + len(NEW_COLUMNS)


class MigrationError(RuntimeError):
    """A precondition or post-condition failed. Nothing is written."""


def detect_format(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    return ("\r\n" if b"\r\n" in raw else "\n"), raw.endswith(b"\n")


def load(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise MigrationError(f"{path} is empty")
    return rows[0], rows[1:]


def save(
    path: Path,
    header: list[str],
    rows: list[list[str]],
    terminator: str,
    ends_with_terminator: bool,
) -> None:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator=terminator)
    writer.writerow(header)
    writer.writerows(rows)
    text = buffer.getvalue()
    if not ends_with_terminator and text.endswith(terminator):
        text = text[: -len(terminator)]
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def check_preconditions(
    header: list[str], rows: list[list[str]], expected_rows: int
) -> None:
    if len(header) == EXPECTED_NEW_COLUMNS:
        raise MigrationError(
            f"this file already has {EXPECTED_NEW_COLUMNS} columns; the schema v2 "
            f"migration has already been applied. Refusing to run twice."
        )
    if len(header) != EXPECTED_OLD_COLUMNS:
        raise MigrationError(
            f"expected {EXPECTED_OLD_COLUMNS} columns, found {len(header)}"
        )
    already = [name for name in NEW_COLUMNS if name in header]
    if already:
        raise MigrationError(f"these schema v2 columns already exist: {already}")
    if expected_rows >= 0 and len(rows) != expected_rows:
        raise MigrationError(
            f"expected {expected_rows} data rows, found {len(rows)}; "
            f"pass --expected-rows to override"
        )
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != len(header)]
    if ragged:
        raise MigrationError(f"ragged rows at csv lines {ragged}")


def migrate(
    header: list[str], rows: list[list[str]]
) -> tuple[list[str], list[list[str]]]:
    return header + NEW_COLUMNS, [row + [""] * len(NEW_COLUMNS) for row in rows]


def verify(old_header, old_rows, new_header, new_rows) -> None:
    if new_header != old_header + NEW_COLUMNS:
        raise MigrationError("header is not the old header followed by the v2 columns")
    if len(new_rows) != len(old_rows):
        raise MigrationError(f"row count changed: {len(old_rows)} -> {len(new_rows)}")
    for line, (old, new) in enumerate(zip(old_rows, new_rows), start=2):
        if new[: len(old)] != old:
            raise MigrationError(f"csv line {line}: an original cell changed")
        if any(cell != "" for cell in new[len(old) :]):
            raise MigrationError(f"csv line {line}: a v2 cell is not empty")


def assert_prefix_bytes(before: bytes, after: bytes) -> None:
    b_lines, a_lines = before.split(b"\n"), after.split(b"\n")
    if len(b_lines) != len(a_lines):
        raise MigrationError(
            f"physical line count changed: {len(b_lines)} -> {len(a_lines)}"
        )
    drifted = [
        i
        for i, (a, b) in enumerate(zip(b_lines, a_lines), start=1)
        if a and not b.startswith(a.rstrip(b"\r"))
    ]
    if drifted:
        raise MigrationError(f"original bytes not preserved on lines {drifted[:10]}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=DEFAULT_EXPECTED_ROWS,
        help="row-count guard; -1 disables it (used by the tests)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.dataset.exists():
            raise MigrationError(f"{args.dataset} does not exist")
        before = args.dataset.read_bytes()
        terminator, ends = detect_format(args.dataset)
        header, rows = load(args.dataset)
        check_preconditions(header, rows, args.expected_rows)
        new_header, new_rows = migrate(header, rows)
        verify(header, rows, new_header, new_rows)
        print(
            f"{len(header)} -> {len(new_header)} columns, {len(rows)} rows, "
            f"0 existing cells changed"
        )
        if args.dry_run:
            print("--dry-run: nothing written.")
            return 0
        stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        backup = args.backup_dir / f"measurements_v0.1.prev2.{stamp}.csv"
        shutil.copy2(args.dataset, backup)
        print(f"backed up to {backup}")
        save(args.dataset, new_header, new_rows, terminator, ends)
        header_after, rows_after = load(args.dataset)
        verify(header, rows, header_after, rows_after)
        assert_prefix_bytes(before, args.dataset.read_bytes())
        print(f"wrote {args.dataset}, re-read and re-verified from disk")
        return 0
    except MigrationError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
