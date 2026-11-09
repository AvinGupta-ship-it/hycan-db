# Extraction log, HYC-0123 (agent A)

Rows written: 29, all for sample S1 = PG (Pt@GO, the only carbon sorbent), one isotherm I1 (77 K, adsorption, 29 markers).

## Extracted
- Main text Sec. 3.5 (p. 2164): "PG has a negligible adsorption capacity of 0.2 wt%" at 77 K and 1.1 bar. One row (text_direct), merged with the Fig. 6 PG point at 1.092 bar, 0.1604 wt% (printed 1.1 bar within 0.022 bar of 1.092). No separate digitized row for that point.
- Fig. 6 (p. 2164), PG series, black circles: 28 digitized rows, archive HYC-0123_fig6_PG.json (axes calibrated on 0.0 and 1.2 bar, 0.0 and 2.0 wt%; third ticks 0.6 bar and 1.2 wt% agree within 0.2%). The tool returned 27 clusters; I counted 29 markers on the plot. Two pairs of overlapping markers (clusters at x = 0.19 bar, 107 px, and 0.90 bar, 95 px) were not separated by the tool. I split them from the pixel extents of the thresholded page image (centres at xmin+4 and xmax-4 for a 9 px marker; script work/build.py) and stored them in HYC-0123_fig6_PG_split.json. Those four rows carry extraction_confidence 3.
- Step-6 check not passed: the only stated PG value is "0.2 wt%" (one significant figure); the digitized series at 1.1 bar is 0.1606, 19.7% below it, so `check` at 5% fails. This is consistent with rounding of the printed value (0.15 to 0.25 wt%), but I did not widen the tolerance. The first check run marked the archive discarded; I re-ran the extraction (same inputs, --overwrite), so the archive status is "unchecked". The archive status therefore does not record a pass. Reconciliation should treat the Fig. 6 PG values as unchecked against a printed value.

## Seen, not extracted
- HPG0 (HKUST-1, Cu3(BTC)2 MOF), HPG5, HPG10 (HKUST-1 with 5 and 10 wt% added PG): MOF majority, not carbon sorbents. Not extracted: 77 K isotherms (Fig. 6; text 1.8 wt% for HPG0 at 1.1 bar; HPG5 identical to HPG0), Fig. 7 bar chart (measured and hypothetical values at 77 K, 1.0 bar), 298 K high-pressure isotherms (Fig. 8; text 0.41 wt% HPG0, 0.77 wt% HPG5, 0.15 wt% HPG10 at 80 bar; HPG0 literature ~0.27 wt%, MOF-5 0.28 wt% at 65 bar, MIL-101 0.43 wt% at 80 bar, 4.2-fold CNT@MOF-5 at 100 bar), low-pressure 298 K isotherms (Fig. S11, HPG0, HPG5, HPG10 only, up to about 0.015 wt%).
- Fig. 7 is a bar chart, not an isotherm: not digitized. The PG value is not shown in it.
- Characterization without H2 uptake in a carbon sorbent: GO has XRD d(002) 0.91 nm (interlayer spacing, Fig. S1), outgassed at 80 C, no H2 measurement. Not a row.
- PG characterization: Pt 18.9 wt% (EDS, Fig. S6), no surface area or pore volume given (text: "significantly low and negligible porosity"; Fig. 5 N2 isotherm only, not digitized, not an H2 isotherm).
- Table S1 EDS (HPG0, HPG5, HPG10) and Table S2 (SBET 937, 848, 676 m2/g; Vtot 0.53, 0.55, 0.45; Vmeso 0.10, 0.18, 0.16; Vmic 0.43, 0.37, 0.29 cm3/g) are for MOF-majority samples, not extracted. The text prints these areas with unit "cm2 g-1" (typo for m2 g-1; table S2 uses m2 g-1).
- Figs. 1-4, 5, S1-S10, S12 are XRD, IR, SEM, TEM, EDS, N2 isotherms: no H2 uptake.

## Coding decisions
- surface_area_method = none on all rows: no area for any sample in the rows written. The validator rejected not_reported because the rows contain no area.
- material_class composite (Pt particles on GO); synthesis_method chemical_oxidation (GO by modified Hummers from graphite).
- measurement_method volumetric_sieverts inferred from the ASAP 2020 (Micromeritics) named for the low-pressure H2 measurement at 77 K; instrument_identified true.
- Basis not named: basis_stated false, basis_inferred excess (volumetric default), uptake_type unspecified. wt% convention unknown.
