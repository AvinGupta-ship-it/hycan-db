# HYC-0132 extractor A log

## Extracted from
- Main text p.6500-6501 (H2 paragraph): 1 atm, 77 K values C800 1.8 wt% (201 cm3(STP)/g), NC800 1.7 wt% (183 cm3(STP)/g), BNC800-1 1.4 wt%, BNC800-2 1.7 wt%. Also Table S1 (SI p.S5) H2 column, same wt% values. 4 rows.
- Surface area, pore volume: Table S1 (SI p.S5) and main text; N content: main text (elemental analysis); B 2.3 wt% in BNC800-1 by EELS (notes only). BET range 0.05-0.20: SI p.S1. Degassing 120 C overnight, instruments: SI p.S1.
- Fig. 5a (main text p.6501), 77 K H2 isotherms, y in cm3(STP)/g, x "Pressure (P)" with no unit (read as atm; end points are stated at 1 atm). Digitized with digitize_figure.py markers mode, archives in digitizations/Fig5a_<sample>.json (axes calibrated on x 0.0/1.0, third tick 0.4; y 0/250, third tick 100; residuals 0.14%). Rows: NC800 18 digitized + merged end point, BNC800-1 13 + merged, BNC800-2 14 (end point not merged), C800 7 + merged. Digitized rows = filled-marker clusters of at least 5 pixels (see limits below).
- Total 56 rows.

## Digitization limits (figure resolution is about 6 px per marker)
- Markers are about 4-5 px wide, drawn with a connecting line, and the four curves overlap; the tool returns connected colour components, not isolated markers. Filled-marker pitch is about 0.05 for P above 0.3 and about 0.025 below 0.3, where components merge with the line and with other series.
- Only clusters of at least 5 pixels were taken as markers. Components of 1-4 pixels (line fragments or partly hidden markers) were not used: C800 below P 0.56 (hidden under NC800; 0.185, 0.207, 0.229, 0.278, 0.319, 0.564), NC800 0.174 and 0.954, BNC800-1 below P 0.31 and 0.951, BNC800-2 below P 0.31 and the purple series at tol 30 contained other-colour fragments (removed as pixel_count < 5). Marker number on the plot is therefore not matched by extracted markers; the isotherm_point_count is left empty because the markers cannot be counted reliably.
- Open markers (desorption branch) have white centres and are not separable from line and filled markers; desorption branch not digitized for any sample. Filled = adsorption is assumed from the convention stated for the SI N2 figures (S2, S10, S11); Fig. 5 does not state it.
- BNC800-2 uses tolerance 30 (tolerance 45 collected blue pixels); others tolerance 45. ROI x 178-340 px, y 134-254 px to exclude the legend.
- Step-6 checks: C800 (0.34% vs 201), NC800 (0.26% vs 183) pass at 5%. BNC800-1 (-5.1% vs 155.7 = 1.4 wt% / 0.0089938) and BNC800-2 (-4.2% vs 189 = 1.7 wt%) pass only at a 6% tolerance because the paper states wt% only and its wt% exceeds the plotted end point. Stated values themselves are stored as printed.
- BNC800-2: the nearest plotted marker is 0.0207 bar from 1 atm, just over the 0.02027 bar merge tolerance, so its printed 1.7 wt% row has no isotherm_id and the digitized end marker is its own row. A small calibration shift would flip this.

## Seen but not extracted
- CO2 uptakes at 273 K and 298 K (main text, Fig. 4a/b, Table S1): not H2.
- Fig. 4c,d Qst and CO2/N2 selectivity: not H2.
- Fig. 5b: H2 uptake normalized per surface area (mmol m-2): not an uptake isotherm of the tables; not digitized; no value in tables or text.
- N2 isotherms Fig. 3a, S2, S10, S11 and PSD Fig. 3b: not H2.
- C600 (1125 m2/g, 0.75 cm3/g) and C1000 (1864 m2/g, 1.56 cm3/g), Table S1: characterization without H2 uptake ("-"); no rows. MIL-100(Al) (not carbon) and carbons made directly from ILs ("very low surface area"): no H2 value.
- Pore size distributions mainly 1-3 nm (NLDFT) for decorated carbons: no average diameter given, field left empty.
- Table S2 literature BN-decorated carbon surface areas: other materials.
- Isosteric heats, selectivities, XPS/EELS details beyond those noted: not uptake.
