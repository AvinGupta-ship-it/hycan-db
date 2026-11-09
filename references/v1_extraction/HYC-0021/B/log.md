# HYC-0021 extraction log (agent B)

Sethia & Sayari, Carbon 99 (2016) 289-294. Rows written: 193 (6 table_direct, 187 figure_digitized). All uptakes are at 77 K. Samples: S1 NAC-1.5-600, S2 NAC-1.5-700, S3 CP-400, S4 CP-600, S5 NAC-1.5-650, S6 NAC-1.5-550 (order of first appearance: abstract, Section 2.2, Fig. 1 legend).

## Sources extracted from

- Table 2 (main p. 291, main-3.png): H2 uptake (wt%, 77 K, 1 bar per text p. 292) for all six samples. Each value is the same measurement as the highest-pressure (~760 mmHg, 1.013 bar) point of that sample's Fig. 3 isotherm. It was merged with that point as one table_direct adsorption row (M8, M70, M99, M130, M154, M180). Table 2 also gives BET area, total pore volume, DFT pore size and DFT ultra-micropore and micropore volumes, which are on every row.
- Table 1 (main p. 290, main-2.png): NAC-1.5-600 2.96 wt% ("This work"). This is the same value as Table 2 and is cited in the source_location of M8.
- Text p. 292-293: "ranging from 0.03 to 2.96 wt%, at 77 K and 1 bar", "(2.96 vs 2.43)", "(2.43 vs 2.42 wt%)" and the Conclusion "2.96 wt%". These repeat the Table 2 values and are cited in the source_location of the merged rows.
- Table 3 (main p. 291): C, H, N (elemental analysis) and O (XPS). These are on every row: N in dopant_concentration_wt_pct, the rest in notes.
- Table S1 (SI p. 4, si1-4.png): XPS N species. They are in functional_groups for CP-400, NAC-1.5-550, NAC-1.5-600 and NAC-1.5-700. The table has no rows for CP-600 or NAC-1.5-650.
- Sections 2.3 and 2.4 (main p. 290): methods.
  - Instrument: Micromeritics ASAP 2020, static volumetric.
  - BET range: P/P0 0.05–0.20.
  - Total pore volume from N2 adsorbed at P/P0 close to 1. Pore size distribution by DFT with slit pores.
  - Degassing: in situ under vacuum at 200 °C for "several hours".
  - H2 purity: 99.999%.
  - The wt% definition is quoted in notes.
  - No free-volume calibration is described.
- Fig. 3 (main p. 292, main-4.png): H2 adsorption (filled markers) and desorption (open markers) isotherms at 77 K, 0-760 mmHg, for six samples. Twelve archives: fig3_<sample>_ads.json and fig3_<sample>_des.json.
- Fig. S4 (SI p. 4, si1-4.png): four repeated adsorption–desorption runs of NAC-1.5-600 at 77 K. Only run 1 (black stars) and run 4 (red diamonds) could be partly separated. Four archives: figS4_run1_ads/des.json and figS4_run4_ads/des.json.

## Digitization method (deviation to note)

- Calibration on the page images, with tick centres found from pixel rows and columns.
  - Fig. 3: x uses 0 at the y-axis line (133.79 px) and 800 at 557.29 px, checked at 400 = 345.54 px. y uses 0.0 at 1428.0 px and 3.0 at 1117.76 px, checked at 1.5 = 1272.5 px.
  - Fig. S4: x uses 0 at 234.9 px and 800 at 758.83 px, checked at 400 = 497.16 px. y uses 0.0 at 616.32 px and 3.0 at 208.95 px, checked at 1.5 = 413.04 px.
  - All verification residuals are below 0.3%.
- The page images are low resolution (about 150 dpi) with anti-aliasing. Open markers are 1-px outlines that the 3-px opening of `digitize_figure.py` removes, and markers of different series and branches overlap. Direct colour isolation therefore could not separate the markers. For every series I made a derived copy of the page image in the work directory (work/der/<archive>.png) and ran `digitize_figure.py extract --mode markers` on it with colour #ffff00.
  - In each copy, the pixels of each marker of that one series and branch were repainted #ffff00. Each marker was located from a visually identified seed.
  - Open markers: the repainted pixels are the white interior pixels within 2.2–3.0 px of the seed, re-centred by mean shift.
  - Filled markers: the repainted pixels are the series-colour pixels within 3.6–4.5 px of the seed, re-centred by mean shift, with a 1-px gap kept between neighbouring markers.
  - The legend area was blanked white.
  - The archives' source_image and sha256 identify the derived images. The helper scripts are work/branch.py and work/drive.py, and the seed lists are in work/specs/.
- In every archive, the count of extracted markers equals the count of seeded markers.
- Sanity check (`digitize_figure.py check`): the six Fig. 3 desorption archives, which hold the 760 mmHg point, pass against Table 2 at 750.06 mmHg (1 bar). The adsorption archives and all Fig. S4 archives remain status "unchecked" because the paper states no value inside their range. They share the calibration of the checked archives.
- The ~760 mmHg point of each Fig. 3 isotherm is drawn with the open symbol but is the turnaround point. It carries the Table 2 value as an adsorption row and has no separate desorption row. For Fig. S4 run 4, the 762 mmHg point has no table value and is kept as a desorption row, with a note.

