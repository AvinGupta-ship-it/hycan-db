# HYC-0087 extraction log (agent A)

Paper has one file (main, 12 PDF pages, journal pp. 550-561), no supplementary file. Two samples: S1 = Horse chestnut shell, S2 = Tangerine peel (ZnCl2-activated biomass carbons). 63 rows written.

## Extracted from

- Table 1 (journal p. 552): 6 rows, per sample the H2 value at 1 bar, at 20 bar and the "Maximum value" with its pressure (HC 80 bar, TP 26 bar). Same table gives S_BET, Vt, Vmicro, V_DFT, Vmeso, carried on every row of the sample (V_DFT has no field; it is in the notes of the Table 1 rows).
- Figure 3 (journal p. 553): 77 K H2 adsorption isotherms (adsorption only, no desorption branch plotted), digitized with `digitize_figure.py extract --mode markers`. S1 (I1): 22 markers extracted, 2 of them merged with Table 1 rows (20 bar, 80 bar), 20 digitized rows. S2 (I2): 19 markers extracted, 2 merged with Table 1 rows (20 bar, 26 bar), 17 digitized rows.
- Table 3 (journal p. 555): Langmuir nm (wt%), 2 rows, `fitted_extrapolated`, pressure_unstated = true. Text on p. 555 repeats the two values.
- Table 4 (journal p. 557): per sample and pressure (80, 55, 33 bar) the pseudo-first-order qe(cal), experimental qe(exp) and pseudo-second-order qe(cal), all in mmol/g; 18 rows. qe(exp) is `measured`; the two qe(cal) columns are `fitted_extrapolated`. wt% = 0.201588 x mmol/g (W1, computed_from_other_unit).

## Figure 3 digitization

- Working image `work/fig3_4x_nolegend.png`: crop x 700-1100, y 1070-1310 of `pages/main-04.png`, 4x Lanczos; the legend box (page pixels x 912-1078, y 1248-1295) painted white so that legend markers are not extracted.
- Tick positions found from pixel rows/columns of the tick labels on the 1x page image, then converted to the 4x image: x = 0 at 87.1, x = 80 at 1488.7 (verify 40 at 787.9, predicted 40.000); y = 0 at 911.1, y = 5 at 42.3 (verify 2.5 at 476.1, predicted 2.503). The plot has no tick marks; the label centres were used. Frame left edge coincides with x = 0 and frame bottom with y = 0.
- Series S1 (black squares): colour #000000, tolerance 80, open-px 26, marker size 20-1500 px, ROI 78 60 1522 905 (right edge of the ROI excludes the plot frame, which touches the last marker). Series S2 (red diamonds): colour #ff0000, tolerance 60, open-px 15, marker size 20-1500 px, ROI 70 40 1535 920. Smaller openings left touching squares merged; open-px 26 gave the most separate squares without dropping any.
- Archives: `digitizations/Fig3_HorseChestnut_77K.json`, `digitizations/Fig3_TangerinePeel_77K.json`. Step-6 checks passed against Table 1 values: S1 at 20 bar (4.22 vs 4.24, 0.36%) and 80 bar (4.44 vs 4.47, 0.72%); S2 at 20 bar (1.82 vs 1.84, 0.93%) and 26 bar (1.86 vs 1.87, 0.47%).
- Not applied to the archives: the 1 bar Table 1 values do not reproduce from the plot. Run on copies in the work directory, the linear interpolation of the extracted markers at 1 bar gave 1.74 wt% (S1, printed 1.90, 8.4% off) and 0.82 wt% (S2, printed 0.89, 8.0% off), so the check at 1 bar fails at 5%. Interpolation between the sparse separable markers at low pressure underestimates a concave curve, but the printed values match the markers at 1.39 bar (S1, 1.885) and 1.19 bar (S2, 0.887). I kept both archives (four other stated values pass) and did not merge the 1 bar rows with plotted points (no marker within 0.02 bar of 1 bar). Reconciler should decide whether the Table 1 1 bar values belong to those markers.
- The last markers lie beyond the last labelled x tick (80 bar): S1 at 80.96 bar, S2 at 80.27 bar (x axis runs to about 82). Their pressures are linear extrapolations of the calibration; flagged `outside_axis_range` in the archives and in the notes.
- Marker counts (`isotherm_point_count`): S1 = 44, S2 = 27. These are approximate. The markers overlap heavily at low pressure, so the tool separated fewer than were counted:
  - S1: 22 extracted of 44 counted. Not separated: 4 squares at 0 to about 0.4 bar (partly hidden under red diamonds and the bottom frame), about 18 overlapping squares between about 1.7 and 15 bar. Counted from the stepped upper-left outline of the merged blob (square side 8 px at page resolution).
  - S2: 19 extracted of about 27 counted. Not separated: about 8 overlapping diamonds between about 2 and 7.3 bar (one blob, rejected as too large). The count in this blob is an estimate (plus or minus 3).
