# HYC-0110 extraction log (agent A)

Rows written: 23 (rows.csv). Samples are numbered by first appearance in the paper among samples that have a row.

## Extracted from

- Table 1 (main p. 13907), PEEK rows: PEEK-CO2-9-80 (S1), PEEK-CO2-9-26 (S2), PEEK-ST-9-70 (S3), PEEK-CO2-9-1 (S4), PEEK-ST-9-20 (S5), PEEK-ST-9-47 (S6), PEEK-CO2-9-5 (S10): excess H2 uptake at 77 K and 2 bar (footnote b), BET SA, volumetric capacity, cumulative pore volume. One row each (M1, M13-M17, M21).
- Table 1 and main text p. 13906, PEEK-CO2-9-80 at 77 K and 20 bar: "~5 wt %" and "35 g/L" (M2), carries I1 because the text cites Figure 7. Not merged with the digitized point at 19.5958 bar (|20 - 19.5958| = 0.404 bar is just outside the 0.4 bar window); both rows kept, cross-referenced in notes.
- Table 1, comparison materials, previously reported by other groups and cited by reference number (kept as rows under the "values reported before" rule, `previously reported:` in notes, `duplicate_of` empty): AX-21 (ref. 14, M18), B/C (ref. 12, M20), CMK-1 (ref. 13, M22), Corncob (ref. 15, M23). They are not measurements of this paper; if the reconciler judges the rule does not cover them, drop M18, M20, M22, M23. Class `other`, synthesis `unknown` because the paper does not describe them; laboratory defaults to the corresponding author's group (Liu group, Duke University) because no laboratory is named.
- Main text p. 13906-13907, "upon compression of 15 t ... ~1 g/mL ... H2 volumetric uptake of ~50 g/L" (M19, sample S8 "(unlabelled 1)"): volumetric-only row, `value_kind = unclear`, because the authors compute it from the 5 wt % value and describe no measurement on compressed material. T and P taken from the preceding sentence. Drop if the reconciler treats it as not a measurement.
- Figure 7B (Caltech, 77 K, "Gibbs Excess(Caltech, 77K)"), 7 markers digitized (M3-M9), archive fig7B_caltech_77K_gibbs_excess.json. All Caltech markers lie below 31.1 bar, so panel B (0-50 bar) holds the whole series; panel A shows the same curve and was used to confirm no red marker lies beyond ~31 bar.
- Figure 7A (NREL, 75.6 K, outside 76.0-79.0 K): highest-pressure marker of each of the three curves: Eng. Excess (M10, I2), Gibbs Excess (M11, I3), Gibbs Excess sk=2.1g/cc (M12, I4). Archives fig7A_nrel_75.6K_*_last_point.json.
- SI main file (si1.txt, pages si1-1 to si1-4): methods only (degassing 300 C, instruments, BET method, burn-off naming); no uptake values.
- Abstract and Conclusions repeat "~5 wt % and 35 g/L at 77 K and 20 bar" and "3.7 wt %"; same values as M2 and M1, no extra rows.

## Digitization notes (Figure 7)

- Calibration (page image main-6.png, pixel indices): panel B x 0 at 164.5, 50 at 553 (check tick 20 at 319.5, 0.26% error); y 0 at 1340.5, 6 at 1039.5 (check tick 4 at 1139.5, 0.17%). Panel A x 0 at 164.5, 150 at 553 (check tick 100 at 423.5); y 0 at 927, 6 at 623.5 (check tick 4 at 724.5). Tick pixels found from pixel rows/columns of the page image.
- The tool's `--mode markers` finds only pixel fragments of hollow (unfilled) squares (52 rejected groups, 44 fragments at open-px 0/1, 8 at open-px 2), so it cannot be applied to the page image directly. A derived image was made in the work directory: pixels with red dominance (R - max(G,B) > 0.12 of full scale) were closed (3x3), hole-filled and opened (3x3); only blobs of single-marker size (about 9x9 px) were painted #ec1b24 (work/B_caltech_singles.png) and passed to `digitize_figure.py extract --mode markers`. Same procedure for the last NREL markers (work/A_end_{black,green,blue}.png, ROI limited to the last marker, filled in the series colour).
- Tool check on the Caltech archive: stated "~5 wt % at 20 bar" vs series interpolated at 20 bar 4.86996 wt% (2.6%, pass at 5%). The three NREL archives are `unchecked`: the paper states no value at 147 bar for them.
- Marker count does NOT match the plot for the Caltech series: 7 extracted of about 40 (40 is an estimate from edge-coverage template matching, not a firm count). Not separable: the vertical stack of overlapping squares at p below ~0.5 bar (uptake below ~2.2 wt%, about 10-15 markers), the contiguous ribbon of overlapping squares from ~0.5 to ~14 bar (about 20 markers; merged blobs of 17-29 px width), the two markers merged in the blob at ~15.5-17.6 bar, and the NREL and Caltech markers that overlap each other in 14-31 bar. The marker at 22.2 bar has a thicker outline (possibly two near-coincident markers) and was extracted as one. No marker below 4.3 bar was extracted, so there is no digitized point near 2 bar.
- NREL series isotherm_point_count 27 is an estimate (23 clearly visible markers at 14-148 bar on the Eng. Excess curve, plus overlapping ones below 14 bar).
- Observation, not coded: the Table 1 value 3.7 wt% "at 2 bar" is numerically close to the digitized Caltech point at 4.3168 bar (3.7367 wt%). The 77 K curve in Fig. 7B appears lower than 3.7 wt% at 2 bar (no digitized point there to test). Table 1 value stored as printed.

