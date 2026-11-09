# HYC-0118 extractor A log (extraction date 2026-11-02)

## Extracted from
- main.pdf p.5 Table 1: QExcess at 1 bar and 60 bar and QTotal at 60 bar, five samples (15 rows; 10 of them merged with plotted points, see below), plus SSA/pore-volume characterization on every row.
- main.pdf p.5 Fig. 5b (77 K, 0-60 bar, QExcess): digitized, five series. Last marker of CS-C, CS-SE, CS-SE-AC, CS-AC merged into the Table 1 60 bar rows (paper says Fig. 5 values are summarized in Table 1; values within 3%).
- main.pdf p.5 Fig. 5a (77 K, 0-1 bar, QExcess): digitized, five series. Not merged with the 1 bar table values (last marker about 0.975 bar, outside 0.02 bar of 1 bar; CS-SE-AC marker about 2.49 vs table 2.76).
- si1.pdf p.2 Fig. S2 (77 K, QTotal): digitized, five series; last marker of each merged into the Table 1 QTotal rows.
- si1.pdf p.3 Fig. S3 (298 K, QExcess): highest-pressure marker of each of five isotherms (5 rows).
- Sample order: CS-C (S1), CS-SE (S2), CS-SE-AC (S3), CS-AC (S4), CS-AC-SE (S5), order of first appearance in Section 2.1.

## Digitization notes
- Legends were painted white in copies of the page images (work dir) before extraction so legend markers were not picked up; archives record those copies as source_image. Axis ticks located by sub-pixel centroids; each axis calibrated on lowest and highest labelled ticks and checked on a third (all checks passed).
- Marker count did NOT equal the count on the plot for most series: markers overlap (green, blue, red under other series in Fig. 5a/5b; very dense markers below about 10 bar in Fig. 5b, S2, S3 and below 0.1 bar in Fig. 5a). Not separated and not extracted: low-pressure cluster of every series in 5a/5b/S2/S3 (purple, black especially), origin marker of CS-SE-AC in 5a, most hidden markers of CS-SE and CS-AC in 5a, CS-SE-AC S2 markers below 4.5 bar, all S3 markers except the last.
- Tool detections lying between markers (line fragments) were removed after overlay inspection: Fig. 5a green 0.3773, 0.6669, 0.7691, 0.8938, 0.9556 bar; red 0.9354; black 0.6134, 0.6590, 0.8777. Fig. 5b green 6.57 (merged blob) and 48.39; red 42.23, 47.69, 51.30, 56.67; black 13.44, 24.27, 29.11, 32.46, 49.27, 56.23. Fig. S2 black 46.48, 55.10. Archives still hold the unfiltered tool output. Kept points not guaranteed to be on a marker for ambiguous low-pressure ones.
- isotherm_point_count values are visual estimates (overlapping markers); S2 counts equal 5b counts.
- S3 CS-AC archive holds 2 detections (58.47 bar is a line fragment, n=16 px); the 59.70 bar point was used.
- Last Fig. 5b/S2 markers lie at about 60.5-61.5 bar (beyond the 60 tick); table pressure 60 bar used on merged rows, digitized pressure in notes.

## Values seen, not extracted or flagged
- Table 1 CS-AC-SE QExcess 60 bar = 6.12 (also text) vs Fig. 5b last marker about 5.77: kept separate rows (table row value_kind fitted_extrapolated by maximum rule; digitized point separate).
- Text says QTotal range 1.89-11.16 wt%; Table 1/Fig. S2 give CS-C 1.86. Table value used.
- Table 1 CS-AC 1 bar printed "1.9"; Fig. 5a end about 1.82.
- Text: saturation not approached in QTotal, "QTotal greater than 11.16 wt% can be obtained above 60 bar" (no value extracted).
- Heat of adsorption 4.01-7.98 kJ/mol, Fig. S4 (not uptake, not digitized); Fig. 6 and Fig. S5 (uptake vs surface area/pore volume correlations, not digitized; their values duplicate Table 1); V<3 nm and V<5 nm in Fig. S5 labels (caption/axes differ from V<2 nm and V<4 nm of Table 1; not extracted).
- Fig. 4 (N2 isotherms, PSD) is not an H2 isotherm; not digitized. EDS Si at% (Fig. 2) recorded in notes only.
- No other material measured. No sample mass, BET range, free-volume calibration or uncertainty stated.
- 298 K uptakes are shown only in Fig. S3 (no table value).
