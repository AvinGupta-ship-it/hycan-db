"""Tests for scripts/v1_search/dataset.py (v1.0 dataset assembly)."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_dataset", REPO_ROOT / "scripts" / "v1_search" / "dataset.py"
)
ds = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ds
spec.loader.exec_module(ds)

TREE = REPO_ROOT / "references" / "v1_extraction"
V01 = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"


def read(path):
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def write(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def make_tree(tmp_path, c_rows):
    """A collected tree with one dual paper (real reconciled rows) and the
    mode-none paper, against the real v0.1 file."""
    cols, _ = read(TREE / "HYC-0048" / "C" / "rows.csv")
    tree = tmp_path / "tree"
    write(
        tree / "papers.csv",
        ["paper_id", "mode", "selection_route", "frame_id"],
        [
            {"paper_id": "HYC-0048", "mode": "dual",
             "selection_route": "S1", "frame_id": "F01196"},
            {"paper_id": "HYC-0041", "mode": "none",
             "selection_route": "legacy_v0.1_not_retrieved", "frame_id": "F02292"},
        ],
    )
    write(tree / "HYC-0048" / "C" / "rows.csv", cols, c_rows)
    return tree


def test_assembles_reconciled_and_carried_over_rows(tmp_path):
    cols, c_rows = read(TREE / "HYC-0048" / "C" / "rows.csv")
    tree = make_tree(tmp_path, c_rows)
    out = tmp_path / "v1.csv"
    processed = tmp_path / "v1_computed.csv"
    rc = ds.main(["--tree", str(tree), "--v01", str(V01),
                  "--out", str(out), "--processed", str(processed)])
    assert rc == 0

    out_cols, rows = read(out)
    assert out_cols == cols
    v01_41 = [r for _, rs in [read(V01)] for r in rs if r["paper_id"] == "HYC-0041"]
    assert len(rows) == len(c_rows) + len(v01_41)
    assert [r["paper_id"] for r in rows[: len(c_rows)]] == ["HYC-0048"] * len(c_rows)
    # Provenance is filled from papers.csv on every row, including HYC-0041's.
    assert {r["selection_route"] for r in rows[: len(c_rows)]} == {"S1"}
    hyc41 = [r for r in rows if r["paper_id"] == "HYC-0041"]
    assert {r["selection_route"] for r in hyc41} == {"legacy_v0.1_not_retrieved"}
    assert {r["frame_id"] for r in hyc41} == {"F02292"}
    # Every other cell of a carried-over row is its v0.1 value.
    skip = set(ds.PROVENANCE)
    for got, src in zip(hyc41, v01_41):
        assert {k: v for k, v in got.items() if k not in skip} == \
               {k: v for k, v in src.items() if k not in skip}

    p_cols, p_rows = read(processed)
    assert set(p_cols) > set(cols)
    assert "reporting_score" in p_cols and "nmax_status" in p_cols
    assert len(p_rows) == len(rows)
    # The carried-over rows are uncoded, so their computed fields are null.
    assert {r["reporting_score"] for r in p_rows if r["paper_id"] == "HYC-0041"} == {""}


def test_refuses_schema_errors_and_writes_nothing(tmp_path):
    _, c_rows = read(TREE / "HYC-0048" / "C" / "rows.csv")
    bad = [dict(r) for r in c_rows]
    bad[0]["temperature_k"] = "9999"  # outside the registered 50-500 K range
    tree = make_tree(tmp_path, bad)
    out = tmp_path / "v1.csv"
    rc = ds.main(["--tree", str(tree), "--v01", str(V01),
                  "--out", str(out), "--processed", str(tmp_path / "p.csv")])
    assert rc == 1
    assert not out.exists()
