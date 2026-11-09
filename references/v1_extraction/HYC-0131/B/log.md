# HYC-0131 extraction log (agent B)

All H2 measurements in this paper are at 25 °C (298.15 K), so only the highest-pressure point of each isotherm is digitized. No H2 value is printed in a table or in text for a carbon sorbent, so no table_direct or text_direct rows.

## Sources extracted from
- Figure 4a (main-06.png, p. 14728), series "none (pristine AC)": highest-pressure closed marker gives M1 (I1). Archive: fig4a_none_pristine_AC_closed.json. 13 blobs for 14 counted closed markers: two overlapping closed markers near 0.08 and 0.11 MPa merge into one blob (36 px) and could not be separated. The legend marker was excluded by the ROI (y >= 166 px).
- Figure 3 (main-05.png, p. 14727), mixture of CB/Pt and styrene (5)-adsorbed AC: highest-pressure closed marker gives M2 (I2). Archive: fig3_styrene5_closed.json. 11 closed markers counted, 11 extracted. A 12-px blob of overlapping open (desorption) circles at P ≈ 0 was rejected by --marker-min-px 15.
- Figure 4a, series "naphthalene (10)": highest-pressure closed marker gives M3 (I3). Archive: fig4a_naphthalene10_closed.json. 7 extracted against 9 visible closed markers: the closed markers at about 0.32 and 0.68 MPa are hidden under the pyrene (13) markers and could not be separated.
- Figure 5a (main-07.png, p. 14729), series "16" triangles (5000 s exposure): M4 (I4). Archive: fig5a_16_5000s_triangles_closed.json. ROI x 440–570, y 140–207 px (P >= 1.6 MPa), so the archive does not include the 1000 s circles or the legend; 6 closed triangles counted and extracted in the ROI.
- Figure 5a, series "16" circles (1000 s exposure): M5 (I5). Archive: fig5a_16_1000s_circles_closed.json. ROI x 440–570, y 207–229 px; 6 closed circles counted and extracted in the ROI.
- Figure 5a, series "21": M6 (I6). Archive: fig5a_21_closed.json. 11 closed markers counted, 11 extracted.
- Figure 5a, series "22": M7 (I7). Archive: fig5a_22_closed.json. ROI x >= 365 px (P >= 0.5 MPa): 9 counted and 9 extracted; closed markers at about 0 and 0.31 MPa are partly hidden under series 18/20 and are outside the ROI.
- Figure 5a, series "23": M8 (I8). Archive: fig5a_23_closed.json. Tight ROI around the highest-pressure black marker (1 counted, 1 extracted). That marker is partly covered by the series 21 marker. The rest of series 23 is mostly hidden under series 19 and 21 and was not digitized.
- Table 1 (p. 14728): BET area and pore volumes of pristine AC ("none") and of the mixtures containing 9–13. Used as characterization on M1 and M3.
- Table 2 (p. 14729): BET area and pore volumes of the mixtures containing 14, 16 and 18–23. Used as characterization on M4–M8.
- Table S2 (si1-8.png, SI p. S8): BET area and pore volumes of the styrene (5) mixture. Used as characterization on M2.
- Section 2 text (pp. 14724–14725): materials, CB/Pt synthesis, organic loading, BELSORP HP instrument, H2 purity, BET range and pore-volume methods. Used for coding.

Axis calibration. Each axis was calibrated on its lowest and highest labelled ticks and checked on a third labelled tick. Fig 3: x 0/3.5 MPa, check 1.5; y 0/0.7 wt%, check 0.4 (1.2% relative error from raster jitter of the y ticks). Fig 4a: x 0/3.5, check 1.5; y 0/0.30, check 0.15. Fig 5a: x 0/3.5, check 1.5; y 0/0.36, check 0.18. Fig 1e: x 0/3.5, check 1.5; y 0/1.1, check 0.5.

