# HYC-0112 extraction log (extractor A, agent A (claude-sonnet-5-5), 2026-10-29)

114 rows written (M1-M114). All value rows are carbon sorbents (CEMC, Pt5CEMC, Pt10CEMC); no non-carbon sorbent was measured for H2.

## Extracted from

- Table 1 (main.pdf p.11), H2 uptake at 77 K and 20 bar, 3 values (6.33, 4.58, 3.99 wt%): rows M15 (CEMC), M45 (Pt5CEMC), M73 (Pt10CEMC), each merged with a plotted point of its Fig. 6 / Fig. 7 isotherm (table_direct, digitized point in notes).
- Table 1 (p.11), parenthesised H2 uptake at 298 K and 20 bar, 3 values (0.20, 0.18, 0.17 wt%): rows M83 (CEMC, I4), M84 (Pt5CEMC, I5), M85 (Pt10CEMC, I6), each merged with the 20 bar marker of the Fig. 6 right panel curve.
- Table 1 (p.11), surface area (BET 3360, 2047, 1279 m2/g; micropore area 2838, 1664, 1002 m2/g) and pore volume (total 1.71, 1.01, 0.66; micropore 1.24, 0.70, 0.42 cm3/g): recorded on every row of the sample. Table 1 values are used where the text (p.9) differs: CEMC total pore volume text 1.91 vs table 1.71; Pt5CEMC area 2049 vs 2047 and pore volume 1.06 vs 1.01; Pt10CEMC area 1249 vs 1279 (stated in the notes of the affected rows).
- Text p.15 ("At 77 K and 20 bar ... 6.33 wt.% ... 4.58 and 3.99 wt.%") and p.17 ("at 298 K and 20 bar are 0.20, 0.18 and 0.17 wt.%"): same measurements as Table 1, no separate rows (cited in source_location).
- Experimental section (p.4-7): degassing (10-10 bar, 523 K overnight), H2 purity 99.9999%, IGA-003 Hiden microbalance, buoyancy correction (bulk density 1.5 g/cm3, H2 density 0.04 g/cm3), BET range P/P0 0.02-0.22, N2 probe, t-plot micropore values, NLDFT PSD, Pt loading 5 and 10 wt% calculated on the zeolite: coded on every row.
- Fig. 6 left panel (p.16), 77 K, CEMC-de: archive Fig6_77K_CEMC-de.json (13 markers); 12 desorption rows M16-M27; its top marker (20.158 bar, 6.3445 wt%) coincides with the adsorption end point and is represented by row M15.
- Fig. 7 left panel (p.18), 77 K CEMC curve: archive Fig7_77K_CEMC.json (15 markers); 14 adsorption rows M1-M14; its top marker (20.118 bar, 6.339 wt%) is merged into M15 (closest plotted point to the printed 20 bar). Fig. 6 CEMC-ad markers are partly hidden under the desorption markers; the Fig. 7 CEMC 77 K markers coincide with the visible Fig. 6 CEMC-ad markers, so the two are one run (I1).
- Fig. 6 left panel, 77 K, Pt5CEMC-ad (Fig6_77K_Pt5CEMC-ad.json, 9 markers, rows M28-M36) and Pt5CEMC-de (Fig6_77K_Pt5CEMC-de.json, 9 markers, rows M37-M44; the 20.0 bar marker is merged into M45): isotherm I2.
- Fig. 6 left panel, 77 K, Pt10CEMC-ad (Fig6_77K_Pt10CEMC-ad.json, 29 markers, rows M46-M72, top marker merged into M73) and Pt10CEMC-de (Fig6_77K_Pt10CEMC-de.json, 10 markers, rows M74-M82): isotherm I3.
- Fig. 6 right panel, 298 K, CEMC-ad / Pt5CEMC-ad / Pt10CEMC-ad: archives Fig6_298K_CEMC-ad.json (14), Fig6_298K_Pt5CEMC-ad.json (9), Fig6_298K_Pt10CEMC-ad.json (13); only the highest-pressure marker of each is used (merged into M83, M84, M85). The Fig. 7 insets show the same 298 K curves; not extracted a second time.
- Fig. 7 left panel, 87 K, CEMC: archive Fig7_87K_CEMC.json (15 markers); highest-pressure marker (19.97 bar, 4.947 wt%) = row M86 (I7). Fig. 7 right panel, 87 K, Pt5CEMC: archive Fig7_87K_Pt5CEMC.json (27 markers); highest-pressure marker (19.97 bar, 3.736 wt%) = row M87 (I8).
- Fig. 7 insets, 308 K, CEMC (Fig7_308K_CEMC.json, 17 markers, top marker row M88, I9) and Pt5CEMC (Fig7_308K_Pt5CEMC.json, 14 markers, top marker row M89, I10).
- Fig. 7 right panel, 77 K, Pt5CEMC: archive Fig7_77K_Pt5CEMC.json (25 markers), rows M90-M114 (I11). Separate run from Fig. 6 Pt5CEMC (different marker pressures, e.g. 0.23, 0.48, 0.74 ... 19.97 bar against 5.50, 7.02 ... 17.99 bar). Its 19.97 bar marker is within tolerance of Table 1's 4.58 wt% at 20 bar but is farther from 20 bar than the Fig. 6 marker, so the table value is merged with M45 and this marker stays its own row (M114).

