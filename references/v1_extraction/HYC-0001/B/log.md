# HYC-0001 extraction log (agent B)

## Sources extracted from
- main-1 Abstract: "The best material with a SSA of 2560 m2/g shows a storage capacity of 4.5 wt% at 77 K" -> row M1 (with main-4 Section 3 "about 4.5 wt%" and main-5 Section 4 "up to 4.5 wt%", same value, one row).
- main-2 Table 1 (BET SSA, average pore diameter, pore volume for radius <6.5 Å, helium density): characterization on the S1 (Activated carbon I) and S6 (sample II = Purified SWCNT II) rows.
- main-2 Section 2.1 and main-5 Acknowledgments: sample origin, synthesis, purification, label choice.
- main-2/main-3 Section 2.2: Sieverts method, degassing (200 °C, ~2 h, 1e-6 mbar), sample mass "typically 100–300 mg", "ultra pure" H2, Seasand blank and He sample-volume determination, Cahn microbalance for 0.2–0.9 bar at 77 K for some samples.
- main-3 Fig. 2a, series T=77K (activated carbon I): 8 markers counted, 8 digitized -> rows M2–M9, isotherm I1 (archive fig2a_activated_carbon_I_77K.json).
- main-3 Fig. 2a, series T=298K (activated carbon I): 5 markers counted, 5 digitized; highest-pressure point only -> row M10, isotherm I2 (archive fig2a_activated_carbon_I_298K.json).
- main-3 Fig. 2b, series T=77K (purified SWCNTs II): 5 markers counted, 5 digitized -> rows M11–M15, isotherm I3 (archive fig2b_purified_SWCNT_II_77K.json).
- main-3 Fig. 2b, series T=298K (purified SWCNTs II): 6 markers counted (including one at the origin), 5 digitized; highest-pressure point only -> row M16, isotherm I4 (archive fig2b_purified_SWCNT_II_298K.json).

## Digitization details
- Fig. 2a calibration: x 0 bar at px 260.5 (left frame/tick), 70 bar at px 584.5 (right frame/tick), check tick 40 bar at px 446 (rel. error 0.19%); y 0 wt% at px 1432.5 (bottom frame/tick), 6 wt% at px 1108 (top frame/tick), check tick 3 wt% at px 1270 (rel. error 0.15%). Tick positions found from pixel columns/rows (x ticks at 353, 400, 446, 492, 538; y ticks at 1162, 1216.5, 1270, 1325, 1379).
- Fig. 2b calibration: x 0 bar at px 673.5, 70 bar at px 993, check 40 bar at px 856 (rel. error 0.04%); y 0.0 at px 1429, 3.0 at px 1108, check 1.5 at px 1268.5 (rel. error 0%). Ticks found at x 719, 765, 811, 856, 902, 948; y 1161.5, 1215, 1268.5, 1322, 1375.
- Series colour #000000 (monochrome figure). Fig. 2a 77 K: tolerance 60, region x 255–583 (includes the y-axis column so the three near-axis markers are kept), y 1112–1385. Fig. 2a 298 K: tolerance 140, 3-px opening, region 262–583 x 1386–1431. Fig. 2b 77 K: tolerance 60, region 676–992 x 1112–1380. Fig. 2b 298 K: tolerance 60, 2-px opening, marker-min-px 7, region 679–992 x 1383–1427 (a 6-px fragment where the fitted line crosses the error bar of the 66-bar marker is rejected as too small).
- Fig. 2b 298 K marker at the origin (0 bar, 0 wt%) could not be separated from the frame corner and the start of the 77 K curve; it is counted (isotherm_point_count 6) but not in the archive. It is not the highest-pressure point, so no row is lost.
- 298 K markers are half-filled squares; the tool centroid is of the black half, about 1 px from the square centre toward the filled corner (about 0.2 bar and 0.01–0.02 wt%).
- The three Fig. 2a 77 K markers below 1 bar (0.24, 0.43, 0.58 bar) overlap the y axis and the fitted curve; centres taken from the tool with the axis column inside the region.
- `digitize_figure.py check` was not run: the paper states no uptake value at a stated pressure for any digitized series (the 4.5 wt% value has no pressure), so archives remain status "unchecked".
- Fitted Langmuir (77 K) and Henry (298 K) lines in Fig. 2 are fits, not data; not digitized.

