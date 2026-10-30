# HYC-0095 extraction log (extractor A, agent A (claude-sonnet-5-5), 2026-10-29)

Rows written: 119 (`rows.csv`). `validate_row_detail.py --errors-only` reports 0 rows with errors. Page numbers are the PDF page footers ("Page N of 27"). Sample ids are numbered in order of first appearance in `rows.csv`.

## Sources extracted from

- Summary, p.2 (text): ~5.1 wt% excess at 40 bar and 77 K -> M1 (approximate). "these materials" is not a named sample; assigned to PEEK-CO2-9-80 (p.24 states the same batch went to NREL, CalTech and SwRI), confidence 3.
- Achievements 3c, p.7 (text): >3 wt.% at 77 K and 2 bar -> M2 (lower bound); >5 wt% at 77 K and 40 bar -> M3 (lower bound). Same sample assignment as M1.
- Achievements 3d, p.7 (text): H2-NMR, >6% at 10 MPa (100 bar), 120 K -> M4 (lower bound, UNC-CH, sample not identified). The methods paragraph on p.17 says the NMR was run at RT (~290 K) and 100 K; the 120 K is as printed in 3d and is not reconciled.
- Table 2, p.13 ("Detailed Characterization of different SWNTs at 77K and 2bar (From NREL)"): 17 rows, M5-M21. RT & 2 bar x4 (T unstated, T left empty), 77 K & 2 bar x5, TPD x3 (0.39 total, ~0.24 Pd, ~0.15 Chemi.; 500 torr = 0.66661 bar, 77 K, `measurement_mode` TPD, `isotherm_branch` not_applicable), after 800 °C degas x2, after 800 °C x1, after H2SO4/CO2/HCl/CO2 treatment x2. BET areas of the matching state are on each row.
- Table 3, p.22, and the text under it: 13 rows, M22-M34. PEEK-CO2-9-1, B/C, PEEK-CO2-9-5, CMK-1, PEEK-CO2-9-26, PEEK-ST-9-47, PEEK-ST-9-20, PEEK-ST-9-70, AX-21, PEEK-CO2-9-80 at 2 bar (M31), PEEK-CO2-9-80 at 20 bar (M32, carries I1 because the text cites Figure 19), Corncob, compressed PEEK-CO2-9-80 (M34, volumetric-only ~50 g/L at 77 K, 20 bar, no wt% given). Volumetric values sit on the gravimetric row of the same sample, T and P. B/C, CMK-1, AX-21 and Corncob carry `previously reported: <ref as printed>`. Table 3 uptakes are 2 bar and 77 K by footnote, except where a pressure is printed.
- Figure 19B, p.23 (CalTech, 77 K, Gibbs Excess): 47 markers digitized -> M35-M81, I1, archive `fig19B_caltech_77K.json`, ±0.1 wt% stated in the caption.
- Figure 19A, p.23 (NREL, 75.6 K): highest-pressure marker of each of two Gibbs-excess series only -> M82 (I2, green "Gibbs Excess", 147.27 bar) and M83 (I3, black "Gibbs Excess sk=2.1 g/cc"), archives `fig19A_nrel_gibbs_75p6K.json` and `fig19A_nrel_gibbs_sk2p1_75p6K.json`. 75.6 K is outside 76.0-79.0 K, so no other points are extracted.
- Figure 20, p.24 (SwRI, 77 K): left panel Run 1 adsorb 17 rows (M84-M100, I4), Run 2 adsorb 12 rows (M101-M112, I5, adsorption) and Run 2 desorb 7 rows (M113-M119, I5, desorption). The right-panel absolute volumetric capacity of Run 2 adsorb is attached to the 12 Run 2 adsorb rows (digitized right-panel pressures agree with the left within ~0.05 bar); at 70 bar the printed "~30 g/L" (p.25) is used.

## Values seen and not extracted

