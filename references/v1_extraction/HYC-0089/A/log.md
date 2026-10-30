# HYC-0089 extraction log (extractor A)

Paper: Agarwal, Noh, Schwarz, Davini, Carbon 25(2), 219-226 (1987). Main article only (no supplementary file). 91 rows written, all `figure_digitized`.

## Sources used

- Table 1 (journal p. 220, main.txt and main-2.png): N2 BET surface area and total oxygen content of the nine commercial activated carbons. No H2 uptake in the table. Used for the characterization columns of every row (BET area, oxygen content in `functional_groups` and `material_description`). Sample labels 1-9 = Table 1 numbers = the digits on Figs 1 and 2.
- Experimental text (p. 219-220): 78 K; Cahn 1000 high pressure recording electrobalance; samples 100-200 mg (a range, so `sample_mass_mg` left empty); degassing 393 K, 18 h, 1e-8 Pa, then flowing He 15 min; gases 99.9999% pure; buoyancy corrections with blank runs, sample volume from manufacturer skeletal densities (1.8-2.2 g/ml) and ideal-gas H2 density; replicate runs, "maximum error was less than 2%". Washing (Soxhlet, distilled water, 5 h, dried 393 K) put in `purification_method`. N2 BET areas on a Quantasorb Quantachrome system, P/P0 range not stated.
- Fig. 1 (journal p. 222, main-4.png), samples 1-5: digitized, 51 markers.
- Fig. 2 (journal p. 222, main-4.png), samples 6-9: digitized, 40 markers. The caption says "as given in Table 2", but the digits 6-9 can only be Table 1 samples (Table 2 numbers samples 1-5 within each carbon). Coded as Table 1 samples 6-9. The text says Figs 1 and 2 show "the nine commercial samples".

## Digitization method (Figs 1 and 2)

- Both figures are black on white with the series marked by digit glyphs (1-9) and line styles, so no colour separates series. Each series was isolated by rectangular windows (marker column +-6 px, glyph rows) placed round its digit markers; everything outside the windows was set to white in a copy of the page image saved in the work directory. The windows only isolate the glyphs; every position and value comes from `digitize_figure.py extract --mode markers`.
- The masked page image was enlarged 4x (bicubic, threshold 128) so the glyph strokes survive the tool's 3-px opening; calibrations were scaled the same way (px_new = 4 px_old + 1.5). `--marker-min-px 300` removes line stubs (largest stub 141 px, smallest glyph blob 531 px). Result: exactly one blob per window, 91 blobs, equal to my marker count on the plot (S1 10, S2 11, S3 10, S4 10, S5 10, S6 10, S7 11, S8 9, S9 10). Cross-check at native resolution (opening off): 79 windows gave a single blob, max |dy| 0.097 g/kg (0.0097 wt%), median 0.007 g/kg; the rest fragmented the glyph.
- Calibration, Fig. 1: x 0 atm at px 232.51 and 40 atm at 943.48; y 5.0 at px 692.79 and 25.0 at 174.65; third ticks x = 20 (px 588.58, predicted 20.033, 0.16%) and y = 15.0 (px 432.88, predicted 15.032, 0.22%). Fig. 2: x 0 at 192.11 and 40 at 966.9; y 12 at 1412.58 and 33 at 923.21; third ticks x = 20 (px 580.49, 0.25%) and y = 21 (px 1204.11, 0.26%). Tick pixel positions are intensity-weighted centroids of the tick marks.
- Units: y axis is "gm of hydrogen per kg of activated carbon" (= mg/g); wt% = 0.1 x g/kg, stored with W1 / computed_from_other_unit. Pressure axis in atm, converted x1.01325. The pressure gauge is a 0-2000 psig model, but the plotted axis is labelled atm and the paper never calls it gauge, so taken as absolute.
- Archives are in `digitizations/` (Fig1_sample1-5.json, Fig2_sample6-9.json); their status is `unchecked` because the tool's `check` needs a numerical uptake printed in the paper at a stated pressure, and the paper prints none. Instead, qualitative consistency: the digitized maxima fall at 15-30 atm (text: "maximum between 25-30 atmospheres"; sample 9 peaks near 15-20 atm, sample 5 near 20 atm), and the 1 atm and 25 atm values agree with the points plotted in Fig. 3 on visual comparison (nothing recorded from Fig. 3).
- Markers lie on the 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40 atm grid; digitized pressures differ from the grid by up to 0.15 atm (glyph centroid asymmetry) and are stored as digitized.
- Marker pressures present per sample: S1, S3, S4: 1, 2, 5, 10-40 (no 3 atm marker); S2: 1, 2, 3, 5, 10-40; S5: 1, 3, 5, 10-40 (no 2 atm marker); S6: 1, 3, 5, 10-40 (no 2 atm); S7: 1, 2, 3, 5, 10-40; S8: 1, 3, 5, 10, 15, 20, 25, 30, 40 (no 2 or 35 atm); S9: 1, 2, 5, 10-40.

## Markers that could not be separated (rows carry extraction_confidence 2 and a note)

