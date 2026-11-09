# HYC-0025 extraction log (agent B)

## Sources extracted from
- main-04/main-05 (pp. 39300-39301), "Synthesis of BCNTs": sample identities (boric acid 6.5, 13, 19.4, 26, 39 mM = BCNTs-I to -V; pristine MWCNTs without boric acid), FCCVD at 800 C, HCl purification of BCNTs; used in material_description and purification_method of all S1-S6 rows.
- main-05 (p. 39301), "Characterization": Sieverts apparatus, 303 K and 16 bar, samples about 250 mg degassed at 423 K for 2-3 h under vacuum; used on all S1-S6 rows.
- main-11 (p. 39307), text "Hydrogen adsorption study": 0.048, 0.216, 0.375, 0.497, 0.266, 0.202 wt% at 303 K and 16 bar; M1-M6.
- main-12 (p. 39308), Table 5: the same six values (and ID/IG, I2D/IG, oxidation T, B at%); recorded on M1-M6, not as separate rows.
- main-14 (p. 39310), Table 8 and text "Hydrogen adsorption isotherm analysis": hydrogen storage (same as M1-M6) and Langmuir Qm 0.257, 0.911, 1.285, 1.411, 0.991, 0.791 wt% at 303 K; Qm rows M7-M12 (fitted_extrapolated, pressure_unstated). b, K_L and R_F put in notes.
- main-15 (p. 39311), Table 9: hydrogen storage at 303 K and 16 bar (same as M1-M6; cited as the primary source of M1-M6); k2 in notes.
- si1-4, Table S1: Qe (Expt.) equals M1-M6; pseudo-second-order Qe (Cal.) 0.048, 0.216, 0.375, 0.497, 0.233, 0.200 wt% -> M13-M18; pseudo-first-order "Qe (Cal.)x 10^3" 0.065, 1.378, 1.462, 1.083, 2.436, 2.091 -> M19-M24, stored as printed x 10^-3 wt% (column-header convention; the other reading gives impossible values), confidence 3.
- main-07 (p. 39303) Table 2 (XPS B, C, O at% and peaks), main-09 (p. 39305) Table 3 (Raman), main-11 Table 4 (TGA), main-14 Table 6 (B 1s area%), main-06/main-08 XPS and XRD text: characterization put in dopant fields, functional_groups and notes of S1-S6 rows.
- main-02 (p. 39298), Introduction, Xia et al. [36]: 4.43 wt% at -196 C and 20 bar for S-doped microporous carbon with 2.03 at% S -> M25 (previously reported, cited literature value).
- main-13 (p. 39309), text "varies from 2.02 to 4.43 wt%" for the Xia et al. [36] S-doped carbons: 4.43 recorded on M25; 2.02 -> M26 (sample not identified), conditions from main-14 Table 7 (77 K, 20 bar).
- main-14 (p. 39310), Table 7: conditions of the studies in Fig. 11d (used for M26 and as a cross-check of M1-M6 and M25).

## Values seen but not extracted, and other decisions
- main-01 abstract: "0.497 wt% at 273 K and 16 bar" for 3.86 at% B. Same measurement as M4; temperature conflicts with every other statement (303 K). Not a separate row; noted on M4.
- main-12 text: "BCNTs-III reported the highest hydrogen storage (0.497 wt% at 303 K and 20 bar)". Same measurement as M4; pressure conflicts with 16 bar elsewhere. Not a separate row; noted on M4.
- main-11 text: "BCNTs-IV (8 at%) and BCNTs-V (6.3 at%)" swaps the B contents given in Tables 2, 5, 8, 9; tables used; noted on M5, M6.
- main-01 graphical abstract: bar chart of hydrogen storage (same values as Table 5) and radar chart (B at%, ID/IG, I2D/IG, hydrogen storage, Qm, K2). Not isotherms; no value beyond the tables.
- main-12 Fig. 10a-f: hydrogen uptake vs time at 303 K, 16 bar (main panels to about 900 s, insets 0-50 s). Kinetics, not an isotherm; not digitized. The transient Qt points before equilibrium are not given in tables or text and are not extracted; the plateaus correspond to the tabulated equilibrium values.
- main-13 Fig. 11a: bar chart, same values as Table 5. Fig. 11b: ID/IG and hydrogen storage vs XPS B at% (values in Tables 3/5). Fig. 11c: B 1s peak-area bars (Table 6). Fig. 11d: normalized hydrogen storage vs dopant concentration for Xia et al., Kim et al. and this work (normalized, not an isotherm; no absolute values). None digitized.
- main-15 Fig. 12a-c: pseudo-first- and pseudo-second-order linearized kinetic plots. Not isotherms; not digitized; derived constants are in Table S1.
- Kinetic and Langmuir constants (k1, k2, R^2, b, K_L, R_F) are not uptake values; recorded in notes only.
- main-02 Introduction and main-03 Table 1, Kim et al. [34], Pt-loaded metal-organic framework (Pt/MOF): a MOF, not a carbon sorbent; no numeric uptake printed (Table 7 gives only 303 K, 100 bar). Not extracted.
- main-02 Introduction and main-03 Table 1, Ramos-Castillo et al. [35], bimetallic Ti-Al sub-nanoclusters on graphene, "increase gravimetric hydrogen content from 3.2 to 3.6 wt%": not extracted. The paper gives no temperature, pressure or measurement method, the range cannot be assigned to individual materials (Ti5, Ti4Al, Ti7, Ti6Al), and the cluster-stability framing indicates computed rather than measured uptakes.
- main-02 Introduction, Xia et al. [36] samples with 1.28, 2.50 and 6.56 at% S: no individual uptake printed (one of them is presumably the 2.02 wt% of M26).
- main-12 text, Silambarasan et al. [70] gamma-irradiated MWCNTs: no uptake value printed.
- main-03 Table 1 rows for Lin et al. [16], Fu et al. [14], Sanchez-Padilla et al. [13], He et al. [33]: not hydrogen uptake (catalysis, ORR, electrochemical DFT); no values.
- No surface area, pore volume or pore diameter is reported for any sample (surface_area_method = none on all rows); the paper may not meet protocol 4 I4, which is outside this extraction's remit.
- main-05 TEM text: purified BCNTs-IV (Fig. 2g, h) showed diameters of about 10-15 nm, while 15-30 nm is given for all BCNTs; the general range is in the descriptions.
- TGA: residue "less than 15 at%" (as printed); ferrocene catalyst residue not identified or quantified, so residual_metal fields left empty. XRD shows boron carbide (BxC) peaks for BCNTs-IV and -V; kept as doped_carbon with a note, since the BxC phase is not quantified.
- No H2 isotherm is shown: each sample has one measured value (303 K, 16 bar), so no isotherm_id is assigned; the Langmuir fit's pressure points are not described.
- Degassing duration printed as a range (2-3 h); not stored in degas_duration_h, noted. Sample mass "around 250 mg" stored as 250.
- measuring_lab_id: corresponding authors are Patwardhan (**), Joshi (***) and Dasgupta (*); the first marked in byline order is Patwardhan, affiliation a (Institute of Chemical Technology). The paper does not say where the Sieverts measurement was made.
- Sample order: S1-S6 follow the graphical abstract on main-01 (MWCNTs, BCNTs-I to -V); S7, S8 are the cited Xia et al. samples (main-02, main-13). Labels from Table 5 (first table reporting uptake).
- digitizations/: empty; the paper has no isotherm figure.
