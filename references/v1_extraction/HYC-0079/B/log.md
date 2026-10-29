# HYC-0079 extraction log (extractor B)

## Sources extracted

- main-2.png (p. 4544), Figure 1: CMK-3 at 77 K, absolute adsorption by four excess-to-absolute conversion methods; four lines without markers, each read at k/10 x p_end (rows I9-I12).
- main-6.png (p. 4548), Figure 9: excess isotherms of NCCR-41, NCCR-56 and CMK-3 at 77 K (left axis) and 298 K (right axis). Every separable 77 K marker digitized; only the highest-pressure 298 K marker of each isotherm digitized (rows I1, I2, I5, I6, I13, I14).
- main-6.png (p. 4548), Figure 10: excess isotherms of CMK-1, NCCR-11 and CMK-8 at 77 K and 298 K, handled the same way (rows I17, I18, I21, I22, I25, I26).
- main-6.png (p. 4548), text, Results 3.2: "NCCR-41 ... 0.29 wt % at 50 bar at room temperature and 2.0 wt % at 77 K and 8 bar pressure". The 0.29 wt% value was merged with the Figure 9 NCCR-41 298 K point at 50.2 bar. The 2.0 wt% value was kept as a separate row with no isotherm_id, because no plotted point lies within tolerance of 8 bar (nearest points: 8.807 and 14.750 bar).
- main-7.png (p. 4549), Table 3: n_max (mol/kg) for the six carbons, stored as mmol/g with W1 computed. These are model parameters (fitted_extrapolated), with temperature and pressure flagged unstated.
- main-7.png (p. 4549), Figures 11 and 12: modified D-A model predictions of absolute adsorption. 77 K lines read at k/10 x p_end; at 298 K only the highest-pressure end was extracted (rows I3, I4, I7, I8, I15, I16, I19, I20, I23, I24, I27, I28).
- main-5.png (p. 4547), Table 2: characterization of the six carbons, carried on every row of each sample.
- main-2.png (p. 4544), Methodology: instrument (Micrometrics HPVA, as printed), H2 purity 99.9995%, outgassing at 473 K overnight in vacuum, N2 sorption on a Micrometrics ASAP 2020, and basis definition (eq 1).

## Digitization method

- Each axis was calibrated on its lowest and highest labelled ticks, with a third labelled tick as a check. Every tick position was found from pixel-row and pixel-column profiles of the page image. All verification residuals were below 0.3%.
- Figures 9 and 10: the fit lines share each series' colour and are drawn over the hollow markers, so the digitizer could not separate markers directly. Marker centres were found by outline template matching on the page image (work/scripts/tm.py), seeded from automatic detections that were checked in zoomed overlays. A derived image with the same pixel geometry as the page, holding one small block per marker centre, was then passed to `digitize_figure.py extract --mode markers`. Each archive's source_image is that derived image (work/derived/<name>.png). Detection scores are in work/derived/<name>_det.json.
- Lines (Figures 1, 11 and 12): each line was isolated by colour into a derived image (work/scripts/clean.py), with the legend masked. Same-colour 77 K and 298 K lines were separated by a dividing polyline; for CMK-1 the polyline flips side at the crossing near 43 bar. Each derived image was run with `--mode curve`, and values were interpolated linearly between neighbouring trace points (work/scripts/interp.py). p_end is the visible end of each trace at the right frame or at the end of the last dash.
- Figure 1 liquid-density line: below about 2.9 bar it is hidden under the magenta line. Its drawn start (about 0.35 bar, the same as the other lines) was taken as p_start, so it was read at k/10 x p_end.
- Archives keep the tool status "unchecked". The tool's own "check" step is not part of this protocol, and the paper states no values for these series except the two NCCR-41 text values.
- Tool check run: `check` was run on fig9_NCCR-41_77K.json at x = 8 bar against the text value 2.0 wt%. Interpolation gave 1.894 wt% (-5.3%), so it failed and the tool marked the archive "discarded". I consider this a paper inconsistency, not a calibration error: the third-tick residual is 0.2%, and the highest plotted NCCR-41 77 K marker is 1.944 wt% at 14.75 bar, so 2.0 wt% matches no plotted point. The archive was regenerated with identical calibration, seeds and output. The discarded copy is kept at work/derived/fig9_NCCR-41_77K_check_discarded_record.json.
- The check could not run on fig9_NCCR-41_298K_highest.json, because 50 bar lies outside its single point at 50.20 bar. The text value 0.29 wt% is 4.6% above the digitized 0.2772 wt%.

## Markers that could not be separated, or are uncertain

