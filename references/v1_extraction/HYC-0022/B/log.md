# HYC-0022 extraction log (agent B)

## Sources extracted
- main p2, Table 1: textural parameters of AC, AC-C2, AC-C4, AC-K3 and AC-K5 (BET with range 0.02-0.25, Vt, Vmeso, Vmicro by DR, V<1nm by HK, D_BJH, D_HK, packing density). These go on every uptake row of each sample. Carbon yields (62, 49, 53, 43%) are not schema fields and were not stored.
- main p2, Characterization text: N2 at 77 K on a Micromeritics ASAP 2020; H2 measured volumetrically (ASAP 2020, 0-1 bar, 77 K) and gravimetrically (Rubotherm, 1-20 bar, 77 K).
- main p3-p4 text: 1-bar capacities AC-K5 2.49, AC-K3 2.23, AC-C2 1.70, AC-C4 1.27, AC 1.23 wt%. Each is merged with the last Figure 4 point of its isotherm (digitized pressure 0.979-0.982 bar after P/P0 conversion; checked against the archive and passed).
- main p5, Figure 4: volumetric H2 isotherms at 77 K, 0-1 bar, x-axis P/Po. All five series digitized (archives fig4_*.json). Pressure is stored as P/P0 x 1 bar because the caption gives the range as 0-1 bar; P0 is not otherwise stated.
- main p5, Figure 7: gravimetric isotherms at 77 K, 1-20 bar, 11 markers per series. AC, AC-C2, AC-C4, AC-K3 and AC-K5 digitized (fig7_*.json). The G212 series here is the same run as SI Figure S2, so it was digitized from S2 only.
- main p6, Table 2: AC-K3 5.63 and AC-K5 7.08 wt% at 20 bar ("this work"), each merged with the 20-bar Figure 7 point (check passed).
- main p6 text and Conclusions: AC-K5 7.08 wt% at 77 K and 20 bar, and a volumetric capacity of 43.2 g L-1 (packing density x gravimetric value). Both are on the AC-K5 20-bar Figure 7 row, with volumetric basis packing_volume.
- SI p2-p3: Rubotherm procedure with blank and He buoyancy measurements; eq 5 defines W_ADS(%) = dm/m_S x 100% (W1 stated). The buoyancy correction gives basis_inferred = excess for the gravimetric rows.
- SI p4, text and Figure S1: G212 volumetric isotherm at 77 K, 0-1 bar; 1.77 wt% at ~1 bar is merged with the last point (check passed). G212 area of 1409 m2/g and pore volume of 0.69 cm3/g; no method is given.
- SI p5, text and Figure S2: G212 gravimetric isotherm, 1.80 wt% at about 1 bar and 3.88 wt% at about 20 bar, merged with the first and last points (check passed). The main p5 text cites the same two values for Figure 7.
- SI p6, Figure S3: four repeated AC-K5 gravimetric isotherms (First, Second, Third, Fourth), digitized as separate isotherms I13-I16.

## Digitization details and markers not separated
- All axes were calibrated on the lowest and highest labelled ticks, with tick pixels found from row and column profiles, and checked on a third tick. Every residual is below 0.25%.
- All figures are greyscale with overlapping series. Each series was isolated into its own black-on-white image in the work directory, built from the page pixels with band boundaries placed in the gaps between chains, and digitize_figure.py was run on that image. Each archive records the isolated image as its source.
- Figure 4, all series: markers below P/P0 ~0.11 overlap into solid bands and cannot be separated or counted. They are not extracted, and isotherm_point_count is empty for I1-I5.
- Figure 4, AC-K5 and AC-K3: between P/P0 ~0.40 and ~0.62 the two chains cross and overlap. About 10 markers of each series there could not be separated and are not extracted.
- Figure 4, AC-K5 and AC-C2: one merged pair each near P/P0 0.35 was separated with a 1-px diagonal cut.
- Figure 4, AC: adjacent open squares touch, so each marker is taken as the enclosed interior of its square (centroid = square centre). The legend square is excluded.
- Figure 4, AC-C4: the tool's 3-px opening removed the AC square outlines. The first marker in the archive (px 229) is an incomplete fragment at the band edge and is excluded from the rows. Two triangles (near P/P0 0.15 and 0.35) are hidden under squares and not extracted.
- Figure 7: the AC and AC-C4 markers at 2 and 4 bar coincide (one blob). The merged centroid is recorded for both series, with extraction_confidence 2.
- Figure S1: the low-pressure band (P/P0 < ~0.11) is not separable and was rejected by size. One touching marker pair near P/P0 0.35 was cut. 43 points are digitized, plus the merged 1.77 value; isotherm_point_count is empty.
- Figure S3: the First marker at 14 bar is occluded by the Third marker. Second markers at 12-20 bar are hidden under other series; 6 Second markers are extracted and its point count is left empty. The First run matches the Figure 7 AC-K5 series within about 1% and may be the same run; the paper does not say, so both are kept.
- Archives without a stated value to check (the Figure S3 series, Figure 7 AC, AC-C2 and AC-C4) remain status "unchecked". The other Figure 4 and Figure 7 archives, plus Figures S1 and S2, passed checks against printed values.

## Values seen but not extracted
- Table 2 literature comparison values, not measured in this work: AX-21 (AC) 2800 m2/g, 4.6 wt% (10 bar), ref 34; KUA-6 (AC) 3808, 5.6 (40 bar), ref 35; Maxsorb-3000 (AC) 3178, 5.2 (40 bar), ref 35; CB850h (TC) 3150, 6.9 (20 bar), ref 6; TC 2535, 5.3 (20 bar), ref 7.
- Mokaya group's value for G212-type comparison, 3.96 wt% at 77 K and 20 bar (main p5, SI p5, ref 6 / SI ref 1): a literature value.
- Figure 5 (pore volumes vs. H2 sorption at 1 bar): not an isotherm. It repeats the 1-bar values and the Table 1 volumes, so it adds no new value.
- Figure 6 (isotherms normalized to the 1-bar capacity, W/Wo): no uptake values, so not digitized. P1/2 is discussed qualitatively only.
- Figure 8 (20-bar uptake vs. S_BET and vs. Vmicro): not an isotherm; it repeats the 20-bar values.
- Figure 9 (H2 uptake/S_BET, x10^-2 mmol m-2, vs. R value): not an isotherm. Its per-area values are derived from the 20-bar uptakes and Table 1 areas, and are not given in the text.
- Figure 1 (XRD, R values AC 1.9, AC-C2 2.2, AC-C4 2.0, AC-K3 1.7, AC-K5 ~1): R is not a schema field. No interlayer spacing is printed.
- Figure 3 (N2 isotherms): characterization only.
- Degassing "below 1.33 Pa at 363 K for 1 h and heated to 623 K for at least 6 h" (main p2) is stated for the N2 isotherm. The paper does not say it applies to the H2 measurements, so the degas fields are left empty.
- "The amount of the sample used was about 0.3-0.6 g" refers to the packing-density measurement, not H2, so sample_mass_mg is empty.
