# HYC-0007 extraction log (extractor B, 2026-11-09)

Input: page images main-1.png to main-5.png (journal pp. 143-147), no supplementary file. 159 rows written; 7 carbon samples (S1 SWCNT, S2 A-SWCNT, S3 ACF-1000, S4 ACF-1400, S5 ACF-1800, S6 ACF-2300, S7 O-ACF-1000); 14 isotherms (I1-I14).

## Sources extracted from

- Abstract and Section 1 (main p.1, journal p.143): sample list and pressure range only; no uptake value of this paper beyond those repeated in Section 3.
- Section 2.1 (main p.2, journal p.144): sample preparation (HiPco SWCNT from Carbon Nanotechnologies Inc.; A-SWCNT treatment; four phenolic-resin ACFs; O-ACF-1000 oxidation), N2 alpha_s-plot characterization at 77 K.
- Section 2.2 (main p.2): 77 K isotherms on BELSORP 28SA (BEL Japan) up to 0.1 MPa after 393 K / 1 Pa / 12 h; H2 purity 99.99999%; 303 K isotherms on the authors' manually controlled high-pressure apparatus (303 +/- 0.1 K thermostat, 30 min equilibration, about 1.0 g sample, cell heated at 393 K for 24 h). Coded on every row.
- Table 1 (main p.2, journal p.144): S_micro, S_ext, V_micro, W_ave for the seven carbon samples, put on every row of each sample (micropore_surface_area, external_surface_area, micropore_volume, average_pore_diameter; method alpha_s_plot, N2; no total or BET area is reported, so bet_surface_area is empty).
- Section 3 text (main p.3, journal p.145), 4 values: SWCNT 0.8 wt% at 0.1 MPa (77 K) -> M25, own row, no isotherm_id; A-SWCNT 1.8 wt% at 0.1 MPa (77 K) -> M52, merged with a Fig. 2a point; ACF-2300 2.3 wt% at 0.1 MPa (77 K) -> M126, own row, no isotherm_id; ACF-2300 0.26 wt% at 303 K and 3.1 MPa -> M127, merged with the Fig. 3b highest-pressure point.
- Fig. 2a (main p.3, journal p.145, 77 K, filled = adsorption, open = desorption): A-SWCNT 26 markers (17 ads, 9 des) -> I3 (25 digitized rows + merged text row M52); SWCNT 24 markers (16 ads, 8 des) -> I1 (24 digitized rows).
- Fig. 2b (main p.3, journal p.145, 77 K): ACF-1000 23 markers -> I5; ACF-1400 23 -> I7; ACF-1800 11 -> I9; ACF-2300 12 -> I11; O-ACF-1000 31 -> I13.
- Fig. 3a / 3b (main p.4, journal p.146, 303 K): highest-pressure point only for each carbon isotherm (protocol scope at temperatures other than 77 K): SWCNT I2, A-SWCNT I4, ACF-1000 I6, ACF-1400 I8, ACF-1800 I10, ACF-2300 I12 (merged with text 0.26 wt%), O-ACF-1000 I14. isotherm_point_count 9 for each (5 filled + 4 open markers; the marker at the origin is not counted; some low-pressure markers overlap, so the count partly relies on the regular 5+4 pattern).

## Digitization method and checks

