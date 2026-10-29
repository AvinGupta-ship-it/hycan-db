"""PRISMA 2020 flow counts and diagram (docs/v1_protocol.md §6, §14).

§14: "A flow diagram and checklist (Page et al. 2021), with stages: identified
per source; merged; screened; frame (per stratum); drawn; retrieved; assessed;
eligible; analysed (per RQ)." Every count here is computed from committed files:

  identified, merged   references/v1_search/merge_counts.json (merge_search.py),
                       checked against merged_records.csv by its SHA-256
  screened             references/v1_screening/screen_a.csv, screen_b.csv
  frame                references/v1_search/frame.csv
  drawn ... eligible   references/v1_fulltext/ (retrieval_plan.csv,
                       retrieval_log.csv, eligibility.csv), through the §7 walk
                       in fulltext.py
  author's review      references/v1_fulltext/author_review.csv (§6)
  v0.1 papers          data/raw/measurements_v0.1.csv (the 51 papers with v0.1
                       rows), joined to the frame by DOI through
                       references/paper_tracking.csv
  analysed (per RQ)    not yet computed: the §11 analyses have not been run,
                       and the diagram says so

Records the walk did not take enter no count past "frame", except the v0.1
papers, which §7 assesses whether drawn or not; they have a lane of their own.
Records retrieved or assessed ahead of a stratum's stop are outside the sample
(§7) and are counted only in a note.

Writes references/v1_prisma/prisma_counts.json and the diagram as
references/v1_prisma/prisma_flow.pdf and .png. The output depends only on the
inputs, so a re-run reproduces it byte for byte.

    python3 scripts/v1_search/prisma.py
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import build_frame

_spec = importlib.util.spec_from_file_location("fulltext", HERE / "fulltext.py")
fulltext = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fulltext)

SEARCH = ROOT / "references" / "v1_search"
SCREEN = ROOT / "references" / "v1_screening"
OUT_DIR = ROOT / "references" / "v1_prisma"
V01_ROWS = ROOT / "data" / "raw" / "measurements_v0.1.csv"
TRACKING = ROOT / "references" / "paper_tracking.csv"
REVIEW = fulltext.FULLTEXT / "author_review.csv"
STRATA = ("S1", "S2")


class PrismaError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identification(merge: dict, merged_sha: str) -> dict:
    if merge["merged_sha256"] != merged_sha:
        raise PrismaError("merge_counts.json does not describe merged_records.csv")
    oa_distinct = merge["openalex_unique"] + merge["openalex_doi_duplicates_merged"]
    removed = merge["openalex_doi_duplicates_merged"] + merge["s2_matched_doi"] + merge["s2_matched_title_year"]
    if oa_distinct + merge["s2_records"] - removed != merge["merged_total"]:
        raise PrismaError("identified minus duplicates is not the merged total")
    return {
        "openalex": {"records": oa_distinct, "subqueries": merge["openalex_subqueries"],
                     "hits_over_subqueries": merge["openalex_count_sum"]},
        "semantic_scholar": {"records": merge["s2_records"]},
        "duplicates_removed": {"total": removed,
                               "openalex_ids_sharing_a_doi": merge["openalex_doi_duplicates_merged"],
                               "semantic_scholar_matched_by_doi": merge["s2_matched_doi"],
                               "semantic_scholar_matched_by_title_and_year": merge["s2_matched_title_year"]},
        "merged": merge["merged_total"],
    }


def screening(screen_a: list[dict], screen_b: list[dict], frame: list[dict], merged_n: int) -> dict:
    a = {r["frame_id"]: r for r in screen_a}
    b = {r["frame_id"]: r for r in screen_b}
    if set(a) != set(b) or len(a) != merged_n:
        raise PrismaError("the two screeners did not screen the same merged records")
    both = sorted(f for f in a if a[f]["decision"] == "exclude" and b[f]["decision"] == "exclude")
    same = collections.Counter(a[f]["exclusion_code"] for f in both
                               if a[f]["exclusion_code"] == b[f]["exclusion_code"])
    differ = sum(1 for f in both if a[f]["exclusion_code"] != b[f]["exclusion_code"])
    per_stratum = collections.Counter(r["stratum"] for r in frame)
    if merged_n - len(both) != len(frame):
        raise PrismaError("screened minus double-excluded is not the frame")
    return {
        "screened": merged_n,
        "excluded_by_both": {"total": len(both),
                             "same_code": {c: same[c] for c in fulltext.CODES if same[c]},
                             "codes_differ": differ},
        "frame": {"total": len(frame), **{st: per_stratum[st] for st in STRATA}},
    }


def v01_frame_ids(v01_rows: list[dict], tracking: list[dict], frame: list[dict]) -> dict[str, str]:
    """v0.1 paper ID -> frame ID, for the papers with v0.1 rows."""
    papers = sorted({r["paper_id"] for r in v01_rows})
    doi = {r["paper_id"]: r["doi"].strip().lower() for r in tracking}
    by_doi = {r["doi"].strip().lower(): r["frame_id"] for r in frame if r["doi"].strip()}
    out = {}
    for p in papers:
        if not doi.get(p) or doi[p] not in by_doi:
            raise PrismaError(f"{p} has no frame record with its DOI")
        out[p] = by_doi[doi[p]]
    return out


def review_counts(review: list[dict], excluded: set[str]) -> dict:
    decided = {r["frame_id"]: r["decision"] for r in review}
    if set(decided) != excluded:
        raise PrismaError("the author's review does not cover exactly the full-text exclusions")
    c = collections.Counter(decided.values())
    if c["reverse"]:
        raise PrismaError("a reversal must be applied to eligibility.csv before the counts are made")
    return {"reviewed": len(decided), "confirmed": c["confirm"], "reversed": c["reverse"]}


def full_text(plan, log, elig, dups, v01: dict[str, str]) -> dict:
    report = fulltext.walk(plan, log, elig, dups)
    outcome = {r["frame_id"]: r for r in elig}
    taken = {f: st for st in STRATA for f in report[st]["taken_ids"]}
    v01_fids = set(v01.values())
    out = {"drawn": {}, "not_retrieved": {}, "assessed": {}, "excluded": {}, "eligible": {},
           "excluded_codes": {}, "frame_duplicate": {}, "stopped": {}, "target": {}, "cap": {}}
    for st in STRATA:
        s = report[st]
        if not s["stopped"]:
            raise PrismaError(f"the {st} walk has not stopped")
        codes = collections.Counter(outcome[f]["exclusion_code"] for f in s["taken_ids"]
                                    if f in outcome and outcome[f]["eligible"] == "false")
        out["drawn"][st] = s["taken"]
        out["not_retrieved"][st] = s["not_retrieved"]
        out["frame_duplicate"][st] = s["frame_duplicate"]
        out["assessed"][st] = s["assessed"]
        out["eligible"][st] = s["eligible"]
        out["excluded"][st] = s["assessed"] - s["eligible"]
        out["excluded_codes"][st] = {c: codes[c] for c in fulltext.CODES if codes[c]}
        out["stopped"][st] = s["stopped"]
        out["target"][st] = s["target"]
        out["cap"][st] = s["cap"]
    for k in ("drawn", "not_retrieved", "frame_duplicate", "assessed", "excluded", "eligible"):
        out[k]["total"] = sum(out[k][st] for st in STRATA)
    total_codes = collections.Counter()
    for st in STRATA:
        total_codes.update(out["excluded_codes"][st])
    out["excluded_codes"]["total"] = {c: total_codes[c] for c in fulltext.CODES if total_codes[c]}
    out["sample_v01_papers"] = sorted(p for p, f in v01.items() if f in taken)

    # Records retrieved or assessed past a stratum's stop, other than v0.1 papers.
    tried = {r["frame_id"] for r in log if r["file"] == "main.pdf"}
    ahead = sorted(f for f in tried if f not in taken and f not in v01_fids)
    stratum = {p["frame_id"]: p["stratum"] for p in plan}
    out["past_the_stop"] = {
        "tried": len(ahead), "assessed": sum(1 for f in ahead if f in outcome),
        "assessed_eligible": sum(1 for f in ahead if f in outcome and outcome[f]["eligible"] == "true"),
        "strata": dict(sorted(collections.Counter(stratum[f] for f in ahead).items())),
        "frame_ids": ahead}
    return out, taken


def v01_lane(plan, log, elig, v01: dict[str, str], taken: dict[str, str]) -> dict:
    """§7 v0.1 papers: drawn, or not drawn and sought by the same routes."""
    planned = {p["frame_id"]: p for p in plan}
    outcome = {r["frame_id"]: r for r in elig}
    tried: dict[str, set[str]] = {}
    obtained = set()
    for r in log:
        if r["file"] == "main.pdf":
            tried.setdefault(r["frame_id"], set()).add(r["route"])
            if r["outcome"] == "obtained":
                obtained.add(r["frame_id"])
    drawn = sorted(p for p, f in v01.items() if f in taken)
    lane = {"papers": len(v01), "drawn": len(drawn), "drawn_eligible": 0,
            "not_drawn": len(v01) - len(drawn), "retrieved": 0, "not_retrieved": [],
            "awaiting_retrieval": [], "assessed": 0, "eligible": 0, "excluded": 0,
            "excluded_codes": {}, "not_assessed_yet": []}
    codes = collections.Counter()
    for p, f in sorted(v01.items()):
        if f in taken:
            lane["drawn_eligible"] += f in outcome and outcome[f]["eligible"] == "true"
            continue
        rec = planned[f]
        needed = ({"oa"} if rec["route1_url"] else set()) | ({"library"} if rec["route2_url"] else set())
        if f not in obtained:
            (lane["awaiting_retrieval"] if needed - tried.get(f, set()) else lane["not_retrieved"]).append(p)
            continue
        lane["retrieved"] += 1
        if f not in outcome:
            lane["not_assessed_yet"].append(p)
            continue
        lane["assessed"] += 1
        if outcome[f]["eligible"] == "true":
            lane["eligible"] += 1
        else:
            lane["excluded"] += 1
            codes[outcome[f]["exclusion_code"]] += 1
    lane["excluded_codes"] = {c: codes[c] for c in fulltext.CODES if codes[c]}
    return lane


def counts() -> dict:
    merge = json.loads((SEARCH / "merge_counts.json").read_text(encoding="utf-8"))
    ident = identification(merge, sha256(SEARCH / "merged_records.csv"))
    frame = build_frame.read_csv(SEARCH / "frame.csv")
    scr = screening(build_frame.read_csv(SCREEN / "screen_a.csv"),
                    build_frame.read_csv(SCREEN / "screen_b.csv"), frame, ident["merged"])
    plan = fulltext.read(fulltext.PLAN)
    log = fulltext.read(fulltext.LOG)
    elig = fulltext.read(fulltext.ELIG)
    dups = fulltext.read(fulltext.DUPS)
    v01 = v01_frame_ids(build_frame.read_csv(V01_ROWS), build_frame.read_csv(TRACKING), frame)
    ft, taken = full_text(plan, log, elig, dups, v01)
    lane = v01_lane(plan, log, elig, v01, taken)
    excluded = ({f for f in taken if any(r["frame_id"] == f and r["eligible"] == "false" for r in elig)}
                | {f for p, f in v01.items() if f not in taken
                   and any(r["frame_id"] == f and r["eligible"] == "false" for r in elig)})
    review = review_counts(fulltext.read(REVIEW), excluded)
    not_reached = {st: scr["frame"][st] - ft["drawn"][st] for st in STRATA}
    not_reached["total"] = sum(not_reached.values())
    return {
        "protocol": "docs/v1_protocol.md §14 (PRISMA 2020, Page et al. 2021)",
        "identification": ident,
        "screening": scr,
        "walk": {"not_reached": not_reached, **ft},
        "author_review": review,
        "v01_papers": lane,
        "analysed": None,
        "analysed_note": "Per-RQ counts are added when the §11 analyses are run.",
        "inputs_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in (
            SEARCH / "merge_counts.json", SEARCH / "merged_records.csv", SEARCH / "frame.csv",
            SCREEN / "screen_a.csv", SCREEN / "screen_b.csv", fulltext.PLAN, fulltext.LOG,
            fulltext.ELIG, REVIEW, V01_ROWS, TRACKING)},
    }


# ---------------------------------------------------------------- diagram

def n(x: int) -> str:
    return f"{x:,}"


def codes_lines(codes: dict, indent: str = "  ") -> list[str]:
    return [f"{indent}{c}: {n(k)}" for c, k in sorted(codes.items(), key=lambda kv: (-kv[1], kv[0]))]


def box_text(c: dict) -> dict[str, list[str]]:
    i, s, w, v, r = c["identification"], c["screening"], c["walk"], c["v01_papers"], c["author_review"]
    ex = s["excluded_by_both"]
    pts = w["past_the_stop"]
    def st(d):
        return f"S1: {n(d['S1'])}   S2: {n(d['S2'])}"

    pending = len(v["awaiting_retrieval"]) + len(v["not_assessed_yet"])
    v01_status = [f"Not retrieved: {len(v['not_retrieved'])}"]
    if v["not_retrieved"]:
        v01_status.append("  (legacy_v0.1_not_retrieved)")
    if v["awaiting_retrieval"]:
        v01_status.append(f"Retrieval not finished: {len(v['awaiting_retrieval'])}")
    if v["not_assessed_yet"]:
        v01_status.append(f"Retrieved, not yet assessed: {len(v['not_assessed_yet'])}")
    return {
        "identified": ["Records identified",
                       f"OpenAlex: {n(i['openalex']['records'])}",
                       (f"  ({i['openalex']['subqueries']} sub-queries, "
                        f"{n(i['openalex']['hits_over_subqueries'])} hits)"),
                       f"Semantic Scholar: {n(i['semantic_scholar']['records'])}"],
        "duplicates": [f"Duplicates removed: {n(i['duplicates_removed']['total'])}",
                       f"  OpenAlex IDs sharing a DOI: {n(i['duplicates_removed']['openalex_ids_sharing_a_doi'])}",
                       f"  Semantic Scholar, same DOI: {n(i['duplicates_removed']['semantic_scholar_matched_by_doi'])}",
                       ("  Semantic Scholar, same title and year: "
                        f"{n(i['duplicates_removed']['semantic_scholar_matched_by_title_and_year'])}")],
        "screened": ["Records screened on title and abstract",
                     f"(two agents): {n(s['screened'])}"],
        "screen_excluded": [f"Excluded by both screeners: {n(ex['total'])}",
                            "  Same code from both:"] + codes_lines(ex["same_code"], "    ")
                           + [f"  Different codes: {n(ex['codes_differ'])}"],
        "frame": ["Sampling frame (§7)", f"{n(s['frame']['total'])}", st(s["frame"])],
        "not_reached": [f"Not reached by the walk: {n(w['not_reached']['total'])}",
                        "  " + st(w["not_reached"]),
                        f"  incl. {v['not_drawn']} v0.1 papers (left)",
                        f"  incl. {pts['tried']} {'/'.join(pts['strata'])} records retrieved past the stop",
                        f"    ({pts['assessed']} assessed), outside the sample"],
        "drawn": ["Reports sought (drawn by the walk)", f"{n(w['drawn']['total'])}", st(w["drawn"])],
        "not_retrieved": [f"Reports not retrieved: {n(w['not_retrieved']['total'])}",
                          "  " + st(w["not_retrieved"])],
        "assessed": ["Reports assessed for eligibility", "(two agents, full text)",
                     f"{n(w['assessed']['total'])}", st(w["assessed"])],
        "ft_excluded": [f"Reports excluded: {n(w['excluded']['total'])}",
                        "  " + st(w["excluded"])] + codes_lines(w["excluded_codes"]["total"]),
        "sample": ["Probability sample: eligible papers",
                   f"{n(w['eligible']['total'])}",
                   f"S1: {w['eligible']['S1']} of target {w['target']['S1']} ({w['stopped']['S1']})",
                   f"S2: {w['eligible']['S2']} of target {w['target']['S2']} ({w['stopped']['S2']})",
                   f"incl. {len(w['sample_v01_papers'])} v0.1 papers"],
        "analysed": ["Analysed (per RQ)", "added when the §11 analyses are run"],
        "v01_in": ["v0.1 papers (previous version)", f"{v['papers']}, all in the frame"],
        "v01_drawn": [f"Drawn by the walk: {v['drawn']}",
                      f"  ({v['drawn_eligible']} eligible; counted in the sample)",
                      f"Not drawn: {v['not_drawn']}",
                      "  sought by the same routes"],
        "v01_assessed": [f"Retrieved: {v['retrieved']}"] + v01_status
                        + [f"Assessed: {v['assessed']}", f"Excluded: {v['excluded']}"]
                        + codes_lines(v["excluded_codes"]),
        "v01_eligible": ["Eligible, not drawn", f"(legacy_v0.1): {v['eligible']}",
                         "secondary analyses and RQ3"],
        "footnote": [f"Author's review (§6): {r['reviewed']} full-text exclusions reviewed, "
                     f"{r['confirmed']} confirmed, {r['reversed']} reversed."
                     + (f" {pending} v0.1 paper(s) still in progress." if pending else "")],
    }


def draw(c: dict, out_dir: Path) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    matplotlib.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7,
                                "svg.hashsalt": "hycan", "pdf.fonttype": 42})
    t = box_text(c)
    line = 0.15            # inches per text line
    pad = 0.08
    gap = 0.28
    lanes = {"label": (0.10, 0.30), "v01": (0.55, 2.15), "main": (2.95, 2.25), "right": (5.55, 2.75)}
    rows = [
        ("Identification", {"main": "identified", "right": "duplicates"}),
        ("Screening", {"main": "screened", "right": "screen_excluded"}),
        ("Screening", {"v01": "v01_in", "main": "frame", "right": "not_reached"}),
        ("Screening", {"v01": "v01_drawn", "main": "drawn", "right": "not_retrieved"}),
        ("Screening", {"v01": "v01_assessed", "main": "assessed", "right": "ft_excluded"}),
        ("Included", {"v01": "v01_eligible", "main": "sample"}),
        ("Included", {"main": "analysed"}),
    ]
    heights = [max(len(t[k]) for k in r.values()) * line + 2 * pad for _, r in rows]
    width = lanes["right"][0] + lanes["right"][1] + 0.10
    height = sum(heights) + gap * (len(rows) - 1) + 0.25 + 0.45
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")

    pos: dict[str, tuple[float, float, float, float]] = {}
    y = height - 0.25
    spans: list[tuple[str, float, float]] = []
    for (stage, row), h in zip(rows, heights):
        for lane, key in row.items():
            x, w = lanes[lane]
            h = len(t[key]) * line + 2 * pad
            pos[key] = (x, y - h, w, h)
            ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="square,pad=0",
                                        linewidth=0.6, edgecolor="black",
                                        facecolor="#f2f2f2" if lane == "v01" else "white"))
            centred = lane == "main"
            for j, text in enumerate(t[key]):
                ty = y - pad - (j + 0.5) * line
                ax.text(x + (w / 2 if centred else 0.07), ty, text,
                        ha="center" if centred else "left", va="center",
                        fontweight="bold" if (j == 0 and centred) else "normal")
        h = max(pos[k][3] for k in row.values())
        if spans and spans[-1][0] == stage:
            spans[-1] = (stage, spans[-1][1], y - h)
        else:
            spans.append((stage, y, y - h))
        y -= h + gap

    lx, lw = lanes["label"]
    for stage, top, bottom in spans:
        ax.add_patch(FancyBboxPatch((lx, bottom), lw, top - bottom, boxstyle="square,pad=0",
                                    linewidth=0, facecolor="#cfd8e3"))
        ax.text(lx + lw / 2, (top + bottom) / 2, stage, rotation=90, ha="center", va="center",
                fontweight="bold")

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops={"arrowstyle": "-|>", "lw": 0.6, "color": "black",
                                "shrinkA": 0, "shrinkB": 0, "mutation_scale": 7})

    def down(a, b):
        xa, ya, wa, _ = pos[a]
        _, yb, _, hb = pos[b]
        arrow(xa + wa / 2, ya, xa + wa / 2, yb + hb)

    def side(a, b):
        xa, ya, wa, ha = pos[a]
        xb, _, _, hb = pos[b]
        top = ya + ha
        arrow(xa + wa, top - min(ha, hb) / 2, xb, top - min(ha, hb) / 2)

    for a, b in (("identified", "screened"), ("screened", "frame"), ("frame", "drawn"),
                 ("drawn", "assessed"), ("assessed", "sample"), ("sample", "analysed"),
                 ("v01_in", "v01_drawn"), ("v01_drawn", "v01_assessed"),
                 ("v01_assessed", "v01_eligible")):
        down(a, b)
    for a, b in (("identified", "duplicates"), ("screened", "screen_excluded"),
                 ("frame", "not_reached"), ("drawn", "not_retrieved"), ("assessed", "ft_excluded")):
        side(a, b)
    ax.text(0.10, 0.22, t["footnote"][0], ha="left", va="center", fontsize=6.5)

    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / "prisma_flow.pdf", out_dir / "prisma_flow.png"]
    fig.savefig(paths[0], metadata={"CreationDate": None, "ModDate": None, "Producer": None,
                                    "Creator": None})
    fig.savefig(paths[1], dpi=300, metadata={"Software": None})
    plt.close(fig)
    return paths


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    args = ap.parse_args(argv)
    c = counts()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "prisma_counts.json").write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")
    for p in draw(c, args.out):
        print(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
