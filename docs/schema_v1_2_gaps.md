# Schema v1.2 — gaps found during Phase C extraction

Status: **open, and now complete.** Nothing here has been implemented. All
twelve Phase C papers have been read, which was the precondition for treating
this as one migration rather than several; see *Sequencing*.

Every gap below blocks real, already-extracted, already-verified rows or costs
real reported values. None is hypothetical, and each names the papers it bites.

**Scoreboard after Phase C extraction (2026-09-25).** Twelve papers read, 105
rows extracted, 35 written, 70 held.

*(Corrected 2026-09-25. This line first read "133 rows extracted … 98 held".
Both figures were wrong: the per-paper counts in the table below were right, but
the totals were not computed from them. Summing the table gives 105 and 70. The
error was arithmetic in a summary line; no row, no per-paper count and no
decision rested on it. It is flagged rather than silently amended because a
public dataset's documentation is not a place to quietly change a number.
`docs/migration_v1_2_plan.md` §0 records it too.)*

| Paper | Extracted | Written | Held by |
| --- | --- | --- | --- |
| HYC-0007 Takagi 2004 | 10 | 0 | gap 3b |
| HYC-0009 Ioannatos 2010 | 20 | 0 | gap 4 (14 rows), gap 2 (6 TPD rows) |
| HYC-0011 Qikun 2002 | 5 | 0 | gap 2, gap 10 |
| HYC-0012 Liu 2010 | 6 | **6** | — |
| HYC-0015 Rajaura 2016 | 2 | 0 | gap 2 |
| HYC-0017 Ma 2009 | 3 | **2** | gap 1 (1 row) |
| HYC-0019 Huang 2010 | 12 | **12** | — |
| HYC-0022 Wang 2009 | 9 | **9** | — |
| HYC-0024 de la Casa-Lillo 2002 | 8 | 0 | gap 10, gap 6 |
| HYC-0025 Sawant 2021 | 6 | **6** | — |
| HYC-0026 Zhao 2013 | 7 | 0 | gap 2, gap 8 |
| HYC-0029 Chen 2008 | 16 | 0 | gap 9, gap 7, gap 1 |

Five of the twelve appended cleanly. **Seven did not, and no two are blocked by
the same thing** — which is the argument for one migration.

---

## Gap 1 — No representation for an uptake reported only as a bound

`uptake_wt_pct` is a bare float. A paper reporting "below 0.2 wt.%" has two
available representations and both are wrong: write `0.2` and a bound becomes a
measurement that enters isotherm fits and Chahine comparisons as a point; write
nothing and the measurement vanishes.

