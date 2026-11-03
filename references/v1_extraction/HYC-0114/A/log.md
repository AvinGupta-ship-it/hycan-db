# HYC-0114 extraction log (agent A)

Paper: Matamba et al., Fuel 392 (2025) 134926. Inputs: main.txt (pdftotext layout) and page images main-1 to main-9. No supplementary file.

## Extracted from

- Main text, Section 3.4 (p. 6): ambient (30 °C) uptake at 8.28 and 66.33 bar for 700, 800 and 900 °C biochar (0.39/1.70, 0.33/1.77, 0.63/2.50 mol/kg), rows M1-M6, `text_direct`. For 800 and 900 °C the paper gives the range only as "with the same pressure increase" after the 700 °C sentence (8.28 to 66.33 bar); pressures taken from there.
- Abstract (p. 1) and Conclusions (p. 8): 2.50 mol/kg at 66.33 bar (900 °C, ambient). Same measurement as M6, no separate row.
- Main text Section 3.4 (p. 6) and Conclusions (p. 8): 15.59 mol/kg at 46.71 bar, 900 °C biochar at LN2 temperature (-196 °C), row M12, `text_direct`, merged with the sixth marker of the Fig. 8 lower panel (digitized 46.556 bar, 15.589 mol/kg; printed pressure within 0.16 bar, within 2% of the plotted point).
- Fig. 8 lower panel (p. 8), series 900-LN2, the only 77 K isotherm: 6 markers digitized with `digitize_figure.py extract --mode markers`, archive `digitizations/HYC-0114_fig8_900-LN2.json`. Rows M7-M11 are markers 1-5; marker 6 is merged into M12. Calibration: x ticks 0 to 50 bar, y ticks 0 to 18 mol/kg, centroids of tick marks in the page image; third-tick check (x = 20 bar, y = 9 mol/kg) within 0.06% of the tick. `check` against the stated value (15.59 at the last marker) passed (difference 0.01%; run at x = 46.556 because the tool requires a point inside the digitized range).
- Table 2 (p. 2): BET area (Ar at -185.86 °C, "BET*"), total pore volume and average pore width for the 700, 800 and 900 °C biochar, copied onto every uptake row of the sample. Section 2.2: textural analysis in Ar at -185.86 °C, Tristar II 320; probe gas coded Ar for area and pore volume. BET P/P0 range and consistency criteria not stated.
- Section 2.4 (p. 3): instrument (automated Sieverts "PCT Pro", no manufacturer named, so `instrument_identified = false`), He volume calibration at 4-5 bar (temperature not stated), H2 purity 99.999 mol%, degassing, sample mass 0.25-0.50 g per run.

## Coding decisions worth a second look

- Sample numbering: S1 to S3 are 700, 800 and 900 °C biochar, the samples with rows. WS and 500 °C biochar are not numbered because they have no uptake value.
- `material_class = other`: biochar, no activation. XRD (Fig. 3c) finds SiO2, Fe2O3, KCl and SiC in the 700 and 800 °C biochar; these are inherent ash minerals, not an added phase, so not `composite`. Biochar elemental composition is not reported (Table 1 is the raw wheat straw only).
- `area_same_sample = yes`: BET area is reported for the same pyrolysis-temperature biochar used for H2; degassing state for the Ar analysis is not stated.
- Degassing: coded the in-instrument step (30 min at 30 °C) as the degas before the H2 test because it is the only step with both temperature and duration tied to the adsorption test. The oven drying at 80 °C for 12 h and the 12 h vacuum degas (temperature not stated) are in `notes`.
- Basis: the paper calls the value "adsorption capacity"/"adsorption" and never names excess, absolute or total, so `uptake_type = unspecified`, `basis_stated = false`, `basis_inferred = excess` (volumetric Sieverts default).
- Temperature: "-196 °C" is a printed number, so 77.15 K with `temperature_inferred = false`. 30 °C stored as 303.15 K.
- `value_kind = measured` for all rows. For the ambient maxima no digitized point exists to compare against; the paper gives the pressure of the measurement (66.33 bar, inside the stated 0 to 70 bar range).
- `replicates_reported`: true for the 900-LN2 isotherm (error bars in the figure, no numeric values or definition); false for the ambient rows (no error bars or numbers shown in the 3D chart). `uncertainty_wt_pct` left empty because no numeric uncertainty is printed.
- Pyrolysis pressure of the biochar used for H2 uptake is not stated (the paper varies 1.01 to 30 bar); recorded in `material_description`.
- `isotherm_point_count`: 6 for I4 (the line starts at the origin where only a tiny faint square, not a full marker, is drawn; origin not counted). Left empty for I1-I3 (3D ribbon chart with no markers).
- Isotherm ids: I1 = 700 °C ambient, I2 = 800 °C ambient, I3 = 900 °C ambient, I4 = 900 °C at LN2. The text values for I1-I3 are given for the samples plotted in Fig. 8 (upper panel) with "(Fig. 8)" cited for the tests; they could not be matched to plotted points because that panel cannot be digitized.

