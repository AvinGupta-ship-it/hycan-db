# Migration plan — synthesis-method relabel and HYC-0027 composition backfill

**Status:** written and committed before any protected file is touched, per §6.7.
**Date:** 2026-09-26
**Applied by:** `scripts/migrate_relabel.py` (committed; refuses to re-run)
**Target file:** `data/raw/measurements_v0.1.csv` — and nothing else. No schema
change; no new columns. Corpus stays at 225 rows and 67 columns.

---

## 0. Why

Two corrections carried since Phase C, both flagged in the execution manual's
§18 Phase C.1 list, both source-verified by locate-only passes on 2026-09-26
before any cell was touched.

**1. Eighteen rows carry a `synthesis_method` that was forced before the right
value existed.** `chemical_activation` and `physical_activation` were added in
schema v1.2. HYC-0019's twelve rows and HYC-0022's six were extracted before
that and landed on `carbonization` and `other`. `physical_activation` has zero
rows in the corpus as a result, which makes the vocabulary look untested.

**2. HYC-0027 has no `metal_element` and no `metal_loading_wt_pct`.** It is the
corpus's Pd spillover paper and the reason gap 7 was added, yet the only rows
populating `metal_loading_wt_pct` are HYC-0029's twelve, every one of which
§12.3 excludes as `temperature_cycle`. **So the field currently has zero
analysis-eligible rows** — gap 7 is closed in the schema and open in the data.

A third correction surfaced while verifying the second, and is included because
it is the same field on the same paper (§3).

## 1. HYC-0019 — twelve rows, `carbonization` → `chemical_activation`

Huang et al. 2010. All six samples share one preparation chain and differ only
in a post-treatment, so all twelve rows take the same value.

The paper states the route in its own words: *"Super activated carbon was
prepared by chemical activation \[in\] nitrogen at 1073 K, using KOH as the
activating agent and litchi wood as the precursor"*, and *"litchi wood-based AC
samples with high porosity were prepared using the KOH activation method."*

The chain is: litchi wood → carbonization at 823 K for 2 h under N2 → **KOH
activation, char:KOH 1:4 by mass, 1073 K for 2 h under N2** → dilute HCl wash →
dried 378 K.

**Why `carbonization` is wrong and not merely imprecise.** Carbonization is step
one of a two-step chain and is not the terminal route; the material's porosity
comes from the KOH step. `synthesis_method` records how the sample was made,
and a reader filtering on `carbonization` expecting a pyrolysis-only carbon
would get a 2623 m²/g KOH-activated carbon. The paper never calls any sample
carbonization-only, and no sample stops at that step.

**The word "physical activation" appears nowhere in this paper.** The phrase
*"physical adsorption of nitrogen at 77 K"* does appear and is a
characterization method, not a route. It must not be mined as one.

**A naming trap, recorded so nobody re-derives the route from a label.** The
numeric suffix in `AC-3NA-373` is the **oxidation temperature in kelvin**, and
`3NA` / `1NA` / `HPO` encode the **oxidant**, not the activating agent. All six
samples have the same activation route. A parser reading `AC-3NA-373` as
"activated at 373 K" or "activated with nitric acid" would be wrong twice.

## 2. HYC-0022 — six rows, `other` → two different values

Wang et al. 2009, and **this is the correction that a one-value relabel would
have got wrong.** The paper performs *both* kinds of activation on the same
starting carbon, so its six `other` rows split:

| Rows | Sample | Route | → value |
| --- | --- | --- | --- |
| M2, M3 | AC-C2, AC-C4 | CO2 gasification, 1223 K, 10 mL/min CO2, 2 h and 4 h | `physical_activation` |
| M4, M5, M6, M7 | AC-K3, AC-K5 | KOH, KOH:AC 3:1 and 5:1 by mass, 1023 K, 1 h soak under Ar | `chemical_activation` |

**Not changed: M1 and M8/M9, which are already `commercial` and correct.** M1 is
the as-received Shanghai Dahe carbon the paper starts from, used with no
activation by these authors. M8/M9 are G212 (PICA, Vierzon), a reference carbon
they measured but did not make; the paper states no route for it.

**On the basis for `physical_activation`.** The exact string "physical
activation" is never printed beside `AC-C2`/`AC-C4`. The paper establishes the
mapping by its own taxonomy instead: *"there are typical two kinds of activation
procedures, namely, physical and chemical activations. The physical activation
involves gasification of the carbon materials in the presence of suitable
oxidizing gasifying agents, such as CO2 and steam"*, followed by *"Both physical
and chemical activations were performed in our study."* The CO2 samples are the
only gas-activated ones in the paper. That is the paper's own classification
applied to its own samples, not an inference about chemistry — but it is a step
removed from a verbatim label, so it is stated here and it goes in the row notes.

**A caveat that must travel with these two rows.** The CO2 treatment is called
activation by the authors and **reduced** both surface area and total pore
volume: 1585 → 1488 → 1308 m²/g and 1.44 → 1.22 → 1.10 cm³/g. The paper says so
plainly — *"the destruction of high porosity is more pronounced during the CO2
activation"* — while micropore fraction rose from 41% to 49%. `synthesis_method`
records the route, not its effect, so the value stands; the effect goes in
`notes` so that a reader does not assume activation implies a higher area.

