# HYC-0085 extraction log (agent B)

Xia & Mokaya 2007, J. Phys. Chem. C 111, 10035. Source: 5 page images (main-1 to main-5), no supplementary file. 83 rows written.

## Passages, tables and figures extracted from

- No tables in the paper.
- Abstract (main-1): monolith H2 uptake "at 20 bar and -196 C, of up to 3.4 wt %"; monolith surface area 1090 m2/g, pore volume 0.75 cm3/g, micropore surface area 156 m2/g. Same value as Section 3.2, so it is one row (M19).
- Section 2.2 (main-2): N2 sorption at -196 C on a Micromeritics ASAP 2020; samples oven-dried 150 C and evacuated 12 h at 200 C before N2 analysis; BET over P/P0 0.05 to 0.2; total pore volume from N2 adsorbed at P/P0 ca. 0.99; micropore area and volume from t-plot. Used for the characterization fields of both samples.
- Section 2.3 (main-2): gravimetric IGA-003 (Hiden), microbalance resolution +/-0.2 ug, -196 C, 0-20 bar, outgassed (10-10 bar) at 200 C overnight, H2 99.9999% further purified by a molecular sieve filter. Used for the method fields of every row.
- Section 3.1 (main-2, main-3): monolith 1090 m2/g, 0.75 cm3/g, micropore area 156 m2/g, average pore size ca. 38 A (pore size distribution, Figure 4 inset; method not named). Recorded on S1 rows.
- Section 3.2 (main-4): monolith "(at -196 C and 20 bar) is ca. 3.4 wt %" -> row M19, merged with the 20-bar adsorption point of Figure 7A (isotherm I1). Buoyancy-correction sentence (carbon density 1.5 g cm-3, adsorbed H2 0.04 g cm-3) -> basis_inferred excess, calibration_described true. CMK-3 "surface area of 1404 m2/g and pore volume of 1.4 cm3/g" -> S2 characterization.
- Section 3.2 continued (main-5): "the maximum hydrogen sorption capacity (at 20 bar) is the same (ca. 3.4 wt %) for both samples" -> row M65 (CMK-3, merged with the 20-bar adsorption point of Figure 7B, isotherm I2). For the monolith it repeats M19.
- Conclusions (main-5): repeats 1090 m2/g, 0.75 cm3/g, 156 m2/g, 553 m2/g / 0.5 cm3/g (silica) and "up to 3.4 wt %" at 20 bar and -196 C (= M19).
- Figure 7A (main-4): monolith H2 isotherm at -196 C, two branches. Rows M1-M18 (adsorption, filled circles), M20-M46 (desorption, open triangles); archives fig7a_adsorption_filled_circles.json, fig7a_desorption_open_triangles.json.
- Figure 7B (main-4): CMK-3 powder H2 isotherm at -196 C, two branches. Rows M47-M64 (adsorption, up-triangles), M66-M83 (desorption, down-triangles); archive fig7b_markers_both_branches.json.

## Figure digitization details