- All Fig. 2 and Fig. 3 symbols are black, so `digitize_figure.py colors` cannot separate series by colour. Series were separated by shape and fill, identified on zoomed crops of the page image: diamonds/circles told apart by their single-pixel top and bottom tips versus flat 3-pixel tops; triangles, inverted triangles and squares by outline. Marker seed positions are in work/labels.py. For each series a page-sized image (same pixel geometry as main-3.png) was written with only that series' markers: an isolated marker keeps its whole connected component; a marker touching others gets the pixels within 4.6 px of its seed that are nearer to it than to any other seed (neighbouring markers of other series and unattributed markers were given seeds too); each marker is replaced by its convex hull (so open symbols become discs) and a 1-px gap separates touching markers of the same series. `extract --mode markers --open-px 0` was run on these images (work/iso_2a_*.png, work/iso_2b_*.png); the tool computed every reported centroid. Extracted marker counts equal the identified marker counts for every series (26, 24, 23, 23, 11, 12, 31). Rows from split markers carry extraction_confidence 2, isolated markers 3.
- Fig. 3 highest-pressure markers are isolated except for the drawn line; a small window around each was copied to a blank image (work/iso_3*_end.png) and digitized with the default 3-px opening, which removes the line.
- Calibration Fig. 2a: x 0 MPa at px 328.45 (left axis), 0.1 MPa at px 541.0 (tick), check 0.05 MPa at px 435.25 (residual 0.49%); y 0 wt% at px 1811.75 (bottom axis), 2.5 wt% at px 1557.2 (top frame), check 1.0 wt% at px 1710.37 (residual 0.43%; the 1.5 tick at px 1659.76 has residual about 0.5%).
- Calibration Fig. 2b: x 0 at px 328.5, 0.1 at px 541.14, check 0.05 at px 435.0 (0.17%); y 0 at px 2133.38, 2.5 at px 1878.99, check 1.5 at px 1980.78 (0.02%).
- Calibration Fig. 3a: x 0 at px 346.59, 3 MPa at px 564.5, check 1 MPa at px 418.76 (0.64%); y 0 at px 1133.86, 0.3 wt% at px 881.0, check 0.1 at px 1050.08 (0.60%).
- Calibration Fig. 3b: x 0 at px 346.8, 3 MPa at px 565.57, check 1 MPa at px 420.0 (0.38%); y 0 at px 1448.54, 0.3 at px 1194.75, check 0.1 at px 1364.48 (0.63%).
- Tick pixel positions were measured as intensity-weighted centres of the tick and frame lines. The tool flags points above 0.1 MPa (Fig. 2) and above 3 MPa (Fig. 3) as beyond the highest labelled tick; they lie inside the plotted axes (to 0.12 and 3.5 MPa).
- `check` passed for Fig. 2a A-SWCNT (1.8 at 0.1 MPa: 1.778, 1.2%), Fig. 2a SWCNT (0.8 at 0.1 MPa: 0.837, 4.6%) and Fig. 2b ACF-2300 (2.3 at 0.1 MPa: 2.301, 0.03%). The single-point Fig. 3b ACF-2300 archive cannot be checked by the tool (it needs an x inside the covered range); a direct comparison gives 0.2637 wt% at 31.02 bar against the printed 0.26 wt% at 3.1 MPa (1.4%). The other archives stay "unchecked" because the paper states no value for those series.

## Merging decisions

- A-SWCNT 1.8 wt% at 0.1 MPa: two plotted points lie within max(2%, 0.02 bar) of 1.0 bar, the filled point at 0.981 bar (1.773 wt%) and the open point at 1.012 bar (1.782 wt%). By the closest-in-pressure rule the text value was merged with the open (desorption) point, and the row is coded isotherm_branch = desorption because the caption defines open symbols as desorption; the text itself names no branch. The filled point is kept as a digitized row. The last adsorption point (1.798 wt% at 1.078 bar) is outside the tolerance.
- SWCNT 0.8 wt% at 0.1 MPa: nearest plotted points 0.969 bar and 1.035 bar, both outside the tolerance, so it is a separate row without isotherm_id.
- ACF-2300 2.3 wt% at 0.1 MPa: nearest plotted point 1.0212 bar (2.317 wt%), 0.0212 bar from 1.0 bar, just outside the 0.02 bar tolerance (borderline), so it is a separate row without isotherm_id.
- ACF-2300 0.26 wt% at 303 K and 3.1 MPa: the highest-pressure Fig. 3b point is at 31.02 bar, within 2% of 31 bar, so the two were merged (M127).

## Coding decisions

