"""Tests for scripts/stage_phase_d_pdfs.py.

The failure that matters here is not "failed to identify a PDF" -- that is
recoverable by hand in ten seconds. It is **naming a PDF with the wrong
paper_id**, which would send a verifier to the wrong paper and make every cell
it checked wrong for a reason nothing downstream could detect. So most of these
tests are about the script REFUSING rather than about it succeeding.

Every test carries a ``MUTATION:`` line naming the defect it would catch, per
manual §6.7.

Validated against reality as well as fixtures: run against the 23 real corpus
PDFs with publisher-style scrambled filenames, the script identified 21 and
misidentified 0, refusing the two scanned papers whose DOI is absent from the
text layer and whose titles were ambiguous.
"""

from __future__ import annotations

import importlib.util
import json
import zlib
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = _ROOT / "scripts" / "stage_phase_d_pdfs.py"

_spec = importlib.util.spec_from_file_location("stage_phase_d_pdfs", SCRIPT)
assert _spec and _spec.loader
stage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage)


# --- fixtures ---------------------------------------------------------------

def make_pdf(path: Path, body: str, *, compress: bool = False) -> None:
    """A file with a PDF header and one stream holding `body`.

    Not a valid PDF -- the script reads bytes and inflates streams rather than
    parsing structure, so this exercises the real code path. `compress=True`
    puts the text behind zlib, which is how a real publisher PDF stores it.
    """
    payload = body.encode("latin-1")
    if compress:
        payload = zlib.compress(payload)
    path.write_bytes(b"%PDF-1.7\n" + b"stream\n" + payload + b"\nendstream\n%%EOF")


BODY_FILLER = (
    "introduction experimental results discussion conclusions references "
    "samples were prepared characterised measured apparatus temperature "
    "pressure isotherm surface area micropore volume nitrogen desorption "
    "figure table shows reported values obtained procedure described above "
) * 4


def entry(pid: str, doi: str, title: str, authors: str = "Ada Lovelace; B Other",
          year: str = "2020") -> dict:
    return {
        "paper_id": pid, "doi": doi, "title": title, "authors": authors,
        "year": year, "journal": "J. Testing", "oa_status": "gold",
        "funnel": "77K_BET", "cand_id": "A1-01", "notes": "n",
        "provenance": {"verdict": "confirmed"},
    }


PAPERS = [
    entry("HYC-0031", "10.1038/s41467-017-01633-x",
          "Oxygen-rich microporous carbons with exceptional hydrogen storage capacity",
          "L. Scott Blankenship; Robert Mokaya", "2017"),
    entry("HYC-0034", "10.1016/j.ijhydene.2016.03.023",
          "Nitrogen-doped porous carbons with high performance for hydrogen storage",
          "Ziqiang Wang; Lixian Sun", "2016"),
    entry("HYC-0051", "10.1016/s0008-6223(01)00051-3",
          "Hydrogen storage capacity of carbon nanotubes filaments and vapor "
          "grown fibers",
          "Gary G. Tibbetts; C. P. Beetz", "2001"),
]


@pytest.fixture()
def bench(tmp_path: Path):
    screening = tmp_path / "screening.json"
    screening.write_text(json.dumps({"papers": PAPERS}), encoding="utf-8")
    src = tmp_path / "downloads"
    src.mkdir()
    out = tmp_path / "staged"
    return screening, src, out


def run(bench, *extra: str) -> int:
    screening, src, out = bench
    return stage.main([str(src), "--screening", str(screening),
                       "--out", str(out), *extra])


# --- DOI extraction ---------------------------------------------------------

def test_finds_a_doi_in_plain_bytes(tmp_path: Path):
    """MUTATION: search only inflated streams, not the raw bytes -> this fails."""
    p = tmp_path / "a.pdf"
    make_pdf(p, "see doi:10.1038/s41467-017-01633-x for details")
    assert "10.1038/s41467-017-01633-x" in stage.dois_in_pdf(p)


