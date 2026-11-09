# HYC-0009 extraction log (agent A)

Rows written: 105 (rows.csv). Archives: digitizations/ (14 files).

## Extracted from
- Table 2 (main.pdf p.5 = journal p.626), 298 K: H2 wt.% for 7 samples; Vs (cm3(STP)/g at 760 Torr) on the same row for 6 (Vulcan has a dash). 7 rows.
- Table 3 (p.626), 77 K: same layout, 7 rows. The Vulcan XC72 row is linked to its plotted isotherm I1 (see below); the other six rows have no isotherm_id.
- Table 4 (main.pdf p.6 = p.627): H2 wt.% desorbed in TPD, 6 CNT samples (Vulcan not measured by TPD), 6 rows, mode TPD, temperature 298 K, pressure unstated, reference temperature 450 C.
- Fig. 3B (p.625), 77 K isotherms, 7 series, 79 digitized rows (below).
- Fig. 3A (p.625), 298 K isotherms, highest-pressure marker of each of 7 series, 7 rows.
- Table 1 (p.624): characterization (BET before and after HNO3, purity, diameter, layers, ID/IG) used on every row; every sample has uptake values, so no characterization-only sample.
- Section 2.2/2.3/2.4 (p.623-624): HNO3 treatment, 250 C pretreatment, 200 mg sample, Fisons Sorptomatic 1900, TPD procedure.

## Problems in the paper, recorded not corrected
- Unit-consistency failure, Tables 2 and 3: for every CNT sample the printed wt.% and Vs disagree (W1 from Vs is 0.38 to 0.51 of the printed wt.%; e.g. SWCNTs-85% at 77 K: 3.27 wt.% vs 139.036 cm3/g = 1.2505 wt%). Vs matches the plotted markers of Fig. 3 (checked on all 12 CNT series); the wt.% column does not. Vulcan XC72: at 77 K 0.24 wt.% matches the plot (26.7 vs 26.5 cm3/g); at 298 K 0.03 wt.% does not (plot 1.26 cm3/g = 0.011 wt%), while 0.005 cm3/m2 x 254 m2/g = 1.27 cm3/g does. wt% convention coded unknown/none on these rows.
- Text p.626 says 0.34% for SWCNTs-85% at 298 K and cites Table 2, which prints 0.36. Table value kept, discrepancy in notes.
- Tables 2 and 3 give no pressure beside the wt.% column. 760 Torr (printed for Vs and for cm3/m2 in the text) was used for the whole row.
- Table 1 BET values in the first column are before HNO3, those in the second after HNO3; the text says samples were treated with HNO3 before characterization and use, so the after-HNO3 area is coded as BET of the measured sample. SWCNTs-60.5% decreases (726 to 703).
- Text p.627 says "388-342 K" for MWCNT peak temperature; Table 4 lists 388-392 K. Not an uptake value.

## Table value vs plotted point (§9 rule)
- Vulcan XC72, 77 K: Table 3 value 0.24 wt.% (760 Torr via cm3/m2 text) is within 2% of the last plotted marker (749.7 Torr). One row (table_direct, I1); the last marker has no separate row; digitized pressure/value and archive in notes.
- All other samples: the highest-pressure plotted marker lies 15.9 to 56 Torr below 760 Torr (limit max(2%, 0.02 bar) = 15.2 Torr), so the table rows are separate rows without isotherm_id, and the plotted last markers are digitized rows. Closest case: Vulcan XC72 at 298 K, 744.1 Torr (15.9 Torr away). The paper does not say Vs is taken from the figure.

