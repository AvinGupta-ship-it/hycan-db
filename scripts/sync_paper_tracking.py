#!/usr/bin/env python3
"""Bring references/paper_tracking.csv into agreement with the dataset.

Applies docs/migration_paper_tracking_plan.md and nothing else. Reads and
writes raw CSV cells through the csv module rather than pandas, so every cell
this script does not name is byte-identical by construction and verify() can
assert exactly that.

Refuses to run twice. See the plan for why each change is made and for the
decision that v1.0 single-reader papers stay `extracted` rather than becoming
`verified`.

Usage:
    python3 scripts/sync_paper_tracking.py --dry-run
    python3 scripts/sync_paper_tracking.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import re
import shutil
import sys
from pathlib import Path

DEFAULT_TRACKING = Path("references/paper_tracking.csv")
DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_BACKUP_DIR = Path("/tmp")

DEFAULT_EXPECTED_ROWS = 30
EXPECTED_COLUMNS = 13

PAPER_ID_RE = re.compile(r"^HYC-\d{4}$")

# --- The plan, §2 and §3, encoded so the script cannot drift from it. --------

MALFORMED_ID_FIX = {"HYC-009": "HYC-0009"}

# Papers extracted under the v2.0 dual-agent protocol -> `verified`.
DUAL_AGENT_VERIFIED = (
    "HYC-0009",
    "HYC-0011",
    "HYC-0012",
    "HYC-0015",
    "HYC-0017",
    "HYC-0019",
    "HYC-0022",
    "HYC-0025",
    "HYC-0026",
    "HYC-0029",
)

# Papers extracted under the v1.0 human protocol -> stay `extracted`.
SINGLE_READER_EXTRACTED = (
    "HYC-0001",
    "HYC-0002",
    "HYC-0004",
    "HYC-0005",
    "HYC-0013",
    "HYC-0016",
    "HYC-0018",
    "HYC-0020",
    "HYC-0021",
    "HYC-0023",
    "HYC-0027",
)

# Dates taken from the dated section headers in docs/ai_usage_log.md (plan §3.3).
EXTRACTION_DATES = {
    "HYC-0009": "2026-09-25",
    "HYC-0011": "2026-09-25",
    "HYC-0012": "2026-09-25",
    "HYC-0015": "2026-09-25",
    "HYC-0016": "2026-08-30",
    "HYC-0017": "2026-09-25",
    "HYC-0018": "2026-08-31",
    "HYC-0019": "2026-09-25",
    "HYC-0022": "2026-09-25",
    "HYC-0023": "2026-08-30",
    "HYC-0025": "2026-09-25",
    "HYC-0026": "2026-09-25",
    "HYC-0029": "2026-09-25",
}


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

    `references/paper_tracking.csv` is CRLF with **no** trailing newline. Writing
    it back with csv.writer's defaults changed the bytes of all 31 physical lines
    (1-30 lost their CR, 31 gained a terminator) while leaving every cell value
    correct, which is precisely the kind of whole-file
    rewrite the plan's "byte-identical by construction" guarantee exists to
    prevent. The cell-level check passed and the bytes were wrong, so the format
    is detected and reproduced rather than assumed.
    """
    raw = path.read_bytes()
    terminator = "\r\n" if b"\r\n" in raw else "\n"
    ends_with_terminator = raw.endswith(b"\n")
    return terminator, ends_with_terminator


def check_preconditions(
    header: list[str], rows: list[list[str]], expected_rows: int
) -> dict[str, int]:
    if len(header) != EXPECTED_COLUMNS:
        raise MigrationError(
            f"expected {EXPECTED_COLUMNS} columns in the tracking file, "
            f"found {len(header)}"
        )
    for name in ("paper_id", "extraction_status", "extraction_date"):
        if name not in header:
            raise MigrationError(f"tracking file has no {name!r} column")
    if expected_rows >= 0 and len(rows) != expected_rows:
        raise MigrationError(
            f"expected {expected_rows} data rows, found {len(rows)}; "
            f"pass --expected-rows to override"
        )
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != len(header)]
    if ragged:
        raise MigrationError(f"ragged rows at csv lines {ragged}")

    idx = {name: header.index(name) for name in header}
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row[idx["extraction_status"]]] = (
            status_counts.get(row[idx["extraction_status"]], 0) + 1
        )

    # Refuse to re-run: if the dual-agent papers already read `verified`,
    # this migration has been applied.
    already = {
        row[idx["paper_id"]]
        for row in rows
        if row[idx["extraction_status"]] == "verified"
    }
    if already & set(DUAL_AGENT_VERIFIED):
        raise MigrationError(
            "this migration has already been applied: "
            f"{sorted(already & set(DUAL_AGENT_VERIFIED))} already read "
            f"'verified'. Refusing to run twice."
        )
    return status_counts


