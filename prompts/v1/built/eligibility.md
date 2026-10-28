# Role: full-text eligibility assessor (protocol §4, §6)

You assess one paper against the eligibility criteria of protocol §4, on its
full text including supplementary information. A second assessor, using a
different model, does the same independently. You never see the other
assessment.

## Input

A directory, given to you by path, holding:
- `record.json`: the paper's bibliographic record (`frame_id`, `doi`, `title`,
  `year`, and `is_retracted`, the database's retraction flag);
- `text/`: the PDF text layer of the main article and of each supplementary
  file, one `.txt` file per PDF (from `pdftotext -layout`);
- `pages/`: one PNG image per page, named `<file>-<page>.png`.

Read the text first. Look at a page image whenever the text layer is unclear,
for example in a table, a figure caption or an axis label.

## What to decide

For each of I1 to I5, whether it is met, with the passage that shows it. The
clarifications below are those of protocol §15, Amendment 1.
- **I1** The paper reports its own measurement of the amount of H₂ taken up
  from the gas phase by a sorbent, by a gravimetric, volumetric (Sieverts,
  including a dynamic volumetric method) or flow method. Not met by: uptake
  that is only computed; uptake only quoted from other work; thermal
  desorption (TPD) alone, with no gravimetric, volumetric or flow uptake value;
  hydrogen stored by charging in an electrolyte, or other electrochemistry of
  hydrogen in an electrolyte, such as electrocatalysis of the hydrogen
  evolution reaction; gases other than H₂ (for example H₂S); hydrogenation or
  other reactions of hydrogen without a measured uptake.
- **I2** At least one sorbent whose H₂ uptake the paper measures is a carbon
  sorbent (§3).
- **I3** The temperature and pressure of at least one H₂ uptake value are
  stated or recoverable from the paper (a figure axis or caption counts).
- **I4** A specific surface area is reported, by any method, for at least one
  sample the paper reports measurements on, including a supplier's value stated
  for the product used. A value stated as typical of a kind of material
  ("generally has", "typically about") does not meet I4.
- **I5** The full text is in English.

Then check the three codes that are not tied to a criterion:
- `not_primary`: the document is a review, perspective, thesis, patent, or an
  abstract without data.
- `retracted`: `record.json` has `is_retracted: true`, or the PDF says the
  article is retracted.
- `duplicate_data`: the paper itself states that every H₂ uptake value it
  reports was published before. You cannot search, so apply this code only on
  the paper's own statement.

The paper is eligible when I1 to I5 are all met and none of these three codes
applies. Otherwise give the first applicable exclusion code, in the order of
the §4 table: `theoretical_only`, `electrochemical`, `not_carbon`,
`not_primary`, `retracted`, `no_conditions_stated`, `no_surface_area`,
`not_english`, `duplicate_data`. When I1 is not met, I2 to I4 are not assessed
(`"met": null`), because they concern the paper's H₂ uptake values; the code
is then decided by I1 and the three codes above. An I1 failure is coded
`theoretical_only` when the paper reports only computation or theory,
`electrochemical` when its hydrogen is electrochemical, and otherwise
`no_conditions_stated` (the paper has no H₂ uptake value, so none with stated
temperature and pressure). An I2
failure is `not_carbon`, I3 `no_conditions_stated`, I4 `no_surface_area`, I5
`not_english`.

## Rules

- Quote; do not paraphrase. Each quote is at most 40 words and gives its
  location (file, page, and section, table or figure). A criterion is met only
  with a quote. For I5, quote the article's first sentence.
- For a criterion that is not met, say in `quote` what you searched for and did
  not find, and leave `location` empty.
- Do not search, do not open other files, and do not use what you may remember
  about the paper.

## Output

Write one JSON file to the output path you are given, with Python's `json`
module (`true`, `false` and `null`, not strings):

```json
{
  "frame_id": "...",
  "eligible": true,
  "exclusion_code": null,
  "exclusion_quote": "",
  "exclusion_location": "",
  "criteria": {
    "I1": {"met": true, "quote": "...", "location": "main, p. 3, Section 2.4"},
    "I2": {"met": true, "quote": "...", "location": "..."},
    "I3": {"met": true, "quote": "...", "location": "..."},
    "I4": {"met": true, "quote": "...", "location": "..."},
    "I5": {"met": true, "quote": "...", "location": "..."}
  },
  "notes": ""
}
```

`exclusion_quote` and `exclusion_location` support a `not_primary`,
`retracted` or `duplicate_data` code; leave them empty otherwise. Reply only
with `eligible` or the exclusion code.

## Protocol sections (registered text)

## 3. Definitions

- **Carbon sorbent.** A sorbent whose majority component by mass is carbon, in
  one of the schema's material classes. Metal-decorated carbons and carbon
  composites are included and flagged by class or by `metal_element`. MOFs,
  zeolites, hydrides and uncarbonized polymers are not carbon sorbents.
- **77 K.** A stated temperature of 76.0–79.0 K, or "liquid nitrogen" with no
  number. The latter is stored as 77.3 K with `temperature_inferred = true`.
- **Uptake basis.** *Excess* (Gibbs surface excess), *absolute*, or *total*
  (adsorbed plus gas in the pore volume).
  - `basis_stated = true` only when the paper names the basis and either defines
    it or reports two bases side by side. The supporting quote is stored in
    `basis_evidence`. "Total" with no definition gives `basis_stated = false`.
  - **Analysis basis.** `basis_inferred` is the basis the analyses use, set by
    the first rule that applies:
    - the stated basis, when `basis_stated = true`;
    - excess or absolute, when the paper calls the value by that name without
      defining it;
    - the instrumental default: a volumetric (Sieverts) value is excess; a
      gravimetric value is excess only if the paper states a buoyancy
      correction, otherwise `unknown`; any other method is `unknown`.

    A value called "total" without a definition falls to the instrumental
    default.
  - The v0.1 field `uptake_type` is kept unchanged and is used only by RQ1
    sensitivity (xiii). Every other analysis uses `basis_inferred`.
- **wt% convention.**
  - Definitions: W1 = 100·m(H₂)/m(sorbent); W2 = 100·m(H₂)/[m(sorbent) + m(H₂)];
    W1 = W2/(1 − W2/100).
  - Where the paper gives a value in mmol g⁻¹ or cm³(STP) g⁻¹, W1 is computed
    from that quantity (§11.0) and used instead of the paper's wt%. A value
    given in mg g⁻¹ is W1 by definition (W1 = 0.1 × mg g⁻¹). A wt% stored only
    because it was computed in one of these ways has `wt_pct_convention = W1`
    and `wt_pct_convention_source = computed_from_other_unit`.
  - A reported wt% has `wt_pct_convention_source = stated` if the paper
    defines its convention, and `inferred_from_paired_units` if the paper also
    gives a value in mmol g⁻¹, mg g⁻¹ or cm³(STP) g⁻¹ for the same point and
    only one convention matches it within the printed rounding. Otherwise
    `wt_pct_convention = unknown`, `wt_pct_convention_source = none`, and the
    value is used as reported. A value whose convention is W2 is converted to W1
    before analysis.
  - Reading W2 as W1 understates W1 by W2²/(100 − W2): 0.26, 0.38 and 0.53 wt%
    at 5, 6 and 7 wt%, that is 5.3–7.5% of the reported value (5–7% of W1).
    RQ1 sensitivity (vii) bounds this.
  - When a value is given in two units that disagree beyond either convention,
    this is reported as a unit-consistency failure, and the W1 computed from the
    non-wt% value is used.
