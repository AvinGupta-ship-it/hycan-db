# Migration plan — synthesis-method relabel and HYC-0027 composition backfill

**Status:** written and committed before any protected file is touched, per §6.7.
**Date:** 2026-09-26
**Applied by:** `scripts/migrate_relabel.py` (committed; refuses to re-run)
**Target file:** `data/raw/measurements_v0.1.csv` — and nothing else. No schema
change; no new columns. Corpus stays at 225 rows and 67 columns.

**Revision history of this plan.** First written for an 18-row scope covering
HYC-0019 and HYC-0022 only. Agent B rejected that scope — not the values —
because the v1.2 vocabulary addition shipped with no data migration, so a
one-or-two-paper relabel would make `chemical_activation` mean "papers we
happened to revisit" rather than "papers that chemically activated their
carbon". Its words: *"Either run the whole migration or defer HYC-0019 until you
do. Applying it to one paper is the worst of the three options."* Locate-only
passes on the remaining candidate papers then **narrowed** the true scope rather
than widening it to every row that carries an activation: two of the seven
candidate papers must not change at all (§8). Final scope: **36 rows across five
papers.**

---

## 0. Why

**1. Thirty-six rows carry a `synthesis_method` that was forced before the right
value existed.** `chemical_activation`, `physical_activation` and
`chemical_exfoliation` were added in schema v1.2. Rows extracted before that
landed on `carbonization` (the first step of a two-step route) or `other` (no
value fit). `physical_activation` has **zero** rows in the corpus as a result,
which makes the vocabulary look untested. `chemical_activation` has 12, all of
them rows appended *after* v1.2 (HYC-0026's seven, HYC-0024's five) — so the
field currently partitions the corpus by extraction date rather than by
chemistry.

**The v1.2 plan undercounted this, and the undercount is instructive.**
`docs/migration_v1_2_plan.md` §3 recorded the stranded set as "HYC-0019's twelve
and HYC-0022's four". Two errors in one clause: **twelve** is a row count while
**four** is a sample count (HYC-0022's four author-activated samples are six
rows), and three further papers — HYC-0016, HYC-0020, HYC-0021 — were not
considered at all. This is the §6.7 rows-versus-samples hazard appearing in a
plan document, which is the third time this project has recorded a count in the
wrong unit. Every count in the present plan is a **row** count and is asserted
by the script.

**2. HYC-0027 has no `metal_element` and no `metal_loading_wt_pct`.** It is the
corpus's Pd spillover paper and the reason gap 7 was added, yet the only rows
populating `metal_loading_wt_pct` are HYC-0029's twelve, **every one of which
§12.3 excludes** as `measurement_mode = temperature_cycle`. Verified by
evaluating the §12.3 mask over the current corpus: of the 12 rows carrying a
metal loading, 0 survive the filters. **The field has zero analysis-eligible
rows** — gap 7 is closed in the schema and open in the data. All five HYC-0027
rows survive all four §12.3 filters, so the backfill takes the field from 0
analysis-eligible rows to 3.

A third correction surfaced while verifying the second and is included because
it is the same field on the same paper (§9.3).

## 1. Scope

| Paper | Rows | From | To |
| --- | --- | --- | --- |
| HYC-0016 (Klechikov 2015) | 7 | `other` | `chemical_activation` |
| HYC-0019 (Huang 2010) | 12 | `carbonization` | `chemical_activation` |
| HYC-0020 (Serafin 2024) | 7 | `carbonization` | `chemical_activation` |
| HYC-0021 (Sethia 2016) | 4 | `carbonization` | `chemical_activation` |
| HYC-0022 (Wang 2009) | 4 | `other` | `chemical_activation` |
| HYC-0022 (Wang 2009) | 2 | `other` | `physical_activation` |
| **Total** | **36** | | 34 chemical + 2 physical |

Deltas, which is what the script asserts: `other` −13, `carbonization` −23,
`chemical_activation` +34, `physical_activation` +2. (13 + 23 = 36 = 34 + 2.)

