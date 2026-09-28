# Corpus Audit

**Dataset:** `data/raw/measurements_v0.1.csv` — 227 rows, 23 papers, 67 columns, schema v1.3
**sha256:** `d6b67069009537955267599ab15984dabfbb03ff7ef24a39868fd772c3c67c6d`
**Audited:** 2026-09-27, at commit `d5ae9d2`
**Required by:** execution manual §18 Phase D

Every number in this document was computed from the dataset at the commit named
above. None was carried over from prose in another document. Where a figure here
disagrees with the execution manual, §6 of this audit says so explicitly.

---

## 1. What this document is for

This is the honest account of what the corpus over- and under-samples, written
before Phase D adds to it, so that the search can be aimed rather than merely
widened. It is also the document a future user of the dataset should read before
computing a mean over it.

The headline is that the corpus is larger than it is useful. 227 rows sounds like
a modelling corpus and is not one: **12 of the 23 papers contribute nothing at all
to the subset the machine-learning pipeline trains on**, and three papers
contribute two thirds of what remains.

---

## 2. The analysis funnel

The dataset deliberately holds rows that must not enter a mean, a regression, or a
Chahine comparison. Manual §12.3 defines four exclusions; they overlap, so they are
evaluated as a union rather than summed.

| Step | Rows | Papers |
| --- | ---: | ---: |
| Dataset | 227 | 23 |
| After the four §12.3 filters | 182 | 19 |
| Tier A/B only | 163 | 17 |
| `uptake_wt_pct` present (the ML target) | 151 | 16 |
| 77 K subset | 105 | 12 |
| BET present (the primary feature) | **102** | **11** |

The four exclusions, individually:

| Exclusion | Rows |
| --- | ---: |
| `measurement_mode != isothermal` | 22 |
| `uptake_bound != exact` | 4 |
| `temperature_unstated` or `pressure_unstated` | 16 |
| no uptake field populated | 12 |
| **union excluded** | **45** |

Those four counts sum to 54 against a union of 45, which is why they must never be
subtracted from 227 one at a time.

**Twelve rows pass all four filters and still carry no `uptake_wt_pct`.** A
wt%-based aggregation must drop them on the target column, not on the filters — a
`mean()` will drop them silently while a row count will not.

They are **not** a single case, and the manual's §12.3 describes only one of the two:

- **Ten HYC-0024 rows** whose only hydrogen quantity is a `volumetric_capacity_kg_m3`
  or an `adsorbed_phase_density_kg_m3`. These are genuinely non-convertible: no
  gravimetric value exists to recover, which is what the v1.3 §4a validator
  amendment was written to admit.
- **Two HYC-0020 rows** — M6 and M7 — which carry `uptake_mmol_g` of 10.09 and 8.23
  and no wt%. These are gravimetric and **do** convert, by the §10.2 factor of
  0.201588, to 2.034 and 1.659 wt%.

The distinction matters for Phase E. The HYC-0024 rows can never enter a wt%-based
figure; the two HYC-0020 rows are missing from it only because nothing has derived
their wt% yet, and `src/hycan/clean.py`'s `clean_dataset` already fills missing
uptake fields from their counterparts via `normalize`. Whether the derived value
should be written into the dataset or computed at load time is a Phase E decision
and is not made here — but a reader told "the twelve are volumetric-only" would
wrongly conclude all twelve are unrecoverable.

---

## 3. Where the corpus is thin

### 3.1 Over half the papers are invisible to the model

| Paper | Rows in corpus | Rows in modelling subset |
| --- | ---: | ---: |
| HYC-0005 | 25 | 25 |
| HYC-0023 | 23 | 23 |
| HYC-0004 | 21 | 21 |
| HYC-0016 | 14 | 7 |
| HYC-0019 | 12 | 6 |
| HYC-0021 | 6 | 6 |
| HYC-0022 | 9 | 5 |
| HYC-0013 | 7 | 3 |
| HYC-0018 | 6 | 3 |
| HYC-0001 | 4 | 2 |
| HYC-0017 | 3 | 1 |
| HYC-0002, 0007, 0009, 0011, 0012, 0015, 0020, 0024, 0025, 0026, 0027, 0029 | 97 | **0** |

