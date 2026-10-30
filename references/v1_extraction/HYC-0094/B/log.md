# HYC-0094 extraction log (agent B)

Input: main-1.png to main-6.png only (no supplementary pages). 116 rows written.

## Sources extracted from

- main-4, Table 1: H2 uptake at -196 °C and 20 bar, at 1 bar (parentheses) and Langmuir-estimated maximum (footnote h) for 8 samples (24 values), plus S_BET, S_micro, V_p, V_micro, PSD maxima, N wt%, helium and packing densities carried on every row of each sample.
- main-4, Fig. 3a (H2 isotherms at -196 °C, 0-20 bar, CP-4-800/700/650/600): digitized markers (4 archives in `digitizations/`). The 20-bar marker of each series is merged with its Table 1 value; the CP-4-600 marker at 0.990 bar is merged with its Table 1 1-bar value (1.97 wt%).
- main-4 text lines 30-33 ("up to 2.63 and 7.03 wt%") and main-1 abstract (7.03 wt% at -196 °C and 20 bar): same values as Table 1 (CP-2-700 at 1 bar, CP-4-800 at 20 bar); cited in source_location, no extra rows.
- main-4 text lines 36-39 ("values of 7.3 - 8.7 wt%") and main-5 Conclusions ("estimated maximum uptake of 8.7 wt%"): same as Table 1 Max. H2 uptake; no extra rows.
- main-2 Experimental (Carbon synthesis, Characterization, H2 measurement: Hiden IGA-003, 99.9999% H2, -196 °C liquid-nitrogen bath, 0-20 bar, buoyancy correction; He density by AccuPyc; packing density at 7 MPa) and main-4 lines 18-22 (buoyancy densities 0.04 and 1.72-2.31 g cm-3): method and characterization fields.

## Coding decisions

- Sample numbering follows first appearance: CP-4-600 and CP-4-800 (main-2 text, lines 76-77), then the Fig. 2a legend on main-3 (CP-4-850, CP-4-700, CP-4-650), then main-3 text (CP-2-650, CP-2-700, CP-2-800). Rows are ordered by Table 1.
- Basis: Fig. 3a isotherms are called "total" without definition -> basis_stated false, uptake_type total for rows of those isotherms; gravimetric with stated buoyancy correction -> basis_inferred excess. Rows not tied to a Fig. 3a isotherm get uptake_type unspecified.
- Langmuir maxima: value_kind fitted_extrapolated, no pressure (pressure_unstated true), no isotherm_id (a model parameter, not a point of a run).
- Table 1-bar values of CP-4-650, CP-4-700 and CP-4-800: their Fig. 3a marker near 1 bar is inside the unresolved low-pressure cluster, so the same-measurement test could not be applied; the paper does not say the value comes from the curve, so these rows have no isotherm_id.
- CP-4-850 and CP-2-650/700/800 have only Table 1 values (1 and 20 bar), so each pair is one isotherm with isotherm_point_count 2.
- material_class doped_carbon: N built into the carbon (N-pyrrolic/N-pyridone groups, 0.32-4.05 wt% N). synthesis_method chemical_activation (one-step KOH activation of polypyrrole). The N-content method is not stated in the main text.
- average_pore_diameter_nm holds the first NLDFT PSD maximum. Both maxima are in notes.
- Isotherms are described as "completely reversible". Only one marker set per curve is plotted, so all markers are coded adsorption.

## Figure 3a digitization method

