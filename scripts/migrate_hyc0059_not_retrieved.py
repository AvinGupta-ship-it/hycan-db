#!/usr/bin/env python3
"""One-off migration: mark HYC-0059 (Guo 2023, Mater. Today Chem.) as full-text NOT RETRIEVED.

Why: the file held under references/HYC-0059_guo2023.pdf is the wrong paper -- its bytes are the
Harisankar et al. 2025 CNT *review* (Korean J. Chem. Eng. 42:13-42), not Guo et al. 2023
(Mater. Today Chem. 30, 101508) which paper_tracking and the filename name. UNT has no access to
the Guo full text. So HYC-0059 stays screening_decision=include but pdf_obtained -> no, joining the
five RSC not-retrieved papers (HYC-0035/0036/0054/0055/0056) on the PRISMA 'reports not retrieved'
line (HANDOFF; manual S7.5). This is a retrieval failure, NOT a screening exclusion -- do not touch
screening_decision or exclusion_reason.

Changes exactly two cells of exactly one row (pdf_obtained, notes), byte-preserving every other line.
Mirrors scripts/migrate_exclude_hyc0038.py. Refuses to run twice.
"""
from __future__ import annotations
import csv, io, sys
from pathlib import Path

TRACKING = Path("references/paper_tracking.csv")
PAPER = "HYC-0059"
NOTE_APPEND = (
    "FULL TEXT NOT RETRIEVED 2026-10-05: UNT has no access to Guo et al. 2023 (Mater. Today Chem. 30, "
    "101508, DOI 10.1016/j.mtchem.2023.101508). The file held as HYC-0059_guo2023.pdf is a MISFILE -- "
    "its contents are the Harisankar et al. 2025 review (Korean J. Chem. Eng. 42:13-42), not Guo. "
    "pdf_obtained set to no; stays screening_decision=include on the PRISMA 'reports not retrieved' "
    "line with HYC-0035/0036/0054/0055/0056 (manual 7.5). Not an exclusion."
)


def split_raw(path: Path) -> tuple[list[str], str]:
    raw = path.read_bytes()
    crlf = raw.count(b"\r\n")
    lone = raw.count(b"\n") - crlf
    if crlf and lone:
        raise SystemExit(f"refusing: {path} has mixed terminators ({crlf} CRLF, {lone} LF)")
    term = "\r\n" if crlf else "\n"
    return raw.decode("utf-8").split(term), term


def main() -> int:
    if not TRACKING.exists():
        raise SystemExit(f"refusing: {TRACKING} not found (run from repo root)")
    lines, term = split_raw(TRACKING)
    header = next(csv.reader([lines[0]]))
    idx = {name: i for i, name in enumerate(header)}
    for col in ("paper_id", "screening_decision", "pdf_obtained", "notes"):
        if col not in idx:
            raise SystemExit(f"refusing: column {col!r} not in header")

    target_i = next((i for i, ln in enumerate(lines) if ln.startswith(PAPER + ",")), None)
    if target_i is None:
        raise SystemExit(f"refusing: {PAPER} row not found")
    row = next(csv.reader([lines[target_i]]))
    if row[idx["pdf_obtained"]] == "no" or NOTE_APPEND[:40] in row[idx["notes"]]:
        print(f"{PAPER} already marked not-retrieved; nothing to do.")
        return 0
    if row[idx["screening_decision"]] != "include":
        raise SystemExit(f"refusing: {PAPER} screening_decision is {row[idx['screening_decision']]!r}, expected 'include'")

    before_pdf = row[idx["pdf_obtained"]]
    row[idx["pdf_obtained"]] = "no"
    existing = row[idx["notes"]].strip()
    row[idx["notes"]] = (existing + " " if existing else "") + NOTE_APPEND
    buf = io.StringIO(); csv.writer(buf, lineterminator="").writerow(row); new_line = buf.getvalue()

    print(f"{TRACKING}: {PAPER} (line {target_i + 1})")
    print(f"  pdf_obtained {before_pdf!r} -> 'no'")
    print("  notes += not-retrieved record")
    print(f"  screening_decision kept {row[idx['screening_decision']]!r}; exclusion_reason untouched")
    if "--dry-run" in sys.argv:
        print("\n--dry-run: nothing written."); return 0

    new_lines = list(lines); new_lines[target_i] = new_line
    TRACKING.write_text(term.join(new_lines), encoding="utf-8")
    back, _ = split_raw(TRACKING)
    if len(back) != len(lines):
        raise SystemExit("post-condition FAILED: line count changed")
    for i, (a, b) in enumerate(zip(lines, back)):
        if i == target_i:
            if b != new_line:
                raise SystemExit("post-condition FAILED: target line not written as intended")
        elif a != b:
            raise SystemExit(f"post-condition FAILED: line {i + 1} changed but should not have")
    chk = next(csv.reader([back[target_i]]))
    assert chk[idx["pdf_obtained"]] == "no" and NOTE_APPEND[:40] in chk[idx["notes"]]
    assert chk[idx["screening_decision"]] == "include"
    print("\nwrote and verified: exactly one row changed, two cells, rest byte-identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
