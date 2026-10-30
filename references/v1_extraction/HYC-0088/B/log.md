# HYC-0088 extraction log (extractor B)

Paper: Lionetti et al. 2024, Int J Hydrogen Energy 61, 639-649; SI (si1, 8 pages). 186 rows.
Samples with H2 uptake: WS_PD_30 (S1), WS_PD_60 (S2), WS_PD_90 (S3), WS_PD_120 (S4). Isotherms: I1-I4 = 77 K low-pressure
(ASAP 2460) for S1-S4; I5 = WS_PD_90 at 77 K up to 80 bar (f-PcT); I6 = WS_PD_90 at 298 K (f-PcT).

## Sources extracted

- Table 6 (main-08, p. 646), H2 uptake at 1 bar and 77 K: 4 values, each merged with the p/p0 ~ 1 point of Fig. 8 (M21, M59, M99, M141).
- Text p. 645 ("1.69 wt%, at 1 bar, for WS_PD_90"), abstract ("1.7 ... wt% at ... 1 ... bar"), Table S3 row 77 K / 1 bar / 1.69: same measurement as Table 6 WS_PD_90; recorded on M99.
- Table S3 (si1-5) row 77 K / 80 bar / 2.62 wt%: M183. The abstract ("2.6 wt% at ... 80 bar"), text p. 646 ("maximum ... around 2.6 wt%") and Conclusions restate it and are recorded on M183. Not merged with Fig. 11b: its last point is at 75.09 bar, more than 2% from 80 bar. No isotherm_id, because the paper does not say the value is taken from the curve.
- Table S3 row 298 K / 80 bar / 0.12 wt%: M185. Not merged with Fig. 12a, whose highest point is at 77.61 bar (3.0% from 80 bar).
- Table 7 (main-09, p. 647) and text p. 646, Toth wt%max = 2.82 +/- 0.04 wt%: M182. value_kind = fitted_extrapolated; no pressure (asymptote), so pressure_unstated = true; isotherm I5, because the text says the fit is to the Fig. 11a data.
- Text pp. 646-647, "amount of hydrogen adsorbed for each cycle at 298 K is approximately 0.1 wt%": M186 (approximate; pressure not stated).
- Fig. 8 (main-07, p. 645), H2 adsorption isotherms at 77 K, four series: the main source of the adsorption branches of I1-I4.
- Fig. 9a-d (main-08, p. 646), H2 adsorption-desorption at 77 K: the source of all desorption points of I1-I4 (M22-39, M60-77, M100-117, M142-159), and of the adsorption points that are hidden in Fig. 8.
- Fig. 11b (main-09, p. 647), WS_PD_90 at 77 K up to 80 bar: adsorption M160-174 and desorption M175-181.
- Fig. 12a (main-10, p. 648), WS_PD_90 at 298 K: highest-pressure point only (M184).
- Characterization copied onto every row: Table 2 (SBET, Vultra, Vmicro, Vmeso, TPV; Vsuper and % Micro in notes), Table 4 (XPS at.%, in notes), Table 5 (C1s functional groups) and Table S1 (WS_PD_90: average pore size 0.79 nm, SBET 1163.2). Methods are from sections 2.2-2.3: BET range p/p0 0.01-0.30, NLDFT, TPV at p/p0 0.995, degassing, instruments, and He pycnometry (skeletal density 2.47 +/- 0.18 g/cm3, WS_PD_90).

## Coding decisions

