"""Schema v1.2, stages 1-3: gaps 1, 2, 4, 5, 7, 8 and 9.

Plan: docs/migration_v1_2_plan.md.

Every check here exists because a real paper could not be recorded without it,
and each test names that paper. §6.7 requires that a new safety-critical check
be mutated and a test confirmed to fail; the mutation cases are marked
MUTATION: and each states the mutation it would catch.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from hycan.schema import MeasurementEntry
from hycan.validate import validate_row

from conftest import BASE_ROW, COLUMNS, make_row

REPO_ROOT = Path(__file__).resolve().parents[1]


def entry(**overrides) -> MeasurementEntry:
    data = dict(BASE_ROW)
    data.update(overrides)
    return MeasurementEntry(**data)


# ---------------------------------------------------------------------------
# Gap 1 -- an uptake reported only as a bound (HYC-0017)
# ---------------------------------------------------------------------------

def test_uptake_bound_defaults_to_exact():
    """Every pre-v1.2 row asserted an exact value, so that must be the default."""
    assert entry().uptake_bound == "exact"


@pytest.mark.parametrize("value", ["exact", "upper", "lower", "approximate"])
def test_uptake_bound_accepts_the_four_documented_values(value):
    assert entry(uptake_bound=value).uptake_bound == value


def test_uptake_bound_rejects_anything_else():
    """MUTATION: widening UptakeBound to str would let this through."""
    with pytest.raises(ValidationError):
        entry(uptake_bound="probably")


def test_an_upper_bound_row_is_recordable():
    """HYC-0017 at 290 K / 60 bar: 'the hydrogen uptake is below 0.2 wt.%'.

    Before v1.2 this had to be written as an exact 0.2, which would enter
    isotherm fits and Chahine comparisons as a measured point, or dropped.
    """
    row = entry(
        temperature_k=290, pressure_bar=60,
        uptake_wt_pct=0.2, uptake_bound="upper",
    )
    assert row.uptake_bound == "upper"
    assert row.uptake_wt_pct == 0.2


# ---------------------------------------------------------------------------
# Gap 2 -- a paper that never states a condition numerically
# (HYC-0011, HYC-0015, HYC-0009's TPD rows)
# ---------------------------------------------------------------------------

def test_an_uptake_row_still_needs_conditions_by_default():
    """MUTATION: dropping the `not getattr(self, flag)` term would pass this."""
    with pytest.raises(ValidationError, match="must state their conditions"):
        entry(temperature_k=None)


def test_temperature_may_be_null_when_the_paper_is_silent():
    """HYC-0011 and HYC-0015 report uptakes at 'room temperature', no number."""
    row = entry(temperature_k=None, temperature_unstated=True)
    assert row.temperature_k is None
    assert row.temperature_unstated is True


def test_pressure_may_be_null_when_the_paper_is_silent():
    """HYC-0009's TPD rows state an adsorption temperature but no pressure."""
    row = entry(pressure_bar=None, pressure_unstated=True)
    assert row.pressure_bar is None


def test_both_conditions_may_be_unstated_at_once():
    row = entry(
        temperature_k=None, temperature_unstated=True,
        pressure_bar=None, pressure_unstated=True,
    )
    assert (row.temperature_k, row.pressure_bar) == (None, None)


def test_the_flag_does_not_license_a_missing_flag_on_the_other_field():
    """Setting one flag must not excuse the other field."""
    with pytest.raises(ValidationError, match="pressure_bar"):
        entry(
            temperature_k=None, temperature_unstated=True,
            pressure_bar=None,
        )


@pytest.mark.parametrize(
    "flag,field,value",
    [
        ("temperature_unstated", "temperature_k", 298),
        ("pressure_unstated", "pressure_bar", 20),
    ],
)
def test_declaring_a_condition_unstated_while_stating_it_is_an_error(
    flag, field, value
):
    """A row cannot both state a condition and declare it unstated.

    MUTATION: deleting the contradiction loop lets a row claim its paper was
    silent while carrying the number, which would silently exclude a perfectly
    good row from any analysis that filters on the flag.
    """
    with pytest.raises(ValidationError, match="cannot both"):
        entry(**{flag: True, field: value})


