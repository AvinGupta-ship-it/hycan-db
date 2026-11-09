# HYC-0031 extraction log (agent B)

Blankenship, Balahmar & Mokaya, Nature Communications 2017 (8:1545), "Oxygen-rich microporous carbons with exceptional hydrogen storage capacity". 393 rows, 20 samples, 25 isotherms (I1-I25). Inputs: page images main-01..12 and si1-01..23 only.

## Sources extracted from

- Main p.4, Table 2 (CA-4600, CA-4700, CA-4800): total and excess wt% at 1, 20 and 30 bar, and g l-1 at 20 and 30 bar, all at -196 oC. The text on p.7 says Table 2 summarises the uptake at 1, 20 and 30 bar taken from the Fig. 6 isotherms. So each value was merged with the closest plotted marker of its isotherm. Where that marker is hidden, the value carries the isotherm_id with no digitized point (the 1-bar excess values). The CA-4800 1-bar values have no plotted marker at 1 bar. The total was merged with the closest marker (0.82 bar, 3.33 wt%), and the gap is stated in notes. The CA-4700 1-bar total was merged with the marker at 0.967 bar.
- Main p.6, Fig. 6 (77 K, gravimetric excess and total, 6 series): digitized. The CA-4700 excess series was digitized from the higher-resolution replot in Supplementary Fig. 10, because in Fig. 6 its 23 and 24 bar rings are hidden under CA-4800 total markers. Archives: F6_CA-4600_total, F6_CA-4600_excess, F6_CA-4700_total, F6_CA-4800_total, F6_CA-4800_excess (all checked against Table 2 at 20 bar; passed).
- Main p.8, Fig. 7 (77 K, volumetric g l-1): CA-4600 total, CA-4700 total and CA-4700 excess were digitized (F7_*). Each point was attached as volumetric_capacity_kg_m3 to the gravimetric row of the same run and pressure. The match used pressure, and the ratio g l-1 / wt% = 10 x packing density served only as an identity check; all 90 points matched. Where Table 2 prints a volumetric value, the printed value is stored and the Fig. 7 point is noted.
- Main pp.7-9 text, abstract and Discussion: printed 25 oC values were extracted. These are excess at 20 bar (AX21 0.3, CA-4600 0.42, CA-4800 0.5, CA-4700 0.63), excess at 30 bar (0.38, 0.50, 0.61, 0.80) and total at 30 bar (AX21 0.8, CA-4800 0.95, CA-4700 1.2). Each was merged with its Supplementary Fig. 14 marker. The 77 K values in the text duplicate the tables and were merged into the table rows (noted).
- Main p.7 text, literature record values: 7.08 wt% (doubly activated carbon, ref. 23), 7.03 wt% (activated polypyrrole carbon, ref. 29) and 7.1 wt% (compactivated sawdust carbon, ref. 55) were extracted as (unlabelled 1-3). Temperature, pressure and basis are unstated, so the rows carry temperature_unstated and pressure_unstated = true and value_kind = unclear. The 7.3 wt% (compactivated polypyrrole, ref. 55) and 7.3 wt% (zeolite-templated carbon, ref. 9) values were taken as the same measurements as PPY-4800 and ZTC-5 in Supplementary Table 4 (same references, same values) and merged there.
- SI p.17, Supplementary Table 2: C-4600, C-4700, C-4800 values at 1 bar (basis unnamed) and at 20 bar (total and excess) were extracted. The CA-4T rows duplicate Table 2 and were not re-entered.
- SI p.18, Supplementary Table 3: G-4700, S-4700, E-4700, F-4700, LAC4700, ACGR4700, ACCA4700 and CN4700 were extracted, with "previously reported" and the reference number. The CA-4700 row duplicates Table 2, and the C-4700 row duplicates Supplementary Table 2.
- SI p.19, Supplementary Table 4: PPY-4800, ZTC-5 (refs 2, 3) and AX21 ("This work") were extracted. The CA-4700 row duplicates Table 2.
- SI p.20, Supplementary Table 5: ACGR4700 and ACCA4700 are named "Excess" at 1 and 20 bar (footnote d). These were merged with the Supplementary Table 3 values (same printed numbers) and form excess isotherms I16 and I17 of 2 points each. The CA-4800 row duplicates Table 2.
- SI p.21, Supplementary Table 6: the CA-4T rows duplicate Table 2 (wt% and g l-1). The MOF rows were not extracted (listed below).
- SI p.9, Supplementary Fig. 9 (total uptake; temperature taken from Supplementary Table 2): the C-4600, C-4700 and C-4800 open circles were digitized above about 10.5 bar only (S9_*). The CA-4T filled series are replots of the Fig. 6 totals: the points coincide, including the double markers near 21 bar (CA-4800) and 23 bar (CA-4600). They were not digitized again.
- SI p.10, Supplementary Fig. 10 (temperature taken from Supplementary Table 4): the CA-4700 excess, ZTC5 total and excess, PPY-4800 total and excess, and AX21 total and excess series were digitized (S10_*). The CA-4700 total series is a replot of Fig. 6 and was not digitized again.
- SI p.14, Supplementary Fig. 14 (25 oC, 8 series): only the highest-pressure marker (30 bar) and the markers at the pressures of printed text values (20 bar, excess series) were digitized (S14_*).
- SI p.15, Supplementary Fig. 15 (CA-4700, 25 oC, to 100 bar): its points up to 30 bar coincide with Supplementary Fig. 14 (same pressures and values), so it was treated as the same run (isotherms I7 and I8). The 100 bar markers were digitized as the highest-pressure points (S15_*).
- Main p.10 Methods: instrument, H2 purity, degassing, BET range, t-plot, total pore volume, NLDFT, packing density, and the definitions of excess and total (Eq. 1) and of volumetric uptake (Eqs 2-3).
- Main p.2 Table 1 and SI p.16 Supplementary Table 1 (elemental analysis): used only for composition notes. They contain no H2 uptake.

