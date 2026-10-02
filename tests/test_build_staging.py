"""Tests for scripts/build_staging.py.

The headline test is `test_the_builder_reproduces_the_committed_hyc0031_rows`:
the builder, run on references/staging/HYC-0031.json, must reproduce the 32
rows now in the dataset **cell for cell**. That is the only check that shows
this tool is a replacement for the hand-written builders it exists to retire,
rather than something that works on fixtures shaped to suit it.

Every other test carries a ``MUTATION:`` line naming the defect it would catch,
and docs/migration_staging_builder_plan.md §7's twelve mutations were run
against the finished script with this file expected to fail on each.
"""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = _ROOT / "scripts" / "build_staging.py"
DATASET = _ROOT / "data" / "raw" / "measurements_v0.1.csv"
SPEC_0031 = _ROOT / "references" / "staging" / "HYC-0031.json"

_spec = importlib.util.spec_from_file_location("build_staging", SCRIPT)
assert _spec and _spec.loader
bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bs)

# §6.7 records a mutation run where every mutation "survived" because the
# imports resolved back to the committed file.
assert Path(bs.__file__).resolve() == SCRIPT.resolve()


def dataset_rows(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(encoding="utf-8", newline="") as h:
        rd = csv.DictReader(h)
        return list(rd.fieldnames or []), list(rd)


@pytest.fixture()
def pre_image(tmp_path: Path) -> Path:
    """The dataset as it stood before HYC-0031 was appended.

    The builder refuses an id already in the dataset, so reproducing HYC-0031
    requires the pre-append state -- which is also the realistic situation a
    staging file is built in.
    """
    cols, rows = dataset_rows(DATASET)
    out = tmp_path / "pre_image.csv"
    with out.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows([r for r in rows if r["paper_id"] != "HYC-0031"])
    return out


@pytest.fixture()
def spec(tmp_path: Path) -> Path:
    """A minimal two-row spec, written to disk so main() can be driven."""
    body = {
        "paper": {
            "paper_id": "HYC-9901",
            "doi": "10.1000/test.1",
            "first_author": "Tester",
            "year": 2020,
            "journal": "Journal of Testing",
            "title": "A test paper",
        },
        "defaults": {
            "material_class": "activated_carbon",
            "measurement_method": "gravimetric_microbalance",
            "measurement_mode": "isothermal",
            "uptake_bound": "exact",
            "extractor": "HyCAN pipeline v2",
            "extraction_date": "2026-10-01",
            "extraction_method": "table_direct",
            "extraction_confidence": 5,
            "reproducibility_tier": "B",
            "source_location": "Table 1",
        },
        "notes": {
            "SHARED": "a shared note fragment",
            "SECOND": "a second fragment",
        },
        "samples": {
            "S1": {
                "label": "AC-1",
                "material_description": "a test activated carbon",
                "bet_surface_area_m2_g": 2000.0,
                "surface_area_method": "BET",
            },
        },
        "measurements": [
            {"sample": "S1", "temperature_k": 77, "pressure_bar": 1,
             "uptake_wt_pct": 2.0, "uptake_type": "excess",
             "notes": ["SHARED"]},
            {"sample": "S1", "temperature_k": 77, "pressure_bar": 20,
             "uptake_wt_pct": 4.0, "uptake_type": "excess",
             "notes": ["SHARED", "SECOND"], "note_extra": "and an extra"},
        ],
    }
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    return p


def edit(spec_path: Path, mutate) -> Path:
    body = json.loads(spec_path.read_text(encoding="utf-8"))
    mutate(body)
    spec_path.write_text(json.dumps(body), encoding="utf-8")
    return spec_path


def run(spec_path: Path, dataset: Path, out: Path, *extra: str) -> int:
    return bs.main(["--dataset", str(dataset), "--out", str(out),
                    *extra, str(spec_path)])


# --- the regression that matters -------------------------------------------

def test_the_builder_reproduces_the_committed_hyc0031_rows(pre_image, tmp_path):
    """Plan §6. The whole justification for this tool.

    HYC-0031's 32 rows were built by a throwaway 67-column script. If the
    shared builder cannot reproduce them exactly, it is not a replacement for
    the hand method and the three sessions that wrote their own were right to.

    MUTATION: any of plan §7's twelve -> this fails.
    """
    out = tmp_path / "regen.csv"
    assert run(SPEC_0031, pre_image, out) == 0

    cols, committed = dataset_rows(DATASET)
    committed = [r for r in committed if r["paper_id"] == "HYC-0031"]
    regen_cols, regen = dataset_rows(out)

    assert regen_cols == cols, "column order diverged from the dataset"
    assert len(regen) == len(committed) == 32
    diffs = [
        (a["measurement_id"], c, a[c], b[c])
        for a, b in zip(committed, regen) for c in cols if a[c] != b[c]
    ]
    assert diffs == [], f"{len(diffs)} cells differ, first: {diffs[:3]}"


def test_the_hyc0031_spec_is_a_real_factoring_not_a_transcription(tmp_path):
    """The spec must actually factor the work, or it saves nothing.

    If every cell were repeated per measurement the reproduction test would
    still pass and the tool would be pointless. This pins the shape: paper and
    default cells written once, per-sample characterisation written once per
    sample, and only a handful of values varying per row.

    MUTATION: inline the sample cells into every measurement -> this fails.
    """
    body = json.loads(SPEC_0031.read_text(encoding="utf-8"))
    varying = {k for m in body["measurements"] for k in m} - {"sample", "notes"}
    assert len(varying) <= 12, sorted(varying)
    assert len(body["samples"]) == 4
    assert len(body["defaults"]) >= 6
    # No measurement may carry a cell that its sample already defines.
    for i, m in enumerate(body["measurements"]):
        shared = set(m) & set(body["samples"][m["sample"]])
        assert not shared, f"measurements[{i}] repeats sample cells {shared}"


# --- reading the dataset rather than assuming it ---------------------------

def test_the_column_order_is_read_from_the_dataset(spec, tmp_path):
    """Plan §7 mutation 1. §6.7: the staging file uses the CSV's PHYSICAL order.

    MUTATION: hard-code the column list -> this fails when the dataset's order
    differs, which is exactly the drift the check exists for.
    """
    cols, rows = dataset_rows(DATASET)
    shuffled = cols[-3:] + cols[:-3]
    ds = tmp_path / "shuffled.csv"
    with ds.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=shuffled, lineterminator="\n")
        w.writeheader()
        w.writerows(rows[:2])
    out = tmp_path / "s.csv"
    assert run(spec, ds, out) == 0
    assert dataset_rows(out)[0] == shuffled


