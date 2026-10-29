# HYC-0044 extraction log (agent B)

Hwang et al. 2021, Nanomaterials 11, 1830. 129 rows. Input: main-01..13.png, si1-1..4.png. Date 2026-10-29.

## Sources extracted

- main p. 6, Table 2: H2 uptake at 77 K and 10 MPa for CF (M24), ACF (M62), PCF_H 0.3 (M15), APCF_H 0.3 (M39) and Pd 0.5/APCF_H 0.3 (M88). Each value is the same measurement as the 10 MPa point of its Figure 4c curve, so they are merged with that point. The table also gives S_BET, Vp, Vmicro and W_average, which are put on every row of each sample.
- main p. 6, Table 2: literature rows NF [30], ANF [30], ARCF1 [31], ACF A20 [32] and ACF A20 [33] (M124-M128). These are coded `previously reported` and `area_same_sample = other_paper`. T and P come from the Table 2 caption and the Figure 4d caption ("measured at 77 K and 10 MPa"); I did not check them against the cited papers.
- main p. 9, Table 3: APCF_H 0.3 (M48), Pd 0.1/APCF_H 0.3 (M72), Pd 0.5/APCF_H 0.3 (M105) and Pd 1/APCF_H 0.3 (M123) at 77 K and 10 MPa. Each is merged with the 10 MPa point of its Figure S3b curve. Table 3 also gives the characterization of Pd 0.1 and Pd 1. The APCF_H 0.3 (5.14) and Pd 0.5 (5.45) values repeat Table 2.
  - Pairing rule: Table 2 is merged with Figure 4c, because the text cites them together. Table 3 is merged with Figure S3, because the text cites them together for the Pd series. Each plotted 10 MPa point is merged only once.
- main p. 5, Table 1: characterization of PCF_H 0.3 (identical to Table 2). The other Table 1 samples are listed under "Not extracted".
- si1 p. 1, Table S1: C and Pd at% for APCF_H 0.3 and the three Pd samples. These go in `notes` only, because the method is not stated and the value is at%, so `metal_loading_wt_pct` stays empty.
- main p. 3-4, Sections 2.2-2.5: synthesis, KOH activation, HCl wash, Pd electrodeposition, N2 sorption (ASAP 2020, HK micropore volume), H2 measurement (gravimetric, 77 K, ISOSORP-HyGrA, Waters Corporation). This gives `instrument_identified = true`. No buoyancy correction, degassing, sample mass, H2 purity, BET range or replicates are stated.
- main p. 9, text Section 3.3: "activated carbon aerogel produced using CO2, 5.3 wt% [17]" becomes M129, (unlabelled 1), with T and P unstated and `value_kind = unclear`.
- Text that repeats table values goes in `source_location`, not on separate rows:
  - abstract: 5.14 and 5.45 wt% at 77 K and 10 MPa; 3058 m2/g; 1.18 cm3/g
  - p. 7: 889 m2/g, 0.47 cm3/g, 11 m2/g, 3058 m2/g, 1.55 cm3/g
  - p. 8: 0.07, 1.35, 2.87 and 5.14 wt% at 77 K and 10 MPa
  - p. 8: Pd 0.5 BET 2611 m2/g
  - p. 9: 5.45 wt%
  - p. 9: literature 150 and 265 m2/g, 0.4 and 0.6 wt% (same as NF and ANF in Table 2)
  - Conclusions: 5.14 and 5.45 wt%
- main p. 7, Figure 4c (77 K H2 isotherms, 0-10 MPa): 5 series digitized. See "Figure digitization".
- si1 p. 4, Figure S3b main panel and inset (77 K H2 isotherms of the Pd series): 4 series digitized. See "Figure digitization".

## Not extracted (value seen, reason)

