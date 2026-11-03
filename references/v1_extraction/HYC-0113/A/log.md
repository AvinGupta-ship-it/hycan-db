# HYC-0113 extractor A log

Sources read: main.txt (text layer) and page images main-1 to main-7, si1.txt and si1 page images. The text layer drops minus signs and tildes ("196 C" is -196 C, "24 mg g-1" is ~24 mg g-1, "4.3 wt%" is ~4.3 wt%); the page images were used to confirm them.

## Extracted from

- Abstract (p. 23893), Conclusions (p. 23898): 2.4 wt% at 1 bar and 4.4 wt% at 36 bar, -196 C, and 11.6 g L-1 at 36 bar. Rows M11 (1 bar) and M24 (36 bar, with volumetric capacity 11.6 kg m-3, basis packing_volume).
- Results p. 23897: "~24 mg g-1 at 1 bar", Fig. 8a. Same measurement as M11; the mg/g value is in M11 notes (no mg/g field).
- Results p. 23898: "maximum Gibbs excess amount adsorbed is 44 mg H2 g-1 at 36 bar" (Fig. 8b), bulk density 0.264 g cm-3, 11.6 g L-1. Same measurement as M24; 44 mg/g in M24 notes; 0.264 g cm-3 in packing_density_g_cm3 on every row.
- Table 2 (p. 23896), HPCDCM row: S_BET 2933 m2 g-1, V_micro 0.981 cm3 g-1 (QSDFT, slit pores, equilibrium model), V_total 2.101 cm3 g-1 (p/p0 = 0.98), D_meso 3.1 nm. Sec. 2.2 (p. 23894): N2 at -196 C, Quantachrome Autosorb 1C, BET p/p0 = 0.05-0.2, degassed overnight at 150 C. Carried on every row.
- Sec. 2.3 (p. 23894-23895): BELSORP-HP, up to 100 bar, about 0.2 g, He at 25 C and -196 C for vessel volume and sample volume. Carried on the I2 rows.
- Fig. 8a (p. 23898), 11 markers, archive `digitizations/fig8a_HPCDCM_77K_ambient.json` (tool check at 0.9957 bar vs stated ~24 mg/g: 24.172, 0.72%). Rows M1-M10 digitized; marker 11 (0.9957 bar, 24.172 mg/g) merged with the printed 2.4 wt% at 1 bar (row M11, isotherm I1).
- Fig. 8b (p. 23898), adsorption branch (filled red squares), 26 resolved markers, archive `digitizations/fig8b_adsorption.json` (tool check at 36 bar vs stated 44 mg/g: 44.019, 0.04%). Rows M12-M23 and M25-M37 digitized; marker 13 (36.43 bar, 44.035 mg/g) merged with the printed 4.4 wt% / 44 mg/g at 36 bar (row M24, isotherm I2). Printed pressure 36 is within 0.72 bar of 36.43, the next markers are at 31.7 and 41.2 bar.

## Decisions

