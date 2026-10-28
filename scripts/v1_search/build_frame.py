"""Build the sampling frame from the merged search and the two screenings
(docs/v1_protocol.md §6, §7).

Inputs
  references/v1_search/merged_records.csv   written by merge_search.py; its
                                            SHA-256 must equal merged_sha256 in
                                            merge_counts.json
  references/v1_screening/screen_a.csv      one row per merged record, per
  references/v1_screening/screen_b.csv      screener (format below)
  references/v1_screening/stratum_tiebreak.csv
                                            the third agent's stratum, needed
                                            only for records whose two flags
                                            disagree

Screening file columns: frame_id, decision, exclusion_code, stratum, evidence.
  decision        include / uncertain / exclude
  exclusion_code  required with exclude, and one of the five codes §6 allows
                  at this stage; empty otherwise
  stratum         S1 or S2, required unless the decision is exclude, and empty
                  with exclude
  evidence        free text; not read by this script

Tiebreak file columns: frame_id, stratum.

Rules
  - A record enters the frame unless both screeners exclude it (§6).
  - Its stratum is the one flag set if only one screener set a flag, the common
    flag if both agree, and the tiebreak if they disagree (§6).

Outputs
  references/v1_search/frame.csv              every frame record, sorted by
                                              frame_id
  references/v1_screening/double_excluded.csv records both screeners
                                              excluded, sorted by frame_id
                                              (the §6 author-audit population)
  references/v1_search/frame_counts.json      counts, Cohen's kappa, SHA-256

Every output depends only on the inputs, so a re-run reproduces them byte for
byte (§7). draw_order.py checks this before it computes the permutation.

    python3 scripts/v1_search/build_frame.py
    python3 scripts/v1_search/build_frame.py tiebreak-input OUT.csv
        writes the stratum tiebreaker's input: frame_id, title, abstract and
        the two flags of every record whose two flags disagree
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEARCH_DIR = ROOT / "references" / "v1_search"
SCREEN_DIR = ROOT / "references" / "v1_screening"

DECISIONS = ("include", "uncertain", "exclude")
TA_EXCLUSION_CODES = (
    "theoretical_only",
    "electrochemical",
    "not_carbon",
    "not_primary",
    "retracted",
)
STRATA = ("S1", "S2")
FRAME_COLUMNS = (
    "frame_id",
    "stratum",
    "stratum_source",
    "decision_a",
    "decision_b",
    "doi",
    "openalex_id",
    "s2_id",
    "year",
    "title",
)


class FrameError(RuntimeError):
    """An input breaks a §6 or §7 rule; the frame is not written."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_merged(search_dir: Path) -> list[dict[str, str]]:
    merged = search_dir / "merged_records.csv"
    counts = json.loads((search_dir / "merge_counts.json").read_text(encoding="utf-8"))
    if sha256_file(merged) != counts["merged_sha256"]:
        raise FrameError("merged_records.csv does not match merge_counts.json")
    return read_csv(merged)


def load_screen(path: Path, frame_ids: set[str]) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    out: dict[str, dict[str, str]] = {}
    for r in rows:
        fid = r["frame_id"]
        if fid in out:
            raise FrameError(f"{path.name}: {fid} screened twice")
        d, code, stratum = r["decision"], r["exclusion_code"], r["stratum"]
        if d not in DECISIONS:
            raise FrameError(f"{path.name}: {fid} has decision {d!r}")
        if d == "exclude":
            if code not in TA_EXCLUSION_CODES:
                raise FrameError(f"{path.name}: {fid} excluded with code {code!r}")
            if stratum:
                raise FrameError(f"{path.name}: {fid} excluded but given a stratum")
        else:
            if code:
                raise FrameError(f"{path.name}: {fid} not excluded but has a code")
            if stratum not in STRATA:
                raise FrameError(f"{path.name}: {fid} has stratum {stratum!r}")
        out[fid] = r
    missing = frame_ids - out.keys()
    extra = out.keys() - frame_ids
    if missing or extra:
        raise FrameError(
            f"{path.name}: {len(missing)} merged records unscreened, "
            f"{len(extra)} unknown frame_ids"
        )
    return out


def cohen_kappa(a: list[bool], b: list[bool]) -> float | None:
    """Cohen's kappa for two binary ratings (§6: include-or-uncertain vs exclude)."""
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    if pe == 1:
        return None
    return (po - pe) / (1 - pe)


def csv_bytes(columns: tuple[str, ...], rows: list[dict[str, str]]) -> bytes:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(columns), lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in columns})
    return buf.getvalue().encode("utf-8")


