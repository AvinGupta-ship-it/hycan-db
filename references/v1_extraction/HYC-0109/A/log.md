# HYC-0109 extraction log (agent A)

Rows written: 99 (rows.csv). Validator (`validate_row_detail.py --errors-only`): no errors; only the expected "Unspecified uptake_type" warnings on 12 Table 1 / text rows.

## Extracted from

- Table 1 (main.pdf p.3, journal p.2): 12 rows, M1-M12. Every printed value, one row per value; ranges (1.0-1.1, 4.2-4.6, 7.8-9.1, 45-53, 0.9-1.1, 5.2-5.7) as one row per printed endpoint with the g l-1 endpoint paired in the same order (pairing is an assumption). g l-1 stored as volumetric_capacity_kg_m3, basis other. M5 is merged with a Figure 1 point (see below).
- Text, Section 1 Introduction last paragraph (main.pdf p.3) and Section 8 Conclusions (p.10): "up to 100 g H2/kg (90 bar, 83 K) and 20 g H2/kg (90 bar, 303 K)": 2 rows, M13 (20 g/kg, merged with a Figure 1 point) and M14 (100 g/kg). The two statements are repeated verbatim in the Conclusions, one row each for both passages.
- Figure 1 top-left (S-33/k excess, main-04.png): 77 K adsorption 18 rows and 77 K desorption 10 rows (M15-M42), 293 K highest-pressure point 1 row (M43). Calibration x 322.18 px = 0 bar, 555.0 px = 20 bar (verify 10 bar, 0.35%); y 375.22 px = 0, 156.0 px = 60 g/kg (verify 30, 0.36%).
- Figure 1 top-right (Batch 5.1 excess): 83 K highest separable point (desorption, 80.23 bar) M44 and 303 K highest separable point (desorption, 89.82 bar) M45. Calibration x 696.3 px = 0, 906.0 px = 80 bar (verify 40, 0.14%); y 371.87 px = 0, 180.0 px = 50 g/kg (verify 20 g/kg, 1.14%).
- Figure 1 bottom-left (S-33/k total stored): 77 K adsorption 18 rows and desorption 10 rows (M46-M73), 293 K highest-pressure point 1 row (M74). Calibration y 668.43 px = 0, 450.0 px = 70 g/kg (verify 30, 0.20%); x as top-left.
- Figure 1 bottom-right (Batch 5.1 total stored): 83 K highest separable point (desorption, 80.22 bar) M75; the 303 K stored points are the two merged rows M5 (adsorption, 80 bar) and M13 (desorption, 90 bar). Calibration y 661.0 px = 0, 449.0 px = 100 g/kg (verify 40, 0.24%); x as top-right. Archive checks passed against the printed values: stored adsorption at 80 bar (printed 1.8 wt% = 18 g/kg, digitized 17.66, 1.9%) and stored desorption at 89.89 bar (printed 20 g/kg, digitized 19.97, 0.14%).
- Figure 5 left (S-33/k absolute 77 K, cyan stars "experimental data", main-06.png): 20 rows, M76-M95. Calibration x 326 px = 0, 551 px = 20 bar (verify 10, 0.44%); y 405 px = 0, 166 px = 100 g/kg (verify 40, 0.42%).
- Figure 5 right (S-33/k absolute, panel titled 298 K): highest-pressure point, 1 row, M96. Calibration x 678 px = 0, 904 px = 20 bar (verify 10, 0.0%); y 405 px = 0, 166 px = 6 g/kg (verify 3, 0.0%).
- Figure 7 top-left (S-33/k absolute 293 K, main-08.png): highest-pressure point, 1 row, M97. Calibration x 330 px = 0, 563 px = 20 bar (verify 10, 0.43%); y 375 px = 0, 180 px = 60 g/kg (verify 40, 0.0%).
- Figure 7 top-right (Batch 5.1 absolute 83 K and 303 K): highest-pressure point of each, 2 rows, M98 and M99. Calibration x 689 px = 0, 898 px = 80 bar (verify 40, 0.48%); y 375 px = 0, 206 px = 60 g/kg (verify 40, 0.30%).
- Table 5 (main.pdf p.9) and Section 7 text: sample characterization carried on every row (BET, NLDFT total pore volume, pore volume <10 A as ultramicropore volume with cutoff 1.0 nm, pore width mode, BET range 0.01-0.03 p/p0); no H2 uptake in it.
- Section 2 and Section 3 text: H2 purity 99.999%, instruments, equation (1), apparent and skeletal densities, definitions of excess, absolute and total stored (basis evidence).

## Merges of a table or text value with a plotted point

