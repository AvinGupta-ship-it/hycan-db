"""Retrieved and not-retrieved records compared (docs/v1_protocol.md §8).

§8: "Retrieved and not-retrieved records are compared on year, publisher,
open-access status and stratum, and the comparison is reported."

The records compared are the records the §7 walk took in each stratum
(`fulltext.walk`, from the committed plan, retrieval log and eligibility
outcomes). A taken record is retrieved when its main text was obtained by
one of the two §8 routes, and `not_retrieved` otherwise; frame duplicates
(none were found) would be left out. The comparison is descriptive: counts
and shares, and the median and quartiles of the year. No test was
pre-specified, and none is computed.

  year       publication year from the merged search record; also split at
             the protocol's period boundary (<= 2015, >= 2016, §11 RQ4)
  publisher  the top organization of the OpenAlex source's host lineage
             (primary_location.source.host_organization_lineage_names, last
             entry), from the archived search responses; publishers with
             fewer than 5 taken records are pooled as "other"; a record with
             no OpenAlex work or no source is "not in OpenAlex" or "no source"
  oa_status  OpenAlex open_access.oa_status of the merged record (gold,
             diamond, hybrid, bronze, green, closed); "not in OpenAlex" when
             the record came from Semantic Scholar only
  stratum    S1 or S2

Writes references/v1_fulltext/retrieval_comparison.json and prints the
tables as Markdown.
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
import build_frame
import merge_search

_spec = importlib.util.spec_from_file_location("fulltext", HERE / "fulltext.py")
fulltext = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fulltext)

OUT = fulltext.FULLTEXT / "retrieval_comparison.json"
OA_ORDER = ("gold", "diamond", "hybrid", "bronze", "green", "closed", "not in OpenAlex")
MIN_PUBLISHER = 5


def publishers() -> dict[str, str]:
    """OpenAlex work id -> top organization of its source's host lineage."""
    out: dict[str, str] = {}
    for f in merge_search.batch_files("hycan_v1_openalex_"):
        data = merge_search.read_json(f)
        for q in data["batch"]:
            for page in q["pages"]:
                for w in merge_search.checked_body(page).get("results") or []:
                    src = (w.get("primary_location") or {}).get("source") or {}
                    names = src.get("host_organization_lineage_names") or []
                    name = names[-1] if names else (src.get("host_organization_name") or "")
                    out[w["id"].rsplit("/", 1)[-1]] = name or "no source"
    return out


def quartiles(years: list[int]) -> dict:
    if not years:
        return {"n": 0}
    q = statistics.quantiles(years, n=4, method="inclusive") if len(years) > 1 else [years[0]] * 3
    return {"n": len(years), "median": statistics.median(years), "q1": q[0], "q3": q[2],
            "min": min(years), "max": max(years)}


def records(plan, log, elig, dups, merged, pubs) -> list[dict]:
    report = fulltext.walk(plan, log, elig, dups)
    obtained = {r["frame_id"]: r["route"] for r in log
                if r["file"] == "main.pdf" and r["outcome"] == "obtained"}
    dup = {r["frame_id"] for r in dups}
    out = []
    for st in ("S1", "S2"):
        for fid in report[st]["taken_ids"]:
            if fid in dup:
                continue
            m = merged[fid]
            oa_id = (m["openalex_id"] or "").rsplit("/", 1)[-1]
            out.append({
                "frame_id": fid, "stratum": st,
                "retrieved": fid in obtained,
                "route": obtained.get(fid, ""),
                "year": int(m["year"]) if m["year"] else None,
                "publisher": pubs.get(oa_id, "no source") if oa_id else "not in OpenAlex",
                "oa_status": (m["oa_status"] or "unknown") if oa_id else "not in OpenAlex",
            })
    return out


def table(recs: list[dict], key, order=None) -> list[dict]:
    groups = {True: collections.Counter(), False: collections.Counter()}
    for r in recs:
        groups[r["retrieved"]][key(r)] += 1
    n = {g: sum(c.values()) for g, c in groups.items()}
    cats = list(order) if order else sorted(set(groups[True]) | set(groups[False]),
                                           key=lambda c: (-(groups[True][c] + groups[False][c]), c))
    rows = []
    for c in cats:
        a, b = groups[True][c], groups[False][c]
        if order and a == b == 0:
            continue
        rows.append({"category": c, "retrieved": a, "not_retrieved": b,
                     "retrieved_share": round(a / n[True], 4) if n[True] else None,
                     "not_retrieved_share": round(b / n[False], 4) if n[False] else None,
                     "retrieved_fraction": round(a / (a + b), 4)})
    return rows


def compare(recs: list[dict]) -> dict:
    count = collections.Counter(r["publisher"] for r in recs)
    pooled = {p for p, k in count.items()
              if k < MIN_PUBLISHER and p not in ("not in OpenAlex", "no source")}
    pub = lambda r: "other" if r["publisher"] in pooled else r["publisher"]
    period = lambda r: ("unknown" if r["year"] is None
                        else "<= 2015" if r["year"] <= 2015 else ">= 2016")
    years = {g: [r["year"] for r in recs if r["retrieved"] is g and r["year"] is not None]
             for g in (True, False)}
    return {
        "n": {"retrieved": sum(r["retrieved"] for r in recs),
              "not_retrieved": sum(not r["retrieved"] for r in recs)},
        "retrieved_by_route": dict(collections.Counter(r["route"] for r in recs if r["retrieved"])),
        "stratum": table(recs, lambda r: r["stratum"], ("S1", "S2")),
        "year": {"retrieved": quartiles(years[True]), "not_retrieved": quartiles(years[False])},
        "period": table(recs, period, ("<= 2015", ">= 2016", "unknown")),
        "publisher": table(recs, pub),
        "publishers_pooled_as_other": sorted(pooled),
        "oa_status": table(recs, lambda r: r["oa_status"], OA_ORDER + ("unknown",)),
    }


def markdown(c: dict) -> str:
    by = c["retrieved_by_route"]
    head = (f"Retrieved {c['n']['retrieved']} (route 1, open access: {by.get('oa', 0)}; route 2, "
            f"library: {by.get('library', 0)}), not retrieved {c['n']['not_retrieved']}.")
    lines = [head, ""]
    y = c["year"]
    for g in ("retrieved", "not_retrieved"):
        q = y[g]
        lines.append(f"- Year, {g.replace('_', ' ')}: median {q['median']:g}, quartiles "
                     f"{q['q1']:g}–{q['q3']:g}, range {q['min']}–{q['max']} (n = {q['n']})")
    for name in ("stratum", "period", "publisher", "oa_status"):
        lines += ["", f"| {name} | retrieved | not retrieved | share retrieved |", "|---|---|---|---|"]
        for r in c[name]:
            lines.append(f"| {r['category']} | {r['retrieved']} ({r['retrieved_share']:.0%}) | "
                         f"{r['not_retrieved']} ({r['not_retrieved_share']:.0%}) | "
                         f"{r['retrieved_fraction']:.0%} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.parse_args(argv)
    merged = {r["frame_id"]: r for r in build_frame.load_merged(fulltext.SEARCH)}
    recs = records(fulltext.read(fulltext.PLAN), fulltext.read(fulltext.LOG),
                   fulltext.read(fulltext.ELIG), fulltext.read(fulltext.DUPS), merged, publishers())
    c = compare(recs)
    OUT.write_text(json.dumps({"protocol": "docs/v1_protocol.md §8", "comparison": c,
                               "records": recs}, indent=2) + "\n", encoding="utf-8")
    print(markdown(c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
