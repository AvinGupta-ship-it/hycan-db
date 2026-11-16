# v1.0 figure captions

Numbers in captions are placeholders by design: every count and estimate is
read from `references/v1_analysis/` at figure-build time
(`scripts/v1_search/figures.py`), and the manuscript captions cite the same
JSON values.

**fig_v1_rq1_ratio.** Maximum excess H₂ uptake at 77 K against BET area for
the RQ1 primary set, one point per sample. The dashed line is the Chahine
rule (1 wt% per 500 m² g⁻¹), the solid line the pooled geometric-mean ratio
from the mixed model, and the band the 95% prediction interval for a new
sample from a new laboratory. Both axes logarithmic.

**fig_v1_rq1_sensitivity.** The RQ1 ratio with its decision 95% CI (the
wider of the t-based and laboratory-bootstrap intervals) for the primary
analysis and sensitivity analyses (i)–(x) and (xii); the shaded band is the
±15% equivalence margin [0.870, 1.150]. Sensitivity (xi), the
leave-one-laboratory-out range, is given above the panel; (xiii), the v0.1
specification, is a slope in different units and is reported in the text.

**fig_v1_rq2_one_bar.** Uptake in the 0.9–1.2 bar window against BET area,
one point per sample (RQ2). The dashed line is the Chahine rule; the solid
line is model (a)'s fit drawn at 1 bar, labelled with the area exponent b.

**fig_v1_rq3_materials.** Interlaboratory dispersion for materials with two
or more laboratories: each laboratory's value divided by the material's
geometric mean, per quantity. Materials with one laboratory for a quantity
are omitted from that panel. The identical kansai-maxsorb-3 values (two
papers from one university) are discussed in
`references/v1_analysis/README.md`.

**fig_v1_rq4_items.** The §7-design-weighted share of eligible papers
meeting each RQ4 reporting item, with Korn–Graubard 95% CIs; the unweighted
count is at the right. Items (b), (h) and (j) are estimated over their §11
domains (papers with a printed wt%, a screenable row, or volumetric data).

**fig_v1_rq5_models.** Pooled out-of-fold R² of the three RQ5 models over
20 GroupKFold-by-paper partitions (bars: mean; whiskers: 2.5–97.5
percentiles across partitions), overall and within the ≤ 1.2 bar and
≥ 10 bar regimes.
