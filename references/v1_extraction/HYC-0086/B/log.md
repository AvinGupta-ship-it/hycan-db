# HYC-0086 extraction log (agent B, 2026-10-29)

Jimenez-Lopez et al. 2025, Chem. Eng. J. 520, 165834, HKUST-1@activated carbon hybrids. Input: page images main-01..11, si1-01..13. 25 rows, all for sample HYC-0086-S1 (AC = MSC 30).

## Scope decision
- Carbon sorbent extracted: AC (MSC 30, Kansai Coke), the only sample whose majority component by mass is carbon.
- Not extracted, HKUST-1 (Basolite C 300): a MOF, not a carbon sorbent (§3).
- Not extracted, HK-AC 5, 10, 20, 35, 50: the label p is g of AC per 100 g of HKUST-1 (main p.2: "HK-AC 50 indicates that for every 1 g of HKUST-1, 0.5 g of AC ... final AC weight percentage of 33.3"). That gives 4.8, 9.1, 16.7, 25.9 and 33.3 wt% AC, so the MOF is the majority component in every hybrid and none is a carbon sorbent (§3). Their values are listed below.

## Sources extracted from
- main p.7, Fig. 6a, AC series (excess wt.% vs pressure, 77 K): M1-M10 (isotherm I1, 10 markers, adsorption only). Archive fig6a_AC_nexc_77K.json.
- si1 p.11, Fig. S9, AC series (total wt.%, 77 K) and main p.7, Fig. 6c, AC series (total kg m-3, 77 K): M11-M20 (isotherm I2, 10 markers). The volumetric value of each point sits on the row of the total wt.% value for the same point. Archives figS9_AC_ntot_wtpct_77K.json and fig6c_AC_ntot_kgm3_77K.json. I2 is the authors' Eq. 2 transformation of the same instrument run as I1. It has its own isotherm_id because its basis (total) differs from I1's (excess), and the basis fields must be uniform within an isotherm.
- si1 p.10, Table S2, AC column: M21 (nexc 5.8 wt%, 77 K, 25 bar), M22 (ntot 37.0 kg m-3, 77 K, 100 bar), M23 (ntot 11.7 kg m-3, 77 K, 5 bar), M25 (ntot 2.0 kg m-3, row printed "77K; 160 bar", stored as 160 K, 5 bar; see Inconsistencies).
- si1 p.13, Fig. S11g, AC at 160 K: M24, the highest-pressure point only (non-77 K isotherm). Archive figS11g_AC_160K.json.
- main p.1 abstract, main p.7-8 text and main p.8 conclusion: the AC values printed there (5.8 wt% at 77 K and 25 bar; 37.0 kg m-3 at 77 K and 100 bar) are the same values as M21 and M22.
- si1 p.13, Table S3, AC row: the H2 storage capacity of 37.0 kg m-3 is the same value as M22.
- Methods and characterization: main p.2 sec. 2.1-2.2, main p.3 sec. 2.4, si1 p.3-5, si1 p.9 Table S1 (AC column). Carried on every row.

## Values seen but not extracted
- AC release capacities (si1 p.13 Table S3, main p.1 abstract, main p.8, Fig. 6f): Release 77K->160K is 35.0 kg m-3 (94 %) and Release 77K->77K is 25.3 kg m-3 (69 %). These are deliverable capacities that Eq. 3 computes as differences of two total uptakes, each already a row (M22 - M25 and M22 - M23). They are not an uptake at a stated state.
- Empty tank (no sorbent): storage 30.8 kg m-3; release 30.4 kg m-3 (98 %) for 77K->160K and 29.5 kg m-3 (95 %) for 77K->77K (si1 p.13 Table S3, main p.1, main p.8).
- HKUST-1 (MOF, not a carbon sorbent):
  - Table S2: nexc 3.8 wt% at 77 K and 25 bar; ntot 35.5 kg m-3 at 100 bar, 13.2 at 5 bar, and 2.2 in the row printed "77K; 160 bar".
  - Table S3: Release 77K->160K 33.3 (95 %), Release 77K->77K 22.3 (63 %).
  - Text: 35.5 kg m-3 (conclusion).
  - Curves not digitized: Fig. 6a, Fig. 6c, Fig. S9, and Fig. S11a at 160 K.
- HK-AC 5 (4.8 wt% AC, not a carbon sorbent):
  - Table S2: nexc 3.9 wt%; ntot 36.1, 13.4 and 2.0 kg m-3.
  - Table S3: Release 77K->160K 34.1 (94 %), Release 77K->77K 22.7 (63 %).
  - Curves not digitized: Fig. 6a, Fig. 6c, Fig. S9, Fig. S11b.
