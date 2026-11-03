# HYC-0110 extraction log (agent B)

McNicholas et al. 2010, J. Phys. Chem. C 114, 13902-13908, "H2 Storage in Microporous Carbons from PEEK Precursors". Input: 7 main-article pages (main-1 to main-7) and 4 SI pages (si1-1 to si1-4), read from page images only. 23 rows written.

## Sources extracted from

- main p.13907 (main-6.png), Table 1: every uptake value, for both the PEEK samples (2 bar, 77 K per footnote b) and the four literature comparison carbons; BET SA and cumulative pore volume columns used as characterization. Rows M1-M11, plus M15 (the "~5 at 77 K, 20 bar" / "35 at 77 K, 20 bar" entry for PEEK-CO2-9-80, merged with the Caltech isotherm).
- main p.13906 (main-5.png), right column, text: "PEEK-CO2-9-80, which achieves 3.7 wt % at 77 K and 2 bar" (same value as M10); "ranging to ~5 wt % at 77 K and 20 bar (Figure 7)" and "~35 g/L using the unaltered porous carbon density of ~0.7 g/mL" (M15); "upon compression of 15 t ... ~1 g/mL; this density corresponds to a H2 volumetric uptake of ~50 g/L" (M23, continued on main p.13907 left column).
- main p.13906, Figure 6 caption: 3.7 wt% at 3103 m2/g for PEEK-CO2-9-80 (same value as M10).
- main p.13902 (main-1.png), abstract, and main p.13907, conclusions: "approximately 5 wt % and 35 g/L, respectively, at 77 K and 20 bar" / "up to ~5 wt % and 35 g/L" (same values as M15, no extra row).
- main p.13907, Figure 7B: series "Gibbs Excess(Caltech, 77K)" (red squares), the 77 K isotherm: rows M12-M14 and M16-M19 (digitized) and M15 (merged with the table/text value). Archive fig7B_caltech_gibbs_excess_77K.json.
- main p.13907, Figure 7A: series "Eng. Excess (NREL, 75.6K)", "Gibbs Excess(NREL, 75.6K)" and "Gibbs Excess (sk=2.1g/cc) (NREL, 75.6K)": highest-pressure marker only, rows M20-M22. Archives fig7A_nrel_eng_excess_75.6K_last.json, fig7A_nrel_gibbs_excess_75.6K_last.json, fig7A_nrel_gibbs_excess_sk2.1_75.6K_last.json.
- main p.13903 (main-2.png), experimental section, and SI p.1-2 (si1-1, si1-2), experimental details: synthesis, burn-off definition, sample naming, instruments (Micromeritics Gemini 2360 5-pt BET; NREL: Hy-Energy PCTPro-2000 above 2 bar, home-built Sieverts device at 2 bar, Quantachrome Autosorb-1 for BET and pore volume; Caltech: Micromeritics ASAP), degassing at 300 C. Used for method coding on every row.
- main p.13904-13905 text and Figure 3 caption: DFT pore-size information for PEEK-CO2-9-80 (modal width 1.35 nm, used as average_pore_diameter_nm with pore_diameter_method DFT and a note that it is a modal value).
- SI p.3 (si1-3), Figure S1A: XPS of PEEK-CO2-9-80, C 1s = 96%, O 1s = 4% (recorded in notes).

## Figure digitization

Calibration (pixel positions found from tick-mark and axis-line pixel profiles, sub-pixel centroids):
- Figure 7B: x 0 bar at 164.5 px, 50 bar at 553.0 px, check 30 bar at 396.95 px (predicted 29.92, error 0.28%); y 0 wt% at 1340.5 px, 6 wt% at 1039.5 px, check 3 wt% at 1189.54 px (predicted 3.009, error 0.31%).
- Figure 7A: x 0 bar at 164.5 px, 150 bar at 553.0 px, check 100 bar at 423.5 px (predicted 100.0); y 0 wt% at 927.0 px, 6 wt% at 623.5 px, check 3 wt% at 775.0 px (predicted 3.005, error 0.16%).

