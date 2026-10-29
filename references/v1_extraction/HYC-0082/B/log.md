# HYC-0082 extraction log (agent B)

Paper: Kostoglou et al. 2021, Chem. Eng. J. 427, 131730. Input: 10 page images (main-01 to main-10), no supplementary file.
Samples: S1 = PDAC (polyaniline-derived activated carbon), S2 = YP80F (commercial, Kuraray). Both are carbon sorbents; no non-carbon material is measured.
Rows written: 152.

## Sources extracted from

- main p.7 Table 3 (excess gravimetric and volumetric H2 capacities): all 7 rows extracted (C_n mmol/g, C_g wt%, C_v g/L); each merged with the plotted point it matches (Fig. 3a or 3c).
- main p.7 Table 3 footnote: defines C_g = m_gas/(m_gas + m_solid), i.e. wt% convention W2, applied to every wt% value of the paper (the paired C_n values match W2 within rounding, not W1, e.g. 8.2 mmol/g gives 1.63 wt% W2 / 1.65 wt% W1, printed 1.6; 28.7 mmol/g gives 5.47 W2 / 5.79 W1, printed 5.5). Validator warning on M131 (23.5 mmol/g vs 4.5 wt%) is this W2 convention (W2 4.52, W1 4.74).
- main p.7 Table 2, row "2021 / Polyaniline-derived activated carbon / This work" (5.5/0.6 wt% at 58/80 bar): same values as Table 3, recorded on the Table 3 rows.
- main p.5-7 text, sec. 3.3: ~2.5/~1.6/~1.1 wt% at ~1 bar (77/90/100 K), ~5.5 wt% at ~58 bar, ~39.6 g/L, ~4.5 wt% at ~47 bar (YP80F), ~29.8 g/L, ~0.6/~0.5 wt% at 298 K and ~80 bar: same measurements as Table 3, recorded on those rows. "~0.13 wt% versus ~4.55 wt% at ~10 bar" (PDAC 298 K and 77 K, describing the Fig. 3c inset): two text_direct rows (M97 and the I4 row at 10 bar). "~28 mmol/cm3 at ~58 bar and ~21 mmol/cm3 at ~47 bar" (uptake normalized to the QSDFT pore volume): stored as adsorbed_phase_density_kg_m3 (x 2.01588) on the Table 3 rows PDAC 77 K 58 bar and YP80F 77 K 47 bar.
- main p.1 abstract and p.9 conclusions: ~5.5 wt% at 77 K and ~60 bar, ~2.5 wt% at 77 K and ~1 bar: same as Table 3 rows.
- main p.3 sec. 2.2: instruments, degassing, sample masses, H2 purity, He free-volume calibration.
- main p.4-5 Table 1 and sec. 3.1-3.2: characterization (QSDFT Ar 87 K areas and volumes, d50, SAXS, skeletal and poured densities), carried on every row.
- main p.6 Fig. 3a (low-pressure isotherms, PDAC): 77 K both branches digitized; 90 K and 100 K highest-pressure marker digitized (merged with Table 3).
- main p.6 Fig. 3c main panel (high-pressure isotherms): PDAC 77 K and YP80F 77 K both branches digitized; PDAC 298 K and YP80F 298 K highest-pressure marker digitized (merged with Table 3).
- main p.6 Fig. 3c inset (0-10 bar, adsorption only): digitized for PDAC 77 K and YP80F 77 K; used only for 3 markers the main panel cannot give (PDAC 0.38 bar/2.40 wt% hidden behind a YP80F marker in the main panel; YP80F 0.44 and 1.27 wt%, whose main-panel markers sit on the y axis and digitize below 0 bar), and for the digitized point quoted in the notes of the "~4.55 wt% at ~10 bar" row.

## Values seen but not extracted

