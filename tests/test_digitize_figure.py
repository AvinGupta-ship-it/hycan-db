"""Unit tests for scripts/digitize_figure.py (manual v2.0 §3.4, §18 Phase A.4).

§3.4 permits figure-only data into the corpus on one condition: a calibrated
script extracted it, the calibration is archived, and the extraction reproduces
a value the paper states in its own text. These tests exercise that chain on a
synthetic figure whose true values are known exactly, so "the digitization is
accurate" is a measured claim rather than an impression.

The synthetic figure (`figure` fixture):

    image        400 x 300 px, white
    x axis       pixel 50 -> 0,  pixel 350 -> 100     (data units, linear)
    y axis       pixel 250 -> 0, pixel 50  -> 10      (pixel axis inverted)
    red series   y = 0.05x exactly, 3 px thick, colour #d62728
    blue series  a flat distractor at y = 8, colour #1f77b4
    axes         black, drawn so colour isolation has something to reject
"""

from __future__ import annotations

import hashlib
import json

import digitize_figure as dg
import numpy as np
import pytest

RED = (214, 39, 40)
BLUE = (31, 119, 180)

X1_PX, X1_VAL, X2_PX, X2_VAL = 50.0, 0.0, 350.0, 100.0
Y1_PX, Y1_VAL, Y2_PX, Y2_VAL = 250.0, 0.0, 50.0, 10.0


def true_y(x_data: float) -> float:
    return 0.05 * x_data


def run(argv, capsys):
    code = dg.main(["digitize_figure.py"] + [str(a) for a in argv])
    return code, capsys.readouterr().out


@pytest.fixture
def figure(tmp_path):
    from PIL import Image

    canvas = np.full((300, 400, 3), 255, dtype=np.uint8)
    canvas[250, 50:351] = 0          # x axis
    canvas[50:251, 50] = 0           # y axis

    for px in range(50, 351):
        x_data = (px - X1_PX) / 3.0
        py = int(round(250 - 20 * true_y(x_data)))
        canvas[py - 1:py + 2, px] = RED
        canvas[89:92, px] = BLUE     # flat distractor near y = 8

    path = tmp_path / "fig3.png"
    Image.fromarray(canvas).save(path)
    return path


@pytest.fixture
def extracted(figure, tmp_path, capsys):
    out = tmp_path / "digitizations" / "HYC-9002_fig3.json"
    code, _ = run([
        "extract", "--image", figure, "--out", out,
        "--color", "#d62728", "--tolerance", 40,
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", X2_PX, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
        "--paper-id", "HYC-9002", "--figure", "Figure 3",
        "--series-name", "AC-800, 77 K",
        "--x-label", "pressure (bar)", "--y-label", "uptake (wt%)",
    ], capsys)
    assert code == 0
    return out


# ---------------------------------------------------------------------------
# Colour parsing
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text", ["#d62728", "d62728", "214,39,40", " 214, 39, 40 "])
def test_parse_color_accepts_every_documented_form(text):
    assert dg.parse_color(text) == RED


@pytest.mark.parametrize("text", ["#d627", "zzzzzz", "1,2", "1,2,3,4", "300,0,0"])
def test_parse_color_rejects_malformed_input(text):
    with pytest.raises(ValueError):
        dg.parse_color(text)


def test_to_hex_round_trips():
    assert dg.to_hex(RED) == "#d62728"
    assert dg.parse_color(dg.to_hex(BLUE)) == BLUE


# ---------------------------------------------------------------------------
# Axis calibration
# ---------------------------------------------------------------------------

def test_linear_axis_maps_its_reference_points_exactly():
    axis = dg.AxisCalibration(X1_PX, X1_VAL, X2_PX, X2_VAL, False, "x")
    assert axis.to_data(X1_PX) == pytest.approx(X1_VAL)
    assert axis.to_data(X2_PX) == pytest.approx(X2_VAL)


def test_linear_axis_interpolates_the_midpoint():
    axis = dg.AxisCalibration(X1_PX, X1_VAL, X2_PX, X2_VAL, False, "x")
    assert axis.to_data(200.0) == pytest.approx(50.0)


def test_an_inverted_pixel_axis_is_handled():
    """Pixel y grows downward while data y grows upward. This is the normal case."""
    axis = dg.AxisCalibration(Y1_PX, Y1_VAL, Y2_PX, Y2_VAL, False, "y")
    assert axis.to_data(250.0) == pytest.approx(0.0)
    assert axis.to_data(150.0) == pytest.approx(5.0)
    assert axis.to_data(50.0) == pytest.approx(10.0)


def test_extrapolation_beyond_the_reference_points_is_linear():
    axis = dg.AxisCalibration(X1_PX, X1_VAL, X2_PX, X2_VAL, False, "x")
    assert axis.to_data(350.0 + 300.0) == pytest.approx(200.0)


