"""Tests for scripts/migrate_v2.py (docs/migration_v2_plan.md).

The migration runs against the frozen schema v1.3 file, so these tests hold after
the live dataset's v2 columns start being filled in.
"""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from pathlib import Path

import migrate_v2
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = REPO_ROOT / "tests" / "fixtures" / "measurements_v0.1_schema_v1_3.csv"
SCRIPT = REPO_ROOT / "scripts" / "migrate_v2.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def pre_image(tmp_path: Path) -> Path:
    target = tmp_path / "measurements_v0.1.csv"
    shutil.copy2(SNAPSHOT, target)
    return target


def read(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[0], rows[1:]


def test_the_new_columns_match_the_schema_v2_block_in_order():
    from hycan.schema import MeasurementEntry

    fields = list(MeasurementEntry.model_fields)
    assert fields[fields.index("basis_stated") :] == migrate_v2.NEW_COLUMNS
    assert len(migrate_v2.NEW_COLUMNS) == 30


def test_migration_appends_empty_columns_and_keeps_every_original_byte(
    pre_image, tmp_path
):
    before = pre_image.read_bytes()
    old_header, old_rows = read(pre_image)
    result = run("--dataset", str(pre_image), "--backup-dir", str(tmp_path / "bk"))
    assert result.returncode == 0, result.stderr
    header, rows = read(pre_image)
    assert header == old_header + migrate_v2.NEW_COLUMNS
    assert len(rows) == len(old_rows)
    for old, new in zip(old_rows, rows):
        assert new[: len(old)] == old
        assert all(cell == "" for cell in new[len(old) :])
    after = pre_image.read_bytes()
    for a, b in zip(before.split(b"\n"), after.split(b"\n")):
        assert b.startswith(a.rstrip(b"\r"))


def test_the_migrated_snapshot_equals_the_live_dataset_while_v2_is_uncoded(
    pre_image, tmp_path
):
    """Until any v2 cell is coded, migrating the v1.3 file must give the live file.

    Once coding starts this stops being true by design, and the test skips.
    """
    live = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"
    header, rows = read(live)
    start = header.index("basis_stated")
    if any(cell for row in rows for cell in row[start:]):
        pytest.skip("schema v2 columns are being coded; round trip no longer applies")
    assert (
        run(
            "--dataset", str(pre_image), "--backup-dir", str(tmp_path / "bk")
        ).returncode
        == 0
    )
    assert pre_image.read_bytes() == live.read_bytes()


def test_the_migration_refuses_to_run_twice(pre_image, tmp_path):
    assert (
        run(
            "--dataset", str(pre_image), "--backup-dir", str(tmp_path / "bk")
        ).returncode
        == 0
    )
    once = pre_image.read_bytes()
    second = run("--dataset", str(pre_image), "--backup-dir", str(tmp_path / "bk"))
    assert second.returncode == 1
    assert "Refusing to run twice" in second.stderr
    assert pre_image.read_bytes() == once


def test_dry_run_writes_nothing(pre_image):
    before = pre_image.read_bytes()
    assert run("--dataset", str(pre_image), "--dry-run").returncode == 0
    assert pre_image.read_bytes() == before


def test_an_unexpected_row_count_is_refused(pre_image):
    before = pre_image.read_bytes()
    result = run("--dataset", str(pre_image), "--dry-run", "--expected-rows", "7")
    assert result.returncode == 1
    assert pre_image.read_bytes() == before
