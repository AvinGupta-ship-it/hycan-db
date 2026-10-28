"""Tests of hycan.v1 against the rules of docs/v1_protocol.md §3, §10 and §11.0.

Each test names the protocol rule it checks. The protocol governs: a failing
test here means the code is wrong, unless the test misstates the protocol.
"""

from __future__ import annotations

import math

import pandas as pd
import pytest

from hycan import v1
from hycan.v1 import Point

# ---------------------------------------------------------------------------
# §3 77 K
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("t", "expected"),
    [
        (76.0, True),
        (77.0, True),
        (77.3, True),
        (79.0, True),
        (75.99, False),
        (79.01, False),
        (None, False),
        (float("nan"), False),
        (298.15, False),
    ],
)
def test_77k_window_is_76_to_79_inclusive(t, expected):
    assert v1.is_77k(t) is expected


# ---------------------------------------------------------------------------
# §3 wt% convention
# ---------------------------------------------------------------------------


def test_w1_w2_definitions_round_trip():
    for w2 in (0.0, 1.0, 5.0, 7.0, 12.5):
        assert v1.w1_to_w2(v1.w2_to_w1(w2)) == pytest.approx(w2, abs=1e-12)
    # W1 = W2 / (1 - W2/100), so 5 wt% W2 is 5/0.95 W1.
    assert v1.w2_to_w1(5.0) == pytest.approx(5.0 / 0.95)


@pytest.mark.parametrize(("w2", "understated"), [(5.0, 0.26), (6.0, 0.38), (7.0, 0.53)])
def test_reading_w2_as_w1_understates_by_the_stated_amounts(w2, understated):
    gap = v1.w2_to_w1(w2) - w2
    assert gap == pytest.approx(w2**2 / (100 - w2))
    assert round(gap, 2) == understated


def test_reading_w2_as_w1_understates_by_5_3_to_7_5_percent_of_reported():
    assert round(100 * (v1.w2_to_w1(5.0) - 5.0) / 5.0, 1) == 5.3
    assert round(100 * (v1.w2_to_w1(7.0) - 7.0) / 7.0, 1) == 7.5
    assert round(100 * (v1.w2_to_w1(5.0) - 5.0) / v1.w2_to_w1(5.0), 1) == 5.0
    assert round(100 * (v1.w2_to_w1(7.0) - 7.0) / v1.w2_to_w1(7.0), 1) == 7.0


def test_w1_prefers_molar_then_volumetric_then_wt_pct():
    row = {"uptake_mmol_g": 10.0, "uptake_ml_stp_g": 100.0, "uptake_wt_pct": 9.9}
    assert v1.w1_wt_pct(row) == pytest.approx(2.01588)
    row = {"uptake_ml_stp_g": 22.414, "uptake_wt_pct": 9.9}
    assert v1.w1_wt_pct(row) == pytest.approx(0.201588)
    assert v1.w1_wt_pct({"uptake_wt_pct": 3.0, "wt_pct_convention": "W1"}) == 3.0


def test_w2_is_converted_and_unknown_is_used_as_reported():
    assert v1.w1_wt_pct({"uptake_wt_pct": 5.0, "wt_pct_convention": "W2"}) == (
        pytest.approx(5.0 / 0.95)
    )
    assert v1.w1_wt_pct({"uptake_wt_pct": 5.0, "wt_pct_convention": "unknown"}) == 5.0
    assert v1.w1_wt_pct({"uptake_wt_pct": 5.0}) == 5.0


def test_sensitivity_vii_treats_unknown_as_w2_but_leaves_w1():
    unknown = {"uptake_wt_pct": 5.0, "wt_pct_convention": "unknown"}
    assert v1.w1_wt_pct(unknown, unknown_as_w2=True) == pytest.approx(5.0 / 0.95)
    stated_w1 = {"uptake_wt_pct": 5.0, "wt_pct_convention": "W1"}
    assert v1.w1_wt_pct(stated_w1, unknown_as_w2=True) == 5.0


def test_conversion_constants_match_section_11_0():
    # W1 = 0.201588 x mmol/g = 0.1 x mg/g = 0.0089938 x cm3(STP)/g
    assert v1.mmol_per_g_to_wt_pct(1.0) == pytest.approx(0.201588)
    assert v1.ml_stp_per_g_to_wt_pct(1.0) == pytest.approx(0.0089938, abs=5e-8)


