# HYC-0091 extraction log (agent B)

Paper: Attia et al. 2020, Chem. Eng. J. 379, 122367. Input: page images main-01..11, si1-01..13 (no text layer).
Rows written: 260 (5 samples; 77 K isotherms I1, I3, I5, I7, I9; 298 K isotherms I2, I4, I6, I8, I10; one single text value).

## Sources extracted from

- Table 4 (main-08.png): H2 capacities at 77 K ("Excess H2 uptake (wt%)") and 298 K at 20 bar for CC-PNP, P-CC-PNP, C30-, C60-, C85-CC-PNP. 10 rows (table_direct), each merged with the highest-pressure closed square of its Fig. 7 isotherm (see "Table 4 / figure merge").
- Section 3.4 text (main-06.png, main-07.png): 1.42, 2.42, 3.6, 4 wt% at 77 K and 0.173 wt% at 298 K are the Table 4 values (same rows, cited in source_location). "C60-CC-PNP ... 1 bar and 77 K ... 2.4 wt%" is its own row (text_direct, no isotherm_id).
- Abstract (main-01.png): "4.0 and 0.173 wt% at 77 K and 298 K at 20 bar" = Table 4 C60 (77 K) and C30 (298 K); same rows.
- Table 5 (main-08.png) "C60-CC-PNP 4.0 (20 bar), This study" and Table S1 (si1-04.png) "C60-CC-PNP 4 (excess)" = Table 4 C60 77 K value; same row.
- Fig. 7a (main-08.png), 77 K, closed squares = adsorption, open squares = desorption (caption): digitized (details below).
- Fig. 7b (main-08.png), 298 K: only the highest-pressure point of each isotherm digitized (merged into the Table 4 298 K rows); for each series the point nearest 20 bar was also digitized, only to document the alternative merge in notes.
- Section 2.5 (main-03.png): Setaram PCTPro-E&E Sieverts apparatus with micro-doser; ~100 mg sample; degassed 12 h at 200 °C under vacuum; 0-20 bar; 77 K and 298 K; H2 99.999%; sample cell ~0.7 mL. No free-volume calibration, no repeated H2 isotherms or error bars.
- Section 2.3 (main-03.png): synthesis and activation conditions of all samples.
- Section 2.4 (main-03.png) and Table 2 (main-07.png): N2 BET areas (77 K), Vtot (Table 2 footnote: DFT; Section 2.4: Gurvich rule at P/P0 = 0.99; conflict recorded in notes), Vmicro (DR), Vmeso, QSDFT pore sizes. No BET P/P0 range or consistency criteria stated. N2 degassing for BET: 4-6 x 10^-6 kPa at 200 °C (not the H2 degassing; not stored as degas_end_pressure_pa).
- Table 1 (main-06.png): EDS composition (at.%) for all five samples: N stored as dopant at.% (method EDS = other), O/Cl/Zn in notes; residual Zn (CC-PNP 0.78, P-CC-PNP 0.23 at.%) as residual_metal_element without wt%.
- Section 3.3 text (main-06.png): BET/SPV values repeat Table 2.

## Values seen but not extracted

