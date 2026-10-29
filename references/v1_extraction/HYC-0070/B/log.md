# HYC-0070 extraction log (agent B)

Source: page images main-1 to main-7 only (no text layer). 27 rows written. Samples with rows: S1 = Ni20(arc), S2 = (unlabelled 1), the cobalt-containing sample.

## Passages, figures and tables extracted from

- main-1, abstract: 2.8 wt % "up to" at about 500 C and 30-50 atm (merged into the 50 atm TPD row M2); 1.6 wt % after 5 cycles (row M4); 2.7 wt % by PCI at 77 K and 70 atm (merged into row M27, together with the Figure 11B point).
- main-1/main-2, Experimental: TPD microreactor, PCI, IGA, BET, TPO methods. Used for method, degassing, sample mass, instrument and temperature coding.
- main-3, right column (TPO): 16.5 wt % Ni in Ni20C80(arc), used as metal_loading_wt_pct of S1.
- main-4, left column: ca. 2.3 wt % for Ni20(arc), TPD after adsorption at 35 atm (row M1).
- main-4, right column: ca. 2.8 wt % at 50 atm (row M2); cycling: initial 2.3 wt % (same as M1), 1.8 wt % after the first 3 cycles (row M3), ca. 1.6 wt % after 10 cycles (row M5).
- main-5, left column: ca. 1.6 wt % for cobalt-containing samples, 500 C and 35 atm (row M6).
- main-5, right column: BET 130 m2/g for Ni20(arc) (on every S1 row); 0.6 wt % at ca. -190 C and 6 atm from the IGA TG profile (row M7).
- main-6, left column: 0.4 wt % estimated at -200 C and 6 atm (row M8); ca. 1.6 wt % at 35 atm and 2.7 wt % at 70 atm by PCI, Figure 11b (rows M24 and M27, merged with plotted points).
- main-6, conclusions: 2.8 wt % at 500 C and 50 atm (same as M2); 2.7 wt % at liquid nitrogen temperature and 70 atm (same as M27).
- main-6, Figure 11B (Ni20(arc), PCI, liquid nitrogen temperature, 77 K in the abstract): digitized, rows M9-M27. Details below.
- No tables in the paper.

## Figure 11B digitization

- Axes calibrated on the page image main-6.png: x (Pressure, atm) 0 at px 723.2, 80 at px 1153.33, check tick 40 at px 938.4 (error 0.06%); y (H2 uptake, %) 0.0 at px 694.67, 3.0 at px 396.6, check tick 1.5 at px 545.57 (error 0.04%). Tick positions from intensity-weighted centroids of the tick marks.
- digitize_figure.py extract --mode markers, colour #000000, tolerance 40, ROI x 724-1152, y 410-694. Archive HYC-0070_fig11B_Ni20arc_PCI_77K.json. Check passed against the printed values at 70 atm (2.7, digitized 2.743, 1.6%) and 35 atm (1.6, interpolated 1.655, 3.4%).
- Markers counted on the plot: 22. The tool returned 19 points because two groups merged:
  - Two touching markers near 16 atm (they share an edge row) were returned as one point (16.14 atm, 0.930, 91 px). A larger opening (4 and 5 px) did not separate them. They were separated by rerunning with the same calibration on split regions: ROI x 801-810, y 598-612 (15.586 atm, 0.9025; archive HYC-0070_fig11B_Ni20arc_PCI_77K_split_a.json) and ROI x 811-822, y 590-603 (16.795 atm, 0.9629; archive HYC-0070_fig11B_Ni20arc_PCI_77K_split_b.json). The split boundary lies between the two markers in the colour mask, so neither marker is cut. These one-point archives cannot be run through `check` (a single point has no range); they share the calibration of the main archive, which passed.
  - Three overlapping markers at p < 1 atm, on top of the y axis, were returned as one point (0.535 atm, 0.337 wt %, 52 px). They overlap too much to be separated by colour or by a rectangular region (two lie at the same pressure, offset vertically by about 3 px; the third is about 0.5 atm higher). NOT EXTRACTED; the merged centroid is not a marker centre. They are counted in isotherm_point_count (22).
- The point near 33.5 atm (1.597 wt %) was merged with the printed "ca. 1.6 wt % at 35 atm (Figure 11b)": the paper gives the value as measured by PCI and cites Figure 11b, and the printed 1.6 equals this point. The printed pressure is 4.4% from it, outside the 2% rule. The curve interpolated at 35 atm is 1.655. If the reconciler applies the pressure rule strictly, this row splits into a digitized point (33.98 bar, 1.597) and a text value at 35.46 bar.
- The point near 70.08 atm (2.744 wt %) was merged with the printed 2.7 wt % at 70 atm (within 2%).