- **Maximum excess, n_ex,max.** Defined per isotherm: one sample, 77 K,
  `basis_inferred = excess`, adsorption branch. It is computed by code from the
  extracted points (`hycan.v1.nmax`); extractors do not classify it.
  - *Observed maximum.* The isotherm extends to p_last ≥ 10 bar, and its highest
    point is followed by at least one point at higher pressure that is lower by
    more than the larger of 1% relative and the highest point's recorded
    uncertainty (`uncertainty_wt_pct`, or `digitization_uncertainty_wt_pct` for
    a digitized point).
  - *Plateau.* No observed maximum, p_last ≥ 20 bar, and the value at p_last is
    less than 3% (relative) above the value linearly interpolated at
    0.7 × p_last.
  - *Lower bound.* p_last ≥ 20 bar and neither of the above. A single reported
    point at ≥ 20 bar with no isotherm is a lower bound.
  - Otherwise the isotherm has no n_ex,max.
  - n_ex,max is the highest measured value. Its pressure is `p_at_nmax_bar`,
    and the isotherm's last pressure p_last is `p_last_bar`.
  - **Basis–shape conflict.** An isotherm with `basis_stated = false` and
    `basis_inferred = excess` that has no observed maximum, p_last ≥ 60 bar, and
    a rise of more than 3% between 0.7 × p_last and p_last is coded
    `basis_shape_conflict = true`, because that shape indicates absolute or
    total uptake. It is excluded from RQ1, RQ3 and RQ5, and the count is
    reported.
- **Value kind.** `measured` (a measured point); `fitted_interpolated` (read from
  a curve fitted to, and within the range of, the measured points);
  `fitted_extrapolated` (beyond p_last, or a model parameter such as a Langmuir
  or Tóth capacity); `unclear`. A value the authors call the maximum or
  saturation is `measured` only if it equals a measured point; otherwise it is
  `fitted_extrapolated`.
- **Laboratory.** The research group and institution whose instrument produced
  the value, or the corresponding author's group when the paper does not say.
  In a multi-laboratory paper each participating laboratory is a separate
  laboratory.
- **Material identity.** Supplier, product name and grade, for commercial
  materials only.

## 4. Eligibility (paper level)

Include a paper when all of the following hold:

- **I1.** It reports original experimental measurement of gas-phase H₂ uptake
  (gravimetric, volumetric, or flow).
- **I2.** At least one measured sorbent is a carbon sorbent (§3).
- **I3.** The temperature and pressure of at least one uptake value are stated
  or recoverable from the paper.
- **I4.** A specific surface area is reported for at least one measured sample
  (any method; the method is recorded).
- **I5.** The full text is in English.

Exclude, with the first applicable reason code:

| Code | Reason |
|---|---|
| `theoretical_only` | Computational or theoretical work with no measured H₂ uptake |
| `electrochemical` | Electrochemical hydrogen storage (charging in electrolyte) |
| `not_carbon` | No measured sorbent is a carbon sorbent |
| `not_primary` | Review, perspective, thesis, patent, or abstract without data |
| `retracted` | Retracted article |
| `no_conditions_stated` | No uptake value with stated or recoverable T and P |
| `no_surface_area` | No surface area for any measured sample |
| `not_english` | Full text not in English |
| `duplicate_data` | Every value in the paper appears in an earlier paper |

The last four codes can be applied only to the full text (§6).

## 6. Screening

- **Title and abstract.**
  - Two screening agents work independently, using different Claude models and
    the same frozen prompt (§9).
  - A record may be excluded at this stage only with `theoretical_only`,
    `electrochemical`, `not_carbon`, `not_primary` or `retracted`, and only when
    the title or abstract makes the code clear. Every other record is marked
    include or uncertain.
  - Records with no abstract in either source are screened on title and venue
    under the same rule.
  - A record enters the frame unless both screeners exclude it.
  - Reported: Cohen's κ for include-or-uncertain against exclude, and the share
    of records without an abstract per source.
- **Stratum.** Each screener who does not exclude a record (include or
  uncertain) also sets its stratum flag (§7). If only one screener sets a flag,
  it is used. If both set flags and they disagree, a third agent decides, seeing
  only the title, the abstract and the two flags.
- **Screening accuracy.**
  - Screeners are not told which records are v0.1 papers. The fraction of
    reference-set-A papers in the merged set that reach the frame is reported as
    screening sensitivity. Because the prompts are piloted on v0.1 papers, this
    is optimistic; the same fraction is reported for reference set B.
  - The author screens a simple random sample of 100 records excluded by both
    screeners (all of them, if fewer), drawn with
    `numpy.random.default_rng(20261031).choice` without replacement from those
    records sorted by `frame_id`, blind to their decisions. The share the author would include, with an exact 95% CI,
    estimates the false-exclusion rate.
- **Full text.**
  - For every drawn paper, two agents assess §4 independently on the full text,
    including supplementary information.
  - A third agent resolves disagreements, quoting the text.
  - The author reviews every full-text exclusion reason, and may reverse one
    only by quoting the passage showing that each §4 criterion is met. Reversals
    are logged and counted.
- **Reporting.** Counts at every stage go in a PRISMA 2020 flow diagram (§14).

## 7. Sampling (strata only)

- **Strata.**
  - *S1:* the title or abstract mentions 77 K or liquid nitrogen AND either a
    pressure ≥ 20 bar (≥ 2 MPa) or the words high pressure, saturation or
    excess maximum.
  - *S2:* every other record in the frame, including records without an
    abstract.

## 9. Data extraction and verification

- **Schema.** Extraction follows schema v2: `src/hycan/schema.py` and
  `docs/data_dictionary.md` as committed in the registration commit. Appendix A
  lists every field this protocol adds. A change to either file after
  registration is an amendment (§15).
- **Scope.**
  - Every H₂ uptake value in tables and text is extracted.
  - From figures, every plotted point of every 77 K isotherm is digitized. At
    other temperatures, only the highest-pressure point of each isotherm is
    digitized.
  - When a value appears both in a table or text and in a figure, the table or
    text value is used, and the figure supplies only the isotherm shape.
  - Also recorded where stated: sample mass; degassing temperature and duration;
    H₂ purity; free-volume calibration gas and temperature; the BET P/P₀ range
    and whether consistency criteria were applied; the surface-area probe gas;
    and whether the surface area was measured on the same sample and treatment
    state as the H₂ isotherm.
- **Figure values.**
  - Digitized with `scripts/digitize_figure.py` from the page image, with axes
    calibrated on at least two labelled ticks per axis and a third tick per axis
    as a residual check. Vector paths are not used.
  - A digitized point is the centre of one plotted marker
    (`digitize_figure.py extract --mode markers`). An isotherm drawn as a line
    without markers is digitized at 10 pressures equally spaced between its
    plotted end points. These values are `value_kind = measured` only if the
    paper states that the line joins measured points, otherwise
    `fitted_interpolated`, and their `isotherm_point_count` is left empty.
  - Each extractor digitizes independently. The recorded value is the mean, and
    its uncertainty is the larger of half the difference and 1% of the axis
    span.
  - Every calibration and point set is archived in `data/digitizations/`.
  - The mapping of curves to samples is a categorical field in the agreement
    statistics.
