"""Tests for scripts/v1_agreement.py (protocol §9 agreement statistics)."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_agreement", REPO_ROOT / "scripts" / "v1_agreement.py"
)
ag = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ag
spec.loader.exec_module(ag)

COLS = [
    "measurement_id",
    "material_description",
    "temperature_k",
    "pressure_bar",
    "uptake_wt_pct",
    "isotherm_branch",
    "extraction_method",
    "basis_inferred",
]


def write(path: Path, rows):
    path.mkdir(parents=True, exist_ok=True)
    with (path / "rows.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)


def r(mid, p, wt, basis="excess", method="table_direct", label="S1"):
    return {
        "measurement_id": mid,
        "material_description": f"{label} | x",
        "temperature_k": "77",
        "pressure_bar": p,
        "uptake_wt_pct": wt,
        "isotherm_branch": "adsorption",
        "extraction_method": method,
        "basis_inferred": basis,
    }


def test_kappa_and_rounding(tmp_path):
    write(
        tmp_path / "P" / "A",
        [r("A1", "1", "1.50"), r("A2", "20", "4.0"), r("A3", "40", "4.5")],
    )
    write(
        tmp_path / "P" / "B",
        [
            r("B1", "1", "1.5"),
            r("B2", "20", "4.1", basis="unknown"),
            r("B3", "60", "4.2"),
        ],
    )
    s = ag.summarize([ag.paper_stats(tmp_path / "P", ag.field_kinds())])
    assert (s["matched_pairs"], s["only_first"], s["only_second"]) == (2, 1, 1)
    assert s["row_detection_agreement"] == pytest.approx(4 / 6)
    assert s["categorical"]["basis_inferred"]["exact_agreement"] == 0.5
    # 1.50 vs 1.5 agree within printed rounding; 4.0 vs 4.1 do not.
    assert s["numeric"]["uptake_wt_pct"]["share_within_tolerance"] == 0.5


def test_figure_values_use_3_percent(tmp_path):
    write(tmp_path / "P" / "A", [r("A1", "20", "5.00", method="figure_digitized")])
    write(tmp_path / "P" / "B", [r("B1", "20.2", "5.12", method="figure_digitized")])
    s = ag.summarize([ag.paper_stats(tmp_path / "P", ag.field_kinds())])
    assert s["numeric"]["uptake_wt_pct"]["share_within_tolerance"] == 1.0
