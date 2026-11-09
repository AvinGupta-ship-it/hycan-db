# HYC-0135 extraction log (agent B)

Input: page images main-1.png to main-8.png (no supplementary file). 23 rows written.

## Sources extracted from

- main-4.png (p. 18468), Fig. 4a, GS@77K (filled squares): all 12 markers digitized, rows M1-M12, isotherm I1. Archive `digitizations/HYC-0135_fig4a_GS_77K.json`.
- main-4.png, Fig. 4a, GS@87K (open squares): 15 markers digitized and counted; only the highest-pressure marker (0.974737 kPa) written, row M13, isotherm I2. Archive `digitizations/HYC-0135_fig4a_GS_87K.json`.
- main-4.png, Fig. 4b, BP280@77K (filled stars): all 9 markers digitized, rows M14-M22, isotherm I3. Archive `digitizations/HYC-0135_fig4b_BP280_77K.json`.
- main-4.png, Fig. 4b, BP280@87K (open stars): 8 markers counted, 7 extracted by the tool; only the highest-pressure marker (0.746003 kPa) written, row M23, isotherm I4. Archive `digitizations/HYC-0135_fig4b_BP280_87K.json`.
- main-4.png, Table 2 (pore volume, micropore volume, BET area): characterization on every row of each sample.
- main-3.png, Table 1 (EDS composition): in `material_description` and notes.
- main-2.png / main-3.png, Experimental text (sample origin, Ar at 87 K characterization by Micromeritics 3Flex, DFT pore analysis, sample masses 0.1676 g GS and 0.3385 g BP280, instrument, gas purity in words, degassing 363.15 K 3 h then 423.15 K 12 h, mean of three measurements): method and reporting fields.
- main-3.png / main-4.png, "Adsorption equilibrium" text and Eq. (1): excess basis named and defined (basis_evidence).
- main-1.png, author line and affiliation: corresponding author Q.R. Zheng (marked *), Jimei University -> `measuring_lab_id`.

## Digitization procedure (Fig. 4)

- Axes calibrated on the lowest and highest labelled ticks, with a third labelled tick as check; tick pixels found by scanning pixel rows and columns of main-4.png.
  - Fig. 4a: x 0.2 kPa = px 233, 1.0 = 518, check 0.6 = 375 (residual 0.23%); y 0.02 mmol/g = px 1425.5, 0.10 = 1203, check 0.06 = 1314 (residual 0.15%).
  - Fig. 4b: x 0.2 kPa = px 743.5, 1.2 = 1075, check 0.6 = 876 (residual 0.05%); y 0.002 mmol/g = px 1408.5, 0.008 = 1188.5, check 0.004 = 1335 (residual 0.11%).
- The figure is black and white, with filled and open markers of the same colour joined by lines. To isolate each series, the page image was preprocessed in the work directory without changing pixel coordinates (script `work/prep.py`): filled markers = dark mask (grey < 128) eroded by a 3x3 element (removes the 1-2 px lines and open-marker outlines, separates the corner-touching squares at 0.13-0.17 kPa, keeps marker centroids); open markers = enclosed white interiors of the hollow markers (grey < 128 for squares, < 230 for the faint open stars). Legend boxes and panel letters were blanked. `digitize_figure.py extract --mode markers` was then run on these images with colour #000000.
- Marker counts: GS@77K 12 counted / 12 extracted; GS@87K 15 / 15; BP280@77K 9 / 9; BP280@87K 8 counted / 7 extracted. In BP280@87K two overlapping open stars near 0.10 and 0.11 kPa (resolved as separate points at 103 and 110 Pa in Fig. 5b) could not be separated at this image resolution and came out as one marker (0.1095 kPa); this point is not used for any row (only the highest-pressure 87 K point is extracted).
- The tool flags points below the lowest or above the highest labelled tick (x < 0.2 kPa, y < 0.02 or > 0.10 mmol/g in Fig. 4a; x < 0.2 kPa, y < 0.002 or > 0.008 mmol/g in Fig. 4b) as outside the calibrated range. Both axes are linear and run from 0 at the frame corner, consistent with the tick spacing, so these are linear readings inside the plotted frame.
- The `check` subcommand was not run: the paper prints no numeric uptake value for any plotted point.
- The line from the origin to the first marker of each series has no marker at the origin and gives no row.

## Values seen but not extracted

