#!/usr/bin/env python3
"""Relabel 36 synthesis_method cells and backfill HYC-0027's Pd composition.

Applies docs/migration_relabel_plan.md and nothing else. Reads and writes raw
CSV cells through the csv module rather than pandas, so every cell this script
does not name is byte-identical by construction and verify() can assert exactly
that.

The 36 relabels move rows extracted before schema v1.2 onto the vocabulary
values v1.2 added and no migration ever applied, which left `synthesis_method`
partitioning the corpus by extraction date rather than by chemistry. Two papers
that carry activation language and must NOT change are named in the plan's §8
and asserted here as preconditions, because the difference between this
migration and a text-matching sweep is that a sweep cannot produce that section.

Every `notes` edit is an exact substring replacement on a sentence the plan
quotes, applied to a named row set whose size is asserted. Rewriting a whole
`notes` cell from a value read out of a tool result is how a long field gets
silently truncated.

Refuses to run twice.

Usage:
    python3 scripts/migrate_relabel.py --dry-run
    python3 scripts/migrate_relabel.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import shutil
import sys
from pathlib import Path

DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")
DEFAULT_BACKUP_DIR = Path("/tmp")

DEFAULT_EXPECTED_ROWS = 225
DEFAULT_EXPECTED_CHANGED_CELLS = 70
EXPECTED_COLUMNS = 67

# Columns this migration is allowed to touch. Anything else changing is a bug,
# not a surprise.
SCOPE_COLUMNS = frozenset(
    {
        "synthesis_method",
        "metal_element",
        "metal_loading_wt_pct",
        "dopant_concentration_at_pct",
        "dopant_concentration_method",
        "notes",
    }
)

# --- Plan §1, encoded per paper so the script cannot drift from the table. ---

_CHEMICAL_ACTIVATION = {
    # §2 Klechikov 2015 -- the seven rows whose activation_method is koh_activation.
    "HYC-0016": ("M3", "M4", "M5", "M8", "M9", "M10", "M12"),
    # §3 Huang 2010 -- all twelve; six samples, one route, two conditions each.
    "HYC-0019": tuple(f"M{n}" for n in range(1, 13)),
    # §4 Serafin 2024 -- all seven; KOH on raw biomass, one-step route.
    "HYC-0020": tuple(f"M{n}" for n in range(1, 8)),
    # §5 Sethia 2016 -- the four NAC samples. M1/M2 are the carbonization control.
    "HYC-0021": ("M3", "M4", "M5", "M6"),
    # §6 Wang 2009 -- the KOH half of the split.
    "HYC-0022": ("M4", "M5", "M6", "M7"),
}

_PHYSICAL_ACTIVATION = {
    # §6 Wang 2009 -- the CO2-gasified half. The corpus's first rows on this value.
    "HYC-0022": ("M2", "M3"),
}


def _expand(mapping: dict[str, tuple[str, ...]]) -> set[str]:
    return {f"{paper}-{row}" for paper, rows in mapping.items() for row in rows}


SYNTHESIS_RELABEL: dict[str, str] = {
    **{mid: "chemical_activation" for mid in _expand(_CHEMICAL_ACTIVATION)},
    **{mid: "physical_activation" for mid in _expand(_PHYSICAL_ACTIVATION)},
}

# Plan §1: the deltas, which is what this migration guarantees. Absolute totals
# were pinned once in this project and were false the next time a paper was
# appended.
EXPECTED_SYNTHESIS_DELTAS = {
    "other": -13,
    "carbonization": -23,
    "chemical_activation": +34,
    "physical_activation": +2,
}

# Plan §5: after this migration these are the only carbonization-only samples in
# the corpus, and they are the control that proves this was not a blanket sweep.
CARBONIZATION_SURVIVORS = frozenset({"HYC-0021-M1", "HYC-0021-M2"})

# Plan §8: named so a future widening of the scope has to delete an assertion
# rather than merely forget a paragraph.
MUST_NOT_CHANGE = {
    "HYC-0001": "authors activated nothing; the KOH route belongs to AX-21",
    "HYC-0004": "Norit supplied the carbons; every route statement is generic",
}

# --- Plan §9, the HYC-0027 composition backfill and the one removal. --------

PD_ROWS = ("HYC-0027-M2", "HYC-0027-M4", "HYC-0027-M5")
PD_N_HEG_ROWS = ("HYC-0027-M4", "HYC-0027-M5")
NITROGEN_REMOVAL_ROW = "HYC-0027-M3"

METAL_ELEMENT = "Pd"
# Plan §9.1: three independent statements support 20 (nominal, EDX, Eq. 1's
# q = 0.20) and one supports 21 (XPS, which over-reads a supported
# nanoparticle's bulk loading).
METAL_LOADING_WT_PCT = "20"
DOPANT_CONCENTRATION_METHOD = "XPS"

# --- Plan §10, the mandatory notes edits. -----------------------------------
#
# Each entry is (scope, operation, *args). A paper scope asserts the expected row
# count; a row scope asserts exactly one row. A replacement whose old text is not
# found on every row in scope aborts the migration -- a sentence that silently
# failed to match would leave the row's prose contradicting its own field, which
# is the whole reason these edits are not optional.

_HYC0019_OLD_A = (
    "synthesis_method stays carbonization on all six rows rather than splitting "
    "the five oxidised samples to chemical_oxidation: in this vocabulary "
    "chemical_oxidation is a graphite-oxide-route synthesis value, the oxidation "
    "here is a post-synthesis surface treatment, and splitting would make the six "
    "rows of a controlled single-variable study non-comparable on the one field "
    "saying how the carbon was made."
)
_HYC0019_NEW_A = (
    "synthesis_method is chemical_activation on all twelve rows. The route is two "
    "steps: carbonization of litchi wood at 823 K for 2 h under N2, then KOH "
    "activation at char:KOH 1:4 by mass, 1073 K for 2 h under N2, and it is the "
    "KOH step that creates the porosity. The field held carbonization until "
    "scripts/migrate_relabel.py (docs/migration_relabel_plan.md), because the "
    "vocabulary had no chemical_activation value before schema v1.2. The five "
    "oxidised samples are still NOT split to chemical_oxidation: in this "
    "vocabulary chemical_oxidation is a graphite-oxide-route synthesis value, the "
    "oxidation here is a post-synthesis surface treatment, and splitting would "
    "make the six rows of a controlled single-variable study non-comparable on "
    "the one field saying how the carbon was made."
)
_HYC0019_OLD_B = (
    "The oxidant, concentration, temperature and duration are in "
    "material_description; the vocabulary has no chemical_activation value."
)
_HYC0019_NEW_B = (
    "The oxidant, concentration, temperature and duration are in "
    "material_description."
)

_HYC0022_OLD = (
    "Recorded as 'other' rather than a vocabulary value because the vocabulary "
    "has neither physical_activation nor chemical_activation; the route is in "
    "activation_method."
)
_HYC0022_NEW = (
    "Recorded as 'other' until scripts/migrate_relabel.py "
    "(docs/migration_relabel_plan.md) relabelled the six author-activated rows to "
    "the values schema v1.2 added: physical_activation on the CO2-gasified AC-C2 "
    "and AC-C4, chemical_activation on the KOH-treated AC-K3 and AC-K5. The "
    "mapping is the paper's own taxonomy applied to its own samples - 'The "
    "physical activation involves gasification of the carbon materials in the "
    "presence of suitable oxidizing gasifying agents, such as CO2 and steam' - "
    "and the CO2 samples are the only gas-activated ones here; the exact string "
    "'physical activation' is never printed beside AC-C2 or AC-C4. The conditions "
    "remain in activation_method."
)

_CO2_CAVEAT = (
    " CO2 ACTIVATION REDUCED THE POROSITY, so do not read this row's "
    "physical_activation as implying a higher area: 1585 -> 1488 -> 1308 m2/g and "
    "1.44 -> 1.22 -> 1.10 cm3/g total pore volume across AC, AC-C2, AC-C4, while "
    "the micropore fraction rose from 41% to 49%. The paper says so plainly ('the "
    "destruction of high porosity is more pronounced during the CO2 activation'). "
    "synthesis_method records the route, not its effect."
)

_HYC0027_M3_OLD = "Nitrogen content approximately 7 at% by XPS."
_HYC0027_M3_NEW = (
    "NO NITROGEN CONTENT IS REPORTED FOR THIS SAMPLE. The paper states one "
    "figure, about 7 at% by XPS, and it sits in the XPS discussion whose only "
    "figure (Fig. 4) is captioned as Pd-N-HEG; the Characterization section "
    "describes XPS on the 'nitrogen-doped specimen', singular. "
    "dopant_concentration_at_pct held 7 until scripts/migrate_relabel.py removed "
    "it (docs/migration_relabel_plan.md). N-HEG is Pd-N-HEG's direct precursor so "
    "its nitrogen content is presumably comparable, but a presumption is not a "
    "measurement -- and an XPS surface atomic percentage whose denominator "
    "includes Pd cannot be transferred to a sample with no Pd in it, so N-HEG's "
    "own-basis value would be HIGHER than 7, not equal to it. dopant_element = N "
    "stays: the paper calls the sample nitrogen-doped and describes the plasma "
    "treatment that doped it."
)

_HYC0027_M2_APPEND = (
    " metal_loading_wt_pct = 20 records that nominal as-added loading, which is "
    "the only Pd figure this paper gives for this sample; no XPS or EDX "
    "composition is reported for Pd-HEG anywhere, including the Supporting "
    "Information contents list. The unit is absent from the sentence stating it "
    "('The amount of palladium loading was maintained to be 20 for Pd-N-HEG and "
    "Pd-HEG specimens') and is read as wt% from the 20 wt% EDX and 21 wt% XPS "
    "values for Pd-N-HEG and from Eq. 1, which substitutes q = 0.20 as a weight "
    "fraction."
)

_HYC0027_M4M5_APPEND = (
    " metal_loading_wt_pct = 20 records the EDX value, which agrees with the "
    "nominal loading and with the q = 0.20 weight fraction Eq. 1 uses. The XPS 21 "
    "wt% is NOT what the field holds: XPS is surface-sensitive and over-reads the "
    "bulk loading of a supported nanoparticle, which is the direction of the "
    "discrepancy. dopant_concentration_method = XPS records the basis of the 7 at% "
    "nitrogen."
)

# (kind, key, operation, args) -- kind is "paper" or "row".
NOTES_EDITS: tuple[tuple[str, str, str, tuple[str, ...], int], ...] = (
    ("paper", "HYC-0019", "replace", (_HYC0019_OLD_A, _HYC0019_NEW_A), 12),
    ("paper", "HYC-0019", "replace", (_HYC0019_OLD_B, _HYC0019_NEW_B), 12),
    ("paper", "HYC-0022", "replace", (_HYC0022_OLD, _HYC0022_NEW), 9),
    ("row", "HYC-0022-M2", "append", (_CO2_CAVEAT,), 1),
    ("row", "HYC-0022-M3", "append", (_CO2_CAVEAT,), 1),
    ("row", "HYC-0027-M3", "replace", (_HYC0027_M3_OLD, _HYC0027_M3_NEW), 1),
    ("row", "HYC-0027-M2", "append", (_HYC0027_M2_APPEND,), 1),
    ("row", "HYC-0027-M4", "append", (_HYC0027_M4M5_APPEND,), 1),
    ("row", "HYC-0027-M5", "append", (_HYC0027_M4M5_APPEND,), 1),
)

# Plan §10 and §15: 12 + 9 + 4 = 25 distinct rows have their notes rewritten.
EXPECTED_NOTES_ROWS = 25

# Plan §0 and §15 post-condition 7: the four §12.3 filters, as a union.
UPTAKE_FIELDS = (
    "uptake_wt_pct",
    "uptake_mmol_g",
    "uptake_ml_stp_g",
    "volumetric_capacity_kg_m3",
    "adsorbed_phase_density_kg_m3",
    "areal_uptake_g_cm2",
)


class MigrationError(RuntimeError):
    """Raised when a precondition or post-condition fails. Nothing is written."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _truthy(cell: str) -> bool:
    return cell.strip().lower() in {"true", "1", "yes"}


