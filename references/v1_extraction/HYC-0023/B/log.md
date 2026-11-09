# HYC-0023 extraction log (agent B, 2026-11-09)

167 rows written; 27 samples (S1-S27); 19 isotherms (I1-I19). Page images only (main-1.png ... main-6.png); no supplementary file.

## Sources extracted

- Table 1 (p. 6315, main-2.png): 17 values, H2 uptake at 77 K, 60 bar, wt%, TiC-CDCs -> 17 table_direct rows (S1-S17). Six of them are merged with the high-pressure end of a Fig. 1 line (below).
- Table 2 (p. 6316, main-3.png): 6 values, 77 K, 60 bar, Mo2C- and SiC-CDCs -> 6 table_direct rows (S18-S23), no isotherm_id.
- Fig. 1 (p. 6316, main-3.png): 77 K isotherms, 7 lines drawn without markers (TiC-CDC 600 °C: unactivated and CO2-activated 2 h 875/900/930/950 °C, 6 h 875 °C, 8 h 875 °C). Digitized with `--mode curve` and read at 10 pressures each by linear interpolation; 64 figure_digitized rows (70 points minus 6 merged), value_kind fitted_interpolated, isotherm_point_count empty.
- Section 3 text (p. 6317, main-4.png, right column): "At room temperature, this CDC adsorbs less than 0.5 wt% at the maximum pressure" -> 1 text_direct row (S24, upper bound, temperature and pressure unstated).
- Fig. 5a-c (p. 6318, main-5.png): Sieverts excess isotherms of the NH3-annealed TiC-CDC (chlorinated at 800 °C) after outgassing at 200, 600 and 800 °C (S25, S26, S27). 77 K: every separable marker of both branches (73 rows: a 9 ads + 15 des, b 8 + 16, c 7 + 15). 87, 150 and 300 K: the highest-pressure marker of each isotherm only (9 rows).

## Fig. 1 digitization

- Calibration (page pixels): x 695 = 0 bar, 1110.5 = 60 bar, check tick 903 = 30 bar (predicted 30.036, 0.12%); y 1429 = 0 wt%, 1090.5 = 5 wt%, check tick 1225.5 = 3 wt% (predicted 3.006, 0.20%). Ticks located from pixel columns/rows below and left of the axis lines.
- The legend text (coloured and black) lies inside the plot, so the rectangle x 900-1015, y 1215-1405 was painted white in a copy of the page (work/main-3_fig1_legendmasked.png); no curve passes through it. ROI x 697-1115, y 1085-1427.
- Colours: red #ff0000, blue #0000ff, green #00ff00, magenta #ff00ff, cyan #00ffff, black #000000, all tolerance 60; dark red #781e1e tolerance 70 with ROI y >= 1172 (excludes anti-aliased pixels of the upper lines; two single contaminated bins remain at 6.5 and 6.9 bar, not adjacent to any interpolation pressure).
- Interpolation pressures k/10 x p_end (k = 1..10) for six lines. The green line (6 h at 875 °C) is hidden beneath the red and blue lines below 12.56 bar, so its visible lowest-pressure end is above 5% of p_end and it is read at p_start + k(p_end - p_start)/9. The blue line (8 h at 875 °C) is hidden under the red line at about 6.4-10.0 and 10.5-15 bar; its value at 11.78 bar is a linear interpolation across that gap.
- Line ends: 59.21 bar (red, magenta, dark red, black), 58.92 (blue), 59.06 (green), 57.18 (cyan). Each end within 2% of 60 bar is merged with the Table 1 value (table value, printed 60 bar, isotherm_id of the line, digitized end point in notes). The cyan line (2 hr at 900 °C) ends at 57.18 bar, outside 2% of 60 bar, so the Table 1 value for that sample is a separate row with no isotherm_id, and all 10 line points are kept.
- Digitized end value vs printed Table 1 value: 950 °C 2 h 4.609 vs 4.7; 8 h 875 °C 4.623 vs 4.62; 6 h 875 °C 4.557 vs 4.58; 930 °C 2 h 4.195 vs 4.5 (-6.8%); 875 °C 2 h 3.722 vs 3.7; unactivated 3.397 vs 3.1 (+9.6%); 900 °C 2 h 3.944 at 57.18 bar vs 3.9 at 60 bar. Recorded as printed.
- Curve-to-sample mapping: legend labels map to Table 1 "TiC, 600, CO2 act ..." rows by time and temperature; "unactivated" mapped to "TiC, 600, H2 ann" (Fig. 2 caption: "non-activated precursor (600 °C CDC)"; Section 2.1: CDC powders were H2-annealed before activation).

## Fig. 5 digitization

