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
