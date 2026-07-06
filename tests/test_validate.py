"""Unit tests for src/hycan/validate.py and src/hycan/clean.py."""

import pandas as pd
import pytest

from hycan.clean import clean_dataset
from hycan.validate import (
    DatasetValidationReport,
    ValidationResult,
    validate_dataset,
    validate_row,
)

# ---------------------------------------------------------------------------
# A fully valid baseline row (zero errors, zero warnings).
# ---------------------------------------------------------------------------

BASE = {
    "paper_id": "HYC-2001",
    "doi": "10.1016/j.carbon.2015.01.001",
    "first_author": "Lee",
    "year": 2015,
    "journal": "Carbon",
    "title": "Hydrogen uptake baseline",
    "sample_id": "HYC-2001-S1",
    "measurement_id": "HYC-2001-M1",
    "material_class": "activated_carbon",
    "material_description": "KOH-activated carbon",
    "synthesis_method": "carbonization",
    "temperature_k": 77.0,
    "pressure_bar": 1.0,
    "uptake_wt_pct": 1.5,
    "uptake_type": "excess",
    "measurement_method": "volumetric_sieverts",
    "source_location": "Table 1",
    "extraction_method": "table_direct",
    "extraction_confidence": 4,
    "reproducibility_tier": "B",
    "extractor": "AG",
    "extraction_date": "2026-06-29",
}


def _patch(base: dict, **overrides) -> dict:
    """Return a copy of *base* with *overrides* applied (None removes the key)."""
    row = dict(base)
    for k, v in overrides.items():
        if v is None:
            row.pop(k, None)
        else:
            row[k] = v
    return row


def _categories(messages):
    return {m.split(":", 1)[0].strip() for m in messages}


# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------

def test_valid_row_passes():
    res = validate_row(BASE)
    assert res.is_valid is True
    assert res.errors == []
    assert res.warnings == []


# ---------------------------------------------------------------------------
# Error categories
# ---------------------------------------------------------------------------

def test_missing_required_field_error():
    res = validate_row(_patch(BASE, doi=None))
    assert res.is_valid is False
    assert "Missing required field" in _categories(res.errors)


def test_temperature_out_of_range_error():
    high = validate_row(_patch(BASE, temperature_k=600.0))
    low = validate_row(_patch(BASE, temperature_k=20.0))
    assert high.is_valid is False
    assert low.is_valid is False
    assert "Temperature out of range" in high.errors
    assert "Temperature out of range" in low.errors


def test_pressure_out_of_range_error():
    res = validate_row(_patch(BASE, pressure_bar=0.0))
    assert res.is_valid is False
    assert "Pressure out of range" in res.errors


def test_uptake_out_of_range_error():
    res = validate_row(_patch(BASE, uptake_wt_pct=25.0))
    assert res.is_valid is False
    assert "Uptake out of range" in res.errors
    # An out-of-range uptake is an error, not the >10 warning.
    assert "Uptake above 10 wt%" not in res.warnings


def test_invalid_value_error():
    res = validate_row(_patch(BASE, material_class="nanotube"))
    assert res.is_valid is False
    assert "Invalid value" in _categories(res.errors)


# ---------------------------------------------------------------------------
# Warning categories (none of these flip is_valid)
# ---------------------------------------------------------------------------

def test_pressure_above_200_warning():
    res = validate_row(_patch(BASE, pressure_bar=250.0))
    assert res.is_valid is True
    assert "Pressure above 200 bar" in res.warnings
    assert res.errors == []


def test_uptake_above_10_warning():
    res = validate_row(_patch(BASE, uptake_wt_pct=15.0))
    assert res.is_valid is True
    assert "Uptake above 10 wt%" in res.warnings


def test_unspecified_uptake_type_warning():
    res = validate_row(_patch(BASE, uptake_type="unspecified"))
    assert res.is_valid is True
    assert "Unspecified uptake_type" in res.warnings


def test_micropore_exceeds_total_warning():
    res = validate_row(
        _patch(BASE, micropore_volume_cm3_g=1.0, total_pore_volume_cm3_g=0.5)
    )
    assert res.is_valid is True
    assert "Micropore volume exceeds total pore volume" in res.warnings


def test_swcnt_missing_single_walled_warning():
    res = validate_row(
        _patch(BASE, material_class="SWCNT", material_description="carbon nanotubes")
    )
    assert res.is_valid is True
    assert "SWCNT description missing 'single-walled'" in res.warnings


def test_swcnt_with_single_walled_no_warning():
    res = validate_row(
        _patch(
            BASE,
            material_class="SWCNT",
            material_description="Single-Walled carbon nanotubes",
        )
    )
    assert "SWCNT description missing 'single-walled'" not in res.warnings


def test_mmol_wt_inconsistent_warning():
    # wt=1.0 but mmol=20 converts to ~4.03 wt% -> far more than 5% apart.
    res = validate_row(_patch(BASE, uptake_wt_pct=1.0, uptake_mmol_g=20.0))
    assert res.is_valid is True
    assert "mmol/g and wt% inconsistent" in res.warnings


def test_mmol_wt_consistent_no_warning():
    # 5.95 mmol/g converts to ~1.2 wt%, consistent with uptake_wt_pct=1.2.
    res = validate_row(_patch(BASE, uptake_wt_pct=1.2, uptake_mmol_g=5.95))
    assert "mmol/g and wt% inconsistent" not in res.warnings


