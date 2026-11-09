# HYC-0118 extraction log (extractor B)

Paper: Park & Park, Carbon 158 (2020) 364-371 (paper.json year 2019), doi 10.1016/j.carbon.2019.10.100. Input: page images main-1..8, si1-1..4. Rows written: 157 (15 table_direct, 142 figure_digitized), 5 samples, 20 isotherms.

## Samples and isotherm map

- S1 CS-C, S2 CS-SE, S3 CS-SE-AC, S4 CS-AC, S5 CS-AC-SE (order of first appearance, Sec. 2.1; labels as printed in Table 1).
- I1-I5: Fig. 5(a), 77 K, QExcess, 0-1 bar (CS-C, CS-SE, CS-SE-AC, CS-AC, CS-AC-SE). Table 1 "1 bar QExcess" values merged with each curve's highest-pressure marker.
- I6-I10: Fig. 5(b), 77 K, QExcess, 0-60 bar (same order). Table 1 "60 bar QExcess" values merged with each curve's highest-pressure marker.
- I11-I15: Fig. S2, 77 K, QTotal, 0-60 bar (same order). Table 1 "60 bar QTotal" values merged with each curve's highest-pressure marker.
- I16-I20: Fig. S3, 298 K, QExcess, 0-60 bar (same order); only the highest-pressure point of each curve extracted (protocol rule for non-77 K isotherms).
- Each plotted curve coded as its own run. The paper does not say whether Fig. 5(a) is the low-pressure part of the Fig. 5(b) run; the Fig. S2 QTotal curves are computed by the authors from the QExcess data via Eq. (11).

## Sources used

- Table 1 (main-5, p. 368): SSA (NLDFT), V_Total, V<2nm, V<4nm, V2-50nm, QExcess at 77 K 1 bar and 60 bar, QTotal at 77 K 60 bar for 5 samples. All 15 uptake values extracted (table_direct, merged with figure markers, see below). V<4nm has no schema field and is recorded in notes.
- Sec. 2.2 (main-2, p. 365): N2 isotherms at 77 K (Autosorb IQ3-XR), SSA and PSD by NLDFT; H2 by volumetric method, BEL-HP (BEL Japan), 77 K and 60 bar; degassing 473 K, 12 h, under vacuum; H2 99.999%. No free-volume calibration, sample mass, BET range or uncertainty stated.
- Sec. 3.3 (main-4/5): definitions of QExcess and QTotal and Eq. (11) used as basis evidence (basis_stated = true for both bases; two bases reported side by side in Table 1).
- Fig. 2(f) (main-3): EDS C/O/Si at% per sample, recorded in notes (residual silica; Si not coded as dopant or metal).
- Fig. 5(a), Fig. 5(b) (main-5), Fig. S2 (si1-2), Fig. S3 (si1-3): digitized, see below.

## Values seen but not extracted as rows

- Text p. 368 "lowest QExcess of 1.83 wt% at 60 bar" (CS-C), "increase in QExcess to 3.51 wt%" (CS-SE), "increased from 5.56 wt% for CS-AC samples to 6.12 wt% for the CS-AC-SE samples", "maximum QExcess values ... between 1.83 and 8.29 wt% was translated into QTotal values between 1.89 and 11.16 wt% at 77 K and 60 bar (Fig. S2)"; Conclusion "QExcess values between 1.83 and 8.29 wt% at 77 K and 60 bar": same measurements as Table 1, recorded once (notes cite the text). Inconsistency: text gives 1.89 wt% as the lowest QTotal, Table 1 prints 1.86 wt% for CS-C; table value recorded, discrepancy noted on HYC-0118-M104.
- Introduction p. 364: Fierro et al. [43] excess uptake 0.4 wt% at 298 K, 50 bar and 5.5 wt% at 77 K, 40 bar on ACs: literature values from another paper, not this paper's measurements.
- Fig. 6(a-d) (main-6) and Fig. S5(a-f) (si1-4): correlation plots of QExcess (77 K, 1 and 60 bar) against pore volumes and SSA; not isotherms, not digitized. Their y values are the Table 1 values. Characterization shown only there and not in tables or text: V<3nm and V<5nm pore volumes (x coordinates of Fig. S5(a,b,d,e)); not extracted.
- Fig. S4 (si1-3): heat of adsorption vs storage coverage; not an uptake. Text p. 369: dH 4.01-7.98 kJ/mol; not an uptake.
- Fig. 4(a,b) (main-4): N2 isotherms and NLDFT PSD; characterization only. Fig. 3, Fig. S1: SEM images.
- Fig. S3 points other than the highest-pressure point of each curve: not extracted (non-77 K rule).
- No non-carbon sorbent is measured in this paper.

