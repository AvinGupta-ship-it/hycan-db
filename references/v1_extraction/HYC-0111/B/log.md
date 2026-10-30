# HYC-0111 extraction log (agent B)

Paper: Gómez Costa, Juárez, Anunziata 2016, InTech book chapter, doi 10.5772/63710. 36 page images (main-01 to main-36; main-36 is blank). No supplementary file. 273 rows written.

## Sources extracted

- Table 3 (main-13, p. 63): H2 sorption (wt%) at 10 bar and 77 K (footnote **) for CMK-1 (2.1), Zn-CMK-1 (4.4) and Ni-CMK-1 (2.4): 3 table_direct rows. Area, VP mesoporous volume and BJH pore diameter of these samples copied onto their rows.
- Table 4 (main-15, p. 65): SBET, VuP, VTP and Wp of CMK-3, Pt-CMK-3, V-CMK-3 and TiO2-CMK-3 copied onto their rows (no H2 values in this table).
- Section 2.2 to 2.8 and p. 56 (main-03 to main-06): synthesis routes, ICP metal contents, N2 physisorption conditions, H2 method (ASAP 2050, 77 K, 0-10 bar, H2 99.9999%, degassed at 523 K for 8 h under vacuum). Coded on every row.
- Sections 3.1, 5 and 7 (main-12, main-17 to main-19, main-22, main-24): cluster sizes and XPS/EDS compositions, used in material_description and notes only.
- Figure 25 (main-29, p. 79): H2 isotherms at 77 K, 0-10 bar, seven samples; Ads. branch drawn as a line without markers, Des. branch as markers. Digitized: six samples, 60 line rows less 2 merged with Table 3 (58), plus 212 Des. marker rows. CMK-1 not separable (see below).

## Figure 25 digitization

- Calibration (page pixels): x 0 bar at 359.42, 10 bar at 673.14, check tick 6 bar at 547.73 (error 0.04%); y 0 wt% at 698.13, 5.0 wt% at 421.66, check tick 2.5 wt% at 560.03 (error 0.1%). Tick centres from intensity-weighted pixel rows/columns of the major ticks.
- The legend sits inside the plot (top left), so each series' region starts below its own legend entry.
- Des. markers lie at a regular 0.25-bar spacing from 0.25 to 10 bar in every series: 40 markers per series; Ni-CMK-1 has one more red square at 0 bar (on the axes). This count is isotherm_point_count on Des. and Table 3 rows; line rows leave it empty.
- Ads. lines: --mode curve, read by linear interpolation at 1, 2, ..., 10 bar (p_end = 10 bar: the paper gives the range 0-10 bar, and the trace runs past 10 bar only by the half-width of the 10 bar marker; p_start about 0). value_kind fitted_interpolated, because the paper does not say the line joins measured points and it reports a Freundlich fit (R2 = 0.98). The lines run under the same-colour Des. markers, so each trace is the per-column median of line and marker pixels. Des. markers and line traces agree within 0.03 wt% for every series.
- Archives (out/digitizations/), colour / tolerance / region / points / check status:
  - fig25_ZnCMK1_des.json: #3a4aa6, 40, 356-712 x 448-702, 36 markers, passed (Table 3, 4.4 at 10 bar: 4.421).
  - fig25_ZnCMK1_ads.json: #3a4aa6, 40, 361-712 x 448-697, curve, passed (4.440 at 10 bar).
  - fig25_NiCMK1_des.json: #ec1b23, 80, 356-712 x 520-702, 31 markers, passed (Table 3, 2.4: 2.381 at 9.995 bar).
  - fig25_NiCMK1_ads.json: #ec1b23, 60, 361-712 x 520-697, curve, passed (2.381 at 10 bar).
  - fig25_CMK3_des.json: #5ec132, 100, 356-712 x 520-702, 36 markers, unchecked (no stated value for CMK-3).
  - fig25_CMK3_ads.json: #5ec132, 60, 361-712 x 520-697, curve, unchecked.
  - fig25_PtCMK3_des.json: #7b1519, 60, 356-712 x 495-702, 35 markers, unchecked (no stated value).
  - fig25_PtCMK3_ads.json: #7b1519, 60, 361-712 x 495-697, curve, unchecked.
  - fig25_VCMK3_des.json: #7ad2db, 40, 356-712 x 502-702, 36 markers, unchecked (no stated value).
  - fig25_VCMK3_ads.json: #7ad2db, 40, 361-712 x 502-697, curve, unchecked.
  - fig25_TiO2CMK3_des.json: #b834a0, 100, 356-712 x 520-702, 38 markers, unchecked (no stated value).
  - fig25_TiO2CMK3_ads.json: #b834a0, 60, 361-712 x 520-697, curve, unchecked.
