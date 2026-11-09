# HYC-0029 extraction log (agent B)

## Sources extracted from
- main-07.png (p. 555), Section 3.3 text: as-prepared CNT weight change 0.22 +/- 0.07 wt.% (M1); "more than 1.0 wt.%" for 973 K and 1073 K activated CNTs after HNO3 wash, two lower-bound rows (M2, M3).
- main-08.png (p. 556), Section 3.4 text: repeats 0.22 +/- 0.07 wt.% (CNT without Co impregnation) and 3.41 +/- 0.05 wt.% (largest capacity, Co loaded activated CNTs, 1 atm); same measurements as M1 and M13, no separate rows.
- main-07.png (p. 555), Section 3.4 text: "maximum weight changes" 3.41 +/- 0.05 wt.% (Co loaded activated CNT, 973 K) and 1.36 +/- 0.03 wt.% (Co loaded as-prepared CNT); same values as Table 2 0.5 M rows (M13, M8), no separate rows.
- main-09.png (p. 557), Table 2: 12 H2 capacity values with Co content (M4-M15).
- main-07.png (p. 555), Table 1: residual Co (wt.%) of as-prepared and 873/973/1073 K activated CNTs; used as residual_metal (M1) and in notes; no H2 values.
- main-03.png (p. 551), Section 2.6: instrument (Cahn TG2121), H2 purity 99.9995%, sample mass "Ten milligrams", pretreatment 673 K 1 h in H2, cycle 303-673 K, buoyancy / quartz blank correction, "repeated at least once".
- main-02/03.png (pp. 550-551), Sections 2.2-2.5: synthesis (CVD of C2H2 over Co0.05Mg0.95O), HCl purification, KOH activation, Co wet impregnation, N2 BET/BJH on Quantachrome Autosorb-1 at 77 K, AAS for Co.
- main-04.png (p. 552) Section 3.2 text and main-05.png Fig. 5: BET areas as-prepared 453, 873 K 467, 973 K 764, 1073 K 859 m2/g (from text).
- main-01.png abstract: cycles 303-673 K "under one atmosphere"; areas 467 and 859 m2/g (same as text).

## Figures
- No figure in the paper is an H2 isotherm; nothing was digitized and `digitizations/` is empty.
- Fig. 9 (p. 555), weight change before/after 5 N HNO3 wash vs sample (not an isotherm, not digitized). Values it shows that tables/text do not give: before-wash points for 873K, 973K and 1073K activated CNTs; after-wash points for as-prepared and 873K CNTs; exact after-wash values for 973K and 1073K (text gives only "more than 1.0 wt.%"). The after-wash 973K marker sits close to the 1.0 wt.% level, not clearly above it; the text bound is recorded as printed (see M2 notes).
- Fig. 10 (p. 555), TG profiles (weight change vs T) of (a) as-prepared CNT, (b) Co loaded as-prepared CNT with 5.67 wt.% Co, (c) Co loaded-activated CNT with 4.41 wt.% Co: temperature-cycle curves, not isotherms; not digitized. Their weight changes correspond to M1, M7 and M12.
- Fig. 11 (p. 556), two successive TG cycles of "the Co loaded activated CNTs": printed legend values 1st cycle 2.88 wt.% and 2nd cycle 2.92 wt.% are not given in tables or text; not extracted (non-isotherm cycling figure). The sample's Co content is not stated; their mean equals Table 2 973 K 0.2 M (2.90 +/- 0.02, M12), noted there.
- Fig. 12 (p. 556), weight change vs Co loading for as-prepared and 973 K activated CNTs: plots the Table 2 values; not digitized.
- Fig. 4 (p. 553), DTG curves of Co nitrate reduction: not H2 uptake.
- Fig. 5 (p. 553), activation temperature vs yield and BET area: yields (%) not extracted (characterization, not in text); areas taken from text.
- Fig. 6 (p. 553), BJH pore size distribution and cumulative pore volume inset: no numeric pore volume or average diameter printed; not extracted.
- Fig. 7 (p. 554), Raman ID/IG ratios: characterization, not extracted.
- Figs. 1, 2, 3, 8, 13: TEM, XPS spectra and schematics; no uptake values.

## Values seen but not extracted
- Table 2 "A ratio of H/Co" and "Enhancement factor (eta)": quantities derived from uptake and Co content, not H2 uptake values.
- Samples with characterization but no H2 row: unwashed 873 K, 973 K and 1073 K activated CNTs (BET 467, 764, 859 m2/g; residual Co 0.16, 0.09, 0.15 wt.%; H2 weight change only in Fig. 9); HNO3-washed as-prepared and 873 K CNTs (Fig. 9 only).
- Literature values quoted from other work (not this paper's measurements): Dillon et al. 5-10 wt.% (SWCNT); Chambers et al. 67 wt.% at 100 atm, 300 K; 0.1-2.0 wt.% from refs [3-5]; Zhou et al. isosteric heats -1.7 and -6.4 kJ/mol; Kim et al. 2.8 wt.% (Ni/MWCNT) and 4 MPa, 300 K; Mu et al. 4.5 wt.% at 10.7 MPa, room temperature; Yoo et al. 1.5 wt.% at 1 atm, 573 K.
- Bulk cobalt nitrate DTG weight ratio 0.204: not a carbon sorbent and not H2 uptake.

## Coding decisions
- All H2 values are weight changes over 303-673 K heating/cooling cycles at 1 atm H2: measurement_mode = temperature_cycle, isotherm_branch = not_applicable, temperature_k = 303, reference_temperature_k = 673, no isotherm_id.
- basis_inferred = excess by instrumental default (gravimetric with stated buoyancy correction); basis_stated = false; uptake_type = unspecified.
- Degas fields hold the in-situ pretreatment (673 K, 1 h, flowing H2), which the paper does not call degassing; flagged in notes.
- Co-loaded samples: material_class = composite, metal_element Co, metal_loading_wt_pct = Table 2 Co content; BET area of the parent CNT with area_same_sample = parent_material. Washed activated CNTs: area_same_sample = unclear (paper does not say whether the area was measured before or after the HNO3 wash).
- Sample labels: Table 2 group heading plus row label (e.g. "Activated CNT-973 K impregnation condition, 0.2 M"); uncatalysed samples labelled from Fig. 9 category and series ("as-prepared (before wash)", "973K (after wash)", "1073K (after wash)").
