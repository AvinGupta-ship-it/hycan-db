# HYC-0138 extraction log (agent A)

## Extracted from
- Table 3 (p.77): H2 capacity at 1.1 atm for FCNFs-I (1.4), -II (3.8), -III (1.8), -IV (1.0 wt%); each merged with the last plotted point of its Fig. 12 panel (printed pressure 1.1 atm = 1.1146 bar is within 2% of the plotted 1.116-1.119 atm); 4 rows, `table_direct`.
- Text, sec. 3.4 (p.76): UFCNFs "about 1.4 wt%" at "relative low pressures"; pressure only in words, so pressure_unstated = true, approximate; 1 row, `text_direct`, no isotherm_id (paper does not tie it to a point).
- Fig. 11 (p.76), UFCNFs, H2 at 76 K: 9 markers digitized (`digitizations/fig11_UFCNFs.json`).
- Fig. 12a (FCNFs-I): 10 markers digitized plus the last marker merged into the Table 3 row (`fig12a_FCNFs-I.json`, 11 markers counted, all separate except the origin marker).
- Fig. 12b, 12c, 12d (FCNFs-II, -III, -IV): 8 markers each digitized plus the last marker merged into the Table 3 row.
- Table 1 (p.73): S_BET, V_P(NLDFT), V_Mi, V_iw(NLDFT), D_P(NLDFT) for all five samples, carried on every row. Table 3 repeats S_BET for the FCNFs (same values) and gives [-COOH] (XPS), carried in functional_groups.
- Experimental sec. 2.2.3 and 2.2.5: degassing, H2 purity, instrument, 76 K.

## Values seen, not extracted
- Text p.77 ordering "~3.8 > ~1.8 > ~1.4 > ~1.0 wt%" at 1.1 atm: same values as Table 3, same measurement, not repeated.
- Abstract "above 200%" and the statement of hydrogen uptake "1 atm" limit (850 mmHg): comparisons or limits, not uptake values.
- N2 isotherms (Figs. 4, 5) and N2 adsorbed volumes: not H2.
- Fractal dimensions, capacitance C (Table 3), Table 2, FTIR, TEM: no uptake.
- No H2 value is printed in a table for UFCNFs; only Fig. 11 and the text.

## Figure problems
- Unseparable markers: at low pressure the markers of Figs. 11, 12b, 12c, 12d overlap into one continuous band. The tool's blob groups were rejected (size) and recorded in each archive as "too large": Fig. 11 blob at pixel (709.8, 1413.2), 367 px (about 7 or more markers, x up to roughly 0.05 atm); Fig. 12b (700.8, 485.1), 278 px; Fig. 12c (216.7, 941.0), 215 px; Fig. 12d (701.3, 943.0), 193 px. Tolerances 5, 15, 25 and 40 did not separate them. These low-pressure points are not extracted and `isotherm_point_count` is empty for I1, I3, I4, I5 because the markers cannot be counted.
- Fig. 12a: the first marker sits at the origin (p = 0) and is half hidden by the plot frame (26 px; tool value 0.0 atm, 0.0298 wt%). Not written as a row: pressure 0 fails the schema's pressure range check (validator error "Pressure out of range"). It is counted in isotherm_point_count = 11.
- Fig. 12b: the legend marker (865, 412), 31 px, was excluded with `--marker-min-px 40`; recorded as "too small" in the archive.
- Axis calibration: ticks located from pixel columns/rows; two ticks per axis plus a verified third tick (x at 0.5 atm, y at 2.0 wt%), residuals 0.0-0.33%. Fig. 12d x-origin taken as 699.7 px (tick groups 699.5 +/- 0.5, neighbours spaced 35.3 px).
- `digitize_figure.py check` against the printed Table 3 value at 1.1 atm: UFCNFs (1.4 at 1.0 atm) pass 1.15%, FCNFs-II pass 1.81%, FCNFs-IV pass 1.39%. FCNFs-I FAIL at 5% (digitized 1.4712 vs printed 1.4, 5.09%) and FCNFs-III FAIL at 5% (1.9053 vs 1.8, 5.85%). The tool discarded those two archives; I re-extracted them unchanged (axis calibration is verified by the third ticks, so the difference is between the paper's printed values and its plotted points, not a calibration error) and their status is `unchecked`. For those two the Table 3 row carries the printed value (1.4, 1.8) and the note gives the digitized value of the same marker (1.48029, 1.92705). The other rows of those two series are digitized values.

## Coding decisions
- measurement_method `unknown`, uptake_type `unspecified`, basis_inferred `unknown`: the paper names Micromeritics ASAP 2020 but never states the method, basis (excess/absolute) or a free-volume calibration or buoyancy correction.
- wt% convention not stated; unknown / none. No paired units.
- 76 K stated as a number; within 76.0-79.0 K so treated as the 77 K class; temperature_inferred false.
- Degassing duration: two stages (300 min in preparation port, then 21 h in analysis port, both at 573 K); 21 h stored.
- average_pore_diameter left empty: Table 1 gives several NLDFT modes per sample (recorded in notes). V_iw has no field (notes).
- material_class `carbon_nanofiber` (authors' name; SBA-15 hard-templated), synthesis_method `template_synthesis`; HNO3 treatment in activation_method text (functionalization, not activation).
- BET range and consistency criteria not stated. area_same_sample `yes` (same labelled materials, N2 and H2 on the FCNFs/UFCNFs).
- Text sec. 3.3.1 says areas decreased "from 775 to 476 m2/g" and micropore volume "about 95"; Table 1 gives 810 to 451 m2/g; the Table 1 value is used and the inconsistency is in notes.
- Corresponding author J.M. Domínguez (asterisk); first affiliation Instituto Mexicano del Petróleo.
