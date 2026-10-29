# HYC-0082 extraction log (extractor A)

Paper: Kostoglou et al. 2021, doi 10.1016/j.cej.2021.131730, "Nanoporous polymer-derived activated carbon for hydrogen adsorption and electrochemical energy storage". Rows written: 126 (83 for HYC-0082-S1 = PDAC, 43 for HYC-0082-S2 = YP80F; 117 figure_digitized, 7 table_direct, 2 text_direct). Validator: 0 errors, 1 warning (see end).

## Extracted from

- Table 3 (p.7), 7 rows, all table_direct, confidence 5, uptake_type excess, wt% convention W2 (footnote defines Cg as mass of H2 per mass of H2 plus degassed sample): PDAC 77 K 1 bar 2.5 wt% (M39), PDAC 90 K 1 bar 1.6 (M40), PDAC 100 K 1 bar 1.1 (M41), PDAC 77 K 58 bar 5.5 (M71), PDAC 298 K 80 bar 0.6 (M82), YP80F 77 K 47 bar 4.5 (M114), YP80F 298 K 80 bar 0.5 (M126). Cn (mmol/g) stored in uptake_mmol_g as printed; per-row note says whether W1, W2 or both from Cn round to the printed wt%.
- Text Sec. 3.3 (p.5-6): repeats the Table 3 values (~2.5, ~1.6, ~1.1 wt% at ~1 bar; ~5.5 wt% at ~58 bar; ~0.6 wt% at 298 K, ~80 bar; ~4.5 wt% at ~47 bar; ~0.5 wt% at 298 K, ~80 bar). Same measurements as the Table 3 rows, so no separate rows (cited in source_location).
- Text passage p.7, left column after Table 2, "~0.13 wt% versus ~4.55 wt% at ~10 bar": 2 text_direct rows, uptake_bound approximate, confidence 4. PDAC 77 K 10 bar 4.55 wt% (M81, isotherm I4) and PDAC 298 K 10 bar 0.13 wt% (M83, isotherm I5). Not merged with a plotted point: the nearest 77 K marker is at 9.711 bar (outside max(2%, 0.02 bar) of 10 bar); the PDAC 298 K markers near 10 bar are hidden under the YP80F squares.
- Fig. 3a (p.6), PDAC H2 isotherms at 77, 90 and 100 K, pressure in mbar, 0-1000 mbar: 77 K adsorption 32 rows + 77 K desorption 6 rows (isotherm I1); 90 K and 100 K highest-pressure point only (I2, I3). Archives: HYC-0082_Fig3a_PDAC_77K_adsorption.json, _77K_desorption.json, _90K_adsorption.json, _100K_adsorption.json.
- Fig. 3c (p.6), H2 isotherms to 80 bar, PDAC and YP80F at 77 and 298 K: PDAC 77 K adsorption 36 points (35 rows plus the 58 bar point merged into the Table 3 row) + desorption 3 rows (I4); YP80F 77 K adsorption 41 rows plus the 47 bar point merged into the Table 3 row (I6); PDAC 298 K (I5) and YP80F 298 K (I7) highest-pressure point only. Archives: HYC-0082_Fig3c_PDAC_77K_adsorption.json, _PDAC_77K_desorption.json, _YP80F_77K_adsorption.json, _YP80F_298K_adsorption.json.
- Table 1 and Sec. 3.1 (characterization, Ar at 87 K, QSDFT): carried into every row of the sample. QSDFT total area (PDAC 2193 m2/g) stored in bet_surface_area_m2_g with surface_area_method=DFT because no BET area is reported; V_DFT 0.995 and V_DFT(MP) 0.944 cm3/g, S_DFT(MP) 2158 m2/g, d50 0.92 nm. YP80F values from the same table.
- Sec. 2.2 (methods): Quantachrome Autosorb-1-MP (PDAC low-pressure H2 "using the same system", so instrument inferred for Fig. 3a), degas 250 C, 12 h; SETARAM Hy-Energy PCTPro-2000 for the high-pressure Fig. 3c data, ~200 mg, He for void volumes, error bars from three independent runs. Density and sample masses recorded as printed.

## Figure digitization

