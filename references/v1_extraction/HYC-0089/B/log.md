# HYC-0089 extraction log (agent B, 2026-10-29)

## Sources extracted from

- Table 1 (main-2.png, p. 220): BET surface area (Nitrogen BET, Quantasorb Quantachrome, per text p. 219-220) and oxygen content (%) for samples 1-9. Used as characterization on every row of samples S1-S9. No H2 values in this table.
- Table 2 (main-3.png, p. 221, printed rotated): oxidation conditions, surface area and back-titration results (HCl, NaOH, Na2CO3, NaHCO3, meq/100gm) for Carbons 2, 4 and 5. The "as received, washed" rows (Carbon 2 sample 2, Carbon 4 sample 1, Carbon 5 sample 1) are Table 1 samples 2, 4, 5 (same areas 1159, 1559, 1119); their titration values are in `notes` of S2, S4, S5. No H2 values in this table.
- Experimental text (main-1.png p. 219, main-2.png p. 220): sample washing, BET instrument, elemental analysis, Cahn 1000 electrobalance, 78 K, 100-200 mg samples, degas 10^-8 Pa / 393 K / 18 h, He flush, 99.9999% gases, Engelhard deoxo, MKS Baratron 222B and Data Instrument EA 0-2000 psig gauges, buoyancy corrections, skeletal densities 1.8-2.2 gm/ml from manufacturers, replicate experiments with maximum error < 2%. Coded on every row.
- Text p. 222-223 (main-2.png, main-5.png): description of the gravimetric observed amount (difference relative to gas in the same volume) and "buoyancy corrections for the adsorbed phase will not be applied". No basis named; basis_stated false, basis_inferred excess (gravimetric with stated buoyancy correction), uptake_type unspecified.
- Fig. 1 (main-4.png, p. 222): 78 K adsorption isotherms, samples 1-5 (numeral markers 1-5), pressure in atm, amount in g H2 per kg carbon. Every marker digitized: sample 1: 10, sample 2: 10, sample 3: 10, sample 4: 10, sample 5: 10 markers. Rows M1-M50. Archives `digitizations/HYC-0089_fig1_sample1.json` ... `_sample5.json`.
- Fig. 2 (main-4.png, p. 222): 78 K adsorption isotherms, samples 6-9 (numeral markers 6-9). Every marker digitized: sample 6: 10, sample 7: 10, sample 8: 9 (no marker at 35 atm), sample 9: 10. Rows M51-M89. Archives `digitizations/HYC-0089_fig2_sample6.json` ... `_sample9.json`.
  - The Fig. 2 caption says the numbers are "the carbon sample as given in Table 2", but Table 2 has no samples 6-9, the text (p. 220) says Figs 1 and 2 show "the nine commercial samples", and the Fig. 3 surface-area positions match Table 1. Curves 6-9 were mapped to Table 1 samples 6-9; stated in each row's notes.

## Digitization procedure

- Markers are black numerals drawn on black solid, dashed, dotted and dash-dot lines, so colour isolation alone cannot separate them (`colors`: greyscale only). Each numeral was located by template matching on the page image: for each digit, a median template was built from that digit's own instances in the figure (aligned iteratively by normalized cross-correlation, cleaner instances only), and every instance was re-located with it (search window +/-6 px around a visually placed seed). The bounding box of each matched glyph was painted pure red on a copy of the page image, one image per series (work/proc/figN_seriesD_painted.png), and `digitize_figure.py extract --mode markers --color #ff0000 --tolerance 30 --open-px 0` took the centre of each painted marker. Matches were checked on enlarged overlays.
- Fig. 1 calibration (pixel positions from tick-mark profiles): x 0 atm = 232.52 px, 40 atm = 943.47 px, check 20 atm = 588.60 px (error 0.17%); y 5.0 = 692.50 px, 25.0 = 174.33 px, check 15.0 = 432.80 px (error 0.16%).
- Fig. 2 calibration: x 0 atm = 192.10 px, 40 atm = 966.90 px, check 20 atm = 580.48 px (error 0.25%); y 12 = 1412.57 px, 33 = 923.19 px, check 21 = 1204.09 px (error 0.26%).
- Extracted marker counts equal the counted markers for all nine series (10, 10, 10, 10, 10, 10, 10, 9, 10).
- Overlapping markers (positions taken from the template match of each digit; extraction_confidence 2): Fig. 1 numerals 2 and 5 superimposed at 5 atm; 4 and 5 superimposed at 25 and 30 atm and partly overlapping at 35 and 40 atm; numeral 5 at 1 atm distorted. Fig. 2 numerals 6 and 9 superimposed at 15 atm and partly overlapping at 10 atm; numeral 7 at 1 and 3 atm merged with curve lines; numeral 9 at 1 atm sits on the x-axis line. It cannot be excluded that a further marker is hidden under a superimposed one (for example a sample 5 point under the sample 2 numeral at 2 atm in Fig. 1); the counts used are the visible numerals.
- Points beyond the outermost calibration tick (tool flag `outside_axis_range`): all 40 atm points (x up to 40.14 atm), sample 2 points at 15-30 and 40 atm (above the 25.0 tick), sample 9 at 1 atm (11.70, below the 12 tick). The axes are linear; values kept, flagged in notes.
- The archives have status `unchecked`: the paper states no numerical uptake value in its text or tables, so the tool's step-6 check against a stated value could not be run.
- Units: amount in g H2/kg carbon (= mg/g) stored as W1 wt% = 0.1 x value (computed_from_other_unit); pressure atm x 1.01325 to bar, treated as absolute (the paper does not call the plotted pressure gauge).

