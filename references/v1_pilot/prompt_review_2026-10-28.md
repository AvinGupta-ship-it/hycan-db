# Independent review of the v1.0 prompts, between pilot rounds 2 and 3

A reviewer agent (`claude-opus-5-5`) in a fresh context, given the prompts, the code and the pilot outputs. Kept verbatim; the README says what was changed in response. Paths refer to the working copy at the time.

The prompts are not ready to freeze. Two problems are critical: the prompts as built show extractors existing v0.1 values for about 20 papers, and reconciliation of the v0.1 papers (legacy mode) cannot match rows at all. I checked the claims below by running the code, reading the built prompts and reading the pilot outputs, except where a finding says otherwise.

## Critical

**1. The prompts break blinding for about 20 v0.1 papers.**
- **Where:** `scripts/v1_prompts.py:138-145` puts all of `schema.py` and `data_dictionary.md` into `extract.md:186` and `reconcile.md:62`.
- **Problem:** those two files name 20 v0.1 papers, mostly by first author and year, together with their values and coding decisions. In the built `extract_B.md`:
  - HYC-0024: 0.78/0.57 cm³/g on ACFC50, adsorbed density 9.26–16.34 kg/m³, Ms 6.3–11.8 kg/m³ (line 2074 on).
  - HYC-0007: areas 320–2250 and 20–590 m²/g by αs (line 2005).
  - HYC-0029: residual Co 1.02/0.16/0.09/0.15 wt%, "more than 1.0 wt%", temperature-cycle rows (lines 1833, 1884).
  - HYC-0011: 8.0 wt%, 6.3×10⁻⁶ g/cm², 9.0 mg film. HYC-0017: "below 0.2 wt% at 290 K". HYC-0026: N 0.20–15.07 wt% (lines 1831–1864).
- `paper.json` gives the agent its paper_id, first author and year, so it can link its paper to these values. B's "fresh blind extraction" of each of these papers is not blind, and neither is A's if the paper is drawn. §9 says neither agent sees any existing row, and §1 names exactly this failure in v0.1.
- **Fix:** add an Amendment 1 item letting the prompts carry a redacted copy of the two registered files: paper-specific rationale removed, every field, vocabulary, validator rule and definition unchanged, both texts hashed. The alternative is to declare these papers unblinded in advance and report them separately. **This needs your decision.**

**2. Legacy reconciliation cannot match rows.**
- **Where:** `reconcile.md:11-17` in legacy mode says match.csv applies the §9 rule.
- **Problem 1:** `v1_extract.py:90-93` takes the sample label from the text before " | " in `material_description`. None of the 521 v0.1 rows contain " | ", so every v0.1 row comes out `only_first` and every B row `only_second`.
- **Problem 2:** every v0.1 row has its v2 fields empty, so any pair that did match would report every v2 field as `differ`.
- **Effect:** every undrawn v0.1 paper would show 0% row detection. Legacy mode was never piloted; the pilot reconciler only ran dual mode, and the round-2 C directories are empty.
- **Fix:**
  - Commit a label map for the v0.1 rows (sample_id to printed label, made from the PDF before B runs) and have `match --legacy` use it.
  - Skip comparing v2 fields that are empty on the v0.1 side, and say so in INTRO_LEGACY.
  - Pilot `reconcile_legacy` on one paper before freezing.

## High

**3. The prompt's rule for values printed only in cm³(STP)/g or mmol/g contradicts the dictionary, and the cm³ case fails the validator.**
- **Problem:** `extract.md:59-63` says to leave `uptake_wt_pct` empty and code W1 / `computed_from_other_unit`. `data_dictionary.md:410` and protocol §3 say to compute W1 and store it with that source.
- For a point printed only in cm³(STP)/g, the prompt-compliant row fails `schema.py:629-634`; I confirmed this. The agent must then break either the prompt or `data_dictionary.md:426` (mmol only when printed), and A and B will not choose the same way.
- **Fix:** follow the dictionary. Store the W1 computed from the printed value, unrounded, with W1 / `computed_from_other_unit`.

