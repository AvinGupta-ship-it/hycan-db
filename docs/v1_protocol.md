# HyCAN-DB v1.0 protocol

**Registration.** This file, `src/hycan/schema.py`, `docs/data_dictionary.md`
and `requirements-v1.lock`, as committed in the registration commit, are
archived together in a standalone Zenodo record, separate from the dataset's
own record. `docs/v1_registration.md` gives the record's DOI, the commit SHA and
the SHA-256 of each archived file. The Zenodo publication date is the
registration date. Before it, no v1.0 search request (§5) is sent, and no frame
record, sampled paper or new data value is seen. After registration no part of
this file, appendices included, is edited. The only permitted change is a dated
amendment appended at the end of §15, stating which data, if any, had been seen
when it was made.

Author: Avin Gupta (ORCID 0009-0009-4133-2275).

## 1. Background and knowledge at registration

An independent referee review of v0.1 (October 2026) found four problems:
- the 51-paper corpus was assembled by hand-steered searching rather than a
  reproducible protocol;
- the reproducibility tiers partly rewarded agreement with the hypothesis they
  were used to test;
- the verification agent saw the values it was checking;
- the headline Chahine-rule estimate pooled ~1 bar and high-pressure
  measurements, so it did not estimate the maximum excess uptake per unit area
  that the rule describes.

In the referee's audit, 237 v0.1 rows checked against the source PDFs held no
numeric transcription errors.

v1.0 changes four things:
- it keeps the v0.1 rows and re-verifies them under a blind protocol;
- it adds papers drawn by probability sampling from a reproducible search;
- it extends the schema to represent the quantity under test;
- it replaces the analyses with those specified here.

**Knowledge at registration.** Before writing this protocol the author had seen
all v0.1 rows and the referee's re-analyses of them. Those included pooled
ratios to the Chahine rule of 1.01 [0.93, 1.09] (77 K, ≥20 bar, stated excess,
7 papers) and 1.27 [1.10, 1.46] (77 K, ≥20 bar, excess plus unspecified basis,
17 papers). No v1.0 search result, frame record or new-paper value had been
seen. The primary analysis (§11, RQ1) is therefore restricted to the
probability sample (unless the RQ1 robustness rule makes sensitivity (iii)
primary), and analyses using v0.1 papers that were not drawn are secondary.

## 2. Research questions

- **RQ1 (primary).** At 77 K, what is the ratio of the maximum Gibbs-excess H₂
  uptake of carbon sorbents to the Chahine rule's prediction (1 wt% per
  500 m² g⁻¹ of BET area), and does it lie within ±15% of 1? Secondary: the
  log-log slope of maximum excess uptake on BET area.
- **RQ2.** How does 77 K uptake near 1 bar scale with BET area and with
  micropore volume?
- **RQ3.** For commercial materials measured by two or more independent
  laboratories, how large is the between-laboratory dispersion of BET area,
  maximum excess uptake, 1-bar uptake and uptake per unit area?
- **RQ4.** In a probability sample of the eligible papers matched by the search,
  how often are the key measurement conditions and corrections reported, and
  how often does a paper report a value that fails the plausibility screen of
  §10.2?
- **RQ5.** How well does a paper-grouped machine-learning model predict 77 K
  excess uptake, compared with physically motivated baselines?

**Margin basis.** In a 14-laboratory round robin on one commercial microporous
carbon of BET area 423 m² g⁻¹ (Zlotea et al. 2009, Int. J. Hydrogen Energy 34,
3044, in this corpus as HYC-0060), the between-laboratory relative standard
deviation of 77 K uptake rose with pressure to a maximum of 14% (up to
1.8 MPa). It was computed on the 9 isotherms that passed the authors'
reversibility criterion; the scatter among all 14 laboratories was larger. BET
areas computed by 61 laboratories from identical isotherms also varied widely
(Osterrieth et al. 2022, Adv. Mater. 34, 2201502). A systematic deviation of the
average ratio smaller than the between-laboratory scatter of a single
measurement could not be detected by one laboratory on one material, so ±15% is
taken as the smallest deviation of practical interest and used as the
equivalence margin.

