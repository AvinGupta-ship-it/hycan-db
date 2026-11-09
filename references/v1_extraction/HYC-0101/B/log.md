# HYC-0101 extraction log (extractor B)

820 rows. Pages read from images only. Temperatures: -196 degC stored as 77.15 K, 25 degC as 298.15 K.

## Sources extracted from

- main p.3 Experimental: degassing (dried 80 degC 24 h, degassed 200 degC, 10^-10 bar, 4-6 h), H2 purity 99.9999%, Hiden IGA-003 (0-20 bar) and Hiden Xemis (0-150 bar), BET range 0.04-0.2, total pore volume at P/Po 0.99, t-plot, NLDFT.
- main p.4 Table 1: excess and total H2 uptake at -196 degC, 20 bar, 8 samples; surface area, pore volume, pore size. Merged with the 20 bar points of Figure 3 (I1-I16).
- main p.4 text: AX21 surface area 2881 and pore volume 1.71; N contents.
- main p.5 text: t-plot micropore areas of S4800 (1157) and S4800P (1413).
- main p.6 Figure 3a-d: 16 isotherms (77 K), all markers digitized.
- main p.7 text: literature values 7.08, 7.03, 7.3 wt% (refs 27, 9, 29) extracted as previously reported (S14-S16).
- main p.8 Table 3: densified samples; MPPY4-C10 and PPY4-C10 merged with Figure S11 20 bar points; MPPY4-C5 and PPY4-C5 single-value rows; PPY4 and MPPY4 rows repeat Table 1 (cited in source_location of the Table 1 rows).
- main p.8 text: AX21 4.5 / 5.6 wt% (merged with Figure S9, pressure digitized).
- main p.9 Figure 5: 4 isotherms (77 K, 0-150 bar, batch 2, Xemis), all markers digitized; merged with Tables S2/S3.
- main p.9 Figure 6: 25 degC; only the 150 bar point is extracted; points at 20-150 bar digitized for reference and recorded in notes of the Table S4 rows.
- main p.10 text: RT values (repeat Table S4/S5, cited in source_location); AX21 0.32 wt% and MPPY4 0.5 wt% at 20 bar, 25 degC (merged with Figure S13 highest points); literature RT excess 1.3 (ref 29), 1.2 (ref 48), 1.3 (ref 49), 1.0 (ref 28).
- SI p.2: excess/total definitions (basis evidence), total formula, packing density method.
- SI p.4 Table S2: total gravimetric and volumetric uptake, 40-150 bar, MPPY4 and MPPY4-C10 (batch 2).
- SI p.5 Table S3: MPPY4 / MPPY4-C10 batch 2 surface area, pore volume, maximum excess 6.5 / 6.0 at ca. 40 bar, volumetric excess 25.4 / 31.2, totals at 80 and 150 bar (repeat Table S2).
- SI p.6 Table S4: 25 degC excess, total (N2 pore volume) and total (D-R micropore volume), 20-150 bar, with total volumetric capacities: six isotherms (I31-I36), all table_direct.
- SI p.7 Table S5: 25 degC; batch 2 rows (repeat Table S4, volumetric excess 6.3 / 6.9 added at 150 bar); carbon KUA5 and two ZTC rows extracted as previously reported (S20-S22).
- SI p.17 Figure S9: AX21 excess and total at 77 K digitized (I17, I18). PPY4 and MPPY4 curves in Figure S9 duplicate Figure 3c (same values at 20 bar to within digitization); not extracted again (digitized for comparison only, work/compare).
- SI p.19 Figure S11a,b: 8 isotherms digitized (I19-I26). The MPPY4 and PPY4 curves here differ from Figure 3c (MPPY4 excess 5.66 vs 5.35 wt%; PPY4 excess 5.41 vs 4.98, total 7.14 vs 6.53 at 20 bar) and are treated as separate plotted runs (I21, I22, I25, I26). The PPY4-C10 and PPY4 curves of Figure S11b lie 8-13% above Table 3 (check passed only at 15% tolerance; recorded in notes).
- SI p.21 Figure S13: 25 degC, IGA; highest-pressure point of each of 3 isotherms extracted (AX21, MPPY4, MPPY4-C10).
- SI p.23 Figure S15: 25 degC; N2-pore-volume total series digitized only to locate Table S4 points (archives FS15_*_total_N2); no separate rows.

## Digitization method

Axes calibrated on the lowest and highest labelled ticks with a third labelled tick as check; tick pixels found by scanning pixel rows/columns (work/scripts/axes.py, ticks.py). All verification residuals below 0.4%. Overlapping open/filled markers of several series could not be isolated by colour alone, so marker centres were located by template matching on the page image (work/scripts/tm.py), reviewed visually on enlarged overlays, and painted as small discs on a blank canvas of the page size; scripts/digitize_figure.py extract --mode markers was run on that canvas with the page-image calibration (archives in digitizations/, 39 files). Each archive's extracted-point count equals the number of markers located. Every series with a printed value passed `digitize_figure.py check` (within 5%, except the four Figure S11b series, 8-13%, noted above). FS13_MPPY4-C10_excess_RT is unchecked: the paper prints no value for it.