- Tool: digitize_figure.py extract --mode markers (centroid of each connected marker after a 3-px opening), page images at 150 dpi, white masking boxes over legends and the Fig. 3c inset in work/page6_masked.png.
- Fig. 3c calibration: x 214.55 px = 0 bar, 593.09 px = 80 bar, verification tick 403.25 px = 40 bar (predicted 39.88); y 823.78 px = 0 wt%, 518.84 px = 6 wt%, verification tick 671.52 px = 3 wt% (predicted 2.996).
- Fig. 3a calibration: x 214.0 px = 0 mbar, 583.0 px = 1000 mbar, verification tick 397.9 px = 500 mbar (predicted 498.4); y 448.46 px = 0 wt%, 155.37 px = 2.5 wt%, verification tick 272.89 px = 1.5 wt% (predicted 1.498).
- Filled-marker series isolated by colour (black, blue, green, maroon, orange); open black rings (desorption) isolated by erasing filled discs and error-bar lines, then shape-filtering for complete rings (work/prep_rings.py), and run with --open-px 1. All 8 archives have status passed.
- Check results (check step, paper-stated values): Fig. 3a PDAC 77 K ads at 996.8 mbar expected 2.5, got 2.476; 77 K des at 980.6 mbar expected 2.5, got 2.470; 90 K at 996.9 mbar expected 1.6, got 1.608; 100 K at 1000 mbar expected 1.1, got 1.097. Fig. 3c PDAC 77 K ads at 58 bar expected 5.5, got 5.469; at 10 bar expected 4.55, got 4.572; at 80 bar expected 5.39 (5.5 minus the "2%" drop at ~80 bar), got 5.403; PDAC 77 K des at 79.6 bar expected 5.39, got 5.424; YP80F 77 K ads at 47 bar expected 4.5, got 4.534; at 80 bar expected 4.32 (4.5 minus the "4%" drop), got 4.352; YP80F 298 K at 80 bar expected 0.5, got 0.477 (4.7%, inside the 5% tolerance). The archives keep the merged blobs so that a check at an x beyond the last separated marker (996.8 mbar, "~1 bar") has an extracted point to interpolate to.
- Row confidence: 4 for isolated markers whose pixel_count is 0.6-1.35 of the series median and that are adsorption; 3 for desorption rings, small-area markers and any marker outside that ratio. Table and text rows 5 and 4.
- isotherm_point_count is an approximate visual count (I1 64, I2 55, I3 55, I4 53, I5 40, I6 67, I7 60); dense clusters counted by area and open markers behind filled ones are not countable.

## Plotted points seen but not extracted

- Fig. 3a PDAC 77 K adsorption: archive point 1 (4.0 mbar, 0.257 wt%, 178 px, about 7 times the 26 px median) is a blob of several overlapping low-pressure markers; archive point 34 (996.9 mbar, 2.476 wt%, 83 px) is a blob of the highest-pressure markers. Neither could be separated into single markers at 150 dpi, so the individual points are lost and no row exists for them. The 77 K 1 bar Table row (M39) therefore carries no digitized note.
- Fig. 3a PDAC 90 K: archive point 27 (997 mbar, 1.608 wt%, 70 px, median 16 px) is a blob of the top markers; the 90 K 1 bar Table row (M40) carries no digitized note. The other 90 K markers are not extracted (rule: highest-pressure point only at other temperatures, and that point is the Table row).
- Fig. 3a PDAC 100 K: highest point (archive point 25, 1.012 bar, 1.101 wt%) merged into Table row M41 (digitized note present). Other 100 K markers not extracted (rule above).
- Fig. 3a PDAC 77 K desorption: 6 complete open rings extracted (indices 0-5). Open rings overlapped by filled markers or other rings are not recoverable; the desorption branch is therefore incomplete.
- Fig. 3c PDAC 77 K adsorption: archive point 1 (x -0.116 bar, 0.999 wt%, 9 px) lies left of the x = 0 axis (edge marker, centroid unreliable), excluded. Archive point 37 (81.32 bar, 5.384 wt%, 26 px) is a full-size marker 1.3 bar beyond the 80 bar tick but inside the plot frame; included (M77, confidence 4); it agrees with the "2% drop at ~80 bar" check.
- Fig. 3c PDAC 77 K desorption: 3 complete rings extracted (indices 0-2); remaining open rings are hidden behind filled markers.
- Fig. 3c YP80F 77 K adsorption: archive points 1-3 (x -0.011 bar; 1.265, 0.891, 0.438 wt%; 16 px) sit on the left axis line (x < 0), excluded. Archive point 24 (22.48 bar, 4.296 wt%, 41 px) and archive point 47 (80.27 bar, 4.352 wt%, 44 px) are about 2 times the 20 px median, i.e. two merged diamonds, excluded. Archive point 35 (47 bar) merged into Table row M114. The YP80F 77 K desorption branch is drawn with open blue diamonds that overlap the filled diamonds and each other; none could be separated, so no YP80F desorption rows are written.
- Fig. 3c PDAC 298 K (red): markers are mostly hidden under the green YP80F squares; only slivers of the highest markers show. No centre could be digitized, so the 80 bar Table row (M82) and the ~10 bar text row (M83) carry no digitized note. No archive exists for this series.
- Fig. 3c YP80F 298 K: only the highest-pressure marker is used (archive point 37, 80.09 bar, 0.478 wt%, merged into Table row M126). The marker at 78.5 bar also falls within the 2% rule but 80.09 bar is closer to the printed 80 bar. Lower-pressure 298 K markers not extracted (rule: highest-pressure point only).
- Fig. 3c inset (0-10 bar replot of the same markers): not digitized, same measurements as the main panel.
- Blue open diamonds and other open markers of the main panel that overlap a filled marker: not separable, not counted in rows.

