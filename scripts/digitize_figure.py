#!/usr/bin/env python3
"""
Programmatic figure digitization for HyCAN-DB (manual v2.0 §3.4, §18 Phase A.4).

§3.4 forbids stating a number read off a plot by looking at it. Figure-only data
enters the corpus one way: a calibrated script extracts it, the calibration and
the extracted series are archived, and the script is committed so anyone can
reproduce the extraction. This is that script.

Subcommands
-----------
    colors    list the candidate series colours in an image, so the colour
              passed to ``extract`` is measured rather than guessed
    extract   calibrate axes from two reference points per axis, isolate one
              series by colour, extract its points, and archive everything
    check     the §3.4 step 6 sanity check: compare the extracted series
              against every value the paper states in its text, and record the
              outcome in the archive

Typical session
---------------
    python3 scripts/digitize_figure.py colors --image fig3.png

    python3 scripts/digitize_figure.py extract \\
        --image fig3.png --paper-id HYC-0007 --figure "Figure 3" \\
        --series-name "CDC-800, 77 K" --color "#d62728" --tolerance 40 \\
        --x1-px 118 --x1-val 0   --x2-px 942 --x2-val 100 \\
        --y1-px 806 --y1-val 0   --y2-px 104 --y2-val 5 \\
        --x-label "pressure (bar)" --y-label "uptake (wt%)" \\
        --out data/digitizations/HYC-0007_fig3.json

    python3 scripts/digitize_figure.py check \\
        --digitization data/digitizations/HYC-0007_fig3.json \\
        --at 20 --expect 1.42 --at 60 --expect 2.10 --tolerance-pct 5

Reference points are read off the image in pixel coordinates with the origin at
the top-left corner, which is what every image viewer reports. Use axis ticks,
never estimated positions: the calibration is only as good as the two points.

Three things this script refuses to do
--------------------------------------
1. Extract outside the plot area. By default the search is bounded by the box
   the four calibration reference pixels span, padded slightly. A legend
   line-sample is the same colour as its series and is usually thicker than the
   curve, so an unbounded search lets it win the per-bin median and silently
   replace real data. ``--no-roi`` disables the bound; ``--roi`` sets it
   explicitly.
2. Extract a double-valued curve as if it were single-valued. Adsorption and
   desorption branches in one colour collapse under a per-bin median into a
   midline that lies on neither branch. Bins holding two separated clusters are
   detected, reported, and refused unless ``--allow-multimodal`` is given.
3. Report a passing check as a statement about the whole series. ``check``
   verifies the points it was given, names them, and says so.

Exit codes
----------
    0  success; for ``check``, every stated value was reproduced
    1  the extraction produced nothing usable, or a ``check`` disagreed —
       §3.4 step 6: discard the digitization, do not adjust it
    2  bad arguments, or a file that does not exist

Archive contents (``--out``)
----------------------------
tool and version, UTC timestamp, source image path with its sha256 and pixel
size, every calibration parameter, the colour, tolerance and region searched,
the extraction parameters, the extracted series in both pixel and data
coordinates, and — once ``check`` has run — every check performed with its
outcome and the archive's resulting status. The source image itself is not
copied into the repository: PDFs and figure crops are gitignored (§5.1), and
the sha256 is what ties the archive to the image.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from collections import Counter
from datetime import datetime, timezone

import numpy as np

TOOL = "digitize_figure.py"
TOOL_VERSION = "2.0"

# A relative tolerance looser than this is not a check. Stated so that a
# generous --tolerance-pct cannot quietly turn the §3.4 gate into a formality.
MAX_TOLERANCE_PCT = 25.0

# An absolute tolerance is for values near zero. Beyond this fraction of the
# series' own y range it stops being a check and becomes a way around one.
MAX_TOLERANCE_ABS_FRACTION = 0.10


# ---------------------------------------------------------------------------
# Image loading
# ---------------------------------------------------------------------------

def load_rgb(path: str) -> np.ndarray:
    """Load *path* as an (H, W, 3) uint8 array, compositing alpha onto white.

    ``Image.convert("RGB")`` alone DISCARDS the alpha channel rather than
    flattening it, which is the opposite of what a digitizer needs. A
    semi-transparent fill under a curve — matplotlib's ``fill_between(...,
    alpha=0.25)``, or any figure saved with ``transparent=True`` — keeps its
    full opaque RGB and therefore matches the series colour at full strength.
    The fill is contiguous with the curve, so cluster detection sees one
    cluster, and the per-bin median lands in the middle of the filled column:
    every extracted value comes out at very close to half its true value,
    internally consistent and plausibly shaped.

    Compositing onto white is correct for a figure destined for a page. A
    transparent background also becomes white rather than black, which matters
    because black is what a dark series would be confused with.
    """
    from PIL import Image

    with Image.open(path) as image:
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            rgba = image.convert("RGBA")
            background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            return np.asarray(
                Image.alpha_composite(background, rgba).convert("RGB"),
                dtype=np.uint8,
            )
        return np.asarray(image.convert("RGB"), dtype=np.uint8)


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_color(text: str) -> tuple[int, int, int]:
    """Accept ``#rrggbb``, ``rrggbb``, or ``r,g,b``."""
    text = text.strip()
    if "," in text:
        parts = [p.strip() for p in text.split(",")]
        if len(parts) != 3:
            raise ValueError(f"expected r,g,b — got {text!r}")
        values = [int(p) for p in parts]
    else:
        hex_text = text.lstrip("#")
        if len(hex_text) != 6:
            raise ValueError(f"expected #rrggbb — got {text!r}")
        values = [int(hex_text[i:i + 2], 16) for i in (0, 2, 4)]
    for value in values:
        if not 0 <= value <= 255:
            raise ValueError(f"channel out of range in {text!r}")
    return tuple(values)  # type: ignore[return-value]


