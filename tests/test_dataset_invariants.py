"""Invariants the published dataset must hold (manual §11.1, §11.5, §8.5).

These test the real file, not a fixture. Every other test module builds its
own data, which means none of them would notice the dataset itself drifting.
Skipped when the dataset is absent so the suite still runs on a bare clone.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from hycan.schema import MeasurementEntry
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
    assert len(columns) == 67
    assert columns[0] == "paper_id"
    # v1.1 appended 39-40; v1.2 appended 41-51; v1.3 appended 52-67. Every one
    # went on the end precisely so that positional appends keep working, and this
    # pins that.
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
    assert columns[51:67] == [
        "micropore_surface_area_m2_g",
        "external_surface_area_m2_g",
        "pore_volume_method",
        "pore_volume_probe_gas",
        "micropore_volume_co2_cm3_g",
        "mesopore_volume_cm3_g",
        "ultramicropore_cutoff_nm",
        "pore_diameter_method",
        "volumetric_capacity_kg_m3",
        "volumetric_capacity_basis",
        "volumetric_capacity_includes_compressed_gas",
        "adsorbed_phase_density_kg_m3",
        "packing_density_g_cm3",
        "skeletal_density_g_cm3",
        "areal_uptake_g_cm2",
        "interlayer_spacing_nm",
    ]


def test_surface_area_method_partitions_the_corpus_cleanly(dataset):
    """v1.3 gap 3. The three no-area values mean three different things.

    unspecified  -> an area IS reported, method not stated.
    none         -> the paper reports no area for any sample.
    not_reported -> this sample has none, in a paper that reports areas for
                    its others.

    Before v1.3 all three collapsed onto `unspecified` and 24 rows sat there with
    an empty area field. validate.py enforces this at dataset level; this asserts
    it against the real corpus so a regression shows up here too.
    """
    area_fields = [
        "bet_surface_area_m2_g",
        "langmuir_surface_area_m2_g",
        "micropore_surface_area_m2_g",
        "external_surface_area_m2_g",
    ]
    has_area = dataset[area_fields].notna().any(axis=1)

    unspecified = dataset[dataset["surface_area_method"] == "unspecified"]
    assert len(unspecified) > 0
    assert has_area[unspecified.index].all(), (
        "a row on 'unspecified' with no area: "
        f"{unspecified[~has_area[unspecified.index]]['measurement_id'].tolist()}"
    )

    for value in ("none", "not_reported"):
        rows = dataset[dataset["surface_area_method"] == value]
        assert len(rows) > 0, value
        assert not has_area[rows.index].any(), (
            f"a row on '{value}' carrying an area: "
            f"{rows[has_area[rows.index]]['measurement_id'].tolist()}"
        )

    papers_with_area = set(dataset[has_area]["paper_id"])
    not_reported = dataset[dataset["surface_area_method"] == "not_reported"]
    for paper in set(not_reported["paper_id"]):
        assert paper in papers_with_area, (
            f"{paper} uses 'not_reported' but reports no area for any sample; "
            f"'none' is the correct value"
        )
    for paper in set(dataset[dataset["surface_area_method"] == "none"]["paper_id"]):
        assert paper not in papers_with_area, (
            f"{paper} uses 'none' but does report an area for another sample; "
            f"'not_reported' is the correct value for the sample that lacks one"
        )


def test_every_ultramicropore_volume_states_its_cutoff(dataset):
    """v1.3 gap 6. The field exists to be comparable; a cutoff makes it so.

    HYC-0005 and HYC-0021 are cut at 0.7 nm. HYC-0022's V<1nm and HYC-0024's
    no-cutoff DR-CO2 volume were held out rather than mixed in, and a future
    append of either must carry its own cutoff rather than inheriting 0.7.
    """
    with_volume = dataset.dropna(subset=["ultramicropore_volume_cm3_g"])
    assert len(with_volume) == 29
    assert with_volume["ultramicropore_cutoff_nm"].notna().all(), (
        with_volume[with_volume["ultramicropore_cutoff_nm"].isna()][
            "measurement_id"
        ].tolist()
    )
    assert set(with_volume["ultramicropore_cutoff_nm"]) == {0.7}
    assert set(with_volume["paper_id"]) == {"HYC-0005", "HYC-0021"}


def test_every_volumetric_capacity_states_its_basis(dataset):
    """v1.3 gap 10. Per pore volume and per tank volume differ by over 2x."""
    with_capacity = dataset.dropna(subset=["volumetric_capacity_kg_m3"])
    assert with_capacity["volumetric_capacity_basis"].notna().all(), (
        with_capacity[with_capacity["volumetric_capacity_basis"].isna()][
            "measurement_id"
        ].tolist()
    )


def test_rows_whose_uptake_does_not_convert_to_wt_pct_are_enumerated(dataset):
    """v1.3 §4a. A null wt% is dropped silently by a mean, so name the rows.

    v1.3 admits a row whose only uptake is volumetric or areal, because HYC-0024
    reports nothing else and computing a wt% would be this project's arithmetic
    rather than the paper's measurement. The hazard is that such a row passes a
    "reports uptake" filter and then contributes nothing to a gravimetric
    statistic. Enumerating them by id means one cannot appear unnoticed -- the
    same discipline as the bounded-uptake test.

    Ten of the eleven are HYC-0024's: that paper's only tabulated hydrogen
    quantities are volumetric, so ten rows carry Ms and/or an adsorbed-phase
    density with no gravimetric value. Its eleventh row, HYC-0024-M4, is NOT here
    -- that sample is KUA1, for which the paper states "close to 1 wt %" in its
    abstract and conclusions, recorded with uptake_bound = approximate.

    **The eleventh is HYC-0011-M5, and it is a different shape of the same
    problem.** Its uptake is AREAL, in g/cm2, because the FePc film was never
    weighed -- so no wt% can be formed even in principle, not merely "the paper
    did not tabulate one". It is the corpus's only row carrying
    `areal_uptake_g_cm2`.
    """
    non_convertible = dataset[
        dataset["uptake_wt_pct"].isna()
        & dataset["uptake_mmol_g"].isna()
        & (
            dataset["volumetric_capacity_kg_m3"].notna()
            | dataset["adsorbed_phase_density_kg_m3"].notna()
            | dataset["areal_uptake_g_cm2"].notna()
        )
    ]
    assert set(non_convertible["measurement_id"]) == {
        "HYC-0024-M1",
        "HYC-0024-M2",
        "HYC-0024-M3",
        "HYC-0024-M5",
        "HYC-0024-M6",
        "HYC-0024-M7",
        "HYC-0024-M8",
        "HYC-0024-M9",
        "HYC-0024-M10",
        "HYC-0024-M11",
        "HYC-0011-M5",
    }


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
    belongs to a different quantity measured on a different instrument. HYC-0046
    reports 77 K surface-excess *saturation* values whose per-sample saturation
    pressure is not stated (only the 3200 m2/g ACA has an explicit 30 bar), so its
    other eight rows carry pressure_unstated.
    """
    flagged = dataset[
        _flag(dataset, "temperature_unstated") | _flag(dataset, "pressure_unstated")
    ]
    assert set(flagged["paper_id"]) == {
        "HYC-0009", "HYC-0011", "HYC-0015", "HYC-0026", "HYC-0046",
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
    # HYC-0024-M4 is the first `approximate`: its paper states "close to 1 wt %"
    # in the abstract and conclusions and tabulates no per-sample wt% at all,
    # so 1.0 is the paper's own rounded prose figure rather than a measurement.
    assert set(bounded["measurement_id"]) == {
        "HYC-0029-M3", "HYC-0029-M4", "HYC-0017-M3", "HYC-0024-M4",
    }, sorted(bounded["measurement_id"])
    assert set(bounded["uptake_bound"]) == {"lower", "upper", "approximate"}
    upper = bounded[bounded["uptake_bound"] == "upper"]
    assert set(upper["measurement_id"]) == {"HYC-0017-M3"}
    approximate = bounded[bounded["uptake_bound"] == "approximate"]
    assert set(approximate["measurement_id"]) == {"HYC-0024-M4"}


def test_paper_level_fields_agree_across_every_row_of_a_paper(dataset):
    """Every row of one paper must carry the same title, doi, author, year, journal.

    **Added because a candidate row reached verification with another paper's
    title.** HYC-0015-M3's `title` was typed from memory as "Structural and
    surface modification of carbon nanotubes for enhanced hydrogen storage
    density" -- a string that appears nowhere in that PDF, for a paper that
    measures graphene oxide. Agent B caught it. Nothing else would have: these are
    row-local fields, every value was individually well-formed, and no validator
    compares one row against another row of the same paper.

    The correct title was already in the corpus on that paper's two existing rows
    and in references/bibliography.bib. This test is the cheap check that makes
    copying it the path of least resistance.

    MUTATION: change one row's `year` or `title` within a paper -> this fails and
    names the paper and the field.
    """
    problems = []
    for field in ("doi", "first_author", "year", "journal", "title"):
        for paper_id, values in dataset.groupby("paper_id")[field]:
            distinct = set(values.dropna())
            if len(distinct) > 1:
                problems.append(f"{paper_id}.{field}: {sorted(distinct)}")
    assert problems == [], problems


def test_metal_loading_is_not_confused_with_dopant_concentration(dataset):
    """Schema v1.2 gaps 7 and 8 exist to keep these two quantities apart.

    **This test previously asserted that they never co-occur on a row, and that
    was wrong.** It read:

        loaded = dataset[dataset["metal_loading_wt_pct"].notna()]
        assert set(loaded["paper_id"]) == {"HYC-0029"}
        assert loaded["dopant_concentration_at_pct"].isna().all()

    Keeping the *fields* apart is the real requirement and is preserved below.
    Asserting the two never appear on one row is a much stronger claim that the
    fields were never given, and that the corpus satisfied only by accident:
    HYC-0027's Pd-N-HEG is palladium metal on nitrogen-doped graphene, so a
    metal loading and a dopant concentration are **both correct on the same
    row**. It is the paper gaps 7 and 8 were added for, and it broke a test
    written as though they were mutually exclusive. The lesson is §6.7's --
    assert the property, not the corpus's current shape.

    MUTATION: put a metal loading into `dopant_concentration_wt_pct`, or drop
    `metal_element` from a loaded row -> the property assertions below fail. The
    co-occurrence enumeration still catches an *accidental* co-occurrence while
    letting the one deliberate case through.
    """
    loaded = dataset[dataset["metal_loading_wt_pct"].notna()]
    assert loaded["metal_element"].notna().all(), (
        "a metal loading with no metal_element names no metal"
    )

    for column in ("dopant_concentration_at_pct", "dopant_concentration_wt_pct"):
        doped = dataset[dataset[column].notna()]
        assert doped["dopant_element"].notna().all(), (
            f"{column} is populated on a row that names no dopant_element"
        )
        assert (doped["dopant_element"] != doped["metal_element"]).all(), (
            f"{column} holds a concentration for the row's own metal_element, "
            f"which is the confusion gaps 7 and 8 exist to prevent"
        )

    # Rows where a metal loading and a dopant concentration are both correct,
    # enumerated so a new accidental one still fails here.
    both = dataset[
        dataset["metal_loading_wt_pct"].notna()
        & (
            dataset["dopant_concentration_at_pct"].notna()
            | dataset["dopant_concentration_wt_pct"].notna()
        )
    ]
    assert set(both["measurement_id"]) == {"HYC-0027-M4", "HYC-0027-M5"}, (
        "Pd-N-HEG is the only material in the corpus carrying both a metal "
        "loading and a dopant concentration"
    )
    assert set(both["metal_element"]) == {"Pd"}
    assert set(both["dopant_element"]) == {"N"}

    by_weight = dataset[dataset["dopant_concentration_wt_pct"].notna()]
    # +HYC-0039: its ammonia-treated AC (S2) carries 2.0 wt% N by CHNS; the
    # metal-decorated ammonia-treated composites keep dopant_element=N but no
    # concentration (the 2.0 wt% was measured on the support, not re-measured on
    # the composite), so only S2 is by-weight here.
    assert set(by_weight["paper_id"]) == {
        "HYC-0026", "HYC-0032", "HYC-0033", "HYC-0034", "HYC-0039"
    }
    assert by_weight["dopant_concentration_method"].notna().all()


def test_characterization_only_rows_carry_characterization(dataset):
    """Rows with no uptake must still carry something, and no conditions.

    Fourteen now, up from the two HYC-0018 rows schema v1.1 recovered: HYC-0029's
    873 K activated sample, HYC-0026's four nitrogen-doped samples, HYC-0007's
    four ACFs, HYC-0015's pristine graphite, and HYC-0033's two boron-doped
    characterization rows -- each a real material whose uptake the paper either
    does not measure or plots without ever printing a number.

    **"No uptake" must mean no uptake OF ANY KIND, not merely no gravimetric
    value.** Before v1.3 those were the same thing. They are not any more:
    HYC-0024's rows carry a volumetric capacity and an adsorbed-phase density
    with no wt%, and they DO state conditions, so testing only the three
    gravimetric fields would wrongly classify them as characterization-only and
    then fail on the conditions assertions below.
    """
    gravimetric = ["uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"]
    non_convertible = [
        "volumetric_capacity_kg_m3",
        "adsorbed_phase_density_kg_m3",
        "areal_uptake_g_cm2",
    ]
    any_uptake = dataset[gravimetric + non_convertible].notna().any(axis=1)
    no_uptake = dataset[~any_uptake]
    assert set(no_uptake["measurement_id"]) == {
        "HYC-0018-M5", "HYC-0018-M6",
        "HYC-0029-M2",
        "HYC-0026-M2", "HYC-0026-M4", "HYC-0026-M5", "HYC-0026-M7",
        "HYC-0007-M5", "HYC-0007-M6", "HYC-0007-M7", "HYC-0007-M8",
        "HYC-0015-M3",
        "HYC-0033-M1", "HYC-0033-M2",
        # HYC-0044's five characterization-only carbon fibres (the PCF_L series and
        # PCF_H 0.5/0.1): Table 1 texture only, H2 never measured (any value is in the
        # unavailable supplementary Fig S1).
        "HYC-0044-M8", "HYC-0044-M9", "HYC-0044-M10", "HYC-0044-M11", "HYC-0044-M12",
    }, sorted(no_uptake["measurement_id"])

    # **The list is read off schema.py, not restated here.** This test used to
    # carry its own copy of ten field names, and that copy went stale twice: it
    # needed the v1.3 component-area fields or HYC-0007's four rows looked
    # uncharacterized, and it omitted `interlayer_spacing_nm`, which would have
    # rejected HYC-0015-M3 -- a row whose ONLY datum is an interlayer spacing and
    # which the schema's own validator accepts. A duplicated list is a list that
    # expires; §0 says schema.py is authoritative, so read it.
    # Pydantic captures a leading-underscore class tuple as a private attribute,
    # so the class attribute is a descriptor rather than the tuple; its default is
    # where the value lives. Reaching through __private_attributes__ is worth the
    # ugliness -- the alternative is a second copy of the list, which is what went
    # stale twice.
    characterization = list(
        MeasurementEntry.__private_attributes__["_CHARACTERIZATION_FIELDS"].default
    )
    assert "interlayer_spacing_nm" in characterization
    assert len(characterization) >= 13
    assert no_uptake[characterization].notna().any(axis=1).all(), sorted(
        no_uptake.loc[
            ~no_uptake[characterization].notna().any(axis=1), "measurement_id"
        ]
    )
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

def test_paired_total_and_excess_rows_are_enumerated(dataset):
    """Rows reporting the SAME measurement twice, as total and as excess.

    HYC-0031 is the first paper in the corpus to report `total` uptake, and it
    reports total and excess at the same sample, temperature and pressure --
    one measurement expressed two ways. Before it, NO sample/T/P group in the
    corpus carried more than one `uptake_type`.

    Any statistic that does not filter on `uptake_type` double-counts these.
    Measured: the corpus-wide mean of `uptake_wt_pct` is 1.9966 excluding
    `total` and 2.1560 including it, an 8% shift from 13 pairs. `fig3_chahine`
    now excludes `total` for this reason and because the Chahine rule bounds
    adsorbed uptake, not total
    (docs/migration_chahine_excess_only_plan.md); there is still no canonical
    §12.3 filter function in the code, so they are enumerated here on the
    precedent of the non-convertible rows above -- a silent double count is the
    §12.3 failure mode and this is what makes it loud.

    MUTATION: append a paper reporting paired total/excess rows without
    deciding how they are aggregated -> this fails and names them.
    """
    groups = dataset.groupby(["sample_id", "temperature_k", "pressure_bar"])
    paired = [ids for _, grp in groups
              if grp["uptake_type"].nunique() > 1
              for ids in [set(grp["measurement_id"])]]
    flat = sorted(i for s in paired for i in s)
    # +HYC-0045-M1/M6: FA-ZTC1 reports a total (7.3 wt%) and an excess (6.2 wt%) at the
    # same 77 K / 20 bar -- the second total/excess paper after HYC-0031.
    assert flat == ['HYC-0031-M1', 'HYC-0031-M10', 'HYC-0031-M11', 'HYC-0031-M12', 'HYC-0031-M13', 'HYC-0031-M14', 'HYC-0031-M16', 'HYC-0031-M17', 'HYC-0031-M18', 'HYC-0031-M19', 'HYC-0031-M2', 'HYC-0031-M20', 'HYC-0031-M21', 'HYC-0031-M22', 'HYC-0031-M23', 'HYC-0031-M25', 'HYC-0031-M26', 'HYC-0031-M28', 'HYC-0031-M29', 'HYC-0031-M3', 'HYC-0031-M31', 'HYC-0031-M32', 'HYC-0031-M4', 'HYC-0031-M5', 'HYC-0031-M6', 'HYC-0031-M9', 'HYC-0045-M1', 'HYC-0045-M6'], (
        "the set of rows reporting one measurement under two uptake types has "
        "changed. Every corpus-wide statistic over uptake_wt_pct must filter "
        "on uptake_type, or it double-counts these rows."
    )
    # Every pair must be exactly one total and one excess, not two of a kind.
    for _, grp in groups:
        if grp["uptake_type"].nunique() > 1:
            assert sorted(grp["uptake_type"]) == ["excess", "total"], (
                f"unexpected uptake_type pairing: {sorted(grp['uptake_type'])}"
            )
