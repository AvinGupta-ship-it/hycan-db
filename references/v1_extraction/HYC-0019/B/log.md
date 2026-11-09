# HYC-0019 extraction log (agent B, 2026-11-09)

Input: page images main-1 to main-5 only (no SI). 53 rows written. 7 samples, 8 isotherms (I1-I8).

## Sources extracted from

- Table 1 (p. 292, main-2): 12 H2 values (77 K "under 0.1 MPa" and 303 K "under 5.7 MPa" for 6 samples) -> rows M10, M11, M19, M21, M29, M30, M32, M33, M42, M44, M52, M53; S_BET, Vmic (D-R, CO2 273 K) and Boehm acidic/basic groups carried on every row of each sample.
- Table 2 (p. 293, main-3): XPS C1s component concentrations and Cox/Cgr; no H2 values; carried in `functional_groups`.
- Text p. 292 Section 2: sample preparation (litchi wood, 823 K carbonization, KOH 1:4 at 1073 K), oxidation conditions, N2 77 K BET (P/P0 0.05-0.3, Quantachrome Autosorb-1), H2 purity 99.9995%, about 200 mg, outgassing 573 K 3 h, He dead-volume determination with LaNi5 cross-check, volumetric method.
- Text p. 292 Section 3.1: AX-21 S_BET 2513 m2/g and Vmic 0.68 cm3/g cited from ref. [24] -> characterization of S4.
- Text p. 294 Section 3.3: AC "2.56 wt.% and 0.41 wt.% at 77 K 0.1 MPa and at 303 K 5.7 MPa" (same measurements as Table 1 2.554 and 0.411; not separate rows, noted on M10/M11); AX-21 "0.46 wt.% obtained at 298 K and 6 MPa ... [24]" -> row M31 with `previously reported` note.
- Fig. 3(a) (p. 294, 77 K, P in torr): 3 series x 8 markers, all digitized. Legend 303/323/373 K is the HNO3 immersion temperature; series assigned to AC-3NA-303/-323/-373 (caption "HNO3 modified ACs", text names AC-3NA-373 and AC-3NA-323, end values match Table 1). Archives fig3a_303K_AC-3NA-303.json, fig3a_323K_AC-3NA-323.json, fig3a_373K_AC-3NA-373.json.
- Fig. 3(b) (p. 294, 303 K, MPa): 3 series x 7 markers digitized; only the highest-pressure point of each used (non-77 K rule). Archives fig3b_303K_AC-3NA-303.json, fig3b_323K_AC-3NA-323.json, fig3b_373K_AC-3NA-373.json.
- Fig. 4 (p. 294, 77 K, torr): AC (10 markers, 9 digitized), AC-3NA-323 (8), AC-HPO-323 (8). Archives fig4_AC.json, fig4_AC-3NA-323.json, fig4_AC-HPO-323.json.

## Digitization details

- Axes calibrated on tick centroids found from pixel row/column profiles. Fig. 3(a): x 0 torr = 149.55 px, 800 = 552.95, check 400 = 351.54; y 0 wt% = 466.92, 3.0 = 122.2, check 1.5 = 294.35. Fig. 3(b): x 0 MPa = 171.55, 6 = 535.67, check 3 = 353.83; y 0 = 901.4, 0.5 = 537.87, check 0.2 = 756.12. Fig. 4: x 0 torr = 135.45, 800 = 548.3, check 400 = 341.9; y 0 = 1471.51, 3.0 = 1150.17, check 1.5 = 1310.95. All verification residuals below 0.15%.
- All markers are black in Fig. 3, so series were separated on copies of page 4 saved in the work directory: legends blanked (p4_fig3a_nolegend.png, p4_fig3b_nolegend.png, p4_fig4_nolegend.png); filled markers extracted with tolerance 60 and the default 3-px opening (which removes open markers); open markers extracted with tolerance 250, `--open-px 0`, on copies where the other classes were whitened (p4_fig3a_circles_only.png; p4_fig3b_circles_only.png, p4_fig3b_triangles_only.png, classified by connected-component fill and shape). Fig. 3(a) filled squares and filled triangles separated by ROI (squares above, triangles below pixel row 370, about 0.84 wt%). Extracted counts equal counted markers for every series except Fig. 4 AC (below).
- Fig. 3(a) 303 K first marker (about 65 torr) is partly hidden behind the 323 K open circle; the tool centroid (68.93 torr, 1.0456 wt%, 39 of about 81 px) is kept in M34 with confidence 3; pixel edges give a full-marker centre near 64.4 torr, 1.044 wt%.
- Fig. 4 AC second marker (about 55 torr) is hidden behind the AC-3NA-323 red circle except a 2-3 px strip of its top edge; it could not be separated as a marker (a no-opening run on that strip gives 54.35 torr, 1.076 wt% from 8 px, biased high). Not extracted; isotherm_point_count for I1 is 10.
- Fig. 4 AC-3NA-323 replots the Fig. 3(a) 323 K points (digitizations agree within 1.5 torr and 0.004 wt% at every point), so it is one run (I4); rows are taken from Fig. 3(a) and each row's notes give the Fig. 4 value.
- Triangle marker centres are the tool's pixel centroids (area centroid for filled, outline centroid for open triangles).
- `digitize_figure.py check` passed for all 9 archives against Table 1 values. For Fig. 3(a) 303 K, 323 K and Fig. 4 AC, AC-3NA-323 the check was run at the last plotted pressure because 0.1 MPa (750 torr) lies outside the plotted range; Fig. 3(b) 373K checked at its last point (5.56 MPa), others at 5.7 MPa.

