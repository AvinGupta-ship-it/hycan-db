# HYC-0027 extraction log (agent B)

Paper: Parambhath, Nagar, Ramaprabhu, Langmuir 2012, 28, 7826-7833 (doi 10.1021/la301232r) and its SI (si1, 5 pages). Read from page images only. 24 rows written.

## Sources extracted from

- si1-4 (SI p. 4), Table S1 ("weight percentage of hydrogen stored by different specimens at 25 °C and 2 MPa, 4 MPa"): all 10 values extracted (M1, M2, M6, M7, M12, M13, M17, M18, M23, M24).
- main-4 (p. 7829), Figure 5b (Pd-N-HEG; 100, 75, 50, 25 °C and Desor. 25 °C): highest-pressure point of each isotherm. The 25 °C top point is the Table S1 4 MPa value (merged, M2); 50/75/100 °C digitized (M3-M5).
- main-4 (p. 7829), Figure 5a (N-HEG): same; 25 °C top merged with Table S1 4 MPa (M13); 50/75/100 °C digitized (M14-M16).
- si1-4 (SI p. 4), Figure S5a (HEG): highest-pressure point of the 25/50/75/100 °C isotherms digitized (M8-M11); the 25 °C top is at 37.1 bar, not within 2% of 4 MPa, so Table S1 4 MPa is a separate row.
- si1-4 (SI p. 4), Figure S5b (Pd-HEG): same (M19-M22).
- main-2 (p. 7827), Experimental: synthesis, Sieverts method, calibration, activation/degassing, sample mass, H2 purity (coded on rows / in notes).
- main-4 (p. 7829) text: "maximum capacity of 4.4 wt %" (25 °C, 4 MPa), "0.53% for HEG", "0.63% for Pd-HEG", "0.88% for N-HEG", "1.97% at 25 °C and 2 MPa" (Pd-N-HEG), "3 wt % at 4 MPa ... 25 °C" (Pd-functionalized graphene, ref. 19): same measurements as Table S1, recorded in the Table S1 rows' notes, no separate rows.
- main-6 (p. 7831) text: "1.76 wt % ... at 2 MPa and 25 °C" (Pd-functionalized graphene, = Table S1) and Eq. 1 substitution (1.97, 0.88 = Table S1 values).

## Values seen but not extracted

