# HYC-0122 extraction log (extractor B)

Input: page images main-01..12, si1-01..11. 9 rows written.

## Samples (numbered by first appearance; carbon sorbents only)

- S1 PdP/P-rGO-2 (abstract, "Pd3P nanoparticles decorated P-doped graphene") - rows M1-M6.
- S2 Pd-rGO (sec. 2.1) - rows M7-M8.
- S3 P-rGO (sec. 2.1 support; sec. 2.3 gives a second recipe, 25 mg PPh3, 2 h; the paper does not say which was measured) - no row; uptake only in figures (see below). Characterization: Raman ID/IG = 1.15 (Fig. S7(b)).
- S4 Pd+P-rGO (sec. 2.1) - row M9.
- S5 PdP/P-rGO-1, S6 PdP/P-rGO-3, S7 PdP/P-rGO-4, S8 PdP/P-rGO-5 (sec. 2.2; PPh3 10, 100, 400, 1000 mg) - no rows; uptake only in Fig. 2(b). Characterization: SEM, XRD phases (Fig. 1): -1 Pd; -3 Pd3P + Pd5P2; -4 Pd5P2; -5 Pd5P2 + Pd7P3. No surface area.
- S9 rGO (sec. 2.3) - no row; uptake only in figures. Characterization: Raman ID/IG = 0.92 (Fig. S7(b)).
- S10 Pd3P + rGO (sec. 2.3 "PdP+rGO"; label from Fig. S5) - no row; uptake only in Fig. S5(b). Characterization: XRD (Fig. S5(a)), SEM agglomeration (Fig. S6).
- S11 Pd3P + P-rGO (sec. 2.3 "PdP+P-rGO"; label from Fig. S5) - no row; uptake only in Fig. S5(b). Characterization: XRD (Fig. S5(a)), SEM (Fig. S6).
- PdP (palladium phosphide particles alone, sec. 2.3) is not a carbon sorbent and has no H2 value.

## Sources extracted

- Main p.1 abstract: 3.66 wt% (298 K, 4 MPa) -> M1; 3.94 wt% (253 K) -> M2; 4.7 wt% (5.5 MPa, 298 K) -> M3; 2.63 wt% after 4 cycles -> M5.
- Main p.4 sec. 3.1 and p.6 sec. 3.3: 3.66 wt% (PdP/P-rGO-2) -> M1; Pd+P-rGO 1.92 wt% -> M9; Pd-rGO 1.64 wt% -> M7.
- Main p.7: 3.94 wt% at 253 K -> M2; 4.7 wt% at 5.5 MPa -> M3; residual about 1.15 wt% -> M4; 2.63 wt% after 4 cycles -> M5; Pd-rGO initial 1.64 wt% -> M7.
- Main p.8: 124.55 and 102.77 cm3(STP)/g at 100 kPa -> M6, M8.
- Main p.10 and conclusions: restatements of 3.66, 2.63, 4.7, about 1.1 wt% (residual, M4 notes).
- SI p.S2 Table S1 "This work" row (15, 25 C, 4 MPa, 3.66 wt%) -> M1.
- Fig. 6(d) (PCT isotherm, 298 K): digitized both series; used for the highest-pressure point (merged with M3) and for the residual marker (merged with M4). Archives fig6d_PdP-P-rGO-2_adsorption.json, fig6d_PdP-P-rGO-2_desorption.json.
- Fig. 9(a) (low-pressure isotherms, 298 K): digitized both series; highest-pressure points merged with M6 and M8. Archives fig9a_PdP-P-rGO-2.json, fig9a_Pd-rGO.json.
- Characterization: Fig. 5(b),(c) and p.5-6 text (BET 288.4, 232.5, 252 m2/g; pore volume 1.019, 0.959, 0.988 cm3/g); sec. 2.4, 2.5.

## Digitization details

