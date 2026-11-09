# HYC-0016 extraction log (agent B)

Input: 18 page images of the main article (DiVA postprint; main-01 is the repository cover page). No supplementary pages were supplied; the paper says its supplementary data are XPS and Raman spectra only.

## Sources extracted from

- Abstract (main-02, paper p. 1): "maximal observed value of ~5 Wt% for 2300 m2/g sample" at 77 K -> M1 (text_direct, approximate; pressure 50 bar from the Figure 5 caption; not merged with Figure 4, see the row notes).
- Section 3.2, H2-annealing paragraph (main-09, paper p. 8): "0.20Wt% at 120 Bar prior to activation and 0.22wt% after" -> M12, M13 (two treatment states of one unidentified sample; temperature not stated numerically).
- Figure 3 (main-17, paper p. 16), 293 K gravimetric isotherms, 5 curves: only the highest-pressure marker of each is extracted (not 77 K) -> M14 (AC), M31-M34.
- Figure 4 (main-17, paper p. 16), 77 K volumetric isotherms, 7 curves: every separable marker digitized -> M2-M11, M15-M30, M35-M72.
- Experimental (main-05, main-06) for methods: N2 adsorption (Quantachrome Nova 1200e) for surface area; Rubotherm gravimetric system at room temperature (precision +/- 0.02 wt% for a typical 200 mg sample; FLUIDCAL fluid densities of H2 and He); Hiden Isochema IMI volumetric system with liquid-nitrogen immersion cell for 77 K; degassing "usually" 150-300 °C, 12-16 h, high vacuum; typical sample size 100-300 mg. No BET P/P0 range, no consistency criteria, no H2 purity, no free-volume calibration stated.

## Digitization

Axes were located by pixel-row and pixel-column inspection of main-17.png (full page image, 1275 x 1650 px).

- Figure 3: x ticks 0 bar at px 367.33 and 140 bar at px 909.5, check tick 60 bar at px 599.5 (residual 0.08%); y ticks 0 wt% at px 612.5 and 0.6 wt% at px 271.0, check tick 0.2 wt% at px 498.54 (residual 0.11%). ROI x 369-908, y 216-611. Red series colour #fe0100, black #000000, tolerance 60, markers mode, default 3-px opening.
- Figure 4: x ticks 0 bar at px 365 and 50 bar at px 945, check tick 20 bar at px 597; y ticks 0 wt% at px 1277 and 5 wt% at px 943.5, check tick 2 wt% at px 1143. ROI x 366-840, y 898-1276 (excludes the curve labels at the right). Red #fe0000, black #000000, tolerance 60, markers mode, default 3-px opening.
- All black markers of a figure share one colour, so black markers were digitized in one run per figure (fig3_black_combined_run.json, fig4_black_combined_run.json). Each marker was then assigned to its curve, and the per-series files (fig3_1740, fig3_1250, fig3_560, fig3_310, fig4_2300, fig4_1730, fig4_1450, fig4_1259, fig4_650, fig4_370) hold that series' points copied unchanged from the combined run, with a `split_from` block naming the run and point indices. The red AC series were digitized directly (fig3_AC_1830_red, fig4_AC_1830_red).
- The tool's value check (`digitize_figure.py check`) could not be run: the paper prints no value at a stated pressure inside any digitized series' range. The only candidate, the abstract's ~5 wt% for the 2300 m2/g sample, has its stated pressure (50 bar, Figure 5 caption) outside the digitized range (2.3-38.75 bar), and the tool refuses it. All archives therefore carry status "unchecked"; the marker-count check (step 6) was done as below.
- Two points lie just above the highest labelled y tick but inside the plot frame and are flagged by the tool as outside the calibrated range: Figure 3 AC at 124.8 bar (0.631 wt%, above 0.6) and Figure 4 2300 m2/g at 38.75 bar (5.097 wt%, above 5).

### Marker counts (step 6)

Figure 3: 5 markers on each of the 5 curves, plus one marker at the origin shared by all curves (not attributed). Extracted: red 5/5; black 20/20 plus the origin marker. Only the highest-pressure marker of each curve is written to rows.

Figure 4 (counts are markers identified per curve; markers below about 0.6 bar pile up along the y axis and cannot be counted or attributed, so the black counts are lower bounds):

| Curve | Markers identified | Extracted | Not extracted |
|---|---|---|---|
| AC, 1830m2/g (red) | 17 | 16 | 1 marker almost wholly hidden behind black markers at about 0.25 wt% near the y axis (~8 px visible). The 5 extracted markers below 1.4 bar are partly covered by black markers or lines (18-32 px against ~42-49 px); their centroids come from the visible part (confidence 2). |
| 2300m2/g | 12 | 10 | 2 markers merged with 1730m2/g markers (near 1.4 and 1.8 bar). |
| 1730m2/g | 9 | 7 | 2 markers merged with 2300m2/g markers (near 1.5 and 2.1 bar). The marker near 20.6 bar is partly hidden by the red AC marker; extracted from its visible part (confidence 2). |
| 1450m2/g | 12 | 9 | 2 merged markers near 2.8-3.4 bar; 1 marker near 1.2 bar merged with a 1259m2/g marker. |
| 1259m2/g | 12 | 8 | 3 merged markers near 2.3-3.4 bar; 1 marker near 1.7 bar merged with a 1450m2/g marker. The marker near 1.25 bar touches neighbouring markers (56 px blob; confidence 2). |
| 650m2/g | 14 | 7 | 7 markers of the low-pressure staircase (about 0.9-3.5 bar) merged into one blob. |
| 370m2/g | 14 | 7 | 7 markers of the low-pressure staircase (about 0.9-3.5 bar) merged into one blob together with y-axis markers. |

