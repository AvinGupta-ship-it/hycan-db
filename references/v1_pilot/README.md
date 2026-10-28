# Prompt pilot on v0.1 papers (protocol §9)

The protocol requires the screening, eligibility, extraction and reconciliation
prompts to be piloted on v0.1 papers only, then frozen in a dated amendment
before reference set B is identified. This directory holds that pilot. None of
its outputs enters the dataset: every v0.1 paper is extracted again under the
frozen prompts (§9).

PDFs, page images and text layers are not redistributed (§8); the agents' inputs
were built from them by `scripts/v1_extract.py prepare`.

## Inputs

- `hycan_v1_lookup_v01_pilot.json`: the OpenAlex records of the 51 v0.1 papers,
  retrieved by `scripts/v1_search/openalex_lookup.js` with every response body
  and its SHA-256. `screen_input.csv` is built from it. OpenAlex holds no
  abstract for 29 of the 51.
- Full texts: HYC-0046 (Kabbour 2006, LLNL author manuscript UCRL-JRNL-227848)
  and HYC-0051 (Tibbetts 2001) in round 1; HYC-0047 (Fierro 2010) and HYC-0060
  (Zlotea 2009) in round 2; HYC-0040 (Flamina 2023) and HYC-0046 again in
  round 3.

## Round 1

Models: screening A `claude-opus-5-5`, B `claude-sonnet-5-5`; eligibility a
`claude-opus-5-5`, b `claude-sonnet-5-5`; extraction A `claude-sonnet-5-5` (text
layer and page images), B `claude-opus-5-5` (page images only); reconciliation
C `claude-opus-5-5`.

- **Screening** (`screen/`): both screeners kept all 51 records. They agreed on
  49 strata. The two disagreements were records whose only 77 K mention was the
  N₂ BET measurement, or whose "high pressure" was pellet compression; the S1
  rule did not say the mention must concern the H₂ measurement.
- **Eligibility** (`eligibility/`): both assessors found HYC-0046 eligible. On
  HYC-0051 they split on I4: its only area is a sentence saying the commercial
  activated carbon "generally has a surface area only around 700 m²/g".
- **Extraction** (`extract/HYC-0046`, `extract/HYC-0051`): 73 matched row pairs,
  96% row-detection agreement, 96% of uptake values within the §9 tolerance,
  every temperature equal. Disagreements concentrated in `isotherm_branch` for
  single values, `surface_area_probe_gas`, `calibration_described`, the
  handling of a table value that is also a plotted point, and extractor A's
  inclusion of non-carbon calibration standards. Agreement statistics:
  `extract/agreement_AB.json`.
- **Reconciliation**: HYC-0051 reproduces all 11 v0.1 values exactly and adds a
  TPD upper bound v0.1 omitted. HYC-0046 reproduces the 9 v0.1 table values and
  adds the five digitized 77 K isotherms; extractor B found that the paper
  states its wt% is W2.
- **Incident.** The HYC-0046 extractors shared the session's scratch folder.
  Extractor A ran a script that extractor B had saved there under the same file
  name, and saw parts of it. A reported this itself (`extract/HYC-0046/A/log.md`).
  Because HYC-0046 is a pilot paper, nothing in the dataset depends on it. From
  now on, every agent gets its own work directory, the prompts forbid shared
  scratch folders, and copies of the dataset were removed from the scratch
  folder.

## Changes made to the prompts after round 1

- S1 rule: the 77 K and pressure mention must concern the H₂ measurement.
- `electrochemical` covers electrochemistry of hydrogen other than storage.
- I4: an area must be given for a sample the paper measured; a typical value
  for a kind of material does not count.
- Extraction: carbon sorbents only; identity fields copied exactly;
  `isotherm_branch` rule for single values; `value_kind` for bounds;
  `synthesis_method` for purchased materials; probe gas named anywhere in the
  paper; `calibration_described` defined; one row for a table value that is the
  same measurement as a plotted point; archive file named as
  `archive: <file>.json`; scratch files only in the agent's work directory.
