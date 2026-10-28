# Role: reconciler C (protocol §9)

{{MODE_INTRO}}

The extraction rules the extractors followed are in the extraction prompt; the
ones you need are restated here. Where they clarify the registered text, they
are the clarifications of protocol §15, Amendment 1.

## Input

A directory, given to you by path, holding:
- `paper.json`: the paper's identity, `extractor` (the string for the
  `extractor` column of every reconciled row) and `verifier` (the string for
  `verified_by`);
- the paper's PDF files, and `text/` and `pages/`: the PDF text layer and one
  PNG image per page, as the extractors had them;
- `first/rows.csv` and `second/rows.csv`: {{MODE_SOURCES}};
- `first/digitizations/` and `second/digitizations/`, where present: the
  archived digitizations each row's `notes` names;
{{MODE_INPUTS}}- `match.csv`: the code's matching of the two row sets, described below;
- `digitized_means.csv`: the value and uncertainty code assigns to figure
  points, described below.

### `match.csv`

{{MATCH_RULES}}

### `digitized_means.csv`

One line per figure point, keyed by `match_line`: `from` (`both`, `first` or
`second`: whose digitization the line uses), `uptake_field` (the column the
value belongs in), `value` (in that column's unit), `pressure_bar`,
`digitization_uncertainty_wt_pct` (always in wt%) and `basis`. {{FIGURE_RULE}}

## What to do

1. Work through `match.csv` line by line. For every field that differs, and
   for every unmatched row, find the answer in the paper: a quotation (at most
   40 words, with file, page, and table or section) or a figure location.
2. Decide each one: the first value, the second value, a value neither gave, or
   both acceptable (when the paper supports both codings equally; say why).
3. Where the two extractions agree, keep the value. Correct an agreed value
   only if the paper plainly contradicts it, and log that as a new value.
4. Figure points. A reconciled `figure_digitized` row takes `value`,
   `pressure_bar` and `digitization_uncertainty_wt_pct` from its
   `digitized_means.csv` line; taking them from there needs no line in
   `resolutions.csv`, but correcting one does. When the two row sets assign a
   plotted curve to different samples, settle the assignment from the figure
   and its legend, log it as a `curve_sample_mapping` line, pair the points of
   the same plotted curve yourself, and compute their value and uncertainty by
   the rule above from the two archive files. When a point has two lines
   because the two sets digitized it in different units, use the line in the
   unit of the figure's axis.
5. Apply the identity rules below, then run, from the tools directory,
   `python3 scripts/validate_row_detail.py <output directory>/rows.csv
   --errors-only` with the absolute path, and fix every error it reports.
6. Check that every line of `match.csv` other than `agree` lines has at least
   one line in `resolutions.csv`.

### Rules the extractors followed that you will need

- A value for a material that is not a carbon sorbent (§3) is not a row. A
  value computed from measurements of several samples or laboratories is not a
  row. A sample with no H₂ uptake value gets no row. Every uptake row of a
  sample carries that sample's characterization.
- A figure that is not an isotherm is not digitized, and neither is an axis
  whose printed tick labels are inconsistent.
- The sample label is the one in the first table that reports the sample's
  uptake, or else in the first figure legend, or else the first in the text;
  samples with no printed label are `(unlabelled 1)`, `(unlabelled 2)`, ... in
  order of first appearance.
- A value in a table or text that is the same measurement as a plotted point
  (the paper says so, or the same sample and temperature with a printed
  pressure within the larger of 2% and 0.02 bar of a plotted point, the one
  the paper marks or else the closest in pressure) is one
  row: the printed value and pressure, `table_direct` or `text_direct`, the
  plotted isotherm's `isotherm_id`, and the digitized point in `notes`. With no
  printed pressure, the pressure is digitized and `notes` say so.
- `isotherm_id` is shared by one sample, one temperature, one instrument run,
  both branches. `isotherm_point_count` counts every measured point of the run,
  both branches; it is empty for a row without `isotherm_id` and for a line
  drawn without markers. A value that is the only one for its sample and
  temperature has no `isotherm_id`. Table or text values for one sample and
  temperature at several pressures, with no plotted curve, are one isotherm.
- `basis_stated`, `basis_evidence`, `basis_inferred`, `uptake_type` and
  `measurement_method` are the same on every row of an isotherm; a basis the
  paper names or states for any value of the isotherm applies to all its rows.
- `value_kind` of a value the authors call the maximum or saturation:
  `measured` if it equals a measured point shown in the paper (the point it
  was merged with, the value of a printed point of the same isotherm, or
  within 3% of a digitized point of the same isotherm), otherwise
  `fitted_extrapolated`; when the paper shows no measured point of that
  isotherm, `measured` if the paper gives its pressure, `fitted_extrapolated`
  if the paper says it was fitted or extrapolated, otherwise `unclear`.
- `measurement_mode` is `isothermal` for any uptake at one temperature,
  including a dynamic volumetric isotherm (`measurement_method =
  volumetric_sieverts`); `flow` only for a flow-through result with no
  equilibrium value at a stated pressure.
- `material_class` is `composite` when the sorbent contains a non-carbon
  phase, otherwise `doped_carbon` when heteroatoms are built into the carbon,
  otherwise the carbon's own class. `synthesis_method` is the route that made
  the raw carbon (for a reduced graphene oxide, its reduction route), or
  `commercial` for a purchased material.
- Uptake values keep their printed digits in the field of their printed unit;
  a point with no printed wt% carries the W1 value computed from its printed
  unit (`W1`, `computed_from_other_unit`). Other fields are in the unit their
  name gives.
- `area_same_sample` is `other_paper` for an area the authors did not measure
  (supplier, datasheet or cited value). `instrument_identified` needs the
  manufacturer and model, or a described home-built instrument.
  `calibration_described` needs the free-volume determination (volumetric) or a
  buoyancy correction (gravimetric). `replicates_reported` needs a numerical
  uncertainty for the value or its isotherm, or the results of at least two
  independent measurements of the sample.
- `measuring_lab_id` is `<surname> group, <institution>` for the
  corresponding author (the first one marked, or the first author if none is
  marked) and the university in that author's first affiliation (else the
  institute or company), unless the paper says another laboratory made the H₂
  measurement; in a multi-laboratory paper, `<laboratory label as printed>
  (<paper_id>)`.

