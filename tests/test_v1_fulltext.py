"""Tests for scripts/v1_search/fulltext.py (the §7 walk and the §6 eligibility decision)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "v1_search"))
spec = importlib.util.spec_from_file_location(
    "fulltext", REPO_ROOT / "scripts" / "v1_search" / "fulltext.py")
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)


def plan(n, st="S1", oa=True, doi=True):
    return [{"stratum": st, "position": str(i + 1), "frame_id": f"F{i:05d}",
             "route1_url": "https://oa/x" if oa else "", "title": f"t{i}", "year": "2010",
             "route2_url": "https://doi.org/x" if doi else ""} for i in range(n)]


def log(fid, route, outcome, file="main.pdf"):
    return {"frame_id": fid, "file": file, "route": route, "url": "u", "outcome": outcome,
            "sha256": "ab" if outcome == "obtained" else "", "bytes": "", "at_utc": "", "note": ""}


def elig(fid, ok):
    return {"frame_id": fid, "eligible": "true" if ok else "false"}


def test_walk_takes_records_in_order_and_skips_unretrieved():
    p = plan(5)
    lg = [log("F00000", "oa", "obtained"),
          log("F00001", "oa", "no_full_text"), log("F00001", "library", "no_full_text"),
          log("F00002", "oa", "no_full_text")]
    s = ft.walk(p, lg, [elig("F00000", True)], [])["S1"]
    assert (s["taken"], s["assessed"], s["eligible"], s["not_retrieved"]) == (2, 1, 1, 1)
    assert s["next_to_retrieve"] == ["F00002"] and s["stopped"] is None
    assert s["retrieve_ahead"] == ["F00002", "F00003", "F00004"]


def test_walk_stops_at_target_and_cap_and_counts_duplicates(monkeypatch):
    monkeypatch.setitem(ft.TARGET, "S1", 2)
    monkeypatch.setitem(ft.CAP, "S1", 3)
    p = plan(6)
    lg = [log(f"F0000{i}", "oa", "obtained") for i in range(6)]
    s = ft.walk(p, lg, [elig("F00000", True), elig("F00001", True)], [])["S1"]
    assert s["stopped"] == "target reached" and s["taken"] == 2
    el = [elig("F00000", False), elig("F00002", False), elig("F00003", False)]
    s = ft.walk(p, lg, el, [{"frame_id": "F00001"}])["S1"]
    assert s["stopped"] == "assessment cap"
    assert (s["taken"], s["assessed"], s["frame_duplicate"]) == (4, 3, 1)


def test_a_record_with_no_route_is_not_retrieved():
    p = plan(2, oa=False, doi=False)
    s = ft.walk(p, [], [], [])["S1"]
    assert s["not_retrieved"] == 2 and s["stopped"] == "plan exhausted"


def test_log_rows_are_checked():
    with pytest.raises(ft.WalkError):
        ft.walk(plan(1), [log("F09999", "oa", "obtained")], [], [])
    bad = log("F00000", "oa", "obtained"); bad["sha256"] = ""
    with pytest.raises(ft.WalkError):
        ft.walk(plan(1), [bad], [], [])


def assessment(fid, eligible, code=None, met=True):
    crit = {c: {"met": met if c != "I1" else (eligible or code != "theoretical_only"),
                "quote": "q", "location": "main"} for c in ft.CRITERIA}
    if eligible:
        crit = {c: {"met": True, "quote": "q", "location": "main"} for c in ft.CRITERIA}
    return {"frame_id": fid, "eligible": eligible, "exclusion_code": code, "criteria": crit}


def test_decide_uses_agreement_or_the_resolver():
    a = assessment("F1", True)
    row = ft.decide(a, assessment("F1", True), None)
    assert row["agree"] == "true" and row["eligible"] == "true"
    b = assessment("F1", False, "no_surface_area")
    b["criteria"]["I4"]["met"] = False
    with pytest.raises(ft.WalkError):
        ft.decide(a, b, None)
    row = ft.decide(a, b, b)
    assert row["resolved"] == "true" and row["exclusion_code"] == "no_surface_area"
    with pytest.raises(ft.WalkError):
        ft.decide(a, assessment("F1", True), a)


def test_assessment_format_is_checked(tmp_path):
    import json
    a = assessment("F1", True); a["criteria"]["I3"]["quote"] = ""
    f = tmp_path / "a.json"; f.write_text(json.dumps(a))
    with pytest.raises(ft.WalkError, match="I3 met without a quote"):
        ft.load_assessment(f, "F1")


def test_a_supplementary_zip_is_unpacked_to_its_one_document(tmp_path):
    import zipfile
    z = tmp_path / "si1.zip"
    with zipfile.ZipFile(z, "w") as w:
        w.writestr("../../escape/Supplementary.PDF", b"%PDF-1.4 x")
        w.writestr("__MACOSX/._Supplementary.PDF", b"junk")
        w.writestr("movie.mp4", b"video")
    out = ft.unzip_document(z)
    assert out == tmp_path / "si1.pdf" and out.read_bytes() == b"%PDF-1.4 x"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["si1.pdf", "si1.zip"]
    two = tmp_path / "si2.zip"
    with zipfile.ZipFile(two, "w") as w:
        w.writestr("a.pdf", b"%PDF-"); w.writestr("b.docx", b"x")
    with pytest.raises(ft.WalkError, match="holds 2 documents"):
        ft.unzip_document(two)


def test_a_zip_of_data_tables_becomes_one_text_file_in_name_order(tmp_path):
    import zipfile
    z = tmp_path / "si1.zip"
    with zipfile.ZipFile(z, "w") as w:
        w.writestr("N2--MOF-5.csv", "p,q\n0.1,5\n")
        w.writestr("../H2.77K--MOF-5.tab", "P\tn\n1\t2\n")
        w.writestr("MANIFEST.TXT", "2 files\n")
        w.writestr("plot.png", b"image")
    out = ft.unzip_document(z)
    assert out == tmp_path / "si1.txt"
    assert out.read_text() == ("==== ../H2.77K--MOF-5.tab ====\nP\tn\n1\t2\n\n"
                               "==== MANIFEST.TXT ====\n2 files\n\n"
                               "==== N2--MOF-5.csv ====\np,q\n0.1,5\n\n")
    assert sorted(p.name for p in tmp_path.iterdir()) == ["si1.txt", "si1.zip"]
    mixed = tmp_path / "si2.zip"
    with zipfile.ZipFile(mixed, "w") as w:
        w.writestr("a.csv", "x"); w.writestr("b.pdf", b"%PDF-")
    with pytest.raises(ft.WalkError, match="holds 2 documents"):
        ft.unzip_document(mixed)


def test_collect_writes_the_outcome_and_keeps_the_assessments(tmp_path, monkeypatch):
    import argparse, json
    monkeypatch.setattr(ft, "ELIG", tmp_path / "eligibility.csv")
    a, b = tmp_path / "a_in.json", tmp_path / "b_in.json"
    a.write_text(json.dumps(assessment("F00001", True)))
    b.write_text(json.dumps(assessment("F00001", True)))
    args = argparse.Namespace(frame_id="F00001", a=str(a), b=str(b), resolver=None)
    assert ft.cmd_collect(args) == 0
    assert [r["eligible"] for r in ft.read(ft.ELIG)] == ["true"]
    kept = tmp_path / "eligibility" / "F00001"
    assert sorted(p.name for p in kept.iterdir()) == ["a.json", "b.json"]
    assert kept.joinpath("a.json").read_bytes() == a.read_bytes()
    with pytest.raises(ft.WalkError, match="already has an outcome"):
        ft.cmd_collect(args)


def test_retrieval_comparison_tables():
    rc_spec = importlib.util.spec_from_file_location(
        "retrieval_comparison", REPO_ROOT / "scripts" / "v1_search" / "retrieval_comparison.py")
    rc = importlib.util.module_from_spec(rc_spec)
    rc_spec.loader.exec_module(rc)
    recs = [{"frame_id": f"F{i}", "stratum": "S1" if i < 4 else "S2", "retrieved": i % 2 == 0,
             "route": "oa" if i % 2 == 0 else "", "year": 2010 + i,
             "publisher": "Big" if i < 6 else f"Small{i}", "oa_status": "closed"} for i in range(8)]
    c = rc.compare(recs)
    assert c["n"] == {"retrieved": 4, "not_retrieved": 4}
    assert c["retrieved_by_route"] == {"oa": 4}
    assert c["stratum"] == [
        {"category": "S1", "retrieved": 2, "not_retrieved": 2, "retrieved_share": 0.5,
         "not_retrieved_share": 0.5, "retrieved_fraction": 0.5},
        {"category": "S2", "retrieved": 2, "not_retrieved": 2, "retrieved_share": 0.5,
         "not_retrieved_share": 0.5, "retrieved_fraction": 0.5}]
    assert c["publishers_pooled_as_other"] == ["Small6", "Small7"]
    assert {r["category"]: r["retrieved"] + r["not_retrieved"] for r in c["publisher"]} == {
        "Big": 6, "other": 2}
    assert c["year"]["retrieved"]["median"] == 2013
    assert [r["category"] for r in c["period"]] == ["<= 2015", ">= 2016"]
