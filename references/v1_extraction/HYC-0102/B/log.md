# HYC-0102 extraction log (agent B)

Inputs: paper.json; pages main-1.png to main-4.png (J. Phys. Chem. B 2006, 110, 24812-24815). The input has no supplementary files.

## Sources extracted from

- main p1 (p. 24812) Abstract: "a 3 wt % hydrogen uptake at 77 K and 30 bar" for the baked ozonized tubes. Same value as the Results text, so it is one row (M6). The surface areas in the abstract are listed under characterization below.
- main p1-p2 Experimental (Materials, Synthesis, Ozonolysis, Characterization, Exfoliation, Hydrogen Uptake): HiPco synthesis, purification (Chiang et al., ref. 24), ozonolysis, acid/bake treatment, BET method (multipoint N2-BET, Micromeritics ASAP 2010, samples dried at 110 °C before BET, no P/P0 range), H2 measured at NREL by "appropriately designed volumetric hydrogen capacity measurements at liquid nitrogen temperatures" (ref. 28). Coded on rows M1-M6.
- main p4 (p. 24815) Figure 5 (77 K H2 adsorption isotherm of pretreated ozonized SWNTs 4, blue diamond markers plus a Langmuir-Freundlich fit line): 5 markers counted, 5 extracted (M1-M5). Archive: digitizations/fig5_series4_markers.json.
  - Calibration on the page image (main-4.png, 1275 x 1650 px). x: 0 at 188.0 px (left axis line), 30 at 599.5 px (right frame line); third tick 10 at 325.0 px (residual 0.12%); the 20 tick is at 462.5 px (predicted 462.3). y: 0.00 at 736.39 px, 3.00 at 502.75 px; third tick 1.50 at 619.83 px (residual 0.22%). Tick and gridline positions come from intensity-weighted pixel row and column profiles.
  - Colour #2a2d7b, tolerance 40, ROI 180 505 598 656. The ROI leaves out the legend diamond (about y 675). Marker pixel counts are 126-137, so no two markers are merged.
  - The tool's stated-value check could not be run on the marker archive, because the paper states no value at any marker pressure, so its status is "unchecked". The same calibration passed the check against the stated 3 wt% at 30 bar on the fit line (see below).
- main p4 Results and Discussion text: "The hydrogen uptake of acid/baked ozonized SWNTs 4 is 3 wt % at 77 K and 30 bar (Figure 5)." gives M6, coded `fitted_extrapolated`. The last measured marker is at 3.25 bar, and only the LFI fit line reaches 30 bar. The same value appears in the Conclusion.
- main p4 Results and Discussion text: "a previously reported value (≈2.4 wt %) recorded under identical conditions for purified SWNTs.29" gives M7, coded previously reported (Panella, Hirscher, Roth, Carbon 2005, ref. 29), `uptake_bound` approximate, 77 K and 30 bar from "identical conditions". It is treated as a separate sample (S2) because the paper does not say the ref. 29 material is its own purified SWNTs.

## Seen but not extracted

- Figure 5, Langmuir-Freundlich isotherm (LFI) fit line: not extracted as rows. It is a model fit to the 5 measured markers, not a separately measured isotherm, and it runs from 0 to about 30.5 bar, far beyond the last measured point (3.25 bar). It was digitized only to check the calibration against the stated value (digitizations/fig5_LFI_fit_line_checkonly.json, curve mode, colour #ee2630, ROI 184 505 612 696): 2.907 wt% at 30 bar against the stated 3 wt%, a 3.1% difference, check passed. Nine trace points beyond 30 bar lie outside the axis range.
- "This is nearly 25% greater than a previously reported value": a ratio, not an uptake value.
- Introduction (p1): literature statements on H2 storage in SWNTs (70 K, proportionality to BET area, carbon nanofibers) give no values.
- Table 1 (p3, TGA weight loss 80-800 °C and C/functional group ratio): not H2 uptake. Weight loss: 1 15%, 2 25%, 3 10%, 4 23%, 5 30%. C/functional group ratios: 27:1, 30:1, 74:1, 4:1, 5:1.
- Figure 1 (Raman spectra), Figure 2 (SEM image), Figure 3 (AFM image), Figure 4 (length distribution histogram of n-dodecylated ozonized SWNTs: 33% 100 nm, 30% 200 nm, 18% 300 nm, 9% 400 nm, 4% 500 nm, 3% 600 nm, 3% 700 nm): not isotherms and not H2 uptake.
- Samples with characterization but no H2 uptake value (no rows):
  - purified SWNTs: BET 680 m2/g after drying at 110 °C (Table 2). After the acid/bake treatment, the surface area rises by "nearly 20%"; no value is printed.
  - 1 (n-butyl SWNTs): 410 m2/g after drying at 110 °C (Table 2); 770 m2/g after the acid/bake treatment (text and abstract).
  - 2 (1-adamantyl SWNTs): 269 m2/g (Table 2).
  - 3 (SWNTs with -CH2CH2CH2CH2CO2H groups): 410 m2/g (Table 2).
  - 4 (ozonized SWNTs before the acid/bake treatment): 381 m2/g after drying at 110 °C (Table 2, abstract). After the acid/bake treatment it becomes the H2 sample S1 (1068 m2/g).
  - 5 (epoxidized SWNTs, m-CPBA): 200 m2/g (Table 2); 366 m2/g after the acid/bake treatment (text).
  - Average bundle diameter from SEM: 10-30 nm for acid/bake-treated 4 and 50 nm for the other samples. These are not pore diameters, so they are not recorded.
- Non-carbon materials: none measured.

## Coding decisions

- Sample numbering: S1 (acid/baked 4, first in the abstract) and S2 (ref. 29 purified SWNTs, first on p4). Only samples with rows are numbered.
- Label of S1: "4", taken from the Figure 5 legend (no table reports its uptake).
- `measuring_lab_id` for S1 is "Simpson group, NREL". The paper says the H2 measurements were made at NREL, but no co-author is at NREL. The acknowledgment thanks "Drs. L. J. Simpson and M. J. Heben (NREL) for the hydrogen uptake experiments", and Simpson is listed first.
- `isotherm_id` I1 is shared by M1-M6. M6 carries it because the paper cites Figure 5 for the value. `isotherm_point_count` is 5 (5 measured markers, adsorption branch only).
