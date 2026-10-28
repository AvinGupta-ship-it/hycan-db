"""Inputs and matching for blind dual extraction (docs/v1_protocol.md §9).

  prepare   build each agent's input directory from the PDFs, each under a
            parent of its own (protocol §15, Amendment 1):
              dual    --out-a: paper.json, text/ (pdftotext -layout), pages/
                      --out-b: paper.json, pages/ only
                      --out-c: paper.json, the PDFs, text/, pages/
              legacy  --out-b and --out-c as above, plus
                      --out-v01:    rows.csv, the paper's v0.1 rows
                      --out-labels: paper.json, the PDFs, text/, pages/,
                                    v01_rows.csv (the labeller's input)
  assemble  copy the two extractions (rows.csv, digitizations/) into the
            reconciler's directory as first/ and second/, with labels.csv in
            legacy mode, and run `match` into it
  check     check a reconciler's output: every non-agree match line has a
            resolution, and every computed W1 equals the value code computes
  match     match two extractions by the §9 rule and write, for agent C,
              match.csv            one line per differing field of each
                                   matched pair, one line per unmatched row,
                                   and one line with an empty field for each
                                   pair that agrees entirely
              digitized_means.csv  the value and uncertainty §9 assigns to
                                   each figure point

§9 matching rule: rows are matched on sample label, temperature (within 1 K),
pressure (within the larger of 2% and 0.02 bar) and the quantity reported.
Within those tolerances a pair on the same isotherm branch, then the closest in
pressure, then in temperature, is preferred; each row is matched at most once.

The sample label is the text of `material_description` before the first " | "
(the extraction prompt's convention), compared after Unicode normalization and
case folding, on its letters and digits only. v0.1 rows carry no such label;
in legacy mode their labels come from the labeller's labels.csv.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

MMOL_TO_WT = 0.201588
ML_STP_TO_WT = 0.0089938  # §11.0, the factor the extraction prompt states

# Fields not compared: identifiers each extractor assigns independently,
# provenance, and free text whose wording legitimately differs.
NOT_COMPARED = frozenset(
    {
        "measurement_id",
        "sample_id",
        "isotherm_id",
        "material_description",
        "source_location",
        "notes",
        "basis_evidence",
        "extractor",
        "extraction_date",
        "extraction_confidence",
        "verified_by",
        "verification_date",
        "reproducibility_tier",
        "selection_route",
        "frame_id",
        "duplicate_of",
        "digitization_uncertainty_wt_pct",
    }
)
# Free-text fields whose wording legitimately differs: compared on presence
# only (one extractor filled it, the other did not).
PRESENCE_ONLY = frozenset(
    {
        "material_identity",
        "free_volume_calibration",
        "purification_method",
        "activation_method",
        "functional_groups",
    }
)
# Compared case-insensitively.
CASE_INSENSITIVE = frozenset({"doi"})
DIGITIZED_NUMERIC = (
    "pressure_bar",
    "uptake_wt_pct",
    "uptake_mmol_g",
    "uptake_ml_stp_g",
)
FIGURE_REL_TOL = 0.03
T_TOL_K = 1.0
P_TOL_REL = 0.02
P_TOL_ABS_BAR = 0.02


def printed_label(material_description: str) -> str:
    return (material_description or "").split(" | ", 1)[0]


def norm_label(material_description: str) -> str:
    label = unicodedata.normalize("NFKC", printed_label(material_description))
    return re.sub(r"[\W_]+", "", label.casefold())


def read_labels(path: Path) -> dict[str, dict[str, str]]:
    """labels.csv (legacy_labels role) -> {"sample": {sample_id: label},
    "row": {measurement_id: label}}; a row-specific label overrides the
    sample's."""
    out: dict[str, dict[str, str]] = {"sample": {}, "row": {}}
    with path.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            mids = [m.strip() for m in (r.get("measurement_ids") or "").split(";")]
            mids = [m for m in mids if m]
            if mids:
                for m in mids:
                    out["row"][m] = r["label"]
            else:
                out["sample"][r["sample_id"]] = r["label"]
    return out


