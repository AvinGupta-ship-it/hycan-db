# HYC-0126 extraction log (agent A)

Extracted from
- main.pdf p.4 (journal p.707), text paragraph on Figure 7: 1.2 wt% at 850 mm Hg, 77 K, mesoporous carbon (row M1, text_direct, same measurement as the last marker of Figure 7 curve c).
- main.pdf p.4, Figure 7 curve c (mesoporous carbon, 77 K H2 adsorption): 35 markers counted, 34 digitized (rows M2-M35, archive digitizations/HYC-0126_fig7_curve_c.json, tolerance 80, ROI inside the plot frame, curves a, b and label c masked on a copy of the page image in the work directory). Calibration ticks: x 0 -> px 281, 850 mmHg -> px 460 (third tick 510 mmHg checked, error 0.37%); y 0 -> px 557, 150 -> px 391 (third tick 90 checked, error 0.40%). Check step passed at x=823.88 mmHg against the text value (133.4 cm3/g = 1.2 wt%), 0.43%.
- Marker 35 (the last, at the plot frame, x about 850 mmHg) is partly hidden by the frame and merges with marker 34 in the tool. It was isolated on a masked copy (frame column kept only in a 7-pixel stub, marker 34 erased) and digitized as a single-point archive, digitizations/HYC-0126_fig7_curve_c_edge_marker35.json (846.84 mmHg, 133.886 cm3/g; x is biased low by clipping). The tool's check cannot run on a one-point archive, so that archive stays status "unchecked". It is the point the text value 1.2 wt% at 850 mmHg belongs to (0.4% in pressure; 1.204 wt% vs 1.2), so it is recorded in the notes of M1 and has no separate row.
- Sample characterization (main text p.3-4): mesoporous carbon surface area 850 m2/g, pore volume 0.50 cm3/g, average pore diameter 2.5 nm (Fig. 6, N2 sorption, method not named); TGA (Fig. 4 curve b) 97% weight loss. Experimental on p.4: Micromeritics ASAP 2010, N2 and H2 sorption at 77 K; synthesis, 900 C 4 h N2 carbonization, HF removal of silica.

Seen but not extracted
- Figure 7 curve a (mesoporous phenylene/silica hybrid) and curve b (mesoporous carbon/silica composite), 77 K H2 isotherms, plus text values "around 0.6 to 0.7 wt.-%" at 850 mm Hg for both. Not carbon sorbents under section 3: the composite is about 36.5 wt% carbon by TGA (expected 37.5%) with silica the majority, and the hybrid is phenylene-bridged silica. Not extracted. Characterization seen: hybrid 680 m2/g, 0.91 cm3/g, BJH peak 2.8 nm; composite 860 m2/g, 0.70 cm3/g, peak 2.0 nm.
- Figure 2 (N2 isotherms of hybrid and composite), Figure 6 (N2 isotherm of mesoporous carbon, no H2): not H2 uptake, not digitized.
- Figures 1, 3, 4, 5, SI Figures S1-S9 (XRD, TEM, TGA, EDS, 29Si NMR): no H2 uptake values.
- Text statement that higher H2 capacities at higher pressure are expected: no value.

Coding notes
- No printed sample label for the mesoporous carbon (Figure 7 curve letters label curves only), so the label is (unlabelled 1).
- measurement_method = unknown and basis_inferred = unknown: the paper names the analyzer (ASAP 2010) but not the method, the basis or a free-volume or buoyancy correction.
- wt% convention: the paper prints only wt% for the text value (no printed paired unit), so unknown/none; digitized rows carry W1 computed from cm3(STP)/g.
- Surface area method not named, so surface_area_method = unspecified, bet_range and consistency codes left empty.
- No degassing, sample mass or H2 purity stated.
