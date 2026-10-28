# HYC-0060 extraction log (extractor B)

Zlotea et al. 2009, Int J Hydrogen Energy 34:3044-3057, a Round Robin on one commercial carbon (Takeda CMS 4A) measured by 14 anonymised laboratories. The input is 14 main-article page images. The supplementary file (Tables 1-4) is cited but is not in the input. 144 rows, one sample (HYC-0060-S1, label "CMS 4A"), 139 digitization archives.

## Sources extracted from

- Table 1 (p. 3049): per-participant method, temperatures, sample density and its method, initial mass, weight loss, outgassing pressure, equilibrium time, temperature stability, EOS, transducer accuracy and H2 purity. These go into each laboratory's rows. The table has no uptake values.
- Sec. 3.1 (p. 3045): commercial CMS 4A from Takeda Chem. Ind., Japan (synthesis_method commercial, material_identity).
- Sec. 3.2 (p. 3046): BET 423 (+-20) m2/g from N2 at 77 K; DR micropore volume 1.7 (+-0.1) e-4 m3/kg = 0.17 cm3/g (also stated as 0.17 cm3/g in Sec. 7.2.1). These are on every row.
- Sec. 6 and 7.1.2 (p. 3048): degassing protocol of 383 K for 24 h then 523 K for 4 h under dynamic vacuum, followed by all participants. Coded degas 249.85 C, 4 h, with the 24 h step in notes; end pressure per laboratory from Table 1.
- Sec. 4.1 (p. 3046): "corresponds to an excess adsorption", which names the basis without defining it. Coded basis_stated false, basis_inferred excess and uptake_type excess on all rows.
- Abstract (p. 3044), Sec. 7.2.1 (p. 3050), Sec. 9 (p. 3055): 1.40(+-0.1) wt% at 1 MPa and 77 K, the group 1 reference (isotherms 3, 6, 7, 11). One row (M140).
- Sec. 7.2.2 (p. 3050): limiting content 1.1 wt% of PCI curves 8a and 8b, no pressure stated. One row (M143).
- Sec. 7.2.3 (pp. 3050-3051): isotherm 1 "around 2.6 wt.% at 8 MPa" is merged with the last isotherm 1 marker (M17). Isotherm 12 "around 1.9 wt.% at 2 MPa" is merged with the last isotherm 12 marker (M113).
- Sec. 7.2.4 (p. 3051): isotherm 13 "1.4 wt.% at 1.5 MPa" is merged with the last isotherm 13 marker (M127). Isotherm 2 "transitory plateau at 1.25 wt.% at around 2 MPa" is merged with the 1.91 MPa marker (M23). Isotherm 2 "second plateau of 1.4 wt.% at pressure above 3 MPa", stated twice, is its own row with pressure unstated (M144).
- Abstract, Sec. 7.4.1 (p. 3052), Sec. 9 (p. 3056): ambient group 1 reference (isotherms 3, 7, 9, 11) of 0.07(+-0.01) wt% at 1 MPa and 0.12(+-0.01) wt% at 2 MPa (M141, M142). The temperature is unstated because the four isotherms span 294-301 K.
- Sec. 7.4.4 (p. 3052): isotherm 5 "almost 0.7 wt.% at 6 MPa" is merged with its highest-pressure marker (M133, coded approximate).
- Fig. 5 (p. 3051): every separable 77 K marker at or below 2.5 MPa, 102 archives (see the isotherm list below).
- Fig. 4 (p. 3050): 77 K markers above 2.5 MPa, which Fig. 5 does not show (isotherms 1, 2 and 3), 25 archives.
- Fig. 8 (p. 3053): highest-pressure point of ambient isotherms 1, 2, 3, 4b, 5, 8b, 9 and 14.
- Fig. 9 (p. 3053): highest-pressure point of ambient isotherms 4a, 6, 7 and 11. These end below 3 MPa, so Fig. 9's finer scale was used.

## Isotherm ids

