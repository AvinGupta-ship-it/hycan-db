# HYC-0077 extraction log (agent B, 2026-10-29)

Paper: Cai et al. 2014, Colloids Surf. A 444, 240-245. Input: 6 page images (main-1 to main-6), no supplementary file. 103 rows written.

## Sources extracted

- p. 4 (journal p. 243), Table 1: S_BET, V_Total, V_Micro, V_Meso, R_Micro and H2 uptake at 77 K, 20 bar and 1 bar (in parentheses, footnote f) for UCs-60, UCs-70, UCs-80, UCs-90, UCs-100, UCs-90-2, Cs-90. All 14 carbon uptake values are rows (10 of them are merged with a plotted point of Fig. 6, see below).
- p. 2 (journal p. 241), Sections 2.1-2.3: synthesis, HF/HCl treatment, N2 sorption (ASAP2020, BET p/p0 0.02-0.25, degassing 300 °C 10 h), H2 measurement (Hiden IGA-001 gravimetric, 77 K to 20 bar, buoyancy correction, degassing 10^-7 bar at 200 °C for 5 h), H2 purity "above 99.999%". These give the method and characterization fields on every row.
- p. 5 (journal p. 244), Fig. 6 main panel: H2 adsorption isotherms at 77 K, 0-20 bar, UCs-100 (open squares), UCs-90-2 (open down-triangles), UCs-90 (open circles), UCs-70 (open diamonds), Cs-90 (open up-triangles). Digitized. Archives: digitizations/HYC-0077_fig6main_<label>.json.
- p. 5, Fig. 6 inset: UCs-90-2 adsorption (filled down-triangles) and desorption (open down-triangles). Adsorption branch digitized. Archive: digitizations/HYC-0077_fig6inset_UCs-90-2_ads.json.
- p. 1 Abstract, p. 5 Section 3 text, p. 6 Conclusions: uptake values that repeat Table 1 (listed below). They are cited in source_location of the Table 1 rows and are not separate rows.

## Coding decisions

- Sample numbering follows first appearance in the paper, counting the graphical-abstract legend on p. 1 (Cs-90, UCs-90, UCs-90-2) and then Section 2.1 (UCs-60, UCs-70, UCs-80, UCs-100): S1 Cs-90, S2 UCs-90, S3 UCs-90-2, S4 UCs-60, S5 UCs-70, S6 UCs-80, S7 UCs-100. Labels are the Table 1 labels.
- Isotherms: I1 Cs-90 (Fig. 6 main), I2 UCs-90 (main), I3 UCs-90-2 (main), I4 UCs-90-2 (Fig. 6 inset), I5 UCs-60 (Table 1 only, 1 and 20 bar), I6 UCs-70 (main), I7 UCs-80 (Table 1 only), I8 UCs-100 (main).
- Inset vs main panel for UCs-90-2: the inset adsorption points are very close to the main-panel down-triangles, but the paper does not say they are the same run. Each plotted curve is one run, so the inset has its own isotherm_id (I4). replicates_reported is false everywhere: the paper gives no uncertainty or error bars and does not present the inset as a repeat measurement.
- Table 1 / Fig. 6 merges. 20 bar: the plotted 20-bar points of all five plotted samples are within 0.4 bar of 20 bar, so they are merged with the Table 1 value. 1 bar: merged for UCs-100 (digitized 0.9979 bar), UCs-70 (0.9979 bar) and UCs-90 (1.0093 bar). For UCs-90-2 and Cs-90, the 1-bar markers are inside the overlapping low-pressure cluster and could not be separated. Those Table 1 values are rows carrying the main-panel isotherm_id, because the paper says Table 1 lists the capacities of the Fig. 6 isotherms ("Detailed hydrogen storage capacities at pressure of 1 and 20 bar are listed in Table 1").
- UCs-90-2 at 20 bar: the inset adsorption 20-bar point (19.9918 bar) is as close in pressure as the main-panel point (19.9895 bar). The Table 1 value is merged with the main-panel point because the paper links Table 1 to the Fig. 6 isotherms of all carbons and cites the inset only for desorption. The inset 20-bar point is kept as its own digitized row (I4).
- Basis: the paper never names excess, absolute or total. basis_stated is false and uptake_type is unspecified. The method is gravimetric with "adsorption results were corrected for the buoyancy effect", so basis_inferred is excess and calibration_described is true. free_volume_calibration is empty because the correction is not described.
- instrument_identified is true: "Intelligent Gravimetric Analyzer (IGA-001, Hiden)".
- wt% convention: no paired units, so unknown/none.
- measuring_lab_id: the corresponding author is X. Zhao (*), affiliation a, which names no university, so the institute is used as printed.
- material_class: UCs-* are templated_carbon (USY zeolite hard template, removed by HF/HCl). Cs-90 is other (non-templated carbonized sucrose; no fitting class). synthesis_method: template_synthesis for UCs-*, carbonization for Cs-90.
- Pore volumes: V_Micro is by DR on N2, which gives pore_volume_method DR and probe N2. V_total is a single point at p/p0 = 0.996, and V_Meso = V_total - V_Micro. Both are recorded in notes.
- bet_consistency_criteria_stated is false: the paper justifies the 0.02-0.25 range by citing references, not by stating consistency criteria.
- area_same_sample is yes: N2 and H2 were measured on the same synthesized samples.

