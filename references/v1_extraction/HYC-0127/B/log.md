# HYC-0127 extraction log (extractor B)

Input: page images main-1 to main-5 only (no SI). Extraction date 2026-11-09.

## Sources extracted from

- main-2 (p. 202), Table 1: four H2 uptakes (as-prepared and Ar-treated fibers for the 90:5:5 and 85:10:5 Fe/Ni/Cu catalysts), plus the BET area, carbon yield and TEM diameters per catalyst. Rows M1-M4.
- main-2 (p. 202), text, col. 1: synthesis (ethylene over Fe/Ni/Cu at 873 K, 300 mL/min, 3 h; Ar treatment at 1273 K for 36 h), nitrogen BET at 77 K, 12 MPa, apparatus, sample mass 50-100 mg, degas ca. 10^3 Pa at 423 K. Used for coding M1-M4.
- main-2 (p. 202), text, col. 2: blank run, MmNi4.5Al0.5 check, interlayer spacing 0.34 nm (electron diffraction, Fig. 2 inset). Used for coding.
- main-3 (p. 203), text, col. 1: 6.54 wt% (same measurement as Table 1, merged into M4), approximately 45 kg H2/m3 at a typical density of 700 kg/m3 (stored on M4 as volumetric capacity and packing density), Ar-treatment area change of roughly 15%.
- main-4 (p. 204), text, col. 1: "present hydrogen uptake measurements, obtained at 298 K". This is the source of temperature_k = 298 on every row.
- main-5 (p. 205), ref. 34 and 36 notes: the 45 kg H2/m3 is "calculated" and "an estimated upper limit"; 6.54 wt% repeated. Recorded in M4 notes.
- Abstract (main-1): "up to 6.5 wt %" at 12 MPa and ambient temperature. This is the rounded 6.54 wt% value (M4), so it gets no separate row.

## Figures

- Figure 1 (p. 202): schematic of the apparatus. No data. Used for instrument and absolute-gauge coding.
- Figure 2 (p. 203): TEM micrograph and electron diffraction of the 90:5:5 fibers. No uptake data.
- Figure 3 (p. 203): H2 uptake (wt%) against time (0-300 min) for the four samples, with error bars. This is kinetics, not an isotherm, so it was not digitized (§9 scope). Its plateau values match Table 1, which the paper already prints. The intermediate time points are not extracted (kinetics). The error bars are the basis for replicates_reported = true. Their magnitude is not printed, so uncertainty_wt_pct is empty. No digitization files exist, so `digitizations/` is empty.

## Values seen but not extracted

- MmNi4.5Al0.5 alloy, 1.27 wt% (p. 202): not a carbon sorbent (hydride calibration check).
- Blank (no sample) run, no adsorption by the stainless steel vessel (p. 202): no value.
- "reproducing hydrogen uptakes as low as 0.1 wt % when using 100 mg" (p. 202): instrument sensitivity, not an uptake. It was not used as uncertainty_wt_pct and is noted on the rows.
- "the amount of reversible hydrogen at 298 K is approximately 80%" (p. 202, citing refs 20-22): an estimate of reversibility, not an uptake value, and the paper says desorption could not be measured accurately.
- 0.46 wt% (p. 202): from GCMC simulations by Wang and Johnson (ref. 24), so it is theoretical and from another paper.
- 0.2 wt% (p. 203): calculated uptake for a physisorbed H2 monolayer on the 6.54 wt% material. This is a calculation, not a measurement.
- "ca. 0.2 wt %" (p. 203): the uptake of Ahn et al. (ref. 17), from another paper.
- 0.4 wt% (p. 204): calculated atomic-monolayer uptake for the 85:10:5 CNFs. This is a calculation.
- 2 wt% per 1 K temperature differential (p. 204): a calculation of instrument error, not an uptake.
- 8 wt% with 70% reversible (p. 204): from Cracknell's simulations (ref. 33), so it is theoretical.
- "approximately 9 wt %" (ref. 36 note, p. 205): a hypothetical future capacity, not a measurement.
- DOE targets of 62 kg H2/m3 and 6.5 wt%: targets, not measurements.
- Table 2 (p. 203): initial uptake rates (x10^17 molecules s^-1 m^-2) of 1.1 +/- 0.1, 3.6 +/- 0.2, 2.3 +/- 0.1 and 5.7 +/- 0.4. These are rates, not uptakes.
- Ishikawa dissociation and exchange rates, and Ea and preexponential values (pp. 203-204): from literature (ref. 38), not uptakes.
- Interlayer spacing 0.36 nm (p. 204): from Orimo et al. (ref. 25), another paper.
- Electrochemical storage in CNFs (p. 204, ref. 42): electrochemical, with no value given.

## Coding decisions

- Labels combine the Table 1 row label (catalyst ratio) with the wording of the Table 1 uptake column ("as prepared", "Ar treated"). Table 2 and Figure 3 print "argon treated" for the same samples.
- Four samples (S1-S4), one per catalyst ratio and treatment state, in Table 1 reading order.
- Table 1 gives one N2 BET area per catalyst ratio, without saying whether it belongs to the as-prepared or the Ar-treated state, and the text says the areas changed by roughly 15% on Ar treatment. The area is therefore carried on both states' rows with area_same_sample = unclear.
- Interlayer spacing of 0.34 nm is recorded only on the 90:5:5 as-prepared row, because Figure 2 shows the 90:5:5 as-prepared fibers. The text also states 0.34 nm generally for the CNFs.
- The volumetric capacity of 45 kg/m3 and the packing density of 0.7 g/cm3 (printed as 700 kg/m3, "typically", for "these nanostructures") are recorded only on M4, where the paper applies them.
- instrument_identified = true: the "novel high-pressure apparatus" is described with a schematic (Fig. 1) and cites the authors' own ref. 31. The paper does not use the word "home-built".
- calibration_described = false: the paper does not state how the free or sample volume was determined. The ballast is only described as matching the sample volume.
- Residual catalyst metal (Fe/Ni/Cu) is not quantified and no purification is stated, so the residual metal fields are empty and material_class is carbon_nanofiber.
- No characterization-only samples exist without uptake.
