# HYC-0024 extraction log (agent B)

## Sources extracted from
- main-1 (p. 10930), abstract: "hydrogen storage values at 10 MPa close to 1 wt %" for the anthracite-derived activated carbon (KUA1) -> M2 (uptake_bound approximate), merged with the Fig. 1 KUA1 10 MPa marker (archive fig1_KUA1_10MPa.json).
- main-4 (p. 10933), Conclusions: same "close to 1 wt % at 10 MPa" statement, attributed to "an activated carbon obtained from an anthracite" = KUA1 -> M2 (one row).
- main-1/main-2 Experimental Section: method (mixed gravimetric and volumetric, cell at 293 K, balance 1 mg), degas (10^-10 MPa, 673 K, 48 h), free-volume correction (He density + cell volume), error bars and 5% agreement with a second system, packing-density method; coded on every row.
- main-2 Table 1: hydrogen adsorbed density at 10 MPa for 8 samples -> M3, M9, M12, M15, M17, M19, M21, M25; Ms at 10 MPa for 5 samples -> M5, M10, M13, M22, M26; BET area, DR N2 and CO2 micropore volumes, mean pore size, packing and helium densities on every row of each sample.
- main-2 Fig. 1 (293 K isotherms, mmol H2/g C): highest-pressure (about 70 MPa) marker of each of the 8 isotherms digitized -> M1, M8, M11, M14, M16, M18, M20, M24 (archives fig1_<label>.json); KUA1 10 MPa marker digitized for the M2 merge only.
- main-4 (p. 10933) text, Section 3.2: KUA1 Ms 6.9 kg/m3 at 5 MPa, 11.8 at 10 MPa, 15.3 at 15 MPa, 19 at 20 MPa -> M4, M5 (same as Table 1 value), M6, M7.
- main-4 Fig. 4 (Ms vs pressure): high-pressure end of the ACFC26 and CF solid lines digitized -> M23, M27 (archives fig4_ACFC26.json, fig4_CF.json); CF line near 10 MPa digitized only as a calibration check against Table 1 Ms 6.3 kg/m3 (fig4_CF_calibration_check_10MPa.json, tool check passed, 0.6%).

## Values seen but not extracted
- Fig. 1: the 5, 10, 20, 30, 40, 50 and 60 MPa points of all 8 isotherms (293 K: only the highest-pressure point is extracted); the KUA1 10 MPa point appears only in the notes of M2.
- Fig. 1: the ACFC50 and A20 error-bar markers overlap at 70 MPa and could not be separated by colour, tolerance or region; the centroid of the combined double marker is recorded for both (M8, M11, confidence 2). The two series also coincide at 50 and 60 MPa; KUA1, ACFC50, A20 and AX21 markers overlap at 5 and 10 MPa. Point count 8 per isotherm (5-70 MPa) assumes coincident markers; the blob at the origin where all lines start is not counted.
- Fig. 1 archives keep tool status "unchecked": the paper prints no mmol/g value to check against. Consistency only: KUA1 10 MPa digitized 4.16 mmol/g divided by the N2 DR volume 0.51 cm3/g gives 16.4 kg/m3 against Table 1 16.34.
- Fig. 2 (not an isotherm: wt% vs micropore volume): wt% at 10 MPa and at 70 MPa for each of the 8 samples (16 points) and two straight lines; not given in tables or text except the approximate KUA1 10 MPa value (M2).
- Fig. 3 (not an isotherm: adsorbed H2 density vs mean pore size): 10 MPa densities (same as Table 1) and 70 MPa densities for the 8 samples, which no table or text gives; theoretical curve at 300 K and 10 MPa from ref. 26 (not a measurement of this paper).
- Fig. 4: the KUA1, A20 and ACFC50 Ms lines merge with each other and with the compressed-hydrogen dashed line at their 70 MPa ends and could not be separated; no rows for those three ends.
- Fig. 4: compressed-hydrogen line (not a sorbent); dotted Ms/hydrogen-density ratio curves on the right axis for KUA1, A20, ACFC50, ACFC26 and CF (a ratio, not an uptake).
- Text p. 10933: compression pressures 9, 15, 22 and 27 MPa for the same stored amounts (compressed gas, not a sorbent); 5 kg H2 occupying 227 L at 34.5 MPa and 340 L at 20 MPa (compressed gas, ref. 40); KUA1 tank volumes 185 L at 34.5 MPa and 263 L at 20 MPa for 5 kg H2 (tank volumes, not printed as an uptake; converting them would be this extraction's arithmetic); 250 L tank at 20 MPa (general statement).
- Text p. 10931: Pd calibration standard of the second (gravimetric) system, H/Pd = 0.72 +/- 0.03 at 293 K and 0.1 MPa, literature 0.73 (metal, not a carbon sorbent).
- Introduction: 60 wt% for graphite nanofibers (ref. 24), 5-10 wt% for nanotubes (ref. 25), DOE 6.5 wt% target, theoretical optimum pore sizes (refs. 19, 26): other work, not measured here.
- Not stated: H2 sample mass (the 5 g Pd and the 0.5-0.2 g packing pellets are not H2 sample masses), H2 purity, BET P/P0 range, instrument manufacturer/model.

## Coding decisions
- Samples numbered by first appearance (Fig. 1 labels, top to bottom): S1 KUA1, S2 ACFC50, S3 A20, S4 AX21, S5 fabric ("commercial fabric" in Fig. 1), S6 AC35, S7 ACFC26, S8 CF; labels as printed in Table 1.
- The table/text-merge rule was applied only to gravimetric values (the quantity plotted in Fig. 1). Table 1 densities and Ms values and the text Ms values are separate quantities on their own rows without isotherm_id: the paper says only that they come from "experiments such as those compiled in Figure 1".
- Ms rows: basis_stated true, basis total (the paper names and defines "total volumetric storage capacity ... includes both the hydrogen adsorbed and the hydrogen compressed"), volumetric_capacity_basis tank_volume, includes compressed gas. They are not put on the gravimetric rows of the same point (Fig. 1 70 MPa for ACFC26 and CF; M2 for KUA1 at 10 MPa) because a row carries one basis, one bound and one value kind; the Fig. 4 curves get their own isotherm_ids (I9, I10).
- measurement_method other ("a mixed gravimetric and volumetric method"), so basis_inferred unknown for the adsorbed amounts; calibration_described true (free volume from He density and cell volume); instrument_identified false; replicates_reported true (error bars on every isotherm point; 5% agreement with a second system).
- BET probe gas coded N2: porous texture by N2 (77 K) and CO2 (273 K); CF has BET 0 and N2 DR volume 0 because its pores are not accessible to N2 at 77 K.
- KUA1 Ms at 15 MPa (M6) value_kind unclear: Fig. 1 has no measured point at 15 MPa.
- Figure calibration: Fig. 1 on the frame lines (x 0 and 80 MPa, y 0 and 12 mmol/g), checked on the 40 MPa and 6 mmol/g ticks; Fig. 4 on the frame lines (x 0 and 80 MPa, y 0 and 0.045 g/cc), checked on the 40 MPa and 0.025 g/cc ticks. The page image is very slightly rotated (Fig. 1 frame about 0.7 px lower at the left than at the right), which shifts the 70 MPa values by under 0.03 mmol/g.
