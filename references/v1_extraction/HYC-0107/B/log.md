# HYC-0107 extraction log (extractor B)

Paper: Bastos-Neto et al. 2012, Energy & Environmental Science, "Assessment of hydrogen storage by physisorption in porous materials". Pages: main-01 to main-10 (journal pp. 8294-8303); no SI. 53 rows written. One laboratory (Gläser group, Universität Leipzig). Carbon sorbents: six commercial activated carbons, S1 AT 470335, S2 AT 470344, S3 AT 100004, S4 AC1, S5 AC2, S6 AC3.

## Sources extracted from

- Introduction, main-02 (p. 8295) right column: definitions of excess, absolute and total amounts. Used for basis_stated = true and basis_evidence.
- Section 2.1, main-02/main-03 (pp. 8295-8296): suppliers. Adsor-Tech GmbH: AT 470335, AT 470344, AT 100004. CarboTech AC GmbH: AC1, AC2. Norit: AC3. H2 purity 99.9992 vol% (Air Products).
- Section 2.2, main-03 (p. 8296): Rubotherm magnetic suspension balance (model not named); "isotherms were reversible and repeatable within <1%"; sample amount 0.5 to 5 g; activated carbons pre-treated at 423 K under vacuum (p < 3 Pa) for at least 10 h; packing density from a graduated cylinder, mean of at least 10 measurements.
- Table 1, main-03 (p. 8296): A_BET (N2, 77 K), V_P (Gurvich rule), V_micro (DR plot) and d_P (BJH) for the six activated carbons. These go on every row of S1-S6. No BET range or consistency criteria are stated.
- Table 2, main-06 (p. 8299): packing (tap) density and helium specific volume for the six carbons. Stored as packing_density_g_cm3, and skeletal_density_g_cm3 = 1 / V̂s (printed V̂s in notes).
- Fig. 2a, main-04 (p. 8297): 77 K excess isotherms. Digitized: AT 470335 (9 markers), AT 100004 (7), AC3 (7), AT 470344 (7), AC1 (13) and AC2 (6), 49 points in all. Four of these points are merged with text maxima (see below), which leaves 45 figure_digitized rows.
- Text, main-04 left column (p. 8297): "AT 470335, which has an apparent maximum of ca. 3.6 wt% at 2–5 MPa". Row M10 (approximate). Its pressure is digitized from the Fig. 2a maximum point, the only plotted point between 2 and 5 MPa.
- Text, main-04 right column (p. 8297) and main-05 left column (p. 8298): Gibbs excess maxima AT 470335 3.5, AT 100004 3.0, AC3 2.9 and AT 470344 2.7 wt%. Each is merged with the highest digitized point of its Fig. 2a isotherm: rows M4, M20, M48 and M13.
- Text, main-05 left column (p. 8298): AC1 and AC2 "with the maximum capacity of hydrogen adsorption under 2.3 wt%". Upper-bound rows M39 and M46 (77 K, pressure_unstated, no isotherm_id).
- Fig. 4, main-05 (p. 8298): 298 K excess isotherm of AT 470335. Only the highest-pressure marker is digitized (14.71 MPa): row M11.

## Digitization