- **Blind dual extraction.**
  - Agents A and B use different Claude models and different inputs: A reads
    the PDF text layer (`pdftotext -layout`) and page images; B reads page
    images only. Neither sees the other's output or any existing row.
  - Agent C, in a separate session, sees A, B and the PDF. C resolves every
    disagreement against the PDF with a quote or figure location, and may enter
    a value neither gave.
  - Rows are matched by code on sample label, temperature (within 1 K),
    pressure (within the larger of 2% and 0.02 bar) and the quantity reported
    (for example gravimetric or volumetric uptake). Unmatched rows count as
    row-detection disagreements.
- **Agreement statistics**, reported per field type:
  - exact agreement and Cohen's κ (categorical fields);
  - the share within printed rounding (table or text) or within 3% relative
    (figures), and the distribution of relative differences (numeric fields);
  - row-detection agreement;
  - C's outcomes: A kept, B kept, new value, both acceptable.
- **Release.** All A, B and C outputs are released.
- **v0.1 papers.** A v0.1 paper drawn into the probability sample and found
  eligible is extracted by A and B and reconciled by C like any drawn paper,
  without access to its v0.1 rows; the v0.1 rows are compared with the
  reconciled rows afterwards. Every other v0.1 paper receives one fresh blind
  extraction by agent B, which C reconciles against the existing v0.1 rows; a
  figure value in such an extraction carries an uncertainty of 1% of the axis
  span. Statistics for these B-only papers are reported separately.
- **Prompts and models.**
  - Screening, eligibility, extraction and reconciliation prompts include §§3,
    4, 6, 7 (strata) and 9 of this protocol and schema v2.
  - The prompts are piloted on v0.1 papers only and then frozen. Their SHA-256
    values and the model identifier for each role are recorded in a dated
    amendment before reference set B is identified (§5). A later model change is
    an amendment.
  - Each role runs once per record or paper. A rerun is allowed only after a
    technical failure (no output, truncated output or tool error) and is logged
    with its reason.
  - Models, versions, prompts and run dates are logged in
    `docs/ai_usage_log.md`.


## Schema v2 (registered text, with paper-specific examples removed)

### src/hycan/schema.py (comments and docstrings removed)

```python
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
```

### docs/data_dictionary.md (paper-specific examples removed)

<!-- docs/data_dictionary.md at the registration commit, with paper-specific examples removed (protocol §15, Amendment 1). -->

# HyCAN-DB Data Dictionary

Every field in the curated dataset is defined below.  
Fields are grouped into five categories matching the curation spreadsheet columns.  
**Required** means the row cannot be imported without a value.  
**Controlled vocabulary** means only the listed strings are accepted.

---

## Paper-Level Fields

### `paper_id`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `HYC-9001` |

**Definition.** Internal sequential identifier for the source paper, assigned by the curator.  
**Units.** None.  
**Scientific significance.** Groups all measurements from a single publication; used as a foreign key throughout the database.  
**If missing.** Cannot be left blank — assign the next unused ID before entering any rows from the paper.

---

### `doi`

| Attribute | Value |
|---|---|
| Type | String (lowercased, no leading `https://doi.org/`) |
| Required | Yes |
| Example | `10.1021/ja0376303` |

**Definition.** Digital Object Identifier uniquely identifying the publication.  
**Units.** None.  
**Scientific significance.** Primary deduplication key; two rows with the same DOI come from the same paper.  
**If missing.** If the paper has no DOI (e.g., a conference poster), enter `no-doi:<first_author>:<year>`.

---

### `first_author`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `Smith` |

**Definition.** Family name (surname) of the first-listed author.  
**Units.** None.  
**Scientific significance.** Human-readable citation shorthand alongside `year`.  
**If missing.** Cannot be left blank; use `Unknown` only for unsigned reports.

---

### `year`

| Attribute | Value |
|---|---|
| Type | Integer, 1990–present |
| Required | Yes |
| Example | `2005` |

**Definition.** Calendar year of publication (print or online-first, whichever is earlier).  
**Units.** None.  
**Scientific significance.** Provides temporal context for the state of the field and material-synthesis capabilities at the time.  
**If missing.** Cannot be left blank; check the DOI record.

---

### `journal`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `Carbon` |

**Definition.** Full journal name as it appears on the article (not abbreviated).  
**Units.** None.  
**Scientific significance.** Useful for filtering by venue or impact level.  
**If missing.** Cannot be left blank; use `Preprint` for arXiv-only papers.

---

### `title`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `Hydrogen sorption in defect-free HiPco single-walled carbon nanotubes` |

**Definition.** Full title of the article, copied verbatim.  
**Units.** None.  
**Scientific significance.** Allows full-text search and disambiguation when multiple papers share an author-year pair.  
**If missing.** Cannot be left blank; retrieve from the DOI record.

---

## Sample-Level Fields

### `sample_id`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `HYC-9001-S1` |

**Definition.** Identifier for a distinct physical sample within one paper. Format: `<paper_id>-S<n>` where *n* increments from 1.  
**Units.** None.  
**Scientific significance.** One paper often reports results for multiple samples (e.g., pristine vs. activated); this field distinguishes them.  
**Uniqueness.** `sample_id` is unique per **physical sample**, not per row. It **may repeat** across rows when the same sample is measured at multiple conditions (e.g., an isotherm sampled at several pressures). The per-row uniqueness key is `measurement_id`, not `sample_id`.  
**If missing.** Cannot be left blank — construct from `paper_id`.

---

### `measurement_id`

| Attribute | Value |
|---|---|
| Type | Text |
| Required | Yes |
| Example | `HYC-9001-M1` |

**Definition.** The unique-per-row key: exactly one `measurement_id` per row in the dataset. Format: `<paper_id>-M<n>` where *n* increments from 1 across all measurements in the paper.  
**Units.** None.  
**Scientific significance.** Because one physical `sample_id` can appear on many rows (measured at multiple temperatures/pressures), a separate per-row identifier is needed as the stable primary key for the dataset. Duplicate `measurement_id` values are a dataset-level error.  
**If missing.** Cannot be left blank — assign the next unused `-M<n>` for the paper.

---

### `material_class`

| Attribute | Value |
|---|---|
| Type | Controlled vocabulary |
| Required | Yes |
| Allowed values | `SWCNT`, `MWCNT`, `DWCNT`, `graphene`, `graphene_oxide`, `reduced_graphene_oxide`, `activated_carbon`, `carbon_nanofiber`, `carbide_derived_carbon`, `templated_carbon`, `carbon_aerogel`, `doped_carbon`, `composite`, `other` |
| Example | `SWCNT` |

**Definition.** The broadest structural/synthetic category of the carbon material.  
**Units.** None.  
**Scientific significance.** The primary grouping variable for comparative analysis; determines which mechanistic models apply (e.g., physisorption on graphenic surfaces vs. intercalation).  
**If missing.** Use `other` and describe fully in `material_description`. If the paper is a composite or heteroatom-doped material, fill `dopant_element` and related fields.

---

### `material_description`

| Attribute | Value |
|---|---|
| Type | Free text |
| Required | Yes |
| Example | `acid-purified SWCNT bundles, diameter 1.2–1.4 nm` |

**Definition.** Short, human-readable description of the sample drawn directly from the paper.  
**Units.** None.  
**Scientific significance.** Captures nuance that controlled-vocabulary fields cannot (e.g., specific diameter range, vendor, batch label).  
**If missing.** Cannot be left blank; paraphrase the paper's material section.

---

### `synthesis_method`

