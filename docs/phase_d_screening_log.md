# Phase D screening log

**Search run:** 2026-09-27
**Protocol:** execution manual §7.3 (search strings), §7.2 (inclusion criteria),
§7.4 (AI-executed search and the bias guard), §7.5 (PRISMA counts)
**Outcome recorded in:** `references/paper_tracking.csv` (the 35 included),
`references/phase_d_screening.json` (their verified metadata)

This log exists because §7.4 requires that every screened paper's decision be
recorded, and because 68 of the 103 distinct candidates are not in the tracking file.
They are not discarded; they are recorded here so a later session resumes rather than
repeats the search.

---

## 1. How the search was run

Neither Crossref nor the OpenAlex/Semantic Scholar **search** endpoints were usable
from this session, so the discovery layer was web search rather than a metadata API.
What each channel could and could not do is worth recording, because it shaped the
result and will shape the next attempt:

| Channel | Status this session |
| --- | --- |
| `curl` to any metadata API from the shell | **blocked** — 403 at the egress proxy on CONNECT, for `api.openalex.org` and `api.semanticscholar.org` alike |
| Crossref via WebFetch | **unavailable** — the domain required an approval that did not arrive |
| OpenAlex `works?filter=title.search:` via WebFetch | **throttled** — 429 on nine consecutive attempts across two agents |
| OpenAlex `works?filter=doi:a|b|c` (batched) via WebFetch | **throttled** — 429 |
| OpenAlex `works/doi:<DOI>` via WebFetch | **reliable** — 35 of 35 first attempts succeeded |
| Semantic Scholar search via WebFetch | **throttled** — 429 |
| Europe PMC via WebFetch | **throttled** at the WebFetch proxy itself |
| Web search | **worked** — this was the discovery layer |

**The operationally useful finding is that OpenAlex's single-DOI path endpoint stayed
reliable while every one of its search and filter endpoints was throttled.** That
asymmetry is what made the verification pass possible at all, and it means a future
session should treat DOI resolution as cheap and title search as expensive, which is
the reverse of the assumption §3.5 is written on.

Four agents ran the searches, each on a slice aimed at a different part of the
analysis funnel, with the five §7.3 strings covered across them:

| Agent | Slice | Queries | Records |
| --- | --- | ---: | ---: |
| A1 | doped and metal-decorated carbons at 77 K | 20 | 38 |
| A2 | undoped porous carbons at 77 K with a BET area, new groups | 18 | 36 |
| A3 | volumetric storage density | 26 | 21 |
| A4 | bias guard: 1998–2005 controversy, and low/negative results | 29 | 28 |
| | | **93** | **123** |

## 2. PRISMA counts

| Stage | Count |
| --- | ---: |
| Records identified | 123 |
| Excluded at title/abstract screening against §7.2 | 14 |
| Duplicates of the 30 already-tracked papers | 3 |
| Same paper identified by two agents | 5 |
| **Distinct candidates carried forward** | **103** |
| Bibliographic metadata resolution attempted | 42 |
| — resolved to a confirmed DOI, **included** | **35** |
| — unresolved, no DOI obtainable | 7 |
| Below the priority cut, resolution not attempted | 61 |
| Full text retrieved | **30** |
| **Full text not retrieved** | **5** |
| — of the retrieved, excluded at full-text review | **1** (HYC-0038; see §5.2) |
| Extracted | 0 at search time (since grown; tracked in `references/paper_tracking.csv` and `docs/ai_usage_log.md`) |

Two of the three tracked-paper duplicates were already inside the 14 exclusions, so
the distinct total is 123 − 14 − 1 − 5 = 103.

**Retrieval updated 2026-09-30**, when `scripts/migrate_pdf_obtained.py` recorded
the outcome in `references/paper_tracking.csv`. 30 of the 35 are now
`pdf_obtained = yes`; all 35 remain `extraction_status = not_started`.

The 5 not retrieved are **HYC-0035, HYC-0036, HYC-0054, HYC-0055, HYC-0056**. They
are a PRISMA line of their own and not an exclusion: `screening_decision` stays
`include` and each row's `notes` records why the full text is absent. Folding them
into the 14 screening exclusions would misreport a retrieval failure as an
eligibility judgement. All five are Royal Society of Chemistry titles, which makes
the loss systematic by publisher rather than random — §7 below, and
`docs/corpus_audit.md` §5.6 for what it costs each funnel target.

## 3. Anti-fabrication measures, and what they caught

Every search agent was instructed that a DOI, year, author or journal not literally
seen in a URL, a search result or a fetched page must be left **empty**, and that a
publisher article ID is not a DOI. Verification was then performed by agents that had
not run the searches.

