# HYC-0129 extraction log (extractor B)

Paper: Favvas et al., J Porous Mater (2008) 15:625-633, doi 10.1007/s10934-007-9142-2. Input: page images main-1 to main-9 only (no SI). One carbon sorbent with H2 uptake: the carbon molecular sieve hollow fiber membrane (no printed sample label; coded `(unlabelled 1)`, sample HYC-0129-S1). 61 rows written, all from Fig. 6.

## Sources extracted from

- main-5 (p. 629), Fig. 6 "Low pressure hydrogen adsorption/desorption at 77 K": both branches digitized (30 adsorption rows, 31 desorption rows), isotherm I1, 77 K, x = P (mbar) 0-1000, y = "Volume (mmol/g)".
- main-3 (p. 627), section 2.5 "Hydrogen adsorption at 77 K": method (commercial volumetric porosimeter, Quantachrome Autosorb-1 with Krypton upgrade), degassing "overnight at 573 K under high vacuum (~10-7 mbar)". No H2 purity, sample mass, free-volume calibration or basis stated.
- main-5 (p. 629), section 3.3 text: Langmuir s.s.a. "around 560 m2/g" calculated from the H2 77 K data with a molecular area of 12.4 A2; stored as `langmuir_surface_area_m2_g` = 560, method Langmuir, probe gas `other` (H2), `area_same_sample` = yes. No BET range or consistency criteria stated.
- main-1 (p. 625), affiliations: corresponding author Favvas (envelope mark), Institute of Physical Chemistry, NCSR "Demokritos" (no university named) -> `measuring_lab_id`.
- main-3 (p. 627), section 2.3: pyrolysis protocol used for `material_description` and `synthesis_method` = pyrolysis.

## Fig. 6 digitization

- Calibration on main-5.png (1241 x 1648 px). x: 0 mbar at px 675.1 (y-axis line and tick centroid), 1000 mbar at px 1119.25 (tick centroid); check tick 500 mbar at px 897.25 (relative error 0.03%). All x ticks 100-900 lie within 0.7 px of the linear calibration. y: 0 at px 1409.75 (gridline centroid), 6 at px 1169.52 (tick centroid); check tick 4 at px 1249.19 (relative error 0.25%); the 2 tick (px 1330.85) reads 1.971 (0.5% of span). Top of the frame (about 7) is unlabelled; points above 6 mmol/g are linear extrapolations within the plot frame (flagged in notes).
- Adsorption (filled black diamonds): `--color #000000 --tolerance 40 --open-px 2 --roi 668 1128 1135 1418 --mode markers`, archive `digitizations/fig6_adsorption.json`, 33 points. Excluded from rows: index 0 (0.87 mbar, 0.437 mmol/g, 231 px) = merged component of about 11 overlapping markers at P of about 0-3 mbar; index 3 (7.86 mbar, 2.05 mmol/g, 200 px) = merged component of about 7 overlapping markers at P of about 3-12 mbar; index 16 (pixel 858.5, 1281.8) = legend sample marker. Tolerances 10-60 and openings 2-5 (and a stack-only ROI) were tried; none separates the stacked markers, which overlap by about half their height.
- Desorption (open diamonds, drawn on top of the filled ones): the outline cannot be isolated from the black adsorption markers, so the series was isolated by its white marker fill: `--color #ffffff --tolerance 40 --open-px 2 --marker-min-px 10 --marker-max-px 80 --roi 668 1128 1135 1272 --mode markers` (ROI bottom just above the legend box), archive `digitizations/fig6_desorption.json`, 34 points. Excluded from rows: indices 13 (576.0 mbar), 15 (595.3 mbar) and 17 (618.9 mbar), which are enclosed white background pockets between the y = 6 gridline and the connecting lines, not markers (verified on enlarged overlays). Two smaller pockets (8 and 4 px) were rejected by the size filter.
- Marker count (step 6). Desorption: 31 open markers counted, 31 extracted. Adsorption: 51 filled markers counted, 30 extracted; not separable: 11 in the lower stack (P about 0-3 mbar, 0-0.9 mmol/g) and 7 of the 9 in the upper stack (P about 3-12 mbar, 1.2-2.4 mmol/g), counted from local maxima of the row darkness profile (a 4-row flat top counted as two markers; one marker hidden by the y = 2 gridline inferred from the widths of rows 1328-1334), uncertainty about +-2 per stack; and 3 markers almost entirely hidden behind open markers, visible only as slivers that the tool rejects as too small (rejected components at pixel 940.5/944.5, 1163.5/1166.5, about 602 mbar; 1086.5, 1144.5, about 926 mbar; 1115.5, 1144.5, about 992 mbar). `isotherm_point_count` = 82 (51 + 31), approximate.
- Adsorption markers above 500 mbar (and those at 43 and 209 mbar) are partly covered by open markers; their centroids are of the visible part and they carry `extraction_confidence` = 2. Neighbouring open markers above 700 mbar overlap each other slightly, so some white-fill centroids may be biased by up to about 1 px.
- The tool's own `check` subcommand needs a value printed in the paper; the paper prints no H2 uptake value, so it could not be run and both archives keep status `unchecked`.

## Values seen but not extracted

- Text, abstract and p. 629: N2 at 77 K showed "negligible uptake" (N2, not H2; no number).
- p. 629-630 text: BET and Langmuir areas from CO2 isotherms at 273 and 298 K "between 525 and 625 m2/g" (molecular area 22.2 A2): a range covering two methods and two temperatures, not assignable to one field; given in notes only.
- p. 629 text and Fig. 7 (main-6): CO2 capacity 4.2 and 4.5 mmol/g at 20 bar (298, 273 K) and CO2, CH4, N2 adsorption/desorption isotherms at 273 and 298 K: not H2.
- Fig. 5 (main-5): TGA of the P84 precursor; text p. 628: Td 798 K, mass loss 34.1% at 1173 K: not H2 uptake.
- Fig. 8 (main-6) and Table 1 (main-7): CO2/CH4 and CO2/N2 kinetic selectivities and CH4, CO2, N2 diffusion coefficients: not H2 uptake.
- Table 2 (main-7): permeance/permeability of the carbon membrane, including H2 (460, 599, 818 GPU x 10-2 and 1610, 1498, 2045 Barrer x 10-2 at 313, 333, 373 K; Eact 9.2 kJ/mol), and qst for CH4, CO2, N2: permeation, not uptake.
- Table 3 (main-7): permeance/permeability of the P84 precursor (H2 25.3, 33.2, 47.7 GPU): permeation of an uncarbonized polymer, not uptake.
- Tables 4 and 5 (main-8) and abstract/conclusions: permselectivities (e.g. H2/CH4 843 at 373 K) and H2 permeance 8.2 GPU (2.74 x 10-9 mol/m2 s Pa): not uptake.
- P84 precursor hollow fibers: characterization only (calculated density about 1.30 g/cm3, Tg 588 K); uncarbonized polymer, not a carbon sorbent, no H2 uptake; no row.
- Section 2.7 (main-4): IGA gravimetric conditions (outgassing at 523 K, buoyancy correction, "the results refer to excess isotherms", gas purities) apply to the CO2, N2 and CH4 measurements only and were not applied to the H2 rows.
