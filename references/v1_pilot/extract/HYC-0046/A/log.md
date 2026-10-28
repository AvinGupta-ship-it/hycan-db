# HYC-0046 (Kabbour 2006), extractor A: log

63 rows written. `validate_row_detail.py rows.csv --errors-only` reports 0 errors and 0 warnings.

## Extracted from

- Table 1 (page 4 image), H2 (wt%) column, 9 values: ACA 1460, 1700, 2000, 2550, 3200 m2/g; Co-CA 800 and (1050) C; Ni-CA 800 and (1050) C. Rows M1 to M9. M1, M4 and M5 also stand for the highest marker of isotherms I2, I4 and I5 (see decisions).
- Text, page 1 right column (Fig. 1 paragraph): "the sample with the surface area of 330 m2/g adsorbs 0.8 wt% at 20 bar". Row M10.
- Text, page 1: "the 3200 m2/g sample adsorbs 5.3 wt% hydrogen at 30 bar pressure" and abstract "5.3 wt% at 30 bar". Same value and pressure as the Table 1 3200 entry; recorded once in M5, no duplicate row.
- Text, page 1 and 3: Co "saturation values of ~2.1 wt% for each sample", Ni "2.3 wt% vs 2.0 wt%". Same values as Table 1; recorded once each in M6 to M9.
- Text, page 3: BET areas of the Ni-CA samples, 970 m2/g (800 C) and 1100 m2/g (1050 C). Carried as characterization on the Ni rows (M8, M9).
- Table 1 / Fig. 2 / abstract: ACA BET areas 1460, 1700, 2000, 2550, 3200 m2/g and 330 m2/g for the as-prepared aerogel. Carried on the sample's rows.
- Figure 1 (page 3 image), five 77 K adsorption isotherms, digitized with `digitize_figure.py extract --mode markers`:
  - 330 m2/g (inverted triangles): 8 separated markers, rows M11 to M18.
  - 1460 m2/g (diamonds): 10 separated markers; marker 9 is M1; other 9 are M19 to M27.
  - 2000 m2/g (squares): 11 separated markers, rows M28 to M38.
  - 2550 m2/g (circles): 16 separated markers; marker 15 is M4; other 15 are M39 to M53.
  - 3200 m2/g (triangles): 11 separated markers; marker 10 is M5; other 10 are M54 to M63.
  - Calibration read from pixel rows and columns of the page-3 image: x ticks at px 730, 912, 1093 for 0, 20, 40 bar (912 is the residual tick; predicted 20.055 bar); y ticks at px 973, 841, 753 for 0, 3, 5 wt% (841 is the residual tick; predicted 3.000). Tick lines are single-pixel and crisp.
  - Marker count extracted equals the count of separated markers I classified for each series (8, 10, 11, 16, 11); no group was rejected by the tool.
  - `check` against stated values, all passed: 3200 at 30 bar vs 5.3 (digitized 5.199, 1.9%, tol 5%); 330 at 20 bar vs 0.8 (digitized 0.841, 5.1%, tol 8%, set from the one-decimal printed rounding of 0.8); 2550 at 30 bar vs 5.0 (5.004); 2000 at 30 bar vs 4.2 (4.210); 1460 at 30 bar vs 3.5 (3.433, 1.9%). The paper gives no pressure for the last three, only "saturation occurs typically at ~30 bar".
  - Archives: `digitizations/HYC-0046_fig1_{330,1460,2000,2550,3200}.json`.

## Figure 1 method (why derived images)

Figure 1 is greyscale and the series differ only by marker shape, so the tool's colour mask cannot separate them. `digitizations/work/make_series_images.py` copies pixels of the page image, unchanged and on the same pixel grid, into one image per series (black on white), classing each connected pixel group by shape (bold ring 7 to 9 px = circle; bold ring 5 to 6 px = square; thin with base bar = triangle; thin with top bar = inverted triangle; thin with no bar = diamond; classes calibrated on the legend and isolated markers). The legend block and tick marks are blanked. The tool then ran on each derived image (`digitizations/work/fig1_series_*.png`; sha256 recorded in each archive) with `--open-px 1` because there are no joining lines and the default 3 px opening would erase the 1 px marker strokes. The classification was checked on a colour-coded overlay.

Known biases: a marker's centroid is the centroid of its outline pixels, so an up-triangle (base bar at the bottom) reads about 1 px (0.02 wt%) low. Points above the highest labelled y tick (5 wt%) are linear extensions of the calibrated axis by under 0.3 wt% (the tool flags them); the flagged markers are 3200 markers 7 to 9 (rows M60 to M62); 3200 marker 10 and 2550 marker 15 are also flagged but are replaced by M5 and M4, which carry the table values.

## Seen but not extracted