- Section 3.4 (main-07.png): "the H2 uptake at 298 K for all samples was still less than 0.2 wt% (Fig. 7b)": a bound stated across all five samples that restates the Table 4 / Fig. 7b values; not a row (statement over several samples).
- Section 3.4 (main-07.png): literature values ACC10 (2 wt%), WKL20 (1.65 wt%), ACC15 (2.3 wt%) [20], ACC (1.68 wt%) [21] at 77 K and 1 bar: other papers' materials.
- Table 5 (main-08.png), other papers: AAC (cloth) 3.1 (72 bar) [21]; PPY2 Activated 3.3 (20 bar) [47]; UCs-90-2 3.65 (20 bar) [48]; FLG-800 2.0 (60 bar) [49]; CT 1.4 (19 bar) [50]; Norit R0.8 2.9 (20 bar) [46]; SNU-4 3.7 (50 bar) [51] (MOF); ZIF-8 3.01 (55 bar) [52] (MOF); COF-8 3.5 (35 bar) [53] (COF): literature values, not measured here.
- Table S1 (si1-04.png): CA-4700 7, CN4800 5.4, AC-K5 7.1 wt% at 77 K, 20 bar (refs 1-3): literature values.
- Table 3 (main-07.png): VRC 1205 m2/g / 0.47 cm3/g [21], Lyocell, Nomex, Acrylic textile fibers, ACC20, ACC-5092-15: literature cloths, no H2 data here; C60-CC-PNP row repeats Table 2.
- Section 3.4 (main-06/07.png): Chahine-rule estimate "(500 m2 g-1, ~1 wt%), the accessible surface area of CC-PNP was estimated as 710 m2 g-1": computed from the H2 uptake, not a measured area; not stored.
- Fig. 8 (main-08.png): excess H2 uptake (77 K) vs BET SSA for P-, C30-, C60-, C85-CC-PNP: not an isotherm; values equal Table 4.
- Fig. 7b (main-08.png): all points other than the highest-pressure point of each 298 K isotherm (protocol). No open (desorption) symbols are visible in Fig. 7b although the caption mentions them.
- CO2 and CH4 data (Fig. 9, 10, 11; Tables 6, 7, S2, S4, S5, S6; Figs. S4-S10; IAST selectivities): not H2.
- Fig. 5 / Fig. 6 (main-06/07.png): N2 isotherms and PSDs (characterization, summarized in Table 2).
- Fig. 2, 3 (main-04.png), Fig. 4 (main-05.png), Figs. S1-S3: XRD (002)/(100) at ~22° and 43° (no d-spacing printed), Raman ID/IG (CC-PNP 0.75, C30 0.72, C60 0.77, C85 0.85), SEM, PNP particle size ~170 nm, photos: characterization with no schema field.
- VRC (viscose rayon cloth precursor) and VRC-PNP: no H2 uptake and no characterization values in this paper; no rows.

## Figure digitization

- Axes calibrated on the lowest and highest labelled ticks, tick centres found from intensity profiles of pixel rows/columns, checked on a middle tick.
  Fig. 7a: x 0 bar = 198.27 px, 30 bar = 594.04 px, check 15 bar at 396.76 px (0.31%); y 0 wt% = 408.04 px, 4 wt% = 158.32 px, check 2 wt% at 283.4 px (0.18%).
  Fig. 7b: x 0 bar = 698.6 px, 30 bar = 1094.38 px, check 15 bar at 897.59 px; y 0 = 406.26 px, 0.20 wt% = 126.4 px, check 0.10 at 266.49 px.
- Series colours: C60 #00ff00, C30 #ff0000, C85 #0000ff, P-CC-PNP #7f00ff, CC-PNP #ff00ff. ROI excludes the in-plot series labels.
- Fig. 7a closed squares (adsorption): one run per series (fig7a_<label>_adsorption.json), --mode markers, tolerance 60 (raised from 40, which lost one partly hidden square in four series), 3-px opening. Detections used: CC-PNP 26, P-CC-PNP 31, C30-CC-PNP 16, C60-CC-PNP 31, C85-CC-PNP 30. Rejected: C85 archive point index 3 at pixel (211, 299), a crossing of overlapping open-square outlines, not a marker. Squares with fewer than 25 matched pixels are partly hidden; their value is the centroid of the visible part (noted per row, confidence 2).
- Fig. 7a open squares (desorption) are white-filled and drawn over the closed squares; in a full-plot run each merges with its neighbours. Each fully visible open square was therefore digitized in its own run with --roi set to that square's box (fig7a_<label>_desorption_NN.json; tolerance 170 green, 200 red/blue/purple, 190 magenta; --open-px 1). Every run returned one marker centred within 1 px of the box centre. Used: CC-PNP 24, P-CC-PNP 25, C30-CC-PNP 18, C60-CC-PNP 28, C85-CC-PNP 25. This deviates from "one file per series": one archive per open square.
- P-CC-PNP origin square (archive point index 0): digitized -0.0074 wt% at 0.055 bar (0.46 px below zero); stored as 0 (schema rejects negative uptakes); noted in the row.
- Fig. 7b: one run per series (fig7b_<label>.json, tolerance 60). The highest-pressure squares of C85 and P-CC-PNP merge with their neighbours there and were isolated with --roi (fig7b_C85-CC-PNP_highest.json, fig7b_P-CC-PNP_highest.json). Nearest-to-20-bar squares isolated with --roi for CC-PNP, P-CC-PNP, C30, C85 (fig7b_<label>_near20.json); C60's is in the full-series archive.
- check (digitize_figure.py check, --at 20, Table 4 value, 5%) passed for all ten full-series archives.

