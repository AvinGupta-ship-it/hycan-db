"""Tests for scripts/migrate_phase_d_screening.py.

Manual §6.7: a migration script committed without its own test file is not
verified, and a passing test suite is weak evidence. Every test below carries a
``MUTATION:`` line in its docstring naming the defect it would catch, and the
mutations listed in docs/migration_phase_d_screening_plan.md §8 were run against
the finished script with this file expected to fail on each.

The fixtures reproduce the real file's format deliberately: **CRLF terminated
with no trailing newline**. That combination is what made the earlier
`paper_tracking.csv` migration rewrite the bytes of all 31 physical lines while
every parsed cell stayed correct, so a fixture written with `\\n` would not
exercise the property these tests exist to protect.
"""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = _ROOT / "scripts" / "migrate_phase_d_screening.py"

_spec = importlib.util.spec_from_file_location("migrate_phase_d_screening", SCRIPT)
assert _spec and _spec.loader
mig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mig)


HEADER = (
    "paper_id,title,authors,year,journal,doi,search_source,screening_decision,"
    "exclusion_reason,pdf_obtained,extraction_status,extraction_date,notes"
)


def _existing_row(n: int) -> str:
    return (
        f"HYC-{n:04d},Existing paper {n},\"Author, A.\",200{n % 10},Carbon,"
        f"10.1000/existing.{n},anchor:x,include,,yes,extracted,2026-01-01,note {n}"
    )


def write_tracking(path: Path, n_rows: int = 3, *, terminator: str = "\r\n",
                   trailing: bool = False) -> None:
    lines = [HEADER] + [_existing_row(i) for i in range(1, n_rows + 1)]
    body = terminator.join(lines) + (terminator if trailing else "")
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(body)


def _entry(pid: str, doi: str, cand: str = "A1-01") -> dict:
    return {
        "paper_id": pid,
        "title": f"Title for {pid}",
        "authors": "Some Author; Other Author",
        "year": "2020",
        "journal": "Journal of Testing",
        "doi": doi,
        "oa_status": "gold",
        "funnel": "77K_BET",
        "cand_id": cand,
        "notes": "reports 77 K uptake and a BET area",
        "provenance": {"verdict": "confirmed", "source": "openalex"},
    }


def write_screening(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps({"papers": entries}), encoding="utf-8")


@pytest.fixture()
def bench(tmp_path: Path):
    tracking = tmp_path / "paper_tracking.csv"
    screening = tmp_path / "screening.json"
    dataset = tmp_path / "measurements.csv"
    write_tracking(tracking)
    write_screening(screening, [
        _entry("HYC-0031", "10.1000/new.1"),
        _entry("HYC-0032", "10.1000/new.2", "A2-07"),
    ])
    dataset.write_text("measurement_id\nHYC-0001-M1\n", encoding="utf-8")
    return tracking, screening, dataset


def run(tracking: Path, screening: Path, dataset: Path, *extra: str) -> int:
    return mig.main([
        "--tracking", str(tracking),
        "--screening", str(screening),
        "--dataset", str(dataset),
        "--backup-dir", str(tracking.parent),
        "--expected-rows", "3",
        *extra,
    ])


# --- format detection -------------------------------------------------------

def test_detects_crlf_without_trailing_newline(bench):
    """MUTATION: hardcode '\\n' as the terminator -> this fails."""
    tracking, _, _ = bench
    assert mig.detect_format(tracking) == ("\r\n", False)


def test_detects_lf_with_trailing_newline(tmp_path: Path):
    """MUTATION: ignore the trailing-newline state -> this fails."""
    p = tmp_path / "t.csv"
    write_tracking(p, terminator="\n", trailing=True)
    assert mig.detect_format(p) == ("\n", True)


# --- the byte-identity guarantee -------------------------------------------

def test_existing_lines_are_byte_identical_after_append(bench):
    """The core guarantee: raw bytes of existing lines, not parsed cells.

    MUTATION: write with csv.writer defaults (LF), or append a trailing
    newline the original lacked -> this fails while a cell-level check passes.
    """
    tracking, screening, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, screening, dataset) == 0
    after = tracking.read_bytes()
    # every original byte is still a prefix of the new file
    assert after.startswith(before), "existing bytes were rewritten"


