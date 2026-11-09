# HYC-0119 extraction log (agent A)

## Extracted from
- main.pdf p.4 Table 2: 1 bar and 30 bar wt%, 30 bar g/L, skeletal density, pore size peaks for CS800-4 and CS850-4.5 (6 rows incl. text repeats).
- main.pdf p.4 Sec. 3.4 text: 2.3 wt% at 1 bar (CS850-4.5; conflicts with Table 2 1.9); 4.5 wt% at 50 bar (also Abstract, Conclusions).
- main.pdf p.2 Table 1: characterization of both samples (carried on every row). Packing densities 0.79 and 0.54 g/cm3 from p.5 text.
- main.pdf p.4 Fig. 4a (77 K, both samples, total and excess): 36 digitized points in 4 archives (digitizations/).
- XPS oxygen contents (p.3 text), FTIR groups, EDS (Fig. 1e) used for composition fields.

## Digitization notes
- Calibration Fig 4a: x 162.5 px = 0 bar, 500.5 px = 30 bar (verified at 15 bar); y 1087.5 px = 0, 813.5 px = 5 wt% (verified at 3 wt%).
- The plot is low-resolution with overlapping hollow (excess) and filled (total) markers. Marker images were derived from the page image (hollow-marker interiors by hole filling; filled markers by morphological opening; same pixel size, saved in work/) and passed to digitize_figure.py markers mode. One spurious fragment on the CS800-4 excess line (x about 410 px) was masked out of the CS800-4 total image.
- Check status: CS850-4.5 total checked against stated 4.3 wt% at 30 bar using the nearest digitized point (27.43 bar, 5% tolerance; 30 bar marker not digitizable). CS800-4 total checked against stated 1.5 wt% at 1 bar (digitized 0.978 bar, 1.427 wt%, 4.9% difference). The two excess series have no stated value in the paper, so their archives stay "unchecked"; extraction_confidence 2 for those rows.
- Markers NOT separated or extracted (overlap, clipping): every 30 bar end-point marker (clipped by right axis); CS850-4.5 total at about 0.1, 0.8, 1.05, 3.4 bar; CS850-4.5 excess at about 3.4 bar and all low-pressure markers hidden under total markers; CS800-4 total and excess below about 7 bar except one total point at 0.98 bar (low-pressure cluster, 3 and 5 bar points overlapped by excess markers); CS800-4 total at 7.1-25.2 bar all found, 8 points. isotherm_point_count values are approximate visible-marker counts.
- Table 2 and text 1 bar values were not matched to a plotted point (none confirmable within 0.02 bar), so they carry no isotherm_id. 30 bar values were matched to the plotted end points (I1, I3) without a digitized: note because the markers could not be digitized.
- Fig. 4a right axis (cm3/g STP) not digitized separately; same curves.
- Fig. 4b (volumetric g/L isotherms): not an H2 gravimetric isotherm in the protocol sense; values shown in the plot that the table does not give were not extracted. Shown curves for MOF-5, Max3 and AC-1 are comparison materials from another paper (ref. 8): not extracted.

## Values seen, not extracted
- CS800-2, CS800-3, CS800-4.5, CS800-5, CS900-4.5 (Table 1): characterization only, no H2 uptake value, no rows. Table 1 values: BET 960/1244/1688/1650/1981 m2/g; Smicro 323/379/622/341/716; Vtotal 0.78/1.06/1.78/1.55/1.45; Vmicro 0.2/0.18/0.56/0.39/0.38; Dave 3.27/3.43/4.22/3.75/2.93 nm.
- Surface oxygen content of CS800-4.5 (17.54 wt%): sample has no H2 value.
- MOF-5, Max3 (Maxsorb 3000), AC-1 (KOH-activated anthracite) in Fig. 4b: from ref. 8, not this paper's measurements.
- Abstract and text repeats of 25.9 g/L (CS800-4), 3.3, 4.3, 1.5 wt%: same measurements as the Table 2 rows, one row each.
- "Optimal operating pressure 25 bar" and "negative excess beyond 25 bar": qualitative, no values.
- Text unit slips noted on rows: Vmicro "1 m3/g", skeletal density unit "cm3/g", BET 2140 vs 2142.
