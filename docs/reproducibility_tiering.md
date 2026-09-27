# Reproducibility Tiering

## Purpose
Every measurement in HyCAN-DB carries a reproducibility tier (A–D) recording how completely and credibly the source paper reported it. The tier is a disclosure, not a verdict on the underlying material: a low tier flags weak reporting or physical implausibility, not necessarily a wrong result. Tiers let downstream meta-analyses weight or filter by reporting quality and let readers audit the corpus.

## Why tiering matters for hydrogen in carbons
The carbon hydrogen-storage literature has a documented reproducibility problem. Around 1998–2005 several papers reported very high room-temperature uptake (roughly 5–14 wt%) on carbon nanotubes; later reproduction attempts largely failed, and critiques (e.g., Yang 2000) drove a consensus that room-temperature physisorption on pure carbons is bounded near ~1 wt% at 100 bar, and that high 77 K uptakes require correspondingly high surface areas. A database that scored an unreproduced high-uptake room-temperature claim identically to a fully characterized modern measurement would misrepresent the field. Tiering encodes that asymmetry explicitly.

## Three layers of reproducibility
1. Methodological — could another lab repeat the measurement from the paper's description (synthesis, purification, surface area, instrument, T, P, equilibration, sample mass, blank correction)?
2. Numerical — has an independent lab obtained a comparable value on a comparable material?
3. Physical — does the value fall within what physisorption allows for the stated surface area and conditions?

## The 10-point rubric
Score each criterion, sum, then map to a tier.

| Criterion | Points |
|---|---|
| BET surface area reported and consistent with material class | 0–2 |
| Measurement method clearly described (instrument, protocol) | 0–2 |
| Temperature and pressure both clearly stated | 0–1 |
| Uptake type (excess / absolute) explicitly stated | 0–1 |
| Sample purity / impurity content reported | 0–1 |
| Calibration or blank correction described | 0–1 |
| Value within Chahine-consistent range for the stated conditions | 0–2 |

Tier mapping:
- Tier A (9–10) — Highly reproducible. Use as anchor points.
- Tier B (6–8) — Reasonably reproducible. Use in primary analysis.
- Tier C (3–5) — Limited reproducibility. Include but interpret cautiously; report meta-analysis sensitivity with and without.
- Tier D (0–2) — Poor reproducibility OR inconsistent with established physics. Include with an explicit flag; never aggregate with higher tiers without showing the comparison separately.

Categorical override: a value that is inconsistent with established physics (for example, room-temperature uptake far above the ~1 wt% physisorption bound) is Tier D regardless of the additive score. The additive score can only raise a paper; the physics-inconsistency clause can cap it at D.

## Note on the current corpus

*Updated 2026-09-25 against a 206-row, 21-paper corpus. The paragraph this replaces was written when every row in the dataset reported `uptake_type = unspecified` and is no longer true.*

183 of 206 rows report `uptake_type = unspecified` and forfeit the "uptake type explicitly stated" point; the maximum achievable score for those rows is 9. 23 rows across the corpus do state a type (`excess`) and can reach 10. Tier A remains uncommon — 36 of 206 rows — and reaching it on an `unspecified` row requires full marks on BET, method, purity, calibration, and Chahine-consistency simultaneously.

Current distribution: 36 A, 124 B, 38 C, 8 D.

## Documented limitation — the rubric assumes physisorption

**This limitation was specified in execution-manual v2.0 §13.4 and recorded there as written into this document. It was not written until v2.3. It is recorded here now, and the gap itself is disclosed because a limitation the project believed it had disclosed and had not is a worse failure than the limitation.**

The seven criteria above are calibrated for physisorptive hydrogen uptake on porous carbons. Applied to metal-decorated, spillover, and non-isothermal systems, the rubric penalizes papers for not reporting quantities their mechanism does not depend on, and rewards them for reporting quantities that do not mean what the criterion assumes.

Two cases in the corpus, of different shapes:

**HYC-0027 (Parambhath et al. 2012)** — Pd-decorated reduced graphene oxide, hydrogen spillover. Its uptake is governed by catalyst dispersion and hydrogen migration from the metal to the carbon support, not by surface area. It is scored against BET consistency and Chahine agreement, neither of which is the operative physics. It landed at Tier C with four of its five lost points attributable to this rather than to any deficiency in its reporting.

