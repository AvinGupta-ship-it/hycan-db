# Role: v0.1 sample labeller (protocol §9, §15 Amendment 1)

This paper was extracted for HyCAN-DB v0.1. Its v0.1 rows describe each sample
in free text, without the printed sample label that the v1.0 matching code
uses. You give each v0.1 sample its label as printed in the paper, so that code
can match the v0.1 rows to a fresh extraction. You do not see the fresh
extraction, and nobody who extracts this paper sees your output.

## Input

A directory, given to you by path, holding:
- `paper.json`: the paper's identity;
- the paper's PDF files, and `text/` and `pages/`: the PDF text layer and one
  PNG image per page;
- `v01_rows.csv`: the paper's v0.1 rows.

## What to do

For each distinct `sample_id` in `v01_rows.csv`, find the sample in the paper
from its `material_description` and its values (conditions, uptake, surface
area), and give:
- `label`: the sample's label exactly as printed in the paper (for example
  `ACA-2550` or `CMS 4A`). When the paper prints several labels for one
  sample, use the one in the first table that reports its uptake, or else in
  the first figure legend that shows it, or else the first one in the text.
  Samples the paper prints no label for are `(unlabelled 1)`,
  `(unlabelled 2)`, ... in the order they first appear in the paper. In a
  multi-laboratory paper the label is the sample's label, ` / `, and the
  laboratory's label as printed (for example `CMS 4A / participant 10`); give
  each laboratory's rows of one v0.1 `sample_id` the label of that laboratory,
  by listing the rows' `measurement_id`s in `measurement_ids`.
- `evidence`: a quotation of at most 25 words showing the label and the
  sample, with its location (file, page, table or figure).

If the rows of one v0.1 `sample_id` belong to samples with different printed
labels, give one line per label with the `measurement_id`s of its rows. If a
v0.1 sample cannot be found in the paper, its label is `(unidentified)`, with
the reason in `evidence`. Do not correct or judge the v0.1 values; that is the
reconciler's task.

Do not search, do not open files outside your input, output and work
directories, and do not use what you may remember about the paper or about
HyCAN-DB. Keep every file you make in your work directory.

## Output

Write `labels.csv` in the output directory with Python's `csv` module
(`csv.DictWriter`, default quoting, `lineterminator="\n"`), UTF-8, with the
header `sample_id,measurement_ids,label,evidence`. `measurement_ids` is empty
when the label applies to every row of the `sample_id`; otherwise it lists the
rows it applies to, separated by `;`. Leave an empty field empty: never write
`None`, `NA` or `null`. Reply only with the number of lines written.

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

## 10. Quality coding (§10.1 only)

### 10.1 Reporting-completeness score

Each row scores one point per item:

1. `basis_stated = true` (§3 evidence rule);
2. `temperature_unstated = false` and `temperature_inferred = false`;
3. `pressure_unstated = false`;
4. surface-area method named (BET, Langmuir, DFT, α_s, t-plot or geometric) and
   its probe gas stated;
5. a total or micropore volume reported for this sample, with its method;
6. degassing before the H₂ measurement reported, with temperature and duration
   (or end vacuum) both stated;
7. instrument identified (manufacturer and model, or home-built with a
   description), and the free-volume determination (volumetric) or buoyancy
   correction (gravimetric) stated;
8. a numerical uncertainty for this value or its isotherm, or at least two
   independent measurements of this sample, reported;
9. the value belongs to an isotherm with at least 5 measured points.

- **Tiers:** A is 8–9, B 6–7, C 4–5, D 0–3. `reporting_score` and
  `reporting_tier` are computed by code from the recorded fields, and no tier is
  assigned by judgement.
- **Outcome-independence.** No item depends on the measured uptake.
- **Coding.** The items are coded in dual extraction, and κ per item is
  reported.
- **Use.** The score is used only as an RQ1 moderator and in RQ1 sensitivity
  (viii); otherwise it is descriptive.
- **Legacy field.** The v0.1 field `reproducibility_tier` is kept under its v0.1
  name as a legacy field and is used by no v1.0 analysis.

## 11. Analysis plan (§11.0 only)

### 11.0 General rules

- **Area rule.** RQ1, RQ2, RQ3, RQ5 and §10.2 use a surface area only when all
  of these hold:
  - `surface_area_method = BET`;
  - `surface_area_probe_gas` is `N2`, `Ar` or `unspecified`; an unspecified
    gas is treated as N₂, and the probe temperature is not recorded;
  - `area_same_sample = yes`.

  Langmuir, DFT, CO₂-derived and unspecified-method areas are recorded but not
  analysed. The primary RQ1 domain is A_BET ≥ 300 m² g⁻¹. Below it, N₂ at 77 K
  can miss narrow pores that H₂ enters, and a given absolute error in the area
  changes the ratio more; sensitivity (vi) removes the floor. The probe gas, the
  stated P/P₀ range and whether consistency criteria were stated are recorded
  and reported.
- **Row filters.** RQ1, RQ2, RQ3 and RQ5 use only rows with
  `measurement_mode = isothermal`, `uptake_bound` ∈ {exact, approximate},
  `isotherm_branch` ≠ desorption and `value_kind = measured`, except where an
  RQ1 sensitivity analysis states otherwise. Other rows are released but not
  analysed.
- **Unit of analysis.**
  - A sample is one material in one synthesis and treatment state, as defined
    by the authors.
  - Per sample and laboratory, RQ1 takes the geometric mean of the n_ex,max
    values of its eligible isotherms (replicates, cycles or instruments) and
    records the count. Only adsorption branches are used.
  - When a sample has both excess and another basis, the excess value is used.
  - When several laboratories measure one sample within a paper, RQ3 uses each
    laboratory's value, and RQ1 uses their median as one sample, with a
    laboratory identifier of its own (paper_id + "-multilab").
  - A row that re-reports a measurement already published (same sample and
    isotherm, cited as such) records the earlier report's `measurement_id` in
    `duplicate_of` when that report is in the dataset, and the citation in
    `notes` otherwise. In each analysis, a row whose `duplicate_of` row is in the
    same analysis set is excluded; otherwise the row is used.
  - The same commercial material measured anew in another paper is a separate
    sample with the same material identity.
- **Conversions.**
  - Pressure is absolute, in bar: MPa × 10; atm × 1.01325; kPa × 0.01;
    psi × 0.0689476; Torr or mmHg × 0.00133322. A value the paper calls gauge
    is converted to bar and then increased by 1.01325 bar.
  - Temperature: °C + 273.15.
  - W1 wt% = 0.201588 × mmol g⁻¹ = 0.1 × mg g⁻¹ = 0.0089938 × cm³(STP) g⁻¹, with
    STP = 273.15 K and 101.325 kPa unless the paper states another reference.
  - Source values are stored with the digits printed. Derived values are stored
    unrounded and rounded only for display.
- **Missing data.** Each analysis is complete-case for the variables it uses,
  and the samples and papers lost to each missing variable are reported. There
  is no imputation, except that the RQ5 tree model handles missing features
  natively.
- **Outliers.** No value is excluded for being extreme. Influence is reported
  through leave-one-laboratory-out estimates and by listing samples with
  |standardized residual| > 3. The plausibility flag enters only through RQ1
  sensitivity (iv).
- **Software.** Python and package versions are pinned in
  `requirements-v1.lock` in the registration commit. Every analysis runs from a
  committed script with fixed seeds.

