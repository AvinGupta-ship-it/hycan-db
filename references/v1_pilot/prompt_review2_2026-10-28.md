# Second independent review, before the freeze

A reviewer agent (`claude-opus-5-5`) in a fresh context, given the revised prompts, the code, the pilot outputs and the draft of Amendment 1. Kept verbatim; the README says what was changed in response. Paths refer to the working copy at the time.

**Not ready to freeze.** There are six blocking items. B1–B4 change prompt or tool hashes. B5 and B6 are fixes to the amendment text. The tests pass (60). `scripts/v1_prompts.py --check` rebuilds the built prompts exactly. The protocol excerpt matches the registered text. No built prompt and no tools file names any v0.1 paper ID or first author. Paths are under `/home/claude/work/hycan-db/` unless shown in full.

### Blocking

**B1. The `value_kind` rule contradicts §3 and goes further than Amendment item 15.**
- `prompts/v1/roles/extract.md:109-114` codes a maximum or saturation value `measured` whenever "the paper gives the pressure". That holds even when plotted points are shown and none equals the value. §3 says `fitted_extrapolated` in that case.
- Item 15 (`/home/claude/work/r3/amendment1_draft.md:95-98`) covers only the case with no points to compare.
- The clauses overlap: a value with a stated pressure that exceeds every point is both `measured` and `fitted_extrapolated`. They also leave a gap: a value below the top point, equal to none, with no pressure.
- `reconcile.md` restates no `value_kind` rule, so C settles A/B differences by the registered §3, a different rule.
- This is the field RQ1 filters on (`value_kind = measured`).
- **Fix:** use item 15's wording, define "equals" (the merged point, or within 3% of a digitized point), and restate items 14 and 15 in `reconcile.md`.

**B2. Nothing keeps the basis coding the same across an isotherm, and `v1.py` then crashes.**
- `src/hycan/v1.py:397-400` raises an error when rows that share an `isotherm_id` differ in `basis_stated` or `basis_inferred`.
- The merge rule makes this likely. In a gravimetric paper, a table value captioned "excess" is coded `excess` because the paper names it. The digitized points of the same isotherm fall to the instrumental default, `unknown`.
- I changed one `basis_inferred` value in the round-3 C rows of HYC-0040 and got `ValueError: isotherm HYC-0040|I3 mixes bases`, which stops the computed fields for the whole dataset.
- **Fix:** add to `extract.md` and `reconcile.md`: "basis_stated, basis_evidence, basis_inferred and measurement_method are coded once per isotherm; a basis the paper names or states for any value of the isotherm applies to all its rows."

**B3. The validator still reports "Missing required field: uptake" for six kinds of error.** This leaves earlier finding 4 only partly closed.
- `src/hycan/validate.py:185-192` passes through only the five schema-v2 message prefixes.
- I tested six rows that still get the generic message:
  - an uptake row with no temperature and no `_unstated` flag;
  - a flag set while the temperature is filled in;
  - a volumetric capacity with no basis;
  - an ultramicropore volume with no cutoff;
  - a surface area with method `none`;
  - a gravimetric row with only `uptake_ml_stp_g`.
- `validate.py` is in the frozen tools MANIFEST.
- **Fix:** pass every model-level `value_error` message through.

**B4. The redaction drops registered rules, and Amendment item 22 overclaims.**
- `scripts/v1_redact_schema.py` drops dictionary paragraphs 215 and 216. Paragraph 215 says one method/probe pair per row, and "where a row's volumes differ, notes records it and these fields carry the primary". Paragraph 216 says a paper whose probe temperature deviates gets a `notes` entry.
- Item 22 says every definition is unchanged and that "the script refuses if any is lost". `check()` only verifies field names and vocabulary values.
- **Fix:** restore both rules without the paper examples (this changes the prompt hashes). Reword item 22 to say what is actually checked: `schema.py` code is identical by syntax tree, field names and vocabularies are present, and the dictionary edits are listed in `REPLACE`/`DROP`.

**B5. Reference set B as defined in item 9 cannot show the miss §5 asks about.**
- "Both screeners mark include" leaves out almost every record without an abstract. In round 2, screener B marked 26 of the 29 no-abstract records `uncertain` (`references/v1_pilot/round2/screen/screen_b.csv`). OpenAlex has no abstract for 29 of the 51 v0.1 papers.
- So recall on set B comes out too high, and the "indexed without abstract" miss reason almost disappears.
- The stated reason misreads §8, which covers only drawn records.
- **Fix:** define set B as the referenced works that both screeners did not exclude, assessed on full text with the frozen eligibility prompts. Report recall separately for records with and without an abstract. This has to be settled before set B is identified.

**B6. Item 24 claims a confinement nothing enforces, and the frozen sources are not committed.**
- Isolation rests on instructions alone. `prepare` only checks that the immediate parent directories differ.
- In round 3 every input and output sat under `/home/claude/work/r3`, so B could have reached `../../out_A`.
- The repository is on the same machine, with:
  - `data/raw/measurements_v0.1.csv`;
  - `references/v1_pilot/round3/`, which holds reconciled rows for HYC-0040 and HYC-0046, both due to be extracted again.