def test_an_array_of_pixels_maps_elementwise():
    axis = dg.AxisCalibration(X1_PX, X1_VAL, X2_PX, X2_VAL, False, "x")
    got = axis.to_data([50.0, 200.0, 350.0])
    assert np.allclose(got, [0.0, 50.0, 100.0])


def test_a_log_axis_is_geometric_not_arithmetic():
    """Pressure axes are routinely log (§15, Fig. 2); half way is the
    geometric mean."""
    axis = dg.AxisCalibration(100.0, 1.0, 300.0, 100.0, True, "x")
    assert axis.to_data(100.0) == pytest.approx(1.0)
    assert axis.to_data(300.0) == pytest.approx(100.0)
    assert axis.to_data(200.0) == pytest.approx(10.0)


def test_identical_reference_pixels_are_rejected():
    with pytest.raises(ValueError, match="reference pixels are identical"):
        dg.AxisCalibration(100.0, 0.0, 100.0, 10.0, False, "x")


def test_identical_reference_values_are_rejected():
    with pytest.raises(ValueError, match="reference values are identical"):
        dg.AxisCalibration(100.0, 5.0, 300.0, 5.0, False, "x")


def test_a_log_axis_with_a_zero_reference_is_rejected():
    with pytest.raises(ValueError, match="positive reference values"):
        dg.AxisCalibration(100.0, 0.0, 300.0, 100.0, True, "x")


def test_as_dict_records_every_calibration_parameter():
    axis = dg.AxisCalibration(X1_PX, X1_VAL, X2_PX, X2_VAL, False, "x")
    stored = axis.as_dict()
    assert stored["reference_1"] == {"pixel": 50.0, "value": 0.0}
    assert stored["reference_2"] == {"pixel": 350.0, "value": 100.0}
    assert stored["scale"] == "linear"
    assert dg.AxisCalibration(1, 1, 2, 10, True, "x").as_dict()["scale"] == "log10"


# ---------------------------------------------------------------------------
# Colour isolation and point extraction
# ---------------------------------------------------------------------------

def test_isolate_series_finds_the_named_series_and_rejects_the_others(figure):
    rgb = dg.load_rgb(str(figure))
    xs, ys, _ = dg.isolate_series(rgb, RED, 40)

    assert len(xs) == 301 * 3                      # 301 columns, 3 px thick
    assert set(rgb[ys, xs].reshape(-1, 3)[:, 0]) == {RED[0]}
    assert not np.any((ys >= 89) & (ys <= 91))     # no blue
    assert 250 not in set(ys[xs > 60])             # no axis


def test_a_tolerance_of_zero_still_matches_an_exact_colour(figure):
    rgb = dg.load_rgb(str(figure))
    xs, _, _ = dg.isolate_series(rgb, RED, 0)
    assert len(xs) == 301 * 3


def test_a_colour_absent_from_the_image_matches_nothing(figure):
    rgb = dg.load_rgb(str(figure))
    xs, _, _ = dg.isolate_series(rgb, (0, 255, 0), 10)
    assert len(xs) == 0


def test_extract_points_returns_one_point_per_bin_at_the_median(figure):
    rgb = dg.load_rgb(str(figure))
    xs, ys, _ = dg.isolate_series(rgb, RED, 40)
    points, multimodal = dg.extract_points(xs, ys, bin_width=1, min_pixels=1)

    assert multimodal == []
    assert len(points) == 301
    assert points[0][0] == 50.0                    # sorted by x
    assert points[-1][0] == 350.0
    assert all(count == 3 for _, _, count in points)


def test_extract_points_drops_bins_below_min_pixels(figure):
    rgb = dg.load_rgb(str(figure))
    xs, ys, _ = dg.isolate_series(rgb, RED, 40)
    points, _ = dg.extract_points(xs, ys, bin_width=1, min_pixels=4)
    assert points == []


def test_min_pixels_is_inclusive_at_the_boundary(figure):
    """Bins hold exactly 3 pixels: 3 must keep them, 4 must drop them."""
    rgb = dg.load_rgb(str(figure))
    xs, ys, _ = dg.isolate_series(rgb, RED, 40)
    kept, _ = dg.extract_points(xs, ys, bin_width=1, min_pixels=3)
    dropped, _ = dg.extract_points(xs, ys, bin_width=1, min_pixels=4)
    assert len(kept) == 301
    assert dropped == []


def test_extract_points_widens_with_bin_width(figure):
    rgb = dg.load_rgb(str(figure))
    xs, ys, _ = dg.isolate_series(rgb, RED, 40)
    points, _ = dg.extract_points(xs, ys, bin_width=10, min_pixels=1)
    assert 30 <= len(points) <= 32
    # the binned x must be the median of the bin, not its first pixel
    assert points[1][0] == pytest.approx(64.5, abs=0.6)


def test_extract_points_on_no_pixels_returns_nothing():
    assert dg.extract_points(np.array([]), np.array([]), 1, 1) == ([], [])


