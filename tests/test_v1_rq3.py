"""Tests for hycan.v1_rq3 (protocol §11, RQ3)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from hycan import v1_rq3

BASE = {
    "paper_id": "HYC-9001", "sample_id": "S1", "measurement_id": "M1",
    "material_identity": "Maker; P1", "temperature_k": 77.0,
    "pressure_bar": 1.0, "uptake_wt_pct": 1.0,
    "measurement_mode": "isothermal", "uptake_bound": "exact",
    "basis_stated": True, "basis_inferred": "excess",
    "wt_pct_convention": "W1", "value_kind": "measured",
    "isotherm_id": None, "isotherm_branch": "adsorption",
    "bet_surface_area_m2_g": 1000.0, "surface_area_method": "BET",
    "surface_area_probe_gas": "N2", "area_same_sample": "yes",
    "measuring_lab_id": "Lab A", "pressure_unstated": False,
    "temperature_unstated": False, "duplicate_of": None,
    "micropore_volume_cm3_g": None, "pore_volume_method": None,
    "pore_volume_probe_gas": None, "micropore_volume_co2_cm3_g": None,
}

KEYS = {"Maker; P1": "maker-p1", "Maker, P1 (grade not printed)": "maker-p1"}


def row(mid, **kw):
    r = dict(BASE, measurement_id=mid)
    r.update(kw)
    return r


def test_rq3_values_group_through_the_map_and_refuse_unmapped():
    df = pd.DataFrame([
        row("M1", uptake_wt_pct=1.0),
        row("M2", paper_id="HYC-9002", sample_id="S1", measuring_lab_id="Lab B",
            material_identity="Maker, P1 (grade not printed)",
            bet_surface_area_m2_g=1200.0, uptake_wt_pct=1.2),
    ])
    out = v1_rq3.rq3_values(df, {"HYC-9001", "HYC-9002"}, KEYS)
    one_bar = out[out["quantity"] == "n_1bar"]
    assert set(one_bar["lab_id"]) == {"Lab A", "Lab B"}
    assert set(out["material_key"]) == {"maker-p1"}
    with pytest.raises(ValueError, match="missing from the map"):
        v1_rq3.rq3_values(df, {"HYC-9001", "HYC-9002"}, {})


def test_a_shared_area_within_a_paper_counts_once():
    df = pd.DataFrame([
        row("M1", measuring_lab_id="Lab A"),
        row("M2", measuring_lab_id="Lab B"),
        row("M3", paper_id="HYC-9002", measuring_lab_id="Lab C",
            bet_surface_area_m2_g=1000.0),
    ])
    out = v1_rq3.rq3_values(df, {"HYC-9001", "HYC-9002"},
                            {"Maker; P1": "maker-p1"})
    areas = out[out["quantity"] == "a_bet"]
    assert sorted(areas["lab_id"]) == ["HYC-9001-shared", "Lab C"]


def test_fit_rq3_cv_and_pooling():
    vals = pd.DataFrame([
        {"material_key": "m1", "quantity": "a_bet", "lab_id": f"L{i}",
         "n_values": 1, "value": v}
        for i, v in enumerate([900.0, 1000.0, 1100.0])
    ] + [
        {"material_key": "m2", "quantity": "a_bet", "lab_id": f"K{i}",
         "n_values": 1, "value": v}
        for i, v in enumerate([400.0, 500.0])
    ] + [
        {"material_key": "m3", "quantity": "ratio", "lab_id": "L0",
         "n_values": 1, "value": 1.0}  # one laboratory: no CV
    ])
    r = v1_rq3.fit_rq3(vals)
    m1 = r["materials"]["m1"]["a_bet"]
    y = np.log([900.0, 1000.0, 1100.0])
    assert m1["n_labs"] == 3
    assert m1["cv_pct"] == pytest.approx(100 * np.std(y, ddof=1))
    assert m1["cv_ci95_pct"][0] < m1["cv_pct"] < m1["cv_ci95_pct"][1]
    assert "m3" not in r["materials"]
    pooled = r["pooled"]["a_bet"]
    y2 = np.log([400.0, 500.0])
    expect = np.sqrt((np.sum((y - y.mean()) ** 2)
                      + np.sum((y2 - y2.mean()) ** 2)) / 3)
    assert pooled["df"] == 3 and pooled["n_materials"] == 2
    assert pooled["cv_pct"] == pytest.approx(100 * expect)
    assert r["pooled"]["n_ex_max"] == {"skipped": "fewer than two laboratories"}


def test_sd_ci_brackets_the_estimate():
    lo, hi = v1_rq3.sd_ci(0.1, 5)
    assert lo < 0.1 < hi