- p. 4 Eq. (1) and p. 8: slope K = 1.41e-3 wt% per m2/g. A correlation over several samples, not an uptake value.
- p. 8: Chahine's rule, 2.00e-3 wt% per m2/g [17,35], and the theoretical monolayer limit, 2.28e-3 wt% per m2/g [36]. These are rules or theory, not measurements.
- p. 9: 4.78 wt%, the physisorption-only capacity of Pd 0.5/APCF_H 0.3 calculated from Eq. (1). It is computed from a correlation over several samples, so it is not a row.
- p. 9: 0.67 wt% spillover improvement (5.45 - 4.78), and Conclusions: spillover enhancement "~0.3 wt%". Both are derived differences, not uptakes. The two numbers disagree with each other.
- p. 8: qualitative statements ("rapid increase below 500 kPa", "saturated at 2 MPa"). No value.
- p. 8: Pd 0.5/APCF_H 0.3 total pore volume "1.42 cm3/g" in the text, against 1.43 in Tables 2 and 3. The table value is used; the discrepancy is noted on the S6 rows.
- p. 7: "fraction of micropores ... increases to around 13.1% (Table 1)". This does not match Table 1 and is not used.
- main p. 5, Table 1: these samples have characterization but no H2 uptake in any table or text, so they get no rows. Values are S_BET m2/g, Vp cm3/g, Vmicro cm3/g (% of Vp):
  - PCF_L 0.5: 201, 0.25, 0.12 (48.0)
  - PCF_L 0.3: 424, 0.27, 0.16 (59.2)
  - PCF_L 0.1: 110, 0.06, 0.02 (33.3)
  - PCF_H 0.5: 377, 0.27, 0.14 (51.9)
  - PCF_H 0.1: 798, 0.46, 0.25 (54.3)
- si1 p. 2, Figure S1a,b: correlation plots of H2 uptake against BET area and against micropore volume. They are not isotherms, so they were not digitized. They show these uptakes, which no table or text gives:
  - PCF_L 5:5, 7:3 and 9:1
  - PCF_H 5:5 and 9:1
  - APCF_L 5:5, 7:3 and 9:1
  - APCF_H 5:5 and 9:1
  - Pd0.1/APCF_L 7:3, Pd0.5/APCF_L 7:3 and Pd1/APCF_L 7:3
  - The APCF_L, APCF_H 5:5 and 9:1, and Pd/APCF_L samples also have no tabulated area or pore volume.
  - The axis units are misprinted ("cm2 g-1", "m3 g-1").
- main p. 7, Figure 4d: H2 uptake against surface area. Not an isotherm, so not digitized. Its values are those of Table 2 (this work and refs. 30-33).
- main p. 7, Figure 4a and 4b, and si1 p. 4, Figure S3a: N2 isotherms and pore size distributions. Not H2.
- Figures 1, 2, 3, 5 and S2: schematic, SEM, TEM, SAED and EDS. Figure 5f gives a Pd particle size distribution (mean 41.7 nm, put in the S6 description). No H2 values.
- No non-carbon comparison sorbents (MOF, zeolite or hydride) have values in this paper.

## Figure digitization

### Figure 4c (main p. 7)

The tool was run on `work/main-07_legendmasked.png`. This is a copy of main-07.png with the in-plot legend box (x 385-535, y 872-955) whitened, so the legend symbols are not extracted. No data marker lies inside that box.

Calibration:
- x axis: 0 MPa at the left frame (229.6 px) and 10 MPa at the right frame (600.5 px). The x tick marks are hidden behind the CF markers that lie on the axis, so the "0" and "10" ticks were located at the frame lines on which their labels are centred. The check uses the centre of the tick label "4" (378.0 px), with residual 0.03%.
- y axis: 0 wt% at the bottom frame (1091.0 px) and 6 wt% at the top frame (823.0 px). The tick marks for 0 and 6 coincide with the frame lines. Check: the tick at 5 (867.5 px), with residual 0.07%.
- Pressure is read in MPa and stored x10 in bar.

