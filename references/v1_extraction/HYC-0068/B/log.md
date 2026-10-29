# HYC-0068 extraction log (extractor B)

Input: page images main-01 … main-15 only (no supplementary file). 829 rows, 10 samples (S1 UTL0, S2 OP0, S3 UTL1, S4 UTL2, S5 UTL3, S6 OP1, S7 OP2, S8 OP3, S9 Coconut shell, S10 ACC), 22 isotherms (I1–I22).

## Sources extracted from

- Sec. 2.1 (p. 520): synthesis (pre-carbonization 450 °C 2 h N2; KOH activation 800 °C 2 h, KOH:C 1:1, 2:1, 3:1; 1 M HCl wash) -> synthesis/purification/activation fields.
- Sec. 2.2 (p. 520): N2 sorption (Autosorb iQ3, outgassing 250 °C 24 h, BET P/P0 0.02–0.2 with ISO 9277:2022 consistency criteria, QSDFT slit kernel) -> surface-area/pore codes on every row.
- Sec. 2.3 (pp. 521–522): low-pressure H2 (Autosorb iQ3, 99.999 % H2, 77 K, 57 ads + 20 des points, ~40 mg, 250 °C 24 h) and high-pressure H2 (SETARAM Hy-Energy PCTPro-2000, ~200 mg, 250 °C 12 h at 1e-6 mbar, He calibration at 303 K plus 77 K reference curve); basis and wt% convention passage ("The measured quantity in the adsorption experiments is the excess gravimetric uptake … (ms + mH2)"; Eq. (6) total) -> basis_stated true / W2 stated for this paper's own values (the passage is a separate paragraph covering "the adsorption experiments", applied to the low- and high-pressure data alike).
- Table 1 (p. 523, elemental analysis) and Table 2 (p. 524, XPS) -> composition in notes (N and O inherent to the biomass, not deliberate doping, so dopant fields left empty; residual mineral elements listed in notes, residual_metal fields left empty because they are not synthesis catalysts).
- Table 3 (p. 525) -> S_BET, V_QSDFT (total pore volume), V<0.7 nm (ultramicropore, cutoff 0.7 nm), V>2 nm (mesopore volume), d50 (average pore diameter, DFT); S_QSDFT, S<0.7, S0.7–2, S>2, V0.7–2, d25–d75 in notes.
- Table 4 (p. 527) -> d002 stored as interlayer_spacing_nm; La(Raman), a(100), La(XRD), Lc, N, T, lp, lc not stored (no field; structural, no H2 data).
- Fig. 6a (p. 528): UTL0–UTL3 low-pressure 77 K isotherms, adsorption and desorption -> isotherms I1 (UTL0), I3 (UTL1), I6 (UTL2), I9 (UTL3).
- Fig. 6b (p. 528): OP0–OP3 low-pressure isotherms -> I2 (OP0), I12 (OP1), I15 (OP2), I18 (OP3).
- Fig. 6c (p. 528): UTL1–UTL3 excess isotherms to 100 bar, adsorption and desorption -> I4, I7, I10.
- Fig. 6d (p. 528): OP1–OP3 excess isotherms -> I13, I16, I19.
- Fig. 6e (p. 528): UTL1–UTL3 total uptake (Eq. 6), adsorption only (full symbols) -> I5, I8, I11.
- Fig. 6f (p. 528): OP1–OP3 total uptake -> I14, I17, I20.
- Table 5 (p. 529): all 22 numeric cells extracted. "Max. uptake" excess values merged with the closest digitized Fig. 6c/d point (all within 2 % of the printed pressure; digitized point recorded in notes). "Max. uptake @80 bar" total values merged with the closest Fig. 6e/f point (UTL1: |dp| = 1.71 bar, 2.1 %, merged because Table 5 summarises the Fig. 6e isotherm; UTL2: the point lies in an unresolved merged cluster, row kept in I8 without a digitized value). The "1 bar" column (8 values) kept as separate rows without isotherm_id: although Fig. 6a/b have points at ≈1.006 bar (within 0.02 bar), Sec. 3.5 states that the low-pressure values up to 1 bar are 2.30–2.62 wt% (UTL) and 2.46–2.59 wt% (OP), while the Table 5 1-bar values are 2.51–2.71 and 2.57–2.80 wt% (UTL0 0.14 against ≈0.02–0.03 wt% in Fig. 6a), so the column is not the Fig. 6a/b end points; the source isotherm is not stated. Conservative choice; reconciler should check.
- Table 6 (p. 529): single-valued literature entries extracted with "previously reported": Coconut shell [16] (2.2 wt% at 1 bar, 4.5 wt% at 47 bar) -> I21; ACC [4,28] (1.6 wt% at 1 bar, 3.1 wt% at 72 bar) -> I22 (two values per material treated as one isotherm; the paper does not say they come from different runs).

