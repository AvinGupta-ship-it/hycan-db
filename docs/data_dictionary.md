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
| Example | `HYC-0001` |

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
| Example | `Panella` |

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
| Example | `HYC-0001-S1` |

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
| Example | `HYC-0001-M1` |

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
| Allowed values | `arc_discharge`, `laser_ablation`, `cvd`, `hipco`, `comocat`, `chemical_oxidation`, `chemical_reduction`, `thermal_reduction`, `pyrolysis`, `template_synthesis`, `carbonization`, `carbide_chlorination`, `commercial`, `unknown`, `other` |
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
| Type | Float, 0–4000 m²/g |
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
| Type | Controlled: `BET`, `Langmuir`, `geometric`, `DFT`, `unspecified`, `none` |
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
**The cutoff is the paper's, not ours.** ~0.7 nm is the conventional ultra-micropore boundary, but papers place it differently and determine it by different methods (CO₂ adsorption at 273 K, DFT/NLDFT models, probe molecules of graded size). Record the value the paper reports and put its stated cutoff and method in `notes`. This field is deliberately not validated against a fixed cutoff, because doing so would silently exclude papers using a defensible alternative.
**Scientific significance.** This is the field the corpus most needed. Two papers in the corpus deviate from the Chahine rule and the explanation each offers turns on pore size rather than total area — HYC-0021 (Sethia 2016) finds uptake tracks ultra-micropore volume, not BET. Without this field that claim cannot be tested across the corpus, and the distinguishing quantity is stranded in free-text notes.
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
| Required | One of `uptake_wt_pct` or `uptake_mmol_g` must be present |
| Example | `2.1` |

**Definition.** Gravimetric hydrogen uptake expressed as mass of H₂ divided by total sample mass, multiplied by 100.  
**Units.** wt%  
**Scientific significance.** The primary figure of merit for onboard storage; the U.S. DOE target is 6.5 wt% (system-level).  
**If missing.** Compute from `uptake_mmol_g` via wt% = mmol_per_g × 0.201588 / 10. Leave null only if `uptake_mmol_g` is filled.

---

### `uptake_mmol_g`

| Attribute | Value |
|---|---|
| Type | Float or null |
| Required | One of `uptake_wt_pct` or `uptake_mmol_g` must be present |
| Example | `10.4` |

**Definition.** Gravimetric hydrogen uptake in millimoles of H₂ per gram of adsorbent.  
**Units.** mmol/g  
**Conversion.** wt% = mmol_per_g × 0.201588. The factor 0.201588 = 2.01588 g/mol (molar mass of H₂) / 10 (unit conversion).  
**Scientific significance.** Molar units are preferred for thermodynamic modelling (e.g., isotherm fitting with Langmuir or Toth equations).  
**If missing.** Compute from `uptake_wt_pct`. Leave null only if `uptake_wt_pct` is filled.

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
| Allowed values | `volumetric_sieverts`, `gravimetric_microbalance`, `TPD`, `electrochemical`, `other`, `unknown` |
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
| Required | Yes |
| Allowed values | `A`, `B`, `C`, `D` |
| Example | `B` |

**Definition.** Assessment of how reproducible the reported result is likely to be, based on reported experimental detail (defined fully in Part 10 of the curation guide).  
- **A**: full experimental protocol, characterisation data, and uncertainty — could be reproduced by another group.  
- **B**: sufficient detail for reproduction with minor ambiguity.  
- **C**: key parameters missing; rough reproduction only.  
- **D**: insufficient detail to attempt reproduction.  
**Units.** None.  
**Scientific significance.** Filters low-reproducibility entries out of benchmarking datasets.  
**If missing.** Cannot be left blank.

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

Eleven fields added in schema v1.2, at physical positions 41–51. Each exists
because a real paper could not be recorded without it; the paper is named in
each entry. Rationale and the fixes still outstanding are in
`docs/schema_v1_2_gaps.md`; the migration is `scripts/migrate_v1_2.py`.

Every one is defaulted so that all 156 rows predating the migration remain valid
unchanged — a pre-v1.2 row does assert an exact, isothermal measurement with
both conditions stated, which is what the defaults say.

### `uptake_bound`

| Attribute | Value |
|---|---|
| Type | Controlled: `exact`, `upper`, `lower`, `approximate` |
| Required | Yes (defaults to `exact`) |
| Example | `upper` |

**Definition.** Whether the uptake fields hold a measured value or a bound on
one. `upper` means the true uptake is *below* the recorded number; `lower` means
above.
**Scientific significance.** A paper reporting "below 0.2 wt.%" has no exact
value. Before this field the only options were to write `0.2`, which turns a
bound into a measured point that enters isotherm fits and Chahine comparisons,
or to drop the measurement. Both are wrong, and the second is worse than it
looks: null and bounded results are the corrective to this literature's
optimistic publication bias. A database that can record 8.0 wt% but not "below
0.2 wt%" systematically over-represents the field's successful tail.
**Papers this exists for.** HYC-0017 (Ma 2009), whose room-temperature result —
"the hydrogen uptake is below 0.2 wt.% at 290 K" — is the paper's headline
*negative* finding and the reason it was published. HYC-0029 (Chen 2008), whose
two high-temperature activated samples are reported only as "more than 1.0 wt.%".
**Downstream contract.** Any row whose value is not `exact` must be excluded from
isotherm fitting and from headline capacity statistics, and plotted as an arrow
rather than a point.
**If missing.** `exact`.

---

### `temperature_unstated` and `pressure_unstated`

| Attribute | Value |
|---|---|
| Type | Boolean |
| Required | Yes (default `false`) |
| Example | `true` |

