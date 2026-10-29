# HYC-0075 extraction log (agent B)

Input: 10 page images (main-01 to main-10); no supplementary file. 126 rows.

## Sources extracted

- main p2, section 2.2 (synthesis of ACBS12/13/14/16 from sword bean shells; KOH/BS = 2, 3, 4, 6): synthesis, activation and purification fields on every ACBS row.
- main p2, section 2.3.4 (N2 physisorption at 77 K, Micromeritics ASAP 2020 HD88; S_BET, V_DR, V0.99, L0 from N2 data; outgassing 523 K > 24 h): surface-area method and probe gas, pore-volume method; BET range not stated.
- main p2, section 2.3.5 (H2 uptake: "Gravimetric Analyser HPVA-100", H2 99.9999 %, up to 40 bar at 77 K; ASAP 2020 HD88 up to 1 bar at 77 K; degassed under primary vacuum at 473 K for at least 12 h): method, instrument, purity and degassing fields.
- main p4, Table 1 (EA: N, C, H, O by difference, C/N, C/O): N content as dopant_concentration_wt_pct; full EA in notes.
- main p4, Fig. 3d (SEM-EDX of ACBS14) and main p5, section 3.3 and Fig. 4 (XPS of ACBS14): functional groups and composition on ACBS14 rows (notes); EDX and XPS values not used as dopant concentration (EDX is neither XPS nor EA; XPS unit not stated).
- main p5, section 3.4 and main p6, Fig. 5b (Raman ID/IG 0.988, 0.980, 0.969, 0.955): in notes.
- main p7, Table 2 (S_BET, V0.99, V_DR, E_A, L0, V_DR/V0.99, Vmeso): characterization on every ACBS row.
- main p6, section 3.6 ("The highest hydrogen storage capacity obtained was 2.63 wt% for sample ACBS16"): merged with the Fig. 7a ACBS16 1.0-bar point (row M95).
- main p6-7, section 3.6 ("the excess adsorption isotherms of all four ACBS samples at 77 K were measured with high pressure up to 40 bar"; "reached up to 5.74 wt% at 40 bar and 77 K"; "2.63 and 5.74 wt% up to 1 bar and 40 bar"): basis naming for the Fig. 7b isotherms; 5.74 merged with the Fig. 7b ACBS16 40-bar point (row M124).
- main p1, abstract, and main p8-9, conclusions (2.63 and 5.74 wt% at 77 K, 1 and 40 bar): same measurements as rows M95 and M124, not separate rows.
- main p7, Fig. 7a (77 K isotherms to 1 bar, four series): all separable markers digitized (rows M1-M94 and M95 merged).
- main p7, Fig. 7b (77 K isotherms to 40 bar, four series): all separable markers digitized (rows M96-M124, M124 merged).
- main p8, Table 3, row "sword bean shell" (Ref. "This work"): ACBS16 values 2.63 wt% at 1 bar and 5.74 wt% at 40 bar/77 K (rows M95, M124), identified as ACBS16 by S_BET 2838 m2/g, N 1.67 wt% and the text.
- main p8, Table 3, row "Maxsorb 3 (commercial sample)" (Ref. "This work"): 2.10 wt% at 1 bar and 5.80 wt% at 40 bar/77 K (rows M125, M126); surface area 3203 m2/g.

## Digitization (scripts/digitize_figure.py extract --mode markers)

