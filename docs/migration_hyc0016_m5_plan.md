# Migration plan — correct HYC-0016-M5 (reference activated carbon mislabeled as KOH-activated r-GO)

**Status:** written and committed before the protected file is touched, per §6.7.
**Date:** 2026-10-07
**Applied by:** `scripts/migrate_hyc0016_m5.py` (committed; refuses to re-run)
**Target file:** `data/raw/measurements_v0.1.csv` — and nothing else. No schema
change; no new columns; no row added or removed. Corpus stays at 521 rows and 67
columns.

**Companion change, same commit:** `scripts/migrate_relabel.py` is edited to
remove `HYC-0016-M5` from `_CHEMICAL_ACTIVATION["HYC-0016"]`. M5 was never a
chemically-activated r-GO sample, so it should never have been in that
migration's relabel map; it was swept in on its (also wrong) `activation_method`
value — the exact §6.7 "a text-match relabel catches a reference sample" hazard
that `MUST_NOT_CHANGE` guards HYC-0001 and HYC-0004 against. Removing it drops
`SYNTHESIS_RELABEL` from 36 rows to 35. See §4.

---

## 0. Why

`HYC-0016-M5` is coded `reduced_graphene_oxide` / `chemical_activation` /
`koh_activation`, with `material_description` "Reduced graphene oxide, BET 1830
m2/g". It is in fact the paper's **reference activated carbon** — the same
physical sample as `HYC-0016-M11`, measured at 293 K (Fig. 3) rather than 77 K
(Fig. 4).

Three independent lines of evidence, none relying on the others:

**1. The paper's own figure captions.** Klechikov et al. 2015 measure a
commercial reference activated carbon alongside the graphene samples and plot it
in both isotherm figures. Fig. 3 (293 K gravimetric): *"reference sample of
activated carbon highlighted by red color."* Fig. 4 (77 K volumetric):
*"Isotherm recorded from reference sample of activated carbon is shown by red
symbols."* Fig. 5 legend: *"AC — reference activated carbon."* So the 293 K
isotherm set digitized into M1–M5 **contains** the reference carbon; one of
M1–M5 is it.

**2. The 77 K twin fixes which one.** A reference sample is a single physical
material with one BET area, measured at both temperatures to anchor the
comparison across panels. At 77 K it is `HYC-0016-M11`, BET **1830 m²/g**
(correctly coded `activated_carbon` at extraction). The only 293 K point at BET
1830 is **M5**. BET is a property of the sample, not the measurement
temperature, so the reference carbon appears at 1830 in both figures: M5 (293 K)
and M11 (77 K) are the same sample. The surrounding 293 K points are genuine
r-GO (M1 310, M2 560, M3 1250, M4 1740 m²/g), and M3/M4 are legitimately
KOH-activated — only M5 is the mislabeled reference.

**3. The dual-agent verification pass flagged it independently.** On 2026-10-05
an isolated Agent B re-read Figs. 2–5 blind to the extraction reasoning and
recorded, on both M5 and M11: *"the BET-1830 293 K row (M5) is the reference
activated carbon (same sample as the 77 K AC row M11), mislabeled
reduced_graphene_oxide/KOH here and in scripts/migrate_relabel.py."* It was left
uncorrected at the time only to avoid rewriting `migrate_relabel.py` mid-pass,
and recorded in `docs/known_limitations.md` as owed. This migration is that
correction.

**Physical consistency check (not evidence, a sanity bound).** The paper states
ambient uptake of ~0.3 wt% per 1000 m²/g at 100 bar; 1830 m²/g → ~0.55 wt%, and
M5 reads 0.627 wt% at 124.5 bar. At 77 K, 1830 m²/g → ~3.7 wt% on the Chahine
rule, M11 reads 4.36. Both consistent with an activated carbon of that area.