| Attribute | Value |
|---|---|
| Type | Controlled vocabulary |
| Required | If reported |
| Allowed values | `arc_discharge`, `laser_ablation`, `cvd`, `hipco`, `comocat`, `chemical_oxidation`, `chemical_reduction`, `thermal_reduction`, `pyrolysis`, `template_synthesis`, `carbonization`, `carbide_chlorination`, `physical_activation`, `chemical_activation`, `chemical_exfoliation`, `commercial`, `unknown`, `other` |
| Example | `hipco` |

**Definition.** The primary method used to synthesise the raw carbon material.  
**Units.** None.  
**Scientific significance.** Synthesis route strongly influences defect density and purity, which in turn affect H₂ uptake.  
**If missing.** Enter `unknown`.

---

### `purification_method`

| Attribute | Value |
|---|---|
| Type | Free text |
| Required | No |
| Example | `HNO3 reflux 12 h, then vacuum annealing at 400 °C` |

**Definition.** Post-synthesis steps to remove catalytic metal particles, amorphous carbon, or other impurities.  
**Units.** None.  
**Scientific significance.** Purity strongly affects surface area and can add oxygen functional groups that alter uptake.  
**If missing.** Leave null.

---

### `activation_method`

| Attribute | Value |
|---|---|
| Type | Free text |
| Required | No |
| Example | `KOH activation at 800 °C, CO₂ atmosphere, 1 h` |

**Definition.** Chemical or physical treatment applied to increase porosity and surface area.  
**Units.** None.  
**Scientific significance.** Activation is the largest single lever for boosting uptake in activated carbons; recording the method enables structure-property correlation.  
**If missing.** Leave null.

---

### `dopant_element`

| Attribute | Value |
|---|---|
| Type | String or null |
| Required | No |
| Example | `N` |

**Definition.** Chemical symbol of the heteroatom deliberately introduced into the carbon lattice.  
**Units.** None.  
**Scientific significance.** Heteroatom doping modifies electronic structure and can create additional adsorption sites.  
**If missing.** Leave null.

---

### `dopant_concentration_at_pct`

| Attribute | Value |
|---|---|
| Type | Float or null |
| Required | No |
| Example | `4.2` |

**Definition.** Atomic percent of the dopant element as determined by XPS or elemental analysis.  
**Units.** at. %  
**Scientific significance.** Doping level correlates with the density of heteroatom-induced binding sites.  
**If missing.** Leave null.

---

### `functional_groups`

| Attribute | Value |
|---|---|
| Type | Free text or null |
| Required | No |
| Example | `–COOH, –OH` |

**Definition.** Surface functional groups identified or inferred from FTIR/XPS.  
**Units.** None.  
**Scientific significance.** Oxygen-containing groups can both anchor H₂ via weak physisorption and reduce hydrophobic pore access.  
**If missing.** Leave null.

---

## Structural Characterisation Fields

### `bet_surface_area_m2_g`

| Attribute | Value |
|---|---|
| Type | Float, 0–5000 m²/g (schema v2; 0–4000 before) |
| Required | Yes |
| Example | `1200.0` |

**Definition.** Specific surface area from the Brunauer-Emmett-Teller (BET) method applied to N₂ or Ar physisorption data.  
**Units.** m²/g  
**Scientific significance.** BET SSA is the most widely reported structural descriptor and the strongest correlate of gravimetric H₂ uptake across carbon classes.  
**If missing.** Leave null and fill `langmuir_surface_area_m2_g` if a Langmuir value is given instead. Never back-calculate from Langmuir.

---

### `langmuir_surface_area_m2_g`

| Attribute | Value |
|---|---|
| Type | Float or null |
| Required | No |
| Example | `1450.0` |

**Definition.** Specific surface area from the Langmuir monolayer model.  
**Units.** m²/g  
**Scientific significance.** Historically common in early CNT papers; typically ~15–20% higher than BET for microporous carbons.  
**If missing.** Leave null.

---

### `surface_area_method`

| Attribute | Value |
|---|---|
| Type | Controlled: `BET`, `Langmuir`, `geometric`, `DFT`, `alpha_s_plot`, `t_plot`, `unspecified`, `none`, `not_reported` |
| Required | Yes (defaults to `unspecified`) |
| Example | `BET` |

**Definition.** How the reported surface area was determined. Added in schema v1.1.
**Scientific significance.** `bet_surface_area_m2_g` and `langmuir_surface_area_m2_g` are separate fields, which handles papers that name their method. It does not handle a paper reporting one unqualified "surface area" — those values previously had nowhere to go without asserting a method the paper never stated. This field records the absence as `unspecified` rather than guessing, and lets an analysis exclude unmethodded areas when comparing against the Chahine rule, which is defined on BET.
**If missing.** `unspecified`. Use `none` only when the paper reports no surface area at all.

---

### `micropore_volume_cm3_g`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–2 cm³/g |
| Required | No |
| Example | `0.42` |

**Definition.** Volume of pores with width < 2 nm, from t-plot or DFT analysis of physisorption data.  
**Units.** cm³/g  
**Scientific significance.** Micropore volume, not total SSA, is often the dominant predictor of H₂ capacity at 77 K.  
**If missing.** Leave null.

---
### `ultramicropore_volume_cm3_g`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–2 cm³/g |
| Required | No |
| Example | `0.27` |

**Definition.** Pore volume in pores below roughly 0.7 nm, as reported by the source paper. Added in schema v1.1.
**Units.** cm³/g
**The cutoff is the paper's, not ours.** ~0.7 nm is the conventional ultra-micropore boundary, but papers place it differently and determine it by different methods (CO₂ adsorption at 273 K, DFT/NLDFT models, probe molecules of graded size). Record the value the paper reports and put its stated cutoff and method in `notes`. This field is deliberately not validated against a fixed cutoff.
**Validation.** `ultramicropore ≤ micropore ≤ total_pore` is enforced as an ERROR, pairwise, so a missing middle term does not suppress the outer comparison.
**If missing.** Leave null. Most papers do not report it.

---

### `total_pore_volume_cm3_g`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–3 cm³/g |
| Required | No |
| Example | `0.85` |

**Definition.** Total volume of all pores, typically taken at P/P₀ = 0.95–0.99.  
**Units.** cm³/g  
**Scientific significance.** Upper bound on physisorption capacity; separates micro- from meso/macropore contribution.  
**If missing.** Leave null.

---

### `average_pore_diameter_nm`

| Attribute | Value |
|---|---|
| Type | Float or null |
| Required | No |
| Example | `2.1` |

**Definition.** Mean or modal pore size from BJH, DFT, or similar analysis.  
**Units.** nm  
**Scientific significance.** Optimal pore diameter for H₂ physisorption is ~0.5–0.7 nm; larger pores reduce gravimetric density.  
**If missing.** Leave null.

---

## Measurement Fields

### `temperature_k`

| Attribute | Value |
|---|---|
| Type | Float, 50–500 K |
| Required | Conditional — required when the row reports any uptake value; optional on a characterization-only row |
| Example | `77.0` |

**Definition.** Temperature at which the H₂ uptake measurement was made.  
**Units.** K  
**Conversion.** °C → K: add 273.15.  
**Scientific significance.** Temperature is the most critical experimental variable. Cryogenic measurements (77 K) probe physisorption; near-ambient measurements test engineering relevance.  
**If missing.** Cannot be left blank; check experimental section.

---

### `pressure_bar`