- Figure 3 adsorption uptake shows a maximum then a decline for S2 (1.87 wt% at 26 bar, 1.57 wt% at 80 bar) and a flat curve for S1 (about 4.44 wt% from 32 to 81 bar).

## Seen, not extracted

- Table 2 (journal p. 554): maximum H2 (wt%) and pressure for almond shell 2.53 (27 bar, ref. 1), pine cone 5.25 (80 bar, ref. 21), coffee bean waste 4.00 (40 bar, ref. 22), olive bagasse 2.59 (25 bar, ref. 23), fruit bunch 2.14 (20 bar, ref. 24), mandarin fruit 1.90 (25 bar, ref. 25): other materials from other papers, not measured here. The two "In this study" rows (4.47 at 80, 1.87 at 26) repeat Table 1.
- Text and abstract repeats of Table 1 values (1.90, 4.24, 4.47 at 80 bar; 0.89, 1.84, 1.87 at 26 bar) and of Langmuir 4.53 / 1.90: same values, no extra rows.
- Text "approximately 2.4 times higher" (4.53/1.90): a ratio, not an uptake value.
- Table 3 Langmuir B, Freundlich nF, KF, Temkin AT, B and all R2: model constants, not uptake values.
- Table 4 R2, k1, k2 and Table 5 (Boyd, pseudo-second-order Weber-Morris, Avrami R2, rate constants): kinetic parameters, no uptake values.
- Figure 1 (N2 adsorption-desorption isotherms at 77 K, volume in cc/g): N2, not H2. Figure 2 (DFT pore size distributions): characterization; the cumulative pore volume plateaus agree with V_DFT in Table 1.
- Figure 4 (linearized Langmuir plot, P/n against P, markers up to about 27 bar for both samples): not an isotherm, a transform of the Fig. 3 data; the y axis is labelled bar/mmol although the fit uses wt% (nm = 4.53 wt%). Not digitized; shows no value that the tables and text lack.
- Figure 5 (uptake H2 in mmol/g against time at 33, 55, 80 bar): kinetics, not digitized. Its plateaus (S1 about 3.2, 2.0, 0.5; S2 about 0.8, 0.65, 0.5 mmol/g) agree with Table 4 qe(exp). Time-resolved points are not extracted.
- Figures 6 and 7 (t/qt against t; qt against t^(1/2)): kinetic linearizations, no uptake values.
- Characterization without H2 rows: none (both samples have H2 rows).

## Coding decisions and inconsistencies in the paper

- Instrument: "Hiden IMI PSI" named, but the paper never says gravimetric or volumetric, names no uptake basis, gives no free-volume or buoyancy procedure. Coded measurement_method = unknown, uptake_type = unspecified, basis_stated = false, basis_inferred = unknown (instrumental default gives unknown for an unknown method), instrument_identified = true, calibration_described = false.
- wt% convention not defined ("H2 % (w/w)"): unknown / none for printed and digitized wt%. Table 4 rows carry W1 / computed_from_other_unit.
- Temperature of the kinetic runs (Table 4, Figure 5) is not stated in Section 3.3; 77 K taken from Section 2.3, which states that the H2 measurements were made at 77 K.
- Table 4 qe(exp) does not agree with Figure 3: S1 at 80 bar is 3.336 mmol/g = 0.672 wt% (W1) in Table 4 but about 4.44 wt% (22 mmol/g) in Fig. 3; S2 at 80 bar is 0.822 mmol/g = 0.166 wt% against 1.57 wt% in Fig. 3. The paper does not explain this. These rows carry no isotherm_id.
- Table 1 1 bar values do not coincide with a plotted marker at 1 bar (see digitization section).
- Langmuir rows carry no isotherm_id: the paper says the fit used "the experimental data" but does not tie it to the Fig. 3 curve or to a pressure range (Fig. 4 reaches only about 27 bar).
- Pore volumes: Vmicro and Vmeso are read as DFT values (text on p. 552 derives them from the DFT cumulative distribution); Vt (method not stated) stored as total pore volume; V_DFT = Vmicro + Vmeso (1.42 and 0.49 cm3/g) noted only. S_BET: BET, N2 at 77 K (Quantachrome Nova 2200e, degassed 105 C 24 h), P/P0 range and consistency criteria not stated; area_same_sample = yes (same named carbons as the H2 samples; H2 degassing 105 C for 4 h differs in duration only).
- Synthesis method coded chemical_activation (ZnCl2 impregnation, then pyrolysis, one route). Introduction says H2 storage of these two biomass carbons was studied in refs. 16 (tangerine peel) and 18 (horse chestnut shell) and the synthesis cites them, but the paper does not say these H2 values were published before, so no "previously reported" tag.
- measuring_lab_id: single author, corresponding author marked with *, first affiliation Balıkesir University.
