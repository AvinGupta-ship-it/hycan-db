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

## 2026-09-25 (continued) — Phase C completed to the schema boundary
Tool: same session, same protocol. Five further papers extracted by isolated
Agent A instances (HYC-0019, 0022, 0024, 0026, 0029), two of them verified and
appended.

**Dispute rate is no longer zero, and that is the useful result.** 308 cells
verified across five papers, 304 agreed, **4 disputed — 1.3%**. All four were
`synthesis_method` on HYC-0022. The extractor assigned `commercial` to all six
samples because the carbon skeleton was bought. The verifier rejected that for
the four samples the authors activated themselves, and its argument was better
than the extractor's: the paper says "Both physical and chemical activations
were performed in our study", and Table 1 reports a carbon yield — 62%, 49%,
53%, 43% — for exactly those four samples and a dash for the as-received one. A
sample with a burn-off yield was not purchased in that state. The disagreement
was upheld.

Two things worth recording about that dispute rather than just its outcome.
First, it was a vocabulary-semantics judgement, not a misread number — which is
the failure mode the isolation protocol is *least* obviously designed to catch,
so it is a more interesting result than another clean sheet would have been.
Second, it only existed because `synthesis_method` has no value for activation.
A schema gap manufactured a disagreement between two careful readers. That is
now gap 5 and it is the widest gap in the inventory: five of the twelve Phase C
papers had to be forced on it.

**Verification also caught two field-semantics errors that no validator would
have.** On HYC-0022 the extractor filled `average_pore_diameter_nm` from the
paper's BJH column. The verifier pointed out that the paper itself calls that
column the *mesopore* size, that BJH desorption analysis is invalid for the
type-I isotherms of the two best samples, and that every scientific claim in the
paper rests on the *other* pore-size column, the HK median micropore size
(0.59 and 0.67 nm). Storing 2.5 nm for the sample whose performance the paper
attributes to 0.67 nm would have been worse than storing nothing, so the field is
empty on all nine rows with both series recorded in `notes`. Same reasoning
emptied `ultramicropore_volume_cm3_g`: that field is documented at a 0.7 nm
cutoff and carries 0.7 nm values for two existing papers, while HYC-0022's
column is cut at 1 nm. Mixing the cutoffs would have destroyed the one quantity
schema v1.1 added specifically to make comparable across the corpus.

The verifier also pinned the paper's wt% denominator independently, without the
Supporting Information: 43.2 g/L = 610 g/L × 0.0708 exactly, so wt% is grams H2
per 100 g of adsorbent rather than per total system mass.

**Verified from the artifact, not from tool self-reports (§3.8).** Every append
re-read from disk against a content-bound baseline: 135 → 147 → 156 rows, 0
errors and no new warning type at each step. 418 tests passing and ruff clean
after. `origin/main` confirmed at the pushed commit by reading the remote ref,
not the push output.

**Where Phase C actually ended.** Not at twelve papers appended — at the schema
boundary. 133 rows extracted, 35 written, **98 held**, seven papers blocked, and
no two blocked by the same limitation. `docs/schema_v1_2_gaps.md` is the
complete inventory: ten gaps, each naming the papers it bites, each with a
proposed fix, in a stated order. The three most consequential were invisible
before this batch:

- **HYC-0024 yields zero storable uptake values.** Eight samples measured at
  293 K and 100 bar, and the paper's only tabulated hydrogen quantities are
  volumetric densities in kg/m³ of micropore volume. Its wt% values exist solely
  in a figure. A wt% could be computed as density × micropore volume, but the
  paper reports two micropore volumes and never says which is the basis, so that
  would be our arithmetic passed off as its measurement.
- **HYC-0029's measurement is not isothermal.** Its thirteen uptakes are weight
  differences across a 303 → 673 → 303 K cycle in flowing hydrogen at 1 atm.
  Storing `temperature_k = 303` would assert an isothermal 303 K measurement that
  did not happen, and those values are not commensurable with the rest of the
  corpus. Appending them unflagged would have quietly corrupted every Chahine
  comparison. This will recur in every TGA-cycling spillover paper.
- **Metal loading in weight percent has no field**, which means *both* of the
  corpus's spillover papers — HYC-0029's cobalt and the already-present
  HYC-0027's palladium — cannot be analysed against the variable their authors
  varied.

**A correction to my own earlier reasoning.** The first half of this session
recorded the gap inventory as four items after six papers. That was premature in
a way worth noting: reading the remaining six papers took it from four gaps to
ten, and three of the six new ones (9, 7, 10) are more consequential than
anything in the original four. The decision to hold the v1.2 migration until all
twelve were read was correct, but the earlier document's confident framing of
"now complete" at the six-paper mark was not, and had I acted on it the migration
would have shipped missing the gap that matters most.

**What was not done, stated plainly.** Schema v1.2 is not started. The 98 held
rows are not in the dataset. HYC-0017's `graphene` versus
`reduced_graphene_oxide` question is still open — its ref [10] could not be
retrieved through this session's proxy and PubMed returned a CAPTCHA.

**Outcome.** 156 rows, 16 papers, 0 errors, 418 tests. 35 rows dual-agent
verified. Phase C read complete; appending complete to the schema boundary.

## 2026-09-25 — Phase C appended: 206 rows, 21 papers
Tool: same session. Five Agent B verification passes in parallel against the
five papers schema v1.2 unblocked, then adjudication and append.

**The dispute rate stopped being zero and became informative.** 704 cells
verified across ten papers, 673 agreed, **23 disputed and upheld, 8 disputed and
dismissed** — 4.4% raised, 3.3% upheld. Four of the five papers in this batch
produced an upheld dispute where the first three had produced none. The protocol
did not change; the papers got messier and the questions got harder, because the
v1.2 flags gave the verifier something substantive to disagree about.

**In every upheld dispute the verifier was right.** Worth recording what they
were, because the pattern is not what I expected:

- **HYC-0026, 16 cells, the largest so far and three separate errors.** The
  pressure had been inferred as 40 bar; the verifier established that every
  "4 MPa" in the paper that functions as a reporting pressure belongs to its
  *excess* isotherms, measured on a different instrument, while the recorded
  values are the *adsorbed* quantity — so the pressure is genuinely unstated and
  assigning one asserted a condition that does not exist.
  `average_pore_diameter_nm` held the paper's L0, which §2.2.2 defines as the
  average *micropore* diameter, on samples carrying 0.19–0.59 cm³/g of mesopore
  volume. And a dopant concentration had been recorded on three samples that
  were never doped — that figure is the anthracite precursor's native nitrogen.
- **HYC-0022, 4 cells.** `commercial` on four samples the authors activated
  themselves, refuted by the carbon yields the paper's own Table 1 reports for
  exactly those four.
- **HYC-0011, 2 cells.** `other` understated a measurement with every defining
  element of a manometric one; and a measurement whose value comes from the
  non-closure of a 295 → 353 → 295 K ramp had been coded isothermal.
