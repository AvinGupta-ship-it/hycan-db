# v1.0 human audit of extraction (protocol §12)

This directory holds the §12 audit sample and, once the author has audited it,
the filled sheet and the scored comparison.

## Files

| File | Content |
|---|---|
| `draw.csv` | The 60 drawn rows: audit stratum (a/b/c), cell (agreed/resolved/all), draw order, paper and `measurement_id`. Drawn by `scripts/v1_search/audit.py draw` with `numpy.random.default_rng(20261029)`, cell by cell in the §12 order, each cell sorted by `measurement_id`. |
| `cells.json` | Every cell's pool size and settled quota (the §12 reporting weights), and the RQ1 primary-set counts behind audit stratum (a). |
| `sheet.csv` | The audit sheet: the paper, sample label, source location, an identification aid, and one empty column per audited field. No extracted value of an audited field appears on it. |

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

For each row of `sheet.csv`, open the paper at `source_location` and record
each audited field from the PDF into the empty columns:

- `uptake_value` and `uptake_unit` — the value as printed (for a figure row,
  as read from the figure), and its unit as printed (`wt%`, `mmol/g`,
  `mL(STP)/g`, ...);
- `temperature_k`, `pressure_bar` — in K and bar (converted from the printed
  unit if needed);
- `a_bet_m2_g`, `a_bet_method`, `a_bet_probe_gas` — the sample's BET area as
  printed, the method name, and the probe gas (`N2`, `Ar`, `CO2`, `other`,
  `unspecified`);
- `basis_stated` — `true`/`false` (§3 evidence rule: does the paper state the
  basis of this value?);
- `basis_inferred` — `excess` / `absolute` / `total` / `unknown`;
- `wt_pct_convention` — `W1` / `W2` / `unknown`;
- `value_kind` — `measured` / `fitted_interpolated` / `fitted_extrapolated` /
  `unclear`;
- `sample_identity` — the printed label of the sample this value belongs to;
- `digitized_point` — figure rows only: the point's pressure and value as
  read from the figure, as `P; value` in bar and the plotted unit.

For a figure row, `isotherm_point` says which plotted point the row is ("k of
n, by increasing pressure", counting the dataset's digitized points of that
isotherm); a row of audit stratum (a) is its isotherm's maximum-uptake point.

Code then compares the filled sheet with the dataset
(`scripts/v1_search/audit.py score`, committed before any sheet was filled,
writes `score.json`). An error is a numeric
difference larger than the printed rounding (table or text) or 3% relative
(figures), or any categorical difference (§12). Errors are reported per field
and per audit stratum with exact (Clopper–Pearson) 95% CIs, and overall
weighted by the rows each cell represents. §12's follow-up rule then applies:
any error in audit stratum (a) is classified, C re-checks every row exposed
to its cause, and a further 30 rows of (a) are audited; a pooled (a) error
rate above 5% sends the author through every RQ1 primary-set value before
analysis.
