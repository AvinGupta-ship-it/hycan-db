# PRISMA 2020 checklist — HyCAN-DB v1.0

Page et al., BMJ 372 (2021) n71. "Manuscript §" refers to
`manuscript/v1/manuscript_v1.md`; file paths are repository paths. This
study synthesizes published physical measurements rather than clinical
trials, so the bias and certainty items are met by their registered
measurement-literature counterparts, named explicitly below.

| # | Item | Where addressed |
|---|---|---|
| 1 | Title identifies the report as a systematic synthesis | Manuscript title ("registered, design-based synthesis") |
| 2 | Abstract | Manuscript abstract (background, methods, results incl. both RQ1 statements, limitations, registration) |
| 3 | Rationale | Manuscript §1 |
| 4 | Objectives | Manuscript §1 and §2.5; research questions RQ1–RQ5, protocol §2 |
| 5 | Eligibility criteria | Protocol §4 (summarized Manuscript §2.1); full-text decisions in `references/v1_fulltext/eligibility.csv` |
| 6 | Information sources | Manuscript §2.1: OpenAlex and Semantic Scholar, with harvest dates and raw responses in `references/v1_search/` |
| 7 | Search strategy | Registered queries, protocol §5; exact requests archived in `references/v1_search/` |
| 8 | Selection process | Manuscript §2.1: two independent agents per record, registered tiebreak, author audit sheet (`references/v1_screening/`) |
| 9 | Data collection process | Manuscript §2.2: independent dual extraction, reconciliation by a third agent, agreement statistics (Table 3; `references/v1_extraction/`) |
| 10 | Data items | Schema and data dictionary (`src/hycan/schema.py`, `docs/data_dictionary.md`); computed fields, protocol §10 |
| 11 | Risk-of-bias assessment of included studies | Per-row reporting items, score and tier (protocol §10.1), §10.2 plausibility screen, and the RQ4 reporting-practice survey (Manuscript §3.6) |
| 12 | Effect measures | Ratio of n_ex,max to A_BET/500 with the registered ±15% equivalence margin; slopes and CVs as defined in protocol §11 |
| 13 | Synthesis methods | Manuscript §2.5 and protocol §11: unit-of-analysis rules, mixed models, bootstrap, design weights; eligibility ladder in Table 5 |
| 14 | Reporting-bias assessment | Protocol §14: no small-study tests (per-value variances unavailable); S1 vs S2 and sensitivity (iii) reported as the available selection checks (Tables 6, 10) |
| 15 | Certainty assessment | Registered decision rule with equivalence margin, 13 sensitivity analyses, robustness rule carried to the abstract (Manuscript §3.3) |
| 16 | Study selection (results) | Figure 1 (`references/v1_prisma/prisma_flow`) and Table 1; per-record outcomes in `references/v1_fulltext/` |
| 17 | Study characteristics | Table 2; per-paper records in `references/v1_extraction/papers.csv`; the dataset itself |
| 18 | Risk of bias within studies (results) | Reporting-tier distribution (Table 2), flagged rows, RQ4 estimates (Table 10) |
| 19 | Results of individual studies | The released row-level dataset with provenance (`data/`), one row per reported measurement |
| 20 | Results of syntheses | Manuscript §3.3–§3.7, Tables 5–11, Figures 2–7 |
| 21 | Reporting biases (results) | Manuscript §3.6 and the S1/S2 contrast; sensitivity (iii) |
| 22 | Certainty of evidence (results) | Sensitivity table (Table 6) with the two inconclusive variants stated; prediction interval reported beside the mean |
| 23 | Discussion | Manuscript §4–§6 (findings, strengths, limitations, implications) |
| 24a | Registration | Zenodo 10.5281/zenodo.23719010, 2026-10-28; `docs/v1_registration.md` |
| 24b | Protocol access | `docs/v1_protocol.md` (archived in the registration record with hashes) |
| 24c | Amendments | Protocol §15 (Amendments 1–2) and deviation D1; Manuscript §7 table |
| 25 | Support | *(Author to complete.)* |
| 26 | Competing interests | *(Author to complete.)* |
| 27 | Availability of data, code and other materials | Manuscript §8; repository and Zenodo archive at release |