## Archive checks (digitize_figure.py check)

- passed: Fig6_77K_CEMC-de (20.158 bar, 6.3445 vs 6.33); Fig6_77K_Pt5CEMC-de (20.0 bar, 4.593 vs 4.58); Fig6_77K_Pt10CEMC-ad (19.981 bar, 3.99 vs 3.99); Fig6_298K_CEMC-ad (20.0275 bar, 0.2009 vs 0.20); Fig6_298K_Pt5CEMC-ad (20.0 bar, 0.1828 vs 0.18); Fig7_77K_CEMC (20.118 bar, 6.339 vs 6.33); Fig7_77K_Pt5CEMC (19.97 bar, 4.5635 vs 4.58).
- discarded: Fig6_298K_Pt10CEMC-ad (20.0 bar, 0.141 vs printed 0.17, 17% off). Not a calibration error: the same right-panel calibration passed for the CEMC and Pt5CEMC curves. The paper is inconsistent between Table 1/text (0.17 wt%) and the plotted Pt10CEMC marker (0.141 wt%). Row M85 stores the printed 0.17, extraction_confidence 3, discrepancy in notes.
- unchecked (the paper prints no number to check against): Fig6_77K_Pt5CEMC-ad (the 20 bar end point is hidden under the desorption marker, which carries the check), Fig6_77K_Pt10CEMC-de, Fig7_87K_CEMC, Fig7_87K_Pt5CEMC, Fig7_308K_CEMC, Fig7_308K_Pt5CEMC.

## Markers seen but not stored as rows

- Fig. 6 Pt10CEMC-ad marker at the plot origin (0 bar, 0 wt%) and Fig. 6 Pt10CEMC-de marker at digitized p = -0.0198 bar, 0.9539 wt% (within one pixel of the left axis): both are in the archives and counted in isotherm_point_count, but not written as rows because the schema requires pressure_bar > 0 (the validator rejects 0 and the digitized pressure of the second marker is negative, i.e. below the digitization resolution of about 0.06 bar per pixel).
- Fig. 6 / Fig. 7, 298 K, 87 K and 308 K curves: all markers other than the highest-pressure marker of each isotherm (scope rule: only the highest-pressure point away from 77 K). These markers are counted in isotherm_point_count.
- Fig. 7 left panel, 77 K CEMC curve and Fig. 7 298 K insets (CEMC, Pt5CEMC): the same curves as Fig. 6 (coincident markers), not extracted twice; the CEMC adsorption markers hidden in Fig. 6 are taken from Fig. 7.
- Unseparated markers (low-pressure overlap of the three samples, markers hidden under other markers of the same figure; each is counted in isotherm_point_count, which is therefore approximate: I1 31, I2 23, I3 45, I4 38, I5 29, I6 23, I7 16, I8 28, I9 25, I10 17, I11 27):
  - Fig. 6 Pt10CEMC-de: desorption markers at about 0.74 (uncertain), 1.0, 1.7, 12.4, 13.9, 16.2 and 18.0 bar overlap the adsorption markers and could not be separated; only the 9 stored markers plus the one at p <= 0 were isolated.
  - Fig. 6 Pt5CEMC: adsorption markers below 5.5 bar and desorption markers below 4 bar are hidden under markers of the other series (the Pt5CEMC curve runs between and under the CEMC and Pt10CEMC markers at low pressure). The Fig. 7 Pt5CEMC curve (I11) is a separate run and does not fill these gaps.
  - Fig. 6 CEMC-de: the lowest separated marker is at 0.97 bar; the estimated count (31) includes about 3 low-pressure markers of the two branches that are hidden under the other series.
  - Fig. 6 right panel (298 K): low-pressure markers of the samples merge into blobs (79-81 px red and blue clusters at p below 0.5 bar); not used for rows (only the 20 bar marker is).
  - Fig. 7 insets (308 K) and 87 K curves: low-pressure clusters (for example a 140 px merged blob in the CEMC 308 K inset near 1.7 bar); not used for rows.
