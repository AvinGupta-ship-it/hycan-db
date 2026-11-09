# HYC-0049 extraction log (agent B, page images only, 2026-11-09)

Stadie et al., Langmuir 2012, "Zeolite-Templated Carbon Materials for High-Pressure Hydrogen Storage". 78 rows in rows.csv.

## Samples (numbered by first appearance)
- S1 MSC-30 (this study; abstract, section 2.1). S2 MSC-30 of ref. 16 (first mentioned in the introduction, p.10058, "Maxsorb MSC-30, by nearly 100% at 34 MPa"). S3 CNS-201 (this study, section 2.1). S4 ZTC-1, S5 ZTC-2, S6 ZTC-3 (section 2.2). S7 P7(2)-H of ref. 16 (Figure 3 caption). S8 CNS-201 of ref. 5 and S9 MSC-30 of ref. 5 (Table 1). S10 CB850h of ref. 34 (section 4).
- The literature samples (S2, S7, S8, S9, S10) are other laboratories' physical samples cited by the paper. They are extracted under "values reported before" with `previously reported:` notes, `area_same_sample = other_paper`, and a `measuring_lab_id` that gives the first author of the cited reference. The paper does not print those laboratories' institutions.

## Sources extracted
- Table 1 (main p.10060): every uptake cell. The "H2 capacity" column holds 77 K Gibbs excess maxima with no pressure printed. The "high P H2 uptake" column holds values at 30 MPa. For this study's samples the column covers 298 K (footnote d gives 296-303 K, and the text says the measurements were at 298 K). For the ref. 16 samples it covers 303 K, from section 4. The table's skeletal densities and BET areas are recorded on every row of each sample.
- Section 3.2 text and abstract: ZTC-3 28.6 mmol/g (5.5 wt %) at 2.4 MPa. This is merged with Table 1 and with the Figure 4 inset marker at 2.367 MPa (within 2%) into one row (M65). The wt% is coded W2 by paired units.
- Section 3.3 text (p.10060): ZTC-3 "8.3 mmol g-1 (1.6 wt %) at 30 MPa and 298 K" restates Table 1's 8.27. It is one row (M70), and the wt% is coded W2 by paired units.
- Section 3.3 text (p.10061): MSC-30 3.9 mmol/g at 10 MPa and 298 K (M20). CNS-201 2.0 mmol/g (M40). The CNS-201 "reference value" of 2.1 mmol/g from ref. 5 (M76). The CNS-201 conditions are taken from the preceding sentence. No plotted point lies within 2% of 10 MPa, so neither value is merged. Linear interpolation of the Figure 5 points gives 4.02 and 2.04 mmol/g (`check` runs on full-series archives in the work directory).
- Section 4 text (p.10062): CB850h 8.33 wt % maximum excess capacity at 77 K, from ref. 34 (M78).
- Sections 2-3 and the SI: characterization recorded on the rows. This covers BET ranges as printed, skeletal densities, ZTC-3 NLDFT pore width 1.5 nm, XPS functional groups (Table S1), sp3/sp2 fractions (notes), degassing at 150 C, both instrument descriptions and the He-pycnometry free-volume method.
- Figure 4 inset (main p.10060): every resolvable 77 K marker of MSC-30, ZTC-2, ZTC-3 and CNS-201, and the highest-pressure marker of each 87 K isotherm.
- Figure 5 (main p.10060): the highest-pressure marker of each 298 K isotherm (MSC-30, ZTC-1, ZTC-2, ZTC-3, CNS-201).
- SI Figure S1 (SI p.5): the highest-pressure marker of each of the three ZTC-3 298 K cycles.

## Coding decisions
- Basis: "Gibbs's excess" is named but never defined, so `basis_stated = false`, `basis_inferred = excess` and `uptake_type = excess` for this study's rows.
- Table 1 77 K capacities. The paper never says these are taken from the Figure 4 curves, and it prints no pressure for them except for ZTC-3. Only ZTC-3 is therefore merged. MSC-30 (27.9), CNS-201 (12.7) and ZTC-2 (26.1) are separate rows with no isotherm_id, and ZTC-1 (18.5) has no plotted 77 K isotherm.
  - MSC-30 and CNS-201 are coded value_kind `measured` because each lies within 3% of a digitized point of the same isotherm.
  - ZTC-2 is INCONSISTENT with its curve. Figure 4's blue-diamond ZTC-2 77 K isotherm plateaus at 21.99 mmol/g, 16% below 26.1. The value is coded `fitted_extrapolated` under the protocol §3 maximum rule, although the paper does not say it was extrapolated.
  - CNS-201: the plotted 77 K isotherm still rises to 13.13 mmol/g at 3.0 MPa, 3.4% above the tabulated 12.7.