Also not extracted from Figure 4: one clean black marker near 0.93 bar, 2.22 wt% (combined-run index 6) that lies on both the 2300m2/g and 1730m2/g traces, so its curve cannot be determined; and the merged or fragmentary black blobs along the y axis below about 1.9 wt% (combined-run indices 0-5), which hold the lowest-pressure points of several curves.

## Values seen but not extracted

- Abstract: "hydrogen storage by graphene materials do not exceed 1 Wt% at 120 Bar H2 at ambient temperatures": a bound over all samples, not a value for one sample.
- Introduction (main-03): literature values from other papers (about 0.3 wt% per 1000 m2/g and at most about 1 wt% at ambient temperature and 100 bar; 4-7 wt% at liquid-nitrogen temperature [3, 10]; 3.1 wt% at 100 bar for 925 m2/g [17]; 0.7 wt% for 640 m2/g at 100 bar [18]; 0.9 wt% for 2139 m2/g at 100 bar [19]): not measurements of this paper.
- Section 3.1 (main-08): annealing of exfoliated HGO in pure H2 at 50 bar and 400 °C for 24 h gave "rather slight increase of hydrogen adsorption by ~10%": a relative change with no uptake value.
- Section 3.2 (main-08/09): "limits maximal adsorption values to ~0.8-0.9 Wt% at ~3000 m2/g": a value read from the fitted trend, no sample.
- Section 3.2 (main-09): two samples degassed at up to 300 °C "showed negligible increase in hydrogen uptake values": no values.
- Discussion (main-10): uptakes "about 3-4 times lower" than [18] and "about six times lower" than [22]: ratios, no values.
- Figure 2 (main-16): uptake against BET surface area, not an isotherm, so not digitized. It shows values the text does not give: 293 K, 120 bar, gravimetric points for FLG, samples 1-4 (rHGO), 5-6 (rBGO), 7-11 (KOH-activated rHGO), commercial mesoporous carbon (MC) and activated carbon (AC); sample 7 also at 274 K (point 7a); three MOF-5 samples (not carbon sorbents) and two Pt/AC samples measured at 288 K in the authors' earlier study [48] (previously reported). The curves of Figure 3 are said to be the isotherms of "several samples" of Figure 2, but the paper does not say which, so the Figure 3 curves keep their own labels.
- Figure 5 (main-18): uptake against BET surface area, not an isotherm, so not digitized. It shows, by volumetric method, 77 K values ("50 Bar") for samples 1-3 (r-HGO), 4-5 (r-BGO), 6-11 (KOH-activated r-GO) and AC; 293 K values (120 bar) for samples 1, 2, 4, 8, 9, 10, 11 and AC; and 274 K values for samples 5, 6 and 7. The sample numbers differ from those of Figure 2 and the paper gives no mapping to the Figure 4 curve labels, so none of these values is linked to a Figure 4 isotherm.
- Figure 1 (main-15): TGA of the Brodie and Hummers graphite-oxide precursors (weight losses 27.8% and 27.2%, DTG peaks at 284.2 °C and 220 °C): no H2 data.

## Characterization without H2 uptake (no rows)

- Graphite-oxide precursors: Brodie GO C/O 2.7 (XPS), (001) d-spacing 6.3-6.6 Å; Hummers GO from ACS Materials C/O 2.47; Hummers GO from Alfa Aesar and Kropfmühl graphite C/O about 2.5 (XPS); GRAnPH Hummers GO from GANF nanofibers.
- Exfoliated products: BGO up to about 850 m2/g; HGO at most about 450-500 m2/g; reduced GRAnPH HGO up to 311 m2/g; KOH-activated samples 1000-2300 m2/g. No pore volumes are reported numerically for any sample.

## Coding decisions

- Sample labels: the curve labels as printed in the figure that carries the extracted values ("1740 m²/g" etc. in Figure 3 with a space, "1730m²/g" etc. in Figure 4 without). The 2300 m2/g sample of the abstract is the "2300m²/g" curve of Figure 4. The reference activated carbon is labelled "AC" as in Figure 2, its first appearance; the captions of Figures 3 and 4 call the red curve the "reference sample of activated carbon". Figure 3 "1740 m²/g" and "1250 m²/g" and Figure 4 "1730m²/g" and "1259m²/g" are kept as separate samples because the paper prints different areas and does not say they are the same samples.
- Gravimetric rows: basis_inferred = unknown and calibration_described = false, because the paper does not state a buoyancy correction (it says only that FLUIDCAL was used to calculate fluid densities of H2 and He). The ± 0.02 wt% instrumental precision is recorded as uncertainty_wt_pct with replicates_reported = true.
- area_same_sample = yes for the authors' graphene samples (with a note that the paper does not say whether the printed area was measured before or after the H2 run), unclear for AC.
- The KOH-activated or exfoliated-only status of each sample, and its precursor, is inferred from its surface area and the paper's stated area ranges; this is noted in material_description.
