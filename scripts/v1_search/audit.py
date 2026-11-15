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

`score` compares the author's filled sheet with the dataset and writes
``score.json``: errors per field and per audit stratum with exact
(Clopper–Pearson) 95% CIs, each audit stratum's row-level error rate, and the
overall row-level rate weighted by the rows each cell represents (§12). An
error is a numeric difference larger than the printed rounding — half the
last printed digit of either entry — or 3% relative for a figure-digitized
value, or any categorical difference. The author's uptake is compared in the
unit he records (`wt%`, `mmol/g` or `mL(STP)/g`); naming a unit whose column
the row does not fill is a unit error. ``sample_identity`` is compared as a
printed label (letters and digits, ignoring case). An empty cell against an
empty field is agreement; empty against filled, either way, is an error.

    python3 scripts/v1_search/audit.py draw [--processed ...] [--tree ...]
        [--out references/v1_audit]
    python3 scripts/v1_search/audit.py score [--sheet ...] [--processed ...]
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

from hycan import v1

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


# ---------------------------------------------------------------------------
# score
# ---------------------------------------------------------------------------

UNIT_COLUMN = {
    "wt%": "uptake_wt_pct", "wt_pct": "uptake_wt_pct", "wt %": "uptake_wt_pct",
    "mmol/g": "uptake_mmol_g", "mmol g-1": "uptake_mmol_g",
    "ml(stp)/g": "uptake_ml_stp_g", "cm3(stp)/g": "uptake_ml_stp_g",
    "cm3/g": "uptake_ml_stp_g", "ml/g": "uptake_ml_stp_g",
}


def half_unit(printed: str) -> float:
    s = str(printed).strip()
    return 0.5 * 10.0 ** (-(len(s.split(".", 1)[1]) if "." in s else 0))


def numeric_error(author: str, stored: str, digitized: bool) -> bool | None:
    """None: both empty (not compared). True: an error under the §12 rule."""
    a, b = str(author or "").strip(), str(stored or "").strip()
    fa, fb = v1.as_float(a), v1.as_float(b)
    if fa is None and fb is None:
        return None
    if fa is None or fb is None:
        return True
    if digitized:
        return abs(fa - fb) > 0.03 * max(abs(fa), abs(fb))
    return abs(fa - fb) > max(half_unit(a), half_unit(b)) + 1e-12


def categorical_error(author: str, stored: str) -> bool | None:
    a = str(author or "").strip().casefold()
    b = str(stored or "").strip().casefold()
    if not a and not b:
        return None
    return a != b


def norm_label(label: str) -> str:
    import re
    import unicodedata
    return re.sub(r"[\W_]+", "", unicodedata.normalize("NFKC", str(label or "")).casefold())


def row_errors(sheet: dict, row: pd.Series) -> dict[str, bool]:
    """{audited field: is_error} for one audited row; fields where both sides
    are empty are left out."""
    figure = v1.as_str(row.get("extraction_method")) == "figure_digitized"

    def stored(field):
        val = row.get(field)
        return "" if pd.isna(val) else str(val)

    out: dict[str, bool | None] = {}
    unit = str(sheet.get("uptake_unit") or "").strip().casefold()
    col = UNIT_COLUMN.get(unit)
    any_uptake = any(stored(c) for c in
                     ("uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"))
    author_val = str(sheet.get("uptake_value") or "").strip()
    if not unit and not author_val and not any_uptake:
        out["uptake_unit"] = out["uptake_value"] = None
    elif col and stored(col):
        out["uptake_unit"] = False
        out["uptake_value"] = numeric_error(author_val, stored(col), figure)
    else:
        # The author's unit names no column the row fills (or is missing or
        # unrecognized while the row holds an uptake): a unit error, and the
        # value cannot be compared.
        out["uptake_unit"] = True
        out["uptake_value"] = True
    out["temperature_k"] = numeric_error(sheet.get("temperature_k"),
                                         stored("temperature_k"), False)
    p_digitized = figure or "pressure digitized" in (stored("notes") or "")
    out["pressure_bar"] = numeric_error(sheet.get("pressure_bar"),
                                        stored("pressure_bar"), p_digitized)
    out["a_bet_m2_g"] = numeric_error(sheet.get("a_bet_m2_g"),
                                      stored("bet_surface_area_m2_g"), False)
    out["a_bet_method"] = categorical_error(sheet.get("a_bet_method"),
                                            stored("surface_area_method"))
    out["a_bet_probe_gas"] = categorical_error(
        sheet.get("a_bet_probe_gas"),
        stored("surface_area_probe_gas") or ("unspecified" if stored("bet_surface_area_m2_g") else ""),
    )
    for field in ("basis_stated", "basis_inferred", "wt_pct_convention", "value_kind"):
        out[field] = categorical_error(sheet.get(field), stored(field))
    label = str(row.get("material_description") or "").split(" | ", 1)[0]
    out["sample_identity"] = (
        norm_label(sheet.get("sample_identity")) != norm_label(label)
        if str(sheet.get("sample_identity") or "").strip() or label else None
    )
    if figure:
        dp = str(sheet.get("digitized_point") or "")
        parts = [x.strip() for x in dp.split(";")]
        p_author = parts[0] if parts else ""
        v_author = parts[1] if len(parts) > 1 else ""
        err_p = numeric_error(p_author, stored("pressure_bar"), True)
        err_v = numeric_error(v_author, stored(col) if col else stored("uptake_wt_pct"), True)
        out["digitized_point"] = (err_p or err_v) if (err_p is not None or err_v is not None) else True
    return {k: bool(v) for k, v in out.items() if v is not None}