- **HYC-0029, 1 cell.** `not_applicable` asserted that no measurement existed
  for the 873 K sample when the paper plots it in Fig. 9 and states a trend
  requiring all three to have been measured. That coding would have foreclosed
  recovering the value later.

Notice that none of these were misread numbers. Every numeric cell in all five
papers agreed. What the isolation caught was **field semantics** — a value put
in a field that means something slightly different from what the value is. That
is a failure mode the protocol was not obviously designed for, and it is the
second batch running where it has been the thing that mattered.

**Eight disputes were dismissed, and the reason is now this project's oldest
defect.** On HYC-0015 the verifier reported that `temperature_unstated`,
`measurement_mode` and `uptake_bound` "are not columns" and that a null
temperature on an uptake row is a schema error. All three are columns, at
physical positions 42, 44 and 41, and the null is exactly what gap 2 permits. It
had read `HyCANDB_Execution_Manual_v2.2.md`, which still documents a 40-column
v1.1 schema and a 119-row corpus, instead of `src/hycan/schema.py`. Two other
verifiers in the same batch flagged the same staleness as a finding and checked
the code instead. **A stale manual manufactured eight false disagreements and
will keep doing so.** Every substantive finding in that report was adopted,
including its argument that HYC-0015's 1.90 wt% at 80 bar and nominal room
temperature warrants Tier D on the physics override rather than the B first
assigned.

**A tooling gap the append surfaced.** HYC-0011's 8.0 wt% correctly trips
`Pre-2005 raw-CNT high uptake (Tier D)`, a warning type new to the corpus, and
§11.5 makes that a stop condition. The stop worked — and there was no way past
it, which meant a *correct* new warning made a legitimate row unappendable. The
fix is `--expect-new-warning`, which takes the exact type string so it cannot be
passed by reflex, admits only the type named, and refuses a type that does not
actually appear so it cannot be left behind as a standing exemption. The row is
in at Tier D with the discrepancy quoted, per disclosure-not-deletion.

**A factual error in my own documentation, found by a verifier reading it against
the paper.** `docs/schema_v1_2_gaps.md` said reaching 8.0 wt% "would require a
film area of ~114 cm², nine times the largest the paper states". 114 cm² is
9.52× the *smaller* stated area and 6.35× the larger. The area figure was right
and the multiplier attribution was wrong, in two files. Corrected in place with
the correction noted. This is the second documentation arithmetic error this
session — the first was the 133/98 row counts — and both were in summary
sentences rather than in the per-item numbers they summarised. The lesson is
specific: compute totals and ratios from the table rather than writing them
alongside it.

**Verified from the artifact, not from tool self-reports (§3.8).** Every append
re-read from disk against a content-bound baseline: 156 → 176 → 192 → 199 → 201
→ 205 → 206 rows, 0 errors at each step. Two appends were refused and both
refusals were correct — a missing `measurement_id` on four characterization-only
rows, which the HYC-0018 precedent requires, and the new warning type above.
473 tests and ruff clean after.

**What was not done.** Stage 4 is not started, so HYC-0007's 10 rows and
HYC-0024's 8 remain held, along with one HYC-0011 row (an areal uptake in g/cm²)
and one HYC-0015 row (an interlayer spacing). HYC-0027 is not backfilled with
its palladium loading, so the spillover subset still cannot be analysed against
metal loading. `score_reproducibility` now has a blind spot v1.2 created: with
`temperature_k` null the Chahine branch returns "cannot assess", so every
`temperature_unstated` row collects a free point and HYC-0011's ordinary
0.26 wt% scores identically to its discredited 8.0 wt%. And the manual is still
stale.

**Outcome.** 206 rows, 21 papers, 0 errors, 473 tests. The 20-paper Phase 3
milestone is cleared. 85 rows dual-agent verified across 10 papers, at a
measured 3.3% upheld dispute rate.

## 2026-09-26 — Phase C.1: HYC-0007 and HYC-0024 under the dual-agent protocol

**Pipeline.** Agent A (locate-only, one pass per paper, §9.2), Agent A row
construction, Agent B verification (§3.2, one isolated pass per paper), Claude
Code for the staging builder. Schema v1.3 shipped first (commit `3945d81`)
because both papers were held on gaps it closes.

**Source acquisition.** Both PDFs from the Project knowledge base. DOIs
`10.1016/j.mseb.2003.10.095` and `10.1021/jp014543m`, both matching
`references/paper_tracking.csv`.