**HYC-0029 (Chen et al. 2008)** — Co-loaded carbon nanofibers. Its reported hydrogen quantities are not isotherm points at all; they are sample weight differences measured across a 303 → 673 → 303 K temperature cycle. The Chahine criterion has nothing to say about such a value. The temperature-and-pressure criterion awards its point for conditions that are stated clearly and that describe a cycle rather than an equilibrium. Its rows landed at Tier B and C by a rubric that was not measuring them.

**The resolution is disclosure, not rescoring.** A tier is a statement about one specific kind of reproducibility. Rescoring spillover and non-isothermal papers upward — or downward — would make the letter mean two different things depending on the row, which is worse than a letter that means one thing imperfectly. The scores stand as assigned.

Two options for a future schema revision, to be evaluated in Phase E when the meta-analysis makes the cost of the present approach visible:

- a mechanism-aware second rubric, scored alongside the physisorption rubric; or
- a `tier_basis` field recording which rubric a row's tier was assigned under.

Neither is adopted yet. Until one is, any analysis that aggregates across mechanisms should report its result with and without the spillover and non-isothermal rows, and say which rows those are.

**A code defect this document recorded, now FIXED (2026-09-27, `docs/migration_score_reproducibility_plan.md`).** Since schema v1.2 made `temperature_k` optional on rows whose paper never stated a temperature, `score_reproducibility` returned "cannot assess" (1 of 2 points) for the Chahine criterion on every such row, so the six rows with a null temperature collected a point for a check that never ran — including all four of HYC-0011's, which meant its ordinary 0.26 wt% and its discredited 8.0 wt% received identical Chahine scores and both suggested Tier C.

One branch was reading three different situations as one, and separating them is the fix. A row with **no uptake of any kind** keeps the point: the criterion has no subject and that is not a reporting failure. A row whose uptake is **not convertible to wt%** — HYC-0024's ten volumetric-only rows — keeps it too: the Chahine rule is defined in wt% and this genuinely cannot be assessed. A row reporting an uptake in wt% whose **paper never stated a temperature** now scores **0**, because the criterion reads "within Chahine-consistent range for the stated conditions" and there are none. That is a reporting deficiency and it scores as one. HYC-0011-M4 now suggests Tier D, matching its assigned tier; the free point had been the only thing holding it above it.

`suggest_tier` may now be used on a row carrying a `*_unstated` flag. Three further defects in the same function were fixed in the same commit — see the blind-spot list below, which is shorter than it was.

## suggest_tier is a suggestion only
`suggest_tier(row)` in `src/hycan/validate.py` applies this rubric to the fields present in a row and returns a suggested letter. It is an approximate scorer and the human extractor makes the final call. It cannot see everything the rubric asks about:
- It confirms a measurement method is recorded but cannot judge whether the paper "clearly described" the instrument and protocol; downgrade by a point if the method was only named. Worked examples 2 and 3 below both hand-score this 1 where the code scores 2.
- "Calibration or blank correction" has no schema field; the scorer cannot award it and always scores it 0. Add the point by hand when the paper describes it. **The code ceiling is therefore 9, not 10**, and no row with an `unspecified` uptake type can be suggested Tier A.
- The Chahine-consistency check is a coarse physical-plausibility heuristic that flags over-claims; it does not replace judgment and cannot apply the categorical physics override — you do. Its 77 K bound also ignores pressure: BET/500 is the rule's form at moderate pressure, so a row at 77 K and 1 bar clears it trivially.
- **A characterization-only row is scored as though it were a failed uptake measurement.** The rubric grades the reporting quality of an uptake measurement and such a row has none, so it collects points only for characterization and lands at Tier C or D however well the paper reports it. HYC-0007's four such rows suggest D against an assigned B. They inherit their paper's tier instead.
- A surface area whose method the paper never stated is still accepted as a Chahine bound, though §10.3 of the manual permits uptake-per-m² only for BET areas. The tier criterion is a sanity bound rather than a published statistic, so an area of unknown method is better than none — but the two rules are inconsistent and that is recorded rather than resolved.

**"Sample purity" is no longer proxied only by a purification method.** It was, and HYC-0007 showed what that cost: its pristine SWCNT scored 0 while the paper reports 11 wt% residual metal for it, and its acid-treated sample scored 1 for having been treated — the scorer rewarding the treatment and ignoring the measurement. A reported `residual_metal_wt_pct` or `residual_metal_element` now earns the point, with the purification proxy kept behind them, so the change can only ever turn a 0 into a 1.