def test_finds_a_doi_inside_a_compressed_stream(tmp_path: Path):
    """Real publisher PDFs store text behind zlib.

    MUTATION: drop _inflate_streams -> this fails.
    """
    p = tmp_path / "b.pdf"
    make_pdf(p, "https://doi.org/10.1016/j.ijhydene.2016.03.023", compress=True)
    assert "10.1016/j.ijhydene.2016.03.023" in stage.dois_in_pdf(p)


def test_strips_trailing_text_a_doi_swallowed(tmp_path: Path):
    """A DOI captured from running text picks up what followed it.

    MUTATION: return the regex match without _clean_doi -> this fails.
    """
    p = tmp_path / "c.pdf"
    make_pdf(p, "10.1021/ja8083225Downloaded from pubs.acs.org")
    assert "10.1021/ja8083225" in stage.dois_in_pdf(p)


def test_a_broken_stream_does_not_abort_the_file(tmp_path: Path):
    """MUTATION: let zlib.error propagate out of _inflate_streams -> this fails."""
    p = tmp_path / "d.pdf"
    p.write_bytes(
        b"%PDF-1.7\nstream\n" + b"\x00\x01not-zlib\xff" + b"\nendstream\n"
        b"stream\n" + zlib.compress(b"10.1038/s41467-017-01633-x") + b"\nendstream\n"
    )
    assert "10.1038/s41467-017-01633-x" in stage.dois_in_pdf(p)


# --- naming -----------------------------------------------------------------

def test_target_name_matches_the_corpus_convention():
    """The existing 23 PDFs are HYC-00NN_surnameYEAR.pdf.

    MUTATION: use the first author's given name, or drop the paper_id prefix
    -> this fails.
    """
    assert stage.target_name(PAPERS[0]) == "HYC-0031_blankenship2017.pdf"
    assert stage.target_name(PAPERS[2]) == "HYC-0051_tibbetts2001.pdf"


def test_target_name_survives_an_accented_surname():
    """MUTATION: drop the NFKD fold in normalise -> this fails."""
    e = entry("HYC-0041", "10.1/x", "T", "Arturo Morandé; Other", "2023")
    assert stage.target_name(e) == "HYC-0041_morande2023.pdf"


# --- the safety property: refuse rather than mislabel -----------------------

def test_identifies_and_stages_a_matching_pdf(bench):
    """MUTATION: never copy -> this fails."""
    screening, src, out = bench
    make_pdf(src / "1-s2.0-S0360319916303xxx-main.pdf",
             "doi 10.1016/j.ijhydene.2016.03.023", compress=True)
    assert run(bench) == 0
    assert (out / "HYC-0034_wang2016.pdf").exists()


def test_refuses_a_pdf_whose_doi_is_not_in_the_list(bench):
    """A PDF for some other paper must not be given any id.

    MUTATION: fall through to the highest title score with no threshold
    -> this fails.
    """
    screening, src, out = bench
    make_pdf(src / "unrelated.pdf", "doi 10.9999/not.in.the.list", compress=True)
    assert run(bench) == 0
    assert not out.exists() or not list(out.glob("*.pdf"))


def test_refuses_when_two_papers_dois_are_both_present(bench):
    """A review citing several corpus papers must not be filed as one of them.

    MUTATION: take exact[0] without checking the id set -> this fails.
    """
    screening, src, out = bench
    make_pdf(src / "review.pdf",
             "cites 10.1038/s41467-017-01633-x and 10.1016/j.ijhydene.2016.03.023",
             compress=True)
    assert run(bench) == 0
    assert not out.exists() or not list(out.glob("*.pdf"))