**4. The validator reports every schema v2 error as "Missing required field: uptake".**
- **Where:** `src/hycan/validate.py:174-176`.
- **Problem:** an uncoded required field, a convention/source mismatch, `basis_stated=true` with no evidence, or an inferred temperature other than 77.3 all produce that same message (tested). `extract.md:168-169` and `reconcile.md:33-34` tell agents to fix every reported error, and this message sends them to the uptake columns.
- **Fix:** pass the pydantic message text through, or have both prompts also run `hycan.schema.validate_row`, which returns the real messages.

**5. `measuring_lab_id` will not agree within a paper or across papers.**
- **Where:** `extract.md:117-119` leaves the format free.
- **Pilot evidence:**
  - HYC-0047: "Fierro group, Institut Jean Lamour (IJL)" against "…(IJL), Nancy".
  - HYC-0060: "RRT participant 1 (anonymised)" against "RRT participant 1 group, anonymised NESSHY…".
- **Effect:** the field is compared exactly, so every row produces a `differ` line. Across papers, RQ1's laboratory random effect and its L−1 degrees of freedom depend on identical strings for the same laboratory, and nothing harmonizes them.
- **Fix:**
  - Use a deterministic format: the corresponding author's surname plus the first-level institution as printed in that author's affiliation, unless the paper names the measuring lab.
  - In multi-lab papers, use the lab label as printed.
  - Add a committed harmonization table before analysis as an Amendment 1 item.

**6. Reconciled rows have no identity rules and no link back to match.csv.**
- **Where:** `reconcile.md:41-48`.
- **Problem:** the prompt does not say which `measurement_id`, `sample_id`, `isotherm_id`, `extractor` or free-text fields C keeps. A and B number samples independently, so C can mix the two schemes and silently merge different samples.
- **Pilot evidence:**
  - Unmatched rows were logged with `field=""` on HYC-0046 and `field=row` on HYC-0051.
  - `second` was used both for "kept" and for "dropped".
  - The extractor field was written as "agent A…; agent B…".
- **Effect:** `v1_agreement.py:115-118` counts row decisions together with field decisions. §12 cannot assign rows to the agreed or resolved cells.
- **Fix:**
  - Matched and only_first rows keep the first extraction's IDs.
  - only_second rows take the first extraction's sample_id when the label matches; otherwise they get new numbers after its maximum.
  - Row decisions use `field=row`, with `first` and `second` defined as keep or drop.
  - Use one fixed `extractor` string.
  - Fields that are not compared come from the row whose values were kept.

## Medium