**97 of 227 rows — 43% of the corpus — belong to papers that contribute nothing
to the modelling subset.** The reasons are individually legitimate: HYC-0007
reports no total surface area, HYC-0024 measures at 293 K, HYC-0029 measures a
temperature cycle rather than an isotherm, HYC-0025 and HYC-0027 measure near room
temperature. Collectively they mean the corpus's apparent size is not its
effective size, and that the row count is the wrong thing to grow.

### 3.2 Three papers are two thirds of the modelling subset

HYC-0005 (25), HYC-0023 (23) and HYC-0004 (21) supply **69 of 102 rows, 68%**.
With `GroupKFold` at K = 5 over 11 groups, the fold that holds out HYC-0005 or
HYC-0023 loses roughly a quarter of the training data, and the fold that holds out
HYC-0017 loses one row. Fold-to-fold variance will dominate the mean, which is why
§14.1 requires the standard deviation and the paper count to be reported alongside
every performance number.

### 3.3 Tier is confounded with material class, and in the modelling subset it is confounded with a single paper

Corpus-wide tier by material class:

| Material class | A | B | C | D |
| --- | ---: | ---: | ---: | ---: |
| carbide_derived_carbon | 23 | 0 | 0 | 0 |
| activated_carbon | 0 | 85 | 2 | 2 |
| reduced_graphene_oxide | 4 | 16 | 0 | 1 |
| MWCNT | 0 | 16 | 13 | 2 |
| composite | 0 | 0 | 15 | 0 |
| SWCNT | 0 | 8 | 4 | 3 |
| doped_carbon | 4 | 4 | 1 | 0 |
| graphene | 2 | 4 | 2 | 0 |
| other | 2 | 5 | 1 | 1 |
| carbon_nanofiber | 0 | 4 | 0 | 0 |
| graphene_oxide | 1 | 1 | 0 | 1 |

**All 23 carbide-derived-carbon rows are Tier A and all of them are HYC-0023.**
Within the modelling subset the confound is total: of its 32 Tier A rows, 23 are
HYC-0023 and the other 9 come from three papers. A sensitivity analysis that
compares "Tier A only" against "Tier A+B" in that subset is therefore not
measuring reporting quality; it is largely measuring one group's carbide-derived
carbons. **Report tier sensitivity with the paper composition of each tier stated,
or the result will be read as a quality effect when it is a paper effect.**

### 3.4 Material coverage is confounded with time

Rows by material family and year bin:

| Family | 95–00 | 01–05 | 06–10 | 11–15 | 16–20 | 21– |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| activated / porous | 0 | 61 | 44 | 4 | 0 | 7 |
| CNT | 3 | 9 | 28 | 0 | 0 | 6 |
| graphene-family | 0 | 0 | 3 | 21 | 8 | 0 |
| other / composite / doped | 0 | 4 | 14 | 8 | 7 | 0 |

Graphene-family rows exist only from 2006, which is real history. But there are
**zero activated-carbon rows in 2016–2020** and zero graphene rows after 2020, which
is not history — it is sampling. Figure 5 plots mean uptake by year bin split by
tier; on this corpus that figure is partly a plot of which material family happened
to be sampled in each bin. Its caption must say so.

### 3.5 Carbon nanotubes are absent from the subset that tests the Chahine rule

CNTs are 46 rows of the corpus (31 MWCNT, 15 SWCNT) and **1 row of the 102-row
modelling subset**. Every other CNT row is excluded by a condition, a measurement
mode, or a missing BET area. The corpus can say a great deal about CNTs and almost
nothing about CNTs *in the framework the analysis uses*, and no figure should imply
otherwise.

### 3.6 The 1998–2005 controversy era is a single paper

| Bin | Rows | Papers | Tiers |
| --- | ---: | ---: | --- |
| 1995–2000 | 3 | 1 | D×3 |
| 2001–2005 | 74 | 6 | B×69, C×3, D×2 |
| 2006–2010 | 89 | 7 | B×34, C×30, A×23, D×2 |
| 2011–2015 | 33 | 4 | B×21, A×7, C×5 |
| 2016–2020 | 15 | 3 | B×6, A×6, D×3 |
| 2021– | 13 | 2 | B×13 |

The first bin is three rows from HYC-0002 alone. Manual §13.1 argues that the
field's late-1990s high-uptake claims and their failed reproductions are the reason
tiering exists at all; the corpus currently represents that entire episode with one
paper. §7.4's bias guard names this as the thing an automated search will not fix
by itself, and Phase D's candidate list targets it deliberately (§5.3 below).

