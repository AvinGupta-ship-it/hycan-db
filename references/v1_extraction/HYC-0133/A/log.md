# HYC-0133 extractor A log

Extracted from
- Fig. 2a (main p.8): rN-pC 77 K excess squares (I1, 20 rows after dropping origin), 87 K excess highest-pressure circle (I2), 77 K absolute line at 10 pressures (I3), 87 K absolute line end point (I4). Archives in digitizations/. Squares/circles are hollow and overlap; I cleaned the page image (fill holes, opening, whiteout of legend/text) into work images and ran extract --mode markers on them. Calibration ticks verified on a third tick; `check` passed for all six archives.
- Text Sec. 3.2 (main p.7): ~2.5 wt% at ~0.8 MPa (77 K), ~2.3 wt% at ~1.5 MPa (87 K), absolute ~3.4/~3.0 wt% at ~6 MPa, 17.3 g/L (on the 3.4 wt% row), 0.9 wt% and 0.55 wt% at 0.01 MPa (merged with Fig. S6 points, I5/I6).
- Fig. S6 (SI p.4): 77 K squares (I5, 18 digitized rows + merged text row), 87 K highest-pressure circle merged with text row (I6).
- Table S4 (SI p.15): max excess 2.49 wt% (rN-pC), adsorbed-phase density 0.02629 g/cm3.
- Table S1/S2, text: rN-pC characterization (BET 1525.4, V_DFT 1.498, V_DFT(MP) 0.447, S_DFT(MP) 1326.3, N 5.97 at% XPS / 6 wt% text, skeletal density 2.15).

Markers not separated (Fig. 2a 77 K): about 10 overlapping squares, 7 in the stack at 1.2-1.85 wt% (p<0.12 MPa) and 3 at 2.19-2.31 wt% (p 0.26-0.40 MPa); positions estimated only by template matching, not extracted. Origin marker (0,0) digitized at -0.003 MPa, 0.001 wt%; not written (pressure 0 fails validator). isotherm_point_count I1 = 31 (21 digitized + ~10 estimated), approximate. I2 = 26 approximate (circles overlap at p<0.5 MPa; only the highest-pressure one is extracted). I5 = 20 and I6 = 17 include an origin marker overlapped in the figure (not extracted).
Fig. 2a dashed fit lines not digitized (fits through the markers).

Not extracted (reason)
- 60MgH2@rN-pC and 60Mg@rN-pC composite (60 wt% MgH2, carbon is 40 wt%, so not a carbon sorbent under section 3 majority-by-mass rule; MgH2 is a hydride): Fig. 4a 77 K excess isotherm (0.66 wt% max, 12-ish markers to ~3.7 MPa, absolute curve), Fig. S15a ultralow-pressure 77/87 K, text 0.66 / 0.62 / 0.7 wt% physisorption, 0.045 g/cm3 density, Table S4 row (0.66 wt%, rhoA 0.04542), 43.5 g/L, 33.4 g/L pellet, Fig. 4b cycling (0.52/0.20 wt%), Fig. S26 ~0.6 wt% at RT, TPD/isothermal desorption/absorption values (3.38, 3.41, 0.93, 2.76 wt%, 3.85, 4.2, 3.5, 3.52/3.47, 3.24/3.17, 2 wt% etc.), PCT. If C judges the composite eligible these need extraction.
- Pure MgH2 values (6.8 wt% TPD, 7.3/5.9, 4.71, 0.72 wt%): hydride.
- Fig. 2b Qst, Fig. 5, Fig. 4b, Fig. 6: not isotherms.
- Table 1 literature values (other works) and [91] 3.25 wt%: other papers.
- ZIF-8 (MOF) BET 1877.3 and N-pC (BET 1146.5 in Table S1; text prints 925.8 m2/g, 0.92 cm3/g, mismatch with Table S1 SDFT(MP) 921.5): characterization only, no H2 uptake, no row.
- Table S4 fit parameters b, c, vp (1.77791 cm3/g): model parameters, not uptake.
- Intro "close to 1% at 0.01 MPa" duplicates the 0.9 wt% row.
- Qst values (14, 10.6, 6 kJ/mol): not uptake.

Judgement calls
- measuring_lab_id: the paper says Y. Li and L. Ren carried out the H2 tests (SJTU); first corresponding author Ferrari is Cambridge. Used the SJTU lab (Li). C may prefer Ferrari group, University of Cambridge.
- Fig. S6 legend names "absolute adsorption" (undefined) so basis_stated false, inferred absolute; Fig. 2a excess/absolute side by side so basis_stated true.
- Instrument "HPSA-auto device, China": no manufacturer, so instrument_identified false. No free-volume calibration or buoyancy statement, calibration_described false.
- Degassing 300 C 12 h from Sec. 2.3 ("all samples outgassed"); end pressure not stated; sample mass for physisorption not stated (~100 mg is for the kinetic tests).
- N content: text says 2.5 to 6 wt% via XPS, Table S2 gives at% 2.33 to 5.97; both stored.
- Temperatures -196/-186 C stored as 77.15/87.15 K.
