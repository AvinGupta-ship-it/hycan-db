"""Tests for the v1.0 prompt build (scripts/v1_prompts.py), the redacted schema
(scripts/v1_redact_schema.py) and the agents' tools tree
(scripts/v1_tools_tree.py): the built prompts are reproducible, carry no v0.1
paper identifiers, and describe the matching code as it is."""

from __future__ import annotations

import csv
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, REPO_ROOT / "scripts" / f"{name}.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def v01_identifiers():
    with (REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv").open(
        encoding="utf-8"
    ) as fh:
        rows = list(csv.DictReader(fh))
    return {r["paper_id"] for r in rows}, {r["first_author"] for r in rows}


def test_built_prompts_are_reproducible():
    assert load("v1_prompts").main(["v1_prompts.py", "--check"]) == 0


def test_built_prompts_carry_no_v01_paper_identifiers():
    built, _ = load("v1_prompts").build()
    ids, authors = v01_identifiers()
    for name, text in built.items():
        assert not [p for p in ids if p in text], name
        assert not [
            a for a in authors if re.search(rf"\b{re.escape(a)}\b", text)
        ], name


def test_reconcile_prompts_describe_the_matching_code():
    built, _ = load("v1_prompts").build()
    ve = load("v1_extract")
    for role in ("reconcile.md", "reconcile_legacy.md"):
        text = built[role]
        for field in ve.NOT_COMPARED | ve.PRESENCE_ONLY:
            assert f"`{field}`" in text, (role, field)
        assert ve.PRESSURE_DIGITIZED in text
    assert "labels.csv" in built["reconcile_legacy.md"]
    assert "labels.csv" not in built["reconcile.md"]


def test_extraction_prompts_carry_sections_10_1_and_11_0():
    built, _ = load("v1_prompts").build()
    for role in ("extract_A.md", "extract_B.md", "reconcile.md", "legacy_labels.md"):
        assert "### 10.1 Reporting-completeness score" in built[role]
        assert "### 11.0 General rules" in built[role]
    assert "### 11.0 General rules" not in built["screen.md"]


def test_tools_tree_has_no_v01_identifiers_and_no_data():
    files = load("v1_tools_tree").build()
    assert set(files) == set(load("v1_tools_tree").FILES) | {"MANIFEST"}
    assert not any(name.startswith(("data/", "references/")) for name in files)


def test_redaction_is_checked_against_the_registered_schema():
    # Amendment 2 added a selection_route value to the working schema; the
    # frozen prompts carry the registered schema, so the check must not use
    # the working copy.
    spec = importlib.util.spec_from_file_location(
        "v1_redact_schema", REPO_ROOT / "scripts" / "v1_redact_schema.py")
    rs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rs)
    import typing
    registered = typing.get_args(rs.registered_schema().SelectionRoute)
    assert "legacy_v0.1_not_retrieved" not in registered
    assert rs.build()["schema.py"] == (
        REPO_ROOT / "prompts" / "v1" / "schema_v2_redacted" / "schema.py").read_text(encoding="utf-8")
