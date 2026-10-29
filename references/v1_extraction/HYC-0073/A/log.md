# HYC-0073 extraction log (extractor A)

## Extracted from

- Table 1 (main.pdf p.3, journal p.225): 20 bar and 1 bar uptake of Zr-CDC, AC-600, AC-700, AC-800, AC-900 (10 rows, table_direct), with BET area, micropore area, total and micropore pore volume for each sample (carried on every row of that sample). Pore size maxima (8/13, 8/13, 13/20, 6/12/22, 12/23 A, NLDFT, N2) are in notes only; they are several maxima, not an average, so average_pore_diameter_nm is empty.
- Results text (main.pdf p.4, journal p.226), Zr-CDC2: 2.8 wt% at -196 C and 20 bar, area 1302 m2 g-1, pore volume 0.63 cm3 g-1 (1 row, text_direct, no isotherm_id; Zr-CDC2 has no plotted isotherm).
- Fig. 3 (main.pdf p.4, journal p.226), H2 isotherms at -196 C (77.15 K), five curves with markers, digitized with digitize_figure.py markers mode: 109 digitized rows. The five 20 bar end markers are the same measurement as the five 20 bar Table 1 values (printed pressure 20 bar within 0.4 bar of the plotted end marker at 19.96-19.99 bar), so they are recorded once, on the Table 1 rows, with the digitized point in notes.
- Experimental section (main.pdf p.2-3): instrument, H2 purity, outgassing, buoyancy correction, assumed density 1.5 g cm-3, BET P/Po range 0.02-0.22, N2 probe, t-plot, KOH activation conditions, washing. Applied to every row.

## Sample numbering

S1 Zr-CDC, S2 AC-700, S3 AC-800, S4 AC-600, S5 AC-900, S6 Zr-CDC2, in order of first printed label: the Fig. 1 caption (main.pdf p.2) names AC-700 and AC-800 before AC-600 and AC-900 appear in Fig. 2 and Table 1. Isotherm ids follow the sample numbers: I1 Zr-CDC, I2 AC-700, I3 AC-800, I4 AC-600, I5 AC-900. Labels in material_description are the Table 1 labels.

## Fig. 3 digitization

- Calibration on the page image main-4.png (1241 x 1625): x ticks 0 bar at px 227.5 and 20 bar at px 500.5, checked on 10 bar (px 364.0, error 0.0); y ticks 0 wt% at px 382.0 and 6 wt% at px 130.0, checked on 3 wt% (px 255.5, relative error 0.4%). Tick pixels from inspected pixel rows and columns.
- The figure is greyscale with hollow white-filled markers of 6-7 px, so the colour isolation of the tool cannot separate the five series. Adaptation: marker interiors (white holes enclosed by the marker outline) were located in the page image by thresholding an 8x enlargement; each marker was then drawn as a solid blob of about 3 px radius centred on its hole (stars, which are dense with no usable hole at most pressures, were taken as the dense core of the ink). One mask image per series, and several per series where neighbouring markers are closer than 8.5 px, were built in the work directory (work/series_img/, built by work/s/build_series2.py) with the same pixel grid as the page image, so the calibration pixels above apply unchanged. digitize_figure.py extract --mode markers (tolerance 40, open-px 2, ROI 229 116 503 380) then measured the centroid of every blob. The tool returned exactly one point per blob, 0.00-0.46 px from the hole or core position. The series membership of each marker came from marker shape and vertical order, checked on enlarged overlays.
- Archives (out/digitizations/): HYC-0073_Fig3_<series>.json for Zr-CDC (3 files), AC-600 (2), AC-700 (2), AC-800 (1), AC-900 (2); the *_set2/_set3 files hold markers that touch their neighbours and could not share an image. Every file also holds the series' 20 bar marker so that each could be checked; that duplicate is used once. All ten archives passed digitize_figure.py check against the Table 1 20 bar value at x = 19.96-19.99 (the last marker, since the tool does not accept x = 20): Zr-CDC +2.44% (digitized 3.893 vs printed 3.8), AC-600 -0.33%, AC-700 +0.79%, AC-800 -0.70%, AC-900 -0.75%. The 1 bar values cannot be checked, see below.
- Digitized values for the last marker of Zr-CDC (3.893) and AC-700 (6.048) differ from the printed 3.8 and 6.0 by more than printed rounding; the printed values are kept.
- Axis range: AC-700 and AC-900 markers above 6 wt% lie beyond the highest labelled y tick (6), inside the plot frame; the tool flags them as outside the calibrated range.
- Stars (AC-900) overlap the AC-700 squares and the connecting lines. Star positions with no hole (p = 2, 3, 7, 8, 10, 11, 12, 16, 17, 19, 20 bar) were found as the densest 5 x 5 px ink region within 3.5 px of a cubic-spline estimate through the stars that do have a hole (shift 0.2-0.9 px), then centroided by the tool.
- Branches: the paper says the isotherms are reversible with no hysteresis and does not mark which markers are adsorption and which desorption. Many pressures show two overlapping markers (twin pair, 3-4 px apart vertically; for Zr-CDC at 1.2, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13 and 14.5 bar, AC-600 near 19 bar, AC-700 at 16 bar). Each resolvable twin is a row; all rows are coded adsorption by the rule, with the pair noted. The lower marker of a Zr-CDC pair has its hole partly covered by the upper marker, so its centroid may sit up to about 1 px (0.02 wt%) low.
- isotherm_point_count is the number of markers identified (extracted plus identified but not extracted): Zr-CDC 34, AC-600 23, AC-700 20, AC-800 19, AC-900 20. It is a lower bound for every isotherm, because markers at low pressure overlap and cannot be counted (see below). Step 6 (extracted equals counted) holds for the separable markers only.

