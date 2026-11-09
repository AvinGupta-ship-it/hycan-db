# HYC-0112 extraction log (agent B)

## Sources extracted
- main p.5-6 (Experimental): N2 sorption (Quantachrome Autosorb iQ), BET range P/P0 0.02-0.22, total pore volume at P/P0 ca. 0.99, t-plot micropore area/volume, NLDFT PSD; H2 by Hiden IGA-003 gravimetric, 99.9999% H2, 0-20 bar, degas 10^-10 bar at 523 K overnight; measurements at 77, 87, 298, 308 K.
- main p.9 text: surface areas and pore volumes (differ from Table 1 for CEMC pore volume 1.91 vs 1.71, Pt5CEMC 2049/1.06 vs 2047/1.01, Pt10CEMC 1249 vs 1279); Table 1 values used, text values in notes.
- main p.11 Table 1: textural properties; H2 uptake 77 K/20 bar (6.33, 4.58, 3.99 wt%) and 298 K/20 bar (0.20, 0.18, 0.17 wt%). Each merged with the plotted 20 bar point (rows M1-type table_direct rows).
- main p.15 text: buoyancy correction (sample density 1.5 g cm-3, adsorbed H2 density 0.04 g cm-3); 77 K values repeated.
- main p.17 text: 298 K values repeated (Pt10CEMC printed as "Pt10ECMC").
- main p.16 Fig. 6 left (77 K): all six series digitized (CEMC-ad taken from Fig. 7, see below). Archives: fig6_77K_Pt10CEMC-ad, fig6_77K_Pt5CEMC-ad, fig6_77K_CEMC-de, fig6_77K_Pt5CEMC-de, fig6_77K_Pt10CEMC-de.
- main p.16 Fig. 6 right (298 K): highest-pressure point of CEMC, Pt5CEMC, Pt10CEMC (all merged with Table 1).
- main p.18 Fig. 7 left/right main panels: 77 K series of CEMC and Pt5CEMC (all points), 87 K highest-pressure points.
- main p.18 Fig. 7 insets: 308 K highest-pressure points; 298 K series are the Fig. 6 298 K runs replotted (not re-extracted).

## Digitization notes
- Calibration: Fig. 6 left x 0/20 (px 218/550, check 10 at 384), y 0/6 (px 691/240, check 3 at 466); Fig. 6 right x 0/20 (719/1047, check 883), y 0/0.20 (680/222, check 0.10 at 451); Fig. 7 CEMC x 0/20 (240/579, check 410), y 0/6 (1404/951, check 3 at 1178); Fig. 7 Pt5CEMC x 0/20 (697/1035, check 866), y 0/4 (1404/987, check 2 at 1196); insets x 0/20 with check 10 (CEMC 415/564/489; Pt5 877/1026/952), y 0/0.20 with check 0.10. All third-tick residuals < 0.7%.
- Legends, panel labels and insets were masked (white) on copies of the page image before extraction (p16_nolegend.png, p16_298_nolegend.png, p18_main_masked.png, p18_inset_masked.png in work/).
- Open markers (Fig. 6 77 K -de series) cannot be isolated by colour from their lines and overlapping filled markers. Their centres were located on the page image from the enclosed interior (hole) centroids, or for Pt10CEMC-de by outline template matching after subtracting the rendered Pt10CEMC-ad series; the located centres were rendered as solid silhouettes on blank page-size images (work/derived_fig6_77K_*.png, spec in work/derive_spec.json) and extracted with digitize_figure.py on the same calibration. Every centre was checked by overlay on the page (work/ov_de_low.png, ov_de_hi.png).
- Fig. 6 CEMC-ad: several filled markers are hidden under open CEMC-de markers. Fig. 7 left 77 K series coincides with it point for point (same run replotted), so the CEMC 77 K adsorption branch was digitized from Fig. 7 (16 markers). Not extracted twice.
- Fig. 6 Pt5CEMC-ad: 9 filled markers from 5.5 to 18 bar extracted; markers below about 4 bar (about 6, at 0-2.5 bar) overlap the Pt10CEMC and CEMC markers and could not be separated; their 20 bar marker is hidden under the open -de marker. Not extracted.
- Fig. 6 Pt5CEMC-de: about 3 low-pressure markers below 2.5 bar not separable (only one partial marker at 2.56 bar extracted).
- Fig. 6 CEMC-de: about 2 markers below 1 bar overlap the Pt10CEMC/Pt5CEMC stack at the y-axis; not extracted.
- Fig. 6 Pt10CEMC-de: the open marker at about 18 bar lies under filled markers and is not separable; not extracted (counted).
- Fig. 7 Pt5CEMC 77 K: two markers at the origin partly under the 87 K diamonds/x-axis; not extracted.
- Fig. 7 Pt5CEMC (main panel 77 K) is a different point set from Fig. 6 Pt5CEMC-ad, so it is coded as a second run (I6); CEMC Fig. 7 and Fig. 6 points coincide (same run).
- Two digitized pressures were slightly negative (markers on the y-axis) and stored as 0, noted in the row.
- digitize_figure.py check (stated vs digitized at 20 bar): PASS for CEMC 77 K (6.33), Pt10CEMC 77 K (3.99), Pt5CEMC 77 K (4.58), CEMC 298 K (0.20), Pt5CEMC 298 K (0.18). FAIL for Pt10CEMC 298 K: plotted 0.141 wt% vs printed 0.17 wt%; same panel calibration reproduces the other two Table 1 values, so this is a paper inconsistency; printed value kept on the row, archive marked discarded by the tool.

## Values seen but not extracted
- Fig. 6 right and Fig. 7 insets: points below 20 bar at 298 and 308 K (only highest-pressure point per isotherm is in scope); Fig. 6 right desorption branches.
- Fig. 7 87 K points below 20 bar (not 77 K).
- Fig. 8: isosteric heats vs uptake (not isotherms). Qst values in abstract/text (7.8, 8.3, 72, 20.8, 17.9, 2.6, 5.4, 0.9, 5.0 kJ/mol) and the coverages at which they are quoted (0.08, 0.014, 0.073, 0.13, 0.18, 1.3, 2.6, 5.0 wt%) are not uptake measurements at stated T and P.
- Fig. 1 XRD, Fig. 2 N2 isotherms and NLDFT PSD, Fig. 3 SEM, Fig. 4 TEM, Fig. 5 Pt particle-size histograms: characterization only (PSD modes 1.1 and 2.0 nm, Pt particles 1-4 nm / 2-5 nm recorded in descriptions/notes).
- Zeolite EMC-2 template: no H2 uptake given; no non-carbon sorbent values in the paper.
- Introduction p.3: "far below 1 wt.%" ambient-temperature capacities refer to literature, not to this paper's samples.

## Digitized points not written as rows
- Three digitized markers lie on the y-axis and their pressure digitizes as 0 or slightly negative (-0.049 and -0.025 bar), which the schema rejects (pressure must be > 0): Fig. 7 left CEMC 77 K first marker (0.174 wt%), Fig. 6 left Pt10CEMC-ad origin marker (0, 0), Fig. 6 left Pt10CEMC-de lowest marker (0.952 wt%). They remain in the archives and in isotherm_point_count but have no row.
