# Extraction log, HYC-0115 (agent A)

## Sources extracted from
- Main Table 2 (p.4): H2 uptake at 100 bar and 5 bar, -196 C, 16 samples.
- Main Table 3 (p.5): same for 21 samples; CES250w-865-75 is "n.d." (characterization only, no row).
- Main Section 3.3 (p.8) text: "<0.1 wt%" at 5 bar, -116 C for CES250w-845-81 (row, upper bound, model-predicted).
- SI Table S3 (si1 p.3): 40 bar values of this work (CES250w-845-81 7.9; CPS230-885-85 7.5) and the authors' earlier CS-885-82 (9.19 wt% at 100 bar, previously reported, ref. [1] in SI / [31] in main text).
- Main Fig. 4a and 4b (p.7): 77 K H2 isotherms, digitized (page image main-7.png).
- SI Fig. S7a and S7b (si1 p.12): 77 K H2 isotherms, digitized (page image si1-12.png).
- Table S2 (composition, notes only), Table 1, Table S1: characterization, no H2 uptake.

## Digitization method
Axes calibrated on lowest and highest labelled ticks, verified on a third tick (Fig. 4: 0/100 bar, 0/8 wt%, check 60 bar and 4 wt%; Fig. S7a check 60 bar; Fig. S7b check 40 bar). Tick pixels found by pixel profiles. Series were separated by colour in a derived image (only the chosen marker pixels, painted in the series colour; overlapping series and the right-hand frame line removed) and run through digitize_figure.py extract --mode markers; archives are in digitizations/. Each archive was checked with digitize_figure.py check against the table value at 100 bar (or 5 bar when the series ends before 100); all passed within 5% except as noted below.
- Check limits: Fig4b_CES250w-845-74 holds a single point (100.1 bar, 6.28), which the tool cannot check (status stays "unchecked"); it agrees with Table 3 (6.3) within 0.3%. FigS7a_CPS250-845-62 and FigS7a_CPS250-835-58 end at about 90 bar, so they were checked at 90 bar against the 100 bar table value (curves are nearly flat there).
- Digitization uncertainty is not entered (per instruction).

## Markers not separated (not extracted)
Heavy overlap of curves and markers. These plotted markers exist but were not digitized:
- Low-pressure cluster (below about 5 bar, many markers on top of each other and on the axis line): only some markers separable. Digitized below 5 bar: Fig4a CPS230-885-85 (8 points), CPS230-855-78 (3), CPS230-835-59.5 (1); S7a CPS250-835-76 (4); none for the other series.
- Fig. 4b: all markers of CES250w-835-54 (open red circle) and CES250w-845-68 (open blue circle) (hidden under blue circles and each other); CES250w-835-75.5 at 40-90 bar and CES250-835-71 at 40-90 bar (red circle and red star overlap); CES250w-845-74 at 10-90 bar (overlap); CES250-885-79 at 10 bar; CES250w-885-81 at 10 and 20 bar.
- Fig. S7a: all markers of CPS250-845-80 (blue squares) and CPS250-855-82 (green squares) (hidden under red squares); CPS250-835-58 except 4 (overlap with other open squares).
- Fig. S7b: CES230w-835-80 at 10, 20, 80, 90 bar (overlap with star and diamonds).
- Marker at P = 0 (on the axis line) of several series not separated.
- `isotherm_point_count` therefore = digitized points + unseparated grid markers at 10, 20, ..., 100 bar that I can see; it excludes unseparable low-pressure markers and is a lower bound. Series with no digitized point have a count from the grid only.

