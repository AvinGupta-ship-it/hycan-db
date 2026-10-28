"""Tests for scripts/v1_search/merge_search.py (protocol §5, §7)."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "merge_search", REPO_ROOT / "scripts" / "v1_search" / "merge_search.py"
)
ms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ms)


def page(body_obj: dict, tamper: bool = False) -> dict:
    body = json.dumps(body_obj)
    digest = hashlib.sha256(body.encode()).hexdigest()
    if tamper:
        body = body.replace("Carbon", "Carb0n")
    return {
        "url": "https://example/x",
        "retrieved_utc": "t",
        "status": 200,
        "sha256": digest,
        "body": body,
    }


def oa_work(wid: str, doi: str | None, title: str, year: int) -> dict:
    return {
        "id": f"https://openalex.org/{wid}",
        "doi": doi,
        "display_name": title,
        "publication_year": year,
        "abstract_inverted_index": {"hydrogen": [0], "uptake": [1]},
    }


def write_search(tmp: Path, tamper: bool = False) -> None:
    oa = {
        "batch": [
            {
                "key": "H1_C01",
                "count": 2,
                "pages": [
                    page(
                        {
                            "meta": {},
                            "results": [
                                oa_work(
                                    "W2", "https://doi.org/10.1/B", "Carbon B", 2010
                                ),
                                oa_work("W1", None, "Porous Carbon A", 2005),
                            ],
                        },
                        tamper,
                    )
                ],
            },
            {
                "key": "H1_C02",
                "count": 1,
                "pages": [
                    page(
                        {
                            "meta": {},
                            "results": [
                                oa_work(
                                    "W2", "https://doi.org/10.1/B", "Carbon B", 2010
                                )
                            ],
                        }
                    )
                ],
            },
        ]
    }
    (tmp / "hycan_v1_openalex_000_002.json").write_text(json.dumps(oa))
    s2 = {
        "pages": [
            page(
                {
                    "data": [
                        {
                            "paperId": "p1",
                            "externalIds": {"DOI": "10.1/b"},
                            "title": "Carbon B",
                            "year": 2010,
                        },
                        {
                            "paperId": "p2",
                            "externalIds": {},
                            "title": "Porous carbon A.",
                            "year": 2006,
                        },
                        {
                            "paperId": "p3",
                            "externalIds": {},
                            "title": "Only In S2",
                            "year": 2019,
                            "abstract": "abc",
                        },
                    ]
                }
            )
        ]
    }
    (tmp / "hycan_v1_semanticscholar.json").write_text(json.dumps(s2))


def test_merge_unions_subqueries_and_matches_s2_by_doi_then_title_year(
    tmp_path, monkeypatch
):
    write_search(tmp_path)
    monkeypatch.setattr(ms, "SEARCH_DIR", tmp_path)
    assert ms.main() == 0
    counts = json.loads((tmp_path / "merge_counts.json").read_text())
    assert counts["openalex_unique"] == 2
    assert counts["s2_matched_doi"] == 1
    assert counts["s2_matched_title_year"] == 1  # 2005 vs 2006 is within 1 year
    assert counts["s2_only"] == 1
    rows = list(csv.DictReader((tmp_path / "merged_records.csv").open()))
    assert [r["frame_id"] for r in rows] == ["F1", "F2", "F3"]
    # DOI-bearing record sorts first, then OpenAlex ID, then S2 ID (protocol §7).
    assert rows[0]["doi"] == "10.1/b" and rows[0]["subqueries"] == "H1_C01;H1_C02"
    assert rows[1]["openalex_id"] == "W1" and rows[1]["in_s2"] == "True"
    assert rows[2]["s2_id"] == "p3"


def test_merge_is_deterministic(tmp_path, monkeypatch):
    write_search(tmp_path)
    monkeypatch.setattr(ms, "SEARCH_DIR", tmp_path)
    ms.main()
    first = (tmp_path / "merged_records.csv").read_bytes()
    ms.main()
    assert (tmp_path / "merged_records.csv").read_bytes() == first


def test_a_tampered_response_body_is_refused(tmp_path, monkeypatch):
    write_search(tmp_path, tamper=True)
    monkeypatch.setattr(ms, "SEARCH_DIR", tmp_path)
    with pytest.raises(ms.IntegrityError):
        ms.main()


def test_two_openalex_ids_with_one_doi_become_one_record(tmp_path, monkeypatch):
    oa = {
        "batch": [
            {
                "key": "H1_C01",
                "count": 2,
                "pages": [
                    page(
                        {
                            "meta": {},
                            "results": [
                                oa_work(
                                    "W9", "https://doi.org/10.1/X", "Carbon X", 2011
                                ),
                                oa_work("W3", "10.1/x", "Carbon X", 2011),
                            ],
                        }
                    )
                ],
            }
        ]
    }
    (tmp_path / "hycan_v1_openalex_000_001.json").write_text(json.dumps(oa))
    monkeypatch.setattr(ms, "SEARCH_DIR", tmp_path)
    ms.main()
    counts = json.loads((tmp_path / "merge_counts.json").read_text())
    assert counts["openalex_doi_duplicates_merged"] == 1
    rows = list(csv.DictReader((tmp_path / "merged_records.csv").open()))
    assert len(rows) == 1 and rows[0]["openalex_id"] == "W3"


def test_gzipped_batches_are_read_and_check_files_skipped(tmp_path, monkeypatch):
    import gzip

    write_search(tmp_path)
    plain = tmp_path / "hycan_v1_openalex_000_002.json"
    (tmp_path / "hycan_v1_openalex_000_002.json.gz").write_bytes(
        gzip.compress(plain.read_bytes(), mtime=0)
    )
    plain.unlink()
    (tmp_path / "hycan_v1_openalex_stemcheck.json").write_text('{"rows": []}')
    (tmp_path / "hycan_v1_semanticscholar_stemcheck.json").write_text('{"rows": []}')
    (tmp_path / "hycan_v1_openalex_counts.json").write_text('{"rows": []}')
    monkeypatch.setattr(ms, "SEARCH_DIR", tmp_path)
    assert ms.main() == 0
    counts = json.loads((tmp_path / "merge_counts.json").read_text())
    assert counts["openalex_unique"] == 2 and counts["s2_only"] == 1
