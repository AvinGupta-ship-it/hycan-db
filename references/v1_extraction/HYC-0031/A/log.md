# Extraction log HYC-0031 (agent A)

## Extracted from
- Main Table 2 (p.4): CA-4600/4700/4800 total and (excess) H2 at 1, 20, 30 bar, 77.15 K (-196 C); volumetric g/l at 20 and 30 bar put on the matching rows; packing densities (text p.8, Methods) in packing_density_g_cm3. Table 1 O content in descriptions.
- Supp. Table 2 (SI p.17): C-4600/4700/4800 1 bar and 20 bar total (excess).
- Supp. Table 3 (SI p.18): G-4700, S-4700, E-4700, F-4700, LAC4700, ACGR4700, ACCA4700, CN4700 1 bar and 20 bar; previously reported citations in notes (refs 8, 9, 4, 10). C-4700 previously reported ref 8.
- Supp. Table 4 (SI p.19): PPY-4800, ZTC-5 (previously reported, refs 2, 3), AX21 (this work). Supp. Table 5 values for ACGR4700/ACCA4700 repeat Table 3 (noted in source_location).
- Text p.7-9: AX21 4.7/5.9 wt% at 20 bar, room-temperature excess at 20 and 30 bar (AX21, CA-4600, CA-4800, CA-4700), room-temperature total at 30 bar (AX21 0.8, CA-4800 0.95, CA-4700 1.2).
- Fig. 6 (excess CA-4600/4700/4800, 77 K): digitized every separable marker. Supp. Fig. 9 (totals CA-4T and C-4T, 77 K). Supp. Fig. 10 (CA-4700 excess supplementary points; PPY-4800, ZTC5, AX21 total and excess). Supp. Fig. 14 (25 C, 0-30 bar): highest-pressure point per isotherm only, plus merged text values. Supp. Fig. 15 (25 C to 100 bar CA-4700): highest-pressure point of total and excess only.
- Methods (p.10): Hiden XEMIS, 99.9999% H2, degas 200 C at 1e-10 bar 4-6 h, BET P/P0 0.04-0.22, t-plot micropore data.

## Merging
All table/text values within 2%/0.02 bar of a plotted point on the same isotherm were merged (digitized point in notes, no separate row). Largest difference: CA-4800 25 C total 30 bar, text 0.95 vs plotted 0.917 (-3.5%).
Table values with isotherm id but no separable marker: 1 bar excess values (Fig. 6 markers hidden), PPY-4800 and ZTC-5 total 20 bar (no marker near 20 bar), CA-4700 25 C excess 30 bar (Supp. Fig. 14 marker not separable; Supp. Fig. 15 separate run gives 0.789 at 30.07 bar).

## Digitization methods and limits
- Filled markers: tool output directly; archives rebuilt from valid markers only (merged/partial centroids dropped, raw outputs kept in work/raw). Open rings and open stars: located by ring/hole fitting, then re-measured by digitize_figure.py on synthetic small-disc images (archive source_image points to those images in work/).
- Same isotherm re-plotted in Fig. 6, Supp. Fig. 9, Supp. Fig. 10 (CA-4T totals, CA-4700 excess) treated as one isotherm; totals from Supp. Fig. 9, excess from Fig. 6 plus Supp. Fig. 10 markers where Fig. 6 markers are hidden. Fig. 6 total curves, Supp. Fig. 10 CA-4700 total, Fig. 8a, Supp. Fig. 13 used only as cross-checks.
- Not separable (hidden or overlapping, low pressure region below about 2-3 bar for most series, and clusters): CA-4600 excess below 4 bar; CA-4800 excess 10-14 bar and below 5 bar; CA-4700 excess at 1 bar; CA-4600/4800 total some low-pressure and 23-24 bar markers; ZTC5 total (only 7 of 33 markers valid); PPY-4800 total and excess partly; AX21 total (18-20 bar star cluster recovered from tips, rows included, centroid offset from isolated stars 8.19 px); AX21 25 C total 30 bar marker partly under axis (flag partial, confidence 3 not applied to merged row); 25 C CA-4600 total only 9 markers separable.
- isotherm_point_count is my count of markers including unseparable ones, a lower-confidence estimate for those series.
- Checks: all archives passed digitize_figure.py check at a printed value except sfig14_CA-4600_total (no printed value, unchecked).

## Seen, not extracted
- Fig. 7, Supp. Fig. 13, Supp. Table 6 MOF rows (NOTT-112, NU-100, MOF-210): not carbon. Supp. Table 6 CA-4T values repeat Table 2.
- Fig. 8a: duplicate of Supp. Fig. 14 excess. Fig. 8b Qst values (9.5-10.6 kJ/mol etc.): not uptake. Fig. 5 TPD CO/CO2 (wt% of evolved gas), XPS, IR, Raman, TGA, XRD, N2 isotherms and PSDs: no H2 uptake; characterization used. Hydrochar CA-hydrochar and C-hydrochar: characterization only, no H2 value, no row.
- Volumetric values 32-41 g/l excess etc. placed on matching rows; CA-4700 volumetric at 1 bar not given.
- Source discrepancies: CA-4800 pore volume 1.54 (text) vs 1.32 (tables), 1.32 used; CA-4800 total 20 bar 41 g/l vs 6.8 x 0.56 = 38; RT total CA-4800 0.95 text vs 0.917 plotted; text says AX21 excess 30 bar 0.38.
- Judgement calls: material_class activated_carbon (oxygen-rich, not coded doped); synthesis_method carbonization (hydrothermal carbonization then KOH); wt% convention unknown (not defined); unlabelled 1 bar and Supp. Table 3 20 bar values coded basis unspecified; area_same_sample for literature carbons other_paper/unclear.
