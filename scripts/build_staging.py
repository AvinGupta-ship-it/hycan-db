#!/usr/bin/env python3
"""Build a validated staging CSV from a per-paper JSON spec — §9.1 step 10.

The bottleneck two consecutive execution-log entries named. Three sessions have
each written a throwaway 67-column builder; this is the shared one, so the
fourth does not. Applies docs/migration_staging_builder_plan.md.

The spec holds what a human decided. Everything mechanical is this script's
job: column order and line terminator come from the dataset at run time,
measurement ids are numbered in spec order, per-sample cells are inherited by
every measurement of that sample, and long shared notes are written once and
referenced by key.

Nothing is derived. No unit conversion, no inference, no condition defaulted.
A cell absent from the spec is empty (§3.5).

Usage:
    python3 scripts/build_staging.py references/staging/HYC-0031.json --dry-run
    python3 scripts/build_staging.py references/staging/HYC-0031.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hycan.schema import MeasurementEntry  # noqa: E402

DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_OUT_DIR = Path("data/raw")

PAPER_ID_RE = re.compile(r"^HYC-\d{4}$")

# Cells the script derives and a spec may therefore not set.
DERIVED = ("measurement_id", "sample_id")

# §6.9. A control character in a cell survives the append and then breaks the
# byte-level line checks every later migration depends on, with a diagnosis
# that blames a quoted newline which is not there.
CONTROL = ("\r", "\n", "\t", "\x00")

SPEC_SECTIONS = ("paper", "defaults", "notes", "samples", "measurements")


class SpecError(RuntimeError):
    """Raised when the spec is wrong. Nothing is written."""


def dataset_columns(dataset: Path) -> list[str]:
    """The dataset's PHYSICAL column order, read at run time.

    Never hard-coded: §6.7 requires the staging file to match the CSV's
    physical order, and a schema change must not silently shift a value into
    the wrong column.
    """
    with dataset.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle), None)
    if not header:
        raise SpecError(f"{dataset} has no header row")
    return header


def dataset_terminator(dataset: Path) -> str:
    """The dataset's line terminator, read from its bytes.

    HYC-0031's throwaway builder hard-coded CRLF because its author had just
    examined references/paper_tracking.csv, which is CRLF, and assumed the
    dataset matched. It does not. Reading it here makes that error impossible
    rather than merely detectable by append_paper.py.
    """
    raw = dataset.read_bytes()
    crlf = raw.count(b"\r\n")
    lone_lf = raw.count(b"\n") - crlf
    if crlf and lone_lf:
        raise SpecError(
            f"{dataset} has mixed line terminators ({crlf} CRLF, {lone_lf} "
            f"lone LF). Fix the dataset before building a staging file for it."
        )
    return "\r\n" if crlf else "\n"


def existing_measurement_ids(dataset: Path) -> set[str]:
    with dataset.open(encoding="utf-8", newline="") as handle:
        return {
            (r.get("measurement_id") or "").strip()
            for r in csv.DictReader(handle)
        }


def load_spec(path: Path) -> dict:
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SpecError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(spec, dict):
        raise SpecError(f"{path} must be a JSON object")
    unknown = sorted(set(spec) - set(SPEC_SECTIONS))
    if unknown:
        raise SpecError(
            f"unknown top-level section(s) {unknown}; expected only "
            f"{list(SPEC_SECTIONS)}"
        )
    for required in ("paper", "samples", "measurements"):
        if required not in spec:
            raise SpecError(f"{path} has no '{required}' section")
    return spec


def check_keys(cells: dict, columns: list[str], where: str) -> None:
    """Refuse an unknown key.

    The worst failure this format allows: a mistyped field name drops its value
    and the output still validates, so nothing downstream notices.
    """
    unknown = sorted(set(cells) - set(columns))
    if unknown:
        raise SpecError(
            f"{where}: {unknown} are not columns of the dataset. A mistyped "
            f"field name would drop its value silently, so it is refused."
        )
    derived = sorted(set(cells) & set(DERIVED))
    if derived:
        raise SpecError(
            f"{where}: {derived} are derived by this script and may not be set "
            f"in the spec"
        )


def resolve_notes(entry: dict, notes: dict, where: str) -> str:
    """Join the named note fragments, in the order given, then any extra text.

    `notes` on a sample or a measurement may be a list of keys into the spec's
    shared note block, or a literal string. An unresolved key is an error, not
    an empty string: a note that silently vanishes is indistinguishable from a
    field deliberately left empty (§11.4).

    A LITERAL string is used verbatim, with no reformatting: a spec that spells
    out a note in full must get exactly that cell back, or a note cannot be
    transcribed faithfully from an existing row. Only the key-list form is
    joined, with ". " between fragments after each one's trailing ". " is
    stripped, so fragments can be written as sentences.
    """
    raw = entry.get("notes")
    parts: list[str] = []
    if isinstance(raw, str):
        parts.append(raw)                      # verbatim
    elif isinstance(raw, list):
        for key in raw:
            if not isinstance(key, str):
                raise SpecError(f"{where}: note key {key!r} is not a string")
            if key not in notes:
                raise SpecError(
                    f"{where}: note key {key!r} is not defined in the spec's "
                    f"'notes' section"
                )
            parts.append(notes[key].rstrip(". "))
    elif raw is not None:
        raise SpecError(f"{where}: 'notes' must be a string or a list of keys")
    extra = entry.get("note_extra")
    if extra:
        if not isinstance(extra, str):
            raise SpecError(f"{where}: 'note_extra' must be a string")
        parts.append(extra.rstrip(". "))
    if not parts:
        return ""
    if len(parts) == 1 and isinstance(raw, str):
        return parts[0]
    return ". ".join(parts) + "."


def build_rows(spec: dict, columns: list[str]) -> list[dict]:
    paper = spec["paper"]
    defaults = spec.get("defaults", {})
    notes = spec.get("notes", {})
    samples = spec["samples"]
    measurements = spec["measurements"]

    check_keys(paper, columns, "paper")
    check_keys(defaults, columns, "defaults")

    paper_id = paper.get("paper_id", "")
    if not PAPER_ID_RE.match(str(paper_id)):
        raise SpecError(
            f"paper_id {paper_id!r} does not match HYC-XXXX. One paper was "
            f"once written 'HYC-009', one digit short, and an id-matching "
            f"repair silently skipped it (§8.2)."
        )
    if not isinstance(measurements, list) or not measurements:
        raise SpecError("'measurements' must be a non-empty list")

    # Sample cells, validated once each rather than once per measurement.
    sample_cells: dict[str, dict] = {}
    for key, sample in samples.items():
        body = {k: v for k, v in sample.items()
                if k not in ("notes", "note_extra", "label")}
        check_keys(body, columns, f"samples[{key!r}]")
        body["notes"] = resolve_notes(sample, notes, f"samples[{key!r}]")
        sample_cells[key] = body

    rows: list[dict] = []
    for i, m in enumerate(measurements, start=1):
        where = f"measurements[{i - 1}]"
        if not isinstance(m, dict):
            raise SpecError(f"{where} is not an object")
        key = m.get("sample")
        if key not in samples:
            raise SpecError(
                f"{where}: sample {key!r} is not defined in 'samples' "
                f"(defined: {sorted(samples)})"
            )
        body = {k: v for k, v in m.items()
                if k not in ("sample", "notes", "note_extra")}
        check_keys(body, columns, where)

        sample = sample_cells[key]
        row = {c: "" for c in columns}
        row.update(defaults)
        row.update(paper)
        # Per-sample cells are inherited by every measurement of that sample.
        row.update({k: v for k, v in sample.items() if k != "notes"})
        row.update(body)

        sample_note = sample["notes"]
        own_note = resolve_notes(m, notes, where)
        row["notes"] = " ".join(p for p in (own_note, sample_note) if p).strip()

        row["sample_id"] = f"{paper_id}-{key}"
        row["measurement_id"] = f"{paper_id}-M{i}"
        rows.append({c: ("" if row[c] is None else row[c]) for c in columns})
    return rows


def check_rows(rows: list[dict], dataset: Path | None) -> None:
    """Plan §5. Every post-condition that can be checked before writing."""
    ids = [r["measurement_id"] for r in rows]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise SpecError(f"duplicate measurement_id(s): {dupes}")
    if dataset is not None and dataset.exists():
        clash = sorted(set(ids) & existing_measurement_ids(dataset))
        if clash:
            raise SpecError(
                f"measurement_id(s) already in the dataset: {clash}. A re-run "
                f"must not collide with rows already appended."
            )
    for r in rows:
        for col, value in r.items():
            if isinstance(value, str) and any(c in value for c in CONTROL):
                bad = [repr(c) for c in CONTROL if c in value]
                raise SpecError(
                    f"{r['measurement_id']}.{col} contains {', '.join(bad)}. A "
                    f"control character survives the append and then breaks "
                    f"every later byte-level line check (§6.9)."
                )

    # §9.1 step 7: the schema is the authority, and a staging file that cannot
    # validate must never reach disk.
    #
    # §11.4 exception: pressure_bar > 200 is a WARNING, not a rejection, so
    # "high-pressure literature can enter the corpus flagged rather than be
    # rejected". schema.py bounds the field at 200 (do not "fix" it) and
    # validate.py downgrades the violation; this build gate must agree, or a
    # high-pressure row never reaches the warning-based append. The downgrade is
    # scoped to exactly the pressure_bar <= 200 bound: the row is re-validated
    # with the pressure clamped so every other field check AND the model
    # validators (conditions, uptake, pore qualifiers) still run strictly.
    errors = []
    pressure_over_200 = []
    for r in rows:
        payload = {k: v for k, v in r.items() if v != ""}
        try:
            MeasurementEntry(**payload)
        except Exception as exc:  # pydantic ValidationError and anything else
            errs = exc.errors() if hasattr(exc, "errors") else []
            only_pressure = bool(errs) and all(
                e.get("loc") == ("pressure_bar",)
                and e.get("type") == "less_than_equal"
                for e in errs
            )
            if only_pressure:
                clamped = dict(payload)
                clamped["pressure_bar"] = 200  # run the remaining checks strictly
                try:
                    MeasurementEntry(**clamped)
                except Exception as exc2:
                    errors.append(f"{r['measurement_id']}: {exc2}")
                else:
                    pressure_over_200.append(r["measurement_id"])
            else:
                errors.append(f"{r['measurement_id']}: {exc}")
    if errors:
        joined = "\n  ".join(errors[:10])
        more = f"\n  ... and {len(errors) - 10} more" if len(errors) > 10 else ""
        raise SpecError(f"{len(errors)} row(s) fail schema validation:\n  {joined}{more}")
    if pressure_over_200:
        print(f"  NOTE:      pressure > 200 bar on {pressure_over_200} -- §11.4 "
              f"admits these flagged; append with --expect-new-warning "
              f"'Pressure above 200 bar'")


def render(rows: list[dict], columns: list[str], terminator: str) -> str:
    out = []
    for row in rows:
        import io
        buf = io.StringIO()
        csv.writer(buf, lineterminator="").writerow([row[c] for c in columns])
        out.append(buf.getvalue())
    header_buf = __import__("io").StringIO()
    csv.writer(header_buf, lineterminator="").writerow(columns)
    return terminator.join([header_buf.getvalue()] + out) + terminator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--out", type=Path, default=None,
                        help="explicit output path; overrides --out-dir")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if not args.dataset.exists():
            raise SpecError(f"dataset does not exist: {args.dataset}")
        spec = load_spec(args.spec)
        columns = dataset_columns(args.dataset)
        terminator = dataset_terminator(args.dataset)
        rows = build_rows(spec, columns)
        check_rows(rows, args.dataset)
    except SpecError as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 1

    paper_id = spec["paper"]["paper_id"]
    out = args.out or (args.out_dir / f"staging_{paper_id}.csv")
    body = render(rows, columns, terminator)

    print(f"{args.spec}: {len(rows)} rows, {len(columns)} columns")
    print(f"  samples:   {sorted({r['sample_id'] for r in rows})}")
    print(f"  ids:       {rows[0]['measurement_id']} .. {rows[-1]['measurement_id']}")
    print(f"  terminator: {terminator!r} (read from {args.dataset})")
    print(f"  schema:    all {len(rows)} rows validate")
    tiers = sorted({r["reproducibility_tier"] for r in rows})
    print(f"  tiers:     {tiers}"
          + ("  <- empty: assign per §13 before appending" if tiers == [""] else ""))

    if args.dry_run:
        print(f"\n--dry-run: nothing written. Would write {out}")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        handle.write(body)

    # Read back from disk and re-check, rather than trusting what was intended.
    with out.open(encoding="utf-8", newline="") as handle:
        back = list(csv.reader(handle))
    if back[0] != columns:
        out.unlink()
        print("post-condition failed: written header does not match the "
              "dataset's column order; file removed", file=sys.stderr)
        return 1
    if len(back) != len(rows) + 1:
        out.unlink()
        print(f"post-condition failed: wrote {len(back) - 1} rows, expected "
              f"{len(rows)}; file removed", file=sys.stderr)
        return 1
    print(f"\nwrote {out}, read back and verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