- Fig. 7a calibration (page pixels, main-07.png): x 0 bar at 245.1 (axis line; the 0.0 tick coincides with it), 1.0 bar at 558.64, check 0.6 bar at 433.27 (rel. error 0.02 %); y 0 wt% at 642.26 (axis line), 3.0 wt% at 399.63 (axis line), check 1.5 wt% at 520.68 (rel. error 0.22 %). Tick positions from intensity-weighted pixel centroids.
- Fig. 7b calibration: x 0 bar at 759.96, 40 bar at 1023.86, check 20 bar at 892.26 (rel. error 0.27 %); y 0 wt% at 625.2, 6 wt% at 418.63, check 3 wt% at 522.02 (rel. error 0.05 %).
- The legend symbols and the panel label inside each plot frame were painted white in working copies of the page image (work/fig7/page7_f7a_masked.png: x 478-572, y 562-640 and x 252-305, y 402-440; work/fig7/page7_f7b_masked.png: x 952-1055, y 560-640 and x 742-795, y 404-445) so they are not read as markers; no data marker lies in those regions. Calibration is in the unchanged page pixel coordinates.
- Settings and counts (extracted / counted on the plot, origin excluded):
  - fig7a_ACBS12.json: #000000, tolerance 90, open 3: 25 / 29. Markers at about 0.05, 0.08, 0.11 and 0.15 bar are hidden under the ACBS13, ACBS14 and ACBS16 markers and could not be separated; not extracted.
  - fig7a_ACBS13.json: #fc0101, tolerance 90, open 2: 25 / 29. Markers at about 0.11, 0.15, 0.19 and 0.22 bar hidden under ACBS14/ACBS16 markers; not extracted. (Tolerance 120 gave one extra 6-px fragment displaced 2 px from the pressure grid at 0.107 bar; not used.)
  - fig7a_ACBS14.json: #0000fc, tolerance 120, open 2: 16 / 29. The 13 markers from about 0.01 to 0.43 bar lie under the ACBS16 diamonds (only slivers visible); not extracted. Several extracted ACBS14 markers are partly covered (6-10 px visible); their centroids are of the visible part (confidence 2).
  - fig7a_ACBS16.json: #008000, tolerance 60, open 3: 29 / 29.
  - fig7b_ACBS12.json: #000000, tolerance 90, open 3: 8 / 8.
  - fig7b_ACBS13.json: #fe0101, tolerance 90, open 3: 7 / 8. The marker at about 2.1 bar (about 2.57 wt%) is under an ACBS14 triangle; not extracted.
  - fig7b_ACBS14.json: #0000fe, tolerance 120, open 3: 7 / 7 (region starts at x 765 px to leave out the origin marker).
  - fig7b_ACBS16.json: #008000, tolerance 90, open 3: 7 / 7.
- The Fig. 7a point count of 29 per series is the common pressure grid (29 markers on the fully visible ACBS16 series; fragments of the hidden markers of the other series are visible at the same pressures).
- Plotted origin (0 bar, 0 wt%) of every series in Fig. 7a and 7b: not a measured uptake, not extracted and not counted. In Fig. 7a only a clipped fragment is visible at the axis corner; in Fig. 7b the four origin markers are stacked.
- Rows with fewer than 12 visible marker pixels have extraction_confidence 2 and a note; other digitized rows 3.
- check (step 6): fig7a_ACBS16 at 0.9998 bar (the digitized end of the series, for the printed 1 bar) 2.617 vs 2.63 printed, 0.49 %, pass; fig7b_ACBS16 at 39.945 bar 5.742 vs 5.74 printed, 0.04 %, pass. The other six archives have no printed value to check against and remain "unchecked".
- Observation for reconciliation: the low-pressure (ASAP 2020) and high-pressure (HPVA-100) data disagree near 1-2 bar (for example ACBS12: 2.09 wt% at 1.0 bar in Fig. 7a, 1.44 wt% at 1.8 bar in Fig. 7b); both are recorded as plotted.

## Coding decisions