def test_a_characterization_only_row_needs_no_flags():
    """v1.1's conditional rule is unchanged for uptake-free rows."""
    row = entry(
        temperature_k=None, pressure_bar=None,
        uptake_wt_pct=None, uptake_mmol_g=None, uptake_ml_stp_g=None,
        bet_surface_area_m2_g=1200,
    )
    assert row.temperature_unstated is False


# ---------------------------------------------------------------------------
# Gap 4 -- pairwise uptake consistency, and the false positive it fixes
# ---------------------------------------------------------------------------

def test_the_hyc_0004_m2_rounding_case_is_not_a_disagreement():
    """The corpus's pre-v1.2 warning was this row, and it was a false positive.

    HYC-0004-M2 reports 0.05 wt% and 0.268 mmol/g. 0.268 mmol/g is 0.0540 wt%,
    which rounds to 0.05 at the paper's own precision. A relative-only
    tolerance called that an 8% disagreement.

    MUTATION: removing the absolute-tolerance early return in
    _uptakes_disagree re-introduces the false positive and fails this test.
    """
    result = validate_row(make_row(uptake_wt_pct=0.05, uptake_mmol_g=0.268))
    assert "mmol/g and wt% inconsistent" not in result.warnings


def test_a_real_wt_pct_versus_mmol_disagreement_still_warns():
    """The fix must not blind the check: 1.0 wt% against 10 mmol/g is 2x off."""
    result = validate_row(make_row(uptake_wt_pct=1.0, uptake_mmol_g=10.0))
    assert "mmol/g and wt% inconsistent" in result.warnings


def test_ml_stp_versus_wt_pct_disagreement_warns():
    """HYC-0009's defect: a tabulated wt% and volume that differ by ~2.5x.

    Its 298 K rows report 0.12 wt% against 5.370 mL(STP)/g, which is 0.048 wt%.
    Before v1.2 nothing compared these two fields at all, so the contradiction
    had to be caught by a human reader.
    """
    result = validate_row(make_row(uptake_wt_pct=0.12, uptake_ml_stp_g=5.370))
    assert "mL(STP)/g and wt% inconsistent" in result.warnings


def test_ml_stp_versus_mmol_disagreement_warns():
    result = validate_row(make_row(uptake_mmol_g=6.0, uptake_ml_stp_g=5.370))
    assert "mL(STP)/g and mmol/g inconsistent" in result.warnings


def test_consistent_values_in_all_three_units_warn_about_none():
    """HYC-0004-M5: 1.29 wt%, 143 mL(STP)/g, and the matching mmol/g."""
    result = validate_row(
        make_row(uptake_wt_pct=1.29, uptake_mmol_g=6.4, uptake_ml_stp_g=143.0)
    )
    assert not [w for w in result.warnings if "inconsistent" in w]


def test_a_large_absolute_difference_warns_even_at_high_values():
    """The absolute floor must not swallow a real disagreement.

    MUTATION: raising _UPTAKE_ABS_TOLERANCE_WT_PCT to 1.0 would pass the
    rounding tests and fail this one.
    """
    result = validate_row(make_row(uptake_wt_pct=5.0, uptake_ml_stp_g=200.0))
    assert "mL(STP)/g and wt% inconsistent" in result.warnings


# ---------------------------------------------------------------------------
# Gap 5 -- vocabulary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value",
    ["physical_activation", "chemical_activation", "chemical_exfoliation"],
)
def test_new_synthesis_methods_are_accepted(value):
    """HYC-0022 (CO2 and KOH activation), HYC-0017 (chemical exfoliation)."""
    assert entry(synthesis_method=value).synthesis_method == value


def test_not_applicable_measurement_method_is_accepted():
    """A characterization-only row records no measurement, so 'unknown' lied."""
    row = entry(
        temperature_k=None, pressure_bar=None,
        uptake_wt_pct=None, uptake_mmol_g=None, uptake_ml_stp_g=None,
        bet_surface_area_m2_g=800,
        measurement_method="not_applicable",
    )
    assert row.measurement_method == "not_applicable"


