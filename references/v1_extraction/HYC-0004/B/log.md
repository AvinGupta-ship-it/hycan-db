# HYC-0004 extraction log (agent B)

Input: main-1.png to main-5.png (pp. 619-623); no supplementary file. All values read from the page images, enlarged with PIL to check each digit.

## Sources extracted

- Table 1 (main-2.png, p. 620), column "H2 total (ml (STP)/g)", 77 K and 1 bar: one row per carbon sample, Nos. 1-21, giving 21 rows (M1-M21 in table order). Texture columns PV, S_BET, S_t and MPV are on every row of their sample.
- Experimental, main-1.png (p. 619) right column and main-2.png (p. 620): sample descriptions (steam-activated 7, 8, 11, 12, 14-19; chemically activated 20; ACF 5, 6, 12; activated graphite 3, 9; CNF 2, 4, 10, 21), N2 physisorption (Micromeritics ASAP 2400), H2 measurement (Micromeritics ASAP 2010, 77 K, 0-1 bar), S_t definition, MPV definition.
- Acknowledgements, main-5.png (p. 623): "Norit for providing the activated carbons", the basis for coding the AC Norit samples as commercial.
- Abstract, main-1.png (p. 619), and discussion, main-4.png (p. 622): "238 ml (STP)/g" is sample 19's Table 1 value. It is recorded on that row (M19) and not as a separate row.

## Sample numbering

sample_id follows the order in which each sample is first named, by number or label, in reading order. Experimental (p. 619) names 7, 8, 11, 12, 14-19, 20, 5, 6, 3, 9, 2, 4, 10, 21; Table 1 then adds 1 and 13.
Mapping of paper No. to sample_id: 7=S1, 8=S2, 11=S3, 12=S4, 14=S5, 15=S6, 16=S7, 17=S8, 18=S9, 19=S10, 20=S11, 5=S12, 6=S13, 3=S14, 9=S15, 2=S16, 4=S17, 10=S18, 21=S19, 1=S20, 13=S21.

## Values seen but not extracted

