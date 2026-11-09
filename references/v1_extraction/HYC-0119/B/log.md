# HYC-0119 extraction log (agent B)

Inputs: pages main-1.png to main-5.png (no SI). 86 rows written. Samples: S1 CS850-4.5, S2 CS800-4, S3 Max3, S4 AC-1 (S3 and S4 are ref. 8 comparison data).

## Sources extracted from

- main-1.png, Abstract: 4.5 wt% (77 K, 50 bar) for CS850-4.5 (row M37); 25.9 g/L (77 K, 30 bar) for CS800-4 (on row M55).
- main-2.png, Sec. 2.1 to 2.3: synthesis, KOH activation, characterization (N2 isotherms on an ASAP 2460, BET; DFT and HK pore sizes), H2 method (BSD-VVS&DVS gravimetric analyzer, degassed 200 °C for 3 h, 77 K, 0 to 50 bar, 1 h equilibrium per point, excess isotherms fitted with a Langmuir model), skeletal density (BSD-TD). Coded on every row of S1 and S2.
- main-2.png, Table 1: textural properties of CS800-4 and CS850-4.5, coded on their rows.
- main-3.png, Sec. 3.2 and 3.3 text: XPS surface O contents (CS850-4.5 20.47 wt%, CS800-4 14.60 wt%), FTIR and XPS functional groups, EDS N, O and residual Fe, HK ultramicropore sizes. Coded on S1 and S2 rows or in their notes.
- main-4.png, Fig. 4a (77 K gravimetric isotherms, total and excess, 0 to 30 bar): 4 series digitized, 17 markers each (rows M1 to M34, M38 to M72).
- main-4.png, Fig. 4b (volumetric isotherms, g/L): CS850-4.5 and CS800-4 values put on the matching Fig. 4a total rows; one CS800-4 point with no visible Fig. 4a marker has its own row (M41); Max3 (M74 to M80) and AC-1 (M81 to M86) digitized as ref. 8 data.
- main-4.png, Table 2: 1 bar and 30 bar wt%, 30 bar g/L, pore size, rho_s (rows M17, M35, M55, M73).
- main-4.png, Sec. 3.4 text: 30-bar totals 3.3 and 4.3 wt% (same as Table 2); CS800-4 1.5 wt% at 1 bar (same as Table 2, M73); CS850-4.5 2.3 wt% at 1 bar (M36); CS850-4.5 4.5 wt% at 50 bar (M37).
- main-5.png, text and Conclusions: packing densities 0.79 and 0.54 g/cm3 and the formulas; 25.9 and 23.6 g/L; 4.5 wt% at 77 K and 50 bar. These repeat values already in rows.

## Coding decisions

