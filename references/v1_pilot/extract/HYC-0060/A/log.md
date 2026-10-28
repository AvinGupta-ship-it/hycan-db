# HYC-0060 extraction log (agent A, 2026-10-28)

Rows written: 154 (rows.csv). Digitization archives: 25 (digitizations/), 147 plotted markers; 4 of them are replaced by a merged text row, so 143 digitized rows remain.

## Extracted from

- Abstract (p. 3044): 1.40(0.1) wt% at 1 MPa, 77 K, and 0.07(0.01) wt% at 1 MPa, ambient (consensus of the four group-1 isotherms) -> HYC-0060-M1, M3 (same values in Sec. 7.2.1 p. 3050 and Sec. 9 p. 3055/3056, recorded once each).
- Sec. 7.2.1 (p. 3048): group-1 plateau "around 1.4 (0.1) wt.% ... for higher pressure", pressure not stated -> M2 (pressure_unstated, uptake_bound approximate).
- Sec. 7.4.1 (p. 3052): 0.12(0.01) wt% at 2 MPa, ambient group 1 (temperature not a single number; 294-301 K per lab) -> M4. The 0.07(0.01) at 1 MPa of the same sentence is M3.
- Sec. 7.2.2 (p. 3050): group 2 "hydrogen limiting content is 1.1 wt.%" (labs 8a/8b), no pressure -> HYC-0060-M77, pressure_unstated, approximate, not tied to a marker.
- Sec. 7.2.3 (p. 3050): lab 1 "around 2.6 wt.% at 8 MPa" = last marker of Fig. 4 lab 1 (digitized 7.933 MPa, 2.628 wt%, within 0.07 MPa and 0.03 wt%): one row, text value at the plotted pressure (79.33 bar), digitized marker dropped (M21).
- Sec. 7.2.3 (p. 3051): lab 12 "around 1.9 wt.% at 2 MPa" = last marker of Fig. 5 lab 12 (digitized 1.962 MPa, 1.950 wt%, equal within printed rounding): one row at 19.62 bar, digitized marker dropped.
- Sec. 7.2.4 (p. 3051): lab 13 "1.4 wt.% at 1.5 MPa" = last marker of Fig. 5 lab 13 (digitized 1.496 MPa, 1.394 wt%): one row at 14.96 bar, digitized marker dropped.
- Sec. 7.2.4 (p. 3051): lab 2 "transitory plateau at 1.25 wt.% at around 2 MPa" -> separate approximate row at 20 bar, no isotherm_id; not merged because it describes a plateau, not one measured point (markers 1.91 MPa 1.26 wt%, 2.24 MPa 1.24 wt% are also kept).
- Sec. 7.2.3 and 7.2.4 (p. 3051): lab 2 "maximum uptake of 1.4 wt.% for pressures above 3 MPa" / "second plateau of 1.4 wt.% at pressure above 3 MPa" -> one approximate row, pressure_unstated (a range, not one pressure).
- Sec. 7.4.4 (p. 3052): lab 5 "highest uptake of almost 0.7 wt.% at 6 MPa" = highest-pressure marker of Fig. 8 lab 5 (digitized 6.002 MPa, 0.681 wt%): one row at 60.02 bar, approximate, digitized marker dropped (isotherm I16).
- Fig. 5 (p. 3051), 77 K, p <= 2.5 MPa: labs 1, 2, 3, 6, 7, 8b, 10, 11, 12, 13 (10 archives, 110 markers) = every marker that could be separated; see "Markers not extracted".
- Fig. 4 (p. 3050), 77 K, p > 2.5 MPa: labs 1 (11 markers), 2 (9), 3 (5) (3 archives). Fig. 4 and Fig. 5 show the same isotherms, so each lab keeps one isotherm_id: Fig. 5 supplies p <= 2.5 MPa, Fig. 4 supplies p > 2.5 MPa, no marker is taken twice.
- Fig. 8 (p. 3053) ambient: highest-pressure marker of labs 1, 2, 3, 4b, 5, 9, 14, 8b (8 archives; lab 8b is read in Fig. 8 because Fig. 9 clips the y axis at 0.2 wt%, its last marker is at 0.22 wt%).
- Fig. 9 (p. 3053) ambient, zoom of Fig. 8 to 3 MPa: highest-pressure marker of labs 4a, 6, 7, 11 (their isotherms end below 3 MPa; 4 archives). Other ambient markers are not extracted (scope: only the highest-pressure point at temperatures other than 77 K).
- Table 1 (p. 3049): per laboratory ambient temperature (293, 293, 298, 298, 298, 296, 301, 294, 293, 301, 294, 298 K for 1, 2, 3, 4a, 4b, 5, 6, 7, 8b, 9, 11, 14), method, initial weight (sample_mass_mg: weight before outgassing, not dry mass), outgassing pressure, H2 purity, sample density method -> coded on the rows of each laboratory.
- Sec. 3.2 (p. 3046): BET 423(20) m2/g (N2, 77 K), DR micropore volume 1.7(0.1)e-4 m3/kg = 0.17 cm3/g (also printed as 0.17 cm3/g in Sec. 7.2.1) -> coded on every row (surface_area_probe_gas N2, BET range and consistency criteria not stated, area_same_sample yes because the area is reported for the RRT material itself, no different treatment indicated).
- Sec. 6 and 7.1.2 (p. 3048): outgassing protocol 383 K 24 h then 523 K 4 h, dynamic vacuum, performed by all participants -> degas_temperature_c 249.85 (523 K), degas_duration_h 4 (second stage), degas_end_pressure_pa per laboratory from Table 1.
- Sec. 4.1 (p. 3046): "adsorption of hydrogen on porous materials corresponds to an excess adsorption" -> uptake_type excess, basis_inferred excess, basis_stated false (named in general, not defined); wt% convention not defined, no paired units: unknown / none.

