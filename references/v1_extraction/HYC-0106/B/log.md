# HYC-0106 extraction log (agent B)

Paper: Lionetti et al. 2025, Int. J. Hydrogen Energy 136, 1029-1040, "Optimized activation of coffee-ground carbons for hydrogen storage". Input: page images main-01..12, si1-01..15 (no text layer). Rows written: 286.

## Sources extracted

- Table 1 (main p. 1031, main-03.png): sample list, precursor, activation type/agent, yield; used for sample identity and descriptions (yields in notes).
- Section 2.1-2.2 text (main p. 1030-1031): synthesis, N2 porosimetry (ASAP 2460, degas 473 K 12 h, P <= 1e-5 mbar, BET p/p0 0.01-0.30, NLDFT, VT at p/p0 0.995), H2 at <= 1 bar on ASAP 2460 (pretreatment 473 K, P <= 1e-5 mbar), HPVA II up to 70 bar at 298 K and 77 K (degassed at 473 K), He pycnometry, Toth model, wt% definition.
- Table 2 (main p. 1033, main-05.png): SBET, Vultra, Vsuper, Vmicro, Vmeso, VT, %micro for the six ACs; carried on every row of each sample (Vsuper and %micro in notes).
- Table 3 (main p. 1035, main-07.png): H2 uptake at 1 bar and 77 K for six samples (1.60, 1.34, 2.65, 2.11, 1.76, 1.51 wt%); each merged with the plotted p/p0 = 1 point (Fig. 5 full marker; for CG_N2+CO2 the Fig. 6a open marker, see below).
- Text p. 1037 (main-09.png) "experimental maximum amount of hydrogen adsorbed is 3.66 wt% at 77 K and 70 bar" (also abstract, conclusions, Tables S7-S9): one row, merged with the Fig. 8a adsorption marker at ~70 bar.
- Table 4 (main p. 1037): Toth wt%max = 3.73 +/- 0.05 wt% at 77 K: one row (fitted_extrapolated, no pressure); K = 1.42 +/- 0.25 and t = 0.89 +/- 0.09 are not uptakes (in notes). Caption says "RT and 77 K" but only a 77 K row is printed.
- Text p. 1037: skeletal density 2.18 g/cm3 (He pycnometry) for CG_PC_KOH: on all CG_PC_KOH rows.
- Table S8 (SI p. 9, si1-09.png): 298 K, 70 bar, 0.50 wt% for CG_PC_KOH: one row, merged with the Fig. 9a adsorption marker at ~70 bar. Its 77 K entries for this work repeat Table 3 and the 3.66 text value (same measurements, not separate rows).
- Table S7 (SI p. 8): "this work" average pore size 1.47 nm for CG_PC_KOH (method not stated): stored as average_pore_diameter_nm.
- Tables S1-S6 (SI p. 3-6): EDX composition (wt% and at%) of each AC: in notes (no deliberate dopant or metal; N in CG_N2+CO2 and K/Mg/Ca/P/Al/Si are precursor residues).
- Fig. 5 (main p. 1035): full markers of CG_CO2, CG_PC_KOH, CG_KOH, CG_PC_DA, CG_DA digitized (archives fig5_*.json) as the adsorption branches.
- Fig. 6a-f (main p. 1036, main-08.png): full markers (adsorption) and open markers (desorption) digitized per panel (fig6*_filled.json, fig6*_hollow.json).
- Fig. 8a (main p. 1038, main-10.png): 9 adsorption and 8 desorption markers of CG_PC_KOH at 77 K up to 70 bar (fig8a_filled.json, fig8a_hollow.json).
- Fig. 8c (main p. 1038): separable single markers of the cycle isotherms (fig8c_filled.json).
- Fig. 9a (main p. 1038): only the highest-pressure point (non-77 K isotherm), merged with Table S8 (fig9a_ads70.json).
- Fig. 9b (main p. 1038): highest-pressure points of the 1st and 3rd cycles (fig9b_filled.json).
- Fig. S7 (SI p. 7, si1-07.png): 77 K panel digitized as a separate run (figS7_77K.json); 273 K and 300 K panels: highest-pressure visible point each (figS7_273K.json, figS7_300K.json).

## Coding decisions applied to all rows