def to_hex(color) -> str:
    r, g, b = (int(c) for c in color)
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------------
# Axis calibration
# ---------------------------------------------------------------------------

class AxisCalibration:
    """Maps one pixel axis to one data axis from two reference points."""

    def __init__(self, p1: float, v1: float, p2: float, v2: float,
                 log: bool, name: str):
        if p1 == p2:
            raise ValueError(f"{name}: the two reference pixels are identical ({p1})")
        if v1 == v2:
            raise ValueError(f"{name}: the two reference values are identical ({v1})")
        if log and (v1 <= 0 or v2 <= 0):
            raise ValueError(f"{name}: a log axis needs positive reference values")
        self.p1, self.v1, self.p2, self.v2 = float(p1), float(v1), float(p2), float(v2)
        self.log = bool(log)
        self.name = name

    def to_data(self, pixels):
        """Pixel coordinate(s) -> data value(s)."""
        pixels = np.asarray(pixels, dtype=float)
        fraction = (pixels - self.p1) / (self.p2 - self.p1)
        if self.log:
            a, b = math.log10(self.v1), math.log10(self.v2)
            return np.power(10.0, a + fraction * (b - a))
        return self.v1 + fraction * (self.v2 - self.v1)

    def span(self) -> tuple[float, float]:
        """The pixel interval between the two reference points, low first."""
        return (min(self.p1, self.p2), max(self.p1, self.p2))

    def decades(self) -> float:
        """How many powers of ten the two reference values span."""
        if self.v1 == 0 or self.v2 == 0:
            return 0.0
        ratio = abs(self.v2 / self.v1)
        return abs(math.log10(ratio)) if ratio > 0 else 0.0

    def residual_at(self, pixel: float, value: float) -> tuple[float, float]:
        """(predicted value, relative error) for a third, verification tick.

        Two reference points fix a mapping exactly at those two points, so a
        linear mapping and a log mapping AGREE there and disagree everywhere
        between. A third tick is the only thing that can tell them apart.
        """
        predicted = float(self.to_data(pixel))
        denominator = max(abs(value), 1e-12)
        return predicted, abs(predicted - value) / denominator

    def data_range(self) -> tuple[float, float]:
        return (min(self.v1, self.v2), max(self.v1, self.v2))

    def as_dict(self) -> dict:
        return {
            "axis": self.name,
            "reference_1": {"pixel": self.p1, "value": self.v1},
            "reference_2": {"pixel": self.p2, "value": self.v2},
            "scale": "log10" if self.log else "linear",
        }


# ---------------------------------------------------------------------------
# colors
# ---------------------------------------------------------------------------

def candidate_colors(rgb: np.ndarray, top: int, min_saturation: int) -> list[tuple]:
    """Most common saturated colours — plot series, not axes, text, or grid."""
    flat = rgb.reshape(-1, 3).astype(int)
    spread = flat.max(axis=1) - flat.min(axis=1)
    saturated = flat[spread >= min_saturation]
    if not len(saturated):
        return []
    counts = Counter(map(tuple, saturated))
    return counts.most_common(top)


def run_colors(args) -> int:
    if not os.path.exists(args.image):
        print(f"Error: image not found: {args.image}")
        return 2
    rgb = load_rgb(args.image)
    print(f"{args.image}: {rgb.shape[1]} x {rgb.shape[0]} px")
    entries = candidate_colors(rgb, args.top, args.min_saturation)
    if not entries:
        print(f"No pixels with channel spread >= {args.min_saturation}. "
              "The figure may be greyscale; lower --min-saturation.")
        return 0
    print(f"\nTop {len(entries)} saturated colours (spread >= {args.min_saturation}):")
    print(f"  {'pixels':>8}  hex       rgb")
    for color, count in entries:
        print(f"  {count:>8}  {to_hex(color)}   {color[0]},{color[1]},{color[2]}")
    print("\nPass one of these to `extract --color`. Start with --tolerance 40 and")
    print("raise it if too few points are found (anti-aliasing softens edges).")
    return 0


