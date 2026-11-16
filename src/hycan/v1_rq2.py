"""The RQ2 models of the v1.0 protocol (docs/v1_protocol.md §11, RQ2).

Data: coded 77 K isothermal rows at 0.9-1.2 bar with ``basis_inferred`` in
{excess, absolute, unknown}, the §11.0 row filters, a §11.0-eligible BET area
of at least 300 m² g⁻¹ and a positive W1 uptake.

Unit of analysis: the §11.0 rule applied to the RQ2 window - per sample and
laboratory, the geometric mean of the eligible rows' uptake and pressure; a
sample measured by several laboratories within a paper enters once, at the
median of the laboratory values, under ``<paper_id>-multilab``.

Models (random effects as in RQ1, via :func:`hycan.v1_rq1._fit_mixed`):

- (a) ln n = a + b·ln A_BET + c·ln(P/1 bar);
- (b) the same with ln V_micro in place of ln A_BET, separately for
  N₂-derived V_micro (``pore_volume_method`` DR, DFT, NLDFT, QSDFT or
  t_plot, ``pore_volume_probe_gas`` N2) and for CO₂-derived V_micro
  (``micropore_volume_co2_cm3_g``), never mixing the two;
- (c) the RQ1 ratio model on the same units, reported as the 1-bar ratio to
  A_BET/500.

BET and V_micro are compared on the samples that have both: (a) and (b)
refitted there, with ML AIC alongside the slopes (REML log-likelihoods are
not comparable across fixed effects).
"""

from __future__ import annotations

from statistics import geometric_mean, median

import numpy as np
import pandas as pd

from . import v1, v1_rq1

RQ2_BASES = ("excess", "absolute", "unknown")
P_WINDOW = (0.9, 1.2)
N2_METHODS = ("DR", "DFT", "NLDFT", "QSDFT", "t_plot")


def _n2_vmicro(row: pd.Series) -> float | None:
    v = v1.as_float(row.get("micropore_volume_cm3_g"))
    if (
        v is None
        or v1.as_str(row.get("pore_volume_method")) not in N2_METHODS
        or v1.as_str(row.get("pore_volume_probe_gas")) != "N2"
    ):
        return None
    return v


def rq2_rows(df: pd.DataFrame, papers: set[str], *,
             require_area: bool = True) -> pd.DataFrame:
    """The eligible window rows, with the §11.0 area, W1 uptake and the two
    V_micro readings attached. ``require_area=False`` drops the area
    condition (RQ3 uses the window uptake without regressing on area)."""
    out = []
    for _, r in df.iterrows():
        if r["paper_id"] not in papers or not v1.is_coded(r):
            continue
        p = v1.as_float(r.get("pressure_bar"))
        if (
            not v1.is_77k(r.get("temperature_k"))
            or v1.as_bool(r.get("temperature_unstated"))
            or not v1._usable_point_row(r)
            or v1.as_str(r.get("value_kind")) != "measured"
            or v1.as_str(r.get("basis_inferred")) not in RQ2_BASES
            or p is None or not P_WINDOW[0] <= p <= P_WINDOW[1]
        ):
            continue
        area = v1.eligible_bet_area(r)
        if require_area and (area is None or area < 300.0):
            continue
        w1 = v1.w1_wt_pct(r)
        if w1 is None or w1 <= 0:
            continue
        out.append({
            "measurement_id": r["measurement_id"], "paper_id": r["paper_id"],
            "sample_id": r["sample_id"],
            "lab_id": v1.as_str(r.get("measuring_lab_id")),
            "pressure_bar": p, "n_w1_wt_pct": w1, "a_bet_m2_g": area,
            "vmicro_n2_cm3_g": _n2_vmicro(r),
            "vmicro_co2_cm3_g": v1.as_float(r.get("micropore_volume_co2_cm3_g")),
        })
    return pd.DataFrame(out)


def _one(values) -> float | None:
    vals = sorted({float(v) for v in values if pd.notna(v)})
    if not vals:
        return None
    if len(vals) > 1:
        raise ValueError(f"conflicting sample values {vals}")
    return vals[0]


