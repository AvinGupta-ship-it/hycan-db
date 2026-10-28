# HYC-0040 extraction log (agent A, claude-sonnet-5-5, 2026-10-28)

Input: HYC-0040_main (9 pages, text layer + page images). No supplementary file was in the input; the paper's Table S2 (surface areas of all samples, BJH pore data) and the XPS results are in the SI and were not available.

## Extracted from

- Table 1, p.7, "experimental" rows (rGO, B-rGO, Ni-B-rGO at 77, 273, 298 K, all at "20 bar"): 9 rows (M33, M34, M35, M64-M66, M101-M103). The same values are in the abstract, p.6 text and the Fig. 8 caption (one row each, not repeated).
- Table 1, p.7, "recalculated negating the weight of B / Ni" rows (B-rGO 11.38, 0.80, 0.33; Ni-B-rGO 8.41, 0.50, 0.19): 6 rows (M104-M109). Coded value_kind = unclear, wt% convention unknown, no isotherm_id, because they are authors' recalculations (formula not given), not measured points.
- Fig. 8 panel (i), p.7, 77 K, three series, all separable markers digitized: rGO 33 markers (32 digitized rows + the end point merged into M33); B-rGO 30 markers counted, 29 extracted (28 digitized rows + end point merged into M64); Ni-B-rGO 35 markers (34 digitized rows + end point merged into M101).
- Fig. 8 panel (ii), p.7, 273 K: all three series run through the tool (marker counts 23, 23, 23 = isotherm_point_count); only the highest-pressure point of each is used, and it is the plotted end point of the printed value, so it is merged into M34, M65, M102 (digitized value in notes).
- Fig. 8 panel (iii), p.7, 298 K: B-rGO (22 markers) and Ni-B-rGO (21 markers) run through the tool; highest-pressure point merged into M66 and M103. rGO has no plotted data (legend entry "rGO-no storage" only; confirmed by a green-colour extraction that found only the legend marker); its value is Table 1 "0" and p.6 text "negligible for rGO" (M35, no isotherm_id, uptake_bound approximate).
- p.6 Results text (pressure composition isotherm paragraph): same values as Table 1, used for cross-checking only.
- p.3 Experimental (GRC apparatus, degassing, 99.99% H2, nearly 200 mg), p.6 (degas at 100 C from TGA), Eq. 2 p.6 (wt% definition, W2): used for method fields.
- p.6 Results (rGO specific surface area 897 m2/g; Autosorb iQ N2 at 77 K named on p.3) and p.3-4 XRD (rGO d = 0.35 nm): used for rGO characterization.

## Values seen and not extracted

- Abstract values (0.24, 0.58, 8.2 wt% B-rGO; 6.9, 0.41, 0.16 wt% Ni-B-rGO): same measurements as Table 1, not duplicated.
- p.6: "net amount of hydrogen stored ... 3.7 g and 3.84 g" for B-rGO and Ni-B-rGO: a mass of H2 for an unstated amount of sample at unstated T and P, not per gram of sorbent. Not a usable uptake value.
- p.8 conclusions: "increase in the adsorbed amount by 1.6 wt.%" (B-rGO vs rGO at 273 K): a difference of two reported values, not a measurement.
- Fig. 9 / p.6-8: Raman spectra of hydrogenated Ni-B-rGO at 253, 268, 373 K and 20 bar, FTIR of hydrogenated Ni-B-rGO (Fig. 10): spectroscopic evidence of adsorbed H2 and C-H, no uptake value.
- Introduction values from other work (Wei 0.007/0.13/0.055 wt% at 293.15 K and 1 bar; Zhou 0.77 wt%; N-doped CNT 2 wt%; Pt/N-MC 1.26 wt%; Chung 0.4 and 3.2 wt%; Blankenship 0.8/1.2 wt% at 30 bar, 8.9 wt% at 30 bar and 77 K, 8.1 wt% at 77 K and 20 bar; Pd-AC 2.5 wt%; Banerjee 0.6 wt%; Pd3Co-graphene 4.6 wt%; Kaskun 0.298 wt%; DFT results): published by others, not measured here.
- GO: characterized (XRD d = 0.7 nm, Raman ID/IG 0.93, TGA 68% loss) but no H2 uptake, so no row and no sample number. Samples are numbered S1 rGO, S2 B-rGO, S3 Ni-B-rGO.
- Characterization with no schema field or no value in the main text: Raman ID/IG (rGO 0.95, B-rGO 0.99, Ni-B-rGO 1.05), crystallite size La (20.2, 19.4, 18.3 nm), TGA losses, Ni particle size 1-2 nm (in description), B and Ni contents (EDS, XPS in SI, no numbers in the main text), BJH pore size distribution (SI). Surface area, pore volumes of B-rGO and Ni-B-rGO are in SI Table S2 and are coded not_reported.

