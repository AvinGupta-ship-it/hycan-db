# HYC-0063 extraction log (agent B)

Paper: Balathanigaimani et al. 2009, Catalysis Today 146, 234-240. Input: 7 page images (main-1 to main-7), no SI. 34 rows written. Samples: S1 MR-1/2, S2 MR-1/3, S3 MR-1/4. Isotherms: I1-I3 = 77 K, Fig. 3 (MR-1/2, MR-1/3, MR-1/4); I4-I6 = 298 K, Fig. 5 (MR-1/2, MR-1/3, MR-1/4).

## Sources extracted from

- Table 1 (p. 236): S_BET, total pore volume, V_DR(N2), V_DR(CO2), average pore width (A, stored in nm), piece density for MR-1/2, MR-1/3, MR-1/4. Copied onto every uptake row of each sample (piece density in packing_density_g_cm3, noted as the monolith piece density).
- Section 2.1 text (p. 235): sample preparation (corn-grain activated carbons R-1/2, R-1/3, R-1/4 compressed with sodium carboxymethylcellulose into monoliths MR-1/2, MR-1/3, MR-1/4), N2 77 K / CO2 273 K physisorption (Micromeritics ASAP 2020), BET range 0.01-0.05, V_T at P/P0 0.99, pore width 4V_T/S_BET, DR on N2 and CO2.
- Section 2.2 text (pp. 235-236): 77 K volumetric analyzer [22], degassing at 473 K until 1 x 10^-3 kPa, liquid nitrogen, 5 min equilibrium per point; 298 K gravimetric analyzer with Rubotherm magnetic suspension microbalance [23], degassing 473 K for 12 h, desorption 50 to 0 bar, error range +/-0.0067 wt%.
- Section 3.2 text (p. 236): "maximum hydrogen uptake on three different carbon monoliths was observed in between 2.39-2.45 wt% at 77 K and 1 bar" -> rows M10 (2.39, MR-1/2) and M22 (2.45, MR-1/3). The range has no per-sample labels in the text; the endpoints are assigned using the digitized Fig. 3 curves at 1000 mbar (MR-1/2 2.386, MR-1/3 2.448, MR-1/4 2.428 wt%) and, for MR-1/2, the printed 10.01 g/L / 0.420 g/cm3 = 2.38 wt%. No separate value is printed for MR-1/4.
- Section 3.2 text (p. 238): MR-1/2 "maximum volumetric H2 adsorption capacity as 10.01 g/L at 77 K and 1 bar" -> on row M10 (same sample, T, p as the 2.39 wt% value), volumetric_capacity_basis packing_volume (per monolith piece volume, from mass-basis uptake x piece density [14]).
- Section 3.3 text (p. 238): "At 298 K and 50 bar ... MR-1/2, MR-1/3 and MR-1/4 ... 0.40, 0.41 and 0.46 wt%" -> rows M11, M23, M34, each merged with the highest-pressure point of its Fig. 5 isotherm (digitized 49.91 bar 0.4012; 49.36 bar 0.3989; 50.06 bar 0.4535 wt%).
- Fig. 3 (p. 236), H2 at 77 K, three lines without markers -> 10 points per line at k/10 x p_end (rows M1-M9, M12-M21, M24-M33; the MR-1/2 k=10 point at 1.0107 bar is merged into text row M10). Archives HYC-0063_fig3_MR-1_2.json, _MR-1_3.json, _MR-1_4.json.
- Fig. 5 (p. 238), H2 adsorption/desorption at 298 K, three panels with markers -> only the highest-pressure point of each isotherm digitized (merged into the text rows above). Archives HYC-0063_fig5a_MR-1_2_top.json, HYC-0063_fig5b_MR-1_3_top.json, HYC-0063_fig5c_MR-1_4_top.json.
- Conclusion (p. 240): repeats the ranges 2.39-2.45 wt% (77 K) and 0.40-0.46 wt% (298 K); same values as above, no extra rows.

## Figure digitization details

