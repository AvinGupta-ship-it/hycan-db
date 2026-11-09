# HYC-0047 extraction log (agent B, 2026-11-09)

Paper: Fierro et al. 2010, Carbon 48, 1902–1911. Input: page images main-01.png to main-10.png only (no SI). 160 rows written.

## Sources extracted from

- Table 1 (main-05.png, p. 1906): rho_He, S_BET, V0.99, V_DR,N2, L0, DR fit ranges and V_DR,CO2 of the nine ACs. Not uptake; attached to every uptake row of each sample (S_BET, V0.99 as total pore volume, V_DR,N2 as micropore volume (DR, N2), V_DR,CO2 in micropore_volume_co2_cm3_g, L0 as stoeckli_L0, rho_He as skeletal density; ranges and ± in notes).
- §2.2 (main-03/04.png, pp. 1903–1904): N2 77 K and CO2 273 K on Micromeritics ASAP 2020, outgassed 48 h at 523 K; BET on the adsorption branch, no P/P0 range and no consistency criteria stated (bet_range_stated = false).
- §2.3.1 (IJL), §2.3.2 (ICMPE), §2.3.3 (ICB) (main-04/05.png, pp. 1904–1905): instrument, calibration, degassing, H2 purity and sample-mass coding per laboratory (details in row notes).
- Table 2 (main-07.png, p. 1908): 32 values extracted: IJL 298 K 5 MPa (9), ICMPE 298 K 5 MPa (7), ICMPE 77 K 4 MPa (9), ICB 77 K 4 MPa (7). Every value printed with ± 0.1 (uncertainty_wt_pct 0.1).
- Fig. 5a (main-06.png, p. 1907): 77 K ICB gravimetric isotherms (I1 M1149, I2 M2029, I3 M2849, I4 T3220), both branches; 52 digitized rows plus 1 marker merged with a Table 2 value.
- Fig. 5b (main-06.png, p. 1907): 77 K ICMPE volumetric isotherms (I5 M1149, I6 M2029, I7 M2849, I8 T3220), both branches, 74 digitized rows; M2849 at 298 K (I9), highest-pressure marker only, 1 row.
- Conclusions, 2nd paragraph (main-09.png, p. 1909): "A maximum H2 excess uptake of 1.1 wt.% for ACs was found at 298 K and 20 MPa": 1 row (sample not identified, coded "(unlabelled 1) / IJL", HYC-0047-S10).

## Coding decisions

- Multi-laboratory paper: three independent laboratories (IJL, ICMPE, ICB, labels as printed in Table 2 and in the Fig. 6/7 captions) measured the same samples. Labels are "<sample> / <lab>", measuring_lab_id "<lab> (HYC-0047)". sample_id is per material across laboratories.
- Sample numbering (first appearance): S1 M1149, S2 M2029, S3 M2849, S4 T3220 (Fig. 1 legends, p. 1905, the first place labels appear), then S5 T1308, S6 T2275, S7 T2451, S8 T2502, S9 T3073 (Table 1 order), S10 (unlabelled 1).
- Basis: every value is called "excess" (Table 2 caption; text p. 1907 for Fig. 5) but excess is never defined. The "total H2 storage" of §3.2.1 (Fig. 4a, mol H2 per vessel) is a vessel quantity, not a second per-mass basis reported side by side. So basis_stated = false, basis_inferred = excess, uptake_type = excess, with the naming quote in basis_evidence.
- wt% convention: W1 / stated for Table 2 values (caption: "expressed as weight% of the outgassed activated carbons") and for ICMPE values (§2.3.2: "All capacities reported here refer to the sample dry mass (i.e. outgassed mass)"). unknown / none for the ICB isotherm points of Fig. 5a and for the 1.1 wt% text value, for which no statement applies.
- Fig. 5b 298 K curve: the caption says ICMPE volumetric device, but text p. 1907 says "measured at 298 K in the gravimetric device". Coded ICMPE volumetric because §2.3.2 lists ICMPE at 77 and 298 K up to 10 MPa, §2.3.3 lists the gravimetric device only at 77 K and up to 8 MPa, and the curve reaches 9.7 MPa. Flagged in notes.
- Table/figure merge (2% / 0.02 bar rule): Table 2 ICB M2029 4.9 at 4 MPa matches the Fig. 5a M2029 adsorption marker at 40.633 bar (4.8544 wt%). Recorded once as table_direct with isotherm_id I2, and the digitized point is in notes. No other Table 2 value lies within 2% of a plotted point. The nearest points are: 5a M1149 38.48 bar, M2849 38.48 bar, T3220 38.59 bar (adsorption) and 41.14 bar (desorption); 5b M1149 31.41/47.51 bar, M2029 29.93/46.65 bar, M2849 38.78 bar, T3220 38.65 bar (desorption); 298 K M2849 marker nearest 5 MPa at 51.6 bar (0.608 wt%). That last marker was digitized only for this check: work/check_fig5b_M2849_298K_marker_near_5MPa.json. These Table 2 rows carry no isotherm_id because the paper does not say they were taken from the curves.
- replicates_reported = true for all Table 2 rows (± 0.1) and for all Fig. 5 rows (each of the four samples was measured independently by two laboratories; M2849 at 298 K by IJL and ICMPE). It is false for the 1.1 wt% text value. ICMPE's statement that PCI curves were measured twice gives no repeat results.
- instrument_identified: IJL true (laboratory-made, described); ICMPE false (Sieverts device not named and not said to be home-built); ICB false (VTI Corporation, no model). calibration_described: ICMPE true (sample-volume correction by He pycnometry); ICB true (buoyancy correction); IJL false (free-volume determination not described).
- isotherm_point_count is the number of markers counted on the plot per run, both branches, excluding the origin markers (see below): I1 15, I2 13, I3 15, I4 10, I5 22, I6 17, I7 19, I8 17, I9 14 (small dash markers along the 298 K line). Markers fully hidden under other markers cannot be counted (see below).
- value_kind = measured for all rows: table values are "measured", Fig. 5 symbols are measured points, and the 1.1 wt% "maximum" has its pressure stated.

