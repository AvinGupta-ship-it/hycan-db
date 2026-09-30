"""Tests for scripts/migrate_pdf_obtained.py.

Manual §6.7: a migration script committed without its own test file is not
verified, and a passing test suite is weak evidence. Every test below carries a
``MUTATION:`` line naming the defect it would catch, and the eight mutations in
docs/migration_pdf_obtained_plan.md §6 were run against the finished script with
this file expected to fail on each.

Two things this file deliberately does the hard way:

**The fixture is CRLF with no trailing newline**, like the real file. A fixture
written with ``\\n`` would not exercise the property these tests exist to
protect: §6.7 records a `paper_tracking.csv` migration that rewrote the bytes of
every physical line while every parsed cell stayed correct.

**The not-retrieved note contains a comma** — ``(RSC, no institutional
access)`` — so writing it forces csv quoting on a cell that previously needed
none. That is a byte-level change to a line the migration is allowed to touch,
and the round-trip is asserted rather than assumed.
"""

from __future__ import annotations

import csv
import importlib.util
import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = _ROOT / "scripts" / "migrate_pdf_obtained.py"
PLAN = _ROOT / "docs" / "migration_pdf_obtained_plan.md"
REAL_TRACKING = _ROOT / "references" / "paper_tracking.csv"

_spec = importlib.util.spec_from_file_location("migrate_pdf_obtained", SCRIPT)
assert _spec and _spec.loader
mig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mig)

# The harness must be driving the scratch copy, never the real tree. §6.7
# records a mutation run where all 8 mutations "survived" because the imports
# resolved back to the committed file.
assert Path(mig.__file__).resolve() == SCRIPT.resolve()

HEADER = ",".join(mig.EXPECTED_HEADER)

N_EXISTING = 4  # non-Phase-D rows in the fixture
N_FIXTURE_ROWS = N_EXISTING + len(mig.PHASE_D)


def _existing_row(n: int) -> str:
    """A pre-Phase-D row. Quoted author cell, so re-quoting tests have a target."""
    return (
        f"HYC-{n:04d},Existing paper {n},\"Author, A.\",200{n % 10},Carbon,"
        f"10.1000/existing.{n},anchor:x,include,,yes,extracted,2026-01-01,note {n}"
    )


def _phase_d_row(pid: str, notes: str) -> str:
    return (
        f"{pid},Title for {pid},Some Author,2020,Journal of Testing,"
        f"10.1000/{pid.lower().replace('-', '.')},phase_d:77K_BET,include,,"
        f"no,not_started,,{notes}"
    )


def write_tracking(
    path: Path,
    *,
    terminator: str = "\r\n",
    trailing: bool = False,
    blank_notes: tuple[str, ...] = ("HYC-0035",),
) -> None:
    """The fixture: 4 existing rows then all 35 Phase D rows, all `no`.

    ``blank_notes`` leaves those ids' notes empty so both append branches are
    exercised — bare note vs `; ` appended to an existing one. The real file has
    a note on all 35, so only the second branch fires in production; the first
    is still reachable code and is tested.
    """
    lines = [HEADER]
    lines += [_existing_row(i) for i in range(1, N_EXISTING + 1)]
    lines += [
        _phase_d_row(pid, "" if pid in blank_notes else f"screened for {pid}")
        for pid in mig.PHASE_D
    ]
    body = terminator.join(lines) + (terminator if trailing else "")
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(body)


@pytest.fixture()
def bench(tmp_path: Path):
    tracking = tmp_path / "paper_tracking.csv"
    dataset = tmp_path / "measurements.csv"
    write_tracking(tracking)
    dataset.write_text("measurement_id\nHYC-0001-M1\n", encoding="utf-8")
    return tracking, dataset


def run(tracking: Path, dataset: Path, *extra: str, rows: int = N_FIXTURE_ROWS) -> int:
    return mig.main([
        "--tracking", str(tracking),
        "--dataset", str(dataset),
        "--backup-dir", str(tracking.parent),
        "--expected-rows", str(rows),
        *extra,
    ])


def cells(path: Path) -> tuple[list[str], dict[str, list[str]]]:
    header, rows = mig.read_rows(path)
    return header, {row[0]: row for row in rows}


# --- the constants themselves ----------------------------------------------

