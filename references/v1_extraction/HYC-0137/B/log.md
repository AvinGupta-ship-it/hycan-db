# HYC-0137 extraction log (agent B)

Paper: Deng et al. 2023, Int J Hydrogen Energy 48:21799-21813. Input: 15 main-text page images, no SI. 306 rows written.

## Sources extracted (one line each)

- Fig. 2(C), main p.5 (journal p. 21803): absolute H2 isotherms at -196 °C, 7 samples, a- (filled) and d- (open) symbols; 14 series digitized (isotherms I1-I7). 146 accepted points; 2 not written (P <= 0, see below); 15 replaced by Table 6 values.
- Fig. 2(F), main p.5: excess H2 isotherms at -196 °C, same 7 runs, 14 series digitized (I8-I14). 142 accepted points; 2 not written (P <= 0, see below); 3 replaced by text maxima.
- Table 6, main p.10 (journal p. 21808): absolute uptake at 1, 10, 30, 50 bar for 7 samples (28 values). 15 merged with Fig. 2(C) points; 13 written as separate rows without isotherm_id.
- Text, main p.11 (journal p. 21809), discussion of Fig. 11: maximum excess uptake 1.83 wt% at 5 bar (CS-700-1), 2.30 wt% at 7.72 bar (CS-1000-1), 2.17 wt% at 7.64 bar (CS-900-1), 3.94 wt% at 12.83 bar (CS-900-4). Range end points; samples identified from Fig. 11. Three merged with Fig. 2(F) points; CS-900-1 written separately (nearest digitized point 7.40 bar, outside 2%).
- Text, main p.11, and Fig. 12 (main p.11): CS-900-4 at 25 °C, "0.52 wt%" at 50 bar; merged with the highest-pressure marker of Fig. 12 (digitized 49.53 bar, 0.514 wt%). Isotherm I15.
- Table 8, main p.12 (journal p. 21810): Langmuir n = 1 capacity Qe for 7 samples, written as fitted_extrapolated rows with pressure_unstated (unit not printed; stored as wt.%, the unit of the fitted data).
- Table 3 (main p.3) and Table 4 (main p.5): activation conditions and pore structure, carried on every row of each sample. Methods text p. 21801-21802: degassing, instrument, Eqs. (1)-(3).

## Figure digitization method

- Calibration (page main-05.png). Fig. 2(C): x 0 bar at px 867.36, 50 bar at 1082.79, check 20 bar at 953.62 (residual 0.1%); y 0 wt% at px 312.38, 6 wt% at 155.0 (frame line, labelled), check 3 wt% at 233.53 (0.2%). Fig. 2(F): x 0 at 873.29, 50 at 1088.58, check 20 at 959.47; y 0 at 543.58, 6 at 379.0, check 3 at 461.0. Fig. 12 (main-11.png): x 0 at 206.34, 50 at 565.27, check 20 at 349.64; y 0 at 831.41, 0.6 at 569.28, check 0.3 at 700.34. Tick positions from pixel-column/row darkness profiles (work/tickpos.py).
- Series isolation. The 14 series per panel are 7 colours, each with filled (adsorption) and open (desorption) symbols; filled and open symbols of one colour cannot be told apart by an RGB tolerance. Each series was therefore isolated into its own image before running `digitize_figure.py extract --mode markers` on it with colour #ff0000:
  - Legends and the "(C)"/"(F)" labels were whitened (rectangles in work/classify.py).
  - Filled markers: pixels in the series hue window with high saturation (black series: dark neutral), closed 3x3 (work/classify3.py); tool run with --open-px 1 --marker-min-px 4.
  - Open markers: pixels in the series hue window with low/medium saturation, minus pixels within 1 px of a filled core of the same series, neutral grey split between d-900-4 (grey) and d-900-2 (bluish grey) by mean(B-R) per component, closed 3x3 and hole-filled (work/classify2.py); tool run with --open-px 1 --marker-min-px 7.
  - Touching markers were split by running the tool on adjacent sub-ROIs (runs named T_*).
  - Acceptance: a filled detection with >= 6 px, an open detection with >= 8 px, or a smaller one when the same point was found cleanly in the other panel (Fig. 2(C) and 2(F) are the same runs, so their pressures must coincide); in the low-pressure stack (P < ~3 bar) only points found in both panels or visually clean. Rejected detections (cross-talk between hues, fragments, merged blobs) are listed below.
  - Each archive in digitizations/ (one per series) holds every tool run used, the accepted indices, and the point list with pixel counts and flags.
