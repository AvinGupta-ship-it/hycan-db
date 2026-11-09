# HYC-0060 extraction log (extractor B)

Paper: Zlotea et al. 2009, Round Robin test (14 laboratories) on one commercial carbon, Takeda CMS 4A. All rows are one sample (HYC-0060-S1, §11.0 "several laboratories measure one sample"); the label is `CMS 4A / participant <code as printed>`; `measuring_lab_id` is `participant <laboratory number> (HYC-0060)`, with 4a/4b and 8a/8b under laboratories 4 and 8 (two instruments each, Sect. 7 and 7.2.2). 209 rows: 115 table_direct, 88 figure_digitized, 6 text_direct. 23 isotherms (I1-I23).

## Sources extracted (one line each)
- si1 p.2, Supplementary Table 1: 51 values at 77 K (participants 1, 3, 6, 7, 8a, 8b, 11, 12, 13; 0.1-1.8 MPa). The caption says the values come from interpolated adsorption isotherms, so they are `fitted_interpolated` with the curve's isotherm_id, except 17 values that lie within 2% of a digitized plotted point (merged, `measured`, digitized point in notes).
- si1 p.4, Supplementary Table 3: 64 values at ambient temperature (participants 1, 3, 4a, 4b, 6, 7, 8b, 9, 11, 14; 0.3-7.0 MPa). These are `fitted_interpolated`, except 11 at 1.5 MPa, which merges with the digitized highest-pressure point. Per-laboratory temperatures come from main Table 1.
- main p.8 (journal p.3051), Fig. 5 (77 K, 0-2.5 MPa): every marker that could be separated was digitized, for isotherms 1, 2, 6, 7, 8b, 10, 11, 12 and 13.
- main p.7 (journal p.3050), Fig. 4 (77 K, 0-10 MPa): used only above 2.5 MPa, for isotherms 1 (squares), 2 (circles) and 3 (up-triangles).
- main p.10 (journal p.3053), Fig. 8 (ambient, 0-22 MPa): highest-pressure point of isotherms 1, 2, 3, 4b, 5, 8b, 9 and 14.
- main p.10 (journal p.3053), Fig. 9 (ambient, 0-3 MPa): highest-pressure point of isotherms 4a, 6 and 11.
- main p.7 Sect. 7.2.2: "hydrogen limiting content is 1.1 wt.%" for curves 8a and b gives one row, with no isotherm_id and no pressure stated.
- main p.7 Sect. 7.2.3: isotherm 1 "around 2.6 wt.% at 8 MPa", merged with the last Fig. 4 square.
- main p.8 Sect. 7.2.3: isotherm 12 "around 1.9 wt.% at 2 MPa", merged with the last Fig. 5 pentagon (1.961 MPa; within the 2% window by less than 0.001 MPa).
- main p.8 Sect. 7.2.4: isotherm 2, "transitory plateau at 1.25 wt.% at around 2 MPa", gives its own row (no plotted point lies within 2%). Isotherm 2, "second plateau"/"maximum uptake of 1.4 wt.% ... above 3 MPa", gives one row with pressure_unstated.
- main p.8 Sect. 7.2.4: isotherm 13 "reaching 1.4 wt.% at 1.5 MPa" is the same measurement as SI Table 1, 13 at 1.5 MPa (1.39). It is recorded once, as the table value, and the text is cited in notes.
- main p.9 Sect. 7.4.4: isotherm 5 "almost 0.7 wt.% at 6 MPa" (296 K), merged with the highest Fig. 8 hexagon (5.995 MPa).
- main p.6 (journal p.3049) Table 1: per-laboratory methodology, temperature, sample density, initial weight, weight loss, outgassing pressure, equilibrium time, temperature stability, EOS, transducer accuracy and H2 purity. It gives no uptake values.
- main p.2-3 Sect. 3.1-3.2, Sect. 6, 7.1.2, 7.1.3: supplier, BET 423 (±20) m2/g (N2, 77 K), DR micropore volume 1.7(±0.1)x10^-4 m3/kg = 0.17 cm3/g (N2), outgassing protocol (383 K 24 h, then 523 K 4 h, dynamic vacuum below 1e-3 Pa), and density/dead-volume methods.

