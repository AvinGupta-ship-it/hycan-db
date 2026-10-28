"""Split the merged search into screening batches and join the screeners'
outputs (docs/v1_protocol.md §6).

  split    write the screening input for every merged record, in batches of
           --size records in frame_id order:
             <out>/batch_NNN.csv   frame_id, title, abstract, venue, year, type
           Only these six columns reach the screeners; the database's
           retraction flag and every other field stay out (§15 Amendment 1,
           item 3).
  join     concatenate one screener's batch outputs (<dir>/batch_NNN.csv,
           written by the agent from the frozen screen.md prompt) into one
           screening file, after checking that each batch output screens
           exactly its input batch, in order, with valid decisions, codes and
           strata. A batch that fails the check is reported by name: under §9
           it may be rerun only for a technical failure (missing, truncated or
           malformed output), and the rerun is logged.

    python3 scripts/v1_search/screening_batches.py split
        --merged references/v1_search/merged_records.csv --out DIR [--size 250]
    python3 scripts/v1_search/screening_batches.py join --inputs DIR
        --outputs DIR --out references/v1_screening/screen_a.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

SCREEN_COLUMNS = ("frame_id", "title", "abstract", "venue", "year", "type")
OUT_COLUMNS = ("frame_id", "decision", "exclusion_code", "stratum", "evidence")
DECISIONS = ("include", "uncertain", "exclude")
TA_CODES = ("theoretical_only", "electrochemical", "not_carbon", "not_primary", "retracted")
STRATA = ("S1", "S2")


class BatchError(RuntimeError):
    pass


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        return list(r.fieldnames or []), list(r)


def write_csv(path: Path, columns, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(columns), lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in columns})


def cmd_split(args) -> int:
    _, merged = read_csv(Path(args.merged))
    merged.sort(key=lambda r: r["frame_id"])
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if any(out.glob("batch_*.csv")):
        raise BatchError(f"{out} already holds batches")
    n = 0
    for i in range(0, len(merged), args.size):
        n += 1
        write_csv(out / f"batch_{n:03d}.csv", SCREEN_COLUMNS, merged[i : i + args.size])
    print(f"{len(merged)} records in {n} batches of up to {args.size}")
    return 0


def check_batch(inp: Path, outp: Path) -> list[str]:
    problems = []
    if not outp.exists():
        return [f"{outp.name}: missing"]
    _, src = read_csv(inp)
    cols, got = read_csv(outp)
    if cols != list(OUT_COLUMNS):
        problems.append(f"{outp.name}: header {cols}")
    if [r["frame_id"] for r in got] != [r["frame_id"] for r in src]:
        problems.append(f"{outp.name}: frame_ids differ from the input batch")
    for r in got:
        d, code, s = r.get("decision"), r.get("exclusion_code"), r.get("stratum")
        fid = r.get("frame_id")
        if d not in DECISIONS:
            problems.append(f"{outp.name}: {fid} decision {d!r}")
        elif d == "exclude" and (code not in TA_CODES or s):
            problems.append(f"{outp.name}: {fid} exclusion code {code!r}, stratum {s!r}")
        elif d != "exclude" and (code or s not in STRATA):
            problems.append(f"{outp.name}: {fid} code {code!r}, stratum {s!r}")
        for v in r.values():
            if v in ("None", "NA", "null", "nan"):
                problems.append(f"{outp.name}: {fid} holds {v!r}")
                break
    return problems


def cmd_join(args) -> int:
    inputs = sorted(Path(args.inputs).glob("batch_*.csv"))
    if not inputs:
        raise BatchError("no input batches")
    problems, rows = [], []
    for inp in inputs:
        outp = Path(args.outputs) / inp.name
        p = check_batch(inp, outp)
        problems += p
        if not p:
            rows += read_csv(outp)[1]
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise BatchError(f"{len(problems)} problems; nothing written")
    write_csv(Path(args.out), OUT_COLUMNS, rows)
    print(f"joined {len(inputs)} batches, {len(rows)} records into {args.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("split")
    s.add_argument("--merged", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--size", type=int, default=250)
    j = sub.add_parser("join")
    j.add_argument("--inputs", required=True)
    j.add_argument("--outputs", required=True)
    j.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        return {"split": cmd_split, "join": cmd_join}[args.cmd](args)
    except BatchError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
