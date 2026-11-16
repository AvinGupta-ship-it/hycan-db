"""Tests for hycan.v1_rq4 (protocol §11, RQ4)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from hycan import v1_rq4

ROW = {
    "paper_id": "P1", "year": 2018, "basis_stated": True,
    "wt_pct_convention_source": "stated", "replicates_reported": False,
    "uncertainty_wt_pct": 0.1, "instrument_identified": True,
    "calibration_described": True, "temperature_inferred": False,
    "temperature_unstated": False, "pressure_unstated": False,
    "bet_range_stated": True, "bet_consistency_criteria_stated": False,
    "sample_mass_mg": 100.0, "degas_temperature_c": 300.0,
    "degas_duration_h": 12.0, "degas_end_pressure_pa": None,
    "plausibility_flag": False, "h2_purity_pct": 99.999,
    "measurement_method": "volumetric_sieverts",
    "free_volume_calibration": "He at 303 K",
    "surface_area_method": "BET", "surface_area_probe_gas": "N2",
    "total_pore_volume_cm3_g": 0.5, "micropore_volume_cm3_g": None,
    "micropore_volume_co2_cm3_g": None, "pore_volume_method": "t_plot",
    "isotherm_point_count": 8.0,
}


def test_paper_items_a_through_j():
    rows = [dict(ROW), dict(ROW, paper_id="P2", basis_stated=False,
                            wt_pct_convention_source="computed_from_other_unit",
                            plausibility_flag=None,
                            measurement_method="gravimetric_microbalance",
                            free_volume_calibration=None)]
    out = v1_rq4.paper_items(pd.DataFrame(rows), {"P1", "P2"})
    out = out.set_index("paper_id")
    p1, p2 = out.loc["P1"], out.loc["P2"]
    assert all(p1[i] is True or p1[i] == 1.0 for i in "acdefghij" if i != "h")
    assert p1["h"] is False or p1["h"] == 0.0  # screenable, unflagged
    assert p2["a"] is False or p2["a"] == 0.0
    assert p2["b"] is None and p2["h"] is None and p2["j"] is None


def test_fv_gas_and_temp_rule():
    ok = v1_rq4._fv_gas_and_temp
    assert ok("He at 303 K")
    assert ok("helium, room temperature")
    assert not ok("helium; temperature not stated")
    assert not ok("calibrated with a reference volume at 298 K")  # no gas
    assert not ok(None)


def test_ratio_estimate_matches_a_hand_computation():
    # S1: N=10, d=4 taken, 2 eligible (one yes); S2: N=100, d=5, 1 eligible (no).
    frame = pd.DataFrame([
        {"paper_id": "A", "year": 2010, "a": True},
        {"paper_id": "B", "year": 2010, "a": False},
        {"paper_id": "C", "year": 2020, "a": False},
    ])
    strata = {"A": "S1", "B": "S1", "C": "S2"}
    counts = {"S1": {"N": 10, "d": 4}, "S2": {"N": 100, "d": 5}}
    r = v1_rq4.ratio_estimate(frame, strata, counts, "a")
    w1, w2 = 10 / 4, 100 / 5
    p = (w1 * 1) / (w1 * 2 + w2 * 1)
    assert r["p_hat"] == pytest.approx(p)
    u1 = np.array([1 - p, -p, 0, 0])          # S1's four taken records
    u2 = np.array([-p, 0, 0, 0, 0])           # S2's five
    var = (10**2 * (1 - 4 / 10) * np.var(u1, ddof=1) / 4
           + 100**2 * (1 - 5 / 100) * np.var(u2, ddof=1) / 5) / (w1 * 2 + w2) ** 2
    assert r["se"] == pytest.approx(np.sqrt(var))
    assert r["ci_method"] == "korn_graubard"
    assert r["ci95"][0] < p < r["ci95"][1]


def test_ratio_estimate_degenerate_cases_use_clopper_pearson():
    frame = pd.DataFrame([
        {"paper_id": "A", "year": 2010, "a": True},
        {"paper_id": "B", "year": 2010, "a": True},
    ])
    strata = {"A": "S1", "B": "S1"}
    counts = {"S1": {"N": 10, "d": 4}}
    r = v1_rq4.ratio_estimate(frame, strata, counts, "a")
    assert r["p_hat"] == 1.0 and r["ci_method"] == "clopper_pearson_unweighted"
    assert r["ci95"][1] == 1.0 and 0 < r["ci95"][0] < 1

    none = v1_rq4.ratio_estimate(frame.assign(a=None), strata, counts, "a")
    assert none == {"n_domain": 0, "n_yes": 0}


def test_fit_rq4_splits_periods():
    frame = pd.DataFrame([
        {"paper_id": p, "year": y, **{i: (p == "A") for i in v1_rq4.ITEMS}}
        for p, y in (("A", 2010), ("B", 2020))
    ])
    strata = {"A": "S1", "B": "S1"}
    counts = {"S1": {"N": 10, "d": 4}}
    out = v1_rq4.fit_rq4(frame, strata, counts)
    assert out["a"]["by_period"]["le_2015"]["p_hat"] == 1.0
    assert out["a"]["by_period"]["ge_2016"]["p_hat"] == 0.0