- Table 1 30 MPa values. The paper says they "were calculated by extrapolation of the data to 30 MPa", so they are coded `fitted_extrapolated` and carry their Figure 5 curve's isotherm_id.
  - ZTC-2 6.45 is merged with the highest plotted ZTC-2 marker (29.756 MPa, within 2% of 30 MPa) under the extraction rule, and stays `fitted_extrapolated` (M55).
  - The other samples' highest plotted points are more than 2% below 30 MPa, so their table and digitized rows are kept separate.
- Ref. 16 and ref. 5 literature values are coded value_kind `unclear`, because how the cited work obtained them is not stated here.
- `replicates_reported = true` only on ZTC-3 298 K rows (the three cycles in Figure S1).
- `degas_temperature_c = 150`: materials were "stored at 150 C under vacuum ... before use", and the SI says samples were degassed as in the Experimental Methods. No duration is given.
- 87 K: the paper prints "liquid helium (87 K)". The temperature is recorded as printed.
- Figure S1 cycles are coded as three separate isotherms (I14-I16). The paper does not say whether any cycle is the ZTC-3 298 K run in Figure 5 (I13), although the cycle 1 points resemble it.

## Digitization (scripts/digitize_figure.py, markers mode; archives in digitizations/)
- Figure 4 inset calibration (page main-4.png), checked against a third tick on each axis:
  - x: 0.0 MPa at x = 248.6 px and 3.5 MPa at x = 551.55 px; check tick 2.0 MPa at x = 421.52 px (0.11% error).
  - y: 0 mmol/g at y = 1154.2 px and 30 mmol/g at y = 1005.2 px; check tick 15 mmol/g at y = 1079.4 px (0.40% error).
  - Each colour was run once over the whole inset (tolerance 80, open-px 2). The diamond (77 K) and triangle (87 K) series of the same colour come out together in one archive (`fig4inset_<colour>_<sample>_77K.json`). Markers were assigned to a curve by position.
  - The 87 K highest-pressure markers were re-run with a small ROI (`*_87K_last.json`).
- Figure 5 calibration (main-4.png), checked against a third tick on each axis:
  - x: 0 MPa at x = 713.18 px and 30 MPa at x = 1133.56 px; check tick 15 MPa at x = 923.34 px.
  - y: 0 mmol/g at y = 1133.44 px and 9 mmol/g at y = 807.66 px; check tick 4 mmol/g at y = 988.54 px.
  - Highest-pressure markers were isolated with ROIs. For MSC-30, ZTC-3 and ZTC-2 that marker touches or overlaps its neighbour.
- Figure S1 calibration (si1-5.png), checked against a third tick on each axis:
  - x: 0 MPa at x = 377.8 px and 35 MPa at x = 947.0 px; check tick 15 MPa at x = 621.90 px.
  - y: 0 mmol/g at y = 612.92 px and 9 mmol/g at y = 158.50 px; check tick 4 mmol/g at y = 412.07 px (0.55% error).
  - Highest-pressure marker of each cycle isolated with an ROI.
- `check` was run on fig4inset_purple_ZTC-3_77K.json at 2.4 MPa, expecting 28.6. It passed with 0.97% error, but the interpolation runs over an archive that also holds 87 K triangles. No other stated value lies at a plotted pressure.
- Figure 5 marker counts were confirmed with full-colour runs in the work directory (t5_*.json), after merging fragments split by the black fit lines: MSC-30 16, ZTC-3 14, ZTC-2 14, ZTC-1 12, CNS-201 9.
- Figure S1 counts, by visual inspection of colour masks; markers of the three cycles overlap, so a fully hidden marker would be missed:
  - cycle 1: 12 filled + 6 open = 18, including an open navy marker at about 27.1 MPa that is mostly covered by a cycle 3 marker;
  - cycle 2: 13 filled + 4 open = 17;
  - cycle 3: 13 filled + 6 open = 19.

## Markers not separated (Figure 4 inset; the page image is about 150 dpi, so markers are about 5 px)
- MSC-30 77 K (red diamonds) and MSC-30 87 K (red triangles): every marker below about 0.2 MPa merges into one continuous red smear. The tool's components there are fragments or merged blobs (archive indices 0-10, including n = 82 and n = 108) and were not extracted. Index 25 (n = 4, 1.10 MPa) is a line fragment.
- ZTC-3 77 K: markers below about 0.1 MPa are hidden under red markers, and one marker near 0.76 MPa sits under the red MSC-30 marker at 0.74 MPa. Indices 0, 14, 16, 17, 19, 21, 23 and 28 (n of 6 or less) are line fragments.
- ZTC-3 87 K: markers below 0.2 MPa, and between about 0.4 and 1.1 MPa, are hidden under the red 87 K triangles. Purple indices 1, 3 and 5 (n = 4-8, 0.08-0.16 MPa) are partly visible low-pressure markers that could not be assigned or separated reliably and are not counted.
- ZTC-2 77 K: two partly hidden markers near 0.17 and 0.45 MPa could not be separated, and markers below about 0.15 MPa are hidden.
- ZTC-2 87 K: markers below about 0.15 MPa are hidden.
- CNS-201 77 K: markers below about 0.22 MPa are hidden under the coloured cluster. Indices 0 and 1 are fragments at the frame.
- CNS-201 87 K: markers below about 0.09 MPa are hidden.
- As a result, every 77 K and 87 K `isotherm_point_count` is a lower bound (the resolvable markers), as stated in each row's notes.
- The Figure 4 main panel shows the same 77/87 K runs compressed (0-30 MPa). Its low-pressure markers form one overlapping vertical stack and were not used.

