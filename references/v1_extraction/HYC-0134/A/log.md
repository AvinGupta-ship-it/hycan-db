# HYC-0134 extraction log (agent A)

## Extracted
- main.txt/main-09.png, Fig. 10a (high-pressure PCI, 25 C, to 9 MPa): C@Pd90Co10-6 (I1) and C@Pd75Co25-6 (I2). Only the highest-pressure point of each isotherm (non-77 K rule). Both end points are open (desorption) symbols over the turning point; coded adsorption branch (see row notes). Digitized with a work copy of the page where the open ring/box was filled; archives digitizations/fig10a_*_end.json. Point counts are visible markers: red 14 (8 filled, 6 open), blue 13 (8 filled, 5 open); the filled marker under each open end point is hidden and not counted.
- main-09.png, Fig. 10b (low-pressure PCI, 25 C, to 0.1 MPa): C@Pd90Co10-6 (I3), C@Pd75Co25-6 (I4). Highest-pressure point only. Red end marker (0.1 MPa) is overprinted by the right frame line; disc re-fitted (work/discfit.py logic) and extracted from a work copy; archive fig10b_C@Pd90Co10-6_end.json. Blue end point extracted directly from the page (archive fig10b_C@Pd75Co25-6_end.json). I3 point count left empty (red markers overlap near the origin); I4 count 10 (two touching markers merged by the tool, counted visually).
- All four archives have status "unchecked": the paper prints no H2 value to check against, so the tool's check step cannot be run.
- Axis calibration: Fig. 10a x: 1 MPa px 788, 10 MPa px 1150 (frame), verify 5 MPa px 948.8; y: 0 px 907, 0.30 px 666.5, verify 0.20 px 747. Fig. 10b x: 0 px 744.5, 0.10 px 1148.5, verify 0.04 px 905.5; y: 0 px 1264.5, 0.020 px 969.5, verify 0.010 px 1117.
- Characterization: Tables 1 and 2 (main), Section 2.3 and 2.4 text, for C@Pd90Co10-6 and C@Pd75Co25-6.

## Seen, not extracted
- Fig. 10a/10b, all other plotted points (absorption and desorption branches below the highest pressure): not required for non-77 K isotherms.
- Fig. 10a desorption branch end points: same state as adsorption end point (turning point), no separate row.
- The text gives no numeric H2 uptake value and no table lists H2 uptake.
- Fig. 5, 9, S5 (N2 isotherms): not H2; not digitized.
- Fig. S6 (in-situ XRD under 1 bar H2): not uptake; C@Pd50Co50-6 and C@Pd75Co25-6 "no obvious hydrogen absorption".
- Samples with characterization but no H2 uptake value (no rows): C@Pd50Co50-4 (SSA 668, Vt 0.51, Vmicro 0.29, Vmeso 0.22), C@Pd50Co50-6 (848, 0.60, 0.35, 0.25), C@Pd50Co50-8 (803, 0.48, 0.31, 0.17), C@Pd75Co25-4 (681, 0.47, 0.29, 0.18), C@Pd75Co25-8 (791, 0.48, 0.31, 0.17), C@Pd90Co10-8 (789, 0.41, 0.32, 0.09); precursor-variant C@Pd90Co10-6 samples (Fig. 2a, 2b, TEM only). Table 1 composition also lists C@Pd50Co50-4/-6/-8. No H2 uptake measured for any of them.
- No non-carbon material measured.

## Coding decisions
- Sample numbering: S1/S2 assigned only to samples with rows, in order of first appearance (C@Pd90Co10-6 in Section 3.1 before C@Pd75Co25-6 in Table 1). Label taken from the Fig. 10 legend.
- synthesis_method = template_synthesis (soft-template EISA with F127, then pyrolysis); alternative would be carbonization.
- measuring_lab_id: H2 laboratory not named; corresponding author (Matei Ghimbeu) first affiliation names the institute with the abbreviation "UHA" only, so the institute was used.
- instrument_identified: low-pressure Autosorb IQ (Quantachrome) true; high-pressure "manual volumetric device" not stated home-built, false. calibration_described true for the 9 MPa runs only (sample volume from He pycnometer density).
- basis: "hydrogen capacity" with no basis named; uptake_type unspecified, basis_inferred excess by volumetric default.
- area_same_sample = yes (N2 measurement of the same C@PdCo-6 material, though H2 runs followed a H2 pretreatment/120 C degas).