## Rows merged with plotted points
- Table value at 100 bar merged with the plotted marker at 100 bar (printed pressure within 2 bar of the digitized point) for every curve that has one; the table row carries the isotherm_id and `digitized: ...` in notes (or a note that the marker could not be separated).
- Table value at 5 bar merged only for CPS230-885-85 (digitized 4.93 bar, 4.33 wt%); 40 bar (Table S3) merged for CPS230-885-85 (digitized 40.4 bar, 7.43).
- No plotted marker at 100 bar (curve ends earlier): CPS230-885-85 (ends 95.7), CPS230-855-78 (94.3), CPS250-845-80 (about 92), CPS250-855-82 (about 91). Their 100 bar table rows carry no isotherm_id.
- Samples with a plotted curve whose 5 bar table value is not a plotted point: 5 bar table rows carry no isotherm_id (paper does not say they come from the curve).
- Samples with no plotted curve: their 5 bar and 100 bar table values (and the 40 bar value of CES250w-845-81) form one isotherm each (point count 2 or 3).

## Discrepancies in the paper
- SI Fig. S7a green filled squares (CPS250-855-82 per legend) end near 8.1 wt% at about 91 bar, while Table 3 gives 7.2 wt% at 100 bar. Table value extracted as printed; series not digitized.
- SI Table S3, row CES250w-845-81: area 3074 and pore volume 1.50 belong to CES250w-885-81 in Table 3 (CES250w-845-81 has 2919 and 1.38). Table 3 characterization used.
- Fig. 4a CPS230-885-85 ends at 95.7 bar (9.05) while Table 3 gives 9.2 at 100 bar.

## Seen but not extracted
- TPSA working capacity columns (Tables 2, 3): predicted differences between two states, not uptake at one condition.
- Toth fit parameters n_m, K, t (Tables S4, S5): model parameters with no stated pressure (not a measured uptake).
- Predicted -116 C isotherms (Figs. S12, S13) and isosteric enthalpies (Figs. S10, S11): model outputs, not measurements.
- Text: "1.0 wt% or less" at 5 bar, -116 C for all TPSA samples (generic, not per sample); PSA working capacity 5.6 wt% for CES250w-845-81 (derived); "9.8 wt% at 100 bar" and "3.6 wt%" for CES230-835-50 (duplicates of table values); "2.4 to 4.5 wt%" range and "43-67%" ratio (summary of table values); 9.0 wt% assumed TPSA capacity (assumption in energy calculation).
- Table S3 literature rows [2]-[10] (Li 2024, Deng 2023, Sultana 2022, Stock 2022, Balahmar 2019, Chen 2019, Blankenship 2017, Adeniran 2015, Liu 2014): other groups' measurements cited for comparison, not this paper's data. Only the authors' own earlier carbon (CS-885-82) was extracted as previously reported.
- Fig. 3, 5, S5, S8, S9 (BO, area, pore volume, uptake vs BO or area; bar charts; Arrhenius): not isotherms, no values absent from the tables. Fig. 1, 2, S1-S4, S6 (SEM, N2 isotherms, PSD, Raman, EDX): no H2 data.
- Table S1 samples CPS, CPS230, CPS250, CES, CES230w, CES250w (carbons before activation), Table 1 materials, Table S2 CPS230-885-70: characterization only, no H2 uptake, no rows.
- CES250w-865-75: Table 3 "n.d." for H2 uptake, no row.
- No metal hydride, zeolite or MOF comparison measurements in the paper.

## Coding decisions
- Basis: paper states all isotherms and uptakes are total adsorption, defined as excess converted to total with N2 total pore volume: basis_stated true, basis_inferred total, uptake_type total. wt% convention not stated: unknown.
- measuring_lab_id: Blankenship (first marked corresponding author), University of Nottingham; the paper does not say where the H2 measurement was made.
- Sample mass: "greater than 20 mg" (minimum) not a value; left empty. H2 purity: "BIP+, Air Products" with no number; left empty. H2 degas: 200 C, 4 h (ramp 10 C/min); the BET degas (200 C, 1 h) is not recorded in the degas fields.
- BET range not stated and consistency criteria not stated (BETSI named, no criteria quoted): both false.
- Sample numbering follows Table 2 then Table 3 order; sample ids are not allocated to samples without H2 values.
- CS-885-82: temperature printed as "-196 C", pressure 100 bar; basis, method and value_kind unknown/unclear because the earlier work's details are not given.