**7. File access is not confined.**
- `launcher.md:11-12` allows "files the instruction names". The built prompt names `tests/test_dataset_invariants.py` (94 HYC row references), `docs/schema_v1_2_gaps.md`, `docs/migration_v1_3_plan.md`, `docs/ai_usage_log.md` and `docs/v1_protocol.md`.
- `{REPO}` (`launcher.md:6`) is not pinned. If it is hycan-db, agents can reach `data/raw/measurements_v0.1.csv` (also the validator's default CSV), `data/digitizations/`, and `references/v1_pilot/extract/`, which holds pilot extractions of HYC-0046/47/51/60. All four are re-extracted under the frozen prompts.
- The pilot ran from `/home/claude/work/v1_tools`, which has no data, but nothing committed requires that.
- `prepare` puts A/ (text layer), B/ and C/ (PDF, later A's and B's rows) side by side. Only an instruction keeps B out of the text layer, and round 1 showed instructions alone do not hold.
- The launcher is not in SHA256SUMS.
- **Fix:**
  - Whitelist exact paths in the launcher.
  - Pin REPO to a committed tools-only tree.
  - Build each agent's inputs under a separate parent directory.
  - Hash the launcher in the freezing amendment.

**8. The unit rule conflicts with the field units.** `extract.md:56-58` forbids any conversion except pressure to bar and temperature to K, but the fields are in °C, h, Pa, mg and absolute wt%. "Temperature to kelvin" invites a K value in a °C field. In round 2, `degas_end_pressure_pa` agreed 75.7% (n=115) and `sample_mass_mg` 80.8%. **Fix:** apply the no-conversion rule to uptake values only, and convert other fields to the unit in their name.

**9. The prompt cites sections it does not contain.** `extract.md:47,58,105` cite §11.0 and §10.1, but the excerpt (`v1_prompts.py:119-127`) covers only §§3, 4, 6, 7 and 9. Agents therefore lack the gauge rule (+1.01325 bar), the kPa/Torr factors and the `duplicate_of` rule. **Fix:** add §10.1 and §11.0 to the extract and reconcile excerpts; §9 sets a minimum, not a maximum.

**10. Several rules change what is measured but are not among the Amendment 1 items.** Each needs an Amendment 1 entry or should be removed:
- `extract.md:32-35`: values averaged across samples or labs are not rows. §9 says every value in tables and text is extracted.
- `extract.md:99-102`: dynamic flowing-gas isotherms are coded `isothermal`, which puts them in the §11.0 analysis sets. Their `measurement_method` is also unspecified, so the §3 instrumental default will split A and B on basis.
- `extract.md:94-97`: a blank or empty-cell run counts for `calibration_described`. §10.1 item 7 and `data_dictionary.md:1190` require the free-volume determination or buoyancy correction.
- `extract.md:71-74`: one isotherm per branch. `data_dictionary.md:1132-1137` defines one isotherm as one instrument run, which changes §10.1 item 9.
- `extract.md:107-109`: "the paper says it was repeated" counts as replicates. §10.1 item 8 requires two independent measurements reported.
- `screen.md:31-32`: excludes on the `is_retracted` metadata flag. §6 allows title/abstract exclusion only when the title or abstract makes the code clear, and this changes N_h.
- `eligibility.md:39-40`: `duplicate_data` is narrowed to papers that say so themselves, narrower than §4.

**11. The table/figure merge rule is undefined and replaces a printed value.**
- **Where:** `extract.md:26-31`.
- **Problem:** "within the digitization uncertainty" cannot be applied by a single extractor, because that uncertainty is computed later. "At the plotted point's pressure" replaces the printed pressure with a digitized one, against §9 and §11.0.
- **Effect:** the merged row's `extraction_method` is unspecified. If it is `table_direct`, its digitized pressure is compared exactly, which creates false `differ` lines, and `figure_values` skips it.
- **Fix:** define the tolerance. Keep the printed pressure and put the digitized pressure in notes. Use `table_direct` or `text_direct` with the plotted isotherm's ID.

**12. `area_same_sample` is undefined for supplier, datasheet and cited areas** (`extract.md:92-93`). Only `yes` enters RQ1 and RQ3, and these are the commercial carbons RQ3 studies; I4 explicitly accepts a supplier value. **This needs your decision.** I recommend `other_paper` for any area the authors did not measure themselves.

**13. Single values versus isotherms are undefined.**
- **Where:** `extract.md:75-76`.
- **Problem:** the prompt does not cover a table that gives several pressures for one sample at one temperature, or an unmerged table value that belongs to a plotted isotherm. Whether a single value's `isotherm_point_count` is empty or 1 is unspecified.
- **Effect:** `v1.isotherm_key` treats each row without an isotherm ID as a one-point isotherm, which keeps it out of RQ1. Round-2 agreement on `isotherm_point_count` was 9.6%.
- **Also:** a text-only "maximum uptake of X" could be coded `measured` or `unclear` (`extract.md:81-83`).

**14. No exclusion code fits when I1 fails for other reasons.**
- **Problem:** the search phrase "adsorption of hydrogen" matches "adsorption of hydrogen sulfide", and "hydrogen spillover" matches hydrogenation catalysis. Neither fits any §4 code (`eligibility.md:35-38`), so these records reach full text. Whether TPD-only papers meet I1 is also undecided.
- `eligibility.md` lacks the Amendment 1 electrochemical wording in `screen.md:21-24`.
- **Fix:** add an Amendment 1 mapping to `no_conditions_stated`, state TPD's status, and copy the electrochemical wording into the eligibility prompt.

**15. The S1 rule leaves several points open** (`screen.md:36-41`, `stratum_tiebreak.md:15-20`). It does not say whether 77 K and ≥ 20 bar must belong to the same measurement, whether −196 °C counts, which pressure units count, or whether "maximum excess" in either word order counts. **Fix:** say "same measurement" and list these forms.

**16. `digitized_means.csv` does not match the reconcile prompt.**
- **Where:** `reconcile.md:18-19` and `v1_prompts.py:74-84` promise "1% of the axis span" for every figure point.
- **Problem:** `v1_extract.py:271-279` uses 1% of the gap between the two y-calibration ticks the extractor picked (0 and 7 wt% in pilot HYC-0047). The uncertainty, which feeds the §3 observed-maximum test, therefore depends on tick choice.
- **Missing entries:** values are written only for matched pairs that are both digitized in the same unit. Re-mapped, merged or unmatched points get nothing, and C has no rule for them.
- **Unclear units and pressure:** `value` is in the row's own unit while the uncertainty is in wt%. The mean pressure is supplied but its use is unstated.
- **No output for curve mapping:** §9's curve-to-sample mapping statistic has nowhere to be recorded.
- **Fix:**
  - Calibrate y on the lowest and highest labelled ticks, or have the code read the axis limits.
  - Give C the §9 rule for points without an entry.
  - Add `field=curve_sample_mapping` to resolutions.csv.

**17. The characterization rules contradict themselves.** `extract.md:36-38` says "for a sample with no uptake" and also "only when the sample has uptake rows". Nothing says each uptake row carries its sample's area and pore fields, which `v1.eligible_bet_area` and `reporting_items` read row by row. The v2 coding of characterization-only rows is also unspecified.

## Low

18. **match.csv description:** `reconcile.md:16-17` says identifiers, provenance and free text are not compared. In fact the paper-level identifiers, `extraction_method`, `data_location` and `measuring_lab_id` are compared exactly, and five free-text fields are compared on presence. The PDF that `prepare` copies into C/ (`v1_extract.py:469-470`) is not listed among the inputs.
19. **Duplicates and BET range:** `extract.md:126-127` gives no instruction to note "previously reported in <citation>", so republished measurements will be counted twice. The BET P/P₀ range that §9 and §11.0 require has no field; tell extractors to put it in notes.
20. **Eligibility details:**
    - `eligibility.md:44-46` says a criterion with no quote is not met, but the example at line 63 shows I5 met with an empty quote.
    - `eligibility_resolve.md` handles only disagreements on criteria, not a disagreement on the exclusion code alone.
    - `record.json` has no `is_retracted`, so `retracted` cannot be applied at full text unless the PDF says so.
21. **Output parsing:**
    - `screen.md:58` and `stratum_tiebreak.md:28` only require quoting fields that contain commas. An embedded `"` or newline breaks `build_frame.py`, and a parsing failure is not one of the §9 grounds for a rerun.
    - Require Python's csv module, empty cells left empty (no None/NA/null; pandas and `v1_extract` read those differently), and booleans spelled `true`/`false`.
    - `rows.csv` in `extract.md:168` and `reconcile.md:34` is relative to the output directory while commands run from REPO; write `<output>/rows.csv`.
22. **Curve mode:** "10 pressures equally spaced between its plotted end points" (`extract.md:140-143`) lets each extractor pick different end points, which shifts the grid and pushes low-pressure points outside the 2% match window. Define the grid.