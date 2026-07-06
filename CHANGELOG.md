# Changelog

All notable changes to HyCAN-DB will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
