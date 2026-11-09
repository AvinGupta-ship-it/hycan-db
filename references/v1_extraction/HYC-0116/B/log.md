# HYC-0116 extraction log (agent B)

Paper: Ramirez-Vidal et al. 2021, ACS Appl. Mater. Interfaces, 10.1021/acsami.0c22192. Inputs: page images only (main-01..39, si1-1..8). Six commercial activated carbons (MSC30, MSP20X, SA1500, SA20, TH90I, Filtrasorb400), samples S1-S6 in the order of Section 2.1. 325 rows, 35 isotherms. No non-carbon sorbent was measured.

## Sources extracted (one line each)

- Main file page 8-10 (printed p.7-9), Sections 2.2-2.3 and 3.1: instruments (HPVA II and 3-Flex, Micromeritics), degassing, sample mass, pressure program, excess/absolute definitions; coded on every row.
- SI page 2, Table S1: BET area and P/P0 range, S_NLDFT, V_T, V_meso, V_micro, V<0.7, V0.7-2, d_T, d_mu, V_mu,DR-N2, V_mu,DR-CO2 for all six samples; on every row of each sample.
- Main file page 17 (printed p.16), Figure 2a (77 K, HPVA II): all six series, adsorption (filled) and desorption (open) markers digitized; 84 rows (one of them merged with the p.17 text value 2.34 wt.%).
- Main file page 17, Figure 2b (273 K): highest-pressure point of each series digitized and merged with the p.17 text values at 14 MPa (6 rows).
- Main file page 18 (printed p.17), Section 3.2 text: 2.34 wt.% at 3 MPa for Filtrasorb400 (merged with Fig 2a); 4 MPa values 5.78, 4.74, 4.04, 3.24, 2.90 and the Filtrasorb400 value 2.31 (pressure from the Fig 4 caption); 14 MPa / 273 K values 1.04, 0.95, 0.86, 0.72, 0.67, 0.55 (merged with Fig 2b).
- Main file page 22 (printed p.21), Figures 5a and 5b (77 K, 3-Flex, up to 100 kPa and 1.5 kPa): every separable marker digitized (5b markers inside the 5b range, 5a markers above it), 134 rows, one isotherm per sample shared by 5a and 5b.
- Main file page 23 (printed p.22), Figure 6a (SA20) and 6b (SA1500): highest-pressure point of the 93-253 K isotherms (17 rows). The 77 K and 273 K curves of Fig 6 are the Fig 2a/2b runs (the eight separable 77 K SA20 markers of Fig 6a agree with Fig 2a within about 1%), so they were not extracted again, except four SA20 77 K markers that are hidden or overlapped in Fig 2a (adsorption near 0.9, 10.4 and 12.2 MPa, desorption near 11.0 MPa), taken from Fig 6a into the Fig 2a isotherm.
- Main file page 27 (printed p.26), Section 3.3 text: maximum absolute H2 at 77 K, 7.5, 6.2, 5.6, 3.9, 3.5, 3.3 wt.% (6 rows, pressure unstated, value_kind unclear).
- SI page 3, Table S2: MDA n_max (mol kg-1) for the six samples (6 rows, fitted_extrapolated, temperature and pressure unstated because the fit spans 77-273 K).
- SI page 5, Table S4: Sips N at 11 temperatures for six samples (66 rows, fitted_extrapolated; Table S4 prints no unit, mol kg-1 taken from Eq. (5) where N has the unit of nabs).

## Digitization

