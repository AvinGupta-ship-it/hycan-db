# HYC-0113 extraction log (agent B)

Wang et al. 2012, J. Mater. Chem. 22, 23893. One carbon sorbent has H2 data: HPCDCM (sample S1). 53 rows.

## Sources extracted from

- main-1, Abstract: "2.4 wt% and 4.4 wt% at 1 bar and 36 bar" at -196 °C; "11.6 g L-1 at 36 bar". Used in M11 (1 bar) and M24 (36 bar, volumetric capacity).
- main-5, p. 23897, right column: "~24 mg g-1 is obtained in the HPCDCM at 1 bar" (isotherm "shown in Fig. 8a"). Recorded in the notes of M11; the paper prints the same point as 2.4 wt%.
- main-6, p. 23898, left column: "maximum Gibbs excess amount adsorbed is 44 mg H2 g-1 at 36 bar"; bulk density "0.264 g cm-3"; "11.6 g L-1". Used in M24.
- main-6, Conclusions: 2.4 wt% at -196 °C and 1 bar; "saturated hydrogen uptake of up to 4.4 wt%" at 36 bar; 11.6 g L-1. Same values as M11 and M24.
- main-2/main-3, Sections 2.2 and 2.3: degassing at 150 °C in vacuum overnight; N2 at -196 °C on an Autosorb 1C; BET range p/p0 = 0.05-0.2; NLDFT/QSDFT; V_total at p/p0 = 0.98; H2 instruments (Autosorb 1C at ambient pressure; BELSORP-HP up to 100 bar, about 0.2 g, He volume calibration at 25 °C and -196 °C, "Gibbs excess"). Coded on every row.
- main-4, Table 2, HPCDCM row: S_BET 2933, V_micro 0.981 (QSDFT, slit pores), V_total 2.101, D_meso 3.1 nm. Coded on every row.
- main-5, text: EDX Cl ~4.3 wt% in HPCDCM (in notes; residual chlorine, not coded as a dopant); micropore size ~0.9 nm (in notes).
- main-6, Fig. 8a (I1, 77.15 K, 0-1 bar, magenta circles): counted 11 markers, extracted 11. Axis calibration: x 0.0 at px 179 and 1.0 at px 529, checked against 0.6 at px 389 (error 0); y 0 at px 664 and 30 at px 507, checked against 10 at px 611.5 (error 0.3%). Points 1-10 are M1-M10. Point 11 (0.9957 bar, 24.17 mg/g) is the same measurement as the text value at 1 bar, so it is merged into M11. Tool check: 24 mg/g at 0.995 bar passes (+0.7%). Archive: digitizations/fig8a_HPCDCM_77K_ambient.json.
- main-6, Fig. 8b, adsorption (I2, filled red squares): before extraction, the legend markers were blanked in a work copy of the page (main-6_fig8b_legend_masked.png, rectangle x 390-525, y 780-822; page coordinates unchanged). Axis calibration: x 0 at px 196.5 and 100 at px 546, checked against 40 at px 336 (error 0.2%); y 0 at px 863 and 40 at px 749, checked against 20 at px 806 (error 0). 26 single markers were extracted (5.4-100.7 bar). The marker at 36.338 bar (44.035 mg/g) is merged into M24 (printed value 36 bar is within 2%); the other 25 are M12-M23 and M25-M37. Tool check: 44 mg/g at 36 bar passes (+0.05%). The tool flags 17 points as extrapolations because they lie above the highest labelled y tick (40 mg/g, up to 44.04 mg/g) or beyond x = 100 (100.7 bar). The axis is linear, so these values are kept. Archive: digitizations/fig8b_HPCDCM_77K_highP_adsorption.json.
- main-6, Fig. 8b, desorption (I2, open blue squares): the open markers sit underneath the red adsorption markers and the red line, so they are partly covered. Colour isolation with the tool (#818ebc, tolerance 50, --open-px 0 or 1) produced only fragments and frame pixels, so those runs were discarded. Marker centres were located by occlusion-aware template matching (work/scripts/find_open_squares_v2.py). Outlines of 7 or 8 px were tried. Blue outline pixels count toward the score, red pixels count as neutral (covering), and white outline pixels count against. A candidate was accepted if it scored at least 4, had at least 6 blue outline pixels, and showed at least two edges with 3 or more blue pixels each. 16 candidates were accepted, and each was checked on a 6x overlay (work/open_squares_v2_overlay_*.png). Each accepted centre was painted as a solid block on a copy of the page with the panel blanked (work/main-6_fig8b_desorption_centres.png, same page coordinates) and digitized with digitize_figure.py using the same calibration. The tool reproduces every template centre exactly. These are M38-M53. The paper states no desorption value, so the archive status is "unchecked". Archive: digitizations/fig8b_HPCDCM_77K_highP_desorption.json.

## Markers seen but not separated (no rows)

- Fig. 8b adsorption, low-pressure pile: a solid red column at px x 193-202, y 810-864 (p about 0-0.6 bar, 0 to about 19 mg/g). It contains an unknown number of overlapping markers: at least 7 (55 px tall, markers 7-8 px). The tool rejected it as too large (352 px).
- Fig. 8b adsorption, cluster: a solid red shape at px x 200-211, y 772-787 (about 2.0-3.1 bar, about 27.7-30.7 mg/g). It contains at least 2 overlapping markers; its stepped edges suggest 4-5. The tool rejected it as too large (115 px).
- Fig. 8b desorption, markers that are covered:
  - Near 86 bar (px about 497.5, 754.5): only right-edge and bottom-edge fragments are visible. Score 3.7, below the acceptance threshold.
  - Near 90.5 bar: only one edge is visible.
  - Near 95.7 and 100.7 bar: hidden under the adsorption markers.
  - Near 10 bar, and on the lower-left edges of the adsorption markers from about 12 to 32 bar: only 1-px blue slivers are visible.
  - Probably near 51 and 65 bar: the desorption pressure sequence has gaps there.
  - Possibly more under the low-pressure pile and the cluster.
  - Their number cannot be determined.
- isotherm_point_count for I2 is therefore a lower bound: 51 = 26 adsorption + 16 desorption separated markers + at least 2 (cluster) + at least 7 (pile).

## Coding decisions

- Basis:
  - I1 (Autosorb 1C): no basis is named. basis_inferred = excess by the volumetric default (Fig. 8 caption: "volumetric hydrogen measurements"); uptake_type = unspecified.
  - I2: the paper names "Gibbs excess" (Section 2.3 and p. 23898) without defining it, so basis_stated = false, basis_inferred = excess and uptake_type = excess. The quote is kept in basis_evidence.
- wt% convention for M11 and M24 is W1, inferred from paired units:
  - 24 mg/g gives W1 2.4 wt% and W2 2.34 wt%, which would print as 2.3.
  - 44 mg/g gives W1 4.4 wt% and W2 4.21 wt%.
  - Digitized rows: the axis is in mg/g, so uptake_wt_pct = 0.1 x mg/g (W1, computed_from_other_unit), with the digitized mg/g value in notes.
- The 1 bar text value is merged with the Fig. 8a marker, not with any Fig. 8b point, because the text says it comes from Fig. 8a.
- The 36 bar maximum is value_kind = measured: it is merged with a plotted adsorption point and lies within 0.1% of it.
- M24 volumetric capacity: 11.6 g L-1 is stored as 11.6 kg m-3, basis packing_volume (excess uptake x calculated bulk density 0.264 g cm-3), excluding compressed gas. packing_density 0.264 is carried on every row as a sample property.
- instrument_identified:
  - I1: true (Quantachrome Autosorb 1C).
  - I2: false. The model "BELSORP-HP" is printed without a manufacturer.
- calibration_described:
  - I1: false (nothing stated).
  - I2: true (He measurement at 25 °C and -196 °C).
- sample_mass_mg = 200 for I2 only ("about 0.2 g").
- degas_duration_h is left empty because "overnight" is not a number.
- replicates_reported = false: there are no error bars, no ± values and no repeated isotherm.
- Pressures are used as printed. The paper does not say whether they are absolute or gauge.

## Values seen but not extracted

- p. 23894 (introduction): OM-CDC saturated H2 excess 48-51 mg g-1 and microporous CDC 39 mg g-1 (ref. 28). From another paper.
- p. 23898: OM-CDC powder 48-52 mg g-1 (ref. 28); microporous CDC powder 39.3 mg H2 g-1 (ref. 28); ordered mesoporous carbons 2.7 wt% at -196 °C and 60 bar (ref. 44) and 2.9 wt% at -196 °C and 30 bar (ref. 28). From other papers, not measured here.
- Table 2 rows for samples with no H2 uptake, none of them carbon sorbents:
  - KIT-6 silica: d211 10.0 nm, a0 24.4 nm, S_BET 609, V_micro 0.003, V_total 1.345, D_meso 9.5.
  - SiC/KIT-6: 8.7, 21.2, 293, 0.050, 0.161, 2.5-3.6.
  - OMSCM (SiC): 8.7, 21.2, 642, 0.134, 0.535, 3.1. Its PSD peaks are 3.10, 1.85 and 0.96 nm (text).
- Table 1 (shape and volume reduction): PCS-800/KIT-6 10 / 3.1 / 243.4 / -; SiC/KIT-6 8.9 / 2.9 / 180.3 / 25.9; OMSCM 8.9 / 2.9 / 180.3 / 25.9; HPCDCM 8.1 / 2.5 / 128.7 / 47.1 (mm, mm, mm3, %). No H2 values.
- Fig. 2 (TG/DTG of HPCDCM in air): ~17 wt% moisture loss up to 140 °C, ~82% combustion at 400-750 °C, residue below 1 wt% at 750 °C. Fig. S1 (TG of OMSCM): about 82% mass retained at 800 °C. No H2 values.
- Fig. 3 (XRD), Fig. 4 (N2 isotherms and PSD), Fig. 5 (SEM), Fig. 6 (TEM), Fig. 7 (Raman), Fig. S2 (HPCDCM cumulative pore volume and PSD): characterization only, no H2 values.
