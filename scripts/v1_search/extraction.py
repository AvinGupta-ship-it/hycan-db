"""The v1.0 extraction run (docs/v1_protocol.md §7, §9; §15 Amendments 1 and 2).

  plan      write references/v1_extraction/papers.csv: every paper that §7 and
            Amendment 2 give a selection_route, with its mode and identity
            (doi, first_author, year, journal, title: a v0.1 paper's from its
            v0.1 rows; a new paper's first author's family name and journal
            as printed on the article, from identity.csv, curated from each
            article's first page, with its DOI, year and title from the plan):
              dual    the probability sample (S1, S2), including v0.1 papers
                      drawn and found eligible: extractors A and B, reconciler
                      C (reconcile.md)
              legacy  the other v0.1 papers retrieved by a §8 route, eligible
                      or not (§9 "every other v0.1 paper"): labeller L, a fresh
                      extraction by B, reconciler C (reconcile_legacy.md)
              none    a v0.1 paper that neither route yielded (Amendment 2)
            A new paper takes the next unused paper_id after the v0.1 papers
            (data dictionary, paper_id), in stratum order (S1, then S2) and draw
            order; a v0.1 paper keeps its ID.
  prepare   build each first-stage agent's input (scripts/v1_extract.py
            prepare: every input under a parent of its own) and fill its
            launcher: A and B (dual), or L and B (legacy)
  assemble  after the first stage, copy the two row sets into C's input, run
            the matching code, and fill C's launcher
  check     scripts/v1_extract.py check on C's output
  collect   copy every agent's output into references/v1_extraction/<paper_id>/

Run layout (under --run, default /home/claude/work/runs/extract):

    prompts/<role prompt>             the frozen prompts (prompts/v1/built/)
    <R>/<paper_id>/in, out, work      R = A, B, C, L; V/<paper_id>/rows holds
                                      the v0.1 rows (legacy), read by code only
    launch/<R>_<paper_id>.txt         the filled launcher

    python3 scripts/v1_search/extraction.py plan
    python3 scripts/v1_search/extraction.py status --transcripts DIR
    python3 scripts/v1_search/extraction.py prepare HYC-0066 [...]
    python3 scripts/v1_search/extraction.py assemble HYC-0066 [...]
    python3 scripts/v1_search/extraction.py check HYC-0066 [...]
    python3 scripts/v1_search/extraction.py collect HYC-0066 [...]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import build_frame

_spec = importlib.util.spec_from_file_location("fulltext", HERE / "fulltext.py")
fulltext = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fulltext)

OUT = ROOT / "references" / "v1_extraction"
PAPERS = OUT / "papers.csv"
RUN = Path("/home/claude/work/runs/extract")
TOOLS = Path("/home/claude/work/v1_tools_frozen")
BUILT = ROOT / "prompts" / "v1" / "built"
V01_ROWS = ROOT / "data" / "raw" / "measurements_v0.1.csv"
TRACKING = ROOT / "references" / "paper_tracking.csv"
IDENTITY = OUT / "identity.csv"
IDENTITY_FIELDS = ("doi", "first_author", "year", "journal", "title")
COLUMNS = ("paper_id", "frame_id", "mode", "selection_route", "stratum", "position",
           "v01_paper", "doi", "first_author", "year", "journal", "title")
STRATA = ("S1", "S2")

# Frozen prompts and models (§15 Amendment 1, "Frozen prompts" and "Models").
PROMPT = {"A": "extract_A.md", "B": "extract_B.md", "C": "reconcile.md",
          "C_legacy": "reconcile_legacy.md", "L": "legacy_labels.md"}
SHA256 = {
    "extract_A.md": "4353f51c58076a747b76aac8d2bb2648080a9dcae050747158c776239c4d943a",
    "extract_B.md": "8cd4d7bff7349bd409370c64853a69f8a19e02703823ef3b43806f404ed96b17",
    "reconcile.md": "1366f8657590e33a2954cf458b70038c7e25b6075cecf2db4c0953af7b27ffd6",
    "reconcile_legacy.md": "0570ed5ee23cc7b302ab0bebc2e215930ad21543d148ccdf44253319c6d3c6cc",
    "legacy_labels.md": "afa48428b36915772752e386683b5919b967a0246eabd984021ba622fd285b1a",
    "launcher.md": "4e8680db86961b5f7eebedb9b67b6daec8c684a0f160b32891dc085dd99cc928",
}
MODEL = {"A": "claude-sonnet-5-5", "B": "claude-opus-5-5", "C": "claude-opus-5-5",
         "L": "claude-opus-5-5"}
TOOLS_MANIFEST_SHA256 = "1410223606bdd826ec0ed8c96bee5b3a35a57e4d56f20378dd90d8bc09ece4b7"

# The `extractor` and `verified_by` strings (as in the round-3 pilot).
EXTRACTOR = {
    "A": f"agent A ({MODEL['A']})",
    "B": f"agent B ({MODEL['B']})",
    "C": f"dual extraction A ({MODEL['A']}) and B ({MODEL['B']}), reconciled by C ({MODEL['C']})",
    "C_legacy": f"v0.1 rows and agent B ({MODEL['B']}), reconciled by C ({MODEL['C']})",
}
VERIFIER = f"agent C ({MODEL['C']})"


class ExtractionError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> list[dict[str, str]]:
    return build_frame.read_csv(path) if path.exists() else []


def v01_papers() -> dict[str, dict]:
    """v0.1 paper ID -> its tracking row and frame ID (the 51 with v0.1 rows)."""
    ids = {r["paper_id"] for r in read(V01_ROWS)}
    frame = {r["doi"].strip().lower(): r["frame_id"]
             for r in read(ROOT / "references" / "v1_search" / "frame.csv") if r["doi"].strip()}
    out = {}
    for r in read(TRACKING):
        if r["paper_id"] in ids:
            fid = frame.get(r["doi"].strip().lower())
            if not fid:
                raise ExtractionError(f"{r['paper_id']} has no frame record")
            out[r["paper_id"]] = {**r, "frame_id": fid}
    if len(out) != len(ids):
        raise ExtractionError("a v0.1 paper with rows is missing from paper_tracking.csv")
    return out


def plan_rows() -> list[dict[str, str]]:
    plan = fulltext.read(fulltext.PLAN)
    log = fulltext.read(fulltext.LOG)
    elig = {r["frame_id"]: r for r in fulltext.read(fulltext.ELIG)}
    report = fulltext.walk(plan, log, list(elig.values()), fulltext.read(fulltext.DUPS))
    planned = {p["frame_id"]: p for p in plan}
    curated = {r["frame_id"]: r for r in read(IDENTITY)}
    v01 = v01_papers()
    v01_identity = {}
    for r in read(V01_ROWS):
        v01_identity.setdefault(r["paper_id"], {k: r[k] for k in IDENTITY_FIELDS})
    by_fid = {v["frame_id"]: pid for pid, v in v01.items()}
    obtained = {r["frame_id"] for r in log if r["file"] == "main.pdf" and r["outcome"] == "obtained"}
    next_id = max(int(r["paper_id"].split("-")[1]) for r in read(TRACKING)) + 1
    rows, taken = [], set()
    for st in STRATA:
        if not report[st]["stopped"]:
            raise ExtractionError(f"the {st} walk has not stopped")
        for fid in report[st]["taken_ids"]:
            taken.add(fid)
            if elig.get(fid, {}).get("eligible") != "true":
                continue
            if fid in by_fid:
                pid = by_fid[fid]
            else:
                pid = f"HYC-{next_id:04d}"
                next_id += 1
            p = planned[fid]
            if fid in by_fid:
                ident = v01_identity[pid]
            elif fid in curated:
                c = curated[fid]
                ident = {"doi": p["doi"], "first_author": c["first_author"], "year": p["year"],
                         "journal": c["journal"], "title": p["title"]}
            else:
                raise ExtractionError(f"{fid} has no row in {IDENTITY.name}")
            rows.append({"paper_id": pid, "frame_id": fid, "mode": "dual", "selection_route": st,
                         "stratum": st, "position": p["position"], "v01_paper": str(fid in by_fid).lower(),
                         **ident})
    for pid, v in sorted(v01.items()):
        fid = v["frame_id"]
        if fid in taken:
            continue  # drawn: in the sample if eligible, else excluded by the walk
        p = planned[fid]
        if fid not in obtained:
            mode, route = "none", "legacy_v0.1_not_retrieved"
        elif fid not in elig:
            raise ExtractionError(f"{pid} ({fid}) was retrieved but has no eligibility outcome")
        else:
            mode = "legacy"
            route = "legacy_v0.1" if elig[fid]["eligible"] == "true" else "legacy_v0.1_ineligible"
        rows.append({"paper_id": pid, "frame_id": fid, "mode": mode, "selection_route": route,
                     "stratum": p["stratum"], "position": p["position"], "v01_paper": "true",
                     **v01_identity[pid]})
    for pid, v in v01.items():
        if v["frame_id"] in taken and elig.get(v["frame_id"], {}).get("eligible") != "true":
            raise ExtractionError(f"{pid} was drawn but not found eligible; §7 has no route for it here")
    used = {r["frame_id"] for r in rows}
    stray = sorted(set(curated) - used)
    if stray:
        raise ExtractionError(f"{IDENTITY.name} names records that are not in the sample: {stray}")
    return rows


def cmd_plan(args) -> int:
    rows = plan_rows()
    OUT.mkdir(parents=True, exist_ok=True)
    PAPERS.write_bytes(build_frame.csv_bytes(COLUMNS, rows))
    count = {}
    for r in rows:
        count[(r["mode"], r["selection_route"])] = count.get((r["mode"], r["selection_route"]), 0) + 1
    for k, n in sorted(count.items()):
        print(f"{k[0]:7s} {k[1]:28s} {n}")
    return 0


def paper(pid: str) -> dict[str, str]:
    rows = {r["paper_id"]: r for r in read(PAPERS)}
    if pid not in rows:
        raise ExtractionError(f"{pid} is not in {PAPERS}")
    return rows[pid]


def check_frozen(run: Path) -> None:
    if sha256(TOOLS / "MANIFEST") != TOOLS_MANIFEST_SHA256:
        raise ExtractionError("the tools directory's MANIFEST differs from Amendment 1")
    (run / "prompts").mkdir(parents=True, exist_ok=True)
    for name, digest in SHA256.items():
        dest = run / "prompts" / name
        if not dest.exists():
            shutil.copy(BUILT / name, dest)
        if sha256(dest) != digest:
            raise ExtractionError(f"{dest} differs from its frozen SHA-256")


def launcher(run: Path, role: str, pid: str, prompt: str) -> None:
    d = run / role / pid
    text = (run / "prompts" / "launcher.md").read_text(encoding="utf-8")
    for key, value in (("{PROMPT_PATH}", run / "prompts" / prompt), ("{TOOLS}", TOOLS),
                       ("{INPUT}", d / "in"), ("{OUTPUT}", d / "out"), ("{WORK}", d / "work")):
        text = text.replace(key, str(value))
    if re.search(r"\{[A-Z_]+\}", text):
        raise ExtractionError("launcher placeholder left unfilled")
    (run / "launch").mkdir(exist_ok=True)
    (run / "launch" / f"{role}_{pid}.txt").write_text(text, encoding="utf-8")
    for sub in ("out", "work"):
        (d / sub).mkdir(parents=True, exist_ok=True)


def cmd_prepare(args) -> int:
    run = Path(args.run)
    check_frozen(run)
    for pid in args.paper_id:
        p = paper(pid)
        if p["mode"] == "none":
            raise ExtractionError(f"{pid} is {p['selection_route']}: not extracted (Amendment 2)")
        legacy = p["mode"] == "legacy"
        info = {k: p[k] for k in ("paper_id", "doi", "first_author", "journal", "title")}
        info["year"] = int(p["year"]) if p["year"] else None
        info.update(extractor_A=EXTRACTOR["A"], extractor_B=EXTRACTOR["B"],
                    extractor_C=EXTRACTOR["C_legacy" if legacy else "C"], verifier=VERIFIER)
        (run / "papers").mkdir(parents=True, exist_ok=True)
        pj = run / "papers" / f"{pid}.json"
        pj.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
        pdfs = fulltext._pdfs(fulltext.PDF_STORE / p["frame_id"])
        cmd = [sys.executable, str(ROOT / "scripts" / "v1_extract.py"), "prepare",
               "--paper-json", str(pj), "--out-b", str(run / "B" / pid / "in"),
               "--out-c", str(run / "C" / pid / "in")]
        for pdf in pdfs:
            cmd += ["--pdf", str(pdf)]
        if legacy:
            cmd += ["--legacy", "--v01", str(V01_ROWS), "--out-v01", str(run / "V" / pid / "rows"),
                    "--out-labels", str(run / "L" / pid / "in")]
        else:
            cmd += ["--out-a", str(run / "A" / pid / "in")]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode:
            raise ExtractionError(f"{pid}: {r.stderr.strip() or r.stdout.strip()}")
        first = "L" if legacy else "A"
        launcher(run, first, pid, PROMPT[first])
        launcher(run, "B", pid, PROMPT["B"])
        print(f"{pid} ({p['mode']}, {p['frame_id']}): {len(pdfs)} PDFs; launch {first} and B")
    return 0


def require_finished(transcripts: str, pid: str, roles: tuple[str, ...]) -> None:
    """Refuse unless every named agent for the paper has finished: an agent can
    write its output file before it has finished revising it."""
    states = agent_states(Path(transcripts))
    waiting = [r for r in roles if states.get((r, pid)) != "finished"]
    if waiting:
        raise ExtractionError(f"{pid}: agent {', '.join(waiting)} not finished")


def cmd_assemble(args) -> int:
    run = Path(args.run)
    check_frozen(run)
    for pid in args.paper_id:
        p = paper(pid)
        legacy = p["mode"] == "legacy"
        require_finished(args.transcripts, pid, ("L", "B") if legacy else ("A", "B"))
        first = (run / "V" / pid / "rows") if legacy else (run / "A" / pid / "out")
        cmd = [sys.executable, str(ROOT / "scripts" / "v1_extract.py"), "assemble",
               "--c", str(run / "C" / pid / "in"), "--first", str(first),
               "--second", str(run / "B" / pid / "out")]
        if legacy:
            cmd += ["--legacy", "--labels", str(run / "L" / pid / "out" / "labels.csv")]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode:
            raise ExtractionError(f"{pid}: {r.stderr.strip() or r.stdout.strip()}")
        launcher(run, "C", pid, PROMPT["C_legacy" if legacy else "C"])
        print(f"{pid}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'assembled'}; launch C")
    return 0


def cmd_check(args) -> int:
    run = Path(args.run)
    bad = 0
    for pid in args.paper_id:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "v1_extract.py"), "check",
                            "--c-input", str(run / "C" / pid / "in"),
                            "--c-output", str(run / "C" / pid / "out")],
                           capture_output=True, text=True, cwd=ROOT, check=False)
        print(f"== {pid}\n{r.stdout.strip()}")
        bad += r.returncode != 0
    return 1 if bad else 0


def cmd_collect(args) -> int:
    """Copy every agent's output (and C's match.csv and digitized_means.csv)
    into references/v1_extraction/<paper_id>/, which is released (§9)."""
    run = Path(args.run)
    for pid in args.paper_id:
        p = paper(pid)
        roles = ("L", "B", "C") if p["mode"] == "legacy" else ("A", "B", "C")
        require_finished(args.transcripts, pid, roles)
        dest = OUT / pid
        if dest.exists():
            raise ExtractionError(f"{dest} exists")
        for role in roles:
            src = run / role / pid / "out"
            if not any(src.iterdir()):
                raise ExtractionError(f"{pid}: {role} wrote no output")
            shutil.copytree(src, dest / role)
        (dest / "C_input").mkdir()
        for name in ("match.csv", "digitized_means.csv") + (("labels.csv",) if p["mode"] == "legacy" else ()):
            shutil.copy(run / "C" / pid / "in" / name, dest / "C_input" / name)
        print(f"{pid}: collected {', '.join(roles)}")
    return 0


def interrupted(transcript: Path) -> bool:
    """True when an agent stopped on an API error (for example the account's
    usage limit) instead of ending its task: its last assistant entry is the
    harness's error message. Such an agent is resumed in its own session."""
    last = None
    try:
        with transcript.open("rb") as fh:
            fh.seek(0, 2)
            size = fh.tell()
            fh.seek(max(0, size - 262144))
            lines = fh.read().decode("utf-8", errors="replace").splitlines()
    except OSError:
        return False
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "assistant":
            last = d
            break
    return bool(last and last.get("isApiErrorMessage"))


