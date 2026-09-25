# Migration plan — schema v1.3 (v1.2 stage 4: gaps 3, 6, 10)

**Status:** written and committed before any protected file is touched, per
execution manual §6.7.
**Date:** 2026-09-25
**Applied by:** `scripts/migrate_v1_3.py` (committed; refuses to re-run)
**Target files:** `src/hycan/schema.py`, `src/hycan/validate.py`,
`data/raw/measurements_v0.1.csv`, `docs/data_dictionary.md`, `tests/` — and
nothing else.

Schema version: **v1.2 → v1.3**. Columns: **51 → 67** (16 new fields).

*(Corrected 2026-09-25: this line first said "17 fields, 51 → 68". 2 + 6 + 8 = 16.
The field tables in §1 were right; the summary line was not — the same class of
error three audits found in the execution manual today, in the same place, a
sentence restating a number computed correctly elsewhere. Counted from
`MeasurementEntry.model_fields`.)*

---

## 0. Scope, and why this is v1.3 rather than "stage 4"

`docs/schema_v1_2_gaps.md` inventoried ten gaps. Seven closed in v1.2 stages 1–3.
The three that remain — gap 3 (one surface-area field, named `bet_`), gap 6 (pore
fields have no method or cutoff), gap 10 (volumetric and areal capacity have no
field) — are closed here.

They are versioned v1.3 rather than as a fourth stage of v1.2 because, unlike
stages 1–3, **this migration changes existing cells.** Stages 1–3 were purely
additive with defaults that left all 156 rows valid unchanged. This one backfills
53 cells across 53 rows (§3), so it is a different kind of change and gets its own
version number and its own verification.

**What unblocks on completion:** the 20 rows held since Phase C — HYC-0007's and
HYC-0024's, plus one row each in HYC-0011 and HYC-0015. Target **~226 rows, 23
papers**.

## 1. The field list (16), and the paper that forces each one

Every field below is justified by a specific measured value in a specific paper
that currently has nowhere to go. Nothing is added speculatively. Sources: the
gap inventory, plus locate-only passes over HYC-0007 and HYC-0024 run 2026-09-25
(recorded in `docs/ai_usage_log.md`).

### Gap 3 — surface area (2 fields, 3 vocabulary values)

| Field | Type | Forced by |
| --- | --- | --- |
| `micropore_surface_area_m2_g` | float, 0–4000, optional | HYC-0007 Table 1 `Smicro`, 9 samples, 320–2250 m²/g |
| `external_surface_area_m2_g` | float, 0–4000, optional | HYC-0007 Table 1 `Sext`, 9 samples, 20–590 m²/g |

`surface_area_method` gains **`alpha_s_plot`** (HYC-0007's αs plot; HYC-0004's
t-plot area is already in the corpus and wants the next value), **`t_plot`**, and
**`not_reported`** (§3, backfill B).

**`bet_surface_area_m2_g` is not renamed.** Renaming breaks `plotting.py`, every
ML feature of that name, and every published row reference. Its documented
meaning is unchanged and is restated in the data dictionary: *the paper's headline
total specific surface area, with the method given by `surface_area_method`.*

**A definitional caveat that must go in the data dictionary.** HYC-0007 defines
S_ext as including meso- and macropore surface: *"The αs plot can provide the
information about the micropore and the external surface containing the mesopore
and macropore."* So `external_surface_area_m2_g` is **not** a geometric external
surface, and a mesopore surface area cannot be recovered from it. Any paper
reporting a genuinely geometric external area needs a note.

### Gap 6 — pore method, probe gas and cutoff (6 fields)

