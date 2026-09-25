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
    "carbide_chlorination",
    "physical_activation",
    "chemical_activation",
    "chemical_exfoliation",
    "commercial",
    "unknown",
    "other",
]

SurfaceAreaMethod = Literal[
    "BET",
    "Langmuir",
    "geometric",
    "DFT",
    "unspecified",
    "none",
]

UptakeType = Literal["excess", "absolute", "total", "unspecified"]

MeasurementMethod = Literal[
    "volumetric_sieverts",
    "gravimetric_microbalance",
    "TPD",
    "electrochemical",
    "other",
    "unknown",
    # v1.2: for a characterization-only row, which records no measurement at
    # all. Such rows previously had to claim "unknown", which asserts that a
    # measurement happened by a method nobody identified.
    "not_applicable",
]

# --- v1.2 additions ---

# Gap 1. A paper that reports "below 0.2 wt.%" has no exact value. Writing the
# number bare would turn a bound into a measurement that enters isotherm fits
# and Chahine comparisons as a point; writing nothing loses a real result, and
# bounded and null results are the corrective to this literature's optimistic
# publication bias. Anything other than "exact" must be excluded from isotherm
# fitting and from headline capacity statistics.
UptakeBound = Literal["exact", "upper", "lower", "approximate"]

# Gap 9. HYC-0029 measures a weight difference across a 303 -> 673 -> 303 K
# cycle at constant pressure in flowing hydrogen. Its uptake is referenced to
# the desorbed state at 673 K, not to vacuum or zero coverage, so it is not
# commensurable with an isothermal uptake and must not enter a Chahine plot.
# Recording a single temperature_k for such a row asserts an isothermal
# measurement that did not happen.
MeasurementMode = Literal["isothermal", "temperature_cycle", "TPD", "flow"]

