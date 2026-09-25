# Extraction Provenance

**What this document is for.** HyCAN-DB is a public dataset, and a public
dataset that does not say how it was built is an assertion rather than
evidence. This file states which rows were produced by which process, what
that process does and does not guarantee, what is known to go wrong with it,
and what you should check yourself before relying on any number here.

It is written to be read by someone who has no connection to this project and
no reason to trust it.

Last updated 2026-09-25, against dataset `data/raw/measurements_v0.1.csv`
(206 rows, 21 papers, sha256 `3ecc8b63d9a17ad6980602bc03c4da2150f0b3a4cbcb6335d7ed3ab5d1701676`).

---

## 1. Summary, stated plainly

**The dataset is now mixed, and the two halves are not equally verified.**

121 of the 206 rows (11 papers) were extracted by a human reading the paper,
with no independent second reader of any kind. `verified_by` and
`verification_date` are empty on all of them. Treat those rows as single-reader
extraction.

85 rows (10 papers) were produced by the AI dual-agent pipeline described in §3
and carry `extractor = "HyCAN pipeline v2"`, with `verified_by` recording the
verification outcome. Every numeric and controlled-vocabulary cell in those rows
was extracted by one agent and then independently re-derived, from the PDF, by a
second agent that had the paper and the candidate values only — no access to the
first agent's reasoning, search keys, notes, or uncertainty flags.

**Measured dispute rate: 31 cells disputed in 704 verified, 4.4% raised and
3.3% upheld.**

| Paper | Cells | Agreed | Disputed, upheld | Disputed, dismissed |
| --- | --- | --- | --- | --- |
| HYC-0025 | 42 | 42 | 0 | 0 |
| HYC-0012 | 64 | 64 | 0 | 0 |
| HYC-0017 | 26 | 26 | 0 | 0 |
| HYC-0019 | 78 | 78 | 0 | 0 |
| HYC-0022 | 98 | 94 | **4** | 0 |
| HYC-0009 | 65 | 65 | 0 | 0 |
| HYC-0029 | 145 | 144 | **1** | 0 |
| HYC-0026 | 102 | 86 | **16** | 0 |
| HYC-0011 | 43 | 41 | **2** | 0 |
| HYC-0015 | 41 | 33 | 0 | **8** |
| **Total** | **704** | **673** | **23** | **8** |

**What the verifier caught, paper by paper.** In every upheld case the verifier
was right and the extractor was wrong, and in every case the error was one a
single reader would plausibly have written into the dataset:

- **HYC-0022, 4 cells.** `synthesis_method` was `commercial` on all six samples
  because the carbon skeleton was purchased. The verifier rejected that for the
  four the authors activated themselves, citing the paper's own "Both physical
  and chemical activations were performed in our study" and the carbon yields —
  62%, 49%, 53%, 43% — that its Table 1 reports for exactly those four and no
  other. A sample with a burn-off yield was not bought in that state.
- **HYC-0029, 1 cell.** The 873 K sample was coded `measurement_method =
  not_applicable`. The verifier pointed out the measurement *was* made — Fig. 9
  plots it, and the paper states a trend across activation temperature that
  requires all three — and only the number is unreported. `not_applicable`
  asserts no measurement exists and would have foreclosed digitising Fig. 9.
- **HYC-0026, 16 cells, the largest dispute so far.** Three separate errors.
  `pressure_bar = 40` was inferred, and the verifier established that every
  "4 MPa" in the paper that functions as a reporting pressure belongs to its
  *excess* isotherms, measured on a different instrument, while the recorded
  values are the *adsorbed* quantity — so the pressure is genuinely unstated.
  `average_pore_diameter_nm` held the paper's L0, which §2.2.2 defines as the
  average *micropore* diameter, on samples with 0.19–0.59 cm³/g of mesopore
  volume. And a `dopant_concentration_wt_pct` had been recorded on three samples
  that were never doped — that figure is the anthracite precursor's native
  nitrogen.