## Figure digitization (scripts/digitize_figure.py extract --mode markers)

- Working images: work/img/main-5_masked.png, si1-2_masked.png, si1-3_masked.png are copies of the page images with the legend boxes and in-plot text labels painted white (pixel coordinates unchanged), so legend symbols are not picked up as markers. Fig. S3 copy also blanks the overlapping caption text "heat of adsorption." inside the plot.
- Fig. 5(a): x ticks 0.0 (px 214.28) and 1.0 (px 587.06), check 0.4 (px 363.37, residual 0.01%); y ticks 0.0 (px 1450.99) and 2.5 (px 1199.15), check 1.0 (px 1350.41, residual 0.15%).
- Fig. 5(b): x 0 (711.16) and 60 (1051.91), check 30 (881.52, 0.01%); y 0 (1443.25) and 8 (1200.69), check 4 (1322.0, 0.02%).
- Fig. S2: x 0 (402.53) and 60 (875.63), check 30 (639.03, 0.02%); y 0 (1199.5) and 12 (816.63), check 6 (1007.73, 0.17%).
- Fig. S3: x 0 (407.58) and 60 (909.19), check 30 (658.54, 0.06%); y 0.0 (582.25) and 0.6 (211.95; the 0.6 label is partly overprinted by the caption, tick spacing consistent with the other ticks), check 0.3 (397.36, 0.14%).
- Tick centres located from pixel-column/row intensity profiles (work/ticks.py). Markers were counted on enlarged images and with a highlight finder (work/hlfind.py: each ball marker has a white specular highlight); every tool detection was checked against the marker positions, and only detections centred on one marker were written as rows.
- Highest-pressure markers of Fig. 5(b) and Fig. S2 lie at about 60.5-61.5 bar, beyond the 60-bar tick (no higher label); their pressures are linear extrapolations of the calibration. These points are merged with the Table 1 60-bar values (printed pressure used on the row).

### Per series: markers counted, extracted, not separated