**Two consequences worth stating, because they are the point of the migration.**
`physical_activation` stops being an untested vocabulary value. And
`carbonization` drops from 25 rows to **2** — HYC-0021's CP-400 and CP-600,
which are the only samples in the corpus that stop at pyrolysis. After this
migration `carbonization` means what its name says instead of serving as the
fallback for "pyrolysed, then something the vocabulary could not express".

**A second line of evidence, independent of the source passes.** Every row in
the table above is corroborated from inside the corpus by its own
`activation_method` and `material_description`, which were extracted
independently of `synthesis_method` and which no part of this migration touches:
all 7 HYC-0016 rows read `koh_activation`; all 12 HYC-0019 rows read `KOH
chemical activation, char:KOH 1:4 by mass, 1073 K for 2 h under N2`; all 7
HYC-0020 rows read `KOH activation (KOH/biomass 1:1), pyrolysis 700-900 C`; the
4 HYC-0021 rows read `koh_activation` against `none` on the 2 that stay; and
HYC-0022's split is already written out in its `activation_method` as `CO2
physical activation` on two rows and `KOH chemical activation` on four. The
relabel is not introducing a claim; it is moving a claim the corpus already makes
in free text into the controlled field that analysis reads.

## 2. HYC-0016 — seven rows, `other` → `chemical_activation`

Klechikov et al. 2015. The authors performed the KOH activation themselves:
*"The thermally reduced graphite oxide powder was further subjected to KOH
activation."* Seven of the paper's fourteen rows carry
`activation_method = koh_activation` and take the new value: **M3, M4, M5, M8,
M9, M10, M12.**

**No ratio, concentration or dwell time is stated** for the activation. That is
a reporting gap in the paper, not a reason to withhold the route — the route is
named in the authors' own words. `activation_method` keeps the bare
`koh_activation` token it already holds; nothing is invented to fill it.

**Two things in this paper that are not activation, recorded so they are not
mined as one.** The hydrogen treatment on M14 is a **reductive anneal** at 50
bar H₂ and 350 °C on the same physical sample as M13, not an activation; its
`activation_method` reads `hydrogen_annealing` and both rows keep `other`. And
M11 is a **reference activated carbon** the authors bought, not made.

**The seven rows that keep `other` are a separate, unverified question, left
open on purpose (§14).** Four are unactivated rGO, two are thermally exfoliated
GO, one is the purchased reference carbon. `thermal_reduction` is very likely
right for the first six and `commercial` for the seventh, but neither was part
of the locate pass that settled the KOH rows, and this migration does not relabel
on likelihood.

## 3. HYC-0019 — twelve rows, `carbonization` → `chemical_activation`

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

**The 823 K carbonization must survive the relabel.** It is a real step and the
relabel removes the only field that mentioned it. It is preserved in `notes`
(§9.1) and remains in `activation_method` and `material_description`.

**The word "physical activation" appears nowhere in this paper.** The phrase
*"physical adsorption of nitrogen at 77 K"* does appear and is a
characterization method, not a route. It must not be mined as one.

**A naming trap, recorded so nobody re-derives the route from a label.** The
numeric suffix in `AC-3NA-373` is the **oxidation temperature in kelvin**, and
`3NA` / `1NA` / `HPO` encode the **oxidant**, not the activating agent. All six
samples have the same activation route. A parser reading `AC-3NA-373` as
"activated at 373 K" or "activated with nitric acid" would be wrong twice.

**The five oxidised samples are still not split to `chemical_oxidation`**, for
the reason the existing `notes` gives and which this migration does not disturb:
in this vocabulary `chemical_oxidation` is a graphite-oxide-route *synthesis*
value, the HNO₃/H₂O₂ treatment here is a post-synthesis surface treatment, and
splitting would make the six rows of a controlled single-variable study
non-comparable on the one field saying how the carbon was made.

## 4. HYC-0020 — seven rows, `carbonization` → `chemical_activation`

Serafin et al. 2024. All three materials (G-700, G-800, G-900) were made by the
authors from fern biomass. The KOH is applied to the **raw biomass before any
heat treatment**, so carbonization and activation are a **single step**, not two.

**This is the weakest call in the batch and the reason is worth stating.** For
HYC-0019 and HYC-0021 the two steps are separate and sequential, so the terminal
step is unambiguous. Here there is no terminal step to pick: the same thermal
treatment both carbonizes and activates, which makes `carbonization` *incomplete*
rather than *wrong*. `chemical_activation` is chosen because KOH is present as a
chemical activating agent and because the porosity — the property the field
exists to predict — is created by it; a reader filtering `carbonization` for
pyrolysis-only carbons would otherwise get three KOH carbons. The alternative
reading, that a one-step route should keep `carbonization` with the KOH recorded
only in `activation_method`, is coherent and is the one Agent B is asked to
reject or accept explicitly (§13, question 2). If it accepts the alternative,
these 7 rows drop from the migration and the totals in §1 change to 29 rows,
`carbonization` −16, `chemical_activation` +27.

**A corpus defect noticed here and deliberately not fixed.** HYC-0020's
`sample_id` values are bare `S1`, `S2`, `S3` rather than the
`HYC-0020-S1` form every other paper uses, and five of the seven rows sit on
`S2`. Out of scope; recorded in §14.

## 5. HYC-0021 — four rows, `carbonization` → `chemical_activation`

Sethia and Sayari 2016. **M3, M4, M5, M6** are the four NAC samples, KOH at a
stated **KOH/CP-400 weight ratio of 1.5**, activated at 550, 600, 650 and 700 °C.
This is the one paper in the batch that states its activation ratio, and the
ratio is already in `material_description`.

**M1 and M2 stay `carbonization` and this is the migration's control.** CP-400
and CP-600 are the carbonized precursor at 400 °C and 600 °C with no activation
step; their `activation_method` reads `none` and their `notes` already read
"Non-activated carbonized precursor". They are the only rows in the corpus that
are genuinely carbonization-only, and after this migration they are the only two
rows carrying the value. A migration that relabelled them too would be the
blanket sweep Agent B warned against; that it does not is checkable.

## 6. HYC-0022 — six rows, `other` → two different values

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

## 7. The two-line summary of the whole relabel

Four papers KOH-activated their own carbon and said so; their rows now say so in
the field analysis reads. One paper did both kinds of activation and its rows
now carry both values. Nothing was relabelled on inference, and nothing was
relabelled because it merely carries an `activation_method`.

## 8. Two papers that carry an activation and must NOT change

Both were candidates on a text search for activation language and both fail on
reading. Recording them is the point: the difference between this migration and
a sweep is that the sweep has no way to produce this section.

**HYC-0001 (Panella 2005) — 2 rows stay `commercial`.** The authors activated
nothing. "Activated carbon I" was synthesised by Richard Chahine at Université
du Québec — an academic source, not a commercial one, so `commercial` is itself
imperfect — and the KOH-from-coke route that the row's `activation_method`
records is stated of **AX-21**, which the paper says its sample is only
*"similar to"*. Relabelling to `chemical_activation` would assert a route the
paper attributes to a different material. The 2 rows keep `commercial` and the
imprecision is recorded in §14 rather than traded for a wrong value.

**HYC-0004 (Nijkamp 2001) — 16 rows stay as they are** (`commercial` ×11,
`pyrolysis` ×3, `other` ×2). The authors activated nothing; Norit supplied the
activated carbons. Every route statement in the paper is a hedged generic class
description cited to textbooks — *"usually phosphoric acid"*, *"e.g. peat,
lignite, coal"* — and describes how activated carbons are made in general, not
how these samples were made. Two specific traps: sample 13 appears in neither
the steam list nor the chemical list, and sample 15's label says AIR while the
text says steam. This is the paper where a text-matching relabel would have done
the most damage, because 14 of its rows carry `steam activation 1000C` in
`activation_method` and one carries `chemical (phosphoric acid) activation`, all
of it supplier-side and none of it sample-specific.

## 9. HYC-0027 — the Pd backfill, the removal, and four companion edits

Parambhath et al. 2012. Five rows, four samples.

| Row | Sample | Change |
| --- | --- | --- |
| M2 | Pd-HEG | `metal_element` → `Pd`, `metal_loading_wt_pct` → `20` |
| M4, M5 | Pd-N-HEG | `metal_element` → `Pd`, `metal_loading_wt_pct` → `20`, `dopant_concentration_method` → `XPS` |
| M3 | N-HEG | `dopant_concentration_at_pct` **7 → null** |
| M1 | HEG | unchanged — no Pd, no N |

### 9.1 `metal_loading_wt_pct = 20` on all three Pd rows

The first draft of this plan recorded **21** (XPS) on Pd-N-HEG and left Pd-HEG
**null**. Agent B disagreed with both and is right on both.

**On the value.** The paper gives three figures for Pd-N-HEG: *"The
concentration of Pd was estimated from XPS Pd 3d peaks and was found to be 21 wt
%"*; *"energy dispersive X-ray analysis … which estimates the Pd concentration
to be 20 wt %"*; and the nominal *"The amount of palladium loading was
maintained to be 20 for Pd-N-HEG and Pd-HEG specimens"*. Eq. 1 substitutes
q = 0.20 as a weight fraction. **20 is supported by three independent statements
and 21 by one**, and XPS is surface-sensitive — on a supported nanoparticle it
over-reads the bulk loading, which is exactly the direction of the discrepancy.
20 goes in the field; the XPS 21 goes in `notes`.

**On Pd-HEG being null.** The first draft gave three grounds and one of them was
wrong. Grounds (i) *a nominal as-added loading is not a measured composition* and
(ii) *no XPS or EDX composition is reported for Pd-HEG anywhere* both stand. But
ground (iii) — that the unit is missing from the sentence in the PDF text layer,
so the quantity is unrecoverable — does not: the unit **is** recoverable, from
EDX's 20 wt% and from Eq. 1's q = 0.20 on the same material, and this project
has already resolved bare percentages on these same five rows (every HYC-0027
uptake is recorded from a bare percentage, with the inference disclosed in
`notes`). Applying a stricter rule to the loading than to the uptake on the same
row is not caution, it is inconsistency. And with 20 chosen for Pd-N-HEG on the
nominal-plus-EDX basis, the identical nominal statement covers Pd-HEG. **20 on
all three, one basis, disclosed in `notes`.**

### 9.2 `dopant_concentration_method = XPS` on M4 and M5

The 7 at% nitrogen these rows keep is an XPS value and the field for saying so
has existed since v1.2 and is empty. Filling it is required by Agent B and is
also what makes the removal in §9.3 legible: after this migration the only rows
carrying a nitrogen at% are the two whose method is recorded.

### 9.3 The removal: `dopant_concentration_at_pct` on M3 (N-HEG)

The corpus currently carries 7.0 at% N on N-HEG, Pd-N-HEG and — via the shared
sample — its second row. The paper states a nitrogen content **once**: *"From XPS
results, the nitrogen content is estimated to be about 7 at. %."* That sentence
sits in the XPS discussion, whose only figure is Figure 4, which the paper
captions as being of the **Pd-N-HEG** sample. The Characterization section says
XPS was used *"to determine the nitrogen content and the type of nitrogen bonding
in nitrogen-doped specimen"*, singular. **No nitrogen content is stated for
N-HEG.**

`dopant_element = N` **stays** on M3: the paper calls the sample nitrogen-doped
and describes the plasma treatment that doped it. The element is stated; the
concentration is not. That is the distinction the two fields exist to carry.

N-HEG is Pd-N-HEG's direct precursor and its N content is presumably comparable,
which is exactly why this is worth removing rather than leaving: a presumption
is not a measurement, and the row currently asserts one. The value stays on M4
and M5, where the paper's own sentence places it.

This is a **data removal**, the only one in this migration, so it gets its own
Agent B question (§13) rather than riding along with the relabels.

**Agent B's physics argument for the removal, recorded because it is stronger
than the textual one.** The 7 at% is an XPS *surface atomic percentage* whose
denominator includes every element XPS sees — on Pd-N-HEG that is C, N, O **and
Pd**. N-HEG has no Pd in its denominator. So N-HEG's own-basis nitrogen at%
would necessarily be **higher** than 7, not equal to it. Copying the figure
across is therefore not merely unsupported, it is biased low in a knowable
direction.

## 10. Companion edits to `notes`, which are mandatory, not cosmetic

Three papers' `notes` currently contain sentences that this migration makes
**false**. Leaving them would put the row's prose in contradiction with its own
controlled field — the failure mode §13.4 was written about. These are not
optional polish and they ship in the same commit as the cell changes.

1. **HYC-0019, all 12 rows.** Two sentences go: `synthesis_method stays
   carbonization on all six rows…` and `…the vocabulary has no chemical_activation
   value.` The replacement states the two-step route including the **823 K
   carbonization**, records that the field held `carbonization` until this
   migration, and preserves verbatim the reasoning for not splitting the oxidised
   samples to `chemical_oxidation`.
2. **HYC-0022, all 9 rows.** The sentence `Recorded as 'other' rather than a
   vocabulary value because the vocabulary has neither physical_activation nor
   chemical_activation; the route is in activation_method.` is paper-level
   boilerplate present on **all nine** rows, including the three `commercial`
   rows whose value does not change. So `notes` changes on 9 rows while
   `synthesis_method` changes on 6, and the script asserts exactly that. The
   replacement keeps the full dispute history — the extractor's `commercial`, the
   verifier's rejection, the carbon-yield evidence — and records the relabel.
   M2 and M3 additionally get the §6 caveat that the CO2 route *reduced* area and
   pore volume.
3. **HYC-0027-M3.** Its `notes` opens `Nitrogen content approximately 7 at% by
   XPS.` — which, after §9.3, asserts in prose exactly what the removal rejects.
   Replaced with the statement that no nitrogen content is reported for this
   sample, why, and that a presumption is not a measurement.
4. **HYC-0027-M2, M4, M5.** Each gains one sentence recording the basis of
   `metal_loading_wt_pct = 20`, because no `metal_loading_method` field exists and
   `notes` is the only place the basis can live. M4/M5 also record that the XPS 21
   wt% is *not* what the field holds and why.

No `notes` edit is made on HYC-0016, HYC-0020 or HYC-0021: nothing in their notes
becomes false, and adding 18 copies of a sentence that this plan already states
would bloat the CSV without adding a fact. Provenance for those rows is this
document plus the CHANGELOG, which is the mechanism `migrate_v1_1.py` used for
its 34 relabels.

## 11. One test asserts something this migration makes false

`tests/test_dataset_invariants.py::test_metal_loading_is_not_confused_with_dopant_concentration`
fails after this migration, and **it is the test that is wrong, not the data.**
It asserts:

```python
loaded = dataset[dataset["metal_loading_wt_pct"].notna()]
assert set(loaded["paper_id"]) == {"HYC-0029"}
assert loaded["dopant_concentration_at_pct"].isna().all()
```

Both lines fail: HYC-0027 joins the first set, and M4/M5 carry a metal loading
**and** a dopant concentration at once.

The docstring says "Schema v1.2 gaps 7 and 8 exist to keep these apart." Keeping
the *fields* apart is right and is preserved. Asserting that the two **never
co-occur on a row** is a much stronger claim that the fields were never given,
and that the corpus satisfied only by accident: **Pd-N-HEG is palladium metal on
nitrogen-doped graphene, so a metal loading and a dopant concentration are both
correct on the same row.** It is the paper gaps 7 and 8 were added for, and it
breaks a test written as though they were mutually exclusive. That is the §6.7
lesson — pin the property, not the corpus's current shape — recurring in a test
rather than in a count.

**Rewritten to assert the real invariants:** every row with a metal loading names
its `metal_element`; every row with a dopant concentration names its
`dopant_element`; no metal loading is stored in a dopant field or vice versa; and
the rows where both legitimately co-occur are **enumerated**, so a future
accidental co-occurrence still fails while the deliberate one passes.

## 12. Three stale vocabularies in `docs/data_dictionary.md`, and a check for them

§8.7 requires the data dictionary to be updated by the commit that changes the
schema. For the v1.2 vocabulary additions it was not, and this migration is what
makes that load-bearing: it puts 36 rows onto values the dictionary says do not
exist.

Verified by reading the file: `physical_activation`, `chemical_activation`,
`chemical_exfoliation` and `not_applicable` appear **zero times** in
`docs/data_dictionary.md`. Three rows are corrected:

| Field | Row | Missing |
| --- | --- | --- |
| `synthesis_method` | `\| Allowed values \|` | `physical_activation`, `chemical_activation`, `chemical_exfoliation` (v1.2) |
| `measurement_method` | `\| Allowed values \|` | `not_applicable` (v1.2) |
| `surface_area_method` | `\| Type \| Controlled: … \|` | `alpha_s_plot`, `t_plot`, `not_reported` (v1.3) |

The third is a different defect: v1.3 **did** document those three values, in a
second `### surface_area_method` section 580 lines further down. So the file
currently gives two different vocabularies for one field, and the stale one is
the one a reader reaches first. Corrected for internal consistency, not because
anything was undocumented.

