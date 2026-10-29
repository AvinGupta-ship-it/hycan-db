# v1.0 extraction (protocol §9)

This directory holds the record of the extraction stage: which papers are
extracted and how, every agent's output (§9, "Release"), and the checks on the
agents. The run is driven by `scripts/v1_search/extraction.py`, and each agent
is checked after it runs by `scripts/v1_search/extraction_runs.py`.

## Files

| File | Content |
|---|---|
| `papers.csv` | Every paper with a `selection_route` (§7, Amendment 2): its `paper_id`, frame record, mode, stratum and draw position, whether it is a v0.1 paper, and the identity copied into its rows (DOI, first author, year, journal, title). Written by `extraction.py plan` from the committed walk, eligibility outcomes and v0.1 rows. |
| `identity.csv` | For each new paper, the first author's family name and the journal as printed on the article (data dictionary, `first_author`, `journal`), read from the article's first page. |
| `<paper_id>/A`, `B`, `L`, `C` | Each agent's output, unchanged: `rows.csv`, `digitizations/` and `log.md` (extractors), `labels.csv` (labeller), `rows.csv` and `resolutions.csv` (reconciler). |
| `<paper_id>/C_input/` | What code gave the reconciler: `match.csv`, `digitized_means.csv`, and `labels.csv` for a v0.1 paper. |
| `access/` | One check report per agent (launcher, frozen prompt SHA-256, model, access audit, output). |
| `access_reviews.json` | Each audit flag reviewed against its call, with the finding. |

## Modes (§9)

- **dual**: the 80 papers of the probability sample (S1 60, S2 20), including
  the 7 v0.1 papers the walk drew. Extractor A (`extract_A.md`,
  `claude-sonnet-5-5`, text layer and page images) and extractor B
  (`extract_B.md`, `claude-opus-5-5`, page images only) work blind to each
  other and to any existing row; code matches their rows (§9 rule,
  `scripts/v1_extract.py`); reconciler C (`reconcile.md`, `claude-opus-5-5`)
  resolves every disagreement against the PDF.
- **legacy**: the 43 v0.1 papers outside the sample that a §8 route retrieved,
  eligible (36, `legacy_v0.1`) or not (7, `legacy_v0.1_ineligible`): §9 gives
  "every other v0.1 paper" one fresh blind extraction by B. The labeller L
  (`legacy_labels.md`) first gives each v0.1 sample its printed label; code
  matches the v0.1 rows to B's rows; reconciler C (`reconcile_legacy.md`)
  resolves them against the PDF. The rows of the 7 ineligible papers are
  released and enter no analysis (§7).
- **none**: HYC-0041, which no §8 route yielded (`legacy_v0.1_not_retrieved`,
  Amendment 2): its v0.1 rows are kept unchanged and it is not extracted.

## Identifiers and identity

- A v0.1 paper keeps its `paper_id`. A new paper takes the next unused ID
  after the v0.1 papers (data dictionary, `paper_id`), in stratum order (S1,
  then S2) and draw order: HYC-0066 to HYC-0138.
- The identity fields every agent copies into its rows come from `paper.json`.
  For a v0.1 paper they are its v0.1 values, so that the legacy matching does
  not report a difference in every row. For a new paper the DOI, year and
  title are those of the search record, and the first author and journal
  are read from the article (`identity.csv`): OpenAlex's author names do not
  separate the family name (for HYC-0048 it gives "Gentil Mwengula", whose
  family name is Kahilu), and its venue names drop colons. Two DOE final
  reports carry "U.S. Department of Energy Final Report" as the journal, a
  conference paper deposited in HAL its conference, and a book chapter
  "InTech (book chapter)", as their first pages print no journal.

## Run

Every agent is started with the frozen launcher, filled with the paths of its
instruction, the tools directory, its input, output and work directory; its
input is built under a parent of its own. The prompts and the tools directory
are checked against their Amendment 1 SHA-256 values before any input is
prepared. Agents run at most 20 at a time.
