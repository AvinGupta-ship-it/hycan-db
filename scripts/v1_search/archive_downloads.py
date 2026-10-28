"""Archive downloaded search files in references/v1_search/ (protocol §5).

Each file the browser scripts saved is checked (every stored response body
against its SHA-256), gzipped with a fixed header (`gzip -n` equivalent: no
name, no time) when larger than 1 MB, and listed in
references/v1_search/downloads.json with the SHA-256 and size of the file as
downloaded. gzip is lossless, so `gunzip -c FILE.gz | sha256sum` reproduces the
listed SHA-256, and merge_search.py reads either form.

    python3 scripts/v1_search/archive_downloads.py FILE [FILE ...]
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEARCH_DIR = ROOT / "references" / "v1_search"
GZIP_ABOVE = 1_000_000


def bodies(data: dict) -> list[dict]:
    if "batch" in data:
        return [p for b in data["batch"] for p in b["pages"]]
    return data.get("pages") or data.get("rows") or []


def check(data: dict) -> int:
    items = bodies(data)
    for it in items:
        if hashlib.sha256(it["body"].encode("utf-8")).hexdigest() != it["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {it.get('url', '')[:100]}")
    return len(items)


def main(argv: list[str]) -> int:
    manifest_path = SEARCH_DIR / "downloads.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for name in argv[1:]:
        src = Path(name)
        raw = src.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        n = check(data)
        entry = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "responses": n,
            "run_at_utc": data.get("run_at_utc"),
        }
        if len(raw) > GZIP_ABOVE:
            dest = SEARCH_DIR / (src.name + ".gz")
            dest.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
            entry["archived_as"] = dest.name
        else:
            dest = SEARCH_DIR / src.name
            dest.write_bytes(raw)
            entry["archived_as"] = dest.name
        manifest[src.name] = entry
        print(f"{src.name}: {n} responses checked -> {dest.name}")
    manifest_path.write_text(json.dumps(dict(sorted(manifest.items())), indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
