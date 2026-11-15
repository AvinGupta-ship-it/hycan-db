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
| `agreement_dual.json`, `agreement_legacy.json` | The §9 agreement statistics (`scripts/v1_search/agreement.py`), dual and legacy papers separately: per-field agreement, row detection, C's outcomes, and per-paper row counts. |

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
had finished (B's `rows.csv` had not changed). On HYC-0033, extractor B ended
a turn while a search script of its own still ran in the background; the
harness marks such an agent finished before it has delivered its report, so
`assemble` started while B had written no `rows.csv` yet and stopped with an
error after copying the first extraction. That partial input was set aside
before any reconciler was started. An agent now counts as finished only once
its transcript holds its report (its `SubagentHandback` call), `assemble`
checks every input before it writes anything, and HYC-0033 was assembled again
after B reported. For every other assembled paper the reconciler's copies
equal the extractors' final outputs.

Extractor A on HYC-0123 separated two pairs of overlapping markers that the
digitizer had returned as single clusters, and stored the four points in an
archive of its own (`HYC-0123_fig6_PG_split.json`), which names in
`calibration_from` the digitizer's archive whose axis calibration it read them
on. Assembly took the axis span (protocol, Amendment 1 item 21) only from an
archive's own calibration, and stopped with an error after writing part of
the reconciler's input. That partial input was set aside before any reconciler
was started; assembly now follows `calibration_from` to an archive in the same
folder, and the paper was assembled again (its `match.csv` was unchanged).

### Interruptions

On 29 Oct 2026 the account's five-hour usage limit, and an hour later its
weekly limit, stopped every running agent mid-task (an API error, not an end
of the task). No such agent was restarted. Each was resumed in its own session
once the limit had reset, with one fixed message: "Your session stopped on an
API usage limit, not by your choice. Continue your task from where you
stopped; your instruction file, input, output and work directory are
unchanged, and the same rules apply."

On 3 Nov 2026 (01:32 UTC) the operator paused the run to free the account's
usage for other work. The 13 agents then running (extractor A on HYC-0121,
HYC-0122 and HYC-0124; extractor B on HYC-0115, HYC-0116, HYC-0118, HYC-0119,
HYC-0121, HYC-0122 and HYC-0123; reconciler C on HYC-0022, HYC-0031 and
HYC-0101) were stopped with the harness's task stop, which writes "[Request
interrupted by user]" (or, during a tool call, "[Request interrupted by user
for tool use]") into the transcript. None was restarted. Each was resumed in
its own session on 9 Nov 2026 with a second fixed message: "Your session was
paused by the run operator to free account usage, not by your choice. Continue
your task from where you stopped; your instruction file, input, output and
work directory are unchanged, and the same rules apply."

Every check report records the number of stops of each kind
(`api_error_stops`, `operator_stops`) and every message the operator sent
after the launcher (`operator_messages`). A report fails if any such message
is not one of the two fixed texts, or does not answer a stop of its own kind
since the previous message (the first text an API-error stop, the second an
operator stop). The harness's own error entries (model `<synthetic>`) are left
out of the model check. An interrupted agent is not treated as finished, so
nothing is assembled or collected from it until it ends its task.

Until 9 Nov 2026 this check read the operator's messages from the agent's
ordinary user entries only. The harness records a message sent to an agent as a
metadata entry of origin "coordinator", between a fixed line before it ("The
coordinator sent a message while you were working:") and one after it
("Address this before completing your current task."), so no report listed the
resume messages and the check passed without testing them. It now reads those
entries, removes the two fixed lines, and every report was recomputed with it.

Some agents' contexts filled and were compacted automatically by the harness
(a summary written in the same session); each report counts these
(`compactions`).

## Agent checks

`extraction_runs.py` checks every finished agent (launcher, frozen prompt,
model, access audit, output) and, on every run, that the shared tools
directory holds exactly its MANIFEST files, unchanged. Every audit flag is read
against its call and recorded in `access_reviews.json`. The command heuristic
flags text, not actions: a `~` in a quotation or comment, a Python variable
named `nc`, a path built inside the agent's own work directory. Those reviews
say so.

Two gaps in the access audit (`scripts/v1_audit_access.py`, shared with the
earlier stages and left unchanged) showed up during the run: it accepts any
command that names one of the two tool scripts, so it does not see a script's
source being read, and it accepts any path that begins with `/dev/null`, so it
does not see a file such as `/dev/null.png` being written. `extraction_runs.py`
therefore adds its own checks, applied to every agent's transcript including
those already checked. These checks flag a call that reads or lists a file in
the tools directory, whether by an absolute path, a relative path while the
tools directory is the working directory, or Python code that opens or imports
one. They also flag a call that names a device path other than `/dev/null`,
`/dev/stdout` and `/dev/stderr`. Their flags are reviewed like the audit's (the
reason ends "(supplementary check)"). A check report is cached against
everything it depends on (the transcript, the agent's run directory, its
launcher, the prompts and the checking code) and recomputed when any of them
changes. Reviews are applied afresh on every run.