## Values seen but not extracted
- main-4 Fig. 3 (wt% storage at 77 K vs BET surface area; 10 points with error bars, one per Table 1 sample, values = saturation of the Langmuir fit): not an isotherm, not digitized. Values for Porous carbon I, Activated carbon II, Purified SWCNT I, Porous carbon II, Purified SWCNT II, Amorphous CNT, SWCNTs (Russia), Ros 1 and Ros 3 are given nowhere in tables or text; Activated carbon I's is given in text (row M1).
- main-5 Fig. 4 (wt% storage at 77 K vs pore volume <1.3 nm; same 10 storage capacities as Fig. 3): not an isotherm, not digitized; no value given in tables/text except Activated carbon I (row M1).
- main-5 Fig. 5 (wt% at 298 K and 66 bar vs surface area; 10 points with error bars; text says 65 bar): not an isotherm, not digitized. Values for all 10 samples are given nowhere in tables or text (the activated carbon I and purified SWCNT II points presumably duplicate the highest-pressure 298 K points of Fig. 2, rows M10 and M16).
- main-5 Section 4: "at room temperature the highest measured storage value is less than 1 wt% even at high hydrogen pressure": a bound over all samples collectively, with no sample identified; not a row.
- main-4 Section 3: slope 1.91 × 10^-3 mass% m^-2 g (77 K, fit across samples) and 0.23 × 10^-3 mass% m^-2 g (298 K, 65 bar, fit across samples): computed from several samples; not rows.
- main-4 Section 3: theoretical monolayer limit 2.28 × 10^-3 mass% m^-2 g; one H2 per 17.5 Å2; 4.5 Å reticular distance; 84% coverage; 10% coverage at RT: derived/theoretical; not rows.
- main-4 Section 3: adsorption enthalpy −(56 ± 10) meV for activated carbon I: not an uptake value.
- main-4 Section 3: Nijkamp et al. [27] slope 1.5 × 10^-3 mass% m^-2 g at 1 bar and 77 K: literature value from another paper.
- main-1 Introduction: "storage capacities in carbon materials at room temperature are less than 1 wt% [4,5]": literature value.
- main-2 Section 2.2: calibration with "well known metal hydrides" (non-carbon calibration standards) and the empty sample holder; no values given.
- main-3 Section 2.2: gravimetric Cahn microbalance measurements (0.2–0.9 bar, 77 K, "some samples"): no separate values; the Fig. 2a points below 1 bar may be these (noted on rows M2–M4).

## Characterization of samples without rows (Table 1, main-2; BET N2 77 K multipoint; pore volume radius <6.5 Å by MP-method)
- Porous carbon I (Mexico): BET 1646 m2/g; avg pore diameter 11.08 Å; pore volume 0.46 cm3/g; He density 2.2 g/cm3; templated carbon (sucrose pyrolysis in mesoporous silica, IPICyT).
- Activated carbon II (Germany): 1065; 18.23 Å; 0.49; 2.0 (from W. Heschel, TU Bergakademie Freiberg).
- Purified SWCNT I (USA/Germany): 1024; 15.37 Å; 0.39; 2.0 (HiPco from CNI, selective oxidation + HCl; "sample I").
- Porous carbon II (Mexico): 946; 10.60 Å; 0.25; 2.1.
- Amorphous CNT (China): 369; 14.48 Å; 0.13; 2.2 (DC arc discharge in H2).
- SWCNTs (Russia): 124; 15.52 Å; 0.05; 1.7 (graphite arc discharge in He, soot).
- Ros 1 (Cyprus): 34; 11.46 Å; 0.01; 2.1 (cracking of liquid hydrocarbons).
- Ros 3 (Cyprus): 22; 11.32 Å; 0.0065; 2.0.

## Coding decisions
- Labels: no table reports uptake and no figure legend names a sample, so the first label in the text is used: "Activated carbon I" (Section 2.1) and "sample II" (Section 2.1, "(sample II)"; Table 1 "Purified SWCNT II (USA)", Section 3 "purified SWCNTs II").
- sample_id numbered by first appearance (Table 1 order, which precedes all text naming samples): Activated carbon I = S1, Purified SWCNT II = S6; S2–S5 and S7–S10 have no rows.
- Row M1 value_kind = measured because 4.5 wt% is within 3% of the digitized 48.2-bar point (4.621 wt%) of the same sample at 77 K, although the paper evaluates storage capacity from the Langmuir saturation value.
- Basis: not named; basis_inferred excess (volumetric instrumental default). wt% convention unknown/none.
- instrument_identified false (Sieverts apparatus described with schematic but not stated to be home-built; Cahn microbalance without model). calibration_described true (Seasand blank of equal volume; sample volume measured volumetrically with He).
- replicates_reported true on all rows: error bars drawn on the Fig. 2 isotherms (no printed numerical uncertainty, so uncertainty_wt_pct left empty).