**`tests/test_data_dictionary.py` is added, because this is the third recurrence
of the same failure.** §8.7 is a manual step and nothing checks it; the manual's
own lesson is that *a manual step that nothing checks will be skipped*. The test
reads every `Literal` vocabulary off the live `MeasurementEntry` model — not off
a regex over comments, which mined comment prose as values once before — and
asserts every value appears as a backticked token in `docs/data_dictionary.md`,
and that every vocabulary field has a section. It would have caught all four
missing values and has no false positives against the current file.

## 13. Verification

Agent B receives the papers and the proposed cell changes only, per §3.2, plus
`src/hycan/schema.py` per Appendix A.3, and is asked five questions rather than
one:

1. Is each of the 36 `synthesis_method` values correct against its paper's own
   words, and specifically: does HYC-0022 split 2 / 4 as claimed, or do all six
   take one value?
2. **HYC-0020 applies KOH to raw biomass, so carbonization and activation are one
   step.** Is `chemical_activation` right, or should a one-step route keep
   `carbonization` with the KOH recorded only in `activation_method`? Answer for
   these 7 rows specifically; §4 states the case for both readings.
3. Are HYC-0001's 2 rows and HYC-0004's 16 rows correctly **excluded**? Is there
   any sample in either paper the authors actually activated themselves?
