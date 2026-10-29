"""Full-text retrieval, eligibility and the sampling walk (docs/v1_protocol.md
§4, §6, §7, §8).

  plan     write references/v1_fulltext/retrieval_plan.csv: in draw order, up
           to the assessment cap of each stratum (110 in S1, 80 in S2), every
           record with its two retrieval routes (§8):
             route 1  an open-access PDF at the record's OpenAlex
                      best_oa_location (pdf_url, else landing_page_url) or
                      open_access.oa_url, read from the archived search
                      responses; a record with no OpenAlex record has none
             route 2  the DOI landing page through the author's university
                      library; a record without a DOI has none
  status   read the plan, the retrieval log and the eligibility outcomes and
           report the walk (§7): per stratum, the records taken, assessed,
           eligible, not retrieved and frame duplicates, whether the walk has
           stopped and why, and the next records to retrieve or assess.
           Writes references/v1_fulltext/walk.json.
  prepare  build the two assessors' inputs for one retrieved record, each
           under a parent of its own (Amendment 1, item 26): record.json,
           text/ (pdftotext -layout) and pages/ (PNG), from the record's PDFs
           (main.pdf first, then si1.pdf, si2.pdf, ...)
  resolver build the resolver's input: the assessors' input plus
           assessments/a.json and b.json
  collect  check the assessments of one record, decide its outcome (the
           assessors' common decision, else the resolver's) and write it to
           references/v1_fulltext/eligibility.csv

The retrieval log (references/v1_fulltext/retrieval_log.csv) has one row per
route tried for each file: frame_id, file (main.pdf, si1.pdf, ...), route
(oa or library), url, outcome (obtained, no_full_text, not_available),
sha256, bytes, at_utc, note. A record is retrieved when main.pdf was
obtained. PDFs are kept outside the repository (§14: not released); the log
keeps their SHA-256.

Walk rules (§7): records are taken in permuted order. A record not obtained by
the routes is `not_retrieved`; a record whose full text or bibliographic
identity repeats an earlier drawn record is `frame_duplicate`; both are
skipped. The walk stops when the stratum's target of eligible papers is
reached (60 in S1, 40 in S2), when the stratum is exhausted, or after its
assessment cap. d_h counts every record taken (assessed, not_retrieved and
frame_duplicate together).

    python3 scripts/v1_search/fulltext.py plan
    python3 scripts/v1_search/fulltext.py status
    python3 scripts/v1_search/fulltext.py prepare FRAME_ID --pdfs DIR
        --out-a DIR --out-b DIR
    python3 scripts/v1_search/fulltext.py resolver FRAME_ID --input DIR
        --a FILE --b FILE --out DIR
    python3 scripts/v1_search/fulltext.py collect FRAME_ID --a FILE --b FILE
        [--resolver FILE]
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_frame
import merge_search

ROOT = HERE.parents[1]
SEARCH = ROOT / "references" / "v1_search"
FULLTEXT = ROOT / "references" / "v1_fulltext"
PLAN = FULLTEXT / "retrieval_plan.csv"
LOG = FULLTEXT / "retrieval_log.csv"
ELIG = FULLTEXT / "eligibility.csv"
DUPS = FULLTEXT / "frame_duplicates.csv"

TARGET = {"S1": 60, "S2": 40}
CAP = {"S1": 110, "S2": 80}
PLAN_COLUMNS = ("stratum", "position", "frame_id", "openalex_id", "doi", "title",
                "year", "is_retracted", "route1_url", "route1_field", "route2_url")
LOG_COLUMNS = ("frame_id", "file", "route", "url", "outcome", "sha256", "bytes",
               "at_utc", "note")
OUTCOMES = ("obtained", "no_full_text", "not_available")
ELIG_COLUMNS = ("frame_id", "eligible_a", "code_a", "eligible_b", "code_b",
                "agree", "resolved", "eligible", "exclusion_code")
CODES = ("theoretical_only", "electrochemical", "not_carbon", "not_primary",
         "retracted", "no_conditions_stated", "no_surface_area", "not_english",
         "duplicate_data")
CRITERIA = ("I1", "I2", "I3", "I4", "I5")


class WalkError(RuntimeError):
    pass


def openalex_locations() -> dict[str, dict[str, str]]:
    """Each OpenAlex work's open-access locations, from the archived responses."""
    out: dict[str, dict[str, str]] = {}
    for f in merge_search.batch_files("hycan_v1_openalex_"):  # includes the slices
        data = merge_search.read_json(f)
        for q in data["batch"]:
            for page in q["pages"]:
                for w in merge_search.checked_body(page).get("results") or []:
                    best = w.get("best_oa_location") or {}
                    oa = w.get("open_access") or {}
                    out[w["id"].rsplit("/", 1)[-1]] = {
                        "pdf_url": best.get("pdf_url") or "",
                        "landing_page_url": best.get("landing_page_url") or "",
                        "oa_url": oa.get("oa_url") or "",
                    }
    return out


