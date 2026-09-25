#!/usr/bin/env python3
"""Schema v1.1 -> v1.2 dataset migration (stages 1-3 of the v1.2 gap inventory).

Plan: docs/migration_v1_2_plan.md. Run with --dry-run first.

What this does to data/raw/measurements_v0.1.csv:

  Appends eleven columns at the END, physical positions 41-51, each with a
  default that makes every existing row valid without inspection:

    41 uptake_bound                  = "exact"
    42 temperature_unstated          = "false"
    43 pressure_unstated             = "false"
    44 measurement_mode              = "isothermal"
    45 reference_temperature_k       = ""
    46 metal_element                 = ""
    47 metal_loading_wt_pct          = ""
    48 residual_metal_element        = ""
    49 residual_metal_wt_pct         = ""
    50 dopant_concentration_wt_pct   = ""
    51 dopant_concentration_method   = ""

Nothing else is touched. This migration is purely additive: the verification
below asserts that ZERO cells changed in physical columns 1-40, which is a
stronger claim than v1.1's migration could make (it relabelled 34 cells).

Why csv, not pandas
-------------------
pandas would reformat cells it was never asked to change -- float precision,
quoting, empty-vs-NaN -- across every row. This reads and writes raw cell
strings, so an unmodified cell is byte-identical by construction and the
verification can assert exactly that.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
from datetime import datetime

DATASET = "data/raw/measurements_v0.1.csv"

# (column name, default value) in physical append order.
NEW_COLUMNS: list[tuple[str, str]] = [
    ("uptake_bound", "exact"),
    ("temperature_unstated", "false"),
    ("pressure_unstated", "false"),
    ("measurement_mode", "isothermal"),
    ("reference_temperature_k", ""),
    ("metal_element", ""),
    ("metal_loading_wt_pct", ""),
    ("residual_metal_element", ""),
    ("residual_metal_wt_pct", ""),
    ("dopant_concentration_wt_pct", ""),
    ("dopant_concentration_method", ""),
]

EXPECTED_OLD_COLUMNS = 40

# A guard that you are migrating the file you think you are, not a property of
# the migration. It is a CLI option rather than a constant so the script itself
# is testable against a small fixture: a migration script that can only be
# exercised by running it on the real dataset is one whose correctness rests on
# a single irreversible attempt (§6.7, "a passing test suite is weak evidence").
DEFAULT_EXPECTED_ROWS = 156


def load(path: str) -> tuple[list[str], list[list[str]]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise SystemExit(f"{path} is empty")
    return rows[0], rows[1:]


def save(path: str, header: list[str], rows: list[list[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def migrate(
    header: list[str], rows: list[list[str]]
) -> tuple[list[str], list[list[str]]]:
    for name, _ in NEW_COLUMNS:
        if name in header:
            raise SystemExit(
                f"{name} is already present; this migration has already run"
            )
    if len(header) != EXPECTED_OLD_COLUMNS:
        raise SystemExit(
            f"expected {EXPECTED_OLD_COLUMNS} columns before migration, "
            f"found {len(header)}"
        )

    widths = {len(row) for row in rows}
    if widths != {EXPECTED_OLD_COLUMNS}:
        raise SystemExit(
            f"rows of differing width before migration: {sorted(widths)}; "
            f"expected only {EXPECTED_OLD_COLUMNS}"
        )

    defaults = [default for _, default in NEW_COLUMNS]
    new_rows = [list(row) + list(defaults) for row in rows]
    return header + [name for name, _ in NEW_COLUMNS], new_rows


def verify(old_path: str, new_path: str, expected_rows: int) -> int:
    """Re-read both files from disk and assert exactly what changed (§3.8)."""
    old_header, old_rows = load(old_path)
    new_header, new_rows = load(new_path)

    problems: list[str] = []

    if expected_rows >= 0 and len(old_rows) != expected_rows:
        problems.append(
            f"expected {expected_rows} rows before migration, "
            f"found {len(old_rows)}"
        )
    if len(new_rows) != len(old_rows):
        problems.append(f"row count {len(old_rows)} -> {len(new_rows)}")
    if old_header != new_header[: len(old_header)]:
        problems.append("the first 40 column names or their order changed")

    appended = new_header[len(old_header):]
    expected_names = [name for name, _ in NEW_COLUMNS]
    if appended != expected_names:
        problems.append(f"appended columns are {appended}, expected {expected_names}")

    changed = 0
    wrong_defaults = 0
    for number, (before, after) in enumerate(zip(old_rows, new_rows), start=2):
        if len(after) != len(new_header):
            problems.append(
                f"line {number} has {len(after)} fields, expected {len(new_header)}"
            )
            continue
        for position in range(min(len(before), EXPECTED_OLD_COLUMNS)):
            if before[position] != after[position]:
                changed += 1
                problems.append(
                    f"line {number}: column {position + 1} "
                    f"({new_header[position]}) changed: "
                    f"{before[position]!r} -> {after[position]!r}"
                )
        for offset, (name, default) in enumerate(NEW_COLUMNS):
            got = after[EXPECTED_OLD_COLUMNS + offset]
            if got != default:
                wrong_defaults += 1
                problems.append(
                    f"line {number}: {name} is {got!r}, expected default {default!r}"
                )

    print(f"  rows: {len(old_rows)} -> {len(new_rows)}")
    print(f"  columns: {len(old_header)} -> {len(new_header)}")
    print(f"  cells changed in columns 1-{EXPECTED_OLD_COLUMNS}: {changed} "
          f"(this migration is additive; anything but 0 is a failure)")
    print(f"  appended cells not carrying their default: {wrong_defaults}")
    for problem in problems[:20]:
        print(f"  PROBLEM: {problem}")
    if len(problems) > 20:
        print(f"  ... and {len(problems) - 20} more")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=DATASET)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup-dir", default="/tmp")
    parser.add_argument(
        "--expected-rows", type=int, default=DEFAULT_EXPECTED_ROWS,
        help="row count to require before migrating; -1 disables the guard",
    )
    args = parser.parse_args(argv[1:])

    if not os.path.exists(args.dataset):
        print(f"Error: dataset not found: {args.dataset}")
        return 2

    header, rows = load(args.dataset)
    new_header, new_rows = migrate(header, rows)

    print(f"appending {len(NEW_COLUMNS)} columns at positions "
          f"{len(header) + 1}-{len(new_header)}:")
    for offset, (name, default) in enumerate(NEW_COLUMNS):
        print(f"  {len(header) + 1 + offset:>2}  {name} = {default!r}")
    print("changing 0 cells in the existing columns")

    if args.dry_run:
        os.makedirs(args.backup_dir, exist_ok=True)
        target = os.path.join(args.backup_dir, "migrate_v1_2_dryrun.csv")
        save(target, new_header, new_rows)
        print(f"\nDry run. Result written to {target}; {args.dataset} untouched.")
        return verify(args.dataset, target, args.expected_rows)

    os.makedirs(args.backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(
        args.backup_dir, f"measurements_v0.1.prev1_2.{stamp}.csv"
    )
    shutil.copy2(args.dataset, backup)
    print(f"\nBackup: {backup}")

    save(args.dataset, new_header, new_rows)
    print(f"Written: {args.dataset}")
    return verify(backup, args.dataset, args.expected_rows)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