def row_label(row: dict, labels: dict[str, dict[str, str]] | None = None) -> str:
    """The printed label of a row: from labels.csv when given, else from
    material_description."""
    if labels is not None:
        mid, sid = row.get("measurement_id", ""), row.get("sample_id", "")
        if mid in labels["row"]:
            return labels["row"][mid]
        if sid in labels["sample"]:
            return labels["sample"][sid]
        return "(no label)"
    return printed_label(row.get("material_description", ""))


def to_float(x: str | None) -> float | None:
    if x is None or str(x).strip() == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def quantity(row: dict) -> str:
    """The kind of value a row reports (§9 'the quantity reported')."""
    if any(
        to_float(row.get(f)) is not None
        for f in ("uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g")
    ):
        return "gravimetric_uptake"
    if to_float(row.get("volumetric_capacity_kg_m3")) is not None:
        return "volumetric_capacity"
    if to_float(row.get("adsorbed_phase_density_kg_m3")) is not None:
        return "adsorbed_phase_density"
    if to_float(row.get("areal_uptake_g_cm2")) is not None:
        return "areal_uptake"
    return "characterization"


def within_pressure(p1: float | None, p2: float | None) -> bool:
    if p1 is None or p2 is None:
        return p1 is None and p2 is None
    # The 1e-9 absorbs binary rounding: 0.52 - 0.50 is 0.02000000000000002.
    return abs(p1 - p2) <= max(P_TOL_REL * max(abs(p1), abs(p2)), P_TOL_ABS_BAR) + 1e-9


def within_temperature(t1: float | None, t2: float | None) -> bool:
    if t1 is None or t2 is None:
        return t1 is None and t2 is None
    return abs(t1 - t2) <= T_TOL_K + 1e-9


@dataclass
class Pair:
    first: dict | None
    second: dict | None


def match(
    first: list[dict],
    second: list[dict],
    first_labels: dict[str, dict[str, str]] | None = None,
    legacy: bool = False,
) -> list[Pair]:
    """Greedy one-to-one matching under the §9 rule (see module docstring).
    `first_labels` gives the first set's labels (legacy mode). In legacy mode a
    v0.1 row with no pressure also matches a row whose pressure was read from a
    figure: the v0.1 rows left the pressure of a saturation value empty where
    the extraction prompt takes the plotted point's pressure."""
    candidates = []
    for i, a in enumerate(first):
        la = norm_label(row_label(a, first_labels))
        for j, b in enumerate(second):
            if la != norm_label(row_label(b)):
                continue
            if quantity(a) != quantity(b):
                continue
            ta, tb = to_float(a.get("temperature_k")), to_float(b.get("temperature_k"))
            pa, pb = to_float(a.get("pressure_bar")), to_float(b.get("pressure_bar"))
            p_ok = within_pressure(pa, pb) or (
                legacy and pa is None and pb is not None and is_digitized(b, "pressure_bar")
            )
            if not (within_temperature(ta, tb) and p_ok):
                continue
            branch_differs = (a.get("isotherm_branch") or "") != (
                b.get("isotherm_branch") or ""
            )
            dp = (
                0.0
                if pa is None or pb is None
                else abs(pa - pb) / max(abs(pa), abs(pb), 1e-9)
            )
            dt = 0.0 if ta is None else abs(ta - tb)
            candidates.append((branch_differs, dp, dt, i, j))
    candidates.sort()
    used_a, used_b, pairs = set(), set(), []
    for _, _, _, i, j in candidates:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        pairs.append(Pair(first[i], second[j]))
    pairs += [Pair(a, None) for i, a in enumerate(first) if i not in used_a]
    pairs += [Pair(None, b) for j, b in enumerate(second) if j not in used_b]
    return pairs


