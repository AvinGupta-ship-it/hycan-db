# Extraction log, HYC-0076 (extractor A: agent A, claude-sonnet-5-5), 2026-10-29

Paper: Fernandez-Lera et al., J. Energy Storage 123 (2025) 116818. Carbon sorbents: nine CO2-activated carbon microspheres. 273 rows in rows.csv.

## Sources extracted from (one line each)

- main.pdf p.5 Table 3, column "H2 storage, measured, -196 C, 100 bar": 9 rows (S1-S9). 8 are the same measurement as the last plotted marker of Fig. 3 (printed pressure 100 bar is within 2 % of the plotted marker at 98.8-101.1 bar), so each is one table_direct row carrying the isotherm_id and `digitized: <p> bar, <v> wt%, archive: <file>.json` in notes. CS-835-78 has no digitized point (markers fully hidden), so its row has no `digitized:` note. The Table 3 values are repeated in the text (Sec. 3.2: 5.30, 9.19, 8.51) and in the abstract and conclusions (9.2); not separate rows.
- main.pdf p.5 Table 3 columns ABET, Vp, V<50nm, Vmicro, V<1nm and activation T, t: characterization on every row (V<50nm only in notes, no field). Mesopore volume 0.32 (CS-835-78) and 0.28 (CS-855-75) from text p.6.
- main.pdf p.6 Fig. 3a and 3b (H2 at -196 C up to 100 bar, Hiden XEMIS gravimetric, total basis): 82 figure_digitized rows. All markers I could separate were digitized.
- si1.pdf p.2 Table S2, column nm (mol/kg = mmol/g), 9 rows, value_kind fitted_extrapolated (Toth capacity, model parameter), pressure_unstated true, isotherm_id of the sample's Fig. 3 curve (the table caption says the fit is to those isotherms).
- si1.pdf p.3 Fig. S1 (CS-835-52, 845-64, 855-65, 865-66) and p.4 Fig. S2 (CS-835-78, 845-79, 855-75, 865-79, 885-82), H2 isotherm at 77 K (square markers) on a Micromeritics 3Flex, adsorbed volume in cm3(STP)/g against p/p0: 171 rows (143 from the linear-p/p0 panel, 28 from the log-p/p0 panel at p/p0 below 0.07).
- main.pdf p.7 text and si1.pdf p.9 Fig. S9, measured isotherm of CS-885-82 at -123 C (150.15 K) up to 40 bar: 2 rows. One text_direct row, 0.58 wt% at 5 bar (merged with the plotted marker at 5.08 bar), and one figure_digitized row, the highest-pressure marker (39.7 bar). Only the highest-pressure point is digitized at a temperature other than 77 K.
- Text Sec. 2.2/2.3, Table 2, SI Table S1, authors and affiliations: methods and characterization fields (instrument, degas, basis quote, N content, corresponding author).

## Coding decisions worth a reviewer's attention

