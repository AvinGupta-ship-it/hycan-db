# HYC-0101 extraction log (agent A, claude-sonnet-5-5, 2026-10-29)

Paper: Adeniran and Mokaya, Nano Energy 16 (2015) 173-185, DOI 10.1016/j.nanoen.2015.06.022. Rows written: 629 (merged table/text+plot rows 54, figure_digitized-only rows 491, table-only rows 84). Validator: 0 errors, 21 warnings (uptake above 10 wt%).

Naming: HYC-0101-Sn are sample ids. Figure ids S9, S11a, S13 and S15 are SI figures; archive file names use the figure id (for example `HYC-0101_S15_MPPY4_Excess.json` is the Figure S15 curve of sample HYC-0101-S14). Page numbers: main text PDF page main-n = journal page 172 + n; SI page = file index si1-n.

## Sample numbering and coding decisions

- S1-S8 follow Table 1 order: PPY2, MPPY2, PPY3, MPPY3, PPY4, MPPY4, S4800, S4800P. S9 = AX21 (commercial benchmark). S10-S13 follow Table 3 order: PPY4-C5, PPY4-C10, MPPY4-C5, MPPY4-C10. S14 = MPPY4 and S15 = MPPY4-C10 as measured in batch 2.
- Two measurement batches are kept as different samples with the same label: batch 1 (Hiden IGA-003, 0-20 bar; Table 1, Table 3, Figures 3, S9, S11a, S13) and batch 2 (Hiden Xemis, 0-150 bar; Tables S2-S5, Figures 5, 6, S15). Reason: the two data sets come from different instruments and pressure ranges, the RT 20 bar value of MPPY4-C10 differs between them (0.344 wt% digitized in Figure S13 vs 0.31 wt% printed in Table S4), and the paper does not say that the same sample batch was used.
- material_class: doped_carbon for the polypyrrole-derived carbons (N comes from the precursor, about 0.4-0.55 wt% N, not deliberate doping; stated in the notes), activated_carbon for S4800, S4800P and AX21.
- AX21: 2881 m2/g and 1.71 cm3/g are printed in the main text without a method, so surface_area_method and pore_volume_method are "unspecified", BET fields are empty and area_same_sample is "unclear".
- All isotherms: temperature -196 °C stored as 77.15 K and 25 °C as 298.15 K (temperature_inferred false, both printed). Excess is gravimetric; total is the authors' excess plus compressed H2 in the pore volume (N2 total pore volume; D-R micropore volume from CO2 at 0 °C for the "parenthesis" values of Table S4). Pressure is absolute bar as printed (bar).
- Volumetric values (g l-1) are stored in uptake notes as the authors' wt% x packing density (0.39 g cm-3 MPPY4, 0.52 g cm-3 MPPY4-C10) and not recomputed.
- isotherm_point_count: markers counted on the plot, including markers detected but not extracted (see below). Estimates, flagged in the notes: Figure S11a MPPY4-C10 Excess 20 (grid shared with the Total curve), Figure S15 RT curves 20 (sample S14) and 21 (sample S15) because the low-pressure markers overlap. Figure S13 curves 18.
- Digitization method disclosure: markers were extracted with `digitize_figure.py extract --mode markers --no-roi` on synthetic marker-only images built per series in the work directory (per-colour opening and watershed splitting to separate touching markers). Where a filled marker was partly hidden by another marker its centre was recovered by fitting a disc of the unobstructed marker size to the visible part; those rows say so in the notes and have extraction_confidence 3. Recovered markers: Fig 3b PPY3 Total 1, Fig 3c PPY4 Total 1, Fig 3d S4800 Total 3, Fig 5 MPPY4 Total 6, Fig 5 MPPY4-C10 Total 2. Every archive in `digitizations/` was checked with `digitize_figure.py check` against printed table or text values (32 passed; 1 unchecked, Figure S13 MPPY4-C10, which has no printed value). The Figure S11a MPPY4-C10 Excess check needed `--tolerance-pct 3` because the absolute tolerance was above the 10% limit.
- Confidence: 5 for table, text and merged rows; 4 for digitized rows; 3 for recovered markers (7 rows) and for all Figure S11a rows (28; heavy overlap of the red MPPY4 and black MPPY4-C10 markers).

## Extracted from