def _schema_defaults() -> dict[str, str]:
    """Defaults of non-optional schema fields: an empty cell means the default."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from hycan.schema import MeasurementEntry

    out = {}
    for name, f in MeasurementEntry.model_fields.items():
        if f.default is None or f.is_required():
            continue
        d = f.default
        out[name] = str(d).lower() if isinstance(d, bool) else str(d)
    return out


SCHEMA_DEFAULTS = _schema_defaults()


def _v2_fields() -> frozenset[str]:
    """The schema v2 fields: basis_stated and every field after it."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from hycan.schema import MeasurementEntry

    names = list(MeasurementEntry.model_fields)
    return frozenset(names[names.index("basis_stated") :])


V2_FIELDS = _v2_fields()


def norm_value(v: str | None, field: str | None = None) -> str:
    s = "" if v is None else str(v).strip()
    if not s and field in SCHEMA_DEFAULTS:
        s = SCHEMA_DEFAULTS[field]
    if s.lower() in ("true", "false"):
        return s.lower()
    return s


PRESSURE_DIGITIZED = "pressure digitized"


def is_digitized(row: dict, field: str) -> bool:
    """Whether the row's value of `field` was read from a figure: every
    DIGITIZED_NUMERIC field of a figure_digitized row, and the pressure of a
    table or text row whose notes say `pressure digitized` (extraction prompt,
    a printed value with no printed pressure)."""
    if field not in DIGITIZED_NUMERIC:
        return False
    if row.get("extraction_method") == "figure_digitized":
        return True
    return field == "pressure_bar" and PRESSURE_DIGITIZED in (row.get("notes") or "")


def values_agree(field: str, a: dict, b: dict) -> bool:
    va, vb = norm_value(a.get(field), field), norm_value(b.get(field), field)
    if field in PRESENCE_ONLY:
        return bool(va) == bool(vb)
    if field in CASE_INSENSITIVE:
        return va.casefold() == vb.casefold()
    if va == vb:
        return True
    fa, fb = to_float(va), to_float(vb)
    if fa is None or fb is None:
        return False
    if is_digitized(a, field) or is_digitized(b, field):
        return abs(fa - fb) <= FIGURE_REL_TOL * max(abs(fa), abs(fb))
    return math.isclose(fa, fb, rel_tol=1e-12, abs_tol=0.0)


def compared_fields(columns: list[str]) -> list[str]:
    return [c for c in columns if c not in NOT_COMPARED]


def pair_fields(columns: list[str], a: dict, legacy: bool) -> list[str]:
    """The fields compared for one matched pair. In legacy mode the first row
    is a v0.1 row, which has no schema v2 coding: a v2 field empty on that side
    is not compared (B's coding is the only one; C checks it)."""
    fields = compared_fields(columns)
    if legacy:
        fields = [
            f for f in fields if not (f in V2_FIELDS and not (a.get(f) or "").strip())
        ]
    return fields


def match_lines(
    pairs: list[Pair],
    columns: list[str],
    legacy: bool = False,
    first_labels: dict[str, dict[str, str]] | None = None,
) -> list[dict]:
    lines = []
    for n, pair in enumerate(pairs, 1):
        a, b = pair.first, pair.second
        base = {
            "match_line": str(n),
            "first_measurement_id": (a or {}).get("measurement_id", ""),
            "second_measurement_id": (b or {}).get("measurement_id", ""),
            "first_label": row_label(a, first_labels) if a else "",
            "second_label": row_label(b) if b else "",
        }
        if a is None or b is None:
            lines.append(
                {
                    **base,
                    "status": "only_second" if a is None else "only_first",
                    "field": "",
                    "first_value": "",
                    "second_value": "",
                }
            )
            continue
        diffs = [f for f in pair_fields(columns, a, legacy) if not values_agree(f, a, b)]
        if not diffs:
            lines.append(
                {
                    **base,
                    "status": "agree",
                    "field": "",
                    "first_value": "",
                    "second_value": "",
                }
            )
        for f in diffs:
            lines.append(
                {
                    **base,
                    "status": "differ",
                    "field": f,
                    "first_value": a.get(f, ""),
                    "second_value": b.get(f, ""),
                }
            )
    return lines


PRESSURE_LABEL = re.compile(r"press|\bbar\b|atm|mpa|kpa|torr|psi|p/p", re.IGNORECASE)