def test_no_uptake_gives_no_w1():
    assert v1.w1_wt_pct({}) is None


@pytest.mark.parametrize(
    ("printed", "half"),
    [("5.5", 0.05), ("12", 0.5), ("2.730", 0.0005), (" 0.26 ", 0.005)],
)
def test_half_unit_of_last_printed_digit(printed, half):
    assert v1.half_unit(printed) == pytest.approx(half)


def test_pair_inference_identifies_w2():
    # 28.6 mmol/g is W1 5.765; a printed 5.5 matches only W2 (5.451 -> 5.5).
    assert v1.convention_from_pair("5.5", "28.6", "mmol_g") == "W2"


def test_pair_inference_identifies_w1():
    assert v1.convention_from_pair("5.77", "28.6", "mmol_g") == "W1"
    assert v1.convention_from_pair("6.0", "60.0", "mg_g") == "W1"
    # 20 mg/g printed without a decimal is too coarse to tell 2.0 from 1.96.
    assert v1.convention_from_pair("2.0", "20", "mg_g") == "ambiguous"


def test_pair_inference_reports_unit_consistency_failure():
    # 13.63 mmol/g is W1 2.748, W2 2.674; a printed 2.73 matches neither.
    assert v1.convention_from_pair("2.73", "13.63", "mmol_g") == "inconsistent"


def test_pair_inference_is_ambiguous_at_low_uptake():
    # At 0.5 wt% the two conventions differ by 0.0025, inside the rounding.
    assert v1.convention_from_pair("0.5", "2.48", "mmol_g") == "ambiguous"


# ---------------------------------------------------------------------------
# §3 maximum excess
# ---------------------------------------------------------------------------


def iso(*pairs, u=0.0):
    return [Point(p, v, u) for p, v in pairs]


def test_observed_maximum_needs_a_later_drop_of_more_than_1_percent():
    r = v1.nmax(iso((5, 3.0), (20, 5.0), (30, 4.9), (40, 4.8)))
    assert r.nmax_status == "observed_max"
    assert (r.n_ex_max_wt_pct, r.p_at_nmax_bar, r.p_last_bar) == (5.0, 20, 40)


def test_drop_of_exactly_1_percent_is_not_an_observed_maximum():
    # 5.0 -> 4.95 is a drop of exactly 1%, not more than 1%.
    r = v1.nmax(iso((5, 3.0), (20, 5.0), (40, 4.95)))
    assert r.nmax_status != "observed_max"


def test_drop_must_exceed_the_highest_points_uncertainty():
    pts = iso((5, 3.0), (20, 5.0), (40, 4.9), u=0.15)
    assert v1.nmax(pts).nmax_status != "observed_max"
    pts = iso((5, 3.0), (20, 5.0), (40, 4.8), u=0.15)
    assert v1.nmax(pts).nmax_status == "observed_max"


def test_observed_maximum_needs_p_last_of_at_least_10_bar():
    assert v1.nmax(iso((2, 2.0), (6, 2.5), (10, 2.4))).nmax_status == "observed_max"
    r = v1.nmax(iso((2, 2.0), (6, 2.5), (9.9, 2.4)))
    assert r.nmax_status == "none"
    assert r.n_ex_max_wt_pct is None and r.p_at_nmax_bar is None
    assert r.p_last_bar == 9.9


def test_plateau_rise_below_3_percent_from_0_7_p_last():
    # value at 0.7 x 40 = 28 bar is interpolated: 4.90 + 0.8 x (4.95 - 4.90) = 4.94
    r = v1.nmax(iso((5, 3.0), (20, 4.80), (25, 4.90), (30, 4.95), (40, 5.0)))
    assert r.nmax_status == "plateau"
    assert r.n_ex_max_wt_pct == 5.0 and r.p_at_nmax_bar == 40


def test_plateau_needs_p_last_of_at_least_20_bar():
    r = v1.nmax(iso((5, 3.0), (10, 4.9), (19, 5.0)))
    assert r.nmax_status == "none"


def test_rise_of_3_percent_or_more_is_a_lower_bound():
    # 0.7 x 40 = 28 bar sits on a point of 4.0; 4.0 x 1.05 = 4.2 at 40 bar.
    r = v1.nmax(iso((5, 2.0), (28, 4.0), (40, 4.2)))
    assert r.nmax_status == "lower_bound"
    assert r.n_ex_max_wt_pct == 4.2 and r.p_at_nmax_bar == 40


