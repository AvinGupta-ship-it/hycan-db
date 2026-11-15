"""Tests for scripts/v1_search/audit.py (the §12 audit draw)."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_audit", REPO_ROOT / "scripts" / "v1_search" / "audit.py"
)
au = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = au
spec.loader.exec_module(au)


def test_settle_quotas_moves_a_shortfall_within_its_stratum():
    cells = {("a", "agreed"): list("ab"), ("a", "resolved"): [f"r{i}" for i in range(40)],
             ("b", "agreed"): list("ABCDEFGHIJ"), ("b", "resolved"): list("KLMNOPQRST"),
             ("c", "all"): list("0123456789")}
    q = au.settle_quotas(cells)
    assert q[("a", "agreed")] == 2 and q[("a", "resolved")] == 28
    assert q[("b", "agreed")] == 8 and q[("b", "resolved")] == 7
    assert q[("c", "all")] == 10  # capped at the pool


def test_settle_quotas_caps_the_other_cell_at_its_pool():
    cells = {("a", "agreed"): list("ab"), ("a", "resolved"): list("cdefg"),
             ("b", "agreed"): list("ABCDEFGHIJ"), ("b", "resolved"): list("KLMNOPQRST"),
             ("c", "all"): list(map(str, range(20)))}
    q = au.settle_quotas(cells)
    assert q[("a", "agreed")] == 2 and q[("a", "resolved")] == 5
    assert q[("c", "all")] == 15


def write_csv(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def test_agreed_classifier_reads_match_lines_and_resolutions(tmp_path):
    pid = "HYC-9001"
    write_csv(tmp_path / pid / "C_input" / "match.csv",
              ["match_line", "status", "first_measurement_id",
               "second_measurement_id", "field", "first_value", "second_value"],
              [
                  # line 1: agreed pair, untouched by C -> agreed.
                  {"match_line": "1", "status": "agree",
                   "first_measurement_id": "M1", "second_measurement_id": "B1"},
                  # line 2: a differing field -> resolved.
                  {"match_line": "2", "status": "differ",
                   "first_measurement_id": "M2", "second_measurement_id": "B2",
                   "field": "uptake_wt_pct"},
                  # line 3: agreed pair later corrected by C -> resolved.
                  {"match_line": "3", "status": "agree",
                   "first_measurement_id": "M3", "second_measurement_id": "B3"},
                  # line 4: only_second row C kept as M9 -> resolved.
                  {"match_line": "4", "status": "only_second",
                   "first_measurement_id": "", "second_measurement_id": "B4"},
              ])
    write_csv(tmp_path / pid / "C" / "resolutions.csv",
              ["match_line", "field", "first_value", "second_value", "decision",
               "final_value", "evidence", "location"],
              [
                  {"match_line": "2", "field": "uptake_wt_pct", "decision": "first",
                   "final_value": "4.2"},
                  {"match_line": "3", "field": "temperature_k", "decision": "new",
                   "final_value": "77"},
                  {"match_line": "4", "field": "row", "decision": "second",
                   "final_value": "M9"},
              ])
    is_agreed = au.agreed_classifier(tmp_path, pid)
    assert is_agreed("M1")
    assert not is_agreed("M2")
    assert not is_agreed("M3")   # its agree line carries a correction
    assert not is_agreed("M9")   # named by a resolution's final_value
    assert not is_agreed("M99")  # unknown to the match -> never agreed


def test_draw_reproduces_the_committed_files(tmp_path):
    committed = REPO_ROOT / "references" / "v1_audit"
    rc = au.main(["draw", "--out", str(tmp_path)])
    assert rc == 0
    for name in ("draw.csv", "cells.json", "sheet.csv"):
        assert (tmp_path / name).read_bytes() == (committed / name).read_bytes(), name


def test_row_errors_applies_the_s12_rule():
    import pandas as pd
    row = pd.Series({
        "measurement_id": "HYC-9001-M1", "paper_id": "HYC-9001",
        "material_description": "AC-1 | activated carbon",
        "extraction_method": "table_direct", "notes": "",
        "temperature_k": "77", "pressure_bar": "20",
        "uptake_wt_pct": "1.50", "uptake_mmol_g": "", "uptake_ml_stp_g": "",
        "bet_surface_area_m2_g": "1250", "surface_area_method": "BET",
        "surface_area_probe_gas": "", "basis_stated": "true",
        "basis_inferred": "excess", "wt_pct_convention": "W1",
        "value_kind": "measured",
    })
    good = {"uptake_value": "1.5", "uptake_unit": "wt%", "temperature_k": "77",
            "pressure_bar": "20", "a_bet_m2_g": "1250", "a_bet_method": "bet",
            "a_bet_probe_gas": "unspecified", "basis_stated": "TRUE",
            "basis_inferred": "excess", "wt_pct_convention": "w1",
            "value_kind": "measured", "sample_identity": "AC 1"}
    errs = au.row_errors(good, row)
    assert errs and not any(errs.values())
    bad = dict(good, temperature_k="78", basis_inferred="absolute",
               uptake_unit="mmol/g", sample_identity="AC-2")
    errs = au.row_errors(bad, row)
    assert errs["temperature_k"] and errs["basis_inferred"]
    assert errs["uptake_unit"] and errs["uptake_value"]  # no mmol/g stored
    assert errs["sample_identity"]
    assert not errs["pressure_bar"] and not errs["a_bet_m2_g"]


def test_row_errors_uses_3_percent_for_figure_rows():
    import pandas as pd
    row = pd.Series({
        "measurement_id": "HYC-9001-M2", "paper_id": "HYC-9001",
        "material_description": "AC-1 | activated carbon",
        "extraction_method": "figure_digitized", "notes": "",
        "temperature_k": "77", "pressure_bar": "20.0",
        "uptake_wt_pct": "2.00", "uptake_mmol_g": "", "uptake_ml_stp_g": "",
        "bet_surface_area_m2_g": "", "surface_area_method": "",
        "surface_area_probe_gas": "", "basis_stated": "false",
        "basis_inferred": "excess", "wt_pct_convention": "unknown",
        "value_kind": "measured",
    })
    sheet = {"uptake_value": "2.05", "uptake_unit": "wt%",
             "temperature_k": "77", "pressure_bar": "20.3",
             "basis_stated": "false", "basis_inferred": "excess",
             "wt_pct_convention": "unknown", "value_kind": "measured",
             "sample_identity": "AC-1", "digitized_point": "20.5; 1.95"}
    errs = au.row_errors(sheet, row)
    assert not errs["uptake_value"]      # 2.5% off, within 3%
    assert not errs["pressure_bar"]      # 1.5% off, within 3%
    assert not errs["digitized_point"]   # both parts within 3%
    bad = dict(sheet, digitized_point="25; 1.95")
    assert au.row_errors(bad, row)["digitized_point"]


def test_clopper_pearson_bounds():
    lo, hi = au.clopper_pearson(0, 30)
    assert lo == 0.0 and 0.10 < hi < 0.13
    lo, hi = au.clopper_pearson(30, 30)
    assert hi == 1.0 and 0.87 < lo < 0.90