- **HYC-0011, 2 cells.** `measurement_method = other` understated a measurement
  that has every defining element of a manometric one (a calibrated 49.30 mL
  cell, quantity inferred from pressure decay, empty-cell blank runs), and its
  third powder measurement was coded `isothermal` when its value comes from the
  non-closure of a 295 → 353 → 295 K ramp.

**The eight dismissed disputes are worth recording too, because the verifier was
reading the wrong authority.** On HYC-0015 it reported that
`temperature_unstated`, `measurement_mode` and `uptake_bound` "are not columns"
and that a null temperature on an uptake row is an error. All three are columns,
at physical positions 42, 44 and 41, and the null is exactly what schema v1.2
gap 2 permits. The verifier had read `HyCANDB_Execution_Manual_v2.2.md`, which
still documents a 40-column v1.1 schema, rather than `src/hycan/schema.py`. Two
other verifiers checked the code and reported the same staleness as a finding.
**The manual is the defect here, not the rows, and it is now the oldest
outstanding item in this project.** Every substantive finding in that report was
adopted, including its argument that the paper's 1.90 wt% at 80 bar and nominal
room temperature warrants Tier D on the physics override.

Read the rate with care. 704 cells across ten papers is a real sample now, and
3.3% upheld is a more honest number than the 0% the first three papers
suggested — but it is not an error rate for the corpus, because it measures
disagreement between two readers of the same paper, not correctness. Four of the
five papers in the second batch produced an upheld dispute; the first three
produced none. The difference is that the second batch's papers are messier and
the questions harder, not that the protocol changed.

Free-text cells in v2 rows (`material_description`, `purification_method`,
`functional_groups`, `notes`, `source_location`) were written by the
adjudicating agent from the source text and are **not** part of the verified
cell count. The verification protocol covers numeric values and controlled
vocabularies.

The v2 rows also carry substantially longer `notes` than the v1.0 rows, because
the verification pass surfaces internal contradictions, traps and unstated
conditions that the protocol requires be recorded rather than resolved
silently. A v1.0 row with a short note is not better evidenced than a v2 row
with a long one; the reverse is closer to true.

---

## 2. Row-level provenance

| Paper | Rows | Protocol | `extractor` as recorded | Second reader | Extraction methods |
| --- | --- | --- | --- | --- | --- |
| HYC-0001 | 4 | v1.0 human | `AG` | none | text_direct, figure_digitized |
| HYC-0002 | 3 | v1.0 human | `AG` | none | table_direct |
| HYC-0004 | 21 | v1.0 human | `AG` | none | table_direct |
| HYC-0005 | 25 | v1.0 human | `AG` | none | table_direct |
| HYC-0013 | 7 | v1.0 human | `Avin Gupta` | none | table_direct |
| HYC-0016 | 14 | v1.0 human | `Avin Gupta` | none | text_direct, figure_digitized |
| HYC-0018 | 4 | v1.0 human | `Avin Gupta` | none | table_direct, text_direct |
| HYC-0020 | 7 | v1.0 human | `AG` | none | text_direct |
| HYC-0021 | 6 | v1.0 human | `Avin Gupta` | none | table_direct |
| HYC-0023 | 23 | v1.0 human | `AG` | none | table_direct |
| HYC-0027 | 5 | v1.0 human | `Avin Gupta` | none | text_direct |
| HYC-0009 | 20 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 65/65 cells agreed** | table_direct |
| HYC-0011 | 4 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 41/43 agreed, 2 upheld** | text_direct |
| HYC-0012 | 6 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 64/64 cells agreed** | table_direct |
| HYC-0015 | 2 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 33/41 agreed, 8 dismissed** | text_direct |
| HYC-0017 | 3 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 26/26 cells agreed** | text_direct |
| HYC-0019 | 12 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 78/78 cells agreed** | table_direct |
| HYC-0022 | 9 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 94/98 agreed, 4 upheld** | table_direct, text_direct |
| HYC-0025 | 6 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 42/42 cells agreed** | table_direct |
| HYC-0026 | 7 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 86/102 agreed, 16 upheld** | table_direct, text_direct |
| HYC-0029 | 16 | **v2.0 dual-agent** | `HyCAN pipeline v2` | **yes, 144/145 agreed, 1 upheld** | table_direct, text_direct |

