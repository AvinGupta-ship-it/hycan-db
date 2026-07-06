"""
Pure unit-conversion functions for normalising HyCAN-DB measurements.

Every paper reports temperature, pressure and hydrogen uptake in whatever units
the authors preferred (°C, atm, MPa, kPa, psi, torr; mmol/g, mg/g, wt %). The
curation pipeline stores everything in a single canonical set of units — kelvin
for temperature, bar for pressure, and weight-percent (or mmol/g) for uptake —
so these helpers exist to convert raw values into the canonical form.

Design rules:
- Every function is pure: no I/O, no globals mutated, output depends only on input.
- Pressure / uptake conversions raise ``ValueError`` on negative input, because a
  negative pressure or a negative amount adsorbed is physically meaningless and
  almost always signals a data-entry error upstream.
- Temperature conversions accept negatives, since Celsius (and Fahrenheit) can be
  legitimately below zero.

Conversion-factor sources:
- Temperature offset 273.15 K: SI definition of the Celsius scale (BIPM SI Brochure,
  9th ed., 2019).
- 1 atm = 1.01325 bar exactly: NIST standard atmosphere
  (NIST Guide to the SI, App. B.8; 1 atm = 101 325 Pa, 1 bar = 100 000 Pa).
- 1 MPa = 10 bar, 1 kPa = 0.01 bar: exact, from 1 bar = 100 000 Pa.
- 1 psi = 0.0689476 bar: NIST (1 psi = 6894.757 Pa; NIST SP 811, App. B.9).
- 1 torr = 1 atm / 760 = 0.00133322368 bar: NIST (1 torr = 101 325 / 760 Pa).
- H2 molar mass 2.01588 g/mol: from the 2021 IUPAC standard atomic weight of
  hydrogen (2 × 1.00794), as specified by the project.
"""

from __future__ import annotations

# Molar mass of molecular hydrogen, g/mol (2 × IUPAC standard atomic weight of H).
H2_MOLAR_MASS_G_PER_MOL = 2.01588

# Exact / NIST pressure conversion factors, expressed as (1 unit) in bar.
_ATM_TO_BAR = 1.01325          # NIST standard atmosphere, exact
_MPA_TO_BAR = 10.0             # 1 MPa = 100 000 Pa = 10 bar, exact
_KPA_TO_BAR = 0.01             # 1 kPa = 100 Pa = 0.01 bar, exact
_PSI_TO_BAR = 0.0689476        # NIST, 1 psi = 6894.757 Pa
_TORR_TO_BAR = 101325.0 / 760.0 / 100000.0  # 1 torr = atm/760, in bar