**Definition.** That the source paper never stated this condition numerically,
which is the only circumstance in which an uptake-bearing row may leave
`temperature_k` or `pressure_bar` null.
**Scientific significance.** Schema v1.1 made the conditions conditional —
required with an uptake, optional without — which solved characterization-only
rows. It did not solve a paper that reports an uptake without stating the
conditions as numbers. Imputing a convention is not available here: "room
temperature" in a 2002 Chinese laboratory and a 2016 Indian one are not the same
number, the difference matters at these uptake levels, and substituting 298 K
fabricates a measurement condition. The flag makes the absence explicit and
filterable instead of leaving analysis to discover a null.
**Papers these exist for.** HYC-0011 (Qikun 2002) and HYC-0015 (Rajaura 2016),
both of which report uptakes at "room temperature" and give no number anywhere;
HYC-0009's six TPD rows, which state an adsorption temperature but describe the
gas only as "H2 (40 cc/min) for 1 h"; and HYC-0026 (Zhao 2013), whose uptake
sentence states no pressure and every pressure in which belongs to a different
quantity measured on a different instrument.
**Validation.** A flag set `true` while its field is populated is an ERROR — a
row cannot both state a condition and declare it unstated. The flag is the only
way to get a null past the conditions check, so nulls cannot appear by accident.
**If missing.** `false`.

---

### `measurement_mode`

| Attribute | Value |
|---|---|
| Type | Controlled: `isothermal`, `temperature_cycle`, `TPD`, `flow` |
| Required | Yes (defaults to `isothermal`) |
| Example | `temperature_cycle` |

**Definition.** What kind of measurement produced the uptake.
**Scientific significance.** This is the field that stops the corpus quietly
corrupting itself. HYC-0029 (Chen 2008) reports weight differences across a
303 → 673 → 303 K cycle at ambient pressure in flowing hydrogen. Its numbers are
not isothermal uptakes: nothing is measured at a single temperature, and the
reference state is a sample at 673 K still sitting in 1 atm of hydrogen rather
than a vacuum or zero-coverage baseline. Recording a single `temperature_k` for
such a row asserts an isothermal measurement that did not happen. Sixteen rows
of that paper, plus HYC-0011's third powder measurement, plus HYC-0009's six TPD
rows, are non-isothermal and must be excluded from Chahine plots and isotherm
fits.
**Downstream contract.** Analysis restricts to `isothermal` by default.
**If missing.** `isothermal`, which is true of every row predating v1.2.

---

### `reference_temperature_k`

| Attribute | Value |
|---|---|
| Type | Float or null, 50–1500 K |
| Required | No |
| Example | `673` |

**Definition.** The temperature of the state the uptake is referenced *against*,
for a measurement that is not isothermal.
**Units.** K
**Why the range runs to 1500 K.** This is a desorption endpoint, not a
measurement temperature, so `temperature_k`'s 50–500 K window does not apply.
HYC-0029's is 673 K; HYC-0009's TPD integrals run to 723.15 K.
**Scientific significance.** Without it a temperature-cycle uptake has no defined
reference state and cannot be interpreted at all, let alone compared.
**Validation.** Required on any non-isothermal row that reports an uptake.
**If missing.** Leave null; meaningful only when `measurement_mode` is not
`isothermal`.

---

### `metal_element`, `metal_loading_wt_pct`, `residual_metal_element`, `residual_metal_wt_pct`

| Attribute | Value |
|---|---|
| Type | String or null; float or null, 0–100 wt% |
| Required | No |
| Example | `Co`, `14.62` |

**Definition.** `metal_*` is an intentionally added supported metal and its
loading by weight. `residual_metal_*` is leftover synthesis catalyst.
**Units.** Weight percent.
**Why these are separate from `dopant_*`.** A supported catalyst particle and a
substitutional lattice heteroatom work by different mechanisms. HYC-0025's boron
and HYC-0026's nitrogen are dopants; HYC-0029's cobalt and HYC-0027's palladium
are impregnated metal. Collapsing them into `dopant_element` would make the
spillover subset uninterpretable. `dopant_concentration_at_pct` is also atomic
percent, and both spillover papers report weight percent.
**Scientific significance.** Before v1.2 *both* of the corpus's spillover papers
had their primary independent variable stranded in free text, so the spillover
subset could not be analysed against metal loading at all — which is the one
thing those papers are about.
**Why residual metal matters separately.** Residual synthesis catalyst is the
Hirscher-contamination class of problem: it decides whether an uptake is the
carbon's at all. HYC-0029 reports 1.02, 0.16, 0.09 and 0.15 wt% residual cobalt
by AAS alongside its intentional loadings.
**If missing.** Leave null. Most papers have no supported metal.

---

### `dopant_concentration_wt_pct` and `dopant_concentration_method`

| Attribute | Value |
|---|---|
| Type | Float or null, 0–100 wt%; controlled: `elemental_analysis`, `XPS`, `AAS`, `ICP`, `other` |
| Required | No |
| Example | `15.07`, `elemental_analysis` |

**Definition.** Dopant concentration by weight, and the technique that measured
it.
**Units.** Weight percent. Use `dopant_concentration_at_pct` for atomic percent;
never convert between them, since the conversion needs a composition the paper
may not give.
**Scientific significance.** HYC-0026 (Zhao 2013) reports nitrogen content only
in weight percent, across 0.20–15.07 wt%, and that is the variable its title is
about. With no field for it the paper's central result was unrecordable, and all
seven of its rows were held out of the dataset.
**Why the method field exists.** The same paper reports bulk (elemental
analysis) and surface (XPS) nitrogen contents that differ systematically — its
own explicit finding, and a factor of two on one sample. A concentration without
its technique is not comparable across papers.
**If missing.** Leave null.
