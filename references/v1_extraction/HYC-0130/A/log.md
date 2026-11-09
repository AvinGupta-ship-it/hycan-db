# HYC-0130 extraction log (agent A)

## Extracted from
- Table 5 (main.pdf p.8, RSC p.20419), "This publication" rows (ACZ-3-8, ACK-3-8, ACK-2-7, ACK-2-8, ACK-2-8-1, ACK-2-8-2, ACK-2-8-3): H2 uptake in mg g-1 at -196 C and 1 bar (the pressure comes from the Section 3.4 text; the table prints none), and H2 uptake per SBET in mg m-2 (stored as areal_uptake_g_cm2, per BET area). 7 rows M1-M7. Each is the same measurement as the last plotted point of its isotherm and carries that isotherm_id with the digitized point in notes.
- Section 3.4 text and abstract: 17.3 mg g-1 (ACK-2-8) and 25.2 mg g-1 (ACK-2-8-2) repeat Table 5 values; no separate rows.
- Tables 3 and 4 (p.5-6): SBET, Vtotal, Vmicro, D of the seven sampled carbons, copied onto every row of each sample. Table 2: samples without H2 uptake (see below).
- Section 2.3: instrument (NOVA 3200e, Quantachrome, static gas adsorption), H2 pressure range 0.01-1 bar at -196 C; surface area by BET (N2 at -196 C, JW-BK122W analyzer), Vmicro by t-plot.
- Fig. 7a (p.8): four 77 K isotherms, ACK-2-7 (I1), ACK-2-8 (I2), ACK-3-8 (I3), ACZ-3-8 (I4). Digitized with digitize_figure.py in markers mode; archives Fig7a_*.json.
- Fig. 8 (p.8): four 77 K isotherms, ACK-2-8 (I5), ACK-2-8-1 (I6), ACK-2-8-2 (I7), ACK-2-8-3 (I8). Archives Fig8_*.json.
- Total 229 rows: 7 table rows and 222 digitized rows.

## Digitization notes
- Calibration, both figures: lowest and highest labelled ticks, third labelled tick as check (all residuals under 0.3%). Fig. 7a x 0 and 1.0 at px 269.5 and 612.5, check 0.4 at 406.5; y 0 and 200 at px 353.5 and 122, check 100 at 237.5. Fig. 8 x 0 and 1.0 at px 160.5 and 582.5, check 0.4 at 329; y 0 and 300 at px 1418 and 1105.5, check 150 at 1261.5.
- The page image is 150 dpi and the open markers are outlined 1-2 px wide, so the tool's default 2-px opening removed them. Every extraction used --open-px 1 and a series colour with a tolerance of 40-130, run over several regions of interest (legend, panel label and other series excluded). The final series in each archive is the union of those tool runs, cleaned by me; each archive records the runs (`extraction.runs`) and the cleanup (`cleanup`). Every archive passed `digitize_figure.py check` at its last point against the Table 5 value (converted with 22.414 mL mmol-1), tolerance 5%.
- Marker counts (isotherm_point_count = 30 for all eight): purple (I4) 30 detections, black (I5) 30, black (I1) 29 + 1 hidden, blue (I3) 29 + 1 hidden. For the covered series the count is detections plus hidden markers, and the hidden positions are estimates from the neighbouring series, not read from the plot.
- Hidden or unrecovered markers (not extracted): I1 first marker (x about 0.005 bar); I3 first marker (about 0.005); I2 markers at about 0.005, 0.037, 0.078 bar; I6 markers at about 0.005, 0.045, 0.07 (only 3 px fragments visible); I7 markers at about 0.005, 0.105, 0.138 (under the purple series); I8 and I4 and I5 none.
- Fragments dropped (<=5 px, part of an already-counted marker or stray pixels): I6 detections at x = 0.0494, 0.0636, 0.0652, 0.2109, 0.3809, 0.5525, 0.8917; I8 detection at x = 0.1576. Fragment pairs merged into one weighted centroid: I6 x = 0.6451 + 0.6478; I7 x = 0.0692 + 0.0814. A stray pixel group at x = 0.055 (Fig. 7a purple) was excluded by region.
- I2 (ACK-2-8 in Fig. 7a): the red open circles lie under the blue triangles, only the upper arc shows, and the digitized values sit about 3 cm3 g-1 above the ACK-3-8 values at the same x; they are biased high. Confidence 2 on all I2 rows. The same sample is digitized in Fig. 8 (I5) with an unobstructed marker; at 1 bar the two differ by 0.1-0.6%.
- Partly covered markers (pixel count below 60% of the series median) are flagged in notes with confidence 2.
- Axis unit is printed "cm3/g" with no STP statement; stored in uptake_ml_stp_g and converted to W1 with 0.0089938.
- Fig. 7a and Fig. 8 both plot ACK-2-8. The paper does not say they are one run, so they are separate isotherms (I2, I5). The table value merges with the plotted point closest to 1 bar (Fig. 7a, x = 0.9898 against 0.9882 in Fig. 8).

