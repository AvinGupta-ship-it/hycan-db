#!/usr/bin/env python3
"""
Staging-to-dataset append for HyCAN-DB (manual v2.0 §18 Phase A.3).

Collapses steps 11-14 of the §9.1 per-paper pipeline into one command that
refuses to proceed on any check failure:

    11  verify the staging file from disk (not from any tool's self-report, §3.8)
    12  validate the staging file standalone; zero errors required
    13  back up the dataset, append positionally, validate the merged file
        against the stored session baseline, diff warning types (§11.5)
    14  remove the staging file

Usage
-----
    # once, at the start of a session (§11.5, §9.1 "Session start")
    python3 scripts/append_paper.py --write-baseline /tmp/hycan_baseline.json

    # per paper
    python3 scripts/append_paper.py data/raw/staging_HYC-0007.csv \\
        --baseline /tmp/hycan_baseline.json

    --dataset PATH      target dataset (default data/raw/measurements_v0.1.csv)
    --baseline PATH     stored session baseline; omitted means derive one now
                        from the current dataset, which is weaker and is stated
                        in the output
    --backup-dir DIR    where the pre-append backup goes (default /tmp)
    --dry-run           run every check against a throwaway copy; the real
                        dataset and the staging file are not touched
    --keep-staging      leave the staging file in place after a successful append

Exit codes
----------
    0  every check passed; the append is on disk (or the dry run passed)
    1  a check failed; the dataset is unchanged or was rolled back
    2  a path argument is missing or unreadable

Why the append is raw text
--------------------------
The merge is a byte-level append of the staging file's body, equivalent to
``tail -n +2 staging >> dataset``. Reading the dataset into pandas and writing
it back would reformat cells it was never asked to change — float precision,
quoting, empty-vs-NaN — and rewrite the 119 rows that §6.7 forbids touching. A
raw append cannot do that. Its precondition is that the physical column order of
the staging file matches the dataset exactly, which is check 4 below.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime

import pandas as pd

from hycan.validate import validate_dataset

DEFAULT_DATASET = "data/raw/measurements_v0.1.csv"
DEFAULT_BACKUP_DIR = "/tmp"
TOOL_VERSION = "1.0"


class CheckFailed(Exception):
    """A pipeline check failed. The caller reports it and changes nothing."""


# ---------------------------------------------------------------------------
# Disk primitives — every fact about a file comes from reading the file
# ---------------------------------------------------------------------------

def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def physical_lines(path: str) -> int:
    """Physical lines in *path*, ignoring blank lines at the end of the file.

    Trailing blanks are discounted rather than absorbed into a tolerance on the
    caller's comparison. A tolerance wide enough to cover a trailing blank line
    is also wide enough to hide exactly one newline inside a quoted field, and
    that newline is what the comparison exists to catch: it breaks the 1:1
    mapping between lines and rows that the positional append relies on.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        lines = handle.readlines()
    while lines and not lines[-1].strip("\r\n").strip():
        lines.pop()
    return len(lines)