4. Is `metal_loading_wt_pct = 20` the right value on all three Pd rows, and is
   the nominal-plus-EDX basis sound where XPS says 21?
5. **Does the paper state a nitrogen content for N-HEG?** If it does, the removal
   is wrong and must not be applied.

## 14. What is NOT changed, and what stays open

Not changed by this migration:

- `activation_method`, on any row. It already carries the correct free-text
  detail for all 36 relabelled rows, including the conditions, and it is the
  independent corroboration §1 relies on.
- HYC-0022's `commercial` rows (M1, M8, M9) — their `notes` change, their
  `synthesis_method` does not.
- HYC-0021's `carbonization` rows (M1, M2), the migration's control.
- HYC-0016's other seven rows, HYC-0001's two, HYC-0004's sixteen.
- `dopant_element` on HYC-0027-M3, which is stated.
- Any numeric characterization or uptake value anywhere.
- The corpus's row count, column count, or column order.

Left open, recorded here so none of it is lost:

- **HYC-0016's seven remaining `other` rows.** `thermal_reduction` is likely
  right for the six rGO/TEGO rows and `commercial` for the purchased reference
  carbon (M11). Needs a locate pass on the paper; not relabelled on likelihood.
- **HYC-0001's `commercial` on an academically-synthesised sample.** Activated
  Carbon I came from a university lab. The vocabulary has no value for
  "synthesised by a third party, not the authors"; `commercial` is the closest
  and is wrong about the supplier.
