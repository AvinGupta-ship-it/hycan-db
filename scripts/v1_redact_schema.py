"""Build the redacted schema v2 text that the agent prompts carry (Amendment 1).

The registered `src/hycan/schema.py` and `docs/data_dictionary.md` explain many
rules with examples from v0.1 papers: paper IDs, first authors and values. An
extractor told its paper's ID, first author and year could link those examples
to its paper, which would break the §9 blinding. The prompts therefore carry a
redacted copy that keeps every field, type, vocabulary, constraint, validator
and definition and removes the paper-specific examples and rationale.

  schema.py           the registered file with every comment and docstring
                      removed (code only: fields, vocabularies, constraints,
                      validators)
  data_dictionary.md  the registered file with the paragraphs listed in
                      REPLACE rewritten without paper-specific content and the
                      paragraphs in DROP removed

Both are built from the registration commit, so the redaction is reproducible
and auditable: `git diff --no-index` against the registered files shows exactly
what was removed. `check()` refuses if any v0.1 paper ID or first author
survives, or if any field heading or vocabulary value of the schema is lost.

    python3 scripts/v1_redact_schema.py
"""

from __future__ import annotations

import ast
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "prompts" / "v1" / "schema_v2_redacted"
REGISTRATION_COMMIT = "0190009f414488812c84d7f3bee8753cdc54f6a4"


def git_show(path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{REGISTRATION_COMMIT}:{path}"],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")


class _StripDocstrings(ast.NodeTransformer):
    def _strip(self, node):
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(
            getattr(body[0], "value", None), ast.Constant
        ) and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
        self.generic_visit(node)
        return node

    visit_Module = _strip
    visit_ClassDef = _strip
    visit_FunctionDef = _strip
    visit_AsyncFunctionDef = _strip


def redact_schema(src: str) -> str:
    """Comments vanish in ast.unparse; docstrings are removed explicitly."""
    tree = _StripDocstrings().visit(ast.parse(src))
    return (
        "# src/hycan/schema.py at the registration commit, with comments and\n"
        "# docstrings removed (protocol §15, Amendment 1).\n"
        + ast.unparse(tree)
        + "\n"
    )


