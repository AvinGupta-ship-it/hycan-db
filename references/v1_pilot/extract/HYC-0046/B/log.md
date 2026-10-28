# HYC-0046 extraction log (agent B, 2026-10-27)

Input: 5 page images (main-1 LLNL cover, main-2 disclaimer, main-3 and main-4 article, main-5 TOC graphic and web abstract). No supplementary file in the input. 62 rows written.

## Sources extracted from

- Figure 1 (p.3), 77 K adsorption isotherms of five samples, monochrome open markers on a 150 dpi raster. Digitized with `scripts/digitize_figure.py` v2.1, markers mode, `--open-px 0`, on the page image `HYC-0046_main-3.png`. Calibration: x ticks 0 bar = px 730 and 40 bar = px 1093, verified at 20 bar = px 912. y ticks 0 wt% = px 973 and 5 wt% = px 753, verified at 3 wt% = px 841. Tick pixels located by inspecting pixel rows and columns. Series separated by grey class (black outlines: circles and squares, `#000000` tolerance 105; anti-aliased grey outlines: up-triangles, diamonds and down-triangles, `#808080` tolerance 150), by pixel-count window and by region of interest. Each archive holds one series only. The marker count in every archive equals the separable markers counted in its region. An overlay of all centroids on the figure was checked by eye for series assignment only, not for values.
  - 3200 m2/gm (up-triangles), isotherm I1: `HYC-0046_fig1_3200_partA.json` (3 markers, 1.1 to 2.8 bar, status unchecked: no printed value falls in its range) and `HYC-0046_fig1_3200_partB.json` (9 markers, 4.6 to 35.5 bar, check passed at 30 bar against the printed 5.3 wt%).
  - 2550 m2/gm (circles), isotherm I2: `HYC-0046_fig1_2550.json` (15 markers, 1.75 to 30.4 bar, check passed at 30.43 bar against the Table 1 value 5.0) and `HYC-0046_fig1_2550_partB.json` (1 marker at 36.2 bar, unchecked). The last circle was digitized separately with its ROI starting at the circle's left edge (px 1055), so the base of the overlapping 3200 triangle (px 1050 to 1054) is not in the centroid.
  - 2000 m2/gm (squares), isotherm I3: `HYC-0046_fig1_2000_partA.json` (2 markers, 0.72 and 2.70 bar, unchecked) and `HYC-0046_fig1_2000_partB.json` (9 markers, 4.1 to 34.5 bar, check passed at 28.21 bar against the Table 1 value 4.2).
  - 1460 m2/gm (diamonds), isotherm I4: `HYC-0046_fig1_1460_partA.json` (7 markers, 2.8 to 20.1 bar, unchecked) and `HYC-0046_fig1_1460_partB.json` (3 markers, 25.6 to 38.0 bar, check passed at 31.33 bar against the Table 1 value 3.5).
  - 330 m2/gm (down-triangles), isotherm I5: `HYC-0046_fig1_330.json` (8 markers, 4.9 to 33.2 bar, check passed at 20 bar against the printed 0.8 wt%).
  - The checks for 2550, 2000 and 1460 use the digitized pressure of each isotherm's highest marker, because Table 1 gives saturation values with no pressure. They test the y value only.
  - Re-extractions (no check had been recorded on either archive): the first `2000_partB` run used ROI x0 = 760 and picked up a cropped 2550 circle at 3.64 bar as a square. It was re-run with x0 = 765. The first `2550` run included the 36 bar circle merged with the 3200 triangle base. It was re-run with x1 = 1049, and `2550_partB` was added.
  - Four 3200 markers and one 2550 marker lie above the highest labelled y tick (5 wt%), so the tool flags them `outside_axis_range`. The axis is linear and the points are inside the plot frame.