def read_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise MigrationError(f"{path} is empty")
    return rows[0], rows[1:]


def detect_format(path: Path) -> tuple[str, bool]:
    """Return this file's line terminator and whether it ends with one.

    The dataset is LF with a trailing newline, but that is detected rather than
    assumed. `sync_paper_tracking.py` rewrote the bytes of all 31 lines of a CRLF
    file while leaving every cell value correct, and the cell-level check passed.
    A cell-level verification cannot certify a byte-level guarantee.
    """
    raw = path.read_bytes()
    terminator = "\r\n" if b"\r\n" in raw else "\n"
    return terminator, raw.endswith(b"\n")


def assert_line_mapping_is_sound(raw: bytes, n_rows: int) -> None:
    """Assert physical line n holds data row n-1, which the byte check needs.

    A newline inside a quoted cell breaks the mapping, and `notes` on this corpus
    runs to several thousand characters, so this is a live risk rather than a
    theoretical one. Checked before any row is mapped to a line, because the
    byte-level comparison is unsound -- not merely noisy -- the moment it is false.
    """
    lines = raw.split(b"\n")
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    if len(lines) != n_rows + 1:
        raise MigrationError(
            f"{len(lines)} physical lines for {n_rows} data rows plus a header; "
            f"expected {n_rows + 1}. A cell contains an embedded newline, so "
            f"physical line n does not hold data row n-1 and the byte-level check "
            f"below cannot be trusted."
        )