- Calibration, Fig. 2a (main-04.png pixels, index convention). x: 0 MPa = 199.45 and 20 MPa = 571.39 (frame lines, which carry the 0 and 20 ticks). Checked at the 10 MPa tick (385.66): error 0.13%. y: 0 wt% = 392.49 and 10 wt% = 120.53. Checked at the 5 wt% tick (256.54): error 0.02%. Each tick position is the intensity-weighted centroid of its tick pixels.
- Calibration, Fig. 4 (main-05.png). x: 0 = 191.84 and 20 MPa = 565.23 (frame lines). Checked at 10 MPa (379.0): error 0.25%. y: 0 = 394.31 and 1.00 wt% = 120.55. Checked at 0.50 (257.0): error 0.31%.
- Fig. 2a is greyscale. All six carbon series are black, joined by fitted curves, and their markers overlap. The tool's colour isolation cannot tell the series apart, so each series was prepared as follows. Every marker was assigned to a series by its symbol (square, circle, triangle, star, x, +). Its centre was found by a least-squares fit of synthetic templates of those symbols to the page's darkness, fitting overlapping markers jointly in each pressure column. The original ink inside the fitted footprint was then recoloured red on a white copy of the page (work/series_imgs/). Finally, digitize_figure.py extract --mode markers --open-px 0 ran on that copy with the same calibration. The tool extracted exactly as many markers as were assigned in every series: AT 470335 9/9, AT 100004 7/7, AC3 7/7, AT 470344 7/7, AC1 9/9 + 4/4, AC2 6/6.
- AC1's markers come in near-pairs about 0.2-0.5 MPa apart (4.3/4.8, 9.6/9.9, 12.2/12.4 and 14.3/14.6 MPa), and the paired markers touch. Its archive is therefore split into fig2a_AC1_a.json and fig2a_AC1_b.json. Both belong to one plotted series and are coded as one run, I5, adsorption branch. The paper does not explain the pairs.
- Fig. 4 has no lines, and the highest-pressure AT 470335 marker stands alone. It was digitized straight from the page image (colour #000000, small ROI).
- Step-6 checks (digitize_figure.py check) passed at the pressure of each maximum: AT 470335 against 3.5 and 3.6, AT 100004 against 3.0, AC3 against 2.9 and AT 470344 against 2.7 wt% (all within 2.1%). AC1, AC2 and Fig. 4 remain "unchecked" because the paper states no value to check them against.
- Confidence. 3 for markers that stand apart: all AT 470335 squares, the AT 100004 circles (on top of each stack), the AT 470344 stars at 11.4 and 13.3 MPa, the AC1 crosses at 2.3, 4.3, 4.8 and 7.0 MPa, and the AC2 plus signs at 2.0 and 3.8 MPa. 2 for markers whose position comes from a joint fit inside a stack.
- Triangle templates are centred on their bounding box. If the plotting software centres triangles on the centroid instead, the AC3 values would be about 1 px (0.04 wt%) lower. That is below the 0.1 wt% floor (1% of the axis span).
- isotherm_point_count is the number of markers counted separately: I1 9, I2 11, I3 7, I4 7, I5 13, I6 6, I7 7. These are lower bounds, because low-pressure markers could not be counted (see below).

## Markers that could not be separated (Fig. 2a), not extracted

- About 0.43 MPa and 0.97 MPa: the markers of AT 100004, AC3, AT 470344 and AC2 form two solid blobs (x ≈ 204-212 px and 213-222 px, y ≈ 313-340 px). Joint template fits left 30-50% of the ink unexplained, so the markers cannot be told apart. The AT 470335 squares at these pressures sit outside the blobs and are extracted. The AC1 cross at 1.13 MPa is extracted at confidence 2: its right half is clear of the blob.
- Below about 0.35 MPa, every series, including the zeolites, merges into a solid black mass along the y axis. Markers there can be neither counted nor extracted.
- A possible AT 470344 star at about 14.8 MPa inside the 14-15 MPa cluster improves the fit only marginally (unexplained ink 0.128 → 0.115), so it is not extracted.
- A possible AC2 plus sign at about 9.6-9.9 MPa improves the fit only from 0.227 to 0.207, and its position is unstable, so it is not extracted.
- At about 12 MPa the composition of the lowest cluster is uncertain. Two AC1 crosses plus one AC2 plus sign fit best (0.259 unexplained). Alternatives that include a star fit worse (0.30-0.32). The best composition is extracted, at confidence 2.

## Conflicts noted in rows

- The paper gives the AT 470335 maximum twice: as 3.5 wt% (M4, merged with the digitized point at 3.527 wt%) and as "ca. 3.6 wt% at 2–5 MPa" (M10). Both rows carry isotherm I1 and the same digitized pressure.
- The text says the maximum capacity of AC1 and AC2 is "under 2.3 wt%". The digitized Fig. 2a maxima are higher: AC1 2.408 wt% at 2.32 MPa and AC2 2.339 wt% at 3.85 MPa.

## Values seen but not extracted

- Zeolites KÖSTROLITH 5A and KÖSTROLITH 13X K2 are not carbon sorbents. They appear in the Fig. 2a and Fig. 3a isotherms, in Fig. 6 and Fig. 7, in Table 1 (605 and 609 m2 g-1, V_P 0.37 and 0.39, V_micro 0.25 and 0.24, d_P 0.5 and 1.3 nm), in Table 2 (0.750 and 0.835 g cm-3, V̂s 0.402 and 0.406) and in the text (maximum under 2.3 wt%).
- The hydrophilic silica aerogel is not a carbon. It appears in Fig. 2b and Fig. 3b, in Table 1 (942 m2 g-1, V_P 5.62, d_P 23.9 nm) and in the text (2.6 wt%; maximum at 5–8 MPa with a maximal excess of ca. 2.6 wt%).
- MOFs are not carbon sorbents. Basolite A100 (2.8 wt%), Cu-MOF (1) (under 2.3 wt%), Cu-MOF (2) (4.2 wt%) and MOF-5 (5.5 wt% at 77 K and 4 MPa, ca. 4.1 wt% at 77 K and 1 MPa) appear in Fig. 2b, 3b, 4, 5, 6, 7 and 8 and in Tables 1 and 2. The literature MOFs MOF-177, MOF-200, MOF-205, MOF-210 and UMCM-2 appear in Fig. 2b, Fig. 5, Fig. 6 and Table 1, with values cited from refs. 55-57. The MOF-5 / Cu-MOF (2) storage comparison is also excluded: 540 vol% at 13 MPa, 176 and 279 vol% at 1 MPa, and deliverable capacities of 364 and 261 vol%.
- Fig. 3a (main-04) plots the same 77 K excess data as Fig. 2a against gas-phase density, so it duplicates the Fig. 2a points and is not digitized. Its per-sample linear extrapolations to zero excess (intercepts about 0.07-0.12 g cm-3; the text says "observed values are in the range above 0.07 g cm-3") are fitted values and are not extracted.
- Fig. 5 (main-05) plots maximum excess at 77 K against A_BET. It is not an isotherm, so it is not digitized. It shows maximum values for AC1 and AC2 that the text gives only as "under 2.3 wt%". The correlation n_exc = (0.00231 ± 0.00015) A_BET, and the derived A_BET of ca. 2580 and 3860 m2 g-1 for 6 and 9 wt%, are computed across samples, so they are not rows.
- Fig. 6 (main-06) plots maximum excess at 77 K against V_micro. It is not an isotherm, so it is not digitized. It again shows the AC1 and AC2 maxima only graphically. The correlation n_exc(ACs) = 1.279 + 2.951 × V_micro, and the derived V_micro of ca. 1.58 and 2.58 cm3 g-1, are computed across samples, so they are not rows.
- Fig. 7 (main-07) shows the stored volume of hydrogen at 77 K in a theoretical tank (cm3 at 293 K and 0.1 MPa per cm3 of tank) for AT 470335, AT 100004, AC3, AT 470344 and AC1. The authors left out AC2 as similar to AC1. These curves are computed by the authors with Eq. 1-2 from the Fig. 2 excess data, the Table 2 densities and the H2 gas density, and they include compressed gas. They are not measured uptake isotherms, no §11.0 conversion exists for the unit, and the carbon markers overlap heavily, so Fig. 7 is not digitized. The text's break-even pressures against compression are not uptake values: AC1 and AC2 ca. 12 MPa, AT 470344 ca. 14 MPa, AC3 and AT 100004 ca. 15 MPa, AT 470335 ca. 16 MPa (extrapolated).
- Fig. 8 (main-07) shows the stored volume at 298 K for AT 470335 (and MOFs). It is computed in the same way as Fig. 7 and is not digitized.
- Fig. 4: the AT 470335 points below the highest pressure are not extracted, because only the highest-pressure point is in scope at temperatures other than 77 K.
- Fig. 1 is a schematic with no data.
- Cited or reference numbers are not measurements by this paper: DOE targets; liquid-H2 density 70.8 kg m-3; 0.076 g cm-3 at 15 K; Poirier and Dailly 0.05-0.07 g cm-3; Lozano-Castelló 1.48 cm3 g-1; the 67.55 wt% claim (ref. 81); Getman binding energies (-28, -10 and -80 kJ mol-1).
