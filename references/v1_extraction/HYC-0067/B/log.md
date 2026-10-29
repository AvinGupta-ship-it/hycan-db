# HYC-0067 extraction log (agent B)

## Sources extracted from

- main-2.png (p. 221), Abstract: "applied in H2 adsorption/desorption process at 77 K and pressure of 20 bar. The mass uptake is found to be 0·643 wt-%" (Fe-GNF 9). Merged into M15. It is the same value as the text and Conclusions.
- main-5.png (p. 224), text "H2 adsorption and desorption": "Based on Fig. 4 a maximum H2 uptake of 0·643 wt-% is obtained" (Fe-GNF 9, 77 K, 20 bar). M15 (text_direct). It is the same measurement as the highest-pressure adsorption marker of Fig. 4: digitized at 19.6871 bar, 0.643501 wt%, within 2% of 20 bar. The paper says the value comes from Fig. 4.
- main-5.png (p. 224), Conclusions: "up to a pressure of 20 bar, the mass uptake is 0·643 wt-%". Same value as M15. No separate row.
- main-5.png (p. 224), Fig. 4 "H2 adsorption and desorption at 77 K and 20 bar" (Fe-GNF 9, isotherm I1). Both branches digitized. Rows: M1-M14 (adsorption), M15 (text value merged with the last adsorption marker), M16-M29 (desorption).
  - Calibration on main-5.png pixels. x: 0 bar at px 163.5, 20 bar at px 586.5, checked at 10 bar (px 375.2; predicted 10.009). y: 0 wt% at px 457.5, 0.7 wt% at px 109.5, checked at 0.3 (px 308.0; predicted 0.3007). Tick positions were found from pixel rows and columns. Other ticks also agree: 0.5 at px 208.5 gives 0.5009, and 15 bar at px 480.8 gives 15.002.
  - The tool ran on a work copy of the page (work/main-5_legend_masked.png). This copy is main-5.png with the legend box (px x 480-579, y 420-453) filled white, so legend symbols could not be read as data markers. Nothing else in the copy was changed.
  - Adsorption, blue diamonds (#25286d, tolerance 60, --open-px 2): archive digitizations/HYC-0067_fig4_adsorption.json. I counted 16 markers on the plot and the tool extracted 15 (see below). The tool's check against the paper's 0.643 wt% at the last marker passed (0.08%).
  - Desorption, pink squares (#be33a1, tolerance 50, default opening): archive digitizations/HYC-0067_fig4_desorption.json. I counted 15 markers and the tool extracted 15. There is no stated value to check against, so the archive status is "unchecked".
  - isotherm_point_count = 31 (16 adsorption + 15 desorption markers counted on the plot).
- main-3.png (p. 222), Table 1 "H2 uptake under various pressures and temperatures": 5 values for GNF from other studies (Refs. 6-10). M30-M34, samples S2-S6, labels (unlabelled 1)-(unlabelled 5). They are extracted under the "values reported before" rule, with `previously reported:` in notes. They are literature values the authors list for comparison and were not measured in this work. The Table 1 footnote "*(weight of adsorbate/weight of adsorbent) × 100%" defines wt% as W1, so these rows are coded wt_pct_convention = W1, source = stated. measuring_lab_id is "Ref. n (HYC-0067)" because the paper names no laboratory or institution for these values. No surface area is given, so surface_area_method = not_reported.
- main-4.png (p. 223), Table 3: BET area 556·65 m2 g-1 and d002 3·423 Å (0.3423 nm) for Fe-GNF 9. These are carried on every S1 row.
- main-3.png (p. 222), Experimental sections (Hydrogen adsorption/desorption process; Characterisation; set-up). These give the method codes for S1: gravimetric; degassed 250 °C for 12 h; 77 K in liquid nitrogen (77 K printed); BET by Quantachrome Autosorb 1 with N2, samples degassed 4 h at 250 °C; no BET range or consistency criteria; no H2 instrument, buoyancy correction, sample mass or H2 purity stated.

## Values seen but not extracted, with reasons

- Fig. 4, adsorption marker near 4 bar (about 0.47 wt%). It lies almost entirely under the desorption square at 3.97 bar. Only about 1 matching blue pixel is visible (px 251, 225). Changing the tolerance (40-80) and the opening (0-3) did not separate it as a marker, so it was not extracted. It is counted in isotherm_point_count.
- Fig. 4, lowest desorption marker. The tool digitized it at 0.0000 bar, 0.03118 wt%: the square is centred on the y axis at px 163.5. The validator rejects pressure_bar = 0, so no row was written for it. It is counted in isotherm_point_count. The archive keeps the point.
- Fig. 4, the adsorption line runs flat past the last visible marker (19.69 bar) to the plot edge at about px 590 (about 20.2 bar), with no visible marker. A further point beyond the axis maximum may exist but is not shown. Nothing was extracted or counted for it.
- Fig. 4, adsorption marker at the origin (M1, 0.0236 bar, 0.00066 wt%). It is partly covered by the axes, so the centroid comes from its visible part. The row is kept.
- Introduction (main-2.png, p. 221): "GNF is capable of adsorbing and retaining up to 30 L H2 per gram of carbon at room temperature" (Ref. 4). Not extracted. It is a cited claim of capability with no pressure, a temperature stated only in words, and a gas volume with no STP reference. As mL(STP) g-1 it would be 30000 (about 270 wt%), outside the schema ranges.
- Introduction: "From Table 1, it can be seen that the H2 uptake of the GNF <1 wt-%". This is a summary bound over the Table 1 values, not a separate measurement.
- Introduction: the US DOE target of 6·5 wt-% is a target, not a measurement.
- Introduction, general characterization (not tied to any sample): AC >1000 m2 g-1; GNF typically 200-300 m2 g-1; GNF interplanar distance 3·37 Å; H2 kinetic diameter 2·89 Å.
- Fe-GNF 1-8 have characterization but no H2 uptake, so they have no rows. Synthesis conditions (Table 2: time h, C2H4/H2 mL min-1, temperature °C) and Table 3 values (BET m2 g-1, d002 Å, morphology):
  - Fe-GNF 1: 2 h, 10:90, 500 °C; 180·15; 3·356; platelet.
  - Fe-GNF 2: 2 h, 20:80, 600 °C; 256·80; 3·394; herringbone.
  - Fe-GNF 3: 2 h, 30:70, 700 °C; 83·88; 3·376; nanotube, herringbone.
  - Fe-GNF 4: 3 h, 10:90, 600 °C; 259·05; 3·422; herringbone.
  - Fe-GNF 5: 3 h, 20:80, 700 °C; 94·47; 3·375; nanotubes.
  - Fe-GNF 6: 3 h, 30:70, 500 °C; 135·30; 3·382; herringbone.
  - Fe-GNF 7: 4 h, 10:90, 700 °C; 87·52; 3·380; nanotube.
  - Fe-GNF 8: 4 h, 20:80, 500 °C; 211·40; 3·399; herringbone, platelet.
  - XRD phases (Fig. 2): graphite, Fe2O3, Fe3C and Fe in various samples. Fe-GNF 9 shows only Fe3C besides graphite.
- The Taguchi yields and S/N ratios are not H2 values. The text gives Fe-GNF 9 a yield of 4·955 g gcat-1 h-1 and S/N 11·594, while the Abstract and Conclusions give 4·489 g gcat-1 h-1 for the optimum sample (an inconsistency in the paper). Fe-GNF 5 S/N smaller-is-better is -26·37.
- Fig. 2 (XRD) and Fig. 3 (TEM) are not isotherms and show no H2 values.

## Coding decisions

- sample_id is numbered only for samples that have rows, in order of first appearance. S1 is Fe-GNF 9, which first appears in the Abstract as the optimum sample (600 °C, 4 h, 30:70 = Table 2 run 9; BET 556·65). The Table 1 literature samples come next (S2-S6, from the Introduction and Table 1).
- Fe-GNF 9 is coded material_class carbon_nanofiber with residual_metal_element = Fe. XRD shows residual Fe3C catalyst, and its amount is not stated. The Fe3C is leftover synthesis catalyst, not an added component, so the sample is not coded composite. The reconciler may revisit this.
- Fe-GNF 9 basis: the basis is not named and the method is gravimetric with no buoyancy correction stated, so basis_stated = false, basis_inferred = unknown and uptake_type = unspecified. The wt% convention for Fig. 4 data is unknown/none. The Table 1 footnote defines wt% for the literature table only.
- measuring_lab_id for S1 is "Sufian group, Universiti Teknologi PETRONAS". Sufian is the corresponding author (*), and the first affiliation is Universiti Teknologi PETRONAS. The acknowledgement thanks the University of Nottingham for "collaboration studies as well as facilities", but the paper does not say the H2 measurement was made there.
- area_same_sample = yes. The text says "The as prepared sample Fe-GNF 9 is selected to undergo H2 adsorption", and the Table 3 area is for as-prepared Fe-GNF 9.
- digitization_uncertainty_wt_pct and the other fields the instruction reserves were left empty.
