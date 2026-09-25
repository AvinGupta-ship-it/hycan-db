# Schema v1.2 — gaps found during Phase C extraction

Status: **open.** Nothing in this document has been implemented. It is the
inventory of schema limitations that Phase C extraction has hit so far, written
before any migration, in the same form as `docs/migration_v1.1_plan.md`.

Every gap below is blocking real, already-extracted, already-verifiable rows.
None of them is a hypothetical. Counts are as of 2026-09-25, after six of the
twelve Phase C papers had been read (HYC-0007, 0009, 0011, 0012, 0015, 0017);
they will grow as the remaining six are read, which is the reason this is an
inventory and not six separate migrations.

**Four of the first six Phase C papers hit at least one of these gaps.** Only
two of the six (HYC-0012, HYC-0017) could be appended without one, and HYC-0017
lost a row to gap 3.

---

## Gap 1 — No field for an uptake reported only as a bound

`uptake_wt_pct` is a float, and a row carrying an uptake must carry a numeric
one. A paper that reports "below 0.2 wt.%" therefore has two representations
available, and both are wrong: write `0.2` and a bound becomes a measurement
that will enter isotherm fits and Chahine comparisons as a point; write nothing
and the measurement disappears.

**Blocking now:** HYC-0017 at 290 K / 60 bar ("the hydrogen uptake is below 0.2
wt.% at 290 K", stated twice, no point value anywhere, no isotherm figure to
digitize). This is the paper's headline *negative* result and the reason it was
published.

**Why it matters beyond one row.** Null and bounded results are the antidote to
this literature's publication bias. A database that can record 4.2 wt% but not
"below 0.2 wt%" systematically over-represents the field's optimistic tail —
which is exactly the distortion the tiering rubric exists to correct.

**Proposed fix:** add `uptake_is_upper_bound` (boolean, default `false`). When
set, `uptake_wt_pct` holds the bound. A cross-field rule excludes flagged rows
from isotherm fitting and from headline capacity statistics, and
`src/hycan/plotting.py` renders them as downward arrows rather than points.

---

## Gap 2 — `temperature_k` and `pressure_bar` cannot express "not stated"

Schema v1.1 made temperature and pressure *conditional* — required when a row
reports an uptake, optional when it does not (§8.5 gap 3). That solved
characterization-only rows. It does not solve a paper that reports an uptake
without stating the conditions numerically.

**Blocking now:**

