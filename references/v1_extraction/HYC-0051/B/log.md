# HYC-0051 extraction log (agent B)

Tibbetts, Meisner, Olk, Carbon 39 (2001) 2291-2301. 11 page images (main-01 to main-11), no supplementary file. 14 rows written.

## Sources extracted from

- Table 1 (main-08, p. 2298), "Hydrogen capacities measured for various carbons at 23°C": 8 carbon values in the "PCI system (3.59 MPa)" column (M1-M4, M6, M8, M10, M11) and 3 upper bounds in the "High pressure manual system (11 MPa)" column (M5, M7, M9).
- Text p. 2297-2298 and Fig. 13 caption (main-07/08): "it sets an upper limit on hydrogen sorption of 0.5 wt.%" for air-etched PYROGRAF in the high pressure manual system. Same measurement as Table 1 "<0.5", so it is merged into M7 (one row).
- Fig. 11 (main-07, p. 2297), curve "C6Hx": highest-pressure point digitized (M12, isotherm I1). Archive: digitizations/HYC-0051_fig11_c6hx.json.
- Fig. 14 (main-08, p. 2298), series "Difference", plus text p. 2298 ("the total hydrogen sorption is quite small, of the order of a tenth of a wt.%"): text value merged with the digitized highest-pressure point (M13, isotherm I2). Archive: digitizations/HYC-0051_fig14_difference.json.
- Text p. 2298 ("corresponds to a hydrogen release less than 0.1 wt.%") and Fig. 15 caption (main-09): MER nanotubes desorption on heating to 500°C after exposure to 3.60 MPa (M14, TPD, upper bound).
- Section 2.1 (main-01 to main-04): sample identities, treatments, the activated-carbon surface area (about 700 m2/g, on M2), and the 350°C / 3 h heating of the CO2-etched fibers before loading (degas fields on M9).
- Section 2.2 (main-04 to main-07): apparatus descriptions used for the instrument and calibration codes.

## Digitization

- Fig. 11 (main-07): x linear, 0 at px 212.0 (tick below axis), 7 at px 609.0, check tick 4 at px 439.25 (relative error 0.17%). y log10, 0.01 MPa at px 1271 (bottom axis), 10 MPa at px 1002 (top frame), check tick 1 at px 1091 (relative error 1.7%). Colour #000000, tolerance 80, no opening, ROI x 219-230, y 1038-1044, which holds only the top marker (rows 1040-1044). 1 marker extracted, 1 counted in the ROI. Result: x = 0.2082 (C6Hx), P = 3.567 MPa. The tool's stated-value check against the PCI maximum pressure 3.59 MPa (Table 1 header) passed.
- Fig. 14 (main-08): x linear, 0 at px 727 (left axis line), 0.12 at px 1100 (right axis line), check tick 0.06 at px 914.5 (mean of the inner ticks at the top, px 915.0, and bottom, px 914.0; relative error 0.54%). y linear, 0 kPa at px 1239 (bottom axis), 4000 kPa at px 1033.5 (top frame), check tick 2000 at px 1136.5 (relative error 0.24%). Colour #8c8c8c, tolerance 70, no opening (a 3-px opening erases the open-triangle outlines), ROI x 754-769, y 1048-1057, holding only the top triangle. 1 marker extracted, 1 counted. Result: x = 0.01082 (CHx), P = 3591 kPa. The check against 3590 kPa passed.
- Both scans are slightly rotated (about 1-2 px across the plot frame); the check-tick errors above include this.
- Marker counts for isotherm_point_count are approximate. Fig. 11 C6Hx: about 39 filled circles on both branches, many overlapping one another and the left axis, and near 0.1-0.3 MPa mixed with LaNi5 squares. Fig. 14 Difference: 25 triangles separable, plus about 7 stacked and overlapping near the origin (32 recorded). These overlapping markers could not be separated by the tool. Only the highest-pressure point of each is required (non-77 K isotherms), so the counts affect only isotherm_point_count.

## Coding decisions

- Samples are numbered in order of first mention, which is the abstract's list: S1 graphite, S2 activated carbon, S3 graphitized PYROGRAF, S4 CO2-etched PYROGRAF, S5 air-etched PYROGRAF, S6 Showa Denko VGCF, S7 FeNiCu filaments, S8 MER nanotubes, S9 Rice nanotubes. Labels are taken from Table 1. "CO2" is written in ASCII; the paper prints a subscript 2.
- Table 1 rows have no isotherm_id. Each is the only value from its run. Graphitized and air-etched PYROGRAF each have two 23°C values, but they come from different apparatus (different runs), and no curve is plotted at 23°C.
- Fig. 11 sample: the figure title and caption say "Air-etched PYROGRAF"; the text (p. 2297) says "graphitized PYROGRAF". It is assigned to air-etched (S5), with the conflict noted on M12 and extraction_confidence 2. Its temperature is not stated, so temperature_unstated = true. No table value is merged with it: its temperature is not established, and it is evidently not background-corrected (about 0.29 wt.% against 0.070 / 0.020 wt.% in Table 1).
- Units of Fig. 11 and Fig. 14: the abscissa is H atoms per C6 (C6Hx) or per C (CHx), and no schema field or §11.0 factor covers this. M12 stores W1 = 100·x·1.00794/(6·12.0107), coded computed_from_other_unit, with the printed quantity in the notes. M13 avoids the conversion because the text prints a wt.% value; its digitized x is in the notes.
- FeNiCu: Table 1 gives 0.066 wt.% at 23°C, while Fig. 14 is at 25°C (caption). The paper does not tie this specific table value to Fig. 14, and the printed temperatures differ, so they are kept as separate rows (M11 without isotherm_id, M13 with I2).
- Instruments: the high pressure manual system is coded instrument_identified = true, because it is described with a schematic (Fig. 8) and contrasted with the "commercial" second system. Its calibration_described = true (high-pressure He calibrates the final sample-space volume). The Gas Reaction Controller (Advanced Materials Corporation) is coded true, with the product name taken as the model. Its calibration_described = false: the empty-chamber PCI subtraction is described, but the free-volume determination is not.
- Basis: never named. Volumetric rows are basis_inferred = excess by the instrumental default. The TPD row is basis_inferred = unknown.
- Activated carbon area: "generally has a surface area only around 700 m2/g". This is a generic value, not measured by the authors. It is recorded as 700, surface_area_method = unspecified, probe gas unspecified, area_same_sample = other_paper. All other samples have surface_area_method = not_reported.
- MER nanotubes are coded MWCNT, following the authors' belief; the manufacturer specifies 10-15% SWNT.