## Seen but not extracted

- Figure 2 (BET area vs burn-off): not an isotherm, no uptake values.
- Figure 3 (differential pore volumes) and Figure 4 (cumulative pore volume vs BET area): characterization, not uptake. Table 1 values stored. Fig. 4 appears to plot the CO2 points near 1000 and near 3100 m2/g lower than Table 1's 0.63 and 1.7 cm3/g (not digitized; Table 1 used).
- Figure 5 (NMR shift vs log pressure, 100 K): NMR shifts, not an uptake.
- Figure 6 (uptake vs BET at 77 K and 2 bar): not an isotherm, not digitized for rows. Markers measured with the tool only for this log (work/fig6_*.json, not rows): CO2 squares at BET/wt% about (526, 1.60), (1025, 2.216), (1672, 2.598), (1979, 2.760), (2327, 2.826), plus the 3103 point (Table 1: 3.7); steam triangles at about (981, 2.080), (1203, 2.295), (1295, 2.408), (1650, 2.511), (1957, 3.020), (2366, 2.956), (2801, 2.937). Matches with Table 1: CO2-9-1, CO2-9-26, CO2-9-80, ST-9-47, ST-9-20, ST-9-70. Values shown in the figure but given in neither table nor text (samples unlabelled in the figure): CO2 at about 1672, 1979 and 2327 m2/g; steam at about 981, 1650, 2366 and 2801 m2/g. Table 1's PEEK-CO2-9-5 (700 m2/g, 2.0 wt%) has no marker in Fig. 6.
- Figure 7A/7B, other markers: NREL curves at 75.6 K below their highest-pressure point (outside 77 K, so only the last point is extracted); Caltech markers listed above as not separable; panel B repeats the data of panel A for 0-50 bar (no separate rows).
- SI Figure S1 (XPS of PEEK-CO2-9-80 and PEEK-ST-9-91) and Figure S2 (NMR of PEEK-CO2-9-80 and PEEK-ST-9-95): no uptake values.
- Samples with characterization but no H2 uptake value (no row): PEEK-CO2-9-59 (about 2000 m2/g, text and Figs. 3-5), PEEK-ST-9-35 (about 1000 m2/g, text and Figs. 3, 5), PEEK-CO2-9-85 (named with PEEK-CO2-9-80 as having the largest cumulative pore volumes, text p. 13905-13906; the abstract's 3275 m2/g sample is not identified in the text), PEEK-ST-9-91 and PEEK-ST-9-95 (about 3000 m2/g, "not analyzed beyond surface area measurements").
- Text: "graphitic slit pore materials typically have excess adsorption capacities of ~1 wt % for every 500 m2/g" (ref. 10 rule of thumb, p. 13903): not a measurement.
- Text p. 13906: "PEEK-CO2-9-80 has a larger H2 gravimetric uptake compared with AX-21 at the same temperature and pressure": no new value.
- Table 1 volumetric capacity of PEEK-ST-9-70 (18 g/L) is 6.0 g/mL times its 3.0 wt %, whereas the other PEEK rows (11, 14, 15, 16, 17, 26 g/L) correspond to ~0.7 g/mL; stored as printed.

## Coding decisions worth review

- `measurement_method`: `volumetric_sieverts` for Table 1 (SI: "Sieverts device specially built" at NREL, generic, `instrument_identified = false`); `unknown` for the Caltech ("Micromeritics ASAP", no model, technique not named) and NREL over-2-bar ("Hy-Energy PCTPro-2000", technique not named, `instrument_identified = true`) isotherms and for the comparison materials.
- `basis_stated = false` everywhere: legends name "Eng. Excess" and "Gibbs Excess" without defining them; two corrections of excess are not two of excess/absolute/total. `basis_inferred = excess` (called excess by name), except M19.
- `replicates_reported = true` for Table 1 rows whose marker in Fig. 6 carries an error bar (magnitude not printed), false for PEEK-CO2-9-5 (no marker) and the comparison rows; true for the Caltech rows (Fig. 7 caption: estimated error +/-0.1%, printed unit "%", stored as 0.1 in `uncertainty_wt_pct`).
- `volumetric_capacity_basis`: `packing_volume` for PEEK-CO2-9-80 (text: "unaltered porous carbon density of ~0.7 g/mL"), `other` for the other PEEK rows (basis not stated).
- I4 row carries `skeletal_density_g_cm3 = 2.1` from the legend "sk=2.1g/cc" (abbreviation not defined in the text).
- Measuring laboratory: 2-bar Table 1 values and NREL isotherms assigned to NREL (SI: made at NREL; first-listed NREL co-author O'Neill); Caltech isotherm to Caltech (first-listed Caltech co-author Stadie).
