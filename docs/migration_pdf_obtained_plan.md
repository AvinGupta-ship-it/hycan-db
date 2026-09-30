# Migration plan — record which Phase D full texts were obtained

**Status:** planned 2026-09-30, before any code was written or any file touched.
**Applied 2026-09-30.** 35 cell changes, 35 of 66 physical lines rewritten, all
inside the Phase D block; header and the 30 pre-Phase-D lines byte-identical;
CRLF and the absent trailing newline preserved; `pdf_obtained` 53 yes / 12 no,
Phase D 30 / 5. Verified by reading the file back and diffing it against
`HEAD`, not from the script's own report. Result sha256
`a2392af29fa28d617f4c5edc62faaf55c16e6563c34b542fb76bdc83ce29e979`.

**§3 was wrong when written and is corrected below** (§3.1). It said the loss
landed "almost entirely on one funnel target". It lands on two.
**Target file:** `references/paper_tracking.csv` (protected under manual §6.7)
**Script:** `scripts/migrate_pdf_obtained.py`
**Tests:** `tests/test_migrate_pdf_obtained.py`
**Manual authority:** §9.1 step 15 (update tracking), §7.5 (PRISMA), §7.4 (bias guard),
§6.7 (protected files, byte-level verification)

---

## 1. Why

`scripts/migrate_phase_d_screening.py` wrote all 35 Phase D rows with
`pdf_obtained = no`, which was true when it ran. **30 of the 35 full texts have
since been obtained** and are in the Project; 5 were not. The tracking file is
the source of truth (§5.2) and currently says none of them were.

§9.1 step 15 — update the tracking file — is the step this project has skipped
most often. It went unrecorded for ten consecutive papers in Phase C, and again
one commit after that was fixed. Doing it before extraction starts, rather than
after, is the cheap moment.

## 2. Scope

For the **30 obtained**: `pdf_obtained` `no` → `yes`.

For the **5 not obtained**: `pdf_obtained` stays `no`, and `notes` gains a
trailing clause recording that the full text was not retrieved, with the date and
the reason.

Nothing else changes. No `screening_decision`, no `extraction_status`, no
`extraction_date`, no row added or removed, and nothing outside the 35 Phase D
rows is touched at all.

## 3. The five, and why this is not a neutral loss

| ID | Paper | Journal |
| --- | --- | --- |
| HYC-0035 | Li 2016 | *RSC Advances* |
| HYC-0036 | Wang 2010 | *Energy & Environmental Science* |
| HYC-0054 | Masika & Mokaya | *Energy & Environmental Science* |
| HYC-0055 | Wang 2012 | *J. Mater. Chem.* |
| HYC-0056 | Balahmar & Mokaya | *J. Mater. Chem. A* |

**All five are Royal Society of Chemistry titles.** That is not a random 14% of
the candidate set going missing; it is a systematic exclusion by publisher, and
§7.4's bias guard is explicit that a corpus shaped by what was easy to obtain
inherits a bias the meta-analysis will then report as a finding.

**It lands almost entirely on one funnel target.** Three of the five are the
`volumetric` papers, taking that target from 5 to 2. Volumetric capacity was
already the corpus's thinnest field — schema gap 10 added the columns and exactly
one paper (HYC-0024) populates them — and Phase D selected those four papers to
broaden precisely that. After this, it stays exercised by two papers' conventions.

The other two are `doped_77K`, which survives at 9 of 11 and is no longer a
blocker.

### 3.1 Correction — it lands on two targets, not one

Written 2026-09-30, after the migration was applied, on recomputing coverage per
funnel tag from `references/phase_d_screening.json` rather than from the note
above. The paragraph above is wrong and is left in place under §2.4.

The three `volumetric` losses are tagged `new_group;volumetric` — the *same three
papers* were the `new_group` candidates. So `new_group` drops from 18 screened to
15 obtained, and that is the target §5.2 of `docs/corpus_audit.md` ranks second
overall, on the grounds that the binding constraint on cross-validation is the
count of groups (11) and not the count of rows (102).

Stated at the precision the evidence supports: `new_group` is a *screening* tag
meaning "plausibly a research group not already in the corpus". Whether a paper
actually adds a group to the 77 K + BET subset is not known until extraction —
Phase C.1 added two papers tagged for that subset and moved the group count by
zero. So the loss is 3 of 18 candidate new groups, not 3 groups.

| target | screened in | obtained | lost |
| --- | --- | --- | --- |
| `new_group` | 18 | 15 | HYC-0054, HYC-0055, HYC-0056 |
| `77K_BET` | 16 | 14 | HYC-0035, HYC-0036 |
| `doped_77K` | 11 | 9 | HYC-0035, HYC-0036 |
| `low_uptake` | 7 | 7 | — |
| `volumetric` | 5 | 2 | HYC-0054, HYC-0055, HYC-0056 |
| `doped_other` | 4 | 4 | — |
| `classic` | 3 | 3 | — |

Tags are not exclusive, so the columns do not sum to 35.

**This must be reported, not absorbed.** §7.5 requires PRISMA counts to carry
"full text not retrieved" as its own number, and `docs/corpus_audit.md` §5.4 and
any eventual data descriptor have to say that the volumetric field is thin
*because of retrieval*, not because the literature is thin. A reader who is told
the corpus has 2 volumetric papers, and not told that 3 more were identified and
could not be obtained, is being given a biased picture with no way to detect it.

## 4. Preconditions

1. Header is the expected 13 columns.
2. Exactly 65 data rows (overridable with `--expected-rows`, so the script is
   testable against a fixture — Appendix A.5).
3. Physical line count equals rows + 1, so the byte check in §5 is sound.
4. All 35 Phase D ids are present.
5. **Refuse to re-run:** if any of the 30 already reads `pdf_obtained = yes`.
6. Every id named in the migration exists exactly once.

## 5. Post-conditions

1. Row count unchanged at 65.
2. **Every physical line outside the 35 Phase D rows is byte-identical**, compared
   as raw lines, not parsed cells.
3. Line terminator (CRLF) and final-newline state (absent) unchanged.
4. Exactly 30 rows changed `pdf_obtained` to `yes`; exactly 5 kept `no`.
5. `pdf_obtained` across the file is only ever `yes` or `no`.
6. No cell outside the `pdf_obtained` and `notes` columns changed, on any row.
7. `data/raw/measurements_v0.1.csv` sha256 unchanged, baselined as the **first**
   action in `main()` — the ordering defect found in
   `migrate_phase_d_screening.py`, where the baseline was taken late enough that
   the guard would have hashed an already-corrupted file.

## 6. Mutations the tests must kill

1. Remove the refuse-to-re-run guard.
2. Write with `csv.writer` defaults instead of the detected CRLF.
3. Compare parsed cells instead of raw bytes.
4. Mark all 35 obtained rather than 30.
5. Change a cell in a column the plan does not name.
6. Touch a row outside the Phase D block.
7. Skip the dataset-untouched assertion.
8. Drop the physical-line-count precondition.

A mutation that does not cause a failure is a gap in the tests, not a pass.