**The BET criterion now uses the three-level scale worked example 2 below always specified.** 2 points for an area whose `surface_area_method` is `BET`; 1 for an area of another or unstated method, for a Langmuir area, or for a paper that reports resolved micropore and external areas with no total; 0 for no area at all. The code previously awarded 2 for any positive `bet_surface_area_m2_g` and 0 otherwise, which scored 0 for HYC-0007's eighteen reported surface-area values and 2 for the 31 rows whose area this project had already recorded as not known to be BET.
When `suggest_tier` and your rubric judgment disagree, your judgment governs and the reason is recorded by the extractor. That disagreement is the point of keeping a human in the loop.

## Worked examples

### Worked Example 1 — Tier A (modern, full reporting)
A recent activated-carbon study reports BET ≈ 2600 m²/g (plausible for a high-surface-area activated carbon), hydrogen uptake measured on a Sieverts-type volumetric instrument with stated equilibration time and void-volume/blank correction, at 77 K and 20 bar, with excess uptake stated explicitly, ash/impurity content reported, and a measured ≈ 4.8 wt% against a Chahine expectation of ≈ 5.2 wt% (2600 / 500).
Scoring: BET 2, method 2, T&P 1, uptake type 1, purity 1, calibration 1, Chahine 2 = 10 → Tier A. (suggest_tier scores this 9, lacking the calibration field; the human awards the tenth point. It reaches 9 only because the row's `surface_area_method` is `BET` — the same area as `unspecified` scores 8.)

### Worked Example 2 — Tier C (older, partial reporting)
An early-2000s porous-carbon paper reports a surface area of ≈ 1800 m²/g given as a Langmuir (not BET) value, hydrogen uptake at 77 K and 1 bar by a volumetric method that is named but whose protocol is not described, no statement of excess vs absolute, no purity or ash data, no explicit blank-correction description, and a value (~2 wt%) that is physically plausible for the conditions.
Scoring: BET 1 (surface area reported but not BET), method 1 (named only), T&P 1, uptake type 0, purity 0, calibration 0, Chahine 2 = 5 → Tier C. (suggest_tier now matches this example's BET and purity points and still reaches Tier C, differing on two criteria it cannot judge: it scores method 2, and it scores Chahine 1 rather than 2 because the only area present is Langmuir and it refuses to bound against one — a Langmuir fit over-reads on a microporous carbon, so using it would loosen the check in the direction that hides an over-claim. The 2 here is awarded on physical plausibility, which is a judgment, not a computation.)

### Worked Example 3 — Tier D (extraordinary uptake exceeding physical bounds)
A late-1990s/early-2000s paper reports high room-temperature uptake — about 6 wt% at 298 K and ~100 bar — on raw or lightly treated carbon nanotubes, with no reported surface area, a volumetric measurement whose blank/buoyancy correction is not detailed, and no statement of excess vs absolute. Room-temperature physisorption on pure carbons is bounded near ~1 wt% at 100 bar, so the value is inconsistent with established physics.
Scoring: BET 0, method 1 (named only), T&P 1, uptake type 0, purity 0, calibration 0, Chahine 0 (value far exceeds the room-temperature bound) = 2 → Tier D. The categorical physics-inconsistency clause independently places it at Tier D. (suggest_tier totals 3 and suggests Tier C, agreeing on BET 0 and Chahine 0 but scoring the named-only method as 2; the human downgrades to D under the physics clause — the intended human-in-the-loop correction. Note that if this row's paper had also failed to state its temperature, the scorer would now total 2 and suggest D by itself, which is the HYC-0011-M4 case.)
Per the ethical principle below, this entry is retained with its flag because it documents the field's contested history; it is never aggregated with higher-tier data without showing the comparison separately.

## Ethical principle
Tiering is disclosure, not deletion. A Tier D entry has scientific value precisely because it records the field's contested history. Removing such entries would be revisionist; including them without a flag would be misleading. The tier is the disclosure.

## Applied tiers
Per-row tiers are stored in the `reproducibility_tier` column of `data/raw/measurements_v0.1.csv`, which is the source of truth. Each assignment is the extractor's final call, informed by `suggest_tier` and this rubric.
