"""Check every title-and-abstract screening agent after it has run
(docs/v1_protocol.md §6; §15 Amendment 1, items 3 and 26).

Each batch is screened by one agent per screener, started with the frozen
launcher (prompts/v1/built/launcher.md) filled with that agent's paths:

    <run>/prompts/screen.md                 the frozen screening prompt
    <run>/batches/batch_NNN.csv             the batch (screening_batches.py split)
    <run>/<S>/batch_NNN/in/batch_NNN.csv    the agent's copy of the batch
    <run>/<S>/batch_NNN/out/batch_NNN.csv   its output
    <run>/<S>/batch_NNN/work/               its work directory
    <run>/launch/<S>_batch_NNN.txt          its filled launcher

For every finished agent whose description is "Screener <S> batch NNN", this
script checks that

  1. the agent's first message is the filled launcher, byte for byte apart
     from the file's final newline, which the agent harness does not pass;
  2. the prompt file is the frozen screen.md (its SHA-256 in Amendment 1);
  3. the agent's turns were written by the model registered for that screener;
  4. the access audit (scripts/v1_audit_access.py) flags no call;
  5. the output screens exactly its input batch (screening_batches.check_batch);

and writes one report per agent to <run>/access/<S>_batch_NNN.json and a
summary to stdout. A batch whose check 5 fails had a technical failure and may
be rerun under §9; a flag from check 4 is reviewed against the transcript and,
if the agent opened another agent's output, the batch is discarded and rerun
(Amendment 1, item 26). Either rerun is logged.

    python3 scripts/v1_search/screening_runs.py --run DIR --transcripts DIR
        [--harness DIR ...]
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
import screening_batches
import v1_audit_access

SCREEN_SHA256 = "41291c79e05592e7c7d36ebc2ef9bb8d9c1a683cffa01d5521d41e0020b971db"
MODELS = {"A": "claude-opus-5-5", "B": "claude-sonnet-5-5"}
TOOLS = "/home/claude/work/v1_tools_frozen"
DESCRIPTION = re.compile(r"^Screener ([AB]) batch[ _](\d{3})$")


def first_user_text(transcript: Path) -> str | None:
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") != "user":
            continue
        content = d.get("message", {}).get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "".join(p.get("text", "") for p in content if p.get("type") == "text")
    return None


def started(transcript: Path) -> str:
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            return json.loads(line).get("timestamp") or ""
        except json.JSONDecodeError:
            continue
    return ""


def agents(transcripts: Path) -> dict[tuple[str, str], list[Path]]:
    """Every finished screening agent's transcript, by (screener, batch), in the
    order the agents were started."""
    found: dict[tuple[str, str], list[tuple[str, Path]]] = {}
    for meta_path in transcripts.glob("*.meta.json"):
        meta = json.loads(meta_path.read_text())
        m = DESCRIPTION.match(meta.get("description", ""))
        if not m or not meta.get("finished"):
            continue
        t = meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))
        if t.exists():
            found.setdefault((m.group(1), "batch_" + m.group(2)), []).append(
                (started(t), t)
            )
    return {k: [p for _, p in sorted(v)] for k, v in found.items()}


def check_agent(run: Path, screener: str, batch: str, transcript: Path,
                harness: list[str]) -> dict:
    agent_dir = run / screener / batch
    launch = (run / "launch" / f"{screener}_{batch}.txt").read_text(encoding="utf-8")
    prompt = run / "prompts" / "screen.md"
    report = {
        "screener": screener,
        "batch": batch,
        "transcript": transcript.name,
        "launcher_exact": first_user_text(transcript) == launch.removesuffix("\n"),
        "prompt_sha256_ok": hashlib.sha256(prompt.read_bytes()).hexdigest() == SCREEN_SHA256,
    }
    report["models"] = v1_audit_access.models(transcript)
    report["model_ok"] = report["models"] == [MODELS[screener]]
    report["flags"] = v1_audit_access.audit(
        transcript, str(prompt),
        [str(agent_dir / "in"), str(agent_dir / "out"), str(agent_dir / "work")],
        TOOLS, harness,
    )
    report["tool_calls"] = sum(1 for _ in v1_audit_access.tool_calls(transcript))
    report["output_problems"] = screening_batches.check_batch(
        run / "batches" / f"{batch}.csv", agent_dir / "out" / f"{batch}.csv"
    )
    report["ok"] = (report["launcher_exact"] and report["prompt_sha256_ok"]
                    and report["model_ok"] and not report["flags"]
                    and not report["output_problems"])
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--harness", action="append", default=[])
    args = ap.parse_args(argv)
    run = Path(args.run)
    (run / "access").mkdir(exist_ok=True)
    found = agents(Path(args.transcripts))
    bad = 0
    for (screener, batch), transcripts in sorted(found.items()):
        # The last agent started for a batch is the one whose output stands;
        # earlier ones are reported as reruns.
        report = check_agent(run, screener, batch, transcripts[-1], args.harness)
        report["earlier_agents"] = [t.name for t in transcripts[:-1]]
        (run / "access" / f"{screener}_{batch}.json").write_text(
            json.dumps(report, indent=2) + "\n"
        )
        if not report["ok"]:
            bad += 1
            print(f"{screener} {batch}: " + json.dumps(
                {k: report[k] for k in ("launcher_exact", "prompt_sha256_ok", "models",
                                        "flags", "output_problems")})[:600])
    print(f"{len(found)} agents checked, {bad} not ok")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
