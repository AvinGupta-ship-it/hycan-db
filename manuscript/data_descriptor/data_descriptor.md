# HyCAN-DB: a verified, reproducibility-tiered database of hydrogen sorption in carbon nanomaterials

**Author:** Avin Gupta (ORCID 0009-0009-4133-2275)

> **Status: draft for author review.** The science, numbers, and figures are
> final and reproducible from the repository; the framing, acknowledgements,
> author-contribution statement, and any venue-specific formatting are left for
> the author to complete before submission (intended for a data-descriptor venue
> such as *Scientific Data*). AI involvement in drafting is disclosed in
> `docs/ai_usage_log.md`.

## Abstract

Hydrogen-storage measurements on carbon nanomaterials are scattered across
hundreds of articles in incompatible units, under inconsistent conditions, and
rarely shared as machine-readable files, which has made the field's central
scaling claim — the Chahine rule, that physisorptive uptake is about 1 wt% per
500 m² g⁻¹ of BET surface area at 77 K — hard to test at corpus scale. HyCAN-DB
is an open, FAIR database of 521 hydrogen-uptake measurements from 51
peer-reviewed papers (1999–2025) spanning 13 carbon material classes, each row
carrying explicit provenance (DOI, source location, extraction method and
confidence) and a reproducibility tier. The corpus was assembled with a
dual-agent extraction-and-verification pipeline in which every cell produced by
one agent is independently re-derived from the source by a second, isolated
agent; 50 of the 51 papers carry a complete row-level verification record.
Pooling the corpus with a hierarchical model, we find the Chahine rule overstates
real uptake: 77 K uptake scales with BET area at 0.72 wt% per 500 m² g⁻¹ (95% CI
0.62–0.81), roughly 30% below the canonical value, robustly across
reproducibility tiers. A paper-grouped machine-learning baseline predicts 77 K
uptake with R² ≈ 0.84 on held-out papers, with pressure and surface area the
dominant features.

## Background & Summary

A curated, openly licensed dataset is infrastructure for an entire subfield: a
single paper reports one finding, while a database enables analyses no single
paper can perform. The carbon hydrogen-storage literature is a natural candidate.
Different groups report uptake at different temperatures and pressures, define
surface area three ways (BET, Langmuir, geometric), under-report pore structure,
and disagree on what counts as a champion material; the late-1990s to mid-2000s
produced a well-known set of extraordinary room-temperature uptake claims that
subsequent work could not reproduce. Authoritative reviews exist, but a clean,
machine-readable, openly licensed dataset focused on carbons does not.

HyCAN-DB fills that gap and, in doing so, enables a quantitative meta-analysis of
the Chahine rule with explicit accounting for reporting quality, and a
forward-looking predictive model usable as a synthesis prior. Every row is
traceable to a table, figure, or quoted sentence in a real paper; discredited
historical claims are retained and flagged rather than dropped, so a user can
filter by reporting quality and see how conclusions depend on that choice.

## Methods

**Literature search and screening.** Candidate papers were identified by a
systematic search across the major engines and by backward and forward citation
chaining from the field's foundational papers, following a documented protocol
(`docs/literature_search_protocol.md`). Screening followed PRISMA, with every
screened paper recorded with its decision and, where excluded, its reason, in
`references/paper_tracking.csv`. The search deliberately counterweighted the
engines' bias toward recent, high-citation, high-uptake work by seeking the
1998–2005 controversy literature and low-uptake (baseline) results. Ten
screened-in papers could not be retrieved (mostly paywalled) and are recorded as
PRISMA "sought but not retrieved," not exclusions.

**Schema and unit normalization.** Each measurement is one row conforming to a
versioned schema (`src/hycan/schema.py`, a Pydantic model; documented in
`docs/data_dictionary.md`) with controlled vocabularies for material class,
synthesis and measurement method, uptake type, surface-area and pore methods, and
reproducibility tier. All values are stored in the units the source reports and
converted in code with tested functions (`src/hycan/normalize.py`); conversions
are never done by hand. Excess and absolute uptake are distinguished only where
the paper uses the exact word for the value in question, since conflating them is
the field's most common error.