- Fig 20 left, Run 1 adsorb, first marker at the origin (digitized -0.043 bar, 0.015 wt%): no row. The pressure is at the axis zero (resolution ~0.07 bar per pixel), the validator rejects pressure 0, and a positive pressure would be invented. The marker is counted in `isotherm_point_count` (18) for I4.
- Fig 19A NREL "Eng. Excess" (blue, 75.6 K) series: no row. Its archive FAILED the check (4.448 vs 5.1 wt% at 40 bar, 12.8%) and was discarded; it is kept only in the work directory (`fig19A_nrel_eng_75p6K_UNCHECKED.json`). The "~5.1 wt% at 40 bar" statement refers to the Gibbs-excess curves; the same calibration passes on both Gibbs-excess series (green 2.7%, black 0.9%).
- Fig 19A NREL, all points below the highest pressure of each series (75.6 K, not 77 K), and the NREL point counts are approximate (about 27 per series; low-pressure markers of the three series overlap).
- Fig 19B CalTech: markers overlap heavily at p <= 5 bar and at p ~ 0 bar, so the 47 extracted markers are an approximate count and the low-pressure rows have confidence 2.
- Fig 20 left Run 1: 5 markers are partly hidden under Run 2 squares (placed from their visible arcs at about 0.25, 0.48, 2.34, 6.82 and 22.7 bar); confidence 3.
- Fig 20 right panel Run 1 adsorb (16 of 18 markers visible, 2 hidden under the first red square) and Run 2 desorb (7): not attached to rows and not archived. There is no paper-stated volumetric value inside their ranges to run `check` against.
- Fig 20 left "Model Fit" and "95% CI" lines: fitted curves, not measurements; not digitized.
- Restatements of values already extracted, not separate rows: ">5 wt% at 77K" (Summary, p.2); ">35 g/L" and "bulk densities greater than 0.7 g/ml" (Summary, p.2; Achievements, p.7); "~5 wt.%" without a pressure (p.23 text and Fig 19 caption); "up to ~5 wt% and 35 g/L" (p.24); ">5%" (Conclusion, p.25); "~35 g/L" (p.22, p.25); "~30 g/L at 77K and 70bar" (p.25, merged onto the 70 bar Run 2 row as the volumetric value); "3.7 wt% at 77K and 2 bar" (p.21 text, Fig 18 caption) = Table 3 value in M31.
- Table 2 "Modified Chahine Criterion (wt% per 500 m2/g)" rows (0.56, 0.64, 1.08, 0.48; 0.67, 0.75, 1.35, 0.67): ratios computed from the table's own uptakes and BET areas, not uptake values. 0.75 = 1.61/(1074/500) supports pairing the "after 800 °C" uptake with the "after 800 °C CO2" BET (area_same_sample `unclear` on M19).
- Table 2 "after 800 °C CO2" BET 75 m2/g for the 1-2 nm DWNT: no uptake value for that state, no row.
- Chahine rule of thumb "~1 wt% for every 500 m2/g" (p.18): general statement, not a measurement.
- Figures 16, 17 and 18: not isotherms, not digitized. Fig 18 plots uptake against BET area (77 K, 2 bar, error bars) and shows about 13 points that no table or text gives: CO2 series 524, 1027, ~1690, ~1980, ~2330 and 3103 m2/g; steam series ~980, ~1210, ~1300, ~1670, ~1960, ~2370 and ~2800 m2/g. No numeric uptakes are printed for them.
- Table 3 caption/text BET for PEEK-CO2-9-80: Fig 4 caption (p.6) prints 3013 m2/g, elsewhere 3103 m2/g; 3103 is used.
- P123 and P103 mesoporous carbon pore sizes (2 nm / 1.18 nm; 1.3 / 1.2 nm) and P84 area (<250 m2/g): characterization without H2 uptake, no rows. PEEK-CO2-9-59 and PEEK-ST-9-35 are named without an uptake value, no rows.
- "Higher binding energy (8.1 kJ/mol)" (p.7): not an uptake value.
- DOE 2015 system goal (5.5 wt%, 0.040 kg H2/L) (p.3): target, not a measurement.
- Conclusion (p.25): "Measurements from 4 different labs: NREL, NIST, UNC and SwRI all confirmed the high uptake". Only NREL, CalTech, UNC-CH and SwRI values are in the paper; NIST measurements are not shown. The statement is a consensus claim, not a value.
- Table 3 "3.7 wt% at 2 bar" for PEEK-CO2-9-80 is not merged with a plotted CalTech point: the nearest marker is 2.07 bar, 3.13 wt% (0.07 bar away, beyond max(2%, 0.02 bar)). The Table 3 "~5 at 20 bar" is likewise not merged with the CalTech marker at 19.55 bar, 4.854 wt% (0.45 bar away, beyond 0.4 bar). Both are separate rows.
- `reference_temperature_k` on the three TPD rows (M14-M16) is left empty: the paper gives no desorption endpoint temperature. The validator raises no error.
- Table 2 label "0.39 wt% total" is stored with 500 torr as the pressure although the pressure at 77 K is not stated; the notes say so.

## Digitization checks (all archives status `passed`)

