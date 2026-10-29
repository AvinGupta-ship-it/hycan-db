"""Tests for scripts/v1_search/prisma.py (PRISMA 2020 counts, protocol §14)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "v1_search"))
spec = importlib.util.spec_from_file_location(
    "prisma", REPO_ROOT / "scripts" / "v1_search" / "prisma.py")
pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr)


def merge(**kw):
    m = {"merged_sha256": "x", "openalex_unique": 98, "openalex_doi_duplicates_merged": 2,
         "openalex_subqueries": 4, "openalex_count_sum": 150, "s2_records": 50,
         "s2_matched_doi": 30, "s2_matched_title_year": 5, "merged_total": 113}
    m.update(kw)
    return m


def test_identification_checks_the_arithmetic_and_the_merged_file():
    i = pr.identification(merge(), "x")
    assert i["openalex"]["records"] == 100
    assert i["duplicates_removed"]["total"] == 37
    assert i["merged"] == 113
    with pytest.raises(pr.PrismaError):
        pr.identification(merge(), "y")
    with pytest.raises(pr.PrismaError):
        pr.identification(merge(merged_total=112), "x")


def scr(fid, d, code=""):
    return {"frame_id": fid, "decision": d, "exclusion_code": code}


def test_screening_counts_double_exclusions_by_code():
    a = [scr("F1", "exclude", "not_carbon"), scr("F2", "exclude", "retracted"),
         scr("F3", "include"), scr("F4", "exclude", "not_primary")]
    b = [scr("F1", "exclude", "not_carbon"), scr("F2", "exclude", "not_primary"),
         scr("F3", "exclude", "not_carbon"), scr("F4", "uncertain")]
    frame = [{"frame_id": "F3", "stratum": "S1"}, {"frame_id": "F4", "stratum": "S2"}]
    s = pr.screening(a, b, frame, 4)
    assert s["excluded_by_both"] == {"total": 2, "same_code": {"not_carbon": 1}, "codes_differ": 1}
    assert s["frame"] == {"total": 2, "S1": 1, "S2": 1}
    with pytest.raises(pr.PrismaError):
        pr.screening(a, b, frame[:1], 4)


def plan_row(fid, oa=True):
    return {"stratum": "S2", "position": "1", "frame_id": fid,
            "route1_url": "u" if oa else "", "route2_url": "d"}


def log(fid, route, outcome):
    return {"frame_id": fid, "file": "main.pdf", "route": route, "outcome": outcome}


def test_v01_lane_separates_drawn_retrieved_not_retrieved_and_unfinished():
    plan = [plan_row("F1"), plan_row("F2"), plan_row("F3", oa=False), plan_row("F4"),
            plan_row("F5")]
    lg = [log("F2", "oa", "obtained"),
          log("F3", "library", "no_full_text"),
          log("F4", "oa", "no_full_text"),
          log("F5", "library", "obtained")]
    elig = [{"frame_id": "F1", "eligible": "true", "exclusion_code": ""},
            {"frame_id": "F2", "eligible": "false", "exclusion_code": "no_surface_area"}]
    v01 = {"P1": "F1", "P2": "F2", "P3": "F3", "P4": "F4", "P5": "F5"}
    lane = pr.v01_lane(plan, lg, elig, v01, {"F1": "S2"})
    assert (lane["drawn"], lane["drawn_eligible"], lane["not_drawn"]) == (1, 1, 4)
    assert lane["retrieved"] == 2
    assert lane["not_retrieved"] == ["P3"]          # its only route was tried
    assert lane["awaiting_retrieval"] == ["P4"]     # route 2 not yet tried
    assert lane["not_assessed_yet"] == ["P5"]
    assert (lane["assessed"], lane["excluded"]) == (1, 1)
    assert lane["excluded_codes"] == {"no_surface_area": 1}


def test_review_must_cover_every_exclusion_and_reversals_stop_the_counts():
    rev = [{"frame_id": "F1", "decision": "confirm"}, {"frame_id": "F2", "decision": "confirm"}]
    assert pr.review_counts(rev, {"F1", "F2"}) == {"reviewed": 2, "confirmed": 2, "reversed": 0}
    with pytest.raises(pr.PrismaError):
        pr.review_counts(rev, {"F1", "F2", "F3"})
    with pytest.raises(pr.PrismaError):
        pr.review_counts([{"frame_id": "F1", "decision": "reverse"}], {"F1"})


def test_committed_counts_are_reproduced():
    committed = REPO_ROOT / "references" / "v1_prisma" / "prisma_counts.json"
    if not committed.exists():
        pytest.skip("no committed PRISMA counts")
    assert json.loads(committed.read_text(encoding="utf-8")) == json.loads(
        json.dumps(pr.counts()))