**Rule source.** The rule is used as stated by Kabbour et al. (2006, Chem.
Mater., HYC-0046): about 1 wt% for every 500 m² g⁻¹ of BET area, applied to the
maximum (saturation) surface excess at 77 K. Kabbour et al. note that this
differs somewhat from Chahine's analyses, which used the excess at about 35 bar;
RQ1 tests the maximum-excess form. Kabbour et al. state the rule for uptake
expressed as mg of H₂ per g of sorbent, which is W1 (§3), so RQ1 uses W1. They
attribute the rule to Chahine and Bose (1996, 11th World Hydrogen Energy
Conference) and Chahine and Bénard (1998, Adv. Cryog. Eng. 43, 1257,
doi:10.1007/978-1-4757-9047-4_157).

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

## 5. Information sources and search

- **Databases.** OpenAlex (primary) and Semantic Scholar (secondary). Both are
  public, so any reader can re-run the search without a subscription.
- **Fields and limits.** Title and abstract. No document-type filter is applied
  at the API; types are screened by §4 codes. No year limit; the search runs
  through its execution date.
- **Search expression:** `H AND C`, where:
  - **H** = "hydrogen storage" OR "hydrogen adsorption" OR "hydrogen uptake" OR
    "hydrogen sorption" OR "hydrogen physisorption" OR "hydrogen spillover" OR
    "hydrogen capacity" OR "adsorption of hydrogen" OR "storage of hydrogen" OR
    "uptake of hydrogen" OR "sorption of hydrogen" OR "H2 storage" OR
    "H2 adsorption" OR "H2 uptake" OR "H2 sorption" OR "H2 physisorption" OR
    cryoadsorption OR "cryo-adsorption"
  - **C** = "activated carbon" OR "porous carbon" OR "microporous carbon" OR
    "nanoporous carbon" OR "mesoporous carbon" OR "templated carbon" OR
    "carbide-derived carbon" OR "carbon aerogel" OR "carbon cryogel" OR
    "carbon xerogel" OR "carbon nanotube" OR "carbon nanofiber" OR
    "carbon nanofibre" OR "carbon nanohorn" OR graphene OR
    "carbon molecular sieve" OR "doped carbon" OR "carbon fiber" OR
    "carbon fibre" OR "carbon foam" OR "carbon sphere" OR "carbon material" OR
    "carbon-based" OR carbonaceous OR "carbon nanostructure" OR nanocarbon OR
    "carbon monolith" OR biocarbon OR biochar OR "superactivated carbon" OR
    graphite OR graphitic OR fullerene OR "carbon black" OR CNT OR SWCNT OR
    MWCNT OR SWNT OR MWNT OR ZTC
- **Implementation.**
  - OpenAlex limits the number of boolean operators per query. The expression is
    therefore run as sub-queries, each pairing one group of at most five H terms
    with one C term. Their union equals the full expression, and results are
    merged by OpenAlex ID.
  - Semantic Scholar is queried for the full expression with its bulk-search
    boolean syntax.
  - The search log records singular and plural counts for three terms to
    confirm stemming. Where a source does not stem, plural forms are added
    explicitly.
- **Execution.**
  - The search runs from committed scripts in `scripts/v1_search/`. It uses
    direct HTTPS requests from a browser on the author's computer, with no
    content-transforming proxy.
  - Every response body is saved unmodified as text, with its request URL,
    retrieval timestamp and SHA-256, in `references/v1_search/`.
  - No LLM-mediated fetch tool is used to obtain search results, abstracts or
    metadata. An agent may start the scripts, but every response body is written
    to disk by the script itself and never passes through a model.
- **Merging** (`scripts/v1_search/merge_search.py`). Records are merged on
  normalized DOI, then on normalized title with publication years differing by
  at most 1.
- **Recall check.**
  - *Reference set A* is the 44 v0.1 papers in Appendix B. Recall is the
    fraction of set A present in the merged set, reported with the reason for
    each miss: not indexed; indexed without abstract; or indexed with abstract
    but not matched.
  - If recall is below 90%, terms are added once, in a dated amendment.
  - Recall is then reported on *reference set B*, which is not used to choose
    terms. Set B is the primary experimental carbon-sorbent H₂ papers among the
    OpenAlex `referenced_works` of Gunther et al. (2026, Int. J. Hydrogen
    Energy 253, 156054), identified by the §6 procedure before the search is
    run.

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

