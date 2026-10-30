# HYC-0111 extraction log (agent A)

Paper: Gomez Costa, Juarez, Anunziata (2016), InTech book chapter, 36 page images (main-01 to main-36); H2 data only in Table 3 and Figure 25. 269 rows in rows.csv.

## Extracted from

- Table 3 (p. 63, main-13), column "H2 sorption (wt%)", footnote "H2 sorption at 10 bar and 77 K": CMK-1 2.1, Zn-CMK-1 4.4, Ni-CMK-1 2.4 wt%. Three rows (M1, M45, M91), table_direct, pressure 10 bar, 77 K, isotherm_branch adsorption (paper does not say desorption).
- Table 3, other columns (Area, VP "mesoporous volume", BJH pore diameter, cluster size, metal): sample characterization on the CMK-1, Zn-CMK-1, Ni-CMK-1 rows. Area has no method named (surface_area_method unspecified, probe gas N2 from Section 2.8). VP stored as mesopore_volume_cm3_g. Cluster sizes not stored (no field).
- Table 4 (p. 65, main-15): SBET (method BET), VuP (micropore volume), VTP (total pore volume), Wp (wide mesopore, stored as average_pore_diameter_nm, method BJH per Section 2.8) for Pt-CMK-3, V-CMK-3, TiO2-CMK-3, CMK-3: characterization on their rows. No H2 value in Table 4.
- Figure 25 (p. 79, main-29), H2 isotherms at 77 K, 0-10 bar, wt%: legend gives for each sample a line labelled "Ads." and a symbol labelled "Des.". Ads. = line drawn without markers; Des. = markers on the line. Seven samples in the legend (CMK-1, Zn-CMK-1, Ni-CMK-1, CMK-3, Pt-CMK-3, V-CMK-3, TiO2-CMK-3).
- Section 2.8 (p. 56): ASAP 2050, 77 K, 0-10 bar, degassing 523 K 8 h under vacuum, H2 99.9999%, N2 isotherms on ASAP 2020, purge 673 K, BJH. Section 2.3-2.7 and 5.1/7: metal contents (Zn 5 wt% ICP after reduction; Ni 5.5 wt% ICP; Pt 1 wt%, ICP/EDS 0.9 wt%; Ti 5 wt% nominal; V 1 wt% nominal). Section 8 (pp. 76-79): Freundlich fit R2 = 0.98, "completely reversible". Author block (p. 81): corresponding author Anunziata (*), first affiliation names National Technological University.

## Figure 25 digitization

