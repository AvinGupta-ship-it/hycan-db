# HYC-0037 extraction log (agent B)

## Sources extracted from

- main p. 3298 (main-2), Section 2 Material and methods: synthesis, HCl purification, BET (multipoint, P/P0 0.05-0.2, N2 at 77 K, ASAP 2020HD88, degas 573 K 8 h), total pore volume at P/P0 0.99, H2 methods (ASAP 2020HD88 volumetric 0-800 mmHg at 77 K after evacuation at 573 K; IGA (Hiden Isochem) gravimetric static mode 0-19 bar at 77 K and 298 K after 10^-6 mbar, 573 K, 10 h; H2 99.999%). Coded on every S1 row.
- main p. 3300 (main-4), XPS/elemental-analysis text: 1.5 at% N (XPS), N/C close to 0.015 (elemental analysis), N and C bonding assignments. Coded on S1 rows.
- main p. 3301 (main-5), text: BET 135 m2/g and total pore volume 0.38 cm3/g; 0.21 wt% at 1 bar (Fig. 5a); "reported as excess uptake" (Fig. 5b); maximum 1.21 wt% at 7 bar; 0.17 wt% at 298 K and 19 bar (Fig. 5c, "excess"). Same values as Table 1; merged into the Table 1 rows.
- main p. 3301 (main-5), Table 1: all uptake cells extracted (this work: 3 rows merged with figure points; literature columns: 10 rows).
- main p. 3301 (main-5), Fig. 5a (77 K, 0-800 mmHg): 21 markers counted, 18 extracted by the tool (archive HYC-0037_fig5a_77K_lowP.json); the 750 mmHg point is merged with Table 1 0.21 wt% (1 bar). Calibration x: 0 mmHg at px 190.41, 800 at 579.06, check 400 at 385.03 (0.15%); y: 0.00 at px 431.0, 0.25 at 159.49, check 0.10 at 322.50 (0.10%). Check against stated 0.21 at 750.06 mmHg: 3.8%, pass.
- main p. 3301 (main-5), Fig. 5b (77 K, 0-19 bar): 11 markers counted, 11 extracted (archive HYC-0037_fig5b_77K_highP.json); 7 bar point merged with Table 1 1.21 wt%. Calibration x: 0 bar at px 191.39, 20 at 586.55, check 10 at 388.65 (0.16%); y: 0.0 at px 761.64, 1.5 at 493.52, check 0.6 at 654.47 (0.07%). Check against stated 1.21 at 7 bar: 0.11%, pass. Solid line through the markers not digitized (markers present).
- main p. 3301 (main-5), Fig. 5c (298 K, 0-19 bar): 11 markers counted and extracted (archive HYC-0037_fig5c_298K.json); only the highest-pressure point used, merged with Table 1 0.17 wt% (19 bar). Calibration x: 0 at px 190.41, 20 at 586.56, check 10 at 388.43 (0.03%); y: 0.00 at px 1095.48, 0.20 at 827.61, check 0.08 at 988.54 (0.19%). Check against stated 0.17 at 19 bar: 2.5%, pass.
- main p. 3297 (main-1), Introduction: 0.25 wt% (N-doped mesoporous carbon, ref. [8]) and 0.16 wt% (pure mesoporous carbon, ref. [8]) at 50 bar and room temperature; extracted as cited values.
- main p. 3298 (main-2), Introduction: 0.34 wt% at room temperature and 100 bar (N-enriched graphitic carbons, ref. [11]); extracted as a cited value.
- main p. 3302 (main-6), Discussion: N-doped microporous carbon [13] 1663 m2/g, "up to 0.15 wt%" (same as Table 1, merged); 0.17 wt% for this work (same as Table 1).
- Abstract (p. 3297) and Conclusions (p. 3302): 0.21 wt% (1 bar), 1.21 wt% (7 bar), 0.17 wt% (298 K, 19 bar), 1.5 at%, 135 m2/g, 0.38 cm3/g; duplicates of Table 1, no separate rows.

## Coding decisions worth checking

