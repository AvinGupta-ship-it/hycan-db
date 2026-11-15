# v1.0 human audit of extraction (protocol §12; deviation D1)

This directory holds the §12 audit sample and, once the author has audited
it, his verdicts and the scored result.

## Deviation D1 — verification format (2026-11-15)

§12 registers a blind audit: the sheet shows "the paper, sample label, source
location and field names only", the author re-enters each value from the PDF,
and code compares. Before entering any value, the author chose a
verification format instead: the audit page shows each extracted value and
he marks it, field by field, as matching the PDF (within the §12 tolerance:
printed rounding, or 3% relative for a value read off a figure) or as wrong,
typing what the PDF shows when wrong. The grounds were burden: re-typing
roughly 700 values duplicates transcription work without, in his judgment,
adding enough over directed verification. The audited fields, the 60-row
sample (`draw.csv`, drawn blind, unchanged), the error rule, the estimator
and the §12 follow-up rules are unchanged.

This is a deviation from the registered design, decided by the author on
2026-11-15 before any audit entry existed, and it is disclosed wherever the
audit is reported. Its cost is independence: seeing the extracted value
before reading the PDF invites confirmation of near-misses that a blind
re-reading would catch, so the audit now bounds the rate of errors the
author can detect when told what to look for, which is weaker evidence than
the registered blind re-extraction. The blinded sheet (`sheet.csv`) is kept
as drawn and was never filled.

## Files

| File | Content |
|---|---|
| `draw.csv` | The 60 drawn rows: audit stratum (a/b/c), cell (agreed/resolved/all), draw order, paper and `measurement_id`. Drawn by `scripts/v1_search/audit.py draw` with `numpy.random.default_rng(20261029)`, cell by cell in the §12 order, each cell sorted by `measurement_id`. |
| `cells.json` | Every cell's pool size and settled quota (the §12 reporting weights), and the RQ1 primary-set counts behind audit stratum (a). |
| `sheet.csv` | The registered blinded sheet, kept as drawn; never filled (deviation D1). |
| `verdicts.csv` | The author's verdicts, one line per row and audited field: `matches` or `wrong`, with the PDF's value when wrong. Exported verbatim from the audit page's store. |
| `score.json` | The scored audit (`scripts/v1_search/audit.py score`). |

## The draw

Audit stratum (a) holds the rows at `p_at_nmax_bar` of the 94 isotherms that
contribute to the RQ1 primary set (29 papers). Its *agreed* cell holds 14
rows, one short of the §12 quota of 15, so per §12 all 14 are taken and the
shortfall moves to the *resolved* cell (16 drawn). Audit strata (b) and (c)
are at full quota: 8 + 7 of the other dual-paper rows, and 15 legacy-paper
rows.

A row is *agreed* when its §9 match line has status `agree` and no resolution
of C's names that line or the row's `measurement_id`; every other row is
*resolved* (`scripts/v1_search/audit.py`, module docstring, has the exact
rule and the RQ1-contribution rule).

## Procedure (the author, without AI assistance — §13)

The audit runs on a page that shows the 60 rows grouped by paper, each row's
audited fields with their extracted values. For every field the author opens
the paper at `source_location` and marks the value `matches` (within its
printed rounding; within 3% for a value read off a figure) or `wrong`,
entering the PDF's value when wrong. An empty value claims the paper does
not report that field; the author confirms or refutes that the same way. The
audited fields are the §12 list: the uptake value with its unit (one field),
T, P, A_BET with its method and probe gas, `basis_stated`,
`basis_inferred`, `wt_pct_convention`, `value_kind`, the sample identity,
and, on figure rows, the digitized point (the author reads the named point
off the figure and compares both its pressure and its value). For a figure
row, "which point" names the plotted point ("k of n, by increasing
pressure", counting the dataset's digitized points of that isotherm); a row
of audit stratum (a) is its isotherm's maximum-uptake point.

An error is a field marked `wrong` (§12's error rule, applied by the author
at the moment of marking). `scripts/v1_search/audit.py score` reports errors
per field and per audit stratum with exact (Clopper–Pearson) 95% CIs, and
overall weighted by the rows each cell represents. §12's follow-up rule then
applies: any error in audit stratum (a) is classified, C re-checks every row
exposed to its cause, and a further 30 rows of (a) are audited; a pooled (a)
error rate above 5% sends the author through every RQ1 primary-set value
before analysis.
