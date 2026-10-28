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