Totals: 151 `table_direct`, 39 `text_direct`, 15 `figure_digitized`. Tiers: 36
A, 124 B, 37 C, 8 D.

**Rows deliberately not written.** All twelve Phase C papers have been read and
schema v1.2 unblocked most of what was held. 105 rows were extracted; **85 are
in the dataset and 20 are held**, none dropped and not one held for lack of
evidence:

| Paper | Extracted | Written | Held because |
| --- | --- | --- | --- |
| HYC-0007 | 10 | 0 | reports a micropore and an external surface area per sample and no total; 18 measured values have no field (gap 3b) |
| HYC-0024 | 8 | 0 | its only tabulated hydrogen quantities are volumetric densities in kg/m3; its wt% values exist solely in a figure (gap 10) |
| HYC-0011 | 5 | 4 | the iron-phthalocyanine film has an areal uptake in g/cm2 and no wt%, no mass and no characterisation (gap 10) |
| HYC-0015 | 3 | 2 | pristine graphite has no uptake and no characterisation value any field can hold — only an XRD interlayer spacing |

Both remaining papers and both remaining rows are blocked on **stage 4** of
`docs/schema_v1_2_gaps.md` (gaps 3, 6 and 10), which is out of scope for v1.2
because it redefines what three existing columns mean.

**Seven rows in the dataset carry no uptake at all**, up from the two schema
v1.1 recovered. HYC-0029's 873 K activated sample and HYC-0026's four
nitrogen-doped samples are real materials whose uptake their papers plot without
ever printing a number; under §3.4 those values await programmatic digitisation
and each row says so.

**Three rows carry a bound rather than a measurement**, which schema v1.2 gap 1
made representable: HYC-0017's room-temperature result ("below 0.2 wt.%", its
headline negative result and the reason the paper was published) and HYC-0029's
two KOH-activated samples ("more than 1.0 wt.%"). All three are excluded from
isotherm fitting and from headline capacity statistics by the `uptake_bound`
flag.

**Twenty-two rows carry conditions their papers never stated numerically**, and
twenty-two carry a measurement that is not isothermal. Both are recorded with
flags rather than by imputing a convention: "room temperature" in a 2002 and a
2016 laboratory are not the same number, and HYC-0029's uptakes are weight
differences across a 303 → 673 → 303 K cycle whose reference state is a sample
at 673 K still sitting in hydrogen. Those sixteen HYC-0029 rows and HYC-0011's
third measurement must not enter a Chahine plot.

Three of these are worth stating plainly, because they are the kind of thing a
database loses quietly:

- **HYC-0017's 290 K bound** is that paper's headline *negative* result and the
  reason it was published. It is recorded in the `notes` of both written
  HYC-0017 rows rather than as a row of its own.
- **HYC-0024 yields no storable uptake at all.** Eight samples measured at 293 K
  and 100 bar, and not one value this schema can hold.
- **HYC-0011's 8.0 wt%** is arithmetically irreconcilable with its own areal
  uptake, film mass and film area, which imply 0.84-1.26 wt%. Recomputed
  independently by the adjudicator; the paper shows no intermediate working, so
  no cause is asserted. It belongs in the corpus at Tier D with the discrepancy
  quoted, per this project's disclosure-not-deletion principle. It is held on
  the temperature gap, not on that.

**A known blemish in this table.** The `extractor` field is spelled two ways —
`AG` on 83 rows and `Avin Gupta` on 36 — because the convention changed
mid-project and existing rows were not backfilled. Both denote the same person
and the same protocol. It is recorded here rather than silently normalised,
because a reader filtering on `extractor` will otherwise get a misleading
split.

