"""Tests for hycan.v1_rq5 (protocol §11, RQ5)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from hycan import v1_rq5

BASE = {
    "paper_id": "HYC-9001", "sample_id": "S1", "measurement_id": "M1",
    "temperature_k": 77.0, "pressure_bar": 10.0, "uptake_wt_pct": 2.0,
    "measurement_mode": "isothermal", "uptake_bound": "exact",
    "basis_stated": True, "basis_inferred": "excess",
    "wt_pct_convention": "W1", "value_kind": "measured", "isotherm_id": "I1",
    "isotherm_branch": "adsorption", "bet_surface_area_m2_g": 1000.0,
    "surface_area_method": "BET", "surface_area_probe_gas": "N2",
    "area_same_sample": "yes", "measuring_lab_id": "Lab A",
    "pressure_unstated": False, "temperature_unstated": False,
    "material_class": "activated_carbon",
    "measurement_method": "volumetric_sieverts",
    "total_pore_volume_cm3_g": 0.8, "micropore_volume_cm3_g": 0.4,
    "dopant_element": None, "metal_element": None, "year": 2015,
}


def iso(pid, iso_id, pts, **kw):
    return [
        dict(BASE, paper_id=pid, isotherm_id=iso_id,
             measurement_id=f"{pid}-{iso_id}-M{i}", pressure_bar=p,
             uptake_wt_pct=wt, **kw)
        for i, (p, wt) in enumerate(pts, 1)
    ]


def test_rq5_rows_filters():
    rows = (
        iso("HYC-9001", "I1", [(1, 1.0), (10, 2.0), (120, 2.6), (50, 2.5)])
        # Still rising steeply at 80 bar and unstated: basis_shape_conflict.
        + iso("HYC-9002", "I1", [(1, 0.5), (40, 2.0), (80, 3.9)],
              basis_stated=False)
    )
    df = pd.DataFrame(rows)
    out = v1_rq5.rq5_rows(df, {"HYC-9001", "HYC-9002"})
    # 120 bar excluded by P <= 100; the conflicted isotherm wholly excluded.
    assert sorted(out["measurement_id"]) == [
        "HYC-9001-I1-M1", "HYC-9001-I1-M2", "HYC-9001-I1-M4"]


def test_feature_matrix_merges_small_classes():
    rows = pd.DataFrame([
        {"paper_id": f"P{i}", "lab_id": "L", "a_bet_m2_g": 1000.0,
         "pressure_bar": 1.0, "n_w1_wt_pct": 1.0,
         "material_class": "activated_carbon" if i < 5 else "SWCNT",
         "method": "volumetric_sieverts", "v_total_cm3_g": None,
         "v_micro_cm3_g": None, "dopant_present": False,
         "metal_present": False, "year": 2015.0}
        for i in range(6)
    ])
    x = v1_rq5.feature_matrix(rows)
    assert "class_activated_carbon" in x and "class_other" in x
    assert "class_SWCNT" not in x
    assert x["class_other"].sum() == 1.0


def synthetic_rows(n_papers=12, seed=11):
    rng = np.random.default_rng(seed)
    out = []
    for pi in range(n_papers):
        area = float(rng.uniform(500, 3000))
        for i in range(30):
            p = float(rng.uniform(0.5, 90))
            n = area / 500.0 * p / (p + 5.0) + rng.normal(0, 0.05)
            out.append({
                "paper_id": f"P{pi}", "lab_id": f"L{pi % 6}",
                "a_bet_m2_g": area, "pressure_bar": p, "n_w1_wt_pct": n,
                "material_class": "activated_carbon",
                "method": "volumetric_sieverts", "v_total_cm3_g": 0.9,
                "v_micro_cm3_g": 0.4, "dopant_present": False,
                "metal_present": False, "year": 2015.0,
            })
    return pd.DataFrame(out)


def test_oof_predictions_and_scores_recover_a_langmuir_world():
    rows = synthetic_rows()
    x = v1_rq5.feature_matrix(rows)
    oof = v1_rq5.oof_predictions(rows, x, groups="paper_id", random_state=0,
                                 weighted=False)
    assert not oof[["physical", "linear", "xgboost"]].isna().any().any()
    s = v1_rq5.score(oof)
    assert s["physical"]["overall"]["r2"] > 0.98  # the generating model
    assert s["physical"]["overall"]["mae"] < 0.1
    for reg in ("le_1p2_bar", "ge_10_bar"):
        assert s["physical"][reg]["n"] < s["physical"]["overall"]["n"]
    boot = v1_rq5.paper_bootstrap(oof, n_boot=20)
    lo, hi = boot["physical"]["overall"]["r2_ci95"]
    assert lo <= s["physical"]["overall"]["r2"] <= hi or lo > 0.9


def test_weighted_scoring_uses_the_weights():
    rows = synthetic_rows(n_papers=6)
    x = v1_rq5.feature_matrix(rows)
    oof = v1_rq5.oof_predictions(rows, x, groups="paper_id", random_state=1,
                                 weighted=True)
    assert "w" in oof
    assert oof.groupby("paper_id")["w"].first().mul(
        oof.groupby("paper_id").size()).round(9).eq(1.0).all()
    s = v1_rq5.score(oof, weighted=True)
    assert np.isfinite(s["linear"]["overall"]["r2"])


def test_summarize_percentiles():
    parts = [
        {m: {r: {"r2": v, "mae": v / 10, "n": 5}
             for r in ("overall", "le_1p2_bar", "ge_10_bar")}
         for m in ("physical", "linear", "xgboost")}
        for v in (0.1, 0.2, 0.3)
    ]
    out = v1_rq5.summarize(parts)
    assert out["linear"]["overall"]["r2"]["mean"] == pytest.approx(0.2)
    assert out["linear"]["overall"]["n"] == 5
