# HYC-0099 extraction log (extractor B)

Masika et al. 2013, ACS Appl. Mater. Interfaces, doi 10.1021/am401622w. Input: page images only (main-1..9, si1-01..12). Rows written: 323 (32 table_direct, 291 figure_digitized). Samples: S1 ZTC8, S2 ZTC8Pd-0.2, S3 ZTC8Pd-0.4, S4 ZTC8Pd-0.8, S5 ZTC8Pd-2.0, S6-S12 Table S2 ZTCs, S13-S22 Table S3 Pt-ZTCs.

## Sources extracted

- Table 1 (main p. 5642, main-4.png): for each of the 5 samples, the H2 uptake at 77 K and 20 bar (total basis), 5 rows, each merged with the plotted 20-bar point of its total isotherm (digitized point in notes); and the Langmuir maximum in parentheses, 5 rows (value_kind fitted_extrapolated, no pressure, no isotherm_id). Surface area (BET), micropore surface area (t-plot), total pore volume (P/Po = 0.99), micropore volume (t-plot) put on every row of the sample. The NLDFT pore-size maxima 0.6/1.2/2.4 nm and the uptake density in umol H2 m-2 are given in notes only; there is no average-diameter or per-BET-area field for them.
- Experimental sections 2.1-2.3 (main p. 5640-5641): synthesis, XRF Pd contents (metal_loading_wt_pct), BET range 0.06−0.22, N2 at −196 °C (ASAP 2020), degassing at 200 °C and 10^-10 bar for 4−6 h (degas_end_pressure_pa = 1e-05; the duration is printed as a range, so it is not stored), H2 purity 99.9999%, IGA gravimetric analyzer (no manufacturer or model, so instrument_identified = false), buoyancy correction stated (calibration_described = true), 0−20 bar at −196 °C.
- Text p. 5644: "error ... (at 77 K and 20 bar) given in Table 1 ... typically ±0.05 wt %". This gives uncertainty_wt_pct = 0.05 on the Table 1 rows and replicates_reported = true on all rows of the total 77 K isotherms. The excess isotherms and the 87 K values get false, because the statement refers only to Table 1.
- Supporting Table S1 (si1-02.png): excess H2 uptake at 77 K and 20 bar, 5 rows, each merged with the 20-bar marker of Figure S6 (digitized point in notes). The excess uptake densities are in notes.
- Supporting Table S2 (si1-03.png): 7 ZTCs, "The data is taken from reference 40b", 7 rows with `previously reported: reference 40b`. Surface area method and probe gas are not stated, so they are coded unspecified, area_same_sample = other_paper, measurement method unknown and basis unknown. The main text cites ref 55 for this comparison.
- Supporting Table S3 (si1-04.png): 10 Pt-ZTCs (IE, IW), "taken from reference 40a", 10 rows with `previously reported: reference 40a`, coded as composites with metal Pt (no loading given). The main text cites ref 54. Pore sizes "0.6/12" (IE 800) and "12.5/2.0" (IW 900) are copied as printed into notes.
- Figure 5 (main-6.png): total 77 K isotherms. Digitized for ZTC8Pd-0.2 (20 adsorption and 17 desorption markers, plus the 20-bar point merged with Table 1). For the other four samples, Figure 5 was used together with Figure S8 (a); see below.
- Figure S8 (si1-12.png): curves (a) 77 K are the same runs as Figure 5. At equal pressures, the desorption markers of ZTC8, ZTC8Pd-0.4, ZTC8Pd-0.8 and ZTC8Pd-2.0 agree with Figure 5 within 0.01 wt%. Each point was therefore extracted once, from Figure 5 where the tool resolves it there and otherwise from Figure S8 (a). Curves (b) 87 K: only the highest-pressure (20-bar) marker of each, 4 rows.
- Figure S6 (si1-10.png): excess 77 K isotherms of all 5 samples, digitized (adsorption and desorption markers).

## Digitization method and calibration