def test_obtained_and_not_obtained_partition_the_phase_d_block():
    """The two lists must cover HYC-0031..HYC-0065 exactly once each.

    An id in neither list is silently skipped by apply_changes and silently
    skipped again by verify's counting loop, so nothing else in this file would
    notice it.

    MUTATION: drop an id from OBTAINED, or list one in both -> this fails.
    """
    assert len(mig.OBTAINED) == 30
    assert len(mig.NOT_OBTAINED) == 5
    assert set(mig.OBTAINED).isdisjoint(mig.NOT_OBTAINED)
    assert set(mig.PHASE_D) == set(mig.OBTAINED) | set(mig.NOT_OBTAINED)
    assert list(mig.PHASE_D) == [f"HYC-{n:04d}" for n in range(31, 66)]


def test_not_obtained_matches_the_ids_tabulated_in_the_plan():
    """Code and plan must name the same five papers.

    The plan's §3 explains *why* these five matter — all RSC, three of them the
    `volumetric` target — and that rationale is only true of this exact set. If
    the code's list drifts from the table, the committed justification quietly
    stops describing what the code did.

    MUTATION: swap an id between OBTAINED and NOT_OBTAINED -> this fails.
    """
    section = PLAN.read_text(encoding="utf-8").split("## 3.")[1].split("\n## ")[0]
    tabulated = re.findall(r"\|\s*(HYC-\d{4})\s*\|", section)
    assert sorted(tabulated) == sorted(mig.NOT_OBTAINED)


# --- format detection -------------------------------------------------------

def test_detects_crlf_without_trailing_newline(bench):
    """MUTATION: hardcode '\\n' as the terminator -> this fails."""
    tracking, _ = bench
    assert mig.detect_format(tracking) == ("\r\n", False)


def test_detects_lf_with_trailing_newline(tmp_path: Path):
    """MUTATION: ignore the trailing-newline state -> this fails."""
    p = tmp_path / "t.csv"
    write_tracking(p, terminator="\n", trailing=True)
    assert mig.detect_format(p) == ("\n", True)


# --- the byte-identity guarantee -------------------------------------------

def test_lines_outside_the_phase_d_block_are_byte_identical(bench):
    """The core guarantee, checked as bytes on the real output.

    MUTATION: write with csv.writer defaults (LF), or add a trailing newline the
    original lacked -> this fails while a cell-level check passes.
    """
    tracking, dataset = bench
    before = mig.read_physical_lines(tracking, "\r\n")
    assert run(tracking, dataset) == 0
    after = mig.read_physical_lines(tracking, "\r\n")
    # header plus the 4 pre-Phase-D rows
    assert after[: N_EXISTING + 1] == before[: N_EXISTING + 1]


def test_terminator_and_final_newline_are_preserved(bench):
    """MUTATION: drop newline='' on the write -> Python translates, this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    raw = tracking.read_bytes()
    assert b"\r\n" in raw
    assert not raw.endswith(b"\n")


def test_lone_lf_never_appears(bench):
    """A bare LF in a CRLF file is the exact corruption §6.7 records.

    MUTATION: join with '\\n', or write without newline='' -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    raw = tracking.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n"), "a lone LF was written"


def test_physical_line_count_is_unchanged(bench):
    """MUTATION: emit the rendered rows with a trailing terminator -> this fails."""
    tracking, dataset = bench
    before = len(mig.read_physical_lines(tracking, "\r\n"))
    assert run(tracking, dataset) == 0
    assert len(mig.read_physical_lines(tracking, "\r\n")) == before


def test_verify_rejects_a_line_that_differs_only_in_its_ending(tmp_path: Path):
    """verify() must compare raw bytes, not parsed cells.

    `a,b,c` and `a,"b",c` parse to identical cells and are different lines, so a
    cell-level check cannot see the difference. This drives verify() directly,
    because the happy path writes correct bytes and therefore cannot distinguish
    a byte check from a cell check.

    MUTATION: compare `next(csv.reader([a]))` instead of `a` in verify's drift
    loop -> this fails. (Plan §6 mutation 3.)
    """
    tracking = tmp_path / "t.csv"
    dataset = tmp_path / "d.csv"
    dataset.write_text("x\n", encoding="utf-8")
    write_tracking(tracking)

    original_lines = mig.read_physical_lines(tracking, "\r\n")
    header, before = mig.read_rows(tracking)

    # Re-quote a field on line 2 -- a row outside the Phase D block.
    scrambled = list(original_lines)
    assert ",Carbon," in scrambled[1]
    scrambled[1] = scrambled[1].replace(",Carbon,", ',"Carbon",', 1)
    assert next(csv.reader([scrambled[1]])) == next(csv.reader([original_lines[1]]))
    assert scrambled[1] != original_lines[1]

    new_rows, _ = mig.apply_changes(header, before)
    with tracking.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\r\n".join(scrambled[: N_EXISTING + 1] + mig.render(new_rows)[N_EXISTING:]))

    with pytest.raises(mig.MigrationError, match="byte-identity"):
        mig.verify(tracking, header, before, original_lines, "\r\n", False,
                   None, dataset)