- Sample numbering follows the first mention in reading order: CS-885-82 (Sec. 2.3, p.3), CS-835-52 (Sec. 3.1 text, p.4), then the Fig. 2 legend order on p.5: S1 CS-885-82, S2 CS-835-52, S3 CS-845-64, S4 CS-855-65, S5 CS-865-66, S6 CS-835-78, S7 CS-845-79, S8 CS-855-75, S9 CS-865-79.
- Isotherm ids: I1-I9 = Fig. 3 curves of S1-S9 (Table 3 and Table S2 rows share them); I10-I18 = 3Flex 77 K H2 isotherms of S1-S9; I19 = CS-885-82 at -123 C.
- Basis (Hiden rows, Table 3, Table S2, S9): uptake_type total; basis_stated true; evidence = the Sec. 2.3 sentences "All isotherms and reported uptake data in this work are in terms of total adsorption ... Conversion from excess to total uptake isotherm was then performed using the single point total pore volume determined in Section 2.2"; the paper defines the quantity by that derivation (net -> excess with He skeletal density -> total with Vp). Fig. S9 caption also says "total". wt% convention not stated: unknown/none.
- 3Flex rows (I10-I18): uptake_type unspecified, basis_stated false, basis_inferred excess (volumetric default). The "All isotherms ... total adsorption" sentence sits in the gravimetric Sec. 2.3 and the paper does not say it covers the 3Flex isotherms. uptake_ml_stp_g = digitized value; uptake_wt_pct = 0.0089938 x cm3(STP)/g (W1, computed_from_other_unit). p0 for H2 is never stated, so pressure_bar is empty with pressure_unstated true and `p/p0 = <value>` is in notes. The 3Flex degas, sample mass and calibration are not stated (empty / false).
- Temperature: -196 C printed, so 77.15 K, temperature_inferred false; -123 C printed, so 150.15 K.
- material_class doped_carbon (N 2.8-3 wt%, O 2.5-2.8 wt% built into the carbon from the TEDA/polymer precursor); dopant N. dopant_concentration_wt_pct only where SI Table S1 gives a row for the label (CS-835-52, CS-845-64, CS-855-65).
- measuring_lab_id "Blankenship group, University of Nottingham": first corresponding author marked (L. S. Blankenship, affiliation b). The paper does not say which lab ran the Hiden or 3Flex measurements.
- Pore volumes: Vp is single-point N2 at p/p0 0.95; Vmicro and V<1nm (ultramicropore volume, cutoff 1.0 nm) are dual N2+H2 2D-NLDFT (SAIEUS); one method/probe pair per row (NLDFT, other), and the Vp difference is stated in notes. BET by BETSI, no P/p0 range and no consistency criteria stated.
- replicates_reported false: the paper gives instrument precision (mass 0.1 ug, pressure 0.02 %) but no uncertainty or repeat for any uptake value.
- sample_mass_mg empty: "at least 50 mg" (dry weight >20 mg) is a bound, not a mass. h2_purity_pct empty: "BIP+, Air Products" with no number. degas_end_pressure_pa empty: the <1e-6 mbar is the base vacuum of the instrument, not a stated degas end pressure.
- isotherm_point_count: Fig. 3 curves = 21 inferred from the unobstructed series (CS-865-66 in 3a and CS-885-82 in 3b each show 11 markers at <=5 bar plus 10 at 10-100 bar, and the pressure grid is shared); applied to the five other curves that have at least 6 visible markers (CS-835-52, CS-845-64, CS-855-65, CS-855-75, CS-865-79); their notes say the count is inferred. Left empty for CS-835-78 (no visible marker) and CS-845-79 (3 visible markers). 3Flex curves = markers positively identified in both panels (lower bound; the log-panel low-p/p0 cluster is not fully separable). S9 = 11 identified (lower bound).
- Fig. 3 markers at the y-axis (digitized pressure below half a pixel, 0.15 bar; 5 markers: CS-885-82 x2, CS-865-66 x2, CS-865-79 x1): pressure cannot be read, and a zero or negative pressure fails validation, so pressure_bar is empty with pressure_unstated true and the uptake is kept.
- Extraction confidence: table 5; text 4; clean digitized markers 4; partly occluded or clustered Fig. 3 markers 3; log-panel cluster markers 2.

## Digitization method (disclosure)

The tool was never run on a raw page image for marker mode: the markers are hollow 1-px outlines, and the raw run returned fragments and wrong centres (e.g. the last green square at 97.7 bar instead of about 101). Instead, per series: (1) page PNG colour-unmixed against white (series RGB), (2) marker template fitted to that series' legend marker (square, circle, diamond, triangle, star) by Nelder-Mead, (3) template matching with a coverage criterion to find marker centres (sub-pixel), checked on overlays, (4) a synthetic image of solid discs at those centres (crop of the plot, 4x scale, series colour) was written in the work directory, (5) `digitize_figure.py extract --mode markers` was run on that image with the axis ticks mapped to the same scale; the tool's output JSON is the archive and the row values are the tool's values. Extracted marker count equals the detected count for all 27 archives. Scripts are in work/.

