# HYC-0009 extraction log (extractor B)

Ioannatos and Verykios 2010, Int. J. Hydrogen Energy 35, 622-628. Pages main-1 to main-7 (journal pp. 622-628); no supplementary file.
143 rows: 14 Table 2/3 uptake rows, 12 Table 2/3 Vm rows, 7 Fig. 3A rows, 104 Fig. 3B rows, 6 Table 4 TPD rows.

## Sources extracted

- Table 1 (main-3.png, p. 624): characterization only. Rows carry the BET area of the state used for H2: the "Sp. surface area after HNO3 treatment" for the six CNT samples (268, 275, 298, 355, 703, 877 m2/g) and 254 m2/g for Vulcan XC-72 (no HNO3 treatment, after-HNO3 cell "-"). Carbon source, growth temperature, purity, diameter, length, layers and ID/IG go in material_description.
- Section 2.1 to 2.4 (main-2.png, main-3.png): methods. Sorptomatic 1900 (Fisons) volumetric apparatus, 200 mg, 250 C vacuum and H2 pretreatment, 77 K and 298 K, 0-1000 Torr; BET on a Micromeritics Gemini III 2375 with N2 at liquid-nitrogen temperature; HNO3 purification; TPD procedure (100 mg, Fisons SXP Elite 300H MS).
- Fig. 3A (main-4.png, p. 625, 298 K): 7 isotherms (I1-I7) with markers. Only the highest-pressure point of each was used (7 rows). All markers were digitized for counting and archiving.
- Fig. 3B (main-4.png, p. 625, 77 K): 7 isotherms (I8-I14), 105 markers. 104 are rows; the last Vulcan XC72 point (749.69 Torr) is the same measurement as the Table 3 Vulcan value and is recorded on that row.
- Table 2 (main-5.png, p. 626, 298 K) and Table 3 (main-5.png, p. 626, 77 K): one row per sample and temperature with H2 wt.% and Vs (14 rows), plus one row per Vm value (12 rows).
- Table 4 (main-6.png, p. 627): H2 wt% desorbed in TPD for the six CNT samples (6 rows, measurement_mode TPD). Tm and Ed are in notes.

## Coding decisions

- The tables print no pressure for the wt% column. The text gives Vs as "the maximum volume adsorbed, Vs, at 760 Torr" and the cm3/m2 column as "cm3 of H2 adsorbed at 760 Torr per m2". All Table 2/3 values were therefore given 760 Torr (1.0132472 bar).
- Matching table values to plotted points used the 2% rule (15.2 Torr at 760 Torr). The last plotted points of the CNT isotherms lie at 704-744 Torr, so none qualifies, and those table rows have no isotherm_id. The borderline cases are MWCNTs-97% at 298 K (743.47 Torr, 16.5 Torr from 760) and Vulcan XC72 at 298 K (744.09 Torr, 15.9 Torr from 760). Vulcan XC72 at 77 K (749.69 Torr) qualifies and was merged.
- Vs nevertheless agrees with the last plotted point of every CNT isotherm to within 0.04-0.61% (3A: -0.18, +0.32, +0.14, -0.10, +0.19, +0.04%; 3B: -0.20, -0.12, -0.61, -0.22, +0.13, -0.19%, in sample order). Vs is therefore value_kind measured: it is called the maximum and lies within 3% of a digitized point. Reconciler: the table rows and the last digitized points are very probably the same measurements.
- Unit-consistency failure: the printed H2 wt.% does not match the printed Vs under either convention. W1 from Vs is 2.0-2.6 times smaller (for example SWCNTs-85% at 77 K: 3.27 wt% printed against 1.2505 wt% from 139.036 cm3/g). These rows are coded wt_pct_convention unknown / none. The validator's 12 "mL(STP)/g and wt% inconsistent" warnings are these rows. The volumes are printed as cm3/g ("cm3/gr" on the axes) with no STP stated, and are stored as cm3(STP)/g.
- Vm is the BET monolayer volume of the H2 isotherm, a model parameter. It is coded value_kind fitted_extrapolated, pressure_unstated true and no isotherm_id.
- Basis: no basis is named or defined. The text's "total hydrogen uptake" and "total adsorbed volume" are read as "overall", so uptake_type is unspecified. A volumetric instrument gives basis_inferred excess; TPD gives unknown.
- Vulcan XC-72 is a carbon black, so it is a carbon sorbent (class other, commercial; supplier not printed) and is extracted although measured "for comparison".
- The CNTs keep residual Fe2O3/Al2O3 catalyst (residual_metal_element "Fe, Al", amount not stated), and their class stays MWCNT/SWCNT. thinMWCNTs (6-10 layers) are coded MWCNT.
- measuring_lab_id is Verykios (corresponding author, marked *), University of Patras.
- Degassing: the stored 250 C / 0.5 h is the evacuation at 250 C for 30 min. Before it came heating under dynamic vacuum to 250 C (no duration) and 1 h under 760 Torr H2 at 250 C. TPD rows store 500 C / 0.25 h under He flow.
- TPD rows: adsorption temperature 298 K (25 C in section 2.4) and reference_temperature_k 723.15 (450 C ramp end). The pressure is not stated (H2 flow at 40 cc/min).

## Values seen but not extracted