## Figure digitization (Fig. 6, page image main-10.png, 1241 x 1654 px)

Calibration (lowest/highest labelled tick, third tick as check; tick centres found from pixel-column/row profiles of the tick marks; all checks < 0.3 px):
- 6a: x 0 mbar @217.71, 1000 @564.00, check 400 @356.00; y 0 @452.49, 3.0 @154.00, check 1.5 @303.44.
- 6b: x 0 @726.73, 1000 @1073.62, check 400 @865.55; y 0 @455.00, 3.0 @156.52, check 1.5 @305.66.
- 6c: x 0 bar @214.52, 100 @562.38, check 40 @353.56; y 0 @846.52, 6 @548.00, check 3 @697.41.
- 6d: x 0 @725.40, 100 @1073.49, check 40 @864.50; y 0 @850.68, 6 @552.35, check 3 @701.51.
- 6e: x 0 @214.52, 100 @562.38, check 40 @353.56; y 0 @1246.35, 10 @948.00, check 4 @1126.68.
- 6f: x 0 @725.40, 100 @1073.49, check 40 @864.50; y 0 @1248.00, 10 @949.55, check 4 @1128.58.

Method (scripts and intermediate images in the work directory): legends whitened; for each series a colour-class isolation image was made (filled markers: solid series colour plus, in 6a–d, the light "blend" colour where an open desorption marker is drawn over the filled marker, opened 3x3; open markers: light series colour, minus a 1-px halo around any filled marker, holes filled); a 2x2 opening; connected groups larger than one marker were split by one 3x3 erosion and kept only if every piece was single-marker size, otherwise dropped as unresolved; then `digitize_figure.py extract --mode markers` (open-px 0, marker size limits) on the isolation image. Every archive is one series in `digitizations/` (34 files). `check` passed against Table 5 for the six excess maxima and five total values at 80 bar.

Marker counts (extracted / unresolved). Markers fully covered by other series, merged groups and the (0,0) origin markers could not be digitized; isotherm_point_count for Fig. 6c–f isotherms = digitized + skipped + unresolved estimates + 1 origin marker (ads) and digitized + unresolved (des); these are lower bounds of the visible markers (approximate, ±3). Low-pressure isotherms use 77 (57 + 20 points stated in Sec. 2.3) because most of the near-vertical p < 20 mbar points cannot be separated on the plot.
- 6a UTL0: 27 ads / 11 des digitized of 57 + 20; markers sit on the x-axis (lower part hidden, y biased up ≈0.01 wt%); merged groups at ≈0–20 mbar (47 px) and ≈1006 mbar (41 px) not separated.
- 6a UTL1: 31 ads / 15 des; p < 20 mbar stack (≈12 markers, 243 px group) and the last two markers at ≈0.98–1.01 bar merged, not separated.
- 6a UTL2: 24 ads / 12 des; most UTL2 markers lie under UTL1 triangles; last two markers (≈0.98–1.01 bar) merged; p < 20 mbar stack not separated.
- 6a UTL3: 33 ads / 20 des; last two markers (≈0.98–1.01 bar) merged; p < 25 mbar stack not separated.
- 6b OP0: 26 ads / 6 des; merged group at ≈60–100 mbar (52 px) not separated; markers sit on the x-axis.
- 6b OP1: 33 ads / 18 des; p < 20 mbar stack (310 px) not separated.
- 6b OP2: 34 ads / 15 des; 6b OP3: 29 ads / 18 des, last two markers (≈0.98–1.01 bar) merged.
- 6c UTL1: 34 ads (2 at p ≤ 0 skipped, see below) / 12 des; ≈3 triangles at 6–9 bar merged; one covered marker at ≈63 bar not found. Count 55.
- 6c UTL2: 32 ads (1 skipped) / 12 des; knee 6–14 bar (≈4–5 circles, 216 px) and the last marker (≈83 bar, mostly under a UTL1 triangle, digitized from a fragment) uncertain; des above 63 bar hidden under UTL1 markers. Count 51.
- 6c UTL3: 32 ads (1 skipped) / 20 des; pair at ≈19–21 bar merged; ≈4–6 squares at p < 4 bar fully covered by UTL1/UTL2 markers (not counted). Count 56.
- 6d OP1: 34 ads (2 skipped) / 16 des; two merged groups at ≈13–15 bar (≈2–4 triangles) and the last two (≈94–96 bar) not separated. Count 58.
- 6d OP2: 33 ads (1 skipped) / 19 des; last two circles (≈94–96 bar) merged. Count 56.
- 6d OP3: 32 ads / 18 des; ≈7–8 squares in the 6–19 bar staircase merged (356 px); two des squares at ≈92–94 bar merged; ≈3 squares at p < 1.3 bar covered (not counted). Count 61.
- 6e UTL1: 33 (2 skipped), ≈7 triangles of the 3–11 bar knee merged. 6e UTL2: 26 (1 skipped), ≈8 circles of the 1.3–13 bar knee and the last three circles (≈79–84 bar, ≈7.0 wt%) merged. 6e UTL3: 30 (1 skipped), two merged pairs at ≈18–22 bar, low-pressure squares covered. Counts 43 / 39 / 36.
- 6f OP1: 35 (2 skipped), a merged pair at ≈1.4 bar and the last two (≈94–96 bar) not separated; 6f OP2: 33 (1 skipped), last two merged; 6f OP3: 27, ≈7 squares in the 6–19 bar staircase merged. Counts 42 / 37 / 41.
- Open (desorption) markers in 6a–d are faint outlines largely overlapping filled markers; only the separable ones were digitized (groups < 15 px rejected as fragments).

