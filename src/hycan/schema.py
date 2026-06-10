"""
Pydantic v2 model for a single HyCAN-DB measurement row.

Quick Pydantic v2 syntax notes used below:
- `Field(ge=x, le=y)` – enforces x ≤ value ≤ y (ge = greater-or-equal, le = less-or-equal).
- `Literal["a", "b"]` – only those exact strings are accepted; anything else raises a
  ValidationError. Equivalent to an enum but stays as a plain string at runtime.
- `model_validator(mode="after")` – runs after all individual fields are validated;
  receives the already-constructed model instance so you can check inter-field logic.
- `Optional[X]` is shorthand for `Union[X, None]`; `= None` provides the default.
- `validate_row()` wraps the model in a try/except so callers get (bool, [errors])
  instead of an exception.
"""

from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------------------------
# Controlled vocabularies as type aliases
# ---------------------------------------------------------------------------

MaterialClass = Literal[
    "SWCNT",
    "MWCNT",
    "DWCNT",
    "graphene",
    "graphene_oxide",
    "reduced_graphene_oxide",
    "activated_carbon",
    "carbon_nanofiber",
    "carbide_derived_carbon",
    "templated_carbon",
    "carbon_aerogel",
    "doped_carbon",
    "composite",
    "other",
]

SynthesisMethod = Literal[
    "arc_discharge",
    "laser_ablation",
    "cvd",
    "hipco",
    "comocat",
    "chemical_oxidation",
    "chemical_reduction",
    "thermal_reduction",
    "pyrolysis",
    "template_synthesis",
    "carbonization",
    "commercial",
    "unknown",
    "other",
]

UptakeType = Literal["excess", "absolute", "total", "unspecified"]

MeasurementMethod = Literal[
    "volumetric_sieverts",
    "gravimetric_microbalance",
    "TPD",
    "electrochemical",
    "other",
    "unknown",
]

ExtractionMethod = Literal[
    "table_direct",
    "text_direct",
    "figure_digitized",
    "figure_estimated",
]

ReproducibilityTier = Literal["A", "B", "C", "D"]


# ---------------------------------------------------------------------------
# Main model
# ---------------------------------------------------------------------------

class MeasurementEntry(BaseModel):
    """One row in the HyCAN-DB dataset, corresponding to a single (T, P, uptake) point."""

    # --- Paper-level ---
    paper_id: str
    doi: str
    first_author: str
    year: int = Field(ge=1990)
    journal: str
    title: str

    # --- Sample-level ---
    sample_id: str
    material_class: MaterialClass
    material_description: str
    synthesis_method: SynthesisMethod = "unknown"
    purification_method: Optional[str] = None
    activation_method: Optional[str] = None
    dopant_element: Optional[str] = None
    dopant_concentration_at_pct: Optional[float] = None
    functional_groups: Optional[str] = None

    # --- Structural characterisation ---
    bet_surface_area_m2_g: Optional[float] = Field(default=None, ge=0, le=4000)
    langmuir_surface_area_m2_g: Optional[float] = Field(default=None, ge=0)
    micropore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    total_pore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=3)
    average_pore_diameter_nm: Optional[float] = Field(default=None, ge=0)

    # --- Measurement ---
    temperature_k: float = Field(ge=50, le=500)
    pressure_bar: float = Field(ge=0, le=200)
    uptake_wt_pct: Optional[float] = Field(default=None, ge=0, le=20)
    uptake_mmol_g: Optional[float] = Field(default=None, ge=0)
    uptake_type: UptakeType
    measurement_method: MeasurementMethod
    uncertainty_wt_pct: Optional[float] = Field(default=None, ge=0)

    # --- Provenance ---
    source_location: str
    extraction_method: ExtractionMethod
    extraction_confidence: int = Field(ge=1, le=5)
    reproducibility_tier: ReproducibilityTier
    notes: Optional[str] = None
    extractor: str
    extraction_date: date
    verified_by: Optional[str] = None
    verification_date: Optional[date] = None

    # --- Cross-field validation ---
    @model_validator(mode="after")
    def at_least_one_uptake(self) -> "MeasurementEntry":
        """Require at least one of the two uptake fields to be non-null."""
        if self.uptake_wt_pct is None and self.uptake_mmol_g is None:
            raise ValueError(
                "At least one of 'uptake_wt_pct' or 'uptake_mmol_g' must be provided."
            )
        return self


# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------

def validate_row(row: dict) -> tuple[bool, list[str]]:
    """
    Validate a raw dict against MeasurementEntry.

    Returns
    -------
    (True, [])              – row is valid.
    (False, [error, ...])   – row is invalid; list contains human-readable messages.
    """
    try:
        MeasurementEntry.model_validate(row)
        return True, []
    except Exception as exc:
        # Pydantic v2 ValidationError exposes .errors() as a list of dicts.
        if hasattr(exc, "errors"):
            messages = [
                f"{' -> '.join(str(loc) for loc in e['loc'])}: {e['msg']}"
                for e in exc.errors()
            ]
        else:
            messages = [str(exc)]
        return False, messages