def route1(loc: dict[str, str] | None) -> tuple[str, str]:
    if not loc:
        return "", ""
    for field in ("pdf_url", "landing_page_url", "oa_url"):
        if loc.get(field):
            name = "open_access.oa_url" if field == "oa_url" else f"best_oa_location.{field}"
            return loc[field], name
    return "", ""


def plan_rows() -> list[dict[str, str]]:
    merged = {r["frame_id"]: r for r in build_frame.load_merged(SEARCH)}
    locs = openalex_locations()
    order = build_frame.read_csv(SEARCH / "draw_order.csv")
    rows = []
    for st in ("S1", "S2"):
        for d in [r for r in order if r["stratum"] == st][: CAP[st]]:
            m = merged[d["frame_id"]]
            oa_id = (m["openalex_id"] or "").rsplit("/", 1)[-1]
            url, field = route1(locs.get(oa_id) if oa_id else None)
            rows.append({
                "stratum": st, "position": d["position"], "frame_id": d["frame_id"],
                "openalex_id": oa_id, "doi": m["doi"], "title": m["title"],
                "year": m["year"], "is_retracted": m["is_retracted"],
                "route1_url": url, "route1_field": field,
                "route2_url": f"https://doi.org/{m['doi']}" if m["doi"] else "",
            })
    return rows


def read(path: Path) -> list[dict[str, str]]:
    return build_frame.read_csv(path) if path.exists() else []


def check_log(log: list[dict[str, str]], plan_ids: set[str]) -> None:
    for r in log:
        if r["frame_id"] not in plan_ids:
            raise WalkError(f"retrieval log names {r['frame_id']}, not in the plan")
        if r["outcome"] not in OUTCOMES or r["route"] not in ("oa", "library"):
            raise WalkError(f"retrieval log row for {r['frame_id']} has {r['route']}/{r['outcome']}")
        if (r["outcome"] == "obtained") != bool(r["sha256"]):
            raise WalkError(f"{r['frame_id']} {r['file']}: a SHA-256 goes with obtained only")


