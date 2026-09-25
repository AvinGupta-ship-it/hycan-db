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
    # v1.3 gap 3. alpha_s_plot is HYC-0007's method; t_plot is HYC-0004's, whose
    # area is already in the corpus under `unspecified`.
    "alpha_s_plot",
    "t_plot",
    # v1.3 gap 3. The three no-method values mean three different things and the
    # distinction is checked, not merely documented:
    #   unspecified   - an area IS reported, with no stated method.
    #   none          - the paper reports no surface area for ANY sample.
    #   not_reported  - this sample has none, in a paper that reports areas for
    #                   its other samples (HYC-0029's 12 Co-loaded samples,
    #                   HYC-0016's S13, HYC-0022's G212).
    # Before v1.3 all three collapsed onto `unspecified`, which is why a reader
    # could not tell "measured, method unknown" from "never measured".
    "not_reported",
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

# --- v1.3 gap 6: how a pore quantity was determined -------------------------
# The same field name has been carrying incompatible quantities. micropore_volume
# is Dubinin-Radushkevich on CO2 at 273 K in HYC-0019 and HYC-0024, DR on N2 at
# 77 K in HYC-0024's other column, plain DR in HYC-0022 and HYC-0026, a DFT
# volume in HYC-0021 and an alpha-s-plot volume in HYC-0007. Without the method
# and the probe gas those are not comparable numbers.
PoreVolumeMethod = Literal[
    "DR",
    "DFT",
    "NLDFT",
    "QSDFT",
    "BJH",
    "HK",
    "t_plot",
    "alpha_s_plot",
    "other",
    "unspecified",
]

# HYC-0019 measures surface area by N2 at 77 K and micropore volume by CO2 at
# 273 K on the same row, which is why its area falls while its micropore volume
# rises. That was unrecordable before v1.3.
PoreVolumeProbeGas = Literal["N2", "CO2", "Ar", "He", "other", "unspecified"]

# average_pore_diameter_nm would otherwise mix a BJH desorption average (which
# HYC-0022's paper itself calls a *mesopore* size), a DR characteristic-energy
# slit width (HYC-0024), an HK median and Stoeckli's L0 (HYC-0026).
# geometric_from_S_V is HYC-0007's Wave, back-calculated from S_micro and
# V_micro under an assumed pore shape -- not a pore-size-distribution model at
# all, so calling it BJH or DFT would misdescribe it.
PoreDiameterMethod = Literal[
    "BJH",
    "DR_characteristic_energy",
    "HK",
    "stoeckli_L0",
    "DFT",
    "geometric_from_S_V",
    "other",
    "unspecified",
]

