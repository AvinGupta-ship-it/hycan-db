# HYC-0061 extraction log (agent B, 2026-11-09)

Input: page images main-1 to main-7 (journal pp. 714-720); no supplementary file. 81 rows written.

## Samples
- S1 MWCNTs, label "MCNTs" (first figure legend naming the sample is Fig. 4, "hydrogen adsorption of MCNTs"; Fig. 3 legend names no sample; "MWCNTs" everywhere else). Order of samples follows the abstract: MWCNTs, AC, SWCNTs, GNFs, GO.
- S2 AC, S3 SWCNTs, S4 GNFs (labels from the Fig. 9 and Fig. 10 legends), S5 GO (Fig. 10 legend).
- Only AC has a surface area: "BET surface area of >1900 m2 g-1" in the purchase description (Section 2.1); stored as 1900 with area_same_sample = other_paper (no N2 measurement described; read as supplier specification). MWCNTs, SWCNTs, GNFs and GO have no surface area or pore data (surface_area_method = not_reported); their purities and tube/fibre diameters are in material_description.

## Passages, tables and figures extracted from
- p. 715 Section 2.1 (materials, suppliers, AC BET >1900), 2.2-2.3 (Sieverts apparatus, Rosemount 3051H transducers, cell volumes, He residual-volume determination, heating-cooling degassing cycle without conditions, H2 99.999%): method fields on every row.
- p. 717 Fig. 3 (MWCNTs 0.302 g, ambient): highest-pressure point of each curve. 'Z correction' (10 markers, all extracted) merged with the Section 3.1 text value 0.264 wt% at 7.5 MPa (M2; plotted point at about 7.24 MPa, merged because the text says the value is from Fig. 3). 'without Z correction' (10 markers counted; 7 extracted, the markers at about 0.35, 0.57 and 1.42 MPa are hidden under the red markers; only the highest point is used) -> M1. Temperature 295 K taken from the Fig. 4 caption for the same 0.302 g measurement (0.80 mg / 0.302 g = 0.265 wt% equals the Fig. 3 Z-corrected end point).
- p. 717 Section 3.2 text: MWCNTs 0.15 wt% at 7.5 MPa after cell correction (M3).
- p. 718-719 text + Fig. 9 (AC, ambient): 0.62 wt% original and 0.47 wt% final at 7.5 MPa merged with the highest-pressure points of the two AC curves (M4, M5; plotted at 7.62 and 7.61 MPa, within 2%). 10 markers per curve, all extracted.
- p. 719 text + Fig. 10 (ambient): "final adsorption values were 0.35, 0.2, and 0.1 wt.% for SWCNTs, GO, and GNFs" (no pressure) merged with the highest-pressure point of each curve, pressure digitized (M6-M8). SWCNTs 9 markers, GO 10 markers (all extracted). GNFs: 8 markers visible, 7 extracted; the lowest-pressure GNF marker (about 0.3 MPa) is mostly hidden under the GO and SWCNT markers, and further GNF markers near zero uptake at 0.55-0.86 MPa may be hidden under GO markers (not separable). Digitized SWCNT end point is 0.337 wt% against the printed 0.35.
- p. 719 Fig. 11 (0.375 g AC, 77 K): every point of 'original adsorption' (14 markers counted; 9 extracted; the 5 markers at about 0.01-1.23 MPa are covered by the green final-adsorption markers and could not be separated, even with smaller opening/marker size, which only returned crescent fragments with biased centres) -> M9-M17; every point of 'final adsorption' (14 of 14) -> M18-M31.
- p. 719 Fig. 12 (77 K, final adsorption): every point of GNFs (10 markers; the lowest-pressure marker digitizes to -0.0109 wt% at 0.166 MPa and is not recorded because uptake_wt_pct must be >= 0), GO (12 of 12), MWCNTs (9 of 9), SWCNTs (10 of 10) -> M32-M71.
- p. 719 text and p. 720 Conclusions: "Compared with AC (4 wt.%)" / "except AC (4 wt.%)" -> M72 (no pressure printed; not merged because several plotted points of the Fig. 11 final curve round to 4 wt% and the paper does not identify one); "less than 1 wt.% at 77 K (up to 7.5 MPa)" for SWCNTs, MWCNTs, GO, GNFs -> upper bounds M73-M76; "no more than 0.5 wt.% at ambient temperature" for MWCNTs, AC, SWCNTs, GNFs, GO -> upper bounds M77-M81.

