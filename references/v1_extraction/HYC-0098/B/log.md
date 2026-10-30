# HYC-0098 extraction log (agent B)

Zhao et al. 2017, BioResources 12(1) 1246-1262. Input: page images main-01.png to main-17.png (no SI). 162 rows: 12 table values, each merged with a plotted point, plus 150 digitized markers.

## Sources extracted

- main-09.png (p. 1254), Table 2: 12 H2 uptake values (wt%, 77 K) at "1 bar" and "4 MPa" for BC, AC2, AC3, AC4, AC5 and AC6, plus S_BET, V0.99, V_DR, Ea, L0, V_DR/V0.99 and V_meso. Each 1-bar value is merged with the highest-pressure marker of that sample's Fig. 9a isotherm (about 752 mmHg = 1.003 bar, within 0.02 bar). Each 4-MPa value is merged with the Fig. 9b marker nearest 4 MPa (3.89 to 3.94 MPa). The text on p. 1255 says the Fig. 9 isotherms' capacities "are listed in Table 2". That statement covers AC5 (38.92 bar, just outside the 2% window) and fixes the choice of the closest marker.
- main-12.png (p. 1257), Fig. 9a: 77 K isotherms up to 1 bar (ASAP 2020 HD88), six series, every separable marker digitized (115 markers including the six merged with Table 2).
- main-12.png (p. 1257), Fig. 9b: 77 K isotherms up to 8 MPa (HPVA-100), six series, every separable single marker digitized (47 markers including the six merged with Table 2).
- main-01.png abstract, main-10.png text p. 1255, main-13.png Table 3 rows "Bamboo / This work", main-14.png Conclusion 3: these repeat the Table 2 values. "0.86 wt.% up to 1 bar and 1.2 wt.% up to 8 MPa" (BC), "2.74 wt.% up to 1 bar and 6.6 wt.% up to 8 MPa" (best ACs), and Table 3's 77 K / 40 bar / 6.60 and 77 K / 1 bar / 2.74 are recorded in the source_location and notes of the matching Table 2 rows, not as separate rows.
- main-04.png (p. 1249), "Measurement of the Hydrogen Storage Capacities at 77 K": instruments and degassing (350 C, 24 h, primary vacuum).
- main-03.png (p. 1248) and main-04.png: N2 physisorption methods (ASAP 2020, 77 K, degassed 24 h at 563 K, BET, DR, V0.99, Stoeckli L0, DFT).
- main-02.png and main-03.png: synthesis of BC and the ACs.
- main-06.png (p. 1251), Table 1, and main-05.png (p. 1250), XPS text: composition of BC and AC5, recorded in notes.

## Calibration

- Fig. 9a (main-12.png pixels). x: 0 mmHg at 435.5, 800 mmHg at 870.3, check tick 400 at 652.55 (residual 0.16%). y: 0 wt% at 575.0, 3.0 wt% at 211.0, check tick 1.5 at 392.62 (residual 0.21%).
- Fig. 9b. x: 0 MPa at 442.59, 9 MPa at 909.0, check tick 4 at 649.39. y: 0 wt% at 1088.62, 7 wt% at 742.73, check tick 3 at 940.59. Both checks passed within the tool's verify tolerance.
- Tick pixel positions were found from dark-pixel rows and columns, with sub-pixel weighting.

## Archives (out/digitizations/)

Black series share their colour with each other and with the text labels inside the plot, so they were digitized over several rectangular regions, one archive per region. Every archive uses the same calibration.

- Fig. 9a: fig9a_AC3_blue (21), fig9a_AC2_red (18), fig9a_AC4_magenta (20), fig9a_AC5_green (15), fig9a_AC6_black_part1 to part4 (1+2+14+3 = 20), fig9a_BC_black_part1 and part2 (2+19 = 21). Every archived Fig. 9a point is written as a row.
- Fig. 9b: fig9b_AC2_red (12), fig9b_AC3_blue (12), fig9b_AC4_magenta_part1 and part2 (6+3; the line fragment at about 4.45 MPa falls between the two regions), fig9b_AC5_green (12), fig9b_AC6_black_part1 and part2 (10+2), fig9b_BC_black (10). The archived components below are not written as rows because each one holds more than one marker or sits at a location that does:
  - AC2: (0.266 MPa, 2.082 wt%, 87 px), (0.403, 2.465, 85 px), (0.669, 2.922, 94 px), (1.367, 3.573, 73 px). Each is two overlapping circles (a single circle is 45 to 52 px).
  - AC3: (0.271, 3.465, 73 px), (0.405, 3.844, 78 px), (0.668, 4.317, 77 px), (1.372, 4.972, 66 px). Each is two overlapping triangles (a single triangle is 37 to 49 px).
  - AC6: (0.262, 3.999, 53 px), (0.402, 4.450, 36 px), (0.673, 4.955, 42 px), (1.369, 5.646, 42 px). Each is two overlapping stars (a single star is 15 to 26 px).
  - BC: (0.347, 0.099, 80 px), a merged cluster of at least three pentagons resting on the x axis between about 0.09 and 0.47 MPa; (0.668, 0.222, 78 px) and (1.369, 0.524, 68 px), each two overlapping pentagons.
  - AC5: (0.244, 4.164), (0.398, 4.586), (0.670, 5.102), (1.332, 5.776). These are partial green triangles at the overlapping-pair locations, mostly hidden under the AC6 stars, and the two markers of each pair cannot be told apart.
  - AC4: (0.271, 4.270, 13 px), a fragment of a magenta diamond at the 0.27 MPa pair location.

