"""Tests for scripts/v1_search/audit.py (the §12 audit draw)."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_audit", REPO_ROOT / "scripts" / "v1_search" / "audit.py"
)
au = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = au
spec.loader.exec_module(au)


def test_settle_quotas_moves_a_shortfall_within_its_stratum():
    cells = {("a", "agreed"): list("ab"), ("a", "resolved"): [f"r{i}" for i in range(40)],
             ("b", "agreed"): list("ABCDEFGHIJ"), ("b", "resolved"): list("KLMNOPQRST"),
             ("c", "all"): list("0123456789")}
    q = au.settle_quotas(cells)
    assert q[("a", "agreed")] == 2 and q[("a", "resolved")] == 28
    assert q[("b", "agreed")] == 8 and q[("b", "resolved")] == 7
    assert q[("c", "all")] == 10  # capped at the pool


def test_settle_quotas_caps_the_other_cell_at_its_pool():
    cells = {("a", "agreed"): list("ab"), ("a", "resolved"): list("cdefg"),
             ("b", "agreed"): list("ABCDEFGHIJ"), ("b", "resolved"): list("KLMNOPQRST"),
             ("c", "all"): list(map(str, range(20)))}
    q = au.settle_quotas(cells)
    assert q[("a", "agreed")] == 2 and q[("a", "resolved")] == 5
    assert q[("c", "all")] == 15


def write_csv(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def test_agreed_classifier_reads_match_lines_and_resolutions(tmp_path):
    pid = "HYC-9001"
    write_csv(tmp_path / pid / "C_input" / "match.csv",
              ["match_line", "status", "first_measurement_id",
               "second_measurement_id", "field", "first_value", "second_value"],
              [
                  # line 1: agreed pair, untouched by C -> agreed.
                  {"match_line": "1", "status": "agree",
                   "first_measurement_id": "M1", "second_measurement_id": "B1"},
                  # line 2: a differing field -> resolved.
                  {"match_line": "2", "status": "differ",
                   "first_measurement_id": "M2", "second_measurement_id": "B2",
                   "field": "uptake_wt_pct"},
                  # line 3: agreed pair later corrected by C -> resolved.
                  {"match_line": "3", "status": "agree",
                   "first_measurement_id": "M3", "second_measurement_id": "B3"},
                  # line 4: only_second row C kept as M9 -> resolved.
                  {"match_line": "4", "status": "only_second",
                   "first_measurement_id": "", "second_measurement_id": "B4"},
              ])
    write_csv(tmp_path / pid / "C" / "resolutions.csv",
              ["match_line", "field", "first_value", "second_value", "decision",
               "final_value", "evidence", "location"],
              [
                  {"match_line": "2", "field": "uptake_wt_pct", "decision": "first",
                   "final_value": "4.2"},
                  {"match_line": "3", "field": "temperature_k", "decision": "new",
                   "final_value": "77"},
                  {"match_line": "4", "field": "row", "decision": "second",
                   "final_value": "M9"},
              ])
    is_agreed = au.agreed_classifier(tmp_path, pid)
    assert is_agreed("M1")
    assert not is_agreed("M2")
    assert not is_agreed("M3")   # its agree line carries a correction
    assert not is_agreed("M9")   # named by a resolution's final_value
    assert not is_agreed("M99")  # unknown to the match -> never agreed


def test_draw_reproduces_the_committed_files(tmp_path):
    committed = REPO_ROOT / "references" / "v1_audit"
    rc = au.main(["draw", "--out", str(tmp_path)])
    assert rc == 0
    for name in ("draw.csv", "cells.json", "sheet.csv"):
        assert (tmp_path / name).read_bytes() == (committed / name).read_bytes(), name
