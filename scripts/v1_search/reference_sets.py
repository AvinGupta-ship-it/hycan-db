"""Reference sets A and B and the recall check (docs/v1_protocol.md §5, §6 and
§15 Amendment 1, item 9).

  setb-input   from the two OpenAlex lookup files (the citing paper by DOI, and
               its referenced works by OpenAlex ID, both written by
               scripts/v1_search/openalex_lookup.js), re-check every stored
               response body against its SHA-256 and write the screening input
               for the referenced works:
                 <dir>/screen_input.csv   frame_id (the OpenAlex ID), title,
                                          abstract, venue, year, type
                 <dir>/records.csv        frame_id, doi (not shown to the
                                          screeners)
                 <dir>/setb_input.json    counts, the citing record and the
                                          SHA-256 of every file
  setb-build   from the two screeners' files in <dir> (screen_a.csv,
               screen_b.csv, in the main screening's format), write
                 <dir>/set_b.csv          the records not excluded by both
                                          screeners (Amendment 1, item 9), with
                                          has_abstract and include_both
                 <dir>/setb_counts.json   counts and Cohen's kappa
  recall       from the merged search (references/v1_search/merged_records.csv)
               report recall on set A (Appendix B) and on set B and its
               both-include subset, each split by whether OpenAlex holds an
               abstract, with the reason for every miss (§5): not indexed;
               indexed without abstract; indexed with abstract but not matched.

Every output depends only on the inputs, so a re-run reproduces it byte for
byte.

    (the two files from openalex_lookup.js hycanReferencedWorks)
    python3 scripts/v1_search/reference_sets.py setb-input CITING.json REFS.json
        --doi 10.1016/j.ijhydene.2026.156054 --out references/v1_setB
    python3 scripts/v1_search/reference_sets.py setb-build --dir references/v1_setB
    python3 scripts/v1_search/reference_sets.py recall
        --merged references/v1_search/merged_records.csv
        --set-a-lookup references/v1_pilot/hycan_v1_lookup_v01_pilot.json
        --setb references/v1_setB --out references/v1_search/recall.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from merge_search import (
    abstract_from_inverted,
    checked_body,
    norm_doi,
    norm_title,
)

ROOT = Path(__file__).resolve().parents[2]
SCREEN_COLUMNS = ("frame_id", "title", "abstract", "venue", "year", "type")
SETB_COLUMNS = ("frame_id", "doi", "title", "year", "has_abstract", "include_both")
# Appendix B of the protocol.
SET_A = tuple(
    f"HYC-{n}"
    for n in [
        "0001",
        "0004",
        "0005",
        "0007",
        "0009",
        "0012",
        "0013",
        "0016",
        "0017",
        "0018",
        "0019",
        "0020",
        "0021",
        "0022",
        "0023",
        "0024",
        "0026",
        "0029",
        "0031",
        "0032",
        "0033",
        "0034",
        "0037",
        "0040",
        "0041",
        "0042",
        "0043",
        "0044",
        "0045",
        "0046",
        "0047",
        "0048",
        "0049",
        "0050",
        "0052",
        "0053",
        "0057",
        "0058",
        "0060",
        "0061",
        "0062",
        "0063",
        "0064",
        "0065",
    ]
)


class SetError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lookup_records(path: Path) -> list[dict]:
    """Every work in a lookup file, after the SHA-256 check of each page."""
    data = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for page in data["pages"]:
        out.extend(checked_body(page).get("results", []))
    return out


def bare_id(openalex_id: str) -> str:
    return (openalex_id or "").replace("https://openalex.org/", "")


def venue(rec: dict) -> str:
    src = ((rec.get("primary_location") or {}).get("source")) or {}
    return src.get("display_name") or ""


def write_csv(path: Path, columns, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(columns), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def cmd_setb_input(args) -> int:
    citing_path, refs_path, out = Path(args.citing), Path(args.refs), Path(args.out)
    citing = [
        r
        for r in lookup_records(citing_path)
        if norm_doi(r.get("doi")) == norm_doi(args.doi)
    ]
    if len(citing) != 1:
        raise SetError(f"expected one record for {args.doi}, found {len(citing)}")
    cited_ids = sorted({bare_id(i) for i in citing[0].get("referenced_works", [])})
    if not cited_ids:
        raise SetError("the citing record lists no referenced works")
    recs = {}
    for r in lookup_records(refs_path):
        recs.setdefault(bare_id(r["id"]), r)
    requested = set(json.loads(refs_path.read_text(encoding="utf-8")).get("ids", []))
    if requested and requested != set(cited_ids):
        raise SetError(
            "the reference lookup did not request exactly the referenced works"
        )
    rows, ids = [], []
    for wid in cited_ids:
        r = recs.get(wid)
        if r is None:
            continue
        ids.append({"frame_id": wid, "doi": norm_doi(r.get("doi")) or ""})
        rows.append(
            {
                "frame_id": wid,
                "title": r.get("display_name") or r.get("title") or "",
                "abstract": abstract_from_inverted(r.get("abstract_inverted_index")),
                "venue": venue(r),
                "year": r.get("publication_year") or "",
                "type": r.get("type") or "",
            }
        )
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "screen_input.csv", SCREEN_COLUMNS, rows)
    write_csv(out / "records.csv", ("frame_id", "doi"), ids)
    manifest = {
        "citing_doi": norm_doi(args.doi),
        "citing_openalex_id": bare_id(citing[0]["id"]),
        "citing_title": citing[0].get("display_name"),
        "referenced_works": len(cited_ids),
        "records_returned": len(rows),
        "not_returned": [w for w in cited_ids if w not in recs],
        "without_abstract": sum(1 for r in rows if not r["abstract"]),
        "inputs": {
            citing_path.name: sha256_file(citing_path),
            refs_path.name: sha256_file(refs_path),
        },
        "screen_input_sha256": sha256_file(out / "screen_input.csv"),
    }
    (out / "setb_input.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({k: v for k, v in manifest.items() if k != "inputs"}, indent=2))
    return 0


def cohen_kappa(a: list[bool], b: list[bool]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else (po - pe) / (1 - pe)


def cmd_setb_build(args) -> int:
    d = Path(args.dir)
    inputs = {r["frame_id"]: r for r in read_csv(d / "screen_input.csv")}
    screens = {}
    for name in ("screen_a.csv", "screen_b.csv"):
        rows = {r["frame_id"]: r for r in read_csv(d / name)}
        if set(rows) != set(inputs):
            raise SetError(f"{name} does not screen exactly the input records")
        screens[name] = rows
    a, b = screens["screen_a.csv"], screens["screen_b.csv"]
    dois = {r["frame_id"]: r["doi"] for r in read_csv(d / "records.csv")}
    out_rows = []
    for fid in sorted(inputs):
        if a[fid]["decision"] == b[fid]["decision"] == "exclude":
            continue
        out_rows.append(
            {
                "frame_id": fid,
                "doi": dois.get(fid, ""),
                "title": inputs[fid]["title"],
                "year": inputs[fid]["year"],
                "has_abstract": "true" if inputs[fid]["abstract"].strip() else "false",
                "include_both": "true"
                if a[fid]["decision"] == b[fid]["decision"] == "include"
                else "false",
            }
        )
    write_csv(d / "set_b.csv", SETB_COLUMNS, out_rows)
    keep_a = [a[f]["decision"] != "exclude" for f in sorted(inputs)]
    keep_b = [b[f]["decision"] != "exclude" for f in sorted(inputs)]
    counts = {
        "screened": len(inputs),
        "set_b": len(out_rows),
        "set_b_without_abstract": sum(r["has_abstract"] == "false" for r in out_rows),
        "include_both": sum(r["include_both"] == "true" for r in out_rows),
        "excluded_by_both": len(inputs) - len(out_rows),
        "kappa_keep_vs_exclude": cohen_kappa(keep_a, keep_b),
        "set_b_sha256": sha256_file(d / "set_b.csv"),
    }
    (d / "setb_counts.json").write_text(json.dumps(counts, indent=2) + "\n")
    print(json.dumps(counts, indent=2))
    return 0


def _merged_index(merged: list[dict]):
    by_oa = {r["openalex_id"]: r for r in merged if r.get("openalex_id")}
    by_doi = {norm_doi(r["doi"]): r for r in merged if r.get("doi")}
    by_title: dict[str, list[dict]] = {}
    for r in merged:
        by_title.setdefault(norm_title(r.get("title")), []).append(r)
    return by_oa, by_doi, by_title


def _found(ref: dict, index) -> bool:
    by_oa, by_doi, by_title = index
    if ref.get("openalex_id") and bare_id(ref["openalex_id"]) in {
        bare_id(k) for k in by_oa
    }:
        return True
    if ref.get("doi") and norm_doi(ref["doi"]) in by_doi:
        return True
    for r in by_title.get(norm_title(ref.get("title")), []):
        try:
            if abs(int(r.get("year") or 0) - int(ref.get("year") or 0)) <= 1:
                return True
        except ValueError:
            continue
    return False


def recall_block(refs: list[dict], index) -> dict:
    """refs: dicts with openalex_id, doi, title, year, indexed, has_abstract."""
    found = [r for r in refs if _found(r, index)]
    misses = [r for r in refs if not _found(r, index)]

    def share(rows, sub):
        return None if not rows else len(sub) / len(rows)

    out = {
        "n": len(refs),
        "found": len(found),
        "recall": share(refs, found),
        "misses": [],
    }
    for flag in (True, False):
        part = [r for r in refs if r["has_abstract"] is flag]
        hit = [r for r in part if _found(r, index)]
        key = "with_abstract" if flag else "without_abstract"
        out[key] = {"n": len(part), "found": len(hit), "recall": share(part, hit)}
    for r in misses:
        reason = (
            "not indexed"
            if not r["indexed"]
            else "indexed without abstract"
            if not r["has_abstract"]
            else "indexed with abstract but not matched"
        )
        out["misses"].append({"id": r["id"], "title": r.get("title"), "reason": reason})
    return out


def cmd_recall(args) -> int:
    merged = read_csv(Path(args.merged))
    index = _merged_index(merged)
    # set A: the Appendix B papers, with their OpenAlex records from the lookup
    v01 = {}
    with (ROOT / "data" / "raw" / "measurements_v0.1.csv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            v01.setdefault(r["paper_id"], r)
    oa = {norm_doi(r.get("doi")): r for r in lookup_records(Path(args.set_a_lookup))}
    set_a = []
    for pid in SET_A:
        doi = norm_doi(v01[pid]["doi"])
        rec = oa.get(doi)
        set_a.append(
            {
                "id": pid,
                "openalex_id": bare_id(rec["id"]) if rec else "",
                "doi": doi,
                "title": (rec or {}).get("display_name") or v01[pid]["title"],
                "year": (rec or {}).get("publication_year") or v01[pid]["year"],
                "indexed": rec is not None,
                "has_abstract": bool(rec and rec.get("abstract_inverted_index")),
            }
        )
    d = Path(args.setb)
    set_b_rows = read_csv(d / "set_b.csv")
    set_b = [
        {
            "id": r["frame_id"],
            "openalex_id": r["frame_id"],
            "doi": r.get("doi", ""),
            "title": r["title"],
            "year": r["year"],
            "indexed": True,
            "has_abstract": r["has_abstract"] == "true",
            "include_both": r["include_both"] == "true",
        }
        for r in set_b_rows
    ]
    report = {
        "merged_sha256": sha256_file(Path(args.merged)),
        "set_a": recall_block(set_a, index),
        "set_b": recall_block(set_b, index),
        "set_b_include_both": recall_block(
            [r for r in set_b if r["include_both"]], index
        ),
    }
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {k: (v["recall"] if isinstance(v, dict) else v) for k, v in report.items()},
            indent=2,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("setb-input")
    p.add_argument("citing")
    p.add_argument("refs")
    p.add_argument("--doi", required=True)
    p.add_argument("--out", required=True)
    b = sub.add_parser("setb-build")
    b.add_argument("--dir", required=True)
    r = sub.add_parser("recall")
    r.add_argument("--merged", required=True)
    r.add_argument("--set-a-lookup", required=True)
    r.add_argument("--setb", required=True)
    r.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        return {
            "setb-input": cmd_setb_input,
            "setb-build": cmd_setb_build,
            "recall": cmd_recall,
        }[args.cmd](args)
    except SetError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
