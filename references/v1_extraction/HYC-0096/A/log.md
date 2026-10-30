# Extraction log, HYC-0096 (Bartucci et al. 2024), extractor A

Input: main article only (34 pages, no SI file supplied). Rows: 269 (`rows.csv`). Digitization archives: 16 (`digitizations/`). Extraction date 2026-10-29.

## Sample numbering and isotherm ids

- Samples in order of first appearance (Table 2, then Table 7): S1 PPAC_WS_N2_1173, S2 PPAC_POW_N2_1173, S3 PPAC_PEL_N2_1173, S4 PPAC_POW_CO2_973, S5 PPAC_POW_CO2_1073, S6 PPAC_POW_CO2_1173.
- I1-I3: 77 K up to 1 bar, S1-S3 (Fig 7). I4-I6: 77 K up to 1 bar, S4-S6 (Fig 12). I7: S6 77 K, 1st run of 6 (Fig 14a, also the 1st run in Fig 14b). I8-I11: S6 77 K, 3rd, 4th, 5th, 6th run (Fig 14b). I12: S6 room temperature, 1st run (Fig 15a). I13-I15: S6 room temperature, 2nd, 5th, 6th run (Fig 15b).
- Basis: paper never names excess, absolute or total, so `basis_stated = false`, `uptake_type = unspecified`; `basis_inferred = excess` by the volumetric default (Micromeritics ASAP 2460 up to 1 bar, f-PcT volumetric apparatus up to 80 bar). wt% convention is not defined and no paired units are printed, so `unknown` / `none`.
- Measuring laboratory coded as the first marked corresponding author in the author line (Conte), first affiliation Universita della Calabria. Policicchio is also marked as corresponding author.
- Instrument: `instrument_identified = true` for the up-to-1-bar data (ASAP 2460 named); `false` for the 80 bar data (f-PcT volumetric apparatus, cited to ref. 46, not described as home-built and no manufacturer or model). No free-volume or buoyancy statement anywhere, so `calibration_described = false`. Sample mass and H2 purity are not stated.

## Extracted from