- Matching code: free-text fields compared on presence, DOI case-insensitively,
  labels on letters and digits only.

## Round 2

Run with the revised prompts (same models) on HYC-0047 and HYC-0060, and the
screening and HYC-0051 eligibility checks repeated (`round2/`).

- **Screening**: the two screeners agreed on all 51 records, strata included.
  The two records split in round 1 are S2 for both.
- **Eligibility**: both assessors coded HYC-0051 `no_surface_area`.
- **Extraction** (`round2/agreement_AB_round2.json`): HYC-0047 gave 115 matched
  pairs with 98% of uptake values and 99% of pressures within the §9 tolerance;
  the round-1 problems (`isotherm_branch`, probe gas, non-carbon rows) did not
  recur. HYC-0060, a 14-laboratory round robin on one material, matched rows
  across laboratories because every laboratory's sample carries the same
  label; with the laboratory added to the label, 98.5% of its uptake values
  agree. Remaining disagreements were definitional: one isotherm ID per branch
  or per run, `instrument_identified`, `replicates_reported`, the
  `measurement_mode` of a dynamic volumetric isotherm, and consensus values
  computed across laboratories. Extractor A of HYC-0047 listed the tools
  directory once, outside its instruction, and reported it.

## Changes made to the prompts after round 2

- In a multi-laboratory paper the sample label includes the laboratory's label.
- Adsorption and desorption branches are separate isotherms;
  `isotherm_point_count` counts one branch.
- `instrument_identified` requires manufacturer and model, or a described
  home-built instrument (§10.1 item 7); `replicates_reported` is defined per
  row.
- `measurement_mode` is `isothermal` for any single-temperature uptake,
  including a dynamic volumetric isotherm.
- Values computed across samples or laboratories are not rows.
- Matching code: an empty cell of a field with a schema default is read as the
  default.

## Independent review (2026-10-28)

A reviewer agent in a fresh context, given the prompts, the code and the pilot
outputs but not this session's notes, found the prompts not ready to freeze
(`prompt_review_2026-10-28.md`, 22 findings). The two critical ones:

- The prompts carried the registered `schema.py` and data dictionary, which
  name 20 v0.1 papers with their values. An extractor told its paper's
  identity could have linked them to its paper.
- Reconciliation of v0.1 papers could not match any row: v0.1 descriptions
  carry no printed label, and every schema v2 field would have been reported
  as a disagreement.

## Changes made after the review

- The prompts carry a redacted schema text (`scripts/v1_redact_schema.py`)
  with every field, vocabulary, rule and definition and without the
  paper-specific examples; a test checks that no v0.1 paper ID or first
  author remains in any built prompt.
- A labelling agent (`legacy_labels`) gives each v0.1 sample its printed
  label; matching skips schema v2 fields empty on the v0.1 side.
- The validator reports schema v2 errors in their own words.
- Rules aligned with the registered dictionary: one `isotherm_id` per
  instrument run with both branches (reverting the round-2 change), point count
  over the run; a point with no printed wt% carries the computed W1; every
  non-uptake field in the unit its name gives; `calibration_described` and
  `replicates_reported` exactly as §10.1 defines them.
- Rules made explicit, and listed in Amendment 1: the S1 forms, I1 failures
  and TPD, `duplicate_data`, aggregates, carbon-only scope, the table/figure
  merge rule with the printed pressure kept, no characterization-only rows,
  `area_same_sample = other_paper` for areas the authors did not measure,
  `measuring_lab_id` format, the curve grid, the axis span, single
  digitizations, and the v0.1 mode.
- Reconciliation: identity rules, row and curve decisions in
  `resolutions.csv`, and a description of `match.csv` generated from the
  matching code.
- Agent environment: each agent's input under its own parent directory, a
  tools directory without data (`scripts/v1_tools_tree.py`), and a launcher
  that lists the only paths an agent may open.

## Round 3

Run with the revised prompts and the tools directory: dual extraction and
reconciliation of HYC-0040 (Flamina 2023; models as in round 1), and the v0.1
mode on HYC-0046 (labeller and reconciler `claude-opus-5-5`, reusing the
round-1 extraction by B). Outputs in `round3/`.

