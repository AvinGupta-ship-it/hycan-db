"""
Day-7 data-validation pipeline for HyCAN-DB.

This module classifies problems in measurement rows according to the curation
manual §11.3, which is the *source of truth* for the error/warning split. The
Pydantic :class:`~hycan.schema.MeasurementEntry` model is used only for three
things — type checks, controlled-vocabulary checks, and required-field presence.
Its numeric *range* constraints (e.g. ``pressure_bar <= 200``) are deliberately
ignored here, because §11.3 sometimes classifies an out-of-range value as a mere
*warning* rather than an error (e.g. pressure above 200 bar). Range logic is
therefore re-implemented below so the §11.3 classification always wins.

Design rules:
- ``validate_row`` is pure: it reads a dict and returns a :class:`ValidationResult`.
- ``validate_dataset`` runs every row, then layers on the two dataset-level checks
  (duplicate ``measurement_id`` -> error; conflicting DOI metadata -> warning).
  ``sample_id`` may repeat: one physical sample can be measured under many
  conditions, so it is no longer the dataset-level uniqueness key.
- ``print_report`` renders the fixed report shape that
  ``scripts/validate_data.py`` consumes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from itertools import combinations

import pandas as pd
from pydantic import ValidationError

from hycan.normalize import ml_stp_per_g_to_wt_pct, mmol_per_g_to_wt_pct
from hycan.schema import MeasurementEntry

# Pydantic error ``type`` strings that correspond to numeric-range constraints.
# These are ignored on purpose — the §11.3 rules below own all range logic.
_RANGE_ERROR_TYPES = frozenset(
    {
        "greater_than",
        "greater_than_equal",
        "less_than",
        "less_than_equal",
        "multiple_of",
        "finite_number",
    }
)

# Carbon-nanotube material classes used by the Tier-D pre-2005 rule.
_CNT_CLASSES = frozenset({"SWCNT", "MWCNT", "DWCNT"})


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Outcome of validating a single row."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class DatasetValidationReport:
    """Aggregate outcome of validating a whole dataset."""

    total: int
    results: list[ValidationResult] = field(default_factory=list)
    error_counts: dict[str, int] = field(default_factory=dict)
    warning_counts: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Small value helpers
# ---------------------------------------------------------------------------

def _is_na(value) -> bool:
    """True for ``None``/NaN/pandas-NA scalars (i.e. an absent CSV cell)."""
    if value is None:
        return True
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def _to_float(value):
    """Best-effort float coercion; returns ``None`` for missing/non-numeric input."""
    if _is_na(value):
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f):
        return None
    return f


def _to_int(value):
    """Best-effort int coercion; returns ``None`` for missing/non-numeric input."""
    f = _to_float(value)
    if f is None:
        return None
    return int(f)


def _category(message: str) -> str:
    """The category of a message = the text before the first colon."""
    return message.split(":", 1)[0].strip()


def _append_unique(target: list[str], message: str) -> None:
    """Append *message* to *target* unless it is already present (de-dup)."""
    if message not in target:
        target.append(message)


# ---------------------------------------------------------------------------
# Schema-based checks (type / vocabulary / required-field presence only)
# ---------------------------------------------------------------------------

# Schema v1.2 (gap 4). Two reported uptakes disagree only if they differ by
# more than 5% relatively AND more than 0.02 wt% absolutely. Either test alone
# is wrong: relative-only fires on reporting rounding near zero (see the note
# in validate_row), and absolute-only would miss a real disagreement between
# two large values.
_UPTAKE_REL_TOLERANCE = 0.05
_UPTAKE_ABS_TOLERANCE_WT_PCT = 0.02

# v1.3 gaps 3 and 6. Same relative-AND-absolute discipline, for the same reason.
# The absolute floors are set from how the corpus's papers actually round:
# HYC-0007 reports surface areas to the nearest 10 m2/g, so 50 m2/g is five
# rounding steps and a genuine parts-vs-whole disagreement is far larger than
# that. Pore volumes are reported to two decimals, so 0.05 cm3/g is five steps.
# Both are deliberately generous: these checks exist to catch a field holding the
# wrong quantity, not to police a paper's arithmetic.
_AREA_SUM_REL_TOLERANCE = 0.10
_AREA_SUM_ABS_TOLERANCE_M2_G = 50.0
_PORE_SUM_REL_TOLERANCE = 0.10
_PORE_SUM_ABS_TOLERANCE_CM3_G = 0.05


def _uptakes_disagree(left: float, right: float) -> bool:
    difference = abs(left - right)
    if difference <= _UPTAKE_ABS_TOLERANCE_WT_PCT:
        return False
    denominator = max(abs(left), abs(right), 1e-9)
    return difference / denominator > _UPTAKE_REL_TOLERANCE


def _schema_errors(clean: dict) -> list[str]:
    """Run the Pydantic model and return only §11.3-relevant schema errors.

    Numeric-range violations are dropped (the range rules below handle those);
    everything else is mapped to a "Missing required field" or "Invalid value"
    message.
    """
    messages: list[str] = []
    try:
        MeasurementEntry.model_validate(clean)
    except ValidationError as exc:
        for err in exc.errors():
            etype = err["type"]
            loc = err["loc"]
            field_name = str(loc[0]) if loc else ""
            if etype in _RANGE_ERROR_TYPES:
                # Owned by the §11.3 range rules — ignore the schema's bound.
                continue
            if etype == "missing":
                _append_unique(messages, f"Missing required field: {field_name}")
            elif etype == "value_error":
                # Raised by the model-level "at least one uptake" validator.
                _append_unique(messages, "Missing required field: uptake")
            else:
                # Wrong type or value outside a controlled vocabulary.
                _append_unique(messages, f"Invalid value: {field_name}")
    return messages


# ---------------------------------------------------------------------------
# Row validation
# ---------------------------------------------------------------------------

def validate_row(row: dict) -> ValidationResult:
    """Validate a single measurement row against the §11.3 rules."""
    # Drop absent cells so the schema reports them as "missing" (not None-typed
    # values) and so defaults apply to optional/defaulted fields.
    clean = {k: v for k, v in row.items() if not _is_na(v)}

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Schema: type / vocabulary / required-field presence.
    for msg in _schema_errors(clean):
        _append_unique(errors, msg)

    # 2. §11.3 range rules (these own everything numeric).
    temp = _to_float(clean.get("temperature_k"))
    if temp is not None and (temp < 50 or temp > 500):
        _append_unique(errors, "Temperature out of range")

    pressure = _to_float(clean.get("pressure_bar"))
    if pressure is not None:
        if pressure <= 0:
            _append_unique(errors, "Pressure out of range")
        elif pressure > 200:
            _append_unique(warnings, "Pressure above 200 bar")

    wt = _to_float(clean.get("uptake_wt_pct"))
    if wt is not None:
        if wt > 20:
            _append_unique(errors, "Uptake out of range")
        elif wt > 10:
            _append_unique(warnings, "Uptake above 10 wt%")

    # 3. §11.3 categorical / cross-field warnings.
    if clean.get("uptake_type") == "unspecified":
        _append_unique(warnings, "Unspecified uptake_type")

    # Pore-volume nesting (§11.1 cross-field, §8.5 gap 4).
    #
    # Ultra-micropores (below ~0.7 nm) are a subset of micropores (below 2 nm),
    # which are a subset of total pore volume. A violation is a transcription
    # error or a misread column, not a physical result, so these are ERRORs —
    # matching §11.2, which has always specified ERROR for the micropore/total
    # pair even though the v1.0 code raised it as a warning. No row in the
    # corpus violates any of the three, so the severity change affects nothing
    # currently in the dataset.
    #
    # The pairs are checked independently so that a missing middle term does
    # not suppress the outer comparison.
    ultramicropore = _to_float(clean.get("ultramicropore_volume_cm3_g"))
    micropore = _to_float(clean.get("micropore_volume_cm3_g"))
    total_pore = _to_float(clean.get("total_pore_volume_cm3_g"))

    mesopore = _to_float(clean.get("mesopore_volume_cm3_g"))

    for smaller, larger, label in (
        (ultramicropore, micropore, "Ultramicropore volume exceeds micropore volume"),
        (ultramicropore, total_pore, "Ultramicropore volume exceeds total pore volume"),
        (micropore, total_pore, "Micropore volume exceeds total pore volume"),
        # v1.3 gap 6. A mesopore volume nests inside the total the same way.
        (mesopore, total_pore, "Mesopore volume exceeds total pore volume"),
    ):
        if smaller is not None and larger is not None and smaller > larger:
            _append_unique(errors, label)

    # v1.3 gap 6. Micropore + mesopore must not exceed the total beyond rounding.
    # A WARNING rather than an ERROR: papers round pore volumes to two decimals
    # and a third pore class (macropore) may be unreported, so a small excess is
    # a reporting artifact while a large one means the fields disagree.
    if micropore is not None and mesopore is not None and total_pore is not None:
        summed = micropore + mesopore
        excess = summed - total_pore
        if (
            excess > _PORE_SUM_ABS_TOLERANCE_CM3_G
            and excess / max(total_pore, 1e-9) > _PORE_SUM_REL_TOLERANCE
        ):
            _append_unique(
                warnings, "Micropore plus mesopore volume exceeds total pore volume"
            )

    # v1.3 gap 3. When a paper reports a micropore and an external surface area
    # AND a headline total, the parts should account for the whole. Relative AND
    # absolute, both must be exceeded: relative-only was the false positive that
    # produced v1.2's removed warning type, and HYC-0007 rounds its areas to the
    # nearest 10 m2/g. No corpus row currently populates all three, checked
    # before this was written, so this cannot fire today.
    micropore_area = _to_float(clean.get("micropore_surface_area_m2_g"))
    external_area = _to_float(clean.get("external_surface_area_m2_g"))
    total_area = _to_float(clean.get("bet_surface_area_m2_g"))
    if (
        micropore_area is not None
        and external_area is not None
        and total_area is not None
    ):
        difference = abs((micropore_area + external_area) - total_area)
        if (
            difference > _AREA_SUM_ABS_TOLERANCE_M2_G
            and difference / max(total_area, 1e-9) > _AREA_SUM_REL_TOLERANCE
        ):
            _append_unique(
                warnings,
                "Micropore plus external surface area inconsistent with total",
            )

    material_class = clean.get("material_class")
    description = clean.get("material_description")
    if (
        material_class == "SWCNT"
        and isinstance(description, str)
        and "single-walled" not in description.lower()
    ):
        _append_unique(warnings, "SWCNT description missing 'single-walled'")

    # Schema v1.2 (gap 4). A row may carry the same uptake in up to three
    # units, and those values can contradict each other: HYC-0009 tabulates a
    # wt% and a volumetric uptake per measurement that disagree by a factor of
    # 2.0-2.6, not constant across rows. Before v1.2 only the wt%-vs-mmol/g
    # pair was checked, so that contradiction had to be caught by a human
    # reader instead of by this function. All three pairs are now compared.
    #
    # The tolerance is deliberately relative AND absolute. The pre-v1.2 check
    # was relative-only, and the corpus's single
    # "mmol/g and wt% inconsistent" warning was a false positive produced by
    # that: HYC-0004-M2 reports 0.05 wt% and 0.268 mmol/g, and 0.268 mmol/g is
    # 0.0540 wt%, which rounds to 0.05 at the paper's own precision. An
    # absolute difference of 0.004 wt% is an 8% relative difference at that
    # magnitude. Every row in the corpus carrying two uptake units agrees to
    # better than 0.004 wt% absolute; only this row's values are small enough
    # for that to clear 5% relative. Fixing it removes a warning type from the
    # §11.5 baseline, which docs/migration_v1_2_plan.md §1 states explicitly.
    #
    # 0.02 wt% is an order of magnitude below the smallest uptake anyone would
    # analyse and an order of magnitude above two-significant-figure rounding.
    mmol = _to_float(clean.get("uptake_mmol_g"))
    ml_stp = _to_float(clean.get("uptake_ml_stp_g"))

    as_wt_pct: list[tuple[str, float]] = []
    if wt is not None:
        as_wt_pct.append(("wt%", wt))
    if mmol is not None:
        try:
            as_wt_pct.append(("mmol/g", mmol_per_g_to_wt_pct(mmol)))
        except ValueError:
            pass
    if ml_stp is not None:
        try:
            as_wt_pct.append(("mL(STP)/g", ml_stp_per_g_to_wt_pct(ml_stp)))
        except ValueError:
            pass

    for (left_name, left), (right_name, right) in combinations(as_wt_pct, 2):
        if _uptakes_disagree(left, right):
            # Label orientation matches the pre-v1.2 string exactly so the
            # existing §11.5 baseline entry is not renamed by accident.
            _append_unique(
                warnings, f"{right_name} and {left_name} inconsistent"
            )

    year = _to_int(clean.get("year"))
    if (
        year is not None
        and year < 2005
        and material_class in _CNT_CLASSES
        and wt is not None
        and wt > 5
    ):
        _append_unique(warnings, "Pre-2005 raw-CNT high uptake (Tier D)")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


# ---------------------------------------------------------------------------
# Dataset validation
# ---------------------------------------------------------------------------

def _row_dicts(df: pd.DataFrame) -> list[dict]:
    """Convert a DataFrame to a list of row dicts (NaN cells preserved as NaN)."""
    return df.to_dict(orient="records")


def validate_dataset(df: pd.DataFrame) -> DatasetValidationReport:
    """Validate every row, then apply the two dataset-level checks."""
    rows = _row_dicts(df)
    results = [validate_row(r) for r in rows]

    # --- Dataset check 1: duplicate measurement_id -> ERROR on every offending row.
    # measurement_id is the unique-per-row key; sample_id MAY repeat (one physical
    # sample measured under multiple conditions), so it is not checked here.
    measurement_ids: dict[str, list[int]] = {}
    for idx, r in enumerate(rows):
        mid = r.get("measurement_id")
        if _is_na(mid):
            continue
        measurement_ids.setdefault(str(mid), []).append(idx)
    for mid, idxs in measurement_ids.items():
        if len(idxs) > 1:
            for idx in idxs:
                _append_unique(results[idx].errors, f"Duplicate measurement_id: {mid}")
                results[idx].is_valid = False

    # --- Dataset check 1b (v1.3 gap 3): surface_area_method used consistently.
    #
    # ERROR, and deliberately at dataset level rather than per row, because the
    # distinction is not row-local:
    #
    #   unspecified  - an area IS reported, method not stated.
    #   none         - the PAPER reports no area for any sample.
    #   not_reported - THIS sample has none, in a paper that reports areas for
    #                  its others.
    #
    # Whether a paper "reports areas for its others" is a fact about the paper's
    # other rows, so a model validator on one row cannot check it at all. Before
    # v1.3 all three collapsed onto `unspecified` and 24 rows sat there with an
    # empty area field, indistinguishable from a measured area whose method the
    # paper omitted. These checks are what stop that decaying back on the next
    # append.
    papers_with_any_area: set[str] = set()
    for r in rows:
        if _present(r.get("bet_surface_area_m2_g")) or _present(
            r.get("micropore_surface_area_m2_g")
        ) or _present(r.get("langmuir_surface_area_m2_g")) or _present(
            r.get("external_surface_area_m2_g")
        ):
            papers_with_any_area.add(str(r.get("paper_id")))

    for idx, r in enumerate(rows):
        method = r.get("surface_area_method")
        has_area = any(
            _present(r.get(f))
            for f in (
                "bet_surface_area_m2_g",
                "langmuir_surface_area_m2_g",
                "micropore_surface_area_m2_g",
                "external_surface_area_m2_g",
            )
        )
        paper = str(r.get("paper_id"))
        if method == "unspecified" and not has_area:
            _append_unique(
                results[idx].errors,
                "surface_area_method is 'unspecified' with no area recorded; "
                "use 'none' if the paper reports none at all, or "
                "'not_reported' if only this sample lacks one",
            )
            results[idx].is_valid = False
        elif method == "not_reported" and paper not in papers_with_any_area:
            _append_unique(
                results[idx].errors,
                "surface_area_method is 'not_reported' but this paper reports no "
                "surface area for any sample; 'none' is the correct value",
            )
            results[idx].is_valid = False
        elif method == "none" and paper in papers_with_any_area:
            _append_unique(
                results[idx].errors,
                "surface_area_method is 'none' but this paper does report a "
                "surface area for another sample; 'not_reported' is the correct "
                "value for a sample that lacks one",
            )
            results[idx].is_valid = False

    # --- Dataset check 2: DOI metadata conflict -> WARNING on every offending row.
    doi_groups: dict[str, list[int]] = {}
    for idx, r in enumerate(rows):
        doi = r.get("doi")
        if _is_na(doi):
            continue
        doi_groups.setdefault(str(doi), []).append(idx)
    for doi, idxs in doi_groups.items():
        authors = {str(rows[i].get("first_author")) for i in idxs}
        years = {str(rows[i].get("year")) for i in idxs}
        if len(authors) > 1 or len(years) > 1:
            for idx in idxs:
                _append_unique(
                    results[idx].warnings, f"DOI metadata conflict: {doi}"
                )

    # --- Aggregate counts by category.
    error_counts: dict[str, int] = {}
    warning_counts: dict[str, int] = {}
    for res in results:
        for msg in res.errors:
            cat = _category(msg)
            error_counts[cat] = error_counts.get(cat, 0) + 1
        for msg in res.warnings:
            cat = _category(msg)
            warning_counts[cat] = warning_counts.get(cat, 0) + 1

    return DatasetValidationReport(
        total=len(results),
        results=results,
        error_counts=error_counts,
        warning_counts=warning_counts,
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(report: DatasetValidationReport) -> None:
    """Print the fixed-shape validation report to stdout."""
    rows_valid = sum(1 for r in report.results if r.is_valid)
    rows_with_errors = sum(1 for r in report.results if r.errors)
    rows_with_warnings = sum(1 for r in report.results if r.warnings)

    lines = [
        "HyCAN-DB Validation Report",
        "==========================",
        f"Rows total: {report.total}",
        f"Rows valid: {rows_valid}",
        f"Rows with errors: {rows_with_errors}",
        f"Rows with warnings: {rows_with_warnings}",
        "Errors by type:",
    ]
    if report.error_counts:
        for cat in sorted(report.error_counts):
            lines.append(f"- {cat}: {report.error_counts[cat]}")
    else:
        lines.append("- none")

    lines.append("Warnings by type:")
    if report.warning_counts:
        for cat in sorted(report.warning_counts):
            lines.append(f"- {cat}: {report.warning_counts[cat]}")
    else:
        lines.append("- none")

    print("\n".join(lines))


# ---------------------------------------------------------------------------
# Reproducibility tiering (see docs/reproducibility_tiering.md)
# ---------------------------------------------------------------------------

def _present(v) -> bool:
    """True unless *v* is None, a float NaN, or an empty/whitespace-only string."""
    if v is None:
        return False
    if isinstance(v, float) and math.isnan(v):
        return False
    if str(v).strip() == "":
        return False
    return True


def _derive_wt_pct(row) -> float | None:
    """Derive uptake in wt% from whichever uptake field is present, else None."""
    if _present(row.get("uptake_wt_pct")):
        return float(row["uptake_wt_pct"])
    elif _present(row.get("uptake_mmol_g")):
        return float(row["uptake_mmol_g"]) * 0.201588
    elif _present(row.get("uptake_ml_stp_g")):
        # Project STP convention: 22.414 mL/mmol.
        return (float(row["uptake_ml_stp_g"]) / 22.414) * 0.201588
    else:
        return None


_ANY_UPTAKE_FIELDS = (
    "uptake_wt_pct",
    "uptake_mmol_g",
    "uptake_ml_stp_g",
    "volumetric_capacity_kg_m3",
    "adsorbed_phase_density_kg_m3",
    "areal_uptake_g_cm2",
)


def _score_bet(row: dict) -> tuple[int, str]:
    """Score "BET surface area reported and consistent with material class", 0-2.

    The three-level scale is the one ``docs/reproducibility_tiering.md``'s second
    worked example already specifies -- "BET 1 (surface area reported but not
    BET)". The code awarded 2 for any positive area and 0 otherwise, which was
    wrong in both directions: 0 for HYC-0007, which reports eighteen surface-area
    values by a named method resolved into micropore and external components with
    no total, and 2 for the 31 rows whose area §8.6 recorded as *not known to be
    BET*.

    A missing ``surface_area_method`` key is read as the schema default
    ``unspecified``; a dataset row always carries the field.
    """
    area = row.get("bet_surface_area_m2_g")
    has_area = _present(area) and float(area) > 0
    method = row.get("surface_area_method") or "unspecified"
    if has_area and method == "BET":
        return 2, "bet_total"
    if has_area:
        return 1, f"area_by_{method}"
    micro, ext = (
        row.get("micropore_surface_area_m2_g"),
        row.get("external_surface_area_m2_g"),
    )
    if _present(micro) and _present(ext):
        return 1, "resolved_components"
    langmuir = row.get("langmuir_surface_area_m2_g")
    if _present(langmuir) and float(langmuir) > 0:
        return 1, "langmuir_only"
    return 0, "no_area"


def _score_purity(row: dict) -> tuple[int, str]:
    """Score "sample purity / impurity content reported", 0-1.

    The criterion is about purity being *reported*, and the code tested whether
    the sample had been *purified*. HYC-0007 shows the difference: its pristine
    SWCNT scored 0 while the paper reports 11 wt% residual metal for it, and its
    acid-treated sample scored 1 for having been treated. A reported residual
    metal content is the strongest evidence and is checked first; the purification
    proxy is kept, so this can only ever turn a 0 into a 1.
    """
    if _present(row.get("residual_metal_wt_pct")):
        return 1, "residual_metal_measured"
    if _present(row.get("residual_metal_element")):
        return 1, "residual_metal_named"
    if _present(row.get("purification_method")):
        return 1, "purification_method"
    return 0, "none"


def _chahine_bounding_area(row: dict) -> tuple[float | None, str]:
    """Return the surface area to bound uptake against, and where it came from.

    Falls back to the sum of the resolved components, which is what an alpha-s
    decomposition means and what this module's own dataset-level check already
    assumes when it verifies that components sum to a stated total.

    **A Langmuir area is deliberately NOT used here**, though it earns a point in
    ``_score_bet``. A Langmuir fit systematically over-reads on a microporous
    carbon, so using it would raise the expected value and loosen the bound --
    hiding exactly the over-claims this criterion exists to catch. Erring toward
    "cannot assess" is the safe direction.
    """
    area = row.get("bet_surface_area_m2_g")
    if _present(area) and float(area) > 0:
        return float(area), "bet_total"
    micro, ext = (
        row.get("micropore_surface_area_m2_g"),
        row.get("external_surface_area_m2_g"),
    )
    if _present(micro) and _present(ext):
        return float(micro) + float(ext), "component_sum"
    return None, "no_area"


def _score_chahine(row: dict) -> tuple[int, str]:
    """Score "value within Chahine-consistent range for the stated conditions", 0-2.

    **The un-assessable case is three cases, and only two of them deserve a
    point.** The pre-v1.3 code collapsed them into one ``chahine = 1``, which
    handed a free point to every row whose paper never stated a temperature --
    §13.7. The consequence was concrete: HYC-0011's ordinary 0.26 wt% row and its
    discredited 8.0 wt% row scored identically, so the one value the criterion
    exists to catch was the one it could not see.

    * No uptake of any kind -> 1. The criterion has no subject. Not a reporting
      failure by the paper.
    * Uptake present but not convertible to wt% (HYC-0024's volumetric-only rows)
      -> 1. The Chahine rule is defined in wt%; this genuinely cannot be assessed.
    * Uptake in wt% but no stated temperature -> **0**. The criterion reads "for
      the stated conditions" and there are none. That is a reporting deficiency
      and it scores as one.

    Pressure is deliberately not penalized here: an unstated pressure already
    costs the ``temp_pressure`` point, and the bound below is pressure-blind at
    every temperature, so it does not prevent evaluation. See the plan's §7 for
    why that pressure-blindness is itself a limitation.
    """
    t = row.get("temperature_k")
    w = _derive_wt_pct(row)
    if w is None:
        any_uptake = any(_present(row.get(f)) for f in _ANY_UPTAKE_FIELDS)
        if not any_uptake:
            return 1, "not_applicable_no_uptake"
        return 1, "not_assessable_non_gravimetric"
    if not _present(t):
        return 0, "temperature_not_reported"
    if float(t) >= 273:
        # room-temperature physisorption bound ~1 wt%
        return (2 if w <= 1.0 else (1 if w <= 2.0 else 0)), "room_temp_bound"
    if float(t) <= 100:
        area, area_basis = _chahine_bounding_area(row)
        if area is None:
            return 1, "cryo_no_area"
        expected = area / 500.0
        points = 0 if w > 1.5 * expected else (1 if w > expected else 2)
        return points, f"cryo_vs_{area_basis}"
    return (0 if w > 6.0 else 2), "mid_temp_bound"


def score_reproducibility(row: dict) -> dict:
    """Apply the 10-point reproducibility rubric to a row's present fields.

    Returns per-criterion points plus the derived wt%, the total, and the
    suggested tier. This is an approximate scorer; see :func:`suggest_tier`
    and ``docs/reproducibility_tiering.md`` for its blind spots.

    Three criteria carry a ``*_basis`` string saying *why* they scored what they
    did, so a suggestion can be audited without re-deriving it. Added with the
    four fixes in ``docs/migration_score_reproducibility_plan.md``.
    """
    bet, bet_basis = _score_bet(row)
    method = (
        2
        if row.get("measurement_method")
        in {"volumetric_sieverts", "gravimetric_microbalance", "TPD", "electrochemical"}
        else 0
    )
    temp_pressure = (
        1
        if _present(row.get("temperature_k")) and _present(row.get("pressure_bar"))
        else 0
    )
    uptake_type = 1 if row.get("uptake_type") in {"excess", "absolute", "total"} else 0
    purity, purity_basis = _score_purity(row)
    calibration = 0  # no schema field; the human assesses this
    chahine, chahine_basis = _score_chahine(row)
    w = _derive_wt_pct(row)

    total = (
        bet + method + temp_pressure + uptake_type + purity + calibration + chahine
    )
    suggested_tier = (
        "A" if total >= 9 else "B" if total >= 6 else "C" if total >= 3 else "D"
    )
    return {
        "bet": bet,
        "bet_basis": bet_basis,
        "method": method,
        "temp_pressure": temp_pressure,
        "uptake_type": uptake_type,
        "purity": purity,
        "purity_basis": purity_basis,
        "calibration": calibration,
        "chahine": chahine,
        "chahine_basis": chahine_basis,
        "derived_wt_pct": w,
        "total": total,
        "suggested_tier": suggested_tier,
    }


def suggest_tier(row: dict) -> str:
    """Return a SUGGESTED reproducibility tier; the extractor makes the final call.

    This is only a suggestion and cannot see everything the rubric requires. Its
    remaining blind spots, after the four fixes in
    ``docs/migration_score_reproducibility_plan.md``:

    1. It confirms a measurement method is recorded but cannot judge whether the
       paper *clearly described* the instrument and protocol. Both of the tiering
       document's worked examples 2 and 3 score this 1 by hand where the code
       scores 2; downgrade for a named-only method.
    2. "Calibration or blank correction" has no schema field, so it is always 0.
       **The code ceiling is therefore 9, not 10**, and no row with an
       ``unspecified`` uptake type can be suggested Tier A.
    3. The Chahine check cannot apply the categorical physics override, and its
       77 K bound ignores pressure -- BET/500 is the rule's form at moderate
       pressure, so a 1 bar row clears it trivially.
    4. **A characterization-only row is scored as though it were a failed uptake
       measurement.** The rubric grades the reporting quality of an uptake
       measurement and these rows have none, so they collect points only for
       characterization and land at Tier C or D however well reported they are.
       HYC-0007's four such rows suggest D against an assigned B. They inherit
       their paper's tier instead; see §6.9 and §13.4.
    5. A surface area whose method the paper never stated is still accepted as a
       Chahine bound, though §10.3 permits uptake-per-m² only for BET areas.

    When this suggestion and your rubric judgment disagree, your judgment governs.
    """
    return score_reproducibility(row)["suggested_tier"]
