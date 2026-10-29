# Extraction log, HYC-0074 (extractor A)

Rows written: 363 (18 table_direct rows, 345 figure_digitized rows), 11 samples (S1-S11), 18 isotherms (I1-I18). The validator (`validate_row_detail.py --errors-only`) reports no errors.

## Sources extracted from

- Table 2 (main.pdf p.1661): excess and total (parentheses) H2 uptake at -196 C and 20 bar, LAC2600/2700/2800, with surface area, micropore area, pore volume and micropore volume. 6 rows.
- Table 3 (main.pdf p.1662): same for LAC4600/4700/4800/4900. 8 rows.
- Table 1 (main.pdf p.1660): elemental composition and yield of the LAC samples, copied into `notes` of their uptake rows (no uptake in the table).
- SI Table S1 (SI p.S4): total H2 uptake at 20 bar for CAC2700, CAC4600, CAC4700, CAC4800, with their surface areas and pore volumes. 4 rows. Its LAC rows (LAC2700 4.4, LAC4600 4.2, LAC4700 5.2, LAC4800 6.0) repeat the Table 2/3 totals and are not separate rows (noted in the rows).
- SI Appendix 2 (SI p.S3): definition of total uptake (basis evidence) and the equation used to compute it from excess.
- Fig. 7A and 7B (main.pdf p.1663): 14 isotherms (7 samples, excess = open markers, total = filled markers), digitized at all markers that could be resolved (p >= 2.5 bar).
- Fig. S10A and S10B (SI p.S14): CAC2700, CAC4600, CAC4700, CAC4800 total curves (open markers), digitized (p >= 1.5 bar for CAC2700, p >= 2.5 bar for the others).
- Main Methods text (p.1659-1660): instrument, purity, outgassing, buoyancy correction, BET range, N2 method.

## Isotherm structure

- Each plotted curve is one isotherm. The excess and total curve of one sample come from one run (total is calculated from excess), but they have different basis codes, so they carry different `isotherm_id`s (I1/I2 = LAC2600 excess/total, ..., I13/I14 = LAC4900, I15-I18 = CAC2700, 4600, 4700, 4800 total). Reconciler: merge them if the protocol wants one id per run.
- Table value at 20 bar and plotted marker: merged by the rule (printed 20 bar within max(2%, 0.02 bar) of a plotted point). The row carries the printed value, `table_direct`, the isotherm id, and `digitized: <p> bar, <v> wt%, archive: <file>.json` in `notes`. Where the printed total differs from the plotted marker by 2.5% or more, `notes` says so and confidence is 4.
- Printed totals vs plotted totals (printed / plotted at the 20-bar marker): LAC2700 4.4 / 4.210 (-4.3%), LAC2800 5.6 / 5.309 (-5.2%), LAC4700 5.2 / 5.054 (-2.8%), LAC4600 4.2 / not resolved at 20 bar (19.49 bar marker 4.074). The other totals and all seven excess values agree within 1.5%. The plotted totals agree with the SI Appendix 2 equation computed from the plotted excess values and the printed pore volumes (H2 density at 77 K and 20 bar taken as about 0.0064 g/cm3, my estimate, not looked up): within 0.02 wt% for the six where both 20-bar markers were digitized (LAC4600 total could not be compared at 20 bar). The printed totals of LAC2700, LAC2800, LAC4600 and LAC4700 are 0.1-0.3 wt% higher than that equation gives. Recorded as printed; no value was altered.
- `isotherm_point_count` is approximate for all 18 isotherms. Markers at p >= 2.5 bar were counted exactly from the extracted series plus the missing nominal pressures; the markers below about 2.5 bar form a stack of up to 14 overlapping curves and cannot be separated. Estimates: LAC curves 32 each (20 at p >= 2.5 bar, about 12 below, from the clearest curves LAC2600 excess and LAC4600 total/excess), CAC4800 32 (20 + about 12), CAC2700 46 (24 + about 22 below 1.5 bar), CAC4600 48 (31 + about 17 below 2.5 bar), CAC4700 49 (31 + about 18). Error about +-3.

## Digitization method and deviations

- Tool: `digitize_figure.py extract --mode markers` (v2.1), calibrated on the lowest and highest labelled ticks of each axis with a third labelled tick as check. Fig 7A: x 0/20 bar, y 0/6 wt%, verify 10 bar and 3 wt% (residuals 0.18% and 0.15%); Fig 7B same y, x residual 0.15%; Fig S10A: x 0/20, y 0/5, verify 10 and 3 (residual 0.00%); Fig S10B: y 0/6, residuals 0.26% (x) and 0.12% (y). Tick pixel positions were located by inspecting pixel rows and columns.
- The plots have 7-8 overlapping curves with open and filled markers of 4 colours, so a plain colour isolation does not separate markers. I preprocessed the page image in my work directory and ran the tool on the result:
  - Open-ring series: enclosed white holes inside the ring ink were found, painted as filled discs in the series colour, and the tool was run on that image with `--open-px 1` and marker size limits taken from the median detected size. Each archive's `source_image` is the preprocessed PNG (sha256 recorded) in the work directory, not the page image.
  - Filled-marker series: raw page image, colour tolerance swept (70-200), then a second pass restricted to a band of +-0.07 to 0.10 wt% around a robust log-linear fit of the first pass points, tolerance swept again, and the tolerance with the most markers kept.
  - Markers below 2.5 bar (1.5 bar for CAC2700) were excluded by cropping the ROI.
  - Three pocket false positives between markers (a gap enclosed by neighbouring rings, not a marker) were blanked with page-pixel rectangles: LAC2600 excess (757-764, 859-865), LAC2800 excess (750-753, 825-829), CAC4800 (1096-1100, 424-429), then the series was rerun. Two further small false detections (CAC4700 at 4.71 bar, CAC4800 at 2.70 bar) were removed by the marker size filter.