def test_a_bin_width_below_one_is_rejected():
    with pytest.raises(ValueError, match="bin-width"):
        dg.extract_points(np.array([1]), np.array([1]), 0, 1)


# ---------------------------------------------------------------------------
# extract — end to end, against known truth
# ---------------------------------------------------------------------------

def test_the_extraction_recovers_the_true_curve(extracted):
    archive = json.loads(extracted.read_text())
    series = archive["series"]
    assert len(series) == 301

    worst = max(abs(p["y"] - true_y(p["x"])) for p in series)
    assert worst < 0.03, f"worst y error {worst} wt%"

    worst_x = max(abs(p["x"] - (p["pixel_x"] - X1_PX) / 3.0) for p in series)
    assert worst_x < 1e-9


def test_the_extraction_spans_the_full_axis_range(extracted):
    series = json.loads(extracted.read_text())["series"]
    assert series[0]["x"] == pytest.approx(0.0)
    assert series[-1]["x"] == pytest.approx(100.0)
    assert series[-1]["y"] == pytest.approx(5.0, abs=0.03)


def test_the_archive_ties_itself_to_the_source_image_by_hash(extracted, figure):
    archive = json.loads(extracted.read_text())
    assert archive["source_image"]["sha256"] == hashlib.sha256(
        figure.read_bytes()
    ).hexdigest()
    assert archive["source_image"]["width_px"] == 400
    assert archive["source_image"]["height_px"] == 300


def test_the_archive_records_every_calibration_parameter(extracted):
    """§3.4 step 3: the calibration must be archived, not just applied."""
    calibration = json.loads(extracted.read_text())["calibration"]
    assert calibration["x"]["reference_1"] == {"pixel": 50.0, "value": 0.0}
    assert calibration["x"]["reference_2"] == {"pixel": 350.0, "value": 100.0}
    assert calibration["y"]["reference_1"] == {"pixel": 250.0, "value": 0.0}
    assert calibration["y"]["reference_2"] == {"pixel": 50.0, "value": 10.0}
    assert calibration["x"]["scale"] == "linear"
    assert calibration["x"]["label"] == "pressure (bar)"
    assert calibration["y"]["label"] == "uptake (wt%)"


def test_the_archive_records_the_isolation_parameters(extracted):
    isolation = json.loads(extracted.read_text())["isolation"]
    assert isolation["color_hex"] == "#d62728"
    assert isolation["color_rgb"] == [214, 39, 40]
    assert isolation["tolerance"] == 40.0
    assert isolation["matched_pixels_in_region"] == 903
    assert isolation["region"] is not None


def test_the_archive_names_the_only_permitted_extraction_method(extracted):
    """§3.4 step 5: figure_digitized. figure_estimated must never be assigned."""
    hint = json.loads(extracted.read_text())["row_hint"]
    assert hint["extraction_method"] == "figure_digitized"
    assert "figure_estimated" not in json.dumps(json.loads(extracted.read_text()))
    assert "AC-800, 77 K" in hint["source_location"]
    assert "extraction_confidence is reduced" in hint["reminder"]


def test_the_archive_identifies_the_paper_and_figure(extracted):
    archive = json.loads(extracted.read_text())
    assert archive["paper_id"] == "HYC-9002"
    assert archive["figure"] == "Figure 3"
    assert archive["tool"] == "digitize_figure.py"
    assert archive["created_utc"].endswith("+00:00")


def test_extract_creates_the_output_directory(extracted):
    assert extracted.parent.name == "digitizations"
    assert extracted.exists()


def test_extract_points_to_the_next_step(figure, tmp_path, capsys):
    out = tmp_path / "a.json"
    code, text = run([
        "extract", "--image", figure, "--out", out, "--color", "#d62728",
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", X2_PX, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
    ], capsys)
    assert code == 0
    assert "check" in text and "--tolerance-pct" in text


# ---------------------------------------------------------------------------
# extract — refusals
# ---------------------------------------------------------------------------

def test_a_colour_that_matches_nothing_exits_2_without_writing(
    figure, tmp_path, capsys
):
    out = tmp_path / "none.json"
    code, text = run([
        "extract", "--image", figure, "--out", out, "--color", "#00ff00",
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", X2_PX, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
    ], capsys)
    assert code == 1
    assert "No pixels matched inside the region" in text
    assert not out.exists()


def test_a_reference_pixel_outside_the_image_exits_2(figure, tmp_path, capsys):
    out = tmp_path / "none.json"
    code, text = run([
        "extract", "--image", figure, "--out", out, "--color", "#d62728",
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", 9999, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
    ], capsys)
    assert code == 2
    assert "outside the image width" in text
    assert not out.exists()


def test_a_degenerate_calibration_exits_2(figure, tmp_path, capsys):
    out = tmp_path / "none.json"
    code, text = run([
        "extract", "--image", figure, "--out", out, "--color", "#d62728",
        "--x1-px", 100, "--x1-val", X1_VAL, "--x2-px", 100, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
    ], capsys)
    assert code == 2
    assert "identical" in text
    assert not out.exists()


