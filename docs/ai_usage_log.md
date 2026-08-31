# AI Usage Log — HyCAN-DB

Per Execution Manual Section 17.5, every meaningful AI-assisted session is logged here for the project's audit trail.

## 2026-06-10 — Day 5 literature search session
Tool: Claude.ai Opus 4.8 (web) for procedural walkthrough; Google Scholar for searches; Claude Code for creating docs/literature_search_protocol.md scaffold.
Purpose: Identify first 30 candidate papers for HyCAN-DB corpus.
What I provided: Project context (Days 1-4 state) and request for granular Day 5 walkthrough.
What it produced: Step-by-step task list; scaffold of docs/literature_search_protocol.md.
What I verified: Every DOI was looked up on the publisher's page. No AI-provided DOIs were accepted. All include/exclude/maybe calls were my own judgment.
What I changed: N/A — walkthrough followed as written.

## 2026-06-29 — Day 6 screening and PDF collection
Tool: Claude (chat), Opus 4.8
Purpose: Procedural guidance for Day 6 — how to screen 30 candidates at the
abstract level, citation chaining, the legitimate PDF-access playbook, file-naming,
the PRISMA-count update, and the end-of-day commit.
What I provided: The HyCAN-DB Execution Manual (canonical) and my current project
state (Days 1–5 complete, 30 rows in paper_tracking.csv).
What it produced: A step-by-step Day-6 walkthrough. It did NOT make any screening
decision, did NOT decide database contents, and did NOT supply any DOI.
What I did myself: Read every abstract and made each include/exclude/maybe/review
call; obtained every DOI from publisher pages; obtained every PDF via
[OA / Google Scholar / UNT library / ILL]; assigned every filename.
What I verified: That each decision matches the four-point relevance test (§7.3) and
the exclusion vocabulary (§7.5); that each collected PDF is the complete article;
that no PDF was committed to GitHub.
What I changed: [note any deviation from the walkthrough, or "none"].

## 2026-06-29 — Day 7: validation pipeline
Tool: Claude Code (Claude Opus 4.8)
Purpose: Generate the data-validation pipeline (validate.py, clean.py, validate_data.py), its tests, and a fake 5-row toy CSV, to the spec in Execution Manual §11.3-§11.4.
What I provided: The §11.3 error/warning rules and the §11.4 build prompt, with explicit file permissions and the toy-data structure (3 valid / 1 warning / 1 error).
What it produced: src/hycan/validate.py (validate_row, validate_dataset, print_report), src/hycan/clean.py (clean_dataset), scripts/validate_data.py (CLI, exit 0/1), tests/test_validate.py (>=10 tests, all passing), and data/raw/test_measurements.csv (toy data).
What I verified: Read validate.py and clean.py and followed the logic for each §11.3 condition; ran the full test suite (61 passed); ran the CLI on the toy CSV and confirmed the report matched the §11.4 example (total 5, valid 4, errors 1, warnings 1) with exit code 1.
What I changed: Nothing; the output matched the spec on the first build, so no fix-up prompts were needed.

## 2026-06-29 — Day 8: first paper extraction (Panella 2005, HYC-0001)
Tool: Claude.ai (chat) to locate values + quotes; Claude Code to write the CSV from my verified/digitized values.
Purpose: Extract hydrogen sorption data from Panella, Hirscher, Roth (2005), Carbon 43:2209-2214 (DOI 10.1016/j.carbon.2005.03.037) into data/raw/measurements_v0.1.csv.
What I provided: The PDF, the schema, and the §9.4 extraction-assistant structure.
What the AI produced: A located list of every sample + structural value from Table 1 with page citations; the text-stated 77 K uptake (4.5 wt%) with quotes; flags for figure-only uptakes; and a Claude Code prompt that wrote the 4-row CSV from values I dictated.
What I verified against the PDF: DOI; Table 1 BET/pore values for both samples (2564/0.75 and 854/0.36); the 4.5 wt% quote in the abstract, Section 3, and conclusion; the Sieverts measurement method; and that "excess"/"absolute" appear nowhere (Find = 0 hits).
What I digitized myself (WebPlotDigitizer): Act. carbon I 298 K (Fig 5) = 0.53 wt%; SWCNT II 77 K (Fig 2b, cross-checked Fig 3) = 2.52 wt%; SWCNT II 298 K (Fig 2b lower curve, cross-checked Fig 5) = 0.35 wt%.
Judgments I made/ratified: uptake_type = unspecified; extraction_confidence 4 (text) / 3 (digitized); reproducibility_tier B (rubric ~8/10); sample_id keyed per measurement (S1-S4), pending a Day-9 schema-feedback issue.
What I changed: Nothing; the CSV validated 4/4 on the first build

