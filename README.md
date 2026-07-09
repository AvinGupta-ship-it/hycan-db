# HyCAN-DB: Hydrogen in Carbon Nanomaterials Database

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)
![Version](https://img.shields.io/badge/version-v0.1--alpha-blue.svg)

HyCAN-DB is an open, FAIR-compliant database of hydrogen sorption measurements
in carbon nanomaterials (activated carbons, carbon nanotubes, and related porous
carbon materials). It gathers primary measurements extracted
from peer-reviewed literature, harmonises them into consistent units with full
provenance, and attaches a transparent reproducibility tier to every data point.
The goal is to give a scientifically literate reader — not only specialists — a
single, auditable place to compare how much hydrogen different carbon materials
actually store, and under what conditions, so that reproducible research at the
intersection of hydrogen energy storage and data-driven materials science can build
on a trustworthy foundation.

---

## Why this project exists

Published hydrogen-storage measurements are scattered across hundreds of journal
articles in incompatible units, reported under inconsistent conditions, and rarely
shared as machine-readable files. HyCAN-DB solves this by (1) systematically
extracting and digitising isotherms from the literature, (2) converting all data to
consistent SI units with full provenance metadata, (3) flagging outliers and
transcription errors with an auditable quality-control log, and (4) releasing
everything under open licences so the community can build on it immediately.

---

## Repository structure

```
hycan-db/
├── data/
│   ├── raw/            # Curated dataset (measurements_v0.1.csv, tracked) + source xlsx (gitignored)
│   ├── interim/        # Partially processed intermediate files
│   ├── processed/      # Reserved for analysis-ready builds (none yet)
│   └── external/       # Third-party reference data
├── docs/
│   ├── data_dictionary.md          # Field definitions and controlled vocabularies
│   ├── literature_search_protocol.md
│   ├── reproducibility_tiering.md  # Tiering rubric and worked examples
│   └── ai_usage_log.md             # Contemporaneous AI-assistance log
├── figures/            # Publication-quality figures (300 dpi)
├── manuscript/
│   ├── data_descriptor/
│   └── poster/
├── notebooks/          # Jupyter notebooks (00_setup_check, 01_corpus_overview)
├── references/
│   ├── papers/                     # Source PDFs (gitignored, copyright)
│   ├── bibliography.bib
│   └── paper_tracking.csv          # Screening audit trail
├── scripts/            # Standalone entry points (validate_data.py)
├── src/
│   └── hycan/          # Python package: schema, normalize, validate, clean, plotting
├── tests/              # pytest suite (test_schema, test_normalize, test_validate)
├── CHANGELOG.md
├── CITATION.cff
├── pyproject.toml
├── requirements.txt
└── ruff.toml
```

---

## Installation

Requires Python 3.10+.

```bash
# 1. Clone the repository
git clone https://github.com/[username]/hycan-db.git
cd hycan-db

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install the hycan package in editable mode
python3 -m pip install -e .
```

---

## Quick Start

The dataset ships as a single CSV at `data/raw/measurements_v0.1.csv`. Load it and
reproduce the Chahine-rule figure with a few lines:

```python
import pandas as pd
from hycan.plotting import set_house_style, fig3_chahine

df = pd.read_csv("data/raw/measurements_v0.1.csv")
set_house_style()
fig3_chahine(df)
```

The corpus-overview notebook (`notebooks/01_corpus_overview.ipynb`) reproduces all
three figures end-to-end, with narration walking through each step.

---

## Data and code availability

The curated dataset lives in this repository at `data/raw/measurements_v0.1.csv`,
alongside the code in `src/hycan/` used to validate, harmonise, and plot it. A
citable Zenodo DOI will be minted at the v1.0 release.

> **Zenodo DOI:** _(placeholder — a DOI will be minted at v1.0; none exists yet)_

Literature PDFs are excluded from this repository due to copyright restrictions;
provenance metadata is included so all sources can be independently retrieved.

---

## Reproducibility tiering

Every measurement in HyCAN-DB carries a reproducibility tier (A–D) reflecting how
completely the source reports the information needed to reproduce it. The scoring
criteria, the physics-override clause, and worked examples are documented in
[`docs/reproducibility_tiering.md`](docs/reproducibility_tiering.md).

---

## AI assistance disclosure

Code in `src/hycan/` and the analysis notebooks was drafted with AI assistance
(Claude and Claude Code) under human review; all scientific decisions, data
extraction, verification against source papers, tiering judgments, and analytical
interpretations are the author's own. A contemporaneous log is maintained in
[`docs/ai_usage_log.md`](docs/ai_usage_log.md).

---

## Citation

If you use HyCAN-DB in your work, please cite using the metadata in
[`CITATION.cff`](CITATION.cff).

---

## License

- **Code** (`src/`, `scripts/`, `notebooks/`): [MIT License](LICENSE)
- **Curated data** (`data/`): [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## Acknowledgements

_Acknowledgements will be added before submission (advisors, institutions, data sources, compute resources)._
