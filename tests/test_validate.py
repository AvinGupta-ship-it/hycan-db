"""Unit tests for src/hycan/validate.py and src/hycan/clean.py."""

import csv
from pathlib import Path

import pandas as pd
import pytest

from hycan.clean import clean_dataset
from hycan.validate import (
    DatasetValidationReport,
    ValidationResult,
    score_reproducibility,
    suggest_tier,
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


def test_micropore_exceeds_total_is_an_error_in_v1_1():
    """§11.2 always specified ERROR here; the v1.0 code raised a warning.

    No row in the corpus violates it, so resolving the mismatch in the
    manual's favour changes nothing in the dataset.
    """
    res = validate_row(
        _patch(BASE, micropore_volume_cm3_g=1.0, total_pore_volume_cm3_g=0.5)
    )
    assert res.is_valid is False
    assert "Micropore volume exceeds total pore volume" in res.errors


def test_ultramicropore_exceeding_micropore_is_an_error():
    """§8.5 gap 4: ultramicropore <= micropore <= total."""
    res = validate_row(
        _patch(BASE, ultramicropore_volume_cm3_g=0.9,
               micropore_volume_cm3_g=0.4, total_pore_volume_cm3_g=1.0)
    )
    assert res.is_valid is False
    assert "Ultramicropore volume exceeds micropore volume" in res.errors


def test_ultramicropore_exceeding_total_is_caught_without_a_micropore_value():
    """The pairs are checked independently; a missing middle term must not hide it."""
    res = validate_row(
        _patch(BASE, ultramicropore_volume_cm3_g=1.5,
               micropore_volume_cm3_g=None, total_pore_volume_cm3_g=1.0)
    )
    assert res.is_valid is False
    assert "Ultramicropore volume exceeds total pore volume" in res.errors


def test_properly_nested_pore_volumes_are_clean():
    res = validate_row(
        _patch(BASE, ultramicropore_volume_cm3_g=0.27,
               ultramicropore_cutoff_nm=0.7,
               micropore_volume_cm3_g=0.43, total_pore_volume_cm3_g=0.64)
    )
    assert res.is_valid is True
    assert not [w for w in res.warnings if "pore" in w.lower()]


def test_equal_pore_volumes_are_not_a_violation():
    res = validate_row(
        _patch(BASE, ultramicropore_volume_cm3_g=0.4,
               ultramicropore_cutoff_nm=0.7,
               micropore_volume_cm3_g=0.4, total_pore_volume_cm3_g=0.4)
    )
    assert res.is_valid is True


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


# ---------------------------------------------------------------------------
# Reproducibility tiering
# ---------------------------------------------------------------------------

def test_suggest_tier_returns_valid_letter():
    assert suggest_tier(BASE) in {"A", "B", "C", "D"}


def test_full_report_row_scores_nine_tier_a():
    """Worked example 1 of docs/reproducibility_tiering.md.

    `surface_area_method` was absent from this fixture until the scorer learned to
    tell a BET area from an area of unknown method. The example states "reports BET
    ≈ 2600 m²/g", so the row was always meant to carry a BET area and the fixture
    merely omitted the field that says so. Adding it completes the fixture; the
    total is still 9 and the tier still A. §6.7: check what a field's absence
    *means* before changing the assertion that depends on it.
    """
    row = {
        "bet_surface_area_m2_g": 2600,
        "surface_area_method": "BET",
        "measurement_method": "gravimetric_microbalance",
        "temperature_k": 77,
        "pressure_bar": 20,
        "uptake_type": "excess",
        "purification_method": "HNO3 reflux",
        "uptake_wt_pct": 4.8,
    }
    # code ceiling is 9; calibration unscored
    assert score_reproducibility(row)["total"] == 9
    assert suggest_tier(row) == "A"


def test_the_same_area_without_a_stated_method_scores_one_point_less():
    """The one-line difference between worked examples 1 and 2.

    MUTATION: collapse `_score_bet` back to "2 for any positive area" -> this
    fails, and so does the corpus assertion that HYC-0005's 25 rows score 1.
    """
    row = {
        "bet_surface_area_m2_g": 2600,
        "surface_area_method": "unspecified",
        "measurement_method": "gravimetric_microbalance",
        "temperature_k": 77,
        "pressure_bar": 20,
        "uptake_type": "excess",
        "purification_method": "HNO3 reflux",
        "uptake_wt_pct": 4.8,
    }
    scored = score_reproducibility(row)
    assert scored["bet"] == 1
    assert scored["bet_basis"] == "area_by_unspecified"
    assert scored["total"] == 8


def test_missing_bet_room_temp_high_uptake_tier_c():
    row = {
        "measurement_method": "volumetric_sieverts",
        "temperature_k": 298,
        "pressure_bar": 100,
        "uptake_type": "unspecified",
        "purification_method": "acid",
        "uptake_wt_pct": 4.2,
    }
    # suggest_tier says C; the human later downgrades to D via the physics clause.
    assert suggest_tier(row) == "C"


def test_cryogenic_low_pressure_low_uptake_tier_b():
    row = {
        "bet_surface_area_m2_g": 1500,
        "measurement_method": "volumetric_sieverts",
        "temperature_k": 77,
        "pressure_bar": 1,
        "uptake_type": "unspecified",
        "uptake_wt_pct": 0.5,
    }
    # low value at 1 bar is consistent, not penalized
    assert suggest_tier(row) == "B"


def test_calibration_always_zero():
    assert score_reproducibility(BASE)["calibration"] == 0


def test_derive_wt_pct_via_mmol():
    row = {"uptake_mmol_g": 10}
    assert score_reproducibility(row)["derived_wt_pct"] == pytest.approx(
        2.01588, abs=1e-6
    )


# ---------------------------------------------------------------------------
# The four score_reproducibility fixes.
# docs/migration_score_reproducibility_plan.md. Each guard carries a MUTATION:
# line, and each was confirmed to fail against the mutation it names.
# ---------------------------------------------------------------------------

DATASET = Path(__file__).resolve().parents[1] / "data" / "raw" / "measurements_v0.1.csv"


def _corpus() -> list[dict]:
    with DATASET.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _scored() -> dict[str, dict]:
    return {r["measurement_id"]: score_reproducibility(r) for r in _corpus()}


# --- Defect 1: a null temperature no longer buys a free Chahine point -------


def test_an_unstated_temperature_scores_zero_on_chahine_not_one():
    """§13.7's prescribed fix. The criterion reads "for the stated conditions".

    MUTATION: restore `if not _present(t) or w is None: chahine = 1` -> this
    fails, and HYC-0011-M4 goes back to suggesting C.
    """
    row = {
        "measurement_method": "volumetric_sieverts",
        "uptake_wt_pct": 8.0,
        "temperature_unstated": True,
    }
    scored = score_reproducibility(row)
    assert scored["chahine"] == 0
    assert scored["chahine_basis"] == "temperature_not_reported"


def test_the_discredited_row_and_the_ordinary_row_no_longer_score_alike():
    """The concrete consequence §13.7 names, asserted on the real rows.

    HYC-0011-M4 is the 8.0 wt% film that carries the corpus's only
    `Pre-2005 raw-CNT high uptake (Tier D)` warning; M1 is an ordinary 0.26 wt%
    row from the same paper. Neither states a temperature. Under the old scorer
    both totalled 3 and both suggested C -- the free point was the only thing
    holding the 8.0 wt% row above D.

    MUTATION: restore the free point -> M4 suggests C again and this fails.
    """
    scored = _scored()
    assert scored["HYC-0011-M4"]["suggested_tier"] == "D"
    assert scored["HYC-0011-M4"]["chahine_basis"] == "temperature_not_reported"


def test_the_three_unassessable_chahine_cases_partition_the_corpus():
    """Pinned as a partition, not as a total, per §6.7.

    Six rows failed to report a temperature; twelve carry no uptake at all; eleven
    report uptake non-gravimetrically. Each gets a different basis and only the
    last two keep a point.

    Ten, not the eight the plan first said: that figure was taken from the count
    of `volumetric_capacity_kg_m3` rather than computed from the rows whose uptake
    does not convert to wt%. Three HYC-0024 rows carry only an adsorbed-phase
    density and one carries an approximate wt% from the paper's abstract.

    MUTATION: merge any two of the three branches -> the partition breaks.
    """
    by_basis: dict[str, list[str]] = {}
    for mid, s in _scored().items():
        by_basis.setdefault(s["chahine_basis"], []).append(mid)

    no_uptake = by_basis.get("not_applicable_no_uptake", [])
    non_grav = by_basis.get("not_assessable_non_gravimetric", [])
    unstated = by_basis.get("temperature_not_reported", [])

    # 12 before the 2026-10-02 Phase D batch; +2 for HYC-0033's two
    # characterization-only boron-doped rows (its hydrogen uptake is figure-only).
    assert len(no_uptake) == 14
    assert len(non_grav) == 11
    assert sorted(unstated) == [
        "HYC-0011-M1",
        "HYC-0011-M2",
        "HYC-0011-M3",
        "HYC-0011-M4",
        "HYC-0015-M1",
        "HYC-0015-M2",
    ]
    scored = _scored()
    assert all(scored[m]["chahine"] == 1 for m in no_uptake + non_grav)
    assert all(scored[m]["chahine"] == 0 for m in unstated)
    # Ten of the eleven belong to the one paper whose hydrogen is entirely
    # volumetric; the eleventh is HYC-0011's areal row, where the film was never
    # weighed so no wt% exists even in principle.
    assert {m.rsplit("-", 1)[0] for m in non_grav} == {"HYC-0024", "HYC-0011"}
    assert "HYC-0011-M5" in non_grav


def test_a_volumetric_only_row_keeps_its_point_because_the_rule_is_gravimetric():
    """Distinguishes defect 1's fix from a blanket penalty.

    MUTATION: score 0 whenever `_derive_wt_pct` is None -> this fails, and
    HYC-0024's eight volumetric rows are penalised for the schema's limits
    rather than the paper's reporting.
    """
    row = {
        "measurement_method": "volumetric_sieverts",
        "temperature_k": 293,
        "pressure_bar": 100,
        "volumetric_capacity_kg_m3": 30.0,
        "volumetric_capacity_basis": "tank_volume",
    }
    scored = score_reproducibility(row)
    assert scored["chahine"] == 1
    assert scored["chahine_basis"] == "not_assessable_non_gravimetric"


# --- Defect 2: the three-level BET scale the rubric already specified -------


def test_resolved_component_areas_score_a_bet_point_instead_of_zero():
    """HYC-0007 reports a micropore and an external area and no total.

    MUTATION: drop the `resolved_components` branch -> all 8 HYC-0007 rows score
    `bet = 0`, which asserts the paper reported no surface area.
    """
    row = {
        "micropore_surface_area_m2_g": 1200,
        "external_surface_area_m2_g": 300,
        "surface_area_method": "alpha_s_plot",
    }
    scored = score_reproducibility(row)
    assert scored["bet"] == 1
    assert scored["bet_basis"] == "resolved_components"


def test_the_bet_scale_is_pinned_across_the_corpus_by_paper():
    """The 39 rows defect 2 moves, by id, so a silent re-collapse fails.

    MUTATION: award 2 for any positive area -> HYC-0005 and HYC-0012 go back to
    2 and this fails; drop the component branch -> HYC-0007 goes back to 0.
    """
    by_basis: dict[str, set[str]] = {}
    for mid, s in _scored().items():
        by_basis.setdefault(s["bet_basis"], set()).add(mid.rsplit("-", 1)[0])
    assert by_basis["resolved_components"] == {"HYC-0007"}
    assert by_basis["area_by_unspecified"] == {"HYC-0005", "HYC-0012"}
    scored = _scored()
    assert all(
        s["bet"] == 1
        for s in scored.values()
        if s["bet_basis"] in {"resolved_components", "area_by_unspecified"}
    )
    assert all(s["bet"] == 2 for s in scored.values() if s["bet_basis"] == "bet_total")
    assert all(s["bet"] == 0 for s in scored.values() if s["bet_basis"] == "no_area")


# --- Defect 3: purity means purity REPORTED, not the sample PURIFIED --------


def test_a_reported_residual_metal_scores_the_purity_point():
    """HYC-0007's pristine SWCNT scored 0 while the paper reports 11 wt% metal.

    MUTATION: restore `purity = 1 if purification_method` alone -> this fails.
    """
    row = {"residual_metal_element": "Ni", "residual_metal_wt_pct": 11.0}
    scored = score_reproducibility(row)
    assert scored["purity"] == 1
    assert scored["purity_basis"] == "residual_metal_measured"


def test_the_purity_fix_only_ever_turns_a_zero_into_a_one():
    """It must not cost any row a point it already had.

    MUTATION: reorder `_score_purity` so a named metal shadows a measured one, or
    make any branch return 0 -> a row loses a point and this fails.
    """
    for row in _corpus():
        if row.get("purification_method", "").strip():
            assert score_reproducibility(row)["purity"] == 1, row["measurement_id"]


# --- Defect 4: the Chahine bound can see a resolved area -------------------


def test_the_chahine_bound_falls_back_to_the_component_sum():
    """1200 + 300 = 1500 m²/g, so the expectation is 3.0 wt% and 1.0 clears it.

    MUTATION: drop `_chahine_bounding_area`'s component branch -> the basis
    becomes `cryo_no_area`, the score drops to 1, and this fails.
    """
    row = {
        "micropore_surface_area_m2_g": 1200,
        "external_surface_area_m2_g": 300,
        "temperature_k": 77,
        "pressure_bar": 1,
        "uptake_wt_pct": 1.0,
    }
    scored = score_reproducibility(row)
    assert scored["chahine"] == 2
    assert scored["chahine_basis"] == "cryo_vs_component_sum"


def test_a_langmuir_area_earns_a_bet_point_but_never_bounds_chahine():
    """Deliberate asymmetry: Langmuir over-reads on microporous carbon, so using
    it as a bound would loosen the check in the direction that hides an
    over-claim.

    MUTATION: add Langmuir to `_chahine_bounding_area` -> the basis becomes
    `cryo_vs_...` and this fails.
    """
    row = {
        "langmuir_surface_area_m2_g": 1800,
        "temperature_k": 77,
        "pressure_bar": 1,
        "uptake_wt_pct": 2.0,
    }
    scored = score_reproducibility(row)
    assert scored["bet"] == 1
    assert scored["bet_basis"] == "langmuir_only"
    assert scored["chahine_basis"] == "cryo_no_area"


# --- The rubric's own worked examples, which are the real validation --------


def test_worked_example_two_scores_its_bet_and_purity_points():
    """docs/reproducibility_tiering.md example 2: a Langmuir area, 77 K / 1 bar,
    no type, no purity, ~2 wt%. Hand-scored BET 1, purity 0, Chahine 2, Tier C.

    The fix brings BET and purity onto the document's numbers. **Chahine does not
    match and is not meant to:** the document awards 2 on physical plausibility --
    2 wt% at 77 K / 1 bar is unremarkable -- which is a judgment the code has no
    way to make. It returns 1, "cannot assess", because the only area present is
    Langmuir and `_chahine_bounding_area` deliberately refuses to bound against
    one. Two documented divergences are asserted here rather than hidden: this,
    and `method` 2 where the document hand-scores 1 for a named-only protocol.
    Both land on Tier C anyway, which the document itself states.
    """
    row = {
        "langmuir_surface_area_m2_g": 1800,
        "measurement_method": "volumetric_sieverts",
        "temperature_k": 77,
        "pressure_bar": 1,
        "uptake_type": "unspecified",
        "uptake_wt_pct": 2.0,
    }
    scored = score_reproducibility(row)
    assert (scored["bet"], scored["purity"]) == (1, 0)
    assert scored["chahine"] == 1, "the document awards 2 on plausibility"
    assert scored["chahine_basis"] == "cryo_no_area"
    assert scored["method"] == 2, "the document hand-scores this 1; the code cannot"
    assert scored["suggested_tier"] == "C"


def test_worked_example_three_scores_zero_on_bet_and_chahine():
    """Example 3: no surface area, room temperature, an uptake far above the
    ~1 wt% bound. Hand-scored BET 0, Chahine 0, Tier D under the physics clause.

    The code reaches Tier C, which the document states explicitly -- it cannot
    apply the categorical override and scores the method as recorded. Asserting
    the C is asserting the documented blind spot, not endorsing it.
    """
    row = {
        "measurement_method": "volumetric_sieverts",
        "temperature_k": 298,
        "pressure_bar": 100,
        "uptake_type": "unspecified",
        "uptake_wt_pct": 6.0,
    }
    scored = score_reproducibility(row)
    assert (scored["bet"], scored["chahine"]) == (0, 0)
    assert scored["suggested_tier"] == "C"


# --- What the fix must not disturb -----------------------------------------


def test_no_assigned_tier_changed_and_the_scorer_still_returns_a_letter():
    """The plan's post-conditions 2 and 8.

    MUTATION: make `suggest_tier` return the assigned tier -> the agreement
    assertion below becomes 225 and this fails.
    """
    scored = _scored()
    assert all(s["suggested_tier"] in {"A", "B", "C", "D"} for s in scored.values())
    assert suggest_tier({}) in {"A", "B", "C", "D"}
    agree = sum(
        1
        for r in _corpus()
        if scored[r["measurement_id"]]["suggested_tier"] == r["reproducibility_tier"]
    )
    # 141 of 227. Agreement with the assigned tiers is NOT the success metric --
    # if it were, the correct fix would be whatever reproduces the humans'
    # choices, which destroys the only thing an independent scorer is for. The
    # scorer's plan §6 names the rows that moved away and why none is re-tiered.
    #
    # Pinned as a total on purpose, unlike most counts in this suite: it is a
    # statement about how far an independent scorer diverges from human judgment
    # over the whole corpus, and that is only meaningful as a total. It must be
    # updated deliberately whenever the corpus changes, which is the point.
    # 141 of 227 before HYC-0031. 164 of 259 after HYC-0031: that paper
    # contributes 23 agreements and 9 disagreements, the 9 being the rows where
    # the extractor overrode the scorer on its two documented blind spots -- a
    # vacuous Chahine bound at 1 bar, and a `total` row scored against a bound
    # defined for `excess`. Now 191 of 288 after the 2026-10-02 Phase D batch
    # (HYC-0032/0033/0034/0037): +27 agreements and exactly 2 disagreements --
    # HYC-0032-M9 (scorer C, assigned B: the pressure-blind Chahine bound at
    # 1 bar) and HYC-0037-M3 (scorer A, assigned B: residual Fe is unquantified
    # and the paper credits it for part of the uptake, so not anchor-quality).
    # Both are documented hand-adjustments. Updated deliberately, per this pin's
    # own instruction. No assigned tier changed.
    # Now 224 of 343 after the HYC-0039/0040/0041/0042/0043 Phase D batch: +33
    # agreements and 22 documented hand-adjustments where the assigned tier diverges
    # from the scorer. HYC-0039's 14 cryogenic (77 K) rows: the calibration point is
    # added by hand for the He skeletal-density void-volume correction the scorer
    # cannot see (scorer C, assigned B). HYC-0040's three 77 K rows: the categorical
    # physics override -- 9.8/8.2/6.9 wt% on ~900 m2/g is inconsistent with
    # physisorption (scorer C, assigned D) -- and four of its 273/298 K rows take the
    # calibration point for the LaNi5/basolite reference-sample calibration (scorer C,
    # assigned B). HYC-0043-M2: the 100-bar 4.51 wt% value (scorer B, assigned C)
    # because Fig 4b shows the excess maximum near ~25-30 bar, so the 100-bar pairing
    # is uncertain. All 22 are new rows; no existing assigned tier changed.
    assert agree == 224


def test_the_rows_in_tension_with_their_assigned_tier_are_named():
    """Plan §6. These are open questions, deliberately not resolved in code.

    Eight when the scorer was fixed; **nine since HYC-0011-M5 was appended, and
    the ninth has a different cause from the other eight.** M5's uptake is areal,
    so `_derive_wt_pct` returns None and the Chahine criterion scores 1, "cannot
    assess" -- a free point that lifts it to a suggested C against an assigned D.
    That is the same shape of defect §13.7 fixed for a null temperature, surviving
    in the non-gravimetric branch, and it is the argument for a `tier_basis` field
    or a second mechanism-aware rubric rather than another patch to this one.

    MUTATION: quietly re-tier any of them in the dataset -> this fails, which is
    the point: the disagreement is published, per §13.6.
    """
    scored = _scored()
    tension = sorted(
        r["measurement_id"]
        for r in _corpus()
        if scored[r["measurement_id"]]["suggested_tier"] != r["reproducibility_tier"]
        and r["paper_id"] in {"HYC-0005", "HYC-0011"}
    )
    assert tension == [
        "HYC-0005-M2",
        "HYC-0005-M3",
        "HYC-0005-M4",
        "HYC-0005-M6",
        "HYC-0005-M7",
        "HYC-0011-M1",
        "HYC-0011-M2",
        "HYC-0011-M3",
        "HYC-0011-M5",
    ]


def test_the_code_ceiling_is_still_nine_because_calibration_has_no_field():
    """MUTATION: award calibration a point -> a row could suggest A on an
    `unspecified` uptake type and this fails."""
    assert max(s["total"] for s in _scored().values()) <= 9
    assert all(s["calibration"] == 0 for s in _scored().values())