- **HYC-0020's `sample_id` values** are bare `S1`/`S2`/`S3` rather than
  `HYC-0020-S{n}`. A dataset invariant asserting the `sample_id` format would
  catch it and does not exist.
- **Manual v2.3 §12.3's counts are pinned to the pre-Phase-C.1 corpus** — it says
  206 rows, 38 excluded, 168 kept across 17 papers. Evaluating the same four
  filters over the current 225 rows gives **43 excluded, 182 kept across 19
  papers**. Not caused by this migration and not fixed by it; the §13.7
  `score_reproducibility` fix is the commit that has to recompute that table
  anyway.

## 15. Method and post-conditions

Same discipline as `migrate_v1_3.py` and `sync_paper_tracking.py`: raw CSV cells
through the `csv` module, the file's own line terminator detected and
reproduced, every line outside the named scope compared **byte for byte** rather
than cell by cell, refuses to re-run, `--dry-run`, backs up to `/tmp`, and
`--expected-rows` / `--expected-changed-cells` as CLI options so the script is
testable against a fixture.

The dataset is LF-terminated, ends with a newline, and has 226 physical lines for
225 rows — so no cell contains an embedded newline and physical line *n* is data
row *n−1*. The script asserts that before it maps a row to a line, because the
byte-level line check is unsound the moment it stops being true.

