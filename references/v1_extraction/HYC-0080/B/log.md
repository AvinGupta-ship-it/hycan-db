# HYC-0080 extraction log (agent B)

Pages: main-01..13 (journal pp. 30-42), si1-01..12. Page references below are file pages, with journal pages in brackets.

## Sources extracted from

- Table 4, main p.8 [p.37]: 20 values (excess and total H2 uptake at 77 K and 298 K, 25 bar, for M-C-800, M-C-4-700, M-C-4-800, M-C-KOH-4-800, M-C-APS-4-800), one row each. The same values repeated in text Sec. 3.3 (pp.7-8), Table 5, SI Table S1, the abstract and the conclusion are the same measurements, so they get no extra rows.
- Fig. 7a, main p.8 [p.37], 77 K isotherms, closed = adsorption, open = desorption. Axes calibrated on x 0 at 213.38 px and 30 at 594.26 px (15 at 403.29 px gives 14.958, 0.28%), and on y 0 at 636.58 px and 6 at 360.68 px (3 at 498.30 px gives 3.007, 0.24%). Digitized markers, adsorption + desorption: M-C-800 20+23, M-C-4-700 21+27, M-C-4-800 33+41, M-C-KOH-4-800 29+33, M-C-APS-4-800 19+26. That is 272 markers; 2 of them are merged with Table 4 values, so 270 digitized rows.
- Fig. 7b, main p.8 [p.37], 298 K isotherms. Axes calibrated on x 0 at 679.32 px and 30 at 1059.54 px (15 at 869.72 px gives 15.023, 0.15%), and on y 0 at 642.91 px and 0.3 at 360.69 px (0.1 at 548.80 px gives 0.100, 0.04%). Only the highest-pressure marker of each isotherm is digitized, plus the marker used to test each merge with Table 4.
- Text Sec. 3.3, main p.8 [p.37]: "higher H2 uptake at 1 bar and 77 K (2.7 wt%)" for M-C-KOH-4-800. One row.
- Text Sec. 3.3, main p.7 [p.36] with SI Fig. S2(a), p.2: "126.6 cm3 g-1" of H2 on M-C-800. Merged with the highest relative-pressure marker of the Fig. S2(a) H2 isotherm. Axes calibrated on x 0 at 459 px and 1.0 at 864 px (0.4 at 621 px, 0.0%), and on y 0 at 1194 px and 140 at 874 px (80 at 1012 px gives 79.6, 0.47%).
- SI Fig. S3, p.3: M-C-KOH-4-800 '1st' and 'Last' H2 isotherms. The temperature is not stated, so only the highest-pressure marker of each is digitized. Axes calibrated on x 0 at 311 px and 30 at 927 px (15 at 619 px), and on y 0 at 1021 px and 10 at 571 px (4 at 841 px), both 0.0%.
- Table 2, main p.7 [p.36]: BET area, Vtot (DFT), Vmicro (DR), Vmeso (Vtot - Vmicro) and QSDFT pore diameters, copied to every row of each sample. Where two diameters are printed, the first is stored and both are given in notes.
- Table 1, main p.4 [p.33]: EDS composition in at%. S is stored as dopant (method other = EDS); residual K/Ca are given in notes because they are at%, not wt%.
- Sec. 2.2-2.4, main pp.2-3 [pp.31-32]: synthesis, N2 physisorption at 77 K, degassing, and the PCTPro-E&E (Setaram) Sieverts apparatus with ~200 mg sample, 12 h at 200 C and 99.999% H2. The free-volume determination is not described.
- Sec. 2.3 and Figs. 2-5, main pp.3-6 [pp.32-35]: FTIR functional groups copied to functional_groups. Raman, XRD and SEM have no schema field (listed below).

## Coding decisions

