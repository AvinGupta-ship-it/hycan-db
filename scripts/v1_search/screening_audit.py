"""The author's audit of double-excluded records (docs/v1_protocol.md §6).

  make   draws a simple random sample of 100 records excluded by both
         screeners (all of them, if fewer) with
         numpy.random.default_rng(20261031).choice, without replacement, from
         those records sorted by frame_id, and writes a blind audit sheet: the
         title, venue, year and abstract of each, with no screening decision.
  score  reads the completed sheet and reports the share the author would
         include, with an exact (Clopper-Pearson) 95% CI: the estimated
         false-exclusion rate.

The author fills `author_decision` with include or exclude in the sheet.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_frame

ROOT = build_frame.ROOT
SEED = 20261031
SAMPLE_SIZE = 100
DOUBLE_EXCLUDED = "references/v1_screening/double_excluded.csv"
SHEET = "references/v1_screening/author_audit_sheet.csv"
SHEET_COLUMNS = (
    "audit_order",
    "frame_id",
    "title",
    "venue",
    "year",
    "abstract",
    "author_decision",
    "author_note",
)


def draw(frame_ids_sorted: list[str]) -> list[str]:
    n = len(frame_ids_sorted)
    idx = np.random.default_rng(SEED).choice(n, size=min(SAMPLE_SIZE, n), replace=False)
    return [frame_ids_sorted[i] for i in idx]


def clopper_pearson(k: int, n: int, level: float = 0.95) -> tuple[float, float]:
    a = (1 - level) / 2
    lo = 0.0 if k == 0 else float(beta.ppf(a, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - a, k + 1, n - k))
    return lo, hi


def make(root: Path = ROOT) -> bytes:
    ids = [r["frame_id"] for r in build_frame.read_csv(root / DOUBLE_EXCLUDED)]
    if ids != sorted(ids):
        raise RuntimeError("double_excluded.csv is not sorted by frame_id")
    merged = {
        r["frame_id"]: r
        for r in build_frame.read_csv(root / "references/v1_search/merged_records.csv")
    }
    rows = []
    for order, fid in enumerate(draw(ids), 1):
        m = merged[fid]
        rows.append(
            {
                "audit_order": str(order),
                "frame_id": fid,
                "title": m["title"],
                "venue": m["venue"],
                "year": m["year"],
                "abstract": m["abstract"],
                "author_decision": "",
                "author_note": "",
            }
        )
    return build_frame.csv_bytes(SHEET_COLUMNS, rows)


def score(sheet_rows: list[dict[str, str]]) -> dict:
    decisions = [r["author_decision"].strip().lower() for r in sheet_rows]
    bad = [d for d in decisions if d not in ("include", "exclude")]
    if bad:
        raise RuntimeError(f"{len(bad)} rows lack an include/exclude decision")
    k, n = decisions.count("include"), len(decisions)
    lo, hi = clopper_pearson(k, n)
    return {
        "audited": n,
        "author_would_include": k,
        "false_exclusion_rate": k / n if n else None,
        "ci95_clopper_pearson": [lo, hi],
    }


def main(argv: list[str]) -> int:
    if argv[1:] == ["make"]:
        path = ROOT / SHEET
        if path.exists():
            print(f"REFUSED: {SHEET} exists; the draw is made once", file=sys.stderr)
            return 1
        path.write_bytes(make())
        print(f"wrote {SHEET}")
        return 0
    if argv[1:] == ["score"]:
        print(json.dumps(score(build_frame.read_csv(ROOT / SHEET)), indent=2))
        return 0
    print("usage: screening_audit.py make|score", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