def test_a_missing_image_exits_2(tmp_path, capsys):
    code, text = run(["colors", "--image", tmp_path / "absent.png"], capsys)
    assert code == 2
    assert "not found" in text


# ---------------------------------------------------------------------------
# colors
# ---------------------------------------------------------------------------

def test_colors_lists_both_series_and_not_the_black_axes(figure, capsys):
    code, text = run(["colors", "--image", figure], capsys)
    assert code == 0
    assert "#d62728" in text and "#1f77b4" in text
    assert "#000000" not in text          # spread 0, below --min-saturation
    assert "400 x 300 px" in text


def test_colors_reports_a_greyscale_image_rather_than_guessing(tmp_path, capsys):
    from PIL import Image

    Image.fromarray(np.full((20, 20, 3), 128, dtype=np.uint8)).save(
        tmp_path / "grey.png"
    )
    code, text = run(["colors", "--image", tmp_path / "grey.png"], capsys)
    assert code == 0
    assert "greyscale" in text


# ---------------------------------------------------------------------------
# check — §3.4 step 6
# ---------------------------------------------------------------------------

def test_interpolate_hits_a_known_point(extracted):
    series = json.loads(extracted.read_text())["series"]
    assert dg.interpolate(series, 50.0) == pytest.approx(2.5, abs=0.03)


def test_interpolate_refuses_an_x_outside_the_extracted_range(extracted):
    series = json.loads(extracted.read_text())["series"]
    with pytest.raises(ValueError, match="outside the extracted range"):
        dg.interpolate(series, 150.0)


def test_check_passes_when_the_digitization_reproduces_the_stated_value(
    extracted, capsys
):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)
    assert code == 0
    assert "PASS" in text
    assert "AC-800, 77 K" in text


def test_check_fails_and_says_discard_not_adjust(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 3.5, "--tolerance-pct", 5], capsys)
    assert code == 1
    assert "FAIL at x=50" in text
    assert "discard this digitization" in text
    assert "Do not adjust it to fit" in text


def test_check_honours_an_absolute_tolerance(extracted, capsys):
    code, _ = run(["check", "--digitization", extracted,
                   "--at", 50, "--expect", 2.6, "--tolerance-abs", 0.2], capsys)
    assert code == 0

    code, _ = run(["check", "--digitization", extracted,
                   "--at", 50, "--expect", 2.6, "--tolerance-abs", 0.01], capsys)
    assert code == 1


def test_check_without_a_tolerance_is_refused(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5], capsys)
    assert code == 2
    assert "requires a stated tolerance" in text


def test_check_on_an_x_outside_the_range_exits_2(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 150, "--expect", 7.5, "--tolerance-pct", 5], capsys)
    assert code == 2
    assert "outside the extracted range" in text


def test_check_on_a_missing_archive_exits_2(tmp_path, capsys):
    code, text = run(["check", "--digitization", tmp_path / "absent.json",
                      "--at", 1, "--expect", 1, "--tolerance-pct", 5], capsys)
    assert code == 2
    assert "not found" in text


def test_check_on_an_archive_with_no_series_exits_2(tmp_path, capsys):
    path = tmp_path / "empty.json"
    path.write_text(json.dumps({"series": []}), encoding="utf-8")
    code, text = run(["check", "--digitization", path,
                      "--at", 1, "--expect", 1, "--tolerance-pct", 5], capsys)
    assert code == 2
    assert "no extracted series" in text


def test_check_reports_the_difference_and_the_criterion(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 20, "--expect", 1.0, "--tolerance-pct", 5], capsys)
    assert code == 0
    assert "paper states:     1" in text
    assert "digitized series:" in text
    assert "5% of stated: pass" in text


# ---------------------------------------------------------------------------
# C2 — a legend swatch must not become data
#
# An isolated audit built a figure with a legend line-sample in the series
# colour, placed in the lower-right whitespace where a legend goes on a
# saturating isotherm. The swatch is thicker than the curve, so it won the
# per-bin median: 4.88 wt% was extracted as 0.82 wt%, an 83% error across 11%
# of the x range, written to the archive as data with exit 0.
# ---------------------------------------------------------------------------

@pytest.fixture
def figure_with_legend(tmp_path):
    from PIL import Image

    canvas = np.full((300, 400, 3), 255, dtype=np.uint8)
    canvas[250, 50:351] = 0
    canvas[50:251, 50] = 0

    for px in range(50, 351):
        x_data = (px - X1_PX) / 3.0
        py = int(round(250 - 20 * true_y(x_data)))
        canvas[py - 1:py + 2, px] = RED

    # legend sample: same colour, thicker, inside the plot box, lower right
    canvas[228:237, 260:330] = RED

    path = tmp_path / "legend.png"
    Image.fromarray(canvas).save(path)
    return path


