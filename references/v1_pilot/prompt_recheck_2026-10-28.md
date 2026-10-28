# Re-check of the second review's findings, before the freeze

A checker agent (`claude-opus-5-5`) in a fresh context. Kept verbatim; the README says what was changed in response. Paths refer to the working copy at the time.

**HyCAN-DB Amendment 1 check: not ready to freeze.** B6 is still broken. B1 and B3 each need a small fix before freezing, because the amendment wording can't be changed afterwards. Everything else checks out.

**Baseline:** the full suite gives `1054 passed`, and `v1_prompts.py --check` gives `built prompts match`.

**B1 value_kind: NOT FULLY FIXED, BLOCKING (one phrase)**
- Fixed: the rule matches §3, the no-point exception is declared as a clarification (item 16), and the same text is in extract.md:119-126, reconcile.md:88-93 and the built prompts.
- Gap: "equals" is defined only as "the point it was merged with, or within 3% of a digitized point" (amendment lines 121-123).
  - A maximum stated in the text whose isotherm is printed only as a table (item 13) equals a printed point but passes neither test.
  - The no-point clause doesn't apply either, because points are shown.
  - So the literal result is `fitted_extrapolated`, which goes against §3.
  - "Within 3% of a digitized point" also doesn't say the point must be from the same isotherm.
- Fix, in all three places: "it is the point it was merged with (item 12), has the value of a printed point of the same isotherm, or lies within 3% of a digitized point of the same isotherm."

**B2 basis constant within an isotherm: FIXED**
- v1.py:397-400 raises "mixes bases".
- The rule is in extract.md:114-116, reconcile.md:85-87 and item 13.
- `v1_extract.py check` on a synthetic output with mixed bases in I1 printed `['I1']` and exited 1.
- Small overstatement: item 13 says `hycan.v1` refuses any mixed isotherm, but it only checks 77 K isotherms.

**B3 validator messages: FIXED except one case, BLOCKING (wording)**
- Five of the six test rows give their own message:
  - no temperature, no flag → `Missing required field: temperature_k`
  - `*_unstated` flag with a value filled → `Invalid row: temperature_unstated is set but temperature_k is populated…`
  - volumetric capacity without basis → `Invalid row: … volumetric_capacity_basis is null…`
  - ultramicropore volume without cutoff → `Invalid row: … ultramicropore_cutoff_nm is null…`
  - surface-area method `none` with an area → `Invalid row: surface_area_method is 'none' but … bet_surface_area_m2_g`
  - A row with no uptake at all still gives `Missing required field: uptake`, which is correct.
- The sixth row, which has only `uptake_ml_stp_g`, still gives `Missing required field: uptake`.
  - Cause: validate.py:159 lists that rule's message among the no-uptake prefixes, and tests/test_schema_v2.py:153-156 asserts that output.
  - This contradicts item 27's "every model-level rule in its own words".
- Fix: delete that prefix and update the assertion. On a scratch copy with that change, only that one assertion fails (1053 passed). The alternative is to reword item 27.

**B4 redacted dictionary: FIXED**
- Both redacted files rebuild byte-identical from the script.
- Paragraphs 215 and 216 are now rewritten with their rules intact.
- I compared all rewritten paragraphs against the registered text: every rule is kept. The six dropped paragraphs are history and counts only.
- No v0.1 paper ID or author-year pair survives. The redacted schema.py has the same syntax tree as the registered file minus its docstrings.
- Item 24 describes the script correctly: field names are checked in both files, vocabulary values in schema.py.

**B5 reference set B: FIXED**
- Item 9 keeps records without an abstract unless both screeners exclude them.
- Identifying set B at title and abstract is justified by §6, which reads full text only for drawn records.
- Recall is also reported on the both-`include` subset, split by abstract, and the sensitivity caveat is stated. Consistent with §§5–6.