- Tool checks against printed values (all passed, <= 1.2%): Table 6 at 10 and 30 bar for all 7 absolute adsorption runs, Table 6 at 50 bar for d-700-1 (Fig. 2(C)), text maxima at 5, 7.64, 7.72, 12.83 bar on the excess adsorption runs. This also confirms the colour-to-sample mapping.
- Confidence: 3 for clean markers, 2 for partly occluded markers (centroid of visible part), sub-ROI splits of overlapping markers and low-pressure-stack points.

## Marker counts and markers not separated

The low-pressure stack (P < ~3 bar; x ~ 864-880 px in Fig. 2(C), 870-886 px in Fig. 2(F)) holds the first points of all 14 series on top of each other; most of these markers are hidden and cannot be counted or separated. isotherm_point_count is therefore the number of markers identified for the run in Fig. 2(C) and 2(F) combined, a lower bound: CS-700-1 24, CS-800-1 18, CS-900-1 19, CS-1000-1 24, CS-900-2 22, CS-900-3 24, CS-900-4 30 (CS-900-4 is drawn on top and is probably near-complete). Extracted vs identified, per series, and markers seen but not extracted:

- a-700-1: C 12 extracted; the ~1.4 bar marker (extracted in F at 1.44 bar) is hidden in C. F 12 extracted; the ~40.6 bar marker is under the four-sample marker stack, not separable.
- d-700-1: C 11. F 10; the ~38 bar marker is under open circles/triangles; a 7-px detection at 0.96 bar, 1.41 wt% not confirmed in C, not extracted.
- a-800-1: C 10; a 4-px fragment at 0.03 bar, 0.55 wt% (stack) not extracted. F 7; markers at ~30.3, 35.2, 40.2 bar are under orange/green markers (40.1 bar fragment of 3 px only).
- d-800-1: C 8; a 7-px fragment at 0.12 bar, 0.27 wt% not extracted. F 3; open circles at ~13.3, 23.1, 33.2, 37.7, 42.9 bar are under open triangles (fragments of 3-5 px only).
- a-900-1: green triangles lie under the orange a-1000-1 triangles at almost every pressure. C 7 extracted; ~35.3, 40.3, 45.2 bar only as 4-5 px fragments; 1.43 bar 4-px fragment not extracted. F 8; ~35.2 and 40.3 bar only as 5-px fragments.
- d-900-1: open green triangles overlap open orange triangles (hexagram shapes). C 3 extracted; ~8.5, 28, 33, 38, 43, 50 bar only as 3-5 px fragments; 3.06 bar, 2.26 wt% (9 px) not confirmed in F, not extracted. F 5; ~8.5, 33, 37.8, 50 bar fragments only; a 9-px detection at 38.64 bar, 0.75 wt% lies off the marker position and was rejected.
- a-1000-1: C 13 and F 13 detected, including three markers at P ~ 0 (0.32, 0.60, 0.77 wt%). Four of these have digitized pressure <= 0 and were not written because pressure_bar must be > 0: C -0.0121 bar 0.317 wt% and -0.0007 bar 0.608 wt%; F -0.0176 bar 0.771 wt% and -0.0176 bar 0.599 wt% (marker centres within one pixel, 0.23 bar, of zero; flagged in the archives). A ~1.1-1.2 bar fragment (4-5 px) in both panels not extracted.
- d-1000-1: C 9, F 9; a low-pressure open triangle (C 1.95 bar 2.15 wt%; F 3.14 bar 2.30 wt%; positions disagree) not extracted.
- a-900-2: C 11, F 11; F 1.50 bar 2.45 wt% 4-px fragment not extracted.
- d-900-2: C 10, F 10; C detections at 0.83 bar 2.45 wt% and 2.33 bar 3.08 wt% are mixed grey/purple pixels in the stack, not extracted.
- a-900-3: C 13, F 13.
- d-900-3: C 10, F 11. Pale-yellow mask picked up overlaps of open green and orange triangles (C at 8.45, 10.33, 18.00, 27.98, 33.22, 37.81, 42.82 bar near 2.6-3.0 wt%; F at 13.29, 23.09, 33.00, 40.24, 42.75 bar near 0.5-2.0 wt%); these are not d-900-3 markers and were rejected. C ~5.3 bar marker only as 5-px fragment; C 1.66 bar 2.93 wt% not confirmed in F; merged stack blobs at P ~ 0 (C 41 px, F 39 px) not extracted.
- a-900-4: C 17, F 17 (1.1/1.4 bar and 3.9 bar markers split from touching neighbours). A fragment right of the 3.9 bar marker (possible ~5 bar point, partly hidden) not separable.
- d-900-4: C 12, F 13 (F 9.69 and 10.95 bar split). C ~2.0 bar marker (extracted in F) hidden; merged stack blobs (C 42 px at 0.38 bar; F 67 px at 0.42 bar) and F 0.29 bar 1.56 wt% (not confirmed in C) not extracted.
- Fig. 12: 30 markers (15 filled, 15 open; tool run on the filled series found 13 blobs, two of them double); only the highest-pressure marker extracted (protocol §9, not 77 K).

