# HYC-0128 extraction log (agent B)

Wang et al. 2010, Energy & Environmental Science, "Hydrogen storage in a Ni–B nanoalloy-doped three-dimensional graphene material". Input: page images main-1 to main-6 only (no supplementary file). 136 rows written: 131 `figure_digitized` (Fig. 4), 2 `table_direct` and 3 `text_direct` (each merged with a plotted point).

## Sources extracted from

- main-4, Table 1 (structural properties of GP and GP-Ni0.83B1.09): BET area, pore volume and pore-size range for GP and Doped-GP, put on every row of S1 and S2. "Real capacity/wt%" 1.4 (GP) is merged with the Fig. 4 GP point at P/P0 = 1.0 (M18). 4.4 (Doped-GP) is merged with the Fig. 4 GP-Ni0.83B1.09 point at P/P0 = 1.0 (M53).
- main-1, Abstract and Broader context: "4.4 wt% at 77 K and 106 kPa" gives the printed pressure of M53.
- main-3, text discussing Fig. 4:
  - "~1.4 wt%" (GP) is M18.
  - "maximal hydrogen storage capacity of 4.4 wt%" is M53.
  - "GP-Ni2.41B0.69 ... decreases to 2.6 wt%" is M88, merged with the Fig. 4 point at P/P0 = 1.0 (pressure digitized).
- main-4, text discussing Fig. 5 (273 K):
  - GP "maximum capacity of 0.008 wt% at 106 kPa" is M35.
  - GP-Ni0.83B1.09 "capacity of 0.2 wt%" is M71 (pressure digitized).
  - Both are merged with the highest-pressure point of their Fig. 5 isotherm.
- main-2, Experimental:
  - instrument "pore and surface analyzer (Quantachrome Adsorb-1) which employs the standard volumetric method";
  - degassing "overnight under high vacuum and 150 °C";
  - H2 measured at 77 K and 273 K (87 K for the isosteric heat);
  - surface area, pore size and pore volume from the N2 isotherm at 77 K;
  - ICP-ES for Ni and B.
- main-2, Results: Ni 2.41/1.51/0.83 wt% and B 0.69/1.39/1.09 wt%, and the sample names GP, GP-Ni2.41B0.69, GP-Ni1.51B1.39 and GP-Ni0.83B1.09.
- main-3, Fig. 4 (H2 adsorption and desorption at 77 K, P/P0 with P0 = 106.66 kPa, mg/g): every separable marker of all eight series was digitized. The archives are `digitizations/HYC-0128_fig4_{STc,STo,SQc,SQo,CIc,CIo,TRc,TRo}.json` (ST = GP stars, SQ = GP-Ni0.83B1.09 squares, CI = GP-Ni2.41B0.69 circles, TR = GP-Ni1.51B1.39 triangles; c = closed = adsorption, o = open = desorption, per the caption).
- main-3, Fig. 5 (273 K): only the highest-pressure point of each isotherm was digitized, following §9. The archives are `digitizations/HYC-0128_fig5_GP_273K_top.json` and `digitizations/HYC-0128_fig5_GP-Ni0.83B1.09_273K_top.json`.

## Coding decisions

- **Sample labels.**
  - GP-Ni0.83B1.09 is labelled `Doped-GP`, its label in Table 1, the first table that reports its uptake.
  - GP is labelled `GP`, also from Table 1.
  - GP-Ni2.41B0.69 and GP-Ni1.51B1.39 take their labels from the figure legends (Fig. 1a, Fig. 4).
- **Sample numbering** follows first appearance. The Abstract names the 3D graphene, then the Ni 0.83/B 1.09 sample. Results then list the 2.41 and 1.51 samples.
- **Material class and synthesis.**
  - GP is coded `reduced_graphene_oxide` / `thermal_reduction`: graphite oxide heated at 150 °C under vacuum for 45 min. The paper calls it "3D graphene".
  - The Ni–B samples are coded `composite`, with `metal_element` Ni and the ICP-ES Ni content.
  - B is part of the Ni–B nanoalloy particles and is not coded as a lattice dopant. Its content is given in `notes`.
- **Pore data.**
  - Table 1 "Pore volume" has no qualifier and is stored as `total_pore_volume_cm3_g`, with probe gas N2 and method unspecified.
  - The "pore size distribution 10–60 Å" is a range, not an average. It is recorded only in `notes`.