- Table 1 columns "H2 meso" and "H2 micro" (ml (STP)/g) for Nos. 1-21. These are not measured uptakes. They split each H2 total into a mesopore and a micropore contribution using the H2 versus t-surface correlation that the authors fitted across several samples (Fig. 2; carbon slope 0.0891 from samples 4, 10, 21). They are values computed from several samples' measurements, so they are not rows. Values (No.: meso / micro): 1: 0/0; 2: 2/4; 3: 6/8; 4: 11/1; 5: 1/142; 6: 1/183; 7: 2/140; 8: 6/28; 9: 16/19; 10: 7/0; 11: 17/133; 12: 15/127; 13: 10/178; 14: 18/150; 15: 16/155; 16: 27/134; 17: 21/144; 18: 20/167; 19: 7/231; 20: 54/92; 21: 22/0. Observations: for No. 3, 0.0891 x 85 = 7.6, but 6 is printed; for No. 9, meso + micro = 35 while total = 36.
- Table 2 (main-2.png, p. 620): silica, alumina, zeolite and MCM-41 samples 22-36 are not carbon sorbents (§3). H2 total (ml (STP)/g): 22 SiO2 90: 4; 23 Zeolite L: 59; 24 Zeolite ZSM5: 80; 25 Zeolite ferrierite: 65; 26 SiO2 D051 A: 9; 27 SiO2 1614 E: 9; 28 SiO2 Caboxil M5: 11; 29 S980G: 5; 30 SiO2 Aerosil 200: 0; 31 SiO2 Becker AD 050: 18; 32 SiO2-60-1: 3; 33 Al2O3 preshaped: 7; 34 SiO2 380: 27; 35 MCM-41: 65; 36 S970SH: 28. Each also has PV, S_BET, S_t, MPV, H2 meso and H2 micro.
- Text, p. 621: "the oxidic surfaces take up 0.06 ml (STP)/m2 at 1 bar, the carbon surfaces 0.09 ml (STP)/m2". These are slopes of correlations across several samples (Fig. 2). Also derived from them: a_M = 0.14 nm2, a monolayer capacity of 7 x 10^18 molecules/m2, and coverages of 22% (oxides) and 34% (carbon) at 1 bar. Not rows.
- Text, p. 621: "H2 uptake per ml of micropore volume amounts to 490 ml (STP)/g", and the apparent H2 density in zeolite micropores, 0.044 g/ml (63% of liquid hydrogen, 0.07 g/ml). These describe zeolites (not carbon) and come from a correlation. Not rows.
- Text, p. 622: Fig. 4 lower line: "an H2 uptake of 220 ml (STP)/ml or an H2 density of 0.020 g/ml (28% of liquid H2)", lower limit mainly from samples 19 and 20. Upper limit: samples 6, 11, 14 and 16, "515 ml (STP)/ml or an H2 density of 0.046 g/ml (66% of liquid H2)". These are adsorbed-phase densities from correlations across several samples. Not rows.
- Text, p. 622: "similar hydrogen densities (0.04-0.05 ml/g)" for zeolites and activated carbons (unit printed as ml/g), and "density of H2 in the micropores of carbon ... ranges from 0.02-0.05 g/ml, that is 30%-70% of the density of liquid H2". These are ranges across samples. Not rows.
- Text, p. 622: MCM-41 "adsorbs 65 ml (STP)/g, which is a 12% higher uptake than other mesoporous oxides". Silica, not carbon (same as Table 2 No. 35).
- Text, p. 619 and p. 622: DOE target "6.5 wt%, which equals 720 ml (STP)/g"; projected uptakes of "~560 ml (STP)/g" (Abstract) and "560 ml (STP)/g" for 1 ml/g micropore volume at 0.05 g/ml; "780 ml (STP)/g" at liquid-H2 density. These are targets and projections, not measurements.
- Fig. 1 (p. 621; H2 uptake vs BET area), Fig. 2 (p. 621; H2 uptake vs t-surface), Fig. 3 (p. 622; t-surface corrected uptake vs micropore volume, oxides), Fig. 4 (p. 622; t-surface corrected uptake vs micropore volume, carbon): correlation scatter plots, not isotherms, so not digitized. Every plotted point is a Table 1 or Table 2 value: H2 total in Figs. 1 and 2; H2 micro against MPV in Figs. 3 and 4. The only figure-only values are the fitted lines: Fig. 1: y = 0.1369x + 9.1651, R2 = 0.8901 (carbon), and y = 0.0845x + 2.3709, R2 = 0.5284 (silica and alumina). Fig. 2: y = 0.0891x, R2 = 0.9882 (carbon), and y = 0.0558x, R2 = 0.9838 (oxides). Fig. 3: y = 492.9x + 0.1148, R2 = 0.9899. Fig. 4: y = 514.81x + 0.3238 (upper) and y = 216.66x + 0.6518 (lower). Regression parameters across samples, not rows.
- Text, p. 619: "From adsorption-desorption experiments it is evident that reversible physisorption exclusively takes place with all samples". No desorption values are reported.
- No isotherm is plotted anywhere in the paper, so digitizations/ is empty and digitize_figure.py was not run.
- No carbon sample has characterization without an H2 uptake value.

## Coding decisions (also stated in row notes)

- uptake_type = unspecified, basis_stated = false. "H2 total" names the sum of the meso and micro contributions, not an uptake basis.
- measurement_method = volumetric_sieverts, inferred from the instrument (Micromeritics ASAP 2010, a static volumetric analyser); the paper does not use the word volumetric. basis_inferred = excess by the volumetric default.
- No isotherm_id: each sample has a single reported value (1 bar) at 77 K, although the run covered 0-1 bar.
- S_t (t-plot area excluding the micropores) is stored in external_surface_area_m2_g. MPV method not stated (pore_volume_method = unspecified, probe N2).
- No. 1 (Synthetic graphite) H2 total is printed as 0 and stored as an exact 0.
- No. 21 (Hyperion CNF): the paper says only that it was "catalytically synthesized" and names no supplier, so synthesis_method = other and it is not coded commercial.
- No. 12 (ACF 500) appears in both the ACF list and the steam-activated list. activation_method records steam activation at 1000 °C.