Caltech series (Figure 7B, 77 K), how it was digitized:
- The markers are hollow squares about 8 px wide in a low-resolution raster. Their outlines are broken by the lines and markers of the other three series, so `extract --mode markers` on the original page found only edge fragments (2-3 per marker) at every tolerance and colour tried (#ec1b24 and #b91c22, tolerance 60-140, opening 0-3 px). To get one blob per marker, I made a processed copy of the page image: work/main-6_redfilled60.png (sha256 515ffacf...; script work/scripts/make_redfilled.py). Inside the Figure 7B plot area, with the legend box excluded, pixels with R - max(G,B) > 60 were taken, given a 3x3 binary closing and hole filling, and painted pure #ff0000. Pixel coordinates are unchanged, and no other pixel on the page is pure red. The tool then ran on that copy: colour #ff0000, tolerance 20, markers mode, 3-px opening, ROI 155 1035 470 1345. The archive's source_image is that processed copy. `digitize_figure.py check --at 20 --expect 5` passed (4.873 vs the paper's "~5 wt% at 77 K and 20 bar", -2.5%).
- Marker count: about 40 markers counted on the plot (approximate, about +/-3; isotherm_point_count = 40). Roughly 22 of them lie below about 3 bar, including a stack of about 11 heavily overlapping markers at p of about 0-0.2 bar between 0 and 2 wt%. The rest lie between 3 and 31 bar.
- The tool returned 15 blobs. I used only the 8 blobs whose bounding box (8-10 x 8-9 px) and pixel count (58-83) correspond to one filled marker, each checked against an overlay on the enlarged original: archive points 3 (4.297 bar), 8 (14.550), 9 (16.123), 10 (19.649), 11 (22.218), 12 (24.903), 13 (27.656) and 14 (31.017). Rejected archive points: 0 (0.000 bar, 248 px), 1 (0.174 bar, 294 px) and 2 (1.455 bar, 702 px) are merged stacks of many markers. Point 4 (6.335 bar, 36 px) is an irregular partial fill. Point 5 (8.723 bar, 72 px) is two partial markers merged, with a 15 px wide bounding box. Point 6 (9.974 bar, 12 px) is a fragment. Point 7 (11.808 bar, 156 px) is two markers merged.
- Markers I could not separate, so no rows: about 32 Caltech markers. These are all markers below about 4 bar except the one at 4.3 bar, the markers at about 5.5, 6.4, 7, 8.2, 8.8, 10, 11.1 and 12.5 bar, and the marker at about 17.5 bar. The 17.5 bar marker's outline did not close, so it was not filled and the opening removed it. These positions are approximate locations used only to describe the gap, not extracted values.
- Point 9 (16.123 bar): only the top half of this marker filled, and the blob takes in its right edge plus a few pixels toward the next marker. The ring centre is about 1.3 px to the left, so the digitized pressure may be high by about 0.17 bar (about 1%). The uptake is unaffected within about 0.2 px.

NREL series (Figure 7A, 75.6 K): 75.6 K is outside the protocol's 77 K window (76.0-79.0 K), so only the highest-pressure marker of each curve was digitized, on the original page image with a tight ROI around that marker:
- Eng. Excess: colour #6a6e9a, tolerance 90, ROI 541 827 552 839. 1 marker, 48 px, 147.18 bar, 1.874 wt%.
- Gibbs Excess: colour #00a64f, tolerance 130, ROI 541 740 552 752. 1 marker, 32 px, 146.97 bar, 3.585 wt%.
- Gibbs Excess (sk=2.1 g/cc): colour #878686, tolerance 40, ROI 541 729 552 741. 1 marker, 46 px, 147.36 bar, 3.795 wt%.
- Marker count per NREL curve: about 29 (approximate, about +/-3). There are 16 markers above 50 bar (counted in Figure 7A), 7 between 14 and 43 bar and about 6 at or below 10 bar (counted in Figure 7B); markers overlap at low pressure. The three NREL curves have markers at the same pressures. Not extracted: the other markers of each NREL curve (about 28 per curve), because they are not at 77 K.
- No `check` run on the NREL archives: the paper states no value from these curves (status left "unchecked").

## Values seen but not extracted, and why

- Figure 6 (main p.13906; uptake against BET area at 77 K and 2 bar) is not an isotherm and was not digitized. Its points for PEEK-CO2-9-1, -26 and -80 and PEEK-ST-9-47, -20 and -70 duplicate Table 1 values, which were extracted. It also shows samples whose 2-bar uptakes appear in no table or text: three CO2-derived points between the 1027 and 3103 m2/g points, and four steam-derived points (one below 1207 m2/g, one between 1294 and 1956 m2/g, two above 1956 m2/g). These are not extracted (non-isotherm figure). PEEK-CO2-9-5 (700 m2/g) is not plotted in Figure 6.
- Figure 2 (BET area against burn-off, CO2 and steam series, with error bars): characterization only, not digitized. Its samples include PEEK-CO2-9-85 (3275 m2/g per the abstract range).
- Figure 3 (DFT differential pore volume of PEEK-CO2-9-26, -59, -80 and PEEK-ST-9-35, -70) and text: characterization, not digitized. Text values: PEEK-CO2-9-80 has pores of approximately 1.2, 1.35, 1.8 and 2.5 nm, with 0.1 cm3/A/g at 1.35 nm and 0.06-0.07 cm3/A/g at 1.8 and 2.5 nm. PEEK-CO2-9-26 is dominated by pores < 1.5 nm (a bound, not entered). The largest-volume pore of PEEK-ST-9-35 is about 1.35 nm.
- Figure 4 (cumulative pore volume against BET area): characterization only, not digitized. Text: ~1.7 cm3/g for PEEK-CO2-9-80,85.
- Figure 5 (H2 NMR shift against log pressure at 100 K; estimated error +/-0.2 ppm) and Figure S2 (NMR spectra at 100 K, 10 MPa): NMR, not uptake.
- Samples with characterization but no H2 uptake value (no rows):
  - PEEK-CO2-9-59: Figures 3 and 5; about 2000 m2/g per text.
  - PEEK-CO2-9-85: 3275 m2/g; about 1.7 cm3/g.
  - PEEK-ST-9-35: Figures 3 and 5; about 1000 m2/g per text.
  - PEEK-ST-9-91: XPS C 1s = 99%, O 1s = 1%, Figure S1B.
  - PEEK-ST-9-95: NMR, Figure S2; about 3000 m2/g.
- p.13903: "graphitic slit pore materials typically have excess adsorption capacities of ~1 wt % for every 500 m2/g of surface area" (ref 10). A general rule, not a value for a sample.
- p.13902, introduction: DOE 2015 system target of 5.5 wt% (40 g/L). A target, not a measurement.
- p.13906: "PEEK-CO2-9-80 has a larger H2 gravimetric uptake compared with AX-21 at the same temperature and pressure". Qualitative.
- Table 1 "NA" entries: no value.

## Coding decisions worth checking

- Temperature: the experimental section says isotherms were measured "at NREL and Caltech at 77 K", but the Figure 7 legend and caption give 75.6 K for NREL. I used the specific 75.6 K for the NREL curves.
- The three NREL curves are coded as separate isotherms (I2, I3, I4), one per plotted curve, although they appear to be three reductions of one data set. Eng. Excess is coded basis_inferred = unknown, because engineering excess is none of the protocol bases. Its uptake_type is excess, after the printed name.
- basis_stated = false on every row: "excess" and "Gibbs Excess" are named but not defined, and the Eng. Excess curve shown beside the Gibbs curves is not one of the protocol bases.
- The ~5 wt% at 20 bar (Table 1, text, abstract) is merged with the Caltech 77 K point at 19.649 bar: same sample, same printed temperature, and within 2% in pressure. The paper does not say which laboratory's curve it is from.
- The Table 1 3.7 wt% at 2 bar is not merged with Figure 7. The SI says the 2-bar values were measured on the NREL home-built Sieverts device, a different instrument from both Figure 7 data sets. It carries no isotherm_id.
- Caltech "+/-0.1%" error is read as 0.1 wt% (uncertainty_wt_pct = 0.1).
- Caltech "Micromeritics ASAP" has no model number, so instrument_identified = false. NREL "Hy-Energy PCTPro-2000" is coded true. The NREL 2-bar "Sieverts device specially built" is not described, so it is coded false.
- replicates_reported = true for the PEEK 2-bar values that Figure 6 plots with error bars (all except PEEK-CO2-9-5), and for all PEEK-CO2-9-80 isotherm rows (independent NREL and Caltech measurements; Caltech +/-0.1%).
- Literature comparison carbons (B/C, CMK-1, AX-21, Corncob) are extracted as "previously reported" with the citation, measuring_lab_id "not stated (ref N)", area_same_sample = other_paper, and surface_area_probe_gas = unspecified. Their material classes are inferred from the names: B/C is coded doped_carbon with dopant B (inferred from the label).
- The ~50 g/L for PEEK-CO2-9-80 compressed at 15 t is coded as a separate sample, "(unlabelled 1)", a densified state with area_same_sample = parent_material. It has value_kind = unclear, because it is the authors' projection of the ~5 wt% to the compressed density.
- Volumetric capacity basis: the paper states it (wt% x ~0.7 g/mL packing density) only for PEEK-CO2-9-80. packing_volume is applied to the whole Table 1 column. For PEEK-ST-9-70 the printed 18 g/L does not equal 3.0 wt% x 0.7 g/mL.