**B6 agent confinement: NOT FIXED, BLOCKING**
- What works:
  - pytest: 3 passed.
  - Re-auditing the five round-3 transcripts gives 0 flags (once the tool-results folder is passed as `--harness`).
  - 11 normal-use calls were not flagged.
  - Direct absolute-path reads of other agents' outputs or `measurements_v0.1.csv` are flagged.
- Synthetic transcripts that were **not flagged**:
  - (d) `..` climbing:
    - Read `<work>/../../out_A/P1/rows.csv`
    - `cat <work>/../../out_A/…`
    - `cd .. && cd ..`, `ls ..`, `find ..`
    - `os.listdir('..')`
    - a Glob pattern of `../../out_A/**`
  - (b) the v0.1 rows: `cat ~/work/hycan-db/data/raw/measurements_v0.1.csv`, and the same via `$HOME/…`.
  - (c) the tools directory:
    - `ls <tools>`, `ls -la <tools>/`, `find <tools>`
    - after `cd <tools>`: `python3 -c "open('src/hycan/schema.py')"`, a heredoc that reads it, `grep -rn uptake` with no path, `cd scripts && cat …`, `cp -r src <work>`
  - Other gaps:
    - Tools other than the eight it checks are ignored: MultiEdit, LS, Task subagents, MCP reads (Drive, project, memory), and `curl`.
    - A Write into the input directory passes, although item 26 says written files are checked to lie in the output and work directories.
    - Paths are recognised only if their top-level folder exists on the machine running the audit. `/Users/…` is invisible here (tested).
- So item 26's "flags every file it opened, and every path its commands name" is not true.
- Fix, in code plus tests:
  - normalise every path before the prefix check, and flag any `..` component;
  - flag `~`, `$HOME` and `${HOME}`;
  - inside the tools directory, allow only the two `python3 scripts/…` commands (plus `cd` and filters on their output);
  - flag any tool not on an allowlist (Read, Write, Edit, Glob, Grep, Bash), and flag curl, wget and URLs;
  - limit Write and Edit to the output, work and harness folders;
  - recognise any `/name/…` path, not only top-level folders that exist locally.
- Then reword item 26 to call the Bash check a heuristic that flags for review.
- Also extend item 26's discard rule to the reconciler, tiebreaker and resolver opening v0.1 rows, pilot outputs or the repository. It currently covers only screeners, assessors, extractors and the labeller.

**Non-blocking items**
- W1 factor: FIXED. v1_extract.py:51 uses 0.0089938, the same as the prompt and §11.0. v1.py works out to 0.00899384, a relative difference of 5e-6, which doesn't matter.
- mg/g axis span: FIXED (v1_extract.py:416-419, with a test).
- v0.1 rows without pressure matching a digitized-pressure row: FIXED (v1_extract.py:203-205, and described in the built reconcile_legacy prompt).
- Unlabelled-sample naming: FIXED. It reads the same in extract.md:76, reconcile.md:70, legacy_labels.md:26 and item 17.
- Curve grid near zero: FIXED (extract.md:245-251 matches item 21). Every grid point now lies between the line's two ends.
- I1 failure means I2–I4 not assessed: FIXED in eligibility.md, eligibility_resolve.md:47-48 and item 4.
- Reconciler characterization sentence: FIXED (reconcile.md:62-65).
- Tools-directory wording: FIXED and consistent (extract.md:264-265, reconcile.md:140-141, launcher.md:13-15).
- "Not piloted in final form": present, but it leaves out that `stratum_tiebreak` and `eligibility_resolve` were never run at all. There are no outputs in references/v1_pilot, even though round 1 had two stratum splits and an I4 split. Add one sentence before freezing.

**One side effect of my check:** `v1_tools_tree.py --help` treats `--help` as the output folder and wrote `--help/` into the repo root. I moved it to `/tmp/claude-0/-home-claude/663fb236-481a-5f2f-b02f-82bfd72801cf/scratchpad/tools_tree_built`, and `git status` no longer shows it. No other file was changed.
