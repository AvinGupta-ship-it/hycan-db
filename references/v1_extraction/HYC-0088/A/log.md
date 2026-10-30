# Extraction log HYC-0088, agent A (claude-sonnet-5-5), run date 2026-10-29

Rows written: 180 (M1-M180). Validator: scripts/validate_row_detail.py --errors-only reports no errors; without the flag it reports only the uptake_type=unspecified warning on every row.

## Extracted from
- Abstract (main p.639): "1.7 and 2.6 wt% at a pressure of 1 and 80 bar" (77 K). Restatements of Table 6 WS_PD_90 (1.69 wt%) and SI Table S3 (2.62 wt%); no separate rows, cited in the notes of those rows.
- Table 1 (main p.641): sample labels WS_PD_30/60/90/120 and activation times 30/60/90/120 min at 1173 K; used for S1-S4 and the descriptions; no uptake.
- Methods text (main p.640-641, Section 2): synthesis route, ASAP 2460 (H2 up to 1 bar; 12 h at 473 K, P <= 1e-5 mbar), homemade volumetric Sieverts f-PcT built by DeltaE S.r.l (up to 80 bar, 298 K and 77 K; 473 K overnight, P < 1e-6 mbar), He pycnometry at 298 K, Toth model; used for method, degassing, instrument and calibration fields.
- Table 2 (main p.643): SBET (BET, p/p0 0.01-0.30, N2 77 K), Vultra (d<0.7 nm), Vsuper, Vmicro, Vmeso, TPV, % micro for S1-S4; on every row of each sample. Vsuper and % micro have no field and are not stored.
- Table 3 (main p.644): textural data for WS_PT (pellet-derived, SBET 674) and WS_GR (granular-derived, SBET 1041) and WS_PD_90; WS_PT and WS_GR have characterization (also Fig. 4, Fig. S3) but no H2 uptake value, so they get no rows and no sample id.
- Table 4 (main p.645): XPS atomic composition; recorded in notes (K, Ca, N, Cl, P, F, Na are incidental, not coded as dopant or metal, no composition-method field fits). Table 5 (main p.645): XPS C1s components; functional_groups.
- Fig. 8 (main p.645, 77 K, 0-1 bar, four adsorption series): digitized, 4 archives (fig8_ADS_WS_PD_30/60/90/120), rows for S2 (partly), S3 and S4 adsorption and the merged 1-bar rows; S1 adsorption taken from Fig. 9a because the Fig. 8 red markers are partly hidden.
- Table 6 (main p.646): 1.28, 1.61, 1.69, 1.33 wt% at 1 bar, 77 K for S1-S4, rows M21, M57, M95, M135 as table_direct; each is also the Fig. 8 marker at 1 bar (printed 1 bar within 2% of 1.0054, 1.0019, 1.0019, 1.0041 bar), merged into one row with `digitized:` notes, isotherm I1-I4.
- Fig. 9a-d (main p.646, adsorption filled and desorption open circles per sample): desorption rings digitized for all four samples (4 archives, ring interiors on derived images), adsorption filled markers digitized for S1 (9a) and S2 (9b) only.
- Fig. 11b (main p.647, WS_PD_90, 77 K, up to 80 bar): adsorption (filled) and desorption (open circles) digitized, isotherm I5; Fig. 11a plots the same adsorption markers with the Toth fit line (same positions, counted once, not digitized separately).
- Table 7 (main p.647) and text p.646: Toth wt%max 2.82 +/- 0.04 wt% at 77 K as a fitted_extrapolated row without pressure, isotherm I5.
- Text p.646: skeletal density 2.47 +/- 0.18 g/cm3 (He pycnometry), "maximum amount of hydrogen adsorbed of around 2.6 wt%" (same value as SI Table S3 2.62), experimental error almost 10% for cycles; used for skeletal_density, notes and replicates_reported.
- Fig. 12a (main p.648, WS_PD_90, 298 K): highest-pressure marker (open circle, desorption, 77.54 bar) digitized, isotherm I6, one row.
- Text p.647 (below Table 7): "approximately 0.1 wt%" per cycle at 298 K, one text_direct row, approximate bound, pressure unstated.
- SI Table S1 (si1 p.1-2): literature walnut-shell adsorbents; only the row "This paper" (BET 1163.2, TPV 0.491, micropore 92 %, average pore size 0.79 nm) used: average_pore_diameter_nm 0.79 on S3 rows, BET 1163.2 noted.
- SI Table S3 (si1 p.5): row Walnut shells (this paper): 77 K/1 bar 1.69 (same as Table 6, merged), 77 K/80 bar 2.62 and 298 K/80 bar 0.12 rows (data_location SI), H2/SBET column derived by the authors (noted, not stored).
- SI Table S2, Fig. S1-S4 (SEM, pore volume histograms, XPS): characterization only; nothing stored.