- Page image main-4.png is 1275 x 1650 px (150 dpi); markers are 5-8 px across. The figure is greyscale (`colors` finds no coloured pixels).
- Figure 7A calibration. x: 0 bar at px 748.65 (the 0 tick is hidden under the origin marker, so the y-axis line centroid was used, which is where the 0 tick sits), 20 bar at px 1117.5; check tick 10 bar at px 933.0 (predicted 9.996). Tick centroids 5 = 840.75, 15 = 1025.25 are consistent. y: 0 wt% at px 329, 3.5 wt% at px 105; check tick 2.0 at px 201 (predicted 2.000).
- Figure 7B calibration. x: 0 bar at px 754.0 (the 0 tick below the axis is in column 754, like the other ticks; the grey in column 755 belongs to the y-axis line), 20 bar at px 1118; check tick 10 at px 936 (predicted 10.000). y: 0 wt% at px 611, 3.5 wt% at px 402; check tick 2.0 at px 491.5 (predicted 2.001).
- Figure 7A, symbol key: none printed. The text says the plot shows adsorption and desorption ("the desorption closely matches adsorption"). The filled circles (integer pressures 3-19 bar, plus 1.25, 1.75 and 2.0 bar) lie on the slightly lower trace and are coded adsorption; the open triangles (half-integer pressures 2.5-18.5 bar, plus 20, 1.5 and 0-1.0 bar) lie on the slightly upper trace and are coded desorption. This follows the usual filled/open convention, and the upper desorption trace agrees with it. The paper does not state it.
- Figure 7A adsorption run: colour #000000, tolerance 100, 4-px opening, ROI 751,107-1125,327, marker size 15-45 px. 18 markers were extracted: 1.19 bar and 3-19 bar.
- Figure 7A adsorption, markers not separable (not extracted, but counted):
  - two overlapping filled circles at about 1.75 and 2.0 bar. They form one 60-px blob, rejected as too large and recorded in the archive.
  - the circles that lie under open triangles, where only a ring shows: at the origin, at 8 low-pressure positions (about 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 and 1.0 bar), at 1.5 bar and at 20 bar. At 20 bar the visible ring looks open rather than filled. At this resolution I cannot tell whether these hidden circles are filled or open; they are counted as adsorption points.
  - The 20-bar adsorption point is the one the text value 3.4 wt% merges with (M19).
  - Adsorption count: 18 extracted + 2 merged + 11 hidden = 31.
- Figure 7A desorption run: the open triangles cannot be isolated by their black outlines, because those touch the connecting lines and the other markers. Their opaque white interiors were isolated instead: colour #FFFFFF, tolerance 40, no opening, ROI 750,106-1126,333, marker size 3-6 px. That size window keeps every triangle interior and drops the background, the letter counters of "A" and "Monolithic carbon" (7-46 px), and 1-2 px gaps along the lines. 27 markers were extracted. The marker centre is the interior centroid, about 1 px below the symbol's box centre (under 0.02 wt%). The 20-bar triangle digitizes at 19.89 bar.
- Figure 7A desorption, marker not separable: the triangle at the axes origin (about 0 bar, 0 wt%). Its interior is 1-2 px because the marker sits on both axis lines, so it was rejected as too small; it is counted. Also rejected: a 2-px white gap between the y-axis and the curve line at y 322-323, which is not a marker.
  - Desorption count: 27 + 1 = 28. Isotherm I1 point count: 31 + 28 = 59.
- Figure 7B, symbol key: none printed. Both branches use filled triangles of the same grey level, so the tool cannot separate them by colour, and the panel is one archive holding both series. Up-triangles (integer pressures 3-19 bar, lower trace) are coded adsorption and down-triangles (half-integer pressures 2.5-18.5 bar, upper trace) desorption. Each extracted marker was assigned by orientation, checked on the pixel pattern of every blob (wide top = down-triangle, wide bottom = up-triangle), and by its trace.
- Figure 7B run: colour #000000, tolerance 60, 2-px opening, ROI 750,397-1126,610, marker size 7-30 px. 38 blobs were extracted, of which 36 are single markers and were written as rows:
  - the 34 markers from 2.5 to 19 bar;
  - the two lowest markers at about 0.01 bar, an up-triangle at 0.316 wt% and a down-triangle at 0.394 wt%, which touch apex to apex on the y-axis line (confidence 2).
- Figure 7B, markers not separable (counted, not written as rows):
  - (a) the blob at 0.10 bar, 0.716 wt%, which is a down-triangle and an up-triangle superimposed about 2 px apart;
  - (b) the 20-bar blob at 19.94 bar, 3.374 wt%, an up- and a down-triangle superimposed. It is the point M65 merges with;
  - (c) four merged clusters between about 0.15 and 2.0 bar (blobs of 34, 49, 57 and 48 px, rejected as too large and recorded in the archive). By the wide top and bottom edges they hold about 17 markers: about 9 up- and 8 down-triangles, including the 1.5-bar pair and up-triangles at about 1.75 and 2.0 bar.
  - Isotherm I2 point count: about 29 adsorption + 28 desorption = 57. The low-pressure part of this count is approximate (plus or minus 2) because of the overlap.
