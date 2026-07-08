"""Pure plotting functions for the HyCAN-DB corpus-overview notebook.

Each ``fig*`` function takes a dataframe and a ``save_path``, writes a
300-dpi PNG to that path (creating the parent ``figures/`` directory if
needed), and returns the matplotlib ``Figure`` so the caller can display
it inline. The functions do not mutate the input dataframe.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Consistent color per material_class across every figure in the notebook.
_MATERIAL_ORDER = ["activated_carbon", "SWCNT", "carbon_nanofiber", "other"]


def set_house_style() -> None:
    """Apply the seaborn ``whitegrid`` theme with the colorblind palette globally."""
    sns.set_theme(style="whitegrid", palette="colorblind")


def _material_palette(classes):
    """Return a stable {material_class: color} mapping for the given classes.

    Classes are ordered by a fixed house order first (so colors are stable
    across figures), then any unexpected classes are appended alphabetically.
    """
    known = [c for c in _MATERIAL_ORDER if c in set(classes)]
    extra = sorted(c for c in set(classes) if c not in _MATERIAL_ORDER)
    ordered = known + extra
    colors = sns.color_palette("colorblind", n_colors=max(len(ordered), 1))
    return {cls: colors[i] for i, cls in enumerate(ordered)}, ordered


def _ensure_parent_dir(save_path) -> None:
    """Create the directory that will hold ``save_path`` if it does not exist."""
    parent = os.path.dirname(save_path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def _save(fig, save_path) -> None:
    """Write ``fig`` to ``save_path`` as a 300-dpi PNG."""
    _ensure_parent_dir(save_path)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")


def fig1_corpus_map(df, save_path):
    """Stacked bar of paper COUNT per year, colored by material_class.

    A paper is counted once per (year, material_class): the frame is
    deduped on paper_id before counting so a paper with many measurement
    rows does not inflate the bars.
    """
    palette, ordered = _material_palette(df["material_class"].dropna().unique())

    # One row per paper; keep the fields needed for the stacked bar.
    papers = df.dropna(subset=["paper_id"]).drop_duplicates(subset="paper_id")
    counts = (
        papers.groupby(["year", "material_class"]).size().unstack(fill_value=0)
    )
    # Order columns by the house material order for stable stacking/legend.
    counts = counts.reindex(columns=[c for c in ordered if c in counts.columns])

    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = np.zeros(len(counts))
    years = counts.index.astype(int).astype(str)
    for cls in counts.columns:
        vals = counts[cls].to_numpy()
        ax.bar(years, vals, bottom=bottom, label=cls, color=palette[cls])
        bottom += vals

    ax.set_title("Hydrogen sorption literature in carbon nanomaterials")
    ax.set_xlabel("year")
    ax.set_ylabel("number of papers")
    # Integer y ticks since these are counts.
    ymax = int(bottom.max()) if len(bottom) else 0
    ax.set_yticks(range(0, ymax + 1))
    ax.legend(title="material_class")
    fig.tight_layout()

    _save(fig, save_path)
    return fig


def fig2_condition_space(df, save_path):
    """Scatter of the temperature-pressure space, one point per measurement.

    X = temperature_k, Y = pressure_bar (log scale). Points are colored by
    material_class so the reader can see which conditions each material
    family was measured at.
    """
    palette, ordered = _material_palette(df["material_class"].dropna().unique())

    sub = df.dropna(subset=["temperature_k", "pressure_bar"])

    fig, ax = plt.subplots(figsize=(8, 5))
    for cls in ordered:
        rows = sub[sub["material_class"] == cls]
        if rows.empty:
            continue
        ax.scatter(
            rows["temperature_k"],
            rows["pressure_bar"],
            label=cls,
            color=palette[cls],
            s=55,
            edgecolor="white",
            linewidth=0.5,
            alpha=0.9,
        )

    ax.set_yscale("log")
    ax.set_title("Coverage of the temperature–pressure measurement space")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("pressure (bar)")
    if not sub.empty:
        ax.legend(title="material_class")
    fig.tight_layout()

    _save(fig, save_path)
    return fig


def fig3_chahine(df, save_path):
    """Scatter of uptake_wt_pct vs bet_surface_area_m2_g for the 77 K subset.

    Overlays the Chahine rule (y = x / 500, i.e. ~1 wt% per 500 m2/g) and
    colors points by material_class. Rows with null BET are dropped; if
    nothing remains, an empty but labeled axes is saved with an annotation.
    """
    palette, ordered = _material_palette(df["material_class"].dropna().unique())

    sub = df[df["temperature_k"] == 77].dropna(
        subset=["bet_surface_area_m2_g", "uptake_wt_pct"]
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title("The Chahine rule across material classes")
    ax.set_xlabel("BET surface area (m$^2$/g)")
    ax.set_ylabel("uptake (wt%)")

    if sub.empty:
        ax.text(
            0.5,
            0.5,
            "No 77 K rows with BET",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=12,
        )
        fig.tight_layout()
        _save(fig, save_path)
        return fig

    for cls in ordered:
        rows = sub[sub["material_class"] == cls]
        if rows.empty:
            continue
        ax.scatter(
            rows["bet_surface_area_m2_g"],
            rows["uptake_wt_pct"],
            label=cls,
            color=palette[cls],
            s=55,
            edgecolor="white",
            linewidth=0.5,
            alpha=0.9,
        )

    # Chahine line y = x / 500 spanning the observed BET range (incl. origin).
    x_max = float(sub["bet_surface_area_m2_g"].max())
    x_line = np.linspace(0, x_max, 100)
    ax.plot(
        x_line,
        x_line / 500.0,
        color="0.35",
        linestyle="--",
        linewidth=1.5,
        label="Chahine rule (1 wt% / 500 m$^2$/g)",
    )

    ax.legend(title="material_class")
    fig.tight_layout()

    _save(fig, save_path)
    return fig
