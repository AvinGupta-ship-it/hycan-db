"""Tests for scripts/v1_search/extraction.py and extraction_runs.py (protocol §9)."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "v1_search"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / "v1_search" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ex = _load("extraction")
runs = _load("extraction_runs")


def test_frozen_hashes_are_amendment_1s_and_the_built_prompts():
    protocol = (REPO_ROOT / "docs" / "v1_protocol.md").read_text(encoding="utf-8")
    for name, digest in ex.SHA256.items():
        assert f"`prompts/v1/built/{name}` | `{digest}`" in protocol
        assert hashlib.sha256((ex.BUILT / name).read_bytes()).hexdigest() == digest
    assert ex.TOOLS_MANIFEST_SHA256 in protocol


def test_models_are_amendment_1s():
    protocol = (REPO_ROOT / "docs" / "v1_protocol.md").read_text(encoding="utf-8")
    for role, prompt, model in (("A", "extract_A.md", ex.MODEL["A"]),
                                ("B", "extract_B.md", ex.MODEL["B"]),
                                ("C", "reconcile.md", ex.MODEL["C"]),
                                ("C", "reconcile_legacy.md", ex.MODEL["C"]),
                                ("L", "legacy_labels.md", ex.MODEL["L"])):
        assert re.search(rf"\| `{re.escape(prompt)}` \| `{re.escape(model)}` \|", protocol), role


def test_reconciler_prompt_depends_on_mode():
    assert runs.prompt_name("C", "dual") == "reconcile.md"
    assert runs.prompt_name("C", "legacy") == "reconcile_legacy.md"
    assert runs.prompt_name("B", "legacy") == "extract_B.md"
    assert runs.prompt_name("L", "legacy") == "legacy_labels.md"


def test_committed_plan_is_reproduced():
    if not ex.PAPERS.exists():
        pytest.skip("no committed plan")
    rows = ex.plan_rows()
    committed = ex.read(ex.PAPERS)
    assert committed == [{k: str(r[k]) for k in ex.COLUMNS} for r in rows]


def test_plan_routes_and_ids():
    if not ex.PAPERS.exists():
        pytest.skip("no committed plan")
    rows = ex.read(ex.PAPERS)
    assert len({r["paper_id"] for r in rows}) == len(rows)
    assert len({r["frame_id"] for r in rows}) == len(rows)
    new = [r for r in rows if r["v01_paper"] == "false"]
    # New papers take consecutive IDs after the v0.1 papers, in stratum then draw order.
    ids = [int(r["paper_id"][4:]) for r in new]
    assert ids == list(range(66, 66 + len(new)))
    order = [(r["stratum"], int(r["position"])) for r in new]
    assert order == sorted(order)
    for r in rows:
        assert (r["mode"] == "dual") == (r["selection_route"] in ("S1", "S2"))
        assert (r["mode"] == "none") == (r["selection_route"] == "legacy_v0.1_not_retrieved")
        assert r["first_author"] and r["journal"] and r["year"]


def test_tools_directory_check_finds_a_stray_file(tmp_path):
    tools = tmp_path / "tools"
    (tools / "scripts").mkdir(parents=True)
    (tools / "scripts" / "a.py").write_text("x = 1\n")
    digest = hashlib.sha256(b"x = 1\n").hexdigest()
    (tools / "MANIFEST").write_text(f"{digest}  scripts/a.py\n")
    ex.TOOLS_MANIFEST_SHA256, saved = hashlib.sha256((tools / "MANIFEST").read_bytes()).hexdigest(), ex.TOOLS_MANIFEST_SHA256
    try:
        assert runs.tools_problems(tools) == []
        (tools / "dz").mkdir()
        (tools / "dz" / "t.json").write_text("{}")
        assert runs.tools_problems(tools) == ["files in the tools directory not in its MANIFEST: ['dz/t.json']"]
        (tools / "src" / "__pycache__").mkdir(parents=True)
        (tools / "src" / "__pycache__" / "m.pyc").write_bytes(b"")
        (tools / "dz" / "t.json").unlink()
        assert runs.tools_problems(tools) == []
        (tools / "scripts" / "a.py").write_text("x = 2\n")
        assert runs.tools_problems(tools) == ["tools file changed or missing: scripts/a.py"]
    finally:
        ex.TOOLS_MANIFEST_SHA256 = saved


def _transcript(tmp_path, calls):
    import json as _json
    lines = [_json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": name, "input": inp}]}}) for name, inp in calls]
    p = tmp_path / "agent.jsonl"
    p.write_text("\n".join(lines) + "\n")
    return p


def test_supplementary_flags_see_script_source_reads_and_device_files(tmp_path):
    tools = "/w/tools"
    t = _transcript(tmp_path, [
        ("Bash", {"command": f"cd {tools} && python3 scripts/digitize_figure.py extract --image /w/in/p.png | head -5"}),
        ("Bash", {"command": f"cd {tools} && sed -n 1,60p scripts/digitize_figure.py | head -0"}),
        ("Bash", {"command": f"grep -n 'Pressure out of range' -r {tools}/scripts/validate_row_detail.py"}),
        ("Bash", {"command": "python3 - <<'EOF'\nprint(open('scripts/validate_row_detail.py').read())\nEOF"}),
        ("Bash", {"command": "ls -la /dev/null.png; python3 x.py > /dev/null 2>&1"}),
        ("Read", {"file_path": f"{tools}/scripts/digitize_figure.py"}),
        ("Bash", {"command": "cat > /w/work/run.sh <<'EOF'\ncat scripts/digitize_figure.py\nEOF\nbash /w/work/run.sh"}),
    ])
    calls = sorted({f["call"] for f in runs.supplementary_flags(t, tools)})
    # 1 runs the script and filters its output; 7's heredoc is file content
    # (running the written script is the audit's business, not this check's).
    assert calls == [2, 3, 4, 5, 6]


def test_supplementary_flags_ignore_prose_naming_the_script(tmp_path):
    t = _transcript(tmp_path, [
        ("Bash", {"command": "cat > /w/work/a.py <<'EOF'\n'''values come from digitize_figure.py'''\nEOF\npython3 /w/work/a.py"}),
        ("Bash", {"command": "python3 - <<'EOF'\nimport sys\nfrom digitize_figure import main\nEOF"}),
    ])
    assert sorted({f["call"] for f in runs.supplementary_flags(t, "/w/tools")}) == [2]


def test_supplementary_flags_see_relative_reads_inside_the_tools_directory(tmp_path):
    t = _transcript(tmp_path, [
        ("Bash", {"command": "cd /w/tools && ls"}),
        ("Bash", {"command": "cd /w/tools && ls scripts/"}),
        ("Bash", {"command": "cd /w/tools && python3 scripts/validate_row_detail.py /w/out/rows.csv | head -40"}),
        ("Bash", {"command": "cd /w/tools && ls -la $OUT && head -n 5 /w/out/rows.csv"}),
        ("Bash", {"command": "cd /w/tools && cat MANIFEST"}),
    ])
    assert sorted({f["call"] for f in runs.supplementary_flags(t, "/w/tools")}) == [1, 2, 5]


def test_supplementary_flags_skip_redirection_targets(tmp_path):
    t = _transcript(tmp_path, [("Bash", {"command": "cd /w/tools && cat > $W/run_a.sh <<'EOF'\nx\nEOF\nbash $W/run_a.sh"})])
    assert runs.supplementary_flags(t, "/w/tools") == []


def test_cross_access_lists_other_agents_and_the_repository(tmp_path):
    run = Path("/home/claude/work/runs/extract")
    t = _transcript(tmp_path, [
        ("Read", {"file_path": f"{run}/A/HYC-0001/out/rows.csv"}),
        ("Read", {"file_path": f"{run}/B/HYC-0001/out/rows.csv"}),
        ("Bash", {"command": "cat /home/claude/work/hycan-db/data/raw/measurements_v0.1.csv"}),
        ("Bash", {"command": "ls /home/claude/work/runs/screen"}),
    ])
    hits = runs.cross_access(t, run, "A", "HYC-0001")
    assert [h.split(":")[0] for h in hits] == ["call 2 Read", "call 3 Bash", "call 3 Bash", "call 4 Bash"]
