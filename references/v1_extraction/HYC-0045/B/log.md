# HYC-0045 extraction log (agent B)

Masika and Mokaya 2013, Prog. Nat. Sci. Mater. Int. 23, 308-316. Source: page images main-1 to main-9 (no SI). 110 rows, samples S1 FA-ZTC1, S2 FA-ZTC2, S3 FA-ZTC3, S4 C5-FA-ZTC3, S5 C10-FA-ZTC3.

## Sources extracted from

- main-5 (p. 312) Table 1: FA-ZTC1/2/3 surface area (micropore area), pore volume (micropore volume), pore size (NLDFT PSD maximum), and H2 uptake (wt%) at 77 K and 20 bar. Rows M24, M49, M71. Each is merged with the 20-bar marker of the matching Fig. 7 series. The uptake density rho (umol H2 m^-2) goes in notes.
- main-6 (p. 313) Table 2: FA-ZTC3, C5-FA-ZTC3 and C10-FA-ZTC3, with the same columns. The FA-ZTC3 value (6.2 wt%, rho 9.8) is the same measurement as in Table 1, so it stays as one row (M71). Rows M89 and M110 are merged with the 20-bar markers in Fig. 8.
- main-7 (p. 314) Fig. 7, the 77 K H2 isotherms of FA-ZTC1, FA-ZTC2 and FA-ZTC3. Digitized in marker mode, archived as fig7_FA-ZTC1.json, fig7_FA-ZTC2.json and fig7_FA-ZTC3.json. Rows I1, I2 and I3.
- main-7 (p. 314) Fig. 8, the 77 K H2 isotherms of FA-ZTC3, C5-FA-ZTC3 and C10-FA-ZTC3. C5 and C10 are digitized in fig8_C5-FA-ZTC3.json and fig8_C10-FA-ZTC3.json, giving rows I4 and I5. The FA-ZTC3 series was digitized only for comparison (fig8_FA-ZTC3_comparison.json) and produced no rows; see below.
- main-7 (p. 314) Section 3.5, second paragraph, repeated in the Summary (main-8, p. 315): FA-ZTC1 "excess hydrogen uptake of 6.2 wt%" (M25) and "projected maximum total hydrogen adsorption capacity of up to 9.22 wt% (equivalent to ... 13.8 umol H2/m2)" from a Langmuir extrapolation (M26).
- main-1 Abstract and main-7 Section 3.5 text: 7.3 wt% at 20 bar and 77 K (FA-ZTC1), plus 6.6 wt% (FA-ZTC2) and 6.2 wt% (FA-ZTC3). These are the same measurements as Table 1 and appear in source_location only, with no separate rows.
- main-2 (p. 309) Sections 2.1 and 2.2, and main-3 (p. 310) Section 2.3: synthesis, compaction, BET range (P/Po 0.06-0.22), total pore volume at P/Po = 0.99, NLDFT, the Micromeritics ASAP 2020 for N2 sorption, and the Hiden IGA gravimetric analyser. The H2 section gives 99.9999% H2, degassing at 200 C and 10^-10 bar for 4-6 h, measurement at -196 C from 0 to 20 bar, buoyancy correction, a carbon density of 1.5 g/cm3 and an adsorbed-H2 density of 0.04 g/cm3.

## Digitization

