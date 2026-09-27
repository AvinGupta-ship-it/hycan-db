"""Tests for references/bibliography.bib and scripts/build_bibliography.py.

§3.5 requires every citation to be resolved against a record rather than
recalled. These tests assert that property against the artifacts: the .bib is in
sync with its sources file, every corpus paper has an entry, and every entry's
author surname and year agree with the value the dataset extracted independently
from the same PDF.

That last check is the load-bearing one. It caught two name-splitting bugs that
would each have put a fabricated surname into a published bibliography —
"Y. Y. Fan" rendered as "Y. Fan, Y.", and "Barbara Panella" as "Barbara Panella,
Barbara". Each guard carries a MUTATION: line and each was confirmed to fail
against the mutation it names.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_bibliography.py"
SOURCES = REPO_ROOT / "references" / "bibliography_sources.json"
BIB = REPO_ROOT / "references" / "bibliography.bib"
DATASET = REPO_ROOT / "data" / "raw" / "measurements_v0.1.csv"
DATA_LICENCE = REPO_ROOT / "data" / "LICENSE.md"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import build_bibliography as bb  # noqa: E402


def sources() -> list[dict]:
    return json.loads(SOURCES.read_text(encoding="utf-8"))["papers"]


def entries() -> dict[str, str]:
    text = BIB.read_text(encoding="utf-8")
    return {
        m.group(2): m.group(0)
        for m in re.finditer(r"@(\w+)\{(HYC-\d{4}),.*?\n\}", text, re.S)
    }


def corpus_papers() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with DATASET.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            out.setdefault(row["paper_id"], row)
    return out


# --- the generated file is the generator's output ---------------------------


def test_the_bib_is_in_sync_with_its_sources_file():
    """MUTATION: hand-edit one field in bibliography.bib -> --check exits 1."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_generator_refuses_an_entry_missing_a_required_field():
    """It must never emit a partial citation, and never fill one in.

    MUTATION: drop the `missing` check in `format_entry` -> a record with no year
    emits an entry with no year field and this fails.
    """
    with pytest.raises(bb.BibliographyError, match="missing"):
        bb.format_entry({"paper_id": "HYC-9999", "authors": ["X, Y"], "title": "t"})


def test_the_generator_refuses_a_duplicate_paper_id():
    """MUTATION: drop the `seen` check in `build` -> two entries share a key,
    which silently breaks every citation to it."""
    rec = dict(sources()[0])
    with pytest.raises(bb.BibliographyError, match="duplicate"):
        bb.build([rec, dict(rec)])


# --- coverage ---------------------------------------------------------------


def test_every_corpus_paper_has_an_entry():
    """A row in the dataset with no citable reference is unusable downstream.

    MUTATION: delete a paper from the sources file -> this fails and names it.
    """
    missing = sorted(set(corpus_papers()) - set(entries()))
    assert missing == [], f"corpus papers with no bibliography entry: {missing}"


def test_every_entry_key_is_its_paper_id():
    """The key IS the paper_id, so a citation resolves to the rows it describes.

    MUTATION: switch the generator to author-year keys -> this fails.
    """
    for pid, text in entries().items():
        assert re.match(r"^@\w+\{" + re.escape(pid) + r",", text)


def test_the_screened_out_papers_are_kept_because_prisma_needs_them():
    """MUTATION: filter the sources file to `include` only -> this fails, and the
    PRISMA exclusion list loses its citations."""
    excluded = sorted(
        r["paper_id"] for r in sources() if r["screening_decision"] != "include"
    )
    assert excluded == ["HYC-0010", "HYC-0028", "HYC-0030"]
    for pid in excluded:
        assert pid in entries()
        assert pid not in corpus_papers()

    # Four more were screened IN and have not been extracted yet. They are citable
    # so the manuscript can discuss them, and they are not in the corpus.
    pending = sorted(
        r["paper_id"] for r in sources()
        if r["screening_decision"] == "include" and not r["in_corpus"]
    )
    assert pending == ["HYC-0003", "HYC-0006", "HYC-0008", "HYC-0014"]
    assert len(sources()) == len(corpus_papers()) + len(excluded) + len(pending)


# --- agreement with the dataset, which was extracted independently ----------


def test_every_first_author_surname_matches_the_dataset():
    """The check that caught both name-splitting bugs.

    `first_author` in the dataset was read off the same PDF by a different pass,
    so this is a genuine cross-check rather than a restatement.

    MUTATION: in `split_name`, take `parts[0]` as the given name and the rest as
    the family name -> "Y. Y. Fan" becomes "Y. Fan, Y." and this fails. MUTATION:
    consume the initials but keep all remaining tokens as the family name ->
    "M. Sterlin Leo Hudson" becomes "Sterlin Leo Hudson, M." and this fails too.
    """
    by_id = {r["paper_id"]: r for r in sources()}
    problems = []
    for pid, row in sorted(corpus_papers().items()):
        first = bb.split_name(by_id[pid]["authors"][0])
        if first.startswith("{"):
            continue  # deliberately unsplit; see HYC-0011's note
        surname = first.split(",")[0].strip().lower()
        expected = row["first_author"].strip().lower()
        if surname not in expected and expected not in surname:
            problems.append(f"{pid}: bib={surname!r} dataset={expected!r}")
    assert problems == [], problems


