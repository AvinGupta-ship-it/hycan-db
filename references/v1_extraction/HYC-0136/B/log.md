# HYC-0136 extraction log (agent B)

Arifin et al. 2021, Int J Hydrogen Energy 46:31084-31095. Inputs: page images main-01 to main-12 (article) and si1-01 to si1-15 (supplementary file: a Turnitin originality report whose pages si1-05 to si1-15 reproduce the submitted manuscript text). 9 rows written. No figure was digitized, so `digitizations/` is empty.

## Sources extracted from

- main-01 (p. 31084), Highlights and Abstract: "The hydrogen adsorption at room temperature shows a promising value, 1.95 wt %"; abstract gives GRHA 1:3 = 1.95 wt %. This is the same measurement as M1 and was merged into it. The abstract's GRHA 1:3 pore volume "0.2069 cm3/g" differs from Table 1 (0.21). Rows carry the Table 1 value. The abstract also calls it "the largest pore volume", but Table 1 gives GRHA 1:1 a larger TPV (0.22).
- main-03 (p. 31086), Methods "Characterization" and "Static adsorption test": BET by N2 at 77 K (Quantachrome TouchWin), degassed at 150 °C overnight, PSD by DFT. H2 test details used on every row: custom volumetric rig (Fig. 2), samples dried overnight at 120 °C, 1 g sample, H2 set at 30 bar in the loading column and then expanded into the adsorption column, run until equilibrium.
- main-02 and main-03, Synthesis: preparation route (rice husk carbonized at 350 °C for 2 h to make RHA; impregnated with 1, 3 or 5 M H3PO4 at 80 °C for 2 h; 700 °C for 2 h in a muffle furnace using a double crucible with ceramic wool and carbon powder, no inert gas; washed to neutral pH). Used for the descriptions and the synthesis, activation and purification fields.
- main-05 (p. 31088), Functional group analysis (Fig. 4 FTIR): functional groups recorded.
- main-06 (p. 31089), Table 1: BET, TPV, Vmicro, Vmicro/TPV, Vmeso and pore size for GRHA 1:1, 1:3 and 1:5, recorded on their rows.
- main-06 (p. 31089), Table 2: XRD d spacing (stored as `interlayer_spacing_nm`) and crystallite size (in notes).
- main-07 (p. 31090), Fig. 7: Raman ID/IG and I2D/IG ratios printed on the figure (in notes).
- main-08 (p. 31091), Results "Hydrogen adsorption" text: GRHA 1:3 "around 974 mmol/g (1.95 wt %)", GRHA 1:1 "341.59 mmol/g (0.68 wt %)", GRHA 1:5 "252.31 mmol/g (0.50 wt %)". These are the same measurements as Table 4 q_e,exp and were merged into M1, M4 and M7.
- main-09 (p. 31092), Table 3, row "GRHA" (This work): 25.00 °C, 30.00 bar, 1.95 %. Merged into M1. This row is the source of the measurement temperature (298.15 K), which was also applied to GRHA 1:1 and 1:5 (see their notes).
- main-10 (p. 31093), Table 4: q_e,exp with "± 0.0100%" was extracted as the measured rows M1, M4 and M7. q_e,cal from the pseudo-first-order and pseudo-second-order kinetic models was extracted as `fitted_extrapolated` rows M2, M3, M5, M6, M8 and M9. The k1, k2, k3 and R2 values are not uptakes and are recorded in notes.
- main-10 (p. 31093), Conclusion: "up to 974 mmol/g (1.95 wt %)" for GRHA 1:3. Same measurement as M1.

## Data problems recorded in the rows

- **Unit-consistency failure (protocol §3).** Every measured value is printed in both mmol/g and wt%, and the two disagree beyond either convention. For example, W1 from 973.99 mmol/g is 196.3 wt%, but the paper prints 1.95 wt%. The printed wt% is roughly mmol/g × 0.002. Both printed values are stored, with `wt_pct_convention = unknown` and source `none`. The validator reports the matching "mmol/g and wt% inconsistent" warnings on M1, M4 and M7.
- **q_e,cal rows have no wt%.** W1 computed from them would be 67-1620 wt%, outside the schema's 0-20 wt% range, so `uptake_wt_pct` is left empty on those rows.
- **Pressure of 30 bar.** It is the pressure the paper reports for the test, but the methods describe it as the set pressure in the loading column before expansion, so the true equilibrium pressure is not reported. Whether it is gauge or absolute is not stated. Stored as 30 bar.

