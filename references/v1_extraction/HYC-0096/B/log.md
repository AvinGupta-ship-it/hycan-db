# HYC-0096 extraction log (agent B)

Input: 33 page images of the main article (HAL deposit, pages main-01 to main-33). No supplementary file is in the input, so every value the paper places in the SI (Tables S1-S30, Figures S1-S7) is unavailable. All page numbers below are image page numbers (main-NN). rows.csv has 279 rows. Bibliographic fields are copied from paper.json (its title spells "Row Material Form"; the article page reads "raw material form").

## Sources extracted from

- main p.3, Abstract: 1.85 wt% at 77 K up to 1 bar (merged with the Table 11 row for PPAC_POW_CO2_1173), 3.45 wt% at 77 K up to 80 bar (merged with the run-1 77 K row), 0.28 wt% up to 80 bar at room temperature (merged with the room-temperature run-1 row).
- main p.7-8, section 2.2: instruments (Micromeritics ASAP 2460 up to 1 bar; f-PcT volumetric apparatus, ref. 46, for high pressure), degassing (473 K, 12 h, 10^-5 mbar), BET range (0.01-0.30 P/P0), NLDFT pore analysis, Toth model.
- main p.10-11, Table 2: synthesis parameters for the N2-carbonized samples. main p.11, Table 3: mass yields (in notes).
- main p.13, Table 4: BET SSA and NLDFT pore volumes for PPAC_WS/PEL/POW_N2_1173. main p.14, Table 5: EDX (in notes).
- main p.16, Figure 7: 77 K H2 isotherms up to 1 bar for PPAC_WS_N2_1173, PPAC_PEL_N2_1173 and PPAC_POW_N2_1173 (digitized, isotherms I1-I3).
- main p.17, Table 6: H2 uptake at 1 bar (± 0.01 wt%) for the three N2 samples (merged with the plotted highest-pressure point of each Figure 7 series).
- main p.17, text: Toth asymptotic capacity "wMax ~ 4.1" for PPAC_PEL_N2_1173 and PPAC_POW_N2_1173 (one row each, approximate, fitted_extrapolated).
- main p.18, Tables 7 and 8: synthesis parameters and yields of the CO2-carbonized samples. main p.20, Table 9: BET SSA and pore volumes. main p.21-22, Table 10: EDX (in notes).
- main p.23, Figure 12: 77 K H2 isotherms up to 1 bar for PPAC_POW_CO2_973, _1073 and _1173 (digitized, isotherms I4-I6).
- main p.23, Table 11: H2 uptake at 1 bar (± 0.01 wt%) for the three CO2 samples (merged with the plotted highest-pressure points).
- main p.23-24, text: Toth wt%MAX 5.17 for PPAC_POW_CO2_1173 (fitted_extrapolated); 1317 m2/g and 1.85 wt% at 1 bar (same as Tables 9 and 11).
- main p.25, Figure 14a: first 77 K adsorption/desorption run up to about 75 bar on PPAC_POW_CO2_1173 (digitized, I7). Figure 14b: all six 77 K adsorption runs (runs 2-6 digitized, I8-I12).
- main p.25-26, text: 3.45 wt% (first measurement of each day, "3.45 wt% at 80 bar"; merged with the highest-pressure points of runs 1 and 4) and 3.14 wt% at 80 bar ("the third of the first day"; merged with the run-3 highest-pressure point).
- main p.26, Figure 15a/b: room-temperature runs up to about 78 bar on PPAC_POW_CO2_1173; only the highest-pressure point of each run is extracted (I13 run 1, I14 run 2, I15 run 4, I16 run 5, I17 run 6). Text: 0.28 wt% at 80 bar (run 1).
- main p.26-27, Conclusion: 1.85 wt% at 1 bar and 77 K; 3.45 wt% at 77 K up to 80 bar (same measurements as above).

## Coding decisions applying to many rows