# Paragraph index (blank-line separated, 0-based) -> replacement text. Every
# replacement keeps the paragraph's definitions, rules and validation and
# removes paper-specific examples.
REPLACE = {
    5: "| Attribute | Value |\n|---|---|\n| Type | String |\n| Required | Yes |\n"
    "| Example | `HYC-9001` |",
    13: "| Attribute | Value |\n|---|---|\n| Type | String |\n| Required | Yes |\n"
    "| Example | `Smith` |",
    30: "| Attribute | Value |\n|---|---|\n| Type | String |\n| Required | Yes |\n"
    "| Example | `HYC-9001-S1` |",
    34: "| Attribute | Value |\n|---|---|\n| Type | Text |\n| Required | Yes |\n"
    "| Example | `HYC-9001-M1` |",
    87: "**Definition.** Pore volume in pores below roughly 0.7 nm, as reported by "
    "the source paper. Added in schema v1.1.\n**Units.** cm³/g\n**The cutoff is "
    "the paper's, not ours.** ~0.7 nm is the conventional ultra-micropore "
    "boundary, but papers place it differently and determine it by different "
    "methods (CO₂ adsorption at 273 K, DFT/NLDFT models, probe molecules of "
    "graded size). Record the value the paper reports and put its stated cutoff "
    "and method in `notes`. This field is deliberately not validated against a "
    "fixed cutoff.\n**Validation.** `ultramicropore ≤ micropore ≤ total_pore` is "
    "enforced as an ERROR, pairwise, so a missing middle term does not suppress "
    "the outer comparison.\n**If missing.** Leave null. Most papers do not "
    "report it.",
    172: "**Definition.** Whether the uptake fields hold a measured value or a "
    "bound on one. `upper` means the true uptake is *below* the recorded number; "
    "`lower` means above.\n**Downstream contract.** Any row whose value is not "
    "`exact` must be excluded from isotherm fitting and from headline capacity "
    "statistics, and plotted as an arrow rather than a point.\n**If missing.** "
    "`exact`.",
    176: "**Definition.** That the source paper never stated this condition "
    "numerically, which is the only circumstance in which an uptake-bearing row "
    "may leave `temperature_k` or `pressure_bar` null. A condition stated only in "
    "words (\"room temperature\") is not a number and is not imputed.\n"
    "**Validation.** A flag set `true` while its field is populated is an ERROR "
    "— a row cannot both state a condition and declare it unstated. The flag is "
    "the only way to get a null past the conditions check, so nulls cannot "
    "appear by accident.\n**If missing.** `false`.",
    180: "**Definition.** What kind of measurement produced the uptake. A weight "
    "difference across a temperature cycle, or a TPD desorption integral, is not "
    "an isothermal uptake and must not be recorded as one.\n**Downstream "
    "contract.** Analysis restricts to `isothermal` by default.\n**If missing.** "
    "`isothermal`, which is true of every row predating v1.2.",
    183: "| Attribute | Value |\n|---|---|\n| Type | Float or null, 50–1500 K |\n"
    "| Required | No |\n| Example | `573` |",
    184: "**Definition.** The temperature of the state the uptake is referenced "
    "*against*, for a measurement that is not isothermal.\n**Units.** K\n**Why "
    "the range runs to 1500 K.** This is a desorption endpoint, not a "
    "measurement temperature, so `temperature_k`'s 50–500 K window does not "
    "apply.\n**Validation.** Required on any non-isothermal row that reports an "
    "uptake.\n**If missing.** Leave null; meaningful only when "
    "`measurement_mode` is not `isothermal`.",
    187: "| Attribute | Value |\n|---|---|\n| Type | String or null; float or "
    "null, 0–100 wt% |\n| Required | No |\n| Example | `Pd`, `5.0` |",
    188: "**Definition.** `metal_*` is an intentionally added supported metal and "
    "its loading by weight. `residual_metal_*` is leftover synthesis catalyst.\n"
    "**Units.** Weight percent.\n**Why these are separate from `dopant_*`.** A "
    "supported catalyst particle and a substitutional lattice heteroatom work by "
    "different mechanisms: a lattice heteroatom such as boron or nitrogen is a "
    "dopant; an impregnated metal such as cobalt or palladium is a supported "
    "metal. `dopant_concentration_at_pct` is atomic percent.\n**Why residual "
    "metal matters separately.** Residual synthesis catalyst decides whether an "
    "uptake is the carbon's at all.\n**If missing.** Leave null. Most papers "
    "have no supported metal.",
    191: "| Attribute | Value |\n|---|---|\n| Type | Float or null, 0–100 wt%; "
    "controlled: `elemental_analysis`, `XPS`, `AAS`, `ICP`, `other` |\n"
    "| Required | No |\n| Example | `3.5`, `elemental_analysis` |",
    192: "**Definition.** Dopant concentration by weight, and the technique that "
    "measured it.\n**Units.** Weight percent. Use `dopant_concentration_at_pct` "
    "for atomic percent; never convert between them, since the conversion needs "
    "a composition the paper may not give.\n**Why the method field exists.** "
    "Bulk (elemental analysis) and surface (XPS) contents can differ "
    "systematically; a concentration without its technique is not comparable "
    "across papers.\n**If missing.** Leave null.",
    198: "Not a new field, restated here because v1.3 makes the point checkable. "
    "**It is the paper's headline *total* specific surface area**, whatever "
    "method produced it; `surface_area_method` says which. It is *not* "
    "necessarily a BET value.",
    203: "**A caveat that travels with `external_surface_area_m2_g`.** It is not "
    "necessarily a geometric external surface: a paper's external area may "
    "include mesopore surface, in which case a mesopore surface area cannot be "
    "recovered from it. A paper reporting a genuinely geometric external area "
    "needs a `notes` entry saying so.",
    204: "When a row carries a micropore area, an external area **and** a total, "
    "the validator warns if the parts do not account for the whole — relative "
    "*and* absolute, 10% and 50 m²/g, both must be exceeded.",
    206: "The vocabulary includes `alpha_s_plot`, `t_plot` and `not_reported`. "
    "The three no-method values are distinct and the distinction is "
    "**enforced, not merely documented**:",
    213: "Micropore volumes from different methods and probe gases (DR on CO2 at "
    "273 K, DR on N2 at 77 K, DFT, αs-plot) are not comparable numbers; record "
    "the method and probe gas with the volume.",
    214: "The probe gas matters on its own: a paper may measure surface area by "
    "N2 at 77 K and micropore volume by CO2 at 273 K on the same row.",
    215: "**One method/probe pair per row, not per field.** Where a row's pore "
    "volumes were determined by different methods, `notes` records it and these "
    "fields carry the primary.",
    216: "The probe temperature is not a separate field: N2 physisorption is taken "
    "as 77 K and CO2 as 273 K, so the gas carries the temperature. A paper that "
    "deviates gets a `notes` entry.",
    220: "Named by probe gas rather than by pore size on purpose: calling a CO2-DR "
    "volume \"ultramicropore\" would assert a cutoff the paper may never state.",
    225: "An ultramicropore comparison only works if every value shares a "
    "cutoff, and papers' cutoffs differ (0.7 nm, 1 nm, or none stated).",
    226: "The cutoff is stated per row instead of assumed from this document. "
    "Filter on the cutoff before comparing values.",
    229: "`average_pore_diameter_nm` would otherwise mix quantities that are not "
    "interchangeable: a BJH desorption average (a mesopore size, invalid for a "
    "type-I isotherm), a DR characteristic-energy slit width, an HK median "
    "micropore size, and Stoeckli's L0.",
    230: "`geometric_from_S_V` is a width back-calculated from the micropore area "
    "and volume under an assumed pore shape. It is **not a "
    "pore-size-distribution model at all**, so recording it as BJH or DFT would "
    "misdescribe how the number was obtained.",
    232: "`volumetric_capacity_kg_m3`: float, 0–200 kg/m³, optional. Hydrogen "
    "stored per unit volume. **`volumetric_capacity_basis` is required whenever "
    "it is populated** — an unqualified volumetric figure is not interpretable, "
    "because per pore volume and per tank volume can differ by more than a "
    "factor of two.",
    234: "`volumetric_capacity_includes_compressed_gas`: bool, default `False`. "
    "`True` when the figure includes the compressed hydrogen in the tank volume, "
    "as a total-per-tank figure does; an adsorbed-phase density excludes it.",
    238: "A separate field from `volumetric_capacity_kg_m3` rather than a basis "
    "value on it, because a paper can report both an adsorbed density per "
    "micropore volume and a capacity per tank volume for the same sample at the "
    "same conditions.",
    241: "`packing_density_g_cm3` is sample mass per volume of tank — the "
    "quantity that converts an adsorbed amount into a system-level capacity. A "
    "compacted, loose or tapped density should be identified in `notes`.",
    242: "**`skeletal_density_g_cm3` is load-bearing, not decorative.** A helium "
    "(skeletal) density may be what a paper uses to subtract the compressed-gas "
    "contribution from a measured weight increase; without it, the "
    "excess/absolute basis of that paper's numbers cannot be reconstructed.",
    245: "An areal uptake lets a reader check a gravimetric figure against the "
    "paper's own film mass and area.",
    247: "Float ≥ 0, optional. The d-spacing between graphene or graphitic "
    "layers, from XRD.",
    250: "`volumetric_capacity_kg_m3` does not convert without a density the "
    "paper may not state, and computing a wt% from it would present this "
    "project's arithmetic as the paper's measurement.",
    251: "So a row may report uptake and carry a null `uptake_wt_pct`. **Any "
    "gravimetric analysis must filter on `uptake_wt_pct` presence rather than on "
    "\"reports uptake\",** because a null is dropped silently by a mean.",
}
REPLACE.update(
    {
        168: "Eleven fields added in schema v1.2, at physical positions 41–51.",
        169: "Every one is defaulted so that rows predating the migration remain "
        "valid unchanged — a pre-v1.2 row does assert an exact, isothermal "
        "measurement with both conditions stated, which is what the defaults "
        "say.",
        195: "Sixteen fields added in schema v1.3, at physical positions 52–67: "
        "surface-area components and methods, pore-volume methods and cutoffs, "
        "and volumetric and areal capacity.",
        196: "Every field is defaulted so that rows predating the migration remain "
        "valid unchanged.",
    }
)
DROP = {199, 202, 208, 209, 219, 235}


