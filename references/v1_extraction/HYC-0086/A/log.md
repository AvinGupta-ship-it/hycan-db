# HYC-0086 extraction log (extractor A)

Paper: Jimenez-Lopez et al., Chem. Eng. J. 520 (2025) 165834, HKUST-1@activated carbon hybrids made by resonant acoustic mixing. Main article plus SI file si1. H2 measurement: HPVA II manometric (Micromeritics), 77 K up to 140 bar, excess by the Leachman EOS; total by Eq. 2 from tapped and skeletal density.

Rows written: 34 (all for sample HYC-0086-S1, AC = commercial MSC 30). Four isotherm ids: I1 Fig. 6a (excess, wt%), I2 Fig. 6c (total, kg m-3), I3 Fig. S9 (total, wt%), I4 Fig. S11 (160 K).

## Scope decisions

- Carbon sorbent test (section 3): the majority component by mass must be carbon. AC (MSC 30) passes. The five HK-AC hybrids fail: they hold 5 to 50 g AC per 100 g HKUST-1, which is 4.76, 9.09, 16.67, 25.93 and 33.3 wt% AC, so a MOF is the majority component by mass in every hybrid. They are not extracted. Everything seen for them is listed below.
- HKUST-1 (pure MOF, measured for comparison) is not a carbon sorbent. Not extracted.
- Release (usable) capacities are differences of two total uptakes, (ntot)storage minus (ntot)release (Eq. 3), not stored or adsorbed amounts. Not extracted, listed below.
- Excess basis: Table S2 and Fig. 6a/6d call the quantity nexc, defined in the Abbreviations as "Measured excess hydrogen uptake"; total basis: ntot is defined in Sec. 2.4 and the Abbreviations, and the paper reports both side by side, so basis_stated = true for I1, I2, I3 and the Table S2 ntot rows. Fig. S11 calls the quantity "H2 adsorbed (wt.%)" without naming a basis: basis_stated = false, uptake_type = unspecified, basis_inferred = excess (volumetric Sieverts default).
- wt% convention is not defined by the paper for nexc or ntot: wt_pct_convention = unknown, source = none.
- One isotherm id per plotted curve: excess (Fig. 6a), total in kg m-3 (Fig. 6c), total in wt% (Fig. S9) and the 160 K curve (Fig. S11) come from the same instrument runs but carry different bases and quantities, and the basis fields are coded once per isotherm id.
- Table S2 nexc rows carry the Fig. 6a isotherm id because Sec. 3.2 says the maximum nexc values are "see Fig. 6-a and Table S2". Table S2 ntot rows are not tied to a plotted curve by the paper, so they carry an id only when merged with a plotted point (none for AC).
- measuring_lab_id is "Fierro group, Université de Lorraine": V. Fierro is the author marked with * (corresponding author), first affiliation Université de Lorraine; the paper does not say the H2 measurement was made elsewhere.

## Extracted

- Table S2 (SI PDF p. 10), nexc 77 K 25 bar, AC = 5.8 wt%: 1 row (M6), table_direct, carries I1. Same value in the abstract and Sec. 3.2 (one measurement, one row). No Fig. 6a marker within 0.50 bar of 25 bar (nearest 19.18 and 29.82 bar), so not merged.
- Table S2 (SI PDF p. 10) and Table S3 (SI PDF p. 13), ntot 77 K 100 bar, AC = 37.0 kg m-3: 1 row (M22), table_direct, no isotherm id. Same value in the abstract and Conclusions and as "H2 storage capacity" in Table S3 (one measurement). No Fig. 6c marker within 2.00 bar of 100 bar (nearest accepted 103.74 bar, 37.90 kg m-3), so not merged.
- Table S2, ntot 77 K 5 bar, AC = 11.7 kg m-3: 1 row (M32), no isotherm id (no Fig. 6c marker within 0.10 bar of 5 bar).
- Table S2, ntot printed "77K; 160 bar", AC = 2.0 kg m-3: 1 row (M33), coded 160 K and 5 bar (inferred), confidence 2, value_kind unclear. The printed label cannot be right: the value equals ntot(100 bar) minus R77K->160K (37.0 - 35.0 = 2.0, same relation holds for every column of Tables S2 and S3), and 2 kg m-3 at 77 K and 160 bar contradicts Fig. 6c (about 40 kg m-3). If the reconciler prefers the printed label, change temperature_k to 77 and pressure_bar to 160 and reconsider value_kind.
- Fig. 6a (main-07 panel a), AC, nexc vs p, 77 K: 10 markers counted, 10 extracted (M1-M5, M7-M11) plus the Table S2 row M6 in the same isotherm. Archive fig6a_AC.json, check at 25 bar expected 5.8, got 5.800 (passed). One extra detection at 0.25 bar (49 px, 23% of a marker) is a fragment of the 0.22 bar marker and is not a row.
- Fig. 6c (main-07 panel c), AC, ntot (kg m-3) vs p, 77 K: 10 markers counted, 10 extracted (M12-M21), basis tank volume, includes compressed gas. Archive fig6c_AC.json, check at 100 bar expected 37.0, got 37.196 (passed). One extra detection at 112.92 bar (9 px) is a line fragment and is not a row.
- Fig. S9 (si1-11), AC, ntot (wt%) vs p, 77 K: 10 markers counted, 9 extracted (M23-M31). Archive figS9_AC.json, check at 100 bar expected 15.4167 (37.0/240), got 15.082 (2.2%, passed). The first marker digitizes at -0.04 bar, which is not a valid pressure (pressure_bar must be above 0), so it is not a row; its value would have been 0.21 wt%. Note for the reconciler: at 100 bar the Fig. S9 curves sit below ntot(Table S2)/rho_tap by 2.2% for AC and up to 4.5% for the hybrids (digitization checks), a small inconsistency inside the paper; the plotted values are what is stored.
- Fig. S11 (si1-13 panel g), AC, H2 adsorbed (wt%) at 160 K: highest-pressure marker only (M34, 136.85 bar, 2.99 wt%), charge branch. 19 markers counted over both branches (charge solid, discharge open). Archive figS11_AC_160K.json, check at 5 bar expected nexc 0.5548 (from Table S2 ntot at 5 bar, 160 K, Eq. 2), got 0.5216 (6.0%, within the 10% tolerance set for this check). The other markers of this isotherm (detected between 0.6 and 127.6 bar) are not rows: only the highest-pressure point is extracted at temperatures other than 77 K.
- Table S1 (SI PDF p. 9), AC characterization: ABET N2 77 K 3030 m2/g (Ar 87 K 2830), VT N2 1.76, VT Ar 1.61 cm3/g, 2D-NLDFT-HS values S 2258 m2/g, Vtot 1.60, Vmicro 0.90, Vsupermicro 0.04, Vultramicro 0.86, Vmeso 0.70 cm3/g, rho_tap 240 kg m-3, rho_sk 2010 kg m-3. Carried on every row (ultramicropore cut-off 0.7 nm; pore volumes are 2D-NLDFT values from N2 and H2 at 77 K, probe gas coded other; micropore, ultramicropore and mesopore volumes are the 2D-NLDFT values; total pore volume column is the 2D-NLDFT value, VT N2 at p/p0 = 0.97 is in notes). BET range not stated (bet_range_stated false); Rouquerol criteria stated (bet_consistency_criteria_stated true). Sample mass "around 1 g" is stored as 1000 mg; degassing 398 K (stored as 124.85 C), "overnight", no numeric duration; HPVA II is named with manufacturer and model (instrument_identified true); no free-volume calibration described (calibration_described false); no H2 purity stated; no replicate or uncertainty for the AC isotherm (replicates_reported false).

