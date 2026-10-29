# HYC-0062 extraction log (agent B)

Input: main-1.png to main-4.png (Science 285, 91-93, 1999). No supplementary file. Pages 3 (right two columns, from "Regulation of NMDA Receptors") and the end of page 1 (left column, BSCCO paper) belong to other articles. main-4.png is a download cover page.

## Sources extracted from
- main page 2 (p. 92), Table 1: rows CNT, Li-doped CNT, Li-doped Graphite, K-doped CNT, K-doped Graphite. Gave M1, M3, M4, M5, M6 (Wi wt%, Vi g/liter, Pabsorb 1 atm).
- main page 2 (p. 92), text col. 1: "a maximum value corresponding to a total of 14.5 weight % H2 at 673 K" (Li-doped CNT, TGA heating ramp). Gave M2 (temperature cycle).
- main page 2 (p. 92), text col. 2: 20 wt% at 653 K for Li-doped CNT and "~14 weight % (saturated value)" for K-doped CNT. Same measurements as the Table 1 values, merged into M1 and M3.
- main page 2 (p. 92), text col. 3: "0.4 weight % ... measured for the same carbon nanotubes ... (9)". Same as Table 1 CNT, merged into M4 (previously reported, ref. 9).
- main page 1 (p. 91), abstract and text col. 3: ~20 wt% (Li-doped CNT, 653 K, 200 to 400 C) and ~14 wt% (K-doped CNT, room temperature); ~160 and 112 kg H2/m3. Same measurements as M1 and M3; volumetric text values recorded in notes only.
- main page 1 (p. 91), text col. 3: synthesis, purification, doping, Merck graphite, specific surface areas 130 (CNT) and 8.6 (graphite) m2/g, Li/C and K/C about 1/15 by XPS, densities ~0.9 g/cm3 (Li-doped CNT) and ~2.0 g/cm3 (Li-doped graphite). Used as characterization.
- main page 2 (p. 92), text col. 1: TGA method, H2 purity (>99.99%), pretreatment at 873 K for 1 hour in purified H2 (99.99%). Used for method fields.
- main page 2 (p. 92), Fig. 1 caption: K-doped CNT held at 298 K for 2 hours. Used for the M3 temperature.
- main page 3 (p. 93), text col. 1: saturated uptake measured at 653 K (Li-doped CNT and graphite) and 298 K (K-doped materials). Used for the M5 and M6 temperatures.

## Schema constraints (values printed but not storable in their field)
- Temperatures 653 K (M1, M5) and 673 K (M2) are above the schema v2 range for temperature_k (50-500 K), and validate_row_detail.py rejects them as errors. temperature_k is left empty with temperature_unstated = true, and the printed temperature is given in each row's notes. These temperatures ARE stated in the paper.
- Table 1 Vi = 280 g/liter for Li-doped Graphite (M5) is above the schema maximum for volumetric_capacity_kg_m3 (200). Not stored in the field; recorded in notes.
- Table 1 CNT row: Tabsorb is printed only as the range 298-773 K. No single temperature, so M4 has temperature_k empty and temperature_unstated = true (explained in notes).

## Values seen but not extracted
- Table 1 FeTi-H (>263 K, 25 atm, <2 wt%, 96 g/liter) and NiMg-H (>523 K, 25 atm, <4 wt%, 81 g/liter): metal hydrides, not carbon sorbents.
- Table 1 Cryoadsorption (~77 K, 20 atm, ~5 wt%, ~20 g/liter, 1.66 kWh/Kg, 0.67 kWh/liter): a generic benchmark value for a class of systems (activated-carbon cryoadsorption, refs. 3 and 4), not a sample measured in this paper. Reference value, not a row.
- Table 1 Isooctane/gasoline (>233 K, 1 atm, 17.3 wt%, 117 g/liter, 12.7 kWh/Kg, 8.76 kWh/liter), and the text "gasoline or diesel (17.3 weight %)": not a sorbent.
- Table 1 energy-density columns (kWh/Kg, kWh/liter) for all carbon rows: derived quantities with no schema field. Not extracted (values listed in row notes).
- p. 91 text, "the H2 uptake by these systems is less than 6 weight % (Table 1)": a generic statement about metal hydrides and cryoadsorption. Not a carbon-sample value.
- p. 91 text, literature values: Dillon (printed "Dollin") et al., SWNT soots about 5 to 10 wt% at 133 K and 300 torr (ref. 5); Chambers et al., graphite nanofibers 67 wt% at 120 atm and room temperature (ref. 6); Ye et al., SWNT 8.25 wt% at 80 K and 100 atm (ref. 7). These are other groups' measurements on other samples, cited as background, not measurements in this paper. Not extracted.
- p. 92 text col. 3, "no H2 absorption" for undoped graphite: no number printed, so no row. Undoped graphite characterization: Merck graphite, average diameter 50 um, specific surface area 8.6 m2/g (method not stated), interplanar distance 0.335 nm.
- p. 92 text col. 2, "the H2 uptake by alkali-doped graphite was only 35 to 70% of that by alkali-doped CNT": a ratio, not an uptake value.
- p. 92 text col. 1, Li-doped CNT TGA cycle "H2 uptake began at temperatures around 773 K and ended at 423 K": temperatures only, no uptake value.
- p. 93 text, cycling: "after more than 20 cycles of absorption-desorption, the capacities of H2 uptake are reduced by less than 10% for both systems". A cycling result with no per-cycle values. Not a row; recorded in notes, and replicates_reported = false.
- p. 93 text, TPD: "the Li-doped CNT exposed to H2 at 10 atm for 1 hour can store the same amount of H2 as those systems at ambient pressure for 2 hours". No number printed (implied equal to the ambient-pressure value). Not extracted.
- p. 93 text, Li-doped materials keep their H2 uptake capability after heating in air at 373 K: qualitative, no value.
- Fig. 1A (Li-doped CNT) and Fig. 1B (K-doped CNT): TGA weight (mg) against temperature (K), drawn as lines without markers. Not isotherms, so not digitized. They show the TGA sample weights (A axis 2.7-3.2 mg; B axis 4.4-5.1 mg) and the full weight-temperature profiles: the weight gain on cooling and the desorption profile on heating. The text does not give these numerically, except the 14.5 wt% maximum (Fig. 1A, M2) and the ~14 wt% saturated value (Fig. 1B, M3). The sample mass is not stated in the text, so sample_mass_mg is empty.
- Fig. 2: FTIR spectra (Li-H about 1420 cm-1, C-H 3000 to 3350 cm-1 and 2600 to 3400 cm-1). No uptake values.
- Interplanar distance 0.347 nm (CNT) is stored only on the undoped CNT row (M4). On the doped rows it is mentioned in notes, as a parent-material value.

## Digitization
- None. The paper has no H2 isotherm figure, so digitizations/ is empty.
