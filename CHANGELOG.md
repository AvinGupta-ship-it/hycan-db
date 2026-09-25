# Changelog

All notable changes to HyCAN-DB will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
### Added — Phase C, first three papers under the §3.2 dual-agent protocol
- HYC-0025 (Sawant 2021), 6 rows. Boron-doped MWCNTs, 0–8 at% B, 0.048–0.497 wt% at 303 K and 16 bar. The paper reports no surface area of any kind, so these are the corpus's first `surface_area_method = none` rows — representable only under schema v1.1, which is what gap 1 was for.
- HYC-0012 (Liu 2010), 6 rows. Arc-discharge SWCNTs and CVD MWCNTs, 0.2–1.7 wt% at ~293 K and ~120 bar. This paper is its own authors' retraction of their 1999 *Science* result, which is already in the corpus as HYC-0002 at Tier D; the corpus now holds both the claim and the retraction, which is the point of tiering as disclosure.
- HYC-0017 (Ma 2009), 2 rows. Chemically exfoliated graphene, 0.4 wt% at 77 K and 0.35 wt% at 87 K, both at 1 bar, on a stated BET area of 156 m²/g.
- `docs/schema_v1_2_gaps.md` — the inventory of schema limitations Phase C has hit, written before any migration.
### Verification
- **First measured dispute rate: 0 disputes in 132 verified cells** (42/42, 64/64, 26/26). Each paper was extracted by one agent and every numeric and controlled-vocabulary cell independently re-derived from the PDF by a second agent holding the paper and the candidate values only. Free-text cells are not part of the count. Three papers is a small sample and the number should not be read as a validated error rate; `docs/ai_usage_log.md` says why, and lists what the verification pass did demonstrably catch.
- Four internal contradictions in HYC-0025 and one sample-ordering trap in HYC-0012 were surfaced by verification and are recorded in row notes under §3.7 rather than resolved silently.
- HYC-0019 (Huang 2010), 12 rows. Litchi-wood KOH-activated carbon, six samples oxidized to varying degrees, each at 77 K/1 bar and 303 K/57 bar. 468–2675 m²/g, 0.086–2.645 wt%.
- HYC-0022 (Wang 2009), 9 rows. Commercial activated carbon further activated with CO₂ or KOH, up to 3190 m²/g and 7.08 wt% at 77 K and 20 bar, plus a purchased reference carbon the authors measured to check their instrument.
### Dataset
- 121 → 156 rows, 11 → 16 papers, 40 columns unchanged. 0 errors. Warning types unchanged throughout: `Unspecified uptake_type` 98 → 133, `mmol/g and wt% inconsistent` 1 → 1. No new warning type at any of the five appends (§11.5). 418 tests passing, ruff clean.
- 35 rows now carry `extractor = "HyCAN pipeline v2"` with `verified_by` and `verification_date` populated, per §8.4. The 121 v1.0 rows are untouched and remain single-reader; `docs/extraction_provenance.md` states the split plainly.
### Verification — the protocol's first real dispute
- **4 disputed cells in 308 verified, 1.3%.** All four were in one field of one paper. HYC-0022's `synthesis_method` was extracted as `commercial` on all six samples, on the ground that the carbon skeleton was purchased. The verifier rejected that for the four samples the authors activated themselves, citing the paper's own "Both physical and chemical activations were performed in our study" and the carbon yields — 62%, 49%, 53%, 43% — that its Table 1 reports for exactly those four samples and no other. A sample with a burn-off yield was not bought in that state. Upheld; those rows carry `other`, because the vocabulary has no value for activation at all. Had it had one, the dispute would not have arisen — recorded as gap 5.
### Outstanding
- **All twelve Phase C papers are now read. 133 rows extracted, 35 written, 98 held** — none dropped, and not one held for lack of evidence. Seven papers are blocked, no two by the same limitation: HYC-0007 (10 rows), HYC-0009 (20), HYC-0011 (5), HYC-0015 (2), HYC-0024 (8), HYC-0026 (7), HYC-0029 (16), plus one HYC-0017 row. `docs/schema_v1_2_gaps.md` is the complete inventory with a proposed fix and a sequencing order for each of ten gaps. Unblocking is worth about 98 rows and would take the corpus past the 20-paper Phase 3 milestone.
- Notable holds: HYC-0024 yields **zero** storable uptake values — eight samples measured at 293 K and 100 bar, reported only as volumetric densities in kg/m³. HYC-0029's 13 uptakes come from a 303→673→303 K temperature cycle rather than an isothermal measurement, so storing one `temperature_k` would assert something false and would quietly corrupt any Chahine comparison.
- HYC-0011's headline 8.0 wt% is arithmetically irreconcilable with the paper's own areal uptake, film mass and film area, which imply 0.84–1.26 wt%; reaching 8.0 would need a film area nine times the largest the paper states. Recomputed independently. Belongs in the corpus at Tier D with the discrepancy quoted, per the tiering doc's disclosure-not-deletion principle.

