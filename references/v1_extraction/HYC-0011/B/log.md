# HYC-0011 extraction log (agent B)

Input: 4 page images (main-1.png to main-4.png, pp. 497-500); no supplementary file. No tables in the paper. No figure is an isotherm, so nothing was digitized and `digitizations/` is empty.

## Sources extracted from
- main-1.png (p. 497), Abstract: 8.0% for the CVD film (sample 2) -> M4 (same value as the Section 3 text); "even higher H2 storage capacity than that" for the catalytic-decomposition film (sample 3) -> M6 (lower bound 8.0 wt%).
- main-2.png (p. 498), Section 2 Experiment: apparatus (brass cell 49.30 ml, MEMS vacuum sensor 10^2-10^6 Pa, accuracy 20 Pa), procedure (heated to 353 K, vacuum-degassed 4-5 h to 3.7 x 10^-5 tau, H2 99.99%, empty-cell correction runs), sample descriptions and masses -> method and sample fields on every row.
- main-2.png (p. 498), Section 3 paragraph 1: sample 1, 0.26 wt% at "just greater than 1 atm", room temperature -> M1.
- main-2.png (p. 498), Section 3 paragraph 2: sample 1, 0.21 wt% at 0.52 atm, room temperature -> M2.
- main-2.png (p. 498), Section 3 paragraph 3: sample 1, 0.22 wt% from the heating/cooling cycle to 353 K -> M3 (temperature_cycle).
- main-2.png (p. 498), Section 3 paragraph 4: sample 2, 6.3 x 10^-6 g/cm2 and 8.0 wt% (film mass 9.0 mg) -> M4 (one row, same run).
- main-2.png/main-3.png (pp. 498-499), Section 3 paragraph 6: sample 3, 2.5 x 10^-5 g/cm2 -> M5.
- main-3.png (p. 499), Section 3 final paragraph: "A H2 adsorption capacity above 8.0% was achieved at room temperature in CNT films" -> supports M6 (same statement as the Abstract bound; not a separate row).

## Values seen but not extracted
- main-1.png (p. 497), Introduction: values from other groups' published work, not measured in this paper: Dillon [1] 5-10 wt% extrapolated for pure CNTs (soot at 133 K and 300 tau); Ye [2] 8.25 wt% for SWNTs at 80 K and 12 MPa; Chen [3] 14 wt% and 20 wt% by TGA for alkali-metal-doped CNTs, with "the fresh datum is 0.25 wt%" [4]; Liu [5] 4.2 wt% at 10 MPa and room temperature. Not rows (cited literature, not this paper's measurements).
- main-2.png (p. 498): "ambient pressure (5.2 x 10^4-1.4 x 10^5 Pa)" is the overall range of all experiments, not the pressure of any single value; not used as a row pressure.
- main-2.png (p. 498), Section 3 paragraph 6/7: sample 3 areal uptake "about four times as large as that of sample 2" (a ratio of M5 to M4, not a new value); "the corresponding H2 adsorptivity (wt%) of sample 3 would be remarkable" (no number; covered by M6).
- main-1.png (p. 497), Abstract: H2 storage by arc-discharge CNTs "generally takes 25 h or above" and capacity "is very low" (no uptake number).
- main-2.png (p. 498), Fig. 1: apparatus schematic, no values.
- main-3.png (p. 499), Figs. 2, 3, 5, 6: pressure versus time at room temperature for samples 1, 1, 2 and 3 (kinetics, not isotherms); not digitized. They show cell pressures (initial and final) that the text does not print, including the equilibrium pressures of M1, M4 and M5, whose pressure_bar is therefore left empty with pressure_unstated = true. They show no uptake values.
- main-3.png (p. 499), Fig. 4: pressure versus temperature for sample 1 ("T up", "T down"), a temperature cycle, not an isotherm; not digitized. Shows pressures only; the uptake from it is the printed 0.22 wt% (M3).
- Characterization: no surface area, pore volume or pore size is reported for any sample (surface_area_method = none on every row). Sample 1 composition (about 60 wt% MWNTs, 0.5-2 um long, 10-25 nm diameter, rest carbon nanoparticles and amorphous carbon), film thickness 2.5-10 um and film sizes 3 x 4 cm2 and 4.5 x 4 cm2 are recorded in material_description. TEM images are said to be shown elsewhere [9,10].
- Sensor accuracy (20 Pa) is an instrument specification, not an uncertainty on any uptake value; replicates_reported = false and uncertainty_wt_pct empty.
- No non-carbon sorbent is measured.

## Coding decisions
- Samples: S1 = sample 1 (arc-discharge MWNT powder, 169.5 mg), S2 = sample 2 (CVD film from C2H2, Fe(OH)3 catalyst), S3 = sample 3 (film from thermal decomposition of FePc; synthesis_method = pyrolysis because the paper separates it from its "CVD method" sample).
- M1 and M2 are separate runs on sample 1 (separate experiments and figures; the paper attributes a pressure rise in the 0.52 atm run to H2 left from "the last time"), so each has its own isotherm_id (I1, I2) with isotherm_point_count = 1.
- Sample 3: the areal uptake (exact, M5) and the abstract's wt% lower bound (M6) are from the same run but are kept on separate rows, because one row would mark the exact areal value as a bound. M4 keeps its areal and wt% values on one row (both exact).
- Pressure: only 0.52 atm (M2) is printed as a number; "just greater than 1 atm", "above 1 atm" and "P < 1 atm" are not, so those rows have pressure_unstated = true. Temperature is "room temperature" throughout, so temperature_unstated = true on every row.
- Method: closed-cell manometric (pressure-drop) measurement, coded volumetric_sieverts; basis not named, so basis_inferred = excess by the volumetric default and uptake_type = unspecified. instrument_identified = true (the authors' own apparatus, described with a schematic); calibration_described = false (only an empty-cell wall correction is described, no free-volume determination).
- Degassing: 353 K -> 79.85 C; end pressure 3.7 x 10^-5 "tau", read as Torr -> 0.004932914 Pa (unit symbol is non-standard; flagged in notes); duration printed as 4-5 h, left empty.
- measuring_lab_id: the paper prints the corresponding author as "Zhu Changchun*" and "Z. Changchun"; the surname is taken as the paper prints it ("Changchun group, Xi'an Jiaotong University"), consistent with first_author "Qikun" in paper.json; the e-mail (chzhu@) suggests the family name is Zhu.
- Internal inconsistency flagged on M4: 6.3 x 10^-6 g/cm2 over a 12 or 18 cm2 film divided by 9.0 mg gives about 0.84 or 1.26 wt%, not the printed 8.0 wt%; both printed values are stored as printed.
- Validator (`validate_row_detail.py --errors-only`): no errors. Warnings only: uptake_type unspecified (all rows) and "Pre-2005 raw-CNT high uptake" on M4 and M6.