- Fig. 6(d), main-07.png: x axis linear, ticks 0 (px 738.5) and 5 (px 1038), check tick 3 (px 918, residual 0.11%). y axis log; only two labelled ticks, 1 MPa (px 680.5) and 10 MPa (px 508.5); no third labelled tick exists, so the y check used the unlabelled minor tick 5 MPa (px 560, residual 0.37%); minor tick positions down to 0.2 MPa match the log scale. Points below 1 MPa (including the residual marker at 0.253 MPa) are extrapolations of the 1-10 MPa calibration (flagged by the tool).
- Fig. 6(d) preprocessing (copies in work dir only): legend and the red "1.15 wt%" / "3.55 wt%" labels whited out (main-07_masked.png). Open (hollow) desorption diamonds share colour with their connecting line, so their enclosed interiors (<= 60 px) were filled with the series colour (work/scripts/fill_open_markers.py -> main-07_masked_openfilled.png) before --mode markers.
- Fig. 6(d) counts: desorption (open) 12 counted, 12 extracted. Adsorption (filled) 10 counted, 9 extracted: the filled marker at ~5.0 MPa is mostly hidden under an open marker and could not be separated. No adsorption marker is visible at 5.5 MPa (only the open diamond). Isotherm point count recorded as 22.
- Fig. 6(d) checks: desorption series at 4.70 wt% gives 5.48 MPa vs stated 5.5 MPa (pass); adsorption series checked at 4.0 wt% against the nominal 4.5 MPa step of sec. 2.5.2 (pass; weak check, the step pressure is nominal).
- Fig. 9(a), main-09.png: x ticks 0 kPa (px 261.5) and 120 kPa (px 596), check 60 (px 428.75, residual 0); y ticks 0 (px 1149) and 160 (px 873), check 80 (px 1011, residual 0). Legend and the "124.55" / "102.77" labels whited out in a copy (main-09_masked.png).
- Fig. 9(a) counts: PdP/P-rGO-2 18 markers counted, 17 extracted: the lowest red marker (~4 kPa) is overdrawn by Pd-rGO stars and fragments into groups below the size threshold. Pd-rGO 20 counted, 19 extracted: the two lowest stars (~1-2 kPa) overlap and merge into one centroid. A red marker fully hidden under an orange star would not be countable. Checks: 124.55 at 99.32 kPa (0.02%), 102.77 at 99.36 kPa (0.16%), pass.

## Judgement calls

- M1 (3.66 wt%, 4 MPa) and M5 (2.63 wt%, 4 MPa) are within 2% in pressure of Fig. 6(d) PCT markers at ~3.98 MPa, but the paper attributes them to the separate kinetic and cycling tests, and those PCT markers digitize at 3.023 wt% (adsorption) and 2.703 wt% (desorption). They were not merged and carry no isotherm_id.
- The cycled value (M5) is kept under sample S1 (same physical sample, after 4 cycles); area_same_sample = unclear because the BET area is for the as-prepared state and the cycled material contains H0.6P3.2Pd12.
- Instrument for Fig. 9(a) printed as "Mike TriStar II 3020": coded instrument_identified = true (model named). Sieverts apparatus: false (no model, not stated home-built).
- Pore volume 1.019 cm3/g called "microporous volume" in text but "Pore Volume" in Fig. 5(c): recorded as total pore volume. "Average pore radius of about 2.8 nm" not recorded (radius vs width ambiguity).

## Values seen but not extracted