- **One search agent caught itself** writing a DOI it had not seen, during its own QA
  pass, and rebuilt its output file programmatically from a validated structure
  rather than hand-editing.
- **The verification pass found no further fabrication.** 29 of 29 recorded DOIs
  resolved to the paper they claimed. That is the finding, and it is only meaningful
  because the check was run by agents that had not produced the values.
- **Six records carried an RSC article ID and no DOI**, because the agents correctly
  refused to convert one into the other by pattern. Those were resolved by *testing*
  the hypothesis `10.1039/<ID>` against the API and requiring the returned title to
  match — a confirmation, not a guess. All six confirmed.
- **Two year discrepancies** surfaced between a search agent's recording and
  OpenAlex's `publication_year`, both looking like online-first versus issue year —
  the same defect §7 of the manual records on six bibliography entries. The OpenAlex
  value was recorded and the discrepancy noted rather than silently resolved.
- **One OpenAlex record lists a single author** for a 14-laboratory round-robin study
  (now HYC-0056). This is the same under-reporting that gave HYC-0011 one author where
  the article prints four. The API value was recorded as returned and **the author
  list must be corrected from the PDF** before that paper is cited.

## 4. The 35 included papers

In `paper_tracking.csv` as HYC-0031 … HYC-0065, with verified metadata in
`references/phase_d_screening.json`. Ordered by funnel priority, which is what the ID
sequence encodes.