- Samples: only HPCDCM has an H2 uptake, so it is HYC-0113-S1 (KIT-6, SiC/KIT-6 and OMSCM have no row).
- Two isotherms: I1 = Fig. 8a (Autosorb 1C, ambient pressure), I2 = Fig. 8b (BELSORP-HP, 0-100 bar). Separate instrument runs, so separate isotherm ids.
- I1: basis not named, `uptake_type = unspecified`, `basis_inferred = excess` by the volumetric default (Fig. 8 caption calls it a volumetric measurement). I2: "Gibbs excess amount" is named, not defined, so `basis_stated = false`, `uptake_type = excess`, `basis_inferred = excess`.
- wt% convention: for 2.4 wt% vs ~24 mg/g and 4.4 wt% vs 44 mg/g only W1 matches the printed rounding (W2 would be 2.34 and 4.21), so `inferred_from_paired_units`, W1. Digitized points are in mg/g on the axis, stored as W1 = 0.1 x mg/g with `computed_from_other_unit`.
- `average_pore_diameter_nm` left empty: the paper gives two distribution modes (micropore 0.9 nm, mesopore 3.1 nm), not an average. Both are in notes.
- Cl ~4.3 wt% (EDX) is residual from chlorination, not an introduced dopant: `material_class = carbide_derived_carbon`, no dopant fields, value in notes.
- `instrument_identified`: I1 true (Quantachrome Autosorb 1C); I2 false (BELSORP-HP printed without a manufacturer). `calibration_described`: I2 true (He volumes), I1 false (nothing stated for the Autosorb).
- `isotherm_point_count`: I1 = 11 (all markers separated). I2 = 26 is a lower bound (resolved adsorption markers only), see below.
- Figure calibration: Fig. 8a x 0.0 -> px 179, 1.0 -> px 529, check 0.6 -> px 389 (0.6); y 0 -> px 664, 30 -> px 507, check 10 -> px 611.5 (10.03). Fig. 8b x 0 -> px 196, 100 -> px 546, check 60 -> px 406.5 (60.14); y 0 -> px 863, 40 -> px 749, check 20 -> px 806 (20.00). Image: pages/main-6.png. The tool flags 17 Fig. 8b points as outside the calibrated range because the highest labelled y tick is 40 and the highest labelled x tick is 100; the data reach 44.0 mg/g and 100.7 bar. The scales are linear and the unlabelled minor ticks agree (y 10, 30 and 50 mg/g at px 834.5, 777.5 and 720.5; x 10 and 30 bar at px 231 and 301), so these are readings on the printed scale.
- ROI for the Fig. 8b adsorption run is x 181-563, y 722-780 px, chosen to exclude the legend markers (legend square at about px 414, 792). The legend marker therefore is not in the archive.

## Markers not separated or not extracted (Fig. 8b)

- Adsorption markers at the lowest pressures merge into a solid red column (px x 193-201, y 810-865: about 0-1.4 bar, 0-19 mg/g). The count of markers in it cannot be determined. It lies below the ROI and is not in the archive.
- A second merged group of at least two adsorption markers (px x 199-210, y 770-790: about 1-4 bar, 26-33 mg/g) was rejected by the tool as too large (68 px inside the ROI, 121 px in full); it cannot be split.
- The desorption branch (open blue squares, 1 px outline) was not digitized. In markers mode on the blue colour the tool returned outline fragments (top and bottom edges as separate "markers", 3-12 px, tested at tolerance 25-70 and opening 0 and 1), not marker centres, and the open squares are partly hidden under the filled adsorption squares and the red line. About 13 open squares can be distinguished between 34 and 92 bar and several more below 17 bar. No value was read by eye. The text says the desorption branch is consistent with the adsorption branch and shows no hysteresis.
- Because of these, I2 `isotherm_point_count = 26` counts only the resolved adsorption markers.

## Seen, not extracted

- Intro (p. 23893-23894): OM-CDC 2200-2600 m2 g-1, 48-51 mg g-1 (ref. 28); microporous CDC 1578 m2 g-1, 39 mg g-1 (ref. 28). Other materials from another paper.
- Results p. 23898: OM-CDC powder 48-52 mg g-1 (ref. 28); microporous CDC powder 39.3 mg H2 g-1 (ref. 28); ordered mesoporous carbons from MCM-48 and SBA-15: 2.7 wt% (-196 C, 60 bar, ref. 44) and 2.9 wt% (-196 C, 30 bar, ref. 28). Literature values for other materials.
- Table 2: KIT-6 (S_BET 609, V_micro 0.003, V_total 1.345, D_meso 9.5), SiC/KIT-6 (293, 0.050, 0.161, 2.5-3.6), OMSCM (642, 0.134, 0.535, 3.1). Characterization only, no H2 uptake, and not carbon sorbents (silica, SiC/silica, SiC).
- Table 1 (monolith dimensions and volume change), Fig. 2 and SI Fig. S1 (TG), Fig. 3 (XRD), Fig. 4 and SI Fig. S2 (N2 isotherms and pore size distributions), Figs. 5-7 (SEM, TEM, Raman): no H2 uptake values.
- Raman D/G peaks, TG moisture loss (~17 wt%) and residual mass (<1 wt% at 750 C): not H2 uptake.
