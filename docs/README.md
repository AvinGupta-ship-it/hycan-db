# HyCAN-DB documentation

This directory holds the project's reference documentation, methodology, and
engineering records. For the project overview, installation, and headline
results, see the [root README](../README.md). For the dataset itself see
`data/raw/measurements_v0.1.csv` and the data dictionary below.

## Start here

- [v0.1_summary.md](v0.1_summary.md) — plain-language summary of the analysis and
  model findings (the Chahine meta-analysis and the ML baseline).
- [data_dictionary.md](data_dictionary.md) — every column defined, with the
  controlled vocabularies and units.
- [reproducibility_tiering.md](reproducibility_tiering.md) — the A–D reproducibility
  rubric, the physics-override clause, and worked examples.
- [known_limitations.md](known_limitations.md) — what to know before relying on
  any particular value.

## How the corpus was built

- [literature_search_protocol.md](literature_search_protocol.md) — the search
  strategy and the PRISMA companion to `references/paper_tracking.csv`.
- [extraction_provenance.md](extraction_provenance.md) — how every row was
  extracted and independently re-derived under the dual-agent protocol.
- [ai_usage_log.md](ai_usage_log.md) — the contemporaneous, session-by-session
  log of AI assistance and human verification (per Execution Manual §17.5).

## Provenance and audit

- [corpus_audit.md](corpus_audit.md) — an internal consistency audit of the
  corpus and its documentation.
- [phase_d_screening_log.md](phase_d_screening_log.md) — the Phase D screening
  decisions.
- [schema_v1_2_gaps.md](schema_v1_2_gaps.md) — schema gaps found during Phase C
  extraction.

## Migration records

Each migration plan documents a change to the dataset or schema before it was
made, and is applied by a committed script in `scripts/` that refuses to run
twice and is covered by a round-trip test (§6.7). They are kept as the engineering
record of how the corpus reached its current state.

**Schema:**

- [migration_v1.1_plan.md](migration_v1.1_plan.md) — schema v1.1.
- [migration_v1_2_plan.md](migration_v1_2_plan.md) — schema v1.1 → v1.2.
- [migration_v1_3_plan.md](migration_v1_3_plan.md) — schema v1.3 (v1.2 stage 4).

**Data corrections:**

- [migration_relabel_plan.md](migration_relabel_plan.md) — the `synthesis_method`
  relabel and HYC-0027 Pd-composition backfill.
- [migration_relabel_test_scope_plan.md](migration_relabel_test_scope_plan.md) —
  scoping a `physical_activation` post-condition to a delta.
- [migration_hyc0016_m5_plan.md](migration_hyc0016_m5_plan.md) — correcting
  HYC-0016-M5 (a reference activated carbon mislabeled as KOH-activated r-GO).
- [migration_chahine_excess_only_plan.md](migration_chahine_excess_only_plan.md) —
  keeping total-uptake rows out of the Chahine figure.
- [migration_held_rows_plan.md](migration_held_rows_plan.md) — writing the last
  two held rows and backfilling two spacings.
- [migration_record_extraction_plan.md](migration_record_extraction_plan.md) — a
  routine tool for §9.1 step 15 (extraction record).
- [migration_score_reproducibility_plan.md](migration_score_reproducibility_plan.md) —
  fixing four `score_reproducibility` defects.
- [migration_staging_builder_plan.md](migration_staging_builder_plan.md) — a
  reusable staging builder.

**Screening and tracking:**

- [migration_exclude_hyc0038_plan.md](migration_exclude_hyc0038_plan.md) —
  excluding HYC-0038 at full-text review.
- [migration_paper_tracking_plan.md](migration_paper_tracking_plan.md) — bringing
  `references/paper_tracking.csv` into agreement with the dataset.
- [migration_pdf_obtained_plan.md](migration_pdf_obtained_plan.md) — recording
  which Phase D full texts were obtained.
- [migration_phase_d_screening_plan.md](migration_phase_d_screening_plan.md) —
  folding the Phase D screening results into `paper_tracking.csv`.
