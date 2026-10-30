# HYC-0103 extraction log (extractor A)

## Extracted from

- main.pdf p.3 (printed p.11316), Table 1, hydrogen uptake column: 20 values at -196 C, 10 samples (ZTC1-ZTC5, Ac-ZTC1-Ac-ZTC5) x {20 bar, 1 bar (footnote g, in parentheses)}. All 20 are rows (`table_direct`). Their characterization (BET area, t-plot micropore area, total and micropore pore volume, DFT pore size maxima) is carried on the rows.
- main.pdf p.4 (printed p.11317), Figure 3 (H2 uptake isotherms, 0-20 bar, wt%, -196 C): six series, panels a-f = ZTC3, ZTC2, ZTC1, Ac-ZTC3, Ac-ZTC2, Ac-ZTC1 (caption). Digitized with `digitize_figure.py extract --mode markers`; archives in `digitizations/` (one per series, status `passed`). 150 digitized rows; the six 20 bar Table 1 values and one 1 bar Table 1 value merged with a plotted point are table rows (see below).
- main.pdf Section 2.2 and 2.3 (text): BET range 0.06-0.22 P/P0 (N2, -196 C, ASAP 2020), t-plot micropore area and volume, total pore volume at P/P0 ~0.99; H2 99.9999% with molecular sieve filter; Hiden IGA-003 gravimetric analyzer (manufacturer and model named); degassing 10-7 bar, 120 C, overnight; buoyancy correction with carbon density 1.5 g/cm3 and hydrogen density 0.04 g/cm3. Section 2.1: synthesis and KOH activation conditions. Used for the sample fields, no uptake values.
- Sample numbering: S1-S5 = ZTC1-ZTC5, S6-S10 = Ac-ZTC1-Ac-ZTC5; isotherm I<n> belongs to S<n> (I4, I5, I9, I10 are the 1 bar / 20 bar value pairs of samples with no plotted curve, 2 points each).

## Table 1 values merged with plotted points (one row, no separate digitized row)

20 bar values of ZTC1, ZTC2, ZTC3, Ac-ZTC1, Ac-ZTC2, Ac-ZTC3 are the last plotted marker of their Figure 3 curve (printed 20 bar within 0.4 bar of the marker; digitized 19.924, 20.021, 19.926, 19.972, 19.986, 20.007 bar). The 1 bar value of Ac-ZTC3 (2.0 wt%) is merged with the plotted marker at 1.0095 bar (2.0084 wt%), within 0.02 bar. Each such row carries `digitized: <bar>, <wt%>, archive: <file>` in notes and the isotherm_id of the curve. `digitize_figure.py check` against the Table 1 20 bar values passed for all six (differences 0.46-2.54%, below 5%).

## 1 bar Table 1 values with a plotted curve but no merged point

ZTC1, ZTC2, ZTC3, Ac-ZTC1 and Ac-ZTC2 have a Figure 3 curve, but no separated plotted marker lies within 0.02 bar of 1 bar (markers overlap near 1 bar), and the paper says only that the isotherms are in Figure 3 and the capacity at 1 and 20 bar is in Table 1, not that the 1 bar value was read from the curve. These five 1 bar rows therefore have no isotherm_id (no point count). A reconciler may judge otherwise.

## Figure 3 digitization details