@pytest.mark.parametrize("terminator", ["\n", "\r\n"])
def test_the_line_terminator_is_read_from_the_dataset(spec, tmp_path, terminator):
    """Plan §7 mutation 2 -- the HYC-0031 defect, made impossible.

    The throwaway builder hard-coded CRLF because its author had just examined
    paper_tracking.csv, which is CRLF, and assumed the dataset matched. It is
    LF. Reading it here means the staging file cannot carry the wrong one.

    MUTATION: hard-code either terminator -> one parametrisation fails.
    """
    cols, rows = dataset_rows(DATASET)
    ds = tmp_path / "ds.csv"
    with ds.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=cols, lineterminator=terminator)
        w.writeheader()
        w.writerows(rows[:2])
    out = tmp_path / "s.csv"
    assert run(spec, ds, out) == 0
    raw = out.read_bytes()
    if terminator == "\r\n":
        assert raw.count(b"\n") == raw.count(b"\r\n"), "a lone LF was written"
    else:
        assert b"\r" not in raw, "a CR was written into an LF dataset"


def test_a_mixed_terminator_dataset_is_refused(spec, tmp_path, capsys):
    """A dataset already holding two conventions has no terminator to inherit.

    MUTATION: pick the more common one -> this fails.
    """
    cols, rows = dataset_rows(DATASET)
    ds = tmp_path / "ds.csv"
    with ds.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows[:2])
    raw = ds.read_bytes()
    ds.write_bytes(raw.replace(b"\n", b"\r\n", 1))
    assert run(spec, ds, tmp_path / "s.csv") == 1
    assert "mixed line terminators" in capsys.readouterr().err


# --- the spec's own integrity ----------------------------------------------

def test_an_unknown_key_is_refused(spec, pre_image, tmp_path, capsys):
    """Plan §7 mutation 3, and the worst failure this format allows: a mistyped
    field name drops its value and the output still validates.

    MUTATION: drop check_keys -> this passes and the value vanishes.
    """
    edit(spec, lambda b: b["samples"]["S1"].update({"bet_surface_area": 1.0}))
    assert run(spec, pre_image, tmp_path / "s.csv") == 1
    err = capsys.readouterr().err
    assert "not columns of the dataset" in err and "bet_surface_area" in err


def test_a_derived_cell_may_not_be_set_in_the_spec(spec, pre_image, tmp_path,
                                                   capsys):
    """MUTATION: drop the DERIVED check -> a spec can hand-number ids and
    silently disagree with its own order."""
    edit(spec, lambda b: b["measurements"][0].update(
        {"measurement_id": "HYC-9901-M99"}))
    assert run(spec, pre_image, tmp_path / "s.csv") == 1
    assert "derived by this script" in capsys.readouterr().err


def test_an_undefined_sample_is_refused(spec, pre_image, tmp_path, capsys):
    """Plan §7 mutation 11.

    MUTATION: default to the first sample -> this fails.
    """
    edit(spec, lambda b: b["measurements"][0].update({"sample": "S9"}))
    assert run(spec, pre_image, tmp_path / "s.csv") == 1
    assert "is not defined in 'samples'" in capsys.readouterr().err


