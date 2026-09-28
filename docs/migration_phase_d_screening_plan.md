# Migration plan — Phase D screening results into `paper_tracking.csv`

**Status:** planned 2026-09-27, before any code was written or any file touched
**Target file:** `references/paper_tracking.csv` (protected under manual §6.7)
**Script:** `scripts/migrate_phase_d_screening.py`
**Tests:** `tests/test_migrate_phase_d_screening.py`
**Manual authority:** §7.4 (screening must be recorded), §7.5 (PRISMA), §6.7 (protected
files, byte-level verification), §5.2 (`paper_tracking.csv` is the source of truth)

---

## 1. Why this migration exists

Phase D's literature search identified 123 candidate papers. §7.4 states that "every
screened paper gets a row in `paper_tracking.csv` with its decision and, if excluded,
its reason. A screening decision made and not recorded did not happen."

`paper_tracking.csv` is a protected file. Manual §6.7 requires that any change to it
be applied by a committed script under a migration plan written beforehand, with
byte-level verification that untouched lines are unchanged. This document is that
plan. It was written before the script.

## 2. Scope — what this migration does

**Appends 35 new rows**, `HYC-0031` through `HYC-0065`, to `references/paper_tracking.csv`.

It **modifies no existing row**, **changes no existing cell**, and **deletes nothing**.
That is the whole scope, and it is narrower than any previous migration to this file.

## 3. What the 35 rows are, and why only 35

The search produced 123 candidate records across four agents. They were reduced as
follows, and every step is reproducible from the artifacts in the screening log:

| Step | Count |
| --- | ---: |
| Candidate records produced by the four search agents | 123 |
| Less: agent-screened exclusions against §7.2 | −14 |
| Less: a further confirmed duplicate of a tracked paper | −1 |
| Less: the same paper found by two agents | −5 |
| Distinct screened candidates | 103 |

The three duplicates of already-tracked papers were `A1-05` (HYC-0025), `A4-25`
(HYC-0012) and `A2-32` (HYC-0024); the first two were already inside the 14
agent-screened exclusions, so only one is subtracted again here. An earlier draft of
this table wrote −3 and −3, which totalled correctly to 103 by coincidence and named
the wrong figures on both lines.
| Of which: bibliographic metadata independently resolved against OpenAlex | 42 attempted |
| **Resolved to a confirmed DOI and full metadata** | **35** |
| Unresolved (no DOI obtainable; see §3.2) | 7 |
| Not yet metadata-resolved (below the priority cut) | 61 |

**Only the 35 with a confirmed DOI enter the tracking file.** The reason is §3.5:
a DOI that has not been resolved is not a DOI, and `paper_tracking.csv` is the
project's source of truth. Writing an unresolved title, year or DOI into it would put
a value into the authoritative file that nothing has checked — the precise defect that
§7 of the handoff record and the three OpenAlex errors in `bibliography_sources.json`
exist to prevent.

The other 68 are not discarded. They are recorded in `docs/phase_d_screening_log.md`
with their evidence level, which satisfies §7.4's "a screening decision made and not
recorded did not happen" without contaminating the source of truth. In PRISMA terms
they are **identified** but not yet **screened to a decision**; the log keeps the
counts so a later session can resume without redoing the searches.

### 3.1 How the 35 were verified

Each was resolved through OpenAlex's `works/doi:` endpoint by an agent that did not
perform the search, and the returned title was compared against the title the search
agent had recorded. **29 confirmed on the recorded DOI; 6 were recorded with a
publisher article ID rather than a DOI and were confirmed by testing the hypothesis
`10.1039/<RSC-ID>` against the same endpoint and requiring the returned title to
match.** No candidate resolved to a different paper. Every `title`, `authors`, `year`
and `journal` value written by this migration is the verbatim OpenAlex field, not the
search agent's recording of it.

This matters because one search agent caught itself writing a DOI it had not seen,
and removed it before writing its file. The verification pass is what makes the
absence of a second such case a finding rather than an assumption.

### 3.2 The seven unresolved, and why they stay out

Three are DOE Hydrogen Program annual progress reports. These are **not
peer-reviewed**, which §7.1 requires, so they are excluded on the merits and not
merely on a missing DOI. Four are Elsevier articles whose PII is known but whose DOI
is not derivable from it; they remain candidates in the screening log and can be
resolved when the rate limit permits.

## 4. Column-by-column specification for the new rows

