# HYC-0071 extraction log (extractor B)

Rallapalli et al., Int. J. Energy Res. (published online 2011), "Activated carbon @ MIL-101(Cr)". Inputs: page images main-1..8, si1-1..6. 45 rows written, all for one carbon sorbent: the commercial activated carbon (HYC-0071-S1, label "Activated carbon", Table I).

## Scope decision
- Carbon sorbent extracted: activated carbon WS-480 (Chemviron carbon), measured by the authors (Table I, Fig. 6).
- Not extracted, not carbon sorbents (§3): MIL-101(Cr) (a MOF), and AC@MIL-101/A, /B, /C, /D. Section 2.4 gives their carbon contents as 0.63, 1.25, 1.87 and 2.5 wt%, so the main component by mass is the MOF. HKUST-1A and HKUST-1B (SI) are MOFs.

## Sources extracted from
- main p. 750 (main-5.png), Table I, row "Activated carbon": BET 946.96 m2/g, pore volume 0.48 cm3/g, pore width 0.90 nm, H2 uptake 3.7 wt% and 414.4 cc/g at 77 K and up to 6000 kPa. This is row M21. It is merged with the Fig. 6 adsorption point at 5964.23 kPa, the plotted point closest to the printed 6000 kPa; the 6070.46 kPa point is also within 2% but farther away. Pressure is stored as 60 bar.
- main p. 751 (main-6.png), text: "The hydrogen uptake capacities obtained for AC and four composite materials ... are 3.7, 10.1, 8.4, 7.2, and 6.1 wt%". The AC value is the same as Table I (M21), so it gets no row of its own.
- main p. 748 (main-3.png), Sections 2.1 and 2.5: AC source (WS-480, Chemviron carbon); gas purity 99.999%; N2 BET on ASAP 2020 at 77.4 K; BET area, BJH pore diameter (desorption) and single-point pore volume; H2 measured on BELSORP-HP (BEL Japan) at 77.4 K up to 6000 kPa; degassing at 1 K/min to 393 K under 6.7 x 10^-2 Pa, held 10 h; "errors ... within the range of +/-0.5%". It is unclear whether this means wt% or relative %, so it was not stored as uncertainty_wt_pct, but replicates_reported = true. The free-volume determination is not described. No sample mass and no BET P/P0 range are given.
- main p. 751 (main-6.png), Fig. 6, series "Activated Carbon": digitized, both branches (below).

