"""The §12 human-audit sample of the v1.0 extraction (docs/v1_protocol.md §12).

`draw` draws the 60 audit rows with ``numpy.random.default_rng(20261029)`` and
writes, under references/v1_audit/:

  - ``draw.csv`` — the drawn rows: audit stratum, cell, draw order, paper and
    measurement_id;
  - ``cells.json`` — every cell's pool size and quota (the §12 reporting
    weights);
  - ``sheet.csv`` — the audit sheet: the paper, sample label, source location
    and identification aids, and one empty column per audited field. No
    extracted value of an audited field appears on the sheet.

Audit strata and cells, drawn cell by cell in this order, each cell sorted by
measurement_id (lexicographic), without replacement with the generator's
``choice`` on the sorted ids:

  (a) 30 rows from the RQ1 primary set, each the row at ``p_at_nmax_bar`` of a
      contributing isotherm: 15 from rows A and B agreed on every compared
      field before reconciliation, 15 from rows C resolved;
  (b) 15 other rows from the dual papers: 8 agreed, 7 resolved;
  (c) 15 rows from the legacy (B-only) papers.

A cell with fewer rows than its quota contributes them all (no generator
call), and the shortfall moves to the other cell of the same audit stratum;
both quotas are settled from the pool sizes before either cell is drawn.

A row is *agreed* when its §9 match line has status ``agree`` and no
resolution of C's names that line or the row's measurement_id; every other
row (a differing or unmatched line, a row C corrected or added) is
*resolved*. A reconciled row's match line comes from the §9 identity rules:
a matched pair and a kept only-first row keep the first row set's
measurement_id, and every other reconciled row is named by ``final_value``
in a resolution.

An isotherm contributes to the RQ1 primary set (§11) when it is a coded 77 K
``basis_inferred = excess`` isotherm of a probability-sample (dual) paper
with ``nmax_status`` in {observed_max, plateau}, ``basis_shape_conflict``
false, every usable point ``value_kind = measured``, and the §11.0-eligible
BET area of its maximum-point row at least 300 m² g⁻¹. (No row of the v1.0
dataset has ``duplicate_of`` set, so the §11.0 duplicate rule removes
nothing.)

    python3 scripts/v1_search/audit.py draw [--processed ...] [--tree ...]
        [--out references/v1_audit]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hycan import v1  # noqa: E402

SEED = 20261029
QUOTAS = (("a", "agreed", 15), ("a", "resolved", 15),
          ("b", "agreed", 8), ("b", "resolved", 7), ("c", "all", 15))
AUDIT_FIELDS = (
    "uptake_value", "uptake_unit", "temperature_k", "pressure_bar",
    "a_bet_m2_g", "a_bet_method", "a_bet_probe_gas", "basis_stated",
    "basis_inferred", "wt_pct_convention", "value_kind", "sample_identity",
    "digitized_point",
)


def contributing_audit_rows(df: pd.DataFrame, dual: set[str]) -> dict[str, str]:
    """{measurement_id: isotherm_key} of the row at p_at_nmax_bar of every
    isotherm contributing to the RQ1 primary set."""
    iso = v1.isotherm_table(df)
    eligible = iso[
        iso["nmax_status"].isin(["observed_max", "plateau"])
        & ~iso["basis_shape_conflict"].astype(bool)
        & (iso["value_kinds"] == "measured")
        & iso["paper_id"].isin(sorted(dual))
    ]
    keys = df.apply(v1.isotherm_key, axis=1)
    out: dict[str, str] = {}
    for _, e in eligible.iterrows():
        g = df[keys == e["isotherm_key"]]
        use = g[g.apply(v1._usable_point_row, axis=1)]
        cands = []
        for _, r in use.iterrows():
            w = v1.w1_wt_pct(r)
            if (
                w is not None
                and math.isclose(float(r["pressure_bar"]), e["p_at_nmax_bar"],
                                 rel_tol=0.0, abs_tol=1e-12)
                and math.isclose(w, e["n_ex_max_wt_pct"], rel_tol=1e-12)
            ):
                cands.append(r)
        if not cands:
            raise SystemExit(f"REFUSED: no row at p_at_nmax for {e['isotherm_key']}")
        row = max(cands, key=lambda r: r["measurement_id"])
        area = v1.eligible_bet_area(row)
        if area is not None and area >= 300:
            out[row["measurement_id"]] = e["isotherm_key"]
    return out


def agreed_classifier(tree: Path, pid: str):
    """is_agreed(measurement_id) for one dual paper, from its §9 match lines
    and C's resolutions (module docstring)."""
    with (tree / pid / "C_input" / "match.csv").open(newline="", encoding="utf-8") as fh:
        match = list(csv.DictReader(fh))
    with (tree / pid / "C" / "resolutions.csv").open(newline="", encoding="utf-8") as fh:
        res = list(csv.DictReader(fh))
    line_status: dict[str, set] = {}
    mid2line: dict[str, str] = {}
    for x in match:
        line_status.setdefault(x["match_line"], set()).add(x["status"])
        if x["first_measurement_id"]:
            mid2line.setdefault(x["first_measurement_id"], x["match_line"])
    resolved_lines = {x["match_line"] for x in res if x["match_line"]}
    resolved_mids = {x["final_value"] for x in res if x["final_value"]}

    def is_agreed(mid: str) -> bool:
        line = mid2line.get(mid)
        return (
            line is not None
            and line_status.get(line) == {"agree"}
            and line not in resolved_lines
            and mid not in resolved_mids
        )

    return is_agreed


