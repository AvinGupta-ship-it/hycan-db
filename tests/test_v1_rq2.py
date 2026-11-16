"""Tests for hycan.v1_rq2 (protocol §11, RQ2)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from hycan import v1_rq2

BASE = {
    "paper_id": "HYC-9001", "sample_id": "S1", "measurement_id": "M1",
    "temperature_k": 77.0, "pressure_bar": 1.0, "uptake_wt_pct": 1.0,
    "measurement_mode": "isothermal", "uptake_bound": "exact",
    "basis_stated": True, "basis_inferred": "excess",
    "wt_pct_convention": "W1", "value_kind": "measured",
    "isotherm_branch": "adsorption", "bet_surface_area_m2_g": 1000.0,
    "surface_area_method": "BET", "surface_area_probe_gas": "N2",
    "area_same_sample": "yes", "measuring_lab_id": "Lab A",
    "pressure_unstated": False, "temperature_unstated": False,
    "micropore_volume_cm3_g": 0.5, "pore_volume_method": "DR",
    "pore_volume_probe_gas": "N2", "micropore_volume_co2_cm3_g": None,
}


def row(mid, **kw):
    r = dict(BASE, measurement_id=mid)
    r.update(kw)
    return r


def test_rq2_rows_apply_the_window_and_filters():
    df = pd.DataFrame([
        row("M1"),                                      # in
        row("M2", pressure_bar=1.2),                    # in (inclusive)
        row("M3", pressure_bar=1.5),                    # outside the window
        row("M4", basis_inferred="total"),              # basis out
        row("M5", basis_inferred="unknown"),            # in: unknown allowed
        row("M6", value_kind="fitted_interpolated"),    # row filter
        row("M7", isotherm_branch="desorption"),        # row filter
        row("M8", bet_surface_area_m2_g=250.0),         # under the area floor
        row("M9", surface_area_method="Langmuir"),      # §11.0 area rule
        row("M10", temperature_k=87.0),                 # not 77 K
    ])
    out = v1_rq2.rq2_rows(df, {"HYC-9001"})
    assert sorted(out["measurement_id"]) == ["M1", "M2", "M5"]


def test_n2_vmicro_requires_method_and_probe_gas():
    df = pd.DataFrame([
        row("M1"),
        row("M2", sample_id="S2", pore_volume_probe_gas="CO2"),
        row("M3", sample_id="S3", pore_volume_method="unspecified"),
    ])
    out = v1_rq2.rq2_rows(df, {"HYC-9001"}).set_index("measurement_id")
    assert out.loc["M1", "vmicro_n2_cm3_g"] == 0.5
    assert pd.isna(out.loc["M2", "vmicro_n2_cm3_g"])
    assert pd.isna(out.loc["M3", "vmicro_n2_cm3_g"])


def test_rq2_samples_collapse_rows_then_laboratories():
    df = pd.DataFrame([
        row("M1", pressure_bar=0.9, uptake_wt_pct=1.0),
        row("M2", pressure_bar=1.1, uptake_wt_pct=2.0),
        # A second laboratory on the same sample -> multilab median.
        row("M3", measuring_lab_id="Lab B", uptake_wt_pct=3.0),
    ])
    out = v1_rq2.rq2_samples(df, {"HYC-9001"})
    assert len(out) == 1
    r = out.iloc[0]
    assert r["lab_id"] == "HYC-9001-multilab" and r["n_labs"] == 2
    assert r["n_rows"] == 3
    lab_a = float(np.sqrt(1.0 * 2.0))
    assert r["n_w1_wt_pct"] == pytest.approx(np.median([lab_a, 3.0]))
    assert r["pressure_bar"] == pytest.approx(
        np.median([np.sqrt(0.9 * 1.1), 1.0]))


def synthetic(n_labs=12, seed=7, b=1.0):
    rng = np.random.default_rng(seed)
    rows = []
    for li in range(n_labs):
        u = rng.normal(0, 0.05)
        for sk in range(4):
            area = float(rng.uniform(400, 3000))
            p = float(rng.uniform(0.9, 1.2))
            y = u + b * np.log(area / 1000) + 0.3 * np.log(p) + rng.normal(0, 0.05)
            rows.append({
                "paper_id": f"P{li}", "sample_id": f"S{sk}",
                "lab_id": f"L{li}", "n_rows": 1, "n_labs": 1,
                "n_w1_wt_pct": float(np.exp(y)), "pressure_bar": p,
                "a_bet_m2_g": area, "vmicro_n2_cm3_g": area / 2000.0,
                "vmicro_co2_cm3_g": None,
            })
    return pd.DataFrame(rows)


def test_fit_rq2_recovers_the_slope():
    r = v1_rq2.fit_rq2(synthetic(), n_boot=10)
    t = r["a_bet"]["terms"]["b_ln_a_bet"]
    assert t["ci95"][0] < 1.0 < t["ci95"][1]
    # V_micro here is proportional to area, so its slope matches.
    tv = r["b_vmicro_n2"]["terms"]["b_ln_vmicro"]
    assert abs(tv["estimate"] - t["estimate"]) < 1e-6
    assert r["b_vmicro_co2"] == {"skipped": "0 samples"}
    comp = r["comparison_same_samples"]
    assert comp["n_samples"] == 48
    assert set(comp["ml_aic"]) == {"a_bet", "b_vmicro_n2"}
    assert "ratio" in r["c_one_bar_ratio"]
