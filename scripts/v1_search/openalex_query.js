// HyCAN-DB v1.0 search, OpenAlex part (docs/v1_protocol.md §5).
//
// Runs in a browser tab on https://api.openalex.org, so requests are same-origin
// HTTPS with no content-transforming proxy. Every response body is kept as the
// exact text the API returned, with its request URL, retrieval time and SHA-256,
// and saved to one JSON file per batch. Those files, archived unmodified in
// references/v1_search/, are the record of the search.
//
// The registered expression is H AND C. OpenAlex limits boolean operators per
// query, so H is split into groups of at most five terms and each group is
// paired with one C term. The union of these sub-queries equals H AND C.
// No document-type filter is applied (protocol §5).

const H_TERMS = [
  '"hydrogen storage"', '"hydrogen adsorption"', '"hydrogen uptake"', '"hydrogen sorption"',
  '"hydrogen physisorption"', '"hydrogen spillover"', '"hydrogen capacity"',
  '"adsorption of hydrogen"', '"storage of hydrogen"', '"uptake of hydrogen"',
  '"sorption of hydrogen"', '"H2 storage"', '"H2 adsorption"', '"H2 uptake"', '"H2 sorption"',
  '"H2 physisorption"', 'cryoadsorption', '"cryo-adsorption"',
];
const C_TERMS = [
  '"activated carbon"', '"porous carbon"', '"microporous carbon"', '"nanoporous carbon"',
  '"mesoporous carbon"', '"templated carbon"', '"carbide-derived carbon"', '"carbon aerogel"',
  '"carbon cryogel"', '"carbon xerogel"', '"carbon nanotube"', '"carbon nanofiber"',
  '"carbon nanofibre"', '"carbon nanohorn"', 'graphene', '"carbon molecular sieve"',
  '"doped carbon"', '"carbon fiber"', '"carbon fibre"', '"carbon foam"', '"carbon sphere"',
  '"carbon material"', '"carbon-based"', 'carbonaceous', '"carbon nanostructure"', 'nanocarbon',
  '"carbon monolith"', 'biocarbon', 'biochar', '"superactivated carbon"', 'graphite', 'graphitic',
  'fullerene', '"carbon black"', 'CNT', 'SWCNT', 'MWCNT', 'SWNT', 'MWNT', 'ZTC',
];
const GROUP = 5;
const SELECT = 'id,doi,title,display_name,publication_year,type,language,primary_location,' +
  'best_oa_location,open_access,authorships,abstract_inverted_index,is_retracted,biblio';

function hGroups() {
  const g = [];
  for (let i = 0; i < H_TERMS.length; i += GROUP) g.push(H_TERMS.slice(i, i + GROUP));
  return g;
}

function subQueries() {
  const out = [];
  hGroups().forEach((h, hi) => C_TERMS.forEach((c, ci) => {
    out.push({
      key: `H${hi + 1}_C${String(ci + 1).padStart(2, '0')}`,
      filter: `title_and_abstract.search:(${h.join(' OR ')}) AND ${c}`,
    });
  }));
  return out;
}

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function fetchRaw(url) {
  for (let attempt = 0; attempt < 6; attempt++) {
    const r = await fetch(url);
    const body = await r.text();
    if (r.status === 429 || r.status >= 500) {
      await new Promise(res => setTimeout(res, 2000 * (attempt + 1)));
      continue;
    }
    return { status: r.status, body };
  }
  throw new Error('gave up after retries: ' + url);
}

async function runOne(q, perPage) {
  const pages = [];
  let cursor = '*';
  while (cursor) {
    const url = 'https://api.openalex.org/works?per-page=' + perPage + '&cursor=' +
      encodeURIComponent(cursor) + '&select=' + SELECT + '&filter=' + encodeURIComponent(q.filter);
    const { status, body } = await fetchRaw(url);
    if (status !== 200) throw new Error(q.key + ' HTTP ' + status + ' ' + body.slice(0, 300));
    pages.push({ url, retrieved_utc: new Date().toISOString(), status, sha256: await sha256Hex(body), body });
    const j = JSON.parse(body);
    cursor = j.meta.next_cursor && j.results.length ? j.meta.next_cursor : null;
  }
  const first = JSON.parse(pages[0].body);
  return { key: q.key, filter: q.filter, count: first.meta.count, pages };
}

function save(name, obj) {
  const blob = new Blob([JSON.stringify(obj)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
}

// Usage in the page console: await hycanRun(i0, i1, perPage)
// runs sub-queries [i0, i1) and downloads one batch file.
async function hycanRun(i0, i1, perPage) {
  const qs = subQueries().slice(i0, i1);
  const batch = [];
  for (const q of qs) batch.push(await runOne(q, perPage));
  save(`hycan_v1_openalex_${String(i0).padStart(3, '0')}_${String(i1).padStart(3, '0')}.json`, {
    source: 'OpenAlex', script: 'scripts/v1_search/openalex_query.js',
    protocol: 'docs/v1_protocol.md §5', run_at_utc: new Date().toISOString(), batch,
  });
  return batch.map(b => [b.key, b.count, b.pages.length]);
}

// Stemming check (protocol §5 Implementation): the counts for three terms in
// the singular and in the plural. Equal or near-equal counts show that the
// source stems; otherwise plural forms are added to C_TERMS before the run.
const STEM_PAIRS = [
  ['"carbon nanotube"', '"carbon nanotubes"'],
  ['"activated carbon"', '"activated carbons"'],
  ['"carbon nanofiber"', '"carbon nanofibers"'],
];

async function hycanStemCheck() {
  const rows = [];
  for (const pair of STEM_PAIRS) {
    for (const term of pair) {
      const url = 'https://api.openalex.org/works?per-page=1&select=id&filter=' +
        encodeURIComponent('title_and_abstract.search:' + term);
      const { status, body } = await fetchRaw(url);
      if (status !== 200) throw new Error(term + ' HTTP ' + status);
      rows.push({ term, url, retrieved_utc: new Date().toISOString(), status,
                  sha256: await sha256Hex(body), body,
                  count: JSON.parse(body).meta.count });
    }
  }
  save('hycan_v1_openalex_stemcheck.json', {
    source: 'OpenAlex', script: 'scripts/v1_search/openalex_query.js',
    protocol: 'docs/v1_protocol.md §5', run_at_utc: new Date().toISOString(), rows,
  });
  return rows.map(r => [r.term, r.count]);
}

// Count probe: the result count of every sub-query (one record per request),
// saved before the run so that batches can be sized; the counts are kept with
// their response bodies like every other response.
async function hycanCounts() {
  const rows = [];
  for (const q of subQueries()) {
    const url = 'https://api.openalex.org/works?per-page=1&select=id&filter=' +
      encodeURIComponent(q.filter);
    const { status, body } = await fetchRaw(url);
    if (status !== 200) throw new Error(q.key + ' HTTP ' + status);
    rows.push({ key: q.key, filter: q.filter, url, retrieved_utc: new Date().toISOString(),
                status, sha256: await sha256Hex(body), body,
                count: JSON.parse(body).meta.count });
    await new Promise(res => setTimeout(res, 120));
  }
  save('hycan_v1_openalex_counts.json', {
    source: 'OpenAlex', script: 'scripts/v1_search/openalex_query.js',
    protocol: 'docs/v1_protocol.md §5', run_at_utc: new Date().toISOString(), rows,
  });
  return { subqueries: rows.length, total: rows.reduce((a, r) => a + r.count, 0),
           largest: rows.map(r => [r.key, r.count]).sort((a, b) => b[1] - a[1]).slice(0, 5) };
}
