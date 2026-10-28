// HyCAN-DB v1.0: look up known works in OpenAlex by DOI (docs/v1_protocol.md
// §5 Execution; used for the prompt pilot on v0.1 papers and for reference
// set B). Not a search: it retrieves the records of DOIs already in hand.
//
// Runs in a browser tab on https://api.openalex.org. Every response body is
// kept as the exact text the API returned, with its request URL, retrieval
// time and SHA-256, and the batch is downloaded as one JSON file.

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function fetchRaw(url) {
  for (let tries = 0; ; tries++) {
    const r = await fetch(url);
    const body = await r.text();
    if (r.status === 200) {
      return { url, retrieved_utc: new Date().toISOString(), status: r.status,
               sha256: await sha256Hex(body), body };
    }
    if ((r.status !== 429 && r.status < 500) || tries >= 6) {
      throw new Error('HTTP ' + r.status + ' ' + body.slice(0, 300));
    }
    await new Promise(res => setTimeout(res, 2000 * (tries + 1)));
  }
}

// name: label for the output file; dois: array of bare DOIs.
async function hycanLookup(name, dois) {
  const pages = [];
  for (let i = 0; i < dois.length; i += 40) {
    const chunk = dois.slice(i, i + 40).map(d => d.toLowerCase());
    const url = 'https://api.openalex.org/works?per-page=50&filter=doi:' +
      chunk.map(d => encodeURIComponent('https://doi.org/' + d)).join('|');
    pages.push(await fetchRaw(url));
    await new Promise(res => setTimeout(res, 300));
  }
  const blob = new Blob([JSON.stringify({
    source: 'OpenAlex', script: 'scripts/v1_search/openalex_lookup.js',
    purpose: name, dois, run_at_utc: new Date().toISOString(), pages,
  })], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'hycan_v1_lookup_' + name + '.json';
  document.body.appendChild(a); a.click(); a.remove();
  return pages.map(p => [p.status, JSON.parse(p.body).meta.count]);
}

// Look up works by OpenAlex ID (W...), for example the referenced works of a
// paper. ids: array of IDs, with or without the https://openalex.org/ prefix.
async function hycanLookupIds(name, ids) {
  const pages = [];
  const bare = ids.map(i => i.replace('https://openalex.org/', ''));
  for (let i = 0; i < bare.length; i += 40) {
    const url = 'https://api.openalex.org/works?per-page=50&filter=openalex_id:' +
      bare.slice(i, i + 40).join('|');
    pages.push(await fetchRaw(url));
    await new Promise(res => setTimeout(res, 300));
  }
  const blob = new Blob([JSON.stringify({
    source: 'OpenAlex', script: 'scripts/v1_search/openalex_lookup.js',
    purpose: name, ids: bare, run_at_utc: new Date().toISOString(), pages,
  })], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'hycan_v1_lookup_' + name + '.json';
  document.body.appendChild(a); a.click(); a.remove();
  return pages.map(p => [p.status, JSON.parse(p.body).meta.count]);
}
