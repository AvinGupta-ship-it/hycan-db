# HYC-0067 extraction log (extractor A)

Rows written: 30 (rows.csv). One sample (Fe-GNF 9), one 77 K isotherm (I1) with 31 plotted markers (16 adsorption, 15 desorption); 30 of the 31 markers are rows (see "Not written" below).

## Extracted from

- Text p. 224 (PDF page 5), section "H2 adsorption and desorption": "Based on Fig. 4 a maximum H2 uptake of 0.643 wt-% is obtained" at 77 K and 20 bar. Same value in the Abstract ("The mass uptake is found to be 0.643 wt-%", 77 K, 20 bar) and in the Conclusions ("up to a pressure of 20 bar, the mass uptake is 0.643 wt-%"). One row (M16, text_direct), merged with the last adsorption marker of Fig. 4 (digitized 19.687 bar, 0.6435 wt%; printed 20 bar is within 2% of the marker; the paper says the value is taken from Fig. 4). No separate digitized row for that marker.
- Fig. 4 (p. 224), 77 K isotherm of Fe-GNF 9, adsorption series (blue diamonds): 15 rows (M1-M15) plus the merged M16.
- Fig. 4, desorption series (magenta squares): 14 rows (M17-M30).
- Table 3 (p. 223): BET area 556.65 m2 g-1 and d002 3.423 A of Fe-GNF 9 (characterization on every row; d002 stored as 0.3423 nm).
- Table 2 (p. 222), Fe-GNF 9 synthesis conditions (4 h, C2H4/H2 30:70 mL/min, 600 C), used in material_description.
- Experimental text p. 222: H2 degassing 250 C for 12 h; BET by N2 on Quantachrome Autosorb 1, degassed 4 h at 250 C; gravimetric H2 measurement; static; 77 K by liquid nitrogen immersion.
- Results text p. 223: XRD of Fe-GNF 9 shows graphite and Fe3C only (recorded as residual_metal_element = Fe, no amount).

## Values seen but not extracted

- Table 1 (p. 222), five H2 uptake values of other authors' carbon samples (0.59 wt-% volumetric 90 bar 298 K, ref. 6; 0.18 gravimetric 80 bar 298 K, ref. 7; 0.35 volumetric 10 MPa 303 K, ref. 8; 0.29 gravimetric 20 bar 300 K, ref. 9; 0.40 gravimetric/volumetric 140 bar 298 K, ref. 10). They are literature values for samples not measured or characterized in this paper (no sample label, surface area or conditions beyond the table), used only for comparison. I read the "values reported before" rule as covering the paper's own measurements that were published earlier, not a literature comparison table. If the reconciler reads it otherwise, these are the five values.
- Introduction p. 221: "GNF capable of adsorbing and retaining up to 30 L H2 per gram of carbon at room temperature" (ref. 4) and "H2 uptake of the GNF <1 wt-%": literature statements, no sample, temperature only "room temperature", no pressure. Not a measurement of this paper.
- Table 3 and Table 2: Fe-GNF 1 to 8 have BET areas (180.15, 256.80, 83.88, 259.05, 94.47, 135.30, 87.52, 211.40 m2 g-1), d002 (3.356, 3.394, 3.376, 3.422, 3.375, 3.382, 3.380, 3.399 A) and synthesis conditions, but no H2 uptake. No row, no sample_id.
- Yields (4.489 and 4.955 g gcat-1 h-1) and S/N ratios: not H2 uptake.
- Figs. 1, 2, 3: schematic, XRD patterns, TEM: no H2 values.
- Fig. 4 shows no value that the text does not give, apart from the plotted points digitized.
- No non-carbon sorbent was measured.

## Not written

- Desorption marker at the y axis (centroid px 163.5, 442.0): digitized as 0.000000 bar, 0.031178 wt% (archive HYC-0067_Fig4_desorption_low.json, first point). `validate_row_detail.py` reports `Pressure out of range` for pressure_bar = 0.0, and the pressure cannot be stated more exactly than "below about 0.03 bar" (1 px = 0.047 bar), so no row was written. The marker is counted in isotherm_point_count (31).

## Fig. 4 digitization

