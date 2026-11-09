# HYC-0064 extraction log (agent B)

Paper: Cheng et al. 2025, Int J Coal Sci Technol 12:84, doi 10.1007/s40789-025-00811-3. Input: main-01..12.png only (no SI pages). 10 rows written.

## Sources extracted from

- main p5 Table 4 (pore parameters and H2 uptake, different activators): ZD-AC 0.04, ZD-H-AC 0.18, ZD-HK-AC 0.91, ZD-HNa-AC 0.38 wt%, no pressure printed; characterization (S_lang, S_BET, S_mic, V_total, V_meso, V_mic, dp) copied to every row of each sample. Rows M1, M5, M6, M7.
- main p5 Table 5 (different alkali-carbon ratios): ZD-HK1-AC 0.56, ZD-HK2-AC 0.77, ZD-HK3-AC 0.91, ZD-HK4-AC 0.64 wt%, no pressure printed. Rows M1 (HK3 = ZD-HK-AC), M8, M9, M10.
- main p1 abstract and p10 Table 7 ("ZD Coal | 303 K 80 bar | 0.91 | 1980 | This work"): give 80 bar and 303 K for the 0.91 wt% value (M1), and are the only numeric temperature in the paper.
- main p6 Section 3.2 text: "ZD-HK-AC ... reaches 1.26 wt% at 80 bar" (Fig. 4a). Row M2 (conflicts with Table 4/5 and the plotted curve; value_kind unclear).
- main p6 Fig. 4a (4 isotherms, 303 K, absolute pressure): highest-pressure marker of each digitized and merged with the Table 4 value of the same sample.
- main p6 Fig. 4b (4 isotherms): highest-pressure marker of each digitized and merged with the Table 5 value; the ZD-HK3-AC curve is the same isotherm as Fig. 4a ZD-HK-AC.
- main p9 Fig. 8 (ZD-HK3-AC, 5 adsorption-desorption cycles): highest-pressure markers of the two separable cycle ends digitized (rows M3, M4).
- main p3 Sections 2.2-2.4: preparation, characterization (N2 at 77 K, Micromeritics ASAP-2460, BET, t-plot, V_total at P/P0 = 0.99, DFT slit PSD) and H2 method (H-Sorb 2600T, degas 200 °C 240 min under vacuum, volume calibration). Corresponding author Xingxing Cheng, affiliation 1 Shandong University.

## Decisions

- ZD-HK-AC (Table 4, Fig. 4a) and ZD-HK3-AC (Table 5, abstract, Fig. 4b, Fig. 8 text, conclusions) treated as one sample, labelled ZD-HK-AC (first table reporting its uptake): all eight Table 4/5 numbers are identical, and the Fig. 4a ZD-HK-AC and Fig. 4b ZD-HK3-AC markers agree within 0.003 wt% at all 11 points. Their last two markers differ by about 1 bar in pressure between the panels (4a: 71.12 and 78.45 bar; 4b: 72.11 and 79.38 bar). Treated as one isotherm (I1) plotted twice, not two runs; both series archived.
- Temperature 303 K applied to all rows: Table 7 gives "303 K 80 bar" as this work's adsorption condition. The text otherwise says only "room temperature". If the reconciler holds that 303 K applies only to the 0.91 wt% value, the other rows would need temperature_unstated = true.
- Table 4/5 values have no printed pressure. Each equals the highest-pressure marker of that sample's Fig. 4 curve within digitization error, and the paper says testing was confined to 80 bar maximum. So each was merged with that marker, using the digitized pressure ("pressure digitized"). For M1 the printed 80 bar (abstract, Table 7) is within 2% of the Fig. 4a marker (78.45 bar, a 1.55 bar difference) and of the Fig. 4b marker (79.38 bar).
- The 1.26 wt% at 80 bar (p6 text) contradicts 0.91 wt% (Tables 4/5, abstract, Table 7, conclusions) and the plotted curve. It is recorded as printed in its own row, with isotherm_id I1 because the sentence attributes it to Fig. 4a, and value_kind = unclear.
- Fig. 8 was digitized at its highest-pressure points only, because it is not at 77 K. Its five cycles share one style (black adsorption squares, red desorption circles) and overlap. Cycles cannot be numbered, marker counts per cycle cannot be determined, and only two adsorption end markers are separable: a single square at 82.37 bar / 0.7191 wt%, and a merged group at 81.02 bar / 0.7427 wt% (68 px against about 49 px for one square). The merged group holds the end markers of at least two cycles and is recorded once. The end points of the remaining cycles (at least two, probably three) could not be separated and were not extracted. Fig. 8 reaches only about 0.72-0.74 wt% near 81-82 bar, against 0.91 wt% at 80 bar for the same sample in Fig. 4/Table 4. The paper does not explain this.
- Sample S1 has replicates_reported = true because Fig. 8 shows repeated isotherms of it. All other samples have it false.
- ZD-AC and ZD-H-AC are coded material_class = other: the paper calls them unactivated (directly carbonized coal), although it names them "-AC" and groups them with the "activated carbon samples". synthesis_method = carbonization. KOH/NaOH samples are chemical_activation and activated_carbon.
- instrument_identified = false (model "H-Sorb 2600T" without a manufacturer). calibration_described = false: "calibrate the volume" and "sample volume calibration" are stated without the method or gas.
- No sample in the paper is commercial, doped or metal-loaded.

