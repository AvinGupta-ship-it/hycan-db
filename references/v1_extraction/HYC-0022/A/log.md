# HYC-0022 extraction log (extractor A)

Paper: Wang, Gao, Hu, JACS 2009, 10.1021/ja8083225. Rows written: 282 (validator: 0 errors; only the "Unspecified uptake_type" warning).

## Extracted from

- Table 1: sample names, SBET, pore volumes, carbon yields. Used for sample fields (yields in notes only).
- Table 2: 20-bar H2 uptake 5.63 wt% (isotherm I9) and 7.08 wt% (isotherm I10, volumetric 43.2 kg/m3). The I9 and I10 rows carry the table value (table_direct) merged with the plotted point.
- Main text, 1 bar values: Fig 4 last points I1 1.23, I2 1.70, I3 1.27, I4 2.23, I5 2.49 (text_direct, merged with plotted last points); G212 1.80 at 1 bar and 3.88 at 20 bar (main_text).
- SI text: G212 1.77 wt% at about 1 bar (data_location SI).
- Fig 4 (77 K, 0-1 bar, wt%): AC-K5, AC-K3, AC-C2, AC-C4, AC digitized with digitize_figure.py (archives Fig4_*.json, all check status passed).
- Fig 7 (20 bar isotherms, 0-20 bar): AC-K5 (11 pts, passed), AC-K3 (11, passed), AC-C2 (10, unchecked), AC (5, unchecked), AC-C4 (8, unchecked).
- SI Fig S1 (G212 volumetric, 0-1): 44 pts, passed. SI Fig S2 (G212 high pressure, 0-20 bar): 11 pts, passed.
- SI methods: gravimetric Rubotherm-type measurement with buoyancy correction; no model number given (instrument_identified false); calibration_described true (buoyancy correction); degassing conditions ambiguous.

## Method

Figures are monochrome at 150 dpi. Series were isolated in masked copies of the page images (same pixel geometry, kept in work/) and passed to the tool in markers mode. Axes calibrated from tick centroids with a third tick used as verification (errors under 0.3%). Merge rule: printed value matches plotted point within max(2%, 0.02 bar); row carries the printed value and a note "digitized: p bar, v wt%, archive: file.json".

## Values seen but not extracted

- SI Fig S3 (four AC-K5 replicate runs): markers overlap (filled square, open circle, open diamond, star, all black); no point-wise extraction. replicates_reported true for AC-K5 because of it.
- Fig 7: AC at 2, 4 bar (merged with C4) and 12, 14, 16, 18 bar (hidden by G212 rings); AC-C4 at 2, 4, 6 bar (overlapped by AC); AC-C2 at 2 bar (hidden under G212). G212 in Fig 7 not digitized (rings); G212 rows come from SI Fig S2, the same curve.
- Fig 7 AC, AC-C2, AC-C4 archives stay "unchecked": the paper states no value for them.
- Fig 4 dense region (P/Po below about 0.13) and the K3/K5 crossing zone (about 0.40-0.68, about 14 columns per series) unresolved. isotherm_point_count is a lower bound (K5 43, K3 43, C2 41, C4 43, AC 41; S1 44). One C2 marker near x 313 px lost. AC and C4 left zone (below about 0.16) not extracted. S1 dense region below P/Po 0.11 not extracted.
- Half-filled C2/C4 markers: centroid of the dark part (x biased about +1 px; C4 y about 1 px low).
- K5/K3 last-point pressures 0.9792/0.9795 vs printed 1 bar: deviation 0.021 bar, just over the 0.02 bar tolerance; merged anyway for consistency (borderline, flagged).
- Fig 4 and S1 x-axis labelled "Relative Pressure (P/Po)" while caption and text say 0-1 bar: x read as bar.
- Table 2 literature entries: AX-21 4.6 at 10 bar (ref 34); KUA-6 5.6 and Maxsorb-3000 5.2 at 40 bar (ref 35); CB850h 6.9 at 20 bar (ref 6); TC 5.3 at 20 bar (ref 7). Not this paper's measurements.
- Mokaya G212 3.96 wt% at 20 bar (ref 6 / SI ref 1): literature value.
- Figs 5, 6, 8, 9: derived, normalized or uptake-vs-property plots (Fig 8 20-bar values are in Fig 7; Fig 9 is uptake/SBET vs R value).
- Fig 3 (N2 isotherms), XRD R values, HRTEM: not H2 uptake.
- Table 1 carbon yields: notes only. G212 0.69 cm3/g pore volume: type and method not stated, not placed in a volume field.
- No sample without H2 uptake exists in the paper.
