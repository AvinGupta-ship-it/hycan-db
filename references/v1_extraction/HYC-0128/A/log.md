# Extraction log, HYC-0128 (agent A)

Source: main.txt/main-1..6.png only (no supplementary files). Pressure axes are P/P0 with P0 = 106.66 kPa printed on the axis label, converted with 1.0666 bar. Fig. 4 and Fig. 5 y axes are mg/g, stored as W1 = 0.1 x mg/g.

## Extracted from
- Abstract and text p.4 (journal p.197): GP-Ni0.83B1.09 4.4 wt% at 106 kPa (M76 row, text_direct, matched to Fig. 4 top closed-square marker; same value in Table 1 and abstract).
- Text p.4: GP-Ni2.41B0.69 2.6 wt% (no pressure; pressure digitized from the P/P0 = 1.0 marker).
- Table 1 (journal p.198): GP real capacity 1.4 wt% (table_direct; text says ~1.4; pressure digitized). Doped-GP real capacity 4.4 wt% (same measurement as the 4.4 row). BET areas 477 (GP) and 272 (Doped-GP = GP-Ni0.83B1.09) m2/g, "pore volume" 1.04 and 0.632 cc/g, attached to every row of those samples.
- Text p.5 (journal p.198): 273 K, GP 0.008 wt% at 106 kPa and GP-Ni0.83B1.09 0.2 wt% (no pressure; pressure digitized).
- ICP-ES composition (Ni 2.41/1.51/0.83 wt%, B 0.69/1.39/1.09 wt%) on the rows of the three doped samples.
- Fig. 4 (77 K, four samples, adsorption closed and desorption open symbols): digitized, 8 series, archives S1_ads/S1_des (GP, stars), S2_ads/S2_des (GP-Ni2.41B0.69, circles), S3_ads/S3_des (GP-Ni1.51B1.39, triangles), S4_ads/S4_des (GP-Ni0.83B1.09, squares). The legend order of the labels follows the series order in the plot (square top = 4.4 wt% = Ni0.83B1.09; circle top 26.5 mg/g = 2.6 wt% = Ni2.41B0.69; stated values confirm the mapping; triangles = Ni1.51B1.39 by elimination).
- Fig. 5 (273 K): only the highest-pressure point of each isotherm (P/P0 = 1.0 open marker) digitized, archives F5_doped_des.json (full open-square series, 11 markers), F5_doped_ads.json (12 closed markers, not used as rows), F5_GP_top.json. The two top points are carried by the text rows 0.008 wt% and 0.2 wt%.

## Interpretive decisions
- The marker at P/P0 = 1.0 is the turning point: the closed-symbol adsorption line ends at P/P0 about 0.977 and joins an open marker (closed square in Fig. 4 for GP-Ni0.83B1.09) at 1.0, from which the desorption line starts. The paper's capacities (4.4, 2.6, 1.4, 0.2, 0.008 wt%) equal the values at this marker. Text rows are coded adsorption (no desorption statement). The one digitized row for such a marker (GP-Ni1.51B1.39, 31.48 mg/g, P/P0 0.9995) is coded desorption because its marker is open per the caption. Closed square at 1.0 (GP-Ni0.83B1.09) is carried by the 4.4 wt% row.
- For the three text rows without printed pressure (GP 1.4, GP-Ni2.41B0.69 2.6, GP-Ni0.83B1.09 273 K 0.2) the digitized pressure of the matching marker is used.
- 273 K: the last closed adsorption markers (doped 1.70 mg/g at P/P0 0.978; GP about 0.06 mg/g) are not extracted because only the highest-pressure point of each isotherm is extracted.
- Fig. 5 GP isotherm_point_count left empty: the red markers lie on the x axis and cannot be counted.
- B in Ni-B is coded as dopant_element with its ICP wt%, Ni as metal_element, material_class composite; the paper calls the samples "Ni-B nanoalloy-doped".
- No basis is named: basis_stated false, basis_inferred excess (volumetric default), uptake_type unspecified. wt% convention of printed wt% values: unknown (the paper plots mg/g, a unit pairing that is not printed numerically).
- measuring_lab_id: corresponding author C. M. Li, Nanyang Technological University.

## Unresolved markers (Fig. 4)
The figure is printed at low resolution with eight black series. Markers that could not be separated were not extracted:
- Low-pressure cluster, P/P0 below about 0.15 (y below about 6 mg/g): all eight series merge into one black mass. Not extracted. isotherm_point_count excludes these markers, so counts (34, 33, 34, 34) are lower bounds.
- Closed triangle and closed circle (GP-Ni1.51B1.39 and GP-Ni2.41B0.69 adsorption) overlap into one blob at P/P0 about 0.23, 0.28, 0.33, 0.38, 0.43, 0.48 (six pairs) and at 0.577 (a three-marker blob with the open circle), 0.727 and 0.778 (triangle merged with open circle). Only the pairs at 0.527 and 0.627-0.98 were separated (watershed split, flagged confidence 2 on the affected rows).
- Open circle (GP-Ni2.41B0.69 desorption) partly hidden or merged at P/P0 about 0.245 (merged with the open triangle), 0.541, 0.577, 0.735, 0.78.
- Open star plus closed star at P/P0 about 0.93 (one blob), not extracted.
- Open triangle at P/P0 about 0.245 merged with the open circle, not extracted.
- Hollow markers were filled (small enclosed white areas) and the four in-plot labels and axis frame were whited out in a copy of the page image in the work directory before running the tool; marker centroids of triangles are centroids of the filled triangle.

## Values seen, not extracted
- Table 1 "Theoretical monolayer H2 capacity" 1.3 (GP), 0.5 (doped), 4.8 wt% (perfect graphene): calculated, not measured.
- Introduction: Ru-doped templated carbon 1.43 wt% at 298 K, 10.3 MPa (ref. 15) and templated carbon 1.0 wt% "at the similar conditions" (ref. 36): literature comparison materials, not samples measured here; conditions of the second not stated.
- Isosteric heat about 1 kJ/mol, "7.5 mg/g" loading threshold, Fig. 7: not uptake values. Fig. 7 (isosteric heat) and Fig. 6 (N2 isotherms) not digitized; 87 K H2 isotherms used for Fig. 7 are mentioned but not plotted.
- 273 K "about 25 times" ratio: derived by the authors.
- N2 characterization of GP-Ni2.41B0.69 and GP-Ni1.51B1.39: none in the paper.

## Process notes
- One check call on S1_des.json was run at the wrong x and discarded that archive; S1_des was re-extracted from the same image with identical settings and then checked at the correct point (passed). S3_des and the unused F5/ads archives have no stated value to check against (S3 has no printed capacity); they stay status unchecked.
- Calibration Fig. 4: x 0.0 at 728.5 px, 1.0 at 1066.67 px (check 0.6 at 931.7, error 0.15%); y 0 at 421.44 px, 50 at 119.33 px (check 30 at 239.67, 0.28%). Fig. 5: x 0.0 at 731.3, 1.0 at 1066.8 (check 0.6 at 932.57); y 0.0 at 1406.6, 2.0 at 1133.7 (check 1.2 at 1242.64).
