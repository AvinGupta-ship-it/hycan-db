# Migration plan — keep total uptake out of the Chahine figure

**Status:** planned 2026-10-01, before any code was written or any file touched
**Target file:** `src/hycan/plotting.py` (protected under manual §6.7)
**Tests:** `tests/test_plotting.py`
**Manual authority:** §12.3 (analysis filters), §13.3 (the Chahine criterion),
§6.7 (protected files)

---

## 1. Why

The Chahine rule bounds **adsorbed** hydrogen against surface area — roughly
1 wt% per 500 m²/g at 77 K. A **total** uptake is the adsorbed amount *plus* the
compressed gas occupying the pore volume, which the authors of HYC-0031 add
explicitly through their eq. (1). A total uptake therefore exceeds the Chahine
bound **by construction**, and plotting it against that line compares a
different quantity to the rule.

Until 2026-09-30 the corpus held **zero** `uptake_type = total` rows, so this
could not arise. HYC-0031 introduced 13 of them, and `fig3_chahine` now plots 9:

| row | sample | uptake | BET | bound (BET/500) |
| --- | --- | ---: | ---: | ---: |
| HYC-0031-M1 | CA-4600 | 3.1 | 2001 | 4.00 |
| HYC-0031-M3 | CA-4600 | 6.2 | 2001 | 4.00 |
| HYC-0031-M5 | CA-4600 | 6.7 | 2001 | 4.00 |
| HYC-0031-M9 | CA-4700 | 3.9 | 3771 | 7.54 |
| HYC-0031-M11 | CA-4700 | 8.1 | 3771 | 7.54 |
| HYC-0031-M13 | CA-4700 | 8.9 | 3771 | 7.54 |
| HYC-0031-M18 | CA-4800 | 3.4 | 2864 | 5.73 |
| HYC-0031-M20 | CA-4800 | 6.8 | 2864 | 5.73 |
| HYC-0031-M22 | CA-4800 | 7.3 | 2864 | 5.73 |

Three of the nine (M11, M13, M22) sit above their own bound, and they are
*supposed* to: that is what "total" means. Left in, the figure shows the corpus's
best-reported modern activated carbon apparently violating the rule the figure
exists to illustrate, and the violation is an artefact of the y-axis quantity.

**It is also a double count.** Those 9 rows are the paired partners of 9 `excess`
rows at the same sample, temperature and pressure — one measurement expressed two
ways. Before this append, **zero** sample/T/P groups in the figure carried more
than one `uptake_type`; now 9 do. Excluding `total` collapses each pair to the
one point that the rule describes, so a single change fixes both problems.

The same double count inflates any corpus-wide mean of `uptake_wt_pct`: 1.9966
excluding `total`, 2.1560 including it, an 8% shift. That is **not** fixed here —
see §6.

## 2. What was checked and is NOT wrong

§12.3's other exclusions were suspected and cleared, measured rather than
assumed. Of the 132 rows `fig3_chahine` currently plots, **all 132** are already
`uptake_bound = exact` and `measurement_mode = isothermal`, and none has
`temperature_unstated` — the `temperature_k == 77` filter excludes those by
construction. So the figure's only contamination is the 9 `total` rows.

Three rows carry `pressure_unstated = True`. They are left in: the Chahine bound
is a function of surface area, not pressure, and §13.3's criterion is scored
against surface area alone. Recorded so the decision is visible rather than
overlooked.

## 3. Scope

In `fig3_chahine` only: exclude rows whose `uptake_type` is `total` from the
plotted subset. 132 → 123 rows.

`unspecified` rows stay. 91 of the 132 are `unspecified`, and §B.5 of the manual
records that as the field's normal state and not an extraction failure —
excluding them would empty the figure of most of the corpus. `absolute` would
also stay if it appeared; it does not occur in the corpus.

The axis label gains "excess or unspecified" so the figure states its own
subset, and the exclusion count is reported, because a figure that silently
drops rows is the §12.4 failure.

Nothing else changes. No other figure, no other filter, no data.

## 4. Preconditions

1. `uptake_type` is a column of the frame.
2. The exclusion is applied *after* the 77 K and null filters, so the reported
   count is the number of rows the figure would otherwise have plotted.

## 5. Post-conditions

1. No plotted point has `uptake_type = total`.
2. Every plotted point's `(sample_id, temperature_k, pressure_bar)` is unique —
   the double count is gone.
3. A frame with no `total` rows plots exactly what it plotted before, so the
   change is a no-op on the pre-HYC-0031 corpus.
4. A frame consisting only of `total` rows yields the empty-but-labelled axes,
   not a crash.

## 6. Explicitly NOT fixed here

`uptake_type` still appears nowhere else in `plotting.py` or `clean.py`, and
**there is no canonical §12.3 filter function in the code at all** — the four
exclusions the manual calls mandatory live only in its prose, so every analysis
has to remember them independently. That is the root cause of this defect and of
its being introduced unnoticed. A `src/hycan/analysis.py` exposing one
`analysis_subset(df)` used by every figure is the durable fix. Not attempted
here; this plan keeps its scope to the figure that is wrong today.

Until then, a dataset invariant test enumerates the paired total/excess rows by
`measurement_id`, on the precedent of the null-wt% rows already enumerated in
`tests/test_dataset_invariants.py`, so a future aggregation cannot meet them
silently.

## 7. Mutations the tests must kill

1. Remove the `total` exclusion.
2. Apply it before the 77 K filter, so the reported count is wrong.
3. Exclude `unspecified` as well, emptying the figure.
4. Exclude `excess` instead of `total`.
5. Drop the uniqueness post-condition.
6. Leave the axis label unchanged while excluding rows.

A mutation that does not cause a failure is a gap in the tests, not a pass.

### 7.1 Result

**Seven mutations run, six killed.** The seventh was added beyond the plan's
list — filtering in place with `sub.drop(..., inplace=True)` — and it survived.
That is **not** a gap: `df[mask]` returns a copy in pandas, so `sub` is never a
view on the caller's frame and an in-place drop on it cannot reach `df`. The
mutation is semantically equivalent, so no test can kill it, and inventing one
would be a test that passes for the wrong reason.
`test_the_input_frame_is_not_mutated` is kept because it states the module
docstring's promise, with the caveat recorded that it cannot catch this.

`src/hycan/plotting.py` **had no tests at all** before this change, although it
produces every published figure and is protected under §6.7. That is how a
figure could be wrong with nothing failing. `tests/test_plotting.py` now covers
the Chahine subset in full and gives the other two figures smoke coverage; a
real behavioural suite for those two is still owed.

### 7.2 The invariant promised in §6

`tests/test_dataset_invariants.py` now enumerates by `measurement_id` the **13
sample/T/P groups, 26 rows**, that report one measurement under two uptake
types, all of them HYC-0031's, and asserts each pair is exactly one `excess` and
one `total`. Appending another such paper fails that test and names the rows,
which is what makes a silent double count loud.
