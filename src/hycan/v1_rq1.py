"""The RQ1 models of the v1.0 protocol (docs/v1_protocol.md §11, RQ1).

Primary: a linear mixed model on y = ln[n_ex,max / (A_BET/500)] with random
intercepts for laboratory and paper-within-laboratory; the sample is the
residual. Fitted by REML, unweighted. exp(mu) is the geometric-mean ratio;
its 95% CI is t-based on L − 1 degrees of freedom (L laboratories), a
laboratory-cluster bootstrap (2,000 resamples, seed 20261030) is also run,
and the §11 decision uses the wider of the two intervals against
[1/1.15, 1.15]. The 95% prediction interval (a new sample from a new
laboratory) adds all three variance components to the mean's variance. If
the laboratory variance is estimated at zero (succeeding at nothing beyond
1e-8), the model is refitted without it and ``lab_variance_zero`` is set.

Secondary: ln n_ex,max = a + b·ln A_BET with the same random effects; b is
reported with a reliability correction b/λ, λ = 1 − σ_u²/s²(ln A_BET), for
σ_u = ln(1.10) and ln(1.20).
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats

MARGIN = (1 / 1.15, 1.15)
BOOT_SEED = 20261030
BOOT_N = 2000


def _fit_mixed(frame: pd.DataFrame, rhs: str = "1") -> dict:
    """REML fit of ``y ~ rhs`` with laboratory and paper-within-laboratory
    random intercepts; refitted with paper-only random intercepts when the
    laboratory variance is estimated at zero (§11, RQ1)."""
    from statsmodels.regression.mixed_linear_model import MixedLM

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            res = MixedLM.from_formula(
                f"y ~ {rhs}", groups="lab_id", re_formula="1",
                vc_formula={"paper": "0 + C(paper_id)"}, data=frame,
            ).fit(reml=True)
            lab_var = float(np.asarray(res.cov_re)[0, 0])
            paper_var = float(res.vcomp[0]) if len(res.vcomp) else 0.0
            lab_zero = lab_var <= 1e-8
        except (np.linalg.LinAlgError, ValueError):
            # Papers coincide too nearly with laboratories for the laboratory
            # variance to be estimated: the §11 zero-variance refit applies.
            res, lab_zero = None, True
        if lab_zero:
            res = MixedLM.from_formula(
                f"y ~ {rhs}", groups="paper_id", re_formula="1", data=frame,
            ).fit(reml=True)
            lab_var, paper_var = 0.0, float(np.asarray(res.cov_re)[0, 0])
    k = len(res.fe_params)
    return {
        "params": [float(p) for p in res.fe_params],
        "se": [float(s) for s in res.bse[:k]],
        "lab_var": lab_var, "paper_var": paper_var,
        "resid_var": float(res.scale), "lab_variance_zero": lab_zero,
    }


def _interval(mu: float, se: float, labs: int) -> tuple[float, float]:
    t = float(stats.t.ppf(0.975, labs - 1))
    return (mu - t * se, mu + t * se)


def _resample_labs(frame: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    labs = sorted(frame["lab_id"].unique())
    picked = rng.choice(np.array(labs, dtype=object), size=len(labs), replace=True)
    parts = []
    for i, lab in enumerate(picked):
        g = frame[frame["lab_id"] == lab].copy()
        g["lab_id"] = f"boot{i}:{lab}"
        g["paper_id"] = "boot" + str(i) + ":" + g["paper_id"]
        parts.append(g)
    return pd.concat(parts, ignore_index=True)


def decision(lo: float, hi: float) -> str:
    if MARGIN[0] <= lo and hi <= MARGIN[1]:
        return "supported"
    if hi < MARGIN[0]:
        return "overstates"
    if lo > MARGIN[1]:
        return "understates"
    return "inconclusive"


def fit_primary(samples: pd.DataFrame, *, n_boot: int = BOOT_N,
                seed: int = BOOT_SEED) -> dict:
    frame = samples.rename(columns={}).copy()
    frame["y"] = np.log(
        frame["n_ex_max_w1_wt_pct"] / (frame["a_bet_m2_g"] / 500.0)
    )
    labs = int(frame["lab_id"].nunique())
    fit = _fit_mixed(frame, "1")
    mu, se = fit["params"][0], fit["se"][0]
    ci_t = _interval(mu, se, labs)
    rng = np.random.default_rng(seed)
    mus, failures = [], 0
    for _ in range(n_boot):
        try:
            mus.append(_fit_mixed(_resample_labs(frame, rng), "1")["params"][0])
        except Exception:
            failures += 1
    ci_boot = (
        (float(np.percentile(mus, 2.5)), float(np.percentile(mus, 97.5)))
        if mus else (float("nan"), float("nan"))
    )
    wider = (min(ci_t[0], ci_boot[0]), max(ci_t[1], ci_boot[1])) if mus else ci_t
    sd_all = np.sqrt(se**2 + fit["lab_var"] + fit["paper_var"] + fit["resid_var"])
    t = float(stats.t.ppf(0.975, labs - 1))
    pred = (mu - t * sd_all, mu + t * sd_all)
    return {
        "n_samples": int(len(frame)), "n_papers": int(frame["paper_id"].nunique()),
        "n_labs": labs,
        "mu": mu, "se": se,
        "ratio": float(np.exp(mu)),
        "ci95_t": [float(np.exp(x)) for x in ci_t],
        "ci95_bootstrap": [float(np.exp(x)) for x in ci_boot],
        "bootstrap_resamples": len(mus), "bootstrap_failures": failures,
        "ci95_decision": [float(np.exp(x)) for x in wider],
        "decision": decision(*[float(np.exp(x)) for x in wider]),
        "prediction_interval_95": [float(np.exp(x)) for x in pred],
        "variances": {"laboratory": fit["lab_var"], "paper": fit["paper_var"],
                      "sample": fit["resid_var"]},
        "lab_variance_zero": fit["lab_variance_zero"],
    }


def fit_secondary(samples: pd.DataFrame) -> dict:
    frame = samples.copy()
    frame["y"] = np.log(frame["n_ex_max_w1_wt_pct"])
    frame["ln_area"] = np.log(frame["a_bet_m2_g"])
    frame["ln_area_c"] = frame["ln_area"] - frame["ln_area"].mean()
    labs = int(frame["lab_id"].nunique())
    fit = _fit_mixed(frame, "ln_area_c")
    b, se = fit["params"][1], fit["se"][1]
    ci = _interval(b, se, labs)
    s2 = float(frame["ln_area"].var(ddof=1))
    corrected = {}
    for pct, su in (("10", np.log(1.10)), ("20", np.log(1.20))):
        lam = 1.0 - su**2 / s2
        corrected[f"b_corrected_{pct}pct"] = float(b / lam)
    return {
        "b": float(b), "se": float(se), "ci95": [float(x) for x in ci],
        "s2_ln_area": s2, **corrected,
        "lab_variance_zero": fit["lab_variance_zero"],
    }