| Field | Type | Forced by |
| --- | --- | --- |
| `pore_volume_method` | Literal, default `unspecified` | `micropore_volume_cm3_g` currently holds DR, DFT and αs-plot volumes indistinguishably across HYC-0019, 0021, 0022, 0024, 0026, 0007 |
| `pore_volume_probe_gas` | Literal, default `unspecified` | HYC-0019 measures area by N2/77 K and micropore volume by CO2/273 K **on the same row**; HYC-0024 reports both |
| `micropore_volume_co2_cm3_g` | float, 0–2, optional | HYC-0024 Table 1 reports **two** DR micropore volumes per sample, `DR volume N2` and `DR volume CO2`, which are not interchangeable (0.78 vs 0.57 on ACFC50) |
| `mesopore_volume_cm3_g` | float, 0–3, optional | reported by several corpus papers with nowhere to go |
| `ultramicropore_cutoff_nm` | float, 0–2, optional | HYC-0005/0021 are cut at 0.7 nm, HYC-0022 at 1 nm, HYC-0024 at no stated cutoff |
| `pore_diameter_method` | Literal, default `unspecified` | `average_pore_diameter_nm` would otherwise mix BJH desorption, a DR slit width, an HK median and Stoeckli L0 |

**Vocabularies.**
`pore_volume_method`: `DR`, `DFT`, `NLDFT`, `QSDFT`, `BJH`, `HK`, `t_plot`,
`alpha_s_plot`, `other`, `unspecified`.
`pore_volume_probe_gas`: `N2`, `CO2`, `Ar`, `He`, `other`, `unspecified`.
`pore_diameter_method`: `BJH`, `DR_characteristic_energy`, `HK`, `stoeckli_L0`,
`DFT`, `geometric_from_S_V`, `other`, `unspecified`.