**Extraction.** HYC-0007: 9 samples in Table 1, of which 7 are carbon; 8 rows (4
uptake, 4 characterization-only). HYC-0024: 8 samples; 11 rows (8 at 293 K /
100 bar plus 3 for KUA1 at 50/150/200 bar from §3.2's text).

**Verification.** 446 cells verified, 10 disputed, **0 numeric cells disputed.**
- HYC-0024: 282 cells, 0 disputes. The verifier independently re-derived Table
  1's ambiguous column alignment for three samples and reached the same
  conclusion by four arguments, two of them new: significant figures (Ms prints
  to one decimal, adsorbed density to two) and Ms/rho(H2) reproducing the
  paper's stated ratio ordering.
- HYC-0007: 164 cells, 10 disputes, all upheld — 4 incomplete
  `source_location`, 4 `extraction_confidence` against the data-dictionary
  rubric, 1 `measurement_method`, 1 field-meaning error
  (`activation_method` → `functional_groups`).
- Quote verification: every quoted sentence located.

**Decisions and their basis.**
- HYC-0007's H-YZ and H-ZSM-5 excluded: zeolites, not carbon (§7.2). LaNi5
  excluded: apparatus-validation standard, not a sample.
- `bet_surface_area_m2_g` null on all HYC-0007 rows: the paper reports no total
  surface area, only S_micro and S_ext from an alpha-s plot. Summing them would
  fabricate a total.
- HYC-0007's 303 K `measurement_method = unknown`, against the extraction's
  `other` and the verifier's `volumetric_sieverts`. The paper names no
  technique; `other` asserts one outside the vocabulary and the verifier's
  reading, though sound, is inference (§3.11).
- HYC-0024 `uptake_type = unspecified` on all rows under §3.6: the words
  "excess" and "absolute" appear nowhere, though the arithmetic is a Gibbs
  surplus.
- HYC-0024-M4 `uptake_wt_pct = 1.0`, `uptake_bound = approximate`: the paper's
  own prose figure, stated in both the abstract and the conclusions. Not
  tabulated, hence approximate.

**Fields left deliberately empty.** `ultramicropore_volume_cm3_g` and
`ultramicropore_cutoff_nm` on all HYC-0024 rows: the paper states no size cutoff
for either DR volume, and filling the field would assert the 0.7 nm it is
documented at. `packing_density_g_cm3` and `volumetric_capacity_kg_m3` on three
HYC-0024 rows: blank in Table 1. `uptake_wt_pct` on ten HYC-0024 rows: the
paper's per-sample wt% exists only in Figure 2, and deriving it would require
choosing between two micropore volumes it never distinguishes. All uptake fields
on four HYC-0007 rows: figure-only (§3.4).

**Premise corrections.** The first extraction pass asserted that HYC-0024 states
no gravimetric value outside a figure. It does, twice. Corrected.

**Source anomalies.** HYC-0007: the abstract and conclusion both claim 77 K
isotherms over 0-3.5 MPa where §2.2 restricts them to 0.1 MPa; W_ave = 2V/S is
the slit width for the ACFs but the cylinder radius for the SWCNTs, so it is not
a cylinder diameter for those samples. HYC-0024: Figure 4's caption gives Ms in
g/cm3 against kg/m3 everywhere else; the CF sentence in §3.1 reads "small enough
to obtain an acceptable" where the argument requires "too small"; the
adsorbed-density denominator is unspecified; KUA1's micropore volume overshoots
its own implied void volume by 24%.

**Validation.** Baseline 206 rows / 0 errors / 2 warning types. After: 225 rows,
0 errors, same 2 warning types, no new type. No `--expect-new-warning` needed.

**Outcome.** 19 rows, Tier B throughout, confidence 4-5. 206 -> 225 rows,
21 -> 23 papers. `paper_tracking.csv` set to `verified` for both.

**Where the pipeline was slow.** Two places. Row construction is now the
bottleneck rather than reading: a 67-column builder script with long `notes`
strings took longer than either the locate pass or the verification. A staging
helper that took per-sample values as a table and a shared note block would cut
it. Second, the invariant tests that pin absolute counts had to be updated three
times in one session; they should assert deltas and partitions, not totals, and
that change has now been made where it bit.

---

## HYC-0031 — Blankenship, Balahmar & Mokaya 2017, 2026-09-30

**Paper.** *Oxygen-rich microporous carbons with exceptional hydrogen storage
capacity*, Nature Communications 8:1545, doi `10.1038/s41467-017-01633-x`. First
Phase D paper extracted. Table-driven; no digitization.

**Correction check, done BEFORE extraction and closed.** The PDF's first page
reads "There are amendments to this paper" and its last "© The Author(s) 2017,
corrected publication 2021". HYC-0031 was one of the 32 Phase D papers the
screening log §8.3 records as *unchecked* for corrections. The notice is
`10.1038/s41467-021-26590-4`, October 2021, and it is **author-name only**: "the
author name L. Scott Blankenship was incorrectly written as Troy Scott
Blankenship II." No data changed. Crossref refused the WebFetch route (HTTP 429,
the §8.3 hazard), so the notice was located by search and read from PMC. Both
Agent A and Agent B independently flagged the amendment and named the two
CA-4800 cells as its likeliest targets; the notice rules that out, which closed
their largest residual uncertainty.

**Screening tag corrected.** The paper was screened in under `doped_77K`. **It is
not a doped carbon.** Its oxygen comes from the cellulose-acetate precursor, and
the authors set their work explicitly against doping: "A question that has not
been investigated is the effect of the level of oxygen content in porous
carbons." `schema.py` settles it — `dopant_element` carries only deliberately
introduced N, Fe and B, and no corpus row uses O, because every activated carbon
contains oxygen. XPS finds "only oxygen and carbon … in detectable quantities".
`material_class = activated_carbon`, `dopant_element` empty on all 32 rows. The
`doped_77K` funnel target therefore drops from 9 of 11 obtained to **8 of 10**.
The other ten `doped_77K` titles each name a real dopant, so this is one bad tag
and not a systematic screening failure — but titles are weak evidence and only
extraction confirms the rest.

**Dual-agent record (§3.2).** Agent A locate-only, Agent B on the PDF, the
candidate rows and `schema.py` with `notes`, `extraction_confidence` and
`reproducibility_tier` stripped, Agent C on the two live disputes with neither
prior reading attached.

- Cells checked: **1920** (32 rows × 60 columns as handed to B).
- AGREE 1814, DISAGREE 64, UNVERIFIABLE 42.
- The 42 unverifiable are all AX21 texture cells needing Supplementary Table 4.
- **Every cell carrying a hydrogen number agreed.** All 32 `uptake_wt_pct`, all
  12 `volumetric_capacity_kg_m3`, all 26 texture values, all three packing
  densities, every `uptake_type` and every unit reproduced. That is the §3.2
  pattern holding for a thirteenth paper: disputes are field semantics and
  provenance, not arithmetic.
- The 64 disagreements were 6 distinct findings. **4 upheld, 2 dismissed.**

**Upheld against the extraction:**

1. **AX21's three cryogenic values do have a determinable temperature.** The
   extraction set `temperature_unstated`. B and C both read 77 K and C's
   argument governs: the paper states its uptake measurements were at −196 °C
   **or** 25 °C, and separately reports AX21 excess at 20 bar and 25 °C as
   0.3 wt%, so 4.7 wt% excess at 20 bar cannot be the 25 °C point. The flag
   exists to stop a *convention* being substituted for a missing condition; it
   does not cover resolving a disjunction the paper states using a contradiction
   the paper supplies. The extraction was applying §3.5 too mechanically, and
   three real benchmark points would have dropped out of every temperature-
   filtered query and every Chahine comparison. `extraction_confidence` 4, not
   5, because the temperature is deduced; the inference chain is in `notes`.
2. **`uptake_bound` on the three room-temperature totals.** Marked `approximate`
   off the authors' word "estimated". They are stated definitely and repeated in
   the abstract, and every total in the paper is derived by the same eq. (1), so
   flagging only three would exclude the paper's headline room-temperature
   result from headline statistics while keeping the equally-derived 8.9 wt%.
   Corrected to `exact`.
3. **Three `source_location` page numbers.** The 20 bar room-temperature values
   are printed on p. 8; the sentence completes on p. 9. Corrected to pp. 8–9.
4. **No structured field carried the paper's own sample labels.** "AX21"
   appeared nowhere a query could reach. `material_description` now leads with
   the paper's label on all 32 rows.

**Dismissed, 2-1 (A and C against B):**

5. **`average_pore_diameter_nm` stays null.** B proposed 0.85 nm with method
   `DFT`. Table 2's "Pore size" column is **three NLDFT distribution maxima** per
   sample, not a central tendency, and the paper designates none as principal —
   it calls the 6–7 Å feature "extra" relative to its comparator. Recording one
   would assert a selection the authors never made; C's 4V/S check puts the
   smallest mode about 3× below a geometric average. `pore_diameter_method` is
   `unspecified`, the corpus convention on a null diameter. **The part of B's
   objection that was right:** the numbers were being lost silently, and are now
   recorded in `notes` per §11.4.