- Figures 7 and 12 plot H2 uptake against "Relative Pressure (p/p°)". The text says these isotherms run "at 77 K, up to 1 bar" and Tables 6 and 11 give the p/p° = 1 values "at 1 bar", so pressure_bar = p/p° x 1 bar. If p° were 1 atm, these pressures would be 1.3 % higher.
- Branches in Figure 7: the caption says adsorption/desorption, but both branches use identical markers and colours. Above p/p° of about 0.3 (0.5 for PPAC_POW_N2_1173, 0.77 for PPAC_PEL_N2_1173), the markers of each series form two interleaved pressure sets. The set that ends at the highest-pressure point is coded adsorption. The other set is coded desorption, and for the red and blue series its points also lie above the chord through their neighbours. Every other marker is coded adsorption, the default, because its branch cannot be read from the plot. The PPAC_PEL_N2_1173 desorption set (0.77, 0.84, 0.90) was assigned because it matches the desorption pressure set of the PPAC_POW_N2_1173 series.
- Branches in Figure 12: the caption calls these "adsorption isotherms", so all markers are coded adsorption. For PPAC_POW_CO2_973 and _1073, a second interleaved, slightly higher set is visible above p/p° of about 0.25 and is probably a desorption branch, but the paper does not say so.
- Basis: the paper never names excess, absolute or total. Every row has basis_stated false, uptake_type unspecified and basis_inferred excess (volumetric default). The paper gives no wt% convention.
- instrument_identified: true for the up-to-1-bar rows (Micromeritics ASAP 2460). False for the high-pressure and room-temperature rows: the f-PcT apparatus is cited to ref. 46, with no manufacturer or model and no home-built description in this paper. No free-volume or helium calibration is described.
- replicates_reported: true for the rows of isotherms I1-I6, because Tables 6 and 11 print ± 0.01 wt% for their 1-bar point, and for every PPAC_POW_CO2_1173 row, because six repeated 77 K and six room-temperature high-pressure runs are reported. False for the two "wMax ~ 4.1" Toth rows.
- Degassing (473 K, 12 h, 10^-5 mbar) is entered on every row except runs 2, 3, 5 and 6 (77 K and room temperature). The paper says that during cycling the sample was degassed only after each day's three measurements.
- Ultra-micropore volumes (Vult) are given in notes only, because the paper states no cutoff and the schema requires one. Super-micropore volumes (Vsup) are also in notes. Pore-volume method NLDFT with N2. Vmes printed as "-" for PPAC_POW_CO2_973 and _1073 is left empty.
- Text values printed "at 80 bar" are stored at 80 bar, as printed. The highest plotted pressure is about 75.5 bar at 77 K and about 77.6 bar at room temperature. The digitized points are in notes.
- Run 3: the text gives 3.14 wt% at 80 bar for "the third of the first day". The plotted run-3 end point is about 3.23 wt% (2.9 % higher). The run-6 end point, about 3.15 wt%, is closer. The printed value is recorded for run 3 as the paper says.
- Room-temperature run 1, highest point (about 77.6 bar, 0.283 wt%): Figure 15a draws it with an open (desorption) marker, while Figure 15b plots it in the run-1 adsorption isotherm. It is coded adsorption. Room temperature is not a number, so temperature_k is empty and temperature_unstated is true.
- Toth rows: wt%MAX is a model asymptote ("ideally to infinite" pressure), so pressure is empty with pressure_unstated true, and value_kind is fitted_extrapolated. The rows carry the isotherm_id of the fitted 77 K isotherm.
- The origin marker of Figure 14b run 6 digitized at -0.0047 wt%, less than 1 px below zero. It is stored as 0 and noted.

## Digitization notes

- Axes were calibrated on gridline and tick pixel positions. Fig. 7: x 0.0 at 207.11 px and 1.0 at 1099.93 px (check 0.4); y 0.00 at 1196.99 px and 2.00 at 699.12 px (check 1.00). Fig. 12: x 208.89 / 1114.89 (check 571.0), y 664.99 / 159.91 (check 412.0). Fig. 14a: x 0 at 181.09 and 70 at 569.58 (check 30), y 0 at 1428.09 and 3.5 at 1195.12 (check 1.5). Fig. 14b: x 709.0 / 1097.68, y 1428.09 / 1196.0. Fig. 15a: x 0 at 189.2 and 80 at 624.14. Fig. 15b: x 708.84 / 1142.43; y 0 at 998.97 and 0.25 at 795.14 (check 0.10). All third-tick checks passed (relative error under 0.3 %).
- Some points lie beyond the last labelled tick (p/p° slightly above 1.0; pressures above 70 bar in Figure 14). The tool flags these as outside the calibrated range; the linear calibration is used.
- Some series have several archives (part A, part B, ...) because the tool's region is rectangular. The parts exclude the legend (Figures 7 and 12) or the filled adsorption markers (Figure 14a open desorption markers). Each row's notes name its archive. The digitize_figure.py check passed for the Figure 7 and 12 part-A archives against Tables 6 and 11 at p/p° = 1. The other archives have no paper value at a plotted pressure, so they remain unchecked.
- Figures 7 and 12 used --open-px 3, which removes the dashed connecting lines. PPAC_PEL_N2_1173 used --open-px 2, because it lies under PPAC_POW_N2_1173 and most of its markers are partly hidden. Its centroids may be biased, so those rows have confidence 2.
- isotherm_point_count for I1-I6 is the number of markers the tool separated, plus one for each blob about twice a single marker (33 px or more). It is a lower bound, because markers hidden in the low-pressure stacks cannot be counted.

