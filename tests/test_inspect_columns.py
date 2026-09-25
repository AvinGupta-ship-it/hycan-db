"""Unit tests for scripts/inspect_columns.py (manual v2.0 §18 Phase A.2).

The tool exists to replace two things: ad-hoc pandas heredocs, and the `awk
-F','` habit that silently shifts every column after a quoted comma (§6.7,
§B.3). The tests that matter most are therefore the ones that prove a quoted
comma cannot shift a column, and that the physical-versus-declared column order
is reported rather than assumed.

Nothing here touches the real dataset except through a read-only hash check.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import inspect_columns as ic
import pandas as pd
import pytest
from conftest import COLUMNS, make_row, write_csv

REPO_ROOT = Path(__file__).resolve().parents[1]
REAL_DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"


def run(argv, capsys):
    """Invoke main() and return (exit_code, stdout)."""
    code = ic.main(["inspect_columns.py"] + argv)
    return code, capsys.readouterr().out


# ---------------------------------------------------------------------------
# The quoted-comma problem this tool exists to remove
# ---------------------------------------------------------------------------

def test_quoted_comma_does_not_shift_columns(tmp_path, capsys):
    path = write_csv(
        tmp_path / "commas.csv",
        [make_row(notes="Value as printed, no conversion, see Table 2")],
    )
    code, out = run([str(path), "--col", "measurement_id"], capsys)

    assert code == 0
    # measurement_id is the 37th physical column. A comma-split read would put
    # something else there; pandas puts the measurement_id there.
    assert "physical position: 37 of 51" in out
    assert "HYC-9001-M1" in out


def test_a_field_holding_a_comma_stays_one_field(tmp_path):
    path = write_csv(tmp_path / "commas.csv", [make_row(notes="a, b, c")])
    df = pd.read_csv(path)
    assert len(df.columns) == 51
    assert df.loc[0, "notes"] == "a, b, c"


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

def test_overview_is_the_default_view(clean_dataset, capsys):
    code, out = run([str(clean_dataset)], capsys)
    assert code == 0
    assert "3 rows x 51 columns" in out
    assert "paper_id" in out and "measurement_id" in out


def test_overview_counts_empty_cells(tmp_path, capsys):
    path = write_csv(tmp_path / "d.csv", [make_row(), make_row(
        measurement_id="HYC-9001-M2", uncertainty_wt_pct=None)])
    code, out = run([str(path)], capsys)
    assert code == 0
    uncertainty = [ln for ln in out.splitlines() if "uncertainty_wt_pct" in ln][0]
    # one of the two rows is empty in that column
    assert uncertainty.split()[3] == "1"  # non-null
    assert uncertainty.split()[4] == "1"  # empty


def test_overview_marks_an_entirely_empty_column(clean_dataset, capsys):
    code, out = run([str(clean_dataset)], capsys)
    dopant = [ln for ln in out.splitlines() if "dopant_element" in ln][0]
    assert "<all empty>" in dopant


# ---------------------------------------------------------------------------
# --order  (§6.7)
# ---------------------------------------------------------------------------

def test_order_reports_physical_order_first(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--order"], capsys)
    assert code == 0
    assert "Physical CSV column order" in out
    physical_block = out.split("schema.py declaration order:")[0]
    assert "  1  paper_id" in physical_block
    assert " 37  measurement_id" in physical_block
    assert " 38  uptake_ml_stp_g" in physical_block
    assert " 39  surface_area_method" in physical_block
    assert " 40  ultramicropore_volume_cm3_g" in physical_block


def test_order_identifies_the_expected_offset_not_a_defect(clean_dataset, capsys):
    """§6.7's offset is expected; only a difference in column *sets* is a defect."""
    code, out = run([str(clean_dataset), "--order"], capsys)
    assert code == 0
    assert "MISMATCH" not in out
    assert "Same columns, different order" in out
    assert "measurement_id: CSV #37" in out


def test_order_flags_a_real_set_mismatch(tmp_path, capsys):
    columns = [c for c in COLUMNS if c != "notes"] + ["invented_column"]
    row = make_row()
    row.pop("notes")
    row["invented_column"] = "x"
    path = write_csv(tmp_path / "wrong.csv", [row], columns=columns)

    code, out = run([str(path), "--order"], capsys)
    assert code == 0
    assert "MISMATCH" in out
    assert "invented_column" in out
    assert "notes" in out.split("in schema.py only:")[1]