## Markers counted but not separable (not extracted)

- Fig. 9a. Every series follows the same 21-step pressure schedule; all 21 markers are visible for AC3 and BC. The data point at the origin is clipped by the axes and not counted. Hidden markers:
  - AC2: about 15, 38 and 85 mmHg, behind the AC3, AC4, AC5 and AC6 markers. At 15 mmHg only 6 red pixels remain.
  - AC4: about 15 mmHg.
  - AC5: about 15, 230, 270, 305, 343 and 380 mmHg, covered by the AC6 stars.
  - AC6: about 15 mmHg, under the BC pentagon. The BC 15 mmHg component includes a few of that star's pixels; its confidence is lowered to 2.
- Fig. 9b. Each sample shows 16 markers: one near 0.13 MPa, overlapping pairs near 0.27, 0.40, 0.67 and 1.37 MPa, and seven singles at about 2.57, 2.76, 3.92, 4.14, 5.21, 6.84 and 7.95 MPa. The count comes from AC2 and AC3, where all markers are visible. The eight pair markers are not separable for any sample. Further markers not separable:
  - BC: the 0.13 MPa marker, inside the axis cluster.
  - Every AC4 diamond in Fig. 9b, including the one at 5.21 MPa (9 px visible), shows only its lower part below the AC6 stars. They are extracted, and all AC4 Fig. 9b rows are flagged partial (confidence 2).
- Partly hidden markers that were extracted are flagged in notes with confidence 2: AC4 at 35 and 82 mmHg (Fig. 9a), AC5 from 82 to 571 mmHg (Fig. 9a), the AC3 0.16 MPa triangle (Fig. 9b), all AC4 markers in Fig. 9b and all AC5 markers in Fig. 9b.

## Digitizer check step

The extraction instruction does not include a `check` step; it was run anyway against the Table 2 values (5% tolerance).

- Passed: Fig. 9a AC3, AC4, AC5 and BC; Fig. 9b AC2, AC3, AC4, AC5 and AC6.
- Failed:
  - Fig. 9a AC2 at 750.06 mmHg: expected 2.20, got 1.981 (9.95%).
  - Fig. 9a AC6 (part4) at 750.06 mmHg: expected 2.50, got 2.627 (5.08%).
  - Fig. 9b BC at 4.0 MPa: expected 1.2, got 1.109 (7.58%).
- The calibration passes its third-tick checks and the other series on the same axes pass. The failures therefore reflect disagreement between Table 2 and Fig. 9 in the paper, not a digitization error.
- The tool marked those three archives "discarded". Copies of the discarded archives, with their failed-check records, are kept in work/discarded_checks/.
- The three series were then re-extracted with identical calibration and parameters (status "unchecked") so their markers could be archived and written. This follows the v1 rule: the printed value goes in the row and the digitized value goes in notes. The discrepancy is stated in the notes of rows M154 (AC2, +10.9%), M99 (AC6, -5.0%) and M24 (BC, +9.8%).

## Interpretation decisions

- **Sample numbering, by first appearance.** BC (abstract) S1; AC4 (p. 1248, nomenclature example) S2; AC5 (Fig. 2) S3; then AC6, AC3 and AC2 in the top-to-bottom order of the Fig. 6 labels (p. 1253): S4, S5, S6.
- **Fig. 9 caption swap.** The caption says "(a) at 77 K and up to 8 MPa, and (b) at 77 K and up to 1 bar". The axes (mmHg up to 800 in (a), MPa up to 9 in (b)) and the text (p. 1255: "up to 1 bar ... Fig. 9a", "8 MPa ... Fig. 9b") show the caption is swapped. Panels are used as the axes show.
- **Curve-to-sample mapping in Fig. 9.** Mapping is by marker colour, consistent with the Fig. 7 and Fig. 8 legends: AC2 red, AC3 blue, AC4 magenta, AC5 green, AC6 black stars, BC black pentagons. The Fig. 9 text labels have no leader lines. In Fig. 9a the "AC5" label sits by the black-star curve end and "AC6" by the green; in Fig. 9b "AC4" sits by the star end and "AC6" below the magenta. These suggest the opposite assignment.
  - By colour: AC5 green ends at 2.577 (Table 2: 2.58), and AC6 black star ends at 2.630 (Table 2: 2.50).
  - Under the label positions instead: AC5 would be 2.630 (+1.9%) and AC6 2.577 (+3.1%).
  - The reconciler should check this mapping.
