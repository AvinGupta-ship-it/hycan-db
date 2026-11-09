# HYC-0133 extraction log (agent B)

Paper: Li et al. 2026, Nano-Micro Letters, 10.1007/s40820-025-01931-w. Input: page images only (main 20 pages, SI 17 pages). One carbon sorbent with H2 uptake data: rN-pC (HYC-0133-S1). 67 rows.

## Sources extracted from

- Main p.7, Section 3.2 text: excess ~2.5 wt% at -196 °C and ~0.8 MPa (M42), ~2.3 wt% at -186 °C and ~1.5 MPa (M43); absolute ~3.4 wt% at ~6 MPa, -196 °C (merged into M40) and ~3.0 wt% at ~6 MPa, -186 °C (M44); maximum volumetric uptake ~17.3 g H2 L-1 (on M40); 0.9 and 0.55 wt% at 0.01 MPa, -196/-186 °C (merged into M65, M67).
- Main p.8, Fig. 2a: -196 °C excess isotherm, open squares, 32 markers counted (I1, M1-M29); -186 °C excess isotherm, open circles, highest-pressure marker only (I2, M30); -196 °C absolute-adsorption line read at 10 pressures (I3, M31-M40); -186 °C absolute-adsorption line, highest-pressure end only (I4, M41).
- SI p.4, Fig. S6: -196 °C ultralow-pressure isotherm, 20 open squares (I5, M47-M66, marker 19 merged with the 0.9 wt% text value); -186 °C ultralow-pressure isotherm, 17 open circles, highest-pressure marker merged with the 0.55 wt% text value (I6, M67).
- SI p.16, Table S4: rN-pC "Max excess adsorption" 2.49 wt% (M45) and rhoA 0.02629 g cm-3 as adsorbed-phase density (M46).
- Characterization on every rN-pC row: main p.3-4 (Section 2.2.1 synthesis; Section 2.3 N2 at -196 °C on Autosorb-IQ3; degassing 300 °C, 12 h; HPSA-auto Sieverts PCT apparatus); main p.5-7 and Fig. 1a (BET 1525.4 m2 g-1; PV 1.50 cm3 g-1; micropores 0.447 mL g-1; skeletal density ~2.15 g cm-3); main p.9 and Fig. S14b (DFT PSD peak ~0.59 nm, used as modal pore width); SI Table S1 (S_BET 1525.4, V_DFT 1.498, S_DFT(MP) 1326.3, V_DFT(MP) 0.447); SI Table S2 (XPS N 5.97 at%); main p.5 (XPS N groups, C 1s components).

## Coding decisions

- Temperatures printed in °C (-196, -186) are stored as 77.15 and 87.15 K; Table S4 prints 77K and is stored as 77.0 K. Pressures in MPa are multiplied by 10. No pressure is called gauge.
- Fig. 2a reports excess (markers) and absolute (lines) side by side for the same runs, so basis_stated = true for I1-I4 and the p.7 text values. Fig. S6 labels its data "absolute adsprtion" with no definition and no excess counterpart, so basis_stated = false and basis_inferred = absolute for I5 and I6.
- The absolute-adsorption lines are modelled (Toth fit converted to absolute, Eq. S1), so value_kind = fitted_interpolated. They get separate isotherm_ids (I3, I4) from the excess runs because the basis differs.
- Text values without a plotted point within the larger of 2% and 0.02 bar of their printed pressure are not merged and have no isotherm_id: ~2.5 wt% at ~0.8 MPa (nearest I1 markers at 7.24 and 8.80 bar); ~2.3 wt% at ~1.5 MPa (nearest -186 °C circles at 15.49 and 13.56 bar); ~3.0 wt% at ~6 MPa, -186 °C (the absolute line ends at 53.2 bar).
- Table S4 2.49 wt% has no printed pressure and the paper does not say it was taken from the isotherm, so it is not merged (pressure_unstated = true). It is within 3% of the digitized I1 maximum (10.42 bar, 2.495 wt%), so value_kind = measured. Its temperature is 77 K because its R2 (0.9983) matches the -196 °C fit in Fig. 2a (0.99829).
- The volumetric capacity of 17.3 g L-1 is placed on the 3.4 wt% absolute row because 3.4/100/(1/2.15 + 1.498) = 0.0173 g cm-3. Its basis is skeletal plus pore volume, coded as other.
- measuring_lab_id: Ferrari (Cambridge) is the first marked corresponding author, but the Author Contributions say "Y. Li and L. Ren carried out the hydrogen storage properties tests". Both are affiliated only with Shanghai Jiao Tong University, so the lab is "Li group, Shanghai Jiao Tong University".
- instrument_identified = false: "HPSA-auto device, China" names a model but no manufacturer. calibration_described = false: free-volume determination is not described (only the MBWR EOS). sample_mass_mg is left empty: "~100 mg" is stated for "isothermal ab/desorption tests" in the Mg hydride context, not clearly for the cryogenic adsorption runs. H2 purity, BET P/P0 range and consistency criteria are not stated.
- wt% convention: not defined. "H2 storage capacity is calculated as wt% of entire composite" does not distinguish W1 from W2, and no paired units are given, so unknown/none.
- average_pore_diameter_nm = 0.59: this is the main peak (mode) of the DFT PSD below 2.5 nm (p.9, Fig. S14b), not a mean.
- Dopant: XPS 5.97 at% (Table S2). Text p.5 says "N content of rN-pC increases from 2.5 wt% to 6 wt%", which matches the Table S2 at% values and is likely mislabelled, so no wt% is recorded. STEM gives 2.06 at% N and 3.52 at% O (Table S3); XPS O is 2.55 at%.

