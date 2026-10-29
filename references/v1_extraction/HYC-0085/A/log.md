# HYC-0085 extraction log (agent A, claude-sonnet-5-5, 2026-10-29)

71 rows written: 36 for S1 (I1), 35 for S2 (I2). Validator: 0 errors; only warning is uptake_type = unspecified (paper never names the basis).

## Passages, tables and figures extracted from

- Abstract (page 1, main.pdf): "hydrogen uptake capacity, at 20 bar and -196 C, of up to 3.4 wt %" for the carbon monolith. Same value as Section 3.2 text; one row (M19).
- Section 2.1 (page 2): synthesis of S1 (CVD nanocasting, acetonitrile, 950 C, 3 h, SBA-15 monolith template, HF etch). Used for S1 description and synthesis_method.
- Section 2.2 (page 2): N2 sorption at -196 C, ASAP 2020; BET P/P0 0.05 to 0.2; total pore volume at P/P0 ca. 0.99; micropore surface area and volume by t-plot; N2 degassing 150 C oven dry then 12 h at 200 C (this is N2 degassing, not used in the H2 degas fields).
- Section 2.3 (page 2): IGA-003 (Hiden) gravimetric, -196 C, 0-20 bar, outgassed 10^-10 bar at 200 C overnight, H2 99.9999% purified. Used for instrument, degas, purity.
- Section 3.1 (page 3): S1 BET 1090 m2/g, pore volume 0.75 cm3/g, micropore surface area 156 m2/g, average pore size ca. 38 A (pore size distribution, Figure 4 inset; method not named).
- Section 3.2 (pages 4-5) and Figure 7 caption: buoyancy correction with carbon density 1.5 g/cm3 and H2 density 0.04 g/cm3 for adsorbed H2; "ca. 3.4 wt %" at 20 bar for S1 (M19); "saturation is not achieved at 20 bar"; CMK-3 surface area 1404 m2/g, pore volume 1.4 cm3/g; "maximum hydrogen sorption capacity (at 20 bar) is the same (ca. 3.4 wt %) for both samples" (S2 text row, M54).
- Figure 7A (page 4, main-4.png): S1 77 K isotherm, digitized. Rows M1-M18 (filled circles, adsorption), M20-M36 (open triangles, desorption). M19 is the text value merged with the 20 bar marker (digitized point recorded in notes, no separate digitized row).
- Figure 7B (page 4, main-4.png): S2 (CMK-3) 77 K isotherm, digitized. Rows M37-M53 (up-triangles, adsorption), M55-M71 (down-triangles, desorption). M54 is the text value merged with the 20 bar marker.

## Figures and values seen but not extracted