def walk(plan: list[dict], log: list[dict], elig: list[dict], dups: list[dict]) -> dict:
    """The §7 walk state for each stratum."""
    check_log(log, {p["frame_id"] for p in plan})
    tried: dict[str, set[str]] = {}
    obtained: set[str] = set()
    for r in log:
        if r["file"] == "main.pdf":
            tried.setdefault(r["frame_id"], set()).add(r["route"])
            if r["outcome"] == "obtained":
                obtained.add(r["frame_id"])
    outcome = {r["frame_id"]: r for r in elig}
    dup = {r["frame_id"]: r for r in dups}
    report = {}
    for st in ("S1", "S2"):
        recs = sorted((p for p in plan if p["stratum"] == st), key=lambda p: int(p["position"]))
        s = {"target": TARGET[st], "cap": CAP[st], "taken": 0, "assessed": 0,
             "eligible": 0, "not_retrieved": 0, "frame_duplicate": 0,
             "stopped": None, "next_to_retrieve": [], "next_to_assess": [],
             "taken_ids": []}
        for p in recs:
            if s["eligible"] >= TARGET[st]:
                s["stopped"] = "target reached"
                break
            if s["assessed"] >= CAP[st]:
                s["stopped"] = "assessment cap"
                break
            fid = p["frame_id"]
            needed = {"oa"} if p["route1_url"] else set()
            if p["route2_url"]:
                needed.add("library")
            done_routes = tried.get(fid, set())
            if fid in dup:
                s["taken"] += 1; s["frame_duplicate"] += 1; s["taken_ids"].append(fid)
                continue
            if fid not in obtained:
                if needed - done_routes:
                    s["next_to_retrieve"].append(fid)
                    break
                s["taken"] += 1; s["not_retrieved"] += 1; s["taken_ids"].append(fid)
                continue
            if fid not in outcome:
                s["next_to_assess"].append(fid)
                break
            s["taken"] += 1; s["assessed"] += 1; s["taken_ids"].append(fid)
            if outcome[fid]["eligible"] == "true":
                s["eligible"] += 1
        else:
            if s["eligible"] >= TARGET[st]:
                s["stopped"] = "target reached"
            elif s["assessed"] >= CAP[st]:
                s["stopped"] = "assessment cap"
            elif not s["next_to_retrieve"] and not s["next_to_assess"]:
                s["stopped"] = "plan exhausted"
        report[st] = s
    # Retrieval does not depend on eligibility, so records past the frontier
    # may be retrieved ahead of it. A record retrieved but never reached is
    # not taken: it enters no count.
    for st in ("S1", "S2"):
        s = report[st]
        if s["stopped"]:
            s["retrieve_ahead"] = []
            continue
        recs = sorted((p for p in plan if p["stratum"] == st), key=lambda p: int(p["position"]))
        ahead = []
        for p in recs:
            fid = p["frame_id"]
            needed = ({"oa"} if p["route1_url"] else set()) | ({"library"} if p["route2_url"] else set())
            if fid in obtained or fid in dup or not (needed - tried.get(fid, set())):
                continue
            ahead.append(fid)
        s["retrieve_ahead"] = ahead
    return report


def _quotes_ok(a: dict) -> list[str]:
    problems = []
    for c in CRITERIA:
        v = a["criteria"].get(c, {})
        if v.get("met") is True and not v.get("quote"):
            problems.append(f"{c} met without a quote")
    if a["eligible"] and a["exclusion_code"] is not None:
        problems.append("eligible with an exclusion code")
    if not a["eligible"] and a["exclusion_code"] not in CODES:
        problems.append(f"exclusion code {a['exclusion_code']!r}")
    if a["eligible"] and not all(a["criteria"].get(c, {}).get("met") is True for c in CRITERIA):
        problems.append("eligible with a criterion not met")
    return problems


def load_assessment(path: Path, fid: str) -> dict:
    a = json.loads(path.read_text(encoding="utf-8"))
    if a.get("frame_id") != fid:
        raise WalkError(f"{path}: frame_id {a.get('frame_id')!r}, expected {fid}")
    if not isinstance(a.get("eligible"), bool) or set(a.get("criteria", {})) != set(CRITERIA):
        raise WalkError(f"{path}: not an assessment in the prompt's format")
    problems = _quotes_ok(a)
    if problems:
        raise WalkError(f"{path}: " + "; ".join(problems))
    return a


def decide(a: dict, b: dict, resolver: dict | None) -> dict[str, str]:
    agree = (a["eligible"] == b["eligible"] and a["exclusion_code"] == b["exclusion_code"]
             and all(a["criteria"][c]["met"] == b["criteria"][c]["met"] for c in CRITERIA))
    if not agree and resolver is None:
        raise WalkError(f"{a['frame_id']}: the assessors disagree; the resolver decides")
    if agree and resolver is not None:
        raise WalkError(f"{a['frame_id']}: the assessors agree; no resolver is used")
    final = a if agree else resolver
    return {
        "frame_id": a["frame_id"],
        "eligible_a": str(a["eligible"]).lower(), "code_a": a["exclusion_code"] or "",
        "eligible_b": str(b["eligible"]).lower(), "code_b": b["exclusion_code"] or "",
        "agree": str(agree).lower(), "resolved": str(not agree).lower(),
        "eligible": str(final["eligible"]).lower(),
        "exclusion_code": final["exclusion_code"] or "",
    }


