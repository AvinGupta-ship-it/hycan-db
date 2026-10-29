# HYC-0069 extraction log (agent B)

Attia et al. 2020, Int. J. Hydrogen Energy, 10.1016/j.ijhydene.2020.03.004. I read the page images only (main-01 to main-11, si1-1 to si1-4). The output has 148 rows.

## Sources used

- main p.3, Experimental, "Materials characterization": N2 adsorption at 77 K (Autosorb-iQ2-Xr); BET areas; total pore volume (SPV/TPV) from N2 at P/Po = 0.99; micropore volume by DR; PSD by NLDFT (cylinder pore, adsorption branch). Samples for N2 were degassed at 4-6 x 10^-6 kPa, at 80 C, or 200 C for SBL-CO-PP-C-7. The BET P/Po range and consistency criteria are not stated.
- main p.3, Experimental, H2 measurement: automated Sieverts-type apparatus, PCTPro-E&E with microdoser, from Setaram. "~100 mg" of sample degassed 12 h at 80 C, or 200 C for SBL-CO-PP-C-7 and -C-20, "in vacuum" (no end pressure given). Isotherms 0-20 bar at 298 K and 77 K, ~0.7 ml cell, 99.999% gas. Free-volume calibration is not described, and there are no replicates or uncertainties. I used this passage for the method fields of S2 and S3.
- main p.2-3, Experimental, syntheses: SBL-PNP-0.25-4-750; CO-PP-0; SBL-CO-PP-7 and -20 (and -5, -10, -15); SBL-CO-PP-C-7 and -C-20 (KOH 2:1, 800 C, N2, 1 h). I used these for the material fields.
- main p.6, text: characterization of SBL-PNP-0.25-4-750 cited from ref. [7] (SSA 2635 m2/g, TPV 1.69 cm3/g, micropore volume 1.41 cm3/g, pores 0.92 nm and 2 nm). These go on the S1 rows.
- main p.7, Table 1: textural properties of SBL-CO-PP-C-7 (2679, 1.335, 1.150, 0.185, 0.8/2.6) and SBL-CO-PP-C-20 (2330, 1.270, 0.780, 0.490, 1.9). These go on the S2 and S3 rows. The footnote letters c and d are swapped, and footnote d says the micropore volume is by the "MP method" while the Experimental section says DR. I coded DR.
- main p.7, Table 2: H2 values of SBL-CO-PP-C-7 (4.4 wt% at 77 K, 0.170 wt% at 298 K) and SBL-CO-PP-C-20 (4.1, 0.130), all at 20 bar. These give 4 table rows, each merged with a plotted marker (see the Fig. 6 entries).
- main p.7, text: "4.4 and 4.1 wt% at 77 K and 20 bar". main p.8, text: "0.17 wt% compared to 0.13 wt%". Table 4 (SBL-CO-PP-C-7, 4.4 wt% at 20 bar), the abstract, the highlights, the conclusion and si1 p.4 all print the same values as Table 2, so they add no extra rows.
- main p.8, text: EDS composition of SBL-CO-PP-C-7 (C 52.01, N 36.22, O 7.80 at.%) and SBL-CO-PP-C-20 (C 56.10, N 43.90 at.%, no O). These give the dopant fields. By mass, carbon is only about 50% (C-7) and 52% (C-20). I treated both as carbon sorbents (`doped_carbon`) because they are carbonized, KOH-activated porous carbons with no non-carbon phase. This is flagged for the reconciler.
- main p.7, Fig. 6a (77 K): digitized every separable marker of SBL-CO-PP-C-7 (green) and SBL-CO-PP-C-20 (magenta), both branches. Details follow.
- main p.7, Fig. 6b (298 K): digitized only the highest-pressure marker of SBL-CO-PP-C-7 (black) and SBL-CO-PP-C-20 (magenta). Each falls within 0.4 bar of 20 bar, so it was merged with its Table 2 value.
- si1 p.4, text below Fig. S2: SBL-PNP-0.25-4-750 "has 3.6 wt.% (77 K) and 0.115 wt.% (298 K)", previously reported (JMCA, 6, 23087-23100, 2018). This gives 2 rows. No pressure is printed with these values, so `pressure_unstated = true`.

## Figure digitization (Fig. 6)