**Bites:** HYC-0017 at 290 K / 60 bar ("the hydrogen uptake is below 0.2 wt.% at
290 K", stated twice, no point value, no isotherm to digitize) — 1 row, and it is
the paper's headline negative result. HYC-0029 ("the high temperature activated
CNTs still possessed more than 1.0 wt.% of weight change") — a lower bound for
two samples. HYC-0024 ("hydrogen storage values at 10 MPa close to 1 wt %") — an
approximation, not a bound, and equally unstorable.

**Why it matters beyond three rows.** Null and bounded results are the antidote
to this literature's publication bias. A database that can record 8.0 wt% but not
"below 0.2 wt%" systematically over-represents the field's optimistic tail — the
exact distortion the tiering rubric exists to correct.

**Fix:** `uptake_bound` (enum: `exact`, `upper`, `lower`, `approximate`, default
`exact`). Cross-field rule: anything not `exact` is excluded from isotherm
fitting and from headline capacity statistics, and `plotting.py` renders bounds
as arrows.

---

## Gap 2 — An uptake-bearing row cannot say its paper never stated a condition

Schema v1.1 made temperature and pressure conditional — required with an uptake,
optional without (§8.5 gap 3). That fixed characterization-only rows. It does not
fix a paper that reports an uptake without stating the conditions numerically.

**Bites, four papers:**

- **HYC-0011** (Qikun 2002). Four uptakes (0.26, 0.21, 0.22, 8.0 wt%) and no
  numeric temperature anywhere — only "room temperature". Three of the four have
  no numeric pressure either ("just greater than 1 atm", "above 1 atm").
- **HYC-0015** (Rajaura 2016). Two uptakes (1.90, 1.34 wt%) at a stated 80 bar,
  temperature only as "room temperature". The paper's one "298 K" belongs to two
  cited works by other groups.
- **HYC-0009** (Ioannatos 2010), six TPD rows. Adsorption temperature stated
  (298 K); pressure never stated. The runs were under flowing H2 at 40 cm³/min,
  ambient by construction, but the paper does not say so and §3.4 forbids
  supplying it.
- **HYC-0026** (Zhao 2013), three rows. The pressure does not appear in the
  sentence reporting the uptakes; 4 MPa has to be assembled from "a plateau was
  reached at 4 MPa", a later "at 2 MPa instead of 4 MPa", and a figure caption
  that labels *excess* uptake while the recorded values are *adsorbed* uptake.
  The linkage crosses a quantity boundary, which is too weak to append on.

Imputing 298 K is the obvious shortcut and it is not available: "room
temperature" in a 2002 Chinese laboratory and a 2016 Indian one are not the same
number, the difference matters at these uptake levels, and substituting a
convention silently fabricates a measurement condition.

**Fix:** `temperature_unstated` and `pressure_unstated` booleans, default
`false`, each required `true` for the corresponding field to be null on an
uptake-bearing row. Analysis filters on the flag instead of discovering nulls. A
free-text `temperature_as_reported` is worse — nothing downstream can consume it.

---

## Gap 3 — One surface-area field, and it is named `bet_`

**3a. The field name asserts a method the paper may not claim.**
`surface_area_method` (v1.1 gap 1) records the truth, but the number still sits
in `bet_surface_area_m2_g`, and `plotting.py` plus any ML feature of that name
consume all of them as BET. Now five papers: HYC-0005 (a total surface area),
HYC-0012 (method never stated), HYC-0021 and HYC-0023 by inheritance.

**3b. A paper can report more than one surface area, or none for some samples.**

- **HYC-0007** (Takagi 2004) reports, per sample, a *micropore* surface area
  (320–2250 m²/g) and an *external* surface area (20–590 m²/g) from an αs-plot,
  and no total. **Eighteen measured values have nowhere to go.** Summing them
  would fabricate a total; putting the micropore value in
  `bet_surface_area_m2_g` is worse than the HYC-0005 case, where the quantity
  was right and only the method unknown — here the quantity itself differs. All
  ten rows are held on this alone. HYC-0004 (Nijkamp 2001) is already in the
  corpus with a t-plot area and wants the same fields.
- **`surface_area_method` cannot say "not reported for this sample."** HYC-0022's
  G212 and HYC-0029's twelve Co-loaded samples have no surface area, in papers
  that do report surface areas for their other samples. `none` is reserved for
  papers reporting none at all, so those rows take `unspecified`, which already
  means "reported without a stated method" on 35 existing rows. The two states
  are now conflated in the dataset.

**Fix:** rename nothing — renaming `bet_surface_area_m2_g` breaks every consumer
and every published row reference. Add `micropore_surface_area_m2_g` and
`external_surface_area_m2_g`; extend `surface_area_method` with `alpha_s_plot`,
`t_plot` and `not_reported`; add a cross-field check that micropore + external is
consistent with a populated total when all three exist. Document in
`docs/data_dictionary.md` that `bet_surface_area_m2_g` means "the paper's
headline total specific surface area, method given by `surface_area_method`" —
which is what it has meant since v1.1.

---

## Gap 4 — Two reported uptake values on one row can contradict each other

`validate.py` warns when `uptake_mmol_g` and `uptake_wt_pct` disagree (the
corpus's `mmol/g and wt% inconsistent ×1`). There is no equivalent for
`uptake_ml_stp_g` versus `uptake_wt_pct`, and `_gravimetric_wt_pct()` silently
prefers wt% when both are present.

**Bites:** HYC-0009 (Ioannatos 2010) tabulates both a wt% and a volume `Vs` for
every measurement, and **the two cannot be reconciled**. Converting Vs at the
project's STP convention gives 0.048–0.145 wt% against a reported 0.12–0.36 wt%
at 298 K, and 0.69–1.25 wt% against a reported 1.35–3.27 wt% at 77 K. The
discrepancy factor is 2.0–2.6 and is not constant across rows, so it is not a
unit error with one fix. Separately, the paper's "H/C" column reconciles with its
wt% only if read as H2 *molecules* per carbon atom, while the text calls it
hydrogen *atoms* per carbon atom.

The fourteen volumetric rows are therefore extracted with `uptake_wt_pct` only —
the paper's headline quantity, the one its abstract and conclusions argue from —
with Vs and the discrepancy in `notes`. Filling `uptake_ml_stp_g` would have
asserted an STP basis the paper never states *and* stored two mutually
contradictory uptakes on one row.

**Fix:** extend the consistency check to all three uptake fields pairwise at
WARNING severity, and add the new warning type to the §11.5 baseline in the same
commit (a new warning type is otherwise a stop condition). **Cheapest gap to
close and it should go first** — it is the one that would have caught this
automatically instead of relying on a verifier noticing.

---

## Gap 5 — `synthesis_method` has no value for activation, and this is now the widest gap

Activation is how a high-surface-area carbon acquires its porosity. The
vocabulary has no term for it, so five Phase C papers had to be forced:

- **HYC-0019** (litchi-wood char + KOH, 1073 K) → `carbonization`, describing
  only the skeleton-forming step.
- **HYC-0022** (commercial AC + CO2 at 1223 K, or + KOH at 1023 K) → `other` on
  four rows. **This produced the protocol's first real dispute**: the extractor
  assigned `commercial` throughout, the verifier rejected it for the four
  samples the authors activated themselves, citing the paper's own "Both
  physical and chemical activations were performed in our study" and the carbon
  yields (62/49/53/43%) that Table 1 reports for exactly those four. The
  disagreement was upheld and is recorded in those rows' notes. Had the
  vocabulary held the right value, the dispute would not have arisen.
- **HYC-0026** (anthracite + KOH) → `other`, discarding the paper's most basic
  material descriptor.
- **HYC-0029** (CVD MWCNT + KOH, 873–1073 K) → activation in `activation_method`
  only.
- **HYC-0024** (KOH-activated anthracite) → `other`.

Two smaller vocabulary holes: **`chemical_exfoliation`** for HYC-0017 (mapping it
to `chemical_oxidation` was rejected — the paper's XPS C/O of 10.8–14.9 is
inconsistent with a graphite-oxide route), and a **`not_applicable`** value for
`measurement_method` on characterization-only rows, which currently must carry
`unknown` in a required field when the true statement is "no measurement here".

**Fix:** add `physical_activation`, `chemical_activation` and
`chemical_exfoliation` to `synthesis_method`; add `not_applicable` to
`measurement_method`. Leave HYC-0011's FePc case alone — `pyrolysis` and `cvd`
both genuinely cover it, and that ambiguity is the paper's, not the schema's.

---

## Gap 6 — Pore-volume and pore-size fields have no method or cutoff

The schema has four porosity fields and no way to say how any of them was
determined. Across Phase C the same field name carries incompatible quantities:

- `micropore_volume_cm3_g` is Dubinin–Radushkevich on **CO2 at 273 K** in
  HYC-0019 and HYC-0024, DR on **N2 at 77 K** in HYC-0024's other column, plain
  DR in HYC-0022 and HYC-0026, and a **DFT** volume in HYC-0021. In HYC-0019 the
  surface area comes from N2 at 77 K while the micropore volume comes from CO2 at
  273 K on the same row — different probe gases, unrecordable, and the reason
  that paper's surface area falls while its micropore volume rises.
- `average_pore_diameter_nm` would hold a **BJH desorption average** (HYC-0022,
  which the paper itself calls the *mesopore* size), a **DR characteristic-energy
  slit width** (HYC-0024), an **HK median micropore size**, or **L0 by Stoeckli**
  (HYC-0026). These are not interchangeable. HYC-0022's row is left empty for
  this reason: storing its 2.5 nm BJH value would tell a reader the best sample's
  characteristic pore is 2.5 nm when the paper attributes its performance to
  0.67 nm, and BJH is invalid for that sample's type-I isotherm anyway.
- **`ultramicropore_volume_cm3_g` has an undocumented cutoff collision.** It is
  documented at 0.7 nm and carries 0.7 nm values for HYC-0005 and HYC-0021.
  HYC-0022's V<1nm is cut at **1 nm**; HYC-0024's DR-CO2 column states **no
  cutoff at all**. Both were left empty rather than mixed in, because this is the
  one quantity v1.1 gap 4 was added to make comparable across the corpus, and
  mixing cutoffs would destroy exactly that. HYC-0022's paper concludes V<1nm
  predicts its 1 bar uptake better than the micropore fraction does, so the loss
  is real.

**Fix:** `pore_volume_method`, `pore_volume_probe_gas`, `pore_diameter_method`,
and either an explicit `ultramicropore_cutoff_nm` or a second field for the
1 nm cutoff. Also add `mesopore_volume_cm3_g` and
`median_micropore_diameter_nm`, both reported by several papers with nowhere to
go.

---

## Gap 7 — Metal loading in weight percent has no field

**Bites both of the corpus's metal-spillover papers.** HYC-0029 reports Co
1.27–14.62 wt% across twelve samples as its primary independent variable;
HYC-0027 (already in the corpus) reports Pd at 20–21 wt% buried in notes.
`dopant_concentration_at_pct` is atomic percent and, per §8.2, stays blank when a
paper reports weight percent — so **the spillover subset cannot be analysed
against metal loading at all.**

A supported catalyst metal is also not the same thing as a substitutional
heteroatom dopant. HYC-0025's boron and HYC-0026's nitrogen are lattice dopants;
HYC-0029's cobalt and HYC-0027's palladium are impregnated particles.

**Fix:** `metal_element` and `metal_loading_wt_pct`, kept distinct from
`dopant_element`. While there: `residual_metal_element` and
`residual_metal_wt_pct` — HYC-0029 reports residual Co of 1.02/0.16/0.09/0.15
wt% from its synthesis catalyst, and residual synthesis metal is the
Hirscher-contamination class of problem that decides whether an uptake is the
carbon's at all.

---

## Gap 8 — Dopant concentration in weight percent has no field

Same shape as gap 7, different field. **HYC-0026** reports nitrogen content only
in wt% (0.20–15.07), never in at%, and that is the paper's central variable and
the subject of its title. `dopant_concentration_at_pct` cannot hold it, and
converting wt% → at% would store a derived number the paper does not report. All
seven rows are held partly on this.

The paper also reports bulk (elemental analysis) and surface (XPS) nitrogen
contents that differ systematically — its explicit finding — and no field records
which technique a composition came from.

**Fix:** `dopant_concentration_wt_pct`, plus `dopant_concentration_method`
(`elemental_analysis`, `XPS`, …).

---

## Gap 9 — A non-isothermal measurement is stored as if isothermal

**HYC-0029** (Chen 2008) measures a weight difference across a
303 → 673 → 303 K cycle at constant 1 atm in flowing hydrogen. The stored
quantity is therefore the difference between the adsorbed state at 303 K and the
desorbed state at 673 K — **not** an isothermal uptake referenced to vacuum or
zero coverage. `temperature_k` is a single required float, so storing 303 asserts
an isothermal 303 K measurement that did not happen, and those thirteen values
are not commensurable with the rest of the corpus. They must not enter a Chahine
plot or any isotherm comparison.

This will recur in every TGA-cycling spillover paper, which is a live subfield.
Storing them unflagged would quietly corrupt the corpus's core analysis, which is
why all sixteen rows are held.

**Fix:** `measurement_mode` (`isothermal`, `temperature_cycle`, `TPD`,
`flow`), plus `reference_temperature_k` or a `temperature_k_min` /
`temperature_k_max` pair. Analysis restricts to `isothermal` by default.

---

## Gap 10 — Volumetric and areal hydrogen capacity have no field

The schema's three uptake fields are all gravimetric per gram of sample. Papers
that report hydrogen per unit *volume* have nowhere to put it:

- **HYC-0024** (de la Casa-Lillo 2002) reports, for all eight samples, an
  adsorbed-H2 density in kg/m³ of micropore volume, and Ms, a tank-volumetric
  capacity including compressed gas. **These are the only hydrogen quantities in
  its primary table.** Its wt% values exist solely in a figure. So the paper
  yields **zero storable uptake values** and all eight rows are held. A wt% could
  be computed as density × micropore volume, but the paper does not say which of
  its two micropore volumes is the basis, so that would be our arithmetic rather
  than its measurement.
- **HYC-0022** reports 43.2 g/L for its best sample.
- **HYC-0011** reports areal uptake in g/cm² of film, which is what makes its
  8.0 wt% claim checkable and irreconcilable (see below).

**Fix:** `volumetric_capacity_kg_m3` with a basis flag (pore volume / packing
volume / tank volume, and whether compressed gas is included), plus the
`packing_density_g_cm3` and `skeletal_density_g_cm3` the same papers report.
HYC-0024's helium skeletal density is load-bearing: it is the quantity used to
convert raw weight uptake into adsorbed amount, so without it the excess/absolute
basis cannot be reconstructed downstream.

---

## One finding that is not a schema gap

**HYC-0011's headline 8.0 wt% is arithmetically irreconcilable with its own
numbers.** Its areal uptake (6.3×10⁻⁶ g/cm²), film mass (9.0 mg) and two stated
film areas (12 and 18 cm²) imply 0.84–1.26 wt%; reaching 8.0 wt% would require a
film area of ~114 cm², nine times the largest the paper states. Recomputed
independently by the adjudicator. The paper gives no intermediate working, so the
cause cannot be determined from the text and none is asserted.

Per `docs/reproducibility_tiering.md` — "Tiering is disclosure, not deletion" —
the row belongs in the corpus at Tier D with the discrepancy quoted verbatim, not
dropped. It is blocked on gap 2, not on this.

---

## Sequencing

Order:

1. **Gap 4** — a validator change with no migration. Do it first; it is the only
   gap whose absence let a real inconsistency through undetected.
2. **Gaps 1, 2, 5, 7, 8** together — additive columns and vocabulary values with
   defaults that leave every existing row byte-identical.
3. **Gap 9** — additive, but needs a decision on what the analysis default is.
4. **Gaps 3, 6, 10** last — these need a `docs/data_dictionary.md` rewrite and
   touch `plotting.py` and any ML feature list.

Unblocking is worth **70 rows across seven papers**, taking the corpus from 156
rows / 16 papers to **226 rows / 23 papers** — past the 20-paper Phase 3
milestone. Stages 1–3, which schema v1.2 implements, account for 52 of those 70
rows and five of the seven papers (HYC-0009, HYC-0011, HYC-0015, HYC-0026,
HYC-0029, plus one HYC-0017 row), reaching 208 rows and 21 papers. Stage 4 would
add HYC-0007's 10 and HYC-0024's 8.

A migration script per stage, each committed before it runs, each refusing to run
twice, each reading and writing raw CSV cells so unmodified cells are
byte-identical by construction — the pattern `scripts/migrate_v1_1.py`
established and that made its verification assertable.
