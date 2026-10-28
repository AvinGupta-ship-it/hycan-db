"""Title-and-abstract screening counts (docs/v1_protocol.md §6).

Reads the archived search (references/v1_search/), the two screeners' files
and the frame counts, and writes references/v1_screening/screening_counts.json:

  - the share of records without an abstract per source: OpenAlex (its
    records after DOI duplicates are merged), Semantic Scholar (its records as
    returned) and the merged set (§6, "Reported");
  - each screener's decisions, exclusion codes and strata;
  - the cross-table of the two screeners' decisions;
  - agreement and Cohen's kappa for include-or-uncertain against exclude
    (§6), on all records and separately on records with and without an
    abstract;
  - the frame and double-excluded counts from frame_counts.json.

The output depends only on the inputs, so a re-run reproduces it byte for
byte.

    python3 scripts/v1_search/screening_counts.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_frame
import merge_search

ROOT = HERE.parents[1]
SEARCH = ROOT / "references" / "v1_search"
SCREEN = ROOT / "references" / "v1_screening"


def source_abstracts() -> dict:
    recs, _, _ = merge_search.load_openalex()
    merge_search.collapse_openalex_doi_duplicates(recs)
    oa_none = sum(1 for r in recs.values() if not r["abstract"])
    s2_n = s2_none = 0
    for f in merge_search.batch_files("hycan_v1_semanticscholar"):
        for page in merge_search.read_json(f)["pages"]:
            for p in merge_search.checked_body(page).get("data") or []:
                s2_n += 1
                s2_none += not p.get("abstract")

    def block(n, none):
        return {"records": n, "without_abstract": none, "share": none / n}

    return {"openalex": block(len(recs), oa_none),
            "semantic_scholar": block(s2_n, s2_none)}


def agreement(ids, a, b) -> dict:
    ka = [a[f]["decision"] != "exclude" for f in ids]
    kb = [b[f]["decision"] != "exclude" for f in ids]
    return {
        "records": len(ids),
        "agreement": sum(x == y for x, y in zip(ka, kb)) / len(ids),
        "kappa": build_frame.cohen_kappa(ka, kb),
        "kept_by_a": sum(ka),
        "kept_by_b": sum(kb),
        "kept_by_a_only": sum(x and not y for x, y in zip(ka, kb)),
        "kept_by_b_only": sum(y and not x for x, y in zip(ka, kb)),
        "excluded_by_both": sum(not x and not y for x, y in zip(ka, kb)),
    }


def screener(rows: dict) -> dict:
    v = list(rows.values())
    return {
        "decisions": dict(sorted(Counter(r["decision"] for r in v).items())),
        "exclusion_codes": dict(sorted(Counter(
            r["exclusion_code"] for r in v if r["exclusion_code"]).items())),
        "strata": dict(sorted(Counter(r["stratum"] for r in v if r["stratum"]).items())),
    }


def counts() -> dict:
    merged = build_frame.load_merged(SEARCH)
    ids = sorted(r["frame_id"] for r in merged)
    a = build_frame.load_screen(SCREEN / "screen_a.csv", set(ids))
    b = build_frame.load_screen(SCREEN / "screen_b.csv", set(ids))
    with_abs = {r["frame_id"] for r in merged if r["abstract"].strip()}
    merged_none = len(ids) - len(with_abs)
    frame = json.loads((SEARCH / "frame_counts.json").read_text(encoding="utf-8"))
    return {
        "merged_sha256": build_frame.sha256_file(SEARCH / "merged_records.csv"),
        "screen_a_sha256": build_frame.sha256_file(SCREEN / "screen_a.csv"),
        "screen_b_sha256": build_frame.sha256_file(SCREEN / "screen_b.csv"),
        "without_abstract": {
            **source_abstracts(),
            "merged": {"records": len(ids), "without_abstract": merged_none,
                       "share": merged_none / len(ids)},
        },
        "screener_a": screener(a),
        "screener_b": screener(b),
        "decision_pairs_a_b": {
            f"{x}/{y}": n for (x, y), n in sorted(
                Counter((a[f]["decision"], b[f]["decision"]) for f in ids).items())
        },
        "kept_vs_excluded": {
            "all": agreement(ids, a, b),
            "with_abstract": agreement([f for f in ids if f in with_abs], a, b),
            "without_abstract": agreement([f for f in ids if f not in with_abs], a, b),
        },
        "frame": {k: frame[k] for k in ("frame", "frame_S1", "frame_S2",
                                         "double_excluded", "stratum_tiebreaks",
                                         "frame_sha256")},
    }


def main() -> int:
    try:
        out = counts()
    except build_frame.FrameError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(out, indent=2) + "\n"
    (SCREEN / "screening_counts.json").write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
