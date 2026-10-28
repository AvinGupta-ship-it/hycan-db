"""Assemble the v1.0 agent prompts and their SHA-256 values (protocol §9).

Each role template in prompts/v1/roles/ is filled with:
  - {{PROTOCOL_EXCERPT}}: protocol §§3, 4, 6, the strata of §7, and §9 for
    screening and eligibility; those plus §10.1 and §11.0 for extraction,
    reconciliation and labelling (§9 sets the minimum), copied from the
    registered docs/v1_protocol.md;
  - {{SCHEMA_V2}}: the redacted copies of src/hycan/schema.py and
    docs/data_dictionary.md in prompts/v1/schema_v2_redacted/ (Amendment 1),
    which must equal what scripts/v1_redact_schema.py builds from the
    registration commit;
  - {{COLUMNS}}: the dataset's column order;
  - {{MATCH_RULES}}: the matching rule, written from the constants of
    scripts/v1_extract.py so that the reconciler's description of match.csv
    cannot drift from the code;
  - the role's own variables (below).

The protocol excerpt is read from the registration commit, so an amendment
appended to §15 cannot change a prompt silently, and the script refuses if the
working copies of those sections differ from the registered ones.

Writes prompts/v1/built/<role>.md, a copy of prompts/v1/launcher.md, and
prompts/v1/built/SHA256SUMS (the built prompts, the launcher and the two
redacted schema files). The SHA-256 values are what the freezing amendment
records.

    python3 scripts/v1_prompts.py            build and print the hashes
    python3 scripts/v1_prompts.py --check    rebuild in memory, compare to disk
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = ROOT / "prompts" / "v1" / "roles"
BUILT = ROOT / "prompts" / "v1" / "built"
LAUNCHER = ROOT / "prompts" / "v1" / "launcher.md"
REDACTED = ROOT / "prompts" / "v1" / "schema_v2_redacted"
REGISTRATION_COMMIT = "0190009f414488812c84d7f3bee8753cdc54f6a4"

COLUMNS_FROM = "data/raw/measurements_v0.1.csv"

INPUTS_A = """A directory, given to you by path, holding:
- `paper.json`;
- `text/`: the PDF text layer of the main article and of each supplementary
  file, one `.txt` file per PDF (from `pdftotext -layout`);
- `pages/`: one PNG image per page, named `<file>-<page>.png`.

Read the text first, and use the page images for tables, figures, captions,
symbols and anything the text layer garbles."""

INPUTS_B = """A directory, given to you by path, holding:
- `paper.json`;
- `pages/`: one PNG image per page of the main article and of each
  supplementary file, named `<file>-<page>.png`.

There is no text layer. Read everything from the page images."""

INTRO_DUAL = """Two extractors, A and B, extracted one paper independently, with different
models and different inputs (A: text layer and page images; B: page images
only). You reconcile their rows against the paper. Neither extractor saw the
other's rows. The first row set is A's, the second B's."""

INTRO_LEGACY = """This paper was extracted for HyCAN-DB v0.1. Extractor B has extracted it
again, from page images only and blind to those rows. You reconcile B's
extraction with the v0.1 rows, against the paper. The first row set is the
v0.1 rows, the second B's. Neither is preferred: decide every difference from
the paper."""

LEGACY_INPUTS = """- `labels.csv`: the label of each v0.1 sample as printed in the paper,
  made by a separate agent from the paper and the v0.1 rows (columns
  `sample_id`, `measurement_ids`, `label`, `evidence`; a line with
  `measurement_ids` applies to those rows only);
"""