## Plotted markers not digitized (could not be separated)

- Fig. 3, all series: markers below about 20 mmHg are stacked on the y-axis (x < 146 px) and overlap one another and the axis line. They are counted only where identifiable, so isotherm_point_count is a lower bound.
- Fig. 3, NAC-1.5-700:
  - A vertical stack of at least 2–3 filled diamonds at P < 5 mmHg (x 135–140 px, y 1409–1432 px) is not separable.
  - Filled markers at about 30, 100, 300, 400 and 500 mmHg appear hidden under open diamonds and were not counted.
- Fig. 3, NAC-1.5-650:
  - Filled down-triangles at about 100, 300, 400 and 500 mmHg are visible only as small fragments next to the open triangles. They are counted but not digitized.
  - The open triangle at about 300 mmHg has its interior covered. It is counted but not digitized.
  - Violet markers on the axis near (139,1374), (140,1389) and (136,1401) px are not separable.
  - A possible open triangle near (152,1328) px is ambiguous.
- Fig. 3, NAC-1.5-550:
  - A filled triangle near 30 mmHg, at about (150,1369) px, is mostly under a NAC-1.5-700 open diamond. It is counted but not digitized.
  - Other green markers below about 60 mmHg overlap NAC-1.5-700/650/600 markers and were not separated.
- Fig. 3, NAC-1.5-600:
  - Stars below about 25 mmHg near the axis are not separable.
  - The stars at 300, 400 and 500 mmHg look heavier, which may mean filled stars hidden under the open ones. These were not counted.
- Fig. 3, CP-400:
  - A filled square at about 140 mmHg (centre about (207.5,1426.5) px) is mostly under an open square. It is counted but not digitized.
  - Filled squares at about 200 and 500 mmHg may be fully hidden. They were not counted.
- Fig. 3, CP-600: nothing further identified. Markers below 10 mmHg may be hidden under the NAC-1.5-700 stack.
- Fig. S4, runs 2 (violet) and 3 (green): the markers lie under run 4 and between runs 1 and 4 and are not separable. No rows were written.
- Fig. S4, run 1:
  - The open star at 760 mmHg has an interior split by a line, which gave two 3-px fragments. It is counted but not digitized.
  - Filled and open stars at or below 200 mmHg are mostly covered by the other runs. Filled stars near 140 and 180 mmHg show only their tips. These were not digitized.
- Fig. S4, run 4:
  - At least 2 filled diamonds stacked on the axis at about 5 mmHg (x 238 px, y 590–605 px) are not separable.
  - Filled diamonds at about 100 and 200 mmHg are mostly under open diamonds. They are counted but not digitized.
- Partly hidden markers that were digitized have the centroid of their visible part, extraction_confidence 2 and a note on the row.
- CP-400: the 31.5 mmHg filled square digitized to -0.0004 wt% (centre 0.04 px below the 0.0 tick). It is stored as 0 because the schema does not allow a negative uptake. The note is on the row (M89).

## Values seen but not extracted

- Table 1, literature comparison values for other groups' activated carbons at 77 K and 1 bar: ACT-850 2.41 [14], PBA 2.84 [15], CAC1 2.85 [16], Ch800/700/3 2.95 [17], C2-1/4-700 2.50 [18], CAC4 3.21 [19] and AC8 3.28 [20]. These samples were not prepared or measured in this paper, so they were not extracted.
- Introduction p. 290: "3.28 wt% from hemp stem [20] and 2.85 wt% from petroleum pitch [15]". These are literature values, not extracted.
- Abstract: NAC-1.5-600 "2.94 wt% at 77 K and 1 bar". This conflicts with 2.96 in Tables 1-2, the text and the Conclusion. It was not made a separate row (same sample, temperature and pressure as the Table 2 value and the same plotted point) and is recorded in the notes of M8.
- Text p. 293: Fig. S4 runs show "less than 0.5% loss per cycle". This is not an uptake value and not an uncertainty in wt%. It was not stored. replicates_reported = true for NAC-1.5-600 because four runs are plotted.
- Text p. 292: BET area of NAC-1.5-600 given as 1312 m2/g, against 1317 m2/g in Table 2. The Table 2 value is stored and the discrepancy is noted on the S1 rows.
- Figs. 4 and 5 (main p. 292) and Figs. 6 and 7 (main p. 293-294): H2 uptake, pore volumes, surface area and N/O/H or N-species content against activation temperature. These are not isotherms and were not digitized. The values they show are the Table 2, Table 3 and Table S1 values, so there are no new values.
- Fig. 1 (N2 isotherms), Fig. 2 (DFT PSD), Figs. S1–S2 (TEM) and Fig. S3 (XPS N1s): no H2 uptake values.
- Table 2: DFT pore size of CP-600 is printed "<0.364" nm (probe molecules). It is not stored as a number and is noted on the S4 rows. CP-400 pore size and DFT volumes are NA.
- No non-carbon sorbents are measured in this paper.
