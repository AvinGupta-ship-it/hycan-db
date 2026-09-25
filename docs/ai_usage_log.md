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
call; obtained every DOI from publisher pages; obtained every PDF via Google Scholar UNT library; assigned every filename.
What I verified: That each decision matches the four-point relevance test (§7.3) and
the exclusion vocabulary (§7.5); that each collected PDF is the complete article;
that no PDF was committed to GitHub.

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
What I verified: confirmed all 21 SBET/MPV/PV/H2-total values against Table 1 (p.620); Find-checked "excess"/"absolute"; verified the conversion factor 22.414 ml(STP)/mmol against NIST and the paper's DOE anchor (720 ml(STP)/g = 6.5 wt%).
What I digitized: none — all values table-direct.
What I decided/ratified: H2 total as the uptake (meso/micro excluded); uptake_type=unspecified; material_class (graphite->other, ACF->activated_carbon, CNF->carbon_nanofiber); CNF synthesis=cvd; all rows Tier B; sample_ids HYC-0004-S1..S21. Opened schema-feedback issues
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

- extraction_confidence = 3 on all 14 rows. Digitized rows carry 3 because
  uptake and pressure both come off my own axis calibration. The two prose rows
  were dropped from 4 to 3 because their sentence omits the temperature.

- temperature_k = 293 on M13/M14, recorded with the inference stated in the notes
  field. The paper also reports gravimetric runs at 274 K and 288 K, so 293 K is
  read from surrounding context rather than from the sentence itself.
  Why recording 293 with a note beats leaving the field blank:

- reproducibility_tier = B (8/10 on the §13.4 rubric). Full marks on BET,
  method description, T and P, purity (XPS C/O ratios), calibration (2-minute
  zero-point correction, FLUIDCAL densities), and Chahine consistency; zero on
  uptake type.
  Why the single lost point is the right one to lose here:

- M11 retained as material_class = activated_carbon. This is the paper's internal
  reference sample, not a graphene material, measured on the same instrument
  under the same conditions.
  Why I kept a reference sample rather than dropping it:

Schema feedback generated: synthesis_method has no controlled value for thermal
exfoliation of graphite oxide or for KOH activation; both were recorded as
`other`.

## 2026-08-31 — Paper extraction: HYC-0018 (Singh & De 2020)

Tool: Claude Opus 5 (claude.ai web chat) for locate-only extraction assistance;
Claude Code (CLI) for staging-file authoring.

Purpose: §9.4 locate-only assistance for extracting hydrogen sorption data from
Singh & De, "Thermally exfoliated graphene oxide for hydrogen storage,"
Materials Chemistry and Physics 239 (2020) 122102,
DOI 10.1016/j.matchemphys.2019.122102. Selected as the most recent paper in the
unextracted set, on the expectation that a 2020 paper would state excess or
absolute outright — the criterion every row in the corpus currently fails.

