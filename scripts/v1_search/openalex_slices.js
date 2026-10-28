// HyCAN-DB v1.0 search, OpenAlex completeness re-query (docs/v1_protocol.md §5).
//
// OpenAlex cursor paging can return a record on two pages of one sub-query and
// leave out another. In the run of 2026-10-28, two sub-queries (H1_C11 and
// H1_C15) gave fewer distinct records than the count the API reported for
// them. This script re-queries a sub-query in slices of at most 200 records,
// so that every slice is one page and no paging is used: first the
// sub-query's records counted by publication year (group_by), then one request
// per year, and for a year above 200 records one request per month of
// publication date. Each slice's filter is the sub-query's registered filter
// with a publication-date restriction added, so the union of the slices is the
// sub-query; the search expression is unchanged. The group_by response is kept
// as the first page of each sub-query (it holds no records).
//
// It is injected into the same page after openalex_query.js and uses that
// script's subQueries() and withKey(), so the key the author typed into its box
// is added to each request only when it is sent and is never written into a
// saved URL, returned or logged.
//
// Usage in the page console: await hycanSliced(['H1_C11', 'H1_C15'])
// downloads hycan_v1_openalex_slices.json.

const SLICE_SELECT = 'id,doi,title,display_name,publication_year,type,language,primary_location,' +
  'best_oa_location,open_access,authorships,abstract_inverted_index,is_retracted,biblio';
const SLICE_MAX = 200;

async function sliceSha(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function sliceFetch(url) {
  for (let attempt = 0; attempt < 6; attempt++) {
    const r = await fetch(withKey(url));
    const body = await r.text();
    if (r.status === 429 || r.status >= 500) {
      await new Promise(res => setTimeout(res, 2000 * (attempt + 1)));
      continue;
    }
    return { status: r.status, body };
  }
  throw new Error('gave up after retries: ' + url);
}

async function slicePage(url) {
  const { status, body } = await sliceFetch(url);
  if (status !== 200) throw new Error('HTTP ' + status + ' ' + url + ' ' + body.slice(0, 300));
  return { url, retrieved_utc: new Date().toISOString(), status, sha256: await sliceSha(body), body };
}

function sliceUrl(filter, restriction) {
  return 'https://api.openalex.org/works?per-page=' + SLICE_MAX + '&select=' + SLICE_SELECT +
    '&filter=' + encodeURIComponent(filter + restriction);
}

function monthEnd(y, m) {
  return String(new Date(Date.UTC(y, m, 0)).getUTCDate()).padStart(2, '0');
}

// A slice must fit one page: the page holds every record the slice counts.
function wholeSlice(key, page) {
  const j = JSON.parse(page.body);
  if (j.meta.count > SLICE_MAX || j.results.length !== j.meta.count) {
    throw new Error(key + ' slice not one page: ' + page.url);
  }
  return j.results.map(w => w.id);
}

async function sliceOne(q) {
  const pages = [];
  const g = await slicePage('https://api.openalex.org/works?group_by=publication_year&filter=' +
    encodeURIComponent(q.filter));
  pages.push(g);
  const groups = JSON.parse(g.body).group_by;
  const ids = new Set();
  let grouped = 0;
  for (const grp of groups) {
    const y = Number(grp.key);
    if (!Number.isInteger(y)) throw new Error(q.key + ' publication_year group ' + grp.key);
    grouped += grp.count;
    if (grp.count <= SLICE_MAX) {
      const p = await slicePage(sliceUrl(q.filter, ',publication_year:' + y));
      wholeSlice(q.key, p).forEach(id => ids.add(id));
      pages.push(p);
    } else {
      for (let m = 1; m <= 12; m++) {
        const mm = String(m).padStart(2, '0');
        const p = await slicePage(sliceUrl(q.filter, ',from_publication_date:' + y + '-' + mm +
          '-01,to_publication_date:' + y + '-' + mm + '-' + monthEnd(y, m)));
        wholeSlice(q.key, p).forEach(id => ids.add(id));
        pages.push(p);
      }
    }
  }
  return { key: q.key, filter: q.filter, count: grouped, method: 'publication-date slices',
           distinct: ids.size, pages };
}

async function hycanSliced(keys) {
  const qs = subQueries().filter(q => keys.includes(q.key));
  if (qs.length !== keys.length) throw new Error('unknown sub-query key');
  const batch = [];
  for (const q of qs) batch.push(await sliceOne(q));
  save('hycan_v1_openalex_slices.json', {
    source: 'OpenAlex', script: 'scripts/v1_search/openalex_slices.js',
    protocol: 'docs/v1_protocol.md §5', run_at_utc: new Date().toISOString(), batch,
  });
  return batch.map(b => [b.key, b.count, b.distinct, b.pages.length]);
}