`geometric_from_S_V` exists for HYC-0007's `Wave`, which is **not a
pore-size-distribution model**: it is back-calculated from S_micro and V_micro
under an assumed pore geometry (*"estimated from Smicro and Vmicro by assuming a
cylinder-shaped pore"*). Recording it as BJH or DFT would misdescribe it.

**Decision — an explicit cutoff, not a second volume field.** The gap inventory
offered either. An explicit `ultramicropore_cutoff_nm` is chosen because a second
field hard-codes one more cutoff and the next paper will use 0.8 nm, and because
an explicit number lets analysis filter for comparability instead of trusting the
data dictionary. Consequence: the 29 existing rows must be backfilled to 0.7 (§3,
backfill A), and a null cutoff on a populated ultramicropore volume becomes an
error (§4).

**One method triple per row, not one per field.** `pore_volume_method` and
`pore_volume_probe_gas` describe the row's pore-volume determinations
collectively. Where a single row's volumes genuinely come from different methods,
the row's `notes` records it and `pore_volume_method` takes the primary. This is
a deliberate limit: a field triple per pore-volume field would be nine more
columns to record a distinction no corpus paper has yet made within one sample.
If one appears, that is the trigger to revisit — not now.

### Gap 10 — volumetric, areal and structural quantities (8 fields, 1 of them a flag)

| Field | Type | Forced by |
| --- | --- | --- |
| `volumetric_capacity_kg_m3` | float, 0–200, optional | HYC-0024 `Ms 10 MPa (kg/m3)`, 5 samples, 6.3–11.8; HYC-0022's 43.2 g/L |
| `volumetric_capacity_basis` | Literal or null | HYC-0024's Ms is per **tank** volume; its other density is per **micropore** volume |
| `volumetric_capacity_includes_compressed_gas` | bool, default False | HYC-0024's Ms explicitly includes compressed H2; its adsorbed density explicitly does not |
| `adsorbed_phase_density_kg_m3` | float, 0–200, optional | HYC-0024 `hydrogen adsorbed density (10 MPa) (kg/m3)`, 8 samples, 9.26–16.34 |
| `packing_density_g_cm3` | float, 0–5, optional | HYC-0024 Table 1, 5 samples, 0.72–1.22 |
| `skeletal_density_g_cm3` | float, 0–5, optional | HYC-0024 `helium density`, 8 samples, 1.70–1.95 |
| `areal_uptake_g_cm2` | float ≥ 0, optional | HYC-0011's 6.3×10⁻⁶ g/cm², the quantity that makes its 8.0 wt% claim checkable |
| `interlayer_spacing_nm` | float ≥ 0, optional | HYC-0015's held row |

`volumetric_capacity_basis`: `micropore_volume`, `total_pore_volume`,
`packing_volume`, `tank_volume`, `other`.

**Two volumetric fields, not one with a basis flag.** HYC-0024 reports *both*
quantities for the same sample at the same conditions: an adsorbed-phase density
per micropore volume excluding compressed gas, and Ms per tank volume including
it. One field plus a basis flag cannot hold both, and choosing one would discard a
primary-table measurement. `adsorbed_phase_density_kg_m3` is the adsorbed-phase
quantity; `volumetric_capacity_kg_m3` is the system-level one that the basis flag
and the compressed-gas flag qualify.

**`skeletal_density_g_cm3` is load-bearing, not decorative.** HYC-0024 uses its
helium density to subtract the compressed-gas contribution from the measured
weight increase: *"the amount of hydrogen adsorbed is calculated using the weight
of sample, the helium density of the carbon material, and the volume of the sample
cell."* Without it the excess/absolute basis of that paper's numbers cannot be
reconstructed by a downstream user.

## 2. What is deliberately NOT added

- **A mesopore surface area field.** No corpus paper reports one; HYC-0007 folds
  mesopore surface into S_ext by its own definition.
- **A per-field method triple** for total, ultramicropore and mesopore volume.
  See §1. Nine columns for an unobserved distinction.
- **`pore_volume_probe_temperature_k`.** N2 physisorption is 77 K and CO2 is
  273 K throughout the corpus, so the probe gas already carries the temperature. A
  paper that deviates gets a note, and that is the trigger to add the field.
- **A computed wt% for HYC-0024.** Its wt% values exist only in Figure 2. A wt%
  could be derived as adsorbed density × micropore volume, but the paper does not
  say **which** of its two micropore volumes is the basis, so the result would be
  this project's arithmetic presented as the paper's measurement. §3.4 forbids it
  and §3.9 forbids the silent conversion. HYC-0024's rows therefore carry
  volumetric uptake and no gravimetric uptake, which is what the paper reports.

## 3. Backfills — 53 cells across 53 rows

This migration changes existing cells. Each backfill is enumerated, sourced, and
verified separately.

**Backfill A — `ultramicropore_cutoff_nm = 0.7` on 29 rows.**
HYC-0005 (25 rows) and HYC-0021 (4 rows) are the only rows with a populated
`ultramicropore_volume_cm3_g`. Both papers' values are cut at 0.7 nm, which is
what `docs/data_dictionary.md` has documented for the field since v1.1. The
backfill moves that fact from documentation into the data, where the new §4 check
can enforce it.

**Backfill B — `surface_area_method`: `unspecified` → `not_reported` on 16 rows.**
HYC-0016 ×2 (M13, M14), HYC-0022 ×2, HYC-0029 ×12. Each has a null
`bet_surface_area_m2_g` in a paper that reports surface areas for its *other*
samples. `unspecified` means "reported without a stated method" and is wrong for
these; `none` is reserved for papers reporting none at all. This is the
conflation gap 3 named.

**Backfill C — `surface_area_method`: `unspecified` → `none` on 8 rows.**
HYC-0002 ×3 and HYC-0027 ×5. These rows carry the schema *default* rather than a
considered value, and both papers report no surface area anywhere. **Verified
against the sources rather than inferred from the empty cells**, by two
independent locate passes on 2026-09-25:

- HYC-0002 (Liu 1999, *Science*): no numeric surface area of any kind. The word
  "area" does not occur in the paper. Characterization is HRSEM, HRTEM (mean tube
  diameter 1.85 ± 0.05 nm), Raman, TGA (≈40 wt% catalyst residue) and GC-MS.
- HYC-0027 (Parambhath 2012, *Langmuir*): no numeric surface area. Surface area
  appears five times, all qualitative. The Characterization section lists Raman,
  XRD, FESEM, TEM, XPS and a Sieverts apparatus — **no gas-sorption analyser** —
  and the Supporting Information contents list names none either.

This backfill is not in the gap inventory. It was found while mapping backfill
B's scope, and it is included because it makes `unspecified` mean exactly one
thing, which is what lets §4's new check exist at all.

**After all three backfills, `surface_area_method` partitions cleanly:**
`unspecified` (31 rows) always has an area value; `none` (20) and `not_reported`
(16) never do. That is a checkable invariant, and §4 checks it.

## 4. New validation rules

**Errors** — a row that violates one is invalid:

1. `ultramicropore_volume_cm3_g` populated while `ultramicropore_cutoff_nm` is
   null. The field exists to be comparable across the corpus; an unstated cutoff
   destroys that, which is exactly why HYC-0022's and HYC-0024's values were held
   out rather than mixed in.
2. `volumetric_capacity_kg_m3` populated while `volumetric_capacity_basis` is
   null. A volumetric capacity with no stated basis is not interpretable — per
   pore volume and per tank volume differ by more than a factor of two in
   HYC-0024's own table.
3. `surface_area_method` in {`none`, `not_reported`} while any of
   `bet_surface_area_m2_g`, `langmuir_surface_area_m2_g`,
   `micropore_surface_area_m2_g`, `external_surface_area_m2_g` is populated.
4. `surface_area_method == "unspecified"` while all four surface-area fields are
   null. This is the invariant backfills B and C create; without the check it
   would decay on the next append.

**Warnings** — flagged, not rejected:

5. `micropore_surface_area_m2_g` + `external_surface_area_m2_g` inconsistent with
   a populated `bet_surface_area_m2_g`, when all three exist. Tolerance is
   **relative AND absolute: 10% and 50 m²/g, both must be exceeded.** Relative-only
   was the false positive that produced v1.2's removed warning type (§11.2);
   HYC-0007 rounds its areas to the nearest 10 m²/g, so an absolute floor is
   required. No corpus row currently has all three populated, so this check
   cannot fire today — confirmed before writing it.
6. Pore nesting extended: `mesopore_volume_cm3_g` + `micropore_volume_cm3_g`
   must not exceed `total_pore_volume_cm3_g` beyond tolerance.

## 4a. Amendment — an existing validator blocks gap 10, and it has to change

**Found while implementing, not while planning. Recorded here rather than done
silently.**

`schema.py`'s `at_least_one_uptake` validator currently reads:

> When uptake is reported, at least one of the two gravimetric fields must carry
> it, **so that a volumetric-only row cannot enter** without a value the analysis
> can use directly.

That rule rejects every HYC-0024 row. Its only tabulated hydrogen quantities are
volumetric, and §2 forbids computing a wt% from them. So gap 10 cannot be closed
without amending the rule — adding the fields is not sufficient.

**The rule was right when written and is wrong now.** It dates from v1.0, when the
schema's only volumetric-looking field was `uptake_ml_stp_g` — gas volume per gram,
which *is* convertible to wt% through `normalize.ml_stp_per_g_to_wt_pct`. There was
no non-convertible quantity in the schema, so "volumetric-only" meant "a row that
declined to do an arithmetic conversion it could have done." `volumetric_capacity_kg_m3`
is a different kind of thing: H2 mass per unit *volume of tank or pore*, convertible
to a gravimetric figure only with a density the paper may not state.

**The fix.** Split the uptake fields in two:

- **Gravimetric-convertible:** `uptake_wt_pct`, `uptake_mmol_g`, `uptake_ml_stp_g`.
  If any of these is populated, at least one of wt% or mmol/g must be — the
  original rule, unchanged, for the case it was written for.
- **Non-convertible:** `volumetric_capacity_kg_m3`, `adsorbed_phase_density_kg_m3`,
  `areal_uptake_g_cm2`. A row carrying only these **is** an uptake row: its
  conditions are required (HYC-0024 states 293 K and 10 MPa) and it counts as
  reporting uptake, so it is not misfiled as characterization-only.

`_reports_uptake()` covers both sets, so the §4 conditions rule applies unchanged.

**The risk this creates, and the guard.** A row with volumetric uptake and no wt%
passes a "has any uptake" filter and then contributes nothing to a gravimetric
mean — `pandas` drops the null silently. This is the §12.3 failure mode exactly.
Two mitigations: the analysis filter keys on `uptake_wt_pct` for gravimetric work,
which §12.3 already does; and `tests/test_dataset_invariants.py` **enumerates by
measurement_id** every row whose uptake is non-convertible, the way it already
enumerates bounded uptakes, so such a row cannot appear without a deliberate test
change. Manual §12.3's exclusion table gains this category.

## 5. Method and verification

Per §6.7 and the v1.1/v1.2 precedent:

- **Raw CSV cells via the `csv` module, not a pandas round-trip**, so every cell
  the migration does not name is byte-identical by construction.
- **Byte-level line comparison** for every line outside the backfill scope, not
  only a cell comparison. `paper_tracking.csv`'s migration earlier today passed
  its cell check while rewriting all 31 lines' bytes, because the file was CRLF
  and `csv.writer` wrote LF. `measurements_v0.1.csv` must be checked the same
  way: detect its terminator and final-newline state, reproduce them, and compare
  raw lines.
- **Refuses to re-run**, `--dry-run`, backs up to `/tmp` with a dated name.
- **`--expected-rows` and `--expected-changed-cells` as CLI options**, not
  constants, so the script is testable against a fixture.

Post-conditions, asserted by the script and independently by
`tests/test_schema_v1_3.py`:

1. Row count unchanged at **206**. Column count **51 → 67**. Physical line count
   unchanged.
2. Exactly **53 cells changed**, all in `ultramicropore_cutoff_nm` (29, a new
   column) and `surface_area_method` (24). Columns 1–51 otherwise byte-identical;
   the 16 new columns appended at physical positions 52–67.
3. Zero validation errors. Warning baseline unchanged: `Unspecified uptake_type`
   ×183 and `Pre-2005 raw-CNT high uptake (Tier D)` ×1, and **no new type**.
4. `surface_area_method` partitions as §3 states: 31 `unspecified` all with an
   area, 20 `none` and 16 `not_reported` all without.
5. All 29 rows with an ultramicropore volume have cutoff 0.7.
6. `docs/data_dictionary.md` documents all 16 fields **in this commit** — §8.7,
   which the v1.2 commit violated by shipping eleven fields without it.

## 6. A scope finding that is not a schema gap

**HYC-0007 contains two non-carbon samples.** H-YZ and H-ZSM-5 are zeolites.
§7.2 requires a carbon-based sorbent, so both are **excluded** from the corpus and
the exclusion is recorded in `references/paper_tracking.csv`'s notes and in the
execution log. Seven of its nine samples are carbon: SWCNT, A-SWCNT, four ACFs and
O-ACF-1000. The LaNi5 in its §2.2 is an apparatus-validation standard, not a
sample, and is excluded too.

This does not change the field list — HYC-0007's carbon samples need
`micropore_surface_area_m2_g` and `external_surface_area_m2_g` regardless — but it
changes the expected row count for that paper and must not be discovered during
the append.

## 7. Sequencing

1. This plan, committed. ✅ (the §6.7 gate)
2. `schema.py`: 16 fields, 3 vocabulary values, 4 new Literals, the §4 error
   rules in the model validator.
3. `validate.py`: the §4 warnings.
4. `docs/data_dictionary.md`: all 16 fields, with the S_ext caveat and the
   cutoff-comparability note.
5. `tests/test_schema_v1_3.py`: gap by gap, each guard carrying a `MUTATION:`
   marker naming what it would catch — and each mutation actually run.
6. `scripts/migrate_v1_3.py` + its tests. Applied. Dataset re-read from disk and
   re-verified.
7. `tests/test_dataset_invariants.py`: column count 51 → 67 with positions 52–67
   enumerated, plus the §3 partition and cutoff invariants.
8. Revalidate, full suite, ruff. Commit. Then the held rows (a separate commit,
   under the dual-agent protocol).