### 3.7 Two v1.3 pore fields are empty where the model would use them

Feature availability inside the 102 modelling rows:

| Feature | Populated |
| --- | --- |
| `bet_surface_area_m2_g` | 102 / 102 |
| `total_pore_volume_cm3_g` | 83 / 102 |
| `micropore_volume_cm3_g` | 63 / 102 |
| `average_pore_diameter_nm` | 32 / 102 |
| `ultramicropore_volume_cm3_g` | 29 / 102 (all from 2 papers) |
| `mesopore_volume_cm3_g` | **0 / 102** |
| `micropore_volume_co2_cm3_g` | **0 / 102** |

The two v1.3 pore fields are populated only where a paper stated them, and those
papers are outside the 77 K BET subset. Their value so far is interpretive rather
than predictive: they record *which quantity* the existing `micropore_volume_cm3_g`
column holds, which previously mixed DR-on-CO₂, DR-on-N₂, DFT and αs-plot values in
one column.

### 3.8 Doping is not modellable and the corpus knows it

18 doped rows across 5 papers and 2 concentration units. At the 77 K / 1 bar
benchmark there are **50 rows, of which 4 are doped, all N-doped, all HYC-0021**.
Five doped rows reach the modelling subset, from two papers. Manual §15 states that
Figure 4 as originally specified cannot be built on this, and §14.3 forbids doping
as an ML feature until Phase D supplies a doped subset at comparable conditions.
This audit confirms both from the data.

---

## 4. Where the corpus is sound

Not everything is a gap, and the Phase D search should not disturb these.

- **Provenance is complete.** Every row carries a source location, an extraction
  method and a confidence. 163 rows are `table_direct`, 49 `text_direct`, 15
  `figure_digitized`; none is the deprecated `figure_estimated`.
- **Verification is real and measured.** 12 of 23 papers were extracted under the
  dual-agent protocol (106 rows); 1211 cells verified, 43 disputed, 35 upheld, and
  every numeric cell agreed. The 11 single-reader papers are labelled as such and
  are not backfilled.
- **The Chahine test has a usable spread.** 111 rows across 12 papers carry a 77 K
  temperature, a BET area and a wt% uptake after filtering, spanning BET areas from
  7 to 3190 m²/g. That is a genuine three-order-of-magnitude lever arm for testing a
  linear scaling rule.
- **Deliberate empties are documented.** Five fields are intentionally null where
  the paper prints a number that means something else (§11.4). This is the least
  visible quality property of the dataset and the one most likely to be "fixed" by
  someone who has not read the log.

---

## 5. What Phase D should therefore buy

Ranked by how much each moves the funnel, not by how many rows it adds.

**5.1 Doped carbons measured at 77 K.** Unblocks Figure 4 and the doping feature,
both of which are currently blocked outright rather than merely weak. A paper
contributing 4 doped rows at 77 K / 1 bar from a second group is worth more than
any number of undoped rows.

**5.2 New *groups* that survive to the 77 K + BET subset.** The binding constraint
on cross-validation is 11 groups, not 102 rows. A 3-row paper from a twelfth group
improves the generalisation estimate more than a 25-row paper from an existing one.
Screen for the *combination* of a 77 K uptake and a reported BET area — Phase C.1
added two papers and moved this number by zero, because one reported no total area
and the other measured at 293 K.

**5.3 The 1998–2005 controversy literature and low-uptake results.** §7.4's bias
guard, and §3.6 above quantifies why it matters. Papers whose finding is that a
material does *not* store hydrogen establish the baseline the whole tiering rubric
is calibrated against, and schema v1.2's `uptake_bound` made them recordable where
they previously were not.

**5.4 Volumetric storage density.** Gap 10 added the fields; exactly one paper
(HYC-0024, 8 rows) populates them, so `volumetric_capacity_basis` has been
exercised by one paper's conventions only.

**5.5 Activated carbons from 2016–2020, and CNTs with a BET area**, to break the
two confounds in §3.4 and §3.5. This is the lowest-priority target and the easiest
to satisfy incidentally.

---

## 6. Disagreements with the execution manual, as found

