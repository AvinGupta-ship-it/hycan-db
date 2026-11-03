# Extraction log, HYC-0107 (Bastos-Neto 2012), extractor A

Rows written: 16 (HYC-0107-M1 to M16). Samples: S1 AT 470335, S2 AT 470344, S3 AT 100004, S4 AC1, S5 AC2, S6 AC3 (all commercial activated carbons). Isotherms: I1 S1 77 K, I2 S2 77 K, I3 S3 77 K, I4 S4 77 K, I5 S5 77 K, I6 S6 77 K, I7 S1 298 K.

## Extracted from

- Section 2.1, 2.2 (main.pdf p.3): sample sources (S1-S6 suppliers), Rubotherm magnetic suspension balance (no model), "reversible and repeatable within <1%", degassing 423 K / p < 3 Pa / at least 10 h, sample mass 0.5 to 5 g, H2 purity 99.9992 vol%. Attached to every row.
- Table 1 (p.3): ABET, total pore volume (Gurvich), micropore volume (DR), average pore size (BJH) of the six carbons, all "from N2 sorption isotherms at 77 K". Attached to every row of the sample. No BET range or consistency criteria printed. No H2 values in the table.
- Table 2 (p.6): packing (tap) density of the six carbons (packing_density_g_cm3). Helium specific volume V^s is printed, not a density, so skeletal_density_g_cm3 is left empty and V^s is in notes.
- Section 3 text, p.4: "AT 470335 (3.5 wt%)" (M4, merged with the digitized maximum of Fig. 2a), "ca. 3.6 wt% at 2-5 MPa" (M10), "AT 100004 (3.0 wt%)" (M12), "AC3 (2.9 wt%)" (M15). p.5: "AT 470344 (2.7 wt%)" (M11), "AC1, AC2 ... under 2.3 wt%" (M13, M14, upper bounds).
- Fig. 2a (p.4), AT 470335 open squares, 77 K: 9 markers digitized (M1-M9; the marker at 3.79 MPa is the one merged into M4). Archive: digitizations/Fig2a_AT470335_77K.json.
- Fig. 4 (p.5), AT 470335 open squares, 298 K: highest-pressure marker (M16). Archive: digitizations/Fig4_AT470335_298K_highest_pressure.json.

## Digitization details

- Fig. 2a calibration (page image main-04.png): x 199.5 px = 0 MPa, 571.5 px = 20 MPa; y 392.5 px = 0 wt%, 120.5 px = 10 wt%; third ticks x 386.0 px = 10 MPa (error 0.27%), y 256.5 px = 5 wt% (error 0). Tick pixels located from pixel rows and columns (frame lines at cols 199-200, 571-572 and rows 120-121, 392-393).
- All Fig. 2a series are black, so there is no series colour. The open markers have outlines about 1 px wide, and the tool's 3-px opening removes them. For the squares I made a copy of the page image (work/fig2a_squares_filled.png, same pixel grid) in which holes inside marker outlines are filled (threshold < 150), blobs are opened with 3x3, and only solid blobs 6-7 px wide with fill >= 0.95 in the upper carbon band (cy 290-330 px) are kept. The tool then ran in markers mode on that copy: 9 markers extracted, 9 counted on the plot. The archive's source_image points to that copy.
- Cross-check of the 9 centres: tool run on the original page image in a 10x10 px window per square (tolerance 140, open-px 0) agrees to within 0.02 MPa and 0.005 wt%.
- Check against a stated value passed: digitized 3.531 wt% at 3.8 MPa vs stated 3.5 wt% (0.88%, tolerance 5%).
- Count of AT 470335 markers on Fig. 2a: 9 resolvable. Markers at p < ~0.3 MPa coincide with the y axis and the other series' markers (a partly hidden open square is visible at the axis near 0.1 MPa, 1.9 wt%) and cannot be counted or separated; isotherm_point_count = 9 is therefore a lower bound.
- Fig. 4 calibration (main-05.png): x 192.0 px = 0 MPa, 565.3 px = 20 MPa; y 394.3 px = 0, 120.5 px = 1.00 wt%; third ticks x 379.0 px = 10 MPa (0.19%), y 257.0 px = 0.5 wt% (0.29%). The highest-pressure square is isolated; tool run on the original image in a 12x12 px window (tolerance 140, open-px 0): 14.718 MPa, 0.578 wt%. Repeats with tolerance 90 and 180 and a larger window gave 14.655 to 14.718 MPa and 0.578 to 0.579 wt%.
- Fig. 4 archive status is "unchecked": the paper states no number for the 298 K isotherm of AT 470335 (only "essentially identical for all three samples"), so the check against a stated value cannot be run. Placement was verified by overlay on the page image.
- Fig. 4 isotherm_point_count = 11: distinct squares resolved at about 14.7, 13.9, 12.1, 10.7, 9.4, 7.8, 6.1, 4.6, 3.2, 2.3 and 1.7 MPa; the cluster below ~1.5 MPa overlaps the other two series and cannot be counted, so 11 is a lower bound.
- No desorption branch is shown in either figure (the text says the isotherms were reversible).

## Markers I could not separate (not digitized)

