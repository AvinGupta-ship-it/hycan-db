"""Unit tests for scripts/validate_row_detail.py (manual v2.0 §18 Phase A.1)."""

from __future__ import annotations

import pandas as pd
import pytest
import validate_row_detail as detail
from conftest import make_row, write_csv

from hycan.validate import validate_dataset

# ---------------------------------------------------------------------------
# Message -> field mapping
# ---------------------------------------------------------------------------

def test_category_of_splits_on_first_colon():
    assert detail.category_of("Duplicate measurement_id: HYC-1-M1") == (
        "Duplicate measurement_id"
    )
    assert detail.category_of("Unspecified uptake_type") == "Unspecified uptake_type"


def test_fields_for_reads_the_field_out_of_the_message():
    assert detail.fields_for("Missing required field: uptake_type") == ("uptake_type",)
    assert detail.fields_for("Invalid value: material_class") == ("material_class",)


def test_fields_for_uses_the_table_for_the_rest():
    assert detail.fields_for("Temperature out of range") == ("temperature_k",)
    assert detail.fields_for("mmol/g and wt% inconsistent") == (
        "uptake_wt_pct",
        "uptake_mmol_g",
    )


def test_unknown_category_degrades_instead_of_raising():
    assert detail.fields_for("Some rule added later") == (detail.UNMAPPED,)


# Rows engineered to trigger every message category the validator can emit.
# If validate.py grows a rule, this list stops being exhaustive and the
# coverage test below is the thing that should be updated alongside
# CATEGORY_FIELDS -- which is the point of having it.
TRIGGERS = [
    ("Missing required field", [make_row(temperature_k=None)]),
    ("Invalid value", [make_row(material_class="nanofluff")]),
    ("Temperature out of range", [make_row(temperature_k=600.0)]),
    ("Pressure out of range", [make_row(pressure_bar=0.0)]),
    ("Pressure above 200 bar", [make_row(pressure_bar=250.0)]),
    ("Uptake out of range", [make_row(uptake_wt_pct=25.0)]),
    ("Uptake above 10 wt%", [make_row(uptake_wt_pct=12.0)]),
    ("Unspecified uptake_type", [make_row(uptake_type="unspecified")]),
    (
        "Micropore volume exceeds total pore volume",
        [make_row(micropore_volume_cm3_g=1.2, total_pore_volume_cm3_g=0.8)],
    ),
    (
        "SWCNT description missing 'single-walled'",
        [make_row(material_class="SWCNT", material_description="nanotube sample")],
    ),
    (
        "mmol/g and wt% inconsistent",
        [make_row(uptake_wt_pct=1.5, uptake_mmol_g=40.0)],
    ),
    (
        "Pre-2005 raw-CNT high uptake (Tier D)",
        [
            make_row(
                year=2002,
                material_class="SWCNT",
                material_description="single-walled nanotubes",
                uptake_wt_pct=8.0,
            )
        ],
    ),
    (
        "Duplicate measurement_id",
        [make_row(), make_row()],
    ),
    (
        "DOI metadata conflict",
        [make_row(measurement_id="HYC-9001-M1"),
         make_row(measurement_id="HYC-9001-M2", first_author="Other")],
    ),
]


@pytest.mark.parametrize("category,rows", TRIGGERS, ids=[t[0] for t in TRIGGERS])
def test_every_emitted_category_maps_to_a_field(category, rows):
    """No category the validator emits may render as (unmapped)."""
    report = validate_dataset(pd.DataFrame(rows))
    messages = [m for r in report.results for m in (r.errors + r.warnings)]
    matching = [m for m in messages if detail.category_of(m) == category]
    assert matching, f"trigger row did not produce {category!r}; got {messages}"
    for message in matching:
        assert detail.fields_for(message) != (detail.UNMAPPED,)


def test_describe_names_the_field_and_shows_its_value():
    row = make_row(temperature_k=600.0)
    text = detail.describe("Temperature out of range", row)
    assert "temperature_k=600.0" in text


def test_describe_marks_an_empty_cell():
    row = make_row(uptake_type=None)
    text = detail.describe("Missing required field: uptake_type", row)
    assert "uptake_type=<empty>" in text


# ---------------------------------------------------------------------------
# Row identity
# ---------------------------------------------------------------------------

def test_line_numbers_reliable_for_an_ordinary_file(clean_dataset):
    assert detail.line_numbers_are_reliable(str(clean_dataset), 3) is True


def test_line_numbers_unreliable_when_a_field_holds_a_newline(tmp_path):
    path = write_csv(
        tmp_path / "newline.csv",
        [make_row(notes="first line\nsecond line")],
    )
    assert detail.line_numbers_are_reliable(str(path), 1) is False


def test_row_label_offsets_index_to_csv_line():
    label = detail.row_label(0, make_row(), with_line=True)
    assert "csv line 2" in label and "df_index 0" in label
    assert "HYC-9001-M1" in label and "paper HYC-9001" in label


def test_row_label_omits_line_when_unreliable():
    assert "csv line" not in detail.row_label(0, make_row(), with_line=False)


