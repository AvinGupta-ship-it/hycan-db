# HYC-0116 extractor A log

## Extracted from
- Main text sec. 2.1-2.3: samples, degassing (373 K 48 h; 3-Flex 383 K at least 24 h), HPVAII and 3-Flex instruments, about 1.2 g sample, pressure steps, repeatability statement (no results, so replicates_reported false).
- Main text sec. 3.1: excess and absolute definitions (basis evidence).
- Main text p.17 (3.2): 77 K values at 4 MPa (5.78, 4.74, 4.04, 3.24, 2.90, 2.31; Filtrasorb400 ambiguity noted in rows), Filtrasorb400 2.34 wt% at 3 MPa (merged with the plotted 3.03 MPa point of Fig 2a), 273 K values at 14 MPa (merged with the plotted highest-pressure point of Fig 2b; six rows, isotherms I7-I12).
- Main text p.26 (3.3): maximum absolute H2 at 77 K, six values (pressure not stated).
- Fig 2a (77 K, I1-I6): filled (adsorption) and open (desorption) markers digitized, archives fig2a_*.json. SA20 filled markers needed two ROI parts (a, b) to separate them from open markers.
- Fig 2b (273 K): only the highest-pressure marker of each isotherm is a row; each archive also holds the 12.5 MPa marker, which is not a row.
- Fig 5a and 5b (77 K, 3-Flex, I13-I18): digitized, archives fig5a_*.json and fig5b_*.json. 5b markers that coincide with a 5a point are not repeated.
- SI Table S1: all characterization (BET and P/P0 range, NLDFT Vmicro, Vmeso, VT, V<0.7 nm, average pore size, DR-CO2 volume). SNLDFT, Vmicro-average size, V0.7-2 nm and DR-N2 volumes are not stored (no field or redundant); SNLDFT is not an uptake-row field.
- SI Table S2: nmax (MDA parameter), six rows, fitted_extrapolated, no single T or P.
- SI Table S4: Sips N, 66 rows (6 samples x 11 temperatures), absolute, fitted_extrapolated, pressure not applicable; unit not printed, taken as mol kg-1.

## Not extracted (reason)
- Fig 6 (SA20, SA1500, 77 to 273 K): NOT DONE. The 77 K data are the Fig 2a data. The highest-pressure points of the other 20 isotherms were not digitized because the 11 colour-graded series overlap and could not be separated reliably. This is an omission.
- Fig S2 (absolute isotherms of SA20 and SA1500 versus fugacity, Sips fits at 77 K and other T): NOT DONE; derived from the excess data by Eq. (2) and shown with fitted lines.
- Fig 3 (3D and contour plots), Fig 4 (uptake vs area), Fig 7-11, Fig S1, S3: not isotherms; values shown are those in text or tables, nothing extra. Fig 4 shows the same 4 MPa (Filtrasorb400 3 MPa) and 14 MPa values.
- Table S2 Va, alpha, beta, P0; Table S3 R2 values; Qst and entropy values: not uptake.
- Fig 5c Henry constants: not uptake.
- Henry-law regression lines in Fig 5b: lines, not markers.

## Digitization notes and limits
- Calibrations: Fig 2a x ticks 0-12.5 MPa (check tick 5.0), y 0-6 (check 3); Fig 2b y 0-1.0 (check 0.6); Fig 5a x 0-100 kPa (check 60), y 0-2.5 (check 1.0); Fig 5b x 0-1.5 kPa (check 1.0), y 0-0.25 (check 0.10). Tick positions from pixel inspection; verification ticks passed.
- digitize_figure.py check at stated values passed (within 1%) for Fig 2a MSC30, MSP20X, SA1500, TH90I at 4 MPa, Filtrasorb400 at 3 MPa, SA20 at 4 MPa (on a whole-ROI test run, since the archived SA20 series is split), and all six Fig 2b series at 14 MPa. The Fig 2b archives hold two points so the check could run.
- Open markers have no solid pixels of the series colour at their centre, so their centres were found from the enclosed interior of each hollow marker (hole image in the work directory) and then passed through digitize_figure.py in markers mode. MSP20X open markers at 273 K needed tolerance 230.
- Hidden or merged markers (so point counts may be wrong): Fig 2a, markers at p below about 0.3 MPa overlap between series; one near-zero marker per series is hidden, and several are only partly visible. MSC30 filled marker at 5 MPa and MSP20X filled marker at 5 MPa are mostly covered by the open marker (12 px, confidence 2). Two points with digitized pressure at or below zero are not rows (MSC30 -0.633 bar, 1.294 wt%, partly hidden; Filtrasorb400 -0.042 bar, 0.148 wt%) because the schema needs pressure above 0. SA20 shows 4 of 5 open markers separated (the one near 11 MPa is hidden behind the TH90I open marker). Marker count set to 16 (11 adsorption steps + 5 desorption points stated in sec. 2.3) for I1-I12; for 273 K I did not count the plot.
- Fig 5a: heavy overlap. Extracted counts MSC30 24, MSP20X 27, SA1500 23, SA20 19, TH90I 21, Filtrasorb400 9 (orange series merged into a band and partly under SA20); true counts are higher. isotherm_point_count for I13-I18 is the number extracted, a lower bound. Fig 5b TH90I markers could not be separated from the steep line of the same colour; no 5b rows for TH90I.
- Open marker highest-pressure MSP20X 273 K point: coded as the 14 MPa adsorption end point (see row notes).
- Desorption markers in Fig 2a are plotted at pressures other than the 11.5, 8, 4.5, 1.5, 0.5 MPa stated in the text; the plotted positions are used.
- Hysteresis: paper says adsorption and desorption overlap; open markers coded desorption as the caption says.

## Coding notes
- Text gives no wt% convention; unknown/none.
- Labels: printed as MSC30, MSP20X, SA1500, SA20, TH90I (text also prints TH90), Filtrasorb400.
- BET value from Table S1 (3305 for MSC30; main text prints 3310 and 3300 in places). SA1500 BET P/P0 range printed as 0.05-0.018 (probable typo, kept as printed).
- 4 MPa text values are interpolated (4 MPa is not a measured step): value_kind unclear, no isotherm_id.