## Row groups
- (no isotherm_id) adsorption, table_direct: 1 rows (M178)
- (no isotherm_id) adsorption, text_direct: 1 rows (M179)
- I1 adsorption, figure_digitized: 20 rows (M1-M20)
- I1 adsorption, table_direct: 1 rows (M21)
- I1 desorption, figure_digitized: 17 rows (M22-M38)
- I2 adsorption, figure_digitized: 18 rows (M39-M56)
- I2 adsorption, table_direct: 1 rows (M57)
- I2 desorption, figure_digitized: 18 rows (M58-M75)
- I3 adsorption, figure_digitized: 19 rows (M76-M94)
- I3 adsorption, table_direct: 1 rows (M95)
- I3 desorption, figure_digitized: 17 rows (M96-M112)
- I4 adsorption, figure_digitized: 22 rows (M113-M134)
- I4 adsorption, table_direct: 1 rows (M135)
- I4 desorption, figure_digitized: 18 rows (M136-M153)
- I5 adsorption, figure_digitized: 15 rows (M154-M168)
- I5 adsorption, table_direct: 2 rows (M176, M177)
- I5 desorption, figure_digitized: 7 rows (M169-M175)
- I6 desorption, figure_digitized: 1 rows (M180)

## Isotherm point counts (isotherm_point_count)
- I1 (WS_PD_30): 44 = 20 adsorption markers + 1 merged 1-bar marker + 18 desorption rings + 5 estimated unseparated markers; approximate (markers wholly hidden under other series, and desorption rings hidden at the origin, are not counted; the 1-bar turnaround marker counted once).
- I2 (WS_PD_60): 41 = 19 adsorption markers + 1 merged 1-bar marker + 18 desorption rings + 3 estimated unseparated markers; approximate (markers wholly hidden under other series, and desorption rings hidden at the origin, are not counted; the 1-bar turnaround marker counted once).
- I3 (WS_PD_90): 38 = 19 adsorption markers + 1 merged 1-bar marker + 17 desorption rings + 2 estimated unseparated markers; approximate (markers wholly hidden under other series, and desorption rings hidden at the origin, are not counted; the 1-bar turnaround marker counted once).
- I4 (WS_PD_120): 45 = 22 adsorption markers + 1 merged 1-bar marker + 18 desorption rings + 4 estimated unseparated markers; approximate (markers wholly hidden under other series, and desorption rings hidden at the origin, are not counted; the 1-bar turnaround marker counted once).
- I5 (WS_PD_90, 77 K, Fig. 11b): 24 = 16 filled circles (including the origin marker) + 8 open circles (7 extracted, 1 partly hidden); Fig. 11c cycle markers not counted.
- I6 (WS_PD_90, 298 K, Fig. 12a): 16 = 14 filled circles + 2 open circles (origin and 77.5 bar); only the highest-pressure marker extracted.

