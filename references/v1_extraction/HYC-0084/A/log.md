# HYC-0084 extraction log (agent A)

Rows written: 36 (M1-M34 sample S1 = AC4, M35-M36 sample S2 = Maxsorb-3). Instruction file read in full before starting.

## Extracted from

- Abstract (article p.1): AC4 6.8 wt.% at 4 MPa -> M30 (text_direct); 2.86 wt.% at 1 bar -> M22 (merged with Fig 3a last marker). Abstract SBET 3508 conflicts with Table 1 and text (3503); the Table 1 value is used.
- Sec 2.3.2 (article p.3): H2 instruments (ASAP 2020 HD88 Micromeritics for up to 1 bar; HPVA-100 VTI/TA Instruments, called a "gravimetric analyzer", for up to 8 MPa), degassing 350 C 24 h primary vacuum, repeatability "errors lower than 3% on each measurement". Used for coding, no values.
- Table 1 (article p.3): AC4 characterization (SBET 3503, V0.99 1.68, VDR 1.10, Vmeso 0.58, L0 1.22) on every S1 row.
- Sec 3.2 text (article p.4-5): 6.7 wt.% at 4 MPa -> M29; 2.86 wt.% at 1 bar -> M22.
- Sec 3.3 text (article p.5): lab-made AC 6.8 and 2.86 wt.% (M30, M22); Maxsorb-3 "only" 5.8 wt.% at 4 MPa and 2.1 wt.% at 1 bar -> M36, M35; Maxsorb-3 3203 m2/g as its area.
- Table 2 (article p.6), row Oil palm shell, This work: 6.7 (77 K, 40 bar) -> M29; 2.86 (77 K, 1 bar) -> M22; 3503 m2/g.
- Conclusions (article p.6): 6.7 wt.% at 4 MPa and 2.86 wt.% at 1 bar (same values as above).
- Figure 3a (article p.5, page image main-6): 22 markers digitized, M1-M21 plus the last marker merged into M22. Archive HYC-0084_fig3a_AC4_77K_lowP.json. Calibration: x 0.0 -> 338.34 px, 1.0 -> 556.54 px, verify 0.4 at 425.48 px predicts 0.3994 (0.16%); y 0.0 -> 623.32 px, 3.0 -> 456.13 px, verify 1.5 at 539.79 px predicts 1.4988 (0.08%). Tick positions are sub-pixel centroids of the tick marks. Colour 000000, tolerance 100, open-px 2, ROI x 320-576 y 446-634. 22 markers extracted = 22 counted. Tool check at 0.995 bar vs stated 2.86: 2.8584, 0.05%, pass. Same 22 markers also found at tolerance 140 and 170 (values differ by under 0.01 wt.%).
- Figure 3b (article p.5, page image main-6): archive HYC-0084_fig3b_AC4_77K_highP.json. Calibration: x 0 -> 729.65 px, 8 -> 938.97 px, verify 4 at 835.0 px predicts 4.026 (0.66%); y -1 -> 637.47 px, 7 -> 453.73 px, verify 3 at 545.67 px predicts 2.997 (0.10%). Colour 000000, tolerance 100, open-px 2, ROI x 706-964 y 445-635. The tool returned 12 points; I count 15 markers on the plot (see below). Tool check at 4 MPa vs stated 6.7: 6.784, 1.26%, pass. Rows: tool points 2-7 and 9-12 are M23-M28 and M31-M34; tool point 8 (3.969 MPa, 6.783 wt.%) is merged into M29 and M30 (printed 4 MPa within 2% of it; the neighbouring marker at 4.18 MPa is 4.5% away and does not qualify).

## Markers not separated or not stored in Figure 3b

- Three blobs of overlapping markers, near 0.68 MPa (19 px), 1.34 MPa (18 px) and 2.69 MPa (25 px), have 1.4 to 2 times the pixel area of a single marker (single markers 9-16 px). I count two markers in each, so the plot has 15 markers, but the tool cannot separate them and returns one centroid each (M26, M27, M28, confidence 2). The three hidden markers are not stored. isotherm_point_count = 15 counts them.
- The origin marker (0 MPa, about 0 wt.%) was returned at x = -0.0057 MPa and flagged by the tool as outside the calibrated axis range ("extrapolation, not a reading"). A row with negative or zero pressure fails validation (pressure must exceed 0), so no row is written for it. It is counted in isotherm_point_count = 15. The Figure 3a origin marker (0.0007 bar, 0.0057 wt.%) is in range and is stored as M1.

## Seen but not extracted

