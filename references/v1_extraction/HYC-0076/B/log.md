# HYC-0076 extraction log (agent B)

239 rows, 9 samples (S1 CS-835-52, S2 CS-845-64, S3 CS-855-65, S4 CS-865-66, S5 CS-835-78, S6 CS-845-79, S7 CS-855-75, S8 CS-865-79, S9 CS-885-82), 28 isotherm IDs. No non-carbon material is measured in the paper.

## Sources extracted from

- Table 3 (main p.5): "Measured, -196 °C, 100 bar" uptake for all 9 samples (9 table_direct rows). Each is merged with the 100-bar marker of its Fig. 3 curve where that marker could be separated (8 samples). The paper says Table 3 values come from the Fig. 3 isotherms. Characterization (A_BET, Vp, V<50nm, Vmicro, V<1nm, activation T and t, BO/t) is put on every row of the sample.
- Table 3 (main p.5): "Theoretical, -123 °C, 5 bar" (Tóth-potential / Clausius-Clapeyron prediction, made by linear extrapolation below 12 bar per the Fig. S9 caption) for all 9 samples. These are 9 table_direct rows with value_kind = fitted_extrapolated. The CS-885-82 value 0.18 is merged with the Fig. S9 extrapolation marker.
- Fig. 3a and 3b (main p.6): -196 °C Hiden XEMIS isotherms up to 100 bar, digitized marker by marker (details below).
- Text, main p.6: "CS-835-78 has an uptake of 8.51 wt% at 100 bar and -196 °C" is the same value as Table 3, so it has one row (Table 3). Mesopore volumes 0.32 (CS-835-78) and 0.28 (CS-855-75) cm3/g are stored in mesopore_volume_cm3_g.
- Text, main p.7: "an uptake at 5 bar of 0.18 vs 0.58 wt%" for CS-885-82 at -123 °C. 0.58 is measured: one text_direct row merged with the Fig. S9 measured marker at 5.06 bar. 0.18 is the Table 3 theoretical value, so there is one row (Table 3).
- Sections 2.1-2.3 (main p.2-3): synthesis, activation, BET/BETSI, single-point Vp, 2D-NLDFT dual N2/H2 fit, Hiden XEMIS gravimetric method, degassing (200 °C, 4 h), He-density buoyancy correction, and the total-basis definition used as basis_evidence.
- Table S1 (SI p.2): N and O wt% (elemental analysis) for CS-835-52, CS-845-64 and CS-855-65, stored as dopant N wt% plus notes.
- Fig. S1b, S1e, S1h, S1k, S2b, S2e, S2h, S2k, S2n (SI p.3-4): Micromeritics 3Flex H2 isotherms at -196 °C, 15 markers each at p/p0 >= 0.125, giving 135 rows with uptake in cm3(STP)/g (W1 computed). The x axis is relative pressure and p0 for H2 at -196 °C is not stated, so pressure_bar is empty, pressure_unstated = true, and the digitized p/p0 is in notes.
- Fig. S8a and S8b (SI p.8): highest-pressure point of the predicted -123 °C isotherms for CS-835-52, CS-855-65, CS-865-66, CS-855-75 and CS-885-82 (5 rows, fitted_extrapolated).
- Fig. S9 (SI p.9): measured -123 °C isotherm of CS-885-82. One row for the highest-pressure point (39.72 bar, 2.798 wt%). The 5.06-bar marker was digitized only to merge with the text value 0.58. The extrapolation marker (5.03 bar, 0.189 wt%) was digitized only to merge with the Table 3 value 0.18.

## Digitization method

- The tool is digitize_figure.py extract --mode markers, run on per-series canvases in work/iso/ that keep the page's pixel grid.
- How the canvases were made (scripts in work/scripts/):
  - legend boxes were painted white on work copies of the page;
  - a colour-class mask was made for each series;
  - closing was used where another series' line cuts a ring;
  - holes were filled, so hollow markers become solid;
  - a disk opening removed the connecting lines;
  - a watershed split separated touching markers of the same series;
  - the kept components were painted pure #ff00ff.
- Every extracted set was overlaid on enlarged crops and checked by eye.
- Fig. 3a calibration:
  - x: 0 bar at px 258.56 and 100 bar at px 587.44; checked at 40 bar (px 389.88), error 0.18%.
  - y: 2 wt% at px 1384.02 and 8 wt% at px 1124.15; checked at 4 wt% (px 1296.99), error 0.23%.
- Fig. 3b calibration:
  - x: 0 at px 698.41 and 100 at px 1028.42; checked at 40 (px 829.52), error 0.68%.
  - y: same as Fig. 3a.
- Every Fig. 3 series' 100-bar point reproduces Table 3 within 0.5% (tool check passed).
- Fig. S9 calibration:
  - x: 0 at px 310.68 and 40 at px 1018.97; checked at 20 (px 664.84).
  - y: 0.5 at px 639.29 and 2.5 at px 246.32; checked at 1.5 (px 442.08).
  - The check passed against 0.58 wt% at 5 bar and 0.18 wt% at 5 bar.
