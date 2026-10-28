# src/hycan/schema.py at the registration commit, with comments and
# docstrings removed (protocol §15, Amendment 1).
from __future__ import annotations
from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator
MaterialClass = Literal['SWCNT', 'MWCNT', 'DWCNT', 'graphene', 'graphene_oxide', 'reduced_graphene_oxide', 'activated_carbon', 'carbon_nanofiber', 'carbide_derived_carbon', 'templated_carbon', 'carbon_aerogel', 'doped_carbon', 'composite', 'other']
SynthesisMethod = Literal['arc_discharge', 'laser_ablation', 'cvd', 'hipco', 'comocat', 'chemical_oxidation', 'chemical_reduction', 'thermal_reduction', 'pyrolysis', 'template_synthesis', 'carbonization', 'carbide_chlorination', 'physical_activation', 'chemical_activation', 'chemical_exfoliation', 'commercial', 'unknown', 'other']
SurfaceAreaMethod = Literal['BET', 'Langmuir', 'geometric', 'DFT', 'alpha_s_plot', 't_plot', 'not_reported', 'unspecified', 'none']
UptakeType = Literal['excess', 'absolute', 'total', 'unspecified']
MeasurementMethod = Literal['volumetric_sieverts', 'gravimetric_microbalance', 'TPD', 'electrochemical', 'other', 'unknown', 'not_applicable']
UptakeBound = Literal['exact', 'upper', 'lower', 'approximate']
MeasurementMode = Literal['isothermal', 'temperature_cycle', 'TPD', 'flow']
CompositionMethod = Literal['elemental_analysis', 'XPS', 'AAS', 'ICP', 'other']
PoreVolumeMethod = Literal['DR', 'DFT', 'NLDFT', 'QSDFT', 'BJH', 'HK', 't_plot', 'alpha_s_plot', 'other', 'unspecified']
PoreVolumeProbeGas = Literal['N2', 'CO2', 'Ar', 'He', 'other', 'unspecified']
PoreDiameterMethod = Literal['BJH', 'DR_characteristic_energy', 'HK', 'stoeckli_L0', 'DFT', 'geometric_from_S_V', 'other', 'unspecified']
VolumetricCapacityBasis = Literal['micropore_volume', 'total_pore_volume', 'packing_volume', 'tank_volume', 'other']
ExtractionMethod = Literal['table_direct', 'text_direct', 'figure_digitized', 'figure_estimated']
ReproducibilityTier = Literal['A', 'B', 'C', 'D']
BasisInferred = Literal['excess', 'absolute', 'total', 'unknown']
WtPctConvention = Literal['W1', 'W2', 'unknown']
WtPctConventionSource = Literal['stated', 'inferred_from_paired_units', 'computed_from_other_unit', 'none']
ValueKind = Literal['measured', 'fitted_interpolated', 'fitted_extrapolated', 'unclear']
IsothermBranch = Literal['adsorption', 'desorption', 'not_applicable']
SurfaceAreaProbeGas = Literal['N2', 'Ar', 'CO2', 'other', 'unspecified']
AreaSameSample = Literal['yes', 'parent_material', 'other_paper', 'unclear']
DataLocation = Literal['main_text', 'SI']
SelectionRoute = Literal['S1', 'S2', 'legacy_v0.1', 'legacy_v0.1_ineligible']
_V2_CODED_ALWAYS = ('basis_inferred', 'wt_pct_convention', 'wt_pct_convention_source', 'value_kind', 'isotherm_branch', 'temperature_inferred', 'data_location', 'instrument_identified', 'calibration_described', 'replicates_reported', 'measuring_lab_id')
_V2_CODED_WITH_AREA = ('surface_area_probe_gas', 'area_same_sample')
_V2_CODED_WITH_BET = ('bet_range_stated', 'bet_consistency_criteria_stated')