def _extract(image, out, capsys, *extra):
    return run([
        "extract", "--image", image, "--out", out,
        "--color", "#d62728", "--tolerance", 40,
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", X2_PX, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
        *extra,
    ], capsys)


def test_a_legend_swatch_inside_the_plot_box_is_detected_not_averaged(
    figure_with_legend, tmp_path, capsys
):
    """Two clusters in one bin must refuse, not silently produce a midline."""
    out = tmp_path / "d.json"
    code, text = _extract(figure_with_legend, out, capsys)

    assert code == 1
    assert "more than one cluster" in text
    assert "REFUSED" in text
    assert "hysteresis" in text
    assert not out.exists()


def test_the_legend_can_be_excluded_with_an_explicit_roi(
    figure_with_legend, tmp_path, capsys
):
    """And then the extracted curve is the real one."""
    out = tmp_path / "d.json"
    code, text = _extract(figure_with_legend, out, capsys,
                          "--roi", "50", "50", "259", "250")
    assert code == 0, text

    series = json.loads(out.read_text())["series"]
    covered = [p for p in series if p["x"] >= 60]
    assert covered, "the ROI should still cover the upper x range"
    worst = max(abs(p["y"] - true_y(p["x"])) for p in series)
    assert worst < 0.05, f"worst y error {worst} wt%"


def test_allow_multimodal_records_the_affected_bins_in_the_archive(
    figure_with_legend, tmp_path, capsys
):
    out = tmp_path / "d.json"
    code, text = _extract(figure_with_legend, out, capsys, "--allow-multimodal")

    assert code == 0
    assert "Proceeding under --allow-multimodal" in text
    bins = json.loads(out.read_text())["extraction"]["multimodal_bins"]
    assert len(bins) > 50
    assert all(len(b["clusters"]) >= 2 for b in bins)


def test_the_default_region_is_the_calibration_box(extracted):
    isolation = json.loads(extracted.read_text())["isolation"]
    assert isolation["region"] is not None
    x0, y0, x1, y1 = isolation["region"]
    assert x0 <= 50 and x1 >= 350
    assert y0 <= 50 and y1 >= 250
    assert "calibration box" in isolation["region_basis"]


def test_no_roi_searches_the_whole_image_and_says_so(figure, tmp_path, capsys):
    out = tmp_path / "d.json"
    code, text = _extract(figure, out, capsys, "--no-roi")
    assert code == 0
    assert "whole image" in text
    assert "will be treated as data" in text
    assert json.loads(out.read_text())["isolation"]["region"] is None


def test_a_reversed_or_outside_roi_is_rejected(figure, tmp_path, capsys):
    out = tmp_path / "d.json"
    code, text = _extract(figure, out, capsys, "--roi", "300", "50", "100", "250")
    assert code == 2
    assert "corners are reversed" in text or "not inside" in text
    assert not out.exists()


def test_the_region_report_counts_what_it_excluded(
    figure_with_legend, tmp_path, capsys
):
    out = tmp_path / "d.json"
    code, text = _extract(figure_with_legend, out, capsys,
                          "--roi", "50", "50", "259", "250")
    assert code == 0
    assert "excluded" in text
    archive = json.loads(out.read_text())["isolation"]
    assert archive["matched_pixels_in_image"] > archive["matched_pixels_in_region"]


# ---------------------------------------------------------------------------
# H6 — hysteresis loops
# ---------------------------------------------------------------------------

@pytest.fixture
def hysteresis_figure(tmp_path):
    from PIL import Image

    canvas = np.full((300, 400, 3), 255, dtype=np.uint8)
    for px in range(50, 351):
        x_data = (px - X1_PX) / 3.0
        for offset in (-0.5, +0.5):          # two branches, one colour
            py = int(round(250 - 20 * (true_y(x_data) + offset)))
            canvas[py - 1:py + 2, px] = RED

    path = tmp_path / "hyst.png"
    Image.fromarray(canvas).save(path)
    return path


def test_a_hysteresis_loop_is_refused_rather_than_collapsed_to_a_midline(
    hysteresis_figure, tmp_path, capsys
):
    out = tmp_path / "d.json"
    code, text = _extract(hysteresis_figure, out, capsys)

    assert code == 1
    assert "more than one cluster" in text
    assert "lies on neither of them" in text
    assert not out.exists()


def test_cluster_splits_on_a_gap_and_not_within_one():
    assert len(dg.cluster(np.array([10, 11, 12]), 5.0)) == 1
    assert len(dg.cluster(np.array([10, 11, 40, 41]), 5.0)) == 2
    assert len(dg.cluster(np.array([10, 11, 14, 15]), 5.0)) == 1
    assert dg.cluster(np.array([]), 5.0) == []