- **HYC-0040** (`round3/agreement_AB_HYC-0040.json`): 109 matched pairs, one
  row only B extracted (a marker mostly hidden behind another series), so 99.5%
  row-detection agreement. Every numeric field, including the uptake values,
  pressures and `isotherm_point_count`, agreed within the §9 tolerance (the
  point count agreed on 9.6% of pairs in round 2), and so did every schema v2
  categorical. The only disagreements were the material class, synthesis
  method and composition of one nickel-decorated sample. Both extractors merged
  the printed 20 bar values with the plotted end points, coded the paper's wt%
  as W2 from its own equation, converted the atm axis to bar, and left the
  calibration standards (LaNi₅, a MOF) out.
- The reconciler resolved every line of `match.csv`. It found that
  `digitized_means.csv` gave every point an uncertainty from the pressure axis:
  the code assumed uptake on the y axis, and this paper plots uptake on x. The
  code now finds the uptake axis (`v1_extract.uptake_axis`, with a test).
- **HYC-0046, v0.1 mode**: the labeller gave all nine v0.1 samples their
  printed labels; with them, six v0.1 rows matched B's rows and three did not,
  because the v0.1 rows have no pressure for a saturation value B had placed at
  the digitized pressure. The reconciler merged those three pairs, kept the
  v0.1 identifiers, added B's 45 digitized points, checked B's schema v2 coding
  against the paper, and resolved every line (`round3/legacy/HYC-0046/C/`).
- Every agent wrote files only in its own output and work directories
  (checked on disk). One reconciler reported opening two files in which its
  own tool environment had saved its long command output; the launcher now
  allows those.

## Changes made after round 3

- `digitized_means.csv`: the uncertainty uses the uptake axis.
- Extraction: when several plotted points fall within the pressure tolerance of
  a printed value, the merged point is the one the paper marks, or else the
  closest; a figure axis whose printed tick labels are inconsistent is not
  digitized (the two extractors of HYC-0040 handled such an axis in two
  different ways).
- Reconciliation: taking a figure value from `digitized_means.csv` is not
  logged as a decision.

## Second review and re-check (2026-10-28)

A second reviewer in a fresh context checked the revised prompts, the code, the
round-3 outputs and the draft amendment (`prompt_review2_2026-10-28.md`). It
found the 22 earlier findings closed or partly closed and six blocking
problems:

- the `value_kind` rule for a stated maximum went beyond §3 and the
  amendment;
- nothing kept the basis the same across an isotherm, which `hycan.v1`
  requires;
- six validator rules still reported "Missing required field: uptake";
- the redaction dropped two dictionary rules (one method and probe gas per
  row; the probe temperature), and the amendment overstated what the
  redaction script checks;
- defining reference set B by "both screeners include" would drop most records
  without an abstract;
- the amendment claimed a confinement that nothing enforced.

All six were fixed: the `value_kind` rule now follows §3 with a defined
"equals"; the basis, `uptake_type` and `measurement_method` are coded once per
isotherm and `v1_extract.py check` flags any isotherm that mixes them; every
model-level validator rule reports its own text; both dictionary rules were
restored; set B is every referenced work not excluded by both screeners; and
`scripts/v1_audit_access.py` audits each agent's transcript after every run,
with a pre-specified rerun for a confirmed breach. Most non-blocking items
were fixed too: the W1 factor, mg/g axes, v0.1 rows without a pressure,
label and class rules, the curve grid near zero, I1 failures, and the
reconciler's wording. A checker in a fresh context then re-tested the fixes
(`prompt_recheck_2026-10-28.md`). It found two wording gaps and an audit that
missed `..`, `~`, `$HOME`, reads inside the tools directory, other tools and
paths that do not exist on the auditing machine. All of these were fixed, and
the audit now flags every adversarial case in `tests/test_v1_audit_access.py`
and none of the round-3 calls.

The changes after round 3 were not piloted again; the agreement statistics of
the main run (§9) report how the frozen prompts performed.