- Table 6 (p.17): 1.43, 1.77, 1.75 wt% at 1 bar, +/- 0.01. Merged with the highest-pressure plotted point of each Fig 7 curve (1.0039, 1.0011, 1.0039 bar); 3 rows (I1-I3), `uncertainty_wt_pct = 0.01`.
- Figure 7 (p.16), 77 K, up to 1 bar, H2 adsorption/desorption: PPAC_WS_N2_1173 (red) 33 markers, PPAC_POW_N2_1173 (blue) 35 markers, PPAC_PEL_N2_1173 (green) 12 distinguishable markers. Digitized rows: 32 + 34 + 11, plus the 3 merged Table 6 rows. Adsorption and desorption points use one marker style, so branches cannot be separated; all coded adsorption.
- Table 11 (p.23): 0.95, 1.38, 1.85 wt% at 1 bar, +/- 0.01. Merged with the highest-pressure plotted point of each Fig 12 curve (1.005, 1.0055, 1.0032 bar); 3 rows (I4-I6).
- Figure 12 (p.23), 77 K, up to 1 bar: 973 K (red) 32 markers, 1073 K (green) 32 markers, 1173 K (blue) 33 markers. Digitized rows: 31 + 31 + 32, plus the 3 merged Table 11 rows. One marker of the 1173 K curve sits on the axis origin (digitized x = 0.0); stored as half a pixel (0.000552 bar) because the validator rejects pressure 0 (noted in the row).
- Text p.17 (Section 3.2.2), Toth fit: "wMax ~ 4.1" for PPAC_PEL_N2_1173 and PPAC_POW_N2_1173 together; 2 rows, `uptake_bound = approximate`, `value_kind = fitted_extrapolated`, 77 K from context, pressure unstated, no isotherm_id.
- Text p.23-24 (Section 3.3.2), Toth fit: 5.17 wt%MAX for PPAC_POW_CO2_1173 (stated twice); 1 row, same coding.
- Figure 14a (p.25), 77 K up to 80 bar, 1st run: 15 filled markers (adsorption) and 11 open markers (desorption) digitized, 26 markers in all. Three desorption rings (about 3.8, 15.6 and 75.5 bar) overlap filled markers and were archived as one merged blob each, so their centroids lie between ring and filled marker (up to about 0.1 bar, 0.03 wt%); the filled marker at 15.6 bar is mostly covered by its ring (centroid of the visible crescent). The desorption origin ring has digitized y = -0.0008, stored as 0.
- Figure 14b (p.25), 77 K, runs 3-6 (adsorption only): run 3 10 markers, run 4 14, run 5 15, run 6 16 (including the origin marker; digitized y = -0.0006, stored as 0). Run 3 markers are partly hidden behind other runs; centroid of the visible part. `isotherm_point_count = 16` for each run is the number of marker stacks on the shared pressure grid.
- Text p.25 (abstract p.3, conclusion p.27): "3.45 wt%" for the first measurement at 77 K up to 80 bar (Fig 14a); 1 row (I7), 80 bar.
- Text p.25-26: "maximum storage capacity is reached in the first measurement of each day (3.45 wt% at 80 bar)"; 1 row for the first measurement of day 2 (4th run, I9). The 1st-run value is the I7 row above.
- Text p.26: "the third of the first day reaches a value of 3.14 wt% at 80 bar"; 1 row (I8, 3rd run). The figure disagrees: the plotted 3rd run ends at about 3.23 wt% (digitized 3.2309 at 75.43 bar) and the plotted 6th run ends at 3.143 wt%. Value kept as printed, attached to the 3rd run as the paper says, discrepancy in `notes`, confidence 3.
- Figure 15a (p.26), room temperature up to 80 bar, 1st run: highest-pressure marker only (open ring at 77.6368 bar, 0.2828 wt%); 1 row (I12). The ring marks the turning point and the same point is the last adsorption marker of run 1 in Fig 15b, so coded adsorption. 21 distinguishable markers counted (15 filled, 6 open).
- Figure 15b (p.26), room temperature, highest-pressure marker of runs 2, 5 and 6; 3 rows (I13-I15).
- Text p.26 (abstract p.3): "0.28 wt% at 80 bar" for the first room-temperature measurement; 1 row (I12). Temperature is only "room temperature", so `temperature_unstated = true` on every room-temperature row.
- Table 4 (p.13) and Table 9 (p.20): SSA (BET, N2, P/P0 0.01-0.30), Vmic, Vmes, VT (NLDFT, N2) carried on every row of S1-S3 and S4-S6; Vult and Vsup printed in `notes`. `ultramicropore_volume_cm3_g` left empty because the paper states no ultra-micropore cutoff and the schema then requires one.
- Table 5 (p.14) and Table 10 (p.21): EDX averages (C, O, K wt%) written into `material_description`; K is native to the precursor, so no metal or dopant field is set.
- Table 2 (p.10) and Table 7 (p.18): carbonization gas and range, activation gas, temperature and time written into `activation_method` and `material_description`.
- Section 2.2 (p.7-8): ASAP 2460 for up to 1 bar, f-PcT for high pressure, outgassing 473 K, 12 h, 1e-5 mbar (stored as 199.85 C, 12 h, 0.001 Pa) before each adsorption/desorption measurement, BET range 0.01-0.30 P/P0 (ref. 47 cited, no consistency criteria stated, `bet_consistency_criteria_stated = false`), NLDFT on N2 isotherms.

## Seen but not extracted