- SWCNT and A-SWCNT are classed SWCNT, not composite: the 11 and 9 wt% metal is residual HiPco catalyst (recorded as residual_metal Fe; the elemental-analysis sentence says only "metal", and the TEM dark spots are attributed to Fe catalyst particles). The paper expresses their H2 uptake by weight exclusive of metal; this is stated in each row's notes.
- The HiPco material is purchased, so synthesis_method = commercial. The ACFs' source and activation route are not stated, so synthesis_method = unknown. O-ACF-1000 is kept as activated_carbon, with its oxygen groups in functional_groups (attributed by the authors citing ref. 13, not measured).
- The 303 K apparatus type is not named, so measurement_method = unknown and basis_inferred = unknown. instrument_identified = false because the home-built apparatus is described only by its thermostat, cell and procedure. No basis is named anywhere, so basis_stated = false and uptake_type = unspecified. No wt% convention or paired units, so wt_pct_convention = unknown/none. No uncertainty or replicate measurement is reported (the desorption branch is the same run), so replicates_reported = false.
- isotherm_point_count for the 77 K isotherms other than A-SWCNT is the number of markers identified, a lower bound (see below).

## Values seen but not extracted

- Fig. 2a, low-pressure overlap (x px 331-370, y px 1763-1809; below about 0.02 MPa and 0.48 wt%): roughly 19 markers (about 470 dark px) of SWCNT, H-YZ and H-ZSM5, possibly also A-SWCNT, overlap into one blob and could not be attributed or separated. SWCNT points below 0.0103 MPa are therefore missing. In the A-SWCNT cluster at 0.020-0.026 MPa, three filled markers were extracted, but an overlapped open marker cannot be excluded.
- Fig. 2b, low-pressure overlap: roughly 53 markers (about 1340 dark px) not attributed: about 10 in the ACF-2300/ACF-1800/ACF-1400 band at 0.025-0.049 MPa (where diamonds and circles converge), about 38 in the blob below about 0.031 MPa (all five ACF series), and about 5 along the axis below 0.0045 MPa. As a result, ACF-2300 has no points below 0.049 MPa, ACF-1800 none below 0.053 MPa, ACF-1400 none below 0.032 MPa, ACF-1000 none below 0.034 MPa and O-ACF-1000 none below 0.006 MPa.
- Fig. 3a/3b: all points other than the highest-pressure point of each carbon isotherm (protocol scope at 303 K).
- H-YZ and H-ZSM-5 zeolites (not carbon sorbents): all Fig. 2a and Fig. 3a isotherm points, their points in Figs. 4 and 5, the Table 1 rows (H-YZ S_micro 710 m2/g, S_ext 60, V_micro 0.27, W_ave 0.75 nm; H-ZSM-5 330, 50, 0.15, 0.92) and the text statement that zeolite uptake was below the ACFs'.
- LaNi5 1.42 wt% (Section 2.2): metal-hydride check of the 303 K apparatus, not a carbon sorbent.
- Fig. 4 (77 K, 0.1 MPa uptake vs V_micro; not an isotherm, not digitized): it shows values for ACF-1000, ACF-1400, ACF-1800 and O-ACF-1000 that the text and tables do not give (SWCNT, A-SWCNT and ACF-2300 are given in the text). It also shows the zeolites.
- Fig. 5 (303 K, 3.1 MPa uptake vs V_micro; not an isotherm, not digitized): it shows values for SWCNT, A-SWCNT, ACF-1000, ACF-1400, ACF-1800 and O-ACF-1000 that the text does not give (ACF-2300 0.26 wt% is given). It also shows the zeolites.
- Section 1 literature values (">3 wt.% at ambient temperature" [1-4], "less than 0.7 wt.% at ambient temperature and high pressure (10 MPa)" [7-9]): other papers' results, not measurements of this paper.
- "theoretical surface area is 2630 m2/g" (abstract, Section 3): a theoretical value, not a measurement.
- "Oxidation of ACF-1000 resulted in a >30% decrease in hydrogen uptake" and "amounts ... at 303 K were approximately one-tenth as large as those at 77 K": relative statements, not uptake values.
- DOE target 6.5 wt%: not a measurement.
- Fig. 1 (TEM images): no values. Raman and TEM tube diameter 0.9-1.3 nm is recorded in material_description.
