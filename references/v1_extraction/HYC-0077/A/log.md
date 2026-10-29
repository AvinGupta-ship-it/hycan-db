# Extraction log, HYC-0077 (extractor A), 93 rows

Sources are named as `main p.<n>` (page n of the main article, `in/pages/main-<n>.png`). Fig. 6 y-axis is wt%, x-axis pressure in bar (0-20); all curves are 77 K.

## Extracted from

- Table 1, main p.4 (carbon rows UCs-60, UCs-70, UCs-80, UCs-90, UCs-100, UCs-90-2, Cs-90): 14 H2 values (20 bar value and, in parentheses, 1 bar value for each of 7 samples), all 77 K, gravimetric. 14 rows. Surface areas (BET, p/p0 0.02-0.25, N2), total pore volume (p/p0 0.996), micropore volume (DR), mesopore volume (by difference) copied onto every row of the sample. 8 of the 14 values are the same measurement as a plotted Fig. 6 point and are the merged rows (see below); 6 are separate table rows (UCs-60 x2 and UCs-80 x2 with no plotted curve, forming isotherms I1 and I3 of 2 printed values each; UCs-90-2 1 bar and Cs-90 1 bar, see below).
- Fig. 6 main panel, main p.5 (five 77 K adsorption series, markers digitized): UCs-70 (open diamonds, I2), UCs-90 (open circles, I4), UCs-100 (open squares, I5), Cs-90 (open up-triangles, I7); 68 markers extracted (18, 16, 20, 14), archives `digitizations/Fig6_main_<sample>.json`. UCs-90-2 (open down-triangles) is digitized from the inset instead (next line).
- Fig. 6 inset, main p.5 (UCs-90-2 adsorption, filled down-triangles, I6): 19 markers used: 17 from `digitizations/Fig6_inset_UCs-90-2_open2px.json` (p about 0.2, 0.4, 0.6, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20 bar) and 2 from `digitizations/Fig6_inset_UCs-90-2_open3px.json` (the markers at about 0.8 and 0.98 bar, which merge into one blob with a 2-px opening). Run on the raw page image (filled markers separate cleanly), roi x 921-1150, y 270-443; inset axes calibrated on ticks 0 and 20 bar / 0 and 3.6 wt%, verified on 10 bar and 1.8 wt%.
- Text, main p.2-5: values repeated from Table 1 are not separate rows, they are noted in the `notes` of the table row: "1.39, 1.30 and 1.34 wt% at 1 bar" (Cs-90, UCs-90, UCs-90-2), "1.15 wt% at 1 bar" (UCs-100), abstract "up to 3.65 wt% at 77 K and 20 bar" (UCs-90-2, 3.65 in Table 1).
- Experimental text, main p.2: H2 measurement (Hiden IGA-001, buoyancy-corrected, 77 K to 20 bar, degas 10^-7 bar / 200 C / 5 h, H2 above 99.999%), N2 characterization (ASAP 2020, BET 0.02-0.25, degas 300 C / 10 h), synthesis and treatments.

## Merge and pressure decisions

- Table value and plotted point are one measurement (one row, table value, printed pressure, `table_direct`, isotherm id of the curve, `digitized:` note, no separate digitized row): UCs-70 at 1 bar (digitized 0.9979 bar, 1.4204 wt%) and 20 bar (20.0009 bar, 3.5249); UCs-90 at 1 bar and 20 bar; UCs-100 at 1 bar and 20 bar; UCs-90-2 at 20 bar (inset 19.9541 bar, 3.6571); Cs-90 at 20 bar (19.9554 bar, 2.8603).
- UCs-90-2 1 bar (Table 1 1.34): the inset marker nearest 1 bar is at 0.976 bar (1.3542 wt%), 0.024 bar from the printed 1 bar, outside the larger of 2% and 0.02 bar, so the table value is a separate row without isotherm id and the digitized marker is a separate row. The inset has only 0.09 bar per pixel, so the 0.024 bar is below its resolution and the two are probably the same measurement; reconciler should decide.
- Cs-90 1 bar (Table 1 1.39): no separate plotted marker could be located near 1 bar (hidden behind neighbouring series), so a separate table row without isotherm id.
- Tool flag "outside axis range" on the 20 bar points (for example 20.0009) is the marker centre lying 0.0009 bar beyond the calibrated 20 bar tick, not an extrapolation.