- Basis: the paper never names excess/absolute/total; uptake_type unspecified, basis_stated false, basis_inferred excess (volumetric default; ASAP 2460 and HPVA II are volumetric).
- wt% convention: W1 stated, from "The H2 uptake of the ACs was expressed in wt% (weight percent of adsorbed gas per gram of adsorbent)" (p. 1031); applied to every row as the paper's single definition of its wt% unit.
- Pressure for Fig. 5, 6 and S7: the x axis is relative pressure p/p0 and p0 is not printed. The paper states the H2 isotherms were collected up to 1 bar and Table 3 gives the p/p0 = 1 values as "1 bar", so pressure_bar = p/p0 x 1 bar (assumption recorded in every such row).
- Temperatures: 77 K printed (not inferred); RT = 298 K (text p. 1031/1038); S7 panels 273 K and 300 K as printed.
- Laboratory: corresponding author Lionetti (marked *), first affiliation Università Della Calabria -> "Lionetti group, Università Della Calabria".
- Degassing: ASAP H2 rows 473 K (199.85 C), end pressure <= 1e-5 mbar stored as 0.001 Pa, duration not stated for H2 (12 h is stated only for N2 porosimetry). HPVA rows 473 K, no duration/pressure; the cycles run without heating (Fig. 8c/9b 2nd, 3rd, 5th, 6th) carry no degas values.
- calibration_described: true for HPVA rows (He pycnometry in the HPVA for the skeletal volume, "crucial for evaluating the storage capacity"), false for ASAP rows (nothing stated). instrument_identified true for both (manufacturer and model named).
- replicates_reported: true for CG_PC_KOH 77 K low-pressure isotherms (Fig. 5/6c and the separate Fig. S7 77 K run), all HPVA cycle isotherms (77 K and RT) and the Toth row (+/- 0.05); false for the other five samples and for the single 273 K and 300 K runs.
- Synthesis: CG_N2+CO2 pyrolysis; CG_CO2 physical_activation (carbonization and activation simultaneous under CO2); CG_PC_KOH and CG_PC_DA carbonization (pre-carbonization to CG_PC); CG_KOH and CG_DA chemical_activation (KOH on raw CG forms the carbon). All material_class activated_carbon.
- Samples numbered S1-S6 in Table 1 order. The precursors CG (raw spent coffee grounds) and CG_PC (biochar) have characterization (TGA Fig. 1/S1: ash about 3 %/3.2 %, char residue 27.4 %; EDX carbon content of CG 68 +/- 9 %; SEM Fig. S5) but no H2 uptake: no rows, no sample_id.

## Digitization method

- Every axis calibrated on the lowest and highest labelled ticks with a third labelled tick as check (all checks < 0.6 % relative error, recorded in each archive). Tick positions found from pixel rows/columns. In Fig. 5 and 6 the y ticks 0 and 3.5, in Fig. 8a-c the y ticks 0 and 4.5, in Fig. 9 the y tick 1.6 and x tick 0 coincide with frame lines: their positions were taken as the sub-pixel centres of those frame lines, consistent with the inner tick spacing within 0.5 px.
- Fig. S7: the x tick 0.0 is hidden by markers in all three panels, so x was calibrated on the 0.2 and 0.8 ticks (lowest and highest unobscured labelled ticks), verified on 0.4.
- Working images (in the work directory): legends and in-plot labels painted white (fig5_clean.png, fig6_clean.png, fig89_clean.png, figS7_clean.png); for open markers, images in which the white interior of each closed open-marker outline is painted cyan (fig6_holes_*.png, fig8a_holes.png, fig9a_holes.png), digitized with the tool as markers (open-marker position = centroid of its interior); in Fig. S7 the red Toth line crossing each black marker was bridged with black only where it lies inside a marker (figS7_bridged.png). Archives reference these images by path and sha256.
- Two white pockets enclosed by the frame, a tick and a marker were excluded from the open-marker images (Fig. 6a at px 151.9/487.3, Fig. 6e at px 153.5/1306.5); they are not markers.
- Fig. 5 vs Fig. 6: Fig. 6 open (DES) markers have opaque white interiors and hide adsorption markers at the same position; Fig. 5 shows the complete adsorption branches. Adsorption points were taken from Fig. 5 when the marker is whole there, otherwise from Fig. 6; a marker partly hidden in both (40-70 % of a full marker) was extracted with confidence 2 and a note; less than 40 % visible, not extracted.
- Marker counts: Fig. 6 open markers 19 per panel, all extracted (CG_N2+CO2: 18 rows plus the p/p0 = 1 marker merged with Table 3). Adsorption markers: 20 per sample at p/p0 >= 0.03 (all extracted except 2 CG_CO2 markers at p/p0 ~0.33 and ~0.40 hidden in both figures and 3 CG_N2+CO2 markers at ~0.185, ~0.265 and ~1.0 hidden under open markers in Fig. 6a), plus about 5 (CG_PC_KOH about 6) per sample in the overlapping low-pressure cluster (p/p0 < 0.03), of which only isolated ones were extracted. isotherm_point_count is therefore approximate (44; 45 for CG_PC_KOH).
- The digitizer check (tool `check`) passed against stated values for fig5_CO2/PCKOH/KOH/PCDA/DA and fig6a_hollow (Table 3 at p/p0 = 1), fig8a_filled (3.66 at 70 bar) and fig9a_ads70 (0.50 at 70 bar); the other archives have no stated value to check against and remain "unchecked".