def test_single_point_at_20_bar_or_more_is_a_lower_bound():
    r = v1.nmax(iso((20, 4.5)))
    assert r.nmax_status == "lower_bound"
    assert r.n_ex_max_wt_pct == 4.5
    assert v1.nmax(iso((19.9, 4.5))).nmax_status == "none"


def test_plateau_test_does_not_extrapolate_below_the_first_point():
    # 0.7 x 25 = 17.5 bar lies below the first point (18 bar): not evaluable.
    r = v1.nmax(iso((18, 4.95), (25, 5.0)))
    assert r.nmax_status == "lower_bound"
    assert r.rise_last_vs_07_relative is None


def test_tied_maximum_uses_its_last_occurrence():
    r = v1.nmax(iso((10, 5.0), (20, 4.0), (30, 5.0), (40, 4.5)))
    assert r.nmax_status == "observed_max" and r.p_at_nmax_bar == 30
    # A drop between two equal maxima is not "followed by a lower point".
    r = v1.nmax(iso((5, 3.0), (10, 5.0), (20, 4.0), (30, 5.0)))
    assert r.nmax_status != "observed_max"


def test_points_at_one_pressure_are_averaged_for_the_interpolation():
    pts = iso((5, 3.0), (28, 4.8), (28, 5.0), (40, 5.0))
    assert v1.rise_last_vs_07(pts) == pytest.approx(5.0 / 4.9 - 1)


def test_nmax_of_empty_isotherm_is_none():
    assert v1.nmax([]).nmax_status == "none"


# ---------------------------------------------------------------------------
# §3 basis-shape conflict
# ---------------------------------------------------------------------------

RISING_80 = iso((5, 2.0), (56, 4.0), (80, 4.5))  # rise 12.5% from 56 to 80 bar


def test_conflict_for_inferred_excess_rising_at_60_bar_or_more():
    r = v1.nmax(RISING_80)
    assert v1.basis_shape_conflict(r, False, "excess") is True


def test_no_conflict_when_basis_is_stated_or_not_excess():
    r = v1.nmax(RISING_80)
    assert v1.basis_shape_conflict(r, True, "excess") is False
    assert v1.basis_shape_conflict(r, False, "absolute") is False


def test_no_conflict_below_60_bar_or_with_observed_maximum():
    r = v1.nmax(iso((5, 2.0), (35, 4.0), (50, 4.5)))
    assert v1.basis_shape_conflict(r, False, "excess") is False
    r = v1.nmax(iso((5, 2.0), (30, 5.0), (56, 4.0), (80, 4.5)))
    assert r.nmax_status == "observed_max"
    assert v1.basis_shape_conflict(r, False, "excess") is False


def test_conflict_threshold_is_a_rise_of_more_than_3_percent():
    # 0.7 x 100 = 70 bar sits on a point of 4.0.
    below = v1.nmax(iso((5, 2.0), (70, 4.0), (100, 4.116)))  # +2.9%
    above = v1.nmax(iso((5, 2.0), (70, 4.0), (100, 4.124)))  # +3.1%
    assert v1.basis_shape_conflict(below, False, "excess") is False
    assert v1.basis_shape_conflict(above, False, "excess") is True


def test_conflict_is_null_for_uncoded_basis():
    assert v1.basis_shape_conflict(v1.nmax(RISING_80), None, "excess") is None


# ---------------------------------------------------------------------------
# Rows, isotherms and dataset-level fields
# ---------------------------------------------------------------------------


def coded_row(**over):
    base = {
        "paper_id": "HYC-9001",
        "measurement_id": "HYC-9001-M1",
        "sample_id": "S1",
        "temperature_k": 77.0,
        "pressure_bar": 20.0,
        "uptake_wt_pct": 5.0,
        "uptake_mmol_g": None,
        "uptake_ml_stp_g": None,
        "wt_pct_convention": "W1",
        "measurement_mode": "isothermal",
        "uptake_bound": "exact",
        "isotherm_branch": "adsorption",
        "pressure_unstated": "False",
        "temperature_unstated": "False",
        "extraction_method": "table_direct",
        "uncertainty_wt_pct": None,
        "digitization_uncertainty_wt_pct": None,
        "basis_stated": "True",
        "basis_inferred": "excess",
        "temperature_inferred": "False",
        "instrument_identified": "True",
        "calibration_described": "True",
        "replicates_reported": "True",
        "surface_area_method": "BET",
        "surface_area_probe_gas": "N2",
        "area_same_sample": "yes",
        "bet_surface_area_m2_g": 2500.0,
        "total_pore_volume_cm3_g": 1.2,
        "micropore_volume_cm3_g": None,
        "micropore_volume_co2_cm3_g": None,
        "pore_volume_method": "DR",
        "degas_temperature_c": 200.0,
        "degas_duration_h": 12.0,
        "degas_end_pressure_pa": None,
        "isotherm_point_count": 12,
        "isotherm_id": None,
        "value_kind": "measured",
        "measuring_lab_id": "LAB1",
    }
    base.update(over)
    return base