## 2026-06-29 — HYC-0004 extraction (Nijkamp 2001)
Tools: Claude.ai (value location, judgment-call recommendations, build prompt); Claude Code (CSV append).
Purpose: Append HYC-0004 (Nijkamp et al. 2001) hydrogen-sorption rows to data/raw/measurements_v0.1.csv.
What I provided: the Nijkamp 2001 PDF and the HyCAN-DB Execution Manual.
What Claude.ai produced: located 21 carbonaceous Table-1 samples (SBET, MPV, PV, H2 total) with citations; pre-filled mechanical fields; recommended material_class, synthesis_method, tier, and uptake_type; the ml(STP)/g->wt% formula; the Claude Code build prompt; schema-feedback issue text.
What I verified: confirmed all 21 SBET/MPV/PV/H2-total values against Table 1 (p.620); Find-checked "excess"/"absolute" = [FILL: __ hits each]; verified the conversion factor 22.414 ml(STP)/mmol against [FILL: NIST / textbook] and the paper's DOE anchor (720 ml(STP)/g = 6.5 wt%).
What I digitized: none — all values table-direct.
What I decided/ratified: H2 total as the uptake (meso/micro excluded); uptake_type=unspecified; material_class (graphite->other, ACF->activated_carbon, CNF->carbon_nanofiber); CNF synthesis=[FILL: cvd / other]; all rows Tier B; sample_ids HYC-0004-S1..S21. Opened schema-feedback issues #[FILL] and #[FILL].
What Claude Code produced: appended 21 rows (4 Panella rows preserved); validation = 25 rows, 0 errors, exit 0.

## 2026-07-05 — Schema v1.0: measurement_id key and as-reported ml(STP)/g support
Tool: Claude Code (<model shown in your session>) — two fresh sessions (code; then dataset migration). Design pre-decided in a Claude.ai chat; I ratified it.
Purpose: Resolve the two Day-8/9 schema-feedback issues — add measurement_id as the unique-per-row key (letting sample_id repeat per physical sample), and add an as-reported uptake_ml_stp_g field plus ml(STP)/g -> mmol/g and -> wt% converters — then migrate the 25-row dataset and bump the CHANGELOG.
What I provided: The ratified design (measurement_id format {paper_id}-M{n}; collapse the four Panella sample_ids to two physical samples S1,S1,S2,S2; uptake_ml_stp_g float 0-2225; converter constant 22.414 L/mol at STP = the Day-9 convention; dataset-level duplicate check on measurement_id; CHANGELOG [0.0.2]) and explicit file allow/deny lists forbidding any CI and forbidding edits to measurements_v0.1.csv in the code session.
What it produced: edits to src/hycan/schema.py, src/hycan/normalize.py, src/hycan/validate.py, docs/data_dictionary.md, tests/test_schema.py, tests/test_normalize.py, tests/test_validate.py, CHANGELOG.md; and a column-add + Panella re-key + Nijkamp ml(STP)/g backfill migration of data/raw/measurements_v0.1.csv.
What I verified: read every diff; ran the full pytest suite (76 passing); ran scripts/validate_data.py on the 25-row file (25 valid, 0 errors, exit 0); confirmed the new converters reproduce the stored uptake_mmol_g/uptake_wt_pct for the Nijkamp rows via the migration's per-row consistency check; confirmed the four Panella rows collapsed to two physical samples at BET 2564 and 854; confirmed the pressure>200 warning reclassification and all other fields were untouched.>
What I changed: None

## 2026-07-06 to 2027-07-09  — extraction, corpus overview, reproducibility tiering
(3 sessions logged separately below; dates are my working days, not calendar days)