- Pressure for Fig. 8/9: the x axis is relative pressure p/p0, and p0 is not stated. I converted with p0 = 1 bar, because the text says the 77 K isotherms span "the pressure range of 0-1 bar" and Table 6 reports the values "at 1 bar". Points at p/p0 = 1.002-1.006 lie just beyond the highest labelled tick.
- Fig. 8 and Fig. 9 plot the same runs: at shared pressures their filled markers agree within 0.01 wt% (9-17 shared points per sample, mean |dy| 0.0017-0.0027 wt%; the largest differences are at partly occluded markers). Each point is recorded once. Adsorption values come from Fig. 8 where its marker is unoccluded, and from Fig. 9 otherwise; each row names its archive.
- The p/p0 ~ 1 point appears in Fig. 8 as ADS, while Fig. 9 draws it as the first DES marker. It is kept once, as adsorption, merged with Table 6. The Fig. 9 DES archives contain it, but no DES row was written for it.
- wt% convention: the definition "weight percent of gas adsorbed per gram of absorbent (wt.%)" appears in the high-pressure (f-PcT) paragraph. I coded W1/stated for f-PcT rows and unknown/none for the ASAP 2460 rows.
- Basis: no basis named, so basis_stated = false. Both instruments are volumetric, so basis_inferred = excess; uptake_type = unspecified.
- replicates_reported: true for f-PcT rows (repeated isotherms in Fig. 11c/12b; Table 7 +/-). False for ASAP rows (no uncertainty, no repeated low-pressure isotherm).
- Fig. 12a: the highest-pressure marker of the 298 K run is the open (desorption) marker at 77.61 bar, 0.110 wt%, which is the one extracted. The highest adsorption-branch point (72.32 bar, 0.1225 wt%) is not extracted (only one point per non-77 K isotherm).
- material_class activated_carbon. K, Ca, Na, Cl, P and F (XPS) are biomass residues or contaminants, and N comes from the N2 annealing; none was deliberately added, so no dopant or metal fields were set (details in notes). synthesis_method pyrolysis (N2 carbonization); CO2 activation goes in activation_method.
- measuring_lab_id: Conte (first marked corresponding author), Università Della Calabria (affiliation a). Both H2 instruments are in-house.
- isotherm_point_count: I1-I4 = 45 (27 adsorption: 20 above p/p0 0.02 found in all four samples, plus 7 below; 18 desorption plus the shared p/p0 ~ 1 point). The 7 low-pressure adsorption markers are fused or hidden. They resolve as 7 for WS_PD_120 (top layer in Fig. 8) and WS_PD_60, and I assumed 7 for WS_PD_30 and WS_PD_90, so these counts are estimates. I5 = 24 (16 adsorption including the origin marker, plus 8 desorption). I6 = 16 (14 adsorption plus 2 desorption).

## Digitization (scripts/digitize_figure.py extract --mode markers; archives in digitizations/)

Calibration (page pixels; lowest/highest labelled ticks, third tick verified; tick pixels found from row/column darkness profiles):
- Fig. 8: x 0->710, 1.0->1146 (0.6 at 971.5); y 0->1267, 1.8->926 (1.0 at 1077.5).
- Fig. 9a/9c: x 0->310.3, 1.0->588.1 (0.6 at 477.0). Fig. 9b/9d: x 0->688.8, 1.0->966.1 (0.6 at 855.1).
  y 9a/9b: 0->1153.1, 1.8->935.5 (1.0 at 1032.25); y 9c/9d: 0->1469.4, 1.8->1251.15 (1.0 at 1348.2).
- Fig. 11b: x 0->516.1, 60->707.0 (40 at 643.45); y 0->997.16, 3.0->802.04 (2.0 at 866.98). Points above 60 bar lie beyond the highest labelled tick.
- Fig. 12a: x 0->313.86, 60->533.83 (40 at 460.63); y 0->393.85, 1.0->158.33 (0.4 at 299.48).

Image preparation (scripts in the work directory: prep.sh, mask.py, holes.py, run_digitize.sh):
- Legends and in-plot text that share a series colour were painted white on copies of the page images; the pixel grid is unchanged.
- Filled markers were extracted from these masked copies with the tool's default 3-px opening, which removes thin open-marker outlines.
- Open (DES) markers have the same colour as the filled ones. To isolate them, the enclosed white interior of each outline (fill_holes of non-white pixels) was painted as a solid disc on a blank copy, and the tool then extracted those discs. Hole areas: 7-24 px. Spurious holes of 1-5 px were dropped.
- The tool's check (Table 6 values at p/p0 = 1) passed for the four Fig. 8 archives and the four Fig. 9 DES archives. The other archives have no stated value at a plotted pressure.

