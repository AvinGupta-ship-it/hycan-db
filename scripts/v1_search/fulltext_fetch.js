// HyCAN-DB v1.0 full-text retrieval helper (docs/v1_protocol.md §8).
//
// Injected into a tab of the built-in browser on the author's computer, on the
// site that serves the full text (route 1: the open-access host; route 2: the
// publisher's site reached from the DOI through the author's university
// library). It fetches one file the page links to, with the tab's own session,
// checks that the bytes are a PDF, and saves them unmodified to the Downloads
// folder as hycan_ft_<frame_id>_<file> (file: main.pdf, si1.pdf, ...),
// returning the SHA-256 computed in the page. No full text passes through a
// model on the way; the retrieval log records the route, URL and SHA-256.
//
// Usage in the page: await hycanSavePdf('F01196', 'main.pdf', url)

async function ftSha256(buf) {
  const d = await crypto.subtle.digest('SHA-256', buf);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function ftSave(name, buf) {
  const blob = new Blob([buf], { type: 'application/pdf' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
}

async function hycanSavePdf(frameId, file, url) {
  if (!/^F\d{5}$/.test(frameId) || !/^(main|si\d+)\.pdf$/.test(file)) {
    throw new Error('bad frame_id or file name');
  }
  const r = await fetch(url, { credentials: 'include', redirect: 'follow' });
  const buf = await r.arrayBuffer();
  const head = new TextDecoder().decode(new Uint8Array(buf.slice(0, 5)));
  const result = { status: r.status, final_url: r.url, type: r.headers.get('content-type'),
                   bytes: buf.byteLength, is_pdf: head === '%PDF-' };
  if (r.status !== 200 || !result.is_pdf) return { saved: false, ...result };
  const name = 'hycan_ft_' + frameId + '_' + file;
  ftSave(name, buf);
  return { saved: true, name, sha256: await ftSha256(buf), ...result };
}