- f5a_CS-C (I1, black): 15 markers identified, 13 extracted (indices 0-12). Not separated: marker at ~0.005 bar (~0.12 wt%) at the axis corner, merged with the axis/purple marker; marker at ~0.34 bar (~0.89 wt%) merged with the line. A further marker may be hidden at the origin under CS-SE-AC.
- f5a_CS-SE (I2, red): almost entirely hidden under CS-AC (blue) markers; crescents visible at about 0.27, 0.39, 0.53, 0.66, 0.80 bar cannot be centroided. Only the highest-pressure marker (index 1, 0.983 bar) extracted, merged with Table 1; index 0 (fragment at 0.965 bar) excluded.
- f5a_CS-SE-AC (I3, purple): 16 markers, 16 extracted (all).
- f5a_CS-AC (I4, blue): 7 markers identified at 0.17-0.98 bar, 7 extracted. Low-pressure markers (<0.15 bar) lie under CS-SE-AC markers and could not be separated or counted.
- f5a_CS-AC-SE (I5, green): 10 markers identified, 8 extracted. Not separated: markers at ~0.03 bar (~0.40 wt%) and ~0.075 bar (~0.64 wt%) overlapping CS-C/CS-SE-AC; lower-pressure markers hidden.
- f5b_CS-C (I6, black): 13 markers identified at P >= 3 bar plus an unresolved low-pressure stack; 11 extracted (indices 1-8, 10-12). Excluded: index 0 (blob of the low-pressure stack, 106 px), index 9 (line segment at 34.7 bar, no marker). Not separated: markers at ~3.1 bar and ~20.5 bar.
- f5b_CS-SE (I7, red): 13 markers identified at P >= 4.5 bar; 13 extracted (indices 0-6, 8, 9, 10, 12, 13, 15). Excluded line fragments: indices 7 (21.6 bar), 11 (41.3 bar), 14 (55.3 bar). Markers 0-4 (4.6-10.7 bar) are in an overlapping chain partly under CS-AC; confidence 2. Low-pressure stack (<4 bar) not separable.
- f5b_CS-SE-AC (I8, purple): 19 markers identified (15 at P >= 3 bar, 4 highlights at the bottom of the low-pressure stack); the stack below ~3 bar holds more markers that overlap vertically (spacing smaller than the marker diameter) and could not be counted or separated. 10 extracted (indices 9, 10, 12-19). Excluded: indices 0-4 (stack, pressure not resolvable at 0.18 bar/px), 5 (stack blob, 403 px), 6, 7, 11 (fragments of single markers, 9-15 px), 8 (two merged markers at ~5.5 and ~6.8 bar). Not separated: markers at ~3.05, 4.6, 5.5, 6.8, 10.8 bar.
- f5b_CS-AC (I9, blue): 8 markers identified at 15.6-61.2 bar, 8 extracted (indices 2-9). Markers between 3 and 11 bar lie under CS-AC-SE (green) and could not be separated; indices 0 and 1 excluded (not verifiable as single markers, index 1 is an 80 px blob).
- f5b_CS-AC-SE (I10, green): 14 markers identified (6 in the 3-10 bar chain, 8 at 15-61 bar); 8 extracted (indices 2-9). Excluded: index 0 (chain blob, 252 px), index 1 (two merged markers at ~8.6 and ~10.1 bar). Chain markers at ~3.1, 4.4, 5.8, 7.2, 8.6, 10.1 bar not separated.
- fS2_CS-C (I11, black triangles): 13 markers identified at P >= 3 bar; 9 extracted (indices 1, 3-10). Excluded: index 0 (low-pressure stack blob), index 2 (merged triangles at ~6.2, 7.6, 9.1 bar). Low-pressure stack not separable.
- fS2_CS-SE (I12, red): 11 identified at 7.7-60.8 bar, 11 extracted. Lower-pressure triangles under CS-AC not separable.
- fS2_CS-SE-AC (I13, purple): 14 separated triangles at 4.6-61.4 bar, 14 extracted (indices 1-14); index 0 is the low-pressure stack blob (1342 px), excluded. Stack below ~4 bar not separable or countable.
- fS2_CS-AC (I14, blue): 12 identified at 6.3-61.0 bar, 12 extracted. Lower-pressure triangles hidden.
- fS2_CS-AC-SE (I15, green): 14 identified; 11 extracted (indices 1, 2, 3, 5-12). Excluded: index 0 (chain blob, 173 px), index 4 (two merged triangles at ~9.0 and ~10.5 bar).
- fS3_* (I16-I20): ROI restricted to the highest-pressure markers (x 880-917 px). Extracted: CS-C 58.81 bar 0.1961 wt%; CS-SE 59.10 bar 0.4246; CS-SE-AC 59.90 bar 0.5208; CS-AC 59.68 bar 0.4581; CS-AC-SE 59.51 bar 0.4392. Markers identified per curve (isotherm_point_count, lower bounds except CS-SE-AC): CS-SE-AC 13, CS-C 9, CS-SE 9, CS-AC-SE 9, CS-AC 5 (blue markers mostly hidden under green and purple). Fig. S3 legend labels the black series "CS"; taken to be CS-C.
- isotherm_point_count is the number of markers identified on the plot; it is exact only for I3 and a lower bound for every other isotherm (stated in each row's notes).

### Step-6 value checks (digitize_figure.py check, 5% tolerance) and figure-table inconsistencies

- Fig. 5(b) vs Table 1 at 60 bar: CS-SE-AC 8.16 vs 8.29 pass; CS-AC 5.48 vs 5.56 pass; CS-SE 3.46 vs 3.51 pass; CS-C 1.81 vs 1.83 pass; CS-AC-SE 5.70 vs 6.12 FAIL (archive status set to "discarded" by the tool). The other four series of the same panel and calibration pass within 2%, and the green end marker visibly lies below the 6 wt% tick, so this is an inconsistency between Fig. 5(b) and Table 1 (Fig. 6(b) plots 6.12), not a digitization error. The digitized rows of f5b_CS-AC-SE were kept; the merged row HYC-0118-M95 records the printed 6.12 with the digitized point (61.44 bar, 5.76 wt%) in notes. Flag for agent C.
- Fig. S2 vs Table 1 QTotal at 60 bar: all five pass (11.00/11.16, 7.00/7.09, 6.16/6.23, 4.07/4.10, 1.80/1.86).
- Fig. 5(a) vs Table 1 at 1 bar: the tool check cannot run (x = 1 lies beyond the last marker, 0.97-0.99 bar). Comparison of the last markers with Table 1: CS-C 1.066 vs 1.08 (-1%), CS-AC-SE 1.961 vs 2.03 (-3.4%), CS-AC 1.815 vs 1.9 (-4.5%), CS-SE 1.749 vs 1.87 (-6.5%), CS-SE-AC 2.477 vs 2.76 (-10.3%). Calibration residuals are <=0.15%; Fig. 6(a) plots the Table 1 values. Inconsistency between Fig. 5(a) and Table 1, noted on the merged rows (M13, M14, M30, M37, M45). Flag for agent C.
- Fig. S3: no value stated in the paper; archives unchecked.

## Coding decisions

- Table/figure merging: the paper states the QExcess values "are shown in Fig. 5 and are summarized in Table 1", and that the maximum QExcess values were "translated into QTotal values ... (Fig. S2)"; each Table 1 value is therefore the same measurement as the highest-pressure marker of the corresponding curve, recorded once with the printed value and printed pressure (1 or 60 bar) and the digitized point in notes.
- QTotal rows (I11-I15): basis total (defined in the paper), basis_stated true. value_kind = unclear: the paper says QTotal "cannot be determined experimentally" and computes it from QExcess with Eq. (11) using V_pore and NIST bulk density, so it is neither a directly measured nor a fitted value.
- QExcess rows: basis excess, basis_stated true (defined, and reported side by side with QTotal in Table 1); measurement_method volumetric_sieverts; calibration_described false (no free-volume determination stated); instrument_identified true (BEL-HP, BEL Japan); replicates_reported false.
- Surface area: Table 1 footnote a says the SSA is computed with the NLDFT method; stored in bet_surface_area_m2_g with surface_area_method = DFT, probe N2 (N2 isotherms at 77 K). No BET area, BET range or consistency criteria are reported (bet_range_stated and bet_consistency_criteria_stated = false). Pore volumes NLDFT/N2: V_Total -> total, V<2nm -> micropore, V2-50nm -> mesopore.
- material_class: CS-C and CS-SE (carbonized coconut shell, not activated) = other; KOH-activated samples = activated_carbon. Residual silica (EDS Si 2.16 to 0.02 at%) treated as an impurity, not a composite phase; recorded in notes. synthesis_method = carbonization for all; silica elimination recorded as purification_method, KOH activation as activation_method.
- wt% convention not stated and no paired units: wt_pct_convention unknown / none.
- Degassing 473 K stored as 199.85 °C (printed value in notes). Pressures treated as absolute (the paper does not say gauge).
- measuring_lab_id: Park group, Inha University (corresponding author S.-J. Park).