## Seen but not extracted

- Sec. 7.2.1 (p. 3050) [25] 1.45 wt% for Takeda CMS 4A at 77 K, 2 MPa: a value from another paper (reference 25), not measured here.
- Sec. 7.4.1 (p. 3052) [25] 0.1 wt% at 2 MPa, room temperature: same, another paper.
- Sec. 3.2 (p. 3046) Grande et al. [24] macropore 3.1e-4 and micropore 1.7e-4 m3/kg (Hg intrusion, CO2 at 297 K): characterization by other authors, no H2 uptake.
- Sec. 7.4.3 (p. 3052) lab 6 ambient "lower hydrogen capacity by around 0.02 wt.% at 2 MPa": a difference between curves, not an uptake value.
- Sec. 7.4.4 (p. 3052) lab 2 ambient "almost no uptake": qualitative, no number (its last marker is extracted from Fig. 8, 0.009 wt% at 5.0 MPa).
- Sec. 7.4.2 and 7.4.3 (p. 3052) qualitative comparisons of isotherms 4b, 8b, 14, 1, 4a with group 1 ("similar values as isotherms 3 and 9"): no numbers.
- Sec. 3.1 (p. 3045) "values ranging from few to several tens of hydrogen wt% have been published [1-10]": literature, not this study.
- Figs 6 and 7 (p. 3051-3052) and the ambient statistics figures: standard deviation and interlaboratory consistency h, plus maxima of relative standard deviation 14% (77 K) and 36% (ambient) in Sec. 7.3, 7.4 and 9: dispersion statistics, not uptake values.
- Supplementary Tables 1 to 4 (interpolated uptake at 0.1 to 1.8 MPa, mean, deviation, h) cited in Sec. 7.3 and 7.4: supplementary material not provided in the input.
- Table 1 (p. 3049) weight loss (%), equilibrium times, temperature stability, equation of state, pressure transducer accuracy: not H2 uptake; not coded (no schema field), except purity, mass, degassing pressure, density.
- Fig. 3 (p. 3050) weight loss vs outgassing pressure, Fig. 2 (p. 3047) TPD of m/z 44 and 18 during outgassing, Fig. 1 SEM: not H2 uptake.
- Mean sample density 1.99e3 kg/m3 (Sec. 7.1.3): statistic over laboratories, not coded; per-laboratory He-based densities of Table 1 (labs 1, 3, 5, 6, 7, 11, 12) are coded in skeletal_density_g_cm3; the pure-carbon densities assumed by labs 4 and 13 (2.1, 2.2) are not measurements and are not coded.
- Non-carbon materials: none measured. Metal hydrides (Pd, LaNi5) appear only as possible calibration references (Sec. 4.2.1), with no values.
- Desorption branches: the paper mentions them (Sec. 7.3) but Figs 4, 5, 8, 9 show adsorption only; no desorption values exist in the input.

## Markers not extracted (77 K, Figs 4 and 5)

- Fig. 5 low-pressure region: below about 0.1 MPa the markers of eleven series overlap in a solid black cluster. Lowest separable marker per series (MPa): lab 12 0.101, lab 10 0.078, lab 13 0.099, lab 8b 0.227, lab 2 0.246, lab 7 0.298, lab 11 0.398, lab 6 0.417, lab 1 0.465, lab 3 0.612. Markers at lower pressure were not separable and are not extracted; isotherm_point_count is therefore empty on every isotherm.
- Lab 8a (filled half-circles in the legend) lies exactly under lab 8b in Fig. 5; no 8a marker could be separated, so lab 8a has no digitized rows (only the group-2 text value, Sec. 7.2.2).
- Lab 11 star at p = 0.7 MPa is hidden behind the lab 1 square; stars below 0.4 MPa are unresolved. Only four lab 3 up-triangles could be separated in Fig. 5; any others between 0.6 and 1.97 MPa are hidden behind markers of other labs. Lab 6 down-triangles at 0.8, 1.2 and 1.44 MPa are overlapped by other markers (confidence 2).
- Black blobs at about (202, 266) and (199, 276) in Fig. 5 (page main-08 pixels) belong to the cluster and were not assigned to any series.
- Lab 3 has no marker between 1.97 and 2.99 MPa in Figs 4 and 5 (a gap in the plotted data, not a missed marker).
- Fig. 4 lab 2 circle at 5.19 MPa is partly hidden behind a lab 3 triangle (confidence 2).