## Digitization
- Tool: `digitize_figure.py extract --mode markers --open-px 0 --tolerance 330` with colour #000000. All figures are black-and-white, so series could be isolated only by region: one run per marker, with a square ROI around that marker (half-size 4 px in Fig. 5, 5 px for Fig. 5 diamonds and in Fig. 9, 6-7 px in Figs. 4 and 8). Each archive in `digitizations/` holds the unmodified tool output for every marker of one series, with its status (accepted, merged, or overlapped and not extracted).
- Calibration ticks (pixel centres found by scanning pixel rows and columns). Fig. 5: x 0.0 at 185, 2.5 at 556, check 1.0 at 333; y 0.0 at 414.36, 1.4 at 223, check 0.7 at 318.42. Fig. 4: x 0 at 341.66, 10 at 899.0, check 5 at 620.56; y 0.0 at 1465.87, 3.0 at 1061.24, check 1.5 at 1263.14. Fig. 8: x 0 at 361.25, 22 at 914.42, check 10 at 612.48; y 0.0 at 548.32, 0.7 at 162.60, check 0.3 at 383.31. Fig. 9: x 0.0 at 190.0, 3.0 at 524.69, check 1.5 at 357.49; y 0.00 at 1443.35, 0.20 at 1179.88, check 0.10 at 1311.26. All check-tick residuals are 0.3% or less.
- Fig. 5 has no y label above 1.4 wt%, so values above it (isotherms 1, 10, 12) are read on the linear calibration and the tool flags them as outside the axis range. Merged pairs agree with the SI tables to within 0.3-2.7% (for example 12: 1.72 printed vs 1.725 digitized at 1.0 MPa; 1.91 vs 1.917 at 1.8 MPa).
- Marker counts were checked per marker (each run yields the one marker in its ROI). `isotherm_point_count` is a minimum count of markers identified on the plot, because markers near the origin overlap across isotherms. It is left empty for 8a (I14) and for 7 at ambient temperature (I13).
- The tool archives carry status "unchecked": `digitize_figure.py check` needs a stated value inside a series' x-range, which a one-marker archive cannot cover. The merged table/plot pairs above serve as the check.

## Markers seen but not extracted (could not be separated)
- Fig. 5, below about 0.2 MPa (x 185-215 px): a solid column of overlapping markers from all eleven 77 K isotherms, including every 8a marker, the low-pressure points of 1, 2, 3, 6, 7, 8b, 10, 11, 12 and 13, and the hexagon chain of 10 below 0.31 MPa. None was extracted.
- Fig. 5, 0.25-1.5 MPa plateau band: these markers overlap and were not extracted. Isotherm 1 squares at 0.70 and 0.90 MPa (the 0.70 position was used only to merge SI Table 1, 1 at 0.7 MPa). Isotherm 11 stars at 0.3, 0.6, 0.7, 0.9 and 1.2 MPa, plus 0.5 MPa (whose position was used only to merge SI 11 at 0.5 MPa). Isotherm 7 diamonds at 0.29, 0.8 and 1.2 MPa, plus 0.5 and 1.0 MPa (positions used only to merge SI 7 at 0.5 and 1.0 MPa). Isotherm 6 down-triangles below 1.5 MPa. Isotherm 3 up-triangles at 0.61 and 1.97 MPa (the latter overlaps 6 at 1.96 MPa) and all others. Isotherm 13 asterisks at 0.4 MPa (under an 8b filled circle) and 1.4 MPa.
- Fig. 4, 2.0-2.7 MPa: a solid band of overlapping up- and down-triangles (isotherms 3 and 6) that could not be counted or separated. Also Fig. 4 circle 2 and triangle 3 at about 2.9 MPa and at about 5.2 MPa, which overlap pairwise.
- Fig. 8/9, isotherm 7 at ambient temperature: the highest-pressure point could not be identified with certainty, because the pentagons near 1.8-1.9 MPa touch asterisks of isotherm 9 and diamonds of isotherm 3. Only SI Table 3 values are extracted for this isotherm.
- Ambient isotherms below their highest-pressure point were not digitized (out of scope). So for ambient SI Table 3 values, coincidence with a plotted point was checked only against the highest-pressure point.

