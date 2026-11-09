# HYC-0121 extraction log (agent B)

Input: 6 main-article page images (main-1.png to main-6.png); no supplementary file. Rows: 64 (63 digitized, 1 text). Run paused by the operator between digitization and row writing; rows written 2026-11-09 (extraction_date), digitization archives created 2026-11-03 UTC.

## Sources extracted

- Figure 7 (main-4.png, p. 2291), H2 sorption isotherms at -196 °C, x = pressure (mm of Hg), y = wt% H2. Three series, all digitized (77 K isotherms):
  - TiC-CDC, filled squares (S1, I1): 22 markers extracted, archive `digitizations/fig7_TiC-CDC.json`.
  - TiC-CDC H2 annealed, open squares (S2, I2): 22 markers extracted, archive `digitizations/fig7_TiC-CDC_H2_annealed.json`; highest-pressure marker merged with the text value 3.0 wt% / 336 cm3 g-1 (row M44).
  - activated carbon (IRH33), stars (S3, I3): 20 markers extracted, archive `digitizations/fig7_activated_carbon.json`.
- Text p. 2291, right column: "values up to 336 cm3 g-1 (3.0 wt%), as shown in Figure 7" (S2, merged with the Figure 7 point).
- Text p. 2292 (3 wt% with 0.8 g cm-3 bulk density gives 24 kg m-3) and Conclusions p. 2292 ("up to 3.0 wt% and volumetric density up to 24 kg m-3 at 1 atm pressure and -196 °C"): placed on the same row M44 (volumetric capacity 24 kg m-3, basis packing_volume, packing density 0.8 g cm-3).
- Experimental p. 2292-2293 (main-5.png, main-6.png): synthesis (TiC from Alfa Aesar, Cl2 3 h), Autosorb-1 (Quantachrome) for Ar porosimetry and H2 sorption, wt% definition (W1, stated), H2 at -196 °C and -186 °C.
- Figure 3 (main-3.png): printed average pore size 0.92 nm for TiC CDC 800 °C, used as characterization of S1 (pore_diameter_method DFT; weighted NLDFT average, Eq. 2).

## Figure 7 digitization

