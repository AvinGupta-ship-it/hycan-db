# HYC-0083 extraction log (extractor B)

Yang, Xia & Mokaya, J. Am. Chem. Soc. 2007, 129, 1673-1679 (10.1021/ja067149g). Source: page images only (main-1..7, si1-1..8). 433 rows in `rows.csv`; 49 archives in `digitizations/`.

## Sources extracted (one line each)

- Table 1 (main p.4 / p.1676): H2 uptake at -196 C and 20 bar for CA800 3.9, CA850 6.0, CB850 5.5, CB850h 6.9 wt%. Each merged with the 20-bar point of the matching Fig. 4 isotherm: table_direct rows, digitized point given in `notes`. Also the Langmuir maxima 4.67, 6.35, 6.46, 8.33 wt% (footnote d) and the textural data that every row of the sample carries.
- Section 2 text (main p.2): synthesis, BET method and range (P/Po 0.02-0.25), total pore volume at P/Po ca. 0.99, gravimetric IGA-003 (Hiden) and volumetric ASAP 2020 methods, degassing (10^-10 bar, 200 C, overnight; ASAP: 200 C, overnight), H2 purity 99.9999%.
- Section 3.2 text (main p.4-5): buoyancy-correction description (carbon density 1.5 g/cm3 from He at 323 K; adsorbed-H2 density 0.04 g/cm3); text value CA850 2.3 wt% at 1 bar (gravimetric), merged with the 1.0-bar point of I5; text value CA850 2.6 wt% at 1 bar (volumetric; also in the abstract and Conclusions), recorded on I6; G212 2.0 wt% at 1 bar and 3.96 wt% at 20 bar (the 20-bar value merged with the plotted point); Zhao et al. G212 2.15 wt% at 1 bar, recorded as sample S6 with `previously reported` in notes.
- Abstract and Conclusions: 6.9 wt%, 8.33 wt% and 2.6 wt% repeat Table 1 and the text, so they get no extra rows and are named in `source_location`.
- Fig. 4 (main p.5): isotherms a CA800 (I1), b CB850 (I7), c CA850 (I3) and d CB850h (I9) at -196 C, 0-20 bar, both branches. Digitized.
- Supporting Fig. 3S (SI p.S4): the same four isotherms without the buoyancy correction for adsorbed H2: a (I2), c (I4), b (I8), d (I10). Digitized.
- Fig. 5A (main p.6): curve b, the CA850 volumetric isotherm (I6), digitized. Curve a was digitized only for comparison (see Replots).
- Fig. 5B (main p.6): the H2 curve, the CA850 gravimetric isotherm at 0-2 bar (I5). Digitized.
- Supporting Fig. 5S (SI p.S6): curve b, G212 in red (I13). Digitized.
- Supporting Fig. 7S (SI p.S8): CB850h at -196 C (I11), every resolvable point. At -186 C (I12, 87.15 K), only the highest-pressure point.
- Supporting Fig. 4S (SI p.S5): Langmuir plots. Cited for the Table 1 maxima; not digitized because it is not an isotherm.

## Values seen but not extracted