## Digitization
- Axes calibrated on frame/tick pixels found by scanning pixel rows and columns (tick lengths 6 px major); third-tick checks all within 0.5%. Fig. 3: x 0 at 186, 8 at 589 (check 4 at 387.5); y 0 at 1047, 0.35 at 747 (check 0.15 at 919). Fig. 9: x 0 at 176.5, 8 at 589 (4 at 383); y 0 at 968, 0.7 at 664 (0.3 at 837.5). Fig. 10: x 0 at 175, 8 at 588 (4 at 382); y 0 at 1464, 0.4 at 1160 (0.2 at 1312). Fig. 11: x 0 at 739, 8 at 1125 (4 at 932); y 0.0 at 449, 4.5 at 153.5 (2.0 at 317.5). Fig. 12: x 0 at 715, 8 at 1124.5 (4 at 920); y 0.0 at 923, 1.6 at 629 (0.8 at 776).
- Legend boxes were painted white on page copies in the work directory (main-4_fig3_legendmasked.png, main-6_fig9/10/11/12_legendmasked.png) so legend markers were not picked up; the archives reference these copies. No data marker lies inside a masked box.
- `check` passed for Fig. 3 Z correction (0.264 at the plotted end point), Fig. 9 both curves (0.62, 0.47 at 7.5 MPa), Fig. 10 all three (0.35, 0.2, 0.1 at the end points; GNF with 10% tolerance because 0.1 is printed to one decimal), Fig. 11 final (4 wt% at the maximum). Fig. 3 without Z, Fig. 11 original and the Fig. 12 series have no exact stated value to check against (status unchecked).

## Values seen but not extracted
- Abstract and Conclusions: LaNi5 1.38-1.41 wt% and 1.43-1.90 wt% (metal hydride calibration standard, not a carbon sorbent).
- Introduction (pp. 714-715): literature values cited from other papers (Dillon: soot containing 0.1-0.2 wt% SWCNTs measured at 133 K, 5-10 wt% inferred for pure SWCNTs, 6.5 wt%; DOE 6 and 9 wt%; Ye 8 wt%; Cheng 2.5-6.3 wt%; Blackman 0.22-8.0, 0.27-65, 0.057-0.9 wt%; Orimo 5 wt%; Ritschel below 0.18 wt% and 0.63 wt%): not measurements of this paper.
- Table 1 (densities of Fe, Cu, Al, Fe3O4 by He) and Table 2 (BWR parameters): not H2 uptake.
- Fig. 4: helium adsorption of the sample cell and hydrogen adsorption of the sample cell (empty cell, not a sorbent); hydrogen adsorption of MCNTs in grams (absolute mass, same measurement as the Fig. 3 Z-correction curve; recorded in the notes of M2, not digitized separately). Text: cell 0.36 mg at 7.5 MPa (cell); 0.80 mg total for 0.302 g MWCNTs (same point as M2, noted there); "error of 20%" (not an uptake).
- Fig. 5 and text: sample cell and stainless steel powder (2.672 g) plus cell at 77 K (not carbon); cell volume 5.383 ml at 77 K.
- Figs. 6, 7, 8 and pp. 717-718 text: LaNi5 loads 0.070-2.005 g, theoretical 1.38-1.50 wt%, errors 38% (0.52 wt%), 11% (0.15 wt%), 1.5% (0.02 wt%), Blackman LaNi5 1.46, 1.65, 1.55 and 0.09 wt%, estimated 0.09 wt% cell effect at 10 MPa (metal hydride or literature; not carbon).
- Fig. 9 'adsorption of sample cell' and Fig. 11 'sample cell' series (empty-cell adsorption expressed in wt%, not a sorbent).
- Fig. 12 GNFs lowest-pressure point (-0.0109 wt%, negative, see above).
- Fig. 1 (SEM images) and Fig. 2 (schematic): no values.
