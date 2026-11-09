# HYC-0106 extraction log (agent A, claude-sonnet-5-5), 2026-10-29

Rows written: 202 (rows.csv). Validator: `validate_row_detail.py --errors-only` reports no errors (only the expected warning that `uptake_type` is `unspecified`, because the paper never names the uptake basis).

Page references: "p." is the journal page (main article pages 1029-1040 = PDF pages 1-12); SI pages are the PDF pages of si1.

## Conventions and assumptions

- Samples numbered S1-S6 in Table 1 order (CG_N2+CO2, CG_CO2, CG_PC_KOH, CG_KOH, CG_PC_DA, CG_DA). CG and CG_PC have no H2 uptake value, so they get no sample_id and no row.
- Isotherms: I1-I6 = Fig. 6a-f (77 K, ASAP 2460, adsorption and desorption); I7 = Fig. 8a (CG_PC_KOH, 77 K, HPVA II, to 70 bar); I8 = Fig. 9a (CG_PC_KOH, 298 K, HPVA II); I9 = Fig. 9b 1st cycle (298 K); I10, I11, I12 = Fig. S7 at 77, 273, 300 K.
- Fig. 6 and Fig. S7 x axes are printed as relative pressure p/p0. p0 is not given. `pressure_bar` = p/p0 x 1 bar (assumption, stated in notes of every such row); Table 3 pairs the p/p0 = 1.00 end of the Fig. 6 isotherms with 1 bar.
- Fig. 8 and Fig. 9 x axes are in bar (absolute assumed; the paper does not say gauge).
- Temperatures: "77 K", "298 K" (printed as "room temperature (298 K)" in the text and "RT" in Fig. 9), 273 K and 300 K are printed numbers, so `temperature_inferred` = false everywhere.
- Basis: the paper never names excess, absolute or total. `basis_stated` = false, `uptake_type` = unspecified, `basis_inferred` = excess by the instrumental default. The paper calls the HPVA II "high-pressure volumetric analyzer" but never calls the Micromeritics ASAP 2460 volumetric; `volumetric_sieverts` for the ASAP rows is coded from the instrument type (noted on those rows).
- wt% convention: Sec. 2.2 defines "weight percent of adsorbed gas per gram of adsorbent", so W1, source `stated` (quote in notes).
- Digitized values: `digitize_figure.py extract --mode markers`, calibration on the lowest and highest labelled ticks with a third-tick check (all verification errors below 0.2 %). Archives: 19 JSON files in `digitizations/`. `check` against a paper value passed for all Fig. 6, Fig. 8a and Fig. 9a archives; Fig. 9b and the three Fig. S7 archives are `unchecked` because the paper prints no value at those points.
- `extraction_date` 2026-10-29. `digitization_uncertainty_wt_pct` left empty as instructed.

## Extracted from

