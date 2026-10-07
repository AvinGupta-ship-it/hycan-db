# Known limitations

An honest, consolidated list of what a user of HyCAN-DB v0.1 should know before
relying on it (manual §2.5, §3.10). None of these affects the headline results —
the Chahine meta-analysis and the ML model both run on the 77 K analysis subset,
where none of the items below changes a value — but each is a real limitation,
recorded rather than hidden. Items are kept out of the dataset's *values* and
stated here instead.

## Data labels

No outstanding label errors. One was corrected after the v0.1 verification pass
and is recorded here for provenance:

- **HYC-0016-M5 (corrected 2026-10-07).** It had been extracted as
  `reduced_graphene_oxide` / `koh_activation` and then swept into
  `scripts/migrate_relabel.py`'s KOH relabel as `chemical_activation`. It is in
  fact the paper's **reference activated carbon** — the 293 K measurement of the
  same physical sample as the 77 K row HYC-0016-M11 (Klechikov 2015; the Fig. 3
  caption marks the reference carbon in red, and the 2026-10-05 dual-agent pass
  flagged it independently). It was the third instance of the §6.7 "a text-match
  relabel catches a reference sample" hazard, after HYC-0001 and HYC-0004.
  `scripts/migrate_hyc0016_m5.py` (`docs/migration_hyc0016_m5_plan.md`) set M5's
  `material_class`, `synthesis_method`, `activation_method` and
  `material_description` to match M11, and M5 was removed from the relabel
  migration's scope (`SYNTHESIS_RELABEL` 36 → 35). No headline result moved: the
  row is a 293 K measurement and every headline result is at 77 K.

## Tooling

- **`score_reproducibility` has a known blind spot (§13.7) and is advisory only.**
  It awards the Chahine criterion a free "cannot assess" point when
  `temperature_k` is null, so a paper that never states a temperature collects a
  point for a check that never ran — HYC-0011's discredited 8.0 wt% row and its
  ordinary 0.26 wt% row score identically. Three related issues (§18 item 3):
  `bet` reads only `bet_surface_area_m2_g`, so a paper reporting a micropore and
  an external area by a named method scores 0; `purity` is proxied by
  `purification_method`; and the Chahine branch returns "cannot assess" at 77 K
  for want of a *total* area even when micropore and external areas are present.
  **This is not load-bearing:** every tier in the dataset was assigned by hand
  against §13.3 and cross-checked by an independent agent, not taken from this
  function, and HYC-0011's Tier D is pinned by the §11.2 pre-2005 warning
  independently. Do not use `suggest_tier` on a row where `temperature_unstated`
  or `pressure_unstated` is true; score it by hand.

## Schema gaps (found during verification; schema unchanged)

Four quantities a few papers report have no schema home. Each is recorded in the
relevant row's `notes`; adding fields was deferred rather than opening a schema
migration that no published figure or model needs.

- **No `graphite` material class.** Three HYC-0004 rows are `other` for this
  reason (graphite references in an activated-carbon survey).
- **No `not_applicable` `measurement_mode`.** Characterization-only rows assert
  an `isothermal` mode that did not happen (the `measurement_method` field already
  has `not_applicable`; `measurement_mode` does not).
- **No oxygen-content field.** HYC-0031's independent variable (reported three
  ways — CHN, XPS, TPD) lives only in `notes`.
- **No isosteric-heat field.** HYC-0031 reports q_st per sample; it is not
  recorded as a column.

## Incomplete coverage

- **HYC-0031 is `extracted`, not `verified`.** 29 of its 32 rows are confirmed
  from the main PDF; the three AX21 cryogenic rows' temperature is stated only in
  the Supplementary Information, which was not obtained, so full verification
  waits for the SI.
- **Ten screened-in papers were not retrieved** (PRISMA "sought but not
  retrieved", not exclusions): HYC-0003, 0006, 0008, 0014, 0035, 0036, 0054,
  0055, 0056, 0059 — mostly RSC/paywalled, no accessible full text. They are
  tracked `not_started` with the reason in `notes`.

## Analysis caveats (detailed in the notebooks)

- The publication-bias funnel/Egger test uses within-paper dispersion as a
  precision proxy (the papers report no per-value uncertainty), so it is
  suggestive, not a formal small-study test (`notebooks/04_meta_analysis.ipynb`).
- Doping is excluded as a model feature for want of a comparable subset
  (§14.3); its absence is not evidence that doping does not matter
  (`notebooks/05_ml_baseline.ipynb`).
- Figure 4's per-area normalisation is unstable at low BET; a few points sit
  off-scale and are annotated rather than dropped.
