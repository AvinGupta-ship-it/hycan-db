# HYC-0071 extraction log (extractor A)

Rows: 47 (1 table row + 22 filled-symbol and 24 open-symbol digitized points, all one isotherm I1 of one sample S1).

## Scope decision

- Only one sample in this paper is a carbon sorbent (protocol section 3): the commercial activated carbon WS-480 (Chemviron carbon), printed label "Activated carbon" (Table I), "Activated Carbon" (Figure 6 legend). It is sample HYC-0071-S1.
- MIL-101 is a Cr terephthalate MOF. The AC@MIL-101/A to /D composites contain 0.63, 1.25, 1.87 and 2.5 wt% carbon (main p. 748, section 2.4), so their majority component is the MOF and they are not carbon sorbents under section 3. Not extracted. Reconciler may want to review this call because the titles call them "activated carbon composites".

## Extracted from

- Main text, Table I (p. 750), row "Activated carbon": BET 946.96 m2 g-1, pore volume 0.48 cm3 g-1, pore width 0.90 nm, H2 uptake 3.7 wt%, 414.4 cc g-1. Row M1 (table_direct). The same 3.7 wt% is repeated in the text on p. 751 (Results, "are 3.7, 10.1, 8.4, 7.2, and 6.1 wt%, respectively"); one row only.
- Main text, Figure 6 (p. 751), Activated Carbon series (down-pointing triangles), 77.4 K: filled symbols (23 resolved, 22 rows plus the point merged into M1) and open symbols (24 resolved, 24 rows). Rows M2 to M47.
- Main text, section 2.1 (supplier, WS-480, gas purity 99.999 %), section 2.5 (instrument BELSORP-HP, BEL Japan, Inc; degas 393 K, 10 h, 6.7 x 10-2 Pa; N2 BET with ASAP 2020, BJH desorption pore width, single-point adsorption pore volume; uptake error within +/-0.5 %) used for the sample and method columns.

## Decisions that need a second look

- Table I value vs Figure 6: the paper prints no pressure for the value, only "up to 6000 kPa" for the isotherm range (Table I caption, Figure 6 caption, section 3). The last (highest-pressure) filled marker of the Activated Carbon curve digitizes to 3.699 wt%, the printed 3.7, and the end points of the other five curves also sit at the heights of their Table I values (visual comparison only, those curves are not digitized), so Table I appears to list each isotherm's end value. M1 is the last filled marker of the Activated Carbon curve: printed 3.7 wt% and 414.4 cc g-1, digitized 6079.9 kPa (60.7995 bar), 3.69861 wt%. `pressure digitized` is in notes. If the reconciler reads "up to 6000 kPa" as the printed pressure, the closest plotted point is the second-last filled marker (5964.2 kPa, 3.664 wt%, row M23), 36 kPa from 6000 against 80 kPa for the last one; both are within 2 % of 6000 kPa and both round to 3.7 wt%.
- Branch assignment: the paper does not say which symbols are adsorption or desorption (caption: "adsorption-desorption isotherms", legend shows filled symbols only). Filled = adsorption, open = desorption by convention. Support: filled markers have a constant pitch of about 13 px (about 245 kPa) as for preset adsorption pressures; open markers have a pitch growing from 10 to 13 px; the Table I value equals the last filled marker.
- measurement_method = unknown: BELSORP-HP is named but the paper never says volumetric or gravimetric, and no free-volume or buoyancy statement is made. So basis_inferred = unknown, uptake_type = unspecified, calibration_described = false.
- wt% convention: M1 has both wt% and cc g-1 for the same point. W1 from 414.4 cc g-1 is 3.727 wt% (matches printed 3.7 within rounding); a W2 reading of 3.7 would give W1 3.84 wt% (427.2 cc g-1), no match. Coded W1, inferred_from_paired_units. All six cc g-1 values in Table I are exactly 112 x the printed wt% (3.7 x 112 = 414.4), so the cc g-1 figures look derived from wt% by the authors. Digitized rows have no paired unit: unknown, none.
- uncertainty: "within the range of +/-0.5 %" (p. 748) is a percentage, not wt%, so `uncertainty_wt_pct` is empty and replicates_reported = true (stated reproducibility in %).
- Table I "Pore volume" is stored as total_pore_volume_cm3_g (method other, probe N2) because section 2.5 says pore volume was obtained by the single-point adsorption method; one sentence in section 3 calls it "micropore volume". No P/P0 for the single point is printed.
- Pore width 0.90 nm is stored as average_pore_diameter_nm with method BJH as printed (BJH desorption), although a 0.9 nm width is outside the BJH range.
- measuring_lab_id: first marked corresponding author is Rajesh S. Somani; first affiliation names no university, so the institute is used as printed.
- Sample mass and free-volume calibration are not stated; fields empty. BET P/P0 range and consistency criteria not stated (false).
- N2 BET measured on the same carbon in the same degas state (393 K, vacuum): area_same_sample = yes.

## Figure 6 digitization

