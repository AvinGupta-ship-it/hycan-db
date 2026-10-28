"""Tests for the frame, draw-order and screening-audit scripts (protocol §6, §7)."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts" / "v1_search"
sys.path.insert(0, str(SCRIPTS))


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bf = load("build_frame")
do = load("draw_order")
sa = load("screening_audit")

MERGED_COLS = (
    "frame_id",
    "doi",
    "openalex_id",
    "s2_id",
    "title",
    "year",
    "venue",
    "abstract",
)
SCREEN_COLS = ("frame_id", "decision", "exclusion_code", "stratum", "evidence")


def write_csv(path: Path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bf.csv_bytes(tuple(cols), rows))


def setup(tmp_path, a_rows, b_rows, tiebreak=None, n=6):
    search, screen = tmp_path / "search", tmp_path / "screen"
    merged = [
        {
            "frame_id": f"F{i}",
            "doi": f"10.1/x{i}",
            "openalex_id": f"W{i}",
            "s2_id": "",
            "title": f"Paper {i}",
            "year": "2010",
            "venue": "J",
            "abstract": "a",
        }
        for i in range(1, n + 1)
    ]
    write_csv(search / "merged_records.csv", MERGED_COLS, merged)
    sha = hashlib.sha256((search / "merged_records.csv").read_bytes()).hexdigest()
    (search / "merge_counts.json").write_text(json.dumps({"merged_sha256": sha}))
    write_csv(screen / "screen_a.csv", SCREEN_COLS, a_rows)
    write_csv(screen / "screen_b.csv", SCREEN_COLS, b_rows)
    if tiebreak is not None:
        write_csv(screen / "stratum_tiebreak.csv", ("frame_id", "stratum"), tiebreak)
    return search, screen


def s(fid, decision, stratum="", code=""):
    if decision == "exclude" and not code:
        code = "not_carbon"
    return {
        "frame_id": fid,
        "decision": decision,
        "exclusion_code": code,
        "stratum": stratum,
        "evidence": "",
    }


A = [
    s("F1", "include", "S1"),
    s("F2", "exclude"),
    s("F3", "exclude"),
    s("F4", "uncertain", "S2"),
    s("F5", "include", "S1"),
    s("F6", "include", "S2"),
]
B = [
    s("F1", "include", "S1"),
    s("F2", "exclude"),
    s("F3", "include", "S2"),
    s("F4", "exclude"),
    s("F5", "include", "S2"),
    s("F6", "uncertain", "S2"),
]
TIE = [{"frame_id": "F5", "stratum": "S1"}]


def frame_rows(outputs):
    return list(
        csv.DictReader(io.StringIO(outputs["references/v1_search/frame.csv"].decode()))
    )


def test_frame_rules(tmp_path):
    out = bf.build(*setup(tmp_path, A, B, TIE))
    rows = {r["frame_id"]: r for r in frame_rows(out)}
    assert "F2" not in rows  # both excluded
    assert rows["F1"]["stratum"] == "S1" and rows["F1"]["stratum_source"] == "agreed"
    assert rows["F3"]["stratum"] == "S2" and rows["F3"]["stratum_source"] == "b"
    assert rows["F4"]["stratum"] == "S2" and rows["F4"]["stratum_source"] == "a"
    assert rows["F5"]["stratum"] == "S1" and rows["F5"]["stratum_source"] == "tiebreak"
    assert list(rows) == sorted(rows)
    de = out["references/v1_screening/double_excluded.csv"].decode().split()
    assert de == ["frame_id", "F2"]
    counts = json.loads(out["references/v1_search/frame_counts.json"])
    assert (counts["frame"], counts["frame_S1"], counts["frame_S2"]) == (5, 2, 3)
    assert (
        counts["frame_sha256"]
        == hashlib.sha256(out["references/v1_search/frame.csv"]).hexdigest()
    )


def test_frame_is_byte_reproducible(tmp_path):
    dirs = setup(tmp_path, A, B, TIE)
    assert bf.build(*dirs) == bf.build(*dirs)


def test_disagreeing_flags_without_tiebreak_refuse(tmp_path):
    with pytest.raises(bf.FrameError, match="tiebreak"):
        bf.build(*setup(tmp_path, A, B))


def test_unneeded_tiebreak_refuses(tmp_path):
    tie = TIE + [{"frame_id": "F1", "stratum": "S2"}]
    with pytest.raises(bf.FrameError, match="without a disagreement"):
        bf.build(*setup(tmp_path, A, B, tie))


@pytest.mark.parametrize(
    "bad",
    [
        s("F2", "exclude", code="no_surface_area"),  # full-text-only code (§4)
        s("F2", "maybe"),
        s("F2", "include"),  # no stratum
        s("F2", "exclude", stratum="S1"),
        {
            "frame_id": "F2",
            "decision": "include",
            "exclusion_code": "not_carbon",
            "stratum": "S1",
            "evidence": "",
        },
    ],
)
def test_invalid_screening_rows_refuse(tmp_path, bad):
    a = [bad if r["frame_id"] == "F2" else r for r in A]
    with pytest.raises(bf.FrameError):
        bf.build(*setup(tmp_path, a, B, TIE))


def test_every_merged_record_must_be_screened_once(tmp_path):
    with pytest.raises(bf.FrameError, match="unscreened"):
        bf.build(*setup(tmp_path, A[:-1], B, TIE))
    with pytest.raises(bf.FrameError, match="twice"):
        bf.build(*setup(tmp_path, A + A[:1], B, TIE))


def test_tampered_merge_refuses(tmp_path):
    search, screen = setup(tmp_path, A, B, TIE)
    (search / "merge_counts.json").write_text(json.dumps({"merged_sha256": "0" * 64}))
    with pytest.raises(bf.FrameError, match="does not match"):
        bf.build(search, screen)


def test_kappa():
    assert bf.cohen_kappa([True, False, True, False], [True, False, True, False]) == 1.0
    assert bf.cohen_kappa([True, True, False, False], [True, False, True, False]) == 0.0
    assert bf.cohen_kappa([True, True], [True, True]) is None


def test_draw_order_follows_section_7(tmp_path):
    frame = bf.build(*setup(tmp_path, A, B, TIE))["references/v1_search/frame.csv"]
    order = do.draw_order(frame)
    sha = hashlib.sha256(frame).hexdigest()
    s_val = int(sha[:16], 16)
    s1 = sorted(
        r["frame_id"]
        for r in frame_rows({"references/v1_search/frame.csv": frame})
        if r["stratum"] == "S1"
    )
    expected = [s1[i] for i in np.random.default_rng([s_val, 1]).permutation(len(s1))]
    assert [r["frame_id"] for r in order if r["stratum"] == "S1"] == expected
    assert [r["position"] for r in order if r["stratum"] == "S2"] == ["1", "2", "3"]
    assert do.draw_order(frame) == order


def test_draw_refuses_an_uncommitted_frame(tmp_path):
    import subprocess

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "f.csv").write_text("x\n")
    with pytest.raises(do.DrawError, match="not committed"):
        do.check_committed(tmp_path, "f.csv")
    env = {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
        "PATH": "/usr/bin:/bin",
    }
    subprocess.run(["git", "-C", str(tmp_path), "add", "f.csv"], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-qm", "f"], check=True, env=env
    )
    do.check_committed(tmp_path, "f.csv")
    (tmp_path / "f.csv").write_text("y\n")
    with pytest.raises(do.DrawError, match="differs"):
        do.check_committed(tmp_path, "f.csv")


def test_screening_audit_draw():
    ids = [f"F{i:04d}" for i in range(1, 251)]
    drawn = sa.draw(ids)
    assert len(drawn) == 100 and len(set(drawn)) == 100
    idx = np.random.default_rng(20261031).choice(250, size=100, replace=False)
    assert drawn == [ids[i] for i in idx]
    assert sorted(sa.draw(ids[:40])) == ids[:40]  # all of them, if fewer


def test_clopper_pearson_known_values():
    lo, hi = sa.clopper_pearson(0, 100)
    assert lo == 0.0 and hi == pytest.approx(0.0362, abs=1e-4)
    lo, hi = sa.clopper_pearson(5, 100)
    assert lo == pytest.approx(0.0164, abs=1e-4) and hi == pytest.approx(
        0.1128, abs=1e-4
    )


def test_screening_audit_score_requires_every_decision():
    rows = [{"author_decision": "include"}, {"author_decision": "exclude"}]
    assert sa.score(rows)["author_would_include"] == 1
    with pytest.raises(RuntimeError):
        sa.score(rows + [{"author_decision": ""}])