LEGACY_RULES = """
### v0.1 papers

These rules take precedence over the identity rules above.

- A kept v0.1 row keeps its v0.1 `measurement_id` and `sample_id`. Its
  `material_description` becomes `<label> | <v0.1 material_description>`, with
  the label from `labels.csv`. New rows and samples are numbered after the
  v0.1 rows' highest numbers. Isotherm IDs are B's; a new isotherm is numbered
  after B's highest.
- The v0.1 rows have no schema v2 coding, and `match.csv` does not compare a
  v2 field that is empty on the v0.1 side. For those fields, `isotherm_id`
  included, B's coding is the only one: check it against the paper, at least
  once per sample for the fields that are the same on every row of a sample
  (basis, wt% convention, instrument, calibration, replicates, laboratory,
  degassing, sample mass, H₂ purity, probe gas, `area_same_sample`, BET range),
  and keep it unless the paper contradicts it (then log `new`).
- A kept v0.1 row that B did not extract gets its v2 fields from the paper by
  the extraction rules, usually as B coded that sample's other rows; log one
  line with `field` = `v2_fields` and `decision` = `new`.
- A v0.1 row with no H₂ uptake value is outside the §9 scope: drop it (`row`,
  `second`) and carry its characterization onto that sample's uptake rows
  where they lack it.
- A figure point B digitized takes B's value and pressure, with 1% of the axis
  span, from `digitized_means.csv`. A `figure_digitized` point only in the
  v0.1 rows is kept if it is in the figure, with its v0.1 value and
  `digitization_uncertainty_wt_pct` = 1% of the span between the lowest and
  highest labelled ticks of that figure's uptake axis, in wt%.
"""

LEGACY_OUTPUT = """  - `field` = `v2_fields`: the v2 coding of a kept v0.1 row that B did not
    extract (see above).
"""

ROLE_SPECS = {
    "screen": ("screen.md", "base", {}),
    "stratum_tiebreak": ("stratum_tiebreak.md", "base", {}),
    "eligibility": ("eligibility.md", "base", {}),
    "eligibility_resolve": ("eligibility_resolve.md", "base", {}),
    "extract_A": ("extract.md", "full", {"AGENT": "A", "INPUTS": INPUTS_A}),
    "extract_B": ("extract.md", "full", {"AGENT": "B", "INPUTS": INPUTS_B}),
    "reconcile": (
        "reconcile.md",
        "full",
        {
            "MODE_INTRO": INTRO_DUAL,
            "MODE_SOURCES": "the rows of extractor A and of extractor B",
            "MODE_INPUTS": "",
            "FIGURE_RULE": "A point both extractors digitized in the same unit gets "
            "the mean of the two values and of the two pressures, with uncertainty "
            "the larger of half the difference and 1% of the axis span, the larger "
            "of the two extractors' spans (§9). A point "
            "only one extractor digitized gets that value, with 1% of its axis span "
            "(Amendment 1). The axis span is the distance between the two "
            "calibration ticks of the uptake axis, its lowest and highest labelled "
            "ticks.",
            "MODE_RULES": "",
            "MODE_OUTPUT": "",
            "MATCH_LEGACY": "",
        },
    ),
    "reconcile_legacy": (
        "reconcile.md",
        "full",
        {
            "MODE_INTRO": INTRO_LEGACY,
            "MODE_SOURCES": "the v0.1 rows and extractor B's rows",
            "MODE_INPUTS": LEGACY_INPUTS,
            "FIGURE_RULE": "Every point B digitized gets B's value and pressure, with "
            "uncertainty 1% of the axis span (§9, v0.1 papers). The axis span is "
            "the distance between the two calibration ticks of the uptake axis, "
            "its lowest and highest labelled ticks.",
            "MODE_RULES": LEGACY_RULES,
            "MODE_OUTPUT": LEGACY_OUTPUT,
            "MATCH_LEGACY": "legacy",
        },
    ),
    "legacy_labels": ("legacy_labels.md", "full", {}),
}


class PromptError(RuntimeError):
    pass


def git_show(path: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{REGISTRATION_COMMIT}:{path}"],
        check=True,
        capture_output=True,
    )
    return out.stdout.decode("utf-8")


