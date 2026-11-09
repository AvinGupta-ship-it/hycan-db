# HYC-0043 extraction log (agent B, 2026-11-09)

Ma et al. 2019, BioResources 14(4) 9755-9765. Input: 11 page images (main-01 to main-11), no SI. 82 rows written.

## Sources extracted from

- Abstract (p. 9755, main-01): "the highest hydrogen uptake reached 4.51 wt% at 77 K and 100 bar" for WC-ACHF-1.0% -> M81 (text_direct, no isotherm_id; see pressure conflict below).
- Methods (p. 9757, main-03): N2 sorption on ASAP 2020 at 77 K (surface area, porosity; t-plot micropores, BJH mesopores); H2 "0 to 100 bar and at 77 K using a high-pressure Automated Sievert's apparatus from Advanced Material Corporation" -> measurement_method volumetric_sieverts, instrument_identified false (no model), no degassing, sample mass, H2 purity or free-volume calibration stated; basis not named (basis_stated false, basis_inferred excess by the volumetric default).
- Text p. 9758-9759 (main-04/05): N contents of WC-ACHF-0%, -0.5%, -1.0%, -2.0%, -3.0% = 0%, 0.77%, 1.06%, 0.79%, 1.04% -> dopant_concentration_at_pct (taken as XPS at.%, since 1.06% equals the XPS at.% printed for WC-ACHF-1.0% in Fig. 2a).
- Fig. 2a inset table (p. 9759): WC-ACHF-1.0% C 91.26, N 1.06, O 7.34, P 0.35 at.% -> notes of S1 rows.
- Table 1 (p. 9759): C1s components for all five samples -> functional_groups only (percentages not stored).
- Text p. 9760 (main-06): WC-ACHF-1.0% specific surface area 1902 m2/g and total pore volume 0.860 cm3/g -> S1 rows (BET named in Fig. 3 inset legend and Fig. 4d axis; probe N2 from Methods; P/P0 range not stated).
- Text p. 9760: "ranging from 2.06 to 2.24 wt% at 77 K and 1 bar" -> 2.06 merged with the 1.007-bar point of Fig. 4a WC-ACHF-3.0% (M69); 2.24 as M80 (WC-ACHF-1.0%, no isotherm_id).
- Text p. 9760: "ranging from 4.08 to 4.51 wt% at 77 K and 100 bar" -> 4.51 = M81 (same value as Abstract); 4.08 = M82, assigned to WC-ACHF-0% (ACHF) via the Abstract's "approximately 10.5% more than that of ACHF" (4.51/1.105 = 4.08). Attribution uncertain: the Fig. 4b inset and Figs. 4c-e put WC-ACHF-3.0% at about the same value. Confidence 2.
- Text p. 9761 and Conclusions: PSD peaks (ACHF mainly 0.68 nm; WC-ACHFs two sets at 0.50 and 0.56 nm; WC-ACHF-1.0% "centered at 0.56 nm") -> average_pore_diameter_nm 0.68 (S2) and 0.56 (S1), pore_diameter_method unspecified.
- Fig. 4a (p. 9761, main-07; 77 K, 0-1 bar): digitized WC-ACHF-0.5% (I1, 17 rows), WC-ACHF-2.0% (I2, 25 rows), WC-ACHF-3.0% (I3, 26 digitized rows + merged text row M69).
- Fig. 4b (p. 9761, main-07; 77 K, "0 to 100 bar", axis ends at about 90 bar): digitized WC-ACHF-1.0% (I4, 10 rows).

## Sample numbering and labels