## Values seen but not extracted, with reasons

- Raw peach pit (no H2 uptake; characterization only): Table 1 EDX (C 68.05 wt% / 73.98 at%, O 31.80 / 25.95, K 0.13 / 0.03), FTIR (Figure 1), TGA/DTG (Figure 2: mass loss 69 % under N2, about 99 % in air, up to 1173 K).
- PPAC_POW_CO2_1273: synthesized but fully consumed (Table 8: 10.31 g to 0.00 g, mass loss 100 %). No characterization and no H2 uptake, so no row.
- Figures 3 and 8 (N2 isotherms), 4 and 9 (pore size distributions, cumulative pore volume), 5 and 10 (SEM), 6 and 11 (FTIR): not H2 uptake.
- Figure 13 and text p.24: isosteric heat of adsorption (blue curve about 9.0-9.4 kJ/mol up to 0.01 wt%; average 9.07 kJ/mol). Not an uptake value. It was derived from isotherms at 77 K, 279.65 K and 285.65 K up to 1 bar; the 279.65 K and 285.65 K isotherms are not shown in the main text.
- Toth heterogeneity parameter t (about 0.24 for the N2 samples; about 0.25 for PPAC_POW_CO2_1173): not an uptake.
- Room-temperature isotherms up to 1 bar for every sample (Figures S3 and S6) and the Toth parameters (Tables S15 and S29) are in the SI, which is not in the input.
- Figure 7 low-pressure stack (p/p° below about 0.015): red, green and blue markers pile up, with blue drawn on top. Only the markers in rows.csv could be separated. PPAC_PEL_N2_1173 lies under PPAC_POW_N2_1173: at p/p° 0.09-0.33 only partial markers were separated (confidence 2), and below 0.025 only three partial markers were found. Its other markers there are hidden.
- Figure 7 blobs about twice a single marker, each recorded once (second marker not separable): PPAC_WS_N2_1173 at p/p° 0.0130, 0.1041, 0.1877; PPAC_POW_N2_1173 at 0.0012, 0.2648, 0.3973; PPAC_PEL_N2_1173 at 0.5267, 0.5924, 0.6583, 0.7236.
- Figure 12 low-pressure stack (p/p° below about 0.015): markers of the three series overlap and only those in rows.csv were separated. Blobs about twice a single marker, each recorded once: PPAC_POW_CO2_973 at 0.1062; PPAC_POW_CO2_1073 at 0.0066, 0.0128, 0.1624, 0.2411; PPAC_POW_CO2_1173 at 0.0013, 0.0032, 0.0071, 0.1055, 0.3969, 0.4627.
- Figure 14a: the open desorption markers at about 4.0 bar (about 2.31 wt%) and about 75.5 bar (about 3.42 wt%) overlap filled adsorption markers and could not be separated (not extracted). The filled adsorption marker at about 15.5 bar lies mostly under an open marker; only its visible part was digitized (confidence 2).
- Figure 14b run 1 (black triangles): the same measurement as Figure 14a, and hidden under run 4 apart from one fragment, so it is not re-extracted. Run 2 (cyan): only the marker at about 70 bar is separable; the other 15 are hidden under runs 3-6. Run 3 (pink): 8 of 16 markers separable; the markers at about 0, 0.45, 3.7, 21.2, 26.8, 32.2, 37.6 and 43.0 bar are hidden or show only 3-4 px fragments. Run 4 (blue): the markers at 0 and 0.45 bar are hidden. Run 5 (red): the origin marker is hidden.
- Figure 15a/b (room temperature): only the highest-pressure point of each run is extracted, under the scope rule for temperatures other than 77 K. The run-3 (pink) highest-pressure marker is hidden under runs 4 and 5 and could not be separated, so room-temperature run 3 has no row. The run-1 highest point was taken from Figure 15a, because in Figure 15b it lies under run 2.
- Abstract and Conclusion characterization values (1317 m2/g, 0.60 cm3/g, about 85 % microporous, SSA and VT gains of 22.5 % and 23.5 %) are not uptakes; they are consistent with Table 9.
- main p.11 contains a broken cross-reference ("Erreur ! Source du renvoi introuvable.") in the TGA comparison; no value is lost.
