# HYC-0040 extraction log (agent B)

Paper: Flamina et al. 2023, Applied Surface Science Advances 13, 100371. Inputs: main-1..9.png, si1-1..6.png. 104 rows written.

## Sources extracted from

- main p7 Table 1 (experimental rows): 9 values (rGO, B-rGO, Ni-B-rGO at 77, 273, 298 K; 20 bar) -> 9 table_direct rows (M33, M63, M98, M99-M104). The same values are repeated in main p1 abstract (some with "~"), main p6 Results text, main p7 Fig. 8 caption and drop-line labels, and SI p2 Table S1 ("Present work"); each is one measurement, so one row each, all locations named in `source_location`.
- main p7 Fig. 8(i) 77 K PCI (absorption): all markers digitized. rGO 33 markers (I1), B-rGO 30 (I2), Ni-B-rGO 35 (I3). The highest-pressure marker of each series is merged with its Table 1 value (see "Merging"), the rest are figure_digitized rows (32 + 29 + 34 = 95 rows).
- main p7 Fig. 8(ii) 273 K PCI: markers counted only: rGO 23 (I4), B-rGO 23 (I5), Ni-B-rGO 23 (I6). The highest-pressure point of each curve is the Table 1 value (rows M99-M101). No value was digitized (see "Fig. 8(ii) axis").
- main p7 Fig. 8(iii) 298 K PCI: B-rGO 22 markers (I7), Ni-B-rGO 21 markers (I8), digitized; only the highest-pressure point of each is a row, merged with its Table 1 value (M103, M104). rGO: legend "rGO-no storage", no points plotted (checked: no green pixels in the plot area outside the legend); Table 1 "0" -> row M102 (uptake_bound approximate, no isotherm_id).
- main p2 Experimental (synthesis of GO, rGO, B-rGO, Ni-B-rGO): material descriptions and synthesis_method.
- main p3 Experimental: BET/BJH method (Autosorb iQ, N2 at 77 K), GRC volumetric PCI method (Advanced Materials Corporation), H2 99.99 %, degassing 12 h, ~200 mg sample, LaNi5 / Basolite C-300 calibration standards; main p6: degassing at 100 C before PCI, Eq. (2) wt% definition (W2, stated).
- main p3 XRD text: rGO interlayer spacing 0.35 nm (stored); GO 0.7 nm (GO has no row).
- main p5 Fig. 4(f) EDS maps of Ni-B-rGO: C 60 wt.%, B 20 wt.%, Ni 18 wt.% (stored as dopant_concentration_wt_pct 20, method other; metal_loading_wt_pct 18).
- main p5 FTIR text/Fig. 5 and SI p3-4 XPS text/Fig. S2: functional_groups.
- SI p3 Table S2: BET area, pore volume, pore size for rGO, B-rGO, Ni-B-rGO (stored on every row of each sample; rGO pore volume 4.1 cc/g exceeds the schema maximum of 3 for total_pore_volume_cm3_g and is kept in notes only).
- SI p2 Fig. S1: N2 sorption isotherms with "Surface area = 897 / 119 / 85 m2/g" (same values as Table S2); not H2, not digitized.

## Samples and numbering

- S1 Ni-B-rGO, S2 B-rGO, S3 rGO: numbered by first appearance in the paper (title names Ni-dispersed B-doped rGO; the abstract introduces B-rGO; rGO as a sample first appears in the Experimental section). GO is characterized only (no H2 uptake), gets no row and no number.
- Labels taken from Table 1 (first table reporting uptake): "rGO", "B-rGO", "Ni-B-rGO".
- Class: Ni-B-rGO composite (Ni nanoparticles), B-rGO doped_carbon (B in lattice per XPS BC3), rGO reduced_graphene_oxide; synthesis_method thermal_reduction for all (raw carbon = Hummers GO thermally reduced at 400 C).

## Merging table/text values with plotted points