def check_preconditions(
    header: list[str], rows: list[list[str]], expected_rows: int
) -> dict[str, int]:
    if len(header) != EXPECTED_COLUMNS:
        raise MigrationError(
            f"expected {EXPECTED_COLUMNS} columns, found {len(header)}"
        )
    for name in sorted(SCOPE_COLUMNS | {"measurement_id", "paper_id"}):
        if name not in header:
            raise MigrationError(f"dataset has no {name!r} column")
    if expected_rows >= 0 and len(rows) != expected_rows:
        raise MigrationError(
            f"expected {expected_rows} data rows, found {len(rows)}; "
            f"pass --expected-rows to override"
        )
    ragged = [i for i, row in enumerate(rows, start=2) if len(row) != len(header)]
    if ragged:
        raise MigrationError(f"ragged rows at csv lines {ragged}")

    idx = {name: header.index(name) for name in header}
    by_id = {row[idx["measurement_id"]]: row for row in rows}

    missing = sorted(set(SYNTHESIS_RELABEL) - set(by_id))
    if missing:
        raise MigrationError(f"plan names rows that are not in the dataset: {missing}")
    missing_pd = [mid for mid in PD_ROWS + (NITROGEN_REMOVAL_ROW,) if mid not in by_id]
    if missing_pd:
        raise MigrationError(f"HYC-0027 rows missing from the dataset: {missing_pd}")

    # Refuse to re-run. If any relabel target already holds its new value, this
    # migration has been applied and a second pass would silently double every
    # notes append.
    already = sorted(
        mid
        for mid, value in SYNTHESIS_RELABEL.items()
        if by_id[mid][idx["synthesis_method"]] == value
    )
    if already:
        raise MigrationError(
            f"this migration has already been applied: {len(already)} row(s) "
            f"already hold their new synthesis_method, e.g. {already[:3]}. "
            f"Refusing to run twice."
        )

    # Plan §8. The two excluded papers are asserted, not merely described.
    for paper, reason in MUST_NOT_CHANGE.items():
        in_scope = [
            mid for mid in SYNTHESIS_RELABEL if mid.startswith(f"{paper}-")
        ]
        if in_scope:
            raise MigrationError(
                f"{paper} must not be relabelled ({reason}) but the relabel map "
                f"names {in_scope}"
            )

    counts: dict[str, int] = {}
    for row in rows:
        value = row[idx["synthesis_method"]]
        counts[value] = counts.get(value, 0) + 1
    return counts


