# Reference set B (protocol §5; §15 Amendment 1, item 9)

Set B is identified before the search is run and is not used to choose search
terms. It is the referenced works of Gunther et al. (2026), "Adsorption-based
hydrogen storage: A comprehensive review and comparative analysis of
cryogenic sorption data", Int. J. Hydrogen Energy 253,
doi:10.1016/j.ijhydene.2026.156054 (OpenAlex W7166335407), that would enter
the frame under §6: every record not excluded by both screeners.

## Lookup

- `hycan_v1_lookup_setB_gunther2026_citing.json` and
  `hycan_v1_lookup_setB_gunther2026_refs.json`: written on 2026-10-28 by
  `hycanReferencedWorks` in `scripts/v1_search/openalex_lookup.js` (commit
  8cb168e), run in the built-in browser of the Claude desktop app on the
  author's computer, on api.openalex.org. Every response body is stored as
  returned, with its URL, time and SHA-256; the referenced-work IDs were read
  from the citing record inside the page.
- OpenAlex lists 91 referenced works; all 91 records were returned, 23 without
  an abstract (`setb_input.json`).
- `screen_input.csv`: the six screening columns, built by
  `scripts/v1_search/reference_sets.py setb-input`. `records.csv` keeps the
  DOIs, which the screeners did not see.

## Screening

- The frozen `screen.md` prompt (SHA-256 `41291c79…71db`, Amendment 1),
  started with the frozen launcher; screener A `claude-opus-5-5`, screener B
  `claude-sonnet-5-5`, each with its own copy of the input and its own output
  and work directories, on 2026-10-28. Each ran once.
- Both screeners excluded the same 77 records (κ = 1.0 for kept against
  excluded); they agreed on every decision (3 include, 11 uncertain, 77
  exclude) and differed only in the exclusion code of some excluded records.
- `access/`: the access audit of both transcripts
  (`scripts/v1_audit_access.py`): no flag. Its first pass flagged each
  screener's listing of the folder that held only its own input or output
  file; the audit now treats that folder as allowed, and the change is in the
  same commit as this file.

## Set B

`set_b.csv` (`reference_sets.py setb-build`): 14 records, 8 of them without
an abstract, 3 marked include by both screeners. Several are not H₂ papers
(methane or argon adsorption, MOFs for natural gas): the screeners kept them
as uncertain, which the definition keeps in set B. Recall on all 14 therefore
understates the search's recall on relevant papers, and recall on the 3
include-both records is reported alongside it (§5, item 9).