## Seen but not extracted
- Zero-pressure markers, counted in isotherm_point_count but not written because the digitized pressure is 0.0000 bar within centroid precision and the validator rejects pressure_bar = 0: S1 DES (0.0000 bar, 0.2123 wt%, HYC-0088_fig9a_DES_WS_PD_30.json); S2 ADS (0.0000 bar, 0.1627 wt%, HYC-0088_fig9b_ADS_WS_PD_60.json); S3 adsorption (0.0000 bar, 0.0038 wt%, HYC-0088_fig11b_ADS_WS_PD_90_77K.json).
- Not extracted, S1 ADS: merged near-origin blob at pixel (310.5,1141.2), n=104 px (3.7 x median marker), p~0.0001 bar, q~0.099 wt% (fig9a_ADS_WS_PD_30); counted as 4 marker(s) in the point count.
- Not extracted, S1 ADS: 9-px sliver of a filled marker peeking out from under a desorption ring at pixel (312,1115), p~0.005 bar, q~0.35 wt% (tool rejected 'too small') (fig9a_ADS_WS_PD_30); counted as 1 marker(s) in the point count.
- Not extracted, S2 ADS: merged near-origin blob at pixel (689.0,1144.5), n=60 px (2.0 x median marker), p~0, q~0.07 wt% (fig9b_ADS_WS_PD_60); counted as 2 marker(s) in the point count.
- Not extracted, S2 ADS: 9-px sliver at pixel (709.0,1228.0) (partly hidden marker, p~0, q~0.21 wt%) (fig8_ADS_WS_PD_60); counted as 1 marker(s) in the point count.
- Not extracted, S3 ADS: 9-px sliver at pixel (716.0,1184.0) (partly hidden marker, p~0.013 bar, q~0.44 wt%) (fig8_ADS_WS_PD_90); counted as 1 marker(s) in the point count.
- Not extracted, S4 ADS: merged near-origin blob at pixel (710.8,1256.6), n=73 px (1.55 x median marker), p~0.001 bar, q~0.057 wt% (fig8_ADS_WS_PD_120); counted as 2 marker(s) in the point count.
- Not extracted, S4 ADS: merged near-origin blob at pixel (711.0,1237.8), n=90 px (1.91 x median marker), p~0.002 bar, q~0.156 wt% (fig8_ADS_WS_PD_120); counted as 2 marker(s) in the point count.
- Not extracted, S3 DES(I5): open ring near p~0.4 bar, q~0.98 wt% partly hidden under the filled adsorption marker at 0.82 bar, 1.01 wt%; centroid not separable (fig11b_DES_WS_PD_90_77K); counted as 1 marker(s) in the point count.
- Excluded from rows, S1 ADS: legend marker at pixel (478.5,1097.5) (fig9a_ADS_WS_PD_30).
- Excluded from rows, S2 ADS: legend marker at pixel (948.0,1197.0) (fig8_ADS_WS_PD_60).
- Excluded from rows, S2 ADS: legend marker at pixel (856.6,1097.6) (fig9b_ADS_WS_PD_60).
- Excluded from rows, S3 ADS: legend marker at pixel (947.5,1216.8) (fig8_ADS_WS_PD_90).
- Excluded from rows, S4 ADS: legend marker at pixel (947.5,1235.0) (fig8_ADS_WS_PD_120).
- Excluded from rows, S1 DES: legend ring at pixel (478.5,1109.5) (fig9a_DES_WS_PD_30).
- Excluded from rows, S1 DES: 1.0-bar ring at (1.0054 bar, 1.2790 wt%) is the turnaround point already counted as the Table 6 / Fig. 8 adsorption point (fig9a_DES_WS_PD_30).
- Excluded from rows, S2 DES: legend ring at pixel (856.5,1109.5) (fig9b_DES_WS_PD_60).
- Excluded from rows, S2 DES: 1.0-bar ring at (1.0018 bar, 1.6097 wt%) is the turnaround point already counted as the Table 6 / Fig. 8 adsorption point (fig9b_DES_WS_PD_60).
- Excluded from rows, S3 DES: 1.0-bar ring at (1.0032 bar, 1.6919 wt%) is the turnaround point already counted as the Table 6 / Fig. 8 adsorption point (fig9c_DES_WS_PD_90).
- Excluded from rows, S4 DES: legend ring at pixel (857.4,1426.4) (fig9d_DES_WS_PD_120).
- Excluded from rows, S4 DES: 1.0-bar ring at (1.0051 bar, 1.3336 wt%) is the turnaround point already counted as the Table 6 / Fig. 8 adsorption point (fig9d_DES_WS_PD_120).
- Excluded from rows, S3 ADS(I5): legend marker at pixel (660.0,930.5) (45.2 bar, 1.03 wt%) (fig11b_ADS_WS_PD_90_77K).
- Fig. 8 and Fig. 9 desorption: the open rings at the origin end of each desorption branch (p below about 0.003 bar) and ring-covered filled adsorption markers (for example S2 near 0.185, 0.265 and 0.33 bar, under the desorption rings of Fig. 9b and under other series in Fig. 8) cannot be seen; not extracted.
- Fig. 9c and 9d filled adsorption markers: hidden under the opaque open rings, not digitized; Fig. 8 gives the S3 and S4 adsorption branches.
- Fig. 11c (WS_PD_90, cycles 1-6 at 77 K, six marker shapes, about 96 overlapping markers) and Fig. 12b (298 K cycles, about 84 overlapping markers): markers of different cycles overlap and cannot be separated; not digitized. Fig. 11c is a set of repeated runs (separate isotherms), not I5.
- Fig. 12a filled adsorption markers (14, up to 72.3 bar): not extracted, rule for non-77 K isotherms is the highest-pressure point only (the open circle at 77.54 bar).
- Fig. 11a Toth fit line (red): fit curve, parameters in Table 7; not digitized.
- Fig. 10 (main p.647): correlation of the maximum uptake with SBET, TPV, Vmicro, Vultra and Vsuper, four points per panel at 1.28/1.61/1.69/1.33 wt% (same as Table 6); not an isotherm, not digitized, no value beyond Table 6 and Table 2.
- Table 7 Toth K = 1.24 +/- 0.17 and t = 0.66 +/- 0.04: fit parameters, not uptake values; written in the notes of the Toth row.
- Conclusion "over 1.6 wt% at 77 K and 1 bar" for WS_PD_60 and WS_PD_90 and abstract rounded values: restatements of Table 6 (noted on the merged rows), no extra rows.
- Table 3 / Fig. 4 / Fig. S3 WS_PT and WS_GR, and the sample made entirely in CO2 (burned, no yield): characterization or process remark only, no H2 uptake; no rows.
- Fig. 2, 3, 4 (N2 isotherms, PSD), Fig. 5 (SEM), Fig. 6 and 7 (XPS), Fig. 1 (TGA): N2 or characterization data, not H2 uptake; not digitized.
- SI Table S1 literature rows and SI Table S3 rows for other carbons (lemon peel [20], corncob [21], tangerine peel [22], cherry laurel [23], olive bagasse [24], almond shells [25], lignin [26], palmyra sprout [27], coconut shells [28], pinecone [29], date pits [30], peanut shell [31], pine lignin [32], Posidonia oceanica [33], wood chips [33], rice husk [34]): values from other papers for other carbons, not measurements of this paper; not extracted.

