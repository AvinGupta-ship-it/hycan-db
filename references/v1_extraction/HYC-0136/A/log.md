# HYC-0136 extraction log (agent A)

Extracted from:
- Main text p.31091 (Hydrogen adsorption section): H2 uptake of GRHA 1:3, 1:1, 1:5 at 30 bar (wt% and mmol/g).
- Table 3 (p.31092): GRHA 25 C, 30 bar, 1.95 wt% (this work), same value as GRHA 1:3 in text.
- Table 4 (p.31093): qe,exp (mmol/g) 341.59, 973.99, 252.31, same measurements as text (3 rows total, merged).
- Table 1 (p.31089): BET area, pore volumes, pore size for each sample (characterization on every row).
- Methods text: BET (N2, 77 K, Quantachrome TouchWin, degas 150 C overnight), PSD by DFT, rig, 1 g sample, drying 120 C overnight.
- SI (si1): a Turnitin report plus a pre-print manuscript of the same paper; same values, nothing extra. data_location = main_text.

Not extracted:
- Fig. 10 (H2 uptake in mmol/g against time at 30 bar): kinetics curves, not isotherms, not digitized. Their end values equal the table/text values. Marker/curve points shown but not given in tables/text: none beyond the end values.
- Fig. 11, Fig. 12 (kinetic model fits) and Table 4 qe,cal, k1, k2, k3, R2: model outputs, not measurements.
- Fig. 6 (N2 isotherms at 77 K): not H2.
- Table 3 literature entries (Palimera sprout carbon, jute AC, fungi AC, BCNTs, MWCNTs, SWCNTs, carbon nanofibers, GO/ZIF-8@Pt, microporous AC, porous carbon, carbon nanotubes): other papers' values, not this paper's measurements.
- RHA (rice husk ash, BET 8.37 m2/g, TPV 0.04): characterization only, no H2 value, no row.
- Table 1 literature comparison entries (bamboo cane, kenaf, ginger, olive stone, rice husk refs 45, 46): other work.
- Highlights/abstract value 1.95 wt% (GRHA 1:3): same as Table 3.
- XRD d-spacing (Table 2, XRD) stored in interlayer_spacing_nm; crystallite size, TGA, Raman not stored.

Flags:
- Unit-consistency failure: 974 mmol/g would be 196 wt% (x0.201588) but the paper prints 1.95 wt%; the same ~100x mismatch holds for 341.59 (0.68 wt%) and 252.31 (0.50 wt%). Both printed values stored. wt_pct_convention unknown/none.
- Temperature: 25 C stated in Table 3 only for the 1.95 wt% value (GRHA 1:3); GRHA 1:1 and 1:5 stated only as room temperature, so temperature_unstated = true.
- Sample label for GRHA 1:3: Table 3 prints generic 'GRHA'; label taken from text/Table 4.
- Basis never named; volumetric rig so excess by instrumental default; no free-volume calibration stated.