- Page image main-6.png (1241 x 1630 px). Tick pixels found by inspecting pixel rows and columns: x axis 0 at 687, 1000 at 740, 2000 at 793, 3000 at 845.5, 4000 at 898, 5000 at 951, 6000 at 1003.5, 7000 at 1056; y axis 0 at 1345 and 1 to 11 at 1319, 1293, 1267, 1241, 1215, 1189, 1163, 1137, 1110.5, 1084, 1058 (26.09 px per wt%).
- Calibration: x 687 = 0 and 1056 = 7000 kPa, verified on 3000 at 845.5 (predicted 3006.8, 0.23 %); y 1345 = 0 and 1058 = 11 wt%, verified on 6 at 1189 (predicted 5.979, 0.35 %). Tick labels are consistent.
- All series in Figure 6 are black (colour #231f20), so the Activated Carbon curve was isolated with a derived image made with `work/prep.py` from the page image (same pixel grid, only pixels erased or redrawn): `ac_filled.png` keeps the original pixels within -9 to +3 px of the lowest dark pixel of each column for x >= 703 px (the AC curve is the lowest curve), erasing the other series. `ac_holes.png` redraws the white interiors enclosed by the outlines of open triangles (24 interiors, 8 to 13 px each) as dark blobs dilated by 1 px, because the tool's 3-px opening deletes 1-px outlines of hollow markers.
- `digitize_figure.py extract --mode markers --color '#231f20' --tolerance 60`, default opening: filled series 23 points (archive `digitizations/HYC-0071_Fig6_ActivatedCarbon_filled.json`), open series 24 points (archive `digitizations/HYC-0071_Fig6_ActivatedCarbon_open.json`). Open-marker points are centroids of marker interiors, which coincide with the marker centroid.
- Step-6 check: filled series at 6000 kPa digitized 3.67477 against 3.7 stated (0.68 %), pass. Open series at 5829 kPa digitized 3.63846 against 3.7 stated (1.66 %), pass; the paper states the value only for the isotherm end, so this is an approximate check for the open series.
- Marker centroids of triangles lie about 1 px (about 0.05 wt%) above the bounding-box centre; the tool's centroid convention was kept.

## Markers seen but not extracted (Figure 6, Activated Carbon series)

- Markers at p below about 300 kPa (x < 703 px, uptake below about 1.8 wt%): the filled and open triangles stack along the y axis and overlap each other and markers of the other series; individual markers could not be separated. Not extracted, not counted.
- One filled marker at about 2586 kPa (px 823, 2.96 wt%) is mostly covered by the open marker at 2516 kPa. A run with a 2-px opening finds a 13-px fragment there, but a single-point archive cannot pass the step-6 check (no stated value at that pressure), so no row was written. Counted in isotherm_point_count.
- One filled marker expected at about 2320 kPa (px 809) is fully covered by the open marker at 2324 kPa (no visible pixels); position inferred only from the 13-px pitch. Not extracted, not counted.
- A 2-px opening also finds an 8-px fragment at about 490 kPa (px 713, 1.97 wt%) next to the open marker at 427 kPa. It may be a covered filled marker but does not fit the 13-px pitch; not extracted, not counted.
- isotherm_point_count = 48 = 23 filled + 1 partly covered filled + 24 open resolved markers. It is a lower bound because the low-pressure cluster is not counted.

## Values seen but not extracted

- Table I: MIL-101 (6.36 wt%, 712.3 cc g-1; BET 2887.39), AC@MIL-101/A (10.1 wt%, 1131.2 cc g-1), /B (8.4, 940.8), /C (7.2, 806.4), /D (6.1, 683.2): MOF and MOF composites, not carbon sorbents. Their BET areas, pore volumes and pore widths are characterization of the same non-carbon samples.
- Text p. 751: MIL-101 "6.3 wt%" (Table I gives 6.36), "nearly 58 % increase" for AC@MIL-101/A: not carbon sorbents; the 58 % is a derived comparison.
- Abstract: AC@MIL-101/A 10.1 wt% at 77.4 K, 6000 kPa: composite, not carbon sorbent.
- Figure 6 curves of MIL-101 and AC@MIL-101/A to /D: not carbon sorbents, not digitized.
- Introduction and discussion literature values (Rowsell et al. 1.62, 1.32, 1.25 wt% for IRMOF-11, IRMOF-1, MOF-177; Latroche et al. MIL-101 6.1 wt% at 6 MPa, 77 K): other papers' MOF data, not measured here.
- Figure 4 (N2 isotherms at 77.4 K) and Figure 5 (pore size distributions): not H2 uptake, not digitized. Figures 1 to 3 (PXRD, TGA, TEM): no uptake values.
- Supplementary file si1: HKUST-1A (3.27 wt%, BET 1342.52 m2 g-1, 0.64 cm3 g-1) and HKUST-1B (Table 1 3.95 wt%, text 3.96 wt%, BET 1483.28, 0.73) and their H2 isotherms (SI Figures 3a, 3b, 77 K, up to 6000 and 2700 kPa) and N2 isotherms (SI Figure 2): a copper MOF, not a carbon sorbent. SI also quotes literature values for HKUST-1 (3.2 wt% at 88 bar, 3.3 wt% at 25 bar, 3.6 wt% at 10 bar, 3.6 wt% at 50 bar, 4.1 wt% at 26 bar): other papers, MOF.
- Carbon content of the composites (0.63, 1.25, 1.87, 2.5 wt%) and TGA water contents (35, 20, 5 %): characterization of composites, no uptake.
- No sample with characterization but without an H2 uptake value is in scope.
