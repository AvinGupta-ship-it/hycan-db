"""Invariants the published dataset must hold (manual §11.1, §11.5, §8.5).

These test the real file, not a fixture. Every other test module builds its
own data, which means none of them would notice the dataset itself drifting.
Skipped when the dataset is absent so the suite still runs on a bare clone.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from hycan.validate import validate_dataset

DATASET = Path(__file__).resolve().parents[1] / "data" / "raw" / "measurements_v0.1.csv"

pytestmark = pytest.mark.skipif(not DATASET.exists(), reason="dataset not present")


@pytest.fixture(scope="module")
def dataset() -> pd.DataFrame:
    return pd.read_csv(DATASET)


@pytest.fixture(scope="module")
def report(dataset):
    return validate_dataset(dataset)


def test_the_dataset_validates_with_zero_errors(report):
    assert report.error_counts == {}, report.error_counts


def test_the_warning_baseline_holds(report):
    """§11.5: a new warning type is a stop condition."""
    assert set(report.warning_counts) == {
        "Unspecified uptake_type",
        "mmol/g and wt% inconsistent",
    }, report.warning_counts


def test_measurement_id_is_unique(dataset):
    duplicated = dataset["measurement_id"][dataset["measurement_id"].duplicated()]
    assert duplicated.empty, sorted(duplicated)


def test_pore_volumes_nest(dataset):
    """§8.5 gap 4: ultramicropore <= micropore <= total, pairwise."""
    for smaller, larger in (
        ("ultramicropore_volume_cm3_g", "micropore_volume_cm3_g"),
        ("ultramicropore_volume_cm3_g", "total_pore_volume_cm3_g"),
        ("micropore_volume_cm3_g", "total_pore_volume_cm3_g"),
    ):
        pair = dataset.dropna(subset=[smaller, larger])
        violations = pair[pair[smaller] > pair[larger]]
        assert violations.empty, (
            smaller, larger, violations["measurement_id"].tolist()
        )


def test_physical_column_order_is_the_one_appends_rely_on(dataset):
    """§6.7. A positional append follows the CSV, not schema.py."""
    columns = list(dataset.columns)
    assert len(columns) == 40
    assert columns[0] == "paper_id"
    assert columns[36:40] == [
        "measurement_id",
        "uptake_ml_stp_g",
        "surface_area_method",
        "ultramicropore_volume_cm3_g",
    ]


def test_figure_estimated_is_assigned_to_no_row(dataset):
    """§3.4: the legacy value must never be assigned to a new row."""
    assert not (dataset["extraction_method"] == "figure_estimated").any()


def test_rows_reporting_uptake_state_their_conditions(dataset):
    """§8.5 gap 3, from the other side."""
    uptake = dataset[["uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"]]
    reports_uptake = uptake.notna().any(axis=1)
    missing = dataset[reports_uptake & (
        dataset["temperature_k"].isna() | dataset["pressure_bar"].isna()
    )]
    assert missing.empty, missing["measurement_id"].tolist()


def test_characterization_only_rows_carry_characterization(dataset):
    uptake = dataset[["uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"]]
    no_uptake = dataset[~uptake.notna().any(axis=1)]
    assert len(no_uptake) == 2, no_uptake["measurement_id"].tolist()

    characterization = [
        "bet_surface_area_m2_g", "langmuir_surface_area_m2_g",
        "micropore_volume_cm3_g", "ultramicropore_volume_cm3_g",
        "total_pore_volume_cm3_g", "average_pore_diameter_nm",
    ]
    assert no_uptake[characterization].notna().any(axis=1).all()
    assert no_uptake["temperature_k"].isna().all()
    assert no_uptake["pressure_bar"].isna().all()


def test_the_two_recovered_singh_rows_are_present(dataset):
    """§8.5 gap 3: these could not be represented under schema v1.0."""
    recovered = dataset[dataset["measurement_id"].isin(
        ["HYC-0018-M5", "HYC-0018-M6"]
    )].set_index("measurement_id")
    assert len(recovered) == 2

    assert recovered.loc["HYC-0018-M5", "bet_surface_area_m2_g"] == 41
    assert recovered.loc["HYC-0018-M5", "total_pore_volume_cm3_g"] == 0.14
    assert recovered.loc["HYC-0018-M5", "material_class"] == "graphene_oxide"

    assert recovered.loc["HYC-0018-M6", "bet_surface_area_m2_g"] == 218
    assert recovered.loc["HYC-0018-M6", "total_pore_volume_cm3_g"] == 1.40
    assert "Fig. 9" in recovered.loc["HYC-0018-M6", "notes"]


def test_texier_mandoki_no_longer_claims_a_bet_determination(dataset):
    """§8.6: the paper's column is 'TSA, total surface area' and never BET."""
    rows = dataset[dataset["paper_id"] == "HYC-0005"]
    assert len(rows) == 25
    assert set(rows["surface_area_method"]) == {"unspecified"}
    assert set(rows["extraction_confidence"]) == {4}


def test_surface_area_method_is_set_wherever_an_area_is_recorded(dataset):
    has_area = dataset[dataset["bet_surface_area_m2_g"].notna()]
    assert has_area["surface_area_method"].notna().all()
    assert not (has_area["surface_area_method"] == "none").any()


def test_the_sethia_ultramicropore_backfill_matches_table_2(dataset):
    """§8.5 gap 4, the paper the field exists for."""
    rows = dataset[dataset["paper_id"] == "HYC-0021"].set_index("sample_id")
    expected = {"HYC-0021-S3": 0.12, "HYC-0021-S4": 0.27,
                "HYC-0021-S5": 0.21, "HYC-0021-S6": 0.0}
    for sample, value in expected.items():
        assert rows.loc[sample, "ultramicropore_volume_cm3_g"] == pytest.approx(value)
    for sample in ("HYC-0021-S1", "HYC-0021-S2"):
        assert pd.isna(rows.loc[sample, "ultramicropore_volume_cm3_g"])


def test_the_corpus_can_now_test_the_ultramicropore_hypothesis(dataset):
    """The point of gap 4: two deviating papers, both with the quantity."""
    with_ultra = dataset.dropna(subset=["ultramicropore_volume_cm3_g"])
    assert set(with_ultra["paper_id"]) >= {"HYC-0005", "HYC-0021"}
    assert len(with_ultra) >= 25
