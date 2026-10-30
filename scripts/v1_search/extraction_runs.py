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
import posixpath
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


# Supplementary checks, added during the run (README, "Agent checks"): the access
# audit accepts any command that names one of the two tool scripts, so it does
# not see a script's source being read, and it accepts any path that starts with
# /dev/null, so it does not see a file such as /dev/null.png being written.
READERS = {"grep", "egrep", "fgrep", "rg", "sed", "awk", "gawk", "cat", "head", "tail", "less", "more",
           "wc", "od", "xxd", "hexdump", "strings", "cp", "mv", "diff", "cmp", "sha256sum", "md5sum",
           "nl", "tac", "cut", "sort", "uniq", "file", "stat", "ls", "find", "tree", "du", "tar", "zip",
           "base64", "vi", "vim", "nano"}
PATTERN_FIRST = {"grep", "egrep", "fgrep", "rg", "sed", "awk", "gawk"}
TOOL_SCRIPT_REL = re.compile(r"(?<![\w/.])scripts/(digitize_figure|validate_row_detail)\.py\b")
TOOLS_VAR = re.compile(r"\$\{?TOOLS?\b")
PY_TOOLS_READ = re.compile(
    r"open\(\s*[rbuf]*['\"][^'\"]*(v1_tools_frozen|scripts/(digitize_figure|validate_row_detail)\.py)"
    r"|^\s*(?:import\s+(?:scripts\.)?(?:digitize_figure|validate_row_detail)\b"
    r"|from\s+(?:scripts\.)?(?:digitize_figure|validate_row_detail)\s+import\b)|inspect\.getsource", re.MULTILINE)
DEVICE = re.compile(r"/dev/(?!(?:null|stdout|stderr|tty|zero|urandom|random)(?![\w.])|fd/)[\w./-]*")


def supplementary_flags(transcript: Path, tools: str) -> list[dict]:
    """Calls that read or list a file in the tools directory (a script's source
    included) or name a device path other than /dev/null, /dev/stdout and
    /dev/stderr."""
    flags = []

    def flag(n, name, reason, detail):
        if not any(f["call"] == n and f["reason"] == reason for f in flags):
            flags.append({"call": n, "tool": name, "reason": reason, "detail": str(detail)[:300]})

    for n, name, args in v1_audit_access.tool_calls(transcript):
        if name in ("Read", "Grep", "Glob", "Write", "Edit", "NotebookEdit"):
            path = str(args.get("file_path") or args.get("path") or args.get("notebook_path") or "")
            if path == tools or path.startswith(tools + "/"):
                flag(n, name, "tool call opens a path in the tools directory (supplementary check)", path)
            if DEVICE.search(path):
                flag(n, name, "tool call names a device path (supplementary check)", path)
            continue
        if name != "Bash":
            continue
        cmd = args.get("command") or ""
        for pipe in v1_audit_access.pipelines(v1_audit_access.HEREDOC.sub(" ", cmd)):
            for words in pipe:
                if words and posixpath.basename(words[0]) in READERS and any(
                        a == tools or a.startswith(tools + "/") or TOOL_SCRIPT_REL.search(a) or TOOLS_VAR.search(a)
                        for a in words[1:]):
                    flag(n, name, "command reads or lists a file in the tools directory (supplementary check)",
                         " ".join(words))
        # A file named relatively while the tools directory is the working directory.
        for body, _ in v1_audit_access.tools_context(v1_audit_access.HEREDOC.sub(" ", cmd), tools):
            for pipe in v1_audit_access.pipelines(body):
                words = pipe[0]
                prog = posixpath.basename(words[0]) if words else ""
                if prog not in READERS:
                    continue
                ops, skip = [], False
                for a in words[1:]:
                    if skip:
                        skip = False
                    elif re.fullmatch(r"\d*(>>?|<)&?", a):
                        skip = True  # a redirection and its target
                    elif not a.startswith("-") and not a.isdigit():
                        ops.append(a)
                if prog in PATTERN_FIRST and ops:
                    ops = ops[1:]
                if not ops and prog in ("ls", "find", "tree", "du"):
                    ops = ["."]
                if any(not a.startswith(("/", "$")) for a in ops):
                    flag(n, name, "command reads or lists a relative path in the tools directory (supplementary check)",
                         " ".join(words))
        if PY_TOOLS_READ.search(cmd):
            flag(n, name, "code opens or imports a file in the tools directory (supplementary check)",
                 PY_TOOLS_READ.search(cmd).group(0))
        for m in DEVICE.finditer(cmd):
            flag(n, name, "command names a device path other than /dev/null, /dev/stdout or /dev/stderr "
                 "(supplementary check)", m.group(0))
    return flags