- Total vs excess: Fig. 4a plots "total" and "excess" for each sample from the same run. They have separate isotherm_ids because basis fields must be uniform within an isotherm. Excess: basis_stated = true (two bases side by side, plus the V_excess model in Sec. 2.3). Total: basis_stated = false, because §3 says an undefined "total" is false. That makes basis_inferred the gravimetric default, unknown, since no buoyancy correction is stated. A reconciler may read the side-by-side clause as also covering "total".
- Table 2 30-bar values (4.3 and 3.3 wt%) are named "total" in the text. Their printed pressure (30 bar) is within 0.6 bar of the last Fig. 4a total marker. That marker is clipped by the right axis frame and digitizes to 29.76 bar. Each pair was merged into one table_direct row in the total isotherm.
- Table 2 1-bar values (1.9 and 1.5 wt%) do not name a basis. The nearest Fig. 4a markers are at 1.09 and 0.95 bar, outside the 0.02 bar window, so these rows have no isotherm_id.
- CS850-4.5 2.3 wt% at 1 bar (text) conflicts with Table 2 (1.9 wt%) and with Fig. 4a (about 1.85 wt% at 1 bar). It is recorded as printed in its own row.
- 4.5 wt% at 50 bar is beyond the plotted range. No basis is named, so it has no isotherm_id and uptake_type unspecified. Context suggests total.
- Fig. 4a right axis (cm3(STP)/g) has ticks every 41.0 px per 100 cm3/g, and the left axis has 54.7 px per wt%. That puts 100 cm3/g at 0.75 wt%, against 0.899 (W1) or 0.891 (W2). This is a unit-consistency failure between the two axes. All values were read on the wt% axis, which matches the paper's printed wt% values (checks below). No cm3/g value was stored, because no per-point value is printed in that unit. wt_pct_convention = unknown/none throughout.
- Fig. 4b values equal Fig. 4a total wt% × packing density at every matched pressure: 4b/4a ratio 5.36 to 5.44 for CS850-4.5 (rho_p 0.54) and 7.90 to 8.0 for CS800-4 (rho_p 0.79). They were stored as volumetric_capacity_kg_m3 (g/L = kg/m3), basis packing_volume, on the total rows. includes_compressed_gas = false (conservative, since "total" is undefined).
- CS800-4 has 18 points: Fig. 4b shows a CS800-4 marker at 0.32 bar, 7.84 g/L (about 0.99 wt%). Its Fig. 4a counterpart is hidden under the CS850-4.5 marker at 0.31 bar, 1.0 wt%, and could not be digitized from Fig. 4a. It gets a volumetric-only row (M41, isotherm I3). isotherm_point_count = 18 for I3 and I4.
- material_class doped_carbon: the paper says N and O are "uniformly doped in the carbon shell" (EDS, CS850-4.5). XPS O wt% is stored in dopant_concentration_wt_pct (method XPS). Residual Fe is recorded for CS850-4.5, where EDS shows it, and was not quantified.
- synthesis_method = carbonization (hydrothermal carbonization, then 800 °C carbonization; Fe2O3 is removed by HCl to leave hollow spheres). instrument_identified = true: "BSD-VVS&DVS" is the manufacturer prefix plus model. calibration_described = false. measuring_lab_id: corresponding author Zhu (*), first affiliation Tongji University.
- pore_volume_probe_gas = N2: Sec. 2.2 names only N2 sorption for the textural analysis. pore_volume_method and pore_diameter_method are unspecified. Table 1 prints pore volumes in "m3/g", read as cm3/g.
- Ref. 8 data (Max3, AC-1): the Fig. 4 caption cites ref. 8 and calls them "commercially available". synthesis commercial; surface_area_method not_reported; method and basis unknown. temperature_unstated = true, because no temperature is stated for these data. All visible markers were digitized because the figure presents them with the 77 K isotherms.

## Figure digitization (scripts/digitize_figure.py, mode markers)

- Fig. 4a calibration: x 0 bar at px 162.5, 30 bar at 500.8, check 15 bar at 331.46 (error 0.11%). y 0 wt% at px 1087.5, 5 wt% at 814.0, check 3 wt% at 923.5 (error 0.06%). Tick pixels came from pixel rows and columns of the tick marks.
- Fig. 4b calibration: x 0 at 162.5, 30 at 500.5, check 15 at 331.5. y 0 g/L at 1417.5, 30 at 1144.5, check 15 at 1281.5.
- Preprocessing, all in the work directory: legends were masked to white. For open markers, the enclosed ring holes (8 px or smaller) were filled with the series colour so the tool's opening keeps them. Each series was run on an image keeping only rectangular windows around its marker positions. Positions came from pixel inspection and from cores of the colour mask eroded with a disk. Lines and other series' markers are separated this way.
- Marker counts (counted on the plot, then extracted): CS850-4.5 total 17/17, excess 17/17; CS800-4 total 17/17 visible (18 in the run), excess 17/17 visible (18). Fig. 4b: CS850-4.5 17/17; CS800-4 14 of 18; Max3 7/7; AC-1 6/6 visible.
- At low pressure the total and excess markers coincide (CS850-4.5 up to 1.09 bar, 6 markers; CS800-4 up to 3.0 bar, 8 markers). The same marker was digitized for both series. The lowest CS800-4 markers (0.17 to 0.23 bar) lie within 2 px of the y axis and are partly behind it.
- Last markers at 30 bar are clipped by the right axis frame. Their centroids come from the visible part (x about 29.6 to 29.9 bar).
- Not separated, recorded here:
  - Fig. 4a: one CS800-4 marker (total and excess) is hidden under the CS850-4.5 marker at 0.31 bar, 1.0 wt%.
  - Fig. 4b CS800-4: the three lowest-pressure markers are fragments of 3 to 10 px under the AC-1, Max3 and MOF-5 lines (expected near 1.9, 3.3 and 4.2 g/L). The clipped 30-bar marker is also a fragment; Table 2 gives 25.9 g/L.
  - Fig. 4b AC-1: a marker near 1 bar may be hidden under the CS850-4.5 marker. It was not counted. The AC-1 3-bar marker is mostly covered by the CS850-4.5 line (4 px, confidence 2).
