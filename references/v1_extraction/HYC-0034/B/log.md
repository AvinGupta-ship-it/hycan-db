# HYC-0034 extraction log (agent B)

Wang et al. 2016, Int. J. Hydrogen Energy 41, 8489-8497. Inputs: page images main-1 to main-9 (pp. 8489-8497), no supplementary file. 403 rows.

## Sources extracted

- Table 1 (p. 8493, main-5): H2 uptake (wt%) at 77 K and 1 bar, and in parentheses at 77 K and 20 bar, for PC-2-600, PC-2-700, PC-2-800, PC-4-600, PC-4-700, PC-4-800 and PC; S_BET with micropore surface area in parentheses, V_p with micropore volume in parentheses, NLDFT PSD maxima, N (wt%) with N/C ratio in parentheses. All 14 uptake values are rows (13 merged with a plotted point, 1 separate, see Fig. 6 PC-4-800).
- Experimental (pp. 8490-8491): samples synthesis (chitosan hydrothermal carbonization 220 °C 12 h; KOH/HC 2 or 4; 600-800 °C under Ar, 3 °C/min, 1 h; HCl wash; 105 °C drying; PC "prepared via the same method"), characterization (Autosorb-1 N2 at 77 K, BET 0.01-0.2, total pore volume at P/P0 ca. 0.995, t-plot micropore area and volume, NLDFT slit PSD, Vario III elemental analyzer), hydrogen storage (Autosorb-1 volumetric 0-1 bar 77 K; PCI unit from Advanced Materials Corporation 0-20 bar 77 K; H2 99.999%).
- XPS passage (p. 8492): N species of PC-2-600, PC-2-700, PC-2-800 recorded in functional_groups.
- Fig. 4 (p. 8494, main-6): 77 K H2 isotherms 0-760 mmHg, 7 series, digitized (markers).
- Fig. 6 (p. 8494, main-6): 77 K H2 isotherms 0-20 bar, 7 series, digitized (markers).
- Text p. 8492-8494 linking Table 1 to the figures: "Hydrogen sorption isotherms ... from 0 to 1 bar at 77 K are shown in Fig. 4 ... The hydrogen storage capacity ... is listed in Table 1" and "High-pressure hydrogen uptakes ... shown in Fig. 6 and the hydrogen storage capacity of porous carbons is given in Table 1". Read as the paper saying the Table 1 values come from those isotherms.

## Sample numbering (first appearance)

S1 PC-2-800 (abstract), S2 PC and S3 PC-2-600 (Experimental, same sentence, PC first), S4 PC-2-700 (Fig. 1 caption), S5 PC-4-800 (p. 8492 text), S6 PC-4-600 and S7 PC-4-700 (Fig. 2 legend). HC (hydrochar) has no H2 uptake and gets no sample number.

## Digitization method (both figures)

- Work image: copy of main-6.png with the two legend boxes painted white (Fig. 4 legend x 449-562, y 294-433; Fig. 6 legend x 989-1100, y 286-424, page pixels), saved as work/main-6_legends_masked.png; this is the archived source image. Nothing else changed; pixel coordinates are page coordinates.
- Fig. 4 calibration (tick centroids measured from pixel columns/rows): x 0 mmHg = 176.22 px, 800 = 570.67, check 400 = 373.44 (error 0.002%); y 0.0 wt% = 437.75, 3.0 = 147.11, check 1.5 = 292.08 (error 0.25%).
- Fig. 6 calibration: x 0 bar = 707.57, 20 = 1110.82, check 8 = 868.57 (0.19%); y 0 wt% = 441.56, 7 = 151.43, check 4 = 275.54 (0.14%).
- `digitize_figure.py check` passed for all 14 archives: Fig. 4 at 750.06 mmHg (1 bar) against the Table 1 1-bar values; Fig. 6 at each series' highest digitized pressure against the Table 1 20-bar values (x = 20 itself is outside every extracted range).
- Fig. 4 pressures converted mmHg to bar with 0.00133322. Table-1 merges: the last plotted point of each Fig. 4 series lies at 755-761 mmHg (1.008-1.015 bar), within 2% of 1 bar; no other point qualifies. Fig. 6 merges use the visible marker closest to 20 bar within 2% (0.4 bar).
- Branches: the paper says the 0-1 bar isotherms are completely reversible, and many Fig. 4 markers occur in near-coincident pairs (probably adsorption and desorption points at nearly equal pressure), but the plot does not identify which is which; all points are coded adsorption. Fig. 6 shows a single monotonic branch per sample.
- extraction_confidence: 5 for Table 1 values, 3 for Fig. 6 points, 2 for Fig. 4 points (150 dpi image, heavy marker overlap).

