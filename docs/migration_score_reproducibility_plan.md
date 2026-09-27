# Plan — fix the four `score_reproducibility` defects

**Status:** written and committed before any protected file is touched, per §6.7.
**Date:** 2026-09-27
**Target files:** `src/hycan/validate.py` (protected), `tests/test_validate.py`
(protected), `docs/reproducibility_tiering.md`. **No change to
`data/raw/measurements_v0.1.csv`.** No assigned `reproducibility_tier` changes.

---

## 0. Why, and the one thing this plan does not do

Execution manual §13.7 records one defect in `score_reproducibility`. Agent B
found three more while verifying HYC-0007. All four are now fixed together,
because all four are in the same function and three of them fire on the same
paper.

**This plan changes no tier in the dataset.** `suggest_tier` is advisory: every
`reproducibility_tier` in the corpus was assigned by judgment against §13.3 and
cross-checked by Agent B, not taken from the function's output. What changes is
what the function *suggests*, which is what §13.7 says must be made honest before
anything consumes it automatically. Where the fixed scorer now disagrees with an
assigned tier, §6 records the disagreement as a question rather than resolving it.

**Three of the four fixes make the code agree with a rubric this project already
wrote down.** `docs/reproducibility_tiering.md`'s second worked example scores a
Langmuir-only area as **"BET 1 (surface area reported but not BET)"**, and the
same document lists the purity proxy as a known weakness. The scorer implements a
different, undocumented scale. The defect is the code, not the rubric.

## 1. Defect 1 — a null temperature buys a free Chahine point

§13.7. The current branch is:

```python
if not _present(t) or w is None:
    chahine = 1  # cannot assess
```

Before v1.2 `temperature_k` was required, so this fired only when a row had no
derivable uptake. Since v1.2, six rows legitimately carry a null `temperature_k`
under `temperature_unstated`, and each collects a point for a check that never
ran. **HYC-0011's ordinary 0.26 wt% row and its discredited 8.0 wt% row score
identically**, because neither states a temperature. The one value the criterion
exists to catch is the one it cannot see.

**One condition is being read as three different situations.** Separating them is
the whole fix:

| Situation | Rows | Honest score |
| --- | --- | --- |
| No uptake of any kind — a characterization-only row | 11 | **1.** The criterion has no subject. Not a reporting failure. |
| Uptake present but not convertible to wt% — HYC-0024's volumetric-only rows | 10 | **1.** The Chahine rule is defined in wt%; this genuinely cannot be assessed. |
| Uptake in wt% but the paper never stated a temperature | 6 | **0.** The criterion reads "within Chahine-consistent range for **the stated conditions**". There are none. This is a reporting deficiency and scores as one. |

The third row of that table is §13.7's prescribed fix, stated there as "the honest
score is 0 with a reason — not 1 by default". The first two are the cases the old
branch was written for and they keep their point.

**Pressure is deliberately out of scope.** Twelve rows carry a null
`pressure_bar`. They already lose the `temp_pressure` point, which requires both,
and the Chahine bound as implemented is pressure-blind at every temperature — so
an unstated pressure does not prevent evaluating it. Penalizing it twice would be
punishing the same omission in two criteria. That the 77 K bound ignores pressure
entirely is a separate imprecision, recorded in §7.

## 2. Defect 2 — `bet` scores 0 for a paper that reported its surface areas

The criterion is "BET surface area reported and consistent with material class",
0–2. The code awards 2 for any positive `bet_surface_area_m2_g` and 0 otherwise.
Two things are wrong with that, in opposite directions.

**It scores 0 where an area was reported.** HYC-0007 reports a *micropore* and an
*external* surface area per sample from an αs plot and no total, so
`bet_surface_area_m2_g` is null on all 8 rows and the scorer says "no surface area
reported" about a paper that reported eighteen surface-area values by a named
method. Those are the values `micropore_surface_area_m2_g` and
`external_surface_area_m2_g` were added in v1.3 to hold.