| Column | Value |
| --- | --- |
| `paper_id` | `HYC-0031` … `HYC-0065`, assigned in descending funnel-priority order |
| `title` | verbatim OpenAlex `display_name` |
| `authors` | verbatim OpenAlex author list, `;`-separated, in order |
| `year` | verbatim OpenAlex `publication_year` |
| `journal` | verbatim OpenAlex `primary_location.source.display_name` |
| `doi` | the confirmed DOI, lowercased (matching the file's existing convention) |
| `search_source` | `phase_d:<agent>:<cand_id>`, e.g. `phase_d:A1:A1-10` |
| `screening_decision` | `include` on all 35 |
| `exclusion_reason` | empty on all 35 |
| `pdf_obtained` | `no` on all 35 |
| `extraction_status` | `not_started` on all 35 |
| `extraction_date` | empty on all 35 |
| `notes` | the funnel tags that justify the paper's priority, plus any caveat to confirm when the PDF arrives |

`paper_id` ordering is by the funnel-priority score, so the ID sequence itself encodes
the upload priority and the list handed to Avin is in ID order.

## 5. Preconditions — the script refuses unless all hold

1. The file has exactly 13 columns and the expected header.
2. It has exactly 30 data rows (overridable with `--expected-rows` so the script is
   testable against a fixture rather than only against the real file — manual
   Appendix A.5 requirement 2).
3. Its physical line count equals data rows + 1. This is the precondition
   `migrate_relabel.py` added: a newline inside a quoted `notes` cell would break the
   line-to-row mapping that the byte-level check in §6 depends on, so the byte check
   is unsound without it.
4. No row already carries any `paper_id` in `HYC-0031`…`HYC-0065` — **the refuse-to-re-run
   guard.**
5. No DOI being added already appears in the file.
6. Every new row has all 13 fields populated per §4, with no field containing a
   CR, LF, tab or NUL.

## 6. Post-conditions — asserted after writing, before the backup is released

1. Row count is exactly 30 + 35 = 65.
2. **Physical lines 1 through 31 are byte-identical to the original.** Not
   cell-identical — byte-identical, compared as raw lines. Manual §6.7 records that a
   cell-level check cannot see a line ending and passed while every line's bytes
   changed.
3. The file's line terminator and final-newline state are unchanged. The file is
   **CRLF with no trailing newline**; `csv.writer`'s defaults would write LF and add
   one, silently rewriting all 31 existing lines. The format is detected from the file
   and reproduced, never assumed.
4. Every one of the 35 new rows parses to exactly 13 fields.
5. The set of `paper_id` values in the file is exactly the original 30 plus the 35 new.
6. No DOI appears twice in the file.
7. The dataset is untouched: `data/raw/measurements_v0.1.csv` has the same sha256
   before and after. This migration must not touch it and asserts that it did not.

If any post-condition fails the original is restored from the backup and the script
exits non-zero.

## 6.1 Amendment, 2026-09-27: one pre-existing test file must change

**This section was added after the migration was applied and before it was
committed.** It is an amendment rather than a revision, and the reason it exists is
recorded rather than folded away.

Applying the migration broke **9 tests in `tests/test_sync_paper_tracking.py`**.
Manual §6.7 forbids editing an existing file under `tests/` except under a committed
migration plan, and this plan did not name that file, so the plan is amended here
before the edit is made.

Nothing about the failures indicates the migration is wrong. All nine are the hazard
§6.7 already names — *"a test that hardcodes the corpus's row count expires at the
next append"* — applied to the tracking file rather than to the dataset. Two causes:

1. **Two tests pin `len(rows) == 30` directly.** `test_the_tracking_file_shape_is_pinned`
   and `test_the_status_counts_account_for_every_row`. The second one's own docstring
   already says that pinning absolute counts here "was wrong: every append changes
   them, so the pin failed for reasons unrelated to what it was guarding" — and then
   leaves `== 30` in the assertion chain. The fix follows that docstring's own
   reasoning and removes the count, keeping the partition assertions, which hold at
   any corpus size.
2. **Seven tests drive `sync_paper_tracking.py` against a sandbox rebuilt from the
   real tracking file**, and that script's `--expected-rows` defaults to 30. With 65
   rows in the fixture the script correctly refuses. The fix is to make the test
   helper derive `--expected-rows` from the fixture it just built, rather than relying
   on a default that is a snapshot of one moment. Callers that pass their own value —
   including the two that deliberately pass `-1` — keep it.

A third test needed a change for the same reason: `test_the_script_refuses_a_wrong_row_count`
appended a row and then asserted the literal string `"expected 30 data rows"`. Once
the helper derives the count, that guard no longer fires by default. It now takes the
fixture's count *before* appending and passes it explicitly, so the test states the
mismatch it is testing instead of depending on a default that was a snapshot of one
moment. That is a stronger test, not a weaker one — it no longer passes or fails
according to how many papers happen to be tracked.

**No assertion is weakened.** The delta-based pins stay exactly as they are: `24 cell
change(s)` and `13 physical lines changed` are both deltas, which §6.7 says are the
right thing to pin, and both still hold. What is removed is one absolute total that
the neighbouring test had already identified as the wrong thing to assert.

**Verified by mutation, not by inspection.** Four guards that these tests cover were
removed one at a time from `sync_paper_tracking.py` in a scratch copy — the row-count
guard, the ragged-row guard, the already-applied guard, and `detect_format`'s CRLF
detection — and the edited file failed on all four. The harness asserted it was
loading the scratch copy's script before running, per §6.7's record of a mutation run
that tested nothing because the imports resolved back to the real tree.

## 7. What this migration deliberately does not do

- **It does not change `extraction_status` on any existing row.** Nothing about the
  existing 30 papers changed.
- **It does not resolve the two `extraction_date` staleness cases** noted in §18 item 4
  (HYC-0011 and HYC-0015 gained rows after their recorded extraction date). That is a
  separate concern about a column that cannot express "extracted then, added to since",
  and folding it in here would put two unrelated changes in one migration.
- **It does not mark any new paper `pdf_obtained = yes`.** No PDF has been obtained;
  that is Avin's step, and recording it in advance would assert something untrue.

## 8. Verification that the tests test something

Per manual §6.7, a migration script committed without its own test file is not
verified, and a passing suite is weak evidence. `tests/test_migrate_phase_d_screening.py`
carries a `MUTATION:` line on every test naming the defect it would catch, and
thirteen mutations were run against the finished script with the suite expected to
fail on each.

**The harness has its own guard.** Manual §6.7 records a mutation run in which all
eight mutations "survived" because the package was installed editable and the scratch
copy's imports resolved back to the real `src/`. This harness loads the script by
absolute path derived from the test file's own location, and the run asserts that
`mig.__file__` points inside the scratch copy before any mutation is applied. That
assertion is printed and passed.

**First round: 5 of 12 survived.** Every survivor was a test that passed for the
wrong reason, and in four of the five the script's behaviour was still safe — a
later check caught what the mutated one no longer did — so the tests were measuring
the outcome rather than the guard.

| # | Mutation | Round 1 | Round 2 |
| --- | --- | --- | --- |
| 1 | Remove the refuse-to-re-run guard (precondition 4) | survived | killed |
| 2 | Write with `csv.writer` defaults instead of the detected CRLF terminator | killed | killed |
| 3 | Append a trailing newline the original did not have | killed | killed |
| 4 | Compare parsed cells instead of raw bytes in post-condition 2 | survived | killed |
| 5 | Drop the physical-line-count precondition (5.3) | survived | killed |
| 6 | Let one new row carry 12 fields instead of 13 | killed | killed |
| 7 | Admit a DOI already present in the file | survived | killed |
| 8 | Skip the dataset-untouched assertion (post-condition 7) | survived | killed |
| 9 | Accept any `provenance.verdict` | killed | killed |
| 10 | Drop the control-character guard | killed | killed |
| 11 | Do not restore the backup on post-condition failure | killed | killed |
| 12 | Let `--dry-run` fall through to the write | killed | killed |
| 13 | Take the dataset baseline sha late again (see below) | — | killed |

What each survivor needed:

- **1 and 7** — the tests re-used the same screening file, so a second check
  (duplicate DOI, row count) fired instead of the one under test. Fixed by giving
  the re-run fresh DOIs so only the id guard can catch it, and by asserting the
  refusal is a *precondition* (`refusing:` on stderr, file unchanged) rather than
  merely a non-zero exit.
- **4** — the happy path writes correct bytes, so no end-to-end test can distinguish
  a byte comparison from a cell comparison. Fixed with a test that drives `verify()`
  directly against a line re-quoted as `,"Carbon",` instead of `,Carbon,` — identical
  parsed cells, different bytes.
- **5** — with the precondition gone, `verify()`'s line-count check caught the
  embedded newline after the write, and its message also contains the phrase the
  test matched on. Fixed by asserting `post-condition` is *absent* from stderr.
- **8** — the script never writes the dataset, so removing the assertion changes
  nothing on the happy path. Fixed with a test that monkeypatches `render_new_lines`
  to corrupt the dataset mid-run and requires the migration to fail and restore.

### 8.1 A defect the mutation round found in the script itself

Writing the test for mutation 8 exposed a real ordering bug: `dataset_sha_before` was
computed **after** `render_new_lines`, immediately before the write. Anything that
touched `data/raw/measurements_v0.1.csv` earlier in the run would have been hashed in
the baseline, so post-condition 7 would have compared the corrupted file against
itself and passed. The baseline is now taken as the first action in `main()`, and
mutation 13 pins that ordering.

This is the second time in this project that a guard has been found to be checking
after the thing it guards against could already have happened, and it was found by
writing a test that made the guarded event actually occur rather than by reading the
code. A mutation that cannot be made to fire is not evidence that the guard works.