### Day 11 [2026-07-06] — Papers HYC-0002, HYC-0005, HYC-0020 extracted
Tool: [your actual tool + version]
Purpose: Locate (not interpret) samples, surface-area values, and H2 uptake in three PDFs,
using the Part 6 §9.4 extraction-assistance prompt (verbatim quotes required per value).
What it produced: Per-sample candidate rows with quoted source sentences/table captions.
What I verified: Opened each PDF and confirmed every quoted sentence exists and every number
matches the source before it entered measurements_v0.1.csv. Discarded any value the tool
could not tie to a verbatim quote.
Scientific decisions I made (not the AI):
  - Texier-Mandoki 2004: the paper's N2 "total surface area" is not called BET, so I mapped it
    into bet_surface_area_m2_g with an explicit note flagging the ambiguity rather than treating
    it as a clean BET value.
  - Liu 1999: paper reports no surface area of any kind → entered BET-null deliberately, with a
    note, rather than inferring one.
  - Marked uptake_type unspecified on all rows because no source states excess vs absolute.
Result: 60 rows, 60 valid, exit 0.

### Day 12 [2026-07-06] — Corpus overview notebook + plotting module (commit ed9db4a)
Tool: Claude Code
Purpose: Draft 01_corpus_overview.ipynb (9 narrated sections) and src/hycan/plotting.py
(set_house_style, fig1_corpus_map, fig2_condition_space, fig3_chahine).
What it produced: the notebook, plotting.py, and three 300-dpi PNGs in figures/.
What I verified: Ran the notebook end-to-end on data/raw/measurements_v0.1.csv; inspected
Figure 3 and confirmed the Chahine line passes through the 77 K point cloud — my check that no
unit bug had crept into the mmol/wt% conversions (Part 7). Confirmed all three PNGs saved.
What I changed: Nothing in the AI output; I own the interpretation in the section commentary.

### Day 13 [2026-07-09] — Reproducibility tiering live (commit 1dfb2ae)
Tool: Claude Code (3 separate sessions)
Purpose: Stand up the Part 10 tiering rubric, an approximate scorer, and apply considered tiers.
What it produced:
  - docs/reproducibility_tiering.md — 10-point rubric, physics-override clause, three worked
    examples (Tier A / C / D).
  - score_reproducibility + suggest_tier in src/hycan/validate.py (pure appends; existing
    functions untouched) + 6 tests.
  - ruff.toml (ignore E402 in notebooks — false positive on the src-path insert pattern).
  - Text-only edit of measurements_v0.1.csv retiering HYC-0002 (see decision below).
What I verified: Full suite 82 passed; ruff clean; ran a throwaway probe printing
score_reproducibility's per-criterion breakdown for all five papers and read the scores against
the rubric myself; confirmed final tier counts 57 B / 3 D via a quote-aware CSV read.
Scientific decisions I made (the scorer only suggests — §13.5, §17.7):
  - HYC-0002 Liu 1999 → Tier D. suggest_tier scored it 4 → C, but 2.4–4.2 wt% at 298 K sits far
    above the ~1 wt% room-temperature physisorption bound on pure carbon with no reported surface
    area — the discredited-class pattern (§13.2). I applied the categorical physics override the
    scorer cannot apply, and recorded the rationale in the row note.
  - HYC-0020 Serafin 2024 → Tier B (kept). suggest_tier scored it 5 → C on the same room-temp
    Chahine trip, but this is a 2024 paper with reported BET, a named method, and 45 bar elevated-
    pressure measurement on a characterized activated carbon — the override targets discredited
    over-claims on pure carbon, which this is not. I judged the scorer's C a false trip and kept B.
Honest limitations noted: suggest_tier always scores calibration 0 (no schema field), cannot
judge method-description quality, proxies purity weakly by purification_method, and cannot apply
the physics override — all documented in reproducibility_tiering.md.
Follow-up I opened: GitHub issue on the schema's inability to record surface-area *method*
(BET vs Langmuir vs geometric vs none) — the gap Liu and Texier-Mandoki both exposed.

## 2026-08-30 — HYC-0023 (Gogotsi et al. 2009) extraction

**Tool:** Claude (chat) for locating; Claude Code for writing a staging CSV.

**What I asked.** Ran the §9.4 locate-only prompt against the PDF: enumerate
samples, BET values, and uptake measurements with figure/table locations, quote
the source sentence for each, convert nothing, flag uncertainty. Later asked
Claude Code to generate a 23-row staging file from values I had already verified,
scoped to one new file and forbidden from touching the dataset or source.

