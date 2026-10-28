# HYC-0040 extraction log (agent B)

Input: 9 page images of the main article (HYC-0040_main-1 to -9). No supplementary pages were supplied.

## Sources extracted from

- Table 1, p. 7: experimental wt% at 77, 273 and 298 K (20 bar) for rGO, B-rGO, Ni-B-rGO, extracted as table_direct rows and merged with the highest-pressure marker of each plotted curve. Also the "recalculated" rows for B-rGO (negating the weight of B) and Ni-B-rGO (negating the weight of Ni), extracted as rows with value_kind = unclear, wt% convention unknown/none and no isotherm_id, because they re-normalize the measured value to the sample mass minus B or Ni rather than reporting a separate measurement.
- Text p. 6, results paragraph ("At 77 K ... 9.8 wt.%, 8.2 wt.% and 6.9 wt.%", "At 273 K ... 0.35, 0.58, 0.41 wt.%", "at 298 K ... 0.24 and 0.16 wt.% ... negligible for rGO"): same values as Table 1, cited in source_location. No separate rows.
- Abstract, p. 1: B-rGO ~0.24 (298 K), ~0.58 (273 K), 8.2 (77 K) wt%; Ni-B-rGO ~6.9, ~0.41, 0.16 wt%. Same measurements as Table 1. No separate rows.
- Fig. 8 caption, p. 7: same values again. No separate rows.
- Fig. 8(i), p. 7, 77 K: every marker digitized. rGO 33 markers (archive Fig8i_77K_rGO.json), B-rGO 30 (Fig8i_77K_B-rGO.json), Ni-B-rGO 35 (Fig8i_77K_Ni-B-rGO.json). The highest-pressure marker of each curve is merged with its Table 1 value and is not a separate row.
- Fig. 8(ii), p. 7, 273 K: every marker digitized to count them (23 per curve). Only the highest-pressure point is used, merged with Table 1 (archives Fig8ii_273K_*.json).
- Fig. 8(iii), p. 7, 298 K: B-rGO 22 markers, Ni-B-rGO 21 markers. Only the highest-pressure point is used, merged with Table 1 (archives Fig8iii_298K_*.json).
- Methods passages, p. 3 (GRC Sieverts set-up, H2 99.99%, degassing 12 h, ~200 mg, leak check and standard-sample calibration, BET with N2 at 77 K on an Autosorb iQ, degassing 100 C for 3 h before BET) and p. 6 (degassed at 100 C before PCI; Eq. (2) defines wt.%H as W2): used for the method and reporting fields.
- Text p. 6: rGO specific surface area 897 m2/g (BET, N2). Text p. 3: rGO interlayer spacing 0.35 nm. Fig. 4(f), p. 5: EDS map wt% for Ni-B-rGO (C 60, B 20, Ni 18). FTIR text p. 5: functional groups.

## Figure digitization notes

- Masks: copies of page 7 in the work directory (p7_mask_a/b/c.png) had the legends, the "T = ..." boxes and the coloured "%" labels painted white before colour isolation. No data marker lies in a masked area.
- Calibration: Fig. 8(i) x on ticks 1 and 9 (checked at 5) and y on 0 and 20 atm (checked at 10). Residuals were 0.07% on both axes. Fig. 8(iii): x on 0.02 and 0.22 (checked at 0.12), y on 0 and 20 atm (checked at 10). Residuals were 0.13% and 0.10%. The y axes are in atm. Pressures are converted to bar by multiplying by 1.01325.
- Fig. 8(ii) x axis is inconsistent. Its major ticks are equally spaced (78.6 px) but labelled 0.1, 0.2, 0.3, 0.3, 0.4, 0.5. Calibrated on 0.1 and 0.5, the 0.4 tick reads 0.4198 (4.96% off), so the verify tolerance was raised to 6% to archive the points. The digitized endpoints (rGO 0.320, B-rGO 0.528, Ni-B-rGO 0.392 wt%) are 7-9% below the printed values marked at the same points (0.35, 0.58, 0.41). Only the printed values are stored. The digitized endpoints appear in notes only.
- Origin: every Fig. 8 curve starts at the plot origin, where no marker is visible (any marker there is hidden by the axes). These points are not extracted and not counted in isotherm_point_count.
- Occluded marker: the first B-rGO marker in Fig. 8(i) (~0.42 wt%, ~0.8 atm) is almost entirely hidden under the first Ni-B-rGO triangle. It was extracted from 4 visible pixels using a 1-px opening, which probably biases its centroid low by about 0.1-0.2 atm. Its extraction_confidence is 3.
- The 77 K B-rGO marker at ~6.98 wt% sits on the grey 6.9% drop line. With the default 3-px opening the tool missed it, so the series was rerun with a 1-px opening. The final archive holds all 30 markers.
- The first 298 K B-rGO marker was split into two fragments by the overlapping Ni-B-rGO triangle. At colour tolerance 85 it merged into one marker, giving 22 markers, which matches the visual count.
- Black series were isolated with the default 3-px opening, which removes the connecting line. The centroid of an opened triangle can sit slightly below the marker's nominal centre, within 1% of the axis span.
- rGO at 77 K ends in two close markers: 20.115 bar / 9.819 wt% and 20.776 bar / 9.842 wt%. The second-highest is within 2% of the printed 20 bar. The printed 9.8 wt% is still matched to the highest-pressure marker, because the dashed 9.8% drop line starts at that marker. The second-highest marker is kept as a digitized row.
- The tool's `check` subcommand was not run, so the archives show status "unchecked". Each printed endpoint value is compared with its digitized point in the row notes.
- Fig. 8(iii) legend lists "rGO-no storage" but no points are plotted for it. The rGO 298 K row is the Table 1 value 0, coded approximate because the text calls it "negligible". It has no isotherm_id.