def uptake_axis(archive: dict, value: float | None) -> str:
    """Which axis of a digitization carries the uptake. A pressure-composition
    plot puts uptake on x, so y cannot be assumed: the axis on which a
    digitized point equals the row's uptake value is taken, then the axis
    whose label does not name a pressure, then y."""
    cal = archive["calibration"]
    if set(cal) & {"x", "y"} != {"x", "y"}:
        return "y" if "y" in cal else "x"
    if value is not None:
        hits = [
            ax
            for ax in ("x", "y")
            if any(
                math.isclose(float(pt.get(ax, "nan")), value, rel_tol=1e-9)
                for pt in archive.get("series", [])
            )
        ]
        if len(hits) == 1:
            return hits[0]
    pressure = [ax for ax in ("x", "y") if PRESSURE_LABEL.search(cal[ax].get("label") or "")]
    if len(pressure) == 1:
        return "y" if pressure[0] == "x" else "x"
    return "y"


def axis_span(digitization_dir: Path, row: dict) -> float | None:
    """1% of this is the §9 floor on a figure value's uncertainty: the distance
    between the two calibration ticks of the uptake axis, which the extraction
    prompt sets at its lowest and highest labelled ticks."""
    notes = row.get("notes") or ""
    m = re.search(r"archive:\s*([\w.\-]+\.json)", notes) or re.search(
        r"([\w.\-]+\.json)", notes
    )
    if not m:
        return None
    path = digitization_dir / m.group(1)
    if not path.exists():
        return None
    archive = json.loads(path.read_text(encoding="utf-8"))
    f = uptake_field(row)
    ax = archive["calibration"][uptake_axis(archive, to_float(row.get(f)) if f else None)]
    span = abs(float(ax["reference_2"]["value"]) - float(ax["reference_1"]["value"]))
    if f == "uptake_wt_pct" and (row.get("wt_pct_convention_source") or "") == (
        "computed_from_other_unit"
    ):
        span *= 0.1  # the axis is in mg/g; the row stores W1 = 0.1 x mg/g
    return span


def uptake_field(row: dict) -> str | None:
    """The uptake column holding the value as printed or digitized: the other
    unit when the stored wt% was computed from it (extraction prompt)."""
    if (row.get("wt_pct_convention_source") or "") == "computed_from_other_unit":
        for f in ("uptake_mmol_g", "uptake_ml_stp_g"):
            if to_float(row.get(f)) is not None:
                return f
    for f in ("uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g"):
        if to_float(row.get(f)) is not None:
            return f
    return None


def to_wt(field: str, value: float) -> float:
    return (
        value
        * {
            "uptake_wt_pct": 1.0,
            "uptake_mmol_g": MMOL_TO_WT,
            "uptake_ml_stp_g": ML_STP_TO_WT,
        }[field]
    )


def _digitized(row: dict | None) -> bool:
    return row is not None and row.get("extraction_method") == "figure_digitized"


def _single(n: int, row: dict, directory: Path | None, side: str, basis: str) -> dict | None:
    f = uptake_field(row)
    if f is None:
        return None
    span = axis_span(directory, row) if directory else None
    u = None if span is None else 0.01 * span
    return {
        "match_line": str(n),
        "from": side,
        "uptake_field": f,
        "value": repr(to_float(row[f])),
        "pressure_bar": row.get("pressure_bar", ""),
        "digitization_uncertainty_wt_pct": "" if u is None else repr(to_wt(f, u)),
        "basis": basis,
    }