### Markers seen but not separable (not extracted; counted in isotherm_point_count)

- C60-CC-PNP 77 K: 6 closed squares visible only as slivers: in the low-pressure stack at x 199-201 px, y about 309, 353, 385, 399 px (about 1.58, 0.88, 0.36, 0.15 wt% at 0.1-0.2 bar), and at about (210, 257) and (204, 290) px (about 2.4 and 1.9 wt%) under the open-square staircase; about 7 open squares in the overlapping staircase from (212, 254) to (202, 284) px (about 1.3 to 0.5 bar), each partly covered by the next.
- C30-CC-PNP 77 K: below about 7 bar the isotherm is hidden behind the C60 symbols; about 8 squares visible only as red slivers (left edge of the C60 staircase, x 205-221 px, y 241-284 px; stack at x 196-200 px, y 309-346 px; branch not identifiable) and about 9 open squares partly visible below-right of the C60 symbols (x 215-285 px, y 205-245 px, including (260,216), (269,212), (278,210) px). Closed squares under the open squares between 14.4 and 17.0 bar and between 18.5 and 20.4 bar are fully hidden and not counted.
- C85-CC-PNP 77 K: 2 partly hidden closed squares at about (201, 328) and (197, 390) px (about 1.3 and 0.3 wt%, below 0.3 bar); about 8 open squares in the overlapping staircase from (223, 274) to (203, 308) px (about 2.1 to 0.4 bar).
- P-CC-PNP 77 K: about 5 open squares in the overlapping staircase from (221, 297) to (203, 320) px (about 1.9 to 0.6 bar).
- CC-PNP 77 K: about 4 open squares overlapping at x 203-214 px, y 333-341 px (about 0.4-1.3 bar) and one partly covered at about (458, 320) px (about 19.5 bar).
- isotherm_point_count (77 K): I1 55, I3 61, I5 51, I7 72, I9 65 = extracted points + markers listed above. Approximate lower bounds: fully hidden markers cannot be counted.
- isotherm_point_count (298 K, Fig. 7b, closed squares counted including partly visible ones): I2 29, I4 30, I6 26, I8 27, I10 28. Approximate lower bounds (low-pressure squares hidden under other series).

## Table 4 / figure merge

The paper says Fig. 7 presents the isotherms "at 77 K and 298 K and 20 bar (Table 4)" and that the isotherms were measured over 0-20 bar, so each Table 4 value was merged with the highest-pressure adsorption square of its isotherm (digitized 20.1-20.8 bar; printed pressure 20 bar stored). The protocol tie-break "closest in pressure" would instead pick the preceding square for C60 and C85 at 77 K and for all five series at 298 K; those points are given in the rows' notes. At 298 K the printed values agree better with the highest-pressure squares (e.g. P-CC-PNP: printed 0.073; highest 0.0733 at 20.36 bar; preceding 0.0780 at 19.97 bar).

## Coding notes

- Basis: the paper calls the 77 K and 298 K uptakes "excess" but never defines it: basis_stated false, basis_inferred excess, uptake_type excess. wt% convention unknown (no paired units).
- material_class doped_carbon for all samples (N built in from polypyrrole, 7.85-12.93 at.% by EDS); synthesis_method carbonization (carbonized viscose rayon cloth/PNP made by the authors; the cloth precursor is commercial but unnamed).
- pore_volume_method DR (micropore volume; Vtot method conflicting between Table 2 footnote and Section 2.4); average_pore_diameter_nm = first QSDFT PSD peak listed in Table 2 (full list in notes).
- measuring_lab_id: corresponding author H. Oh, affiliation a (Gyeongnam National University of Science and Technology (GNTECH)).
- Confidence: table values 5; text value 4; clean digitized markers 3; partly hidden closed squares 2.
