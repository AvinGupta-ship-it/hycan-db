# Extraction log: HYC-0051 (Tibbetts 2001, Carbon 39:2291), extractor A

Inputs read: text layer and page images 1-11 of the main article. No supplementary files. No figure was digitized, so `digitizations/` is empty.

## Extracted

- Table 1 (p. 2298), High pressure manual system (11 MPa) column: La0.93Ni5 2.0 (M1), Graphitized PYROGRAF <0.7 (M8), Air etched PYROGRAF <0.5 (M10), CO2 etched PYROGRAF <0.2 (M12). Bounds are coded `uptake_bound = upper`.
- Table 1, PCI system (3.59 MPa) column: LaNi5 1.5 (M2), Nd2Fe14B 0.19 (M3), Graphite flakes 0.018+/-0.011 (M4), Activated carbon 0.041+/-0.014 (M5), MER nanotubes 0.028 (M6), Rice nanotubes 0.050 (M7), Graphitized PYROGRAF 0.020 (M9), Air etched PYROGRAF 0.070 (M11), Showa Denko VGCF 0.042 (M13), FeNiCu filaments 0.066 (M14).
- Section 3 text and Fig. 15 caption (p. 2298-2299): MER nanotubes "hydrogen release less than 0.1 wt.%" on heating to 500 C after 3.60 MPa exposure (M15). Desorption upper bound, coded TPD, confidence 2. Included on the literal "every H2 uptake value in text" scope; reconciliation may drop it as a release figure rather than an uptake.
- Section 2.1.1 text: "around 700 m2/g" surface area recorded on the Activated carbon row (M5) only, `surface_area_method = unspecified`, `area_same_sample = unclear` (stated generically for the carbon type, citing [10]). All other rows are `not_reported`.

## Coding decisions worth a second look

- Non-carbon rows: La0.93Ni5 (M1), LaNi5 (M2) and Nd2Fe14B (M3) are metal hydride and magnet calibration references, not carbon sorbents under section 3. They are included because Table 1 prints them and the scope says every H2 uptake value in tables; `material_class = other` and the notes flag them. Drop them if the reconciliation rules exclude non-carbon sorbents.
- Table 1 prints one row "La0.93Ni5, LaNi5" with 2.0 (manual) and 1.5 (PCI). Sections 2.1.4 and 3 say LaNi5 was tested only in the PCI system and the manual-system results are for La0.93Ni5, so I split it into two samples.
- Conditions of table rows: T = 23 C (296.15 K) from the Table 1 title. P = 11 MPa (110 bar) and 3.59 MPa (35.9 bar) are the column headers; the paper does not say at which pressure each value was read. Section 2.3 says the manual reservoir was pressurised to approximately 12 MPa.
- Nd2Fe14B (M3): Table 1 puts 0.19 in the 3.59 MPa PCI column, but Section 2.2.2 and Fig. 12 describe a soak-mode test at 120 kPa H2, heated to 475 K, cooled to 297.6 K, 3.18 g sample. I used the text's conditions (297.6 K, 1.2 bar, 3180 mg). The row will not match an extraction that used the table header's conditions.
- FeNiCu filaments (M14): Fig. 14 caption says the PCI was at 25 C, Table 1 says 23 C. Table value and table temperature used.
- Fig. 11 versus text: Section 2.3 says the carbon PCI superimposed on LaNi5 in Fig. 11 is graphitized PYROGRAF; the Fig. 11 title and caption say air etched PYROGRAF.
- Basis: the paper never names excess, absolute or total, so `basis_stated = false`, `uptake_type = unspecified`. Volumetric (Sieverts-type, calibrated volumes) gives `basis_inferred = excess` by the instrumental default; M15 is TPD so `unknown`.
- wt% convention: `unknown` / `none` throughout. The paper defines no convention and prints no per-gram paired unit; for Nd2Fe14B (6.03e-3 g H2 on 3.18 g) W1 and W2 both round to 0.19.
- `value_kind = unclear` on all bound rows (M8, M10, M12, M15), since a bound is not a measured point.
- Sample identity: the same labelled material measured in both instruments shares a `sample_id` (Graphitized PYROGRAF S8, Air etched PYROGRAF S9).
- `doi` is lowercased per the data dictionary (paper.json prints the S uppercase).
- Degassing: only CO2 etched PYROGRAF has a stated pre-loading heating (350 C, 3 h, Section 2.1.3), recorded in the degas fields and flagged as a pre-loading bake. Section 2.2.1's "heated to about 500 C to outgas" is a capability, not a per-sample protocol.
- Sample mass: 3.18 g (Nd2Fe14B, text) and 0.77 g (Air etched PYROGRAF manual row, from the printed label "Sample #1; 0.77g" on Fig. 13). Other samples: only a general "0.3-1.0 g" range, not recorded.

## Seen but not extracted

- Fig. 14 (FeNiCu PCI at 25 C; Sample, Empty and Difference series) and Fig. 11 (C6Hx carbon fiber and LaNi5Hx PCIs). These are room-temperature isotherms, so only each isotherm's highest-pressure point would be in scope. Not digitized for three reasons. (1) Both plot composition as x in CHx, C6Hx or LaNi5Hx, an H:C or H:metal atomic ratio. The instructions allow no conversion from that unit and give it no column, so a digitized point cannot be stored as a valid row without an unsanctioned unit conversion. (2) The Sample curves in both figures are raw controller PCIs that include the empty-chamber background; Section 3 says the sorption reported in Table 1 comes from PCI subtraction, and the Empty series is a blank, not a sample. (3) The LaNi5 isotherm's value (1.5 wt.%, x about 6.5) and the FeNiCu and air etched values are already recorded from Table 1. If reconciliation wants the figure endpoints, they need x converted to wt% by CHx stoichiometry. The Fig. 14 Difference series appears to end near x = 0.01, which would be above the table's 0.066 wt.%; this is a visual impression, not digitized.
- Fig. 14 caption, "final x for both the empty chamber and the chamber + sample of 0.0085, or 0.07 wt.%": a pressure-gauge hysteresis artifact the authors attribute to miscalibration, not an uptake. The plotted hysteresis end appears near 0.08 on the x axis, about ten times the caption's 0.0085; not resolved.
- Section 2.2.2 intermediate quantities for Nd2Fe14B (delta P about 15 kPa, 2.98e-3 mol, 6.03e-3 g, 1.049 L): the same point as the 0.19 wt.% already in M3.
- Section 2.2.2 "x about 6.5 (1.5 wt.%)" for LaNi5Hx: same value as Table 1 (M2).
- Fig. 13 caption and Section 3 "upper limit of 0.5 wt.%": same value as Table 1 <0.5 (M10).
- Abstract "largest sorption observed is less than 0.1 wt.% at room temperature and 3.5 MPa": a summary bound over all samples, not tied to one sample.
- Section 3 "no additional hydrogen uptake was observed" after exposure to 3.6 MPa while heating to 500 C: no number.
- Section 4 "2.6 wt.% per degree temperature drop" for a hypothetical 1 g sample in 1 L at 100 bar and 300 K: an illustration of a thermal artifact, not a measurement.
- Introduction and Discussion literature values (70, 13, 1, 0.25 wt.%; Zhu 1-5 wt.%; Chahine and Bose 0.6 wt.% and Zhou and Zhou 0.5 wt.% at 6 MPa): other groups' results, not this paper's measurements.
- Figs. 9, 12, 13, 15 and 16 are pressure or temperature versus time or temperature traces, not isotherms; Fig. 16 is an empty chamber. Figs. 1-7 are micrographs, Figs. 8 and 10 are schematics.