What I provided: the paper PDF; the 38-column header; the running validation
baseline (97 rows, 0 errors, 74 "Unspecified uptake_type" + 1 "mmol/g and wt%
inconsistent"); the DOI, which I resolved on the ScienceDirect publisher page.

What it produced:
- A locate-only inventory: five samples (GO, EGR 200/300/400/500), the complete
  Table 2 characterization set, all four extractable uptake values with their
  source locations, and explicit exclusion lists.
- 17 verbatim search keys, chosen to avoid the mangled degree-sign and
  superscript characters in this PDF's text layer.
- A fully-specified Claude Code prompt writing only
  data/raw/staging_HYC-0018.csv, with all other repo files named as forbidden
  and git/pytest/ruff/CI explicitly prohibited.
- Correct identification that the paper is a Chahine outlier by roughly six
  times, and that the paper states and explains this itself.

What I verified:
- Cmd+F'd all 17 search keys. All 17 located.
- Checked the full S_BET and V_T columns of Table 2 (41/46/248/218/135 and
  0.14/0.27/1.63/1.40/0.85) and the present-study row of Table 3 against the PDF.
- Resolved the DOI on the publisher page and confirmed journal, volume, year,
  and article number. Recorded year as 2020 to match the volume, noting the
  paper was accepted in 2019.
- Verified the staging file from the terminal rather than accepting Claude Code's
  summary of what it had written.
- Validated standalone after correction: 4 rows, 4 valid, 0 errors.
- Re-verified all 4 rows against Table 3 and the Fig. 10 labels before appending.
- Validated merged: 101 rows, 101 valid, 0 errors, warnings 78 + 1, matching the
  pre-append baseline with no new warning types.

What I caught and corrected:
- The selection premise was wrong. The paper does not designate its values as
  excess or absolute. It uses the word "excess" exactly once, in the ordinary-
  English sense of exceeding the Chahine rule — the precise §9.5 trap, and a
  cleaner instance of it than the previous paper.
- Table 2 gives EGR(300) total pore volume as 1.63 cm³/g while the abstract,
  Highlights, and §3.2 body text all give 1.64. I confirmed 1.63 in Table 2
  directly and recorded that value as the primary data table, with the
  discrepancy noted in the row.
- The schema requires temperature_k and pressure_bar on every row, which
  surfaced only at validation: the two characterization-only rows for GO and
  EGR(400) failed with 4 missing-field errors. This is a structural constraint,
  not a typo — measurements_v0.1.csv cannot hold a row that is not a
  measurement. Second structural schema gap found this week, after the
  surface-area-method gap blocking HYC-0025.
- Controlled vocabularies for material_class, synthesis_method,
  activation_method, and uptake_type were read from schema.py before the staging
  prompt was written, rather than after validation failed. This followed
  directly from the previous paper, where AI-supplied values for
  measurement_method and extraction_method were wrong on every row.
- That check also showed the schema distinguishes graphene_oxide from
  reduced_graphene_oxide. Applied here. It also means HYC-0016's rows, entered
  as plain `graphene`, are coarser than the schema allows — a candidate cleanup,
  not an error.
- Excluded: all six literature comparison rows in Table 3; the Introduction's
  survey values (Wang 1.75 wt%, Rao 3.0 wt%, and the 0.4–1.4 and 0.1–0.7 wt%
  ranges); and the isosteric heat values, which have no schema field.

Scientific decisions — mine:
Each was recommended by the AI with a stated basis and ratified by me after
independent verification against the PDF.

- uptake_type = unspecified on all 4 rows, despite the word "excess" appearing
  in the paper.

- reproducibility_tier = B, 7/10. Full marks on BET, method description, T and P,
  purity (EDX and XPS elemental analysis), and calibration (explicit blank run to
  30 bar, stated sample mass and pretreatment). Zero on uptake type. Zero on the
  Chahine criterion: 3.12 wt% at 248 m²/g is roughly six times the 1 wt% per
  500 m²/g rule.
  Why a paper this carefully reported still loses both Chahine points, and why
  that lands at B rather than C:

- Dropped the GO and EGR(400) characterization rows rather than populating
  temperature_k and pressure_bar with the nitrogen adsorption conditions.
  Why filling those fields would have been the worse error:

- Excluded EGR(400)'s 77 K uptake. It is plotted in Fig. 9 but its numeric value
  is printed nowhere in the paper, while EGR 200/300/500 all have exact printed
  values.

- extraction_confidence: 5 on the two Table 3 rows, 4 on the two rows whose
  values come from printed labels in the Fig. 10 schematic. Nothing in this
  paper was digitized, which is why these sit above HYC-0016's uniform 3.

Result: 4 rows added, 97 → 101. Eight papers extracted. Commit a1528a6.

## 2026-09-24 — Paper extraction: HYC-0021 (Sethia & Sayari 2016)

Tool: Claude Opus 5 (claude.ai web chat) for locate-only extraction assistance;
Claude Code (CLI) for staging-file authoring.

Purpose: §9.4 locate-only assistance for extracting hydrogen sorption data from
Sethia & Sayari, "Activated carbon with optimum pore size distribution for
hydrogen storage," Carbon 99 (2016) 289–294,
DOI 10.1016/j.carbon.2015.12.032. Selected because the corpus holds many
activated carbons but none in which pore structure is the deliberate
independent variable — the control condition the Singh outlier (HYC-0018)
invites.

What I provided: the paper PDF; the 38-column header; the running validation
baseline (101 rows, 0 errors, 78 "Unspecified uptake_type" + 1 "mmol/g and wt%
inconsistent"); screenshots of Tables 2 and 3 for numeric verification; the DOI,
resolved on the ScienceDirect publisher page.

What it produced:
- A locate-only inventory of all six samples (CP-400, CP-600, and NAC-1.5-550
  through -700) with the complete Table 2 textural and uptake data, the Table 3
  elemental composition, and the measurement protocol.
- 17 verbatim search keys, three of which were chosen specifically to pin down a
  suspected internal discrepancy.
- A fully-specified Claude Code prompt writing only
  data/raw/staging_HYC-0021.csv, with all other repo files named as forbidden
  and git/pytest/ruff/CI explicitly prohibited.
- Identification of two internal inconsistencies and one schema mapping problem
  before any row was written.

What I verified:
- Cmd+F'd all 17 search keys. All 17 located.
- Verified the complete Table 2 and Table 3 contents against the PDF by
  screenshot: six rows across uptake, BET, total pore volume, DFT pore size,
  ultra-micropore and micropore volumes, and the full nitrogen column.
- Resolved the DOI on the publisher page and confirmed journal, volume, year and
  pagination. Recorded year as 2016 to match the volume; the paper was accepted
  in December 2015.
- Verified the staging file from the terminal rather than from Claude Code's
  summary.
- Validated standalone: 6 rows, 6 valid, 0 errors — clean on the first attempt,
  the first paper this week to pass without correction.
- Re-verified all 6 rows against the Table 2 screenshot before appending.
- Validated merged: 107 rows, 107 valid, 0 errors, warnings 84 + 1, matching the
  pre-append baseline with no new warning types.

What I caught and corrected:
- The abstract gives NAC-1.5-600's uptake as 2.94 wt%; Table 1, Table 2, the body
  text and the Conclusion all give 2.96. I confirmed 2.96 in Table 2 directly and
  recorded that, noting the discrepancy in the row. This is the same failure mode
  as HYC-0018's 1.63/1.64 pore volume, and I resolved it the same way: the
  primary data table wins.
- The same sample's BET area appears as 1317 in Table 2 and 1312 in one body
  sentence. Table 2 value recorded.
- dopant_concentration_at_pct expects atomic percent; the paper reports nitrogen
  in weight percent. Left blank on all six rows rather than converting, per §10,
  with the weight-percent values recorded in notes.
- The paper mis-cites its own tables twice, pointing to Tables 1 and 3 for
  ultra-micropore values that appear in Table 2. No effect on the extracted
  values.
- Controlled vocabularies were read from schema.py before the staging prompt was
  written rather than after validation failed. This is the second paper using
  that order and the first to validate cleanly on the first attempt.

Scientific decisions — mine:

- material_class: `other` for the two non-activated carbonized precursors,
  `doped_carbon` for the four NAC samples, rather than `activated_carbon`.

- reproducibility_tier = A, 9/10. Full marks on BET, method description, T and P,
  purity (CHN elemental analysis, XPS, and stated gas purities to five nines),
  calibration (explicit BET relative-pressure ranges, in-situ activation
  conditions, and four reversibility cycles at under 0.5% loss per cycle), and
  Chahine consistency. Loses only the uptake-type point.

- Ultra-micropore volume (pores below 0.7 nm: 0.12, 0.27, 0.21 and 0.0 cm³/g)
  recorded in the notes field rather than mapped into
  micropore_volume_cm3_g, which holds the paper's separate below-2 nm column.

- extraction_confidence = 5 on all six rows, including NAC-1.5-600 despite its
  two internal discrepancies, because both resolve unambiguously in favor of the
  primary data table.

Schema feedback generated: no field exists for pore-size-resolved pore volume.
This is the third structural gap found this week, after the surface-area-method
gap (blocking HYC-0025) and the requirement that every row carry temperature_k
and pressure_bar (which forced dropping two characterization-only rows from
HYC-0018). This one is the most consequential: the corpus now holds two papers
whose uptake departs from the Chahine prediction, and without a pore-size-
resolved field it cannot test the explanation either paper offers.

Result: 6 rows added, 101 → 107. Nine papers extracted. Commit d2c6b6b.

## 2026-09-24 — Paper extraction: HYC-0027 (Parambhath et al. 2012)

Tool: Claude Opus 5 (claude.ai web chat) for locate-only extraction assistance;
Claude Code (CLI) for staging-file authoring.

Purpose: §9.4 locate-only assistance for extracting hydrogen sorption data from
Parambhath, Nagar & Ramaprabhu, "Effect of Nitrogen Doping on Hydrogen Storage
Capacity of Palladium Decorated Graphene," Langmuir 2012, 28, 7826–7833,
DOI 10.1021/la301232r. The corpus held no metal-decorated carbons and no
spillover-mechanism papers, so every existing row assumed physisorption.

Note on selection: the AI's first recommendation was HYC-0013 (Hudson 2014,
Fe-decorated rGO), with HYC-0027 named as the fallback in the same class. I
uploaded HYC-0027. I chose to continue with it rather than switch, since the
locate-only pass was already complete and both papers occupy the same gap.
Hudson remains queued.

What I provided: the paper PDF; the 38-column header; the running baseline
(107 rows, 0 errors, 84 "Unspecified uptake_type" + 1 "mmol/g and wt%
inconsistent"); the DOI, resolved on the ACS publisher page.

What it produced:
- A locate-only inventory of four samples (HEG, N-HEG, Pd-HEG, Pd-N-HEG), the
  five extractable uptake values with conditions, the full measurement protocol,
  and explicit exclusion lists.
- 17 verbatim search keys. All 17 located.
- A fully-specified Claude Code prompt writing only
  data/raw/staging_HYC-0027.csv, with all other repo files named as forbidden
  and git/pytest/ruff/CI explicitly prohibited.
- Correct identification that this paper reports no BET surface area anywhere,
  and that its mechanism is chemisorption-mediated rather than physisorption.

What I verified:
- Cmd+F'd all 17 search keys. All 17 located.
- Read the two source sentences on journal page 7829 directly and confirmed all
  five uptake values (0.53, 0.63, 0.88, 1.97, 4.4) against the text.
- Confirmed the MPa to bar conversions independently: 2 MPa = 20 bar,
  4 MPa = 40 bar.
- Resolved the DOI on the ACS page and confirmed journal, volume, year and
  pagination.
- Verified the staging file from the terminal rather than from Claude Code's
  summary.
- Validated standalone: 5 rows, 5 valid, 0 errors — clean on the first attempt,
  the second consecutive paper to do so.
- Re-verified all 5 rows before appending.
- Validated merged: 112 rows, 112 valid, 0 errors, warnings 89 + 1, matching the
  pre-append baseline with no new warning types. Confirmed specifically that the
  validator does not warn on a missing BET value, which mattered because these
  are the first rows in the corpus with that field empty.

What I caught and excluded:
- Equation 1 substitutes a value of 0.72 for palladium nanoparticle uptake. That
  number appears nowhere else in the paper and no measurement is reported for
  bare Pd NPs. Not extracted.
- Values belonging to other work: 1.76 wt% and 3 wt% (the authors' own earlier
  paper, ref. 19), 3.1 wt% (ref. 55), and the theoretical 13.79 wt% and ~5 wt%
  (refs. 58, 59). Table S1 is in Supporting Information and not in the obtained
  PDF.
- Three of the five uptake values are written as bare percentages without a unit.
  I recorded them as wt% and lowered their extraction_confidence to 3 to mark the
  inference.
- Pd loading is reported three ways: 21 wt% by XPS, 20 wt% by EDX, 20 wt%
  intended. No schema field; recorded in notes.

Scientific decisions:
Each was recommended by the AI with a stated basis, and I ratified it after
checking the relevant passage in the PDF myself.

- uptake_wt_pct for all five values including the three bare percentages. Basis
  given: the abstract describes the enhancements as being in hydrogen uptake
  capacity, Equation 1 treats 0.88 and 1.97 as the same quantity in a single
  calculation, and no other uptake unit appears in the paper, so a unit change
  mid-sentence would break the paper's own arithmetic. Ratified after reading the
  passage.

- material_class: `graphene` for HEG, `doped_carbon` for N-HEG, and `composite`
  for both Pd-bearing samples. dopant_element = N rather than Pd on Pd-N-HEG.
  Basis given: Pd nanoparticles on a carbon support are a two-phase material
  rather than a doped lattice, which is the distinction the schema's separate
  `composite` and `doped_carbon` values exist to record; and nitrogen is
  substitutionally incorporated in the graphene network per the XPS assignments
  (pyridinic 398.1 eV, pyrrolic 399.04 eV, sp³ C–N 400.21 eV), while Pd sits on
  the surface as discrete particles. Ratified after checking the XPS section.

- dopant_concentration_at_pct = 7 on the three nitrogen-bearing rows. The paper
  reports approximately 7 at.% nitrogen by XPS — atomic percent, matching the
  schema field's units directly. This is the first paper in the corpus where this
  field was usable; HYC-0021 reported nitrogen in weight percent and the field was
  left blank there rather than converted.

- reproducibility_tier = C, 5/10. Full marks on method description, T and P,
  purity, and calibration. Zero on uptake type, zero on BET (none reported), and
  zero on Chahine (unassessable without BET). Basis given: the score is honest
  under §13.4 as written, but four of the five lost points do not reflect
  reporting quality — §13.4 is built around physisorption, and this paper's
  mechanism is dissociative chemisorption on Pd followed by migration of atomic
  hydrogen onto the support, so surface area is not the governing variable and
  the Chahine rule does not apply. The measurement protocol itself is strong:
  calibrated Sieverts apparatus, van der Waals correction at high pressure,
  empty-cell and leak tests, stated activation and degas cycles, room temperature
  held to ±1 °C. Ratified as written rather than adjusted, on the stated ground
  that the fix belongs in the tiering documentation rather than in the score.

  First Tier C in the corpus. This is the second paper this week whose tier is
  depressed by a rubric assumption rather than by its own reporting, after
  HYC-0018, and a second metal-decorated paper (HYC-0013) is queued. Flagged for
  docs/reproducibility_tiering.md.

- extraction_confidence: 4 on the two Pd-N-HEG rows, 3 on the other three. Basis
  given: an inferred unit is a provenance gap of the same kind as the inferred
  temperature in HYC-0016, which also cost a point. Nothing in this paper is
  digitized, so nothing falls below 3.

Corpus note: the database now holds an explicit disagreement. HYC-0016
(Klechikov 2015) argues that graphene-related materials never exceed standard
carbon trends and that high reported values were overestimates. HYC-0027 reports
4.4 wt% at 300 K and 4 MPa. Both are in the dataset with their tiers attached
(B and C respectively), which is what the tiering system exists to make visible.

Result: 5 rows added, 107 → 112. Ten papers extracted. Commit a76097f.

## 2026-09-24 — HYC-0013 (Hudson et al. 2014, Int. J. Hydrogen Energy 39, 8311–8320)

**Tool:** Claude (chat) for §9.4 locate-only pass and staging-prompt authoring; Claude Code for staging-file generation.

**What the AI did.** Ran the §9.4 locate-only pass against the PDF: enumerated the four samples (GO, TR-GO, CR-GO, Fe-GS), the four BET values, and the seven uptake values with T/P/units, plus source locations. Read the controlled vocabularies out of schema.py before any prompt was written. Authored the Claude Code prompt that generated data/raw/staging_HYC-0013.csv. Claude Code wrote that file and nothing else; it did not touch measurements_v0.1.csv, the source modules, tests, or any existing data, and no CI was created.

**What I did.** Verified all twelve ASCII search keys by Cmd+F (12/12 hit). Spot-checked Table 3 (p. 8317) and the BET paragraph (p. 8315) against the located values by screenshot rather than transcription. Verified the staging file from the terminal with pandas rather than from Claude Code's self-report — which mattered, because a truncated paste had left row 7 partially empty and Claude Code correctly reported the gap rather than inventing values. Re-verified all seven rows against the PDF before the append. Took a validation baseline at session start (112 rows, 0 errors, Unspecified uptake_type ×89, mmol/g-wt% inconsistent ×1) and confirmed the merged file landed at exactly 119 rows, 0 errors, 96 + 1 warnings, no new warning type. Pasted the DOI from the publisher record, not from the model.

**Decisions and who made them.** Four calls were escalated to me one at a time with the model's read and basis stated. In all four I ratified the recommendation rather than deriving the call independently, and the log records that honestly:
- `uptake_type = unspecified` on all seven rows. The paper never labels the Table 3 values excess or absolute; its only use of "excess" is the p. 8318 statement that H₂ and He adsorb in nearly equal volume on TR-GO, described as the characteristic feature of no excess adsorption — a claim about the helium-correction argument, not a type assignment.
- `material_class`: GO → graphene_oxide, TR-GO and CR-GO → reduced_graphene_oxide, Fe-GS → graphene with dopant_element = Fe. Fe-GS was classified as graphene rather than composite so it stays comparable to the other metal-decorated rows in the corpus. Fe loading is unreported in any unit, so dopant_concentration_at_pct is blank.
- `extraction_confidence = 5` on all seven rows. Every value is table-direct, with the BET values independently restated in body text and Conclusions and the three 77 K uptakes restated volumetrically (230 / 60 / 240 cm³/g STP) reconciling at 22.414 mL/mmol.
- Tier score 9/10 → Tier A, losing only the uptake-type point.

**Premise correction.** The paper was recommended to me as "Fe-decorated rGO, a second spillover paper to pair with HYC-0027." Both halves were wrong and the PDF corrected them: the Fe-decorated sample is arc-discharge graphene sheets, not rGO, and the authors attribute uptake across all four samples to defect concentration rather than spillover — Fe-GS at 2.16 wt% only marginally exceeds undecorated TR-GO at 2.07 wt%. Spillover appears in this paper only in its literature review. The recommendation was flagged as provisional when made and corrected out loud once the PDF was open.

**The Chahine call — the substantive judgment in this entry.** The §13.4 criterion "value within Chahine-consistent range" was scored 2/2 despite TR-GO at 375 m²/g yielding 2.07 wt% (≈2.8× the Chahine estimate of 1 wt% per 500 m²/g at 77 K) and CR-GO at 9 m²/g yielding 0.54 wt% (≈30× it). Reasoning: §13.2 fixes the operative physisorption bound at roughly 1 wt% at 300 K/100 bar and flags 77 K values above roughly 6 wt%; this paper's 300 K values (0.1–0.32 wt%) sit well inside and its 77 K values are nowhere near 6 wt%, so nothing here resembles the 5–14 wt% room-temperature claims the tiering system exists to penalize. Chahine is a linear surface-area scaling that this paper explicitly argues against, presenting CR-GO as its evidence that defect concentration drives uptake independently of area. Scoring the paper down for deviating from a correlation it is presenting evidence against would penalize the finding rather than the reporting quality.

**Schema and methodology notes.** No new schema gap surfaced. Fig. 4 reports pore-size distribution only as relative volume normalized to the saturated amount, so no absolute pore volume in cm³/g exists to record — this is adjacent to open schema gap #4 but is a reporting limitation of the paper, not a schema limitation. Two internal inconsistencies were recorded in row notes without affecting extracted fields: Fig. 9(b) text states the as-prepared TR-GO I_D/I_G as 0.946 while Table 2 assigns 0.946 to GO and 0.848 to TR-GO (Table 2 taken as authoritative per the primary-table rule, now the fourth such conflict in the corpus), and the Fig. 2 caption mislabels panel (d) as CR-GO where the figure and body text say Fe-GS. Table 1 (p. 8312) is a literature summary of other groups' data including Parambhath (already HYC-0027) and was excluded from extraction entirely.

**Outcome.** 7 rows, Tier A, extraction_confidence 5, all table_direct. Dataset at 119 rows across 11 papers. Committed as d696dc3, pushed to origin/main.
## 2026-09-24 — Session: Phase A (pipeline automation)

**Phase.** §18 Phase A — the four helper scripts, with tests. No paper was
extracted and no dataset row changed in this session.

**Baseline at start.** Commit `3a37957` on `origin/main`. Dataset
`data/raw/measurements_v0.1.csv`: 119 rows, 11 papers, sha256
`55875a906d565df3…`, validation 0 errors, warning types `Unspecified
uptake_type ×96` and `mmol/g and wt% inconsistent ×1`. Test suite as the
manual recorded it: 82 tests.

**§6 did not match the repository, and this was surfaced before any work
began.** Three mismatches. The working tree was not clean: six untracked
files existed, a previous session having begun Phase A without committing
it. The test count was not 82 but 119, of which one was failing. Phase A was
therefore roughly 40% done rather than not started, and only A.1 had any
tests, so §18's "each with tests" was unmet. The untracked material was
treated as unverified draft, on the ground that §3.8 applies to a previous
session's output exactly as it applies to a subagent's.

**Work completed.** All four scripts under `scripts/`, each with tests, in
five commits (`4567286`, `9f10e12`, `55f5c44`, `70dab25`, `3d3fb57`):
`validate_row_detail.py` (per-row validation detail), `inspect_columns.py`
(column inspection CLI), `append_paper.py` (§9.1 steps 11–14 as one
refusing command), `digitize_figure.py` (§3.4 programmatic digitization).
394 tests pass; `ruff check --select E,F` is clean across `scripts/` and
`tests/`. The dataset, `src/hycan/`, `references/`, and the pre-existing
test modules are byte-identical to `3a37957`.

**Verification architecture used on this session's own work.** Four
isolated agents, none of which saw the reasoning behind the code they were
judging. Two audited the first version, two re-audited after the fixes with
instructions to be adversarial. Every defect below was demonstrated by
execution, not inferred from reading.

**Problems — what the audits found, stated without minimisation.**

The first pair found 6 critical and 7 high defects in code that passed 239
tests. Three mattered most. `append_paper.py` wrapped its rollback in
`except CheckFailed`, but `verify_merged` reaches pandas, which raises
`ParserError`; a staging file with 39 fields against a 38-column header was
absorbed by pandas as an index, passed all eight preflight checks, and left
the dataset unparseable with no rollback — taking `validate_data.py` and
`validate_row_detail.py` down with it, so every recovery tool failed at
once. The §11.5 new-warning-type stop condition was bypassable because
`--baseline` never checked which dataset the baseline came from. And
`digitize_figure.py` had no plot-area bound, so a legend sample in the
series colour won the per-bin median: 4.88 wt% extracted as 0.82 wt%, an
83% error across 11% of the x range, archived as data with exit 0.

The second pair, given the fixed scripts, found that four of the ten fixes
were incomplete and that the fixes had introduced problems of their own.
Two produced silently wrong numbers. `load_rgb` called
`Image.convert("RGB")`, which discards alpha rather than compositing it, so
a semi-transparent fill under a curve matched the series colour at full
strength and every extracted value came out at almost exactly half its true
value — internally consistent, plausibly shaped, undetected by any check.
And because two reference points fix a mapping exactly at those two points,
a log axis read without `--log-x` is correct at both ends and wrong
everywhere between; `check` cannot catch it, because it constrains y at an
x the calibration pins, and papers state values at axis endpoints more
often than mid-axis. One omitted flag produced pressure errors of 13× to
398× in an archive marked `passed`.

**A failure in this session's own method, recorded because §17.1 requires
it.** After the first fixes, a mutation sweep was run against the four
functions that had just been changed, all four mutations were caught, and
that was taken as evidence about the test suite. It was evidence about four
lines. An isolated auditor then ran 56 mutations across the whole suite and
**41 of the first 42 survived**: the tests asserted that a code path had
been taken, not what it computed. Disabling the backup hash verification
entirely survived, because the test asserted the word "verified" appeared
in the output and that word came from an unconditional `print`. One
assertion, `assert "merged row count is" in out or "errors" in out`, was
vacuous because the second disjunct is always true after preflight prints
"0 errors". The tests were rewritten and every mutation an auditor used now
fails the suite, including the eleven written against the second round of
fixes.

**Decisions made.**
- Untracked Phase A material from the previous session treated as
  unverified draft rather than as completed work (§3.8).
- The failing test was judged correct and the implementation wrong: the
  `n_rows + 2` tolerance for a trailing blank line also absorbs exactly one
  newline inside a quoted field, which is the only thing the check exists
  to detect. The same defect was then found in `append_paper.py`'s
  `describe_file`, where it gated the safety of a byte-level append onto
  the dataset and nothing tested it.
- Refusal thresholds for multi-cluster detection were changed from a raw
  count to a contiguous-run test after an audit showed the original refused
  ordinary marker-and-line isotherms, error-bar caps and dash gaps.
  Refusing correct extractions trains an operator into
  `--allow-multimodal`, which disables the check that matters.
- Baseline provenance was changed from a path comparison to a hash of the
  row prefix the baseline described, after an audit defeated the path check
  using file moves alone.
- `ruff --fix` was run broadly at one point and modified
  `tests/test_schema.py`, a pre-existing file §6.7 places off limits. It
  was reverted immediately and confirmed byte-identical. The lesson is
  §6.7's: a tool that edits in place needs its scope named explicitly.

**Known limitations carried forward, not fixed here.** Nothing consumes a
digitization archive's `status` field: no validator and no part of
`append_paper.py` reads it, so a row carrying
`extraction_method = figure_digitized` can still be appended without
reference to any archive. Closing that belongs with Phase B's schema work.
`check` verifies the points it is given and says so, but nothing enforces
that every value a paper states from a figure has been checked. A staging
cell containing a NUL byte is still accepted. The default region of
interest is derived from the calibration reference pixels, which is the
plot area only when those pixels are the extreme ticks; calibrating from
interior ticks silently narrows the search, and the tool reports how many
pixels it excluded so this is visible rather than silent.

**Pipeline bottlenecks.** The two §18 named (summary-only validator output,
ad-hoc pandas heredocs) are closed by A.1 and A.2. The bottleneck this
session revealed is different: a test suite that passes is weak evidence
that code is correct. Mutation testing found in minutes what 239 passing
tests did not, and should be run against any new safety-critical check
rather than only when something looks wrong.

**State at end.** Branch `phase-a-pipeline-automation`, five commits ahead
of `3a37957`. Dataset unchanged at 119 rows, 11 papers, 0 errors, warning
types 96 + 1. 394 tests pass. **Not pushed:** the git proxy refuses writes
to `AvinGupta-ship-it/hycan-db` because the repository is not in this
session's authorized set. Reads succeed, which is how `origin/main` was
confirmed at `3a37957`. The work was delivered as a git bundle instead. Per
§2.4 this is recorded as not done rather than as done.

**Next.**
1. Authorize the repository for the session, or apply the bundle, so Phase
   A is on `origin/main`.
2. Phase B — schema v1.1: the four gaps in §8.5 and the two cleanups in
   §8.6, in one migration, with the §13.4 limitation written into
   `docs/reproducibility_tiering.md`.
3. Phase C — the twelve unextracted PDFs in §6.3 under the §3.2 dual-agent
   protocol, with the figure-only papers batched so all required crops are
   requested at once.

## 2026-09-25 — Session: Phase B (schema v1.1)

**Phase.** §18 Phase B — close the four gaps in §8.5 and the two cleanups in
§8.6, in one migration.

**Baseline at start.** Commit `ca737dc` on `origin/main`. 119 rows, 11 papers,
38 columns, sha256 `55875a90…`, 0 errors, warnings `Unspecified uptake_type
×96` and `mmol/g and wt% inconsistent ×1`. 394 tests.

**State at end.** Commit `94d634c` on `origin/main`, confirmed by reading the
remote rather than the push output. 121 rows, 11 papers, 40 columns, sha256
`b75dd0d0…`, 0 errors, warnings `Unspecified uptake_type ×98` and `mmol/g and
wt% inconsistent ×1`. 418 tests. Tier distribution 36 A / 77 B / 5 C / 3 D.

**Pipeline.** Claude (this session) as Agent A for the three source
extractions; an isolated agent as Agent B, given the papers and the candidate
values only, with no access to Agent A's reasoning (§3.2). Migration and
backfill applied by committed scripts (`scripts/migrate_v1_1.py`,
`scripts/backfill_v1_1_sources.py`), each of which refuses to run twice.
Both read and write raw CSV cells rather than going through pandas, so an
unmodified cell is byte-identical by construction.

**Verification.** 40 cells submitted to Agent B across three papers. Forty
agreed. Agent B raised one DISAGREE, and it was correct: the list of
HYC-0005 total pore volumes in the verification prompt held six values for
seven samples, having dropped AX-21's 1.14, which made everything from AX-21
onward appear misaligned. The dataset was right and the prompt was wrong.
Recorded here because a verification protocol that only ever catches errors
in the data is not being tested on its own inputs, and because the error was
in a hand-written list — the same class of mistake the protocol exists to
catch, arriving from an unexpected direction.

**Source acquisition.** Three PDFs supplied by the author on request, batched
into one list per §7.4 rather than requested one at a time.

**Decisions and their basis.**

- *Gap 3, what replaces the unconditional uptake requirement.* Temperature and
  pressure are required exactly when a row reports any uptake value. A row
  reporting no uptake must instead report at least one characterization value;
  a row reporting neither asserts nothing and is rejected. The §8.2 rule that
  an uptake-bearing row must carry uptake gravimetrically is preserved, scoped
  to rows that report uptake.
- *Gap 4, severity.* `ultramicropore ≤ micropore ≤ total` is an ERROR, checked
  pairwise so a missing middle term cannot suppress the outer comparison.
- *A manual/code mismatch resolved in the manual's favour (§0).* §11.2 has
  always specified ERROR for `micropore_volume > total_pore_volume`; the v1.0
  code raised it as a warning. It is now an ERROR. No row in the corpus
  violates it, so the dataset is unaffected. §11.4's list of two behaviours
  that look like bugs and are not does not include this one, so it was treated
  as a genuine mismatch rather than a deliberate divergence.
- *Column placement.* Both new columns appended at physical positions 39 and
  40, matching how `measurement_id` and `uptake_ml_stp_g` were added, so the
  §6.7 positional-append property survives.
- *HYC-0016 relabelling scope.* Applied to rows whose `material_description`
  literally begins "Reduced graphene oxide" — 11 rows. S13 reads "Thermally
  exfoliated graphene oxide" instead. Thermal exfoliation does reduce GO, so
  `reduced_graphene_oxide` is defensible, but it is an inference rather than a
  reading, and the Klechikov paper was not in this batch. Left as `graphene`.

**Premise corrections — both §8.6 suspicions confirmed, one more strongly than
expected.** §8.6 asked whether HYC-0005's rows had a total surface area
entered into the BET field. They did. Table 1's column is headed `TSA` and
footnoted "TSA, total surface area", and the strings "BET" and "Brunauer"
occur nowhere in the paper; its only method sentence names instruments and no
model. All 25 rows had been asserting a determination the authors never
claimed. `surface_area_method` is now `unspecified` and
`extraction_confidence` drops 5 → 4. The values stay in
`bet_surface_area_m2_g` because the schema has no generic surface-area field;
gap 1's new field is what makes the disclosure possible.

**Unplanned gain.** The same paper's `V_DR(CO2)` column is defined in text as
"the narrowest micropores (i.e., pores size smaller than 0.7 nm)" — the same
physical quantity as HYC-0021's ultra-micropore column, by a different method
(Dubinin-Radushkevitch on a 273 K CO₂ isotherm rather than DFT). That put 25
further rows into the new field. The corpus now holds 29 ultra-micropore
values across two papers, both of which argue uptake tracks ultra-microporosity
rather than total surface area. Until this migration neither claim could be
tested against the other.

**Source anomalies recorded.**

- Sethia 2016: body text says BET 1312 m²/g where Table 2 says 1317 (primary
  table wins, §3.7); abstract says 2.94 wt% where Tables 1 and 2 say 2.96; two
  cross-references point at the wrong table number.
- Singh 2020: abstract, highlights, body and conclusion all give EGR (300)'s
  total pore volume as 1.64 cm³/g while Table 2 gives 1.63. The table wins.
  The manual's §3.7 conflict table records this as "1.63 vs 1.64 wt%"; the
  unit is cm³/g, not wt%. **The manual should be corrected.**
- Singh 2020 naming trap: the paper uses "GO exfoliated at 300 °C" in prose to
  mean the sample Table 2 calls EGR (300). An extractor matching on "GO" plus
  a wt% will produce a false GO uptake of 3.12. Recorded in the GO row's notes.
- Singh 2020: Fig. 9(c) and 9(f) mislabel samples as "EGO" rather than "EGR".

**Schema and methodology notes.** A new limitation surfaced, of the same kind
as §13.4's: the §13.3 tiering rubric scores the reporting quality of an uptake
measurement, and has nothing to say about a characterization-only row. The two
recovered HYC-0018 rows inherit their paper's tier rather than being scored
independently, and their notes say so. This should be written up alongside
§13.4 when that section is next touched.

**What is still open.** HYC-0016-S13's material_class, pending the Klechikov
paper. `average_pore_diameter_nm` is in Singh's Table 2 for the three
pre-existing HYC-0018 rows and was not backfilled, being outside the
migration's stated file scope. Nothing consumes a digitization archive's
`status` field, so a `figure_digitized` row can still be appended without any
check that its §3.4 gate passed — the natural fix is a `digitization_archive`
field, and this migration was not the place to add one.

**Where the pipeline was slow.** Delivery, not analysis. The executing session
could read `origin` but not write to it, so every commit reached the
repository as a git bundle applied by hand. Two rounds were lost to a glob
matching a stale bundle in the Downloads folder and to two bundles built with
different ref names. Bundles should carry a distinctive name and always be
built from a named branch. Authorizing the repository for the session removes
the whole class of problem.

**Outcome.** Schema v1.1 complete. HYC-0025 unblocked. Commits `3ec8673` and
`94d634c` on `origin/main`.

## 2026-09-25 — Phase C, first three papers under the dual-agent protocol
Tool: Claude Opus 5 in a cloud session, executing the manual's §18 Phase C with
isolated subagents as Agent A (extractor) and Agent B (verifier).
Purpose: Extract the twelve remaining Phase C papers under §3.2, starting with
HYC-0025 (unblocked by schema v1.1) and working through the batch.

**What actually ran.** Six papers were extracted by six independent Agent A
instances that each received only the PDF and the field specification — no
access to each other, to the dataset, or to any prior extraction. Three papers
were then verified by Agent B instances that received the PDF and the candidate
rows **only**: no reasoning, no search keys, no uncertainty flags, no note that
anything was doubtful. Three papers were appended.

**Dispute rate, first measurement of it.** 132 cells verified, 0 disputed
(HYC-0025 42/42, HYC-0012 64/64, HYC-0017 26/26). This is the first number the
protocol has produced and it should be treated with suspicion, not satisfaction.
Three papers is a small sample; two of the three were tabulated papers where the
values are unambiguous; and the one historical case where a verifier caught
something real, it caught an error in the *verification prompt*, not in the
dataset. What the pass demonstrably did was surface internal contradictions and
traps that a single reader would plausibly have written into the dataset:

- **HYC-0025** — the abstract states 273 K where the Methods section, three
  tables and two figure captions state 303 K; one sentence states 20 bar where
  five other places state 16; one sentence transposes two samples' dopant
  concentrations, contradicted by its own next sentence and five tables. Also
  that Table 8's Langmuir Qm values (0.257–1.411 wt%) are fitted maxima 2.8–4.2×
  the measured uptakes, and that the paper's Langmuir *isotherm* is not a
  Langmuir *surface area* — `surface_area_method = none`, the corpus's first.
- **HYC-0012** — the running text lists the samples in an order that reverses
  Table 1's for the last two, so a reader mapping the text onto the table's value
  column would swap the CO2-oxidized and KOH-activated results. Agent B
  independently confirmed the table binding and reached the same resolution.
- **HYC-0017** — the room-temperature result exists only as an upper bound.
  Agent B independently arrived at the same conclusion the adjudicator had
  reached, that writing `0.2` would convert a bound into a measurement, and
  proposed the same fix (a boolean flag). That convergence is weak evidence of
  correctness and is recorded as such.

**What was verified from the artifact, not from a tool's self-report (§3.8).**
Every append was re-read from disk by `scripts/append_paper.py` against a
content-bound session baseline: 121 → 127 → 133 → 135 rows, 0 errors at each
step, no new warning type at any step. 418 tests passing and `ruff` clean after.
The 8.0 wt% arithmetic in HYC-0011 below was recomputed by the adjudicator
rather than accepted from the extractor's report.

**The substantive finding is not the three papers.** Four of the six papers read
hit a schema limitation, and 35 of 43 extracted rows are blocked on the schema
rather than on evidence. `docs/schema_v1_2_gaps.md` is the inventory: bounded
uptake values have no representation; an uptake-bearing row cannot say that its
paper never stated a temperature (HYC-0011, HYC-0015 and HYC-0009's TPD rows all
need this); a paper reporting a micropore and an external surface area but no
total has nowhere to put either (HYC-0007, eighteen measured values); and
`validate.py` has no consistency check between `uptake_ml_stp_g` and
`uptake_wt_pct`, which is why HYC-0009's mutually irreconcilable wt% and volume
columns had to be caught by a reader instead of by the validator. The v1.1
migration was executed as one batch for exactly this reason and v1.2 should be
too, so nothing was implemented and six Phase C papers remain to be read.

**A verified-but-unresolved scientific problem, recorded rather than resolved.**
HYC-0011's headline 8.0 wt% cannot be reconciled with the paper's own numbers.
Its areal uptake (6.3×10⁻⁶ g/cm²), its stated film mass (9.0 mg) and its two
stated film areas (12 and 18 cm²) imply 0.84–1.26 wt%; reaching 8.0 wt% would
require a film area of ~114 cm², nine times the largest area the paper states.
The arithmetic was checked independently by the adjudicator and is correct. The
paper gives no intermediate working, so the cause cannot be determined from the
text, and no cause is asserted here. Under `docs/reproducibility_tiering.md`'s
stated principle — "Tiering is disclosure, not deletion" — the row belongs in
the corpus at Tier D with that discrepancy quoted verbatim in its `notes`, not
dropped. It is currently blocked on gap 2, not on this.

**One judgment call flagged rather than buried.** HYC-0025's §13.3 method score
sits on the Tier B/C boundary: the paper describes its protocol (apparatus type,
250 mg sample, degas at 423 K for 2–3 h under vacuum, ~100 s to equilibrium) but
never identifies the instrument and describes no calibration or blank correction.
Scored 2, giving 6 → Tier B; scored 1 it would be 5 → Tier C. The basis is in the
row notes so the call can be reversed by anyone who disagrees with it.

**One question left open on purpose.** HYC-0017's `material_class` stays
`graphene` and `synthesis_method` stays `other`, on the paper's own words: it
says only "a chemical exfoliation method" and never uses "oxide", "oxidation" or
"reduction". Verification flagged that its XPS C/O ratio of 10.8–14.9 is more
typical of well-reduced graphene oxide, and that its ref [10] (Wu et al., Carbon
2008) would settle the route. That reference could not be retrieved — the
publisher page returned nothing through this session's proxy and PubMed returned
a CAPTCHA. The §8.6 HYC-0016 relabel was applied to rows whose own
`material_description` read "Reduced graphene oxide"; relabelling here would rest
on an inference from a C/O ratio instead, so it is recorded in the row notes for
revisit rather than applied.

**Outcome.** 135 rows, 14 papers, 0 errors, 418 tests. 14 rows now
distinguishable as dual-agent-verified. Phase C is 3 of 12 papers appended, 6 of
12 read, and gated on a v1.2 schema decision for the rest.