- measuring_lab_id: the first author in byline order who carries a corresponding mark is Kiyoung Lee (b, **), so "Lee group, Kyungpook National University". The paper does not say where H2 was measured.
- Basis: Table 4 prints excess and total side by side and its caption names "Excess and total H2 uptake capacities ... at 77 and 298 K". So basis_stated = true for the 77 K and 298 K excess columns and for both total columns, and the Fig. 7a/7b isotherms carry the same coding. The 2.7 wt% text value names no basis (volumetric default: excess). Fig. S3 is called "excess" in the text but not defined (basis_stated false, inferred excess).
- Merge rule (plotted marker within 0.5 bar of the printed 25 bar):
  - Merged: 77 K M-C-KOH-4-800 (marker at 25.21 bar, 4.720 wt%) and M-C-4-800 (25.254 bar, 3.612 wt%); 298 K M-C-800 (24.987 bar), M-C-KOH-4-800 (25.035 bar) and M-C-APS-4-800 (24.706 bar).
  - Not merged, because the nearest marker is outside 0.5 bar: 77 K M-C-800 (25.61 bar), M-C-4-700 (26.00 bar, 3.330 wt%, which matches the printed 3.32) and M-C-APS-4-800 (26.24 bar); 298 K M-C-4-700 (24.474 and 25.894 bar). These table rows have no isotherm_id, because the paper's "as shown in Fig. 7a and Table 4" does not say the value was taken from a specific point. The reconciler may want to review the M-C-4-700 77 K case.
  - 298 K M-C-4-800: the marker near 25 bar is almost completely hidden under the M-C-APS-4-800 marker; only a 1-px L-shaped edge is visible. Its digitization (24.908 bar, 0.0940 wt%), together with the highest marker, failed digitize_figure.py check against the printed 0.10 at 25 bar: 0.0939, 6.1% > 5%. That archive was set aside (work/dz/final/fig7b_M-C-4-800_298K_two-point_DISCARDED.json), so the table value is not merged. The fully visible highest-pressure marker (26.249 bar, 0.0924 wt%) was re-digitized alone into fig7b_M-C-4-800_298K.json.
- Digitizer checks against Table 4 at 25 bar passed for all five 77 K adsorption archives (0.06-1.32%) and for the 298 K M-C-4-700, M-C-KOH-4-800 and M-C-APS-4-800 archives (1.3-2.5%). The 298 K M-C-800 archive could not be checked, because 25 bar is outside its digitized range (23.49-24.99 bar). The desorption, S2 and S3 archives are unchecked because no value is printed for them.
- Fig. S2(a) H2 isotherm: the temperature, the instrument and P0 are not stated, and the x-axis is relative pressure. So temperature and pressure are unstated, measurement_method and basis_inferred are unknown, and degassing, mass and purity are left empty. The highest plotted marker is an open symbol at P/P0 1.006, 126.7 cm3/g; the text calls the value the amount adsorbed, so the row is coded adsorption. Point count about 45 (21 closed + 24 open; low-pressure markers overlap).
- Fig. S3: the '1st' isotherm may be the same run as the Fig. 7a M-C-KOH-4-800 adsorption branch, but the paper does not say, so it is kept as its own isotherm. Point counts are left empty because markers below ~7 bar overlap too much to count.
- replicates_reported = true for the M-C-KOH-4-800 77 K rows, the 2.7 wt% row and the S3 rows, because Fig. S3 shows a first and a repeated H2 isotherm and the text cites it for reproducibility. It is false for the 298 K rows and all other samples.
- material_class = doped_carbon for all five samples, because the paper reports natural S/O doping, with S confirmed by EDS (Table 1) and FTIR. M-C-4-700 has no EDS row, so its S concentration is left empty.
- 298 K point counts (Fig. 7b, counted on the plot, approximate where markers are hidden): M-C-800 16, M-C-4-700 22, M-C-4-800 18, M-C-KOH-4-800 17, M-C-APS-4-800 18.

## Fig. 7a: markers not separated, and other digitization issues

- In every series the lowest-pressure markers form a dense stack or a solid column along the y-axis. Those markers could not be separated or counted, so isotherm_point_count is the count of separated markers (a lower bound). Not extracted:
  - M-C-KOH-4-800: adsorption below ~2.2 bar (< 3.3 wt%), a solid green column x < ~1.2 bar plus a stack to 2.2 bar; desorption below 0.95 bar and some open markers between 1.0 and 1.5 bar that show only as border lines.
  - M-C-4-800: adsorption below ~1.3 bar; desorption below ~0.7 bar. A white slit at ~0.57 bar bordered by both green and blue (classification 0.50) is not counted.
  - M-C-4-700: adsorption below ~3.7 bar, where closed markers are hidden under the open-marker stack; desorption below ~1.4 bar.
  - M-C-APS-4-800: adsorption below ~4.4 bar, a solid orange column x < ~1.5 bar plus a stack; desorption between ~0.6 and 1.8 bar where only border lines show, and below 0.56 bar.
  - M-C-800: adsorption below ~3.5 bar; desorption below ~1.7 bar, under the orange column.