Every `notes` edit is applied as an **exact substring replacement** on a sentence
this plan quotes, and the script refuses if the substring is not found on exactly
the rows expected. Rewriting a whole `notes` cell from a value read in a tool
result is how a truncated field gets silently shortened.

Post-conditions, asserted by the script and independently by
`tests/test_migrate_relabel.py`:

1. 225 rows and 67 columns, unchanged. Physical line count unchanged.
2. Changes confined to six columns: `synthesis_method`, `metal_element`,
   `metal_loading_wt_pct`, `dopant_concentration_at_pct`,
   `dopant_concentration_method`, `notes`. Every other cell byte-identical.
3. `synthesis_method` counts move by exactly the **deltas** in §1 — `other` −13,
   `carbonization` −23, `chemical_activation` +34, `physical_activation` +2 —
   asserted against the before-counts, not against absolute totals.
4. Exactly 36 rows change `synthesis_method`, and they are exactly the 36
   measurement_ids this plan names.
5. `physical_activation` goes from 0 rows to 2 — the value stops being untested.
6. `carbonization` is left on exactly `HYC-0021-M1` and `HYC-0021-M2`.
7. `metal_loading_wt_pct` gains exactly 3 rows, all HYC-0027, **all of which
   survive the four §12.3 filters** — the condition gap 7 was added to satisfy
   and which no row currently meets.
8. `dopant_concentration_at_pct` is populated on exactly the two Pd-N-HEG rows
   within HYC-0027, and HYC-0025's five rows are untouched.
9. Every row carrying `metal_loading_wt_pct` also carries `metal_element`.
10. `notes` changes on exactly 12 + 9 + 4 = 25 rows, and every quoted substring
    was found and replaced on exactly the rows expected.
11. Zero validation errors. Warning baseline unchanged at `Unspecified
    uptake_type ×202` and `Pre-2005 raw-CNT high uptake (Tier D) ×1`, no new
    type.
