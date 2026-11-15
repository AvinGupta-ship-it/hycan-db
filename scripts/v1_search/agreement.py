"""Agreement statistics of the v1.0 extraction run (docs/v1_protocol.md §9).

Runs scripts/v1_agreement.py over every extracted paper in the collected tree
(references/v1_extraction/) and writes the summaries §9 asks for — dual papers
(extractor A against extractor B), separately the legacy B-only papers (the
v0.1 rows against extractor B), and the comparison of each sampled v0.1
paper's v0.1 rows with its reconciled rows — each with per-paper counts:

    references/v1_extraction/agreement_dual.json
    references/v1_extraction/agreement_legacy.json
    references/v1_extraction/agreement_v01_sample.json

The collected tree holds no copy of the v0.1 rows (they are the dataset,
data/raw/measurements_v0.1.csv), so for a legacy paper the first row set is
staged from that file, with the paper's labels.csv and resolutions.csv, in the
layout v1_agreement.py reads. Staging is in a temporary directory; nothing in
the repository is modified.

    python3 scripts/v1_search/agreement.py [--tree references/v1_extraction]
        [--v01 data/raw/measurements_v0.1.csv]
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / f"{name}.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ve = _load("v1_extract")
ag = _load("v1_agreement")

PER_PAPER_KEYS = (
    "paper", "rows_first", "rows_second", "matched_pairs",
    "only_first", "only_second", "curves",
)


def stage_legacy(paper_dir: Path, stage: Path, cols: list[str], rows: list[dict]) -> Path:
    """One legacy paper in the layout v1_agreement.py reads: the paper's v0.1
    rows as V/rows.csv, extractor B's rows, and C's labels and resolutions."""
    d = stage / paper_dir.name
    (d / "V").mkdir(parents=True)
    (d / "B").mkdir()
    (d / "C").mkdir()
    ve.write_csv(d / "V" / "rows.csv", cols, rows)
    (d / "B" / "rows.csv").symlink_to(paper_dir / "B" / "rows.csv")
    (d / "C" / "labels.csv").symlink_to(paper_dir / "C_input" / "labels.csv")
    (d / "C" / "resolutions.csv").symlink_to(paper_dir / "C" / "resolutions.csv")
    return d


def stage_v01_sample(paper_dir: Path, stage: Path, cols: list[str], rows: list[dict]) -> Path:
    """One sampled v0.1 paper for the §9 comparison of its v0.1 rows with the
    reconciled rows. The v0.1 samples' printed labels come from the paper's
    comparison labeller run (L_compare/, the frozen legacy_labels prompt); no
    resolutions file is staged, so no C outcomes are counted."""
    d = stage / paper_dir.name
    (d / "V").mkdir(parents=True)
    (d / "C").mkdir()
    ve.write_csv(d / "V" / "rows.csv", cols, rows)
    (d / "C" / "rows.csv").symlink_to(paper_dir / "C" / "rows.csv")
    (d / "C" / "labels.csv").symlink_to(paper_dir / "L_compare" / "labels.csv")
    return d


def report(papers: list[dict]) -> dict:
    return {
        "summary": ag.summarize(papers),
        "papers": [{k: p[k] for k in PER_PAPER_KEYS if k in p} for p in papers],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", default=str(ROOT / "references" / "v1_extraction"))
    ap.add_argument("--v01", default=str(ROOT / "data" / "raw" / "measurements_v0.1.csv"))
    args = ap.parse_args(argv)
    tree = Path(args.tree)
    kinds = ag.field_kinds()
    v01_cols, v01_rows = ve.read_rows(Path(args.v01))

    with tree.joinpath("papers.csv").open(newline="", encoding="utf-8") as fh:
        papers = sorted(csv.DictReader(fh), key=lambda r: r["paper_id"])

    dual, legacy, v01_sample = [], [], []
    with tempfile.TemporaryDirectory() as tmp:
        for p in papers:
            pid, paper_dir = p["paper_id"], tree / p["paper_id"]
            if p["mode"] == "none":
                continue
            mine = [r for r in v01_rows if r.get("paper_id") == pid]
            if p["mode"] == "legacy" or p.get("v01_paper") == "true":
                if not mine:
                    print(f"REFUSED: no v0.1 rows for {pid}", file=sys.stderr)
                    return 1
            if p["mode"] == "dual":
                dual.append(ag.paper_stats(paper_dir, kinds, "A", "B"))
                if p.get("v01_paper") == "true":
                    staged = stage_v01_sample(paper_dir, Path(tmp) / "v01s", v01_cols, mine)
                    v01_sample.append(
                        ag.paper_stats(staged, kinds, "V", "C", legacy=True)
                    )
            elif p["mode"] == "legacy":
                staged = stage_legacy(paper_dir, Path(tmp), v01_cols, mine)
                legacy.append(ag.paper_stats(staged, kinds, "V", "B", legacy=True))

    for name, group in (("agreement_dual", dual), ("agreement_legacy", legacy),
                        ("agreement_v01_sample", v01_sample)):
        out = report(group)
        tree.joinpath(f"{name}.json").write_text(
            json.dumps(out, indent=2) + "\n", encoding="utf-8"
        )
        s = out["summary"]
        print(
            f"{name}: {s['papers']} papers, {s['matched_pairs']} matched pairs, "
            f"row detection {s['row_detection_agreement']:.3f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
