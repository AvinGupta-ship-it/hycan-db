# HYC-0125 extraction log (agent B)

Paper: Yakobson & Hauge, Rice University, DOE Final Report DE-FC36-05GO15080 (34 pages, main only, no SI). The report is mostly computational; the only measured H2 uptake data are the two isotherm panels of Fig. 10 (p.11), measured at Caltech.

## Extracted from

- main p.11, Fig. 10a (Fluorinated MSC-30), 77 K blue series: 17 rows (M1-M17), isotherm I1, sample S1. Archive `digitizations/HYC-0125_fig10a_fluorinatedMSC30_77K.json`.
- main p.11, Fig. 10a, 87 K red series: highest-pressure point only, 1 row (M18), isotherm I2, sample S1. Archive `digitizations/HYC-0125_fig10a_fluorinatedMSC30_87K.json`.
- main p.11, Fig. 10b (MSC-30), 77 K blue series: 14 rows (M19-M32), isotherm I3, sample S2. Archive `digitizations/HYC-0125_fig10b_MSC30_77K.json`.
- main p.11, Fig. 10b, 87 K red series: highest-pressure point only, 1 row (M33), isotherm I4, sample S2. Archive `digitizations/HYC-0125_fig10b_MSC30_87K.json`.
- main p.10, bullets 4-6 (sample identity, "BF3/F2-treated at 100 oC (wt gain due to F is 19 %)", "pure MSC-30 (3350 m2/g)", "Adsorption data provided by Channing Ahn, Caltech", "returned to Cal Tech for evaluation of hydrogen bonding behavior"): characterization, sample description and measuring laboratory for all rows.

## Digitization details (Fig. 10, p.11)

