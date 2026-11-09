# HYC-0135 extraction log (agent A)

- Fig. 4a (main.pdf p.4), GS@77K: 12 filled-square markers counted, 12 digitized (rows M1-M12). The first three markers (0.13-0.17 kPa) overlap and merged into one blob in the tool; they were separated by row-slice ROIs (GS_77K_fig4a_m1/m2/m3.json); the other nine are in GS_77K_fig4a_p4-12.json. The legend marker was excluded by ROI.
- Fig. 4a, GS@87K: 15 open-square markers counted; only the highest-pressure point digitized (M13), per scope for non-77 K isotherms. Open marker digitized with --open-px 1 on a ROI around the outline.
- Fig. 4b (p.4), BP280@77K: 9 filled stars counted, 9 digitized (M14-M22); legend star excluded by ROI (two archive files).
- Fig. 4b, BP280@87K: about 8 open stars counted (4 overlapping near the origin, count uncertain); only the highest-pressure point digitized (M23). The thin outline star was captured as a 16-px group; centroid may be about 0.5 px off (under 1% of the axis span).
- Axis calibration: Fig. 4a x ticks 0.2 at px 233, 1.0 at px 518, check 0.6 at px 375; y ticks 0.02 at 1425.5, 0.10 at 1203, check 0.06 at 1314. Fig. 4b x 0.2 at 743.5, 1.2 at 1075, check 0.6 at 876; y 0.002 at 1408.5, 0.008 at 1188.5, check 0.004 at 1335. Tick pixels found by inspecting pixel rows/columns. The tool's `check` step was not run: the paper prints no uptake value to compare with.
- Archives are saved with status "unchecked" for the same reason.
- Pressure axis is kPa (converted to bar); uptake axis is mmol g-1, so uptake_mmol_g holds the digitized value and uptake_wt_pct is W1 computed from it.
- Fig. 5 (p.5): Gamma_1 (nm-2) against P/Pa at low coverage, replotting of Fig. 4 data in surface-excess units. Not an H2 uptake in wt%, mmol/g or cm3/g; not digitized.
- Table 3 (p.5): Henry constants H_P, virial constants B_AS and zero-coverage isosteric heat q0st at 77 and 87 K. Derived quantities, not uptake; not extracted. Text values (q0st mean 6.399 and 3.735 kJ/mol; the conclusions print 3.635 for BP280, which disagrees with the 3.735 in the text) also not uptake.
- Table 4 and Fig. 6: potential well depths epsilon_sf/k; not uptake.
- Table 1 (EDS): GS C 78.88, O 13.62, P 3.24, Cl 0.12, Nb 4.14 atom %; BP280 C 99.02, S 0.98 atom %. Put in material_description; the non-carbon elements are called impurity and no phase is identified, so material_class was not set to composite for GS and metal fields were left empty.
- Table 2: BET 220.5 and 36.1 m2 g-1, pore volume 0.2248 and 0.1015, micropore volume 0.0301 and 0.0047 cm3 g-1 (DFT, Ar 87 K); recorded on every row.
- Abstract rounds the areas to about 220 and 36 m2/g; not extracted separately.
- Fig. 2 (Ar 87 K isotherms) and Fig. 3 (PSD): not H2; not extracted.
- Values with no home: no H2 uptake in wt% printed anywhere; no uptake value printed in any table or text.
- Materials not extracted: none (no non-carbon comparison sorbents).
