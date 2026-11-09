# HYC-0125 extraction log (agent A)

Source: main.txt and page images only (34 pages; no supplementary file). Only page 11, Fig. 10, holds measured H2 uptake. 36 rows written.

## Extracted
- Fig. 10a (page 11), fluorinated MSC-30 (BF3/F2-treated at 100 C), 77 K, adsorption: 19 rows (I1), digitized with digitize_figure.py markers mode, archive digitizations/fig10a_fluorinated_MSC30_77K.json. The archive was made from a derived image work/main-11_a_blue_filled3.png (black fit line crossing the blue markers recoloured blue so each marker is one blob; no geometry change). Archive holds 21 detections; two not used: the legend marker (2.23 bar, 4.09 wt%) and a merged blob of about 3 overlapping markers (96 px, near 1.06 bar, 2.01 wt%). Counted about 26 markers on the plot: 19 extracted, 3 in the merged blob, about 4 near the origin largely hidden behind 87 K markers (the tool detected only 9-px fragments at tolerance 80, centroids at negative pressure, so not used). isotherm_point_count 26 is approximate.
- Fig. 10a, 87 K: highest-pressure point only (13.66 bar, 3.52 wt%), 1 row (I2); archive fig10a_fluorinated_MSC30_87K.json. Markers counted about 22 (heavy overlap below 2 bar, estimated from blob areas); count approximate.
- Fig. 10b (page 11), pure MSC-30, 77 K, adsorption: 15 rows (I3), archive fig10b_MSC30_77K.json (17 detections: legend marker not used, origin marker at 0 bar / 0 wt% not extracted because pressure 0 is invalid in pressure_bar). 16 markers counted on the plot, 16 detected excluding the legend marker, count matches.
- Fig. 10b, 87 K: highest-pressure point only (31.12 bar, 4.80 wt%), 1 row (I4); archive fig10b_MSC30_87K.json. 20 markers counted; a merged blob of 3 markers near 1.7 bar does not affect the extracted point.
- Text p.10: MSC-30 surface area 3350 m2/g (pure sample), used in S2 characterization. Fluorinated sample: no surface area; 19% weight gain due to F.

## Digitization notes
- Calibration Fig. 10a: x ticks 0 (263.17 px, y-axis line), 15 (423.5, verify), 30 (584); y ticks 2 (371), 3 (312, verify), 4 (254). The y tick labelled 1 is hidden behind markers, so the lowest labelled y tick could not be located by pixel inspection; calibration used ticks 2 and 4 with 3 as check (error 0.3%). Values below 2 wt% are a linear continuation of that calibration (tool flags them as outside calibrated range).
- Calibration Fig. 10b: x ticks 0 (664), 20 (838.5, verify), 40 (1013.5); y ticks 0 (485.5), 3 (353.5, verify), 6 (221.5).
- The tool's step-6 `check` needs a value the paper states; the paper states no uptake value in text, so the archives stay status "unchecked". Marker counts were compared as the instruction requires.
- Pressures are from plotted x position; no pressures are printed for any value.

## Seen, not extracted
- Insets of Fig. 10a/b (isosteric heat vs loading, kJ/mol) and text values 6.1 and 6.2 kJ/mol zero-coverage enthalpy: not uptake.
- Pages 3-9, 11-33: GCMC and DFT simulation results (foam capacities, Figs. 14-17, quantum-correction table, 7.7 wt% spillover estimate, metallacarborane 7.7 and 6.38 wt%): computed, not measured.
- Page 8: HiPco SWNT surface area "of the order of 1500 m2/gram", hydrogen adsorption "too weak" at room temperature, and carpet (VANTA) storage "similar to HiPco": no H2 uptake value, no sample row.
- Page 26: "Up to 4 wt% ... IRMOF-8 at 298 K and 10 MPa": a MOF reported from other work, not a carbon sorbent and not measured here.
- Page 10: one-gram fluorinated VANTA/carbon samples tested at NREL and Air Products showed no significant increase: no values given.

## Coding decisions
- MSC-30: paper does not say it is commercial or activated carbon: synthesis_method unknown, material_class other, no material_identity.
- Fluorinated MSC-30: doped_carbon, dopant F and B (carbon converted to a solid superacid by F2 then BF3).
- Basis: axis reads "Surface Excess Adsorption"; named but not defined: basis_stated false, basis_inferred excess, uptake_type excess. Measurement method not named: unknown. wt% convention not stated: unknown/none.
- Lab: "High surface area samples provided by Cal Tech were exposed to fluorine and boron trifluoride and returned to Cal Tech for evaluation" and "Adsorption data provided by Channing Ahn, Caltech": measuring_lab_id "Ahn group, Caltech" for both samples (Fig. 10a attribution is by inference from the first quote).
- Surface area of S1 coded not_reported; 3350 m2/g is not carried over as a parent-material area.