- Fig. 5a/5b (main-5.png, p. 18469), "Isotherms of excess amount of hydrogen on the GS (a) and carbon black BP280 (b) at low surface coverage", y-axis Gamma_1 labelled "nm^2", x-axis P/Pa: not extracted as rows. These are the same measurements as the low-pressure markers of Fig. 4 (GS@77K 5 points at 134, 151, 169, 226, 283 Pa; GS@87K 4 points; BP280@77K 4 points at 46, 75, 103, 179 Pa; BP280@87K 6 points), re-expressed as a surface concentration per unit BET area (Eq. 2-9, A = BET area). A verification digitization (work/check_fig5a_GS_77K.json, work/check_fig5b_BP280_77K.json) gives the same pressures as Fig. 4 and Gamma_1 / n_exc constant per sample (4.46-4.48 for GS, 32.7-33.5 for BP280). The quantity is normalized by the BET area, not by a film or geometric area, so it does not fit `areal_uptake_g_cm2`, and the unit label is ambiguous; the gravimetric values of the same points are in the Fig. 4 rows. The fitted lines in Fig. 5 ("Fitting liner") are not extracted.
- Table 3 (main-5.png): Henry constants H_P (E+10 mol m^-2 Pa^-1) GS 13.82 (77 K), 4.950 (87 K); BP280 5.702, 3.296; second virial constants B_AS (E+7 m^3 g^-1) GS 8.879, 3.593; BP280 3.665, 2.393; q_st^0 (kJ/mol) GS 6.357, 6.441; BP280 3.693, 3.776. Model parameters, not uptake values.
- Text p. 18468 / conclusions: mean limit isosteric heat 6.399 kJ/mol (GS) and 3.735 kJ/mol (BP280); the conclusions print 3.635 kJ/mol for BP280 (inconsistent with the 3.735 in the text and with the Table 3 mean 3.7345). Not uptake values.
- Fig. 6 (main-6.png): ln(B_AS/A) against epsilon_sf/kT with smooth and rough model curves; not an isotherm. Its legend lists "BP280@77K" twice (open and filled star); presumably the open star is 87 K. Not digitized.
- Table 4 (main-6.png): potential well epsilon_sf/k (K) GS 33.55 (77 K), 32.14 (87 K); BP280 31.97, 31.75. Not uptake values. Abstract and conclusions repeat 33.55 K and 31.97 K.
- Fig. 2 (main-3.png): adsorption/desorption isotherms of argon at 87 K on GS and BP280 (n_exc in mmol/g against P/P0). Characterization of the carbon sorbents, not H2; not digitized.
- Fig. 3 (main-4.png): DFT pore size distributions from the Ar isotherms; characterization, not digitized.
- Fig. 1 (main-3.png): SEM images and EDS spectra; characterization only.
- Abstract: specific surface areas "about 220 m2/g and 36 m2/g" (rounded forms of Table 2), measurement range 77-87 K and 0-1 kPa. No uptake value.
- No non-carbon material is measured in the paper.

## Coding decisions

- Samples: S1 = GS (label from the Fig. 3a legend, the first legend showing the sample; no table reports its uptake), S2 = BP280 (Fig. 3b legend).
- Temperatures 77 K and 87 K are printed in the Fig. 4 legends and Table 3, so `temperature_inferred = false` (the text says liquid nitrogen and liquid argon baths).
- Basis: excess named and defined via Gibbs's definition and Eq. (1) -> `basis_stated = true`, `basis_inferred = excess`, `uptake_type = excess`.
- Method: volumetric, Micromeritics 3Flex -> `volumetric_sieverts`, `instrument_identified = true`. Helium is listed among the gases used, but the free-volume determination is not described -> `calibration_described = false`.
- Replicates: the text says the mean of three measurements was used, with no individual results or uncertainty -> `replicates_reported = false`.
- Degassing: two steps under vacuum (363.15 K for 3 h, then 423.15 K for 12 h); the final step is recorded (150.0 C, 12 h). No end pressure ("ultra-high vacuum").
- H2 purity: "ultra-high-purity grade", no number -> `h2_purity_pct` empty.
- Surface area probe gas: the paper does not name the gas next to the BET area, but its only physisorption characterization is Ar at 87 K (Fig. 2), from which the PSD and pore volumes in Table 2 were obtained by DFT -> `surface_area_probe_gas = Ar`, `pore_volume_probe_gas = Ar`, `pore_volume_method = DFT`. BET range and consistency criteria not stated.
- GS class: rGO-derived graphene sheets -> `reduced_graphene_oxide`, `synthesis_method = thermal_reduction` (thermally expanded r-GO). EDS shows Nb 4.14 at%, P 3.24 at%, Cl 0.12 at%, O 13.62 at%; the paper calls the contamination an impurity and identifies no phase, so not coded composite; Nb recorded in `residual_metal_element` (wt% not given). No deliberate dopant.
- BP280: commercial graphitized thermal carbon black from Cabot Corporation -> `synthesis_method = commercial`, `material_class = other`, H2O2 wash in `purification_method`.
- Digitized pressures converted from kPa to bar (x 0.01); wt% computed as W1 = 0.201588 x mmol/g.