def test_order_says_why_it_could_not_compare_when_hycan_is_absent(
    clean_dataset, capsys, monkeypatch
):
    monkeypatch.setattr(
        ic, "_schema_order", lambda: (None, "hycan is not importable here (x)")
    )
    code, out = run([str(clean_dataset), "--order"], capsys)
    assert code == 0
    assert "Declaration order NOT compared" in out
    assert "not importable" in out
    assert "did not run" in out


def test_a_schema_that_raises_is_reported_not_swallowed(
    clean_dataset, capsys, monkeypatch
):
    """--order exists to run the §6.7 check; it must not claim to have run it."""
    monkeypatch.setattr(
        ic, "_schema_order",
        lambda: (None, "schema.py raised while importing: ValueError: boom"),
    )
    code, out = run([str(clean_dataset), "--order"], capsys)
    assert code == 0
    assert "schema.py raised while importing" in out
    assert "ValueError: boom" in out
    assert "did not run" in out
    assert "Same columns, different order" not in out


def test_schema_order_is_actually_importable_here():
    """Guards the monkeypatched tests above from hiding a broken import."""
    fields, reason = ic._schema_order()
    assert reason is None
    assert fields is not None
    assert "paper_id" in fields
    assert "measurement_id" in fields


# ---------------------------------------------------------------------------
# --col and --values
# ---------------------------------------------------------------------------