- Checks (digitize_figure.py check, 5%): Fig. 4a CS850-4.5 total at 29.76 bar vs 4.3 wt% PASS (0.97%); CS800-4 total at 29.76 vs 3.3 PASS (0.96%); Fig. 4b CS850-4.5 at 29.82 vs 23.6 g/L PASS (0.12%). Fig. 4a CS850-4.5 excess at 1 bar vs Table 2 1.9 PASS (2.5%) and CS800-4 excess at 1 bar vs 1.5 PASS (3.3%). The total and excess markers coincide there, and the Table 2 1-bar values name no basis. No stated value lies in the range of Fig. 4b CS800-4, Max3 or AC-1, so those archives are "unchecked".
- Archives: out/digitizations/fig4a_CS850-4.5_total.json, fig4a_CS850-4.5_excess.json, fig4a_CS800-4_total.json, fig4a_CS800-4_excess.json, fig4b_CS850-4.5.json, fig4b_CS800-4.json, fig4b_Max3.json, fig4b_AC-1.json.

## Values seen but not extracted

- MOF-5 volumetric isotherm, Fig. 4b (purple): not a carbon sorbent (ref. 8 comparison).
- Samples with characterization but no H2 uptake (Table 1, SBET m2/g, Smicro m2/g, Vtotal, Vmicro "m3/g", Dave nm):
  - CS800-2: 960, 323, 0.78, 0.2, 3.27.
  - CS800-3: 1244, 379, 1.06, 0.18, 3.43.
  - CS800-4.5: 1688, 622, 1.78, 0.56, 4.22; also XPS O 17.54 wt%, Raman I_D/I_G 1.0, HK ultramicropore 0.37 nm.
  - CS800-5: 1650, 341, 1.55, 0.39, 3.75; HK 0.37 nm.
  - CS900-4.5: 1981, 716, 1.45, 0.38, 2.93; HK 0.48 nm.
- Intermediates CFe-HTC and CS: no data.
- U.S. DOE 2020 target 4.5 wt% (Sec. 3.4): a target, not a measurement.
- Non-isotherm figures with no H2 values: Fig. 1 (SEM, TEM, EDS), Fig. 2 (Raman, XRD, FTIR, XPS), Fig. 3 (N2 isotherms and DFT/HK pore size distributions).
- Raman I_D/I_G (1.05 for CS850-4.5 and CS800-4), XRD peaks at 24° and 44°, XPS binding energies, and sphere diameter and shell thickness from TEM: these quantities have no schema field.
- Conclusions BET "2140 m2/g" for CS850-4.5: duplicates Table 1 (2142), which was used; noted on the rows.
- "Optimal operating pressure is 25 bar" and "excess adsorption ... began to decline beyond 25 bar": qualitative, no value.