**It scores 2 where the method is unknown.** 31 rows carry an area in
`bet_surface_area_m2_g` that is not known to be BET — HYC-0005's 25 and
HYC-0012's 6, both `surface_area_method = unspecified`. §8.6 records that
HYC-0005's 25 rows were deliberately reassessed for exactly this: the paper's
column is headed "TSA, total surface area" and never says BET, so the method was
set to `unspecified` and `extraction_confidence` dropped 5 → 4. Awarding those
rows full marks on a criterion that names BET contradicts a decision this project
already made and recorded.

**Fix: the three-level scale the tiering document already specifies.**

| Points | Condition | Basis string |
| --- | --- | --- |
| 2 | an area is present **and** `surface_area_method == "BET"` | `bet_total` |
| 1 | an area is present by another or unstated method | `area_by_<method>` |
| 1 | no total, but micropore **and** external areas are both present | `resolved_components` |
| 1 | no total, but a Langmuir area is present | `langmuir_only` |
| 0 | no area of any kind | `no_area` |

A row whose `surface_area_method` key is absent entirely — possible only for a
hand-built dict, never for a dataset row — is treated as `unspecified`, matching
the schema default.

## 3. Defect 3 — purity is proxied by whether the sample was *purified*

`purity = 1 if _present(row.get("purification_method"))`. The criterion is
"Sample purity / impurity content **reported**". Those are different claims, and
HYC-0007 shows the difference cleanly: its **pristine** SWCNT scores 0 despite
the paper reporting 11 wt% residual metal for it, while its acid-treated A-SWCNT
scores 1 for having been treated. The scorer rewards the treatment and ignores
the measurement.

Schema v1.2 added `residual_metal_element` and `residual_metal_wt_pct` for
reported impurity content. **Fix:** score 1 for a reported residual metal weight
percent, or a named residual metal, or a purification method — in that order of
strength, recorded as a basis string. This only ever converts a 0 to a 1; no row
loses the point.

## 4. Defect 4 — the Chahine bound cannot see a resolved surface area

At 77 K with `bet_surface_area_m2_g` null the code returns `chahine = 1`,
"cryogenic but no surface area to bound against". For HYC-0007 there *is* an area
to bound against: an αs-plot decomposition into micropore and external components,
whose sum is the total. Summing them is this project's own convention —
`validate.py`'s dataset check already asserts that component areas sum
consistently with a total wherever both are present.

**Fix:** resolve the bounding area as `bet_surface_area_m2_g`, else
`micropore_surface_area_m2_g + external_surface_area_m2_g` when both are present,
and record which was used.

**Langmuir is deliberately not used as a Chahine bound**, though it does earn a
BET point under §2. This is the one place the fix does **not** reach the tiering
document's worked example 2, which awards that row Chahine 2 on physical
plausibility — a judgment the code has no way to make. It returns 1, "cannot
assess". The divergence is asserted as a test rather than hidden, alongside the
`method` point the same example hand-scores differently.

A Langmuir fit systematically over-reads on a microporous
carbon, so using it would raise the expected value and loosen the bound — it would
hide exactly the over-claims the criterion exists to catch. Erring toward
"cannot assess" is the safe direction; erring toward a generous bound is not.

## 5. What every changed score is, in full

Computed over all 225 rows. **45 rows change their total or their suggested tier.**

Per criterion:

| Criterion | Change | Rows | Papers |
| --- | --- | --- | --- |
| `bet` | 0 → 1 (`resolved_components`) | 8 | HYC-0007 |
| `bet` | 2 → 1 (`area_by_unspecified`) | 31 | HYC-0005 (25), HYC-0012 (6) |
| `purity` | 0 → 1 (`residual_metal_measured`) | 1 | HYC-0007 |
| `chahine` | 1 → 2 (`cryo_vs_component_sum`) | 3 | HYC-0007 |
| `chahine` | 1 → 0 (`temperature_not_reported`) | 6 | HYC-0011 (4), HYC-0015 (2) |

Suggested-tier movements:

| Movement | Rows | Papers |
| --- | --- | --- |
| C → B | 3 | HYC-0007 |
| B → C | 5 | HYC-0005 |
| C → D | 4 | HYC-0011 |
| total changed, tier unchanged | 33 | HYC-0005, HYC-0007, HYC-0012, HYC-0015 |