- Every centroid is the tool's output; no value was read by eye. Only marker counts and the pressures of unresolved markers (nominal grid 3, 4, ..., 18, 18.5, 19, 19.5, 20 bar) were judged visually.
- Archives were left with `status: unchecked`. I ran the tool's `check` against the printed 20-bar values on copies: it passes for most series and marks LAC2700 total and LAC2800 total as discarded at 3% tolerance, because the printed totals differ from the plotted ones (see above), not because of an extraction fault. The archives in `digitizations/` were not modified by it.
- Fig. S10 also redraws LAC2700 (A) and LAC4600, LAC4700, LAC4800, LAC4900 (B). I compared these with the Fig. 7 totals and they coincide within about 0.01-0.03 wt%; they are replots, so they were not digitized again and no rows were made from them.

## Markers seen but not extracted

- All series: markers below about 2.5 bar (below 1.5 bar for CAC2700), unresolved stack (see counts above).
- LAC2600 total: markers at about 3 bar and 18.5 bar. LAC2600 excess: 7 bar and 18.5 bar.
- LAC2800 total: 18.5 and 19 bar. LAC2800 excess: 18.5 bar.
- LAC4600 total: the 20-bar marker (merged with the 19.5-bar marker; the Table 3 total row has no digitized partner and says so). LAC4600 excess: 5 and 9 bar.
- LAC4800 excess: 9 markers at 8-16 bar hidden behind LAC4700 total markers.
- LAC4900 excess: 5 markers at 3-7 bar hidden behind LAC4800 total markers.
- LAC4900 total: the marker nominally at 6 bar was merged with a neighbour; its centroid (5.78 bar) is flagged in the row, confidence 3.
- Ends of curves: 18.5/19/19.5/20 bar markers touch each other; where only some were separated the series are short by that many.

## Coding decisions worth checking

- Basis: `basis_stated = true` for both excess and total (Table 2/3 footnote e gives both side by side; SI Appendix 2 defines total). CAC totals use the Appendix 2 sentence (Table S1 names "Total H2 uptake" only).
- `wt_pct_convention = unknown`: the paper does not define its wt% convention. The 1/(1+dV) term in the Appendix 2 equation resembles a W2-type conversion but does not state one.
- `value_kind = measured` for totals as well (calculated from a measured excess point at the same pressure).
- `measurement_method = gravimetric_microbalance`; `instrument_identified = true` (Hiden IGA-003); `calibration_described = true` (buoyancy correction stated, "as previously described"); `replicates_reported = false`; outgassing 200 C "overnight" (duration left empty); H2 purity 99.9999%; sample mass not stated.
- Lab: corresponding author R. Mokaya, University of Nottingham.
- `synthesis_method = carbonization` (hydrothermal carbonization of lignin to hydrochar). For CAC the paper does not describe the preparation, but the Conclusions call the precursor "cellulose-derived hydrochar"; I coded carbonization on that basis. CAC activation conditions are read from the label and the Table S1 title.
- `area_same_sample`: yes for LAC; unclear for CAC (the paper cites ref. 28 and does not say CAC data were measured here or previously reported, so no `previously reported` note was added). BET method, N2 and P/P0 0.02-0.25 are from the Methods text for "the activated carbons"; consistency criteria not stated.
- Pore volume: micropore volume and micropore area by t-plot, total pore volume at P/P0 0.99, all N2. `average_pore_diameter_nm` left empty because the paper prints several NLDFT maxima per sample (given in `notes`).
- Table 1 composition (C, H, O %, C/H, yield) is in `notes`; no dopant is deliberate, so dopant fields are empty.
- The text gives surface area 1159 m2/g for LAC2600; Table 2 and the abstract give 1157. I used the table value.

## Values seen, not extracted

- All CO2 data (Tables 2 and 3 CO2 columns, Figs 4-6, Fig. S6-S9, Qst values): not H2.
- LD hydrochar (Table 1: C 66.6, H 5.06, O 28.34 %, C/H 13.2; Appendix 1: Mw about 3200 D, -OH content): no H2 uptake, so no row.
- Fig. 8 (H2 uptake against surface area): not an isotherm; it shows the Table totals, no new values.
- Hydrogen uptake densities 14.5 and 11.2 umol/m2 and slopes 2.9e-3 and 2.24e-3 wt%/(m2/g): derived across several samples.
- Literature comparison values (11.8 +- 0.7, 10.7 +- 0.8, 9 +- 0.1, 9.55, 11.75 umol/m2; "best activated carbons"): other materials/papers.
- Restatements of table values in the abstract and text (up to 6.2 wt%; LAC2600 3.2, LAC2700 3.7, LAC2800 4.7 wt%; totals 3.6-5.6 and 4.2-6.2 wt%; excess 3.5-5.2; LAC2700 4.4 and CAC2700 3.6 wt%; conclusions 3.6-5.6 and 4.2-6.2): same measurements as the table rows, no separate rows.
- Table S1 LAC rows: same values as Tables 2 and 3 (see above).
- Fig. S10 LAC curves: replots (see above).
- Fig. 7 and Fig. S10 show no desorption branch and no other temperature.
