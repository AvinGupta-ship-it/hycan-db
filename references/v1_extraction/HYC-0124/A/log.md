# HYC-0124 extractor A log

## Extracted from
- Text p.5 (journal p.25916): max excess 29 mmol/g (5.8 wt%) MSC30 and 23.8 mmol/g (4.8 wt%) MSP20X; pressure 4 MPa / 77 K from Conclusion (p.25923). 3 rows with the Sips-section 28 mmol/g (5.6 wt%) value (journal p.25919).
- Text p.7 (journal p.25919): Sips maximum nabs 37 mmol/g (7.4 wt%), MSC30 (fitted, absolute; T and P unstated). 1 row.
- Table 1 (journal p.25916): textural properties, put on every row of each sample (BET 3305/2363, NLDFT Vmicro 0.96/0.88, Vtot 1.60/0.93, Vmeso 0.64/0.05, Smicro 1708/1963, average micropore size 1.28/1.04, DR CO2 Vmicro 0.37/0.45; others in notes).
- Table 2 (journal p.25917): MDA nmax 72.46 / 47.38 mol/kg with rho_a 96.6 / 86.93 kg/m3. 2 rows (fitted_extrapolated, no single T/P).
- SI Table S1: nmax 74.94 / 47.68 mol/kg (Va variable). 2 rows.
- Fig. 2a/2b (PDF page main-06): all 77 K points that could be separated, adsorption and desorption; highest-pressure filled symbol at each other temperature. Archives in digitizations/. Calibration: a x 0 at px 265, 15 at 578, check 5 at 369.5; y 0 at 416.5, 30 at 162, check 15 at 289. b x 0 at 643, 15 at 955, check 5 at 747; y 0 at 416, 30 at 162, check 15 at 289. Tick residuals <= 0.4%.
- digitize_figure.py `check` run only for the two 77 K filled archives (at x = 3 MPa vs stated 29 and 23.8 mmol/g, 0.7% and 0.2%, PASS). The paper states no other value readable from Fig. 2, so the other archives remain status unchecked; their rows rest on the tick checks above.

## Digitization notes and markers not recovered
- 77 K, both panels: markers overlap heavily. Not separable and not extracted: the filled grey adsorption circle at about 5 MPa (hidden by open circles; ring at 5.0 MPa in both panels), filled circles at about 10-12.5 MPa in panel b (hidden by other symbols), and any filled marker at about 0.5 and 1 MPa (not visible). A filled marker clipped on the y axis (x -0.048 MPa, 6.37 mmol/g in a; 6.67 in b) is a calibration extrapolation (outside axis range) and is not a row. Isotherm_point_count 16 comes from the stated pressure steps, not from a visible marker count.
- 77 K desorption open circles (5 per panel) and the partly hidden filled circles are partial: open circles were located by ring template matching (rings.py in work), painted magenta in a work copy (painted_desorb.png) and read through the tool; archives name that source image. The 5.0 MPa open circle overlaps a second ring.
- Fig2a_MSC30_77K_adsorption_occluded.json holds 3 blobs; only the 7.771 MPa one is used (the others are fit-curve pixels). Fig2b_..._occluded.json and _occluded2.json each used for one point. 77K filled archive point at 13.870 MPa (b) not used; the 13.882 MPa occluded2 value is.
- Other temperatures: archives for 93 K (a), 173 K (a, b) contain curve pixels besides the marker; chosen blob documented in row notes. MSP20X 93 K: highest-pressure diamond is hidden behind the 77 K and 113 K symbols; no row. MSP20X 133 K square split in two blobs, weighted mean used. Several end-point markers are partly occluded (confidence 2).
- Other-temperature desorption points and lower-pressure adsorption points are not digitized (protocol).

## Values seen, not extracted
- Fig. 3b (nexc max vs temperature, mmol/g, five points per AC): figure is not an isotherm; the x-axis values (about 37-144 K) do not match the 77-153 K stated in the text, so not used. Fig. 3a (nexc wt% vs ABET): MSC30 5.8 and MSP20X 4.8 wt%, same as text; literature points (refs 43, 58-63) belong to other papers.
- Intro/Conclusion literature values: 6.4 wt% at 77 K and 4 MPa, micropore volume 0.87 cm3/g (ref 15); 66 kg/m3 adsorbed density at 77 K and 4 MPa (previous study, ref 74); upper limit 6.8 wt% (Fierro et al., ref 63); Schlapbach-Zuttel 34 mol/kg (6.8 wt%) for graphene 2630 m2/g; hypothetical maximum 42.96 and 30.72 mol/kg computed from ABET (computed from a literature constant, not this paper's measurement).
- Abstract "up to 5.8 wt%": same as the MSC30 maximum.
- Text: Sips nabs above nexc "103.8% and 102.4% at 273 K" (a difference, not an uptake); Qst, entropy, cp, Va, fugacity quantities (Figs 4-11, S2-S9) are not uptake values. Fig. S1, S2 (fits) not digitized (fits, not new data). Fig. 1 PSD, Fig. 4, 6 not uptake isotherms.
- Text says adsorption was completely reversible; no numeric uncertainty given for uptake (temperature control +/-0.005 K only), so replicates_reported false.
- No other material measured (no comparison or standard material).
