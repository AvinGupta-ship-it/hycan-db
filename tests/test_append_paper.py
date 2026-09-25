"""Unit tests for scripts/append_paper.py (manual v2.0 §18 Phase A.3).

This is the only Phase A script that writes to the dataset, so the tests are
weighted toward the refusals rather than the happy path. Every test that
performs an append asserts on bytes read back from disk, never on what the
script printed about itself (§3.8).

The rollback test matters most: a failed post-append verification must leave
measurements_v0.1.csv byte-identical to what it was before the append.
"""

from __future__ import annotations

import hashlib
import json
import os

import append_paper as ap
import pandas as pd
import pytest
from conftest import COLUMNS, make_row, write_csv


def sha(path) -> str:
    return hashlib.sha256(bytes(path.read_bytes())).hexdigest()


def run(argv, capsys):
    code = ap.main(["append_paper.py"] + [str(a) for a in argv])
    return code, capsys.readouterr().out


@pytest.fixture
def dataset(tmp_path):
    """A clean two-row dataset with zero errors and zero warnings."""
    rows = [make_row(measurement_id=f"HYC-9001-M{n}", pressure_bar=float(n))
            for n in (1, 2)]
    return write_csv(tmp_path / "measurements_test.csv", rows)


@pytest.fixture
def staging(tmp_path):
    """Two new rows for a different paper, clean."""
    rows = [
        make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                 measurement_id=f"HYC-9002-M{n}", pressure_bar=float(n),
                 doi="10.1016/j.carbon.2016.04.002")
        for n in (1, 2)
    ]
    return write_csv(tmp_path / "staging_HYC-9002.csv", rows)


@pytest.fixture
def baseline(tmp_path, dataset, capsys):
    path = tmp_path / "baseline.json"
    ap.main(["append_paper.py", "--dataset", str(dataset),
             "--write-baseline", str(path)])
    capsys.readouterr()
    return path


# ---------------------------------------------------------------------------
# Disk primitives (§3.8)
# ---------------------------------------------------------------------------

def test_physical_lines_ignores_a_trailing_blank_line(tmp_path):
    path = tmp_path / "trailing.csv"
    path.write_text("a,b\n1,2\n\n", encoding="utf-8")
    assert ap.physical_lines(str(path)) == 2


def test_physical_lines_ignores_several_trailing_blank_lines(tmp_path):
    path = tmp_path / "trailing.csv"
    path.write_text("a,b\n1,2\n\n\n\n", encoding="utf-8")
    assert ap.physical_lines(str(path)) == 2


def test_physical_lines_counts_a_file_with_no_trailing_newline(tmp_path):
    path = tmp_path / "bare.csv"
    path.write_text("a,b\n1,2", encoding="utf-8")
    assert ap.physical_lines(str(path)) == 2


def test_physical_lines_counts_an_embedded_newline_as_an_extra_line(tmp_path):
    path = write_csv(tmp_path / "embedded.csv", [make_row(notes="one\ntwo")])
    assert ap.physical_lines(str(path)) == 3  # header + 2 physical lines for 1 row


def test_describe_file_refuses_a_row_containing_a_newline(tmp_path):
    """The defect this check exists to catch, at the size that used to slip through."""
    path = write_csv(tmp_path / "embedded.csv", [make_row(notes="one\ntwo")])
    with pytest.raises(ap.CheckFailed, match="significant lines"):
        ap.describe_file(str(path), "staging file")


def test_describe_file_accepts_a_trailing_blank_line(tmp_path, dataset):
    with open(dataset, "a", encoding="utf-8") as handle:
        handle.write("\n")
    info = ap.describe_file(str(dataset), "dataset")
    assert info["rows"] == 2


def test_describe_file_reports_a_hash_that_matches_the_bytes(dataset):
    assert ap.describe_file(str(dataset), "dataset")["sha256"] == sha(dataset)


def test_describe_file_refuses_a_path_that_does_not_exist(tmp_path):
    with pytest.raises(ap.CheckFailed, match="does not exist"):
        ap.describe_file(str(tmp_path / "absent.csv"), "staging file")


# ---------------------------------------------------------------------------
# Baseline (§11.5)
# ---------------------------------------------------------------------------

def test_write_baseline_records_rows_errors_warnings_and_hash(
    tmp_path, dataset, capsys
):
    out_path = tmp_path / "baseline.json"
    code, out = run(["--dataset", dataset, "--write-baseline", out_path], capsys)

    assert code == 0
    stored = json.loads(out_path.read_text())
    assert stored["rows"] == 2
    assert stored["error_counts"] == {}
    assert stored["warning_counts"] == {}
    assert stored["sha256"] == sha(dataset)
    assert "Baseline written" in out


def test_baseline_of_a_dataset_with_warnings_stores_the_types(tmp_path, capsys):
    rows = [make_row(measurement_id="HYC-9001-M1", uptake_type="unspecified")]
    ds = write_csv(tmp_path / "warned.csv", rows)
    out_path = tmp_path / "baseline.json"
    run(["--dataset", ds, "--write-baseline", out_path], capsys)

    assert json.loads(out_path.read_text())["warning_counts"] == {
        "Unspecified uptake_type": 1
    }


def test_a_missing_baseline_is_refused_with_the_command_to_make_one(
    tmp_path, dataset, staging, capsys
):
    code, out = run([staging, "--dataset", dataset,
                     "--baseline", tmp_path / "absent.json"], capsys)
    assert code == 1
    assert "baseline not found" in out
    assert "--write-baseline" in out