## 3. HYC-0027 — the Pd backfill, and one over-attribution to remove

Parambhath et al. 2012. Five rows, four samples.

| Row | Sample | Change |
| --- | --- | --- |
| M2 | Pd-HEG | `metal_element` → `Pd` |
| M4, M5 | Pd-N-HEG | `metal_element` → `Pd`, `metal_loading_wt_pct` → `21` |
| M3 | N-HEG | `dopant_concentration_at_pct` **21 → null** (see below) |
| M1 | HEG | unchanged — no Pd, no N |

**`metal_loading_wt_pct = 21` on Pd-N-HEG only, and the basis.** The paper
states *"The concentration of Pd was estimated from XPS Pd 3d peaks and was
found to be 21 wt %"*, corroborated by *"energy dispersive X-ray analysis …
which estimates the Pd concentration to be 20 wt %"*. XPS is the value recorded;
the EDX figure goes in `notes`. Both are stated for **Pd-N-HEG only**.

**`metal_loading_wt_pct` is left NULL on Pd-HEG, deliberately.** The only
loading the paper gives for that sample is the nominal as-added figure — *"The
amount of palladium loading was maintained to be 20 for Pd-N-HEG and Pd-HEG
specimens"* — and no XPS or EDX composition is reported for Pd-HEG anywhere,
including in the Supporting Information contents list. Two reasons not to enter
it: a nominal as-added loading is not a measured composition, and **the unit is
missing from that sentence in the PDF text layer**. "wt %" renders correctly
elsewhere in the same extraction, so the omission cannot be dismissed as an
artifact. 20 wt% is near-certain from context (XPS 21, EDX 20, and eq. 1
substitutes q = 0.20 as a weight fraction), but near-certain from context is
what `notes` is for, not what a composition field is for. `metal_element = Pd`
is certain and is recorded.

**The removal: `dopant_concentration_at_pct` on M3 (N-HEG).** The corpus
currently carries 7.0 at% N on N-HEG, Pd-N-HEG and — via the shared sample — its
second row. The paper states a nitrogen content **once**: *"From XPS results,
the nitrogen content is estimated to be about 7 at. %."* That sentence sits in
the XPS discussion, whose only figure is Figure 4, which the paper captions as
being of the **Pd-N-HEG** sample. The Characterization section says XPS was used
*"to determine the nitrogen content and the type of nitrogen bonding in
nitrogen-doped specimen"*, singular. **No nitrogen content is stated for N-HEG.**

N-HEG is Pd-N-HEG's direct precursor and its N content is presumably comparable,
which is exactly why this is worth removing rather than leaving: a presumption
is not a measurement, and the row currently asserts one. The value stays on M4
and M5, where the paper's own sentence places it.

This is a **data removal**, the only one in this migration, so it gets its own
Agent B question (§5) rather than riding along with the relabels.

## 4. What is NOT changed

- `activation_method`, on any row. It already carries the correct free-text
  detail for all 18 relabelled rows, including the conditions.
- HYC-0022's `commercial` rows (M1, M8, M9).
- HYC-0019's `carbonization` step, which remains described in
  `activation_method` and `material_description`.
- Any numeric characterization or uptake value anywhere.
- The corpus's row count, column count, or column order.

## 5. Verification

Agent B receives the paper and the proposed cell changes only, per §3.2, and is
asked three questions rather than one:

1. Is each of the 18 `synthesis_method` values correct against the paper's own
   words, and specifically: does HYC-0022 split 2 / 4 as claimed, or do all six
   take one value?
2. Is `metal_loading_wt_pct = 21` the right value and the right sample, and is
   leaving Pd-HEG null defensible or an omission?
3. **Does the paper state a nitrogen content for N-HEG?** If it does, the removal
   is wrong and must not be applied.

## 6. Method and post-conditions

Same discipline as `migrate_v1_3.py` and `sync_paper_tracking.py`: raw CSV cells
through the `csv` module, the file's own line terminator detected and
reproduced, every line outside the named scope compared **byte for byte** rather
than cell by cell, refuses to re-run, `--dry-run`, backs up to `/tmp`, and
`--expected-rows` / `--expected-changed-cells` as CLI options so the script is
testable against a fixture.

Post-conditions, asserted by the script and independently by
`tests/test_migrate_relabel.py`:

1. 225 rows and 67 columns, unchanged. Physical line count unchanged.
2. Changes confined to four columns: `synthesis_method`, `metal_element`,
   `metal_loading_wt_pct`, `dopant_concentration_at_pct`, plus `notes` on the
   rows those touch. Every other cell byte-identical.
3. `synthesis_method` counts move by exactly: `carbonization` −12,
   `other` −6, `chemical_activation` +16, `physical_activation` +2.
4. `physical_activation` goes from 0 rows to 2 — the value stops being untested.
5. `metal_loading_wt_pct` has at least one row that survives the §12.3 analysis
   filters, which is the condition gap 7 was added to satisfy and which no row
   currently meets.
6. Zero validation errors. Warning baseline unchanged, no new type.
7. HYC-0027's `dopant_concentration_at_pct` is populated on exactly the two
   Pd-N-HEG rows.
