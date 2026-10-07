"""Tests for scripts/migrate_hyc0016_m5.py and the correction it establishes.

Two kinds of test, as in test_migrate_relabel.py:

* A **pre-image** round trip -- the committed dataset with this migration's cell
  changes undone -- run through the real script in a tmp_path, asserted to
  reproduce the committed bytes. This is the strongest single claim available
  about a script that refuses to re-run: the script, and only the script,
  produced the current bytes.
* **Resulting-dataset invariants** asserted directly, so a later edit that
  reintroduces the mislabel fails here rather than in a notebook.

Each safety guard carries a MUTATION: line naming the change it catches.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "migrate_hyc0016_m5.py"
DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import migrate_hyc0016_m5 as m5  # noqa: E402
import migrate_relabel as mr  # noqa: E402


def read_dataset(path: Path = DATASET) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[0], rows[1:]


def rows_by_id(path: Path = DATASET) -> dict[str, dict[str, str]]:
    header, rows = read_dataset(path)
    index = header.index("measurement_id")
    return {row[index]: dict(zip(header, row)) for row in rows}


def run_script(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def build_pre_image(destination: Path) -> Path:
    """Write the dataset with this migration's changes undone.

    Reverses M5's four identity fields and notes prefix, and swaps the corrected
    verified_by sentence back to the old flag on every HYC-0016 row. Running the
    script against the result must reproduce the committed file byte for byte.
    """
    header, rows = read_dataset()
    idx = {name: header.index(name) for name in header}
    out = [list(row) for row in rows]

    for row in out:
        mid = row[idx["measurement_id"]]
        if mid == m5.M5:
            for column, (before, after) in m5.IDENTITY_FIELDS.items():
                assert row[idx[column]] == after, (column, row[idx[column]])
                row[idx[column]] = before
            assert row[idx["notes"]].startswith(m5.M5_NOTES_PREFIX), mid
            row[idx["notes"]] = row[idx["notes"]][len(m5.M5_NOTES_PREFIX):]
        text = row[idx["verified_by"]]
        if m5.VERIFIED_BY_NEW in text:
            row[idx["verified_by"]] = text.replace(
                m5.VERIFIED_BY_NEW, m5.VERIFIED_BY_OLD
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    m5.write_rows(destination, header, out, "\n", True)
    return destination


@pytest.fixture
def pre_image(tmp_path: Path) -> Path:
    workdir = tmp_path / "repo"
    target = workdir / "data" / "raw" / "measurements_v0.1.csv"
    build_pre_image(target)
    return target


# --- The round trip ---------------------------------------------------------


def test_running_the_migration_on_its_pre_image_reproduces_the_committed_file(
    pre_image: Path,
) -> None:
    """MUTATION: change any value in IDENTITY_FIELDS, M5_NOTES_PREFIX or
    VERIFIED_BY_NEW -> the output diverges from the committed file."""
    result = run_script(
        "--dataset", str(pre_image), "--backup-dir", str(pre_image.parent),
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_image.read_bytes() == DATASET.read_bytes()


def test_the_pre_image_is_actually_different_from_the_committed_file(
    pre_image: Path,
) -> None:
    """Guards the round trip against passing trivially."""
    assert pre_image.read_bytes() != DATASET.read_bytes()


def test_the_migration_refuses_to_run_twice(pre_image: Path) -> None:
    """MUTATION: drop the identity-value precondition -> a second run doubles the
    notes prefix and this passes."""
    first = run_script(
        "--dataset", str(pre_image), "--backup-dir", str(pre_image.parent),
        cwd=pre_image.parents[2],
    )
    assert first.returncode == 0, first.stdout + first.stderr
    before = pre_image.read_bytes()
    second = run_script(
        "--dataset", str(pre_image), "--backup-dir", str(pre_image.parent),
        cwd=pre_image.parents[2],
    )
    assert second.returncode == 1
    assert "already been applied" in second.stderr
    assert pre_image.read_bytes() == before, "a refused run must write nothing"


def test_dry_run_writes_nothing(pre_image: Path) -> None:
    before = pre_image.read_bytes()
    result = run_script(
        "--dataset", str(pre_image), "--dry-run", cwd=pre_image.parents[2]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_image.read_bytes() == before


# --- The resulting dataset invariants ---------------------------------------


def test_m5_is_now_the_reference_activated_carbon() -> None:
    """MUTATION: revert any identity field on M5 -> this fails."""
    m5row = rows_by_id()["HYC-0016-M5"]
    assert m5row["material_class"] == "activated_carbon"
    assert m5row["synthesis_method"] == "other"
    assert m5row["activation_method"] == "none"
    assert m5row["material_description"] == (
        "Reference activated carbon sample, BET 1830 m2/g"
    )


def test_m5_matches_its_77k_twin_m11_on_sample_identity() -> None:
    """M5 and M11 are the same physical sample at two temperatures.

    MUTATION: give M5 a different class/synthesis/activation than M11 -> fails.
    """
    rows = rows_by_id()
    m5row, m11 = rows["HYC-0016-M5"], rows["HYC-0016-M11"]
    for field in ("material_class", "synthesis_method", "activation_method",
                  "material_description"):
        assert m5row[field] == m11[field], field


def test_m5_measurement_fields_were_not_touched() -> None:
    """The fix is identity-only; the 293 K measurement itself is unchanged.

    MUTATION: let the migration overwrite temperature_k or uptake_wt_pct -> fails.
    """
    m5row = rows_by_id()["HYC-0016-M5"]
    assert m5row["temperature_k"] == "293"
    assert float(m5row["uptake_wt_pct"]) == 0.627
    assert m5row["source_location"] == "Figure 3"
    # distinct from M11's 77 K measurement
    assert m5row["temperature_k"] != rows_by_id()["HYC-0016-M11"]["temperature_k"]


def test_the_old_m5_signature_exists_on_no_row() -> None:
    """A reduced_graphene_oxide / BET 1830 / 293 K row was the mislabel.

    MUTATION: skip the material_class change -> this fails.
    """
    rows = rows_by_id()
    offending = [
        mid for mid, r in rows.items()
        if r["material_class"] == "reduced_graphene_oxide"
        and r["bet_surface_area_m2_g"] == "1830"
        and r["temperature_k"] == "293"
    ]
    assert offending == []


def test_m5_is_not_in_the_relabel_migration_scope() -> None:
    """migrate_relabel must no longer claim M5 as a KOH-rGO relabel.

    MUTATION: re-add "M5" to migrate_relabel._CHEMICAL_ACTIVATION -> fails here
    (and the migrate_relabel round trip also breaks).
    """
    assert "HYC-0016-M5" not in mr.SYNTHESIS_RELABEL


def test_every_hyc0016_row_carries_the_corrected_verification_record() -> None:
    """The paper-level verified_by record is uniform and no longer stale.

    MUTATION: scope the verified_by swap to M5/M11 only -> the other 12 rows keep
    the old flag and this fails.
    """
    rows = rows_by_id()
    hyc0016 = [mid for mid, r in rows.items() if r["paper_id"] == "HYC-0016"]
    assert len(hyc0016) == 14
    for mid in hyc0016:
        vb = rows[mid]["verified_by"]
        assert "left uncorrected to avoid rewriting that migration" not in vb, mid
        assert "subsequently corrected M5 to activated_carbon/other/none" in vb, mid


def test_m5_notes_explain_the_correction_and_keep_their_provenance() -> None:
    """MUTATION: drop the notes prepend -> the activated_carbon row has no
    explanation for a reader, and this fails."""
    notes = rows_by_id()["HYC-0016-M5"]["notes"]
    assert "Paper's internal reference sample of activated carbon" in notes
    assert "same physical sample as the 77 K reference-carbon row HYC-0016-M11" in notes
    assert "data/digitizations/HYC-0016_fig3.json" in notes  # original provenance kept