## Seen but not extracted

HKUST-1 (not a carbon sorbent):
- Table S2: nexc 77 K 25 bar 3.8 wt%; ntot 77 K 100 bar 35.5, 5 bar 13.2, "77K; 160 bar" 2.2 kg m-3; R77K->77K 22.3, R77K->160K 33.3 kg m-3. Table S3: storage 35.5, release 33.3 (95%) and 22.3 (63%) kg m-3. Fig. 6a, 6c, S9, S11 panel a curves. Text: 372 kg m-3 and 380 kg m-3 tapped density, 35.5 kg m-3 at 77 K and 100 bar, "3.8" lower bound of the 3.8 to 4.8 wt% range (Sec. 3.2). Table S1 characterization.

Hybrids HK-AC 5, 10, 20, 35, 50 (MOF is the majority component by mass, 4.76 to 33.3 wt% AC):
- Table S2 nexc 77 K 25 bar (wt%): 3.9, 4.0, 4.1, 4.5, 4.8. ntot 77 K 100 bar (kg m-3): 36.1, 37.1, 37.8, 38.9, 39.4. ntot 77 K 5 bar: 13.4, 13.8, 14.0, 13.8, 14.1. ntot "77K; 160 bar": 2.0, 2.1, 2.0, 2.1, 2.0. R77K->77K: 22.7, 23.3, 23.8, 25.1, 25.3. R77K->160K: 34.1, 35.0, 35.8, 36.8, 37.4.
- Table S3 storage and release capacities of the same samples (same values as Table S2); abstract and Conclusions values for HK-AC 50 (4.8 wt% nexc, 39.4 and 37.4 kg m-3, 26% increase over HKUST-1).
- Fig. 6a, 6c, S9 curves of the five hybrids (14 markers each, partly hidden by other series); Fig. 6d (five consecutive nexc cycles of HK-AC 50 at 77 K, cycle 5 on top, adsorption solid and desorption open symbols, 19 markers; the text gives a standard deviation below 2% over five cycles); Fig. S11 panels b to f (160 K). Digitization attempts for these series were archived in the work directory, not in this output.
- Table S1 characterization of the five hybrids.

Other values and figures that are not H2 uptake rows for AC:
- Release capacities for AC: R77K->77K 25.3 kg m-3 and R77K->160K 35.0 kg m-3 (Tables S2 and S3, Fig. 6f, abstract, Sec. 3.2, Conclusions); % release 69 and 94 (Table S3). Derived differences of total uptakes, not stored amounts.
- Empty tank: storage 30.8, release 30.4 (98%) and 29.5 (95%) kg m-3 (Table S3, abstract, Sec. 3.2). Not a sorbent.
- Fig. 6b and Fig. S8: nexc against ABET and against S2D-NLDFT (Chahine plots). Not isotherms; they show only the Table S2 nexc values already listed.
- Fig. 6e: stacked bars of H2 storage capacity split into compression and adsorption contributions for all samples. The totals equal the Table S3 storage capacities; the split values are not given in a table or in the text and the bar chart is not digitized (not an isotherm).
- Fig. 6f: bars of release capacities (same as Table S3).
- Fig. 4, S6, 5: N2 77 K, Ar 87 K and H2O 293 K isotherms (textural and water, not H2 uptake). H2 (77 K) low-pressure isotherms on the 3Flex were used for the 2D-NLDFT pore size analysis; no H2 uptake value is printed or plotted for them.
- Fig. S10: tapped density against wt% AC; text value 372 kg m-3 HKUST-1 and 240 kg m-3 AC (AC value used in the Eq. 2 data).
- Fig. 2, 3, 5, S1 to S5, S7: structure, XRD, FTIR, TGA, SEM, water affinity, no H2 data.
