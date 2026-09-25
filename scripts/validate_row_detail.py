#!/usr/bin/env python3
"""
Per-row validation detail for HyCAN-DB (manual v2.0 §18 Phase A.1).

``scripts/validate_data.py`` reports error and warning *counts by type*. That is
the right shape for a pass/fail gate and the wrong shape for fixing anything:
"Invalid value: 3" does not say which rows, which field, or what the offending
value was. This script closes that gap. It reports, for every affected row, the
row's identity, the field each message is about, and that field's current value.

Usage
-----
    python3 scripts/validate_row_detail.py [CSV_PATH] [options]

    --errors-only           show only rows with errors
    --warnings-only         show only rows with warnings
    --paper HYC-XXXX        restrict to one paper (repeatable)
    --category TEXT         restrict to messages whose category CONTAINS TEXT
                            (case-insensitive substring, repeatable)
    --field NAME            restrict to messages about NAME (case-insensitive
                            EXACT field name, not a substring; repeatable)
    --summary               category counts plus the affected measurement_ids
    --limit N               print at most N rows of detail (0 = no limit)
    --no-dataset-checks     use validate_row alone; skip the two dataset-level
                            checks (duplicate measurement_id, DOI conflict)

Exit codes
----------
    0  no errors in the selected rows
    1  one or more errors in the selected rows
    2  the CSV path does not exist, is unreadable, or the flags contradict
       each other (--errors-only with --warnings-only)

Design notes
------------
The default path runs :func:`hycan.validate.validate_dataset`, which calls
``validate_row`` on every row and then layers on the two dataset-level checks.
Those two checks are genuinely per-row facts (this row duplicates that one), so
excluding them would make the detail view less complete than the summary view it
replaces. ``--no-dataset-checks`` gives the strict ``validate_row``-only view.

Messages are mapped to the schema fields they are about via
:data:`CATEGORY_FIELDS`. Any category not in that table renders as ``(unmapped)``
rather than raising, so a new rule in ``validate.py`` degrades this script's
output instead of breaking it. ``tests/test_validate_row_detail.py`` checks the
table against a hand-maintained list of triggering rows, which covers every
category the validator emits today but does not detect a category added to
``validate.py`` later. Adding a rule there means adding its trigger here.

This script reads the CSV and never writes to it.
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

from hycan.validate import validate_dataset, validate_row

DEFAULT_CSV = "data/raw/measurements_v0.1.csv"

# Message category -> the schema field(s) the message is about.
# Categories are the text before the first colon (see hycan.validate._category).
# Two categories carry their field in the message itself and are handled
# separately: "Missing required field" and "Invalid value".
CATEGORY_FIELDS: dict[str, tuple[str, ...]] = {
    "Temperature out of range": ("temperature_k",),
    "Pressure out of range": ("pressure_bar",),
    "Pressure above 200 bar": ("pressure_bar",),
    "Uptake out of range": ("uptake_wt_pct",),
    "Uptake above 10 wt%": ("uptake_wt_pct",),
    "Unspecified uptake_type": ("uptake_type",),
    "Micropore volume exceeds total pore volume": (
        "micropore_volume_cm3_g",
        "total_pore_volume_cm3_g",
    ),
    "SWCNT description missing 'single-walled'": (
        "material_class",
        "material_description",
    ),
    "mmol/g and wt% inconsistent": ("uptake_wt_pct", "uptake_mmol_g"),
    "Pre-2005 raw-CNT high uptake (Tier D)": (
        "year",
        "material_class",
        "uptake_wt_pct",
    ),
    "Duplicate measurement_id": ("measurement_id",),
    "DOI metadata conflict": ("doi", "first_author", "year"),
}

# Categories whose field name is the text after the first colon.
_FIELD_IN_MESSAGE = ("Missing required field", "Invalid value")

# Some validator messages name a logical requirement rather than a column.
# "Missing required field: uptake" means "at least one uptake column must be
# populated" (§8.2), and reporting the bare word `uptake` sends the reader
# looking for a column that does not exist. Expand those to the real columns.
PSEUDO_FIELDS: dict[str, tuple[str, ...]] = {
    "uptake": ("uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"),
}

UNMAPPED = "(unmapped)"


# ---------------------------------------------------------------------------
# Message -> fields
# ---------------------------------------------------------------------------

def category_of(message: str) -> str:
    """The category of a message = the text before the first colon."""
    return message.split(":", 1)[0].strip()


def fields_for(message: str) -> tuple[str, ...]:
    """Return the schema field(s) *message* is about, or ``("(unmapped)",)``."""
    category = category_of(message)
    if category in _FIELD_IN_MESSAGE:
        _, _, rest = message.partition(":")
        name = rest.strip()
        if not name:
            return (UNMAPPED,)
        return PSEUDO_FIELDS.get(name, (name,))
    return CATEGORY_FIELDS.get(category, (UNMAPPED,))


def _show_value(row: dict, field: str) -> str:
    """Render a row's value for *field* for display."""
    if field == UNMAPPED or field not in row:
        return ""
    value = row[field]
    try:
        if pd.isna(value):
            return "<empty>"
    except (TypeError, ValueError):
        pass
    text = str(value)
    if text.strip() == "":
        return "<empty>"
    if len(text) > 60:
        text = text[:57] + "..."
    return text