## Values seen but not extracted

- Table 1, La0.93Ni5 / LaNi5: 2.0 wt.% (manual system) and 1.5 wt.% (PCI). Nd2Fe14B: 0.19 wt.% (PCI). Metal-alloy calibration standards, not carbon sorbents.
- Text p. 2295 and Fig. 11: LaNi5Hx, x of approximately 6.5 (1.5 wt.%). Metal hydride calibration, not carbon.
- Text p. 2295 and Fig. 12: Nd2Fe14B, 3.18 g, heated to 475 K in 120 kPa H2, cooled to 297.6 K, ΔP ~15 kPa in 1.049 L, 2.98×10^-3 mol H2, 6.0×10^-3 g H, 0.19 wt.%. Not carbon.
- Fig. 9 (main-06): La0.93Ni5 pressure and temperature against time. Not carbon, not an isotherm.
- Fig. 11 LaNi5Hx curves: not carbon. Fig. 11 C6Hx points other than the highest-pressure one: a non-77 K isotherm, so only the highest-pressure point is digitized.
- Fig. 13: pressure against time for air-etched PYROGRAF. Not an isotherm. Its result (0.5 wt.% upper limit) is in the text and table (M7).
- Fig. 14 "Sample" series (chamber plus sample, uncorrected) and "Empty" series (empty chamber): not extracted. The paper states that the Difference curve is the corrected PCI for the filament sample, and the empty chamber is not a sorbent. The other Difference points are not digitized (non-77 K isotherm).
- Fig. 14 caption: "a final x for both the empty chamber and the chamber + sample of 0.0085, or 0.07 wt.%". This is a hysteresis residual that the paper attributes to gauge miscalibration, for both the empty and the loaded chamber, so it is not a sorption value. By the axis calibration, the plotted desorption end points lie near x = 0.085, a factor of 10 from the caption. This is not reconciled.
- Fig. 15: pressure rise against temperature. Not an isotherm. Its value is in the text (M14).
- Fig. 16: empty chamber, and data of Fan et al. [8] and Liu et al. [19]. No sorbent from this work, or other papers' data.
- Abstract: "The largest sorption observed is less than 0.1 wt.% hydrogen at room temperature and 3.5 MPa". A summary across samples, not a per-sample value; consistent with the Table 1 PCI values.
- Text p. 2298: "each material tested in the Gas Reaction Controller was exposed to hydrogen at 3.6 MPa while heating to 500°C. No additional hydrogen uptake was observed". No number. The order of this treatment relative to the Table 1 values is not stated.
- Text p. 2297: the LaNi5 hysteresis "is as large as the total sorption observed in the graphitized PYROGRAF sample". No number.
- Abstract and conclusions: "very little hydrogen sorption", "none ... appreciably above background", "claims ... larger than a 1 wt.%". No per-sample values.
- Introduction (p. 2291), cited values from other work: up to 70 wt.% nanofibers [3]; less than 1 wt.%; 0.25 wt.% nanotubes [6]; 1 wt.% filaments [7]; 13 wt.% nanotubes [8]; metal hydrides below 3 wt.%; 6.5 wt.% target [2].
- Discussion (p. 2299-2300), cited values or hypothetical calculations: Zhu et al. [16], 1-5 wt.% for samples of 0.16-0.8 g, R² 0.997; 33.3 kPa/K at 10^4 kPa and 300 K, "2.6 wt.% per degree temperature drop" (hypothetical); 41% adiabatic temperature rise; Chahine and Bose [21], 0.6 wt.% on AX-21 at 6 MPa ("298°C" as printed); Zhou and Zhou [15], 0.5 wt.%.
- Enthalpies of 31 kJ/mol (LaNi5) and 4 kJ/mol (activated carbon, [15]): not uptake values.

## Characterization seen (not in numeric fields)

- Activated carbon: "relatively low mesopore volume" (no number). The VGCF area is implied as about 1/70 of the activated carbon's [10], but no number is printed.
- Showa Denko VGCF diameters averaging 200 nm; Rice nanotube bundles near 14 nm; MER material 10-15% SWNT per the manufacturer; FeNiCu catalyst Fe:Ni:Cu = 85:10:5. These are fiber or bundle sizes, not pore sizes, and are kept in material_description.
- Sample masses: "0.3-1.0 g we can load in the sample chamber" (PCI, a range, not per sample; not recorded). Fig. 13: 0.77 g (recorded on M7).
- Manual system: "The sample space could be heated to about 500°C ... to outgas or otherwise activate the samples". This states a capability, not a protocol for any sample, so no degas values are recorded from it.