- Calibration, Fig. 6a. Pressure axis: x = 0 at px 307, x = 25 at px 617, checked on 10 at px 431. Uptake axis: y = 0.0 at px 1446, y = 5.0 at px 1226, checked on 2.5 at px 1336. Both checks gave relative error 0.
- Calibration, Fig. 6b. Pressure axis: 0 at px 677, 25 at px 987, checked on 10 at px 801. Uptake axis: 0.00 at px 1434, 0.20 at px 1249, checked on 0.10 at px 1342 (relative error 0.54%).
- Fig. 6a markers overlap heavily. The squares are 9 px. Closed squares (adsorption) are drawn first, and white-filled open squares (desorption) are drawn on top in descending-pressure order. Magenta is drawn over green.
- I could not get one marker per point from a single run per series, because the tool merges touching markers into one blob. Instead, I located each marker's 9x9 box programmatically, from its visible corners and outlines, checking consistency with the drawing order. I then ran `digitize_figure.py extract --mode markers --open-px 0` once per marker, with `--roi` set to that box.
- As a result, `digitizations/` holds one archive per marker, named `fig6a_<series>_<ads|des>_<nn>.json`, numbered from the lowest pressure, and `fig6b_<series>_ads_<nn>.json`. This is not one file per series.
- In 12 boxes, a fragment of a neighbouring marker formed a second component. I reran those with `--marker-min-px 16`, which drops the fragment; the tool records it as rejected in the archive.
- Acceptance rule: I accepted a marker only if the tool returned exactly one component, with its centroid within 2 px of the box centre on both axes (below 1% of either axis span). Otherwise the marker is listed below as not separable.
- Count, SBL-CO-PP-C-7 at 77 K: 35 closed and 28 open markers, so `isotherm_point_count` = 63. Thirty closed markers and all 28 open markers became rows; the 20 bar closed marker is merged into the Table 2 row.
- Count, SBL-CO-PP-C-20 at 77 K: 41 numbered closed markers, plus 2 more closed markers whose presence is certain from uncovered pixels in the low-pressure stack, and 47 open markers, so `isotherm_point_count` = 90.
- These counts are lower bounds. A marker drawn exactly behind another of the same colour, or hidden under the SBL-CO-PP-C-20 stack, cannot be seen. In particular:
  - there may be further closed magenta markers near (319,1358) px (1 px of evidence) and in the gap near 1.0-1.4 bar;
  - there may be further green markers under the magenta stack below 0.5 bar.
- Fig. 6b counts: SBL-CO-PP-C-7 has 15 closed markers and SBL-CO-PP-C-20 has 17. No open markers are visible.
- I did not run the tool's optional `check` subcommand. Each single-marker archive covers only its own pressure, so `check` cannot be run at the printed 20 bar. The comparison with the printed value is in the notes of each merged row instead.
- Merging with Table 2 at 77 K:
  - SBL-CO-PP-C-7: the closed marker at 20.26 bar (4.367 wt%) is the plotted point closest to 20 bar, so Table 2's 4.4 wt% replaces it.
  - SBL-CO-PP-C-20: the open marker at 19.92 bar is closer to 20 bar than the closed marker at 19.72 bar (4.080 wt%). I merged with the closed (adsorption) marker because Table 2 is an adsorption uptake, and kept the 19.92 bar open marker as its own desorption row.

## Plotted markers not extracted (with reason)

- Fig. 6a, SBL-CO-PP-C-7 closed marker 01 (box 303-311 x 1437-1445 px). Only 3 px are visible beside the magenta stack, and the tool rejected the group as too small. No value.
- Fig. 6a, SBL-CO-PP-C-7 closed marker 02 (box 304-312 x 1416-1424). Only a 1-px strip is visible; the centroid is 4.0 px off the box centre. The tool gave -0.242 bar, 0.591 wt%. Not separable.
- Fig. 6a, SBL-CO-PP-C-7 closed marker 03 (box 305-313 x 1397-1405). The centroid is 3.6 px off; the tool gave -0.132 bar, 1.039 wt%. Not separable.
- Fig. 6a, SBL-CO-PP-C-7 closed marker 04 (box 306-314 x 1380-1387). The centroid is 2.2 px off; the tool gave 0.067 bar, 1.428 wt%. Not separable.
- Fig. 6a, SBL-CO-PP-C-7 closed marker 32 (box 519-526 x 1254-1262). Only its top rows show above an open square, and the centroid is 2.1 px off; the tool gave 17.32 bar, 4.320 wt%. Not separable.
- Fig. 6a, SBL-CO-PP-C-20 closed marker 01 (box 303-311 x 1440-1448). The tool gave 0.0 bar, 0.0455 wt%: the marker is centred on the zero-pressure tick. The validator rejects a pressure of 0, and no positive value can be read, so there is no row. Its archive is in the work directory only.
- Fig. 6a, SBL-CO-PP-C-20 open marker 01 (box 303-311 x 1367-1375). The tool gave 0.0 bar, 1.7045 wt%, with the same problem: zero pressure, so no row.
- Fig. 6a, SBL-CO-PP-C-20: 2 closed markers inferred in the low-pressure stack (around rows 1416-1425 and 1431-1440 px, near 0.4 and 0.2 wt%). Their pixels prove they exist, but their positions are not pinned by any visible corner. Counted, not extracted.
- Fig. 6a, CO-PP-0, SBL-CO-PP-7 and SBL-CO-PP-20 curves: not digitized, because these are not carbon sorbents (see below).
- Fig. 6b: only the highest-pressure marker of each carbon is extracted, as the protocol requires at 298 K. The other 14 (C-7) and 16 (C-20) markers, and the CO-PP-0, SBL-CO-PP-7 and SBL-CO-PP-20 curves, were not digitized.

## Values seen but not extracted (with reason)

### Not carbon sorbents (§3)

CO-PP-0 is an uncarbonized cross-linked polymer. SBL-CO-PP-7 and SBL-CO-PP-20 are uncarbonized polymer composites containing only 7 and 20 wt% activated carbon, so their majority component is the uncarbonized polymer.