## Values seen but not extracted (with reason)
- Abstract: 1.40(±0.1) wt.% (77 K) and 0.07(±0.01) wt.% (ambient) at 1 MPa. These are reference values from the group-1 laboratories (consensus across laboratories), so they are not rows.
- Sect. 7.2.1: "plateau of around 1.4 (±0.1) wt.%" and "maximum hydrogen adsorbed is 1.4 wt.% at 77 K and 1 MPa" (group 1 = participants 3, 6, 7, 11), repeated in Sect. 9 as 1.4(±0.1) wt%. These are a consensus across laboratories.
- Sect. 7.4.1 and Sect. 9: 0.07(±0.01) and 0.12(±0.01) wt.% at 1 and 2 MPa, ambient (group 1 = 3, 7, 9, 11). These are a consensus across laboratories.
- Sect. 7.2.1: "recently published value (1.45 wt.%) of the hydrogen uptake in the Takeda CMS 4A material at 77 K and 2 MPa [25]". Sect. 7.4.1: "0.1 wt.% at 2 MPa ... of a Takeda CMS 4A material [25]". These are literature values from another paper (ref. 25, a different measurement of the commercial material), cited only for comparison; they are not this study's measurements, so they were not extracted. The reconciler may decide whether the "previously reported" rule should apply.
- Sect. 7.4.1: "overlapping within maximum 0.01 wt.%" is a spread, not an uptake. Sect. 7.4.3: isotherm 6 lower "by around 0.02 wt.% at 2 MPa" is a difference, not an uptake. Sect. 7.4.4: curve 2 (293 K) "shows almost no uptake" gives no number (its highest point is digitized).
- Sect. 7.2.3: participant 10's second 77 K isotherm (24 ml/min flow) is not shown and has no values.
- SI Table 1, Mean and Standard deviation rows (77 K): 1.048/0.101, 1.236/0.117, 1.305/0.137, 1.386/0.124, 1.435/0.136, 1.491/0.166, 1.548/0.225 at 0.1-1.8 MPa. These are computed across laboratories, so they are not rows.
- SI Table 3, Mean and Standard deviation rows (ambient): 0.030/0.011, 0.057/0.018, 0.073/0.020, 0.098/0.026, 0.112/0.029, 0.151/0.034, 0.237/0.051, 0.296/0.073 at 0.3-7.0 MPa. These are computed across laboratories.
- SI Tables 2 and 4 (interlaboratory consistency h, critical h, number of participants), Figs. 6 and 10 (standard deviation against pressure), and Figs. 7 and 11 (h by participant) are statistics derived across laboratories, not uptake values.
- Fig. 2 (H2O/CO2 desorption spectra and temperature profile during outgassing) and Fig. 3 (weight loss against outgassing pressure) contain no H2 uptake. Fig. 1 is SEM.
- Sect. 3.2: Grande et al. [24] values (macropore volume 3.1x10^-4 m3/kg by Hg intrusion, micropore volume 1.7x10^-4 m3/kg by CO2 at 297 K) are another paper's characterization and are not recorded in the fields.
- Sect. 7.1.3: mean sample density 1.99x10^3 kg/m3 (SD 0.38x10^3) across seven laboratories is not recorded. Per-laboratory He densities are recorded in `skeletal_density_g_cm3`, including participant 5's 0.2, which the paper calls an outlier.
- No non-carbon material was measured. Pd, LaNi5 and sea sand are mentioned only as generic calibration standards, with no values.

## Coding decisions (summary)
- material_class `other` (carbon molecular sieve); synthesis `commercial`; material_identity "Takeda Chem. Ind. Japan; carbon molecular sieve CMS 4A".
- BET 423, DR micropore 0.17 cm3/g (N2): area_same_sample `yes` (measured by the authors/organisers on the RRT material); BET range and consistency criteria not stated.
- Basis: Sect. 4.1 calls H2 adsorption "excess adsorption" without defining it. So basis_stated false, basis_inferred excess, and uptake_type excess, with the quote in basis_evidence.
- wt% convention unknown/none (no paired units). instrument_identified false for all (methodology only, no make or model).
- calibration_described true for laboratories whose He density method is given (1, 3, 5, 6, 7, 11, 12) and false otherwise. That includes 4 and 13 (carbon density assumed; 13's buoyancy correction is said to be not accurately described), and 8 and 9 (dead volume determined, method not reported).
- replicates_reported true: the same sample was measured independently by 14 laboratories. uncertainty_wt_pct is empty (no per-laboratory uncertainty).
- Degassing: 249.85 C (523 K) for 4 h, from the protocol all participants followed (preceded by 383 K for 24 h). degas_end_pressure_pa is the final outgassing pressure per laboratory from Table 1. sample_mass_mg is the initial weight before outgassing.
- extraction_confidence: 5 for tables, 4 for text, 3 for clean digitized markers, 2 for markers touching other markers or crossed by another series' line.