- 77 K: I1 = participant 1 (square), I2 = 2 (circle), I3 = 3 (up-triangle), I4 = 6 (down-triangle), I5 = 7 (diamond), I6 = 8a (half-filled circle), I7 = 8b (filled circle), I8 = 10 (hexagon), I9 = 11 (star), I10 = 12 (pentagon), I11 = 13 (asterisk).
- Ambient: I12 = 1, I13 = 2, I14 = 3, I15 = 4a, I16 = 4b, I17 = 5, I18 = 6, I19 = 7, I20 = 8b, I21 = 9, I22 = 11, I23 = 14 (Table 1 temperatures).
- Points extracted per 77 K isotherm: I1 17, I2 16, I3 8, I4 13, I5 6, I6 1, I7 4, I8 19, I9 15, I10 14, I11 14.

## Digitization method

- Calibration ticks (page pixels, subpixel centres of the tick marks):
  - Fig. 4: x 0 at 341.66 and 10 at 899.01, check 5 at 620.56; y 0.0 at 1465.79 and 3.0 at 1061.35, check 1.5 at 1263.14.
  - Fig. 5: x 0.0 at 185.25 and 2.5 at 555.79, check 1.0 at 333.29; y 0.0 at 414.36 and 1.4 at 223.00, check 0.7 at 318.42.
  - Fig. 8: x 0 at 361.25 and 22 at 914.42, check 10 at 612.49; y 0.0 at 548.15 and 0.7 at 162.61, check 0.3 at 383.13.
  - Fig. 9: x 0.0 at 190.00 and 3.0 at 524.70, check 1.5 at 357.48; y 0.05 at 1377.00 and 0.20 at 1179.81, check 0.10 at 1311.00.
- All four figures are monochrome. The eleven 77 K series differ only by marker shape and the tool isolates by colour, so each marker was digitized in its own run: `digitize_figure.py extract --mode markers --color #000000 --tolerance 400 --open-px 1 --marker-min-px 8`, with `--roi` set to that marker's bounding box. The box positions came from template matching against in-plot exemplar markers and from inspection of pixel dumps. Every run returned exactly one marker, so the count check is one marker per ROI. That gives one archive per marker rather than one per series, named `HYC-0060_<fig>_<isotherm id>_m<nn>.json`; ambient ones are `..._last.json`.
- Fig. 5 points above its highest labelled y tick (1.4 wt%) are extrapolated along the linear axis and are flagged outside_axis_range in their archives. Five markers shown in both figures were digitized from Fig. 4 as a check: isotherm 1 at 1.30, 1.82 and 2.29 MPa, the isotherm 12 top and the isotherm 10 top. Fig. 4 and Fig. 5 agree within 0.02 MPa and 0.007 wt%. These check archives are in the work directory and are not rows.
- Overlapping markers were digitized with the other marker's pixels inside the box and get extraction_confidence 2. Half-filled markers (8a in Fig. 5; ambient 11 and 14) have their dark-pixel centroid shifted toward the filled half by about 1-1.4 px. This is noted on those rows.

## Values seen but not extracted