- **Basis, convention and lab.**
  - Basis is not named. The volumetric instrument gives `basis_inferred = excess` and `uptake_type = unspecified`.
  - Printed wt% values have `wt_pct_convention = unknown` / `none`, because the paper prints no second unit for any point. The mg/g values are only plotted.
  - `instrument_identified = true` (manufacturer and model named). `calibration_described`, `replicates_reported` and the degas duration ("overnight") are not stated.
  - `measuring_lab_id` = Li group, Nanyang Technological University (corresponding author Chang Ming Li, affiliation a).
- **Turning points at P/P0 = 1.0.** In every Fig. 4 and Fig. 5 isotherm, the adsorption line from the P/P0 ≈ 0.98 point and the desorption line both join the point at P/P0 = 1.0.
  - For GP, GP-Ni2.41B0.69 and GP-Ni1.51B1.39 (Fig. 4), and for both Fig. 5 isotherms, this point is drawn with the open (desorption) symbol on top. For GP-Ni0.83B1.09 in Fig. 4 it is drawn with the closed symbol.
  - Each such point is one row, coded `adsorption` and archived with the adsorption series. It is counted once in marker counts.
- **Merges.** The printed capacities 1.4, 4.4 and 2.6 wt% (77 K), and 0.008 and 0.2 wt% (273 K), match the P/P0 = 1.0 points: 13.92, 44.44 and 26.45 mg/g, and 0.0818 and 1.866 mg/g.

## Digitization procedure

- **Fig. 4 calibration** on the page image main-3.png, from pixel-row and pixel-column profiles:
  - x: 0.0 at the left axis line, 728.51 px; 1.0 at the tick at 1066.67 px; checked at 0.6 = 931.67 px (relative error 0.13%).
  - y: 0 at the bottom axis line, 421.49 px; 50 at the top axis line, 119.33 px; checked at 20 = 301.0 px (relative error 0.31%).
- **Fig. 5 calibration:**
  - x: 0.0 at 731.33 px, 1.0 at 1067.0 px, checked at 0.6 = 932.56 px.
  - y: 0.0 at 1406.45 px, 2.0 at 1133.67 px, checked at 0.8 = 1297.56 px.
- **Pressure.** pressure_bar = P/P0 × 106.66 kPa × 0.01, with P0 as printed on both axes. Uptake in wt% = 0.1 × mg/g (W1).
- **Separating the Fig. 4 series.** All eight series are black, so colour cannot separate them, and the connecting lines join every marker.
  - For each series I built an image (`work/f4/derived_<series>.png`) with the same size and geometry as main-3.png. It holds only the page pixels of that series' markers, and white elsewhere.
  - Markers were found with a dark-pixel mask (grey < 150) inside the axes box. Small enclosed holes (≤ 45 px) and open-symbol interiors were filled, and a 3×3 opening removed the connecting lines.
  - Each marker was assigned to a series by its symbol (closed or open square, circle, triangle or star) and by curve continuity, checked on zoomed tiles.
  - Partly overlapping markers were split by a seeded watershed. Scripts are `work/f4_blobs.py`, `work/f4_seeds.py` and `work/f4_segment.py`; seeds are in `work/f4/seeds.json`.
  - Two pieces were clipped to the symbol's own box to drop an attached line fragment: the open square at page (775.5, 381.5) and the open star at (798.5, 395.5).
- **Running the tool.** `digitize_figure.py extract --mode markers` ran on each derived image with colour #000000 ± 420 and `--open-px 1`, so open-symbol outlines survive. The archive's `source_image` is the derived image, with its sha256.
- **Marker counts.** Extracted counts equal the counted markers for every series: STc 18, STo 16, SQc 18, SQo 17, CIc 17, CIo 15, TRc 17, TRo 16. Rejected pixel groups of 1–4 px (outline fragments) are listed in each archive.
- **Fig. 5 points.** Each point was taken from the page image itself, with a tight `--roi` around the single marker and `--open-px 1`:
  - GP-Ni0.83B1.09: grey open square, #000000 ± 380.
  - GP: pale red open star, #d09090 ± 75.
- **§3.4 step-6 checks (`check`).**
  - Passed for SQc (44 mg/g), STc (14 mg/g), CIc (26 mg/g), Fig. 5 GP (0.08 mg/g) and Fig. 5 GP-Ni0.83B1.09 (2.0 mg/g, with an absolute tolerance of 0.5 mg/g, the rounding of the printed "0.2 wt%").
  - SQo, STo, CIo, TRc and TRo have no value printed in the paper, so their archives stay `unchecked`.
- **Confidence.** Digitized rows are confidence 3. Rows whose marker overlapped another series' marker are confidence 2: watershed-split pieces, and the coincident triangle/circle pairs below.