**Three defects in the paper as published**, each confirmed by more than one
reading and none of them touched by the 2021 correction:

- **CA-4800 total pore volume.** Body p. 3 gives 1.54 cm³/g; Table 2 gives 1.32.
  1.54 is CA-4700's *micropore* volume from the row above. 1.32 is stored, on two
  independent grounds: the paper's own micropore proportion, "88% for both
  CA-4700 and CA-4800", is satisfied by 1.17/1.32 = 88.6% and not by
  1.17/1.54 = 76%; and — Agent B's addition, from a different direction — eq. (1)
  with V_T = 1.32 reproduces both printed CA-4800 totals (6.83, 7.35 against
  6.8, 7.3) while V_T = 1.54 gives 6.97 and 7.56 and reproduces neither.
- **CA-4800 volumetric total at 20 bar.** Table 2 prints 41 g/L; the paper's own
  eq. (3) with its packing density of 0.56 g/cm³ gives 38.1. 41 is exactly this
  sample's 30 bar value. **The other 11 volumetric cells in Table 2 reproduce to
  within 0.55 g/L**, so this is one cell and not a method disagreement. Stored
  **as published**, with the arithmetic in `notes` and confidence 3: 38.1 is this
  project's number, not the authors'. Found independently by the extractor, by
  Agent A and by Agent B.
- **Isosteric heat.** The abstract and Discussion both claim "above
  10 kJ mol⁻¹" for the carbons; CA-4600 peaks at 9.5. True of CA-4700 and
  CA-4800 only.

**One trap worth recording for future extractions.** The abstract silently
switches samples: its gravimetric figures (8.1 / 7.0 / 8.9 wt%) are CA-4700, its
volumetric figures (44 / 48 g/L) are CA-4600, whose volumetric values are 37 and
41. An extractor keying on the abstract attributes 44 g/L to CA-4700.

**Text-layer hazard, new and severe.** This PDF replaces the hyphen with
**U+0002 (STX)** at hyphenated line breaks: `CA\x024600`, `CA\x02hydrochar`,
`micro\x02porous`. Searching the literal string `CA-4600` **silently misses
occurrences, including the sentence carrying its BET surface area.** Any verifier
keying on sample names in this paper will report false absences. Figure text
layers are also interleaved with body prose, so no value is readable from any
figure.

**Fields left deliberately empty.** `average_pore_diameter_nm` and
`pore_diameter_method` (finding 5 above). `uncertainty_wt_pct` on all 32: the
paper's only stated spread is "within ±5%" for *surface area and pore volume* on
repeated synthesis, which is a texture repeatability and not an uptake
uncertainty — putting it in `uncertainty_wt_pct` would be the right word on the
wrong quantity. `skeletal_density_g_cm3`: ρ_s appears only as a symbol in the
alternative packing-density relation, with no value. `external_surface_area_m2_g`
and `mesopore_volume_cm3_g`: obtainable only by subtracting the recorded
micropore values from the recorded totals, which the paper never prints.
`interlayer_spacing_nm`: the XRD feature at 2θ ≈ 22° belongs to the hydrochar,
which is not one of these samples. All texture on the six AX21 rows:
Supplementary Table 4, not obtained. `metal_*` and `residual_metal_*`: positively
supported as absent, XPS finding only C and O after the HCl wash.

**CA-hydrochar is deliberately not a row.** The main article gives it elemental
composition only, and no quantity the schema can hold, so a row would carry no
characterization at all.

**Tiering (§13).** 12 A / 17 B / 3 C. Assigned by `score_reproducibility` with
three recorded extractor adjustments:

- `calibration = 0` on all rows. The paper describes **no buoyancy or blank
  correction** — the dominant systematic for gravimetric H₂ at these capacities,
  and the subject of Broom & Hirscher, which the paper itself cites as ref 74.
  What it does describe is measuring a reference material (AX21) and comparing
  to published values, which is inter-laboratory agreement and is already scored
  under criterion 7 and §13.2's "Numerical" layer. Awarding criterion 6 for it
  would score one piece of evidence twice, and the tiering document's Tier A
  worked example explicitly includes "void-volume/blank correction", which this
  paper has no counterpart to.
- `chahine` capped at 1 at 1 bar. Blind spot 3: the BET/500 bound ignores
  pressure and is vacuous at 1 bar. Capped rather than zeroed, because the values
  are high and not impossible, and the paper says so itself.
- **A `total` row inherits the `chahine` score of the `excess` row at the same
  sample, temperature and pressure. This is a NEW blind spot**, never exercised
  because the corpus held zero `total` rows until now. Chahine bounds *adsorbed*
  uptake against surface area; a total legitimately exceeds it by the
  compressed-gas term. The scorer gave CA-4600's 5.6 wt% excess row `chahine` 1
  and its 6.2 wt% total row `chahine` 0, for one measurement expressed twice.

Differs from `suggest_tier` on 9 of 32 rows, each with its reason recorded.

**Two schema gaps this paper exposes, neither closed here:**

- **Oxygen content has no home.** The paper's independent variable is reported
  three ways that disagree — CHN bulk 22.8/17.9/20.6 wt%, XPS surface
  14.3/13.8/14.8, TPD 22.3/18.5/21.2 — and the disagreement is an explicit
  finding. It is not a dopant, so the dopant fields would be the field-meaning
  violation §3.2 warns about. **HYC-0031's central claim, that oxygen content
  raises uptake at matched porosity, is not queryable from the corpus.** A
  `heteroatom_element` + `heteroatom_content_wt_pct` + method triple would close
  it; `CompositionMethod` already exists to carry the bulk/surface split.
- **Isosteric heat has no field at all.** Eight main-text values with their
  coverages. This is the paper's third headline claim.

Also noted: `PoreDiameterMethod` has no `NLDFT` member although
`PoreVolumeMethod` does; and there is no field for a multimodal PSD.

**A live analysis hazard this append introduces.** HYC-0031 is the **first paper
in the corpus to report `uptake_type = total`**, and the first to carry paired
total/excess rows at the same sample, temperature and pressure — 13 such pairs.
Before this append, zero sample/T/P groups held more than one uptake type.
`uptake_type` appears **nowhere** in `plotting.py` or `clean.py`, and none of
§12.3's four filters excludes by it, so **any corpus-wide mean of
`uptake_wt_pct` now double-counts this paper's measurements.** Not yet guarded;
it needs a §12.3 filter and an enumerating invariant test, on the precedent of
the null-wt% rows already enumerated by `measurement_id` in
`tests/test_dataset_invariants.py`.