- Table 3 (p. 1035) and text Sec. 3.2: six H2 uptakes at 1 bar and 77 K (1.60, 1.34, 2.65, 2.11, 1.76, 1.51 wt%). Six rows (table_direct). Each is merged with the open marker at p/p0 about 1.00 of the matching Fig. 6 panel (same sample, 77 K, printed 1 bar within 0.02 bar), so no separate digitized row exists for those six markers; the digitized point is in the notes. The adsorption markers end at p/p0 about 0.94 and do not qualify.
- Table 1 (p. 1031), Table 2 (p. 1033), Sec. 2.2: characterization (SBET, Vultra, Vmicro, Vmeso, VT, NLDFT, BET range 0.01-0.30, N2 at 77 K, degassing 473 K, P <= 1e-5 mbar). Carried on every row of the sample. Vsuper and % micro are in notes.
- Fig. 6a-f (p. 1036), H2 at 77 K up to 1 bar, adsorption (filled) and desorption (open) markers. Rows: a 16 adsorption + 14 desorption; b 13 + 14; c 11 + 17; d 14 + 15; e 11 + 13; f 11 + 13 (the extra desorption marker of each panel is the Table 3 merged row).
- Fig. 8a (p. 1038), CG_PC_KOH at 77 K up to 70 bar, HPVA II: 8 adsorption rows, 1 merged adsorption row (see next line), 8 desorption rows.
- Text Sec. 3.2 (p. 1037), abstract, conclusions, Tables S7-S9: "experimental maximum amount of hydrogen adsorbed is 3.66 wt% at 77 K and 70 bar". One row (text_direct), merged with the adsorption marker at 70.478 bar (3.656 wt%; the marker is partly covered by the open desorption marker, pixel_count 13 against a median of 26). The desorption marker at 70.078 bar (3.659 wt%) is a separate desorption row. I merged with the adsorption marker rather than the desorption marker (closer in pressure to 70) because the text says "adsorbed" and both markers lie within the digitization uncertainty of the printed pressure.
- Table 4 (p. 1037) and text: Toth wt%max 3.73 ± 0.05 wt% at 77 K (K 1.42 ± 0.25, t 0.89 ± 0.09 in notes). One row, `fitted_extrapolated`, pressure unstated (asymptote), isotherm I7.
- Text Sec. 3.2 (p. 1038) and Fig. 9a: "around 0.5 wt% at 70 bar" at 298 K. One row (text_direct, approximate), merged with the 70 bar marker of Fig. 9a (digitized 69.999 bar, 0.4912 wt%; the digitized marker is the open desorption marker, which covers the adsorption marker). Tables S8 and S9 print 0.50 for the same point.
- Fig. 9b (p. 1038): the 1st-cycle (filled circle) marker at 70 bar, 70.135 bar and 0.3672 wt%. One row.
- Fig. S7 (SI p. 7): 77 K adsorption, 12 separable markers (12 rows); 273 K and 300 K, only the highest-pressure marker of each (1 row each; both are cut off by the figure edge at p/p0 about 0.815, confidence 2). The other 7 separable markers of the 273 K and 300 K series are in the archive JSON files but not in rows, per the scope rule for temperatures other than 77 K.

## Seen but not extracted

