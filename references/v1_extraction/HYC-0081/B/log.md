# HYC-0081 extraction log (agent B)

Kumar et al. 2013, Chem. Commun., "Porous graphene frameworks pillared by organic linkers with tunable surface area and gas storage properties". Inputs: page images main-1..3 and si1-01..12; no text layer. 46 rows written.

## Sources extracted from

- main-1.png (p. 2015), abstract: "nearly 1.2 wt% H2 ... at 77 K and 1 atm, increasing to ~1.9 wt% at high pressure". These repeat the main-text values; no separate rows (see M1, M21).
- main-2.png (p. 2016), right column: N2 porosity text, giving BET, Langmuir, NL-DFT pore volume and pore widths for PGF-1 and PGF-2, and the RGO BET area. Left column: PXRD d-spacings (2.1 and 2.4 nm) and the synthesis summary.
- main-2.png, Fig. 3d (H2 at 77 K to 1 atm, cc/g; PGF-1 red, PGF-2 blue): only the last marker of each series was digitized, and only for the notes of M1 and M2. Archives: fig3d_PGF-1_red_last.json, fig3d_PGF-2_blue_last.json.
- main-3.png (p. 2017), text: "PGF-1 and PGF-2 adsorb 1.2 and 1.0 wt% of H2, respectively, at 1 atm and 77 K (Fig. 3d)" gives M1 and M2, each merged with the last Fig. 3d marker.
- main-3.png, text: "at high pressure the PGF frameworks show nearly 1.9 wt% and 1.8 wt% of H2 uptake (~20 atm, Fig. 4b)" gives M21 and M44, each merged with the last Fig. 4b marker of its series. Both are uptake_bound = approximate.
- main-3.png, Fig. 4a (PGF-1, 77 K blue and 87 K red, cc/g, to 1 atm): highest-pressure marker of each curve (M3 = I3, M4 = I4). Archives: fig4a_PGF-1_77K_blue_last.json, fig4a_PGF-1_87K_red_last.json.
- main-3.png, Fig. 4b (77 K to 20 atm, wt%; PGF-1 blue, PGF-2 red per caption):
  - PGF-1: 17 separated markers (M5-M21, I5). Archives: fig4b_PGF-1_blue_a.json and fig4b_PGF-1_blue_b.json.
  - PGF-2: all 23 markers (M22-M44, I6). Archives: fig4b_PGF-2_red_a.json, _b, _c and _d.
- si1-10.png, Fig. S12 (PGF-2, 77 K blue and 87 K red, mL/g, to 1 atm): highest-pressure marker of each curve (M45 = I7, M46 = I8). Archives: figS12_PGF-2_77K_blue_last.json, figS12_PGF-2_87K_red_last.json.
- si1-03.png and si1-04.png, SI Adsorption Measurements, give the methods:
  - Quadrasorb-SI for the low-pressure isotherms: 433 K, 0.1 Pa, about 6 h, ~100-150 mg, helium expansion.
  - BELSORP-HP for the high-pressure isotherms: 433 K, 18 h, 0.1 Pa, about 200 mg, He dead volume, H2 99.999%, virial non-ideal correction.
- si1-02.png: synthesis of RGO-IBz, PGF-1 and PGF-2, and purification.

## Figure digitization details

- All axes were calibrated on the lowest and highest labelled ticks, with a third labelled tick as the check. Every tick was located from pixel columns and rows. Every check passed, with residuals of 0.41% or less (largest: the Fig. S12 y axis).
- Fig. 4b, PGF-1 (blue):
  - The plot has 22 markers. The 5 lowest-pressure markers (below about 2 atm, about 0.55-0.95 wt%) are drawn under the PGF-2 markers, show only as edge fragments, and could not be separated. They were not extracted. Their count is uncertain by about one.
  - The other 17 needed two ROI runs. With a 2-px opening, the four markers at 11.9-15.0 atm stayed joined; a 3-px opening separates them but erodes the partly covered low-pressure markers. So part a (P < 11.3 atm) used open-px 2 and part b (P > 11.3 atm) used open-px 3.
  - The markers at 2.4, 3.3 and 5.5 atm are partly covered by red markers. They are given confidence 2.
- Fig. 4b, PGF-2 (red), 23 markers:
  - Part a: 17 markers from 2.3 to 20.1 atm.
  - Part b: the 4 lowest markers, separated with a 3-px opening.
  - Parts c and d: an overlapping pair near 1.0 and 1.2 atm that no opening separated. Each was isolated with an ROI limited to its own rows. The lower marker's top is hidden, so its centroid may sit about 1 px low. Both are given confidence 2.
