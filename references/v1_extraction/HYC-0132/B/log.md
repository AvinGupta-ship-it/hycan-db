# HYC-0132 extraction log (agent B, 2026-11-09)

Aijaz et al., Chem. Commun. 2014, 50, 6498. Inputs: page images main-1..4 and si1-01..12 (no text layer). 76 rows written.

## Sources extracted

- main-3 (p. 6500), text, last paragraph: C800 "201 cm3 g-1 on STP, corresponding to 1.8 wt%, at 77 K and 1 atm". One row (M76), merged with the highest-pressure point of the Fig. 5a C800 series (digitized 0.99961 bar, 200.14 cm3/g; printed 1 atm is within 2% of it).
- main-4 (p. 6501), text, first paragraph: NC800 "At 1 atm ... 1.7 wt% (183 cm3 g-1 on STP)" (M23, merged with the NC800 highest-pressure point, 0.99520 bar, 183.30 cm3/g); BNC800-1 and BNC800-2 "1.4 and 1.7 wt%" with no pressure printed (M43, M66, merged with each series' highest-pressure point, pressure digitized). The paragraph discusses the Fig. 5a isotherms at 1 atm, so these are taken as the isotherm end points.
- si1-05 (p. S5), Table S1, column "H2 uptake (wt%) at 77 K": C800 1.8, NC800 1.7, BNC800-1 1.4, BNC800-2 1.7. These are the same values as the text and are on the same four merged rows. Table S1 also supplies the BET areas and pore volumes on every row.
- si1-02 (p. S2), Materials and Instrumentation: instrument (BELSORP mini II, volumetric, for gases other than N2), BET range 0.05-0.20, degassing ("preactivation at 120 oC overnight"), NLDFT PSD.
- main-2/main-3 text: N contents (NC800 14.8 wt%, BNC800-1 11.5 wt% by elemental analysis; BNC800-2 8.1 wt%), B 2.3 wt% in BNC800-1 by EELS, XPS bonding assignments.
- main-4 (p. 6501), Fig. 5a, H2 isotherms at 77 K, four series digitized (filled symbols): NC800 23 points (M1-M22 + merged M23), BNC800-1 20 (M24-M42 + M43), BNC800-2 23 (M44-M65 + M66), C800 10 (M67-M75 + M76).

## Fig. 5a digitization

- Page image main-4.png is 1241 x 1625 px (about 150 dpi). The plot is about 184 x 142 px and each symbol is about 3-5 px.
- Calibration on main-4.png pixel coordinates, tick centroids found from pixel row/column darkness profiles: x 0.0 at 145.93 px, 1.0 at 329.47 px, check tick 0.4 at 219.4 px (predicted 0.4003); y 0 at 251.29 px, 250 at 109.87 px, check tick 100 at 194.71 px (predicted 100.02). Same calibration for all four series.
- The legend (x 143-215, y 111-157 px) was painted white in a work copy of main-4.png (main-4_fig5a_legendmasked.png) so the legend symbols are not extracted. No curve pixel lies in that rectangle (checked). The archives name this masked copy as source image.
- x-axis is labelled "Pressure (P)" with no unit. The text gives the isotherm end as 1 atm, so the axis is read as atm and pressure_bar = axis value x 1.01325.
- Filled symbols are taken as the adsorption branch and open symbols as desorption (SI Figs. S2, S10, S11 state this, but the Fig. 5 caption does not). The open symbols are white-filled and drawn over the filled ones.
- Series settings for `digitize_figure.py extract --mode markers`:
  - NC800: #34549f, tol 40, opening 0, min 2 px, ROI x 163-338. Result: 23 symbols, P(axis) 0.108-0.982.
  - BNC800-1: #008042, tol 90, opening 1, min 2 px, ROI x 177-338. Result: 20 symbols, 0.186-0.985.
  - BNC800-2: #6e509f, tol 30, opening 0, min 3 px, ROI x 163-338. Result: 23 symbols, 0.106-0.980.
  - C800: #e92124, tol 60, opening 0, min 2 px, ROI x 246-338. Result: 10 symbols, 0.567-0.987.
- Marker counts: the extracted filled symbols equal the filled symbols counted inside each ROI. I counted them from per-column colour-fraction profiles along each curve, where filled-symbol maxima alternate with the white centres of open symbols. All four series fall on one pressure grid: filled-symbol x positions agree within about 1 px. That grid has steps of about 0.025 below P = 0.3 and about 0.05 above it.
- Near P = 0.95 each series has a filled symbol that is mostly hidden between two white-filled open symbols (at about 0.94 and 0.965). Only 2-3 px of it are visible, so its centroid is biased toward lower pressure by up to about 1-2 px. It is kept because it falls on the regular adsorption grid (about 92, 97, 100 kPa). Confidence 2.
- Symbols not separated and not extracted:
  - All four series, P < about 0.10 (the steep initial rise): the four curves overlap within 1-3 px and individual symbols cannot be separated or counted.
  - BNC800-1, P about 0.10-0.17: hidden under the BNC800-2 symbols, which are drawn on top. Symbols at 0.19-0.28 are partly covered (confidence 2).
  - C800, P about 0.10-0.51: hidden under the NC800 symbols, which are drawn on top. Only slivers are visible, so they were not extracted. The C800 symbol at 0.567 is partly covered (confidence 2).
  - Desorption branch (open symbols), all four series, not digitized. Their only distinguishing feature is a 1-2 px white centre. Their outline has no colour that `digitize_figure.py` can isolate from the filled symbols and the connecting line. A white-hole isolation was tried, but it found only some of the centres and also picked up background noise. Open symbols counted on the NC800 curve at P >= 0.1: 22 (from about 0.965 down to about 0.12).
- isotherm_point_count = 45 on all rows of I1-I4: 23 filled + 22 open symbols counted at P >= 0.1 on the NC800 curve, applied to all four because they share one pressure grid. This is a lower bound, because symbols below 0.1 cannot be counted.
- Step-6 checks (`digitize_figure.py check`, 5%):
  - C800 at axis 0.9865 against the printed 201 cm3/g: 200.13, pass.
  - NC800 at 0.982 against 183: 183.30, pass.
  - BNC800-2 at 0.9797 against the printed 1.7 wt% read as W1 (189.02 cm3/g): 180.97, -4.3%, pass.
  - BNC800-1 at 0.9849 against the printed 1.4 wt% read as W1 (155.66 cm3/g): 146.99, -5.6%, FAIL. The tool then marked that archive "discarded".
- Why the BNC800-1 check failed: the paper prints no value in the plotted unit for BNC800-1, so the check could only use a converted value. The paper's printed wt% values are inconsistent with its own cm3/g values. For NC800, 183 cm3/g gives W1 1.646 wt%, but 1.7 is printed. On the plot, the BNC800-1 end symbol lies below the 150 tick (pixel 168.1 against the tick at 166.25), while 155.66 would sit at pixel 163.2. The calibration is shared with the three series that pass. So I take the failure to come from the paper's wt% figure, not from the digitization.
- Disclosure of the re-run: I re-ran the extraction with identical settings (identical points) to out/digitizations/fig5a_BNC800-1_adsorption.json, which now has status "unchecked". The discarded archive is kept as work/fig5a_BNC800-1_adsorption_check-failed_discarded.json. The BNC800-1 rows and M43 state this in their notes.

## Values seen but not extracted

- Fig. 5b (main-4): H2 uptake from Fig. 5a normalized by surface area, plotted against pressure. It is the same measurements divided by the BET area, not a separate measurement, so it was not digitized. Its axis is labelled mmol m-2, but its values (C800 end about 0.075, BNC800-1 about 0.135) match cm3(STP) m-2 (201/2731 = 0.074), so the unit label looks wrong.
- CO2 data (not H2): Table S1 CO2 uptakes at 298 K and 273 K (C800 2.6/4.1, NC800 3.8/5.7, BNC800-1 3.1/4.0, BNC800-2 3.2/4.4 mmol g-1), Fig. 4a-b CO2 isotherms, the text's 2.3 mmol g-1 at 0.15 atm and 273 K for NC800, Fig. 4c Qst (26/23/17 kJ mol-1 quoted), and Fig. 4d / text CO2/N2 selectivities 22, 57 and 44.
- N2 sorption isotherms and PSDs (Fig. 3a-b, Figs. S2, S10, S11): characterization only. NLDFT pore sizes "mainly centered at 1-3 nm" for the decorated carbons (Table S2: 1-3 nm for BNC800-1/-2). This is a range, so average_pore_diameter_nm is left empty.
- Samples with characterization but no H2 uptake:
  - C600: BET 1125 m2/g, pore volume 0.75 cm3/g (Table S1, Fig. S10a).
  - C1000: BET 1864 m2/g, pore volume 1.56 cm3/g (Table S1, Fig. S10b).
  - Carbons from direct carbonization of EMIM DCN and EMIM TCB at 800 C: "very low surface area", N2 isotherms in Fig. S11, no numbers.
  - MIL-100(Al) (a MOF, not a carbon sorbent): PXRD and N2 isotherm (Figs. S1, S2).
- Table S2 (si1-12): surface areas and pore sizes of BN-carbon materials from other papers (refs 2-5 of the SI). These are literature values, not rows.
- Other inconsistencies noted:
  - BNC800-2 area: 1522 m2/g in Table S1 and the text, but also "~1525" and "1525 m2 g-1" in the text. 1522 is used.
  - The SI figure captions label samples "CN800" and "BCN800-1" (Figs. S3, S7, S8) for NC800 and BNC800-1.
