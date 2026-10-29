# HYC-0072 extraction log (agent B)

Paper: Almasoudi and Mokaya 2014, J. Mater. Chem. A, doi 10.1039/c4ta00530a. Main article only (pages main-1 to main-9); no supplementary file was supplied.

## Sources extracted from

- Section 2.1 (p. 10961, main-2): synthesis of AC-BF900, AC-BF1000 (LI route), AC-CB700, AC-CB850 (LI + CVD route), KOH activation, compaction at 5 and 10 tonnes (370 and 740 MPa). Used for sample descriptions on all rows.
- Section 2.2 (p. 10961-10962, main-2/3): N2 sorption at -196 C (Micromeritics ASAP 2020), BET range P/P0 0.06-0.22, total pore volume at P/P0 = 0.99, NLDFT PSD. Used for surface-area and pore-volume coding.
- Section 2.3 (p. 10962, main-3): H2 uptake by gravimetry, Hiden IGA-003, 99.9999% H2, -196 C (liquid nitrogen bath), 0-20 bar, oven drying 24 h at 80 C, degassing 200 C at 10^-10 bar for 4-6 h, buoyancy correction (carbon density 1.5-1.8 g cm-3, H2 density 0.04 g cm-3). Used for method fields on all rows.
- Table 1 (p. 10964, main-5): BET surface area, micropore surface area, total pore volume, micropore volume, NLDFT pore-size maxima for the 12 activated samples. Copied onto every row of each sample.
- Section 3.2 (p. 10966, main-7): packing densities (0.4, 0.56, 0.45, 0.52 g cm-3 for the four uncompacted carbons; ca. 0.65 and 0.68 after 5 and 10 tonnes). Copied to packing_density_g_cm3.
- Table 2 (p. 10965, main-6): H2 uptake at -196 C/20 bar in wt% and g l-1 for 12 samples. 12 rows (table_direct), each merged with the 20-bar marker of its Fig. 5 series where that marker could be digitized (10 of 12).
- Fig. 5a-d (p. 10965, main-6): 77 K H2 isotherms, 12 series, triangle markers. Digitized with digitize_figure.py in markers mode; 220 figure_digitized rows. Archives in digitizations/ (one per series).

## Digitization set-up (Fig. 5)

- Working image: a copy of main-6.png with the four legends and the panel labels (a)-(d) painted white (work/main-6_fig5_masked.png), so that legend markers and label text are not picked up; plot data were not altered.
- Tick centres found from pixel-row/column darkness profiles. Calibration (pixel = value), with the third tick as check:
  - 5a: x 311.10 = 0, 607.71 = 20, check 459.57 = 10; y 1135.06 = 0, 909.43 = 7, check 1038.34 = 3.
  - 5b: x 311.81 = 0, 608.09 = 20, check 460.00 = 10; y 1410.03 = 0, 1184.41 = 7, check 1313.31 = 3.
  - 5c: x 669.00 = 0, 967.15 = 20, check 818.14 = 10; y 1138.34 = 0, 912.00 = 7, check 1041.38 = 3.
  - 5d: x 668.90 = 0, 967.15 = 20, check 818.13 = 10; y 1414.05 = 0, 1187.77 = 7, check 1317.00 = 3.
  - All check ticks within 0.2% (tool verification passed).
- Colours: black #000000, red #ee322a, blue #3852a4. Tolerance 40 or 60 and opening 2 or 3 px chosen per series to maximise separated single markers (settings stored in each archive).
- digitize_figure.py check against Table 2 at the 20-bar marker passed (5% tolerance) for the 10 series with a digitized 20-bar marker. Fig5b_AC-BF1000.json and Fig5b_AC-BF1000at5Ton.json stay unchecked (no 20-bar marker separable).
- Marker counts: the pressure program visible in every series is 1.5, 2, 3, 4, 5, 6, 7, 8, 8.5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 18.5, 19, 19.5, 20 bar (23 markers), preceded by the origin and markers near 0.05, 0.1, 0.25, 0.5, 0.75 and 1.0 bar (fully resolved only for AC-CB850, Fig. 5d black). isotherm_point_count = 30 on every row. Below about 1.5 bar the markers of all three series in each panel overlap and could not be counted one by one, so the low-pressure part of each count comes from the AC-CB850 sequence. AC-BF1000@5Ton shows an extra red marker near 0 bar (0.18 wt%), so its true count may be 31.
- AC-BF900@10Ton (5a, blue) and AC-CB700@10Ton (5c, blue) are each drawn as two near-coincident curves with markers (offset 1-2 px in 5a, 2-4 px in 5c, converging at 18-20 bar). The paper does not say what the second curve is (desorption or repeat run), so all rows are coded adsorption under one isotherm_id. Overlapping marker pairs could not be separated: the centroid of each blob is recorded and flagged in notes (confidence 2 where the pair is visibly doubled). The second-curve markers are not counted in isotherm_point_count.

