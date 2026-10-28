"""Tests for scripts/v1_extract.py: the §9 matching rule and figure values."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_extract", REPO_ROOT / "scripts" / "v1_extract.py"
)
ve = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ve
spec.loader.exec_module(ve)


def row(mid, label="AC-800", t="77", p="20", wt="5.0", **kw):
    r = {
        "measurement_id": mid,
        "material_description": f"{label} | KOH-activated carbon",
        "temperature_k": t,
        "pressure_bar": p,
        "uptake_wt_pct": wt,
        "isotherm_branch": "adsorption",
        "extraction_method": "table_direct",
    }
    r.update(kw)
    return r


def ids(pairs):
    return [
        ((p.first or {}).get("measurement_id"), (p.second or {}).get("measurement_id"))
        for p in pairs
    ]


def test_labels_match_after_normalization():
    assert ve.norm_label("AC-800 | x") == ve.norm_label("ac 800 | y") == "ac800"
    assert ve.norm_label("AC‐800 | x") == "ac800"  # Unicode hyphen
    assert ve.norm_label("AC-800 | x") != ve.norm_label("AC-900 | x")
    assert ve.norm_label("Co-CA (1050°C) | x") == ve.norm_label("Co-CA-1050°C | y")


@pytest.mark.parametrize(
    ("p1", "p2", "ok"),
    [
        ("20", "20.39", True),
        ("20", "20.41", False),
        ("0.5", "0.52", True),
        ("0.5", "0.53", False),
        ("1", "1.02", True),
    ],
)
def test_pressure_tolerance_is_larger_of_2_percent_and_0_02_bar(p1, p2, ok):
    assert ve.within_pressure(float(p1), float(p2)) is ok


def test_temperature_tolerance_is_1_k():
    assert ve.within_temperature(77.0, 77.3) and ve.within_temperature(77.0, 78.0)
    assert not ve.within_temperature(77.0, 78.1)


def test_match_pairs_by_label_conditions_and_quantity():
    first = [row("A1"), row("A2", p="40"), row("A3", label="AC-900")]
    second = [
        row("B1", p="40.3"),
        row("B2", p="20.1"),
        row("B3", label="AC-900", t="298"),
    ]
    assert sorted(ids(ve.match(first, second)), key=str) == sorted(
        [("A1", "B2"), ("A2", "B1"), ("A3", None), (None, "B3")], key=str
    )


def test_quantity_must_agree():
    first = [row("A1")]
    second = [row("B1", wt="", volumetric_capacity_kg_m3="30")]
    assert sorted(ids(ve.match(first, second)), key=str) == sorted(
        [("A1", None), (None, "B1")], key=str
    )


def test_each_row_is_matched_once_and_same_branch_is_preferred():
    first = [row("A1", p="20", isotherm_branch="desorption"), row("A2", p="20")]
    second = [row("B1", p="20.1")]
    assert ("A2", "B1") in ids(ve.match(first, second))


def test_match_lines_list_differing_fields_and_ignore_provenance():
    a = row("A1", notes="from Table 2", basis_inferred="excess")
    b = row("B1", notes="Table 2, row 3", basis_inferred="unknown")
    pairs = ve.match([a], [b])
    lines = ve.match_lines(pairs, list(a.keys()))
    assert [(x["status"], x["field"]) for x in lines] == [("differ", "basis_inferred")]


def test_agreeing_pair_gets_one_agree_line():
    lines = ve.match_lines(ve.match([row("A1")], [row("B1")]), list(row("x").keys()))
    assert [(x["status"], x["field"]) for x in lines] == [("agree", "")]


def test_figure_values_agree_within_3_percent_but_table_values_must_be_equal():
    fa = row("A1", wt="5.00", extraction_method="figure_digitized")
    fb = row("B1", wt="5.10", extraction_method="figure_digitized")
    assert ve.values_agree("uptake_wt_pct", fa, fb)
    assert not ve.values_agree(
        "uptake_wt_pct", row("A1", wt="5.00"), row("B1", wt="5.01")
    )
    assert ve.values_agree("uptake_wt_pct", row("A1", wt="5.0"), row("B1", wt="5.00"))
    assert ve.values_agree(
        "basis_stated", row("A", basis_stated="True"), row("B", basis_stated="true")
    )


def archive(dirpath: Path, name: str, y1: float, y2: float) -> None:
    dirpath.mkdir(parents=True, exist_ok=True)
    (dirpath / name).write_text(
        json.dumps(
            {
                "calibration": {
                    "y": {
                        "reference_1": {"pixel": 500, "value": y1},
                        "reference_2": {"pixel": 100, "value": y2},
                    }
                }
            }
        )
    )


def test_dual_figure_value_is_mean_with_section_9_uncertainty(tmp_path):
    archive(tmp_path / "a", "fa.json", 0, 6)
    archive(tmp_path / "b", "fb.json", 0, 6)
    a = row(
        "A1", wt="5.00", extraction_method="figure_digitized", notes="archive: fa.json"
    )
    b = row(
        "B1", wt="5.20", extraction_method="figure_digitized", notes="archive: fb.json"
    )
    out = ve.figure_values(
        ve.match([a], [b]), tmp_path / "a", tmp_path / "b", legacy=False
    )
    assert float(out[0]["value"]) == pytest.approx(5.10)
    # max(half difference 0.10, 1% of a 6 wt% span 0.06) = 0.10
    assert float(out[0]["digitization_uncertainty_wt_pct"]) == pytest.approx(0.10)
    b2 = dict(b, uptake_wt_pct="5.02")
    out = ve.figure_values(
        ve.match([a], [b2]), tmp_path / "a", tmp_path / "b", legacy=False
    )
    assert float(out[0]["digitization_uncertainty_wt_pct"]) == pytest.approx(0.06)


def test_figure_uncertainty_is_converted_to_wt_pct(tmp_path):
    archive(tmp_path / "a", "fa.json", 0, 30)
    archive(tmp_path / "b", "fb.json", 0, 30)
    a = row(
        "A1",
        wt="",
        uptake_mmol_g="25.0",
        extraction_method="figure_digitized",
        notes="archive: fa.json",
    )
    b = row(
        "B1",
        wt="",
        uptake_mmol_g="25.1",
        extraction_method="figure_digitized",
        notes="archive: fb.json",
    )
    out = ve.figure_values(
        ve.match([a], [b]), tmp_path / "a", tmp_path / "b", legacy=False
    )
    assert out[0]["uptake_field"] == "uptake_mmol_g"
    assert float(out[0]["digitization_uncertainty_wt_pct"]) == pytest.approx(
        0.3 * 0.201588
    )


def test_legacy_figure_value_is_b_with_1_percent_of_span(tmp_path):
    archive(tmp_path / "b", "fb.json", 0, 5)
    v01 = row("M1", wt="4.9", extraction_method="figure_digitized")
    b = row(
        "B1", wt="5.0", extraction_method="figure_digitized", notes="archive: fb.json"
    )
    out = ve.figure_values(
        ve.match([v01], [b]), tmp_path / "a", tmp_path / "b", legacy=True
    )
    assert float(out[0]["value"]) == 5.0
    assert float(out[0]["digitization_uncertainty_wt_pct"]) == pytest.approx(0.05)


def test_free_text_compared_on_presence_and_doi_case_insensitively():
    a = row(
        "A1", material_identity="Norit, Darco G-60", doi="10.1016/S0008-6223(01)00051-3"
    )
    b = row(
        "B1",
        material_identity="Norit Darco activated carbon G-60",
        doi="10.1016/s0008-6223(01)00051-3",
    )
    assert ve.values_agree("material_identity", a, b)
    assert ve.values_agree("doi", a, b)
    assert not ve.values_agree("material_identity", a, row("B2", material_identity=""))


def test_legacy_labels_come_from_labels_csv(tmp_path):
    labels = tmp_path / "labels.csv"
    labels.write_text(
        "sample_id,measurement_ids,label,evidence\n"
        "HYC-0099-S1,,ACA-2550,Table 1\n"
        "HYC-0099-S2,HYC-0099-M3,CMS / lab 2,Table 2\n"
        "HYC-0099-S2,HYC-0099-M4,CMS / lab 3,Table 2\n",
        encoding="utf-8",
    )
    lab = ve.read_labels(labels)
    v01 = [
        {**row("HYC-0099-M1"), "sample_id": "HYC-0099-S1",
         "material_description": "carbon aerogel, 2550 m2/g"},
        {**row("HYC-0099-M3"), "sample_id": "HYC-0099-S2",
         "material_description": "round robin CMS"},
        {**row("HYC-0099-M4"), "sample_id": "HYC-0099-S2",
         "material_description": "round robin CMS"},
    ]
    b = [row("B1", label="ACA 2550"), row("B2", label="CMS / lab 3")]
    assert sorted(ids(ve.match(v01, b, lab)), key=str) == sorted(
        [("HYC-0099-M1", "B1"), ("HYC-0099-M4", "B2"), ("HYC-0099-M3", None)],
        key=str,
    )
    # without the labels nothing matches: v0.1 descriptions carry no label
    assert all(p.first is None or p.second is None for p in ve.match(v01, b))


def test_legacy_mode_skips_v2_fields_empty_on_the_v01_side():
    v01 = row("M1", basis_inferred="", uptake_type="excess")
    b = row("B1", basis_inferred="excess", uptake_type="unspecified")
    cols = list(v01.keys())
    pairs = ve.match([v01], [b])
    legacy = [x["field"] for x in ve.match_lines(pairs, cols, legacy=True)]
    dual = [x["field"] for x in ve.match_lines(pairs, cols)]
    assert legacy == ["uptake_type"]
    assert sorted(dual) == ["basis_inferred", "uptake_type"]


def test_single_digitization_gets_one_percent_of_its_span(tmp_path):
    archive(tmp_path / "a", "fa.json", 0, 8)
    a = row(
        "A1", wt="5.00", extraction_method="figure_digitized", notes="archive: fa.json"
    )
    out = ve.figure_values(ve.match([a], []), tmp_path / "a", tmp_path / "b", False)
    assert out[0]["from"] == "first"
    assert float(out[0]["digitization_uncertainty_wt_pct"]) == pytest.approx(0.08)
    # a digitized point matched to a table value: the digitized side only
    t = row("B1", wt="5.02")
    out = ve.figure_values(ve.match([a], [t]), tmp_path / "a", tmp_path / "b", False)
    assert [e["from"] for e in out] == ["first"]


def test_computed_wt_pct_uses_the_printed_unit_for_figure_values(tmp_path):
    archive(tmp_path / "a", "fa.json", 0, 30)
    archive(tmp_path / "b", "fb.json", 0, 30)
    kw = {
        "extraction_method": "figure_digitized",
        "wt_pct_convention": "W1",
        "wt_pct_convention_source": "computed_from_other_unit",
    }
    a = row("A1", wt=repr(25.0 * 0.201588), uptake_mmol_g="25.0",
            notes="archive: fa.json", **kw)
    b = row("B1", wt=repr(25.2 * 0.201588), uptake_mmol_g="25.2",
            notes="archive: fb.json", **kw)
    out = ve.figure_values(ve.match([a], [b]), tmp_path / "a", tmp_path / "b", False)
    assert out[0]["uptake_field"] == "uptake_mmol_g"
    assert float(out[0]["value"]) == pytest.approx(25.1)


def test_a_digitized_pressure_on_a_table_row_is_compared_within_3_percent():
    a = row("A1", p="29.4", notes="pressure digitized; archive: fa.json")
    b = row("B1", p="30.0", notes="pressure digitized; archive: fb.json")
    assert ve.values_agree("pressure_bar", a, b)
    assert not ve.values_agree("pressure_bar", row("A", p="29.4"), row("B", p="30.0"))
    # the uptake of those rows is printed, so it must be equal
    assert not ve.values_agree("uptake_wt_pct", dict(a, uptake_wt_pct="5.0"),
                               dict(b, uptake_wt_pct="5.1"))


def test_prepare_refuses_inputs_that_share_a_parent(tmp_path):
    paper = tmp_path / "paper.json"
    paper.write_text('{"paper_id": "HYC-9999"}', encoding="utf-8")
    rc = ve.main([
        "prepare", "--paper-json", str(paper), "--pdf", str(tmp_path / "x.pdf"),
        "--out-a", str(tmp_path / "p" / "A"), "--out-b", str(tmp_path / "p" / "B"),
        "--out-c", str(tmp_path / "q" / "C"),
    ])
    assert rc == 1


def test_axis_span_uses_the_uptake_axis_of_a_pressure_composition_plot(tmp_path):
    d = tmp_path / "a"
    d.mkdir()
    (d / "pct.json").write_text(json.dumps({
        "calibration": {
            "x": {"label": "Wt.%_H", "reference_1": {"value": 1.0},
                  "reference_2": {"value": 9.0}},
            "y": {"label": "Pressure_(atm)", "reference_1": {"value": 0.0},
                  "reference_2": {"value": 20.0}},
        },
        "series": [{"x": 5.25, "y": 12.0}],
    }))
    r = row("A1", wt="5.25", extraction_method="figure_digitized",
            notes="archive: pct.json")
    assert ve.axis_span(d, r) == pytest.approx(8.0)
    # no exact point: the label decides
    assert ve.axis_span(d, dict(r, uptake_wt_pct="5.3")) == pytest.approx(8.0)


def test_legacy_v01_row_without_pressure_matches_a_digitized_pressure():
    v01 = row("M1", p="", wt="5.0")
    b = row("B1", p="30.4", wt="5.0", notes="pressure digitized; archive: f.json")
    assert ids(ve.match([v01], [b], legacy=True)) == [("M1", "B1")]
    assert ("M1", "B1") not in ids(ve.match([v01], [b]))
    # a printed pressure on the B side does not qualify
    assert ("M1", "B2") not in ids(ve.match([v01], [row("B2", p="30.4")], legacy=True))


def test_mg_per_g_axis_span_is_scaled_to_w1(tmp_path):
    d = tmp_path / "a"
    archive(d, "mg.json", 0, 50)
    r = row("A1", wt="2.5", extraction_method="figure_digitized",
            notes="archive: mg.json", wt_pct_convention="W1",
            wt_pct_convention_source="computed_from_other_unit")
    assert ve.axis_span(d, r) == pytest.approx(5.0)


def test_check_flags_an_isotherm_with_mixed_basis():
    rows = [row("A1", isotherm_id="I1", basis_inferred="excess"),
            row("A2", isotherm_id="I1", basis_inferred="unknown")]
    mixed = {k for k, v in ve._per_isotherm(rows, ve.ISOTHERM_CONSTANT).items()
             if len(v) > 1}
    assert mixed == {"I1"}