Series:
- CF (black): `fig4c_CF_filled_plateau.json`.
  - The 9 markers at 2-10 MPa were extracted (ROI x > 285 px).
  - About 6 markers at 0-1 MPa, including a lobe at the origin, merge into one black blob on the x axis and could not be separated. They were not digitized. The point count of 15 is approximate.
- ACF (red): `fig4c_ACF_filled.json`, 14 filled markers.
  - Not separable: the filled square near 0.2 MPa (hidden behind the squares near 0.1 and 0.4 MPa) and an open square near 0-0.05 MPa at about 1.0 wt% (only its bottom edge is visible).
  - Counted 16.
- PCF_H0.3 (green): `fig4c_PCF_H0.3_filled.json`, 15 filled markers, all extracted. No open marker is visible. Counted 15.
- APCF_H0.3 (magenta): `fig4c_APCF_H0.3_filled.json`, 15 filled markers.
  - Not separable: two partially visible open triangles, near 0.05-0.1 MPa at about 3.9 wt% and near 0-0.05 MPa at about 3.0 wt%.
  - A magenta outline near 1.0-1.4 MPa at about 4.9-5.0 wt% may be an open marker merged with the connecting lines. I could not tell, so it is not counted.
  - Counted 17.
- Pd 0.5/APCF_H0.3 (teal):
  - Filled markers come from two runs, `..._filled_low.json` (5 markers at 0-1 MPa) and `..._filled_plateau.json` (9 markers at 2-10 MPa). One run over the whole plot also returned a blob at 279.8, 853.9 px. It is the junction of the two teal connecting lines near 1.3 MPa, not a marker. Splitting the region of interest (ROI) removed it.
  - Open markers: `..._open_1.json` (0.18 MPa) and `..._open_2.json` (1.24 MPa). Each uses a tight ROI with no opening; connecting lines touch the outlines.
  - Not separable: the filled triangle near 0.1 MPa at about 2.4 wt% (hidden behind a PCF hexagon) and the open triangle near 0.08 MPa at about 3.2 wt% (partly hidden).
  - Counted 18.

### Figure S3b (si1 p. 4)

The tool was run on si1-4.png.

Main panel calibration:
- x axis: 0 MPa at the left frame (462.7 px), on which the label "0" is centred; 10 MPa at the right frame or tick (1017.3 px). Check: the tick at 4 (684.45 px), with residual 0.04%.
- y axis: 0 wt% at the bottom frame (1207.55 px) and 6 wt% at the top frame (807.68 px). Check: the tick at 5 (874.21 px), with residual 0.03%.

Inset calibration:
- x axis: 0 MPa at the inset's left frame (548.83 px) and 10 MPa at its right frame or tick (826.77 px). Check: the tick at 4 (660.09 px), with residual 0.08%.
- y axis: 5.0 wt% at the tick (1146.44 px) and 5.5 wt% at the top end of the left frame (946.5 px). Check: the tick at 5.2 (1066.09 px), with residual 0.02%.

Points between 5.0 and 5.5 wt% are taken from the inset only, because its scale is finer and it separates the Pd 0 mM and Pd_1 mM markers, which overlap in the main panel. All other points come from the main panel. As a cross-check, the main panel gives 0.79 MPa / 5.036 wt% and 0.98 MPa / 5.197 wt% for the two Pd_0.5 mM points also read from the inset (inset: 0.80 MPa / 5.045 wt% and 1.00 MPa / 5.199 wt%).

Series:
- Pd 0 mM (black, = APCF_H 0.3): `figS3b_inset_Pd0mM_filled.json`, 9 filled markers at 2-10 MPa.
  - The marker centroids include some outline pixels of the overlapping open circles and green hexagons.
  - Not separable: open circles partly visible behind the filled ones at 2, 3 and 6 MPa (inset), and about 3 markers below 0.3 MPa in the main panel hidden behind the Pd_1 mM and Pd_0.5 mM markers.
  - Counted about 15.