# ---------------------------------------------------------------------------
# Command-line behaviour
# ---------------------------------------------------------------------------

def run(argv, capsys):
    code = detail.main(["validate_row_detail.py"] + argv)
    return code, capsys.readouterr().out


def test_clean_dataset_exits_zero(clean_dataset, capsys):
    code, out = run([str(clean_dataset)], capsys)
    assert code == 0
    assert "Rows reported: 0" in out


def test_error_exits_one_and_names_the_field(tmp_path, capsys):
    path = write_csv(
        tmp_path / "bad.csv",
        [make_row(), make_row(measurement_id="HYC-9001-M2", temperature_k=600.0)],
    )
    code, out = run([str(path)], capsys)
    assert code == 1
    assert "ERROR" in out
    assert "temperature_k=600.0" in out
    assert "HYC-9001-M2" in out


def test_warnings_alone_exit_zero(tmp_path, capsys):
    path = write_csv(tmp_path / "warn.csv", [make_row(uptake_type="unspecified")])
    code, out = run([str(path)], capsys)
    assert code == 0
    assert "WARNING" in out and "Unspecified uptake_type" in out


def test_errors_only_suppresses_warnings(tmp_path, capsys):
    path = write_csv(
        tmp_path / "mixed.csv",
        [make_row(temperature_k=600.0, uptake_type="unspecified")],
    )
    code, out = run([str(path), "--errors-only"], capsys)
    assert code == 1
    assert "WARNING" not in out


def test_field_filter_selects_one_field(tmp_path, capsys):
    path = write_csv(
        tmp_path / "mixed.csv",
        [make_row(pressure_bar=250.0, uptake_type="unspecified")],
    )
    code, out = run([str(path), "--field", "pressure_bar"], capsys)
    assert code == 0
    assert "Pressure above 200 bar" in out
    assert "Unspecified uptake_type" not in out


def test_paper_filter_selects_one_paper(tmp_path, capsys):
    path = write_csv(
        tmp_path / "two.csv",
        [
            make_row(uptake_type="unspecified"),
            make_row(
                paper_id="HYC-9002",
                doi="10.1016/j.carbon.2016.01.002",
                sample_id="HYC-9002-S1",
                measurement_id="HYC-9002-M1",
                uptake_type="unspecified",
            ),
        ],
    )
    code, out = run([str(path), "--paper", "HYC-9002"], capsys)
    assert code == 0
    assert "Rows reported: 1" in out
    assert "HYC-9002-M1" in out and "HYC-9001-M1" not in out


def test_category_filter_is_case_insensitive_substring(tmp_path, capsys):
    path = write_csv(tmp_path / "warn.csv", [make_row(uptake_type="unspecified")])
    code, out = run([str(path), "--category", "unspecified uptake"], capsys)
    assert code == 0
    assert "Unspecified uptake_type" in out


def test_summary_lists_categories_and_ids(tmp_path, capsys):
    path = write_csv(
        tmp_path / "warn.csv",
        [
            make_row(uptake_type="unspecified"),
            make_row(measurement_id="HYC-9001-M2", uptake_type="unspecified"),
        ],
    )
    code, out = run([str(path), "--summary"], capsys)
    assert code == 0
    assert "Unspecified uptake_type (uptake_type): 2" in out
    assert "HYC-9001-M1" in out and "HYC-9001-M2" in out


def test_limit_suppresses_the_tail(tmp_path, capsys):
    rows = [
        make_row(measurement_id=f"HYC-9001-M{n}", uptake_type="unspecified")
        for n in range(1, 5)
    ]
    path = write_csv(tmp_path / "many.csv", rows)
    code, out = run([str(path), "--limit", "2"], capsys)
    assert code == 0
    assert "2 more rows suppressed" in out


def test_no_dataset_checks_drops_the_duplicate_check(tmp_path, capsys):
    path = write_csv(tmp_path / "dup.csv", [make_row(), make_row()])

    code, out = run([str(path)], capsys)
    assert code == 1
    assert "Duplicate measurement_id" in out

    code, out = run([str(path), "--no-dataset-checks"], capsys)
    assert code == 0
    assert "Duplicate measurement_id" not in out
    assert "Dataset-level checks skipped" in out


def test_missing_file_exits_two(tmp_path, capsys):
    code, out = run([str(tmp_path / "nope.csv")], capsys)
    assert code == 2
    assert "not found" in out


def test_contradictory_flags_exit_two(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--errors-only", "--warnings-only"], capsys)
    assert code == 2
    assert "mutually exclusive" in out


def test_quoted_comma_survives_the_read(tmp_path, capsys):
    """The notes field holds a comma; it must stay one field (§6.7, §B.3)."""
    path = write_csv(
        tmp_path / "comma.csv",
        [make_row(notes="Reported as 1.5 wt%, see caption", temperature_k=600.0)],
    )
    frame = pd.read_csv(path)
    assert len(frame.columns) == 38
    assert frame.loc[0, "notes"] == "Reported as 1.5 wt%, see caption"
    code, _ = run([str(path)], capsys)
    assert code == 1


# ---------------------------------------------------------------------------
# Exit code reflects the SELECTED rows, not the whole file
#
# An isolated audit found the exit code was derived from the unfiltered
# results, so every filtered invocation was a false failure.
# ---------------------------------------------------------------------------

def _mixed(tmp_path):
    """One paper with an error, one clean paper with a warning."""
    rows = [
        make_row(paper_id="HYC-9001", measurement_id="HYC-9001-M1",
                 temperature_k=None),                       # ERROR
        make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                 measurement_id="HYC-9002-M1",
                 doi="10.1016/j.carbon.2016.04.002",
                 uptake_type="unspecified"),                # WARNING only
    ]
    return write_csv(tmp_path / "mixed.csv", rows)