| Attribute | Value |
|---|---|
| Type | Float, 0–200 bar |
| Required | Conditional — required when the row reports any uptake value; optional on a characterization-only row |
| Example | `1.0` |

**Definition.** Gas pressure at which the reported uptake was measured.  
**Units.** bar  
**Conversions.** 1 atm = 1.01325 bar; 1 MPa = 10 bar; 1 psi = 0.0689476 bar.  
**Scientific significance.** Together with temperature, pressure defines the thermodynamic state; isotherms are meaningless without both.  
**If missing.** Cannot be left blank; check experimental section or figure axis.

---

### `uptake_wt_pct`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–20 wt% |
| Required | One of `uptake_wt_pct` or `uptake_mmol_g` must be present when the row carries an uptake convertible to wt% (see "A consequence for analysis") |
| Example | `2.1` |

**Definition.** Gravimetric hydrogen uptake in wt%, as the paper reports it. Papers use two conventions: W1 = 100·m(H₂)/m(sorbent) and W2 = 100·m(H₂)/[m(sorbent) + m(H₂)]. Schema v2 records which one in `wt_pct_convention`; the v1.0 analysis converts W2 values to W1 and uses a value of unknown convention as reported (protocol §3).  
**Units.** wt%  
**Scientific significance.** The primary figure of merit for onboard storage; the U.S. DOE target is 6.5 wt% (system-level).  
**If missing.** When the paper gives no wt% for the point, compute W1 from `uptake_mmol_g` (wt% = mmol_per_g × 0.201588) or `uptake_ml_stp_g`, and in schema v2 set `wt_pct_convention_source` to `computed_from_other_unit`. A value printed only in mg/g is stored here as W1 = 0.1 × mg/g, with the same source.

---

### `uptake_mmol_g`

| Attribute | Value |
|---|---|
| Type | Float or null |
| Required | One of `uptake_wt_pct` or `uptake_mmol_g` must be present when the row carries an uptake convertible to wt% (see "A consequence for analysis") |
| Example | `10.4` |

**Definition.** Gravimetric hydrogen uptake in millimoles of H₂ per gram of adsorbent.  
**Units.** mmol/g  
**Conversion.** wt% = mmol_per_g × 0.201588. The factor 0.201588 = 2.01588 g/mol (molar mass of H₂) / 10 (unit conversion).  
**Scientific significance.** Molar units are preferred for thermodynamic modelling (e.g., isotherm fitting with Langmuir or Toth equations).  
**If missing.** Leave null. A v1.0 row fills this field only with a value printed in the paper, because the analysis computes W1 from it (protocol §3); a value computed from wt% would make that circular. Some v0.1 rows hold computed values here, and the v1.0 re-extraction (§9) corrects them.

---

### `uptake_ml_stp_g`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–2225 mL(STP)/g |
| Required | No |
| Example | `233.0` |

**Definition.** As-reported volumetric hydrogen uptake, expressed as a volume of H₂ gas at STP per gram of adsorbent, preserved exactly as the paper reported it.  
**Units.** mL(STP)/g at 273.15 K, 1 atm (STP).  
**Conversion.** mmol/g = mL(STP)/g ÷ 22.414; wt% = (mL(STP)/g ÷ 22.414) × 0.201588. The molar volume 22.414 L/mol (= 22.414 mL/mmol) is the ideal-gas value at 273.15 K, 1 atm — the HyCAN-DB convention. The upper bound 2225 mL(STP)/g corresponds to the 20 wt% ceiling on `uptake_wt_pct`.  
**Scientific significance.** Some older adsorption papers report capacity only in mL(STP)/g; storing the as-reported value keeps a faithful provenance record alongside the canonical `uptake_wt_pct` / `uptake_mmol_g`.  
**If missing.** Leave null if the paper did not report in this unit.

---

### `uptake_type`

| Attribute | Value |
|---|---|
| Type | Controlled vocabulary |
| Required | Yes |
| Allowed values | `excess`, `absolute`, `total`, `unspecified` |
| Example | `excess` |

**Definition.** Thermodynamic definition of the reported uptake quantity.  
- **excess**: the amount adsorbed beyond what the same volume would contain as bulk gas (Gibbs excess). Most gravimetric instruments measure this directly.  
- **absolute**: total amount in the adsorbed phase (excess + pore-volume gas).  
- **total**: entire gas inside the vessel divided by sample mass (instrument-dependent).  
- **unspecified**: the paper does not clarify which definition is used.  
**Units.** None.  
**Scientific significance.** This is the most frequently confused distinction in the H₂ storage literature. Excess and absolute diverge significantly above ~50 bar; mixing them inflates apparent capacity.  
**If missing.** Enter `unspecified` and note it in the `notes` field.

---

### `measurement_method`

| Attribute | Value |
|---|---|
| Type | Controlled vocabulary |
| Required | Yes |
| Allowed values | `volumetric_sieverts`, `gravimetric_microbalance`, `TPD`, `electrochemical`, `not_applicable`, `other`, `unknown` |
| Example | `volumetric_sieverts` |

**Definition.** Instrument/technique used to measure hydrogen uptake.  
**Units.** None.  
**Scientific significance.** Volumetric and gravimetric methods have different systematic error sources; method should be recorded for inter-study comparison.  
**If missing.** Enter `unknown`.

---

### `uncertainty_wt_pct`

| Attribute | Value |
|---|---|
| Type | Float or null |
| Required | No |
| Example | `0.05` |

**Definition.** Reported absolute uncertainty (1σ or stated error bar) in the uptake value, in wt%.  
**Units.** wt%  
**Scientific significance.** Enables proper weighting in regression models and flags measurements that should not be over-interpreted.  
**If missing.** Leave null.

---

## Provenance Fields

### `source_location`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `Table 2, row 3` or `Figure 4a, extracted at P = 20 bar` |

**Definition.** Precise pointer to where in the paper this exact number was found.  
**Units.** None.  
**Scientific significance.** Allows a future curator to verify or correct the value without re-reading the entire paper.  
**If missing.** Cannot be left blank.

---

### `extraction_method`

| Attribute | Value |
|---|---|
| Type | Controlled vocabulary |
| Required | Yes |
| Allowed values | `table_direct`, `text_direct`, `figure_digitized`, `figure_estimated` |
| Example | `table_direct` |

**Definition.** How the numerical value was obtained from the paper.  
- **table_direct**: copied exactly from a table cell.  
- **text_direct**: copied exactly from a sentence in the text.  
- **figure_digitized**: extracted using a digitisation tool (e.g., WebPlotDigitizer).  
- **figure_estimated**: visually estimated from a figure without a digitisation tool.  
**Units.** None.  
**Scientific significance.** Informs the expected precision and signals which values benefit from re-extraction.  
**If missing.** Cannot be left blank.

---

### `extraction_confidence`

| Attribute | Value |
|---|---|
| Type | Integer, 1–5 |
| Required | Yes |
| Example | `5` |

**Definition.** Curator's subjective confidence that the extracted number correctly represents what the paper reports.  
- **5**: value read directly from a clean table — essentially certain.  
- **4**: read from clear text or a high-quality figure with digitisation.  
- **3**: digitised from a moderate-quality figure.  
- **2**: estimated from a low-quality or overlapping figure.  
- **1**: guessed or inferred; substantial uncertainty.  
**Units.** None.  
**Scientific significance.** Used to weight or filter measurements in meta-analyses.  
**If missing.** Cannot be left blank.

---