def redact_dictionary(text: str) -> str:
    paras = re.split(r"\n\s*\n", text)
    out = []
    for i, p in enumerate(paras):
        if i in DROP:
            continue
        out.append(REPLACE.get(i, p))
    header = (
        "<!-- docs/data_dictionary.md at the registration commit, with "
        "paper-specific examples removed (protocol §15, Amendment 1). -->\n\n"
    )
    return header + "\n\n".join(out) + "\n"


def v01_identifiers() -> tuple[set[str], set[str]]:
    with (ROOT / "data" / "raw" / "measurements_v0.1.csv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {r["paper_id"] for r in rows}, {r["first_author"] for r in rows}


def check(schema_text: str, dict_text: str) -> list[str]:
    problems = []
    ids, authors = v01_identifiers()
    for text, name in ((schema_text, "schema.py"), (dict_text, "data_dictionary.md")):
        for pid in ids:
            if pid in text:
                problems.append(f"{name}: v0.1 paper ID {pid}")
        for a in authors:
            if re.search(rf"\b{re.escape(a)}\b", text):
                problems.append(f"{name}: v0.1 first author {a}")
    sys.path.insert(0, str(ROOT / "src"))
    import typing

    from hycan.schema import MeasurementEntry

    for name, f in MeasurementEntry.model_fields.items():
        if f"`{name}`" not in dict_text:
            problems.append(f"data_dictionary.md: field {name} not mentioned")
        if name not in schema_text:
            problems.append(f"schema.py: field {name} lost")
        ann = f.annotation
        args = typing.get_args(ann)
        lits = [a for a in (ann, *args) if typing.get_origin(a) is typing.Literal]
        for lit in lits:
            for v in typing.get_args(lit):
                if f"'{v}'" not in schema_text:
                    problems.append(f"schema.py: value {v} of {name} lost")
    return problems


def build() -> dict[str, str]:
    schema_text = redact_schema(git_show("src/hycan/schema.py"))
    dict_text = redact_dictionary(git_show("docs/data_dictionary.md"))
    problems = check(schema_text, dict_text)
    if problems:
        raise RuntimeError("redaction check failed:\n" + "\n".join(problems))
    return {"schema.py": schema_text, "data_dictionary.md": dict_text}


def main() -> int:
    try:
        out = build()
    except RuntimeError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in out.items():
        (OUT / name).write_text(text, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
