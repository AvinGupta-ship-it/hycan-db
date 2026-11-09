# HYC-0053 extraction log (agent B)

Rows written: 1110 (54 table values, 1 text value, 1055 digitized points). Temperature -196 °C stored as 77.15 K. Lab: Matsutaka group, RIKEN (corresponding author, first affiliation RIKEN Baton Zone Program; no other laboratory named for H2).

## Sources extracted
- Abstract/text p. 22392–22399 (main-02..main-09): 2.8 wt% and 20.3 g-H2 per L (abstract), 2.55, 2.54, 2.80, 2.68–2.80, 2.35 wt% (text) — merged into the rows of the table values they restate; CA-4700 3.9 wt% (text p. 22393) extracted as a literature row (previously reported, ref. 27).
- Table 1 (main-04): 7 H2 uptakes (Char/KOH series) with SBET, Vtotal, QSDFT micropore volume.
- Table 2 (main-06): 5 H2 uptakes (heating-time series).
- Table 3 (main-11): 4 samples, gravimetric uptakes; volumetric uptakes and bulk densities for the two pellets.
- Table 4 (main-12) / Table S8 (si1-20): ZTC/rGO 22.4 (total, 5 bar), ZTC 38 (20 bar), ACM-2 29.7 (40 bar) g-H2 per L extracted as previously reported literature rows; CA carbon 20.3 and ZIF-8 carbon 11.6 merged into the Table 3 pellet rows.
- Tables S1–S4 (si1-07, si1-08, si1-10, si1-12): flow-rate, temperature, K2CO3 and CTA series. Table S1 0.1 L/min and Table S2 700 °C rows = Table 1 1 : 2 sample (identical values); Table S2 600 °C row = Table 2 2 h sample.
- Tables S5, S6 (si1-15..si1-17): all pellet and powder rows with an uptake; rows already in Table 3 (S5 No. 1, 3; S6 No. 1, 3) and S5 No. 4 (= Table 1 1 : 2) merged. Tables S5/S6 print no conditions; -196 °C and 1 bar taken from the Fig. 9 caption (which plots these data) and the main text.
- Table S7 (si1-18): V0.6–1.0 nm and V0.6–0.7 nm put in notes of the four Table 3 samples (not ultramicropore volumes: a 0.6–0.7 nm slice, not a cumulative volume below a cutoff).
- Figures digitized (77 K H2 isotherms): Fig. 1c/1d, Fig. 2c/2d, Fig. 8e, 8f, Fig. S4a/b, S5c/d, S7c/d, S8c/d, S9c/d, S11c/d. Archives in digitizations/ (one per series per panel).