## Digitization (Fig. 5a and 5b, main-06.png)

- Calibration on page pixels. Fig. 5a: x 0 MPa at px 717, 10 MPa at px 1112, check 4 MPa at px 875 (0.0% error); y 0 wt% at px 762, 7 wt% at px 556, check 3 wt% at px 674 (0.32%). Fig. 5b: x 0 at 717, 10 at 1118, check 4 at 877 (0.25%); y 0 at 1056, 7 at 843, check 3 at 965 (0.31%). Tick positions were found from pixel rows and columns.
- All series are black, so each series and branch was isolated before running the tool. For each series a full-page image was written to work/img/ (same pixel coordinates; pixels < 128 grey set to the series colour, everything else white). It keeps only that series' markers. A filled marker is the dark pixels within 5 px of its centre and nearer to it than to any other marker (2 px margin to same-series neighbours). An open marker is its enclosed white interior dilated by 1 px, or the closed and filled ring when no interior was enclosed. Marker identification and series assignment were made from enlarged crops (work/z*.png, work/ov*.png). Then digitize_figure.py extract --mode markers ran per series (3-px opening; 2-px opening and 4-px minimum for the 298 K dash marker). Extracted counts equal placed counts for every archive, and every extracted centroid lies within 1.2 px of the identified marker centre. A residual search (work/residual.py) for dark blobs and enclosed interiors outside the extracted markers found only line segments: a 3 px-thick double-line band at Fig. 5a px 1005–1018/589, a 3×3 px line overlap at px 724/662, and gaps between the parallel M2849/T3220 lines (Fig. 5a) and M2029/T3220 lines (Fig. 5b px 727/952).
- Archives were not passed through the tool's legacy `check` step; calibration was verified with the third tick on each axis.
- extraction_confidence 3 for isolated markers, 2 for markers overlapping a neighbour (window truncated, possible bias up to ~1 px ≈ 0.025 MPa / 0.034 wt%) or with uncertain series assignment.

## Values seen but not extracted