def _run(argv, capsys):
    code = detail.main(["validate_row_detail.py"] + [str(a) for a in argv])
    return code, capsys.readouterr().out


def test_selecting_a_clean_paper_exits_zero(tmp_path, capsys):
    code, out = _run([_mixed(tmp_path), "--paper", "HYC-9002"], capsys)
    assert code == 0
    assert "HYC-9002-M1" in out
    assert "HYC-9001-M1" not in out


def test_selecting_the_paper_that_has_the_error_exits_one(tmp_path, capsys):
    code, out = _run([_mixed(tmp_path), "--paper", "HYC-9001"], capsys)
    assert code == 1
    assert "Missing required field" in out


def test_warnings_only_exits_zero_when_the_only_error_is_filtered_out(
    tmp_path, capsys
):
    code, out = _run([_mixed(tmp_path), "--warnings-only"], capsys)
    assert code == 0
    assert "Unspecified uptake_type" in out
    assert "Missing required field" not in out


def test_a_category_filter_that_matches_nothing_exits_zero(tmp_path, capsys):
    code, out = _run([_mixed(tmp_path), "--category", "zzz-no-such-rule"], capsys)
    assert code == 0
    assert "Rows reported: 0" in out


def test_errors_only_still_exits_one_when_an_error_is_selected(tmp_path, capsys):
    code, _ = _run([_mixed(tmp_path), "--errors-only"], capsys)
    assert code == 1


def test_an_unfiltered_run_on_a_file_with_an_error_exits_one(tmp_path, capsys):
    code, _ = _run([_mixed(tmp_path)], capsys)
    assert code == 1


def test_a_clean_file_exits_zero(clean_dataset, capsys):
    code, _ = _run([clean_dataset], capsys)
    assert code == 0


# ---------------------------------------------------------------------------
# --category actually filters, and other reporting details
# ---------------------------------------------------------------------------

def test_category_filter_excludes_non_matching_messages(tmp_path, capsys):
    code, out = _run([_mixed(tmp_path), "--category", "Unspecified"], capsys)
    assert code == 0
    assert "Unspecified uptake_type" in out
    assert "Missing required field" not in out          # the negative assertion
    assert "Rows reported: 1" in out


def test_warnings_only_suppresses_errors_in_the_summary_too(tmp_path, capsys):
    code, out = _run([_mixed(tmp_path), "--warnings-only", "--summary"], capsys)
    assert code == 0
    assert "WARNINGS" in out
    assert "ERRORS" not in out


def test_a_row_with_no_measurement_id_is_not_reported_as_nan(tmp_path, capsys):
    rows = [make_row(measurement_id=None, temperature_k=None)]
    path = write_csv(tmp_path / "noid.csv", rows)

    code, out = _run([path, "--summary"], capsys)
    assert code == 1
    assert "<no measurement_id>" in out
    assert "nan" not in out


def test_the_cli_omits_line_numbers_when_a_field_holds_a_newline(tmp_path, capsys):
    """The consequence of line_numbers_are_reliable, driven through main()."""
    path = write_csv(tmp_path / "embedded.csv",
                     [make_row(notes="one\ntwo", temperature_k=None)])
    code, out = _run([path], capsys)

    assert code == 1
    assert "csv line numbers omitted" in out
    assert "csv line" not in out.split("omitted")[1]


def test_line_numbers_are_shown_for_an_ordinary_file(tmp_path, capsys):
    path = write_csv(tmp_path / "plain.csv", [make_row(temperature_k=None)])
    code, out = _run([path], capsys)
    assert code == 1
    assert "csv line 2" in out
    assert "csv line numbers omitted" not in out


def test_a_zero_byte_csv_exits_two(tmp_path, capsys):
    path = tmp_path / "empty.csv"
    path.write_bytes(b"")
    code, out = _run([path], capsys)
    assert code == 2
    assert "empty or has no header row" in out


def test_the_uptake_pseudo_field_is_reported_usefully(tmp_path, capsys):
    """'Missing required field: uptake' names no real column; say which apply."""
    rows = [make_row(uptake_wt_pct=None, uptake_mmol_g=None,
                     uptake_ml_stp_g=None)]
    path = write_csv(tmp_path / "nouptake.csv", rows)
    code, out = _run([path], capsys)

    assert code == 1
    assert "uptake" in out
    # the operator must be able to tell which columns would satisfy the rule
    assert "uptake_wt_pct" in out or "uptake_mmol_g" in out