def settle_quotas(cells: dict[tuple[str, str], list[str]]) -> dict[tuple[str, str], int]:
    """The §12 quotas, with each audit stratum's shortfall moved to its other
    cell before any draw."""
    quotas = {(s, c): q for s, c, q in QUOTAS}
    for stratum, pair in (("a", ("agreed", "resolved")), ("b", ("agreed", "resolved"))):
        for short, other in (pair, pair[::-1]):
            lack = quotas[(stratum, short)] - len(cells[(stratum, short)])
            if lack > 0:
                quotas[(stratum, short)] -= lack
                quotas[(stratum, other)] = min(
                    quotas[(stratum, other)] + lack, len(cells[(stratum, other)])
                )
    quotas[("c", "all")] = min(quotas[("c", "all")], len(cells[("c", "all")]))
    return quotas


def isotherm_point(df: pd.DataFrame, keys: pd.Series, row: pd.Series) -> str:
    """'k of n, by increasing pressure' among the row's isotherm's
    figure-digitized rows — identification only, no extracted value."""
    if v1.as_str(row.get("extraction_method")) != "figure_digitized":
        return ""
    g = df[(keys == v1.isotherm_key(row))
           & (df["extraction_method"] == "figure_digitized")].copy()
    g = g.sort_values(["pressure_bar", "measurement_id"], kind="mergesort")
    mids = list(g["measurement_id"])
    return f"{mids.index(row['measurement_id']) + 1} of {len(mids)}, by increasing pressure"


def cmd_draw(args) -> int:
    tree = Path(args.tree)
    out = Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    with (tree / "papers.csv").open(newline="", encoding="utf-8") as fh:
        papers = list(csv.DictReader(fh))
    dual = {p["paper_id"] for p in papers if p["mode"] == "dual"}
    legacy = {p["paper_id"] for p in papers if p["mode"] == "legacy"}

    a_rows = contributing_audit_rows(df, dual)
    classifiers = {pid: agreed_classifier(tree, pid) for pid in sorted(dual)}
    cells: dict[tuple[str, str], list[str]] = {("a", "agreed"): [], ("a", "resolved"): [],
             ("b", "agreed"): [], ("b", "resolved"): [], ("c", "all"): []}
    pid_of: dict[str, str] = {}
    for _, r in df.iterrows():
        mid, pid = r["measurement_id"], r["paper_id"]
        pid_of[mid] = pid
        if pid in dual:
            stratum = "a" if mid in a_rows else "b"
            cell = "agreed" if classifiers[pid](mid) else "resolved"
            cells[(stratum, cell)].append(mid)
        elif pid in legacy:
            cells[("c", "all")].append(mid)

    cells = {k: sorted(v) for k, v in cells.items()}
    quotas = settle_quotas(cells)
    rng = np.random.default_rng(SEED)
    drawn: list[dict] = []
    for stratum, cell, _ in QUOTAS:
        pool, k = cells[(stratum, cell)], quotas[(stratum, cell)]
        picked = (list(pool) if len(pool) <= k
                  else list(rng.choice(np.array(pool, dtype=object), size=k,
                                       replace=False)))
        for n, mid in enumerate(picked, 1):
            drawn.append({"audit_stratum": stratum, "cell": cell, "order": n,
                          "paper_id": pid_of[mid], "measurement_id": mid})

    out.mkdir(parents=True, exist_ok=True)
    with (out / "draw.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["audit_stratum", "cell", "order",
                                           "paper_id", "measurement_id"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(drawn)
    (out / "cells.json").write_text(json.dumps({
        "seed": SEED,
        "cells": {f"{s}/{c}": {"pool": len(cells[(s, c)]), "quota": quotas[(s, c)]}
                  for s, c, _ in QUOTAS},
        "rq1_primary": {"isotherms": len(a_rows),
                        "papers": len({pid_of[m] for m in a_rows})},
    }, indent=2) + "\n", encoding="utf-8")

    keys = df.apply(v1.isotherm_key, axis=1)
    by_mid = df.set_index("measurement_id", drop=False)
    with (out / "sheet.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["paper_id", "measurement_id",
                                           "sample_label", "source_location",
                                           "isotherm_point", *AUDIT_FIELDS],
                           lineterminator="\n")
        w.writeheader()
        for d in drawn:
            r = by_mid.loc[d["measurement_id"]]
            w.writerow({
                "paper_id": d["paper_id"],
                "measurement_id": d["measurement_id"],
                "sample_label": v1.as_str(r["material_description"]) and
                                str(r["material_description"]).split(" | ", 1)[0],
                "source_location": v1.as_str(r["source_location"]) or "",
                "isotherm_point": isotherm_point(df, keys, r),
                **{f: "" for f in AUDIT_FIELDS},
            })
    for s, c, _ in QUOTAS:
        print(f"{s}/{c}: pool {len(cells[(s, c)])}, drawn {quotas[(s, c)]}")
    print(f"drawn {len(drawn)} rows -> {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    d.add_argument("--processed",
                   default=str(ROOT / "data" / "processed" / "measurements_v1.0_computed.csv"))
    d.add_argument("--tree", default=str(ROOT / "references" / "v1_extraction"))
    d.add_argument("--out", default=str(ROOT / "references" / "v1_audit"))
    args = ap.parse_args(argv)
    return {"draw": cmd_draw}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
