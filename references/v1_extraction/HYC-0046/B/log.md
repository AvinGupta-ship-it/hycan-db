# HYC-0046 extraction log (agent B)

Input: five page images (main-1 to main-5) of the LLNL preprint UCRL-JRNL-227848. main-1 is a cover page and main-2 a disclaimer, with no data. The supporting information (Figure 1S) is not in the input.

## Sources extracted

- Table 1 (main-4.png): the H2 (wt%) saturation values at 77 K for ACA (1460, 1700, 2000, 2550, 3200 m2/g), Co-CA-800°C (1050°C) and Ni-CA-800°C (1050°C). That makes 9 values, one row each. The values for 1460, 2000, 2550 and 3200 are merged with the highest digitized point of their Figure 1 isotherm. Basis: p.3 says the saturation values are "taken from the surface excess adsorption isotherms", and p.4 defines them as "the maximum amount of hydrogen sorbed in the surface excess isotherm trace".
- Text p.3 (main-3.png): "the 3200 m2/g sample adsorbs 5.3 wt% hydrogen at 30 bar pressure". This is the same value as Table 1 ACA (3200), and the printed pressure (30 bar) is used on the merged row. The digitized highest point is at 28.8 bar.
- Text p.3: Co-modified CAs "saturation values of ~2.1 wt% for each sample", and Ni "(2.3 wt% vs 2.0 wt%)". These are the same values as Table 1 and are recorded on the Table 1 rows, coded exact as in the table.
- Text p.3: Ni-CA BET areas "970 m2/g vs 1100 m2/g" (800 vs 1050 °C) are recorded on the Ni rows.
- Text p.4 (main-4.png): "yielding up to 5 wt%" (CAs up to 2550 m2/g) and "gravimetric density of 5.3 wt%" (3200 m2/g). These are the same as the Table 1 values and add no rows.
- Abstract (main-5.png): "saturation value of 5.3 wt% at 30 bar pressure at 77 K" (3200 m2/g). This is the same as the 3200 row.
- Figure 1 (main-3.png, single panel, 77 K adsorption isotherms): every marker of the four carbon series is digitized. The archives are digitizations/fig1_3200.json (15 markers), fig1_2550.json (21), fig1_2000.json (18) and fig1_1460.json (17). Tool counts equal the markers counted. Each archive's `check` passed against the Table 1 value (3200 at 30 bar vs 5.3, and the others at the digitized pressure of the merged point).

## Figure 1 digitization method

- Axes were calibrated on the page image main-3.png. x: 0 bar at px 730 (frame/tick) and 40 bar at px 1093, with the check tick 20 bar at px 912 (error 0.28%). y: 0 wt% at px 973 and 5 wt% at px 753 (right-side ticks), with the check tick 3 wt% at px 841 (error 0). The tick positions were found by scanning pixel rows and columns.
- Every series is printed in black, and the series are told apart only by marker shape. So per-series images were made in the work directory: each marker was located by template matching of its shape (triangle, circle, square, diamond, inverted triangle), and the original page pixels inside its 1-px-dilated template footprint were copied. Pixels on other markers' strokes and on the axis line/ticks were excluded. `digitize_figure.py extract --mode markers` (colour #000000, tolerance 430, opening 0, ROI 724 715 1095 976) was run on each image. The archive `source_image` is that derived image, and the scripts are in the work directory.
- The colour table-of-contents copy of Figure 1 (main-5.png) was used only to decide which series each marker in the dense low-pressure cluster (p < 3 bar, near the y axis) belongs to. It has no labelled y ticks and was not digitized.
- Markers at p < 2 bar overlap heavily: 3200 points 1-5, 2550 points 1-6, 2000 points 1-8 and 1460 points 1-7 (their rows have extraction_confidence 2). Their centroids come from their own template footprints and are uncertain by about 1 px (about 0.1 bar, 0.02 wt%). Markers on the y-axis line had the axis pixels removed. The 3200 and 2550 markers at about 36 bar overlap each other.
- Hidden markers cannot be excluded. Additional markers fully covered by others at p < 0.1 bar next to the y axis may exist, especially for 3200 m2/g, whose lowest visible point is about 1.05 wt%. Counts are of visible markers.
- A short grey diagonal at px (745-747, 880-882) belongs to no identified marker. It was treated as a rendering artifact, not a marker. The 1460 point at 1.26 bar / 2.00 wt% sits next to it, and its position is the less certain of that cluster.
- Points above the highest labelled y tick (5 wt%) use the linear y calibration extrapolated within the plot frame (frame top = 5.82 wt%). These are four 3200 points and the 2550 point at 30.4 bar.
- Only adsorption traces are plotted ("For clarity, only adsorption isotherm traces are shown ... adsorption and desorption data were identical"). Desorption points are not shown and could not be counted, so isotherm_point_count is the number of plotted adsorption markers.
- The 2000 m2/g maximum is a near tie: 4.2159 wt% at 28.2 bar against 4.2035 wt% at 34.5 bar. The 28.2 bar point was taken as the saturation point.

