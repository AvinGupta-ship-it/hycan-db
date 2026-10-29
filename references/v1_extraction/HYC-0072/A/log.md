# log.md - HYC-0072 (Almasoudi and Mokaya 2014), extractor A (claude-sonnet-5-5), 2026-10-29

230 rows in rows.csv: 12 Table 2 rows (each carries the 20 bar value, and the g l-1 value as volumetric_capacity_kg_m3) and 218 digitized rows. validate_row_detail.py --errors-only: 0 errors.

## Passages and tables extracted from

- Table 2 (main page 6, journal p. 10965): H2 uptake at -196 C / 20 bar, 12 samples, wt% and g l-1 (both on the same row). Merged with the 20 bar marker of the matching Fig. 5 isotherm (digitized point recorded in notes) for 10 samples; for AC-BF1000 and AC-BF1000@5Ton the 20 bar marker is overdrawn in Fig. 5b and no digitized point exists.
- Table 1 (main page 5, p. 10964): BET area (parenthesis = micropore area), total pore volume (parenthesis = micropore volume), PSD maxima; placed on every row of the sample. PSD maxima are three modal values per sample (6/12/25 A etc.), so average_pore_diameter_nm is left empty and the maxima are in notes.
- Section 2.1 (synthesis and compaction), 2.2 (BET P/P0 0.06-0.22, N2 at -196 C, ASAP 2020, NLDFT PSD, total pore volume at P/P0 0.99), 2.3 (H2 at -196 C, 0-20 bar, Hiden IGA-003, 99.9999% H2, degas 200 C / 10^-10 bar / 4-6 h, buoyancy correction): used for characterization, method and degassing fields.
- Section 3.2 text: packing densities 0.4 (AC-BF900), 0.56 (AC-BF1000), 0.45 (AC-CB700), 0.52 (AC-CB850); "ca. 0.65 and 0.68" after 5 and 10 tonnes. Stored in packing_density_g_cm3 on all rows of each sample (compacted values are "ca.").
- Fig. 5a-d (main page 6, p. 10965): 12 H2 isotherms at -196 C, adsorption only (no desorption branch shown or mentioned). Digitized as below.

## Sample numbering and labels

- S1-S12 follow the order of Tables 1 and 2: AC-BF900, @5Ton, @10Ton, AC-BF1000, @5Ton, @10Ton, AC-CB700, @5Ton, @10Ton, AC-CB850, @5Ton, @10Ton. The running text introduces them in a different order (section 2.1 names the four uncompacted samples first); the table order was used for numbering. I1-I12 match S1-S12. Labels are those of Table 2.
- Fig. 5b legend prints "AC-BF100" for AC-BF1000 (typo; read as AC-BF1000, same black series as in Table 2).
- Non-activated intermediates BF900, BF1000, CB700, CB850 are named in section 2.1 with no characterization and no H2 value: no row.

## Figure digitization (page image main-6.png 1241x1625 px; panel crops with legend and panel letter whitened in work copies; tool digitize_figure.py v2.1 markers mode, tolerance 40, 3-px opening)

Calibration (page pixel coordinates, tick centroids from pixel rows/columns): panel a x 0 at 311.09, 20 at 607.71, y 0 at 1135.063, 7 at 909.43; b x 311.9 / 608.0, y 1410.037 / 1184.41; c x 669.0 / 967.0, y 1138.34 / 912.0; d x 668.98 / 967.0, y 1414.052 / 1187.77. Third-tick verification (x = 10, y = 3) predicted within 0.11% in every panel. Step 6 check against the Table 2 value at the highest digitized pressure: all 10 archives PASS (differences 0.2% to 1.1%).

Series colours: black #000000, red #ee322a, blue #3852a4. Draw order is black, red, blue, so blue is on top and black is most hidden.