- Pd_0.1 mM (red): `figS3b_inset_Pd0.1mM_filled.json`, 9 filled markers. `figS3b_inset_Pd0.1mM_open_1.json` gives the open square near 1.3 MPa; red lines cross it, so its centroid may be displaced by up to about 3 px.
  - Not separable: below 0.3 MPa in the main panel the red markers (origin square, and squares near 2.8 and 3.8 wt%) are almost entirely hidden.
  - Counted about 14.
- Pd_0.5 mM (blue):
  - `figS3b_inset_Pd0.5mM_filled.json`: 11 filled markers (0.80 MPa, 1.00 MPa and 9 at 2-10 MPa).
  - `figS3b_main_Pd0.5mM_filled_low.json`: 2 filled markers (0.35 and 0.56 MPa).
  - `figS3b_main_Pd0.5mM_split_marker_1.json` and `_2.json`: filled markers near 0.08 and 0.16 MPa, each split in two by an overlying green line. The row value is the pixel-count-weighted mean of the two component centroids from the tool, that is, the centroid of the marker's visible pixels.
  - Open markers: `figS3b_inset_Pd0.5mM_open_1.json` and `_open_2.json` (0.83 and 1.18 MPa).
  - Not separable: about 3 partly visible open diamonds below 0.6 MPa (main panel), and an origin marker if there is one.
  - Counted about 20.
- Pd_1 mM (green):
  - `figS3b_main_Pd1mM_filled_low.json`: 7 filled markers, including the origin point. It digitizes at -0.0003 wt% and is stored as 0.
  - `figS3b_inset_Pd1mM_filled.json`: 9 filled markers at 2-10 MPa.
  - Open markers: `figS3b_main_Pd1mM_open_2.json` (0.07 MPa) and `_open_1.json` (0.20 MPa).
  - Not separable: about 3 partly visible open hexagons (near 0.4 MPa at about 4.2 wt%, and near 1.2-1.3 MPa at about 4.8-5.0 wt%).
  - Counted about 21.

### General

- Archives: the protocol asks for one archive per series. Several series need more than one tool run, because tight ROIs were needed for open, split or hidden-adjacent markers. Every tool output is kept unchanged, named by figure, series and part.
- Stated-value check (`digitize_figure.py check`): run on every archive that contains the 10 MPa point, against the table value, at the last digitized pressure (9.97-9.99 MPa, because the tool refuses x = 10 just outside the extracted range). All passed, within 5%:
  - CF 0.07
  - ACF 1.35
  - PCF 2.87
  - APCF 5.14 (Figure 4c and Figure S3b)
  - Pd 0.5 5.45 (Figure 4c and Figure S3b)
  - Pd 0.1 5.30
  - Pd 1 5.17
- Archives with no stated value in their range (the low-pressure, open-marker and split-marker runs) remain `unchecked`. They use the same calibration as the checked archive of the same figure panel.
- Branches: neither H2 figure caption says which markers are adsorption and which desorption. The empty/filled meaning is defined only for the N2 panels (Figure 4a: empty = adsorption, filled = desorption; Figure S3a likewise).
  - In both H2 figures, open markers form a second branch below about 1.3 MPa and coincide with the filled markers at 2-10 MPa.
  - All points are coded `adsorption`, because the paper never says a value was measured on desorption. Each row's `notes` says whether its marker is filled or open.
- Duplicated curves: Figure S3b "Pd 0 mM" (I6) and "Pd_0.5 mM" (I8) show the same samples as Figure 4c APCF_H0.3 (I4) and Pd 0.5/APCF_H0.3 (I5).
  - Their digitized points agree within digitization error, so each pair is probably one run plotted twice. The paper does not say so.
  - They are kept as separate isotherms, because each plotted curve is one run.
  - `replicates_reported` stays false.
- Isotherm point counts are counts of the markers I could identify, including partly hidden ones. They are approximate where markers overlap below about 1.3 MPa.