## Markers per series: separated, not separated, excluded

- Fig5a_AC-BF900 (black): 19 markers separated (5-20 bar); 18 rows plus the 20-bar marker merged with Table 2. Not separated: 11 markers at 0-4 bar (under the red and blue markers).
- Fig5a_AC-BF900at5Ton (red): 23 separated (1.5-20 bar); 22 rows plus 20-bar merge. Not separated: 7 markers at 0-1 bar (under the blue markers).
- Fig5a_AC-BF900at10Ton (blue): 29 blobs. Not extracted: archive index 0 (origin, 0 bar, 0 wt%); index 4 (0.37 bar, 1.61 wt%, 39 px) and index 5 (0.89 bar, 2.21 wt%, 111 px), which are merged blobs of several markers around 0.5-1.0 bar. 25 rows plus 20-bar merge.
- Fig5b_AC-BF1000 (black, legend printed "AC-BF100"): no rows from the figure. All three Fig. 5b curves coincide within about 0.1 wt% and the black markers are covered by the blue and red ones. The tool found only 9 slivers of 6-10 px (-0.09/0.40, 0.15/0.45, 5.01/3.37, 6.06/3.51, 8.01/3.82, 9.09/3.89, 10.17/3.97, 15.10/4.48, 20.06/4.92 bar/wt%), which are not marker centres. About 30 markers not separated. Table 2 row only (isotherm I2).
- Fig5b_AC-BF1000at5Ton (red): 2 rows (0.0128 bar/0.178 wt% and 0.0466 bar/0.575 wt%, both on the y axis, confidence 2). Not extracted: index 1 (origin). Not separated: all markers above about 0.05 bar (under the black and blue markers), including the 20-bar marker.
- Fig5b_AC-BF1000at10Ton (blue): 27 blobs. Not extracted: index 3 (0.37 bar, 1.51 wt%, 35 px) and index 4 (0.87 bar, 2.00 wt%, 105 px), which are merged blobs. 24 rows plus 20-bar merge.
- Fig5c_AC-CB700 (black): 24 blobs. Not extracted: index 0 (1.12 bar, 2.56 wt%, 32 px), a merged blob around 1 bar. 22 rows plus 20-bar merge. Not separated: markers at 0-1 bar.
- Fig5c_AC-CB700at5Ton (red): 20 blobs. Not extracted: index 0 (0.00 bar, 0.28 wt%), a marker centred on the y axis whose digitized pressure is 0.0 bar (pressure not resolvable; the validator rejects 0 bar); index 1 (origin). 17 rows (index 2 at 6 bar is partly hidden, confidence 2) plus 20-bar merge. Not separated: about 10 markers between about 0.05 and 5 bar (under the blue markers).
- Fig5c_AC-CB700at10Ton (blue): 26 blobs. Not extracted: index 0 (0.00 bar, 0.56 wt%), a marker centred on the y axis with digitized pressure 0.0 bar; index 1 (0.06 bar, 0.92 wt%, 61 px) and index 3 (0.78 bar, 1.99 wt%, 209 px), which are merged blobs. 22 rows plus 20-bar merge; indices 4-10 and 12-22 (2-18.5 bar) are doubled pairs (see above). The 1.5-bar marker was not separated.
- Fig5d_AC-CB850 (black): 29 blobs. Not extracted: index 0 (origin). 27 rows plus 20-bar merge. Not separated: the 1.5-bar marker (hidden).
- Fig5d_AC-CB850at5Ton (red): 20 blobs. Not extracted: index 0 (4.08 bar, 2.90 wt%, 11 px), a sliver under half a full marker. 18 rows plus 20-bar merge. Not separated: about 10 markers at 0-4 bar (under the black and blue markers).
- Fig5d_AC-CB850at10Ton (blue): 25 blobs. Not extracted: index 0 (0.27 bar, 1.33 wt%, 9 px sliver). 23 rows (indices 1 and 2 at 0.98 and 1.58 bar are partly hidden, confidence 2) plus 20-bar merge. Not separated: the other markers below 1 bar.