def test_verify_rejects_a_line_that_differs_only_in_its_ending(tmp_path: Path):
    """verify() must compare raw bytes, not parsed cells.

    A line that lost its CR parses to identical cells and is a different line.
    This drives verify() directly, because the happy path writes correct bytes
    and so cannot distinguish a byte check from a cell check.

    MUTATION: compare `next(csv.reader([a]))` instead of `a` in verify's
    drift loop -> this fails.
    """
    tracking = tmp_path / "t.csv"
    dataset = tmp_path / "d.csv"
    dataset.write_text("x\n", encoding="utf-8")
    write_tracking(tracking, n_rows=2)
    original_lines = mig.read_physical_lines(tracking, "\r\n")

    # Re-quote one field on line 2. `a,b,c` and `a,"b",c` parse to identical
    # cells and are different bytes, so a cell-level check cannot see it.
    scrambled = list(original_lines)
    assert ",Carbon," in scrambled[1]
    scrambled[1] = scrambled[1].replace(",Carbon,", ',"Carbon",', 1)
    assert next(csv.reader([scrambled[1]])) == next(csv.reader([original_lines[1]]))
    assert scrambled[1] != original_lines[1]

    entry = _entry("HYC-0031", "10.1000/new.1")
    new_line = mig.render_new_lines((entry,))[0]
    with tracking.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\r\n".join(scrambled + [new_line]))

    with pytest.raises(mig.MigrationError, match="byte-identity"):
        mig.verify(
            tracking, original_lines, "\r\n", False, 2, (entry,), None, dataset,
        )


def test_terminator_and_final_newline_are_preserved(bench):
    """MUTATION: drop the newline='' on the write -> Python translates, this fails."""
    tracking, screening, dataset = bench
    assert run(tracking, screening, dataset) == 0
    raw = tracking.read_bytes()
    assert b"\r\n" in raw
    assert not raw.endswith(b"\r\n\r\n")
    assert not raw.endswith(b"\n\n")
    # unchanged final-newline state: the fixture has none
    assert not raw.endswith(b"\n")


def test_lone_lf_never_appears(bench):
    """A bare LF in a CRLF file is the exact corruption §6.7 records.

    MUTATION: join the new lines with '\\n' -> this fails.
    """
    tracking, screening, dataset = bench
    assert run(tracking, screening, dataset) == 0
    raw = tracking.read_bytes()
    assert raw.count(b"\n") == raw.count(b"\r\n"), "a lone LF was written"


# --- row-level outcome ------------------------------------------------------

def test_appends_exactly_the_new_rows(bench):
    """MUTATION: drop or duplicate an entry -> this fails."""
    tracking, screening, dataset = bench
    assert run(tracking, screening, dataset) == 0
    header, rows = mig.read_rows(tracking)
    assert len(rows) == 5
    ids = [r[0] for r in rows]
    assert ids == ["HYC-0001", "HYC-0002", "HYC-0003", "HYC-0031", "HYC-0032"]


def test_every_new_row_has_thirteen_fields(bench):
    """MUTATION: let build_row emit 12 fields -> this fails."""
    tracking, screening, dataset = bench
    assert run(tracking, screening, dataset) == 0
    _, rows = mig.read_rows(tracking)
    assert all(len(r) == mig.EXPECTED_COLUMNS for r in rows)


def test_fixed_columns_take_the_planned_values(bench):
    """Plan §4: include / no / not_started, with no exclusion reason or date.

    MUTATION: mark a new paper pdf_obtained=yes or extracted -> this fails.
    """
    tracking, screening, dataset = bench
    assert run(tracking, screening, dataset) == 0
    header, rows = mig.read_rows(tracking)
    idx = {n: header.index(n) for n in header}
    for row in rows[3:]:
        assert row[idx["screening_decision"]] == "include"
        assert row[idx["exclusion_reason"]] == ""
        assert row[idx["pdf_obtained"]] == "no"
        assert row[idx["extraction_status"]] == "not_started"
        assert row[idx["extraction_date"]] == ""
        assert row[idx["search_source"]].startswith("phase_d:")


def test_no_existing_cell_changes(bench):
    """MUTATION: touch any existing row -> this fails."""
    tracking, screening, dataset = bench
    _, before = mig.read_rows(tracking)
    assert run(tracking, screening, dataset) == 0
    _, after = mig.read_rows(tracking)
    assert after[: len(before)] == before


# --- preconditions ----------------------------------------------------------

