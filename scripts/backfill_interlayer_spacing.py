#!/usr/bin/env python3
"""Backfill `interlayer_spacing_nm` on HYC-0015's graphene-oxide and rGO rows.

Applies docs/migration_held_rows_plan.md §3 and nothing else. Both numbers are
already in the corpus as prose -- each row's `material_description` states its
spacing -- and schema v1.3 added the numeric field without backfilling the two
rows that could already fill it.

**This is not tidying.** The same commit writes 0.339 nm on the pristine graphite.
Leaving the graphene oxide and rGO null would make `interlayer_spacing_nm` mean
"graphite only", and a reader filtering on it would conclude the paper measured no
other spacing -- when the collapse from 8.84 A to 3.85 A on reduction is the
paper's entire thesis. Both values were re-verified against the PDF by Agent B
rather than copied from the prose.

Reads and writes raw CSV cells through the csv module, so every cell this script
does not name is byte-identical by construction and verify() can assert exactly
that. Refuses to run twice.

Usage:
    python3 scripts/backfill_interlayer_spacing.py --dry-run
    python3 scripts/backfill_interlayer_spacing.py
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
DEFAULT_EXPECTED_ROWS = 227
EXPECTED_COLUMNS = 67

SCOPE_COLUMNS = frozenset({"interlayer_spacing_nm", "notes"})

# Plan §3. The values are the paper's, in nm: 8.84 A and 3.85 A.
BACKFILL = {
    "HYC-0015-M1": "0.884",
    "HYC-0015-M2": "0.385",
}

# The paper's own inconsistency travels with the rGO row. Agent B upheld the
# assignment to rGO on four grounds; the loose phrase is recorded rather than
# smoothed over.
NOTES_APPEND = {
    "HYC-0015-M2": (
        " interlayer_spacing_nm = 0.385 records the 3.85 A this row's own "
        "material_description already stated in prose; schema v1.3 added the field "
        "and did not backfill it. THE PAPER'S SENTENCE IS INTERNALLY INCONSISTENT: "
        "it assigns the 23.72 deg / 3.85 A peak to 'the chemical reduction by "
        "hydrogen', while the Experimental section reduces with hydrazine hydrate "
        "and no hydrogen gas is involved in making rGO. The assignment to rGO is "
        "upheld on four grounds: Fig. 5's caption names exactly three patterns (GO, "
        "rGO, and GO exposed to hydrogen) and the prose assigns exactly three peaks, "
        "the third named explicitly as the hydrogenated GO, so 23.72 deg is the rGO "
        "by elimination; the mechanism attached to it is the rGO one ('removal of "
        "functional group and moisture by chemical and thermal reduction', matching a "
        "hydrazine step run at 60 C); the 8.84 -> 3.85 A collapse is the paper's "
        "thesis; and the hydrogenated GO is treated in the next sentences as a GO "
        "rather than a reduced product."
    ),
}

EXPECTED_CHANGED_CELLS = len(BACKFILL) + len(NOTES_APPEND)


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
    """Return this file's line terminator and whether it ends with one.

    Detected rather than assumed: a cell-level verification cannot certify a
    byte-level guarantee, and writing a CRLF file back with csv.writer's defaults
    once changed every line's bytes in this project while every cell stayed
    correct.
    """
    raw = path.read_bytes()
    return ("\r\n" if b"\r\n" in raw else "\n"), raw.endswith(b"\n")


def assert_line_mapping_is_sound(raw: bytes, n_rows: int) -> None:
    """Assert physical line n holds data row n-1, which the byte check needs.

    A newline inside a quoted cell breaks the mapping, and `notes` on this corpus
    runs to several thousand characters, so this is a live risk.
    """
    lines = raw.split(b"\n")
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    if len(lines) != n_rows + 1:
        raise MigrationError(
            f"{len(lines)} physical lines for {n_rows} data rows plus a header; "
            f"expected {n_rows + 1}. A cell contains an embedded newline, so the "
            f"byte-level check below cannot be trusted."
        )


def check_preconditions(
    header: list[str], rows: list[list[str]], expected_rows: int
) -> None:
    if len(header) != EXPECTED_COLUMNS:
        raise MigrationError(
            f"expected {EXPECTED_COLUMNS} columns, found {len(header)}"
        )
    for name in sorted(SCOPE_COLUMNS | {"measurement_id"}):
        if name not in header:
            raise MigrationError(f"dataset has no {name!r} column")
    if expected_rows >= 0 and len(rows) != expected_rows:
        raise MigrationError(
            f"expected {expected_rows} data rows, found {len(rows)}; "
            f"pass --expected-rows to override"
        )

    idx = {name: header.index(name) for name in header}
    by_id = {row[idx["measurement_id"]]: row for row in rows}
    missing = sorted(set(BACKFILL) - set(by_id))
    if missing:
        raise MigrationError(
            f"rows named by the plan are not in the dataset: {missing}"
        )

    already = sorted(
        mid for mid in BACKFILL if by_id[mid][idx["interlayer_spacing_nm"]].strip()
    )
    if already:
        raise MigrationError(
            f"this migration has already been applied: {already} already carry an "
            f"interlayer_spacing_nm. Refusing to run twice."
        )


def apply_changes(
    header: list[str], rows: list[list[str]]
) -> tuple[list[list[str]], list[str]]:
    idx = {name: header.index(name) for name in header}
    new_rows = [list(row) for row in rows]
    changes: list[str] = []

    for row in new_rows:
        mid = row[idx["measurement_id"]]
        if mid in BACKFILL:
            row[idx["interlayer_spacing_nm"]] = BACKFILL[mid]
            changes.append(f"{mid}: interlayer_spacing_nm '' -> {BACKFILL[mid]!r}")
        if mid in NOTES_APPEND:
            suffix = NOTES_APPEND[mid]
            if suffix.strip() in row[idx["notes"]]:
                raise MigrationError(
                    f"{mid}: notes already contains the text this migration appends"
                )
            row[idx["notes"]] = row[idx["notes"]].rstrip() + suffix
            changes.append(f"{mid}: notes, appended {len(suffix)} chars")

    return new_rows, changes


def verify(
    header: list[str],
    before: list[list[str]],
    after: list[list[str]],
    expected_changed_cells: int | None = EXPECTED_CHANGED_CELLS,
) -> int:
    """Assert every post-condition in plan §7. Returns the changed-cell count."""
    idx = {name: header.index(name) for name in header}

    if len(after) != len(before):
        raise MigrationError(f"row count changed: {len(before)} -> {len(after)}")

    changed: list[tuple[int, str]] = []
    for line, (old, new) in enumerate(zip(before, after), start=2):
        if len(old) != len(new):
            raise MigrationError(f"column count changed on csv line {line}")
        for col, (a, b) in enumerate(zip(old, new)):
            if a != b:
                changed.append((line, header[col]))
    illegal = [(line, col) for line, col in changed if col not in SCOPE_COLUMNS]
    if illegal:
        raise MigrationError(f"cells changed outside the plan's scope: {illegal}")
    if expected_changed_cells is not None and len(changed) != expected_changed_cells:
        raise MigrationError(
            f"expected {expected_changed_cells} changed cells, found {len(changed)}"
        )

    populated = {
        row[idx["measurement_id"]]
        for row in after
        if row[idx["interlayer_spacing_nm"]].strip()
    }
    if expected_changed_cells is not None:
        # Plan §7 post-condition 2: the field stops being an empty column. The
        # graphite row was appended separately, so all three must be present.
        expected = set(BACKFILL) | {"HYC-0015-M3"}
        if populated != expected:
            raise MigrationError(
                f"interlayer_spacing_nm should be populated on exactly "
                f"{sorted(expected)}, found {sorted(populated)}"
            )

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
    """Assert every line the plan does not name is byte-for-byte unchanged.

    verify() compares parsed cells, which cannot see a line-ending or quoting
    change. This compares raw lines, which can.
    """
    before = before_bytes.split(b"\n")
    after = after_bytes.split(b"\n")
    if len(before) != len(after):
        raise MigrationError(
            f"physical line count changed: {len(before)} -> {len(after)}"
        )
    drifted = [
        i
        for i, (a, b) in enumerate(zip(before, after), start=1)
        if a != b and i not in changed_lines
    ]
    if drifted:
        raise MigrationError(
            f"{len(drifted)} line(s) changed bytes without changing any cell this "
            f"migration names, at physical lines {drifted[:10]}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=DEFAULT_EXPECTED_ROWS,
        help="row count guard; -1 disables it (used by the tests)",
    )
    parser.add_argument(
        "--expected-changed-cells",
        type=int,
        default=EXPECTED_CHANGED_CELLS,
        help="changed-cell guard; -1 disables it (used by the tests)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if not args.dataset.exists():
            raise MigrationError(f"{args.dataset} does not exist")

        before_bytes = args.dataset.read_bytes()
        terminator, ends_with_terminator = detect_format(args.dataset)
        header, rows = read_rows(args.dataset)
        assert_line_mapping_is_sound(before_bytes, len(rows))
        check_preconditions(header, rows, args.expected_rows)

        new_rows, changes = apply_changes(header, rows)
        expected_cells = (
            None if args.expected_changed_cells < 0 else args.expected_changed_cells
        )
        changed_cells = verify(header, rows, new_rows, expected_cells)

        changed_lines = {
            i + 1
            for i, (old, new) in enumerate(zip(rows, new_rows), start=1)
            if old != new
        }
        print(
            f"{changed_cells} cell(s) changed across {len(changed_lines)} line(s); "
            f"line terminator {terminator!r}, trailing newline {ends_with_terminator}"
        )
        for line in changes:
            print(f"  {line}")

        if args.dry_run:
            print("\n--dry-run: nothing written.")
            return 0

        stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        backup = args.backup_dir / f"measurements.pre_interlayer.{stamp}.csv"
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.dataset, backup)
        print(f"\nbacked up to {backup}")

        write_rows(args.dataset, header, new_rows, terminator, ends_with_terminator)

        # Re-read from disk and re-verify. A self-report is not evidence (§3.8).
        header_after, rows_after = read_rows(args.dataset)
        if header_after != header:
            raise MigrationError("header changed on write")
        verify(header, rows, rows_after, expected_cells)
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