### `reproducibility_tier`

| Attribute | Value |
|---|---|
| Type | Single character |
| Required | No (schema v2: legacy field) |
| Allowed values | `A`, `B`, `C`, `D` |
| Example | `B` |

**Definition.** Assessment of how reproducible the reported result is likely to be, based on reported experimental detail (defined fully in Part 10 of the curation guide).  
- **A**: full experimental protocol, characterisation data, and uncertainty — could be reproduced by another group.  
- **B**: sufficient detail for reproduction with minor ambiguity.  
- **C**: key parameters missing; rough reproduction only.  
- **D**: insufficient detail to attempt reproduction.  
**Units.** None.  
**Scientific significance.** Filters low-reproducibility entries out of benchmarking datasets.  
**If missing.** May be blank on v1.0 rows.  
**Schema v2 status: legacy.** The v0.1 rubric behind this field awarded points for agreeing with the Chahine rule, so a tier filter partly assumed the answer to the Chahine test. No v1.0 analysis uses this field. The v1.0 reporting-completeness score (`reporting_score`, `reporting_tier`, protocol §10.1) replaces it and is computed by code.

---

### `notes`

| Attribute | Value |
|---|---|
| Type | Free text or null |
| Required | No |
| Example | `Authors report "excess" uptake but use a volumetric instrument without void-volume correction` |

**Definition.** Any curation notes, caveats, or flags not captured by structured fields.  
**Units.** None.  
**Scientific significance.** Qualitative metadata that prevents future curators from making the same mistakes.  
**If missing.** Leave null.

---

### `extractor`

| Attribute | Value |
|---|---|
| Type | String |
| Required | Yes |
| Example | `AG` |

**Definition.** Initials of the person who extracted the data.  
**Units.** None.  
**Scientific significance.** Enables inter-extractor reliability analysis.  
**If missing.** Cannot be left blank.

---

### `extraction_date`

| Attribute | Value |
|---|---|
| Type | Date string, `YYYY-MM-DD` |
| Required | Yes |
| Example | `2026-06-09` |

**Definition.** ISO 8601 date on which the row was extracted.  
**Units.** None.  
**Scientific significance.** Version-control for the dataset; later schema changes can be applied only to rows extracted after a given date.  
**If missing.** Cannot be left blank.

---

### `verified_by`

| Attribute | Value |
|---|---|
| Type | String or null |
| Required | No |
| Example | `RK` |

**Definition.** Initials of a second curator who independently cross-checked this row.  
**Units.** None.  
**Scientific significance.** Rows with `verified_by` set can be trusted at a higher level for benchmarking.  
**If missing.** Leave null.

---

### `verification_date`

| Attribute | Value |
|---|---|
| Type | Date string or null, `YYYY-MM-DD` |
| Required | No |
| Example | `2026-06-15` |

**Definition.** ISO 8601 date on which verification was completed.  
**Units.** None.  
**Scientific significance.** Enables detection of stale verifications if the row is later edited.  
**If missing.** Leave null.

---

## Schema v1.2 Fields — Qualifiers on What a Row Asserts

Eleven fields added in schema v1.2, at physical positions 41–51.

Every one is defaulted so that rows predating the migration remain valid unchanged — a pre-v1.2 row does assert an exact, isothermal measurement with both conditions stated, which is what the defaults say.

### `uptake_bound`

| Attribute | Value |
|---|---|
| Type | Controlled: `exact`, `upper`, `lower`, `approximate` |
| Required | Yes (defaults to `exact`) |
| Example | `upper` |

**Definition.** Whether the uptake fields hold a measured value or a bound on one. `upper` means the true uptake is *below* the recorded number; `lower` means above.
**Downstream contract.** Any row whose value is not `exact` must be excluded from isotherm fitting and from headline capacity statistics, and plotted as an arrow rather than a point.
**If missing.** `exact`.

---

### `temperature_unstated` and `pressure_unstated`

| Attribute | Value |
|---|---|
| Type | Boolean |
| Required | Yes (default `false`) |
| Example | `true` |

**Definition.** That the source paper never stated this condition numerically, which is the only circumstance in which an uptake-bearing row may leave `temperature_k` or `pressure_bar` null. A condition stated only in words ("room temperature") is not a number and is not imputed.
**Validation.** A flag set `true` while its field is populated is an ERROR — a row cannot both state a condition and declare it unstated. The flag is the only way to get a null past the conditions check, so nulls cannot appear by accident.
**If missing.** `false`.

---

### `measurement_mode`

| Attribute | Value |
|---|---|
| Type | Controlled: `isothermal`, `temperature_cycle`, `TPD`, `flow` |
| Required | Yes (defaults to `isothermal`) |
| Example | `temperature_cycle` |

**Definition.** What kind of measurement produced the uptake. A weight difference across a temperature cycle, or a TPD desorption integral, is not an isothermal uptake and must not be recorded as one.
**Downstream contract.** Analysis restricts to `isothermal` by default.
**If missing.** `isothermal`, which is true of every row predating v1.2.

---

### `reference_temperature_k`

| Attribute | Value |
|---|---|
| Type | Float or null, 50–1500 K |
| Required | No |
| Example | `573` |

**Definition.** The temperature of the state the uptake is referenced *against*, for a measurement that is not isothermal.
**Units.** K
**Why the range runs to 1500 K.** This is a desorption endpoint, not a measurement temperature, so `temperature_k`'s 50–500 K window does not apply.
**Validation.** Required on any non-isothermal row that reports an uptake.
**If missing.** Leave null; meaningful only when `measurement_mode` is not `isothermal`.

---

### `metal_element`, `metal_loading_wt_pct`, `residual_metal_element`, `residual_metal_wt_pct`

| Attribute | Value |
|---|---|
| Type | String or null; float or null, 0–100 wt% |
| Required | No |
| Example | `Pd`, `5.0` |

**Definition.** `metal_*` is an intentionally added supported metal and its loading by weight. `residual_metal_*` is leftover synthesis catalyst.
**Units.** Weight percent.
**Why these are separate from `dopant_*`.** A supported catalyst particle and a substitutional lattice heteroatom work by different mechanisms: a lattice heteroatom such as boron or nitrogen is a dopant; an impregnated metal such as cobalt or palladium is a supported metal. `dopant_concentration_at_pct` is atomic percent.
**Why residual metal matters separately.** Residual synthesis catalyst decides whether an uptake is the carbon's at all.
**If missing.** Leave null. Most papers have no supported metal.

---

### `dopant_concentration_wt_pct` and `dopant_concentration_method`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–100 wt%; controlled: `elemental_analysis`, `XPS`, `AAS`, `ICP`, `other` |
| Required | No |
| Example | `3.5`, `elemental_analysis` |

**Definition.** Dopant concentration by weight, and the technique that measured it.
**Units.** Weight percent. Use `dopant_concentration_at_pct` for atomic percent; never convert between them, since the conversion needs a composition the paper may not give.
**Why the method field exists.** Bulk (elemental analysis) and surface (XPS) contents can differ systematically; a concentration without its technique is not comparable across papers.
**If missing.** Leave null.

---

## Schema v1.3 Fields — Surface Area, Pore Method, and Volumetric Capacity

Sixteen fields added in schema v1.3, at physical positions 52–67: surface-area components and methods, pore-volume methods and cutoffs, and volumetric and areal capacity.

Every field is defaulted so that rows predating the migration remain valid unchanged.

### `bet_surface_area_m2_g` — what it has always meant

