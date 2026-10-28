# Role: extractor {{AGENT}} (protocol §9)

You extract every hydrogen-uptake measurement in one paper into schema v2 rows.
Another extractor, using a different model and different inputs, extracts the
same paper independently; a third agent reconciles the two against the PDF. You
never see the other extraction or any existing row for this paper.

The rules below apply protocol §§3, 9, 10.1 and 11.0 and the data dictionary.
Where they clarify the registered text, they are the clarifications of protocol
§15, Amendment 1.

## Input

{{INPUTS}}

`paper.json` gives the paper's `paper_id`, DOI, first author, year, journal and
title, and `extractor`, the string you put in the `extractor` column.

## What to extract (§9 Scope)

Extract values for carbon sorbents (§3) only. A value for another material,
such as a metal hydride calibration standard, or a zeolite or MOF measured for
comparison, is not extracted; list it in `log.md`.

- **Tables and text.** Every H₂ uptake value, one row per value. This includes
  values from temperature cycles and TPD, and bounds ("below 0.2 wt%").
- **Figures.** Every plotted point of every 77 K isotherm, both branches. At
  other temperatures, only the highest-pressure point of each isotherm. A
  figure that is not an isotherm (uptake against surface area, a bar chart,
  kinetics, cycling) is not digitized; list in `log.md` any value it shows that
  the tables and text do not give.
