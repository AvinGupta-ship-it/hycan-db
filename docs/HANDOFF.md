# HyCAN-DB — session handoff

**Written 2026-10-01.** Read this first in a new session, then
`claude/HyCANDB_Execution_Manual_v2.5` (the Project doc) for anything it points
at. **Verify every number below from disk before relying on it** — §0 of the
manual exists because this project has twice recorded a deliverable as done
that was not.

```
git clone https://github.com/AvinGupta-ship-it/hycan-db.git
python3 -m pytest tests/ -q          # expect: all passing
```

---

## 1. State as of this writing

| | |
| --- | --- |
| Papers screened | 65 |
| Extracted | 24 (12 `extracted`, 12 `verified`) |
| Not started | 41 |
| Rows | 259 — 48 A / 160 B / 41 C / 10 D |
| Phase D | 35 screened, 30 obtained, **1 extracted, 29 waiting** |
| 77 K + BET modelling subset | 123 rows, 14 papers |

Deliberately no commit SHA here: a pinned one is stale the moment anything
lands. `git log --oneline -5` is the state.

Five Phase D papers were screened in and **not retrieved** — HYC-0035, HYC-0036,
HYC-0054, HYC-0055, HYC-0056, all Royal Society of Chemistry. They stay
`screening_decision = include`, `pdf_obtained = no`, with the reason in `notes`.
That is a retrieval failure, not an exclusion, and §7.5 requires it as its own
PRISMA line. Do not fold them into the 14 screening exclusions.

## 2. The next action

**Extract HYC-0032** (`Combined experimental and simulation study on H2 storage
in oxygen and nitrogen co-doped activated carbon`, *RSC Advances* 2023; tags
`77K_BET;doped_77K`). Then HYC-0033, HYC-0034, HYC-0037, HYC-0038, HYC-0039 —
the `paper_id` order encodes funnel priority.

**Batch four or five papers per session**, and fan the agent passes out
concurrently: Agent A's locate pass is independent per paper, as is Agent B's
verification. Running them one paper at a time is what made 2026-09-30 a whole
session for one paper. The three-agent protocol itself is not optional (§3.2);
only the waiting is parallelizable.

## 3. The per-paper recipe, with the tooling that now exists

§9.1 has eighteen steps. These are the ones with tools, and the two the manual
omits.

```
# session start -- note the PATH; manual §9.1 writes this flag bare, which is wrong
python3 scripts/append_paper.py --write-baseline /tmp/hycan_baseline.json

# step 10: build the staging file from a JSON spec -- do NOT hand-write 67 columns
cp references/staging/HYC-0031.json references/staging/HYC-00XX.json   # as a model
python3 scripts/build_staging.py references/staging/HYC-00XX.json --dry-run
python3 scripts/build_staging.py references/staging/HYC-00XX.json

# steps 11-14
python3 scripts/append_paper.py data/raw/staging_HYC-00XX.csv \
    --baseline /tmp/hycan_baseline.json --dry-run
python3 scripts/append_paper.py data/raw/staging_HYC-00XX.csv \
    --baseline /tmp/hycan_baseline.json

# step 15 -- the step this project has skipped more than any other
python3 scripts/record_extraction.py --paper-id HYC-00XX --status extracted \
    --append-note "..." --dry-run
```

**Two steps §9.1 does not mention and a test enforces:**

1. **The bibliography.** Add the paper to `references/bibliography_sources.json`
   and run `scripts/build_bibliography.py`.
   `tests/test_bibliography.py::test_every_corpus_paper_has_an_entry` fails
   without it. Provenance values are a controlled vocabulary —
   `{pdf, openalex, semanticscholar, openalex+semanticscholar, none}` — and
   `doi` alone is free text. Two counts in that file are pinned and must be
   updated deliberately (`pdf_held`, and the `number` provenance partition).
2. **The correction check.** Before extracting, establish whether the paper
   carries a published correction. HYC-0031 announced one on its own first page
   and in its footer; it turned out to be author-name only. **32 of the 35
   Phase D papers are still unchecked**, and the screening log §8 records which.
   Crossref through WebFetch is rate-limited and `curl` is blocked at the egress
   proxy, so expect to locate notices by search and read them from PMC.

## 4. Conventions you would otherwise re-derive

Read them out of the data, not out of documentation — but these are what you
will find, and the manual is wrong or silent on several.

- `sample_id` = `HYC-XXXX-SN`, `measurement_id` = `HYC-XXXX-MN`. The builder
  derives both; the spec may not set them.
- `extractor` = `HyCAN pipeline v2` for new work.
- `temperature_k`: **77** for −196 °C, **298** for 25 °C. Not 77.15 —
  `plotting.py` filters the Chahine subset with `df["temperature_k"] == 77`,
  exact equality, so 77.15 silently vanishes from the figure.
- KOH-activated carbons: `synthesis_method = chemical_activation`, with the
  detail in the free-text `activation_method`.
- `surface_area_method = BET` describes `bet_surface_area_m2_g` only; a t-plot
  micropore area shares the row and its method goes in `notes`. Same for
  `pore_volume_method`.
- **Oxygen in an activated carbon is not a dopant.** `dopant_element` holds only
  deliberately introduced heteroatoms — N, Fe, B in the corpus. Every activated
  carbon contains oxygen; if it counted, all 259 rows would be doped. HYC-0031
  was screened in under `doped_77K` on this mistake, so that target is **8 of
  10 obtained, not 9 of 11**. The other ten `doped_77K` titles each name a real
  dopant, but titles are weak evidence and only extraction confirms them.
- `uptake_type`: use the §3.6 exact-word rule. The corpus is mostly
  `unspecified` and §B.5 records that as normal, not as a failure.