S1 WC-ACHF-1.0% (first named, Abstract), S2 WC-ACHF-0% (Abstract "ACHF"; also WA-0), S3 WC-ACHF-0.5%, S4 WC-ACHF-2.0%, S5 WC-ACHF-3.0% (order of the charcoal proportions in Experimental). Labels as in the Fig. 3/Fig. 4 legends (no table reports H2 uptake). Text variants: WC-ACHF-1%, WC-ACHF-3%, WA-x in insets.
material_class: doped_carbon for S1, S3-S5 (N 0.77-1.06 at.% and P built into the carbon from the liquefaction reagents, per XPS and the paper's "multiple heteroatoms (N, P)"); activated_carbon for S2 (N content printed as 0%; P not quantified for it). Note the paper also says XPS of "the prepared WC-ACHF samples" shows C, N, O and P, which contradicts N = 0% for WC-ACHF-0%. synthesis_method carbonization; steam activation in activation_method.
measuring_lab_id from corresponding author Jianing Li (first marked *), affiliation a (no university named).

## Digitization

- Tool: scripts/digitize_figure.py extract --mode markers, run on copies of main-07.png with the legend and inset whitened (work/page07_mask4a.png, work/page07_mask4b.png; pixel coordinates unchanged), because the legends repeat the series markers and the insets carry markers and lines inside the plot frames.
- Fig. 4a calibration: x 0.0 at px 351.25 (left frame, which carries the 0.0 tick), 1.0 at 615.47, check 0.6 at 509.52 (0.17%); y -0.5 at 768.51, 2.5 at 572.69, check 1.0 at 670.51 (0.14%).
- Fig. 4b calibration: x 0 at 704.45, 80 at 933.66, check 40 at 819.11 (0.05%); y -1 at 794.62 (bottom frame, which carries the -1 tick), 6 at 563.1 (top frame, carries the 6 tick), check 2 at 695.43 (0.05%).
- Archives (out/digitizations/): HYC-0043_fig4a_WC-ACHF-0.5.json (colour #6a1ebe, tol 60, 2-px opening), HYC-0043_fig4a_WC-ACHF-2.0.json (#30e6e0, tol 50, 3-px), HYC-0043_fig4a_WC-ACHF-3.0.json (#1414c8, tol 80, 3-px; check at 1 bar vs 2.06: pass), HYC-0043_fig4b_WC-ACHF-1.0.json (#d21ecd, tol 60, 3-px). The other three archives remain 'unchecked': the paper prints no value at a plotted pressure for those series (4.51 wt% is printed at 100 bar, beyond the plotted range).
- Parameters chosen from sweeps of colour tolerance and opening size as the run whose detections best matched the markers counted on enlarged crops (overlays in work/).
- The page image is low resolution (markers about 7-8 px, lines 2-3 px, several series overlapping), so marker centroids of partly covered markers are biased and confidence is 2-3.

## Marker counts and markers not separated

- Fig. 4a WC-ACHF-3.0% (blue): 29 markers counted, 28 tool blobs; two markers near 0.12 and 0.16 bar merged into one blob (centroid 0.1424 bar, 1.0568 wt%), not extracted. The 1.007-bar point is replaced by the text value 2.06 wt% (M69).
- Fig. 4a WC-ACHF-2.0% (cyan): 29 markers counted, 25 extracted; the 4 lowest-pressure markers (below about 0.15 bar) overlap the WC-ACHF-3.0% series and were not separated.
- Fig. 4a WC-ACHF-0.5% (violet): 19 markers visible (from about 0.38 bar), 17 extracted; 2 visible markers not separated; markers below about 0.38 bar hidden under the WC-ACHF-2.0% and -3.0% series (isotherm_point_count 19 counts visible markers only; the fully visible blue series has 29).
- Fig. 4a WC-ACHF-0% (black) and WC-ACHF-1.0% (magenta): completely hidden under the WC-ACHF-0.5% and WC-ACHF-2.0% series (no matching pixels); not digitized, no rows.
- Fig. 4b WC-ACHF-1.0% (magenta): 13 markers counted (12 visible plus the origin marker under the blue one), 10 extracted; the origin marker, the lowest-pressure visible marker and the highest-pressure marker were not separated in the chosen run (a trial run at tolerance 65 finds the last one at 79.07 bar but merges the two markers at the maximum and adds a spurious line blob).
- Fig. 4b WC-ACHF-0%, -0.5%, -2.0%, -3.0%: the four curves overlap into one thick band above about 10 bar and cross repeatedly below; across tolerances 40-110 and openings 2-5 the tool returned mostly line blobs rather than markers, so these four isotherms (about 13-14 markers each) are not digitized and have no rows. Trial outputs are in work/sw_4b_*.json.

## Values seen but not extracted

- Abstract: "increased approximately 10.5% more than that of ACHF" (relative comparison, not an uptake; used only to attribute 4.08 wt%).
- Conclusions (p. 9763): "hydrogen storage of 4.51 wt% at 298 K and 100 bar" for WC-ACHF-1.0%: same value as the Abstract's 77 K value, treated as the same measurement with a misprinted temperature (Methods state H2 at 77 K only); no separate 298 K row. Noted on M81.
- 4.51 and 4.08 wt% are printed "at 100 bar", but Fig. 4b's axis ends at about 90 bar and the isotherms peak near 28 bar and then fall; the printed values match the isotherm maxima, not points at 100 bar. Rows keep the printed pressure (100 bar) and say so in notes.
- p. 9760: "1.4 to 1.97wt% at 77 K and 1 bar" for activated carbons of Arshad et al. 2016 and Rambau et al. 2018 (other papers, not measured here).
- Fig. 4a inset (category plot of 1-bar uptake per sample, not an isotherm, not digitized): shows values for WA-0, WA-0.5 and WA-2 that the text does not give (text gives only the range ends).
- Fig. 4b inset (same, "100 bar"): shows values for WA-0.5 and WA-2, and separate values for WA-0 and WA-3, that the text does not give.
- Figs. 4c-e (uptake vs micropore volume, BET area, total pore volume, with linear fits R2 = 0.9933, 0.7400, 0.877): not isotherms, not digitized; show the "100 bar" uptakes of the four WC-ACHFs (including WA-0.5 and WA-2, not given in text) against their micropore volumes, BET areas and total pore volumes (not given in text except WC-ACHF-1.0% area and total volume).
- Fig. 3 inset (bar chart): BET area, total pore volume and micropore volume of all five samples; not digitized. Only WC-ACHF-1.0% area and total volume are printed in the text; the micropore volumes of all samples and the areas and total volumes of WC-ACHF-0%, -0.5%, -2.0%, -3.0% are not given in text (those rows carry surface_area_method = not_reported).
- Fig. 3 PSD curves: not digitized (not uptake); peak positions taken from the text.
- Fig. 2b-d, Table 1: XPS binding energies and component fractions (characterization only).
- CO2 uptakes (Abstract, Fig. 5, p. 9762, Conclusions: 4.76, 4.80, 7.13, 3.93, 4.36 mmol/g; 20.97, 21.12, 31.35, 17.28, 19.20 wt%; 7.13 "mol g-1" in Conclusions; literature 5.8 mmol/g): not H2, not extracted. Figs. 5c-d (CO2 vs BET area and total pore volume) not extracted.
- Text "hydrogen adsorption was entirely reversible": no desorption branch is plotted, so all rows are adsorption.
- No non-carbon sorbent measured; the commercial wood charcoal powder is a precursor additive, not a measured sorbent.
