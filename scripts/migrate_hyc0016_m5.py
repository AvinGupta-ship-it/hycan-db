#!/usr/bin/env python3
"""Correct HYC-0016-M5: the reference activated carbon mislabeled as KOH r-GO.

Applies docs/migration_hyc0016_m5_plan.md and nothing else. M5 is the 293 K
measurement of Klechikov 2015's internal reference activated carbon (Fig. 3,
red), the same physical sample as the 77 K row HYC-0016-M11 (both BET 1830
m2/g). It was extracted as reduced_graphene_oxide / koh_activation and then
swept into scripts/migrate_relabel.py's KOH relabel onto chemical_activation.
This script sets M5's four sample-identity fields to match M11, rewrites its
notes to explain the correction, and updates the now-stale verification flag on
both M5 and M11.

Reads and writes raw CSV cells through the csv module rather than pandas, so
every cell this script does not name is byte-identical by construction and
verify() can assert exactly that (§3.8: a self-report is not evidence).

Refuses to run twice: the preconditions require M5 to hold its pre-correction
values, which it does not after one run.

Usage:
    python3 scripts/migrate_hyc0016_m5.py --dry-run
    python3 scripts/migrate_hyc0016_m5.py
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

DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_BACKUP_DIR = Path("/tmp")

EXPECTED_COLUMNS = 67
# M5: 4 identity fields + notes + verified_by = 6; plus verified_by on the other
# 13 HYC-0016 rows (the flag is the paper-level record, duplicated per row) = 13.
EXPECTED_CHANGED_CELLS = 19

PAPER = "HYC-0016"
EXPECTED_PAPER_ROWS = 14  # HYC-0016-M1 .. M14
M5 = "HYC-0016-M5"
M11 = "HYC-0016-M11"

# Columns this migration is allowed to touch. Anything else changing is a bug.
SCOPE_COLUMNS = frozenset(
    {
        "material_class",
        "synthesis_method",
        "activation_method",
        "material_description",
        "notes",
        "verified_by",
    }
)

# --- Plan §1: the four sample-identity fields, as (from, to). ---------------
# M5 must currently hold every "from" value; this is also the refuse-to-re-run
# guard, since after one run it holds the "to" values instead.
IDENTITY_FIELDS: dict[str, tuple[str, str]] = {
    "material_class": ("reduced_graphene_oxide", "activated_carbon"),
    "synthesis_method": ("chemical_activation", "other"),
    "activation_method": ("koh_activation", "none"),
    "material_description": (
        "Reduced graphene oxide, BET 1830 m2/g",
        "Reference activated carbon sample, BET 1830 m2/g",
    ),
}

# --- Plan §2: the notes sentence prepended to M5. ---------------------------
M5_NOTES_PREFIX = (
    "Paper's internal reference sample of activated carbon, not a graphene "
    "material; shown in red in Fig. 3 (the 293 K gravimetric isotherms) and the "
    "same physical sample as the 77 K reference-carbon row HYC-0016-M11 (both "
    "BET 1830 m2/g). Reclassified from reduced_graphene_oxide / "
    "chemical_activation / koh_activation to activated_carbon / other / none by "
    "scripts/migrate_hyc0016_m5.py (docs/migration_hyc0016_m5_plan.md) after the "
    "2026-10-05 dual-agent verification identified the original label as the "
    "reference carbon mislabeled as KOH-activated r-GO; the row was also removed "
    "from scripts/migrate_relabel.py's KOH relabel scope in the same change. "
)

# --- Plan §3: the verified_by flag sentence, replaced on M5 and M11. --------
VERIFIED_BY_OLD = (
    "FLAGGED for a dedicated relabel migration: the BET-1830 293 K row (M5) is "
    "the reference activated carbon (same sample as the 77 K AC row M11), "
    "mislabeled reduced_graphene_oxide/KOH here and in "
    "scripts/migrate_relabel.py (SYNTHESIS_RELABEL); left uncorrected to avoid "
    "rewriting that migration."
)
VERIFIED_BY_NEW = (
    "The BET-1830 293 K row (M5) is the reference activated carbon (same sample "
    "as the 77 K AC row M11); the verification pass found it mislabeled "
    "reduced_graphene_oxide/KOH both in the dataset and in "
    "scripts/migrate_relabel.py, and scripts/migrate_hyc0016_m5.py "
    "(docs/migration_hyc0016_m5_plan.md) subsequently corrected M5 to "
    "activated_carbon/other/none and removed it from that migration's scope."
)


class MigrationError(RuntimeError):
    """Raised when a precondition or post-condition fails. Nothing is written."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise MigrationError(f"{path} is empty")
    return rows[0], rows[1:]


