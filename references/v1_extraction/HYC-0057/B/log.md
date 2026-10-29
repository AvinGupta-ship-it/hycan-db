# HYC-0057 extraction log (agent B)

## Sources extracted
- Table 1 (main-05.png, journal p. 4): 7 rows, N-C-1 to N-C-4 and B-C-1 to B-C-3, H2 uptake at 77 K and 1.13 bar (footnote a), with BET, Langmuir and micropore areas, pore volume and micropore volume. Formulation columns (TEOS, sucrose, colloidal silica) used in material_description.
- Experimental text (main-05.png, journal p. 4): instruments (Micromeritics ASAP 2010 low pressure; cryostat with PCTPro-2000, Hy-Energy, high pressure), volumetric method, at least 100 mg sample, UHP H2 and He, degassing at 120 C under vacuum for 12 h, BET with N2 at 77 K, total pore volume at P/P0 > 0.97. These were coded on every row.
- Section 3.1 text (main-06.png, journal p. 5): "the result for the optimized material (sample N-C-2), figure 3, shows an uptake of ~4.2 wt%". Merged with the Figure 3 filled-series point closest to 30 bar (the text says saturation is reached "above about 30 bar"). One row, uptake_bound approximate, pressure digitized.
- Figure 3 (main-07.png, journal p. 6), N-C-2 at 77 K: filled markers (35 filled circles and a filled square at the origin), 36 markers counted and 36 extracted (archive fig3_N-C-2_filled.json), isotherm I1. Open markers (open circles and an open square near 0.2 bar): 24 separable markers extracted (fig3_N-C-2_open.json), isotherm I2. The figure has no legend and the paper does not say whether the two series are adsorption and desorption or repeat runs. Each series is coded as its own run, with branch adsorption (the protocol default) and replicates_reported false.
- Section 3.2 text (main-08.png, journal p. 7): "sample C-4 (2811 m2 g-1) absorbs 5.7 wt% at 25 bars" was merged with the Figure 8 C-4 77K point at 24.68 bar. "sample C-1 (1424 m2 g-1) absorbs only 2.8 wt%" (25 bar taken from the same sentence) was merged with the C-1 77K point at 25.32 bar. "sample C-4 ... absorbs only about 0.5 wt% hydrogen at 40 bars" (room temperature) was merged with the highest point of the C-4 RT series at 39.53 bar.
- Figure 8 (main-08.png, journal p. 7): the C-4 77K filled triangles (32 counted, 32 extracted, isotherm I3) and the C-1 77K filled squares (28 counted, 28 extracted, isotherm I4). Because the two series overlap at low pressure, rectangular regions had to be used, so each series is split over several archives: fig8_C-4_77K_pt1/pt2/main/end30/end31/end32.json and fig8_C-1_77K_pt1/pt2/main.json. For C-4 RT (open triangles) and C-1 RT (open squares), only the highest-pressure point is extracted (isotherms I5 and I6, 17 markers each). The archives fig8_C-4_RT.json and fig8_C-1_RT.json hold all the separable markers (17 and 16).
- Table 2 (main-09.png, journal p. 8): 18 values at 77 K and 40 bar for C-1 to C-18, with BET area and synthesis conditions. C-4 (5.68) and C-1 (2.81) were merged with the Figure 8 points at 39.89 bar and 39.25 bar. The other 16 are table_direct rows with no isotherm_id.