def rq2_samples(df: pd.DataFrame, papers: set[str]) -> pd.DataFrame:
    """One analysis unit per sample (§11.0 rule applied to the RQ2 window)."""
    rows = rq2_rows(df, papers)
    if rows.empty:
        return pd.DataFrame(columns=[
            "paper_id", "sample_id", "lab_id", "n_rows", "n_labs",
            "n_w1_wt_pct", "pressure_bar", "a_bet_m2_g", "vmicro_n2_cm3_g",
            "vmicro_co2_cm3_g",
        ])
    per_lab = []
    for (pid, sid, lab), g in rows.groupby(
        ["paper_id", "sample_id", "lab_id"], dropna=False, sort=True
    ):
        per_lab.append({
            "paper_id": pid, "sample_id": sid, "lab_id": lab,
            "n_rows": len(g),
            "n": geometric_mean(g["n_w1_wt_pct"]),
            "p": geometric_mean(g["pressure_bar"]),
            "area": _one(g["a_bet_m2_g"]),
            "vn2": _one(g["vmicro_n2_cm3_g"]),
            "vco2": _one(g["vmicro_co2_cm3_g"]),
        })
    out = []
    for (pid, sid), g in pd.DataFrame(per_lab).groupby(
        ["paper_id", "sample_id"], sort=True
    ):
        first = g.iloc[0]
        multi = len(g) > 1
        out.append({
            "paper_id": pid, "sample_id": sid,
            "lab_id": f"{pid}-multilab" if multi else first["lab_id"],
            "n_rows": int(g["n_rows"].sum()), "n_labs": len(g),
            "n_w1_wt_pct": median(g["n"]) if multi else first["n"],
            "pressure_bar": median(g["p"]) if multi else first["p"],
            "a_bet_m2_g": _one(g["area"]),
            "vmicro_n2_cm3_g": _one(g["vn2"]),
            "vmicro_co2_cm3_g": _one(g["vco2"]),
        })
    return pd.DataFrame(out)


def _slope_fit(frame: pd.DataFrame, predictor: str, label: str) -> dict:
    """Model (a)/(b): ln n on ln(predictor) and ln(P/1 bar)."""
    sub = frame.dropna(subset=[predictor]).copy()
    sub = sub[sub[predictor] > 0]
    if len(sub) < 5 or sub["paper_id"].nunique() < 3:
        return {"skipped": f"{len(sub)} samples"}
    sub["y"] = np.log(sub["n_w1_wt_pct"])
    sub["ln_x"] = np.log(sub[predictor])
    sub["ln_p"] = np.log(sub["pressure_bar"])
    labs = int(sub["lab_id"].nunique())
    fit = v1_rq1._fit_mixed(sub, "ln_x + ln_p")
    terms = {}
    for name, b, se in zip(fit["names"], fit["params"], fit["se"]):
        lo, hi = v1_rq1._interval(b, se, labs)
        key = {"ln_x": f"b_ln_{label}", "ln_p": "c_ln_p"}.get(name, name)
        terms[key] = {"estimate": b, "se": se, "ci95": [float(lo), float(hi)]}
    return {
        "n_samples": len(sub), "n_papers": int(sub["paper_id"].nunique()),
        "n_labs": labs, "terms": terms,
        "lab_variance_zero": fit["lab_variance_zero"],
    }


def _ml_aic(frame: pd.DataFrame, predictor: str) -> float:
    """ML AIC of the (a)/(b) model, for the same-subset comparison."""
    import warnings

    from statsmodels.regression.mixed_linear_model import MixedLM

    sub = frame.copy()
    sub["y"] = np.log(sub["n_w1_wt_pct"])
    sub["ln_x"] = np.log(sub[predictor])
    sub["ln_p"] = np.log(sub["pressure_bar"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            res = MixedLM.from_formula(
                "y ~ ln_x + ln_p", groups="lab_id", re_formula="1",
                vc_formula={"paper": "0 + C(paper_id)"}, data=sub,
            ).fit(reml=False)
        except (np.linalg.LinAlgError, ValueError):
            res = MixedLM.from_formula(
                "y ~ ln_x + ln_p", groups="paper_id", re_formula="1", data=sub,
            ).fit(reml=False)
    return float(res.aic)


def fit_rq2(samples: pd.DataFrame, *, n_boot: int = v1_rq1.BOOT_N,
            seed: int = v1_rq1.BOOT_SEED) -> dict:
    """All RQ2 models from the sample table."""
    out = {
        "a_bet": _slope_fit(samples, "a_bet_m2_g", "a_bet"),
        "b_vmicro_n2": _slope_fit(samples, "vmicro_n2_cm3_g", "vmicro"),
        "b_vmicro_co2": _slope_fit(samples, "vmicro_co2_cm3_g", "vmicro"),
    }
    ratio_in = samples.rename(columns={"n_w1_wt_pct": "n_ex_max_w1_wt_pct"})
    out["c_one_bar_ratio"] = v1_rq1.fit_primary(ratio_in, n_boot=n_boot,
                                                seed=seed)
    both = samples.dropna(subset=["a_bet_m2_g", "vmicro_n2_cm3_g"])
    both = both[both["vmicro_n2_cm3_g"] > 0]
    if len(both) >= 5 and both["paper_id"].nunique() >= 3:
        out["comparison_same_samples"] = {
            "n_samples": len(both),
            "n_papers": int(both["paper_id"].nunique()),
            "a_bet": _slope_fit(both, "a_bet_m2_g", "a_bet"),
            "b_vmicro_n2": _slope_fit(both, "vmicro_n2_cm3_g", "vmicro"),
            "ml_aic": {"a_bet": _ml_aic(both, "a_bet_m2_g"),
                       "b_vmicro_n2": _ml_aic(both, "vmicro_n2_cm3_g")},
        }
    else:
        out["comparison_same_samples"] = {"skipped": f"{len(both)} samples"}
    return out