def detect_format(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    terminator = "\r\n" if b"\r\n" in raw else "\n"
    return terminator, raw.endswith(b"\n")


def assert_line_mapping_is_sound(raw: bytes, n_rows: int) -> None:
    """Assert physical line n holds data row n-1, which the byte check needs."""
    lines = raw.split(b"\n")
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    if len(lines) != n_rows + 1:
        raise MigrationError(
            f"{len(lines)} physical lines for {n_rows} data rows plus a header; "
            f"expected {n_rows + 1}. A cell contains an embedded newline, so the "
            f"byte-level check below cannot be trusted."
        )


def check_preconditions(header: list[str], rows: list[list[str]]) -> None:
    if len(header) != EXPECTED_COLUMNS:
        raise MigrationError(
            f"expected {EXPECTED_COLUMNS} columns, found {len(header)}"
        )
    for name in sorted(SCOPE_COLUMNS | {"measurement_id", "paper_id"}):
        if name not in header:
            raise MigrationError(f"dataset has no {name!r} column")
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != len(header)]
    if ragged:
        raise MigrationError(f"ragged rows at csv lines {ragged}")

    idx = {name: header.index(name) for name in header}
    by_id = {row[idx["measurement_id"]]: row for row in rows}

    for mid in (M5, M11):
        if mid not in by_id:
            raise MigrationError(f"{mid} is not in the dataset")

    # Refuse to re-run: M5 must still hold every pre-correction "from" value.
    m5 = by_id[M5]
    for column, (before, _after) in IDENTITY_FIELDS.items():
        got = m5[idx[column]]
        if got != before:
            raise MigrationError(
                f"{M5}.{column} is {got!r}, expected {before!r}. This migration "
                f"has already been applied, or the row has changed since the plan "
                f"was written. Refusing to run."
            )

    # The verified_by flag is the paper-level verification record, duplicated on
    # every HYC-0016 row. It must appear on all and only the paper's rows, so the
    # one-sentence swap keeps that record uniform across the paper.
    paper_rows = sorted(
        row[idx["measurement_id"]] for row in rows if row[idx["paper_id"]] == PAPER
    )
    if len(paper_rows) != EXPECTED_PAPER_ROWS:
        raise MigrationError(
            f"expected {EXPECTED_PAPER_ROWS} {PAPER} rows, found {len(paper_rows)}"
        )
    carriers = sorted(
        row[idx["measurement_id"]]
        for row in rows
        if VERIFIED_BY_OLD in row[idx["verified_by"]]
    )
    if carriers != paper_rows:
        raise MigrationError(
            f"the verified_by flag sentence should appear on exactly the "
            f"{EXPECTED_PAPER_ROWS} {PAPER} rows; found it on {carriers}"
        )
    # The notes prefix must not already be present (another re-run guard).
    if M5_NOTES_PREFIX.strip() in by_id[M5][idx["notes"]]:
        raise MigrationError(f"{M5} notes already carry the correction prefix")


