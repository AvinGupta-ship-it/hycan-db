"""Tests for the canonical analysis filter, src/hycan/load.py (manual §12.3).

These assert two things: the filter's *properties* (every surviving row is an
isothermal, exact, fully-conditioned uptake measurement, and nothing excluded
is), which are robust to future appends; and the current *counts*, pinned as a
regression guard in the style of test_dataset_invariants.py. A count that moves
on an append is updated deliberately, in the same commit, after confirming the
property assertions still hold.
"""

from __future__ import annotations

import pandas as pd

from hycan.load import (
    DEFAULT_DATASET,
    _has_any_uptake,
    _is_true,
    analysis_subset,
    confirmed_bet_area,
    load_dataset,
)

# Pinned against the 521-row corpus (2026-10-06). MUTATION: drop a filter from
# analysis_subset -> one of these counts rises and the test fails.
N_DATASET = 521
N_ANALYSIS_SUBSET = 431
N_ANALYSIS_PAPERS = 45
N_WITH_WT_PCT = 419


def _df() -> pd.DataFrame:
    return load_dataset(DEFAULT_DATASET)


def test_load_dataset_reads_the_full_corpus():
    df = _df()
    assert len(df) == N_DATASET
    # keep_default_na=False must NOT have been passed: an untouched optional
    # column must contain real NaNs, not the literal empty string.
    assert df["verified_by"].isna().any()


def test_analysis_subset_counts_are_pinned():
    sub = analysis_subset(_df())
    assert len(sub) == N_ANALYSIS_SUBSET
    assert sub["paper_id"].nunique() == N_ANALYSIS_PAPERS


def test_analysis_subset_only_keeps_conditioned_isothermal_exact_uptake_rows():
    """The property behind the count: every surviving row satisfies all four
    §12.3 conditions. Robust to appends in a way the raw count is not."""
    sub = analysis_subset(_df())
    assert (sub["measurement_mode"].fillna("isothermal") == "isothermal").all()
    assert (sub["uptake_bound"].fillna("exact") == "exact").all()
    assert not _is_true(sub["temperature_unstated"]).any()
    assert not _is_true(sub["pressure_unstated"]).any()
    assert _has_any_uptake(sub).all()


def test_every_excluded_row_fails_at_least_one_filter():
    """The complement property: no row is dropped that satisfies all four
    conditions -- i.e. the filter excludes nothing it should keep."""
    df = _df()
    kept_ids = set(analysis_subset(df)["measurement_id"])
    excluded = df[~df["measurement_id"].isin(kept_ids)]
    mode = excluded["measurement_mode"].fillna("isothermal")
    bound = excluded["uptake_bound"].fillna("exact")
    fails = (
        (mode != "isothermal")
        | (bound != "exact")
        | _is_true(excluded["temperature_unstated"])
        | _is_true(excluded["pressure_unstated"])
        | ~_has_any_uptake(excluded)
    )
    assert fails.all()


def test_require_wt_pct_drops_only_rows_without_the_target():
    df = _df()
    full = analysis_subset(df)
    wt = analysis_subset(df, require_wt_pct=True)
    assert len(wt) == N_WITH_WT_PCT
    assert wt["uptake_wt_pct"].notna().all()
    # It is a strict subset, and the only difference is the target column.
    assert set(wt["measurement_id"]) <= set(full["measurement_id"])
    dropped = full[~full["measurement_id"].isin(wt["measurement_id"])]
    assert dropped["uptake_wt_pct"].isna().all()


def test_analysis_subset_is_idempotent():
    df = _df()
    once = analysis_subset(df)
    twice = analysis_subset(once)
    assert list(once["measurement_id"]) == list(twice["measurement_id"])


def test_confirmed_bet_area_masks_non_bet_methods():
    df = _df()
    area = confirmed_bet_area(df)
    # Where a BET area is returned, the method is BET; where the method is not
    # BET, the area is NaN even if bet_surface_area_m2_g is populated.
    non_bet = df["surface_area_method"] != "BET"
    assert area[non_bet].isna().all()
    bet_rows = df["surface_area_method"] == "BET"
    assert (area[bet_rows].notna() == df.loc[bet_rows, "bet_surface_area_m2_g"].notna()).all()