## Digitization and method notes
- Calibrations: each axis on its lowest and highest labelled tick plus a verify tick; tick pixel centres from pixel rows and columns. Fig. 8: x 710.2 -> 0, 1146.15 -> 1.0 (verify 971.52 -> 0.6), y 1267.47 -> 0, 925.7 -> 1.8 (verify 1077.63 -> 1.0). Fig. 9a/9c x 310.5 -> 0, 588.0 -> 1.0; Fig. 9b/9d x 689.0 -> 0, 966.0 -> 1.0 (verify 855.0 -> 0.6). Fig. 11b x 516.0 -> 0, 707.0 -> 60 (verify 643.5 -> 40), y 997.25 -> 0, 802.25 -> 3.0 (verify 867.0 -> 2.0). Fig. 12a x 314.0 -> 0, 534.0 -> 60 (verify 460.52 -> 40), y 394.0 -> 0, 158.53 -> 1.0 (verify 299.5 -> 0.4).
- Pressure axes of Fig. 8 and 9 are labelled "Relative Pressure (p/p0)" but run 0-1 and the text gives the range as 0-1 bar; read as bar.
- Pressure axes of Fig. 11b and 12a are labelled only to 60 bar while markers reach 75.2 and 77.5 bar; the linear calibration is extended to them (the right frame edge falls at about 77.9 bar in Fig. 11b and 79.1 bar in Fig. 12a on that calibration, and the 20, 40, 60 bar ticks of Fig. 12a are equally spaced). The tool flags those points outside_axis_range.
- Open (hollow) markers are opaque, white inside, and drawn over filled markers; the tool centroids connected coloured blobs and cannot use thin rings. For every desorption series (Fig. 9a-d, 11b, 12a) ring interiors were found as holes in the series-colour mask (hue mask; smoothed gray ink mask for black rings) and filled in the series colour on a copy of the page image (derived images d_f9a_open.png, d_f9b_open.png, d_f9c_open.png, d_f9d_open.png, d_f11b_open.png, d_f12a_open.png in the work directory, named as source_image in the archives); the tool then ran in markers mode on the derived image. The point is the centre of the ring interior.
- Marker acceptance for filled markers: pixel count between 50 % and 135 % of the series median; smaller are partly hidden slivers (not extracted), larger are merged markers (not extracted); legend markers excluded. Partly hidden accepted markers (50-80 %) have extraction_confidence 3.
- Archives with status passed (check at 1.0 bar against Table 6, differences 0.04-0.39 %): fig8 ADS S1-S4 and fig9a/9b/9c/9d DES. Archives left "unchecked": fig9a_ADS and fig9b_ADS (no paper-stated value inside their x range 0.014-0.95 bar; same calibration as the passed desorption archives of the same panel), fig11b ADS and DES and fig12a (no paper-stated value at a pressure inside their series ranges).
- Independent consistency check of Fig. 11b (not a tool check): the Toth curve with Table 7 parameters (wt%max 2.82, K 1.24, t 0.66) gives 0.993, 1.854, 2.169, 2.589, 2.619 wt% at 0.817, 4.555, 10.05, 53.7 and 75.2 bar against digitized 1.013, 1.850, 2.165, 2.627, 2.579 wt% (differences +2.0, -0.2, -0.2, +2.1, -1.5 %).
- Rows with pressure on the axis origin were not written; digitized values are stored to 6 decimals; digitization_uncertainty_wt_pct left empty as instructed.