## Digitization method
- Page images are 150 dpi. Axes calibrated on located ticks (pixel rows/columns inspected), third labelled tick as verification (all within 0.4%). The 0 tick of every linear pressure axis except Fig. 8e/8f and Fig. S9c is hidden under data markers, so those axes are calibrated on 0.2 and 1.2 bar and verified on 0.6 bar. Log axes calibrated on the decade ticks (10^-5 or 10^-4 and 10^0) and verified on 10^-2.
- Legend boxes and panel letters were painted white in a work copy of each page (work/masked/, pixel coordinates unchanged) so legend markers are not extracted. For black series on SI pages, the black inward tick marks were also painted white (…_ticks.png).
- digitize_figure.py extract --mode markers, colour tolerance 60, 2-px opening (removes 1-px connecting lines). Each isotherm is plotted twice (linear and log pressure axis): markers above 0.11 bar are taken from the linear panel, below 0.11 bar from the log panel; a marker resolved only in the other panel is added if no point within 0.03 wt% / 0.15 decade exists (linear-panel fill-ins below 0.06 bar rejected for pressure precision). Blobs larger than 1.45× the series single-marker size are overlapping markers and were not extracted (listed below).
- Hollow (adsorption) markers in Fig. 8e/8f, S9c/d and S11c/d are thin rings that colour isolation cannot separate from the connecting lines, and a 2-px opening removes them. Their centres were located by painting the enclosed interior of each ring (white region enclosed by the series colour, ≤40 px, ≤8 px across) into a work copy (work/scripts/fillrings.py, work/masked/*_holes.png) and running digitize_figure.py markers mode on that copy (1-px opening, 2-px minimum). Rows from these archives have confidence 2. Rings overlapped by other markers are not recoverable. Filled markers in these figures are desorption points (captions of Fig. 8 legend and Figs. S9, S11).
- Tool check (digitize_figure.py check at 1 bar against the table value, 5% tolerance) passed for every linear archive that reaches 1 bar; it could not be run for Char/KOH 1/1.5 (Fig. 1), 600 °C 30 min and 8 h (Fig. 2), 0.5 L/min (Fig. S4), CTA 600 °C 2 h (Fig. S8), CA carbon powder des. (Fig. 8f) and 200 °C pellet (Fig. S9), whose markers near 1 bar are hidden behind other series. Fig. S11 PVP K90: digitized ~1.87 wt% at 1 bar vs printed 1.79 (4%).
- Table 1-bar values were not merged with plotted points: no adsorption point lies within 0.02 bar of 1 bar (points at about 0.95 and 1.05 bar); the printed values equal linear interpolation between those points within 0.01 wt%, so they are coded value_kind = unclear without isotherm_id. Fig. S11 PEO has a desorption point at 0.981 bar (1.510 wt%), within 0.02 bar; not merged because it is on the desorption branch.
- isotherm_point_count is the number of markers established (extracted + estimated count in overlapping blobs + fragments) for both branches; markers fully hidden behind other series are not counted, so counts are lower bounds.

## Same run plotted in several figures (digitized once)
- Table 1 Char/KOH 1 : 2 isotherm (I5) = Fig. S4 "0.1 L/min" = Fig. S5 "700 °C 2h" = Fig. S9 "powder" (CA batch 2): digitized points coincide within 0.01 wt% and 0.002 bar at every high-pressure point. Adsorption taken from Fig. 1 only; desorption (filled squares) taken from Fig. S9. Archives figS4a/b_0.1 and figS5c/d_700 kept for the comparison only.
- Fig. 2 "600 °C 2h" = Fig. S5 "600 °C 2h" (I9): each marker taken once from whichever figure resolves it.
- Fig. 8f CA carbon powder/pellet = CA batch 1 powder and 150 °C PVA pellet (Table 3); Fig. 8e = ZIF-8 carbon batch 1 powder and 150 °C pellet; Fig. S11 = CA batch 3 powder and pellets (caption says "CA batch 3 in Table S4", meaning Table S5).
- Fig. S9 75 °C and 150 °C pellets mapped to Table S5 No. 5 and 6 (10 mg/mL PVA), not No. 10 and 11 (5 mg/mL); the legend does not say which.

## Markers not extracted (not separable or not recoverable)
- I2 (fig1_1-0.5): merged blob of ~2 overlapping markers at 0.008099 bar, 0.566 wt% (not separable)
- I2 (fig1_1-0.5): merged blob of ~2 overlapping markers at 0.02501 bar, 0.873 wt% (not separable)
- I2 (fig1_1-0.5): merged blob of ~5 overlapping markers at 0.0402 bar, 1.026 wt% (not separable)
- I3 (fig1_1-1): merged blob of ~2 overlapping markers at 0.0202 bar, 0.711 wt% (not separable)
- I3 (fig1_1-1): merged blob of ~3 overlapping markers at 0.04581 bar, 0.999 wt% (not separable)
- I5 (fig1_1-2): merged blob of ~2 overlapping markers at 0.01467 bar, 0.511 wt% (not separable)
- I5 (fig1_1-2): merged blob of ~3 overlapping markers at 0.0456 bar, 0.904 wt% (not separable)
- I5 (figS9des_powder): merged blob of ~2 overlapping markers at 0.0429 bar, 0.877 wt% (not separable)
- I5 (figS9des_powder): merged blob of ~2 overlapping markers at 0.42 bar, 2.184 wt% (not separable)
- I5 (figS9des_powder): occluded marker fragment (6 px) at 0.01242 bar, 0.477 wt% (centre not recoverable)
- I6 (fig1_1-3): merged blob of ~3 overlapping markers at 0.04696 bar, 0.734 wt% (not separable)
- I7 (fig1_1-4): merged blob of ~2 overlapping markers at 0.0153 bar, 0.355 wt% (not separable)
- I7 (fig1_1-4): merged blob of ~3 overlapping markers at 0.04709 bar, 0.658 wt% (not separable)
- I8 (fig2_30min): merged blob of ~2 overlapping markers at 0.04995 bar, 0.820 wt% (not separable)
- I9 (figS5_600): merged blob of ~2 overlapping markers at 0.01461 bar, 0.575 wt% (not separable)
- I9 (figS5_600): merged blob of ~2 overlapping markers at 0.02416 bar, 0.728 wt% (not separable)
- I9 (figS5_600): merged blob of ~3 overlapping markers at 0.0465 bar, 0.978 wt% (not separable)
- I11 (fig2_8h): merged blob of ~2 overlapping markers at 0.01013 bar, 0.486 wt% (not separable)
- I11 (fig2_8h): merged blob of ~2 overlapping markers at 0.01514 bar, 0.588 wt% (not separable)
- I11 (fig2_8h): merged blob of ~2 overlapping markers at 0.04934 bar, 0.975 wt% (not separable)
- I12 (fig2_12h): merged blob of ~3 overlapping markers at 0.0465 bar, 0.698 wt% (not separable)
- I13 (figS4_0.06): occluded marker fragment (6 px) at 0.1065 bar, 1.230 wt% (centre not recoverable)
- I14 (figS4_0.3): merged blob of ~2 overlapping markers at 1.045 bar, 2.630 wt% (not separable)
- I16 (figS4_1.0): occluded marker fragment (6 px) at 0.0006216 bar, 0.086 wt% (centre not recoverable)
- I16 (figS4_1.0): occluded marker fragment (6 px) at 0.0009512 bar, 0.075 wt% (centre not recoverable)
- I16 (figS4_1.0): occluded marker fragment (6 px) at 0.003283 bar, 0.241 wt% (centre not recoverable)
- I16 (figS4_1.0): occluded marker fragment (6 px) at 0.008606 bar, 0.397 wt% (centre not recoverable)
- I17 (figS4_1.5): merged blob of ~2 overlapping markers at 0.01513 bar, 0.477 wt% (not separable)
- I17 (figS4_1.5): merged blob of ~4 overlapping markers at 0.04434 bar, 0.790 wt% (not separable)
- I17 (figS4_1.5): merged blob of ~2 overlapping markers at 0.0665 bar, 0.943 wt% (not separable)
- I19 (figS5_800): merged blob of ~3 overlapping markers at 0.0435 bar, 0.630 wt% (not separable)
- I21 (figS7_700): merged blob of ~2 overlapping markers at 0.04864 bar, 0.960 wt% (not separable)
- I21 (figS7_700): occluded marker fragment (6 px) at 0.3708 bar, 1.980 wt% (centre not recoverable)
- I22 (figS7_800): merged blob of ~5 overlapping markers at 0.04714 bar, 0.798 wt% (not separable)
- I22 (figS7_800): occluded marker fragment (6 px) at 0.0006952 bar, 0.053 wt% (centre not recoverable)
- I23 (figS8_600-2h): merged blob of ~9 overlapping markers at 0.03495 bar, 0.847 wt% (not separable)
- I24 (figS8_600-8h): merged blob of ~2 overlapping markers at 0.01476 bar, 0.486 wt% (not separable)
- I24 (figS8_600-8h): merged blob of ~3 overlapping markers at 0.0459 bar, 0.856 wt% (not separable)
- I25 (figS8_700-2h): merged blob of ~2 overlapping markers at 0.04949 bar, 0.807 wt% (not separable)
- I26 (fig8ads_CApowder): occluded marker fragment (2 px) at 0.04741 bar, 0.658 wt% (centre not recoverable)
- I26 (fig8ads_CApowder): occluded marker fragment (3 px) at 0.3793 bar, 1.822 wt% (centre not recoverable)
- I26 (fig8ads_CApowder): occluded marker fragment (4 px) at 0.515 bar, 2.055 wt% (centre not recoverable)
- I26 (fig8des_CApowder): merged blob of ~3 overlapping markers at 0.03172 bar, 0.550 wt% (not separable)
- I27 (fig8ads_CApellet): merged blob of ~5 overlapping markers at 0.05206 bar, 0.953 wt% (not separable)
- I27 (fig8des_CApellet): merged blob of ~2 overlapping markers at 0.01093 bar, 0.585 wt% (not separable)
- I27 (fig8des_CApellet): merged blob of ~2 overlapping markers at 0.1026 bar, 1.354 wt% (not separable)
- I28 (fig8ads_ZIFpowder): merged blob of ~4 overlapping markers at 0.2581 bar, 1.507 wt% (not separable)
- I28 (fig8des_ZIFpowder): merged blob of ~2 overlapping markers at 0.2063 bar, 1.369 wt% (not separable)
- I28 (fig8des_ZIFpowder): merged blob of ~2 overlapping markers at 0.3127 bar, 1.643 wt% (not separable)
- I28 (fig8des_ZIFpowder): merged blob of ~2 overlapping markers at 0.9423 bar, 2.498 wt% (not separable)
- I29 (fig8ads_ZIFpellet): merged blob of ~2 overlapping markers at 0.1537 bar, 1.044 wt% (not separable)
- I29 (fig8des_ZIFpellet): merged blob of ~2 overlapping markers at 0.01109 bar, 0.283 wt% (not separable)
- I30 (figS9ads_75): merged blob of ~2 overlapping markers at 0.3649 bar, 1.701 wt% (not separable)
- I30 (figS9ads_75): merged blob of ~2 overlapping markers at 0.5188 bar, 1.871 wt% (not separable)
- I32 (figS9des_200): merged blob of ~2 overlapping markers at 0.006418 bar, 0.383 wt% (not separable)
- I32 (figS9des_200): merged blob of ~2 overlapping markers at 0.01742 bar, 0.584 wt% (not separable)
- I32 (figS9des_200): merged blob of ~2 overlapping markers at 0.3421 bar, 1.414 wt% (not separable)
- I32 (figS9des_200): merged blob of ~2 overlapping markers at 0.6588 bar, 1.646 wt% (not separable)
- I33 (figS9des_250): merged blob of ~2 overlapping markers at 0.4576 bar, 1.421 wt% (not separable)
- I33 (figS9des_250): merged blob of ~2 overlapping markers at 0.9468 bar, 1.656 wt% (not separable)
- I33 (figS9des_250): merged blob of ~3 overlapping markers at 1.046 bar, 1.687 wt% (not separable)
- I34 (figS9ads_300): merged blob of ~2 overlapping markers at 0.0001504 bar, 0.028 wt% (not separable)
- I34 (figS9ads_300): merged blob of ~2 overlapping markers at 0.003213 bar, 0.221 wt% (not separable)
- I34 (figS9ads_300): merged blob of ~2 overlapping markers at 0.1553 bar, 1.110 wt% (not separable)
- I34 (figS9ads_300): merged blob of ~2 overlapping markers at 0.2078 bar, 1.214 wt% (not separable)
- I34 (figS9ads_300): merged blob of ~2 overlapping markers at 0.5196 bar, 1.525 wt% (not separable)
- I34 (figS9ads_300): merged blob of ~2 overlapping markers at 0.8341 bar, 1.684 wt% (not separable)
- I35 (figS11des_powder): merged blob of ~2 overlapping markers at 0.524 bar, 2.157 wt% (not separable)
- I36 (figS11des_MC): merged blob of ~2 overlapping markers at 0.8456 bar, 2.097 wt% (not separable)
- I40 (figS11ads_HPC): merged blob of ~2 overlapping markers at 0.2615 bar, 1.357 wt% (not separable)
- I40 (figS11ads_HPC): merged blob of ~2 overlapping markers at 0.3664 bar, 1.510 wt% (not separable)
- I40 (figS11des_HPC): merged blob of ~3 overlapping markers at 0.371 bar, 1.569 wt% (not separable)
- I40 (figS11des_HPC): merged blob of ~2 overlapping markers at 0.4864 bar, 1.686 wt% (not separable)
- figS9des_300: point at 0.9155 bar, 1.672 wt% dropped (non-monotonic in its branch; probable misassigned or partly occluded marker)
- figS11des_PEO: point at 0.03884 bar, 0.459 wt% dropped (non-monotonic in its branch; probable misassigned or partly occluded marker)
- figS11des_HPC: point at 0.8817 bar, 1.995 wt% dropped (non-monotonic in its branch; probable misassigned or partly occluded marker)
- Further markers are completely hidden behind other series (no pixels of their colour visible), notably: Char/KOH 1/1.5 and 1/1 (Fig. 1) under the 1/2, 1/3 and 1/4 series; 600 °C 2h (Fig. 2) under the other heating times; 0.5 L/min (Fig. S4, only 3 markers visible) and 0.3 L/min under 1.0 and 0.1 L/min; the last points (about 1.05 bar) of 600 °C 30 min and 8 h (Fig. 2); most hollow adsorption markers of the ZIF-8 powder/pellet (Fig. 8e), the 200 °C and 250 °C pellets (Fig. S9) and the CA batch 3 powder (Fig. S11), which lie under the filled desorption markers.

## Values seen but not extracted
- Table 4 / Table S8 MOF and MOF-composite pellets (SNU-70, MOF-5/ENG, MOF-5, MOF-177 incl. 25.8 at ~60 bar, UiO-66, UiO-66/PIM-1, HKUST-1, MIL-101(Cr)): not carbon sorbents.
- Cover page (main-01) "20 g-H2/L at -196 °C and 1 bar": same measurement as 20.3 (CA carbon pellet).
- Text p. 22400 "below approximately 1.8 wt%" (pellets pressed above 150 °C) and p. 22401 "approximately 14–17 g-H2 per L" (PVP and HPC pellets): summaries of several samples already in Table S5. Percentage reductions (-15 wt%, -1 wt%, -61%, -43 wt%, Table 3/S5/S6 parentheses): derived from two samples, not uptake values.
- Fig. 4 and Fig. S3 (H2 uptake vs CO2 uptake) and Fig. 9 (volumetric uptake vs bulk density): not isotherms; every plotted H2 value is in Tables 1, 2, S5, S6.
- Table S5 No. 12 (CA batch 2 pellet, PVA 3 mg/mL): no pellet formed, no data.
- N2 (Figs. 1a, 2a, 5a, 8a, 8b, S5a, S7a, S8a, S9a, S11a), CO2 (Fig. 3) isotherms, pore size distributions (Figs. 1b, 2b, 3b/d, 5b, 8c/d, S5b, S7b, S8b, S9b, S11b) and Fig. S6 pore-section volumes: not H2 data. Yields: not recorded.
- Fig. 5 (N2 only) samples are the Table S1 samples.

## Coding notes
- Labels: the row-identifier cell(s) of the first table reporting the uptake, joined by spaces where the row has several (Table S4 "600 2"; Table S5/S6 "CA batch 2 Pellet (75 °C) PVA"). Table S2 "800" (KOH) and Table S3 "800" (K2CO3) are different samples with the same printed label; descriptions distinguish them.
- CA batch 3 powder (SBET 2396, 2.66 wt%) resembles Table 1 1 : 3 (2400, 2.66, same activation conditions) but the paper does not link them; kept separate.
- Pellets coded composite (polymer binder ~10–15 wt%). ZIF-8-derived carbon coded other (carbonized MOF, composition not reported). Synthesis of CA carbons: carbonization (hydrothermal carbonization of CA at 250 °C, 1 h); KOH/K2CO3 activation in activation_method.
- Basis never named for this work's values; volumetric instrument (BELSORP-Max II) gives basis_inferred excess. No free-volume or helium calibration, sample degassing, sample mass or H2 purity stated (the 300 °C, >1 h, <1 Pa treatment is of the blank tube). No uncertainties or repeat measurements reported.
- Volumetric uptakes (g-H2 L-1) stored as volumetric_capacity_kg_m3 with basis packing_volume (they equal gravimetric uptake × pellet bulk density within rounding) and bulk density in packing_density_g_cm3.
- Literature rows (CA-4700, ZTC/rGO, ZTC, ACM-2) carry "previously reported" notes; their laboratory institution is not printed in this paper.