- Calibrations (page pixels): panel a x 238.5 = 0, 586.5 = 50 bar, check 378 = 20 (0.22%); y 1024 = 0, 727 = 6 wt%, check 875.5 = 3 (0.00%). Panel b x 687 = 0, 1035 = 50, check 826.5 = 20 (0.22%); y 1024 = 0, 727.5 = 6, check 875.5 = 3 (0.17%). Panel c x 238.5 = 0, 586.5 = 50, check 378 = 20 (0.22%); y 1404.5 = 0, 1108 = 6, check 1256.5 = 3 (0.17%).
- ROIs exclude the legend, the "Toutgas" annotation and the axis line: a x 242-600, y 805-1022; b x 691-1050, y 805-1022; c x 242-600, y 1180-1402.
- 77 K adsorption (filled black squares): `--mode markers --open-px 3 --marker-min-px 32` (a full square is ~64 px). Two touching end markers in panels a and c (about 44.4 and 45.7 bar) form one blob; they were split by painting one pixel column white (x = 552, a: y 846-858; c: y 1214-1226) in a copy of the page (work/main-5_fig5_ads_split.png).
- 77 K desorption (open black squares, drawn on top of the filled ones): the tool cannot isolate hollow markers whose outlines join the connecting lines, so a hole-interior image was made for each panel (work/holes5a.png, holes5b.png, holes5c.png; script work/holes.py): achromatic pixels darker than mean 200 inside the ROI, scipy binary_fill_holes, interior pixels painted black on white, same pixel grid as the page. Markers extracted from it with `--open-px 2 --marker-min-px 20` (a full interior is 36-49 px). In panel c the open square at ~38.0 bar has a 2-px gap in its bottom edge where an 87 K triangle overlaps it; pixels (502,1221) and (503,1221) were added to the outline before filling.
- Every extracted marker was checked on an enlarged overlay of the page (work/ov5a_f.png, ov5b_f.png, ov5c_f.png): one cross per separable marker, none on a non-marker. Markers with fewer pixels than a full marker are partly occluded; their rows have extraction_confidence 2 and a note.
- Markers counted on the plot vs extracted (77 K): all fully or mostly visible filled and open squares are extracted. Not separated, so not extracted:
  - a, adsorption: one filled square at ~17.4 bar visible only as a 12-px sliver under an open square; filled squares below ~9 bar visible only as slivers under the open squares or hidden beneath the 87 K and 33 K series (not countable).
  - a, desorption: fragments at ~2.9, 2.4, 2.1, 1.9 bar (4-14 px interiors) and further stacked outlines below ~1.9 bar, hidden beneath the 87 K triangles and 33 K circles near 0-2 wt% (not countable).
  - b, adsorption: filled squares below ~13.9 bar visible only as slivers or hidden (not countable).
  - b, desorption: fragments at ~2.5, 2.1, 1.9, 1.65, 1.15 bar and further hidden markers (not countable).
  - c, adsorption: partly visible filled squares at ~13.2 and ~9.6 bar (21 and 27 px after opening), one hidden under the open square at ~17.8 bar, and slivers or hidden markers at lower pressure (not countable).
  - c, desorption: fragments at ~1.15-2.8 bar (9 blobs of 4-14 px, more than one fragment per marker in places) and hidden markers below (not countable).