- Axes were calibrated on the lowest and highest labelled ticks, with a third tick as a check. Tick pixel positions were found from pixel rows and columns:
  - Fig 5: x 0→219.28 px, 20→569.19 px, check 10→394.27 px; y 0→499.42 px, 5→176.75 px, check 3→305.66 px.
  - Fig S6: x 0→525.5, 20→934.5, check 10→730.0; y 0→821.5, 5→206.5, check 3→452.5.
  - Fig S8, ZTC8 panel: x 0→397.0, 20→636.49, check 10→517.0; y 0→509.5, 5→157.0, check 3→298.0.
  - Fig S8, ZTC8Pd-0.4 panel: x 739/983/861; y 512.0/186.0/316.5.
  - Fig S8, ZTC8Pd-0.8 panel: x 392/623/507; y 992/650.49/787.
  - Fig S8, ZTC8Pd-2.0 panel: x 736/980/858; y 983.5/625/768.5.
  - Every check tick agreed within 0.3 px.
- Filled markers (adsorption) were found with `extract --mode markers` on the series colour, using a 3-px opening for Fig S6 and 2 px for Fig 5 and Fig S8. Open markers (desorption) were found with `extract --mode markers` on white (`#ffffff`), which locates each open marker's white interior. The tolerance was 30 for Fig S6, 60 for Fig 5 (ZTC8Pd-0.4, -0.8, -2.0) and Fig S8, and 100 for Fig 5 (ZTC8, ZTC8Pd-0.2). Each interior was assigned to a series by the colour of the ring around it.
- Rejected detections: legend and text, slivers of white between parallel adsorption and desorption lines, outline remnants of open markers, and blobs containing several merged markers. The accepted markers of each series and branch were copied unchanged into per-series subset archives, which the rows cite, such as `FigS6_ZTC8Pd-0.2_ads.json` and `Fig5_ZTC8Pd-0.8_des.json`. Each subset archive names its raw tool archive (`*_filled.json`, `*_open*.json`, also saved) and the indices used.
- Branch was assigned from marker fill (Figure S8 caption: filled = adsorption, empty = desorption). The same convention was applied to Figure 5 and Figure S6, whose captions do not state it.
- Step-6 check (`digitize_figure.py check`) passed for every subset archive that reaches 19-20 bar. Each was checked against the Table 1 or Table S1 value at 20 bar with 5% tolerance, at the archive's highest digitized pressure (19.0-19.97 bar). The 20-bar markers are clipped by the frame or partly hidden, so no archive covers exactly 20 bar.
  - Not checkable: single-point archives (`Fig5_ZTC8_ads`, `FigS6_ZTC8_ads`, `FigS8b_*_highest`); archives without a stated value in range (`FigS8a_ZTC8_ads` ≤3.3 bar, `FigS8a_ZTC8Pd-0.4_ads` ≤7 bar, `FigS8a_ZTC8Pd-0.8_des` ≤1 bar, `FigS8a_ZTC8Pd-0.4_des` ≤18 bar); and the 87 K archives, for which no value is printed.

## Markers counted vs extracted (step 6). These markers could not be separated.

In the counts below, the desorption numbers include the 20-bar marker, which is merged with the Table 1 or Table S1 row rather than given its own row.

- Every isotherm: below about 1.5 bar the markers of all series form one continuous band, so they could not be separated or fully counted. isotherm_point_count is therefore the number of markers identified, a lower bound (stated in notes).
- Every isotherm: where adsorption and desorption share a pressure (most integer pressures from 4 to 19 bar), the empty desorption marker is drawn over the filled adsorption marker. Adsorption markers were extracted only where part of them is visible. Partly visible ones have extraction_confidence 2.
- The (0, 0) origin marker of ZTC8 (Fig 5, S6, S8) is not extracted and not counted. It is a point at 0 bar and 0 wt%, not an uptake measurement.
- I1 ZTC8 total, 29 markers identified:
  - Extracted: 5 adsorption (1.5, 1.9, 2.5, 3.25 bar from S8a; 19.5 bar from Fig 5) and 24 desorption (0.25-9 bar and 18, 20 bar from S8a; 10-17 and 19 bar from Fig 5).
  - Not separated: adsorption markers at 4-19 bar, hidden under desorption markers; the Fig 5 open marker near 0 bar, about 0.2 wt%.