- Figs. 4/5: all markers below about 0.1 MPa lie in a vertical stack of all eleven 77 K isotherms and cannot be separated, assigned or counted. For that reason isotherm_point_count is empty on every row.
- Fig. 5: isotherm 1 markers between 0.1 and 0.45 MPa are hidden in the 1.2-1.4 wt% band.
- Fig. 5: isotherm 3 markers other than those at 0.6, 1.48 and 1.97 MPa are hidden under the markers of isotherms 6, 7 and 11. A possible triangle near 1.0 MPa was ambiguous and was skipped.
- Fig. 5: isotherm 6 markers near 1.07 and 1.3 MPa and below 0.4 MPa are covered by stars, asterisks and diamonds (weak template match).
- Fig. 5: the isotherm 7 diamond near 1.4 MPa (weak match) and diamonds below 0.5 MPa are covered.
- Fig. 5: the isotherm 13 asterisk near 0.4 MPa is covered by the 0.38 MPa filled circle of 8b.
- Fig. 5: isotherm 10 hexagons below about 0.2 MPa merge with other markers.
- Fig. 5: the 8a markers other than the one at 0.106 MPa are all inside the stack.
- Fig. 4: markers at or below 2.5 MPa are the same data replotted in Fig. 5 and were taken from Fig. 5 only, so they are not duplicated.
- Figs. 8/9: all points of the twelve ambient isotherms except each one's highest-pressure point (protocol Sec. 9).
- Fig. 2: TPD-MS of H2O and CO2 during outgassing. Not H2 uptake.
- Fig. 3: weight loss against outgassing pressure. Not H2 uptake.
- Figs. 6 and 10: standard deviation of hydrogen content against pressure. These are interlaboratory statistics, not a sample's uptake.
- Figs. 7 and 11: interlaboratory consistency h. Not uptake.
- Sec. 7.2.1: "(1.45 wt.%) ... Takeda CMS 4A material at 77 K and 2 MPa [25]". A literature value from ref. 25, not measured here.
- Sec. 7.4.1: "0.1 wt.% at 2 MPa ... Takeda CMS 4A material [25]". A literature value from ref. 25.
- Sec. 7.2.1: "plateau of around 1.4 (+-0.1) wt.% ... for higher pressure". The same group 1 value as the 1 MPa reference, so it is part of row M140.
- Sec. 7.4.1: "overlapping within maximum 0.01 wt.%". A difference between curves, not an uptake.
- Sec. 7.4.3: "lower hydrogen capacity by around 0.02 wt.% at 2 MPa" (isotherm 6). A difference, not an uptake.
- Sec. 7.4.4: "curve 2 shows almost no uptake". Qualitative.
- Secs. 7.3 and 7.5: maximum relative standard deviations of 14% and 36%. Statistics.
- Sec. 3.2: Grande et al. macropore 3.1e-4 and micropore 1.7e-4 m3/kg (ref. 24). Literature characterization.
- Sec. 7.1.3: mean sample density 1.99e3 (+-0.38e3) kg/m3. A statistic across laboratories; the per-laboratory densities are in skeletal_density_g_cm3.
- Sec. 7.2.3: the second isotherm 10 run at 24 ml/min is mentioned but not plotted, so there are no values.
- Supplementary Tables 1-4 (interpolated uptakes at fixed pressures and h values): not in the input.
- Non-carbon materials (Amendment 1): Pd, LaNi5 and sea sand are named only as calibration references. No values are reported, so nothing to list.

## Coding decisions

- One sample, because all laboratories measured the same commercial material under the same degassing protocol (Sec. 11.0 definition). The participant is identified by measuring_lab_id, isotherm_id and notes.
- material_class is other: a carbon molecular sieve whose activation is not stated.
- measuring_lab_id uses the paper's anonymous participant codes, because the paper withholds which institution is which. 4a/4b and 8a/8b are each one laboratory with two instruments. Consensus rows name the group members.
- Participant 10 used a dynamic volumetric method at 50 ml/min, coded measurement_method other and measurement_mode flow.
- sample_mass_mg is Table 1's initial (pre-outgassing) mass. skeletal_density_g_cm3 is Table 1's He-based sample density. It is left empty where an assumed carbon density was used (4a, 4b, 13) or none was reported.
- calibration_described is true for participants 1, 3, 5, 6, 7, 11 and 12, which report a sample density from He expansion, a He isotherm or He pycnometry. It is false for 2, 4a/4b, 8a/8b, 9, 10, 13 and 14; for 13 the paper says the buoyancy correction is "not accurately described". instrument_identified is false everywhere, because no make or model is given.
- replicates_reported is true: the same sample was measured independently by eleven (77 K) and twelve (ambient) laboratories, and the paper reports interlaboratory standard deviations.
- Text values merged with a plotted marker keep the text value at the marker's pressure. The digitized value is given in that row's notes. M113 ("around 1.9") differs from the digitized 1.947 wt% by more than 1% of the axis span, but the text explicitly describes the end of isotherm 12 at 2 MPa.
- Group 1 consensus values, the 8a/8b limiting content and the isotherm 2 plateau have value_kind unclear, because none of them identifies a single measured point.
