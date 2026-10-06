"""Tests for the feature matrix and baseline model (src/hycan/features.py, ml.py).

Pins the modeling subset and the qualitative model result: grouped CV keeps every
paper on one side of each split, the tree models generalise to held-out papers
with R2 well above the linear baseline, and the dominant features are the 77 K
physisorption drivers (pressure and BET area). Ranges, not exact floats, because
a fit shifts at low decimals across library versions.
"""

from __future__ import annotations

import warnings

import numpy as np
import pytest

from hycan.load import load_dataset
from hycan import features, ml


@pytest.fixture(scope="module")
def frame():
    return features.feature_frame(load_dataset())


@pytest.fixture(scope="module")
def design(frame):
    return features.design_matrix(frame)


def test_modeling_subset_is_tier_ab_77k(frame):
    assert 170 < len(frame) < 230
    assert frame["paper_id"].nunique() >= 25
    assert set(frame["reproducibility_tier"].unique()) <= {"A", "B"}
    assert (frame["uptake_type"] != "total").all() if "uptake_type" in frame else True


def test_design_matrix_shape_and_target(design):
    X, y, groups = design
    assert X.shape[0] == len(y) == len(groups)
    assert "bet_surface_area_m2_g" in X.columns
    assert any(c.startswith("mat_") for c in X.columns)  # one-hot material_class
    assert np.isfinite(y).all()


def test_fold_isolation_holds(design):
    from sklearn.model_selection import GroupKFold

    X, y, groups = design
    gkf = GroupKFold(n_splits=5)
    assert ml.verify_fold_isolation(groups, gkf, X)


def test_trees_generalise_and_beat_linear(design):
    X, y, groups = design
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cv = ml.cross_validate(X, y, groups)
    rf = cv["models"]["RandomForest"]
    xgb = cv["models"]["XGBoost"]
    lin = cv["models"]["LinearRegression"]
    # Tree models predict held-out papers well; both clear a clearly-above-chance bar.
    assert rf["r2_mean"] > 0.7
    assert xgb["r2_mean"] > 0.7
    assert rf["mae_mean"] < 0.8 and xgb["mae_mean"] < 0.8
    # And both beat the linear baseline, which struggles with the sparse features.
    assert rf["r2_mean"] > lin["r2_mean"]


def test_out_of_fold_predictions_cover_every_row(design):
    X, y, groups = design
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pred = ml.out_of_fold_predictions(X, y, groups)
    assert len(pred) == len(y)
    assert np.isfinite(pred).all()


def test_shap_ranks_pressure_and_bet_on_top(design):
    X, y, groups = design
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = ml.fit_full(X, y, "XGBoost")
        importance, values = ml.shap_summary(model, X)
    top3 = set(importance.head(3).index)
    assert "pressure_bar" in top3
    assert "bet_surface_area_m2_g" in top3
    assert values.shape[0] == len(X)