## Values seen but not extracted

- Table 2, CO2 uptake column (mmol g-1 at 25 C and 1 bar; 2.0, 2.4, 2.2, 2.0, 2.0, 2.0, 2.0, 2.3, 2.1, 1.9, 2.1, 1.6): CO2, not H2.
- Abstract, Section 3.3 and Summary: CO2 uptakes 2.4, 2.2 and 2.0 mmol g-1: CO2, not H2.
- Abstract (p. 10960): 6.5 wt% (AC-BF900@5Ton), 5.7 wt% (AC-BF900@10Ton), 6.2 wt% (AC-BF900), 42.3 g l-1, all at -196 C and 20 bar. Same measurements as Table 2; no separate rows (cited in source_location).
- Section 3.2 (p. 10965): "increasing from 6.2 to 6.5 wt%" and "from 6.2 to 5.7 wt%" (AC-BF900 family, 20 bar). Same as Table 2; no separate rows.
- Section 3.2 (p. 10966): "following compaction of sample AC-CB700, the volumetric hydrogen uptake increases significantly from 24.8 g l-1 to 38.8 g l-1 and 42.3 g l-1 after 10 and 5 tonne compaction", and "from 24.8 g l-1 for sample AC-CB700 to 42.3 g l-1 for sample AC-CB700@5Ton". These numbers are the Table 2 values of AC-BF900, AC-BF900@10Ton and AC-BF900@5Ton; Table 2 gives 26.5, 33.3 and 36.4 g l-1 for AC-CB700, @10Ton and @5Ton. The sample label in the text is taken as a misprint and no rows were made. Flagged for reconciliation.
- Section 3.2 (p. 10966): AC-BF1000 "ca. 32 g l-1 compared to 27.4 g l-1 before compaction". Approximate restatement of Table 2 (31.9 and 32.0; 27.4); no separate rows.
- Summary (p. 10966-10967): 6.5 wt%, 6.2 wt%, 5.7 wt% and 42.3 g l-1 at -196 C and 20 bar. Same as Table 2; no separate rows.
- "up to 70% improvement/increase in volumetric hydrogen uptake" (Abstract, Section 3.2, Summary): a ratio derived from Table 2, not a measurement.
- Table 2, AC-CB700: 26.5 g l-1 does not equal wt% x packing density (6.2 x 0.45 x 10 = 27.9 g l-1); the other 11 values do. Recorded as printed and noted on the row.
- Introduction (p. 10960-10961): literature values from cited works (ca. 20 g l-1 at -196 C and 40 bar, refs 44-45; 30-40 g l-1 at -196 C and 45-60 bar, refs 48-49; ca. 30 g l-1 at -196 C and 40 bar, ref. 48; 35 g l-1 at -196 C and 60 bar, ref. 50; 29 g l-1 at -196 C and 40 bar, ref. 51; packing densities 0.4-0.5 and 0.7 g cm-3; 2800 m2 g-1 and 1 cm3 g-1, ref. 53; compaction stabilities 180, 340 and 420 MPa). Not measurements of this paper.
- Section 3.1 and 3.2 derived percentages and differences (surface-area rise of 135 m2 g-1, ca. 4%; micropore-area rise of 402 m2 g-1, 16%; 14% and 18%; micropore-area share 89% to 86%; micropore-volume share 69% to 56%; 75-97%; above 54%; ca. 40% lower N2 uptake): derived from Table 1 or Figs. 2-3, not H2 values.
- Fig. 1 (XRD), Figs. 2-3 (N2 sorption isotherms), Fig. 4 (NLDFT pore-size distributions): not H2 uptake; not digitized. The pore-size maxima in Table 1 are recorded in notes, not as average_pore_diameter_nm (three maxima, no single diameter).
- Non-activated ZIF-templated carbons BF900, BF1000, CB700 and CB850 (Section 2.1): no characterization or H2 uptake reported; no rows.
- ZIF-8 template (Basolite Z1200): not a carbon sorbent, no uptake reported.
- Degassing duration "4-6 h": a range, so degas_duration_h is left empty (stated in notes). The 10^-10 bar end pressure is stored as 1e-05 Pa.
- Sample mass for the H2 measurement is not stated (the ca. 0.25 g refers to compaction).
