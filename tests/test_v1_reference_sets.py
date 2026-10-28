"""Tests for scripts/v1_search/reference_sets.py on synthetic lookup files."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "v1_search"))
spec = importlib.util.spec_from_file_location(
    "reference_sets", REPO_ROOT / "scripts" / "v1_search" / "reference_sets.py"
)
rs = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = rs
spec.loader.exec_module(rs)


def page(results):
    body = json.dumps({"meta": {"count": len(results)}, "results": results})
    return {
        "url": "u",
        "retrieved_utc": "t",
        "status": 200,
        "sha256": hashlib.sha256(body.encode()).hexdigest(),
        "body": body,
    }


def work(wid, title, doi=None, abstract=True, year=2010):
    return {
        "id": f"https://openalex.org/{wid}",
        "doi": doi,
        "display_name": title,
        "publication_year": year,
        "type": "article",
        "primary_location": {"source": {"display_name": "Carbon"}},
        "abstract_inverted_index": {"hydrogen": [0], "uptake": [1]}
        if abstract
        else None,
    }


def test_set_b_input_build_and_recall(tmp_path):
    citing = work("W0", "Review", doi="https://doi.org/10.1/review")
    citing["referenced_works"] = [
        "https://openalex.org/W2",
        "https://openalex.org/W1",
        "https://openalex.org/W3",
    ]
    (tmp_path / "c.json").write_text(json.dumps({"pages": [page([citing])]}))
    refs = [
        work("W1", "Hydrogen on carbon A", doi="https://doi.org/10.1/a"),
        work("W2", "MOF paper", abstract=False),
        work("W3", "Hydrogen on carbon B", abstract=False, year=2012),
    ]
    (tmp_path / "r.json").write_text(
        json.dumps({"ids": ["W1", "W2", "W3"], "pages": [page(refs)]})
    )
    d = tmp_path / "setB"
    assert (
        rs.main(
            [
                "setb-input",
                str(tmp_path / "c.json"),
                str(tmp_path / "r.json"),
                "--doi",
                "10.1/review",
                "--out",
                str(d),
            ]
        )
        == 0
    )
    rows = list(csv.DictReader((d / "screen_input.csv").open()))
    assert [r["frame_id"] for r in rows] == ["W1", "W2", "W3"]
    assert rows[0]["abstract"] == "hydrogen uptake" and rows[1]["abstract"] == ""
    hdr = "frame_id,decision,exclusion_code,stratum,evidence\n"
    (d / "screen_a.csv").write_text(
        hdr + "W1,include,,S2,\nW2,exclude,not_carbon,,\nW3,uncertain,,S2,\n"
    )
    (d / "screen_b.csv").write_text(
        hdr + "W1,include,,S2,\nW2,exclude,not_carbon,,\nW3,include,,S2,\n"
    )
    assert rs.main(["setb-build", "--dir", str(d)]) == 0
    setb = list(csv.DictReader((d / "set_b.csv").open()))
    assert [
        (r["frame_id"], r["has_abstract"], r["include_both"], r["doi"]) for r in setb
    ] == [("W1", "true", "true", "10.1/a"), ("W3", "false", "false", "")]
    index = rs._merged_index(
        [
            {
                "openalex_id": "https://openalex.org/W1",
                "doi": "",
                "title": "x",
                "year": "2010",
            }
        ]
    )
    refs_b = [
        {
            "id": "W1",
            "openalex_id": "W1",
            "doi": "",
            "title": "",
            "year": "",
            "indexed": True,
            "has_abstract": True,
        },
        {
            "id": "W3",
            "openalex_id": "W3",
            "doi": "",
            "title": "Hydrogen on carbon B",
            "year": "2012",
            "indexed": True,
            "has_abstract": False,
        },
    ]
    block = rs.recall_block(refs_b, index)
    assert block["recall"] == 0.5
    assert block["without_abstract"] == {"n": 1, "found": 0, "recall": 0.0}
    assert block["misses"][0]["reason"] == "indexed without abstract"
