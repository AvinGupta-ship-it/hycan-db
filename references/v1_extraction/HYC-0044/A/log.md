# HYC-0044 extraction log (extractor A)

Paper: Hwang et al. 2021, Nanomaterials 11, 1830. Output: 113 rows, 9 isotherms (I1-I9), 0 validator errors (`--errors-only`).

## Extracted from

- Table 2 (main text p6), own-sample rows: S1 PCF_H 0.3 (2.87 wt%), S2 CF (0.07), S3 APCF_H 0.3 (5.14), S4 ACF (1.35), S6 Pd 0.5/APCF_H 0.3 (5.45), all at 10 MPa = 100 bar. Each is merged with the plotted ~10 MPa point of its Fig 4c series into one `table_direct` row (M9, M23, M38, M52, M66), conf 5.
- Table 3 (main text p9), Pd loading vs uptake at 10 MPa: S3 Pd 0 mM = 5.14, S5 Pd 0.1 mM = 5.30, S6 Pd 0.5 mM = 5.45, S7 Pd 1 mM = 5.17. Merged with the ~10 MPa point of each Fig S3b series (M75, M84, M97, M113), conf 5. S3 Pd 0 mM repeats the Table 2 value for APCF_H 0.3.
- Table S1 (SI p1): Pd at% by EDX, put in sample notes only. No H2 values.
- Table 1 (main text p5): BET, Vp, Vmicro for the samples used in S1-S7 (sample descriptors only).
- Fig 4c (main text p7, page image, 77 K, 0-10 MPa, wt%): 5 series digitized, filled markers only.
  - CF (I1, S2): 9 plateau points, 2.0-9.98 MPa (low-pressure points not separable, see below).
  - ACF (I2, S4): 14 points.
  - PCF_H 0.3 (I3, S1): 15 points.
  - APCF_H 0.3 (I4, S3): 14 points.
  - Pd 0.5/APCF_H 0.3 (I5, S6): 14 points.
- Fig S3b (SI p4, page image), Pd-loading series:
  - Main panel: Pd 0.5 mM (I8, S6) 13 points; Pd 1 mM (I9, S7) 16 points including the origin (0.126 bar, 0.0024 wt%).
  - Inset: Pd 0 mM (I6, S3) 9 points; Pd 0.1 mM (I7, S5) 9 points. Inset used because these two series are hidden under others in the main panel at p < 2 MPa.
- Abstract and Sec. 3.2/3.3 text: repeat of the same Table 2/3 values (5.14, 5.45, 2.87, 1.35, 0.07, 5.30, 5.17). Same measurements, no extra rows.
- Axis calibrations (pixel-level, from frame and tick pixels, with one verify tick each):
  - Fig 4c (page7_clean_4c.png): x 0@229.55 px, 10@600.55 px; y 0@1091.2, 6@823.0; verify x 6, y 4.
  - Fig S3b main (si4_clean_s3b.png): x 0@462.65, 10@1017.3; y 0@1207.5, 6@807.6; verify x 6, y 5.
  - Fig S3b inset: x 0@548.9, 10@826.9; y 5.0@1146.4, 5.5@946.5; verify x 6, y 5.2.
- Working copies: legends, insets, titles and curve-fit lines whited out with rectangles in work-dir copies (page7_clean_4c.png, si4_clean_s3b.png). Originals untouched.
- Tool `check` against the printed 10 MPa value: 8 archives passed. Digitizations in `digitizations/` (9 JSON files).

## Tool check failure (CF)

- `check` for Fig 4c CF failed: digitized 0.0786 wt% vs printed 0.07 (12% relative, 0.009 wt%, 0.4 px). The tool marked that archive `discarded`.
- I regenerated the CF archive with identical parameters; its status is `unchecked` (not `passed`). CF rows are kept. Protocol digitization uncertainty (1% of axis span = 0.06 wt%) covers the difference. The merged row M9 carries the printed 0.07 as `table_direct`.

## Seen but not extracted

