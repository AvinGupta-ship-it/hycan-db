"""Render the v1.0 manuscript to PDF (manuscript/v1/manuscript_v1.pdf).

The Markdown file is the source of record; this script typesets it with the
generated tables (manuscript/v1/tables.md) and the figures appended, so the
PDF is self-contained. Not part of the pinned analysis environment: it needs
the `markdown` package and Playwright with Chromium (both outside
requirements-v1.lock), and changes no analysis output.

    python3 scripts/v1_search/render_pdf.py [--out manuscript/v1/manuscript_v1.pdf]
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CSS = """
@page { size: A4; margin: 22mm 20mm; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt;
       line-height: 1.45; color: #111; max-width: 100%; }
h1 { font-size: 16pt; line-height: 1.25; margin: 0 0 6pt; }
h2 { font-size: 12.5pt; margin: 18pt 0 6pt; }
h3 { font-size: 11pt; margin: 14pt 0 4pt; }
p { margin: 0 0 7pt; text-align: justify; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; background: #f5f5f3;
             border-left: 3px solid #888; font-size: 9.5pt; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt;
       background: #f2f2f2; padding: 0 2px; }
table { border-collapse: collapse; margin: 8pt 0 12pt; font-size: 8.8pt;
        width: 100%; }
th, td { border: 0.5pt solid #999; padding: 3pt 5pt; text-align: left;
         vertical-align: top; }
th { background: #eceff2; }
tr { page-break-inside: avoid; }
.figure { page-break-inside: avoid; margin: 14pt 0; }
.figure img { max-width: 100%; max-height: 520pt; display: block;
              margin: 0 auto; }
.figure .cap { font-size: 9pt; margin-top: 5pt; text-align: justify; }
.pagebreak { page-break-before: always; }
"""

FIGURES = [
    ("Figure 1", ROOT / "references" / "v1_prisma" / "prisma_flow.png"),
    ("Figure 2", ROOT / "figures" / "v1" / "fig_v1_rq1_ratio.png"),
    ("Figure 3", ROOT / "figures" / "v1" / "fig_v1_rq1_sensitivity.png"),
    ("Figure 4", ROOT / "figures" / "v1" / "fig_v1_rq2_one_bar.png"),
    ("Figure 5", ROOT / "figures" / "v1" / "fig_v1_rq3_materials.png"),
    ("Figure 6", ROOT / "figures" / "v1" / "fig_v1_rq4_items.png"),
    ("Figure 7", ROOT / "figures" / "v1" / "fig_v1_rq5_models.png"),
]


def captions() -> dict[str, str]:
    """Figure stem -> caption text, from figures/v1/CAPTIONS.md."""
    out: dict[str, str] = {}
    name = None
    for block in (ROOT / "figures" / "v1" / "CAPTIONS.md").read_text(
        encoding="utf-8"
    ).split("\n\n"):
        block = " ".join(block.split())
        if block.startswith("**") and ".**" in block:
            name = block[2:block.index(".**")]
            out[name] = block[block.index(".**") + 3:].strip()
    return out


def html_of(md_text: str) -> str:
    import markdown

    return markdown.markdown(md_text, extensions=["tables"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "manuscript" / "v1" /
                                         "manuscript_v1.pdf"))
    args = ap.parse_args(argv)

    body = html_of((ROOT / "manuscript" / "v1" / "manuscript_v1.md")
                   .read_text(encoding="utf-8"))
    tables = html_of((ROOT / "manuscript" / "v1" / "tables.md")
                     .read_text(encoding="utf-8"))
    caps = captions()
    figs = []
    for label, path in FIGURES:
        data = base64.b64encode(path.read_bytes()).decode()
        cap = caps.get(path.stem, "")
        figs.append(
            f'<div class="figure"><img src="data:image/png;base64,{data}">'
            f'<div class="cap"><b>{label}.</b> {cap}</div></div>')
    doc = (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head>"
           f"<body>{body}"
           f"<div class='pagebreak'></div><h1>Tables</h1>{tables}"
           f"<div class='pagebreak'></div><h1>Figures</h1>{''.join(figs)}"
           f"</body></html>")

    from playwright.sync_api import sync_playwright

    out = Path(args.out)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.set_content(doc, wait_until="load")
        page.pdf(path=str(out), format="A4", print_background=True)
        browser.close()
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
