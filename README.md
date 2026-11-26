# HyCAN-DB: Hydrogen in Carbon Nanomaterials Database

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)
![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23231985.svg)](https://doi.org/10.5281/zenodo.23231985)

HyCAN-DB is an open database of primary hydrogen sorption measurements on
carbon sorbents (activated carbons, nanotubes, graphene-family materials,
carbide-derived, templated and zeolite-derived carbons, and doped variants),
with full per-row provenance and a registered, design-based analysis of what
the literature actually supports.

**v1.0: 17,061 measurement rows from 124 papers (1987–2026), built under a
publicly registered protocol — 80 papers drawn as a stratified probability
sample of a 5,251-record frame, each independently dual-extracted and
adjudicated, plus the re-extracted v0.1 corpus.**

---

## The registered study

The protocol ([`docs/v1_protocol.md`](docs/v1_protocol.md)) fixed the search,
the two-stratum sampling design, the extraction pipeline, a 60-row author
audit, five research questions and every analysis — including the ±15%
equivalence margin and 13 sensitivity analyses — before the first search
request was sent. It was registered on Zenodo on 28 October 2026 with file
hashes: [10.5281/zenodo.23719010](https://doi.org/10.5281/zenodo.23719010)
([`docs/v1_registration.md`](docs/v1_registration.md)).

Headline results (details in
[`manuscript/v1/manuscript_v1.md`](manuscript/v1/manuscript_v1.md), every
number regenerable from committed code):

- **The Chahine rule holds on average at the excess maximum**: the pooled
  ratio of n_ex,max to A_BET/500 is 0.976 (95% CI 0.905–1.052; 82 samples,
  29 papers, 26 laboratories), inside the registered margin. Restricted to
  explicitly stated excess values the CI (0.865–1.081) crosses the margin
  and the registered decision is inconclusive, so the conclusion depends on
  that choice.
- **It is a poor sample-level predictor**: the 95% prediction interval for a
  new material is 0.61–1.56, and uptake rises sublinearly with area (ln–ln
  slope 0.75, CI 0.66–0.85).
- **At 1 bar the rule fails** (ratio 0.58, CI 0.52–0.65; area exponent 0.57).
- **Interlaboratory CV** on identical commercial carbons: ≈9% for 1-bar
  uptake (pooled, 95% CI 5–21%).
- **Reporting practice is weak**: by design-weighted estimates, 6% of
  eligible papers state the uptake basis for every value, 7% their wt%
  convention, 9% instrument and calibration.
- **A four-term linear model predicts uptake as well as gradient-boosted
  trees** under paper-grouped cross-validation (out-of-fold R² 0.71 vs
  0.65); every model is weak above 10 bar.

---

## Repository structure

```
hycan-db/
├── data/
│   ├── raw/            measurements_v1.0.csv — the dataset (one row per reported measurement)
│   │                   measurements_v0.1.csv — the superseded v0.1 dataset, retained
│   └── processed/      measurements_v1.0_computed.csv — §10 computed fields
├── docs/
│   ├── v1_protocol.md               the registered protocol (amendments in §15)
│   ├── v1_registration.md           the Zenodo registration record
│   ├── data_dictionary.md           field definitions and controlled vocabularies
│   ├── extraction_provenance.md     how the v0.1 rows were built and verified
│   ├── known_limitations.md         v0.1-era caveats; v1.0 limitations are in the manuscript
│   └── history/                     archival project records
├── manuscript/v1/      manuscript (md + typeset PDF), generated tables, PRISMA checklist
├── figures/v1/         the v1.0 figures + captions (v0.1 figures remain in figures/)
├── references/
│   ├── v1_search/      raw API responses, merge, frame, draw order
│   ├── v1_screening/   both screeners' decisions, tiebreaks, author audit
│   ├── v1_fulltext/    retrieval and eligibility records, author review
│   ├── v1_extraction/  per-paper A/B/C/L outputs, resolutions, agreement stats
│   ├── v1_audit/       the §12 author audit: draw, verdicts, score
│   ├── v1_analysis/    §11 outputs (RQ1–RQ5, sensitivity, moderators)
│   └── v1_prisma/      PRISMA 2020 counts and flow diagram
├── scripts/v1_search/  the v1.0 pipeline (search → … → analysis → tables → figures)
├── src/hycan/          schema, validation, computed coding, v1 analysis modules
├── tests/              pytest suite (1,161 tests)
├── CHANGELOG.md  CITATION.cff  requirements-v1.lock  pyproject.toml
```

---

## Installation

Requires Python 3.13 (the pinned analysis environment).

```bash
git clone https://github.com/AvinGupta-ship-it/hycan-db.git
cd hycan-db
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux  (.venv\Scripts\activate on Windows)
python3 -m pip install -r requirements-v1.lock
python3 -m pip install -e . --no-deps
python3 -m pytest -q             # 1,161 tests
```

---

## Quick start

Load the dataset and reproduce the RQ1 primary result:

```bash
python3 scripts/v1_search/analysis.py rq1        # writes references/v1_analysis/rq1.json
```

```python
import json
r = json.load(open("references/v1_analysis/rq1.json"))["primary"]
print(f"ratio {r['ratio']:.3f}, 95% CI {r['ci95_t']}, decision: {r['decision']}")
```

Regenerate everything else from the committed inputs:

```bash
python3 scripts/v1_search/analysis.py rq1-sens   # sensitivity analyses (i)–(xiii)
python3 scripts/v1_search/analysis.py rq1-mods   # moderators
python3 scripts/v1_search/analysis.py rq2        # … rq3, rq4, rq5 likewise
python3 scripts/v1_search/prisma.py              # PRISMA counts + flow diagram
python3 scripts/v1_search/tables.py              # manuscript tables
python3 scripts/v1_search/figures.py             # manuscript figures
```

---

## How the dataset was built, and what that means for trusting it

Every probability-sample paper was extracted twice by independent agents
(one from the text layer and page images, one from page images alone),
reconciled by a third against the source with a recorded decision and
location for every disagreement, and checked by a figure-curve labeller;
models and frozen prompts per role are fixed in the registered Amendment-1
table. Agreement between the independent extractions is released in full
(`references/v1_extraction/agreement_*.json`): row detection 0.83, uptake
values within tolerance in 88.7% of 9,282 pairs, BET areas in 99.9%. The
author audited 60 drawn rows field-by-field against the PDFs and found 0
errors (`references/v1_audit/`). The v0.1 corpus was re-extracted under the
same frozen pipeline; [`docs/extraction_provenance.md`](docs/extraction_provenance.md)
documents the original v0.1 build.

Every row carries a §10.1 reporting-completeness score and tier (A–D),
computed by code; low-quality and discredited historical claims are retained
and flagged (372 rows by the physical-plausibility screen) rather than
dropped.

---

## v0.1

The v0.1 release
([10.5281/zenodo.23231986](https://doi.org/10.5281/zenodo.23231986)) remains
available; its data rows stand, and its analyses — including the 0.72 wt%
per 500 m²/g estimate — are withdrawn on the record itself and should not be
cited. The registered v1.0 study replaces them, and sensitivity (xiii) of
the manuscript quantifies why the v0.1 specification misled.

---

## Data and code availability

The dataset is `data/raw/measurements_v1.0.csv` with computed fields in
`data/processed/measurements_v1.0_computed.csv`; the pipeline and analysis
code are under `scripts/` and `src/hycan/`. The project is archived on
Zenodo (data CC BY 4.0, code MIT).

> **Zenodo DOI:** [10.5281/zenodo.23231985](https://doi.org/10.5281/zenodo.23231985) — concept DOI, always resolves to the latest version.

Literature PDFs are excluded for copyright reasons; the released search,
screening, retrieval and extraction records let every source be retrieved
and every decision re-traced independently.

---

## How this fits together

**HyCAN-DB** curates what the field has measured.
[**H2STAR**](https://doi.org/10.5281/zenodo.23257816) converts those
measurements into system-level consequence and derives what a material would
have to be; its carbon-nanotube case study is drawn entirely from this
corpus, every entry carrying its `HYC-` identifier.

---

## Citation

Please cite using the metadata in [`CITATION.cff`](CITATION.cff), or cite
the dataset directly:

> Gupta, Avin (2026). *HyCAN-DB: Hydrogen in Carbon Nanomaterials Database*
> (v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23231985

The DOI above is the concept DOI (always the latest version); each release's
version DOI is listed on the Zenodo record.

## License

- **Code** (`src/`, `scripts/`, `notebooks/`): [MIT](LICENSE)
- **Data** (`data/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`data/LICENSE.md`](data/LICENSE.md)