def _notes_targets(
    kind: str, key: str, idx: dict[str, int], rows: list[list[str]]
) -> list[list[str]]:
    if kind == "paper":
        return [row for row in rows if row[idx["paper_id"]] == key]
    return [row for row in rows if row[idx["measurement_id"]] == key]


def apply_changes(
    header: list[str], rows: list[list[str]]
) -> tuple[list[list[str]], list[str]]:
    """Return new rows plus a human-readable list of every cell changed."""
    idx = {name: header.index(name) for name in header}
    new_rows = [list(row) for row in rows]
    changes: list[str] = []

    for row in new_rows:
        mid = row[idx["measurement_id"]]

        if mid in SYNTHESIS_RELABEL:
            before = row[idx["synthesis_method"]]
            after = SYNTHESIS_RELABEL[mid]
            row[idx["synthesis_method"]] = after
            changes.append(f"{mid}: synthesis_method {before!r} -> {after!r}")

        if mid in PD_ROWS:
            for column, value in (
                ("metal_element", METAL_ELEMENT),
                ("metal_loading_wt_pct", METAL_LOADING_WT_PCT),
            ):
                before = row[idx[column]]
                if before.strip():
                    raise MigrationError(
                        f"{mid}: {column} already holds {before!r}; this "
                        f"migration only fills empty composition cells"
                    )
                row[idx[column]] = value
                changes.append(f"{mid}: {column} '' -> {value!r}")

        if mid in PD_N_HEG_ROWS:
            before = row[idx["dopant_concentration_method"]]
            if before.strip():
                raise MigrationError(
                    f"{mid}: dopant_concentration_method already holds {before!r}"
                )
            row[idx["dopant_concentration_method"]] = DOPANT_CONCENTRATION_METHOD
            changes.append(
                f"{mid}: dopant_concentration_method '' -> "
                f"{DOPANT_CONCENTRATION_METHOD!r}"
            )

        if mid == NITROGEN_REMOVAL_ROW:
            before = row[idx["dopant_concentration_at_pct"]]
            if not before.strip():
                raise MigrationError(
                    f"{mid}: dopant_concentration_at_pct is already empty; the "
                    f"plan's §9.3 removal has nothing to remove"
                )
            row[idx["dopant_concentration_at_pct"]] = ""
            changes.append(f"{mid}: dopant_concentration_at_pct {before!r} -> ''")

    # Notes, last, so a failure here cannot leave a half-applied composition.
    for kind, key, operation, args, expected in NOTES_EDITS:
        targets = _notes_targets(kind, key, idx, new_rows)
        if len(targets) != expected:
            raise MigrationError(
                f"notes edit on {kind} {key}: expected {expected} row(s), "
                f"found {len(targets)}"
            )
        for row in targets:
            mid = row[idx["measurement_id"]]
            text = row[idx["notes"]]
            if operation == "replace":
                old, new = args
                found = text.count(old)
                if found != 1:
                    raise MigrationError(
                        f"{mid}: the sentence this migration replaces occurs "
                        f"{found} time(s) in notes, expected exactly 1. The plan "
                        f"quotes it verbatim; if the cell has since changed, "
                        f"update the plan before the script."
                    )
                row[idx["notes"]] = text.replace(old, new)
                changes.append(f"{mid}: notes, replaced 1 sentence")
            else:
                (suffix,) = args
                if suffix.strip() in text:
                    raise MigrationError(
                        f"{mid}: notes already contains the text this migration "
                        f"appends; refusing to duplicate it"
                    )
                row[idx["notes"]] = text.rstrip() + suffix
                changes.append(f"{mid}: notes, appended {len(suffix)} chars")

    return new_rows, changes