def test_a_baseline_missing_a_required_key_is_refused(
    tmp_path, dataset, staging, capsys
):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"rows": 2}), encoding="utf-8")
    code, out = run([staging, "--dataset", dataset, "--baseline", bad], capsys)
    assert code == 1
    assert "missing 'warning_counts'" in out or "missing 'error_counts'" in out


def test_running_without_a_baseline_states_the_weakening_out_loud(
    dataset, staging, tmp_path, capsys
):
    code, out = run([staging, "--dataset", dataset,
                     "--backup-dir", tmp_path / "bak", "--dry-run"], capsys)
    assert code == 0
    assert "NO STORED BASELINE" in out
    assert "cannot catch a warning type introduced earlier" in out


# ---------------------------------------------------------------------------
# Preflight refusals — nothing is written while these run
# ---------------------------------------------------------------------------

def test_reordered_staging_columns_are_refused(tmp_path, dataset, baseline, capsys):
    swapped = list(COLUMNS)
    swapped[36], swapped[37] = swapped[37], swapped[36]
    bad = write_csv(tmp_path / "swapped.csv",
                    [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1")],
                    columns=swapped)

    before = sha(dataset)
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)

    assert code == 1
    assert "do not match the dataset" in out
    assert "different order" in out
    assert "position 37" in out
    assert sha(dataset) == before


def test_an_extra_staging_column_is_refused(tmp_path, dataset, baseline, capsys):
    row = make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1")
    row["invented"] = "x"
    bad = write_csv(tmp_path / "extra.csv", [row], columns=COLUMNS + ["invented"])

    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "in staging only" in out and "invented" in out


def test_a_missing_staging_column_is_refused(tmp_path, dataset, baseline, capsys):
    columns = [c for c in COLUMNS if c != "notes"]
    row = make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1")
    row.pop("notes")
    bad = write_csv(tmp_path / "short.csv", [row], columns=columns)

    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "in dataset only" in out and "notes" in out


def test_a_measurement_id_repeated_within_staging_is_refused(
    tmp_path, dataset, baseline, capsys
):
    rows = [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1"),
            make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1",
                     pressure_bar=2.0)]
    bad = write_csv(tmp_path / "dupe.csv", rows)

    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "repeated within staging" in out
    assert "HYC-9002-M1" in out


def test_a_measurement_id_already_in_the_dataset_is_refused(
    tmp_path, dataset, baseline, capsys
):
    bad = write_csv(tmp_path / "collide.csv",
                    [make_row(measurement_id="HYC-9001-M2")])

    before = sha(dataset)
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)

    assert code == 1
    assert "already present in the dataset" in out
    assert "HYC-9001-M2" in out
    assert sha(dataset) == before


def test_a_blank_measurement_id_is_refused_with_its_line_number(
    tmp_path, dataset, baseline, capsys
):
    bad = write_csv(tmp_path / "blank.csv",
                    [make_row(paper_id="HYC-9002", measurement_id=None)])

    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "missing measurement_id at csv lines [2]" in out


def test_staging_with_a_validation_error_is_refused(
    tmp_path, dataset, baseline, capsys
):
    bad = write_csv(tmp_path / "invalid.csv",
                    [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1",
                              temperature_k=None)])

    before = sha(dataset)
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)

    assert code == 1
    assert "validation errors" in out
    assert "Missing required field" in out
    assert "validate_row_detail.py" in out  # points at the A.1 tool
    assert sha(dataset) == before