def test_refuses_a_pdf_with_no_extractable_text(bench, capsys):
    """A scan with no text layer. Two of the real 23 are exactly this.

    Asserts the REASON, not only the outcome: without the empty-text guard the
    title scores are all zero and the threshold refuses anyway, so checking
    "nothing was staged" cannot tell the two guards apart. The operator needs
    to be told it is a scan, not that nothing scored well.

    MUTATION: remove the `if not blob.strip()` guard -> this fails.
    """
    screening, src, out = bench
    (src / "scan.pdf").write_bytes(b"%PDF-1.4\n" + bytes(400) + b"\n%%EOF")
    assert run(bench) == 0
    assert not out.exists() or not list(out.glob("*.pdf"))
    assert "no text layer" in capsys.readouterr().out


def test_refuses_the_second_pdf_claiming_the_same_paper(bench, capsys):
    """Two downloads of one paper must not both be staged.

    The duplicate must be reported as NOT IDENTIFIED. Asserting only that one
    file exists cannot isolate this: with the bookkeeping gone, the second copy
    is still skipped by the never-overwrite guard, so the file count is right
    for the wrong reason and the operator is told the duplicate succeeded.

    MUTATION: drop the `claimed` bookkeeping -> this fails.
    """
    screening, src, out = bench
    body = "doi 10.1016/j.ijhydene.2016.03.023"
    make_pdf(src / "first.pdf", body, compress=True)
    make_pdf(src / "second (1).pdf", body, compress=True)
    assert run(bench) == 0
    assert len(list(out.glob("*.pdf"))) == 1
    report = capsys.readouterr().out
    assert "NOT IDENTIFIED (1)" in report
    assert "already matched by" in report


def test_title_fallback_identifies_a_pdf_with_no_doi(bench):
    """One real corpus PDF prints no DOI and was recovered this way.

    MUTATION: remove the title fallback -> this fails.
    """
    screening, src, out = bench
    make_pdf(src / "noDOI.pdf",
             "Hydrogen storage capacity of carbon nanotubes filaments and "
             "vapor grown fibers Tibbetts Beetz "
             # A real paper has hundreds of words. MIN_TEXT_WORDS rejects a file
             # with almost none, so a two-line fixture would be refused as a
             # scan and would test the wrong branch.
             + BODY_FILLER, compress=True)
    assert run(bench) == 0
    assert (out / "HYC-0051_tibbetts2001.pdf").exists()


def test_a_short_file_is_reported_as_a_scan_not_as_a_weak_match(bench, capsys):
    """MIN_TEXT_WORDS must be what rejects a text-free file.

    MUTATION: set MIN_TEXT_WORDS to 0 -> this fails.
    """
    screening, src, out = bench
    make_pdf(src / "tiny.pdf", "abcd efgh ijkl", compress=True)
    assert run(bench) == 0
    assert "no text layer" in capsys.readouterr().out


def test_title_fallback_will_not_fire_on_generic_words_alone(bench):
    """"hydrogen storage carbon" must not identify anything.

    MUTATION: drop STOPWORDS, or lower the 0.75 threshold -> this fails.
    """
    screening, src, out = bench
    make_pdf(src / "generic.pdf",
             "hydrogen storage in carbon materials a study of the effect "
             + BODY_FILLER, compress=True)
    assert run(bench) == 0
    assert not out.exists() or not list(out.glob("*.pdf"))


# --- non-destructiveness ----------------------------------------------------

def test_never_modifies_or_removes_an_input(bench):
    """MUTATION: shutil.move instead of copy2 -> this fails."""
    screening, src, out = bench
    p = src / "keep.pdf"
    make_pdf(p, "doi 10.1016/j.ijhydene.2016.03.023", compress=True)
    before = p.read_bytes()
    assert run(bench) == 0
    assert p.exists() and p.read_bytes() == before


def test_never_overwrites_an_existing_staged_file(bench):
    """MUTATION: copy unconditionally -> this fails."""
    screening, src, out = bench
    make_pdf(src / "x.pdf", "doi 10.1016/j.ijhydene.2016.03.023", compress=True)
    out.mkdir()
    dest = out / "HYC-0034_wang2016.pdf"
    dest.write_bytes(b"PRECIOUS")
    assert run(bench) == 0
    assert dest.read_bytes() == b"PRECIOUS"