## 7. Sampling

- **Strata.**
  - *S1:* the title or abstract mentions 77 K or liquid nitrogen AND either a
    pressure ≥ 20 bar (≥ 2 MPa) or the words high pressure, saturation or
    excess maximum.
  - *S2:* every other record in the frame, including records without an
    abstract.
- **Frame IDs.** Each merged record gets `frame_id` = "F" + the zero-padded rank
  of its sort key. The sort key is the normalized DOI if present, else the
  OpenAlex ID, else the Semantic Scholar paper ID.
- **Randomization.**
  - The frame file, `references/v1_search/frame.csv` (every record that enters
    the frame, with its `frame_id` and stratum), is written by the committed
    script `scripts/v1_search/build_frame.py` from the archived search responses
    and screening outputs. The script is committed before the first record is
    screened, and re-running it must reproduce the frame file byte for byte; a
    frame file it does not reproduce invalidates the draw. The frame file and its
    SHA-256 are committed before the permutation is computed.
  - Let s = the integer value of the first 16 hex digits of that SHA-256. The
    order within stratum h (h = 1 for S1, 2 for S2) is
    `numpy.random.default_rng([s, h]).permutation(N_h)`, applied to that
    stratum's records sorted by `frame_id`.
  - The NumPy version is pinned (§11.0). The resulting orders are committed
    before any full text is retrieved.
- **Targets.** 60 eligible papers from S1 and 40 from S2.
- **Procedure.**
  - Records are taken in permuted order. Each is retrieved (§8) and checked
    against §4 on the full text.
  - Eligible papers enter the sample. Ineligible ones are recorded with their
    reason.
  - A record not obtained by the §8 routes is recorded as `not_retrieved` and
    skipped.
  - A drawn record that duplicates an earlier drawn record is recorded as
    `frame_duplicate` and skipped.
  - The walk stops when the target is reached, when the stratum is exhausted, or
    after 110 full-text assessments in S1 or 80 in S2.
  - The result is a simple random sample of the retrievable eligible papers in
    each stratum.
- **Design weights.** Let d_h be the number of records taken in stratum h
  (assessed, `not_retrieved` and `frame_duplicate` together), and n_h the number
  of eligible papers among them. The number of eligible, retrievable papers in
  stratum h is estimated as N̂_h = N_h × n_h / d_h, and each sampled paper
  carries weight N̂_h / n_h = N_h / d_h.
- **Analysis sets.**
  - RQ1, RQ2, RQ4 and RQ5 use the probability sample, including v0.1 papers
    drawn by the procedure, as the primary set.
  - RQ1, RQ2 and RQ5 are repeated on all §4-eligible papers as a pre-specified
    secondary analysis.
  - RQ3 uses all §4-eligible papers, because its unit is the material, not a
    sample of the literature.
- **v0.1 papers.**
  - All 51 remain in the release.
  - Each is assessed against §4 on the full text by the §6 procedure.
  - A v0.1 paper drawn by the procedure and found eligible carries its stratum
    as `selection_route`.
  - Undrawn eligible v0.1 papers are `legacy_v0.1`. Every ineligible v0.1
    paper, drawn or not, is `legacy_v0.1_ineligible` and enters no analysis.

## 8. Full-text retrieval

- **Routes.** For every drawn record, retrieval is attempted in this order
  before any full text is read:
  - (1) an open-access PDF at the record's OpenAlex `best_oa_location` or
    `open_access.oa_url`;
  - (2) the DOI landing page through the author's university library
    subscriptions.

  Each route is tried once when the record is reached, and the outcome is
  logged. No other source is used. A v0.1 paper is retrieved by the same routes;
  a PDF held from v0.1 is used only if one of the routes also yields it.
- **Supplementary information** is retrieved by the same routes and is part of
  the full text for eligibility and extraction.
- **Not retrieved.** A record not obtained by these routes is `not_retrieved`.
  Interlibrary loan and requests to authors are not used for any record, so that
  retrieval effort is the same for every record. Retrieved and not-retrieved
  records are compared on year, publisher, open-access status and stratum, and
  the comparison is reported.
- **Redistribution.** PDFs are not redistributed.

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