- Calibration of Fig. 7 (page main-7): x uses 0 bar at px 165 (the 0 tick lies on the y-axis line) and 20 bar at px 593, checked at 10 bar on px 379. y uses 0 wt% at px 450 and 8 wt% at px 134, checked at 4 wt% on px 292. Both residuals are 0.
- Calibration of Fig. 8: x uses 0 bar at px 701 and 20 bar at px 1129, checked at 10 bar on px 915. y uses 0 wt% at px 449 and 7 wt% at px 133, checked at 3 wt% on px 314. Both residuals are within 0.5 px.
- Legends: the digitizer ran on main-7_legends_masked.png in the work directory. That file is a copy of main-7.png with the two legend boxes painted white (Fig. 7 x 482-587, y 360-425; Fig. 8 x 992-1124, y 372-437), so that the legend symbols are not picked up as markers. No other pixel was changed.
- Step-6 check: the stated 20-bar table value passes for every archive. The check was run at the last digitized pressure (19.92-19.95 bar) because the tool rejects x = 20, which lies outside the digitized range. Differences are 0.2-1.3%.
- Partial occlusion: a marker whose visible component is under 70% of its series median pixel count is marked "partly hidden" in notes and has extraction_confidence 2. This covers M7, M28-M30 and M72.
- Low-pressure overlap: below about 1.5-2 bar in both figures, consecutive markers overlap into continuous bands, and later series cover earlier ones. These markers cannot be separated or counted. Every isotherm_point_count is therefore the number of markers I could count, which is a lower bound. Specifics:
  - FA-ZTC1 (I1): only markers from 1.5 to 20 bar were extracted (24). The two components the tool rejected as too large (46 px at px 190,348 and 80 px at px 184,361) are merged triangles in the band below 1.5 bar. More triangles there are hidden under the FA-ZTC2 and FA-ZTC3 markers.
  - FA-ZTC2 (I2): 23 markers extracted. Two neighbouring markers at about 4.8 and 5.0 bar overlap and could not be separated at any opening or tolerance tried; the tool rejected them as one 69 px component at px 269,290. A 10 px fragment at px 187,363.5, inside the band, was also rejected because it is too small. The remaining markers below 1.5 bar are hidden under FA-ZTC3. The point count is 25: 23 extracted plus the 4.8/5.0 pair.
  - FA-ZTC3 (I3): 22 markers extracted. Two neighbouring markers at about 3.0 and 3.3 bar overlap and could not be separated (rejected as one 87 px component). Everything below about 1.7 bar forms one 809 px component, which was rejected. The point count is 24: 22 extracted plus the pair.
  - C5-FA-ZTC3 (I4): 18 markers from 7 to 20 bar were written as rows. The marker at the origin is in the archive at 0.021 bar and -0.007 wt%. It was not written as a row, because a negative uptake fails the schema (uptake_wt_pct >= 0). Below 7 bar the red triangles are hidden under the C10 circles, apart from small tips near 4-6 bar that the tool does not resolve. The point count is 19: 18 plus the origin marker.
  - C10-FA-ZTC3 (I5): this run used ROI x 702-1138, y 134-448 so that the black axes are excluded. 21 markers were extracted. The tool rejected four components: two merged pairs at about 1.3/1.5 bar (77 px) and 3.0/3.3 bar (74 px), the low-pressure band (626 px), and a 12 px fragment at the origin that the ROI edge cuts. The point count is 25: 21 extracted plus the two pairs.
- Anomalous points near 0 bar: Fig. 7 shows a FA-ZTC2 marker at 0.004 bar and 1.98 wt% (M27) and a FA-ZTC3 marker at 0.023 bar and 1.44 wt% (M50). Each is joined to the near-origin points by a vertical line. They are plotted markers, so I kept them as rows with confidence 2 and a flag. Whether each is the first or the last point of its run is unknown.
- Branches: each figure plots one series per sample. The paper says "the isotherms show no hysteresis" but does not say whether desorption points are plotted, and none can be told apart. All points are coded adsorption.
- FA-ZTC3 in Fig. 8: I treat this as a replot of the Fig. 7 run (I3), not a second run. Both figures show the same pressure set (2.0, 2.5, 3.0, 3.3, then 12-19 in steps of 1, 19.5 and 20 bar), and the values agree within 0.04 wt%. The Fig. 8 values are lower because the C5 triangles cover the tops of the diamonds. Table 2 also repeats the Table 1 value. Rows come from Fig. 7, where the blue series is drawn on top. The Fig. 8 archive also holds occluded fragments below 3.4 bar that are not used. In it the 3.0/3.3 pair is separated, but both markers are partly covered, so I did not use them to fill the gap in Fig. 7. As a consequence, replicates_reported = false for FA-ZTC3.

## Coding decisions

