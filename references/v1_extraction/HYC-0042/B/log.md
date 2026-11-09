# HYC-0042 extraction log (agent B)

Molefe et al., 2019, Frontiers in Chemistry, 10.3389/fchem.2019.00864. Input: page images main-01.png to main-10.png (no supplementary file). 47 rows written.

## Sources extracted

- Table 1 (main-07.png, p. 7), column "Measured H2 uptake (wt. %)" (footnote e: 77 K and 1 bar): Pristine ZTC 2.38 (M19, merged with the last Figure 6 ZTC marker), PIM-1/80 wt% ZTC 1.87 (M31), PIM-1/UiO-66(Zr)/ZTC (80 wt%) 1.65 (M44). Columns "Measured BET SSA" (footnote a, N2 at 77 K), "Micropore area" (footnote c, t-plot) and "Total pore vol." (footnote d, H-K analysis at p/p ~0.99) carried on every row of these three samples.
- Figure 6 (main-07.png, p. 7), H2 adsorption isotherms at 77 K, 0-1000 mbar, adsorption branch only: series ZTC (I1, M1-M19), PIM-1/80 wt% ZTC (I2, M20-M30), PIM-1/UiO-66(Zr)/ZTC (80 wt%) (I3, M32-M43) digitized; archives in digitizations/.
- Table 2 (main-07.png, p. 7): row PIM-1/AX21 (60 wt%), 1.90 wt% at 77 K and 1 bar, BET 2,075, cited to Tian et al., 2019 (M47, previously reported). The "This work" rows for PIM-1/80 wt% ZTC (1.87; 2,433) and PIM-1/UiO-66(Zr)/ZTC (80 wt%) (1.65; 1,767) repeat Table 1 and are the same measurements (no separate rows; named in source_location).
- Introduction (main-02.png, p. 2, left column): "up to 8.9 wt. % at 77 K and 30 bar on activated carbons (Blankenship et al., 2017)" (M45) and "carbons such as CA-4700 have 3.9 wt % at 77 K and 1 bar (Blankenship et al., 2017)" (M46), extracted under the "values reported before" rule with `previously reported` notes. They are literature values, not measurements of this work; C should confirm whether quoted literature values belong in the dataset.
- Sample Characterization (main-04.png, p. 4): instrument (Micrometrics ASAP 2020 HD, 77 K, H2 up to 1 bar), BET from N2 isotherms, degassing (vacuum down to 10^-7 bar, 200 C, at least 8 h). Chemicals (p. 3): H2 and N2 "ultra-high purity grade" (no number, h2_purity_pct left empty).
- Experimental Procedure (pp. 3-4): ZTC synthesis (furfuryl alcohol / zeolite 13X, ethylene CVD at 700 C, carbonization 900 C, HF/HCl template removal) and composite preparation (TCE solvent impregnation; fillers degassed 200 C 4 h before mixing; ternary heated at 150 C).
- FTIR discussion (pp. 5-6): functional groups recorded for ZTC, PIM-1/80 wt% ZTC and the ternary composite.
- Corresponding author: Nicholas M. Musyoka (marked *), first affiliation HySA Infrastructure Centre of Competence, Energy Centre, Council for Scientific and Industrial Research (CSIR), Pretoria; no university in that affiliation, so measuring_lab_id = "Musyoka group, Council for Scientific and Industrial Research (CSIR)".

## Scope decisions

- PIM-1/80 wt% ZTC: 80 wt% ZTC + 20 wt% PIM-1, majority carbon; extracted as composite.
- PIM-1/UiO-66(Zr)/ZTC (80 wt%): 40 wt% ZTC + 40 wt% UiO-66(Zr) + 20 wt% PIM-1. No phase exceeds 50 wt%, but the paper calls it a "ZTC-based composite" and carbon is the majority element by mass; extracted as composite with metal_element Zr. C should confirm it is a carbon sorbent under section 3.
- measurement_method volumetric_sieverts is inferred from the named instrument (ASAP 2020 HD); the text does not name the method. basis_inferred = excess follows from it.

## Figure 6 digitization