# ---------------------------------------------------------------------------
# extract
# ---------------------------------------------------------------------------

def isolate_series(rgb: np.ndarray, color: tuple[int, int, int], tolerance: float,
                   roi: tuple[int, int, int, int] | None = None):
    """Pixel coordinates whose colour is within *tolerance* of *color*.

    Distance is Euclidean in RGB. *roi* is (x0, y0, x1, y1) inclusive; pixels
    outside it are discarded before anything else looks at them, which is what
    keeps a legend swatch out of the series.
    """
    difference = rgb.astype(np.int32) - np.array(color, dtype=np.int32)
    distance = np.sqrt((difference ** 2).sum(axis=2))
    matched = distance <= tolerance
    if roi is not None:
        x0, y0, x1, y1 = roi
        bounded = np.zeros_like(matched)
        bounded[y0:y1 + 1, x0:x1 + 1] = matched[y0:y1 + 1, x0:x1 + 1]
        matched = bounded
    ys, xs = np.nonzero(matched)
    return xs, ys, distance


def cluster(values: np.ndarray, max_gap: float) -> list[np.ndarray]:
    """Split sorted *values* wherever consecutive entries differ by > max_gap."""
    if not len(values):
        return []
    ordered = np.sort(np.asarray(values, dtype=float))
    breaks = np.nonzero(np.diff(ordered) > max_gap)[0]
    return np.split(ordered, breaks + 1)


def longest_run(indices: list[int]) -> int:
    """Length of the longest run of consecutive integers in *indices*."""
    if not indices:
        return 0
    ordered = sorted(set(indices))
    best = run = 1
    for previous, current in zip(ordered, ordered[1:]):
        run = run + 1 if current == previous + 1 else 1
        best = max(best, run)
    return best


