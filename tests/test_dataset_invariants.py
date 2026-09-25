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
    """§11.5: a new warning type is a stop condition.

    Schema v1.2 removed "mmol/g and wt% inconsistent" from this baseline, and
    that removal is deliberate rather than a suppressed signal. The corpus's
    only instance of it was a false positive: HYC-0004-M2 reports 0.05 wt% and
    0.268 mmol/g, and 0.268 mmol/g is 0.0540 wt%, which rounds to 0.05 at the
    paper's own precision. The check fired because its tolerance was
    relative-only, and an absolute difference of 0.004 wt% is 8% relative at
    that magnitude. The tolerance is now relative and absolute, so the pair is
    correctly read as consistent. See docs/migration_v1_2_plan.md §1, which
    states the baseline change before the code was touched.

    The generalisation to all three uptake pairs also introduced two new
    warning labels, "mL(STP)/g and wt% inconsistent" and "mL(STP)/g and mmol/g
    inconsistent". Neither is in this baseline because neither fires on any row
    in the corpus -- checked against all 24 rows carrying both a volumetric and
    a gravimetric uptake before the check was written.

    `Pre-2005 raw-CNT high uptake (Tier D)` enters the baseline with HYC-0011
    (Qikun 2002), whose headline claim is 8.0 wt% on a raw CNT film. The
    warning is doing exactly what §11.2 wrote it to do, and the row is retained
    at Tier D under the disclosure-not-deletion principle of
    `docs/reproducibility_tiering.md`, so the right response to the §11.5 stop
    condition is to admit the type deliberately rather than to keep the row
    out. `scripts/append_paper.py` refused that append until this line changed,
    which is the check working. That row's `notes` records that the 8.0 wt% is
    arithmetically irreconcilable with the paper's own areal uptake, film mass
    and film area, which imply 0.84-1.26 wt%.
    """
    assert set(report.warning_counts) == {
        "Unspecified uptake_type",
        "Pre-2005 raw-CNT high uptake (Tier D)",
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
    assert len(columns) == 51
    assert columns[0] == "paper_id"
    # v1.1 appended 39-40; v1.2 appended 41-51. Both went on the end precisely
    # so that positional appends keep working, and this pins that.
    assert columns[36:40] == [
        "measurement_id",
        "uptake_ml_stp_g",
        "surface_area_method",
        "ultramicropore_volume_cm3_g",
    ]
    assert columns[40:51] == [
        "uptake_bound",
        "temperature_unstated",
        "pressure_unstated",
        "measurement_mode",
        "reference_temperature_k",
        "metal_element",
        "metal_loading_wt_pct",
        "residual_metal_element",
        "residual_metal_wt_pct",
        "dopant_concentration_wt_pct",
        "dopant_concentration_method",
    ]


def test_figure_estimated_is_assigned_to_no_row(dataset):
    """§3.4: the legacy value must never be assigned to a new row."""
    assert not (dataset["extraction_method"] == "figure_estimated").any()


def _flag(dataset, column):
    """Read a v1.2 boolean column, which round-trips through CSV as a string."""
    return dataset[column].astype(str).str.strip().str.lower() == "true"


def test_rows_reporting_uptake_state_their_conditions(dataset):
    """§8.5 gap 3, from the other side, as amended by schema v1.2 gap 2.

    A row reporting uptake must state its temperature and pressure, OR declare
    with the matching `*_unstated` flag that its paper never stated one. The
    flag is the only escape, so a null cannot appear by accident.
    """
    uptake = dataset[["uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"]]
    reports_uptake = uptake.notna().any(axis=1)
    unexcused = (
        (dataset["temperature_k"].isna() & ~_flag(dataset, "temperature_unstated"))
        | (dataset["pressure_bar"].isna() & ~_flag(dataset, "pressure_unstated"))
    )
    missing = dataset[reports_uptake & unexcused]
    assert missing.empty, missing["measurement_id"].tolist()


def test_a_condition_is_never_both_stated_and_declared_unstated(dataset):
    """Schema v1.2 gap 2's contradiction check, asserted against the dataset."""
    for column, flag in (
        ("temperature_k", "temperature_unstated"),
        ("pressure_bar", "pressure_unstated"),
    ):
        both = dataset[dataset[column].notna() & _flag(dataset, flag)]
        assert both.empty, (column, both["measurement_id"].tolist())


def test_only_papers_that_never_state_a_condition_use_the_flags(dataset):
    """The flags are narrow: four papers, and the reason is in each row's notes.

    HYC-0011 and HYC-0015 report uptakes at "room temperature" with no number.
    HYC-0009's TPD rows give a hydrogen flow rate and no pressure. HYC-0026's
    uptake sentence states no pressure, and every pressure the paper does state
    belongs to a different quantity measured on a different instrument.
    """
    flagged = dataset[
        _flag(dataset, "temperature_unstated") | _flag(dataset, "pressure_unstated")
    ]
    assert set(flagged["paper_id"]) == {
        "HYC-0009", "HYC-0011", "HYC-0015", "HYC-0026",
    }, sorted(set(flagged["paper_id"]))


def test_non_isothermal_rows_state_their_reference_temperature(dataset):
    """Schema v1.2 gap 9. A cycle's uptake is meaningless without its reference.

    HYC-0029 cycles 303 -> 673 -> 303 K; HYC-0011's third powder measurement
    ramps to 353 K; HYC-0009's TPD rows integrate desorption to 723.15 K.
    """
    cycled = dataset[dataset["measurement_mode"] != "isothermal"]
    assert not cycled.empty
    reports_uptake = cycled[
        ["uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"]
    ].notna().any(axis=1)
    missing = cycled[reports_uptake & cycled["reference_temperature_k"].isna()]
    assert missing.empty, missing["measurement_id"].tolist()


def test_bounded_uptakes_are_flagged_and_rare(dataset):
    """Schema v1.2 gap 1. A bound must never masquerade as a measurement."""
    bounded = dataset[dataset["uptake_bound"] != "exact"]
    assert set(bounded["uptake_bound"]) <= {"upper", "lower", "approximate"}
    # HYC-0029's two KOH-activated samples, reported only as "more than 1.0
    # wt.%", and HYC-0017's room-temperature result, reported only as "below
    # 0.2 wt.%" -- that paper's headline negative result, and the row gap 1 was
    # written for.
    assert set(bounded["measurement_id"]) == {
        "HYC-0029-M3", "HYC-0029-M4", "HYC-0017-M3",
    }, sorted(bounded["measurement_id"])
    assert set(bounded["uptake_bound"]) == {"lower", "upper"}
    upper = bounded[bounded["uptake_bound"] == "upper"]
    assert set(upper["measurement_id"]) == {"HYC-0017-M3"}


def test_metal_loading_is_not_confused_with_dopant_concentration(dataset):
    """Schema v1.2 gaps 7 and 8 exist to keep these apart."""
    loaded = dataset[dataset["metal_loading_wt_pct"].notna()]
    assert set(loaded["paper_id"]) == {"HYC-0029"}
    assert loaded["dopant_concentration_at_pct"].isna().all()
    assert loaded["dopant_concentration_wt_pct"].isna().all()

    by_weight = dataset[dataset["dopant_concentration_wt_pct"].notna()]
    assert set(by_weight["paper_id"]) == {"HYC-0026"}
    assert by_weight["dopant_element"].notna().all()
    assert by_weight["dopant_concentration_method"].notna().all()


def test_characterization_only_rows_carry_characterization(dataset):
    """Rows with no uptake must still carry something, and no conditions.

    Seven now, up from the two HYC-0018 rows schema v1.1 recovered: HYC-0029's
    873 K activated sample and HYC-0026's four nitrogen-doped samples, each a
    real material whose uptake the paper plots without ever printing a number.
    """
    uptake = dataset[["uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"]]
    no_uptake = dataset[~uptake.notna().any(axis=1)]
    assert set(no_uptake["measurement_id"]) == {
        "HYC-0018-M5", "HYC-0018-M6",
        "HYC-0029-M2",
        "HYC-0026-M2", "HYC-0026-M4", "HYC-0026-M5", "HYC-0026-M7",
    }, sorted(no_uptake["measurement_id"])

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