- Calibration (all three series): x on labelled ticks 0 mbar (px 175.9) and 1000 mbar (px 561.25), verified at 600 mbar (px 407.08, residual 0.013%); y on 0,0 wt% (px 920.3) and 2,8 wt% (px 609.93), verified at 1,2 wt% (px 787.2, residual 0.063%). Tick pixels are intensity-weighted centroids of the tick-mark runs (x ticks on row 925, y ticks on columns 170-171). Labels use decimal commas. Pressures digitized in mbar and divided by 1000.
- ZTC (dark green left triangles): colour #008000, tolerance 40, ROI 177 640 563 919 (excludes the legend marker at y about 623), open-px 2, marker-min-px 4. 19 markers extracted = 19 counted. Marker 1 overlaps the PIM-1 square; marker 19 sits on the right axis frame and is half clipped (centroid from its visible part, 0.998 bar, 2.3754 wt%). Check against Table 1 (2.38 at 998.05 mbar): 0.20%, pass.
- PIM-1/80 wt% ZTC (bright green diamonds): colour #00ff00, tolerance 40, ROI 177 680 563 919 (excludes legend), open-px 2, marker-min-px 4. 11 markers extracted = 11 visible markers. The line continues past the last visible marker (974.7 mbar, 1.8611 wt%) to the 1000 mbar frame, so at least one further point of the run is clipped from view. The Table 1 value (1.87 at 1 bar) is outside 0.02 bar of any visible marker, so it is a separate table row carrying I2 (the p. 7 text says the Figure 6 curves show 1.87, 1.65 and 1.22 wt%). The tool check cannot run (1000 mbar is outside the digitized range); linear extrapolation of the last two markers to 1000 mbar gives 1.877, consistent with 1.87. isotherm_point_count = 12 (11 visible + the 1-bar point).
- PIM-1/UiO-66(Zr)/ZTC (80 wt%) (magenta down triangles): colour #ff00ff, tolerance 60, ROI 177 690 563 919 (excludes legend), open-px 2, marker-min-px 4. 13 pixel groups for 12 visible markers. Markers 1 and 2 are partly hidden by the ZTC and PIM-1/80 wt% UiO-66(Zr) markers (centroids from visible magenta pixels, confidence 2). Marker 3 is split by the crossing ZTC line into groups 3 and 4 and could not be joined by any tolerance (40-90) or opening (1-3) setting; its row uses the pixel-count-weighted mean of the two group centroids (107.056 mbar, 0.6835 wt%). As for I2, the line runs past the last visible marker (934.2 mbar, 1.6269 wt%) to the frame; Table 1 1.65 at 1 bar is a separate row carrying I3; extrapolation to 1000 mbar gives 1.659. isotherm_point_count = 13 (12 visible + the 1-bar point).
- Archives HYC-0042_fig6_PIM1-80ZTC.json and HYC-0042_fig6_PIM1-UiO66-ZTC.json keep status "unchecked" because the only stated values (at 1 bar) lie outside their digitized ranges.

## Values seen but not extracted

- Table 1, Pristine UiO-66(Zr): 1.36 wt% (77 K, 1 bar); BET 1,903, micropore area 1,882, pore volume 0.75. MOF, not a carbon sorbent.
- Table 1, PIM-1/80 wt% UiO-66(Zr): 1.22 wt% (77 K, 1 bar; also Table 2, p. 7 text, abstract); BET 1,054, estimated BET 1,679, micropore area 1,014, pore volume 0.48, estimated H2 1.29. 80 wt% MOF + 20 wt% polymer, not a carbon sorbent.
- Table 1, Pristine PIM-1: 1.02 wt% (77 K, 1 bar); BET 785, micropore area 707, pore volume 0.54. Uncarbonized polymer, not a carbon sorbent.
- Table 1, "Estimated BET SSA" (2,722 PIM-1/80 wt% ZTC; 2,200 ternary) and "Estimated H2 uptake" (2.11 PIM-1/80 wt% ZTC; 1.70 ternary): computed as mass-weighted sums of measurements of several samples (footnotes b, f); not rows. Repeated in p. 7 text.
- Figure 6 series UiO-66(Zr) (red circles), PIM-1/80 wt% UiO-66(Zr) (blue triangles), PIM-1 (black squares): not carbon sorbents; not digitized.
- Figure 5 (p. 6): N2 isotherms at 77 K, not H2; not digitized. Figures 1-4 (PXRD, TGA, FTIR, SEM): no H2 values.
- Table 2 literature rows that are not carbon sorbents: PIM-1/MIL-101(Cr) (80 wt%)-Monoliths 1.73 wt%, BET 2,333 (Molefe et al., 2019); PIM-1/MIL-101 (40 wt%)-Films 1.11 wt%, BET 1,580 (Tian et al., 2019); PIM-1/PAF-1 (37.5 wt%) 1.15 wt%, BET 1,639 (Rochat et al., 2017).
- Introduction p. 2: "maximum total of 10 wt. % on NOTT-112 MOFs ... at 77 K and 77 bar (Yan et al., 2009)" and "MOFs ... around 2.5 wt. % (Rowsell and Yaghi, 2006)": MOFs, not carbon. p. 1: "type IV cylinder ... >=5 wt. % of H2 at 700 bar (Hua et al., 2017)": compressed-gas tank, not a sorbent. p. 2 DOE targets 4.5 wt.% and 0.030 kg H2/L, p. 8 ">4.5 wt. %": targets, not measurements.
- Abstract p. 1: surface area 1,054-2,433 m2/g and uptake 1.22-1.87 wt% at 1 bar and 77 K: range endpoints are Table 1 values already covered (1.87) or out of scope (1.22).
- p. 6 text "785 to 1,767 ... and to 2,433 m2g-1" and p. 8 conclusion "1,767-2,433" and "1,054": repeat Table 1 areas.
- p. 7 text "slight decrease (<=11% loss)", "over 80% of the estimated surface areas", "62.8%"; p. 8 "negligible loss of < 12%": derived ratios, not uptake values.
- p. 7 text: "best H2 storage properties at both 0.1 and 10 MPa adsorption measurements" (Tian et al., 2019): no value printed.