- **HYC-0011** (Qikun 2002). Four uptake values (0.26, 0.21, 0.22, 8.0 wt%) and
  no numeric temperature anywhere: the paper says only "room temperature". Three
  of the four have no numeric pressure either ("just greater than 1 atm", "above
  1 atm"); only one states 0.52 atm.
- **HYC-0015** (Rajaura 2016). Two uptake values (1.90, 1.34 wt%) at a stated 80
  bar, but again temperature only as "room temperature". The single "298 K" in
  the paper belongs to two cited works by other groups.
- **HYC-0009** (Ioannatos 2010), six TPD rows. Adsorption temperature is stated
  (298 K); pressure is not stated at all. The TPD runs were under flowing H2 at
  40 cm³/min, which is ambient by construction, but the paper never says so and
  §3.4's discipline forbids supplying it.

Imputing 298 K is the obvious shortcut and it is not available: "room
temperature" in a 2002 Chinese laboratory paper and in a 2016 Indian one are not
the same number, the difference matters at these uptake levels, and a database
that silently substitutes a convention has fabricated a measurement condition.

**Proposed fix:** allow `temperature_k` and `pressure_bar` to be null on an
uptake-bearing row *when* a companion flag says the paper did not state them,
rather than relaxing the requirement generally. Two booleans,
`temperature_unstated` and `pressure_unstated`, both default `false`, each
required to be `true` for the corresponding field to be null on an uptake row.
Analysis then filters on the flags instead of discovering nulls. The alternative
— free-text `temperature_as_reported` — is worse, because nothing downstream can
consume it.

---

## Gap 3 — Only one surface-area value per row, and it is named `bet_`

Two distinct problems, both live.

**3a. The field name asserts a method the paper may not claim.** `surface_area_method`
(v1.1 gap 1) records the truth, but the value still sits in a column called
`bet_surface_area_m2_g`. Four papers now do this: HYC-0005 (a total surface
area), HYC-0012 (method never stated), and HYC-0021 and HYC-0023 by inheritance.
Downstream, `src/hycan/plotting.py` and any ML feature named
`bet_surface_area_m2_g` consume all of them as if BET.

**3b. A paper can report more than one surface area, and the schema holds one.**
**Blocking now:** HYC-0007 (Takagi 2004) reports, for each of nine samples, a
*micropore* surface area (320–2250 m²/g) and an *external* surface area
(20–590 m²/g) from an αs-plot, and no total. Eighteen measured surface areas
have nowhere to go. Summing them to manufacture a total would be fabrication,
and putting the micropore value into `bet_surface_area_m2_g` is worse than the
HYC-0005 case — there the quantity was right and the method unknown; here the
quantity itself is different. So HYC-0007's rows are currently extractable only
with all eighteen values dropped to `notes`.

HYC-0004 (Nijkamp 2001) is already in the corpus with a t-plot surface area and
will want the same fields.

**Proposed fix:** rename nothing (renaming `bet_surface_area_m2_g` breaks every
consumer and every published row reference). Add
`micropore_surface_area_m2_g` and `external_surface_area_m2_g`, both optional
floats, and extend `surface_area_method` with `alpha_s_plot` and `t_plot`. Add a
cross-field check that `micropore + external` is consistent with a populated
total when all three exist. Document in `docs/data_dictionary.md` that
`bet_surface_area_m2_g` means "the paper's headline total specific surface area,
whose determination method is given by `surface_area_method`" — which is what it
has actually meant since v1.1.

---

## Gap 4 — Two reported uptake values on one row can contradict each other

`validate.py` warns when `uptake_mmol_g` and `uptake_wt_pct` disagree (the
corpus's `mmol/g and wt% inconsistent ×1`). It has no equivalent for
`uptake_ml_stp_g` versus `uptake_wt_pct`, and the conversion in
`_gravimetric_wt_pct()` silently prefers wt% when both are present.

**Blocking now:** HYC-0009 (Ioannatos 2010) tabulates both a wt% and a volume
`Vs` for every measurement, and **the two cannot be reconciled**: converting Vs
at the project's STP convention gives 0.048–0.145 wt% against a reported
0.12–0.36 wt% at 298 K, and 0.69–1.25 wt% against a reported 1.35–3.27 wt% at
77 K. The discrepancy factor is 2.0–2.6 and is not constant across rows, so it
is not a unit error with a single fix. Separately, the paper's own "H/C" column
reconciles with its wt% only if read as H2 *molecules* per carbon atom, while
the text calls it hydrogen *atoms* per carbon atom.

The fourteen volumetric HYC-0009 rows were therefore extracted with
`uptake_wt_pct` only — the paper's headline quantity, the one its abstract and
conclusions argue from — and with Vs recorded in `notes` together with the
discrepancy. Filling `uptake_ml_stp_g` would have asserted an STP basis the
paper never states *and* stored two mutually contradictory uptakes on one row.

**Proposed fix:** extend the existing consistency check to all three uptake
fields pairwise, at WARNING severity, and add the new warning type to the §11.5
baseline in the same commit that introduces it (a new warning type is otherwise
a stop condition). This is the cheapest gap to close and should go first,
because it is the one that would have caught the problem automatically instead
of relying on a verifier noticing.

---

## Gap 5 — `synthesis_method` vocabulary, again

Two Phase C papers name a route that is not in the vocabulary and is not `other`
in any informative sense:

- **HYC-0017**: "a chemical exfoliation method" from artificial graphite.
  Recorded as `other`. Mapping it to `chemical_oxidation` was rejected: the
  paper's own XPS gives C/O = 10.8–14.9, which is inconsistent with a
  graphite-oxide route (graphene oxide is C/O ≈ 2).
- **HYC-0011**: thermal decomposition of iron phthalocyanine. Recorded as
  `pyrolysis`, which is defensible; `cvd` is equally defensible and the paper
  itself uses both phrasings.

**Proposed fix:** add `chemical_exfoliation`. Leave the FePc case alone — the
existing vocabulary genuinely covers it twice over, and the ambiguity is the
paper's, not the schema's. Record the choice in `notes`, which HYC-0011's rows
do.

---

## Sequencing

Gaps 1, 2, 3b and 4 each block rows that are already extracted and verified.
Gap 4 first, because it is a validator change with no migration. Then 1, 2 and 5
together, since all three are additive columns or vocabulary values with
defaults that leave every existing row byte-identical. Then 3, which needs a
data-dictionary rewrite and touches downstream consumers.

**Do not start until all twelve Phase C papers have been read.** The reason this
is one document and not five is that v1.1 was executed as a single migration for
exactly this reason (§8.5: "All four are to be closed together, in one
migration"), and six papers remain unread. A gap found in HYC-0026 after a v1.2
migration has shipped costs a second migration.

Blocked rows, by paper, as of 2026-09-25:

| Paper | Rows extracted | Rows written | Blocked by |
| --- | --- | --- | --- |
| HYC-0007 | 10 | 0 | gap 3b (18 surface areas have no field) |
| HYC-0009 | 20 | 0 | gap 4 (14 rows), gap 2 (6 TPD rows) |
| HYC-0011 | 5 | 0 | gap 2 |
| HYC-0012 | 6 | **6** | — |
| HYC-0015 | 2 | 0 | gap 2 |
| HYC-0017 | 3 | **2** | gap 1 (1 row) |

43 rows extracted, 8 written, 35 blocked on schema rather than on evidence.