## Values seen but not extracted

- Introduction, p. 2: literature values cited for comparison, not measured in this paper:
  - Wei et al. [21]: 0.007, 0.13 and 0.055 wt% at 293.15 K, 1 bar.
  - Zhou et al. [22]: 0.77 wt% at 298 K, 80 bar.
  - Al-doped graphene, 5.13 wt% at 300 K and 0.1 GPa, and Ti-decorated graphene, 6.11 wt% [23,24]: DFT values.
  - N-doped CNTs [25]: 2 wt% at 298 K, 100 bar.
  - N-containing mesoporous carbons and Pt/N-MC [26]: 0.51 and 1.26 wt%.
  - Boron-substituted CNTs [27]: 2 wt% at 80 bar, 300 K.
  - Chung et al. [16]: 0.4 and 3.2 wt% at RT and 77 K, 56 bar.
  - Blankenship et al. [28]: 0.8 wt% excess and 1.2 wt% total at 30 bar, RT; 8.9 wt% at 77 K, 30 bar.
  - Pd-modified activated carbon [29]: 2.5 wt% at 298 K, 20 bar.
  - Pd-doped MWCNT [31]: 0.6 wt% at 273 K, 50 atm.
  - Pd3Co-decorated graphene composite [32]: ~4.6 wt% at 298 K, 30 bar.
  - Ni-doped MWCNT [33]: 0.298 wt% at 298 K, 20 bar.
- Text p. 6: Blankenship L.S et al. [28], 8.1 wt% at 77 K and 20 bar. This is a cited literature value.
- Text p. 6: "the net amount of hydrogen stored for a known amount of B-rGO and Ni-B-rGO is found to be: 3.7 g and 3.84 g". These are absolute masses for an unstated sample amount and unstated conditions. No schema field fits, and they cannot be converted.
- Text p. 8: "an increase in the adsorbed amount by 1.6 wt.%". This is a difference computed from two samples' values, so it is not a row.
- Supplementary Table S1 (a tabulation of literature values) and Table S2 (surface areas and pore data of the samples) were not in the input. The BET areas of B-rGO and Ni-B-rGO are therefore not recorded (surface_area_method = not_reported). The BJH pore-size results and the XPS results in the SI are also not available.
- Calibration standards LaNi5 (a metal hydride) and Basolite C300 (a MOF): not carbon sorbents, and no values are reported.
- GO sample: characterization only, no H2 uptake, so it has no row and no sample_id. Its characterization is XRD (001) at 12.5 deg with d = 0.7 nm, ID/IG 0.93, La 20.6 nm, and a TGA weight loss of 68% up to 1000 C.
- Characterization with no schema field:
  - Raman ID/IG: rGO 0.95, B-rGO 0.99, Ni-B-rGO 1.05 (1.15 after hydrogenation).
  - Crystallite size La: 20.2, 19.4 and 18.3 nm.
  - TGA weight loss: rGO 49.4%, B-rGO 20%, Ni-B-rGO 42.5%.
  - B-rGO G band at 1606 cm-1 vs 1584 cm-1.
- Fig. 9 (Raman of hydrogenated Ni-B-rGO at 253, 268 and 373 K and 20 bar) and Fig. 10 (FTIR at 303 K): qualitative evidence of adsorbed H2 and C-H bonds. No uptake values.
- Transducer resolution (~0.007 bar up to 68.9 bar, ~0.0007 bar up to 3.45 bar): an instrument specification, not an uptake uncertainty.