### Added — schema v1.1 (manual §8.5 gaps 1–4, §8.6 cleanups)
- `surface_area_method` (controlled: `BET`, `Langmuir`, `geometric`, `DFT`, `unspecified`, `none`, default `unspecified`). Gap 1. Unblocks HYC-0025, which reports one unqualified "surface area" that previously had nowhere to go without asserting a method the paper never stated.
- `ultramicropore_volume_cm3_g` (float, 0–2). Gap 4, the most consequential. The corpus holds two Chahine-deviating papers and could not test the explanation either offers, because the distinguishing quantity was stranded in free-text notes.
- `carbide_chlorination` added to the `synthesis_method` vocabulary. Gap 2.
- Cross-field validation `ultramicropore ≤ micropore ≤ total_pore`, ERROR severity, checked pairwise so a missing middle term cannot suppress the outer comparison.
- `scripts/migrate_v1_1.py` — the migration itself, committed and re-runnable, with `--dry-run`. It reads and writes raw CSV cells rather than going through pandas, so an unmodified cell is byte-identical by construction and the verification can assert exactly that.
- `docs/migration_v1.1_plan.md` — the §6.7 plan, written before any protected file was touched.
### Changed
- `temperature_k` and `pressure_bar` are now conditionally required: mandatory when a row reports any uptake value, optional when it reports none. Gap 3. A sample whose BET and pore data are published but whose uptake was never measured is now a recordable row; under v1.0 it was not, and two such rows were dropped from HYC-0018.
- `micropore_volume > total_pore_volume` is now an ERROR rather than a warning. §11.2 always specified ERROR and the v1.0 code raised a warning; the mismatch is resolved in the manual's favour per §0. No row in the corpus violates it, so nothing in the dataset changes.
- HYC-0023: 23 rows `synthesis_method` `other` → `carbide_chlorination`.
- HYC-0016: 11 rows `material_class` `graphene` → `reduced_graphene_oxide`, on rows whose `material_description` begins "Reduced graphene oxide".
- `surface_area_method` populated as `BET` on the 109 rows carrying a `bet_surface_area_m2_g` value, `unspecified` on the other 10.
### Dataset
- 119 rows, 11 papers, unchanged in count. 38 → 40 columns, both appended at the end so positional appends still work (§6.7). Exactly 34 cells changed in the pre-existing 38 columns, all of them the two relabels above. Validation: 0 errors, warning types unchanged at `Unspecified uptake_type ×96` and `mmol/g and wt% inconsistent ×1`. 405 tests passing.
### Added — source-backed backfills (second commit)
- `ultramicropore_volume_cm3_g` backfilled for HYC-0021 (Sethia 2016, Table 2, pores below 0.7 nm) and HYC-0005 (Texier-Mandoki 2004, Table 1 V_DR(CO2), which the paper defines as pores below 0.7 nm). 29 rows across two papers now carry the quantity, which is what makes the deviation both papers report testable across the corpus.
- HYC-0018: two characterization-only rows recovered (GO and EGR 400), representable only under v1.1's conditional temperature and pressure. Neither sample has a numeric hydrogen uptake in the paper's text or tables; EGR (400)'s exists only as plotted points in Fig. 9, so under §3.4 it awaits digitization and the row says so.
- `tests/test_dataset_invariants.py` — invariants asserted against the real dataset rather than a fixture, including the §11.5 warning baseline and the pore-volume nesting.
### Changed — HYC-0005 surface area
- `surface_area_method` BET → `unspecified` and `extraction_confidence` 5 → 4 on all 25 rows. §8.6 asked whether a total surface area had been entered into the BET field. It had: Table 1's column is headed "TSA" and footnoted "total surface area", and the strings "BET" and "Brunauer" do not occur anywhere in the paper. The values stay in `bet_surface_area_m2_g` because the schema has no generic surface-area field; `surface_area_method` now carries the truth. The rows previously asserted a method the authors never claimed.
### Dataset (after backfill)
- 121 rows, 11 papers, 40 columns. 0 errors. Warning types unchanged; `Unspecified uptake_type` rises 96 → 98, which §11.5 permits as an increase in an existing type. 418 tests passing.
### Verification
- Every backfilled cell was extracted from the PDF and then independently re-derived by a second agent holding the papers and the candidate values only, with no access to the first agent's reasoning (§3.2). 40 cells checked, 40 agreed. The one disagreement it raised was against a transcription error in the verification prompt, not against the dataset, and is recorded in `docs/ai_usage_log.md`.
### Outstanding
- No backfill remains blocked on a source. Still open: `ultramicropore_volume_cm3_g` for HYC-0021 (Sethia 2016), the two recovered characterization-only rows for HYC-0018 (Singh 2020), and the §8.6 `extraction_confidence` reassessment for HYC-0005 (Texier-Mandoki 2004). HYC-0016-S13 ("Thermally exfoliated graphene oxide") is left as `graphene` pending the same batch rather than relabelled on inference.