## Figure digitization: calibration

- Fig. 6 main panel (page pixels, from the intensity-weighted centroids of the tick marks): x 0 bar = 710.55 px, 20 bar = 1150.48 px; check tick 10 bar = 930.47 px, predicted 9.998 bar. y 0.0 wt% = 467.70 px, 3.6 wt% = 142.73 px; check tick 1.8 wt% = 305.50 px, predicted 1.797 wt% (0.18%).
- The per-series images are the page crop x 690-1165, y 125-485, upscaled 4 times (u = 4(page px - origin) + 1.5). The same ticks become x 83.7 / 1843.42 / check 963.38 and y 1372.3 / 72.42 / check 723.5.
- Fig. 6 inset (page pixels): x 0 bar = 922.42 px, 20 bar = 1149.28 px; check 10 bar = 1035.85 px, predicted 10.000 bar. y 0.0 wt% = 443.79 px, 3.6 wt% = 277.0 px; check 1.8 wt% = 360.52 px, predicted 1.797 wt%.
- digitize_figure.py check against Table 1 passed (5% tolerance) for every archive: UCs-100 at 1 bar (1.15) and at its 20-bar point (3.23); UCs-90 at 20 bar (3.37) and 1 bar (1.30); UCs-70 at 20 bar (3.52) and 1 bar (1.43); UCs-90-2 main and inset at their 20-bar points (3.65); Cs-90 at its 20-bar point (2.85). Where the last point lies a few hundredths of a bar below 20, the check was run at that point's digitized pressure.

## Figure digitization: isolation method (Fig. 6 main panel)

- Fig. 6 is black-and-white. Five series of open symbols overlap heavily below about 1 bar and in pairs at higher pressure (down-triangles on diamonds, up-triangles on squares). Colour isolation alone cannot separate the series.
- Marker centres were found on the page image by shape-template matching (scripts in work/scripts: tm.py, refine.py, cfit.py, joint.py, final_main.py). The templates were square 7 px, circle 8 px, triangles 9 px and diamond 9.5 px, rendered at quarter-pixel offsets.
  - Unoverlapped markers: normalized cross-correlation fit within +-2 px.
  - Overlapped markers: joint fit (squared residual) with the neighbouring fitted markers held fixed. A marker was accepted only if its gain was at least 3, its gain per unit template ink was at least 0.15, and a visual check of the overlay showed a distinctive edge of that shape. Accepted this way (extraction_confidence 2): UCs-90-2 at 16, 14, 12, 6, 5, 4, 2 and 0.6 bar; Cs-90 at 8 and 0.2 bar; UCs-90 at 1.0 and 0.2 bar; UCs-100 at 0.8, 0.6 and 0.4 bar. Other markers: confidence 3.
- Each series' fitted centres were drawn as 8 x 8 px red blocks into a per-series image (work/prep/fig6main4x_<label>.png). That image was run through digitize_figure.py extract --mode markers --open-px 0. The tool's centroids equal the fitted centres to 0 px, and the number of extracted markers equals the number of fitted markers in every series (UCs-100 20, UCs-90 12, UCs-70 19, UCs-90-2 13, Cs-90 11).
- Fig. 6 inset: the filled adsorption markers were digitized directly from page pixels (work/prep/inset_ads.png: inset interior only, legend x 1085-1150 / y 308-345 whited out, left frame column x 920 excluded). Settings: --color #000000 --tolerance 80 --open-px 2. The 0.8-bar and 1.0-bar markers touch apex-to-base, so 2 pixels at (932, 384) and (933, 384) were whited out to separate them. This moves the 1.0-bar centroid by about 0.3 px. 23 markers were extracted, equal to the 23 adsorption markers counted.

## Plotted markers seen but not extracted