Not a new field, restated here because v1.3 makes the point checkable. **It is the paper's headline *total* specific surface area**, whatever method produced it; `surface_area_method` says which. It is *not* necessarily a BET value.

### `micropore_surface_area_m2_g`, `external_surface_area_m2_g`

Float, 0–4000 m²/g, optional. A paper may resolve its surface area into
components instead of reporting a total.

**A caveat that travels with `external_surface_area_m2_g`.** It is not necessarily a geometric external surface: a paper's external area may include mesopore surface, in which case a mesopore surface area cannot be recovered from it. A paper reporting a genuinely geometric external area needs a `notes` entry saying so.

When a row carries a micropore area, an external area **and** a total, the validator warns if the parts do not account for the whole — relative *and* absolute, 10% and 50 m²/g, both must be exceeded.

### `surface_area_method` — three values that mean three different things

The vocabulary includes `alpha_s_plot`, `t_plot` and `not_reported`. The three no-method values are distinct and the distinction is **enforced, not merely documented**:

| Value | Meaning | Area field |
| --- | --- | --- |
| `unspecified` | An area **is** reported, with no stated method | always populated |
| `none` | The paper reports no surface area for **any** sample | always null |
| `not_reported` | **This sample** has none, in a paper that reports areas for its others | always null |

### `pore_volume_method`, `pore_volume_probe_gas`

Controlled, default `unspecified`. How the row's pore volumes were determined.

`pore_volume_method`: `DR`, `DFT`, `NLDFT`, `QSDFT`, `BJH`, `HK`, `t_plot`,
`alpha_s_plot`, `other`, `unspecified`.
`pore_volume_probe_gas`: `N2`, `CO2`, `Ar`, `He`, `other`, `unspecified`.

Micropore volumes from different methods and probe gases (DR on CO2 at 273 K, DR on N2 at 77 K, DFT, αs-plot) are not comparable numbers; record the method and probe gas with the volume.

The probe gas matters on its own: a paper may measure surface area by N2 at 77 K and micropore volume by CO2 at 273 K on the same row.

**One method/probe pair per row, not per field.** Where a row's pore volumes were determined by different methods, `notes` records it and these fields carry the primary.

The probe temperature is not a separate field: N2 physisorption is taken as 77 K and CO2 as 273 K, so the gas carries the temperature. A paper that deviates gets a `notes` entry.

### `micropore_volume_co2_cm3_g`

Float, 0–2 cm³/g, optional. A second micropore volume, from CO2.

Named by probe gas rather than by pore size on purpose: calling a CO2-DR volume "ultramicropore" would assert a cutoff the paper may never state.

### `mesopore_volume_cm3_g`

Float, 0–3 cm³/g, optional. Reported by several corpus papers with nowhere to go.
The validator checks that it nests inside `total_pore_volume_cm3_g` (an error) and
warns if micropore + mesopore exceeds the total beyond 10% and 0.05 cm³/g — a
warning rather than an error because papers round to two decimals and an
unreported macropore class can make the parts fall short of the whole.

### `ultramicropore_cutoff_nm`

Float, 0–2 nm, optional, but **required whenever `ultramicropore_volume_cm3_g` is
populated** — a populated volume with a null cutoff is a validation error.

An ultramicropore comparison only works if every value shares a cutoff, and papers' cutoffs differ (0.7 nm, 1 nm, or none stated).

The cutoff is stated per row instead of assumed from this document. Filter on the cutoff before comparing values.

### `pore_diameter_method`

Controlled, default `unspecified`: `BJH`, `DR_characteristic_energy`, `HK`,
`stoeckli_L0`, `DFT`, `geometric_from_S_V`, `other`, `unspecified`.

`average_pore_diameter_nm` would otherwise mix quantities that are not interchangeable: a BJH desorption average (a mesopore size, invalid for a type-I isotherm), a DR characteristic-energy slit width, an HK median micropore size, and Stoeckli's L0.

`geometric_from_S_V` is a width back-calculated from the micropore area and volume under an assumed pore shape. It is **not a pore-size-distribution model at all**, so recording it as BJH or DFT would misdescribe how the number was obtained.

### `volumetric_capacity_kg_m3`, `volumetric_capacity_basis`, `volumetric_capacity_includes_compressed_gas`

`volumetric_capacity_kg_m3`: float, 0–200 kg/m³, optional. Hydrogen stored per unit volume. **`volumetric_capacity_basis` is required whenever it is populated** — an unqualified volumetric figure is not interpretable, because per pore volume and per tank volume can differ by more than a factor of two.

`volumetric_capacity_basis`: `micropore_volume`, `total_pore_volume`,
`packing_volume`, `tank_volume`, `other`.

`volumetric_capacity_includes_compressed_gas`: bool, default `False`. `True` when the figure includes the compressed hydrogen in the tank volume, as a total-per-tank figure does; an adsorbed-phase density excludes it.

### `adsorbed_phase_density_kg_m3`

Float, 0–200 kg/m³, optional. Hydrogen density **in the adsorbed phase**, per
volume of pore, excluding compressed gas.

A separate field from `volumetric_capacity_kg_m3` rather than a basis value on it, because a paper can report both an adsorbed density per micropore volume and a capacity per tank volume for the same sample at the same conditions.

### `packing_density_g_cm3`, `skeletal_density_g_cm3`

Float, 0–5 g/cm³, optional.

`packing_density_g_cm3` is sample mass per volume of tank — the quantity that converts an adsorbed amount into a system-level capacity. A compacted, loose or tapped density should be identified in `notes`.

**`skeletal_density_g_cm3` is load-bearing, not decorative.** A helium (skeletal) density may be what a paper uses to subtract the compressed-gas contribution from a measured weight increase; without it, the excess/absolute basis of that paper's numbers cannot be reconstructed.

### `areal_uptake_g_cm2`

Float ≥ 0, optional. Hydrogen per unit area of a film or supported sample.

An areal uptake lets a reader check a gravimetric figure against the paper's own film mass and area.

### `interlayer_spacing_nm`

Float ≥ 0, optional. The d-spacing between graphene or graphitic layers, from XRD.

### A consequence for analysis: not every uptake converts to wt%

v1.3 admits rows whose only uptake is volumetric or areal. Before it,
`at_least_one_uptake` required a gravimetric value on any row reporting uptake,
"so that a volumetric-only row cannot enter without a value the analysis can use
directly" — a rule written when the only volumetric-looking field was
`uptake_ml_stp_g`, which **does** convert to wt%.

`volumetric_capacity_kg_m3` does not convert without a density the paper may not state, and computing a wt% from it would present this project's arithmetic as the paper's measurement.

So a row may report uptake and carry a null `uptake_wt_pct`. **Any gravimetric analysis must filter on `uptake_wt_pct` presence rather than on "reports uptake",** because a null is dropped silently by a mean.

---

## Schema v2 Fields — the v1.0 Protocol

Schema v2 adds the fields that `docs/v1_protocol.md` needs. Every one is optional
and defaults to null, which keeps every v0.1 row valid.

**A row counts as coded under schema v2 once `basis_stated` is not null**, and
the extraction codes it on every row. On an uncoded row, null means "not yet
coded". On a coded row:

