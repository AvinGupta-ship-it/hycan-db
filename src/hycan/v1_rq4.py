"""The RQ4 reporting-practice survey of the v1.0 protocol (§11, RQ4).

Items (a)-(j) are paper-level booleans over the probability sample, each
computed from the recorded fields (None = the paper is outside the item's
domain):

- a: every row of the paper has ``basis_stated`` true (an uncoded row counts
  false, because "every uptake value" cannot be verified for it);
- b: some row's ``wt_pct_convention_source`` is ``stated``, among papers
  with a printed wt% (a source of ``stated``, ``inferred_from_paired_units``
  or ``none``; a computed wt% prints none);
- c: some row reports a numerical ``uncertainty_wt_pct`` or
  ``replicates_reported``;
- d: some row meets §10.1 item 7 (:func:`hycan.v1.reporting_items`);
- e: some row has ``bet_range_stated`` or
  ``bet_consistency_criteria_stated``;
- f: some row states ``sample_mass_mg``;
- g: some row meets the §10.1 item-6 degassing rule;
- h: some row's ``plausibility_flag`` is true, among papers with at least
  one screenable row (a non-null flag);
- i: some row states ``h2_purity_pct``;
- j: some volumetric row's ``free_volume_calibration`` text names a gas and
  a temperature (a word-boundary gas name and a printed temperature or
  "room temperature"/"ambient", not overridden by "temperature not
  stated"), among papers with volumetric rows.

Estimator (§11, RQ4): the stratified ratio estimator with weight N_h/d_h.
With a constant weight per stratum the point estimate is
p̂ = Σ_h w_h Σ z / Σ_h w_h Σ t over the d_h taken records per stratum
(records outside the domain, `not_retrieved` and `frame_duplicate` included,
contribute zeros). Variance is by Taylor linearization with the
finite-population correction: u_i = z_i − p̂ t_i and
Var = T̂⁻² Σ_h N_h² (1 − d_h/N_h) s²_{u,h}/d_h. The 95% CI is
Korn-Graubard: the Clopper-Pearson interval at the effective sample size
n_e = p̂(1−p̂)/Var. When the linearized variance is zero (every domain paper
agrees), the exact Clopper-Pearson interval on the unweighted domain count
is reported instead.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from scipy import stats

from . import v1

ITEMS = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")
WT_PRINTED_SOURCES = ("stated", "inferred_from_paired_units", "none")


def _fv_gas_and_temp(text: str | None) -> bool:
    if text is None:
        return False
    t = text.lower()
    if "temperature not stated" in t:
        return False
    gas = re.search(r"\b(he|helium|n2|nitrogen|h2|hydrogen|ar|argon)\b", t)
    temp = (
        re.search(r"\d+(\.\d+)?\s*(k\b|°c)", t)
        or "room temperature" in t
        or "ambient" in t
    )
    return bool(gas) and bool(temp)


def paper_items(df: pd.DataFrame, papers: set[str]) -> pd.DataFrame:
    """One row per paper with items a-j (True/False/None) and the year."""
    out = []
    for pid, g in df[df["paper_id"].isin(sorted(papers))].groupby("paper_id"):
        sev = [
            (it or {}).get("7_instrument_and_calibration", False)
            for it in (v1.reporting_items(r) for _, r in g.iterrows())
        ]
        wt_sources = [v1.as_str(s) for s in g["wt_pct_convention_source"]]
        printed = [s for s in wt_sources if s in WT_PRINTED_SOURCES]
        flags = [v1.as_bool(x) for x in g["plausibility_flag"]]
        screenable = [f for f in flags if f is not None]
        vol = g[g["measurement_method"] == "volumetric_sieverts"]
        years = {v1.as_float(y) for y in g["year"]}
        if len(years) != 1:
            raise ValueError(f"{pid}: mixed years")
        out.append({
            "paper_id": pid, "year": int(years.pop()),
            "a": all(v1.as_bool(r.get("basis_stated")) is True
                     for _, r in g.iterrows()),
            "b": (any(s == "stated" for s in printed) if printed else None),
            "c": any(
                v1.as_bool(r.get("replicates_reported"))
                or v1.as_float(r.get("uncertainty_wt_pct")) is not None
                for _, r in g.iterrows()
            ),
            "d": any(sev),
            "e": any(
                v1.as_bool(r.get("bet_range_stated"))
                or v1.as_bool(r.get("bet_consistency_criteria_stated"))
                for _, r in g.iterrows()
            ),
            "f": g["sample_mass_mg"].map(v1.as_float).notna().any(),
            "g": any(
                v1.as_float(r.get("degas_temperature_c")) is not None
                and (v1.as_float(r.get("degas_duration_h")) is not None
                     or v1.as_float(r.get("degas_end_pressure_pa")) is not None)
                for _, r in g.iterrows()
            ),
            "h": (any(screenable) if screenable else None),
            "i": g["h2_purity_pct"].map(v1.as_float).notna().any(),
            "j": (any(_fv_gas_and_temp(v1.as_str(r.get("free_volume_calibration")))
                      for _, r in vol.iterrows()) if len(vol) else None),
        })
    return pd.DataFrame(out)


def kg_ci(p: float, var: float) -> tuple[float, float]:
    """The Korn-Graubard 95% CI at effective sample size p(1-p)/var."""
    n_e = p * (1 - p) / var
    x_e = n_e * p
    lo = 0.0 if p == 0 else float(stats.beta.ppf(0.025, x_e, n_e - x_e + 1))
    hi = 1.0 if p == 1 else float(stats.beta.ppf(0.975, x_e + 1, n_e - x_e))
    return lo, hi


def cp_ci(k: int, n: int) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(stats.beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(0.975, k + 1, n - k))
    return lo, hi


def ratio_estimate(frame: pd.DataFrame, strata: dict[str, str],
                   counts: dict[str, dict[str, float]], item: str,
                   domain: pd.Series | None = None) -> dict:
    """The stratified ratio estimate of item ``item`` over the papers of
    ``frame`` (optionally restricted to ``domain``), against the §7 walk
    counts ``counts[h] = {"N": N_h, "d": d_h}``."""
    y = frame[item]
    in_domain = y.notna()
    if domain is not None:
        in_domain &= domain
    t = in_domain.astype(float)
    z = t * y.where(in_domain, False).astype(float)
    h_of = frame["paper_id"].map(strata)
    z_hat = t_hat = 0.0
    for h, c in counts.items():
        w = c["N"] / c["d"]
        z_hat += w * float(z[h_of == h].sum())
        t_hat += w * float(t[h_of == h].sum())
    n, k = int(t.sum()), int(z.sum())
    if t_hat == 0:
        return {"n_domain": 0, "n_yes": 0}
    p = z_hat / t_hat
    var = 0.0
    for h, c in counts.items():
        u = (z - p * t)[h_of == h].to_numpy(float)
        u = np.concatenate([u, np.zeros(int(c["d"]) - len(u))])
        var += c["N"] ** 2 * (1 - c["d"] / c["N"]) * float(np.var(u, ddof=1)) \
            / c["d"]
    var /= t_hat ** 2
    if var > 0 and 0 < p < 1:
        lo, hi = kg_ci(p, var)
        method = "korn_graubard"
    else:
        lo, hi = cp_ci(k, n)
        method = "clopper_pearson_unweighted"
    return {
        "n_domain": n, "n_yes": k, "p_hat": p, "se": float(np.sqrt(var)),
        "ci95": [lo, hi], "ci_method": method,
    }


def fit_rq4(frame: pd.DataFrame, strata: dict[str, str],
            counts: dict[str, dict[str, float]]) -> dict:
    out = {}
    early = frame["year"] <= 2015
    for item in ITEMS:
        out[item] = ratio_estimate(frame, strata, counts, item)
        out[item]["by_period"] = {
            "le_2015": ratio_estimate(frame, strata, counts, item, early),
            "ge_2016": ratio_estimate(frame, strata, counts, item, ~early),
        }
    return out
