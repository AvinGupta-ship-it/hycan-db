# HYC-0104 extraction log (agent B)

## Sources extracted from

- Fig. 9a (main p. 976), TE7 filled red triangles (adsorption branch, run I1): 13 markers digitized, 13 rows; archive fig9a_TE7_filled_triangles_adsorption.json. Different pressures and point count from the Fig. 9b run, so treated as a separate run. Panel (a) has no x-axis title; taken as MPa as in panels (c) and (d).
- Fig. 9a, TiC-CDC-800 filled black squares (adsorption branch, run I4): 22 markers digitized, 19 rows (3 at the zero-pressure tick, see below); archive fig9a_TiC-CDC-800_filled_squares_adsorption.json. Different pressures and point count from the Fig. 9c run, so treated as a separate run.
- Fig. 9a, SWCNTs open blue circles (desorption branch of run I7): 24 markers digitized, 24 rows; archive fig9a_SWCNTs_open_circles_desorption.json. Open symbols are coded desorption by the paper's own convention in the Fig. 3 caption ("solid symbols represent adsorption, and the open symbols represent desorption"); the Fig. 9 caption does not define them.
- Fig. 9a, SWCNTs filled blue circles: digitized as a cross-check only (work/crosscheck_fig9a_SWCNTs_filled_circles.json, 16 markers). They match the Fig. 9d points within about 1 px at every pressure, so they are the same run (I7); no rows were written from them, to avoid duplicates.
- Fig. 9b (main p. 976), TE7 "Experimental data" red triangles (run I2): 20 markers, 20 rows; archive fig9b_TE7_excess_adsorption.json.
- Fig. 9b, TE7 "Absolute adsorption" blue dashed line (I3): curve mode, read at k/10 x p_end (p_end = 17.70 MPa), 10 rows, value_kind fitted_interpolated (fitted_extrapolated for 17.70 MPa, beyond the last measured point at 16.44 MPa); archive fig9b_TE7_absolute_calculated_curve.json.
- Fig. 9c (main p. 976), TiC-CDC-800 "Experimental Data" black squares (run I5): 17 markers, 15 rows (2 at the zero tick); archive fig9c_TiC-CDC-800_excess_adsorption.json.
- Fig. 9c, "Absolute Adsorption" blue dashed line (I6): 10 rows (p_end = 13.92 MPa; the 13.92 MPa point is beyond the last measured point at 13.29 MPa and coded fitted_extrapolated); archive fig9c_TiC-CDC-800_absolute_calculated_curve.json.
- Fig. 9d (main p. 976), SWCNTs "Experimental data" blue circles (adsorption branch of run I7): 23 markers, 21 rows (2 at the zero tick); archive fig9d_SWCNTs_excess_adsorption.json.
- Fig. 9d, "Absolute Adsorption" blue dashed line (I8): 10 rows (p_end = 12.45 MPa, all within the measured range); archive fig9d_SWCNTs_absolute_calculated_curve.json. Trace points above 3 wt% lie beyond the highest labelled tick (3), so the calibration is extrapolated there by less than 3% of the axis span.
- SI Table S1 (SI p. 4): "Max uptake (wt%)" 4.55 (TiC-CDC-800), 4.82 (SWCNTs), 3.74 (TE7) gives 3 rows (value_kind fitted_extrapolated, no pressure, so pressure_unstated = true). On the same rows, rho_A (0.06978, 0.05073, 0.1016 g cm-3) is stored as adsorbed_phase_density_kg_m3.
- Main text p. 975 ("70 kg m-3 and 50 kg m-3" for TiC-CDC-800 and SWCNTs; "101 kg m-3" for TE7) and p. 977 ("(50 kg m3)"): these are the same fitted adsorbate densities as Table S1 rho_A, rounded. They are cited in the notes of the Table S1 rows, not entered as separate rows.
- Table 2 (main p. 971) and the text on pp. 969 and 971: BET area, total pore volume (P/P0 = 0.95), micropore volume and PSD maxima, carried on every row of each sample. The BET range was chosen by the Rouquerol consistency criteria (bet_consistency_criteria_stated = true), but no numerical range is printed (bet_range_stated = false).
- Methods (main pp. 969-970): instrument (Hiden Isochema HTP-1), 77 K liquid-nitrogen bath, H2 purity 99.99996%, about 100 mg samples, degassing at 473 K for 10 h at about 10^-4 Pa, and reproducibility within 0.3% of measured amounts (gives replicates_reported = true; the figure is relative, so uncertainty_wt_pct is left empty). Synthesis and treatment of TE7, TiC-CDC-800 and the SWCNTs are also taken from here.

## Values seen but not extracted