## Values seen but not extracted
- Figure 1e (main-02.png, p. 14724), series "CB/Pt" (gray, carbon sorbent, 25 °C): the gray markers are almost entirely hidden under the "without CB/Pt" (MoO3) purple markers along 0 wt%. The highest-pressure gray marker could not be separated: the digitizer found no gray marker at tolerance 30, 40 or 50. No row was written. The text (p. 14725) says "MoO3 and CB/Pt did not adsorb any H2 gas". That statement gives no number, so it is not a row.
- Figure 1e, series "without CB/Pt" (MoO3 alone): not a carbon sorbent.
- Figure 1e, the CB/Pt + MoO3 mixtures and their legend "maximum values" 1.14 wt% (H/Mo = 1.65), 1.09 wt% (1.57), 0.99 wt% (1.42), 0.87 wt% (1.26), 0.63 wt% (0.92) and 0.22 wt% (0.32): not carbon sorbents (MoO3:CB:Pt = 5000:50:1 by weight, so the majority component is MoO3). Also not extracted: the text values H/Mo = 1.65, 1.57, 0.92 and the statement that the H0.92MoO3 measurement stopped at 0.18 MPa.
- Figure 4a, series biphenyl (9), anthracene (11) and phenanthrene (12): the highest-pressure markers overlap one another and the pyrene (13) markers. All lie below the 0 wt% line, and the digitizer found no separable marker for these colours. Not extracted, because schema v2 cannot hold a negative uptake (uptake_wt_pct >= 0).
- Figure 4a, series pyrene (13): digitized (fig4a_pyrene13_closed.json, 10 closed markers). The highest-pressure point is 3.0891 MPa, −0.00368 wt%, below zero. Not extracted, because the schema cannot store a negative uptake.
- Figure 5a, series 18 (anthraquinone): digitized for P >= 1.3 MPa (fig5a_18_closed.json, 6 markers). The highest-pressure point is 3.1017 MPa, −0.00258 wt%, below zero. Not extracted, because the schema cannot store a negative uptake. The text says the anthraquinone-adsorbed AC "did not physically adsorb H2 gas".
- Figure 5a, series 19 (tetrahydropyran) and 20 (cyclopentanecarboxylic acid): the highest-pressure markers (about 3.07 MPa) are hidden under the 23/21 markers (19) and the 22 marker (20). The digitizer found no separable marker. Not extracted.
- Text p. 14727: "maximum H/5 molar ratio was 2.05" (Figure 3 right axis). Text p. 14729: H/16 = 1.07 (1000 s) and 1.25 (5000 s). These are H-to-adsorbate molar ratios, a unit schema v2 has no field for. Converting them to a gravimetric uptake would need assumptions, so they are not extracted. The Figure 5a right axis (H/16) was not digitized.
- Text pp. 14726–14727: spillover rates and counts (844 H atoms per Pt nanoparticle per s; 1.69 million H atoms in 2000 s; 5.06 million and 1432 H atoms in 1 h and 1 s; abstract: at least 1430 H atoms per s, 5.15 million in 1 h). These are not H2 uptake values.
- Schemes 1–3 (pp. 14727–14728): GC conversions and yields from the autoclave method (4 MPa, 25 °C; for example 1 → 2/3, 4 → 3, 5 → 6/7, 8 → 3 1% and 11%, 14 → 15 90%, 16 → 17 61%). These are reaction yields, not H2 uptake values.
- Table S1 (si1-2.png): organic-compound adsorption temperatures, densities and saturation amounts (mmol per g AC). These are not H2 values; adsorption temperatures are cited in row notes.
- Figures 4b, 5b and S5: N2 isotherms at −196 °C (characterization only). Figures 1f, 1g, 2, S1–S4: XRD, XPS, SEM and TEM, not uptake.

## Samples with characterization but no H2 row
- Mixtures of CB/Pt and 9–13 (Table 1, SBET m2 g-1 / Vtotal / Vmicro / Vmeso cm3 g-1; normalized per g AC in brackets): 9 biphenyl 15 / 0.01 / 0.01 / 0.00 (26 / 0.02 / 0.01 / 0.01); 11 anthracene 6 / 0.01 / 0.00 / 0.00 (13 / 0.01 / 0.01 / 0.01); 12 phenanthrene 5 / 0.01 / 0.00 / 0.00 (10 / 0.01 / 0.00 / 0.01); 13 pyrene 2 / 0.00 / 0.00 / 0.00 (5 / 0.01 / 0.00 / 0.01).
- Mixtures with 14, 18, 19 and 20 (Table 2): 14 cyclooctanone 41 / 0.02 / 0.01 / 0.01 (66 / 0.04 / 0.02 / 0.02; autoclave only, no H2 isotherm); 18 anthraquinone 7 / 0.01 / 0.00 / 0.00 (13 / 0.01 / 0.01 / 0.00); 19 tetrahydropyran 735 / 0.34 / 0.32 / 0.02 (1040 / 0.49 / 0.45 / 0.03); 20 cyclopentanecarboxylic acid 126 / 0.06 / 0.04 / 0.02 (196 / 0.10 / 0.06 / 0.04).
- CB/Pt: no surface area is reported. Its H2 isotherm (Figure 1e) was not separable; see above.

## Other notes
- Total pore volume of pristine AC: Table 1 prints 0.89 cm3 g-1, while the text (p. 14726) and the Table S1 footnote print 1.59 cm3 g-1. The Table 1 value is stored on M1.
- isotherm_point_count is a visual count of markers on both branches. For I3 and I6–I8 it counts only the visible markers, because other markers are hidden by overlapping series. Each row's notes give the breakdown.
- Sample numbering covers only samples with rows, in order of first appearance: pristine AC (Section 2.1), then the styrene (Section 3.2), naphthalene (Section 3.3), 16, 21, 22 and 23 (Section 3.4) mixtures.