def apply_changes(
    header: list[str], rows: list[list[str]]
) -> tuple[list[list[str]], list[str]]:
    idx = {name: header.index(name) for name in header}
    new_rows = [list(row) for row in rows]
    changes: list[str] = []

    for row in new_rows:
        mid = row[idx["measurement_id"]]

        if mid == M5:
            for column, (before, after) in IDENTITY_FIELDS.items():
                row[idx[column]] = after
                changes.append(f"{mid}: {column} {before!r} -> {after!r}")
            row[idx["notes"]] = M5_NOTES_PREFIX + row[idx["notes"]]
            changes.append(f"{mid}: notes, prepended {len(M5_NOTES_PREFIX)} chars")

        # verified_by: swap the one stale flag sentence wherever it occurs (all
        # HYC-0016 rows carry the same paper-level record).
        text = row[idx["verified_by"]]
        if VERIFIED_BY_OLD in text:
            if text.count(VERIFIED_BY_OLD) != 1:
                raise MigrationError(
                    f"{mid}: verified_by flag occurs "
                    f"{text.count(VERIFIED_BY_OLD)} time(s), expected 1"
                )
            row[idx["verified_by"]] = text.replace(VERIFIED_BY_OLD, VERIFIED_BY_NEW)
            changes.append(f"{mid}: verified_by, replaced 1 sentence")

    return new_rows, changes


def verify(
    header: list[str], before: list[list[str]], after: list[list[str]]
) -> int:
    idx = {name: header.index(name) for name in header}

    if len(after) != len(before):
        raise MigrationError(f"row count changed: {len(before)} -> {len(after)}")

    changed: list[tuple[int, str, str]] = []
    for line, (old, new) in enumerate(zip(before, after), start=2):
        if len(old) != len(new):
            raise MigrationError(f"column count changed on csv line {line}")
        for col, (a, b) in enumerate(zip(old, new)):
            if a != b:
                changed.append((line, header[col], new[idx["measurement_id"]]))
    illegal = [
        (line, col, mid) for line, col, mid in changed if col not in SCOPE_COLUMNS
    ]
    if illegal:
        raise MigrationError(f"cells changed outside the plan's scope: {illegal}")
    if len(changed) != EXPECTED_CHANGED_CELLS:
        by_col: dict[str, int] = {}
        for _, col, _mid in changed:
            by_col[col] = by_col.get(col, 0) + 1
        raise MigrationError(
            f"expected {EXPECTED_CHANGED_CELLS} changed cells, found "
            f"{len(changed)}: {by_col}"
        )

    by_id_before = {r[idx["measurement_id"]]: r for r in before}
    by_id_after = {r[idx["measurement_id"]]: r for r in after}
    m5, m11 = by_id_after[M5], by_id_after[M11]

    # 1. M5 now holds every target identity value.
    for column, (_before, after_val) in IDENTITY_FIELDS.items():
        if m5[idx[column]] != after_val:
            raise MigrationError(
                f"{M5}.{column} is {m5[idx[column]]!r}, expected {after_val!r}"
            )

    # 2. M5 equals M11 on the four identity fields (same physical sample).
    for column in IDENTITY_FIELDS:
        if m5[idx[column]] != m11[idx[column]]:
            raise MigrationError(
                f"{M5}.{column}={m5[idx[column]]!r} != {M11}.{column}="
                f"{m11[idx[column]]!r}; the two rows must match on identity fields"
            )

    # 3. M5's measurement fields are untouched.
    for column in ("temperature_k", "pressure_bar", "uptake_wt_pct",
                   "source_location", "sample_id", "bet_surface_area_m2_g"):
        if m5[idx[column]] != by_id_before[M5][idx[column]]:
            raise MigrationError(f"{M5}.{column} must not change but did")
    if m5[idx["temperature_k"]] != "293":
        raise MigrationError(f"{M5} temperature_k is not 293")

    # 4. The old M5 signature (rGO / 1830 / 293 K) exists on no row.
    offending = [
        r[idx["measurement_id"]]
        for r in after
        if r[idx["material_class"]] == "reduced_graphene_oxide"
        and r[idx["bet_surface_area_m2_g"]] == "1830"
        and r[idx["temperature_k"]] == "293"
    ]
    if offending:
        raise MigrationError(
            f"a reduced_graphene_oxide / BET 1830 / 293 K row still exists: "
            f"{offending}"
        )

    # 5. The stale verified_by flag is gone everywhere; the new text is on every
    #    HYC-0016 row (the paper-level record stays uniform across the paper).
    still_flagged = [
        r[idx["measurement_id"]]
        for r in after
        if VERIFIED_BY_OLD in r[idx["verified_by"]]
    ]
    if still_flagged:
        raise MigrationError(
            f"the old verified_by flag still appears on {still_flagged}"
        )
    corrected = sorted(
        r[idx["measurement_id"]]
        for r in after
        if VERIFIED_BY_NEW in r[idx["verified_by"]]
    )
    paper_rows = sorted(
        r[idx["measurement_id"]] for r in after if r[idx["paper_id"]] == PAPER
    )
    if corrected != paper_rows:
        raise MigrationError(
            f"the corrected verified_by text should appear on exactly the "
            f"{EXPECTED_PAPER_ROWS} {PAPER} rows; found {corrected}"
        )

    # 6. M5's notes now carry the correction prefix and keep their provenance.
    if M5_NOTES_PREFIX.strip() not in m5[idx["notes"]]:
        raise MigrationError(f"{M5} notes lost the correction prefix")
    if "data/digitizations/HYC-0016_fig3.json" not in m5[idx["notes"]]:
        raise MigrationError(f"{M5} notes lost the original digitization provenance")

    return len(changed)