## Fig. 4 series (archive, settings, decisions)

Tool point numbers below refer to the archive's `series` order. "Blob of k" = one tool point covering k overlapping markers that could not be separated (one row, value = blob centroid). Markers stacked at the bottom-left under the PC diamonds (P below about 15 mmHg, uptake below about 0.3 wt%) are mostly hidden; markers of other series hidden there could not be counted or separated, so the Fig. 4 isotherm_point_count values are lower bounds.

- PC-2-600 (black squares), fig4_pc2600.json, tol 60, open 1, min 3: 30 tool points; merged as fragments of one partly hidden square: 8+9, 18+19, 20+21, 22+23 (squares under PC diamonds and olive triangles); blobs of 2: points 1, 13, 14. 26 rows; 29 markers counted. Several squares above 450 mmHg are almost entirely covered by PC diamonds; their positions rest on small fragments.
- PC-4-600 (red circles), fig4_pc4600.json, tol 60, open 2, min 3: 26 tool points; blobs of 2: points 9-19 and 23. 26 rows; 40 markers counted. Not extracted (could not be separated at these settings): a circle at about 20 mmHg under the PC diamond pile and a circle at about 125-150 mmHg visible only as 3-pixel fragments around an olive triangle (both detected only as fragments with opening 1, which in turn merged the two touching circles at 705 and 721 mmHg).
- PC-2-700 (blue up-triangles), fig4_pc2700.json, tol 60, open 1, min 2: 28 tool points; merged fragments: 10+11 (triangle under magenta, about 225 mmHg), 12+13 (about 264 mmHg; may be two markers); blob of 3: point 6 (about 97-116 mmHg); blobs of 2: points 14-21, 25. 26 rows; 37 markers counted.
- PC-4-700 (dark-cyan down-triangles), fig4_pc4700.json, tol 40, open 3, min 6: 26 tool points; blob of 3: point 5 (about 97-116 mmHg); blobs of 2: points 2, 12-18, 23; points 10 and 11 may also hold two nearly coincident markers (counted as one). 26 rows; 37 markers counted.
- PC-2-800 (magenta left-triangles), fig4_pc2800.json, tol 60, open 2, min 3: 25 tool points; blobs of 2: points 1, 9-18, 21, 22; points 6, 19, 20 are slightly oversized and may hold two (counted as one); magenta fragments at the edge of the low-pressure pile were not counted. 25 rows; 38 markers counted.
- PC-4-800 (olive right-triangles), fig4_pc4800.json, tol 60, open 2, min 3: 28 tool points; blob of 3: point 7; blobs of 2: points 6, 9, 10, 11, 20, 22, 23, 24, 25. Points 1, 2, 13, 15, 16 are small fragments of mostly hidden triangles (kept as rows). 28 rows; 39 markers counted.
- PC (purple diamonds), fig4_pc.json, tol 60, open 2, min 3: 25 tool points; point 1 (n = 183 px, centroid 4.3 mmHg, 0.146 wt%) is a vertical stack of about 5 diamonds at about 0-8 mmHg (row-width minima suggest centres near 0.04, 0.11, 0.17, 0.21, 0.26 wt%) that no opening or tolerance separated without losing other markers; excluded from the rows as not one marker. 24 rows; 29 markers counted.

## Fig. 6 series