- Fig. 6 markers not separable or not extracted: every panel has hidden, partly covered or merged markers (filled adsorption markers under open desorption markers, and stacks at p/p0 below 0.04). Counts of markers I could count on the plot (visible plus inferred hidden, approximate): a 42, b 37, c 39, d 36, e 35, f 34. Digitized: a 31, b 28, c 29, d 30, e 25, f 25. Unextracted per panel: a about 11, b about 9, c about 10, d about 6, e about 10, f about 9. Specific cases: adsorption markers hidden under desorption markers in the p/p0 gaps of the adsorption series (b 0.24-0.53, c 0.24-0.66, d 0.24-0.47, e 0.24-0.66, f 0.24-0.66); covered crescents near p/p0 0.1 in panels b and c; in panel c an open circle at the frame edge merged with a filled blob; in panel a a partly covered adsorption marker near p/p0 0.104 (pixel_count 21, about 0.62 of the median) was dropped because its centroid was biased. `isotherm_point_count` for I1-I6 is therefore approximate.
- Fig. 6a, last desorption marker (p/p0 1.0045): the marker is clipped by the right frame edge (pixel_count 18 against a series median of 71). Digitized 1.634 wt% against the printed 1.60 (2.1 % high, the largest difference of the six panels; the others agree within 0.3 %). The Table 3 value is used; the digitized point is only in the notes. A hull re-measurement of the visible part gave 1.604-1.614 wt%, which supports a biased tool centroid; the archive was left as the tool wrote it.
- Fig. 5 (p. 1035): H2 adsorption branches of all six samples at 77 K, replotted from Fig. 6 with labelling inconsistencies; its black CG_N2+CO2 series duplicates the CG_CO2 data (a plotting error). Not digitized; Fig. 6 is the source of the same measurements.
- Fig. 8b: the same 9 adsorption markers as Fig. 8a plus the red Toth fit curve. Not digitized (duplicate markers; the line is a model fit, not a measured line).
- Fig. 8c: six 77 K adsorption cycles (markers: down triangle, circle, right triangle, left triangle, square, up triangle) at 9 pressure columns up to 70 bar. The six marker shapes overlap into 2-3 components per pressure, about 6 px wide, so no marker can be separated. No values extracted. Cycle 1 appears to coincide with the Fig. 8a adsorption markers.
- Fig. 9b: markers of cycles 2-6 at 70 bar merge into two components; not separable. Other pressures of cycle 1 and the other cycles not extracted (non-77 K isotherm: only the highest-pressure point of an isotherm is in scope; cycles 2-6 are inseparable).
- Fig. 9a: the adsorption marker at 70 bar is hidden by the open marker (see above); the other RT points are not extracted (non-77 K scope).
- Fig. S7: 77 K merged blobs not extracted (a stack of about 6 low-pressure markers near p/p0 0.01-0.04, and two 2-marker blobs near p/p0 0.094 and 0.146); 273 K a 2-marker stack at the lowest pressure; 300 K a 3-marker stack. Toth fit lines are model fits and not digitized. The 273/300 K highest markers are half clipped by the figure bitmap edge at p/p0 about 0.815 although the text says isotherms reach 1 bar. Fig. S7 77 K may be the same run as Fig. 6c (matching pressures at 0.21, 0.24 and 0.66 and uptakes within about 0.5 %); the paper does not say, so it is coded as a separate isotherm with a note.
- Fig. S6 (SI p. 7): correlation of the 77 K uptake with BET area, micropore volume and ultramicropore volume. The plot area is empty in the supplied page image, so nothing could be read. Not an isotherm in any case.
- Fig. 7 (p. 1037): isosteric heat of adsorption for CG_PC_KOH, average 9.01 kJ/mol. Not an uptake value.
- Table S7 "0.5 at 1 bar and 298 K" for CG_PC_KOH: contradicts the main text and Tables S8-S9 (70 bar). Not used.
- Tables S8 and S9, "this work" rows: repeats of Table 3 and the 3.66 and 0.50 values (no separate rows). H2/SBET ratios in Table S8 (1.58, 2.18, 0.30, 1.39, 1.58, 1.77, 1.36, 1.10 per 1000) are computed by the authors, not extracted.
- Tables S7, S8, S9, other rows: literature values for other spent-coffee carbons, other biomass carbons, metal hydrides, MOFs and benchmark carbons (AC-23, AC-HIC, Maxsorb-3, Filtercarb GCC 8 x 30, Filtercarb PHA) from cited papers. Not measured here, so not extracted.
- Table S7: average pore size 1.47 nm for CG_PC_KOH (method not stated) is on the S3 rows. Its micropore volume 0.616 equals Table 2.
- Text of Sec. 3.2: "Chahine rule" (1 wt% per 500 m2/g) is a rule of thumb, not a measurement.
- The text Sec. 3.2 refers to "Fig. 7" for the high-pressure 77 K isotherm, cycles and Toth fit where the figure is Fig. 8. Fig. 8 was used.
- Table 1 yields (7.82, 7.25, 19.80, 22.77, 3.53, 1.08 %): in the material descriptions only.
- CG and CG_PC characterization: TGA of CG (Fig. 1; residue 27.4 % in N2, ash about 3 %, Fig. S1), EDX of CG (carbon 68 ± 9 %), SEM (Figs. 4, S2-S5). No H2 uptake, so no row.
- EDX Tables S1-S6 (images): C more than 80 wt% with O, K, Mg, P, Ca (and Al, Si in CG_DA). These are native ash and activation residues, not intentional metals or a synthesis catalyst, so `metal_element`, `dopant_element` and `residual_metal_*` are empty.
- Figs. 2, 3 (N2 isotherms, PSD, histograms): N2, not H2; the PSD values are only through Table 2.
- Sample mass, H2 purity and free-volume calibration gas: not stated. He pycnometry on the HPVA gives the skeletal density 2.18 g/cm3 of CG_PC_KOH; the paper does not say it serves as the free-volume calibration, so `calibration_described` = false.
- H2 pretreatment duration: 12 h is stated only for the N2 measurements; the H2 pretreatment gives only 473 K and P <= 1e-5 mbar (ASAP rows) or "high vacuum" (HPVA rows), so `degas_duration_h` is empty. Thermal treatment between cycles (473 K, 12 h, Figs. 8c and 9b captions) is not a pre-measurement degassing.
- `replicates_reported`: true for I7, I8, I9 (the paper plots six further cycles at 77 K and six at RT, and a second RT run) and for the Toth row (± printed); false for I1-I6 and I10-I12.
- `instrument_identified`: true for ASAP 2460 and HPVA II rows; false for the Fig. S7 rows (the SI does not name the instrument).

## Paths

No path outside the permitted list was opened.
