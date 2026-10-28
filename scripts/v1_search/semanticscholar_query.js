// HyCAN-DB v1.0 search, Semantic Scholar part (docs/v1_protocol.md §5).
//
// Runs in a browser tab on https://api.semanticscholar.org. Bulk search matches
// the query against title and abstract; '+' is AND, '|' is OR, double quotes mark
// phrases, parentheses group. Every response body is kept as the exact text the
// API returned, with its request URL, retrieval time and SHA-256.

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
const QUERY = '(' + H_TERMS.join(' | ') + ') + (' + C_TERMS.join(' | ') + ')';
const FIELDS = 'paperId,corpusId,externalIds,title,abstract,year,venue,publicationTypes,' +
  'openAccessPdf,authors';

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function s2Run() {
  const pages = [];
  let token = null;
  do {
    let url = 'https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=' +
      encodeURIComponent(QUERY) + '&fields=' + FIELDS;
    if (token) url += '&token=' + encodeURIComponent(token);
    let r, body, tries = 0;
    while (true) {
      r = await fetch(url);
      body = await r.text();
      if ((r.status !== 429 && r.status < 500) || ++tries > 10) break;
      await new Promise(res => setTimeout(res, 3000 * tries));
    }
    if (r.status !== 200) throw new Error('HTTP ' + r.status + ' ' + body.slice(0, 300));
    pages.push({ url, retrieved_utc: new Date().toISOString(), status: r.status,
                 sha256: await sha256Hex(body), body });
    token = JSON.parse(body).token || null;
    await new Promise(res => setTimeout(res, 1100));
  } while (token);
  const blob = new Blob([JSON.stringify({
    source: 'Semantic Scholar', script: 'scripts/v1_search/semanticscholar_query.js',
    protocol: 'docs/v1_protocol.md §5', query: QUERY, run_at_utc: new Date().toISOString(), pages,
  })], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'hycan_v1_semanticscholar.json'; document.body.appendChild(a); a.click(); a.remove();
  const first = JSON.parse(pages[0].body);
  return [pages.length, first.total];
}
