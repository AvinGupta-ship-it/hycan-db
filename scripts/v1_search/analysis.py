"""The §11 analyses of the v1.0 protocol, from the assembled dataset.

`rq1` builds the RQ1 primary set (hycan.v1_sets), fits the primary and
secondary models (hycan.v1_rq1) and writes, under references/v1_analysis/:

  - ``rq1_samples.csv`` — the analysis units (one n_ex,max per sample);
  - ``rq1.json`` — the primary ratio with both 95% intervals and the §11
    decision, the secondary slope, the exclusion ladder from all coded 77 K
    excess isotherms down to the primary set, and the distribution of
    ``p_at_nmax_bar`` with every value outside 10–60 bar listed.

    python3 scripts/v1_search/analysis.py rq1 [--processed ...] [--tree ...]
        [--out references/v1_analysis] [--boot 2000]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hycan import v1, v1_rq1, v1_sets  # noqa: E402


def dual_papers(tree: Path) -> set[str]:
    with (tree / "papers.csv").open(newline="", encoding="utf-8") as fh:
        return {r["paper_id"] for r in csv.DictReader(fh) if r["mode"] == "dual"}


def ladder(df: pd.DataFrame, dual: set[str]) -> dict:
    """Isotherms and papers lost at each §11/RQ1 step (the §11.0
    missing-data report for the primary set)."""
    iso = v1.isotherm_table(df)
    iso = iso[iso["paper_id"].isin(sorted(dual))]
    steps = {"coded_77k_excess_isotherms": iso}
    steps["nmax_observed_or_plateau"] = iso[
        iso["nmax_status"].isin(v1_sets.PRIMARY_STATUSES)
        & ~iso["basis_shape_conflict"].astype(bool)
    ]
    measured = v1_sets.eligible_isotherms(df, dual, area_min=None)
    steps["every_point_measured"] = measured
    steps["eligible_area_300"] = v1_sets.eligible_isotherms(df, dual)
    return {
        name: {"isotherms": int(len(t)), "papers": int(t["paper_id"].nunique()) if len(t) else 0}
        for name, t in steps.items()
    }


def cmd_rq1(args) -> int:
    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    dual = dual_papers(tree)
    samples = v1_sets.rq1_samples(df, dual)
    out.mkdir(parents=True, exist_ok=True)
    samples.to_csv(out / "rq1_samples.csv", index=False, lineterminator="\n")

    primary = v1_rq1.fit_primary(samples, n_boot=args.boot)
    secondary = v1_rq1.fit_secondary(samples)
    iso = v1_sets.eligible_isotherms(df, dual)
    p = iso["p_at_nmax_bar"].astype(float)
    outside = iso[(p < 10) | (p > 60)]
    report = {
        "primary": primary,
        "secondary": secondary,
        "exclusion_ladder": ladder(df, dual),
        "p_at_nmax_bar": {
            "n": int(len(p)),
            "quartiles": [float(x) for x in np.percentile(p, [25, 50, 75])],
            "min": float(p.min()), "max": float(p.max()),
            "outside_10_60_bar": [
                {"isotherm_key": r["isotherm_key"],
                 "p_at_nmax_bar": float(r["p_at_nmax_bar"])}
                for _, r in outside.iterrows()
            ],
        },
    }
    (out / "rq1.json").write_text(json.dumps(report, indent=2) + "\n",
                                  encoding="utf-8")
    print(f"samples {primary['n_samples']}, papers {primary['n_papers']}, "
          f"labs {primary['n_labs']}")
    print(f"ratio {primary['ratio']:.4f}, t CI {primary['ci95_t']}, "
          f"bootstrap CI {primary['ci95_bootstrap']}")
    print(f"decision: {primary['decision']} "
          f"(CI {primary['ci95_decision']}, margin {v1_rq1.MARGIN})")
    print(f"prediction interval: {primary['prediction_interval_95']}")
    print(f"secondary b = {secondary['b']:.4f} CI {secondary['ci95']}, "
          f"corrected {secondary['b_corrected_10pct']:.4f} / "
          f"{secondary['b_corrected_20pct']:.4f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rq1")
    r.add_argument("--processed",
                   default=str(ROOT / "data" / "processed" / "measurements_v1.0_computed.csv"))
    r.add_argument("--tree", default=str(ROOT / "references" / "v1_extraction"))
    r.add_argument("--out", default=str(ROOT / "references" / "v1_analysis"))
    r.add_argument("--boot", type=int, default=v1_rq1.BOOT_N)
    args = ap.parse_args(argv)
    return {"rq1": cmd_rq1}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
