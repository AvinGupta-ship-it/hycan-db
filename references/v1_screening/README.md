# v1.0 title-and-abstract screening (protocol §6, §7)

The 11,238 merged records (`references/v1_search/merged_records.csv`, SHA-256
`e276a0ca…41e5`) were screened on 2026-10-28 (UTC) by two screeners, each
seeing only the six screening columns (`frame_id`, title, abstract, venue,
year, type):

- screener A: `claude-opus-5-5`; screener B: `claude-sonnet-5-5`;
- the frozen prompt `prompts/v1/built/screen.md` (SHA-256
  `41291c79e05592e7c7d36ebc2ef9bb8d9c1a683cffa01d5521d41e0020b971db`,
  Amendment 1), started with the frozen launcher
  (`prompts/v1/built/launcher.md`, SHA-256 `4e8680db…c928`) filled with the
  agent's paths;
- agents ran from the frozen tools directory (`scripts/v1_tools_tree.py`);
  no agent saw a v0.1 row, a pilot output, the repository or the other
  screener's output.

## Batches and agents

- `scripts/v1_search/screening_batches.py split --size 100` cut the merged set,
  in `frame_id` order, into 113 batches (112 of 100 records, one of 38). Each
  batch was screened by one agent per screener: 226 agents, at most 20 running
  at a time.
- Each agent had its own directory holding only its copy of the batch (`in/`),
  its output (`out/`) and its work directory (`work/`).
- `scripts/v1_search/screening_runs.py` checked every finished agent: its
  first message is the filled launcher; the prompt file is the frozen
  `screen.md`; every turn was written by that screener's model; the access
  audit (`scripts/v1_audit_access.py`, Amendment 1, item 26) flags no call, or
  every flag has a review that found no access; and the output screens exactly
  its input batch. All 226 standing agents pass (`access/<S>_batch_NNN.json`;
  3,609 tool calls).
- The audit flagged 5 calls in 2 agents. Each was reviewed against the
  transcript (`access_reviews.json`); none opened anything outside the
  agent's own paths. In B batch 087, four commands printed a `~` as a bullet
  from a Python string; in B batch 105, the agent piped the first bytes of its
  own output through `od -c`.
- `screening_batches.py join` then checked each output against its batch
  again and joined them into `screen_a.csv` and `screen_b.csv`
  (`screen_a_report.json`, `screen_b_report.json`). Every exclusion and every
  S1 flag carries an evidence quotation, and every quotation is found in its
  record's title or abstract. In 53 records the source stores the abstract's
  line breaks as the two characters `\n`. The check now reads those two
  characters as a space, so a quotation that spans a line break is matched.
  Before this change, two quotations by screener A were reported as not found.

### Reruns (protocol §9: technical failure only)

- **Usage limit.** Between 20:30Z and 20:34Z, 20 agents (A and B, batches
  040–049) stopped with HTTP 429 "You've hit your 5-hour limit". Each batch was
  rerun once with a fresh agent and a fresh copy of its input, once requests
  were accepted again. The
  stopped agents are listed in each report's `earlier_agents`. One of them
  (A batch 041) had written an output file but had not finished; that file
  was not used.
- **Container restart.** At about 23:02Z the session's cloud container was
  restarted. Eight running agents (A 106, 107, 109, 112; B 106, 109, 111, 112)
  stopped mid-turn with no error, and the harness kept no record of them. Each
  batch was rerun once in the same way. The stopped agents are listed in each
  report's `unfinished_agents`. One of them (A batch 106) had written an output
  file but had not finished; that file was not used.
- No batch was rerun for any other reason, and no output was discarded under
  item 26.

## Results (`screening_counts.json`)

| | Screener A | Screener B |
|---|---:|---:|
| include | 1,608 | 1,408 |
| uncertain | 3,268 | 3,539 |
| exclude | 6,362 | 6,291 |
| `theoretical_only` | 2,260 | 2,159 |
| `not_carbon` | 1,731 | 1,789 |
| `electrochemical` | 1,254 | 1,249 |
| `not_primary` | 1,112 | 1,086 |
| `retracted` | 5 | 8 |
| S1 flags | 171 | 168 |

