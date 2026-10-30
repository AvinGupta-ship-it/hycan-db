# HYC-0102 extraction log (extractor A)

Rows written: 6 (M1-M5 digitized from Figure 5; M6 text value). All belong to one sample, HYC-0102-S1 (acid/baked ozonized SWNTs, legend label "4").

## Extracted

- Figure 5 (p. 24815), 77 K isotherm of "4", blue diamonds: 5 markers counted on the plot, 5 extracted (M1-M5), archive `digitizations/fig5_series4_markers.json`.
  - Axes calibrated on page image main-4.png (150 dpi) from pixel centroids: x = 0 bar at 188.33 px, 30 bar at 599.50 px; y = 0.00 wt% at 736.37 px, 3.00 wt% at 502.75 px. Third ticks: 10 bar at 325.01 px (predicted 9.973, 0.27% error), 1.50 wt% at 619.83 px (predicted 1.4965, 0.23% error).
  - Colour #282b74, tolerance 40, `--mode markers`, ROI x 189-599, y 503-655. The first run with the full plot area returned 6 points; the sixth (3.596 bar, 0.794 wt%) is the legend symbol "4", so the ROI was cut above it and the run repeated. The first marker overlaps the red fit line (100 px against 123-134 px for the others), and its centroid may be shifted slightly.
  - The archive status stays "unchecked": `digitize_figure.py check` needs a printed value inside the digitized range, and the only printed value for this sample is 3 wt% at 30 bar, outside it (3.228 bar highest marker; the command refused x = 30).
  - No desorption branch is shown; no marker is hidden that I could see.
- Abstract, text p. 24815 (Results and Discussion) and Conclusion: "3 wt % hydrogen uptake at 77 K and 30 bar" for acid/baked ozonized SWNTs 4, Figure 5 cited. One row (M6), `text_direct`, `value_kind = fitted_extrapolated` because the plotted markers stop at 3.228 bar and only the Langmuir-Freundlich fit line reaches 30 bar. It is not within 2% or 0.02 bar of any plotted point. It carries I1 because the paper cites Figure 5 for it. The same statement in the abstract, text and conclusion is one value.

## Seen, not extracted

- Figure 5 red Langmuir-Freundlich (LFI) fit line (no markers): not digitized. It is a model fitted to the markers, not a measured isotherm; the markers are the isotherm. Its end at 30 bar is covered by the text value (M6). If the reconciler wants the fit digitized, it spans roughly 0 to 30 bar.
- Text p. 24815: "nearly 25% greater than a previously reported value (~2.4 wt%) recorded under identical conditions for purified SWNTs [ref. 29, Panella, Hirscher, Roth, Carbon 2005, 43, 2209]". Not extracted: it is another group's literature benchmark on a sample the paper does not describe, not a measurement of any sample in this paper, and the "purified SWNTs" of ref. 29 are not stated to be the purified SWNTs of Table 2 (680 m2/g). It would be a row of the cited paper, not of this one. Borderline under the "values reported before" rule: if the reconciler reads that rule as covering it, the row would be 2.4 wt%, approximate, 77 K, 30 bar ("identical conditions"), no area (`surface_area_method = not_reported`), measuring laboratory not stated in this paper, no isotherm_id.
- Tables 1 and 2 and the SSA text: samples with characterization but no H2 uptake value, so no rows.
  - Purified SWNTs (HiPco, purified per Chiang et al., ref. 24): N2 BET 680 m2/g after drying at 110 C (Table 2). The acid/bake treatment of unfunctionalized SWNTs raises the area "by nearly 20%"; no number is printed.
  - 1 (n-butyl SWNTs): TGA weight loss 15%, C/functional group 27:1; SSA 410 m2/g (110 C), 770 m2/g after acid/bake.
  - 2 (1-adamantyl SWNTs): 25%, 30:1; SSA 269 m2/g.
  - 3 (-CH2CH2CH2CH2CO2H SWNTs): 10%, 74:1; SSA 410 m2/g.
  - 4 as prepared (ozonized SWNTs, before acid/bake): 23%, 4:1; SSA 381 m2/g. This is a different treatment state from the H2 sample (S1).
  - 5 (epoxidized SWNTs): 30%, 5:1; SSA 200 m2/g, 366 m2/g after acid/bake.
- Figures 1-4 (Raman spectra, SEM, AFM, length histogram): no H2 values.
- Introduction and references: no numerical H2 uptake values are given there.

## Coding decisions worth a second look

- Sample label "4": from the Figure 5 legend (no table reports its uptake). The text calls it "acid/baked ozonized SWNTs 4" and "pretreated ozonized SWNTs 4"; Tables 1 and 2 use "4" for the unbaked tubes.
- `measuring_lab_id = Simpson group, NREL`: the paper says the H2 measurements were made at NREL, but no author is affiliated there. The Acknowledgment thanks Drs. L. J. Simpson and M. J. Heben (NREL) for the hydrogen uptake experiments, and ref. 28 (the instrument reference) has Simpson first. The rule's "co-author affiliated there" cannot be applied.
- `basis_stated = false`, `uptake_type = unspecified`, `basis_inferred = excess` by the instrumental default for a volumetric measurement; `measurement_method = volumetric_sieverts` from "volumetric hydrogen capacity measurements".
- `wt_pct_convention = unknown`: only wt% is printed.
- Temperature 77 K is a printed number (Figure 5 caption, text), so `temperature_inferred = false`; "liquid nitrogen temperatures" appears only in the Experimental Section.
- `area_same_sample = yes`: "Hydrogen uptake measurements were carried out with the pretreated ozonized sample (4) with a SSA of 1068 m2/g." `bet_range_stated = false` (only "multipoint regression of nitrogen-BET"), `bet_consistency_criteria_stated = false`.
- Degassing: the paper gives drying at 110 C before BET and degassing at 80 C for TGA; nothing for the H2 run, so the degas fields are empty.
- Activation: the acid/bake treatment (called "exfoliation" in the paper) is recorded in `activation_method` because it is the paper's treatment to raise surface area; `synthesis_method = hipco`; functional groups of the baked sample are not stated (Scheme 1 draws an epoxide-type oxygen for the unbaked 4), so `functional_groups` is empty.
- Sample numbering counts only samples that carry rows.