## Digitization

- Fig. 4a: frame x 181-593, y 1058-1391 px on main-06.png. x ticks 0 at 181.47, 40 at 374.91 (check), 80 at 568.5. y ticks 0.0 at 1374.75, 0.4 at 1254.49 (check), 1.0 at 1073.83. Residuals 0.04% (x) and 0.09% (y).
- Fig. 4b: x ticks 0 at 707.56, 40 at 897.41 (check), 80 at 1086.48. y ticks 0.0 at 1389.05, 0.4 at 1263.11 (check), 1.0 at 1073.56. Residuals below 0.3%.
- Fig. 8 (main-09.png): x ticks 0 at 197.45, 40 at 373.60 (check), 80 at 549.57. y ticks 0.0 at 461.45 (on the bottom frame line), 0.4 at 318.77 (check), 0.8 at 177.27. Residuals below 0.5%.
- Tick centres were found as intensity-weighted pixel rows and columns. The legends (Fig. 4a, 4b, 8) and the in-plot caption of Fig. 8 were whited out on copies of the page images (work/main-06_legend_masked.png and work/main-09_legend_masked.png). Pixel geometry is unchanged, and the archives point to these copies.
- Marker counts (counted on the plot / extracted):
  - Fig. 4a: ZD-AC 11/10 (the 3.4 bar square is hidden under the ZD-H-AC and ZD-HNa-AC markers; only a sliver is visible, and runs with smaller opening and minimum size picked up line fragments and an off-centre sliver, so the default run was kept). ZD-H-AC 11/11. ZD-HNa-AC 11/11 (rerun with --marker-min-px 22 to drop line fragments). ZD-HK-AC 11/11.
  - Fig. 4b: ZD-HK1-AC 12/11 (the 3.3 bar square is hidden; the 8 bar square is partly hidden and was found as a 9 px fragment, so its centroid is biased). ZD-HK2-AC 12/11 (the 3.3 bar circle is hidden under the HK3/HK4 markers). ZD-HK3-AC 11/11. ZD-HK4-AC 12/12.
  - Fig. 8: not countable. 29 black and 20 red marker groups were extracted, many of them merged overlaps of several cycles. Unseparated markers are as described above.
- The digitize_figure.py check at 80 bar against the table values passed for ZD-H-AC, ZD-HNa-AC, ZD-HK1-AC, ZD-HK2-AC and ZD-HK4-AC. It could not run for ZD-AC (78.04), ZD-HK-AC (78.45) or ZD-HK3-AC (79.38), whose last markers lie below 80 bar, or for Fig. 8, which has no stated value. Those archives stay "unchecked".
- Only the highest-pressure point of each curve is used in rows, because all isotherms are at 303 K. The other markers are in the archives only.

## Values seen and not extracted

