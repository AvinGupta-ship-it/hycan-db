# HYC-0032 extraction log (agent B, 2026-11-09)

Paper: Anuchitsakol et al., RSC Advances 2023, 13, 36009-36022 (main, 14 pages) plus ESI (si1, 5 pages). Read from page images only. 189 rows written.

## Sources extracted from

- main p.5, Table 1 (this work): H2 uptake at -196 C and 25 C, "at 1 bar" (caption), for N-AC900-2, N-AC900-1, N-AC800-1, AC900, AC800, with S_BET, V_t and CHN-O composition. 10 rows (table_direct). Each value is merged with the ~1 bar point of the matching Fig. 9a / Fig. 9b series (same sample and temperature, plotted point within 0.02 bar of 1 bar).
- main p.5, Table 1 (literature comparison rows, "Year/ref." column): 20 cited values for 20 other carbons at -196 C, 1 bar. Extracted under the "values reported before" rule with `previously reported: <Year (ref. N)>` in notes. Blank Year/ref. cells are attributed to the reference printed in the row above (noted on each such row). Measuring laboratory, method, basis and instrument are not given, so these are coded `unknown`/`false`. `measuring_lab_id` is "unidentified laboratory of ref. N (HYC-0032)". Material class is taken from the cited reference titles where the label alone is not enough. Composition is given in notes only; dopant concentration fields are left empty because the paper does not state the basis for the cited values.
- main p.1, Introduction: "ammonia treatment of a commercial AC improved hydrogen adsorption efficiency from 1.98 to 2.34 wt% at -196 C and 0.93 bar (ref. 39)". These are the same values as Table 1 rows "Commercial AC" and "AC-He400-N500". There is one row per value, using the explicit 0.93 bar. The conflict with the Table 1 caption ("1 bar") is noted on both rows.
- main p.7, Fig. 9a (-196 C, 0-1 bar, 5 series): every separable marker digitized (`digitizations/fig9a_*.json`), 159 digitized rows, plus the merged ~1 bar points.
- main p.7, Fig. 9b (25 C, 5 series): only the highest-pressure point of each series is used (`digitizations/fig9b_*.json`). It is merged with the Table 1 25 C value.
- main p.1 Abstract, p.7 Section 3.2 ("1.78-2.62 wt%") and p.11 Conclusions ("up to 2.62 wt% at -196 C and 1 bar"): same measurements as Table 1. No separate rows; noted on the N-AC900-2 and AC800 rows.
- main p.3, Section 2.1.2/2.1.3: characterization and H2 method details (multipoint BET, N2 at -196 C; V_t at P/P0 = 0.95; NLDFT slit-pore PSD; CHN analyzer LECO 628 with O by difference; Micromeritics ASAP2020 plus; degassing 300 C, 12 h, "ultrahigh vacuum"). The 6 h at 300 C degassing is for the N2 BET measurement, not H2.

## Digitization details

- Calibration, Fig. 9a: x 0 bar at px 716.56, 1.0 bar at px 1025.87, check at 0.4 bar px 840.39 (error 0.09%). y 0 wt% at px 352.49, 3.0 wt% at px 136.64, check at 1.5 wt% px 244.56 (error 0.005%). Calibration, Fig. 9b: x 0 / 1.0 bar at px 716.61 / 1025.73, check at 0.4 bar px 840.42. y 0 / 0.14 wt% at px 668.32 / 452.51, check at 0.08 wt% px 545.03. All tick positions were measured from pixel rows and columns.
- The tool was run on `work/main-07_masked.png`, a copy of main-07.png with three non-data regions set to white: the Fig. 9a legend box (x 838-1023, y 295-350), the Fig. 9a in-plot label "-196 C (a)" and the Fig. 9b label "25 C (b)". No plotted data lie in these regions. The archives record this image and its sha256.
- Marker mode settings: 2-px opening. Tolerance 70 (red) or 130 (black, magenta, blue, green; blue in 9b 160). Size limits reject fragments and overlapping pairs. Rejected groups are listed in each archive.
- Step-6 `check` passed for 9 of 10 archives against the Table 1 values at the last digitized pressure (differences 0.02-4.1%). `fig9a_N-AC900-2.json` stays "unchecked" because the paper states no value inside its digitized range (0.03-0.80 bar). Its ~1 bar point is hidden. It shares the calibration of the four Fig. 9a series that passed.

### Markers not separated or not digitized (Fig. 9a, -196 C)