- Table 2 literature rows ([30]-[33]; NF, ANF, ARCF1, ACF A20 x2): other groups' measurements, not this paper's samples. Flag for C: if the protocol wants literature comparison values from review tables, they are in Table 2 and Fig 4d.
- Fig 4d (uptake vs BET area, literature plus this work): not an isotherm; this-work points duplicate Table 2.
- Fig S1: not an isotherm. Shows uptake bars/points for PCF_L, PCF_H, APCF_L, APCF_H series and Pd/APCF_L samples whose values are not given in any table or in the text. No values read off; flag for C.
- Table 1 samples with no H2 value anywhere: PCF_L 0.5 (BET 201, Vp 0.25, Vmicro 0.12), PCF_L 0.3 (424/0.27/0.16), PCF_L 0.1 (110/0.06/0.02), PCF_H 0.5 (377/0.27/0.14), PCF_H 0.1 (798/0.46/0.25). Characterization only.
- Calculated values in the text, not measurements: 4.78 wt% (Eq. 1), spillover 0.67 vs about 0.3 wt%, slope 1.41e-3 wt% per m2/g, Chahine 2.00e-3 and Zuettel 2.28e-3 slopes, aerogel 5.3 wt% [17], 0.4/0.6 wt% quoted from [30].
- Markers that could not be separated or are hidden (not extracted):
  - Fig 4c CF low-pressure cluster: one merged blob (n = 593 px), at least 6 markers plus the origin. Only the 9 isolated plateau points are used.
  - Fig 4c teal (Pd 0.5/APCF_H 0.3) 0.1 MPa marker, about 2.4 wt%: merged with neighbours.
  - Fig 4c magenta (APCF_H 0.3) 0.1 MPa marker (n = 9 px): split by a vertical line, below the size filter.
  - Fig 4c ACF 0.2 MPa marker: hidden under other series.
  - Fig 4c origin markers (all series): hidden at the axis corner.
  - Fig S3b blue (Pd 0.5 mM) 0.1 and 0.2 MPa diamonds: only fragments (n = 45, 29, 35 px).
  - Fig S3b red (Pd 0.1 mM) and black (Pd 0 mM) main-panel low-pressure filled markers: hidden under other series. Plateau points taken from the inset instead.
  - Fig S3b blue, red and black origin markers: hidden. Only the Pd 1 mM origin is visible and is included.
  - Open markers, Fig 4c and Fig S3b (instruction asks for both branches): NOT extracted. In Fig 4c open markers appear only at about 0.1-1.2 MPa in each of the five series, drawn over or behind the filled markers and offset from them (e.g. an open teal triangle near 5.3 wt% at about 1 MPa against filled 5.2). Their centroids cannot be separated from the filled markers and lines at the page-image resolution. At 2-10 MPa only filled markers are plotted. Not done: open-marker rows are missing from rows.csv, and C will need a higher-resolution source or a judgment call. Flag for C.

## Judgment calls

- All rows coded `adsorption`, per the instruction (adsorption unless the paper says desorption). The paper defines empty/filled markers only for the N2 isotherms (Fig 4a caption "empty-filled markers"; Fig S3a "adsorption (empty) and desorption (filled)"). No caption says what open vs filled means for the H2 isotherms (Fig 4c, S3b), and Fig S3b assigns marker shape by Pd concentration (0 mM black circles, 0.1 mM red rectangles, 0.5 mM blue rhomboids, 1 mM green hexagons). RISK for C: if the N2 convention were carried over to H2, the filled markers I extracted would be the desorption branch; the paper does not say so, so I did not code it.
- Fig 4c and Fig S3b series for the same sample (S3 APCF_H 0.3 = Pd 0 mM; S6 Pd 0.5 mM) are coded as separate isotherms (I4 vs I6, I5 vs I8), not merged, because the two figures are different plots and the points differ by digitization error.
- `isotherm_point_count` = 16 on every row: filled markers only, counting those hidden or merged that I could infer (see the unseparated-marker list). It does NOT include the open markers, so it understates the instruction's "both branches" count (see the open-marker entry). Each row's notes say "point count = filled markers only".
- Partial markers: under 50% of plateau marker area are excluded by the tool's min-px filter; 50-75% are kept at extraction_confidence 2 (15 rows: M11-M14, M24, M26-M28, M40, M43, M54, M55, M57, M85, M86).
- Gravimetric method (ISOSORP-HyGrA, Waters) without a stated buoyancy correction: `basis_inferred` = unknown. Uptake basis (excess vs absolute vs total) not stated; `uptake_type` left unspecified, which gives the validator warning on all rows.
- S3b Pd 1 mM origin row (0.126 bar, 0.0024 wt%) is included; the origin markers of the other series are hidden.

## Inconsistencies in the paper

- Total pore volume of Pd 0.5/APCF_H 0.3 (BET 2611 m2/g) stated as 1.42 cm3/g in the text and 1.43 in Table 3/Table 2. Table value (1.43) used.
- "0.5 nm" appears where "0.5 mM" is meant (Pd concentration).
- The text cites "Table 2 and Figure 4c and Figure S2" for the 10 MPa uptakes; Figure S2 is the FE-SEM figure, the Pd-loading H2 isotherms are Figure S3b.