- Instruction step 6 (marker count): every marker the tool could not isolate is listed above, and none of those archive points was written as a row.
- The tool's own `check` (stated value against digitized series) could not be run. The only stated value, 3.4 wt% at 20 bar, lies beyond the extracted range of every archive (7A adsorption ends at 19.0 bar, 7A desorption at 19.89 bar, 7B at 19.94 bar). Compared by hand:
  - 7A 20-bar desorption marker: 3.320 wt%, -2.4% from "ca. 3.4";
  - 7B 20-bar blob: 3.374 wt%, -0.8%.
  - The archives therefore stay status "unchecked".

## Values seen but not extracted

- Introduction (main-1) and Section 3.2 (main-4), literature comparisons: these are other papers' measurements cited for comparison, not measurements made in this paper.
  - Pang et al., 1.78 wt% at ambient pressure and -196 C (2314 m2/g mesoporous carbon);
  - Terres et al., 2.7 wt% at -196 C and 60 bar (MCM-48-templated carbon);
  - zeolite-templated carbons, 2.6 wt% at ambient pressure and close to 7 wt% at 20 bar and -196 C.
- Mesoporous silica (SBA-15) monolith: not a carbon sorbent, and it has no H2 uptake value. Its characterization: surface area 553 m2/g, pore volume 0.5 cm3/g, average pore size ca. 38 A, no microporosity (Section 3.1, Abstract, Conclusions; Figure 4).
- Figure 4 (N2 isotherms and pore size distribution of silica and carbon monoliths): not an H2 isotherm, so not digitized. The values it supports are in the text.
- Figure 3 (TGA/DTG of the carbon monolith): mass-loss events at ca. 45 C (water), ca. 535 C (amorphous carbon) and ca. 630 C (graphitic carbon). Residual mass above 700 C is below 1 wt% (typically 0.5-0.8 wt%), which is silica residue, noted in the S1 description. Not an H2 quantity.
- Figure 5 (XRD): carbon wide-angle peaks at 2theta ca. 26 deg and 43 deg ((002), (101)). No d-spacing is printed, so interlayer_spacing_nm is left empty rather than computed. One low-angle peak is attributed to (110).
- Figures 1, 2 and 6 (photographs, SEM, TEM): no H2 data. Monolith dimensions: silica 2.0 cm high x 1.0 cm diameter, carbon 1.8 cm x 0.8 cm.
- "Although the powder sample has a higher uptake capacity at lower pressure": no number given.
- Microbalance resolution +/-0.2 ug: an instrument resolution, not an uncertainty of any uptake value, so replicates_reported is false and uncertainty_wt_pct is empty.

## Coding decisions worth checking

- Sample labels are taken from the Figure 7 in-plot panel labels: "Monolithic carbon" (S1) and "Powdered carbon" (S2). The caption names, "mesoporous carbon monolith" and "powdered mesoporous carbon CMK-3", are in material_description.
- S2 (CMK-3): the paper does not describe its preparation or say how its area was measured. Coded as follows, with the reasons in notes:
  - synthesis_method template_synthesis, because CMK-3 is by name an SBA-15 replica;
  - surface_area_method BET with probe N2, bet_range_stated true and pore_volume_method other, from the general Section 2.2;
  - area_same_sample yes, because the text attaches the area to the same CMK-3 sample whose isotherm is shown.
- S1 synthesis_method is template_synthesis (CVD nanocasting inside a silica template); `cvd` would also be defensible. HF template removal is recorded in purification_method.
- Basis: not named. Gravimetric with a stated buoyancy correction gives basis_inferred excess (instrumental default), basis_stated false and uptake_type unspecified.
- skeletal_density_g_cm3 = 1.5 is the assumed carbon density used for the buoyancy correction, not a measured value.
- degas_duration_h is empty ("overnight"). degas_end_pressure_pa = 1e-05 (printed 10-10 bar). Degassing for the H2 measurement is 200 C. The 150 C / 200 C, 12 h conditions belong to the N2 analysis.
- The text values (M19, M65) are uptake_bound approximate ("ca. 3.4") and value_kind measured (merged with the 20-bar adsorption point of each isotherm).
