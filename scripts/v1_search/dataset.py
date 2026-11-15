"""Assemble the v1.0 dataset from the reconciled extraction outputs
(docs/v1_protocol.md §9, §14; §15 Amendment 2).

For every extracted paper in references/v1_extraction/papers.csv (file order,
the committed sampling order), the paper's rows are reconciler C's rows.csv,
unchanged except that `selection_route` and `frame_id` — §7 sampling
provenance, which no extractor sees — are filled from papers.csv. For
HYC-0041 (mode `none`, Amendment 2) the v0.1 rows are carried over unchanged
from data/raw/measurements_v0.1.csv, with the same two provenance fields
filled; their schema v2 coding stays empty, so every computed field of theirs
is null.

The assembled rows are validated against schema v2 (`hycan.validate`) before
anything is written. Two files are produced:

  - data/raw/measurements_v1.0.csv — the extracted rows (97 columns, LF);
  - data/processed/measurements_v1.0_computed.csv — the same rows with the
    computed fields of protocol §3, §10.1 and §10.2 appended
    (`hycan.v1.add_computed_fields`).

    python3 scripts/v1_search/dataset.py [--tree references/v1_extraction]
        [--v01 data/raw/measurements_v0.1.csv]
        [--out data/raw/measurements_v1.0.csv]
        [--processed data/processed/measurements_v1.0_computed.csv]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

PROVENANCE = ("selection_route", "frame_id")


def paper_rows(p: dict, tree: Path, v01_cols: list[str], v01_rows: list[dict],
               columns: list[str]) -> list[dict]:
    """One paper's dataset rows, provenance filled from its papers.csv record."""
    if p["mode"] == "none":
        rows = [dict(r) for r in v01_rows if r.get("paper_id") == p["paper_id"]]
        if v01_cols != columns:
            raise SystemExit("REFUSED: v0.1 columns differ from C columns")
    else:
        path = tree / p["paper_id"] / "C" / "rows.csv"
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if list(reader.fieldnames or []) != columns:
                raise SystemExit(f"REFUSED: {path} columns differ")
            rows = [dict(r) for r in reader]
    if not rows:
        raise SystemExit(f"REFUSED: no rows for {p['paper_id']}")
    for r in rows:
        for field in PROVENANCE:
            r[field] = p[field]
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", default=str(ROOT / "references" / "v1_extraction"))
    ap.add_argument("--v01", default=str(ROOT / "data" / "raw" / "measurements_v0.1.csv"))
    ap.add_argument("--out", default=str(ROOT / "data" / "raw" / "measurements_v1.0.csv"))
    ap.add_argument("--processed",
                    default=str(ROOT / "data" / "processed" / "measurements_v1.0_computed.csv"))
    args = ap.parse_args(argv)
    tree = Path(args.tree)

    with tree.joinpath("papers.csv").open(newline="", encoding="utf-8") as fh:
        papers = list(csv.DictReader(fh))
    with Path(args.v01).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        v01_cols, v01_rows = list(reader.fieldnames or []), list(reader)

    first = papers[0]
    with (tree / first["paper_id"] / "C" / "rows.csv").open(newline="", encoding="utf-8") as fh:
        columns = list(csv.DictReader(fh).fieldnames or [])

    rows: list[dict] = []
    for p in papers:
        rows.extend(paper_rows(p, tree, v01_cols, v01_rows, columns))

    import pandas as pd

    from hycan.v1 import add_computed_fields
    from hycan.validate import print_report, validate_dataset

    # Validate the frame as the pipeline loads it: an empty cell is missing,
    # as it is after pd.read_csv (hycan.load.load_dataset).
    df = pd.DataFrame(rows, columns=columns).replace("", pd.NA)
    report = validate_dataset(df)
    errors = sum(1 for r in report.results if r.errors)
    warnings = sum(1 for r in report.results if r.warnings)
    if errors:
        print_report(report)
        print(f"REFUSED: {errors} rows with schema errors; nothing written",
              file=sys.stderr)
        return 1
    print(f"validated: {len(rows)} rows, 0 errors, {warnings} rows with warnings")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in columns} for r in rows)

    computed = add_computed_fields(pd.read_csv(out, low_memory=False))
    processed = Path(args.processed)
    processed.parent.mkdir(parents=True, exist_ok=True)
    computed.to_csv(processed, index=False, lineterminator="\n")

    papers_n = len({r['paper_id'] for r in rows})
    print(f"{out}: {len(rows)} rows, {papers_n} papers, {len(columns)} columns")
    print(f"{processed}: {len(computed.columns)} columns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
