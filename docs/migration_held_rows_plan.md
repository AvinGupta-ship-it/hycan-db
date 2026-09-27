# Plan — write the last two held rows, and backfill two spacings

**Status:** written and committed before any protected file is touched, per §6.7.
**Date:** 2026-09-27
**Applied by:** `scripts/append_paper.py` for the two new rows;
`scripts/backfill_interlayer_spacing.py` for the two cells on existing rows.
**Target file:** `data/raw/measurements_v0.1.csv`. 225 → 227 rows, 67 columns
unchanged.

---

## 0. Why these two rows and not others

These are the last rows held out of the corpus, and **their blocker was removed a
commit ago and nobody wrote them.** Schema v1.3 added `areal_uptake_g_cm2` for
HYC-0011's FePc film and `interlayer_spacing_nm` for HYC-0015's pristine graphite
(§8.8 gap 10), and both fields still have **zero rows**. A field added to admit a
row and then left empty is a gap that looks closed, which is why this is Phase C.1
item 6 rather than nothing.

Extracted by Agent A, verified by Agent B under §3.2 with the PDFs, the candidate
rows and `src/hycan/schema.py` and nothing else. **61 cells verified, 2 disputed,
both upheld** (§4).

## 1. Row 1 — HYC-0011-M5, the FePc film's areal uptake

| field | value |
|---|---|
| `sample_id` / `measurement_id` | `HYC-0011-S3` / `HYC-0011-M5` |
| `material_class` | `MWCNT` |
| `synthesis_method` | `pyrolysis` |
| `areal_uptake_g_cm2` | `2.5e-05` |
| `temperature_unstated` / `pressure_unstated` | `True` / `True` |
| `surface_area_method` | `none` |
| `measurement_method` | `volumetric_sieverts` |
| `extraction_confidence` / `reproducibility_tier` | `3` / `D` |

The paper's third sample, distinct from the two already recorded: *"Sample 3 is
formed by the thermal decomposition of FeC32N8H16 (FePc) which is either carbon
source or catalyst required for the CNTs growth in the reactor"*, and structurally
*"relatively dense and well-aligned MWNTs nearly normal to Si substrate"* against
sample 2's *"coiled and tangled MWNTs grown randomly"*. Its uptake is reported
**only** per unit area: *"The measured H2 uptake per unit area of the film is
2.5 × 10⁻⁵ g/cm², which is about four times as large as that of sample 2."*

**The exponent is the one cell that could quietly be wrong, and it is fixed three
ways.** This PDF's text layer deletes superscript minus signs elsewhere, so the
glyph alone is not enough. (i) The extraction retains a U+2212 in both `10−5` here
and `10−6` for sample 2. (ii) **The paper's own comparison settles it**: 2.5e−5 /
6.3e−6 = 3.97, "about four times"; +5 gives 4 × 10¹⁰, −3 gives 397, −7 gives
0.0397. (iii) Physical sanity: 2.5e−5 g/cm² is 0.025 mg H₂/cm² against a carbon
loading of 0.5–0.75 mg/cm² from the paper's own 9.0 mg film over 12–18 cm² — a few
per cent, which is sane. 2.5 × 10⁺⁵ g/cm² would be 2.5 tonnes of hydrogen per
square centimetre.

**Why no mass, area, temperature or pressure.** The film was never weighed, which
is exactly why the paper reports an areal quantity and can only "deduce" that its
wt% "would be remarkable" — and why gap 10 was needed to record it at all. The
paper prints two film areas, *"(3 × 4 cm²; 4.5 × 4 cm²)"*, **for the two films
jointly and never says which is which**, so no area is recorded and the areal
value cannot be converted to a mass. Room temperature is asserted for the
experiments collectively and in the title and abstract but **never numerically**,
and the 353 K in the protocol is a pre-measurement degassing temperature; the
pressure for this sample is given only as *"above 1 atm"*. Both `*_unstated` flags
are therefore set, matching all four sibling rows.

**`synthesis_method = pyrolysis`, and the paper distinguishes it from CVD.** Its
own taxonomy is *"arc discharge method (sample 1), CVD method (sample 2) and
catalytic decomposition (sample 3)"*, so `cvd` would contradict a distinction the
paper draws itself. `pyrolysis` is supported by the paper's own words — "formed by
the thermal decomposition of" — and is the closest value in the vocabulary, which
has no `catalytic_decomposition`. Agent B agreed after reading the `Literal` list.

**Tier D by judgment, not by the scorer.** `score_reproducibility` totals 3 and
suggests C. The row has no surface area, no stated temperature, no stated
pressure, no mass, no purity and no calibration, and its single value cannot be
converted or compared to anything in the corpus. Its sibling film row is D. This
is the §13.7 blind spot the scorer still has for a row whose uptake is
non-gravimetric — it scores the Chahine criterion "cannot assess" and keeps the
point.

