# HYC-0109 extraction log (extractor B)

Paper: Burress et al. 2009, Nanotechnology 20, 204026, "Hydrogen storage in engineered carbon nanospaces". 110 rows. Samples: S1 = Batch 5.1, S2 = S-33/k (order of first appearance, Table 1). Laboratories (Table 1, "independent laboratories"): U. Missouri, Hiden HTP1, Hiden IGA-001; coded as a multi-laboratory paper (labels "<sample> / <laboratory>", measuring_lab_id "<laboratory> (HYC-0109)").

## Sources extracted

- main-01.png: IOPscience download cover page. No data.
- main-03.png (p.2) Table 1: 12 rows (M1-M12). U. Missouri ranges (1.0-1.1, 7.8-9.1, 0.9-1.1 wt% with g/l ranges) each stored as a lower-bound row and an upper-bound row. Hiden HTP1 values: 7.0 wt% (83 K, 50 bar) not merged (no plotted point within 2% of 50 bar), 1.1 wt% (303 K, 50 bar) merged with the Figure 1 bottom-right 303 K desorption marker at 49.146 bar, 1.8 wt% (303 K, 80 bar) merged with the 303 K adsorption marker at 80.372 bar. Hiden IGA-001 values (footnote a, extrapolated) coded fitted_extrapolated. g l^-1 values stored as volumetric_capacity_kg_m3 (basis other, includes compressed gas). Basis total (Table 1 "H2 storage" = the paper's total amount stored; checked against the Figure 1 stored curves).
- main-03.png (p.2) section 1 and main-10.png (p.9) section 8: "storage capacities up to 100 g H2/kg (90 bar, 83 K) and 20 g H2/kg (90 bar, 303 K)": M13 (100 g/kg, no isotherm_id, fitted_extrapolated: the 83 K curve ends at 80.3 bar, 92.9 g/kg) and M14 (20 g/kg, merged with the top of the Figure 1 bottom-right 303 K curve, 89.946 bar, 20.007 g/kg). Sample identified from the temperatures (83 K and 303 K data exist only for Batch 5.1 on the Hiden HTP1).
- main-03.png (p.2) section 2: excess and total-amount-stored definitions (basis_evidence), H2 purity 99.999%, instruments, rho_a = 0.58 (S-33/k) and 0.42 (Batch 5.1) g/cm3 and rho_s = 2.0 g/cm3 (coded on every row).
- main-04.png (p.3) section 3: absolute-adsorption definition (basis_evidence); Quantachrome Autosorb-1-C N2 isotherms.
- main-05.png (p.4) section 3/4 text: structural data rho_a = 0.5, rho_s = 2.0 g/cm3 for eqs (2)-(4) (noted on rows); Sigma = 2100 m2/g for S-33/k used to convert simulations (noted on S-33/k rows).
- main-04.png (p.3) Figure 1 top-left (S-33/k excess, Hiden IGA-001): 77 K adsorption 21 rows (M15-M35), 77 K desorption 11 rows (M36-M46), 293 K adsorption highest-pressure point (M47).
- main-04.png (p.3) Figure 1 top-right (Batch 5.1 excess, Hiden HTP1): 83 K and 303 K highest-pressure points (M48, M49), taken from the desorption markers because the adsorption markers at the top of each curve lie under them.
- main-04.png (p.3) Figure 1 bottom-left (S-33/k total amount stored): 77 K adsorption 21 rows (M50-M70), desorption 11 rows (M71-M81), 293 K highest-pressure point (M82).
- main-04.png (p.3) Figure 1 bottom-right (Batch 5.1 total amount stored): 83 K highest-pressure point (M83, desorption marker, adsorption marker hidden under it); 303 K points used for the merged Table 1 and text rows (M4, M5, M14).
- main-06.png (p.5) Figure 5 left, "experimental data" (S-33/k absolute, 77 K): all 23 markers (M84-M106).
- main-06.png (p.5) Figure 5 right, "experimental data" (298 K as printed): highest-pressure point (M107).
- main-08.png (p.7) Figure 7 top-left (S-33/k absolute, 293 K adsorption): highest-pressure point (M108).
- main-08.png (p.7) Figure 7 bottom-right (Batch 5.1 absolute, 83 K): highest-pressure point (M109); Figure 7 top-right (Batch 5.1 absolute, 303 K): highest-pressure point (M110).
- main-09.png (p.8) Table 5 and section 7 text: BET (N2, 0.01-0.03 p/p0, 0.162 nm2), NLDFT total pore volume, pore volume <10 A (stored as ultramicropore volume, cutoff 1.0 nm), pore width mode (stored as average_pore_diameter_nm, DFT), on every row; NLDFT surface area and porosity in notes.
- main-11.png (p.10): references only. No data.

## Digitization

- Calibration: every axis on its lowest and highest labelled ticks with a third labelled tick as check; tick pixels found by scanning pixel rows and columns for black tick marks. All checks within 0.6% (archives record the residuals).
- Legends inside the plot areas were painted white in working copies of the page images (work/p04_f1_legendmasked.png, p06_f5_legendmasked.png, p08_f7_legendmasked.png) so the legend markers are not counted; no data marker lies in a masked box. Archives cite these copies with their sha256.
- Marker counts (tool count vs my count): Figure 1 S-33/k 77 K adsorption 21 of 23 in both panels (two squares at about 0.35 and 0.51 bar lie under desorption circles and cannot be separated); 77 K desorption 11 of 11; Figure 5 left 23 of 23. For non-77 K curves only the highest point is needed; their low-pressure markers overlap (Figure 1 and Figure 7 near the origin, Batch 5.1 83 K desorption below 15 bar), so isotherm_point_count is a stated lower bound for I1/I7 (29), I2/I8 (24), I4/I6 (28), I10 (19), I11 (20), I12 (18), I13 (14).
- The three lowest S-33/k 77 K adsorption squares in Figure 1 are clipped by the left axis frame: digitized pressures (0.215, 0.215, 0.258 bar) are biased high by up to about 0.1 bar (confidence 3). Adsorption squares partly covered by neighbouring desorption circles in Figure 1 may be shifted by up to about 1.5 px (0.13 bar).
- Figure 7 77 K squares are crossed by the fit lines above 10 bar and split in two by the tool; the 15 separable ones agree with the Figure 5 left experimental points within digitization resolution, so this isotherm is extracted once from Figure 5 left (comparison archive f7TL_S33k_absolute_77K_ads_comparison.json, not used for rows). The Figure 7 bottom row re-plots the top-row points (the paper says so) and is not extracted twice.
- digitize_figure.py check: passed for f1BR_B51_stored_303K_ads.json (80 bar vs 18 g/kg; 50 bar vs 11 g/kg), f1BR_B51_stored_83K_ads.json and f1BR_B51_stored_83K_des.json (50 bar vs 70 g/kg), f1BR_B51_stored_303K_des_rerun.json (89.9 bar vs 20 g/kg). All other archives remain "unchecked" because the paper states no value on those curves.
- f1BR_B51_stored_303K_des.json is marked "discarded": after a passing check at 89.9 bar I also checked its interpolated value at 50 bar against Table 1's 1.1 wt% (11.90 vs 11 g/kg, 8.2%). That comparison was misdirected: Table 1's value matches the adsorption branch (11.17 g/kg at 50 bar, check passed), not the desorption branch. The series was re-extracted with identical parameters as f1BR_B51_stored_303K_des_rerun.json (identical points), which the rows cite; the discarded archive is kept for the record.

## Values seen but not extracted

- Abstract: "~80 g H2/kg carbon, ~50 g H2/liter carbon, at 50 bar and 77 K": rounded summary of the Table 1 S-33/k values from two laboratories (U. Missouri 7.8-9.1 wt%, 45-53 g/l; Hiden IGA-001 7.6 wt%, 40 g/l); no sample or laboratory stated; treated as a cross-laboratory summary, not a row.
- Figure 1, Figure 5, Figure 7 non-77 K isotherms (Batch 5.1 83 K and 303 K, S-33/k 293 K and 298 K): all points other than the highest-pressure point (protocol: other temperatures, highest point only), except points merged with Table 1/text values.
- Figure 1 adsorption markers at the top of the Batch 5.1 83 K and 303 K curves (excess and stored): hidden under desorption markers, not separable; the coincident desorption markers were digitized instead.
- Figure 5 left/right simulated points (slit thickness 6.7, 10.1, 13.5 A, 77 K and 298 K): molecular-dynamics results, not measurements.
- Figure 6: theoretical Langmuir excess isotherms (localized/mobile, 77 K and 293 K): computed, not measured.
- Figure 7 one- and two-binding-energy fit lines (77/83 K solid, 293/303 K dashed): model fits, not data.
- Table 2: alpha(T) 6.4 and 11.2 A2 (simulation); theta m Sigma m_s / m^e_ads 7.5 and 15.1 A2 at 47 bar; "experimental upper bounds" m Sigma m_s / m^e_ads 13.4 A2 (77 K, 47 bar) and 148 A2 (293 K, 47 bar), "calculated from experimental data for S-33/k in figure 1, extrapolated to 47 bar": areas per molecule, not H2 uptake values.
- Table 3: binding energies and site fractions (S-33/k 77 K: 6.4 and 8.6 kJ/mol, 61% and 39%; Batch 5.1 83 K: 4.8 and 9.0 kJ/mol, 75% and 25%; uncertainties <0.5 kJ/mol and 10%): not uptake values.
- Table 4 and Figure 8: adsorption/desorption times and coverage kinetics (simulation and theory): not uptake values.
- Figures 3 and 4: simulation cell, potentials and density profiles: not uptake values.
- Figure 9: NLDFT pore size distributions (characterization; Table 5 values used). Caption: Batch 5.1 has the larger nanopore volume and area but lower uptake than S-33/k (qualitative).
- Section 4/5 text: E_B 5.3 and 8.1 kJ/mol (simulated), 5.0 kJ/mol (graphite, literature): not uptake values.
- Table 1 cells marked "-" (Batch 5.1 U. Missouri at 77 K/50 bar and 293 K/80 bar; S-33/k U. Missouri at 293 K/80 bar): no value.
- No non-carbon reference material is measured in the paper.

## Coding decisions worth review

- Basis: excess, total and absolute are each named and defined, and Figure 1 shows excess and total side by side, so basis_stated = true on every row; Table 1 and the text "storage capacities" are coded total (stated) because the paper's storage quantity is its defined total amount stored and the checkable values match the stored curves.
- measurement_method = unknown on every row: the paper says "measured gravimetrically and volumetrically" on the three instruments without saying which method each used.
- Laboratory of the absolute isotherms (Figures 5 and 7) inferred from the Figure 1 runs (same pressures; Batch 5.1 cryogenic data exist only from the Hiden HTP1); the paper does not name the instrument.
- Figure 5 right ("298 K") and Figure 7 top-left ("293 K") room-temperature absolute data look like the same points; both recorded as printed (M107, M108).
- replicates_reported = true at sample level (two laboratories measured each sample, Table 1); no numerical uncertainty is given for any uptake value.
- area_same_sample = yes although Table 5 is introduced as "our typical BET surface areas"; Figure 7 caption assigns the areas to the two samples.
