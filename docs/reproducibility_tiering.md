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

## Note on the current v0.1 corpus
Every row extracted so far reports uptake_type as `unspecified`, so every current row forfeits the "uptake type explicitly stated" point. The maximum achievable score for any current row is therefore 9, and reaching Tier A additionally requires full marks on BET, method, purity, calibration, and Chahine-consistency. Treat Tier A as rare for this corpus until uptake_type is resolved from the sources.

## suggest_tier is a suggestion only
`suggest_tier(row)` in `src/hycan/validate.py` applies this rubric to the fields present in a row and returns a suggested letter. It is an approximate scorer and the human extractor makes the final call. It cannot see everything the rubric asks about:
- It confirms a measurement method is recorded but cannot judge whether the paper "clearly described" the instrument and protocol; downgrade by a point if the method was only named.
- "Calibration or blank correction" has no schema field; the scorer cannot award it and always scores it 0. Add the point by hand when the paper describes it.
- "Sample purity" is proxied weakly by the presence of a purification method; judge it from the paper.
- The Chahine-consistency check is a coarse physical-plausibility heuristic that flags over-claims; it does not replace judgment and cannot apply the categorical physics override — you do.
When `suggest_tier` and your rubric judgment disagree, your judgment governs and the reason is recorded by the extractor. That disagreement is the point of keeping a human in the loop.

## Worked examples

### Worked Example 1 — Tier A (modern, full reporting)
A recent activated-carbon study reports BET ≈ 2600 m²/g (plausible for a high-surface-area activated carbon), hydrogen uptake measured on a Sieverts-type volumetric instrument with stated equilibration time and void-volume/blank correction, at 77 K and 20 bar, with excess uptake stated explicitly, ash/impurity content reported, and a measured ≈ 4.8 wt% against a Chahine expectation of ≈ 5.2 wt% (2600 / 500).
Scoring: BET 2, method 2, T&P 1, uptake type 1, purity 1, calibration 1, Chahine 2 = 10 → Tier A. (suggest_tier would score this 9, lacking the calibration field; the human awards the tenth point.)

### Worked Example 2 — Tier C (older, partial reporting)
An early-2000s porous-carbon paper reports a surface area of ≈ 1800 m²/g given as a Langmuir (not BET) value, hydrogen uptake at 77 K and 1 bar by a volumetric method that is named but whose protocol is not described, no statement of excess vs absolute, no purity or ash data, no explicit blank-correction description, and a value (~2 wt%) that is physically plausible for the conditions.
Scoring: BET 1 (surface area reported but not BET), method 1 (named only), T&P 1, uptake type 0, purity 0, calibration 0, Chahine 2 = 5 → Tier C. (suggest_tier also reaches Tier C here, though it scores the criteria differently — it sees no BET value and a recorded method.)

### Worked Example 3 — Tier D (extraordinary uptake exceeding physical bounds)
A late-1990s/early-2000s paper reports high room-temperature uptake — about 6 wt% at 298 K and ~100 bar — on raw or lightly treated carbon nanotubes, with no reported surface area, a volumetric measurement whose blank/buoyancy correction is not detailed, and no statement of excess vs absolute. Room-temperature physisorption on pure carbons is bounded near ~1 wt% at 100 bar, so the value is inconsistent with established physics.
Scoring: BET 0, method 1 (named only), T&P 1, uptake type 0, purity 0, calibration 0, Chahine 0 (value far exceeds the room-temperature bound) = 2 → Tier D. The categorical physics-inconsistency clause independently places it at Tier D. (suggest_tier would total ~3 and suggest Tier C for this row; the human downgrades to D under the physics clause and by scoring the method as named-only — the intended human-in-the-loop correction.)
Per the ethical principle below, this entry is retained with its flag because it documents the field's contested history; it is never aggregated with higher-tier data without showing the comparison separately.

## Ethical principle
Tiering is disclosure, not deletion. A Tier D entry has scientific value precisely because it records the field's contested history. Removing such entries would be revisionist; including them without a flag would be misleading. The tier is the disclosure.

## Applied tiers
Per-row tiers are stored in the `reproducibility_tier` column of `data/raw/measurements_v0.1.csv`, which is the source of truth. Each assignment is the extractor's final call, informed by `suggest_tier` and this rubric.