**A defect in this session's own append, caught by a test and not by the
tooling.** The staging file was written **CRLF** because the extractor had
carefully detected `references/paper_tracking.csv`'s format and then assumed
`data/raw/measurements_v0.1.csv` shared it. It does not — the dataset is **LF**.
`append_paper.py` reported "0 errors, 0 new warning types" and printed "Verify
merged file re-read from disk", because it checks cells and counts and **a
cell-level check cannot see a line ending**. The file was left with 228 LF lines
and 32 CRLF ones. Caught by
`test_migrate_relabel.py::test_running_the_migration_on_its_pre_image_reproduces_the_committed_file`,
whose byte-level replay is the only check in the suite that could see it. Fixed
by rewriting the appended rows to LF, verified by re-running that replay and by
asserting the committed prefix is byte-identical. **`append_paper.py` must learn
to refuse a staging file whose terminator differs from the dataset's**; until it
does, this recurs on any paper. This is the §6.7 failure class, committed by the
very session that had just written two byte-level migration scripts against it.

**A pre-existing defect found while amending the tests.** `dual_agent_papers()`
defines dual-agent completion by the `extractor` column, which says who produced
a row and not whether an independent verifier checked it. Against the
evidence-bearing `verified_by` column, **HYC-0007 and HYC-0024 are tracked
`verified` with no `verified_by` on any of their rows.** They were the §9.1
step-15 stragglers and `sync_paper_tracking.py` marked them verified from the
proxy. Recorded, not changed: whether their verification happened is a claim
about work done, not a test's call. Both tests now assert the honest
relationships and enumerate the gap by paper id, so a new unevidenced `verified`
fails.

**Validation.** Baseline 227 rows / 0 errors / 2 warning types
(`Unspecified uptake_type` 204, `Pre-2005 raw-CNT high uptake (Tier D)` 1).
After: 259 rows, 0 errors, same 2 types, `Unspecified uptake_type` 204 → 205 for
AX21's 1 bar row, whose uptake type the paper does not state. No
`--expect-new-warning` needed. Full suite 759 passed.

**Outcome.** 32 rows, 227 → 259, 23 → 24 papers. Tracked `extracted`, **not
`verified`**: the protocol ran and every dispute resolved, but two resolutions
turn on Supplementary Table 4 and Supplementary Fig. 11, which are not in the
obtained PDF, and `verified` would assert a completeness the record does not
have. Obtaining the Supplementary Information is a one-file fetch and would close
the AX21 temperature outright, its six rows' texture, and the −186 °C thread in
the Q_st method.

**New tooling.** `scripts/record_extraction.py` — the routine tool for §9.1 step
15, the step this project has skipped more than any other (ten consecutive
papers in Phase C, then HYC-0007 and HYC-0024 one commit after that was fixed).
Every previous repair was a one-off migration, and `sync_paper_tracking.py`
refuses to run twice by design, so after every extraction the project faced a
protected file, a routine update and no routine tool. It refuses a paper excluded
at screening, one whose `pdf_obtained` is not `yes`, one with no dataset rows,
and `verified` without a `--verified-by` record. 27 tests, 16 mutations run
against plan §6's twelve, all killed, with a passing control on the scratch tree.

**Where the pipeline was slow.** Row construction again, as the HYC-0007/0024
entry predicted — and the staging-helper it recommended was still not built, so
the same 67-column builder script was written from scratch. Building it now would
also be the natural place to put the terminator check §6.7 needs.

## 2026-10-02 — Phase D batch: HYC-0032, HYC-0033, HYC-0034, HYC-0037

**Pipeline.** Agent A (extraction) and Agent B (verification) were run as four
isolated pairs, one per paper, as concurrent Opus subagents; Agent B received only
the candidate rows (numeric, vocabulary and source-location cells), the PDF, and
`src/hycan/schema.py` — never Agent A's reasoning, notes, search keys or gap
analysis. The orchestrator (Claude Code) built the staging specs, ran
`build_staging.py` / `append_paper.py` / `record_extraction.py` /
`build_bibliography.py`, assigned the controlled vocabularies and tiers, and
adjudicated the one dispute from the primary source.

**Source acquisition.** All four PDFs were in the Claude Project, filename stem →
ID. The DOIs were resolved against OpenAlex during Phase D screening (2026-09-27,
all 35 confirmed); they were **not** re-resolved this session because OpenAlex was
unreachable from the container — `curl` 403s on CONNECT at the egress proxy and
`WebFetch` is gated behind an interactive approval that no one was present to
grant. Two consequences, both recorded below: the published-correction check was
done by reading each PDF rather than by a Crossref/OpenAlex pass, and three issue
numbers are unresolved in the bibliography.

**Correction/retraction check.** Agent A read each PDF for a printed correction,
erratum, corrigendum, retraction or expression-of-concern notice. **None found in
any of the four** (HYC-0032 carries only a routine "Check for updates" badge). The
corpus-wide raw-JSON Crossref pass §6.9 owes is still owed and now also wants the
three issue numbers; it needs network access this session did not have.

**Extraction and verification, per paper.** Across all four, **every numeric cell
agreed** under independent verification — the protocol's measured pattern.

- **HYC-0032** (Anuchitsakol 2023, *RSC Adv.* 13, 36009–36022), 10 rows, Tier B.
  Five present-work samples (3 O/N co-doped `doped_carbon`, 2 unmodified
  `activated_carbon`) × 77 K and 298 K at 1 bar, all from Table 1. Agent B: 178
  cells, all numeric and vocabulary cells agreed. **One dispute upheld:** the
  KOH:char mass ratio was written 1:2 in the three N-AC synthesis descriptions;
  Agent B read the paper as 2:1. Adjudicated against the primary source — §2.1.1,
  "a weight ratio of 1 g sample per 2 g KOH" = 2 g KOH per 1 g char — Agent B was
  right; corrected in six descriptive cells. One vocabulary dispute **dismissed:**
  Agent B recommended `pore_volume_method = other` for the single-point total pore
  volume; kept `unspecified` to match the 31 existing corpus rows that record a
  single-point total that way (a Gurvich reading applies no pore-size model), with
  the single-point basis in `notes`. Table 1 is a mixed table; only the five
  present-work rows were extracted, the rest being other authors' literature
  (column "Year/ref."). The GCMC study (Figs 11–14) is of idealised slit-pore
  models and no simulated value was recorded.

- **HYC-0033** (Romanos 2019, *Sci. Rep.* 9:2971), 2 rows, Tier C,
  **characterization-only.** Agent B: 44 cells, 0 disputes, and independently
  confirmed the decision: the paper reports hydrogen uptake only in Figs 4–5 with
  no value in any table or in the text, so it is figure-only **and unanchorable** —
  §3.4 step 6 cannot be satisfied because there is no text value for a digitised
  series to reproduce. Two BET rows recorded (3300 non-irradiated / 3100
  irradiated m²/g, both rounded to the nearest hundred by the authors). Boron
  content 1.4 wt% (PGNAA → `dopant_concentration_method = other`) is stated only
  for the "resulting" post-etch sample, so it is on the irradiated row and null on
  the non-irradiated one. Skeletal density 2.0 g/cm³ is **assumed**, not measured,
  and was not recorded. `measurement_method = not_applicable` on both rows.

