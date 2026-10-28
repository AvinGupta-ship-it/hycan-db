"""Build the tools directory the v1.0 agents run from (protocol §15, Amendment 1).

The agents need two scripts, `scripts/digitize_figure.py` and
`scripts/validate_row_detail.py`, and the `hycan` modules the validator
imports. Running them from the repository would put the v0.1 rows, the v0.1
digitizations and the pilot extractions within reach of an extractor, and the
modules' comments name v0.1 papers. This script writes a directory that holds
only those files, with comments and docstrings removed (the code is unchanged:
`ast.unparse` of the same syntax tree), and a path line in each script so that
it imports `hycan` from the directory itself. It holds no data.

    python3 scripts/v1_tools_tree.py OUT_DIR       build, print MANIFEST hash
    python3 scripts/v1_tools_tree.py --check DIR   rebuild in memory, compare

OUT_DIR/MANIFEST lists every file with its SHA-256; the freezing amendment
records the SHA-256 of MANIFEST.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = (
    "src/hycan/__init__.py",
    "src/hycan/normalize.py",
    "src/hycan/schema.py",
    "src/hycan/validate.py",
    "scripts/digitize_figure.py",
    "scripts/validate_row_detail.py",
)
PATH_LINE = (
    "import sys as _sys, pathlib as _pathlib\n"
    "_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parents[1] / 'src'))"
)


class _StripDocstrings(ast.NodeTransformer):
    def _strip(self, node):
        body = node.body
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(getattr(body[0], "value", None), ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            node.body = body[1:] or [ast.Pass()]
        self.generic_visit(node)
        return node

    visit_Module = _strip
    visit_ClassDef = _strip
    visit_FunctionDef = _strip
    visit_AsyncFunctionDef = _strip


def strip(src: str, add_path: bool) -> str:
    tree = _StripDocstrings().visit(ast.parse(src))
    if add_path:
        n = 0
        while (
            n < len(tree.body)
            and isinstance(tree.body[n], ast.ImportFrom)
            and tree.body[n].module == "__future__"
        ):
            n += 1
        tree.body[n:n] = ast.parse(PATH_LINE).body
    return ast.unparse(tree) + "\n"


def v01_identifiers() -> tuple[set[str], set[str]]:
    with (ROOT / "data" / "raw" / "measurements_v0.1.csv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {r["paper_id"] for r in rows}, {r["first_author"] for r in rows}


def build() -> dict[str, str]:
    out = {}
    for rel in FILES:
        src = (ROOT / rel).read_text(encoding="utf-8")
        out[rel] = strip(src, add_path=rel.startswith("scripts/"))
    ids, authors = v01_identifiers()
    problems = []
    for rel, text in out.items():
        problems += [f"{rel}: v0.1 paper ID {p}" for p in ids if p in text]
        problems += [
            f"{rel}: v0.1 first author {a}"
            for a in authors
            if re.search(rf"\b{re.escape(a)}\b", text)
        ]
    if problems:
        raise RuntimeError("tools tree check failed:\n" + "\n".join(problems))
    out["MANIFEST"] = "".join(
        f"{hashlib.sha256(t.encode('utf-8')).hexdigest()}  {rel}\n"
        for rel, t in sorted(out.items())
    )
    return out


def main(argv: list[str]) -> int:
    try:
        files = build()
    except RuntimeError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    manifest_sha = hashlib.sha256(files["MANIFEST"].encode("utf-8")).hexdigest()
    if len(argv) == 3 and argv[1] == "--check":
        d = Path(argv[2])
        bad = [
            rel
            for rel, t in files.items()
            if not (d / rel).exists() or (d / rel).read_text(encoding="utf-8") != t
        ]
        extra = sorted(
            str(p.relative_to(d))
            for p in d.rglob("*")
            if p.is_file()
            and "__pycache__" not in p.parts
            and str(p.relative_to(d)) not in files
        )
        if bad or extra:
            print(f"MISMATCH: differ {bad}, not in MANIFEST {extra}", file=sys.stderr)
            return 1
        print(f"tools tree matches; MANIFEST sha256 {manifest_sha}")
        return 0
    if len(argv) != 2 or argv[1].startswith("-"):
        print(__doc__, file=sys.stderr)
        return 2
    d = Path(argv[1])
    if d.exists():
        print(f"REFUSED: {d} exists", file=sys.stderr)
        return 1
    for rel, t in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(t, encoding="utf-8")
    print(f"wrote {d}; MANIFEST sha256 {manifest_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