## Values seen but not extracted (tables and text)

- Table 2 (comparison with literature): rows for other papers' materials are other works' measurements, not this paper's; the "This work" row repeats the Table 3 values (PDAC 77 K, 58 bar, 5.5 wt%), already extracted.
- Abstract and conclusions give ~5.5 wt% at ~60 bar; Table 3 and Sec. 3.3 give 58 bar. The Table 3 pressure (58 bar) is used for M71. Mismatch noted here only.
- Derived ratios and differences in the text: the ~55% decrease of the ~1 bar uptake from 77 K to 100 K, the 2.2-fold increase of the PDAC 77 K uptake from ~1 bar to ~58 bar, the 35 times smaller PDAC uptake at 298 K than at 77 K (~0.13 versus ~4.55 wt% at ~10 bar; those two wt% values are extracted, the ratio is not), and the 2% (PDAC) and 4% (YP80F) drops of the excess amount at ~80 bar relative to the maximum. Not stored as rows (derived from extracted values); the 2% and 4% drops were used only to set the 5.39 and 4.32 wt% check targets.
- Fig. 3d and the normalized text values (~0.013 and ~0.012 mmol/m2; ~28 and ~21 mmol/cm3 per pore volume): no schema field for surface-normalized or pore-volume-normalized uptake; not extracted.
- Fig. 3b isosteric heat of adsorption and the Qst text (~8.3 kJ/mol at zero coverage, ~6.6 kJ/mol at ~5.5 mmol/g loading): a heat of adsorption against loading, not an uptake measurement; not extracted.
- Table 4 and Sec. 3.4 (capacitance, supercapacitor and electrochemical data, e.g. ~78 and ~63 F/g): not H2 uptake.
- The ~39.6 g/L and ~29.8 g/L volumetric uptakes in the text are the Table 3 Cv values, stored in volumetric_capacity_kg_m3 on the Table rows (M71 39.6, M114 29.8; Cv of the other Table rows also stored, basis other); the skeletal densities (2.15 g/cm3 PDAC, 2.10 g/cm3 YP80F) are in skeletal_density_g_cm3.

## Coding decisions

- wt% convention W2 for all rows, source Table 3 footnote. For figure points, wt% is read from the y-axis labelled "Gravimetric H2 uptake (wt%)" and the same convention applies because the same data feed Table 3. uptake_mmol_g is left empty for digitized and text rows (not printed). For Table rows the printed Cn is stored; W2 computed from Cn rounds to the printed wt% in all 7 rows, W1 only in 4 (M39, M41, M82, M126; not in M40, M71, M114), which supports W2.
- uptake_type excess for all rows. The paper names the quantity "excess" without defining it, so basis_stated false and basis_inferred excess.
- Text rows with a tilde: uptake_bound approximate. Table rows without a tilde: exact.
- Fig. 3a hardware: the paper records the low-pressure H2 isotherms "using the same system" as the Ar measurements (Autosorb-1-MP); recorded as inferred from that statement. Fig. 3c hardware: PCTPro-2000 as stated.
- Measurement ids HYC-0082-M1 to M126 follow the order isotherm I1 to I7, then branch, then pressure.

## Validator

- scripts/validate_row_detail.py on out/rows.csv --errors-only: 0 errors.
- Full run shows one warning: M114 (YP80F 77 K 47 bar, 4.5 wt% with 23.5 mmol/g) is inconsistent under W1 (23.5 mmol/g is 4.74 wt% under W1; 4.52 wt% under W2). Expected, because the paper's convention is W2; left as printed.