def extract_points(xs, ys, bin_width: int, min_pixels: int, max_gap: float = 5.0):
    """Collapse matched pixels to one point per x bin (median y within the bin).

    Returns (points, multimodal), where *points* is a list of
    (pixel_x, pixel_y, pixel_count) and *multimodal* lists the bins whose
    matched pixels fell into more than one cluster. A double-valued curve —
    an adsorption/desorption hysteresis loop drawn in one colour — produces
    those, and its per-bin median lies on neither branch.
    """
    if bin_width < 1:
        raise ValueError("--bin-width must be >= 1")
    points: list[tuple[float, float, int]] = []
    multimodal: list[dict] = []
    if not len(xs):
        return points, multimodal

    bins = (xs // bin_width).astype(int)
    for bin_index in np.unique(bins):
        mask = bins == bin_index
        count = int(mask.sum())
        if count < min_pixels:
            continue
        bin_ys = ys[mask]
        groups = cluster(bin_ys, max_gap)
        if len(groups) > 1:
            multimodal.append({
                "bin_index": int(bin_index),
                "pixel_x": float(np.median(xs[mask])),
                "separation_px": float(
                    max(b.min() - a.max() for a, b in zip(groups, groups[1:]))
                ),
                "clusters": [
                    {"pixel_y_min": float(g.min()),
                     "pixel_y_max": float(g.max()),
                     "pixels": len(g)}
                    for g in groups
                ],
            })
        points.append(
            (float(np.median(xs[mask])), float(np.median(bin_ys)), count)
        )
    points.sort(key=lambda p: p[0])
    return points, multimodal


def default_roi(x_axis: AxisCalibration, y_axis: AxisCalibration,
                width: int, height: int, pad_pct: float) -> tuple[int, int, int, int]:
    """The plot box implied by the calibration reference pixels, padded."""
    x0, x1 = x_axis.span()
    y0, y1 = y_axis.span()
    pad_x = (x1 - x0) * pad_pct / 100.0
    pad_y = (y1 - y0) * pad_pct / 100.0
    return (
        max(0, int(math.floor(x0 - pad_x))),
        max(0, int(math.floor(y0 - pad_y))),
        min(width - 1, int(math.ceil(x1 + pad_x))),
        min(height - 1, int(math.ceil(y1 + pad_y))),
    )


def run_extract(args) -> int:
    if not os.path.exists(args.image):
        print(f"Error: image not found: {args.image}")
        return 2

    if not args.out.endswith(".json"):
        print(f"Error: --out must be a .json archive, got: {args.out}\n"
              "This guard exists because a typo here would otherwise "
              "overwrite whatever file was named.")
        return 2
    if os.path.exists(args.out) and not args.overwrite:
        print(f"Error: {args.out} already exists. Pass --overwrite to replace "
              "it.\nRe-extracting over an existing archive would erase its "
              "recorded check results, which is how a discarded digitization "
              "gets quietly replaced by an adjusted one (§3.4).")
        return 2

    try:
        color = parse_color(args.color)
        x_axis = AxisCalibration(
            args.x1_px, args.x1_val, args.x2_px, args.x2_val, args.log_x, "x"
        )
        y_axis = AxisCalibration(
            args.y1_px, args.y1_val, args.y2_px, args.y2_val, args.log_y, "y"
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    # A third tick per axis, used only as a residual check.
    #
    # Two reference points fix a mapping exactly at those two points, so a
    # linear reading of a log axis agrees with the truth at both ends and
    # disagrees everywhere between. `check` cannot catch it either, because it
    # constrains y at an x the calibration pins — and papers state values at
    # axis endpoints far more often than mid-axis. An audit produced pressure
    # errors of 13x to 398x from one omitted --log-x, certified "passed".
    verifications = []
    for axis, pixel, value in (
        (x_axis, args.x_verify_px, args.x_verify_val),
        (y_axis, args.y_verify_px, args.y_verify_val),
    ):
        if (pixel is None) != (value is None):
            print(f"Error: --{axis.name}-verify-px and --{axis.name}-verify-val "
                  "must be given together.")
            return 2
        if pixel is None:
            if not axis.log and axis.decades() > 2 and not args.assume_linear:
                print(
                    f"Error: the {axis.name} axis is declared linear but its "
                    f"reference values span {axis.decades():.1f} decades "
                    f"({axis.v1:g} to {axis.v2:g}). That is the signature of a "
                    f"log axis read without --log-{axis.name}, which agrees "
                    "with the truth at both reference points and is wrong "
                    "everywhere between.\nGive a third tick "
                    f"(--{axis.name}-verify-px/--{axis.name}-verify-val) so "
                    f"the mapping can be checked, add --log-{axis.name} if the "
                    "axis is logarithmic, or pass --assume-linear if it really "
                    "is linear across that range."
                )
                return 2
            continue
        predicted, error = axis.residual_at(pixel, value)
        verifications.append({
            "axis": axis.name, "pixel": float(pixel), "stated": float(value),
            "predicted": predicted, "relative_error": error,
        })
        if error > args.verify_tolerance_pct / 100.0:
            print(
                f"Error: the {axis.name} calibration does not reproduce its "
                f"verification tick.\n  at pixel {pixel:g} the axis states "
                f"{value:g}, the calibration predicts {predicted:.6g} "
                f"({100 * error:.2f}% off, tolerance "
                f"{args.verify_tolerance_pct:g}%).\nThe two reference points "
                f"are wrong, or the axis is "
                f"{'linear' if axis.log else 'logarithmic'} rather than "
                f"{'logarithmic' if axis.log else 'linear'}."
            )
            return 2

    rgb = load_rgb(args.image)
    height, width = rgb.shape[:2]

    for label, pixel, limit, axis in (
        ("--x1-px", args.x1_px, width, "width"),
        ("--x2-px", args.x2_px, width, "width"),
        ("--y1-px", args.y1_px, height, "height"),
        ("--y2-px", args.y2_px, height, "height"),
    ):
        if not 0 <= pixel < limit:
            print(f"Error: {label}={pixel:g} is outside the image {axis} {limit}")
            return 2

    # Region of interest. The default is the box the calibration spans, which
    # is the plot area, because the reference points are axis ticks.
    if args.no_roi:
        roi = None
        roi_note = "disabled (--no-roi)"
    elif args.roi:
        try:
            x0, y0, x1, y1 = (int(v) for v in args.roi)
        except (TypeError, ValueError):
            print("Error: --roi takes four integers: X0 Y0 X1 Y1")
            return 2
        if not (0 <= x0 < x1 < width and 0 <= y0 < y1 < height):
            print(f"Error: --roi {x0} {y0} {x1} {y1} is not inside the "
                  f"{width} x {height} image, or its corners are reversed")
            return 2
        roi = (x0, y0, x1, y1)
        roi_note = "explicit (--roi)"
    else:
        roi = default_roi(x_axis, y_axis, width, height, args.roi_pad_pct)
        roi_note = f"derived from the calibration box, padded {args.roi_pad_pct:g}%"

    unbounded, _, _ = isolate_series(rgb, color, args.tolerance, None)
    xs, ys, _ = isolate_series(rgb, color, args.tolerance, roi)

    print(f"{args.image}: {width} x {height} px")
    print(f"colour {to_hex(color)} +/- {args.tolerance}: {len(unbounded)} "
          f"matching pixels in the image")
    if roi is None:
        print("region: whole image — a legend sample in this colour will be "
              "treated as data")
    else:
        print(f"region: x {roi[0]}-{roi[2]}, y {roi[1]}-{roi[3]}  ({roi_note})")
        print(f"        {len(xs)} inside, {len(unbounded) - len(xs)} excluded")

    if not len(xs):
        print("\nNo pixels matched inside the region. Run the `colors` "
              "subcommand to measure the series colour, raise --tolerance, or "
              "widen the region with --roi.")
        return 1

    # The gap that counts as "two clusters" scales with the plot, not with a
    # fixed pixel count. At 5 px a marker's upper and lower arc, an error-bar
    # cap, and a dash gap on a steep segment all split, and an audit measured
    # those false refusals on ordinary single-valued isotherms — which trains
    # an operator to pass --allow-multimodal habitually, disabling the check
    # that actually matters.
    y_span_px = abs(y_axis.p2 - y_axis.p1)
    max_gap = args.max_gap if args.max_gap is not None else max(
        5.0, args.gap_pct_of_axis / 100.0 * y_span_px
    )

    try:
        points, multimodal = extract_points(
            xs, ys, args.bin_width, args.min_pixels, max_gap
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2
    if not points:
        print(f"\nNo x bin held >= {args.min_pixels} pixels. Lower --min-pixels "
              "or raise --bin-width.")
        return 1

    run = longest_run([entry["bin_index"] for entry in multimodal])
    fraction = len(multimodal) / len(points)
    # A hysteresis loop or a legend sample occupies a CONTIGUOUS stretch of x.
    # A marker, an error bar or a dash gap produces isolated bins. Run length
    # is what separates the two, so it, not the raw count, decides.
    structural = run >= args.min_multimodal_run or fraction >= 0.5

    if multimodal:
        print(f"\n{len(multimodal)} of {len(points)} x bins hold more than one "
              f"cluster of matched pixels (gap > {max_gap:.1f} px, "
              f"longest consecutive run {run}).")
        for entry in multimodal[:5]:
            spans = ", ".join(
                f"y {c['pixel_y_min']:.0f}-{c['pixel_y_max']:.0f}"
                for c in entry["clusters"]
            )
            print(f"    pixel_x {entry['pixel_x']:.0f}: {spans}")
        if len(multimodal) > 5:
            print(f"    ... and {len(multimodal) - 5} more")

        if structural and not args.allow_multimodal:
            print(f"\nREFUSED. {run} consecutive bins is a structural split, "
                  "not an artefact: the usual causes are an adsorption/"
                  "desorption hysteresis loop drawn in one colour, a legend "
                  "sample in the series colour, or two series sharing a "
                  "colour. A per-bin median across two branches lies on "
                  "neither of them, so the extracted value would be a number "
                  "that appears nowhere in the figure.\nCrop to one branch, "
                  "narrow --roi to exclude the legend, or pass "
                  "--allow-multimodal if you have checked that the split is "
                  "an artefact.")
            return 1
        if structural:
            print("\nProceeding under --allow-multimodal despite a structural "
                  "split. The affected bins are recorded in the archive.")
        else:
            print("\nScattered rather than contiguous, so these read as marker "
                  "edges, error-bar caps or dash gaps rather than a second "
                  "branch. Proceeding; the affected bins are recorded in the "
                  "archive.")

    px = np.array([p[0] for p in points])
    py = np.array([p[1] for p in points])
    dx = x_axis.to_data(px)
    dy = y_axis.to_data(py)

    # Points outside the calibrated axis range are extrapolations, not
    # readings, and a consumer reading `series` must be able to tell which.
    # An aggregate count cannot do that, so each point carries the flag.
    x_lo, x_hi = x_axis.data_range()
    y_lo, y_hi = y_axis.data_range()

    series = [
        {
            "x": float(x),
            "y": float(y),
            "pixel_x": float(a),
            "pixel_y": float(b),
            "pixel_count": int(c),
            "outside_axis_range": not (
                x_lo <= float(x) <= x_hi and y_lo <= float(y) <= y_hi
            ),
        }
        for x, y, (a, b, c) in zip(dx, dy, points)
    ]
    outside = [p for p in series if p["outside_axis_range"]]

    archive = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "unchecked",
        "paper_id": args.paper_id,
        "figure": args.figure,
        "series_name": args.series_name,
        "source_image": {
            "path": args.image,
            "sha256": sha256(args.image),
            "width_px": int(width),
            "height_px": int(height),
        },
        "calibration": {
            "x": {**x_axis.as_dict(), "label": args.x_label,
                  "decades_spanned": x_axis.decades()},
            "y": {**y_axis.as_dict(), "label": args.y_label,
                  "decades_spanned": y_axis.decades()},
            "verification_ticks": verifications,
        },
        "isolation": {
            "color_hex": to_hex(color),
            "color_rgb": list(color),
            "tolerance": float(args.tolerance),
            "matched_pixels_in_image": len(unbounded),
            "matched_pixels_in_region": len(xs),
            "region": list(roi) if roi else None,
            "region_basis": roi_note,
        },
        "extraction": {
            "bin_width_px": int(args.bin_width),
            "min_pixels_per_bin": int(args.min_pixels),
            "max_cluster_gap_px": float(max_gap),
            "longest_multimodal_run": int(run),
            "aggregation": "median y of matched pixels within each x bin",
            "n_points": len(series),
            "multimodal_bins": multimodal,
            "points_outside_axis_range": len(outside),
        },
        "series": series,
        "checks": [],
        "row_hint": {
            "extraction_method": "figure_digitized",
            "source_location": f"{args.figure}, digitized"
            + (f" ({args.series_name})" if args.series_name else ""),
            "notes": f"Digitized with {TOOL} v{TOOL_VERSION}; archive: "
                     f"{os.path.basename(args.out)}",
            "reminder": "extraction_confidence is reduced for digitized values "
                        "(§3.4 step 5), and the §3.4 step 6 check must pass "
                        "before any row is written: digitize_figure.py check",
        },
    }

    directory = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(directory, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(archive, handle, indent=2)
        handle.write("\n")

    print(f"\n{len(series)} points extracted")
    print(f"  x range: {dx.min():.6g} to {dx.max():.6g}  ({args.x_label or 'x'})")
    print(f"  y range: {dy.min():.6g} to {dy.max():.6g}  ({args.y_label or 'y'})")
    if outside:
        print(f"  {len(outside)} point(s) fall outside the calibrated axis "
              "range and are extrapolations, not readings")
    print(f"\nArchive: {args.out}  (status: unchecked)")
    print("\nNo row may be written from this archive until §3.4 step 6 passes:")
    print(f"  python3 {os.path.join('scripts', TOOL)} check \\")
    print(f"      --digitization {args.out} \\")
    print("      --at <x the paper states> --expect <value the paper states> \\")
    print("      --tolerance-pct 5")
    return 0


# ---------------------------------------------------------------------------
# check  (§3.4 step 6)
# ---------------------------------------------------------------------------

def interpolate(series: list[dict], x: float) -> float:
    xs = np.array([p["x"] for p in series], dtype=float)
    ys = np.array([p["y"] for p in series], dtype=float)
    order = np.argsort(xs)          # np.interp requires ascending x
    xs, ys = xs[order], ys[order]
    if x < xs.min() or x > xs.max():
        raise ValueError(
            f"x={x:g} is outside the extracted range [{xs.min():g}, {xs.max():g}]; "
            "the check must use a point the digitized series actually covers"
        )
    return float(np.interp(x, xs, ys))


def run_check(args) -> int:
    if not os.path.exists(args.digitization):
        print(f"Error: digitization not found: {args.digitization}")
        return 2
    with open(args.digitization, "r", encoding="utf-8") as handle:
        archive = json.load(handle)

    series = archive.get("series")
    if not series:
        print(f"Error: {args.digitization} holds no extracted series")
        return 2

    if args.tolerance_pct is None and args.tolerance_abs is None:
        print("Error: give --tolerance-pct or --tolerance-abs. §3.4 step 6 "
              "requires a stated tolerance.")
        return 2
    if args.tolerance_pct is not None and args.tolerance_pct > MAX_TOLERANCE_PCT:
        print(f"Error: --tolerance-pct {args.tolerance_pct:g} is looser than "
              f"{MAX_TOLERANCE_PCT:g}%, which is not a check. If the figure is "
              "genuinely this coarse, say so in the row's notes and use "
              "--tolerance-abs with a stated physical basis.")
        return 2

    y_values = [p["y"] for p in series]
    y_range = max(y_values) - min(y_values)
    if args.tolerance_abs is not None:
        if args.tolerance_abs <= 0:
            print("Error: --tolerance-abs must be positive.")
            return 2
        ceiling = MAX_TOLERANCE_ABS_FRACTION * y_range
        if y_range > 0 and args.tolerance_abs > ceiling:
            print(f"Error: --tolerance-abs {args.tolerance_abs:g} is "
                  f"{100 * args.tolerance_abs / y_range:.0f}% of this series' "
                  f"own y range ({y_range:.4g}), which is not a check. The "
                  f"ceiling is {ceiling:.4g} "
                  f"({100 * MAX_TOLERANCE_ABS_FRACTION:g}% of the range).\n"
                  "An absolute tolerance is for values near zero, where a "
                  "relative one is meaningless — not for widening the gate.")
            return 2

    if len(args.at) != len(args.expect):
        print(f"Error: {len(args.at)} --at value(s) and {len(args.expect)} "
              "--expect value(s). They pair up, so give the same number.")
        return 2

    # §3.4 step 6 says the digitization must reproduce every value the paper
    # states from the same figure. Verifying the image is still the one that
    # was digitized comes first: the sha256 is the only tie between them.
    image = archive.get("source_image", {})
    image_path, recorded = image.get("path"), image.get("sha256")
    if image_path and os.path.exists(image_path):
        actual = sha256(image_path)
        if actual != recorded:
            print(f"Error: {image_path} no longer matches the image this "
                  f"archive was extracted from.\n  archive: {recorded[:16]}...\n"
                  f"  on disk: {actual[:16]}...\nRe-extract before checking.")
            return 2
        image_state = "verified against the archived sha256"
    else:
        image_state = f"not available for verification ({image_path})"

    print(f"Digitization: {args.digitization}")
    name = archive.get("series_name") or "(unnamed series)"
    print(f"  paper {archive.get('paper_id')}, {archive.get('figure')}, {name}")
    print(f"  points: {len(series)}")
    print(f"  source image: {image_state}")
    if archive.get("extraction", {}).get("multimodal_bins"):
        print(f"  NOTE: {len(archive['extraction']['multimodal_bins'])} bin(s) "
              "held more than one cluster; this series is a per-bin median "
              "across them")
    print()

    results = []
    for at, expect in zip(args.at, args.expect):
        if args.tolerance_abs is None and expect == 0:
            print(f"Error: --expect 0 at x={at:g} cannot be checked against a "
                  "relative tolerance. Use --tolerance-abs with a value that "
                  "says how close to zero counts.")
            return 2
        try:
            got = interpolate(series, at)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 2

        difference = got - expect
        percent = (None if expect == 0
                   else 100.0 * abs(difference) / abs(expect))

        criteria = []
        passed = True
        if args.tolerance_abs is not None:
            ok = abs(difference) <= args.tolerance_abs
            criteria.append(f"|diff| <= {args.tolerance_abs:g} absolute: "
                            f"{'pass' if ok else 'FAIL'}")
            passed = passed and ok
        if args.tolerance_pct is not None:
            if expect == 0:
                # Every nonzero reading is infinitely far from zero in
                # relative terms. Applying the percentage here would discard
                # a correct digitization for being 0.03 wt% off a stated 0.
                criteria.append("relative criterion not applicable at "
                                "expect = 0; absolute criterion decides")
            else:
                ok = percent <= args.tolerance_pct
                criteria.append(f"|diff| <= {args.tolerance_pct:g}% of stated: "
                                f"{'pass' if ok else 'FAIL'}")
                passed = passed and ok

        print(f"  at x = {at:g}")
        print(f"    paper states:     {expect:g}")
        print(f"    digitized series: {got:.6g}   (linear interpolation)")
        shown = "n/a" if percent is None else f"{percent:.2f}%"
        print(f"    difference:       {difference:+.6g}  ({shown})")
        for line in criteria:
            print(f"    {line}")
        print()

        results.append({
            "at": float(at),
            "expected": float(expect),
            "got": float(got),
            "difference": float(difference),
            "percent": None if percent is None else float(percent),
            "tolerance_pct": args.tolerance_pct,
            "tolerance_abs": args.tolerance_abs,
            "passed": bool(passed),
        })

    # The verdict covers every check ever recorded on this archive, not just
    # this invocation. Otherwise a failed check is undone by re-running with an
    # easier point, which is precisely the "adjust it until it fits" that §3.4
    # forbids — and `extract` is already guarded against the same move.
    prior = archive.get("checks", [])
    prior_failures = [c for c in prior if not c.get("passed", False)]
    every_passed = all(r["passed"] for r in results) and not prior_failures
    if prior_failures and all(r["passed"] for r in results):
        print(f"NOTE: {len(prior_failures)} earlier check(s) on this archive "
              "failed. A later passing check does not undo them; the archive "
              "stays discarded. Re-extract if the calibration has been "
              "corrected.")

    # Record the outcome in the archive. Without this a failed archive is
    # byte-identical to a passed one, and "discard this digitization" is a
    # sentence the tool prints rather than an effect it has.
    archive.setdefault("checks", []).extend([
        {**r, "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        for r in results
    ])
    archive["status"] = "passed" if every_passed else "discarded"
    if every_passed:
        archive["row_hint"] = dict(archive.get("row_hint") or {})
        archive["row_hint"]["extraction_method"] = "figure_digitized"
        archive["row_hint"].pop("notes", None)
        archive["row_hint"]["notes"] = (
            f"Digitized with {TOOL} v{TOOL_VERSION}; §3.4 step 6 check passed "
            f"at {', '.join(str(r['at']) for r in results)}."
        )
    else:
        archive["row_hint"] = {
            "extraction_method": None,
            "notes": "DISCARDED by a failed §3.4 step 6 check. No row may be "
                     "written from this archive. Re-calibrate from the axis "
                     "ticks or obtain a higher-resolution crop and extract "
                     "again; do not adjust this one to fit.",
        }
    with open(args.digitization, "w", encoding="utf-8") as handle:
        json.dump(archive, handle, indent=2)
        handle.write("\n")

    checked = ", ".join(f"x={r['at']:g}" for r in results)
    if every_passed:
        print(f"PASS — the digitization reproduces the paper's stated value(s) "
              f"at {checked}.")
        print("This is a statement about those point(s), not about the whole "
              "series. Check every value the paper states from this figure.")
        print(f"Archive status recorded as 'passed' in {args.digitization}.")
        return 0

    failed = ", ".join(
        "x={:g}".format(r["at"]) for r in results if not r["passed"]
    )
    print(f"FAIL at {failed} — §3.4 step 6: discard this digitization. "
          "Do not adjust it to fit.")
    print("Re-do the calibration from the axis ticks, or obtain a "
          "higher-resolution crop, and extract again.")
    print(f"Archive status recorded as 'discarded' in {args.digitization}; "
          "its row_hint no longer names an extraction_method.")
    return 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Programmatic figure digitization (manual §3.4). "
                    "Never eyeball a plot."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    colors = sub.add_parser("colors", help="list candidate series colours in an image")
    colors.add_argument("--image", required=True)
    colors.add_argument("--top", type=int, default=12)
    colors.add_argument("--min-saturation", type=int, default=40)

    extract = sub.add_parser("extract", help="calibrate, isolate, extract, archive")
    extract.add_argument("--image", required=True)
    extract.add_argument("--out", required=True)
    extract.add_argument("--overwrite", action="store_true")
    extract.add_argument("--color", required=True)
    extract.add_argument("--tolerance", type=float, default=40.0)
    extract.add_argument("--x1-px", type=float, required=True)
    extract.add_argument("--x1-val", type=float, required=True)
    extract.add_argument("--x2-px", type=float, required=True)
    extract.add_argument("--x2-val", type=float, required=True)
    extract.add_argument("--y1-px", type=float, required=True)
    extract.add_argument("--y1-val", type=float, required=True)
    extract.add_argument("--y2-px", type=float, required=True)
    extract.add_argument("--y2-val", type=float, required=True)
    extract.add_argument("--log-x", action="store_true")
    extract.add_argument("--log-y", action="store_true")
    extract.add_argument("--roi", nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    extract.add_argument("--no-roi", action="store_true")
    extract.add_argument("--roi-pad-pct", type=float, default=2.0)
    extract.add_argument("--bin-width", type=int, default=1)
    extract.add_argument("--min-pixels", type=int, default=1)
    extract.add_argument("--max-gap", type=float, default=None)
    extract.add_argument("--gap-pct-of-axis", type=float, default=4.0)
    extract.add_argument("--min-multimodal-run", type=int, default=8)
    extract.add_argument("--allow-multimodal", action="store_true")
    extract.add_argument("--x-verify-px", type=float, default=None)
    extract.add_argument("--x-verify-val", type=float, default=None)
    extract.add_argument("--y-verify-px", type=float, default=None)
    extract.add_argument("--y-verify-val", type=float, default=None)
    extract.add_argument("--verify-tolerance-pct", type=float, default=2.0)
    extract.add_argument("--assume-linear", action="store_true")
    extract.add_argument("--paper-id", default="")
    extract.add_argument("--figure", default="")
    extract.add_argument("--series-name", default="")
    extract.add_argument("--x-label", default="")
    extract.add_argument("--y-label", default="")

    check = sub.add_parser(
        "check", help="§3.4 step 6 sanity check against stated values"
    )
    check.add_argument("--digitization", required=True)
    check.add_argument("--at", type=float, action="append", required=True)
    check.add_argument("--expect", type=float, action="append", required=True)
    check.add_argument("--tolerance-pct", type=float, default=None)
    check.add_argument("--tolerance-abs", type=float, default=None)

    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])
    if args.command == "colors":
        return run_colors(args)
    if args.command == "extract":
        return run_extract(args)
    return run_check(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
