#!/usr/bin/env python3
"""
Command-line entry point for the HyCAN-DB data-validation pipeline.

Usage
-----
    python3 scripts/validate_data.py [CSV_PATH]

If no path is given it defaults to ``data/raw/measurements_v0.1.csv``. The data
is validated *exactly as loaded* — it is never cleaned first. Exit codes:

    0  no errors across all rows and dataset checks
    1  one or more errors
    2  the CSV path does not exist
"""

from __future__ import annotations

import os
import sys

import pandas as pd

from hycan.validate import print_report, validate_dataset

DEFAULT_CSV = "data/raw/measurements_v0.1.csv"


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else DEFAULT_CSV

    if not os.path.exists(path):
        print(f"Error: CSV file not found: {path}")
        return 2

    # Load raw; pandas infers numeric columns. Per-value coercion in the
    # validator handles anything that stays as text.
    df = pd.read_csv(path)

    report = validate_dataset(df)
    print_report(report)

    total_errors = sum(report.error_counts.values())
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