## 10. Quality coding

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

### 10.2 Plausibility screen

The screen is a flag, separate from the score. It applies to isothermal rows
only, not to `temperature_cycle`, `TPD` or `flow` rows.

- **Excess, absolute and unknown-basis rows** are flagged when:
  - at 77 K, uptake > 2 × (A_BET/500) + 0.5 wt%, using A_BET under the §11.0
    area rule, or uptake > 10 wt%; or
  - at 273–303 K and ≤ 100 bar, uptake > 1.5 wt%.
- **Total-basis rows** are flagged when they exceed the same bound plus
  100·ρ_H₂(T, P)·V_total. ρ is in g cm⁻³, from CoolProp for normal hydrogen
  (Leachman et al. 2009), and V_total is in cm³ g⁻¹. Total-basis rows without
  V_total are not screened.
- A row is screenable when at least one bound above can be evaluated for it.
  At 77 K the 10 wt% cap always can, and the area bound needs an A_BET under the
  §11.0 rule. At 273–303 K the row must be at ≤ 100 bar. A total-basis row also
  needs V_total. All other rows are counted as not screenable.

## 11. Analysis plan

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

### RQ1

- **Data (primary set).** One n_ex,max per sample (§11.0) from the probability
  sample (§7), meeting all of these:
  - 77 K (§3);
  - `measurement_mode = isothermal`;
  - `uptake_bound` ∈ {exact, approximate};
  - `basis_inferred = excess` (§3), with `basis_shape_conflict = false`;
  - `value_kind = measured`;
  - `nmax_status` ∈ {observed_max, plateau};
  - an eligible BET area (§11.0) with A_BET ≥ 300 m² g⁻¹.
- **Effect.** y = ln[n_ex,max / (A_BET/500)], with uptake in W1 wt%.
- **Model.**
  - Linear mixed model on y with random intercepts for laboratory (§3), paper
    within laboratory, and sample within paper (the residual).
  - Fitted by REML and unweighted, because no per-value sampling variances are
    available. If the laboratory variance is estimated at zero, the model is
    refitted without it and this is reported.
  - exp(μ) is the geometric-mean ratio. Its 95% CI is t-based on L − 1 degrees
    of freedom, where L is the number of laboratories.
  - A laboratory-cluster bootstrap (2,000 resamples, seed 20261030) is also
    reported, and the decision below uses the wider of the two intervals.
  - The 95% prediction interval is for a new sample from a new laboratory and
    includes all three variance components.
  - Software: statsmodels MixedLM with variance components.
- **Interpretation.** The margin is ±15%, symmetric on the log scale:
  [1/1.15, 1.15] = [0.870, 1.150]. The 95% CI is equivalent to two one-sided
  tests at α = 0.025.
  - *supported* if the CI lies within [0.870, 1.150];
  - *overstates* if the upper limit is below 0.870;
  - *understates* if the lower limit is above 1.150;
  - *inconclusive* otherwise.

  "Supported" refers to the average ratio. The rule is described as accurate for
  individual materials only if the 95% prediction interval also lies within
  [0.870, 1.150]. The prediction interval is reported next to the pooled ratio
  wherever the ratio appears.
- **Secondary.** ln n_ex,max = a + b·ln A_BET with the RQ1 random effects. b is
  reported with its 95% CI and with a reliability correction b/λ, where
  λ = 1 − σ_u²/s²(ln A_BET), for σ_u = ln(1.10) and ln(1.20) (BET
  reproducibility of 10% and 20%). b = 1 is judged on the corrected estimates.
- **Moderators** (exploratory). Each is added alone to the primary model, then
  all together on the complete-case subset:
  - measurement method;
  - material class (classes with fewer than 5 papers merged into other);
  - micropore fraction V_micro/V_total, both from the N₂ isotherm;
  - publication year (linear, centred at 2010);
  - `basis_stated`;
  - wt% convention known (stated, inferred or computed) against unknown;
  - stratum (S1/S2);
  - `reporting_score`.

  Results are reported with 95% CIs, and no moderator result is presented as
  confirmatory.