# --- v1.3 gap 10: what a volumetric capacity is per ------------------------
# HYC-0024 reports both per-micropore-volume and per-tank-volume figures for the
# same sample at the same conditions, and they differ by more than 2x. A
# volumetric capacity with no stated basis is not interpretable.
VolumetricCapacityBasis = Literal[
    "micropore_volume",
    "total_pore_volume",
    "packing_volume",
    "tank_volume",
    "other",
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

    # --- v1.3 gap 3: a paper can report more than one surface area ---
    # Physical CSV positions 52-53. HYC-0007 reports, per sample, a micropore
    # surface area (320-2250 m2/g) and an external surface area (20-590 m2/g)
    # from an alpha-s plot, and NO total -- eighteen measured values with nowhere
    # to go, which held all of that paper's rows out of the corpus.
    #
    # bet_surface_area_m2_g is deliberately NOT renamed: renaming breaks
    # plotting.py, every ML feature of that name and every published row
    # reference. Its meaning is unchanged and is what it has been since v1.1 --
    # the paper's headline TOTAL specific surface area, with the method given by
    # surface_area_method.
    #
    # Caveat that travels with external_surface_area_m2_g: HYC-0007 defines its
    # S_ext as "the external surface containing the mesopore and macropore", so
    # this is not a geometric external surface and a mesopore surface area cannot
    # be recovered from it.
    micropore_surface_area_m2_g: Optional[float] = Field(
        default=None, ge=0, le=4000
    )
    external_surface_area_m2_g: Optional[float] = Field(
        default=None, ge=0, le=4000
    )

    # --- v1.3 gap 6: how each pore quantity was determined ---
    # Physical CSV positions 54-59. One method/probe pair per row rather than per
    # field: no corpus paper yet determines two of a single sample's pore volumes
    # by different methods, and nine more columns to record an unobserved
    # distinction is the wrong trade. Where a row's volumes do differ in method,
    # `notes` records it and these fields carry the primary.
    pore_volume_method: PoreVolumeMethod = "unspecified"
    pore_volume_probe_gas: PoreVolumeProbeGas = "unspecified"
    # HYC-0024 reports TWO DR micropore volumes per sample -- N2 at 77 K and CO2
    # at 273 K -- which are not interchangeable (0.78 vs 0.57 cm3/g on ACFC50).
    # The CO2-DR volume gets its own field, named by probe gas, because calling
    # it "ultramicropore" would assert a cutoff that paper explicitly never
    # states.
    micropore_volume_co2_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    mesopore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=3)
    # The cutoff is now stated per row instead of assumed from the data
    # dictionary. HYC-0005 and HYC-0021 are cut at 0.7 nm, HYC-0022's V<1nm at
    # 1 nm, HYC-0024's DR-CO2 at no stated cutoff at all. Mixing them would
    # destroy the one comparison v1.1 gap 4 added the field to make possible, so
    # a populated volume with a null cutoff is an error (see below).
    ultramicropore_cutoff_nm: Optional[float] = Field(default=None, ge=0, le=2)
    pore_diameter_method: PoreDiameterMethod = "unspecified"

    # --- v1.3 gap 10: volumetric, areal and structural quantities ---
    # Physical CSV positions 60-66. Two volumetric fields rather than one with a
    # basis flag, because HYC-0024 reports BOTH for the same sample at the same
    # conditions: an adsorbed-phase density per micropore volume excluding
    # compressed gas, and Ms per tank volume including it. One field could hold
    # only one of them, and choosing would discard a primary-table measurement.
    volumetric_capacity_kg_m3: Optional[float] = Field(default=None, ge=0, le=200)
    volumetric_capacity_basis: Optional[VolumetricCapacityBasis] = None
    volumetric_capacity_includes_compressed_gas: bool = False
    adsorbed_phase_density_kg_m3: Optional[float] = Field(
        default=None, ge=0, le=200
    )
    packing_density_g_cm3: Optional[float] = Field(default=None, ge=0, le=5)
    # HYC-0024's helium density is load-bearing, not decorative: it is the
    # quantity the paper uses to subtract the compressed-gas contribution from
    # the measured weight increase, so without it the excess/absolute basis of
    # its numbers cannot be reconstructed downstream.
    skeletal_density_g_cm3: Optional[float] = Field(default=None, ge=0, le=5)
    # HYC-0011's areal uptake (6.3e-6 g/cm2) is what makes its 8.0 wt% headline
    # checkable -- and irreconcilable with its own film mass and area.
    areal_uptake_g_cm2: Optional[float] = Field(default=None, ge=0)

    # Physical CSV position 67. HYC-0015's held row.
    interlayer_spacing_nm: Optional[float] = Field(default=None, ge=0)

    # --- Cross-field validation ---
    # Split in two at v1.3. The first three convert to a gravimetric figure
    # through `normalize`; the last three do not without a density the paper may
    # not state. See `at_least_one_uptake`.
    _GRAVIMETRIC_UPTAKE_FIELDS = (
        "uptake_wt_pct",
        "uptake_mmol_g",
        "uptake_ml_stp_g",
    )
    _NON_CONVERTIBLE_UPTAKE_FIELDS = (
        "volumetric_capacity_kg_m3",
        "adsorbed_phase_density_kg_m3",
        "areal_uptake_g_cm2",
    )
    _SURFACE_AREA_FIELDS = (
        "bet_surface_area_m2_g",
        "langmuir_surface_area_m2_g",
        "micropore_surface_area_m2_g",
        "external_surface_area_m2_g",
    )
    _UPTAKE_FIELDS = (
        "uptake_wt_pct",
        "uptake_mmol_g",
        "uptake_ml_stp_g",
        "volumetric_capacity_kg_m3",
        "adsorbed_phase_density_kg_m3",
        "areal_uptake_g_cm2",
    )
    _CHARACTERIZATION_FIELDS = (
        "bet_surface_area_m2_g",
        "langmuir_surface_area_m2_g",
        "micropore_surface_area_m2_g",
        "external_surface_area_m2_g",
        "micropore_volume_cm3_g",
        "micropore_volume_co2_cm3_g",
        "ultramicropore_volume_cm3_g",
        "mesopore_volume_cm3_g",
        "total_pore_volume_cm3_g",
        "average_pore_diameter_nm",
        "packing_density_g_cm3",
        "skeletal_density_g_cm3",
        "interlayer_spacing_nm",
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

        v1.0-v1.2 required that when uptake is reported, at least one of the two
        gravimetric fields carry it, "so that a volumetric-only row cannot enter
        without a value the analysis can use directly."

        **v1.3 narrows that rule rather than dropping it.** It was written when
        the schema's only volumetric-looking field was `uptake_ml_stp_g` -- gas
        volume per gram, which *is* convertible to wt% through
        `normalize.ml_stp_per_g_to_wt_pct`. So "volumetric-only" then meant "a row
        declining an arithmetic conversion it could have done", and refusing it
        was right.

        `volumetric_capacity_kg_m3` is a different kind of quantity: H2 mass per
        unit volume of tank or of pore, convertible to a gravimetric figure only
        with a density the paper may not state. HYC-0024's only tabulated hydrogen
        quantities are of exactly this kind, and computing a wt% from them would
        require choosing between two micropore volumes the paper never
        distinguishes -- this project's arithmetic presented as the paper's
        measurement, which §3.4 and §3.9 both forbid.

        So: a row carrying a gravimetric-convertible value must still carry wt% or
        mmol/g. A row whose only uptake is non-convertible is admitted, and it
        still counts as reporting uptake, so its conditions are required and it is
        not misfiled as characterization-only. `tests/test_dataset_invariants.py`
        enumerates such rows by measurement_id so they cannot appear unnoticed --
        a null wt% is dropped silently by a pandas mean, which is the §12.3
        failure mode.
        """
        reports_gravimetric = any(
            getattr(self, f) is not None for f in self._GRAVIMETRIC_UPTAKE_FIELDS
        )
        if reports_gravimetric:
            if self.uptake_wt_pct is None and self.uptake_mmol_g is None:
                raise ValueError(
                    "At least one of 'uptake_wt_pct' or 'uptake_mmol_g' "
                    "must be provided."
                )
        elif not self._reports_uptake() and not self._reports_characterization():
            raise ValueError(
                "A row must report at least one uptake value or at least one "
                "characterization value; this row reports neither."
            )
        return self

    @model_validator(mode="after")
    def pore_and_area_qualifiers_are_present_when_needed(self) -> "MeasurementEntry":
        """Schema v1.3 (gaps 3, 6, 10). Four rules, each with a reason.

        1. An ultramicropore volume needs its cutoff. The field exists to make one
           quantity comparable across the corpus (v1.1 gap 4, added for HYC-0021's
           central finding). A value whose cutoff nobody stated is not comparable
           to one cut at 0.7 nm, and mixing them destroys exactly what the field
           was for -- which is why HYC-0022's 1 nm value and HYC-0024's
           no-cutoff value were held out rather than entered.

        2. A volumetric capacity needs its basis. Per micropore volume and per
           tank volume differ by more than a factor of two in HYC-0024's own
           table, so an unqualified number is not interpretable.

        3. `none` and `not_reported` must not carry an area. Both mean the sample
           has no reported surface area; a value alongside either is a
           contradiction.

        The matching rule -- that `unspecified` must CARRY an area, and that
        `not_reported` is used only where the paper reports areas for its other
        samples -- is deliberately **not** here. It cannot be evaluated from one
        row: "a paper that reports areas for its others" is a fact about the
        paper's other rows. It lives in `validate.py` as a dataset-level check,
        which can also verify the stronger property a row-local check cannot.
        """
        if (
            self.ultramicropore_volume_cm3_g is not None
            and self.ultramicropore_cutoff_nm is None
        ):
            raise ValueError(
                "ultramicropore_volume_cm3_g is populated but "
                "ultramicropore_cutoff_nm is null; an ultramicropore volume "
                "whose cutoff is unstated is not comparable with one cut at "
                "0.7 nm, and the field exists to be comparable"
            )

        if (
            self.volumetric_capacity_kg_m3 is not None
            and self.volumetric_capacity_basis is None
        ):
            raise ValueError(
                "volumetric_capacity_kg_m3 is populated but "
                "volumetric_capacity_basis is null; per pore volume and per tank "
                "volume are not the same quantity"
            )

        areas_present = [
            f for f in self._SURFACE_AREA_FIELDS if getattr(self, f) is not None
        ]
        if self.surface_area_method in ("none", "not_reported") and areas_present:
            raise ValueError(
                f"surface_area_method is '{self.surface_area_method}' but these "
                f"surface-area fields are populated: {', '.join(areas_present)}"
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