- HK-AC 10 (9.1 wt% AC):
  - Table S2: nexc 4.0 wt%; ntot 37.1, 13.8 and 2.1 kg m-3.
  - Table S3: Release 77K->160K 35.0 (94 %), Release 77K->77K 23.3 (63 %).
  - Curves not digitized: Fig. 6a, Fig. 6c, Fig. S9, Fig. S11c.
- HK-AC 20 (16.7 wt% AC):
  - Table S2: nexc 4.1 wt%; ntot 37.8, 14.0 and 2.0 kg m-3.
  - Table S3: Release 77K->160K 35.8 (94 %), Release 77K->77K 23.8 (63 %).
  - Curves not digitized: Fig. 6a, Fig. 6c, Fig. S9, Fig. S11d.
- HK-AC 35 (25.9 wt% AC):
  - Table S2: nexc 4.5 wt%; ntot 38.9, 13.8 and 2.1 kg m-3.
  - Table S3: Release 77K->160K 36.8 (95 %), Release 77K->77K 25.1 (65 %).
  - Curves not digitized: Fig. 6a, Fig. 6c, Fig. S9, Fig. S11e.
- HK-AC 50 (33.3 wt% AC):
  - Table S2: nexc 4.8 wt%; ntot 39.4, 14.1 and 2.0 kg m-3.
  - Table S3: Release 77K->160K 37.4 (95 %), Release 77K->77K 25.3 (64 %).
  - Text: abstract (4.8 wt%, 39.4 kg m-3, 37.4 kg m-3, a 26 % increase over HKUST-1) and main p.8 (25.3 kg m-3).
  - Fig. 6d, five 77 K cycles with desorption branches (standard deviation below 2 %).
  - Curves not digitized: Fig. 6a, Fig. 6c, Fig. S9, Fig. S11f.
- Text main p.7: the hybrids' maximum nexc is 3.8-4.8 wt% at 20-40 bar. These are the non-carbon samples above.
- Fig. 6b (main p.7) and Fig. S8a/b (si1 p.11): nexc at 25 bar against A_BET or S_2D-NLDFT. These are not isotherms, and every value equals a Table S2 value (AC 5.8 wt% = M21).
- Fig. 6e (main p.7): bar chart of the H2 stored at 77 K and 100 bar, split into compressed and adsorbed parts for the empty tank, HKUST-1, the hybrids and AC. It is not an isotherm and was not digitized. The tables and text give only the total (AC 37.0 = M22), not the adsorbed and compressed parts.
- Fig. 6f (main p.7): bar chart of the Release 77K->160K values, the same values as Table S3 (not rows; see above).
- Low-pressure H2 isotherms at 77 K (3Flex, si1 p.3), used only as 2D-NLDFT input: no uptake values are shown.
- Main p.7: "the BET area of the AC extrapolated from the dotted line ... would be around 2800 m2 g-1". This is a hypothetical value, not a measurement. The heuristic slopes (1 wt% per 500 m2 g-1 for BET; 1.25 wt% per 500 m2 g-1 for S_2D-NLDFT) are not values.
- Characterization of the non-carbon samples (si1 p.9 Table S1), not used:
  - HKUST-1: A_BET 1780 (N2), 1820 (Ar); V_T 0.76 (N2), 0.71 (Ar); rho_tap 372; rho_sk 2457.
  - HK-AC 5: A_BET 1970, 1760; V_T 0.88, 0.79; rho_tap 360; rho_sk 2473.
  - HK-AC 10: A_BET 2050, 1840; V_T 0.96, 0.85; rho_tap 361; rho_sk 2462.
  - HK-AC 20: A_BET 2090, 1970; V_T 1.00, 0.91; rho_tap 349; rho_sk 2582.
  - HK-AC 35: A_BET 2100, 1950; V_T 1.03, 0.93; rho_tap 342; rho_sk 2410.
  - HK-AC 50: A_BET 2180, 1990; V_T 1.09, 0.98; rho_tap 325; rho_sk 2502.
  - 2D-NLDFT values are also given for each in Table S1.
- Non-H2 data: water isotherms at 293 K (Fig. 5), thermal conductivity (Fig. 2f; AC 0.23 W m-1 K-1), TGA/DTG (Fig. 2d-e, S2, S3), XRD/FTIR (Fig. 2a-c), N2/Ar isotherms (Fig. 4, S6). None is an H2 uptake value.

## Inconsistencies and coding choices
- Table S2 prints the third ntot row as "77K; 160 bar". It is stored as 160 K and 5 bar (M25) for three reasons:
  - The text and the Fig. 6 caption define the temperature-swing discharge state as 5 bar and 160 K.
  - Eq. 3 with Table S3 reproduces the row for every sample (AC: 37.0 - 2.0 = 35.0; HKUST-1: 35.5 - 2.2 = 33.3; HK-AC 50: 39.4 - 2.0 = 37.4).
  - The isotherms go only up to 140 bar.
  The printed label is quoted in the row's notes, and extraction_confidence is 3.
