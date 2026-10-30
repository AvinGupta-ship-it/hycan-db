# HYC-0097 extraction log (agent B)

Paper: Fierro et al. 2019, conference poster (Carbon 2019, Lexington), HAL hal-02186765. Input: main-1.png (HAL cover page), main-2.png (the poster). No supplementary file. 68 rows written.

## Sources extracted from

- main-1.png (HAL cover page): title, authors and deposit details only; no data.
- main-2.png header: corresponding author marked "*" is Vanessa Fierro, affiliation 1 "Institut Jean Lamour, UMR 7198 CNRS and Université de Lorraine, Épinal, France", so `measuring_lab_id` = "Fierro group, Université de Lorraine". No DOI is printed and paper.json gives `doi` = "", which the validator rejects as a missing required field. Following the data dictionary rule for papers without a DOI, `doi` = "no-doi:Fierro:2019" on every row.
- main-2.png Methodology box: samples MSP 20X, MSC 30, SA 1500, SA 20, TH90I ("CACs"). N2 at 77 K, 1 atm (ASAP 2020) leads to "BET Surface". N2 and CO2 (273 K, 1 atm, ASAP 2420) together lead to "2D-NLDFT HS: Pore size distribution and S_NLDFT". H2 at T = 77-273 K, P = 0.1-14 MPa (1-140 atm), "(HPVA)", then MDA modelling in MATLAB. The poster names no instrument manufacturer, so `instrument_identified` = false; `measurement_method` = volumetric_sieverts, inferred from the instrument name HPVA. No degassing, sample mass, H2 purity or free-volume calibration is stated.
- main-2.png Modified Dubinin-Astakhov section: the text says "we first fitted the excess hydrogen adsorption with the MDA equation", and the equation n_exc = n_abs - rho_g V_a is given with its terms defined. This gives `basis_stated` = true and excess basis on all rows.
- main-2.png Acknowledgements: "CACs free supply from Ingevity and Silcarbon Aktivkohle". All samples are therefore `synthesis_method` = commercial, but the poster does not say which supplier made which sample.
- **Figure 3** ("Excess H2 isotherms at 77 K and 0.1-14 MPa"; x: Absolute Pressure (MPa); y: excess H2 wt.%). This is 43 rows over 5 series, each in its own isotherm, I1-I5.
  - Image: crop of main-2.png at offset (105,4826), 1228x1018 px, saved as work/fig3.png.
  - Ticks found from pixel rows and columns. x: 0 MPa at 178 px, 12 MPa at 955.5 px, check tick 6 MPa at 566.5 px (error 0.06%). y: 0 at 799.5 px, 6 wt% at 108 px, check tick 3 at 453.5 px (error 0.07%).
  - Tool settings: markers mode, tolerance 40, open-px 6, ROI 180 52 1018 798.
  - Series colours and archives: MSC30 #ff0000, fig3_MSC30.json; MSP20X #008000, fig3_MSP20X.json; SA_1500 #0000ff, fig3_SA_1500.json; SA_20 #8000ff, fig3_SA_20.json; TH90I #800080, fig3_TH90I.json.