## Fig. 6 digitization (activated carbon, 77 K)
- Calibration on the page image main-6.png. x: 0 kPa at px 687 and 7000 kPa at px 1056, checked at 3000 kPa = px 845.5 (predicted 3006.8, 0.23%). y: 0 wt% at px 1345 and 11 wt% at px 1058, checked at 5 wt% = px 1215 (predicted 4.983, 0.35%). Tick positions were read from pixel rows and columns.
- All six series are black (#231f20) and no rectangle isolates the AC curve, so the region was set with a band about 17 px wide that follows the AC curve, for x = 712 to 1015 px. Every pixel outside the band was whitened in a copy of the page, with pixel positions unchanged (work/prep_inputs.py).
- Adsorption branch (filled down-triangles): digitize_figure.py markers mode, 3-px opening, on the band-masked page. 22 markers were extracted (599 to 6070 kPa). Archive digitizations/HYC-0071_fig6_activated_carbon_ads.json. The tool check against Table I (3.7 wt% at 6000 kPa) passed: 3.669, 0.83%.
- Desorption branch (open down-triangles): open symbols are drawn white-filled on top of the filled ones. Their white interiors, found by hole filling of the ink mask inside the band (components of 4 px or more), were painted #231f20 on a white page. digitize_figure.py markers mode (--open-px 1, --marker-min-px 4) gave the centroid of each interior, which is the triangle's centre. 23 markers were extracted (673 to 5824 kPa). Archive digitizations/HYC-0071_fig6_activated_carbon_des.json. Its status is left "unchecked": the only value the paper states (6000 kPa) lies outside the branch's extracted range.
- Marker count: I count 46 AC markers at x >= 712 px (about 474 kPa and above): 23 filled and 23 open. The tools extracted 22 filled and all 23 open. isotherm_point_count = 46 counts only these markers, so it is a lower bound for the whole run.
- Markers not separated:
  - One filled marker at about 822 px (about 2.56 MPa). Only its right third shows; the rest is under the open marker at 2517 kPa, and its centre cannot be located. Counted but not extracted.
  - The filled markers are spaced about 13 px apart. The gap between 795.5 px and 835.4 px suggests a further filled marker at about 808 px (about 2.30 MPa), hidden under the open marker at 2324 kPa. No part of it can be told apart from that open marker, so it is neither counted nor extracted.
  - All AC markers below about 474 kPa (x < 712 px). They overlap the low-pressure points of the five MOF/composite series and could not be told apart or counted. Two candidates were seen and not used: a filled blob at px (703, 1298) and an open interior at px (709.5, 1294).
- Branch assignment: the Fig. 6 caption says "adsorption-desorption isotherms" and the legend shows filled symbols only. Filled = adsorption and open = desorption follows the same authors' SI Fig. 3a/3b legends ("ads" filled, "des" open).
- The other five Fig. 6 series (MIL-101, AC@MIL-101/A-D) were not digitized: they are not carbon sorbents.

## Values seen but not extracted
- Table I, MIL-101: BET 2887.39 m2/g, 1.45 cm3/g, 2.15 nm, 6.36 wt%, 712.3 cc/g. Not extracted: MOF. The text on p. 751 gives "6.3 wt%" for MIL-101.
- Table I, AC@MIL-101/A: 3555.61, 1.75, 2.61, 10.1 wt%, 1131.2 cc/g. Not extracted: composite, about 99.4 wt% MOF.
- Table I, AC@MIL-101/B: 2767.93, 1.45, 2.28, 8.4 wt%, 940.8 cc/g. Not extracted: composite, mostly MOF.
- Table I, AC@MIL-101/C: 2402.67, 1.17, 2.25, 7.2 wt%, 806.4 cc/g. Not extracted: composite, mostly MOF.
- Table I, AC@MIL-101/D: 1856.35, 0.90, 2.16, 6.1 wt%, 683.2 cc/g. Not extracted: composite, mostly MOF.
- Summary (p. 746): AC@MIL-101/A, 10.1 wt% at 77.4 K up to 6000 kPa. Not extracted: composite. The text on p. 751 also gives a 58% increase over MIL-101, a derived comparison.
- Introduction (p. 746): Rowsell et al., 1.62, 1.32 and 1.25 wt% for IRMOF-11, IRMOF-1 and MOF-177, with Langmuir areas 1910, 3360 and 4530 m2/g. Not extracted: literature MOF values from other work.
- Introduction (p. 747): MIL-101 literature BET 4100 +/- 200 and Langmuir 5900 +/- 300 m2/g; 6.1 wt% (6 MPa, 77 K) [36]. Not extracted: literature MOF values.
- Section 2.4 and Fig. 2 (TGA): carbon contents 0.63/1.25/1.87/2.5 wt%; water contents of MIL-101, AC@MIL-101/A and /D of 35%, 20% and 5%. No H2 values.
- Fig. 1 (PXRD), Fig. 3 (TEM): no H2 values.
- Fig. 4 (N2 isotherms of all six materials, including AC, at 77.4 K): not an H2 isotherm and not digitized. The AC N2 isotherm is Type I (text p. 749).
- Fig. 5a/5b (NLDFT N2 and DFT CO2 pore size distributions of MIL-101 and composites): no AC data. Composite pore sizes from the text (1.7-2.5 and 2.9-3.4 nm; 0.45-0.61 nm; 0.61-0.64 nm) belong to MOF samples.
- SI Table 1, HKUST-1A: BET 1342.52 m2/g, total pore volume 0.64 cm3/g, 3.27 wt%. Not extracted: MOF.
- SI Table 1, HKUST-1B: BET 1483.28 m2/g, total pore volume 0.73 cm3/g, 3.95 wt%; the SI text says 3.96 wt%. Not extracted: MOF.
- SI Fig. 3a/3b: H2 isotherms of HKUST-1A (77 K, up to 6000 kPa) and HKUST-1B (77 K, up to 2700 kPa). Not digitized: MOF.
- SI Fig. 1 (PXRD), SI Fig. 2 (N2 isotherms of HKUST-1A/B): no H2 values for carbon.
- SI text: literature HKUST-1 values of 3.2 wt% (77 K, 88 bar, ref. 2), 3.3 wt% (77 K, 25 bar, ref. 3), 3.6 wt% (77 K, 10 bar, ref. 4), 3.6 wt% (77 K, 50 bar, ref. 5) and 4.1 wt% (77 K, 26 bar, ref. 6). Not extracted: literature MOF values from other work.