- M5 (Table 1, Batch 5.1, Hiden HTP1, 303 K, 80 bar, 1.8 wt%, 7.6 g l-1) = Figure 1 bottom-right total-stored adsorption triangle at 80.2488 bar, 17.7092 g/kg (printed 80 bar within 2%; value 1.8 wt% matches the stored value and not the excess value 6.06 g/kg at 80.26 bar). Isotherm I1, basis total. Archive B51_303K_stored_ads.json.
- M13 (text, 20 g/kg at 90 bar, 303 K) = Figure 1 bottom-right total-stored desorption triangle at 89.8989 bar, 19.9727 g/kg. Isotherm I1, branch desorption. Archive B51_303K_stored_des.json. Sample not named in the sentence: Batch 5.1 assumed (only sample reaching 90 bar).
- No other table or text value lies within the larger of 2% and 0.02 bar of a plotted point of the same sample and temperature: Batch 5.1 83 K, 50 bar (nearest plotted 47.77 and 51.96 bar); Batch 5.1 303 K, 50 bar (nearest 48.94 and 51.43 bar, 2.1% and 2.9% away); 100 g/kg at 90 bar, 83 K (83 K isotherm ends near 80.5 bar); every S-33/k Table 1 value is at 50 or 80 bar and the S-33/k isotherms end at about 20 bar.

## Values seen but not extracted

- Abstract: "~80 g H2/kg carbon, ~50 g H2/liter carbon, at 50 bar and 77 K": sample not named, rounded restatement of the S-33/k Table 1 values (7.8-9.1 wt%, 45-53 g l-1); no row (a row would need a guessed sample and laboratory). Reconciler may add it as an approximate value.
- Figure 1 S-33/k 77 K, markers clipped by the y-axis frame, not extracted because the centroid of the visible part biases the pressure: three adsorption squares at about 0.04-0.11 bar in the excess panel (digitized y 7.59, 3.48, 10.87 g/kg, pixel x 324.5, 324.5, 325.0) and in the stored panel (digitized y 7.51, 3.34, 10.87 g/kg), and one desorption circle at about 0.2 bar (excess y 16.87, stored y 17.03 g/kg, pixel x 326.1-326.2). They are counted in isotherm_point_count.
- Figure 1 S-33/k 77 K, two adsorption squares at about 0.2 and 0.4 bar are hidden behind desorption circles (excess panel circles at digitized 0.34/16.87 and 0.49/22.62; stored panel 0.34/17.03 and 0.50/22.75) and cannot be separated; counted in isotherm_point_count (23 adsorption squares = 18 extracted + 3 clipped + 2 hidden; the Figure 5 left isotherm shows 23 stars).
- Figure 1 Batch 5.1 (83 K and 303 K): every point except the highest separable one, by scope (not 77 K). The adsorption endpoint of the 83 K isotherms at about 80.7 bar is hidden behind the last desorption circle, and the adsorption endpoint of the 303 K isotherms at about 90.5 bar is hidden behind the last orange triangle; they cannot be separated, so the desorption marker is the highest separable point. The 303 K excess and stored adsorption points at 80.26 bar are not extracted separately except M5 (stored), by scope.
- Figure 1 S-33/k 293 K: every point except the highest-pressure one (19.92 bar), by scope; a red adsorption triangle at about 0.2 bar is hidden behind the first orange triangle.
- Figure 5 left (S-33/k 77 K): three cyan stars at 0.04, 0.07 and 0.11 bar (digitized y 8.16, 3.89, 11.42 g/kg; pixel counts 8-10, at the y-axis frame and overlapped by simulation symbols) not extracted; counted in isotherm_point_count.
- Figure 5 simulation points (slit thickness 6.7, 10.1, 13.5 A; computed, not measured), Figure 6 (theoretical Langmuir isotherms), Figure 3, 4 and 8 (simulation and kinetics): not measurements.
- Figure 7 top-left 77 K squares: same isotherm as Figure 5 left, comparison only, not digitized again. Figure 7 bottom row (two-binding-energy fits): same points as the top row. Fit lines in Figure 7 are model curves, not extracted. Figure 7 293 K, 303 K and 83 K series: only the highest-pressure point (not 77 K); the fit lines split many markers.
- Table 2 (area per site, A2, from S-33/k extrapolated to 47 bar), Table 3 (binding energies, site fractions), Table 4 (adsorption and desorption times): not H2 uptake values. Sigma = 2100 m2/g (simulation conversion) and the NLDFT surface areas 3200 and 2200 m2/g: not stored (one surface-area method per row; BET stored).
- No value for a non-carbon material and no mean or consensus value across laboratories is given in the paper.

## Marker counts (isotherm_point_count, lower bounds where markers overlap)