- Table 1 (p.4): H2 (wt%) saturation values at 77 K for 10 samples. ACA 1460, 2000 and 2550 each equal their Fig. 1 maximum and replace that digitized marker (pressure taken from the digitization). ACA 3200 is recorded once, together with the p.3 text value. ACA 1700, Co-CA-800/1050 °C and Ni-CA-800/1050 °C are single rows with `pressure_unstated = true`.
- p.3 text, Fig. 1 discussion: "The sample with the surface area of 330 m2/g adsorbs 0.8 wt% at 20 bar". Recorded as row M55, replacing the 330 marker digitized at 18.95 bar / 0.82 wt%.
- p.3 text: "the 3200 m2/g sample adsorbs 5.3 wt% hydrogen at 30 bar pressure". Recorded as row M11, replacing the 3200 marker digitized at 28.83 bar / 5.28 wt%. The same value appears in Table 1 and in the abstract.
- p.3 text, Ni: "lower BET surface area (970 m2/g vs 1100 m2/g)". Used as the BET area of Ni-CA-800 °C and Ni-CA-1050 °C.
- p.3 and p.4 text, methods and coding: Sieverts volumetric method; "excess sorption measurements" (basis named, not defined, so `basis_stated = false` and `basis_inferred = excess`); "only adsorption isotherm traces are shown ... adsorption and desorption data were identical"; N2 BET areas; undoped CAs CO2-activated at 950 °C.
- p.4 text, wt% convention: mass% is defined as (mg H2)/(g aerogel), and the paper states that its wt% "yields a slightly lower quantity than values expressed in mg of sorbed hydrogen per gm of sorbent". Fig. 2 caption: "1 mass% sorption per 500 m2/g, converted to wt%". Coded as W2, `stated`, on every row.

## Markers seen but not extracted (not separable)

`isotherm_point_count` counts every marker of the source isotherm, including these. The counts are approximate (about ±2) because the markers overlap below about 2 bar. The colour TOC reproduction (p.5) was used only to confirm series identity and marker counts in that region.

- 3200 (I1, 15 markers): 3 not separated, near 0.9 bar/2.4 wt%, 0.3 bar/1.7 wt% and P near 0 / 0.9 to 1.0 wt%. They overlap circles, squares or the y axis.
- 2550 (I2, 21 markers): 5 not separated, near 1.2/2.4, 0.8/2.1, 0.4/1.6, 0.2/1.25 and 0.1/0.8 (bar/wt%).
- 2000 (I3, 19 markers): 8 not separated, near 1.65/2.4, 1.05/2.1 and 0.55/1.5, plus five below 0.3 bar between 0.2 and 1.2 wt%.
- 1460 (I4, 18 markers): 8 not separated, near 1.8/2.2 and 1.3/2.0 (two touching diamonds), 0.6/1.8, plus five below 0.5 bar between 0.3 and 1.4 wt%.
- 330 (I5, 17 markers): 9 not separated, a chain of touching down-triangles from about 3.4 bar/0.55 wt% down to P near 0. Pairs at 3.4 and 2.7 bar touch, as do the markers below them.

## Values seen and not extracted (other reasons)

- Table 1 ΔH (kJ/mol) for all 10 samples (6.7, 6.5, 6.4, 6.4, 6.2, 7.5 (7.2), 7.0 (7.1)). Differential enthalpies, not uptake; no schema field.
- Figure 2 (p.4), saturation value vs BET area. Every y value duplicates Table 1, or the 0.8 wt% text value for the 330 sample. The Co-CA BET areas appear only as x positions in Fig. 2, and those markers overlap other metal-modified markers of the same style, so no area was digitized. The Co rows carry no area (`surface_area_method = BET`, null value, `area_same_sample = unclear`). The Ni-CA-800 °C marker plots at about the 1000 tick against a printed 970 m2/g, so Fig. 2 x positions are not more reliable than the text.
- p.3 text, Co: "saturation values of ~2.1 wt% for each sample". Ni: "(2.3 wt% vs 2.0 wt%)". Both duplicate Table 1.
- p.4 text: "yielding up to 5 wt%" (duplicates 2550), "gravimetric density of 5.3 wt%" and "The absolute value of 5.3 wt%" (duplicates 3200; "absolute" here means magnitude, not the absolute basis), "saturation occurs typically at ~30 bar" (general statement, no sample), ">7kJ/mole" (enthalpy).
- p.3 and p.4 text: "1% for every 500 m2/g", "~35 bar", 2630 m2/g for graphene. These are literature rules or reference figures, not measurements in this paper.
- Abstract (p.5): "5.3 wt% at 30 bar pressure at 77 K" duplicates row M11. "~5 to 7 kJ/mole" is enthalpy.
- TOC graphic (p.5): a lower-resolution colour reproduction of Figs. 1 and 2. Not digitized, because it duplicates Fig. 1.
- Supporting information Figure 1S (77 K isotherms of the Ni- and Co-modified aerogels) is cited on p.3 and p.4 but is not in the input pages. Not extracted.
- No characterization-only rows: every sample with an area also has an uptake row carrying that area.
