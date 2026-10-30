# HYC-0087 extraction log (agent B, 2026-10-29)

Bicil 2025, Sakarya University Journal of Science 29(5) 550-561. Pages read from images main-01 to main-12 (no SI files supplied). 55 rows written. Samples: S1 = Tangerine peel (first named in keywords and abstract), S2 = Horse chestnut shell. No non-carbon sorbent is measured in this paper.

## Sources extracted from

- Table 1 (main-03, p. 552): H2 % (w/w) at 1 bar and 20 bar and the "Maximum value" (H2 %, pressure) for both samples -> M6, M7, M14 (Tangerine peel), M30, M44, M45 (Horse chestnut shell). SBET, Vt, Vmicro, VDFT, Vmeso -> characterization on every row of each sample.
- Section 3.1 text (main-03, p. 552): repeats the Table 1 uptake values (1.90/4.24/4.47 and 0.89/1.84/1.87 wt%) and BET areas (2128, 1230 m2/g); same rows, not duplicated.
- Abstract (p. 550), Introduction (p. 551), Section 3.1 text and Table 2 (main-05, p. 554), Conclusion (p. 559): repeat 4.47 wt% at 80 bar and 1.87 wt% at 26 bar; same rows as M44 and M7.
- Section 2.1 (p. 551): synthesis (ZnCl2 activation; 600 °C for horse chestnut shell, 700 °C for tangerine peel). Section 2.2 (p. 552): N2 at 77 K, Quantachrome Nova 2200e, degassed 105 °C for 24 h. Section 2.3 (p. 552): Hiden IMI PSI, 77 K, degassed 105 °C for 4 h before H2 analysis.
- Figure 3 (main-04, p. 553), hydrogen adsorption isotherms at 77 K (Section 3.1 text): both series digitized; archives `digitizations/HYC-0087_fig3_tangerine_peel.json` (13 points) and `digitizations/HYC-0087_fig3_horse_chestnut_shell.json` (20 points). Rows M1-M13 (I1) and M25-M44 (I2); the points at 20 and 26 bar (Tangerine peel) and 20 and 80 bar (Horse chestnut shell) are merged with the Table 1 values.
- Table 3 and text (main-06, p. 555): Langmuir nm 1.90 and 4.53 %wt. -> M15, M46 (fitted_extrapolated, no pressure).
- Table 4 (main-08, p. 557): qe(exp), pseudo-first-order qe(cal) and pseudo-second-order qe(cal) in mmol/g at 80, 55 and 33 bar -> M16-M24, M47-M55.

## Figure 3 digitization

- Axes have no tick marks; tick positions are the centres of the tick-label bounding boxes found from pixel rows and columns. x: 0 -> 721.0, 20 -> 809.0, 40 -> 896.0, 60 -> 984.0, 80 -> 1072.0 px. y: 0 -> 1297.5, 0.5 -> 1275.5, 1 -> 1253.5, 1.5 -> 1231.5, 2 -> 1210.5, 2.5 -> 1188.5, 3 -> 1167.5, 3.5 -> 1145.5, 4 -> 1123.5, 4.5 -> 1101.5, 5 -> 1080.5 px. Calibration on 0/80 and 0/5; check ticks x 40 (predicted 39.886, 0.28%) and y 2.5 (predicted 2.512, 0.46%). Plot frame: left 721.5, right 1081 (about 82 bar), top 1080.5, bottom 1298.
- Work copy `work/main-04_legend_blanked.png`: the legend box (x 918-1072, y 1253-1293) painted white so its markers are not read as data; nothing else changed.
- Horse chestnut shell: colour #000000, tolerance 40, ROI 712 1083 1079 1305, `--open-px 4` (breaks the frame-line bridge between the 0.57-bar square and a hidden square), marker size 45-80 px. The 0.91-bar square touches the frame and carries 8 frame pixels (72 px), which moves its centroid about 0.5 px (0.11 bar) toward lower pressure.
- Tangerine peel: colour #ff0000, tolerance 40, ROI 712 1075 1088 1305, default opening, marker size 15-45 px.
- Sanity checks (`digitize_figure.py check`, recorded in the archives, status passed): Horse chestnut shell 4.232 at 20 bar vs 4.24 printed (0.19%), 4.443 at 80 bar vs 4.47 (0.61%); Tangerine peel 1.833 at 20 bar vs 1.84 (0.41%), 1.865 at 26 bar vs 1.87 (0.26%).
- The last marker of each series (80.80 and 80.30 bar) lies beyond the last labelled tick (80) but inside the frame; the tool flags it as outside the calibrated range.

### Markers counted but not separated (not extracted)

- Horse chestnut shell, 44 markers counted (approximate), 20 separated. Not separated: (a) one merged group of 957 px between about 1.7 and 16 bar (rejected by the digitizer as too large); counting its visible top-left and bottom-right square corners gives 20 squares; (b) at least 4 squares near 0 bar (located from pixel positions, for orientation only: two stacked at about 0 to 0.15 wt%, one near 0.5 wt%, one near 0.9 wt%) drawn under the tangerine-peel diamonds and visible only as edge fragments (one 32-px fragment rejected as too small). Values for these were not read.
- Tangerine peel, 25 markers counted (approximate), 13 separated. Not separated: (a) a 69-px group of 2 overlapping diamonds at about 0.1 bar near 0 and 0.14 wt%; (b) a 282-px group between about 0.9 and 9 bar along which diamonds overlap into a continuous band; a template cover gives about 10 diamonds, but markers stepping along the band direction leave no outline features, so the count is uncertain by a few markers. Values for these were not read.
- Corner detection and the template cover were used only to count markers, never to produce values. `isotherm_point_count` (25 for I1, 44 for I2) carries these approximate counts.
- Neither series shows a desorption branch.