- main p.7 Table 2:
  - CO-PP-0: 1.3 wt% at 77 K and 0.017 wt% at 298 K (20 bar); CH4 1.30 mmol/g.
  - SBL-CO-PP-7: 1.6 and 0.030 wt%; CH4 1.75.
  - SBL-CO-PP-20: 2.2 and 0.050 wt%; CH4 3.00.
- main p.7 text: CO-PP-0 1.3 wt% at 77 K and 0.017 wt% at 298 K; SBL-CO-PP-20 2.2 wt% at 77 K; "SBL-CO-PP-2 (2.2 wt%)", a misprint for SBL-CO-PP-20.
- main p.7 Table 3: SBL-CO-PP-20 2.2 wt% and SBL-CO-PP-7 1.6 wt% at 77 K, 20 bar.
- Their characterization:
  - main p.7 Table 1, CO-PP-0: BET 695 m2/g, Vtot 0.857, Vmicro 0.264, Vmeso 0.593 cm3/g, DDFT 1.3/2.6 nm.
  - main p.7 Table 1, SBL-CO-PP-7: 820, 0.932, 0.355, 0.577, 1.2/3 (broad).
  - main p.7 Table 1, SBL-CO-PP-20: 1421, 0.857, 0.616, 0.241, 0.8/1.5. The abstract prints 1420 m2/g for this sample.
  - main p.4 text: TGA char yields 11, 25 and 73 wt%.
  - si1 p.3 Table S1: BET areas of SBL-CO-PP-5 (745), SBL-CO-PP-10 (122) and SBL-CO-PP-15 (76 m2/g). These are polymer composites with no H2 value.

### Samples with characterization but no H2 value

- SBL-PNP-0.25-4-750-2-800: BET 1054 m2/g (si1 p.3 Table S1) and TPV 0.61 cm3/g (main p.6). No row.
- SBL (carbonized sugar beet leaves) and SBL-PNP: synthesis intermediates with no data. No row.

### Literature comparison values

These are other groups' materials, cited from other papers and not measured here.

- main p.7 Table 3, H2 at 77 K:
  - Hypercross-linked polyaniline: 2.2 wt%, 30 bar [18].
  - Nanoporous PT4AC: 2.2, 60 bar [19].
  - PmCB-3: 2.1, 80 bar [25].
  - PPYsvp2h: 2.2, 90 bar [21].
  - Nanoporous Co-PBS-350C: 1.24, 80 bar [41].
  - PIM-1: 2.6, 100 bar [42].
  - UPO16: 2.2, 30 bar [43].
- main p.8 Table 4, H2 at 77 K:
  - Norit R0.8: 2.9, 20 bar [45].
  - CT: 1.4, 19 bar [46].
  - PPY2 Activated: 3.3, 20 bar [47].
  - ACC: 3.1, 72 bar [48].
  - UCs-90-2: 3.65, 20 bar [49].
  - FLG-800: 2.0, 60 bar [50].
  - Ch900/700/3: 4.6, 40 bar [51].
  - ACBS14: 5.0, 40 bar [52].
  - SAC-02: 3.8, 60 bar [53].
  - WC-ACHF-1%: 4.5, 100 bar [54].
- main p.8 text, 298 K and 20 bar:
  - Norit R0.8: 0.15 wt% (SSA 1384) [45].
  - Takeda 4A: 0.1 wt% (SSA 397) [45].
  - MOF-5: 0.1 wt% (SSA 2360) [45].
  - MIL-101: 0.15 wt% (SSA 3293) [45].
  - MIL-53: 0.15 wt% (SSA 902) [45].
  - MOF-184-Mg: 0.15 wt% (SSA 3154) [13].
  - The MOFs are not carbon sorbents in any case.
- main p.6 text: literature SSAs AC-CPD84% 1418 [37], P3KC 1860 [38], SDBPy-700 2098 [39] and NPCM-700 1958 m2/g [40].
- main p.9 Table 5: literature CH4 values. Not H2.

### Other values

- main p.8 Fig. 7 and si1 p.4 Fig. S2: uptake against BET SSA, not isotherms. The values shown are those of Table 2, plus SBL-PNP-0.25-4-750, whose value comes from the si1 p.4 text.
- si1 p.4 text:
  - "ca. 2600 m2/g should be close to 5.2 wt%": a Chahine-rule prediction, not a measurement.
  - "the difference between two samples is only 0.055wt%": a computed difference, not a measurement.
  - "(over 25 bar)" and "(@77 K, 25 bar)": no value attached.
- CH4 data are not H2, so none were extracted: Table 2 CH4 column (C-7 8.15, C-20 6.60 mmol/g), text, highlights and abstract (8.15 mmol/g), Fig. 8 (CH4 isotherms), Fig. 9 (CH4 cycling, 98% retention).
- main p.6 Fig. 5 (N2 isotherms and PSD), si1 p.2 Fig. S1 (N2 isotherms), main p.4 Fig. 2 (FTIR) and Fig. 3 (TGA), main p.5 Fig. 4 (SEM): characterization only, no H2 values.
