# HYC-0078 extraction log (agent A)

Page references: "main p.N" is the page image main-0N.png; the journal page is p.N + 259.

## Extracted from

- Abstract (main p.1): 4.6 mmol/g (1.99 wt%) at 120 kPa and approx. 15.02 mmol/g (5.14 wt%) at 5192 kPa merged with the plotted points (rows M39, M52); BET 579.4 m2/g and total pore volume 0.340 cm3/g used for sample S2.
- Sect. 2 and 3 text (main p.3): instruments (Micromeritics ASAP 2020 to 120 kPa; automated Sievert's PCT Pro to 5192 kPa), 77 K, drying 80 C 12 h then vacuum degassing 24 h (VacPrep 061), activation recipe, N2 isotherms at 77 K for BET; no H2 purity, free-volume calibration, sample mass or degassing temperature stated.
- Table 1 (main p.3): activation conditions (10 % and 40 % NaCl or KCl, w/w) used in activation_method; the "Sample weight (grams)" column is the weight of the product after carbonization of a 3 g shell batch, not an H2 sample mass, so sample_mass_mg is empty.
- Sect. 4.2 text (main p.5): 579 m2/g, average pore size 2.35 nm, total pore volume 0.340 cm3/g for ACNC40-900.
- Sect. 4.3 text (main p.5-6): interlayer spacing 0.355 nm (XRD 2theta = 25 deg, stated for the five-sample set), coded on both samples.
- Table 2 (main p.6): EDS (surface) weight % used for dopant_concentration_wt_pct (N: ACNC10-900 37.41, ACNC40-900 13.81; method coded other = EDS); Na 0.46 and 0.27 wt% only in notes (Na from the NaCl activating agent, not coded as residual catalyst).
- Sect. 4.5 text (main p.7): functional_groups for both samples (C triple bond C near 2100 cm-1 in FTIR; hydroxyl groups reported eliminated); for ACNC40-900 also the Raman assignments (aromatic C=C near 1500, C-N near 1200 cm-1). The Raman band near 600 cm-1 of ACNC10-900 (attributed to Fe or Si) is not a functional group and is not coded.
- Sect. 4.6 text and Conclusion (main p.7-8): 0.98 and 4.6 mmol/g (0.44 and 1.99 wt%) at 120 kPa; 13.69 mmol/g (4.77 wt%) and 15.018 mmol/g (5.14 wt%) at 5192 kPa; each is the same measurement as the last plotted marker of its isotherm (rows M17, M39, M45, M52); basis statement "excess amount" and Eq. 2 (wt% definition, W1 form) taken from here.
- Table 3 (main p.9): rows "Pistachio shells" (579.4 m2/g, 0.204 cm3/g, 1.99 wt% at 120 kPa; 5.14 wt% at 5192 kPa, "This study") merged into M39 and M52; the Table 3 pore volume 0.204 conflicts with 0.340 in the Abstract and Sect. 4.2 (0.340 coded, 0.204 in notes).
- Fig. 9 (main p.7), ACNC10-900 (I1): 29 markers extracted (1 merged into M17, 12 desorption M18-M29, 16 adsorption M1-M16); ACNC40-900 (I2): 10 markers extracted (1 merged into M39, 9 adsorption M30-M38). Archives fig9_ACNC10-900.json and fig9_ACNC40-900.json.
- Fig. 10 (main p.8), ACNC10-900 (I3): 6 markers extracted (1 merged into M45, 5 in M40-M44); ACNC40-900 (I4): 7 markers extracted (1 merged into M52, 6 in M46-M51). Archives fig10_ACNC10-900.json and fig10_ACNC40-900.json. Points are averages of three runs on fresh samples; error bars exist.

## Digitization settings and checks

- Work copies fig9_nolegend.png and fig10_nolegend.png are the page images with the legend box painted white (so legend markers are not read as data); all pixel coordinates are unchanged from the page images.
- Fig. 9 calibration: x 0 kPa at px 720.89, 120 kPa at px 1123.73, check tick 60 kPa at px 922.28 (0.015 % error); y 0 mmol/g at px 1402.52, 5 mmol/g at px 1086.27, check tick 3 at px 1212.56 (0.11 % error). Tick pixels from intensity centroids of the tick marks.
- Fig. 10 calibration: x 0 kPa at px 171.18, 5000 kPa at px 558.98, check tick 2500 at px 365.22 (0.07 % error); y -2 mmol/g at px 1437.81, 18 mmol/g at px 1095.74, check tick 8 at px 1266.78 (0.004 % error).
- Colours and tolerances: Fig. 9 red #ff4846 tol 60 (max marker 20 px), gray #626262 tol 35 (max marker 24 px); Fig. 10 black #000000 tol 60, red #ff0000 tol 160 (tol 160 is needed so the red marker split by an error-bar line at the origin is read as one marker). Oversize blobs (several merged markers) were rejected with --marker-max-px and are recorded in the archives.
- Step-6 checks passed against the printed values: Fig. 9 red at 120 kPa digitized 4.696 vs printed 4.6 mmol/g (2.1 %); Fig. 9 gray 0.988 vs 0.98 (0.85 %); Fig. 10 red at 5187 kPa 15.008 vs 15.018 (0.07 %); Fig. 10 black 13.687 vs 13.69 (0.02 %).
- The tool flags the Fig. 9 marker at 120.08 kPa and the Fig. 10 markers at 5187.2 and 5190.4 kPa as outside the calibrated tick range (they lie beyond the highest labelled tick on a linear axis); values kept, they match the printed 120 kPa and 5192 kPa.

## Markers seen but not extracted (could not be separated)

- Fig. 9 ACNC40-900 (red): the adsorption branch 0-30 kPa is a continuous band of overlapping markers (merged blob, 1243 px, centroid 7.8 kPa, 2.27 mmol/g, not a marker centre); the desorption markers at about 2.5, 5, 10, 20 and 30 kPa sit on that band and merge with it. Not extracted.
- Fig. 9 ACNC40-900 (red): adsorption and desorption markers at the same pressure overlap in pairs and the tool returns one blob each, rejected: about 40.1 (4.105), 50.0 (4.242), 60.1 (4.348), 70.1 (4.429), 80.2 (4.500), 89.6 (4.562; two markers side by side), 99.7 (4.610), 109.7 (4.649) kPa (mmol/g in brackets are blob centroids, not marker centres). The whole desorption branch of this isotherm is therefore not extracted, and the adsorption markers at about 40, 50, ..., 110 kPa are not extracted either.
- Fig. 9 ACNC10-900 (gray): the adsorption branch 0-30 kPa is a continuous band of overlapping markers (483 px blob centroid 14.5 kPa, 0.59 mmol/g); the pair at 80 kPa (blob 28 px, centroid 0.953 mmol/g, two squares stacked) is merged. Both rejected, not extracted.
- Fig. 9 isotherm_point_count is left empty for I1 and I2 because the markers of the dense bands cannot be counted. The 0-30 kPa bands are not treated as lines without markers (no curve-mode rows).
- Fig. 9 branch assignment (not printed numerically): the paper labels the sparse markers at low pressure "Desorption" and the dense band "Adsorption"; at pressures above 30 kPa the lower marker of a same-pressure pair and the single markers at 35, 45, ..., 115 and 120 kPa form the lower, monotonic adsorption curve, and the upper markers (including 88.65, 98.75 and 108.61 kPa for gray) the desorption curve. The 120 kPa marker is coded adsorption (last adsorption point; the printed 120 kPa values are equilibrium uptakes with no desorption statement).
- Fig. 10 ACNC10-900 (black): the first marker (about 0.2 bar, about 0.1 mmol/g) is partly hidden behind the red marker of ACNC40-900; the tool returns only an 8 px sliver (17 kPa, 0.255 mmol/g) that is not a marker centre. Not extracted; counted in isotherm_point_count (7 markers per Fig. 10 series).
- Fig. 10 error bars (in mmol/g, not wt%) are not digitized and uncertainty_wt_pct is empty; replicates_reported = true for I3 and I4.

## Values seen but not rows

- Fig. 4a (N2 isotherms at 77 K of all five samples) and Fig. 4b (BJH pore size distribution): not H2, not digitized.
- Fig. 1, 2, 3, 5, 6, 7, 8, 11: schematics, SEM, XRD, EDS, FTIR, Raman; no H2 values.
- Samples with characterization but no H2 uptake value, no rows: Pi-char (Table 1 weight 0.1373 g; Table 2 C 71.36, N 27.86, K 0.27, Ca 0.51 wt%), ACKC10-900 (0.2204 g; C 72.66, K 23.15, Ca 4.19), ACKC40-900 (0.3074 g; C 79.86, N 16.31, K 2.86, Ca 0.37, Cl 0.59), with N2 isotherms in Fig. 4a and no printed BET area.
- Sect. 4.2 prints "the ratio of microporous surface area to the overall surface area exhibited 279 m2/g and 579 m2/g" and "pore volume exhibited an increase from 0.0035 to 0.17 cm3/g (shown in Fig. 4b)" without saying which sample or quantity each belongs to: not coded (no micropore area, micropore volume or ACNC10-900 area).
- Literature comparison values (other groups' measurements, not this paper's own samples; the "values reported before" rule is applied only to the paper's own samples): Table 3 rows sawdust 3.03 wt% 77 K 100 kPa [10], Typha orientalis 0.61 wt% 298 K 8000 kPa [87], Palimera sprout 1.06 wt% 298 K 1500 kPa [88], pinecones 5.5 wt% 77 K 8000 kPa [89], food waste 6.15 wt% 77 K 2300 kPa [90], bark and Camellia shell 3.01 wt% 77 K 100 kPa [91], onion peel 3.67 wt% 77 K 100 kPa [92], almond shells 2.53 wt% 77 K 2700 kPa [92]; Introduction and Sect. 4.6 values 0.149 wt% (Pinjari, room temperature, 50 bar), 6.8 wt% (Lee, room temperature, 100 bar), 1.67 and 1.11 wt% (Dogan, 5 M ZnCl2 and KOH, 3000 kPa), 0.173 wt% (Attia, room temperature) and 4 wt% (77 K, 20 bar), 0.31 and 2.53 wt% (Bicil), 0.83 wt% (Jin, room temperature, 100 bar). Also surface areas and pore volumes of other studies in the Introduction.

## Coding decisions worth a second look

- Sample numbering: S1 = ACNC10-900, S2 = ACNC40-900, in order of first appearance among the samples that have rows (Pi-char, ACKC10-900 and ACKC40-900 have no H2 values and no rows).
- material_class doped_carbon with dopant N: the authors describe "self-nitrogen doping" (Sect. 4.6) and report EDS N of 13.81 and 37.41 wt% (surface EDS, implausibly high); the alternative coding is activated_carbon. Na (0.27 and 0.46 wt%) is not coded as composite or residual metal.
- synthesis_method chemical_activation: NaCl impregnation and carbonization at 900 C are one step ("one-step activation process").
- wt% convention: Eq. 2 defines wt% as H2 mass per AC mass x 100 (W1), so the printed wt% are coded W1/stated, but they do not match W1 from the printed mmol/g (0.44 vs 0.198, 1.99 vs 0.927, 4.77 vs 2.76, 5.14 vs 3.03 wt%); the validator warns on M17, M39, M45, M52 (unit-consistency failure of the paper). Digitized points have mmol/g only, wt% computed as W1.
- Basis: "excess amount" is named but not defined, so basis_stated false, basis_inferred excess for all four isotherms, uptake_type excess.
- measurement_method volumetric_sieverts for the ASAP 2020 isotherms is inferred from the instrument type (the paper names "Sievert's" only for the PCT Pro); instrument_identified true for ASAP 2020, false for the PCT Pro (manufacturer not named).
- measuring_lab_id: corresponding author N. V. Salim, Swinburne University of Technology; the acknowledgements thank two non-authors for access to the H2 adsorption equipment without naming an institution, so no other laboratory is coded.
- Degassing: oven drying at 80 C for 12 h then vacuum degassing for 24 h; degas_duration_h = 24, degas_temperature_c empty because the vacuum-degassing temperature is not stated (the 300 C, 12 h degassing is for the N2 BET analysis).
- surface_area_probe_gas N2 for the BET of ACNC40-900 (N2 isotherms at 77 K); area_same_sample yes (same labelled sample and treatment); BET range and consistency criteria not stated. ACNC10-900 has surface_area_method not_reported.
- Pore volume and pore diameter methods left unspecified for ACNC40-900 (only the pore size distribution is named as BJH); pore_volume_probe_gas N2.
- dopant_concentration_method other (EDS).
- "approximately 15.02 mmol/g" in the Abstract is coded exact: the text prints 15.018.
