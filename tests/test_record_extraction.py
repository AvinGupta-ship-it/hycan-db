"""Tests for scripts/record_extraction.py.

Manual §6.7: a script that writes a protected file and ships without its own
test file is not verified, and a passing test suite is weak evidence. Every test
carries a ``MUTATION:`` line naming the defect it would catch, and the twelve
mutations in docs/migration_record_extraction_plan.md §6 were run against the
finished script with this file expected to fail on each.

The fixture reproduces the real file's format deliberately: **CRLF terminated
with no trailing newline**, the combination that once let a migration rewrite
every physical line while every parsed cell stayed correct.
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = _ROOT / "scripts" / "record_extraction.py"
REAL_TRACKING = _ROOT / "references" / "paper_tracking.csv"
REAL_DATASET = _ROOT / "data" / "raw" / "measurements_v0.1.csv"

_spec = importlib.util.spec_from_file_location("record_extraction", SCRIPT)
assert _spec and _spec.loader
rec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rec)

# §6.7 records a mutation run where every mutation "survived" because the
# imports resolved back to the committed file. Prove which file is loaded.
assert Path(rec.__file__).resolve() == SCRIPT.resolve()

HEADER = ",".join(rec.EXPECTED_HEADER)
TARGET = "HYC-0031"


def _row(pid: str, *, decision="include", obtained="yes", status="not_started",
         date="", notes="a note") -> str:
    return (f'{pid},Title for {pid},"Author, A.",2017,Carbon,'
            f'10.1000/{pid.lower()},anchor:x,{decision},,{obtained},'
            f'{status},{date},{notes}')


def write_tracking(path: Path, *, terminator="\r\n", trailing=False,
                   rows=None) -> None:
    rows = rows if rows is not None else [
        _row("HYC-0001", status="extracted", date="2026-01-01"),
        _row("HYC-0002"),
        _row(TARGET),
        _row("HYC-0032"),
    ]
    body = terminator.join([HEADER] + rows) + (terminator if trailing else "")
    with path.open("w", encoding="utf-8", newline="") as h:
        h.write(body)


def write_dataset(path: Path, *, n=3, paper=TARGET) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.writer(h, lineterminator="\n")
        w.writerow(["paper_id", "measurement_id", "uptake_wt_pct"])
        for i in range(1, n + 1):
            w.writerow([paper, f"{paper}-M{i}", "1.0"])


@pytest.fixture()
def bench(tmp_path: Path):
    tracking = tmp_path / "paper_tracking.csv"
    dataset = tmp_path / "measurements.csv"
    write_tracking(tracking)
    write_dataset(dataset)
    return tracking, dataset


def run(tracking: Path, dataset: Path, *extra: str, paper=TARGET,
        status="extracted", date="2026-09-30") -> int:
    return rec.main([
        "--paper-id", paper, "--status", status, "--date", date,
        "--tracking", str(tracking), "--dataset", str(dataset),
        "--backup-dir", str(tracking.parent), *extra,
    ])


def cells(path: Path) -> tuple[list[str], dict[str, list[str]]]:
    header, rows = rec.read_rows(path)
    return header, {r[0]: r for r in rows}


# --- format -----------------------------------------------------------------

def test_detects_crlf_without_trailing_newline(bench):
    """MUTATION: hardcode '\\n' as the terminator -> this fails."""
    tracking, _ = bench
    assert rec.detect_format(tracking) == ("\r\n", False)


def test_terminator_and_final_newline_are_preserved(bench):
    """MUTATION: drop newline='' on the write -> Python translates, this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    raw = tracking.read_bytes()
    assert b"\r\n" in raw
    assert not raw.endswith(b"\n")