- Figure 10, NCCR-11 at 77 K: most stars are hidden under the NCCR-11 dashed fit line and coincide with CMK-8 squares. Digitized only: 1.47, 2.72, 3.97, 10.22, 14.39, 20.01 and 36.26 bar, plus 45.42 bar (negative, not a row). Not separable: stars near 0.6, 5.4, 7.5, 26.2 and 31.5 bar, and near 40.6 and 50 bar (negative region). A star at 31.0 bar (0.49 wt% on the left-axis scale) was judged to belong to the 298 K branch. The isotherm_point_count of 15 is approximate.
- Figure 10, CMK-8 at 77 K: the marker near 50 bar lies below 0 wt% (negative region) and was not digitized. It is counted in isotherm_point_count = 15.
- Figure 9, the first 77 K markers of NCCR-41, NCCR-56 and CMK-3 near 0.4-0.5 bar: they overlap each other, the fit lines and the left frame, and their centres come from partial outlines (confidence 2).
- Figure 9, CMK-3: the 77 K and 298 K circles overlap near 26-27 bar. The circle at 26.33 bar was assigned to 77 K; the assignment is uncertain.
- Figure 10, CMK-8: the 77 K and 298 K squares overlap near 31 bar. The square at 31.67 bar was assigned to 77 K; the assignment is uncertain.
- All six 298 K highest-pressure markers (at or near 50 bar) are clipped by the right plot frame, and their centres come from weak partial-outline matches (confidence 2). The NCCR-11 298 K star at 50.0 bar is the weakest of these.
- 298 K isotherm_point_count values (NCCR-41 14, NCCR-56 16, CMK-3 14, CMK-1 19, NCCR-11 15, CMK-8 15) are approximate. The low-pressure 298 K markers of the three series in each figure overlap heavily.

## Values seen but not extracted

- Negative excess values in Figure 10 at 77 K (the schema requires uptake >= 0; digitized values are in the archives):
  - CMK-1: 38.234 bar, -0.3625 wt%, and 49.481 bar, -0.8316 wt%.
  - NCCR-11: 45.420 bar, -0.3925 wt%.
  - CMK-8: 40.629 bar, -0.1279 wt%, and 45.420 bar, -0.4647 wt%.
  - Not digitized: CMK-8 near 50 bar (about -0.75 wt%), and NCCR-11 near 40.6 and 50 bar (negative region).
  - The NCCR-56 and CMK-3 77 K series in Figure 9 show no markers beyond 45 bar; their fit lines reach 0 wt% at the bottom axis near 46-47 bar.
- Negative absolute values in Figure 1 at p_end = 49.790 bar: effective thickness method -0.2498 wt% and liquid density method -0.3089 wt%. The schema requires uptake >= 0.
- 298 K excess markers other than the highest-pressure point of each isotherm (Figures 9 and 10): excluded by the scope for temperatures other than 77 K.
- Modified D-A fit lines through the excess markers in Figures 9 and 10: these are model fits of isotherms whose measured points (the markers) were extracted.
- Graphical abstract (main-1.png, p. 4543): schematic excess and absolute 77 K curves for an unidentified "Ordered Mesoporous carbon". No sample is identified, so it was not digitized.
- Introduction (p. 4543): "maximum hydrogen adsorption capacity reported for unactivated CMK-3 was 1.8 wt % at 77 K and 8 bar" (ref 15). This is another group's measurement on another sample, not this paper's data.
- Table 3, other columns: R2, alpha, beta, p0 (MPa), m and V_a (m3/kg) are model parameters, not uptake. The text gives V_a of about 0.0023 m3/kg and a saturation pressure of 44 MPa for the 1D carbons, and V_a of 0.0029 m3/kg for NCCR-11 and CMK-8, whereas Table 3 prints 0.0028 and 0.0030.
- Text on Figure 1 (p. 4545): absolute adsorption reaches a maximum at 15 bar (liquid density method) and between 20 and 25 bar (total pore volume method). These are pressures only, with no uptake values.
- Figures 13 and 14 (p. 4549): heats of adsorption against pressure, not uptake. The Summary gives a differential enthalpy of about 2 to 9 kJ/mol.
- Figures 2-8: XRD, N2 sorption isotherms with pore-size distributions, TEM and Raman. These are characterization, not H2 uptake.
- Ordered mesoporous silicas (templates; not carbon sorbents, and no H2 uptake measured). Table 1, main-5.png (p. 4547):

  | Silica | a0 (nm) | t (nm) | S_BET (m2/g) | Vp (cm3/g) | D_BJH (nm) | D_TEM (nm) |
  |---|---|---|---|---|---|---|
  | MCM-41 | 4.2 | 1.7 | 966 | 0.86 | 2.5 | 2.6 |
  | IITM-56 | 6.0 | 2.2 | 758 | 0.89 | 3.8 | 3.6 |
  | SBA-15 | 10.1 | 3.7 | 576 | 0.96 | 6.4 | 6.5 |
  | MCM-48 | 8.1 | 1.8 | 1091 | 1.03 | 2.8 | 2.7 |
  | SBA-11 | 13.7 | 3.9 | 671 | 0.69 | 1.9 | 2.1 |
  | KIT-6 | 20.0 | 3.2 | 785 | 1.07 | 6.8 | 6.7 |

## Other notes

- Vp in Table 2 (under BET, method not stated) is stored as the total pore volume with pore_volume_method = unspecified and probe gas N2. For CMK-3, the text uses V_BET = 1.08 cm3/g, whereas Table 2 prints 1.15 cm3/g.
- Nitrogen contents from elemental analysis (0.16-0.79 wt%) come from a sucrose precursor with no deliberate doping. They are recorded in notes, not as dopants.
- calibration_described = false: the paper mentions only generically "the experimentally measured dead space volume (e.g., from helium experiments)" and does not describe its own free-volume determination.
