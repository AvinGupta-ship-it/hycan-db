#!/usr/bin/env python3
"""Apply schema v1.3 to data/raw/measurements_v0.1.csv (gaps 3, 6, 10).

Implements docs/migration_v1_3_plan.md and nothing else. Two kinds of change:

  1. Append 16 new columns at physical positions 52-67, each with the default
     that makes every existing row valid unchanged.
  2. Backfill 53 cells across 53 rows (plan §3): ultramicropore_cutoff_nm on 29
     rows, and surface_area_method on 24.

Unlike migrate_v1_2.py this one CHANGES EXISTING CELLS, which is why it is a
version bump rather than a fourth stage, and why verify() checks the changed
cells by name and every other line byte-for-byte.

Reads and writes raw CSV cells through the csv module rather than pandas, so a
cell this script does not name is byte-identical by construction. Detects the
file's own line terminator and final-newline state and reproduces them: the
paper_tracking.csv migration earlier the same day passed its cell-level check
while rewriting all 31 lines' bytes, because that file was CRLF and csv.writer
wrote LF. A cell-level verification cannot certify a byte-level guarantee.

Refuses to run twice.

Usage:
    python3 scripts/migrate_v1_3.py --dry-run
    python3 scripts/migrate_v1_3.py
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

EXPECTED_OLD_COLUMNS = 51
EXPECTED_NEW_COLUMNS = 67
DEFAULT_EXPECTED_ROWS = 206
DEFAULT_EXPECTED_CHANGED_CELLS = 53

# (column name, default written into every existing row) -- plan §1.
# The defaults are what an existing row already asserts implicitly, so no
# existing row's meaning changes by gaining these columns.
NEW_COLUMNS: list[tuple[str, str]] = [
    # Gap 3
    ("micropore_surface_area_m2_g", ""),
    ("external_surface_area_m2_g", ""),
    # Gap 6
    ("pore_volume_method", "unspecified"),
    ("pore_volume_probe_gas", "unspecified"),
    ("micropore_volume_co2_cm3_g", ""),
    ("mesopore_volume_cm3_g", ""),
    ("ultramicropore_cutoff_nm", ""),
    ("pore_diameter_method", "unspecified"),
    # Gap 10
    ("volumetric_capacity_kg_m3", ""),
    ("volumetric_capacity_basis", ""),
    ("volumetric_capacity_includes_compressed_gas", "False"),
    ("adsorbed_phase_density_kg_m3", ""),
    ("packing_density_g_cm3", ""),
    ("skeletal_density_g_cm3", ""),
    ("areal_uptake_g_cm2", ""),
    ("interlayer_spacing_nm", ""),
]

# --- Backfill A: the cutoff every existing ultramicropore value was measured at.
# HYC-0005 and HYC-0021 are the only papers with the field populated and both cut
# at 0.7 nm, which docs/data_dictionary.md has documented since v1.1. This moves
# that fact from documentation into the data, where the new schema check enforces
# it.
ULTRAMICROPORE_CUTOFF_NM = "0.7"

# --- Backfill B: this sample has no area, in a paper that reports areas for its
# others. Previously collapsed onto `unspecified`.
NOT_REPORTED_MEASUREMENT_IDS = {
    "HYC-0016-M13",
    "HYC-0016-M14",
    "HYC-0022-M8",
    "HYC-0022-M9",
    "HYC-0029-M5",
    "HYC-0029-M6",
    "HYC-0029-M7",
    "HYC-0029-M8",
    "HYC-0029-M9",
    "HYC-0029-M10",
    "HYC-0029-M11",
    "HYC-0029-M12",
    "HYC-0029-M13",
    "HYC-0029-M14",
    "HYC-0029-M15",
    "HYC-0029-M16",
}

# --- Backfill C: the paper reports no surface area for ANY sample. These rows
# carried the schema DEFAULT rather than a considered value. Verified against the
# sources by independent locate passes 2026-09-25, not inferred from the empty
# cells -- see plan §3.
NO_AREA_PAPERS = {"HYC-0002", "HYC-0027"}


class MigrationError(RuntimeError):
    """A precondition or post-condition failed. Nothing is written."""


def detect_format(path: Path) -> tuple[str, bool]:
    """Return this file's line terminator and whether it ends with one."""
    raw = path.read_bytes()
    terminator = "\r\n" if b"\r\n" in raw else "\n"
    return terminator, raw.endswith(b"\n")


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
            f"this file already has {EXPECTED_NEW_COLUMNS} columns; the v1.3 "
            f"migration has already been applied. Refusing to run twice."
        )
    if len(header) != EXPECTED_OLD_COLUMNS:
        raise MigrationError(
            f"expected {EXPECTED_OLD_COLUMNS} columns, found {len(header)}"
        )
    for name in ("measurement_id", "paper_id", "surface_area_method",
                 "ultramicropore_volume_cm3_g"):
        if name not in header:
            raise MigrationError(f"dataset has no {name!r} column")
    already = [name for name, _ in NEW_COLUMNS if name in header]
    if already:
        raise MigrationError(f"these v1.3 columns already exist: {already}")
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
) -> tuple[list[str], list[list[str]], list[str]]:
    """Return the new header, new rows, and a description of every cell change."""
    idx = {name: header.index(name) for name in header}
    new_header = list(header) + [name for name, _ in NEW_COLUMNS]
    defaults = [default for _, default in NEW_COLUMNS]
    cutoff_col = len(header) + [n for n, _ in NEW_COLUMNS].index(
        "ultramicropore_cutoff_nm"
    )

    changes: list[str] = []
    new_rows: list[list[str]] = []
    for row in rows:
        new_row = list(row) + list(defaults)
        mid = row[idx["measurement_id"]]
        paper = row[idx["paper_id"]]

        # Backfill A -- the cutoff for every populated ultramicropore volume.
        if row[idx["ultramicropore_volume_cm3_g"]].strip():
            new_row[cutoff_col] = ULTRAMICROPORE_CUTOFF_NM
            changes.append(
                f"{mid}: ultramicropore_cutoff_nm -> {ULTRAMICROPORE_CUTOFF_NM}"
            )

        # Backfills B and C -- surface_area_method, mutually exclusive.
        before = row[idx["surface_area_method"]]
        if mid in NOT_REPORTED_MEASUREMENT_IDS:
            if before != "unspecified":
                raise MigrationError(
                    f"{mid} is in the not_reported backfill list but reads "
                    f"{before!r}, not 'unspecified'"
                )
            new_row[idx["surface_area_method"]] = "not_reported"
            changes.append(f"{mid}: surface_area_method -> not_reported")
        elif paper in NO_AREA_PAPERS:
            if before != "unspecified":
                raise MigrationError(
                    f"{mid} is in a no-area paper but reads {before!r}, "
                    f"not 'unspecified'"
                )
            new_row[idx["surface_area_method"]] = "none"
            changes.append(f"{mid}: surface_area_method -> none")

        new_rows.append(new_row)

    return new_header, new_rows, changes