def test_refuses_to_run_twice(bench, capsys):
    """MUTATION: remove the refuse-to-re-run guard -> this fails.

    The ids must be what triggers the refusal. Re-running the *same* screening
    file would also trip the duplicate-DOI check, so this second run reuses the
    paper_ids with fresh DOIs: only the id guard can catch it.
    """
    tracking, screening, dataset = bench
    assert run(tracking, screening, dataset) == 0
    write_screening(screening, [
        _entry("HYC-0031", "10.1000/unseen.1"),
        _entry("HYC-0032", "10.1000/unseen.2"),
    ])
    assert mig.main([
        "--tracking", str(tracking), "--screening", str(screening),
        "--dataset", str(dataset), "--backup-dir", str(tracking.parent),
        "--expected-rows", "5",
    ]) == 1
    assert "already been applied" in capsys.readouterr().err


def test_refuses_a_doi_already_tracked(bench, capsys):
    """MUTATION: drop the existing-DOI check -> this fails.

    Asserts refusal happens as a PRECONDITION, before anything is written.
    Without that assertion the post-condition duplicate-DOI check also returns
    1, and the test would pass with the precondition deleted.
    """
    tracking, screening, dataset = bench
    before = tracking.read_bytes()
    write_screening(screening, [_entry("HYC-0031", "10.1000/existing.2")])
    assert run(tracking, screening, dataset) == 1
    err = capsys.readouterr().err
    assert "refusing:" in err and "already tracked" in err
    assert "post-condition" not in err, "caught too late: only verify() stopped it"
    assert tracking.read_bytes() == before


def test_refuses_an_existing_row_with_an_embedded_newline(bench, capsys):
    """The line-mapping precondition, exercised through main().

    An embedded newline in an EXISTING quoted cell makes physical line n stop
    holding data row n-1, which silently invalidates verify()'s byte check. The
    control-character guard cannot catch this: it only inspects the new rows.

    MUTATION: delete the `assert_line_mapping(...)` CALL in check_preconditions
    -> this fails.
    """
    tracking, screening, dataset = bench
    lines = [HEADER, _existing_row(1), _existing_row(2),
             'HYC-0003,"two\r\nlines",A,2003,Carbon,10.1000/existing.3,'
             'x,include,,yes,extracted,2026-01-01,n']
    with tracking.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\r\n".join(lines))
    assert run(tracking, screening, dataset) == 1
    err = capsys.readouterr().err
    # Must be refused BEFORE writing. Without the precondition the write goes
    # ahead and verify()'s line-count check catches it after the fact, with a
    # message that also mentions "physical lines" -- so asserting on that
    # phrase alone cannot tell the two apart.
    assert "refusing:" in err and "physical lines" in err
    assert "post-condition" not in err, "caught too late: only verify() stopped it"


def test_refuses_a_duplicate_doi_within_the_new_set(bench):
    """MUTATION: drop the within-set duplicate check -> this fails."""
    tracking, screening, dataset = bench
    write_screening(screening, [
        _entry("HYC-0031", "10.1000/same"),
        _entry("HYC-0032", "10.1000/same"),
    ])
    assert run(tracking, screening, dataset) == 1


def test_refuses_an_unverified_doi(bench):
    """Manual §3.5: only a confirmed DOI may enter the source of truth.

    MUTATION: accept any provenance.verdict -> this fails.
    """
    tracking, screening, dataset = bench
    e = _entry("HYC-0031", "10.1000/new.1")
    e["provenance"]["verdict"] = "unresolved"
    write_screening(screening, [e])
    assert run(tracking, screening, dataset) == 1


def test_refuses_a_missing_required_field(bench):
    """MUTATION: drop the required-key check -> this fails."""
    tracking, screening, dataset = bench
    e = _entry("HYC-0031", "10.1000/new.1")
    e["journal"] = ""
    write_screening(screening, [e])
    assert run(tracking, screening, dataset) == 1


def test_refuses_a_nul_byte_in_a_cell(bench):
    """A NUL survives the append and then truncates the value in pandas (§6.9).

    MUTATION: drop the control-character guard -> this fails.
    """
    tracking, screening, dataset = bench
    e = _entry("HYC-0031", "10.1000/new.1")
    e["notes"] = "before\x00after"
    write_screening(screening, [e])
    assert run(tracking, screening, dataset) == 1


def test_refuses_an_embedded_newline_in_a_cell(bench):
    """An embedded newline breaks the line-to-row mapping the byte check needs.

    MUTATION: drop the control-character guard -> this fails.
    """
    tracking, screening, dataset = bench
    e = _entry("HYC-0031", "10.1000/new.1")
    e["title"] = "two\nlines"
    write_screening(screening, [e])
    assert run(tracking, screening, dataset) == 1


def test_refuses_an_unexpected_row_count(bench):
    """MUTATION: drop the expected-rows precondition -> this fails."""
    tracking, screening, dataset = bench
    assert mig.main([
        "--tracking", str(tracking), "--screening", str(screening),
        "--dataset", str(dataset), "--backup-dir", str(tracking.parent),
        "--expected-rows", "99",
    ]) == 1


