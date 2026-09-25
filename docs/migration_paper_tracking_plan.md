# Migration plan — `references/paper_tracking.csv`

**Status:** written and committed before any change to the file, as
execution manual §6.7 requires for a protected file.
**Date:** 2026-09-25
**Applied by:** `scripts/sync_paper_tracking.py` (committed; refuses to re-run)
**Target file:** `references/paper_tracking.csv` — and nothing else.

---

## 0. Why this migration exists

Manual §5.2 designates `references/paper_tracking.csv` the **source of truth**
for paper tracking, and §9.1 step 15 requires `extraction_status` and
`extraction_date` to be set directly in it as each paper completes.

Step 15 was skipped for the whole of Phase C, and partially skipped earlier.
The file therefore contradicts the dataset it is supposed to track. This was
found by an independent audit of execution manual v2.3 against the repository,
not by the pipeline that was supposed to maintain it — which is the more
important finding and is addressed in §5 below.

## 1. The measured discrepancy

`references/paper_tracking.csv` holds 30 rows. `data/raw/measurements_v0.1.csv`
holds 21 papers. Comparing them:

| Defect | Count | Detail |
| --- | --- | --- |
| Extracted papers recorded `not_started` | 10 | Every Phase C paper |
| Rows with `extraction_status = extracted` but no `extraction_date` | 3 | HYC-0016, HYC-0018, HYC-0023 |
| Rows with a malformed `paper_id` | 1 | `HYC-009` for Ioannatos 2010, one digit short of the `HYC-XXXX` pattern §8.2 requires |
| Rows recorded `verified` | 0 | Ten papers completed the dual-agent protocol |

Current state: 11 `extracted`, 19 `not_started`, 0 `verified`.

## 2. What `verified` means, decided here

§5.2 says: "Under v2.0, `verified` means the dual-agent protocol completed with
all disputes resolved." That definition is kept and is now applied literally,
which settles the only judgment call in this migration:

- **The 10 papers extracted under the v2.0 dual-agent protocol become
  `verified`.** All 85 of their rows carry `extractor = "HyCAN pipeline v2"`
  with `verified_by` and `verification_date` populated, and every dispute is
  resolved and recorded in `docs/extraction_provenance.md`.
- **The 11 papers extracted under the v1.0 human protocol stay `extracted`.**
  They were read once, by one reader, and `verified_by` is empty on all 121 of
  their rows. Marking them `verified` would assert a second reading that never
  happened. `extracted` is the honest value.

This is the substantive decision in this plan, and it is deliberately the
conservative one: the field is a claim about verification, and a corpus where
`verified` means two different things depending on the row is worse than one
where 121 rows honestly say they were read once.

The two groups, enumerated so the script cannot drift from this plan:

```
verified  (10): HYC-0009 HYC-0011 HYC-0012 HYC-0015 HYC-0017
                HYC-0019 HYC-0022 HYC-0025 HYC-0026 HYC-0029
extracted (11): HYC-0001 HYC-0002 HYC-0004 HYC-0005 HYC-0013
                HYC-0016 HYC-0018 HYC-0020 HYC-0021 HYC-0023 HYC-0027
```

## 3. The changes, cell by cell

Nothing outside these cells is touched. The 9 screened-but-not-extracted rows
are not modified at all.

**3.1 — `paper_id`: one cell.** `HYC-009` → `HYC-0009`. The row is Ioannatos &
Verykios 2010, which the dataset carries as HYC-0009 across 20 rows. The
malformed ID is why a naive ID-matching fix would have silently skipped this
paper, and it is corrected first so the status update below can match it.

**3.2 — `extraction_status`: ten cells.** The ten papers in §2's `verified`
list: `not_started` → `verified`.

**3.3 — `extraction_date`: thirteen cells.** Set where empty, from the dated
section header of the paper's extraction entry in `docs/ai_usage_log.md`. Dates
already present are not changed.

| Paper | Date | Source |
| --- | --- | --- |
| HYC-0009, 0011, 0012, 0015, 0017, 0019, 0022, 0025, 0026, 0029 | 2026-09-25 | Phase C entries |
| HYC-0016 | 2026-08-30 | `## 2026-08-30 — Paper extraction: HYC-0016 (Klechikov et al. 2015)` |
| HYC-0018 | 2026-08-31 | `## 2026-08-31 — Paper extraction: HYC-0018 (Singh & De 2020)` |
| HYC-0023 | 2026-08-30 | `## 2026-08-30 — HYC-0023 (Gogotsi et al. 2009) extraction` |