- **HYC-0034** (Wang 2016, *IJHE* 41, 8489–8497), 14 rows, Tier B. Seven samples
  (6 N-doped `doped_carbon` + 1 nitrogen-free `activated_carbon` reference) × 77 K
  at 1 and 20 bar, all from Table 1. Agent B: 262 cells, 0 disputes — it
  re-transcribed Table 1 independently with no swaps between the headline BET /
  t-plot-micropore columns and confirmed the single-point vs t-plot pore-volume
  split. The hydrochar precursor **HC** was correctly excluded (N content only, no
  area/uptake). The abstract states SBET / pore-volume / N ranges that differ
  slightly from Table 1 (e.g. SBET 1362–3009 vs 1394–2919; the body also carries
  PC's total pore volume over from PC-2-600); Table 1 was used throughout (§3.7),
  with the discrepancy noted.

- **HYC-0037** (Chen 2013, *IJHE* 38, 3297–3303), 3 rows, Tier B,
  **low-uptake (bias guard, §7.4).** One N-doped nanotube sample: 0.21 wt%
  (1 bar/77 K), 1.21 wt% (7 bar/77 K), 0.17 wt% (19 bar/298 K), all in Table 1 and
  the text. Agent B: 53 cells, 0 numeric disputes. `uptake_type` split confirmed
  by the exact-word rule: `unspecified` for the 1 bar/77 K value (Fig 5a, not
  labelled excess) and `excess` for the 7 bar/77 K (Fig 5b) and 298 K (Fig 5c)
  isotherms. `measurement_method` split confirmed: volumetric Sieverts (ASAP
  2020HD88) for the 1 bar value, gravimetric microbalance (IGA, Hiden) for the
  other two. Table 1 is a literature-summary table; only column 1 ("this work")
  was extracted. `residual_metal_element = Fe` from the FeCl₃ catalyst, not
  quantified. `material_class = MWCNT`: the paper says "nitrogen-doped carbon
  nanotubes" with a 10–20 nm wall thickness, which is multi-walled, and the corpus
  files doped nanotubes by structural class (cf. HYC-0025, a boron-doped MWCNT).

**Decisions and their basis.** `material_class`: doped activated carbons →
`doped_carbon` (cf. HYC-0021, HYC-0026); doped nanotubes → their structural class
(HYC-0037 → MWCNT, cf. HYC-0025); unmodified base carbons → `activated_carbon`
with no `dopant_element` (their incidental biomass N/O is not a deliberate doping
step — the oxygen-is-not-a-dopant convention, extended to incidental heteroatoms).
`pore_volume_method = unspecified` for a single-point total pore volume (31-row
precedent). Tiers were assigned from `score_reproducibility` with two documented
hand-adjustments, both §5 blind spots: **HYC-0032-M9** (scorer C → B — the 1.78
wt% at 1 bar exceeds the pressure-blind BET/500 Chahine bound, which is a
saturation rule that does not apply at 1 bar; the value is within physical bounds)
and **HYC-0037-M3** (scorer A → B — the residual Fe is unquantified and the paper
credits it for part of the uptake, so the sample is not anchor-quality). Every
other tier matches the scorer.

**Fields left deliberately empty.** HYC-0033's uptake (figure-only, unanchorable)
and its assumed skeletal density; the non-irradiated row's boron concentration
(the paper states it only for the post-etch sample); `average_pore_diameter_nm` on
HYC-0032 and HYC-0034 (the papers report multiple NLDFT PSD maxima, not a single
average) and HYC-0037 (method stated, no value); the oxygen content of HYC-0032's
co-doped samples (the schema holds one dopant; O is in the description and
`functional_groups`); HYC-0034's N/C ratio (no field).

**Premise correction — HYC-0038 (Firlej 2021, *Nanomaterials* 11, 2173).** Screened
in with the caveat "confirm experimental data present, exclude if simulation-only."
On reading, the only experimental hydrogen result is an adsorption **energy**
(~9 kJ/mol, which has no schema field) and a figure-only amount-adsorbed axis with
no stated pressure; every uptake isotherm in the paper is GCMC-simulated. The
physical boron carbons are real (¹¹B/¹³C NMR, 5/11/19/23 wt% B), so the common
"boron is simulation-only" trap does not apply — but there is no storable
experimental (T, P, uptake) measurement. **Recommended EXCLUDE**, pending whether
the Supplementary Information or a companion experimental dataset can be obtained;
not yet actioned (a screening reversal is a protected-file migration + a §7.5
PRISMA line). It yielded no rows and is left `include` / `not_started`.

**Source anomalies.** HYC-0032's inverted KOH ratio (our error, caught by Agent
B). HYC-0034's abstract/Table-1 range mismatch and PC total-pore-volume carryover.
HYC-0037 prints "Hidden Isochem" for Hiden and "10⁻⁶ mbar" as "106 mbar" in the
text layer. HYC-0033 omits the non-irradiated binding-energy value in the printed
article itself.

**Schema and methodology notes.** No new blocking gap. The known limitations these
papers touch are already recorded: `PoreDiameterMethod` has no `NLDFT` member
(HYC-0032/0034 PSDs), and the schema holds one dopant where HYC-0032 is O/N
co-doped.

