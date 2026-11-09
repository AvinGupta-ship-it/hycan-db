# HYC-0012 extraction log (agent B)

Input: page images main-1 to main-4 only (no supplementary file). No figure was digitized, so `digitizations/` is empty.

## Sources extracted from

- main-3 (p. 454), Table 1: six H2 uptake values at room temperature (19.0-23.0 °C) and 11.96-12.20 MPa, one per sample, with specific surface areas -> rows M2-M7 (`table_direct`). Each is the only value for its sample and temperature, so no `isotherm_id`.
- main-1 (p. 452), Introduction: "our work in 1999 with a 4.2 wt.% capacity for purified SWCNTs prepared by a hydrogen arc discharge method measured under a pressure of 10-12 MPa and at room temperature using a Sievelt apparatus of the metal hydride laboratory at our institute [4]" -> row M1 (`text_direct`), extracted under the "values reported before" rule as the authors' own earlier measurement, with `previously reported: [4] ...` in notes. Temperature is printed only as "room temperature" and pressure only as the range 10-12 MPa, so both are left empty with `*_unstated = true`. The paper says on p. 454 that "our previous reported hydrogen storage capacities were overestimated". The reconciler should decide whether this background value belongs in scope.
- main-2 (p. 453), Section 2 Experimental and Section 3: synthesis and treatment of the samples, volumetric method, home-built Sievelt apparatus description, sample mass "no less than 200 mg", and SWCNT surface areas of 65 and 229 m2/g before and after purification. These are coded on the rows.
- main-3 (p. 454), left column: blank experiment, leak rate and LaNi5 check. These are coded in the notes and the calibration fields.

## Values seen but not extracted

- main-1 Abstract, main-2 p. 453 Introduction, main-3 p. 454 right column, main-4 p. 455 Summary: "hydrogen storage capacity of the CNTs is less than 1.7 wt.%" at about 12 MPa and room temperature. This is a summary bound across all samples, not a value for one sample (not a row).
- main-3 p. 454: "the purified and post-treated CNT samples display hydrogen storage capacities of 0.9-1.7 wt.%". This is a summary range across Table 1 samples, and its end points are already rows M3 and M5.
- main-3 p. 454: "we also measured three of our CNT samples using an apparatus built ... by Kiyobayashi et al. [19], and the results were in the range of 0.7-0.9 wt.%" (the Acknowledgements on p. 455 confirm the measurements were made on Dr. T. Kiyobayashi's equipment). Not extracted: the three samples are not identified, no value is given for any single sample, and temperature and pressure are not stated. Only a range across samples is printed.
- main-3 p. 454: LaNi5 calibration, "A result of 1.4 wt.% was obtained reproducibly". Not extracted because LaNi5 is a metal hydride, not a carbon sorbent.
- main-1 p. 452: Dillon et al. [1], SWCNTs "could store ~10 wt.% hydrogen at room temperature". Not extracted because it is another group's literature value, not a measurement by this paper's authors.
- main-1 p. 452: Tibbetts et al. [5], nine types of SWCNT, MWCNT, carbon fiber and carbon filament samples "lower than 0.1 wt.% at room temperature and 3.5 MPa". Not extracted because it is another group's literature value and a bound across nine samples.
- main-3 p. 454: DOE benchmark of 6.5 wt.% is a target, not a measurement.
- main-2 p. 453, Fig. 1 (a, b): TEM images of purified SWCNTs. No values.
- main-3 p. 454, Fig. 2a: hydrogen pressure (about 12.06-12.08 MPa) and temperature (about 19.2-19.5 °C) against time in a blank experiment with no adsorbent. This is not an uptake or an isotherm, so it was not digitized.
- main-3 p. 454, Fig. 2b: calculated hydrogen content of the blank Sievelt system (about 176-177 mmol) against time, with linear fit; the text gives a total leak rate of 3.02e-8 mmol/s and a leak error under 0.001% for a 10-h test. This is not a sorbent uptake or an isotherm, so it was not digitized.
- main-4 p. 455, Fig. 3: literature hydrogen storage capacities of CNTs (wt.%) against publication year (1997-2010). This is not an isotherm and shows other papers' values, so it was not digitized.
- Characterization without separate rows: average SWCNT diameter of 1.8 nm, mean MWCNT diameter of about 30 nm and purified-SWCNT purity of about 95% (TGA and TEM). These are tube diameters and purity, not pore diameters, and are recorded in `material_description`. Every Table 1 sample has an H2 value.

## Coding decisions worth checking

- Surface areas: Table 1 says "Specific surface area" and the paper names no method and no probe gas. They are coded `surface_area_method = unspecified` and `surface_area_probe_gas = unspecified`, with the value in `bet_surface_area_m2_g` as the headline area. `bet_range_stated` and `bet_consistency_criteria_stated` are coded `false`.
- `area_same_sample = yes` for all Table 1 samples. For the SWCNTs, the text says the areas "were measured to be 65 m2/g and 229 m2/g" before and after purification. For the MWCNTs, the paper says the "characterization of the samples are presented in a previous paper [18]" (same group). It does not say whether the areas were re-measured for this work.
- Sample mass is printed only as "no less than 200 mg", so `sample_mass_mg` is left empty and the bound is in notes.
- `instrument_identified = true` because the paper describes the home-built Sievelt apparatus and its components. `calibration_described = false` because the free-volume determination is not described; the LaNi5 measurement and the blank leak test are checks, not free-volume calibration.
- `replicates_reported = false` because no uncertainty is reported for a CNT uptake value. The Kiyobayashi re-measurements cannot be attributed to particular samples.
- `measuring_lab_id`: corresponding author Cheng; the affiliation names no university, so the institute is used: "Institute of Metal Research, Chinese Academy of Sciences".
- Basis is not named anywhere ("hydrogen storage capacity"), so `basis_stated = false`, `uptake_type = unspecified`, and `basis_inferred = excess` by the volumetric (Sieverts) instrumental default.
- Sample numbering follows first appearance: S1 is the 1999 purified SWCNTs (Introduction). Then, from Section 2, S2 is As-prepared SWCNTs, S3 As-prepared MWCNTs, S4 Purified SWCNTs, S5 Air-oxidized MWCNTs (treatment a), S6 KOH-activated MWCNTs (treatment b) and S7 CO2-oxidized MWCNTs (treatment c). The label "CO2-oxidized MWCNTs" is printed with a subscript 2.
