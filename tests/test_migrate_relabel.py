"""Tests for scripts/migrate_relabel.py and the invariants it establishes.

Each test that guards a safety property carries a MUTATION: line naming the
change it would catch, per the convention in test_schema_v1_2.py. §6.7 makes a
passing suite weak evidence, so every guard here was confirmed to fail against
the mutation it names.

Two kinds of test live here:

* Tests that build a **pre-image** fixture -- the dataset with the migration's
  cell changes undone -- run the real script against it in a tmp_path and assert
  its post-conditions. They are the only way to test a script that refuses to
  re-run without reverting the corpus.
* Tests that assert the **resulting** dataset invariants directly, so that a
  later append or hand edit that breaks one fails here rather than in a notebook.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "migrate_relabel.py"
DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import migrate_relabel as mr  # noqa: E402

# The pre-migration values, kept here and nowhere else, so the fixture can
# reconstruct the pre-image without the script's own map deciding what the
# pre-image was.
PRE_MIGRATION_SYNTHESIS = {
    "HYC-0016": "other",
    "HYC-0019": "carbonization",
    "HYC-0020": "carbonization",
    "HYC-0021": "carbonization",
    "HYC-0022": "other",
}


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


def corpus_row_count() -> int:
    """The live row count, so these tests survive the next append.

    `migrate_relabel.py`'s `--expected-rows` default is 225, the count it actually
    ran against, and that is a historical record worth keeping. But these tests
    build their fixture from the CURRENT dataset, so passing the default would
    make every one of them fail the moment a row was appended -- which is exactly
    what happened when HYC-0011-M5 and HYC-0015-M3 took the corpus to 227. §6.7:
    a pinned total is a test that expires.
    """
    return len(read_dataset()[1])


def build_pre_image(destination: Path) -> Path:
    """Write the dataset with this migration's changes undone.

    Reverses every cell the migration sets, so running the script against the
    result must reproduce the committed file byte for byte. That round trip is
    the strongest single assertion available about the migration: it proves the
    script is the only thing that produced the current bytes.
    """
    header, rows = read_dataset()
    idx = {name: header.index(name) for name in header}
    out = [list(row) for row in rows]

    for row in out:
        mid = row[idx["measurement_id"]]
        paper = row[idx["paper_id"]]

        if mid in mr.SYNTHESIS_RELABEL:
            row[idx["synthesis_method"]] = PRE_MIGRATION_SYNTHESIS[paper]
        if mid in mr.PD_ROWS:
            row[idx["metal_element"]] = ""
            row[idx["metal_loading_wt_pct"]] = ""
        if mid in mr.PD_N_HEG_ROWS:
            row[idx["dopant_concentration_method"]] = ""
        if mid == mr.NITROGEN_REMOVAL_ROW:
            row[idx["dopant_concentration_at_pct"]] = "7"

        # Notes, reversed: every replacement swapped back, every append stripped.
        text = row[idx["notes"]]
        for kind, key, operation, args, _expected in mr.NOTES_EDITS:
            if kind == "paper" and key != paper:
                continue
            if kind == "row" and key != mid:
                continue
            if operation == "replace":
                old, new = args
                text = text.replace(new, old)
            else:
                (suffix,) = args
                assert text.endswith(suffix), mid
                text = text[: -len(suffix)]
        row[idx["notes"]] = text

    destination.parent.mkdir(parents=True, exist_ok=True)
    mr.write_rows(destination, header, out, "\n", True)
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
    """The script, and only the script, produced the bytes now committed.

    MUTATION: change any value in SYNTHESIS_RELABEL, METAL_LOADING_WT_PCT or any
    NOTES_EDITS replacement text -> the output diverges from the committed file.
    """
    result = run_script(
        "--dataset", str(pre_image), "--expected-rows", str(corpus_row_count()),
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_image.read_bytes() == DATASET.read_bytes()


def test_the_pre_image_is_actually_different_from_the_committed_file(
    pre_image: Path,
) -> None:
    """Guards the round trip against passing trivially.

    MUTATION: make build_pre_image a no-op -> the round trip above still passes
    while proving nothing. This fails.
    """
    assert pre_image.read_bytes() != DATASET.read_bytes()


def test_the_migration_refuses_to_run_twice(pre_image: Path) -> None:
    """MUTATION: drop the `already` precondition -> the second run appends every
    notes suffix a second time and this passes."""
    first = run_script(
        "--dataset", str(pre_image), "--expected-rows", str(corpus_row_count()),
        cwd=pre_image.parents[2],
    )
    assert first.returncode == 0, first.stdout + first.stderr
    before = pre_image.read_bytes()
    second = run_script(
        "--dataset", str(pre_image), "--expected-rows", str(corpus_row_count()),
        cwd=pre_image.parents[2],
    )
    assert second.returncode == 1
    assert "already been applied" in second.stderr
    assert pre_image.read_bytes() == before, "a refused run must write nothing"


def test_dry_run_writes_nothing(pre_image: Path) -> None:
    """MUTATION: move the write above the --dry-run return -> this fails."""
    before = pre_image.read_bytes()
    result = run_script(
        "--dataset", str(pre_image), "--dry-run",
        "--expected-rows", str(corpus_row_count()), cwd=pre_image.parents[2]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert pre_image.read_bytes() == before


def test_the_migration_refuses_a_dataset_whose_row_count_it_does_not_expect(
    pre_image: Path,
) -> None:
    """MUTATION: drop the --expected-rows guard -> a truncated corpus migrates
    silently."""
    result = run_script(
        "--dataset",
        str(pre_image),
        "--expected-rows",
        "999",
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 1
    assert "expected 999 data rows" in result.stderr


def test_the_migration_refuses_a_changed_cell_count_it_does_not_expect(
    pre_image: Path,
) -> None:
    """MUTATION: drop the changed-cell guard -> a relabel map that grew by one
    paper applies without anyone noticing."""
    result = run_script(
        "--dataset",
        str(pre_image),
        "--expected-rows",
        str(corpus_row_count()),
        "--expected-changed-cells",
        "71",
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 1
    assert "expected 71 changed cells" in result.stderr


def test_an_embedded_newline_is_caught_before_the_byte_check_runs(
    pre_image: Path,
) -> None:
    """A cell containing a newline makes physical line n stop holding data row
    n-1, which silently invalidates assert_untouched_lines_are_byte_identical.

    MUTATION: delete assert_line_mapping_is_sound -> the migration runs and its
    byte-level guarantee is unsound without saying so.
    """
    header, rows = read_dataset(pre_image)
    idx = header.index("notes")
    rows[0][idx] = rows[0][idx] + "\nsecond physical line"
    mr.write_rows(pre_image, header, rows, "\n", True)
    result = run_script(
        "--dataset", str(pre_image), "--expected-rows", str(corpus_row_count()),
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 1
    assert "embedded newline" in result.stderr


def test_a_notes_sentence_that_no_longer_matches_aborts_the_migration(
    pre_image: Path,
) -> None:
    """The plan quotes each replaced sentence verbatim. If the cell has changed
    since, the plan is stale and must be updated before the script runs.

    MUTATION: replace the `found != 1` check with a bare str.replace -> the
    relabel applies while the row's prose keeps asserting the old vocabulary.
    """
    header, rows = read_dataset(pre_image)
    pid, notes = header.index("paper_id"), header.index("notes")
    old = mr.NOTES_EDITS[0][3][0]
    for row in rows:
        if row[pid] == "HYC-0019":
            row[notes] = row[notes].replace(old, "paraphrased away")
    mr.write_rows(pre_image, header, rows, "\n", True)
    result = run_script(
        "--dataset", str(pre_image), "--expected-rows", str(corpus_row_count()),
        cwd=pre_image.parents[2],
    )
    assert result.returncode == 1
    assert "occurs 0 time(s) in notes" in result.stderr


def test_the_two_excluded_papers_cannot_be_relabelled_by_accident() -> None:
    """Plan §8. HYC-0001 and HYC-0004 carry activation language and must not
    change; asserting it means widening the scope requires deleting a check.

    MUTATION: add "HYC-0004" to _CHEMICAL_ACTIVATION -> check_preconditions
    raises, and this test names why.
    """
    for paper in mr.MUST_NOT_CHANGE:
        assert not [
            mid for mid in mr.SYNTHESIS_RELABEL if mid.startswith(f"{paper}-")
        ], f"{paper} is in the relabel map and plan §8 says it must not be"


# --- The scope, as the plan states it ---------------------------------------


def test_the_relabel_map_is_thirty_six_rows_across_five_papers() -> None:
    """MUTATION: drop a paper from _CHEMICAL_ACTIVATION -> the count changes."""
    assert len(mr.SYNTHESIS_RELABEL) == 36
    papers = {mid.rsplit("-", 1)[0] for mid in mr.SYNTHESIS_RELABEL}
    assert papers == {
        "HYC-0016",
        "HYC-0019",
        "HYC-0020",
        "HYC-0021",
        "HYC-0022",
    }
    by_value: dict[str, int] = {}
    for value in mr.SYNTHESIS_RELABEL.values():
        by_value[value] = by_value.get(value, 0) + 1
    assert by_value == {"chemical_activation": 34, "physical_activation": 2}


def test_the_deltas_balance_against_the_row_count() -> None:
    """36 rows leave two values and arrive at two others; the arithmetic that
    §6.7 says this project gets wrong in prose is checked here instead.

    MUTATION: change any delta in EXPECTED_SYNTHESIS_DELTAS -> this fails.
    """
    out = -sum(d for d in mr.EXPECTED_SYNTHESIS_DELTAS.values() if d < 0)
    into = sum(d for d in mr.EXPECTED_SYNTHESIS_DELTAS.values() if d > 0)
    assert out == into == len(mr.SYNTHESIS_RELABEL) == 36


# --- The resulting dataset invariants ---------------------------------------


def test_every_relabelled_row_corroborates_its_value_in_activation_method(
    ) -> None:
    """Plan §1's second line of evidence, asserted rather than asserted-in-prose.

    `activation_method` was extracted independently of `synthesis_method` and no
    part of this migration touches it, so it is a genuine second source. Every
    chemically activated row must name a chemical agent; the two physically
    activated rows must name a gas.

    MUTATION: relabel a row whose activation_method says `none` -> this fails.
    """
    rows = rows_by_id()
    for mid, value in mr.SYNTHESIS_RELABEL.items():
        activation = rows[mid]["activation_method"].lower()
        if value == "chemical_activation":
            assert "koh" in activation, (mid, activation)
        else:
            assert "co2" in activation, (mid, activation)


def test_physical_activation_is_no_longer_an_untested_vocabulary_value() -> None:
    """The v1.2 addition had zero rows until this migration.

    MUTATION: drop HYC-0022's CO2 rows from the map -> back to zero.
    """
    rows = rows_by_id()
    physical = {
        mid for mid, row in rows.items()
        if row["synthesis_method"] == "physical_activation"
    }
    assert physical == {"HYC-0022-M2", "HYC-0022-M3"}


def test_carbonization_now_means_carbonization_only() -> None:
    """Plan §5. Two rows keep the value and both are genuinely pyrolysis-only.

    This is the migration's control: a blanket relabel of everything carrying an
    activation would have emptied the value, and a blanket relabel of everything
    labelled `carbonization` would have taken these two with it.

    MUTATION: add HYC-0021-M1/M2 to the relabel map -> this fails.
    """
    rows = rows_by_id()
    carbonization = {
        mid for mid, row in rows.items()
        if row["synthesis_method"] == "carbonization"
    }
    assert carbonization == {"HYC-0021-M1", "HYC-0021-M2"}
    for mid in carbonization:
        assert rows[mid]["activation_method"] == "none"
        assert "Non-activated" in rows[mid]["notes"]


def test_no_row_asserts_the_pre_v1_2_vocabulary_in_its_notes() -> None:
    """Plan §10. A row whose prose contradicts its own controlled field is worse
    than one with no prose at all.

    MUTATION: skip the HYC-0019 or HYC-0022 notes edits -> this fails.
    """
    stale = [
        mid for mid, row in rows_by_id().items()
        if "the vocabulary has neither physical_activation" in row["notes"]
        or "the vocabulary has no chemical_activation value" in row["notes"]
        or "synthesis_method stays carbonization" in row["notes"]
    ]
    assert stale == []


def test_the_notes_edits_preserved_what_the_plan_said_they_would() -> None:
    """Three facts the relabel could have destroyed and had to carry forward.

    MUTATION: drop the 823 K clause from _HYC0019_NEW_A, or the dispute history
    from _HYC0022_NEW -> this fails.
    """
    rows = rows_by_id()
    # HYC-0019's carbonization step survived losing the field that named it.
    for mid in (f"HYC-0019-M{n}" for n in range(1, 13)):
        notes = rows[mid]["notes"]
        assert "823 K" in notes
        assert "chemical_oxidation is a graphite-oxide-route" in notes
    # HYC-0022's dispute history survived.
    for mid in (f"HYC-0022-M{n}" for n in range(1, 10)):
        assert "DISPUTE, RESOLVED IN THE VERIFIER'S FAVOUR" in rows[mid]["notes"]
    # The CO2 caveat travels with exactly the two physical_activation rows.
    caveat = [
        mid for mid, row in rows.items()
        if "CO2 ACTIVATION REDUCED THE POROSITY" in row["notes"]
    ]
    assert sorted(caveat) == ["HYC-0022-M2", "HYC-0022-M3"]


def test_hyc0027_carries_its_palladium(
    ) -> None:
    """Gap 7 was added for this paper and the data never populated it.

    MUTATION: drop a row from PD_ROWS -> this fails.
    """
    rows = rows_by_id()
    for mid in mr.PD_ROWS:
        assert rows[mid]["metal_element"] == "Pd"
        assert float(rows[mid]["metal_loading_wt_pct"]) == 20.0
    assert rows["HYC-0027-M1"]["metal_element"] == ""


def test_the_metal_loading_field_finally_has_analysis_eligible_rows() -> None:
    """The condition the plan's §0 states as the reason for the backfill.

    Before it, all 12 rows carrying a metal loading were HYC-0029's, every one
    excluded by §12.3 as `temperature_cycle`, so the field had zero rows any
    analysis could see.

    MUTATION: drop the HYC-0027 backfill -> zero eligible rows and this fails.
    """
    header, raw = read_dataset()
    idx = {name: header.index(name) for name in header}
    eligible = {
        row[idx["measurement_id"]]
        for row in raw
        if row[idx["metal_loading_wt_pct"]].strip()
        and mr.survives_analysis_filters(row, idx)
    }
    assert eligible == set(mr.PD_ROWS)


def test_the_nitrogen_content_is_gone_from_n_heg_and_only_from_n_heg() -> None:
    """Plan §9.3. The paper states a nitrogen content once, for Pd-N-HEG.

    MUTATION: apply the removal to M4/M5 as well -> this fails, and so does the
    claim that the paper's own sentence places the value there.
    """
    rows = rows_by_id()
    assert rows["HYC-0027-M3"]["dopant_concentration_at_pct"] == ""
    assert rows["HYC-0027-M3"]["dopant_element"] == "N", (
        "the element is stated even though the concentration is not"
    )
    for mid in mr.PD_N_HEG_ROWS:
        assert float(rows[mid]["dopant_concentration_at_pct"]) == 7.0
        assert rows[mid]["dopant_concentration_method"] == "XPS"
    # HYC-0025's five rows are outside this migration entirely.
    hyc0025 = [
        mid for mid, row in rows.items()
        if mid.startswith("HYC-0025-")
        and row["dopant_concentration_at_pct"].strip()
    ]
    assert len(hyc0025) == 5


def test_the_removed_value_is_not_still_asserted_in_prose() -> None:
    """A removal whose row still says "7 at% by XPS" has removed nothing.

    MUTATION: skip the HYC-0027-M3 notes replacement -> this fails.
    """
    notes = rows_by_id()["HYC-0027-M3"]["notes"]
    assert "NO NITROGEN CONTENT IS REPORTED FOR THIS SAMPLE" in notes
    assert "Nitrogen content approximately 7 at% by XPS." not in notes


def test_the_metal_loading_basis_is_recorded_because_no_field_holds_it() -> None:
    """There is no `metal_loading_method` field, so `notes` is the only place the
    basis of 20 wt% can live -- and the XPS 21 wt% must be marked as NOT the
    stored value or a reader will assume the higher figure was used.

    MUTATION: drop the _HYC0027_M4M5_APPEND text -> this fails.
    """
    rows = rows_by_id()
    for mid in mr.PD_N_HEG_ROWS:
        assert "The XPS 21 wt% is NOT what the field holds" in rows[mid]["notes"]
    assert "nominal as-added loading" in rows["HYC-0027-M2"]["notes"]