- Table 1 (p.9), raw peach pit EDX: raw material, no H2 measurement.
- Tables 3 and 8 (p.11, p.18), mass loss and yield: not uptake.
- PPAC_POW_CO2_1273 (Tables 7 and 8): final mass zero, no characterization and no H2 measurement; no sample, no row.
- Figures 3, 8 (N2 isotherms) and 4, 9 (pore size distribution): not H2.
- Figures 1, 2, 5, 6, 10, 11 (FTIR, TGA, SEM): no H2 values.
- Figure 13 (p.25), isosteric heat versus coverage up to 0.01 wt%: not an isotherm; the printed mean 9.07 kJ/mol is not an uptake value.
- Isotherms of PPAC_POW_CO2_1173 at 77, 279.65 and 285.65 K up to 1 bar used for the heat of adsorption (p.24): not plotted or tabulated in the main text.
- Room-temperature isotherms up to 1 bar of every sample (Figures S3, S6) and Tables S15, S29 (Toth parameters), S30 (literature comparison): SI not supplied.
- Abstract and conclusion repeats of 1.85 wt% (Table 11 row), 3.45 wt% (I7 row) and 0.28 wt% (I12 row): one row each, not duplicated. Abstract "about 1317 m2/g" and "0.60 cm3/g" repeat Table 9 (1316.8, 0.593).
- Figure 14b, 1st run (black triangles) and Figure 15b, 1st run: same measurement as Figures 14a and 15a; not digitized again.
- Figure 14b, 2nd run (cyan triangles), 77 K: markers hidden behind other runs; only three slivers of 9, 17 and 60 pixels were found (about 21.7, 59.3 and 70.0 bar). Not extracted, no row.
- Figure 14b, runs 3, 4 and 5: markers at the origin and at 0.3-0.5 bar are hidden behind run 6 and run 5; runs 3 and 4 are also hidden at several higher pressures. Only distinguishable markers were extracted (run 3 10 of 16, run 4 14 of 16, run 5 15 of 16).
- Figure 15b, runs 3 (magenta) and 4 (blue): highest-pressure marker hidden behind other runs (12 and 73 pixel fragments); not extracted.
- Figure 7: low-pressure markers of the green (PPAC_PEL_N2_1173) curve under the blue markers, and any red markers hidden under blue ones at p < 0.005 bar, cannot be counted; counts are of distinguishable markers. The first two green blobs (0.5246 and 0.5297 bar, 1.5749 wt%) look like two overlapping markers and are two rows.
- Figure 14a: a possible filled marker under the origin ring, and desorption markers that coincide with filled markers, cannot be separated. The 9-pixel fragment at 15.33 bar belongs to the 15.6 bar marker. Blobs from the legend markers and legend text (Figure 14a at about 64 bar and 67-76 bar, y < 0.4 wt%) were excluded.
- Legend markers picked up by the tool and excluded: Figure 7 (0.5941 bar; 0.5123, 0.3395, 0.1708 wt%), Figure 12 (0.5701, 0.5701, 0.5695 bar; 0.5128, 0.3405, 0.1703 wt%), Figure 14b runs 3-6 (48.8 bar; 1.0257, 0.5379, 0.295, 0.0519 wt%).
- Figures 7 and 12 x axes read "Relative Pressure (p/p0)"; read as bar because captions and tables say "up to 1 bar" and the top points match the 1 bar table values.

## Digitization checks (`digitize_figure.py check`)

- Passed: Fig7 WS, PEL, POW; Fig12 973, 1073, 1173 (against Tables 6 and 11 at 1 bar); Fig14a adsorption (3.4016 against 3.45, 1.40%) and desorption (3.4391 against 3.45, 0.32%); Fig14b run 4 (3.4527 against 3.45, 0.08%); Fig14b run 6 (3.1429 against 3.14, 0.09%); Fig14b run 3 (3.2310 against the printed 3.14, 2.90%, inside the 5% tolerance but see the discrepancy above).
- Not checkable: Fig14b run 5, Fig15a, Fig15b runs 2, 5, 6 (the paper prints no value for them; Fig15a and the Fig15b archives hold a single marker, and `check` rejects x at the end of a one-point range). The third-tick axis verification passed on every archive.