| Sample | Fig. | Archive | markers extracted | rows written | notes |
|---|---|---|---|---|---|
| S1 AC-BF900 | 5a black | HYC-0072_Fig5a_AC-BF900.json | 19 (5.02-19.93 bar) | 18 + Table row | markers at 1.5, 2, 3, 4 bar and the p < 1.5 bar cluster are overdrawn by red and blue markers and were not separated |
| S2 AC-BF900@5Ton | 5a red | HYC-0072_Fig5a_AC-BF900_5Ton.json | 23 (1.55-19.95) | 22 + Table row | p < 1.5 bar cluster not separated |
| S3 AC-BF900@10Ton | 5a blue | HYC-0072_Fig5a_AC-BF900_10Ton.json | 27 (0-19.98) | 25 + Table row | 2 merged blobs rejected (39 px near 0.37 bar, 111 px near 0.9 bar); origin marker digitized at 6e-5 bar, -0.0051 wt% is outside the calibrated axis range (tool: extrapolation), not written |
| S4 AC-BF1000 | 5b black | none | 0 | Table row only | only apex tips (1-3 px) show above the red/blue markers; tool finds no marker at opening 3 and merges tips with the connecting line at opening 1; no archive |
| S5 AC-BF1000@5Ton | 5b red | none (test run kept in work dir) | 3 near p = 0 only | Table row only | red markers hidden under blue; the 3 detections (0.007 bar/0.187, 0.007/0.001, 0.041/0.575) cannot be checked against any stated value, so the archive was not released and no row written |
| S6 AC-BF1000@10Ton | 5b blue | HYC-0072_Fig5b_AC-BF1000_10Ton.json | 25 (0.04-19.97) | 24 + Table row | 2 merged blobs rejected (35 px near 0.36 bar, 105 px near 0.86 bar) |
| S7 AC-CB700 | 5c black | HYC-0072_Fig5c_AC-CB700.json | 23 (1.51-20.03) | 22 + Table row | 1 merged blob rejected (31 px near 1.1 bar); 20 bar marker is 0.034 bar beyond the x = 20 axis (tool flags it as outside range), used only in the Table row note |
| S8 AC-CB700@5Ton | 5c red | HYC-0072_Fig5c_AC-CB700_5Ton.json | 20 (0-20.0) | 17 + Table row | markers at 1.5-5 bar hidden under blue; two markers on the y axis not written (one at p = 0.0 bar, 0.304 wt%: schema rejects p = 0; one at 0.0 bar, -0.0101 wt%, outside axis range) |
| S9 AC-CB700@10Ton | 5c blue | HYC-0072_Fig5c_AC-CB700_10Ton.json | 24 (0-19.97) | 22 + Table row | 2 merged blobs rejected (61 px near 0.06 bar, 209 px near 0.8 bar); first marker on the y axis (p = 0.0, 0.558 wt%) not written (schema rejects p = 0); the blue curve in Fig. 5c is drawn twice (two strokes 1-2 px apart, converging above 18 bar), blobs are larger than in other panels and each centroid is of the combined blob |
| S10 AC-CB850 | 5d black | HYC-0072_Fig5d_AC-CB850.json | 29 (0.001-20.0) | 28 + Table row | 1.5 bar marker not separated |
| S11 AC-CB850@5Ton | 5d red | HYC-0072_Fig5d_AC-CB850_5Ton.json | 18 (6.04-19.97) | 17 + Table row | markers below 6 bar hidden under blue/black |
| S12 AC-CB850@10Ton | 5d blue | HYC-0072_Fig5d_AC-CB850_10Ton.json | 24 (0.27-19.97) | 23 + Table row | first marker (0.27 bar, n = 9 px) is small, confidence 2 |

Marker counts versus plot: the counts in the table are what the tool separated, not what is on the plot. Markers that overlap (p < 1.5 bar in every panel) or are overdrawn by another series are not separable at this resolution, and no value was taken for them. In the 20 bar rows the digitized value minus the Table 2 value ranged from -1.1% to +0.7%.

isotherm_point_count is approximate. Shared pressure grid read from the separable series: 1.5, 2, 3, 4, 5, 6, 7, 8, 8.5, 9, 10 to 18 in steps of 1, 18.5, 19, 19.5, 20 bar = 23 markers, counted for every series (markers hidden at these pressures counted because the line passes through and a marker of another series sits at that pressure; in Fig. 5b the black apex tips are visible at all 23 pressures). Added for p < 1.5 bar: resolved markers of that series plus each rejected blob counted as max(2, round(blob px / median blob px of the series)). Counts: I1 23, I2 23, I3 34 (23 + 4 + 2 + 5), I4 24 (23 + one black marker visible near 0.4 wt% at the y axis), I5 26 (23 + 3), I6 35 (23 + 3 + 2 + 7), I7 25, I8 25, I9 34 (23 + 2 + 2 + 7), I10 30 (23 + 7 markers below 1.5 bar), I11 23, I12 24. Any series may have more markers below 1.5 bar than counted.

## Seen but not extracted

- CO2 uptake at 25 C and 1 bar (Table 2, third column, 12 values, 1.6 to 2.4 mmol g-1; also abstract, section 3.3, summary): not H2.
- Fig. 1 (XRD), Figs. 2 and 3 (N2 sorption isotherms), Fig. 4 (PSD): no H2 uptake; no H2 value shown that tables and text do not give.
- Introduction values from other work (about 20 g l-1 at -196 C and 40 bar [44,45]; about 30 g l-1 at 40 bar [48]; 30-40 g l-1 at 45-60 bar [48,49]; 35 g l-1 at 60 bar and 29 g l-1 at 40 bar for CDC [50,51]): other authors' materials, not measured here.
- Repeats of Table 2 values in the abstract, section 3.2 and summary (6.2, 6.5, 5.7 wt%; 42.3 g l-1; about 32 vs 27.4 g l-1 for AC-BF1000): same measurements, recorded once on the Table 2 rows. "Up to 70%" improvement (42.3 vs 24.8 g l-1) is a derived comparison, not a row.
- Text/table conflict: section 3.2 says the volumetric uptake of "sample AC-CB700" rises from 24.8 to 38.8 and 42.3 g l-1; Table 2 gives these values to AC-BF900 (6.2 wt% x 0.4 g cm-3 = 24.8). Table 2 used.
- Table 2 internal inconsistency: AC-CB700 6.2 wt% x 0.45 g cm-3 = 27.9 g l-1 but 26.5 g l-1 is printed (all other rows agree with wt% x packing density within rounding). Printed values stored.
- Digitized but not written: a_blue origin marker (6e-5 bar, -0.0051 wt%), c_red origin marker (0.0 bar, -0.0101 wt%), c_red marker (0.0 bar, 0.304 wt%), c_blue first marker (0.0 bar, 0.558 wt%): outside the calibrated range or pressure 0.0, which the schema rejects.
- H2 degassing duration "4-6 h" is a range: degas_duration_h left empty. Sample mass for H2 not stated (the 0.25 g in section 2.1 is the compaction charge). Skeletal density not stated (1.5-1.8 g cm-3 is the buoyancy-correction assumption, in free_volume_calibration).
- Derived percentages in text (micropore share 75-97% of area, above 54% of pore volume, +4%, +16%, 14%, 18%): not H2 values.
