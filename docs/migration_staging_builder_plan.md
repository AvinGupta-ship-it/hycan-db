# Plan — a reusable staging builder

**Status:** planned 2026-10-01, before any code was written
**Script:** `scripts/build_staging.py`
**Specs:** `references/staging/HYC-XXXX.json`
**Tests:** `tests/test_build_staging.py`
**Manual authority:** §9.1 step 10 (staging file), §6.7 (physical column order,
byte-level verification), §3.5 (nothing derived silently)

---

## 1. Why

Two consecutive execution-log entries have named the same bottleneck.

After HYC-0007 and HYC-0024 (2026-09-26):

> "Row construction is now the bottleneck rather than reading: a 67-column
> builder script with long `notes` strings took longer than either the locate
> pass or the verification. **A staging helper that took per-sample values as a
> table and a shared note block would cut it.**"

After HYC-0031 (2026-09-30):

> "Row construction again, as the HYC-0007/0024 entry predicted — and the
> staging-helper it recommended was still not built, so the same 67-column
> builder script was written from scratch."

Three sessions have now each written a throwaway 67-column builder. 29 Phase D
papers remain. This is the one per-paper cost that tooling can remove, and the
recommendation is two entries old.

It is also where the CRLF defect came from. HYC-0031's throwaway builder hard-coded
`lineterminator="\r\n"` because its author had just examined
`references/paper_tracking.csv`, which is CRLF, and assumed
`data/raw/measurements_v0.1.csv` matched. It does not. A shared builder that
reads the terminator from the dataset makes that class of error impossible
rather than merely detected.

## 2. What it is

A per-paper **spec** in JSON, and one script that turns it into a validated
staging CSV. The spec holds exactly what a human decided; everything mechanical
is the script's job.

```
{
  "paper":        paper-level cells, written once
  "defaults":     cells that are the same on every row
  "notes":        named note fragments, written once and referenced by key
  "samples":      per-sample characterisation, written once per sample
  "measurements": one entry per (T, P, uptake) point
}
```

A sample's cells are inherited by every measurement of that sample. A
measurement may override any of them. `notes` keys resolve to text and join in
the order given, so the long shared paragraphs are written once instead of 32
times — which is the specific thing the 2026-09-26 entry asked for.

## 3. What the script must do, and why each one

1. **Read the column order from the dataset header at run time.** Never
   hard-coded. §6.7: the staging file uses the CSV's *physical* order, and a
   schema change must not silently shift a value into the wrong column.
2. **Read the line terminator from the dataset** and write with it. This is the
   HYC-0031 defect made impossible rather than caught.
3. **Auto-number `measurement_id`** as `{paper_id}-M{n}` in spec order, and
   derive `sample_id` as `{paper_id}-{sample_key}`. Hand-numbering 32 ids is
   error-prone and carries no information.
4. **Refuse an unknown key** anywhere in the spec. A mistyped field name that
   silently drops its value is the worst failure this format allows, because
   the output still validates.
5. **Validate every row through `schema.py`** before writing anything, and
   refuse on any error. The schema is the authority (§9.1 step 7), and a
   staging file that cannot validate should never reach disk.
6. **Derive nothing.** No unit conversion, no inference, no defaulting a
   condition. If a cell is not in the spec it is empty. §3.5.
7. **Refuse a duplicate `measurement_id` or an id that already exists in the
   dataset**, so a re-run cannot collide.

## 4. Preconditions

1. The dataset exists and its header parses to the expected column count.
2. Every `measurements[].sample` names a key present in `samples`.
3. Every `notes` key referenced is defined.
4. `paper_id` matches `HYC-\d{4}` (§8.2 — one paper was once written `HYC-009`,
   one digit short, and an id-matching repair silently skipped it).
5. No spec cell names a column absent from the dataset header.

## 5. Post-conditions

1. The staging file's column order equals the dataset's, exactly.
2. Its line terminator set equals the dataset's, exactly.
3. Row count equals `len(measurements)`.
4. Every row validates against `MeasurementEntry` with zero errors.
5. `measurement_id`s are unique and absent from the dataset.
6. No cell contains a CR, LF, tab or NUL — the control characters that break
   the byte-level checks every later append depends on (§6.9).

## 6. The regression that proves it works

**`references/staging/HYC-0031.json` is derived from the 32 rows now committed,
and the test asserts that the builder reproduces them cell for cell.**

That is the strongest check available: it demonstrates the tool on real work
rather than on a fixture shaped to suit it. If the builder cannot reproduce a
paper that was extracted by hand, it is not a replacement for the hand method.

The spec is generated *from* the committed rows programmatically rather than
retyped, so it cannot drift from them through transcription.

## 7. Mutations the tests must kill

1. Hard-code the column order instead of reading the dataset header.
2. Hard-code the line terminator.
3. Accept an unknown key in the spec.
4. Skip schema validation.
5. Write the file before validating.
6. Accept a `measurement_id` that already exists in the dataset.
7. Accept a duplicate `measurement_id` within the spec.
8. Let a measurement silently fail to inherit its sample's cells.
9. Resolve note keys in the wrong order, or drop an unresolved key silently.
10. Accept a control character in a cell.
11. Accept a `measurements[].sample` that names no defined sample.
12. Number `measurement_id` from something other than spec order.

A mutation that does not cause a failure is a gap in the tests, not a pass.

## 8. Not in scope

Tier assignment. `reproducibility_tier` is a human judgment informed by
`score_reproducibility` and §13, with the extractor's adjustments recorded; the
spec carries it as a value the human supplies, and the builder never computes
it. The spec may leave it empty, which is the state a staging file is in between
§9.1 steps 8 and 10.
