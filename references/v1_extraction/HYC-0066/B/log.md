# HYC-0066 extraction log (agent B)

## Sources extracted from

- Table 1 (main-4, J. Mater. Chem. p.149): H2 uptake (wt%) of all 8 samples (BF-900, BF-1000, BF-1050, BF-1100, ACBF-900, ACBF-1000, ACBF-1050, ACBF-1100), with surface area (micropore surface area), pore volume (micropore volume) and pore size maxima. 8 table_direct rows at 20 bar, each merged with its plotted 20-bar point where that point could be digitized.
- Section 2.2 and 2.3 text (main-2, p.147): N2 sorption method (ASAP 2020, BET range 0.06-0.22, total pore volume at P/P0 = 0.99, NLDFT), H2 method (IGA gravimetric, 99.9999% H2, oven drying 24 h at 80 C, degas 200 C and 10^-10 bar for 4-6 h, 0-20 bar at -196 C, liquid nitrogen bath).
- Section 3.4 text (main-5, p.150): isotherms at -196 C and 20 bar in Fig. 6a/6b; the uptake at 20 bar is summarised in Table 1; wt% calculated with a density of 1.5 g cm-3 for the carbons and 0.04 g cm-3 for hydrogen (coded as a stated buoyancy correction, so calibration_described = true and basis_inferred = excess; basis_stated = false because no basis is named); isotherms completely reversible, no hysteresis, no saturation within 20 bar.
- Fig. 6a (main-5, p.150), 77 K isotherms of BF-T carbons: series BF-900 (archive Fig6a_BF-900.json) and BF-1050 (archive Fig6a_BF-1050.json) digitized.
- Fig. 6b (main-5, p.150), 77 K isotherms of ACBF-T carbons: all four series digitized (archives Fig6b_ACBF-900.json, Fig6b_ACBF-1000.json, Fig6b_ACBF-1050.json, Fig6b_ACBF-1100.json).
- Text p.151, p.152 and abstract: 6.2 wt% for ACBF-900 at -196 C and 20 bar (same value as Table 1; one row).

## Digitization

- Page image main-5.png (1241 x 1625 px, about 150 dpi). Markers are 3-5 px wide; all calibrations from tick-mark pixel centroids.
- Fig. 6a: x 0 bar at px 690.99, 20 bar at 871.03, check 10 bar at 780.94; y 0.0 wt% at px 1388.0, 3.5 wt% at 1213.6, check 2.0 wt% at 1288.31 (residuals 0.08% and 0.03%).
- Fig. 6b: x 0 bar at px 935.89, 20 bar at 1128.64, check 10 bar at 1032.24; y 0 wt% at px 1394.96, 7 wt% at 1213.75, check 4 wt% at 1291.51 (residuals 0.03% and 0.1%).
- Settings (markers mode, open-px 1, marker-min-px 2, marker-max-px 40): BF-900 and ACBF-900 colour #187040 tol 30; BF-1050 #3c50a0 tol 15; ACBF-1050 #3c50a0 tol 12; ACBF-1000 #d21e1e tol 40; ACBF-1100 #000000 tol 160 on a derived copy of main-5.png (work/main-5_neutral.png) in which every pixel with max(RGB) - min(RGB) >= 45 was set to white, because the thin black crosses could not be isolated by colour from the green, blue and red series on the original image; pixel geometry is unchanged. ROIs were set to exclude the legends and titles.
- The tool's `check` step could not be run: Table 1 states 20 bar, and every digitized series ends at 19.69-19.98 bar, outside which `check` refuses to evaluate. Archives therefore remain status "unchecked". Manual comparison of the last plotted marker with Table 1: BF-900 2.636 vs 2.6; BF-1050 3.116 vs 3.1; ACBF-900 6.227 vs 6.2; ACBF-1000 4.866 vs 4.9; ACBF-1100 4.724 vs 4.7; ACBF-1050 merged 19.5/20 bar blob 3.743 vs 3.9 (see discrepancies).
- All plotted markers are coded adsorption: the plots do not distinguish branches, and the paper says the isotherms are completely reversible. The extra points at 8.5, 18.5 and 19.5 bar in several series could be desorption points, but nothing in the paper says so.

## Markers seen but not extracted, with reason

- Fig. 6a BF-1000 (red circles) and BF-1100 (black crosses): not digitized. The two curves coincide along their whole length; the crosses are drawn over the circles and the markers cannot be separated, so no marker could be assigned to either series or counted. Only their Table 1 values (3.0 and 3.0 wt% at 20 bar) are rows.
- All 8 series: the low-pressure markers (below about 1-1.5 bar) form an unresolved pile along the y axis, overlapping each other and the other series. They could not be separated or counted and are not extracted. isotherm_point_count therefore gives only the markers I could count and is a lower bound.
- Archive points not used as rows (blobs of several merged markers): Fig6a_BF-900.json 1.022 bar (16 px, low-pressure pile); Fig6a_BF-1050.json 0.918 bar (12 px, pile) and 8.245 bar (14 px, the 8 and 8.5 bar markers merged); Fig6b_ACBF-1000.json 0.961 bar (27 px, pile); Fig6b_ACBF-1050.json 1.187 bar (15 px, the ca. 1.1 and 1.5 bar markers merged) and 19.691 bar (15 px, the 19.5 and 20 bar markers merged).
- Fig. 6b ACBF-1050: the 11 bar marker is visible but its colour core was too small to extract (rejected as 1 px), so it has no row. Its 19.5 and 20 bar markers overlap, so the 20-bar table row carries no digitized point.
- Fig. 6b ACBF-1100: the marker near 1.45 bar lies inside the low-pressure overlap (below the ROI) and is not extracted. A possible marker near 18.5 bar could not be resolved from the 18 bar marker.
- Fig. 6b ACBF-900 at 1.10 bar, ACBF-1050 at 5.93 bar, ACBF-1100 at 1.93 and 15.0 bar, and Fig. 6a BF-1050 at 1.17 and 17.1 bar: partly hidden markers, extracted from 2 px or fewer, with extraction_confidence 2. All ACBF-1100 rows have confidence 2 because of the derived image.