- Table 2, literature values for other papers' materials (no sample of this paper): phenolic resin-derived activated carbon fibers 77 K 40 bar 1.65-3.45 wt% [50]; polypyrrole-derived activated carbons 77 K 20 bar 4.24-7.03 [51]; polythiophene-derived activated carbons 77 K 20 bar 4.55-5.71 [52]; polyaniline-derived activated carbon tubes 77/298 K 50/75 bar 3.3-5.2/0.38-0.62 [31]; iron-loaded polyaniline-derived activated carbons 77/298 K 60/80 bar 5.3-6.2/0.6-0.85 [30]; mesoporous polymer-derived activated carbons 77 K 20 bar 3.04-4.77 [53]; PVDC-derived activated carbon 77 K 20 bar 4.85 [54]; polymer-derived activated hard carbons 298 K 100 bar 0.3-0.4 [55]; hyper-crosslinked polymer-derived porous carbon 77 K 30 bar 4.7 [56].
- Text p.6-7 "~0.013 mmol/m2 at ~58 bar" (PDAC) and "~0.012 mmol/m2 at ~47 bar" (YP80F): uptake divided by the QSDFT surface area, a normalization of the recorded uptake, not a film/supported-sample areal uptake; not stored.
- Fig. 3d (uptake / QSDFT surface area vs pressure, 77 and 298 K, with inset): a normalized replot of the Fig. 3c isotherms; not digitized. Its values are not given elsewhere except the two maxima above.
- Fig. 3b (isosteric heat vs loading, Virial fit): not an isotherm; shows Qst ~8.3 kJ/mol at zero coverage falling to ~6.6 kJ/mol at ~5.5 mmol/g. The loading values carry no temperature or pressure; no H2 uptake row.
- Text ratios and relative values: uptake at ~1 bar decreases by ~55% from 77 to 100 K; uptake at 77 K increases 2.2 times from ~1 to ~58 bar; excess drops by 2% (PDAC) and 4% (YP80F) at ~80 bar relative to the maximum; PDAC stores 35 times less H2 at 298 K than at 77 K at ~10 bar. Derived from recorded values; not rows.
- Qst ~8.3 kJ/mol (this work), ~9.2 kJ/mol (activated carbon cloth, ref. [8]), 5-8 kJ/mol (literature range): not uptake values.
- Chahine rule (1 wt% at 77 K and ~35 bar per 500 m2/g or 0.2 cm3/g) and DOE targets (5.5 wt%, 0.04 kg H2/L): not measurements.
- Fig. 3a 90 K and 100 K markers other than the highest-pressure one, and Fig. 3c 298 K markers other than the highest-pressure one: not digitized (other temperatures, highest point only).
- Fig. 3c inset markers other than the three used: same runs as the main-panel markers, so not digitized separately as rows.
- Fig. 2 (Raman, SAXS, Ar isotherms at 87 K, QSDFT PSD), Fig. 1 (schematic, SEM), Fig. 4 and Table 4 (supercapacitor data): not H2 uptake. Characterization from them is on the rows (Table 1 values, La ~5.1/~4.4 nm, d50).
- N content 0.5-2.3 wt% (XPS) quoted for similar PANi-derived carbons from ref. [29], not measured here: not coded as a dopant (noted on S1 rows).
- No value is said to be previously reported; no multi-laboratory or consensus value.

## Digitization

Calibration (page px, main-06.png, tick centroids from pixel rows/columns):
- Fig. 3a: x 0 mbar = 214.0 (axis line), 1000 mbar = 583.02, check 500 mbar = 397.9 (0.33% error); y 0 = 448.36 (axis line), 2.5 wt% = 155.37, check 1.0 = 331.4 (0.20%).
- Fig. 3c main: x 0 bar = 214.55 (axis line), 80 bar = 593.2, check 40 bar = 403.39 (0.26%); y 0 = 823.78, 6 wt% = 518.82 (frame lines), check 3 = 671.52 (0.14%).
- Fig. 3c inset: x 0 = 409.66 (axis line), 10 bar = 577.0, check 5 = 493.0 (0.39%); y 0 = 754.46, 5 = 624.49 (frame lines), check 2 = 702.0 (0.91%).
Pressures read in mbar (Fig. 3a) are converted to bar.

Image preparation (files in the work directory; each archive records its source image and sha256):
- main-06_fig3a_legendmasked.png: Fig. 3a legend (page px x 218-345, y 156-226) painted white so the legend symbols are not read as data.
- main-06_fig3c_masked.png: Fig. 3c legend (x 240-352, y 684-766) and the inset with its labels (x 372-592, y 614-790; x 372-400, y 608-614) painted white for the main-panel series.
- Open (desorption) markers have the colour of the filled markers. They were isolated on copies of the page in which the series' filled markers (3x3 opening, dilated 1 px) and, in Fig. 3c, the error bars on them were painted white, and all other colours removed: main-06_fig3a_desorb.png, main-06_fig3c_pdac77_desorb.png, main-06_fig3c_yp77_desorb.png. A marker partly hidden by a filled marker gives the centroid of its visible arc (bias up to ~2 px, below 1% of the axis span); such rows (fewer than 15 pixels) have extraction_confidence 2. Components under 10 pixels are fragments and are not rows.

