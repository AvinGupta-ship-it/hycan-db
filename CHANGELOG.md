# Changelog

All notable changes to HyCAN-DB will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
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
### Outstanding
- Three backfills need the source PDFs and are deferred to a second commit: `ultramicropore_volume_cm3_g` for HYC-0021 (Sethia 2016), the two recovered characterization-only rows for HYC-0018 (Singh 2020), and the §8.6 `extraction_confidence` reassessment for HYC-0005 (Texier-Mandoki 2004). HYC-0016-S13 ("Thermally exfoliated graphene oxide") is left as `graphene` pending the same batch rather than relabelled on inference.

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