- **Agreement**, include-or-uncertain against exclude (§6): 94.0%,
  Cohen's κ = 0.877. With an abstract (6,423 records): 94.7%, κ = 0.886.
  Without one (4,815): 92.9%, κ = 0.858. A alone kept 304 records, B alone 375.
  Only 3 records were included by one screener and excluded by the other.
- **Records without an abstract**, by source: OpenAlex 4,515 of 10,043
  (45.0%); Semantic Scholar 5,851 of 8,608 (68.0%); the merged set 4,815 of
  11,238 (42.8%). Records without an abstract were screened on title and venue
  (§6).
- **Stratum.** 4,572 records were kept by both screeners. Their flags
  disagreed on 8, which went to the stratum tiebreaker:
  - the frozen `stratum_tiebreak.md` (SHA-256 `8245414b…745bb`), model
    `claude-opus-5-5`, started with the frozen launcher;
  - its input held only `frame_id`, title, abstract and the two flags in
    sorted order (`stratum_tiebreak_input.csv`, written by
    `build_frame.py tiebreak-input`);
  - it set S1 for 7 records and S2 for 1 (`stratum_tiebreak.csv`, with
    quotations);
  - its access audit flags no call (`access/stratum_tiebreak.json`).

## Frame (§6, §7)

`scripts/v1_search/build_frame.py` (`references/v1_search/frame_counts.json`):

| | Records |
|---|---:|
| Merged | 11,238 |
| Excluded by both screeners (`double_excluded.csv`) | 5,987 |
| **Frame** | **5,251** |
| S1 | 176 |
| S2 | 5,075 |

`references/v1_search/frame.csv` SHA-256
`814f47cf446b91d545cd4b359e0e17bdc460fd8e86a489a924e221443cc23171`.

The frame was built with `build_frame.py` as registered in 0190009. The copy
here also has a `tiebreak-input` command, added after screening, which writes
the tiebreaker's input. Its `build()` is unchanged, and the registered file
reproduces all three outputs byte for byte. Re-running the current script
reproduces them as well.

## Screening sensitivity (§6; `sensitivity.json`)

`scripts/v1_search/reference_sets.py sensitivity`: of the reference-set papers
in the merged set, the share that reach the frame.

- **Set A** (Appendix B, the v0.1 papers): 44 of 44 (100%). Both screeners kept
  all 44. The prompts were piloted on v0.1 papers, so this is optimistic (§6).
- **Set B** (`references/v1_setB/`): 4 of the 5 in the merged set (80%).
  - The record not kept is W2067236644 (F02682), "MOF-5 composites exhibiting
    improved thermal conductivity". It has no abstract, and both screeners
    excluded it as `not_carbon`.
  - In the set-B screening, run on the review's 91 references with the same
    prompt and models, both screeners had marked the same title-only record
    uncertain.
  - The difference shows that screening by title alone varies between runs.
  - MOFs are not carbon sorbents (§3).
- **Set B, include by both screeners:** 2 of 2 (100%).

## Files

| File | What it holds |
|---|---|
| `screen_a.csv`, `screen_b.csv` | Each screener's row for every merged record |
| `screen_a_report.json`, `screen_b_report.json` | Counts and the evidence-quotation check of each join |
| `stratum_tiebreak_input.csv`, `stratum_tiebreak.csv` | The tiebreaker's input and its decisions |
| `double_excluded.csv` | The records both screeners excluded (the §6 author-audit population) |
| `screening_counts.json` | The counts above (`scripts/v1_search/screening_counts.py`) |
| `sensitivity.json` | Screening sensitivity on sets A and B |
| `access/` | The check of every agent (`screening_runs.py`) and the tiebreaker's access audit |
| `access_reviews.json` | The review of every audit flag |