- Working images in the work directory: `main-11_legend_masked.png` (legend markers of both panels painted white so they are not picked up as data) and `main-11_a_bluehue.png` (from the masked image; in the panel-a plot area every pixel whose blue channel exceeds both red and green by >= 40 was set to #1338dd, because the black fit line is drawn over the blue 77 K markers and darkens their upper halves to navy; without this the tool found only fragments of 13 markers). Only the panel-a 77 K series used the recoloured image.
- Panel a calibration: x on 0 bar (y-axis line, px 263.17; no separate tick mark) and 30 bar (px 584.07), checked on 15 bar (px 423.45, rel. error 0.1%). y on 2 wt% (px 370.96) and 4 wt% (px 254.08), checked on 3 wt% (px 312.00, rel. error 0.3%). The lowest labelled y tick (1 wt%) is hidden under markers and could not be located, so 2 wt% was used as the lower calibration tick. The x-axis line of panel a sits at about 0.11 wt% on this calibration (no 0 label on the y-axis).
- Panel b calibration: x on 10 bar (px 751.0) and 40 bar (px 1013.32), checked on 20 bar (px 838.63, rel. error 0.1%); the 0 bar tick is hidden under the origin marker and could not be located. y on 0 wt% (x-axis line, px 485.54) and 6 wt% (px 221.58), checked on 3 wt% (px 353.73, rel. error 0.1%).
- Colours: blue #1338dd, red #e43d21, tolerance 40, markers mode.
- `digitize_figure.py check` not run: the report prints no uptake value for any Fig. 10 point to check against. Archives remain status "unchecked".
- The solid lines drawn through each series (black for panel-a 77 K, red, blue) are curves through the markers (likely fits for the isosteric-heat analysis); not digitized because markers are present.

## Plotted points seen but not extracted

- Fig. 10a 77 K: 5 overlapping markers at about 0.8-1.5 bar (about 1.77-2.25 wt%) merge into one blob (archive series index 5, 276 px); morphological opening 4-7 px did not separate them into single markers. Not extracted; counted in isotherm_point_count.
- Fig. 10a 77 K: 2 markers at about 0.70 and 0.99 wt% next to the y-axis are mostly covered by 87 K markers (20 and 27 px visible of about 57); their centroids give negative pressures (-0.114 and -0.016 bar, archive indices 0 and 1). Not extracted.
- Fig. 10a 77 K: 1 marker at about 0.38 wt% (rows 462-468) is almost fully hidden under an 87 K marker (only a blue fringe visible); the tool does not detect it. Not extracted; counted. A faint purple fringe at about 0.2 wt% may indicate one more hidden 77 K marker; not counted.
- Fig. 10a 77 K: markers at 1.20, 1.40 and 1.58 wt% (archive indices 2-4) are partly covered by 87 K markers (42-46 px visible); extracted with extraction_confidence 2.
- Fig. 10b 77 K: origin marker (archive index 0: 0.053 bar, -0.002 wt%) not extracted; the digitized uptake is negative (pixel noise at the origin) and cannot be stored. Counted.
- Fig. 10b 77 K: marker at about 0.1 bar / 1.5 wt% (archive index 1) is mostly covered by 87 K markers (18 px visible of about 46); centroid unreliable. Not extracted; counted.
- Fig. 10a 87 K and Fig. 10b 87 K: all points except the highest-pressure one not extracted (protocol: only the highest-pressure point of non-77 K isotherms). Panel-a red count 22 is approximate because markers below 2 bar overlap; panel-b red count 20 (one blob of 3 at about 1.7 bar).

## Values seen but not extracted (not H2 uptake rows)

- Fig. 10a and 10b insets (p.11): isosteric heat (kJ/mol) against uptake (wt%); not isotherms, not digitized. Text values: zero-coverage enthalpy approximately 6.1 kJ/mol (fluorinated MSC-30) and approximately 6.2 kJ/mol (MSC-30) (p.10).
- p.8: HiPco SWNT, "surface areas of the order of 1500 m2/gram; however, hydrogen adsorption was too weak, preventing significant hydrogen adsorption at room temperature": no uptake value; no row. Characterization: surface area ~1500 m2/g (method not stated).
- p.8: VANTA SWNT arrays, diameters 0.8-3 nm, array thickness ~0.5 mm: characterization only, no uptake value; no row.
- p.9: "Hydrogen storage on unfunctionalized carpets proved to be similar to that for HiPco produced SWCNTs": no value; no row.
- p.10: one-gram carbon nanotube salt (fluorinated/BF3 VANTA) samples tested with NREL and Air Products: "did not indicate a significant increase of hydrogen storage over unfluorinated materials"; no value; no row.
- p.7: carbon nano-foam "~2600 m2/g", "~0.9 g/cm3": computed model structure, not a measured sample.
- p.13, Fig. 12: model foam densities (0.57-0.97 g/cm3) and accessible surface areas (1522-2437 m2/g): computational.
- pp.16-19, Figs. 14-17 and the Table on p.19 (classical overestimates in %): GCMC-simulated excess and total gravimetric/volumetric capacities of model foams and tube bundles at 77, 150 and 298 K: theoretical, not measured; not extracted.
- pp.20, 25, 26: 7.7 wt% for fully hydrogenated graphene (CH) by spillover: theoretical stoichiometric value; not extracted.
- p.26: "Up to 4 wt% of adsorption has been reported for IRMOF-8 at 298 K and 10 MPa": literature value for a MOF (not a carbon sorbent, not original to this report); not extracted.
- pp.32-33, Fig. 24: computed capacities of metallacarboranes (7.85/7.67, 7.93/7.73, 6.38/6.23 wt% for Sc/Ti; 7.7 wt% for Ti2(C2B8H10); 6.38 wt% for C4B8H12Me2): theoretical and not carbon sorbents; not extracted.
- Figs. 1, 3-7, 11, 13, 18-23, 25: potentials, binding energies, structures and energies from calculations; no measured uptake.

## Coding decisions

- Samples numbered only for samples with rows: S1 = Fluorinated MSC-30 (first H2 sample in the text, p.10 bullet 5), S2 = MSC-30. Labels from the Fig. 10 panel titles.
- measuring_lab_id "Ahn group, Caltech": p.10 says the adsorption data were provided by Channing Ahn, Caltech, and the fluorinated samples were returned to Cal Tech for evaluation.
- Basis: values named "Surface Excess Adsorption" on the Fig. 10 axes; the report's definition of excess (p.14) is in the GCMC simulation section, so basis_stated = false (conservative), basis_inferred = excess (paper calls the value excess).
- measurement_method unknown (not stated). Instrument, calibration, degassing, sample mass, H2 purity, replicates: not stated.
- Surface area 3350 m2/g printed for pure MSC-30 without method or gas: surface_area_method unspecified, probe gas unspecified, area_same_sample unclear for S2; carried on S1 rows as parent_material.
- MSC-30: no supplier or purchase stated, so synthesis_method unknown and material_identity empty; material_class activated_carbon from the MSC-30 designation. Fluorinated MSC-30 coded doped_carbon (F from direct fluorination, B from BF3 complexation; no separate non-carbon phase described). "wt gain due to F is 19 %" not stored as a concentration (it is a mass gain relative to the parent).
