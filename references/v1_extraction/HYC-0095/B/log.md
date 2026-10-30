# HYC-0095 extraction log (extractor B)

Liu 2011, DOE Final Report DE-FC36-05GO15103 (Duke University). 27 page images (main-01 to main-27), no SI. 81 rows written.

## Sources extracted from

- main-13.png, Table 2 (SWNT/DWNT data "From NREL"): all uptake cells extracted (Sieverts RT and 77 K at 2 bar; TPD cell of "0.9 nm SWNT + 2 nm Pd" as three values: total, Pd part, chemisorbed part). Rows M1-M2, M57, M59-M72.
- main-22.png, Table 3: all seven PEEK samples (NREL, 77 K, 2 bar; volumetric capacities on the same rows) and the four literature comparison materials (B/C ref. 10, CMK-1 ref. 11, AX-21 ref. 12, Corncob ref. 13), coded as previously reported values with the citation in notes. PEEK-CO2-9-80 "~5 at 77 K, 20 bar" / "35 at 77 K, 20 bar" merged with the CalTech Figure 19 point closest to 20 bar (the text cites Figure 19 for it; 77 K identifies the CalTech series) (M19).
- main-02.png, Summary: "~5.1 wt% hydrogen (excess) at 40 bar and 77K" (NREL and CalTech), attributed to PEEK-CO2-9-80 (M4).
- main-07.png, item 3d: H2-NMR ">6% storage at 120K" at 10 MPa (UNC-CH), unlabelled PEEK-derived sample (M58).
- main-25.png: "SwRI showed ~30g/L at 77K and 70bar" merged with the highest-pressure Run 2 point of Figure 20 (M48).
- main-23.png, Figure 19A/19B (PEEK-CO2-9-80 isotherms): NREL series at 75.6 K, highest-pressure point only (M5-M7); CalTech series at 77 K, separable markers (M8-M23).
- main-24.png, Figure 20 (SwRI, 77 K): left panel excess wt% (all three series) with right-panel absolute volumetric capacity on the same rows (M24-M55).
- main-17.png (methods): instruments, degassing at 300 C, BET method, DFT pore volumes, labs. main-25.png: SwRI skeletal density 3.02 g/cc and the absolute volumetric-capacity definition (basis evidence).

## Figure digitization (scripts/digitize_figure.py, archives in digitizations/)