## Markers seen but not separated, or not extracted

- **Fig. 4, low-pressure cluster.** Below about P/P0 0.17 (below about 5 mg/g), the markers of all eight series merge into one solid black cluster (page px x 737–792, y 379–420). It runs down to an origin blob at about P/P0 0.01. These markers cannot be separated or counted, and none was extracted. They include:
  - the GP-Ni0.83B1.09 closed square at about P/P0 0.13, and open squares at about 0.10 and below;
  - the pair of a closed triangle and a closed circle at about P/P0 0.177 (page ≈ 788, 394), which merges with the open circle at about 0.174 (page ≈ 787.5, 389);
  - the open triangle at about P/P0 0.146 (page ≈ 778, 395), whose outline joins the cluster;
  - the GP stars below P/P0 0.177 (closed) and 0.207 (open);
  - every lower point of each series.

  For this reason `isotherm_point_count` is left empty for I1, I3, I5 and I6. The separable counts are 34, 35, 32 and 33 respectively; the shared turning point is counted once.
- **Fig. 4, coincident closed markers.** The closed triangle (GP-Ni1.51B1.39 adsorption) and the closed circle (GP-Ni2.41B0.69 adsorption) are drawn on top of each other, offset by less than 2 px, at P/P0 ≈ 0.226, 0.276, 0.326, 0.377, 0.426 and 0.476. Each pair was digitized as one blob, and both rows carry the blob centroid.
- **Fig. 4, pairs split by watershed** (centres less certain, confidence 2):
  - closed and open star at P/P0 ≈ 0.93;
  - closed and open circle at ≈ 0.93–0.94;
  - closed triangle with open circle at ≈ 0.78, 0.73 and 0.53;
  - closed triangle above closed circle at ≈ 0.68, 0.63 and 0.58 (at 0.58 with an open circle on top);
  - open circle above the coincident closed pair at ≈ 0.377;
  - open triangle with open circle at ≈ 0.30 and 0.25.
- **Fig. 5, other markers** (not extracted, because §9 takes only the highest-pressure point at temperatures other than 77 K):
  - GP-Ni0.83B1.09: 36 more markers (19 closed, 17 open; 37 including the turning point, which is `isotherm_point_count` of I4).
  - GP: red stars; those below about P/P0 0.85 lie on or under the x axis and cannot be counted, so `isotherm_point_count` of I2 is empty.

## Values seen but not extracted

- Table 1, "Theoretical monolayer H2 capacity": 1.3 wt% (GP), 0.5 wt% (Doped-GP) and 4.8 wt% (Perfect Graphene). These are calculated monolayer capacities, not measurements. The text also cites "~1.3 wt%".
- Table 1, "Perfect Graphene" BET 2630 m²/g (also "2,630 m² g⁻¹" in main-5): a theoretical reference, not a measured sample.
- main-1, Introduction: Ru-doped templated carbon "1.43 wt% at 298 K and 10.3 MPa" (Wang and Yang, ref. 15). A literature value for a sample not studied in this paper.
- main-4: templated carbon with "super high surface area (~2,600 m² g⁻¹)" at "~1.0 wt%" "at the similar conditions", from the authors' previous study (ref. 36). A comparison value for a sample not studied in this paper, with no numerical temperature or pressure.
- main-5: "When hydrogen capacity is below 7.5 mg g⁻¹, the adsorption heats of both samples are similar at ~1 kJ mol⁻¹", and "relatively constant at ~1 kJ mol⁻¹". These are isosteric-heat statements; 7.5 mg/g is a loading threshold, not an uptake measured at a stated T and P.
- main-5, Fig. 7: isosteric heat against H2 adsorbed for GP and GP-Ni0.83B1.09. Not an isotherm, not digitized, and it gives no uptake at a stated T and P.
- main-2: H2 isotherms at 87 K (liquid argon) were measured for the isosteric heat but are not shown or tabulated, so there are no values.
- main-4, Fig. 6: N2 isotherms at 77 K and the pore-size-distribution inset for GP and GP-Ni0.83B1.09. These are characterization only; the Table 1 values are used.
- main-2 and main-3, Figs. 1–3 (XRD, EDX, SEM, TEM): characterization only. TEM shows Ni–B particles from a few nm to about 20 nm (in the S2 description).
- Abstract and conclusions, "better than that of pristine graphene by three times", and main-4, "about 25 times higher": ratios of values already extracted.
- No non-carbon comparison material is measured. Every sample has H2 uptake rows, so no characterization-only sample needs listing.
