# HYC-0131 extraction log (agent A)

Run date 2026-11-09. All hydrogen measurements are at 25 C (298.15 K), BELSORP HP, so only the highest-pressure point of each isotherm is extracted. 6 rows written (M1-M6, one per isotherm I1-I6).

## Extracted
- Figure 3 (p.14727, main-05): styrene (5)-adsorbed AC + CB/Pt, closed symbols. Highest point 3.1712 MPa, 0.6428 wt% -> M1. Axes calibrated on 0/3.5 MPa and 0/0.7 wt% ticks, verified on 2.0 MPa and 0.4 wt% (left-axis tick pixels are irregular by up to 1.4 px; verify passed). 10 of 11 closed markers extracted (marker at origin merged with the axis line). Point count 22 = 11 closed + 11 open visible.
- Figure 4a (p.14728, main-06): pristine AC ("none") -> M2, 3.148 MPa, 0.2612 wt%; naphthalene (10) -> M3, 3.1013 MPa, 0.0153 wt%. Verified on 1.5 MPa and 0.15 wt%. Pristine AC: 14 of 15 closed markers extracted; the origin marker is hidden behind the green series and the legend marker (0.283 MPa, 0.2768) is not data. Naphthalene: only 6 of about 10 closed markers separated (earlier ones overlapped by other series). Counts for I2 (23) and I3 (17) are estimates.
- Figure 5a (p.14729, main-07), left axis (wt%): 21 -> M4, 3.185 MPa, 0.0601 wt%; 22 -> M5, 3.1776 MPa, 0.0136 wt%; 23 -> M6, 3.0843 MPa, 0.0480 wt% (marker partly hidden behind 21, 9 px visible against 23-26 px for a free marker; confidence 2). Verified on 1.5 MPa and 0.18 wt%. The legend markers at 1.63 MPa appear in the archives and are not data. Point counts 21, 20 and 19 are estimates.
- Table 1 (p.14728), Table 2 (p.14729), Table S2 (SI p.S8): BET areas and pore volumes for the samples above (non-normalized values stored; normalized per g AC in notes). Surface areas are per gram of the filled sample (ratio normalized/non-normalized is about 1.4, the mass of 5 mmol organic per g AC plus CB/Pt).
- Main text 2.1 to 2.4: instrument (BELSORP HP, Microtrac), H2 purity (>99.99999%), BET range (P/P0 0.05-0.20), DR micropore volume, Vtotal at P/P0 0.96. Table S1 (SI p.S2): adsorption temperatures and amounts (5 mmol per g AC).

## Isotherms seen but not extracted
- Figure 4a, biphenyl (9), anthracene (11), phenanthrene (12), pyrene (13): near the zero line, markers largely overplotted. 9, 11 and 12 could not be separated by colour (no markers found). The pyrene (13) archive (HYC-0131_Fig4a_pyrene-13.json) has 10 points, the last at 3.0887 MPa, -0.0034 wt%; its markers, like those of 9, 11 and 12, lie on or just below the zero line. Schema v2 requires uptake_wt_pct >= 0, so no row is written for a negative reading. Rows for 9, 11, 12 and 13 would be about 0 or slightly negative.
- Figure 5a, anthraquinone (18): last six closed markers (to 3.099 MPa) are at -0.0002 to -0.0024 wt%, below the zero line; negative, no row (archive HYC-0131_Fig5a_18.json).
- Figure 5a, tetrahydropyran (19) and cyclopentanecarboxylic acid (20): all markers are hidden behind series 21, 22 and 23 (digitizer found only the legend marker). No values.
- Figure 5a, 2-tert-butyl-1,4-benzoquinone (16), 1000 s and 5000 s exposure curves (closed circles and triangles): plotted against the right axis (H/16 molar ratio, arrow in legend), not wt%. The right-axis reading of the end points (about 0.88 and 1.04) does not match the text maxima (H/16 = 1.07 at 1000 s, 1.25 at 5000 s; conversion 53% and 63%), so no value is taken from this axis. H/16 is not a unit of the schema. Not extracted (two isotherms of one sample).
- Figure 1e: CB/Pt alone (grey markers) is almost entirely hidden behind the "without CB/Pt" (MoO3 alone) series at 0 wt%; no grey marker could be separated. Text states "MoO3 and CB/Pt did not adsorb any H2 gas" (not a number; no row). CB/Pt has no surface area reported.
- Figure 1e, CB/Pt + MoO3 mixtures (maximum 1.14, 1.09, 0.99, 0.87, 0.63, 0.22 wt%; H/Mo 1.65, 1.57, 1.42, 1.26, 0.92, 0.32) and MoO3 alone: not carbon sorbents (MoO3 is the majority phase, about 99 wt%). Not extracted.
- Text: maximum H/styrene = 2.05 (Figure 3), H/16 = 1.07 and 1.25: molar ratios of H atoms to organic molecule, not uptake units of the schema; not extracted separately. Figures 4b, 5b and S5 (N2 isotherms at -196 C, volume adsorbed in cm3(STP) per g AC): not H2 uptake. 
- Autoclave experiments (Schemes 1-3: GC yields of 1, 4, 5, 8, 14, 16 hydrogenation at 4 MPa, 25 C): reaction yields, not H2 uptake. Compounds 1, 4, 8 have no H2 uptake isotherm and no characterization. Compound 14 (cyclooctanone) has N2 characterization (Table 2: SBET 41, Vtotal 0.02, Vmicro 0.01, Vmeso 0.01; normalized 66, 0.04, 0.02, 0.02) but no H2 isotherm (autoclave only); no row.
- Figure 1f,g, 2, S1-S4: XRD, XPS, TEM, SEM, not uptake.
- Spillover rates (844 and 1432 H atoms per Pt nanoparticle per second; 5.06 million per hour): derived quantities, not uptake.

## Decisions
- Samples numbered only for samples with a row, in order of the first H2 data: styrene (5), pristine AC, naphthalene (10), 21, 22, 23.
- Labels: "styrene (5)" from the text (Fig. 3 has no legend); "none (pristine AC)" and "naphthalene (10)" from the Fig. 4a legend; "21", "22", "23" from the Fig. 5a legend.
- Pristine AC coded as AC alone (Fig. 4 caption); the paper does not state whether CB/Pt was in this run.
- Organic-filled AC plus CB/Pt coded composite (Pt particles), metal_element Pt, loading not printed.
- Basis not named: basis_stated false, uptake_type unspecified, basis_inferred excess (volumetric, pressure-difference method). wt% convention unknown. The wt% basis (per mixture or per AC) is not stated.
- calibration_described true: text says dead volume was measured by evacuation before measurement (gas not stated).
- Discrepancy: SI Table S1 footnote gives the AC total pore volume as 1.59 cm3/g, Table 1 gives 0.89 cm3/g for pristine AC.