**Validation.** Baseline 259 rows / 0 errors / 2 warning types
(`Unspecified uptake_type` 205, `Pre-2005 raw-CNT high uptake (Tier D)` 1). After
the four appends: 288 rows, 0 errors, same 2 types, `Unspecified uptake_type`
205 → 232 (+27; HYC-0037's two `excess` rows correctly do not count). No new
warning type, so no `--expect-new-warning`. Full suite **805 passed**.

**Migration — `migrate_relabel` post-condition scoped to a delta.** HYC-0032's two
CO2-activated base carbons are legitimately `physical_activation`, and the
historical relabel migration asserted a global absolute count for that value
(0 before, 2 after), which four of its own tests then failed against the larger
dataset. Per §6.7 ("pin deltas and partitions, not absolute totals; a
post-condition that a later append invalidates was never testing this migration")
the redundant absolute check was removed — the `+2` delta is already verified by
the `EXPECTED_SYNTHESIS_DELTAS` check, and post-condition 4 already pins the exact
36 relabelled cells. The physical_activation test was scoped from a global
equality to a subset. No dataset cell changed; the relabel output is byte-identical
(the round-trip test proves it). Two mutations confirm the scoped guards still
catch a bad relabel: corrupting a relabel target is caught by the delta check
(+35 vs +34), and dropping a mapped row by the changed-cell-count check (69 vs 70).
`docs/migration_relabel_test_scope_plan.md`.

**Pinned tests updated, deliberately.** `test_bibliography` pdf_held 24 → 28 and
the issue-number `none` partition 7 → 11; `test_validate` scorer-vs-human
agreement 164 → 191 (+27 agreements, 2 disagreements = the two hand-adjustments
above) and the Chahine `not_applicable_no_uptake` partition 12 → 14 (HYC-0033's two
rows); `test_dataset_invariants` the no-uptake enumeration (+HYC-0033-M1/M2) and
the `dopant_concentration_wt_pct` paper set (+HYC-0032/0033/0034).

**Bibliography.** Four entries added, all PDF-sourced for authors/title/
journal/volume/pages/year (pdf_held 28). HYC-0033 is a genuine `none` (Scientific
Reports is article-numbered). HYC-0032/0034/0037 print no issue on the article and
OpenAlex was unreachable, so their issue is omitted with a disclosing note and
will move to `openalex` once retrievable.

**Outcome.** 29 rows (10 + 2 + 14 + 3), 259 → 288, 24 → 28 papers. All four tracked
`verified`, with the dispute record in `verified_by` on every row — the first
Phase D papers to carry it. The 77 K BET modelling subset the gate in §14.1 turns
on gained **3 groups (11 → 14)** — HYC-0032/0034/0037, all doped carbons —
directly against the "more groups, not more rows" target; HYC-0033 is
characterization-only and does not enter it. Tier distribution 48 A / 187 B /
43 C / 10 D.

**Where the pipeline was slow.** The OpenAlex egress gate. The issue-number
resolution and the corpus-wide retraction pass both need `works/doi:`, which this
session could not reach; a session with that access should backfill the three
issue numbers and run the owed Crossref/OpenAlex pass in one go.

## 2026-10-02 (continued) — Phase D batch: HYC-0039–0043, and HYC-0038 excluded

**Scope.** Five papers extracted under the dual-agent protocol (§3.2) and one
excluded at full-text review, continuing §9.1 in `paper_id` order after the
morning's HYC-0032/0033/0034/0037 batch.

**Method.** The extractor read all six PDFs in full (via `project_read`) and
assembled candidate rows; five isolated Agent B subagents (sonnet) then verified
each paper independently, each given only the candidate values (my notes and
reasoning stripped), the PDF (read independently), and `schema.py`. The extractor
adjudicated the disputes as Agent C. Agent A and Agent B passes were fanned out
concurrently.

**Verification outcome — 0 numeric disputes across all five papers.** Every
uptake, surface area, pore volume, dopant/metal loading, temperature and pressure
transcription was confirmed against the primary source (Agent B checked ~536 /
144 / 279 / ~60 / ~60 cells for 0039 / 0040 / 0041 / 0042 / 0043). Every dispute
raised was field-semantics or provenance, not a wrong number. The adjudications:

- **HYC-0039** (Aboud 2021, 14 samples × 2 = 28 rows; metal-decorated/ammonia-treated
  Norit AC). Metal-decorated samples are `composite` with `metal_element` (HYC-0027/0029
  convention); the ammonia-treated base is `doped_carbon`. Agent B caught an **inherited
  N concentration**: 2.0 wt% N was measured on the ammonia-treated support only, so it
  was nulled on the six metal+NH3 composites (kept on S2), `dopant_element=N` retained —
  the HYC-0027-M3 "a presumption is not a measurement" precedent. A **calibration point**
  was added by hand for the He skeletal-density void-volume correction (tiering doc l.24),
  lifting the 14 cryogenic rows C→B. Metal impregnation removed from `activation_method`
  (not a pore activation). No surface area is reported in this paper for any sample
  (`surface_area_method=none`; the textural data are approximate and in ref 90).
- **HYC-0040** (Flamina 2023, rGO/B-rGO/Ni-B-rGO, 3 × 3 = 9 rows). B-rGO kept
  `reduced_graphene_oxide` + `dopant_element=B` (structure-preserving: HYC-0013's
  Fe-decorated graphene stays graphene, and the doped-nanotube rule; HYC-0027's
  N-graphene→doped_carbon noted as the competing precedent). Ni-B-rGO is `composite`
  (Ni is catalytic-only per the paper, so `metal_element`). **Physics override:** the
  three 77 K uptakes (9.8 / 8.2 / 6.9 wt% on ~900 m²/g, 4–5.5× the Chahine bound and
  above record carbons) are Tier D (tiering doc l.33); the plausible 273/298 K rows are
  B with a calibration point (LaNi5/basolite reference calibration). The paper's wt%
  basis (m_H2/(m_sample+m_H2)) differs from the corpus dry-sample basis; recorded as
  reported with a disclosing note (§3.9). The recalculated/DFT/literature values are
  excluded; rGO at 298 K is a tabulated 0 (exact, noted as "negligible").
- **HYC-0041** (Morande 2023, commercial Haycarb AC + N/B, 13 rows). 0 disputes of any
  kind. `dopant_element="B, N"` for the two co-doped samples (the schema's one-dopant
  field; comma-space delimiter; endorsed by Agent B as the first multi-element value, no
  code filters it). DR micropore V0 and by-difference mesopore Vm recorded with a note;
  the MDA-extrapolated Table 6 values excluded. `source_location` cites Table 2 only for
  the seven XPS samples.
- **HYC-0042** (Molefe 2019, ZTC + MOF/polymer composites, 3 rows). Scope: only the ZTC
  and the two ZTC-containing composites (carbon present) are in; pristine UiO-66 (MOF),
  PIM-1 (polymer) and PIM-1/UiO-66 (no carbon) are out. Composite `synthesis_method`
  set to `template_synthesis` (the carbon component's route, per all 15 existing composite
  rows); `pore_volume_method` `HK`→`unspecified` (single-point total at p/p0~0.99 per
  footnote d); the ZTC HF/HCl purification propagated to the composites. Estimated
  (mass-weighted) columns excluded.
- **HYC-0043** (Ma 2019, wood-charcoal AC hollow fibers, 2 rows). Only WC-ACHF-1.0% is
  text-anchored; the other four samples are figure-only and unanchorable (§3.4 step 6).
  298 K in the conclusion is a typo for 77 K (four other locations). **Agent B digitized
  Fig 4b** and found the excess maximum near ~25–30 bar with the ~100-bar point lower, so
  the 100-bar/4.51 wt% row was downgraded to Tier C (confidence 4): the paper states the
  pairing but it reflects the run window, not the peak pressure. N/P are incidental
  (precursor-derived), so `dopant_element` is empty; `functional_groups` unit corrected to
  at.% (Fig 2a).

**HYC-0038 excluded** (Firlej 2021). Full-text review: all uptake isotherms are
GCMC-simulated and the only experimental hydrogen result is an adsorption energy
(no anchored (T, P, uptake)), so no row is extractable. `screening_decision=exclude`,
`exclusion_reason=no_experimental_uptake`, applied by
`scripts/migrate_exclude_hyc0038.py` (one row, three cells, rest byte-identical) under
`docs/migration_exclude_hyc0038_plan.md`; the citation is kept for PRISMA and the §7.5
line added to `docs/phase_d_screening_log.md` §5.2. Ratified by Avin.

**A second `migrate_relabel` absolute pin, same §6.7 fix.** Post-condition 7 asserted
`eligible == set(PD_ROWS)` — that HYC-0027's three Pd rows were the *only* metal-loading
rows surviving the §12.3 filters. HYC-0039's 24 metal-loading rows legitimately break
that; scoped to a subset (`set(PD_ROWS) <= eligible`), its test relaxed likewise, the
delta check untouched. No dataset cell changed; the relabel output is byte-identical.
`docs/migration_relabel_test_scope_plan.md` addendum. Mutation-checked: dropping the
backfill still fails both the post-condition and the test.

**Pinned tests updated, deliberately.** `test_bibliography` pdf_held 28→34, issue `none`
partition 11→16, issue `pdf` partition +HYC-0043, excluded list +HYC-0038. `test_validate`
scorer-vs-human agreement 191→224 (+33 agreements, 22 documented hand-adjustments: the
HYC-0039 calibration lifts, the HYC-0040 physics override and calibration lifts, and the
HYC-0043-M2 pressure downgrade). `test_dataset_invariants` `dopant_concentration_wt_pct`
paper set +HYC-0039. `test_migrate_relabel` metal-loading eligibility `==`→`<=`.

**Outcome.** 55 rows (28 + 9 + 13 + 3 + 2), **288 → 343, 28 → 33 papers**, 0 errors, no
new warning type. All five `verified` with the dispute record in `verified_by` on every
row. Tier distribution across the batch: 51 B, 1 C, 3 D (the HYC-0040 77 K over-claims).
The 77 K + BET modelling subset gains HYC-0041 (13), HYC-0042 (3) and HYC-0043 (2) and
rGO's 77 K row from HYC-0040 — more real doped/templated/commercial-AC groups against
the "more groups, not more rows" target; HYC-0039 (no BET) does not enter it. Bibliography
35 → 41 entries. 805 tests passing.

**Where the pipeline was slow.** OpenAlex remained unreachable, so the three owed issue
numbers (HYC-0032/0034/0037), HYC-0043's would-be corroboration, and the corpus-wide
retraction pass are still owed to a session with `works/doi:` access. Per-PDF correction
checks found none in the six papers read.

## 2026-10-02 (continued) — Phase D batch: HYC-0044–0048

**Models.** Agent A (extraction/adjudication) Opus; Agent B (independent verification)
five parallel Sonnet subagents, one per paper, each re-reading the PDF via the project
store with no sight of Agent A's reasoning.

**Batch.** HYC-0044 (Hwang 2021, PVA/PAN carbon fibers + Pd), HYC-0045 (Masika 2013,
zeolite-13X ZTC), HYC-0046 (Kabbour 2006, activated carbon aerogels + Ni/Co), HYC-0047
(Fierro 2010, anthracite ACs, three labs/devices), HYC-0048 (Kahilu 2023, HTC coal/sewage
ACs). 48 rows, `288`-style append 343 → 391, 33 → 38 papers, 0 errors, no new warning type.
Tiers 38 A / 19 B / 5 C.

**Agent B found 0 numeric transcription disputes in all five papers.** Every uptake, BET
area, pore volume, T and P confirmed against the primary source. What it caught was a
**unit error**, not a value error: HYC-0047's pressures were stored as the MPa magnitude
(5, 4) rather than bar (50, 40). Fixed on all rows. The other adjudications were
field-semantics: HYC-0044's Waverage is Saito-Foley, not the HK used for its micropore
volume → `pore_diameter_method=other`; HYC-0047's L0 is Stoeckli's exact
L0=10.8/(E0−11.4) → `stoeckli_L0` (not HYC-0024's DR-characteristic-energy slit width);
HYC-0048's average pore diameter is irreconcilable across Tables 4/6/8 and AC-HCB's
Table-6 value does not reproduce from its own area and volume, so the field was dropped.

**The one modelling reversal.** HYC-0047 was first extracted as one row per lab × device ×
condition (32 rows). That broke `test_plotting`'s pinned invariant that no sample/T/P is
plotted twice at 77 K — the two 77 K devices (ICMPE volumetric, ICB gravimetric) double-
counted each material in the Chahine subset. The corpus is designed around one excess
point per (sample, T, P); the multi-lab values are provenance, not separate rows. Re-cut
to 18 rows (ICMPE recorded, the IJL/ICB values in `source_location`). The dataset was
`git checkout`-reverted to 343 and all five re-appended with the corrected HYC-0047 — the
documented recovery pattern; the first three appends reproduced byte-identical shas.

**Classification precedents checked against the corpus, not assumed.** Non-activated
carbon fibre → `other` and activated carbon fibre → `activated_carbon` (HYC-0024, the
corpus's one prior fibre paper). Every metal-bearing carbon in the corpus is `composite`
(HYC-0027/0029/0039/0040), so Pd/APCF, Ni-CA and Co-CA follow; `carbon_aerogel` is a new
class (HYC-0046 its first rows). Characterization-only rows (HYC-0044's five PCF process
samples) follow HYC-0007: table-complete texture → Tier B by hand.

**Bibliography.** 41 → 46 entries, appended by a full `ensure_ascii=False` re-dump that
reproduced every existing entry byte-for-byte (verified before writing). HYC-0046 is the
awkward one: its held PDF is the LLNL preprint with no volume/issue/pages/year, so those
were read from the reference lists of two held PDFs that cite it (HYC-0047 ref [42] prints
`18(26):6085-7`; HYC-0044 ref [17]) and the Caltech DOI record — a new `citing_pdf`
provenance value, because OpenAlex, Semantic Scholar and Crossref were all 403 at the
egress proxy this session.

**Pinned tests updated, deliberately.** `test_bibliography` pdf_held 34→39, issue `none`
16→19, issue `pdf` +HYC-0045, allowed-provenance +`citing_pdf`. `test_validate`
agreement 224→257 (+33 agreements, 15 hand-adjustments), Chahine no-uptake 14→19.
`test_dataset_invariants` no-uptake +HYC-0044-M8…M12, flag papers +HYC-0046, total/excess
pairs +HYC-0045-M1/M6. `migrate_relabel` post-condition 6 (the carbonization survivor set)
de-pinned from an absolute inventory to the migration's delta — the third §6.7 fix of this
kind — because HYC-0044's carbon fibres are legitimately `carbonization`. 805 tests passing.

**Still owed.** The OpenAlex backfill now owes three more issue numbers (HYC-0044/0047/0048)
and a re-confirmation of HYC-0046's citation, plus the standing corpus-wide retraction pass
— all blocked on `works/doi:` egress. Agent B found no correction/retraction notice in any
of the five PDFs read.