def section(text: str, heading: str) -> str:
    """The text of one '## ' section, from its heading to the next '## '."""
    m = re.search(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", text, re.DOTALL | re.MULTILINE)
    if not m:
        raise PromptError(f"section not found: {heading}")
    return m.group(0).rstrip() + "\n"


def strata(text: str) -> str:
    sec = section(text, "7. Sampling")
    m = re.search(r"^- \*\*Strata\.\*\*\n(?:  .*\n)+", sec, re.MULTILINE)
    if not m:
        raise PromptError("§7 strata not found")
    return "## 7. Sampling (strata only)\n\n" + m.group(0)


def subsection(text: str, heading: str) -> str:
    """The text of one '### ' subsection, to the next '### ' or '## '."""
    m = re.search(
        rf"^### {re.escape(heading)}\n.*?(?=^### |^## |\Z)", text, re.DOTALL | re.MULTILINE
    )
    if not m:
        raise PromptError(f"subsection not found: {heading}")
    return m.group(0).rstrip() + "\n"


def protocol_excerpt(text: str, kind: str) -> str:
    parts = [
        section(text, "3. Definitions"),
        section(text, "4. Eligibility (paper level)"),
        section(text, "6. Screening"),
        strata(text),
        section(text, "9. Data extraction and verification"),
    ]
    if kind == "full":
        parts += [
            "## 10. Quality coding (§10.1 only)\n\n"
            + subsection(text, "10.1 Reporting-completeness score"),
            "## 11. Analysis plan (§11.0 only)\n\n"
            + subsection(text, "11.0 General rules"),
        ]
    return "\n".join(parts)


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def schema_v2() -> tuple[str, dict[str, str]]:
    """The redacted schema text, after checking the committed copies equal a
    fresh build from the registration commit."""
    built = _load("v1_redact_schema").build()
    on_disk = {
        name: (REDACTED / name).read_text(encoding="utf-8") for name in built
    }
    if on_disk != built:
        raise PromptError(
            "prompts/v1/schema_v2_redacted differs from scripts/v1_redact_schema.py"
        )
    text = (
        "### src/hycan/schema.py (comments and docstrings removed)\n\n```python\n"
        + built["schema.py"]
        + "```\n\n### docs/data_dictionary.md (paper-specific examples removed)\n\n"
        + built["data_dictionary.md"]
    )
    return text, built


def _code_list(names, keep_order: bool = False) -> str:
    return ", ".join(f"`{n}`" for n in (names if keep_order else sorted(names)))


def match_rules(legacy: bool) -> str:
    ve = _load("v1_extract")
    label = (
        "the text of `material_description` before the first ` | `, or, for a "
        "v0.1 row, its label in `labels.csv`"
        if legacy
        else "the text of `material_description` before the first ` | `"
    )
    text = (
        "`match.csv` has the columns "
        + _code_list(ve.MATCH_COLUMNS, keep_order=True)
        + ". Code pairs a row of the first set with a row of the second when they "
        f"have the same sample label ({label}; compared on letters and digits "
        f"only, ignoring case), temperatures within {ve.T_TOL_K:g} K, pressures "
        f"within the larger of {ve.P_TOL_REL:.0%} and {ve.P_TOL_ABS_BAR:g} bar (or "
        "both empty), and the same quantity reported (gravimetric uptake, "
        "volumetric capacity, adsorbed-phase density, areal uptake, or "
        "characterization only). Among candidates it prefers a pair on the same "
        "isotherm branch, then the closest pressure, then the closest "
        "temperature, and pairs each row at most once. `status` is `differ` (one "
        "line for each field that differs within a matched pair, with both "
        "values), `only_first` or `only_second` (one line for each unmatched "
        "row), or `agree` (one line for a matched pair that agrees on every "
        "compared field).\n\n"
        "Every column is compared except "
        + _code_list(ve.NOT_COMPARED)
        + ". "
        + _code_list(ve.PRESENCE_ONLY)
        + " are compared only on whether they are filled; `doi` ignoring case; "
        "booleans ignoring case; numbers as numbers; and an empty cell of a "
        "field with a schema default is read as that default. A pressure or "
        "uptake value read from a figure ("
        + _code_list(ve.DIGITIZED_NUMERIC)
        + " on a `figure_digitized` row, and the pressure of a row whose `notes` "
        f"say `{ve.PRESSURE_DIGITIZED}`) agrees with the other set's value within "
        f"{ve.FIGURE_REL_TOL:.0%} relative."
    )
    if legacy:
        text += (
            " A v0.1 row with no pressure also pairs with a row whose pressure was "
            "read from a figure (a `figure_digitized` row, or `notes` saying "
            f"`{ve.PRESSURE_DIGITIZED}`); the pressure then appears as a "
            "difference. A schema v2 field that is empty on the v0.1 row is not "
            "compared."
        )
    return text


def build() -> tuple[dict[str, str], dict[str, str]]:
    registered = git_show("docs/v1_protocol.md")
    working = (ROOT / "docs" / "v1_protocol.md").read_text(encoding="utf-8")
    excerpts = {}
    for kind in ("base", "full"):
        excerpts[kind] = protocol_excerpt(registered, kind)
        if protocol_excerpt(working, kind) != excerpts[kind]:
            raise PromptError(
                "docs/v1_protocol.md §§3, 4, 6, 7, 9, 10.1 or 11.0 differ from "
                "the registration"
            )
    schema_text, redacted = schema_v2()
    columns = (ROOT / COLUMNS_FROM).read_text(encoding="utf-8").splitlines()[0]
    built = {}
    for role, (template, kind, own) in ROLE_SPECS.items():
        common = {
            "PROTOCOL_EXCERPT": excerpts[kind],
            "SCHEMA_V2": schema_text,
            "COLUMNS": "```\n" + columns + "\n```",
            "MATCH_RULES": match_rules(own.get("MATCH_LEGACY") == "legacy"),
        }
        text = (ROLES / template).read_text(encoding="utf-8")
        for key, value in {**own, **common}.items():
            text = text.replace("{{" + key + "}}", value)
        left = re.findall(r"\{\{[A-Z_0-9]+\}\}", text)
        if left:
            raise PromptError(f"{role}: unfilled {sorted(set(left))}")
        built[f"{role}.md"] = text
    built["launcher.md"] = LAUNCHER.read_text(encoding="utf-8")
    return built, redacted


def sums(built: dict[str, str], redacted: dict[str, str]) -> str:
    lines = [
        f"{hashlib.sha256(text.encode('utf-8')).hexdigest()}  {name}\n"
        for name, text in sorted(built.items())
    ]
    lines += [
        f"{hashlib.sha256(text.encode('utf-8')).hexdigest()}  "
        f"../schema_v2_redacted/{name}\n"
        for name, text in sorted(redacted.items())
    ]
    return "".join(lines)


def main(argv: list[str]) -> int:
    try:
        built, redacted = build()
    except PromptError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    if argv[1:] == ["--check"]:
        bad = [
            name
            for name, t in built.items()
            if not (BUILT / name).exists()
            or (BUILT / name).read_text(encoding="utf-8") != t
        ]
        stale = sorted(
            p.name
            for p in BUILT.glob("*.md")
            if p.name not in built
        )
        if bad or stale or (BUILT / "SHA256SUMS").read_text() != sums(built, redacted):
            print(f"MISMATCH: {bad or stale or 'SHA256SUMS'}", file=sys.stderr)
            return 1
        print("built prompts match")
        return 0
    BUILT.mkdir(parents=True, exist_ok=True)
    for p in BUILT.glob("*.md"):
        if p.name not in built:
            p.unlink()
    for name, text in built.items():
        (BUILT / name).write_text(text, encoding="utf-8")
    (BUILT / "SHA256SUMS").write_text(sums(built, redacted))
    print(sums(built, redacted), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
