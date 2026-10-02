# Migration: exclude HYC-0038 at full-text review

**Date:** 2026-10-02
**Scope:** one row of the protected file `references/paper_tracking.csv`; one PRISMA
line in `docs/phase_d_screening_log.md`; one citation added to
`references/bibliography_sources.json` (kept, per §7.5, because PRISMA needs it).

## Decision

HYC-0038 (Firlej et al. 2021, *Nanomaterials* 11, 2173, "Hydrogen Storage in Pure
and Boron-Substituted Nanoporous Carbons—Numerical and Experimental Perspective")
was screened **in** at title/abstract (funnel `doped_77K`) and its full text was
obtained. On full-text review it yields **no extractable experimental (T, P,
uptake) measurement**:

- The paper is a review plus a Grand Canonical Monte Carlo (GCMC) study. Every
  hydrogen **uptake isotherm** (gravimetric/volumetric capacity vs pressure,
  Figures 1, 2d, 4a, 5c, 7c) is **simulated**, not measured.
- The only **experimental** hydrogen result is an **adsorption energy**
  (~9 kJ/mol, Figure 6d), derived from a pair of low-pressure isotherms at 77 K
  and 87 K via Clausius–Clapeyron. Figure 6d plots adsorption energy against
  gravimetric storage with **no pressure axis**, so no anchored (temperature,
  pressure, uptake) triple exists in the text or any table.

Per manual §7.2 ("Exclude only when the *value* cannot be determined") the paper
is excluded: no uptake value at stated conditions can be recorded. The boron
carbons are physically real (NMR-confirmed), so the Supplementary Information or a
companion experimental dataset could rescue it later; the exclusion is recorded as
a full-text-review decision, not a permanent eligibility judgement, and the
citation is kept.

Ratified by Avin ("go with your recommendations", 2026-10-02).

## Changes

1. `references/paper_tracking.csv`, the HYC-0038 row only, byte-preserving every
   other line (the file is CRLF):
   - `screening_decision`: `include` -> `exclude`
   - `exclusion_reason`: (empty) -> `no_experimental_uptake`
   - `notes`: append the full-text-review record.
   `extraction_status` stays `not_started` (the paper yielded no rows).
2. `docs/phase_d_screening_log.md`: a new "Excluded at full-text review (1)"
   section and a PRISMA line, so the funnel distinguishes a full-text exclusion
   from the 14 title/abstract exclusions and the 5 retrieval failures.
3. `references/bibliography_sources.json`: a `screening_decision = exclude`,
   `in_corpus = false`, `pdf_held = true` entry (spliced, not re-dumped).
4. `tests/test_bibliography.py`: the excluded-list, `pdf_held` and issue-partition
   pins updated for this entry and the five included Phase D papers of the same batch.

## Verification

`migrate_exclude_hyc0038.py` re-reads the tracking file and asserts: exactly the
HYC-0038 row changed, the three named cells hold the new values, and every other
line is byte-identical. Then the full test suite.
