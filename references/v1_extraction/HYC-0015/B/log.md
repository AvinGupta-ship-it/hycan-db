# HYC-0015 extraction log (agent B)

Input: 20 page images of the main article (main-01 is a repository cover page); no supplementary file. No tables in the paper.

## Passages and figures extracted from

- Abstract, p.1 (main-02): GO 1.90 wt% and rGO 1.34 wt% "at room temperature", "pressure up to 80 bars". Same measurements as rows M1 and M2.
- Introduction, p.4 (main-05): "storage capacity (1.34 wt. % to 1.90wt. %)". Same measurements as M2 and M1.
- Section 2.1, p.4-5 (main-05, main-06): synthesis of GO (modified Hummers' method) and rGO (hydrazine hydrate reduction). Used for material description and synthesis_method.
- Section 2.3, p.5-6 (main-06, main-07): home-built ("indigenous fabricated") Sieverts apparatus up to 80 bar, schematic Fig. 1; degassing "under rotary vacuum (10-2 tor) at room temperature"; "volumes of sample cells ... precisely measured for calibrations"; "exposing the samples to hydrogen gas at pressure 80 bar for six times". Used for method fields on M1 and M2.
- XRD text, p.10 (main-11): GO interlayer spacing 8.84 A (2theta 9.96 deg), rGO 3.85 A (2theta 23.72 deg). Stored in interlayer_spacing_nm on M1 and M2.
- FTIR text and Fig. 7, p.12-13 (main-13, main-14): O-H, C-O, C=O bands. Stored in functional_groups.
- Hydrogen Storage Performance, p.13 (main-14): "The rGO absorbs a small amount of molecular hydrogen1.34 wt% at 80 bar"; GO "at same pressure". Row M2 (rGO); pressure for M1.
- Results text after Fig. 8, p.14 (main-15): "The increase H2 uptake (1.90wt%)capacity of GO". Row M1 (GO).
- Conclusion, p.14 (main-15): "about to 1.90 wt. % and 1.34wt. %, respectively at room temperature". Same measurements as M1 and M2. The results section prints both values without a qualifier, so uptake_bound = exact.

## Figures not digitized

- Fig. 8, p.13 (main-14), "Hydrogen uptake by graphene oxide and reduced graphene oxide": hydrogen absorption (wt%) against time (s), 0-5000 s. The text calls it an isotherm, but the x-axis is time, so it is a kinetics plot and is not digitized. Each series has 12 markers after a shared point at the origin, then a horizontal line without markers to 5000 s. The intermediate time-resolved uptake values are not given in the text and were not extracted. The final markers correspond to the text values 1.90 wt% (GO) and 1.34 wt% (rGO) according to the text. Flag for the reconciler: the rGO end marker was not checked against 1.34 wt% because the figure is not digitized.
- Fig. 1 (apparatus schematic), Fig. 2 (SEM), Fig. 3 (TEM), Fig. 4 (XRD of graphite), Fig. 5 (XRD of GO, H-GO, RGO), Fig. 6 (Raman), Fig. 7 (FTIR): no H2 uptake values.
- digitizations/ is empty because the paper has no uptake-vs-pressure isotherm figure.

## Values seen but not extracted

- Literature values cited in the Introduction, p.3 (main-04), measured by other papers and not in this paper: graphene about 1.2 wt% at 10 bar and 77 K, and 0.1 wt% at 298 K [18]; MWCNT 0.9 wt% and GO 1.2 wt% at room temperature and 5 MPa [19]; GO 0.2 wt% at 77 K and 1 bar, and at room temperature [21]; GO 4.8 wt% at 77 K and 0.49 wt% at 298 K, 9 MPa [22]; GO wrapped with V2O5 1.36 wt% and with TiO2 1.26 wt% at 7 MPa and 77 K [23]; graphene specific surface "2630 cm2/gm" [13, 14]; DOE targets 6.0 wt% and 45 gH2/l (2010), 9.0 wt% and 81 H2/l (2015) [11].
- Introduction, p.2 (main-03): 800 bar, 88.89 m3 and 33 K for high-pressure and liquid storage. These are not uptake values.
- Graphite starting material, p.9 (main-10): XRD (002) at 2theta 26.32 deg, interlayer spacing 3.39 A. This is a parent material with no H2 uptake, so it gets no row.
- H-GO (GO exposed to H2 at 1000 mbar, in situ XRD), p.10 (main-11): (002) at 2theta 12.20 deg, interlayer distance 7.1 A. This is not a separate sorbent sample and has no uptake value, so it gets no row. The text calls it "hydrogenated rGO" in one sentence and "hydrogenated graphene oxide" elsewhere. The Fig. 5 caption says "GO exposed to hydrogen gas".
- Raman, p.11-12 (main-12, main-13): GO D and G bands at 1355 and 1605 cm-1, rGO at 1340 and 1586 cm-1; ID/IG about 0.36 (GO) and about 0.77 (rGO); GO 2D band at 2623 cm-1; I2D/IG about 0.75, corresponding to 5-7 layers. The schema has no field for these.
- TEM, p.8 (main-09): hexagonal lattice "distance" about 10.35 nm and layer thickness about 5 to 8 nm (GO). The schema has no field for these.
- No surface area (any method), pore volume or pore diameter is reported for any sample, so surface_area_method = none on both rows. This bears on eligibility criterion I4.

## Coding decisions

- Labels: "GO" and "rGO", as in the Fig. 8 legend (the first legend that shows their uptake) and the text. Fig. 5 prints "RGO".
- Temperature is stated only as "room temperature": temperature_k is empty and temperature_unstated = true.
- No isotherm_id: each sample has a single printed value, and the paper has no uptake-vs-pressure curve.
- measuring_lab_id: the corresponding author marked * is Rajaura, whose first affiliation is the University of Rajasthan.
