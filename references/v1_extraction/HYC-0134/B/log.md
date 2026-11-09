# HYC-0134 extraction log (agent B)

Paper: Matei Ghimbeu et al. 2015, Microporous and Mesoporous Materials 223 (2016) 79-88, "One-pot synthesis of tailored Pd-Co nanoalloy particles confined in mesoporous carbon". Pages read: main-01 to main-10, si1-1 to si1-7 (images only).

## Sources extracted from

- Fig. 10a (main-09, journal p. 87), 25 C high-pressure PCI, C@Pd90Co10-6 (red circles): highest-pressure marker only (non-77 K isotherm) -> M1 (I1). Archive fig10a_Pd90Co10-6_highest_pressure.json.
- Fig. 10a, C@Pd75Co25-6 (blue squares): highest-pressure marker only -> M2 (I2). Archive fig10a_Pd75Co25-6_highest_pressure.json.
- Fig. 10b (main-09), 25 C low-pressure PCI, C@Pd90Co10-6 (red filled circles): highest-pressure marker only -> M3 (I3). Archive fig10b_Pd90Co10-6_highest_pressure.json.
- Fig. 10b, C@Pd75Co25-6 (blue filled squares): highest-pressure marker only -> M4 (I4). Archive fig10b_Pd75Co25-6_highest_pressure.json.
- Table 2 (main-06): BET area, Vt, Vmicro (DR), Vmeso of C@Pd90Co10-6 and C@Pd75Co25-6, carried on their rows.
- Table 1 (main-04): Pd, Co, PdCo wt% and C/H/O of the two H2 samples (metal_loading_wt_pct = PdCo wt%; detail in notes).
- Section 2.3 (main-02): N2 sorption method (Micromeritics ASAP 2420, degas 300 C overnight, BET range 0.05-0.3, DR micropore volume, Vt at P/P0 0.95, BJH desorption).
- Section 3.2 text (main-06): BJH mesopore diameter 3.5 nm for all C@PdxCoy-6 samples -> average_pore_diameter_nm.
- Section 2.4 (main-03): H2 methods (25 C PCI; Autosorb IQ Quantachrome to 0.1 MPa, ideal EOS; manual volumetric device to 9 MPa, 6N H2, GASPAK real EOS, He-pycnometer sample-volume correction, density ~1.6 (+-0.1) g/cm3; pre-treatment under H2 at ambient T, degas ~120 C; "measured twice" with no results shown).
- Section 3.4 (main-09/10) and Fig. 10 caption: 25 C for both panels; full symbols absorption, open symbols desorption.

## Digitization

- Fig. 10a calibration on main-09.png: x 0 MPa at px 747.5 (inward tick under the origin markers), 10 MPa at px 1150 (right frame, tick coincident); verify 5 MPa at px 948.5 (rel. error 0.12%). y 0.00 wt% at px 907, 0.35 wt% at px 626.5 (top frame tick); verify 0.20 at px 747 (rel. error 0.18%).
- Fig. 10b calibration: x 0 at px 744, 0.10 MPa at px 1148.5 (outward ticks); verify 0.06 at px 986.5 (0.08%). y 0.000 at px 1264.5, 0.020 at px 969.5; verify 0.010 at px 1117 (0.0%).
- Each archive holds one marker (the highest-pressure point), isolated with a tight ROI and --open-px 0; 1 marker extracted = 1 marker counted in each ROI.
- M1: the top marker of the red series in Fig. 10a is an open circle drawn as a 1-px anti-aliased ring; tolerance 40-180 split it into fragments, so tolerance 250 (ROI 1112-1122 x 685-696, ring only plus 2-3 px of the joining lines) was used; centroid (1116.3, 690.2) agrees with the ring's geometric centre (~1116.5, 690.5).
- M1/M2 branch: both top markers are open symbols (caption: open = desorption) at the turning point; the filled absorption line ends at them and open markers are drawn white-filled over filled markers (visible for C@Pd75Co25-6 at 4.2 MPa), so the point is coded as the last adsorption point (isotherm_branch = adsorption). Reconciler may prefer desorption.
- M3: the marker sits on the right axis frame (0.10 MPa); its 8-px core is fully visible (not clipped).
- The tool's `check` step (comparison with a value stated by the paper) was not run: the paper prints no H2 uptake value in text or tables, so the archives stay `unchecked`.
- Marker counts (isotherm_point_count): I1 = 14 (8 filled incl. origin, 6 open: ~0.12, 0.58, 1.6, 4.05, 7.0, 9.15 MPa); I2 = 13 (8 filled incl. origin partly hidden by the red origin circle, 5 open: ~0.6, 1.65, 4.2, 6.9, 9.15 MPa; a hidden open marker under the filled square at ~7.95 MPa cannot be excluded); I4 = 10 (tool found 9 because the 0.008 and 0.010 MPa squares touch). Tool runs for counting in the work directory (count_10a_*.json, count_10b_*.json).
- I3 (Fig. 10b, C@Pd90Co10-6): markers below ~0.005 MPa overlap into one red cluster that cannot be separated (9 separable markers at ~0.008-0.0992 MPa plus the cluster); isotherm_point_count left empty.