## Table value / plotted point merges (rule: printed pressure within max(2%, 0.02 bar) of a plotted point)

- Merged (one row, printed value, isotherm_id): AC-3NA-373 77 K 0.696 (last point 1.0114 bar), AC-3NA-323 77 K 1.941 (0.9930 bar), AC-HPO-323 77 K 1.498 (1.0038 bar), AC-3NA-323 303 K 0.321 (57.86 bar).
- Not merged (separate table row without isotherm_id, plus digitized point): AC 77 K 2.554 (last plotted point 0.8565 bar, 2.558 wt%), AC-3NA-303 77 K 2.466 (0.9715 bar, 2.471 wt%), AC-3NA-303 303 K 0.352 (58.32 bar, 0.352 wt%), AC-3NA-373 303 K 0.086 (55.60 bar, 0.0862 wt%). In each case the value equals the plotted endpoint within 0.3% and the printed "under 0.1 MPa"/"under 5.7 MPa" looks nominal, but the paper does not say the table value is taken from the curve, so the rule was applied as written. Reconciler should decide whether these are duplicates.

## Values seen but not extracted

- Fig. 5 (p. 294, uptake vs acidic groups; not an isotherm): filled squares are the Table 1 77 K values. Open circles, legend "at 303 K, 5. MPa" (right axis), six samples: they do not coincide with the Table 1 5.7 MPa values (all plot below them), so they appear to be 303 K values at 5 MPa that the tables and text do not give; not digitized.
- Fig. 6 (p. 295, uptake vs S_BET; not an isotherm): open circles are the Table 1 77 K values of the oxidized ACs; about 10 filled squares ("Pristine ACs", two overlapping pairs) are litchi-wood ACs of S_BET about 750-3400 m2/g from the authors' earlier work [29]; their uptakes and areas are not given in tables or text; not digitized. Text p. 295: "BET surface areas of the as-prepared ACs ranged from 750 to 3400 m2/g [29]" (characterization of those samples only).
- Fig. 3(b): the 6 lower-pressure markers of each 303 K isotherm (non-77 K rule).
- Fig. 1 (CO2 pore size distributions) and Fig. 2 (XPS C1s spectra): no H2 values.
- Text p. 293: Tamon and Okazaki total acidity "0.356 equiv./kg" (not H2, other work); abstract/text ratios ("29 times", "one-third") are not uptake values.

## Coding decisions

- material_class `activated_carbon` for all; oxidation adds surface oxygen groups (recorded in `functional_groups`), not lattice heteroatoms, so not `doped_carbon` and no `dopant_element`.
- synthesis_method `chemical_activation` (abstract: "prepared by chemical activation ... using KOH"); KOH step in `activation_method`, carbonization in `material_description`.
- Vmic stored in `micropore_volume_cm3_g` with `pore_volume_method = DR`, `pore_volume_probe_gas = CO2` (only micropore volume given).
- Basis not named anywhere: `basis_stated = false`, `basis_inferred = excess` (volumetric default), `uptake_type = unspecified`. wt% convention not defined, no paired units: `unknown`/`none`.
- Degassing (573 K = 299.85 C, 3 h), about 200 mg and 99.9995% H2 applied to all rows (stated for "each measurement"). He dead-volume determination coded `calibration_described = true` only for 303 K rows: the sentence follows the 303 K/6 MPa apparatus and ends "up to 6 MPa"; 77 K rows `false` (unclear). Neither apparatus identified by make/model.
- AX-21 (S4) extracted because the paper states the value was published before ([24]); method, basis, probe gas unknown; `area_same_sample = other_paper`; lab = first author of [24], institution not printed.
- Sample order of first appearance: AC (abstract), AC-3NA-373 (abstract, described), AC-3NA-323 (Section 2 example), AX-21 (Section 3.1), then Table 1 order.