- Overlapped markers of Figure 1 near the y axis (p below about 1.7 bar for the four carbon-aerogel isotherms; below about 3.5 bar for the 330 m2/g isotherm). Markers there fuse into groups of 40 to 170 pixels and cannot be separated by shape or colour at this resolution (about 7 px markers). Their groups are listed with pixel centroids in `digitizations/work/series_assignment.json` ("unassigned"). Estimated number of missing markers by shape fragments (plus or minus 3): 330 about 9, 1460 about 8, 2000 about 7, 2550 about 5, 3200 about 5. These estimates are what makes `isotherm_point_count` 17, 18, 18, 21, 16 (separated plus estimated); they are counts, not extracted values.
- Table 1 ΔH column (6.7, 6.5, 6.4, 6.4, 6.2 kJ/mol for the ACAs; 7.5 (7.2) Co and 7.0 (7.1) Ni): differential enthalpy of adsorption, not an uptake value, no schema field.
- Text ">7 kJ/mole" and abstract "~5 to 7 kJ/mole": same reason.
- Figure 2 (page 4): saturation value vs BET area. Its y values repeat Table 1 and the 330 m2/g text value. Its x values for the Co-CA samples are the only place those areas appear (the Ni areas are printed in the text); they are plotted points, not printed numbers, and Figure 2 is not an isotherm, so they were not digitized. The two Co rows therefore carry `surface_area_method = not_reported`.
- Figure 2 dashed line (1 mass% per 500 m2/g converted to wt%): a reference line, not data.
- Page 5 table-of-contents graphic: coloured, lower-resolution copy of Figures 1 and 2. Not digitized (duplicate).
- Figure 1S (adsorption isotherms of the Ni- and Co-modified aerogels, supporting information): referenced on page 1 and 4 but not part of the input, so no Co or Ni isotherm points were extracted. Their saturation values are in Table 1.
- Statements about other work: "1% for every 500 m2/g of surface area", "~35 bar" (refs 2 to 4), "up to 5 wt%" summary, "comparable to the highest value we have measured in an activated carbon (ref 12)" and the 2630 m2/g single-graphene-sheet figure. Not measurements of this paper's samples.

## Coding decisions that reconciliation may want to check

- Sample labels. ACAs use the Table 1 label ("ACA (1460 m2/g)"); the Fig. 1 legend form ("1460 m2/gm") is in the description. The 330 m2/g sample has no table label; label is the Fig. 2 legend text "as-prepared aerogel (330 m2/gm)". Table 1 prints "Co-CA-800oC (1050oC)" as one row for two samples; I used "Co-CA-800°C" and "Co-CA (1050°C)" (and the Ni equivalents) so the two samples have distinct labels. The second label is derived from the parenthesised value, not printed as such.
- 330 m2/g sample is an uncarbonized resorcinol-formaldehyde aerogel (`material_class = other`). Protocol section 3 excludes uncarbonized polymers as carbon sorbents; extracted because the scope asks for every uptake value in the paper.
- wt% convention W2, source `stated`. Basis: "we express the saturation value in wt%, which yields a slightly lower quantity than values expressed in mg of sorbed hydrogen per gm of sorbent" and the Fig. 2 caption "1 mass% sorption per 500 m2/g, converted to wt%". No formula is printed, so this is the one coding most worth checking; the alternative is `unknown` / `none`. Applied to digitized rows too, since the Fig. 1 axis is the same wt% quantity.
- Basis: `basis_stated = false` (paper says "excess" and "surface excess" but never defines it and gives no second basis); `basis_inferred = excess` by name and by volumetric default; the quote is stored in `basis_evidence` as support.
- Pressure of Table 1 values. Table 1 prints none. Where the value matches exactly one marker of the Fig. 1 isotherm (1460, 2550, 3200), the table row takes that marker's place in the isotherm (protocol section 9: table value used, figure supplies the other points); pressure is the digitized pressure of that marker (1460, 2550) or the printed 30 bar (3200, where the digitized marker is at 28.8 bar). For 2000 the two highest markers both equal 4.2, so the table row stays a single value with `pressure_unstated = true` and both markers are kept as figure rows. 1700, Co and Ni have no Fig. 1 isotherm, so `pressure_unstated = true`; the paper's "typically ~30 bar" is quoted in notes, not used as a value.
- 330 m2/g text value (M10) is not tied to a marker (none at 20 bar); kept as a single value and all eight markers kept.
- `value_kind = measured` for Fig. 1 markers and for rows equal to a marker within the printed rounding; `unclear` for 1700, Co, Ni and the 330 text value.
- Surface-area typing: areas are called BET by the Fig. 2 caption (all samples) and by the abstract (3200). Probe gas `N2` only for the Ni rows ("not adequately measured by N2 BET measurements" is written about them); `unspecified` elsewhere. `area_same_sample = yes` because the paper attaches each area to the sample whose uptake it reports; no degassing state is given. No BET range or consistency criteria are stated.
- Laboratory: `Ahn group, California Institute of Technology`. The paper does not say where the isotherms were measured; there are two corresponding authors (Baumann, LLNL; Ahn, Caltech); the Sieverts apparatus is cited to a Caltech paper (ref 10, Bowman, Luo, Ahn et al.) and the first author is at Caltech.
- `instrument_identified = false`: the apparatus is "a volumetric Sieverts apparatus" with a literature citation only; no maker, model or home-built description. `calibration_described` and `replicates_reported` false; no sample mass, degassing, H2 purity or free-volume calibration is stated.
- `metal_element` used for Co and Ni (nanoparticles in the aerogel network); loadings not stated.

## Process note (blind-extraction integrity)

The scratchpad folder was shared with another extraction agent, who saved a file with the same name (`build_rows.py`) over mine. I ran it twice before noticing; it printed a row count (62) and wrote to the other agent's output directory (it regenerated that agent's `rows.csv` from its own script; I opened no output file of theirs). Before that, a small text patch of mine read that file and wrote it back with identical content (the patch strings were not found), which could in principle have undone an edit made by its owner in the same instant. I also printed the first 600 and last 400 characters of that file, which showed its column list, the output path, note-variable names (W2NOTE, LABNOTE, SAT_NOTE) and one note sentence quoting the Ni-CA text. None of this changed any value or coding in this extraction; all decisions above were made before it. My generator now lives in a uniquely named private scratch folder.
