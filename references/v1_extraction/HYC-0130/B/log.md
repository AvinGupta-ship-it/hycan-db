# HYC-0130 extraction log (agent B)

## Sources extracted from

- Main p. 8 (journal p. 20419), Table 5 "This publication" rows: H2 uptake (mg g-1) of ACZ-3-8 11.6, ACK-3-8 17.1, ACK-2-7 16.7, ACK-2-8 17.3, ACK-2-8-1 20.2, ACK-2-8-2 25.2, ACK-2-8-3 22.8. Each is merged with the last marker of the matching plotted isotherm (printed 1 bar, last markers at 0.987-0.991 bar), 7 rows, table_direct. The temperature and pressure (-196 C, 1 bar) come from the Fig. 7b caption, the text on p. 7 and the Fig. S4 caption. ACK-2-8 is merged with the Fig. 8 marker (0.99025 bar), which is closer to 1 bar than the Fig. 7a marker (0.98688 bar).
- Main p. 8, Fig. 7a: H2 isotherms at -196 C, 0-1 bar, for ACK-2-7, ACK-2-8, ACK-3-8 and ACZ-3-8. All four series are digitized (I1-I4).
- Main p. 8, Fig. 8: H2 isotherms at -196 C, 0-1 bar, for ACK-2-8, ACK-2-8-1, ACK-2-8-2 and ACK-2-8-3. All four series are digitized (I5-I8).
- Main p. 3 (journal p. 20414), section 2.3: instrument for H2 (NOVA 3200e, Quantachrome, static volumetric; 0.01-1 bar at -196 C), and BET/t-plot/BJH from N2 at -196 C (JW-BK122W). No degassing, sample mass, H2 purity, free-volume calibration or BET P/P0 range is stated for any measurement.
- Main p. 2 (journal p. 20413), section 2.2: synthesis, activation, washing and HNO3/H3PO4/NH3.H2O modification. These go in the activation, purification and description fields.
- Main pp. 5-6 (journal pp. 20416-20417), Tables 3 and 4: S_BET, V_total, V_micro and D-bar for the seven samples that have H2 data, carried on every row.
- Main p. 7 (journal p. 20418), section 3.3 text and Fig. 6 (XPS): N species of ACK-2-8-1 and ACK-2-8-3 and the P-O of ACK-2-8-2. These go in functional_groups. The figure is not digitized.
- SI p. 5, Fig. S3 (Boehm titration): used only qualitatively, as text, in functional_groups. The bar heights are not digitized.

## Digitization

- Both figures are on page image main-08.png. Each calibration uses the lowest and highest labelled ticks, with a third labelled tick as a check. Every tick pixel position is a weighted centre of the tick-mark pixels.
- Fig. 7a calibration: x 0.0 at px 269.48 and 1.0 at px 612.5 (check 0.6 at px 475.37, residual 0.03%). y 0 at px 353.54 and 200 at px 121.82 (check 100 at px 237.54).
- Fig. 8 calibration: x 0.0 at px 160.5 and 1.0 at px 582.11 (check 0.6 at px 413.55, residual 0.03%). y 0 at px 1418.01 and 300 at px 1105.52 (check 150 at px 1261.79, residual 0.02%).
- Run settings: `--mode markers` with the following colour, tolerance, open-px and marker-min-px for each series.
  - Fig. 7a ACK-2-7: #000000, tolerance 100, open-px 0, min-px 9.
  - Fig. 7a ACK-2-8: #c84648, 90, 0, 6.
  - Fig. 7a ACK-3-8: #3a529f, 60, 0, 7.
  - Fig. 7a ACZ-3-8: #a3719b, 37, 0, 6.
  - Fig. 8 ACK-2-8: #000000, 100, 2, 15.
  - Fig. 8 ACK-2-8-1: #ee3a32, 80, 0, 8.
  - Fig. 8 ACK-2-8-2: #3953a4, 60, 0, 13.
  - Fig. 8 ACK-2-8-3: #b264a8, 40, 0, 9.