- Page image main-29.png, 1004 x 1418 px. Tick positions from pixel inspection (sub-pixel centroids). x: 0 at 359.43 px, 10 at 673.20 px, check tick 6 at 547.72 px (predicted 6.0009). y: 0.0 at 698.12 px, 5.0 at 421.67 px, check tick 2.5 at 560.02 px (predicted 2.4977).
- A work copy (work/main-29_legendmasked.png) has the legend area (x 361-470, y 416-524) painted white so legend symbols and legend lines are not detected; no data fall in that area (curves are below y = 546 at x = 470). The archives name this copy as source image; pixel coordinates are identical to main-29.png.
- Des. markers (markers mode, one JSON per series in digitizations/): fig25_ZnCMK1_des_markers 37 points, fig25_NiCMK1_des_markers 31, fig25_CMK3_des_markers 33, fig25_PtCMK3_des_markers 36, fig25_VCMK3_des_markers 35, fig25_TiO2CMK3_des_markers 38. Markers sit on a regular grid of 0.25 bar from 0.25 to 10 bar; I count 40 markers per series (isotherm_point_count = 40 on every row of an isotherm, including the Ads. line rows and the table rows, because the run has 40 markers; the Ads. line alone has no markers).
- Ads. lines (curve mode, one JSON per series): fig25_ZnCMK1_ads_curve (299 trace points), fig25_NiCMK1_ads_curve (277), fig25_CMK3_ads_curve (307), fig25_PtCMK3_ads_curve (294), fig25_VCMK3_ads_curve (310), fig25_TiO2CMK3_ads_curve (301). Rows read by linear interpolation at p = k/10 x p_end, k = 1..10, with p_end = 10 bar (the paper's range 0-10 bar and the last marker at 10.0 bar; the traced colour extends to 10.06-10.09 bar only because the end marker lies on the line end). Every trace starts below 0.15 bar (below 5% of p_end). value_kind fitted_interpolated (the paper does not say the line joins measured points; it says the data were fitted with a Freundlich isotherm). The line and the Des. marker centres agree within 0.03 wt% at every marker.
- Table value merged with plotted point (same sample, 77 K, printed 10 bar within 0.2 bar of the marker): Zn-CMK-1 table 4.4 with Des. marker at 10.0064 bar, 4.4225 wt% (M45); Ni-CMK-1 table 2.4 with Des. marker at 9.9936 bar, 2.3805 wt% (M91). These markers have no separate digitized row, and the Ads. line reading at 10 bar for Zn-CMK-1 and Ni-CMK-1 is not kept as a separate row (table value used for the 10 bar point; 9 line rows each instead of 10).
- check step against the stated 10 bar values: Zn-CMK-1 and Ni-CMK-1 archives (markers and line) passed at 5% (Ni markers checked at x = 9.99 because the last marker is at 9.994). The other archives remain "unchecked": the paper states no H2 value for CMK-3, Pt-CMK-3, V-CMK-3 or TiO2-CMK-3 to check against.
- Marker counts differ from my count of 40 (markers I could not separate, grid index k = p/0.25): Zn-CMK-1 k = 1-3 (0.25, 0.5, 0.75 bar) covered by the V-CMK-3 and Pt-CMK-3 symbols and lines; Ni-CMK-1 k = 3-11 (0.75-2.75 bar) hidden behind the CMK-3 circles; CMK-3 k = 1-7 (0.25-1.75 bar) merged with the Ni-CMK-1 squares and the CMK-1 outline; Pt-CMK-3 k = 1-4 (0.25-1.0 bar); V-CMK-3 k = 1-5 (0.25-1.25 bar); TiO2-CMK-3 k = 1-2 (0.25, 0.5 bar). Fragments of 3-8 px and detections in these ranges were not accepted.
- Partially covered markers kept (pixel count below 60% of the series' full-marker count, so the centre may be biased by up to about 1 px, 0.02 wt%): Zn-CMK-1 k = 4; Ni-CMK-1 k = 1, 2, 12, 14, 15, 17; CMK-3 k = 8-16, 18, 20-22, 25, 28 (the CMK-3 blobs are small throughout the low-pressure range because colour pixels blended with the hidden CMK-1 black outline fall outside the colour tolerance; circles are otherwise fully visible); Pt-CMK-3 k = 5-7.
- CMK-1 (black line, open black squares): the line and the squares lie behind the CMK-3 line and circles; only 8 near-black pixels exist inside the plot, and only grey outline fragments of squares show around the green circles. No digitized point or line reading is possible, so CMK-1 has only the Table 3 row (M1, isotherm I1, merged with the unseparable plotted point at 10 bar; point count 40 from the visible outline fragments on the same 0.25-bar grid).
- A small red blob at the origin (0, 0), 3-4 px wide and partly under the axes, could be a clipped Ni-CMK-1 marker at zero pressure; not extracted and not counted.

## Seen but not extracted

- Figure 9, Figure 11 (pp. 63, 64): N2 adsorption-desorption isotherms at 77 K (not H2).
- Figures 10, 11 PSD; Figures 1-8 XRD; Figures 12-15 XPS; Figure 16 Raman; Figures 17-24 TEM and EDS; Figure 26 scheme: no H2 uptake values.
- Tables 1 and 2 (XRD d-spacings and a0): not uptake; no interlayer spacing reported.
- Si-MCM-48 (Table 3) and SBA-15 (Table 4): silica templates, not carbon, no H2 uptake; characterization (area 1034 and 1040 m2/g) not stored.
- Section 2.8 H2 chemisorption (Micromeritics Chemisorb 2720, TCD, 295 K pulse titration of metal dispersion): described, no values reported; not an uptake measurement.
- Section 8 text "The Zn-CMK-1 sample has the highest hydrogen uptake (0-10 bar)": no number. Freundlich fit R2 = 0.98: not an uptake value; fitted constants not printed.
- Introduction: "reported ... [12,13]" for Pt, Zn, Ni, V and TiO2 in CMK-1/CMK-3; the paper does not state that these H2 values or isotherms were published before, so no "previously reported" note was added.
- Figure 25 values not given in Table 3 (CMK-3, Pt-CMK-3, V-CMK-3, TiO2-CMK-3 at 10 bar) are only digitized.

## Coding decisions for the reconciler

- measurement_method = unknown: the paper names "ASAP 2050 apparatus properly calibrated" without manufacturer and without saying volumetric or gravimetric. instrument_identified false, calibration_described false (only "properly calibrated"). basis_stated false, uptake_type unspecified, basis_inferred unknown (method unknown). wt% convention unknown (no paired units).
- Sample order: CMK-1 S1, CMK-3 S2 (both first appear in Section 2.2), Zn-CMK-1 S3, Ni-CMK-1 S4, Pt-CMK-3 S5, TiO2-CMK-3 S6, V-CMK-3 S7. Isotherm ids I1-I7 follow the same order. TiO2-CMK-3 label taken from the Figure 25 legend (hyphen); Tables 4 and several captions print "TiO2-CMK-3" with an en dash.
- Table 3 header "Area (m2/g)": method not named, so unspecified (value in bet_surface_area_m2_g as the headline area); bet_range_stated and bet_consistency_criteria_stated left empty for these three samples (area not coded BET). Table 4 BET rows: both false (no P/P0 range, no criteria stated). area_same_sample yes (areas are tabulated per labelled sample; N2 purge 673 K versus H2 degas 523 K noted here).
- Pt-CMK-3 loading: 1 wt% (Section 2.5) used; ICP/EDS 0.9 wt% (Section 5.1) is in the notes. TiO2-CMK-3 and V-CMK-3 loadings are nominal.
- Table rows carry branch adsorption (default) although the merged plotted point is a Des. marker.
- measuring_lab_id: corresponding author Anunziata (* in author block); first affiliation names National Technological University.
