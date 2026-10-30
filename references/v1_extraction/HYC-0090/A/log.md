# Extraction log, HYC-0090, extractor A

74 rows in rows.csv (M1 to M74). 24 archives in digitizations/. Validator (`--errors-only`): no errors.

## Sources extracted from

- Fig. 8a (main p. 12806, 77 K, total gravimetric uptake wt.%, 7 samples): digitized in curve mode, 7 archives `fig8a_<series>.json`; rows at 10, 20, ..., 90 bar for each sample (the 100 bar point is the text row, see below).
- Fig. 8b (main p. 12806, 77 K, total volumetric uptake g/L, 7 samples): digitized in curve mode, 7 archives `fig8b_<series>.json`; the volumetric value of each 10 to 90 bar row comes from here and goes on the same row as the gravimetric value (same sample, temperature and pressure).
- Fig. 9a and 9b (main p. 12807, 298 K, total gravimetric and volumetric, 5 samples): digitized in curve mode, 10 archives `fig9a_<series>.json` and `fig9b_<series>.json`; only the highest-pressure point (100 bar) of each isotherm is used, as the 298 K rule requires, and it is the text row (the printed value is the same measurement).
- Sec. 3.4 text, p. 12807, 77 K: gravimetric "6.5, 5.9, 5.3, 5.0, 4.3, 3.4, and 2.1 wt.%" and volumetric "24, 36, 29, 23, 18, 13, and 9 g/L" for DACA, in situDIW, DIW, Cold-5tDACA, Hot-5tDACA, Hot-10tDACA, Hot-15tDACA in the stated order (7 rows, M10, M21, M32, M42, M53, M64, M74). The printed value has no pressure; the pressure is taken as the plotted end point at 100 bar (pressure digitized). Merged with the plotted end point of the isotherm, no separate digitized row.
- Abstract p. 12798 and Conclusions p. 12809 (in situDIW 5.9 wt.% and 36 g/L at 77 K, 1.8 wt.% and 6.9 g/L at 298 K, all "at 100 bar"; DACA 6.5 wt.% and 24 g/L): same measurements as the text rows above; the in situDIW rows (M10, M11) carry the printed pressure of 100 bar.
- Sec. 3.4 text, pp. 12807 and 12808, 298 K: gravimetric "~2.1 and ~1.8 wt.%" (DACA, in situDIW) and "~1.3, 0.8, and 0.6 wt.%" (DIW, Cold-5tDACA, Hot-5tDACA); volumetric "2.5 (Hot-5tDACA), 2.8 (Cold-5tDACA), 5.0 (DACA), 6.0 (DIW), and 6.9 g/L (in situDIW)". 5 rows (M11, M22, M33, M43, M54). The "~" values are stored with `uptake_bound = approximate`; the in situDIW row uses the abstract's unqualified 1.8 and 6.9 and is `exact`.
- Table 1 (main p. 12805): characterization of all 7 samples (BET area, t-plot micropore area, Vtot, V<0.7, Vmicro/Vtot, V0.7-25, V>25, average pore width), repeated on every row of the sample; bulk densities 0.52 (in situDIW), 0.21 (DACA), 0.45 (DIW) g/cm3 from the Sec. 3.4 text, stored as `packing_density_g_cm3`.
- Sec. 2 and SI S1 (p. S4 to S5): instrument, degassing, calibration, replicates, sample mass, basis. Basis is "total" from SI eq. S1 (excess plus rho_gas x Va) and the text heading "High-Pressure Total H2 Adsorption Isotherms"; the wt.% convention is not defined (`unknown`).

## Digitization method

- All Fig. 8 and Fig. 9 isotherms plot hundreds of overlapping markers that merge into one continuous band; the markers cannot be separated or counted, so marker mode was not usable (it returned about 4 points) and curve mode was used on every series. The marker count check of the instructions (step 6) cannot be done; `isotherm_point_count` is empty on every digitized row and `fitted_interpolated` is the `value_kind`. The paper does not say the lines join measured points.
- p_end = 100 bar for every line (highest-pressure end, last marker at 100 bar), so the 10 pressures are 10, 20, ..., 100 bar. The 100 bar value of every sample is the printed text value, not a digitized row.
- Calibration (pixel positions found by inspecting the page image, third tick checked by the tool): Fig. 8a x 0 and 100 bar, check at 60; y 0 and 7 wt.%, check at 4. Fig. 8b x 0 and 100, check at 60; y 0 and 35 g/L, check at 20. Fig. 9a x 0 and 100, check at 60; y 0 and 2.5 wt.%, check at 1.5. Fig. 9b x 0 and 100, check at 60; y 0 and 7 g/L, check at 4.
- Each series was isolated on a copy of the page in which the legend entries were masked (work/m_<fig>_<series>.png), so legend swatches of the same colour could not be picked up. Colour tolerance 40, except Hot-15tDACA (lilac, close to the lilac anti-aliased edge of the in situDIW purple band) where tolerance 20, a region limited to the lower part of the plot and a masked purple legend entry were used.
- Sample ordering: S1 in situDIW (the optimized sample, first named in the abstract), S2 DACA, S3 DIW, S4 Hot-5tDACA, S5 Cold-5tDACA, S6 Hot-10tDACA, S7 Hot-15tDACA, in the order they first appear in the Experimental and Results sections. Rows are ordered by sample, 77 K by ascending pressure, then the 298 K row.
- Isotherm IDs: I1 to I7 are the 77 K isotherms S1 to S7; I8 to I12 are the 298 K isotherms of S1 to S5.