## 6. Agreement with the assigned tiers goes DOWN, and that is not a defect

| | Rows whose suggested tier matches the assigned tier |
| --- | --- |
| Current scorer | 144 / 225 (64.0%) |
| Fixed scorer | **140 / 225 (62.2%)** |

**Agreement with the assigned tiers is the wrong success metric and must not be
used as one.** If it were the metric, the correct "fix" would be whatever makes
the scorer reproduce the humans' choices — which destroys the only thing an
independent scorer is for. The scorer is checked against the **rubric**, and §7's
tests check it against the rubric's own three worked examples.

The movement decomposes into four gains and eight losses, and each is worth
reading on its own terms.

**Four gains, all of them the defect working as intended.**

- **HYC-0007-M1, M2, M3: suggested C → B, assigned B.** The current scorer calls
  four of this paper's eight rows Tier D — "poor reproducibility or inconsistent
  with established physics" — about a paper that reports two resolved surface
  areas by a named method, a residual metal content, and a Sieverts measurement.
  All three defects 2, 3 and 4 fire here at once.
- **HYC-0011-M4: suggested C → D, assigned D.** This is the 8.0 wt% film, the
  corpus's one `Pre-2005 raw-CNT high uptake (Tier D)` warning and the row §13
  exists for. The free Chahine point was the only thing holding it at C. This
  single row is the clearest evidence the fix is right.

**Eight losses, and neither group is resolved by this plan.**

- **HYC-0005-M2, M3, M4, M6, M7: suggested B → C, assigned B.** They sat at
  exactly 6 points and lose the BET point under §2. The rubric's own worked
  example scores an area of unknown method as 1, and §8.6 already recorded that
  this paper's area is not known to be BET — so the new score follows the
  documented rubric and the assigned B is the thing now in question. These are the
  five weakest rows of that paper's 25.
- **HYC-0011-M1, M2, M3: suggested C → D, assigned C.** Ordinary 0.21–0.26 wt%
  rows from a paper that states no temperature, no surface area, no uptake type,
  no purity and no calibration. They score 2 of 10. Tier D reads harsh for an
  unremarkable value, and it is also what the rubric computes.

**Neither group is re-tiered here.** Eight assigned tiers are now in tension with
the documented rubric, and resolving that is a scientific judgment on eight rows
across two papers, not a side effect of a code fix. Recorded in
§6.9 of the manual as an open question with the rows named. §13.6 governs: the
tier is the disclosure, so the disagreement is published rather than smoothed.

## 7. What is still wrong after this fix

Stated because a fix that quietly narrows its own scope is worse than no fix.

- **`calibration` is still always 0.** No schema field records a blank correction
  or void-volume calibration. The code ceiling is therefore 9, not 10, and no row
  can be suggested Tier A on an `unspecified` uptake type. Unchanged.
- **The four characterization-only HYC-0007 rows still suggest Tier D** against an
  assigned B. This is §6.9's standing limitation — the rubric scores the reporting
  quality of an *uptake measurement*, and these rows have none, so they inherit
  their paper's tier. The fix lifts them from 1 point to 2 and does not make them
  meaningful. A `tier_basis` field or a second mechanism-aware rubric is the real
  answer and belongs in Phase E, per §13.4.
- **`method` still cannot tell a described protocol from a named one.** The rubric
  awards 2 for "clearly described (instrument, protocol)" and the code awards 2 for
  any recorded vocabulary value. Both of the tiering document's worked examples 2
  and 3 score this 1 by hand. No schema field distinguishes them.
- **The 77 K Chahine bound ignores pressure.** BET/500 is the rule's canonical
  form at moderate pressure; applying it unchanged at 1 bar sets an expectation far
  above what any carbon delivers there, so a 1 bar row passes trivially. 50 rows
  sit at 77 K / 1 bar. Making the bound pressure-aware needs an isotherm model and
  is out of scope here.
- **A non-BET total area is still accepted as a Chahine bound**, even though §10.3
  says uptake per m² may be computed only where the method is BET. The tier
  criterion is a sanity bound rather than a published statistic, so an area of
  unknown method is better than no bound — but it is an inconsistency between two
  sections of this project's own rules, and it is recorded rather than resolved.