def test_an_undefined_note_key_is_refused(spec, pre_image, tmp_path, capsys):
    """Plan §7 mutation 9. §11.4: a note that silently vanishes is
    indistinguishable from a field deliberately left empty.

    MUTATION: resolve a missing key to "" -> this passes and the note is lost.
    """
    edit(spec, lambda b: b["measurements"][0].update({"notes": ["NOPE"]}))
    assert run(spec, pre_image, tmp_path / "s.csv") == 1
    assert "is not defined in the spec's 'notes'" in capsys.readouterr().err


def test_a_malformed_paper_id_is_refused(spec, pre_image, tmp_path, capsys):
    """§8.2: one paper was once written HYC-009, a digit short, and an
    id-matching repair silently skipped it.

    MUTATION: drop the PAPER_ID_RE check -> this fails.
    """
    edit(spec, lambda b: b["paper"].update({"paper_id": "HYC-991"}))
    assert run(spec, pre_image, tmp_path / "s.csv") == 1
    assert "does not match HYC-XXXX" in capsys.readouterr().err


def test_an_unknown_top_level_section_is_refused(spec, pre_image, tmp_path,
                                                 capsys):
    """A whole section quietly ignored is worse than a single cell.

    MUTATION: drop the section check -> a typo'd "sample" section is ignored.
    """
    edit(spec, lambda b: b.update({"sample": {"S2": {}}}))
    assert run(spec, pre_image, tmp_path / "s.csv") == 1
    assert "unknown top-level section" in capsys.readouterr().err


# --- inheritance, ids, notes ------------------------------------------------

def test_sample_cells_are_inherited_by_every_measurement(spec, pre_image,
                                                         tmp_path):
    """Plan §7 mutation 8 -- the whole point of the per-sample table.

    MUTATION: stop applying sample cells -> this fails with empty BET.
    """
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    cols, rows = dataset_rows(out)
    assert [r["bet_surface_area_m2_g"] for r in rows] == ["2000.0", "2000.0"]
    assert {r["material_description"] for r in rows} == {"a test activated carbon"}


def test_a_measurement_may_override_a_sample_cell(spec, pre_image, tmp_path):
    """MUTATION: apply sample cells after measurement cells -> this fails."""
    edit(spec, lambda b: b["measurements"][1].update(
        {"bet_surface_area_m2_g": 1500.0}))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    rows = dataset_rows(out)[1]
    assert [r["bet_surface_area_m2_g"] for r in rows] == ["2000.0", "1500.0"]


def test_measurement_ids_follow_spec_order(spec, pre_image, tmp_path):
    """Plan §7 mutation 12.

    MUTATION: number by sorted pressure, or from 0 -> this fails.
    """
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    rows = dataset_rows(out)[1]
    assert [r["measurement_id"] for r in rows] == ["HYC-9901-M1", "HYC-9901-M2"]
    assert [r["pressure_bar"] for r in rows] == ["1", "20"]
    assert {r["sample_id"] for r in rows} == {"HYC-9901-S1"}


def test_note_fragments_resolve_in_the_order_given(spec, pre_image, tmp_path):
    """Plan §7 mutation 9, and the feature the 2026-09-26 log entry asked for.

    MUTATION: join in sorted or reversed order -> this fails.
    """
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    rows = dataset_rows(out)[1]
    assert rows[0]["notes"] == "a shared note fragment."
    assert rows[1]["notes"] == (
        "a shared note fragment. a second fragment. and an extra.")


def test_a_literal_note_is_used_verbatim(spec, pre_image, tmp_path):
    """A spec that spells a note out in full must get exactly that cell back,
    or a note cannot be transcribed faithfully from an existing row -- which is
    what the HYC-0031 spec does on all 32 rows.

    MUTATION: reformat a literal (strip or append a period) -> this fails.
    """
    literal = "verbatim; with punctuation, and no trailing stop"
    edit(spec, lambda b: b["measurements"][0].update({"notes": literal}))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    assert dataset_rows(out)[1][0]["notes"] == literal


# --- validation and collisions ---------------------------------------------

def test_a_row_that_fails_the_schema_is_refused_and_nothing_is_written(
    spec, pre_image, tmp_path, capsys
):
    """Plan §7 mutations 4 and 5. §9.1 step 7: schema.py is the authority, and
    a staging file that cannot validate must never reach disk.

    MUTATION: write before validating, or skip validation -> this fails.
    """
    edit(spec, lambda b: b["measurements"][0].update(
        {"uptake_type": "not_a_vocabulary_value"}))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 1
    assert "fail schema validation" in capsys.readouterr().err
    assert not out.exists(), "a refused build must leave no file behind"