## Digitization method

- Every axis was calibrated on its lowest and highest labelled ticks and verified on a middle tick. All tick pixels were found by scanning pixel rows and columns. All verification residuals were 0.5 px or less.

| Figure | x axis | y axis |
|---|---|---|
| Fig. 6 | 0 @ 205, 30 @ 536, verified 15 @ 371 | 0 @ 886, 10 @ 552, verified 5 @ 719 |
| Fig. 7 | 0 @ 700, 30 @ 945, verified 15 @ 822 | 0 @ 390, 50 @ 115, verified 25 @ 253 |
| SI Fig. 9 | 0 @ 367, 30 @ 947, verified 15 @ 657 | 0 @ 900, 10 @ 317, verified 5 @ 609 |
| SI Fig. 10 | 0 @ 363, 30 @ 945, verified 15 @ 654 | 0 @ 881, 10 @ 295, verified 5 @ 588 |
| SI Fig. 14 | 0 @ 370.5, 30 @ 960.5, verified 15 @ 665.5 | 0 @ 843, 1.2 @ 297, verified 0.6 @ 570 |
| SI Fig. 15 | 0 @ 381, 100 @ 941, verified 50 @ 661 | 0 @ 861, 3.0 @ 297, verified 1.5 @ 579 |

- Marker centres were found on the page image. Isolated filled markers used the tool's own --mode markers centroid on the page with the legend masked. Doubles, rings and stars needed more:
  - Overlapping filled doubles were split from the image moments and the extent along the long axis.
  - Open rings used angular-coverage ring fits or the centroid of the hole-filled ring.
  - Stars were found by template matching.
  - Partly hidden markers used fits that treat other colours as neutral.
- Each series was then archived by running scripts/digitize_figure.py extract --mode markers on a layer that holds a small disk at each centre. The layer is an up-scaled crop of the plot (scale S), and the page's tick calibration was transformed by X = (x - x0)*S + (S - 1)/2.
- Each archive holds exactly the markers listed (centres = extracted points). Its status was set with the tool's check command against a printed value; all passed, except S14_CA-4600_total, which stays unchecked because the paper prints no value for that isotherm.
- The scripts and layers are in the work directory (scripts/, centers/, layers/).
- Rows of partly hidden or split markers carry extraction_confidence one lower and a note.

## Markers counted but not digitized (could not be separated)

- Fig. 6:
  - CA-4700 total: about 4 markers below about 0.6 bar, hidden under the blue and black markers (only fragments visible).
  - CA-4800 total: 1 fragment near 0.2 bar / 1.4 wt%.
  - Origin markers: the red and black origin markers, if present, are hidden under the blue origin marker.
  - Excess series: CA-4600 excess markers below 3 bar (about 7), CA-4800 excess markers below 3 bar and at 12-14 bar (behind the black filled markers), and CA-4700 excess markers below 2 bar are hidden under the total markers.
  - The CA-4800 total origin marker (0 bar, 0 wt%) is in archive F6_CA-4800_total but was not entered as a row: its digitized pressure is -0.03 bar.
- Fig. 7:
  - Low-pressure markers (below about 0.7 bar) of CA-4600 and CA-4700 total are hidden in a cluster with the MOF series.
  - CA-4700 excess markers at 1 and 2 bar are hidden under the total markers.
  - The CA-4600 excess open markers (about 6 px rings beside the filled markers and lines) could not be separated, so no series was digitized for them.
- SI Fig. 9: C-4600, C-4700 and C-4800 markers below about 10.5 bar are dense, overlapping open circles at about 0.5 bar spacing (several tens per series). They were not digitized and could not be counted, so isotherm_point_count is empty for I13-I15.
- SI Fig. 10:
  - All series below about 1.5-2 bar lie in a dense cluster dominated by AX21 stars (about 13 star positions for AX21 total). Not digitized; isotherm_point_count is empty for I18-I23.
  - The ZTC5 total marker near 30 bar is hidden under the PPY-4800 total marker.
  - The ZTC5 excess ring at 2 bar lies behind the ZTC5 total marker.
  - The PPY-4800 excess rings near 1 and 2 bar are overlapped.
