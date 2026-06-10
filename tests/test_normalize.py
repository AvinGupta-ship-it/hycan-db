"""Unit tests for src/hycan/normalize.py.

Coverage:
- each forward conversion against an independently known value;
- round-trip conversions (forward then inverse) recover the input to < 1e-9;
- negative pressures (and negative uptakes) raise ValueError.
"""

import math

import pytest

from hycan.normalize import (
    H2_MOLAR_MASS_G_PER_MOL,
    atm_to_bar,
    celsius_to_kelvin,
    kelvin_to_celsius,
    kpa_to_bar,
    mg_per_g_to_wt_pct,
    mmol_per_g_to_wt_pct,
    mpa_to_bar,
    psi_to_bar,
    torr_to_bar,
    wt_pct_to_mmol_per_g,
)

TOL = 1e-9


# ---------------------------------------------------------------------------
# Forward conversions vs. known values
# ---------------------------------------------------------------------------

def test_celsius_to_kelvin_known():
    # 0 °C is the ice point = 273.15 K; 25 °C (room temp) = 298.15 K.
    assert celsius_to_kelvin(0.0) == pytest.approx(273.15, abs=TOL)
    assert celsius_to_kelvin(25.0) == pytest.approx(298.15, abs=TOL)


def test_celsius_to_kelvin_negative_allowed():
    # Liquid-nitrogen-ish: -196 °C = 77.15 K. Negative °C must NOT raise.
    assert celsius_to_kelvin(-196.0) == pytest.approx(77.15, abs=TOL)
    assert celsius_to_kelvin(-273.15) == pytest.approx(0.0, abs=TOL)


def test_kelvin_to_celsius_known():
    assert kelvin_to_celsius(273.15) == pytest.approx(0.0, abs=TOL)
    assert kelvin_to_celsius(77.0) == pytest.approx(-196.15, abs=TOL)


def test_atm_to_bar_known():
    # NIST standard atmosphere: 1 atm = 1.01325 bar exactly.
    assert atm_to_bar(1.0) == pytest.approx(1.01325, abs=TOL)
    assert atm_to_bar(0.0) == pytest.approx(0.0, abs=TOL)


def test_mpa_to_bar_known():
    # 1 MPa = 10 bar; a common 10 MPa storage point = 100 bar.
    assert mpa_to_bar(1.0) == pytest.approx(10.0, abs=TOL)
    assert mpa_to_bar(10.0) == pytest.approx(100.0, abs=TOL)


def test_kpa_to_bar_known():
    # 1 kPa = 0.01 bar; 100 kPa = 1 bar.
    assert kpa_to_bar(100.0) == pytest.approx(1.0, abs=TOL)


def test_psi_to_bar_known():
    # NIST: 1 psi = 0.0689476 bar; atmospheric 14.6959 psi ≈ 1.01325 bar.
    assert psi_to_bar(1.0) == pytest.approx(0.0689476, abs=TOL)
    assert psi_to_bar(14.6959) == pytest.approx(1.013247, abs=1e-5)


def test_torr_to_bar_known():
    # 760 torr = 1 atm = 1.01325 bar; 1 torr = 0.00133322368... bar.
    assert torr_to_bar(760.0) == pytest.approx(1.01325, abs=TOL)
    assert torr_to_bar(1.0) == pytest.approx(0.0013332236842, abs=TOL)


def test_mmol_per_g_to_wt_pct_known():
    # 10 mmol/g of H2 = 10 * 2.01588 / 1000 g/g = 0.0201588 ratio = 2.01588 wt %.
    assert mmol_per_g_to_wt_pct(10.0) == pytest.approx(2.01588, abs=TOL)
    assert mmol_per_g_to_wt_pct(0.0) == pytest.approx(0.0, abs=TOL)


def test_mg_per_g_to_wt_pct_known():
    # 50 mg/g = 0.05 g/g = 5 wt %.
    assert mg_per_g_to_wt_pct(50.0) == pytest.approx(5.0, abs=TOL)
    assert mg_per_g_to_wt_pct(10.0) == pytest.approx(1.0, abs=TOL)


def test_wt_pct_to_mmol_per_g_known():
    # Inverse of the mmol case: 2.01588 wt % should give back 10 mmol/g.
    assert wt_pct_to_mmol_per_g(2.01588) == pytest.approx(10.0, abs=TOL)


# ---------------------------------------------------------------------------
# Round-trips (forward then inverse recovers the input within 1e-9)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("c", [-273.15, -40.0, 0.0, 25.0, 1000.0])
def test_temperature_roundtrip(c):
    assert kelvin_to_celsius(celsius_to_kelvin(c)) == pytest.approx(c, abs=TOL)


@pytest.mark.parametrize("mmol", [0.0, 0.5, 7.3, 42.0])
def test_uptake_mmol_wtpct_roundtrip(mmol):
    wt = mmol_per_g_to_wt_pct(mmol)
    assert wt_pct_to_mmol_per_g(wt) == pytest.approx(mmol, abs=TOL)


def test_uptake_wtpct_mmol_roundtrip():
    # Round-trip the other direction: wt % -> mmol/g -> wt %.
    for wt in (0.0, 0.8, 5.5, 12.0):
        mmol = wt_pct_to_mmol_per_g(wt)
        assert mmol_per_g_to_wt_pct(mmol) == pytest.approx(wt, abs=TOL)


# ---------------------------------------------------------------------------
# Negative-input guards
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "func",
    [atm_to_bar, mpa_to_bar, kpa_to_bar, psi_to_bar, torr_to_bar],
)
def test_negative_pressure_raises(func):
    with pytest.raises(ValueError):
        func(-1.0)


@pytest.mark.parametrize(
    "func",
    [mmol_per_g_to_wt_pct, mg_per_g_to_wt_pct, wt_pct_to_mmol_per_g],
)
def test_negative_uptake_raises(func):
    with pytest.raises(ValueError):
        func(-0.001)


def test_negative_temperature_does_not_raise():
    # Sanity guard against accidentally adding a negativity check to temperature.
    assert math.isfinite(celsius_to_kelvin(-200.0))
    assert math.isfinite(kelvin_to_celsius(-5.0))


def test_h2_molar_mass_constant():
    # The conversion depends on this exact value per the project spec.
    assert H2_MOLAR_MASS_G_PER_MOL == 2.01588
