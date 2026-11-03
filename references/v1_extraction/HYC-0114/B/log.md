# HYC-0114 extraction log (agent B)

## Sources extracted from
- main p.6, Section 3.4 text: 30 °C uptake end points (8.28 and 66.33 bar) for 700, 800 and 900 °C biochar (rows M1-M6, isotherms I1-I3), and the LN2 maximum 15.59 mol/kg at 46.71 bar for 900 °C biochar (row M12, merged with the last Fig. 8 bottom marker).
- main p.1, abstract: 2.50 mol/kg at 66.33 bar (900 °C biochar, ambient) is the same measurement as M6. "15.29 mol/kg at cryogenic temperature at 46.21 bar" conflicts with Section 3.4 and the conclusions (15.59 mol/kg at 46.71 bar). The digitized last marker (15.594 mol/kg) matches 15.59, so the abstract figure is treated as a misprint of M12 and gets no row of its own (recorded in M12 notes).
- main p.8, Section 4 Conclusions: 2.50 mol/kg at 66.33 bar (= M6) and 15.59 mol/kg at 46.71 bar (= M12). No new values.
- main p.8, Fig. 8 bottom panel (900-LN2, 77.15 K isotherm): digitized with digitize_figure.py in markers mode, archived as digitizations/fig8b_900-LN2.json (rows M7-M11, plus the digitized comparison point in M12).
  - Calibration: x 0 px 281.19, 50 px 1009.12, check 30 at 717.91 (rel. err 9e-5). y 0 px 894.75, 18 px 566.64, check 9 at 730.68 (rel. err 9e-5). Tick pixels found from pixel rows and columns.
  - Colour #ff0000, tolerance 40, ROI 270 595 1015 905 (excludes the legend), open-px 3, marker-min-px 12. With the default minimum size the tool returned one 9-px line fragment at about 42.1 bar, which is not a marker. The size filter removed it and is recorded in the archive as a rejected group.
  - Marker count: I count 7 markers on the plot: a marker at the axis origin, clipped by the axes so only its hollow quarter shows, plus 6 markers with error bars and drop lines. The tool separates the 6, not the origin marker, which is drawn mostly under the axis lines. The origin marker is not extracted and isotherm_point_count = 7.
  - Markers are half-filled circles. The opening keeps mostly the filled half, so centroids sit 1.6-2.5 px (0.11-0.17 bar) left of the paper's drop lines (drop lines at about 7.58, 15.60, 24.27, 32.17, 40.66, 46.73 bar; digitized 7.47, 15.44, 24.17, 32.04, 40.51, 46.56 bar). Tool output is recorded unchanged.
  - Step-6 check: stated 15.59 mol/kg checked at x = 46.557 (the last marker centroid; the stated 46.71 bar lies 0.15 bar outside the extracted range because of the centroid offset above): digitized 15.5938, diff 0.02 %, pass.
- main p.2, Table 2: BET area (Ar at -185.86 °C), total pore volume and average pore width for the 700, 800 and 900 °C biochars, carried on every uptake row of those samples.
- main p.2-3, Sections 2.2 and 2.4: methods (Tristar II 320 with Ar; PCT Pro Sieverts; He volume calibration at 4-5 bar; H2 99.999 mol%; drying, VacPrep degassing and 30 min / 30 °C in-situ degassing; 0.25-0.50 g sample).
- main p.4, Section 3.1 and Fig. 3c (XRD): SiO2, Fe2O3, KCl and SiC phases in 700 and 800 °C biochar (class composite), no visible peaks for 900 °C biochar (class other).

## Seen but not extracted
- main p.8, Fig. 8 top panel: a 3D ribbon plot (no markers) of the 30 °C isotherms of 700, 800 and 900 °C biochar, up to about 66 bar. Not digitized because it is a perspective 3D projection: its axes are not orthogonal pixel axes and the capacity ticks lie on a different plane from the ribbons, so the 2D calibration of digitize_figure.py does not apply. The highest-pressure point of each isotherm (66.33 bar), which is all the protocol asks for at a temperature other than 77 K, is printed in Section 3.4 (M2, M4, M6). There are no markers, so point counts are left empty.
- main p.2, Table 2, WS column (raw wheat straw: BET 2.49 m2/g, total pore volume 0.0040 cm3/g, average pore width 6.40 nm): not a sorbent tested for H2, so no row.
- main p.2, Table 2, 500 °C biochar column (BET 4.61 m2/g, total pore volume 0.0080 cm3/g, average pore width 6.97 nm): characterization only, no H2 uptake, so no row.
- 600 °C biochar (Table 3 yields only): no characterization, no H2 uptake.
- main p.2, Table 1: proximate and ultimate analysis of raw wheat straw (C 42.30 wt%, H 5.68, N 0.65, S 0.07, O 40.20 by difference; moisture 7.50, volatiles 71.20, ash 3.60, fixed carbon 17.70 wt%, air dried). This is the precursor's composition, not a sorbent's, so it is not stored.
- main p.3, Fig. 2: Ar sorption isotherms at -185.86 °C (WS, 700, 800, 900 °C biochar). Characterization, not H2 uptake.
- main p.4, Fig. 3a-c: FTIR, TGA, XRD. Characterization only.
- main p.5, Fig. 4 (carbon conversion), Table 3 (biogas, bio-oil and biochar yields), Fig. 5 and Fig. 6 (pyrolysis gas composition including H2 vol%), main p.7 Fig. 7 (syngas vol%), and the vol% values in Sections 3.2-3.3, the abstract and the conclusions (for example H2 86.07 vol% at 800 °C and 30 bar): H2 production from pyrolysis, not H2 uptake on a sorbent, so not extracted.
- main p.1, Introduction: DOE targets 5.50 wt% and 40.00 g/L. A target, not a measurement.

## Coding decisions
- sample_id numbers only the samples that get rows (S1 700 °C, S2 800 °C, S3 900 °C biochar), in order of first appearance. WS, 500 °C and 600 °C biochar get no rows and no sample_id.
- The labels "700 °C biochar" etc. are taken from the first figure legend that shows each sample (Fig. 2); no table reports uptake.
- The pyrolysis pressure of the biochar used for H2 and textural tests is not stated. Table 2 and Fig. 8 label samples by pyrolysis temperature only, so area_same_sample = yes.
- The 30 °C text values share isotherm_id with the plotted Fig. 8 top isotherm of the same sample, because Section 3.4 describes that figure's data ("(Fig. 8)" ... "increased from 0.39 to 1.70 mol/kg when adsorption pressure increased from 8.28 to 66.33 bar").
- The LN2 temperature is printed as -196 °C (abstract -196.0 °C), so 77.15 K is stored with temperature_inferred = false.
