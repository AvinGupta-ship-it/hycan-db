# HYC-0052 extraction log (agent B)

Input: page images main-1 to main-5 (no supplementary file). Samples: S1 = AX-21 (activated carbon), S2 = MWNT. No non-carbon sorbent is measured.

## Sources extracted

- main-3 (p. 477), Table 1, "Amount of H2 adsorbed on AX-21 at 6 MPa, wt%" (298, 273, 253, 233 K): 4 rows. The 233, 273 and 298 K values are the same measurement as the highest-pressure Fig. 3 marker of that isotherm (digitized pressure within 1.2 bar of 60 bar) and are merged into one row each (M1, M4, M5). The 253 K value (M2) is not a plotted point.
- main-3 (p. 477), Table 1, "Amount of H2 adsorbed on MWNT at 6 MPa, wt%" (298, 273, 253, 233 K): 4 rows (M6, M8, M10, M12). None of them is a plotted point (nearest markers 1.5 bar or more from 60 bar), so they have no isotherm_id and value_kind = unclear.
- main-2 (p. 476), Fig. 3, H2 wt% against p/MPa, activated carbon on the left axis (0 to 1.0) and MWNT on the right axis (0 to 0.50, "double enlarged"); 9 isotherms at 233 to 318 K, none at 77 K, so only the highest-pressure marker of each is extracted: AC 253 K (M3, new row), MWNT 233, 253, 273, 298, 318 K (M7, M9, M11, M13, M14). The AC 233, 273 and 298 K highest-pressure markers merged with Table 1 (see above).
- main-1 (p. 475) section 2 and main-2 (p. 476) sections 2 to 4: sample descriptions, AX-21 area and pore volume, MWNT BET area (N2, 77 K, ref. [21]), degassing (393 K, 24 h plus 4 h in situ), apparatus and helium-expansion free-volume calibration, sample masses (about 20 g AX-21, 8.61 g MWNT), temperatures (233 to 298 K, 20 K steps, plus 318 K for MWNT only), pressures up to 11 MPa.
- main-1 title block: corresponding author L. Zhou (marked *), affiliation a "... Tianjin University ..." gives measuring_lab_id "Zhou group, Tianjin University".

## Digitization (Fig. 3, main-2.png)

- Axis frame and ticks located from pixel rows and columns: left frame x = 654.38 (p = 0.0), right frame x = 987.83 (p = 12.0), check tick 6.0 at x = 820.61 (predicted 5.982, 0.3%). Bottom frame y = 1303.20 (0.0 / 0.00), top frame y = 960.70 (1.0 / 0.50); check tick left 0.5 at y = 1133.0 (predicted 0.4969, 0.6%), right 0.25 at y = 1132.8 (predicted 0.2488, 0.5%). Other inner ticks agree within 1 px.
- Figure is greyscale; all series are black. Each target marker was isolated with a tight --roi around its bounding box (colour #000000, tolerance 250, --mode markers, --open-px 0, --marker-min-px 5); one marker extracted per run, matching the one marker in each region. Archives in digitizations/, one file per marker.
- Archives behind rows: fig3_AC_233K_end, fig3_AC_253K_end, fig3_AC_273K_end, fig3_AC_298K_end, fig3_MWNT_233K_end, fig3_MWNT_253K_end, fig3_MWNT_273K_end, fig3_MWNT_298K_end, fig3_MWNT_318K_end.
- Archives used only for the table/figure merge check (no row of their own): fig3_AC_253K_check_penultimate (57.97 bar), fig3_MWNT_233K-253K_check_near6MPa (58.24 bar), fig3_MWNT_298K_check_near6MPa (58.53 bar), fig3_MWNT_273K_check_below6MPa (52.97 bar), fig3_MWNT_273K_check_above6MPa (63.80 bar).
- AC 233 K merge is borderline: highest marker digitized at 58.90 bar, 1.10 bar from the printed 60 bar against the 1.2 bar limit.
- Markers that could not be separated: MWNT 233 K and 253 K end markers overlap (up-triangle partly behind down-triangle), and MWNT 298 K and 318 K end markers overlap; each was digitized with a region drawn tight around its own outline, which includes a few pixels of the neighbour (extraction_confidence 2). Near 5.8 MPa the MWNT 233 K and 253 K markers are superimposed and were digitized together for the merge check only.
- digitize_figure.py check was not run: each archive holds one point, and the check requires the queried pressure to lie inside the series range.
- isotherm_point_count (origin marker at (0,0) excluded in all series; counts approximate because markers overlap near the origin): AC 233 K 20, AC 253 K 20, AC 273 K 17, AC 298 K 16 (markers below about 1 MPa partly hidden); MWNT 233 K 13, 253 K 13, 273 K 13, 298 K 14, 318 K 14 (MWNT series overlap heavily below about 3 MPa, most 253 K markers sit behind 233 K markers; counts estimated to about +/-2).

## Values seen but not extracted

- Fig. 3: all markers other than the highest-pressure marker of each isotherm (isotherms at 233 to 318 K, not 77 K; protocol extracts only the highest-pressure point).
- Table 1, column n_AC/n_NT (3.6, 3.7, 4.2, 5.1): ratio of the two samples' uptakes, computed from several samples; not a row.
- Table 1, column c_AC/c_NT (0.16(6.25), 0.17(5.9), 0.19(5.3), 0.23(4.3)): ratio of surface concentrations of the two samples (inverse in parentheses); not a row.
- Fig. 4 (main-3): n_AC/n_NT against T at 6.0 MPa (four points, 233 to 298 K); ratio plot, not an isotherm; not digitized; values are those of the Table 1 ratio column.
- Fig. 5 (main-4): isosteres of H2 on MWNT, ln p (MPa) against 1/T at fixed amounts 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.19, 0.21 wt% (five temperatures each); not an isotherm figure; not digitized. The (T, p, amount) combinations it shows are not given in tables or text.
- Fig. 6 (main-4): isosteric heat -dH (about 1.73 to 1.59 kJ/mol) against amount adsorbed 0.12 to 0.21 wt% for MWNT; not an uptake; not digitized.
- Text (main-3, main-4) and abstract: isosteric heats -1.7 kJ/mol (MWNT, average) and -6.4 kJ/mol (AX-21, previously reported, ref. [20]); not uptake values.
- Text and abstract: "3.6-5.1 times higher" (AC versus MWNT at 6 MPa), "3-5 times less", "surface concentration ... 4-6 times higher", "3000/137 = 21.9": ratios across samples; not rows.
- Abstract and conclusion: ranges "233-298 K", "pressures up to 11 MPa": conditions, not values.
- Characterization recorded on rows, not as separate rows: AX-21 specific surface area about 3000 m2/g and pore volume about 1.3 cm3/g (method and measuring party not stated); MWNT BET 137 m2/g (N2, 77 K, cited to ref. [21]). MWNT wall thickness and inner diameter about 10 nm (from TEM, Fig. 1) recorded only in material_description, not as a pore diameter.
- Experimental figures not uptake: reference-cell temperature constant within +/-0.05 K, adsorption-cell temperature constancy +/-0.1 K, transducer linearity deviation below 0.05% over 20 MPa (Keller PAA-23/8465.1-200).
- Fig. 1 (TEM image) and Fig. 2 (apparatus schematic): no values.