- **Sensitivity analyses:**
  - (i) stated excess only (`basis_stated = true`);
  - (ii) adding stated-excess lower-bound values;
  - (iii) all §4-eligible papers, including v0.1 papers not drawn;
  - (iv) without §10.2-flagged rows;
  - (v) A_BET ≥ 500 m² g⁻¹;
  - (vi) all A_BET > 0;
  - (vii) every unknown-convention wt% treated as W2 and converted;
  - (viii) `reporting_tier` A or B only;
  - (ix) excluding class composite and any sample with `metal_element` set or a
    non-carbon sorbent phase;
  - (x) adding `value_kind = fitted_interpolated`;
  - (xi) leave-one-laboratory-out (range of estimates);
  - (xii) design-weighted, with paper weights from §7;
  - (xiii) the v0.1 specification for continuity: `hycan.meta.chahine_mixedlm`
    on `hycan.meta.chahine_subset` exactly as at commit 45c669a, applied to all
    rows of the probability-sample papers.
- **Robustness rule.** The RQ1 conclusion is the primary analysis's category. If
  (i), (ii) or (iii) gives a different category, the abstract and conclusions
  state both and say that the conclusion depends on that choice. If fewer than
  20 papers contribute to the primary set, (iii) becomes the primary analysis
  and the switch is reported.
- **Descriptive.** The distribution of `p_at_nmax_bar` is reported, with values
  outside 10–60 bar listed.

### RQ2

- **Data.** 77 K (§3), 0.9–1.2 bar, isothermal, `basis_inferred` excess,
  absolute or unknown. Area by the §11.0 rule, with A_BET ≥ 300 m² g⁻¹.
- **Models** (random effects as in RQ1):
  - (a) ln n = a + b·ln A_BET + c·ln(P/1 bar), reporting b with its 95% CI;
  - (b) the same with ln V_micro in place of ln A_BET, fitted separately for
    N₂-derived V_micro (DR, DFT, NLDFT, QSDFT or t-plot) and for CO₂-derived
    V_micro at 273 K, never mixing the two;
  - (c) the RQ1 ratio model, reported as the 1-bar ratio to A_BET/500.
- BET and V_micro predictors are compared on the subset of samples that have
  both.

### RQ3

- **Materials.** Identical supplier, product name and grade, measured by two or
  more laboratories.
- **Data.** n_ex,max as in RQ1 (`basis_inferred = excess`,
  `basis_shape_conflict = false`, `nmax_status` ∈ {observed_max, plateau});
  n at 1 bar as in RQ2.
- **Per material.** The number of laboratories, and the between-laboratory SD on
  the log scale (as CV ≈ 100·SD, with χ²-based 95% CIs) of:
  - A_BET;
  - n_ex,max;
  - n at 1 bar (the RQ2 window);
  - n_ex,max/A_BET.
- **Headline.** The pooled between-laboratory SD of each quantity from a model
  with material fixed effects and laboratory random effects, with its 95% CI.

### RQ4

- **Data.** The probability sample only.
- **Items** (paper level):
  - (a) basis stated for every uptake value;
  - (b) wt% convention explicitly stated (inference does not count);
  - (c) a numerical uncertainty or replicate for at least one H₂ value;
  - (d) §10.1 item 7 met for at least one H₂ measurement;
  - (e) BET P/P₀ range or consistency criteria stated;
  - (f) sample mass for the H₂ measurement stated;
  - (g) degassing conditions stated;
  - (h) at least one row flagged by §10.2, among papers with at least one
    screenable row;
  - (i) H₂ purity stated;
  - (j) free-volume calibration gas and temperature stated, among papers with
    volumetric data.
- **Population.** §4-eligible, retrievable papers among the records matched by
  §5.
- **Estimator.**
  - Stratified ratio estimator, with weight N_h/d_h, where d_h is the number of
    records taken in stratum h (§7). Eligible, retrieved papers form a domain;
    `not_retrieved` and `frame_duplicate` records lie outside it.
  - Variance by Taylor linearization with finite-population correction.
  - 95% CIs by the Korn–Graubard method.
  - Also reported by publication period (≤ 2015 and ≥ 2016) as a descriptive
    contrast.
- **Precision.** The expected half-width is about ±15 percentage points; RQ4 is
  descriptive.

### RQ5