def test_pressure_above_200_is_admitted_flagged(spec, pre_image, tmp_path, capsys):
    """Manual §11.4: pressure_bar > 200 is a WARNING, not a rejection, so
    high-pressure literature (e.g. HYC-0049's 30 MPa / 300 bar room-temperature
    isotherms) can enter the corpus flagged. schema.py bounds the field at 200
    and this build gate downgrades ONLY that bound, matching validate.py.

    MUTATION: drop the pressure-downgrade branch (validate straight through
    MeasurementEntry) -> this fails, and a real 30 MPa measurement is rejected
    before it can reach the warning-based append.
    """
    edit(spec, lambda b: b["measurements"][0].update({"pressure_bar": 300}))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    assert out.exists(), "a pressure>200 row must be admitted, flagged"
    assert "pressure > 200 bar" in capsys.readouterr().out
    # the 300 bar value is written verbatim, not clamped
    _, rows = dataset_rows(out)
    assert any(r["pressure_bar"] in ("300", "300.0") for r in rows)


def test_pressure_above_200_with_a_second_error_is_still_refused(
    spec, pre_image, tmp_path, capsys
):
    """The §11.4 downgrade is scoped to the pressure bound alone. A row that is
    over 200 bar AND violates another rule must still be refused -- the clamped
    re-validation runs every other field and model check strictly.

    MUTATION: admit on any error once pressure>200 is present -> this fails.
    """
    edit(spec, lambda b: b["measurements"][0].update(
        {"pressure_bar": 300, "uptake_type": "not_a_vocabulary_value"}))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 1
    assert "fail schema validation" in capsys.readouterr().err
    assert not out.exists()


def test_an_id_already_in_the_dataset_is_refused(spec, tmp_path, capsys):
    """Plan §7 mutation 6. A re-run must not collide with appended rows.

    MUTATION: drop the collision check -> append_paper.py catches it later, but
    only after a staging file has been written and reviewed.
    """
    edit(spec, lambda b: b["paper"].update({"paper_id": "HYC-0031"}))
    assert run(spec, DATASET, tmp_path / "s.csv") == 1
    assert "already in the dataset" in capsys.readouterr().err


def test_a_duplicate_id_within_the_spec_is_impossible_by_construction(
    spec, pre_image, tmp_path
):
    """Plan §7 mutation 7.

    Ids are derived from spec position, so a duplicate cannot be expressed --
    which is itself the guarantee, and is why the spec may not set
    measurement_id (tested above). This records that the guard is structural.
    """
    edit(spec, lambda b: b["measurements"].append(dict(b["measurements"][0])))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 0
    ids = [r["measurement_id"] for r in dataset_rows(out)[1]]
    assert ids == ["HYC-9901-M1", "HYC-9901-M2", "HYC-9901-M3"]
    assert len(set(ids)) == len(ids)


def test_a_control_character_in_a_cell_is_refused(spec, pre_image, tmp_path,
                                                  capsys):
    """Plan §7 mutation 10. §6.9: a control character survives the append and
    then breaks every later byte-level line check.

    MUTATION: drop the CONTROL check -> this passes and the dataset gains a row
    whose lines do not map 1:1 onto its rows.
    """
    edit(spec, lambda b: b["measurements"][0].update(
        {"notes": "two\r\nlines"}))
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out) == 1
    assert "control character" in capsys.readouterr().err
    assert not out.exists()


def test_dry_run_writes_nothing(spec, pre_image, tmp_path):
    """MUTATION: let --dry-run fall through to the write -> this fails."""
    out = tmp_path / "s.csv"
    assert run(spec, pre_image, out, "--dry-run") == 0
    assert not out.exists()


def test_a_missing_dataset_is_a_refusal_not_a_traceback(spec, tmp_path, capsys):
    """MUTATION: drop the exists() check -> this raises."""
    assert run(spec, tmp_path / "nope.csv", tmp_path / "s.csv") == 1
    assert "does not exist" in capsys.readouterr().err


def test_malformed_json_is_a_refusal_not_a_traceback(tmp_path, capsys):
    """MUTATION: drop the JSONDecodeError handler -> this raises."""
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    assert run(p, DATASET, tmp_path / "s.csv") == 1
    assert "not valid JSON" in capsys.readouterr().err


# --- the committed spec -----------------------------------------------------

def test_the_committed_spec_validates_against_the_schema(pre_image, tmp_path):
    """Every row the committed spec produces must validate, independently of
    the reproduction test above.

    MUTATION: change a vocabulary value in the spec -> this fails.
    """
    out = tmp_path / "s.csv"
    assert run(SPEC_0031, pre_image, out) == 0
    cols, rows = dataset_rows(out)
    assert len(rows) == 32
    for r in rows:
        bs.MeasurementEntry(**{k: v for k, v in r.items() if v != ""})