- Calibration ticks were found on the main-4 page image by pixel-row and pixel-column inspection. x: 0 at px 731 and 20 at px 1024 (axis and frame lines at the labelled ends), checked at 10 = px 878 (0.34% error). y: 0 at px 841 and 6 at px 638, checked at 4 = px 705 (0.49% error).
- The figure is monochrome. All four series are black and differ only by marker shape (triangle, square, star, circle), so `digitize_figure.py colors` finds no colours and colour isolation cannot separate the series.
- Each marker centre was therefore located on the page image with my own code in the work directory: normalized cross-correlation with templates cut from isolated markers of the same figure, with sub-pixel peaks. For CP-4-600 circles at or below 2 bar, the centroid of each circle's enclosed white interior was used instead. Each centre was rendered as a small filled block on a blank image with the page's pixel grid, one image per series. `digitize_figure.py extract --mode markers` was run on each rendering with the page calibration. The archives' source_image is therefore the rendering in the work directory.
- The tool's centroids reproduce the located centres to within 0.25 px.
- The step-6 checks passed against Table 1: 20 bar for all four series, within 0.2-0.73%; 1 bar for CP-4-600, 0.57%.
- Points above 6 wt% lie above the highest labelled y tick. The tool flags them as extrapolations; they are inside the axis frame on a linear axis.
- Marker counts digitized, which equal the tool output: CP-4-800 22 (2-20 bar), CP-4-700 24 (one at about 0.03 bar, then 1.57-20 bar), CP-4-650 21 (3-20 bar), CP-4-600 30 (0.03-20 bar).
- Markers that could not be separated (low-pressure cluster near the origin, about 0-3 bar):
  - CP-4-800: triangles below 2 bar.
  - CP-4-700: squares between about 0.03 and 1.5 bar. One square near 1.2 bar is partly visible but was not separable.
  - CP-4-650: stars below 3 bar, including the star at 2 bar hidden behind the 2-bar square.
  - CP-4-600: a possible further marker in the stacked block at the origin (about 0.03 bar, 0.37 wt%).
  - The CP-4-600 schedule (about 0.03, 0.07, 0.24, 0.48, 0.68, 0.99, 1.19, 1.47, 2, 3, ...) suggests each series has about 30 points. The isotherm_point_count values for CP-4-650/700/800 (21/24/22) count only identified markers and are lower bounds.

## Values seen but not extracted

- Volumetric capacities with no sample named, so they cannot be attributed to one sample without my own calculation:
  - "volumetric density of up to 37 g H2 L-1 at 20 bar" (main-1 abstract; main-5 Conclusions);
  - "volumetric capacities typically in the range 20 - 37 g H2 L-1 at 20 bar, and 25 - 43 g H2 L-1 at the estimated maximum capacity" (main-5 lines 57-59);
  - "estimated volumetric uptake of 43 g H2 L-1 ... from Langmuir plots" (main-5 Conclusions).
- Projected volumetric densities, which are hypothetical values for a packing density of at least 0.6 g cm-3, not measurements: "42 g H2 L-1 at 20 bar" and "50 g H2 L-1 at the estimated maximum" (main-5 lines 63-67).
- main-4 Fig. 3b (H2 uptake at -196 °C and 20 bar against surface area) is not an isotherm and was not digitized.
  - Its "this work" points duplicate the Table 1 20-bar values.
  - Its literature points (activated carbons, ref. 4; MOFs, ref. 23) are not this paper's samples.
- Literature values quoted for comparison, not measured in this paper:
  - 6.9 wt% for zeolite-templated carbon at -196 °C and 20 bar (ref. 7a), with estimated maximum 8.33 wt%;
  - about 4.4 wt% for CDCs (refs. 5, 8);
  - 3.0-5.6 wt% for one-step KOH carbons (ref. 4);
  - 7.08 wt% for a doubly activated carbon (ref. 13);
  - 6.84 wt% (estimated maximum 8.24 wt%) for an N-doped carbon (ref. 20);
  - up to 3.0 wt% at 1 bar for templated carbons;
  - uptake increases of 96% and 63% (refs. 11a and 11b,c).
- Chahine rule (10 µmol H2 per m2): a reference relation, not a measurement.
- Polypyrrole and polypyrrole carbonized at 800 °C (N 13.5 -> 11.7 wt%, carbon yield about 60 wt%) have characterization but no H2 uptake, so no row.
- main-3 Fig. 2a (N2 sorption isotherms) and Fig. 2b (NLDFT PSD) are not H2 data.
- Supplementary Figures S1-S5 and Table S1 are cited (S2: N2 sorption of CP-2 samples; S5: H2 uptake against micropore volume) but are not in the input.