- Choice of min-px: about 35% of the size of a full marker in that series, so that slivers too small to locate a marker centre are rejected. Any rejection is recorded in the archive.
- Deviation from "one file per series": a single rectangular region cannot cover a series without also taking in the legend symbol of the same colour, the "(a)" label, or, for the Fig. 7a red series, ACZ-3-8 outline pixels. Most series were therefore run in 2 or 3 region tiles, each in its own archive. Every row names its archive. The files are:
  - fig7a_ACK-2-7_p1/p2
  - fig7a_ACK-2-8_p1/p2/p3
  - fig7a_ACK-3-8_p1/p2
  - fig7a_ACZ-3-8_p1/p2
  - fig8_ACK-2-8_p1/p2
  - fig8_ACK-2-8-1_p1/p2
  - fig8_ACK-2-8-2_p1/p2
  - fig8_ACK-2-8-3_all
- Marker counts: every series has 30 markers on the plot, adsorption branch only.
  - Fig. 7a ACK-2-7: 28 extracted.
  - Fig. 7a ACK-2-8: 26 extracted.
  - Fig. 7a ACK-3-8: 30 extracted.
  - Fig. 7a ACZ-3-8: 30 extracted.
  - Fig. 8 ACK-2-8: 30 extracted.
  - Fig. 8 ACK-2-8-1: 28 extracted.
  - Fig. 8 ACK-2-8-2: 23 extracted.
  - Fig. 8 ACK-2-8-3: 29 extracted.
- Endpoint check: `digitize_figure.py check` was run on the archive holding each series' highest-pressure marker. The expected value was the Table 5 value converted to cm3(STP)/g (mg g-1 / 2.01588 x 22.414). All 8 checks passed: digitized values lie 0.65-0.93% above the expected value, and 1.24% above for the Fig. 7a ACK-2-8 upper-arc centroid. The low-pressure tile archives have no value stated by the paper to check against and stay "unchecked".
- Units: the y axes read "Adsorbed H2 Volume (cm3/g)" without saying STP. They are read as cm3(STP)/g, which matches the Table 5 mg g-1 values. The wt% is computed as W1.
- The paper states an H2 range of 0.01-1 bar, but the first markers digitize at 0.002-0.007 bar. That is within about 2 px of the y axis, so within the digitization error.

## Markers not separated (not extracted)

- Fig. 7a ACK-2-7: the marker at about 0.002 bar is fully hidden under the other series' first markers at the y axis (it is counted because the series line visibly starts there). The marker at about 0.035 bar shows only as a 2-px sliver below the ACK-3-8 triangle and was rejected by size.
- Fig. 7a ACK-2-8 (red open circles): the markers at about 0.002, 0.035, 0.075 and 0.105 bar show only as small red fragments beside the ACK-3-8 triangles.
  - The 26 extracted markers show only their upper arc. Their centroids lie 0.3-1.1 cm3/g above the same points in Fig. 8 (see below). They are flagged in notes with confidence 2.
- Fig. 8 ACK-2-8-1: the markers at about 0.005 and 0.035 bar are hidden under the first markers of the other series.
- Fig. 8 ACK-2-8-2: the markers at about 0.005, 0.07, 0.105, 0.14, 0.20, 0.24 and 0.27 bar are hidden under, or split into fragments by, the ACK-2-8-3 open down-triangles drawn on top of them.
- Fig. 8 ACK-2-8-3: the first marker, at about 0.005 bar, shows only as a 4x2-px sliver at the y axis.
- Partly occluded markers that were extracted are flagged in their row notes with extraction_confidence 2:
  - Fig. 7a ACK-2-7 at 0.079, 0.101 and 0.209 bar.
  - The first markers of Fig. 7a ACK-3-8, Fig. 7a ACZ-3-8 and Fig. 8 ACK-2-8.
  - Fig. 8 ACK-2-8-1 at 0.066 bar.
  - Fig. 8 ACK-2-8-2 at 0.040, 0.169 and 0.306 bar.

## Same run plotted twice (flag for reconciliation)

- The Fig. 7a ACK-2-8 curve and the Fig. 8 ACK-2-8 curve coincide marker by marker over 26 common points: pressures agree within 0.006 bar and values within 1.1 cm3/g.
- They therefore look like one run plotted twice. Under the rule "each plotted curve is one run" they are coded as separate isotherms (I2, I5), and every row of both says so in notes.
- replicates_reported is false, because these are not independent measurements.
- If the reconciler treats them as one run, I2 (26 rows) duplicates I5.

## Values seen but not extracted