def apply_changes(
    header: list[str], rows: list[list[str]]
) -> tuple[list[list[str]], list[str]]:
    """Return new rows plus a human-readable list of every cell changed."""
    idx = {name: header.index(name) for name in header}
    new_rows = [list(row) for row in rows]
    changes: list[str] = []

    for row in new_rows:
        pid = row[idx["paper_id"]]

        # §3.1 — the malformed id, corrected first so the rest can match on it.
        if pid in MALFORMED_ID_FIX:
            fixed = MALFORMED_ID_FIX[pid]
            row[idx["paper_id"]] = fixed
            changes.append(f"{pid}: paper_id -> {fixed}")
            pid = fixed

        # §3.2 — status for the dual-agent papers.
        if pid in DUAL_AGENT_VERIFIED:
            before = row[idx["extraction_status"]]
            if before != "verified":
                row[idx["extraction_status"]] = "verified"
                changes.append(f"{pid}: extraction_status {before!r} -> 'verified'")

        # §3.3 — fill an empty extraction_date; never overwrite one.
        if pid in EXTRACTION_DATES and not row[idx["extraction_date"]].strip():
            row[idx["extraction_date"]] = EXTRACTION_DATES[pid]
            changes.append(
                f"{pid}: extraction_date '' -> {EXTRACTION_DATES[pid]!r}"
            )

    return new_rows, changes


def verify(
    header: list[str],
    before: list[list[str]],
    after: list[list[str]],
    dataset_papers: set[str],
    expected_changed_cells: int | None = 24,
) -> None:
    """Assert every post-condition in plan §4. Raises on any failure."""
    idx = {name: header.index(name) for name in header}

    if len(after) != len(before):
        raise MigrationError(
            f"row count changed: {len(before)} -> {len(after)}"
        )

    # Post-condition 2: only the named cells changed.
    changed: list[tuple[int, str]] = []
    for line, (old, new) in enumerate(zip(before, after), start=2):
        if len(old) != len(new):
            raise MigrationError(f"column count changed on csv line {line}")
        for col, (a, b) in enumerate(zip(old, new)):
            if a != b:
                changed.append((line, header[col]))
    allowed = {"paper_id", "extraction_status", "extraction_date"}
    illegal = [(line, col) for line, col in changed if col not in allowed]
    if illegal:
        raise MigrationError(f"cells changed outside the plan's scope: {illegal}")
    if expected_changed_cells is not None and len(changed) != expected_changed_cells:
        by_col: dict[str, int] = {}
        for _, col in changed:
            by_col[col] = by_col.get(col, 0) + 1
        raise MigrationError(
            f"expected {expected_changed_cells} changed cells, found "
            f"{len(changed)}: {by_col}"
        )

    # Post-condition 3: every paper_id is well formed.
    malformed = [
        row[idx["paper_id"]]
        for row in after
        if not PAPER_ID_RE.match(row[idx["paper_id"]])
    ]
    if malformed:
        raise MigrationError(f"malformed paper_id values remain: {malformed}")

    tracked = {row[idx["paper_id"]]: row for row in after}

    # Post-condition 4: every dataset paper is extracted or verified, with a date.
    for pid in sorted(dataset_papers):
        row = tracked.get(pid)
        if row is None:
            raise MigrationError(f"{pid} is in the dataset with no tracking row")
        status = row[idx["extraction_status"]]
        if status not in {"extracted", "verified"}:
            raise MigrationError(
                f"{pid} is in the dataset but tracked as {status!r}"
            )
        if not row[idx["extraction_date"]].strip():
            raise MigrationError(f"{pid} is extracted with no extraction_date")

    # Post-condition 5: nothing outside the dataset claims to be extracted.
    for pid, row in sorted(tracked.items()):
        if pid in dataset_papers:
            continue
        status = row[idx["extraction_status"]]
        if status in {"extracted", "verified"}:
            raise MigrationError(
                f"{pid} is tracked as {status!r} but has no rows in the dataset"
            )

    # Post-condition 6: the final counts.
    counts: dict[str, int] = {}
    for row in after:
        counts[row[idx["extraction_status"]]] = (
            counts.get(row[idx["extraction_status"]], 0) + 1
        )
    expected_counts = {"extracted": 11, "verified": 10, "not_started": 9}
    if expected_changed_cells is not None and counts != expected_counts:
        raise MigrationError(
            f"expected status counts {expected_counts}, found {counts}"
        )