- Fig. 2a, AT 100004 (open circles), AC3 (open triangles), AT 470344 (stars), AC1 (crosses), AC2 (plus signs): all drawn in black and overlapping from about 0.4 MPa to 14.6 MPa, with up to five markers within a 7 px marker width at the same pressure and the series converging above 10 MPa. Colour cannot separate them and blob analysis merges them. No point of these five series was extracted from the figure; their only rows are the text maxima (M11-M15). Their isotherm_point_count is empty. Their text maxima have value_kind = unclear because no digitized point of the same isotherm exists to compare with (AC1, AC2 bounds are measured by rule).

## Values seen but not extracted

- Fig. 2a, KÖSTROLITH 5A and 13X K2 (zeolites): not carbon.
- Fig. 2b and text: Basolite A100 (2.8 wt%), Cu-MOF (1) (under 2.3 wt%), Cu-MOF (2) (4.2 wt%), MOF-5 (5.5 wt% at 77 K and 4 MPa; ca. 4.1 wt% at 77 K and 1 MPa), hydrophilic aerogel (2.6 wt%, maximum at 5-8 MPa; a silica aerogel), both zeolites (under 2.3 wt%), and MOF-177, MOF-200, MOF-205, MOF-210, UMCM-2 (literature data, refs 55-57): not carbon.
- Fig. 4: Cu-MOF (2) and MOF-5 at 298 K: not carbon. The other AT 470335 markers at 298 K: only the highest-pressure point is digitized at temperatures other than 77 K.
- Fig. 3 (excess uptake against gas-phase density, with linear extrapolations): re-plot of the Fig. 2 data on a density axis, not a pressure isotherm; not digitized. The extrapolated densities (about 0.07 to 0.12 g cm-3) are fits, not measurements.
- Fig. 5 (maximum excess uptake at 77 K against ABET) and Fig. 6 (against micropore volume): not isotherms. They show a maximum for AC1 and AC2 that the text gives only as an upper bound (under 2.3 wt%); not read from the plot. The fits n_exc = (0.00231 +/- 0.00015) A_BET and n_exc(ACs) = 1.279 + 2.951 V_micro are regression results.
- Fig. 7 (77 K) and Fig. 8 (298 K): stored volume of hydrogen per tank volume (cm3 cm-3 at 293 K, 0.1 MPa), computed from the excess isotherm, bed packing density and gas density (Eqs. 1, 2); not an uptake isotherm in schema units, not digitized. The text gives volumetric values for MOF-5 and Cu-MOF (2) only (540, 176, 279, 364, 261 vol%): not carbon. No volumetric value is printed for any carbon.
- Derived or projected values: 6 and 9 wt% DOE targets, "ideal" sorbent ABET 2580 and 3860 m2 g-1 and micropore volume 1.58 and 2.58 cm3 g-1: not measurements.
- "uptake of up to 67.55 wt%" (ref. 81, Chambers et al.): a literature claim, not a measurement in this paper. Micropore volume 1.48 cm3 g-1 (Lozano-Castello, ref. 78): literature, no H2 value.
- Table 1 and Table 2 rows for zeolites, aerogel and MOFs: not carbon. No carbon sample has characterization without an H2 value.

## Coding decisions worth a second look

- basis_stated = true: Section 3 defines the excess capacity ("refers to the amount of hydrogen present in the adsorbed layer in excess of the bulk gas density") and also defines absolute and total capacity; the values are called Gibbs excess.
- wt_pct_convention = unknown, source none: the paper never defines the convention of the wt% values; the nomenclature gives m_excess,w in g g-1 and gravimetry is said to give "the amount stored by the unit mass of adsorbent", which points to W1 but is not a definition of the reported wt%. No paired unit for any point.
- calibration_described = false: no buoyancy correction or free-volume determination is stated for the H2 isotherms; helium specific volume V^s appears only in the stored-mass equation (Eq. 1) and Table 2.
- instrument_identified = false (Rubotherm named, no model). replicates_reported = true ("repeatable within <1%", a stated reproducibility in %); uncertainty_wt_pct left empty because the figure is relative.
- area_same_sample = yes: Table 1 is the textural data of "the studied adsorbents" from N2 at 77 K, without citation for the carbons (the MOFs taken from literature carry citations); N2 degassing conditions are not stated.
- M4 (printed 3.5 wt%, no pressure) is merged with the digitized maximum of the AT 470335 isotherm (3.532 wt% at 3.786 MPa, 0.9% from the printed value); pressure taken from the digitization. M10 ("ca. 3.6 wt% at 2-5 MPa") is a second printed value for the same maximum; its pressure is a range, so no single pressure is stored and pressure_unstated = true, with the range in notes.
- measuring_lab_id: corresponding author R. Glaser (marked *), first affiliation a, "Institut fur Nichtklassische Chemie e.V. an der Universitat Leipzig", which names a university; the paper does not say the H2 measurements were made elsewhere.
- Temperatures 77 K and 298 K are printed numbers (temperature_inferred = false). Degassing 423 K stored as 149.85 C; "p < 3 Pa" and "at least 10 h" are bounds stored as 3 Pa and 10 h.
