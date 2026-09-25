# Schema v1.1 Migration Plan

Written before any protected file is touched, per §6.7. Closes the four gaps
in manual §8.5 and the two cleanups in §8.6, in one migration, per §8.5.

Baseline: commit `ca737dc`, `data/raw/measurements_v0.1.csv` at 119 rows,
11 papers, sha256 `55875a906d565df37d3bae32e304fbb39b7d02c1d52b7a17c27df9f187f156d5`,
0 errors, warning types `Unspecified uptake_type ×96` and
`mmol/g and wt% inconsistent ×1`.

## Files this migration is permitted to touch

`src/hycan/schema.py`, `src/hycan/validate.py`, `docs/data_dictionary.md`,
`data/raw/measurements_v0.1.csv`, `CHANGELOG.md`, `tests/test_schema.py`,
`tests/test_validate.py`, and new files under `scripts/` and `tests/`.
Nothing else.

## 1. Schema changes

**Gap 1 — `surface_area_method`.** New controlled field, `Literal["BET",
"Langmuir", "geometric", "DFT", "unspecified", "none"]`, default
`"unspecified"`. Unblocks HYC-0025, which reports one unqualified "surface
area".

**Gap 2 — `carbide_chlorination`.** Added to the `SynthesisMethod`
vocabulary. Per §8.7, adding a value is permitted and requires no row
migration except the rows being corrected.

**Gap 3 — conditional temperature and pressure.** `temperature_k` and
`pressure_bar` become `Optional`. Two cross-field rules replace the current
unconditional requirement:

- A row with any uptake value (`uptake_wt_pct`, `uptake_mmol_g`,
  `uptake_ml_stp_g`) must carry both `temperature_k` and `pressure_bar`, and
  must still carry at least one of `uptake_wt_pct` or `uptake_mmol_g`. That
  second clause is the existing §8.2 rule, preserved.
- A row with no uptake value must carry at least one characterization value.
  A row with neither asserts nothing and is rejected.

**Gap 4 — `ultramicropore_volume_cm3_g`.** New optional float, 0–2, for pore
volume below the ~0.7 nm cutoff. The cutoff is a property of the source
paper's method and is documented in the data dictionary rather than enforced.
New cross-field check, ERROR severity: `ultramicropore ≤ micropore ≤ total`,
evaluated pairwise so that a missing middle term does not suppress the
outer comparison.

## 2. Column order

Both new columns are appended at the **end** of the CSV, at physical
positions 39 and 40, matching how `measurement_id` and `uptake_ml_stp_g` were
added (§6.7). Positional appends continue to work; `schema.py` declaration
order continues to differ from physical order, as §6.7 documents.

## 3. Row backfills — what is determinable here, and what is not

**Determinable from data already in the dataset, done in this migration:**

| Change | Rows | Basis |
| --- | --- | --- |
| `synthesis_method` `other` → `carbide_chlorination` | 23 (HYC-0023) | every `material_description` reads "TiC-derived CDC, chlorinated at N C" |
| `material_class` `graphene` → `reduced_graphene_oxide` | HYC-0016 samples S1–S10, S12 | every `material_description` reads "Reduced graphene oxide, BET N m2/g" |
| `surface_area_method` → `BET` | every row with `bet_surface_area_m2_g` populated | the field is BET by definition; the extractor placed the value there |
| `surface_area_method` → `unspecified` | all other rows | default; no claim made |

**Not determinable without the source PDF. Deferred to a second commit, and
requested as one batch per §7.4:**

| Change | Rows | Why it needs the paper |
| --- | --- | --- |
| `ultramicropore_volume_cm3_g` backfill | 6 (HYC-0021, Sethia 2016) | 3 of 6 values appear in row `notes` (0.27, 0.21, 0.0 cm³/g, Table 2); 3 do not. §8.5 says backfill from the source, and a partial backfill from second-hand notes is worse than none |
| recover 2 characterization-only rows | HYC-0018 (Singh 2020) | the dropped rows are not in the dataset in any form |
| `extraction_confidence` reassessment | 25 (HYC-0005, Texier-Mandoki 2004) | §8.6 asks whether a total surface area was entered into the BET field; only the paper says |

**HYC-0016-S13** is described as "Thermally exfoliated graphene oxide" rather
than "Reduced graphene oxide". Thermal exfoliation reduces GO, so
`reduced_graphene_oxide` is defensible, but the description does not say so in
the words the other twelve use. It is left as `graphene` and listed with the
PDF batch rather than relabelled on inference.

## 4. Verification, per §8.7

In the same commit: schema edit, matching `docs/data_dictionary.md` section,
new tests, `CHANGELOG.md` entry, and a full revalidation showing:

- row count exactly 119, unchanged
- 0 errors
- no warning type absent from the baseline
- 40 columns, with positions 1–38 unchanged in name and order
- every pre-existing cell value unchanged except the 23 + 11 relabels above

The revalidation is run against the file on disk, not against an in-memory
frame (§3.8). A diff of the old and new CSV restricted to columns 1–38 must
show exactly 34 changed cells and nothing else.

## 5. Rollback

The migration is applied by a committed script under `scripts/`, not by hand
edits, so it is reproducible and reversible. The pre-migration dataset is
recoverable from `ca737dc` at any time.
