"""Tests for hycan.v1_sets and hycan.v1_rq1 (protocol §11.0, RQ1)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from hycan import v1_rq1, v1_sets

BASE = {
    "paper_id": "HYC-9001", "doi": "10.1/x", "sample_id": "S1",
    "material_description": "AC-1 | x", "material_class": "activated_carbon",
    "measurement_id": "HYC-9001-M1", "temperature_k": 77.0,
    "pressure_bar": 20.0, "uptake_wt_pct": 2.0, "uptake_type": "excess",
    "measurement_method": "volumetric", "extraction_method": "table_direct",
    "measurement_mode": "isothermal", "uptake_bound": "exact",
    "basis_stated": True, "basis_inferred": "excess", "wt_pct_convention": "W1",
    "value_kind": "measured", "isotherm_id": "I1",
    "isotherm_branch": "adsorption", "bet_surface_area_m2_g": 1000.0,
    "surface_area_method": "BET", "surface_area_probe_gas": "N2",
    "area_same_sample": "yes", "measuring_lab_id": "Lab A",
    "pressure_unstated": False, "temperature_unstated": False,
    "duplicate_of": None, "notes": "",
}


def point(mid, p, wt, **kw):
    r = dict(BASE, measurement_id=mid, pressure_bar=p, uptake_wt_pct=wt)
    r.update(kw)
    return r


def isotherm(pid, sid, iso, lab, pts, area=1000.0, **kw):
    return [
        point(f"{pid}-{iso}-M{i}", p, wt, paper_id=pid, sample_id=sid,
              isotherm_id=iso, measuring_lab_id=lab,
              bet_surface_area_m2_g=area,
              material_description=f"{sid} | x", **kw)
        for i, (p, wt) in enumerate(pts, 1)
    ]


OBSERVED_MAX = [(1, 1.0), (10, 2.0), (30, 2.5), (50, 2.2)]


def test_rq1_samples_takes_geometric_mean_then_multilab_median():
    rows = (
        isotherm("HYC-9001", "S1", "I1", "Lab A", OBSERVED_MAX)
        + isotherm("HYC-9001", "S1", "I2", "Lab A",
                   [(1, 1.1), (10, 2.1), (30, 3.6), (50, 3.2)])
        # A second laboratory measures the same sample: multilab median.
        + isotherm("HYC-9001", "S1", "I3", "Lab B",
                   [(1, 1.0), (10, 2.0), (30, 4.0), (50, 3.5)])
        # Below the area floor: out of the primary set.
        + isotherm("HYC-9002", "S1", "I1", "Lab C", OBSERVED_MAX, area=200.0,
                   basis_stated=False)
        # lower_bound isotherm: out of the primary set.
        + isotherm("HYC-9003", "S1", "I1", "Lab D",
                   [(1, 1.0), (10, 2.0), (40, 3.0)])
    )
    df = pd.DataFrame(rows)
    out = v1_sets.rq1_samples(df, {"HYC-9001", "HYC-9002", "HYC-9003"})
    assert len(out) == 1
    r = out.iloc[0]
    assert r["lab_id"] == "HYC-9001-multilab" and r["n_labs"] == 2
    assert r["n_isotherms"] == 3
    # Lab A: gmean(2.5, 3.6); Lab B: 4.0; the sample enters at their median.
    lab_a = float(np.sqrt(2.5 * 3.6))
    assert r["n_ex_max_w1_wt_pct"] == pytest.approx(np.median([lab_a, 4.0]))


def test_eligible_isotherms_excludes_unmeasured_value_kinds():
    rows = isotherm("HYC-9001", "S1", "I1", "Lab A", OBSERVED_MAX)
    rows[1]["value_kind"] = "fitted_interpolated"
    df = pd.DataFrame(rows)
    assert v1_sets.eligible_isotherms(df, {"HYC-9001"}).empty
    relaxed = v1_sets.eligible_isotherms(
        df, {"HYC-9001"}, value_kinds=("measured", "fitted_interpolated"))
    assert len(relaxed) == 1


def synthetic_samples(n_labs=14, seed=3):
    rng = np.random.default_rng(seed)
    rows = []
    for li in range(n_labs):
        u = rng.normal(0, 0.1)
        for sk in range(3):
            area = float(rng.uniform(400, 3000))
            y = u + rng.normal(0, 0.1)
            rows.append({"paper_id": f"P{li}", "sample_id": f"S{sk}",
                         "lab_id": f"L{li}", "n_isotherms": 1, "n_labs": 1,
                         "n_ex_max_w1_wt_pct": float(np.exp(y) * area / 500),
                         "a_bet_m2_g": area})
    return pd.DataFrame(rows)


def test_fit_primary_recovers_a_unit_ratio():
    r = v1_rq1.fit_primary(synthetic_samples(), n_boot=25)
    assert r["n_labs"] == 14
    assert 0.9 < r["ratio"] < 1.1
    assert r["ci95_decision"][0] <= r["ratio"] <= r["ci95_decision"][1]
    assert r["ci95_decision"][0] <= r["ci95_t"][0] or \
           r["ci95_decision"][1] >= r["ci95_t"][1]
    lo, hi = r["prediction_interval_95"]
    assert lo < r["ci95_t"][0] and hi > r["ci95_t"][1]
    assert r["bootstrap_resamples"] + r["bootstrap_failures"] == 25


def test_decision_categories():
    assert v1_rq1.decision(0.9, 1.1) == "supported"
    assert v1_rq1.decision(0.5, 0.7) == "overstates"
    assert v1_rq1.decision(1.2, 1.4) == "understates"
    assert v1_rq1.decision(0.8, 1.2) == "inconclusive"


def test_fit_secondary_slope_near_one():
    r = v1_rq1.fit_secondary(synthetic_samples(seed=5))
    assert r["ci95"][0] < 1.0 < r["ci95"][1]
    assert r["b_corrected_20pct"] > r["b_corrected_10pct"] > r["b"] > 0
