# Schema v1.1 → v1.2 migration plan

Written and committed **before** any protected file is touched, per manual §6.7.
Scope: stages 1–3 of `docs/schema_v1_2_gaps.md` — gaps 1, 2, 4, 5, 7, 8 and 9.
Gaps 3, 6 and 10 (stage 4) are **out of scope** and stay open; they redefine what
three existing columns mean, need a `docs/data_dictionary.md` rewrite, and touch
`plotting.py` and the ML feature list, so they get their own reviewed change.

Everything here is additive. No existing column changes meaning, and no existing
cell changes value. That is the property the verification asserts.

---

## 0. A correction to the counts in the committed gap document

`docs/schema_v1_2_gaps.md` and `docs/extraction_provenance.md` as committed at
`d65a8e2` state "133 rows extracted … 98 held". **Both numbers are wrong.** The
per-paper counts in those documents are right; the totals were not computed from
them. Summing the per-paper figures:

    10 + 20 + 5 + 6 + 3 + 3 + 12 + 9 + 8 + 6 + 7 + 16 = 105 extracted
    6 + 2 + 12 + 9 + 6                                =  35 written
                                                         70 held

**105 extracted, 35 written, 70 held.** Corrected in both documents as part of
this migration. The error was arithmetic in a summary line; no row, no
per-paper count and no decision rests on it, and nothing in the dataset is
affected. It is recorded here rather than quietly amended because a public
dataset's provenance document is not a place to silently change a number.

Consequently the stage 1–3 payoff, stated correctly: this migration unblocks
**52 rows across five papers** — HYC-0009 (20), HYC-0011 (5), HYC-0015 (3),
HYC-0017 (1), HYC-0026 (7), HYC-0029 (16) — taking the corpus from 156 rows /
16 papers to **208 rows / 21 papers**, clearing the 20-paper Phase 3 milestone.
Stage 4 would later add HYC-0007 (10) and HYC-0024 (8), reaching 226 / 23.

---

## 1. A defect in the existing validator, found while designing gap 4

The corpus's §11.5 warning baseline is:

    Unspecified uptake_type: 133
    mmol/g and wt% inconsistent: 1

**That single `mmol/g and wt% inconsistent` warning is a false positive.** It is
`HYC-0004-M2`, which reports `uptake_wt_pct = 0.05` and
`uptake_mmol_g = 0.268`. 0.268 mmol/g converts to 0.0540 wt%, which rounds to
0.05 at the precision the paper gives. The two reported values are mutually
consistent; the row is fine.

The check fires because `validate.py` uses a **relative-only** tolerance:

```python
denom = max(abs(wt), 1e-9)
if abs(converted - wt) / denom > 0.05:
```

At wt = 0.05 a 0.004 wt% absolute difference is an 8% relative difference. A
relative-only test is the wrong instrument near zero, where reporting precision
dominates. Every one of the corpus's 26 rows carrying both fields agrees to
better than 0.004 wt% in absolute terms; `HYC-0004-M2` is the only one whose
*relative* difference exceeds 5%, purely because its values are the smallest.

**Fix:** require both tests to fail before warning — relative difference above
5% **and** absolute difference above 0.02 wt%. 0.02 wt% is an order of magnitude
below the smallest uptake in the corpus that anyone would analyse, and an order
of magnitude above the rounding noise of a two-significant-figure report.

**Consequence, stated plainly: this removes a warning type from the baseline.**
After this migration the baseline is

    Unspecified uptake_type: 133

and `mmol/g and wt% inconsistent` is absent. §11.5 makes a *new* warning type a
stop condition; it does not address a type disappearing. A type disappearing
because a demonstrated false positive was fixed is a different event from one
disappearing silently, so it is stated here, restated in `CHANGELOG.md`, and the
baseline assertion in `tests/test_dataset_invariants.py` is updated in the same
commit with the reason in a comment. The manual does not specify a tolerance, so
there is no manual-versus-code conflict under §0 — the code was simply the only
authority and it was wrong.

---

## 2. Eleven new columns, appended at the end

Physical positions 41–51, appended after `ultramicropore_volume_cm3_g` so that
positional appends keep working (§6.7). Every column has a default that makes
all 156 existing rows valid without inspection.

| # | Column | Type | Default | Gap |
| --- | --- | --- | --- | --- |
| 41 | `uptake_bound` | `exact` / `upper` / `lower` / `approximate` | `exact` | 1 |
| 42 | `temperature_unstated` | bool | `false` | 2 |
| 43 | `pressure_unstated` | bool | `false` | 2 |
| 44 | `measurement_mode` | `isothermal` / `temperature_cycle` / `TPD` / `flow` | `isothermal` | 9 |
| 45 | `reference_temperature_k` | float 50–1500, optional | empty | 9 |
| 46 | `metal_element` | text, optional | empty | 7 |
| 47 | `metal_loading_wt_pct` | float 0–100, optional | empty | 7 |
| 48 | `residual_metal_element` | text, optional | empty | 7 |
| 49 | `residual_metal_wt_pct` | float 0–100, optional | empty | 7 |
| 50 | `dopant_concentration_wt_pct` | float 0–100, optional | empty | 8 |
| 51 | `dopant_concentration_method` | `elemental_analysis` / `XPS` / `AAS` / `ICP` / `other`, optional | empty | 8 |