- Labels: ACBS16 is printed as "sword bean shell" in Table 3, the first table giving its uptake; that cell names the precursor shared by all four samples rather than a sample label, so the label ACBS16 (Tables 1-2, figure legends, text) is used. Maxsorb 3 is labelled "Maxsorb 3" (Table 3 cell "Maxsorb 3 (commercial sample)").
- Sample numbering follows section 2.2, where the samples first appear as KOH/BS = 2, 3, 4, 6 (S1 ACBS12, S2 ACBS13, S3 ACBS14, S4 ACBS16), then S5 Maxsorb 3 (first named on p7).
- Fig. 7a isotherms (ASAP 2020 HD88): measurement_method volumetric_sieverts from the instrument type (the paper does not name the technique); no basis named, so basis_inferred excess by the instrumental default; uptake_type unspecified; instrument_identified true (Micromeritics ASAP 2020 HD88 named in section 2.3.4).
- Fig. 7b isotherms: the paper calls the instrument "Gravimetric Analyser HPVA-100"; coded gravimetric_microbalance as printed, instrument_identified false (no manufacturer). The paper calls them "excess adsorption isotherms" without a definition: uptake_type excess, basis_stated false, basis_inferred excess, quote in basis_evidence.
- Maxsorb 3: section 2.3.5 names instruments only for "a series of ACBS", so measurement_method unknown, basis_inferred unknown, instrument_identified false, degassing and H2 purity empty. The two values come from the low- and high-pressure measurements (different instruments) with no plotted curve, so they are not treated as one isotherm and carry no isotherm_id. Surface area 3203 m2/g is printed without method and without saying whether the authors measured it: surface_area_method unspecified, probe gas unspecified, area_same_sample unclear.
- material_class doped_carbon for the ACBS samples: the paper states that N and O heteroatoms were incorporated into the carbon framework; dopant_element "N, O"; dopant_concentration_wt_pct is the EA nitrogen content.
- pore_diameter_method stoeckli_L0: Table 2 L0 equals 10.8/(E_A - 11.4) for all four samples. Vmeso equals V0.99 - V_DR for all four samples.
- Degassing for H2: 473 K printed, stored as 199.85 C; "at least 12 h" stored as 12 h; end pressure "primary vacuum" not a number, left empty.
- wt% convention unknown/none on all rows (no value printed in a second unit).
- No uncertainty, error bars or repeated isotherms reported: replicates_reported false. No free-volume calibration or buoyancy correction stated: calibration_described false.

## Values seen but not extracted

- Table 3 (main p8), values from other papers, not measured in this work: rice husks 2682 m2/g, 2.85 wt% at 1 bar/77 K [41]; tamarind seeds 1785 m2/g, 4.73 wt% at 40 bar/303 K [42]; chitosan 1049 m2/g, 2.95 wt% at 1 bar and 5.61 wt% at 40 bar/77 K [4]; polyacrylonitrile 2206 m2/g, N 1.29 wt%, 2.66 wt% at 1.2 bar/77 K [24]. The remaining Table 3 rows (glucose and melamine [43], polyaniline [44], polypyrrole [45], rapeseed dregs [46], sodium alginate and urea [47], waste shrimp shells [48], oil tea shell [49]) give no H2 value.
- Fig. 7c and 7d (main p7): H2 capacity at 77 K and 1 bar and at 77 K and 40 bar plotted against V_DR and S_BET for the four ACBS samples, with linear fits (R2 = 0.98, 0.93, 1, 0.98). Not isotherms, not digitized. ACBS16's values are printed in the text and Table 3; the ACBS12, ACBS13 and ACBS14 values are not printed in tables or text and are the end points of the Fig. 7a and 7b isotherms, digitized there.
- Hidden isotherm markers listed under Digitization (Fig. 7a: 4 ACBS12, 4 ACBS13, 13 ACBS14; Fig. 7b: 1 ACBS13) and the plotted origins: not extracted.
- Sword bean shell charcoal BSC (carbonized at 723 K, precursor of all ACBS): no H2 uptake; characterization only: TG carbonization yield 32 % (Fig. 2, section 3.1); "surface area ... not large enough" (no number). No row.
- Fig. 2 TG yield of ACBS14 activation 72 %; Fig. 5a XRD peaks at about 23 and 44 degrees (no d-spacing printed); Fig. 6a N2 isotherms and Fig. 6b NLDFT PSD; V_DR/V0.99 0.55-0.75 (Table 2): characterization, not H2 uptake.
- Electrochemical results (Fig. 8, sections 3.7 and 4, Table 3): specific capacitances (183 F/g at 2 mV/s, 211 F/g at 0.5 A/g, 93 F/g for Maxsorb 3, 138 F/g after 5000 cycles), energy density 16.7-19.5 Wh/kg, internal resistances 0.44, 0.42, 0.40, 0.31 ohm: not H2 uptake.
