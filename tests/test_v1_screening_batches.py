"""Tests for scripts/v1_search/screening_batches.py."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "screening_batches", REPO_ROOT / "scripts" / "v1_search" / "screening_batches.py"
)
sb = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sb
spec.loader.exec_module(sb)


def test_split_and_join(tmp_path):
    merged = tmp_path / "merged.csv"
    with merged.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["frame_id", "doi", "title", "abstract", "venue",
                                           "year", "type", "is_retracted"])
        w.writeheader()
        for i in (3, 1, 2):
            w.writerow({"frame_id": f"F{i}", "title": f"t{i}", "is_retracted": "True"})
    assert sb.main(["split", "--merged", str(merged), "--out", str(tmp_path / "in"),
                    "--size", "2"]) == 0
    b1 = (tmp_path / "in" / "batch_001.csv").read_text()
    assert b1.splitlines()[0] == "frame_id,title,abstract,venue,year,type"
    assert "is_retracted" not in b1 and "F1" in b1 and "F2" in b1
    out = tmp_path / "out"
    out.mkdir()
    hdr = "frame_id,decision,exclusion_code,stratum,evidence\n"
    (out / "batch_001.csv").write_text(hdr + "F1,include,,S1,q\nF2,exclude,not_carbon,,q\n")
    (out / "batch_002.csv").write_text(hdr + "F3,uncertain,,S2,\n")
    assert sb.main(["join", "--inputs", str(tmp_path / "in"), "--outputs", str(out),
                    "--out", str(tmp_path / "screen_a.csv")]) == 0
    assert len((tmp_path / "screen_a.csv").read_text().splitlines()) == 4
    (out / "batch_002.csv").write_text(hdr + "F3,exclude,not_relevant,,\n")
    assert sb.main(["join", "--inputs", str(tmp_path / "in"), "--outputs", str(out),
                    "--out", str(tmp_path / "screen_x.csv")]) == 1
    assert not (tmp_path / "screen_x.csv").exists()


def test_join_report_counts_missing_and_unfound_evidence(tmp_path):
    inp, out = tmp_path / "in", tmp_path / "out"
    inp.mkdir()
    out.mkdir()
    cols = "frame_id,title,abstract,venue,year,type\n"
    (inp / "batch_001.csv").write_text(
        cols
        + 'F1,Hydrogen uptake at 77 K,"Uptake of 5 wt% at 77 K and 40 bar.",,2010,article\n'
        + "F2,DFT study of H2 on graphene,,,2012,article\n"
        + "F3,MOF-5 storage,,,2013,article\n"
        + "F4,Carbon review,,,2014,article\n"
    )
    hdr = "frame_id,decision,exclusion_code,stratum,evidence\n"
    (out / "batch_001.csv").write_text(
        hdr
        + 'F1,include,,S1,"uptake of 5 wt% at 77  K ... 40 bar"\n'
        + "F2,exclude,theoretical_only,,DFT study\n"
        + "F3,exclude,not_carbon,,\n"
        + "F4,exclude,not_primary,,a review of carbons\n"
    )
    rep = tmp_path / "r.json"
    assert sb.main(["join", "--inputs", str(inp), "--outputs", str(out),
                    "--out", str(tmp_path / "s.csv"), "--report", str(rep)]) == 0
    import json

    r = json.loads(rep.read_text())
    assert r["decisions"] == {"exclude": 3, "include": 1}
    assert r["strata"] == {"S1": 1}
    assert r["evidence_required"] == 4
    assert r["evidence_missing"] == ["F3"]
    assert r["evidence_not_in_record"] == ["F4"]