- Fig. 2(b) bar labels (298 K, 4 MPa, kinetic, not in text): PdP/P-rGO-1 1.83, PdP/P-rGO-3 3.40, PdP/P-rGO-4 3.05, PdP/P-rGO-5 2.33 wt%; increments over Pd-rGO 0.19, 2.02, 1.76, 1.41, 0.69 wt%. Bar chart, not digitized.
- Fig. 6(b) and Fig. S7(a) labels: P-rGO 1.22 wt%, rGO 0.94 wt% (298 K, 4 MPa); not given as these samples' uptakes in text. Bar/kinetic figures.
- Fig. 6(c) inset: PdP/P-rGO-2 3.66 wt% at 293 K and 2.80 wt% at 333 K (4 MPa); text gives only the 253 K value. Bar chart. (The 293 K label 3.66 equals the 298 K value of M1.)
- Fig. 7(b): Pd-rGO cycle capacities Cyc-1 1.21, Cyc-2 0.85, Cyc-3 0.57, Cyc-4 0.33 wt%; text gives only "a decrease of about 80%". Cycling bar chart.
- Fig. 7(d): "28.1%" decrease; Cyc-1 to Cyc-3 bars unlabelled. Cycling bar chart.
- Fig. S5(b): Pd3P + P-rGO 2.72 wt%, Pd3P + rGO 2.21 wt% (298 K, 4 MPa); text says only that they exceed Pd+P-rGO (1.92 wt%) and Pd-rGO (1.64 wt%). Kinetic figure. That comparative statement was not coded as lower bounds.
- Kinetic (uptake vs time) curves Figs. 2(a), 6(a), 6(c), 7(a), 7(c), S5(b), S7(a): not isotherms, not digitized.
- Fig. S4: percentage of uptake in the first 2 h (65.6, 59.3, 58.0%): kinetic ratio, not uptake.
- Main p.7 and Fig. 6(d): desorption capacity 3.55 wt% ("about 75.5%" of total): released amount (difference 4.7 - 1.15), not an equilibrium uptake.
- Abstract: "1.03 wt% of the capacity loss" and p.7 "decrease rate of about 28%": differences between M1 and M5.
- Main p.6-7: partition of the 3.66 wt% into 0.94 wt% (25.7 at% H, rGO surface), 0.28 wt% (7.8 at%, P-doping sites), 0.01 wt% (0.3 at%, Pd3P; "calculated" from hydride stoichiometry), 2.43 wt% (66.3 at%, spillover), 1.22 wt% physical and 2.44 wt% chemical: computed attributions, not measurements.
- Main p.9: H:Pd ratios 1.53 (PdP/P-rGO-2) and 1.29 (Pd-rGO), threshold 0.77: derived from M6/M8.
- Main p.2: ~72.5% decay of Pd/N-rGO after three cycles: the authors' earlier work, no value for this paper's samples.
- Main p.1-2 introduction (Bakhshi et al. 437%, etc.) and SI Table S1 rows other than "This work" (Pd bulk 0.56, Pd nanoparticles 0.72, Pd/super activated carbon 1.15, Pd/activated carbon 0.7, Pd/SWNT 0.5, Pd/MWNT 0.35, Pd/N-doped graphite nanoplatelets 1.25, Pd/acid-functionalized FLG 1.76, Pd/graphite oxide 0.95, Pd/N-doped FLG 2.3, Pd/graphene nanocomposites 7.16 wt%): values from other papers; Pd bulk and Pd nanoparticles are not carbon sorbents.
- SI Fig. S1 / main sec. 2.5.1: LaNi5 used to calibrate the Sieverts system; no LaNi5 uptake value printed.
- Other characterization not mapped to fields: Raman ID/IG 1.15 (PdP/P-rGO-2), 1.21 (Pd-rGO), 1.25 (Pd+P-rGO), 1.16 after cycling; XPS P 2p fractions (PdP/P-rGO-2 P-O 43.6%, P-C 38.9%, P-Pd 17.5%; after cycles 26.7/47.6/25.7%; Pd+P-rGO P-O 43.3%, P-C 33.3%, P 23.4%); Pd 3d fractions (Fig. 8(f)); Scherrer grain sizes 23.2, 21.3, 20.5 nm (Fig. S3); SEM particle size ~20 nm (Fig. S2); lattice fringe 0.248 nm (Pd3P (031)).
