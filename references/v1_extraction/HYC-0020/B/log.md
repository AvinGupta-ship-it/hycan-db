# HYC-0020 extraction log (agent B, 2026-11-09)

Input: page images only (main-01..11, si1-1..7). 20 rows written; 20 digitization archives in `digitizations/`.

## Sources extracted from

- main p. 1, Abstract: "G-800 adsorbs 13.63 mmol H2/g (2.73 wt%) at 25 C and 45 bar" -> row M1 (same point as sec. 3.2, Conclusions and Fig. 8b).
- main p. 2, sec. 2.1: preparation (KOH 1/1 wt/wt, carbonized 1 h at 700-900 C under N2, HCl wash, dried 200 C) -> synthesis/activation/purification fields of all rows.
- main p. 2, sec. 2.2: N2 (-196 C) and CO2 (0 C) adsorption on QUADRASORB evo, BET range 0.05-0.25, V_tot at P/P0 = 0.99, NLDFT; H2 purity 99.999 %; 25-100 C up to 45 bar; degassing 16 h under vacuum at 200 C; cycles 1, 3, 5, 10 -> method/characterization fields of all rows.
- main p. 4, Table 3: BET area, total pore volume, N2 micropore volume (1.4-2 nm), CO2 micropore volume (0.3-1.4 nm) for G-700, G-800, G-900 -> characterization fields of all rows.
- main p. 5, sec. 3.2 para 2: 13.63 (25 C, 45 bar), 9.61, 6.51, 5.93, 4.52 mmol/g for G-800 (40-100 C); 10.09 (G-700) and 8.23 (G-900) mmol/g at 25 C; ranges 8.63-3.54 (G-700) and 6.40-2.91 (G-900) mmol/g for 40-100 C -> rows M1-M5, M11, M12, M15, M16, M17, M20.
- main p. 10, Conclusions bullet 3: G-800 at 45 bar 13.63 (2.73 wt%), 9.61 (1.92 wt%), 6.51 (1.302 wt%), 5.93 (1.186 wt%), 4.52 (0.904 wt%) mmol/g at 25, 40, 60, 80, 100 C -> rows M1-M5 (wt% stored; printed wt% = 0.2 x mmol/g, neither W1 nor W2 with 0.201588 matches within printed rounding, convention coded unknown/none).
- main p. 6, Fig. 8a-c: 15 H2 isotherms (3 samples x 25, 40, 60, 80, 100 C), 11 markers each; highest-pressure marker of each digitized (archives fig8{a,b,c}_*.json); 11 of the 15 matched to text values (rows carry the text value, digitized point in notes; tool check passed for all 11, max deviation 0.9 %); G-700 60 C, G-700 80 C, G-900 60 C, G-900 80 C have no text value -> digitized rows M13, M14, M18, M19.
- main p. 9, Fig. 12: G-800 multi-cycle isotherms at 25 C (1, 3, 5, 10 cycles); highest-pressure marker of the 10-cycle series digitized -> row M6.
- SI pp. 5-6, Fig. S1a-d: G-800 multi-cycle isotherms at 40, 60, 80, 100 C; coincident end-marker blob digitized and assigned to the top-drawn 10-cycle series -> rows M7-M10 (confidence 2, low-resolution raster).

## Calibration notes

- Fig. 8a: x 0/50 at px 177/600, check 20 at 346; y 0/10 at px 1246/957.5, check 4 at 1130. Fig. 8b: x 670/1098, check 841; y 0/14 at 1059/745, check 6 at 925. Fig. 8c: x 666/1091, check 836; y 0/8 at 1433/1155, check 4 at 1294. Residuals <= 0.52 %.
- Fig. 12: x 0/50 at 150/569, check 20 at 317; y 0/16 at 1258/938, check 8 at 1097.5. Residuals <= 0.36 %.
- Fig. S1a-d (SI pp. 5-6): low-resolution, pixelated raster (one source pixel ~4 page px); tick positions irregular by up to ~3 px, so third-tick residuals are 0.2-1.6 % (S1a y-axis 1.58 %). Tick labels are consistent; no axis was rejected.
- Marker isolation: Fig. 8 tolerance 90, opening 2 px, ROI restricted to P > 42 bar (excludes legend and panel labels), one marker per series found = one counted. Fig. 12 colour #006900 tol 60, opening 2 px, ROI P > 42 bar and above the inset. Fig. S1 colour #255640 tol 60, opening 3 px, ROI around the end marker (wider ROIs or larger tolerances picked up line segments and panel labels).
- Archives of the 4 Fig. 8 series without a text value, of Fig. 12 and of Fig. S1a-d keep status "unchecked": the paper states no value for those series to check against.

## Values seen but not extracted