def _pdfs(d: Path) -> list[Path]:
    main = d / "main.pdf"
    if not main.exists():
        raise WalkError(f"{d} has no main.pdf")
    si = sorted(d.glob("si*.pdf"), key=lambda p: int(p.stem[2:]))
    return [main, *si]


def _render(pdfs: list[Path], d: Path, dpi: int) -> None:
    (d / "text").mkdir(parents=True)
    (d / "pages").mkdir()
    for pdf in pdfs:
        subprocess.run(["pdftotext", "-layout", str(pdf), str(d / "text" / f"{pdf.stem}.txt")],
                       check=True)
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(d / "pages" / pdf.stem)],
                       check=True)


def record_json(fid: str) -> dict:
    p = {r["frame_id"]: r for r in read(PLAN)}[fid]
    return {"frame_id": fid, "doi": p["doi"], "title": p["title"],
            "year": int(p["year"]) if p["year"] else None,
            "is_retracted": p["is_retracted"] == "True"}


def cmd_plan(args) -> int:
    rows = plan_rows()
    FULLTEXT.mkdir(parents=True, exist_ok=True)
    PLAN.write_bytes(build_frame.csv_bytes(PLAN_COLUMNS, rows))
    for st in ("S1", "S2"):
        mine = [r for r in rows if r["stratum"] == st]
        print(f"{st}: {len(mine)} records, {sum(bool(r['route1_url']) for r in mine)} with "
              f"route 1, {sum(bool(r['route2_url']) for r in mine)} with route 2, "
              f"{sum(not r['route1_url'] and not r['route2_url'] for r in mine)} with neither")
    return 0


def duplicate_candidates(plan: list[dict], log: list[dict]) -> list[list[str]]:
    """Pairs of planned records that may be one paper: the same main.pdf
    SHA-256, or the same normalized title with years at most 1 apart. Each
    pair is checked by hand; a confirmed later record goes in
    frame_duplicates.csv."""
    pairs = []
    by_sha: dict[str, str] = {}
    for r in log:
        if r["file"] == "main.pdf" and r["sha256"]:
            if r["sha256"] in by_sha and by_sha[r["sha256"]] != r["frame_id"]:
                pairs.append([by_sha[r["sha256"]], r["frame_id"], "same main.pdf"])
            by_sha.setdefault(r["sha256"], r["frame_id"])
    seen: dict[str, list[dict]] = {}
    for p in plan:
        key = merge_search.norm_title(p["title"])
        for q in seen.get(key, []):
            try:
                close = abs(int(q["year"] or 0) - int(p["year"] or 0)) <= 1
            except ValueError:
                close = False
            if key and close:
                pairs.append([q["frame_id"], p["frame_id"], "same title"])
        seen.setdefault(key, []).append(p)
    return pairs


def cmd_status(args) -> int:
    plan, log = read(PLAN), read(LOG)
    report = walk(plan, log, read(ELIG), read(DUPS))
    report["duplicate_candidates"] = duplicate_candidates(plan, log)
    (FULLTEXT / "walk.json").write_text(json.dumps(report, indent=2) + "\n")
    for st in ("S1", "S2"):
        s = report[st]
        print(f"{st}: taken {s['taken']}, assessed {s['assessed']}, eligible "
              f"{s['eligible']}/{s['target']}, not retrieved {s['not_retrieved']}, "
              f"duplicates {s['frame_duplicate']}; stopped: {s['stopped']}; next "
              f"retrieve {s['next_to_retrieve']} assess {s['next_to_assess']}")
    for pair in report["duplicate_candidates"]:
        print("check for a frame duplicate: " + " / ".join(pair))
    return 0