- Axes calibrated on tick pixels found by scanning pixel rows/columns: x 0 mmHg at px 809, 700 at px 1019, check 400 at px 929 (error 0.0%); y 0 wt% at px 1402, 3.5 at px 1219, check 1.5 at px 1323 (error 0.73%). Markers at 723 and 757 mmHg lie beyond the last labelled tick (700) but on the plotted axis (minor tick at 750); the tool flags them as outside the calibrated range.
- The figure is greyscale with three black series, so each series was isolated into its own cleaned image (scripts in the work directory) and the tool run on each with --mode markers: filled squares = 5x5-px all-dark cores (6x6 cores in the overlap window near the origin, dilated 3x3 so they survive the tool's 3-px opening); open squares = enclosed white holes, dilated 5x5; stars = small components after a 3x3 opening, with filled squares removed. Plot text labels were masked.
- Sanity check (digitize_figure.py check): open-square series at 756.6 mmHg against the paper's 3.0 wt%: PASS. The paper states no value for the TiC-CDC or activated-carbon series, so those archives remain "unchecked".
- Marker counts: away from the origin the extracted counts equal the counted markers (filled 20, open 20, stars 20 for P > 50 mmHg). Near the origin (P < ~25 mmHg) the three series overlap:
  - extracted with reduced confidence (2): filled squares at 18.3 and 25.0 mmHg; open squares at 8.1 and 23.1 mmHg (the 23.1 mmHg hole is partly covered by a filled square below it, possible upward bias ~0.02 wt%).
  - not separable, not extracted: one star at about 20 mmHg, 0.38 wt% (only its right-hand tips are visible; counted in I3's point count); two 1-3 px enclosed white slits at about 0.77 and 0.66 wt% next to the y axis that may be holes of partly hidden open squares (not counted); a solid column of overlapping markers from about 0.0 to 0.35 wt% at P < ~15 mmHg containing at least two markers whose series cannot be told apart (not counted).
  - isotherm_point_count (I1 22, I2 22, I3 21) is therefore a lower bound; the notes on each row say so.

## Values seen but not extracted

- Figure 1 (p. 2288): H2 uptake at 1 atm, -196 °C vs BET SSA for TiC-, ZrC-, SiC- and B4C-CDCs (as-produced and H2-treated), activated carbons and carbon nanotubes, with a linear fit. Not an isotherm; not digitized. The individual uptake values and BET areas it shows are not given in the text or a table, and the plotted points cannot be assigned to specific samples.
- Figure 2 (p. 2289): calculated maximum possible uptake vs pore volume (solid or liquid H2 filling); computed, not measured.
- Figure 5a-d (p. 2291): uptake at 1 atm, -196 °C vs volume and NLDFT SSA of pores below and above 1 nm for about 14 CDC samples; not isotherms; values not given in text; samples not identified.
- Figure 6 (p. 2291): uptake at 0.1 atm, -196 °C vs volume of pores below 1 nm (about 12 CDC samples); not an isotherm; values not given in text; samples not identified.
- Figure 8a,b (p. 2292): uptake at 1 atm per BET and per DFT SSA vs integrated heat of adsorption (7 samples); derived quantity; not digitized.
- Figure 9 (p. 2292): isosteric heat of adsorption vs volume adsorbed for TiC-CDC 800 °C, TiC-CDC 1000 °C, activated carbon, MOF Cu3(BTC)2(H2O)3 [22] and SWCNT; not uptake values. H2 isotherms at -186 °C (87.4 K) used for Qst are not shown.
- Text p. 2288: "ca. 1.1 wt% per 1000 m2 g-1 of SSA" (slope of a fit across many materials) and "ca. 3 wt% appears to be the limit" (estimate): not rows, computed across samples / not a measurement.
- Text p. 2289: pores occupying 78% of the volume (ca. 1.6 cm3 g-1) could exceed 10 wt% (calculation): not a measurement.
- Text p. 2291: "H2 treatment increased the storage by as much as 75%" (relative change, no sample named); "CDCs can store over 20% more H2 than advanced MOFs".
- Text p. 2291, non-carbon comparison values cited from other work (not extracted, not carbon sorbents): MOF-5 ca. 1.3 wt% [14]; Cu3(BTC)2(H2O)3 ca. 1.4 wt% [22]; [Co3(bpdc)3bpy]·4DMF·H2O ca. 2 wt% [23]; MOF-505 ca. 2.48 wt% [24,25]; low-temperature metal hydrides [26].
- Text p. 2291: CNTs "<0.9 wt% [14]": a bound summarizing several CNT samples from earlier work, no identifiable sample; not a row.
- Text p. 2292: "Volumetric capacity enhancements of about 40%" (relative estimate); heats of adsorption 6.6 and 11 kJ mol-1 (abstract, p. 2288) and 8 kJ mol-1 (p. 2291) and literature heats (activated carbons and CNTs 5-6.5, MOFs 0-7 kJ mol-1, ideal 15 kJ mol-1): not uptake values.

## Characterization of samples without uptake rows

- Figure 3 average NLDFT pore sizes (Ar, -196 °C) of as-produced CDCs: TiC CDC 600 °C 0.67 nm, 1000 °C 0.97 nm, 1200 °C 1.42 nm; ZrC CDC 600 °C 0.80 nm, 800 °C 0.83 nm, 1000 °C 1.21 nm, 1200 °C 1.41 nm; B4C CDC 600 °C 0.86 nm, 800 °C 0.95 nm, 900 °C 1.03 nm, 1200 °C 1.27 nm; SiC CDC 800 °C 0.83 nm, 1000 °C 0.86 nm, 1200 °C 0.97 nm. Their H2 uptakes appear only in Figs. 1, 5, 6, 8 (not isotherms) and cannot be assigned to these samples.
- TEM (Fig. 4): TiC-CDC at 400, 800, 1000, 1200 °C; interplanar distance ca. 0.34 nm for graphite ribbons at higher synthesis temperatures (no H2 rows for these).
- Trace metal in CDC up to 0.5 at% (p. 2292), no element or sample named; not recorded in residual_metal fields (those are wt%).

## Coding decisions

- surface_area_method = none on all rows: no surface-area number is printed for any sample (BET/NLDFT areas appear only as plot coordinates). The validator rejects not_reported when no row in the paper carries an area.
- Basis: no excess/absolute/total named for the uptake ("total volume of adsorbed H2" in the abstract and "total H2 uptake" on p. 2290 mean overall amount); basis_stated false, uptake_type unspecified, basis_inferred excess (volumetric default).
- wt% convention: W1 stated (Experimental, p. 2293); applied to all three series. 336 cm3 g-1 printed without STP; stored in uptake_ml_stp_g, consistent with 3.0 wt% as W1.
- measuring_lab_id: corresponding author Gogotsi (marked *), first affiliation Drexel University; the paper does not say H2 was measured elsewhere (co-author Jagiello is at Quantachrome Instruments, the instrument maker).
- Instrument: Autosorb-1 (Quantachrome) named with model, so instrument_identified true; no free-volume determination, degassing, sample mass or H2 purity stated.
- No uncertainty, error bars or repeated isotherms: replicates_reported false.
