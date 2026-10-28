"""Agreement statistics for dual extraction (docs/v1_protocol.md §9).

For one or more papers, each a directory with the two extractions' rows.csv
(in A/ and B/, or in the directories named by --first and --second) and C's
resolutions.csv in C/, reports per field type:
  - categorical fields: exact agreement and Cohen's kappa;
  - numeric fields: the share within printed rounding (table or text values) or
    within 3% relative (figure values), and the distribution of relative
    differences;
  - row detection: matched pairs against rows found by one extractor only;
  - C's outcomes: first kept, second kept, new value, both acceptable, for
    fields, rows and curve-to-sample assignments separately;
  - the curve-to-sample mapping: digitized curves, and the share C did not
    reassign.

Pairs come from the §9 matching in v1_extract.py.

    python3 scripts/v1_agreement.py PAPER_DIR [PAPER_DIR ...] [--json OUT]
        [--first A --second B] [--legacy]
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "v1_extract", Path(__file__).resolve().parent / "v1_extract.py"
)
ve = importlib.util.module_from_spec(_spec)
sys.modules["v1_extract"] = ve
_spec.loader.exec_module(ve)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hycan.schema import MeasurementEntry


def field_kinds() -> dict[str, str]:
    kinds = {}
    for name, f in MeasurementEntry.model_fields.items():
        ann = str(f.annotation)
        if "Literal" in ann or "bool" in ann:
            kinds[name] = "categorical"
        elif "float" in ann or "int" in ann:
            kinds[name] = "numeric"
        else:
            kinds[name] = "text"
    return kinds


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    if pe == 1:
        return None
    return (po - pe) / (1 - pe)


def printed_half_unit(s: str) -> float:
    s = s.strip()
    return 0.5 * 10.0 ** (-(len(s.split(".", 1)[1]) if "." in s else 0))


def numeric_agrees(a: dict, b: dict, field: str) -> tuple[bool, float | None]:
    va, vb = (a.get(field) or "").strip(), (b.get(field) or "").strip()
    fa, fb = ve.to_float(va), ve.to_float(vb)
    if fa is None and fb is None:
        return True, None
    if fa is None or fb is None:
        return False, None
    rel = abs(fa - fb) / max(abs(fa), abs(fb)) if max(abs(fa), abs(fb)) > 0 else 0.0
    if ve.is_digitized(a, field) or ve.is_digitized(b, field):
        return rel <= ve.FIGURE_REL_TOL, rel
    return abs(fa - fb) <= max(
        printed_half_unit(va), printed_half_unit(vb)
    ) + 1e-12, rel


ROW_ITEM = "row"
CURVE_ITEM = "curve_sample_mapping"


def c_outcomes(path: Path) -> dict:
    """C's decisions, split into field decisions, row decisions (`row`) and
    curve-to-sample assignments (`curve_sample_mapping`)."""
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    out = {"fields": Counter(), "rows": Counter(), "curve_sample_mapping": Counter()}
    for r in rows:
        key = {ROW_ITEM: "rows", CURVE_ITEM: "curve_sample_mapping"}.get(
            r.get("field", ""), "fields"
        )
        out[key][r["decision"]] += 1
    return {k: dict(v) for k, v in out.items()}


def n_curves(rows: list[dict]) -> int:
    """Digitized curves of one row set: distinct isotherms among its
    figure_digitized rows (a row without isotherm_id counts on its own)."""
    keys = {
        r.get("isotherm_id") or f"row:{r.get('measurement_id')}"
        for r in rows
        if r.get("extraction_method") == "figure_digitized"
    }
    return len(keys)


def paper_stats(
    paper_dir: Path,
    kinds: dict[str, str],
    first_name: str = "A",
    second_name: str = "B",
    legacy: bool = False,
) -> dict:
    cols, first = ve.read_rows(paper_dir / first_name / "rows.csv")
    _, second = ve.read_rows(paper_dir / second_name / "rows.csv")
    labels = ve.read_labels(paper_dir / "C" / "labels.csv") if legacy else None
    pairs = ve.match(first, second, labels, legacy=legacy)
    matched = [p for p in pairs if p.first is not None and p.second is not None]
    out = {
        "paper": paper_dir.name,
        "rows_first": len(first),
        "rows_second": len(second),
        "matched_pairs": len(matched),
        "only_first": sum(p.second is None for p in pairs),
        "only_second": sum(p.first is None for p in pairs),
        "categorical": {},
        "numeric": {},
    }
    for field in ve.compared_fields(cols):
        kind = kinds.get(field, "text")
        use = [p for p in matched if field in ve.pair_fields(cols, p.first, legacy)]
        if kind == "categorical":
            a = [ve.norm_value(p.first.get(field), field) for p in use]
            b = [ve.norm_value(p.second.get(field), field) for p in use]
            out["categorical"][field] = {"a": a, "b": b}
        elif kind == "numeric":
            res = [numeric_agrees(p.first, p.second, field) for p in use]
            out["numeric"][field] = res
    out["curves"] = max(n_curves(first), n_curves(second))
    res_path = paper_dir / "C" / "resolutions.csv"
    if res_path.exists():
        out["c_outcomes"] = c_outcomes(res_path)
    return out


def summarize(papers: list[dict]) -> dict:
    cat: dict[str, dict] = {}
    num: dict[str, list] = {}
    for p in papers:
        for f, v in p["categorical"].items():
            cat.setdefault(f, {"a": [], "b": []})
            cat[f]["a"] += v["a"]
            cat[f]["b"] += v["b"]
        for f, v in p["numeric"].items():
            num.setdefault(f, []).extend(v)
    summary = {
        "papers": len(papers),
        "rows_first": sum(p["rows_first"] for p in papers),
        "rows_second": sum(p["rows_second"] for p in papers),
        "matched_pairs": sum(p["matched_pairs"] for p in papers),
        "only_first": sum(p["only_first"] for p in papers),
        "only_second": sum(p["only_second"] for p in papers),
        "c_outcomes": {
            k: dict(
                sum(
                    (Counter(p.get("c_outcomes", {}).get(k, {})) for p in papers),
                    Counter(),
                )
            )
            for k in ("fields", "rows", "curve_sample_mapping")
        },
        "categorical": {},
        "numeric": {},
    }
    curves = sum(p.get("curves", 0) for p in papers)
    reassigned = sum(summary["c_outcomes"]["curve_sample_mapping"].values())
    summary["curve_sample_mapping"] = {
        "curves": curves,
        "assigned_differently": reassigned,
        "agreement": (curves - reassigned) / curves if curves else None,
    }
    found = (
        summary["matched_pairs"] * 2 + summary["only_first"] + summary["only_second"]
    )
    summary["row_detection_agreement"] = (
        2 * summary["matched_pairs"] / found if found else None
    )
    for f, v in sorted(cat.items()):
        n = len(v["a"])
        if not n:
            continue
        summary["categorical"][f] = {
            "n": n,
            "exact_agreement": sum(x == y for x, y in zip(v["a"], v["b"])) / n,
            "kappa": cohen_kappa(v["a"], v["b"]),
        }
    for f, v in sorted(num.items()):
        both = [(ok, rel) for ok, rel in v if rel is not None]
        mismatch = sum(1 for ok, rel in v if rel is None and not ok)
        if not both and not mismatch:
            continue
        rels = [rel for _, rel in both]
        summary["numeric"][f] = {
            "n_both_present": len(both),
            "share_within_tolerance": sum(ok for ok, _ in both) / len(both)
            if both
            else None,
            "rel_diff_median": statistics.median(rels) if rels else None,
            "rel_diff_max": max(rels) if rels else None,
            "presence_mismatch": mismatch,
        }
    return summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paper_dirs", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--first", default="A")
    ap.add_argument("--second", default="B")
    ap.add_argument(
        "--legacy",
        action="store_true",
        help="first is the v0.1 rows; labels from C/labels.csv (§9 v0.1 papers)",
    )
    args = ap.parse_args(argv)
    kinds = field_kinds()
    papers = [
        paper_stats(Path(d), kinds, args.first, args.second, args.legacy)
        for d in args.paper_dirs
    ]
    summary = summarize(papers)
    text = json.dumps(summary, indent=2)
    if args.json:
        Path(args.json).write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