- Basis:
  - The paper never defines its basis. The Summary calls the uptakes "total" ("total hydrogen uptake capacity of up to 7.3 wt% at 20 bar and 77 K"), and that sentence refers to all the templated carbons. I therefore set uptake_type = total on all isotherm rows and on the 9.22 wt% row.
  - basis_stated = false, because "total" is not defined. basis_inferred = excess, which is the §3 default for a gravimetric value with a stated buoyancy correction.
  - The paper treats these values as more than excess: it reports a separate "excess" 6.2 wt% for FA-ZTC1, and its buoyancy calculation uses an adsorbed-H2 density of 0.04 g/cm3. C should review this.
  - The excess 6.2 wt% row (M25) is reported next to the total, so basis_stated = true. It has no pressure (pressure_unstated = true), value_kind = unclear and no isotherm_id. It equals the tabulated FA-ZTC3 value.
- The 9.22 wt% row (M26) is a Langmuir capacity: value_kind = fitted_extrapolated, pressure_unstated = true, isotherm I1, because the paper says it is fitted to the FA-ZTC1 77 K adsorption data. "Up to" is kept as exact (uptake_bound = exact).
- Hydrogen uptake density rho (umol H2 per m2 of surface area): 11.0, 10.6 and 9.8 in Table 1; 9.8, 9.9 and 10.6 in Table 2; 13.8 for the 9.22 wt% projection. These are recorded in notes. They are uptake per specific surface area, not a film areal uptake, so areal_uptake_g_cm2 is left empty.
- Pore size: the pore size of C5 and C10 is printed as "0.6/1.2" nm (two PSD maxima). average_pore_diameter_nm is left empty and the printed value is in notes. FA-ZTC1/2/3 are 1.2 nm, coded as DFT (NLDFT PSD maxima).
- skeletal_density_g_cm3 = 1.5 is the carbon density assumed in the buoyancy correction, not a measurement.
- Degas duration "4-6 h" is a range, so degas_duration_h is left empty. degas_end_pressure_pa = 1e-05, converted from 10^-10 bar.
- instrument_identified = true (Hiden IGA). calibration_described = true (buoyancy correction stated). free_volume_calibration is empty because no gas or temperature is given.
- measuring_lab_id: Mokaya, the corresponding author marked *, School of Chemistry, University of Nottingham.

## Values seen but not extracted

- Z13X (zeolite 13X template; not a carbon sorbent): Table 1 gives surface area 658 m2/g (micropore 646), pore volume 0.33 cm3/g (micropore 0.31), pore size 1.0 nm, and no H2 uptake ("-"). Figs. 1, 2 and 3 show its XRD, TGA (about 10% water loss at 180-350 C) and N2 isotherm and PSD.
- FA-ZTC1-co (zeolite/carbon composite before etching): XRD and TGA only. The carbon content is about 28%. There is no H2 value.
- FA-ZTC1 TGA: residual weight below 2% at 620 C. This is characterization, not uptake, and it is not a metal, so no residual_metal field was used.
- XRD d-spacing of about 1.4 nm at 2theta = 6.3 deg (zeolite-like ordering) is not an interlayer spacing, so it is not recorded.
- Fig. 3 and Fig. 6 (N2 sorption isotherms and NLDFT PSDs) and Fig. 4 (TEM): not H2.
- Fig. 9 (H2 uptake against BET area, with the Chahine-rule line) is not an isotherm and was not digitized. It plots the five samples whose values are in Tables 1-2. The FA-ZTC3 square sits visibly below the other 6.x wt% points and was not checked numerically.
- Text ranges and rules that are not measurements of one sample: "hydrogen uptake density of between 10 and 11 umol H2/m^-2" (range across samples); the Chahine rule of 1 wt% per 500 m2/g (= 10 umol H2/m2); "micropore surface area ... up to 88%", "micropore volume ... up to 75%" and "74%"; "constant proportion of microporosity ... 87%".
- Values from other papers, cited for comparison and not measured here:
  - 6.9 wt% at 20 bar and 77 K for a zeolite beta/EMC-2 templated carbon [6]
  - 7.08 wt% at 20 bar and 77 K for a doubly activated carbon [7]
  - 7.03 wt% for polypyrrole-based activated carbon [8]
  - MOF-5 destroyed at 180 MPa and ZIFs stable to 340 MPa [37]
  - activated carbons stable to 420 MPa [37]
  - pores > 1.5 nm contributing little at 77 K up to 60 bar [55]
- DOE target of 5 wt% (40 g/L) below 100 bar (Introduction): a target, not a measurement.
