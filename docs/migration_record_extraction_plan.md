# Migration plan — a routine tool for §9.1 step 15

**Status:** planned 2026-09-30, before any code was written or any file touched
**Target file:** `references/paper_tracking.csv` (protected under manual §6.7)
**Script:** `scripts/record_extraction.py`
**Tests:** `tests/test_record_extraction.py`
**Manual authority:** §9.1 step 15, §5.2 (tracking is the source of truth),
§6.7 (protected files, byte-level verification), §3.2 (dual-agent record)

---

## 1. Why this exists at all

§9.1 step 15 — update `references/paper_tracking.csv` after an extraction — is
**the step this project has skipped more than any other**. The record:

- skipped for every paper in Phase C, ten consecutive papers;
- skipped again for HYC-0007 and HYC-0024 **one commit after** that was fixed;
- one paper written under a malformed id (`HYC-009`) that an id-matching repair
  would have silently passed over.

Each time it was fixed by a one-off migration. `scripts/sync_paper_tracking.py`
is the most recent, and it **refuses to run twice** by design, because it
encodes one specific backfill.

So after every extraction the project has faced a protected file, a routine
update, and no routine tool — and the routine update is what loses. That is not
carelessness; it is a missing tool. The durable fix is a step-15 tool with the
same guarantees the one-off migrations have, usable on every future paper.

This plan is therefore written once and the script is reused, rather than a new
migration plan per paper.

## 2. Scope

For one `--paper-id`, in `references/paper_tracking.csv` only:

| column | set to |
| --- | --- |
| `extraction_status` | `--status` (`extracted` or `verified`) |
| `extraction_date` | `--date`, default today |
| `notes` | optionally appended to, via `--append-note` |

Nothing else. No other row is touched, no row is added or removed, and no other
column changes on the target row.

`verified` is permitted only with `--verified-by`, which records the dual-agent
outcome. §5.2 defines `verified` as the §3.2 protocol completed with all
disputes resolved, so the script will not write that word without the evidence
string that makes it true.

## 3. Preconditions

1. Header is the expected 13 columns.
2. Physical line count equals data rows + 1, so the byte check in §4 is sound.
3. The named `paper_id` exists exactly once.
4. `screening_decision` on that row is `include`. A paper excluded at screening
   cannot have been extracted, and if it has, one of the two records is wrong
   and the script must stop rather than paper over it.
5. **`pdf_obtained` is `yes`.** The same argument: a full text that was never
   retrieved cannot have been extracted.
6. **The dataset actually contains rows for this paper**, and the count is
   reported. Writing `extracted` for a paper with no rows is the failure mode
   step 15 exists to prevent, inverted.
7. **Refuse to re-run:** if the row already carries the requested status *and*
   date. Re-running with a different status is allowed — `extracted` becomes
   `verified` after Agent B — and is reported as a transition.

## 4. Post-conditions

1. Row count unchanged.
2. **Every physical line except the target row's is byte-identical**, compared
   as raw lines, not parsed cells.
3. Line terminator (CRLF) and final-newline state (absent) unchanged.
4. On the target row, only `extraction_status`, `extraction_date` and `notes`
   differ.
5. `extraction_status` across the file stays inside its vocabulary
   (`not_started`, `extracted`, `verified`).
6. `data/raw/measurements_v0.1.csv` sha256 unchanged, baselined as the **first**
   action in `main()` — the ordering defect found in
   `migrate_phase_d_screening.py`, where the baseline was taken late enough that
   the guard would have hashed an already-corrupted file.

## 5. First use

`HYC-0031` → `extracted`, 2026-09-30, 32 rows in the dataset.

Not `verified`: the dual-agent protocol ran and every dispute resolved, but two
resolutions turn on material that is **not in the obtained PDF** — the
Supplementary Information. Agent C named Supplementary Table 4 and
Supplementary Fig. 11 as what would settle the AX21 temperature outright, and
Supplementary Table 4 holds AX21's textural properties, which are blank on six
rows. `verified` would assert a completeness the record does not have. The
tracking note records what is outstanding.