- Fig. 6 main, UCs-90-2 (down-triangles): 10 bar (top edge visible just above the UCs-70 diamond; joint-fit gain below 0); 8 bar (coincides with the UCs-70 diamond); 1 bar and all points below 0.6 bar (inside the low-pressure cluster). Not separable.
- Fig. 6 main, Cs-90 (up-triangles): 7 bar (base visible below the UCs-100 square; gain 2.0), 6 bar (apex visible above the square; gain below 0), 5 bar (apex above the square; gain 1.2). Not separable. At 2 bar, the Cs-90 line runs into the UCs-90 circle, so a marker is probably hidden there; it is not visible. The 1 bar point and the points between 0.2 and 3 bar are inside the cluster.
- Fig. 6 main, UCs-90 (circles): markers between 0.2 and 1 bar (about 0.4-0.8 bar) are not separable. A circle near 0.1 bar (y about 415 px) and a partial circle near 0.01 bar (y about 448 px) have arcs visible but were not separable with confidence. The lowest circle (0.094 wt%) digitized at -0.002 bar, outside the axis range (pressure cannot be negative), so it was not extracted.
- Fig. 6 main, UCs-70 (diamonds): the lowest diamond (0.279 wt%) digitized at -0.002 bar, outside the axis range, so it was not extracted.
- Fig. 6 main, UCs-100 (squares): markers below 0.4 bar are in the vertical stack at x about 707-716 px (square edges visible at y about 427-437 px). Not separable.
- Fig. 6 inset, adsorption: the lowest marker (-0.005 bar, 0.0622 wt%) is outside the axis range, so it was not extracted. The 0.0543-bar blob (28 px) may contain two overlapping markers. The 20-bar point (3.6607 wt%) lies slightly above the 3.6 tick (linear extrapolation flagged by the tool) and is kept.
- Fig. 6 inset, desorption (open symbols): the markers lie almost entirely behind the adsorption markers. Grey partial outlines are visible above most adsorption markers (for example at 2, 4, 6, 8, 10, 14 and 18 bar), but no desorption marker could be separated or counted. None were digitized.
- isotherm_point_count is the markers counted on the plot plus the hidden markers identified above. I1 15 (11 digitized + 7, 6, 5 bar + the Table 1 1-bar point), I2 15 (12 + three circles near 0.1, 0.01 and 0 bar), I3 15 (13 + 10 bar + the Table 1 1-bar point), I4 23 (adsorption branch only; desorption markers could not be counted), I6 20 (19 + the diamond at 0 bar), I8 21 (20 + one square in the low stack). These are lower bounds where markers are hidden in the cluster.

## Values seen but not extracted (other reasons)

- Abstract (p. 1): "a hydrogen storage capacity of up to 3.65 wt% at 77 K and 20 bar" for the carbon of 1200 m2/g. This is UCs-90-2, Table 1, the same measurement as row M38.
- Conclusions (p. 6): UCs-90-2 "up to 3.6 wt% at 77 K and 20 bar". Rounded restatement of M38.
- Section 3 (p. 5): "Cs-90, UCs-90, and UCs-90-2 exhibit a hydrogen uptake of 1.39, 1.30, and 1.34 wt% at 1 bar" and UCs-100 "1.15 wt% at 1 bar". Same as the Table 1 rows M2, M14, M26 and M87.
- Section 3 (p. 5): "the adsorption uptakes of hydrogen at 1 bar vary between 1.1 and 1.4 I_D/I_G [sic] wt%". A range across samples, not a measurement.
- Graphical abstract (p. 1), inset "Hydrogen adsorption at 77 K", 0-20 bar: a thumbnail re-plot (about 165 x 110 px) of the 77 K isotherms of three samples. The panel has no legend; by colour match with the XRD legend the curves are blue = UCs-90-2, black = UCs-90, red = Cs-90. It was treated as a reproduction of the Fig. 6 isotherms in the graphical abstract, not as separate runs, and was not digitized. The reconciler may wish to review this choice.
- USY zeolite (Table 1; zeolite template, not a carbon sorbent): S_BET 701.5 m2/g, V_Total 0.405, V_Micro 0.304, V_Meso 0.101 cm3/g, R_Micro 0.75; no H2 uptake ("-").
- Section 3 text (p. 4): "BET specific surface areas and total pore volumes of the carbons derived in the presence of USY zeolites are of respectively up to 1038 m2/g and 0.88 cm3 g-1 ... the one in the absence of zeolite (700 m2/g and 0.417 cm3 g-1)". This is inconsistent with Table 1 (maximum 1218.6 m2/g and 1.068 cm3/g; Cs-90 723.2 m2/g); the Table 1 values are used. "603 m2/g [26]" is a value from another paper.
- Fig. 1 (XRD, p. 3): broad peaks at 2θ about 24° and 44° (plus 14.13°, 14.27°, 18.03°, 21.78°). No d-spacing is printed, so interlayer_spacing_nm is empty.
- Fig. 2 (N2 isotherms, p. 3) and Fig. 3 (NLDFT pore size distributions, p. 3): not H2. The text gives PSD maxima "at around 1.4 nm" for zeolite-derived carbons and the ranges <1, 1-2, 2-10, >10 nm. This is not an average pore diameter, so average_pore_diameter_nm is empty.
- Fig. 4 (SEM, p. 4): no values.
- Fig. 5 (Raman, p. 5): I_D/I_G UCs-60 0.815, UCs-70 0.808, UCs-80 0.958, UCs-90 1.003, UCs-100 1.034, UCs-90-2 1.007, Cs-90 1.003. No schema field.