def verify(
    header: list[str],
    before: list[list[str]],
    after: list[list[str]],
    before_counts: dict[str, int],
    expected_changed_cells: int | None = DEFAULT_EXPECTED_CHANGED_CELLS,
) -> int:
    """Assert every post-condition in plan §15 and return the changed-cell count.

    The count is returned rather than printed by the caller's own tally because
    those two numbers are not the same: a row whose `notes` takes two substring
    replacements produces two log lines and one changed cell. Reporting the log
    length as a cell count would overstate the edit by 14.
    """
    idx = {name: header.index(name) for name in header}
    strict = expected_changed_cells is not None

    # 1. Shape unchanged.
    if len(after) != len(before):
        raise MigrationError(f"row count changed: {len(before)} -> {len(after)}")

    # 2. Only the scoped columns changed.
    changed: list[tuple[int, str, str]] = []
    for line, (old, new) in enumerate(zip(before, after), start=2):
        if len(old) != len(new):
            raise MigrationError(f"column count changed on csv line {line}")
        for col, (a, b) in enumerate(zip(old, new)):
            if a != b:
                changed.append((line, header[col], new[idx["measurement_id"]]))
    illegal = [
        (line, col, mid) for line, col, mid in changed if col not in SCOPE_COLUMNS
    ]
    if illegal:
        raise MigrationError(f"cells changed outside the plan's scope: {illegal}")
    if strict and len(changed) != expected_changed_cells:
        by_col: dict[str, int] = {}
        for _, col, _mid in changed:
            by_col[col] = by_col.get(col, 0) + 1
        raise MigrationError(
            f"expected {expected_changed_cells} changed cells, found "
            f"{len(changed)}: {by_col}"
        )

    def counts_of(rows: list[list[str]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for row in rows:
            value = row[idx["synthesis_method"]]
            out[value] = out.get(value, 0) + 1
        return out

    after_counts = counts_of(after)

    # 3. The synthesis_method DELTAS, not absolute totals.
    for value, delta in EXPECTED_SYNTHESIS_DELTAS.items():
        got = after_counts.get(value, 0) - before_counts.get(value, 0)
        if got != delta:
            raise MigrationError(
                f"synthesis_method {value!r} moved by {got:+d}, expected "
                f"{delta:+d} (before {before_counts.get(value, 0)}, after "
                f"{after_counts.get(value, 0)})"
            )
    untouched = (set(before_counts) | set(after_counts)) - set(
        EXPECTED_SYNTHESIS_DELTAS
    )
    drifted = {
        v: (before_counts.get(v, 0), after_counts.get(v, 0))
        for v in untouched
        if before_counts.get(v, 0) != after_counts.get(v, 0)
    }
    if drifted:
        raise MigrationError(
            f"synthesis_method values outside the plan changed count: {drifted}"
        )

    # 4. Exactly the 36 named rows changed synthesis_method, and to the named value.
    relabelled = {
        new[idx["measurement_id"]]: new[idx["synthesis_method"]]
        for old, new in zip(before, after)
        if old[idx["synthesis_method"]] != new[idx["synthesis_method"]]
    }
    if relabelled != SYNTHESIS_RELABEL:
        unexpected = sorted(set(relabelled) - set(SYNTHESIS_RELABEL))
        missed = sorted(set(SYNTHESIS_RELABEL) - set(relabelled))
        wrong = {
            mid: (relabelled[mid], SYNTHESIS_RELABEL[mid])
            for mid in set(relabelled) & set(SYNTHESIS_RELABEL)
            if relabelled[mid] != SYNTHESIS_RELABEL[mid]
        }
        raise MigrationError(
            f"relabelled set does not match the plan: {len(unexpected)} "
            f"unexpected {unexpected[:5]}, {len(missed)} missed {missed[:5]}, "
            f"{len(wrong)} wrong value {dict(list(wrong.items())[:3])}"
        )

    # 5. physical_activation stops being an untested vocabulary value.
    if strict and before_counts.get("physical_activation", 0) != 0:
        raise MigrationError(
            "physical_activation already had rows before this migration; the "
            "plan's §1 claim that it was untested is false"
        )
    if after_counts.get("physical_activation", 0) != 2:
        raise MigrationError(
            f"expected 2 physical_activation rows after, found "
            f"{after_counts.get('physical_activation', 0)}"
        )

    # 6. carbonization is left on exactly the two control rows.
    survivors = {
        row[idx["measurement_id"]]
        for row in after
        if row[idx["synthesis_method"]] == "carbonization"
    }
    if strict and survivors != set(CARBONIZATION_SURVIVORS):
        raise MigrationError(
            f"carbonization should be left on exactly "
            f"{sorted(CARBONIZATION_SURVIVORS)}, found {sorted(survivors)}"
        )

    # 7. metal_loading_wt_pct gains exactly the three Pd rows, all of which
    #    survive the four §12.3 filters -- the condition gap 7 was added for.
    loaded_before = {
        row[idx["measurement_id"]]
        for row in before
        if row[idx["metal_loading_wt_pct"]].strip()
    }
    loaded_after = {
        row[idx["measurement_id"]]
        for row in after
        if row[idx["metal_loading_wt_pct"]].strip()
    }
    if loaded_after - loaded_before != set(PD_ROWS):
        raise MigrationError(
            f"metal_loading_wt_pct should gain exactly {sorted(PD_ROWS)}, gained "
            f"{sorted(loaded_after - loaded_before)}"
        )
    if loaded_before - loaded_after:
        raise MigrationError(
            f"metal_loading_wt_pct lost rows: {sorted(loaded_before - loaded_after)}"
        )
    eligible = {
        row[idx["measurement_id"]]
        for row in after
        if row[idx["metal_loading_wt_pct"]].strip()
        and survives_analysis_filters(row, idx)
    }
    if eligible != set(PD_ROWS):
        raise MigrationError(
            f"expected exactly {sorted(PD_ROWS)} to carry a metal loading and "
            f"survive the §12.3 filters, found {sorted(eligible)}"
        )

    # 8. The nitrogen removal hits one row and nothing else.
    at_pct_before = {
        row[idx["measurement_id"]]
        for row in before
        if row[idx["dopant_concentration_at_pct"]].strip()
    }
    at_pct_after = {
        row[idx["measurement_id"]]
        for row in after
        if row[idx["dopant_concentration_at_pct"]].strip()
    }
    if at_pct_before - at_pct_after != {NITROGEN_REMOVAL_ROW}:
        raise MigrationError(
            f"dopant_concentration_at_pct should lose exactly "
            f"{NITROGEN_REMOVAL_ROW}, lost {sorted(at_pct_before - at_pct_after)}"
        )
    if at_pct_after - at_pct_before:
        raise MigrationError(
            f"dopant_concentration_at_pct gained rows: "
            f"{sorted(at_pct_after - at_pct_before)}"
        )
    hyc0027_at_pct = {mid for mid in at_pct_after if mid.startswith("HYC-0027-")}
    if hyc0027_at_pct != set(PD_N_HEG_ROWS):
        raise MigrationError(
            f"within HYC-0027, dopant_concentration_at_pct should survive on "
            f"exactly {sorted(PD_N_HEG_ROWS)}, found {sorted(hyc0027_at_pct)}"
        )

    # 9. A metal loading always names its element.
    nameless = [
        row[idx["measurement_id"]]
        for row in after
        if row[idx["metal_loading_wt_pct"]].strip()
        and not row[idx["metal_element"]].strip()
    ]
    if nameless:
        raise MigrationError(
            f"rows carry a metal loading with no metal_element: {nameless}"
        )

    # 10. notes changed on exactly the expected rows.
    notes_changed = {
        new[idx["measurement_id"]]
        for old, new in zip(before, after)
        if old[idx["notes"]] != new[idx["notes"]]
    }
    if strict and len(notes_changed) != EXPECTED_NOTES_ROWS:
        raise MigrationError(
            f"notes changed on {len(notes_changed)} rows, expected "
            f"{EXPECTED_NOTES_ROWS}"
        )
    stale = sorted(
        new[idx["measurement_id"]]
        for new in after
        if "the vocabulary has neither physical_activation" in new[idx["notes"]]
        or "the vocabulary has no chemical_activation value" in new[idx["notes"]]
        or "synthesis_method stays carbonization" in new[idx["notes"]]
    )
    if stale:
        raise MigrationError(
            f"notes still assert the pre-v1.2 vocabulary on {len(stale)} row(s): "
            f"{stale[:5]}"
        )

    return len(changed)


def survives_analysis_filters(row: list[str], idx: dict[str, int]) -> bool:
    """Evaluate the four §12.3 exclusions as a union, on one raw CSV row."""
    mode = row[idx["measurement_mode"]].strip() or "isothermal"
    if mode != "isothermal":
        return False
    if (row[idx["uptake_bound"]].strip() or "exact") != "exact":
        return False
    if _truthy(row[idx["temperature_unstated"]]) or _truthy(
        row[idx["pressure_unstated"]]
    ):
        return False
    return any(row[idx[name]].strip() for name in UPTAKE_FIELDS)


def write_rows(
    path: Path,
    header: list[str],
    rows: list[list[str]],
    terminator: str,
    ends_with_terminator: bool,
) -> None:
    """Write the file back in its own line-ending convention."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator=terminator)
    writer.writerow(header)
    writer.writerows(rows)
    text = buffer.getvalue()
    if not ends_with_terminator and text.endswith(terminator):
        text = text[: -len(terminator)]
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def assert_untouched_lines_are_byte_identical(
    before_bytes: bytes, after_bytes: bytes, changed_lines: set[int]
) -> None:
    """Assert every line the plan does not name is byte-for-byte unchanged.

    verify() compares parsed cells, which cannot see a line-ending or quoting
    change. This compares raw lines, which can. `changed_lines` is 1-indexed over
    physical lines, header = line 1.
    """
    before = before_bytes.split(b"\n")
    after = after_bytes.split(b"\n")
    if len(before) != len(after):
        raise MigrationError(
            f"physical line count changed: {len(before)} -> {len(after)}. "
            f"A trailing-newline change does this."
        )
    drifted = [
        i
        for i, (a, b) in enumerate(zip(before, after), start=1)
        if a != b and i not in changed_lines
    ]
    if drifted:
        raise MigrationError(
            f"{len(drifted)} line(s) changed bytes without changing any cell this "
            f"migration names, at physical lines {drifted[:10]}. This is a "
            f"line-ending or quoting rewrite, not a cell edit."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_BACKUP_DIR)
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=DEFAULT_EXPECTED_ROWS,
        help="row count guard; -1 disables it (used by the tests)",
    )
    parser.add_argument(
        "--expected-changed-cells",
        type=int,
        default=DEFAULT_EXPECTED_CHANGED_CELLS,
        help="changed-cell guard; -1 disables it (used by the tests)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if not args.dataset.exists():
            raise MigrationError(f"{args.dataset} does not exist")

        before_bytes = args.dataset.read_bytes()
        terminator, ends_with_terminator = detect_format(args.dataset)
        header, rows = read_rows(args.dataset)
        assert_line_mapping_is_sound(before_bytes, len(rows))
        before_counts = check_preconditions(header, rows, args.expected_rows)

        new_rows, changes = apply_changes(header, rows)
        expected_cells = (
            None if args.expected_changed_cells < 0 else args.expected_changed_cells
        )
        changed_cells = verify(
            header, rows, new_rows, before_counts, expected_cells
        )

        changed_lines = {
            i + 1
            for i, (old, new) in enumerate(zip(rows, new_rows), start=1)
            if old != new
        }

        print(
            f"{changed_cells} cell(s) changed across {len(changed_lines)} line(s) "
            f"in {len(changes)} operation(s); line terminator {terminator!r}, "
            f"trailing newline {ends_with_terminator}"
        )
        for line in changes:
            print(f"  {line}")

        if args.dry_run:
            print("\n--dry-run: nothing written.")
            return 0

        stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        backup = args.backup_dir / f"measurements.pre_relabel.{stamp}.csv"
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.dataset, backup)
        print(f"\nbacked up to {backup}")

        write_rows(args.dataset, header, new_rows, terminator, ends_with_terminator)

        # Re-read from disk and re-verify. A self-report is not evidence (§3.8).
        header_after, rows_after = read_rows(args.dataset)
        if header_after != header:
            raise MigrationError("header changed on write")
        verify(header, rows, rows_after, before_counts, expected_cells)
        assert_untouched_lines_are_byte_identical(
            before_bytes, args.dataset.read_bytes(), changed_lines
        )

        print(f"wrote {args.dataset}, re-read and re-verified from disk")
        print(f"sha256 {_sha256(args.dataset)}")
        return 0

    except MigrationError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