**Why correct it rather than leave it documented.** It is a verified label
error with an unambiguous fix, not a scientific ambiguity. The row is invisible
to every headline result (all 77 K; M5 is 293 K) and to the ML model, so this
does not move a single published number — but a dataset that ships a row it
knows is wrong, when the correct values are in hand, is not "done to the best of
our ability."

## 1. Scope — the fields that change on M5

M5 and M11 are the same physical sample, so the **sample-identity** fields must
match M11. The **measurement** fields legitimately differ (M5 is the 293 K
gravimetric point, M11 the 77 K volumetric point) and are **not** touched.

| Column | From (M5 now) | To (= M11) |
|---|---|---|
| `material_class` | `reduced_graphene_oxide` | `activated_carbon` |
| `synthesis_method` | `chemical_activation` | `other` |
| `activation_method` | `koh_activation` | `none` |
| `material_description` | `Reduced graphene oxide, BET 1830 m2/g` | `Reference activated carbon sample, BET 1830 m2/g` |

**Not touched on M5**, and why each legitimately differs from M11:
`temperature_k` 293 (vs 77), `pressure_bar` 124.5 (vs 38.7), `uptake_wt_pct`
0.627 (vs 4.36), `measurement_method` gravimetric_microbalance (vs
volumetric_sieverts — 293 K Rubotherm vs 77 K Hiden IMI), `uncertainty_wt_pct`
0.02 (stated only for the gravimetric balance; blank on the volumetric row),
`source_location` Figure 3 (vs Figure 4), `sample_id` S5 (per-measurement id;
unifying physical-sample ids across the paper is a separate, analysis-irrelevant
cleanup and is out of scope). `bet_surface_area_m2_g` is already 1830 on both
and `reproducibility_tier` already B on both — no change needed.

## 2. The notes edit on M5

M5's current `notes` describe only the digitization provenance and do not assert
r-GO or KOH, so they do not contradict the corrected fields. But a reader seeing
an `activated_carbon` row at 293 K in a graphene paper needs the same
explanation M11 carries. The migration **prepends** a sentence mirroring M11 and
recording the correction, leaving the existing provenance sentence intact:

> Paper's internal reference sample of activated carbon, not a graphene
> material; shown in red in Fig. 3 (the 293 K gravimetric isotherms) and the
> same physical sample as the 77 K reference-carbon row HYC-0016-M11 (both BET
> 1830 m2/g). Reclassified from reduced_graphene_oxide / chemical_activation /
> koh_activation to activated_carbon / other / none by
> scripts/migrate_hyc0016_m5.py (docs/migration_hyc0016_m5_plan.md) after the
> 2026-10-05 dual-agent verification identified the original label as the
> reference carbon mislabeled as KOH-activated r-GO; the row was also removed
> from scripts/migrate_relabel.py's KOH relabel scope in the same change.

## 3. The verified_by edit on all 14 HYC-0016 rows

`verified_by` holds the paper-level verification record, duplicated verbatim on
every HYC-0016 row, and it carries a sentence that now goes stale — it says the
mislabel is present "here and in scripts/migrate_relabel.py" and was "left
uncorrected." After this migration that is false, and on M5 it would directly
contradict the row's corrected class. The migration replaces that one sentence
wherever it occurs — all **14** HYC-0016 rows — so the paper's record stays
uniform rather than splitting into "corrected" and "left uncorrected" halves. The
rest of each `verified_by` record is untouched:

- Old (on both M5 and M11): *"FLAGGED for a dedicated relabel migration: the
  BET-1830 293 K row (M5) is the reference activated carbon (same sample as the
  77 K AC row M11), mislabeled reduced_graphene_oxide/KOH here and in
  scripts/migrate_relabel.py (SYNTHESIS_RELABEL); left uncorrected to avoid
  rewriting that migration."*