## Digitized versus printed, end point (100 bar)

The printed value is stored on the row; the digitized end point is in its notes.

| Sample | T (K) | Printed gravimetric (wt.%) | Figure | Printed volumetric (g/L) | Figure |
|---|---|---|---|---|---|
| in situDIW | 77 | 5.9 | 5.97 (+1.1%) | 36 | 37.3 (+3.7%) |
| DACA | 77 | 6.5 | 6.70 (+3.0%) | 24 | 24.5 (+2.0%) |
| DIW | 77 | 5.3 | 5.23 (-1.2%) | 29 | 31.6 (+9.1%) |
| Hot-5tDACA | 77 | 4.3 | 4.32 (+0.5%) | 18 | 18.1 (+0.8%) |
| Cold-5tDACA | 77 | 5.0 | 5.07 (+1.3%) | 23 | 23.7 (+3.1%) |
| Hot-10tDACA | 77 | 3.4 | 3.38 (-0.6%) | 13 | 13.4 (+3.1%) |
| Hot-15tDACA | 77 | 2.1 | 2.08 (-0.7%) | 9 | 9.5 (+5.2%) |
| in situDIW | 298 | 1.8 | 1.76 (-2.1%) | 6.9 | 6.8 (-1.2%) |
| DACA | 298 | ~2.1 | 2.20 (+4.8%) | 5.0 | 5.1 (+2.3%) |
| DIW | 298 | ~1.3 | 1.49 (+14.3%) | 6.0 | 6.1 (+0.9%) |
| Hot-5tDACA | 298 | ~0.6 | 0.93 (+54.2%) | 2.5 | 2.7 (+7.7%) |
| Cold-5tDACA | 298 | ~0.8 | 1.12 (+39.6%) | 2.8 | 3.3 (+17.6%) |

- The paper's printed values and its plotted end points disagree by more than rounding for several samples, mostly at 298 K, where the printed "~" gravimetric values are lower than the plots. I did not reinterpret either: the printed text value is stored, the figure value is in `notes`, and `extraction_confidence` is 3 (not 4) on those rows. The 10 to 90 bar rows of DIW at 77 K come from the figure (the printed 29 g/L is 9% below the plotted 31.6 g/L), with `extraction_confidence` 2 and a flag in `notes`. A reconciler should decide which of the two the paper means.
- Check history (disclosure). While testing, I ran `digitize_figure.py check` on some archives with tolerances I chose myself (the instructions do not require that step). Seven archives were marked "discarded" because the printed value disagreed with the trace by more than the tolerance I had set; one run on `fig8b_Hot15t.json` with a looser tolerance could not reverse a "discarded" status, which is sticky. I did not record which seven, so I do not list them here. I then re-extracted all 24 archives from the same images with identical parameters (`--overwrite`), so all 24 now show status "unchecked". "Unchecked" does not mean they passed; the table above is the actual comparison.

## Flags and omissions

- Hot-5tDACA at 10 bar: not extracted. The curve is hidden behind the Hot-10tDACA curve around 10 bar in Fig. 8a and 8b (trace of 2 pixels in each panel), so no reliable value exists. Its first row is at 20 bar. All other samples have rows at 10, 20, ..., 90 bar.
- DACA at 90 bar, volumetric: trace partly hidden by a neighbouring curve (4.0 px vs 6.0 px per column); `extraction_confidence` 2. Any other row where a trace was mostly hidden carries the same flag in `notes`.
- in situDIW volumetric values at 20 to 90 bar (Fig. 8b): above the highest labelled y tick (35 g/L); the tool reports them as extrapolations. Kept, with the y axis extended linearly; the unlabelled minor tick at 37.5 g/L fits the extension. Flagged in `notes`.
- Fig. 9b legend: the orange curve (DACA colour in Fig. 9a) is labelled "DIW" in the Fig. 9b legend. Assigned to DACA by colour match with Fig. 9a and by the text order (5.0 g/L for DACA). Noted in `source_location`.
- Hot-10tDACA and Hot-15tDACA have no 298 K isotherm and no 298 K value anywhere in the paper; no 298 K rows.
- Degassing: main text says all sorbents degassed at 120 °C for 12 h (stored); SI S1 says 10 h at each sample's activation temperature, and later 150 °C for 12 h to about 6.7e-2 Pa. Conflict recorded in `notes`; 120 °C and 12 h stored with the SI end pressure.
- Sample mass 0.2 to 0.5 g (SI, a range): not stored, `sample_mass_mg` empty. Bulk density of the four pellets is only a range 0.5 to 0.55 g/cm3: not stored.
- Table 1 column "V<0.7" has the footnote "Vmicro" in the table and the text calls it ultramicropore volume; stored as `ultramicropore_volume_cm3_g` with cutoff 0.7 nm, `micropore_volume_cm3_g` left empty.