- Page image main-4.png (150 dpi). Axes calibrated on tick pixels found by inspecting pixel rows and columns: x 0 bar at 209.0 px, 20 bar at 497.7 px, verified on 10 bar at 353.45 px (tool: 0.07% error); y 0 wt% at 319.3 px, 6 wt% at 108.0 px, verified on 3 wt% at 213.35 px (0.28% error).
- Filled series (ZTC1 red circles, ZTC2 blue squares, ZTC3 green down-triangles): run on the page image itself, 3-px opening (ZTC3: 2-px opening, minimum marker 3 px, because 3 px erased some triangles).
- Open series (Ac-ZTC1 red circles, Ac-ZTC2 blue squares, Ac-ZTC3 green down-triangles): the tool's opening removes thin outlines, so I made derived images in the work directory (same geometry, `work/holes_final_<colour>.png`) in which only the white interiors of open markers are painted in the series colour, built with scipy hole filling after removing the filled markers of the same colour. The tool was run on these images with 1-px opening, so each point is the centre of one open marker's interior. Calibration is unchanged. Two local repairs on these images: Ac-ZTC2 marker at 15 bar had its interior split in two by the connecting line (bridged with a 3x1 vertical closing in a small window); Ac-ZTC3 marker at 15 bar was missed at the base threshold and was taken from a stricter pass inside a 12 x 15 px window.
- Marker counts (separated markers kept as points / detections in archive): ZTC1 28/30, ZTC2 28/30, ZTC3 28/29, Ac-ZTC1 26/27, Ac-ZTC2 22/22, Ac-ZTC3 25/25. isotherm_point_count equals the number kept, so it is a lower bound.
- Detections not used as points (merged or partly hidden markers, centroid is not one marker's centre): ZTC1 0.210 bar/0.863 wt% (33 px, about two markers) and 1.122 bar/1.494 wt% (173 px, cluster); ZTC2 0.208 bar/0.534 wt% (12 px, partly hidden) and 0.778 bar/0.949 wt% (96 px, cluster); ZTC3 0.752 bar/0.591 wt% (220 px, cluster); Ac-ZTC1 1.124 bar/2.728 wt% (18 px, two interiors merged).
- Markers not separated: below about 2 bar the six curves are dense and overlap each other. The solid-marker clusters of ZTC1, ZTC2 and ZTC3 (below about 2.0, 1.0 and 2.0 bar), and several open markers of all three activated samples below about 1.1 bar, cannot be separated at this resolution, so the extracted marker count does not equal the true count there. Not counted, not extracted.
- Pressure positions: separated markers sit at round pressure values (for example 2.5, 3, 3.5, ... 20 bar for ZTC1 and ZTC3; 2, 3, 4, ... 20 bar for Ac-ZTC2), consistent with the digitized x values (within 0.08 bar). The digitized x values are stored, not the round values.
- Branches: the text says the isotherms are completely reversible with no hysteresis; branches are not distinguishable in Figure 3, so every plotted marker is coded adsorption.

## Seen but not extracted

- Figure 4A and 4B (H2 uptake at 20 bar against surface area and pore volume), SI Figure S6A and S6B (against micropore area and volume): not isotherms; the values are Table 1 values; not digitized.
- Text, Figure 4B discussion: 3.61, 3.35, 3.22, 3.0 and 2.86 wt%/cm3 (Ac-ZTC1, Ac-ZTC2, Ac-ZTC4, Ac-ZTC5, Ac-ZTC3): uptake per unit total pore volume, a derived ratio, not an uptake.
- Text, p.11317: volumetric capacity "19-28 g of H2/L" for ZTCs and "26-37 g of H2/L" for Ac-ZTCs, estimated by the authors from assumed packing densities of 0.8 and 0.6 g/cm3: ranges over samples, no per-sample value printed, packing densities assumed; not extracted.
- Abstract and text: "60 and 96%", "84%", "from 2.4-3.5 wt % ... to between 4.3 and 6.1 wt %", "1.9-2.6 wt %" and "0.8-1.5 wt %" at 1 bar, "6.1 wt % at 20 bar" for Ac-ZTC1, "2.4 to 4.7 wt %" for ZTC3: restatements or derived percentages of Table 1; no new value.
- Text, p.11314: literature values for other materials ("6.9 wt % (at 77 K and 20 bar)", "~3.0 to 5.3 wt %", "~0.8 to 2.3 wt % (at 77 K and 1 bar)", refs 8, 11, 16-18): not measurements of this paper.
- Text, Figure 3 discussion: "no saturation is achieved even at 20 bar": no value.
- SI Table S1 (si1.pdf p.2): ZTC6, ZTC7, ZTC8, Ac-ZTC6, Ac-ZTC7, Ac-ZTC8 have textural data only, no H2 uptake, so no rows. Characterization (surface area m2/g, micropore area in parentheses; pore volume cm3/g, micropore volume in parentheses; DFT pore size maxima nm): ZTC6 1084 (792), 0.66 (0.37), 1.2/2.5; ZTC7 916 (667), 0.57 (0.31), 1.3/2.5; ZTC8 720 (551), 0.41 (0.26), 1.2/2.5; Ac-ZTC6 867 (138), 0.75 (0.06), 1.3/3.4; Ac-ZTC7 980 (156), 0.85 (0.07), 1.3/3.5; Ac-ZTC8 1112 (146), 0.91 (0.06), 1.3/3.4.
- SI Figure S5 (isosteric heat against uptake): not an uptake value or isotherm; not digitized.
- Figures 1 and 2, SI Figures S1-S4: N2 isotherms, pore size distributions and XRD; no H2 uptake.

## Inconsistencies and choices

- ZTC1 CVD temperature: 800 C in Section 2.1, "prepared at 700 C" in the Results text; description uses 800 C and the row notes record the conflict.
- No metal hydride, zeolite or MOF comparison material is measured in the paper.
- The paper does not name the uptake basis ("excess", "absolute" or "total" never appear): uptake_type `unspecified`, basis_stated false, basis_inferred `excess` from the stated buoyancy correction on a gravimetric measurement.
- wt% convention not stated and no paired units: convention `unknown`, source `none`.
- skeletal_density_g_cm3 = 1.5 on every row is the carbon density the authors assumed for the buoyancy correction, not a measured sample property (stated in notes).
- Degassing duration "overnight" is not numeric and is left empty; 10-7 bar stored as 0.01 Pa.
- Temperature -196 C stored as 77.15 K (printed number, not inferred).
- Table 1 does not name the surface-area method; Section 2.2 names BET (P/P0 0.06-0.22) with N2, so method BET, probe N2; no consistency criteria stated.
- DFT pore size maxima are two values per sample (for example 1.3/2.2 nm), so average_pore_diameter_nm is empty and the maxima are in notes.