def test_a_change_to_a_row_outside_the_phase_d_block_is_rejected(bench,
                                                                 monkeypatch):
    """Plan §6 mutation 6: touch a row the migration does not name.

    `pdf_obtained` is in verify's allowed-columns set, so the column check
    cannot catch this and the yes/no counts do not move -- only the byte-level
    comparison of non-Phase-D lines can. The run must fail and restore.

    MUTATION: skip non-Phase-D lines in verify's drift loop (e.g. `continue` on
    every row) -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real = mig.apply_changes

    def also_touch_an_old_row(header, rows):
        new_rows, changes = real(header, rows)
        idx = header.index("pdf_obtained")
        new_rows[0][idx] = "no"  # HYC-0001, was 'yes'
        return new_rows, changes

    monkeypatch.setattr(mig, "apply_changes", also_touch_an_old_row)
    assert run(tracking, dataset) == 1
    assert tracking.read_bytes() == before


def test_the_header_line_is_compared_too(bench, monkeypatch):
    """verify() checks the header line separately; the drift loop skips it.

    MUTATION: delete the `original_lines[0] != lines_after[0]` check -> this
    fails.
    """
    tracking, dataset = bench
    header, rows = mig.read_rows(tracking)
    original_lines = mig.read_physical_lines(tracking, "\r\n")
    new_rows, _ = mig.apply_changes(header, rows)

    mangled = list(original_lines)
    mangled[0] = mangled[0].replace("paper_id", '"paper_id"', 1)
    with tracking.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\r\n".join([mangled[0]] + mig.render(new_rows)))

    with pytest.raises(mig.MigrationError, match="header line"):
        mig.verify(tracking, header, rows, original_lines, "\r\n", False,
                   None, dataset)


# --- row-level outcome ------------------------------------------------------

def test_exactly_thirty_become_yes_and_five_stay_no(bench):
    """Plan §5 post-condition 4.

    MUTATION: mark all 35 obtained -> this fails. (Plan §6 mutation 4.)
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    header, by_id = cells(tracking)
    i = header.index("pdf_obtained")
    assert [by_id[p][i] for p in mig.OBTAINED] == ["yes"] * 30
    assert [by_id[p][i] for p in mig.NOT_OBTAINED] == ["no"] * 5


def test_marking_all_thirty_five_obtained_is_rejected(bench, monkeypatch):
    """The guard behind the test above, exercised rather than assumed.

    MUTATION: delete verify's `should still read 'no'` check -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real = mig.apply_changes

    def mark_everything(header, rows):
        new_rows, changes = real(header, rows)
        idx = header.index("pdf_obtained")
        for row in new_rows:
            if row[0] in mig.NOT_OBTAINED:
                row[idx] = "yes"
        return new_rows, changes

    monkeypatch.setattr(mig, "apply_changes", mark_everything)
    assert run(tracking, dataset) == 1
    assert tracking.read_bytes() == before


def test_the_five_gain_the_not_retrieved_note(bench):
    """MUTATION: drop the notes branch in apply_changes -> this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    header, by_id = cells(tracking)
    i = header.index("notes")
    for pid in mig.NOT_OBTAINED:
        assert mig.NOT_OBTAINED_NOTE in by_id[pid][i]