## Discrepancies found in the paper

- Fig. 5 black series (legend CG_N2+CO2) coincides point by point with the CG_CO2 desorption branch of Fig. 6b (e.g. 0.5066/1.1945 vs 0.5068/1.1949; 0.8987/1.3220 vs 0.8995/1.3242 p/p0/wt%) and reaches only ~1.34 wt% at p/p0 = 1, against 1.60 wt% in Table 3 and Fig. 6a. Treated as a plotting error and not extracted (archive fig5_N2CO2.json kept for reference). CG_N2+CO2 adsorption is from Fig. 6a only.
- Fig. 8a: the text says it is the first cycle, but its points coincide with the Fig. 8c 4th-cycle (down-triangle) markers (1 bar 2.238 vs 2.241; 70 bar 3.655 vs 3.664 wt%), not the 1st-cycle circles (2.361; 3.563 wt%). Fig. 8a and the 8c down-triangles were treated as one run (8c down-triangles not extracted again); the 8c circles were extracted as a separate run (I8).
- Table S7 gives "0.5 at 1 bar and 298 K"; Tables S8/S9, the main text and Fig. 9a give ~0.5 wt% at 70 bar (Fig. 9a uptake at ~1 bar is about 0.004 wt%). Treated as a typo; no separate row.
- Fig. 3b ultramicropore bar for CG_CO2 (~0.32 cm3/g) disagrees with Table 2 (0.241 cm3/g, which also sums with Vsuper 0.050 to Vmicro 0.291); Table 2 used.
- Fig. 9a (RT, ads+des) is not the same plotted data as the Fig. 9b 1st cycle (70 bar: ~0.50 vs 0.368 wt%); treated as separate runs (no statement in the paper).
- Fig. S7 77 K panel coincides with the Fig. 5/6c adsorption points up to p/p0 0.66 but has points at 0.72 and 0.79 that Fig. 5 lacks (Fig. 5: 0.744, 0.811); treated as a separate run (I16). The SI figure is cropped at p/p0 ~0.82.

## Values seen but not extracted