def test_max_gap_controls_the_split(hysteresis_figure, tmp_path, capsys):
    """A gap threshold wider than the branch separation stops the detection."""
    out = tmp_path / "d.json"
    code, _ = _extract(hysteresis_figure, out, capsys, "--max-gap", "100")
    assert code == 0                  # one cluster now, so no refusal
    assert json.loads(out.read_text())["extraction"]["multimodal_bins"] == []


def test_median_is_used_not_mean(figure):
    """An asymmetric outlier pixel in a bin must not move the point."""
    rgb = dg.load_rgb(str(figure)).copy()
    column = 200
    # Two stray pixels against the curve's three: asymmetric, so the mean and
    # the median genuinely differ. A symmetric blob would make this test pass
    # under either statistic and prove nothing.
    rgb[60:62, column] = RED

    xs, ys, _ = dg.isolate_series(rgb, RED, 40)
    in_column = np.sort(ys[xs == column])
    assert len(in_column) == 5

    points, multimodal = dg.extract_points(xs, ys, 1, 1)
    assert multimodal, "the blob is a second cluster and must be reported"
    point = [p for p in points if p[0] == column][0]

    expected_median = float(np.median(in_column))
    expected_mean = float(np.mean(in_column))
    assert expected_median != pytest.approx(expected_mean)   # the test is live
    assert point[1] == pytest.approx(expected_median)
    assert point[1] != pytest.approx(expected_mean)


# ---------------------------------------------------------------------------
# H7 — the archive path
# ---------------------------------------------------------------------------

def test_extract_refuses_a_non_json_output_path(figure, tmp_path, capsys):
    """A typo here would otherwise overwrite whatever file was named."""
    victim = tmp_path / "schema.py"
    victim.write_text("SENTINEL = 1\n", encoding="utf-8")

    code, text = _extract(figure, victim, capsys)

    assert code == 2
    assert "must be a .json archive" in text
    assert victim.read_text() == "SENTINEL = 1\n"


def test_extract_refuses_to_overwrite_an_existing_archive(
    figure, extracted, capsys
):
    before = extracted.read_text()
    code, text = _extract(figure, extracted, capsys)

    assert code == 2
    assert "already exists" in text
    assert "discarded digitization gets quietly replaced" in text
    assert extracted.read_text() == before


def test_overwrite_is_allowed_when_asked_for(figure, extracted, capsys):
    code, _ = _extract(figure, extracted, capsys, "--overwrite",
                       "--series-name", "second pass")
    assert code == 0
    assert json.loads(extracted.read_text())["series_name"] == "second pass"


# ---------------------------------------------------------------------------
# C4, C5, C6, M2, M4 — the check gate
# ---------------------------------------------------------------------------

def test_a_passing_check_is_recorded_in_the_archive(extracted, capsys):
    code, _ = run(["check", "--digitization", extracted,
                   "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)
    assert code == 0

    archive = json.loads(extracted.read_text())
    assert archive["status"] == "passed"
    assert len(archive["checks"]) == 1
    assert archive["checks"][0]["at"] == 50.0
    assert archive["checks"][0]["passed"] is True
    assert archive["checks"][0]["checked_utc"].endswith("+00:00")
    assert archive["row_hint"]["extraction_method"] == "figure_digitized"


def test_a_failed_check_marks_the_archive_discarded(extracted, capsys):
    """A failed archive must not be byte-identical to a passed one."""
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 3.5, "--tolerance-pct", 5], capsys)
    assert code == 1

    archive = json.loads(extracted.read_text())
    assert archive["status"] == "discarded"
    assert archive["checks"][0]["passed"] is False
    assert archive["row_hint"]["extraction_method"] is None
    assert "No row may be written" in archive["row_hint"]["notes"]
    assert "do not adjust" in archive["row_hint"]["notes"].lower()
    assert "recorded as 'discarded'" in text


def test_a_fresh_archive_is_marked_unchecked(extracted):
    archive = json.loads(extracted.read_text())
    assert archive["status"] == "unchecked"
    assert archive["checks"] == []


def test_check_verifies_several_stated_values_at_once(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 20, "--expect", 1.0,
                      "--at", 50, "--expect", 2.5,
                      "--at", 80, "--expect", 4.0,
                      "--tolerance-pct", 5], capsys)
    assert code == 0
    assert len(json.loads(extracted.read_text())["checks"]) == 3
    assert "at x=20, x=50, x=80" in text


def test_one_failing_point_among_several_discards_the_archive(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 20, "--expect", 1.0,
                      "--at", 50, "--expect", 4.9,
                      "--tolerance-pct", 5], capsys)
    assert code == 1
    assert "FAIL at x=50" in text
    assert json.loads(extracted.read_text())["status"] == "discarded"


def test_mismatched_at_and_expect_counts_are_rejected(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 20, "--at", 50, "--expect", 1.0,
                      "--tolerance-pct", 5], capsys)
    assert code == 2
    assert "They pair up" in text