- Figure 4 (N2 isotherms of silica and carbon monolith, pore size distribution inset): not an H2 isotherm, not digitized. Values it shows are in the text.
- Figure 3 (TGA/DTG), Figure 5 (XRD), Figures 1, 2, 6 (photograph, SEM, TEM): not H2 data. TGA residual mass above 700 C "less than 1 wt % (typically 0.5-0.8 wt %)" is recorded in the S1 description only; no residual metal field set (silica, not metal).
- Mesoporous silica monolith (SBA-15 template): 553 m2/g, 0.5 cm3/g, no microporosity. Characterization only; no H2 uptake value and not a carbon sorbent. No row.
- Literature comparison values quoted in the Introduction and Section 3.2 (other authors' samples, not measured here): 1.78 wt % at ambient pressure and -196 C for a 2314 m2/g mesoporous carbon (Pang, ref 15); 2.7 wt % at -196 C and 60 bar for MCM-48-templated carbon (Terres, ref 16); zeolite-templated carbons "up to 2.6 wt % at ambient pressure and close to 7 wt % at 20 bar and -196 C" (ref 17). Not this paper's measurements; no sample description; no rows.
- Carbon density 1.5 g/cm3 and H2 density 0.04 g/cm3 (buoyancy correction): these are assumed analysis parameters, not a measured skeletal density or adsorbed-phase density at a stated pressure. Recorded in notes only; skeletal_density_g_cm3 and adsorbed_phase_density_kg_m3 left empty.
- Sample mass for H2 runs, degas duration ("overnight"), free-volume/He calibration gas and temperature, uncertainties: not stated; left empty or coded false.
- No consensus, multi-laboratory or mean values in the paper.

## Coding decisions worth a second look

- Labels: no table; the first figure caption showing H2 uptake (Figure 7) gives "mesoporous carbon monolith" (S1) and "CMK-3" (S2). In-plot panel labels are "Monolithic carbon" and "Powdered carbon"; Figure 4 labels the monolith "Mesoporous carbon". All listed in material_description.
- synthesis_method S1 = template_synthesis (hard-template nanocasting; CVD is the infiltration step and is named in the description). A reconciler may prefer cvd. S2 = unknown: the paper does not describe how the CMK-3 was made or obtained. S2 material_class templated_carbon rests on the name "CMK-3" and the paper's description of CMK-3 type carbons as nanocast mesoporous carbons.
- S2 surface area 1404 m2/g and pore volume 1.4 cm3/g: method not named, not stated as measured by the authors: surface_area_method = unspecified, area_same_sample = unclear, probe gas N2 taken from the general N2 sorption description, BET-range fields left empty (area not coded as BET).
- Basis: not named. Buoyancy correction stated, so basis_inferred = excess by the gravimetric default; basis_stated = false; uptake_type = unspecified. The correction uses an adsorbed-phase H2 density (0.04 g/cm3), which could mean an absolute-type correction; recorded in notes.
- wt% convention: never defined and no paired units: unknown / none.
- "ca. 3.4 wt %" read as uptake_bound = approximate. value_kind = measured because the value is at the highest plotted pressure and within 3% of the digitized 20 bar marker (S1: 3.32295 digitized, 2.3% below 3.4; S2: 3.37588, 0.7% below).
- Branch assignment: neither Figure 7A nor 7B has a legend. Figure 7A: text says "the desorption closely matches adsorption", so two branches are drawn; filled circles are at integer pressures 1..19 and open triangles at half-integer pressures 18.5..1.5, desorption values slightly above adsorption: circles = adsorption, triangles = desorption. Figure 7B: two filled-triangle series, up-triangles at integer pressures and down-triangles at half-integer pressures (checked by shape at 2.5-5 bar), same pressure grid as 7A; the text never mentions desorption for CMK-3, so this assignment is by analogy only. A reader who does not accept it should treat the 7B down-triangle rows (M55-M71) as unlabelled-branch.
- Temperature: "-196 C" printed, stored as 77.15 K, temperature_inferred = false.
- isotherm_point_count (61 for I1, 62 for I2) is approximate: below ca. 2 bar the markers of both branches overlap (spacing ca. 0.1 bar, markers ca. 7 px wide) and cannot be counted one by one. I1 count: 29 triangles (white-interior outlines found by hole detection: 10 at 0 to 1.0 bar, 1.5, 2.5 to 18.5 in steps of 1, and 20) plus 32 circles (18 separated, 2 merged near 1.8 and 2.0, 1 hidden at 1.5, 1 at 20, about 10 hidden below 1.2 inferred to mirror the triangles). I2 count: 34 separated plus 2 at 20 bar, plus about 26 in the overlapped region below 2.5 bar (about 12 overlapped pairs below 1.5 bar and the merged blobs at 1.5 and 2.0 bar).

## Digitization record

Page image: pages/main-4.png (1275 x 1650 px). All tick positions found by sub-pixel darkness centroids of the tick marks and axis lines; calibration on the lowest and highest labelled tick of each axis, third labelled tick as residual check.

Figure 7A (frame: left axis x = 748.46 px, bottom axis y = 329.04 px, top frame y = 105.0 px):
- x: 0 bar at 748.46 px, 20 bar at 1117.5 px; other ticks found at 5: 840.78, 10: 933.0, 15: 1025.25. Verify tick 10 bar at 933.0 px: relative error 0.011%.
- y: 0.0 wt% at 329.04 px, 3.5 wt% at 105.0 px; other ticks at 0.5: 297.18, 1.0: 265.18, 1.5: 232.82, 2.0: 201.0, 2.5: 169.0, 3.0: 137.0. Verify tick 2.0 wt% at 201.0 px: relative error 0.013%.

Figure 7B (left axis x = 754.13 px, bottom axis y = 611.0 px; the y axis runs to above 3.5, frame top at 396 px):
- x: 0 bar at 754.0 px, 20 bar at 1118.0 px (ticks 5: 845.0, 10: 936.0, 15: 1027.0). Verify tick 10 bar: relative error 0.0%.
- y: 0.0 wt% at 611.0 px, 3.5 wt% at 402.0 px (ticks 0.5: 581.68, 1.0: 551.16, 1.5: 521.5, 2.0: 491.5, 2.5: 461.76, 3.0: 431.84). Verify tick 2.0 wt%: relative error 0.06%.

Archives (all in digitizations/, colour #000000, mode markers):
- HYC-0085_fig7A_adsorption_circles.json: tolerance 40, 3 px opening, region 752 108 1124 326, marker size 6-40 px. 18 points (1.2, 3 to 19 bar). Rejected by size: the merged blob of two filled circles near 1.8 and 2.0 bar (56 px, pixel centre 783.5, 269.5); not turned into a point. Status unchecked: the paper states no value inside 1.2-19 bar for this series; same calibration as the passed archive below.
- HYC-0085_fig7A_20bar_marker.json: one-marker region 1109 110 1123 122, tolerance 160, no opening. One point (19.9314 bar, 3.32295 wt%): the 20 bar circle and triangle overlap and give one glyph. Step-6 check against the paper's 3.4 wt % at 20 bar, at x = 19.9314 (the point's own x; the tool needs x inside the extracted range): difference 2.27%, passed (5% tolerance).
- HYC-0085_fig7A_desorption_triangle_<p>.json, p = 02.5 ... 18.5 (17 files, one per marker): the open triangles are hollow and joined by the connecting line, so one tool run per marker with a 11 x 11 px region centred on the marker (centred from the white interior of each outline), tolerance 200, no opening. One component each (24-32 px). The point is the centroid of the outline pixels in the region; for a hollow triangle this sits about 1.5 px (0.02 wt%) below the marker centre (outline base is the thick edge). Not corrected. Status unchecked (no paper-stated value in range; same calibration).
- HYC-0085_fig7B_triangles.json: tolerance 40, 2 px opening, region 757 398 1124 608, marker size 8-25 px. 39 points. Rows were written for the 34 separated markers from 2.5 to 19 bar (17 up-triangles at integer pressures, 17 down-triangles at half-integer pressures) and the 20 bar glyph (19.9515 bar, 3.37588 wt%; text row M54). The other 4 points are NOT rows: 0.22 and 0.29 bar (overlapped up/down pairs, 15 and 14 px) and 1.51 and 1.92 bar (20 px blobs of overlapped markers; the 1.92 bar centre is 0.08 bar off the expected 2.0 bar grid point). Rejected by size in the tool: two merged blobs at pixel centres (771.3, 522.8) and (762.7, 539.9), and 8 text/line fragments of 4-6 px. Step-6 check against 3.4 wt % at 20 bar at x = 19.9515: difference 0.71%, passed.

Marker count reconciliation (extracted against counted):
- Figure 7A, extracted as rows: 18 circles, 17 triangles, 1 shared 20 bar glyph. Not separable, no row: (a) all markers below about 1.2 bar, about 10 circles and about 10 triangles at ca. 0.1 bar spacing (triangles 0.0, 0.1, 0.2 ... 0.8, 1.0 bar; white triangle fill drawn over the circles); (b) the triangle at 1.0 bar (touches the neighbouring markers); (c) the triangle and the hidden circle at 1.5 bar; (d) the two circles near 1.8 and 2.0 bar (merged blob); (e) the 20 bar desorption triangle, identical position to the 20 bar adsorption circle (one glyph, used for M19 only). Tried: opening 1-5 px and tolerance 40-220; no setting separated these.
- Figure 7B, extracted as rows: 17 up-triangles, 17 down-triangles, 1 shared 20 bar glyph. Not separable, no row: all markers below about 2.2 bar (overlapped up/down pairs at ca. 0.1-0.2 bar spacing, blobs of 2 or more markers); the 20 bar desorption marker (same glyph as the adsorption marker, used for M54 only).
- Resolution of the page image (about 150 dpi) is the limit: markers are 6-9 px wide.