## Fig. 3B (77 K) digitization
Greyscale figure (colour #231f20); series separated by masking windows (22 px, 3x crop; 17 px for plus markers) around marker positions found in a first whole-plot marker extraction; centroids come from digitize_figure.py (mode markers). Calibration on page image crop (3x): x ticks 0 (229 px) and 800 (1421.5 px), verify 400 (826 px); y ticks 0 (1340.5 px) and 400 (29.5 px), verify 200 (685 px). All archives passed `check` against printed Vs (or the wt%-derived value for Vulcan) at the last marker, tolerance 5%.
Markers counted on the plot (origin marker (0,0) of every series excluded from counts and rows) vs extracted:
- Vulcan XC72: 15 counted, 15 extracted (14 rows; last marker is the Table 3 row). First marker touches the x axis (region clipped at the axis line).
- MWCNTs-95.7% (circles): 17 counted, 16 extracted. First marker (about 46 Torr) is merged with the MWCNTs-97% and -99% markers, not separable.
- MWCNTs-97% (up-triangles): 15 counted, 3 extracted. The first marker is merged in the same blob; 11 more are merged with the MWCNTs-99% diamonds into one connected blob each (centroids not usable), so only the 3 highest-pressure markers could be separated. 12 unseparated.
- MWCNTs-99% (diamonds): 15 counted, 3 extracted, same reason. 12 unseparated. The three separated pairs touch each other, so those centroids carry larger error (confidence 2).
- thinMWCNTs-95% (plus): 15 counted, 14 extracted. The first marker (about 45 Torr) is hidden behind the merged blob above. Thin strokes: centroid of the strokes that pass the colour threshold.
- SWCNTs-60.5% (down-triangles): 14 counted, 14 extracted.
- SWCNTs-85% (asterisks): 14 counted, 14 extracted. Arm fragments rejected as too small; centroid of the strokes that survive the threshold.
isotherm_point_count uses the counted numbers. Markers for 97% and 99% are the only ones not fully recovered; no point was read by eye.

## Fig. 3A (298 K)
Calibration: x 0 (229 px) to 800 (1409.5 px), verify 400 (820 px); y 0 (1391.5 px) to 40 (59.5 px), verify 20 (725.5 px). All 7 series separable at the high-pressure end. Counted (origin excluded): Vulcan 12, circles 11, up-triangles 12, diamonds 11, plus 11, down-triangles 11, asterisks 11 (79 markers; the first up-triangle and diamond are merged with each other, 77 blobs found). Only the highest-pressure marker of each is a row; the archives hold the other separable markers. The up-triangle and diamond archives omit the two merged first markers.
Archive history: the first check of the Vulcan 298 K archive used the printed 0.03 wt.% (3.34 cm3/g) and failed, so that archive was discarded; the whole 298 K set was re-extracted and checked once against 0.005 cm3/m2 x 254 m2/g = 1.27 cm3/g (printed values), which passed (0.69%). The 298 K check values for the CNT series are the printed Vs.

## Seen, not extracted
- Vm columns of Tables 2 and 3 (BET monolayer volume of H2, a model-derived capacity with no stated pressure): 12 values (4.018 to 11.588 cm3/g at 298 K; 41.543 to 85.172 at 77 K). They are mentioned in the notes of the table rows.
- H/C and cm3/m2 columns (Tables 2 and 3): no schema field; listed in row notes.
- Tm and Ed of Table 4 (K, kJ/mol): not uptake.
- Fig. 4 (kinetics of H2 uptake under flow, 298 K, MWCNT-95.7%): not an isotherm, not digitized; no value in tables or text.
- Fig. 5 (TPD spectra, ppm H2 vs T): not digitized.
- Fig. 1 (SEM), Fig. 2 (Raman): no uptake.
- 1.75 wt.% monolayer capacity of SWCNTs-85% by the Zuttel model (p.626): a calculation.
- Introduction p.623: Dillon 5-10 wt.%, Ye up to 8 wt.%, Liu 2-4 wt.%, Zhu up to 5 wt.%, Wu up to 0.25 wt.%, Darkrim-Levesque 11 wt.% (simulation): values from other papers.
- Origin markers (0,0) in both panels.
- No metal hydride, zeolite or MOF is measured; no non-carbon material excluded.

## Coding notes
- uptake_type unspecified, basis_stated false for all rows: the paper never names the basis. Volumetric rows: basis_inferred excess (instrumental default, "volumetric adsorption apparatus"); TPD rows unknown. measurement_method volumetric_sieverts is used for the generic volumetric apparatus.
- Vulcan XC72: material_class other (carbon black), commercial, supplier not named. BET 254 m2/g is in the as-prepared column and the paper does not say whether Vulcan was acid-treated, so area_same_sample = unclear. No degassing or sample mass is coded for Vulcan because the pretreatment text is written for CNTs.
- Residual catalyst (Fe2O3/Al2O3, amount not given) is not coded as composite or residual metal; purity is by TGA before acid treatment.
- Degassing (volumetric): 250 C, 0.5 h (the 30 min evacuation at 250 C); the vacuum heating ramp has no duration. No end pressure.
- measuring_lab_id: corresponding author Verykios (marked *), University of Patras.