def test_refuses_an_unexpected_header(bench):
    """MUTATION: drop the header check -> this fails."""
    tracking, screening, dataset = bench
    with tracking.open("w", encoding="utf-8", newline="") as h:
        h.write("wrong,header\r\na,b")
    assert run(tracking, screening, dataset) == 1


def test_line_mapping_precondition_catches_an_embedded_newline(tmp_path: Path):
    """migrate_relabel.py's precondition: physical lines == rows + 1.

    Without it the byte-level check compares the wrong lines. This is the
    precondition, tested directly, because a quoted newline in an EXISTING row
    cannot be caught by the control-character guard on the new ones.

    MUTATION: delete assert_line_mapping -> this fails.
    """
    with pytest.raises(mig.MigrationError, match="physical lines"):
        mig.assert_line_mapping(["header", "row1", "row1-continued"], 1)
    mig.assert_line_mapping(["header", "row1"], 1)


# --- post-conditions --------------------------------------------------------

def test_dataset_is_not_touched(bench):
    """MUTATION: none -- this is an outcome check, not a guard check.

    Kept because it states the intended outcome, but note that it cannot kill a
    mutation of the sha assertion: the script never writes the dataset, so
    removing the check leaves this passing. The test below is the one that
    exercises the guard.
    """
    tracking, screening, dataset = bench
    before = dataset.read_bytes()
    assert run(tracking, screening, dataset) == 0
    assert dataset.read_bytes() == before


def test_dataset_sha_guard_fires_when_the_dataset_changes(bench, monkeypatch,
                                                          capsys):
    """Post-condition 7 must actually detect a changed dataset.

    Simulates the failure it exists for -- something in the run touching
    data/raw/measurements_v0.1.csv -- by mutating the dataset mid-run, and
    requires the migration to fail and restore rather than report success.

    MUTATION: remove the `_sha256(dataset) != dataset_sha_before` check
    -> this fails.
    """
    tracking, screening, dataset = bench
    before_tracking = tracking.read_bytes()
    real_render = mig.render_new_lines

    def render_and_scribble(papers):
        dataset.write_text("measurement_id\nCORRUPTED\n", encoding="utf-8")
        return real_render(papers)

    monkeypatch.setattr(mig, "render_new_lines", render_and_scribble)
    assert run(tracking, screening, dataset) == 1
    assert "must" in capsys.readouterr().err
    assert tracking.read_bytes() == before_tracking


def test_dry_run_writes_nothing(bench):
    """MUTATION: let --dry-run fall through to the write -> this fails."""
    tracking, screening, dataset = bench
    before = tracking.read_bytes()
    assert run(tracking, screening, dataset, "--dry-run") == 0
    assert tracking.read_bytes() == before


def test_post_condition_failure_restores_the_original(bench, monkeypatch):
    """A failed post-condition must leave the file exactly as it was.

    MUTATION: remove the restore-from-backup on failure -> this fails.
    """
    tracking, screening, dataset = bench
    before = tracking.read_bytes()

    def boom(*a, **k):
        raise mig.MigrationError("induced")

    monkeypatch.setattr(mig, "verify", boom)
    assert run(tracking, screening, dataset) == 1
    assert tracking.read_bytes() == before


# --- the real artifacts -----------------------------------------------------

def test_real_screening_file_is_loadable_and_fully_verified():
    """Every record shipped must carry a confirmed or corrected DOI.

    MUTATION: add an entry with verdict 'unresolved' -> this fails.
    """
    papers = mig.load_new_papers(_ROOT / "references" / "phase_d_screening.json")
    assert len(papers) == 35
    assert all(
        p["provenance"]["verdict"] in ("confirmed", "corrected") for p in papers
    )
    ids = [p["paper_id"] for p in papers]
    assert ids == [f"HYC-{n:04d}" for n in range(31, 66)]
    dois = [p["doi"] for p in papers]
    assert len(set(dois)) == len(dois)
    assert all(d == d.lower() and d.startswith("10.") for d in dois)


def test_real_screening_file_rows_render_to_thirteen_fields():
    """MUTATION: add a column to build_row -> this fails."""
    papers = mig.load_new_papers(_ROOT / "references" / "phase_d_screening.json")
    for p in papers:
        row = mig.build_row(p)
        assert len(row) == mig.EXPECTED_COLUMNS
        assert not any(ch in v for v in row for ch in "\r\n\t\x00")