## Values seen but not extracted

- Figure 1, 330 m2/g series (18 markers) and text p.3 "The sample with the surface area of 330 m2/g adsorbs 0.8 wt% at 20 bar": not extracted. The sample is the uncarbonized resorcinol-formaldehyde organic aerogel (Fig. 1 caption: "was not carbonized"), an uncarbonized polymer and not a carbon sorbent (§3). Its markers were digitized only to separate the series. Those archives are in the work directory (digitizations_not_extracted/), not the output.
- Figure 2 (main-4.png): saturation value vs BET surface area. It is not an isotherm and was not digitized. Its values are the ACA, Ni and Co saturation values (all in Table 1) and the 330 m2/g point (0.8 wt%, not carbon). It also shows graphically the BET surface areas of the Co-modified aerogels (800 and 1050 °C, roughly 900-1100 m2/g), which the text and table do not print. Those Co rows therefore have surface_area_method = not_reported. The dashed line is a model (1 mass% per 500 m2/g converted to wt%), not a measurement.
- Table 1 ΔH (kJ/mol) differential enthalpies at zero coverage: ACA 1460 6.7, 1700 6.5, 2000 6.4, 2550 6.4, 3200 6.2, Co-CA-800°C 7.5 (1050°C 7.2), Ni-CA-800°C 7.0 (1050°C 7.1). Not extracted because they are not uptake values.
- Text p.4 ">7kJ/mole" (metal-modified) and abstract "~5 to 7 kJ/mole": enthalpies, not uptake.
- Text p.3 "We can generally expect a gravimetric density of 1% for every 500 m2/g ... in activated carbons" and p.4 "1% hydrogen sorbed for every 500 m2/g": a literature scaling rule, not a measurement.
- Text p.4 "saturation occurs typically at ~30 bar for higher surface area materials": a general statement, not attached to one sample. It was not used as the pressure of the 1700, Co and Ni rows, which are pressure_unstated.
- Text p.4 "comparable to the highest value we have measured in an activated carbon,12": no value printed.
- Text p.3 "primary particles with characteristic diameters between 3 and 25 nm": particle size, not a pore diameter. Not recorded.
- Text p.4 "high-resolution isotherm measurements at low pressure (in the range 0-2.5 bars)": these isotherms are not shown separately. No values.
- SI Figure 1S (77 K isotherms of the Ni- and Co-modified CAs): not in the input, so its points were not extracted. The Ni/Co rows carry only the Table 1 saturation values (value_kind unclear, no pressure).
- Table-of-contents graphic (main-5.png): a colour duplicate of Figures 1 and 2. Not digitized.

## Coding decisions

- wt% convention W2, source stated. p.4 says "we express the saturation value in wt%, which yields a slightly lower quantity than values expressed in mg of sorbed hydrogen per gm of sorbent", with mass% defined as "(mg hydrogen)/(g aerogel)". Only W2 is lower than mg/g.
- Basis: the paper names "excess" ("Hydrogen adsorption/desorption excess sorption measurements were performed with a volumetric Sieverts apparatus") but does not define it, so basis_stated is false and basis_inferred and uptake_type are excess.
- measuring_lab_id: the paper does not say which laboratory made the H2 measurements; the Sieverts apparatus is cited to ref. 10, Bowman, Ahn, Fultz et al. The first-marked corresponding author is Baumann (‡: Lawrence Livermore National Laboratory, no university), so the lab is "Baumann group, Lawrence Livermore National Laboratory". The Caltech authors (Kabbour, Saulnier, Ahn) may have measured; the paper does not say.
- Instrument: a generic "volumetric Sieverts apparatus" with no model or description, so instrument_identified is false. No free-volume calibration, degassing, sample mass, H2 purity or uncertainty is stated.
- BET probe gas N2 (p.4 "N2 BET measurements"). No BET range or consistency criteria are stated. No pore volumes are reported.
- Sample labels are taken from Table 1. The 1050 °C metal samples appear there only as the parenthetical entries of the rows "Co-CA-800°C (1050°C)" and "Ni-CA-800°C (1050°C)" and are labelled Co-CA-1050°C and Ni-CA-1050°C.