- **`total` uptake is new to the corpus** and only HYC-0031 has it. It is not
  commensurable with `excess`: it adds the compressed gas in the pore volume.
  `fig3_chahine` excludes it, and `tests/test_dataset_invariants.py` enumerates
  the 13 paired total/excess rows so a future aggregation cannot meet them
  silently.
- `temperature_unstated` is for a paper that is **silent**. It does not cover
  resolving a disjunction the paper itself states using a contradiction the
  paper itself supplies — that distinction cost three real benchmark rows on
  HYC-0031 before Agent C overturned it.

## 5. Tiering (§13)

Run `score_reproducibility(row)`, then adjust by hand and **record each
adjustment and its basis**. The scorer's documented blind spots, plus the ones
HYC-0031 found:

- `calibration` is always 0 in code and the extractor may add the point. On
  HYC-0031 it was **not** added: the paper describes no buoyancy or blank
  correction, and its reference-material cross-check is inter-laboratory
  agreement, already scored under criterion 7. Awarding it would score one
  piece of evidence twice.
- The Chahine bound **ignores pressure**, so a 1 bar row clears it trivially.
  Cap it rather than accept the free 2.
- **A `total` row is scored against a bound defined for `excess`** and is
  penalised for the very term that makes it total. Let it inherit the paired
  excess row's score. This blind spot had never been exercised before HYC-0031.

Current scorer-vs-human agreement is pinned at 164 of 259 in
`tests/test_validate.py`, deliberately, and must be updated by hand each append.

## 6. Open items, ranked

1. **`verified_by` on HYC-0007 and HYC-0024.** Both are tracked `verified`, and
   the execution log documents real dual-agent runs — HYC-0024 at 282 cells / 0
   disputes, HYC-0007 at 164 cells / 10 disputes all upheld — but no row carries
   a `verified_by` record, so the dataset does not corroborate the tracking
   file. Decided: **populate `verified_by` from the log's counts**, not downgrade
   the papers. Needs a small migration plan; `tests/test_sync_paper_tracking.py`
   enumerates the gap as `VERIFIED_WITHOUT_ROW_EVIDENCE` meanwhile.
2. **A canonical §12.3 filter.** The four exclusions the manual calls mandatory
   exist **only in its prose** — there is no filter function anywhere in the
   code, which is why `uptake_type` went unfiltered and the corpus-wide mean of
   `uptake_wt_pct` is still 8% inflated (1.997 → 2.156) outside `fig3_chahine`.
   A `src/hycan/analysis.py` exposing one `analysis_subset(df)` used by every
   figure is the durable fix.
3. **Three stale years**: HYC-0052 → 2004, HYC-0054 → 2014, HYC-0061 → 2010.
   OpenAlex reported the online-first year. Needs its own migration plan.
4. **The correction/retraction check across the corpus.** No column records it
   and no §9.1 step consults one, across all 65 papers. 32 of the Phase D 35 are
   unchecked; a raw-JSON Crossref pass is owed, because the WebFetch route
   summarises and was caught dropping a present field twice.
5. **Two schema gaps HYC-0031 exposed.** Oxygen content has no home although it
   is that paper's independent variable, reported three ways that disagree
   (CHN / XPS / TPD) — so its central claim is not queryable from the corpus. And
   isosteric heat has no field at all. Also `PoreDiameterMethod` lacks `NLDFT`
   although `PoreVolumeMethod` has it, and nothing can hold a multimodal PSD.
6. **A behavioural suite for `fig1_corpus_map` and `fig2_condition_space`.**
   `plotting.py` had no tests at all until 2026-10-01; those two have smoke
   coverage only.
7. **`figures/` is stale** and must not be published in that state (§12.4).

## 7. Things that will bite you

- **A cloud session cannot push.** The git proxy returns 403 on writes; it is a
  policy denial and must not be retried. Work reaches `origin` as a **git
  bundle** built from a named branch (`git bundle create <file> main`), never
  from `HEAD`, with a distinctive filename. Verify the bundle by cloning it and
  running the suite, then verify the push **from the remote ref**, never from the
  push's own output.
- **Avin is the sole author on commits.** Match the existing identity exactly.
  No `Co-Authored-By`, no "Generated with" line, no bot identity. AI involvement
  is disclosed in `docs/ai_usage_log.md`, which is where it belongs.
- **Tests pinned to absolute counts expire on every append.** Four files had to
  be amended for HYC-0031. Prefer partitions and deltas; where a total is pinned
  on purpose, its comment says so.
- **A cell-level check cannot see a line ending.** The dataset is **LF**;
  `references/paper_tracking.csv` is **CRLF with no trailing newline**. HYC-0031
  was appended with the wrong one and every check passed. `build_staging.py` now
  reads the terminator from the dataset and `append_paper.py` refuses a mismatch,
  but the general lesson stands for any new script.
- **Mutation-test every script that writes a protected file**, and make the
  harness prove it loaded the scratch copy. §6.7 records a run where all eight
  mutations "survived" because the imports resolved back to the real tree.
- **PDF text layers are hostile.** HYC-0031 replaced the hyphen with **U+0002**
  at hyphenated line breaks, so `CA-4600` as a search key silently missed the
  sentence carrying its own BET area. Figure text layers interleave with body
  prose; no value is readable from a figure without §3.4 digitization.
- **Supplementary Information is not in the Project PDFs.** It controlled two
  dispute resolutions on HYC-0031 and is why that paper is `extracted` rather
  than `verified`.
- **Do not add CI**, workflows, badges, or references to the Actions tab.
- Avin's progress journal (§17.5) is private. Do not ask about it, summarize it,
  or incorporate it.