def cmd_log(args) -> int:
    """Append one route attempt to the retrieval log."""
    plan = {r["frame_id"]: r for r in read(PLAN)}
    if args.frame_id not in plan:
        raise WalkError(f"{args.frame_id} is not in the plan")
    row = {"frame_id": args.frame_id, "file": args.file, "route": args.route,
           "url": args.url, "outcome": args.outcome, "sha256": args.sha256 or "",
           "bytes": str(args.bytes or ""), "at_utc": args.at_utc, "note": args.note or ""}
    rows = read(LOG) + [row]
    check_log(rows, set(plan))
    if any(r["frame_id"] == row["frame_id"] and r["file"] == row["file"]
           and r["route"] == row["route"] for r in rows[:-1]):
        raise WalkError(f"{args.frame_id} {args.file} was already tried by route {args.route}")
    LOG.write_bytes(build_frame.csv_bytes(LOG_COLUMNS, rows))
    print(json.dumps(row))
    return 0


def cmd_prepare(args) -> int:
    pdfs = _pdfs(Path(args.pdfs))
    dirs = [Path(args.out_a), Path(args.out_b)]
    if dirs[0].resolve().parent == dirs[1].resolve().parent:
        raise WalkError("each assessor's input needs a parent of its own")
    for d in dirs:
        if d.exists():
            raise WalkError(f"{d} exists")
        _render(pdfs, d, args.dpi)
        (d / "record.json").write_text(json.dumps(record_json(args.frame_id), indent=2) + "\n")
    print(f"prepared {args.frame_id}: {len(pdfs)} PDFs")
    return 0


def cmd_resolver(args) -> int:
    src, out = Path(args.input), Path(args.out)
    if out.exists():
        raise WalkError(f"{out} exists")
    shutil.copytree(src, out)
    (out / "assessments").mkdir()
    shutil.copy(args.a, out / "assessments" / "a.json")
    shutil.copy(args.b, out / "assessments" / "b.json")
    return 0


def cmd_collect(args) -> int:
    fid = args.frame_id
    a = load_assessment(Path(args.a), fid)
    b = load_assessment(Path(args.b), fid)
    r = load_assessment(Path(args.resolver), fid) if args.resolver else None
    row = decide(a, b, r)
    rows = [x for x in read(ELIG) if x["frame_id"] != fid]
    if len(rows) != len(read(ELIG)):
        raise WalkError(f"{fid} already has an outcome")
    rows.append(row)
    ELIG.write_bytes(build_frame.csv_bytes(ELIG_COLUMNS, rows))
    print(json.dumps(row))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    sub.add_parser("status")
    p = sub.add_parser("prepare")
    p.add_argument("frame_id"); p.add_argument("--pdfs", required=True)
    p.add_argument("--out-a", required=True); p.add_argument("--out-b", required=True)
    p.add_argument("--dpi", type=int, default=150)
    r = sub.add_parser("resolver")
    r.add_argument("frame_id"); r.add_argument("--input", required=True)
    r.add_argument("--a", required=True); r.add_argument("--b", required=True)
    r.add_argument("--out", required=True)
    lg = sub.add_parser("log")
    lg.add_argument("frame_id"); lg.add_argument("--file", required=True)
    lg.add_argument("--route", required=True, choices=["oa", "library"])
    lg.add_argument("--url", required=True)
    lg.add_argument("--outcome", required=True, choices=list(OUTCOMES))
    lg.add_argument("--sha256"); lg.add_argument("--bytes", type=int)
    lg.add_argument("--at-utc", required=True); lg.add_argument("--note")
    c = sub.add_parser("collect")
    c.add_argument("frame_id"); c.add_argument("--a", required=True)
    c.add_argument("--b", required=True); c.add_argument("--resolver")
    args = ap.parse_args(argv)
    try:
        return {"plan": cmd_plan, "status": cmd_status, "log": cmd_log, "prepare": cmd_prepare,
                "resolver": cmd_resolver, "collect": cmd_collect}[args.cmd](args)
    except WalkError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
