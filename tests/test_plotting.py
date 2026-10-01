"""Tests for src/hycan/plotting.py.

**This module had no tests at all before 2026-10-01**, although it produces
every published figure and is protected under manual §6.7. The gap is recorded
rather than quietly closed: `figures/` was already known to be stale (§12.4),
and an untested figure generator is how a figure can be wrong without anything
failing — which is exactly what happened when HYC-0031's `total` uptake rows
landed in the Chahine plot.

Scope is deliberately the Chahine figure, which
docs/migration_chahine_excess_only_plan.md changes, plus the smoke coverage
needed to assert that the other two figures still run. Every test carries a
``MUTATION:`` line naming the defect it would catch, and the plan's §7 mutations
were run against the finished module with this file expected to fail on each.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless; must precede the pyplot import in plotting

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from hycan import plotting as pl  # noqa: E402


def row(**kw) -> dict:
    """One plottable 77 K row. Only the columns the figures read."""
    base = dict(
        paper_id="HYC-9001",
        sample_id="HYC-9001-S1",
        measurement_id="HYC-9001-M1",
        material_class="activated_carbon",
        year=2020,
        bet_surface_area_m2_g=2000.0,
        uptake_wt_pct=4.0,
        temperature_k=77.0,
        pressure_bar=20.0,
        uptake_type="excess",
        uptake_bound="exact",
        measurement_mode="isothermal",
    )
    base.update(kw)
    return base


def frame(rows) -> pd.DataFrame:
    return pd.DataFrame(rows)


def plotted(fig) -> list[tuple[float, float]]:
    """Every (x, y) the axes actually scattered, read back off the artists."""
    points: list[tuple[float, float]] = []
    for coll in fig.axes[0].collections:
        for x, y in coll.get_offsets():
            points.append((float(x), float(y)))
    return points


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")


# --- the total-uptake exclusion ---------------------------------------------

def test_total_uptake_rows_are_not_plotted(tmp_path):
    """Plan §5 post-condition 1, and §7 mutation 1.

    MUTATION: remove the `uptake_type != "total"` filter -> this fails, and the
    figure plots a quantity the Chahine line does not describe.
    """
    df = frame([
        row(measurement_id="M1", uptake_type="excess", uptake_wt_pct=7.0),
        row(measurement_id="M2", uptake_type="total", uptake_wt_pct=8.1),
    ])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    ys = sorted(y for _, y in plotted(fig))
    assert ys == [7.0], f"a total-uptake row reached the figure: {ys}"


def test_excess_rows_are_plotted_and_not_the_ones_excluded(tmp_path):
    """Plan §7 mutation 4: exclude `excess` instead of `total`.

    MUTATION: filter on `uptake_type != "excess"` -> this fails.
    """
    df = frame([
        row(measurement_id="M1", uptake_type="excess", uptake_wt_pct=5.6),
        row(measurement_id="M2", uptake_type="total", uptake_wt_pct=6.2),
    ])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert [y for _, y in plotted(fig)] == [5.6]


def test_unspecified_rows_are_kept(tmp_path):
    """Plan §3: `unspecified` is most of the corpus and §B.5 calls it the
    field's normal state, so excluding it would empty the figure.

    MUTATION: exclude anything other than `excess` -> this fails.
    """
    df = frame([
        row(measurement_id="M1", uptake_type="unspecified", uptake_wt_pct=2.5),
        row(measurement_id="M2", uptake_type="excess", uptake_wt_pct=4.1),
        row(measurement_id="M3", uptake_type="total", uptake_wt_pct=9.9),
    ])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert sorted(y for _, y in plotted(fig)) == [2.5, 4.1]


def test_the_paired_double_count_is_gone(tmp_path):
    """Plan §5 post-condition 2, the reason one change fixes two problems.

    HYC-0031 reports total and excess at the SAME sample, temperature and
    pressure -- one measurement expressed twice. Before it, no sample/T/P group
    in this figure appeared more than once.

    MUTATION: remove the total exclusion -> the same sample/T/P is plotted
    twice and this fails.
    """
    df = frame([
        row(measurement_id="M1", uptake_type="excess", uptake_wt_pct=7.0),
        row(measurement_id="M2", uptake_type="total", uptake_wt_pct=8.1),
        row(measurement_id="M3", uptake_type="excess", uptake_wt_pct=7.2,
            pressure_bar=30.0),
        row(measurement_id="M4", uptake_type="total", uptake_wt_pct=8.9,
            pressure_bar=30.0),
    ])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert len(plotted(fig)) == 2, "a sample/T/P appeared more than once"


def test_the_exclusion_count_is_reported_after_the_77k_filter(tmp_path, capsys):
    """Plan §4 precondition 2 and §7 mutation 2.

    The count must be the number of rows the figure WOULD have plotted, so a
    298 K total row must not be counted. Applying the exclusion before the
    77 K filter reports 2 instead of 1.

    MUTATION: move the exclusion above the temperature filter -> this fails.
    """
    df = frame([
        row(measurement_id="M1", uptake_type="excess"),
        row(measurement_id="M2", uptake_type="total"),
        row(measurement_id="M3", uptake_type="total", temperature_k=298.0),
    ])
    pl.fig3_chahine(df, tmp_path / "f.png")
    out = capsys.readouterr().out
    assert "excluded 1 total-uptake row(s)" in out, out


def test_nothing_is_reported_when_there_is_nothing_to_exclude(tmp_path, capsys):
    """A figure that announces an exclusion it did not make is noise.

    MUTATION: print unconditionally -> this fails.
    """
    df = frame([row(measurement_id="M1", uptake_type="excess")])
    pl.fig3_chahine(df, tmp_path / "f.png")
    assert "excluded" not in capsys.readouterr().out


def test_the_axis_label_states_the_subset(tmp_path):
    """Plan §3 and §7 mutation 6. A figure that drops rows must say which.

    MUTATION: leave the y label as "uptake (wt%)" while excluding rows ->
    this fails, and the figure silently misrepresents its own subset.
    """
    df = frame([row(measurement_id="M1")])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    label = fig.axes[0].get_ylabel()
    assert "excess" in label and "unspecified" in label, label


# --- the change must be a no-op on the pre-HYC-0031 corpus -----------------

def test_a_frame_with_no_total_rows_plots_exactly_what_it_did_before(tmp_path):
    """Plan §5 post-condition 3.

    MUTATION: filter on a column other than uptake_type, or drop rows whose
    uptake_type is null -> this fails.
    """
    rows = [row(measurement_id=f"M{i}", uptake_type=t, uptake_wt_pct=float(i))
            for i, t in enumerate(["excess", "unspecified", "unspecified"], start=1)]
    df = frame(rows)
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert sorted(y for _, y in plotted(fig)) == [1.0, 2.0, 3.0]


def test_a_frame_of_only_total_rows_gives_the_empty_axes_not_a_crash(tmp_path):
    """Plan §5 post-condition 4.

    MUTATION: apply the exclusion after the `sub.empty` branch -> this raises.
    """
    df = frame([
        row(measurement_id="M1", uptake_type="total"),
        row(measurement_id="M2", uptake_type="total", uptake_wt_pct=9.0),
    ])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert plotted(fig) == []
    texts = [t.get_text() for t in fig.axes[0].texts]
    assert any("No 77 K rows" in t for t in texts), texts
    assert (tmp_path / "f.png").exists()


def test_rows_at_other_temperatures_and_null_bet_are_still_dropped(tmp_path):
    """The pre-existing filters must survive the change.

    MUTATION: replace the temperature filter with the uptake_type one ->
    this fails.
    """
    df = frame([
        row(measurement_id="M1", uptake_wt_pct=4.0),
        row(measurement_id="M2", temperature_k=298.0, uptake_wt_pct=0.5),
        row(measurement_id="M3", bet_surface_area_m2_g=None, uptake_wt_pct=6.0),
        row(measurement_id="M4", uptake_wt_pct=None),
    ])
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert [y for _, y in plotted(fig)] == [4.0]


def test_the_input_frame_is_not_mutated(tmp_path):
    """The module docstring promises it. MUTATION: filter in place -> fails."""
    df = frame([
        row(measurement_id="M1", uptake_type="excess"),
        row(measurement_id="M2", uptake_type="total"),
    ])
    before = df.copy()
    pl.fig3_chahine(df, tmp_path / "f.png")
    pd.testing.assert_frame_equal(df, before)


# --- the real corpus --------------------------------------------------------

def test_the_real_corpus_plots_no_total_rows(tmp_path):
    """Asserted against the committed dataset, not a fixture.

    HYC-0031 put 9 total-uptake rows into this figure's subset, 3 of them above
    their own Chahine bound. This reads the real file and requires none to
    survive.

    MUTATION: remove the exclusion -> this fails with 9 rows.
    """
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "raw" / "measurements_v0.1.csv")
    raw = df[df["temperature_k"] == 77].dropna(
        subset=["bet_surface_area_m2_g", "uptake_wt_pct"])
    assert (raw["uptake_type"] == "total").sum() > 0, (
        "the corpus no longer exercises this case; the test has stopped testing"
    )
    fig = pl.fig3_chahine(df, tmp_path / "f.png")
    assert len(plotted(fig)) == len(raw) - int((raw["uptake_type"] == "total").sum())

    # Post-condition 2 on the real data: no sample/T/P plotted twice.
    kept = raw[raw["uptake_type"] != "total"]
    groups = kept.groupby(["sample_id", "temperature_k", "pressure_bar"]).size()
    assert (groups > 1).sum() == 0, (
        f"{int((groups > 1).sum())} sample/T/P groups are plotted more than once"
    )


# --- smoke coverage for the other two figures ------------------------------

@pytest.mark.parametrize("fn", ["fig1_corpus_map", "fig2_condition_space"])
def test_the_other_figures_still_run_and_write_a_file(fn, tmp_path):
    """Not a behaviour test -- these had no coverage at all and this at least
    fails if the change broke an import or a shared helper."""
    df = frame([row(measurement_id="M1"),
                row(measurement_id="M2", material_class="SWCNT", year=2005)])
    fig = getattr(pl, fn)(df, tmp_path / f"{fn}.png")
    assert fig is not None
    assert (tmp_path / f"{fn}.png").exists()
