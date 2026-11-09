# HYC-0120 extraction log (agent B)

## Sources extracted
- main p. 232 (main-3), Fig. 4 inset (AC, 77 K isotherm, 0-50 bar): 6 markers counted, 6 extracted (archive digitizations/fig4_inset_AC_77K.json; x ticks 0/50 at px 898/1073, check 20 at 968; y ticks 0.0/3.0 at px 887/713, check 2.0 at 771). Rows M1-M5 (isotherm I1).
- main p. 233 (main-4), Fig. 5 inset (SWCNTs, 77 K isotherm, 0-50 bar): 6 markers counted, 6 extracted (archive digitizations/fig5_inset_SWCNTs_77K.json; x ticks 0/50 at px 366/531, check 20 at 432; y ticks 0.0/3.0 at px 330/163.5, check 2.0 at 219; colour tolerance 30 used to separate markers from the dark fit line). Rows M6-M10 (isotherm I2).
- main p. 232-233, Results text: "maximum uptake measured from the adsorption isotherms at 77 K and high hydrogen pressures ... 2.7 wt% for activated carbon and 2.4 wt% for SWCNTs". No pressure printed; merged with digitized points (AC: 44.29 bar point, 2.698 wt%, closest in value; the 38.37 bar point, 2.724 wt%, is also within 3%. SWCNTs: 20.86 bar point, 2.417 wt%, the only one within 3%). Rows M5, M8.
- main p. 232, Results text: TDS storage capacity 2.6 wt% (SWCNTs) and 2.5 wt% (AC). Rows M11, M12 (measurement_mode TPD).
- main p. 231, Experimental: TDS procedure (25 mbar loading, ~20 K, degas 470 K ~3 h, <1e-5 mbar), Pd calibration; coded on TPD rows.
- main p. 232, Results: sample descriptions and surface areas (AC BET 1065 m2/g, N2 at 77 K; SWCNTs 854 m2/g, method not named).

## Seen, not extracted
- Fig. 4 and Fig. 5 insets: a marker at the plot origin (0 bar, 0 wt%) in each isotherm; counted in isotherm_point_count (6) but no row, because pressure 0 is rejected by the validator (pressure out of range) and the point carries no uptake information.
- TPD rows M11/M12: loading temperature "approximately 20 K" is below the schema range of temperature_k (50-500 K); stored as temperature_unstated = true with an explanatory note, although the paper does state it.
- p. 231: PdH0.7 calibration standard, 0.66 wt% at 0.7 bar, room temperature (metal hydride, not a carbon sorbent).
- p. 231-232: background (empty sample cell / sea sand), "less than 0.01 wt% on a sample of 3 mg" (not a carbon sorbent measurement; instrument background).
- p. 230 Introduction: literature values (<1 wt% at room temperature [1-4]; 2 wt% zeolites [5], 5 wt% carbon materials [1], 7 wt% coordination polymers [6] at 77 K) are cited from other work, not measurements of this paper.
- Figs. 2, 3, 4 (main panel), 5 (main panel), 6: TDS spectra and coverage vs temperature, not isotherms; no further uptake values beyond the text values (peak temperatures 25, 34, 37, 51 K; complete desorption below 80 K).
- p. 233 Discussion: theoretical/literature quantities (interstitial channel SSA 31 m2/g, potential energies 11, 5, 9 kJ/mol; 3.4 and 3.8 kJ/mol heats of adsorption [18]) are not measurements of this paper.
- The "within an error of 0.2 wt%" statement compares TDS and isotherm amounts; not recorded as uncertainty_wt_pct.
