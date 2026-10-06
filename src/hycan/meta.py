"""Meta-analysis of the Chahine rule across the corpus (manual §A.6, §14).

The headline question HyCAN-DB exists to answer (§1.3): does physisorptive H2
uptake on carbons scale with BET area as the Chahine rule claims — 1 wt% per
500 m2/g at 77 K — once the whole literature is pooled with explicit quality
weighting? No single paper can answer it; the corpus can.

Three functions, each taking the dataset and returning plain dicts so a notebook
can narrate them and a test can pin them:

* ``chahine_mixedlm`` — the slope of uptake on BET with **paper-level random
  intercepts**, because measurements from one paper are correlated and ignoring
  that inflates confidence in the slope (§E, "hierarchical regression"). Returns
  the fixed-effect slope and its 95% CI, expressed both per m2/g and per 500 m2/g
  (so it reads directly against the rule's "1 wt% / 500 m2/g").
* ``tier_sensitivity`` — the same slope recomputed over All / Tier A-B / Tier A
  rows, so a reader sees whether the result depends on including low-quality data
  (§13.3, §A.6 "sensitivity across tier-inclusion thresholds").
* ``publication_bias`` — a paper-level funnel + Egger-style intercept test on each
  paper's mean deviation from the Chahine prediction, to ask whether small or
  low-precision studies skew high (§7.4, §A.6). Honest about its limitation: the
  corpus carries no per-measurement standard errors, so precision is proxied by
  within-paper dispersion and sample size.

All three operate on the Chahine subset: 77 K, analysis-filtered (§12.3),
wt% present, a method-confirmed BET area, and ``total``-uptake rows excluded
(the rule bounds adsorbed, not total, uptake).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from hycan.load import analysis_subset, confirmed_bet_area

CHAHINE_WT_PCT_PER_M2 = 1.0 / 500.0  # the rule: 1 wt% per 500 m2/g


def chahine_subset(df: pd.DataFrame) -> pd.DataFrame:
    """The 77 K rows eligible for the Chahine comparison (matches Fig 3)."""
    w = analysis_subset(df, require_wt_pct=True).copy()
    w["bet"] = confirmed_bet_area(w)
    w["uptake_wt_pct"] = pd.to_numeric(w["uptake_wt_pct"], errors="coerce")
    w = w[
        (pd.to_numeric(w["temperature_k"], errors="coerce") == 77)
        & w["bet"].notna()
        & w["uptake_wt_pct"].notna()
        & (w["uptake_type"] != "total")
    ]
    return w


def chahine_mixedlm(
    df: pd.DataFrame,
    subset: pd.DataFrame | None = None,
    through_origin: bool = True,
) -> dict:
    """Fit uptake ~ BET with a random intercept per paper; return slope + 95% CI.

    The Chahine rule is *proportional* (uptake = BET / 500, no intercept), so the
    rule test is the through-origin fit (``through_origin=True``, the default):
    its fixed-effect slope is the corpus-level uptake-per-area, and
    ``wt_pct_per_500_m2`` reads directly against the rule's 1.0.

    ``through_origin=False`` fits a free intercept instead, which answers a
    different question — is the relationship even proportional? A nonzero
    intercept means low-area carbons still adsorb a baseline amount and the
    marginal slope is shallower than the through-origin fit implies.
    """
    w = chahine_subset(df) if subset is None else subset
    formula = "uptake_wt_pct ~ 0 + bet" if through_origin else "uptake_wt_pct ~ bet"
    md = smf.mixedlm(formula, data=w, groups=w["paper_id"])
    res = md.fit(reml=True, method="lbfgs")
    slope = float(res.params["bet"])
    ci = res.conf_int().loc["bet"]
    lo, hi = float(ci[0]), float(ci[1])
    out = {
        "through_origin": through_origin,
        "n_obs": int(w.shape[0]),
        "n_papers": int(w["paper_id"].nunique()),
        "slope_wt_pct_per_m2": slope,
        "slope_ci95": (lo, hi),
        # The reader-facing form: wt% per 500 m2/g, directly against the rule's 1.0
        "wt_pct_per_500_m2": slope * 500.0,
        "wt_pct_per_500_m2_ci95": (lo * 500.0, hi * 500.0),
        "chahine_reference": 1.0,
        "m2_per_g_per_wt_pct": (1.0 / slope) if slope else float("nan"),
        "meets_rule": bool(lo * 500.0 <= 1.0 <= hi * 500.0),
    }
    if not through_origin:
        out["intercept_wt_pct"] = float(res.params["Intercept"])
    return out


def _ols_through_origin(w: pd.DataFrame) -> float:
    x = w["bet"].to_numpy(float)
    y = w["uptake_wt_pct"].to_numpy(float)
    return float(np.sum(x * y) / np.sum(x * x)) if len(w) else float("nan")


def tier_sensitivity(df: pd.DataFrame) -> dict:
    """Chahine slope over All / Tier A-B / Tier A, by the mixed model and by a
    through-origin OLS (the rule has no intercept), so robustness is visible."""
    full = chahine_subset(df)
    out = {}
    for label, mask in (
        ("all_tiers", full["reproducibility_tier"].notna()),
        ("tier_AB", full["reproducibility_tier"].isin(["A", "B"])),
        ("tier_A", full["reproducibility_tier"] == "A"),
    ):
        w = full[mask]
        entry = {
            "n_obs": int(len(w)),
            "n_papers": int(w["paper_id"].nunique()),
            "ols_origin_wt_pct_per_500_m2": _ols_through_origin(w) * 500.0,
        }
        # MixedLM needs >1 group; guard the tier_A case.
        if w["paper_id"].nunique() > 1:
            try:
                mm = chahine_mixedlm(df, subset=w)
                entry["mixedlm_wt_pct_per_500_m2"] = mm["wt_pct_per_500_m2"]
                entry["mixedlm_ci95"] = mm["wt_pct_per_500_m2_ci95"]
            except Exception as exc:  # pragma: no cover - convergence guard
                entry["mixedlm_wt_pct_per_500_m2"] = None
                entry["mixedlm_error"] = str(exc)
        out[label] = entry
    return out


def publication_bias(df: pd.DataFrame) -> dict:
    """Paper-level funnel + Egger-style intercept test on deviation from Chahine.

    For each paper, the effect is the mean of (uptake - BET/500) over its 77 K
    rows — how far above or below the rule it sits — and precision is 1/SE of that
    mean (SE from within-paper dispersion, n>=2). Egger's test regresses the
    standardized effect on precision; a nonzero intercept is funnel asymmetry,
    the small-study signature of publication bias.

    Limitation, stated rather than hidden: these are not true meta-analytic
    standard errors (the papers do not report per-value uncertainty), so this
    detects dispersion-weighted asymmetry, not formal small-study bias.
    """
    w = chahine_subset(df).copy()
    w["resid"] = w["uptake_wt_pct"] - w["bet"] * CHAHINE_WT_PCT_PER_M2
    rows = []
    for pid, g in w.groupby("paper_id"):
        n = len(g)
        if n < 2:
            continue
        eff = float(g["resid"].mean())
        sd = float(g["resid"].std(ddof=1))
        if sd == 0 or np.isnan(sd):
            continue
        se = sd / np.sqrt(n)
        rows.append({"paper_id": pid, "n": n, "effect": eff, "se": se,
                     "precision": 1.0 / se})
    funnel = pd.DataFrame(rows)
    mean_eff = float(funnel["effect"].mean()) if len(funnel) else float("nan")
    result = {
        "n_papers_in_test": int(len(funnel)),
        "mean_effect_wt_pct": mean_eff,
    }
    if len(funnel) >= 3:
        # Egger: standardized effect ~ precision; intercept != 0 => asymmetry.
        y = (funnel["effect"] / funnel["se"]).to_numpy()
        x = sm.add_constant(funnel["precision"].to_numpy())
        egger = sm.OLS(y, x).fit()
        result["egger_intercept"] = float(egger.params[0])
        result["egger_intercept_p"] = float(egger.pvalues[0])
        result["egger_slope"] = float(egger.params[1])
        result["asymmetry_detected"] = bool(result["egger_intercept_p"] < 0.05)
    return result, funnel


def descriptive_summary(df: pd.DataFrame) -> dict:
    """Corpus-level descriptive numbers for notebook 03 / the v0.1 summary."""
    full = analysis_subset(df)
    wt = analysis_subset(df, require_wt_pct=True)
    tiers = df["reproducibility_tier"].value_counts().to_dict()
    return {
        "dataset_rows": int(len(df)),
        "dataset_papers": int(df["paper_id"].nunique()),
        "analysis_rows": int(len(full)),
        "analysis_papers": int(full["paper_id"].nunique()),
        "wt_pct_rows": int(len(wt)),
        "tier_counts_full": {k: int(v) for k, v in sorted(tiers.items())},
        "material_classes": int(df["material_class"].nunique()),
        "year_min": int(pd.to_numeric(df["year"], errors="coerce").min()),
        "year_max": int(pd.to_numeric(df["year"], errors="coerce").max()),
    }