### The 15 figure-digitized rows

`figure_digitized` rows carry values read from a plot, not from a table or a
sentence. In this release all 15 were produced under the v1.0 protocol using
WebPlotDigitizer, with the project files archived at
`data/digitizations/HYC-0016_fig3.json` and `HYC-0016_fig4.json`. Those
archives are the audit trail: they contain the calibration and the extracted
series, and the extraction can be reproduced from them.

Digitized values are inherently less certain than table values. They carry
reduced `extraction_confidence` for that reason. If your analysis is sensitive
to a few points, filter on `extraction_method` and check whether they are
doing the work.

`extraction_method = figure_estimated` exists in the schema for historical
compatibility and **is not assigned to any row.** A value eyeballed off a plot
is not admissible data in this project.

---

## 3. The dual-agent verification protocol

This is the process that will produce rows from the next paper onward. It is
described in enough detail to be implemented and criticised.

**Agent A (extractor)** receives the PDF. It produces candidate rows: every
sample, every characterization value, every uptake value with temperature,
pressure, units as reported, and the paper's own word for uptake type. For
each cell it records a `source_location`, and for every claim about method,
instrument, sample identity and uptake type it supplies the verbatim sentence
or table caption supporting it, plus a plain-ASCII search key for locating
that quote in the PDF text layer.

**Agent B (verifier)** receives the PDF and the candidate rows **only**. It
does not receive Agent A's reasoning, notes, uncertainty flags, search keys or
commentary. It independently re-derives every numeric cell, every
controlled-vocabulary assignment and every `source_location` from the PDF, then
reports agreement or disagreement cell by cell. Agent B is instructed that
finding a discrepancy is the purpose of the task, not a failure of it.

**Isolation is the entire mechanism.** An Agent B that can see Agent A's
reasoning is an editor, not a verifier, and will anchor on A's conclusions. Any
implementation that leaks A's output into B's context has disabled the
protocol while appearing to run it.

**Agent C (adjudicator)** receives the PDF and the disputed cells alone, with
neither prior reading attached, and produces its own value. Majority resolves.
If all three differ, or if C's reading suggests the paper itself is ambiguous,
the case goes to a human.

**Quote verification.** If any quoted sentence Agent A supplied cannot be
located in the PDF, Agent A's entire output for that paper is discarded and
the paper is re-extracted from scratch by a fresh agent. Not the offending
cell — the whole paper.

**Recording.** Each paper's log entry records cells verified, cells disputed,
and how each dispute resolved. A paper with zero disputes across thirty cells
is evidence the protocol is calibrated. A paper with many is a signal worth
investigating.

### Measured dispute rates

**None. No paper has been through this protocol yet.** There is no dispute
rate to report, and none is estimated or projected here. When Phase C runs,
this section will carry real counts.

---

## 4. Known failure modes

Stated without minimisation. Some are inherent to the approach; some were found
by adversarial audit of this project's own tooling and are fixed but worth
knowing about.

**Inherent to a language model reading a PDF.** Plausible, confident, wrong
output is the characteristic failure, and nothing internal to the model
reliably distinguishes it from correct output. The mitigations here — required
verbatim quotes, an isolated second reader, programmatic unit conversion, a
third-party DOI resolution step — reduce the rate but do not eliminate it.

**Sample-to-value mapping.** Papers reporting many samples invite
mis-association of an uptake value with the wrong sample. The mitigation is
extracting sample by sample rather than measurement by measurement. This is the
failure most likely to survive verification, because a plausible
mis-association reads as coherent to both readers.

**Excess versus absolute uptake.** The field's most confused distinction. These
values are assigned only when the paper uses that exact word for those values;
otherwise `unspecified`. 96 of 119 rows are `unspecified` — that is the honest
state of the literature, not an extraction gap. Do not assume a type where the
dataset declines to assign one.