## 2. Row 2 — HYC-0015-M3, the pristine graphite's interlayer spacing

| field | value |
|---|---|
| `sample_id` / `measurement_id` | `HYC-0015-S3` / `HYC-0015-M3` |
| `material_class` | `other` |
| `synthesis_method` | `commercial` |
| `interlayer_spacing_nm` | `0.339` |
| `measurement_method` | `not_applicable` |
| conditions | all null, no flags — a characterization-only row |
| `extraction_confidence` / `reproducibility_tier` | `4` / `D` |

*"Most intense peak in the pristine graphite is appearing at 2θ = 26.32° which is
corresponding to (002) plane of graphite and interlayer spacing is about to
3.39 Å."* 3.39 Å = 0.339 nm.

**The paper prints 3.39, not the textbook 3.35, and this is the cell most at risk
of being silently "corrected".** Both agents were told not to supply graphite's
commonly quoted spacing and neither did. Agent B added an independent arithmetic
check: Bragg on the paper's own 2θ with the paper's own stated Cu Kα source gives
d = 1.5406 / (2 sin 13.16°) = 3.383 Å, which rounds to the printed 3.39. Of the
paper's four d-spacings it is the only one that closes tightly, which is evidence
the digit is not mangled.

**No hydrogen uptake is reported for the graphite, confirmed twice.** The paper
measures GO (1.90 wt%) and rGO (1.34 wt%) only; Fig. 8's caption names two
samples; the hydrogen-storage section degasses and measures "the GO and rGO
samples". The graphite appears only as the synthesis starting material and in the
Fig. 4 XRD. So the row is legitimately characterization-only and **no uptake field
is populated** — which is what makes it the first row in the corpus to be carried
by `interlayer_spacing_nm` alone.

## 3. Two cells backfilled on rows already in the corpus

| row | field | current | new |
|---|---|---|---|
| HYC-0015-M1 (graphene oxide) | `interlayer_spacing_nm` | null | `0.884` |
| HYC-0015-M2 (reduced graphene oxide) | `interlayer_spacing_nm` | null | `0.385` |

**Both numbers are already in the corpus, as prose.** M1's
`material_description` reads "XRD (002) at 9.96 deg, interlayer spacing 8.84 A"
and M2's reads "XRD broad peak at 23.72 deg, interlayer spacing 3.85 A". v1.3
added the numeric field and did not backfill the two rows that could already fill
it.

**This is not optional tidying.** Writing 0.339 on the graphite while leaving the
GO and rGO null would make `interlayer_spacing_nm` mean "graphite only" — a reader
filtering on it would conclude this paper measured no other spacing, when the
paper's entire thesis is the collapse from 8.84 Å to 3.85 Å on reduction. Both
values were re-verified against the PDF by Agent B rather than copied from the
prose.

**One inconsistency in the paper travels with M2.** The sentence assigning 3.85 Å
says *"After the chemical reduction by hydrogen"*, while the Experimental section
says the reductant was hydrazine hydrate and no hydrogen gas is involved in making
rGO. Agent B upheld the assignment to rGO on four grounds: Fig. 5's caption names
exactly three patterns and the prose assigns exactly three peaks, with the third
(12.20°) named explicitly as the hydrogenated GO, so 23.72° is the rGO by
elimination; the explanation attached to it is the rGO mechanism ("removal of
functional group and moisture by chemical and thermal reduction", matching a
hydrazine step run at 60 °C); the 8.84 → 3.85 Å collapse is the paper's thesis;
and the hydrogenated GO is treated in the next sentences as a GO, not a reduced
product. The loose phrase goes in M2's `notes`. HYC-0015 is already listed in
§3.7's internal-contradiction table for a related hydrazine/hydrogen confusion.

## 4. Verification — 61 cells, 2 disputed, both upheld

Both disputes were defects in the candidate rows and both are corrected before
anything is appended.

**Dispute 1 — HYC-0015's `title` was wrong, and it was wrong because it was typed
from memory.** The candidate carried "Structural and surface modification of
carbon nanotubes for enhanced hydrogen storage density". That string appears
nowhere in the PDF; it is about carbon nanotubes and this paper measures graphene
oxide. The real title, on the title page and **already carried verbatim by
HYC-0015-M1 and M2**, is "Role of interlayer spacing and functional group on the
hydrogen storage properties of graphene oxide and reduced graphene oxide". The DOI
and page range were right, so the row was the right paper with another paper's
title. The correct value was sitting in the corpus and in
`references/bibliography.bib`, and copying it from either would have avoided this
entirely. §3.5's rule — a citation recalled from weights is not a citation —
applies to the extractor's own paper-level fields, not only to DOIs, and **no
row-local validator catches two different titles under one `paper_id`**. §6 adds
the invariant that would have.

**Dispute 2 — `activation_method` was null and should record the degassing.** All
four sibling HYC-0011 rows carry "vacuum degassed at 353 K for 4-5 h", from the
paper's universal procedure statement, which applies to sample 3 as much as to the
others. Corrected to match.