def clopper_pearson(k: int, n: int) -> tuple[float, float]:
    from scipy.stats import beta
    if n == 0:
        return (0.0, 1.0)
    lo = 0.0 if k == 0 else float(beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(0.975, k + 1, n - k))
    return (lo, hi)


def cmd_score(args) -> int:
    out = Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    by_mid = df.set_index("measurement_id", drop=False)
    with Path(args.sheet).open(newline="", encoding="utf-8") as fh:
        sheet = {r["measurement_id"]: r for r in csv.DictReader(fh)}
    with (out / "draw.csv").open(newline="", encoding="utf-8") as fh:
        draw = list(csv.DictReader(fh))
    cells = json.loads((out / "cells.json").read_text(encoding="utf-8"))["cells"]

    unfilled = [d["measurement_id"] for d in draw
                if not any(str(sheet.get(d["measurement_id"], {}).get(f) or "").strip()
                           for f in AUDIT_FIELDS)]
    if unfilled:
        print(f"REFUSED: {len(unfilled)} drawn rows have no audited entry "
              f"(first: {unfilled[0]})", file=sys.stderr)
        return 1

    per_field: dict[tuple[str, str], list[int]] = {}
    per_row: dict[str, list[int]] = {}
    for d in draw:
        errs = row_errors(sheet[d["measurement_id"]], by_mid.loc[d["measurement_id"]])
        s = d["audit_stratum"]
        per_row.setdefault(s, []).append(int(any(errs.values())))
        for f, e in errs.items():
            per_field.setdefault((s, f), []).append(int(e))

    report = {"fields": {}, "strata": {}, "overall": {}}
    for (s, f), v in sorted(per_field.items()):
        k, n = sum(v), len(v)
        report["fields"][f"{s}/{f}"] = {"errors": k, "n": n,
                                        "ci95": clopper_pearson(k, n)}
    weighted_num = weighted_den = 0.0
    for s, v in sorted(per_row.items()):
        k, n = sum(v), len(v)
        report["strata"][s] = {"row_errors": k, "n": n, "rate": k / n,
                               "ci95": clopper_pearson(k, n)}
    for d in draw:
        c = cells[f"{d['audit_stratum']}/{d['cell']}"]
        w = c["pool"] / c["quota"]
        errs = row_errors(sheet[d["measurement_id"]], by_mid.loc[d["measurement_id"]])
        weighted_num += w * int(any(errs.values()))
        weighted_den += w
    report["overall"] = {"weighted_row_error_rate": weighted_num / weighted_den}
    (out / "score.json").write_text(json.dumps(report, indent=2) + "\n",
                                    encoding="utf-8")
    for s, v in report["strata"].items():
        print(f"stratum {s}: {v['row_errors']}/{v['n']} rows with an error, "
              f"CI95 [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}]")
    print(f"overall weighted row-error rate: "
          f"{report['overall']['weighted_row_error_rate']:.4f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    d.add_argument("--processed",
                   default=str(ROOT / "data" / "processed" / "measurements_v1.0_computed.csv"))
    d.add_argument("--tree", default=str(ROOT / "references" / "v1_extraction"))
    d.add_argument("--out", default=str(ROOT / "references" / "v1_audit"))
    s = sub.add_parser("score")
    s.add_argument("--sheet", default=str(ROOT / "references" / "v1_audit" / "sheet.csv"))
    s.add_argument("--processed",
                   default=str(ROOT / "data" / "processed" / "measurements_v1.0_computed.csv"))
    s.add_argument("--out", default=str(ROOT / "references" / "v1_audit"))
    args = ap.parse_args(argv)
    return {"draw": cmd_draw, "score": cmd_score}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
