# Literature Search Protocol — HyCAN-DB

This document records the search strategy used to assemble the HyCAN-DB literature corpus. It is the reproducibility companion to references/paper_tracking.csv.

## Engines used

- **Google Scholar** (https://scholar.google.com) — primary engine for the initial Day 5 sweep. Broad recall, free, no institutional login required.
- **Semantic Scholar** — to be added in a later phase, for citation chaining via API.
- **Scopus** (via UNT/TAMS credentials) — to be added in a later phase, for precision.

## Primary search strings (Section 7.4 of the Execution Manual)

Each string was run in Google Scholar with no date restriction, sort-by-relevance, and the "include patents" option disabled. The top 30 relevance-ranked results from each string were scanned.

### S1 — Carbon nanotubes
`("hydrogen storage" OR "hydrogen uptake" OR "hydrogen adsorption" OR "H2 sorption") AND ("carbon nanotube" OR "CNT" OR "MWCNT" OR "SWCNT")`
- Date executed: 2026-06-10
- Papers logged from this string: [6]

### S2 — Graphene and derivatives
`("hydrogen storage" OR "hydrogen uptake" OR "hydrogen adsorption") AND ("graphene" OR "graphene oxide" OR "reduced graphene oxide")`
- Date executed: 2026-06-10
- Papers logged from this string: [6]

### S3 — Activated, porous, templated, and carbide-derived carbons
`("hydrogen storage" OR "hydrogen sorption") AND ("activated carbon" OR "porous carbon" OR "templated carbon" OR "carbide-derived carbon")`
- Date executed: 2026-06-10
- Papers logged from this string: [6]

### S4 — Doped and functionalized carbons
`("hydrogen storage" OR "hydrogen uptake") AND ("nitrogen-doped carbon" OR "boron-doped carbon" OR "heteroatom doped" OR "functionalized carbon")`
- Date executed: 2026-06-10
- Papers logged from this string: [4]

### S5 — Hydrogen spillover on carbon
`("hydrogen spillover" OR "spillover") AND ("carbon" OR "nanotube" OR "graphene")`
- Date executed: 2026-06-10
- Papers logged from this string: [2]

## Anchor papers (added by direct lookup, not by query)

Six foundational papers (Execution Manual Section 7.4) were added by name before running the open searches. They are guaranteed includes regardless of how the queries rank them.

| paper_id | Citation | Significance |
|---|---|---|
| HYC-0001 | Panella, Hirscher, Roth — Carbon, 2005 | Multi-nanostructure comparison; calibration anchor |
| HYC-0002 | Liu et al. — Science, 1999 | High-profile early SWCNT claim; later contested |
| HYC-0003 | Yang — Carbon, 2000 | Early systematic CNT study |
| HYC-0004 | Nijkamp et al. — Applied Physics A, 2001 | Hirscher group early data |
| HYC-0005 | Texier-Mandoki et al. — Carbon, 2004 | Activated carbon foundational data |
| HYC-0006 | Chahine & Bénard — 1998 (or Bénard & Chahine, Scripta Materialia, 2007 if 1998 inaccessible) | Source of the Chahine rule (~1 wt% H2 per 500 m²/g BET at 77 K) |

## Inclusion criteria

See Execution Manual Section 7.3. Summary:
- Experimental measurement of hydrogen uptake (gravimetric, volumetric, or both)
- Carbon-based sorbent
- Specified temperature and pressure conditions
- At least BET surface area characterization reported

## Exclusion criteria (controlled vocabulary for the exclusion_reason column)

- `theoretical_only` — DFT/MD/ab initio with no experimental component
- `no_conditions_stated` — measurement reported without T and P
- `not_carbon` — sorbent is a MOF, zeolite, metal hydride, etc., with no carbon component
- `duplicate` — already logged from another search string
- `cannot_access` — full text not available through any open or institutional channel
- `other` — any other reason (must be explained in notes)

## PRISMA flow counts (running)

| Stage | Count | Last updated |
|---|---|---|
| Identified — anchor papers | 6 | 2026-06-10 |
| Identified — Google Scholar S1 | [6] | 2026-06-10 |
| Identified — Google Scholar S2 | [6] | 2026-06-10 |
| Identified — Google Scholar S3 | [6] | 2026-06-10 |
| Identified — Google Scholar S4 | [4] | 2026-06-10 |
| Identified — Google Scholar S5 | [2] | 2026-06-10 |
| Identified — citation chaining | 0 | 2026-06-10 |
| Duplicates removed | [0] | 2026-06-10 |
| Screened (title and abstract) | 0 | 2026-06-10 |
| Full-text reviewed | 0 | 2026-06-10 |
| Included in database | 0 | 2026-06-10 |

## Change log

- 2026-06-10: Protocol document initialized. Day 5 sweep executed; 30 candidate papers identified.
