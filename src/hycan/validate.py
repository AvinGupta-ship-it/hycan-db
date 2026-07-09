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
- ``print_report`` renders the fixed report shape consumed by ``scripts/validate_data.py``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import pandas as pd
from pydantic import ValidationError

from hycan.normalize import mmol_per_g_to_wt_pct
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

    micropore = _to_float(clean.get("micropore_volume_cm3_g"))
    total_pore = _to_float(clean.get("total_pore_volume_cm3_g"))
    if micropore is not None and total_pore is not None and micropore > total_pore:
        _append_unique(warnings, "Micropore volume exceeds total pore volume")

    material_class = clean.get("material_class")
    description = clean.get("material_description")
    if (
        material_class == "SWCNT"
        and isinstance(description, str)
        and "single-walled" not in description.lower()
    ):
        _append_unique(warnings, "SWCNT description missing 'single-walled'")

    mmol = _to_float(clean.get("uptake_mmol_g"))
    if wt is not None and mmol is not None:
        try:
            converted = mmol_per_g_to_wt_pct(mmol)
        except ValueError:
            converted = None
        if converted is not None:
            denom = max(abs(wt), 1e-9)
            if abs(converted - wt) / denom > 0.05:
                _append_unique(warnings, "mmol/g and wt% inconsistent")

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
        return (float(row["uptake_ml_stp_g"]) / 22.414) * 0.201588  # project STP convention: 22.414 mL/mmol
    else:
        return None


def score_reproducibility(row: dict) -> dict:
    """Apply the 10-point reproducibility rubric to a row's present fields.

    Returns per-criterion points plus the derived wt%, the total, and the
    suggested tier. This is an approximate scorer; see :func:`suggest_tier`
    and ``docs/reproducibility_tiering.md`` for its blind spots.
    """
    bet = (
        2
        if _present(row.get("bet_surface_area_m2_g"))
        and float(row["bet_surface_area_m2_g"]) > 0
        else 0
    )
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
    purity = 1 if _present(row.get("purification_method")) else 0
    calibration = 0  # no schema field; the human assesses this

    t = row.get("temperature_k")
    w = _derive_wt_pct(row)
    bet_area = row.get("bet_surface_area_m2_g")
    if not _present(t) or w is None:
        chahine = 1  # cannot assess
    elif float(t) >= 273:
        # room-temperature physisorption bound ~1 wt%
        chahine = 2 if w <= 1.0 else (1 if w <= 2.0 else 0)
    elif float(t) <= 100:
        if _present(bet_area) and float(bet_area) > 0:
            expected = float(bet_area) / 500.0
            chahine = 0 if w > 1.5 * expected else (1 if w > expected else 2)
        else:
            chahine = 1  # cryogenic but no surface area to bound against
    else:
        chahine = 0 if w > 6.0 else 2

    total = (
        bet + method + temp_pressure + uptake_type + purity + calibration + chahine
    )
    suggested_tier = (
        "A" if total >= 9 else "B" if total >= 6 else "C" if total >= 3 else "D"
    )
    return {
        "bet": bet,
        "method": method,
        "temp_pressure": temp_pressure,
        "uptake_type": uptake_type,
        "purity": purity,
        "calibration": calibration,
        "chahine": chahine,
        "derived_wt_pct": w,
        "total": total,
        "suggested_tier": suggested_tier,
    }


def suggest_tier(row: dict) -> str:
    """Return a SUGGESTED reproducibility tier; the human extractor makes the final call.

    This is only a suggestion and cannot see everything the rubric requires. Its
    four blind spots: (1) it confirms a measurement method is recorded but cannot
    judge whether the paper *clearly described* the instrument and protocol
    (downgrade for a named-only method); (2) "calibration or blank correction" has
    no schema field, so it is always scored 0; (3) "sample purity" is proxied
    weakly by the presence of a purification method; and (4) the Chahine check is a
    coarse heuristic that cannot apply the categorical physics override. When this
    suggestion and your rubric judgment disagree, your judgment governs.
    """
    return score_reproducibility(row)["suggested_tier"]