- I4 ZTC8Pd-0.2 total, 37 identified:
  - Extracted: 20 adsorption and 17 desorption.
  - Not separated: desorption at 2, 3, 4 bar (open-triangle interiors not resolved); adsorption at 17, 18, 19 bar (covered); the lowest adsorption marker near 0.07 bar, which is only partly visible.
- I6 ZTC8Pd-0.4 total, 34 identified:
  - Extracted: 10 adsorption (Fig 5: 1.1, 1.5, 2.5, 3.25, 4, 5, 19.5 bar; S8a: 1.3, 6, 7 bar) and 24 desorption (S8a 0.2-18 bar, Fig 5 19 and 20 bar).
  - Not separated: adsorption 8-19 bar.
- I9 ZTC8Pd-0.8 total, 39 identified:
  - Extracted: 15 adsorption (Fig 5) and 24 desorption (Fig 5 2-20 bar, S8a 0.19-0.95 bar).
  - Not separated: adsorption 4-11 bar (hidden exactly under the desorption markers).
- I12 ZTC8Pd-2.0 total, 33 identified:
  - Extracted: 7 adsorption and 26 desorption, all from Fig 5. The two lowest desorption markers (about 0.04 bar) are partly hidden by the y axis.
  - Not separated: adsorption 4-19 bar.
- I2 ZTC8 excess, 13 identified:
  - Extracted: 1 adsorption (19.5 bar) and 12 desorption (9-20 bar).
  - Not separated: desorption 2-8 bar and adsorption 1.5-19 bar, covered by the ZTC8Pd-0.8 and ZTC8Pd-0.4 markers and by the ZTC8 desorption markers.
- I5 ZTC8Pd-0.2 excess, 38 identified:
  - Extracted: 19 adsorption and 19 desorption.
  - Not separated: desorption at 3 bar (interior covered by a ZTC8Pd-0.4 marker); adsorption at 18 and 19 bar; adsorption markers at about 0.14 and 0.98 bar, which are only partly visible.
- I7 ZTC8Pd-0.4 excess, 10 identified:
  - Extracted: 8 adsorption and 2 desorption (19, 20 bar).
  - Not separated: adsorption 8-19 bar and desorption 2-18 bar, covered by ZTC8Pd-0.8 markers.
- I10 ZTC8Pd-0.8 excess, 34 identified:
  - Extracted: 14 adsorption and 20 desorption.
  - Not separated: adsorption 4-9 and 12 bar (hidden or merged with the line).
- I13 ZTC8Pd-2.0 excess, 30 identified:
  - Extracted: 4 adsorption and 26 desorption.
  - Not separated: adsorption 4-19 bar (hidden), and the low-pressure adsorption blobs (5 merged groups below 1.4 bar).
- 87 K curves (b), Figure S8: only the 20-bar marker extracted (rule for non-77 K isotherms). The point counts (I3 30, I8 32, I11 29, I14 31) are the desorption markers plus the adsorption markers at adsorption-only pressures identified on curve (b), a lower bound.

## Values seen but not extracted