class MeasurementEntry(BaseModel):
    paper_id: str
    doi: str
    first_author: str
    year: int = Field(ge=1990)
    journal: str
    title: str
    sample_id: str
    measurement_id: str
    material_class: MaterialClass
    material_description: str
    synthesis_method: SynthesisMethod = 'unknown'
    purification_method: Optional[str] = None
    activation_method: Optional[str] = None
    dopant_element: Optional[str] = None
    dopant_concentration_at_pct: Optional[float] = None
    functional_groups: Optional[str] = None
    bet_surface_area_m2_g: Optional[float] = Field(default=None, ge=0, le=5000)
    langmuir_surface_area_m2_g: Optional[float] = Field(default=None, ge=0)
    surface_area_method: SurfaceAreaMethod = 'unspecified'
    micropore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    ultramicropore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    total_pore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=3)
    average_pore_diameter_nm: Optional[float] = Field(default=None, ge=0)
    temperature_k: Optional[float] = Field(default=None, ge=50, le=500)
    pressure_bar: Optional[float] = Field(default=None, ge=0, le=200)
    uptake_wt_pct: Optional[float] = Field(default=None, ge=0, le=20)
    uptake_mmol_g: Optional[float] = Field(default=None, ge=0)
    uptake_ml_stp_g: Optional[float] = Field(default=None, ge=0, le=2225)
    uptake_type: UptakeType
    measurement_method: MeasurementMethod
    uncertainty_wt_pct: Optional[float] = Field(default=None, ge=0)
    source_location: str
    extraction_method: ExtractionMethod
    extraction_confidence: int = Field(ge=1, le=5)
    reproducibility_tier: Optional[ReproducibilityTier] = None
    notes: Optional[str] = None
    extractor: str
    extraction_date: date
    verified_by: Optional[str] = None
    verification_date: Optional[date] = None
    uptake_bound: UptakeBound = 'exact'
    temperature_unstated: bool = False
    pressure_unstated: bool = False
    measurement_mode: MeasurementMode = 'isothermal'
    reference_temperature_k: Optional[float] = Field(default=None, ge=50, le=1500)
    metal_element: Optional[str] = None
    metal_loading_wt_pct: Optional[float] = Field(default=None, ge=0, le=100)
    residual_metal_element: Optional[str] = None
    residual_metal_wt_pct: Optional[float] = Field(default=None, ge=0, le=100)
    dopant_concentration_wt_pct: Optional[float] = Field(default=None, ge=0, le=100)
    dopant_concentration_method: Optional[CompositionMethod] = None
    micropore_surface_area_m2_g: Optional[float] = Field(default=None, ge=0, le=4000)
    external_surface_area_m2_g: Optional[float] = Field(default=None, ge=0, le=4000)
    pore_volume_method: PoreVolumeMethod = 'unspecified'
    pore_volume_probe_gas: PoreVolumeProbeGas = 'unspecified'
    micropore_volume_co2_cm3_g: Optional[float] = Field(default=None, ge=0, le=2)
    mesopore_volume_cm3_g: Optional[float] = Field(default=None, ge=0, le=3)
    ultramicropore_cutoff_nm: Optional[float] = Field(default=None, ge=0, le=2)
    pore_diameter_method: PoreDiameterMethod = 'unspecified'
    volumetric_capacity_kg_m3: Optional[float] = Field(default=None, ge=0, le=200)
    volumetric_capacity_basis: Optional[VolumetricCapacityBasis] = None
    volumetric_capacity_includes_compressed_gas: bool = False
    adsorbed_phase_density_kg_m3: Optional[float] = Field(default=None, ge=0, le=200)
    packing_density_g_cm3: Optional[float] = Field(default=None, ge=0, le=5)
    skeletal_density_g_cm3: Optional[float] = Field(default=None, ge=0, le=5)
    areal_uptake_g_cm2: Optional[float] = Field(default=None, ge=0)
    interlayer_spacing_nm: Optional[float] = Field(default=None, ge=0)
    basis_stated: Optional[bool] = None
    basis_inferred: Optional[BasisInferred] = None
    basis_evidence: Optional[str] = None
    wt_pct_convention: Optional[WtPctConvention] = None
    wt_pct_convention_source: Optional[WtPctConventionSource] = None
    value_kind: Optional[ValueKind] = None
    isotherm_id: Optional[str] = None
    isotherm_branch: Optional[IsothermBranch] = None
    isotherm_point_count: Optional[int] = Field(default=None, ge=1)
    temperature_inferred: Optional[bool] = None
    data_location: Optional[DataLocation] = None
    digitization_uncertainty_wt_pct: Optional[float] = Field(default=None, ge=0)
    surface_area_probe_gas: Optional[SurfaceAreaProbeGas] = None
    bet_range_stated: Optional[bool] = None
    bet_consistency_criteria_stated: Optional[bool] = None
    area_same_sample: Optional[AreaSameSample] = None
    degas_temperature_c: Optional[float] = Field(default=None, ge=-50, le=1500)
    degas_duration_h: Optional[float] = Field(default=None, ge=0)
    degas_end_pressure_pa: Optional[float] = Field(default=None, ge=0)
    sample_mass_mg: Optional[float] = Field(default=None, gt=0)
    h2_purity_pct: Optional[float] = Field(default=None, ge=90, le=100)
    free_volume_calibration: Optional[str] = None
    instrument_identified: Optional[bool] = None
    calibration_described: Optional[bool] = None
    replicates_reported: Optional[bool] = None
    measuring_lab_id: Optional[str] = None
    material_identity: Optional[str] = None
    duplicate_of: Optional[str] = None
    selection_route: Optional[SelectionRoute] = None
    frame_id: Optional[str] = None

    @model_validator(mode='after')
    def schema_v2_consistency(self) -> 'MeasurementEntry':
        if self.basis_stated is True and (not (self.basis_evidence or '').strip()):
            raise ValueError('basis_stated is true but basis_evidence is empty; a stated basis must carry the quote that states it')
        if self.temperature_inferred is True and self.temperature_k != 77.3:
            raise ValueError("temperature_inferred is true, so temperature_k must be 77.3 (the 'liquid nitrogen' convention, protocol §3)")
        if self.digitization_uncertainty_wt_pct is not None and self.extraction_method != 'figure_digitized':
            raise ValueError('digitization_uncertainty_wt_pct is set on a row whose extraction_method is not figure_digitized')
        if self.basis_stated is not None:
            required = list(_V2_CODED_ALWAYS)
            if self.surface_area_method not in ('none', 'not_reported'):
                required += _V2_CODED_WITH_AREA
            if self.surface_area_method == 'BET':
                required += _V2_CODED_WITH_BET
            missing = [f for f in required if getattr(self, f) is None]
            if missing:
                raise ValueError('row is coded under schema v2 (basis_stated is set) but these fields are uncoded: ' + ', '.join(missing))
        convention, source = (self.wt_pct_convention, self.wt_pct_convention_source)
        if (convention is None) != (source is None):
            raise ValueError('wt_pct_convention and its source are coded together')
        if source is not None:
            allowed = {'computed_from_other_unit': ('W1',), 'stated': ('W1', 'W2'), 'inferred_from_paired_units': ('W1', 'W2'), 'none': ('unknown',)}[source]
            if convention not in allowed:
                raise ValueError(f'wt_pct_convention_source {source} requires wt_pct_convention in {allowed}, not {convention}')
        return self
    _GRAVIMETRIC_UPTAKE_FIELDS = ('uptake_wt_pct', 'uptake_mmol_g', 'uptake_ml_stp_g')
    _NON_CONVERTIBLE_UPTAKE_FIELDS = ('volumetric_capacity_kg_m3', 'adsorbed_phase_density_kg_m3', 'areal_uptake_g_cm2')
    _SURFACE_AREA_FIELDS = ('bet_surface_area_m2_g', 'langmuir_surface_area_m2_g', 'micropore_surface_area_m2_g', 'external_surface_area_m2_g')
    _UPTAKE_FIELDS = ('uptake_wt_pct', 'uptake_mmol_g', 'uptake_ml_stp_g', 'volumetric_capacity_kg_m3', 'adsorbed_phase_density_kg_m3', 'areal_uptake_g_cm2')
    _CHARACTERIZATION_FIELDS = ('bet_surface_area_m2_g', 'langmuir_surface_area_m2_g', 'micropore_surface_area_m2_g', 'external_surface_area_m2_g', 'micropore_volume_cm3_g', 'micropore_volume_co2_cm3_g', 'ultramicropore_volume_cm3_g', 'mesopore_volume_cm3_g', 'total_pore_volume_cm3_g', 'average_pore_diameter_nm', 'packing_density_g_cm3', 'skeletal_density_g_cm3', 'interlayer_spacing_nm')

    def _reports_uptake(self) -> bool:
        return any((getattr(self, f) is not None for f in self._UPTAKE_FIELDS))

    def _reports_characterization(self) -> bool:
        return any((getattr(self, f) is not None for f in self._CHARACTERIZATION_FIELDS))

    @model_validator(mode='after')
    def conditions_required_with_uptake(self) -> 'MeasurementEntry':
        for field, flag in (('temperature_k', 'temperature_unstated'), ('pressure_bar', 'pressure_unstated')):
            if getattr(self, flag) and getattr(self, field) is not None:
                raise ValueError(f'{flag} is set but {field} is populated; a row cannot both state a condition and declare it unstated')
        if self._reports_uptake():
            missing = [field for field, flag in (('temperature_k', 'temperature_unstated'), ('pressure_bar', 'pressure_unstated')) if getattr(self, field) is None and (not getattr(self, flag))]
            if missing:
                raise ValueError('Rows reporting uptake must state their conditions, or set the matching *_unstated flag; missing: ' + ', '.join(missing))
        return self

    @model_validator(mode='after')
    def at_least_one_uptake(self) -> 'MeasurementEntry':
        reports_gravimetric = any((getattr(self, f) is not None for f in self._GRAVIMETRIC_UPTAKE_FIELDS))
        if reports_gravimetric:
            if self.uptake_wt_pct is None and self.uptake_mmol_g is None:
                raise ValueError("At least one of 'uptake_wt_pct' or 'uptake_mmol_g' must be provided.")
        elif not self._reports_uptake() and (not self._reports_characterization()):
            raise ValueError('A row must report at least one uptake value or at least one characterization value; this row reports neither.')
        return self

    @model_validator(mode='after')
    def pore_and_area_qualifiers_are_present_when_needed(self) -> 'MeasurementEntry':
        if self.ultramicropore_volume_cm3_g is not None and self.ultramicropore_cutoff_nm is None:
            raise ValueError('ultramicropore_volume_cm3_g is populated but ultramicropore_cutoff_nm is null; an ultramicropore volume whose cutoff is unstated is not comparable with one cut at 0.7 nm, and the field exists to be comparable')
        if self.volumetric_capacity_kg_m3 is not None and self.volumetric_capacity_basis is None:
            raise ValueError('volumetric_capacity_kg_m3 is populated but volumetric_capacity_basis is null; per pore volume and per tank volume are not the same quantity')
        areas_present = [f for f in self._SURFACE_AREA_FIELDS if getattr(self, f) is not None]
        if self.surface_area_method in ('none', 'not_reported') and areas_present:
            raise ValueError(f"surface_area_method is '{self.surface_area_method}' but these surface-area fields are populated: {', '.join(areas_present)}")
        return self

def validate_row(row: dict) -> tuple[bool, list[str]]:
    try:
        MeasurementEntry.model_validate(row)
        return (True, [])
    except Exception as exc:
        if hasattr(exc, 'errors'):
            messages = [f"{' -> '.join((str(loc) for loc in e['loc']))}: {e['msg']}" for e in exc.errors()]
        else:
            messages = [str(exc)]
        return (False, messages)
