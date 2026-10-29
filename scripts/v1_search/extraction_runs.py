"""Check every extraction agent after it has run (docs/v1_protocol.md §9; §15
Amendment 1, items 22 to 26). The same checks as fulltext_runs.py, for the
extraction roles: extractors A and B, the v0.1 sample labeller L and the
reconciler C (reconcile.md for a sampled paper, reconcile_legacy.md for a v0.1
paper outside the sample).

Run layout: scripts/v1_search/extraction.py. For every finished agent described
"Extraction <R> <paper_id>" (R = A, B, C or L), it checks that the first message
is the filled launcher, the prompt file is the frozen one, every turn was
written by the registered model, the access audit flags no call (or every flag
has a review that found no access), and the output is complete:

  A, B  rows.csv with the column list's header, rows of this paper only, and
        no validator error; log.md present
  L     labels.csv with its header, covering every v0.1 sample_id
  C     rows.csv as above, resolutions.csv with its header, and
        scripts/v1_extract.py check passing (every non-agree match line
        resolved, every computed W1 equal to code's, no isotherm mixing bases)

One report per agent goes to <run>/access/<R>_<paper_id>.json.

    python3 scripts/v1_search/extraction_runs.py --run DIR --transcripts DIR
        [--harness DIR ...] [--reviewed FILE]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import extraction
import screening_runs
import v1_audit_access

ROOT = HERE.parents[1]
DESCRIPTION = re.compile(r"^Extraction (A|B|C|L) (HYC-\d{4})$")
COLUMNS = (ROOT / "data" / "raw" / "measurements_v0.1.csv").read_text(encoding="utf-8").splitlines()[0]
LABELS_HEADER = "sample_id,measurement_ids,label,evidence"
RESOLUTIONS_HEADER = "match_line,field,first_value,second_value,decision,final_value,evidence,location"


def prompt_name(role: str, mode: str) -> str:
    return extraction.PROMPT["C_legacy" if role == "C" and mode == "legacy" else role]


def agents(transcripts: Path) -> tuple[dict, dict]:
    found: dict[tuple[str, str], list[tuple[str, Path]]] = {}
    stopped: dict[tuple[str, str], list[str]] = {}
    for meta_path in sorted(transcripts.glob("*.meta.json")):
        meta = json.loads(meta_path.read_text())
        m = DESCRIPTION.match(meta.get("description", ""))
        if not m:
            continue
        key = (m.group(1), m.group(2))
        t = meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))
        if meta.get("finished") and t.exists():
            found.setdefault(key, []).append((screening_runs.started(t), t))
        else:
            stopped.setdefault(key, []).append(t.name)
    return {k: [p for _, p in sorted(v)] for k, v in found.items()}, stopped


def first_line(path: Path) -> str:
    with path.open(encoding="utf-8") as f:
        return f.readline().rstrip("\n")


def rows_problems(path: Path, pid: str) -> list[str]:
    if not path.exists():
        return [f"{path.name} missing"]
    problems = []
    if first_line(path) != COLUMNS:
        problems.append(f"{path.name}: header differs from the column list")
    with path.open(encoding="utf-8", newline="") as f:
        others = {r.get("paper_id") for r in csv.DictReader(f)} - {pid}
    if others:
        problems.append(f"{path.name}: rows of other papers {sorted(map(str, others))}")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_row_detail.py"), str(path),
                        "--errors-only", "--limit", "5"],
                       capture_output=True, text=True, cwd=ROOT, check=False)
    if r.returncode:
        problems.append(f"{path.name}: validator errors: " + r.stdout.strip()[-400:])
    return problems


def output_problems(run: Path, role: str, pid: str, mode: str) -> list[str]:
    out = run / role / pid / "out"
    if role in ("A", "B"):
        problems = rows_problems(out / "rows.csv", pid)
        if not (out / "log.md").exists():
            problems.append("log.md missing")
        return problems
    if role == "L":
        f = out / "labels.csv"
        if not f.exists():
            return ["labels.csv missing"]
        problems = [] if first_line(f) == LABELS_HEADER else ["labels.csv: header differs"]
        with f.open(encoding="utf-8", newline="") as h:
            labelled = {r["sample_id"] for r in csv.DictReader(h)}
        with (run / "V" / pid / "rows" / "rows.csv").open(encoding="utf-8", newline="") as h:
            samples = {r["sample_id"] for r in csv.DictReader(h)}
        if samples - labelled:
            problems.append(f"labels.csv: v0.1 samples without a label {sorted(samples - labelled)}")
        return problems
    problems = rows_problems(out / "rows.csv", pid)
    f = out / "resolutions.csv"
    if not f.exists():
        problems.append("resolutions.csv missing")
    elif first_line(f) != RESOLUTIONS_HEADER:
        problems.append("resolutions.csv: header differs")
    else:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "v1_extract.py"), "check",
                            "--c-input", str(run / "C" / pid / "in"), "--c-output", str(out)],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode:
            problems.append("v1_extract.py check: " + r.stdout.strip()[-400:])
    return problems


def check_agent(run: Path, role: str, pid: str, mode: str, transcript: Path,
                harness: list[str]) -> dict:
    d = run / role / pid
    prompt = run / "prompts" / prompt_name(role, mode)
    launch = (run / "launch" / f"{role}_{pid}.txt").read_text(encoding="utf-8")
    report = {
        "screener": role, "batch": pid, "transcript": transcript.name,
        "launcher_exact": screening_runs.first_user_text(transcript) == launch.removesuffix("\n"),
        "prompt_sha256_ok": (hashlib.sha256(prompt.read_bytes()).hexdigest()
                             == extraction.SHA256[prompt.name]),
        "models": v1_audit_access.models(transcript),
    }
    report["model_ok"] = report["models"] == [extraction.MODEL[role]]
    report["flags"] = v1_audit_access.audit(
        transcript, str(prompt), [str(d / "in"), str(d / "out"), str(d / "work")],
        str(extraction.TOOLS), harness, own=[str(d)])
    report["tool_calls"] = sum(1 for _ in v1_audit_access.tool_calls(transcript))
    report["output_problems"] = output_problems(run, role, pid, mode)
    return report


def tools_problems(tools: Path = extraction.TOOLS) -> list[str]:
    """The shared tools directory must hold exactly its MANIFEST files, unchanged
    (Python's __pycache__ aside): an agent that wrote there could reach the
    others. Checked on every run, because the access audit sees a write made
    through a script's output argument only when the agent reports it."""
    problems = []
    if hashlib.sha256((tools / "MANIFEST").read_bytes()).hexdigest() != extraction.TOOLS_MANIFEST_SHA256:
        return ["tools MANIFEST changed"]
    listed = {}
    for line in (tools / "MANIFEST").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            digest, name = line.split(None, 1)
            listed[name.strip()] = digest
    for name, digest in listed.items():
        f = tools / name
        if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != digest:
            problems.append(f"tools file changed or missing: {name}")
    extra = sorted(str(f.relative_to(tools)) for f in tools.rglob("*")
                   if f.is_file() and f.name != "MANIFEST" and "__pycache__" not in f.parts
                   and str(f.relative_to(tools)) not in listed)
    if extra:
        problems.append(f"files in the tools directory not in its MANIFEST: {extra}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", default=str(extraction.RUN))
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--harness", action="append", default=[])
    ap.add_argument("--reviewed")
    args = ap.parse_args(argv)
    run = Path(args.run)
    (run / "access").mkdir(exist_ok=True)
    modes = {r["paper_id"]: r["mode"] for r in extraction.read(extraction.PAPERS)}
    reviews = screening_runs.load_reviews(args.reviewed)
    used: set = set()
    found, stopped = agents(Path(args.transcripts))
    bad = 0
    for (role, pid), transcripts in sorted(found.items()):
        report = check_agent(run, role, pid, modes[pid], transcripts[-1], args.harness)
        screening_runs.apply_reviews(report, reviews, used)
        report["earlier_agents"] = [t.name for t in transcripts[:-1]]
        report["unfinished_agents"] = stopped.get((role, pid), [])
        (run / "access" / f"{role}_{pid}.json").write_text(json.dumps(report, indent=2) + "\n")
        if not report["ok"]:
            bad += 1
            print(f"{role} {pid}: " + json.dumps(
                {k: report[k] for k in ("launcher_exact", "prompt_sha256_ok", "models",
                                        "flags", "output_problems")})[:900])
    stale = sorted(set(reviews) - used)
    for key in stale:
        print("review matches no flag: " + json.dumps(key))
    tools = tools_problems()
    for t in tools:
        print("TOOLS: " + t)
    print(f"{len(found)} agents checked, {bad} not ok; tools directory "
          + ("clean" if not tools else "NOT clean"))
    return 1 if bad or stale or tools else 0


if __name__ == "__main__":
    sys.exit(main())