## 5. Two schema gaps Agent B found, recorded and not fixed here

Both are real and neither is a defect in these rows. Adding a vocabulary value is
permitted by §8.7 and removing one is not, so both are cheap to close later and
nothing is lost by waiting.

- **`MaterialClass` has no `graphite`.** Graphite is not `graphene` — this paper
  defines graphene as "a single layer of graphite" — and is none of the other
  thirteen values, so `other` is the only fit. The gap is not new and this row is
  not the first to hit it: HYC-0004-M1 ("synthetic graphite (non-porous)"),
  HYC-0004-M3 and HYC-0004-M9 ("activated synthetic graphite") are all already
  `other` for the same reason. **A `graphite` value would recover four rows'
  material identity**, and row 2 follows the established precedent exactly.
- **`MeasurementMode` has no `not_applicable`.** A characterization-only row must
  therefore assert `measurement_mode = isothermal`, which asserts an isothermal
  measurement that did not happen — precisely the defect that `not_applicable` was
  added to `MeasurementMethod` to remove in v1.2. It affects the 8 existing
  characterization-only rows as well as row 2, all of which carry `isothermal`
  because nothing else is available.

## 6. A fourth spacing this paper prints and the corpus will still not record

*"The (002) peak in case of hydrogenated graphene oxide is appearing at 2θ =
12.20° and inter layer distance 7.1 Å"* — the graphene oxide under 1000 mbar H₂,
measured by in-situ XRD. After this migration the paper's four printed spacings
are three-out-of-four represented.

**Recommended, and deliberately not done here:** record it as `HYC-0015-M4` on
`sample_id = HYC-0015-S1`, since it is the same physical material in a different
atmosphere — which is what a second `measurement_id` on one `sample_id` is for,
and what the corpus already does for HYC-0016-M13/M14 (one sample before and after
hydrogen treatment). It would be characterization-only, with the 1000 mbar in
`material_description` and **not** in `pressure_bar`, which would assert an uptake
condition that does not exist. Agent B verified the value but **not the cells of
such a row**, so appending it now would put an unverified row in the corpus and
break §3.2. It needs one more Agent B pass, which is cheap, and it is listed as a
Phase C.1 follow-on rather than folded in here.

Two numbers in the same paper that look like spacings and must never enter this
field, recorded so they are not: the TEM "distance of the hexagonal lattice …
about 10.35 nm", which is two orders of magnitude above any graphene lattice
distance and is an internal oddity of the paper, and the TEM "layer thickness is
approximately 5-8 nm", which is a stack thickness.

**A limitation of both agents' reading, stated because it is not resolvable
here:** both XRD figures are raster images, so neither agent could read any
in-plot annotation. Every value above comes from the running prose. If Figs. 4 and
5 print differently-rounded spacings, that is invisible to this extraction.

## 7. Method and post-conditions

The two new rows go in through `scripts/append_paper.py` (§9.1 steps 11–14), which
verifies the staging file from disk, validates it standalone, backs up, appends
positionally in the CSV's physical column order, re-verifies the merged file
against a session baseline and diffs warning types. The staging file populates all
67 columns explicitly, including the defaulted ones, per Appendix A.1.

The two backfilled cells go in through `scripts/backfill_interlayer_spacing.py`,
with the same discipline as the other migration scripts: raw CSV cells through the
`csv` module, the file's own line terminator detected and reproduced, every line
outside the named scope compared **byte for byte**, refuses to re-run, `--dry-run`,
backs up to `/tmp`, and CLI guards so it is testable against a fixture.

Post-conditions, asserted by the scripts and independently by tests:

1. 225 → **227 rows**, 67 columns unchanged.
2. `areal_uptake_g_cm2` goes from **0 rows to 1**, and `interlayer_spacing_nm`
   from **0 to 3**. Neither field is an empty column any more, which is the whole
   point of this migration.
3. The backfill changes exactly 2 cells, both `interlayer_spacing_nm`, plus
   `notes` on HYC-0015-M2. Every other pre-existing cell byte-identical.
4. Zero validation errors. Warning baseline gains no new **type**;
   `Unspecified uptake_type` rises from 202 to 204.
5. `HYC-0011-M5` is the only row in the corpus whose sole uptake is areal, and it
   joins the enumerated non-convertible set, taking it from 10 rows to 11.
6. `HYC-0015-M3` joins the enumerated characterization-only set, 11 → 12, and
   carries no condition and no `*_unstated` flag.
7. **Every row sharing a `paper_id` carries the same `title`, `doi`,
   `first_author`, `year` and `journal`.** A new dataset invariant, added because
   dispute 1 would have passed every existing check.
8. Every pinned count the two rows move is updated in the same commit, with the
   positions enumerated rather than the number merely bumped (§6.7).