def test_point_uncertainty_uses_digitization_uncertainty_for_figure_points():
    fig = coded_row(
        extraction_method="figure_digitized",
        uncertainty_wt_pct=0.5,
        digitization_uncertainty_wt_pct=0.05,
    )
    assert v1.point_uncertainty(fig) == 0.05
    assert v1.point_uncertainty(coded_row(uncertainty_wt_pct=0.2)) == 0.2
    assert v1.point_uncertainty(coded_row()) == 0.0


def test_row_without_isotherm_id_is_its_own_isotherm():
    assert v1.isotherm_key(coded_row()) == "HYC-9001|row:HYC-9001-M1"
    assert v1.isotherm_key(coded_row(isotherm_id="I1")) == "HYC-9001|I1"


def isotherm_rows(points, iso_id="I1", sample="S1", **over):
    return [
        coded_row(
            measurement_id=f"HYC-9001-{iso_id}-{i}",
            isotherm_id=iso_id,
            sample_id=sample,
            pressure_bar=p,
            uptake_wt_pct=v,
            **over,
        )
        for i, (p, v) in enumerate(points)
    ]


def test_isotherm_table_classifies_and_filters_points():
    rows = isotherm_rows([(5, 3.0), (20, 5.0), (30, 4.9), (40, 4.8)])
    # A desorption point higher than the maximum must not count.
    rows.append(
        coded_row(
            measurement_id="HYC-9001-D",
            isotherm_id="I1",
            pressure_bar=35,
            uptake_wt_pct=6.0,
            isotherm_branch="desorption",
        )
    )
    # A lower-bound point must not count either.
    rows.append(
        coded_row(
            measurement_id="HYC-9001-L",
            isotherm_id="I1",
            pressure_bar=36,
            uptake_wt_pct=7.0,
            uptake_bound="lower",
        )
    )
    t = v1.isotherm_table(pd.DataFrame(rows))
    assert len(t) == 1
    rec = t.iloc[0]
    assert rec.nmax_status == "observed_max"
    assert rec.n_ex_max_wt_pct == 5.0 and rec.p_at_nmax_bar == 20 and rec.n_points == 4


def test_isotherm_table_uses_w1():
    rows = isotherm_rows([(20, 5.0), (40, 4.0)], wt_pct_convention="W2")
    rec = v1.isotherm_table(pd.DataFrame(rows)).iloc[0]
    assert rec.n_ex_max_wt_pct == pytest.approx(5.0 / 0.95)


def test_isotherm_table_skips_non_77k_and_non_excess_and_uncoded():
    rows = (
        isotherm_rows([(20, 1.0), (40, 1.2)], iso_id="RT", temperature_k=298.0)
        + isotherm_rows([(20, 5.0), (40, 6.0)], iso_id="ABS", basis_inferred="absolute")
        + isotherm_rows([(20, 5.0), (40, 6.0)], iso_id="UNC", basis_stated=None)
    )
    assert v1.isotherm_table(pd.DataFrame(rows)).empty


def test_isotherm_mixing_samples_is_an_error():
    rows = isotherm_rows([(20, 5.0)]) + isotherm_rows([(40, 4.0)], sample="S2")
    for i, r in enumerate(rows):
        r["measurement_id"] = f"HYC-9001-X{i}"
    with pytest.raises(ValueError, match="mixes samples"):
        v1.isotherm_table(pd.DataFrame(rows))