def test_lone_lf_never_appears(bench):
    """Plan §6 mutation 2. A bare LF in a CRLF file is §6.7's exact corruption.

    MUTATION: render with csv.writer's defaults, or join with '\\n' -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    raw = tracking.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n"), "a lone LF was written"


# --- the byte-identity guarantee -------------------------------------------

def test_every_other_line_is_byte_identical(bench):
    """MUTATION: rewrite the whole file through csv.writer -> this fails."""
    tracking, dataset = bench
    before = rec.read_physical_lines(tracking, "\r\n")
    assert run(tracking, dataset) == 0
    after = rec.read_physical_lines(tracking, "\r\n")
    assert len(after) == len(before)
    for i, (a, b) in enumerate(zip(before, after)):
        if i == 3:            # header + HYC-0001 + HYC-0002 -> target is index 3
            continue
        assert a == b, f"line {i + 1} changed and is not the target"


def test_verify_rejects_a_line_that_differs_only_in_its_ending(tmp_path: Path):
    """Plan §6 mutation 3: verify() must compare raw bytes, not parsed cells.

    `a,b,c` and `a,"b",c` parse identically and are different lines. Driven
    through verify() directly, because the happy path writes correct bytes and
    so cannot distinguish a byte check from a cell check.

    MUTATION: compare next(csv.reader([a])) instead of a -> this fails.
    """
    tracking = tmp_path / "t.csv"
    dataset = tmp_path / "d.csv"
    write_tracking(tracking)
    write_dataset(dataset)

    original_lines = rec.read_physical_lines(tracking, "\r\n")
    header, before = rec.read_rows(tracking)
    new_rows, _ = rec.apply_change(header, before, 2, "extracted", "2026-09-30", None)

    scrambled = list(original_lines)
    assert ",Carbon," in scrambled[1]
    scrambled[1] = scrambled[1].replace(",Carbon,", ',"Carbon",', 1)
    assert next(csv.reader([scrambled[1]])) == next(csv.reader([original_lines[1]]))

    rendered = rec.render(new_rows)
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("\r\n".join([scrambled[0], scrambled[1]] + rendered[1:]))

    with pytest.raises(rec.MigrationError, match="byte-identity"):
        rec.verify(tracking, header, before, original_lines, "\r\n", False,
                   2, "extracted", "2026-09-30", None, dataset)


def test_touching_another_row_is_rejected(bench, monkeypatch):
    """Plan §6 mutation 4.

    MUTATION: make verify's drift loop skip every line -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real = rec.apply_change

    def also_touch_another(header, rows, target, status, date, note):
        new_rows, changes = real(header, rows, target, status, date, note)
        new_rows[0][header.index("extraction_status")] = "verified"
        return new_rows, changes

    monkeypatch.setattr(rec, "apply_change", also_touch_another)
    assert run(tracking, dataset) == 1
    assert tracking.read_bytes() == before


def test_changing_an_unnamed_column_is_rejected(bench, monkeypatch):
    """Plan §6 mutation 5, on the TARGET row so the byte check is not what fires.

    A change on any other row is caught by the drift loop instead, which would
    let the allowed-columns check be deleted with this test still passing.

    MUTATION: delete verify's allowed-columns check -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real = rec.apply_change

    def also_change_year(header, rows, target, status, date, note):
        new_rows, changes = real(header, rows, target, status, date, note)
        new_rows[target][header.index("year")] = "1999"
        return new_rows, changes

    monkeypatch.setattr(rec, "apply_change", also_change_year)
    assert run(tracking, dataset) == 1
    assert tracking.read_bytes() == before


# --- the change itself ------------------------------------------------------

def test_sets_status_and_date(bench):
    """MUTATION: write the wrong column -> this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    header, by_id = cells(tracking)
    row = by_id[TARGET]
    assert row[header.index("extraction_status")] == "extracted"
    assert row[header.index("extraction_date")] == "2026-09-30"


def test_leaves_every_other_cell_on_the_target_row_alone(bench):
    """MUTATION: rebuild the row instead of editing it -> this fails."""
    tracking, dataset = bench
    header, before = cells(tracking)
    assert run(tracking, dataset) == 0
    _, after = cells(tracking)
    for col, name in enumerate(header):
        if name in ("extraction_status", "extraction_date", "notes"):
            continue
        assert before[TARGET][col] == after[TARGET][col], f"{name} changed"


def test_append_note_preserves_the_existing_note(bench):
    """MUTATION: assign the note instead of appending -> this fails."""
    tracking, dataset = bench
    assert run(tracking, dataset, "--append-note", "32 rows") == 0
    header, by_id = cells(tracking)
    assert by_id[TARGET][header.index("notes")] == "a note; 32 rows"


