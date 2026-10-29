# HYC-0070 extraction log (extractor A)

Paper: Zhong et al., J. Phys. Chem. B 2002, 106, 9507-9513, "Nanosized Nickel(or Cobalt)/Graphite Composites for Hydrogen Storage". Input: main article only (7 pages), no supplementary file. 29 rows written (M1-M29), all validated with `validate_row_detail.py --errors-only` (0 errors).

## Sources extracted from

- Abstract (p.9507): 2.8 wt % at about 500 °C and 30-50 atm (merged into M2); 1.6 wt % after 5 cycles (M5); 2.7 wt % by PCI at 77 K and 70 atm (merged into M11). "can be released at 500 °C and 1 atm" is a desorption condition, not an uptake value, not extracted.
- Experimental section (pp.9507-9508): TPD method (home-built microreactor, GC 8000 and HPR20 MS, ca. 300 mg, 700 °C pretreatment in Ar, 35 atm charging from RT to 500 °C, TPD to 700 °C at 10 °C/min), IGA-003 (outgassed in vacuum to 700 °C), PCI by Advanced Materials Corporation (no model), Nova 3000 BET at liquid-nitrogen temperature (gas not named, range not stated). Used for method columns only.
- Results section 3, text on Figure 5 (p.9510): Ni20(arc) "ca. 2.3 wt % H2" (M1).
- Results section 3, text after Figure 6 (p.9510): "50atm ... ca. 2.8 wt %" (M2); sample not named in the sentence, Summary (p.9512) names Ni20C80 (arc).
- Results section 3, text on Figure 7 (p.9510): initial 2.3 wt % (M3), 1.8 wt % after the first 3 cycles (M4), ca. 1.6 wt % after 10 cycles (M6). The abstract says 1.6 wt % after 5 cycles (M5); the two cycle counts differ and both are recorded as printed. Cycling conditions are not restated, typical 500 °C and 35 atm used (flagged in notes).
- Results section 3, p.9511: cobalt-containing samples "ca. 1.6 wt % for H2 adsorption at 500 °C and 35 atm" (M7, sample `(unlabelled 1)`, S2).
- Results section 4, text on Figure 11A (pp.9511-9512): "0.6 wt % H2 uptake at ca. -190 °C" at 6 atm (M8); "estimated to be 0.4 wt % only" at -200 °C and 6 atm (M9).
- Results section 4, text on Figure 11B (p.9512): "ca. 1.6 wt % at 35 atm" (M10) and "2.7 wt % at 70 atm" (M11, merged with the plotted 70 atm point).
- Summary (p.9512): 2.8 wt % at 500 °C and 50 atm and 2.7 wt % at 70 atm; same values as M2 and M11.
- Figure 11B (p.9512, PDF page 6): 77 K PCI isotherm of Ni20(arc), digitized with `digitize_figure.py` (M12-M29, plus the 70 atm point in M11). See digitization notes below.

## Figure 11B digitization

