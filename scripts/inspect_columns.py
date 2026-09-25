#!/usr/bin/env python3
"""
Column inspection CLI for HyCAN-DB (manual v2.0 §18 Phase A.2).

Replaces the ad-hoc ``python3 - <<'PYEOF' ... pandas ...`` heredocs used to
answer "what is in column N", "what values does this column take", "what is the
physical column order". Those heredocs are slow to write, easy to get wrong, and
tempt the shell alternative that is actually wrong: ``awk -F','`` splits on
commas inside quoted fields and silently shifts every later column (§6.7, §B.3).

This tool uses pandas for every read, so the quoted-comma problem cannot occur
by construction.

Usage
-----
    python3 scripts/inspect_columns.py [CSV_PATH] [options]

    (no options)            one line per column: position, dtype, non-null,
                            unique count, example value
    --order                 physical CSV order beside schema.py declaration
                            order, with the §6.7 offsets made explicit
    --col NAME              detail for one column (repeatable)
    --values NAME           value counts for one column (repeatable)
    --missing               columns with empty cells, most-empty first
    --head N / --tail N     show N rows
    --where COL=VALUE       filter rows (repeatable; string equality)
    --select COL            limit --head/--tail output to these columns
                            (repeatable)
    --top N                 how many values to list per column (default 15)

Exit codes
----------
    0  success
    2  the CSV path does not exist, or a named column is not in the file

This script reads the CSV and never writes to it.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

import pandas as pd

DEFAULT_CSV = "data/raw/measurements_v0.1.csv"


def _schema_order() -> tuple[list[str] | None, str | None]:
    """(field names in declaration order, reason they are unavailable).

    A missing package and a broken ``schema.py`` are different events and are
    reported differently. Column inspection of an arbitrary CSV should work
    without hycan installed, so ImportError degrades quietly. A schema.py that
    raises while importing is a defect, and swallowing it would silently turn
    --order — whose entire job is the §6.7 comparison — into a command that
    prints one list and exits 0 as though it had checked something.
    """
    try:
        from hycan.schema import MeasurementEntry
    except ImportError as exc:
        return None, f"hycan is not importable here ({exc})"
    except Exception as exc:  # noqa: BLE001 - reported, not swallowed
        return None, (f"schema.py raised while importing: "
                      f"{type(exc).__name__}: {exc}")
    return list(MeasurementEntry.model_fields), None


def field_counts(path: str) -> dict[int, list[int]]:
    """Distinct field counts across the file, mapped to the lines that have them.

    Uses a real CSV parser, so a comma inside a quoted field is not miscounted
    the way ``awk -F','`` would miscount it. A file whose rows are not all the
    same width is exactly the silent column shift this tool exists to catch, so
    it is reported rather than parsed over.
    """
    counts: dict[int, list[int]] = {}
    with open(path, "r", encoding="utf-8", newline="") as handle:
        for number, row in enumerate(csv.reader(handle), start=1):
            if not row or (len(row) == 1 and not row[0].strip()):
                continue
            counts.setdefault(len(row), []).append(number)
    return counts


def _example(series: pd.Series) -> str:
    """First non-empty value in *series*, truncated for display."""
    non_null = series.dropna()
    if len(non_null) == 0:
        return "<all empty>"
    text = str(non_null.iloc[0])
    return text[:47] + "..." if len(text) > 50 else text


def _require_columns(df: pd.DataFrame, names: list[str]) -> list[str]:
    """Return the names missing from *df* (empty list when all present)."""
    return [n for n in names if n not in df.columns]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def overview(df: pd.DataFrame) -> None:
    print(f"{len(df)} rows x {len(df.columns)} columns\n")
    width = max((len(c) for c in df.columns), default=10)
    print(f"{'#':>3}  {'column'.ljust(width)}  {'dtype':<10} {'non-null':>8} "
          f"{'empty':>6} {'unique':>7}  example")
    for position, column in enumerate(df.columns, start=1):
        series = df[column]
        non_null = int(series.notna().sum())
        empty = len(df) - non_null
        unique = int(series.nunique(dropna=True))
        print(f"{position:>3}  {column.ljust(width)}  {series.dtype!s:<10} "
              f"{non_null:>8} {empty:>6} {unique:>7}  {_example(series)}")


def order(df: pd.DataFrame) -> None:
    """Physical CSV order beside schema declaration order.

    §6.7: the CSV's physical order differs from schema.py's declaration order.
    That difference is expected and is why positional appends must follow the
    CSV. A difference in the column *sets*, by contrast, is a real defect.
    """
    physical = list(df.columns)
    declared, reason = _schema_order()

    print("Physical CSV column order (what a positional append must follow):")
    for position, column in enumerate(physical, start=1):
        print(f"  {position:>3}  {column}")

    if declared is None:
        print(f"\nDeclaration order NOT compared: {reason}")
        print("The §6.7 check you asked for did not run.")
        return

    print("\nschema.py declaration order:")
    for position, column in enumerate(declared, start=1):
        print(f"  {position:>3}  {column}")

    only_csv = [c for c in physical if c not in declared]
    only_schema = [c for c in declared if c not in physical]

    print()
    if only_csv or only_schema:
        print("MISMATCH — the column sets differ. This is a defect, "
              "not the §6.7 offset:")
        if only_csv:
            print(f"  in CSV only:      {', '.join(only_csv)}")
        if only_schema:
            print(f"  in schema.py only: {', '.join(only_schema)}")
        return

    moved = [
        (c, physical.index(c) + 1, declared.index(c) + 1)
        for c in physical
        if physical.index(c) != declared.index(c)
    ]
    if not moved:
        print("Physical order matches declaration order exactly.")
        return

    print("Same columns, different order — expected per §6.7. Positions that differ:")
    for column, csv_position, schema_position in moved:
        print(f"  {column}: CSV #{csv_position}, schema #{schema_position}")
    print("\nA positional append (tail -n +2 staging >> dataset) must "
          "use the CSV order.")


def column_detail(df: pd.DataFrame, name: str, top: int) -> None:
    series = df[name]
    non_null = series.dropna()
    print(f"--- {name} ---")
    print(f"physical position: {list(df.columns).index(name) + 1} of {len(df.columns)}")
    print(f"dtype: {series.dtype}   non-null: {len(non_null)}   "
          f"empty: {len(df) - len(non_null)}   unique: {series.nunique(dropna=True)}")

    numeric = pd.to_numeric(non_null, errors="coerce").dropna()
    if len(numeric) and len(numeric) == len(non_null):
        print(f"min: {numeric.min()}   max: {numeric.max()}   "
              f"mean: {numeric.mean():.6g}   median: {numeric.median():.6g}")

    if len(non_null):
        counts = non_null.value_counts()
        print(f"top {min(top, len(counts))} of {len(counts)} distinct values:")
        for value, count in counts.head(top).items():
            text = str(value)
            text = text[:67] + "..." if len(text) > 70 else text
            print(f"  {count:>5}  {text}")
    print()


def value_counts(df: pd.DataFrame, name: str, top: int) -> None:
    series = df[name]
    counts = series.value_counts(dropna=False)
    print(f"--- {name}: {len(counts)} distinct values (empty included) ---")
    for value, count in counts.head(top).items():
        text = "<empty>" if pd.isna(value) else str(value)
        text = text[:67] + "..." if len(text) > 70 else text
        print(f"  {count:>5}  {text}")
    if len(counts) > top:
        print(f"  ... {len(counts) - top} more (raise --top to see them)")
    print()


def missing(df: pd.DataFrame) -> None:
    empties = {c: int(df[c].isna().sum()) for c in df.columns}
    empties = {c: n for c, n in empties.items() if n}
    if not empties:
        print("No empty cells in any column.")
        return
    print(f"{len(empties)} of {len(df.columns)} columns have empty cells "
          f"(of {len(df)} rows):")
    for column, count in sorted(empties.items(), key=lambda kv: -kv[1]):
        print(f"  {count:>5}  ({100 * count / len(df):5.1f}%)  {column}")


def apply_where(df: pd.DataFrame, clauses: list[str]) -> pd.DataFrame:
    """Filter by ``COL=VALUE``, matching as text, as a number, or as empty.

    String equality alone is a trap on this dataset. temperature_k is float64,
    so ``astype(str)`` yields "77.0" and ``--where temperature_k=77`` matches
    nothing — reporting "0 of 119 rows" on the dataset's most-filtered column,
    exit 0, which reads as real absence of data rather than a coercion bug.
    A numeric comparison is therefore attempted alongside the text one, and an
    empty VALUE selects empty cells.
    """
    for clause in clauses:
        column, separator, value = clause.partition("=")
        if not separator:
            raise ValueError(f"--where needs COL=VALUE, got: {clause}")
        column = column.strip()
        value = value.strip()
        if column not in df.columns:
            raise ValueError(f"--where names a column not in the file: {column}")

        series = df[column]
        mask = series.astype(str).str.strip() == value

        if value:
            # Only the QUERY is coerced, never the column. Coercing the column
            # too would turn the query into a value comparison rather than a
            # literal one on text columns, so `--where code=1e2` would also
            # select a cell reading "100" and `--where code=0077` would select
            # "77.0" and " 77 ". Comparing the raw column to a number matches
            # numeric columns, which is the case this exists for, and matches
            # nothing on a string column, which is correct.
            wanted = pd.to_numeric(value, errors="coerce")
            if pd.notna(wanted):
                mask = mask | (series == wanted)
        else:
            mask = mask | series.isna()

        df = df[mask]
    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect CSV columns with pandas (never awk; see §6.7)."
    )
    parser.add_argument("csv", nargs="?", default=DEFAULT_CSV)
    parser.add_argument("--order", action="store_true")
    parser.add_argument("--col", action="append", default=[])
    parser.add_argument("--values", action="append", default=[])
    parser.add_argument("--missing", action="store_true")
    parser.add_argument("--head", type=int, default=0)
    parser.add_argument("--tail", type=int, default=0)
    parser.add_argument("--where", action="append", default=[])
    parser.add_argument("--select", action="append", default=[])
    parser.add_argument("--top", type=int, default=15)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])

    if not os.path.exists(args.csv):
        print(f"Error: CSV file not found: {args.csv}")
        return 2

    # Width is measured BEFORE pandas is asked to parse. A file whose rows are
    # not all the same width is the silent column shift this tool exists to
    # catch, and pandas raises on some of those files and silently pads others.
    # Either way the operator should see which lines are the wrong width.
    try:
        widths = field_counts(args.csv)
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        print(f"Error: cannot read {args.csv}: {exc}")
        return 2

    ragged = len(set(widths)) > 1
    if ragged:
        print(f"WARNING: {args.csv} has rows of differing width. Column "
              "positions are not reliable for the affected rows.")
        for width, lines in sorted(widths.items()):
            shown = lines[:5]
            more = f" and {len(lines) - 5} more" if len(lines) > 5 else ""
            print(f"  {width:>3} field(s) on line(s) {shown}{more}")
        print()

    try:
        df = pd.read_csv(args.csv)
    except pd.errors.EmptyDataError:
        print(f"Error: {args.csv} is empty or has no header row.")
        return 2
    except pd.errors.ParserError as exc:
        print(f"Error: {args.csv} is not well-formed CSV: {exc}")
        if ragged:
            print("The width table above says which lines are at fault.")
        return 2
    except UnicodeDecodeError as exc:
        print(f"Error: {args.csv} is not valid UTF-8: {exc}")
        return 2

    named = args.col + args.values + args.select
    unknown = _require_columns(df, named)
    if unknown:
        print(f"Error: column(s) not in {args.csv}: {', '.join(unknown)}")
        print(f"Available: {', '.join(df.columns)}")
        return 2

    try:
        filtered = apply_where(df, args.where)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    if args.where:
        print(f"Filter {args.where} -> {len(filtered)} of {len(df)} rows\n")

    did_something = False

    if args.order:
        order(filtered)
        did_something = True

    for name in args.col:
        column_detail(filtered, name, args.top)
        did_something = True

    for name in args.values:
        value_counts(filtered, name, args.top)
        did_something = True

    if args.missing:
        missing(filtered)
        did_something = True

    if args.head < 0 or args.tail < 0:
        print("Error: --head and --tail must be zero or positive.")
        return 2

    if args.head or args.tail:
        view = filtered[args.select] if args.select else filtered
        with pd.option_context("display.max_columns", None, "display.width", 200):
            if args.head:
                print(view.head(args.head).to_string())
            if args.tail:
                print(view.tail(args.tail).to_string())
        did_something = True

    if not did_something:
        overview(filtered)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
