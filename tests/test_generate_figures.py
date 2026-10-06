"""Smoke test for scripts/generate_figures.py (manual §12.4, §15).

The manual notes fig1/fig2 had no behavioural coverage; this runs the whole
generator in --check mode (writing to a temp dir, nothing to figures/) and
asserts it exits 0 and emits a PNG and a PDF for each of figures 1-5. It does
not assert pixels -- only that every figure builds end to end against the real
dataset through the §12.3 filter.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_figures.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("generate_figures", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_generate_figures_check_exits_zero():
    mod = _load_module()
    assert mod.main(["--check"]) == 0


def test_each_figure_writes_png_and_pdf():
    mod = _load_module()
    mod.set_house_style()
    df = mod.load_dataset()
    out = Path(tempfile.mkdtemp())
    mod.fig1_corpus_map(df, out)
    mod.fig2_condition_space(df, out)
    mod.fig3_chahine(df, out)
    mod.fig4_doping(df, out)
    mod.fig5_tier_by_year(df, out)
    for stem in (
        "fig1_corpus_map",
        "fig2_condition_space",
        "fig3_chahine",
        "fig4_doping",
        "fig5_tier_by_year",
    ):
        assert (out / f"{stem}.png").exists(), stem
        assert (out / f"{stem}.pdf").exists(), stem


def test_fig3_slope_is_physically_plausible():
    """The Chahine sanity check (manual §12.2), as an assertion rather than an
    eyeball: the fitted 77 K slope sits in the same order as the rule and below
    it -- if a unit bug inflated uptake, this would blow past the rule."""
    mod = _load_module()
    mod.set_house_style()
    df = mod.load_dataset()
    info = mod.fig3_chahine(df, Path(tempfile.mkdtemp()))
    # Chahine reference is 1/500 = 0.002 wt%*g/m^2; the corpus should land within
    # a factor of ~2 and (as measured) just below it.
    assert 0.001 < info["slope_all_wt_per_m2"] < 0.0025
    assert info["rows"] > 100 and info["papers"] >= 20


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