- **Target.** 77 K isothermal rows with:
  - `basis_inferred = excess`, from an isotherm with
    `basis_shape_conflict = false`;
  - `uptake_bound` ∈ {exact, approximate};
  - P ≤ 100 bar;
  - area by the §11.0 rule.

  All models are trained and scored on the same rows.
- **Models:**
  - (a) physical baseline n = k·A_BET·P/(P + p₀), with k and p₀ fitted;
  - (b) linear model in A_BET, ln P and A_BET·ln P;
  - (c) gradient-boosted trees (XGBoost).
- **Features for (c):**
  - ln A_BET, ln P and P;
  - material class (one-hot; classes with fewer than 5 papers merged into
    other);
  - measurement method;
  - total and micropore volume (missing left missing);
  - dopant and metal presence (binary);
  - publication year.

  No feature is derived from uptake.
- **Hyperparameters for (c).** Fixed, with no tuning: n_estimators = 500,
  learning_rate = 0.05, max_depth = 4, others default.
- **Validation.**
  - GroupKFold(n_splits = 5, shuffle = True, random_state = r) for r = 0…19,
    grouped by paper; scikit-learn ≥ 1.6. Sensitivity: grouped by laboratory.
  - Per partition: pooled out-of-fold R² and MAE.
  - Reported: the mean and the 2.5–97.5 percentiles across partitions, and a
    paper-level bootstrap 95% CI (2,000 resamples, seed 20261032) on
    partition r = 0. Each is given overall and within the ≤ 1.2 bar and
    ≥ 10 bar regimes.
  - Sensitivity: rows weighted by 1/(rows in their paper).

## 12. Human audit of extraction

- **Sample.** After reconciliation, 60 rows are drawn in three audit strata
  with `numpy.random.default_rng(20261029)`:
  - (a) 30 rows from the RQ1 primary set, each the row at `p_at_nmax_bar` of an
    isotherm that contributes to it;
  - (b) 15 other rows from papers extracted by agents A and B (§9);
  - (c) 15 rows from papers extracted by agent B alone (§9).

  In (a), 15 rows are drawn from rows on which A and B agreed on every field
  before reconciliation and 15 from rows C resolved; in (b), 8 and 7. If a cell
  holds fewer rows than its quota, all are taken and the shortfall is drawn from
  the other cell of the same audit stratum. Rows are drawn without replacement
  with that generator's `choice`, cell by cell in the order listed (agreed
  before resolved), each cell sorted by `measurement_id`. The further sample
  (follow-up below) continues the same generator and excludes rows already
  audited.
- **Procedure.**
  - The audit sheet shows the paper, sample label, source location and field
    names only.
  - The author records each field from the PDF, and code compares.
  - Fields audited: uptake value and unit; T; P; A_BET with method and probe
    gas; `basis_stated`; `basis_inferred`; `wt_pct_convention`; `value_kind`;
    sample identity; and, for figure rows, the digitized point.
- **Error.** A numeric difference larger than the printed rounding (table or
  text) or 3% relative (figures), or any categorical difference.
- **Reported.** Errors per field and per audit stratum, with exact
  (Clopper–Pearson) 95% CIs, and an overall rate weighted by the number of rows
  each audit stratum and cell represents.
- **Follow-up.**
  - If audit stratum (a) has any error, its cause is classified, and agent C
    re-checks every row exposed to that cause.
  - A further 30 rows of audit stratum (a), split 15 and 15 as in the first
    sample, are then audited. Both samples are reported separately and pooled.
  - If the pooled error rate in audit stratum (a) exceeds 5%, the author checks
    every RQ1 primary-set value before analysis.

## 13. AI use

- **Roles.** Every agent role is performed by Anthropic Claude models directed
  by the author: search execution, screening, eligibility, extraction,
  reconciliation, code, analysis, figures, and drafting or editing of the
  manuscript.
- **Logging.** The model, version, frozen prompt hash and run dates for each role
  are logged, and summarized in a Methods table.
- **Declaration.** The manuscript carries Elsevier's Declaration of generative AI
  and AI-assisted technologies.
- **Human work.** The author performs the screening audit (§6) and the
  extraction audit (§12) without AI assistance, and is responsible for all
  content.

## 14. Reporting