def figure_values(
    pairs: list[Pair], first_dir: Path, second_dir: Path | None, legacy: bool
) -> list[dict]:
    """§9 figure values, uncertainty always in wt%.

    Dual mode: a point both extractors digitized in the same unit gets the mean
    of the two values (and pressures), with uncertainty max(half difference,
    1% of the axis span). A point only one extractor digitized gets that value,
    with 1% of its axis span (Amendment 1). Legacy mode: B's value, with 1% of
    the axis span (§9 v0.1 papers). The axis span is the distance between the
    two calibration ticks, which the extraction prompt sets at the lowest and
    highest labelled ticks."""
    out = []
    for n, pair in enumerate(pairs, 1):
        a, b = pair.first, pair.second
        if legacy:
            if _digitized(b):
                e = _single(n, b, second_dir, "second", "B value; 1% of axis span")
                if e:
                    out.append(e)
            continue
        fa = uptake_field(a) if _digitized(a) else None
        fb = uptake_field(b) if _digitized(b) else None
        if fa is not None and fa == fb:
            va, vb = to_float(a[fa]), to_float(b[fb])
            spans = [
                x
                for x in (axis_span(first_dir, a), axis_span(second_dir, b))
                if x is not None
            ]
            span = max(spans) if spans else None
            half = abs(va - vb) / 2
            u = max(half, 0.01 * span) if span is not None else None
            pa, pb = to_float(a.get("pressure_bar")), to_float(b.get("pressure_bar"))
            out.append(
                {
                    "match_line": str(n),
                    "from": "both",
                    "uptake_field": fa,
                    "value": repr((va + vb) / 2),
                    "pressure_bar": ""
                    if pa is None or pb is None
                    else repr((pa + pb) / 2),
                    "digitization_uncertainty_wt_pct": ""
                    if u is None
                    else repr(to_wt(fa, u)),
                    "basis": "mean of first and second; max(half difference, "
                    "1% of axis span)",
                }
            )
            continue
        for row, directory, side in ((a, first_dir, "first"), (b, second_dir, "second")):
            if _digitized(row):
                e = _single(
                    n, row, directory, side, "one digitization; 1% of axis span"
                )
                if e:
                    out.append(e)
    return out