def test_every_year_matches_the_dataset():
    """Six entries would have carried the online-first year from OpenAlex.

    MUTATION: take OpenAlex's year for HYC-0009, HYC-0012, HYC-0018, HYC-0021 or
    HYC-0029 -> that entry is one year low and this fails.
    """
    by_id = {r["paper_id"]: r for r in sources()}
    problems = [
        f"{pid}: bib={by_id[pid]['year']} dataset={row['year']}"
        for pid, row in sorted(corpus_papers().items())
        if str(by_id[pid]["year"]) != str(row["year"])
    ]
    assert problems == [], problems


def test_every_doi_matches_the_dataset():
    """MUTATION: alter a DOI in the sources file -> this fails. A DOI is the one
    field a reader uses to check everything else, so it must agree exactly."""
    by_id = {r["paper_id"]: r for r in sources()}
    problems = [
        f"{pid}: bib={by_id[pid]['doi']!r} dataset={row['doi']!r}"
        for pid, row in sorted(corpus_papers().items())
        if by_id[pid]["doi"].lower() != row["doi"].lower()
    ]
    assert problems == [], problems


# --- provenance is recorded, not assumed -----------------------------------


def test_every_field_of_every_entry_records_where_it_came_from():
    """MUTATION: drop a key from a `provenance` block -> this fails.

    §3.5's requirement is not "the value is right", it is "the value was
    resolved". A field with no recorded provenance is indistinguishable from one
    recalled from memory.
    """
    allowed = {"pdf", "openalex", "semanticscholar", "openalex+semanticscholar", "none"}
    for r in sources():
        prov = r["provenance"]
        for field in ("authors", "title", "journal", "year", "number"):
            assert field in prov, f"{r['paper_id']}: no provenance for {field}"
        for field, value in prov.items():
            if field == "doi":
                continue  # free text naming the resolution path
            assert value in allowed, f"{r['paper_id']}: {field} provenance {value!r}"


def test_author_lists_come_from_the_pdf_wherever_one_is_held():
    """OpenAlex gave HYC-0002 an author who is a different person and gave
    HYC-0011 one author where the article prints four. A service is not the
    record for a byline.

    MUTATION: source an author list from OpenAlex for a paper whose PDF is held
    -> this fails.
    """
    for r in sources():
        if r["pdf_held"]:
            assert r["provenance"]["authors"] == "pdf", r["paper_id"]
    assert sum(1 for r in sources() if r["pdf_held"]) == 23


def test_the_issue_number_provenance_partition_is_pinned():
    """`number` is the weakest field in the file, and this pins exactly how weak.

    Only Science, JACS and J. Phys. Chem. B print an issue number in their
    citation lines; every Elsevier and Springer running head in this corpus
    carries volume, year and pages only. **An earlier version of this test, and
    the .bib header it was written to protect, both asserted that NO pdf printed
    one — over-generalised from the Elsevier majority.** This test failing is what
    caught it, which is the argument for pinning a partition rather than a claim.

    MUTATION: source an issue from a service for HYC-0002, HYC-0022 or HYC-0024
    -> this fails, and three entries silently lose their primary-source issue.
    """
    by_prov: dict[str, list[str]] = {}
    for r in sources():
        by_prov.setdefault(r["provenance"]["number"], []).append(r["paper_id"])
    assert sorted(by_prov["pdf"]) == ["HYC-0002", "HYC-0022", "HYC-0024"]
    assert len(by_prov["openalex"]) == 21
    assert len(by_prov["none"]) == 6
    # Match the FIELD, not the word: two of these notes contain the phrase
    # "article number", which a substring test read as an issue field.
    field = re.compile(r"^\s*number\s*=", re.M)
    for pid in by_prov["none"]:
        assert not field.search(entries()[pid]), f"{pid} emits an issue it lacks"
    for pid in by_prov["pdf"] + by_prov["openalex"]:
        assert field.search(entries()[pid]), f"{pid} has an issue and does not emit it"


def test_the_single_sourced_entries_say_so():
    """Three papers could not be cross-checked because Semantic Scholar was rate
    limited, and one of those has no PDF either.

    MUTATION: drop HYC-0028's note -> this fails, and the one entry in the file
    with no corroboration at all stops saying so.
    """
    by_id = {r["paper_id"]: r for r in sources()}
    assert not by_id["HYC-0028"]["pdf_held"]
    assert "Semantic Scholar could not be reached" in by_id["HYC-0028"]["note"]
    assert by_id["HYC-0028"]["provenance"]["authors"] == "openalex"


def test_hyc0019_is_flagged_as_the_one_pdf_without_citation_fields():
    """Its PDF is an unpaginated manuscript printing only a 2009 copyright line,
    so its year, volume, issue and pages all rest on the services.

    MUTATION: take 2009 from that PDF as the year -> the year-agreement test
    fails; drop the note -> this fails.
    """
    r = {x["paper_id"]: x for x in sources()}["HYC-0019"]
    assert r["pdf_held"] is True
    assert r["year"] == "2010"
    assert r["provenance"]["year"] != "pdf"
    assert r["provenance"]["pages"] != "pdf"
    assert "unpaginated manuscript" in r["note"]


# --- the data licence -------------------------------------------------------


def test_the_data_licence_exists_and_names_cc_by_and_the_mit_boundary():
    """It blocked Zenodo (§16, §6.8) and publishing the dataset under the code's
    MIT licence is hard to unwind after a DOI is minted.

    MUTATION: delete data/LICENSE.md -> this fails.
    """
    assert DATA_LICENCE.is_file()
    text = DATA_LICENCE.read_text(encoding="utf-8")
    assert "CC BY 4.0" in text
    assert "creativecommons.org/licenses/by/4.0/legalcode" in text
    assert "MIT" in text, "the boundary against the root licence must be stated"
    assert "reproducibility_tier" in text, "tier caveat must reach a data reuser"