- Because the low-pressure markers of every Fig. 5 run overlap or are hidden, isotherm_point_count is left empty for all Fig. 5 isotherms (77, 87, 150, 300 K).
- 87, 150 and 300 K: highest-pressure filled marker of each run, isolated with an ROI starting at the column where it separates from the preceding marker (`--open-px 1`, tolerance 90; green #00ff00, magenta #ff00ff, blue #0000ff).
- The tool's `check` subcommand was not run: no printed value lies inside any digitized series' pressure range (Table 1 values are at 60 bar, beyond the Fig. 1 line ends; Fig. 5 has no printed values), so every archive has status "unchecked". digitization_uncertainty_wt_pct is left empty as instructed.

## Values seen but not extracted

- Tables 1 and 2, column "Hydrogen uptake per SSA [10^3 wt% g/m2]" (23 values): ratio of uptake to BET SSA computed by the authors, not a separate measurement; no schema field.
- Fig. 5a-c, 33 K isotherms (red circles, 3 runs, highest-pressure point near 3-4 bar, ~5.2-5.6 wt%): temperature 33 K is below the schema range of temperature_k (50-500 K; the validator reports "Temperature out of range"), so no row can hold them.
- Section 3 text: "At 30 K, TiC-CDC shows that the hydrogen uptake saturates around 5.5 wt% at pressures close to ambient": 30 K is below the schema temperature range (and the Fig. 5 legend gives 33 K); not extracted.
- Conclusions (p. 6319): "a gravimetric hydrogen-storage density of 4.7 wt% at elevated pressure obtained either with TiC chlorinated at 600 °C activated under CO2 or low temperature synthesized CDCs (400 or 500 °C) activated under KOH": a summary restating Table 1 (TiC, 600, CO2 act 950 °C, 2 h = 4.7 wt%); for the KOH-activated 400 and 500 °C CDCs Table 1 prints 4.5 wt%, not 4.7. Not a separate measurement; not extracted.
- Fig. 3a and 3b (p. 6317): excess capacity at 77 K, 60 bar vs BET SSA and vs total pore volume; not isotherms, not digitized. Its CDC series repeat Tables 1 and 2. Values the tables and text do not give: "Microporous AC" (4 points, magenta triangles; the commercial and experimental microporous activated carbons, incl. KOH-activated anthracite and phenolic-resin carbons of Section 2.1) and "AX21" (1 point, black pentagon), each with uptake and BET SSA / pore volume read only from the plot. Also the Chahine-rule line and the blue and red dashed bounding lines (not data).
- Fig. 4 (p. 6318): excess capacity per SSA vs average pore size for the Fig. 3 samples; not an isotherm and a derived ratio; includes the Microporous AC and AX21 points not given in tables or text. Not digitized.
- Fig. 2 (p. 6317): NLDFT pore size distributions of the unactivated, 8 hr at 875 °C and 2 hr at 950 °C TiC-CDCs; characterization only, no H2 value.
- Fig. 5d (p. 6318): isosteric heat Qst vs excess capacity for the three outgassing states; not an isotherm. Text values: Qst ~8.5 kJ/mol at low loading decreasing to ~5.5 kJ/mol; Qst "only slightly increases in the 1-2.5 wt% range" after annealing; not uptake values.
- Section 3 text: "the typical TiC-CDC has a higher heat of adsorption (above 8.5 kJ/mol) than AX-21 (6.5 kJ/mol) at low hydrogen loading, and just ~25% lower uptake at ~60% lower SSA": relative comparison, no uptake value. "isosteric heat of hydrogen in MOF-5 (~4.8 kJ/mol)": not a carbon sorbent, not uptake.
- Section 3 text: "The 950 °C 2 h sample has a very large SSA, >3000 m2/g compared to the 2700 m2/g of the 875 °C 8 h sample": characterization restating Table 1 (3038, 2643 m2/g) approximately.
- Section 3 text, PGAA of the NH3-annealed TiC-CDC: H below 0.09%, Cl below 0.04%, Ti 0.1% before and <0.015% after vacuum annealing: composition, recorded in notes of S24-S27 (residual_metal_element = Ti; wt% field left empty because the unit of % is not stated).
- Section 2.2: porosity samples outgassed for at least 12 h at 300 °C (Quantachrome Autosorb-1): degassing for the porosity analysis, not stated for the H2 measurement, so not used in degas fields.
- Fig. 5a-c, 87, 150 and 300 K: all points other than the highest-pressure one of each run, by protocol scope.

## Coding decisions

- Basis: Section 2.3 names excess and defines it by its procedure ("measuring absolute adsorption up to 60 bar, and then subtracting the empty volume contribution using the calculated volume and known system volumes"), so basis_stated = true with that quote on every row; Fig. 1 axis "Excess H2 capacity" and Fig. 5 caption "Sieverts excess H2 isotherms" agree.
- Instrument: "home-built Sieverts apparatus [21]" with a description (dosing cell, 3 overlapping pressure gauges 0-60 bar, MWBR equation of state) -> instrument_identified = true. calibration_described = true from the same Section 2.3 sentence (free volume from calculated volume and known system volumes); no gas or temperature stated, so free_volume_calibration is empty.
- measuring_lab_id: the paper does not say the H2 measurement was made in another laboratory (the apparatus is cited to ref. 21, whose authors include co-author Yildirim, NIST), so all rows carry the corresponding author's lab: "Gogotsi group, Drexel University".
- Surface area: BET, probe gas Ar (Section 2.2: "Argon sorption ... to assess porosity and surface area data"), although Section 3 says the pore characteristics were "measured under N2 and CO2 sorption". BET range and consistency criteria not stated. area_same_sample: yes for Table 1 (explicit same-batch statement), unclear for Table 2 (statement names Table 1 only).
- Fig. 5 sample labels: the panel annotations "Toutgas= 200 °C", "Toutgas= 600 °C", "Toutgas= 800 °C" (no other printed label). The room-temperature text value refers to "this CDC" without an outgassing state, so it is a separate sample S24 labelled "TiC-CDC" (the text's name for it) rather than being assigned to one of S25-S27.
- No replicate measurements or uncertainties are reported (replicates_reported = false). No wt% convention stated and no paired units (wt_pct_convention unknown / none).