- **Figure 4** ("MDA fitting of excess H2 Isotherms on MSC30"; x: Pressure [MPa]; y: Hydrogen excess [mmol/g]). This is 25 rows: all 15 separable markers of the 77 K curve (I6), plus the highest-pressure marker of each of the other 10 curves (I7-I16).
  - Image: crop of main-2.png at offset (1333,4826), 1176x1018 px, saved as work/fig4.png.
  - Ticks taken from gridline pixels, which coincide with the labelled ticks. x: 0 at 114 px, 15 at 1167 px, check tick 10 at 816 px. y: 0 at 816 px, 30 at 43 px, check tick 15 at 429 px. The spacing is uniform: 351 px per 5 MPa and 128-130 px per 5 mmol/g.
  - Markers are thin anti-aliased open circles in a low-resolution raster. With any RGB tolerance that excludes the grey fit lines, the circles broke into fragments (108 or more groups). The tool was therefore run on derived images with the same geometry, work/fig4_red.png and work/fig4_blue.png, made by work/make_sep2.py:
    - red pixels: R-G > 25 and |G-B| < 20; blue pixels: B-R > 25 and |R-G| < 20;
    - each mask dilated 3x3, then painted as pure colour on white.
    - Tool settings: markers mode, tolerance 40, open-px 0, marker size 15-400 px.
  - Result: 99 red groups (archive fig4_MSC30_red_markers.json) and 53 blue groups (fig4_MSC30_blue_markers.json). A single ring is 69-82 px, so larger groups are overlapping markers.
  - There are 11 fitted curves. Red markers fall on common pressure steps, about 1, 2, 3, 5, 7.5, 10, 12.5 and 14 MPa, plus the low-pressure doses. From 2 MPa upward every step has 11 markers, and blue markers form 5 groups of 11. Curves were assigned by ranking the markers within each step: highest is the 77 K curve, lowest is the 273 K curve.
  - The two highest markers at 13.6-13.8 MPa (20.56 and 19.59 mmol/g) were assigned to curves 1 and 2 by rank and by continuity with each curve's 10.4 and 12.3 MPa points. The fitted curves 1 and 2 cross there, so these rows have confidence 2.
  - The figure gives no legend for red versus blue markers. All markers are coded `isotherm_branch` = adsorption, because the paper does not say any were measured on desorption. Blue markers sit at pressures different from the red steps and may be a desorption branch; this is noted on each blue row.
- §3.4 step-6 `check`: not applicable. The poster prints no numeric uptake value to check against, so every archive keeps status "unchecked".

## Figure 3: markers counted but not extracted, and position biases

- MSP20X (I1, 10 markers counted, 7 extracted): 3 low-pressure markers are hidden behind MSC30 markers, which are drawn on top. They are at about 0.1 MPa / 2.8 wt%, about 0 MPa / 1.4 wt% and about 0 MPa / 0.2 wt%. Only fragments (ears) are visible; tool fragment centroids were 0.054/2.842 + 0.193/2.813, 0.107/1.375 and 0.093/0.239, all biased. Not extracted.
- SA_1500 (I3, 11 counted, 10 extracted): the marker near 0 MPa / 0.1-0.15 wt% is hidden behind the MSC30 diamond. Not extracted.
- SA_20 (I4, 10 counted, 7 extracted): 3 markers not extracted.
  - About 0 MPa / 0.2 wt%: hidden.
  - About 0.15 MPa / 1.1 wt%: mostly hidden behind TH90I.
  - About 2 MPa / 3.1 wt%: hidden behind the SA_1500 circle; the fragment centroid was 2.177 MPa / 3.125, biased.
  - The SA_20 line also runs on past the 13 MPa axis limit, so at least one more point lies outside the plotted range. It is not visible and not counted.
- TH90I (I5, 10 counted, 9 extracted): the marker near 0 MPa / 0.15 wt% is hidden behind the MSC30 diamond. Not extracted.
- MSC30 (I2): 10 counted, 10 extracted.
- Markers at the left frame (the MSC30 points at 0.18 and 1.30 wt%, SA_1500 at 0.87 wt%, TH90I at 1.20 wt%) are clipped by the plot frame or covered by the MSC30 line. The tool centroid is therefore biased toward higher pressure, by up to about 0.07 MPa; the geometric estimate is in each row's notes, and these rows have confidence 2.
- SA_1500 at 2.52 wt% is half hidden by the TH90I hexagon, so its pressure is biased low (estimated centre about 0.83 MPa, tool 0.76 MPa).
- SA_1500 at about 13 MPa is clipped by the right frame. Its centre is about 12.97 MPa; the tool gave 12.907 MPa.

## Figure 4: values seen but not extracted