- Fig. S8 calibration:
  - x for panel a: 50, 100, 150 bar at px 359.04, 477.69, 597.90.
  - x for panel b: 50, 100, 150 bar at px 795.47, 915.51, 1034.39.
  - y: 1 and 5 wt% at px 1184.14 and 851.09; checked at 3 wt% (px 1017.57).
- Fig. S1 and S2 linear panels:
  - x for S1: 0 at px 544 and 1.0 at px 755; checked at 0.4 (px 628).
  - x for S2: 0 at px 552 and 1.0 at px 754; checked at 0.4 (px 633).
  - y for S1: 0 at the frame row and 600 at 152 px above it; checked at 200.
  - y for S2: 0 at the frame row and 1000 at 173 px above it; checked at 400 (detected tick).
- Fig. S1 log-x panels were not used: the 10^-3 tick lies 0.5 px off the 10^-5 to 10^-1 calibration (3.6% at 32 px per decade), and the markers there are not separable anyway (see below).

## Fig. 3 marker counts (all markers of each run, against those extracted)

- Fig. 3a CS-835-52 (green squares): 10 extracted (10-100 bar). About 11 markers below 5 bar are hidden behind the other three series, so the count could not be completed.
- Fig. 3a CS-845-64 (blue circles): 3 extracted (80, 90, 100 bar).
  - The circles at 0-70 bar are hidden or mostly hidden behind the CS-855-65 diamonds and CS-865-66 stars, so the count could not be completed.
  - The 60 and 70 bar circles gave partial components (area below 75% of a full marker) and were rejected.
- Fig. 3a CS-855-65 (red diamonds): 21 counted, 18 isolated.
  - The 10 and 20 bar markers needed a local 5-px closing because they are partly covered by stars.
  - The markers at about 3, 4 and 5 bar overlap each other and the grey and green markers, and were not separable.
  - One marker digitized at -0.018 bar (0.879 wt%) is not a row, because a pressure at or below 0 cannot be stored.
- Fig. 3a CS-865-66 (grey stars): 21 counted, 21 extracted.
- Fig. 3b CS-835-78 (green triangles): no marker separable, because all are hidden behind the blue squares, grey diamonds and black stars. The count is unknown and only the Table 3 row exists.
- Fig. 3b CS-855-75 (blue squares): 8 extracted (30-100 bar). The markers at 0-20 bar are hidden behind the black stars.
- Fig. 3b CS-845-79 (red circles): 2 extracted (90 and 100 bar). The circles at 0-80 bar are hidden behind the grey diamonds and black stars. The 80-bar circle was partial and rejected.
- Fig. 3b CS-865-79 (grey diamonds): 7 extracted (30, 40, 60-100 bar).
  - 30, 40 and 60 bar needed a local 3-px closing.
  - The 50-bar diamond merged with a star (area +34%) and was rejected.
  - The markers at 0-20 bar are hidden.
- Fig. 3b CS-885-82 (black stars): 21 counted, 21 isolated. Two markers digitized at -0.023 bar (0.763 wt%) and -0.021 bar (1.164 wt%) are not rows, because a pressure at or below 0 cannot be stored.
- isotherm_point_count is filled only where every marker was counted: 21 for CS-855-65, CS-865-66 and CS-885-82, and 15 for the Fig. S9 measured run (the overlapping cluster below 2 bar is uncertain by about 1). It is empty elsewhere.

## Seen but not extracted

- Fig. S1 and S2 H2 isotherms (3Flex):
  - Markers at p/p0 < 0.125 in the linear panels and all markers in the log-x panels (S1a, d, g, j; S2a, d, g, j, m) were not extracted. They form dense overlapping clusters and the red dual-fit curve covers them, so they could not be separated or counted.
  - The N2 isotherms and the dual-fit curves are not H2 data.
- Fig. S9:
  - The other measured markers (2.13, 3.05, 4.06, 10.07, 20.00 and 29.82 bar, plus about 7 overlapping markers below 2 bar) were not extracted, because at other temperatures only the highest-pressure point is taken.
  - The predicted grey circles (12-38 bar) are the same predicted CS-885-82 curve as Fig. S8b, whose highest point (107.9 bar) was taken.
- Fig. S8:
  - The highest-pressure markers of CS-845-64 (S8a, hidden behind the CS-855-65 diamond) and of CS-835-78, CS-845-79 and CS-865-79 (S8b, hidden or merged) were not separable.
  - Their Table 3 5-bar values carry the predicted-curve isotherm IDs.
  - All lower-pressure predicted markers were not extracted (non-77 K rule).
