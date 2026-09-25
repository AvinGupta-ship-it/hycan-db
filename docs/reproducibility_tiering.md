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

**A related consequence, recorded separately because it is a code defect rather than a rubric limitation:** since schema v1.2 made `temperature_k` optional on rows whose paper never stated a temperature, `score_reproducibility` returns "cannot assess" (1 of 2 points) for the Chahine criterion on every such row. Fifteen rows across four papers carry a null condition, and the six with a null temperature collect that point for a check that never ran — including all four of HYC-0011's rows, so its ordinary 0.26 wt% and its discredited 8.0 wt% receive identical Chahine scores (both total 3 and suggest Tier C). `suggest_tier` must not be used on a row where `temperature_unstated` or `pressure_unstated` is true; score those by hand. Manual §13.7 has the detail and the fix.

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