- Table 3 values are also printed in Table S8 (77 K, 1 bar, all six samples) and, for CG_PC_KOH, in Tables S7 and S9 and the abstract/conclusions: same measurements, one row each.
- 3.66 wt% (77 K, 70 bar) also in abstract, conclusions, Tables S7, S8, S9: same measurement.
- 0.50 wt% (298 K, 70 bar) also in Table S9 and main text p. 1038 ("around 0.5 wt%"): same measurement.
- Table S8 H2/SBET x 1000 ratios (1.58, 2.18, 0.30, 1.39, 1.58, 1.77, 1.36, 1.10 for this work): derived quantities, not uptakes.
- Table S7 literature entries (refs [3]-[12]): coffee-ground ACs from other papers, e.g. 1.75 wt% at 1 bar 77 K [3]; 0.6 wt% at 120 bar 298 K and 4.0 wt% at 40 bar 77 K [9]; 5.79 wt% at 37 bar 77 K and 9 wt% at 100 bar 77 K [12]; with their SBET/TPV/pore data: cited values, not measured in this paper.
- Table S8 literature entries: walnut shells 1.69 (77 K, 1 bar), 2.62 (77 K, 80 bar), 0.12 (298 K, 80 bar) [13]; lemon peel 0.93 [14]; pinecone 1.57 and 5.25 [15]; Posidonia oceanica 6.3 and wood chips 6.3 (77 K, 80 bar) [16]; peach pit 1.85 [17]; empty fruit bunch 1.97 (1 bar) and 2.14 (20 bar) [18]; bark/Camellia shell 3.01 [19]; orange peels 3.3 (10 bar) [20]; oil-palm shell 2.86 [21]; all cited from other papers.
- Table S9 benchmark materials: metal hydrides Mg2NiH4 3.59, LaNi5H6 1.37, ZrMn2H2 1.77, FeTiH2 1.89, MgH2 7.6 wt% [22] (not carbon, cited); MOFs MOF-5 1.90, UiO-66 1.50, MOF-74(Zn) 2.16, Co14Zn86-MOF-74 3.08, MOF-177 7.5 wt% [23,24] (not carbon, cited); ACs AC-23 0.66 (298 K, 100 bar) [25], AC-HIC 1.35 [26], Maxsorb-3 6 (77 K, 20 bar) [27], Filtercarb GCC 8x30 2.19 and PHA 2.55 (77 K, 20 bar) [28] (cited); CG_PC_KOH entries repeat rows.
- Fig. 7: isosteric heat vs uptake for CG_PC_KOH, average 9.01 kJ/mol: not an isotherm, no uptake value beyond the axis.
- Fig. 2a: N2 isotherms at 77 K (not H2); Fig. 2b: NLDFT PSD waterfall: characterization only.
- Fig. 3a/b: pore-volume histograms repeating Table 2 (see discrepancy above).
- Fig. 1 and Fig. S1: TGA/DTG of the CG precursor (peaks 350.17, 487.45, 566.62, 594.82, 649.14 K in N2; 335.36, 480.36, 562.20, 695.42, 772.81, 793.29 K in air; residue 27.4 % in N2, ash ~3.2 % in air): precursor characterization, no H2 uptake.
- Fig. 4 and Figs. S2-S5: SEM (Fig. S2-S5 images are not rendered in the SI page images): no values.
- Fig. S6: correlation of maximum 77 K uptake with SBET, Vmicro, Vultra; the figure is not rendered in the SI page image; text gives R2 = 0.72 (Vmicro), 0.78 (Vultra), 0.71 (SBET): not uptakes.
- Text "average SBET value of about 1270 m2/g" (mean over samples) and the Chahine-rule statement: not uptake rows.
- Fig. 8b: same adsorption markers as Fig. 8a (digitized as a cross-check, fig8b_filled.json, matches within 0.15 bar and 0.005 wt%, except 0.31 bar for the partly covered 70-bar marker of Fig. 8a) plus the Toth fit line (a model curve, not data; parameters in Table 4): not extracted again.
- Fig. 8c not extracted (markers overlap; cycle shape not separable at 150 dpi): at ~0.05 bar one blob of all six cycles (~0.50-0.65 wt%); at ~1 bar the 2nd, 3rd, 5th, 6th cycle markers merged (~1.88 wt%); at ~5 bar 1st+4th merged (~3.02) and 2nd/3rd/5th/6th merged (~2.49); at 20 and 30 bar 1st+4th merged (~3.50, ~3.58) and 2nd/3rd/5th/6th merged (~2.98, ~3.06); at 40 bar 1st+4th merged (~3.60) and 2nd+5th merged (~3.05); at 50 and 60 bar 1st+4th merged (~3.61); at 70 bar 5th+6th merged (~3.14). 4th-cycle (down-triangle) markers: same run as Fig. 8a, not extracted again. Each cycle has 9 markers (isotherm_point_count 9).
- Fig. 9a: all points except the highest-pressure adsorption point (non-77 K isotherm): 8 further adsorption markers (0.7-60 bar) and 8 desorption markers (4-70 bar, highest 69.93 bar 0.4889 wt%), digitized in fig9a_filled.json / fig9a_hollow.json for reference only.
- Fig. 9b: highest-pressure (70 bar) markers of the 2nd, 4th, 5th and 6th cycles overlap in one blob (~0.487 wt%) and behind the 3rd-cycle marker: not separable; lower-pressure points not extracted (non-77 K isotherms).
- Fig. S7 77 K panel: merged low-pressure cluster (~4 markers, p/p0 < 0.02) and the two merged markers at p/p0 ~0.085 and ~0.10 (blob at 0.094, 1.42 wt%): not separable. 273 K and 300 K panels: all points below the highest visible one (non-77 K isotherms); further points beyond p/p0 0.82 are cropped out of the SI image. Toth fit lines: model curves.
- Low-pressure adsorption markers not extracted (Fig. 5/6, p/p0 < 0.03): CG_N2+CO2 Fig. 6a marker at p/p0 -0.0008, 0.067 wt% (on the axis origin, pressure not resolvable); CG_CO2 Fig. 6b blob at 0.0015/0.087 (about 3 merged markers) and Fig. 5 marker at 0.0058/0.32 (mostly hidden); CG_PC_KOH Fig. 6c blob at 0.0005/0.115 (about 3 merged markers) and Fig. 5 markers at ~0.001/0.48 and ~0.35 wt% (mostly hidden); CG_KOH low-pressure adsorption markers hidden under Fig. 6d open markers and Fig. 5 markers of other series (one partly visible below the lowest open marker, ~0.10 wt%); CG_PC_DA markers hidden under Fig. 6e open markers (~0.13-0.25 wt%); CG_DA Fig. 5 blob at 0.0051/0.14 (about 5 merged markers) and Fig. 6f marker at p/p0 -0.0007, 0.022 wt% (on the axis origin).