Digitized points not written as rows (non-positive digitized pressure; marker centred at p ≈ 0 on the 0–100 bar axis, pressure below one pixel ≈ 0.29 bar, cannot be stored): fig6c_utl1_ads (−0.022 bar, 1.114 wt%; −0.006, 0.554), fig6e_utl1_ads (−0.006, 1.118; −0.006, 0.552), fig6c_utl2_ads (−0.045, 0.796), fig6e_utl2_ads (−0.046, 0.817), fig6c_utl3_ads (−0.006, 1.287), fig6e_utl3_ads (−0.006, 1.327), fig6d_op1_ads (−0.077, 0.655; −0.012, 1.300), fig6f_op1_ads (−0.077, 1.302; −0.007, 0.649), fig6d_op2_ads (−0.115, 1.150), fig6f_op2_ads (−0.115, 1.131).

## Values seen but not extracted

- Abstract: "up to 2.6 wt.% at low pressures (1 bar) and 5.3 wt.% at high pressures (30–40 bar)" — rounded restatement of the best Table 5 / Fig. 6 values, no sample named.
- Sec. 3.5 (p. 528): "between 2.30 and 2.62 wt.% for the UTL series and 2.46–2.59 wt.% for the OP series" — range across samples (endpoints not attributed to samples); used only as a cross-check of Fig. 6a/b.
- Sec. 3.5 (p. 529) and Sec. 4 (p. 531): "5.24 wt.% for OP3 and 5.29 wt.% for UTL3" at ~30 bar — same measurements as the Table 5 rows already extracted.
- Sec. 3.5: "reported values ranging from 4.6 to 5.9 wt.%" for coffee-waste and glucose carbons [5,58] — literature range.
- Table 6 ranges (several samples each, not single values): Bamboo [59] 2.0–2.3 wt% at 1 bar (S_BET 1220–2150, V 0.4–0.5); Glucose derived [58] 4.6–5.0 at 100 bar (2140–2550, 1.1–2.0 t-plot); Orange peel [15] "2.3-3-3" at 10 bar (1000–1400, 0.3–0.4, H3PO4); Tangerine peel [26] 0.9–1.7 at 30 bar (<1250); Coffee waste [5] 2.7–2.8 / 5.4–5.9 at 1/35 bar (2990–3330, 1.2–1.6); Orange peel "This work" 2.6–2.8 / 4.1–5.2 at 1/25–33 bar; Tea leaves "This work" "2.5-2-6" / 4.4–5.3 at 1/30–34 bar (summaries of Table 5).
- Fig. 7 (p. 530): Kendall τb matrix (correlation coefficients and p-values for H2 uptake at 250, 500, 750 mbar, 1, 5, 10 bar and maximum vs structural parameters, 11 samples incl. 3 from earlier work) — not an isotherm; it shows no uptake values.
- Fig. 4 (p. 525) N2 isotherms and QSDFT PSDs, Fig. 3 XPS, Fig. 5 Raman/SAXS/XRD, Fig. 1–2 schematic/SEM — characterization only, no H2 values.
- Skeletal density 1.9 ± 0.2 g/cm3 (Sec. 2.2) — assumed literature value used for SAXS normalisation and porosity, not measured; not stored.
- Sec. 3.6: earlier coffee-waste study reproducibility "less than 5 % error" — refers to other samples; replicates_reported = false (paper states no repeats were possible for these samples).
- No non-carbon sorbent values in the paper.
