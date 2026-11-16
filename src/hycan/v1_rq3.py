"""The RQ3 interlaboratory analysis of the v1.0 protocol (§11, RQ3).

Materials: rows sharing a ``material_identity`` (identical supplier, product
name and grade), measured by two or more laboratories. RQ3 runs on all
§4-eligible papers (§7). ``material_identity`` is free text spelled
differently across papers and extraction streams, so grouping goes through
the committed map ``references/v1_analysis/material_identity_map.csv``
(every distinct string -> a material key; strings merge only when their
printed product designations are identical modulo trivial formatting, or
one string merely adds supplier detail); :func:`rq3_values` refuses an
unmapped string.

Per material and laboratory, one value per quantity (the geometric mean of
the laboratory's values):

- ``a_bet``: the distinct §11.0-eligible BET areas of the laboratory's rows
  (no 300 m² g⁻¹ floor - the floor bounds the RQ1 domain, not the area).
  Within one paper, an identical area carried by two or more laboratories'
  rows is one reported measurement, not an interlaboratory replication (the
  HYC-0060 round robin stamps its one central 423 m² g⁻¹ on every
  participant), so it enters once, under the laboratory id
  ``<paper_id>-shared``;
- ``n_ex_max``: n_ex,max as in RQ1 (``basis_inferred = excess``,
  ``basis_shape_conflict = false``, ``nmax_status`` in {observed_max,
  plateau}, every usable point measured), without the area condition;
- ``n_1bar``: the RQ2-window uptake (:func:`hycan.v1_rq2.rq2_rows` with
  ``require_area=False``);
- ``ratio``: n_ex,max/(A_BET/500) per sample carrying both, under RQ1's area
  rule.

Per material and quantity (two or more laboratories): the between-laboratory
SD of ln(value), as CV ≈ 100·SD, with the χ²-based 95% CI on L − 1 degrees
of freedom. The pooled (headline) SD per quantity is the material
fixed-effects, laboratory-random model fitted as a one-way within-material
ANOVA - each laboratory appears once per material, so the pooled SD is
sqrt(Σ_m Σ_l (y_ml − ȳ_m)² / Σ_m (L_m − 1)), with the χ² CI on the summed
degrees of freedom.
"""

from __future__ import annotations

from statistics import geometric_mean

import numpy as np
import pandas as pd
from scipy import stats

from . import v1, v1_rq2, v1_sets

QUANTITIES = ("a_bet", "n_ex_max", "n_1bar", "ratio")


def sd_ci(sd: float, df: int) -> tuple[float, float]:
    """χ²-based 95% CI for an SD estimated on ``df`` degrees of freedom."""
    lo = sd * float(np.sqrt(df / stats.chi2.ppf(0.975, df)))
    hi = sd * float(np.sqrt(df / stats.chi2.ppf(0.025, df)))
    return lo, hi