- Many closed markers are partly covered by open markers drawn over them, and sometimes an open marker sits almost exactly on its closed marker. The value is the centroid of the visible pixels, which can be biased by up to ~4 px (about 0.3 bar or 0.09 wt%). Rows flagged in notes have confidence 2.
- Open markers are digitized as the centroid of their white interior. Where the interior shows only as a 1-3 px slit in the stacks, the row is flagged in notes with confidence 2.
- Tool components rejected as not being markers:
  - border lines: M-C-800 closed run at 472.0 px; M-C-APS-4-800 closed run at 243.1, 421.0 and 534.0 px; M-C-KOH-4-800 closed run at 230.5 and 233.0 px (edge of the solid stack);
  - a strong red row at x 525-532 px, y 481 px, which is the top border of the open marker at ~24.6 bar and not a hidden closed marker;
  - white gaps 1-2 px wide between neighbouring markers (blue at 299, 308.5, 328, 336, 347, 357, 377, 387, 397, 435 px and three 6x2 gaps in the closed staircase; red at 312, 325, 339, 352.5, 366.6, 379.3, 456.7, 493.5 px);
  - label letter holes ("M-C-KOH-4-800", "M-C-4-800", "M-C-4-700", "M-C-800" and "(a)/(b)" in Fig. S2).
- The M-C-4-800 adsorption markers were separated with windows on the top edge of each closed marker (33 windows), because neighbouring closed markers touch. Four M-C-KOH-4-800 closed markers between 4.4 and 6.5 bar (Z0, Z, Z3, Z4) were also windowed, because the global run merged them.

## Values seen but not extracted

- Table 5, main p.9 [p.38]: comparison values from other papers, not measurements in this paper. AA-O 4.5 (20 bar), AC-0 4.3 (20 bar), PPY2 Activated 3.3 (20 bar), ACC 3.1 (72 bar), UCs-90-2 3.65 (20 bar), SCEMC700 4.43 (20 bar), FLG-800 2.0 (60 bar), CT 1.4 (19 bar), Norit R0.8 2.9 (20 bar) and 0.15 at 298 K (20 bar). The MOFs (not carbon sorbents): MOF-5 4.4 and 0.10, MIL-53 3.1 and 0.15, MIL-101 4.5 and 0.15 wt%. The M-C-KOH-4-800 entries (4.7 and 0.23 at 25 bar) duplicate Table 4.
- SI Table S1, p.3: literature comparison values. AC-K5 7.1, PAF-1 6.5 (porous aromatic framework, not a carbon sorbent), CN4800 5.4, ZTC-5 6.2, CA-4700 7 wt%, all at 77 K and 20 bar. The M-C-KOH-4-800 entries duplicate Table 4.
- Text p.8 [p.37]: human hair 2.03 wt% [55], viscose rayon 1.68 wt% [72], and AX-21_33 "less than 0.2 wt%" at 20 bar [82]. These are values from other papers.
- Text p.7 [p.36]: M-C-800 "less than 0.1 wt% at the same pressure (25 bar)" at 298 K. This is the same measurement as the Table 4 value 0.08, so it gets no separate row and is noted on that row.
- Text p.7 [p.36]: "higher ... by 30% for the uptake at 77 K and by 140% for the uptake at 298 K" are relative differences, not uptake values. The Chahine-rule estimate of 575 m2/g is not an uptake.
- Fig. 8, main p.8 [p.37]: excess uptake against BET area. It is not an isotherm and shows no values beyond Table 4 and Table 2.
- Text p.7 and SI Fig. S2(b): N2 uptake of 14 cm3/g on M-C-800. N2, not H2.
- Fig. 6 and SI Fig. S1: N2 isotherms and PSDs used as characterization. The Fig. 6b and S1 legends print "M-C-7-800", apparently meaning M-C-4-800.
- Figs. 9-11, Tables 6-8, SI Tables S2-S4 and Figs. S4-S7: CO2, CH4 and N2 uptake and selectivities. Not H2.
- M-C-400: characterization only, so no row. Table 1 EDS (at%): C 77.19, O 20.08, S 0.02, K 1.72, Mg 0.08, Ca 0.91, Cl 0. Raman ID/IG 0.58. The N2 surface area is "below the detection limit".
- Characterization with no schema field: Raman ID/IG (M-C-800 0.76, M-C-4-800 0.81, M-C-KOH-4-800 0.84); XRD peaks at ~23 and 43 degrees 2-theta (no d-spacing printed); carbon yield 30 wt% of the peels; carbon yields of three synthesis replicates within 2%.