## Values seen but not extracted

- Fig. 10a: all other markers of the two 25 C high-pressure runs (13 for C@Pd90Co10-6, 12 for C@Pd75Co25-6), both branches: non-77 K isotherm, only the highest-pressure point is digitized.
- Fig. 10b: all other markers of the two 25 C low-pressure runs (C@Pd90Co10-6: 8 separable + unresolved cluster; C@Pd75Co25-6: 9): non-77 K isotherm.
- Fig. S6 and SI p. 7, Section 3.4: in-situ XRD under 1 bar H2 at room temperature of C@Pd50Co50-6, C@Pd75Co25-6, C@Pd90Co10-6: qualitative hydride formation (only C@Pd90Co10-6), no uptake value.
- Section 3.4/4 text: qualitative comparisons only ("absorbs more hydrogen", "completely reversible"); no number.
- Section 2.2: nominal total metal quantity "~5 wt.% with respect to carbon framework" (nominal, not measured; measured Table 1 value used).
- No non-carbon material (hydride standard, MOF, zeolite) was measured for H2.

## Samples with characterization but no H2 uptake (no rows)

- C@Pd50Co50-4: Table 2 SSA 668 m2/g, Vt 0.51, Vmicro 0.29, Vmeso 0.22 cm3/g, crystallite 5.5 nm, TEM 8.5 nm; Table 1 C 66.56, H 3.30, O 28.80, Pd 0.45, Co 0.87, PdCo 1.32 wt%, Pd/Co 49/51.
- C@Pd50Co50-6: SSA 848, Vt 0.60, Vmicro 0.35, Vmeso 0.25, 7.5 nm, 11.0 nm; Table 1 C 83.76, H 2.19, O 10.66, Pd 2.14, Co 1.25, PdCo 3.39 wt%, 49/51. (Also in-situ XRD under 1 bar H2, no uptake.)
- C@Pd50Co50-8: SSA 803, Vt 0.48, Vmicro 0.31, Vmeso 0.17, 7.5 nm, 10.5 nm; Table 1 C 88.45, H 0.61, O 7.22, Pd 2.39, Co 1.33, PdCo 3.72 wt%, 50/50.
- C@Pd75Co25-4: SSA 681, Vt 0.47, Vmicro 0.29, Vmeso 0.18, 7.6 nm, 12.7 nm.
- C@Pd75Co25-8: SSA 791, Vt 0.48, Vmicro 0.31, Vmeso 0.17, 8.0 nm, 12.0 nm.
- C@Pd90Co10-8: SSA 789, Vt 0.41, Vmicro 0.32, Vmeso 0.09, 16 nm, 23.0 nm.
- C@Pd90Co10-6 made from Pd nitrate + Co acetate (Fig. 2a, TEM mean 20.3 nm) and from Pd acetate + Co acetate (Fig. 2b, TEM mean 19.7 nm): TEM only.

## Figures that are not H2 isotherms (not digitized; no H2 values)

- Fig. 1 (scheme); Figs. 2, 4, 8, S2, S3 (TEM, particle-size histograms); Figs. 3, 6, S1, S6 (XRD); Fig. 7 (lattice parameter vs annealing T, EDX maps); Fig. S4 (material mass vs T); Figs. 5, 9, S5 (N2 isotherms and BJH distributions).

## Coding decisions

- Sample numbering: only samples with H2 rows are numbered, in order of first appearance (C@Pd90Co10-6 in Section 3.1/Fig. 2 = S1; C@Pd75Co25-6 = S2). Labels as in the Fig. 10 legends (subscripts written as plain digits).
- measuring_lab_id: corresponding author Matei Ghimbeu, affiliation a prints the university as "UHA"; the paper does not state which laboratory performed the H2 measurements.
- instrument_identified false for the 9 MPa manual volumetric device (described, but neither named nor stated to be home-built); true for the Autosorb IQ (Quantachrome).
- calibration_described true for the 9 MPa device (sample-volume correction from He-pycnometer density); false for the Autosorb IQ (nothing stated).
- h2_purity_pct 99.9999 (6N) only on the high-pressure rows, where it is stated.
- area_same_sample yes; skeletal_density 1.6 g/cm3 ("around 1.6 (+-0.1)", stated for the materials collectively) on all rows.
- Temperature 298.15 K for Fig. 10b although Section 2.4 says "room temperature" for that device: Fig. 10 caption and Section 3.4 give 25 C for both panels.