def rq3_values(df: pd.DataFrame, papers: set[str],
               key_of: dict[str, str]) -> pd.DataFrame:
    """One row per material key, quantity and laboratory: the laboratory's
    geometric-mean value. ``key_of`` maps every ``material_identity`` string
    to its material key (the committed map)."""
    sub = df[df["paper_id"].isin(sorted(papers))]
    sub = sub[sub["material_identity"].map(lambda x: v1.as_str(x) is not None)]
    unmapped = sorted(
        {s for s in map(v1.as_str, sub["material_identity"])
         if s not in key_of}
    )
    if unmapped:
        raise ValueError(
            "material_identity strings missing from the map: "
            + "; ".join(s[:60] for s in unmapped))
    identity = {}
    for (pid, sid), g in sub.groupby(["paper_id", "sample_id"]):
        keys = {key_of[v1.as_str(x)] for x in g["material_identity"]}
        if len(keys) != 1:
            raise ValueError(f"{pid} {sid}: mixed material keys {sorted(keys)}")
        identity[(pid, sid)] = keys.pop()

    values: dict[tuple[str, str, str], list[float]] = {}

    def add(key: tuple[str, str] | None, quantity: str, lab, value):
        lab = v1.as_str(lab)
        if key is None or lab is None or value is None or value <= 0:
            return
        values.setdefault((identity[key], quantity, lab), []).append(
            float(value))

    # a_bet: the distinct eligible areas per sample and laboratory; within a
    # paper, an area identical across laboratories enters once (see above).
    for pid, by_paper in sub.groupby("paper_id"):
        holders: dict[tuple[str, float], set[str]] = {}
        for (sid, lab), g in by_paper.groupby(["sample_id", "measuring_lab_id"]):
            areas = {v1.eligible_bet_area(r) for _, r in g.iterrows()}
            for a in sorted(a for a in areas if a is not None):
                holders.setdefault((sid, a), set()).add(lab)
        for (sid, a), labs in sorted(holders.items()):
            if len(labs) > 1:
                add((pid, sid), "a_bet", f"{pid}-shared", a)
            else:
                add((pid, sid), "a_bet", labs.pop(), a)

    # n_ex_max and the ratio, from the RQ1 isotherm machinery (no area floor).
    iso = v1_sets.eligible_isotherms(df, papers, area_min=None)
    for _, e in iso.iterrows():
        key = (e["paper_id"], e["sample_id"])
        if key not in identity:
            continue
        add(key, "n_ex_max", e["measuring_lab_id"], e["n_ex_max_wt_pct"])
        if e["a_bet_m2_g"] is not None and not pd.isna(e["a_bet_m2_g"]):
            add(key, "ratio", e["measuring_lab_id"],
                e["n_ex_max_wt_pct"] / (e["a_bet_m2_g"] / 500.0))

    # n at 1 bar, from the RQ2 window without the area condition.
    win = v1_rq2.rq2_rows(df, papers, require_area=False)
    for _, r in win.iterrows():
        key = (r["paper_id"], r["sample_id"])
        if key in identity:
            add(key, "n_1bar", r["lab_id"], r["n_w1_wt_pct"])

    rows = [
        {"material_key": m, "quantity": q, "lab_id": lab,
         "n_values": len(vals), "value": geometric_mean(vals)}
        for (m, q, lab), vals in sorted(values.items())
    ]
    return pd.DataFrame(rows, columns=[
        "material_key", "quantity", "lab_id", "n_values", "value"])


def fit_rq3(values: pd.DataFrame) -> dict:
    """The per-material CVs and the pooled SD per quantity."""
    out: dict = {"materials": {}, "pooled": {}}
    pooled: dict[str, tuple[float, int]] = {}
    for (m, q), g in values.groupby(["material_key", "quantity"]):
        if len(g) < 2:
            continue
        y = np.log(g["value"].to_numpy(float))
        df_ = len(y) - 1
        sd = float(np.std(y, ddof=1))
        lo, hi = sd_ci(sd, df_)
        out["materials"].setdefault(m, {})[q] = {
            "n_labs": len(y), "cv_pct": 100 * sd,
            "cv_ci95_pct": [100 * lo, 100 * hi],
        }
        ss, df0 = pooled.get(q, (0.0, 0))
        pooled[q] = (ss + float(np.sum((y - y.mean()) ** 2)), df0 + df_)
    for q in QUANTITIES:
        if q not in pooled or pooled[q][1] < 1:
            out["pooled"][q] = {"skipped": "fewer than two laboratories"}
            continue
        ss, df_ = pooled[q]
        sd = float(np.sqrt(ss / df_))
        lo, hi = sd_ci(sd, df_)
        n_mat = sum(1 for k in out["materials"].values() if q in k)
        out["pooled"][q] = {
            "n_materials": n_mat, "df": df_, "cv_pct": 100 * sd,
            "cv_ci95_pct": [100 * lo, 100 * hi],
        }
    return out