- Calibration on page image main-6.png: x ticks 0 (px 723) and 80 (px 1153.5), verified on 40 (px 938.5, predicted 40.05, error 0.12%); y ticks 0.0 (px 694.5) and 3.0 (px 396.5), verified on 1.5 (px 545.5, error 0%). Tick pixels found by scanning pixel rows and columns (outward ticks below the x axis and left of the y axis). x axis is in atm, y axis is "H2 uptake(%)" read as wt %; pressures converted to bar by x 1.01325 in rows.csv.
- Marker colour #000000 (greyscale page), tolerance 60, `--mode markers`, ROI inside the frame.
- Markers counted on the plot: 22 (3 overlapping near the origin, 8 between 2 and 14 atm, 2 touching at 15.6 and 16.8 atm, 9 from 19.4 to 70 atm). `isotherm_point_count` = 22 (the origin cluster count is a minimum, the overlap hides how many there are beyond the 3 that its outline requires).
- Full-series run (`digitizations/HYC-0070_fig11B_Ni20arc_PCI_77K.json`): 19 centroids. Two are not single markers. (1) Origin cluster, centroid at 0.31 atm and 0.33 wt %: three overlapping markers that no region or tolerance separates; no row written for these 3 markers (lowest pressures, about 0.0 to 0.6 atm, about 0.3 to 0.36 wt %). (2) The pair at 15.6 and 16.8 atm touches at one pixel and merged into one 91-pixel centroid; it was separated by two ROI-limited reruns (`..._pairA.json` at 15.61 atm, 0.9010 wt %, 49 px; `..._pairB.json` at 16.82 atm, 0.9614 wt %, 42 px) and the merged centroid has no row. Rows M12-M29 come from the 17 single-marker centroids of the full run (minus the 70 atm point) and the two ROI reruns.
- Check against stated values (`check`, 5% tolerance): 70 atm vs 2.7 wt %: 2.742, +1.56%, pass; 35 atm vs 1.6 wt %: 1.653 by interpolation, +3.33%, pass. The full-series archive status is `passed`. The two ROI archives are `unchecked`: the paper states no value in their pressure range, and they share the calibration and verification ticks of the full run.
- The 70 atm marker (70.058 atm, 2.7433 wt %) is the same measurement as the printed "2.7 wt % at 70 atm" (printed pressure within 2% of the plotted point; the abstract gives the same PCI value): one row (M11) with the printed value, `text_direct`, digitized point in notes, no separate digitized row.
- The printed "ca. 1.6 wt % at 35 atm" (M10) is not merged: the nearest plotted point is 33.54 atm, 4.2% from 35 atm, outside max(2%, 0.02 bar). The paper cites Figure 11b for it, so M10 carries I1; the 33.54 atm point keeps its own row (M27).
- Temperature of the isotherm: caption and text say "liquid nitrogen temperature" (no number); the abstract states "77 K" for the PCI measurement. 77 K used as printed, `temperature_inferred` = false. If the reconciler reads the rule as applying figure by figure, the alternative is 77.3 K with `temperature_inferred` = true (within 1 K of 77).
- One adsorption branch only is plotted. No desorption branch.

## Coding decisions worth a second look

