# Extraction log HYC-0129 (agent A)

## Extracted from
- Fig. 6 (main.txt p. 629, PDF page 5; H2 adsorption/desorption at 77 K, 0 to about 1010 mbar, y axis "Volume (mmol/g)"): 65 rows. 34 adsorption (filled diamonds), 31 desorption (open diamonds). One sample, one run, isotherm I1. Archives: digitizations/HYC-0129_fig6_adsorption.json, digitizations/HYC-0129_fig6_desorption.json.
- Sample characterization used on every row: text p. 629 (Langmuir s.s.a. about 560 m2/g from the H2 77 K isotherm, 12.4 A2 per molecule); Sect. 2.5 (Autosorb-1, degas overnight at 573 K, about 1e-7 mbar); Sect. 2.1, 2.3 (precursor and pyrolysis).

## Digitization method and caveats (Fig. 6)
- Axis calibration: x 0 mbar at px 675, 1000 mbar at px 1119, check tick 500 mbar at px 897 (error 0); y 0 mmol/g at px 1410, 6 mmol/g at px 1169.5, check tick 4 mmol/g at px 1249.5 (relative error 0.1%). Tick pixels found from pixel rows and columns of the page image (gridlines at y = 1169.5, 1249, 1331, 1410; x ticks 675, 720, 764, 808.5, 853, 897, 941, 986, 1030, 1075, 1119). The axis tick labels are consistent.
- The markers are black diamonds about 9 px wide on a 1241 x 1648 page image and overlap heavily; open (desorption) diamonds are drawn over filled ones with white fill. `digitize_figure.py` on the raw page image merged overlapping filled markers into blobs and cannot see open markers (its 3 px opening removes their 1 px outlines). I therefore located marker centres by template fitting on the page image (open diamonds: white interior plus dark ring; filled diamonds: forward-model fit of a filled diamond of half-diagonal 4 px, accounting for occlusion by open diamonds), checked the fits on enlarged overlays, then drew one 3 x 3 px black square at each centre on a white canvas of the page's size (work/synth_ads.png, work/synth_des.png) and ran `digitize_figure.py extract --mode markers` on those derived images with the calibration above. The archives' `source_image` therefore points to those derived images, not to the page. Centres are quantised to whole pixels (open-diamond centres at .5 px rounded), about +/- 0.5 px, that is about 1 mbar and 0.0125 mmol/g.
- Marker count check: 34 centres in, 34 extracted (adsorption); 31 in, 31 extracted (desorption). The counts equal the markers I resolved, not the true number of markers on the plot (see below).
- Points beyond the top labelled tick (6 mmol/g) are flagged by the tool as outside the calibrated range; the axis is linear and the plot continues above the 6 tick, so these are read on the same linear calibration.
- Not separable: a stack of overlapping filled markers at p below about 12 mbar and below about 2.3 mmol/g (pixel x 673 to 681, y 1360 to 1410, about 10 or more markers, only the left and right tips of individual diamonds are visible). Not extracted. I extracted the 7 markers in the stack above y = 1360 whose left tips and widths are distinguishable (4.5 to 11.3 mbar); they are confidence 2. `isotherm_point_count` = 65 is therefore a lower bound.
- Partly hidden filled markers behind open markers, fitted from visible slivers, confidence 2: adsorption at about 40.5, 668.9 and 693.7 mbar. Other filled markers hidden behind open ones may exist (for example between 407 and 650 mbar, where only the desorption markers and two connecting lines are clearly visible; and near 862 mbar, a gap of 18 px between filled markers at 842 and 883 mbar). I did not add markers I could not see.
- The black blob at about 94.6 mbar (adsorption) is longer than one diamond and may be two overlapping markers; recorded as one.
- Paper-stated value check (`digitize_figure.py check`, step 6): not run, because the paper prints no H2 uptake value to check against (the 4.2 and 4.5 mmol/g CO2 values are for another gas).

## Values seen but not extracted
- Fig. 7 and text: CO2 4.2 mmol/g (298 K) and 4.5 mmol/g (273 K) at 20 bar, N2 and CH4 isotherms: not H2.
- Text: N2 uptake at 77 K "negligible", no value: not H2.
- Fig. 8, Tables 1 to 5: kinetic selectivity, diffusion coefficients, permeances, permselectivities: not H2 uptake. H2 permeance values (Table 2, 3, abstract 8.2 GPU) are transport data, not uptake.
- Precursor P84 polymer hollow fiber (Tables 3, 5, Fig. 3, Fig. 5): no H2 uptake value, no row.
- CO2-derived BET and Langmuir s.s.a. "between 525 and 625 m2/g" (22.2 A2 per molecule), no single value: recorded in notes only.
- Fig. 5 (TGA, weight loss 34.1%), Fig. 4 and Fig. 3 (SEM), Fig. 8: not H2 isotherms.

## Coding decisions
- `material_class` = other (carbon molecular sieve hollow fiber membrane; no vocabulary entry fits); `synthesis_method` = pyrolysis (Sect. 2.3 "Pyrolysis procedure"; the precursor polymer is commercial, the carbon is the authors' own, so not `commercial`).
- Sample has no printed label: `(unlabelled 1)`.
- Basis: the paper says "excess isotherms" only for the gravimetric IGA runs (CO2, N2, CH4), not for the Autosorb H2 isotherm, so `basis_stated` = false, `uptake_type` = unspecified, `basis_inferred` = excess by the volumetric default.
- `uptake_wt_pct` = 0.201588 x mmol/g (W1, computed_from_other_unit); the paper gives no wt% for H2.
- `surface_area_method` = Langmuir, probe gas `other` (H2 at 77 K), `area_same_sample` = yes (computed from the H2 isotherm of this sample). No BET area for H2 (paper: BET with H2 is inconsistent); BET fields coded false.
- Degas: 573 K stored as 299.85 C; "overnight" has no number, so duration is empty; about 10^-7 mbar stored as 1e-05 Pa.
- `instrument_identified` = true (Quantachrome Autosorb-1); `calibration_described` = false (no free-volume determination stated for H2); no uncertainty, no repeats.
- `measuring_lab_id`: corresponding author E. P. Favvas (marked &), first affiliation Institute of Physical Chemistry, NCSR "Demokritos" (no university named).
- Desorption rows `isotherm_branch` = desorption; adsorption and desorption share I1 (one run).