- Table 5, "H2 uptake per S_BET (mg m-2)" column: 0.0088, 0.0092, 0.0099, 0.0089, 0.0109, 0.0133, 0.0107. These are ratios derived from uptake and S_BET, not measurements, and not the areal uptake of a film.
- Table 5, "Ref." rows: values for other papers' materials, cited for comparison and not measured in this paper. The table gives no conditions for them, several are ranges summarizing many samples, and the MOFs are not carbon. The rows are:
  - C-4 (ref. 8): 3870 m2 g-1, 39 mg g-1, 0.01.
  - P2 (ref. 31): 1807, <20, <0.0111.
  - Carbide-derived carbons (ref. 10): <3000, 3-27, <0.01.
  - MOFs (ref. 7): 1132-4346, 11.7-25.4, <0.01.
  - Zeolite-based carbons (ref. 43): 2254, 22.7, 0.0101.
  - PC-2-800 (ref. 5): 2919, 27.1, 0.0093.
  - ACs (ref. 28): <2500, <20, 0.008.
  - ACs (ref. 3): 2849, <30, <0.01.
  - CAC (ref. 44): 1767-3711, 19.2-32.1, 0.0086.
  - UCs (ref. 45): 1127.2, 1.43, 0.0013.
- Main p. 8, Fig. 7b: H2 uptake against S_BET for ACZ-3-8, ACK-2-7, ACK-3-8 and ACK-2-8, with a linear fit (R2 = 0.9163, p. 7). It is not an isotherm, and its values are those of Table 5.
- SI p. 6, Fig. S4: H2 uptake against S_BET for ACK-2-8 and ACK-2-8-1/-2/-3, with a fit (R2 = 0.0214, p. 7). It is not an isotherm, and its values are those of Table 5.
- Text: the uptakes repeated in the abstract, p. 7 and the Conclusions are the same measurements as Table 5 (17.3 and 25.2 mg g-1 "at -196 C and 1 bar") and are recorded once, on the Table 5 rows. The relative values are derived and not extracted: "16.8%, 31.8%, and 45.7% higher" than ACK-2-8 (abstract), "49.1% higher than ... ACZ-3-8" (p. 7) and "45.7% higher" (p. 7).
- Characterization only, no H2 uptake, so no rows. Values are S_BET (m2 g-1), V_total, V_micro (cm3 g-1) and D-bar (nm):
  - AC, carbonized only (Fig. S2, SI p. 4): S_BET 10.7, V_total 0.011, D-bar 4.02; N2 isotherm shown.
  - Table 2 (p. 4):
    - ACK-0.5-6: 644, 0.404, 0.312, 4.81.
    - ACK-1-6: 705, 0.429, 0.344, 4.62.
    - ACK-2-6: 1006, 0.578, 0.505, 2.30 (also in Table 3).
    - ACK-3-6: 970, 0.545, 0.454, 2.23 (also in Table 3).
    - ACZ-1-6: 901, 0.514, 0.428, 2.28.
    - ACZ-2-6: 996, 0.640, 0.496, 2.31.
    - ACZ-3-6: 1268, 0.760, 0.531, 2.39 (also in Table 3).
  - Table 3 (p. 5):
    - ACK-3-7: 1111, 0.592, 0.487, 2.13.
    - ACZ-3-7: 1176, 0.720, 0.505, 2.45.
  - Fig. S1 (SI p. 3): S_BET against activation time (0.5, 1, 2, 3 h) for ACK-2-8 and ACZ-3-8. The samples at 0.5, 1 and 3 h have no H2 data, and the figure is not an isotherm. It was not digitized.
- Other non-H2 content, not extracted:
  - Table 1 (p. 3): proximate and ultimate analysis of the raw cyanobacteria (moisture 15.03, volatiles 68.04, ash 5.97, fixed carbon 10.96; C 43.28, H 6.36, O 35.81, N 7.7, S 0.88 wt%).
  - Table S1 (SI p. 2): XRF of cyanobacteria ash.
  - Fig. 1: TG/DTG.
  - Figs. 2-4: N2 isotherms and PSDs.
  - Fig. 5: SEM.
  - Fig. 6: XPS spectra (only the peak assignments are used).
  - Fig. S3: acidic and basic group amounts (mmol g-1, bar chart).
- No non-carbon sorbent of this paper was measured for H2.
