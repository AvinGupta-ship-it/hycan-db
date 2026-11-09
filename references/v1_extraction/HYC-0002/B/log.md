# HYC-0002 extraction log (agent B)

Input: page images main-1 to main-4 (no SI). The article runs over main-1 (from the "Reports" heading), main-2 and main-3 (to the end of ref. 12). The top of main-1 (references of a preceding ecology article), the bottom of main-3 (a separate article, "Polycationic Peptides from Diatom Biosilica...") and main-4 (Science cover sheet) are not part of this paper.

## Sources extracted from
- Table 1 (p. 1128, main-2): storage capacities of samples 1, 2, 3 (2.4, 2.8, 4.2 wt%). Rows M1 to M3. Initial mass is stored as sample mass. Final mass and residual % are in notes.
- Table 1 caption and text p. 1128 (main-2): conditions (298 K, 100 to 120 atm / about 10 to 12 MPa, degassing at 423 K, H2 purity 99.999%, error <0.38 wt%). Applied to M1 to M3 and, where stated as the general procedure, to M4 and M5.
- Abstract (p. 1127, main-1): 4.2 wt% (same measurement as Table 1 sample 3, merged into M3); 0.9 wt% residual stored hydrogen for the HCl- and vacuum-treated sample (row M4).
- Text p. 1127 col. 3 (main-1): 4.2 wt%, H/C 0.52, purity 50 wt% (merged into M3).
- Text p. 1129 col. 1 (main-3): "less than 1 weight %" at "pressures lower than 5 MPa", sample not specified (row M5, upper bound, unlabelled sample).
- Text p. 1129 col. 2 (main-3): 4.2 wt% again (merged into M3).
- Text p. 1128 col. 1 and p. 1129 col. 1 (main-2, main-3): synthesis, TGA catalyst residue (~40 wt%), SWNT purity (50 to 60 wt%), HRTEM/Raman diameters (sample description and notes only).

## Figures
- Fig. 1 (p. 1128): HRSEM image. No values.
- Fig. 2 (p. 1128): apparatus schematic. No values.
- Fig. 3 (p. 1128): hydrogen adsorbed (wt%) and right-axis ΔP/Weight (atm/g) against adsorption duration (0 to 500 min) for Sample 1#, 2#, 3#. This is kinetics, not an isotherm, so it was not digitized and digitizations/ is empty. The time-resolved points (a series of markers from 0 to 480 min for each sample) and the ΔP/Weight values are not given in the tables or text. They were not extracted, and the figure was not compared numerically with Table 1.

## Values seen but not extracted
- Abstract: "78.3 percent of the adsorbed hydrogen (3.3 weight percent) could be released under ambient pressure at room temperature". The 3.3 wt% is an amount released on depressurisation, the difference between the 4.2 wt% capacity (M3) and the 0.9 wt% residual (M4). It is not an uptake at one state, and the schema has no mode for a pressure-swing released amount. The 78.3% is a fraction.
- Abstract and p. 1127: H/C atom ratio 0.52 for the 4.2 wt% value. There is no schema field for it, so it is recorded in the M3 notes.
- Text p. 1127: "~80% of the adsorbed H2 can be released at room temperature". This is a fraction, not an uptake.
- Table 1: residual H2 storage 21.2% (sample 1) and 24.9% (sample 2), printed as a percentage of total capacity, which is not an uptake unit. The paper prints no wt% for these two samples, and computing one from the masses or the percentages would be derived arithmetic, so they are not rows. The masses and percentages are in the M1 and M2 notes. Sample 3's 21.7% is printed in wt% in the abstract (0.9 wt%) and is row M4.
- Table 1: final masses 482.6, 504.9 and 497.4 mg (after venting). These are not uptake values and are recorded in notes.
- Text p. 1129: "a weight increase (0.5 to 1 weight %) for all three samples" and "21 to 25% of the total adsorbed H2". These are ranges across the three samples, not per-sample values.
- Text p. 1129: heating at 473 K made "the weight increase disappeared". This is qualitative, with no number.
- Text p. 1129: "after four cycles of adsorption/desorption, the H2 uptake capacity of the SWNTs remained almost unchanged". No value is given.
- Text p. 1128: "~70% of the whole adsorption capacity is achieved" after the first 60 min. This is a kinetic fraction.
- Text p. 1129: "the H2 adsorption capacity of pure SWNTs will likely be larger than 4.2 weight %". This is the authors' expectation for a hypothetical pure material, not a measurement.
- Intro p. 1127 and p. 1129: results of other groups cited as background. Dillon et al. (1): soot with 0.1 to 0.2 wt% SWNTs at 133 K, extrapolated to 5 to 10 wt% for pure SWNTs. Ye et al. (2): H/C about 1.0 at 80 K and >12 MPa. Chambers et al. (3): nanofibers "in excess of 11, 45, and 67 weight %" at room temperature and 12 MPa. Chen et al. (4): 20 and 14 wt% for Li- and K-doped MWNTs at ambient pressure. These are not measurements reported by this paper, so they were not extracted. I considered the "values reported before" rule and judged it to cover data the paper presents as its own results, not literature cited in the introduction. Reconciler to confirm.
- Characterization without uptake rows: none. All three labelled samples have uptake rows.
- No surface area, pore volume or pore size is reported for any sample (relevant to eligibility criterion I4). Tube diameter (1.85 ± 0.05 nm HRTEM; 1.85 and 1.62 nm from Raman RBM 121 and 138 cm-1) and bundle size (~20 nm) are recorded in material_description, not as pore diameters.
- Degassing vacuum "about 1.3 Pa torr in the control experiment": the unit is ambiguous and the value is from a control run, so it was not stored as degas_end_pressure_pa.
- Anode composition (graphite 94.5 at.%, Ni 3, Co 0.75, Fe 0.75 at.%, FeS 1 at.%) is synthesis feedstock, recorded in material_description only.

## Coding decisions needing reconciler attention
- Sample labels follow Table 1 as printed: "1", "2", "3". In the text they appear as "sample 1/2/3" and in the Fig. 3 legend as "Sample 1#/2#/3#".
- Pressure for M1 to M3 is stored as 100 bar (10 MPa). The paper prints "100 to 120 atm", "about 10 to 12 MPa" and "about 10 megapascal" (abstract), and does not state the equilibrium pressure.
- For M4 (0.9 wt% residual), "room temperature" is stored as 298 K because the paper itself gives room temperature as "about 298 K". The pressure is "ambient", so pressure_unstated is true. The value comes from ex situ weighing, so measurement_method is other. It has no isotherm_id because it was not the same instrument run as M3.
- For M5 (<1 wt% below 5 MPa), the sample is unspecified, the pressure is stored as the 5 MPa limit, and the temperature is taken as the paper's 298 K measurement temperature.
- instrument_identified is true for the volumetric rows. The apparatus is described in detail (Fig. 2, components, 45.10 ml system volume) but is not named or explicitly called home-built. calibration_described is false because no method is given for the volume determination.
- Material class is SWCNT, with Ni, Co, Fe recorded as residual catalyst, not as a composite.
