# HYC-0047 extraction log (extractor B)

Paper: Fierro et al. 2010, Carbon 48:1902-1911. Input: 10 page images (main article; no supplementary file). Rows written: 139 (M1-M139). Extraction date 2026-10-27.

## Sources extracted from

- Table 1, p. 1906: rho_He, S_BET, V0.99, V_DR,N2, L0 and V_DR,CO2 for the 9 ACs. Attached to every uptake row of S1-S9 (no characterization-only rows needed).
- Sections 2.1-2.3, pp. 1903-1905: synthesis, N2/CO2 characterization and the three H2 devices (IJL volumetric at 298 K; ICMPE Sieverts at 77/298 K; ICB-CSIC VTI gravimetric at 77 K). Used for the method, lab, degassing, purity, sample mass, calibration and instrument fields.
- Table 2, p. 1908: 32 printed uptake values (4 columns x 9 samples, minus 4 n.d. cells), M1-M32. Three of them are the same measurement as a Fig. 5 marker and carry the marker's pressure (see "Merge rule").
- Section 4 (Conclusions), p. 1909: "A maximum H2 excess uptake of 1.1 wt.% for ACs was found at 298 K and 20 MPa", M33. The sample is not named, so it is coded `(unlabelled)` (S10) and attributed to the IJL device, the only one operated to 20 MPa.
- Fig. 5a, p. 1907 (77 K, ICB gravimetric): 7 series digitized, 41 markers. 39 are written as digitized rows and 2 as merged table rows. Isotherms I1-I7.
- Fig. 5b, p. 1907 (77 K, ICMPE volumetric): 8 series digitized, 67 markers. 66 are written as digitized rows and 1 as a merged table row. Isotherms I8-I15.
- Fig. 5b, "M2849 at 298K": only the highest-pressure marker was digitized (9.70 MPa, 0.904 wt%), M139, isotherm I16.

## Digitization method (Fig. 5)

- Calibration on labelled ticks found by pixel scans of the page image (page 6, 1241 x 1654 px).
  - Fig. 5a: x 0 and 10 MPa at px 717 and 1112, check tick 4 MPa at px 875. y 0 and 7 wt% at px 762 and 556, check tick 3 at px 674.
  - Fig. 5b: x 0 and 10 MPa at px 717 and 1118 (the 10 tick is the right frame line), check tick 4 MPa at px 877 (0.25% residual). y 0 and 7 wt% at px 1056 and 843, check tick 4 at px 934 (0.23% residual).