- OPC (oil palm shell charcoal, also called BC in Sec 3.2), AC2, AC3, AC6: characterization in Table 1 but no H2 uptake value (Sec 3.2: only AC4 was taken for H2 analysis; Figure 3 shows one curve per panel). Table 1: OPC SBET 198, V0.99 0.91. AC2 (W=2, 800 C) SBET 1600, V0.99 0.70, VDR 0.63, EA 25.98, L0 0.74, VDR/V0.99 0.90, Vmeso 0.07. AC3 (W=3) 3201, 1.51, 1.01, 20.01, 1.25, 0.67, 0.50. AC6 (W=6) 3183, 1.71, 1.03, 19.05, 1.41, 0.60, 0.64. No rows, and no sample ids.
- Sec 3.3 literature values for Maxsorb-3 from other papers: about 6 wt.% at 77 K and 5 MPa, 5 wt.% at 2 MPa (ref 16, Anson 2007); about 3 wt.% at 80 K and 10 MPa (ref 17, Khalil 2013). Not measured in this work.
- Table 2 literature rows, quoted from other papers for other materials and not measured here: Bamboo 3208 m2/g, 6.60 wt.% (77 K, 40 bar) and 2.74 wt.% (77 K, 1 bar), ref 1; Carbon precursor 2386 m2/g, 2.94 wt.% (77 K, 1 bar), ref 20; Chitosan 3100, 5.6 (77 K, 40 bar), ref 21; Corncob 3708, 5.8 (77 K, 40 bar), ref 22; Anthracites 3220, 6.6 (77 K, 40 bar), ref 23; Carbon aerogels 1980, 4.3 (77 K, 20 bar), ref 24; Bark 3170, 4.08 (77 K, 10 bar), ref 21. Ref 1 (Zhao 2017) is by the same group but is a different material. The "published before" rule is read as applying to this paper's own samples.
- Figure 1 (N2 adsorption-desorption isotherms at 77 K, four samples), Figure 2 and Figure 4 (DFT pore size distributions): not H2 uptake, not digitized. Figure 4 includes Maxsorb-3 (labelled Mawsorb-3 in the caption).
- Introduction: H2 density 90 g m-3 at 1 bar and 273 K, DOE target 5.5 wt.%: not uptake measurements.

## Coding decisions to check

- Maxsorb-3 rows (M35, M36): Sec 2.1 says it "was used for the sake of comparison" and the 5.8 and 2.1 wt.% values carry no citation, but the text never says they were measured here. Included with confidence 3. If the reconciler decides they are literature values, drop both rows. Instrument, degassing and the 3% error statement are not attributed to Maxsorb-3 (instrument_identified false, replicates_reported false, degassing empty). Its two values are one isotherm I3 (no plotted curve; the paper does not say they are different runs).
- 6.7 versus 6.8 wt.% at 4 MPa: the paper prints both for the same point (6.7 in Table 2, Sec 3.2, Conclusions; 6.8 in Abstract, Sec 3.3). Both stored (M29, M30), each merged with the same plotted marker (digitized 6.783). No separate digitized row for that marker.
- Sample label: Table 2 (the only table with uptake) lists the sample under the feedstock column as "Oil palm shell"; Table 1 and the text name it AC4. Label AC4 used because the Table 2 cell is a feedstock category, not a sample name.
- Sample numbering: S1 = AC4 (its data appear in the Abstract before Maxsorb-3 is described), S2 = Maxsorb-3. Samples with no rows are not numbered.
- measurement_method: ASAP 2020 HD88 (Fig 3a, I1) is named by manufacturer and model only, so `unknown` and basis_inferred `unknown`. HPVA-100 (Fig 3b, I2) is called a gravimetric analyzer by the paper: `gravimetric_microbalance`, no buoyancy correction stated, basis_inferred `unknown`. No basis named anywhere: uptake_type `unspecified`, basis_stated false.
- Branches: Figure 3 does not mark desorption points; Sec 3.2 says there was no hysteresis cycle. All points coded adsorption. The overlapping pairs in Figure 3b might be adsorption and desorption points; the paper does not say so.
- measuring_lab_id: the asterisk (corresponding author) is on M Fan, whose first affiliation is Fujian Agriculture and Forestry University; the printed corresponding email is weigang-zhao@fafu.edu.cn (first author W Zhao). Fan used because the asterisk is the stated mark; only the surname would differ.
- Pore-diameter method for L0 not named in the paper (L0 and EA tabulated beside V_DR): `unspecified`. VDR coded method DR, probe N2.
- Total pore volume V0.99 taken as total_pore_volume; Vmeso 0.58 equals V0.99 - VDR.
- Sec 2.3.2 error statement ("errors lower than 3% on each measurement") coded replicates_reported true for AC4; uncertainty_wt_pct left empty because it is a relative percentage.
- Figure 3 y-axis label reads "Hydrogen storage capacaties (wt. % at 77 K)" (spelling as printed).
