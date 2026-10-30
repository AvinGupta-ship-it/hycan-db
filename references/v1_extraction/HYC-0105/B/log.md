# HYC-0105 extraction log (agent B, 2026-10-29)

Stelitano et al. 2020, Energies 13, 2237. 121 rows. Samples: S1 DPC, S2 ADPC0.5, S3 ADPC1, S4 ADPC3. Isotherms: I1/I3/I5 = Figure 7 (0–1 bar, ASAP 2460) for ADPC0.5/ADPC1/ADPC3; I2/I4/I6 = Figure 9 (0–80 bar, Sieverts fPcT) for ADPC0.5/ADPC1/ADPC3.

## Sources extracted

- Table 1 (main p.4): H2 uptake columns i (77 K, 1 bar) and l (77 K, 80 bar) for DPC, ADPC0.5, ADPC1, ADPC3 (8 values); SBET, VT, Vmicro, DFT ultra- and super-micropore volumes, Vmeso, Vmacro and Fmicro put on every row of each sample. The 1-bar values of the ADPC samples are merged with the highest-pressure Figure 7 point (digitized at 0.995–0.997 bar). The 80-bar values are merged with the highest-pressure Figure 9 point (digitized at 74.7–75.0 bar). They fall outside the 2% pressure window, but the text attributes the 80-bar maximum capacity to the Figure 9 isotherms ("The 77 K isotherms showed a maximum storage capacity at 80 bar (Figure 9)"), and the values agree (1.79/1.783, 5.25/5.250, 3.40/3.388).
- Table 2 (main p.12): Tóth wt%max ± 0.2 for ADPC0.5 (1.634), ADPC1 (5.435), ADPC3 (4.980). Stored as fitted_extrapolated with no pressure (pressure_unstated) and no isotherm_id, because the paper does not say which data set was fitted.
- Section 2.1–2.2 text (main p.3, p.5): synthesis, BET range 0.05–0.15, VT at P/P0 0.995 (Table 1 footnote says 0.99), DFT slit-pore model, instruments (ASAP 2460 for 0–1 bar; Sieverts' type apparatus fPcT [46] for 0–80 bar), degassing (≈473 K overnight before H2; 473 K 12 h vacuum before N2), wt% definition ("weight percent of adsorbed gas per gram of adsorbent").
- Section 3.3 text (main p.10–12) and Abstract (p.1): DPC "as low as 0.38 wt%" (row M2, pressure not printed, conflicts with Table 1 0.00 and Figure 8); ADPC1 "≈5.5 wt%" at 80 bar / "5.5 wt% at 77 K and 80 bar" / "asymptotic uptake close to 5.5 wt%" (row M81, approximate, fitted_extrapolated, conflicts with Table 1 5.25).
- Table S1 (si1 p.1): WDS composition of ADPC1 and ADPC3, in the notes of those samples' rows.
- Figure 7 (main p.10): 77 K H2 isotherms up to 1 bar, three series, all digitized (69 resolvable markers; 66 digitized rows plus 3 merged with Table 1). Archives: digitizations/fig7_ADPC1.json (24 points), fig7_ADPC3.json (23), fig7_ADPC0.5.json (22).
- Figure 9 (main p.12): 77 K H2 isotherms up to 80 bar, three series, all digitized. Archives: digitizations/fig9_ADPC0.5.json, fig9_ADPC1.json, fig9_ADPC3.json (15 points each).

## Digitization method

- Figure 7: calibration x 0.0 at px 355.55, 1.0 at px 961.68, check 0.4 at px 598.04 (error 0.02%); y 0.0 at px 1392.0, 1.6 at px 926.88, check 0.8 at px 1159.73 (error 0.12%). Tick pixels come from intensity-weighted centroids of the tick marks. Colour #000000, tolerance 60, markers mode, ROI 328 900 989 1389.
- Figure 9: calibration x 0 at px 434.32, 80 at px 871.01, check 40 at px 652.61 (error 0.03%); y 0 at px 1247.02, 6 at px 910.22, check 3 at px 1078.68 (error 0.04%). Colour #000000, tolerance 130 (the ADPC3 circles are shaded grey on their upper-left half; the grey fit lines stay excluded), markers mode, ROI 410 912 897 1273.
- All series in both figures are black, so the tool cannot separate them by colour. For each series I made an image in the work directory (work/fig7_<series>.png, work/fig9_<series>.png; script work/make_series.py) in which the other series' marker components, as found by the tool's own mask, are painted white. The tool was then run on that image with the page calibration. Each archive passed the tool's `check` step against Table 1 (Figure 7 at 0.995 bar against the 1-bar values; Figure 9 at the last plotted pressure, ~75 bar, against the 80-bar values).
- Figure 7: in every series, the touching marker pairs near 0.78/0.80, 0.85/0.87 and 0.92/0.93 bar were split with a 1-px white vertical cut at the pair midpoint; the tool did this split by itself for ADPC3 at 0.92/0.94. The extracted marker counts equal the markers counted outside the unresolved regions listed below.

## Markers seen but not extracted

- Figure 7: an unresolvable stack of overlapping markers from all three series at p ≈ 0–0.01 bar, 0.03–0.20 wt% (one merged blob). At least four ADPC3 circles show through by their highlights; the diamonds and triangles cannot be counted.
- Figure 7: a merged blob at ≈0.011 bar, ≈0.22 wt% (ADPC3 circle overlapping an ADPC0.5 triangle).
- Figure 7: a merged blob at ≈0.02–0.04 bar, 0.29–0.32 wt% (ADPC1 diamond ~0.31, ADPC3 circle ~0.31, ADPC0.5 triangles ~0.29 and ~0.32). Because of these three clusters, isotherm_point_count for I1, I3 and I5 is a lower bound.
- Figure 7: near 0.47 bar, each series shows two overlapping markers offset ~0.005 bar. They could not be separated, and one centroid was recorded (rows flagged in notes). The hidden partner is counted in isotherm_point_count. Near 0.105 bar, each series' marker looks slightly enlarged (possibly two coincident markers); recorded as one point and counted once.
- Figure 7: the three markers in the legend were excluded. Figure 7 shows one marker type per sample, so although the text says adsorption/desorption measurements were made, no point can be identified as desorption; all points are coded adsorption.
- Figure 9: overlapping marker(s) at the origin (0 bar, 0 wt%), apparently an ADPC3 circle over at least one other marker. They cannot be attributed to a series, so they are not extracted and not counted. The three legend markers were excluded.
- Figure S5 (si1 p.4): 77 K H2 isotherms up to ~75 bar for (a) ADPC0.5, (b) ADPC1, (c) ADPC3. Each panel has 6 runs (1st/2nd step × 1st–3rd run), each with an adsorption branch (filled) and a desorption branch (open): 36 series in all. Not digitized and no values extracted. All series share one colour and differ only by marker shape and fill, at ~4–5 px in a blurred low-resolution image. At each pressure step the markers of the six runs overlap into vertical stacks, and the desorption points crowd together at 0–10 bar. The tool isolates series by colour only, so markers could neither be assigned to series nor counted. The figure is used only as evidence of repeated isotherms (replicates_reported = true on the 0–80 bar rows). It shows uptakes of the repeated runs (for ADPC1, a visible spread between runs at high pressure) that the tables and text do not give. Related text: cycles after the first lower the maximum capacity slightly, and it is recovered by 473 K for 12 h.

## Values seen but not extracted (text, tables, non-isotherm figures)

- "1.6 wt%" for ADPC1 at 1 bar (p.11 and Conclusions): restates Table 1 1.57; noted on row M65.
- "≈1.8 wt%" for ADPC0.5 at 80 bar (p.12): restates Table 1 1.79; noted on row M40.
- "5.25 wt% at 80 bar" for ADPC1 (Conclusions): restates Table 1; noted on row M80.
- "14 H2 molecules/nm2" for ADPC1 (p.12): authors' per-BET-area density derived from ≈5.5 wt% and SBET; not an areal uptake of a film, so not stored (mentioned on row M81).
- "increase of as much as 150% relative to the one predicted by the Chahine rule" (Abstract), "more than 150%" (Conclusions), "more than double that of the expected value" (p.12): derived comparisons, not uptake values.
- Chahine rule "1 wt% per 500 m2/g, i.e., 6 H2 molecules/nm2" (p.2) and the Chahine line in Figure 10a: literature rule, not a measurement. Introduction "≤3000 m2 g−1": literature.
- Table 2 Tóth t (0.254/0.244/0.242 ± 0.005) and K (4.401/2.858/2.587 ± 0.03): fit parameters, not uptakes; recorded in the notes of the Tóth rows.
- Figure 8 (main p.11): H2 uptake at 1 bar and 77 K against SSA (a) and Vmicro (b), with error bars. Not an isotherm, not digitized. Its points repeat Table 1 column i (DPC shown at 0, not 0.38); its error bars are the only uncertainty shown for the 1-bar values (not printed numerically).
- Figure 10 (main p.13): H2 uptake at 80 bar and 77 K against SSA (a, with Chahine line) and Vmicro (b), with error bars. Not an isotherm, not digitized. Its points correspond to Table 1 column l; error bars not printed numerically.
- Figure 4 (main p.8): N2 adsorption–desorption isotherms at 77 K, not H2. Text: DPC "did not show an appreciable N2 uptake (here not shown)".
- Figure 5 (main p.9, cumulative pore volume), Figure 6 (main p.9, Fmicro bars), Figure S2 (PSD), Figure S3 (ADPC1 − ADPC3 cumulative-volume difference; text says its maximum is "around 15 Å"; the difference values are not printed), Figure S4 (bars of SBET, VT and PSD fractions, plus (d) the mesopore volume fraction Fmeso for each sample, which no table prints): characterization figures, not digitized.
- Text restatements of characterization: ADPC1 micropore volume 0.383 cm3/g and BET 1173 m2/g (p.10, Conclusions); WDS means C 81.3 at%, O 17.7 at%, other elements 1 at% (p.5); "O/C atomic ratio close to 20%" (Conclusions). The PSD peak "centered around 0.5 nm" is stored as average_pore_diameter_nm for the ADPC samples only (Figure S2 puts the DPC peak near 15 Å).
- Figure 3 / Figure S1 (XRD) and Figure 2 (SEM): no uptake values.

## Scope and coding notes

- No non-carbon sorbent was measured (the "Sample Holder" appears only in the XRD figures).
- DPC (S1) is included with material_class = other but flagged: it is pinecone powder dehydrated at 453 K in air. Section 3.1 calls it "the carbonized sample" and the paper treats it as the KOH/DPC = 0 member of the series, but no carbonization step is described for it and its carbon content is not given, so whether it is a carbon sorbent under §3 is unclear.
- The 1-bar instrument (Micromeritics ASAP 2460) is coded volumetric_sieverts, instrument_identified = true. The 0–80 bar "Sieverts' type apparatus (fPcT)" is coded instrument_identified = false (no manufacturer, model or home-built description). No free-volume calibration is described.
- wt% is coded W1/stated from the Section 2.2 definition. The uptake basis is never named: basis_stated = false, uptake_type = unspecified, basis_inferred = excess (volumetric default).
