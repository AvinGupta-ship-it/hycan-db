"""Tests for schema v1.3 — gaps 3, 6 and 10, plus the migration that applies it.

Each guard carries a MUTATION: line naming the change it would catch, per the
convention started in test_schema_v1_2.py. §6.7 makes a passing suite weak
evidence, so every guard here was run against the mutation it names and confirmed
to fail.

Gap 3  — a paper can report more than one surface area, or none for some samples.
Gap 6  — pore fields had no method, probe gas or cutoff.
Gap 10 — volumetric, areal and structural quantities had no field.
"""

from __future__ import annotations

import csv
import io
import subprocess
import sys
from pathlib import Path

import pytest

from hycan.schema import validate_row
from hycan.validate import validate_row as validate_row_full

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "migrate_v1_3.py"
DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"

NEW_COLUMN_NAMES = [
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


def base_row(**overrides):
    """A minimal valid v1.3 row: characterization only, BET area, no uptake."""
    row = {
        "paper_id": "HYC-9999",
        "doi": "10.1000/test",
        "first_author": "Tester",
        "year": 2020,
        "journal": "J. Test",
        "title": "A test paper",
        "sample_id": "HYC-9999-S1",
        "measurement_id": "HYC-9999-M1",
        "material_class": "activated_carbon",
        "material_description": "Test activated carbon",
        "bet_surface_area_m2_g": 1000.0,
        "surface_area_method": "BET",
        "uptake_type": "unspecified",
        "measurement_method": "not_applicable",
        "source_location": "Table 1",
        "extraction_method": "table_direct",
        "extraction_confidence": 5,
        "reproducibility_tier": "B",
        "extractor": "test",
        "extraction_date": "2026-09-25",
    }
    row.update(overrides)
    return row


def uptake_row(**overrides):
    """A minimal valid row that reports a gravimetric uptake."""
    row = base_row(
        temperature_k=77.0,
        pressure_bar=1.0,
        uptake_wt_pct=2.0,
        measurement_method="volumetric_sieverts",
    )
    row.update(overrides)
    return row


# --- Gap 3: more than one surface area, and three kinds of "no area" ---------


def test_the_two_new_surface_area_fields_accept_hyc_0007s_values():
    """Gap 3b. Eighteen measured values that previously had nowhere to go."""
    ok, errors = validate_row(
        base_row(
            bet_surface_area_m2_g=None,
            micropore_surface_area_m2_g=2250.0,
            external_surface_area_m2_g=70.0,
            surface_area_method="alpha_s_plot",
        )
    )
    assert ok, errors


@pytest.mark.parametrize("method", ["alpha_s_plot", "t_plot", "not_reported"])
def test_the_new_surface_area_methods_are_accepted(method):
    """MUTATION: drop any of the three from the Literal -> this fails."""
    area = None if method == "not_reported" else 1000.0
    ok, errors = validate_row(
        base_row(
            bet_surface_area_m2_g=area,
            micropore_volume_cm3_g=0.4 if area is None else None,
            surface_area_method=method,
        )
    )
    assert ok, errors


def test_an_unknown_surface_area_method_is_still_refused():
    """MUTATION: widen SurfaceAreaMethod to str -> this fails."""
    ok, _ = validate_row(base_row(surface_area_method="alphas_plot"))
    assert not ok


def test_none_and_not_reported_must_not_carry_an_area():
    """MUTATION: delete error rule 3 -> this fails.

    Both values mean the sample has no reported surface area. A value alongside
    either is a contradiction, not a rounding question.
    """
    for method in ("none", "not_reported"):
        for field in (
            "bet_surface_area_m2_g",
            "langmuir_surface_area_m2_g",
            "micropore_surface_area_m2_g",
            "external_surface_area_m2_g",
        ):
            row = base_row(
                bet_surface_area_m2_g=None,
                micropore_volume_cm3_g=0.4,
                surface_area_method=method,
            )
            row[field] = 900.0
            ok, errors = validate_row(row)
            assert not ok, f"{method} + {field} was accepted"
            assert any(method in e for e in errors), errors


def _dataset_errors(*rows):
    """Run validate_dataset over `rows` and return (n_rows_with_errors, all errors)."""
    import pandas as pd

    from hycan.validate import validate_dataset

    report = validate_dataset(pd.DataFrame(list(rows)))
    bad = [r for r in report.results if not r.is_valid]
    return len(bad), [e for r in report.results for e in r.errors]


def test_the_three_no_area_values_are_checked_at_dataset_level():
    """MUTATION: delete dataset check 1b -> all three assertions fail.

    This is the invariant backfills B and C create, and it is deliberately NOT a
    model validator. `not_reported` means "this sample lacks an area in a paper
    that reports areas for its others", which cannot be evaluated from one row --
    it is a fact about the paper's other rows. So the check lives in
    validate_dataset, where it can also verify the two stronger properties a
    row-local check cannot: that `not_reported` is not used in a paper with no
    areas at all, and that `none` is not used in a paper that has them.

    24 rows used to sit on `unspecified` with nothing in the field,
    indistinguishable from a measured area whose method the paper omitted.
    """
    no_area = dict(bet_surface_area_m2_g=None, micropore_volume_cm3_g=0.4)

    # 1. `unspecified` with no area anywhere in the paper.
    count, errors = _dataset_errors(
        base_row(surface_area_method="unspecified", **no_area)
    )
    assert count == 1
    assert any("'unspecified' with no area" in e for e in errors), errors

    # 2. `not_reported` in a paper that reports no area for any sample.
    count, errors = _dataset_errors(
        base_row(surface_area_method="not_reported", **no_area)
    )
    assert count == 1
    assert any("reports no surface area for any sample" in e for e in errors), errors

    # 3. `none` in a paper that DOES report an area for another sample.
    count, errors = _dataset_errors(
        base_row(measurement_id="HYC-9999-M1", surface_area_method="BET"),
        base_row(measurement_id="HYC-9999-M2", surface_area_method="none", **no_area),
    )
    assert count == 1
    assert any("'not_reported' is the correct" in e for e in errors), errors


def test_the_valid_combinations_pass_at_dataset_level():
    """The mirror of the above: each value used correctly is clean."""
    no_area = dict(bet_surface_area_m2_g=None, micropore_volume_cm3_g=0.4)

    # A paper reporting areas for some samples and not others.
    count, errors = _dataset_errors(
        base_row(measurement_id="HYC-9999-M1", surface_area_method="BET"),
        base_row(
            measurement_id="HYC-9999-M2",
            surface_area_method="not_reported",
            **no_area,
        ),
    )
    assert count == 0, errors

    # A paper reporting no area at all.
    count, errors = _dataset_errors(
        base_row(surface_area_method="none", **no_area)
    )
    assert count == 0, errors

    # An area with no stated method.
    count, errors = _dataset_errors(base_row(surface_area_method="unspecified"))
    assert count == 0, errors


def test_unspecified_is_satisfied_by_any_of_the_four_area_fields():
    """A micropore-only paper on `unspecified` is legitimate."""
    for field in (
        "bet_surface_area_m2_g",
        "langmuir_surface_area_m2_g",
        "micropore_surface_area_m2_g",
        "external_surface_area_m2_g",
    ):
        row = base_row(bet_surface_area_m2_g=None, surface_area_method="unspecified")
        row[field] = 900.0
        ok, errors = validate_row(row)
        assert ok, (field, errors)


def test_parts_inconsistent_with_the_whole_warns_and_does_not_error():
    """MUTATION: make the area-sum check an ERROR -> this fails.

    HYC-0007 rounds areas to the nearest 10 m2/g, so this must tolerate rounding
    and flag only a real disagreement.
    """
    result = validate_row_full(
        base_row(
            bet_surface_area_m2_g=1000.0,
            micropore_surface_area_m2_g=300.0,
            external_surface_area_m2_g=100.0,
        )
    )
    assert result.is_valid
    assert any("external surface area" in w for w in result.warnings), result.warnings


def test_rounding_in_the_area_parts_does_not_warn():
    """MUTATION: make the area tolerance relative-only -> this fails.

    980 + 20 = 1000 exactly; 975 + 20 = 995 against a stated 1000 is one
    rounding step and must stay silent. Relative-only was the false positive
    that produced v1.2's removed warning type.
    """
    for micro, ext, total in ((980.0, 20.0, 1000.0), (975.0, 20.0, 1000.0)):
        result = validate_row_full(
            base_row(
                bet_surface_area_m2_g=total,
                micropore_surface_area_m2_g=micro,
                external_surface_area_m2_g=ext,
            )
        )
        assert result.is_valid
        assert not any(
            "external surface area" in w for w in result.warnings
        ), (micro, ext, total, result.warnings)


# --- Gap 6: method, probe gas, cutoff ---------------------------------------


def test_the_pore_method_vocabularies_are_closed():
    """MUTATION: widen any of the three to str -> this fails."""
    for field, bad in (
        ("pore_volume_method", "dubinin"),
        ("pore_volume_probe_gas", "nitrogen"),
        ("pore_diameter_method", "bjh"),
    ):
        ok, _ = validate_row(base_row(**{field: bad}))
        assert not ok, f"{field}={bad} was accepted"


def test_hyc_0019s_mixed_probe_gases_are_now_recordable():
    """Gap 6. Area by N2 at 77 K, micropore volume by CO2 at 273 K, same row.

    That combination is why HYC-0019's surface area falls while its micropore
    volume rises, and it was unrecordable before v1.3.
    """
    ok, errors = validate_row(
        base_row(
            surface_area_method="BET",
            micropore_volume_cm3_g=0.35,
            pore_volume_method="DR",
            pore_volume_probe_gas="CO2",
        )
    )
    assert ok, errors


def test_hyc_0024s_two_micropore_volumes_coexist():
    """Gap 6. DR on N2 at 77 K and DR on CO2 at 273 K are not interchangeable."""
    ok, errors = validate_row(
        base_row(
            micropore_volume_cm3_g=0.78,
            micropore_volume_co2_cm3_g=0.57,
            pore_volume_method="DR",
            pore_volume_probe_gas="N2",
        )
    )
    assert ok, errors


def test_an_ultramicropore_volume_without_its_cutoff_is_an_error():
    """MUTATION: delete error rule 1 -> this fails.

    The field exists to be comparable across the corpus. A value whose cutoff
    nobody stated is not comparable with one cut at 0.7 nm, which is why
    HYC-0022's 1 nm value and HYC-0024's no-cutoff value were held out.
    """
    ok, errors = validate_row(
        base_row(micropore_volume_cm3_g=0.4, ultramicropore_volume_cm3_g=0.2)
    )
    assert not ok
    assert any("ultramicropore_cutoff_nm" in e for e in errors), errors


def test_an_ultramicropore_volume_with_its_cutoff_is_fine():
    ok, errors = validate_row(
        base_row(
            micropore_volume_cm3_g=0.4,
            ultramicropore_volume_cm3_g=0.2,
            ultramicropore_cutoff_nm=0.7,
        )
    )
    assert ok, errors


def test_a_cutoff_alone_is_allowed():
    """A paper may state a cutoff for a quantity it reports as zero or omits."""
    ok, errors = validate_row(base_row(ultramicropore_cutoff_nm=1.0))
    assert ok, errors


def test_mesopore_volume_nests_inside_the_total():
    """MUTATION: drop the mesopore pair from the nesting check -> this fails."""
    result = validate_row_full(
        base_row(mesopore_volume_cm3_g=0.9, total_pore_volume_cm3_g=0.5)
    )
    assert not result.is_valid
    assert any("Mesopore volume exceeds" in e for e in result.errors), result.errors


def test_micropore_plus_mesopore_over_total_warns_but_does_not_error():
    """MUTATION: make the pore-sum check an ERROR -> this fails."""
    result = validate_row_full(
        base_row(
            micropore_volume_cm3_g=0.60,
            mesopore_volume_cm3_g=0.40,
            total_pore_volume_cm3_g=0.70,
        )
    )
    assert result.is_valid
    assert any("Micropore plus mesopore" in w for w in result.warnings), result.warnings


def test_pore_volume_rounding_does_not_warn():
    """MUTATION: make the pore-sum tolerance relative-only -> this fails."""
    result = validate_row_full(
        base_row(
            micropore_volume_cm3_g=0.42,
            mesopore_volume_cm3_g=0.10,
            total_pore_volume_cm3_g=0.50,
        )
    )
    assert result.is_valid
    assert not any("Micropore plus mesopore" in w for w in result.warnings)


# --- Gap 10: volumetric, areal, structural ---------------------------------


def test_a_volumetric_capacity_without_its_basis_is_an_error():
    """MUTATION: delete error rule 2 -> this fails.

    Per micropore volume and per tank volume differ by more than 2x in
    HYC-0024's own table, so an unqualified number is not interpretable.
    """
    ok, errors = validate_row(
        uptake_row(uptake_wt_pct=None, volumetric_capacity_kg_m3=11.8)
    )
    assert not ok
    assert any("volumetric_capacity_basis" in e for e in errors), errors


def test_hyc_0024s_row_shape_is_now_valid():
    """Gap 10 plus the §4a amendment, together.

    HYC-0024's only tabulated hydrogen quantities are volumetric. Before v1.3
    `at_least_one_uptake` rejected such a row outright, so adding the fields
    alone would not have released this paper.
    """
    ok, errors = validate_row(
        base_row(
            temperature_k=293.0,
            pressure_bar=100.0,
            measurement_method="gravimetric_microbalance",
            volumetric_capacity_kg_m3=11.8,
            volumetric_capacity_basis="tank_volume",
            volumetric_capacity_includes_compressed_gas=True,
            adsorbed_phase_density_kg_m3=16.34,
            packing_density_g_cm3=1.01,
            skeletal_density_g_cm3=1.73,
            micropore_volume_cm3_g=0.51,
            micropore_volume_co2_cm3_g=0.50,
            pore_volume_method="DR",
            pore_volume_probe_gas="N2",
        )
    )
    assert ok, errors


def test_a_gravimetric_uptake_still_needs_wt_pct_or_mmol():
    """MUTATION: drop the gravimetric branch of at_least_one_uptake -> fails.

    The §4a amendment NARROWS the old rule; it does not remove it. A row with
    only mL(STP)/g is still refused, because that unit converts.
    """
    ok, errors = validate_row(
        uptake_row(uptake_wt_pct=None, uptake_ml_stp_g=250.0)
    )
    assert not ok
    assert any("uptake_wt_pct" in e for e in errors), errors


def test_a_volumetric_only_row_still_needs_its_conditions():
    """MUTATION: leave the volumetric fields out of _UPTAKE_FIELDS -> this fails.

    If a volumetric-only row were not counted as reporting uptake it would be
    misfiled as characterization-only and its conditions would stop being
    required — HYC-0024 states 293 K and 10 MPa.
    """
    ok, errors = validate_row(
        base_row(
            volumetric_capacity_kg_m3=11.8,
            volumetric_capacity_basis="tank_volume",
        )
    )
    assert not ok
    assert any("conditions" in e for e in errors), errors


def test_hyc_0011s_areal_uptake_is_recordable():
    """Gap 10. The quantity that makes its 8.0 wt% headline checkable."""
    ok, errors = validate_row(
        base_row(
            bet_surface_area_m2_g=None,
            surface_area_method="none",
            temperature_unstated=True,
            pressure_bar=1.0,
            areal_uptake_g_cm2=6.3e-6,
        )
    )
    assert ok, errors


def test_hyc_0015s_interlayer_spacing_is_recordable():
    """Gap 10, the structural half."""
    ok, errors = validate_row(
        base_row(
            bet_surface_area_m2_g=None,
            surface_area_method="none",
            interlayer_spacing_nm=0.87,
        )
    )
    assert ok, errors


def test_the_new_numeric_fields_are_bounded():
    """MUTATION: drop any ge/le -> this fails."""
    for field, bad in (
        ("micropore_surface_area_m2_g", 5000.0),
        ("external_surface_area_m2_g", -1.0),
        ("micropore_volume_co2_cm3_g", 3.0),
        ("mesopore_volume_cm3_g", 4.0),
        ("ultramicropore_cutoff_nm", 3.0),
        ("volumetric_capacity_kg_m3", 300.0),
        ("adsorbed_phase_density_kg_m3", -1.0),
        ("packing_density_g_cm3", 6.0),
        ("skeletal_density_g_cm3", -0.1),
        ("areal_uptake_g_cm2", -1.0),
        ("interlayer_spacing_nm", -1.0),
    ):
        ok, _ = validate_row(base_row(**{field: bad}))
        assert not ok, f"{field}={bad} was accepted"


def test_the_compressed_gas_flag_defaults_to_false():
    """An adsorbed-phase quantity is the common case; Ms is the exception."""
    from hycan.schema import MeasurementEntry

    entry = MeasurementEntry.model_validate(base_row())
    assert entry.volumetric_capacity_includes_compressed_gas is False


def test_every_v1_3_field_defaults_so_a_pre_v1_3_row_stays_valid():
    """MUTATION: make any new field required -> this fails.

    The migration appends columns to 206 existing rows; a required new field
    would invalidate every one of them.
    """
    row = base_row()
    for name in NEW_COLUMN_NAMES:
        assert name not in row
    ok, errors = validate_row(row)
    assert ok, errors


# --- The migration script ---------------------------------------------------


def run_migration(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


BACKFILLED_TO_NOT_REPORTED = {
    "HYC-0016-M13",
    "HYC-0016-M14",
    "HYC-0022-M8",
    "HYC-0022-M9",
} | {f"HYC-0029-M{n}" for n in range(5, 17)}
BACKFILLED_TO_NONE_PAPERS = {"HYC-0002", "HYC-0027"}


@pytest.fixture
def pre_migration(tmp_path: Path) -> Path:
    """A 51-column copy of the dataset as it stood before v1.3.

    Works whether the real dataset is still pre-migration or already migrated, so
    these tests are runnable both before the migration is applied and forever
    after. Reversing the backfills touches only the rows the plan names;
    HYC-0011, HYC-0015 and HYC-0025 were already `none` before v1.3 and must stay
    that way, or the fixture would manufacture a pre-image that never existed.
    """
    (tmp_path / "data" / "raw").mkdir(parents=True)
    target = tmp_path / "data" / "raw" / "measurements_v0.1.csv"

    with DATASET.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    header, body = rows[0], rows[1:]

    if len(header) == 51:
        # Already the pre-image; copy byte for byte.
        target.write_bytes(DATASET.read_bytes())
        return tmp_path

    keep = len(header) - len(NEW_COLUMN_NAMES)
    assert header[keep:] == NEW_COLUMN_NAMES, (
        f"dataset has {len(header)} columns, neither 51 nor 67"
    )
    old_header = header[:keep]
    method = old_header.index("surface_area_method")
    mid_col = old_header.index("measurement_id")
    paper_col = old_header.index("paper_id")

    old_body = []
    for row in body:
        old = row[:keep]
        if (
            old[mid_col] in BACKFILLED_TO_NOT_REPORTED
            or old[paper_col] in BACKFILLED_TO_NONE_PAPERS
        ):
            old[method] = "unspecified"
        old_body.append(old)

    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(old_header)
    writer.writerows(old_body)
    target.write_text(buffer.getvalue(), encoding="utf-8", newline="")
    return tmp_path


def test_the_migration_adds_sixteen_columns_and_changes_53_cells(pre_migration: Path):
    """MUTATION: add or drop a column from NEW_COLUMNS -> this fails."""
    result = run_migration("--backup-dir", str(pre_migration / "bk"), cwd=pre_migration)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "51 -> 67 columns" in result.stdout
    assert "53 cell change(s)" in result.stdout


def test_the_migration_refuses_to_run_twice(pre_migration: Path):
    """MUTATION: drop the already-applied guard -> this fails."""
    first = run_migration("--backup-dir", str(pre_migration / "bk"), cwd=pre_migration)
    assert first.returncode == 0, first.stdout + first.stderr
    second = run_migration("--backup-dir", str(pre_migration / "bk"), cwd=pre_migration)
    assert second.returncode != 0
    assert "already been applied" in second.stdout + second.stderr


def test_dry_run_writes_nothing(pre_migration: Path):
    """MUTATION: make --dry-run write -> this fails."""
    path = pre_migration / "data" / "raw" / "measurements_v0.1.csv"
    before = path.read_bytes()
    result = run_migration(
        "--dry-run", "--backup-dir", str(pre_migration / "bk"), cwd=pre_migration
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert path.read_bytes() == before


def test_every_original_cell_survives_byte_identical(pre_migration: Path):
    """MUTATION: route the write through pandas -> this fails.

    The whole reason the script uses the csv module. Only the two columns the
    plan names may differ; every other original cell must be unchanged.
    """
    path = pre_migration / "data" / "raw" / "measurements_v0.1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        before = list(csv.reader(handle))
    assert (
        run_migration("--backup-dir", str(pre_migration / "bk"), cwd=pre_migration
                      ).returncode == 0
    )
    with path.open(encoding="utf-8", newline="") as handle:
        after = list(csv.reader(handle))

    old_header = before[0]
    assert after[0][: len(old_header)] == old_header
    allowed = {"surface_area_method"}
    for line, (old, new) in enumerate(zip(before[1:], after[1:]), start=2):
        for col, (a, b) in enumerate(zip(old, new[: len(old_header)])):
            if a != b:
                assert old_header[col] in allowed, (
                    f"csv line {line}: {old_header[col]} changed {a!r} -> {b!r}"
                )


def test_the_migration_preserves_the_line_ending_convention(pre_migration: Path):
    """MUTATION: hardcode lineterminator instead of detecting it -> this fails.

    Not hypothetical: the paper_tracking.csv migration the same day rewrote all
    31 lines' bytes because it assumed LF on a CRLF file, and its cell-level
    check passed anyway.
    """
    path = pre_migration / "data" / "raw" / "measurements_v0.1.csv"
    before = path.read_bytes()
    assert (
        run_migration("--backup-dir", str(pre_migration / "bk"), cwd=pre_migration
                      ).returncode == 0
    )
    after = path.read_bytes()
    assert after.count(b"\r\n") == before.count(b"\r\n")
    assert after.endswith(b"\n") == before.endswith(b"\n")
    assert len(after.split(b"\n")) == len(before.split(b"\n"))


def test_the_migration_refuses_a_wrong_column_count(tmp_path: Path):
    """MUTATION: drop the column-count guard -> this fails."""
    (tmp_path / "data" / "raw").mkdir(parents=True)
    (tmp_path / "data" / "raw" / "measurements_v0.1.csv").write_text(
        "a,b,c\n1,2,3\n", encoding="utf-8"
    )
    result = run_migration(
        "--expected-rows", "-1", "--backup-dir", str(tmp_path / "bk"), cwd=tmp_path
    )
    assert result.returncode != 0
    assert "expected 51 columns" in result.stdout + result.stderr


def test_the_migration_refuses_a_wrong_row_count(pre_migration: Path):
    """MUTATION: drop the row-count guard -> this fails."""
    path = pre_migration / "data" / "raw" / "measurements_v0.1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerows(rows + [rows[-1]])
    path.write_text(buffer.getvalue(), encoding="utf-8", newline="")
    result = run_migration("--backup-dir", str(pre_migration / "bk"), cwd=pre_migration)
    assert result.returncode != 0
    assert "expected 206 data rows" in result.stdout + result.stderr


def test_the_migration_backs_up_before_writing(pre_migration: Path):
    """MUTATION: drop the backup -> this fails."""
    backup_dir = pre_migration / "bk"
    result = run_migration("--backup-dir", str(backup_dir), cwd=pre_migration)
    assert result.returncode == 0, result.stdout + result.stderr
    backups = list(backup_dir.glob("measurements_v0.1.prev1_3.*.csv"))
    assert len(backups) == 1, f"expected one backup, found {backups}"