## Seen, not extracted

- Abstract: "15.29 mol/kg at 46.21 bar" (LN2). Conflicts with Section 3.4, the Conclusions and the plotted marker (15.59 at 46.71 bar; digitized 15.589 at 46.556 bar). Treated as a misprint of the same measurement; no separate row. Noted in M12.
- Fig. 8 upper panel (3D ribbon chart, 700/800/900 °C at 30 °C, pressure axis labelled 10 to 60 bar, z axis 0 to 2.5 mol/kg): not digitized. The projection is oblique, the ribbons sit at different depths from the back-wall gridlines and the z axis, and no markers are drawn, so no valid linear axis calibration exists. The highest-pressure value of each ribbon comes from the text (66.33 bar). Intermediate steps of the three ribbons (roughly eight per ribbon, count not certain) are not given in the text and are not extracted.
- Fig. 8 lower panel: error bars on all six points (not digitized; no numeric values given); the (0,0) vertex of the line (not a measured point).
- Digitization note: the markers are half-filled circles, so the tool's centroid sits about 2 px (about 0.14 bar) to the left of the circle centre, as the printed 46.71 bar against the digitized 46.556 bar and the error-bar positions show. The y values are unaffected (last marker 15.589 against the printed 15.59). I kept the tool's output unaltered. The tool also found one extra red fragment of the connecting line at pixel (894, 617), x about 42.09 bar, y about 15.23 mol/kg; it is not a marker and was rejected with `--marker-min-px 10` (recorded in the archive under `rejected_markers`).
- Table 2: wheat straw (WS) BET 2.49 m2/g, total pore volume 0.0040 cm3/g, average pore width 6.40 nm, and 500 °C biochar BET 4.61 m2/g, 0.0080 cm3/g, 6.97 nm. No H2 uptake value for either (Section 2.4 says tests were run "for all the samples", but Fig. 8 and the text give 700, 800 and 900 °C biochar only), so no rows.
- Table 1 (proximate and ultimate analysis of raw wheat straw), Table 3 (product yields), Figs. 1, 4, 5, 6, 7 (pyrolysis rig, carbon conversion, pyrolysis gas and syngas composition): H2 produced in the pyrolysis gas (for example 86.07 vol% at 800 °C and 30 bar) is gas production, not H2 uptake by a sorbent; not extracted.
- Fig. 2 (Ar isotherms of WS and biochar, volume adsorbed in cm3/g STP against P/P0): Ar adsorption at -185.86 °C, not H2; not extracted.
- Fig. 3 (FTIR, TGA, XRD): characterization only. Functional groups left empty (text says high temperatures destroyed all functional groups; spectra of the 700 to 900 °C biochar are near flat apart from a weak band near 1000 cm-1 for 700 °C).
- Introduction: DOE targets (5.5 wt%, 40 g/L); not measurements.