## Digitization method notes
- Figure 3 axes: the only x tick drawn on the bottom axis is at 10 bar (col 258). The 0 bar and 50 bar positions were taken from the centres of the tick labels (col 179, and col 570, which is also the right frame line) and checked against the 10 bar tick (relative error 1.0%, i.e. 0.2% of the span). The y axis was calibrated on the 0 tick (row 1271) and the 5 tick (row 1035.5) and checked on 3 (row 1130).
- Figure 8 axes: x was calibrated on 0 and 40 bar (cols 704 and 1106, where the ticks coincide with the frame lines) and checked on 20 bar (col 905). y was calibrated on 0 (row 872; only the tail of the tick shows because the origin marker hides the rest) and 6 (row 631), and checked on 3 (row 752).
- The digitizer matches markers by colour, so it cannot separate hollow markers from the black lines. For these, a derived copy of the page image with identical pixel geometry was made in the work directory, with the enclosed white interiors of the hollow markers painted a single colour, and the tool was run on that copy. Scripts: work/derive_fig3_open.py and work/derive_fig8_rt.py. On Figure 3, three enclosed gaps between the two crossing lines were excluded, and the interior of the open square, whose outline is not closed, was painted explicitly.
- In the C-4 77K series, three touching triangles at about 38.9, 39.4 and 39.9 bar came out as one blob. They were split at the minima of the column dark-pixel count in a derived copy of the image (work/derive_fig8_cluster.py) and digitized one at a time. The triangle on the right frame line (39.89 bar) includes frame pixels, so its centroid may sit about 1.5 px (about 0.04 wt%) high.
- Sanity checks passed (digitize_figure.py check) against values the paper prints:
  - Figure 3, both series: 4.2 at 30 bar.
  - C-4 77K: 5.7 at 25 bar; 5.68 at 39.89 bar.
  - C-1 77K: 2.8 at 25 bar; 2.81 at 39.25 bar.
  - C-4 RT: 0.5 at 39.53 bar, with a 10% tolerance because the paper says "about 0.5".
- Archives with no printed value to check against are still unchecked: fig8_C-4_77K_pt1, pt2, end30 and end31; fig8_C-1_77K_pt1 and pt2; fig8_C-1_RT.

## Markers seen but not extracted
- Figure 3 open series: about 6 open circles show only partly behind filled circles. Five appear as rims at about 35.7, 37.4, 38.8, 40.4 and 42.0 bar, and one sits just above the last filled circle at about 49.5 bar. The tool could not separate them, so they are not extracted; they are included in the I2 point count of 30. Further open circles may be completely hidden.
- Figure 8 C-1 RT: the open square at the origin overlaps the left frame and could not be separated. It is counted in the I6 point count of 17. The C-4 RT open triangle at the origin, if there is one, is hidden.
- Figure 8 RT series: only the highest-pressure point is extracted, as the protocol requires for non-77 K isotherms.

## Values seen but not extracted
- Abstract and Section 4 (main-02.png, main-09.png): "an excess hydrogen storage capacity of 4.2 wt%" with "nearly 2000 m2 g-1". This restates the N-C-2 result already extracted from Section 3.1, so it is not a separate row.
- Abstract and Section 4: "a specific surface area value of nearly 3000 m2 g-1 and an excess hydrogen adsorption capacity of nearly 5.8 wt%". No sample is named. It matches the Table 2 C-5 values (2943 m2 g-1, 5.75 wt%) rounded, so it is treated as a restatement and not given a separate row.
- Section 1.1 (main-03.png): "hydrogen adsorption of more than about 1-2 wt% at room temperature and 100 bars by any form of carbon material [45-49]". This is a literature statement, not a measurement in this paper.
- Section 1.4 (main-04.png): the authors' previous study [78] reports more than 2300 m2 g-1 and 2.0 cm3 g-1, with no H2 value. This is earlier work and no sample in this paper.
- Section 3.2 (main-06.png): "BET specific surface area values of up to 2943 m2 g-1" (C-5, the same as Table 2), "a ratio of micropore area to total surface area as high as 95%" and "macropore surface area near zero". These are not tied to a sample's row as numbers, so they are not extracted.
- Figure 9 (main-09.png): excess H2 at 77 K and 40 bar plotted against surface area. It is not an isotherm and its values are those of Table 2, so it was not digitized. The fitted line shows no further values.
- Figure 7 (main-08.png): BET area against KOH content at 700 and 800 C. This is characterization; the values match Table 2.
- Figure 5 (main-08.png): N2 adsorption isotherm of C-4 at 77 K (P0 = 0.998 bar). Not H2; no numeric characterization extracted.
- Figures 2 and 6 (main-07.png, main-08.png): pore size distributions for N-C-1 to N-C-4, B-C-3 (with an X50 magnified curve) and C-4. Characterization with no numeric pore diameter stated (the text says "a predominance of pores below about 3 nm"). The Figure 2b inset is a TGA of B-C-3 in air showing no silica residue.
- Figures 1 and 4: micrographs (FESEM and TEM) with no uptake values.
- No non-carbon reference materials were measured.