def test_dry_run_copies_nothing(bench):
    """MUTATION: let --dry-run fall through -> this fails."""
    screening, src, out = bench
    make_pdf(src / "x.pdf", "doi 10.1016/j.ijhydene.2016.03.023", compress=True)
    assert run(bench, "--dry-run") == 0
    assert not out.exists()


def test_refuses_a_screening_file_missing_a_required_field(tmp_path: Path):
    """MUTATION: drop the required-key loop in load_papers -> this fails."""
    bad = tmp_path / "s.json"
    broken = dict(PAPERS[0])
    broken["doi"] = ""
    bad.write_text(json.dumps({"papers": [broken]}), encoding="utf-8")
    with pytest.raises(stage.StagingError):
        stage.load_papers(bad)


def test_empty_source_folder_is_not_an_error(bench):
    """MUTATION: return 1 on an empty folder -> this fails."""
    assert run(bench) == 0


# --- the real artifact ------------------------------------------------------

def test_every_real_screening_entry_yields_a_distinct_filename():
    """35 papers must not collide on a filename.

    MUTATION: drop the paper_id from target_name -> this fails, because two
    Masika 2013 papers are in the list.
    """
    papers = stage.load_papers(_ROOT / "references" / "phase_d_screening.json")
    names = [stage.target_name(p) for p in papers]
    assert len(set(names)) == len(names) == 35
    assert all(n.startswith("HYC-00") and n.endswith(".pdf") for n in names)


# --- the matcher's three tuning knobs, each pinned ---------------------------

def test_stopwords_exclude_the_field_vocabulary():
    """STOPWORDS is what stops "hydrogen storage carbon" identifying anything.

    Pinned as a unit test because it is a property of the word list, not of any
    one PDF: with the list empty, a title's score is carried by words every
    paper in this corpus contains.

    MUTATION: empty STOPWORDS -> this fails.
    """
    tokens = stage.title_tokens(
        "Hydrogen storage and adsorption in porous carbon materials"
    )
    for common in ("hydrogen", "storage", "adsorption", "carbon", "materials"):
        assert common not in tokens, f"{common!r} must not count toward a match"
    assert "porous" in tokens


def test_a_title_too_short_to_be_distinctive_is_not_matched_on(bench):
    """A two-word title cannot identify a paper, so it must be skipped.

    MUTATION: lower MIN_TITLE_TOKENS to 1 -> this fails.
    """
    screening, src, out = bench
    short = entry("HYC-0099", "10.1/short", "Porous Carbons", "Solo Author", "2022")
    screening.write_text(json.dumps({"papers": [short]}), encoding="utf-8")
    make_pdf(src / "p.pdf", "porous carbons " + BODY_FILLER, compress=True)
    assert run(bench) == 0
    assert not out.exists() or not list(out.glob("*.pdf"))


def test_refuses_two_papers_whose_titles_both_score_high(bench, capsys):
    """Near-identical titles must produce a refusal, not a coin flip.

    The margin requirement is the only thing standing between a pair of
    companion papers from one group and a confidently wrong filename.

    MUTATION: drop `best[0] - second[0] >= 0.25` -> this fails.
    """
    screening, src, out = bench
    a = entry("HYC-0097", "10.1/a",
              "Templating of carbon in zeolites under pressure part one",
              "Norah Balahmar", "2016")
    b = entry("HYC-0098", "10.1/b",
              "Templating of carbon in zeolites under pressure part two",
              "Norah Balahmar", "2017")
    screening.write_text(json.dumps({"papers": [a, b]}), encoding="utf-8")
    make_pdf(src / "p.pdf",
             "Templating of carbon in zeolites under pressure part "
             + BODY_FILLER, compress=True)
    assert run(bench) == 0
    assert not out.exists() or not list(out.glob("*.pdf"))
    assert "ambiguous" in capsys.readouterr().out
