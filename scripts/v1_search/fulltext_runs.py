"""Check every full-text eligibility agent after it has run (docs/v1_protocol.md
§6; §15 Amendment 1, items 3 and 26). The same checks as screening_runs.py,
for the two assessors and the resolver.

Run layout (fulltext.py prepare and resolver build the inputs):

    <run>/prompts/eligibility.md, eligibility_resolve.md   the frozen prompts
    <run>/<S>/<frame_id>/in/          the agent's input (S = A, B or R)
    <run>/<S>/<frame_id>/out/<frame_id>.json   its output
    <run>/<S>/<frame_id>/work/        its work directory
    <run>/launch/<S>_<frame_id>.txt   its filled launcher

For every finished agent described "Eligibility A|B <frame_id>" or
"Eligibility resolver <frame_id>", it checks that the first message is the
filled launcher, the prompt file is the frozen one, every turn was written by
the registered model, the access audit flags no call (or every flag has a
review that found no access, as in screening_runs.py), and the output is an
assessment in the prompt's format for that record. One report per agent goes
to <run>/access/<S>_<frame_id>.json.

    python3 scripts/v1_search/fulltext_runs.py --run DIR --transcripts DIR
        [--harness DIR ...] [--reviewed FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import fulltext
import screening_runs
import v1_audit_access

PROMPTS = {"A": "eligibility.md", "B": "eligibility.md", "R": "eligibility_resolve.md"}
SHA256 = {
    "eligibility.md": "e0e253900a4086ad004164bb7315e966c0dcb35403c8f1677c3f0217df156e75",
    "eligibility_resolve.md": "29649f4703d824828a0c3d56fb9b9e7ad9defb739aba4fc42a734b6b48d692ec",
}
MODELS = {"A": "claude-opus-5-5", "B": "claude-sonnet-5-5", "R": "claude-opus-5-5"}
TOOLS = screening_runs.TOOLS
DESCRIPTION = re.compile(r"^Eligibility (A|B|resolver) (F\d{5})$")


def agents(transcripts: Path) -> tuple[dict, dict]:
    found: dict[tuple[str, str], list[tuple[str, Path]]] = {}
    stopped: dict[tuple[str, str], list[str]] = {}
    for meta_path in sorted(transcripts.glob("*.meta.json")):
        meta = json.loads(meta_path.read_text())
        m = DESCRIPTION.match(meta.get("description", ""))
        if not m:
            continue
        key = ("R" if m.group(1) == "resolver" else m.group(1), m.group(2))
        t = meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))
        if meta.get("finished") and t.exists():
            found.setdefault(key, []).append((screening_runs.started(t), t))
        else:
            stopped.setdefault(key, []).append(t.name)
    return {k: [p for _, p in sorted(v)] for k, v in found.items()}, stopped


def check_agent(run: Path, role: str, fid: str, transcript: Path, harness: list[str]) -> dict:
    d = run / role / fid
    prompt = run / "prompts" / PROMPTS[role]
    launch = (run / "launch" / f"{role}_{fid}.txt").read_text(encoding="utf-8")
    report = {
        "screener": role, "batch": fid, "transcript": transcript.name,
        "launcher_exact": screening_runs.first_user_text(transcript) == launch.removesuffix("\n"),
        "prompt_sha256_ok": hashlib.sha256(prompt.read_bytes()).hexdigest() == SHA256[PROMPTS[role]],
        "models": v1_audit_access.models(transcript),
    }
    report["model_ok"] = report["models"] == [MODELS[role]]
    report["flags"] = v1_audit_access.audit(
        transcript, str(prompt), [str(d / "in"), str(d / "out"), str(d / "work")],
        TOOLS, harness, own=[str(d)])
    report["tool_calls"] = sum(1 for _ in v1_audit_access.tool_calls(transcript))
    problems = []
    try:
        fulltext.load_assessment(d / "out" / f"{fid}.json", fid)
    except (fulltext.WalkError, FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        problems.append(str(exc))
    report["output_problems"] = problems
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--harness", action="append", default=[])
    ap.add_argument("--reviewed")
    args = ap.parse_args(argv)
    run = Path(args.run)
    (run / "access").mkdir(exist_ok=True)
    reviews = screening_runs.load_reviews(args.reviewed)
    used: set = set()
    found, stopped = agents(Path(args.transcripts))
    bad = 0
    for (role, fid), transcripts in sorted(found.items()):
        report = check_agent(run, role, fid, transcripts[-1], args.harness)
        screening_runs.apply_reviews(report, reviews, used)
        report["earlier_agents"] = [t.name for t in transcripts[:-1]]
        report["unfinished_agents"] = stopped.get((role, fid), [])
        (run / "access" / f"{role}_{fid}.json").write_text(json.dumps(report, indent=2) + "\n")
        if not report["ok"]:
            bad += 1
            print(f"{role} {fid}: " + json.dumps(
                {k: report[k] for k in ("launcher_exact", "prompt_sha256_ok", "models",
                                        "flags", "output_problems")})[:600])
    stale = sorted(set(reviews) - used)
    for key in stale:
        print("review matches no flag: " + json.dumps(key))
    print(f"{len(found)} agents checked, {bad} not ok")
    return 1 if bad or stale else 0


if __name__ == "__main__":
    sys.exit(main())
