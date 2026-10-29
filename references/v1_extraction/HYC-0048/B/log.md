# HYC-0048 extraction log (agent B)

Paper: Kahilu et al. 2023, Waste Disposal & Sustainable Energy 5:125-149. Input: 25 page images (main-01 to main-25, journal pp. 125-149); no supplementary file.

## Sources extracted from

- p. 126 (Materials): H2 grade "N5.0" from AFROX; used for h2_purity_pct (99.999) on every row.
- p. 128 (Characterization; Hydrogen adsorption): N2 at 77 K, autosorb iQ, BET and NLDFT/BJH; H2 by Micromeritics HPVA (high-pressure volumetric, 77 K); degassing 373 K overnight, then 373 K under vacuum 24 h in a 10 cm3 cell with about 1.2 g; adsorption 1 to 35 bar, desorption "from 28 bar to 1.6 bar"; free volume from cold and warm volume measurement after the adsorption-desorption tests. Coded on every row.
- p. 134 Table 3, p. 135 Table 4 and text, p. 136 Table 5, p. 137 Table 6, p. 143 Table 8, p. 144 Table 10: characterization of AC-HCT, AC-HCS and AC-HCB. Table 6 values are stored (BET area, BET-adsorption total pore volume, BJH 4V/A pore diameter, He skeletal density, composition in notes); every conflicting value in the other tables and the text is listed in the row notes.
- p. 141 Fig. 8a (77 K, cm3/g vs MPa) and Fig. 9a (77 K, wt% vs P/P0): every separable marker of both branches of the three isotherms digitized. The two figures plot the same points (see "Figure pairing"), so each point is one row carrying the Fig. 8a pressure and cm3/g and the Fig. 9a wt%.
- p. 141 Fig. 8b and Fig. 9b (273 K): highest-pressure adsorption point of each isotherm only, merged in the same way (3 rows).
- p. 142 Table 7, rows "AC-HCT 6.12", "AC-HCS 6.80", "AC-HCB 6.57" (3.5 MPa, 77 K, "Maximum H2 uptake"): each is the same measurement as the highest-pressure 77 K adsorption marker (pressure 34.80, 34.87, 35.00 bar digitized, within 2% of 35 bar). Recorded as table_direct rows that replace those digitized points; the digitized point is in the notes, and the Fig. 8a cm3/g of the point is kept in uptake_ml_stp_g.
- p. 141 text, "the highest hydrogen uptakes (% in weight) at relatively lower pressure were observed on AC-HCB (~4%) compared to AC-HCS (~2.5%) and AC-HCT (~2.5% in weight)": 3 rows, uptake_bound approximate, pressure_unstated, no isotherm_id; 77 K assigned from context (see row notes).
- Abstract (p. 125), p. 139, pp. 141-142 and Conclusions (p. 145) repeat 6.12, 6.8 and 6.57 wt% at 35 bar. These are the Table 7 values, so they were not given separate rows; the locations are named in source_location.

## Digitization

- Calibration (page main-17.png pixels; ticks found from pixel rows/columns):
  - Fig. 8a: x 0.0 MPa at px 229, 3.5 at 584, check 2.0 at 432; y 50 at 509.5, 200 at 213, check 150 at 312.
  - Fig. 9a: x 0.0 at 219, 1.0 at 570.5, check 0.6 at 430; y 1 at 1080.5, 7 at 764, check 4 at 922.5.
  - Fig. 8b: x 0.0 at 678, 3.5 at 1051.5, check 2.0 at 891; y 5 at 420, 20 at 165, check 10 at 335.
  - Fig. 9b: x 0.0 at 676.5, 1.0 at 1044, check 0.6 at 897; y 0.1 at 1080.5, 0.6 at 807.5, check 0.4 at 917.
  All third-tick checks passed (error at most 0.2%).