- Figures 5a, 5b, S5a, S5b: every marker other than the highest-pressure adsorption marker of each isotherm (25-100 °C isotherms, not 77 K; protocol extracts only the highest-pressure point).
- Desorption branches (Desor. 25 °C) in all four panels: treated as the desorption branch of the 25 °C run (same isotherm_id, counted in isotherm_point_count). Their highest-pressure markers were digitized and archived but not written as rows, because at non-77 K only one point per isotherm is extracted and the adsorption-branch endpoint was taken as that point. Note for the reconciler: the plotted desorption top marker sits at equal or slightly higher pressure than the adsorption top marker: HEG 37.65 bar, 0.704 wt% (adsorption top 37.14 bar); Pd-HEG 38.69 bar, 0.789 wt% (adsorption 37.65 bar); N-HEG 41.00 bar, 1.470 wt% (adsorption 40.12 bar); Pd-N-HEG 39.63 bar, 4.405 wt% (adsorption 39.64 bar). Archives: *_25C_desorption_top.json.
- 25 °C adsorption markers nearest 2 MPa, digitized only to test the merge with Table S1 2 MPa values (none merged): HEG 19.27 bar, 0.529 wt% (error-bar column of this partly hidden marker gives 19.51 bar; either way more than 2% from 20 bar); Pd-HEG 18.89 bar, 0.623 wt%; Pd-N-HEG 19.18 bar, 1.986 wt%; N-HEG 19.51 bar, 0.859 wt% (borderline: within one pixel, 0.18 bar, of the 19.6 bar limit). Archives: *_25C_near2MPa.json. In HEG, Pd-HEG and N-HEG a Desor. 25 °C marker lies within 2% of 2 MPa; it was not used for merging because Table S1 reports uptake capacity (adsorption) and a desorption point is not the same measurement.
- 0.72 wt% for Pd NPs (Eq. 1, p. 7831, 25 °C, 2 MPa): palladium nanoparticles alone, not a carbon sorbent.
- 1.12 wt% "enhancement" (Eq. 1, p. 7831): computed from measurements of several samples; not a row.
- Abstract 66% and 124% increases, conclusion 272% increase, p. 7829 "about 47% increase": derived ratios between samples; not rows.
- Abstract TOC graphic: a reduced copy of Figure 5b; not digitized separately.
- Introduction (p. 7826): "≤1 wt %" for pure carbon materials (literature, refs 11, 20; generic, no sample); DOE target 6.5 wt % and 62 kg m-3 (targets, not measurements).
- p. 7830: few-layered graphene 3.1 wt % "at high pressures and temperature of 300 K" (ref. 55, another group's result cited for comparison in the discussion, pressure stated only in words); not extracted as data of this paper. The reconciler may decide otherwise under the "values reported before" rule.
- p. 7830-7831: 13.79 wt % (Al on graphene, ref. 59) and ~5 wt % (Ca-decorated graphene nanoribbon, ref. 58): theoretical values, not measurements.
- Graphite powder (Gr, Figure S1a): Raman only, no H2 uptake; not a row.
- Characterization only (no separate rows; recorded in notes of the sample's uptake rows): Raman ID/IG 0.98 (HEG), 1.01 (N-HEG), 1.05 (Pd-N-HEG); XRD d-spacing increase 8-9% over 0.34 nm graphite (no value printed); Pd crystallite 8.2 nm (Pd-HEG), 5.8 nm (Pd-N-HEG); TEM Pd size 3.1 ± 0.6 nm (Pd-N-HEG), ~50 nm agglomerates (Pd-HEG); XPS N about 7 at.% with pyridinic/pyrrolic/sp3 C-N, Pd 21 wt % (XPS), 20 wt % (EDX) for Pd-N-HEG.
- Figures 1, 2, 3, 4, 6 and S1-S4 are not isotherms and show no H2 uptake values.
- No surface area (BET or any other), pore volume or pore size is reported for any sample anywhere in the paper or SI (surface_area_method = none on every row). This bears on eligibility criterion I4.

## Digitization

- Axis calibration (pixel positions found from intensity-weighted tick/frame profiles):
  - Figure S5 (si1-4): x 0 MPa at 458.0 (frame/0 tick), 4 MPa at 829.04, check 2 MPa at 643.33 (predicted 1.998, 0.10%). Panel (a) y: 0.0 at 962.0, 0.6 at 743.5, check 0.3 at 852.67 (0.07%). Panel (b) y: 0.0 at 670.3, 0.9 at 407.67, check 0.3 at 583.0 (0.28%).
  - Figure 5 (main-4): x 0 at 829.88, 4 at 1048.3, check 2 at 939.13 (0.04%). Panel (b) y: 0.0 at 578.16, 5.0 at 412.64, check 2.0 at 511.75 (0.31%). Panel (a) y: 0.0 at 756.72, 1.5 at 611.76, check 1.0 at 660.3 (0.23%).
- Markers are hollow symbols with error bars, drawn over thick connecting lines of the same colour; the digitizer's marker mode cannot separate whole series. Each target marker was therefore digitized with a tight region of interest (--roi) around that one marker and its error bar, --mode markers, --open-px 0, --marker-min-px 1. The tool often split the one hollow marker into several pixel groups (anti-aliased outline, line stub, overlapping star of the desorption series); these groups are all parts of the same marker, and the recorded value is the pixel-count-weighted centroid of all groups in the archive (equivalently, the centroid of the marker's pixels in the ROI). Fragment counts are given in each row's notes. Raising the tolerance until a single group formed pulled in the overlapping desorption-star pixels, so it was not used.
- Colour tolerances: S5 blue 230 (to exclude overlapping brown-star tints), other S5 colours 260; Figure 5 blue 120-150 and brown 150 (the two overlap, colour distance 163), green 245, red 238, black 331 (about 0.75 x the colour's distance to white, so anti-aliased marker pixels are included and the white background is not).
- One archive per digitized marker (top point, near-2 MPa point, desorption top) rather than one per series, because each marker needed its own ROI.
- The digitizer's `check` subcommand cannot run on single-marker archives (it requires the stated x to lie inside the digitized range), so the archives remain status "unchecked". Values that merge with printed values agree with them: Pd-N-HEG 4.390 vs 4.40 wt%; N-HEG 1.463 vs 1.47 wt%.
- Points beyond the highest labelled tick (x > 4 MPa in Figure 5; HEG 25 °C at 0.70 wt% above the 0.6 label of panel S5a) are linear extrapolations of the calibration and are flagged by the tool.
- Marker counts (isotherm_point_count; 25 °C counts include the Desor. 25 °C branch):
  - Figure S5b (Pd-HEG): 4 markers per series (25 °C 4 + desorption 4 = 8; 50, 75, 100 °C: 4 each). No marker at the origin.
  - Figure S5a (HEG): 25 °C 11 + desorption 11 = 22; 50 °C 11; 75 °C 12 (two overlapping circles near 2 MPa); 100 °C 11. Markers below 0.5 MPa overlap; ±1 possible.
  - Figure 5a (N-HEG): 25 °C 12 + desorption 12 = 24; 50 °C 12; 75 °C 12; 100 °C 11. Approximate: low-resolution figure, markers below about 0.7 MPa overlap.
  - Figure 5b (Pd-N-HEG): 25 °C 9 + desorption 9 = 18; 50 °C 9; 75 °C 8; 100 °C 8. Approximate for the same reason.

## Coding decisions

- Samples in order of first appearance: S1 Pd-N-HEG (abstract, first sentence), S2 HEG, S3 N-HEG, S4 Pd-HEG (introduction, "mechanical mixture"), S5 Pd-functionalized graphene (p. 7829, previous study). Labels from Table S1 (first table reporting uptake): Pd-HEG is "Pd-HEG Mixture" there; the superscript S1 after "Pd-functionalized graphene" is a citation marker and is omitted from the label.
- HEG coded reduced_graphene_oxide (made from Hummers graphite oxide; authors call it graphene). synthesis_method other for all samples: the raw carbon is HEG made by hydrogen(-induced, low-temperature per ref. 38's title) exfoliation of graphite oxide, a route not in the vocabulary; doping, Pd decoration and mixing are not synthesis.
- Pd loading 20 stored as wt% for Pd-N-HEG (EDX 20 wt%, XPS 21 wt%, Eq. 1 q = 0.20) and Pd-HEG ("maintained to be 20", unit not printed). N content about 7 at.% (XPS) is reported for Pd-N-HEG only.
- Basis: none named; volumetric Sieverts, so basis_inferred excess, basis_stated false, uptake_type unspecified. wt% convention not defined: unknown/none.
- calibration_described true: "The unit has been calibrated with high-purity hydrogen (99.99%) at various initial pressures. At various pressures and temperatures, the volume of gas contained in the empty sample cell was precisely measured." instrument_identified false (Sieverts apparatus, no make/model, not called home-built). h2_purity_pct 99.99 is stated for the calibration hydrogen.
- Degassing: the stated activation before H2 exposure (10^-6 Torr, 300 °C, 2 h) is coded on all HEG/N-HEG/Pd-HEG/Pd-N-HEG rows; the inter-cycle degassing (3 h, 200 °C, 10^-6 Torr) is in notes because the paper does not say which runs it precedes. Sample mass "over 250 mg" is not a number and is left empty.
- replicates_reported true for rows carrying an isotherm_id of a plotted isotherm (error bars on all plotted points, no numeric uncertainty printed); false for unmerged Table S1 rows (no isotherm_id) and for Pd-functionalized graphene.
- Pd-functionalized graphene (previously reported, SI ref. S1 / ref. 19): two table values at 25 °C coded as one isotherm I17 (2 values); measurement_method volumetric_sieverts because the paper says its setup is described in ref. 19; calibration, degassing and H2 purity not coded for it, since the paper describes them only for the four samples of this work.
- measuring_lab_id: corresponding author S. Ramaprabhu (marked *), Indian Institute of Technology Madras.
