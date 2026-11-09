# HYC-0026 extraction log (agent B, 2026-11-09)

Paper: Zhao et al. 2013, Int J Hydrogen Energy 38:10453-10460, doi 10.1016/j.ijhydene.2013.06.048. Input: page images main-1..main-8 only (no SI). 53 rows written.

## Sources extracted from

- main-5.png (p. 10457), Sec. 3.3 text, left column: "ACs before doping showed outstanding capacities of 5.4, 6.0 and 6.5 wt.% at 77 K due to their high SBET, 2527, 2955 and 3434 m2/g, respectively" -> 3 text_direct rows (AC250 M1, AC300 M2, AC340 M53). No pressure is printed with these values: pressure_unstated = true. The AC300 value is not merged with a Fig. 5a point (no printed pressure; the paper does not say it is taken from Fig. 5a), so it has no isotherm_id; value_kind measured (within 3% of the digitized AC300 plateau points). AC250 and AC340 have no plotted isotherm: no isotherm_id, value_kind unclear (a "capacity" with no pressure and no measured point to compare).
- main-6.png (p. 10458), Fig. 5a, "Hydrogen adsorption isotherms at 77 K of the AC30y series" (H2 ads, wt.% vs P, MPa): AC300 (I1), AC301 (I2), AC302 (I3), adsorption (filled) and desorption (open) branches -> 50 figure_digitized rows. Branch assignment uses the full/empty convention printed in the Fig. 3 caption; the Fig. 5a caption does not repeat it, the text calls the curves "adsorption-desorption isotherms".
- main-5.png Table 3 (textural parameters, N2 at 77 K): SBET, V0.99, VDR, Ea, L0, VDR/V0.99, Vme -> characterization on every row of AC250, AC300, AC301, AC302, AC340.
- main-3.png Table 1 (elemental analysis) and main-4.png Table 2 (XPS N1s/C1s and surface wt%): N content (EA) -> dopant_concentration_wt_pct for AC301 and AC302; full EA and XPS compositions and XPS functional groups in notes / functional_groups.
- main-2.png Sec. 2.1 (synthesis: KOH activation of Taisi anthracite; urea doping at 623 K, W = 1 or 2; hot-water Soxhlet wash), Sec. 2.2.2 (N2 physisorption, ASAP 2020; degassing 48 h under vacuum at 523 K "prior to any adsorption experiment"; BET, DR, V0.99, L0/Ea per ref. [34]), Sec. 2.2.3 (H2: gravimetric analyzer, VTI Corporation, 0-8 MPa at 77 and 298 K; "counterpart excess" isotherms on HPVA-II, Micromeritics) -> method fields.
- main-1.png affiliations: corresponding author V. Fierro (*), affiliation a = Institut Jean Lamour (no university named) -> measuring_lab_id "Fierro group, Institut Jean Lamour". The paper does not say the H2 measurements were made elsewhere.

## Coding decisions

- Basis: Fig. 5 values are "H2 ads" / "Adsorbed hydrogen uptake" from the gravimetric VTI analyzer; "adsorbed" is never defined as excess, absolute or total, and no buoyancy correction is stated -> uptake_type unspecified, basis_stated false, basis_inferred unknown, measurement_method gravimetric_microbalance. The paper defines "excess" (Sec. 3.4) only for the volumetric (HPVA-II) data of Figs. 6-8, which are not isotherms and were not digitized.
- Instrument: "gravimetric analyzer (VTI Corporation)" names a manufacturer without a model -> instrument_identified false; no buoyancy/free-volume correction stated -> calibration_described false. No numerical uncertainty or repeat results ("within the experimental error interval" only) -> replicates_reported false.
- Degassing: taken from Sec. 2.2.2 ("prior to any adsorption experiment"), applied to the H2 rows: 249.85 C (523 K), 48 h; end vacuum not stated numerically.
- BET range and consistency criteria: not stated (data "treated as described elsewhere [9,30]") -> false. Area measured by the authors on the same samples -> area_same_sample yes.
- L0 coded pore_diameter_method stoeckli_L0 (average micropore diameter calculated per ref. [34], Stoeckli et al.).
- Sample numbering by first appearance (Table 1 order): S1 AC250, S2 AC251, S3 AC300, S4 AC301, S5 AC302, S6 AC340, S7 AC341. S2 and S7 have no rows (see below).
- isotherm_point_count = markers counted on Fig. 5a, both branches: I1 AC300 17 (10 filled incl. the origin marker + 7 open); I2 AC301 18 (10 filled + 8 open; no AC301 marker visible at the origin, where a coincident one would be hidden under the red and green origin markers); I3 AC302 19 (9 visible filled incl. origin + 1 filled square hidden behind the open square at ~0.25 MPa + 8 open).
- extraction_confidence: 4 for the text values; 3 for digitized points at P >= 1 MPa; 2 for points below 1 MPa (overlapping markers of all three samples) and for partly occluded markers.