## Values seen but not extracted

- Fig. 3 (main-5.png, p. 223): amount adsorbed at 1 atm and 25 atm against surface area for the nine samples. Not an isotherm; not digitized. Its points are the same measurements as the 1 and 25 atm points of the Fig. 1-2 isotherms (no new values).
- Fig. 4 (main-6.png, p. 224): amount adsorbed against NaOH titre for Carbon 2 (Table 2 samples 1-5) at 1, 5, 10 and 25 atm. Not an isotherm; not digitized. New values not given in tables or text: uptakes at 1, 5, 10 and 25 atm for Carbon 2 samples 1 (only hydrogen treated), 3, 4 and 5 (oxidized); the as-received point duplicates Fig. 1 sample 2.
- Fig. 5 (main-6.png, p. 224): same plot for Carbon 4 (Table 2 samples 1-4) at 1, 5, 10, 25 atm. Not digitized. New values: Carbon 4 samples 2, 3, 4 (oxidized) at the four pressures.
- Fig. 6 (main-7.png, p. 225): same plot for Carbon 5 (Table 2 samples 1-3) at 1, 5, 10, 25 atm. Not digitized. New values: Carbon 5 samples 2, 3 (oxidized) at the four pressures.
- Text p. 225: "An enhancement of about 20% by weight is realized on a well oxidized and highly acidic carbon depicted in Figure 5" - a relative enhancement, not an uptake value.
- Text p. 223: Menon's estimate that the maximum should occur at 70.7 atmospheres, and "we observe the maximum between 25-30 atmospheres" - pressures, not uptake values.
- Text p. 225: surface areas after oxygen treatment "remained the same within experimental error (5%)" - characterization statement.
- Samples with characterization but no H2 uptake row (their uptakes appear only in Figs 4-6):
  - Carbon 2 sample 1 (only hydrogen treated, 873 K in H2 30 min): surface area 1160 m2/gm; HCl 51.90, NaOH 1.98, Na2CO3 0.70, NaHCO3 0.50 meq/100gm.
  - Carbon 2 sample 3 (30 min, 2% O2, 873 K): 1097 m2/gm; HCl 38.80, NaOH 7.73, Na2CO3 0.97, NaHCO3 0.49.
  - Carbon 2 sample 4 (20 min, 2% O2, 973 K): 1231 m2/gm; HCl 53.00, NaOH 10.60, Na2CO3 1.50, NaHCO3 0.50.
  - Carbon 2 sample 5 (180 min, 10% O2, 623 K): 1122 m2/gm; HCl 37.40, NaOH 23.24, Na2CO3 4.60, NaHCO3 1.34.
  - Carbon 4 sample 2 (10 min, 1% O2, 873 K): 1523 m2/gm; HCl 42.04, NaOH 16.01, Na2CO3 NA, NaHCO3 NA.
  - Carbon 4 sample 3 (20 min, 2% O2, 973 K): 1509 m2/gm; HCl 20.39, NaOH 32.85, Na2CO3 14.83, NaHCO3 4.20.
  - Carbon 4 sample 4 (120 min, 20% O2, 653 K): 1513 m2/gm; HCl 18.56, NaOH 39.47, Na2CO3 23.96, NaHCO3 19.30.
  - Carbon 5 sample 2 (10 min, 20% O2, 673 K): 1090 m2/gm; HCl 32.10, NaOH 25.03, Na2CO3 NA, NaHCO3 NA.
  - Carbon 5 sample 3 (30 min, 20% O2, 673 K): 1093 m2/gm; HCl 25.30, NaOH 35.05, Na2CO3 NA, NaHCO3 NA.
- No non-carbon materials are measured in this paper.
- Not stored as numbers (ranges): sample mass 100-200 mgms; skeletal density 1.8-2.2 gm/ml. Reproducibility "maximum error was less than 2%" is relative, so uncertainty_wt_pct is empty; replicates_reported = true.