## Digitization record

- Calibration: tick centres found by sub-pixel centroiding of the tick marks on the page image. 77 K panel x ticks 1/9 (verify 5), y ticks 0/20 (verify 10); 298 K panel x ticks 0.02/0.22 (verify 0.12), y 0/20 (verify 10). All verification ticks agree within 0.12%.
- 273 K panel x axis: printed tick labels read 0.1, 0.2, 0.3, 0.3, 0.4, 0.5 on six equally spaced ticks, which is not a linear labelling (a third-tick check on the printed labels fails by 13%). The ticks sit at 0.05 + 0.1 n (first tick half a spacing from the spine, the same layout as the 77 K panel, origin at the spine where the curves start), and the printed labels are consistent with rounding of those values. Calibrated on tick 1 = 0.05 and tick 6 = 0.55, verified on tick 3 = 0.25 (0.04%). With this calibration the B-rGO and Ni-B-rGO end points (0.585, 0.414) reproduce the printed 0.58 and 0.41 within 1.1%. Calibrating on the printed labels 0.1 and 0.5 instead gave end points of 0.320 (rGO), 0.528 (B-rGO), 0.392 (Ni-B-rGO).
- rGO 273 K: the plotted end point (0.3251 wt%, 21.0 atm) is 7.1% below the printed 0.35 wt% (the dotted drop line sits at the plotted point, label printed 0.35%). The check against the paper's printed x could not be run (x = 0.35 is outside the digitized range); it was run at x = 0.32, which passes (3.8%). Same for Ni-B-rGO 298 K (plotted end 0.1527 vs printed 0.16, check run at x = 0.15, passes 0.25%). The panel calibration is shared with the series whose checks at the printed x pass (273 K: B-rGO 0.86%, Ni-B-rGO 0.01%; 298 K: B-rGO 0.31%).
- Checks at the printed values: 77 K rGO 0.96%, B-rGO 0.56%, Ni-B-rGO 2.11% (tool `check`, stated pressure 20 against digitized atm axis).
- Plot pressure axis is in atm; digitized pressures are converted x 1.01325 to bar. The end points plot at 20.3-21.0 atm while the paper states 20 bar; rows carry the printed 20 bar and the digitized pressure is in notes.
- Marker counts (tool output minus non-data detections = markers counted by eye on 3-5x enlargements): 77 K rGO 33 = 33; B-rGO 29 extracted vs 30 counted (see below); Ni-B-rGO 35 = 35; 273 K 23 = 23 for all three series; 298 K B-rGO 22 = 22, Ni-B-rGO 21 = 21.
- Marker not separated: 77 K B-rGO first marker (about 0.4 wt%, 0.9 atm), hidden behind the first Ni-B-rGO triangle (only a crescent of blue is visible). Counted in isotherm_point_count (30), not extracted.
- 298 K B-rGO first marker (near 0.017 wt%, 1 atm) is partly hidden by the Ni-B-rGO triangle (7 marker pixels): present in its archive with a biased centroid, not used in any row.
- 77 K B-rGO marker at 6.98 wt%, 15.5 atm is crossed by the dotted drop line of the Ni-B-rGO 6.9% label (14 marker pixels instead of about 23): extracted (row confidence 3), centroid may be biased.
- Non-data detections inside the archives (the archive holds the tool's raw output; the page has the legend and labels inside the plot area, so a rectangular region could not exclude them). Not used in any row. Listed as archive file: index (pixel x, pixel y): 77K_rGO: 1 (185.0, 148.0) legend marker; 77K_B-rGO: 0 (185.0, 178.8) legend marker; 77K_Ni-B-rGO: 3 (185.0, 209.8) legend marker; 273K_rGO: 2 (721.4, 141.5) legend marker; 273K_B-rGO: 0 (721.1, 172.1) legend marker and 22 (1113.5, 376.0) stroke of the "0.58%" label; 273K_Ni-B-rGO: 0 (721.0, 203.0) legend marker and 5 (819.5, 207.5) letter in the legend text; 298K_B-rGO: 1 (455.9, 629.9) legend marker; 298K_Ni-B-rGO: 2 (456.0, 660.8) legend marker. Black-series runs used --marker-min-px 11 to drop most text strokes (rejected groups are recorded in the archives).
- All eight archives are in digitizations/ with status passed. Colour tolerance 60, --open-px 2 (needed to keep markers split by dotted lines), ROI inside the axes.

## Coding decisions

- wt% convention: Eq. 2 (p.6) defines wt.%H = m(H2)/(m(sample)+m(H2)) x 100, so every wt% value in the paper (table, text, plot axis "Wt.% H") is W2, source stated. The recalculated Table 1 rows are unknown/none because their formula is not given.
- Basis: no excess/absolute/total named; Sieverts-type pressure-drop measurement, so basis_stated false, basis_inferred excess (instrumental default), uptake_type unspecified.
- Instrument: "Gas Reaction Controller (GRC) procured from Advanced Materials Corporation" taken as manufacturer plus product name, instrument_identified true. calibration_described false: the paper says the chamber was "calibrated using standard samples like LaNi5 and basolite (C-300)" but not how the free volume was determined.
- Degassing: 12 h (p.3 procedure) at 100 C (p.6, from TGA). "pressure was increased from 10^-3 atm to 20 atm" is a start pressure, not stated as the degas end pressure, so degas_end_pressure_pa is empty. Sample mass "nearly 200 mg" stored as 200.
- Lab: Flamina group, Indian Institute of Technology, Kanpur (corresponding author A. Flamina marked *, first affiliation); the paper names no other H2 laboratory.
- Merging table values with plotted end points: the figure annotates each end point with the printed value by a dotted drop line, so each is one measurement (rows M33, M34, M64-M66, M101-M103); the printed pressure (20 bar) is kept. The second-highest plotted point of the 77 K isotherms lies within 2% of 20 bar for rGO (20.11 bar), B-rGO (19.82 bar) and Ni-B-rGO (20.19 bar) but its value differs from the printed one, so it stays a separate digitized row.
- Classes: B-rGO doped_carbon with dopant B; Ni-B-rGO composite with dopant B and metal_element Ni (no loading in the main text). Synthesis: rGO and B-rGO thermal_reduction, Ni-B-rGO chemical_reduction (hydrazine hydrothermal Ni step).
- Surface area: rGO 897 m2/g coded BET (Autosorb iQ, N2 at 77 K named in the methods; the Results text calls it "specific surface area"), area_same_sample yes (same degas temperature), BET range not stated ("P/P0 between 0 and 1" is the measured range), consistency criteria not stated.
- rGO at 298 K: Table 1 prints 0, text says negligible; coded approximate with value 0.
- Not coded: H2 free-volume calibration gas and temperature, uncertainty, replicates (none reported).