- **Reporting bias.** Small-study and publication-bias tests are not performed,
  because per-value sampling variances are unavailable. S1 against S2 and RQ1
  sensitivity (iii) are reported as the available checks on selection.
- **PRISMA 2020.** A flow diagram and checklist (Page et al. 2021), with stages:
  identified per source; merged; screened; frame (per stratum); drawn;
  retrieved; assessed; eligible; analysed (per RQ).
- **Generated outputs.** Every count-bearing document and table is generated by
  committed code.
- **Data availability.** Released under CC BY 4.0 (data) and MIT (code) with a
  Zenodo DOI: rows, data dictionary, screening decisions, the frame, raw API
  responses, all agent outputs, audit sheets and code. PDFs are not released.
- **Deviations.** The manuscript includes a table of every amendment and
  deviation, with its date, its reason, and whether the relevant data had been
  seen.

## 15. Amendments

None yet. Each amendment is dated and appended here, and states which data, if
any, had been seen when it was made. Any analysis not specified in §11 is
reported as exploratory.

---

## Appendix A. Fields added in schema v2

Fields marked *computed* are produced by code (`src/hycan/v1.py`) from extracted
fields. They appear in the processed release, not in the extraction schema, and
are never entered by an extractor. Where `src/hycan/v1.py` and this protocol
differ, the protocol governs and the code is corrected. `src/hycan/v1.py` and its
tests against the §3 and §10.1 rules are committed before the first full text is
extracted.

| Field | Values |
|---|---|
| `basis_stated` | true / false (§3 rule) |
| `basis_inferred` | excess / absolute / total / unknown |
| `basis_evidence` | quoted text |
| `basis_shape_conflict` | true / false (*computed*, §3) |
| `wt_pct_convention` | W1 / W2 / unknown |
| `wt_pct_convention_source` | stated / inferred_from_paired_units / computed_from_other_unit / none |
| `value_kind` | measured / fitted_interpolated / fitted_extrapolated / unclear |
| `isotherm_id` | identifier shared by all points of one isotherm |
| `isotherm_branch` | adsorption / desorption / not_applicable |
| `nmax_status` | observed_max / plateau / lower_bound / none (*computed*, §3) |
| `p_at_nmax_bar`, `p_last_bar` | number (*computed*) |
| `temperature_inferred` | true / false |
| `surface_area_probe_gas` | N2 / Ar / CO2 / other / unspecified |
| `bet_range_stated`, `bet_consistency_criteria_stated` | true / false |
| `area_same_sample` | yes / parent_material / other_paper / unclear |
| `degas_temperature_c`, `degas_duration_h` | number |
| `degas_end_pressure_pa` | number |
| `sample_mass_mg` | number |
| `h2_purity_pct` | number |
| `free_volume_calibration` | text (gas and temperature) |
| `instrument_identified`, `calibration_described`, `replicates_reported` | true / false |
| `isotherm_point_count` | integer |
| `measuring_lab_id` | string (§3 Laboratory) |
| `material_identity` | supplier + product + grade, else empty |
| `duplicate_of` | measurement_id of the earlier report, else empty |
| `data_location` | main_text / SI |
| `digitization_uncertainty_wt_pct` | number |
| `selection_route` | S1 / S2 / legacy_v0.1 / legacy_v0.1_ineligible |
| `frame_id` | §7 |
| `reporting_score`, `reporting_tier` | §10.1 (*computed*) |

Also in schema v2:
- The upper bound of `bet_surface_area_m2_g` is raised from 4000 to
  5000 m² g⁻¹.
- `reproducibility_tier` becomes optional and legacy; it is used by no v1.0
  analysis.
- `activation_method` keeps its v0.1 meaning (synthesis activation) and is not
  used by §10.1.

## Appendix B. Reference set A

The v0.1 papers whose recorded fields show a surface area (§4 to be confirmed
on the full text):

HYC-0001, 0004, 0005, 0007, 0009, 0012, 0013, 0016, 0017, 0018, 0019, 0020,
0021, 0022, 0023, 0024, 0026, 0029, 0031, 0032, 0033, 0034, 0037, 0040, 0041,
0042, 0043, 0044, 0045, 0046, 0047, 0048, 0049, 0050, 0052, 0053, 0057, 0058,
0060, 0061, 0062, 0063, 0064, 0065.
