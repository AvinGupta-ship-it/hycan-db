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