- Abstract and text restate the Table 1 values (4.9 wt%; 4.7−5.3 wt%; 5.3 wt% for ZTC8Pd-0.2; densities 12.0 and 14.3−18.3 umol m-2; Langmuir maxima 5.8 and 6.1−7.3 wt%). They are the same measurements as the Table 1 rows, so they are not separate rows.
- The abstract graphic and Figure 6 are bar charts of uptake density against Pd loading, not isotherms, and were not digitized; their values are in Table 1. Qualitative observation: the 0.2 wt% bar looks taller than the 2 wt% bar, whereas Table 1 gives 14.3 (ZTC8Pd-0.2) and 14.9 (ZTC8Pd-2.0). This is a possible inconsistency, not quantified.
- Figure 7 (Qst against uptake) is not an isotherm. The Qst values (5.3 kJ/mol for ZTC8; about 6.7 kJ/mol initial for the Pd-ZTCs) are not uptake values.
- Figure S7 ("Cycles of hydrogen sorption profiles ... for a variety zeolite templated carbons") was not digitized, for three reasons:
  - The three samples are not identified, so they cannot be linked to any sample of this paper. Panel 1 ends near 7 wt%, above every sample here.
  - The figure states no temperature.
  - In every panel the red (cycle 1) and black (cycle 2) adsorption and desorption markers coincide and cannot be separated.
  - It shows three ZTCs, each with two cycles of adsorption and desorption from 0 to 20 bar, ending near 7, 4.5 and 3.2 wt% (axis ranges; not digitized). The main text cites it only as evidence of reproducibility.
- Figure S8 curves (a) for ZTC8, ZTC8Pd-0.4, ZTC8Pd-0.8 and ZTC8Pd-2.0 duplicate Figure 5 (same runs, see above). Points were not extracted twice.
- Zeolite Y CBV100 (template, not a carbon sorbent; Figures S1 and S2): N2 sorption and PSD only, no H2 uptake.
- A Pd-ZTC with 4 wt% Pd (Figure S5): TEM only (Pd particles up to 15 nm, agglomerated fine crystallites by SAED), no H2 uptake, so no row.
- Characterization without H2 values:
  - Figure 1 and S1 XRD: Pd fcc peaks at 2θ = 39°, 47°, 68° (d = 0.224, 0.193, 0.137 nm); ZTC8 weak peak at 2θ = 6° and broad (002) feature at 26°.
  - Figure 2 and S2 N2 isotherms and PSDs.
  - Figure S3 TGA: residual mass at 800 °C of 12% (ZTC8Pd-2.0), 10% (ZTC8Pd-0.8), 7.0% (ZTC8Pd-0.4), 4.5% (ZTC8Pd-0.2), about 0 for ZTC8.
  - TEM: Figures 3, 4 and S4.
  - XRF Pd 0.19/0.38/0.78/1.92 wt% (stored as metal_loading_wt_pct).
  - ZTC8 micropore fractions 75% (area) and 61% (volume); Pd-ZTCs about 73% and 57%.
- Literature statements that are not values from this paper's measurements: Chahine rule (1 wt% per 500 m2/g); a 43% increase for Pd-doped MOFs with 3 wt% Pd (Cheon, ref 76; MOF, not carbon); Ru-doped templated carbon order 6% > 8% > 3% Ru (ref 71, qualitative); activated carbon Qst 4−6.5 kJ/mol and ZTC Qst 8−10 kJ/mol (literature ranges).
- Text range summaries of Tables S2 and S3 (densities 9−13 and 7.6−11.6 umol m-2): computed from the table rows, not separate values.

## Discrepancies noted for reconciliation

- ZTC8 total: Table 1 gives 4.9 wt% at 20 bar. The 20-bar marker digitizes at 4.823 wt% (Figure S8 a), and the Fig 5 ZTC8 marker at 19 bar is at 4.748. The plotted curve ends about 1.6% below the printed value.
- Excess, Table S1 vs Figure S6: ZTC8Pd-0.4 is printed as 4.4 and digitizes at 4.289 (−2.5%); ZTC8Pd-0.8 is printed as 4.3 and digitizes at 4.358 (+1.3%). In Figure S6 the blue (ZTC8Pd-0.4) curve ends below the green (ZTC8Pd-0.8) curve, the reverse of the table. Possible label swap. The table's densities agree with the table's wt% values.
- 87 K basis: the paper names no basis for curves (b). Coded uptake_type unspecified, basis_inferred excess by the §3 instrumental default (gravimetric, buoyancy correction stated). However, curves (a) in the same figure equal the total isotherms, so (b) may also be total.
- The SI cites "reference 40a/40b", which does not match the main reference list (ref 40 is Prins, Chem. Rev. 2012). The main text cites refs 54 and 55 for the same comparisons.