## Digitization method and deviation (read this)

- Fig. 6 main panel is monochrome: all five series are black, hollow white-filled markers that overlap and hide each other. `digitize_figure.py extract --mode markers` on the raw page image gave unusable blobs (tested with colour #000000; junk test archive not released). So each marker centre was located by fitting the marker outline template (square, circle, diamond, up-triangle shape measured from the legend glyphs, anchor = where the legend line meets the glyph; trimmed outline-darkness fit, frame-aware near the plot frame), verified by overlays of the fitted outlines on 6-24x enlarged page crops, then written into one derived image per series (white page-sized image, red binary disc of radius 2.5 px at each fitted centre, `work/derived/series_<sample>.png`) which `digitize_figure.py --mode markers` read with the real calibration (x ticks 0 and 20 bar at px 710.55 and 1150.48, verified at 10 bar px 930.47; y ticks 0 and 3.6 wt% at px 467.74 and 142.72, verified at 1.8 wt% px 305.5), `--color '#ff0000' --tolerance 60 --roi 700 120 1170 480`. The tool's centroid of each disc differs from the fitted centre by at most 0.4 px (0.02 bar, 0.004 wt%) because of pixel quantization. The tool therefore supplied calibration, archiving and the check, not marker detection; the archived `source_image` of the four `Fig6_main_*` files is the derived image, not the page.
- Fitting check: fitted 20 bar and 1 bar markers reproduce Table 1 (for example UCs-70 20 bar: 3.5249 against 3.52; Cs-90 20 bar: 2.8603 against 2.85).
- `check` results (all PASS, tolerance 5%): UCs-70 at 20 bar +0.14%, at 1 bar -0.62%; UCs-90 at 20 bar -0.01%, at 1 bar +0.11%; UCs-100 at 20 bar -0.13%, at 1 bar -0.50%; Cs-90 at 19.9554 bar (the highest digitized pressure; the tool refuses 20) vs 2.85: +0.36%; inset open2px at 19.95 bar vs 3.65: +0.19%; inset open3px at 1 bar vs 1.34: +1.61%. All six archives have status `passed`.
- Inset: the tool's centroid uses the opened core of each filled triangle (about 1 px above the triangle centre, 0.02 wt%). Inset UCs-90-2 values agree with my template fits of the main-panel open down-triangles at 2-7, 9, 10, 12, 14, 16 bar within 0.01 wt%, at 18 bar within 0.02 wt% and at 20 bar within 0.012 wt% (those main-panel fits are not archived and are not rows).
- `digitization_uncertainty_wt_pct` left empty as instructed. Digitized rows have `extraction_confidence` 3 (2 below 1.2 bar where markers overlap), table rows 5.

## Markers counted but not extracted

- UCs-70: two markers on the y-axis line, fitted centres (710.25, 441.75) and (711.75, 421.75), about 0.00 and 0.055 bar, 0.288 and 0.509 wt%: pressure not determinable at 1 px (0.045 bar) resolution, not extracted. Counted in `isotherm_point_count` = 20.
- UCs-90: one marker at (710.5, 459.5), about 0.00 bar, 0.091 wt%, same reason; count 17.
- UCs-90-2 inset: four filled markers overlapped on the y-axis line at pixel (922.4, 441.2), (922.5, 430.2), (922.8, 422.6), (923.0, 415.6) (0.055, 0.294, 0.456, 0.608 wt%, the last blob of 28 px may hold two markers), pressure not determinable; counted (4) in `isotherm_point_count` = 23. The merged blob at (932.7, 383.5) in the 2-px run (0.8 + 0.98 bar) was replaced by the two markers of the 3-px run. The inset legend filled triangle (pixel 1100.0, 336.0) is a legend glyph, not data.
- UCs-90-2 desorption branch (open down-triangles in the inset): the open markers lie behind the filled adsorption markers with an offset of about 0.1 to 2 px (0.00 to 0.04 wt%) and show only as a thin crescent above the filled marker, so no marker centre can be separated; none extracted, none counted. The paper says desorption shows virtually no hysteresis. This means the UCs-90-2 desorption rows are missing.
- UCs-90-2 main panel: the marker at 8 bar is completely hidden behind the UCs-70 diamond and at 10-18 bar partly behind diamonds; the inset gives all of them.
- Markers hidden or overlapped and not separable (not counted): UCs-100 below 0.43 bar (a stack of overlapped square edges near (712, 430)); Cs-90 between 0.2 and 3 bar (any 0.4-1 bar markers are hidden behind diamonds, circles and squares); No marker found at 1.5 and 2.5 bar (UCs-70, UCs-90), at 7 and 9 bar (UCs-70, UCs-90) and at 3 and 5 bar (UCs-90); UCs-100 has markers at 1.5 and 2.5 bar.

## Values seen and not extracted

- USY zeolite row of Table 1 (SBET 701.5, VTotal 0.405, VMicro 0.304, VMeso 0.101): zeolite, not a carbon sorbent, and no H2 value ("-"). No row.
- Text range "adsorption uptakes of hydrogen at 1 bar vary between 1.1 and 1.4 (ID/IG) wt%" (main p.5): a range summary of Table 1 values, not a measurement. No row.
- Conclusions "UCs-90-2 is up to 3.6 wt% at 77 K and 20 bar" (main p.5): rounding of the Table 1 value 3.65, noted on that row. Abstract "surface area of 1200 m2/g": rounding of 1218.6 in Table 1.
- Text "BET surface areas ... up to 1038 m2/g and 0.88 cm3/g", "700 m2/g and 0.417 cm3/g" (Cs-90): characterization repeats, not H2.
- "previous reported ... 603 m2/g [26]": another paper's value, not H2.
- Fig. 1 (XRD), Fig. 2 (N2 isotherms at 77 K, adsorption and desorption), Fig. 3 (NLDFT pore size distributions), Fig. 4 (SEM), Fig. 5 (Raman): not H2 isotherms, not digitized, no H2 value shown that Table 1 lacks.
- UCs-60 and UCs-80 appear only in Table 1 (no H2 curve in Fig. 6).
- Average pore diameter: not given in a table; PSD maxima mentioned in text (about 1.4 nm for zeolite-templated carbons) are not tabulated per sample, left empty.
- No sample mass, free-volume calibration gas, uncertainty or replicate result is printed; `replicates_reported` false. The balance resolution (+-0.1 ug) is not an uncertainty of the uptake.

## Coding notes

- Basis: paper names no basis; `uptake_type` unspecified, `basis_stated` false, `basis_inferred` excess (gravimetric with stated buoyancy correction). wt% convention not defined: `unknown` / `none`.
- UCs samples `templated_carbon` / `template_synthesis`; Cs-90 (no zeolite, same infiltration and carbonization) coded `other` / `carbonization`. HF/HCl treatment entered under `purification_method` (template removal).
- `bet_consistency_criteria_stated` false: the paper gives a reason for the 0.02-0.25 range but names no consistency criteria. `area_same_sample` yes (N2 area after 300 C degas on the same carbons; H2 degas was 200 C).
- `measuring_lab_id`: corresponding author Zhao (asterisk), first affiliation (a) Qingdao Institute of Bioenergy and Bioprocess Technology, Chinese Academy of Sciences (an institute, no university).
- Header has 97 columns (read from the instruction file line 301 and asserted in the script); `validate_row_detail.py --errors-only`: no errors (warnings only: `uptake_type` unspecified on every row).
- Scripts, derived images and fits are in the work directory (`work/gen_rows.py`, `work/final_anchors.py`, `work/build_derived.py`, `work/run_tool.sh`).