def test_an_empty_staging_file_is_refused(tmp_path, dataset, baseline, capsys):
    empty = tmp_path / "empty.csv"
    empty.write_text(",".join(COLUMNS) + "\n", encoding="utf-8")

    code, out = run([empty, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "no data rows" in out


def test_a_dataset_that_already_has_errors_is_refused(tmp_path, staging, capsys):
    broken = write_csv(tmp_path / "broken.csv",
                       [make_row(measurement_id="HYC-9001-M1", temperature_k=None)])
    code, out = run([staging, "--dataset", broken], capsys)
    assert code == 1
    assert "already has 1 errors before this append" in out


def test_no_arguments_at_all_exits_2(capsys):
    code, out = run([], capsys)
    assert code == 2
    assert "--write-baseline" in out


# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------

def test_dry_run_changes_nothing_on_disk(dataset, staging, baseline, tmp_path, capsys):
    dataset_before, staging_before = sha(dataset), sha(staging)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak", "--dry-run"], capsys)

    assert code == 0
    assert "Dry run passed" in out
    assert sha(dataset) == dataset_before
    assert sha(staging) == staging_before
    assert staging.exists()
    assert not (tmp_path / "bak").exists()


def test_dry_run_reports_the_row_arithmetic(dataset, staging, baseline, capsys):
    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--dry-run"], capsys)
    assert code == 0
    assert "2 + 2 = 4 rows" in out


def test_dry_run_still_refuses_a_bad_staging_file(
    tmp_path, dataset, baseline, capsys
):
    bad = write_csv(tmp_path / "collide.csv",
                    [make_row(measurement_id="HYC-9001-M1")])
    code, _ = run([bad, "--dataset", dataset, "--baseline", baseline,
                   "--dry-run"], capsys)
    assert code == 1


# ---------------------------------------------------------------------------
# The append
# ---------------------------------------------------------------------------

def test_a_successful_append_lands_on_disk(
    dataset, staging, baseline, tmp_path, capsys
):
    before_rows = len(pd.read_csv(dataset))

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    merged = pd.read_csv(dataset)
    assert len(merged) == before_rows + 2
    assert list(merged.columns) == COLUMNS
    assert set(merged["measurement_id"]) == {
        "HYC-9001-M1", "HYC-9001-M2", "HYC-9002-M1", "HYC-9002-M2"
    }
    assert "rows after:     4" in out


def test_the_appended_values_survive_the_round_trip(
    dataset, staging, baseline, tmp_path, capsys
):
    run([staging, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", tmp_path / "bak"], capsys)

    merged = pd.read_csv(dataset)
    row = merged[merged["measurement_id"] == "HYC-9002-M2"].iloc[0]
    assert row["paper_id"] == "HYC-9002"
    assert row["pressure_bar"] == 2.0
    assert row["notes"] == "Value as printed, no conversion applied"  # comma intact
    assert row["uptake_type"] == "excess"


def test_the_backup_matches_the_pre_append_dataset(
    dataset, staging, baseline, tmp_path, capsys
):
    before = sha(dataset)
    backup_dir = tmp_path / "bak"

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", backup_dir], capsys)

    assert code == 0
    backups = list(backup_dir.iterdir())
    assert len(backups) == 1
    assert hashlib.sha256(backups[0].read_bytes()).hexdigest() == before
    assert "verified" in out


def test_the_staging_file_is_removed(dataset, staging, baseline, tmp_path, capsys):
    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)
    assert code == 0
    assert not staging.exists()
    assert "Staging removed" in out


def test_keep_staging_leaves_it_in_place(dataset, staging, baseline, tmp_path, capsys):
    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak", "--keep-staging"], capsys)
    assert code == 0
    assert staging.exists()
    assert "Staging kept" in out


def test_the_seam_gets_exactly_one_newline_when_the_dataset_lacks_a_trailing_one(
    tmp_path, staging, capsys
):
    text = write_csv(tmp_path / "bare.csv",
                     [make_row(measurement_id="HYC-9001-M1")]).read_text()
    bare = tmp_path / "bare.csv"
    bare.write_text(text.rstrip("\n"), encoding="utf-8")

    code, _ = run([staging, "--dataset", bare, "--backup-dir", tmp_path / "bak"],
                  capsys)

    assert code == 0
    assert "\n\n" not in bare.read_text()
    assert len(pd.read_csv(bare)) == 3


def test_an_increased_count_of_an_existing_warning_type_is_allowed(
    tmp_path, capsys
):
    """§11.5: a higher count of a known warning type is expected and fine."""
    ds = write_csv(tmp_path / "warned.csv",
                   [make_row(measurement_id="HYC-9001-M1",
                             uptake_type="unspecified")])
    base = tmp_path / "baseline.json"
    run(["--dataset", ds, "--write-baseline", base], capsys)

    stage = write_csv(tmp_path / "more.csv",
                      [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1",
                                uptake_type="unspecified")])

    code, out = run([stage, "--dataset", ds, "--baseline", base,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    assert "Unspecified uptake_type: 1 -> 2" in out
    assert len(pd.read_csv(ds)) == 2


# ---------------------------------------------------------------------------
# The rollback — the test that matters most
# ---------------------------------------------------------------------------

def test_a_new_warning_type_is_refused_and_rolled_back(
    dataset, baseline, tmp_path, capsys
):
    """§11.5 makes a new warning type a stop condition, after the bytes are written."""
    stage = write_csv(tmp_path / "novel.csv",
                      [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1",
                                uptake_type="unspecified")])
    before = sha(dataset)

    code, out = run([stage, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "new warning type" in out
    assert "Unspecified uptake_type" in out
    assert "rolled back" in out and "restored and verified" in out
    assert sha(dataset) == before               # byte-identical
    assert len(pd.read_csv(dataset)) == 2       # and re-parses to the old shape
    assert stage.exists()                       # staging kept for investigation


def test_rollback_leaves_the_backup_in_place_for_inspection(
    dataset, baseline, tmp_path, capsys
):
    stage = write_csv(tmp_path / "novel.csv",
                      [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1",
                                uptake_type="unspecified")])
    backup_dir = tmp_path / "bak"
    before = sha(dataset)

    run([stage, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", backup_dir], capsys)

    backups = list(backup_dir.iterdir())
    assert len(backups) == 1
    assert hashlib.sha256(backups[0].read_bytes()).hexdigest() == before


def test_a_row_count_mismatch_after_the_append_is_caught(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """If the append writes the wrong number of rows, verification must notice."""
    real_append = ap.append_body

    def sabotage(target, body):
        real_append(target, body + body)  # writes twice as many rows

    monkeypatch.setattr(ap, "append_body", sabotage)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    # Pin the specific message. "errors" as an alternative would always match,
    # because preflight prints "0 errors" on every run that gets this far.
    assert "merged row count is 6, expected 2 + 2 = 4" in out
    assert sha(dataset) == before
    assert len(pd.read_csv(dataset)) == 2


def test_a_column_list_that_changes_during_the_append_is_caught(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    real_describe = ap.describe_file

    def sabotage(path, label):
        info = real_describe(path, label)
        if label == "merged dataset":
            info["columns"] = info["columns"][:-1]
        return info

    monkeypatch.setattr(ap, "describe_file", sabotage)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "merged column list changed during the append" in out
    assert sha(dataset) == before


def test_appended_rows_absent_from_the_merged_file_are_caught(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """The append must be checked by identity, not only by row count."""
    real_append = ap.append_body

    def sabotage(target, body):
        # right number of rows, wrong rows: ids the staging file never held
        real_append(target, body.replace("HYC-9002-M", "HYC-9003-M"))

    monkeypatch.setattr(ap, "append_body", sabotage)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "appended rows not found in the merged file" in out
    assert "HYC-9002-M1" in out
    assert sha(dataset) == before


def test_an_error_introduced_by_the_append_is_caught_and_rolled_back(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """verify_merged's error branch: right row count, right ids, bad value."""
    real_append = ap.append_body

    def sabotage(target, body):
        real_append(target, body.replace(",77.0,", ",9999.0,"))

    monkeypatch.setattr(ap, "append_body", sabotage)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "merged dataset has" in out and "errors" in out
    assert "rolled back" in out
    assert sha(dataset) == before
    assert len(pd.read_csv(dataset)) == 2


def test_a_doi_metadata_conflict_created_by_the_merge_is_a_new_warning_type(
    dataset, baseline, tmp_path, capsys
):
    """§11.5 again, through a warning that exists only once the files are merged.

    Neither file carries the warning alone: it appears because the staging row
    reuses the dataset's DOI under a different first_author.
    """
    stage = write_csv(tmp_path / "conflict.csv",
                      [make_row(paper_id="HYC-9001", sample_id="HYC-9001-S9",
                                measurement_id="HYC-9001-M9",
                                first_author="Nakamura")])
    before = sha(dataset)

    code, out = run([stage, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "new warning type" in out
    assert "DOI metadata conflict" in out
    assert "rolled back" in out
    assert sha(dataset) == before


# ---------------------------------------------------------------------------
# staging_body
# ---------------------------------------------------------------------------

def test_staging_body_drops_the_header_and_keeps_every_data_line(staging):
    body = ap.staging_body(str(staging))
    assert "paper_id" not in body.splitlines()[0]
    assert len(body.strip().splitlines()) == 2
    assert body.endswith("\n")


def test_staging_body_refuses_a_header_only_file(tmp_path):
    path = tmp_path / "header.csv"
    path.write_text(",".join(COLUMNS) + "\n", encoding="utf-8")
    with pytest.raises(ap.CheckFailed, match="no data rows"):
        ap.staging_body(str(path))


def test_staging_body_refuses_a_file_with_no_newline_after_the_header(tmp_path):
    path = tmp_path / "oneline.csv"
    path.write_text(",".join(COLUMNS), encoding="utf-8")
    with pytest.raises(ap.CheckFailed, match="no newline after its header"):
        ap.staging_body(str(path))


# ---------------------------------------------------------------------------
# Rollback under a non-CheckFailed exception, and rollback that itself fails
#
# These paths had no coverage at all. An isolated audit demonstrated that a
# pandas ParserError raised inside verify_merged escaped both handlers and left
# the dataset appended-but-unverified, which is the worst state available.
# ---------------------------------------------------------------------------

def test_a_non_checkfailed_exception_during_verification_still_rolls_back(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    def explode(target, context):
        raise ValueError("something pandas-shaped went wrong")

    monkeypatch.setattr(ap, "verify_merged", explode)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "ValueError: something pandas-shaped went wrong" in out
    assert "restored and verified byte-identical" in out
    assert sha(dataset) == before
    assert len(pd.read_csv(dataset)) == 2


def test_a_malformed_merged_file_is_a_refusal_not_a_traceback(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """The auditor's trigger: a merged file pandas cannot tokenize."""
    real_append = ap.append_body

    def sabotage(target, body):
        real_append(target, body + "a,b,c\n")   # 3 fields against 40 columns

    monkeypatch.setattr(ap, "append_body", sabotage)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "REFUSED" in out
    assert "rolled back" in out
    assert sha(dataset) == before
    assert len(pd.read_csv(dataset)) == 2       # still parses


def test_a_failed_rollback_says_so_and_names_the_backup(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """The last line of defence. It must never claim a verification it did not do."""
    def explode(target, context):
        raise ap.CheckFailed("verification failed on purpose")

    monkeypatch.setattr(ap, "verify_merged", explode)

    real_copy = ap.shutil.copy2
    calls = {"n": 0}

    def half_restore(src, dst):
        calls["n"] += 1
        if calls["n"] == 1:
            return real_copy(src, dst)          # the backup itself
        with open(dst, "w", encoding="utf-8") as handle:
            handle.write("truncated\n")         # a restore that does not restore
        return dst

    monkeypatch.setattr(ap.shutil, "copy2", half_restore)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "ROLLBACK VERIFICATION FAILED" in out
    assert "Restore it by hand" in out
    assert "restored and verified byte-identical" not in out
    assert str(tmp_path / "bak") in out         # names where the good copy is


def test_a_rollback_that_raises_is_reported_rather_than_crashing(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    def explode(target, context):
        raise ap.CheckFailed("verification failed on purpose")

    monkeypatch.setattr(ap, "verify_merged", explode)

    real_copy = ap.shutil.copy2
    calls = {"n": 0}

    def fail_second(src, dst):
        calls["n"] += 1
        if calls["n"] == 1:
            return real_copy(src, dst)
        raise OSError("disk went away")

    monkeypatch.setattr(ap.shutil, "copy2", fail_second)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "ROLLBACK ITSELF FAILED" in out
    assert "disk went away" in out
    assert "Restore it by hand" in out


def test_a_backup_that_does_not_match_aborts_before_any_append(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """The backup hash check, tested through the check rather than through print()."""
    real_sha = ap.sha256

    def lie_about_the_backup(path):
        return "0" * 64 if ".bak" in str(path) else real_sha(path)

    monkeypatch.setattr(ap, "sha256", lie_about_the_backup)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "does not match the dataset; aborting" in out
    assert "Append" not in out                  # never reached the append
    assert sha(dataset) == before


# ---------------------------------------------------------------------------
# Baseline integrity (§11.5)
# ---------------------------------------------------------------------------

def test_a_baseline_from_another_dataset_is_refused(
    dataset, staging, tmp_path, capsys
):
    """Without this the §11.5 stop condition is bypassable by pointing elsewhere."""
    other = write_csv(tmp_path / "other.csv",
                      [make_row(measurement_id="HYC-8000-M1",
                                uptake_type="unspecified")])
    foreign = tmp_path / "foreign.json"
    run(["--dataset", other, "--write-baseline", foreign], capsys)

    before = sha(dataset)
    code, out = run([staging, "--dataset", dataset, "--baseline", foreign,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "was taken from" in out
    assert "other.csv" in out
    assert sha(dataset) == before


def test_a_baseline_with_no_recorded_dataset_is_refused(
    dataset, staging, tmp_path, capsys
):
    anonymous = tmp_path / "anon.json"
    anonymous.write_text(json.dumps(
        {"rows": 2, "error_counts": {}, "warning_counts": {}}), encoding="utf-8")

    code, out = run([staging, "--dataset", dataset, "--baseline", anonymous,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "does not record which dataset" in out


def test_a_warning_type_appearing_before_the_append_is_refused(
    dataset, staging, baseline, tmp_path, capsys
):
    """§11.5 session integrity: the dataset drifted after the baseline was taken."""
    dirty = pd.read_csv(dataset)
    dirty.loc[len(dirty)] = make_row(measurement_id="HYC-9001-M9",
                                     uptake_type="unspecified")
    dirty.to_csv(dataset, index=False)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "already carries warning type(s) absent from the baseline" in out
    assert "Unspecified uptake_type" in out
    assert "Something changed earlier in this session" in out


def test_a_dataset_that_lost_rows_since_the_baseline_is_refused(
    dataset, staging, baseline, tmp_path, capsys
):
    shrunk = pd.read_csv(dataset).iloc[:1]
    shrunk.to_csv(dataset, index=False)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "are not the rows this baseline was taken from" in out


def test_a_dataset_edited_in_place_since_the_baseline_is_refused(
    dataset, staging, baseline, tmp_path, capsys
):
    """Same row count, different content: only a content check catches this."""
    edited = pd.read_csv(dataset)
    edited.loc[0, "uptake_wt_pct"] = 9.9
    edited.to_csv(dataset, index=False)

    before = sha(dataset)
    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "are not the rows this baseline was taken from" in out
    assert sha(dataset) == before


def test_a_dataset_swapped_for_a_decoy_at_the_same_path_is_refused(
    tmp_path, capsys
):
    """The path is the same, so a path-only check binds nothing.

    An audit produced this with file moves alone, no JSON editing: take the
    baseline while a decoy occupies the path, put the real dataset back, and a
    staging row carrying a brand-new warning type appends with the run
    reporting "new warn types: none".
    """
    real = write_csv(tmp_path / "ds.csv",
                     [make_row(measurement_id="HYC-9001-M1")])
    decoy = write_csv(tmp_path / "decoy.csv",
                      [make_row(measurement_id="HYC-9001-M1",
                                pressure_bar=250.0)])

    parked = tmp_path / "parked.csv"
    real.rename(parked)
    decoy.rename(tmp_path / "ds.csv")

    base = tmp_path / "b.json"
    run(["--dataset", tmp_path / "ds.csv", "--write-baseline", base], capsys)
    assert "Pressure above 200 bar" in json.loads(base.read_text())["warning_counts"]

    (tmp_path / "ds.csv").rename(tmp_path / "decoy.csv")
    parked.rename(tmp_path / "ds.csv")

    stage = write_csv(tmp_path / "s.csv",
                      [make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                                measurement_id="HYC-9002-M1",
                                doi="10.1016/j.carbon.2016.04.002",
                                pressure_bar=250.0)])
    before = sha(tmp_path / "ds.csv")

    code, out = run([stage, "--dataset", tmp_path / "ds.csv",
                     "--baseline", base, "--backup-dir", tmp_path / "bak"],
                    capsys)

    assert code == 1
    assert "are not the rows this baseline was taken from" in out
    assert sha(tmp_path / "ds.csv") == before


def test_a_baseline_without_a_content_fingerprint_is_refused(
    dataset, staging, tmp_path, capsys
):
    stale = tmp_path / "old.json"
    stale.write_text(json.dumps({
        "rows": 2, "error_counts": {}, "warning_counts": {},
        "dataset": str(dataset.resolve()),
    }), encoding="utf-8")

    code, out = run([staging, "--dataset", dataset, "--baseline", stale], capsys)
    assert code == 1
    assert "predates content binding" in out


def test_a_hardlink_alias_to_the_same_file_is_accepted(
    dataset, staging, baseline, tmp_path, capsys
):
    """Binding is to the file, not to the spelling of its path."""
    alias = tmp_path / "alias.csv"
    os.link(dataset, alias)

    code, out = run([staging, "--dataset", alias, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0, out
    assert len(pd.read_csv(alias)) == 4


def test_the_baseline_sha_messages_distinguish_matched_from_drifted(
    dataset, staging, baseline, tmp_path, capsys
):
    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak", "--dry-run"], capsys)
    assert code == 0
    assert "matches the baseline exactly" in out

    # append for real, then a second append sees a drifted dataset
    second = write_csv(tmp_path / "s2.csv",
                       [make_row(paper_id="HYC-9003", sample_id="HYC-9003-S1",
                                 measurement_id="HYC-9003-M1",
                                 doi="10.1016/j.carbon.2017.01.003")])
    run([staging, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", tmp_path / "bak"], capsys)
    code, out = run([second, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    assert "has changed since the baseline was taken: 2 -> 4 rows (+2" in out


def test_write_baseline_refuses_a_dataset_that_has_errors(tmp_path, capsys):
    broken = write_csv(tmp_path / "broken.csv",
                       [make_row(measurement_id="HYC-9001-M1",
                                 temperature_k=None)])
    out_path = tmp_path / "baseline.json"

    code, out = run(["--dataset", broken, "--write-baseline", out_path], capsys)

    assert code == 1
    assert "REFUSED" in out
    assert "cannot tell which errors it caused" in out


def test_write_baseline_reads_the_file_back_before_reporting_it(
    tmp_path, dataset, capsys
):
    """§3.8 applies to the artifact the whole session is anchored to."""
    out_path = tmp_path / "baseline.json"
    code, out = run(["--dataset", dataset, "--write-baseline", out_path], capsys)

    assert code == 0
    assert "written and read back" in out
    assert json.loads(out_path.read_text())["dataset"] == str(dataset.resolve())


def test_a_baseline_that_is_not_json_is_refused(dataset, staging, tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("this is not json", encoding="utf-8")
    code, out = run([staging, "--dataset", dataset, "--baseline", bad], capsys)
    assert code == 1
    assert "not valid JSON" in out


# ---------------------------------------------------------------------------
# Malformed inputs
# ---------------------------------------------------------------------------

def test_a_staging_row_with_more_fields_than_the_header_is_refused(
    dataset, baseline, tmp_path, capsys
):
    """Pandas' default index absorption turns this into a clean-looking frame.

    The refusal must come from the explicit field-count check, naming the
    width mismatch, rather than from a downstream check tripping by accident
    on columns that silently shifted.
    """
    # Take the dataset's own header and first data line verbatim, so quoting
    # is already correct, and prepend one extra field.
    header, first = dataset.read_text().split("\n")[:2]
    bad = tmp_path / "wide.csv"
    bad.write_text(header + "\n" + "EXTRA," + first + "\n", encoding="utf-8")

    before = sha(dataset)
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "rows of differing width" in out
    assert "40 field(s) on line(s) [1]" in out
    assert "41 field(s) on line(s) [2]" in out
    assert sha(dataset) == before
    assert "Traceback" not in out


def test_a_staging_row_with_fewer_fields_than_the_header_is_refused(
    dataset, baseline, tmp_path, capsys
):
    header = ",".join(COLUMNS)
    bad = tmp_path / "narrow.csv"
    bad.write_text(header + "\n" + ",".join(["x"] * 39) + "\n", encoding="utf-8")

    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "rows of differing width" in out


def test_a_quoted_comma_is_not_counted_as_a_field_boundary(
    dataset, staging, baseline, tmp_path, capsys
):
    """The field-count check must use a CSV parser, not a comma split."""
    rows = [make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                     measurement_id="HYC-9002-M1",
                     doi="10.1016/j.carbon.2016.04.002",
                     notes="a, b, c, d, e, f, g",
                     source_location="Table 2, row 3, column 4")]
    path = write_csv(tmp_path / "commas.csv", rows)

    assert ap.field_counts(str(path)) == {40: [1, 2]}

    code, out = run([path, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)
    assert code == 0, out
    merged = pd.read_csv(dataset)
    row = merged[merged["measurement_id"] == "HYC-9002-M1"].iloc[0]
    assert row["notes"] == "a, b, c, d, e, f, g"
    assert row["source_location"] == "Table 2, row 3, column 4"


def test_a_zero_byte_csv_is_a_refusal_not_a_traceback(
    dataset, baseline, tmp_path, capsys
):
    empty = tmp_path / "empty.csv"
    empty.write_bytes(b"")
    code, out = run([empty, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "empty or has no header row" in out


def test_a_staging_file_with_a_trailing_blank_line_does_not_pollute_the_dataset(
    dataset, staging, baseline, tmp_path, capsys
):
    """A blank line inside the dataset is invisible to every validator here."""
    with open(staging, "a", encoding="utf-8") as handle:
        handle.write("\n")

    code, _ = run([staging, "--dataset", dataset, "--baseline", baseline,
                   "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    text = dataset.read_text()
    assert "\n\n" not in text
    assert ap.physical_lines(str(dataset)) == len(pd.read_csv(dataset)) + 1


def test_a_second_append_still_works_after_one_with_a_trailing_blank_line(
    dataset, staging, baseline, tmp_path, capsys
):
    """The regression: one blank line used to block every later append."""
    with open(staging, "a", encoding="utf-8") as handle:
        handle.write("\n")
    run([staging, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", tmp_path / "bak"], capsys)

    second = write_csv(tmp_path / "s2.csv",
                       [make_row(paper_id="HYC-9003", sample_id="HYC-9003-S1",
                                 measurement_id="HYC-9003-M1",
                                 doi="10.1016/j.carbon.2017.01.003")])
    code, out = run([second, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0, out
    assert len(pd.read_csv(dataset)) == 5


def test_a_blank_line_between_staging_rows_is_refused(
    dataset, baseline, tmp_path, capsys
):
    """Caught by the line-count check in preflight, before anything is written."""
    rows = [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1"),
            make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M2")]
    path = write_csv(tmp_path / "gap.csv", rows)
    lines = path.read_text().split("\n")
    path.write_text("\n".join(lines[:2] + [""] + lines[2:]), encoding="utf-8")

    before = sha(dataset)
    code, out = run([path, "--dataset", dataset, "--baseline", baseline], capsys)

    assert code == 1
    assert "4 significant lines but 2 parsed rows" in out
    assert "a blank line between data rows" in out
    assert sha(dataset) == before


def test_staging_body_refuses_a_blank_line_between_rows_directly(tmp_path):
    """staging_body is the second line of defence if preflight is ever bypassed."""
    rows = [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1"),
            make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M2")]
    path = write_csv(tmp_path / "gap.csv", rows)
    lines = path.read_text().split("\n")
    path.write_text("\n".join(lines[:2] + [""] + lines[2:]), encoding="utf-8")

    with pytest.raises(ap.CheckFailed, match="blank line"):
        ap.staging_body(str(path))


def test_staging_body_strips_trailing_blank_lines(tmp_path):
    path = write_csv(tmp_path / "trail.csv",
                     [make_row(paper_id="HYC-9002", measurement_id="HYC-9002-M1")])
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("\n\n\n")

    body = ap.staging_body(str(path))
    assert body.endswith("\n")
    assert "\n\n" not in body
    assert len(body.split("\n")) == 2   # one data line plus the final empty split


def test_a_whitespace_padded_measurement_id_still_collides(
    dataset, baseline, tmp_path, capsys
):
    bad = write_csv(tmp_path / "padded.csv",
                    [make_row(measurement_id="  HYC-9001-M2  ")])
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "already present in the dataset" in out


def test_staging_rows_with_no_paper_id_are_refused(
    dataset, baseline, tmp_path, capsys
):
    bad = write_csv(tmp_path / "nopaper.csv",
                    [make_row(paper_id=None, measurement_id="HYC-9002-M1")])
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "missing or blank paper_id" in out
    assert "Append" not in out


def test_a_whitespace_only_paper_id_is_refused(dataset, baseline, tmp_path, capsys):
    """It satisfies the schema's 'required text' rule and is still unusable."""
    bad = write_csv(tmp_path / "blankpaper.csv",
                    [make_row(paper_id="   ", measurement_id="HYC-9002-M1")])
    code, out = run([bad, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "missing or blank paper_id" in out
    assert "Append" not in out


def test_crlf_line_endings_round_trip(dataset, baseline, tmp_path, capsys):
    rows = [make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                     measurement_id="HYC-9002-M1",
                     doi="10.1016/j.carbon.2016.04.002")]
    path = write_csv(tmp_path / "crlf.csv", rows)
    path.write_bytes(path.read_text().replace("\n", "\r\n").encode("utf-8"))

    code, out = run([path, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0, out
    merged = pd.read_csv(dataset)
    assert len(merged) == 3
    assert "HYC-9002-M1" in set(merged["measurement_id"])


# ---------------------------------------------------------------------------
# Time-of-check / time-of-use, and reporting honesty
# ---------------------------------------------------------------------------

def test_a_staging_file_rewritten_after_validation_is_refused(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """The bytes appended must be the bytes that were validated."""
    real_body = ap.staging_body

    def rewrite_first(path):
        with open(path, "a", encoding="utf-8") as handle:
            handle.write("sneaky\n")
        return real_body(path)

    # simulate an external writer between preflight and the body read
    real_preflight = ap.preflight

    def preflight_then_tamper(staging_path, dataset_path, baseline_path):
        context = real_preflight(staging_path, dataset_path, baseline_path)
        with open(staging_path, "a", encoding="utf-8") as handle:
            handle.write(",".join(["x"] * 40) + "\n")
        return context

    monkeypatch.setattr(ap, "preflight", preflight_then_tamper)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "changed on disk between validation and append" in out
    assert sha(dataset) == before


def test_the_verify_line_reports_measured_numbers_not_a_fixed_string(
    tmp_path, capsys
):
    """The summary line must be derived, or it can contradict the table below it."""
    ds = write_csv(tmp_path / "warned.csv",
                   [make_row(measurement_id="HYC-9001-M1",
                             uptake_type="unspecified")])
    base = tmp_path / "b.json"
    run(["--dataset", ds, "--write-baseline", base], capsys)

    stage = write_csv(tmp_path / "s.csv",
                      [make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                                measurement_id="HYC-9002-M1",
                                doi="10.1016/j.carbon.2016.04.002",
                                uptake_type="unspecified")])
    code, out = run([stage, "--dataset", ds, "--baseline", base,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    assert "2 rows, 0 errors, 0 new warning types" in out
    assert "<-- NEW TYPE" not in out
    assert "new warn types: none" in out


def test_the_new_type_marker_renders_when_a_type_is_new():
    lines = ap.warning_delta({"Known": 3}, {"Known": 4, "Novel": 1})
    assert "    Known: 3 -> 4" in lines
    assert "    Novel: 0 -> 1   <-- NEW TYPE" in lines


def test_the_summary_survives_a_staging_file_that_cannot_be_removed(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """A good append must never be reported as a refusal."""
    def refuse(path):
        raise OSError("Permission denied")

    monkeypatch.setattr(ap.os, "remove", refuse)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    assert "SUMMARY (for the §17 execution log)" in out
    assert "rows after:     4" in out
    assert "could not be removed" in out
    assert "Do not re-run this command" in out
    assert len(pd.read_csv(dataset)) == 4


def test_the_dry_run_rehashes_the_dataset_rather_than_restating_it(
    dataset, staging, baseline, tmp_path, capsys
):
    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--dry-run"], capsys)
    assert code == 0
    assert "unchanged on disk, re-hashed" in out


def test_two_appends_in_the_same_second_do_not_share_a_backup_name(
    dataset, staging, baseline, tmp_path, capsys
):
    backup_dir = tmp_path / "bak"
    run([staging, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", backup_dir], capsys)

    second = write_csv(tmp_path / "s2.csv",
                       [make_row(paper_id="HYC-9003", sample_id="HYC-9003-S1",
                                 measurement_id="HYC-9003-M1",
                                 doi="10.1016/j.carbon.2017.01.003")])
    run([second, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", backup_dir], capsys)

    backups = sorted(backup_dir.iterdir())
    assert len(backups) == 2
    assert len({b.read_bytes() for b in backups}) == 2   # distinct contents


def test_the_staging_removal_check_actually_runs(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    monkeypatch.setattr(ap.os, "remove", lambda path: None)   # pretends to delete

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 0
    assert "still present after removal" in out
    assert "Staging removed" not in out


# ---------------------------------------------------------------------------
# Exit codes
# ---------------------------------------------------------------------------

def test_a_missing_staging_path_exits_2(dataset, tmp_path, capsys):
    code, out = run([tmp_path / "absent.csv", "--dataset", dataset], capsys)
    assert code == 2
    assert "staging file not found" in out


def test_a_missing_dataset_path_exits_2(staging, tmp_path, capsys):
    code, out = run([staging, "--dataset", tmp_path / "absent.csv"], capsys)
    assert code == 2
    assert "dataset not found" in out


def test_write_baseline_on_a_missing_dataset_exits_2(tmp_path, capsys):
    code, out = run(["--dataset", tmp_path / "absent.csv",
                     "--write-baseline", tmp_path / "b.json"], capsys)
    assert code == 2
    assert "dataset not found" in out


def test_a_partial_write_during_the_append_is_rolled_back(
    dataset, staging, baseline, tmp_path, monkeypatch, capsys
):
    """ENOSPC mid-append leaves a state matching neither before nor after.

    That is the one outcome with no safe recovery, so the write itself must be
    inside the rollback guard, not before it.
    """
    real_append = ap.append_body

    def partial(target, body):
        real_append(target, body[:len(body) // 2])   # truncated mid-row
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(ap, "append_body", partial)
    before = sha(dataset)

    code, out = run([staging, "--dataset", dataset, "--baseline", baseline,
                     "--backup-dir", tmp_path / "bak"], capsys)

    assert code == 1
    assert "No space left on device" in out
    assert "restored and verified byte-identical" in out
    assert sha(dataset) == before
    assert len(pd.read_csv(dataset)) == 2


def test_an_oversized_field_is_a_refusal_not_a_traceback(
    dataset, baseline, tmp_path, capsys
):
    """csv.reader caps a field at 128 KiB; every other tool reads such a file."""
    big = write_csv(tmp_path / "big.csv",
                    [make_row(paper_id="HYC-9002", sample_id="HYC-9002-S1",
                              measurement_id="HYC-9002-M1",
                              doi="10.1016/j.carbon.2016.04.002",
                              notes="x" * 200_000)])

    code, out = run([big, "--dataset", dataset, "--baseline", baseline], capsys)
    assert code == 1
    assert "cannot parse" in out
    assert "Traceback" not in out


def test_a_directory_passed_as_a_path_is_a_refusal_not_a_traceback(
    dataset, tmp_path, capsys
):
    code, out = run([tmp_path, "--dataset", dataset], capsys)
    assert code in (1, 2)
    assert "Traceback" not in out


def test_a_refused_baseline_is_not_left_on_disk(tmp_path, capsys):
    """A refused baseline left behind is a usable baseline."""
    broken = write_csv(tmp_path / "broken.csv",
                       [make_row(measurement_id="HYC-9001-M1",
                                 temperature_k=None)])
    out_path = tmp_path / "baseline.json"

    code, out = run(["--dataset", broken, "--write-baseline", out_path], capsys)

    assert code == 1
    assert not out_path.exists()
    assert "removed" in out


def test_the_baseline_records_a_content_fingerprint(tmp_path, dataset, capsys):
    out_path = tmp_path / "b.json"
    run(["--dataset", dataset, "--write-baseline", out_path], capsys)

    stored = json.loads(out_path.read_text())
    assert len(stored["prefix_sha256"]) == 64
    assert stored["prefix_sha256"] == ap.prefix_sha256(str(dataset), stored["rows"])


def test_the_fingerprint_covers_exactly_the_rows_the_baseline_described(
    tmp_path, dataset, staging, baseline, capsys
):
    """Appending must not invalidate the baseline; editing a described row must."""
    recorded = json.loads(baseline.read_text())["prefix_sha256"]

    run([staging, "--dataset", dataset, "--baseline", baseline,
         "--backup-dir", tmp_path / "bak"], capsys)

    assert ap.prefix_sha256(str(dataset), 2) == recorded    # appends are fine
    assert ap.prefix_sha256(str(dataset), 4) != recorded    # more rows, new hash