- I2/I6 (S-33/k 77 K excess, stored): 34 = 23 adsorption squares + 11 desorption circles.
- I3/I7 (S-33/k 293 K excess, stored): 29 = 19 adsorption triangles (18 visible + 1 hidden) + 10 desorption triangles; I11 and I10 (absolute): 19.
- I4/I8 (Batch 5.1 83 K excess, stored): 36 = 17 adsorption squares (counted on Figure 7) + 19 desorption circles (ring-template count on Figure 1; only 10 are separable by the digitizer because of overlap).
- I1/I5 (Batch 5.1 303 K stored, excess): 29 = 15 adsorption triangles (counted on Figure 7, lower bound) + 14 desorption triangles (13 detected, the first detection holds two overlapping markers); I13 (absolute): 15.
- I12 (Batch 5.1 83 K absolute): 17. I9 (S-33/k 77 K absolute): 23.

## Legend markers present in the archives (excluded from rows)

- S33k_77K_excess_ads.json (386.5, 259.5); S33k_77K_excess_des.json (386.6, 280.3); S33k_77K_stored_ads.json (397.5, 554.5); S33k_77K_stored_des.json (397.5, 575.6).
- B51_83K_excess_ads.json (763.5, 256.5); B51_83K_excess_des.json (763.4, 277.4); B51_83K_stored_ads.json (808.5, 541.0); B51_83K_stored_des.json (808.4, 561.9); B51_83K_absolute_ads_fig7.json (752.0, 276.0).
- S33k_77K_absolute_ads_fig5.json (441.5, 383.5); S33k_298K_absolute_ads_fig5.json (702.5, 230.5).
- The Batch 5.1 83 K archives also hold split or duplicate fragments of squares at the y-axis and behind circles; only the highest-pressure marker of each is used. All archives have status unchecked except B51_303K_stored_ads.json and B51_303K_stored_des.json (passed).

## Discrepancies and judgement calls

- Basis of Table 1 and of the text values: the paper never says whether they are excess or total stored. The Table 1 values (and the 20 g/kg) agree numerically with the total-stored curves of Figure 1, not the excess curves (303 K, 80 bar: 1.8 wt% vs stored 17.7 and excess 6.1 g/kg; 83 K, 50 bar: 7.0 wt% vs stored about 72 g/kg; 303 K, 50 bar: 1.1 wt% vs stored 11.5-11.8 g/kg). Coded unspecified / unknown on the unmerged rows; the merged rows M5 and M13 take the stored isotherm basis.
- Stored (total) and absolute isotherms (Figure 1 bottom, Figure 5, Figure 7) are derived by the authors from the measured excess isotherm with equations (1) and (3); they are extracted because the paper presents them as results and calls the Figure 5 and 7 points experimental. They duplicate the excess measurement; the reconciler may drop them.
- Laboratory attribution is an inference: Table 1 labels the Batch 5.1 row "Hiden HTP1 (figure 1)" and the S-33/k row "Hiden IGA-001 (figure 1)", so Figure 1 data and the absolute data derived from it carry those laboratories. The paper does not say which instrument was gravimetric or volumetric, so measurement_method is unknown.
- replicates_reported true on all rows: Table 1 reports each sample measured in independent laboratories (the paper's own "validation"); no uncertainty is printed.
- Figure 5 right is titled 298 K while Figure 1 and Figure 7 label the S-33/k ambient isotherm 293 K; the Figure 7 293 K top point is 3.64 g/kg at 19.94 bar and the Figure 5 298 K top point 3.52 g/kg at 19.89 bar; both stored with the printed temperature (probably the same data).
- Text "up to 100 g/kg (90 bar, 83 K)" (M14) is not reached by the plotted 83 K isotherms (total stored 92.9 g/kg at 80.2 bar); value_kind unclear. Section 1 also says 90 bar, 303 K: the 303 K isotherm does reach 90 bar (M13).
- Table 1 g l-1 vs wt% pairing: 0.9 wt% with 5.2 g l-1 follows the S-33/k apparent density (0.58 g/cm3), 1.1 wt% with 5.7 g l-1 does not (would be 6.4); the S-33/k Hiden values also imply about 0.52. Range endpoints paired in printed order.
- Table 1 S-33/k Hiden IGA-001 values carry footnote a (extrapolated from isotherms, equations (6) and (10)): value_kind fitted_extrapolated, no isotherm_id (footnote does not say which curve).
- Characterization stored: pore volume <10 A (0.76 and 0.39 cm3/g) as ultramicropore volume with cutoff 1.0 nm; pore width mode as average_pore_diameter_nm (0.75, 1.13 nm; printed 7.5, 11.3 A), pore_diameter_method DFT; no micropore volume (<2 nm) is given; degassing, sample mass, free-volume calibration not stated.