def test_an_existing_note_is_appended_to_not_replaced(bench):
    """A note already recording why the paper was screened in must survive.

    MUTATION: assign the note instead of appending -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    header, by_id = cells(tracking)
    i = header.index("notes")
    # HYC-0036 carried a note in the fixture; HYC-0035 did not.
    assert by_id["HYC-0036"][i] == f"screened for HYC-0036; {mig.NOT_OBTAINED_NOTE}"
    assert by_id["HYC-0035"][i] == mig.NOT_OBTAINED_NOTE


def test_the_note_round_trips_through_csv_quoting(bench):
    """The note contains a comma, so the cell must be quoted on write.

    Without quoting the note would split into two cells, making the row ragged
    and shifting every value after `notes` -- except `notes` is last, so the
    row would simply gain a 14th field. This asserts the parsed cell equals the
    constant exactly, and that the raw line quotes it.

    MUTATION: render with a writer that does not quote (QUOTE_NONE) -> this
    fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    _, rows = mig.read_rows(tracking)
    assert all(len(r) == mig.EXPECTED_COLUMNS for r in rows)
    header, by_id = cells(tracking)
    assert by_id["HYC-0035"][header.index("notes")] == mig.NOT_OBTAINED_NOTE
    line = [
        ln for ln in mig.read_physical_lines(tracking, "\r\n")
        if ln.startswith("HYC-0035,")
    ][0]
    assert '"' in line, "a cell containing a comma was written unquoted"


def test_no_cell_outside_pdf_obtained_and_notes_changes(bench):
    """Plan §5 post-condition 6, as an outcome check over every row.

    MUTATION: change any other column -> this fails.
    """
    tracking, dataset = bench
    header, before = cells(tracking)
    assert run(tracking, dataset) == 0
    _, after = cells(tracking)
    assert set(before) == set(after)
    for pid, old in before.items():
        new = after[pid]
        for col, name in enumerate(header):
            if name in ("pdf_obtained", "notes"):
                continue
            assert old[col] == new[col], f"{pid}.{name} changed"


def test_a_change_to_an_unnamed_column_is_rejected(bench, monkeypatch):
    """Plan §6 mutation 5, on a Phase D row so the byte check is not what fires.

    A non-Phase-D row would be caught by the drift loop instead, which would
    let the allowed-columns check be deleted with this test still passing.

    MUTATION: delete verify's allowed-columns check -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real = mig.apply_changes

    def also_change_a_year(header, rows):
        new_rows, changes = real(header, rows)
        idx = header.index("year")
        for row in new_rows:
            if row[0] == "HYC-0031":
                row[idx] = "1999"
        return new_rows, changes

    monkeypatch.setattr(mig, "apply_changes", also_change_a_year)
    assert run(tracking, dataset) == 1
    assert tracking.read_bytes() == before


def test_row_count_is_unchanged(bench):
    """MUTATION: append or drop a row -> this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    _, rows = mig.read_rows(tracking)
    assert len(rows) == N_FIXTURE_ROWS


def test_pdf_obtained_holds_only_yes_or_no(bench):
    """Plan §5 post-condition 5.

    MUTATION: write 'Yes' or 'true' -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    _, rows = mig.read_rows(tracking)
    i = mig.EXPECTED_HEADER.index("pdf_obtained")
    assert {r[i] for r in rows} <= {"yes", "no"}


def test_the_yes_no_domain_guard_fires_on_a_dirty_pre_existing_value(bench,
                                                                     capsys):
    """Plan §5 post-condition 5, tested on the one path that reaches it.

    Worth stating plainly: this guard cannot catch a mistake by *this*
    migration. A bad value on a Phase D row is caught first by the per-row
    `should read 'yes'` / `should still read 'no'` checks, and a bad value on
    any other row is caught first by the byte-identity drift loop. Both were
    tried before settling on this.

    What it does catch is a `pdf_obtained` domain that was already dirty before
    the run -- here `Yes` on a pre-Phase-D row. That line is rendered back
    byte-identically, so the drift loop passes it, and the domain check is the
    only thing that sees it.

    MUTATION: delete verify's `outside yes/no` check -> this fails.
    """
    tracking, dataset = bench
    lines = mig.read_physical_lines(tracking, "\r\n")
    assert lines[1].count(",yes,") == 1
    lines[1] = lines[1].replace(",yes,", ",Yes,", 1)
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("\r\n".join(lines))
    before = tracking.read_bytes()

    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "outside yes/no" in err, f"a different check fired first: {err}"
    assert tracking.read_bytes() == before


# --- preconditions ----------------------------------------------------------

def test_refuses_to_run_twice(bench, capsys):
    """Plan §6 mutation 1, and the only guard that can catch a re-run.

    A second run is otherwise idempotent -- it would re-render byte-identical
    output, pass every post-condition and exit 0 -- so nothing downstream would
    report it. The refusal must therefore be a precondition, which is why this
    asserts on `refusing:` and on the absence of `post-condition`.

    MUTATION: remove the refuse-to-re-run guard -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    after_first = tracking.read_bytes()
    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "already been applied" in err
    assert "post-condition" not in err, "caught too late: only verify() stopped it"
    assert tracking.read_bytes() == after_first