Notes on three of them:

- **`uptake_bound`** defaults to `exact`, so every existing row asserts what it
  already asserted. `upper` means `uptake_wt_pct` holds a value the true uptake
  is below.
- **`measurement_mode` defaults to `isothermal`**, which is true of all 156
  existing rows and of every paper read so far except HYC-0029.
  `reference_temperature_k` is meaningful only when the mode is not isothermal:
  for HYC-0029 it is 673 K, the desorption end of its 303→673→303 K cycle, and
  without it the recorded uptake has no defined reference state. Its range runs
  to 1500 K because desorption temperatures are not measurement temperatures and
  the 500 K ceiling on `temperature_k` does not apply.
- **`metal_*` is deliberately separate from `dopant_*`.** A supported catalyst
  particle and a substitutional lattice heteroatom are different things with
  different mechanisms: HYC-0025's boron and HYC-0026's nitrogen are dopants,
  HYC-0029's cobalt and HYC-0027's palladium are impregnated metal. Collapsing
  them into one field would make the spillover subset uninterpretable.

## 3. Four controlled-vocabulary additions

- `synthesis_method` += `physical_activation`, `chemical_activation`,
  `chemical_exfoliation`
- `measurement_method` += `not_applicable`

No existing row's value changes. `not_applicable` exists for
characterization-only rows, which currently must claim `unknown` in a required
field when the true statement is "this row records no measurement".

**Not done here, on purpose:** existing rows forced onto `other` or
`carbonization` by the absence of an activation value — HYC-0019's twelve and
HYC-0022's four — are **not** relabelled in this migration. Relabelling them is a
data change, not a schema change, it needs its own Agent B pass against the
papers, and mixing it in would break the "no existing cell changes value"
property that makes this migration's verification assertable. Recorded as
outstanding.

## 4. Two validator changes

**4a. Gap 2 — conditions may be absent when the paper did not state them.**
`conditions_required_with_uptake` currently raises if an uptake-bearing row
lacks `temperature_k` or `pressure_bar`. It will instead accept a null field
when the matching `*_unstated` flag is `true`, and raise a **new ERROR** if a
flag is `true` while its field is populated — a row cannot both state a
condition and declare it unstated. The flags are the only way to get a null
past the check, so nulls cannot appear by accident.

**4b. Gap 4 — pairwise consistency across all three uptake fields.** The
existing wt%-versus-mmol/g check is generalised to all three pairs
(wt%↔mmol/g, wt%↔mL(STP)/g, mmol/g↔mL(STP)/g) at WARNING severity, using the
relative-and-absolute rule from §1. Two new warning *labels* are introduced,
`mL(STP)/g and wt% inconsistent` and `mL(STP)/g and mmol/g inconsistent`;
**neither fires on any of the 156 existing rows**, verified before the change by
converting all 24 rows that carry both volumetric and gravimetric values. So the
baseline after this migration contains one warning type, not three.

This is the gap whose absence let HYC-0009's 2.0–2.6× internal contradiction
reach a human reader instead of a validator.

## 5. Order of work

1. This plan, committed. ← the §6.7 gate
2. `scripts/migrate_v1_2.py` — appends the eleven columns with their defaults,
   `--dry-run` first, refuses to run twice, reads and writes raw CSV cells via
   the `csv` module so unmodified cells are byte-identical by construction, and
   verifies by re-reading both files from disk and asserting that **zero** cells
   changed in physical columns 1–40.
3. `src/hycan/schema.py` — eleven fields, four vocabulary values, the two
   validator changes.
4. `src/hycan/validate.py` — the generalised consistency check.
5. `scripts/validate_row_detail.py` — field mappings for the new warning labels.
6. New tests in new files. `tests/test_dataset_invariants.py` is the one
   pre-existing test file this migration edits, for the baseline assertion in
   §1, and that edit is the reason it is named here (§6.7).
7. Run the migration, verify from disk, run the full suite, `ruff check` only
   (**never** `ruff --fix` at repository scope — a broad `--fix` during Phase A
   modified a protected test file and had to be reverted).
8. Correct the counts in §0 across both affected documents.

## 6. Rollback

`scripts/migrate_v1_2.py` writes a timestamped backup before touching the
dataset. Because the migration is purely additive and asserts zero changes in
columns 1–40, reverting is dropping the eleven appended columns; the backup
makes that a file copy rather than a computation.

## 7. What this does not do

- Does not append any of the 70 held rows. That is the next step, under Agent B
  verification, after the migration is verified on disk.
- Does not touch gaps 3, 6 or 10.
- Does not relabel any existing row (§3).
- Does not add a `digitization_archive` field. Still outstanding from §6.9:
  nothing consumes a digitization archive's `status`, so a `figure_digitized`
  row can still be appended without any check that its §3.4 gate passed.