- Round 2 already had an agent list the tools directory against its instructions.
- `git status` shows `prompts/` and `scripts/v1_*.py` untracked and the `validate.py` change uncommitted. Neither `--check` nor `TOOLS_SHA` can be reproduced from any commit.
- **Fix:**
  - Run each agent in a container that mounts only its own paths, with the tools directory read-only. Otherwise reword item 24 to state exactly what is enforced, not "prevent a repeat".
  - Commit everything and cite the commit SHA in the amendment.

### Not blocking

These need fixing before the main run. The code fixes do not change prompt hashes.

1. **The W1 check uses a different factor from the prompt.** `check` uses 0.201588/22.414 with a relative tolerance of 1e-6 (`scripts/v1_extract.py:51, 716`). The prompt's §11.0 factor, 0.0089938, differs by 4.8×10⁻⁶ relative, so every row printed only in cm³(STP)/g fails (I tested 0.89938 against 0.899384). §9 allows no rerun for this. Raise the tolerance to 1e-5, and have code recompute W1 after C averages figure values printed in mmol/g or cm³/g.
2. **Axes in mg/g get ten times the digitization uncertainty.** For a row stored as W1 from mg/g, `_single` takes 1% of the mg/g axis span as if it were wt% (I got 0.5 instead of 0.05). That raises the §3 threshold for an observed maximum and pushes isotherms out of RQ1. Scale by 0.1 when the axis is in mg/g.
3. **Two clarifications the amendment does not declare.**
   - Tabulated values for one sample and temperature at several pressures count as one isotherm unless the paper says otherwise (`extract.md:122-125`). This lets more isotherms reach `observed_max` or `plateau`, and affects §10.1 item 9.
   - An axis with inconsistent tick labels is not digitized (`extract.md:216-219`). This narrows the §9 scope, and C is not told.
4. **v0.1 rows with no pressure never match.** 26 v0.1 uptake rows have no pressure. B uses the digitized pressure, so those pairs fail (in the pilot, 3 of 9 on HYC-0046). Either let an empty v0.1 pressure match a B row marked `pressure digitized` (do this before freezing, because the match-rule text in the prompt would change), or note in item 21 that row detection for B-only papers will read low.
5. **Rules two extractors could apply differently:**
   - which printed label to use when a sample has several (table versus legend). A mismatch leaves the whole sample unmatched, and C then keeps A's rows and drops B's without comparing fields;
   - several `(unlabelled)` samples collapse into one label;
   - a table value that is not merged but belongs to a sample and temperature that also has a plotted curve (left over from earlier finding 13);
   - figures that are not isotherms (uptake against BET area, bar charts, kinetics, cycling);
   - `material_class` for metal-decorated doped carbons (pilot κ 0.46; `synthesis_method` κ 0);
   - the curve grid's switch on whether a line "starts above zero" (item 19): lines that start near zero can get grids with no points in common;
   - under item 5, a paper that fails I1 also fails I2, so the table order gives `not_carbon`, while `eligibility.md:56-59` says `no_conditions_stated`. Assess I2 only when I1 is met.
6. **Reconciler prompt details:**
   - `reconcile.md:62-63` contradicts itself: a sample with no uptake has no uptake rows to carry its characterization;
   - in v0.1 mode, new `isotherm_id`s can collide with B's;
   - the v0.1-mode rules in `scripts/v1_prompts.py:104-109` can require a digitization uncertainty on a row whose `extraction_method` is not `figure_digitized`, which the validator rejects;
   - a pair digitized in different units gives two `digitized_means.csv` lines and no rule for choosing;
   - the figure-value rule given to C does not say the larger of the two axis spans is used.
7. `extract.md:242-244` allows opening the tools directory; the launcher forbids it.
8. RQ3 needs the same `material_identity` across papers, and "as printed" guarantees mismatches. Add a harmonization table, like the one in item 18.
9. The amendment should say three things were never piloted in their final form: the screening and eligibility prompts as revised after round 2, the extraction changes made after round 3, and the v0.1 mode, whose pilot reused B's round-1 extraction.

### The 22 earlier findings

- **Closed:** 1, 3, 5, 6, 8, 9, 10, 11, 12, 14, 15, 17 (one wording problem left, item 6), 18, 19, 20, 21.
- **Partly closed:**
  - 2: rows with no pressure (item 4);
  - 4: see B3;
  - 7: see B6;
  - 13: see item 5;
  - 16: mg/g axes, pairs in different units, and merged rows with a digitized pressure are not averaged;
  - 22: the grid switch.
- **Still fully open:** none.

### Checked and fine

- The redacted schema and the tools tree carry no v0.1 identifiers or values that I could find; I read the word-level diff in full.
- The validator reads no files.
- Amendment items 1–8, 10–14, 16–18, 20, 21 and 23 match the prompts.
- The match-rule text given to the reconciler matches the code.