def build(
    search_dir: Path = SEARCH_DIR, screen_dir: Path = SCREEN_DIR
) -> dict[str, bytes]:
    """Return {relative output path: bytes} without writing anything."""
    merged = load_merged(search_dir)
    ids = {r["frame_id"] for r in merged}
    a = load_screen(screen_dir / "screen_a.csv", ids)
    b = load_screen(screen_dir / "screen_b.csv", ids)
    tie_path = screen_dir / "stratum_tiebreak.csv"
    tiebreak = (
        {r["frame_id"]: r["stratum"] for r in read_csv(tie_path)}
        if tie_path.exists()
        else {}
    )

    frame, double_excluded, unresolved = [], [], []
    for rec in sorted(merged, key=lambda r: r["frame_id"]):
        fid = rec["frame_id"]
        ra, rb = a[fid], b[fid]
        if ra["decision"] == "exclude" and rb["decision"] == "exclude":
            double_excluded.append({"frame_id": fid})
            continue
        flags = [r["stratum"] for r in (ra, rb) if r["decision"] != "exclude"]
        if len(flags) == 1:
            stratum, source = flags[0], "a" if ra["decision"] != "exclude" else "b"
        elif flags[0] == flags[1]:
            stratum, source = flags[0], "agreed"
        elif fid in tiebreak:
            stratum, source = tiebreak[fid], "tiebreak"
            if stratum not in STRATA:
                raise FrameError(f"stratum_tiebreak.csv: {fid} has {stratum!r}")
        else:
            unresolved.append(fid)
            continue
        frame.append(
            {
                "frame_id": fid,
                "stratum": stratum,
                "stratum_source": source,
                "decision_a": ra["decision"],
                "decision_b": rb["decision"],
                **{
                    k: rec.get(k, "")
                    for k in ("doi", "openalex_id", "s2_id", "year", "title")
                },
            }
        )
    if unresolved:
        raise FrameError(
            f"{len(unresolved)} records need a stratum tiebreak, first {unresolved[0]}"
        )
    unused = set(tiebreak) - {
        r["frame_id"] for r in frame if r["stratum_source"] == "tiebreak"
    }
    if unused:
        raise FrameError(
            f"stratum_tiebreak.csv has {len(unused)} records without a disagreement"
        )

    frame_b = csv_bytes(FRAME_COLUMNS, frame)
    order = sorted(ids)
    kappa = cohen_kappa(
        [a[f]["decision"] != "exclude" for f in order],
        [b[f]["decision"] != "exclude" for f in order],
    )
    frame_sha = hashlib.sha256(frame_b).hexdigest()
    counts = {
        "merged": len(merged),
        "double_excluded": len(double_excluded),
        "frame": len(frame),
        "frame_S1": sum(r["stratum"] == "S1" for r in frame),
        "frame_S2": sum(r["stratum"] == "S2" for r in frame),
        "stratum_tiebreaks": sum(r["stratum_source"] == "tiebreak" for r in frame),
        "kappa_include_or_uncertain_vs_exclude": kappa,
        "frame_sha256": frame_sha,
    }
    return {
        "references/v1_search/frame.csv": frame_b,
        "references/v1_screening/double_excluded.csv": csv_bytes(
            ("frame_id",), double_excluded
        ),
        "references/v1_search/frame_counts.json": (
            json.dumps(counts, indent=2) + "\n"
        ).encode(),
    }


TIEBREAK_COLUMNS = ("frame_id", "title", "abstract", "flag_1", "flag_2")


def tiebreak_input(
    search_dir: Path = SEARCH_DIR, screen_dir: Path = SCREEN_DIR
) -> bytes:
    """The stratum tiebreaker's input (§6): every record both screeners kept
    with different strata, with only its title, abstract and the two flags.
    The flags are written in sorted order, so neither is marked as screener A's
    or B's."""
    merged = load_merged(search_dir)
    ids = {r["frame_id"] for r in merged}
    a = load_screen(screen_dir / "screen_a.csv", ids)
    b = load_screen(screen_dir / "screen_b.csv", ids)
    rows = []
    for rec in sorted(merged, key=lambda r: r["frame_id"]):
        ra, rb = a[rec["frame_id"]], b[rec["frame_id"]]
        if "exclude" in (ra["decision"], rb["decision"]):
            continue
        if ra["stratum"] != rb["stratum"]:
            f1, f2 = sorted((ra["stratum"], rb["stratum"]))
            rows.append({"frame_id": rec["frame_id"], "title": rec["title"],
                         "abstract": rec["abstract"], "flag_1": f1, "flag_2": f2})
    return csv_bytes(TIEBREAK_COLUMNS, rows)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["tiebreak-input"]:
        if len(argv) != 2:
            print("usage: build_frame.py tiebreak-input OUT.csv", file=sys.stderr)
            return 2
        try:
            data = tiebreak_input()
        except FrameError as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 1
        Path(argv[1]).write_bytes(data)
        n = len(list(csv.reader(io.StringIO(data.decode("utf-8"))))) - 1
        print(f"{n} records for the stratum tiebreak")
        return 0
    try:
        outputs = build()
    except FrameError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    for rel, data in outputs.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(outputs["references/v1_search/frame_counts.json"].decode(), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