- every boolean and categorical that applies must be coded, and the schema
  rejects the row otherwise. Each vocabulary has a value for "not stated", such
  as `false`, `unknown`, `unspecified` or `unclear`. The fields are
  `basis_inferred`, `wt_pct_convention`, `wt_pct_convention_source`,
  `value_kind`, `isotherm_branch`, `temperature_inferred`, `data_location`,
  `instrument_identified`, `calibration_described`, `replicates_reported` and
  `measuring_lab_id` always; `surface_area_probe_gas` and `area_same_sample`
  when the row reports a surface area; `bet_range_stated` and
  `bet_consistency_criteria_stated` when that area is BET;
- a null numeric or text field means the paper does not state the quantity, or,
  for `isotherm_id`, `material_identity`, `duplicate_of` and `frame_id`, that the
  field does not apply (a single point, a non-commercial material, no earlier
  report, a paper outside the frame).

So an uncoded field never passes for a coded `false`: `basis_stated` null says
nobody has looked, `false` says the paper does not name its basis. Computed
fields (`src/hycan/v1.py`) are produced only for coded rows. Rules are in the
protocol; section numbers below refer to it.

### `basis_stated`, `basis_evidence`

Boolean, plus the quoted text. `true` only when the paper names the uptake basis
(excess, absolute, or total) **and** defines it or reports two bases side by
side (§3). "Total" with no definition is `false`. A `true` must carry the quote
in `basis_evidence`; the schema rejects a `true` with an empty quote.

### `basis_inferred`

Allowed values: `excess`, `absolute`, `total`, `unknown`. The basis the analysis
uses, set by the first rule of §3 that applies: the stated basis when
`basis_stated` is `true`; `excess` or `absolute` when the paper calls the value
by that name without defining it; otherwise the instrumental default, under
which a volumetric (Sieverts) value is `excess`, a gravimetric value is `excess`
only if a buoyancy correction is stated (else `unknown`), and any other method
is `unknown`. A value called "total" without a definition falls to the
instrumental default.

### `wt_pct_convention`, `wt_pct_convention_source`

`wt_pct_convention` allowed values: `W1`, `W2`, `unknown`. W1 is
100·m(H₂)/m(sorbent); W2 is 100·m(H₂)/[m(sorbent) + m(H₂)].
`wt_pct_convention_source` allowed values: `stated`,
`inferred_from_paired_units`, `computed_from_other_unit`, `none`. A reported wt%
is `stated` if the paper defines its convention, and
`inferred_from_paired_units` if the paper also gives a value in mmol g⁻¹,
mg g⁻¹ or cm³(STP) g⁻¹ for the same point and only one convention matches it
within the printed rounding. `computed_from_other_unit` means the paper gives no
wt% for the point and the stored wt% was computed as W1 from its value in one
of those units. `none` means no basis for either convention. The schema checks
that the two agree: `computed_from_other_unit` goes with `W1`, `stated` and
`inferred_from_paired_units` with `W1` or `W2`, and `none` with `unknown`.
Whatever the source, the analysis computes W1 from `uptake_mmol_g` or
`uptake_ml_stp_g` when either is present (§3).

### `value_kind`

Allowed values: `measured`, `fitted_interpolated`, `fitted_extrapolated`,
`unclear`. `measured` is a measured point. `fitted_interpolated` is read from a
curve fitted to, and within the range of, the measured points.
`fitted_extrapolated` lies beyond the highest measured pressure, or is a model
parameter such as a Langmuir or Tóth capacity. A value the authors call the
"maximum" or "saturation" is `measured` only if it equals a measured point.

### `isotherm_id`, `isotherm_branch`, `isotherm_point_count`

`isotherm_id` is an identifier shared by every row from one isotherm (one
sample, one temperature, one instrument run). It is what lets code find an
isotherm's maximum (§3) instead of an extractor guessing it.
`isotherm_branch` allowed values: `adsorption`, `desorption`, `not_applicable`.
`isotherm_point_count` is the number of measured points in the source isotherm,
including points not extracted.

### `temperature_inferred`

Boolean. `true` when the paper says "liquid nitrogen" with no number; the row
then carries `temperature_k = 77.3`, which the schema enforces. A number printed
in the paper is never inferred.

### `data_location`

Allowed values: `main_text`, `SI`. Where the value was found. Supplementary
information is part of the full text (§8).

### `digitization_uncertainty_wt_pct`

Float, wt%. For `figure_digitized` rows only: the larger of half the difference
between the two independent digitizations and 1% of the axis span (§9).

### `surface_area_probe_gas`

Allowed values: `N2`, `Ar`, `CO2`, `other`, `unspecified`. The gas behind the
reported surface area. The analysis uses a BET area only when the gas is `N2`,
`Ar` or `unspecified`, and treats `unspecified` as N₂ (§11.0).

### `bet_range_stated`, `bet_consistency_criteria_stated`

Booleans. Whether the paper states the relative-pressure range used for the BET
fit, and whether it says that consistency criteria (for example Rouquerol's)
were applied. BET areas of microporous carbons depend on both.

### `area_same_sample`

Allowed values: `yes`, `parent_material`, `other_paper`, `unclear`. Whether the
surface area was measured on the same sample, in the same treatment state, as
the H₂ uptake. `parent_material` covers an area reported for the carbon before
doping, metal decoration or densification. Only `yes` enters the analysis.

### `degas_temperature_c`, `degas_duration_h`, `degas_end_pressure_pa`

Degassing before the H₂ measurement: temperature (°C), duration (h) and final
pressure (Pa). Distinct from `activation_method`, which keeps its v0.1 meaning of
synthesis activation (for example KOH activation).

### `sample_mass_mg`, `h2_purity_pct`, `free_volume_calibration`

Sample mass used for the H₂ measurement (mg), hydrogen purity (%), and the
free-volume calibration as text (gas and temperature, for example "He at
77 K"). Small sample masses and helium calibration at 77 K are both known error
sources on microporous carbons.

### `instrument_identified`, `calibration_described`, `replicates_reported`

Booleans. Instrument named (manufacturer and model, or home-built with a
description); the free-volume determination (volumetric) or buoyancy correction
(gravimetric) stated; at least two independent measurements of the sample, or a
numerical uncertainty, reported.

### `measuring_lab_id`, `material_identity`, `duplicate_of`

`measuring_lab_id` names the laboratory whose instrument produced the value
(§3); in a multi-laboratory paper each laboratory gets its own. `material_identity`
is supplier, product and grade for commercial materials, else null.
`duplicate_of` is the `measurement_id` of an earlier report of the same
measurement in the dataset (an earlier report outside the dataset is cited in
`notes` instead). Such a row is excluded from an analysis only when the row it
points to is in the same analysis set (§11.0).

### `selection_route`, `frame_id`

`selection_route` allowed values: `S1`, `S2`, `legacy_v0.1`,
`legacy_v0.1_ineligible`. How the paper entered the dataset (§7): an eligible
paper drawn from stratum S1 or S2 of the probability sample, or a v0.1 paper
outside the sample (`legacy_v0.1` if eligible under protocol §4,
`legacy_v0.1_ineligible` if not, drawn or not). `frame_id` is the paper's
identifier in the sampling frame.

### Computed fields (processed release only)

`basis_shape_conflict`, `nmax_status`, `p_at_nmax_bar`, `p_last_bar`,
`reporting_score` and `reporting_tier` are computed by `src/hycan/v1.py` from
the fields above. They appear in the processed release and are never entered by
an extractor. `nmax_status` takes the values `observed_max`, `plateau`,
`lower_bound` and `none` (§3); `reporting_tier` takes `A` to `D` by the §10.1
thresholds.


