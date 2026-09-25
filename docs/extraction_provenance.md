# Extraction Provenance

**What this document is for.** HyCAN-DB is a public dataset, and a public
dataset that does not say how it was built is an assertion rather than
evidence. This file states which rows were produced by which process, what
that process does and does not guarantee, what is known to go wrong with it,
and what you should check yourself before relying on any number here.

It is written to be read by someone who has no connection to this project and
no reason to trust it.

Last updated 2026-09-24, against dataset `data/raw/measurements_v0.1.csv`
(119 rows, 11 papers, sha256 `55875a906d565df37d3bae32e304fbb39b7d02c1d52b7a17c27df9f187f156d5`).

---

## 1. Summary, stated plainly

**Every row currently in the dataset was extracted by a human reading the
paper.** No row in this release was produced by the AI dual-agent pipeline,
and no row has been through independent second-reader verification of any
kind. The `verified_by` and `verification_date` columns are empty on all 119
rows. Treat the dataset as single-reader extraction.

The AI pipeline described in §3 below is built and tested but has not yet been
run against any paper. When it is, the rows it produces will be distinguishable
by their `extractor` value and this section will be rewritten with measured
numbers rather than an absence.

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

Totals: 87 `table_direct`, 17 `text_direct`, 15 `figure_digitized`. Tiers: 36
A, 75 B, 5 C, 3 D.

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
