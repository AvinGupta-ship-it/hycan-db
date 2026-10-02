# migrate_relabel — scope the physical_activation post-condition to a delta

**2026-10-02.** A verification-logic fix to a historical migration. **No dataset
cell changes**; the relabel output is untouched and remains byte-identical, which
`test_running_the_migration_on_its_pre_image_reproduces_the_committed_file`
proves.

## Problem

`scripts/migrate_relabel.py` check 5 (the "physical_activation stops being an
untested vocabulary value" post-condition) asserted **absolute global counts**:
`physical_activation` == 0 before the migration and == 2 after. That was true at
migration time (the plan's §1 claim), but it is a global post-condition that a
later append invalidates.

The 2026-10-02 Phase D batch invalidated it: **HYC-0032**'s two base carbons
(AC800, AC900) are CO2-gasified activated carbons, which are legitimately
`synthesis_method = physical_activation` (the same value the relabel put on
HYC-0022's CO2 rows, and the corpus's established convention for CO2 gasification,
§6.9). Their four rows (HYC-0032-M7/M8/M9/M10) take the global
`physical_activation` count to 6, so check 5 refused the migration when its own
test suite reconstructed the pre-image and re-ran it. Four tests failed, all from
this one refusal.

This is exactly the fragility §6.7 names: *"Pin deltas and partitions, not
absolute totals … A post-condition that a later append invalidates was never
testing this migration."*

## Fix

1. **`scripts/migrate_relabel.py`** — remove check 5's two absolute assertions
   (before == 0, after == 2). The `+2` **delta** is already verified, robustly,
   by the `EXPECTED_SYNTHESIS_DELTAS` check earlier in `verify()`
   (`after_counts[v] - before_counts[v] == delta`, with `physical_activation: +2`
   in the table), which passes unchanged with the new rows (before 4, after 6,
   delta +2). Check 5 was a redundant absolute cross-check; it is replaced by a
   comment pointing at the delta check. Nothing else in the script changes.

2. **`tests/test_migrate_relabel.py::test_physical_activation_is_no_longer_an_untested_vocabulary_value`**
   — change the global-set equality `physical == {"HYC-0022-M2","HYC-0022-M3"}`
   to a **subset** assertion `{"HYC-0022-M2","HYC-0022-M3"} <= physical`. The
   test's purpose — that the migration relabels HYC-0022's two CO2 rows onto
   `physical_activation` — is preserved, and its MUTATION (drop those rows from
   the map) still fails. The equality was itself a global absolute that any later
   physical_activation row breaks.

## Why this does not weaken the migration's guarantee

- **Post-condition 4** (`relabelled != SYNTHESIS_RELABEL`) already pins exactly
  which 36 cells changed `synthesis_method` and to which values — scoped to the
  diff, so robust to new data. That is the migration's core correctness
  guarantee and is untouched.
- The **`EXPECTED_SYNTHESIS_DELTAS`** check verifies the `physical_activation`
  `+2` delta (and every other synthesis delta), and its `untouched` companion
  asserts no other `synthesis_method` value's count changed. Both are deltas and
  both still run.
- The round-trip test proves the migration reproduces the committed dataset byte
  for byte. The relabel logic is unchanged.

## Verification

- Full suite green after the two edits.
- Mutation check 1: corrupt one `SYNTHESIS_RELABEL` target to a non-
  `physical_activation` value → `EXPECTED_SYNTHESIS_DELTAS` delta check fails
  (the `+2` is now `+1`). The delta check still catches a bad relabel.
- Mutation check 2: drop `HYC-0022-M2` from `SYNTHESIS_RELABEL` → the scoped test
  fails (the subset no longer holds) **and** the delta check fails.