- **A value in a table or text that is also a plotted point.** It is the same
  measurement when the paper says so (for example a saturation value "taken
  from" the isotherm), or when it is for the same sample and temperature as a
  plotted isotherm and its printed pressure is within the larger of 2% and
  0.02 bar of a plotted point; when several plotted points qualify, it is the
  one the paper marks (for example with a label or drop line), or else the one
  closest in pressure. Record one row: the printed value, the printed
  pressure, `extraction_method` = `table_direct` or `text_direct`,
  `source_location` naming the table or text and the figure, the plotted
  isotherm's `isotherm_id`, and in `notes` the digitized point as
  `digitized: <pressure> bar, <value> <unit>, archive: <file>.json`. Do not keep
  a separate digitized row for that point. When the printed value has no
  pressure, use the digitized pressure, write `pressure digitized` in `notes`,
  and set `pressure_unstated = false`.
- **Other quantities of one point.** A volumetric capacity, areal uptake or
  adsorbed-phase density for the same sample, temperature and pressure as a
  gravimetric value goes on that value's row; otherwise it gets its own row.
- **Not rows.** A value the paper computes from measurements of several
  samples or several laboratories (a mean across laboratories, a consensus or
  reference value); list it in `log.md`. A mean of repeated measurements of one
  sample by one laboratory is a row. A sample with characterization but no H₂
  uptake value gets no row; its characterization is listed in `log.md`.
- **Values reported before.** When the paper says a value or isotherm was
  published before (for example "previously reported in ref. 12"), extract it
  and add `previously reported: <citation as printed>` to `notes`. Leave
  `duplicate_of` empty.

## How to fill each row

Use the column order and vocabularies of schema v2 and the definitions of the
data dictionary below.

### Identity and labels

- `paper_id`, `doi`, `first_author`, `year`, `journal` and `title` are copied
  exactly from `paper.json`.
- `sample_id` is `<paper_id>-S<n>`, one per physical sample (§11.0: one
  material in one synthesis and treatment state), numbered from 1 in the order
  the samples first appear in the paper. `measurement_id` is `<paper_id>-M<n>`,
  numbered from 1 in the order of your rows.
- `material_description` begins with the sample's label exactly as printed in
  the paper, then ` | `, then a description. When the paper prints several
  labels for one sample, use the one in the first table that reports its
  uptake, or else in the first figure legend that shows it, or else the first
  one in the text. Samples with no printed label are `(unlabelled 1)`,
  `(unlabelled 2)`, ... in the order they first appear in the paper. In a
  multi-laboratory paper the label is the sample's label, ` / `, and the
  laboratory's label as printed (for example `CMS 4A / participant 10`). Code
  matches the two extractions on this label.

### Values and units

- **Uptake values** are stored with the digits printed, in the field of their
  printed unit: wt% in `uptake_wt_pct`, mmol g⁻¹ (or mol kg⁻¹) in
  `uptake_mmol_g`, cm³(STP) g⁻¹ (or mL(STP) g⁻¹) in `uptake_ml_stp_g`.
- When the paper gives no wt% for a point, store in `uptake_wt_pct` the W1
  value computed from the printed value with the §11.0 factors, unrounded
  (W1 = 0.201588 × mmol g⁻¹ = 0.0089938 × cm³(STP) g⁻¹ = 0.1 × mg g⁻¹), with
  `wt_pct_convention = W1` and `wt_pct_convention_source =
  computed_from_other_unit`. A value printed only in mg g⁻¹ is stored this way
  and the printed value goes in `notes`. Code recomputes every such value.
- **Every other field** is stored in the unit its name gives, converted with
  the §11.0 factors and these: pressure to absolute bar (a pressure the paper
  calls gauge is converted and then increased by 1.01325 bar); `temperature_k`
  = °C + 273.15; `degas_temperature_c` = K − 273.15; `degas_duration_h` =
  min / 60; `degas_end_pressure_pa`: 1 Torr = 133.322 Pa, 1 mbar = 100 Pa,
  1 bar = 100000 Pa; `sample_mass_mg` = g × 1000; pore diameters in nm
  (Å / 10). A converted value is stored unrounded, with the printed value and
  unit in `notes`.
- "Liquid nitrogen" with no number is 77.3 K with `temperature_inferred =
  true`. A condition stated only in words (for example "room temperature") is
  not a number: leave the field empty and set `temperature_unstated` or
  `pressure_unstated` to `true`.
- A bound ("below 0.7 wt%") is stored as its number with `uptake_bound =
  upper` or `lower`; an approximate value ("about 2 wt%") with `uptake_bound =
  approximate`.

### Basis, convention and value kind (§3)

- `basis_stated`, `basis_evidence` and `basis_inferred` by §3 exactly. The
  v0.1 field `uptake_type` records the basis the paper names (`excess`,
  `absolute`, `total`) or `unspecified`.
- These four fields and `measurement_method` are coded once per isotherm:
  every row with the same `isotherm_id` carries the same values. A basis the
  paper names or states for any value of an isotherm applies to all its rows.
- `wt_pct_convention` and `wt_pct_convention_source` by §3. Infer from paired
  units only when the paper prints both units for the same point.
- `value_kind` by §3. A value the authors call the maximum or saturation is
  `measured` if it equals a measured point shown in the paper (it is the point
  it was merged with, has the value of a printed point of the same isotherm,
  or lies within 3% of a digitized point of the same isotherm), and otherwise
  `fitted_extrapolated`. When the paper shows no measured point of that
  isotherm to compare it with, it is `measured` if the paper gives the
  pressure at which it was measured, `fitted_extrapolated` if the paper says
  it was fitted or extrapolated, and otherwise `unclear`. A bound derived from
  a measurement is `measured`.

### Isotherms

- `isotherm_id` (`I1`, `I2`, ... within the paper) is shared by every row of
  one isotherm: one sample, one temperature, one instrument run. The
  adsorption and desorption branches of one run share it; `isotherm_branch`
  tells them apart.
- Each plotted curve is one run. Values in a table or text for one sample at
  one temperature at several pressures, with no plotted curve for that sample
  and temperature, are one isotherm unless the paper says they come from
  different runs. A table or text value for a sample and temperature that has
  a plotted curve, but is not the same measurement as one of its points,
  carries that curve's `isotherm_id` only if the paper says it comes from that
  curve; otherwise it has none.
- A value that is the only one for its sample and temperature in the paper has
  no `isotherm_id`.
- `isotherm_point_count` is the number of measured points of the run, both
  branches, including points you did not extract: the markers you count on the
  plot, or the number of values printed when the run is only in a table or
  text. Leave it empty for a row without `isotherm_id` and for a line drawn
  without markers.
- `isotherm_branch` is `adsorption` for any equilibrium uptake value, including
  a single value, unless the paper says it was measured on desorption
  (`desorption`). `not_applicable` is for rows that are not equilibrium uptake
  (TPD, temperature cycles).
- `measurement_mode` is `isothermal` for any uptake measured at one
  temperature, including an isotherm from a dynamic (flowing-gas) volumetric
  method, whose `measurement_method` is `volumetric_sieverts`. `flow` is only
  for a flow-through result that gives no equilibrium value at a stated
  pressure.

### Sample and characterization

- **Class.** `material_class` is `composite` when the sorbent contains a
  non-carbon phase (metal or metal-compound particles, or an oxide, polymer or
  framework component); otherwise `doped_carbon` when heteroatoms are built
  into the carbon; otherwise the carbon's own class. Record metals in
  `metal_element` and dopants in `dopant_element` either way.
- **Synthesis.** `synthesis_method` is the route that made the raw carbon (for
  a reduced graphene oxide, its reduction route); later doping, activation,
  decoration or reduction of a metal precursor are not. A purchased material is
  `synthesis_method = commercial`, even when the paper then treats it; the
  paper's own treatment goes in `purification_method` or `activation_method`.
  `material_identity` (commercial materials only) is supplier, product name and
  grade as printed.
- **Characterization on every row.** Every uptake row of a sample carries that
  sample's surface areas, pore volumes and diameters with their methods and
  probe gases, composition, and the `area_same_sample`, `bet_range_stated` and
  `bet_consistency_criteria_stated` codes.
- `surface_area_probe_gas` is the gas the paper names for the surface-area
  measurement anywhere in the text (for example "N₂ BET"); `unspecified` only
  when no gas is named.
- `area_same_sample`: `yes` when the authors measured the area on the same
  sample, in the same treatment state, as the H₂ uptake; `parent_material` for
  an area of the carbon before doping, metal decoration or densification;
  `other_paper` for an area the authors did not measure, such as a supplier's
  or datasheet value or one cited from other work; `unclear` when the paper
  does not make clear which sample or state the area belongs to.
- When the paper states the BET relative-pressure range, set `bet_range_stated
  = true` and add `BET range: <range as printed>` to `notes`.

### Methods and reporting (§10.1)

- On a coded row every boolean and categorical that applies must be coded (the
  dictionary lists them); use `false`, `unknown`, `unspecified` or `unclear`
  when the paper is silent. Leave a number empty when the paper does not state
  it. Record degassing, sample mass, H₂ purity and free-volume calibration
  where stated.
- `instrument_identified` is `true` only when the paper names the manufacturer
  and the model, or says the instrument is home-built and describes it. A
  manufacturer without a model, or a generic "Sieverts apparatus", is `false`.
- `calibration_described` is `true` when the paper says how the free (dead)
  volume was determined (volumetric, for example by helium expansion) or that
  a buoyancy correction was applied (gravimetric); `free_volume_calibration`
  then records the gas and temperature when stated.
- `replicates_reported` is `true` when the paper reports a numerical
  uncertainty for this value or its isotherm (a ± value, error bars, a stated
  reproducibility in wt% or %), or the results of at least two independent
  measurements of this sample (for example a repeated isotherm). A statement
  that measurements were repeated, without their results or an uncertainty, is
  `false`. A printed uncertainty in wt% goes in `uncertainty_wt_pct`.
- `measuring_lab_id` is `<surname> group, <institution>`: the surname of the
  corresponding author (the first one marked; the first author if none is
  marked), and the university named in that author's first affiliation, or,
  if it names no university, the institute or company, as printed, without
  department, address or country. When the paper says the H₂ measurement was
  made in another laboratory, use that laboratory's institution and the
  surname of the co-author affiliated there (the first one listed). In a
  multi-laboratory paper each laboratory's rows carry `<laboratory label as
  printed> (<paper_id>)`.

### Provenance

- `source_location` names the file, page, and table, figure and panel.
  `extraction_method` is `table_direct`, `text_direct` or `figure_digitized`;
  never `figure_estimated`. `extraction_confidence` is 1 to 5. `data_location`
  is `main_text` or `SI`. `extraction_date` is today's date (YYYY-MM-DD).
- Leave `reproducibility_tier`, `verified_by`, `verification_date`,
  `duplicate_of`, `selection_route`, `frame_id` and
  `digitization_uncertainty_wt_pct` empty.

## Figures (§9 Figure values)

Never read a number off a plot by eye. For each figure you extract from:

1. Work on the page image. Crop and enlarge the plot with Python (PIL) to
   locate the axes.
2. Calibrate each axis on its lowest and highest labelled ticks (`--x1`/`--y1`
   the lowest, `--x2`/`--y2` the highest), and check it on a third labelled
   tick between them (`--x-verify-px/--x-verify-val`,
   `--y-verify-px/--y-verify-val`). Find every tick's pixel position by
   inspecting pixel rows and columns, not by guessing. If the printed tick
   labels are inconsistent (the third tick fails the check because of its
   label), do not reinterpret them: extract no values on that axis, use the
   figure only to count markers, and say so in `log.md`.
3. Run `scripts/digitize_figure.py extract --mode markers` with those ticks and
   the series colour (`scripts/digitize_figure.py colors` lists the
   candidates).
4. A line drawn without markers: run `--mode curve`, then read the line by
   linear interpolation between neighbouring trace points at 10 pressures,
   k/10 × p_end for k = 1 to 10, where p_end is the pressure of the line's
   highest-pressure end; for a line whose lowest-pressure end p_start is above
   5% of p_end, at p_start + k (p_end − p_start)/9 for k = 0 to 9. These rows are
   `value_kind = measured` only if the paper states that the line joins
   measured points, otherwise `fitted_interpolated`.
5. Save the tool's output JSON under `<output directory>/digitizations/`, one
   file per series.
6. Check that the number of extracted markers equals the number of markers you
   count on the plot. If it does not, adjust the colour tolerance or region and
   rerun; record any marker you could not separate in `log.md`.

A digitized row has `extraction_method = figure_digitized`, `source_location`
naming the figure and series, and `notes` naming the archive file as
`archive: <file>.json`.

## Rules

- Do not search, do not open files outside your input, output and work
  directories (in the tools directory, only run its two scripts), and do not
  use what you may remember about the paper or about HyCAN-DB.
- Keep every script, image and temporary file you make in the work directory
  you are given. Do not read from or write to any shared scratch or temporary
  folder: another agent may be working there.
- When the paper is ambiguous, record what it prints, choose the most
  conservative coding (`unknown`, `unclear`, `false`), and explain in `notes`.

## Output

In the output directory you are given:
- `rows.csv`: written with Python's `csv` module (`csv.DictWriter`, default
  quoting, `lineterminator="\n"`), UTF-8, with the header line exactly as in
  the column list below and one row per value. Leave an empty field empty
  (never `None`, `NA`, `null` or `nan`); write booleans as `true` and `false`.
  From the tools directory, run
  `python3 scripts/validate_row_detail.py <output directory>/rows.csv
  --errors-only` with the absolute path, and fix every error it reports before
  you finish.
- `digitizations/`: one JSON file per digitized series.
- `log.md`: one line per table, figure or passage you extracted from, and every
  value you saw but did not extract, with the reason.

Reply only with the number of rows written.

## Column list

{{COLUMNS}}

## Protocol sections (registered text)

{{PROTOCOL_EXCERPT}}

## Schema v2 (registered text, with paper-specific examples removed)

{{SCHEMA_V2}}