Marker counts (extracted vs on the plot):
- fig9a/9b/9c/9d_des: 19 of 19 open markers each.
- fig11b_ads: 16 of 16 (the origin marker is not a row).
- fig11b_des: 7 of 8. One ring at about 0.5 bar / 0.99 wt% is hidden under the adsorption marker at 0.9 bar: not separable, not extracted.
- fig12a_ads: 14 of 14. fig12a_des: 2 of 2 (origin and 77.6 bar).
- fig8_ads_WS_PD_30: 18 detections. 0.043 and 0.105 are hidden by WS_PD_120 (taken from Fig. 9a). The detections at 0.135, 0.160 and 0.188 are partly occluded and replaced by Fig. 9a. None of the low-pressure markers was detected.
- fig8_ads_WS_PD_60: 18 detections. The fragment at p/p0 -0.002 / 0.206 wt% is unused (frame edge; possibly the 0.162 marker). The partly occluded 0.132 and 0.158 are replaced by Fig. 9b. The squares at 0.185, 0.21, 0.24, 0.265 and 0.33 are under WS_PD_90 triangles: 0.21 and 0.24 come from Fig. 9b; 0.185, 0.265 and 0.33 are hidden in both figures and not extracted.
- fig8_ads_WS_PD_90: 21 detections. The fragment 0.0138 / 0.438 wt% (n = 9 px, about 25% visible) is unused. A triangle tip at about 0.31 wt% is visible above WS_PD_120 but was not detected.
- fig8_ads_WS_PD_120: 25 detections. Two of them are fused pairs (0.0018 / 0.055 wt%, n = 73; 0.0023 / 0.154 wt%, n = 90) and are not extracted.
- fig9a_ads: 22 detections. The fused blob 0.0023 / 0.099 wt% (n = 90, about 3 markers spanning 0.02-0.17 wt%) and the fragment 0.0061 / 0.315 wt% (n = 9) are not extracted. One more filled marker near 0.22-0.25 wt% is hidden under DES rings.
- fig9b_ads: 13 detections. The fused pair 0.0007 / 0.071 wt% (n = 60) is not extracted. The other low markers (about 0.21, 0.29, 0.37 and 0.50 wt%) are under DES rings; 0.37 (partial) and 0.50 come from Fig. 8.
- fig9c_ads: 11 of the 11 visible filled markers. The remaining adsorption markers are under DES rings and come from Fig. 8.
- fig9d_ads: 14 detections. The fused blob 0.0020 / 0.057 wt% (n = 52) is not extracted. The fused 0.0895 / 0.759 wt% (two markers and a ring) and the partial markers at 0.594 and 0.660 were replaced by Fig. 8.
- Overlays of the tool's centres on the page crops confirmed placement (crops/ov_*.png in the work directory).

## Figures not digitized

- Fig. 11a (same run as Fig. 11b): the red Toth line cuts through the markers, so only 6 of 16 were isolated. Fig. 11b was used instead; the Toth curve is a fit and is not data.
- Fig. 11c, six 77 K cycles of WS_PD_90: all markers are black, differ only in shape (about 5 px) and overlap in clusters at every pressure. They cannot be separated by colour or isolated, so the cycles are not digitized. The 1st cycle appears to be the Fig. 11a/b run.
- Fig. 12b, six 298 K cycles: same problem. The highest-pressure points of the six cycles (about 0.10-0.14 wt% near 77 bar) cannot be separated, so none is extracted.

## Values seen but not extracted

- WS_PT (pellets) and WS_GR (granular), Table 3 / Fig. 4 / Fig. S3: characterization only, no H2 uptake. WS_PT: SBET 674, Vultra 0.160, Vsuper 0.099, Vmicro 0.259, Vmeso 0.032, TPV 0.291, 89% micro. WS_GR: SBET 1041, Vultra 0.316, Vsuper 0.076, Vmicro 0.392, Vmeso 0.040, TPV 0.432, 91% micro.
- Samples processed entirely in CO2 (powder: no yield; pellets: tiny non-porous yield): no data.
- Conclusions: "over 1.6 wt%" at 77 K and 1 bar for the most ultramicroporous samples. This restates Table 6 (WS_PD_60 1.61, WS_PD_90 1.69) and is noted on M59 and M99.
- Text p. 646: cycle differences "within the experimental error (almost 10%)". A relative reproducibility with no value to extract.
- Table 7: K = 1.24 +/- 0.17 and t = 0.66 +/- 0.04 (Toth parameters, not uptake), noted on M182. The text's "t parameter value of 0.66" is the same.
- Table S3, H2/SBET x 10^3 (1.45, 2.25, 0.10): derived ratios, not uptake.
- Table S3, other rows (lemon peel, corncob, tangerine peel, cherry laurel, olive bagasse, almond shells, lignin, Palmyra sprout, coconut shells, pinecone, date pits, peanut shell, pine-derived lignin, Posidonia oceanica, wood chips, rice husk): literature values from other papers, not measured here.
- Table S1 (other WS-based adsorbents) and the text's De Rose et al. values (SSA 497.34, TPV 0.208, Vmicro 0.175): literature characterization.
- Fig. 10 (H2 uptake vs SBET, TPV, Vmicro, Vultra, Vsuper): replots Table 6 against Table 2, not an isotherm. R^2 values: 0.92, 0.91, 0.94, 0.90, 0.52.
- Fig. 2 and Fig. 4 (N2 isotherms and NLDFT PSD), Fig. 3 and Fig. S3 (pore-volume bar charts), Fig. 1 (TGA), Fig. 5/S1/S2 (SEM), Fig. 6/7/S4 and Table S2 (XPS): not H2 uptake. The pore-volume values match Tables 2/3.
- Origin markers (0, 0) in Fig. 11b (adsorption) and Fig. 12a (desorption): not measured uptakes, not extracted.
- Abstract and Conclusions values (SBET 1163 m2/g, TPV 0.491, Vmicro 0.450; average SBET about 900 m2/g; 87-96% micropores): the same as Table 2, or summary statistics of it.