- Fig. 3d, Fig. 4a and Fig. S12 (all to 1 atm): the markers of every curve overlap so heavily that markers mode returns one blob per curve. In Fig. 3d the filled triangles merge into a solid band. So only the highest-pressure marker of each curve was digitized, with an ROI equal to that marker's bounding box. Moving the ROI by 1-3 px changes the centroid by at most 0.7% in pressure and 0.4% in uptake. All other markers of these 6 curves are not separable and were not extracted. Their number cannot be counted, so isotherm_point_count is empty for I1-I4, I7 and I8.
- Stated-value checks (digitize_figure.py check):
  - Passed: fig4b_PGF-1_blue_b at 20 atm vs 1.9 wt% (1.1%); fig4b_PGF-2_red_a at 20 atm vs 1.8 wt% (1.8%); fig3d_PGF-1_red_last vs 1.2 wt% (= 133.4 cc/g as W1; 1.3%).
  - FAILED: fig3d_PGF-2_blue_last vs 1.0 wt% (= 111.2 cc/g as W1). The plotted end point is 120.2 cc/g (1.08 wt%), 8% higher, and the tool set the archive status to discarded. The calibration checks out, and Fig. S12 independently ends at 120.4 mL/g at 0.988 atm. So the printed 1.0 wt% is low, not the digitization. M2 stores the printed 1.0 wt%. The digitized point appears only in its notes, with this explanation.
  - Unchecked (the paper states no value in their range): fig4b_PGF-1_blue_a, fig4b_PGF-2_red_b/c/d, both fig4a archives and both figS12 archives.
- Duplicate curves:
  - The Fig. 4a 77 K curve ends at 134.7 cc/g at 0.978 atm, matching the Fig. 3d PGF-1 end point.
  - The Fig. S12 77 K curve ends at 120.4 mL/g at 0.988 atm, matching the Fig. 3d PGF-2 end point.
  - Both are probably replots of the Fig. 3d isotherms, but the paper does not say so. Following "each plotted curve is one run", they carry their own isotherm_ids (I3, I7). This is flagged in the notes.

## Values seen but not extracted, with reasons

- Fig. 3d: all markers except the last of each series. They merge into a continuous band and cannot be separated (see above).
- Fig. 4a and Fig. S12, 77 K curves: all markers except the last. Overlapping open triangles that cannot be separated.
- Fig. 4a and Fig. S12, 87 K curves: points below the highest pressure. These are not 77 K, so only the highest-pressure point is in scope.
- Fig. 4b PGF-1: 5 low-pressure markers hidden behind PGF-2 markers. They cannot be separated.
- Fig. 4a inset and Fig. S12 inset: isosteric heat against uptake. Not an isotherm, not digitized. The text gives initial Qst 7.9 kJ/mol (PGF-1) and 8.7 kJ/mol (PGF-2). These are not uptake values.
- Table S1 (si1-11.png, si1-12.png): virial fit parameters for the 77/87 K H2 isotherms. These are not uptake values.
- Non-H2 data are out of scope:
  - N2: final uptake 477 mL (PGF-1) and 571 mL (PGF-2).
  - CO2 at 195 K: 572 and 301 mL, i.e. 112 and 60 wt%, about 0.85 atm.
  - CO2 at 273 K: 42 and 36 wt% at about 30 atm.
  - CO2 at 273/293 K and 1 atm: PGF-1 7.2/5.5 wt%, PGF-2 7.7/6.3 wt%.
  - DR heats of CO2 adsorption: 27.4 and 27.7 kJ/mol.
  - CH4 at 195 K and 1 atm: 50 mL (3.57%) and 48 mL (3.40%).
  - Figs. 3a-c, S11 and S13.
- Samples with characterization but no H2 uptake get no rows:
  - RGO: BET 42 m2/g; type-II N2 isotherm, Fig. S10b; PXRD, Fig. S5d; 13C NMR, Fig. S3; interlayer spacing about 0.34 nm.
  - GO: BET 14 m2/g, Fig. S10a; PXRD, Fig. S5c.
  - RGO-IBz: FTIR, XPS (I 3d, C 1s) and Raman; no surface area.
- Not digitized because they are not isotherms: Fig. S8/S9 (NL-DFT pore-size distributions), Figs. S1, S2, S4-S7, Fig. 1, Fig. 2.
- The paper has no non-carbon comparison sorbents (no MOF, zeolite or hydride values) and no multi-laboratory or consensus values.
