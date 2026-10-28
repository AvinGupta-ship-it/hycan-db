"""Merge the archived OpenAlex and Semantic Scholar responses (protocol §5, §7).

Reads the raw batch files in references/v1_search/, re-checks every stored
response body against its recorded SHA-256, and builds one record set:

  1. the union of the OpenAlex sub-queries, by OpenAlex ID, including any
     sub-query re-queried in publication-date slices (openalex_slices.js);
     a sub-query whose distinct records still number fewer than the count
     OpenAlex reported for it is listed in merge_counts.json;
  2. Semantic Scholar records merged in by normalized DOI, then by normalized
     title with publication years differing by at most 1;
  3. a frame_id for every record: "F" + the zero-padded rank of its sort key,
     where the sort key is the normalized DOI if present, else the OpenAlex ID,
     else the Semantic Scholar paper ID.

Writes references/v1_search/merged_records.csv and merge_counts.json. The output
depends only on the input files, so re-running it reproduces the same bytes.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEARCH_DIR = ROOT / "references" / "v1_search"


class IntegrityError(RuntimeError):
    """A stored response body does not match its recorded SHA-256."""


def norm_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    d = doi.strip().lower()
    d = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d)
    return d or None


def norm_title(t: str | None) -> str:
    if not t:
        return ""
    t = unicodedata.normalize("NFKD", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def abstract_from_inverted(inv: dict | None) -> str:
    if not inv:
        return ""
    positions = [(p, w) for w, ps in inv.items() for p in ps]
    return " ".join(w for _, w in sorted(positions))


def checked_body(page: dict) -> dict:
    body = page["body"]
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if digest != page["sha256"]:
        raise IntegrityError(f"SHA-256 mismatch for {page['url'][:120]}")
    return json.loads(body)


def batch_files(prefix: str) -> list[Path]:
    """The archived result files of one source: `<prefix>*.json` or
    `<prefix>*.json.gz` (gzip keeps every stored body byte for byte), without
    the stemming-check and count-probe files, which hold no results."""
    files = [
        f
        for f in SEARCH_DIR.iterdir()
        if f.name.startswith(prefix)
        and (f.name.endswith(".json") or f.name.endswith(".json.gz"))
        and "stemcheck" not in f.name
        and "counts" not in f.name
    ]
    return sorted(files, key=lambda f: f.name)


def read_json(path: Path) -> dict:
    raw = path.read_bytes()
    if path.name.endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def load_openalex() -> tuple[dict[str, dict], dict[str, int], dict]:
    """The OpenAlex records, the count OpenAlex reported for each sub-query in
    the paged run, and a completeness report: every sub-query re-queried in
    slices (its paged count, its sliced count, its distinct records over both)
    and every sub-query whose distinct records fall short of its count."""
    recs: dict[str, dict] = {}
    per_query: dict[str, int] = {}
    sliced: dict[str, int] = {}
    seen: dict[str, set] = {}
    for f in batch_files("hycan_v1_openalex_"):
        data = read_json(f)
        for b in data["batch"]:
            if b.get("method") == "publication-date slices":
                sliced[b["key"]] = b["count"]
            elif b["key"] in per_query:
                raise ValueError(f"sub-query {b['key']} appears in two paged batches")
            else:
                per_query[b["key"]] = b["count"]
            ids = seen.setdefault(b["key"], set())
            for page in b["pages"]:
                for w in checked_body(page).get("results") or []:
                    oid = w["id"].rsplit("/", 1)[-1]
                    ids.add(oid)
                    r = recs.setdefault(
                        oid,
                        {
                            "openalex_id": oid,
                            "s2_id": None,
                            "doi": norm_doi(w.get("doi")),
                            "title": w.get("display_name") or w.get("title") or "",
                            "year": w.get("publication_year"),
                            "type": w.get("type"),
                            "venue": (
                                (w.get("primary_location") or {}).get("source") or {}
                            ).get("display_name"),
                            "language": w.get("language"),
                            "is_retracted": w.get("is_retracted"),
                            "oa_status": (w.get("open_access") or {}).get("oa_status"),
                            "oa_url": (w.get("best_oa_location") or {}).get("pdf_url")
                            or (w.get("open_access") or {}).get("oa_url"),
                            "abstract": abstract_from_inverted(
                                w.get("abstract_inverted_index")
                            ),
                            "first_author": (
                                (w.get("authorships") or [{}])[0].get("author") or {}
                            ).get("display_name"),
                            "subqueries": set(),
                            "in_openalex": True,
                            "in_s2": False,
                            "abstract_source": None,
                        },
                    )
                    r["subqueries"].add(b["key"])
                    if r["abstract"] and not r["abstract_source"]:
                        r["abstract_source"] = "openalex"
    completeness = {
        "sliced": {
            k: {
                "paged_count": per_query.get(k),
                "sliced_count": n,
                "distinct": len(seen[k]),
            }
            for k, n in sorted(sliced.items())
        },
        "short": [
            [k, n, len(seen.get(k, ()))]
            for k, n in sorted(per_query.items())
            if len(seen.get(k, ())) < max(n, sliced.get(k, 0))
        ],
    }
    return recs, per_query, completeness


def collapse_openalex_doi_duplicates(recs: dict[str, dict]) -> int:
    """Merge OpenAlex records that share a normalized DOI (protocol §5).

    OpenAlex sometimes holds two work IDs for one article. They are one record:
    the lowest work ID is kept, the sub-query sets are united, and the first
    non-empty abstract is kept. Returns the number of records removed.
    """
    by_doi: dict[str, list[str]] = {}
    for oid, r in recs.items():
        if r["doi"]:
            by_doi.setdefault(r["doi"], []).append(oid)
    removed = 0
    for oids in by_doi.values():
        if len(oids) < 2:
            continue
        keep, *drop = sorted(oids)
        kept = recs[keep]
        for oid in drop:
            other = recs.pop(oid)
            kept["subqueries"] |= other["subqueries"]
            if not kept["abstract"] and other["abstract"]:
                kept["abstract"] = other["abstract"]
                kept["abstract_source"] = other["abstract_source"]
            removed += 1
    return removed


def merge_s2(recs: dict[str, dict]) -> dict[str, int]:
    by_doi = {r["doi"]: r for r in recs.values() if r["doi"]}
    by_title: dict[str, list[dict]] = {}
    for r in recs.values():
        by_title.setdefault(norm_title(r["title"]), []).append(r)
    stats = {
        "s2_records": 0,
        "s2_matched_doi": 0,
        "s2_matched_title_year": 0,
        "s2_only": 0,
    }
    for f in batch_files("hycan_v1_semanticscholar"):
        data = read_json(f)
        for page in data["pages"]:
            for p in checked_body(page).get("data") or []:
                stats["s2_records"] += 1
                doi = norm_doi((p.get("externalIds") or {}).get("DOI"))
                hit = by_doi.get(doi) if doi else None
                if hit:
                    stats["s2_matched_doi"] += 1
                else:
                    year = p.get("year")
                    for cand in by_title.get(norm_title(p.get("title")), []):
                        if (
                            year is not None
                            and cand["year"] is not None
                            and abs(cand["year"] - year) <= 1
                        ):
                            hit = cand
                            break
                    if hit:
                        stats["s2_matched_title_year"] += 1
                if hit:
                    hit["in_s2"] = True
                    hit["s2_id"] = hit["s2_id"] or p.get("paperId")
                    if not hit["abstract"] and p.get("abstract"):
                        hit["abstract"] = p["abstract"]
                        hit["abstract_source"] = "semantic_scholar"
                    continue
                stats["s2_only"] += 1
                rec = {
                    "openalex_id": None,
                    "s2_id": p.get("paperId"),
                    "doi": doi,
                    "title": p.get("title") or "",
                    "year": p.get("year"),
                    "type": ";".join(p.get("publicationTypes") or []),
                    "venue": p.get("venue"),
                    "language": None,
                    "is_retracted": None,
                    "oa_status": None,
                    "oa_url": (p.get("openAccessPdf") or {}).get("url"),
                    "abstract": p.get("abstract") or "",
                    "first_author": ((p.get("authors") or [{}])[0]).get("name"),
                    "subqueries": {"S2"},
                    "in_openalex": False,
                    "in_s2": True,
                    "abstract_source": "semantic_scholar"
                    if p.get("abstract")
                    else None,
                }
                recs["S2:" + p["paperId"]] = rec
                if doi:
                    by_doi[doi] = rec
                by_title.setdefault(norm_title(rec["title"]), []).append(rec)
    return stats


def sort_key(r: dict) -> str:
    if r["doi"]:
        return "1:" + r["doi"]
    if r["openalex_id"]:
        return "2:" + r["openalex_id"]
    return "3:" + (r["s2_id"] or "")


def main() -> int:
    recs, per_query, completeness = load_openalex()
    openalex_doi_duplicates = collapse_openalex_doi_duplicates(recs)
    n_openalex = len(recs)
    stats = merge_s2(recs)
    rows = sorted(recs.values(), key=sort_key)
    width = len(str(len(rows)))
    cols = [
        "frame_id",
        "doi",
        "openalex_id",
        "s2_id",
        "title",
        "year",
        "type",
        "venue",
        "first_author",
        "language",
        "is_retracted",
        "oa_status",
        "oa_url",
        "in_openalex",
        "in_s2",
        "subqueries",
        "abstract_source",
        "abstract",
    ]
    out = SEARCH_DIR / "merged_records.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for rank, r in enumerate(rows, 1):
            row = dict(r)
            row["frame_id"] = "F" + str(rank).zfill(width)
            row["subqueries"] = ";".join(sorted(r["subqueries"]))
            w.writerow({c: row.get(c) for c in cols})
    no_abstract = sum(1 for r in rows if not r["abstract"])
    counts = {
        "openalex_subqueries": len(per_query),
        "openalex_count_sum": sum(per_query.values()),
        "openalex_sliced": completeness["sliced"],
        "openalex_subqueries_short": completeness["short"],
        "openalex_doi_duplicates_merged": openalex_doi_duplicates,
        "openalex_unique": n_openalex,
        **stats,
        "merged_total": len(rows),
        "without_abstract": no_abstract,
        "merged_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }
    (SEARCH_DIR / "merge_counts.json").write_text(json.dumps(counts, indent=2) + "\n")
    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