### Identity rules

- A matched pair and a kept `only_first` row keep the first row set's
  `measurement_id`, `sample_id` and `isotherm_id`.
- A kept `only_second` row takes the `sample_id` of the first row set's sample
  with the same label, or else a new `<paper_id>-S<n>` numbered after the
  first set's highest; the `isotherm_id` of the first set's isotherm that the
  rest of its isotherm matched, or else a new `I<n>` numbered after the first
  set's highest; and a new `measurement_id` numbered after the first set's
  highest, in row order.
- Fields that are not compared (`material_description`, `source_location`,
  `notes`, `basis_evidence`, `extraction_date`, `extraction_confidence`) come
  from the row whose values you kept: the first row set's row for a matched
  pair. You may add to `notes`.
- Every row: `extractor` = the `extractor` string in `paper.json`,
  `verified_by` = its `verifier` string, `verification_date` = today
  (YYYY-MM-DD). Leave `selection_route`, `frame_id`, `duplicate_of` and
  `reproducibility_tier` as the kept row has them.
{{MODE_RULES}}
Do not search, do not open files outside your input, output and work
directories (in the tools directory, only run its two scripts), and do not use
what you may remember about the paper or about HyCAN-DB. Keep every file you
make in your work directory.

## Output

In the output directory you are given, both files written with Python's `csv`
module (`csv.DictWriter`, default quoting, `lineterminator="\n"`), UTF-8,
empty fields empty (never `None`, `NA`, `null` or `nan`), booleans `true` and
`false`:
- `rows.csv`: the reconciled rows, with the header line exactly as in the
  column list below;
- `resolutions.csv` with the header
  `match_line,field,first_value,second_value,decision,final_value,evidence,location`.
  - A differing field: `field` is the column name; `decision` is `first`,
    `second`, `new` or `both_acceptable`, and `final_value` the value kept.
  - An unmatched row: `field` is `row`; `decision` is `first` when the
    reconciled rows follow the first row set (an `only_first` row kept, an
    `only_second` row dropped), `second` when they follow the second, and
    `new` when your row differs from both (for example a split or merged
    row); `final_value` is the reconciled `measurement_id`, or empty for a
    dropped row.
  - A curve assigned to different samples: `field` is
    `curve_sample_mapping`, `first_value` and `second_value` the two
    assignments, `final_value` yours, `location` the figure and curve.
  - A row neither extraction has, or a correction of an agreed value: the
    `match_line` of the nearest line (empty for a new row), `decision` `new`.
{{MODE_OUTPUT}}
Reply only with the number of reconciled rows.

## Column list

{{COLUMNS}}

## Protocol sections (registered text)

{{PROTOCOL_EXCERPT}}

## Schema v2 (registered text, with paper-specific examples removed)

{{SCHEMA_V2}}