def test_extracted_may_later_become_verified(bench):
    """A status transition is the normal second call, not a re-run.

    MUTATION: make the refuse-to-re-run guard key on the id alone -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    assert run(tracking, dataset, "--verified-by", "Agent B: 10/10 agreed",
               status="verified") == 0
    header, by_id = cells(tracking)
    assert by_id[TARGET][header.index("extraction_status")] == "verified"


# --- preconditions ----------------------------------------------------------

def test_refuses_to_run_twice(bench, capsys):
    """Plan §6 mutation 1.

    A second identical run is otherwise idempotent -- it would re-render
    byte-identical output and pass every post-condition -- so only the
    precondition can catch it. Hence the assertion on `refusing:` and on the
    absence of `post-condition`.

    MUTATION: remove the refuse-to-re-run guard -> this fails.
    """
    tracking, dataset = bench
    assert run(tracking, dataset) == 0
    after_first = tracking.read_bytes()
    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "Refusing to run twice" in err
    assert "post-condition" not in err, "caught too late: only verify() stopped it"
    assert tracking.read_bytes() == after_first


def test_refuses_a_paper_excluded_at_screening(bench, capsys):
    """Plan §6 mutation 6.

    MUTATION: drop the screening_decision check -> this fails.
    """
    tracking, dataset = bench
    write_tracking(tracking, rows=[
        _row("HYC-0001"), _row("HYC-0002"),
        _row(TARGET, decision="exclude"), _row("HYC-0032")])
    before = tracking.read_bytes()
    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "screening_decision" in err
    assert tracking.read_bytes() == before


def test_refuses_a_paper_whose_pdf_was_never_obtained(bench, capsys):
    """Plan §6 mutation 7. The five Phase D papers are exactly this case.

    MUTATION: drop the pdf_obtained check -> this fails.
    """
    tracking, dataset = bench
    write_tracking(tracking, rows=[
        _row("HYC-0001"), _row("HYC-0002"),
        _row(TARGET, obtained="no"), _row("HYC-0032")])
    before = tracking.read_bytes()
    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "pdf_obtained" in err
    assert tracking.read_bytes() == before


def test_refuses_when_the_dataset_has_no_rows_for_the_paper(bench, capsys):
    """Plan §6 mutation 8 -- step 15's failure mode, inverted.

    MUTATION: drop the dataset-rows-exist check -> this fails.
    """
    tracking, dataset = bench
    write_dataset(dataset, n=2, paper="HYC-0099")
    before = tracking.read_bytes()
    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "no rows" in err
    assert tracking.read_bytes() == before


def test_verified_requires_the_dual_agent_record(bench, capsys):
    """Plan §6 mutation 9. §5.2 defines `verified` as §3.2 completed.

    MUTATION: drop the --verified-by requirement -> this fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, dataset, status="verified") == 1
    assert "--verified-by" in capsys.readouterr().err
    assert tracking.read_bytes() == before


def test_refuses_an_unknown_paper(bench, capsys):
    """MUTATION: drop the exactly-once check -> this raises or writes nothing."""
    tracking, dataset = bench
    assert run(tracking, dataset, paper="HYC-9999") == 1
    assert "expected exactly once" in capsys.readouterr().err


def test_refuses_a_status_outside_the_vocabulary(bench):
    """Plan §6 mutation 12.

    MUTATION: drop the choices= / STATUSES check -> this fails.
    """
    tracking, dataset = bench
    with pytest.raises(SystemExit):
        run(tracking, dataset, status="done")