- Markers that could not be separated (tried tolerances 40-120 and opening 1-3 px; smaller openings merge markers through the same-colour line, and at 120 the red series picks up the dark-red Pt-CMK-3 markers):
  - Zn-CMK-1 Des.: 0.25, 0.5, 0.75 and 1.0 bar (under V-CMK-3 diamonds, Pt-CMK-3 circles and lines). 36 of 40.
  - Ni-CMK-1 Des.: 0 bar (on the axes) and 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75 bar (under CMK-3 circles and the CMK-1/CMK-3 lines). 31 of 41.
  - CMK-3 Des.: 0.25, 0.75, 1.0, 1.25 bar (under Ni-CMK-1 squares and CMK-1 markers). 36 of 40. Between about 3 and 7 bar the circles are partly covered by Ni-CMK-1 squares, so their centroids may sit up to about 1 px (0.02-0.03 wt%) low; the 6.0 bar marker reads 1.799 wt%, the same as 5.75 bar.
  - Pt-CMK-3 Des.: 0.25, 0.5, 0.75, 1.0, 1.75 bar. 35 of 40.
  - V-CMK-3 Des.: 0.25, 0.5, 0.75, 1.0 bar. 36 of 40.
  - TiO2-CMK-3 Des.: 0.25, 0.5 bar. 38 of 40.
  - CMK-1 (black Ads. line, open-square Des. markers): no point extracted. The black line and the open squares lie under the CMK-3 green line and circles and the Ni-CMK-1 squares over the whole range. Only fragments of square top edges (grey) and dark-green blended line pixels show. A grey-colour marker run found no usable markers, and a black curve run found only scattered pixels with gaps of more than 4 bar. All 40 Des. markers and the whole Ads. line are recorded here as not separable.
- Table 3 and Figure 25 overlap: the Table 3 values (10 bar, 77 K) are the same measurements as the 10 bar ends of the Zn-CMK-1 and Ni-CMK-1 Ads. lines. Each is recorded once, as a table_direct row carrying the isotherm_id and the digitized line value in notes. The 10 bar Des. markers are kept as desorption rows. The CMK-1 Table 3 value carries isotherm_id I1 with no digitized point, because the curve could not be digitized.
- Possible inconsistency: Table 3 gives CMK-1 = 2.1 wt% at 10 bar, but in Figure 25 the CMK-1 open squares are hidden beneath CMK-3 markers that end at 2.18 wt% (digitized), which rounds to 2.2.
- Isotherm ids: I1 CMK-1, I2 CMK-3, I3 Zn-CMK-1, I4 Ni-CMK-1, I5 Pt-CMK-3, I6 TiO2-CMK-3, I7 V-CMK-3.

## Coding decisions

- measurement_method volumetric_sieverts: the paper names "ASAP 2050 apparatus properly calibrated" without a manufacturer or a free-volume method. The ASAP 2050 is a volumetric (manometric) analyzer, so basis_inferred = excess by the instrumental default. instrument_identified false (no manufacturer); calibration_described false.
- Table 3 "Area" has no method named (BET is named only in Table 4), so surface_area_method = unspecified for CMK-1, Zn-CMK-1 and Ni-CMK-1, with probe gas N2 from Section 2.8.
- Metal loadings: Zn 5 wt% and Ni 5.5 wt% (ICP after reduction, cited to ref. [13]); Pt 0.9 wt% (ICP/EDS, p. 69; the synthesis section says 1 wt%, cited to ref. [12]); Ti 5 wt% and V 1 wt% are nominal contents only.
- Labels: CMK-1, Zn-CMK-1 and Ni-CMK-1 as in Table 3. CMK-3, Pt-CMK-3, V-CMK-3 and TiO2-CMK-3 as in their first figure legends (Figures 3 and 4, the same as Figure 25). The subscript in TiO2 is written as a plain 2.

## Values seen but not extracted

- Table 3, Si-MCM-48 (silica template, not a carbon sorbent): H2 sorption "–" (no value); Area 1034 m2/g, VP 0.96 cm3/g, BJH 2.22 nm.
- Table 4, SBA-15 (silica template, not a carbon sorbent, no H2 value): SBET 1040 m2/g, VuP 0.57, VTP 1.38 cm3/g, Wp 7.0 nm.
- Tables 1 and 2 (main-07, main-08): XRD d-spacings and unit-cell a0 of the silicas and carbons. These are mesostructure spacings, not graphitic interlayer spacings and not uptake, so they are not extracted.
- Section 2.8 (main-05): H2 chemisorption by pulse titration at 295 K (Micromeritics Chemisorb 2720). No result is reported.
- Section 8 (main-26): Freundlich fit of the isotherms, R2 = 0.98. No constants K_F or n are printed, so there are no model-parameter rows.
- Text, main-27 p. 77: "The Zn-CMK-1 sample has the highest hydrogen uptake (0–10 bar)"; conclusions (main-30) rank the samples. Neither gives a number.
- Figures 1-8 (XRD), 9 and 11 (N2 isotherms and pore size distributions), 10 (pore size distribution), 12-15 (XPS), 16 (Raman), 17-24 (TEM, EDS, particle-size histograms) and 26 (scheme): not H2 uptake and not digitized. None shows an H2 value missing from the tables and text.