def agent_states(transcripts: Path) -> dict[tuple[str, str], str]:
    """(role, paper_id) -> 'running', 'interrupted' or 'finished', from the
    agents' metadata (the description each agent is started with:
    'Extraction <R> <paper_id>') and, for a stopped agent, its transcript."""
    out: dict[tuple[str, str], str] = {}
    for meta_path in sorted(transcripts.glob("*.meta.json")):
        meta = json.loads(meta_path.read_text())
        m = re.match(r"^Extraction (A|B|C|L) (HYC-\d{4})$", meta.get("description", ""))
        if m:
            key = (m.group(1), m.group(2))
            state = "finished" if meta.get("finished") else "running"
            if state == "finished" and interrupted(meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))):
                state = "interrupted"
            if out.get(key) != "finished":
                out[key] = state
    return out


def cmd_status(args) -> int:
    """Each paper's place in the run, and what can be started next."""
    run = Path(args.run)
    states = agent_states(Path(args.transcripts))
    papers = [r for r in read(PAPERS) if r["mode"] != "none"]
    running = sum(1 for v in states.values() if v == "running")
    todo = {"resume": sorted(f"{r}:{pid}" for (r, pid), v in states.items() if v == "interrupted"),
            "prepare": [], "launch_first": [], "assemble": [], "launch_C": [], "collect": []}
    done = 0
    for p in papers:
        pid = p["paper_id"]
        first = ("L", "B") if p["mode"] == "legacy" else ("A", "B")
        if (OUT / pid).exists():
            done += 1
            continue
        if not (run / "launch" / f"B_{pid}.txt").exists():
            todo["prepare"].append(pid)
        elif any((r, pid) not in states for r in first):
            todo["launch_first"].append(pid + ":" + "".join(r for r in first if (r, pid) not in states))
        elif all(states[(r, pid)] == "finished" for r in first):
            if not (run / "launch" / f"C_{pid}.txt").exists():
                todo["assemble"].append(pid)
            elif ("C", pid) not in states:
                todo["launch_C"].append(pid)
            elif states[("C", pid)] == "finished":
                todo["collect"].append(pid)
    print(f"papers {len(papers)}: collected {done}; agents running {running}")
    for k, v in todo.items():
        print(f"{k} ({len(v)}): {' '.join(v[:40])}{' ...' if len(v) > 40 else ''}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    st = sub.add_parser("status")
    st.add_argument("--run", default=str(RUN))
    st.add_argument("--transcripts", required=True)
    for name in ("prepare", "assemble", "check", "collect"):
        s = sub.add_parser(name)
        s.add_argument("paper_id", nargs="+")
        s.add_argument("--run", default=str(RUN))
        if name in ("assemble", "collect"):
            s.add_argument("--transcripts", required=True)
    args = ap.parse_args(argv)
    try:
        return {"plan": cmd_plan, "status": cmd_status, "prepare": cmd_prepare, "assemble": cmd_assemble,
                "check": cmd_check, "collect": cmd_collect}[args.cmd](args)
    except ExtractionError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