**Dual-agent extraction and verification.** Because a language model reading a
PDF produces plausible, confident, sometimes wrong output, no agent certifies its
own extraction. One agent (A) extracts candidate rows with a source location and
a verbatim supporting quote for every claim; a second, isolated agent (B) receives
the PDF and the candidate values only — not A's reasoning — and independently
re-derives every numeric cell, controlled-vocabulary assignment, and source
location, reporting agreement or disagreement cell by cell. Disputes go to a
third adjudicating pass. Figure-only values are obtained by programmatic
digitization with an archived calibration, never by eye. The measured outcome
across the corpus is that numeric cells agree; the disputes verification upholds
are field-semantics errors (a correct value placed in a field that means
something slightly different). Per-paper dispute records are in
`docs/ai_usage_log.md`; the protocol and its failure modes are documented in
`docs/extraction_provenance.md`.

**Reproducibility tiering.** Every row carries a tier A–D from a ten-point rubric
(`docs/reproducibility_tiering.md`) scoring how completely the source reports what
is needed to reproduce the measurement and whether the value is physically
consistent with its conditions. Tiers are assigned by judgment against the rubric
and cross-checked in verification, not taken from the advisory scorer.

## Data Records

The dataset is a single UTF-8 CSV, `data/raw/measurements_v0.1.csv`: **521 rows,
51 papers with data, 67 columns.** Columns group into paper-level identity
(paper_id, DOI, author, year, journal, title), sample identity and composition
(material class and description, synthesis/purification/activation, dopant and
metal fields), structural characterization (BET and other surface areas, pore
volumes and their methods and probe gas), the measurement (temperature, pressure,
uptake in wt%/mmol g⁻¹/mL STP g⁻¹ and non-gravimetric capacities, uptake type and
bound, method and mode), and provenance (source location, extraction method and
confidence, reproducibility tier, notes, extractor, and verification fields). The
reproducibility-tier distribution is 92 A, 358 B, 54 C, 17 D. Out-of-fold model
predictions are released alongside in `data/processed/predictions_v0.1.csv`.
Citations are in `references/bibliography.bib`, generated from per-field
provenance. The versioned, citable release is archived on Zenodo under CC BY 4.0
(code under MIT).

## Technical Validation

**Schema and cross-field validation.** The dataset validates with zero errors
against the schema, with a controlled set of deliberately admitted warnings
(`src/hycan/validate.py`; asserted against the live dataset by the test suite,
829 tests). Cross-field checks enforce mutual consistency of the uptake units,
pairwise pore-volume nesting, and that a condition is never both stated and
declared unstated.

**Independent verification.** 50 of the 51 papers carry a complete row-level
verification record from the dual-agent protocol; the one exception (HYC-0031) is
29/32 verified, with three rows gated on unobtained Supplementary Information
(`docs/known_limitations.md`). Across the corpus the numeric cells agreed under
independent re-derivation.

**Internal consistency of the physics.** As an end-to-end check, the corpus
reproduces the expected Chahine scaling in form while quantifying its shortfall:
a hierarchical through-origin fit of 77 K uptake on BET area (paper-level random
intercepts, 205 rows / 30 papers) gives a slope of 0.72 wt% per 500 m² g⁻¹ (95%
CI 0.62–0.81), with the shortfall stable across Tier A/B (0.70) and Tier A (0.64)
subsets. A grouped-cross-validation model (GroupKFold by paper, 191 rows / 28
papers) predicts held-out-paper uptake at R² ≈ 0.84 (MAE ≈ 0.5 wt%), well above a
linear baseline, with pressure and BET area dominating SHAP attribution — the
expected 77 K physisorption behaviour, which would not emerge from a corpus
corrupted by unit or transcription errors.

## Usage Notes

The dataset deliberately retains rows that must not enter an uptake aggregation
(non-isothermal cycles, bounded values, unstated-condition and
characterization-only rows). A single shared filter, `hycan.load.analysis_subset`,
applies the required exclusions; users should aggregate through it rather than
over the raw 521 rows. Reproducibility tiers are not interchangeable — Tier D
rows document the field's contested history and should not be averaged with higher
tiers without showing the comparison separately. `docs/known_limitations.md` lists
specific caveats (an advisory-scorer blind spot, four schema gaps, and the
unretrieved PRISMA set). The Quick Start in the
README loads the data and reproduces the headline result in a few lines.

## Code Availability

All code is in the repository under MIT: the `hycan` package (schema, validation,
normalization, the analysis filter, meta-analysis, features, and model), the
figure and prediction generators in `scripts/`, and the analysis notebooks, which
run end-to-end on a fresh clone. Every figure and statistic in this descriptor is
regenerable with `python3 scripts/generate_figures.py` and the notebooks.