The page images are JPEG-like and low resolution (150 dpi). Before running the tool I prepared images in the work directory with the same geometry as the page: legend boxes whitened, and for each series a series-only image holding the original series-coloured pixels inside one box per marker, with 1-2 px gaps closed so that each marker is one pixel group (scripts/build_series.py; boxes in work/boxes/*.json). The tool then calibrated the axes on the page-pixel ticks and returned the marker centroids. Archives record the prepared image path and sha256.

- Figure 19A (main-23.png): x 0 px486, 150 px822, check 50 at px597; y 0 px633, 6 px367, check 3 at px500. Archives f19A_nrel_eng_excess_highest.json, f19A_nrel_gibbs_excess_highest.json, f19A_nrel_gibbs_excess_sk2.1_highest.json (one marker each).
- Figure 19B (main-23.png): x 0 px486, 50 px822, check 20 at px620; y 0 px968, 6 px702, check 3 at px835. Archive f19B_caltech_gibbs_excess_77K.json (16 markers); tool check vs stated "~5 wt% at 20 bar": pass (2.6%).
- Figure 20 left (main-24.png): x 0 px251, 90 px579, check 40 at px397; y -1.0 px1083, 7.0 px830, check 3.0 at px957. Archives f20_left_run1_ads.json (15), f20_left_run2_ads.json (12), f20_left_run2_des.json (7).
- Figure 20 right (main-24.png): x 0 px697, 80 px1004, check 40 at px850; y 0 px1059, 35 px847, check 15 at px968. Archives f20_right_run1_ads.json (13), f20_right_run2_ads.json (11; tool check vs stated "~30 g/L at 70 bar": pass), f20_right_run2_des.json (6).
- Run 2 adsorption vs desorption told apart by marker fill (grey = adsorb, white = desorb); the 70 bar point is grey (adsorption).

## Markers counted but not extracted

- Figure 19, NREL series (Eng. Excess, Gibbs Excess, Gibbs Excess sk=2.1 g/cc; 75.6 K): about 27 markers each; 75.6 K is outside the 77 K window (76.0-79.0 K), so only the highest-pressure point of each was digitized. Counts are approximate (low-pressure markers hidden behind the CalTech series). The three NREL curves look like one NREL run reduced three ways; coded as three isotherms (each plotted curve = one run).
- Figure 19B, CalTech series (77 K): about 37 markers counted (count uncertain by a few); 16 extracted. Not separable at this resolution and left out: the vertical stack of about 6-8 markers at p ~ 0 bar (0-1.2 wt%), the marker(s) near 1.6 wt% and the pair near 1.1 wt%, the diagonal chain of about 10 touching markers between 2.1 and 3.6 wt% (p ~ 0.5-3.5 bar), and the marker near 5.5 bar / 3.95 wt% overlapping an NREL marker. The extracted markers near 1.9 wt% and 22.3 bar appear solid-filled and may each hide a second superimposed marker.
- Figure 20, Run 1 (17 markers): marker near 0.5 bar (under the Run 2 marker at 0.55 bar) hidden in both panels; marker near 6.6 bar hidden in the left panel and half hidden in the right panel - not extracted. Two left-panel markers at p ~ 0 bar were digitized at -0.086 bar (0.016 wt%; right panel 0.165 g/L) and -0.039 bar (2.03 wt%); a pressure of zero or below cannot be stored, so no rows (points remain in f20_left_run1_ads.json).
- Figure 20 right panel: Run 1 markers near 0 bar / 3.0 g/L and near 2.3 bar are mostly hidden under Run 2 markers (no volumetric value on row M26; the p ~ 0 point has no row); Run 2 adsorption and desorption markers at ~46.9 bar overlap almost completely (no volumetric value on M44 and M52).
- Figure 20 "Model Fit" and "95% CI" lines: fitted curves, not extracted.

## Values seen but not extracted

- Table 2 "Modified Chahine Criterion (wt% per 500 m2/gm)" rows (0.56, 0.64, 1.08, 0.48; 0.67, 0.67, 0.75, 1.35): ratios computed from uptake and area, not uptake values.
- Table 2 "BET SA after 800 C CO2" for 1-2 nm DWNT (75 m2/g): characterization of a state with no H2 uptake value.
- Table 1 (main-04.png, main-12.png): CNT growth products, no H2 values.
- main-02.png: ">5 wt% at 77K" and ">3100 m2/g" (restatement of PEEK-CO2-9-80 results), "excess volumetric capacities greater than 35 g/L" (restatement of Table 3 35 g/L); same in main-07.png item 3f, main-24.png ("up to ~5 wt% and 35 g/L"), main-25.png ("~35g/L capacity").
- main-07.png item 3c: ">3 wt.% excess at 77K and 2 bar" (restatement of Table 3 3.7 wt%) and ">5 wt% at 77K and 40 bar" (restatement of the main-02.png ~5.1 wt% at 40 bar, M4). Item 3e: binding energy 8.1 kJ/mol (not uptake).
- main-18.png: "~1 wt% for every 500 m2/g" at 77 K for graphitic slit-pore materials (general rule cited from ref. 9, not a sample value).
- main-21.png text and Figure 18 caption: "3.7 wt% at 77K and 2 bar" for PEEK-CO2-9-80 (same value as Table 3, in M3).
- main-21.png, Figure 18 (excess uptake at 77 K, 2 bar vs BET area; not an isotherm, not digitized): its CO2 series has 6 points and its steam series 7 points; the tabulated samples account for 3 CO2 and 4 steam points (PEEK-CO2-9-5 is not plotted). Points not given in tables or text: 3 CO2 points at BET areas between PEEK-CO2-9-26 and PEEK-CO2-9-80 (one presumably PEEK-CO2-9-59, "~2000 m2/g" in the text) and 4 steam points (one presumably PEEK-ST-9-35, "~1000 m2/g" in the text); their uptakes are only plotted. Error bars in Figure 18 used for replicates_reported of the plotted Table 3 samples.
- main-22.png: compressed PEEK-CO2-9-80 (15 metric tons, density ~1 g/ml) "corresponds to a H2 volumetric uptake of ~50 g/L": a projection combining the uncompressed sample's uptake with the compressed sample's density, not a measurement; not a row. "Initial experiments demonstrated that the compression do not have significant effect on the gravimetric capacity" (no value).
- main-23.png: "large excess gravimetric uptakes (~5 wt.%)" and Figure 19 caption "~5 wt.%" (restatements).
- main-25.png: "The gravimetric uptake is >5%" (summary over NREL, NIST, UNC and SwRI; NIST and UNC values not given).
- Figure 16 (main-18.png, BET vs burn-off for CO2 and steam series, with error bars): characterization only, not digitized.
- Figure 17 (main-20.png, DFT differential pore volumes): characterization only; text values used: PEEK-CO2-9-80 largest pore volume at 1.35 nm (M3-M55 average_pore_diameter_nm, method DFT).
- Characterization of samples without uptake values: PEEK-CO2-9-59 (BET ~2000 m2/g), PEEK-ST-9-35 (BET ~1000 m2/g); MPC from P123 (pore ~1.3 nm / ~2 nm) and P103 (pore ~1.2 nm / 1.18 nm) templates; P84/resol MPC (pores 0.6-0.8 nm, BET <250 m2/g, "pores inaccessible to H2", no uptake value); zeolite-templated MPC (no data).
- Figure 4 caption (main-06.png): PEEK-derived MPC after CO2 activation with ~80% burn-off, "surface area of 3013m2/g", against 3103 m2/g for PEEK-CO2-9-80 in Table 3 and text; 3103 used.
- Refs. 14 and 15 (the authors' JACS 2010 and JPCC 2010 papers) are cited after the PEEK discussion (main-24.png) but the report does not say these values were published there; no "previously reported" note added.

## Coding decisions

- Multi-laboratory paper: PEEK-CO2-9-80 was measured by NREL, CalTech and SwRI (and UNC by NMR); every row's label carries "/ <lab as printed>" and measuring_lab_id "<lab> (HYC-0095)". Table 2 and Table 3 PEEK 2-bar data are NREL's (Table 2 "From NREL"; main-17.png: 2-bar uptakes on NREL's specially built Sieverts device). Literature rows carry the citation ("ref. N") as lab label.
- Table 3 PEEK-CO2-9-80 3.7 wt% at 2 bar not merged with a Figure 19 point (different NREL instrument; NREL Figure 19 data at 75.6 K; no separable CalTech marker near 2 bar).
- SwRI rows: basis_stated = true (excess and absolute volumetric capacity reported side by side, absolute defined in main-25.png). Fig 19 rows: "Gibbs Excess"/"Eng. Excess" named but not defined, basis_stated = false, basis_inferred = excess.
- replicates_reported = true for all PEEK-CO2-9-80 rows (independent isotherms of this sample from three labs; CalTech ±0.1 % error) and for Table 3 samples plotted with error bars in Figure 18.
- Table 2 "Small d Commercial SWNT" uptake row "after 800 C" (1.61 wt%) given the BET of the row "after 800 C CO2" (1074 m2/g) with area_same_sample = unclear.