## Digitization

- Fig. 2a (main p.8, raster about 1240 px wide). Axes: x ticks at 0 MPa (187.79 px) and 6 MPa (571.26 px), checked at 3 MPa (379.61 px, error 0.04%); y ticks at 0 wt% (511.12 px) and 3.5 wt% (219.59 px), checked at 2.0 wt% (344.49 px, error 0.02%). Tick positions are pixel centroids of the tick marks.
- Fig. S6 (SI p.4). Axes: x ticks at 0 MPa (414.35 px) and 0.014 MPa (892.84 px, at the frame), checked at 0.006 MPa (619.47 px, error 0.03%); y ticks at 0 wt% (615.67 px) and 1.0 wt% (268.24 px), checked at 0.4 wt% (477.05 px, error 0.03%).
- Fig. 2a markers sit on solid and dashed lines of the same colour, and many overlap near zero pressure. A whole-plot run merged them, so each marker was run separately with digitize_figure.py extract --mode markers --open-px 0, using a tight region around that marker. Marker positions came from pixel-row and pixel-column edge inspection and template matching of the outlines. This gives one archive per marker (fig2a_rNpC_77K_excess_mNN.json, figS6_rNpC_77K_mNN.json), not one per series. Colours: squares #505050, tolerance 60; Fig. 2a circles #9cb2d7, tolerance 60; S6 squares #4a4a4a, tolerance 60; S6 circles #1f64cd, tolerance 60.
- In Fig. 2a markers 02, 03, 15, 26 and 27, overlapping blue markers or lines split the square outline into 2 colour components. The value used is the pixel-weighted mean of the components in the archive.
- Marker counts: I1 has 32 squares, counted by pixel edges and enlarged views, and 32 per-marker runs each isolated one marker. I5 has 20 squares and I6 has 17 circles. I2 (Fig. 2a, -186 °C circles) is approximately 30, with a range of 28-33: about 16 circles above 0.15 MPa are clear, but the circles between about 0.2 and 0.45 wt% at near-zero pressure form a solid overlapping stack and could not be separated.
- Not extracted although digitized: Fig. 2a I1 markers 03, 04 and 05 (about 0.78, 0.98 and 1.14 wt%). Their digitized pressures were 0 or negative (-0.00098, -0.0165 and -0.00019 MPa), because they sit on the zero-pressure axis and their right edges are hidden under the blue line and circles. The schema needs pressure > 0, so they have no row but still count in isotherm_point_count = 32. The I1 origin marker (M1) gave an uptake of -0.0026 wt%, which is stored as 0 (noted on the row).
- Lines without markers: the -196 °C absolute line was traced in curve mode (#0a0a0a, tolerance 65, region kept above the markers and legend) and read by linear interpolation at k/10 of p_end = 5.980 MPa. The tool check at 5.98 MPa against the stated 3.4 wt% passed (+1.0%). The -186 °C absolute line was traced in curve mode (#2259ab, tolerance 60) and its last point (5.323 MPa) was taken.
- Archives kept only for the merge decisions (no row of their own): fig2a_rNpC_87K_excess_near1p5MPa.json, fig2a_rNpC_87K_excess_near1p4MPa.json, figS6_rNpC_87K_m15.json, figS6_rNpC_87K_m16.json.
- The tool's stated-value check cannot run on single-marker archives (it needs a range), so those archives stay "unchecked". The stated-value comparisons are in the row notes: S6 0.9 vs 0.8996 wt% at 0.1 bar; 0.55 vs 0.5685 wt% at 0.103 bar.
- Not digitized: the dashed "-196 °C fitting" and "-186 °C fitting" Toth curves in Fig. 2a and the Langmuir "Fitting" curves in Fig. S6. They are fits to the plotted markers of the same runs, not separate isotherms. -186 °C markers in Fig. 2a and Fig. S6 other than the highest-pressure one were not extracted (§9: other temperatures, highest-pressure point only).

## Values seen but not extracted

- Restatements of extracted values: Highlights p.1 "~0.9 wt% at 77 K and ultralow pressure of ~0.1 bar"; p.2 "adsorption capacity close to 1% at a pressure as low as 0.01 Mpa"; p.7 "(0.9 wt% at -196 °C) under ultralow relative pressure ranges (<0.1 bar)"; p.10 "(2.5 wt% for rN-pC)" with "saturation pressure ... ~1 Mpa for rN-pC"; p.10 "0.026 g cm-3 for rN-pC" (= Table S4 rhoA).
- rN-pC model and other non-uptake quantities: Table S4 b = 532.995 MPa-1, c = 0.29197, vp = 1.77791 cm3 g-1, R2 = 0.9983 (Toth fit parameters). Fig. 2b and p.7 isosteric heat Qst ~14 kJ mol-1 at zero coverage, falling to ~6 kJ mol-1 at 3 wt% (Qst against uptake, not an isotherm). Fig. 2d and Fig. S7-S9 DFT adsorption energies (calculated). p.7 "saturation plateau ~1 MPa" (pressure only).
- p.13: "maximum volumetric H2 uptake ~43.5 g H2 L-1 ... DFT PV (~0.440 cm3 g-1), skeletal density (~1.904 g cm-3) of rN-pC". 4.2 wt%/(1/1.904 + 0.44) = 43.5, so this belongs to the 60MgH2@rN-pC composite (not a carbon sorbent). The skeletal density 1.904 "of rN-pC" conflicts with 2.15 on p.7, and 2.15 is used for rN-pC.
- 60MgH2@rN-pC / 60 Mg@rN-pC / MgH2@rN-pC is not extracted. It is 60 wt% MgH2 (p.3: 46.8 of 76.8 mg), so carbon is not the majority by mass and it is not a carbon sorbent (§3). Values seen:
  - Abstract: 0.62 wt% adsorbed/desorbed on the scaffold, ~3.59 wt% chemical, 33.4 g L-1 pellets after 500 MPa.
  - Highlights: 3.38 wt% released at 300 °C within 30 min.
  - p.3: 4.2 wt% over two temperature ranges.
  - Fig. 4a (p.10) -196 °C excess isotherm: 0.66 wt%, saturation ~1.8 MPa, R2 0.99953, plus absolute line. Table S4: 0.66 wt%, rhoA 0.04542 g cm-3, b 3407.31, c 0.20782, vp 0.34015.
  - Fig. 4b cycling at -196 °C: 0.52 wt% at 5.3 bar, 0.20 wt% at 1 bar.
  - Fig. S15a ultralow-pressure 77/87 K isotherms (not digitized); Qst 10.6 kJ mol-1.
  - Fig. 5a TPD: T_onset 175 °C, 3.85 wt% final, ~3 wt% before 300 °C.
  - Fig. 5c: 0.93, 2.76, 3.38 and 3.41 wt% at 250, 275, 300 and 325 °C within 30 min.
  - Fig. 5d: 3.5 wt% at 200 °C within 50 min, 3.2 MPa.
  - Fig. S19: 2 wt% at 225 °C within 8 h (58.8%).
  - Fig. S20 PCT at 320, 340 and 360 °C; ΔH 67.98 kJ mol-1.
  - Fig. S21: 3.52 to 3.47 wt% absorption and 3.24 to 3.17 wt% desorption over 10 cycles at 275 °C.
  - Fig. S23 and S24 cycling; Fig. S26: ~0.6 wt% physisorbed and ~4.2 wt% chemisorbed.
  - Table 1 "This work": 0.7/3.6 wt%, De 3.3 wt%/300 °C/10 kPa/15 min.
  - BET 636.5 m2 g-1 (Fig. S14a).
- Pure Mg/MgH2 is not extracted (not a carbon sorbent):
  - TPD: ~6.8 wt%, onset ~299 °C.
  - Absorption: 0.72 and 4.71 wt% at 200 and 250 °C (3.2 MPa).
  - Desorption: <0.5 wt% at 300 °C within 3 h.
  - Cycling at 350 °C: 7.3 to 5.9 wt%.
  - Figs. S16, S18, S22-S24.
- Table 1 rows other than "This work": literature values for other papers' Mg-carbon composites (refs 24, 25, 38, 84-91). These are not this paper's measurements, and they are composites.
- ZIF-8 (MOF, not a carbon sorbent; no H2 uptake): S_BET 1877.3 m2 g-1, V_DFT 0.711, S_DFT(MP) 1367.9, V_DFT(MP) 0.666 (Table S1); text p.5 "~1877 m2 g-1 and 0.71 cm3 g-1".
- N-pC (carbon, characterization only, no H2 uptake, so no row): S_BET 925.8 m2 g-1 and PV 0.92 cm3 g-1 (Fig. 1a, p.5), but Table S1 gives S_BET 1146.5 (conflict); V_DFT 0.920, S_DFT(MP) 921.5, V_DFT(MP) 0.271; XPS C 95.16, N 2.33, O 2.51 at% (Table S2); STEM C 94.7, N 1.36, O 3.98 at% (Table S3); Raman I(D)/I(G) 2.11 (514 nm).