- Preprocessing (scripts and images in the work directory): legends and the "77K"/"273K" labels were whited out in working copies of page 17. Filled (adsorption) markers were extracted from those copies with the tool's default 3-px opening. Open (desorption) markers were extracted from derived images that hold only the white interiors of the open markers, painted in the series colour (scripts/derive.py); the centroid of the interior is the marker centre. Where another series' marker closes part of an interior (AC-HCS des at ~3.18 MPa in Figs. 8a and 9a, AC-HCT des at P/P0 ~0.29 in Fig. 9a), the other colour was used as a barrier. For the filled black squares of Figs. 8a and 9a, the open squares were whited out first so their outlines were not picked up. For Figs. 8b and 9b, the highest-pressure filled marker was taken from extractions on the masked page. Red series used colour tolerance 120: at 60, one partly hidden red marker split into two fragments. All other series used 60.
- Marker counts and extraction (Fig. 8a and Fig. 9a show identical marker layouts):
  - AC-HCB 77 K: 11 ads + 6 des = 17; all 17 extracted in both figures.
  - AC-HCS 77 K: 9 ads + 6 des = 15; 14 extracted. Not separable: des marker at ~2.78 MPa (P/P0 ~0.79). In both figures it is hidden behind the AC-HCB des triangle, with only its bottom edge visible.
  - AC-HCT 77 K: 11 ads + 6 des = 17; 13 extracted. Not separable: the ads markers at ~0.07 and ~0.21 MPa (P/P0 ~0.02, ~0.06), hidden behind the AC-HCS filled squares, and the des markers at ~0.17 and ~0.6 MPa (P/P0 ~0.05, ~0.17), hidden behind the AC-HCS open squares with only arcs visible.
  - The lines of all series run down to the origin (below the y = 50 frame edge in Fig. 8a, to (0,0) in Fig. 9a). No marker is visible there, so the origin was not counted or extracted.
  - 273 K (Fig. 8b), visible markers: AC-HCB 11 + 6 = 17; AC-HCS 10 filled grey + 6 open = 16; AC-HCT 9 filled + 6 open = 15. Further filled AC-HCT markers may be hidden behind the open circles near 0.6 and 1.0 MPa. Only the highest-pressure point of each isotherm was taken.
- Partly hidden markers extracted with extraction_confidence 2 (centroid of the visible part, possible bias up to ~3 px, which is below 1% of the axis span): AC-HCT ads 0.45 and 1.05 MPa; AC-HCT des 1.03 MPa (Fig. 9a interior); AC-HCS ads 2.97 MPa (9 px visible in Fig. 8a, 18 px in Fig. 9a); AC-HCS ads 3.49 MPa (Table 7 row); AC-HCS des 3.18 MPa; AC-HCB ads 1.06 MPa; AC-HCS 273 K highest point (grey square mostly behind the AC-HCT circle).
- Figure pairing: for all 43 extracted 77 K points, the Fig. 9a abscissa x 3.5 MPa matches the Fig. 8a pressure within 0.009 MPa, and cm3/g : wt% = 33.50-33.73. This is why Figs. 8a and 9a are treated as one measurement per point.
- Tool check (step 6): the Fig. 9a ads archives PASS against Table 7 at P/P0 0.99 (5% tolerance). No other archive has a printed value to check against; the pairing above is the consistency check.
- The tool flags points above the highest labelled tick (200 cm3/g in Fig. 8a; 0.6 wt% in Fig. 9b) as beyond the calibrated range. They lie inside the plot frame on a linear axis.
- Archives: out/digitizations/HYC-0048_fig8a_*, _fig9a_* (12 files, 77 K, one per series and branch) and _fig8b_*, _fig9b_* (6 files, 273 K adsorption series).

## Values seen but not extracted