def test_isotherm_mixing_temperatures_or_bases_is_an_error():
    rows = isotherm_rows([(20, 5.0), (40, 4.0)])
    rows[1]["temperature_k"] = 87.0
    with pytest.raises(ValueError, match="mixes 77 K"):
        v1.isotherm_table(pd.DataFrame(rows))
    rows = isotherm_rows([(20, 5.0), (40, 4.0)])
    rows[1]["basis_stated"] = "False"
    with pytest.raises(ValueError, match="mixes bases"):
        v1.isotherm_table(pd.DataFrame(rows))


def test_add_computed_fields_broadcasts_and_leaves_uncoded_rows_null():
    rows = isotherm_rows([(5, 3.0), (20, 5.0), (40, 4.8)])
    rows.append(coded_row(measurement_id="HYC-9001-U", basis_stated=None))
    out = v1.add_computed_fields(pd.DataFrame(rows))
    assert list(out["nmax_status"][:3]) == ["observed_max"] * 3
    assert list(out["p_at_nmax_bar"][:3]) == [20, 20, 20]
    u = out.iloc[3]
    for field in v1.COMPUTED_ROW_FIELDS:
        assert pd.isna(u[field]), field
    assert set(v1.COMPUTED_ROW_FIELDS) <= set(out.columns)


def test_current_dataset_is_uncoded_so_every_computed_field_is_null():
    from hycan.load import load_dataset

    out = v1.add_computed_fields(load_dataset())
    for field in v1.COMPUTED_ROW_FIELDS:
        assert out[field].isna().all(), field


# ---------------------------------------------------------------------------
# §10.1 reporting-completeness score
# ---------------------------------------------------------------------------


def test_complete_row_scores_9_and_tier_a():
    items = v1.reporting_items(coded_row())
    assert len(items) == 9 and all(items.values())
    assert v1.reporting_score(coded_row()) == 9
    assert v1.reporting_tier(9) == "A"


@pytest.mark.parametrize(
    ("change", "item"),
    [
        ({"basis_stated": "False"}, "1_basis_stated"),
        ({"temperature_inferred": "True"}, "2_temperature_stated"),
        ({"temperature_unstated": "True"}, "2_temperature_stated"),
        ({"pressure_unstated": "True"}, "3_pressure_stated"),
        ({"surface_area_probe_gas": "unspecified"}, "4_area_method_and_gas"),
        ({"surface_area_method": "unspecified"}, "4_area_method_and_gas"),
        ({"pore_volume_method": "unspecified"}, "5_pore_volume_with_method"),
        ({"total_pore_volume_cm3_g": None}, "5_pore_volume_with_method"),
        ({"degas_duration_h": None}, "6_degassing"),
        ({"degas_temperature_c": None}, "6_degassing"),
        ({"calibration_described": "False"}, "7_instrument_and_calibration"),
        ({"instrument_identified": "False"}, "7_instrument_and_calibration"),
        ({"replicates_reported": "False"}, "8_uncertainty_or_replicates"),
        ({"isotherm_point_count": 4}, "9_isotherm_points"),
        ({"isotherm_point_count": None}, "9_isotherm_points"),
    ],
)
def test_each_item_is_lost_alone(change, item):
    items = v1.reporting_items(coded_row(**change))
    assert [k for k, v in items.items() if not v] == [item]
    assert v1.reporting_score(coded_row(**change)) == 8


def test_alternatives_within_items():
    # Item 5: a micropore volume also counts. Item 6: end vacuum replaces duration.
    # Item 8: a numerical uncertainty replaces replicates.
    row = coded_row(
        total_pore_volume_cm3_g=None,
        micropore_volume_cm3_g=0.6,
        degas_duration_h=None,
        degas_end_pressure_pa=1e-3,
        replicates_reported="False",
        uncertainty_wt_pct=0.1,
    )
    assert v1.reporting_score(row) == 9


@pytest.mark.parametrize(
    ("score", "tier"),
    [
        (9, "A"),
        (8, "A"),
        (7, "B"),
        (6, "B"),
        (5, "C"),
        (4, "C"),
        (3, "D"),
        (0, "D"),
        (None, None),
    ],
)
def test_tier_thresholds(score, tier):
    assert v1.reporting_tier(score) == tier


def test_score_does_not_depend_on_the_uptake():
    for uptake in (0.1, 5.0, 19.0):
        assert v1.reporting_score(coded_row(uptake_wt_pct=uptake)) == 9


def test_score_withheld_for_uncoded_row_or_uncoded_boolean():
    assert v1.reporting_score(coded_row(basis_stated=None)) is None
    assert v1.reporting_score(coded_row(instrument_identified=None)) is None


