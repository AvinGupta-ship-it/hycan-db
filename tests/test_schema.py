"""Unit tests for src/hycan/schema.py."""

import pytest
from hycan.schema import MeasurementEntry, validate_row

# ---------------------------------------------------------------------------
# Shared fixture – a minimal valid row based on Panella et al. 2005
# (B. Panella, M. Hirscher, S. Roth, Carbon 2005, 43, 2209–2214)
# ---------------------------------------------------------------------------

PANELLA_2005 = {
    # Paper
    "paper_id": "HYC-0001",
    "doi": "10.1016/j.carbon.2005.03.037",
    "first_author": "Panella",
    "year": 2005,
    "journal": "Carbon",
    "title": "Hydrogen adsorption in different carbon nanostructures",
    # Sample – pristine SWCNT
    "sample_id": "HYC-0001-S1",
    "measurement_id": "HYC-0001-M1",
    "material_class": "SWCNT",
    "material_description": "Purified HiPco SWCNTs, BET SSA ~1000 m2/g",
    "synthesis_method": "hipco",
    # Characterisation
    "bet_surface_area_m2_g": 1000.0,
    # Measurement – 77 K, 1 bar (cryogenic volumetric isotherm)
    "temperature_k": 77.0,
    "pressure_bar": 1.0,
    "uptake_wt_pct": 1.5,
    "uptake_type": "excess",
    "measurement_method": "volumetric_sieverts",
    # Provenance
    "source_location": "Figure 1, extracted at P=1 bar",
    "extraction_method": "figure_digitized",
    "extraction_confidence": 3,
    "reproducibility_tier": "B",
    "extractor": "AG",
    "extraction_date": "2026-06-09",
}


def _patch(base: dict, **overrides) -> dict:
    """Return a copy of *base* with *overrides* applied (None values remove the key)."""
    row = dict(base)
    for k, v in overrides.items():
        if v is None:
            row.pop(k, None)
        else:
            row[k] = v
    return row


# ---------------------------------------------------------------------------
# 1. Valid row passes
# ---------------------------------------------------------------------------

def test_valid_row_passes():
    ok, errors = validate_row(PANELLA_2005)
    assert ok is True
    assert errors == []


# ---------------------------------------------------------------------------
# 2. Missing required field fails
# ---------------------------------------------------------------------------

def test_missing_required_field_fails():
    row = _patch(PANELLA_2005, doi=None)  # doi is required
    ok, errors = validate_row(row)
    assert ok is False
    assert any("doi" in e for e in errors)


# ---------------------------------------------------------------------------
# 3. Out-of-range temperature fails (below 50 K)
# ---------------------------------------------------------------------------

def test_temperature_below_range_fails():
    row = _patch(PANELLA_2005, temperature_k=20.0)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("temperature_k" in e for e in errors)


def test_temperature_above_range_fails():
    row = _patch(PANELLA_2005, temperature_k=600.0)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("temperature_k" in e for e in errors)


# ---------------------------------------------------------------------------
# 4. Out-of-range pressure fails
# ---------------------------------------------------------------------------

def test_pressure_above_range_fails():
    row = _patch(PANELLA_2005, pressure_bar=250.0)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("pressure_bar" in e for e in errors)


def test_pressure_negative_fails():
    row = _patch(PANELLA_2005, pressure_bar=-1.0)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("pressure_bar" in e for e in errors)


# ---------------------------------------------------------------------------
# 5. Invalid material_class fails
# ---------------------------------------------------------------------------

def test_invalid_material_class_fails():
    row = _patch(PANELLA_2005, material_class="nanotube")  # not in Literal
    ok, errors = validate_row(row)
    assert ok is False
    assert any("material_class" in e for e in errors)


# ---------------------------------------------------------------------------
# 6. Valid row with mmol_g instead of wt_pct
# ---------------------------------------------------------------------------

def test_valid_mmol_g_only():
    """A row with only uptake_mmol_g (no uptake_wt_pct) is valid."""
    row = _patch(PANELLA_2005, uptake_wt_pct=None, uptake_mmol_g=7.44)
    ok, errors = validate_row(row)
    assert ok is True, errors


# ---------------------------------------------------------------------------
# 7. Both uptakes missing fails
# ---------------------------------------------------------------------------

def test_both_uptakes_missing_fails():
    row = _patch(PANELLA_2005, uptake_wt_pct=None, uptake_mmol_g=None)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("uptake" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# 8. Panella 2005 real example: model round-trips correctly
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 9. measurement_id is required (new unique-per-row key)
# ---------------------------------------------------------------------------

def test_missing_measurement_id_fails():
    row = _patch(PANELLA_2005, measurement_id=None)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("measurement_id" in e for e in errors)


def test_with_measurement_id_passes():
    row = _patch(PANELLA_2005, measurement_id="HYC-0001-M2")
    ok, errors = validate_row(row)
    assert ok is True, errors


# ---------------------------------------------------------------------------
# 10. uptake_ml_stp_g optional field with 0–2225 range
# ---------------------------------------------------------------------------

def test_uptake_ml_stp_g_in_range_passes():
    row = _patch(PANELLA_2005, uptake_ml_stp_g=233.0)
    ok, errors = validate_row(row)
    assert ok is True, errors


def test_uptake_ml_stp_g_null_allowed():
    row = _patch(PANELLA_2005, uptake_ml_stp_g=None)
    ok, errors = validate_row(row)
    assert ok is True, errors


def test_uptake_ml_stp_g_negative_fails():
    row = _patch(PANELLA_2005, uptake_ml_stp_g=-1.0)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("uptake_ml_stp_g" in e for e in errors)


def test_uptake_ml_stp_g_above_range_fails():
    row = _patch(PANELLA_2005, uptake_ml_stp_g=2226.0)
    ok, errors = validate_row(row)
    assert ok is False
    assert any("uptake_ml_stp_g" in e for e in errors)


# ---------------------------------------------------------------------------
# 11. Panella 2005 real example: model round-trips correctly
# ---------------------------------------------------------------------------

def test_panella_2005_roundtrip():
    """The real Panella 2005 data point constructs and round-trips without loss."""
    entry = MeasurementEntry.model_validate(PANELLA_2005)
    assert entry.paper_id == "HYC-0001"
    assert entry.first_author == "Panella"
    assert entry.year == 2005
    assert entry.temperature_k == pytest.approx(77.0)
    assert entry.pressure_bar == pytest.approx(1.0)
    assert entry.uptake_wt_pct == pytest.approx(1.5)
    assert entry.uptake_type == "excess"
    assert entry.material_class == "SWCNT"
    assert entry.extraction_confidence == 3
    assert entry.reproducibility_tier == "B"