- Table 7 (p. 142), literature values for other materials (not this paper's measurements): Norit UOK A 2.40 wt% (0.1 MPa, 77 K) [93]; Mesoporous 1.75 [94]; Takeda 3A (CMS-T3A) coconut shell 1.60 [95]; Mesoporous from silica templates 3 [96]; Derived from commercially available coconut shell 1.70 (0.1 MPa, 77 K) [92]; Pd doped 5.50 (8 MPa, 298 K) [97]; KOH treated 6.60 (4 MPa, 77 K) [46]; From bituminous coal 5.70 (3 MPa, 77 K) [98]; From Chinese coal 4.50 (77.4 K) [99]; Ni doped 1.80 (0.1 MPa, 77 K) [100]; Pt doped 2.30 (10 MPa, 298 K) [101]; Shanghai Dahe (KOH:AC 3:1) K3 5.63 (2 MPa, 77 K) [102]; Shanghai Dahe (KOH:AC 5:1) K5 7.08; AX-21 (10X zeolite template) 4.60 (1 MPa) [103]; KUA-6 5.60 (4 MPa) [104]; Maxsorb 3000 5.20; CB 850 h (TC) from metal organic framework 6.90 (2 MPa) [85]; TC (alkali metal framework) 5.30 [105]; Maxsorb from Kansai coke 2.31 (4 MPa, 77 K) [85]; MSC30 5.78; MSP20X 4.74; SA1500 4.04; SA20 3.24; TH90I 2.90; Filtrasorb 400 2.30 (3 MPa, 77 K).
- p. 135 text: "As reported by Jordá-Beneyto et al. [75] 6.5% (in weight) of hydrogen could be stored at 77 K and 4 MPa on AC". This is another work's value.
- p. 128: "The density of hydrogen adsorbed was measured by the maximum amount adsorbed ... compared to the total pore volume". No density value is printed anywhere.
- p. 140: the desorption isotherms overlap the adsorption isotherms with no hysteresis over 0.1-3.5 MPa. p. 142: only a "negligible quantity" is adsorbed at ambient temperature. Neither passage gives a number.
- Samples with characterization but no H2 uptake (no rows): raw CT, CS, SS and CB, with proximate and ultimate analyses in Tables 1, 2 and 6, and CT 6.07 m2/g, 0.03 cm3/g, 2.16 nm and CS 6.37 m2/g, 0.05 cm3/g, 2.65 nm (Table 4); hydrochars HCT, HCS and HCB from HTC/Co-HTC at 150-270 °C and 10-27 bar (Tables 1, 2, 6), with HCT 11.88 m2/g, 0.07 cm3/g, 2.62 nm and HCS 14.35 m2/g, 0.09 cm3/g, 3.34 nm (Table 4); AC-CT 1354.28 m2/g, 1.05 cm3/g, 3.02 nm and AC-CS 1845.09 m2/g, 1.21 cm3/g, 2.64 nm (direct KOH activation, 850 °C, 135 min; Tables 4, 5, text p. 134); ACs at KOH:HC 1:1, AC-HCT 780.60, AC-HCS 1170.15 and AC-HCB 1005.24 m2/g (text p. 134); the RSM/CCD activation runs (Figs. 3-4, Eqs. 4-6, no tabulated values); commercial charcoal AC (Sigma-Aldrich, granular 4-12 mesh, CAS 7440-44-0), 900 m2/g, 0.76 (Table 5) or 0.71 (Table 8) cm3/g, 3.14 nm, which is probably supplier data.
- Table 5 rows other than "This work", and Table 10 rows other than "This work", are literature textural, yield and cost data for other materials; not extracted.
- Figs. 1-7 and 10 (flow sheet, XRD/FTIR, RSM surfaces, N2 isotherms and BET plots, PSDs, SEM/EDS, mass balance) are not H2 isotherms and give no H2 values.

## Data issues found in the paper (for the reconciler)

- Unit consistency: Fig. 9 wt% is 1/33.6 of the Fig. 8 cm3/g value at 77 K, about 3.3 times the W1 that 0.0089938 x cm3(STP)/g gives (for example 221.4 cm3/g gives 1.99 wt% W1, but 6.58 wt% is plotted and 6.57 printed). wt_pct_convention is unknown on every row, and the cm3/g value is stored so that code can apply the section 3 unit-consistency rule. The Fig. 8 axis is "Volume H2 (cm3/g)" with no STP reference.
- Fig. 9b (273 K) reproduces the Fig. 9a values divided by 10 at the same abscissae (for example AC-HCB 3.96 to 0.396, 6.58 to 0.658). Its cm3/g : wt% ratio differs between samples (about 28-31), and the order of AC-HCS and AC-HCT at 3.5 MPa differs between Fig. 8b (AC-HCT higher) and Fig. 9b (AC-HCS higher). The 273 K rows carry this caution.
- Relative-pressure axis of Fig. 9: Eq. 17 defines P0 = Pc(T/Tc)^2, but the plotted P/P0 equals P/3.5 MPa. P0 is not printed numerically, so pressures were taken from Fig. 8.
- The Methods give desorption pressures "from 28 bar to 1.6 bar", but the plotted desorption points run from ~3.2 to ~0.17 MPa.
- Textural values conflict between tables and text (AC-HCT pore volume 1.89/1.88/1.77; AC-HCS BET 2301.38/2299.25; AC-HCB BET 2243.57/2242.63/2242.69 and pore volume 1.31/1.38; average pore diameter in nm in Tables 4 and 8 vs BJH 4V/A in Å in Table 6). Table 6 values were used, as listed in the notes.
- Co-HTC residence time is 360 min in the Methods (p. 126) and 95 min in Table 10. The Co-HTC pressure for HCB is 18.5 bar in Table 10, while Table 2 shows the highest fixed carbon at 22.75 bar.

## Coding decisions

- sample_id: only the three samples with H2 rows are numbered, in order of first appearance (Abstract: AC-HCT S1, AC-HCS S2, AC-HCB S3). Labels are taken from Table 7.
- measuring_lab_id: Jean Mulopo is the corresponding author (envelope on p. 125). His affiliation 2 is the University of Witwatersrand. The paper names no other H2 laboratory.
- material_class activated_carbon for all three samples, although the ash is 23-41 wt% (mineral matter from coal and sludge, not a deliberately added phase). synthesis_method is carbonization (hydrothermal carbonization made the raw hydrochar); KOH activation is in activation_method and the HCl/water wash in purification_method.
- instrument_identified true (Micromeritics HPVA); calibration_described true (cold/warm free volume after the run); replicates_reported false (no error bars, no repeated isotherm); bet_range_stated false (no P/P0 range stated in the text).