**Figure digitization.** Values read from plots depend on calibration quality
and on whether the digitized series is actually the series it claims to be.
Audit of this project's own digitization tool found three ways it could archive
wrong numbers while reporting success: a legend sample in the series colour
winning the per-bin median (an 83% error, measured); a semi-transparent fill
under a curve halving every value, because alpha was discarded rather than
composited; and a logarithmic axis read as linear, which is exact at both
calibration reference points and wrong everywhere between (pressure errors of
13x to 398x, measured). All three are now refused or detected, and the tool
records its calibration, its search region and its verification checks in the
archive. They are listed because a reader should know what class of error is
possible here, and because the current digitized rows predate the tool.

**Internal contradiction.** Where a paper contradicts itself, the primary data
table wins and the discrepancy is recorded in the row's `notes`. This has
occurred four times in eleven papers. Read the `notes` column.

**Literature-summary tables.** Many papers tabulate other groups' results.
These are not extractable data. Captions are checked for this, and at least one
such table (HYC-0013 Table 1) was excluded on that basis.

**Tiering assumes physisorption.** The reproducibility rubric is calibrated for
physisorptive uptake on porous carbons. Applied to spillover and
metal-decorated systems it penalises papers for not reporting quantities their
mechanism does not depend on. HYC-0027 sits at Tier C with four of its five
lost points attributable to this rather than to any deficiency in its
reporting. The limitation is disclosed rather than corrected by inflating
scores; see `docs/reproducibility_tiering.md`.

**Digitization archives are not yet linked to rows.** The digitization tool
writes a `status` field (`unchecked` / `passed` / `discarded`), but no
validator and no part of the append pipeline reads it. A row carrying
`extraction_method = figure_digitized` can currently be appended without any
check that its archive passed verification. Closing this requires a schema
field and is scheduled with the next migration.

---

## 5. How the tooling itself was built

The extraction and validation code in `scripts/` and `src/hycan/` was written
with AI assistance, and the contemporaneous record is in
`docs/ai_usage_log.md`. Two facts about that record are worth stating here
because they bear on how much the tooling should be trusted:

The Phase A helper scripts were built in a cloud session, reviewed by four
isolated agents that had not seen the reasoning behind the code, and applied to
this repository as a git bundle rather than pushed directly. Those reviews
found thirteen defects in code that passed 239 tests, including one that could
leave the dataset unparseable with no rollback.

A mutation audit of the accompanying test suite found that 41 of the first 42
mutations survived — the tests were asserting that code paths ran, not what
they computed. The suite was rewritten and now fails against every mutation
used to demonstrate the problem. This is recorded because the first version
looked exactly as green as the second.

---

## 6. What to check before relying on this dataset

1. **Assume single-reader extraction.** Nothing here has been independently
   verified. If a number matters to your conclusion, open the paper.
2. **Read the `notes` column** on any row you use. Internal contradictions,
   inferred units and judgement calls are recorded there.
3. **Filter by `reproducibility_tier`** and report your analysis with and
   without Tier C and D rows. Tier D rows are historically contested claims,
   included deliberately with a flag rather than excluded.
4. **Check `uptake_type` before aggregating.** Do not pool `excess` with
   `unspecified` and treat the result as one quantity.
5. **Never aggregate across temperature regimes.** 77 K and 298 K uptake differ
   by roughly an order of magnitude at the same pressure.
6. **Treat `figure_digitized` rows as lower confidence** and check whether your
   result depends on them.
7. **Re-derive the unit conversions if they matter.** They are in
   `src/hycan/normalize.py` with tests; the STP molar volume convention is
   22.414 mL/mmol, which differs from other defensible conventions and would
   shift every volumetric value if changed.
8. **Check the row count and validation state** against what this document
   claims. `python3 scripts/validate_data.py` should report 119 rows, 0 errors.

If you find an error, please open an issue on the repository. A dataset that
gets corrected is more useful than one that is never checked.