CROSS = re.compile(r"/home/claude/work/hycan-db|measurements_v0\.1|/runs/extract/(?:pilot|[ABCLV])/HYC-\d{4}"
                   r"|/home/claude/work/runs/(?!extract\b)\w+")


def cross_access(transcript: Path, run: Path, role: str, pid: str) -> list[str]:
    """Every place a tool call names the repository, the v0.1 rows file, another
    agent's run directory or another stage's run folder: the paths whose opening
    discards an output under Amendment 1, item 26. Text alone is listed too;
    each entry is read against its call (README, "Agent checks")."""
    own = str(run / role / pid)
    hits = []
    for n, name, args in v1_audit_access.tool_calls(transcript):
        for m in CROSS.finditer(json.dumps(args)):
            path = m.group(0)
            if path.startswith("/runs/extract/") and own.endswith(path):
                continue
            hits.append(f"call {n} {name}: {path}")
    return hits


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
    report["flags"] += supplementary_flags(transcript, str(extraction.TOOLS))
    report["cross_access"] = cross_access(transcript, run, role, pid)
    report["tool_calls"] = sum(1 for _ in v1_audit_access.tool_calls(transcript))
    report["output_problems"] = output_problems(run, role, pid, mode)
    return report


def cache_key(run: Path, role: str, pid: str, transcript: Path, harness: list[str]) -> str:
    """What a report depends on: the transcript, the agent's run directory, its
    launcher and prompt, and the checking code. A cached report is reused only
    while all of these are unchanged; reviews are applied afresh every run."""
    h = hashlib.sha256()
    st = transcript.stat()
    h.update(f"{transcript.name} {st.st_size} {st.st_mtime_ns} {harness}".encode())
    for f in sorted((run / role / pid).rglob("*")):
        if f.is_file() and "work" not in f.relative_to(run / role / pid).parts[:1]:
            s = f.stat()
            h.update(f"{f.relative_to(run)} {s.st_size} {s.st_mtime_ns}".encode())
    for f in (run / "launch" / f"{role}_{pid}.txt", Path(__file__), Path(v1_audit_access.__file__),
              Path(screening_runs.__file__), Path(extraction.__file__), ROOT / "scripts" / "v1_extract.py"):
        h.update(hashlib.sha256(f.read_bytes()).digest())
    for f in sorted((run / "prompts").glob("*.md")):
        h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


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
    cache_dir = run / "access_cache"
    cache_dir.mkdir(exist_ok=True)
    for (role, pid), transcripts in sorted(found.items()):
        key = cache_key(run, role, pid, transcripts[-1], args.harness)
        cached = cache_dir / f"{role}_{pid}.json"
        try:
            hit = json.loads(cached.read_text())
        except (OSError, ValueError):
            hit = {}
        if hit.get("key") == key:
            report = hit["report"]
        else:
            report = check_agent(run, role, pid, modes[pid], transcripts[-1], args.harness)
            cached.write_text(json.dumps({"key": key, "report": report}) + "\n")
        screening_runs.apply_reviews(report, reviews, used)
        if report["cross_access"]:
            report["ok"] = False
        report["earlier_agents"] = [t.name for t in transcripts[:-1]]
        report["unfinished_agents"] = stopped.get((role, pid), [])
        (run / "access" / f"{role}_{pid}.json").write_text(json.dumps(report, indent=2) + "\n")
        if not report["ok"]:
            bad += 1
            print(f"{role} {pid}: " + json.dumps(
                {k: report[k] for k in ("launcher_exact", "prompt_sha256_ok", "models",
                                        "flags", "output_problems", "cross_access")})[:900])
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
