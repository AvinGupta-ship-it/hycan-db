# HYC-0120 extraction log (extractor A)

## Extracted
- Results text, main.pdf p.3 (journal p.232): TDS total desorbed H2, 2.5 wt% (activated carbon, M1) and 2.6 wt% (SWCNTs, M7). TPD rows, temperature_k empty with temperature_unstated = true because schema v2 limits temperature_k to 50-500 K and the paper's loading temperature is ~20 K; reference_temperature_k = 370 (end of recorded spectrum); loading pressure 25 mbar = 0.025 bar.
- Results text, main.pdf p.4 (journal p.233): maximum 77 K isotherm uptake 2.7 wt% (activated carbon, M2) and 2.4 wt% (SWCNTs, M8). No pressure printed; each merged with the plotted point of the Fig. 4 / Fig. 5 inset closest in value (AC 44.29 bar; SWCNT 20.92 bar), pressure digitized.
- Fig. 4 inset (main.pdf p.3), AC 77 K isotherm: 5 markers digitized (archive HYC-0120_fig4_inset_AC_77K.json), 4 rows (M3-M6) plus the point merged into M2. Calibration x 0/50 bar, y 0/3.0 wt%, verified on 30 bar and 2.0 wt%. Check against stated 2.7 wt% passed (0.06%).
- Fig. 5 inset (main.pdf p.4), SWCNT 77 K isotherm: 5 markers digitized (archive HYC-0120_fig5_inset_SWCNT_77K.json), 4 rows (M9-M12) plus the point merged into M8. Calibration x 0/50 bar, y 0/3.0 wt%, verified on 20 bar and 2.0 wt%. Check against stated 2.4 wt% at 48.7 bar passed at 4.5% (the stated value matches the plateau line and the 20.9 bar marker, not the highest marker).
- Characterization: AC BET 1065 m2/g (N2, 77 K); SWCNT 854 m2/g (method not named; coded unspecified). Degassing 470 K, ~3 h, <1e-5 mbar (TDS rows only). No pore volumes, compositions or BET range reported.

## Seen, not extracted
- Fig. 4 and Fig. 5 insets: the origin marker (0 bar, 0 wt%) merges with the axes and cannot be separated; counted in isotherm_point_count (6) but not extracted. The fitted line in each inset is not digitized because markers are present.
- Figs. 2, 3, 4, 5 main panels: TDS spectra (partial pressure or arb. units against temperature); not uptake isotherms. Fig. 6 (coverage against desorption temperature, relative values): not digitized; no uptake value not already in text.
- PdH0.7 calibration standard, 0.66 wt% (H/Pd = 0.7 at 0.7 bar, room temperature): not a carbon sorbent.
- Introduction literature values (<1 wt% at room temperature; 2 wt% zeolites [5]; 5 wt% carbon materials [1]; 7 wt% coordination polymers [6]): cited from other papers, not measurements here; no sample, T or P given for the carbon value.
- Background of the empty cell/sea sand: "less than 0.01 wt% on a sample of 3 mg", blank measurement, not a sorbent uptake.
- "within an error of 0.2 wt%": agreement between TDS and isotherm maxima, not a stated uncertainty of either; not coded as uncertainty.
- SWCNT interstitial-channel area 31 m2/g and bundle-model values (GCMC, ref. 17): literature/model, not this sample's measurement.