def write_rows(
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


def assert_untouched_lines_are_byte_identical(
    before_bytes: bytes, after_bytes: bytes, changed_lines: set[int]
) -> None:
    before = before_bytes.split(b"\n")
    after = after_bytes.split(b"\n")
    if len(before) != len(after):
        raise MigrationError(
            f"physical line count changed: {len(before)} -> {len(after)}."
        )
    drifted = [
        i
        for i, (a, b) in enumerate(zip(before, after), start=1)
        if a != b and i not in changed_lines
    ]
    if drifted:
        raise MigrationError(
            f"{len(drifted)} line(s) changed bytes without changing a named cell, "
            f"at physical lines {drifted[:10]}."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if not args.dataset.exists():
            raise MigrationError(f"{args.dataset} does not exist")

        before_bytes = args.dataset.read_bytes()
        terminator, ends_with_terminator = detect_format(args.dataset)
        header, rows = read_rows(args.dataset)
        assert_line_mapping_is_sound(before_bytes, len(rows))
        check_preconditions(header, rows)

        new_rows, changes = apply_changes(header, rows)
        changed_cells = verify(header, rows, new_rows)

        changed_lines = {
            i + 1
            for i, (old, new) in enumerate(zip(rows, new_rows), start=1)
            if old != new
        }

        print(
            f"{changed_cells} cell(s) changed across {len(changed_lines)} line(s) "
            f"in {len(changes)} operation(s); line terminator {terminator!r}, "
            f"trailing newline {ends_with_terminator}"
        )
        for line in changes:
            print(f"  {line}")

        if args.dry_run:
            print("\n--dry-run: nothing written.")
            return 0

        stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        backup = args.backup_dir / f"measurements.pre_m5.{stamp}.csv"
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.dataset, backup)
        print(f"\nbacked up to {backup}")

        write_rows(args.dataset, header, new_rows, terminator, ends_with_terminator)

        header_after, rows_after = read_rows(args.dataset)
        if header_after != header:
            raise MigrationError("header changed on write")
        verify(header, rows, rows_after)
        assert_untouched_lines_are_byte_identical(
            before_bytes, args.dataset.read_bytes(), changed_lines
        )

        print(f"wrote {args.dataset}, re-read and re-verified from disk")
        print(f"sha256 {_sha256(args.dataset)}")
        return 0

    except MigrationError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