| ID | Year | OA | Funnel | First author | Journal | Title |
|---|---|---|---|---|---|---|
| HYC-0031 | 2017 | gold | 77K_BET;doped_77K;volumetric | L. Scott Blankenship | Nature Communications | Oxygen-rich microporous carbons with exceptional hydrogen storage capacity |
| HYC-0032 | 2023 | gold | 77K_BET;doped_77K | Suphakorn Anuchitsakol | RSC Advances | Combined experimental and simulation study on H 2 storage in oxygen and nitrogen co- |
| HYC-0033 | 2019 | gold | 77K_BET;doped_77K | Jimmy Romanos | Scientific Reports | Boron-neutron Capture on Activated Carbon for Hydrogen Storage |
| HYC-0034 | 2016 | closed | 77K_BET;doped_77K | Ziqiang Wang | International Journal of Hydrogen Energy | Nitrogen-doped porous carbons with high performance for hydrogen storage |
| HYC-0035 | 2016 | closed | 77K_BET;doped_77K | D. Li | RSC Advances | Influence of doping nitrogen, sulfur, and phosphorus on activated carbons for gas ad |
| HYC-0036 | 2010 | closed | 77K_BET;doped_77K | Yi Wang | Energy & Environmental Science | Hydrogen storage in a Ni–B nanoalloy-doped three-dimensional graphene material |
| HYC-0037 | 2013 | closed | doped_77K;low_uptake | Liang Chen | International Journal of Hydrogen Energy | Facile synthesis and hydrogen storage application of nitrogen-doped carbon nanotubes |
| HYC-0038 | 2021 | gold | doped_77K | Lucyna Firlej | Nanomaterials | Hydrogen Storage in Pure and Boron-Substituted Nanoporous Carbons—Numerical and Expe |
| HYC-0039 | 2021 | gold | doped_77K | Mohamed F. Aly Aboud | Applied Sciences | Hydrogen Storage in Untreated/Ammonia-Treated and Transition Metal-Decorated (Pt, Pd |
| HYC-0040 | 2023 | gold | doped_77K | A. Flamina | Applied Surface Science Advances | Hydrogen storage in Nickel dispersed boron doped reduced graphene oxide |
| HYC-0041 | 2023 | closed | doped_77K | Arturo Morandé | Journal of Energy Storage | Modification of a commercial activated carbon with nitrogen and boron: Hydrogen stor |
| HYC-0042 | 2019 | gold | 77K_BET;new_group | Lerato Y. Molefe | Frontiers in Chemistry | Polymer-Based Shaping Strategy for Zeolite Templated Carbons (ZTC) and Their Metal O |
| HYC-0043 | 2019 | gold | 77K_BET;new_group | Liyan Ma | BioResources | Preparation and adsorption of CO2 and H2 by activated carbon hollow fibers from rubb |
| HYC-0044 | 2021 | gold | 77K_BET;new_group | Sung-Ho Hwang | Nanomaterials | The Enhanced Hydrogen Storage Capacity of Carbon Fibers: The Effect of Hollow Porous |
| HYC-0045 | 2013 | hybrid | 77K_BET;new_group | Eric Masika | Progress in Natural Science: Materials International | Preparation of ultrahigh surface area porous carbons templated using zeolite 13X for |
| HYC-0046 | 2006 | green | 77K_BET;new_group | Houria Kabbour | Chemistry of Materials | Toward New Candidates for Hydrogen Storage: High-Surface-Area Carbon Aerogels |
| HYC-0047 | 2010 | closed | 77K_BET;new_group | Vanessa Fierro | Carbon | Experimental evidence of an upper limit for hydrogen storage at 77 K on activated ca |
| HYC-0048 | 2023 | hybrid | 77K_BET;new_group | Gentil Mwengula Kahilu | Waste Disposal & Sustainable Energy | Systematic physicochemical characterization, carbon balance and cost of production a |
| HYC-0049 | 2012 | closed | 77K_BET;new_group | Nicholas P. Stadie | Langmuir | Zeolite-Templated Carbon Materials for High-Pressure Hydrogen Storage |
| HYC-0050 | 2008 | green | 77K_BET;new_group | Leire Zubizarreta | Adsorption | H2 storage in carbon materials |
| HYC-0051 | 2001 | closed | classic;low_uptake;new_group | Gary G. Tibbetts | Carbon | Hydrogen storage capacity of carbon nanotubes, filaments, and vapor-grown fibers |
| HYC-0052 | 2003 | closed | classic;low_uptake;new_group | Li Peng Zhou | International Journal of Hydrogen Energy | A comparative study of hydrogen adsorption on superactivated carbon versus carbon na |
| HYC-0053 | 2025 | hybrid | new_group;volumetric | Hiroshi Matsutaka | Journal of Materials Chemistry A | Densification of cellulose acetate-derived porous carbons for enhanced volumetric hy |
| HYC-0054 | 2013 | green | new_group;volumetric | Eric Masika | Energy & Environmental Science | Exceptional gravimetric and volumetric hydrogen storage for densified zeolite templa |
| HYC-0055 | 2012 | closed | new_group;volumetric | Jiacheng Wang | Journal of Materials Chemistry | Synthesis, characterization, and hydrogen storage capacities of hierarchical porous  |
| HYC-0056 | 2016 | green | new_group;volumetric | Norah Balahmar | Journal of Materials Chemistry A | Templating of carbon in zeolites under pressure: synthesis of pelletized zeolite tem |
| HYC-0057 | 2009 | bronze | 77K_BET;new_group | Gregory P. Meisner | Nanotechnology | High surface area microporous carbon materials for cryogenic hydrogen storage synthe |
| HYC-0058 | 2024 | gold | doped_other;low_uptake | D. Rosas-Medellín | Processes | Functional Sulfur-Doped Biocarbon for Hydrogen Storage: Development of Nanomaterials |
| HYC-0059 | 2023 | closed | doped_other;low_uptake | Ruiran Guo | Materials Today Chemistry | A detailed experimental comparison on the hydrogen storage ability of different form |
| HYC-0060 | 2009 | closed | low_uptake | Claudia Zlotea | International Journal of Hydrogen Energy | A Round Robin characterisation of the hydrogen sorption properties of a carbon based |
| HYC-0061 | 2009 | closed | low_uptake | Yuanzhen Chen | Carbon | Influence of sample cell physisorption on measurements of hydrogen storage of carbon |
| HYC-0062 | 1999 | closed | classic;doped_other | Ping Chen | Science | High H2 Uptake by Alkali-Doped Carbon Nanotubes Under Ambient Pressure and Moderate  |
| HYC-0063 | 2009 | closed | new_group | M.S. Balathanigaimani | Catalysis Today | Hydrogen storage on highly porous novel corn grain-based carbon monoliths |
| HYC-0064 | 2025 | diamond | new_group | Shengming Cheng | International Journal of Coal Science & Technology | Synthesis of activated carbon from Zhundong coal and its hydrogen storage applicatio |
| HYC-0065 | 2017 | closed | doped_other | Martyna Baca | International Journal of Hydrogen Energy | Effect of Pd loading on hydrogen storage properties of disordered mesoporous hollow  |

## 5. Excluded at screening (14)

Recorded per §7.4. A screening decision made and not recorded did not happen.

| cand | reason | title |
|---|---|---|
| A1-05 | duplicate_of_HYC-0025 | Hydrogen storage in boron-doped carbon nanotubes: Effect of dopant concentration |
| A1-35 | theoretical_only | Adsorption of hydrogen on boron-doped graphene: A first-principles prediction |
| A1-36 | theoretical_only | Hydrogen storage efficiency of Fe doped carbon nanotubes: molecular simulation study |
| A1-37 | theoretical_only | Hydrogen storage capacity of Al, Ca, Mg, Ni, and Zn decorated phosphorus-doped graphene: I |
| A1-38 | review_only | Hydrogen Storage Properties of Metal-Modified Graphene Materials |
| A3-12 | non_carbon | Volumetric hydrogen adsorption capacity of densified MIL-101 monoliths |
| A3-13 | non_carbon | Experimental assessment of physical upper limit for hydrogen storage capacity at 20 K in d |
| A3-14 | non_carbon | Densified HKUST-1 Monoliths as a Route to High Volumetric and Gravimetric Hydrogen Storage |
| A3-15 | review_only | Porous carbons: a class of nanomaterials for efficient adsorption-based hydrogen storage |
| A3-16 | no_h2_measurement | Direct synthesis of carbide-derived carbon monoliths with hierarchical pore design by hard |
| A4-09 | theoretical_only | Hydrogen storage in nanoporous carbon materials: myth and facts |
| A4-11 | review_only | Understanding factors affecting storage capacity and reproducibility in realistic ambient- |
| A4-17 | review_only | Hydrogen storage in carbon nanotubes |
| A4-25 | duplicate_of_HYC-0012 | Hydrogen storage in carbon nanotubes revisited |

### 5.1 A category §7.2 does not have

Three candidates are **DOE Hydrogen Program annual progress reports**, not
peer-reviewed articles: "Nanostructured Activated Carbon for Hydrogen Storage" (2011),
"Metal-doped Carbon Aerogels for Hydrogen Storage" (2005) and "Carbide-Derived Carbons
with Tunable Porosity Optimized for Hydrogen Storage" (2005). §7.1 scopes the corpus
to peer-reviewed papers, but §7.2's exclusion list has no value for gray literature,
so they sit in the table below as unresolved rather than carrying a reason.

**Recommendation, not applied here:** add `not_peer_reviewed` to the exclusion
vocabulary. Several of these reports correspond to peer-reviewed papers by the same
groups, which are the things worth chasing instead.

### 5.2 Excluded at full-text review (1)

This is a distinct PRISMA stage from the 14 title/abstract exclusions above: the
paper was screened **in**, its full text was retrieved, and only on reading it did
it fail the eligibility criteria. Keeping it separate stops a full-text exclusion
being miscounted as a title/abstract one.

| paper | reason | why |
|---|---|---|
| HYC-0038 | no_experimental_uptake | Firlej et al. 2021, *Nanomaterials* 11, 2173. A review plus GCMC study: every hydrogen **uptake** isotherm is simulated; the only experimental hydrogen result is an **adsorption energy** (~9 kJ/mol, Fig 6d, from 77 K/87 K isotherms), with no pressure axis and no anchored (T, P, uptake) triple. Per §7.2 ("exclude only when the *value* cannot be determined") no row is extractable. Ratified 2026-10-02; `screening_decision=exclude` in `paper_tracking.csv`, citation kept in `bibliography_sources.json` for PRISMA. The boron carbons are physically real, so the SI could rescue it later. See `docs/migration_exclude_hyc0038_plan.md`.

## 6. Carried forward, not yet decided (68)

These have a screening judgement from a search agent but no verified metadata, so they
are not in the tracking file (see the migration plan §3). `evidence` says what the
agent actually saw: `fetched` means it read the page, `title` means it saw only a
search result. Resolving these is the cheapest way to extend the candidate list
without running the searches again — and per §1, single-DOI resolution is the endpoint
that works.

| cand | scr | evidence | identifier | funnel | title |
|---|---|---|---|---|---|
| A3-11 | include | fetched | `` | doped_77K;new_group;volumetric | Nanostructured Activated Carbon for Hydrogen Storage |
| A3-10 | include | fetched | `` | new_group;volumetric | Metal-doped Carbon Aerogels for Hydrogen Storage |
| A3-06 | include | fetched | `S1385894724092337` | new_group;volumetric | Trade-off between surface area and tap density when selecting carbon adsorbents for hydr |
| A3-07 | include | fetched | `S2214785318311623` | new_group;volumetric | Nanoporous Graphene Monolith for Hydrogen Storage |
| A3-09 | include | fetched | `` | volumetric | Carbide-Derived Carbons with Tunable Porosity Optimized for Hydrogen Storage |
| A3-03 | include | fetched | `S1387181110000363` | volumetric | Enhanced volumetric hydrogen and methane storage capacity of monolithic carbide-derived  |
| A3-01 | include | fetched | `S1387181108002308` | volumetric | Enhanced volumetric hydrogen storage capacity of porous carbon powders by forming peels  |
| A4-02 | uncertain | fetched | `10.1038/386377a0` | classic | Storage of hydrogen in single-walled carbon nanotubes |
| A2-11 | uncertain | fetched | `10.3390/reactions2030014` | new_group | Adsorption-Based Hydrogen Storage in Activated Carbons and Model Carbon Structures |
| A4-04 | uncertain | url | `10.1126/science.287.5453.591e` | classic | Room-Temperature Hydrogen Storage in Nanotubes |
| A4-05 | uncertain | url | `10.1126/science.286.5442.1127` | classic | Hydrogen Storage in Single-Walled Carbon Nanotubes at Room Temperature |
| A4-14 | uncertain | url | `10.1007/s00339-003-2414-z` | classic | Hydrogen storage in multi-wall carbon nanotubes using samples up to 85 g |
| A4-15 | uncertain | url | `10.1021/nl015576g` | classic | Studies into the Storage of Hydrogen in Carbon Nanofibers: Proposal of a Possible Reacti |
| A3-17 | uncertain | fetched | `10.1007/s11164-015-2338-1` | new_group | Comparison of MOF-5- and Cr-MOF-derived carbons for hydrogen storage application |
| A4-18 | uncertain | url | `S0360319901001343` | classic | Ball-milled carbon and hydrogen storage |
| A4-12 | uncertain | title | `10.1002/cphc.202100508` | low_uptake | Improving Reproducibility in Hydrogen Storage Material Research |
| A4-20 | uncertain | url | `S0925963502003606` | low_uptake | Hydrogen uptake of carbon nanofiber under moderate temperature and low pressure |
| A4-21 | uncertain | url | `S0360319907004223` | low_uptake | The accuracy of hydrogen sorption measurements on potential storage materials |
| A4-13 | uncertain | title | `C6EE01435F` | low_uptake | Irreproducibility in hydrogen storage material research |
| A4-03 | uncertain | title | `` | classic | Hydrogen adsorption and cohesive energy of single-walled carbon nanotubes |
| A4-16 | uncertain | title | `` | classic | Hydrogen Storage Capacity of Catalytically Grown Carbon Nanofibers |
| A4-27 | uncertain | title | `` | classic | Carbon Nanotube Materials for Hydrogen Storage |
| A4-19 | uncertain | title | `16853032` | low_uptake | Hydrogen storage capacity characterization of carbon nanotubes by a microgravimetrical a |
| A4-22 | uncertain | title | `20239818` | low_uptake | Gravimetric and volumetric methods for hydrogen sorption measurements on carbon nanotube |
| A4-24 | uncertain | title | `240390009` | low_uptake | Upper limit of hydrogen adsorption on activated carbons at room temperature: A thermodyn |
| A1-19 | uncertain | title | `10.3390/ma14092098` | doped_other | Crumpled Graphene-Storage Media for Hydrogen and Metal Nanoclusters |
| A4-26 | uncertain | url | `S000862230600488X` | new_group | Hydrogen storage on chemically activated carbons and carbon nanomaterials at high pressu |
| A2-21 | uncertain | title | `10.1080/01457632.2016.1194703` | new_group | Adsorption Isotherms of Hydrogen on Granular Activated Carbon Derived From Coal and Deri |
| A2-22 | uncertain | title | `10.1021/acsami.0c22192` | new_group | A Step Forward in Understanding the Hydrogen Adsorption and Compression on Activated Car |
| A2-25 | uncertain | title | `10.46690/capi.2023.03.02` | new_group | Construction of PAN-based activated carbon nanofibers for hydrogen storage under ambient |
| A2-31 | uncertain | title | `10.1021/jp3100365` | new_group | Hydrogen Storage in High Surface Area Carbons with Identical Surface Areas but Different |
| A2-33 | uncertain | title | `10.1021/ja067149g` | new_group | Enhanced Hydrogen Storage Capacity of High Surface Area Zeolite-like Carbon Materials |
| A2-34 | uncertain | title | `10.1021/jp808890x` | new_group | High-Pressure Hydrogen Storage in Zeolite-Templated Carbon |
| A2-35 | uncertain | title | `10.1021/acsnano.5b02623` | new_group | Direct Evidence for Solid-like Hydrogen in a Nanoporous Carbon Hydrogen Storage Material |
| A4-28 | uncertain | url | `S0008622308003904` | new_group | Hydrogen adsorption on single-walled carbon nanotubes studied by core-level photoelectro |
| A1-23 | uncertain | title | `10.1021/jp908156v` | doped_other | Hydrogen Storage Properties of N-Doped Microporous Carbon |
| A1-24 | uncertain | title | `10.1021/ja9054838` | doped_other | Hydrogen Storage in High Surface Area Carbons: Experimental Demonstration of the Effects |
| A1-29 | uncertain | title | `10.3390/en8053578` |  | Hydrogen Storage in Pristine and d10-Block Metal-Anchored Activated Carbon Made from Loc |
| A1-30 | uncertain | title | `10.3390/inorganics11060251` |  | Hydrogen Storage Properties of Economical Graphene Materials Modified by Non-Precious Me |
| A2-14 | uncertain | title | `S036031992404206X` | new_group | Physically activated resorcinol-formaldehyde derived carbon aerogels for enhanced hydrog |
| A2-15 | uncertain | title | `S0360319919319871` | new_group | Static and dynamic studies of hydrogen adsorption on nanoporous carbon gels |
| A2-17 | uncertain | title | `` | new_group | Cryogenic hydrogen storage on peanut shell-derived-activated carbons: Isotherm, kinetics |
| A2-18 | uncertain | title | `S0360319917337473` | new_group | A study on optimal pore range for high pressure hydrogen storage behaviors by porous har |
| A2-19 | uncertain | title | `S1385894721033118` | new_group | Nanoporous polymer-derived activated carbon for hydrogen adsorption and electrochemical  |
| A2-24 | uncertain | title | `S0360319923035097` | new_group | Micropores enriched ultra-high specific surface area activated carbon derived from waste |
| A2-26 | uncertain | title | `S0008622311008992` | new_group | Hydrogen storage in CO2-activated amorphous nanofibers and their monoliths |
| A2-27 | uncertain | title | `S2095495615602777` | new_group | Pore size effects of nanoporous carbons with ultra-high surface area on high-pressure hy |
| A2-28 | uncertain | title | `S0360319923052680` | new_group | Comparing the practical hydrogen storage capacity of porous adsorbents: Activated carbon |
| A2-29 | uncertain | title | `` | new_group | MOF-Derived Hierarchically Porous Carbon with Exceptional Porosity and Hydrogen Storage  |
| A2-30 | uncertain | title | `S2352152X24016712` | new_group | Scalable synthesis of biomass-derived three-dimensional hierarchical porous activated ca |
| A2-36 | uncertain | title | `S0008622309002449` | new_group | High performance of nanoporous carbon in cryogenic hydrogen storage and electrochemical  |
| A1-16 | uncertain | title | `S0360319915305760` | doped_other | Enhanced hydrogen storage performance of reduced graphene oxide hybrids with nickel or i |
| A1-17 | uncertain | title | `S0360319919337024` | doped_other | Neutron scattering study of nickel decorated thermally exfoliated graphite oxide |
| A1-18 | uncertain | title | `S0008622312004010` | doped_other | Preparation and characterization of graphene and Ni-decorated graphene using flower peta |
| A1-20 | uncertain | title | `S036031991933335X` | doped_other | Hydrogen storage in platinum loaded single-walled carbon nanotubes |
| A1-21 | uncertain | title | `` | doped_other | Hydrogen Storage in Decorated Multiwalled Carbon Nanotubes by Ca, Co, Fe, Ni, and Pd Nan |
| A1-22 | uncertain | title | `S0360319918302222` | doped_other | Nitrogen-incorporated carbon nanotube derived from polystyrene and polypyrrole as hydrog |
| A1-25 | uncertain | title | `` | doped_other | Preparation and Hydrogen Storage Properties of Zeolite-Templated Carbon Materials Nanoca |
| A1-26 | uncertain | title | `` | doped_other | Copper-doped activated carbon from amorphous cellulose for hydrogen, methane and carbon  |
| A1-27 | uncertain | title | `` | doped_other | Copper salt impregnated biomass-derived microporous carbon for hydrogen storage |
| A1-32 | uncertain | title | `S0360319920325003` | doped_other | Hydrogen adsorption properties of in-situ synthesized Pt-decorated porous carbons templa |
| A1-33 | uncertain | title | `` | doped_other | Nitrogen doped porous carbon derived from EDTA: Effect of pores on hydrogen storage prop |
| A3-18 | uncertain | title | `S2352152X2300590X` | doped_other | Modification of a commercial activated carbon with nitrogen and boron: Hydrogen storage  |
| A1-31 | uncertain | title | `10.1080/15567036.2025.2569826` |  | Hard coal- and lignite-derived N-doped carbons: Structure–performance relationship in CO |
| A1-28 | uncertain | title | `` |  | Hydrogen Adsorption and Isotope Mixing on Copper-Functionalized Activated Carbons |
| A1-34 | uncertain | title | `` |  | Enhanced storage of hydrogen at the temperature of liquid nitrogen |
| A3-19 | uncertain | title | `S1387181107005690` |  | Advanced activated carbon monoliths and activated carbons for hydrogen storage |
| A3-21 | uncertain | title | `` |  | Automotive hydrogen storage system using cryo-adsorption on activated carbon |

## 7. Bias guard — what was done and what it produced

§7.4 requires a deliberate counterweight to a search engine's preference for recent,
high-citation, high-uptake work. One of the four agents was assigned to that
exclusively, and `docs/corpus_audit.md` §3.6 quantifies why: the corpus's entire
1995–2000 bin is three rows from one paper.

It produced, among the included 35:

- **HYC-0062 — the 1999 *Science* paper claiming high H₂ uptake by alkali-doped
  carbon nanotubes at ambient pressure.** The corpus already tracks the 2000 paper
  that revisits and refutes that claim (HYC-0003) but has never held the claim itself.
  Expect Tier D; that is the point.
- **HYC-0051** (Tibbetts, *Carbon* 2001) and **HYC-0052** (Zhou, *IJHE* 2003) — two
  rigorous early comparative studies whose finding is that carbon nanotubes store far
  less hydrogen than the era claimed.
- **HYC-0060** — a 14-laboratory round robin on the same materials, which is a
  calibration anchor for the §13 tiering rubric rather than an ordinary data source.
  This is also the record whose OpenAlex author list is implausibly short (§3).
- **HYC-0061** — a study of how the sample cell's own physisorption biases Sieverts
  measurements, i.e. a paper about the measurement error the whole corpus inherits.

An earlier draft of this section named HYC-0058, HYC-0056 and HYC-0057 for the first,
third and fourth of these. Those IDs were read off the working ranked list rather than
from the assigned identifiers, and all three pointed at different papers. Caught by a
checker that re-derived every claim in this document from
`references/phase_d_screening.json`; recorded here rather than quietly amended.

Seven of the 35 carry the `low_uptake` tag and three carry `classic`. That is a
deliberate over-weighting relative to what the searches surfaced on their own, and it
should be read as a correction rather than as what the literature looks like.

**The bias-guard set survived retrieval intact** (added 2026-09-30). All five papers
named above are `pdf_obtained = yes`, and both tags came through complete —
`low_uptake` 7 of 7, `classic` 3 of 3. §7.4's counterweight is therefore the one
part of Phase D that retrieval did not erode. The five losses fall on `volumetric`
(3 of 5) and `doped_77K` (2 of 11) instead; `docs/corpus_audit.md` §5.6 has the
per-target table and what it costs.

That is a fortunate distribution, not a designed one. Nothing in the collection
route protected the bias-guard papers; they happen to be in Elsevier and AAAS
journals while the five losses are all RSC. Had the publisher gone the other way the
guard itself would have been the casualty, and it would have been a much worse
outcome for the same reason §7.4 exists. If Phase E collection is planned, securing
access to RSC before screening rather than after is the lesson.


---

## 8. Collection outcome, 2026-09-30

**30 of the 35 are in the Project.** Avin collected 30; `scripts/stage_phase_d_pdfs.py`
identified 23 on its first run and the remaining 7 after the matcher was corrected
(commit `743bac1`), which is what the "citing other corpus papers" defect cost.

**The five not obtained are all Royal Society of Chemistry titles:**

| ID | Paper | Access | What its absence costs |
| --- | --- | --- | --- |
| HYC-0035 | Li 2016, *RSC Advances* | closed | `doped_77K`, `77K_BET` |
| HYC-0036 | Wang 2010, *Energy Environ. Sci.* | closed | `doped_77K`, `77K_BET` |
| HYC-0054 | Masika & Mokaya, *Energy Environ. Sci.* | **green** | `volumetric`, `new_group` |
| HYC-0055 | Wang 2012, *J. Mater. Chem.* | closed | `volumetric`, `new_group` |
| HYC-0056 | Balahmar & Mokaya, *J. Mater. Chem. A* | **green** | `volumetric`, `new_group` |

Coverage by funnel target: `new_group` **15 of 18**, `77K_BET` 14 of 16,
`doped_77K` **9 of 11**, `low_uptake` 7 of 7, `volumetric` **2 of 5**,
`doped_other` 4 of 4, `classic` 3 of 3.

**The cost column and the coverage line above were both incomplete when first
written** and were corrected 2026-09-30 after recomputing per-tag coverage from
`references/phase_d_screening.json`. They credited each loss to a single tag and
omitted `new_group` and `77K_BET` entirely. Every one of the five is tagged for two
targets, not one, so the original figures understated the loss. Recorded here rather
than silently amended.

**The Figure 4 blocker is cleared and the volumetric gap is not.** §15 could not
build Figure 4 on 4 doped rows from a single paper; nine doped papers at 77 K is a
different situation entirely. Volumetric capacity remains the thinnest target: the
schema's gap-10 fields were exercised by one paper's conventions, and three of the
four papers meant to broaden that are the ones still missing.

**`new_group` is the loss that was nearly missed.** The same three papers were the
`new_group` candidates, so that pool drops from 18 to 15 — and `docs/corpus_audit.md`
§5.2 ranks it second overall, because the binding constraint on cross-validation is
the count of groups (11) and not of rows (102). It is stated as a candidate loss and
not a group loss deliberately: whether those three would have reached the 77 K + BET
subset cannot be known without the full texts, and Phase C.1 added two papers tagged
for that subset and moved the group count by zero.

**Recorded in the tracking file 2026-09-30** by
`scripts/migrate_pdf_obtained.py`, under `docs/migration_pdf_obtained_plan.md`: the
30 read `pdf_obtained = yes`, the 5 stay `no` and carry the reason in `notes`.
Verified by diffing `references/paper_tracking.csv` against `HEAD` — 35 of 66
physical lines changed, all inside the Phase D block, CRLF and the absent trailing
newline preserved. All 35 remain `extraction_status = not_started`.

### 8.1 HYC-0054 carries a published correction

**Crossref records `updated-by: correction, 10.1039/d1ee90006d`** — *Correction:
Exceptional gravimetric and volumetric hydrogen storage for densified zeolite
templated carbons with high mechanical stability*, *Energy Environ. Sci.*, 2021.
The correction's content is paywalled and has not been read.

**The correction must be obtained and read before that paper is extracted.** A
corrected paper entering the corpus with its superseded values is the failure mode
the whole verification protocol exists to prevent, and no validator downstream
could detect it: the numbers would be internally consistent, correctly sourced to a
real table, and wrong. The paper's headline claim is a volumetric storage figure,
which is exactly the field it was selected to populate.

**Nothing in the pipeline checks for this.** `paper_tracking.csv` has no column for
a retraction or correction notice, and no step in the §9.1 per-paper pipeline
consults one. This is a gap in the protocol rather than an oversight on one paper,
and it applies to all 65 tracked papers, not only the 35 new ones.

### 8.2 Three recorded years are the online-first year, not the issue year

Every Phase D year came from OpenAlex's `publication_year`. Manual §7 already
records that this reports Elsevier's online-first year on six bibliography entries;
it does the same for RSC. Confirmed against Crossref's `published-print`:

| ID | Recorded | Issue year | Evidence |
| --- | --- | --- | --- |
| HYC-0052 | 2003 | **2004** | `published-print [[2004,4]]`, vol 29(5) 475–479, `journal-issue` also 2004-04 |
| HYC-0054 | 2013 | **2014** | `published-print [[2014]]`, vol 7(1) 427–434; RSC's own correction notice cites 2014 |
| HYC-0061 | 2009 | **2010** | `published-print [[2010,3]]`, vol 48(3) 714–720; the PDF's running head reads `CARBON 48 (2010) 714 – 720` |

**Not yet corrected in the data.** `references/paper_tracking.csv` is protected under
§6.7 and a year change needs a migration plan; the staged PDF filenames for
HYC-0052 and HYC-0061 also embed the old year, though harmlessly, since the
`paper_id` prefix is what identifies a file.

**The other 32 are not cleared.** Eight checked clean, four could not be read, and
twenty were never attempted: Crossref refuses `curl` from this session at the egress
proxy and the WebFetch route is rate-limited and needs per-URL approval. Those 32
are **unknown**, not clean, for both the year and the correction check.

### 8.3 Method note on the checks above

Crossref was read through WebFetch, which passes the response through a summarising
model, so a dropped `updated-by` would look exactly like an absent one. Two
mitigations were used and both should be kept if this is resumed: every field had to
be reported as `ABSENT` rather than omitted, and each prompt was validated against a
control DOI with a *known* correction before any `ABSENT` elsewhere was believed.
The summariser was still caught misreporting a present field twice. **A raw-JSON
pass is still owed** before the eight clean rows are treated as verified.
