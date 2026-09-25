#!/usr/bin/env python3
"""
Schema v1.0 -> v1.1 dataset migration (manual §8.5 gaps 1-4, §8.6 cleanups).

Plan: docs/migration_v1.1_plan.md. Run with --dry-run first.

What this does to data/raw/measurements_v0.1.csv:

  1. appends two columns at the END, physical positions 39 and 40:
     surface_area_method, ultramicropore_volume_cm3_g
  2. surface_area_method = "BET" where bet_surface_area_m2_g is populated,
     "unspecified" otherwise
  3. synthesis_method "other" -> "carbide_chlorination" on HYC-0023, whose
     every material_description reads "TiC-derived CDC, chlorinated at N C"
  4. material_class "graphene" -> "reduced_graphene_oxide" where the
     material_description begins "Reduced graphene oxide" (HYC-0016)

Everything else is left exactly as it was found.

Why csv, not pandas
-------------------
pandas would reformat cells it was never asked to change — float precision,
quoting, empty-vs-NaN — across all 119 rows. This reads and writes raw cell
strings, so an unmodified cell is byte-identical by construction, and the
verification below can assert exactly that.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
from datetime import datetime

DATASET = "data/raw/measurements_v0.1.csv"

NEW_COLUMNS = ["surface_area_method", "ultramicropore_volume_cm3_g"]

EXPECTED_ROWS = 119
EXPECTED_OLD_COLUMNS = 38


def load(path: str) -> tuple[list[str], list[list[str]]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[0], rows[1:]


def save(path: str, header: list[str], rows: list[list[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def migrate(
    header: list[str], rows: list[list[str]]
) -> tuple[list[str], list[list[str]], list[dict]]:
    """Return the new header, the new rows, and a log of every cell changed."""
    index = {name: position for position, name in enumerate(header)}
    for name in NEW_COLUMNS:
        if name in index:
            raise SystemExit(
                f"{name} is already present; this migration has already run"
            )

    changes: list[dict] = []
    new_rows: list[list[str]] = []

    for row in rows:
        row = list(row)
        paper = row[index["paper_id"]]
        measurement = row[index["measurement_id"]]

        # §8.6 - carbide chlorination
        position = index["synthesis_method"]
        description = row[index["material_description"]]
        if row[position] == "other" and "chlorinated at" in description:
            changes.append({
                "id": measurement, "field": "synthesis_method",
                "old": row[position], "new": "carbide_chlorination",
            })
            row[position] = "carbide_chlorination"

        # §8.6 - HYC-0016 material_class precision
        position = index["material_class"]
        if (row[position] == "graphene"
                and description.startswith("Reduced graphene oxide")):
            changes.append({
                "id": measurement, "field": "material_class",
                "old": row[position], "new": "reduced_graphene_oxide",
            })
            row[position] = "reduced_graphene_oxide"

        # §8.5 gap 1 - surface_area_method, appended
        bet = row[index["bet_surface_area_m2_g"]].strip()
        row.append("BET" if bet else "unspecified")

        # §8.5 gap 4 - ultramicropore_volume_cm3_g, appended empty.
        # Backfilling HYC-0021 requires the source paper and is a separate
        # commit; see docs/migration_v1.1_plan.md §3.
        row.append("")

        new_rows.append(row)
        del paper

    return header + NEW_COLUMNS, new_rows, changes


def verify(old_path: str, new_path: str) -> int:
    """Re-read both files from disk and assert exactly what changed (§3.8)."""
    old_header, old_rows = load(old_path)
    new_header, new_rows = load(new_path)

    problems: list[str] = []

    if len(new_rows) != len(old_rows):
        problems.append(f"row count {len(old_rows)} -> {len(new_rows)}")
    if len(old_rows) != EXPECTED_ROWS:
        problems.append(
            f"expected {EXPECTED_ROWS} rows before migration, "
            f"found {len(old_rows)}"
        )
    if old_header != new_header[:len(old_header)]:
        problems.append("the first 38 column names or their order changed")
    if new_header[len(old_header):] != NEW_COLUMNS:
        problems.append(
            f"appended columns are {new_header[len(old_header):]}, "
            f"expected {NEW_COLUMNS}"
        )

    changed = 0
    for number, (before, after) in enumerate(zip(old_rows, new_rows), start=2):
        if len(after) != len(new_header):
            problems.append(
                f"line {number} has {len(after)} fields, "
                f"expected {len(new_header)}"
            )
            continue
        for position in range(EXPECTED_OLD_COLUMNS):
            if before[position] != after[position]:
                changed += 1
                if new_header[position] not in ("synthesis_method", "material_class"):
                    problems.append(
                        f"line {number}: unexpected change in {new_header[position]}: "
                        f"{before[position]!r} -> {after[position]!r}"
                    )

    print(f"  rows: {len(old_rows)} -> {len(new_rows)}")
    print(f"  columns: {len(old_header)} -> {len(new_header)}")
    print(f"  cells changed in columns 1-38: {changed}")
    for problem in problems:
        print(f"  PROBLEM: {problem}")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=DATASET)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup-dir", default="/tmp")
    args = parser.parse_args(argv[1:])

    if not os.path.exists(args.dataset):
        print(f"Error: dataset not found: {args.dataset}")
        return 2

    header, rows = load(args.dataset)
    new_header, new_rows, changes = migrate(header, rows)

    print(f"{len(changes)} cell(s) to change in existing columns:")
    for field in sorted({c["field"] for c in changes}):
        affected = [c for c in changes if c["field"] == field]
        sample = affected[0]
        print(f"  {field}: {len(affected)} rows, "
              f"{sample['old']!r} -> {sample['new']!r}")
    print(f"appending {len(NEW_COLUMNS)} columns: {', '.join(NEW_COLUMNS)}")

    if args.dry_run:
        target = os.path.join(args.backup_dir, "migrate_v1_1_dryrun.csv")
        save(target, new_header, new_rows)
        print(f"\nDry run. Result written to {target}; {args.dataset} untouched.")
        return verify(args.dataset, target)

    os.makedirs(args.backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(
        args.backup_dir, f"measurements_v0.1.premigration.{stamp}.csv"
    )
    shutil.copy2(args.dataset, backup)
    print(f"\nBackup: {backup}")

    save(args.dataset, new_header, new_rows)
    print(f"Written: {args.dataset}")
    return verify(backup, args.dataset)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