- New: *"The BET-1830 293 K row (M5) is the reference activated carbon (same
  sample as the 77 K AC row M11); the verification pass found it mislabeled
  reduced_graphene_oxide/KOH both in the dataset and in
  scripts/migrate_relabel.py, and scripts/migrate_hyc0016_m5.py
  (docs/migration_hyc0016_m5_plan.md) subsequently corrected M5 to
  activated_carbon/other/none and removed it from that migration's scope."*

## 4. The companion edit to migrate_relabel.py

`migrate_relabel.py` currently maps `HYC-0016-M5 → chemical_activation`. Because
M5's committed `synthesis_method` becomes `other` here, that mapping must go, or
the migration's round-trip test (`migrate_relabel(pre-image) == committed`) would
re-set M5 to `chemical_activation` and diverge. The edits:

- Remove `"M5"` from `_CHEMICAL_ACTIVATION["HYC-0016"]` →
  `("M3", "M4", "M8", "M9", "M10", "M12")`.
- `EXPECTED_SYNTHESIS_DELTAS`: `chemical_activation` +34 → **+33**, `other` −13 →
  **−12** (M5 was pre-migration `other` → `chemical_activation`; dropping it
  removes one of each move). `carbonization` −23 and `physical_activation` +2 are
  unchanged. Balance: out 12+23 = 35, in 33+2 = 35 = new `len(SYNTHESIS_RELABEL)`.
- `DEFAULT_EXPECTED_CHANGED_CELLS` 70 → **69** (one fewer `synthesis_method`
  cell: 35 synthesis + 3 metal_element + 3 metal_loading + 2
  dopant_concentration_method + 1 dopant_concentration_at_pct + 25 notes = 69).
- Docstring "36 synthesis_method cells" → "35", with M5's exclusion recorded.

`migrate_relabel.py`'s `MUST_NOT_CHANGE` is **paper**-scoped and HYC-0016 still
has six rows that must be relabelled (M3, M4, M8, M9, M10, M12), so M5 cannot be
guarded there. The guard against re-adding M5 is the round-trip test plus the
`len == 35` and delta pins, each of which fails if M5 re-enters the map.

## 5. Mechanics (same architecture as migrate_relabel.py)

Raw-CSV cell edits through the `csv` module, never pandas, so every cell this
script does not name is byte-identical by construction. Preconditions assert the
column count (67), that M5 and M11 exist, that the 14 HYC-0016 rows all carry the
stale flag, and that M5 currently holds the exact "From" values in §1 (refusing
to run twice, since after one run M5 no longer holds them). Post-conditions
assert: only the six scoped columns changed (`material_class`,
`synthesis_method`, `activation_method`, `material_description`, `notes`,
`verified_by`); exactly 19 cells changed (M5's 6 plus `verified_by` on the other
13 rows); M5 now equals M11 on all four identity fields; the old flag is gone and
the corrected text is on all 14 HYC-0016 rows; no row's fields still carry the
old M5 signature. The file is
re-read from disk and re-verified after writing, and every physical line the plan
does not name is asserted byte-for-byte unchanged (§3.8: a self-report is not
evidence). The dataset is LF with a trailing newline; the terminator is detected,
not assumed.

## 6. Post-conditions (asserted by the script and by tests/test_hyc0016_m5.py)

1. M5: `material_class = activated_carbon`, `synthesis_method = other`,
   `activation_method = none`, `material_description = "Reference activated
   carbon sample, BET 1830 m2/g"`.
2. M5 equals M11 on those four fields.
3. M5's measurement fields are unchanged (`temperature_k = 293`,
   `uptake_wt_pct = 0.627`, `source_location = Figure 3`).
4. No row in the corpus has `material_class = reduced_graphene_oxide` with
   `bet_surface_area_m2_g = 1830` at `temperature_k = 293` (the old M5 signature).
5. `HYC-0016-M5` is not in `migrate_relabel.SYNTHESIS_RELABEL`.
6. Corpus still 521 rows, 67 columns, validates with 0 errors; the 77 K Chahine
   subset and the ML feature frame are byte-for-byte unchanged (M5 is 293 K).
