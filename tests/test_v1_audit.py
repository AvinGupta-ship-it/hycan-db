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


def test_score_counts_wrong_verdicts_with_the_s12_weights(tmp_path):
    import json
    # Two drawn rows: one table row (11 fields), one figure row (12 fields).
    processed = tmp_path / "p.csv"
    write_csv(processed, ["measurement_id", "paper_id", "extraction_method"],
              [{"measurement_id": "M1", "paper_id": "P1",
                "extraction_method": "table_direct"},
               {"measurement_id": "M2", "paper_id": "P2",
                "extraction_method": "figure_digitized"}])
    out = tmp_path / "out"
    write_csv(out / "draw.csv",
              ["audit_stratum", "cell", "order", "paper_id", "measurement_id"],
              [{"audit_stratum": "a", "cell": "agreed", "order": "1",
                "paper_id": "P1", "measurement_id": "M1"},
               {"audit_stratum": "c", "cell": "all", "order": "1",
                "paper_id": "P2", "measurement_id": "M2"}])
    (out / "cells.json").write_text(json.dumps({"cells": {
        "a/agreed": {"pool": 14, "quota": 1}, "c/all": {"pool": 30, "quota": 1}}}))
    rows = [{"measurement_id": "M1", "field": f, "verdict": "matches",
             "pdf_value": ""} for f in au.VERIFY_FIELDS]
    rows += [{"measurement_id": "M2", "field": f, "verdict": "matches",
              "pdf_value": ""} for f in au.VERIFY_FIELDS]
    rows.append({"measurement_id": "M2", "field": "digitized_point",
                 "verdict": "wrong", "pdf_value": "20.5; 1.9 wt%"})
    verdicts = tmp_path / "verdicts.csv"
    write_csv(verdicts, ["measurement_id", "field", "verdict", "pdf_value"], rows)

    rc = au.main(["score", "--verdicts", str(verdicts),
                  "--processed", str(processed), "--out", str(out)])
    assert rc == 0
    rep = json.loads((out / "score.json").read_text())
    assert rep["strata"]["a"]["row_errors"] == 0
    assert rep["strata"]["c"]["row_errors"] == 1
    assert rep["fields"]["c/digitized_point"] == {
        "errors": 1, "n": 1, "ci95": rep["fields"]["c/digitized_point"]["ci95"]}
    # Weighted overall: M1 clean (weight 14), M2 errored (weight 30).
    assert abs(rep["overall"]["weighted_row_error_rate"] - 30 / 44) < 1e-12


def test_score_refuses_a_missing_field_verdict(tmp_path, capsys):
    import json
    processed = tmp_path / "p.csv"
    write_csv(processed, ["measurement_id", "paper_id", "extraction_method"],
              [{"measurement_id": "M1", "paper_id": "P1",
                "extraction_method": "figure_digitized"}])
    out = tmp_path / "out"
    write_csv(out / "draw.csv",
              ["audit_stratum", "cell", "order", "paper_id", "measurement_id"],
              [{"audit_stratum": "b", "cell": "agreed", "order": "1",
                "paper_id": "P1", "measurement_id": "M1"}])
    (out / "cells.json").write_text(json.dumps({"cells": {
        "b/agreed": {"pool": 8, "quota": 1}}}))
    verdicts = tmp_path / "verdicts.csv"
    write_csv(verdicts, ["measurement_id", "field", "verdict", "pdf_value"],
              [{"measurement_id": "M1", "field": f, "verdict": "matches",
                "pdf_value": ""} for f in au.VERIFY_FIELDS])  # no digitized_point
    rc = au.main(["score", "--verdicts", str(verdicts),
                  "--processed", str(processed), "--out", str(out)])
    assert rc == 1
    assert "digitized_point" in capsys.readouterr().err


def test_clopper_pearson_bounds():
    lo, hi = au.clopper_pearson(0, 30)
    assert lo == 0.0 and 0.10 < hi < 0.13
    lo, hi = au.clopper_pearson(30, 30)
    assert hi == 1.0 and 0.87 < lo < 0.90