def test_refuses_an_embedded_newline_in_an_existing_row(bench, capsys):
    """Plan §6 mutation 8: the physical-line-count precondition.

    A newline inside a quoted cell makes physical line n stop holding data row
    n-1, which silently invalidates verify()'s byte check -- it would compare
    correctly-written lines against the wrong originals. Must be refused before
    anything is written.

    MUTATION: delete the assert_line_mapping CALL in check_preconditions ->
    this fails. verify()'s own line-count check does not save it: both files
    split into the same number of pieces, so the message differs, which is why
    this asserts on `refusing:` and the absence of `post-condition`.
    """
    tracking, dataset = bench
    lines = mig.read_physical_lines(tracking, "\r\n")
    lines[1] = lines[1].replace('"Author, A."', '"Author,\r\nA."', 1)
    with tracking.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\r\n".join(lines))
    before = tracking.read_bytes()

    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "physical lines" in err
    assert "post-condition" not in err, "caught too late: only verify() stopped it"
    assert tracking.read_bytes() == before


def test_line_mapping_precondition_in_isolation():
    """MUTATION: delete assert_line_mapping -> this fails."""
    with pytest.raises(mig.MigrationError, match="physical lines"):
        mig.assert_line_mapping(["header", "row1", "row1-continued"], 1)
    mig.assert_line_mapping(["header", "row1"], 1)


def test_refuses_an_unexpected_row_count(bench, capsys):
    """MUTATION: drop the expected-rows precondition -> this fails."""
    tracking, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, dataset, rows=999) == 1
    assert "refusing:" in capsys.readouterr().err
    assert tracking.read_bytes() == before


def test_refuses_an_unexpected_header(bench, capsys):
    """MUTATION: drop the header check -> this fails."""
    tracking, dataset = bench
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("wrong,header\r\na,b")
    assert run(tracking, dataset, rows=1) == 1
    assert "refusing:" in capsys.readouterr().err


def test_refuses_a_ragged_row(bench, capsys):
    """MUTATION: drop the ragged-row precondition -> this fails."""
    tracking, dataset = bench
    lines = mig.read_physical_lines(tracking, "\r\n")
    lines[2] = lines[2] + ",extra"
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("\r\n".join(lines))
    assert run(tracking, dataset) == 1
    assert "ragged" in capsys.readouterr().err


def test_refuses_a_missing_phase_d_id(bench, capsys):
    """Every id the migration names must exist exactly once.

    MUTATION: drop the `ids.count(pid) != 1` precondition -> the run would
    silently mark 29 rows and verify's counting loop would catch it only as a
    total, with the file already rewritten. This asserts it is refused first.
    """
    tracking, dataset = bench
    lines = [
        ln for ln in mig.read_physical_lines(tracking, "\r\n")
        if not ln.startswith("HYC-0031,")
    ]
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("\r\n".join(lines))
    before = tracking.read_bytes()
    assert run(tracking, dataset, rows=N_FIXTURE_ROWS - 1) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "expected exactly once" in err
    assert tracking.read_bytes() == before


def test_refuses_a_missing_file(tmp_path: Path, capsys):
    """MUTATION: drop the exists() check -> this raises instead of returning 1."""
    assert run(tmp_path / "nope.csv", tmp_path / "d.csv") == 1
    assert "does not exist" in capsys.readouterr().err


# --- post-conditions --------------------------------------------------------

def test_dataset_is_not_touched(bench):
    """MUTATION: none -- an outcome check, not a guard check.

    Kept because it states the intended outcome, but it cannot kill a mutation
    of the sha assertion: the script never writes the dataset, so deleting the
    check leaves this passing. The test below exercises the guard.
    """
    tracking, dataset = bench
    before = dataset.read_bytes()
    assert run(tracking, dataset) == 0
    assert dataset.read_bytes() == before