def verify(
    old_header: list[str],
    old_rows: list[list[str]],
    new_header: list[str],
    new_rows: list[list[str]],
    expected_changed_cells: int | None,
) -> None:
    """Assert every post-condition in plan §5. Raises on any failure."""
    if len(new_header) != len(old_header) + len(NEW_COLUMNS):
        raise MigrationError(
            f"expected {len(old_header) + len(NEW_COLUMNS)} columns, "
            f"found {len(new_header)}"
        )
    if new_header[: len(old_header)] != old_header:
        raise MigrationError("the original columns were reordered or renamed")
    if new_header[len(old_header):] != [name for name, _ in NEW_COLUMNS]:
        raise MigrationError("the new columns are not in the planned order")
    if len(new_rows) != len(old_rows):
        raise MigrationError(f"row count changed: {len(old_rows)} -> {len(new_rows)}")

    allowed = {"surface_area_method", "ultramicropore_cutoff_nm"}
    changed: list[tuple[int, str]] = []
    for line, (old, new) in enumerate(zip(old_rows, new_rows), start=2):
        if len(new) != len(new_header):
            raise MigrationError(f"csv line {line} has {len(new)} cells")
        # Columns 1..51 must be byte-identical except where the plan names them.
        for col, (a, b) in enumerate(zip(old, new[: len(old_header)])):
            if a != b:
                if old_header[col] not in allowed:
                    raise MigrationError(
                        f"csv line {line}: {old_header[col]} changed from {a!r} "
                        f"to {b!r}, outside the plan's scope"
                    )
                changed.append((line, old_header[col]))
        # A new column counts as changed only where it differs from its default.
        for offset, (name, default) in enumerate(NEW_COLUMNS):
            value = new[len(old_header) + offset]
            if value != default:
                if name not in allowed:
                    raise MigrationError(
                        f"csv line {line}: new column {name} was written "
                        f"{value!r} rather than its default {default!r}"
                    )
                changed.append((line, name))

    if expected_changed_cells is not None and len(changed) != expected_changed_cells:
        by_col: dict[str, int] = {}
        for _, col in changed:
            by_col[col] = by_col.get(col, 0) + 1
        raise MigrationError(
            f"expected {expected_changed_cells} changed cells, found "
            f"{len(changed)}: {by_col}"
        )