## Digitization method

- Page images used: pages/HYC-0060_main-07.png (Fig. 4), main-08.png (Fig. 5), main-10.png (Figs 8 and 9), 1241 x 1654 px. Axes calibrated on labelled ticks found by pixel inspection (tick centres, array-index convention); the third labelled tick checked the calibration in every run (residuals 0.04-0.5% of the stated value).
- Fig. 4: x 0 -> 341.65 px, 10 -> 899.01 (check 5 -> 620.56); y 0 -> 1465.79, 3.0 -> 1061.35 (check 1.5 -> 1263.14).
- Fig. 5: x 0 -> 185.29, 2.5 -> 555.77 (check 1.0 -> 333.31); y 0 -> 414.35, 1.4 -> 223.0 (check 0.7 -> 318.43). The y axis has no labelled tick above 1.4, so markers above 1.4 wt% (parts of labs 10, 12, 1, 11, 6, 7 and 3) are extrapolated along the verified linear axis and the archive flags them outside_axis_range; the unlabelled minor tick at 1.75 wt% (pixel 175.0) is predicted as 1.751 wt%, confirming the extrapolation. Those rows say so in notes.
- Fig. 8: x 0 -> 361.25, 22 -> 914.42 (check 12 -> 663.09); y 0 -> 548.14, 0.7 -> 162.61 (check 0.3 -> 383.13). Fig. 9: x 0.0 -> 190.0, 3.0 -> 525.0 (check 1.0 -> 302.0); y 0 -> 1443.45, 0.20 -> 1179.81 (check 0.10 -> 1311.0).
- All markers are black outline shapes of the same colour, so colour cannot separate series and a plain colour mask merges overlapping markers. Marker centres were therefore located on the page image by fitting an ideal outline (circle, square, diamond, pentagon, hexagon, up/down triangle, star, asterisk, plus) of the series' own marker shape and size to the dark pixels (centre accuracy about 0.5 to 1 px, below 1% of an axis span), starting from the markers visible in enlarged crops, with every fit checked on an overlay.
- Per series a derived image (white page-sized canvas, one black disc of 2.4 px radius at each accepted centre, work-directory file derived/<archive>_discs.png) was passed to digitize_figure.py extract --mode markers with colour #000000, the calibration above and the third-tick check; the tool returned the centroid of each disc and its calibrated value. The archive's source_image path and sha256 therefore refer to the derived image. For every archive the number of extracted markers equals the number of accepted centres, and the centroids lie within 0.2 px of the fitted centres.
- digitize_figure.py check was not run: no value stated in the paper falls inside the extracted pressure range of a series with a stated precision (the merged text values are rounded, "around", or lie beyond the last marker pressure).
- Pressure in bar = MPa x 10. Digitized wt% rounded to 3 decimals (4 below 0.2 wt%), pressure to 0.01 bar. digitization_uncertainty_wt_pct left empty (reconciliation computes it).

## Coding decisions

- measuring_lab_id: laboratories are anonymised by code, so each coded laboratory is "RRT participant N (anonymised)"; 4a and 4b are the same laboratory (participant 4), as are 8a and 8b (participant 8). Consensus values of several laboratories carry the corresponding author group "Zlotea group, Institute for Energy, Joint Research Centre, European Commission" (Sec. 7.4.1 and the abstract refer to groups of labs, not one).
- measurement_method: static volumetric laboratories (1, 2, 3, 5, 6, 8a, 8b, 9) volumetric_sieverts; static gravimetric (4a, 4b, 7, 11, 12, 13, 14) gravimetric_microbalance; lab 10 (dynamic volumetric, 50 ml/min) other with measurement_mode isothermal; consensus rows other (mixed volumetric and gravimetric).
- calibration_described true only where Table 1 and Sec. 7.1.3 state how sample density/dead volume was determined (labs 1, 3, 5, 6, 7, 11, 12); false where the density was not determined, assumed from carbon (labs 4, 13), or the dead volume is only said to be determined without method (8a, 8b, 9), or not reported (2, 10, 14). instrument_identified false everywhere (no instrument named). replicates_reported true for lab 4 ambient (two instruments), lab 8 at 77 K (8a and 8b), and the consensus values with bracketed uncertainties; lab 10's two isotherms differ in flow rate and are not replicates.
- temperature_k for ambient rows is the number printed in Table 1; the ambient consensus values state no single temperature (temperature_unstated).
- extraction_confidence: 3 for separable digitized markers, 2 for markers partly overlapped or hidden (fitted on the outline), 4 for exact text values, 3 for "around/almost/plateau" text values.