**What I verified.** Checked all five quoted sentences in the PDF — all present
verbatim. Spot-checked Table 1 rows 1, 13, 16 and Table 2 row 3 before trusting
the transcription, then re-checked rows 12, 16 and 23 against the PDF after the
staging file was generated. Two whitespace defects in the generated text
(`600 Cfor`, `Porevolume`) were caught on review and fixed before merge.

**Decisions I made.**
- `uptake_type = excess` for all 23 rows. Table headers say only "Hydrogen
  uptake", so this is not literal per §9.5. I accepted it because Fig. 3's
  caption reads "Excess capacity at 77 K, 60 bar" — the identical condition to
  the table column — and §2.3 states the isotherms were determined as excess
  adsorption. Recorded the basis in `notes` on every row.
- Tier A, 10/10 on the §13.4 rubric. I questioned whether "method clearly
  described" should be 1/2 given the home-built Sieverts apparatus, and decided
  no: the rubric asks whether another lab could perform the measurement from the
  description, and the paper gives dosing cell, three overlapping 0–60 bar
  gauges, MBWR equation of state, and a reference for the full apparatus. The
  home-built rig limits *numerical* reproducibility (§13.3, second layer), which
  is a different criterion. Noted rather than deducted.
- Pore volume → `total_pore_volume_cm3_g`, micropore left null. Tables label the
  column only "Pore volume"; Fig. 3b plots the same values against an axis
  reading "Total pore volume (cm³/g)".
- `synthesis_method = other`. Carbide chlorination is not in the controlled
  vocabulary. Detail preserved in `material_description`. Flagging as a second
  schema-feedback candidate alongside the open surface-area-method issue.
- `extraction_confidence = 5` throughout. Every extracted field is directly
  tabulated. The printed per-SSA column does not always reproduce from
  uptake ÷ SSA (row 3: ~2.49 computed vs 2.72 printed), but that column is not
  extracted, so it does not bear on the fields I recorded.

**What I rejected.** Two text-only values not entered as measurements: "saturates
around 5.5 wt%" at 30 K (hedged, no pressure stated) and "less than 0.5 wt%" at
room temperature (a bound, not a measurement). Figs. 1, 3, 4, 5 left
undigitized — no figure-only values were needed, since Tables 1 and 2 carry all
23 uptake points.

**Outcome.** 23 rows appended to `data/raw/measurements_v0.1.csv` (60 → 83).
Validation: 83 rows, 83 valid, 0 errors; warning counts unchanged from the
pre-append baseline. Committed as `b2aa7cf`.

## 2026-08-30 — Paper extraction: HYC-0016 (Klechikov et al. 2015)

Tool: Claude Opus 5 (claude.ai web chat) for locate-only extraction assistance;
Claude Code (CLI) for staging-file authoring. Session ran past midnight; commits
carry 2026-08-31 timestamps.

Purpose: §9.4 locate-only assistance for extracting hydrogen sorption data from
Klechikov et al., "Hydrogen storage in bulk graphene-related materials,"
Microporous and Mesoporous Materials 210 (2015) 46–51,
DOI 10.1016/j.micromeso.2015.02.017. Selected to add the first graphene-class
rows to a corpus dominated by 77 K activated carbon and CDC.

What I provided: the paper PDF; current repo state (83 rows, 6 papers, validation
baseline 0 errors / 60 "Unspecified uptake_type" / 1 "mmol/g and wt% inconsistent");
the 38-column header of measurements_v0.1.csv; the DOI, which I resolved myself on
the ScienceDirect publisher page rather than accepting any AI-supplied identifier.

What it produced:
- A locate-only inventory: sample groups by precursor, all BET values with
  section locations, both prose uptake values, and figure locations for all
  figure-only data. It correctly refused to estimate any value from Figs. 2–5.
- 16 verbatim search keys for quote verification.
- The 14-row value set and a fully-specified Claude Code prompt writing only
  data/raw/staging_HYC-0016.csv, with all other repo files named as forbidden
  and git/pytest/ruff/CI explicitly prohibited.
- Two flagged uncertainties I confirmed as real: Figs. 2 and 5 number the same
  sample set differently and cannot be cross-mapped; and the Fig. 5 caption cites
  50 bar for the 77 K data while the digitized endpoints fall at 38–39 bar.

What I verified:
- Cmd+F'd all 16 quoted search keys in the PDF. All 16 located. Under §9.4 a
  single miss would have voided the entire output.
