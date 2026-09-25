"""Shared fixtures for the Phase A helper-script tests (manual v2.0 §18).

The helpers under ``scripts/`` are command-line entry points, not package
modules, so ``scripts/`` goes on ``sys.path`` here rather than in each test
file. Nothing in this file touches the real dataset: every fixture writes to
pytest's ``tmp_path``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


# The dataset's PHYSICAL column order (manual §6.7). measurement_id and
# uptake_ml_stp_g are columns 37 and 38, appended after verification_date,
# while schema.py declares them mid-model. A positional append must follow
# this order, so the fixtures use it.
COLUMNS = [
    "paper_id",
    "doi",
    "first_author",
    "year",
    "journal",
    "title",
    "sample_id",
    "material_class",
    "material_description",
    "synthesis_method",
    "purification_method",
    "activation_method",
    "dopant_element",
    "dopant_concentration_at_pct",
    "functional_groups",
    "bet_surface_area_m2_g",
    "langmuir_surface_area_m2_g",
    "micropore_volume_cm3_g",
    "total_pore_volume_cm3_g",
    "average_pore_diameter_nm",
    "temperature_k",
    "pressure_bar",
    "uptake_wt_pct",
    "uptake_mmol_g",
    "uptake_type",
    "measurement_method",
    "uncertainty_wt_pct",
    "source_location",
    "extraction_method",
    "extraction_confidence",
    "reproducibility_tier",
    "notes",
    "extractor",
    "extraction_date",
    "verified_by",
    "verification_date",
    "measurement_id",
    "uptake_ml_stp_g",
]

# A row that validates with zero errors and zero warnings. Its `notes` field
# deliberately contains a comma so every fixture file exercises the quoted-comma
# case that breaks `awk -F','` (§6.7, §B.3).
BASE_ROW = {
    "paper_id": "HYC-9001",
    "doi": "10.1016/j.carbon.2015.09.001",
    "first_author": "Ito",
    "year": 2015,
    "journal": "Carbon",
    "title": "A synthetic paper for tests",
    "sample_id": "HYC-9001-S1",
    "material_class": "activated_carbon",
    "material_description": "KOH-activated carbon",
    "synthesis_method": "carbonization",
    "purification_method": "HCl reflux",
    "activation_method": "KOH 1:4",
    "dopant_element": None,
    "dopant_concentration_at_pct": None,
    "functional_groups": None,
    "bet_surface_area_m2_g": 1800.0,
    "langmuir_surface_area_m2_g": None,
    "micropore_volume_cm3_g": 0.6,
    "total_pore_volume_cm3_g": 0.9,
    "average_pore_diameter_nm": 2.1,
    "temperature_k": 77.0,
    "pressure_bar": 1.0,
    "uptake_wt_pct": 1.5,
    "uptake_mmol_g": None,
    "uptake_type": "excess",
    "measurement_method": "volumetric_sieverts",
    "uncertainty_wt_pct": 0.05,
    "source_location": "Table 2, row 3",
    "extraction_method": "table_direct",
    "extraction_confidence": 4,
    "reproducibility_tier": "B",
    "notes": "Value as printed, no conversion applied",
    "extractor": "HyCAN pipeline v2",
    "extraction_date": "2026-09-24",
    "verified_by": "Agent B",
    "verification_date": "2026-09-24",
    "measurement_id": "HYC-9001-M1",
    "uptake_ml_stp_g": None,
}


def make_row(**overrides) -> dict:
    """A copy of :data:`BASE_ROW` with *overrides* applied."""
    row = dict(BASE_ROW)
    row.update(overrides)
    return row


def write_csv(path, rows, columns=None) -> Path:
    """Write *rows* to *path* in the dataset's physical column order."""
    frame = pd.DataFrame(list(rows), columns=list(columns or COLUMNS))
    frame.to_csv(path, index=False)
    return Path(path)


@pytest.fixture
def row_factory():
    return make_row


@pytest.fixture
def csv_writer():
    return write_csv


@pytest.fixture
def clean_dataset(tmp_path):
    """A three-row dataset with zero errors and zero warnings."""
    rows = [
        make_row(measurement_id=f"HYC-9001-M{n}", pressure_bar=float(n))
        for n in (1, 2, 3)
    ]
    return write_csv(tmp_path / "measurements_test.csv", rows)