## Codes and decisions
- Sample numbering follows first appearance among samples that have H2 rows: ACK-2-8 (S1, abstract), ACK-2-8-2 (S2), ACK-2-8-3 (S3), ACK-2-8-1 (S4, Section 2.2), ACZ-3-8 (S5), ACK-2-7 (S6), ACK-3-8 (S7). Samples with no H2 value do not get ids.
- No basis named (uptake_type unspecified, basis_stated false). Volumetric instrument, so basis_inferred = excess. No buoyancy or free-volume statement, so calibration_described false.
- wt% convention not defined in the paper. Table 5 prints mg g-1 only, so the stored wt% is 0.1 x mg g-1 (W1, computed_from_other_unit).
- Temperature -196 C printed; stored as 77.15 K, not inferred.
- BET range and consistency criteria not stated. Degassing, sample mass, H2 purity and free-volume calibration are not stated anywhere (text, SI): left empty. replicates_reported false (no uncertainty, no repeats).
- synthesis_method = carbonization (cyanobacteria carbonized at 400 C); KOH/ZnCl2 activation in activation_method. Doped samples are doped_carbon (N from HNO3 or NH3.H2O, P from H3PO4); dopant concentrations are not printed (XPS spectra only), left empty.
- Measuring lab: corresponding author Hui Hu (asterisk), first affiliation Huazhong University of Science and Technology.

## Seen but not extracted
- Table 5 "Ref." rows (C-4, P2, carbide-derived carbons, MOFs, zeolite-based carbons, PC-2-800, ACs, CAC, UCs): other papers' values, not this paper's measurements.
- Text percentages (16.8%, 31.8%, 45.7% higher than ACK-2-8; 49.1% higher than ACZ-3-8): derived comparisons.
- Fig. 7b (uptake vs SBET; ACZ-3-8, ACK-2-7, ACK-3-8, ACK-2-8 at about 11.6, 16.7, 17.1, 17.3 mg g-1): not an isotherm; every value is in Table 5. Fig. S4 (uptake vs SBET): same, not digitized.
- Table 1 and Table S1 (cyanobacteria proximate, ultimate and ash analysis): no H2 data. Fig. 1, 2, 3, 4 (TG, N2 isotherms, pore size distributions), Fig. 5 SEM, Fig. 6 XPS, Fig. S1-S3: not H2 isotherms.
- Samples with characterization but no H2 uptake value (no rows): ACK-0.5-6, ACK-1-6, ACK-2-6, ACK-3-6, ACZ-1-6, ACZ-2-6, ACZ-3-6 (Table 2: SBET 644, 705, 1006, 970, 901, 996, 1268 m2 g-1); ACK-3-7 (1111) and ACZ-3-7 (1176), ACZ-3-6 (Table 3); AC (carbonized only, Fig. S2); cyanobacteria CB.
