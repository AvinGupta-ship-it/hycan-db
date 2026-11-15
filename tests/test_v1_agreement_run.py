"""Tests for scripts/v1_search/agreement.py (the §9 agreement-statistics run
over the collected tree)."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_agreement_run", REPO_ROOT / "scripts" / "v1_search" / "agreement.py"
)
run = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = run
spec.loader.exec_module(run)

COLS = [
    "paper_id",
    "measurement_id",
    "material_description",
    "temperature_k",
    "pressure_bar",
    "uptake_wt_pct",
    "isotherm_branch",
    "extraction_method",
]


def row(pid, mid, label, p, wt):
    return {
        "paper_id": pid,
        "measurement_id": mid,
        "material_description": f"{label} | x",
        "temperature_k": "77",
        "pressure_bar": p,
        "uptake_wt_pct": wt,
        "isotherm_branch": "adsorption",
        "extraction_method": "table_direct",
    }


def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def test_dual_and_legacy_summaries_from_a_collected_tree(tmp_path):
    tree = tmp_path / "tree"
    tree.mkdir()
    write_csv(
        tree / "papers.csv",
        ["paper_id", "mode"],
        [
            {"paper_id": "HYC-9001", "mode": "dual"},
            {"paper_id": "HYC-9002", "mode": "legacy"},
            {"paper_id": "HYC-9003", "mode": "none"},
        ],
    )
    # Dual paper: A and B agree on one row; B finds one more.
    write_rows(tree / "HYC-9001" / "A" / "rows.csv",
               [row("HYC-9001", "HYC-9001-M1", "AC-1", "1", "1.50")])
    write_rows(tree / "HYC-9001" / "B" / "rows.csv",
               [row("HYC-9001", "HYC-9001-M1", "AC-1", "1", "1.50"),
                row("HYC-9001", "HYC-9001-M2", "AC-2", "20", "4.0")])
    write_csv(tree / "HYC-9001" / "C" / "resolutions.csv",
              ["match_line", "field", "first_value", "second_value", "decision",
               "final_value", "evidence", "location"],
              [{"match_line": "2", "field": "row", "decision": "second"}])
    # Legacy paper: one v0.1 row matching B through the printed label.
    write_rows(tree / "HYC-9002" / "B" / "rows.csv",
               [row("HYC-9002", "HYC-9002-M1", "sample A", "1", "2.0")])
    write_csv(tree / "HYC-9002" / "C" / "resolutions.csv",
              ["match_line", "field", "first_value", "second_value", "decision",
               "final_value", "evidence", "location"],
              [{"match_line": "1", "field": "uptake_wt_pct", "decision": "first"}])
    write_csv(tree / "HYC-9002" / "C_input" / "labels.csv",
              ["sample_id", "label", "measurement_ids"],
              [{"sample_id": "S1", "label": "sample A", "measurement_ids": ""}])
    v01 = tmp_path / "v01.csv"
    legacy_row = row("HYC-9002", "HYC-9002-M1", "legacy name", "1", "2.0")
    legacy_row["sample_id"] = "S1"
    write_csv(v01, COLS + ["sample_id"], [legacy_row])

    rc = run.main(["--tree", str(tree), "--v01", str(v01)])
    assert rc == 0

    dual = json.loads((tree / "agreement_dual.json").read_text())
    assert [p["paper"] for p in dual["papers"]] == ["HYC-9001"]
    assert dual["summary"]["matched_pairs"] == 1
    assert dual["summary"]["only_second"] == 1
    assert dual["summary"]["row_detection_agreement"] == 2 / 3
    assert dual["summary"]["c_outcomes"]["rows"] == {"second": 1}
    assert dual["summary"]["numeric"]["uptake_wt_pct"]["share_within_tolerance"] == 1.0
    assert "a" not in dual["papers"][0]  # raw value lists are not written

    legacy = json.loads((tree / "agreement_legacy.json").read_text())
    # The v0.1 row matches B's row through the labeller's printed label.
    assert legacy["summary"]["matched_pairs"] == 1
    assert legacy["summary"]["only_first"] == 0
    assert legacy["summary"]["c_outcomes"]["fields"] == {"first": 1}


def test_refuses_a_legacy_paper_with_no_v01_rows(tmp_path, capsys):
    tree = tmp_path / "tree"
    tree.mkdir()
    write_csv(tree / "papers.csv", ["paper_id", "mode"],
              [{"paper_id": "HYC-9002", "mode": "legacy"}])
    v01 = tmp_path / "v01.csv"
    write_csv(v01, COLS, [])
    rc = run.main(["--tree", str(tree), "--v01", str(v01)])
    assert rc == 1
    assert "no v0.1 rows" in capsys.readouterr().err