- Table 3 working capacity 100-5 bar at -196 °C is a difference, not an uptake at one pressure: 1.91, 4.47, 2.91, 4.73, 2.67, 4.14, 3.22, 4.35 and 5.01 wt% (CS-835-52, CS-835-78, CS-845-64, CS-845-79, CS-855-65, CS-855-75, CS-865-66, CS-865-79, CS-885-82).
- Table 3 TPSA working capacity (100 bar at -196 °C minus 5 bar at -123 °C) is a difference: 4.71, 8.22, 6.21, 8.71, 5.94, 7.91, 6.65, 8.21 and 9.01 wt% in the same order.
- Table S2 Tóth fitting parameters on the -196 °C isotherms (n_m mol/kg, K ×10^-4 /Pa, t) were not extracted:
  - values: CS-835-52 39.3, 2.89, 0.271; CS-845-64 64.1, 2.86, 0.226; CS-835-78 166, 3.61, 0.166; CS-855-65 53.1, 1.40, 0.267; CS-855-75 119, 2.41, 0.191; CS-845-79 168, 2.45, 0.173; CS-865-66 80.6, 3.86, 0.204; CS-865-79 111, 1.28, 0.211; CS-885-82 225, 3.55, 0.155;
  - the paper presents them only as fit parameters for the Δh estimate, not as capacities;
  - five n_m values convert to more than 20 wt% (W1), so they cannot be stored under the W1 rule.
- Text values not extracted:
  - main p.7, "2.4 ± 0.2 wt% for all samples" at -196 °C and 1 bar: a value across samples.
  - main p.6-7, "the uptake at 5 bar only ranges between 3.35 and 4.19 wt% for all samples": a range across samples with no sample named, and the 5-bar values are not printed per sample.
  - main p.6, "almost 0.1 wt% H2 uptake at 5 bar" improvement, "0.2 wt% greater" (printed against "CS-855-78", which is presumably CS-855-75) and "0.33 wt%" working-capacity improvement: these are differences. The 0.33 wt% statement contradicts Table 3 (4.14 vs 4.47).
  - main p.7, "from 5.30 to 9.19 wt%" and "from 1.91 to 5.01 wt%": Table 3 values and differences already covered.
  - main p.7, measured working capacity 8.61 against predicted 9.01 wt%: differences.
  - main p.7, the 46 mbar PSA discharge pressure and the 6770 and 121 kJ/kg compression work: not uptake.
  - Abstract: 9.2 wt% at -196 °C and 100 bar is 9.19 rounded (Table 3). The 9.0 wt% TPSA and 5.0 wt% PSA working capacities are differences.
  - Conclusions: 1.9-5.0 wt% and 4.7-9.0 wt% are working-capacity ranges.
  - main p.6, "50 % of its maximum uptake at 0.75 bar" (CS-835-52) and "3.18 bar" ("CS-855-82" as printed): these are pressures, not uptakes (Fig. S6c).
- Fig. 4 (uptake and working capacity against BO and A_BET) is not an isotherm; it shows the Table 3 values.
- Fig. S6a and S6b show normalised -196 °C isotherms (no absolute uptake, lines without markers) and were not digitized. Fig. S6c and S6d show the pressure at normalised uptake 0.5.
- Fig. S7 (Δh against uptake), Fig. S3 (pore volume against BO), Fig. S4 (A_BET against BO) and Fig. 2 (N2 isotherms and PSDs) are not H2 isotherms.
- Table 1 is a comparison of storage technologies with no sorbent data.
- Samples with characterization but no H2 uptake:
  - PS polymer microspheres: A_BET 0, d_He 0.39 g/cm3, C 56.29, H 3.91, O 35.24, N 4.56 wt%.
  - CS carbonized microspheres: A_BET 540 m2/g, Vp 0.22, Vmicro 0.18 cm3/g, d_He 1.89 g/cm3, C 93.54, H 0.59, O 2.76, N 3.11 wt% (Table 2).
  - Table S1 "CS-885-72": C 94.38, H 0.32, O 2.51, N 2.79 wt%. No sample with this label has H2 data, and it was not reassigned to CS-885-82.
  - Fig. 1d: SEM of microspheres with BO 52% activated at 864 °C. The sample has no label and no H2 data.
- Printed discrepancies were kept as printed in notes:
  - the text gives V<50nm 1.33 cm3/g for CS-855-75 where Table 3 gives 1.32;
  - the text mesopore volumes 0.32 and 0.28 differ from the Table 3 differences 0.31 and 0.26.
- Coding notes:
  - Basis is coded total with basis_stated = true from the Section 2.3 definition. It is applied to the 3Flex isotherms too, because the statement covers "all isotherms", but it sits in the gravimetric section.
  - The degas end pressure is not stated; the base vacuum <1e-6 mbar is an instrument figure.
  - Sample mass is given only as "at least 50 mg".
  - H2 purity is given only as the grade BIP+.
  - The BET P/P0 range and consistency criteria are not stated (only the BETSI software is named).