- ZTA 527 (486) m2/g, 0.28 (0.23) cm3/g and ZTB 342 (301) m2/g, 0.23 (0.14) cm3/g (Table 1); zeolite beta N2 isotherm (Fig. 2A): zeolite templates, not carbon sorbents, with no H2 uptake.
- MOF-505: 2.6 wt% at 1 bar and 4.1 wt% at 20 bar (ref. 14l), and 2.47 wt% at 1 bar (Yaghi and co-workers, ref. 14c), main p.5. Not a carbon sorbent.
- "maximum capacity of 4.5 wt % at 70 bar" (Hirscher and Panella, ref. 6a): a summary over "a wide range of high surface area carbon nanostructures" from another paper. No identifiable sample, and no temperature stated.
- "uptake of up to 4.5 wt % at 20 bar for zeolite-templated carbons with low levels of zeolite-type structural ordering" (ref. 9): the best value over a set of samples from the authors' earlier paper. No identifiable sample, and no temperature stated.
- "The uptake capacity at 20 bar varies between 4 and 7 wt %" (main p.5): a range across samples that rounds the Table 1 values.
- "(In the absence of buoyancy correction, the uptake at 20 bar is between 3.3 and 6 wt %.)" (main p.5): a range across samples with no sample named. It matches the Fig. 3S endpoints of curve a (3.30) and curve d (5.84), which are extracted as digitized rows.
- Supporting Fig. 4S annotations: "3.90% (20 bar)" CA800, "6.01% (20 bar)" CA850, "5.48% (20 bar)" CB850, "6.92% (20 bar)" CB850h and "3.96% (20 bar)" G212 are more precise prints of the Table 1 and text values. The W0 values 4.67, 6.35, 6.46 and 8.33% equal Table 1. **G212 Langmuir W0 = 1/a = 4.50%** appears only in this figure, which is not an isotherm, so it is not extracted. The fit statistics (R, R2) and the P/W points are not uptakes.
- Fig. 5B D2 isotherm (CA850, D2 uptake in wt%): deuterium, not H2. "expected ratio of wt % uptake is 2:1 (D2:H2)".
- Supporting Fig. 6S and text: molar nD2/nH2 ratio 1.08-1.16 (CA850, 0.1-2 bar), and 1.06-1.10 for other carbons (ref. 17). Ratios, not uptakes.
- Fig. 6 and text: isosteric heat for CB850h, from 8.2 to 4 kJ/mol over 0-5.3 wt%. Not an uptake. Fig. 6 is not an isotherm.
- Supporting Figs. 1S and 2S, Figs. 1 and 3 (XRD, SEM, TEM) and Fig. 2 (N2 isotherms, HK pore-size distribution): characterization only. The "ca. 0.6 nm" PSD maximum is recorded on CA850, CB850 and CB850h.
- Kinetic statement "rapid (2.5-3 min) achievement of equilibrium": not an uptake.

## Replots (digitized once)

- Supporting Fig. 5S black curves a CA800, c CB850, d CA850 and e CB850h replot the Fig. 4 isotherms with the same corrections (caption: 1.5 g/cm3, 0.04 g/cm3). A check digitization of curve e at 8-20 bar matches Fig. 4 curve d within 0.02 wt% (0.044 at 8 bar), and the 20-bar markers of curves c and d match Fig. 4 b and c. The check is in the work directory (`work/verify5S/fig5S_e_hiP_check.json`). No rows were made from these curves.
- Fig. 5A curve a (CA850, gravimetric) plots the same data as the Fig. 5B H2 curve: eight resolved markers agree within 0.01 wt%. The archives are `fig5A_a_seg1-4.json`; rows come from Fig. 5B (I5), which covers 0-2 bar. `fig5A_a_seg4.json` gives the digitized 1-bar point that `notes` cites for the merged text value 2.3 wt%.

## Coding decisions

