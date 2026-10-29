"""Schema v2 row rules (src/hycan/schema.py, schema_v2_consistency; protocol §3)."""

from __future__ import annotations

import pytest
from conftest import make_row
from pydantic import ValidationError

from hycan.schema import MeasurementEntry

CODED = {
    "basis_stated": True,
    "basis_evidence": '"excess adsorption ... Gibbs surface excess" (Section 2.3)',
    "basis_inferred": "excess",
    "wt_pct_convention": "W1",
    "wt_pct_convention_source": "stated",
    "value_kind": "measured",
    "isotherm_branch": "adsorption",
    "temperature_inferred": False,
    "data_location": "main_text",
    "instrument_identified": True,
    "calibration_described": True,
    "replicates_reported": False,
    "surface_area_probe_gas": "N2",
    "area_same_sample": "yes",
    "bet_range_stated": True,
    "bet_consistency_criteria_stated": False,
    "measuring_lab_id": "LAB-1",
}


def entry(**over) -> MeasurementEntry:
    return MeasurementEntry(**make_row(**{**CODED, **over}))


def test_a_fully_coded_row_is_valid():
    entry()


def test_an_uncoded_row_is_valid():
    MeasurementEntry(**make_row())


def test_rule_1_stated_basis_needs_its_quote():
    with pytest.raises(ValidationError, match="basis_evidence is empty"):
        entry(basis_evidence="  ")
    entry(basis_stated=False, basis_evidence=None)


def test_rule_2_inferred_temperature_is_77_3_k():
    entry(temperature_inferred=True, temperature_k=77.3)
    with pytest.raises(ValidationError, match="must be 77.3"):
        entry(temperature_inferred=True, temperature_k=77.0)


def test_rule_3_digitization_uncertainty_needs_a_digitized_value():
    entry(extraction_method="figure_digitized", digitization_uncertainty_wt_pct=0.05)
    with pytest.raises(ValidationError, match="not figure_digitized"):
        entry(digitization_uncertainty_wt_pct=0.05)


@pytest.mark.parametrize(
    "field",
    [
        "basis_inferred",
        "value_kind",
        "isotherm_branch",
        "temperature_inferred",
        "data_location",
        "instrument_identified",
        "calibration_described",
        "replicates_reported",
        "measuring_lab_id",
        "surface_area_probe_gas",
        "area_same_sample",
        "bet_range_stated",
        "bet_consistency_criteria_stated",
    ],
)
def test_rule_4_a_coded_row_codes_every_field_that_applies(field):
    with pytest.raises(ValidationError, match=field):
        entry(**{field: None})


def test_rule_4_area_fields_apply_only_when_an_area_is_reported():
    no_area = {
        "surface_area_method": "not_reported",
        "bet_surface_area_m2_g": None,
        "surface_area_probe_gas": None,
        "area_same_sample": None,
        "bet_range_stated": None,
        "bet_consistency_criteria_stated": None,
    }
    entry(**no_area)
    langmuir = {
        "surface_area_method": "Langmuir",
        "bet_range_stated": None,
        "bet_consistency_criteria_stated": None,
    }
    entry(**langmuir)
    with pytest.raises(ValidationError, match="area_same_sample"):
        entry(**{**langmuir, "area_same_sample": None})


@pytest.mark.parametrize(
    ("convention", "source", "ok"),
    [
        ("W1", "computed_from_other_unit", True),
        ("W2", "computed_from_other_unit", False),
        ("W1", "stated", True),
        ("W2", "stated", True),
        ("unknown", "stated", False),
        ("W2", "inferred_from_paired_units", True),
        ("unknown", "none", True),
        ("W1", "none", False),
    ],
)
def test_rule_5_convention_and_source_agree(convention, source, ok):
    kw = {"wt_pct_convention": convention, "wt_pct_convention_source": source}
    if ok:
        entry(**kw)
    else:
        with pytest.raises(ValidationError, match="requires wt_pct_convention"):
            entry(**kw)


def test_rule_5_convention_and_source_are_coded_together():
    with pytest.raises(ValidationError, match="coded together"):
        MeasurementEntry(**make_row(wt_pct_convention="W1"))


def test_validator_reports_schema_v2_messages_verbatim():
    from hycan.validate import validate_row

    errors = validate_row(make_row(**{**CODED, "basis_evidence": ""})).errors
    assert errors == [
        (
            "Invalid row: basis_stated is true but basis_evidence is empty; a "
            "stated basis must carry the quote that states it"
        )
    ]
    errors = validate_row(make_row(**{**CODED, "value_kind": None})).errors
    assert any("uncoded: value_kind" in e for e in errors)


def test_validator_reports_every_model_rule_in_its_own_words():
    from hycan.validate import validate_row

    errors = validate_row(make_row(volumetric_capacity_kg_m3=30.0)).errors
    assert any("volumetric_capacity_basis is null" in e for e in errors)
    errors = validate_row(make_row(temperature_k=None)).errors
    assert "Missing required field: temperature_k" in errors
    errors = validate_row(make_row(temperature_unstated=True)).errors
    assert any("temperature_unstated is set but temperature_k" in e for e in errors)
    errors = validate_row(
        make_row(uptake_wt_pct=None, uptake_mmol_g=None, uptake_ml_stp_g=20.0)
    ).errors
    assert any("At least one of 'uptake_wt_pct' or 'uptake_mmol_g'" in e for e in errors)


@pytest.mark.parametrize("route", ["S1", "S2", "legacy_v0.1", "legacy_v0.1_ineligible",
                                   "legacy_v0.1_not_retrieved"])
def test_selection_route_values_including_amendment_2(route):
    assert entry(selection_route=route, frame_id="F00001").selection_route == route


def test_an_unknown_selection_route_is_refused():
    with pytest.raises(ValidationError):
        entry(selection_route="legacy_v0.1_unretrieved")
