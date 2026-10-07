# HyCAN-DB: Hydrogen in Carbon Nanomaterials Database

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)
![Version](https://img.shields.io/badge/version-v0.1-blue.svg)

HyCAN-DB is an open, FAIR-compliant database of hydrogen sorption measurements in
carbon nanomaterials (activated carbons, carbon nanotubes, graphene-family
materials, carbide-derived and templated carbons, and doped variants). It gathers
primary measurements from the peer-reviewed literature, harmonises them into
consistent units with full provenance, attaches a transparent reproducibility
tier to every data point, and ships a reproducible meta-analysis and
machine-learning pipeline on top. The goal is a single, auditable place to compare
how much hydrogen different carbon materials actually store, and under what
conditions.

**521 measurements from 51 papers (1999–2025), 13 material classes. 50 of the 51
papers have been through independent dual-agent verification.**

---

## Headline results (v0.1)

- **The Chahine rule overstates real uptake by ~30%.** Pooled across the corpus
  with a hierarchical (paper-random-effects) fit, 77 K uptake scales with BET area
  at **≈0.72 wt% per 500 m²/g (95% CI 0.62–0.81)** — 1 wt% per ~700 m²/g, not per
  500 — and the confidence interval excludes the rule. Robust to reproducibility
  tier. See `notebooks/04_meta_analysis.ipynb` and `docs/v0.1_summary.md`.
- **A paper-grouped model predicts 77 K uptake at R² ≈ 0.84, MAE ≈ 0.5 wt%** on
  held-out papers, with pressure and BET area the dominant features (SHAP). See
  `notebooks/05_ml_baseline.ipynb`.

---

## Repository structure

```
hycan-db/
├── data/
│   ├── raw/            measurements_v0.1.csv — the curated dataset (tracked)
│   └── processed/      predictions_v0.1.csv — out-of-fold model predictions
├── docs/
│   ├── data_dictionary.md          field definitions and controlled vocabularies
│   ├── reproducibility_tiering.md   the A–D tiering rubric and worked examples
│   ├── extraction_provenance.md     how every row was built and verified
│   ├── known_limitations.md         what to know before relying on the data
│   ├── v0.1_summary.md              analysis + model findings, plain language
│   ├── literature_search_protocol.md
│   └── ai_usage_log.md              contemporaneous AI-assistance log
├── figures/            Figures 1–8 (300 dpi PNG + PDF) + CAPTIONS.md
├── notebooks/          00_setup_check, 01_corpus_overview, 03_descriptive_analysis,
│                       04_meta_analysis, 05_ml_baseline
├── references/
│   ├── bibliography.bib             generated from per-field provenance
│   └── paper_tracking.csv           PRISMA screening audit trail
├── scripts/            generate_figures.py, build_predictions.py, validators, migrations
├── src/hycan/          schema, normalize, validate, clean, load, plotting, meta,
│                       features, ml
├── tests/              pytest suite (829 tests)
├── CHANGELOG.md  CITATION.cff  pyproject.toml  requirements.txt  ruff.toml
```

---

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/AvinGupta-ship-it/hycan-db.git
cd hycan-db
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux  (.venv\Scripts\activate on Windows)
python3 -m pip install -e .
python3 -m pip install -r requirements.txt
```

---

## Quick Start

Load the dataset through the canonical analysis filter and reproduce the headline
Chahine-rule result:

```python
from hycan.load import load_dataset
from hycan import meta

df = load_dataset()                       # 521 rows
res = meta.chahine_mixedlm(df)            # hierarchical fit, 77 K subset
print(f"{res['wt_pct_per_500_m2']:.2f} wt% per 500 m2/g "
      f"(95% CI {res['wt_pct_per_500_m2_ci95'][0]:.2f}-"
      f"{res['wt_pct_per_500_m2_ci95'][1]:.2f}); Chahine rule = 1.0")
```

Regenerate every figure from the published data and code:

```bash
python3 scripts/generate_figures.py       # writes figures/fig1..fig8 (PNG + PDF)
python3 scripts/build_predictions.py      # writes data/processed/predictions_v0.1.csv
```

The analysis notebooks (`03_descriptive_analysis`, `04_meta_analysis`,
`05_ml_baseline`) narrate the corpus description, the meta-analysis, and the model,
and run end-to-end on a fresh clone.

---

## How this dataset was built, and what that means for trusting it

The corpus is **521 rows from 51 papers**. 400 rows (40 papers) were produced by
an **AI dual-agent extraction pipeline** — one agent extracts from the PDF, a
second, isolated agent independently re-derives every cell from the PDF alone, and
an adjudicator resolves disputes. The other 121 rows (11 papers) were originally
human-extracted and were **re-read under the same dual-agent protocol in October
2026**, so **50 of the 51 papers now carry a complete row-level `verified_by`
record** (HYC-0031 is the one exception; see `docs/known_limitations.md`). Across
every batch the *numeric* cells agreed — the disputes verification caught were
field-semantics (a correct value in a slightly wrong field), not wrong numbers.

[`docs/extraction_provenance.md`](docs/extraction_provenance.md) is the full
account; [`docs/known_limitations.md`](docs/known_limitations.md) lists what to
check before relying on any particular value. Code was written with AI assistance
under human review; AI involvement is disclosed in
[`docs/ai_usage_log.md`](docs/ai_usage_log.md) rather than obscured.

---

## Reproducibility tiering

Every measurement carries a tier (A–D) reflecting how completely its source
reports what is needed to reproduce it; low-quality and discredited historical
claims are retained and flagged rather than dropped. The rubric, the
physics-override clause, and worked examples are in
[`docs/reproducibility_tiering.md`](docs/reproducibility_tiering.md).

---

## Data and code availability

The dataset is `data/raw/measurements_v0.1.csv`; the code that validates,
harmonises, analyses, and plots it is in `src/hycan/`. A citable Zenodo DOI is
minted with the v0.1 release and added here once the archive is published.

> **Zenodo DOI:** _(pending — added here when the v0.1 archive is published on Zenodo)_

Literature PDFs are excluded for copyright reasons; per-field citation provenance
in `references/bibliography_sources.json` lets every source be retrieved
independently.

---

## Citation

Please cite using the metadata in [`CITATION.cff`](CITATION.cff) (the Zenodo DOI
will be added at release).

## License

- **Code** (`src/`, `scripts/`, `notebooks/`): [MIT](LICENSE)
- **Data** (`data/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`data/LICENSE.md`](data/LICENSE.md)