def test_col_reports_numeric_summary_for_a_numeric_column(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--col", "pressure_bar"], capsys)
    assert code == 0
    assert "min: 1.0" in out and "max: 3.0" in out and "mean: 2" in out


def test_col_omits_numeric_summary_for_a_text_column(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--col", "material_class"], capsys)
    assert code == 0
    assert "min:" not in out
    assert "activated_carbon" in out


def test_values_counts_empty_cells_as_a_value(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--values", "dopant_element"], capsys)
    assert code == 0
    assert "<empty>" in out
    assert "3  <empty>" in out


def test_values_truncates_and_says_how_many_remain(tmp_path, capsys):
    rows = [
        make_row(measurement_id=f"HYC-9001-M{n}", pressure_bar=float(n))
        for n in range(1, 11)
    ]
    path = write_csv(tmp_path / "many.csv", rows)
    code, out = run([str(path), "--values", "pressure_bar", "--top", "3"], capsys)
    assert code == 0
    assert "... 7 more" in out


def test_col_and_values_are_repeatable(clean_dataset, capsys):
    code, out = run(
        [str(clean_dataset), "--col", "pressure_bar", "--col", "temperature_k"],
        capsys,
    )
    assert code == 0
    assert "--- pressure_bar ---" in out
    assert "--- temperature_k ---" in out


# ---------------------------------------------------------------------------
# --missing
# ---------------------------------------------------------------------------

def test_missing_orders_columns_by_emptiness(tmp_path, capsys):
    rows = [
        make_row(measurement_id="HYC-9001-M1"),
        make_row(measurement_id="HYC-9001-M2", uncertainty_wt_pct=None),
        make_row(measurement_id="HYC-9001-M3", uncertainty_wt_pct=None,
                 average_pore_diameter_nm=None),
    ]
    path = write_csv(tmp_path / "gaps.csv", rows)
    code, out = run([str(path), "--missing"], capsys)
    assert code == 0

    listed = [ln.split()[-1] for ln in out.splitlines() if ln.startswith("  ")]
    assert listed.index("uncertainty_wt_pct") < listed.index("average_pore_diameter_nm")


def test_missing_says_so_when_nothing_is_empty(tmp_path, capsys):
    full = {c: "x" for c in COLUMNS}
    path = write_csv(tmp_path / "full.csv", [full])
    code, out = run([str(path), "--missing"], capsys)
    assert code == 0
    assert "No empty cells" in out


# ---------------------------------------------------------------------------
# --where / --head / --tail / --select
# ---------------------------------------------------------------------------

def test_where_filters_and_reports_the_count(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--where", "pressure_bar=2.0"], capsys)
    assert code == 0
    assert "-> 1 of 3 rows" in out


def test_where_matches_on_a_field_containing_a_comma(tmp_path, capsys):
    rows = [
        make_row(measurement_id="HYC-9001-M1", source_location="Table 2, row 3"),
        make_row(measurement_id="HYC-9001-M2", source_location="Table 4"),
    ]
    path = write_csv(tmp_path / "loc.csv", rows)
    code, out = run([str(path), "--where", "source_location=Table 2, row 3"], capsys)
    assert code == 0
    assert "-> 1 of 2 rows" in out


def test_where_without_equals_is_rejected(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--where", "pressure_bar"], capsys)
    assert code == 2
    assert "needs COL=VALUE" in out


def test_where_on_an_unknown_column_is_rejected(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--where", "nope=1"], capsys)
    assert code == 2
    assert "not in the file" in out


def test_head_and_select_limit_the_view(clean_dataset, capsys):
    code, out = run(
        [str(clean_dataset), "--head", "2", "--select", "measurement_id"], capsys
    )
    assert code == 0
    assert "HYC-9001-M1" in out and "HYC-9001-M2" in out
    assert "HYC-9001-M3" not in out
    assert "activated_carbon" not in out


def test_tail_shows_the_last_rows(clean_dataset, capsys):
    code, out = run(
        [str(clean_dataset), "--tail", "1", "--select", "measurement_id"], capsys
    )
    assert code == 0
    assert "HYC-9001-M3" in out and "HYC-9001-M1" not in out


# ---------------------------------------------------------------------------
# Exit codes and read-only guarantee
# ---------------------------------------------------------------------------

def test_missing_file_exits_2(tmp_path, capsys):
    code, out = run([str(tmp_path / "absent.csv")], capsys)
    assert code == 2
    assert "not found" in out


def test_unknown_column_exits_2_and_lists_what_is_available(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--col", "bet_surface_area"], capsys)
    assert code == 2
    assert "bet_surface_area" in out
    assert "Available:" in out
    assert "bet_surface_area_m2_g" in out


def test_unknown_column_is_caught_before_any_view_runs(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--order", "--col", "nope"], capsys)
    assert code == 2
    assert "Physical CSV column order" not in out


def test_inspecting_a_file_never_modifies_it(clean_dataset, capsys):
    before = hashlib.sha256(clean_dataset.read_bytes()).hexdigest()
    run([str(clean_dataset), "--order", "--missing", "--values", "uptake_type",
         "--head", "3"], capsys)
    after = hashlib.sha256(clean_dataset.read_bytes()).hexdigest()
    assert before == after


@pytest.mark.skipif(not REAL_DATASET.exists(), reason="dataset not present")
def test_reading_the_real_dataset_leaves_it_byte_identical(capsys):
    """§6.7 forbids editing measurements_v0.1.csv. Prove this tool cannot."""
    before = hashlib.sha256(REAL_DATASET.read_bytes()).hexdigest()
    code, out = run([str(REAL_DATASET), "--order"], capsys)
    after = hashlib.sha256(REAL_DATASET.read_bytes()).hexdigest()

    assert code == 0
    assert before == after
    assert "MISMATCH" not in out


# ---------------------------------------------------------------------------
# --where must not silently match nothing on a numeric column
#
# An isolated audit found `--where temperature_k=77` reported "0 of 119 rows"
# on the real dataset, where 90 rows match, because astype(str) on a float64
# column yields "77.0". Exit 0, no warning, and every later view then ran on
# the empty frame and reported confidently.
# ---------------------------------------------------------------------------

def test_where_matches_an_integer_literal_against_a_float_column(
    clean_dataset, capsys
):
    code, out = run([str(clean_dataset), "--where", "pressure_bar=2"], capsys)
    assert code == 0
    assert "-> 1 of 3 rows" in out


def test_where_still_matches_the_float_spelling(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--where", "pressure_bar=2.0"], capsys)
    assert code == 0
    assert "-> 1 of 3 rows" in out


def test_where_matches_a_whole_number_float_column(tmp_path, capsys):
    rows = [make_row(measurement_id=f"HYC-9001-M{n}", temperature_k=t)
            for n, t in enumerate([77.0, 77.0, 298.0], start=1)]
    path = write_csv(tmp_path / "temps.csv", rows)

    code, out = run([str(path), "--where", "temperature_k=77"], capsys)
    assert code == 0
    assert "-> 2 of 3 rows" in out


def test_where_selects_the_right_rows_not_merely_the_right_count(
    clean_dataset, capsys
):
    code, out = run([str(clean_dataset), "--where", "pressure_bar=3",
                     "--head", "5", "--select", "measurement_id"], capsys)
    assert code == 0
    assert "HYC-9001-M3" in out
    assert "HYC-9001-M1" not in out
    assert "HYC-9001-M2" not in out


def test_where_with_an_empty_value_selects_empty_cells(tmp_path, capsys):
    rows = [make_row(measurement_id="HYC-9001-M1", uncertainty_wt_pct=0.05),
            make_row(measurement_id="HYC-9001-M2", uncertainty_wt_pct=None)]
    path = write_csv(tmp_path / "gaps.csv", rows)

    code, out = run([str(path), "--where", "uncertainty_wt_pct=",
                     "--head", "5", "--select", "measurement_id"], capsys)
    assert code == 0
    assert "-> 1 of 2 rows" in out
    assert "HYC-9001-M2" in out


def test_where_on_a_text_column_is_unaffected(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--where",
                     "material_class=activated_carbon"], capsys)
    assert code == 0
    assert "-> 3 of 3 rows" in out


def test_where_clauses_are_repeatable_and_all_are_applied(tmp_path, capsys):
    rows = [
        make_row(measurement_id="HYC-9001-M1", temperature_k=77.0, pressure_bar=1.0),
        make_row(measurement_id="HYC-9001-M2", temperature_k=77.0, pressure_bar=20.0),
        make_row(measurement_id="HYC-9001-M3", temperature_k=298.0, pressure_bar=1.0),
    ]
    path = write_csv(tmp_path / "two.csv", rows)

    code, out = run([str(path), "--where", "temperature_k=77",
                     "--where", "pressure_bar=20",
                     "--head", "5", "--select", "measurement_id"], capsys)
    assert code == 0
    assert "-> 1 of 3 rows" in out
    assert "HYC-9001-M2" in out
    assert "HYC-9001-M1" not in out


# ---------------------------------------------------------------------------
# Ragged files: the silent column shift this tool exists to catch
# ---------------------------------------------------------------------------

def test_a_too_wide_row_is_diagnosed_before_pandas_gives_up(tmp_path, capsys):
    """pandas raises here; the operator still needs to know which line is bad."""
    header = ",".join(COLUMNS)
    path = tmp_path / "ragged.csv"
    # The bad row must stay WIDER than the header, which is what this test is
    # for. It was header + 2 when the header was 40 columns wide; keeping the
    # +2 rather than the literal 42 preserves that as the schema grows.
    path.write_text(header + "\n" + ",".join(["x"] * 51) + "\n"
                    + ",".join(["y"] * 53) + "\n", encoding="utf-8")

    code, out = run([str(path)], capsys)
    assert code == 2
    assert "rows of differing width" in out
    assert "53 field(s) on line(s) [3]" in out
    assert "which lines are at fault" in out


def test_a_too_narrow_row_is_warned_about_and_still_inspectable(tmp_path, capsys):
    """pandas pads this one silently, which is the more dangerous case."""
    header = ",".join(COLUMNS)
    path = tmp_path / "short.csv"
    path.write_text(header + "\n" + ",".join(["x"] * 51) + "\n"
                    + ",".join(["y"] * 35) + "\n", encoding="utf-8")

    code, out = run([str(path)], capsys)
    assert code == 0
    assert "rows of differing width" in out
    assert "not reliable" in out
    assert "35 field(s) on line(s) [3]" in out
    assert "2 rows x 51 columns" in out


def test_a_well_formed_csv_gets_no_width_warning(clean_dataset, capsys):
    code, out = run([str(clean_dataset)], capsys)
    assert code == 0
    assert "differing width" not in out


def test_field_counts_is_not_fooled_by_a_quoted_comma(tmp_path):
    path = write_csv(tmp_path / "commas.csv",
                     [make_row(notes="a, b, c, d, e")])
    assert ic.field_counts(str(path)) == {51: [1, 2]}


def test_a_zero_byte_csv_exits_2(tmp_path, capsys):
    path = tmp_path / "empty.csv"
    path.write_bytes(b"")
    code, out = run([str(path)], capsys)
    assert code == 2
    assert "empty or has no header row" in out


# ---------------------------------------------------------------------------
# Views that were asserted only by their shape
# ---------------------------------------------------------------------------

def test_the_example_column_shows_the_first_real_value(clean_dataset, capsys):
    code, out = run([str(clean_dataset)], capsys)
    line = [ln for ln in out.splitlines() if " material_class " in ln][0]
    assert line.rstrip().endswith("activated_carbon")


def test_a_long_example_value_is_truncated(tmp_path, capsys):
    path = write_csv(tmp_path / "long.csv", [make_row(title="Q" * 200)])
    code, out = run([str(path)], capsys)
    line = [ln for ln in out.splitlines() if ln.strip().startswith("6  title")][0]
    assert "..." in line
    assert "Q" * 60 not in line


def test_col_reports_median_distinctly_from_mean(tmp_path, capsys):
    """pressure 1,2,3 makes mean == median; use a skewed column instead."""
    rows = [make_row(measurement_id=f"HYC-9001-M{n}", pressure_bar=p)
            for n, p in enumerate([1.0, 2.0, 100.0], start=1)]
    path = write_csv(tmp_path / "skew.csv", rows)

    code, out = run([str(path), "--col", "pressure_bar"], capsys)
    assert code == 0
    assert "mean: 34.3333" in out
    assert "median: 2" in out


def test_col_omits_the_numeric_summary_on_a_mixed_column(tmp_path, capsys):
    """The guard's purpose: some values numeric, some not."""
    rows = [make_row(measurement_id="HYC-9001-M1", activation_method="800"),
            make_row(measurement_id="HYC-9001-M2", activation_method="KOH 1:4")]
    path = write_csv(tmp_path / "mixed.csv", rows)

    code, out = run([str(path), "--col", "activation_method"], capsys)
    assert code == 0
    assert "min:" not in out
    assert "KOH 1:4" in out


def test_col_honours_top(tmp_path, capsys):
    rows = [make_row(measurement_id=f"HYC-9001-M{n}", pressure_bar=float(n))
            for n in range(1, 11)]
    path = write_csv(tmp_path / "many.csv", rows)

    code, out = run([str(path), "--col", "pressure_bar", "--top", "3"], capsys)
    assert code == 0
    assert "top 3 of 10 distinct values" in out
    assert len([ln for ln in out.splitlines() if ln.startswith("  ")]) == 3


def test_a_negative_head_is_rejected(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--head", "-1"], capsys)
    assert code == 2
    assert "zero or positive" in out


def test_head_and_tail_together_show_both_ends(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--head", "1", "--tail", "1",
                     "--select", "measurement_id"], capsys)
    assert code == 0
    assert "HYC-9001-M1" in out and "HYC-9001-M3" in out


def test_select_accepts_several_columns(clean_dataset, capsys):
    code, out = run([str(clean_dataset), "--head", "1",
                     "--select", "measurement_id",
                     "--select", "pressure_bar"], capsys)
    assert code == 0
    assert "measurement_id" in out and "pressure_bar" in out
    assert "material_class" not in out


def test_numeric_matching_applies_only_to_numeric_columns(tmp_path, capsys):
    """On a text column the query must be a literal, not a value comparison.

    The sixth row is what makes the column text: with only numeric-looking
    values pandas parses the whole column to float64 at read time and "0077",
    "77.0" and "77" are already the same number before this code sees them.
    A real code or ID column has non-numeric entries, and then the literal
    must be honoured.
    """
    values = ["77", "0077", "77.0", "1e2", "100", "KOH 1:4"]
    rows = [make_row(measurement_id=f"HYC-9001-M{n}", activation_method=v)
            for n, v in enumerate(values, start=1)]
    path = write_csv(tmp_path / "codes.csv", rows)

    column = pd.read_csv(path)["activation_method"]
    assert not pd.api.types.is_numeric_dtype(column)   # what the branch tests

    for query in ("77", "0077", "77.0", "1e2", "100"):
        code, out = run([str(path), "--where", f"activation_method={query}"],
                        capsys)
        assert code == 0
        assert "-> 1 of 6 rows" in out, f"{query} over-matched"


def test_numeric_matching_still_applies_to_numeric_columns(tmp_path, capsys):
    rows = [make_row(measurement_id=f"HYC-9001-M{n}", temperature_k=t)
            for n, t in enumerate([77.0, 298.0], start=1)]
    path = write_csv(tmp_path / "t.csv", rows)

    code, out = run([str(path), "--where", "temperature_k=77"], capsys)
    assert code == 0
    assert "-> 1 of 2 rows" in out