## Values seen but not extracted
- Table 1 isoexcess enthalpies dH0 (8.6, 6.7, 6.6, 6.5, 7.3, 8 kJ/mol): not an uptake. They are given in row notes.
- Figure 4 main panel 298 K squares: the same data as Figure 5 (the paper says so). Extracted from Figure 5 only.
- Figure 4, Figure 5 and Figure S1 points other than the highest-pressure point at 87 K and 298 K: not extracted, by protocol 9.
- Figure 4 and 5 right-hand wt % axes: not used. The values were read on the mmol/g axis.
- MSC-30 at 298 K, "3 to 4 mmol g-1 (0.6-0.8 wt %) at 10 MPa" (refs 3, 5, 8, 11, 16): a range across several laboratories, so not a row.
- Ratios and trends, which are not uptake values of a sample:
  - abstract, section 4 and conclusions: 2.3 mmol g-1 (0.46 wt %) per 1000 m2 g-1 at 30 MPa and 298 K;
  - section 4: 9 mmol g-1 (1.8 wt %) per 1000 m2 g-1 at 77 K, and 5.4 H2 per nm2;
  - section 4: ref. 16's 2.8 mmol g-1 (0.55 wt %) and 2.0 mmol g-1 (0.41 wt %) per 1000 m2 g-1 at 303 K;
  - introduction: "~2 wt %" per 1000 m2 g-1 (Chahine's rule) and "~0.2 wt %" per 1000 m2 g-1 at 6.5 MPa (ref. 4);
  - SI: "~5 mmol" per mL of DR micropore volume at 298 K and 30 MPa, and the fits y = 0.0093x, y = 0.0023x and y = 5.13x.
- Relative or general statements:
  - introduction: ZTCs exceeded MSC-30 "by nearly 100% at 34 MPa" (ref. 16);
  - introduction: excess uptake at <10 MPa "usually below 1 wt %";
  - section 4: 15% higher delivery between 0.3 and 2.4 MPa;
  - section 3.1: an "~1 mmol g-1 difference" in calculated uptake from skeletal density;
  - section 3.4: dH lowered by up to 0.7 kJ/mol for 77-87 K fits;
  - heats of adsorption below 8 kJ/mol in ZTCs (ref. 16);
  - MOF-5 heat of adsorption (not a carbon).
- Figure 6 (isoexcess enthalpy against uptake): not an isotherm. It shows no uptake value beyond the isotherms.
- Figure 7 and the abstract graphic (uptake against BET area): not an isotherm, so not digitized.
  - This study's diamonds and squares duplicate Table 1.
  - The "x" points are literature 77 K values from ref. 37. The text and tables do not give them, so they are not extracted.
- SI Figure S2 (uptake at 298 K and 30 MPa against DR micropore volume): not an isotherm, so not digitized. Its uptakes duplicate Table 1. Its DR micropore volumes (CNS-201, ZTC-1, ZTC-2, MSC-30, ZTC-3) are not given in the text or tables and are not recorded.
- Characterization not stored in fields:
  - MSC-30 literature BET range 2600-3400 m2/g;
  - skeletal density 2.12 +/- 0.05 g/mL over four carbons, and standard error +/-0.06 g/mL;
  - XRD 14 A periodicity and Scherrer length 24 nm (ZTC-3);
  - TEM pore-to-pore spacing 1.0 nm;
  - P7(2)-H BET reanalysis 3538 +/- 50 m2/g and CB850h reanalysis 3800 m2/g (given in notes);
  - leak rates and apparatus volumes.
- Materials with characterization but no H2 uptake, so no rows:
  - zeolite NaY, an N2 isotherm (Figure 2) and XRD (Figure 1). It is not a carbon;
  - zeolite NHbeta (precursor);
  - NaY-C composite (XRD, Figure 1) and the Z-C intermediate;
  - calculated FAU framework (XRD);
  - ZTC "0% Pt-Ac" of ref. 33 (XPS, Figure S5);
  - graphite, carbon nanotubes, amorphous carbon and diamond (EELS references, Figures S7-S8);
  - "PFA-P7-H" of ref. 38 (mentioned only).
- No H2 value for a non-carbon material appears in the paper.

## Validator
- `validate_row_detail.py --errors-only`: no errors.
- Warnings: pressure above 200 bar on 14 rows. These are the printed 30 MPa table values and the digitized 298 K highest-pressure points (22.8-29.2 MPa), and they are kept. There is also one `unspecified` uptake_type (M76, ref. 5 reference value, whose basis is not named).
