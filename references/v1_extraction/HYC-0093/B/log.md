# HYC-0093 extraction log (extractor B)

Gao et al. 2023, J. Phys. Chem. C 127, 24027-24038 (10.1021/acs.jpcc.3c06200). Inputs: page images main-01..12, si1-01..14. 187 rows.

## Sources extracted

- main-04/05, Table 1 (elemental analysis): N wt% per sample into `dopant_concentration_wt_pct` (elemental_analysis); C/O/H wt%, N/C, O/C in notes. Characterization only.
- main-05, Table 2 (S_BET, S_micro, V_total, V_micro): on every row of each sample (BET/N2; t-plot; V_total at P/P0 ~ 0.99). Characterization only.
- main-07, Fig. 5a (printed bar labels): packing density 0.439/0.512/0.540/0.589 and He skeletal density 1.905/1.943/1.877/1.355 g/cm3 on every row.
- main-08, Fig. 6f and main-09 text (N 1s species %), SI Fig. S9-S10 and Fig. 6a (O groups): `functional_groups`.
- main-03, Sec. 2.3 (methods): Autosorb-iQ 0-100 kPa at 77 K (liquid N2) and 87 K (liquid Ar); Sieverts BSD-PH2001 0-130 bar at 77 K and 298 K; outgassed under vacuum at 300 C for 5 h; H2 99.999%. Sec. 2.2: N2 BET, outgassed 300 C 8 h (N2 analysis only).
- main-06, Table 3: all 28 uptake values (87 K 1 bar; 77 K 1 bar, 50 bar wt% and g/L; 298 K 1 bar, 130 bar wt% and g/L) -> rows M1/M2/M20/M42 (77 K 1 bar), M43-M46 (87 K), M47-M50 (298 K 1 bar), M139/M151/M168/M183 (77 K 50 bar total, wt% + g/L), M184-M187 (298 K 130 bar, wt% + g/L). Each merged with its plotted point (digitized point in notes).
- main-06, Fig. 4a (77 K, 0-100 kPa): NHPC-2 and NHPC-3 adsorption (solid) markers digitized (I3, I4); NHPC-0/NHPC-1 markers hidden (see below).
- main-06, Fig. 4b (87 K), Fig. 4c (298 K, 0-100 kPa): highest-pressure point per curve only (merged with Table 3).
- main-06, Fig. 4d (excess, 77 K, 0-50 bar): all separable solid (adsorption) and hollow (desorption) markers digitized (I13-I16); Fig. 5b (excess volumetric, 77 K) digitized and put on the matching Fig. 4d rows.
- main-06, Fig. 4e (total, 77 K, 0-50 bar): all separable solid (adsorption) markers digitized (I17-I20); Fig. 5c (total volumetric, 77 K) digitized and put on the matching Fig. 4e rows.
- main-06 Fig. 4f and main-07 Fig. 5d (298 K, 0-130 bar): highest-pressure point only (merged with Table 3; drop lines mark these points).
- Text passages restating Table 3 values (abstract; p. 24031 "~3.0 wt %", "about 2.0 wt %", "2.1 wt %", "approximately 0.10 wt %", 6.10/5.40/4.99/3.16 wt%, 1.26/1.07/1.19/0.88 wt%; p. 24034 26.96/26.47 g/L, 6.65 g/L, 3.00 wt%, 4.99 wt%) and SI Table S1 NHPC-2 row (3.00, 4.99, 26.96): same measurements as Table 3 / plotted points; recorded in the notes of those rows, no separate rows.

## Coding decisions

