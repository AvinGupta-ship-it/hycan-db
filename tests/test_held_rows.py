"""Tests for the last two held rows and scripts/backfill_interlayer_spacing.py.

`docs/migration_held_rows_plan.md`. Two of these guards exist because a mutation
run found nothing else catching them:

* **Nothing pinned the graphite interlayer spacing.** The plan calls 0.339 the cell
  most at risk of being silently "corrected" — the paper prints 3.39 Å and every
  textbook says graphite is 3.35 Å. Changing the corpus value to 0.335 passed the
  entire suite.
* **`backfill_interlayer_spacing.py` had no tests.** Every other migration script
  in this project has a dedicated file; this one was relying on the dataset
  invariants, which check the result and not the script.

Each guard carries a MUTATION: line and each was confirmed to fail against the
mutation it names.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "backfill_interlayer_spacing.py"
DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import backfill_interlayer_spacing as bis  # noqa: E402


def rows_by_id() -> dict[str, dict[str, str]]:
    with DATASET.open(encoding="utf-8", newline="") as handle:
        return {r["measurement_id"]: r for r in csv.DictReader(handle)}


def run_script(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def pre_image(tmp_path: Path) -> Path:
    """The dataset with the backfill undone, so the script can be run for real."""
    target = tmp_path / "repo" / "data" / "raw" / "measurements_v0.1.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    header, rows = bis.read_rows(DATASET)
    idx = {name: header.index(name) for name in header}
    out = [list(r) for r in rows]
    for row in out:
        mid = row[idx["measurement_id"]]
        if mid in bis.BACKFILL:
            row[idx["interlayer_spacing_nm"]] = ""
        if mid in bis.NOTES_APPEND:
            suffix = bis.NOTES_APPEND[mid]
            assert row[idx["notes"]].endswith(suffix), mid
            row[idx["notes"]] = row[idx["notes"]][: -len(suffix)]
    bis.write_rows(target, header, out, "\n", True)
    return target


# --- the two new rows -------------------------------------------------------


def test_the_areal_uptake_row_exists_and_is_the_only_one():
    """HYC-0011-M5. The row `areal_uptake_g_cm2` was added for, unwritten until now.

    MUTATION: blank the field -> this fails, and the field is an empty column again.
    """
    rows = rows_by_id()
    assert "HYC-0011-M5" in rows, "the FePc film's areal uptake row is missing"
    row = rows["HYC-0011-M5"]
    assert float(row["areal_uptake_g_cm2"]) == pytest.approx(2.5e-05)
    carriers = [m for m, r in rows.items() if r["areal_uptake_g_cm2"].strip()]
    assert carriers == ["HYC-0011-M5"]
    # No gravimetric uptake exists even in principle: the film was never weighed.
    for field in ("uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"):
        assert not row[field].strip()


def test_the_areal_exponent_is_negative_five_and_matches_the_papers_own_ratio():
    """The paper says this value is "about four times as large as that of sample 2".

    Sample 2's areal uptake is in HYC-0011-M4's `notes` as 6.3e-6 g/cm2, and the
    ratio is what fixes the exponent independently of a text layer that deletes
    superscript minus signs. 2.5e-5 / 6.3e-6 = 3.97. No other exponent is close:
    +5 gives 4e10, -3 gives 397, -7 gives 0.0397.

    MUTATION: set the field to 2.5e-04 or 2.5e-06 -> the ratio leaves the "about
    four" window and this fails.
    """
    value = float(rows_by_id()["HYC-0011-M5"]["areal_uptake_g_cm2"])
    ratio = value / 6.3e-06
    assert 3.5 < ratio < 4.5, f"ratio to sample 2 is {ratio}, not 'about four'"


def test_the_graphite_row_records_the_papers_spacing_and_not_the_textbooks():
    """HYC-0015-M3, and the reason this test exists.

    **The paper prints 3.39 A. Graphite's commonly quoted (002) spacing is
    3.35 A.** A reader who knows graphite, or a model completing from its weights,
    will read 0.339 as a typo and "fix" it. Nothing in the suite caught a change to
    0.335 until this test, which is precisely the §3.11 "controlled value guessed"
    failure applied to a number rather than a vocabulary.

    The paper's own arithmetic supports 3.39: Bragg at its stated 2-theta = 26.32
    deg with Cu K-alpha gives 1.5406 / (2 sin 13.16 deg) = 3.383 A.

    MUTATION: set the field to 0.335 -> this fails and says why.
    """
    row = rows_by_id()["HYC-0015-M3"]
    assert float(row["interlayer_spacing_nm"]) == pytest.approx(0.339), (
        "the paper prints 3.39 A; 0.335 nm is graphite's textbook value and is NOT "
        "what this paper reports"
    )
    import math

    bragg_angstrom = 1.5406 / (2 * math.sin(math.radians(26.32 / 2)))
    assert round(bragg_angstrom, 2) == pytest.approx(3.38, abs=0.01)
    assert abs(bragg_angstrom - 3.39) < 0.02, (
        "the paper's own 2-theta no longer supports its printed spacing"
    )


def test_the_graphite_row_is_characterization_only_and_carries_no_conditions():
    """The paper reports no hydrogen uptake for the graphite, confirmed twice.

    MUTATION: populate any uptake field or any condition -> this fails.
    """
    row = rows_by_id()["HYC-0015-M3"]
    for field in (
        "uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g",
        "volumetric_capacity_kg_m3", "adsorbed_phase_density_kg_m3",
        "areal_uptake_g_cm2", "temperature_k", "pressure_bar",
    ):
        assert not row[field].strip(), field
    assert row["temperature_unstated"].lower() in {"false", ""}
    assert row["pressure_unstated"].lower() in {"false", ""}
    assert row["measurement_method"] == "not_applicable"


def test_all_three_spacings_are_present_so_the_field_is_not_graphite_only():
    """The point of backfilling M1 and M2 in the same commit as M3.

    The paper's thesis is the collapse from 8.84 A to 3.85 A on reduction. Writing
    only the graphite would make this field mean "graphite only" and a reader
    filtering on it would conclude the paper measured no other spacing.

    MUTATION: revert either backfilled cell -> this fails.
    """
    rows = rows_by_id()
    assert float(rows["HYC-0015-M1"]["interlayer_spacing_nm"]) == pytest.approx(0.884)
    assert float(rows["HYC-0015-M2"]["interlayer_spacing_nm"]) == pytest.approx(0.385)
    carriers = sorted(m for m, r in rows.items() if r["interlayer_spacing_nm"].strip())
    assert carriers == ["HYC-0015-M1", "HYC-0015-M2", "HYC-0015-M3"]
    # The collapse the paper is about, asserted as an ordering rather than a value.
    assert (
        float(rows["HYC-0015-M1"]["interlayer_spacing_nm"])
        > float(rows["HYC-0015-M2"]["interlayer_spacing_nm"])
        > float(rows["HYC-0015-M3"]["interlayer_spacing_nm"])
    ), "GO > rGO > graphite is the paper's own finding"


def test_the_numeric_spacings_agree_with_the_prose_already_in_each_row():
    """Each row's `material_description` states its spacing in angstroms.

    MUTATION: change a numeric cell without its description -> this fails, which is
    what stops the field and the prose drifting apart.
    """
    for mid, angstrom in (
        ("HYC-0015-M1", "8.84"), ("HYC-0015-M2", "3.85"), ("HYC-0015-M3", "3.39"),
    ):
        row = rows_by_id()[mid]
        assert angstrom in row["material_description"], mid
        assert float(row["interlayer_spacing_nm"]) == pytest.approx(
            float(angstrom) / 10
        ), mid


# --- the backfill script ----------------------------------------------------


def test_running_the_backfill_on_its_pre_image_reproduces_the_committed_file(
    pre_image: Path,
) -> None:
    """MUTATION: change a value in BACKFILL or NOTES_APPEND -> the output diverges."""
    result = run_script("--dataset", str(pre_image), cwd=pre_image.parents[2])
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_image.read_bytes() == DATASET.read_bytes()


def test_the_pre_image_differs_from_the_committed_file(pre_image: Path) -> None:
    """Guards the round trip against passing trivially."""
    assert pre_image.read_bytes() != DATASET.read_bytes()


def test_the_backfill_refuses_to_run_twice(pre_image: Path) -> None:
    """MUTATION: drop the `already` precondition -> the second run is still refused,
    by the notes-duplication check, and writes nothing. Both guards are asserted
    here so removing either one is visible."""
    first = run_script("--dataset", str(pre_image), cwd=pre_image.parents[2])
    assert first.returncode == 0, first.stdout + first.stderr
    before = pre_image.read_bytes()
    second = run_script("--dataset", str(pre_image), cwd=pre_image.parents[2])
    assert second.returncode == 1
    assert "already" in second.stderr.lower()
    assert pre_image.read_bytes() == before, "a refused run must write nothing"


def test_the_backfill_dry_run_writes_nothing(pre_image: Path) -> None:
    """MUTATION: move the write above the --dry-run return -> this fails."""
    before = pre_image.read_bytes()
    result = run_script(
        "--dataset", str(pre_image), "--dry-run", cwd=pre_image.parents[2]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_image.read_bytes() == before


def test_the_backfill_refuses_a_row_count_it_does_not_expect(pre_image: Path) -> None:
    """MUTATION: drop the --expected-rows guard -> a truncated corpus is migrated."""
    result = run_script(
        "--dataset", str(pre_image), "--expected-rows", "999",
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 1
    assert "expected 999 data rows" in result.stderr


def test_the_backfill_refuses_a_changed_cell_count_it_does_not_expect(
    pre_image: Path,
) -> None:
    """MUTATION: drop the changed-cell guard -> a widened BACKFILL map applies
    without anyone noticing."""
    result = run_script(
        "--dataset", str(pre_image), "--expected-changed-cells", "9",
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 1
    assert "expected 9 changed cells" in result.stderr


def test_an_embedded_newline_stops_the_backfill_before_the_byte_check(
    pre_image: Path,
) -> None:
    """A newline in a cell breaks the line-to-row mapping the byte check needs.

    MUTATION: delete assert_line_mapping_is_sound -> the migration runs and its
    byte-level guarantee is unsound without saying so.
    """
    header, rows = bis.read_rows(pre_image)
    rows[0][header.index("notes")] += "\nsecond physical line"
    bis.write_rows(pre_image, header, rows, "\n", True)
    result = run_script("--dataset", str(pre_image), cwd=pre_image.parents[2])
    assert result.returncode == 1
    assert "embedded newline" in result.stderr


def test_the_backfill_scope_is_two_columns(pre_image: Path) -> None:
    """MUTATION: add a column to SCOPE_COLUMNS -> this fails, and the migration is
    permitted to touch a field its plan never named."""
    assert bis.SCOPE_COLUMNS == {"interlayer_spacing_nm", "notes"}
    assert set(bis.BACKFILL) == {"HYC-0015-M1", "HYC-0015-M2"}
    assert set(bis.NOTES_APPEND) == {"HYC-0015-M2"}


def test_the_rgo_note_records_the_papers_own_inconsistency(pre_image: Path) -> None:
    """The 3.85 A sentence says "chemical reduction by hydrogen" where the
    Experimental section used hydrazine. The assignment to rGO is upheld, and the
    conflict is published rather than smoothed.

    MUTATION: drop the note -> this fails, and a reader loses the one reason to
    doubt the assignment.
    """
    notes = rows_by_id()["HYC-0015-M2"]["notes"]
    assert "INTERNALLY INCONSISTENT" in notes
    assert "hydrazine" in notes