- Origin markers at (0 MPa, 0 wt%) in Fig. 5a and Fig. 5b (filled squares where all lines start): plot origin, not a measured point; the Fig. 5a one digitizes to −0.017 wt%. Not counted in point counts.
- Fig. 5b M1149 filled square at ~0 MPa, ~1.58 wt% (px ~716, 1008): mostly hidden under an open square; its visible part gives P = −0.032 MPa, which is not a valid reading. Not extracted; counted in I5 (22).
- Markers that cannot be separated or are hidden. Fig. 5a: T3220 adsorption (filled circles) below 3.8 MPa is not visible; they may lie under T3220 open circles or M2849 diamonds. The filled shape at 0.12 MPa / 3.11 wt% was assigned to M2849, but a T3220 filled circle may coincide with it. One or more M2029 filled triangles between 0.14 and 0.63 MPa, and a possible filled marker under the T3220 open circle at 0.27 MPa (thickened lower outline), cannot be resolved. Fig. 5b: no T3220 filled circle below 1.22 MPa, no M2029 filled triangle below 0.54 MPa and no M2849 open diamond below 1.49 MPa can be separated in the near-axis tangle. Four partly hidden filled shapes were assigned to M2849 with confidence 2 (0.0265 MPa/1.94 wt%, 0.127/2.97, 0.511/4.29, 0.812/4.72).
- Table 2 "n.d.": ICMPE 298 K for T3073 and T3220; ICB 77 K for T2275 and T2502.
- Fig. 4a (p. 1907): total H2 stored in the IJL vessel (mol H2/vessel) for packed M1149 at 298 K up to 20 MPa, and the empty-vessel compression curve. This is a vessel total, not an uptake per sorbent mass (sample mass not given, vessel "close to 3 cm3"), so no field fits. Not digitized.
- Fig. 4b and Fig. 5c and text: % gain in H2 storage over compression (33.6% at 1.1 MPa M1149, 38.0% at 1.5 MPa M2029, 31.3% at 2.6 MPa M2849, 14% at 20 MPa M2029, ~3700% near 0.15 MPa, 1.3% near 9 MPa, negative for two ACs). Not uptake.
- Fig. 6a/6b (p. 1908): uptake at 77 K, 4 MPa against S_BET and V_DR,N2. Not isotherms; the points are the Table 2 values.
- Fig. 7 (p. 1909): uptake against S_BET from Xu et al. [41], Kabbour et al. [42], Panella et al. [25], Jordá-Beneyto et al. [27] (other papers' samples) plus this work's Table 2 values. Not extracted.
- 6.4 wt% "upper limit" (abstract, Fig. 6a, §3.2.2, Conclusions): extrapolated from the uptake–S_BET correlation across samples. Not a row.
- 6.8 wt% theoretical maximum (Schlapbach and Züttel); slopes 1.74e-3 to 2.87e-3 wt% g m-2 and plateau "from 5.4 [27] to 6 wt.%" (§3.2.2): theory and literature.
- Abstract "6.0 wt.% at 77 K and 4 MPa" (= Table 2 M2849 ICB) and "reduced to 0.6 wt.% at 298 K and 5 MPa"; Conclusions "decreased to 0.6 wt.%": restate Table 2 values, so no new row.
- §3.2.1 ranges "0.4 to 0.6 wt.%" at 298 K / 5 MPa (Table 2 also prints 0.3 for T1308 ICMPE) and "2.9 to 6.0 wt.%" at 77 K / 4 MPa; §3.2.2 "5.9–6.0 wt.%"; §3.2.3 "6 wt.%": summaries of Table 2.
- Conclusions "5.9–6.0 wt.% in ACs having S_BET = 2451 m2 g-1" (two laboratories): restates T2451 Table 2 values. Table 2 prints ICMPE 5.9 and ICB 5.8, so the text's 6.0 does not match. No new row.
- Introduction: AX-21 about 6 wt% at 77 K and 5 MPa and 5 wt% at 2 MPa [28], about 3 wt% at 80 K and 10 MPa [23], 1 wt% at room temperature and 5 MPa [28], 1.6 wt% at 70 MPa [29]; predicted limits 23.76 wt% [17], 11.7 wt% at 129 MPa [18], 3.5 wt% [19]; DOE targets 6.5 wt% and 62 kg m-3. Other works and targets, not measured here.
- Characterization without H2 uptake: Fig. 1 (N2 isotherms), Fig. 2 (CO2 isotherms), Fig. 3 (DFT pore-size distributions) of M1149, M2029, M2849, T3220. Their values are covered by Table 1. CO2 cross-check of one AC by Micromeritics-France, ICB-CSIC and Alicante: not H2. All nine samples have H2 values, so there is no characterization-only sample.
- No non-carbon material was measured.

## Observations for reconciliation

- Table 2 ICMPE M1149 (3.2 ± 0.1 at 4 MPa) sits above the Fig. 5b M1149 points near 4 MPa (2.97 wt% at 31.4 bar, 3.09 at 47.5 bar, 3.11 at 48.5 bar desorption). The other Table 2 77 K values agree with the plotted runs within about 0.1 wt%.
- Table 2 77 K values are at 4 MPa, while the ICB set points near 4 MPa digitize at 3.85 MPa (M1149, M2849) and 4.06 MPa (M2029).
