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
summary to stdout. When a batch had more than one agent, the last one started
that finished is checked and stands; the report lists the earlier finished
agents and the agents that never finished (stopped by a technical failure; run
the script after every agent has stopped, so none is still running). A batch whose check 5 fails had a technical failure and may
be rerun under §9; a flag from check 4 is reviewed against the transcript and,
if the agent opened another agent's output, the batch is discarded and rerun
(Amendment 1, item 26). Either rerun is logged.

Reviews are kept in a JSON file (--reviewed), one entry per flag:

    {"reviews": [{"screener": "B", "batch": "batch_087",
                  "transcript": "agent-....jsonl", "call": 12,
                  "reason": "command names the home directory",
                  "access": false, "note": "what the call did"}]}

A flag with a review is kept in the report with its review attached. An agent
passes check 4 only if every flag has a review that found no access
("access": false). A review that matches no flag is an error, so the file
cannot hold stale entries.

    python3 scripts/v1_search/screening_runs.py --run DIR --transcripts DIR
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


REVIEW_KEYS = ("screener", "batch", "transcript", "call", "reason", "access", "note")


def load_reviews(path: str | None) -> dict[tuple, dict]:
    if not path:
        return {}
    out = {}
    for r in json.loads(Path(path).read_text(encoding="utf-8"))["reviews"]:
        if set(r) != set(REVIEW_KEYS) or not isinstance(r["access"], bool) or not r["note"]:
            raise ValueError(f"review entry needs exactly {REVIEW_KEYS}: {r}")
        key = (r["screener"], r["batch"], r["transcript"], r["call"], r["reason"])
        if key in out:
            raise ValueError(f"duplicate review: {key}")
        out[key] = r
    return out


def apply_reviews(report: dict, reviews: dict[tuple, dict], used: set) -> None:
    unreviewed = 0
    for f in report["flags"]:
        key = (report["screener"], report["batch"], report["transcript"], f["call"],
               f["reason"])
        if key in reviews:
            used.add(key)
            f["review"] = {"access": reviews[key]["access"], "note": reviews[key]["note"]}
        else:
            unreviewed += 1
    report["flags_unreviewed"] = unreviewed
    report["flags_access"] = sum(1 for f in report["flags"]
                                 if f.get("review", {}).get("access"))
    report["access_ok"] = unreviewed == 0 and report["flags_access"] == 0
    report["ok"] = (report["launcher_exact"] and report["prompt_sha256_ok"]
                    and report["model_ok"] and report["access_ok"]
                    and not report["output_problems"])


def unfinished(transcripts: Path) -> dict[tuple[str, str], list[str]]:
    """Screening agents that never finished (stopped by a technical failure,
    or still running), by (screener, batch)."""
    out: dict[tuple[str, str], list[str]] = {}
    for meta_path in sorted(transcripts.glob("*.meta.json")):
        meta = json.loads(meta_path.read_text())
        m = DESCRIPTION.match(meta.get("description", ""))
        if m and not meta.get("finished"):
            out.setdefault((m.group(1), "batch_" + m.group(2)), []).append(
                meta_path.name.replace(".meta.json", ".jsonl"))
    return out


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
        TOOLS, harness, own=[str(agent_dir)],
    )
    report["tool_calls"] = sum(1 for _ in v1_audit_access.tool_calls(transcript))
    report["output_problems"] = screening_batches.check_batch(
        run / "batches" / f"{batch}.csv", agent_dir / "out" / f"{batch}.csv"
    )
    apply_reviews(report, {}, set())
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
    reviews = load_reviews(args.reviewed)
    used: set = set()
    found = agents(Path(args.transcripts))
    stopped = unfinished(Path(args.transcripts))
    bad = 0
    for (screener, batch), transcripts in sorted(found.items()):
        # The last agent started for a batch is the one whose output stands;
        # earlier ones are reported as reruns.
        report = check_agent(run, screener, batch, transcripts[-1], args.harness)
        apply_reviews(report, reviews, used)
        report["earlier_agents"] = [t.name for t in transcripts[:-1]]
        report["unfinished_agents"] = stopped.get((screener, batch), [])
        (run / "access" / f"{screener}_{batch}.json").write_text(
            json.dumps(report, indent=2) + "\n"
        )
        if not report["ok"]:
            bad += 1
            print(f"{screener} {batch}: " + json.dumps(
                {k: report[k] for k in ("launcher_exact", "prompt_sha256_ok", "models",
                                        "flags", "output_problems")})[:600])
    for key in sorted(set(stopped) - set(found)):
        print(f"{key[0]} {key[1]}: no finished agent; unfinished {stopped[key]}")
    stale = sorted(set(reviews) - used)
    for key in stale:
        print("review matches no flag: " + json.dumps(key))
    reviewed = sum(1 for k in used if not reviews[k]["access"])
    print(f"{len(found)} agents checked, {bad} not ok; "
          f"{reviewed} flags reviewed as no access")
    return 1 if bad or stale else 0


if __name__ == "__main__":
    sys.exit(main())