def read_rows(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


MATCH_COLUMNS = [
    "match_line",
    "status",
    "first_measurement_id",
    "second_measurement_id",
    "first_label",
    "second_label",
    "field",
    "first_value",
    "second_value",
]
FIGURE_COLUMNS = [
    "match_line",
    "from",
    "uptake_field",
    "value",
    "pressure_bar",
    "digitization_uncertainty_wt_pct",
    "basis",
]


def cmd_match(args: argparse.Namespace) -> int:
    cols_a, first = read_rows(Path(args.first) / "rows.csv")
    cols_b, second = read_rows(Path(args.second) / "rows.csv")
    if cols_a != cols_b:
        print("REFUSED: the two rows.csv files have different columns", file=sys.stderr)
        return 1
    labels = read_labels(Path(args.labels)) if args.labels else None
    if args.legacy and labels is None:
        print("REFUSED: legacy mode needs --labels", file=sys.stderr)
        return 1
    pairs = match(first, second, labels, legacy=args.legacy)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(
        out / "match.csv",
        MATCH_COLUMNS,
        match_lines(pairs, cols_a, legacy=args.legacy, first_labels=labels),
    )
    write_csv(
        out / "digitized_means.csv",
        FIGURE_COLUMNS,
        figure_values(
            pairs,
            Path(args.first) / "digitizations",
            Path(args.second) / "digitizations",
            args.legacy,
        ),
    )
    n_pairs = sum(p.first is not None and p.second is not None for p in pairs)
    print(
        f"{n_pairs} matched pairs, {sum(p.second is None for p in pairs)} only first, "
        f"{sum(p.first is None for p in pairs)} only second"
    )
    return 0


PAPER_KEYS = ("paper_id", "doi", "first_author", "year", "journal", "title")


def _render(pdfs: list[Path], d: Path, with_text: bool, dpi: int, copy_pdf: bool) -> None:
    (d / "pages").mkdir(parents=True)
    for pdf in pdfs:
        if with_text:
            (d / "text").mkdir(exist_ok=True)
            subprocess.run(
                ["pdftotext", "-layout", str(pdf), str(d / "text" / f"{pdf.stem}.txt")],
                check=True,
            )
        subprocess.run(
            ["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(d / "pages" / pdf.stem)],
            check=True,
        )
        if copy_pdf:
            shutil.copy(pdf, d / pdf.name)


def _write_paper(d: Path, paper: dict, extra: dict) -> None:
    info = {k: paper[k] for k in PAPER_KEYS if k in paper}
    info.update(extra)
    (d / "paper.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")


def cmd_prepare(args: argparse.Namespace) -> int:
    """Each agent's input under a parent of its own (Amendment 1). The input
    paper JSON carries the paper's identity plus extractor_A, extractor_B,
    extractor_C (the `extractor` string of the reconciled rows) and verifier."""
    targets = {"B": args.out_b, "C": args.out_c}
    if args.legacy:
        targets.update(v01=args.out_v01, labels=args.out_labels)
    else:
        targets["A"] = args.out_a
    missing = [k for k, v in targets.items() if not v]
    if missing:
        print(f"REFUSED: missing output directories for {missing}", file=sys.stderr)
        return 1
    dirs = {k: Path(v) for k, v in targets.items()}
    parents = [d.resolve().parent for d in dirs.values()]
    if len(set(parents)) != len(parents):
        print("REFUSED: every agent's input needs a parent of its own", file=sys.stderr)
        return 1
    for d in dirs.values():
        if d.exists():
            print(f"REFUSED: {d} exists", file=sys.stderr)
            return 1
    paper = json.loads(Path(args.paper_json).read_text(encoding="utf-8"))
    pdfs = [Path(p) for p in args.pdf]
    if not args.legacy:
        _render(pdfs, dirs["A"], True, args.dpi, False)
        _write_paper(dirs["A"], paper, {"extractor": paper.get("extractor_A", "")})
    _render(pdfs, dirs["B"], False, args.dpi, False)
    _write_paper(dirs["B"], paper, {"extractor": paper.get("extractor_B", "")})
    _render(pdfs, dirs["C"], True, args.dpi, True)
    _write_paper(
        dirs["C"],
        paper,
        {"extractor": paper.get("extractor_C", ""), "verifier": paper.get("verifier", "")},
    )
    if args.legacy:
        cols, rows = read_rows(Path(args.v01))
        mine = [r for r in rows if r.get("paper_id") == paper["paper_id"]]
        if not mine:
            print(f"REFUSED: no v0.1 rows for {paper['paper_id']}", file=sys.stderr)
            return 1
        dirs["v01"].mkdir(parents=True)
        write_csv(dirs["v01"] / "rows.csv", cols, mine)
        _render(pdfs, dirs["labels"], True, args.dpi, True)
        _write_paper(dirs["labels"], paper, {})
        write_csv(dirs["labels"] / "v01_rows.csv", cols, mine)
    print("prepared " + ", ".join(f"{k}: {v}" for k, v in dirs.items()))
    return 0


def cmd_assemble(args: argparse.Namespace) -> int:
    """Copy the two extractions into the reconciler's input and match them."""
    c = Path(args.c)
    if not (c / "paper.json").exists():
        print(f"REFUSED: {c} is not a prepared reconciler input", file=sys.stderr)
        return 1
    for name, src in (("first", Path(args.first)), ("second", Path(args.second))):
        dest = c / name
        if dest.exists():
            print(f"REFUSED: {dest} exists", file=sys.stderr)
            return 1
        dest.mkdir()
        shutil.copy(src / "rows.csv", dest / "rows.csv")
        if (src / "digitizations").is_dir():
            shutil.copytree(src / "digitizations", dest / "digitizations")
    if args.legacy:
        shutil.copy(args.labels, c / "labels.csv")
    return cmd_match(
        argparse.Namespace(
            first=str(c / "first"),
            second=str(c / "second"),
            out=str(c),
            legacy=args.legacy,
            labels=str(c / "labels.csv") if args.legacy else None,
        )
    )


def recompute_w1(row: dict) -> float | None:
    """The W1 wt% code computes for a row whose stored wt% was computed from
    another unit (§3, §11.0), or None when the row is not such a row."""
    if (row.get("wt_pct_convention_source") or "") != "computed_from_other_unit":
        return None
    mmol, ml = to_float(row.get("uptake_mmol_g")), to_float(row.get("uptake_ml_stp_g"))
    if mmol is not None:
        return mmol * MMOL_TO_WT
    if ml is not None:
        return ml * ML_STP_TO_WT
    return None  # printed in mg/g: the prompt stores 0.1 x mg/g, notes keep it


def cmd_check(args: argparse.Namespace) -> int:
    """Check a reconciler's output: every non-agree line of match.csv has a
    resolution, and every computed W1 equals the value code computes."""
    c_in, c_out = Path(args.c_input), Path(args.c_output)
    _, lines = read_rows(c_in / "match.csv")
    _, res = read_rows(c_out / "resolutions.csv")
    _, rows = read_rows(c_out / "rows.csv")
    resolved = {r.get("match_line", "") for r in res}
    open_lines = sorted(
        {ln["match_line"] for ln in lines if ln["status"] != "agree"} - resolved,
        key=int,
    )
    w1 = []
    for r in rows:
        v = recompute_w1(r)
        stored = to_float(r.get("uptake_wt_pct"))
        if v is not None and (stored is None or not math.isclose(v, stored, rel_tol=1e-6)):
            w1.append((r.get("measurement_id"), stored, v))
    mixed = sorted(
        iso
        for iso, vals in _per_isotherm(rows, ISOTHERM_CONSTANT).items()
        if len(vals) > 1
    )
    print(f"{len(lines)} match lines, {len(res)} resolutions, {len(rows)} rows")
    print(f"match lines without a resolution: {open_lines or 'none'}")
    print(f"computed W1 differing from code: {w1 or 'none'}")
    print(f"isotherms whose rows differ in {', '.join(ISOTHERM_CONSTANT)}: {mixed or 'none'}")
    return 1 if open_lines or w1 or mixed else 0


# Fields the extraction prompt codes once per isotherm; src/hycan/v1.py refuses
# an isotherm whose rows differ in the basis.
ISOTHERM_CONSTANT = (
    "basis_stated",
    "basis_inferred",
    "uptake_type",
    "measurement_method",
)


def _per_isotherm(rows: list[dict], fields: tuple[str, ...]) -> dict[str, set]:
    out: dict[str, set] = {}
    for r in rows:
        iso = (r.get("isotherm_id") or "").strip()
        if iso:
            out.setdefault(iso, set()).add(
                tuple(norm_value(r.get(f), f) for f in fields)
            )
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--paper-json", required=True)
    p.add_argument(
        "--pdf", action="append", required=True, help="main PDF first, then SI"
    )
    p.add_argument("--out-a")
    p.add_argument("--out-b", required=True)
    p.add_argument("--out-c", required=True)
    p.add_argument("--legacy", action="store_true", help="a v0.1 paper outside the sample")
    p.add_argument("--v01", default="data/raw/measurements_v0.1.csv")
    p.add_argument("--out-v01")
    p.add_argument("--out-labels")
    p.add_argument("--dpi", type=int, default=150)
    a = sub.add_parser("assemble")
    a.add_argument("--c", required=True, help="the reconciler's prepared input")
    a.add_argument("--first", required=True, help="A's output, or the v0.1 rows")
    a.add_argument("--second", required=True, help="B's output")
    a.add_argument("--legacy", action="store_true")
    a.add_argument("--labels", help="the labeller's labels.csv (legacy mode)")
    m = sub.add_parser("match")
    m.add_argument(
        "--first", required=True, help="directory with rows.csv (A, or v0.1 rows)"
    )
    m.add_argument("--second", required=True, help="directory with rows.csv (B)")
    m.add_argument("--out", required=True)
    m.add_argument("--legacy", action="store_true", help="first is the v0.1 rows (§9)")
    m.add_argument("--labels", help="labels.csv for the first row set (legacy mode)")
    k = sub.add_parser("check")
    k.add_argument("--c-input", required=True, help="the reconciler's input")
    k.add_argument("--c-output", required=True, help="the reconciler's output")
    args = ap.parse_args(argv)
    if args.cmd == "assemble" and args.legacy and not args.labels:
        ap.error("assemble --legacy needs --labels")
    return {
        "prepare": cmd_prepare,
        "assemble": cmd_assemble,
        "match": cmd_match,
        "check": cmd_check,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
