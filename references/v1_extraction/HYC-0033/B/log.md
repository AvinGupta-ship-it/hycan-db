# HYC-0033 extraction log (agent B)

## Sources extracted from
- main p. 2, text: "boron-doped high-surface area carbon (3300 m2/g)" -> BET of S1 (B-doped).
- main p. 3, Experimental, Sample preparation: synthesis (corncob, H3PO4 then KOH activation), decaborane B doping, 1 min neutron irradiation at MURR, H2O2 etch (750 C, 1 h), vacuum anneal 600 C 15 h, boron 1.4 wt% (PGNAA) "in the resulting sample" -> S2 dopant_concentration_wt_pct only.
- main p. 3, Subcritical nitrogen adsorption: Autosorb-1C, N2 77 K, BET range 0.01-0.03 P/P0, areas >1000 m2/g rounded to nearest hundred, V_tot at 0.995 P/P0 (no V_tot value printed).
- main p. 4, Eq. 9 text: skeletal density "assumed to be 2.0 g/cm3" -> skeletal_density_g_cm3 (flagged as assumed).
- main p. 4, Supercritical hydrogen adsorption: H2 99.999%, Hiden HTP-1 volumetric analyzer, excess isotherms at T = 80 K, 1-100 bar; degas 400 C, dynamic vacuum 20 torr, 2 h.
- main p. 4, Results: BET 3300 (before) and 3100 m2/g (after irradiation); porosity 0.79 and 0.78 (in notes); QSDFT main peak 7.5 A in both samples -> average_pore_diameter_nm 0.75.
- main p. 5, Figure 4 (80 K): four isotherms (B-doped excess, B-doped total, irradiated excess, irradiated total). 80 K is outside 76.0-79.0 K, so only the highest-pressure point of each isotherm is a row: M2 (I2), M3 (I3), M4 (I4); M1's marker cross-checked here.
- main p. 6, Figure 5: same excess markers as Figure 4 plus Ono-Kondo fit lines; B-doped excess highest-pressure point taken from here (M1, I1); irradiated excess last marker cross-checked here.
- main p. 8, Author Contributions: "M.B. measured supercritical hydrogen adsorption" -> measuring_lab_id "Beckner group, University of Missouri" (corresponding author J.R. is at Lebanese American University).

## Values seen but not extracted
- Figure 4 / Figure 5: every marker other than the highest-pressure one of each isotherm (80 K is not 77 K by protocol section 3; only the highest-pressure point is digitized at other temperatures). Run sizes: B-doped 31 markers, irradiated 33 markers.
- Figure 5: Ono-Kondo fit curves (model fits of the excess data, not measurements); fit parameters (C, rho_mc, E) are not printed.
- p. 5 text: excess maximum at 23 bar (irradiated) and 40 bar (non-irradiated): pressures only, no uptake value; at 80 K maxima are not extracted.
- p. 5 text: 1 min irradiation "caused only a small increase in hydrogen storage at room temperature": no value, temperature in words only.
- p. 6 text and Conclusion: "at 20 bar the irradiated sample showed an improvement of 9% in storage capacities", "higher storage capacities at pressures below 42 bar": relative comparisons, not uptake values.
- p. 6 text: average binding energies "KJ/mol" (number missing in the print) and 6.6 KJ/mol, "6% increase": not uptake values.
- p. 1 text: DOE targets 0.045/0.055/0.065 kg H2/kg and 0.030/0.040/0.050 kg H2/L: targets, not measurements.
- p. 2 text: literature values (moisture uptake +18%/+23%, area increase <100 m2/g in refs 21, 22): other work, not H2 uptake.
- Figure 3 (pore-size distribution of both samples): not an isotherm; its only quantitative statement (main peak 7.5 A, pores < 40 A) is in the text and recorded.
- Undoped corncob activated carbon (intermediate before B doping): no characterization or uptake reported; no row.
- Boron content: 1.4 wt% is printed for "the resulting sample" after irradiation, etching and annealing; no separate value for the non-irradiated B-doped sample, so S1 has none.
- No non-carbon sorbent is measured.

## Digitization
- Calibration (both figures, on the page images): Fig. 4 x 0 bar at px 382, 100 bar at px 813, check 40 bar at px 554 (0.23% residual); y 0 at px 925, 100 at px 583, check 50 at px 754 (0%). Fig. 5 x 0 at px 377, 100 at px 813, check 50 at px 595 (0%); y 0 at px 456, 60 at px 101, check 30 at px 278 (0.28%). Tick positions found from pixel rows/columns.
- Legends (Fig. 4 x 505-812, y 852-922; Fig. 5 x 525-812, y 360-450) and the in-plot "80K" label (Fig. 4 x 386-432, y 588-616) were whited out in copies of the page images (work/main-5_fig4_legendmasked.png, work/main-6_fig5_legendmasked.png; same pixel coordinates; no data markers in those areas) so that legend symbols were not taken as markers.
- digitize_figure.py `check` was not run: the paper prints no uptake value to check against; archives keep status "unchecked".
- fig4_Bdoped1min_total.json (I4): 32 of 33 markers extracted; the marker at the origin is clipped by both axes and cannot be separated.
- fig4_Bdoped_total.json (I2): 18 of 31 markers extracted; 10 markers below ~10 bar are hidden under the open and blue markers, and 3 markers near 42.5, 47.5 and 52.7 bar are hidden under the irradiated total markers where the curves cross.
- fig4_Bdoped1min_excess.json (I3): region x >= 443 px (P > ~14 bar); 17 of the 20 markers there extracted, no spurious points; markers near 52.8, 76.7 and 87.6 bar not separated (the open-square strokes merge with the same-colour connecting line); the 13 markers below ~14 bar overlap other series and were not separated.
- fig5_Bdoped_excess.json (I1): region x >= 598 px (P > ~51 bar); all 10 markers there extracted. Wider regions gave merged or spurious components because the black Ono-Kondo fit line runs through the open markers; the 21 markers below ~51 bar were not separated.
- Cross-check archives for the highest-pressure excess markers in the other figure: fig4_Bdoped_excess_lastpoint_crosscheck.json (96.089 bar, 42.126 g/kg vs 95.902 bar, 42.299 g/kg used) and fig5_Bdoped1min_excess_lastpoint_crosscheck.json (95.482 bar, 29.831 g/kg vs 95.676 bar, 29.745 g/kg used).
- Marker counts (31 B-doped, 33 irradiated) were made on enlarged crops of Figure 5 (excess only) and agree with the separable Figure 4 total markers, which sit at the same pressures.