Manual §0 requires that a false claim be corrected rather than softened, and §20
records that this project's documentation errors cluster in summary sentences. Five
were found while computing this audit. All five are stale-by-two-rows: they were
correct for the 225-row corpus and were not updated when
`docs/migration_held_rows_plan.md` added HYC-0011-M5 and HYC-0015-M3 on 2026-09-27.
The dataset is right in every case.

| Location | Manual says | Dataset says |
| --- | --- | --- |
| §12.3, Appx B.4, Appx C | 43 rows excluded; 11 characterization-only; 15 unstated-condition | **45** excluded; **12**; **16** |
| §6.1, §13.3 | tiers 36 A / 143 B / 38 C / **8 D** | 36 / 143 / 38 / **10 D** |
| §6.1 | `none` ×20; 163 `table_direct`, **47** `text_direct` | `none` ×**22**; 163 / **49** |
| §6.1 | 203 `isothermal`; 104 pipeline-v2 rows | **205**; **106** |
| §15 Fig 1, Fig 5 | MWCNT 30 rows; bins 3/73/89/33/14/13 | MWCNT **31**; bins 3/**74**/89/33/**15**/13 |

§12.3's internal arithmetic is the one worth naming separately: it states 227 in
its own funnel table while stating 43 excluded and 182 kept, and 227 − 182 = 45.
The handoff brief carried the same inconsistency forward, having updated the
characterization-only count to 12 but not the union to 45.

**A sixth manual defect is not staleness.** §12.3 states that the twelve filter
survivors lacking `uptake_wt_pct` "are HYC-0024 rows whose only hydrogen quantity is
volumetric or areal." Ten are. **Two are HYC-0020-M6 and M7, which carry
`uptake_mmol_g` of 10.09 and 8.23** — gravimetric values that convert to wt% by the
§10.2 factor. §2 above sets out why the difference matters. This claim was wrong
when it was written, not merely outdated by a later append.

### 6.2 Two errors in this document's own first draft

Recorded rather than quietly amended, per §2.4, because they are the same failure
mode §20 describes and they were caught by a checker rather than by reading:

1. §3.1 originally read "106 of 227 rows — 47%". The correct figure is 97 and 43%.
   106 is the number of dual-agent-verified rows, quoted two sections away; a
   summary sentence picked up the wrong nearby number while the table beside it was
   right.
2. §2 originally asserted that all twelve wt%-less survivors were HYC-0024, copying
   the manual's §12.3 claim instead of evaluating it. That is how the sixth defect
   above went unnoticed for two revisions of the manual.

Both were found by a script that re-derived all 68 numeric claims in this document
from the dataset and diffed them against the text. That script is the reason to
trust the other 66.

### 6.1 One finding that is not staleness

**Three characterization-only rows assert a measurement method.** Twelve rows carry
no uptake value of any kind, but only nine carry
`measurement_method = not_applicable`:

| Row | `measurement_method` |
| --- | --- |
| HYC-0018-M5 | `unknown` |
| HYC-0018-M6 | `unknown` |
| HYC-0029-M2 | `gravimetric_microbalance` |

HYC-0029-M2 is the substantive one: it names a specific instrument for a row that
records no measurement. The two HYC-0018 rows predate the `not_applicable` value
and assert only that the method is unknown, which is weaker but still asserts that
a measurement occurred.

This is the same defect class that `not_applicable` was added to
`MeasurementMethod` in v1.2 to remove, and it is adjacent to the known gap that
`MeasurementMode` has no `not_applicable` at all, so all twelve rows must also
assert `isothermal`. **It is recorded here and deliberately not fixed:** changing
`measurement_method` on existing rows edits a protected file and requires a
migration plan, and HYC-0029-M2 needs its PDF re-read to establish whether the
paper ran a gravimetric measurement on that sample and reported no value, or
characterized it only. One Agent B pass settles it.

---

## 7. Method

Computed with pandas directly against `data/raw/measurements_v0.1.csv` at commit
`d5ae9d2`. The §12.3 filter was evaluated as a boolean union and the surviving rows
counted, not derived by subtracting the individual exclusion counts. Boolean flags
were normalised from their CSV string form (`"True"` / `"true"`) before testing,
per the hazard in Appendix B.3. No figure in this document was copied from the
execution manual, the handoff brief, or any prior session's prose.
