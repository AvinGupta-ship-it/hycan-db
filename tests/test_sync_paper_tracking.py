"""Tests for scripts/sync_paper_tracking.py and the tracking/dataset invariant.

Each test that guards a safety property carries a MUTATION: line naming the
change it would catch, per the convention in test_schema_v1_2.py. §6.7 makes a
passing suite weak evidence, so every guard here was confirmed to fail against
the mutation it names.
"""

from __future__ import annotations

import csv
import io
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "sync_paper_tracking.py"
TRACKING = REPO_ROOT / "references" / "paper_tracking.csv"
DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"

PAPER_ID_RE = re.compile(r"^HYC-\d{4}$")

TRACKING_HEADER = [
    "paper_id",
    "title",
    "authors",
    "year",
    "journal",
    "doi",
    "search_source",
    "screening_decision",
    "exclusion_reason",
    "pdf_obtained",
    "extraction_status",
    "extraction_date",
    "notes",
]

DUAL_AGENT_PAPERS = {
    "HYC-0009",
    "HYC-0011",
    "HYC-0012",
    "HYC-0015",
    "HYC-0017",
    "HYC-0019",
    "HYC-0022",
    "HYC-0025",
    "HYC-0026",
    "HYC-0029",
}


def run_script(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def read_tracking(path: Path = TRACKING) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[0], rows[1:]


def tracking_map(path: Path = TRACKING) -> dict[str, dict[str, str]]:
    header, rows = read_tracking(path)
    return {row[0]: dict(zip(header, row)) for row in rows}


def dataset_papers() -> set[str]:
    with DATASET.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        col = header.index("paper_id")
        return {row[col] for row in reader if row}


def dataset_rows() -> list[dict[str, str]]:
    with DATASET.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


# --- The invariant. This is the part that outlasts the migration. ------------
#
# §9.1 step 15 was skipped for ten consecutive papers because nothing checked
# it. These tests are the check. They assert against the real files, not a
# fixture, exactly as test_dataset_invariants.py does.


def test_every_dataset_paper_is_tracked_as_extracted_or_verified():
    """MUTATION: mark any extracted paper `not_started` again -> this fails."""
    tracked = tracking_map()
    for paper in sorted(dataset_papers()):
        assert paper in tracked, f"{paper} is in the dataset with no tracking row"
        status = tracked[paper]["extraction_status"]
        assert status in {"extracted", "verified"}, (
            f"{paper} has rows in the dataset but is tracked as {status!r}. "
            f"§9.1 step 15 sets this when the paper is appended."
        )


def test_every_tracked_extracted_paper_has_an_extraction_date():
    """MUTATION: blank any extraction_date on an extracted row -> this fails."""
    for paper, row in sorted(tracking_map().items()):
        if row["extraction_status"] in {"extracted", "verified"}:
            assert row["extraction_date"].strip(), (
                f"{paper} is {row['extraction_status']} with no extraction_date"
            )


def test_every_paper_id_in_the_tracking_file_is_well_formed():
    """MUTATION: restore the malformed `HYC-009` -> this fails.

    The malformed id is why an ID-matching fix would have silently skipped
    Ioannatos 2010. §8.2 requires the HYC-XXXX pattern.
    """
    bad = [pid for pid in tracking_map() if not PAPER_ID_RE.match(pid)]
    assert not bad, f"malformed paper_id values: {bad}"


def test_dual_agent_verified_papers_are_tracked_as_verified():
    """MUTATION: downgrade a dual-agent paper to `extracted` -> this fails.

    §5.2 defines `verified` as the dual-agent protocol completed with all
    disputes resolved. A paper whose every row carries
    extractor = "HyCAN pipeline v2" meets that definition by construction.
    """
    by_paper: dict[str, set[str]] = {}
    for row in dataset_rows():
        by_paper.setdefault(row["paper_id"], set()).add(row["extractor"])
    pipeline_papers = {
        paper
        for paper, extractors in by_paper.items()
        if extractors == {"HyCAN pipeline v2"}
    }
    assert pipeline_papers == DUAL_AGENT_PAPERS, (
        "the set of dual-agent papers in the dataset changed; update the "
        "migration plan and this test together"
    )
    tracked = tracking_map()
    for paper in sorted(pipeline_papers):
        assert tracked[paper]["extraction_status"] == "verified", (
            f"{paper} is fully dual-agent extracted but tracked as "
            f"{tracked[paper]['extraction_status']!r}"
        )


def test_single_reader_papers_are_not_claimed_as_verified():
    """MUTATION: mark a v1.0 paper `verified` -> this fails.

    The 121 v1.0 rows have an empty verified_by. Calling them verified would
    assert a second reading that never happened — the decision in plan §2.
    """
    by_paper: dict[str, set[str]] = {}
    verified_by: dict[str, set[str]] = {}
    for row in dataset_rows():
        by_paper.setdefault(row["paper_id"], set()).add(row["extractor"])
        verified_by.setdefault(row["paper_id"], set()).add(
            row["verified_by"].strip()
        )
    tracked = tracking_map()
    for paper, extractors in sorted(by_paper.items()):
        if "HyCAN pipeline v2" in extractors:
            continue
        assert verified_by[paper] == {""}, (
            f"{paper} is a v1.0 paper with a populated verified_by; the "
            f"premise of this test no longer holds"
        )
        assert tracked[paper]["extraction_status"] == "extracted", (
            f"{paper} was read once by one reader but is tracked as "
            f"{tracked[paper]['extraction_status']!r}"
        )


def test_no_unextracted_paper_claims_to_be_extracted():
    """MUTATION: mark a screened-only paper `extracted` -> this fails."""
    papers = dataset_papers()
    for paper, row in sorted(tracking_map().items()):
        if paper in papers:
            continue
        assert row["extraction_status"] not in {"extracted", "verified"}, (
            f"{paper} is tracked as {row['extraction_status']!r} with no rows "
            f"in the dataset"
        )


def test_the_tracking_file_shape_is_pinned():
    """MUTATION: add, drop or reorder a column -> this fails."""
    header, rows = read_tracking()
    assert header == TRACKING_HEADER
    assert len(rows) == 30
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != len(header)]
    assert not ragged, f"ragged rows at csv lines {ragged}"