Under Amendment 1, item 26, an output is discarded only if its agent opened
another agent's output for the same paper, a v0.1 row, a pilot output or the
repository. No agent has done so: no reviewed flag found such an access, and
every report also lists each tool call that names the repository, the v0.1
rows file, another agent's run directory or another stage's run folder
(`cross_access`), which is empty for every agent. An agent that went outside the launcher's
list without reaching any of those keeps its output, and the breach is
recorded in its review:

- listing the tools directory's `scripts/` folder, which holds only the two
  scripts: extractor A on HYC-0068, HYC-0076, HYC-0044, HYC-0031 (with the
  tools directory itself), HYC-0106 (not self-reported), HYC-0101 (the tools
  directory itself) and HYC-0116 (the tools directory itself, not
  self-reported), and reconciler C on HYC-0100 (whose listing went to
  `head -0`, so it saw nothing), on HYC-0101 (which printed the two script
  names) and on HYC-0124 (to `head -0`, so it saw nothing). Reconciler C on
  HYC-0026 ran `ls` on `scripts/digitize_figure.py` itself, which printed only
  that path;
- reading a tool script's source: extractor A on HYC-0094 (`sed` of
  `digitize_figure.py`, piped to `head -0`, so nothing was printed),
  extractor A on HYC-0096 (`grep` of `validate_row_detail.py` for the message
  its validator run had printed), extractor A on HYC-0124 (`cat` of
  `digitize_figure.py`, piped to `head -0`, so nothing was printed; not
  self-reported) and extractor A on HYC-0135 (`sed` of `digitize_figure.py`,
  which printed its first 60 lines; not self-reported). Neither file holds
  paper data;
- listing the folder that holds the run folders of every stage
  (`/home/claude/work/runs`, reached as `ls ../../../../`): extractor A on
  HYC-0095, which saw the five folder names (`elig`, `extract`, `screen`,
  `setB`, `tiebreak`) and opened nothing inside them. This one was not
  self-reported; the audit found it;
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
  any of those folders, so no paper's rows contain another's digitizations.
  After the tools directory was made immutable (below), the same mistake by
  extractor B on HYC-0093 (`trial/`), extractor A on HYC-0098 (`dg/`),
  extractor B on HYC-0111 (`trial/`), extractor A on HYC-0124 (`trial/`,
  not self-reported), extractor B on HYC-0124 (`trial/`), extractor B on
  HYC-0034 (`trial/`), extractor B on HYC-0045 (`trial/`), extractor B on
  HYC-0047 (`trial/`) and extractor B on HYC-0060 (`testruns/`) was refused,
  and nothing was written;
- writing a scratch image of the agent's own page to `/dev/null.png` and
  removing it: extractor B on HYC-0048 and, hours later, extractor B on
  HYC-0095. Neither read the file back as input. Extractor B on HYC-0021
  passed `/dev/null` as the image output path of its own helper script; the
  command failed and nothing was written. Extractor B on HYC-0053 had its own
  helper write a test image of its own figure to `/tmp/x.png`, a shared
  temporary folder, and deleted it in its next call; it never read the file,
  and no other transcript names it. Listing a system font folder
  (extractor B on HYC-0068 and on HYC-0099, which also loaded two DejaVu fonts
  from it to label its own overlay images), loading one of those fonts to
  label its own check images (reconciler C on HYC-0039 and extractor B on
  HYC-0049) and looking up programs on the
  system path with `which` (reconciler C on HYC-0087, HYC-0022 and HYC-0116)
  reach no paper data.

Except where stated, all of these were reported by the agents themselves
after their reply. The tools check above was added after the first, because
the access audit sees a write made through a script's output argument only
when the agent reports it. At 22:27 UTC on 29 Oct 2026 the tools directory was
made immutable (`chattr +i`), so that a relative output path now fails at once
instead of writing there; its files and MANIFEST are unchanged, and both
scripts run as before.

## Agreement statistics (§9)

`scripts/v1_search/agreement.py` recomputes the §9 matching
(`scripts/v1_extract.py`) for every paper from the collected outputs — for a
legacy paper, the v0.1 rows against extractor B — and reports per field type
through `scripts/v1_agreement.py`, writing `agreement_dual.json` (80 papers)
and `agreement_legacy.json` (43 papers). Numbers below are from those files;
rerun the script to regenerate them.

On the legacy papers, `only_second` dominates row detection by design: the
v0.1 extraction recorded chiefly reported values and maxima, while the §9
prompt digitizes every plotted point of every 77 K isotherm, so most of B's
rows have no v0.1 counterpart and go to C as B-only rows (C kept nearly all of
them). The informative legacy numbers are the matched share of the v0.1 rows
(335 of 398; the 63 unmatched went to C as row decisions) and the field
agreement on the matched pairs.

## Schema limits met in extraction

- `temperature_k` is registered as 50–500 K. An uptake measured at a stated
  temperature above 500 K (HYC-0062: 653 K, and a 673 K temperature-cycle
  value) cannot be stored there. The extractors, like v0.1, leave it empty,
  set `temperature_unstated = true` and give the printed temperature in
  `notes`; for those rows the flag does not mean "never stated". No §11
  analysis uses a row above 303 K.
- `volumetric_capacity_kg_m3` is registered as 0–200; a larger printed value
  (HYC-0062, 280 g/L) is kept in `notes`.