## Digitization (Fig. 5a, main-6.png)

- Axes located by pixel-column/row inspection: plot frame x 145-586, y 145-385. X ticks (MPa) at px 145 (0), 200, 255, 310, 366 (4), 420, 475, 531, 586 (8); y ticks (wt.%) at px 385 (0), 351, 317, 283, 248 (4), 214, 179, 145 (7). Calibration --x1 145=0, --x2 586=8, verify 366=4 (rel. error 0.23%); --y1 385=0, --y2 145=7, verify 248=4 (rel. error 0.10%).
- Derived images (work directory, sha256 recorded in each archive): fig5a_nolabels.png = main-6.png with the three curve labels "AC300", "AC301", "AC302" painted white (boxes x226-268/y179-190, x306-349/y194-205, x386-430/y240-251; no marker or curve inside them), because the red label was otherwise detected as a marker. fig5a_redopen.png and fig5a_navyopen.png = fig5a_nolabels.png with the enclosed white interiors of the hollow red diamonds / navy triangles painted #ff00ff / #00ffff (script work/paint_holes.py: hue mask of the series colour, binary_fill_holes minus mask). Open red and navy markers share colour with the filled markers and the connecting line, so their centres are taken as the centroid of their interior. One navy hole was excluded: a white pocket (x289-291, y214-216) enclosed by the filled triangle at ~2.56 MPa, the connecting line and the left edge of the open triangle at ~2.69 MPa, outside the open triangle.
- Archives (out/digitizations/), digitize_figure.py extract --mode markers, ROI 140 140 592 392:
  - HYC-0026_fig5a_AC300_adsorption.json: #ff0000 tol 40, --open-px 2 -> 10 markers = 10 counted (incl. origin).
  - HYC-0026_fig5a_AC300_desorption.json: #ff00ff tol 10, --open-px 1, --marker-min-px 4 -> 7 = 7 counted.
  - HYC-0026_fig5a_AC301_adsorption.json: #000080 tol 40, --open-px 2 -> 10 = 10 counted.
  - HYC-0026_fig5a_AC301_desorption.json: #00ffff tol 10, --open-px 1, --marker-min-px 4 -> 8 = 8 counted.
  - HYC-0026_fig5a_AC302_adsorption.json: #339966 tol 30, --open-px 2 -> 9 = 9 visible counted (incl. origin); a 4-px fragment at the origin was rejected by the tool as too small.
  - HYC-0026_fig5a_AC302_desorption.json: #008000 tol 40, --open-px 1 -> 8 = 8 counted (ring centroids; open and filled AC302 squares have different colours).