def test_the_status_counts_are_what_the_migration_plan_states():
    """MUTATION: change any status -> this fails.

    Pinned so a status edit has to be deliberate, the same way the column
    count is pinned in test_dataset_invariants.py.
    """
    counts: dict[str, int] = {}
    for row in tracking_map().values():
        counts[row["extraction_status"]] = (
            counts.get(row["extraction_status"], 0) + 1
        )
    assert counts == {"extracted": 11, "verified": 10, "not_started": 9}


def test_every_dataset_paper_was_screened_in():
    """MUTATION: flip a screening_decision to exclude -> this fails."""
    tracked = tracking_map()
    for paper in sorted(dataset_papers()):
        assert tracked[paper]["screening_decision"] == "include", (
            f"{paper} is in the dataset but screened as "
            f"{tracked[paper]['screening_decision']!r}"
        )


# --- The script itself. ------------------------------------------------------


@pytest.fixture
def sandbox(tmp_path: Path) -> Path:
    """A working tree with a pre-migration tracking file and the real dataset."""
    (tmp_path / "references").mkdir()
    (tmp_path / "data" / "raw").mkdir(parents=True)

    header, rows = read_tracking()
    idx = {name: header.index(name) for name in header}
    pre = []
    for row in rows:
        row = list(row)
        pid = row[idx["paper_id"]]
        if pid == "HYC-0009":
            row[idx["paper_id"]] = "HYC-009"
        if pid in DUAL_AGENT_PAPERS:
            row[idx["extraction_status"]] = "not_started"
            row[idx["extraction_date"]] = ""
        if pid in {"HYC-0016", "HYC-0018", "HYC-0023"}:
            row[idx["extraction_date"]] = ""
        pre.append(row)

    # Reproduce the real file's byte format: CRLF, no trailing newline.
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(header)
    writer.writerows(pre)
    text = buffer.getvalue()
    assert text.endswith("\r\n")
    (tmp_path / "references" / "paper_tracking.csv").write_text(
        text[:-2], encoding="utf-8", newline=""
    )

    (tmp_path / "data" / "raw" / "measurements_v0.1.csv").write_bytes(
        DATASET.read_bytes()
    )
    return tmp_path


def test_the_script_applies_exactly_twenty_four_cell_changes(sandbox: Path):
    """MUTATION: widen the allowed columns in verify() -> this fails."""
    result = run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "24 cell change(s)" in result.stdout


def test_the_script_refuses_to_run_twice(sandbox: Path):
    """MUTATION: drop the already-applied guard -> this fails."""
    first = run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox)
    assert first.returncode == 0, first.stdout + first.stderr
    second = run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox)
    assert second.returncode != 0
    assert "already been applied" in second.stdout + second.stderr


def test_dry_run_writes_nothing(sandbox: Path):
    """MUTATION: make --dry-run write -> this fails."""
    path = sandbox / "references" / "paper_tracking.csv"
    before = path.read_bytes()
    result = run_script("--dry-run", "--backup-dir", str(sandbox / "bk"), cwd=sandbox)
    assert result.returncode == 0, result.stdout + result.stderr
    assert path.read_bytes() == before