## 8. Method and post-conditions

`score_reproducibility`'s return dict gains three keys — `bet_basis`,
`purity_basis`, `chahine_basis` — so that a suggestion can be audited without
re-deriving it. Additive; no existing key changes name or meaning.

**One existing test's fixture must be completed, and it is a §6.7 case.**
`test_full_report_row_scores_nine_tier_a` builds a row with
`bet_surface_area_m2_g = 2600` and **no `surface_area_method`**, then asserts a
total of 9. It is the tiering document's worked example 1, which states "reports
BET ≈ 2600 m²/g" — so the row is meant to carry a BET area and the fixture simply
omits the field that says so. Adding `surface_area_method: "BET"` makes the
fixture the row it claims to be. **This is completing a fixture, not weakening an
assertion:** the total stays 9 and the tier stays A. Every other existing
assertion in `tests/test_validate.py` is unchanged and must stay green.

`docs/reproducibility_tiering.md` is updated in the same commit, per §8.7's
principle applied to the rubric: its three worked examples carry parenthetical
notes about how `suggest_tier` scores them differently, and two of those notes
become false once the code matches the rubric.

Post-conditions:

1. `data/raw/measurements_v0.1.csv` byte-identical. sha256 unchanged at
   `1605d9a718d05608b550610eabba3494aea4f87e45e934226eda0cda1c476d2f`.
2. No `reproducibility_tier` value changes anywhere.
3. Validator output unchanged: 225 rows, 225 valid, 0 errors, warning baseline
   `Unspecified uptake_type` ×202 and `Pre-2005 raw-CNT high uptake (Tier D)` ×1,
   no new type. `score_reproducibility` feeds no warning, so this must hold
   exactly.
4. All three worked examples in `docs/reproducibility_tiering.md` are asserted as
   tests, and the scorer reproduces each one's **BET, purity and Chahine** points.
   Where a worked example's hand-scored `method` or `calibration` point differs
   from the code's, the test asserts the documented difference rather than
   pretending it is absent.
5. The five criterion-level changes in §5 are asserted by row id, so a later
   change to the scorer that silently re-awards the free Chahine point fails.
6. Exactly 6 rows score `chahine = 0` with basis `temperature_not_reported`, and
   they are the six carrying `temperature_unstated` with a derivable wt%.
7. Exactly 11 rows score `chahine = 1` with basis `not_applicable_no_uptake` and
   exactly 10 with `not_assessable_non_gravimetric` — so the three-way split is
   pinned by partition, not by total.

   **This figure was wrong in the first draft of this plan, as 8.** It was taken
   from the count of rows carrying `volumetric_capacity_kg_m3` rather than
   computed from the rows whose uptake does not convert to wt%: three HYC-0024
   rows carry only an `adsorbed_phase_density_kg_m3`, and a fourth carries the
   `approximate` wt% the verifier recovered from the paper's abstract. Caught by
   the test that asserts the partition rather than the total, which is the
   argument for pinning partitions — §2.4's error class, found by a check instead
   of by rereading.
8. `suggest_tier` still returns one of A/B/C/D for every row in the corpus and for
   an empty dict.
9. Every new guard is mutated and confirmed to fail. **Eight mutations, and the
   first run of all eight was worthless.** They were applied to a scratch copy of
   the repository, but the package is installed editable, so `import hycan` in
   that copy resolved back to `/home/claude/hycan-db/src/hycan/validate.py` — the
   unmutated original. All eight "survived", which read exactly like eight
   untested guards and was in fact a harness that tested nothing. §3.8 applies to
   a mutation run as much as to a file write: *a test run's exit status is not
   evidence about the code you think it ran.*

   The fix is two lines and both are required: set `PYTHONPATH` to the scratch
   copy's `src/`, **and assert inside each run that `hycan.validate.__file__`
   points into the scratch copy** before trusting the result. With the import
   verified, all eight mutations fail the tests that name them — 5, 2, 4, 3, 1, 2,
   2 and 8 failures respectively. A mutation harness needs its own guard, because
   a silent no-op is indistinguishable from a passing mutant.
