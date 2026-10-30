# HYC-0108 extraction log (agent B)

Zubizarreta et al. 2010, Carbon, "Ni-doped carbon xerogels for H2 storage". Input: 12 page images of the main article (main-01 to main-12); no supplementary file. 24 rows written.

## Sources extracted from

- Table 1 (main p.3, journal p.2724): S_BET, W0-N2, V_T, d_p and W0-CO2 for CX16AOXI, CX45AOXI, CX16AOXS and CX45AOXS, used as characterization on every row of those samples (per total sample mass).
- Table 4 (main p.5): carbon-mass-normalised S_BET, W0(N2) and W0(CO2) for the four Ni-doped samples, recorded in `notes` only. The fields hold the as-measured Table 1 values, which are on the same mass basis as the H2 uptake.
- Table 5 (main p.6): Ni content by ICP (wt%) goes in `metal_loading_wt_pct`; Ni by XPS (at%) and XRD particle size go in `notes`.
- Sections 2.1 to 2.7 (main pp.2-4): synthesis, KOH activation, HNO3 oxidation, Ni doping (dry impregnation or SEA), textural methods, H2 methods (77 K: DMT microbalance with buoyancy correction; 298 K: volumetric apparatus with helium calibration), pre-treatment and degassing, gas purity.
- Fig. 9 (main p.9): excess isotherms at 25 C up to about 196 bar for CX16AOXI, CX16AOXS, CX45OXAS (= CX45AOXS) and CX45OXAI (= CX45AOXI). Only the highest-pressure marker of each series is digitized (rows M1 to M4).
- Fig. 10a/10b (main p.10): CX45AOXS at -196 C up to 40 bar. All 9 measured markers of "Adsorbed hydrogen" (excess, I5, M5 to M13) and of "Total hydrogen" (total, I6, M14 to M22) are digitized from Fig. 10b. The volumetric capacity of each point (g H2 l-1) comes from Fig. 10a and is placed on the same row.
- Text on main p.10 (journal p.2731), also in the Abstract and Conclusions: "31.8 g of hydrogen is stored in 1 L tank filled with sample CX45AOXS" and "values reaching 6 wt.%" at -196 C and 40 bar. This is the same measurement as the 40-bar "Total hydrogen" point of Figs. 10a and 10b, so it is merged into one row (M22, text_direct).
- Fig. 11a/11b (main p.10): CX16AOXI at 25 C up to about 196 bar. Only the highest-pressure marker of "Adsorbed hydrogen" (excess, M23) and of "Total hydrogen" (total, M24) is used. The volumetric capacity comes from Fig. 11a.

## Digitization method

- The page images are 150 dpi and every series is black or grey, so series differ only by marker shape and fill. Each plot was cropped and enlarged 4x (bicubic, `work/upscale.py`), and the axis ticks were located by pixel-row and pixel-column inspection (`work/ticks.py`, `work/ticks2.py`). Every axis was calibrated on its lowest and highest labelled ticks and checked on a middle tick; all residuals were 0.0 to 0.2%.
- Filled markers: `digitize_figure.py extract --mode markers` on colour #111212 (tolerance 60), with a 7 px opening (11 px for Fig. 11a, which has a thick compressed-gas line). Legend boxes and panel labels were painted white first (`work/mask.py`) or excluded by ROI.
- Hollow markers: the digitizer cannot separate them by colour, so a preprocessing step (`work/isolate_open2.py`) paints them solid red. It finds the hollow-marker interiors (compact enclosed holes), fills them, removes solid black markers and opens away the connecting lines. The digitizer then takes the centroid of each red blob.
- Fig. 9: the CX16AOXS and CX45OXAI end markers overlap each other and the CX45OXAS square. For these two, the red blob is only the interior of the hollow marker (`work/isolate_open.py`, one small box per marker): the upper interior belongs to the open triangle and the lower one to the open circle. Confidence for these two rows is 3.
- The reproducible command list is `work/run_digitize.sh`. Step-6 checks passed for Fig. 10a total (31.8 g/l stated, 31.74 digitized at 40 bar) and Fig. 10b total (6 wt.% stated, 5.936 digitized at 39.95 bar, the centroid of the last marker).
- Marker counts. Fig. 10: 9 markers extracted out of 9 counted in each series. Fig. 11: 13 blobs per series, of which those near 120 and 160 bar are visibly doubled (two overlapping markers), so the count is 15. The marker near 80 bar may also be doubled; this is not resolvable. Fig. 9: 13 markers per series (about 10 to 196 bar). The four series overlap below 60 bar, so the count assumes one marker per series at each of the 13 positions seen at higher pressure.
- Every series in Figs. 9, 10 and 11 also has a marker at the origin (0 bar, 0). It is an anchor, not a measurement, and it merges with the axes. It is not extracted and not counted.
- Fig. 10a "Adsorbed hydrogen" open squares at 1 and 2 bar sit behind the "Total hydrogen" filled squares (about 0.2 and 0.5 g/l apart) and could not be separated. The volumetric capacity of rows M5 and M6 is therefore empty.
- Fig. 10a 40-bar markers have centroids 0.02 bar beyond the frame line, where the markers straddle it. The tool flags these as "outside axis range". They are the plotted 40-bar points.