## Values seen but not extracted

- **Literature comparison values (not measurements of this paper).**
  - Table 3 (main-09): Palimera sprout derived carbon 25.00 °C, 15.00 bar, 1.06 % [56]; Jute fibers AC 30.00 °C, 40.00 bar, 1.20 %; Fungi based activated carbon -196.00 °C, 35.00 bar, 4.70 %; BCNTs 29.85 °C, 10.00 bar, 0.16 % [60]; MWCNTs 0.02 %; SWCNTs 0.03 %; Carbon nanofibers 25.00 °C, 120.00 bar, 1.40 % [61]; GO/ZIF-8@Pt -196.00 °C, 10.00 bar, 1.68 % [62] (MOF composite); Microporous activated carbon -196.00 °C, 1.0-10.00 bar, 0.03-23.80 % [67]; Porous carbon -196.00 °C, 10.00 bar, 7.50 % [68]; Carbon nanotubes -158.00 °C, 30.00 bar, 9.20 % [69].
  - Text on main-08 and main-09 repeats several of these: 1.06 wt % (25 °C, 15 bar) [56]; 1.2 and 4.7 wt % [56]; 0.157 wt % (10 bar, 29.85 °C) BCNTs [60]; 1.4 wt % at 120 bar, carbon nanofibers [61]; GO/ZIF-8@Pt 1.68 wt % at -196 °C and 10 bar [62].
  - Table 1 (main-06): comparison BET and pore data for Bamboo cane [42], Kenaf [27], Ginger [28], Olive stone [49] and Rice husk [45], [46]. The text on main-02 and main-05 repeats some of them (299.02, 320.67, 166.70, 1252, 344.70 and 176 m2/g).
- **Targets, not measurements.** US DOE target of 7.5 wt % (233-358 K, 3-100 bar) [63]; "a minimum of 3300 m2/g" [64] (main-09).
- **RHA (rice husk ash).** It has characterization but no H2 uptake value, so it has no row and no sample_id. Table 1: BET 8.37 m2/g, TPV 0.04, Vmicro 0.00, Vmicro/TPV 7.32 %, Vmeso 0.04 cm3/g, pore size 148.00 nm. The TGA weight loss is about 40 % (text). Its N2 isotherm is in Fig. 6(d) and its PSD inset in Fig. 5.
- **Figures that are not H2 isotherms (not digitized).**
  - Fig. 3: TGA. Weight losses are given in the text: 13.84 % (1:1), 24.66 % (1:3), 13.73 % (1:5).
  - Fig. 4: FTIR.
  - Fig. 5: PSD.
  - Fig. 6: N2 sorption isotherms at 77 K, in mmol/g of N2, not H2.
  - Fig. 7: Raman.
  - Fig. 8: XRD.
  - Fig. 9: FESEM.
- **Fig. 10 (main-08).** H2 uptake against time at 30 bar for GRHA 1:1, 1:3 and 1:5. It is a kinetic plot, not an isotherm, so it was not digitized. The curves end at the equilibrium values printed in Table 4 (q_e,exp). The time-resolved intermediate uptakes appear only in this figure and are not extracted.
- **Fig. 11a/b (main-09).** Pseudo-first-order ln(qe-qt) and pseudo-second-order t/qt against time. These are kinetic linearizations, not uptake values, and were not digitized.
- **Fig. 12 (main-10).** Intraparticle diffusion plot, uptake against t^0.5 at 30 bar. It is a kinetic plot, not an isotherm. Its points are the same time-resolved uptakes as Fig. 10 and are not extracted.
- **Supplementary file si1-01 to si1-15 (Turnitin originality report).**
  - si1-01 to si1-05 list similarity sources and contain no data.
  - si1-05 to si1-15 reproduce the submitted manuscript. Its values match the published article: 974 / 341.59 / 252.31 mmol/g and 1.95 / 0.68 / 0.50 wt %. Its Table 5 matches published Table 4 (q_e,exp, q_e,cal, k and R2), and its Table 3 and Tables 1-2 match the published tables.
  - There is no new measurement, so no SI rows were made, to avoid duplicates of M1-M9.