def test_a_pass_is_reported_as_being_about_the_checked_points(extracted, capsys):
    """§3.4 step 6 verifies points, and the wording must not overclaim."""
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)
    assert code == 0
    assert "not about the whole series" in text
    assert "Check every value the paper states" in text


def test_both_tolerances_must_pass_when_both_are_given(extracted, capsys):
    """An absolute tolerance must not silently override a stricter relative one."""
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.6,
                      "--tolerance-pct", 0.001, "--tolerance-abs", 99], capsys)
    assert code == 1
    assert "0.001% of stated: FAIL" in text
    assert "99 absolute: pass" in text


def test_a_tolerance_looser_than_the_cap_is_refused(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 500], capsys)
    assert code == 2
    assert "is not a check" in text
    assert json.loads(extracted.read_text())["status"] == "unchecked"


def test_expect_zero_against_a_relative_tolerance_is_refused(extracted, capsys):
    """It produced a nonsense percentage and failed a correct digitization."""
    code, text = run(["check", "--digitization", extracted,
                      "--at", 0, "--expect", 0, "--tolerance-pct", 5], capsys)
    assert code == 2
    assert "cannot be checked against a relative tolerance" in text
    assert "--tolerance-abs" in text


def test_expect_zero_works_with_an_absolute_tolerance(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 0, "--expect", 0, "--tolerance-abs", 0.1], capsys)
    assert code == 0
    assert "PASS" in text


def test_check_refuses_when_the_source_image_no_longer_matches(
    extracted, figure, capsys
):
    """The sha256 is the only tie between archive and image; check must use it."""
    from PIL import Image

    Image.fromarray(np.full((300, 400, 3), 128, dtype=np.uint8)).save(figure)

    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)

    assert code == 2
    assert "no longer matches the image" in text
    assert json.loads(extracted.read_text())["status"] == "unchecked"


def test_check_says_when_the_image_was_verified(extracted, capsys):
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)
    assert code == 0
    assert "verified against the archived sha256" in text


