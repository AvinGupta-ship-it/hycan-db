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
| Allowed values | `arc_discharge`, `laser_ablation`, `cvd`, `hipco`, `comocat`, `chemical_oxidation`, `chemical_reduction`, `thermal_reduction`, `pyrolysis`, `template_synthesis`, `carbonization`, `commercial`, `unknown`, `other` |
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
| Required | Yes |
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
| Required | Yes |
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
