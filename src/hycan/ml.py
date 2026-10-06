"""Baseline model with grouped cross-validation (manual §14).

The deliverable is not "ML was applied" but ML applied correctly (§14.4):
cross-validation **grouped by paper** so the model is scored on papers it never
trained on, with honest uncertainty (fold spread), transparent feature
attribution (SHAP), and the fold isolation verified rather than assumed.

Three models are compared: ``LinearRegression`` and ``RandomForestRegressor``
(both on median-imputed features -- the stated imputation, since neither handles
NaN) and ``XGBRegressor`` (native NaN handling, so pore-volume missingness is not
imputed away). XGBoost is the primary model used for the predicted-vs-measured
figure and the SHAP attribution.

Every performance statement carries the number of *papers*, not only rows: with
~30 groups a reader needs the group count to judge the interval (§14.4).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor

N_SPLITS = 5
RANDOM_STATE = 0


def _models():
    """Fresh model instances. Linear/RF are wrapped with median imputation; XGB
    handles NaN natively."""
    return {
        "LinearRegression": make_pipeline(
            SimpleImputer(strategy="median"), LinearRegression()
        ),
        "RandomForest": make_pipeline(
            SimpleImputer(strategy="median"),
            RandomForestRegressor(n_estimators=400, random_state=RANDOM_STATE),
        ),
        "XGBoost": XGBRegressor(
            n_estimators=400, max_depth=3, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, random_state=RANDOM_STATE,
        ),
    }


def verify_fold_isolation(groups, splitter, X) -> bool:
    """Confirm no paper appears in both train and test in any fold (§14.4)."""
    groups = np.asarray(groups)
    for tr, te in splitter.split(X, groups=groups):
        if set(groups[tr]) & set(groups[te]):
            return False
    return True


def cross_validate(X: pd.DataFrame, y, groups) -> dict:
    """Grouped 5-fold CV for each model; return mean +/- SD of MAE and R2.

    n_splits is capped at the number of distinct papers so the call is valid on
    small subsets.
    """
    n_groups = len(set(groups))
    n_splits = min(N_SPLITS, n_groups)
    gkf = GroupKFold(n_splits=n_splits)
    assert verify_fold_isolation(groups, gkf, X), "paper leaked across a fold"
    out = {"n_rows": int(len(X)), "n_papers": int(n_groups),
           "n_splits": int(n_splits), "models": {}}
    for name, model in _models().items():
        maes, r2s = [], []
        for tr, te in gkf.split(X, y, groups=groups):
            m = _clone(model)
            m.fit(X.iloc[tr], y[tr])
            pred = m.predict(X.iloc[te])
            maes.append(mean_absolute_error(y[te], pred))
            r2s.append(r2_score(y[te], pred))
        out["models"][name] = {
            "mae_mean": float(np.mean(maes)), "mae_sd": float(np.std(maes, ddof=1)),
            "r2_mean": float(np.mean(r2s)), "r2_sd": float(np.std(r2s, ddof=1)),
            "mae_folds": [float(v) for v in maes],
            "r2_folds": [float(v) for v in r2s],
        }
    return out


def _clone(model):
    from sklearn.base import clone
    return clone(model)


def out_of_fold_predictions(X: pd.DataFrame, y, groups, model_name="XGBoost"):
    """Out-of-fold predictions for every row (each predicted by a model that did
    not train on its paper). Returns a y_pred array aligned to X's rows."""
    groups = np.asarray(groups)
    gkf = GroupKFold(n_splits=min(N_SPLITS, len(set(groups))))
    pred = np.full(len(y), np.nan)
    base = _models()[model_name]
    for tr, te in gkf.split(X, y, groups=groups):
        m = _clone(base)
        m.fit(X.iloc[tr], y[tr])
        pred[te] = m.predict(X.iloc[te])
    return pred


def fit_full(X: pd.DataFrame, y, model_name="XGBoost"):
    """Fit one model on all rows (for SHAP attribution over the whole subset)."""
    m = _models()[model_name]
    m.fit(X, y)
    return m


def shap_summary(model, X: pd.DataFrame):
    """Mean |SHAP| per feature for a fitted XGBoost model, most important first."""
    import shap

    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(X)
    importance = np.abs(values).mean(axis=0)
    order = np.argsort(importance)[::-1]
    return (
        pd.Series(importance[order], index=X.columns[order], name="mean_abs_shap"),
        values,
    )