def test_existing_synthesis_vocabulary_is_unchanged():
    """The migration is additive: nothing was removed or renamed."""
    for value in (
        "arc_discharge", "laser_ablation", "cvd", "hipco", "comocat",
        "chemical_oxidation", "chemical_reduction", "thermal_reduction",
        "pyrolysis", "template_synthesis", "carbonization",
        "carbide_chlorination", "commercial", "unknown", "other",
    ):
        assert entry(synthesis_method=value).synthesis_method == value


# ---------------------------------------------------------------------------
# Gaps 7 and 8 -- supported metal, and dopant concentration by weight
# ---------------------------------------------------------------------------

def test_metal_loading_is_separate_from_dopant_concentration():
    """HYC-0029's Co is an impregnated particle; HYC-0025's B is a lattice dopant.

    Collapsing them into one field would make the spillover subset
    uninterpretable, so a row may legitimately carry both.
    """
    row = entry(
        metal_element="Co", metal_loading_wt_pct=14.62,
        dopant_element="B", dopant_concentration_at_pct=3.86,
    )
    assert (row.metal_element, row.metal_loading_wt_pct) == ("Co", 14.62)
    assert (row.dopant_element, row.dopant_concentration_at_pct) == ("B", 3.86)


def test_residual_metal_is_separate_from_intentional_loading():
    """HYC-0029 reports both: 2.02 wt% Co loaded, 1.02 wt% Co left from synthesis."""
    row = entry(
        metal_element="Co", metal_loading_wt_pct=2.02,
        residual_metal_element="Co", residual_metal_wt_pct=1.02,
    )
    assert row.residual_metal_wt_pct == 1.02


def test_dopant_concentration_by_weight_is_recordable():
    """HYC-0026 reports nitrogen only in wt% (0.20-15.07), never in at%."""
    row = entry(
        dopant_element="N",
        dopant_concentration_wt_pct=15.07,
        dopant_concentration_method="elemental_analysis",
    )
    assert row.dopant_concentration_wt_pct == 15.07


@pytest.mark.parametrize(
    "field", [
        "metal_loading_wt_pct", "residual_metal_wt_pct",
        "dopant_concentration_wt_pct",
    ],
)
@pytest.mark.parametrize("bad", [-0.1, 100.1])
def test_weight_percent_fields_are_bounded_to_0_100(field, bad):
    """MUTATION: dropping ge/le lets a 300 wt% loading in."""
    with pytest.raises(ValidationError):
        entry(**{field: bad})


def test_composition_method_is_a_controlled_vocabulary():
    with pytest.raises(ValidationError):
        entry(dopant_concentration_method="eyeballed")


# ---------------------------------------------------------------------------
# Gap 9 -- non-isothermal measurements (HYC-0029)
# ---------------------------------------------------------------------------

def test_measurement_mode_defaults_to_isothermal():
    """True of all 156 pre-v1.2 rows and of every Phase C paper but HYC-0029."""
    assert entry().measurement_mode == "isothermal"


@pytest.mark.parametrize(
    "value", ["isothermal", "temperature_cycle", "TPD", "flow"]
)
def test_measurement_mode_accepts_the_four_documented_values(value):
    assert entry(measurement_mode=value).measurement_mode == value


def test_a_temperature_cycle_row_can_state_its_reference_state():
    """HYC-0029 cycles 303 -> 673 -> 303 K, so its uptake is referenced to 673 K.

    Without the reference temperature the recorded value has no defined
    reference state and is not commensurable with an isothermal uptake.
    """
    row = entry(
        temperature_k=303, pressure_bar=1.01325,
        measurement_mode="temperature_cycle",
        reference_temperature_k=673,
    )
    assert row.reference_temperature_k == 673


def test_reference_temperature_may_exceed_the_measurement_ceiling():
    """673 K is above temperature_k's 500 K ceiling, and correctly so.

    A desorption endpoint is not a measurement temperature.
    """
    assert entry(reference_temperature_k=673).reference_temperature_k == 673
    with pytest.raises(ValidationError):
        entry(temperature_k=673)


def test_reference_temperature_is_still_bounded():
    """MUTATION: dropping le=1500 would accept an implausible 5000 K."""
    with pytest.raises(ValidationError):
        entry(reference_temperature_k=5000)


# ---------------------------------------------------------------------------
# The migration script itself
# ---------------------------------------------------------------------------