def test_check_proceeds_and_says_so_when_the_image_is_gone(
    extracted, figure, capsys
):
    """Figure crops are gitignored (§5.1), so absence is normal, not an error."""
    figure.unlink()
    code, text = run(["check", "--digitization", extracted,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)
    assert code == 0
    assert "not available for verification" in text


def test_check_warns_that_a_multimodal_series_is_a_median(
    hysteresis_figure, tmp_path, capsys
):
    out = tmp_path / "d.json"
    _extract(hysteresis_figure, out, capsys, "--allow-multimodal")
    code, text = run(["check", "--digitization", out,
                      "--at", 50, "--expect", 2.5, "--tolerance-pct", 5], capsys)
    assert "held more than one cluster" in text
    assert "per-bin median across them" in text


# ---------------------------------------------------------------------------
# Log axes, end to end
# ---------------------------------------------------------------------------

def test_log_flags_reach_the_calibration(figure, tmp_path, capsys):
    """Unit-testing AxisCalibration's log branch does not prove the flag is wired."""
    out = tmp_path / "log.json"
    code, _ = run([
        "extract", "--image", figure, "--out", out,
        "--color", "#d62728", "--tolerance", 40,
        "--x1-px", 50, "--x1-val", 1, "--x2-px", 350, "--x2-val", 1000,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
        "--log-x",
    ], capsys)
    assert code == 0

    archive = json.loads(out.read_text())
    assert archive["calibration"]["x"]["scale"] == "log10"
    assert archive["calibration"]["y"]["scale"] == "linear"

    series = archive["series"]
    assert series[0]["x"] == pytest.approx(1.0)
    assert series[-1]["x"] == pytest.approx(1000.0)
    middle = [p for p in series if abs(p["pixel_x"] - 200) < 0.6][0]
    assert middle["x"] == pytest.approx(31.62, rel=0.02)   # geometric midpoint


def test_a_descending_data_axis_still_interpolates_correctly(
    figure, tmp_path, capsys
):
    """np.interp needs ascending x; the archive's series runs 100 -> 0 here."""
    out = tmp_path / "desc.json"
    code, _ = run([
        "extract", "--image", figure, "--out", out,
        "--color", "#d62728", "--tolerance", 40,
        "--x1-px", 50, "--x1-val", 100, "--x2-px", 350, "--x2-val", 0,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", Y2_PX, "--y2-val", Y2_VAL,
    ], capsys)
    assert code == 0

    series = json.loads(out.read_text())["series"]
    assert series[0]["x"] > series[-1]["x"]
    assert dg.interpolate(series, 50.0) == pytest.approx(2.5, abs=0.05)


def test_points_beyond_the_calibrated_axis_range_are_counted_and_reported(
    figure, tmp_path, capsys
):
    """Those points are extrapolations, not readings, and must be declared.

    The y axis is calibrated across pixels 250-200 only, so the curve's upper
    half maps above the calibrated 0-2.5 range and those points are
    extrapolations rather than readings.
    """
    out = tmp_path / "narrow.json"
    code, text = run([
        "extract", "--image", figure, "--out", out,
        "--color", "#d62728", "--tolerance", 40,
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", X2_PX, "--x2-val", X2_VAL,
        "--y1-px", 250, "--y1-val", 0, "--y2-px", 200, "--y2-val", 2.5,
        "--no-roi",
    ], capsys)

    assert code == 0
    outside = json.loads(out.read_text())["extraction"]["points_outside_axis_range"]
    assert outside > 100
    assert "extrapolations, not readings" in text


def test_a_curve_inside_its_axis_range_reports_no_extrapolations(extracted):
    archive = json.loads(extracted.read_text())
    assert archive["extraction"]["points_outside_axis_range"] == 0


# ---------------------------------------------------------------------------
# Image formats
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mode", ["RGBA", "P", "L"])
def test_load_rgb_normalises_other_image_modes(tmp_path, mode):
    from PIL import Image

    base = Image.fromarray(np.full((10, 12, 3), 200, dtype=np.uint8))
    path = tmp_path / f"{mode}.png"
    base.convert(mode).save(path)

    array = dg.load_rgb(str(path))
    assert array.shape == (10, 12, 3)
    assert array.dtype == np.uint8


def test_an_rgba_figure_extracts_normally(figure, tmp_path, capsys):
    from PIL import Image

    rgba = tmp_path / "rgba.png"
    Image.open(figure).convert("RGBA").save(rgba)

    out = tmp_path / "d.json"
    code, _ = _extract(rgba, out, capsys)
    assert code == 0
    assert len(json.loads(out.read_text())["series"]) == 301


# ---------------------------------------------------------------------------
# Tolerance actually tolerates
# ---------------------------------------------------------------------------

def test_tolerance_admits_an_anti_aliased_edge_pixel_and_zero_does_not(
    tmp_path, capsys
):
    from PIL import Image

    canvas = np.full((300, 400, 3), 255, dtype=np.uint8)
    for px in range(50, 351):
        x_data = (px - X1_PX) / 3.0
        py = int(round(250 - 20 * true_y(x_data)))
        canvas[py - 1:py + 2, px] = RED
        canvas[py + 2, px] = (218, 61, 62)        # blended edge, distance ~31

    path = tmp_path / "aa.png"
    Image.fromarray(canvas).save(path)
    rgb = dg.load_rgb(str(path))

    strict, _, _ = dg.isolate_series(rgb, RED, 0)
    loose, _, _ = dg.isolate_series(rgb, RED, 40)

    assert len(strict) == 301 * 3
    assert len(loose) == 301 * 4


def test_the_distance_metric_is_euclidean_not_per_channel():
    rgb = np.zeros((1, 3, 3), dtype=np.uint8)
    rgb[0, 0] = RED
    rgb[0, 1] = (214, 39, 70)      # one channel off by 30 -> distance 30
    rgb[0, 2] = (194, 19, 20)      # three channels off by 20 -> distance ~34.6

    within, _, _ = dg.isolate_series(rgb, RED, 32)
    assert set(within) == {0, 1}


@pytest.mark.parametrize("flag,value,axis", [
    ("--x1-px", -5, "width"),
    ("--x2-px", -1, "width"),
    ("--y1-px", -5, "height"),
    ("--y2-px", -1, "height"),
])
def test_a_negative_reference_pixel_is_rejected(
    figure, tmp_path, capsys, flag, value, axis
):
    """Pixel coordinates have the origin at the top-left; negatives are typos."""
    argv = {
        "--x1-px": X1_PX, "--x2-px": X2_PX,
        "--y1-px": Y1_PX, "--y2-px": Y2_PX,
    }
    argv[flag] = value
    out = tmp_path / "d.json"

    code, text = run([
        "extract", "--image", figure, "--out", out,
        "--color", "#d62728",
        "--x1-px", argv["--x1-px"], "--x1-val", X1_VAL,
        "--x2-px", argv["--x2-px"], "--x2-val", X2_VAL,
        "--y1-px", argv["--y1-px"], "--y1-val", Y1_VAL,
        "--y2-px", argv["--y2-px"], "--y2-val", Y2_VAL,
    ], capsys)

    assert code == 2
    assert f"is outside the image {axis}" in text
    assert not out.exists()


def test_a_reference_pixel_beyond_the_far_edge_is_rejected(
    figure, tmp_path, capsys
):
    out = tmp_path / "d.json"
    code, text = run([
        "extract", "--image", figure, "--out", out, "--color", "#d62728",
        "--x1-px", X1_PX, "--x1-val", X1_VAL, "--x2-px", X2_PX, "--x2-val", X2_VAL,
        "--y1-px", Y1_PX, "--y1-val", Y1_VAL, "--y2-px", 300, "--y2-val", Y2_VAL,
    ], capsys)
    assert code == 2
    assert "is outside the image height 300" in text
    assert not out.exists()