- **Branches.** In the page images, the symbol key in the Supporting Fig. 7S caption is blank ("adsorption ( ) and desorption ( )"), and no other caption gives one. Up-triangles are coded as adsorption and down-triangles as desorption. Two reasons: this is the usual key, and in Fig. 5A curve b the down-triangle line lies above the up-triangle line, the normal hysteresis order. In the 20-bar runs, up-triangles fall at whole-bar pressures (3-19 bar) and down-triangles at half-bar pressures (2.5-18.5 bar). Shapes were checked at 2.5-6 bar in Fig. 3S. Fig. 4 is too low in resolution to show marker shape, so its branches follow the same pressure grid, since the paper says Fig. 3S shows the same runs.
- **Stars.** A six-pointed star is an up-triangle and a down-triangle drawn at the same point. Each star gives one adsorption row and one desorption row with the same digitized centre. The 20-bar star of each 20-bar run is the turning point.
- **Isotherm ids.** Fig. 3S curves (I2, I4, I8, I10) get their own ids. They are the same runs as Fig. 4 reduced without the adsorbed-H2 buoyancy correction, so they are not replicates. Sharing an id would mix two reductions in one isotherm.
- **I5 and I3.** I5 (Fig. 5B) is probably the low-pressure part of the I3 run: its marker pattern matches, it has no down-triangle at 1.8 or 2.0 bar, and its 1.5-bar value is 2.625 against 2.623 in Fig. 4. The paper does not say so, and each plotted curve is one run, so I5 stays separate.
- **I11.** Fig. 7S at -196 C ends near 6.6 wt% at 20 bar, against 6.9 wt% in Fig. 4 d and 5.84 in Fig. 3S d, and its pressure grid is denser. It is coded as a separate run, which makes `replicates_reported` true for CB850h.
- **replicates_reported.** True for CA850, which has gravimetric and volumetric isotherms (Fig. 5A). False for CA800, CB850 and G212.
- **Basis.** The paper never names the basis. `basis_inferred` = excess by the rule for gravimetric data with a stated buoyancy correction, and excess (volumetric default) for the ASAP 2020 isotherm. The Fig. 4, 5B and 5S values also include a buoyancy correction for the adsorbed H2 volume (density 0.04 g/cm3). That correction moves them toward an absolute-type amount; this is flagged in `notes` for reconciliation.
- **Langmuir maxima.** The Table 1 maxima (4.67, 6.35, 6.46, 8.33) are fitted Langmuir W0 values: `value_kind` fitted_extrapolated, `pressure_bar` empty and `pressure_unstated` = true. The abstract's "estimated maximum of 8.33 wt % at -196 C and 20 bar" describes the fitted range, not a measurement pressure. These rows carry the Fig. 4 isotherm id, because the text says the Langmuir plots were applied to these isotherms and Fig. 4S annotates each fit with that isotherm's 20-bar value.
- **G212 textural data.** The surface area (1405 m2/g) and pore volume (0.7 cm3/g) are printed in parentheses with no method and no statement of who measured them. Coded: method unspecified, probe gas unspecified, `area_same_sample` unclear. The G212 carbon density of 1.8 g/cm3 is cited from Zhao et al.
- **Zhao et al. G212 (S6).** The 2.15 wt% at 1 bar is a value published before by another group, so it is extracted with `previously reported` in notes. It is a separate sample from the authors' G212. Its temperature is not printed, so `temperature_unstated` = true. Its method and laboratory institution are not given.
- **Unmatched text values.** The CA850 volumetric 2.6 wt% at 1 bar and the G212 2.0 wt% at 1 bar correspond to plotted points I could not resolve: an overlapping marker pair at 1.014 bar in Fig. 5A b, and the low-pressure cluster in Fig. 5S. Those text rows carry no digitized value.
- **Text 2.3 vs plot.** The CA850 text value 2.3 wt% at 1 bar is 4-5% above the plotted 1-bar point: 2.191 wt% in Fig. 5B and 2.197 wt% in Fig. 5A.
- **CB850h heat treatment.** The temperature of the 3 h N2 heat treatment is not printed; it is described in words only.

## Digitization

All values come from `scripts/digitize_figure.py extract --mode markers` run on the unmodified page images. Each archive's calibration was checked on a third tick and passed (relative error <= 0.3%).

Same-colour curves cross or come close in each figure. Each curve was therefore split into ROI rectangles on the page image, and each rectangle holds only that curve's markers. I planned the rectangles with an exact re-implementation of the tool's isolation step (Euclidean colour distance, ROI clip, 3x3 opening, 8-connected components of 6-2000 px). Every tool output was checked to equal the planned marker set. This gives one archive per segment, named `<fig>_<curve>[_segN].json`.

Accepted markers are separate components of single-marker or star size that do not touch a marker of another colour drawn over them; in Fig. 3S and 5S, red is drawn over blue and black. Merged blobs, partly hidden markers, markers cut by the axis line and clusters were not extracted.

The tool's stated-value `check` passed for `fig5S_b_G212.json` (3.96 at 20 bar, +0.08%) and `fig5A_a_seg4.json` (2.3 at 1 bar, -4.5%). It could not be run elsewhere: the 20-bar marker centres digitize at 19.95-19.97 bar, just below the stated 20 bar, and no other stated values fall inside an archive's range.

| Figure (page image) | Calibration ticks: x low/high (verify), y low/high (verify), px | Colour, tolerance |
|---|---|---|
| Fig. 4 (main-5) | 0 @185.7, 20 @568.63 (10 @377.12); 0 @671.3, 7 @410.57 (4 @522.38). The 0 ticks coincide with the frame lines. | #3248a4 and #ed1c24, 90 |
| Supp. Fig. 3S (si1-4) | 0 @307, 20 @1002 (10 @655); 0 @652, 6 @202 (3 @427) | #0000ff and #ff0000, 60 |
| Fig. 5A (main-6) | 0.2 @355.23, 1.2 @623.5 (0.6 @462.75); 0 @340.0, 3.0 @105.39 (1.5 @222.53). The 0.0 x tick is hidden under the origin marker, so the lowest clean tick (0.2) was used. | #000000, 100 |
| Fig. 5B (main-6) | 0 @699.46, 2.0 @1024.78 (1.0 @862.18); 0 @343.0, 7 @107.48 (3 @242.0) | #000000, 180 |
| Supp. Fig. 5S (si1-6) | 0 @331, 20 @1023 (10 @677); 0 @838, 7 @365 (3.5 @602) | #ff0000, 60 |
| Supp. Fig. 7S (si1-8) | 0 @365, 20 @945 (10 @655); 0 @1186.5, 7 @779.5 (3 @1012) | #000000, 100 |