- Fig. 8a-c: all points other than the highest-pressure point of each of the 15 isotherms (10 per isotherm, 150 in total) - isotherms at 25-100 C, not 77 K (only highest-pressure point extracted).
- Fig. 12: highest-pressure markers of the 1-, 3- and 5-cycle isotherms - hidden under the 10-cycle marker (only thin red/blue rims visible), could not be separated; all lower-pressure points - not 77 K.
- Fig. S1a-d: highest-pressure markers of the 1-, 3- and 5-cycle isotherms at 40, 60, 80, 100 C - coincide with the 10-cycle marker in one blurred blob, could not be separated (S1d shows a dark/red rim above the green marker, not separable); all lower-pressure points - not 77 K.
- Fig. 12 and Fig. S1a-d insets: bar charts of adsorption capacity against cycle number (1, 3, 5, 10) - cycling bar charts, not digitized; per-cycle capacities are not given in text or tables. Text: "The highest standard deviation for H2 uptake in the different cycles was 5 %" (sec. 3.3) - relative uncertainty, recorded in notes of G-800 rows, not in uncertainty_wt_pct.
- Fig. 11a-e: same G-800 experimental isotherms as Fig. 8b (sec. 3.3: "Experimental adsorption curves for G-800, G-700 and G-900 shown in Fig. 8a-c, were modelled") with nine model-fit lines - no separate rows; model curves not digitized (fits, not measurements). Text refers to the fits as "Fig. 10" and to the 25 C cycle test as "Fig. 11"; the figures are Fig. 11 and Fig. 12.
- Fig. 10a-d: H2 uptake at 45 bar and 25-100 C against S_BET, V_tot, N2 micropore volume and CO2 micropore volume (with R2 of linear fits) - not an isotherm, not digitized. Values it shows that text/tables do not give: G-700 at 60 and 80 C and G-900 at 60 and 80 C (45 bar); these were taken from Fig. 8a/8c instead (rows M13, M14, M18, M19).
- Table S2 (SI pp. 3-4): fitted model parameters, not measured uptakes (no pressure; several are physically meaningless, e.g. G-900 25 C Sips qm 5376.339 mmol/g, outside the schema range). Capacity-type parameters seen, mmol/g, order 25/40/60/80/100 C:
  - Langmuir qm: G-700 26.068/91.606/42.732/35.715/15.278; G-800 83.100/17.949/16.430/16.274/11.759; G-900 22.279/47.609/44.396/36.735/29.450.
  - Toth qm: G-700 27.507/11.058/11.337/159.291/70.854; G-800 19.481/26.848/40.971/179.187/31.979; G-900 96.494/147.914/183.253/417.902/18.829.
  - Hill qH (unit printed as "bar" in Table 2): G-700 25.620/54.754/17.913/51.920/1608.825; G-800 31.541/21.751/22.662/38.001/17.131; G-900 4396.941/60.350/101.525/62.433/23.590.
  - Koble-Corrigan A: G-700 0.358/0.194/0.105/0.152/0.194; G-800 0.212/0.547/0.281/0.286/0.194; G-900 0.630/0.171/0.126/0.083/0.069.
  - Sips qm: G-700 25.621/55.036/17.906/51.958/762.112; G-800 31.503/21.748/22.653/38.127/17.082; G-900 5376.339/60.232/107.789/68.926/23.634.
  - Radke-Prausnitz qm: G-700 21.882/37.956/53.444/6.906/0.141; G-800 47.048/7.918/4.086/0.829/2.828; G-900 0.476/11.876/1.3732/2.686/36.594.
  - Other Table S2 parameters (K, n, 1/n, a, beta, B, e) are not uptake values.
- Table S1 (SI p. 2): SSE of the nine model fits - not uptake values.
- Table 1 (main p. 2): elemental analysis of the precursor (fern leaves): C 78.89 wt%, H 6.45 %, N 2.83 %, O 11.83 % - precursor, not the ACs; no composition of the ACs is given.
- Table 2 (main p. 3): model equations - no values.
- Fig. 1 (N2 isotherms), Fig. 2 (N2 PSD), Fig. 3 (CO2 PSD), Fig. 4 (XRD, peaks at 2theta ~21, 43, 80 deg; no d-spacing given), Fig. 5 (FT-IR), Fig. 6 (Raman, ID/IG = 1.19 G-700, 1.26 G-800, 1.65 G-900), Fig. 7 (SEM/TEM), Fig. 9 (schematic) - characterization, no H2 uptake.
- Fig. 13 and sec. 3.4: isosteric heat 5.7-7.7 kJ/mol for coverage 0.10-0.35 (Qst order G-800 > G-700 > G-900) - not an uptake value.
- Text ranges "1234-1591 m2/g", "0.57-0.90 cm3/g", "0.34-0.62 cm3/g", "0.52 to 0.82 cm3/g" (sec. 3.1, Conclusions) - summaries of Table 3.
- No non-carbon sorbent is measured. No value is said to have been reported before.
