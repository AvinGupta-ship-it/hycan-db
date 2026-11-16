"""The RQ5 prediction baselines of the v1.0 protocol (§11, RQ5).

Target rows: coded 77 K isothermal rows with ``basis_inferred = excess``
from an isotherm with ``basis_shape_conflict = false``, the §11.0 row
filters, P ≤ 100 bar, a §11.0-eligible BET area and a W1 uptake. All three
models are trained and scored on the same rows; the target is the W1 wt%.

Models: (a) the physical baseline n = k·A_BET·P/(P + p₀), k and p₀ fitted
by least squares; (b) the linear model in A_BET, ln P and A_BET·ln P;
(c) gradient-boosted trees (XGBoost, n_estimators 500, learning_rate 0.05,
max_depth 4, others default). Features for (c): ln A_BET, ln P and P;
one-hot material class (classes with fewer than 5 papers in the target set
merged into ``other``) and measurement method; total and micropore volume
(missing left missing); dopant and metal presence; publication year.

Validation: GroupKFold(n_splits=5, shuffle=True, random_state=r) for
r = 0..19, grouped by paper (sensitivity: by laboratory). Per partition the
pooled out-of-fold R² and MAE, overall and within the ≤ 1.2 bar and
≥ 10 bar regimes; reported as the mean and the 2.5-97.5 percentiles across
partitions, plus a paper-level bootstrap 95% CI (2,000 resamples, seed
20261032) on partition r = 0. The row-weight sensitivity weights rows by
1/(rows in their paper) in both fitting and scoring.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from . import v1

BOOT_SEED = 20261032
BOOT_N = 2000
N_PARTITIONS = 20
# n_jobs is an execution setting, not a model hyperparameter: single-thread
# runs identically and avoids thread thrash on small machines.
XGB_PARAMS = {"n_estimators": 500, "learning_rate": 0.05, "max_depth": 4,
              "n_jobs": 1}


def rq5_rows(df: pd.DataFrame, papers: set[str]) -> pd.DataFrame:
    """The RQ5 target rows with their features."""
    iso = v1.isotherm_table(df)
    conflict = dict(zip(iso["isotherm_key"], iso["basis_shape_conflict"]))
    out = []
    for _, r in df.iterrows():
        if r["paper_id"] not in papers or not v1.is_coded(r):
            continue
        key = v1.isotherm_key(r)
        if key not in conflict or bool(conflict[key]):
            continue
        p = v1.as_float(r.get("pressure_bar"))
        if (
            not v1._usable_point_row(r)
            or v1.as_str(r.get("value_kind")) != "measured"
            or p is None or p <= 0 or p > 100.0
        ):
            continue
        area = v1.eligible_bet_area(r)
        w1 = v1.w1_wt_pct(r)
        if area is None or w1 is None:
            continue
        out.append({
            "measurement_id": r["measurement_id"], "paper_id": r["paper_id"],
            "lab_id": v1.as_str(r.get("measuring_lab_id")) or "unknown",
            "n_w1_wt_pct": w1, "a_bet_m2_g": area, "pressure_bar": p,
            "material_class": v1.as_str(r.get("material_class")) or "other",
            "method": v1.as_str(r.get("measurement_method")) or "unknown",
            "v_total_cm3_g": v1.as_float(r.get("total_pore_volume_cm3_g")),
            "v_micro_cm3_g": v1.as_float(r.get("micropore_volume_cm3_g")),
            "dopant_present": v1.as_str(r.get("dopant_element")) is not None,
            "metal_present": v1.as_str(r.get("metal_element")) is not None,
            "year": v1.as_float(r.get("year")),
        })
    return pd.DataFrame(out)


def feature_matrix(rows: pd.DataFrame) -> pd.DataFrame:
    """The (c) feature matrix: deterministic columns from the target set."""
    classes = rows.groupby("material_class")["paper_id"].nunique()
    small = set(classes[classes < 5].index)
    merged = rows["material_class"].map(
        lambda c: "other" if c in small else c)
    x = pd.DataFrame({
        "ln_a": np.log(rows["a_bet_m2_g"]),
        "ln_p": np.log(rows["pressure_bar"]),
        "p": rows["pressure_bar"],
        "v_total": rows["v_total_cm3_g"],
        "v_micro": rows["v_micro_cm3_g"],
        "dopant": rows["dopant_present"].astype(float),
        "metal": rows["metal_present"].astype(float),
        "year": rows["year"],
    }, index=rows.index)
    for name, series in (("class", merged), ("method", rows["method"])):
        for level in sorted(series.unique()):
            x[f"{name}_{level}"] = (series == level).astype(float)
    return x


def _fit_physical(a, p, y, w=None):
    from scipy.optimize import curve_fit

    def f(x, k, p0):
        area, pres = x
        return k * area * pres / (pres + p0)

    sigma = None if w is None else 1.0 / np.sqrt(w)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        (k, p0), _ = curve_fit(f, (a, p), y, p0=(1 / 500.0, 5.0),
                               bounds=([0, 1e-6], [np.inf, np.inf]),
                               sigma=sigma, maxfev=20000)
    return lambda a2, p2: k * a2 * p2 / (p2 + p0)


def _fit_linear(a, p, y, w=None):
    x = np.column_stack([np.ones_like(a), a, np.log(p), a * np.log(p)])
    ww = np.ones_like(y) if w is None else w
    beta = np.linalg.lstsq(x * np.sqrt(ww)[:, None],
                           y * np.sqrt(ww), rcond=None)[0]
    return lambda a2, p2: np.column_stack(
        [np.ones_like(a2), a2, np.log(p2), a2 * np.log(p2)]) @ beta


def _fit_xgb(x, y, w=None):
    from xgboost import XGBRegressor

    m = XGBRegressor(**XGB_PARAMS)
    m.fit(x, y, sample_weight=w)
    return m


def oof_predictions(rows: pd.DataFrame, x: pd.DataFrame, *, groups: str,
                    random_state: int, weighted: bool) -> pd.DataFrame:
    """Pooled out-of-fold predictions of the three models for one partition."""
    from sklearn.model_selection import GroupKFold

    a = rows["a_bet_m2_g"].to_numpy(float)
    p = rows["pressure_bar"].to_numpy(float)
    y = rows["n_w1_wt_pct"].to_numpy(float)
    w = (1.0 / rows.groupby("paper_id")["paper_id"].transform("size")
         .to_numpy(float)) if weighted else None
    preds = {m: np.full(len(rows), np.nan) for m in ("physical", "linear",
                                                     "xgboost")}
    gkf = GroupKFold(n_splits=5, shuffle=True, random_state=random_state)
    for tr, te in gkf.split(x, y, groups=rows[groups]):
        wtr = None if w is None else w[tr]
        preds["physical"][te] = _fit_physical(a[tr], p[tr], y[tr], wtr)(
            a[te], p[te])
        preds["linear"][te] = _fit_linear(a[tr], p[tr], y[tr], wtr)(
            a[te], p[te])
        preds["xgboost"][te] = _fit_xgb(x.iloc[tr], y[tr], wtr).predict(
            x.iloc[te])
    out = rows[["paper_id", "lab_id", "pressure_bar", "n_w1_wt_pct"]].copy()
    for m, v in preds.items():
        out[m] = v
    if weighted:
        out["w"] = w
    return out


def _metrics(y, yhat, w=None) -> dict:
    if len(y) == 0:
        return {"r2": float("nan"), "mae": float("nan"), "n": 0}
    w = np.ones_like(y) if w is None else w
    ybar = np.average(y, weights=w)
    ss_res = float(np.average((y - yhat) ** 2, weights=w))
    ss_tot = float(np.average((y - ybar) ** 2, weights=w))
    return {
        "r2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
        "mae": float(np.average(np.abs(y - yhat), weights=w)),
        "n": int(len(y)),
    }


def score(oof: pd.DataFrame, weighted: bool = False) -> dict:
    """Per-model metrics overall and within the two pressure regimes."""
    out = {}
    regimes = {
        "overall": np.ones(len(oof), dtype=bool),
        "le_1p2_bar": (oof["pressure_bar"] <= 1.2).to_numpy(),
        "ge_10_bar": (oof["pressure_bar"] >= 10.0).to_numpy(),
    }
    w = oof["w"].to_numpy(float) if weighted else None
    y = oof["n_w1_wt_pct"].to_numpy(float)
    for model in ("physical", "linear", "xgboost"):
        yhat = oof[model].to_numpy(float)
        out[model] = {
            name: _metrics(y[m], yhat[m], None if w is None else w[m])
            for name, m in regimes.items()
        }
    return out


def paper_bootstrap(oof: pd.DataFrame, *, n_boot: int = BOOT_N,
                    seed: int = BOOT_SEED) -> dict:
    """Paper-level bootstrap CIs of the partition-0 metrics."""
    rng = np.random.default_rng(seed)
    papers = sorted(oof["paper_id"].unique())
    pid_arr = oof["paper_id"].to_numpy()
    idx = {pid: np.flatnonzero(pid_arr == pid) for pid in papers}
    draws: dict[tuple[str, str, str], list[float]] = {}
    for _ in range(n_boot):
        picked = rng.choice(np.array(papers, dtype=object), size=len(papers),
                            replace=True)
        boot = oof.iloc[np.concatenate([idx[pid] for pid in picked])]
        for model, regs in score(boot).items():
            for reg, met in regs.items():
                for name in ("r2", "mae"):
                    draws.setdefault((model, reg, name), []).append(met[name])
    out: dict = {}
    for (model, reg, name), vals in draws.items():
        arr = np.array(vals, dtype=float)
        arr = arr[np.isfinite(arr)]
        ci = ([float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))]
              if len(arr) else [float("nan"), float("nan")])
        out.setdefault(model, {}).setdefault(reg, {})[f"{name}_ci95"] = ci
    return out


def summarize(per_partition: list[dict]) -> dict:
    """Mean and 2.5-97.5 percentiles of each metric across partitions."""
    out: dict = {}
    for model in ("physical", "linear", "xgboost"):
        out[model] = {}
        for reg in ("overall", "le_1p2_bar", "ge_10_bar"):
            out[model][reg] = {"n": per_partition[0][model][reg]["n"]}
            for name in ("r2", "mae"):
                vals = np.array([p[model][reg][name] for p in per_partition])
                out[model][reg][name] = {
                    "mean": float(vals.mean()),
                    "p2_5": float(np.percentile(vals, 2.5)),
                    "p97_5": float(np.percentile(vals, 97.5)),
                }
    return out