- Every series is drawn in the same black (#111212). The four samples differ only by marker shape. Adsorption markers are filled and desorption markers are open, so series are separated by marker type and by region:
  - Filled markers: colour #111212, tolerance 80, 3-px opening (this removes the 1-2 px curve lines), size window 18-40 px (40-60 px for squares).
  - Open markers: the centroid of the marker's white interior (colour #ffffff, tolerance 30; 280 for open squares, so that grey curve-line pixels crossing the interior are included), with no opening and a size window of 3-30 px. A curve line or a neighbouring marker can truncate an interior, which biases the centroid by up to about 1 px. Rows with small or partly covered interiors have reduced confidence.
- The tool takes one rectangular region per run. Where a series' markers interleave with another series' markers of the same fill type, the series was digitized in several runs, each with its own archive (suffixes _a, _b, ...). In every run, the number of extracted markers equals the number of that series' markers in the region. Pixel groups that the size window rejected (merged markers, background pieces, other-series fragments) are listed under `rejected_markers` in each archive.
- 44 archives in `digitizations/` (status `unchecked`). The tool's legacy `check` subcommand was not run, because the protocol §9 procedure does not include it and the Table 2 values may come from the second measured cycle (ICMPE measured each PCI curve twice).
- Pressures are stored as MPa x 10 bar. `digitization_uncertainty_wt_pct` is left empty.

## Merge rule applied (table value = plotted point)

A Table 2 value was treated as the same measurement as a Fig. 5 marker when both conditions held:

- the marker is that sample's marker nearest the printed 4 MPa and lies within 0.25 MPa of it;
- the digitized uptake equals the table value within 0.07 wt% (1% of the y span).

Merged rows:

- M1149 ICB: 3.2 at 38.48 bar. The Fig. 5a marker reads 3.160 wt%.
- M2029 ICB: 4.9 at 40.63 bar. The Fig. 5a marker reads 4.854 wt%.
- M2849 ICMPE: 5.9 at 38.78 bar. The Fig. 5b marker reads 5.948 wt%.

The digitized points for these three markers were not kept.

Not merged, so each table value is kept at the printed 4 MPa as a single value:

- M1149, M2029 and T3220 ICMPE: no Fig. 5b marker lies within 0.25 MPa of 4 MPa. For the reconciler:
  - The Fig. 5b M1149 curve is about 3.0 wt% at 4 MPa (digitized 2.958 at 3.14 MPa), against the 3.2 in Table 2.
  - The M2029 curve is about 4.7 wt%, against the 4.8 in Table 2.
- M2849 and T3220 ICB: their Fig. 5a markers near 3.9 MPa merge into one pixel group, so neither could be digitized.

## Values seen but not extracted

- Table 2, 4 n.d. cells: T2275 and T2502 (ICB, 77 K); T3073 and T3220 (ICMPE, 298 K). These were not determined.
- Fig. 5a and 5b origin markers (0 MPa, 0 wt%): every series overlaps there and the marker sits on the axes. This is the evacuated start state, so it was not extracted and is not counted in `isotherm_point_count`.
- Fig. 5a markers that could not be separated (counted in the isotherm totals, recorded in row notes):
  - M1149 adsorption: 2 markers at about 0.3-0.4 MPa form one merged group.
  - M2029 adsorption: 1 marker at about 0.12 MPa, merged with an M2849 diamond.
  - M2849 adsorption: 6 markers. The one at about 0.12 MPa merges with M2029. Those at about 0.4 and 0.67 MPa are partly hidden by T3220 open circles. Those at about 3.86, 5.15 and 7.8 MPa each merge with a T3220 filled circle.
  - T3220 adsorption: no separable marker. The three visible markers (about 3.86, 5.27 and 7.95 MPa) merge with M2849 diamonds, and the low-pressure ones are hidden. Nothing was extracted, so this isotherm has no ID.
  - A partial filled fragment at about 0.2 MPa, 3.6 wt% lies under a T3220 open circle. Its series could not be identified.
- Fig. 5b markers that could not be separated:
  - M1149 adsorption: a marker at about 4.75 MPa is partly covered by the open marker at 4.85 MPa, and a near-axis marker sits at about 0.05 MPa, 1.6 wt%.
  - M2849 adsorption: two near-axis diamonds (about 0.74 and 1.9 wt%) merge with the y axis and the steep curve lines, and markers at about 0.14 and 0.35 MPa merge with other markers.
  - Possibly hidden: further M2029, M2849 and T3220 markers below 0.5 MPa, and one covered M1149 open square near 0.1 MPa, 2.2 wt%. Counts state this.
- Fig. 5b, M2849 at 298 K: every point except the highest-pressure one, per protocol §9 (non-77 K isotherm). Its about 30 small markers cannot be counted reliably, so `isotherm_point_count` is empty.
- Fig. 4a (298 K, M1149 and empty vessel): total H2 stored in mol H2 per vessel. This is a system-level total (adsorbed plus compressed gas) with no per-gram or schema field, and converting it would need the approximate vessel volume or bed mass. Not extracted, including its 20 MPa end point.
- Fig. 4b, Fig. 5c and the text "% gain" values: 33.6% at 1.1 MPa (M1149), 38.0% at 1.5 MPa (M2029), 31.3% at 2.6 MPa (M2849), 14% at 20 MPa (M2029), 3700% near 0.15 MPa, 1.3% near 9 MPa, and the "less than 3%" agreement with water-column release. These are gains relative to the empty vessel, not uptakes.
- Fig. 6a and 6b: 77 K, 4 MPa uptakes plotted against S_BET and V_DR,N2. These are the same values as Table 2 (ICMPE and ICB columns), so they were not re-extracted. Also not extracted: the 6.4% extrapolation line and R^2 = 0.97.
- Fig. 7: literature data (Xu [41], Kabbour [42], Panella [25], Jordá-Beneyto [27], including AX-21) are other papers' measurements. "This work" points duplicate Table 2.
- Abstract and conclusions:
  - The 6.4 wt% upper limit is an extrapolation of the uptake-S_BET fit to 2630 m2/g, not a measurement on a sample.
  - The 6.8 wt% figure is a theoretical limit.
  - These duplicate Table 2: "6.0 wt.% at 77 K and 4 MPa" (M2849, ICB), "0.6 wt.% at 298 K and 5 MPa", "5.9-6.0 wt.% in ACs having S_BET = 2451" (T2451 ICMPE 5.9 / M2849 ICB 6.0), and "Excess hydrogen storage values of 6 wt.%".
- p. 1908 text ranges "0.4 to 0.6 wt.%" (298 K, 5 MPa) and "2.9 to 6.0 wt.%" (77 K, 4 MPa): ranges over the Table 2 values.
- p. 1908 theoretical graphene values: 1315 and 2630 m2/g, 1.3e-5 mol H2/m2, 0.034 mol H2/gC, 68 mg H2/gC and 6.8 wt%. These are theory, not measurements.
- Introduction literature values: 23.76 wt% (80 MPa) [17], 11.7 wt% [18], 3.5 wt% [19], and AX-21 at about 6 wt% (77 K, 5 MPa) / 5 wt% (2 MPa) [28], 3 wt% (80 K, 10 MPa) [23], 1 wt% (RT, 5 MPa) [28] and 1.6 wt% (70 MPa) [29]. Also the DOE targets of 6.5 wt% and 62 kg/m3. These are other papers or targets. AX-21 was not measured in this paper.
- p. 1909 slopes 1.74e-3 to 2.87e-3 wt% g/m2 and plateau 5.4 [27] to 6 wt%: literature or derived values.
- Figs. 1-3: N2 and CO2 isotherms and DFT pore-size distributions. This is characterization only.
- Non-carbon materials: none measured. There are no calibration standards, MOFs or zeolites.

## Coding decisions

- Basis: Table 2 and the text call the values "excess" without defining excess. "Total" storage is defined, but only for the per-vessel IJL quantity. So `basis_stated = false`, `basis_inferred = excess` (named) and `uptake_type = excess`.
- wt% convention: coded W1, `stated`, from the Table 2 caption "expressed as weight% of the outgassed activated carbons". The ICMPE section adds "All capacities reported here refer to the sample dry mass". The paper's own 68 mg/g = 6.8 wt% arithmetic is consistent with W1.
- Fig. 5b 298 K curve: the caption gives the ICMPE volumetric device, but the text (p. 1907) says "gravimetric device". The ICB device is described only at 77 K up to 8 MPa, and this curve reaches about 9.7 MPa. So the lab is coded from the caption (ICMPE), `measurement_method = unknown`, and device-specific conditions are left empty.
- Labs: IJL is named after the corresponding author (Fierro). ICMPE is named after the senior-listed ICMPE author (Latroche), because the group leader is not stated. ICB-CSIC is named after its only author (Izquierdo).
- `instrument_identified`:
  - IJL: true (laboratory-made device, described).
  - ICMPE: false (no manufacturer or model, and not stated to be home-built).
  - ICB: false (VTI Corporation named, but no model).
- `calibration_described`:
  - ICMPE: true (He-pycnometry sample-volume correction).
  - ICB: true (buoyancy correction).
  - IJL: false (correction for gas outside the vessel, but no free-volume determination described).
- `replicates_reported`:
  - true for Table 2 values (printed +/- 0.1) and for ICMPE figure points (PCI curves measured twice).
  - false for ICB figure points, the 1.1 wt% text value and the 298 K curve.
- `area_same_sample = yes`: the same sieved AC batches were characterized and measured for H2. BET range and consistency criteria are not stated. The Log(P0/P)^2 ranges in Table 1 are DR fit ranges and are recorded in notes.
- V_DR,CO2 is described as reflecting pores narrower than 0.7 nm. It is stored in `micropore_volume_co2_cm3_g`, not in `ultramicropore_volume_cm3_g`, because it exceeds V_DR,N2 for M1149.
- Separate isotherm IDs are used for the adsorption and desorption branches. The paper speaks of "adsorption and desorption isotherms", and full and open symbols mark them.