## Values seen but not extracted, with reason

- Table 1 "H2 uptake density" (umol H2 m-2): 13.9, 13.3, 14.5, 14.1, 9.7, 12.9, 13.7, 15.4. These are uptake per surface area computed by the paper, not areal uptakes of a film; they are recorded in each sample's notes, not in areal_uptake_g_cm2.
- Abstract and conclusions: "2.6-3.1 wt%" and "3.9-6.2 wt%" at -196 C and 20 bar restate the Table 1 values. "13.0-15.5 umol H2 m-2" restates the density column.
- Percentage changes (activation raises uptake by 25-140%; ACBF-900 140%; ACBF-1000 ca. 65%; increases in surface area and pore volume of 30-240%, 67%, 64%, 60%, 60%, 240%, 190%, 180%) are derived comparisons, not uptake values.
- Literature comparisons on p.151 are other papers' data, not this paper's measurements: KOH-activated CDCs 10 +/- 0.7 and CO2-activated CDCs 9 +/- 0.1 umol H2 m-2 (-196 C, 60 bar, ref. 7c); activated carbon/CNT composites 9.55 umol H2 m-2 (-196 C, 60 bar, ref. 8a); activated carbons, SWNTs, SWNHs and GCFs 11.75 umol H2 m-2 (-196 C, 20 bar, ref. 28); KOH-activated anthracite carbons 9 +/- 0.1 umol H2 m-2 (-196 C, 20 bar, ref. 8b). Chahine rule (1 wt% per 500 m2 g-1) is a literature relation.
- Fig. 7 (main-6) and ESI Fig. S7 (si1-7): uptake against surface area, pore volume, micropore surface area and micropore volume. These are not isotherms, and their values are the Table 1 values.
- ZIF-8 template (Basolite Z1200): not a carbon sorbent and has no H2 uptake. Characterization: surface area 1417 m2 g-1, pore volume 0.77 cm3 g-1, micropore surface area 1397 m2 g-1, micropore volume 0.67 cm3 g-1, NLDFT pore maximum ca. 11 A (text p.147, Fig. S3). TGA in N2: stable to 500 C, residue ca. 35 wt% at 1000 C (Fig. S2).
- ZIF/FA composite: TGA in air, mass loss 350-550 C, residue ca. 33% (Fig. S4b). No H2 uptake.
- Figs. 1-5 and S1-S6 (XRD, TGA, N2 isotherms, SEM, PSDs) contain no H2 uptake. BF-T TGA residues (ca. 11.5 wt% BF-900, ca. 2 wt% others) and carbon yield ca. 97 wt% are in notes or not needed.

## Discrepancies in the paper (recorded, not resolved)

- Text p.150 says BF-1000, BF-1050 and BF-1100 have "between 2.9 and 3.1 wt%", but Table 1 prints 3.0, 3.1 and 3.0.
- Fig. 6b ACBF-1050 (blue squares) ends near 3.74-3.75 wt% at 19.5-20 bar, but Table 1 gives 3.9 wt% (about 4% higher). The legend order and the other three series match Table 1.
- Text p.150 gives the activated surface areas as "1608-3188 m2 g-1", but the smallest ACBF surface area in Table 1 is 1425 (ACBF-1050).
- Text p.151 gives the density range (excluding ACBF-900) as 13.3-15.4 umol H2 m-2 and the abstract gives 13.0-15.5, but Table 1 has 12.9 for ACBF-1000.
- Experimental (p.147) names the template as Basolite Z1200 from Sigma-Aldrich, and the abstract and introduction name BASF.

## Coding decisions

- Samples S1-S8 are in the order of carbonization temperature in Section 2.1 and Table 1. All are templated_carbon with synthesis_method template_synthesis. KOH activation goes in activation_method for the ACBF samples.
- BF-900 retains Zn from incomplete template removal (TGA residue ca. 11.5 wt%), so residual_metal_element = Zn. Its Zn content is not stated, so residual_metal_wt_pct is left empty.
- Temperature: -196 C is printed, so 77.15 K with temperature_inferred = false.
- degas_duration_h is left empty because the paper prints a range (4-6 h). degas_end_pressure_pa is 1e-05, from the printed 10^-10 bar.
- skeletal_density_g_cm3 = 1.5 is the assumed carbon density used in the wt% (buoyancy) calculation, not a measured He density.
- instrument_identified = false, because the paper names the "intelligent gravimetric analyser (IGA)" without a manufacturer.
- pore_volume_method = other: the total pore volume is single-point at P/P0 = 0.99, and the micropore volume method is not stated. average_pore_diameter_nm is left empty because Table 1 gives three NLDFT pore size maxima.