def run_migration(*args, cwd) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "migrate_v1_2.py"), *args],
        capture_output=True, text=True, cwd=cwd,
    )


@pytest.fixture
def pre_migration_dataset(tmp_path):
    """A 40-column dataset, i.e. the shape the migration expects to find."""
    pre_columns = [c for c in COLUMNS if c not in _V1_2_COLUMNS]
    assert len(pre_columns) == 40
    path = tmp_path / "measurements.csv"
    row = make_row()
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(pre_columns)
        for _ in range(2):
            writer.writerow(
                ["" if row.get(c) is None else str(row.get(c, ""))
                 for c in pre_columns]
            )
    return path


_V1_2_COLUMNS = (
    "uptake_bound", "temperature_unstated", "pressure_unstated",
    "measurement_mode", "reference_temperature_k", "metal_element",
    "metal_loading_wt_pct", "residual_metal_element", "residual_metal_wt_pct",
    "dopant_concentration_wt_pct", "dopant_concentration_method",
)


def test_the_migration_refuses_to_run_twice(pre_migration_dataset, tmp_path):
    first = run_migration(
        "--dataset", str(pre_migration_dataset),
        "--backup-dir", str(tmp_path / "bk"), "--expected-rows", "2", cwd=tmp_path,
    )
    assert first.returncode == 0, first.stdout + first.stderr
    second = run_migration(
        "--dataset", str(pre_migration_dataset),
        "--backup-dir", str(tmp_path / "bk"), "--expected-rows", "2", cwd=tmp_path,
    )
    assert second.returncode != 0
    assert "already run" in second.stdout + second.stderr


def test_a_dry_run_leaves_the_dataset_byte_identical(
    pre_migration_dataset, tmp_path
):
    before = pre_migration_dataset.read_bytes()
    result = run_migration(
        "--dataset", str(pre_migration_dataset), "--dry-run",
        "--backup-dir", str(tmp_path / "bk"), "--expected-rows", "2", cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_migration_dataset.read_bytes() == before


def test_the_migration_changes_no_cell_in_the_existing_columns(
    pre_migration_dataset, tmp_path
):
    """The property that makes this migration's verification assertable."""
    original = list(csv.reader(
        pre_migration_dataset.read_text(encoding="utf-8").splitlines()
    ))
    result = run_migration(
        "--dataset", str(pre_migration_dataset),
        "--backup-dir", str(tmp_path / "bk"), "--expected-rows", "2", cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "cells changed in columns 1-40: 0" in result.stdout

    after = list(csv.reader(
        pre_migration_dataset.read_text(encoding="utf-8").splitlines()
    ))
    assert len(after) == len(original)
    for before_row, after_row in zip(original, after):
        assert after_row[:40] == before_row
        assert len(after_row) == 51


def test_the_migration_refuses_a_ragged_file(pre_migration_dataset, tmp_path):
    """MUTATION: dropping the width check lets a shifted file through."""
    with open(pre_migration_dataset, "a", encoding="utf-8", newline="") as handle:
        handle.write(",".join(["x"] * 39) + "\n")
    result = run_migration(
        "--dataset", str(pre_migration_dataset),
        "--backup-dir", str(tmp_path / "bk"), "--expected-rows", "2", cwd=tmp_path,
    )
    assert result.returncode != 0
    assert "differing width" in result.stdout + result.stderr


def test_the_migration_refuses_a_file_of_the_wrong_column_count(tmp_path):
    path = tmp_path / "narrow.csv"
    path.write_text("a,b,c\n1,2,3\n", encoding="utf-8")
    result = run_migration(
        "--dataset", str(path), "--backup-dir", str(tmp_path / "bk"), "--expected-rows", "-1",
        cwd=tmp_path,
    )
    assert result.returncode != 0
    assert "expected 40 columns" in result.stdout + result.stderr


def test_the_migration_backs_up_before_writing(pre_migration_dataset, tmp_path):
    backup_dir = tmp_path / "bk"
    before = pre_migration_dataset.read_bytes()
    result = run_migration(
        "--dataset", str(pre_migration_dataset),
        "--backup-dir", str(backup_dir), "--expected-rows", "2", cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    backups = list(backup_dir.glob("measurements_v0.1.prev1_2.*.csv"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == before