Axis calibration (lowest and highest labelled tick, third tick as check):
- Fig. 3a/3b: x 0 and 100 bar, check 60 bar; y 2 and 8 wt%, check 4 wt%. All passed at the tool's default tolerance.
- Figs. S1/S2 linear panels: x 0.0 and 1.0, check 0.6; y 0 and 600 (S1) or 0 and 1000 (S2) cm3/g, check 400 or 600. Passed.
- Figs. S1/S2 log panels: x 1e-5 and 1e-1, check 1e-3. The check tick is 3.6 % off (0.5 px: tick lines are snapped to whole pixels in the page image), above the tool's 2 % default. The labels are consistent, so values were extracted with `--verify-tolerance-pct 5`; p/p0 on these points carries about 4 % uncertainty; y passed.
- Fig. S9: x 0 and 40 bar, check 20; y 0.5 and 2.5 wt%, check 1.5. Passed.

Sanity checks (`digitize_figure.py check`) against printed values: Fig. 3 vs Table 3 at 100 bar, differences CS-835-52 +0.31 %, CS-845-64 -0.10 %, CS-855-65 +0.17 %, CS-865-66 -0.11 %, CS-855-75 +0.12 %, CS-845-79 +0.28 %, CS-865-79 +0.12 %: all PASS (5 % tolerance). CS-885-82: the last marker is at 98.79 bar, so x = 100 lies outside the digitized range; checked at 98.79 bar against 9.19: -0.31 %, PASS. S9 at 5 bar against 0.58 wt%: +0.08 %, PASS. Figs. S1/S2 archives (18) were not checked: the paper prints no per-sample value for those isotherms (their status stays 'unchecked'). The only related statement, "2.4 +/- 0.2 wt% at 1 bar for all samples" (p.7), is a cross-sample summary. For information, the digitized 3Flex points at p/p0 about 0.99 give 2.32 (CS-835-52), 2.47, 2.40, 2.42, 2.49 (CS-835-78), 3.02 (CS-845-79), 2.77 (CS-855-75), 2.48, 2.59 wt%: CS-845-79 and CS-855-75 fall outside 2.4 +/- 0.2, so that sentence probably refers to the Hiden data.

## Markers seen but not separable (Fig. 3, per series; visible of 21)

- CS-835-52 (green squares): 10 visible (10-100 bar); the 11 markers at <=5 bar are hidden behind later series.
- CS-845-64 (blue circles): 6 visible (50-100 bar); the rest hidden behind later series.
- CS-855-65 (red diamonds): 10 visible (10-100 bar); markers at <=5 bar hidden.
- CS-865-66 (grey stars): all 21 visible.
- CS-835-78 (green triangles): none visible, fully hidden behind later-drawn series; no point digitized.
- CS-855-75 (blue squares): 9 visible (20-100 bar); the 10 bar marker and those at <=5 bar hidden.
- CS-845-79 (red circles): 3 visible (80.7, 91.0, 100.8 bar); the rest hidden.
- CS-865-79 (grey diamonds): 10 visible (one at the y-axis, then 10.3-100.8 bar; the 40 bar marker is overlapped and not accepted: template score 0.44); markers at 0.3-5 bar hidden.
- CS-885-82 (black stars): all 21 visible.
- Figs. S1/S2: in the log panels the squares at p/p0 below about 0.005 and several dense clusters are stacked and could not be separated; only the 2-5 clearly separable markers per sample (28 in total) were digitized. In the linear panels each sample shows the 15 regular markers (p/p0 0.15-0.80 in steps of 0.05, and 0.99) plus one near 0.09-0.10 (not found for CS-845-79, 15 instead of 16).
- Fig. S9: eleven markers separated (0.18, 1.04, 1.57, 2.10, 3.06, 4.03, 5.08, 10.1, 20.0, 29.8, 39.7 bar); a stack of about 8 overlapping squares below about 1.1 bar is not separable (weak candidates at 0.37, 0.49-0.51, 0.79, 0.85, 1.02 bar were not accepted).

