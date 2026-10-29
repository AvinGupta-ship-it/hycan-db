"""Tests for scripts/v1_audit_access.py: the transcript audit flags paths an
agent may not open and passes the calls the launcher allows."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "v1_audit_access", REPO_ROOT / "scripts" / "v1_audit_access.py"
)
aa = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = aa
spec.loader.exec_module(aa)

INS, IN, OUT, WORK, TOOLS = "/w/p/extract_B.md", "/w/in_B/P1", "/w/out_B/P1", "/w/work_B/P1", "/w/tools"


def transcript(tmp_path, calls):
    lines = [
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": n, "input": i}]}})
        for n, i in calls
    ]
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(lines) + "\n")
    return p


def run(tmp_path, calls):
    return aa.audit(transcript(tmp_path, calls), INS, [IN, OUT, WORK], TOOLS, [])


def test_allowed_calls_pass(tmp_path):
    assert run(tmp_path, [
        ("Read", {"file_path": INS}),
        ("Read", {"file_path": IN + "/pages/P1-1.png"}),
        ("Write", {"file_path": OUT + "/rows.csv", "content": ""}),
        ("Bash", {"command": f"cd {WORK} && python3 -c \"import numpy as np; x/w.sum()\""}),
        ("Bash", {"command": f"cd {TOOLS} && python3 scripts/digitize_figure.py extract "
                             f"--image {IN}/pages/P1-7.png --out {WORK}/a.json | "
                             "grep -E \"points extracted|status\""}),
        ("Bash", {"command": f"cd {TOOLS} && python3 scripts/validate_row_detail.py "
                             f"{OUT}/rows.csv --errors-only 2>&1 | head -40"}),
    ]) == []


def test_reading_other_outputs_or_v01_rows_is_flagged(tmp_path):
    flags = run(tmp_path, [
        ("Read", {"file_path": "/w/out_A/P1/rows.csv"}),
        ("Bash", {"command": "head -3 /home/x/hycan-db/data/raw/measurements_v0.1.csv"}),
        ("Glob", {"pattern": "**/*.csv"}),
        ("Bash", {"command": f"cd {WORK} && cat ../../out_A/P1/rows.csv"}),
    ])
    reasons = [f["reason"] for f in flags]
    assert len([r for r in reasons if "outside" in r]) == 3
    assert any("climbs" in r for r in reasons)


def test_looking_inside_the_tools_directory_is_flagged(tmp_path):
    flags = run(tmp_path, [
        ("Bash", {"command": f"ls {TOOLS}/src/hycan"}),
        ("Bash", {"command": f"cd {TOOLS} && ls"}),
        ("Bash", {"command": f"cd {TOOLS} && cat scripts/validate_row_detail.py"}),
        ("Read", {"file_path": TOOLS + "/src/hycan/schema.py"}),
    ])
    assert len(flags) == 4


def test_adversarial_cases_are_flagged(tmp_path):
    cases = [
        ("Read", {"file_path": WORK + "/../../out_A/P1/rows.csv"}),
        ("Bash", {"command": f"cat {WORK}/../../out_A/P1/rows.csv"}),
        ("Bash", {"command": f"cd {WORK} && cd .. && cd .. && ls"}),
        ("Bash", {"command": f"cd {WORK} && python3 -c \"import os; print(os.listdir('..'))\""}),
        ("Glob", {"pattern": "../../out_A/**", "path": WORK}),
        ("Bash", {"command": "cat ~/work/hycan-db/data/raw/measurements_v0.1.csv"}),
        ("Bash", {"command": "cat $HOME/work/hycan-db/data/raw/measurements_v0.1.csv"}),
        ("Bash", {"command": f"ls {TOOLS}"}),
        ("Bash", {"command": f"find {TOOLS}"}),
        ("Bash", {"command": f"cd {TOOLS} && python3 -c \"open('src/hycan/schema.py')\""}),
        ("Bash", {"command": f"cd {TOOLS} && grep -rn uptake"}),
        ("Bash", {"command": f"cd {TOOLS} && cd scripts && cat x.py"}),
        ("Bash", {"command": f"cd {TOOLS} && cp -r src {WORK}"}),
        ("Bash", {"command": f"cd {TOOLS} && python3 - <<'EOF'\nprint(open('MANIFEST').read())\nEOF"}),
        ("Bash", {"command": "curl https://example.org"}),
        ("Bash", {"command": "cat /Users/someone/Downloads/paper.pdf"}),
        ("Write", {"file_path": IN + "/x.csv", "content": ""}),
        ("MultiEdit", {"file_path": OUT + "/rows.csv"}),
        ("WebFetch", {"url": "https://example.org"}),
    ]
    for call in cases:
        assert run(tmp_path, [call]), call


def test_the_report_names_the_models_that_wrote_the_turns(tmp_path):
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join([
        json.dumps({"type": "user", "message": {"content": "go"}}),
        json.dumps({"type": "assistant", "message": {"model": "claude-sonnet-5-5",
                                                     "content": []}}),
        json.dumps({"type": "assistant", "message": {"model": "claude-sonnet-5-5",
                                                     "content": []}}),
    ]) + "\n")
    out = tmp_path / "r.json"
    aa.main([str(p), "--instruction", INS, "--input", IN, "--output", OUT,
             "--work", WORK, "--tools", TOOLS, "--json", str(out)])
    assert json.loads(out.read_text())["models"] == ["claude-sonnet-5-5"]


def test_grep_pattern_is_not_read_as_a_file_in_the_tools_directory(tmp_path):
    cmd = (f"cd {TOOLS} && grep -c -E 'None|NA$|null' {OUT}/x.csv && "
           f"sed -n 1,5p {OUT}/x.csv")
    assert run(tmp_path, [("Bash", {"command": cmd})]) == []
    bad = f"cd {TOOLS} && grep -c 'x' scripts/hycan/schema.py"
    assert run(tmp_path, [("Bash", {"command": bad})])


def test_the_agents_own_directory_may_be_listed_but_not_written(tmp_path):
    own = "/w/runs/A/batch_001"
    calls = [("Bash", {"command": f"cd {own} && ls -la in out work"}),
             ("Read", {"file_path": own + "/in/batch_001.csv"}),
             ("Write", {"file_path": own + "/note.txt", "content": "x"})]
    flags = aa.audit(transcript(tmp_path, calls), INS,
                     [own + "/in/batch_001.csv", own + "/out/batch_001.csv", own + "/work"],
                     TOOLS, [], own=[own])
    assert [f["call"] for f in flags] == [3]
    flags = aa.audit(transcript(tmp_path, calls[:1]), INS,
                     [own + "/in/batch_001.csv", own + "/out/batch_001.csv", own + "/work"],
                     TOOLS, [])
    assert flags  # without `own`, the agent directory is outside the allowed paths


def test_climbs_resolved_against_an_absolute_cd(tmp_path):
    ok = f"cd {WORK} && head -5 ../../out_B/P1/x.csv && python3 -c \"open('../P1/s.py')\""
    assert run(tmp_path, [("Bash", {"command": ok})]) == []
    breach = f"cd {WORK} && cat ../../out_A/P1/x.csv"
    assert run(tmp_path, [("Bash", {"command": breach})])
    unanchored = "cat ../out/x.csv"
    assert run(tmp_path, [("Bash", {"command": unanchored})])


def test_numeric_root_is_not_a_path_and_a_misnamed_write_key_is_checked(tmp_path):
    sed = f"cd {WORK} && sed -i \"s/^21: ('exclude','a'/21: ('exclude','b'/\" d.py"
    assert run(tmp_path, [("Bash", {"command": sed})]) == []
    assert run(tmp_path, [("Write", {"path": WORK + "/m.py", "content": "x"})]) == []
    assert run(tmp_path, [("Write", {"path": "/w/out_A/P1/m.py", "content": "x"})])


def test_a_sed_address_is_not_a_path_but_a_sed_file_operand_is(tmp_path):
    ok = f"cd {WORK} && sed -n '/F04466/,/F04476/p' make_out.py | cut -c1-120"
    assert run(tmp_path, [("Bash", {"command": ok})]) == []
    bad = f"cd {WORK} && sed -n '/F1/p' /w/out_A/P1/x.csv"
    assert run(tmp_path, [("Bash", {"command": bad})])


def test_only_the_agents_own_saved_output_counts_in_the_harness_directory(tmp_path):
    H = "/h/tool-results"
    lines = [
        json.dumps({"type": "user", "message": {"content": [{"type": "tool_result",
            "content": f"<persisted-output>\nOutput too large (40KB). Full output saved to: {H}/mine.txt\n"}]}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read", "input": {"file_path": f"{H}/mine.txt"}}]}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read", "input": {"file_path": f"{H}/other_agent.txt"}}]}}),
    ]
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(lines) + "\n")
    flags = aa.audit(p, INS, [IN, OUT, WORK], TOOLS, [H])
    assert [f["call"] for f in flags] == [2]


def test_single_component_text_is_not_a_path_but_a_root_directory_is(tmp_path):
    text = (f"cat > {WORK}/d.py <<'EOF'\nD = ['H2/He mixture', 'Pd /NHMCS-900', 'W /W ratio']\nEOF")
    assert run(tmp_path, [("Bash", {"command": text})]) == []
    for bad in ("ls /tmp", "cat /home/claude/x", "ls /root"):
        assert run(tmp_path, [("Bash", {"command": bad})]), bad


def test_subagent_handback_is_harmless(tmp_path):
    t = tmp_path / "t.jsonl"
    t.write_text(json.dumps({"type": "assistant", "message": {"model": "m", "content": [
        {"type": "tool_use", "name": "SubagentHandback", "input": {"message": "eligible"}}]}}) + "\n")
    assert aa.audit(t, "/run/prompt.md", ["/run/A/x/in", "/run/A/x/out", "/run/A/x/work"], "/tools", []) == []