- All series, p < ~0.02 bar: the first markers of all five series form one vertical stack at the y axis. AC800 stars are drawn on top. Only AC800 stars at 0.09, 0.17 and 0.28 wt%, the N-AC900-1 square at 0.0014 bar / 0.028 wt%, and a partly hidden AC900 cross at ~0.003 bar / 0.5 wt% are visible. The point counts are therefore lower bounds.
- N-AC900-1 (red squares): there are 4 overlapping pairs at ~0.09/0.10, 0.35/0.365, 0.385/0.40 and 0.425/0.44 bar (blobs of 37-45 px, rejected). Partly hidden squares at ~0.013 bar and ~0.27 bar were rejected. The count is 49 (39 digitized).
- N-AC900-2 (black circles): fragments at ~0.085, 0.17, 0.29, 0.83 and 0.865 bar were rejected as too small. Markers at ~0.20 bar (under an AC900 cross) and ~0.26, 0.89, 0.91, 0.955 and ~1.0 bar (under N-AC900-1 squares) show only slivers and were not isolated. The count is 34 (23 digitized). Six digitized circles are partly covered (confidence 2).
- N-AC800-1 (magenta triangles): the triangle at ~0.26 bar is split by the dashed region line and was rejected. The triangle at 0.097 bar is accepted (28 px including line pixels, confidence 2). The count is 33.
- AC900 (blue crosses): the cross at ~0.003 bar was rejected as too small. The count is 34.
- AC800 (green stars): a blob of at least 2 stacked stars at ~0.008 bar, 0.37-0.45 wt%, was rejected. The count is 38.

### Fig. 9b (25 C)

All five series overlap below ~0.13 bar. AC900 crosses are hidden under AC800 stars below ~0.5 bar. The point counts (N-AC900-2 35, N-AC900-1 32, N-AC800-1 33, AC900 15, AC800 32) are uncertain below 0.13 bar and are a lower bound for AC900. The other 25 C points are not extracted (protocol scope: highest-pressure point only at non-77 K temperatures).

## Values seen but not extracted

- Fig. 11 (main p.8): experimental H2 surface excess (umol/m2) on a graphite surface at -196.15 C (blue triangles, about 18) and -195.80 C (red circles, about 27). These are literature data (refs. 67, 68), shown with GCMC curves. The log-scale y axis is labelled 10, 1, 0; the "0" is inconsistent with a log axis. Following the rule, I did not reinterpret it and extracted no values. The figure was used only to count markers, and the counts are approximate because the markers overlap.
- Fig. 9c (main p.7): isosteric heat against uptake (0-0.12 wt%). Not an isotherm. Text: "interrelated loadings up to 0.12 wt% for isosteric heat calculations". No uptake values beyond Table 1.
- Fig. 10a/b (main p.8): uptake at -196 C and 1 bar against S_BET and V_t, "corresponding to Table 1". Not an isotherm and not digitized; it shows no values beyond Table 1.
- Figs. 12, 13, 14 (main) and ESI Figs. S1, S2, S3: GCMC simulation results (simulated uptake, density profiles, heats). Not measurements; not extracted.
- Abstract: "increasing by 47% from unmodified AC" is a ratio derived from Table 1 values; not a row.
- Fig. 3a (N2 isotherms), Fig. 3b (NLDFT PSD, no numeric average width), Fig. 5 (FTIR), Fig. 6 (XPS N 1s) and Fig. 7 (bar chart of N-species percentages; no printed numbers, not digitized): characterization of samples that have H2 rows. The functional groups are recorded in `functional_groups`.
- ESI Table S1: force-field parameters (simulation); not uptake.
- Biochar and the urea-impregnated intermediate (Fig. 1): no H2 uptake and no characterization values; no rows.
- Introduction: MOFs and zeolites are mentioned without values. "0.68 nm ... at 25 C and 25 bar (ref. 43)" and other cited pore widths are not uptake values.

## Coding decisions

- -196 C is 77.15 K and 25 C is 298.15 K (stated numbers, not inferred).
- `measurement_method = volumetric_sieverts` is inferred from the named instrument (Micromeritics ASAP2020 plus). The paper does not name the method or the uptake basis, so `basis_stated = false`, `uptake_type = unspecified` and `basis_inferred = excess` (instrumental default).
- No uncertainties, error bars or repeated isotherms are given, so `replicates_reported = false`. The free-volume determination is not described, so `calibration_described = false`.
- The N-AC samples are `doped_carbon` with `dopant_element = "N, O"` (the paper calls them "O and N co-doped"). `dopant_concentration_wt_pct` holds the N content (elemental analysis), with O given in notes. AC800 and AC900 are `activated_carbon` (the paper calls them "original"/"unmodified" AC). Their N and O contents are given in notes.
- `synthesis_method = carbonization` for all five samples: the paper calls the biochar step "(carbonization)", N2 at 600 C for 1 h. CO2, KOH and urea treatments go in `activation_method` and the description.
- `pore_volume_method = other`: V_t is a single-point N2 volume at P/P0 = 0.95.
- Sample numbering follows first appearance. The commercial AC of ref. 39 and its ammonia-treated form appear first (Introduction, p.1) and are S1 and S2. This work's samples are S3-S7 in Table 1 order, and the remaining literature samples are S8-S25.