## Markers not extracted, and point counts

- Total-series markers at low pressure in Figures 3, 5, S9, S11 are hidden behind the excess markers of the same run and were not digitized; isotherm_point_count for those totals is taken equal to the excess count (notes on each row).
- Figure 3b MPPY3 Excess: about 5 markers below 0.6 bar hidden behind PPY3 Excess.
- Figure 3c MPPY4 Excess: several low-pressure markers not separable; count 35 taken from Figure S10A (H2 series, 23 markers to 10 bar) plus 12 markers above 10 bar.
- Figure 3d S4800 (legend "S400") Excess and S4800P Excess: dense overlapping runs below about 0.9 bar not separable; counts are lower bounds.
- Figure S11a MPPY4 Excess: 8 markers at 0.28-1.48 bar hidden. Figure S11b PPY4 Excess: about 11 low-pressure markers visible only as fragments; 4 candidate positions dropped as unreliable.
- Figure 5 MPPY4 Excess: 2 markers (about 2 and 4 bar) not separable.
- Origin markers digitized at slightly negative pressure (F3a MPPY2 excess, F3d S4800 and S4800P excess, FS11b PPY4-C10 excess, F5 MPPY4 excess) were not written as rows (pressure 0 is not a valid stored pressure); listed in work/skipped_origin.json.
- Figure 1 legend and Figure 3d legend print "S400"/"S400P" for S4800/S4800P; Figure S1 caption also says "S400 and S400P". Treated as typographical; labels taken from Table 1.

## Values seen but not extracted

- CO2 uptake (Table 2, Table 4, Figures 7, 8, S16, text): not H2.
- MOF values (Table S3 MOF-5, MOF-5 pellets, MOF-177, NOTT-112, NU-100, MOF-210; Table S5 MOF-5, MOF-210; Table 4 MOF210): not carbon sorbents.
- Table 4 carbon monoliths A1 and A3-36 (CO2, ref 57): CO2, not H2.
- Figure S10A D2 uptake of MPPY4 and Figure S10B nD2/nH2 ratio (1.05-1.12): not H2 uptake; the S10A H2 curve duplicates Figure 3c (used only to count markers).
- Figure S12 MPPY4-C10 IGA and Xemis curves: same sample as Figures S11a and 5 (instrument comparison); digitized for comparison only (work/compare), not extracted again.
- Figure S15 D-R totals and excess at 25 degC: duplicate Table S4 / Figure 6.
- Text p.9 "total volumetric hydrogen storage (at 80 bar) is 46 and 60.3 g l-1" and abstract/Summary rounded values (38, 49, 56, 60, 72 g l-1; 3.4 wt% (14 g l-1), 3.2 wt% (18 g l-1) at RT): repeat Tables S2/S4; discrepancies recorded in notes.
- Text p.7 "majority of studies ... 3.0-5.2 wt% at -196 degC and 20 bar for activated carbons [5,6,30]": a range across many papers, not a row.
- Text p.8 "previously been measured under volumetric conditions [33]" for AX21: no number.
- Text p.10 "1.3 wt% for activated CNT superstructures [29]" extracted (S19); text p.9 MOF comparisons (MOF-5, MOF-177, NOTT-112, Nu-100, MOF-210; 9-18 g l-1; 12-28.5 g l-1): MOFs.
- Characterization without H2 uptake: polypyrrole precursor (C 65.2, H 4.4, O 16.7, N 13.4, S 0.2 wt%), sawdust hydrochar (C 69.3, H 6.8, O 23.9 wt%); PPY2600 (976 m2/g, micropore area 906, 0.47 cm3/g, micropore 0.40, pore 6.8 A, N 12.4 wt%, packing density 0.92) and MPPY2600 (1297, 1183, 0.64, 0.53, 5.9 A, N 12.2 wt%, packing density 0.85): no H2 measured. Carbon yields (Table S1) recorded in sample notes. Raman ID/IG 1.4 (PPY4), 1.5 (MPPY4); XRD and TEM qualitative. Skeletal density 2.1-2.2 g/cm3 (ref 53) and estimated powder packing densities 0.3 / 0.4 g/cm3: not stored.
- Figure 6 / S15 points below 150 bar at 25 degC: not extracted per protocol (only highest-pressure point at non-77 K); the table values at those pressures are extracted from Table S4.
- Figure S13 points below 20 bar: not extracted (25 degC).