- 77 K curve: its lowest red marker, near 0 MPa and about 0.9 mmol/g, lies in the cluster of overlapping circles at the origin (tool group n = 306, about 4 rings) and could not be separated. It is counted in `isotherm_point_count` = 16 but not extracted.
- Curves 2-11: only the highest-pressure point of each was extracted, as the scope requires for temperatures other than 77 K. Their other markers (about 14 per curve) were not extracted for that reason. Some low-pressure markers of curves 6-11 are also merged in clusters near the origin, so their counts (15 each) may be off by one.
- Curves 2-10 have no temperature label; the figure labels only 77 K (top) and 273 K (bottom). These rows have `temperature_unstated` = true.
- Figure 3 MSC30 and the Figure 4 77 K curve share the same pressure points: 0.795/0.782, 1.920/1.910, 2.974/2.971, 5.066/5.057, 7.680/7.683, 10.367/10.369 and 12.328/12.327 MPa.
  - Their values agree at low pressure: 1.30 wt% versus 6.48 mmol/g (1.306 wt%), and 2.75 wt% versus 13.59 mmol/g (2.740 wt%).
  - From 1 MPa up, the Figure 4 values are lower by 1-15%, and the gap grows with pressure.
  - Figure 4 also has a point at 13.64 MPa, beyond the 13 MPa axis of Figure 3; the Figure 3 MSC30 line stops at 12.3 MPa.
  - The paper says neither that these are the same run nor why the values differ. They are recorded as separate isotherms, I2 and I6, with this noted on both.
  - Because the two figures disagree beyond either convention, they were not used to infer the Figure 3 wt% convention, which stays unknown/none.

## Other values seen but not extracted

- Introduction: "activated carbons (ACs) exhibit, on average, the highest hydrogen adsorption capacities (up to 7 wt. % at 4 MPa and 77 K) [1,2]". This is a literature value for ACs as a class, not a measurement of a sample in this paper, so it is not a row.
- Introduction: "reduce by 23% the volume needed for hydrogen storage when compared to pure compression at 20 MPa and room temperature [3]" and "moderate pressures, lower than 40MPa". Neither is an uptake value.
- Figure 1 (bar chart plus line): S_NLDFT (m2/g, right axis) and NLDFT pore volumes V<0.7 nm, V0.7-2 nm and Vmesopores (cm3/g) for MSC-30, MSP-20, SA_1500, SA_20 and TH90I. Not digitized, because it is not an isotherm. It is the only source of surface areas and pore volumes, so the rows carry no area or pore-volume numbers.
  - Rows are coded `surface_area_method` = DFT, `surface_area_probe_gas` = other (N2 + CO2, 2D-NLDFT HS), `pore_volume_method` = NLDFT, `pore_volume_probe_gas` = other and `area_same_sample` = yes, all with null values.
  - "BET Surface" is named in the Methodology, but no BET value appears anywhere.
- Figure 2: 3D pore size distributions dV/dw for the five carbons. Not digitized (characterization). Accompanying text: MSC-30, SA1500 and SA20 show "a high percentage of mesopores", while MSP20X and TH90I are "essentially microporous".
- Figure 5: V_a (cm3/g) and n_max (mol/kg) from the MDA fits, plotted against S_NLDFT for the five carbons, with R = 0.83 and 0.93.
  - n_max is a fitted model parameter, not a measured uptake, and the figure is not an isotherm, so neither was digitized. These values are not given elsewhere.
  - The V_a axis tick labels are inconsistent: 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2.
- Figure 6: MDA entropy factor beta (J/mol K) and enthalpy factor alpha (J/mol) against average micropore size (nm), with R = 0.97 and 0.85. These are fitted parameters plus a characterization quantity (average micropore size, method not stated). Not digitized.
- Figures 7 and 8: adsorption enthalpy -ΔH_ads (kJ/mol) and entropy ΔS_ads (J/mol K) against fractional filling θ for the five carbons, derived from the MDA fits. Not digitized.
- MDA equation block: R = 8.314 J/mol K is a constant, not data.
- No non-carbon sorbent (MOF, zeolite or hydride) appears in the paper.

## Files

- Work directory: fig3.png and fig4.png (full-resolution crops), fig4_red.png and fig4_blue.png (colour-separated derived images used for the Figure 4 archives), make_sep2.py (the script that makes them), build_rows.py (writes rows.csv from the archives), and trial/ (exploratory tool runs, not used for rows).
- Validator: `scripts/validate_row_detail.py --errors-only` reports no errors; a full run also reports no warnings.