## Coding decisions and observations
- synthesis_method = carbonization (raw carbon made by pyrolysis/carbonization in N2); physical CO2 activation goes in activation_method. material_class = activated_carbon: K, Ca, N, Cl, P, F, Na in XPS are called contamination or incidental N uptake in N2, not a deliberate dopant or composite phase.
- measurement_method = volumetric_sieverts for both instruments: the paper names the high-pressure apparatus as a volumetric Sieverts apparatus; ASAP 2460 is coded volumetric by instrument type, the paper does not call it volumetric. Basis: the paper names no basis (excess, absolute or total), so basis_stated = false, uptake_type = unspecified and basis_inferred = excess by the volumetric default.
- wt% convention: the paper says "weight percent of gas adsorbed per gram of adsorbent" in Section 2.2 but does not define W1 or W2 or print paired units for the same point; coded unknown/none.
- calibration_described = true only for the f-PcT rows (He pycnometry at 298 K described, stored as free_volume_calibration); false for ASAP rows. replicates_reported = true for f-PcT rows (cycles in Fig. 11c and 12b, experimental error almost 10 %), false for ASAP rows (one isotherm, no uncertainty).
- area_same_sample = yes (BET on the same activated samples); bet_consistency_criteria_stated = false (a correlation coefficient > 0.9999 is given, no Rouquerol criteria).
- measuring_lab_id: corresponding author marked first is Conte; first affiliation Università Della Calabria.
- SI Table S3 80-bar rows: 77 K 2.62 wt% gets isotherm I5 because the text attributes the 2.6 wt% maximum to Fig. 11; it is not merged with a plotted marker (highest plotted adsorption marker 75.2 bar) but is within 3 % of the digitized 2.6269 wt% at 53.7 bar, hence value_kind measured. 298 K 0.12 wt% gets no isotherm_id.
- Observation: the first Sieverts adsorption marker of WS_PD_90 (0.82 bar, 1.01 wt%) is far below the ASAP adsorption values at similar pressure (about 1.6 wt% at 0.79 bar, Fig. 8); the two instruments disagree at low pressure.
- Observation: in Fig. 11b the open desorption rings at 0.63, 0.88 and 1.26 bar (1.11, 1.23, 1.39 wt%) lie 15-28 % above the Toth curve and above the single adsorption marker at 0.82 bar (1.01 wt%), although the text says adsorption and desorption overlap; both recorded as plotted.
- Observation: in Fig. 8 the marker at 1 bar is a filled adsorption marker; Fig. 9 draws the marker at 1 bar as an open desorption ring (turnaround point). Table 6 calls it the adsorption capacity, so it is recorded once as adsorption.
- Observation: desorption ring centres interpolated at the adsorption pressures between 0.1 and 0.95 bar lie within 2 % of the adsorption markers for WS_PD_60, WS_PD_90 and WS_PD_120 (mean differences +0.1, -0.1, +0.4 %), but 0.5-5.3 % above them for WS_PD_30 (mean +3.4 %, largest at 0.10 bar), so the text claim of no hysteresis holds within about 2 % except for WS_PD_30.