- Table 1 (main text p.176): excess and total H2 at 20 bar, 77 K, for S1-S8 (16 values). Each merged with the plotted point of Figure 3 at 19.86-19.94 bar; printed value and pressure 20 bar kept, plot pressure and value in the notes.
- Figure 3a (main text p.178): PPY2 Excess 29 points, PPY2 Total 23, MPPY2 Excess 30, MPPY2 Total 23 (points listed include the Table 1 merged point; rows = points).
- Figure 3b (p.178): PPY3 Excess 30, PPY3 Total 16, MPPY3 Excess 23, MPPY3 Total 25.
- Figure 3c (p.178): PPY4 Excess 31, PPY4 Total 20, MPPY4 Excess 23, MPPY4 Total 23.
- Figure 3d (p.178): S4800 Excess 24, S4800 Total 17, S4800P Excess 22, S4800P Total 24.
- Table 3 (main text p.180): excess and total at 20 bar for PPY4-C5, PPY4-C10, MPPY4-C5, MPPY4-C10 (8 values). MPPY4-C10 values (5.4/7.2) merged with Figure S11a points at 19.94 bar; the other three samples have no plotted isotherm that I extracted (see Figure S11b below), so those 6 rows are table_direct without an isotherm id.
- Figure S11a (SI p.19, si1-19): MPPY4-C10 Total 20 points (2.97-19.93 bar), MPPY4-C10 Excess 10 points (5.90-19.94 bar).
- Main text p.180, AX21 benchmark sentence ("4.5 wt% excess, 5.6 wt% total", 77 K): two rows merged with Figure S9 AX21 points at 19.95 bar; no pressure printed so the pressure is digitized and the notes say "pressure digitized".
- Figure S9 (SI p.17, si1-17): AX21 Excess 30 points (0.21-19.95 bar), AX21 Total 17 points (3.01-19.95 bar).
- Figure 5 (main text p.181, main-09): 77 K, 0-150 bar, batch 2. MPPY4 Excess 20 points, MPPY4 Total 19, MPPY4-C10 Excess 19, MPPY4-C10 Total 18.
- Table S2 (SI p.4, si1-04): total gravimetric and volumetric uptake at 40-150 bar every 10 bar for the two batch 2 samples (24 rows, each merged with a Figure 5 Total point).
- Table S3 (SI p.5, si1-05): excess maximum at ca. 40 bar (6.5 and 6.0 wt%; 25.4 and 31.2 g l-1) for the two batch 2 samples; merged with the Figure 5 Excess maximum point (digitized 6.33 and 5.90 wt%).
- Table S4 (SI p.6, si1-06): 298.15 K, 20-150 bar every 10 bar, three rows per sample and pressure (excess; total with N2 pore volume; total with D-R micropore volume, the parenthesis values), gravimetric and volumetric (84 rows). The 150 bar rows are merged with the Figure S15 digitized points (6 archives) and also cite Table S5; the other pressures have no plotted point extracted and are table_direct without an isotherm id.
- Table S5 (SI p.7, si1-07): 150 bar RT gravimetric and volumetric values for the two batch 2 samples; used for the volumetric figures of the 150 bar excess rows (6.3 and 6.9 g l-1). The literature rows of Table S5 are not extracted (see below).
- Figure S15 (SI p.23, si1-23): RT, highest-pressure point only (149.8-150 bar) for each of 6 curves (Excess, Total, Total D-R for each batch 2 sample). Figure 6 (main text p.181) shows the same excess curve and was used as a cross-check, not digitized separately.
- Main text p.182 RT sentences: MPPY4 0.5 wt% at 20 bar (merged with the Figure S13 digitized point 0.4975 wt% at 20.0 bar) and AX21 0.32 wt% at 20 bar (merged with the Figure S13 AX21 point 0.3268 wt%).
- Figure S13 (SI p.21, si1-21): MPPY4-C10 batch 1 RT highest-pressure point 0.344 wt% at 20 bar, digitized with no printed counterpart (status unchecked; no row merge). The figure has no y-axis label; wt% is taken from the text for the other two curves.

## Values seen but not extracted

