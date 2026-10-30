# HYC-0094 extraction log (agent A)

Paper: Sevilla, Mokaya, Fuertes 2011, Energy Environ. Sci., doi 10.1039/c1ee01608c. Input: main article only (6 pages). The supplementary information (Figures S1-S5, Table S1) is not in the input.
Rows written: 96 (rows.csv). `validate_row_detail.py --errors-only`: no errors.

## Extracted from

- Table 1, main.pdf p.4, column "H2 uptake [wt %]" (20 bar) for 8 samples: 8 rows. For CP-4-600, CP-4-650, CP-4-700 and CP-4-800 each row is the same measurement as the plotted 20 bar end point of Figure 3a (printed 20 bar, digitized 19.92-19.94 bar); `isotherm_id` I1-I4, digitized point in `notes`, no separate digitized row.
- Table 1, same column, value in parentheses (1 bar), 8 rows. CP-4-850, CP-2-650, CP-2-700 and CP-2-800 have no plotted curve: their 1 bar and 20 bar values are one 2-point isotherm (I5-I8, point count 2). For CP-4-600/650/700/800 the markers near 1 bar overlap each other and the other series and could not be separated, so no digitized point within 0.02 bar of 1 bar exists and the paper does not say the value is read from the curve: these four rows have no `isotherm_id`.
- Table 1, column "Max. H2 uptake [wt %]", 8 rows ("derived from Langmuir simulation plots"): `value_kind` = fitted_extrapolated, no pressure (`pressure_unstated` = true), no `isotherm_id` (model capacity, not a measured point of the run).
- Figure 3a (main.pdf p.4, page image main-4.png), 77 K (printed -196 C, stored 77.15 K) gravimetric isotherms of CP-4-600 (circles), CP-4-650 (stars), CP-4-700 (squares), CP-4-800 (triangles): 72 digitized rows (21 + 18 + 16 + 17) plus the 4 end points merged into the 20 bar table rows. Archives: `digitizations/HYC-0094_Fig3a_CP-4-600.json` (22 points), `_CP-4-650.json` (19), `_CP-4-700.json` (17), `_CP-4-800.json` (18).
- Text passages (p.4-5, abstract, conclusions) that repeat Table 1 values ("up to 2.63 and 7.03 wt%", "7.3 - 8.7 wt%", "estimated maximum uptake of 8.7 wt%"): same measurements as Table 1 rows, no separate rows.
- Characterization on every row: Table 1 SBET (N2 BET, P/P0 0.04-0.2), Smicro (t-plot), Vp (N2, P/P0 0.99), Vmicro (t-plot), N content, helium density (stored as skeletal density), packing density (7 MPa); text p.2 for instrument, H2 purity, buoyancy correction.

## Figure 3a digitization method

- Calibration (page image main-4.png, 1241 x 1755 px, tick pixels found by inspecting pixel rows/columns): x 0 bar = px 731, 20 bar = px 1024, check tick 10 bar = px 878 (tool residual 0.34%); y 0 = px 841, 6 = px 638 (highest labelled tick), check tick 4 = px 705 (residual 0.49%). Unlabelled minor tick at 7 = px 604, predicted 604.2 from the calibration, so the scale holds above 6; the tool flags points above y = 6 as extrapolated (triangles from 12 bar, squares from 15 bar, stars from 18.5 bar). They are kept and noted in `notes`.
- All four series are black with hollow markers, so colour cannot separate them, and on the raw page image the tool finds almost no markers (the 3-px opening removes the 1-px outlines). Derived images (work directory, `final_tri.png`, `final_sq.png`, `final_star.png`, `final_circ.png`, built by `work/scripts/fill5.py` and `work/scripts/final_masks.py`): (1) pixels darker than 200 in the plot area, legend and panel label "a" removed; (2) enclosed white holes of 70 px or less filled, so hollow markers become solid; (3) binary erosion with a 4-connected element (2 iterations for triangles, squares, stars; 3 for circles) so thin lines vanish and necks between touching markers break, which leaves marker cores with the same centroid; (4) one series kept per image, inside a band around a guide curve found by template matching of the legend markers (guide used only for masks, never for values); (5) 1-px vertical gaps at x = 852, 859, 999, 1006, 1013, 1020 (midpoints between neighbouring markers of one series, 0.5 bar apart); (6) columns 853-858 blanked for squares and triangles (8.5 bar markers, see below).
- Tool call: `digitize_figure.py extract --mode markers --color #000000 --tolerance 40 --open-px 1 --marker-min-px 3 --marker-max-px 400 --roi 735 590 1030 838`, one run per series. Archive `source_image` therefore points to the derived image, not the page image.
- Cross-check: marker centres from legend-template matching on the page image agree with the tool's centres to about 0.5 px (0.015 wt%, 0.03 bar). The same pipeline applied to the legend markers puts the centroid 0.0 to 0.8 px from the legend line row (circles 0.8 px above, squares 0), i.e. at most 0.024 wt%; no correction applied.
- Step 6 check (`digitize_figure.py check --at 19.9`, x = 20 lies outside the digitized range because the end markers are at 19.92-19.94 bar): CP-4-800 7.042 vs 7.03 (+0.18%), CP-4-700 6.720 vs 6.71 (+0.15%), CP-4-650 6.165 vs 6.15 (+0.25%), CP-4-600 4.266 vs 4.24 (+0.61%); all passed, status `passed` in the archives. The 1 bar table values cannot be checked (no digitized marker below 2 bar).
- Marker count (`isotherm_point_count` = 29 for I1-I4): 22 markers at 2 bar and above (2, 3, 4, 5, 6, 7, 8, 8.5, 9, 10-18, 18.5, 19, 19.5, 20 bar, same pressure grid in all four series, ring count of CP-4-600 confirmed by a Hough circle search on the page image) plus 7 below 2 bar counted on CP-4-600 (about 0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5 bar). Below 2 bar the other three series are overlapped, so their count of 7 is inferred from the shared grid.
- Curves show one branch only. The paper says the isotherms are "completely reversible"; branch coded adsorption.