**3.4 — `screening_decision`.** Confirmed already `include` on all 21 dataset
papers. No change. Asserted by the script rather than assumed.

## 4. Method and verification

Following §6.7 and the precedent of `migrate_v1_1.py` and `migrate_v1_2.py`:

- **Raw CSV cells, not a pandas round-trip.** The script reads with the `csv`
  module and writes the same way, so every cell it does not name is
  byte-identical by construction and the verification can assert exactly that.
- **Refuses to re-run.** If the ten papers already read `verified`, it exits
  non-zero without writing.
- **`--dry-run`** prints the diff and writes nothing.
- **Backs up** to `/tmp` with a dated name before writing.
- **`--expected-rows`** is a CLI option rather than a constant, so the script is
  testable against a fixture. A migration whose correctness rests on one
  irreversible attempt is not verified.

### 4.1 The first attempt rewrote every line, and the cell check did not notice

Recorded because it is the same class of failure as everything else this session
found, and because the fix is now a reusable guard.

`references/paper_tracking.csv` is **CRLF with no trailing newline**. The first
version of this script wrote it back with `csv.writer`'s defaults: LF, plus a
final newline. Every cell value was correct and `verify()` passed — it compares
parsed cells, and a parsed cell cannot see its own line ending. But the bytes of
all 30 lines changed, so `git diff` showed a whole-file rewrite where the plan
promised 13 changed lines. On a protected file, a diff nobody can read is a
review nobody can perform.

Two changes, both kept:

- `detect_format()` reads the terminator and the final-newline state from the
  file's own bytes and `write_rows()` reproduces them. The convention is detected,
  never assumed.
- `assert_untouched_lines_are_byte_identical()` compares **raw lines**, not
  cells, and refuses if any line outside the plan's scope changed bytes. This is
  the check that would have caught the defect, and it is the one that runs now.

The general rule, which belongs in the manual and not only here: **a cell-level
verification cannot certify a byte-level guarantee.** A migration that promises
byte-identical untouched cells has to compare bytes.

Post-conditions the script asserts, and which `tests/test_sync_paper_tracking.py`
asserts independently:

1. Row count unchanged at 30; column count and header unchanged at 13.
   Physical line count unchanged at 31; line terminator and final-newline state
   unchanged.
2. Exactly 24 cells changed across exactly 13 physical lines: 1 `paper_id`, 10
   `extraction_status`, 13 `extraction_date`. Every other cell byte-identical to
   the pre-image, asserted at the byte level as well as the cell level.
3. Every `paper_id` matches `^HYC-\d{4}$`.
4. Every paper in the dataset has a tracking row whose `extraction_status` is
   `extracted` or `verified`, and a non-empty `extraction_date`.
5. No paper absent from the dataset is `extracted` or `verified`.
6. Final counts: 11 `extracted`, 10 `verified`, 9 `not_started`.
7. `data/raw/measurements_v0.1.csv` is not opened for writing. Its sha256 is
   `3ecc8b63d9a17ad6980602bc03c4da2150f0b3a4cbcb6335d7ed3ab5d1701676` before
   and after.

## 5. The real defect this exposes, and the fix

Updating the file is the small half of this. The large half is that **§9.1 step
15 is a manual step in an otherwise automated pipeline, and it was skipped ten
times in a row without anything noticing.** A rule that is followed only when
someone remembers it is not a rule; it is a hope.

Two changes, both of which outlast this migration:

1. **`tests/test_dataset_invariants.py` gains a tracking-consistency test.**
   It already asserts against the real dataset, which makes it the right place:
   every `paper_id` in `measurements_v0.1.csv` must have a tracking row that is
   `extracted` or `verified` with a non-empty `extraction_date`, every
   `paper_id` in the tracking file must match `^HYC-\d{4}$`, and a paper whose
   rows all carry `extractor = "HyCAN pipeline v2"` must be `verified`. After
   this, skipping step 15 fails the suite instead of going unnoticed for a
   phase.
2. **`scripts/append_paper.py` should warn** when the paper it just appended is
   not `extracted` or `verified` in the tracking file. Not an error — the append
   and the tracking update are legitimately separate actions — but the append is
   the moment the discrepancy is created, and it is the cheapest place to
   surface it. Deferred to the next scripts change rather than bundled here, so
   this migration touches one data file and one test file and nothing else.

Change 1 ships with this migration. Change 2 is recorded in manual §18.