- `fig19B_caltech_77K.json`: 47 markers. Check at 20 bar against 5 wt% (stated "~5 wt.% at 77K and 20 bar"): tool value 4.864, 2.7%.
- `fig20L_run1_adsorb_77K.json`: 18 markers (17 rows, see above). Check at 20 bar against 5 wt% (same statement for the same sample): 4.948, 1.0%.
- `fig20L_run2_adsorb_77K.json`: 12 markers. Check at 20 bar against 5 wt%: 4.839, 3.2%.
- `fig20L_run2_desorb_77K.json`: 7 markers. WEAK check: the paper states only "~5 wt.%" / ">5%" with no pressure and the series range starts at 31 bar, so the check is at 64 bar against 5 wt% with a 10% tolerance (7.1%). It confirms the axis scale, not the individual points.
- `fig20R_run2_adsorb_77K.json`: 12 markers. Check at 70 bar against 30 g/L (stated "~30g/L at 77K and 70bar"): 29.28, 2.4%.
- `fig19A_nrel_gibbs_75p6K.json` (green) and `fig19A_nrel_gibbs_sk2p1_75p6K.json` (black): 19 markers each at p >= 30 bar (the NREL curves have about 27 markers in all; the archived ones are the markers I could separate above 30 bar). Check at 40 bar against 5.1 wt% ("~5.1 wt% ... at 40 bar and 77K"): 4.963 (2.7%) and 5.052 (0.9%). The statement is for 77 K and the curves are 75.6 K, so these checks confirm the axis scale only.
- Several checks use a value stated for the same sample in the Table 3 text or the Summary, not a value printed at that exact figure point.

Calibrations (enlarged-image pixels, third tick verified in each): Fig 19B x 65.5 -> 0 and 1409.5 -> 50 (verify 601.5 = 20), y 1093.5 -> 0 and 29.5 -> 6 (verify 209.5 = 5); Fig 19A x 65.5 -> 0 and 1409.5 -> 150 (verify 961.5 = 100), y 1113.5 -> 0 and 49.5 -> 6 (verify 581.5 = 3); Fig 20 left x 157.5 -> 0 and 1469.5 -> 90 (verify 741.5 = 40), y 1037.5 -> -1 and 27.5 -> 7 (verify 405.5 = 4); Fig 20 right x 169.5 -> 0 and 1395.5 -> 80 (verify 781.5 = 40), y 885.5 -> 0 and 37.5 -> 35 (verify 401.5 = 20).

## Figure pipeline (disclosure)

The page images were enlarged 4x (BICUBIC) with the legend masked. Gridline and tick centroids were found for the calibration. Markers were located by chroma ring-template matching pursuit (`mp2.py`) followed by local refinement (`refine.py`), and small solid dots (radius 2.2 px) were painted into a white image at the located centres. `digitize_figure.py extract --mode markers` was then run on that dot image with the calibration in enlarged-image pixels (`--open-px 0 --marker-min-px 4 --marker-max-px 400`). Markers hidden under other markers were placed from their visible arcs or, for the right panel, from the paired left-panel pressure. The NREL green y-values were refined with a vertical-centroid method and three low-pressure green markers hidden under the black curve were set by hand (those low-pressure markers are not archived or extracted). The helper scripts are in the work directory. Filled and hollow red squares in Fig 20 were separated by red-chroma bounding boxes (12 filled = Run 2 adsorb, 7 hollow = Run 2 desorb); the composite square near 47 bar in the right panel was split the same way.

## Coding notes

- Laboratory ids: `NREL (HYC-0095)`, `CalTech (HYC-0095)`, `SwRI (HYC-0095)`, `UNC-CH (HYC-0095)` where the paper names the lab; `Liu group, Duke University` where it does not (Summary and Achievements text, Table 3 PEEK rows, which are not attributed to a lab in the paper).
- Basis: SwRI isotherms `basis_stated` = true on the caption "Excess hydrogen uptake and absolute Volumetric Capacity" (two bases side by side), inferred excess. CalTech, NREL and Table 3: stated false, inferred excess (named, not defined). Table 2: Sieverts default, `uptake_type` unspecified. TPD and NMR: unknown. `wt_pct_convention` is `unknown` throughout (the SwRI axis reads "wt.% H"; no convention is defined).
- Instruments: NREL Hy-Energy PCTPro-2000 for uptakes over 2 bar (identified); NREL 2 bar device, CalTech "custom Sieverts" and SwRI "gravimetric technique" are not manufacturer + model, so `instrument_identified` is false.
- Degas 300 °C on PEEK rows from "All samples were degassed at 300C" (not set for SwRI); 800 °C on the Table 2 "after 800 °C degas" rows.
- The SwRI skeletal density 3.02 g/cc (He-derived estimate, p.25) is on the SwRI rows; NREL black series carries 2.1 g/cc from its legend. SwRI volumetric capacities are absolute (include pore gas), `volumetric_capacity_basis` = other, `volumetric_capacity_includes_compressed_gas` = true. Table 3 g/L values for PEEK-CO2-9-80 use basis `packing_volume` with 0.7 g/ml; the other PEEK g/L values have basis `other` (density not stated for them) and exclude compressed gas.
- `uptake_type` unspecified on M5-M21 and M34 raises validator warnings only.