## 6. Mutations the tests must kill

1. Remove the refuse-to-re-run guard.
2. Write with `csv.writer` defaults instead of the detected CRLF.
3. Compare parsed cells instead of raw bytes.
4. Touch a row other than the target.
5. Change a column the plan does not name.
6. Drop the `screening_decision == include` precondition.
7. Drop the `pdf_obtained == yes` precondition.
8. Drop the dataset-rows-exist precondition.
9. Accept `verified` without `--verified-by`.
10. Skip the dataset-untouched assertion.
11. Drop the physical-line-count precondition.
12. Accept a status outside the vocabulary.

A mutation that does not cause a failure is a gap in the tests, not a pass.

---

## 7. Amendment — test changes the first append forced

**Written 2026-09-30, before the edits, because `tests/` is protected under
§6.7.** Appending HYC-0031's 32 rows broke 13 existing tests. Diagnosed rather
than assumed, they were four distinct things, and only one was a stale pin:

**7.1 A real defect in the appended data, which a test caught and
`append_paper.py` did not.** `data/raw/measurements_v0.1.csv` is **LF**
terminated. The HYC-0031 staging file was written **CRLF**, because the
extractor detected `references/paper_tracking.csv`'s format carefully and then
assumed the dataset shared it. `append_paper.py` reported "0 errors, 0 new
warning types" and printed "Verify  merged file re-read from disk" — a
cell-level check, which cannot see a line ending. The file was left with 228 LF
lines and 32 CRLF ones.

Caught by `tests/test_migrate_relabel.py::test_running_the_migration_on_its_pre_image_reproduces_the_committed_file`,
whose byte-level replay is the only check in the suite that could see it.

Fixed by rewriting the 32 appended rows to LF, verified by re-running that
replay test and by asserting the committed prefix is byte-identical. **The
durable fix is §7.5 below**: `append_paper.py` must refuse a staging file whose
terminator differs from the dataset's.

**7.2 `tests/test_held_rows.py` breaks on every append, not just this one.**
Four of its tests call `backfill_interlayer_spacing.py` without
`--expected-rows`, so they hit the script's default of 227 — the count it
historically ran against, which is worth keeping as a record. The fixture is
built from the *current* dataset, so the default refuses the moment a row is
appended.

`tests/test_migrate_relabel.py` already solved this and documented why, in
`corpus_row_count()`: "these tests build their fixture from the CURRENT dataset,
so passing the default would make every one of them fail the moment a row was
appended… §6.7: a pinned total is a test that expires." The same helper is
adopted here. The scripts' defaults are not touched.

**7.3 `tests/test_sync_paper_tracking.py` asserts an equivalence that is now
false.** `dual_agent_papers()` returns papers all of whose rows carry
`extractor = "HyCAN pipeline v2"`, and the suite asserts the `verified` count
equals its size. That held while every v2-pipeline paper had completed
dual-agent verification. HYC-0031 is the first counterexample: extracted by the
v2 pipeline, deliberately **not** `verified`, because two dispute resolutions
turn on Supplementary material not in the obtained PDF.

The equivalence is amended to containment — `verified` ⊆ v2-pipeline papers —
with the exceptions enumerated by paper id, so a paper cannot silently linger as
`extracted`. This is the §13.4 principle: the letter must keep meaning one
thing, and the exception is disclosed rather than absorbed.

**7.4 `tests/test_validate.py`'s scorer-agreement pin, 141 → 164.** The test's
own comment says it is "pinned as a total on purpose… It must be updated
deliberately whenever the corpus changes, which is the point." Updated
deliberately. No assigned tier changes.

**7.5 Follow-on, not done in this change:** `append_paper.py` verifies cells and
counts and calls the result "verified", and it cannot see a line terminator.
It must detect the dataset's terminator and refuse a staging file that differs,
and it must assert the merged file's terminator and final-newline state are
unchanged. Until it does, §7.1 can recur on any paper. Tracked as the next
piece of work.