## Values seen and not extracted

- Fig. 10a (main p. 12808, Gex versus rho_gas at 77 K, Ono-Kondo fits, 5 samples: DACA, in situDIW, DIW, Cold-5tDACA, Hot-5tDACA): not digitized. The x axis is gas density in g/L, not pressure, and the paper prints no pressure for these points, so a row would have no pressure unless one is computed from an equation of state, which is outside the paper. The curves are a re-expression of the same 77 K measurements as Fig. 8 (excess instead of total basis). The curves peak at a gas density of roughly 20 to 25 g/L and fall to zero at 100 g/L (a model extrapolation); the peak values are not in the text or the tables. Judgment call: flag for the reconciler; if the project wants excess-basis rows, a pressure conversion rule is needed first.
- Fig. 10a fit results in text: Vfilm 0.55 (DACA), 0.50 (in situDIW), 0.43 (DIW), 0.18 (Cold-5tDACA), 0.17 (Hot-5tDACA) cm3/g; saturated film density 100 +/- 20 g/L; liquid H2 density 71 g/L: not H2 uptake values; not extracted.
- Fig. 10b and text: Qst maxima 11.5 (DACA), 10.9 (in situDIW), 9.5 (DIW), 8.4 (Cold-5tDACA), 7.1 (Hot-5tDACA) kJ/mol, Qst curves against Gex (up to about 1 wt.%): heats of adsorption, not uptake; not extracted. Gex values on the Fig. 10b x axis are derived from isotherms at 298, 313 and 328 K that are not shown.
- 313 K and 328 K isotherms (Qst determination, Sec. 3.5, SI S2): the paper says the sorbents were measured at 298, 313 and 328 K, and the main-text SI list names "Gravimetric H2 adsorption isotherms at different temperatures", but the SI file I was given (Fig. S1 to S4 and text) contains no such figure or table. No 313 K or 328 K values available; none extracted.
- Fig. 11 (main p. 12808, benchmark of volumetric against gravimetric uptake, DOE targets and literature sorbents): not an isotherm; the other points are other materials from other papers (HKUST-1 monolith, ZTC, MOF-177, IRMOF-20, NU-1102, NU-1501-Al, Ni2(m-dobdc), Li-doped MOF-5, AX-21, MSC-30, CA-4700, carbon MWCNT, CA T20-F25-KOH, polypyrrole-AC, cryo-compression) and are not carbon sorbents measured here, or are literature values; not extracted. Observation: the in situDIW marker appears to sit above the 36 g/L printed in the abstract and text (roughly 40 g/L judged from the axis ticks; not digitized with the tool and not used); the text value was used. Flag for the reconciler.
- DOE 2025 targets "5.9 wt.% and 36 g/L" (text p. 12808): targets, not measurements; not extracted.
- Introduction p. 12798: Sethia et al. (ref. 20) 5.65 wt.% at 77 K and 0.4 wt.% at 298 K at 22 bar; the authors' own earlier DACA (ref. 7) "up to 6.8 wt.% and 28 g/L at 77 K and 100 bar"; Cao et al. (ref. 24) 9.4 wt.% H2 released in 10 min at about 95 °C (a hydride composite, release not uptake). All are results of other publications, not measurements in this paper. The 6.8 wt.% and 28 g/L value belongs to the DACA of ref. 7; the paper does not say it is the DACA sample measured here (this paper's DACA gives 6.5 wt.% and 24 g/L), so it gets no row and no `previously reported` tag. Flag for the reconciler.
- Table 1 and text, N2 77 K data, Fig. 7 (porosity), XRD (Fig. 5), XPS (O/C ratios), EDS (SI Fig. S4), SI Fig. S1 to S3 (compressive stress, rheology, viscosity): characterization only, no H2 uptake; used for the sample-level columns only (Table 1, O/C, functional groups) and otherwise not extracted. The previously reported micro-mesoporous structure of DACA (ref. 7: Murugavel, Rownaghi, Rezaei, Chem. Mater. 2024, 36 (18), 8565-8577) is a structural statement, not an H2 value; noted in the DACA rows.
- Adsorption/desorption branches: the text says there is no hysteresis between the H2 adsorption and desorption branches and the isotherms are reproducible, but Fig. 8 and Fig. 9 show no separable desorption branch (one marker band per sample). All rows are `isotherm_branch = adsorption`; nothing extracted for desorption.
- 298 K replicate statement ("at least in duplicate, deviations below 5%"): stored as `replicates_reported = true` on the 298 K rows only; the deviation is relative, so `uncertainty_wt_pct` is empty. No individual replicate values are printed.
- Peak pressure region of the 298 K isotherms (below 100 bar): not extracted, per the rule of one point (highest pressure) at temperatures other than 77 K.