def test_refuses_an_embedded_newline_in_an_existing_row(bench, capsys):
    """Plan §6 mutation 11: the physical-line-count precondition.

    A newline inside a quoted cell makes physical line n stop holding data row
    n-1, silently invalidating verify()'s byte check.

    MUTATION: delete the assert_line_mapping CALL -> this fails.
    """
    tracking, dataset = bench
    lines = rec.read_physical_lines(tracking, "\r\n")
    lines[1] = lines[1].replace('"Author, A."', '"Author,\r\nA."', 1)
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("\r\n".join(lines))
    before = tracking.read_bytes()
    assert run(tracking, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "physical lines" in err
    assert "post-condition" not in err, "caught too late: only verify() stopped it"
    assert tracking.read_bytes() == before


def test_line_mapping_precondition_in_isolation():
    """MUTATION: delete assert_line_mapping -> this fails."""
    with pytest.raises(rec.MigrationError, match="physical lines"):
        rec.assert_line_mapping(["header", "row1", "row1-continued"], 1)
    rec.assert_line_mapping(["header", "row1"], 1)


def test_refuses_a_ragged_row(bench, capsys):
    """MUTATION: drop the ragged-row precondition -> this fails."""
    tracking, dataset = bench
    lines = rec.read_physical_lines(tracking, "\r\n")
    lines[2] = lines[2] + ",extra"
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("\r\n".join(lines))
    assert run(tracking, dataset) == 1
    assert "ragged" in capsys.readouterr().err


def test_refuses_an_unexpected_header(bench, capsys):
    """MUTATION: drop the header check -> this fails."""
    tracking, dataset = bench
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("wrong,header\r\na,b")
    assert run(tracking, dataset) == 1
    assert "refusing:" in capsys.readouterr().err


# --- post-conditions --------------------------------------------------------

def test_dataset_is_not_touched(bench):
    """MUTATION: none -- an outcome check. The guard test is below."""
    tracking, dataset = bench
    before = dataset.read_bytes()
    assert run(tracking, dataset) == 0
    assert dataset.read_bytes() == before


def test_dataset_sha_guard_fires_when_the_dataset_changes(bench, monkeypatch,
                                                          capsys):
    """Plan §6 mutation 10.

    MUTATION: remove the _sha256(dataset) != dataset_sha_before check -> fails.
    """
    tracking, dataset = bench
    before = tracking.read_bytes()
    real = rec.render

    def render_and_scribble(rows):
        dataset.write_text("paper_id\nCORRUPTED\n", encoding="utf-8")
        return real(rows)

    monkeypatch.setattr(rec, "render", render_and_scribble)
    assert run(tracking, dataset) == 1
    assert "dataset changed" in capsys.readouterr().err
    assert tracking.read_bytes() == before


def test_dataset_baseline_is_taken_before_any_other_work(bench, monkeypatch):
    """The ordering defect found in migrate_phase_d_screening.py.

    Corrupting the dataset during detect_format -- the first call after the
    baseline -- must still be caught.

    MUTATION: move the dataset_sha_before line below detect_format -> fails.
    """
    tracking, dataset = bench
    real = rec.detect_format

    def detect_and_scribble(path):
        dataset.write_text("paper_id\nCORRUPTED-EARLY\n", encoding="utf-8")
        return real(path)

    monkeypatch.setattr(rec, "detect_format", detect_and_scribble)
    assert run(tracking, dataset) == 1


def test_dry_run_writes_nothing(bench):
    """MUTATION: let --dry-run fall through to the write -> this fails."""
    tracking, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, dataset, "--dry-run") == 0
    assert tracking.read_bytes() == before


def test_post_condition_failure_restores_the_original(bench):
    """MUTATION: remove the restore-from-backup on failure -> this fails."""
    tracking, dataset = bench
    before = tracking.read_bytes()
    original = rec.verify

    def boom(*a, **k):
        raise rec.MigrationError("induced")

    rec.verify = boom
    try:
        assert run(tracking, dataset) == 1
    finally:
        rec.verify = original
    assert tracking.read_bytes() == before


# --- the real artifacts -----------------------------------------------------

def test_real_tracking_records_every_extracted_paper_the_dataset_holds():
    """The invariant step 15 exists to maintain, asserted against the files.

    §5.2 makes the tracking file the source of truth. A paper with rows in the
    dataset and `not_started` in the tracking file is step 15 skipped -- the
    failure that went unnoticed for ten consecutive papers.

    MUTATION: append a paper to the dataset without running this script -> fails.
    """
    with REAL_DATASET.open(encoding="utf-8", newline="") as h:
        in_dataset = {r["paper_id"] for r in csv.DictReader(h)}
    header, rows = rec.read_rows(REAL_TRACKING)
    status = {r[0]: r[header.index("extraction_status")] for r in rows}
    date = {r[0]: r[header.index("extraction_date")] for r in rows}

    untracked = sorted(p for p in in_dataset if p not in status)
    assert not untracked, f"in the dataset but not in the tracking file: {untracked}"

    not_started = sorted(p for p in in_dataset if status[p] == "not_started")
    assert not not_started, (
        f"these papers have dataset rows but read 'not_started': {not_started}. "
        f"That is manual §9.1 step 15 skipped."
    )

    undated = sorted(p for p in in_dataset if not date[p].strip())
    assert not undated, f"extracted with no extraction_date: {undated}"
