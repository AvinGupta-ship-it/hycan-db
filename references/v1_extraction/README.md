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

An agent can write its output file before it has finished revising it, so
`assemble` and `collect` refuse until the agents they copy from have finished
(read from the run's transcripts). That guard was added after HYC-0083 was
assembled while extractor B was still running; the assembly was set aside
before any reconciler was started, and the paper was assembled again once B
had finished (B's `rows.csv` had not changed). For every other assembled
paper the reconciler's copies equal the extractors' final outputs.

## Agent checks

`extraction_runs.py` checks every finished agent (launcher, frozen prompt,
model, access audit, output) and, on every run, that the shared tools
directory holds exactly its MANIFEST files, unchanged. Every audit flag is read
against its call and recorded in `access_reviews.json`. The command heuristic
flags text, not actions: a `~` in a quotation or comment, a Python variable
named `nc`, a path built inside the agent's own work directory. Those reviews
say so.

Under Amendment 1, item 26, an output is discarded only if its agent opened
another agent's output for the same paper, a v0.1 row, a pilot output or the
repository. An agent that went outside the launcher's list without reaching
any of those keeps its output, and the breach is recorded in its review:

- listing the tools directory's `scripts/` folder, which holds only the two
  scripts: extractor A on HYC-0068, HYC-0076 and HYC-0044 (all self-reported);
- writing eight trial digitizations of the agent's own figure to a new folder
  `/work` at the container root, through a mistyped output path
  (`/../work/…` for its own work directory), and listing that folder:
  extractor A on HYC-0085. The harness blocked its attempt to delete them;
  the run operator moved them out of `/work`, and they are kept outside the
  repository. No other transcript names `/work` or those files;
- writing trial digitizations of the agent's own paper into the tools
  directory, because a helper ran the digitizer from there with a relative
  output path, and then deleting or moving them: extractor B on HYC-0068
  (`dz/`), extractor A on HYC-0072 (one file), extractor A on HYC-0075
  (`test/`), extractor B on HYC-0074 (`dig/`), and extractor A on HYC-0048 and
  extractor B on HYC-0075, which used the same folder name (`trial/`) at the
  same time. Each agent read back and deleted only files it had named itself,
  no file names overlapped, and across every transcript no other agent opened
  any of those folders, so no paper's rows contain another's digitizations;
- writing scratch files to system folders (`/dev/null.png`, extractor B on
  HYC-0048) and listing a system font folder (extractor B on HYC-0068).

All of these were reported by the agents themselves after their reply. The
tools check above was added after the first, because the access audit sees a
write made through a script's output argument only when the agent reports
it. At 22:27 UTC on 29 Oct 2026 the tools directory was made immutable
(`chattr +i`), so that a relative output path now fails at once instead of
writing there; its files and MANIFEST are unchanged, and both scripts run as
before.

## Schema limits met in extraction

- `temperature_k` is registered as 50–500 K. An uptake measured at a stated
  temperature above 500 K (HYC-0062: 653 K, and a 673 K temperature-cycle
  value) cannot be stored there. The extractors, like v0.1, leave it empty,
  set `temperature_unstated = true` and give the printed temperature in
  `notes`; for those rows the flag does not mean "never stated". No §11
  analysis uses a row above 303 K.
- `volumetric_capacity_kg_m3` is registered as 0–200; a larger printed value
  (HYC-0062, 280 g/L) is kept in `notes`.