- Excess maximum for AC (M21): the text calls 5.8 wt% at 25 bar the maximum, but Fig. 6a has no AC marker at 25 bar.
  - 5.8 equals linear interpolation between the markers at 19.1 bar (5.64) and 30.0 bar (5.91).
  - The highest plotted marker is about 5.96 wt% at about 50 bar.
  - Coding: not merged with a plotted point (no marker within 2 %, and the paper does not say the value was taken from the curve), so no isotherm_id. value_kind is measured by the 3 % rule (1.9 % from the 30.0 bar marker), and the possible interpolation is flagged in the row's notes.
- M22 (100 bar) and M23 (5 bar): no plotted marker lies at these pressures, and the paper does not say how they were obtained. value_kind is unclear and they have no isotherm_id. The same applies to M25.
- Basis:
  - Excess and total are named and reported side by side, and Eq. 2 defines total, so basis_stated is true for the 77 K rows and the Table S2 rows. ntot includes the gas in the inter- and intra-particle voids of the tapped bed.
  - The 160 K curve (M24) is labelled only "H2 adsorbed", so basis_stated is false and basis_inferred is excess by the manometric default.
- wt% convention: not defined in the paper, and no mmol g-1, mg g-1 or cm3(STP) g-1 values are given, so unknown/none on every row.
- replicates_reported is false. Main p.5 says that "selected" N2, H2 and Ar isotherms were repeated three times with error below 3 %, without naming the samples, in the context of textural analysis. The repeated cycles in Fig. 6d are for HK-AC 50 only.
- Pore volumes:
  - Total pore volume 1.76 cm3 g-1 is the N2 single point at p/p0 = 0.97.
  - The micro-, meso- and ultramicropore volumes come from 2D-NLDFT-HS fitted jointly to N2 and H2 isotherms at 77 K. pore_volume_method is therefore NLDFT and pore_volume_probe_gas is other.
  - The 2D-NLDFT total is 1.60 cm3 g-1 and the Ar total is 1.61 cm3 g-1; both are in the notes.
- Tapped density of HKUST-1: 372 kg m-3 in the text and Table S1, but 380 kg m-3 in the conclusion. AC is 240 kg m-3 everywhere.

## Digitization records
- Fig. 6a, AC (main-07.png).
  - Calibration: x on 0 bar (px 182.46) and 140 bar (px 427.96), checked at 80 bar (px 322.81, error 0.05 %). y on 0 wt% (px 1146.36) and 6 wt% (px 956.69), checked at 3 wt% (px 1051.32, error 0.2 %).
  - Colour #fd0100, tolerance 80, ROI from the plot frame. 10 markers extracted, 10 counted. Tolerance 60 missed the marker at 104 bar.
  - Check passed against Table S2 (5.8 at 25 bar; interpolated 5.79).
- Fig. 6c, AC.
  - Extracted from a work copy of main-07.png with the inset (red dashed box, px x 938-1089, y 1028-1150) painted white, because the inset repeats the curves at another scale.
  - Calibration: x on 0 (px 838.92) and 140 (px 1090.33), checked at 80 (px 982.59). y on 0 (px 1153.24) and 40 kg m-3 (px 966.35), checked at 20 (px 1059.52).
  - The ROI was extended to the top frame (px 944) because the highest point (41.1 kg m-3) lies above the 40 tick.
  - 10 markers extracted, 10 counted. Check passed against Table S2 (37.0 at 100 bar; interpolated 37.21). At 5 bar, linear interpolation gives 10.8 against the printed 11.7: the curve is concave between the markers at 0.9 and 8.1 bar.
- Fig. S9, AC (si1-11.png).
  - Calibration: x on 0 (px 446.85) and 140 (px 892.96), checked at 80 (px 701.59). y on 0 (px 1236.43) and 18 wt% (px 863.80), checked at 10 (px 1029.45).
  - Colour #f50000, tolerance 80. 10 markers extracted, 10 counted.
  - Archive status unchecked: the paper states no value from this figure.
- Fig. S11g, AC at 160 K (si1-13.png).
  - Calibration: x on 0 (px 238.21) and 140 (px 469.00), checked at 80 (px 370.47). y on 0 (px 852.61) and 3.5 wt% (px 660.28), checked at 2.0 (px 743.00).
  - Colour #f50000, tolerance 100, open-px 2: 13 of 13 solid (charge) markers extracted. The default opening missed the solid markers at about 31 and 127 bar, which open markers partly cover.
  - The 6 open (discharge) markers are rings that the tool did not separate. They were counted on enlarged crops (at about 33, 52, 79, 106, 126 and 134 bar). Total count 19 (isotherm_point_count).
  - Only the highest-pressure point (136.9 bar, 2.99 wt%) is used. Archive status unchecked: the paper states no value from this figure.