def test_pre2005_raw_cnt_tier_d_warning():
    res = validate_row(
        _patch(
            BASE,
            year=2003,
            material_class="MWCNT",
            material_description="Multi-walled carbon nanotubes",
            uptake_wt_pct=6.0,
        )
    )
    assert res.is_valid is True
    assert "Pre-2005 raw-CNT high uptake (Tier D)" in res.warnings


# ---------------------------------------------------------------------------
# Dataset-level checks
# ---------------------------------------------------------------------------

def test_dataset_duplicate_sample_id_allowed():
    # One physical sample measured at two conditions: same sample_id, distinct
    # measurement_id. This is now allowed (no duplicate-key error).
    row_a = _patch(BASE, measurement_id="HYC-2001-M1")
    row_b = _patch(BASE, measurement_id="HYC-2001-M2", pressure_bar=20.0)
    report = validate_dataset(pd.DataFrame([row_a, row_b]))
    assert "Duplicate sample_id" not in report.error_counts
    assert "Duplicate measurement_id" not in report.error_counts
    assert all(r.is_valid for r in report.results)


def test_dataset_duplicate_measurement_id_error():
    df = pd.DataFrame([dict(BASE), dict(BASE)])  # identical measurement_id
    report = validate_dataset(df)
    assert report.error_counts.get("Duplicate measurement_id") == 2
    assert all(r.is_valid is False for r in report.results)


def test_dataset_doi_conflict_warning():
    row_a = dict(BASE)
    row_b = _patch(
        BASE,
        sample_id="HYC-2001-S2",
        measurement_id="HYC-2001-M2",
        first_author="Kim",
    )  # same doi
    report = validate_dataset(pd.DataFrame([row_a, row_b]))
    assert report.warning_counts.get("DOI metadata conflict") == 2
    # A metadata conflict is only a warning; rows stay valid.
    assert all(r.is_valid for r in report.results)


# ---------------------------------------------------------------------------
# clean_dataset
# ---------------------------------------------------------------------------

def test_clean_dataset_behaviour():
    raw = pd.DataFrame(
        [
            {
                "doi": "  10.1016/J.CARBON.2010.01.001  ",
                "material_class": " swcnt ",
                "material_description": "  spaced text  ",
                "uptake_wt_pct": 2.01588,  # -> mmol/g should be filled as ~10
                "uptake_mmol_g": None,
            },
            {
                "doi": "10.1021/Foo",
                "material_class": "Activated_Carbon",
                "material_description": "x",
                "uptake_wt_pct": None,  # -> wt% should be filled from mmol/g
                "uptake_mmol_g": 10.0,
            },
        ]
    )
    cleaned = clean_dataset(raw)

    # Input is not mutated.
    assert raw.loc[0, "doi"] == "  10.1016/J.CARBON.2010.01.001  "

    # Whitespace stripped + DOI lowercased.
    assert cleaned.loc[0, "doi"] == "10.1016/j.carbon.2010.01.001"
    assert cleaned.loc[0, "material_description"] == "spaced text"

    # material_class standardised to controlled-vocabulary spellings.
    assert cleaned.loc[0, "material_class"] == "SWCNT"
    assert cleaned.loc[1, "material_class"] == "activated_carbon"

    # Cross-fill of uptake columns.
    assert cleaned.loc[0, "uptake_mmol_g"] == pytest.approx(10.0, abs=1e-3)
    assert cleaned.loc[1, "uptake_wt_pct"] == pytest.approx(2.01588, abs=1e-3)


# ---------------------------------------------------------------------------
# 5-row toy dataset mirroring data/raw/test_measurements.csv
# ---------------------------------------------------------------------------

@pytest.fixture
def toy_df():
    rows = [
        # 3 fully valid rows
        _patch(
            BASE,
            paper_id="HYC-1001",
            doi="10.1/a",
            sample_id="HYC-1001-S1",
            measurement_id="HYC-1001-M1",
        ),
        _patch(
            BASE,
            paper_id="HYC-1002",
            doi="10.1/b",
            sample_id="HYC-1002-S1",
            measurement_id="HYC-1002-M1",
            material_class="MWCNT",
            material_description="Multi-walled carbon nanotubes",
            uptake_wt_pct=0.8,
        ),
        _patch(
            BASE,
            paper_id="HYC-1003",
            doi="10.1/c",
            sample_id="HYC-1003-S1",
            measurement_id="HYC-1003-M1",
            material_class="SWCNT",
            material_description="Single-walled carbon nanotubes",
            uptake_wt_pct=2.5,
        ),
        # 1 row whose only issue is an unspecified uptake_type (one warning)
        _patch(
            BASE,
            paper_id="HYC-1004",
            doi="10.1/d",
            sample_id="HYC-1004-S1",
            measurement_id="HYC-1004-M1",
            uptake_type="unspecified",
        ),
        # 1 row whose only issue is an out-of-range temperature (one error)
        _patch(
            BASE,
            paper_id="HYC-1005",
            doi="10.1/e",
            sample_id="HYC-1005-S1",
            measurement_id="HYC-1005-M1",
            temperature_k=600.0,
        ),
    ]
    return pd.DataFrame(rows)


def test_toy_dataset_report(toy_df):
    report = validate_dataset(toy_df)
    assert isinstance(report, DatasetValidationReport)
    assert report.total == 5
    assert sum(1 for r in report.results if r.is_valid) == 4
    assert report.error_counts == {"Temperature out of range": 1}
    assert report.warning_counts == {"Unspecified uptake_type": 1}


def test_validation_result_dataclass_shape():
    res = validate_row(BASE)
    assert isinstance(res, ValidationResult)
    assert hasattr(res, "is_valid")
    assert hasattr(res, "errors")
    assert hasattr(res, "warnings")