- Table 1 (p2, raw ZD coal, proximate wt% air-dried): M 11.85, V 32.35, A 8.17, FC 52.92. Elemental: C 60.36, H 5.45, O 16.91, N 1.16, S 0.96. Text gives Vad 32.25%, which conflicts with Table 1's 32.35. Raw coal precursor with no H2 uptake.
- Table 2 (p2, ash composition wt%): SiO2 10.32, Al2O3 9.51, Fe2O3 6.19, TiO2 0.56, CaO 39.45, MgO 10.68, K2O 0.62, Na2O 9.88, SO3 5.42. Precursor ash, no H2 uptake.
- Table 3 (p4, XRF wt%, Ca/Fe/Na/Mg/Al/Si). Raw coal 60.5/4.6/5.0/6.0/4.1/2.4. Acid pretreatment 24.2/2.6/3.3/3.0/3.6/2.0. Carbonization 19.2/3.1/2.6/3.5/3.1/1.9. Acid post-treatment 10.2/2.7/2.1/2.9/2.6/1.8. Removal rates in the text: Ca 60% after pretreatment, Si 43%, Ca 83.1% and Si 25% after post-treatment. These are intermediate stages with no H2 uptake. The figures are normalized relative contents, not usable as residual_metal_wt_pct.
- Fig. 1 (TGA of raw coal; 80% weight loss in stage 2, 300-550 °C): not H2.
- Fig. 2 (N2 isotherms; ZD-HK-AC reaches about 650 cm³/g STP, p4 text): not H2.
- Fig. 3 (DFT PSD): text p4 says ZD-HK-AC micropores lie mainly at 0.5-0.9 nm and mesopores at 1.0-2.5 nm. Not a schema field.
- Text p4: "specific surface areas of ... ZD-AC and ZD-H-AC, are 52 m²/g and 452 m²/g". These equal S_lang in Table 4, not S_BET (47, 392); the rows carry the Table 4 values in their respective fields.
- Figs. 5-7 (SEM, EDX, mechanism scheme): no numbers.
- Fig. 9 (p9, H2 storage wt% against S_lang, S_BET, S_mic and V_mic with linear fits): no axis scales are printed, so no values are recoverable. Each panel shows roughly 30 or more points from "all the prepared activated carbon samples", more samples than the 7 in Tables 4/5, and their uptakes are not reported elsewhere.
- Table 6 (p10, regression statistics): RSS S_lang 1.122, S_BET 0.737, S_min 0.743, V_min 0.596. COD 0.612, 0.801, 0.797, 0.857. Fig. 9 insets print the same to more digits. Not uptake values.
- Table 7 (p10) and Fig. 10 (p11), literature comparison measured in other works, not extracted (not measurements of this paper's samples):
  - Tangerine peel 298 K 30 bar 0.60 wt%, 1230 m²/g (Doğan 2020)
  - Wood chips 298 K 80 bar 0.50, 2835 (Pedicini 2020)
  - Palimera sprout 298 K 15 bar 1.06, 2090 (Samantaray 2019)
  - Rice straw 298 K 100 bar 0.65, 2197 (Schaefer 2017)
  - Jute fiber 303 K 40 bar 1.20, 1224 (Ramesh 2017)
  - Rice husk 298 K 100 bar 0.57, 1247 (Toda 2013)
  - Rice husk 303 K 270 bar 1.00, 2537 (Minoda 2013)
  - Coffee bean 298 K 120 bar 0.60, 2070 (Akasaka 2011)
  - Corncob 298 K 50 bar 0.44, 3012 (Sun and Webley 2010)
  - Litchi wood 303 K 57 bar 0.41, 2313 (Huang 2010)
  - Coconut-shell 298 K 100 bar 0.85, 2800 (Jin 2007)
  - The "ZD Coal ... This work" row and the Fig. 10 "This work" point are the M1 value.
- Text p10, literature: Samantaray palm-bud AC, about 2090 m²/g, 1.44 cm³/g, 1.06 wt% at 15 bar and 25 °C. Ramesh jute-fiber AC, 1224 m²/g, 1.2 wt% at 40 bar and 30 °C. Other works, not extracted.
- Text p1 (introduction): DOE light-vehicle system targets of 4.5% (2010) and 5.5% (2015), and the general statement that ordinary activated carbon hardly reaches 1 wt% at normal temperature. Not measurements.
- Text p7: Fig. 8 cycles "nearly identical", "no significant decrease". No numeric value.
- Fig. 4 and Fig. 8 markers other than the highest-pressure point of each curve: not extracted because the isotherms are not at 77 K. They are archived in digitizations/.
- No mean across samples or laboratories, and no non-carbon comparison material, is reported.