def read_csv(path: str) -> pd.DataFrame:
    """Load exactly as scripts/validate_data.py does (no keep_default_na).

    ``index_col=False`` is load-bearing rather than cosmetic. When every data
    row carries more fields than the header names, pandas' default is to treat
    the first field as an index. A malformed 39-field staging row then parses
    into a clean-looking 38-column frame that passes every preflight check and
    only fails at the byte level after the append has been written. Refusing
    the index surfaces the mismatch here, before anything is touched.

    The two pandas parse failures are converted to CheckFailed so that a
    malformed file is a refusal with an exit code, not a traceback.
    """
    try:
        return pd.read_csv(path, index_col=False)
    except pd.errors.EmptyDataError as exc:
        raise CheckFailed(f"{path} is empty or has no header row") from exc
    except pd.errors.ParserError as exc:
        raise CheckFailed(
            f"{path} is not well-formed CSV: {exc}. Every data row must carry "
            "exactly as many fields as the header has columns."
        ) from exc
    except UnicodeDecodeError as exc:
        raise CheckFailed(f"{path} is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        # IsADirectoryError, PermissionError and friends. A bad path argument
        # should be a refusal with an exit code, not a traceback.
        raise CheckFailed(f"cannot read {path}: {exc}") from exc


def field_counts(path: str) -> dict[int, list[int]]:
    """Distinct field counts across the file, mapped to the lines that have them.

    Uses a real CSV parser, so a comma inside a quoted field is not miscounted
    the way ``awk -F','`` or a naive split would miscount it (§6.7, §B.3).

    This is checked explicitly rather than left to pandas. pandas' behaviour on
    a row with more fields than the header has names is to absorb the surplus
    into an index or to drop data with a warning, either of which turns a
    malformed file into a clean-looking frame.
    """
    counts: dict[int, list[int]] = {}
    try:
        with open(path, "r", encoding="utf-8", newline="") as handle:
            for number, row in enumerate(csv.reader(handle), start=1):
                if not row or (len(row) == 1 and not row[0].strip()):
                    continue
                counts.setdefault(len(row), []).append(number)
    except csv.Error as exc:
        # csv.reader caps a single field at 128 KiB. A long notes cell would
        # otherwise take --write-baseline and every append offline with a bare
        # traceback, on a file every other tool in the repo reads happily.
        raise CheckFailed(f"cannot parse {path} as CSV: {exc}") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise CheckFailed(f"cannot read {path}: {exc}") from exc
    return counts


def describe_file(path: str, label: str) -> dict:
    """Read *path* from disk and report what is actually in it (§3.8)."""
    if not os.path.exists(path):
        raise CheckFailed(f"{label} does not exist: {path}")
    df = read_csv(path)

    # Every line, header included, must carry exactly as many fields as the
    # frame has columns. One comparison covers both failure shapes: rows of
    # differing width, and a file uniformly the wrong width.
    counts = field_counts(path)
    if set(counts) != {len(df.columns)}:
        detail = "; ".join(
            f"{n} field(s) on line(s) {lines[:5]}"
            + (" and more" if len(lines) > 5 else "")
            for n, lines in sorted(counts.items())
        ) or "no parsable rows"
        raise CheckFailed(
            f"{label} has rows of differing width: {detail}. The frame parsed "
            f"to {len(df.columns)} columns, so every line must carry "
            f"{len(df.columns)} fields. Fix the file before appending."
        )

    lines = physical_lines(path)
    if lines != len(df) + 1:
        cause = ("a blank line between data rows"
                 if lines > len(df) + 1 else "a malformed row")
        raise CheckFailed(
            f"{label}: {lines} significant lines but {len(df)} parsed rows "
            f"(expected {len(df) + 1} = header + one line per row). "
            f"The usual causes are {cause} and a newline inside a quoted "
            "field. The append is a byte-level operation, so a file whose "
            "lines do not map 1:1 onto its rows cannot be verified line by "
            "line afterwards. Fix the file before appending."
        )
    return {
        "path": path,
        "df": df,
        "rows": len(df),
        "lines": lines,
        "columns": list(df.columns),
        "sha256": sha256(path),
    }


# ---------------------------------------------------------------------------
# Baseline (§11.5)
# ---------------------------------------------------------------------------

def compute_state(df: pd.DataFrame) -> dict:
    report = validate_dataset(df)
    return {
        "rows": report.total,
        "error_counts": dict(report.error_counts),
        "warning_counts": dict(report.warning_counts),
    }


def write_baseline(dataset: str, out_path: str) -> int:
    info = describe_file(dataset, "dataset")
    state = compute_state(info["df"])
    baseline = {
        "tool": "append_paper.py",
        "tool_version": TOOL_VERSION,
        "created": datetime.now().isoformat(timespec="seconds"),
        "dataset": os.path.realpath(dataset),
        "sha256": info["sha256"],
        "prefix_sha256": prefix_sha256(dataset, info["rows"]),
        **state,
    }
    try:
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(baseline, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except OSError as exc:
        raise CheckFailed(f"cannot write the baseline to {out_path}: {exc}") from exc

    # §3.8: the baseline anchors the whole session, so it is read back from
    # disk rather than reported from the dict that was just serialized.
    stored = load_baseline(out_path)
    if (stored["rows"] != state["rows"]
        or stored["warning_counts"] != state["warning_counts"]):
        raise CheckFailed(
            f"the baseline written to {out_path} does not read back as what was "
            "computed. Do not start a session on it."
        )

    print(f"Baseline written and read back: {out_path}")
    print(f"  dataset:  {stored['dataset']}")
    print(f"  sha256:   {stored['sha256'][:16]}...")
    print(f"  rows:     {stored['rows']}")
    print(f"  errors:   {sum(stored['error_counts'].values())}")
    print("  warning types:")
    for name, count in sorted(stored["warning_counts"].items()):
        print(f"    {name}: {count}")

    if sum(stored["error_counts"].values()):
        # Remove it. A refused baseline left on disk is a usable baseline, and
        # the next command that passes --baseline would anchor the session to
        # the broken dataset this call just rejected.
        try:
            os.remove(out_path)
            removed = f"{out_path} removed."
        except OSError as exc:
            removed = f"Could not remove {out_path}: {exc}. Delete it by hand."
        print("\nREFUSED: the baseline dataset has validation errors. A session "
              "anchored to a broken dataset cannot tell which errors it caused. "
              f"Fix the dataset, then take the baseline again. {removed}")
        return 1
    return 0


def prefix_sha256(path: str, data_lines: int) -> str:
    """Hash of the header plus the first *data_lines* data lines.

    This is what binds a baseline to the dataset it was taken from. Comparing
    paths alone binds nothing: the file at a path can be swapped, and comparing
    whole-file hashes cannot work either, because the dataset legitimately
    grows during a session. Hashing the prefix that must not change detects a
    substitution while still permitting appends.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for number, line in enumerate(handle):
            if number > data_lines:
                break
            digest.update(line)
    return digest.hexdigest()


def load_baseline(path: str) -> dict:
    if not os.path.exists(path):
        raise CheckFailed(
            f"baseline not found: {path}\n"
            "Take one first:  python3 scripts/append_paper.py "
            "--write-baseline " + path
        )
    try:
        with open(path, "r", encoding="utf-8") as handle:
            baseline = json.load(handle)
    except json.JSONDecodeError as exc:
        raise CheckFailed(f"baseline {path} is not valid JSON: {exc}") from exc
    if not isinstance(baseline, dict):
        raise CheckFailed(f"baseline {path} is not a JSON object")
    for key in ("rows", "error_counts", "warning_counts"):
        if key not in baseline:
            raise CheckFailed(f"baseline {path} is missing '{key}'")
    return baseline


def check_baseline_belongs_to(baseline: dict, path: str, dataset_path: str) -> None:
    """Refuse a baseline taken from a different dataset.

    Without this, any baseline file is accepted for any dataset, and a baseline
    that happens to carry an extra warning type silently disables the §11.5
    new-warning-type stop condition — the one hard gate on the append.
    """
    recorded = baseline.get("dataset")
    if not recorded:
        raise CheckFailed(
            f"baseline {path} does not record which dataset it was taken from, "
            "so it cannot be matched to this one. Take a fresh baseline."
        )
    if os.path.realpath(recorded) != os.path.realpath(dataset_path) and (
        not os.path.exists(recorded)
        or not os.path.samefile(recorded, dataset_path)
    ):
        raise CheckFailed(
            f"baseline {path} was taken from {recorded}, but this run targets "
            f"{os.path.realpath(dataset_path)}. A baseline from another file "
            "cannot police this one's warning types (§11.5). Take a baseline "
            "for the dataset you are appending to."
        )

    # The path can be made to point at a different file between the baseline
    # and the append. Bind by content: the rows the baseline described must
    # still be the rows at the head of this dataset. Appends are permitted,
    # substitutions are not.
    recorded_prefix = baseline.get("prefix_sha256")
    if not recorded_prefix:
        raise CheckFailed(
            f"baseline {path} predates content binding (no prefix_sha256) and "
            "cannot be verified against this dataset. Take a fresh baseline."
        )
    try:
        actual_prefix = prefix_sha256(dataset_path, int(baseline["rows"]))
    except (OSError, ValueError, TypeError) as exc:
        raise CheckFailed(f"cannot fingerprint {dataset_path}: {exc}") from exc
    if actual_prefix != recorded_prefix:
        raise CheckFailed(
            f"the first {baseline['rows']} row(s) of {dataset_path} are not the "
            "rows this baseline was taken from. The file has been replaced, "
            "reordered, or edited in place since then, so its warning types "
            "cannot be trusted as a baseline (§11.5). Take a fresh one."
        )


# ---------------------------------------------------------------------------
# Preflight checks — nothing is written while these run
# ---------------------------------------------------------------------------

def preflight(staging_path: str, dataset_path: str, baseline_path: str | None) -> dict:
    print("Preflight")

    # 1-3. Both files read from disk; line counts consistent with parsed rows.
    dataset = describe_file(dataset_path, "dataset")
    staging = describe_file(staging_path, "staging file")
    print(f"  1. dataset read from disk: {dataset['rows']} rows, "
          f"{dataset['lines']} lines, sha {dataset['sha256'][:12]}")
    print(f"  2. staging read from disk: {staging['rows']} rows, "
          f"{staging['lines']} lines, sha {staging['sha256'][:12]}")

    # 4. Physical column order must match exactly (§6.7).
    if staging["columns"] != dataset["columns"]:
        extra = [c for c in staging["columns"] if c not in dataset["columns"]]
        absent = [c for c in dataset["columns"] if c not in staging["columns"]]
        detail = []
        if extra:
            detail.append(f"in staging only: {extra}")
        if absent:
            detail.append(f"in dataset only: {absent}")
        if not detail:
            first = next(
                i for i, (a, b) in enumerate(
                    zip(staging["columns"], dataset["columns"])
                ) if a != b
            )
            detail.append(
                f"same columns, different order; first difference at position "
                f"{first + 1}: staging has '{staging['columns'][first]}', "
                f"dataset has '{dataset['columns'][first]}'"
            )
        raise CheckFailed(
            "staging columns do not match the dataset (§6.7). " + "; ".join(detail)
        )
    print("  3. column order matches dataset exactly "
          f"({len(dataset['columns'])} columns)")

    # 5. Non-empty.
    if staging["rows"] < 1:
        raise CheckFailed("staging file has no data rows")

    # 6-7. measurement_id present, unique in staging, and not already in the dataset.
    staging_ids = staging["df"]["measurement_id"]
    if staging_ids.isna().any():
        blanks = [i + 2 for i, v in enumerate(staging_ids.isna()) if v]
        raise CheckFailed(f"staging rows missing measurement_id at csv lines {blanks}")
    staging_ids = staging_ids.astype(str).str.strip()
    duplicated = sorted(staging_ids[staging_ids.duplicated()].unique())
    if duplicated:
        raise CheckFailed(f"measurement_id repeated within staging: {duplicated}")
    existing = set(dataset["df"]["measurement_id"].dropna().astype(str).str.strip())
    collisions = sorted(set(staging_ids) & existing)
    if collisions:
        raise CheckFailed(
            f"measurement_id already present in the dataset: {collisions}"
        )
    print(f"  4. {len(staging_ids)} measurement_ids, unique and new")

    papers = sorted(staging["df"]["paper_id"].dropna().astype(str).str.strip().unique())
    if not papers or any(not p for p in papers):
        raise CheckFailed(
            "staging rows have a missing or blank paper_id. A whitespace-only "
            "paper_id satisfies the schema's 'required text' rule and is still "
            "unusable, so it is rejected here."
        )
    print(f"  5. paper_id(s): {', '.join(papers)}")

    # 8. Staging validates standalone with zero errors (§9.1 step 12).
    staging_state = compute_state(staging["df"])
    staging_errors = sum(staging_state["error_counts"].values())
    if staging_errors:
        detail = "; ".join(
            f"{k}: {v}" for k, v in sorted(staging_state["error_counts"].items())
        )
        raise CheckFailed(
            f"staging file has {staging_errors} validation errors ({detail}). "
            "Run scripts/validate_row_detail.py on it for the failing fields."
        )
    print(f"  6. staging validates standalone: 0 errors, "
          f"{sum(staging_state['warning_counts'].values())} warnings")
    for name, count in sorted(staging_state["warning_counts"].items()):
        print(f"       {name}: {count}")

    # 9. The dataset itself must be clean before anything is appended to it.
    dataset_state = compute_state(dataset["df"])
    dataset_errors = sum(dataset_state["error_counts"].values())
    if dataset_errors:
        raise CheckFailed(
            f"the dataset already has {dataset_errors} errors before this append. "
            "Fix the dataset first."
        )
    print(f"  7. dataset validates: 0 errors, "
          f"{sum(dataset_state['warning_counts'].values())} warnings")

    # 10. Baseline: stored, or derived with the weakening stated out loud.
    if baseline_path:
        baseline = load_baseline(baseline_path)
        check_baseline_belongs_to(baseline, baseline_path, dataset_path)
        source = f"stored baseline {baseline_path}"
        if baseline.get("sha256") and baseline["sha256"] != dataset["sha256"]:
            # Row loss cannot reach here: check_baseline_belongs_to hashes the
            # baseline's whole row prefix, so a shortened dataset is refused
            # there with a more specific message.
            grown = dataset_state["rows"] - baseline["rows"]
            print(f"  8. dataset has changed since the baseline was taken: "
                  f"{baseline['rows']} -> {dataset_state['rows']} rows "
                  f"(+{grown}; expected if you have already appended today)")
        else:
            print("  8. dataset matches the baseline exactly "
                  f"({baseline['rows']} rows, sha verified)")
        novel = set(dataset_state["warning_counts"]) - set(baseline["warning_counts"])
        if novel:
            raise CheckFailed(
                f"the dataset already carries warning type(s) absent from the "
                f"baseline: {sorted(novel)}. Something changed earlier in this "
                "session. Investigate before appending (§11.5)."
            )
    else:
        baseline = {
            "rows": dataset_state["rows"],
            "error_counts": dataset_state["error_counts"],
            "warning_counts": dataset_state["warning_counts"],
            "derived": True,
        }
        source = "derived from the current dataset (no --baseline given)"
        print("  8. NO STORED BASELINE. Deriving one from the dataset as it is now.")
        print("     This cannot catch a warning type introduced earlier in this")
        print("     session. Prefer --write-baseline at session start (§11.5).")

    print(f"  baseline source: {source}")
    print("Preflight passed.\n")

    return {
        "dataset": dataset,
        "staging": staging,
        "baseline": baseline,
        "dataset_state": dataset_state,
        "staging_state": staging_state,
        "papers": papers,
    }


# ---------------------------------------------------------------------------
# The append itself
# ---------------------------------------------------------------------------

def staging_body(path: str) -> str:
    """The staging file's data lines: everything after the header line.

    Blank lines are stripped from the end and refused in the middle. A blank
    line written into the dataset is invisible to every validator in the
    repository, because pandas skips it, and it permanently breaks the
    line-count check that every later append depends on — with a diagnosis
    that blames a quoted newline which is not there.

    Splitting on "\\n" rather than str.splitlines keeps CRLF bytes intact and
    avoids splitting on the exotic line boundaries splitlines() honours.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    _, separator, body = text.partition("\n")
    if not separator:
        raise CheckFailed("staging file has no newline after its header")

    lines = body.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise CheckFailed("staging file has a header but no data rows")
    blanks = [i + 2 for i, line in enumerate(lines) if not line.strip()]
    if blanks:
        raise CheckFailed(
            f"staging file has blank line(s) between data rows at csv lines "
            f"{blanks}. A blank line inside the dataset is invisible to the "
            "validators and breaks every later append's line-count check. "
            "Remove it before appending."
        )
    return "\n".join(lines) + "\n"


def append_body(target: str, body: str) -> None:
    """Append *body* to *target*, guaranteeing exactly one newline at the seam."""
    with open(target, "rb") as handle:
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        if size:
            handle.seek(-1, os.SEEK_END)
            needs_newline = handle.read(1) != b"\n"
        else:
            needs_newline = False
    with open(target, "a", encoding="utf-8", newline="") as handle:
        if needs_newline:
            handle.write("\n")
        handle.write(body)


def verify_merged(target: str, context: dict) -> tuple[dict, dict]:
    """Post-append verification, every fact re-read from disk.

    Returns (merged_info, merged_state) so the caller can report measured
    numbers rather than restating what it intended to write.
    """
    dataset = context["dataset"]
    staging = context["staging"]
    baseline = context["baseline"]

    expected_rows = dataset["rows"] + staging["rows"]

    merged = describe_file(target, "merged dataset")
    if merged["rows"] != expected_rows:
        raise CheckFailed(
            f"merged row count is {merged['rows']}, expected "
            f"{dataset['rows']} + {staging['rows']} = {expected_rows}"
        )
    if merged["columns"] != dataset["columns"]:
        raise CheckFailed("merged column list changed during the append")

    merged_state = compute_state(merged["df"])
    merged_errors = sum(merged_state["error_counts"].values())
    if merged_errors:
        detail = "; ".join(
            f"{k}: {v}" for k, v in sorted(merged_state["error_counts"].items())
        )
        raise CheckFailed(f"merged dataset has {merged_errors} errors ({detail})")

    novel = set(merged_state["warning_counts"]) - set(baseline["warning_counts"])
    # §11.5 makes a new warning type a stop condition -- it stops, the operator
    # assesses, and if the warning is doing its job the type is admitted
    # deliberately. Before this there was no way to admit one, which made a
    # CORRECT new warning unappendable: HYC-0011's 8.0 wt% raw-CNT claim is
    # precisely what "Pre-2005 raw-CNT high uptake (Tier D)" was written to
    # flag, and that row belongs in the corpus at Tier D under the
    # disclosure-not-deletion principle of docs/reproducibility_tiering.md.
    # The override takes the exact type string so it cannot be passed by
    # reflex, tolerates only the types named, and refuses a type that does not
    # actually appear so it cannot be left behind as a standing exemption.
    expected = set(context.get("expect_new_warnings") or ())
    unexpected = novel - expected
    if unexpected:
        raise CheckFailed(
            f"new warning type(s) introduced by this append: "
            f"{sorted(unexpected)}. §11.5 makes a new warning type a stop "
            f"condition. If one is legitimate, name it with "
            f"--expect-new-warning and record why in the row notes."
        )
    stale = expected - novel
    if stale:
        raise CheckFailed(
            f"--expect-new-warning named {sorted(stale)}, which this append "
            f"does not introduce. Remove it rather than leaving a standing "
            f"exemption in place."
        )
    if novel:
        print(f"Admitted new warning type(s) by explicit request: "
              f"{sorted(novel)}")

    merged_ids = set(merged["df"]["measurement_id"].dropna().astype(str).str.strip())
    staged_ids = set(staging["df"]["measurement_id"].astype(str).str.strip())
    absent = sorted(staged_ids - merged_ids)
    if absent:
        raise CheckFailed(f"appended rows not found in the merged file: {absent}")

    return merged, merged_state


def warning_delta(before: dict, after: dict) -> list[str]:
    """Render a warning-type diff.

    *before* is always the session baseline, never the mid-session dataset
    state: §11.5 defines "new warning type" against the baseline, and rendering
    the diff against a different reference set than the gate uses is how a
    summary line ends up contradicting the table printed under it.
    """
    lines = []
    for name in sorted(set(before) | set(after)):
        old = before.get(name, 0)
        new = after.get(name, 0)
        mark = "" if name in before else "   <-- NEW TYPE"
        lines.append(f"    {name}: {old} -> {new}{mark}")
    return lines


def unique_backup_path(backup_dir: str, dataset: str) -> str:
    """A backup path that cannot collide with an existing one.

    Two appends within the same second would otherwise produce the same name
    and shutil.copy2 would overwrite the earlier pre-append state.
    """
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    stem, extension = os.path.splitext(os.path.basename(dataset))
    candidate = os.path.join(backup_dir, f"{stem}.{stamp}.bak{extension}")
    suffix = 1
    while os.path.exists(candidate):
        candidate = os.path.join(
            backup_dir, f"{stem}.{stamp}-{suffix}.bak{extension}"
        )
        suffix += 1
    return candidate


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_append(args) -> int:
    context = preflight(args.staging, args.dataset, args.baseline)
    context["expect_new_warnings"] = tuple(args.expect_new_warning)
    dataset = context["dataset"]
    staging = context["staging"]
    baseline = context["baseline"]

    # The bytes about to be appended must be the bytes that were validated.
    # preflight read and validated the staging file; re-hash it immediately
    # before its body is read, so that anything rewriting it in between is
    # refused rather than silently entering the dataset unvalidated.
    if sha256(args.staging) != staging["sha256"]:
        raise CheckFailed(
            f"{args.staging} changed on disk between validation and append. "
            "Nothing was written. Re-run so the new contents are validated."
        )
    body = staging_body(args.staging)

    if args.dry_run:
        print("Dry run — the real dataset is not touched")
        with tempfile.TemporaryDirectory() as tmpdir:
            trial = os.path.join(tmpdir, os.path.basename(args.dataset))
            shutil.copy2(args.dataset, trial)
            append_body(trial, body)
            merged, merged_state = verify_merged(trial, context)
        print(f"  merge simulated: {dataset['rows']} + {staging['rows']} = "
              f"{merged['rows']} rows, "
              f"{sum(merged_state['error_counts'].values())} errors")
        print("  warning types (vs baseline):")
        for line in warning_delta(
            baseline["warning_counts"], merged_state["warning_counts"]
        ):
            print(line)

        # §3.8: re-read rather than repeating the hash preflight computed.
        after = sha256(args.dataset)
        if after != dataset["sha256"]:
            raise CheckFailed(
                f"{args.dataset} changed during the dry run. Investigate."
            )
        print(f"\n  unchanged on disk, re-hashed: {args.dataset} (sha {after[:12]})")
        print(f"  unchanged on disk: {args.staging} (sha {sha256(args.staging)[:12]})")
        print("\nDry run passed. Re-run without --dry-run to apply.")
        return 0

    # --- Backup, verified by hash (§3.8) ---
    try:
        os.makedirs(args.backup_dir, exist_ok=True)
    except OSError as exc:
        raise CheckFailed(f"cannot create the backup directory: {exc}") from exc
    backup = unique_backup_path(args.backup_dir, args.dataset)
    try:
        shutil.copy2(args.dataset, backup)
    except OSError as exc:
        raise CheckFailed(f"cannot write the backup to {backup}: {exc}") from exc
    if sha256(backup) != dataset["sha256"]:
        raise CheckFailed(f"backup {backup} does not match the dataset; aborting")
    print(f"Backup  {backup}  (sha {dataset['sha256'][:12]}, verified)")

    # --- Append and verify, rolling back on ANY failure ---
    #
    # The write is inside the guarded block, not before it. A partial write —
    # ENOSPC, a quota, a disconnected volume — leaves the dataset matching
    # neither its before state nor its after state, and that is the one
    # outcome with no safe recovery path. It must roll back like any other
    # failure.
    #
    # The catch is Exception, not CheckFailed. verify_merged reaches pandas,
    # which raises ParserError and EmptyDataError; an uncaught one of those
    # would leave the dataset appended-but-unverified.
    try:
        append_body(args.dataset, body)
        print(f"Append  {staging['rows']} rows appended positionally")
        merged, merged_state = verify_merged(args.dataset, context)
    except Exception as exc:
        try:
            shutil.copy2(backup, args.dataset)
            restored = sha256(args.dataset)
        except Exception as restore_exc:
            raise CheckFailed(
                f"{exc}\n  ROLLBACK ITSELF FAILED: {restore_exc}. The verified "
                f"pre-append copy is {backup}. Restore it by hand before doing "
                "anything else."
            ) from exc
        if restored == dataset["sha256"]:
            rollback = (f"rolled back from {backup}; dataset restored and "
                        "verified byte-identical to its pre-append state")
        else:
            rollback = (
                f"ROLLBACK VERIFICATION FAILED. {args.dataset} does not match "
                f"the pre-append hash. The good copy is {backup}. Restore it "
                "by hand before doing anything else."
            )
        label = "" if isinstance(exc, CheckFailed) else f"{type(exc).__name__}: "
        raise CheckFailed(f"{label}{exc}\n  {rollback}") from exc

    # Every number below is measured from the merged file, not restated from
    # what this run intended to write.
    novel = sorted(
        set(merged_state["warning_counts"]) - set(baseline["warning_counts"])
    )
    print(f"Verify  merged file re-read from disk: {merged['rows']} rows, "
          f"{sum(merged_state['error_counts'].values())} errors, "
          f"{len(novel)} new warning types")
    print("  warning types (vs baseline):")
    for line in warning_delta(
        baseline["warning_counts"], merged_state["warning_counts"]
    ):
        print(line)

    # --- Summary before staging removal ---
    #
    # The append has succeeded and been verified by this point. Nothing after
    # this line may turn that into a reported failure, so the §17 material is
    # printed first and staging removal is reported as its own outcome.
    print()
    print("SUMMARY (for the §17 execution log)")
    print(f"  paper(s):       {', '.join(context['papers'])}")
    print(f"  rows before:    {dataset['rows']}")
    print(f"  rows appended:  {staging['rows']}")
    print(f"  rows after:     {merged['rows']}")
    print(f"  errors after:   {sum(merged_state['error_counts'].values())}")
    print(f"  new warn types: {novel if novel else 'none'}")
    print(f"  backup:         {backup}")
    print(f"  dataset sha256: {merged['sha256']}")

    # --- Remove staging (§9.1 step 14) ---
    if args.keep_staging:
        print(f"\nStaging kept: {args.staging}")
    else:
        try:
            os.remove(args.staging)
        except OSError as exc:
            print(f"\nWARNING: the append succeeded and is verified, but the "
                  f"staging file could not be removed: {exc}\n"
                  f"  Delete {args.staging} by hand (§9.1 step 14). Do not "
                  "re-run this command; the rows are already in the dataset.")
            return 0
        if os.path.exists(args.staging):
            print(f"\nWARNING: the append succeeded and is verified, but "
                  f"{args.staging} is still present after removal. Delete it "
                  "by hand. Do not re-run this command.")
            return 0
        print(f"\nStaging removed: {args.staging}")

    print("\nNot done by this script: §9.1 steps 15-18 (paper_tracking.csv, "
          "commit and push, execution log, manual §6).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify, back up, append, and re-verify a staging "
                    "file (§9.1 steps 11-14)."
    )
    parser.add_argument("staging", nargs="?")
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--baseline")
    parser.add_argument("--write-baseline", dest="write_baseline")
    parser.add_argument("--backup-dir", default=DEFAULT_BACKUP_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-staging", action="store_true")
    parser.add_argument(
        "--expect-new-warning", action="append", default=[], metavar="TYPE",
        help=("admit one specific new warning type that §11.5 would otherwise "
              "stop on; give the exact type string, repeatable. Refused if the "
              "named type does not actually appear, so it cannot be left in "
              "place as a standing exemption."),
    )
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])

    try:
        if args.write_baseline:
            if not os.path.exists(args.dataset):
                print(f"Error: dataset not found: {args.dataset}")
                return 2
            return write_baseline(args.dataset, args.write_baseline)
        if not args.staging:
            print("Error: give a staging file, or --write-baseline PATH.")
            return 2
        # Exit 2 is documented as "a path argument is missing or unreadable",
        # so missing paths are separated here from the substantive refusals
        # that exit 1.
        for label, path in (("staging file", args.staging),
                            ("dataset", args.dataset)):
            if not os.path.exists(path):
                print(f"Error: {label} not found: {path}")
                return 2
        return run_append(args)
    except CheckFailed as exc:
        print(f"\nREFUSED: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