- SI Fig. 14: the markers near 0 bar overlap. Each isotherm has 24 markers (about 0, 1-10, 11.5, 13, 14.5, 16, 17.5, 19, 20, 21, 23, 24.5, 26, 27.5 and 30 bar); only the markers named above were digitized (scope).
- SI Fig. 15: 31 markers per series; the 100 bar markers were digitized. The 30 bar markers are also in the S15 archives, only for the tool check; the 30 bar rows use Supplementary Fig. 14.
- Archives S14_CA-4700_total and S14_CA-4800_total also contain the 27.5 bar marker, only for the tool check; it has no row.
- Fig. 8a (25 oC excess) is a replot of the Supplementary Fig. 14 excess series and was not digitized separately. SI Fig. 13 is a replot of CA-4700 total and excess with MOFs and was not digitized.

## Discrepancies recorded

- PPY-4800 total at 20 bar: printed 7.3 wt% (Supplementary Table 4 and text), plotted marker about 7.07 wt%. PPY-4800 at 1 bar: printed 2.2 wt%, nearest plotted marker 0.98 bar / 2.64 wt% (outside the pressure tolerance, so not merged).
- CA-4800 total at 25 oC and 30 bar: printed 0.95 wt%, plotted 0.917 wt%.
- CA-4800 total volumetric at 20 bar: printed 41 g l-1, while 6.8 wt% x 0.56 g cm-3 = 38 g l-1. The printed value is kept.
- The ZTC5 total and excess series in Supplementary Fig. 10 are plotted at different pressures below 20 bar.

## Coding decisions

- material_class is activated_carbon (templated_carbon for ZTC-5). The high oxygen content comes from precursor oxygen and surface groups, not deliberate doping, so O is not coded as a dopant. The CHN, XPS and TPD O contents are in notes.
- synthesis_method is carbonization (hydrothermal carbonisation of the precursor), and KOH activation goes in activation_method.
- Basis: excess and total are each named and defined (Methods, Eq. 1) and reported side by side, so basis_stated = true.
- Unlabelled 1-bar columns in Supplementary Tables 2-4 are coded uptake_type unspecified (footnote e covers the 20-bar column only). Cited values have measurement_method unknown, which gives basis_inferred unknown.
- wt% convention: not defined. Eq. 1 uses a W2-type expression for the gas term, so the code is unknown/none, with a note.
- The degas duration is printed as 4-6 h and was not stored. The degas end pressure is 10^-10 bar = 1e-05 Pa. The H2 purity is 99.9999%.

## Values seen and not extracted

- MOFs (not carbon sorbents):
  - Supplementary Table 6, excess (30 bar) / total (30 bar) wt%, and excess / total g l-1 at 20 (30) bar:

    | MOF | Excess wt% | Total wt% | Excess g l-1 | Total g l-1 |
    |---|---|---|---|---|
    | NOTT-112 | 6.8 (7.0) | 7.8 (8.6) | 16 (17) | 19 (21) |
    | NU-100 | 6.9 (7.8) | 8.5 (10.0) | 11 (12) | 13 (15) |
    | MOF-210, packing density | 6.4 (7.3) | 8.4 (10.2) | 8 (9) | 11 (13) |
    | MOF-210, crystal density | 6.4 (7.3) | 8.4 (10.2) | 16 (18) | 22 (26) |

  - Text p.8: NOTT-112 6.9 wt%, NU-100 6.8 wt%, MOF-210 6.4 wt% (MOF-200 and MOF-205 named without values), MOF ranges 8-16, 9-17, 11-19 and 13-21 g l-1, and MOF-210 "up to 22 and 26 g l-1".
  - The MOF series in Fig. 7 and SI Fig. 13 were not digitized.
- Aggregates across samples or literature (not rows): text p.7 "2-3 wt%" and "5-5.5 wt%"; text p.8 "32-40", "37-44", "33-41" and "41-48 g l-1" (ranges over the Table 2 values); text p.9 "between 0.5 and 1.6 wt%" at 150 bar.
- DOE targets (5.5 wt% and 40 g l-1; 7.5 wt% and 70 g l-1) are targets, not measurements.
- Non-uptake quantities: isosteric heats (Fig. 8b and text: 6.4-5.5, 9.5-8.3, 10.2-9.0 and 10.6-7.6 kJ mol-1), TPD CO2/CO evolution (Fig. 5; O 22.3, 18.5 and 21.2 wt%), and XPS surface O (20.7, 14.3, 13.8 and 14.8 wt%).
- Samples with characterization but no H2 uptake:
  - CA-hydrochar: C 66.2, H 3.9, O 29.9 wt%; O/C 0.339; H/C 0.707.
  - C-hydrochar: C 69.5, H 6.1, O 24.4 wt%; O/C 0.263; H/C 1.053.
  - Cellulose acetate (O/C 0.93) and cellulose (O/C 0.83).
  - SD2600 (IR spectrum only).
- Duplicates merged into one row (noted there): CA-4T values in Supplementary Tables 2-6, the text, the abstract and the Discussion; AX21 and PPY-4800 values in text p.7; ACGR4700 and ACCA4700 values in text p.8 and Supplementary Table 5.

No path outside the permitted list was opened.