- PC-2-600 (black squares), fig6_pc2600.json, tol 50, open 1, min 2, region to x 1110 (frame excluded): 30 points, all rows. The connecting line continues from the last visible square (19.72 bar) to the right frame, so one further measured point at or beyond 20 bar is clipped and invisible; counted (31 markers) but not digitizable. Table 1 4.23 wt% merged with the 19.72 bar marker under the 2% rule; this choice is uncertain.
- PC-4-600 (red circles), fig6_pc4600.json, tol 50, open 1, min 2: 41 tool points; 8 circles split into two fragments by the PC line or diamonds merged: 2+3, 14+15, 18+19, 23+24, 25+26, 27+28, 31+32, 34+35. 33 rows; 33 markers. Point 41 is a half circle clipped at the frame (19.89 bar), merged with Table 1 4.66.
- PC-2-700 (blue up-triangles), fig6_pc2700.json, tol 50, open 1, min 2: 33 points, all rows; point 16 is a triangle mostly hidden by an olive triangle; point 33 is clipped at the frame (19.93 bar), merged with Table 1 5.63.
- PC-4-700 (dark-cyan down-triangles), fig6_pc4700.json, tol 50, open 2, min 3: 36 tool points; 18+19 merged (one triangle split by a line). 35 rows. Point 36 is a 4-pixel fragment at the frame (19.98 bar, 5.261 wt%; centroid of the triangle's top edge, biased high), merged with Table 1 5.22.
- PC-2-800 (magenta left-triangles), fig6_pc2800.json, tol 50, open 1, min 2: 36 points, all rows. Point 36 is the 3-pixel tip of a triangle clipped at the frame (19.99 bar, 6.777 wt%; its true centre is just beyond 20 bar), merged with Table 1 6.77.
- PC-4-800 (olive right-triangles), fig6_pc4800.json, tol 50, open 1, min 2: 34 points, all rows. The line continues from the last visible marker (19.567 bar, 2.2% below 20 bar) to the frame; the 20-bar marker is fully clipped. Table 1 6.00 wt% at 20 bar is a separate table_direct row carrying the same isotherm_id; 35 markers counted.
- PC (brown-red diamonds in Fig. 6), fig6_pc.json, tol 50, open 2, min 3: 20 points, all rows; point 20 is a half diamond at the frame (19.86 bar), merged with Table 1 4.50.

## Values seen but not extracted

- Introduction, literature values from other work (not this paper's measurements): zeolite-templated carbon 5.4 wt% at 77 K and 20 bar [14]; CDC ca. 4.4 wt% at 77 K and 60 bar [19]; KOH-activated carbons 3.3-6.2 wt% at 77 K and 20 bar [25-28]; porous carbons 1.2-2.5 wt% under similar conditions [2,12,27,37-39]; optimum pore size 0.6-0.7 nm [17,29,40]; Chahine rule 1 wt% per 500 m2/g [43].
- Abstract, Results and Conclusions restating Table 1 (not separate measurements): "up to 2.71 wt% at 77 K and 1 bar, and 6.77 wt% at 20 bar, for PC-2-800"; "1.75-2.71 wt% at 77 K and 1 bar"; "4.23-6.77 wt%"; per-sample 1-bar values 2.19, 2.57, 2.71, 1.99, 1.75, 2.38; PC 2.23 wt%; PC-2-600 4.23 wt%, PC 4.50 wt% and PC-2-800 6.77 wt% at 20 bar.
- Abstract characterization ranges disagree with Table 1: surface area 1362-3009 m2/g (Table 1452-2919), pore volume 0.670-1.497 cm3/g (Table 0.721-1.425), N 0.56-6.53 wt% (Table 0.53-6.50). Table values used.
- Text p. 8492 gives PC a total pore volume of 0.721 cm3/g; Table 1 gives 0.569 (0.553 micropore). Table value used; noted on PC rows.
- HC (hydrochar precursor): characterization only, N 10.38 wt% (N/C 15.67%), XPS N1s single peak 396.3 eV (nitride-like or aromatic N-imines); no surface area, no H2 uptake; no row.
- Fig. 2a (N2 sorption isotherms) and Fig. 2b (NLDFT PSDs): characterization, not H2; not digitized.
- Fig. 3 (XPS N1s spectra): not uptake.
- Fig. 5a: H2 isotherms normalized to the 1-bar capacity (W/W0 against P/P0); a derived quantity of the Fig. 4 isotherms with no uptake values of its own; not digitized.
- Fig. 5b: isosteric heat of adsorption (Qst) of PC-2-600 and PC against uptake; not an uptake value; not digitized; the temperatures of the isotherms used for the Clausius-Clapeyron calculation are not stated.
- Fig. 7 (uptake at 77 K and 20 bar against surface area, 6 visible points with the Chahine line): not an isotherm; its values are the Table 1 20-bar values.
- Fig. 8 (uptake at 20 bar against N/C ratio; caption says "196 °C", evidently -196 °C, i.e. 77 K): not an isotherm; its 6 values are the Table 1 20-bar values of the N-containing samples.
- Statements without numbers: P1/2 lowest for PC-2-600; Qst of PC-2-600 smaller than PC above 0.9 wt%.
- Table 1 footnote c reads "NLDTF" (printed typo for NLDFT).
- Degassing: "evacuated for 12 h at 250 °C under vacuum" is given only for the N2 sorption analysis; not recorded in the degas fields of the H2 rows (noted on every row).
