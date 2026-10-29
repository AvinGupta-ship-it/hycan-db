# HYC-0078 extraction log (extractor B, 2026-10-29)

Elyasi et al. 2025, Int. J. Hydrogen Energy 119, 260-270. Input: 11 page images (main-01 to main-11 = journal pp. 260-270); no supplementary file. 70 rows written.

## Samples

- S1 Pi-char, S2 ACNC10-900, S3 ACNC40-900, S4 ACKC10-900, S5 ACKC40-900 (order of Table 1, p. 262). Only S2 and S3 have H2 uptake values; S1, S4, S5 get no rows (characterization listed below).
- Label choice for S3: Table 3 (the only table that reports its uptake) identifies it in the column "Precursor" as "Pistachio shells". That column names the precursor, not the sample, so the sample label "ACNC40-900" (Fig. 9 and Fig. 10 legends, text) is used. The Conclusion misprints the labels as "ANC10-900", "ANC40-900" and "ANC40".

## Sources extracted from

- Fig. 9, p. 266 (main-07): H2 adsorption/desorption at 77 K up to 120 kPa (Micromeritics ASAP 2020), ACNC10-900 (grey squares, isotherm I1) and ACNC40-900 (red circles, I2). Separable markers digitized, both branches: I1 18 adsorption (35-120 kPa) + 13 desorption (2.4-109 kPa); I2 18 adsorption (35-120 kPa) + 8 desorption (40-109 kPa). Branches assigned by the paper's arrows ("Desorption" on the upper trace, "Adsorption" on the lower trace) and by pressure for the diagonal pairs (desorption at about 89, 99, 109 kPa; adsorption at about 90, 100, 110 kPa).
- Fig. 10, p. 267 (main-08): H2 adsorption at 77 K up to 5192 kPa (Sievert's PCT Pro), averages of three measurements with error bars. ACNC10-900 (black squares, I3): 6 of 7 markers digitized; ACNC40-900 (red circles, I4): 7 of 7.
- Section 4.6 text, p. 267: "increased from 0.98 to 4.6 mmol g-1 (0.44-1.99 wt%)"; "maximum adsorption for ACNC10-900 at 5192 kPa was 13.69 mmol g-1 (4.77 wt%) and for ACNC40-900 was 15.018 mmol g-1 (5.14 wt%)". Merged with the highest-pressure markers of Fig. 9 / Fig. 10 (rows M18, M49, M63, M70).
- Abstract, p. 260 (4.6 mmol g-1, 1.99 wt%, 120 kPa; approximately 15.02 mmol g-1, 5.14 wt%, 5192 kPa), Conclusion, p. 267 (0.98 and 4.6 mmol g-1 at 120 kPa; 13.69 and 15.02 mmol g-1 at 5192 kPa) and Table 3, p. 268 (rows "Pistachio shells ... This study": 1.99 wt% at 77 K, 120 kPa; 5.14 wt% at 77 K, 5192 kPa): the same four measurements, recorded on the same merged rows, not as separate rows. 15.018 (Section 4.6) stored; 15.02 elsewhere.
- Section 3, p. 262: methods (TriStar II N2 BET, degas 300 C 12 h; ASAP 2020 and PCT Pro for H2; H2 samples dried 80 C 12 h then degassed under vacuum 24 h on VacPrep 061, degassing temperature not stated). Eq. (2), p. 267: wt% definition with the sorbent mass alone in the denominator (W1), coded wt_pct_convention = W1, source stated on the printed-wt% rows.
- Section 2.1, p. 262 and Table 1: synthesis (NaCl 10 % / 40 % w/w soak 1 day, air-dry 3 days, N2, 10 C/min to 900 C, 30 min).
- Abstract, Section 4.2 (p. 264) and Conclusion: ACNC40-900 BET 579.4 m2/g (N2), total pore volume 0.340 cm3/g, average pore size 2.35 nm.
- Table 2, p. 265 (EDS weight %): ACNC10-900 C 62.13, N 37.41, Na 0.46; ACNC40-900 C 85.92, N 13.81, Na 0.27.
- Section 4.3, p. 265: interlayer spacing 0.355 nm, stated once for all five samples.
- Section 4.5, p. 266: Raman bands for ACNC40-900 (C=C 1500 cm-1, C-N 1200 cm-1) as functional_groups.

## Problems recorded on the rows

- Unit-consistency failure on every value printed in two units: printed wt% matches neither W1 nor W2 computed from the printed mmol/g (0.98 mmol/g -> W1 0.198 wt%, printed 0.44; 4.6 -> 0.927, printed 1.99; 13.69 -> 2.760, printed 4.77; 15.018 -> 3.027, printed 5.14). Both printed values stored; validator warns "mmol/g and wt% inconsistent" on M18, M49, M63, M70 (expected).
- Pore volume conflict for ACNC40-900: text and Abstract give total pore volume 0.340 cm3/g (stored); Table 3 prints "Pore Volume" 0.204 cm3/g.
- Average pore size 2.35 nm printed without its method; equals 4V/A from 0.340 cm3/g and 579.4 m2/g; coded pore_diameter_method = unspecified.
- Basis: "The raw data are obtained in the excess amount of hydrogen adsorbed" (p. 266), excess named but not defined: basis_stated = false, basis_inferred = excess, uptake_type = excess on all four isotherms.
- PCT Pro manufacturer not named: instrument_identified = false for I3, I4. No free-volume calibration or H2 purity stated anywhere.
- H2 measurement laboratory: Acknowledgements thank Prof. Eric May and Dr. Ehsan Sadeghi Pouya "for providing access to the hydrogen adsorption equipment" with no institution printed and neither is a co-author, so measuring_lab_id = corresponding author's group (Salim group, Swinburne University of Technology).

## Digitization (scripts/digitize_figure.py extract --mode markers)

- Fig. 9: x calibrated on ticks 0 kPa (720.89 px) and 120 kPa (1123.73 px), checked at 60 kPa (922.28 px, predicted 59.991); y on 0 (1402.52 px) and 5 mmol/g (1086.27 px), checked at 3 (1212.56 px, predicted 3.003). Tick positions from intensity-weighted centroids of the tick pixels. Colours: grey #646464 tol 40; red #ff4846 tol 40.
- Fig. 10: x on 0 kPa (171.29 px) and 5000 kPa (559.00 px), checked at 2000 (326.39 px); y on -2 (1437.81 px) and 18 mmol/g (1095.74 px), checked at 8 (1266.78 px). Colours: black #000000 tol 40; red #ff0000 tol 160 (the wider tolerance includes the dark-red pixels where error-bar lines cross the red markers, without which the 0 kPa red marker breaks apart and is lost; black, grey and anti-aliased pink stay outside it).
- Archives (out/digitizations/): fig9_ACNC10-900.json and fig9_ACNC40-900.json hold every separable single marker; touching or overlapping marker pairs, which the tool merges into one blob (recorded there as rejected "too large"), were split by re-running with a narrow ROI on each half: fig9_ACNC10-900_80kPa_{upper,lower}.json and fig9_ACNC40-900_{40kPa,50kPa,60kPa,70kPa,80kPa}_{upper,lower}.json, fig9_ACNC40-900_{89-90kPa,99-100kPa,109-110kPa}_{left,right}.json. For pairs that overlap (red 60, 70, 89-90, 109-110 kPa) the shared row or column is included in both halves; the red 80 kPa halves use --open-px 1 because a 3-px opening erases a 2-3 px tall half. Split centroids may be biased by up to about 0.5 px (about 0.01 mmol/g; 0.15 kPa); extraction_confidence 2 for overlapping pairs, 3 for touching pairs. So there are more archive files than series.
- Marker counts in the digitized regions match the counts on the plot: Fig. 9 grey 31 markers (outside the dense band) = 29 single + 2 split; Fig. 9 red, 33-122 kPa, 26 markers = 10 single + 16 split; Fig. 10 black 6 of 7 (one hidden, below); Fig. 10 red 7 of 7.
- digitize_figure.py check against stated values: fig9_ACNC10-900 at 120 kPa vs 0.98 (+0.82 %), fig9_ACNC40-900 at 120 kPa vs 4.6 (+2.08 %), fig10_ACNC10-900 at 5186.9 kPa vs 13.69 (-0.02 %), fig10_ACNC40-900 at 5190.1 kPa vs 15.018 (-0.02 %): all pass (status "passed"). The split archives hold no point the paper states and remain "unchecked".
- The highest-pressure markers lie slightly beyond the last labelled tick (Fig. 9: 120.23 and 120.08 kPa vs tick 120; Fig. 10: 5187 and 5190 kPa vs tick 5000) and are flagged by the tool as extrapolated; all four are merged with printed text values.

## Values seen but not extracted

- Fig. 9, both samples: the adsorption branch from 0 to about 31 kPa is drawn as a continuous band of overlapping markers (dense data points). Individual markers cannot be separated or counted, so none were digitized (the tool rejects the band as one 234-px blob for grey), and isotherm_point_count is left empty for I1 and I2.
- Fig. 9, ACNC40-900: the desorption markers at about 2.5, 5, 10, 20 and 30 kPa (and the cluster at about 30-31 kPa where the band ends) sit on the dense adsorption band and show only as bumps on it; not separable, not digitized.
- Fig. 9, ACNC10-900: any markers below 2 kPa lie under the red ACNC40-900 band at 0 kPa and cannot be seen.
- Fig. 10, ACNC10-900: the marker at 0 kPa (about 0.1 mmol/g) is hidden behind the ACNC40-900 marker; only its top edge is visible, so its centre cannot be located. Counted in isotherm_point_count = 7, not digitized.
- Fig. 10 error bars (both samples; about +/-1 mmol/g on ACNC40-900 at 5192 kPa) not digitized; replicates_reported = true from the error bars and "measured three times for each sample".
- Table 3, p. 268: eight literature rows (Sawdust [10], Typha orientalis [87], Palimera sprout [88], Pinecones [89], Food waste [90], Bark and Camellia shell [91], Onion peel [92], Almond shells [92]) are other papers' values, not this paper's measurements.
- Literature values in the text: Pinjari 0.149 wt% (RT, 50 bar), Lee 6.8 wt% (RT, 100 bar), Dogan 1.67 / 1.11 wt% (5 M ZnCl2 / KOH activated carbons), Attia 0.173 wt% (RT) and 4 wt% (77 K, 20 bar), Bicil 0.31 wt% (RT, 50 bar) and 2.53 wt%, Jin 0.83 wt% (RT, 100 bar); surface areas from refs [38]-[42]; DOE targets (5.5 wt%, 0.40 kg/L). Not this paper's measurements.
- Characterization of samples with no H2 value: Pi-char (EDS C 71.36, N 27.86, K 0.27, Ca 0.51 wt%), ACKC10-900 (C 72.66, K 23.15, Ca 4.19 wt%), ACKC40-900 (C 79.86, N 16.31, K 2.86, Ca 0.37, Cl 0.59 wt%); their N2 isotherms in Fig. 4a and PSDs in Fig. 4b; Table 1 product weights (Pi-char 0.1373, ACKC10-900 0.2204, ACKC40-900 0.3074 g).
- Table 1 product weights for ACNC10-900 (0.6076 g) and ACNC40-900 (0.6342 g): weights after carbonization, not the H2 sample mass; not stored as sample_mass_mg.
- Section 4.2, p. 264: "the ratio of microporous surface area to the overall surface area exhibited 279 m2 g-1 and 579 m2 g-1" and "the pore volume exhibited an increase from 0.0035 to 0.17 cm3 g-1 (shown in Fig. 4b)": not tied to a sample (279 could be a micropore area of ACNC40-900 or the area of another sample), not stored. No surface area or pore volume is printed for ACNC10-900 (surface_area_method = not_reported).
- Section 4.4: raw pistachio-shell composition (C 44.89, H 5.66, N 0.53, S 0.97, O 47.95 %) and K about 1646 mg/kg, cited from refs [72], [73]; not samples of this paper.
- Figs. 1, 2, 3, 5, 6, 7, 8, 11 (schematics, SEM, XRD, EDS spectra, FTIR, Raman) and Fig. 4 (N2 isotherms, PSD): no H2 uptake values.
- No non-carbon sorbent (hydride, MOF, zeolite) is measured in the paper.