## Markers seen but not extracted (could not be separated)

- CP-4-600: the 7 markers below 2 bar (overlap each other and the other series).
- CP-4-650: markers at 2, 3, 4 bar and the 7 below 2 bar (overlapped by neighbouring series).
- CP-4-700: markers at 2, 3, 4, 5 bar, the 7 below 2 bar, and the 8.5 bar marker (overlapped by the triangle above; the blob was contaminated, 40 px against 14-27 px for single markers).
- CP-4-800: markers at 2, 3, 4 bar, the 7 below 2 bar, and the 8.5 bar marker (triangle base overlapped by the square, blob 36 px against 7-13 px).
- Archive points not used: none (both contaminated blobs were masked and the series rerun).
- The extra marker at the very bottom left of the plot (squares and stars near the axis, below about 0.2 bar) is inside the overlapped group and is not extracted.

## Values seen, not extracted

- Figure 3b (uptake against surface area, not an isotherm): not digitized. The "this work" points (filled circles) are the Table 1 20 bar values against SBET and give nothing new; open circles (activated carbons, ref. 4) and triangles (MOFs, ref. 23) are other work and MOFs.
- Figure 2 (N2 isotherms, PSD) and Figure 1 (SEM, TEM): no H2 uptake.
- Volumetric densities: "up to 37 g H2 L-1 at 20 bar", "20 - 37 g H2 L-1 at 20 bar", "25 - 43 g H2 L-1 at the estimated maximum", "43 g H2 L-1 computed from Langmuir plots". They are ranges across samples that the authors computed from Table 1 packing density and uptake; no sample is named, so no row. "42 g H2 L-1 at 20 bar and 50 g H2 L-1" at 0.6 g cm-3 packing is a projection, not a measurement.
- Literature values quoted in the introduction and discussion (other papers, not extracted): 3.0-5.6 wt% for one-step KOH carbons (ref. 4), 6.9 wt% (estimated max 8.33) zeolite-templated carbon (ref. 7a), about 4.4 wt% carbide-derived carbons (refs. 5, 8), 7.08 wt% doubly activated carbon (ref. 13), 6.84 wt% (estimated max 8.24) KOH-activated mesoporous N-doped carbon (ref. 20), up to 3.0 wt% at 1 bar for templated carbons, 96% and 63% improvements (refs. 11a, 11b,c).
- Polypyrrole precursor and polypyrrole carbonized at 800 C (no KOH): characterization only (carbon yield about 60 wt%, N content 13.5 and 11.7 wt%, from the text and SI Table S1), no H2 uptake, no row.
- SI Figure S5 (H2 uptake against micropore volume, per the text and ESI list) and SI Table S1 (elemental composition, O and H content): not available.

## Coding decisions

- Sample numbering follows Table 1 order (CP-4-600 S1, CP-4-650 S2, CP-4-700 S3, CP-4-800 S4, CP-4-850 S5, CP-2-650 S6, CP-2-700 S7, CP-2-800 S8); first appearance in the text runs CP-4-600, CP-4-800, then the others. Labels are as printed.
- `material_class` = doped_carbon, `dopant_element` = N: N-pyrrolic and N-pyridone groups (FT-IR, XPS) are built into the KOH-activated carbon from the polypyrrole precursor; N wt% from Table 1 stored in `dopant_concentration_wt_pct`, method not stated in the main text. `synthesis_method` = chemical_activation (KOH activation is the route that made the carbon); HCl washing in `purification_method`.
- `average_pore_diameter_nm`: Table 1 gives two NLDFT PSD maxima for seven samples (micropore and small mesopore, e.g. 1.3/2.2), so it is left empty and both maxima are in `notes`; CP-2-650 has one maximum (1.3 nm, `pore_diameter_method` DFT).
- Basis: the paper calls the isotherms "total hydrogen uptake" without a definition: `uptake_type` total, `basis_stated` false, `basis_inferred` excess (gravimetric with a stated buoyancy correction, adsorbed H2 density 0.04 g cm-3).
- wt% convention unknown (no paired unit, no definition), source none.
- Instrument: Hiden IGA-003 (`instrument_identified` true), buoyancy correction stated (`calibration_described` true), H2 99.9999% with molecular sieve filter; no degassing conditions, no sample mass, no uncertainty or replicate in the main text.
- `measuring_lab_id`: Mokaya group, University of Nottingham (first corresponding author marked *; his only affiliation); the paper does not name where the H2 isotherms were measured.
- `area_same_sample` = yes (N2 BET on the same CP-x-y carbons); `bet_range_stated` true (0.04 to 0.2), consistency criteria not stated.
- Temperature printed as -196 C (also "liquid nitrogen bath"): stored 77.15 K, not inferred.
