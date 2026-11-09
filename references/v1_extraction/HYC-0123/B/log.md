# HYC-0123 extraction log (extractor B)

## Scope decision
- Carbon sorbents in this paper: GO and PG (Pt-loaded GO, Pt 18.9 wt% by EDS). Only PG has an H2 uptake value; it gives all 29 rows (sample HYC-0123-S1, isotherm I1).
- HPG0 is HKUST-1 (a MOF): not a carbon sorbent, not extracted.
- HPG5 and HPG10 are Pt@GO/HKUST-1 composites in which "The added GO consisted of 5 and 10 wt% of the final material weight" (p. 2161-2162). Their majority component is the MOF, so they are not carbon sorbents (§3) and are not extracted. (The EDS C contents of 54.51 and 52.89 wt% in Table S1 are elemental carbon, mostly from the BTC linker, not a carbon component.)

## Sources extracted
- Main p. 2164 (main-5), Fig. 6, low-pressure H2 isotherms at 77 K, series PG (black circles): 29 markers counted, all digitized (rows M1-M26, M28, M29; the point at 1.092 bar is merged into M27).
  - Calibration: x on ticks 0.0 (737.5 px) and 1.2 (1089.0 px), checked on 0.6 (913.5 px, error 0.14%); y on ticks 0.0 (1431.0 px) and 2.0 (1180.5 px), checked on 0.8 (1331.0 px, error 0.20%). Tick positions from pixel-column and pixel-row centroids.
  - Colour #000000, tolerance 40, ROI x 721-1101, y 1404-1440: 27 markers found. Two blobs (pixel counts 104 and 102, at about 0.19 and 0.90 bar) each held two overlapping markers. Each pair was separated by rerunning with two non-overlapping ROIs split at the blob midpoint, from its column profile (pair 1: x 784-793 and 794-802; pair 2: x 993-1001 and 1002-1012). Archives: fig6_PG_pair1_left/right.json and fig6_PG_pair2_left/right.json. The two merged centroids in fig6_PG.json are not used. 25 + 4 = 29 points, which matches the 29 markers counted in an overlay check. The split points have extraction_confidence 3, because their centroids come from slightly truncated markers (about 1 px, 0.004 bar).
  - Tool sanity check (`digitize_figure.py check`) against the text value 0.2 wt% at 1.1 bar with a 5% tolerance failed (digitized 0.163, 18.6%), and the tool marked fig6_PG.json 'discarded'. The cause is printed rounding: 0.2 is printed to one decimal, and 0.163 rounds to 0.2. The calibration residuals on the third ticks are 0.14% (x) and 0.20% (y). The tool refused an absolute tolerance of 0.05 (no check was run with it). fig6_PG.json was then regenerated with identical parameters (--overwrite), so its status now reads 'unchecked' and the 'discarded' record of the failed check is not in the archive. It is recorded here instead. No calibration or value was adjusted.
- Main p. 2164, Section 3.5 text: "Low-pressure hydrogen adsorption measurements ... were carried out at 77 K and 1.1 bar. As shown in Fig. 6, PG has a negligible adsorption capacity of 0.2 wt%". This is row M27 (text_direct, 1.1 bar), merged with the Fig. 6 point at 1.092 bar (the only plotted point within 0.022 bar of 1.1 bar).
- Main p. 2162, Section 2.2: instrument (ASAP 2020, Micromeritics) and degassing ("The GO and PG samples were outgassed at 80 C"; no duration stated for PG). The H2 purity (99.999%) also comes from this section.
- Main p. 2161, Sections 2.1.1-2.1.2: GO and PG synthesis and purification.
- Main p. 2163, Section 3.3: PG Pt content 18.9 wt% (EDS, Fig. S6).
- Main p. 2162-2163, Section 3.2: carboxyl band of PG at about 1700 cm-1.

## Values seen and not extracted
- Text p. 2164: "1.8 wt% for HPG0" at 77 K, 1.1 bar: HKUST-1, not a carbon sorbent.
- Fig. 6: series HPG0, HPG5, HPG10 at 77 K (to about 1.15 bar): not carbon sorbents.
- Fig. 7 (bar chart, not an isotherm): measured and "hypothetical" uptakes at 77 K and 1.0 bar for HPG0, HPG5, HPG10. These are not carbon sorbents, and the hypothetical values are computed from component fractions.
- Text p. 2165: HPG0 0.41 wt% at 80 bar and 298 K; HPG5 0.77 wt% at 80 bar; HPG10 0.15 wt%; "1.9-fold enhancement in HPG5"; "nearly twofold increase" (Conclusions). All are for samples that are not carbon sorbents.
- Fig. 8 (298 K, to 80 bar; HPG0, HPG5, HPG10) and Fig. S11 (298 K, to about 1.2 bar; HPG0, HPG5, HPG10): not carbon sorbents.
- Literature values cited, not measured here: MOF-5 and HKUST-1 "well below 0.4 wt% at 298 K and 65 bar" [3]; HKUST-1 "~0.27 wt%" [10]; MOF-5 0.28 wt% (65 bar) [3]; MIL-101 0.43 wt% (80 bar) [45]; Pt-MWCNTs@MOF-5 "4.2 times" at 298 K and 100 bar [42].
- Table S2 / text p. 2164: BET areas 937, 848 and 676 m2/g, Vtot, Vmeso, Vmic and Vmeso/Vtot for HPG0, HPG5 and HPG10 (the text prints the units as "cm2 g-1"): not carbon sorbents.
- Table S1: EDS compositions of HPG0, HPG5 and HPG10: not carbon sorbents.
- Characterization of GO, a carbon sorbent with no H2 uptake value, so no row: XRD (002) at 2θ = 9.76°, interlayer spacing 0.91 nm (p. 2162, Fig. S1); IR (Fig. S2); SEM (Fig. S4).
- PG characterization not in a numeric field: XRD Pt (111), (200), (220), (311) peaks at 2θ = 39.6, 46.2, 67.4 and 81.4°; Fig. 5 N2 isotherm of PG ("significantly low and negligible porosity"; no area or pore volume is given for PG); TEM (Fig. S5). Fig. 5 is an N2 isotherm and was not digitized.

## Coding notes
- PG has no reported surface area. The dictionary would code this sample not_reported, since the paper reports areas for its other samples. The validator rejects not_reported because no row of this paper carries an area, so the rows use none, with an explanation in notes.
- Basis is not named, so basis_stated = false. ASAP 2020 is coded volumetric_sieverts, which makes basis_inferred = excess by the instrumental default. calibration_described = false (free-volume determination not described); replicates_reported = false.
- sample_id numbering counts only samples with rows, so PG is S1.
- measuring_lab_id: corresponding author A. Yuan (marked *), affiliation c, Jiangsu University of Science and Technology.