- Samples 2 and 5, 3 atm and 5 atm: the glyphs coincide; the blob matches the pixel-wise union of a clean "5" and a clean "2" from the 10 atm markers (a lone "5" does not). One blob digitized, centre assigned to both (M13/M14 and M43/M44). That sample 2 has a 3 atm marker and sample 5 has no 2 atm marker is my reading of the glyphs; the 2 atm glyph is a clean "2".
- Samples 4 and 5, 25, 30, 35 and 40 atm: "4" and "5" glyphs overlap (offset 0 to 5 px, up to 0.2 g/kg). One blob each, centre assigned to both (M38-M41 and M48-M51).
- Samples 6 and 9, 15 atm: "6" and "9" overlap (offset about 4 px). One blob, assigned to both (M56, M86). At 10 atm the two glyphs touch and were cut at row 1147 (not marked as joint).
- Sample 7 at 2 atm: the "7" top bar and tail are visible under the "9" of sample 9 (M63, confidence 2). Sample 9 at 1 atm sits on the x-axis line and below the lowest labelled y tick (12): y is a linear extension of the calibrated axis (M82, confidence 2).
- Sample 2 values of about 25.1-25.2 g/kg lie above the highest labelled y tick (25.0) of Fig. 1 (tool flags them as extrapolations, but they are inside the plotted axis).
- Stacked glyphs cut by row windows: sample 2 / sample 5 at 1 atm and 20 atm, sample 4 / sample 5 at 15 atm.

## Seen but not extracted

- Fig. 3 (p. 223): uptake at 1 and 25 atm against BET area for the nine samples, plus two straight fit lines. Not an isotherm, not digitized. These 18 values are the same measurements as the 1 and 25 atm markers of Figs 1-2 (already rows). No numbers printed.
- Fig. 4 (p. 224), Fig. 5 (p. 224), Fig. 6 (p. 225): uptake at 1, 5, 10 and 25 atm against meq NaOH/100 g for the oxidized variants of carbon 2 (5 markers per pressure), carbon 4 (4) and carbon 5 (3), that is 48 uptake values at 78 K for samples that appear in Table 2. Not isotherms, not digitized; the tables and text do not give them. Fig. 5 text: "enhancement of about 20% by weight is realized on a well oxidized and highly acidic carbon" (a relative increase, not an uptake value, not extracted).
- Table 2 (p. 221; main-3.png, rotated): characterization of the treated carbons, no H2 uptake in the table, so no rows. Columns: oxidation time (min), % oxygen, temperature (K), N2 surface area (m2/g), HCl / NaOH / Na2CO3 / NaHCO3 (meq/100 g).
  - Carbon 2: 1 H2-treated only, area 1160, 51.90/1.98/0.70/0.50; 2 as received washed, 1159, 44.30/5.90/0.48/0.00 (= Table 1 sample 2); 3 oxidized 30 min, 2% O2, 873 K, 1097, 38.80/7.73/0.97/0.49; 4 oxidized 20 min, 2% O2, 973 K, 1231, 53.00/10.60/1.50/0.50; 5 oxidized 180 min, 10% O2, 623 K, 1122, 37.40/23.24/4.60/1.34.
  - Carbon 4: 1 as received washed, 1559, 32.38/8.89/4.89/4.47 (= Table 1 sample 4); 2 oxidized 10 min, 1% O2, 873 K, 1523, 42.04/16.01/NA/NA; 3 oxidized 20 min, 2% O2, 973 K, 1509, 20.39/32.85/14.83/4.20; 4 oxidized 120 min, 20% O2, 653 K, 1513, 18.56/39.47/23.96/19.30.
  - Carbon 5: 1 as received washed, 1119, 31.20/15.10/NA/NA (= Table 1 sample 5); 2 oxidized 10 min, 20% O2, 673 K, 1090, 32.10/25.03/NA/NA; 3 oxidized 30 min, 20% O2, 673 K, 1093, 25.30/35.05/NA/NA.
- Text: "maximum between 25-30 atmospheres" (location of the maxima, not an uptake value); Menon's predicted maximum at 70.7 atm (theory); "surface areas ... remained the same within experimental error (5%)" (no values); skeletal density range 1.8-2.2 g/ml and sample mass 100-200 mg (ranges for all samples, put in notes only).
- Ash content was measured but no numbers are printed.
- No value for another material, no consensus or multi-sample value, and no value described as previously reported.

## Coding decisions worth a second look

- `basis_stated = false`: the paper defines the observed amount as the difference between adsorbed amount and an equal volume of gas, which is the excess definition, but never names it (excess, absolute or total). `uptake_type = unspecified`; `basis_inferred = excess` by the instrumental default (gravimetric with a stated buoyancy correction, adsorbed phase explicitly not corrected).
- `replicates_reported = true` from "maximum error was less than 2%" (a reproducibility stated in %); `uncertainty_wt_pct` left empty since the figure is relative.
- `area_same_sample = yes`: N2 BET areas were measured on the washed samples (same state as the H2 runs). Oxygen content (by difference) is kept in `functional_groups`, not as a dopant, because the carbons are not doped.
- `measuring_lab_id`: no corresponding author marked, so the first author (Agarwal), first affiliation Syracuse University.
- `h2_purity_pct = 99.9999` is stated for "the gases used".
