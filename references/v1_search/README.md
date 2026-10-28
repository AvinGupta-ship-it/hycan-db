# v1.0 search record (protocol §5)

The search was run on 2026-10-28 (UTC) from the committed scripts in
`scripts/v1_search/`, in the built-in browser of the Claude desktop app on the
author's computer: same-origin HTTPS requests from a tab on each API's own
site, with no proxy. Each script saved every response body as returned, with
its request URL, retrieval time and SHA-256, to the author's Downloads folder;
no response passed through a model. Before each run, the code in the page was
checked against the committed file: the SHA-256 of the functions' source text
and constants, computed in the page, equalled the value computed from the file
(the fingerprints below).

## Files

| File | What it holds |
|---|---|
| `hycan_v1_semanticscholar.json.gz` | Semantic Scholar bulk search, 9 pages |
| `hycan_v1_semanticscholar_stemcheck.json` | Semantic Scholar stemming check |
| `hycan_v1_openalex_stemcheck.json` | OpenAlex stemming check |
| `hycan_v1_openalex_NNN_MMM.json[.gz]` | OpenAlex sub-queries NNN to MMM−1, 40 files |
| `hycan_v1_openalex_slices.json.gz` | OpenAlex re-query of two sub-queries in publication-date slices |
| `downloads.json` | SHA-256, size and response count of every file as downloaded |
| `merged_records.csv`, `merge_counts.json` | The merged record set (`merge_search.py`) |
| `recall.json` | Recall on reference sets A and B (`reference_sets.py recall`) |

Files above 1 MB are stored gzipped with no name or time in the header;
`gunzip -c FILE.gz | sha256sum` gives the SHA-256 listed in `downloads.json`.
`scripts/v1_search/archive_downloads.py` checked every stored body against its
SHA-256 before archiving, and `merge_search.py` checks them again on every
run. No saved URL contains the OpenAlex API key (checked on every file).

## Semantic Scholar

- `semanticscholar_query.js` as committed in af96509 (unchanged since);
  fingerprint `e8d5df04c7b068fc09c64ea8465a02cf17ccc1767410ac3bb05408fc24e0ad89`.
- Stemming check, 08:30Z: singular and plural counts differ by at most 1
  (`"carbon nanotube"` 239,118 / `"carbon nanotubes"` 239,117; `"activated
  carbon"` 105,142 / 105,141; `"carbon nanofiber"` 16,640 / 16,640). The
  source stems; no plural terms were added.
- Search, 08:30–08:32Z: the full expression in one bulk query. Reported total
  8,608; 9 pages returned 8,608 records with 8,608 distinct paper IDs, the last
  page with no continuation token.

## OpenAlex

- Stemming check, 08:26Z, `openalex_query.js` as committed in 1165f95 (its
  `hycanStemCheck` is unchanged in 15808dc): singular and plural counts equal
  (266,058; 117,318; 19,107). The source stems; no plural terms were added.
- Without an API key, OpenAlex then answered HTTP 429 "Insufficient budget":
  requests without a key share a small daily budget per IP address. No batch
  file was saved from those requests. The script gained a box in which the
  author typed the key of a free OpenAlex account (15808dc); the key is added
  to each request only when it is sent and is not in any saved URL.
- Run, 19:37–19:41Z, `openalex_query.js` as committed in 15808dc; fingerprint
  `c86fb58a0b23d505064ba22d0c50c7382eb50f58df8dadd49bdc22de1f0988c4`.
  `hycanRunAll(200, 4)`: the 160 sub-queries (the 18 H terms in 4 groups of at
  most five, × the 40 C terms; §5 Implementation) in 40 batch files of 4, with
  cursor paging at 200 records per page. 231 pages; the counts OpenAlex reported sum to
  19,270 (sub-queries overlap); 24 sub-queries have no hits.
- The browser did not write 6 of the 40 batch files
  (`024_028`, `104_108`, `112_116`, `124_128`, `132_136`, `144_148`). Those
  batches were run again in the same page with `hycanRun` at 19:39–19:41Z.
  For all 160 sub-queries, the count and page count in the archived files
  equal those in the in-page log of the first pass.
- **Paging completeness.** In 11 sub-queries, cursor paging returned some
  records on two pages (24 repeated rows in all). In two of them it also left
  records out: H1_C11 (`"carbon nanotube"`) returned 2,138 distinct records of
  the 2,142 reported, and H1_C15 (`graphene`) 2,508 of 2,511. Both were
  re-queried at 19:47Z by `openalex_slices.js` as committed in c3e13bb
  (fingerprint
  `9db9b4dd619fd2cf7194a0550d734c01ceecb86a5e9278818a0cb570952d5b4c`): a
  count by publication year, then one single-page request per year, or per
  month for the two H1_C15 years above 200 records (2025, 2026); 94
  responses. The search expression is unchanged; only the paging is. The
  slices returned 2,141 and 2,509 records; the year groups leave out records
  with no publication year (1 and 2), each of which the paged run returned.
  The union of the paged run and the slices holds exactly the reported 2,142
  and 2,511 records; the slices added 7 records the paged run had missed.
  `merge_counts.json` lists every sub-query re-queried in slices and every
  sub-query still short of its reported count (none).

## Merge (protocol §5, §7)

`merge_search.py` (`merge_counts.json`): 10,043 OpenAlex records after 5 pairs
of OpenAlex IDs sharing a DOI were merged; 8,608 Semantic Scholar records, of
which 6,604 matched by DOI, 809 by title and year, and 1,195 were added; 11,238
records in all, 4,815 of them (42.8%) without an abstract in either source.
`merged_records.csv` SHA-256
`e276a0ca9c7f842a6aadd7650afd6fc4b570da93de80358629b83a00a6da41e5`.

## Recall (protocol §5; §15 Amendment 1, item 9)

- **Set A** (Appendix B, 44 v0.1 papers): 44 of 44 in the merged set (100%;
  25 of them without an abstract in OpenAlex). Recall is above 90%, so no
  terms are added.
- **Set B** (14 records, `references/v1_setB/`): 5 of 14 (36%). Of the 9
  misses, 4 are indexed without an abstract and 5 have an abstract with no H
  term; most are not H₂ papers (methane, argon and natural-gas adsorption,
  adsorption thermodynamics, a sorption analyser for refrigerants), which the
  set-B definition keeps because a screener marked them uncertain.
- **Set B, include by both screeners**: 2 of 3. The miss, W2088485903 (H₂, CO₂,
  CH₄, CO, N₂ and H₂O adsorption on activated carbon and zeolite for a
  pressure-swing-adsorption unit), measures H₂ isotherms but uses none of the H
  terms: the search does not reach gas-separation papers that never describe
  H₂ uptake as storage or adsorption of hydrogen. This is reported as a
  limitation; set B is not used to choose terms (§5).