def test_dataset_sha_guard_fires_when_the_dataset_changes(bench, monkeypatch,
                                                          capsys):
    """Plan §6 mutation 7, and plan §5 post-condition 7.

    Simulates the failure the guard exists for -- something in the run touching
    data/raw/measurements_v0.1.csv -- by corrupting the dataset after the
    baseline is taken, and requires the migration to fail and restore rather
    than report success.

    MUTATION: remove the `_sha256(dataset) != dataset_sha_before` check ->
    this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real_render = mig.render

    def render_and_scribble(rows):
        dataset.write_text("measurement_id\nCORRUPTED\n", encoding="utf-8")
        return real_render(rows)

    monkeypatch.setattr(mig, "render", render_and_scribble)
    assert run(tracking, dataset) == 1
    assert "dataset changed" in capsys.readouterr().err
    assert tracking.read_bytes() == before


def test_dataset_baseline_is_taken_before_any_other_work(bench, monkeypatch):
    """The ordering defect found in migrate_phase_d_screening.py.

    There the baseline was computed late enough that a corruption occurring
    earlier in the run would have been hashed into the baseline and compared
    with itself -- a guard that reports success on exactly the failure it exists
    to catch. Corrupting the dataset during `detect_format`, the first call
    after the baseline, must still be caught.

    MUTATION: move the `dataset_sha_before = ...` line below detect_format or
    read_rows -> this fails.
    """
    tracking, dataset = bench
    real_detect = mig.detect_format

    def detect_and_scribble(path):
        dataset.write_text("measurement_id\nCORRUPTED-EARLY\n", encoding="utf-8")
        return real_detect(path)

    monkeypatch.setattr(mig, "detect_format", detect_and_scribble)
    assert run(tracking, dataset) == 1


def test_dry_run_writes_nothing(bench):
    """MUTATION: let --dry-run fall through to the write -> this fails."""
    tracking, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, dataset, "--dry-run") == 0
    assert tracking.read_bytes() == before


def test_dry_run_reports_thirty_five_changes(bench, capsys):
    """MUTATION: report the count from OBTAINED alone -> this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset, "--dry-run") == 0
    out = capsys.readouterr().out
    assert "35 cell change(s)" in out
    assert out.count("pdf_obtained 'no' -> 'yes'") == 30
    assert out.count("notes += not-retrieved record") == 5


def test_post_condition_failure_restores_the_original(bench):
    """A failed post-condition must leave the file exactly as it was.

    MUTATION: remove the restore-from-backup on failure -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()

    def boom(*a, **k):
        raise mig.MigrationError("induced")

    original_verify = mig.verify
    mig.verify = boom
    try:
        assert run(tracking, dataset) == 1
    finally:
        mig.verify = original_verify
    assert tracking.read_bytes() == before


def test_a_backup_is_written_before_the_file_is_touched(bench):
    """MUTATION: drop the backup -> restore-on-failure has nothing to restore."""
    tracking, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, dataset) == 0
    backups = list(tracking.parent.glob("paper_tracking.before_obtained.*.csv"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == before


# --- the real artifact ------------------------------------------------------

def test_real_tracking_file_records_the_collection_outcome():
    """Asserted against the committed file, not the script's own report.

    §6.7: a tool's description of its own output is not evidence. This reads
    references/paper_tracking.csv as it stands in the repo and requires the
    recorded state to match the plan. It fails before the migration is applied
    and must keep passing afterwards.
    """
    header, rows = mig.read_rows(REAL_TRACKING)
    assert header == mig.EXPECTED_HEADER
    assert len(rows) == mig.DEFAULT_EXPECTED_ROWS
    by_id = {r[0]: r for r in rows}
    pdf = header.index("pdf_obtained")
    notes = header.index("notes")

    for pid in mig.OBTAINED:
        assert by_id[pid][pdf] == "yes", f"{pid} is not recorded as obtained"
    for pid in mig.NOT_OBTAINED:
        assert by_id[pid][pdf] == "no", f"{pid} is recorded as obtained"
        assert mig.NOT_OBTAINED_NOTE in by_id[pid][notes], (
            f"{pid} is not obtained and carries no record of why; §7.5 requires "
            f"'full text not retrieved' to be visible in the source of truth"
        )
    assert {r[pdf] for r in rows} <= {"yes", "no"}


def test_real_tracking_file_keeps_its_crlf_format():
    """MUTATION: rewrite the file with LF -> this fails.

    The format is load-bearing for every future byte-level migration check.
    """
    raw = REAL_TRACKING.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n"), "a lone LF is in the file"
    assert not raw.endswith(b"\n"), "the file gained a trailing newline"
    assert len(raw.split(b"\r\n")) == mig.DEFAULT_EXPECTED_ROWS + 1