## Fig. 3 markers seen but not extracted

- All series, p below about 1.2 bar: the markers of the five curves and of both branches form one dark column along the y axis (about 35 enclosed cells, none assignable to a series); not extracted, not counted.
- AC-700, AC-800, AC-900, p between 1.2 and 2 bar (cells at about 1.5 and 1.7 bar, y 2.9-3.2 wt%, and small holes at about 1.3-1.7 bar): overlapping squares, diamonds and stars that cannot be assigned to a series; not extracted. Extraction for these three curves starts at 2 bar.
- AC-600 triangles at 1.19, 1.50, 1.69 bar are extracted (confidence 2, partly overlapped); nothing below 1.19 bar.
- Zr-CDC: lower marker of the pair at 11.5 bar (hole covered by the upper marker) and at 1.5 bar (hole 2.9 px2, elongated) not extracted; markers below 1.16 bar not extracted. Single Zr-CDC markers at 2.5 and 3.5 bar show no second marker.
- Small enclosed cells between nearly parallel connecting lines (aspect ratio above 2.3, or lens-shaped, for example at 2.7, 3.7, 11.2, 15.4 bar) are not markers and were not extracted.
- The 1 bar markers of all five curves lie inside the overlapping cluster; no digitized point could be assigned to a curve at 1 bar. The five 1 bar Table 1 values are therefore rows with no digitized point. They carry the curve's isotherm_id because the paper presents Table 1 uptake at 20 bar and 1 bar as the capacity of the Fig. 3 isotherms.

## Seen, not extracted

- Abstract, Broader context, Conclusions: 3.8, 4.9-6.2, 5.8-6.2 wt% at -196 C and 20 bar and 2.2-2.7 wt% at 1 bar for the samples of this paper; same measurements as Table 1 (not repeated). "Enhancement up to 63%" and "ca. 30%" are computed by the authors from Table 1; not rows.
- Introduction: 7.08 wt% (-196 C, 20 bar, doubly activated carbon, 3190 m2 g-1, ref. 7), 3.0-5.2 wt% (activated carbons, refs 8, 9), 6.9 wt% (zeolite-templated carbon, ref. 13), 4.3 wt% (CDC, 35 bar, ref. 14): literature values for materials not measured in this paper; not extracted.
- SI Supplementary Table 1 (si1.pdf p.3): H2 uptake at 20 bar and 1 bar for 13 literature activated carbons (AC I, M30, KUA3, KUA4, KUA5, KUA6, Carbon A, AX-21, Carbon B, PK775C, MK725, APOR8, PC76; surface areas 1694-3808 m2 g-1; refs 1-6 of the SI, other laboratories): compilation of other groups' values, not measurements in this paper; not extracted.
- SI Figures 1 and 2: differential thermogravimetric profiles from temperature-programmed desorption in helium (oxygen groups, not H2 uptake); no values.
- Fig. 2a (N2 isotherms) and 2b (pore size distributions), Fig. 1 (XRD): not H2 data.
- Fig. 4a, 4b (uptake against surface area and pore volume) and Fig. 5 (uptake per area against main pore size): not isotherms, not digitized; the values they show (Zr-CDC2 2.8 wt%, the Table 1 uptakes, the Chahine line) are given in text and table, so nothing is missing from them.
- Text: main pore size 20-23 A for AC-700, AC-800, AC-900 (22 A for AC-800) and "smallest pores" for AC-600/Zr-CDC; several pore size maxima per sample, so average_pore_diameter_nm is empty for every sample.
- Samples with characterization but no uptake: none. Zr-CDC precursor ZrC and Cl2 (Aldrich), not sorbents.

## Coding decisions

- uptake_type unspecified, basis_stated false (the paper never names excess, absolute or total); basis_inferred excess because the gravimetric data are stated to be corrected for buoyancy. wt% only is printed, so wt_pct_convention unknown, source none.
- instrument_identified false: "intelligent gravimetric analyser, IGA, (Hiden)" gives the manufacturer and product line but no model number. calibration_described true (buoyancy correction stated); free_volume_calibration empty (not applicable to a gravimetric correction, and no gas or temperature stated).
- skeletal_density_g_cm3 1.5 is the density the authors assumed for the buoyancy correction, not a measured density.
- degas_end_pressure_pa 1e-5 = 10^-10 bar (printed in the Experimental section, main.pdf p.2); degas_duration_h empty ("overnight" is not a number). The 12 h at 200 C evacuation is for the N2 sorption, not for H2.
- temperature_k 77.15 = -196 C + 273.15; temperature printed as a number, so temperature_inferred false.
- replicates_reported false: the SI says several AC-800 samples were prepared and were very similar, with no results or uncertainty.
- area_same_sample yes: the nitrogen and hydrogen measurements are on the same carbons in the same state (both outgassed at 200 C). Zr-CDC2: BET method and N2 probe taken from the general Experimental statement.
- measuring_lab_id: corresponding author Mokaya (marked *), first affiliation School of Chemistry, University of Nottingham.
- material_class carbide_derived_carbon and synthesis_method carbide_chlorination for all samples (the KOH-activated samples are activated CDC; surface oxygen is not a built-in dopant). No residual Zr found (XRD, TGA, XRF), so residual_metal is empty.
- extraction_confidence: Table 1 rows 5, Zr-CDC2 text row 4, digitized 3, and 2 for stars, lower markers of twin pairs, markers partly covered by neighbours and the low-pressure AC-600 and Zr-CDC markers.