## Values seen but not extracted

- Table 3, "Working capacity" (measured, 100 minus 5 bar), 9 values: derived differences (footnote b), not measurements.
- Table 3, "Theoretical, -123 C, 5 bar" and "Working capacity" (footnote d), 18 values: predictions from the Toth potential method and Clausius-Clapeyron, and differences of them.
- Table 3 BO/t column and Table 3 V<50nm: not uptake (V<50nm kept in notes only).
- Text p.6: "uptake at 5 bar only ranges between 3.35 and 4.19 wt% for all samples": cross-sample range, not attributed to a sample (derived 100-minus-working-capacity values do not reproduce 3.35 exactly).
- Text p.7: "uptake at -196 C and 1 bar (2.4 +/- 0.2 wt% for all samples)": cross-sample summary.
- Text p.6-7: derived differences "almost 0.1 wt% at 5 bar", "0.2 wt% greater", "0.33 wt% working capacity", "improved from 5.30 to 9.19 wt%, working capacity 1.91 to 5.01"; TPSA working capacity 8.61 and predicted 9.01 for CS-885-82 (derived: 9.19 minus 0.58); predicted 0.18 wt% at 5 bar and -123 C (model). Abstract: 9.2, 9.0, 5.0 wt% (repeats and predictions).
- Text p.6: pressure at 50 % of maximum uptake (0.75 bar for CS-835-52, 3.18 bar for "CS-855-82"): pressures, not uptake. PSA/TPSA compression work (6770, 121 kJ/kg) and 46 mbar discharge pressure: not uptake.
- Fig. 4 (capacity against BO and BET area): correlation plots, no values beyond Table 3.
- Fig. S6 (normalized isotherms) and S6c/d: normalized, not uptake. Fig. S7 (isosteric enthalpies): not uptake. Fig. S8 (predicted -123 C isotherms) and the predicted and extrapolated series of Fig. S9: model output, not measurement.
- Figs. S1/S2 N2 isotherms (triangles, ASAP 2020) and PSD panels, Figs. S3-S5: not H2 uptake.
- Table 2, PS (polymer): ABET 0, dHe 0.39 g/cm3, C/H/O/N 56.29/3.91/35.24/4.56 wt%; CS (carbonized, not activated): ABET 540 m2/g, Vp 0.22, Vmicro 0.18 cm3/g, dHe 1.89 g/cm3, C/H/O/N 93.54/0.59/2.76/3.11 wt%. Characterization only, no H2 uptake reported: no row. (PS is also not a carbon sorbent.)
- SI Table S1, row "CS-885-72" (C/H/O/N 94.38/0.32/2.51/2.79 wt%): label matches no sample in the paper (CS-885-82 is the only 885 C sample); not assigned.
- SI Table S2, columns K (x1e-4 Pa-1) and t: fit parameters, not uptake.

## Paper inconsistencies noted

- Fig. 2c legend reads "CS-865-82"; the text reads "CS-855-78" (p.6, comparison with CS-835-78) and "CS-855-82" (p.6, 3.18 bar); Table 3 has CS-865-79, CS-855-75, CS-835-78 and CS-885-82. Labels in rows are those of Table 3.
- Table S1 "CS-885-72" (see above).
- The 3Flex H2 isotherms (Figs. S1/S2) show about 2.3-3.0 wt% at p/p0 0.99, while the text gives "2.4 +/- 0.2 wt% for all samples" at 1 bar (see the checks section).

## Deviation

- The tools directory `scripts/` was listed once (`ls`) before the run; it showed only digitize_figure.py and validate_row_detail.py. No file there was opened.