- Fragments rejected by the marker size window and not data: a blue 'marker' at (0.36 bar, 1.31 wt%) that is a line junction; a red fragment at (0.36, 1.04), 9 px; a black filled fragment at 2.5 bar, 12 px (a filled triangle hidden under an open one); 9-12 px fragments just above the x axis of the Fig. 7 87 K plots; 9-14 px fragments near the axes in the Fig. 6 Pt5CEMC-ad, Pt10CEMC-ad and Pt5CEMC 298 K archives and in the Fig. 7 Pt5CEMC 77 K archive (each listed under rejected_markers in its JSON).
- Preprocessing: legends and axis labels were whitened and hollow-marker interiors were filled on derived copies of the page images (geometry unchanged; scripts derive_open.py, derive_open_keep.py, derive16.py and the p16_clean.png, p18_main_clean.png, p18_inset_clean.png images in the work directory); the tool ran on these derived images for the hollow markers (de branches). Template matching was tried and rejected (false positives).
- Fig. 7 y axes: the data exceed the highest labelled tick for CEMC (labelled to 6; markers at 18.14 and 20.12 bar) and for Pt5CEMC (labelled to 4; markers from 12.97 bar). The calibration (lowest and highest labelled ticks, third tick checked) was extended linearly beyond the top tick; the tool marks these as outside the axis range, and the notes of the affected rows say so. The checks at 20 bar passed (CEMC 6.339 vs 6.33; Pt5CEMC 4.5635 vs 4.58).

## Values seen but not extracted (not H2 uptake measurements)

- Abstract, p.19-21 text and Fig. 8: Qst values (7.8 and 8.3 kJ/mol at 0.08 wt%; 5.0 kJ/mol at 2.6-5.0 wt%; 72, 20.8, 17.9 and 2.6 kJ/mol at coverage 0, 0.014, 0.073 and 0.13 wt%; 5.4 and 0.9 kJ/mol for CEMC at 298/308 K up to 0.18 wt%) and the coverage values at which they are evaluated (0.08, 0.014, 0.073, 0.13, 1.3, 2.6, 5.0, 0.18 wt%): these are heats of adsorption and the coverages are abscissa values of the Qst calculation, not measured uptake values at a stated pressure. Fig. 8 (Qst against uptake) is not an uptake isotherm and was not digitized.
- Fig. 2 (N2 isotherms at 77 K and NLDFT pore size distributions), Fig. 1 (XRD), Figs. 3-5 (SEM, TEM, Pt particle size histograms: Pt 2-4 nm in the abstract, 1-4 nm and 2-5 nm in the text): characterization, not H2 uptake. N2 isotherm values were not read; the PSD is described in notes only.
- Text p.16-17: hysteresis and chemisorption statements for Pt10CEMC ("part of the H2 was chemically adsorbed") carry no numeric uptake value.
- No value for a non-carbon material (zeolite EMC-2 template, Pt metal) is given.
- No mean across laboratories or computed reference value in the paper.

## Coding decisions

- Basis: the paper names no basis (basis_stated false, uptake_type unspecified); the instrument is gravimetric with a stated buoyancy correction, so basis_inferred = excess. wt% has no paired unit: wt_pct_convention unknown, source none. All rows value_kind measured.
- Sample labels as printed in Table 1 (CEMC, Pt5CEMC, Pt10CEMC); S1-S3 in order of appearance. Pt samples are material_class composite with metal_element Pt; metal_loading_wt_pct 5 and 10 is the calculated nominal loading on the EMC-2 zeolite (not a measured Pt content of the carbon), noted on the rows.
- average_pore_diameter_nm filled only for CEMC (PSD mode about 1.1 nm, NLDFT); the Pt samples' PSD has two centres (1.1 and 2.0 nm) and no single average is printed.
- degas_duration_h and sample_mass_mg empty: the paper says "overnight" and gives no sample mass. The "bulk density 1.5 g/cm3" and "H2 density 0.04 g/cm3" are recorded in free_volume_calibration text and not in skeletal_density_g_cm3 or adsorbed_phase_density_kg_m3 (they are assumptions of the buoyancy correction, and the paper calls 1.5 g/cm3 a bulk density).
- measuring_lab_id: Yang group, University of Exeter (first corresponding author marked, first affiliation).
- replicates_reported false: no uncertainty or repeated isotherm is reported (the microbalance resolution of 0.2 ug is not an uncertainty of the value).
- extraction_confidence: 5 for table rows; 3 for table row M85 (table/figure conflict), for digitized markers below 2 bar (overlap) and for all Pt10CEMC desorption markers; 4 otherwise.
- Fig. 6 and Fig. 7 isotherm coding: one id per sample, temperature and run; Fig. 6 and Fig. 7 curves identified as one run only where the marker pressures coincide (CEMC 77 K, CEMC 298 K, Pt5CEMC 298 K).
- Run note: the first session stopped on an API usage limit before rows.csv was written; the rows were then built from the archived digitizations with work/build_rows.py. The validator (--errors-only) reports no errors; its only warning is the unspecified uptake_type, which is the correct coding because the paper names no basis.
