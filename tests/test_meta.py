"""Tests for the meta-analysis (src/hycan/meta.py).

These pin the scientific result within plausible ranges rather than to exact
floats (a mixed-model fit can shift at the 4th decimal across BLAS/statsmodels
versions), and assert the qualitative findings the v0.1 summary rests on: the
corpus falls short of the Chahine rule, the shortfall survives tier restriction,
and the relationship carries a positive baseline offset.
"""

from __future__ import annotations

import warnings

import pytest

from hycan.load import load_dataset
from hycan import meta


@pytest.fixture(scope="module")
def df():
    return load_dataset()


def test_chahine_subset_matches_the_figure(df):
    sub = meta.chahine_subset(df)
    # Same subset Fig 3 plots: 77 K, confirmed BET, wt%, total excluded.
    assert 180 < len(sub) < 230
    assert sub["paper_id"].nunique() >= 25
    assert (sub["uptake_type"] != "total").all()


def test_chahine_rule_is_overstated_by_the_corpus(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = meta.chahine_mixedlm(df, through_origin=True)
    # The corpus reaches well under 1 wt% per 500 m2/g, and the 95% CI excludes
    # the rule's 1.0 -- the headline finding.
    assert 0.5 < res["wt_pct_per_500_m2"] < 0.9
    lo, hi = res["wt_pct_per_500_m2_ci95"]
    assert hi < 1.0, "CI must exclude the Chahine value for the finding to hold"
    assert res["meets_rule"] is False


def test_free_intercept_model_has_a_positive_baseline(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = meta.chahine_mixedlm(df, through_origin=False)
    # Low-area carbons still adsorb a baseline amount: the relationship is not
    # perfectly proportional.
    assert res["intercept_wt_pct"] > 0.3


def test_shortfall_survives_tier_restriction(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ts = meta.tier_sensitivity(df)
    for label in ("all_tiers", "tier_AB", "tier_A"):
        assert ts[label]["mixedlm_wt_pct_per_500_m2"] < 1.0, label
    # Restricting to the best tiers does not push the slope toward the rule.
    assert ts["tier_A"]["mixedlm_wt_pct_per_500_m2"] < 0.9


def test_publication_bias_runs_and_reports(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result, funnel = meta.publication_bias(df)
    assert result["n_papers_in_test"] >= 15
    assert "egger_intercept_p" in result
    assert len(funnel) == result["n_papers_in_test"]


def test_descriptive_summary_counts(df):
    s = meta.descriptive_summary(df)
    assert s["dataset_rows"] == 521
    assert s["analysis_rows"] == 431
    assert s["material_classes"] == 13