- TPD rows (M1-M7): `temperature_k` is empty with `temperature_unstated` = true. The loaded sample sits at room temperature (words only) and the stated 500 °C (773.15 K) charging temperature exceeds the schema's 500 K limit for `temperature_k` (the validator raised an error with 773.15). The 500 °C charging temperature is in notes; `reference_temperature_k` = 973.15 K (TPD end, 700 °C). `measurement_mode` = TPD, `isotherm_branch` = not_applicable, no `isotherm_id` (TPD values are not equilibrium isotherm points, and 35 atm and 50 atm values come from different charges).
- M8 and M9 (IGA TG cooling profile at 6 atm): `measurement_mode` = temperature_cycle (weight change along a temperature scan, not isothermal), `reference_temperature_k` = 273.15 (scan start per caption, 0 °C), no `isotherm_id`. M9 `value_kind` = unclear (authors' estimate after discounting moisture).
- Sample S1 `Ni20(arc)`: one physical sample across as-prepared and cycled rows. BET 130 m2/g is for as-prepared Ni20(arc); `area_same_sample` = yes for first-charge, IGA and PCI rows (pretreatment of the BET sample is not stated) and `unclear` for the cycled rows M4-M6, whose state differs (BET 284 m2/g measured after cycles, Figure 9 caption: after 5 cycles; carried in notes, one area per field).
- Sample S2 is `(unlabelled 1)`: the Co uptake sentence says "cobalt-containing samples" and does not name a sample. Co40(arc) is the only Co label printed (Figure 1c, TEM). No Co surface area, so `surface_area_method` = not_reported.
- M1 and M3 are two text statements of 2.3 wt % for Ni20(arc) at 35 atm (Figure 5 peak and cycle 1 of Figure 7); both kept, may be the same run.
- `replicates_reported` = false everywhere: no uncertainty is printed, and the cycle results come from sequential runs on a sample that changes (BET, Ni dispersion).
- `calibration_described` = false for all rows: the TPD calibration uses a known H2 volume against peak area, which is neither a free-volume determination nor a buoyancy correction; no buoyancy correction is stated for the IGA; the PCI free volume is not described. `instrument_identified` = true for TPD (home-built and described, with GC and MS models) and IGA (Hiden IGA-003), false for PCI (manufacturer, no model).
- `basis_inferred`: excess for the PCI (volumetric default), unknown for TPD and IGA (gravimetric without a stated buoyancy correction; TPD is neither). No basis is named anywhere (`uptake_type` = unspecified, `basis_stated` = false).
- wt % convention unknown (`wt_pct_convention_source` = none) on all rows: no definition, no paired unit.
- `surface_area_probe_gas` = unspecified for S1: "BET method at liquid-nitrogen temperature", the gas is not named. BET range and consistency criteria not stated.
- `measuring_lab_id`: corresponding author J. Lin (starred), National University of Singapore (printed "University"; the text layer shows a capital V from small caps).

## Values seen and not extracted

- Pore/surface characterization with no H2 value: mechanical mixture of 20 wt % Ni and 80 % graphite, BET 8.5 m2/g (no H2 uptake value); Ni40C60(arc), 26.8 wt % Ni by TPO (no H2 value); pure graphite residual 0.50 wt % by TPO; pure Ni powder TPO gain 26.3% (theory 28.3%); cathode deposit with large Ni particles above 100 nm (Figure 1e); Ni20(arc) after 5 cycles, BET 284 m2/g, pore volume and area distributions (Figure 9, no numeric volume stated). No numeric pore volume or pore diameter is printed for any sample, so those fields are empty.
- Figure 5 TPD profiles: C(arc) (pure graphite after arc discharge, peak at 522 °C), Ni40(arc) (peak 539 °C, "intensity about half that of Ni20(arc)"), Ni80(arc) (peak 501 °C, "even lower than" arc-discharged graphite), Ni40 before arc-discharge (peak 489 °C, "almost plain line") have no printed uptake value, only relative statements; not extracted, not digitized (TPD profile, not an isotherm). Same for pure graphite and pure Ni powder ("similar result", no value).
- Figure 6 TPD profiles of Ni20(arc) after charging at 35 atm to upper temperatures 300, 400, 500 and 700 °C: no values printed; not digitized. The 500 °C profile is the Ni20(arc) 35 atm profile of M1.
- Figure 7 TPD profiles for cycles 1, 2, 3, 4, 5, 10 and "no H2 adsorbed": values printed only for cycle 1 (2.3 wt %), 3 (1.8 wt %), 10 (ca. 1.6 wt %) and, in the abstract, 5 (1.6 wt %); cycles 2 and 4 have no printed value; not digitized.
- Text: "deposits on the cathode ... about 30-40% of those deposits on the chamber wall": a ratio, no absolute uptake; not extracted.
- Text: Ni removed from Ni20(arc) with HCl, residual carbon uptake "very similar to that of arc-charged graphite": qualitative, no value.
- Text: "under ambient pressure, almost no adsorbed hydrogen was detected": qualitative, no value.
- Text: "The small weight increase (<0.2 wt %) at temperatures between 0 and -120 °C is most probably due to the trace of moisture in the H2 gas": the authors attribute it to moisture, not H2 uptake; not extracted.
- Figure 11A (IGA TG profile, line without markers, not an isotherm): shows a plateau of about 0.1 wt % between about -20 and -100 °C and the rise to the 0.6 wt % the text gives at the cold end; no value beyond those in M8 and M9 extracted; not digitized.
- Figure 8 (FTIR), Figure 10 (XPS Ni 2p3/2), Figures 1-4 (TEM, XRD, Raman, TPO): no H2 uptake values.
- Abstract: "Under low temperatures below -120 °C and moderate pressures above 6 atm hydrogen storage ... could be detected": no value.
- No metal hydride standard, zeolite or MOF is reported; no other material excluded for scope. References 13 (Chen et al. 1999, alkali-doped CNT) and 17 are cited for background only; no value from them is reported in this paper.
- Previously reported values: none stated ("Previously we had proved that there was no catalytic reaction below 500 °C" is not an uptake value).

## Check of marker count

Counted 22 markers. The full run gives 19 centroids: 1 origin cluster (3 markers), 1 merged pair (2 markers) and 17 single markers (8 between 2 and 14 atm, 9 from 19.4 to 70 atm, the 70 atm marker among them). Markers with a row: 16 single markers plus the 2 ROI-isolated pair markers (together the 18 digitized rows M12-M29) plus the 70 atm marker (in M11) = 19. Markers without a row: the 3 unseparable origin markers. 19 + 3 = 22.