### Added
- Phase A pipeline automation (manual v2.0 §18), four command-line helpers under `scripts/`, each with tests:
  - `validate_row_detail.py` — per-row validation detail: which row, which field, and that field's current value, where `validate_data.py` reports only counts by type.
  - `inspect_columns.py` — column inspection CLI replacing ad-hoc pandas heredocs; reports the physical CSV column order against `schema.py`'s declaration order (§6.7) and warns on rows of differing width.
  - `append_paper.py` — §9.1 steps 11–14 as one command that refuses on any check failure: verify staging from disk, validate standalone, back up, append positionally, re-verify the merged file against the session baseline, remove staging.
  - `digitize_figure.py` — §3.4 programmatic figure digitization: axis calibration with an optional third verification tick, colour isolation bounded to the plot region, point extraction, JSON archival of every parameter, and a check subcommand that records its verdict in the archive.
- 312 new tests (82 → 394 total).
### Changed
- Nothing in the dataset, the schema, the source modules, or the pre-existing tests. `data/raw/measurements_v0.1.csv` is byte-identical: 119 rows, 11 papers, 0 errors, warning types `Unspecified uptake_type ×96` and `mmol/g and wt% inconsistent ×1`.
### Notes
- The scripts were audited by four isolated agents that had not seen the reasoning behind the code. The defects they demonstrated — and the vacuous tests that had let those defects pass — are recorded in `docs/ai_usage_log.md` rather than summarised away.

## [v0.1-alpha] - 2026-07-09
### Added
- Reproducibility tiering rubric (docs/reproducibility_tiering.md): 10-point scoring criteria, physics-override clause, and three worked examples (Tier A/C/D).
- suggest_tier() and score_reproducibility() functions in src/hycan/validate.py, with 6 accompanying unit tests.
- Corpus-overview notebook (notebooks/01_corpus_overview.ipynb): nine narrated sections running end-to-end on the raw dataset.
- Plotting module (src/hycan/plotting.py): house style plus corpus map, condition-space, and Chahine-rule figure generators; three 300-dpi figures in figures/.
- ruff.toml at repository root (ignores E402 in notebooks/ for the sys.path-insert pattern).
### Changed
- HYC-0002 (Liu 1999) re-tiered B to D: room-temperature uptake above the ~1 wt% physisorption bound with no reported surface area; physics override applied.
### Dataset
- 60 validated measurements across 5 papers (Panella 2005, Liu 1999, Nijkamp 2001, Texier-Mandoki 2004, Serafin 2024). Tier distribution: 57 B, 3 D. Validation: 60 rows, 0 errors.

## [0.0.2] - 2026-07-05

### Added
- `measurement_id`: required, unique-per-row key on `MeasurementEntry`
  (format `{paper_id}-M{n}`, e.g. `HYC-0001-M1`). Duplicate `measurement_id`
  is a dataset-level error.
- `uptake_ml_stp_g`: optional field for as-reported volumetric uptake in
  mL(STP)/g at 273.15 K, 1 atm (range 0–2225, matching the 20 wt% ceiling).
- `normalize.ml_stp_per_g_to_mmol_per_g` and `normalize.ml_stp_per_g_to_wt_pct`
  converters, using the ideal-gas molar volume at STP, Vm = 22.414 L/mol
  (= 22.414 mL/mmol) at 273.15 K and 1 atm, together with M(H₂) = 2.01588 g/mol.

### Changed
- Dataset-level uniqueness key moved from `sample_id` to `measurement_id`; the
  duplicate-`sample_id` check has been removed from validation.
- `sample_id` may now repeat across rows: it denotes one physical sample that
  can be measured under multiple conditions.
- Schema field set stabilized ("schema v1.0"): this migration only adds fields,
  never removes them.

## [0.0.1] — 2026-06-09

### Added
- Initial project scaffolding: directory structure, Python package skeleton,
  `requirements.txt`, `pyproject.toml`, `CITATION.cff`, `README.md`,
  `docs/data_dictionary.md` stub, and setup-check notebook.