def test_the_files_line_endings_and_final_newline_survive(sandbox: Path):
    """MUTATION: drop detect_format and write with csv.writer's defaults.

    This is not hypothetical. The first version of the script wrote LF and added
    a trailing newline to a CRLF file with none, changing the bytes of all 30
    lines while every cell value stayed correct. The cell-level check passed.
    Only a byte-level check catches it.
    """
    path = sandbox / "references" / "paper_tracking.csv"
    before = path.read_bytes()
    assert b"\r\n" in before, "fixture should reproduce the real file's CRLF"
    assert not before.endswith(b"\n"), "fixture should have no trailing newline"

    assert run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox).returncode == 0

    after = path.read_bytes()
    assert after.count(b"\r\n") == before.count(b"\r\n")
    assert after.endswith(b"\n") is False
    assert len(after.split(b"\n")) == len(before.split(b"\n"))

    changed = [
        i
        for i, (a, b) in enumerate(
            zip(before.split(b"\n"), after.split(b"\n")), start=1
        )
        if a != b
    ]
    assert len(changed) == 13, (
        f"expected 13 physical lines to change, {len(changed)} did: {changed}"
    )


def test_unnamed_cells_are_byte_identical(sandbox: Path):
    """MUTATION: route the write through pandas -> this fails.

    The whole reason the script uses the csv module is that a cell it does not
    name is byte-identical by construction. This asserts exactly that.
    """
    path = sandbox / "references" / "paper_tracking.csv"
    header_before, before = read_tracking(path)
    assert run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox).returncode == 0
    header_after, after = read_tracking(path)

    assert header_after == header_before
    allowed = {"paper_id", "extraction_status", "extraction_date"}
    for line, (old, new) in enumerate(zip(before, after), start=2):
        for col, (a, b) in enumerate(zip(old, new)):
            if a != b:
                assert header_before[col] in allowed, (
                    f"csv line {line}: {header_before[col]} changed from "
                    f"{a!r} to {b!r}, outside the plan's scope"
                )


def test_the_script_does_not_touch_the_dataset(sandbox: Path):
    """MUTATION: have the script open the dataset for writing -> this fails."""
    dataset = sandbox / "data" / "raw" / "measurements_v0.1.csv"
    before = dataset.read_bytes()
    assert run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox).returncode == 0
    assert dataset.read_bytes() == before


def test_the_script_backs_up_before_writing(sandbox: Path):
    """MUTATION: drop the backup -> this fails."""
    backup_dir = sandbox / "bk"
    assert run_script("--backup-dir", str(backup_dir), cwd=sandbox).returncode == 0
    backups = list(backup_dir.glob("paper_tracking.pre_sync.*.csv"))
    assert len(backups) == 1, f"expected one backup, found {backups}"


def _append_row(path: Path, cells: list[str]) -> None:
    """Append one well-formed CRLF row to a file that has no trailing newline.

    Appending "...\\n" naively would merge with the unterminated last line and
    trip the ragged-row guard instead of the guard under test.
    """
    with path.open(encoding="utf-8", newline="") as handle:
        text = handle.read()
    if not text.endswith("\r\n"):
        text += "\r\n"
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text + ",".join(cells) + "\r\n")


def test_the_script_refuses_a_wrong_row_count(sandbox: Path):
    """MUTATION: drop the row-count guard -> this fails."""
    path = sandbox / "references" / "paper_tracking.csv"
    _append_row(path, ["HYC-9999"] + [""] * 12)
    result = run_script("--backup-dir", str(sandbox / "bk"), cwd=sandbox)
    assert result.returncode != 0
    assert "expected 30 data rows" in result.stdout + result.stderr


def test_the_script_refuses_a_ragged_file(sandbox: Path):
    """MUTATION: drop the ragged-row guard -> this fails."""
    path = sandbox / "references" / "paper_tracking.csv"
    _append_row(path, ["HYC-9999", "too", "few"])
    result = run_script(
        "--expected-rows", "-1", "--backup-dir", str(sandbox / "bk"), cwd=sandbox
    )
    assert result.returncode != 0
    assert "ragged" in result.stdout + result.stderr


def test_the_script_refuses_a_file_missing_a_required_column(tmp_path: Path):
    """MUTATION: drop the column-name check -> this fails."""
    (tmp_path / "references").mkdir()
    (tmp_path / "data" / "raw").mkdir(parents=True)
    (tmp_path / "references" / "paper_tracking.csv").write_text(
        "a,b,c\n1,2,3\n", encoding="utf-8"
    )
    (tmp_path / "data" / "raw" / "measurements_v0.1.csv").write_bytes(
        DATASET.read_bytes()
    )
    result = run_script(
        "--expected-rows", "-1", "--backup-dir", str(tmp_path / "bk"), cwd=tmp_path
    )
    assert result.returncode != 0
    assert "13 columns" in result.stdout + result.stderr