## Values seen but not extracted

- Ni40(arc) / Ni40C60(arc), Figure 5 and text: TPD peak at 539 C "about half" the intensity of Ni20(arc). This is relative, with no wt %. Characterization: 26.8 wt % Ni (TPO), 33 wt % residual.
- Ni80(arc), Figure 5 and text: peak shifted to 501 C with lower intensity. Relative, no wt %.
- C(arc), pure graphite after arc discharge, Figure 5 and text: desorption peak at 522 C. No wt % given.
- Mechanically mixed Ni (40 wt %)/graphite (60 wt %) before arc discharge, Figure 5: "almost plain line" (TPD peak at 489 C labelled in the figure). No value. A similar result is reported for pure graphite and for pure Ni powder. Pure Ni powder is not a carbon sorbent.
- Ni20(arc) after HCl removal of Ni: the residual carbon's uptake is "very similar to that of arc-charged graphite". No value.
- Cathode deposits: capacity "about 30-40% of those deposits on the chamber wall". Relative, with no absolute value, so not computed.
- Ambient pressure: "almost no adsorbed hydrogen was detected". No number.
- TPD and PCI results "in good agreement". No numbers.
- Figure 6 (Ni20(arc), TPD after adsorption up to 300, 400, 500 and 700 C at 35 atm): TPD profiles in arbitrary units. Not an isotherm, so not digitized. No wt % for 300, 400 or 700 C is given in the text.
- Figure 7 (Ni20(arc) cycles 1, 2, 3, 4, 5, 10): TPD profiles in arbitrary units. Not digitized. No wt % for cycles 2 and 4 is given in the text; cycle 5 is given only in the abstract (row M4).
- Abstract versus text: the abstract gives 1.6 wt % "after 5 cycles", and the text gives "after 10 cycles ... remained at ca. 1.6 wt %". Recorded as two rows (M4, M5), read as consistent ("remained"). If they are one measurement, M4 and M5 duplicate it.
- Figure 11A (IGA TG profile, -200 to 0 C at 6 atm): uptake against temperature. Not an isotherm, so not digitized. Values along the curve other than those in the text (0.6 wt % at ca. -190 C; uptake starting at ca. -120 C) are not extracted.
- "The small weight increase (<0.2 wt %) at temperatures between 0 and -120 C" at 6 atm: not extracted. The authors attribute it to moisture, not H2, and it spans a temperature range rather than a single temperature.
- BET 8.5 m2/g for the mechanical mixture (20 wt % Ni, 80 % graphite): characterization only. The paper gives no H2 value for that mixture.
- BET 284 m2/g for Ni20(arc) after H2 charge/discharge cycles: characterization of the cycled state. It is mentioned in the notes of the cycling rows M3-M5, which carry area_same_sample = unclear with the as-prepared 130 m2/g.
- Figure 9 (pore volume and pore area distributions, Ni20(arc) before and after 5 cycles): no total or micropore volume printed. Not digitized (characterization, not an isotherm).
- TPO (Figure 4, main-3): graphite 0.50 wt % residual; Ni powder +26.3 % (theoretical 28.3 %); residuals 21 wt % (Ni20C80) and 33 wt % (Ni40C60). These are metal-content data, not H2 uptake.
- Figures 1-3, 8 and 10 (TEM, XRD, Raman, FTIR, XPS): no H2 uptake values. Particle sizes (Ni 20-70 nm, Co 5-20 nm; Ni up to ca. 200 nm after cycling) are recorded in the material descriptions where relevant. SWCNT content < 3% is reported in the Co paragraph.

## Coding decisions worth review

- TPD rows (M1-M6): temperature_k is empty and temperature_unstated = true. The loaded state is at room temperature (words only). The printed adsorption temperature, 500 C (773.15 K), exceeds the 500 K field limit and is kept in notes. reference_temperature_k = 973.15 (TPD end, 700 C).
- IGA rows (M7, M8): measurement_mode = temperature_cycle, because the value is a weight increase recorded during cooling relative to the start of the profile. reference_temperature_k = 273.15 (0 C, the start of Figure 11A per its axis and caption). Gravimetric with no buoyancy correction stated, so basis_inferred = unknown.
- PCI rows: 77 K printed in the abstract, so temperature_inferred = false. The instrument has a manufacturer (Advanced Materials Corporation) but no model, so instrument_identified = false.
- Surface-area probe gas: the paper says "BET method at liquid-nitrogen temperature" without naming the adsorptive, so it is coded unspecified.