def dataset_paper_ids(path: Path) -> set[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        col = header.index("paper_id")
        return {row[col] for row in reader if row}


def write_rows(
    path: Path,
    header: list[str],
    rows: list[list[str]],
    terminator: str,
    ends_with_terminator: bool,
) -> None:
    """Write the file back in its own line-ending convention.

    Builds the text with the detected terminator and strips a trailing one when
    the original did not have it, so a line this migration does not name keeps
    its exact bytes.
    """
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
    change. This compares raw lines, which can. `changed_lines` is 1-indexed
    over physical lines, header = line 1.
    """
    before = before_bytes.split(b"\n")
    after = after_bytes.split(b"\n")
    if len(before) != len(after):
        raise MigrationError(
            f"physical line count changed: {len(before)} -> {len(after)}. "
            f"A trailing-newline change does this."
        )
    drifted = [
        i
        for i, (a, b) in enumerate(zip(before, after), start=1)
        if a != b and i not in changed_lines
    ]
    if drifted:
        raise MigrationError(
            f"{len(drifted)} line(s) changed bytes without changing any cell "
            f"this migration names, at physical lines {drifted[:10]}. This is a "
            f"line-ending or quoting rewrite, not a cell edit."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracking", type=Path, default=DEFAULT_TRACKING)
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
        default=24,
        help="changed-cell guard; -1 disables it (used by the tests)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if not args.tracking.exists():
            raise MigrationError(f"{args.tracking} does not exist")
        if not args.dataset.exists():
            raise MigrationError(f"{args.dataset} does not exist")

        dataset_sha_before = _sha256(args.dataset)
        before_bytes = args.tracking.read_bytes()
        terminator, ends_with_terminator = detect_format(args.tracking)
        header, rows = read_rows(args.tracking)
        check_preconditions(header, rows, args.expected_rows)
        papers = dataset_paper_ids(args.dataset)

        new_rows, changes = apply_changes(header, rows)
        expected_cells = (
            None if args.expected_changed_cells < 0 else args.expected_changed_cells
        )
        verify(header, rows, new_rows, papers, expected_cells)

        # Physical lines this migration is allowed to rewrite: data row i is
        # physical line i + 1, because the header is line 1.
        changed_lines = {
            i + 1
            for i, (old, new) in enumerate(zip(rows, new_rows), start=1)
            if old != new
        }

        print(
            f"{len(changes)} cell change(s) across {len(changed_lines)} line(s); "
            f"line terminator {terminator!r}, "
            f"trailing newline {ends_with_terminator}"
        )
        for line in changes:
            print(f"  {line}")

        if args.dry_run:
            print("\n--dry-run: nothing written.")
            return 0

        stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        backup = args.backup_dir / f"paper_tracking.pre_sync.{stamp}.csv"
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.tracking, backup)
        print(f"\nbacked up to {backup}")

        write_rows(
            args.tracking, header, new_rows, terminator, ends_with_terminator
        )

        # Re-read from disk and re-verify. A self-report is not evidence (§3.8).
        header_after, rows_after = read_rows(args.tracking)
        if header_after != header:
            raise MigrationError("header changed on write")
        verify(header, rows, rows_after, papers, expected_cells)
        assert_untouched_lines_are_byte_identical(
            before_bytes, args.tracking.read_bytes(), changed_lines
        )

        if _sha256(args.dataset) != dataset_sha_before:
            raise MigrationError("the dataset changed; this script must not touch it")

        print(f"wrote {args.tracking}, re-read and re-verified from disk")
        print(f"dataset sha256 unchanged: {dataset_sha_before}")
        return 0

    except MigrationError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