- Samples: NHPC-0 (S1), NHPC-1 (S2), NHPC-2 (S3), NHPC-3 (S4); labels from Table 3. All coded `doped_carbon` with dopant N (NHPC-0 contains 0.36 wt% N from PVP, graphitic N only; paper names all NHPC-x N-doped). `synthesis_method` = carbonization (PVP carbonized at 500 C); KOH/melamine activation in `activation_method` (C:melamine:KOH ratios 1:0:4, 1:0.5:4, 1:1:4, 1:2:4 assigned in printed order). The carbon precursor "C" has no characterization or H2 data: no row.
- Basis: low-pressure Autosorb isotherms (Fig. 4a-c, Table 3 1 bar columns) name no basis -> `basis_stated` false, `uptake_type` unspecified, `basis_inferred` excess (volumetric default). The Sec. 2.3 sentence "The measurements provide excess H2 uptake at 77 K" follows the high-pressure description and was applied to the high-pressure runs only (conservative).
- 77 K high-pressure excess (Fig. 4d/5b) and total (Fig. 4e/5c, Table 3 50 bar): both named and defined (SI Fig. S1) and reported side by side -> `basis_stated` true; separate isotherm_ids for excess and total of the same run (the four basis fields must be constant per isotherm). Total points are derived from excess via the Langmuir-Freundlich fit -> `value_kind` fitted_interpolated.
- 298 K high-pressure (Fig. 4f/5d, Table 3 130 bar): Fig. 5 caption calls these "excess" -> excess, `basis_stated` true (definition in SI Fig. S1). Eq. 2 calls N_m "total H2 uptake capacity"; noted.
- Volumetric g/L stored in `volumetric_capacity_kg_m3`, basis packing_volume (packing density from eq. 3, no inter-particle void); `volumetric_capacity_includes_compressed_gas` true for total-based values (H2 compressed within pores included), false for excess-based values.
- Hollow markers coded desorption (paper's convention; text calls the isotherms reversible). The highest-pressure Fig. 4d point is drawn as a hollow marker over the adsorption end point; coded adsorption (turning point), one row.
- `instrument_identified`: true for Quantachrome Autosorb-iQ rows; false for the high-pressure rows ("automatic Sieverts-type apparatus (BSD-PH2001)", manufacturer not named separately; conservative). No free-volume calibration or buoyancy statement -> `calibration_described` false. No uncertainties or repeats -> `replicates_reported` false. Sample mass and degas end pressure not stated.
- `measuring_lab_id` = "Xia group, China University of Geosciences": first-marked corresponding author K. Xia, main-text affiliation. SI lists Xia at South China University of Technology, and Author Contributions say X.G. (SCUT) ran the H2 tests with L.H./Y.M. operating the Sieverts apparatus; the paper does not say the measurement was made in another laboratory, so the default rule was applied.
- wt% convention: not defined, no paired mmol/g, mg/g or cm3/g values -> unknown/none.
- `bet_range_stated` false: Fig. S3 shows BET plots but no P/P0 range is stated; no consistency criteria stated.
- `isotherm_point_count`: lower bound (markers the digitizer resolved: non-legend detections, +1 per merged blob, or rows extracted for I13-I20; max of Fig. 4f/5d for I21-I24). Desorption markers of Fig. 4a-c, 4e and overlapping markers could not be counted.

## Figure 4d legend misprint

Fig. 4d legend labels the red down-triangle series NHPC-2 and the pink up-triangle series NHPC-3, the reverse of every other panel (4a-c, 4e-f, 5b-d). Assigned red = NHPC-3, pink = NHPC-2: Fig. 5b (legend as elsewhere) equals Fig. 4d x 10 x packing density only with this assignment (matched-point ratios 0.991-1.019), and with the printed legend the Fig. 4e totals (labelled 4.99 and 3.16 wt%) would fall below the excess. Rows from Fig. 4d for NHPC-2/NHPC-3 carry confidence 2 and a note.

## Inconsistencies noted (printed values kept)

- Table 3 NHPC-2 77 K 1 bar 3.02 wt%; text p. 24034 and SI Table S1 give 3.00 wt%.
- Table 3 and the Fig. 4e label give NHPC-1 total 5.40 wt% at 50 bar; the plotted end point digitizes at 5.54 wt% (check vs 5.40 passes at 5%), and 28.35 g/L / 0.512 = 5.54 wt%.
- Table 3 NHPC-1 5.66 g/L and NHPC-2 6.65 g/L (298 K, 130 bar): Fig. 5d drop lines/end points digitize at 5.46 and 6.43 g/L, equal to 1.07 x 5.12 and 1.19 x 5.40.
- Text p. 24034: NHPC-2 "achieves 4.99 wt % under the same condition" as AC-0 at 77 K and 20 bar; 4.99 wt% is the 50 bar total (Table 3, Fig. 4e label; SI Table S1 "max." at 77 K, 20-50 bar). Treated as the 50 bar value (note on M168); no 20 bar row, the Fig. 4e NHPC-2 point near 20 bar is a digitized row (4.68 wt%).
- SI Table S1 gives NHPC-2 uptake per SSA 2.00 x 10^-3 wt%/(m2/g); Table 3 gives 2.03.
- SI Table S2 labels samples NHPC-1..NHPC-4.

## Digitization

- All archives in `digitizations/` (55 files). Axes calibrated on lowest/highest labelled ticks found from pixel columns/rows, third tick verified (residuals <= 0.3% in every archive). Fig. 4f/5d pressure axes are log (ticks 1, 10, 100 bar). Fig. 4a-c pressures read in kPa and converted to bar (x 0.01).
- Solid markers: `--mode markers` on the page image (`--open-px` 4; 5 for Fig. 4a NHPC-2/3 to split touching markers; 2 for Fig. 4a NHPC-0/1 counting runs). Hollow markers (Fig. 4d only): marker mode on an image of the hollow-marker interiors built from the page image by `work/scripts/interiors2.py` (work/f4d_NHPC-x_open.png, same pixel geometry; archived path and sha256).
- Screening of detections (`work/scripts/screening.py`): legend markers and value labels dropped; fragments (< 0.6 x full-marker pixel count, i.e. partly hidden markers with biased centroids) and merged blobs (> 1.5 x) dropped. Manual drops: Fig. 4a NHPC-2 detections 0-2 (inside the merged low-pressure band below 15 kPa); Fig. 4d NHPC-2 hollow detection 5 (interior of a red NHPC-3 marker). Per-archive drop list:
  - fig4a NHPC-0/NHPC-1: every detection is a sliver of a hidden marker; used for marker counting only (and the NHPC-1 1 bar end marker, 2.95 wt%, in the M2 notes).
  - fig4a NHPC-2: dropped 0-2 (low-pressure band), 3 legend, 4 merged (5-12 kPa); 22 is the 1 bar end marker (partly covered) used only in the M20 notes.
  - fig4a NHPC-3: dropped 0 (merged cluster of the points below 2 kPa), 2 legend.
  - fig4d NHPC-0 solid: dropped 0, 5, 7, 10 fragments, 11 legend. NHPC-1 solid: 0, 1, 2, 5 fragments, 9 legend. NHPC-2 solid: 0, 8 fragments, 10 legend. NHPC-3 solid: 5 fragment, 6 legend. NHPC-2 hollow: 0, 3 fragments (NHPC-3 interiors), 5 manual.
  - fig4e NHPC-0: 0, 2, 10 fragments, 1 legend, 3, 5 merged. NHPC-1: 0, 1, 13, 16 fragments, 2 legend, 3, 5 merged. NHPC-2: 3 legend, 4, 14, 16 merged (40 and 45 bar points lost). NHPC-3: 2 legend, 3, 4 merged, 10, 12 fragments.
  - fig5b NHPC-0: 0-3, 6, 7, 10 fragments, 5, 9, 11, 13 merged (adsorption/desorption pairs), 14 legend. NHPC-1: 0 fragment, 1, 7 merged, 10 legend. NHPC-2: 0 fragment, 5, 8, 9, 11 merged, 14 legend. NHPC-3: 0, 1 fragments, 3-6, 8, 10, 12 merged, 13 legend.
  - fig5c NHPC-0: 0-2, 5, 9, 10, 12 fragments (points above 16 bar hidden under NHPC-2), 3 legend. NHPC-1: 0 legend, 1 fragment. NHPC-2: 4 legend, 5 merged. NHPC-3: 0 fragment, 4 legend, 5, 6 merged.
- Volumetric-gravimetric pairing: a Fig. 5b/5c point goes on the Fig. 4d/4e row with |dp| <= max(4%, 0.4 bar) and vol/(wt% x 10 x packing density) within 5% (all accepted pairs 0.991-1.019). Unpaired volumetric points with an isolated-marker size became volumetric-only rows (M51, M88, M126, M127, M129, M141, M155, M166, M167, M171); two unpaired, possibly merged Fig. 5b blobs were dropped (NHPC-2 0.60 bar 12.20 g/L; NHPC-3 0.43 bar 7.46 g/L).
- Checks against stated values (`digitize_figure.py check`): passed for fig4a NHPC-1/2/3 at 100 kPa, fig4b NHPC-1/2/3 series at 100 kPa, fig4c NHPC-1/3 series at 100 kPa, fig4e NHPC-1/3 at 50 bar, fig5c NHPC-1/2/3 at 50 bar. fig4c NHPC-2 series FAILED at 5% (0.0853 vs printed 0.09; within the printed rounding 0.085-0.095) and is marked discarded; it supplied only the marker count of I11, and the M49 row value is the Table 3 value. Single-marker "highest" archives cannot be checked (stated x outside their one-point range); fig4e NHPC-0/2 and fig5c NHPC-0 end before 50 bar; Fig. 4d and 5b have no stated values. These stay unchecked; their comparisons with printed values are in the row notes.
- Merge tolerance: Table 3 values merged with end points within 2% of the printed pressure, except NHPC-3 at 298 K (Fig. 4f end point 127.0 bar) and NHPC-2 (Fig. 5d end point 127.3 bar), merged because the drop lines mark these points and the text cites Fig. 4f/5d for these capacities.

## Values or points seen but not extracted

- Fig. 4a: NHPC-0 and NHPC-1 markers hidden under NHPC-2 (only slivers visible, about 14 and 20 markers); NHPC-2 markers below 15 kPa merged into one band; NHPC-3 points below ~2 kPa merged at the origin; all desorption (hollow) markers overlap the adsorption markers and could not be separated.
- Fig. 4b, 4c: all points except the highest-pressure one (rule for non-77 K isotherms). Fig. 4c NHPC-0 end marker entirely hidden under NHPC-1 (M47 has no digitized point).
- Fig. 4d: adsorption markers below ~8 bar hidden under the hollow desorption markers; desorption markers below ~3 bar stacked along the y axis; partly hidden markers listed above.
- Fig. 4e: desorption (hollow) markers overlap the adsorption markers (interiors fragmentary) and were not digitized; low-pressure pile-up below ~6 bar partly unresolved.
- Fig. 4f, 5d: all points except the highest-pressure one (298 K), including the desorption branches.
- Fig. 5b, 5c: points dropped as listed above; Fig. 5c NHPC-0 points above 16 bar hidden under NHPC-2.
- Fig. 7b, 7c (uptake per SSA vs pressure, 77 K) and Fig. 7d, Fig. S5, Table 3 last two columns, abstract graphic (uptake per SSA: 1.96/2.05/2.03/1.94 x 10^-3 wt%/(m2/g); 8.49/10.47/10.97/11.41 x 10^-3 (g/L)/(m2/g)): uptake divided by S_BET, not a schema quantity.
- Fig. 7a and text: isosteric heats (7.45 kJ/mol NHPC-0, ~7.95 kJ/mol NHPC-2/3 at low coverage): not uptake.
- Fig. 5e radar chart: NHPC-2 vs CP-2-800, NOTT-112, NU-100 (literature); NHPC-2 values duplicate Table 3.
- SI Fig. S11: ln(P) vs uptake (mg/g) replots of the 77, 87 and 298 K isotherms used for virial fitting (the 298 K data reach ln P ~ 11.5, i.e. the high-pressure run); same measurements as Fig. 4, not digitized to avoid duplicates. SI Table S2: virial correlation coefficients.
- SI Table S1, other materials (literature values, not measured here): carbons PC-2, CH700/700/3, AC-0, AA-0, CP-4-800, CP-2-800; MOFs NOTT-112, NU-100, MOF-210 (MOFs are not carbon sorbents).
- Text p. 24034: PC-2 2.00 wt% (ref. 51), AC-0 4.90 wt% at 77 K and 20 bar (ref. 50), MOF volumetric uptake below 25 g/L (refs. 46-49): literature.
- Introduction p. 24028: N-HEG 0.88 wt% and NEG 0.53 wt% at 298 K, 2 MPa (ref. 16), Chahine's rule: literature.
- Characterization without schema fields: Raman I_D/I_G 0.953/0.973/1.025/1.116 (Fig. 2d), XRD peaks 23.5 and 43.4 deg (no d-spacing printed), NLDFT PSD peaks 0.54/0.94/1.22 nm and mesopores 2-4 nm for all samples (no per-sample pore diameter), external area only as bars in Fig. 3b, O-group percentages (Fig. S10), BET slope/intercept/C constants (Fig. S3), TGA (Fig. S4), N2 isotherms (Fig. 3a).

During the run, a mistyped relative output path made the digitizer try to create /home/claude/work/v1_tools_frozen/trial; the write was refused and nothing was created there.