## Values seen but not extracted

- Fig. 14 (main p.12): the adsorption points of the Fig. 2(C) absolute isotherms re-plotted (same measurements, including the 50-bar point drawn as a- symbol) with Freundlich and Langmuir n = 3 curves; not digitized to avoid duplicate rows, curves are model output.
- Highest-pressure point of each run: drawn with the open (d-) symbol in Fig. 2(C)/(F) and Fig. 12 but with the a- symbol in Fig. 14; coded adsorption (paper does not say it was measured on desorption).
- Fig. 11 (bar chart, main p.11): maximum excess uptake and its pressure for all 7 samples; the values for CS-800-1, CS-900-2 and CS-900-3 are not given in text or tables and were not digitized (not an isotherm).
- Abstract, highlights, conclusions and Table 7 ("This work ... 2.53/5.32, 1 bar/50 bar"): CS-900-4 2.53 wt% at 1 bar and 5.32 wt% at 50 bar, -196 °C: same values as Table 6, not duplicated.
- Text p. 21808: relative increases (22.29%, 31.73%, 36.11%, 34.07%; 36.76%, 71.43%, 81.82%, 76.16%): derived ratios, not uptake values.
- Text p. 21810 and Fig. 15: "the amount of hydrogen adsorbed by biochar per 500 BET area is 0.23 wt%, 0.59 wt%, 0.76 wt%, 0.78 wt%" at 1, 10, 30, 50 bar: computed across samples (regression), not a row. Fig. 15 (A-D) plots Table 6 values against pore parameters (R² values only); not digitized.
- Table 9: regression coefficients a-d of uptake on graded pore volumes at 1, 10, 30, 50 bar; not uptake values.
- Table 8, not extracted: Freundlich k (1.60, 1.66, 1.82, 1.74, 2.33, 2.63, 2.60) and n; Langmuir n = 1 KL; Langmuir n = 2 component capacities Qe1/Qe2 (700-1 1.41/0.84; 800-1 1.15/1.52; 900-1 1.61/1.43; 1000-1 1.71/1.31; 900-2 2.218/2.35; 900-3 2.74/2.76; 900-4 2.61/3.09) and n = 3 Qe1/Qe2/Qe3 (700-1 0.97/1.18/149.78; 800-1 0.59/1.08/1.05; 900-1 1.31/1.24/0.82; 1000-1 1.23/0.63/1.20; 900-2 1.70/1.91/1.05; 900-3 1.14/2.37/2.09; 900-4 2.59/0.56/2.61), KL values, R², reduced chi-square: component parameters of multi-site fits, not sample capacities.
- Fig. 13 (a),(b): this work's points are the Table 6 values; other points are literature values.
- Literature values (other works, not this paper's measurements): introduction (Kizilduman 1.1 wt% at -196 °C, 30 bar; Rowlandson 1.8 wt% at 1 bar; Wang 2.4 wt% at 1 bar; Zhang 170.12 cm3/g (1.53 wt%) at 1 bar; Dogan 1.11 wt% at 30 bar; Chahine 1 wt% per 500 m2/g) and Table 7 (Takagi 2.3 wt% 1 bar; Panella 4.5 wt% 60 bar; Wang 2.4 wt% 1 bar; Rowlandson 1.8 wt% 1 bar; Dogan 1.67 wt% 30 bar; Kizilduman 1.1 wt% 30 bar; Zhang 1.53 wt% 1 bar).
- Fig. 2(A), (B), (D), (E), Figs. 3-10: N2 isotherms, TG/DTG, pore size distributions, SEM, Raman; no H2 values.

## Samples without H2 uptake (characterization only, no rows)

- Corn straw (CS-biomass): Table 1 proximate (M 9.40, A 1.30, V 71.00, FC 18.30 wt%, air-dry) and ultimate analysis (C 43.28, H 5.60, O 50.39 by difference, N 0.63, S 0.10 wt%); Table 2 XRF metals/oxides (e.g. K 2.66 wt%, K2O 2.76 wt%, Si 0.58 wt%); Table 4 BET 1.05 m2/g, A_micro 0, A_meso 1.05, V_total 0.006, V_micro 0, V_meso 0.006 cm3/g, d1/d2 20.99/16.88 nm.
- CS-char (600 °C pyrolysis char): BET 10.10, A_micro 7.23, A_meso 2.87 m2/g, V_total 0.011, V_micro 0.003, V_meso 0.008 cm3/g, d1/d2 4.36/8.99 nm.
- CS-H-char (pickled char, "H-biochar"): BET 168.46, A_micro 137.45, A_meso 31.01 m2/g, V_total 0.11, V_micro 0.06, V_meso 0.05 cm3/g, d1/d2 2.70/4.60 nm; SEM average pore size 4.17 µm (Fig. 4A, "H-600-char").
- Other characterization of the H2 samples not held in fields: H-K average/maximum micropore size (Fig. 3B; text: 0.58-0.59 nm average and 0.51-0.52 nm maximum for 700-1000 °C at 1:1; 0.76 nm and 0.63 nm for KOH/char 4, i.e. CS-900-4); micropore area/volume ratios (Fig. 3A; text 96.46-98.08%); SEM average pore sizes (CS-700-1 1.82 µm, CS-900-1 1.74 µm, CS-900-3 1.16 µm); TG/DTG peak temperatures; Raman band ratios.

## Coding decisions

- Sample numbering: S1-S7 are the seven H2 samples in the order of Table 3/Table 4 (CS-700-1, CS-800-1, CS-900-1, CS-1000-1, CS-900-2, CS-900-3, CS-900-4); samples without H2 rows were not numbered. Labels from Table 6.
- Isotherms: I1-I7 absolute (Fig. 2(C)), I8-I14 excess (Fig. 2(F)) of the same seven runs (absolute computed by the authors from the excess data, Eq. (3)); separate ids because the basis differs. I15: CS-900-4 at 25 °C (Fig. 12).
- Basis: stated (Eqs. (1)-(3) define excess and absolute; both reported side by side) for Fig. 2(C)/Table 6 (absolute) and Fig. 2(F)/Fig. 11 text (excess). The 25 °C value and the Table 8 capacities name no basis: basis_stated false, basis_inferred excess by the instrumental default (gravimetric, buoyancy term in Eq. (1)), although the Table 8 fits use data that coincide with the absolute isotherms.
- Table/text matching: Table 6 values matched to Fig. 2(C) points only within max(2%, 0.02 bar) of the printed pressure (none at 1 bar; 10 bar for CS-700-1, CS-900-1, CS-900-2; 30 bar for all but CS-700-1 (30.76 bar); 50 bar for all but CS-900-1, whose 50-bar marker is not separable in Fig. 2(C)). Unmatched values carry no isotherm_id.
- Measurement: gravimetric_microbalance (maglev balance, Eq. (1)); instrument_identified false (only "PSD-PH device", no manufacturer); calibration_described true (buoyancy term (Vsc + Vs)ρg); replicates_reported false (no uncertainty or repeat for H2; repeats stated only for TGA); measuring lab = corresponding author Yijun Zhao, Harbin Institute of Technology.
- Pore data: micropore volume by H-K (pore_volume_method HK, N2); A_meso (BET minus t-plot micropore area) stored as external_surface_area_m2_g; average_pore_diameter_nm = d1 (4V/A by BET, geometric_from_S_V), BJH d2 in notes. area_same_sample yes (N2 sorption on the final washed samples). BET range not stated.
- Synthesis: pyrolysis (corn straw at 600 °C, N2); H2SO4 pickling/washing in purification_method; KOH activation in activation_method. sample_mass_mg left empty: the 2 g in Table 3 is the activation charge, the H2 sample mass is not stated.
