"""Tests for scripts/v1_search/screening_runs.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "screening_runs", REPO_ROOT / "scripts" / "v1_search" / "screening_runs.py"
)
sr = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sr
spec.loader.exec_module(sr)

HDR_IN = "frame_id,title,abstract,venue,year,type\n"
HDR_OUT = "frame_id,decision,exclusion_code,stratum,evidence\n"


def setup_run(tmp_path, monkeypatch):
    run = tmp_path / "run"
    (run / "prompts").mkdir(parents=True)
    (run / "prompts" / "screen.md").write_text("frozen prompt")
    monkeypatch.setattr(sr, "SCREEN_SHA256",
                        __import__("hashlib").sha256(b"frozen prompt").hexdigest())
    (run / "batches").mkdir()
    (run / "batches" / "batch_001.csv").write_text(HDR_IN + "F1,t,,,2010,article\n")
    (run / "launch").mkdir()
    d = run / "A" / "batch_001"
    for sub in ("in", "out", "work"):
        (d / sub).mkdir(parents=True)
    (d / "in" / "batch_001.csv").write_text(HDR_IN + "F1,t,,,2010,article\n")
    (d / "out" / "batch_001.csv").write_text(HDR_OUT + "F1,uncertain,,S2,\n")
    launch = f"Read {run}/prompts/screen.md ... Input: {d}/in/batch_001.csv"
    (run / "launch" / "A_batch_001.txt").write_text(launch + "\n")
    return run, d, launch


def transcript(tdir, name, description, first, calls, model, finished=True):
    tdir.mkdir(exist_ok=True)
    lines = [json.dumps({"type": "user", "timestamp": "2026-10-28T20:00:00Z",
                         "message": {"role": "user", "content": first}})]
    lines += [json.dumps({"type": "assistant", "message": {"model": model, "content": [
        {"type": "tool_use", "name": n, "input": i}]}}) for n, i in calls]
    (tdir / f"{name}.jsonl").write_text("\n".join(lines) + "\n")
    (tdir / f"{name}.meta.json").write_text(json.dumps(
        {"description": description, "finished": finished}))


def test_a_clean_agent_passes_and_each_failure_is_reported(tmp_path, monkeypatch):
    run, d, launch = setup_run(tmp_path, monkeypatch)
    tdir = tmp_path / "t"
    calls = [("Read", {"file_path": str(run / "prompts" / "screen.md")}),
             ("Read", {"file_path": str(d / "in" / "batch_001.csv")}),
             ("Write", {"file_path": str(d / "work" / "s.py"), "content": "x"})]
    transcript(tdir, "agent-1", "Screener A batch 001", launch, calls, "claude-opus-5-5")
    transcript(tdir, "agent-2", "Screener B batch_001", "x", [], "claude-sonnet-5-5",
               finished=False)  # unfinished: not checked yet
    assert sr.main(["--run", str(run), "--transcripts", str(tdir)]) == 0
    rep = json.loads((run / "access" / "A_batch_001.json").read_text())
    assert rep["ok"] and rep["models"] == ["claude-opus-5-5"]

    # wrong model, a launcher that differs, and a read of another agent's output
    calls.append(("Read", {"file_path": str(run / "B" / "batch_001" / "out" / "batch_001.csv")}))
    transcript(tdir, "agent-1", "Screener A batch_001", launch + " ", calls,
               "claude-sonnet-5-5")
    assert sr.main(["--run", str(run), "--transcripts", str(tdir)]) == 1
    rep = json.loads((run / "access" / "A_batch_001.json").read_text())
    assert not rep["launcher_exact"] and not rep["model_ok"] and rep["flags"]


def test_a_reviewed_flag_passes_only_with_no_access_and_stale_reviews_fail(tmp_path, monkeypatch):
    run, d, launch = setup_run(tmp_path, monkeypatch)
    tdir = tmp_path / "t"
    calls = [("Read", {"file_path": str(run / "prompts" / "screen.md")}),
             ("Bash", {"command": f"cd {d} && python3 -I -c \"print('~', 1)\""})]
    transcript(tdir, "agent-1", "Screener A batch 001", launch, calls, "claude-opus-5-5")
    args = ["--run", str(run), "--transcripts", str(tdir)]
    assert sr.main(args) == 1
    rep = json.loads((run / "access" / "A_batch_001.json").read_text())
    flag = rep["flags"][0]
    assert flag["reason"] == "command names the home directory" and rep["flags_unreviewed"] == 1

    def review(access, call=flag["call"]):
        p = tmp_path / "reviews.json"
        p.write_text(json.dumps({"reviews": [{
            "screener": "A", "batch": "batch_001", "transcript": "agent-1.jsonl",
            "call": call, "reason": flag["reason"], "access": access,
            "note": "the ~ is text printed by python"}]}))
        return args + ["--reviewed", str(p)]

    assert sr.main(review(False)) == 0
    rep = json.loads((run / "access" / "A_batch_001.json").read_text())
    assert rep["ok"] and rep["flags"][0]["review"]["access"] is False
    assert sr.main(review(True)) == 1          # a reviewed access still fails
    assert sr.main(review(False, call=99)) == 1  # a review matching no flag fails


def test_unfinished_agents_are_listed_with_the_agent_that_stands(tmp_path, monkeypatch):
    run, d, launch = setup_run(tmp_path, monkeypatch)
    tdir = tmp_path / "t"
    calls = [("Read", {"file_path": str(run / "prompts" / "screen.md")})]
    transcript(tdir, "agent-0", "Screener A batch 001", launch, [], "claude-opus-5-5",
               finished=False)  # stopped by a technical failure
    transcript(tdir, "agent-1", "Screener A batch 001", launch, calls, "claude-opus-5-5")
    assert sr.main(["--run", str(run), "--transcripts", str(tdir)]) == 0
    rep = json.loads((run / "access" / "A_batch_001.json").read_text())
    assert rep["transcript"] == "agent-1.jsonl"
    assert rep["unfinished_agents"] == ["agent-0.jsonl"] and rep["earlier_agents"] == []