- The paper marks the highest-pressure marker of every Fig. 8 curve with a dashed drop line labelled with the printed value (6.9%, 8.2%, 9.8%; 0.35%, 0.41%, 0.58%; 0.16%, 0.24%); zoomed images confirm each drop line starts at the top marker. Each printed value is therefore recorded once with the printed pressure (20 bar) and the curve's isotherm_id, digitized point in notes.
- The top markers lie at 20.35-20.87 atm (20.52-21.14 bar), more than 2 % above the printed 20 bar; at 77 K the second-highest markers of all three series (20.12, 19.83, 20.20 bar) are within 2 % of 20 bar, but the drop line marks the top marker, so the top marker is the merged one and the second-highest markers are kept as digitized rows (M32, M62, M97, noted).
- Digitized vs printed at the merged points: rGO 77 K 9.839 vs 9.8; B-rGO 77 K 8.267 vs 8.2; Ni-B-rGO 77 K 6.896 vs 6.9; B-rGO 298 K 0.2473 vs 0.24; Ni-B-rGO 298 K 0.1525 vs 0.16 (-4.7 %).
- Pressure discrepancy: Table 1 caption and text print 20 bar; the experimental section says pressure was increased "from 10^-3 atm to 20 atm"; Fig. 8 y axes are in atm. Rows carry the printed 20 bar.

## Fig. 8(ii) axis (273 K)

- x-axis tick labels are printed 0.1, 0.2, 0.3, 0.3, 0.4, 0.5 at equally spaced major ticks (px 725, 803.5, 882, 960.5, 1039, 1117.5 on main-7.png): the labels are inconsistent (0.3 repeated), so no wt% value was extracted from this panel; the panel was used only to count markers (23 per series, own connected-component count, visually verified). No digitization archive for this panel.

## Digitization details

- Axes located from pixel rows/columns of main-7.png. Fig. 8(i): x 1 @ px 180, 9 @ 556.5, check 5 @ 368 (0.11 %); y 0 @ px 496, 20 @ 150.5, check 10 @ 323 (0.14 %). Fig. 8(iii): x 0.02 @ px 446.5, 0.22 @ 824, check 0.12 @ 635.5 (0.11 %); y 0 @ 971, 20 @ 626, check 10 @ 798.5 (0.00 %).
- Work images: copies of main-7.png with the legend, the "T = ..." box and the drop-line value labels painted white (main-7_f8a_clean.png, main-7_f8c_clean.png in the work directory) so legend symbols and coloured labels are not read as markers; no data region was altered.
- Fig. 8(i): rGO #008000 tol 60 -> 33/33; B-rGO #0000ff tol 130, opening 2 px -> 30/30 (at tol 60 two markers were lost: the first one, mostly hidden under the first Ni-B-rGO triangle, and one crossed by the black drop line); Ni-B-rGO #000000 tol 100 -> 35/35.
- Fig. 8(iii): B-rGO #0000ff tol 130, opening 2 px -> 22/22 (first marker partly hidden under a Ni-B-rGO triangle); Ni-B-rGO #000000 tol 100 -> 21/21.
- Partly hidden markers: B-rGO 77 K marker 1 (row M34, confidence 3) and B-rGO 298 K marker 1 (archive only) are centroids of their visible parts, biased by up to ~1.5 px (~0.09 atm) toward the visible side.
- Tool check (`digitize_figure.py check`, stated point at 20 bar = 19.74 atm, 5 %): passed for rGO 77 K (at 9.8 wt%, +0.38 %), B-rGO 77 K (at 8.2, +0.81 %), B-rGO 298 K (at 0.24, +1.17 %). Could not run for Ni-B-rGO 77 K (stated 6.9 wt% just beyond last digitized x 6.896) or Ni-B-rGO 298 K (stated 0.16 beyond last digitized x 0.1525); those two archives remain "unchecked".
- Some markers lie outside the calibrated tick range (x < 1 or > 9, y > 20 in Fig. 8(i); x < 0.02 or > 0.22, y > 20 in Fig. 8(iii)); they are on the same linear axes and were kept.

## Coding decisions