def assert_untouched_prefix_is_byte_identical(
    before_bytes: bytes, after_bytes: bytes, changed_lines: set[int]
) -> None:
    """Every line the plan does not name keeps its original bytes as a prefix.

    A cell comparison cannot see a line-ending or quoting rewrite; this can. The
    new columns are appended, so an untouched line's original text must survive
    as a literal prefix of its new text.
    """
    before = before_bytes.split(b"\n")
    after = after_bytes.split(b"\n")
    if len(before) != len(after):
        raise MigrationError(
            f"physical line count changed: {len(before)} -> {len(after)}. "
            f"A trailing-newline change does this."
        )
    drifted = []
    for i, (a, b) in enumerate(zip(before, after), start=1):
        if i in changed_lines or not a:
            continue
        if not b.startswith(a.rstrip(b"\r")):
            drifted.append(i)
    if drifted:
        raise MigrationError(
            f"{len(drifted)} line(s) lost their original bytes without any cell "
            f"this migration names changing, at physical lines {drifted[:10]}. "
            f"This is a line-ending or quoting rewrite, not a cell edit."
        )


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
    parser.add_argument(
        "--expected-changed-cells",
        type=int,
        default=DEFAULT_EXPECTED_CHANGED_CELLS,
        help="changed-cell guard; -1 disables it (used by the tests)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if not args.dataset.exists():
            raise MigrationError(f"{args.dataset} does not exist")

        before_bytes = args.dataset.read_bytes()
        terminator, ends_with_terminator = detect_format(args.dataset)
        header, rows = load(args.dataset)
        check_preconditions(header, rows, args.expected_rows)

        new_header, new_rows, changes = migrate(header, rows)
        expected_cells = (
            None if args.expected_changed_cells < 0 else args.expected_changed_cells
        )
        verify(header, rows, new_header, new_rows, expected_cells)

        changed_lines = {
            i + 1
            for i, (old, new) in enumerate(zip(rows, new_rows), start=1)
            if old != new[: len(header)]
        }

        print(
            f"{len(header)} -> {len(new_header)} columns, {len(rows)} rows "
            f"unchanged, {len(changes)} cell change(s) across "
            f"{len(changed_lines)} line(s)"
        )
        print(f"line terminator {terminator!r}, trailing newline "
              f"{ends_with_terminator}")
        for line in changes:
            print(f"  {line}")

        if args.dry_run:
            print("\n--dry-run: nothing written.")
            return 0

        stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        backup = args.backup_dir / f"measurements_v0.1.prev1_3.{stamp}.csv"
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.dataset, backup)
        print(f"\nbacked up to {backup}")

        save(args.dataset, new_header, new_rows, terminator, ends_with_terminator)

        # Re-read from disk and re-verify. A self-report is not evidence (§3.8).
        header_after, rows_after = load(args.dataset)
        if header_after != new_header:
            raise MigrationError("header on disk does not match what was written")
        verify(header, rows, header_after, rows_after, expected_cells)
        assert_untouched_prefix_is_byte_identical(
            before_bytes, args.dataset.read_bytes(), changed_lines
        )

        print(f"wrote {args.dataset}, re-read and re-verified from disk")
        return 0

    except MigrationError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
