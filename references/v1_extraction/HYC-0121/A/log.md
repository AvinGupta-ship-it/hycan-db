# HYC-0121 extraction log (agent A)

Extracted from:
- Fig 7 (main.pdf p.4, journal p.2291): three 77 K isotherms, digitized with digitize_figure.py (markers mode). I1 = S1 TiC-CDC (800 C), filled squares, 18 rows; I2 = S2 TiC-CDC H2 annealed, hollow squares, 18 digitized rows + 1 text row; I3 = S3 activated carbon IRH33, stars, 20 rows. Archives: out/digitizations/HYC-0121_fig7_{filled,hollow,star}.json. Axes calibrated on x ticks 0 and 700 (check 400) and y ticks 0 and 3.5 (check 2.0); the series were separated by colour-independent masking (all markers black), since the tool takes only one colour.
- Text p.2291 "values up to 336 cm3 g-1 (3.0 wt %)" and Conclusions p.2292 "3.0 wt %", "24 kg m-3" and Experimental "0.8 g cm-3": merged with the last hollow-square point (756.7 mmHg = 1.00888 bar vs printed 1 atm) into one text_direct row (S2, I2) carrying 3.0 wt%, 336 cm3(STP)/g, 24 kg/m3 (packing_volume basis, no compressed gas) and 0.8 g/cm3. Attaching the 24 kg/m3 to S2 is an assumption ("bulk CDC with 3 wt%"). Step-6 check passed for hollow series (3.03 digitized vs 3.0 stated at 756 mmHg, 1.0%). No stated value exists to check the other two series.

Digitization caveats:
- Markers below about 50 mmHg overlap each other and the axis (all three series, 0 to ~25 mmHg) and could not be separated; not extracted. Tool output for filled (65.4 mmHg blob, 112 px, merged 52 and 78 mmHg squares) and hollow (66.7 mmHg fragment, 9 px, partial 52 mmHg square) were dropped as non-single-marker artefacts, remaining in the archives. The 52 mmHg squares of the filled and hollow series (about 1.15 and 1.27 wt%) are therefore not extracted. The hollow 78 mmHg square is slightly overlapped (71 px) and kept.
- isotherm_point_count (22, 22, 20) counts identifiable markers including the obscured ones near the origin by eye; the exact number there is uncertain.
- Pressure axis in mm of Hg converted x 0.00133322 to bar. No branch is labelled; all adsorption.

Not extracted (with reason):
- Fig 1 (uptake at 1 atm vs BET SSA, many carbons, literature plus CDCs), Fig 5 (uptake at 1 atm vs volume/SSA of pores <1 nm and >1 nm), Fig 6 (uptake at 0.1 atm vs pore volume <1 nm), Fig 8 (uptake per area vs heat), Fig 9 (heat vs volume adsorbed): not isotherms; samples are unlabelled points of a CDC series with uptake values that the tables and text do not give (e.g. 1.0 to 2.9 wt% at 1 atm in Fig 5, 0.6 to 1.4 wt% at 0.1 atm in Fig 6); no per-sample identity, so not rows.
- Fig 3 PSDs and Fig 4 TEM: no uptake. Fig 3 gives SSA/pore data graphically only; no per-sample numbers printed for Fig 7 samples.
- Text: "increased the storage by as much as 75 %", MOF-5 1.3 wt%, Cu3(BTC)2(H2O)3 1.4 wt%, [Co3(bpdc)3bpy] 2 wt%, MOF-505 2.48 wt%, CNTs below 0.9 wt%: other materials or literature values, not extracted. Heats of adsorption (6.6 to 11 kJ/mol) not an uptake.
- "Liquid-argon temperature (-186 C)" measurements are mentioned as made, with no values or plotted isotherms shown.
- Trace metal up to 0.5 at% in CDC: unspecified element, not coded.

Coding notes: no surface area stated for any sample as a number (SSA only in figures) so surface_area_method = none; basis not named, Autosorb-1 not stated as volumetric so measurement_method = unknown and basis_inferred = unknown; wt% convention W1 stated in Experimental (gas mass per sorbent mass, "slightly higher values" than per total mass).