- Literature comparison values (Table 1 columns for refs. [20], [11], [8], [13]; introduction values for refs. [8], [11]) were extracted under the "values reported before" rule, with `previously reported: [n]` in notes, area_same_sample = other_paper, measurement_method unknown, basis_inferred unknown. Their measuring laboratory is not printed, so measuring_lab_id is "unknown (cited ref. [n])". If these are judged out of scope, rows M31-M43 are the cited values.
- 3D-meso-CN [8] (mesoporous carbon nitride) is treated as a carbon sorbent because the paper groups it with N-doped carbon materials and calls it "N-doped mesoporous carbon"; its composition is not given.
- The introduction's "N-doped mesoporous carbon" [8] is taken to be the same material as Table 1's 3D-meso-CN [8], and the introduction's "N-enriched graphitic carbons" [11] the same as Table 1's N-enriched graphitic C [11]; the paper does not say so explicitly.
- The room-temperature values (0.25, 0.16, 0.34 wt%) have temperature_unstated = true and are not grouped with the 298 K Table 1 values.
- Table 1 values for one cited sample at one temperature and several pressures were grouped as one isotherm (I4: 3D-meso-CN 77 K, 1 and 50 bar; I5: ref. [20] 77 K, 1 and 16 bar), as the rule requires when no curve is plotted and no run split is stated.
- Text calls ref. [20] "Zhong et al."; the reference list gives [20] as Jin Z et al. (J Am Chem Soc 2010).
- S1 class doped_carbon (N 1.5 at%); the "small amount of iron residue" is recorded as residual_metal_element = Fe, not as a composite phase.
- Fig. 5b basis: "reported as excess uptake [40,41]" names the basis without defining it, so basis_stated = false, basis_inferred = excess. Fig. 5a: basis not named, volumetric default excess. Fig. 5c: "excess hydrogen adsorption isotherm", named without definition.
- IGA (Hiden Isochem) treated as manufacturer plus model (instrument_identified = true); the IGA variant is not printed.
- replicates_reported = false: no error bars or uncertainties; Fig. 5a (volumetric) and Fig. 5b (gravimetric) at 77 K are different measurements, not presented as repeats.
- Table 1 prints "0.21(1 bar)" without qualifier while the text says "about 0.21 wt%"; coded exact from the table. The pressure-matching rule ties it to the 750 mmHg (1.0005 bar) point, digitized at 0.2021 wt%; the 800 mmHg end point (0.2076 wt%) is 6.7% away in pressure.

## Values seen but not extracted

- Fig. 5a: three overlapping markers at about 0-12 mmHg (near 0.007-0.016 wt%) merge into one blob (100 px, centroid px 193.75, 418.2) that the tool cannot separate; it was rejected (marker-max-px 70) and is listed under rejected_markers in the archive. No rows for these three points; they are counted in isotherm_point_count = 21.
- Fig. 5c: the 10 points below 19 bar (298 K isotherm; only the highest-pressure point of a non-77 K isotherm is extracted).
- Badzian et al. [19]: "0.7-0.8 wt% uptake at ambient temperature and 7 MPa in the N doped carbon" (1 at% N, several forms: nanotubes, nanoparticulates, rings); a range across several material forms, not a value for one sample.
- Table 1: "Not given" cells (ref. [20] at 298 K; N-doped micro C [13] at 77 K).
- Ref. [20] BET surface area printed as a range "200-300" m2/g; not stored as a number (noted on its rows).
- Fig. 4: N2 adsorption-desorption isotherm at 77 K of S1 (type IV, hysteresis at P/P0 0.4-1.0); characterization, not digitized; its BET area and pore volume are taken from the text.
- Fig. 2: XPS C 1s (284.5, 285.3, 289.7 eV) and N 1s (396.9, 400.3, 405.0 eV) peaks of S1; characterization only.
- Fig. 3: Raman spectrum of S1, D band about 1288 cm-1, G band about 1602 cm-1, ID/IG = 1.14; characterization only.
- Fig. 1a: product of melamine/FeCl3 pyrolysis at 873 K after 773 K for 2 h (graphitic microsheets); SEM image only, no H2 uptake, so no row.
- Fig. 1b-f: SEM/TEM/HRTEM of S1 (diameters 50-400 nm, wall thickness about 10-20 nm); characterization, in material_description.
- Average pore size of S1: method stated (N2 adsorption volume at P/P0 0.99) but no value printed.