# ---------------------------------------------------------------------------
# §11.0 area rule
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("change", "eligible"),
    [
        ({}, True),
        ({"surface_area_probe_gas": "Ar"}, True),
        ({"surface_area_probe_gas": "unspecified"}, True),
        ({"surface_area_probe_gas": "CO2"}, False),
        ({"surface_area_probe_gas": None}, False),
        ({"surface_area_method": "Langmuir"}, False),
        ({"surface_area_method": "unspecified"}, False),
        ({"area_same_sample": "parent_material"}, False),
        ({"area_same_sample": "unclear"}, False),
        ({"bet_surface_area_m2_g": None}, False),
        ({"bet_surface_area_m2_g": 0.0}, False),
    ],
)
def test_area_rule(change, eligible):
    area = v1.eligible_bet_area(coded_row(**change))
    assert (area is not None) is eligible


# ---------------------------------------------------------------------------
# §10.2 plausibility screen
# ---------------------------------------------------------------------------


def test_77k_area_bound():
    # A_BET 1000 -> bound 2 x 2 + 0.5 = 4.5 wt%
    assert v1.plausibility_flag(
        coded_row(bet_surface_area_m2_g=1000.0, uptake_wt_pct=4.6)
    )
    assert not v1.plausibility_flag(
        coded_row(bet_surface_area_m2_g=1000.0, uptake_wt_pct=4.4)
    )


def test_77k_cap_applies_without_an_area():
    row = coded_row(surface_area_method="Langmuir", uptake_wt_pct=10.1)
    assert v1.plausibility_flag(row) is True
    row = coded_row(surface_area_method="Langmuir", uptake_wt_pct=9.0)
    assert v1.plausibility_flag(row) is False


def test_room_temperature_bound_up_to_100_bar():
    rt = {"temperature_k": 298.0, "pressure_bar": 100.0}
    assert v1.plausibility_flag(coded_row(uptake_wt_pct=1.6, **rt)) is True
    assert v1.plausibility_flag(coded_row(uptake_wt_pct=1.4, **rt)) is False
    assert (
        v1.plausibility_flag(
            coded_row(uptake_wt_pct=1.6, temperature_k=298.0, pressure_bar=150.0)
        )
        is None
    )


def test_other_temperatures_are_not_screenable():
    assert v1.plausibility_flag(coded_row(temperature_k=150.0)) is None


def test_total_basis_adds_the_pore_gas_and_needs_v_total():
    v_total = 1.2
    extra = 100 * v1.h2_density_g_cm3(77.0, 100.0) * v_total
    area_bound = 2 * 1000 / 500 + 0.5  # below the 10 wt% cap
    common = {
        "bet_surface_area_m2_g": 1000.0,
        "pressure_bar": 100.0,
        "total_pore_volume_cm3_g": v_total,
    }
    total = {"basis_inferred": "total", **common}
    excess = {"basis_inferred": "excess", **common}
    middle = area_bound + extra / 2
    assert v1.plausibility_flag(coded_row(uptake_wt_pct=middle, **excess)) is True
    assert v1.plausibility_flag(coded_row(uptake_wt_pct=middle, **total)) is False
    assert (
        v1.plausibility_flag(
            coded_row(uptake_wt_pct=area_bound + extra + 0.01, **total)
        )
        is True
    )
    no_v = {**total, "total_pore_volume_cm3_g": None}
    assert v1.plausibility_flag(coded_row(uptake_wt_pct=5.0, **no_v)) is None


def test_normal_hydrogen_density_at_77k():
    # Leachman et al. 2009 normal hydrogen, 77 K and 30 bar: about 9.8 kg/m3.
    assert v1.h2_density_g_cm3(77.0, 30.0) == pytest.approx(0.00982, rel=0.01)


def test_non_isothermal_and_uncoded_rows_are_not_screened():
    assert v1.plausibility_flag(coded_row(measurement_mode="TPD")) is None
    assert v1.plausibility_flag(coded_row(basis_stated=None)) is None


def test_as_bool_reads_csv_strings():
    assert v1.as_bool("True") is True and v1.as_bool("false") is False
    assert v1.as_bool(None) is None and v1.as_bool(math.nan) is None
    with pytest.raises(ValueError):
        v1.as_bool("yes")
