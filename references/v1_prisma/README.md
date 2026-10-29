# v1.0 PRISMA 2020 flow (protocol §6, §14)

`scripts/v1_search/prisma.py` computes every count in the flow from the
committed files and draws the diagram; nothing here is typed by hand (§14,
"Generated outputs").

| File | Content |
|---|---|
| `prisma_counts.json` | The counts at each §14 stage, with the inputs' SHA-256. |
| `prisma_flow.pdf`, `prisma_flow.png` | The flow diagram (Page et al. 2021), drawn from `prisma_counts.json`. |

## Stages and sources

- **Identified, merged.** `references/v1_search/merge_counts.json`
  (`merge_search.py`), checked against `merged_records.csv` by its SHA-256.
  OpenAlex records are counted as distinct work IDs before the 5 pairs that
  share a DOI are merged (10,043 + 5); the hits over the 160 sub-queries are
  shown as well, because the sub-queries overlap. Duplicates removed are those 5
  and the Semantic Scholar records matched to an OpenAlex record by DOI or by
  title and year.
- **Screened.** Both screeners' files (`references/v1_screening/`). A record
  is excluded when both screeners exclude it (§6); the diagram gives the codes
  where the two agree, and the number where they differ.
- **Frame.** `references/v1_search/frame.csv`, per stratum.
- **Drawn, retrieved, assessed, eligible.** The §7 walk, computed by
  `fulltext.walk` from `references/v1_fulltext/`. "Drawn" is the records the
  walk took. A record not reached by the walk enters no later count. The seven
  S1 records retrieved past the stop (two of them assessed) are outside the
  sample and are only noted.
- **v0.1 papers.** The 51 papers with rows in `data/raw/measurements_v0.1.csv`,
  joined to the frame by DOI through `references/paper_tracking.csv`. §7 has
  every v0.1 paper assessed, drawn or not, so the diagram gives them a lane of
  their own: the 7 drawn are counted in the sample, and the 44 not drawn are
  followed through retrieval and assessment to `legacy_v0.1`.
- **Author's review.** `references/v1_fulltext/author_review.csv` must cover
  exactly the full-text exclusions. The script refuses to run if a reversal is
  recorded but not yet applied to `eligibility.csv`.
- **Analysed (per RQ).** Not yet computed. The §11 analyses have not been run,
  and the diagram says so.

## Reproducing

    .venv/bin/python scripts/v1_search/prisma.py

Under `requirements-v1.lock`, a re-run reproduces all three files byte for
byte. `tests/test_v1_prisma.py` checks that the committed counts are
reproduced. In another environment the PDF and the counts were also
reproduced, but the PNG was not: its rasterisation depends on the installed
libraries.
