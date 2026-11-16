"""The PRISMA 2020 flow counts (protocol §14), assembled from committed
artifacts only — nothing here recounts raw data.

Sources: ``references/v1_search/merge_counts.json`` (identified, merged),
``references/v1_screening/screening_counts.json`` (screened),
``references/v1_search/frame_counts.json`` (excluded at screening, frame per
stratum), ``references/v1_fulltext/walk.json`` (drawn, retrieved, assessed,
eligible per stratum), ``references/v1_extraction/papers.csv`` (the v0.1
other-methods arm) and the ``references/v1_analysis`` outputs (analysed per
RQ). Writes ``references/v1_analysis/prisma.json``.

    python3 scripts/v1_search/prisma.py [--out references/v1_analysis]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def counts(out_dir: Path) -> dict:
    merge = json.loads(
        (ROOT / "references" / "v1_search" / "merge_counts.json").read_text())
    frame = json.loads(
        (ROOT / "references" / "v1_search" / "frame_counts.json").read_text())
    walk = json.loads(
        (ROOT / "references" / "v1_fulltext" / "walk.json").read_text())
    with (ROOT / "references" / "v1_extraction" / "papers.csv").open(
        newline="", encoding="utf-8"
    ) as fh:
        papers = list(csv.DictReader(fh))

    v01 = [r for r in papers if r["v01_paper"] == "true"]
    v01_routes: dict[str, int] = {}
    for r in v01:
        v01_routes[r["selection_route"]] = v01_routes.get(
            r["selection_route"], 0) + 1

    def rq(name: str) -> dict:
        return json.loads((out_dir / f"{name}.json").read_text())

    rq3_values = list(csv.DictReader(
        (out_dir / "rq3_values.csv").open(newline="", encoding="utf-8")))
    analysed = {
        "rq1_primary": {
            "papers": rq("rq1")["primary"]["n_papers"],
            "samples": rq("rq1")["primary"]["n_samples"],
        },
        "rq2_primary": {
            "papers": rq("rq2")["primary"]["a_bet"]["n_papers"],
            "samples": rq("rq2")["primary"]["a_bet"]["n_samples"],
        },
        "rq3": {
            "materials_with_2plus_labs": len(rq("rq3")["materials"]),
        },
        "rq4": {
            "papers": rq("rq4")["items"]["a"]["n_domain"],
        },
        "rq5_primary": {
            "papers": rq("rq5")["primary"]["n_papers"],
            "rows": rq("rq5")["primary"]["n_rows"],
        },
        "rq3_laboratory_values": len(rq3_values),
    }

    return {
        "identification": {
            "openalex_records": merge["openalex_unique"],
            "semantic_scholar_records": merge["s2_records"],
            "merged_unique_records": merge["merged_total"],
        },
        "screening": {
            "screened": merge["merged_total"],
            "excluded_by_double_screen": frame["double_excluded"],
            "frame": {"total": frame["frame"], "S1": frame["frame_S1"],
                      "S2": frame["frame_S2"]},
        },
        "sampling": {
            h: {
                "drawn": walk[h]["taken"],
                "not_retrieved": walk[h]["not_retrieved"],
                "frame_duplicate": walk[h]["frame_duplicate"],
                "assessed": walk[h]["assessed"],
                "ineligible": walk[h]["assessed"] - walk[h]["eligible"],
                "eligible": walk[h]["eligible"],
                "stopped": walk[h]["stopped"],
            }
            for h in ("S1", "S2")
        },
        "other_methods_v01_corpus": {
            "v01_papers": len(v01),
            "by_route": dict(sorted(v01_routes.items())),
        },
        "analysed": analysed,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "references" / "v1_analysis"))
    args = ap.parse_args(argv)
    out_dir = Path(args.out)
    report = counts(out_dir)
    (out_dir / "prisma.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    s = report["sampling"]
    print(f"merged {report['identification']['merged_unique_records']}, "
          f"frame {report['screening']['frame']['total']} "
          f"(S1 {report['screening']['frame']['S1']}, "
          f"S2 {report['screening']['frame']['S2']})")
    for h in ("S1", "S2"):
        print(f"{h}: drawn {s[h]['drawn']}, assessed {s[h]['assessed']}, "
              f"eligible {s[h]['eligible']}")
    print(f"analysed: {report['analysed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
