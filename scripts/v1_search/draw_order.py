"""Compute the within-stratum draw order (docs/v1_protocol.md §7).

Refuses unless references/v1_search/frame.csv is committed, unmodified, and
reproduced byte for byte by build_frame.py from the committed inputs, because
§7 says the frame and its SHA-256 are committed before the permutation is
computed, and a frame the script does not reproduce invalidates the draw.

Let s be the integer value of the first 16 hex digits of the frame's SHA-256.
The order within stratum h (h = 1 for S1, 2 for S2) is
numpy.random.default_rng([s, h]).permutation(N_h), applied to that stratum's
records sorted by frame_id.

Writes references/v1_search/draw_order.csv (stratum, position, frame_id), which
is committed before any full text is retrieved.
"""

from __future__ import annotations

import csv
import hashlib
import io
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_frame

ROOT = build_frame.ROOT
FRAME = "references/v1_search/frame.csv"
OUT = "references/v1_search/draw_order.csv"
STRATUM_INDEX = {"S1": 1, "S2": 2}


class DrawError(RuntimeError):
    pass


def check_committed(root: Path, rel: str) -> None:
    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(root), *args], check=False, capture_output=True, text=True
        )

    if git("ls-files", "--error-unmatch", rel).returncode != 0:
        raise DrawError(f"{rel} is not committed")
    if git("diff", "--quiet", "HEAD", "--", rel).returncode != 0:
        raise DrawError(f"{rel} differs from the committed version")


def seed_from_sha(sha256_hex: str) -> int:
    return int(sha256_hex[:16], 16)


def draw_order(frame_bytes: bytes) -> list[dict[str, str]]:
    rows = list(csv.DictReader(io.StringIO(frame_bytes.decode("utf-8"))))
    s = seed_from_sha(hashlib.sha256(frame_bytes).hexdigest())
    out = []
    for name, h in STRATUM_INDEX.items():
        recs = sorted(r["frame_id"] for r in rows if r["stratum"] == name)
        perm = np.random.default_rng([s, h]).permutation(len(recs))
        for pos, i in enumerate(perm, 1):
            out.append({"stratum": name, "position": str(pos), "frame_id": recs[i]})
    return out


def main() -> int:
    try:
        check_committed(ROOT, FRAME)
        rebuilt = build_frame.build()["references/v1_search/frame.csv"]
        on_disk = (ROOT / FRAME).read_bytes()
        if rebuilt != on_disk:
            raise DrawError("build_frame.py does not reproduce frame.csv byte for byte")
    except (DrawError, build_frame.FrameError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    rows = draw_order(on_disk)
    data = build_frame.csv_bytes(("stratum", "position", "frame_id"), rows)
    (ROOT / OUT).write_bytes(data)
    sha = hashlib.sha256(on_disk).hexdigest()
    print(f"frame sha256 {sha}; s = {seed_from_sha(sha)}; {len(rows)} records ordered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
