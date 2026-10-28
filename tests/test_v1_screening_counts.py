"""Tests for scripts/v1_search/screening_counts.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "v1_search"))
spec = importlib.util.spec_from_file_location(
    "screening_counts", REPO_ROOT / "scripts" / "v1_search" / "screening_counts.py"
)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def row(d, code="", stratum=""):
    return {"decision": d, "exclusion_code": code, "stratum": stratum}


def test_agreement_and_screener_counts():
    a = {"F1": row("include", stratum="S1"), "F2": row("exclude", "not_carbon"),
         "F3": row("uncertain", stratum="S2"), "F4": row("exclude", "retracted")}
    b = {"F1": row("uncertain", stratum="S2"), "F2": row("exclude", "not_carbon"),
         "F3": row("exclude", "not_primary"), "F4": row("include", stratum="S2")}
    g = sc.agreement(["F1", "F2", "F3", "F4"], a, b)
    assert (g["agreement"], g["kept_by_a_only"], g["kept_by_b_only"],
            g["excluded_by_both"]) == (0.5, 1, 1, 1)
    s = sc.screener(a)
    assert s["decisions"] == {"exclude": 2, "include": 1, "uncertain": 1}
    assert s["exclusion_codes"] == {"not_carbon": 1, "retracted": 1}
    assert s["strata"] == {"S1": 1, "S2": 1}