## Values seen and not extracted

- Table 2 (p. 554) and text p. 554: literature maxima for other carbons, not measured in this paper: almond shell 2.53 wt% at 27 bar [1], pine cone 5.25 at 80 [21], coffee bean waste 4.00 at 40 [22], olive bagasse/olive pulp 2.59 at 25 [23], fruit bunch 2.14 at 20 [24], mandarin fruit/tangerine fruit 1.90 at 25 [25].
- Table 3 (p. 555): Langmuir B 0.53 and 0.79 (units not stated) and R2 0.9920 and 0.9955 (recorded in notes of M46, M15); Freundlich nF 2.27 and 2.27, KF 1.37 and 0.64, R2 0.9626 and 0.8991; Temkin AT 0.57 and 0.25, B 2.18 and 0.99, R2 0.9206 and 0.9662. Model constants, not uptake values.
- Table 4 (p. 557): pseudo-first-order R2 and k1, pseudo-second-order R2 and k2. Rate constants and fit statistics, not uptake values.
- Table 5 (p. 559) and text pp. 558-559: Boyd (R2, R, A), Weber-Morris (R2_1, k1, R2_2, k2; k1 4.834 and 0.982 mmol g-1 min-1/2 at 80 bar in the text), Avrami (R2, nAV, KAV), R2 ranges 0.2855-0.4988 and 0.5995-0.8443. Kinetic parameters, not uptake values.
- Figure 1 (p. 552): N2 adsorption-desorption isotherms at 77 K; not H2.
- Figure 2 (p. 553): DFT pore-size distributions; characterization only (Vmicro, Vmeso, VDFT taken from Table 1).
- Figure 4 (p. 556): linearized Langmuir plot (P/n against P, up to about 27 bar); not an isotherm, not digitized; its points are transforms of Figure 3 points and give no value beyond Figure 3 and Table 3. Its y-axis is labelled bar/mmol although Table 3 gives nm in %wt.
- Figure 5 (p. 556): uptake (mmol/g) against time, 0-4 min, at 80, 55 and 33 bar for both samples, with fitted curves; kinetics, not digitized. The time-resolved uptakes are not in any table; the equilibrium values are Table 4 qe(exp) (extracted).
- Figure 6 (p. 557, t/qt against t) and Figure 7 (p. 558, Weber-Morris qt against t1/2): kinetic transforms, not digitized; the time-resolved values they show are not in any table.

## Discrepancies and coding decisions

- Table 1 "1 bar" values do not match the plotted points near 1 bar. Horse chestnut shell: 1.90 wt% printed; Figure 3 has 1.682 wt% at 0.91 bar and 1.889 wt% at 1.48 bar (digitized). Neither is within 0.02 bar of 1 bar, so M45 has no isotherm_id. Tangerine peel: the markers near 1 bar are in the merged group, so M14 could not be matched and has no isotherm_id. No `check` was run at 1 bar.
- Tangerine peel: the text calls 1.87 wt% at 26 bar the maximum, and p. 554 says this carbon "was tested under low pressure conditions", but Figure 3 plots it to about 80 bar, falling to 1.568 wt%.
- Table 4 qe(exp) values are far below the isotherm values for the same sample and pressure (Horse chestnut shell 3.336 mmol/g = 0.672 wt% at 80 bar vs 4.47 wt%; Tangerine peel 0.822 mmol/g = 0.166 wt% at 80 bar vs 1.568 wt% digitized). Recorded as printed. The kinetic runs are a separate experiment (Figure 5), so they were not merged with Figure 3 points even where the pressure tolerance is met (80 and 55 bar for Horse chestnut shell), and they carry no isotherm_id. The temperature (77 K) comes from the general statement in Section 2.3.
- Langmuir nm rows: pressure_unstated = true because the value is a model capacity with no pressure. isotherm_id not assigned because the paper says only that the "experimental data" were fitted, without naming a run.
- measurement_method = volumetric_sieverts from the named Hiden IMI PSI manometric instrument (the paper does not say "volumetric"). Hence basis_inferred = excess (instrumental default); the paper never names excess, absolute or total, so basis_stated = false.
- pore_volume_method = DFT: the text gives Vmicro and Vmeso with the DFT distribution, and Vmicro + Vmeso = VDFT for both samples. The method for Vt is not stated.
- area_same_sample = yes: the BET and H2 measurements are on the same activated carbons (degassed at 105 °C for 24 h before N2 and for 4 h before H2).
- The synthesis procedures cite ref. [18] (horse chestnut shell) and ref. [16] (tangerine peel), whose titles are hydrogen-storage studies of these carbons. The paper does not say that these H2 values or isotherms were reported before, so no `previously reported` note was added.
- p. 559 calls the horse chestnut sample "horse chestnut peel"; taken to be the same sample.