- Not extracted: the origin markers (0 MPa, 0 wt%) of AC300 and AC302. The tool places them at -0.012 and -0.057 MPa, outside the calibrated range (flagged as extrapolations); a zero-pressure point carries no uptake. They are included in isotherm_point_count.
- Not separable: an AC302 filled (adsorption) square at ~0.25 MPa, hidden behind the open square drawn over it; only a 1-px rim of exact filled colour (#339966) is visible on its top and left edges, so its centre cannot be located. Counted in I3, not extracted. A second hidden AC302 filled square at ~0.39 MPa is possible (ambiguous blended pixels on the left edge of that open square); not counted and not extracted.
- Partly occluded filled markers (the open marker is drawn over them with a white fill), centroid of the visible part, offset up to ~2 px (~0.06 wt%): AC300 0.67 MPa; AC301 0.24, 0.37, 0.64 MPa; AC302 0.63 MPa (top strip only, likely ~2 px high) and 1.25 MPa. Noted on each row.
- Triangle markers: centroid (filled) or interior centroid (open) lies up to ~1 px below the bounding-box centre (~0.03 wt%).
- The tool's `check` subcommand was not run: the paper states no Fig. 5a value at a stated pressure (6.0 wt% for AC300 has no pressure), so archive status stays "unchecked". The prompt's step 6 (extracted marker count equals counted markers) is met for every archive.

## Values seen but not extracted

- Sec. 3.3: "N-doped ACs had adsorbed hydrogen uptakes within the range 4.4-5.4 wt.%" - a range over four samples (AC251, AC301, AC302, AC341), not a value of one sample.
- Fig. 5b (H2 ads vs N-EA content, 7 ACs): not an isotherm. It shows values for AC251 and AC341 (and AC301, AC302) that no table or text gives individually; the AC250/AC300/AC340 values equal the text values. Pressure not stated.
- Fig. 6 (H2 excess at 77 K and 4 MPa vs SBET; 36 non-doped Taisi ACs from refs [7-9,30,50] and the 7 ACs of this study): not an isotherm. Excess values of all 7 ACs (volumetric HPVA-II) are not given in tables or text. The 36 earlier ACs are previously reported data of the same group.
- Fig. 7a/7b (H2 excess at 77 K and 2 MPa vs SBET and N-XPS / N-EA, 3D) and Fig. 8 (H2 excess at 77 K and 2 MPa vs SBET): not isotherms. Excess values at 2 MPa for the ACs of this study ("our data") are not given in tables or text; the other points are literature data of refs [23], [24], [28], [29].
- Sec. 2.2.3: isotherms "at 77 and 298 K" were measured; no 298 K value or isotherm is shown anywhere in the paper.
- Introduction: DOE target of 6 wt.%; "6.6 wt.% calculated by Schlapbach and Zuttel [10]"; "H2 uptakes higher than 3 wt.% at 77 K" in KOH-activated ACs [7,8] - targets, theory or earlier work, not measurements of this paper.
- Table 4 (ANOVA SS, df, F, P for SBET and N effect) - statistics computed across this paper's and literature samples, not uptake values.
- Figs. 1-2 (XPS spectra), Fig. 3 (N2 isotherms and PSD of AC30y), Fig. 4 (SBET vs N-EA) - no H2 values.
- No non-carbon materials (calibration standards, zeolites, MOFs) are measured.

## Samples with characterization but no row

- AC251 (S2; AC250 N-doped with urea/AC = 1): SBET 2082 m2/g, V0.99 0.89, VDR 0.72, Vme 0.17 cm3/g, Ea 23.0 kJ/mol, L0 0.9 nm, VDR/V0.99 0.81; EA C 84.63, H 2.63, N 7.83, S 0.00, O 4.91 wt%; XPS C 89.1, N 5.1, O 5.8 wt%. H2 values only in Figs. 5b, 6, 7b, 8 (not digitized).
- AC341 (S7; printed "AC 341" in Table 1; AC340 N-doped with urea/AC = 1): SBET 2737 m2/g, V0.99 1.29, VDR 0.84, Vme 0.45 cm3/g, Ea 20.5 kJ/mol, L0 1.2 nm, VDR/V0.99 0.65; EA C 86.56, H 0.47, N 8.78, S 0.47, O 3.72 wt%; XPS C 87.0, N 3.5, O 9.5 wt%. H2 values only in Figs. 5b, 6, 7, 8 (not digitized).