- Table 1 as-prepared (before HNO3) areas: MWCNTs 208, 232 and 243; thinMWCNTs 309; SWCNTs 726 and 813 m2/g. They belong to the as-prepared treatment state, which has no H2 uptake, so they are not rows. They are quoted in notes.
- Table 2/3 H/C columns (14 values): derived from wt% (H2 molecules per C atom). There is no field.
- Table 2/3 cm3/m2 columns (14 values): Vs (or V at 760 Torr) divided by the BET area. This is a derived normalisation, not a film areal uptake, so it is not stored. The values are quoted in notes.
- Table 4 Tm (K) and Ed (kJ/mol): not uptake. They are quoted in notes.
- Text p. 626, "0.34% (Table 2)" for SWCNTs-85% at 298 K: Table 2 prints 0.36. The table value is stored and the discrepancy noted on that row. "3.27% (Table 3)" repeats the table.
- Text p. 626, "adsorption capacity of 1.75 wt.%" for a hydrogen monolayer on SWCNTs-85% (877 m2/g): a Zuttel-model estimate, not a measurement.
- Text p. 626, area ranges ("about 200 ... to about 800 m2/g", "between 268 and 877 m2/g"): summaries of Table 1.
- Introduction (pp. 622-623), other authors' values, not this paper's measurements: Darkrim and Levesque 11 wt% at 10 MPa and 77 K (simulation); Dillon et al. 5-10 wt% and 19.6 kJ/mol; Ye et al. up to 8 wt% at 80 K and 40-80 bar; Liu et al. 2-4 wt% at 12 MPa; Zhu et al. up to 5 wt% at 100 atm; Wu et al. up to 0.25 wt%. Also the DOE target of 6.5 wt%.
- Fig. 4 (main-6.png, p. 627): MWCNTs-95.7% uptake (wt% H2) under H2 flow at 298 K against exposure time, 4 markers at 15, 30, 60 and 120 min plus the origin. This is a kinetics figure, not an isotherm, so it was not digitized. Its values are not given in the tables or text; the text says only that at least 60 min is needed to reach equilibrium.
- Fig. 5 (main-6.png, p. 627): TPD spectra (ppm H2 against T), not an isotherm. The integrated amounts and Tm are in Table 4.
- Figs. 1 and 2 (SEM and Raman spectra) contain no uptake values.
- No non-carbon sorbent is measured.

## Digitization (Figs. 3A and 3B)

- Calibration on page pixels (tick centres found from pixel rows and columns):
  - Fig. 3A: x 0 Torr = 716.0, 800 = 1109.5, check 400 = 913.0 (error 0.13%); y 0 = 593.5, 40 = 149.5, check 20 = 371.5 (error 0%).
  - Fig. 3B: x 0 = 716.0, 800 = 1113.5, check 400 = 915.0 (error 0.13%); y 0 = 1116.5, 400 = 679.5, check 200 = 898.0 (error 0%).
  - The 0-Torr ticks lie under the origin marker; their visible tails below the axis are centred on x = 716.
- Separating series: all seven series are black, so they cannot be told apart by colour, and were separated by symbol shape. Symbol templates came from the legend (up triangle, diamond) and from isolated data markers (square, circle, down triangle, asterisk, plus).
  - Marker seeds came from connected components, band template matching and thin-stroke detection. For the two lowest-pressure pile-ups in Fig. 3B, where up to six markers overlap, seeds were placed by inspecting enlarged pixel maps; their positions were then computed, not read.
  - All markers of a panel were then fitted jointly by coordinate descent on pixel agreement with the binarized page (grey < 110, axis lines excluded). The residual maps show only edge pixels and connecting lines left unexplained. Work files: work/fit3A.json, work/fit3B_v2.json, work/resid3A.png, work/resid3B_v2.png.
- Feeding the tool: each series was redrawn in pure red on a blank page-sized canvas (work/canvas/fig3X_<series>.png).
  - An isolated marker is its own dark page pixels inside its fitted footprint, dilated by 2 px.
  - A marker that overlaps another marker or an axis line is drawn as the fitted template.
  - digitize_figure.py extract --mode markers --open-px 0 --color #ff0000 was then run on each canvas, so each archive's source_image is that canvas. Archives: out/digitizations/HYC-0009_Fig3{A,B}_<series>.json.
- Confidence:
  - 4: own-pixel centre.
  - 3: template centre (overlap or axis contact).
  - 2: the first-pressure points of MWCNTs-95.7%, MWCNTs-97%, MWCNTs-99% and thinMWCNTs-95% in Fig. 3B, which form one pile-up. The thinMWCNTs plus there is visible only as one arm and one bar end.
- Marker counts (extracted = counted, origin excluded): Fig. 3A squares 12, circles 11, up triangles 12, diamonds 11, plus 11, down triangles 11, asterisks 11. Fig. 3B squares 15, circles 17, up triangles 15, diamonds 15, plus 15, down triangles 14, asterisks 14.
- Not separated: in both panels a marker cluster sits at the origin (0, 0). Only a square is visible, and the other series' markers are hidden beneath it. It was treated as the plotted origin, not a measured point: not extracted and not counted in isotherm_point_count.
- The tool rejected one stray 1-px connecting-line pixel in the Fig. 3B thinMWCNTs canvas (recorded in that archive).
- The tool's stated-value check (digitize_figure.py check) could not be run. The only values the paper states for these curves are Vs at 760 Torr, outside every series' digitized range (last points 704-750 Torr), and the tool refuses an x outside the range. All archives remain "unchecked". The informal agreement of the last points with Vs (within 0.61%) is listed above.