# Gap 8. Composition is reported by different techniques that do not agree:
# HYC-0026's explicit finding is that its bulk (elemental analysis) and surface
# (XPS) nitrogen contents differ systematically.
CompositionMethod = Literal["elemental_analysis", "XPS", "AAS", "ICP", "other"]

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
    measurement_id: str
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
    surface_area_method: SurfaceAreaMethod = "unspecified"
    micropore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    ultramicropore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    total_pore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=3)
    average_pore_diameter_nm: Optional[float] = Field(default=None, ge=0)

    # --- Measurement ---
    temperature_k: Optional[float] = Field(default=None, ge=50, le=500)
    pressure_bar: Optional[float] = Field(default=None, ge=0, le=200)
    uptake_wt_pct: Optional[float] = Field(default=None, ge=0, le=20)
    uptake_mmol_g: Optional[float] = Field(default=None, ge=0)
    uptake_ml_stp_g: Optional[float] = Field(default=None, ge=0, le=2225)
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

    # --- v1.2: qualifiers on what the uptake and its conditions mean ---
    # Physical CSV positions 41-51. All defaulted so that every pre-v1.2 row is
    # valid unchanged: an existing row does assert an exact, isothermal
    # measurement with both conditions stated, which is what the defaults say.
    uptake_bound: UptakeBound = "exact"
    temperature_unstated: bool = False
    pressure_unstated: bool = False
    measurement_mode: MeasurementMode = "isothermal"
    # Not bounded by temperature_k's 50-500 K window: this is a desorption
    # endpoint, not a measurement temperature.
    reference_temperature_k: Optional[float] = Field(default=None, ge=50, le=1500)

    # --- v1.2: supported metal, kept distinct from a lattice dopant ---
    # An impregnated catalyst particle (HYC-0029's Co, HYC-0027's Pd) and a
    # substitutional heteroatom (HYC-0025's B, HYC-0026's N) work by different
    # mechanisms. Collapsing them into dopant_element would make the spillover
    # subset uninterpretable. residual_* is synthesis-catalyst contamination,
    # which decides whether an uptake is the carbon's at all.
    metal_element: Optional[str] = None
    metal_loading_wt_pct: Optional[float] = Field(default=None, ge=0, le=100)
    residual_metal_element: Optional[str] = None
    residual_metal_wt_pct: Optional[float] = Field(default=None, ge=0, le=100)

    # --- v1.2: dopant concentration by weight, with its technique ---
    # dopant_concentration_at_pct is atomic percent; papers reporting weight
    # percent had nowhere to put it, which blocked HYC-0026 entirely.
    dopant_concentration_wt_pct: Optional[float] = Field(
        default=None, ge=0, le=100
    )
    dopant_concentration_method: Optional[CompositionMethod] = None

    # --- Cross-field validation ---
    _UPTAKE_FIELDS = ("uptake_wt_pct", "uptake_mmol_g", "uptake_ml_stp_g")
    _CHARACTERIZATION_FIELDS = (
        "bet_surface_area_m2_g",
        "langmuir_surface_area_m2_g",
        "micropore_volume_cm3_g",
        "ultramicropore_volume_cm3_g",
        "total_pore_volume_cm3_g",
        "average_pore_diameter_nm",
    )

    def _reports_uptake(self) -> bool:
        return any(getattr(self, f) is not None for f in self._UPTAKE_FIELDS)

    def _reports_characterization(self) -> bool:
        return any(getattr(self, f) is not None for f in self._CHARACTERIZATION_FIELDS)

    @model_validator(mode="after")
    def conditions_required_with_uptake(self) -> "MeasurementEntry":
        """Temperature and pressure are required exactly when uptake is reported.

        Schema v1.1 (§8.5 gap 3). An uptake value without its conditions is
        uninterpretable: carbon physisorption at 77 K is roughly an order of
        magnitude above the same material at 298 K. A sample whose BET and pore
        data are published but whose uptake was never measured is a legitimate
        row, and under v1.0 it could not be recorded at all — two such rows were
        dropped from HYC-0018.

        Schema v1.2 (gap 2) adds the only exception: a paper may report an
        uptake without ever stating a condition numerically. HYC-0011 and
        HYC-0015 give uptakes at "room temperature" and no number; HYC-0009's
        TPD rows state no pressure. Imputing 298 K is not available -- "room
        temperature" in a 2002 and a 2016 laboratory are not the same number,
        the difference matters at these uptake levels, and substituting a
        convention fabricates a measurement condition. So the field may be null
        when the matching `*_unstated` flag says the paper is silent, and only
        then. A flag set while its field is populated is a contradiction and an
        error in its own right: a row cannot both state a condition and declare
        it unstated.
        """
        for field, flag in (
            ("temperature_k", "temperature_unstated"),
            ("pressure_bar", "pressure_unstated"),
        ):
            if getattr(self, flag) and getattr(self, field) is not None:
                raise ValueError(
                    f"{flag} is set but {field} is populated; a row cannot both "
                    f"state a condition and declare it unstated"
                )

        if self._reports_uptake():
            missing = [
                field
                for field, flag in (
                    ("temperature_k", "temperature_unstated"),
                    ("pressure_bar", "pressure_unstated"),
                )
                if getattr(self, field) is None and not getattr(self, flag)
            ]
            if missing:
                raise ValueError(
                    "Rows reporting uptake must state their conditions, or set "
                    "the matching *_unstated flag; missing: " + ", ".join(missing)
                )
        return self

    @model_validator(mode="after")
    def at_least_one_uptake(self) -> "MeasurementEntry":
        """A row must report either an uptake measurement or characterization.

        When uptake is reported, at least one of the two gravimetric fields must
        carry it, so that a volumetric-only row cannot enter without a value the
        analysis can use directly (§8.2, preserved from v1.0).
        """
        if self._reports_uptake():
            if self.uptake_wt_pct is None and self.uptake_mmol_g is None:
                raise ValueError(
                    "At least one of 'uptake_wt_pct' or 'uptake_mmol_g' "
                    "must be provided."
                )
        elif not self._reports_characterization():
            raise ValueError(
                "A row must report at least one uptake value or at least one "
                "characterization value; this row reports neither."
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