- Fig. 9a TiC-CDC-800 open squares (desorption, run I4) and TE7 open triangles (desorption, run I1): not separable by the tool. These hollow markers have 1-px outlines and no centre dot. The 3-px opening in the tool's marker mode removes them. Most are also partly hidden behind the filled markers of the same run, or stacked in the p near 0 column. Trials with hole-filled image copies gave fragmented, positionally biased blobs and false blobs between the two connecting lines, so I took no values from them. I counted about 10 open squares and 8 open triangles. The stack of open squares at about 1.1-1.8 wt% near p = 0.03-0.1 MPa cannot be counted.
- Fig. 9a TE7 filled triangles near p = 0 (about 5-8 markers at about 0.06-1.9 wt%): hidden behind the TiC-CDC-800 squares and SWCNT circles in the low-pressure column, so their centroids cannot be separated. Not extracted.
- Fig. 9a SWCNT open circles between about 0.97 and 1.33 wt% at p near 0.1 MPa: hidden behind the TiC-CDC-800 markers, so they cannot be counted or extracted. Because of this and the two items above, isotherm_point_count for I1 (26), I4 (32) and I7 (47) is the number of markers I could positively identify, which is a lower bound.
- 7 markers at the zero-pressure tick were digitized (they are in the archives) but no rows were written, because the digitized pressure is 0 or slightly negative, within half a pixel of the zero tick. Their pressure cannot be resolved, and validate_row_detail.py rejects pressure_bar = 0. The markers are: Fig. 9a TiC-CDC-800 0.00, 0.158 and 0.369 wt%; Fig. 9c TiC-CDC-800 0.206 and 0.846 wt%; Fig. 9d SWCNTs 0.00 and 0.245 wt%.
- Fig. 9b-d red "Fitting" lines: Tóth fits drawn through the measured points of the same runs. They are not separate isotherms, so they were not digitized.
- SI Figs. S5, S6 and S7: re-plots of the runs in Figs. 9c, 9d and 9b. I checked this by digitizing each one in the work directory (for example, the last S5 point is 13.285 MPa / 1.501 wt% against 13.294 / 1.506 in 9c, and the last S7 point is 16.447 / 1.735 against 16.435 / 1.726 in 9b). They were not extracted again. Their fit and absolute curves repeat Fig. 9. Their parameter insets repeat Table S1, except that the S7 inset prints rho_A = 0.1016 ± 2.233 where Table S1 has ± 0.0002.
- Table S1 b, c and v_p (fitted pore volume 0.6526, 0.9501 and 0.3685 cm3 g-1): model parameters, not uptake or measured porosity. v_p is quoted in the notes of the max-uptake rows only.
- Fig. S8 (simulated absolute H2 isotherms in 0.60, 0.99 and 1.16 nm SWCNT models) and the MC-simulated densities of about 82 kg m-3 (pp. 976-977): simulation, not measurement.
- Bulk H2 densities of 0.32 and 0.95 kg m-3 at 0.1 and 0.3 MPa (p. 975), liquid H2 at 70 kg m-3 (14 K) and solid H2 at 87 kg m-3 (12 K) (p. 975): reference properties, not uptake.
- INS results in Figs. 5-8 and S1-S4: integrated intensities in arbitrary units against dosing pressure (including the "Type I isotherm" of Fig. 7a), elastic-line FWHM (for example 0.330 ± 0.003 meV, 0.44 and 0.34 meV) and solid-like to total H2 ratios. None of these is an H2 uptake quantity, and none is an isotherm in uptake units.
- Table S2 diffusion coefficients and Figs. S9-S14 (MD and MC simulations): simulation.
- Fig. 3a N2 isotherms and Fig. 3b PSD: N2 characterization; the PSD maxima from Table 2 are stored.
- Table 1 Raman (D/G FWHM; I_D/I_G of 0.87 for TiC-CDC-800, 0.97 for TE7 and 0.05 for SWCNTs), Fig. 2 Raman and the RBM-derived tube diameters of 0.6-1.2 nm: characterization with no schema field.
- Fig. 4 TGA (TiC-CDC-800 2.6 wt% residue, about 0.84 mol% TiC; all samples > 97 wt% carbon): quoted in the sample notes. residual_metal_wt_pct is left empty because the paper prints no Ti wt%.
- Isosteric enthalpies of "5-10 kJ mol-1" (p. 975): cited literature values, not measured here.
- No non-carbon material was measured, and there are no multi-laboratory or consensus values.

## Digitization method notes

- Every axis was calibrated on its lowest and highest labelled ticks, found from pixel tick profiles, and checked on a third tick. All checks were within 1%: the y check for 9b is 0.98%, the rest are at most 0.2%.
- Image copies used by the tool are in work/img/. All of them have unchanged geometry.
  - Legends were masked white: main-09_f9a_nolegend.png, main-09_f9b_nolegend.png, main-09_f9c_nolegend.png, main-09_f9d_nolegend.png.
  - In the Fig. 9d copy, the red fit line and red-over-blue blend pixels were recoloured blue, so that the circles it crosses survive the opening: main-09_f9d_redtoblue.png. A 9-px dash of the absolute curve was rejected with --marker-min-px 15.
  - The Fig. 9d markers were erased for the absolute-curve run: main-09_f9d_nomarkers.png.
  - For the SWCNT open circles in Fig. 9a, a 3x3 block was painted at each circle's single-pixel centre dot: main-09_f9a_SWCNTopen_dots.png. 20 dots were found automatically (an isolated pure-blue pixel with ring pixels 2-4 px away in all four axis directions). 4 dots were confirmed by inspection where the ring is partly hidden: (262,298), (261,307), (257,350) and (256,360).
- Fig. 9c black squares were isolated with tolerance 258 around #000000, which takes in the red fit line crossing each square, so the squares survive the 3-px opening. The 2-px line itself is removed. Marker counts equal the visual counts for 9b (20), 9c (17) and 9d (23).
- The archives' status is "unchecked" because the paper prints no isotherm point value to run `check` against.