- wt% convention: W2, stated (Eq. (2), main p6) for all wt% values, including digitized Fig. 8 values (axis "Wt.% H").
- Basis: never named ("in excess to that reported by Blankenship" means "greater than") -> basis_stated false, uptake_type unspecified, basis_inferred excess (volumetric default).
- instrument_identified true: "Gas Reaction Controller (GRC) procured from Advanced Materials Corporation, USA" (manufacturer and product named). calibration_described false: only calibration "using standard samples like LaNi5 and basolite (C-300)", no free-volume determination.
- Degassing: 100 C, 12 h (PCI-specific statements); the BET paragraph's "degassed at 100 C for 3 hrs prior to all measurements" noted.
- replicates_reported false: no error bars, no uncertainty, no repeated isotherms (transducer resolution is not an uptake uncertainty).
- area_same_sample yes for all three (areas reported for "all prepared nanohybrids", same labels, authors' own measurement). bet_range_stated false ("P/P0 between 0 and 1" is the measurement range).
- Pore volume stored as total_pore_volume_cm3_g with method unspecified (printed "Pore volume", caption "average pore volume"); pore size stored as average_pore_diameter_nm with method BJH (radius vs diameter not stated; BJH insets plotted vs pore radius).
- measuring_lab_id: corresponding author A. Flamina (*), affiliation a, Indian Institute of Technology, Kanpur.

## Values seen but not extracted

- main p7 Table 1 "recalculated negating the weight of B" (B-rGO 11.38, 0.80, 0.33 wt%) and "recalculated negating the weight of Ni" (Ni-B-rGO 8.41, 0.50, 0.19 wt%): the same measurements re-expressed on a different mass basis (sample mass minus B or Ni), not uptake per sorbent mass; recorded in the notes of the matching experimental rows, not as separate rows.
- main p6 "the net amount of hydrogen stored for a known amount of B-rGO and Ni-B-rGO is found to be: 3.7 g and 3.84 g": absolute amounts for an unstated sample mass, temperature and pressure; not a specific uptake.
- main p8 Conclusions "This leads to an increase in the adsorbed amount by 1.6 wt.%": a difference computed between samples, not a measurement.
- main p8 Conclusions "These results are the best so far reported ..." : no value.
- main p2 Introduction, literature values cited for comparison (other papers): Wei et al. 0.007, 0.13, 0.055 wt% (293.15 K, 1 bar); Zhou et al. 0.77 wt% (298 K, 80 bar); Al-doped graphene 5.13 wt% (300 K, 0.1 GPa, DFT); Ti-graphene 6.11 wt% (300 K, DFT); N-doped CNTs 2 wt% (298 K, 100 bar); N-MC 0.51 and Pt/N-MC 1.26 wt%; B-substituted CNTs 2 wt% (80 bar, 300 K); Chung et al. 0.4 and 3.2 wt% (RT and 77 K, 56 bar); Blankenship et al. 0.8 wt% excess and 1.2 wt% total (30 bar, RT); Pd-modified activated carbon 2.5 wt% (298 K, 20 bar); Pd-doped MWCNT 0.6 wt% (273 K, 50 atm); Pd3Co-B-doped graphene 4.6 wt% (298 K, 30 bar); Ni-doped MWCNT 0.298 wt% (298 K, 20 bar); microporous carbons 8.9 wt% (77 K, 30 bar). Not this paper's measurements.
- main p6 Results: Blankenship et al. 8.1 wt% at 77 K and 20 bar (literature).
- SI p1-2 Table S1: 22 literature values (graphene-like nanosheets, single-layer graphene, exfoliated GO, thermally exfoliated GO, hierarchical graphene, Fe-graphene, F-graphite, N-graphene, Pd3Co/B-graphene, TiO2/N-rGO, Pd/N-graphene, Ni/Pd-rGO, Pd/Al2O3-graphene, Al-graphene, functionalized hydrogen-exfoliated graphene with and without Pd): other papers' values. Its "Present work" rows duplicate Table 1 and are covered by the Table 1 rows.
- main p3 calibration standards LaNi5 (298 K) and Basolite C-300 (MOF, 77 K): non-carbon materials, no values printed.
- main p8 Fig. 9 Raman of hydrogenated Ni-B-rGO at 253, 268, 373 K and 20 bar, and Fig. 10 FTIR of hydrogenated Ni-B-rGO at 303 K: qualitative evidence of adsorbed H2 / C-H bonds, no uptake values.
- GO (characterization only, no H2 uptake, no BET): XRD (001) 12.5 deg, d = 0.7 nm; Raman ID/IG 0.93, La 20.6 nm; TGA total weight loss 68 %; FTIR O-H, C=O, C=C, C-OH, C-O.
- Characterization without a schema field: Raman ID/IG rGO 0.95, B-rGO 0.99, Ni-B-rGO 1.05 (1.15 after hydrogenation); La rGO 20.2 nm, B-rGO 19.4 nm, Ni-B-rGO 18.3 nm; TGA weight loss rGO 49.4 %, B-rGO 20 %, Ni-B-rGO 42.5 %; Ni particle size ~1-2 nm, inter-particle distance ~20 nm (in material_description); Ni(111) d = 0.21 nm; XPS binding energies (SI p3).
- Figures not digitized: Fig. 7 TGA, Fig. 5/6/9/10 spectra, Fig. 2 XRD, SI Fig. S1 N2 isotherms and BJH insets, SI Fig. S2 XPS: not H2 isotherms.