- Page image main-5.png (1241 x 1754 px). Axis tick pixel positions found by inspecting pixel rows and columns: x ticks 0, 5, 10, 15, 20 bar at px 163.5, 269.5, 375.5, 481, 586.5; y ticks 0 to 0.7 wt% at px 457.5, 407.5, 358, 308, 258.5, 208.5, 159.5, 109.5. Calibration on 0 and 20 bar and on 0 and 0.7 wt%; third-tick checks: 10 bar at px 375.5 predicts 10.024 bar (0.24%), 0.4 wt% at px 258.5 predicts 0.40029 wt% (0.07%).
- Markers: adsorption navy diamonds (#262a72), desorption magenta squares (#bd319d). `--mode markers`, `--open-px 2`, `--marker-min-px 4`. Counted on the enlarged plot: 16 diamonds, 15 squares; extracted: 16 diamonds (15 + 1) and 15 squares (13 + 2). Counts equal.
- Each series needs two archives because the legend (lower right, x 483-576 px, y 424-452 px) holds one diamond and one square and a single rectangle that includes the origin corner would also include the legend. Main ROI x 167-600 (diamonds) or 158-600 (squares), y 100-420; corner ROI for the origin diamond x 158-176, y 448-466 and for the two squares near the axis x 157-176, y 421-452. Files: HYC-0067_Fig4_adsorption_main.json (15 points, tolerance 100), HYC-0067_Fig4_adsorption_origin.json (1 point, tolerance 60), HYC-0067_Fig4_desorption_main.json (13 points, tolerance 70), HYC-0067_Fig4_desorption_low.json (2 points, tolerance 70).
- Check step: only one value is stated by the paper from this figure (0.643 wt% at 20 bar). `check` refuses x = 20 (the last marker is at 19.687 bar), so it was run at x = 19.6871 against 0.643: digitized 0.643501, difference 0.08%, passed (HYC-0067_Fig4_adsorption_main.json, status passed). The other three archives are `unchecked` because the paper states no value on them to check against; their markers were verified only by calibration ticks and by the marker count.
- Diamond at about 4.11 bar (M5): mostly hidden under a desorption square (3.95 bar). The tool found 4 visible pixels; the centroid of the visible part lies to the right of the true centre (probably by up to about 3 px, 0.15 bar). Confidence 2.
- Origin diamond (M1) overlaps both axis lines; digitized at 0.0236 bar, 0.00066 wt%. Confidence 3.
- Desorption markers stop at 16.0 bar although the text says desorption started at 20 bar; no marker or magenta line is visible between 16 and 20 bar.
- Lines between markers are not read; the curves have markers.

## Coding decisions

- sample_id HYC-0067-S1: numbered among samples that have rows; Fe-GNF 1-8 have no uptake.
- material_class carbon_nanofiber (not composite): Fe3C is residual growth catalyst of an as-prepared sample, recorded in residual_metal_element (amount not reported); no metal was added to the sorbent. Protocol text could be read as composite for "metal-compound particles".
- wt% convention coded unknown / none: the Table 1 footnote defines wt-% as (weight of adsorbate/weight of adsorbent) x 100% (W1) but attaches to the literature values; the paper does not state a convention for its own uptake.
- Basis: no basis named, no buoyancy correction stated for the gravimetric measurement: basis_stated false, uptake_type unspecified, basis_inferred unknown.
- measurement_method gravimetric_microbalance (paper: "gravimetric measurement"); the instrument is not named for H2 (the Quantachrome Autosorb 1 is the N2 BET instrument): instrument_identified false; no buoyancy correction: calibration_described false.
- measuring_lab_id: corresponding author Sufian (asterisk), first affiliation Universiti Teknologi PETRONAS. The Acknowledgements thank the University of Nottingham "for the collaboration studies as well as facilities" but do not say the H2 measurement was made there.
- area_same_sample yes: BET area in Table 3 is for the as-prepared Fe-GNF 9, the sample taken for H2 uptake. BET range and consistency criteria not stated.
- Pressure 20 bar: gauge or absolute not stated, stored as printed.
- Sample mass, H2 purity, free-volume calibration, degas end pressure, total/micropore volume, uncertainty: not stated in the paper.
- Fig. 4 y axis is labelled "Mass Uptake (wt %)"; digitized values are stored in uptake_wt_pct as wt% with no unit conversion.