**Marker counts.** In the table below, "counted" is the `isotherm_point_count`. Low-pressure clusters cannot be counted marker by marker, so their counts are estimates, as explained after the table.

| Isotherm | Counted (both branches) | Extracted markers | Not separated (logged) |
|---|---|---|---|
| I1 Fig. 4 a CA800 | 60 | 38 | 22: cluster 0-1.3 bar (blob at 0.68 bar), partial markers at 0.12 and 0.23 bar, merged 1.8+2.0 bar pair, 1.2 bar marker inside the cluster edge |
| I3 Fig. 4 c CA850 | 60 | 36 | 24: all markers below 2.4 bar hidden under or touching red curves (1.2 up-triangle, 1.5 star, merged 1.8+2.0 pair, low-pressure cluster) |
| I7 Fig. 4 b CB850 | 60 | 36 | 24: red cluster 0-1.5 bar shared with d (blob n=428), 1.47 bar star touching blue, merged 1.8+2.0 pair |
| I9 Fig. 4 d CB850h | 60 | 39 | 21: red cluster shared with b, 1.2 bar up-triangle and 1.79 bar marker touching other markers |
| I2 Fig. 3S a CA800 | 60 | 41 | 19: origin markers split by the axis line, blobs at 0.10 and 0.53 bar (clusters), partial at 0.22 bar, merged 1.8+2.0 pair |
| I4 Fig. 3S c CA850 | 60 | 36 | 24: markers below 2.4 bar under the red curves (1.19 up-triangle and 1.49 star touching red, merged 1.8+2.0 pair, cluster) |
| I8 Fig. 3S b CB850 | 60 | 38 | 22: red clusters at 0.08, 0.21 and 0.68 bar shared with d, merged 1.8+2.0 pair |
| I10 Fig. 3S d CB850h | 60 | 41 | 19: red clusters shared with b below 1.1 bar |
| I5 Fig. 5B H2 CA850 | 24 | 23 | 1: origin marker cut by the axis line |
| I6 Fig. 5A b CA850 volumetric | 36 (approx.) | 10 | ~26: nine overlapping up/down pairs (0.27, 0.33, 0.39, 0.64, 0.76, 0.80, 1.01, 1.07, 1.14 bar), the down-triangle end point at 0.002 bar touching the cluster, about 7 markers in the 0-0.2 bar cluster |
| I13 Supp. Fig. 5S b G212 | 65 (approx.) | 42 | ~23: cluster below 1.3 bar (blobs n=103 and 714) |
| I11 Supp. Fig. 7S -196 C | 90 (approx.) | 45 | ~45: cluster below 2.2 bar (n=925), partial marker at 2.21 bar, nine down/up pairs at 2.5, 2.9, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5 and 9.5 bar |
| I12 Supp. Fig. 7S -186 C | 88 (approx.) | 1 (highest pressure, as required) | n/a |

The count of 60 for each 20-bar run has two parts:
- 36 markers counted at 2.5-20 bar: 17 down-triangles, 17 up-triangles and the 20-bar star.
- 24 markers in 0-2 bar, taken from the resolved view of the CA850 run in Fig. 5B: the origin up-triangle, a down-triangle at 0.004 bar, stars at 0.1-0.6, 0.8, 1.0 and 1.5 bar, a down-triangle at 0.7 bar, and up-triangles at 1.2, 1.8 and 2.0 bar. The markers resolved at 1.0-2.0 bar in Fig. 3S and Fig. 4 for each sample match this pattern.

The counts for I6, I11, I12 and I13 are area-based estimates for the clustered regions.

The digitization uncertainty for each point is left to the reconciler, per the instruction.