Calibration (pixel positions found from pixel rows/columns; every run passed the tool's third-tick check):
- Fig 2a: x 0 MPa at 241, 12.5 at 534, check 5.0 at 358; y 0 at 1212.5, 6 at 790.5, check 3 at 1001.5.
- Fig 2b: x 0 at 737, 12.5 at 1025, check 5.0 at 851.5; y 0 at 1203, 1.0 at 822, check 0.6 at 974.5.
- Fig 5a: x 0 kPa at 246.5, 100 at 444.5, check 60 at 365.5; y 0 at 706, 2.5 at 246, check 1.5 at 429.5.
- Fig 5b: x 0 kPa at 561.5, 1.5 at 755.5, check 0.5 at 626; y 0 at 706, 0.25 at 246, check 0.15 at 429.5.
- Fig 6a: x 0 MPa at 299, 14 at 555.5, check 8 at 445.5; y 0 at 658.5, 4.5 at 183.5, check 2 at 447.5. Fig 6b: x 0 at 724.5, 14 at 981, check 8 at 871; same y.

Method: `digitize_figure.py extract --mode markers` with the series colour. Filled markers of clean series were extracted in one run per series. Open (desorption) markers, overlapping markers, the dense Fig 5a series and the Fig 6 highest points were extracted with one single-marker ROI per marker (ROI positions found with helper scripts in the work directory; values always come from the tool). Archives: one JSON per series for whole-series runs (fig2a_<series>_ads_main.json, fig5b_<series>.json); one JSON per marker for single-marker runs (fig2a_<series>_des_N.json, fig2a_*_5MPa/last/3MPa.json, fig5a_<series>/mNN.json, fig6*_..._highest.json, fig6a_SA20_77K_*.json). Whole-series archives also contain fragment centroids (line pieces, partial markers) that were not used; each row names its archive and carries the value used. Unreferenced files fig5a_*/m01 etc. are archived attempts on markers excluded below.

Stated-value checks (`digitize_figure.py check`): fig2a_Filtrasorb400_ads_main.json PASS at 3 MPa vs 2.34 wt.%; fig2a_{MSC30,MSP20X,SA1500,SA20,TH90I}_ads_main.json PASS at 4 MPa vs 5.78, 4.74, 4.04, 3.24, 2.90 wt.% (linear interpolation 5.823, 4.743, 4.076, 3.251, 2.919). Single-point archives (Fig 2b, Fig 6) cannot be checked by the tool (it needs the stated x inside the digitized range); the Fig 2b points agree with the 14 MPa text values within 0.6%.

Marker counts (extracted vs counted) and markers not separated:
- Fig 2a (each run: 11 adsorption + 5 desorption steps; Filtrasorb400 shows all 16): MSC30 9+5, MSP20X 8+5, SA1500 8+5, SA20 9+5 (incl. 4 from Fig 6a), TH90I 9+5, Filtrasorb400 11+5. Not separable: adsorption markers in the cluster within about 0.3 MPa of the origin, where all six series overlap (MSC30 2, MSP20X 3, SA1500 3, SA20 2, TH90I 2). Partial markers rejected: MSC30 and MSP20X filled markers at 5 MPa in the whole-series run (re-extracted with a single-marker ROI), SA20 near 0.9, 3.2, 7.2 (desorption ring fragment) and 12.1 MPa, TH90I near 0.13 MPa and 11.2 MPa (desorption ring fragment), SA1500 near 12.9 MPa (re-extracted).
- Fig 2b: only the highest-pressure point per series was required (6 extracted).
- Fig 5a/5b (approximate counts in isotherm_point_count): MSP20X 28 extracted of about 30 (not separated: 98.6 kPa marker under an MSC30 marker; 5b marker near 0.06 kPa overlapped by TH90I and Filtrasorb400 markers); MSC30 21 of about 30 (not separated: markers near 6.4, 8.3 and 73 kPa partly covered, six markers at about 77-97 kPa hidden under MSP20X circles); SA1500 21 of about 31 (not separated: markers near 2.5, 8.7, 12.2, 17.2 kPa partly covered, one near 22 kPa under a Filtrasorb400 marker, four at about 67-79 kPa under TH90I markers, 5b marker near 0.34 kPa partly under an SA20 marker); SA20 19 of about 27 (not separated: markers below about 10 kPa in the near-axis cluster, seven markers at about 72-97 kPa under Filtrasorb400 markers); TH90I 22 of about 25 (not separated: 2.2 kPa marker partly covered, both 5b markers near 0.05 and 0.23 kPa overlapped by Filtrasorb400/MSP20X markers); Filtrasorb400 23 of about 27 (not separated: 1.6 kPa marker clipped by the y axis, 5b markers near 0.006, 0.06 and 0.26 kPa partly covered). Acceptance rule: template-match score >= 0.6 and pixel count >= 70% of the series' typical marker.
- Fig 6: one highest-pressure point per isotherm. SA20 93-253 K and SA1500 113-253 K extracted. SA1500 93 K not extracted: in Fig 6b the 77 K and 93 K markers have the same colour; filled pure-blue markers near 10.1 MPa (3.6 wt.%) and 12.0 MPa (3.5 wt.%) are not in the Fig 2a 77 K run, and the 93 K run's rightmost marker may be hidden under the 77 K marker at 12.9 MPa, so its highest-pressure point cannot be identified. Temperature assignment near the right edge is uncertain for SA20 93, 113, 133 K and SA1500 113 K (rows carry confidence 2 and a note); rows were assigned by following each row of markers across 10-14 MPa, which gives a monotonic decrease with temperature.

## Values seen but not extracted

- Abstract: "Excess hydrogen adsorption capacities of 2.3 to 5.8 wt.% were obtained at 77 K and 4 MPa" and "surface areas ranging from 996 to 2216 m2 g-1": ranges summarizing per-sample values extracted elsewhere.
- Main p.4 (printed): "up to 7 wt.% at 4 MPa and 77 K" (refs 14, 24) and Chahine's rule (1 wt.% per 500 m2 g-1): literature values.
- Main p.17 (printed): excess H2 "higher than 5, 3 and 2 wt.% for MSC30, SA20 and Filtrasorb400 ... at temperatures lower than 93 K and pressures between 2 and 8 MPa": describes a region of the interpolated surface of Fig 3, not a value at stated conditions.
- Main p.20 (printed): 1.25 wt.% per 500 m2 g-1 of S_NLDFT: a slope, not an uptake.
- Main p.23-24 (printed): n_max range 72.5-20.8 mol kg-1 and Va 1.50-0.362 cm3 g-1 (same as Table S2; Va is not an uptake); Richard et al. 71.6 mol kg-1 and 1470 MPa for AX-21 (literature); A_BET 3300 vs 2800 m2 g-1 for MSC30 vs AX-21.
- Main p.28-29 (printed): "(0-3.5 mmol g-1)" range of adsorbed amounts used for entropies: not an uptake measurement.
- Figure 1 (N2 and CO2 isotherms, PSDs, pore volumes): characterization only; values taken from Table S1.
- Figure 3 (3D excess surfaces and T-P contour maps for MSC30, SA20, Filtrasorb400): not isotherms; no values beyond the text above.
- Figure 4 (uptake vs A_BET and S_NLDFT at 77 K/4 MPa and 273 K/14 MPa): not an isotherm; its values are the p.17 text values already extracted.
- Figure 5c (Henry's constant vs micropore size), Figure 7 (MDA parameters vs texture; n_max = Table S2), Figure 8, Figure 9 (isosteric heats vs absolute uptake), Figure 10 (entropies; n_max labels = Table S2), Figure 11 (model curves), Figure S1, Figure S3: not uptake isotherms.
- Figure S2 (absolute H2 isotherms of SA20 and SA1500 vs fugacity at 11 temperatures, Sips fits): not digitized; the x axis is fugacity, not pressure, and the values are computed by the authors from the excess isotherms with Eq. (2); the maximum absolute values are taken from the p.26 text instead.
- Table S2 Va, alpha, beta, P0; Table S3 (R2); Table S4 b and k: not uptake values.

## Coding notes and discrepancies

- Basis: excess named and defined (Section 3.1) and absolute reported separately (Eq. 2), so basis_stated = true for excess and absolute rows; n_max is coded absolute with basis_stated = false (the paper links it to nabs through Theta = nabs/nmax but does not name its basis).
- wt% convention unknown (no point printed in two units). Table S2 and S4 values are mol kg-1, stored in uptake_mmol_g with W1 computed.
- calibration_described: true for 3-Flex rows, false for HPVA rows (the only free-volume sentence is in the 3-Flex paragraph). replicates_reported false: "The first isotherm was repeated twice" without results.
- MSC30 A_BET printed 3305 (Table S1), 3310 and 3300 (text); Table S1 used. SA1500 BET range printed "0.05-0.018". Text says "nine temperatures" while Table S2 and Fig 6 have eleven. Stated desorption steps (11.5, 8, 4.5, 1.5, 0.5 MPa) differ from the plotted open markers (about 11, 7.5, 5, 3.5, 2.5 MPa); stated adsorption steps include 0.1, 0.5, 0.8 MPa while markers lie near 0.1, 0.8, 2, 3, 5, 7.5, 10, 12.5, 14 MPa.
- Filtrasorb400: 2.34 wt.% at 3 MPa (text, matches the plotted point) and 2.31 wt.% (listed with the 4 MPa values, Fig 4 caption says 3 MPa) conflict; both recorded as printed, 2.31 with value_kind unclear and no isotherm_id.