- Figure S11b (PPY4 and PPY4-C10, SI): not extracted. Its digitized end values disagree with Table 1 and Table 3 by 8-12%: PPY4 total 7.14 wt% at 19.93 bar vs Table 1 6.5; PPY4 excess 5.37 at 19.0 bar vs 5.0; PPY4-C10 excess 5.17 at 19.5 bar vs Table 3 4.6; PPY4-C10 total 6.53 at 19.94 bar vs 5.9. Figure 3c and Figure S9 give PPY4 curves consistent with Table 1; the cause of the Figure S11b mismatch is not stated in the paper and was not resolved. Table 3 values are kept as rows.
- Figure S11a MPPY4 (red, Total 10 points, Excess 6 points): replot of the Figure 3c MPPY4 curves, heavily occluded by the C10 markers; no rows (same data already extracted from Figure 3c).
- Figure S11a MPPY4-C10 Excess: about 10 further open black markers overlap the open red markers and could not be separated; not extracted (isotherm_point_count 20 is estimated from the Total grid).
- Figure S9 MPPY4 and PPY4 curves: replots of Figure 3c; no rows.
- Figure S12 (checked on the page image): replot of the MPPY4-C10 excess isotherms, Xemis 0-150 bar and IGA 0-20 bar, captioned "virtually identical"; same data as Figure 5 and Figure S11a; no rows.
- Figure S10A (H2 and D2 uptake of MPPY4): the y-axis label and unit are absent and the caption gives no temperature, so unit and temperature are not printed; not extracted. The H2 curve resembles the 77 K excess (about 4.7 at 10 bar) but that is not stated. Figure S10B is the D2/H2 ratio, not an uptake.
- Near-origin markers detected but not extracted (steep low-pressure region, overlapping rings or the y-axis; counted in isotherm_point_count): Fig 3a PPY2 Excess 2; Fig 3b PPY3 Excess 2; Fig 3c PPY4 Excess 2; Fig 3d S4800P Excess 2; Fig 3d S4800 Excess 4 plus a dense unresolvable smear; Fig 5 MPPY4 Excess 2; Fig 5 MPPY4-C10 Excess 1. Low-pressure RT markers in Figure S15 overlap one another and cannot be counted individually, so only the highest-pressure point of each RT curve is a row.
- Room-temperature curves of Figures S13 and S15 other than the highest-pressure point: out of scope (only 77 K isotherms are digitized in full).
- Literature or comparison materials (not this paper's samples): Table S3 MOFs (MOF-5, MOF-5 pellets, MOF-177, NOTT-112, NU-100, MOF-210); Table S5 KUA5, ZTC (two entries), MOF-5, MOF-210; main text comparison values 3.0-5.2, 7.08, 7.03 and 7.3 wt% (refs 5, 6, 27, 9, 29, 30); RT comparison values 1.3 (CNT, ref 29), 1.2 and 1.3 (ZTC) and 1.0 wt% (KUA5).
- CO2 uptake data (Figures 7, 8, S14, S16; Tables 2 and 4; PPY2600/MPPY2600 comparison carbons): not H2.
- Derived percentages in the text ("45% higher", "10% decrease" and similar): not independent measurements.
- Characterization-only values, not uptake rows: Table S1 yields, N2 isotherms, pore size distributions, t-plot micropore areas (1157 and 1413 m2/g, stored on S7 and S8 where they are printed), D-R CO2 micropore volumes 1.97/1.50 cm3/g (1.71/1.25 at 25 °C), skeletal density 2.1-2.2 g cm-3 from ref 53.

## Discrepancies in the paper

- Fig 3c MPPY4 Excess digitizes to 5.354 wt% at 19.88 bar against printed 5.5 (2.6% low); Fig S11a MPPY4 Excess ends at 5.67 (3% high). Fig 5 MPPY4 excess maximum digitized 6.33 against printed 6.5; MPPY4-C10 5.90 against 6.0. The printed value is on the merged row and the digitized plot value is in its notes.
- Table S4 prints the MPPY4-C10 excess at 150 bar as 1.33 wt% and Table S5 prints 1.32; the Table S4 value is stored and the Table S5 value is in the notes.
- Main text p.181 prints PPY4-C10 excess as 4.5 wt% ("5.0-4.5 wt% for excess") while Table 3 prints 4.6; Table 3 value stored, text value in the notes.
- Summary section (p.184) gives RT values of 3.4/3.2 wt% (14/18 g l-1) that conflict with Tables S4/S5 and the abstract (3.6/3.4 wt%); not stored separately. Abstract and summary volumetric roundings (38, 56, 49, 72 g l-1) differ from the table values (37.4, 55.4, 48.4, 72.3 g l-1); table values stored.
- The SI says the packing density was measured at 7 MPa, the main text says 74 MPa; both noted, no row field affected.
- RT 20 bar MPPY4-C10: Figure S13 digitized 0.344 wt% (batch 1) vs Table S4 0.31 wt% (batch 2); kept as different samples.
- The MPPY4-C10 sample is labelled 10MPPY4 in Figure S13 and MPPY4-C10 elsewhere; noted on the rows.