## Values seen but not extracted

- Fig. 7 (main p.9, bar chart): excess H2 uptake at -196 C and 40 bar for CX16AOX, CX45AOX, CX16AOXI, CX16AOXS, CX45AOXI and CX45AOXS. It is not an isotherm, so it is not digitized. No table or text gives these values, except that CX45AOXS corresponds to the 40-bar point of Fig. 10b. As a result, the undoped supports CX16AOX and CX45AOX have no row. The text says these uptakes "correspond to the amount of hydrogen reversibly desorbed".
- Text (main p.9): "The increase in adsorption capacity is approximately 1 wt.% in the best case (i.e. sample CX16AOXS)". This is a difference relative to the support, not an uptake value.
- Text (main p.10): "13.1 g is stored by compression at the same conditions" (empty 1 L tank, -196 C, 40 bar). Not a sorbent value. The "Compressed hydrogen" lines in Figs. 10a and 11a are not digitized for the same reason.
- Text (main p.10): "DOE target: 45 g H2 L-1". This is a target, not a measurement.
- Fig. 6 (main p.8) and Fig. 8 (main p.9): H2 temperature-programmed desorption rate profiles (umol H2 g-1 s-1 against temperature) for the Ni-doped samples and the support. They are not isotherms, and the paper prints no integrated desorbed amount, so there is no value to extract. The Fig. 8 legend labels are CX16AOXI, CX45AOXI, CX16OXAS, CX45OXAS and Support.
- Figs. 9 and 11, all markers other than the highest-pressure one: not extracted, because these isotherms are at 25 C (protocol: highest-pressure point only).
- Samples with characterization but no H2 uptake row:
  - CX16A: Table 1, 1803 m2/g, 0.69, 2.11, 16 nm, 0.47; PZC 7.
  - CX45A: Table 1, 1684, 0.72, 2.37, 45 nm, 0.47; PZC 7.
  - CX16AOX: Table 1, 1822, 0.69, 1.72, 16 nm, 0.57; PZC 4; uptake only in the Fig. 7 bar chart.
  - CX45AOX: Table 1, 1587, 0.67, 1.89, 45 nm, 0.47; PZC 4; uptake only in the Fig. 7 bar chart.
  - Pristine CX16 and CX45: PZC 9 (Table 2) and CO2/CO TPD (Fig. 2, CX16).
- Non-H2 data:
  - Fig. 1: N2 isotherms.
  - Fig. 2: CO2/CO TPD.
  - Table 3 and Fig. 3: Ni adsorption against pH.
  - Figs. 4 and 5: TEM images and Ni particle-size histograms.

## Paper inconsistencies noted

- Fig. 10: the caption and the 31.8 g/l sentence name CX45AOXS, but one sentence says "Fig. 10 shows ... sample CX16AOXI". Rows follow the caption.
- The text calls the Fig. 11 sample "CX684OXI" once (p.2732), a misprint for CX16AOXI.
- The figure legends use CX45OXAS, CX45OXAI and CX16OXAS, and Table 4 uses CX45OXS. Section 2.5 writes "CXA16OXI". The labels used in the rows follow Table 1 and the Fig. 1 legends.
- The text gives Ni grain sizes of 2.5 and 2.4 nm for CX16AOXI and CX45AOXI, while Table 5 prints 2.7 and 2.4 nm. Rows use Table 5.
- The text gives the SEA pH as 7 (CX16AOX) and 5.0 (CX45AOX), but Table 3 marks 7.6/7.3 in bold for CX16OX.

## Coding decisions

- Fig. 10/11 isotherms: `basis_stated = true`. The paper names excess ("The hydrogen adsorption capacities correspond to excess adsorption values"), defines total storage, and plots both side by side. Fig. 9: excess is named but not defined for that figure, so `basis_stated = false` and `basis_inferred = excess`.
- The total and adsorbed series of one figure get separate `isotherm_id` values because their bases differ. The total is computed by the authors from the excess run plus gas compressed in the voids.
- Fig. 9 CX16AOXI (I1) and the Fig. 11b adsorbed curve (I7) are the same sample, temperature and basis, with nearly identical end points. The paper does not say whether they are the same run, so both are kept, and `replicates_reported = false`.
- `measuring_lab_id`: the corresponding author is Zubizarreta (Instituto Nacional del Carbón, CSIC). The H2 instrument references [10] and [39] are works of the Alicante co-authors, but the paper does not say where the H2 measurements were made.
- Volumetric capacity: the adsorbed series uses `packing_volume` without compressed gas; the total series uses `tank_volume` with compressed gas (1 L tank filled with sample).