- **HPVA-100.** The paper calls it a "gravimetric analyzer (VTI Corporation of TA Instruments)". Coded gravimetric_microbalance as printed. No buoyancy correction is stated, so basis_inferred is unknown. The ASAP 2020 HD88 low-pressure data are coded volumetric_sieverts from the instrument (the paper names no method), so their basis_inferred is excess. The paper never names excess, absolute or total: basis_stated false, uptake_type unspecified.
- **Branches in Fig. 9b.** Each sample shows two nearly coincident plotted lines, and the text says "There was no hysteresis cycle". No marker identifies the desorption points, so all points are coded adsorption, one isotherm per sample. This assumes the two lines are adsorption and desorption of one run; the paper does not say they are separate runs, so replicates_reported is false.
- **Table 2 "4 MPa" column against the text.** The text (p. 1255) calls the BC 1.2 wt% and the AC 6.6 wt% values the maximum "up to 8 MPa", and the abstract gives 6.6 "at 4 MPa". The Table 2 values lie closer to each isotherm's plateau maximum (BC about 1.17, AC2 about 4.36) than to the marker at 3.92 MPa (BC 1.09, AC2 4.31). The rows keep the printed pressure (40 bar) and value.
- **Table 3 "Bamboo / This work".** It pairs 3208 m2/g (AC5's S_BET) with both 6.60 wt% (AC5, 40 bar) and 2.74 wt% (AC3's 1-bar value; AC3 S_BET 2559).
- **measuring_lab_id.** "Fan group, Brunel University". The asterisk marks Mizi Fan (affiliation c, Brunel University), although the printed corresponding-author e-mail is weigang-zhao@hotmail.com (first author, Fujian Agriculture and Forestry University). No separate H2 laboratory is named.
- **Classes.**
  - BC is a non-activated bamboo char (carbonized at 650 C): material_class other.
  - The ACs are activated_carbon.
  - synthesis_method is carbonization for all, because the raw carbon is the carbonized bamboo; KOH activation goes in activation_method and the washing in purification_method.
- **Characterization.**
  - BC Table 2 entries printed "N" are left empty.
  - V0.99 is stored as total pore volume. For BC, pore_volume_method is "other" (single point at P/P0 = 0.99); for the ACs it is DR (V_DR).
  - L0 is stored as average_pore_diameter_nm with stoeckli_L0.
  - area_same_sample is yes: the same samples were measured, after 24 h outgassing at 563 K for N2 and at 350 C for H2.
  - No BET P/P0 range or consistency criteria are stated.

## Values seen but not extracted

- **Table 3 (p. 1258).** Literature values for other carbons, measured in other papers, not this work: empty fruit bunch (77 K 1 bar 1.97 wt%, 20 bar 2.14 wt%, 687 m2/g; Arshad et al. 2016); anthracites (40 bar 6.6, 3220; Zhao et al. 2014); rice husk (1 bar 2.72, 3044; Heo and Park 2015); chitosan (40 bar 5.6, 3100; Wrobel-Iwaniec et al. 2015); corncob (40 bar 5.8, 3708; Wang et al. 2014); activated carbon aerogels (20 bar 4.3, 1980; Robertson et al. 2013); fungi (1 bar 2.4, 2500; Wang et al. 2014); activated carbon xerogels (11 bar 4.3, 2204; Zhang et al. 2012).
- **Maxsorb-3** (commercial activated carbon, p. 1256). Surface area 3203 m2/g and a PSD in Fig. 10. The paper prints no H2 uptake value for it; it says only that the bamboo ACs were "much higher". No row.
- **Raw bamboo** (not a carbon sorbent). Table 1: N <0.3, C 46.12, O 33.22, H 6.29, S <0.5 wt%. FTIR in Fig. 4. No H2 uptake, no row.
- **Figures not digitized.**
  - Fig. 2: TG; carbonization yield 24.3%, activation yield 69.8%, total AC5 yield about 17%.
  - Fig. 3: XPS spectra.
  - Fig. 4: FTIR.
  - Fig. 5: SEM/HRTEM.
  - Fig. 6: XRD; BC broad peaks near 2 theta = 24 and 44 deg.
  - Fig. 7: N2 isotherms.
  - Figs. 8 and 10: DFT pore size distributions.
  - None shows H2 uptake.
- No values in other units (mmol/g, cm3/g), no volumetric capacities, no uncertainties and no sample masses or H2 purity are given.