- Checked all 12 BET surface-area curve labels against Figs. 3 and 4 directly
  (310/560/1250/1740/1830; 370/650/1259/1450/1730/1830/2300 m²/g). These labels
  became the bet_surface_area_m2_g values, so an error here would propagate to
  every digitized row.
- Resolved the DOI on the ScienceDirect page and confirmed title, journal,
  volume, year, and pagination before any row was written.
- Performed all digitization myself in WebPlotDigitizer. Project files archived
  at data/digitizations/HYC-0016_fig3.json and HYC-0016_fig4.json and referenced
  in the row notes.
- Verified the staging file from the terminal with `wc -l` and `head -3` rather
  than accepting Claude Code's own summary of what it had written.
- Validated the staging file standalone: 14 rows, 14 valid, 0 errors, 14
  "Unspecified uptake_type" warnings and no other warning type.
- Re-verified 3 rows against the PDF after staging (M5, M12, M14) covering both
  figures and the prose source.
- Validated the merged file: 97 rows, 97 valid, 0 errors, warnings 74 + 1,
  matching the pre-append baseline exactly with no new warning types.

What I caught and corrected:
- The paper recommendation rested on a false premise. It was proposed as a
  multi-sample table paper; the paper contains no data tables at all and nearly
  every value is figure-only. I kept the paper but rescoped the work to endpoint
  digitization anchored on the printed curve labels.
- I mistyped the Fig. 3 y-axis calibration as 10.6 instead of 0.6. The resulting
  uptakes (~11 wt%) were physically impossible for ambient-temperature carbon and
  contradicted the paper's own statement that uptake does not exceed 1 Wt% at
  120 Bar. Recalibrated; the stored pixel positions made the fix a single edit.
- measurement_method was wrong on all 14 rows and extraction_method wrong on 2:
  the AI supplied `gravimetric`, `volumetric`, and `text_reported`, none of which
  are in the schema's controlled vocabulary. Validation caught all 16; corrected
  to `gravimetric_microbalance`, `volumetric_sieverts`, and `text_direct` after
  reading the Literal definitions in schema.py directly.
- A first diagnostic script reported spurious errors on every empty optional
  field, an artifact of `keep_default_na=False` rather than a defect in the data.
  Confirmed against schema.py before acting on it.
- Values belonging to other groups that appear in the Introduction (3.1 wt% /
  925 m²/g; Srinivas 0.7 wt% / 640 m²/g; Wang 0.9 wt% / 2139 m²/g) and the
  extrapolated ~0.8–0.9 wt% at ~3000 m²/g saturation estimate were identified as
  not-this-paper's-data and excluded.

Scientific decisions — mine:
Each of the following was recommended by the AI with a stated basis and ratified
by me after independent verification against the PDF.

- uptake_type = unspecified on all 14 rows. The word "excess" does not appear in
  the paper; "absolute" appears once, describing MOFs from other groups rather
  than these measurements.
  Why I accepted this rather than inferring a type: [YOUR SENTENCE]

- extraction_confidence = 3 on all 14 rows. Digitized rows carry 3 because
  uptake and pressure both come off my own axis calibration. The two prose rows
  were dropped from 4 to 3 because their sentence omits the temperature.
  Why an inferred temperature is worth the same confidence penalty as a
  digitized axis: [YOUR SENTENCE]

- temperature_k = 293 on M13/M14, recorded with the inference stated in the notes
  field. The paper also reports gravimetric runs at 274 K and 288 K, so 293 K is
  read from surrounding context rather than from the sentence itself.
  Why recording 293 with a note beats leaving the field blank: [YOUR SENTENCE]

- reproducibility_tier = B (8/10 on the §13.4 rubric). Full marks on BET,
  method description, T and P, purity (XPS C/O ratios), calibration (2-minute
  zero-point correction, FLUIDCAL densities), and Chahine consistency; zero on
  uptake type.
  Why the single lost point is the right one to lose here: [YOUR SENTENCE]

- M11 retained as material_class = activated_carbon. This is the paper's internal
  reference sample, not a graphene material, measured on the same instrument
  under the same conditions.
  Why I kept a reference sample rather than dropping it: [YOUR SENTENCE]

Schema feedback generated: synthesis_method has no controlled value for thermal
exfoliation of graphite oxide or for KOH activation; both were recorded as
`other`. This is the third such case after carbide chlorination (HYC-0023) and
the