Archives in digitizations/ and marker accounting:
- fig3a_PDAC_77K_adsorption.json: 34 components. Points 1-32 single markers (rows). Point 0 (8.9 mbar) is part of a blob of >=6 overlapping markers at P < ~13 mbar (also overlapping the 90/100 K markers): not separable, no row. Point 33 (997 mbar, 2.475 wt%) is a cluster of >=3 overlapping markers at ~0.97-1.01 bar: not separable; quoted in the notes of the Table 3 row at 1 bar (2.5 wt%), which is the same measurement per text sec. 3.3.
- fig3a_PDAC_77K_desorption.json: 16 open markers. Point 2 (239 mbar, 8 px, mostly hidden behind an adsorption marker): no row. 15 rows. Further open markers may be hidden in the blob and the 1-bar cluster.
- fig3a_PDAC_90K_highest.json: rightmost marker overlaps its neighbours; region limited to it (x >= 584 px), centroid approximate (1.009 bar, 1.615 wt%).
- fig3a_PDAC_100K_highest.json: rightmost marker, separate (1.012 bar, 1.104 wt%).
- 90 K and 100 K point counts: filled markers counted with the digitizer (90 K: 25 single plus clusters of >=4, >=3, >=4; 100 K: 23 single plus clusters of >=6, >=4); open markers fragment too much to count reliably and are not included, so 36 and 33 are lower bounds.
- fig3c_PDAC_77K_adsorption.json: 36 components. Point 0 (0.999 wt%) is partly hidden behind a YP80F marker in the main panel and in the inset and digitizes to -0.12 bar: no row. A marker at ~2.4 wt% is hidden behind a YP80F marker in the main panel: row from the inset (point 1). Point 10 (9.78 bar, 4.563 wt%) merged into the text row "~4.55 wt% at ~10 bar"; point 29 (58.15 bar, 5.467 wt%) merged into the Table 3 row at 58 bar. Point 35 (81.2 bar) is the highest-pressure marker, beside the frame.
- fig3c_PDAC_77K_desorption.json: 10 open markers (rows). Four more open markers are partly hidden and not separable: between filled markers 6 and 7 (~4 bar), behind marker 17 (~23 bar), right of marker 18 (~26 bar), right of marker 21 (~33 bar). Point count 51 = 37 filled + 14 open (lower bound).
- fig3c_YP80F_77K_adsorption.json: 47 components. Points 0-2 sit on the y axis and digitize to -0.011 bar: point 2 (0.438 wt%) and point 0 (1.265 wt%) replaced by inset points 1 and 2; point 1 (0.891 wt%) is below 0 bar in the inset too: no row. Point 23 (22.5 bar) and point 46 (80.3 bar) are pairs of overlapping filled markers: no rows (so the highest-pressure marker, ~80 bar, has no row). Point 34 (46.86 bar, 4.534 wt%) merged into the Table 3 row at 47 bar. A YP80F marker may be hidden under the 298 K markers at the origin (not counted).
- fig3c_YP80F_77K_desorption.json: 14 components; points 0, 2, 5, 6, 12 (8-9 px, partly hidden open markers at ~21, 29, 43, 48, 66 bar): no rows; 9 rows. Point count 63 = 49 filled + 14 open (lower bound).
- fig3c_PDAC_298K_highest.json (79.72 bar, 0.594 wt%) and fig3c_YP80F_298K_highest.json (80.06 bar, 0.478 wt%): merged with the Table 3 rows at 80 bar. 298 K counts: PDAC 18 (markers separable at P >~ 34 bar; low-pressure markers hidden behind YP80F markers), YP80F 43 (35 single, one overlapping pair, low-pressure cluster of >=6); lower bounds.
- The PDAC 298 K marker at ~10 bar (for the "~0.13 wt%" text row) is hidden behind a YP80F 298 K marker in the inset; no digitized point.
- fig3c_inset_PDAC_77K_adsorption.json (11 markers; the ~1.0 wt% marker is hidden behind a YP80F marker) and fig3c_inset_YP80F_77K_adsorption.json (17 markers).
- digitize_figure.py check: passed for Fig. 3c PDAC 77 K adsorption (58 bar, 5.5 wt%), YP80F 77 K adsorption (47 bar, 4.5 wt%), Fig. 3a 77 K adsorption (cluster at 0.997 bar vs 2.5 wt%), 90 K and 100 K highest (vs 1.6 and 1.1 wt%), 298 K highest (vs 0.6 and 0.5 wt%), inset PDAC (9.76 bar vs 4.55 wt%). The two 77 K desorption archives of Fig. 3c were checked against the Table 3 values at 58 and 47 bar on the paper's statement that the isotherms are fully reversible (passed). fig3a_PDAC_77K_desorption.json and fig3c_inset_YP80F_77K_adsorption.json remain unchecked: the paper states no value within their ranges.

## Coding decisions

- Basis: "excess" is named (Table 3 title, Fig. 3 caption, abstract) but not defined, so basis_stated = false, basis_inferred = excess, uptake_type = excess, for all seven isotherms (the Table 3 title covers the 1-bar values of the low-pressure isotherms).
- Low-pressure isotherms (Quantachrome Autosorb-1-MP, "using the same system" as the Ar measurements): the ~50 mg sample mass, degassing (10^-6 mbar, 250 C, 12 h) and He void-volume calculation stated in the Ar paragraph are applied to these rows (calibration_described = true); no uncertainty or repeat reported (replicates_reported = false; the statement that six PDAC replicates showed excellent reproducibility gives no results).
- High-pressure isotherms (SETARAM PCTPro-2000): error bars from three independent runs, so replicates_reported = true; the error bars are not printed numbers, so uncertainty_wt_pct is empty.
- Surface area: no BET area is reported; the headline QSDFT (Ar, 87 K) S_DFT is stored with surface_area_method = DFT and probe gas Ar; bet_range_stated and bet_consistency_criteria_stated coded false.
- measuring_lab_id: corresponding author Kostoglou, first affiliation Montanuniversität Leoben; the paper does not say the H2 measurements were made elsewhere.
- material_class activated_carbon for both (no non-carbon phase; no measured heteroatom content).