def _reject_negative(value: float, name: str) -> None:
    """Raise ``ValueError`` if ``value`` is negative (used by pressure/uptake)."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value!r}.")


# ---------------------------------------------------------------------------
# Temperature
# ---------------------------------------------------------------------------

def celsius_to_kelvin(c: float) -> float:
    """Convert a temperature from degrees Celsius to kelvin.

    Uses the SI Celsius-scale definition ``K = °C + 273.15`` (BIPM SI Brochure,
    9th ed., 2019). Negative Celsius values are valid and accepted.
    """
    return c + 273.15


def kelvin_to_celsius(k: float) -> float:
    """Convert a temperature from kelvin to degrees Celsius.

    Inverse of :func:`celsius_to_kelvin`: ``°C = K - 273.15`` (BIPM SI Brochure,
    9th ed., 2019).
    """
    return k - 273.15


# ---------------------------------------------------------------------------
# Pressure  (canonical unit: bar)
# ---------------------------------------------------------------------------

def atm_to_bar(p: float) -> float:
    """Convert pressure from standard atmospheres to bar.

    Factor: 1 atm = 1.01325 bar exactly (NIST standard atmosphere; 1 atm =
    101 325 Pa, 1 bar = 100 000 Pa). Raises ``ValueError`` for negative input.
    """
    _reject_negative(p, "pressure (atm)")
    return p * _ATM_TO_BAR


def mpa_to_bar(p: float) -> float:
    """Convert pressure from megapascals to bar.

    Factor: 1 MPa = 10 bar exactly (1 MPa = 1 000 000 Pa, 1 bar = 100 000 Pa).
    Raises ``ValueError`` for negative input.
    """
    _reject_negative(p, "pressure (MPa)")
    return p * _MPA_TO_BAR


def kpa_to_bar(p: float) -> float:
    """Convert pressure from kilopascals to bar.

    Factor: 1 kPa = 0.01 bar exactly (1 kPa = 1000 Pa, 1 bar = 100 000 Pa).
    Raises ``ValueError`` for negative input.
    """
    _reject_negative(p, "pressure (kPa)")
    return p * _KPA_TO_BAR


def psi_to_bar(p: float) -> float:
    """Convert pressure from pounds per square inch to bar.

    Factor: 1 psi = 0.0689476 bar (NIST SP 811, App. B.9; 1 psi = 6894.757 Pa).
    Raises ``ValueError`` for negative input.
    """
    _reject_negative(p, "pressure (psi)")
    return p * _PSI_TO_BAR


def torr_to_bar(p: float) -> float:
    """Convert pressure from torr (mmHg) to bar.

    Factor: 1 torr = 1 atm / 760 = 0.00133322368... bar (NIST; 1 torr =
    101 325 / 760 Pa). Raises ``ValueError`` for negative input.
    """
    _reject_negative(p, "pressure (torr)")
    return p * _TORR_TO_BAR


# ---------------------------------------------------------------------------
# Uptake  (canonical unit: weight-percent, relative to dry sorbent mass)
# ---------------------------------------------------------------------------
#
# Convention: wt % is expressed relative to the host (sorbent) mass,
#     wt % = (mass H2 / mass sorbent) × 100,
# which is the form most commonly tabulated in the carbon-adsorption literature
# and which keeps the mmol/g <-> wt % conversion linear (and round-trippable).

def mmol_per_g_to_wt_pct(x: float) -> float:
    """Convert hydrogen uptake from mmol H2 per gram of sorbent to weight-percent.

    ``wt % = x [mmol/g] × M(H2) [g/mol] / 1000 [mmol/mol] × 100`` with
    M(H2) = 2.01588 g/mol (IUPAC 2021 standard atomic weight of H). Raises
    ``ValueError`` for negative input.
    """
    _reject_negative(x, "uptake (mmol/g)")
    return x * H2_MOLAR_MASS_G_PER_MOL / 10.0


def mg_per_g_to_wt_pct(x: float) -> float:
    """Convert hydrogen uptake from mg H2 per gram of sorbent to weight-percent.

    ``wt % = x [mg/g] / 1000 [mg/g per unit ratio] × 100 = x / 10`` (pure unit
    arithmetic, no physical constant required). Raises ``ValueError`` for
    negative input.
    """
    _reject_negative(x, "uptake (mg/g)")
    return x / 10.0


def wt_pct_to_mmol_per_g(x: float) -> float:
    """Convert hydrogen uptake from weight-percent to mmol H2 per gram of sorbent.

    Inverse of :func:`mmol_per_g_to_wt_pct`:
    ``mmol/g = x [wt %] × 10 / M(H2)`` with M(H2) = 2.01588 g/mol (IUPAC 2021).
    Raises ``ValueError`` for negative input.
    """
    _reject_negative(x, "uptake (wt %)")
    return x * 10.0 / H2_MOLAR_MASS_G_PER_MOL


# ---------------------------------------------------------------------------
# Uptake reported as a gas volume at STP  (ml(STP)/g)
# ---------------------------------------------------------------------------
#
# Some papers report uptake as a volume of gas at "STP" per gram of sorbent.
# Converting to an amount of substance needs the molar volume of an ideal gas.
# HyCAN-DB fixes STP at 273.15 K and 1 atm (101.325 kPa), for which the ideal-gas
# molar volume is Vm = 22.414 L/mol = 22.414 mL/mmol (the Day-9 convention used
# throughout the project). We deliberately do NOT use 22.711 L/mol (0 °C, 1 bar)
# or 24.465 L/mol (25 °C, 1 atm) so that ml(STP)/g <-> mmol/g <-> wt% stays a
# single self-consistent chain.

# Ideal-gas molar volume at STP (273.15 K, 1 atm), L/mol = mL/mmol.
STP_MOLAR_VOLUME_ML_PER_MMOL = 22.414


def ml_stp_per_g_to_mmol_per_g(x: float) -> float:
    """Convert hydrogen uptake from mL(STP)/g to mmol H2 per gram of sorbent.

    Divides the reported gas volume by the ideal-gas molar volume at STP:
    ``mmol/g = x [mL(STP)/g] / Vm`` with Vm = 22.414 L/mol (= 22.414 mL/mmol)
    at 273.15 K and 1 atm (101.325 kPa) — the STP convention used throughout
    HyCAN-DB (Day-9). This is the physical definition of the ideal-gas molar
    volume at 273.15 K, 1 atm, not a source-specific citation. Raises
    ``ValueError`` for negative input.
    """
    _reject_negative(x, "uptake (mL(STP)/g)")
    return x / STP_MOLAR_VOLUME_ML_PER_MMOL


def ml_stp_per_g_to_wt_pct(x: float) -> float:
    """Convert hydrogen uptake from mL(STP)/g to weight-percent.

    Chains the mL(STP)/g -> mmol/g step (divide by the ideal-gas molar volume at
    STP, Vm = 22.414 L/mol = 22.414 mL/mmol at 273.15 K and 1 atm / 101.325 kPa,
    the HyCAN-DB Day-9 convention) with the existing mmol/g -> wt% factor
    (M(H2) = 2.01588 g/mol):
    ``wt % = (x / 22.414) × 0.201588`` where 0.201588 = M(H2) / 10. This matches
    this module's existing mmol/g <-> wt% convention. The molar volume is the
    physical ideal-gas value at 273.15 K, 1 atm, not a source-specific citation.
    Raises ``ValueError`` for negative input.
    """
    _reject_negative(x, "uptake (mL(STP)/g)")
    return (x / STP_MOLAR_VOLUME_ML_PER_MMOL) * (H2_MOLAR_MASS_G_PER_MOL / 10.0)
