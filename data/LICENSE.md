# Licence for the HyCAN-DB dataset

**The contents of this `data/` directory are licensed under the Creative Commons
Attribution 4.0 International Licence (CC BY 4.0).**

- Human-readable summary: <https://creativecommons.org/licenses/by/4.0/>
- Full legal code: <https://creativecommons.org/licenses/by/4.0/legalcode>

Copyright (c) 2026 Avin Gupta.

## This is not the licence on the code

The repository root carries an [MIT licence](../LICENSE), and it covers `src/`,
`scripts/` and `notebooks/` — **not** this directory. The two are deliberately
different, because a permissive code licence and an attribution-requiring data
licence protect different things: MIT lets anyone reuse the pipeline, and CC BY
requires that anyone redistributing the curated measurements says where they came
from. Publishing a curated dataset under a code licence is a mistake that is hard
to unwind once a DOI has been minted, so the boundary is stated here rather than
left to be inferred from the root.

## What you may do

Share and adapt the data for any purpose, including commercially, provided you
give appropriate credit, link to this licence, and indicate whether you made
changes. You may not apply legal or technological measures that restrict others
from doing anything the licence permits.

## How to attribute

Cite the dataset itself, not only the papers it draws on:

> Gupta, A. (2026). *HyCAN-DB: a curated database of hydrogen sorption
> measurements in carbon nanomaterials.* <https://github.com/AvinGupta-ship-it/hycan-db>

Once a Zenodo DOI is minted it replaces the repository URL in that citation, and
`CITATION.cff` at the repository root carries the canonical form.

## What this licence does and does not cover

**Covered:** the curated database — `raw/measurements_v0.1.csv`, the archived
figure digitizations in `digitizations/`, and any built file placed in
`processed/`. These are this project's own work: the selection, extraction,
normalisation, provenance annotation and reproducibility tiering of values
reported in the literature.

**Not covered, and not redistributable under it:**

- **The source papers.** No PDF is in this repository. `references/papers/` is
  gitignored, and the papers remain under their publishers' copyright. Every row
  carries a DOI so the original can be obtained through normal channels.
- **Individual measured values as facts.** A number reported in a published paper
  is that paper's finding. This licence covers HyCAN-DB's curation of those
  values, and it does not purport to license the underlying facts or to transfer
  any right the original authors hold. Anyone relying on a specific value should
  cite the paper as well as this dataset — which is what `paper_id`, `doi` and
  `source_location` on every row exist to make possible.
- **Any figure reproduced from a paper.** None is included. Where a value existed
  only in a figure it was digitized to coordinates; the archived digitization
  records the extracted series, not the image.

## Before you rely on these numbers

The dataset is curated, not authoritative, and it says so in its own
documentation. Two things in particular:

- **Every row carries a `reproducibility_tier`, and the tiers are not
  interchangeable.** Tier D rows are retained deliberately because they document
  the field's contested history — several are claims the literature has not
  reproduced. Aggregating across tiers without showing the comparison separately
  will mislead you. `docs/reproducibility_tiering.md` gives the rubric.
- **The dataset deliberately holds rows that must not enter an average.** Some are
  non-isothermal, some are bounds rather than values, some have a condition their
  paper never stated, and some carry no gravimetric uptake at all. Filter before
  you aggregate; the execution manual's §12.3 states the filter and the counts.

`docs/extraction_provenance.md` records how the rows were produced, including the
fact that most were extracted by an AI pipeline under dual-agent verification,
the measured dispute rate, and the pipeline's known failure modes. Read it before
relying on the data.