def describe(message: str, row: dict) -> str:
    """One detail line: the message, the field(s) it concerns, and their values."""
    parts = []
    for field in fields_for(message):
        value = _show_value(row, field)
        parts.append(f"{field}={value}" if value else field)
    return f"{message}  [{', '.join(parts)}]"


# ---------------------------------------------------------------------------
# Row identity
# ---------------------------------------------------------------------------

def significant_line_count(path: str) -> int:
    """Physical lines in *path*, ignoring blank lines at the end of the file.

    pandas skips blank lines when parsing, so a file that ends with one still
    yields the expected number of rows. Trailing blanks are therefore discounted
    here rather than absorbed into a tolerance on the comparison: a tolerance
    wide enough to cover a trailing blank line is also wide enough to hide one
    embedded newline, which is the very thing the comparison exists to detect.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        lines = handle.readlines()
    while lines and not lines[-1].strip("\r\n").strip():
        lines.pop()
    return len(lines)


def line_numbers_are_reliable(path: str, n_rows: int) -> bool:
    """True when physical CSV lines map 1:1 onto DataFrame rows.

    A quoted field containing a newline breaks that mapping, and a wrong line
    number sends the reader to the wrong row. When this returns False the
    caller omits line numbers rather than printing misleading ones.

    The comparison is exact: header + one line per row. Any newline inside a
    quoted field pushes the count past that and the mapping is refused.
    """
    try:
        return significant_line_count(path) == n_rows + 1
    except OSError:
        return False


def row_label(index: int, row: dict, with_line: bool) -> str:
    """Identify a row for a human who is about to open the CSV."""
    mid = row.get("measurement_id")
    paper = row.get("paper_id")
    try:
        mid = "" if pd.isna(mid) else str(mid)
    except (TypeError, ValueError):
        mid = str(mid)
    try:
        paper = "" if pd.isna(paper) else str(paper)
    except (TypeError, ValueError):
        paper = str(paper)
    ident = mid or "<no measurement_id>"
    where = f"df_index {index}"
    if with_line:
        where += f", csv line {index + 2}"
    suffix = f", paper {paper}" if paper else ""
    return f"{ident}  ({where}{suffix})"


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------

def _message_selected(message: str, categories: list[str], fields: list[str]) -> bool:
    if categories:
        low = category_of(message).lower()
        if not any(c.lower() in low for c in categories):
            return False
    if fields:
        msg_fields = {f.lower() for f in fields_for(message)}
        if not any(f.lower() in msg_fields for f in fields):
            return False
    return True


def collect(df: pd.DataFrame, results, args) -> list[dict]:
    """Build the per-row detail records the reporters consume."""
    rows = df.to_dict(orient="records")
    papers = [p.upper() for p in args.paper]
    records = []

    for index, (row, result) in enumerate(zip(rows, results)):
        if papers:
            paper = str(row.get("paper_id", "")).upper()
            if paper not in papers:
                continue

        errors = [
            m
            for m in result.errors
            if _message_selected(m, args.category, args.field)
        ]
        warnings = [
            m
            for m in result.warnings
            if _message_selected(m, args.category, args.field)
        ]

        if args.errors_only:
            warnings = []
        if args.warnings_only:
            errors = []
        if not errors and not warnings:
            continue

        records.append(
            {"index": index, "row": row, "errors": errors, "warnings": warnings}
        )

    return records


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_detail(records: list[dict], with_line: bool, limit: int) -> None:
    if not records:
        print("No rows matched.")
        return

    shown = records if limit <= 0 else records[:limit]
    for record in shown:
        print(row_label(record["index"], record["row"], with_line))
        for message in record["errors"]:
            print(f"  ERROR    {describe(message, record['row'])}")
        for message in record["warnings"]:
            print(f"  WARNING  {describe(message, record['row'])}")
        print()

    if limit > 0 and len(records) > limit:
        print(f"... {len(records) - limit} more rows suppressed by --limit {limit}")


def print_summary(records: list[dict], max_ids: int = 12) -> None:
    buckets: dict[tuple[str, str], list[str]] = {}
    for record in records:
        mid = record["row"].get("measurement_id")
        try:
            blank = pd.isna(mid)
        except (TypeError, ValueError):
            blank = False
        # An empty cell renders as the literal "nan" via str(), which reads as
        # a real id in the affected-ids list. Use the same placeholder row_label
        # uses so the two views agree.
        mid = "<no measurement_id>" if blank or not str(mid).strip() else str(mid)
        for severity, messages in (
            ("ERROR", record["errors"]),
            ("WARNING", record["warnings"]),
        ):
            for message in messages:
                buckets.setdefault((severity, category_of(message)), []).append(mid)

    if not buckets:
        print("No rows matched.")
        return

    for severity in ("ERROR", "WARNING"):
        keys = sorted(k for k in buckets if k[0] == severity)
        if not keys:
            continue
        print(f"{severity}S")
        for key in keys:
            ids = buckets[key]
            fields = ", ".join(fields_for(key[1]))
            head = ", ".join(ids[:max_ids])
            more = f", +{len(ids) - max_ids} more" if len(ids) > max_ids else ""
            print(f"- {key[1]} ({fields}): {len(ids)}")
            print(f"    {head}{more}")
        print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Per-row validation detail: which field failed on which row."
    )
    parser.add_argument("csv", nargs="?", default=DEFAULT_CSV)
    parser.add_argument("--errors-only", action="store_true")
    parser.add_argument("--warnings-only", action="store_true")
    parser.add_argument("--paper", action="append", default=[])
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--field", action="append", default=[])
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--no-dataset-checks", action="store_true")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])

    if args.errors_only and args.warnings_only:
        print("Error: --errors-only and --warnings-only are mutually exclusive.")
        return 2

    if not os.path.exists(args.csv):
        print(f"Error: CSV file not found: {args.csv}")
        return 2

    # Loaded exactly as validate_data.py loads it: no keep_default_na=False,
    # which would make every empty optional cell look like a populated string
    # (manual §6.7).
    try:
        df = pd.read_csv(args.csv)
    except pd.errors.EmptyDataError:
        print(f"Error: {args.csv} is empty or has no header row.")
        return 2
    except pd.errors.ParserError as exc:
        print(f"Error: {args.csv} is not well-formed CSV: {exc}")
        return 2
    except UnicodeDecodeError as exc:
        print(f"Error: {args.csv} is not valid UTF-8: {exc}")
        return 2
    except OSError as exc:
        print(f"Error: cannot read {args.csv}: {exc}")
        return 2

    if args.no_dataset_checks:
        results = [validate_row(r) for r in df.to_dict(orient="records")]
    else:
        results = validate_dataset(df).results

    records = collect(df, results, args)

    print(f"HyCAN-DB Per-Row Validation Detail — {args.csv}")
    print(f"Rows read: {len(df)}   Rows reported: {len(records)}")
    if args.no_dataset_checks:
        print("Dataset-level checks skipped (--no-dataset-checks).")
    print()

    if args.summary:
        print_summary(records)
    else:
        with_line = line_numbers_are_reliable(args.csv, len(df))
        if not with_line:
            print("(csv line numbers omitted: physical lines do not map 1:1 to rows)\n")
        print_detail(records, with_line, args.limit)

    # The exit code describes the SELECTED rows, which is what the flags asked
    # about. Deriving it from the unfiltered results instead would make every
    # filtered invocation a false failure: `--paper HYC-0002` would print "No
    # rows matched." and then exit 1 because some other paper has an error.
    has_errors = any(record["errors"] for record in records)
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
