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
    # +HYC-0038: screened in at title/abstract, full text obtained, then excluded at
    # full-text review (all uptake isotherms are GCMC-simulated; the only experimental
    # result is an adsorption energy, so no (T, P, uptake) value is extractable). Kept
    # here because PRISMA needs its citation. See docs/migration_exclude_hyc0038_plan.md.
    assert excluded == ["HYC-0010", "HYC-0028", "HYC-0030", "HYC-0038"]
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
    # "citing_pdf": resolved from the reference list(s) of held PDFs that cite the work
    # (and corroborated by the publisher DOI record). Added for HYC-0046, whose own held
    # PDF is a preprint (UCRL-JRNL-227848) that prints no volume/issue/pages/year, and
    # whose citation was read from HYC-0047 ref [42] and HYC-0044 ref [17] because the
    # OpenAlex/Semantic Scholar/Crossref APIs were unreachable from the extraction session.
    allowed = {"pdf", "openalex", "semanticscholar", "openalex+semanticscholar",
               "citing_pdf", "none"}
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
    # 23 for the original corpus, plus HYC-0031, the first Phase D paper
    # whose full text was obtained and extracted (2026-09-30); plus the
    # 2026-10-02 Phase D batch HYC-0032/0033/0034/0037, all PDF-held; plus the
    # HYC-0039/0040/0041/0042/0043 batch (5) and HYC-0038 (excluded but PDF-held),
    # all PDF-held: 28 + 6 = 34. Plus the HYC-0044/0045/0046/0047/0048 batch (5), all
    # PDF-held (HYC-0046's is the LLNL preprint): 34 + 5 = 39. Plus the
    # HYC-0049/0050/0051/0052/0053 batch (5), all PDF-held: 39 + 5 = 44. Plus the
    # HYC-0057/0058/0060/0061 batch (4), all PDF-held: 44 + 4 = 48.
    assert sum(1 for r in sources() if r["pdf_held"]) == 48


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
    # +HYC-0043: BioResources prints an issue number in its citation line
    # (14(4), 9755-9765), so its issue is PDF-sourced like Science/JACS/JPCB.
    # +HYC-0045: Prog. Nat. Sci.: Mater. Int. prints its issue (23(3)) in the citation line.
    assert sorted(by_prov["pdf"]) == ["HYC-0002", "HYC-0022", "HYC-0024", "HYC-0043", "HYC-0045"]
    assert len(by_prov["openalex"]) == 21
    # HYC-0046's issue (18(26)) is sourced from held citing PDFs + the DOI record (the
    # services were unreachable), so it sits in its own provenance class.
    assert by_prov["citing_pdf"] == ["HYC-0046"]
    # 6 for the original corpus, plus HYC-0031 (2026-09-30). Nature
    # Communications prints volume and article number in its running head and
    # no issue, so claiming one would be invented -- which is what this
    # partition exists to stop. +4 for the 2026-10-02 Phase D batch: HYC-0033
    # is article-numbered (Scientific Reports, genuinely no issue), while
    # HYC-0032/0034/0037 print no issue on the article and OpenAlex was
    # unreachable from the extraction session, so their issue is omitted
    # pending an OpenAlex backfill (each entry's note says so, and it moves to
    # 'openalex' once the issue is retrieved).
    # +5 for the HYC-0039/0040/0041/0042 included papers and HYC-0038 (excluded):
    # all are MDPI/Elsevier/Frontiers article-number journals that print no issue, so
    # their issue is omitted. 11 + 5 = 16. (HYC-0043 is the batch's one exception; its
    # issue is PDF-sourced, counted under 'pdf' above.)
    # +3 for the HYC-0044/0047/0048 batch papers: MDPI (article-numbered), Elsevier and
    # Springer running heads print no issue, so each is omitted pending an OpenAlex backfill.
    # 16 + 3 = 19. (HYC-0045 is PDF-sourced; HYC-0046 is citing_pdf; both emit their issue.)
    # +5 for the HYC-0049/0050/0051/0052/0053 batch: ACS Langmuir, Springer Adsorption,
    # Elsevier Carbon and IJHE, and RSC J. Mater. Chem. A all print no issue in the article
    # citation line, so each is omitted pending an OpenAlex backfill. 19 + 5 = 24.
    # +4 for the HYC-0057/0058/0060/0061 batch: IOP Nanotechnology and MDPI Processes are
    # article-numbered (no issue), Elsevier IJHE and Carbon running heads print no issue,
    # so each is omitted pending an OpenAlex backfill. 24 + 4 = 28.
    assert len(by_prov["none"]) == 28
    # Match the FIELD, not the word: two of these notes contain the phrase
    # "article number", which a substring test read as an issue field.
    field = re.compile(r"^\s*number\s*=", re.M)
    for pid in by_prov["none"]:
        assert not field.search(entries()[pid]), f"{pid} emits an issue it lacks"
    for pid in by_prov["pdf"] + by_prov["openalex"] + by_prov["citing_pdf"]:
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
