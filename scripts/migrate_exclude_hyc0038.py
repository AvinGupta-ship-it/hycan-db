#!/usr/bin/env python3
"""One-off migration: exclude HYC-0038 at full-text review.

Applies docs/migration_exclude_hyc0038_plan.md and nothing else. Changes exactly
three cells of exactly one row of references/paper_tracking.csv
(screening_decision, exclusion_reason, notes), byte-preserving every other line.
The file is CRLF; this script reads and writes raw lines and re-serialises only
the HYC-0038 line through csv, so every line it does not name is byte-identical by
construction and verify() asserts that as bytes.

Refuses to run twice: if HYC-0038 is already `exclude`, it reports and exits 0
without writing.
"""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

TRACKING = Path("references/paper_tracking.csv")
PAPER = "HYC-0038"
NEW_DECISION = "exclude"
NEW_REASON = "no_experimental_uptake"
NOTE_APPEND = (
    "EXCLUDED at full-text review 2026-10-02 (ratified): no extractable experimental "
    "(T, P, uptake) measurement -- all uptake isotherms are GCMC-simulated; the only "
    "experimental H2 result is an adsorption energy (~9 kJ/mol, Fig 6d, from 77 K/87 K "
    "isotherms), with no pressure axis and no anchored uptake value. Kept in the "
    "bibliography for PRISMA (manual 7.5). SI could rescue it later."
)


def split_raw(path: Path) -> tuple[list[str], str]:
    raw = path.read_bytes()
    crlf = raw.count(b"\r\n")
    lone = raw.count(b"\n") - crlf
    if crlf and lone:
        raise SystemExit(f"refusing: {path} has mixed terminators ({crlf} CRLF, {lone} LF)")
    term = "\r\n" if crlf else "\n"
    text = raw.decode("utf-8")
    # keep the terminator on each line so non-target lines stay byte-identical
    lines = text.split(term)
    return lines, term


def main() -> int:
    if not TRACKING.exists():
        raise SystemExit(f"refusing: {TRACKING} not found (run from repo root)")
    lines, term = split_raw(TRACKING)
    header = next(csv.reader([lines[0]]))
    idx = {name: i for i, name in enumerate(header)}
    for col in ("paper_id", "screening_decision", "exclusion_reason", "notes"):
        if col not in idx:
            raise SystemExit(f"refusing: column {col!r} not in header")

    target_i = None
    for i, line in enumerate(lines):
        if not line:
            continue
        # cheap prefix test before paying for a csv parse
        if line.startswith(PAPER + ","):
            target_i = i
            break
    if target_i is None:
        raise SystemExit(f"refusing: {PAPER} row not found")

    row = next(csv.reader([lines[target_i]]))
    if row[idx["screening_decision"]] == NEW_DECISION:
        print(f"{PAPER} already screening_decision={NEW_DECISION}; nothing to do.")
        return 0
    if row[idx["screening_decision"]] != "include":
        raise SystemExit(
            f"refusing: {PAPER} screening_decision is "
            f"{row[idx['screening_decision']]!r}, expected 'include'"
        )

    before = list(row)
    row[idx["screening_decision"]] = NEW_DECISION
    row[idx["exclusion_reason"]] = NEW_REASON
    existing = row[idx["notes"]].strip()
    row[idx["notes"]] = (existing + " " if existing else "") + NOTE_APPEND

    buf = io.StringIO()
    csv.writer(buf, lineterminator="").writerow(row)
    new_line = buf.getvalue()

    print(f"{TRACKING}: {PAPER} (line {target_i + 1})")
    print(f"  screening_decision {before[idx['screening_decision']]!r} -> {NEW_DECISION!r}")
    print(f"  exclusion_reason   {before[idx['exclusion_reason']]!r} -> {NEW_REASON!r}")
    print("  notes += full-text-review record")

    if "--dry-run" in sys.argv:
        print("\n--dry-run: nothing written.")
        return 0

    new_lines = list(lines)
    new_lines[target_i] = new_line
    TRACKING.write_text(term.join(new_lines), encoding="utf-8")

    # verify: re-read, assert only the target line changed, as bytes
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
    assert chk[idx["screening_decision"]] == NEW_DECISION
    assert chk[idx["exclusion_reason"]] == NEW_REASON
    assert NOTE_APPEND in chk[idx["notes"]]
    print("\nwrote and verified: exactly one row changed, three cells, rest byte-identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