Fig. 3 calibration (page main-3.png): x 0 mbar at px 736.46 (left frame), 1200 mbar at px 1095.65 (right frame), verify 600 mbar tick at px 915.92 (0.08% error); y 0 wt% at px 996.83 (bottom frame), 3 wt% at px 626.40 (top frame), verify 1.5 wt% tick at px 811.53 (0.05% error). Ticks located by darkness-weighted centroids of pixel rows/columns.

Fig. 3 curve separation: the legend shades are MR-1/2 mid-grey thick, MR-1/3 dark thin, MR-1/4 light grey, but in the plot all three lines render dark and lie within 1-14 px of one another (separate below about 430 mbar and above about 880 mbar, merged into one 3-5 px band in between). No colour/tolerance/ROI setting of digitize_figure.py separates them. They were therefore separated by a deterministic script (work/fig3_separate.py): per pixel column, dark runs (grey < 215) are found and split at interior intensity maxima >= 35 levels lighter than both flanking minima; series are assigned to runs by an order-preserving nearest-prediction assignment, with the vertical order taken from the page in the separated regions (low pressure, top to bottom: MR-1/2, MR-1/4, MR-1/3; at the high-pressure end: MR-1/3, MR-1/4, MR-1/2); in the merged band (x 918-963 px) every series receives the whole band. One masked copy of the page per series (work/fig3_mask_MR-1_2.png, _MR-1_3.png, _MR-1_4.png; non-series pixels set to white) was then digitized with `digitize_figure.py extract --mode curve --color #000000 --tolerance 372 --roi 744 629 1093 987` (tolerance 372 = all kept pixels with grey < 215; the archive's source_image is the masked copy, with its sha256). No dark pixel in the plot was left unassigned.

Curve-to-sample mapping: at 1 bar it is fixed by the text range and the checks (MR-1/2 2.386 vs printed 2.39; MR-1/3 2.448 vs printed 2.45; both pass). At low pressure the upper line is taken as MR-1/2 and the lighter line of the lower pair as MR-1/4 (MR-1/2 thick line; MR-1/4 lightest; this order also follows the paper's CO2 uptake order MR-1/2 > MR-1/4 > MR-1/3). This means MR-1/2 crosses the other two inside the merged band; the alternative (no crossing, upper line = MR-1/3) cannot be excluded from the pixels. It would swap the MR-1/2 and MR-1/3 values below about 430 mbar (by up to about 0.1 wt% at 100 mbar). Recorded with extraction_confidence 2.

Line ends: MR-1/2 ends at 1010.74 mbar, MR-1/3 at 1047.49 mbar. The MR-1/4 line merges into the MR-1/3 line near its end; its end is taken where its own run disappears (1020.76 mbar). The lowest trace point is 25.19 mbar (ROI starts right of the y-axis inner ticks), below 5% of p_end, so the read pressures are k/10 x p_end, k = 1-10. The paper does not state that the lines join measured points, so these rows are value_kind fitted_interpolated, and isotherm_point_count is empty.

Check for MR-1/4 (Fig. 3): the paper gives no per-sample value; the archive check was run as 2.42 +/- 0.03 wt% at 1000 mbar, which encodes only "within the printed range 2.39-2.45 wt%" (passed, 2.428). The archive records 2.42 as "expected"; that number is not printed in the paper.

Fig. 5 calibration (page main-5.png), per panel, frame lines as 0/60 bar and 0/0.5 wt%, inner ticks for verification: top panel x 181.50/549.50, verify 20 bar at 304.03; y 491.38/125.25, verify 0.2 at 344.82. Middle panel x 181.30/548.91, verify 303.70; y 933.27/565.86, verify 786.30. Bottom panel x 180.21/548.91, verify 302.88; y 1372.10/1005.35, verify 1225.67. All verification errors < 0.2%. The 50 bar point in each panel is an open (desorption) marker drawn on the end of the adsorption line; it was extracted with `--mode markers --open-px 0` and a tight ROI around the marker to exclude the connecting line (1 marker found = 1 counted). Checks against the printed values pass (0.30%, 2.70%, 1.41%).

Fig. 5 point counts (isotherm_point_count, both branches, 50 bar turning point counted once): MR-1/2 15, MR-1/3 16, MR-1/4 17. Approximate: markers below about 2 bar overlap and cannot be counted exactly.

## Values seen but not extracted

- Fig. 5, all points other than the highest-pressure point of each isotherm (both branches, 298 K): out of scope (non-77 K isotherm).
- MR-1/3 at 298 K: printed 0.41 wt% vs digitized Fig. 5 point 0.399 wt% (2.7% lower). The printed value is used (row M23); Fig. 6 plots the MR-1/3 mass-basis point near the printed value.
- Fig. 4 (p. 237, not an isotherm): mass-basis (wt%) and volume-basis (g/L) H2 capacities at 77 K and 1 bar plotted against S_BET, pore width, V_DR(N2), V_DR(CO2), V_T and piece density. Values not given in tables/text: the MR-1/4 mass-basis value at 77 K, and the volume-basis values of MR-1/3 and MR-1/4 at 77 K. Not digitized.
- Fig. 6 (p. 239, not an isotherm): the same comparison at 298 K and 50 bar. Values not given in tables/text: the volume-basis (g/L) capacities of MR-1/2, MR-1/3 and MR-1/4 at 298 K (text says only that MR-1/2 is largest). Not digitized.
- Fig. 1a/1b (p. 235): N2 (77 K) and CO2 (273 K) physisorption isotherms, not H2. Not extracted.
- Fig. 2 (p. 236): N2 adsorption energy distributions (peaks 3-7 and 7-11 kJ/mol), not H2 uptake. Not extracted.
- Text p. 236: "maximum hydrogen uptake ... in between 2.39-2.45 wt%" is a range across the three samples; only its endpoints were turned into rows (see above); MR-1/4 has no printed 77 K value.
- R-series powdered activated carbons R-1/2, R-1/3, R-1/4: precursors of the monoliths, no H2 uptake and no characterization in this paper. No rows.
- Comparisons with coal-based, coconut-based and commercial ACs, carbon cloths, ACF, Maxsorb, AX-21 and coal-based monoliths (refs [3,4,8-12,14,28-30]) are qualitative; no values printed. Not extracted.

## Coding decisions

- material_class composite: the monoliths contain sodium carboxymethylcellulose binder (polymer); the paper does not state that it was removed or carbonized. synthesis_method carbonization (carbonized corn-grain char); the char:activating-agent activation (agent not named) is in activation_method.
- basis: no basis named anywhere. 77 K volumetric rows basis_inferred excess (instrumental default); 298 K gravimetric rows unknown (no buoyancy correction stated). uptake_type unspecified on all rows.
- wt% convention unknown/none: no mmol/g, mg/g or cm3(STP)/g H2 values printed (only g/L, which does not qualify as a paired unit).
- instrument_identified false for both instruments (77 K analyzer unnamed; Rubotherm microbalance named without model). calibration_described false for both (no free-volume or buoyancy procedure stated).
- replicates_reported true with uncertainty 0.0067 wt% only on the 298 K rows: the "+/-0.0067 wt%" sentence ends the 298 K gravimetric paragraph; not applied to the 77 K volumetric rows (false).
- area_same_sample yes: Section 2.1 says the authors measured the monoliths by N2/CO2 physisorption; the N2 isotherms are also cited with ref [18] (authors' earlier paper on the same monoliths).
- measuring_lab_id: corresponding author H. Moon (asterisk), affiliation a, Chonnam National University; the paper does not say either H2 measurement was made in another laboratory.
- Fig. 3 MR-1/3 text value 2.45 wt% at 1 bar (M22) is not within 0.02 bar of a read point (0.9427, 1.0475 bar), so it is a separate row; it carries isotherm I2 because the text introduces it as the uptake observed in the Fig. 3 measurements.
