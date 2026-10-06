#!/usr/bin/env python3
"""Generate the publication figures for Phase 5 (manual §15), filtered per §12.3.

This is the canonical Phase-E figure generator (§5, §18 Phase E). It loads the
dataset through ``hycan.load``, applies ``analysis_subset`` where the figure is an
uptake aggregation, and writes each figure as both a 300-dpi PNG and a PDF to
``figures/``. ``src/hycan/plotting.py`` (the notebook-01 helpers) is left
untouched: its ``_MATERIAL_ORDER`` names four classes and the corpus now has
thirteen, so its palette would cycle colors. The palette here collapses the long
tail of rare classes into one grey "other (rare)" bucket, which is both
colorblind-legible and honest about where the corpus's mass is.

Figures 1–5 are built here. Figures 6–8 depend on the model and are built with
the ML stage.

Per-figure filtering, decided against the manual's intent (§12.3 is about not
mixing incompatible *uptake* numbers in an aggregation, not about hiding corpus
composition):

* Fig 1 (corpus map) and Fig 2 (condition space) describe the corpus and use the
  full dataset; their captions state the totals and the null-condition counts.
* Fig 3 (Chahine), Fig 4 (doping) and Fig 5 (tier × year) are uptake
  aggregations and use ``analysis_subset`` (plus the wt% target and, for Fig 3,
  a BET area the method confirms).

Usage:
    python3 scripts/generate_figures.py            # writes figures/*.png and *.pdf
    python3 scripts/generate_figures.py --check     # build in a temp dir, write nothing
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from hycan.load import analysis_subset, confirmed_bet_area, load_dataset  # noqa: E402
from hycan import features as _features  # noqa: E402
from hycan import ml as _ml  # noqa: E402

FIG_DIR = Path("figures")

# Fixed class order by overall corpus frequency, so a class keeps its colour
# across figures. Classes past the ninth are drawn in one grey bucket.
_CLASS_ORDER = [
    "activated_carbon",
    "composite",
    "MWCNT",
    "doped_carbon",
    "reduced_graphene_oxide",
    "carbide_derived_carbon",
    "templated_carbon",
    "SWCNT",
    "carbon_nanofiber",
]
_OTHER_LABEL = "other (rare)"
_OTHER_COLOR = (0.6, 0.6, 0.6)


def set_house_style() -> None:
    sns.set_theme(style="whitegrid", palette="colorblind")


def _class_palette() -> dict:
    cb = sns.color_palette("colorblind", n_colors=10)
    # Skip cb[7] (grey) for the named classes so it does not collide with the
    # grey "other (rare)" bucket -- that collision made SWCNT and "other"
    # indistinguishable in a first pass.
    class_colors = [cb[i] for i in (0, 1, 2, 3, 4, 5, 6, 8, 9)]
    palette = {cls: class_colors[i] for i, cls in enumerate(_CLASS_ORDER)}
    palette[_OTHER_LABEL] = _OTHER_COLOR
    return palette


def _collapse_class(series: pd.Series) -> pd.Series:
    return series.where(series.isin(_CLASS_ORDER), _OTHER_LABEL)


def _save(fig, stem: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(out_dir / f"{stem}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _legend_order(present: set) -> list:
    return [c for c in _CLASS_ORDER if c in present] + (
        [_OTHER_LABEL] if _OTHER_LABEL in present else []
    )


def fig1_corpus_map(df: pd.DataFrame, out_dir: Path) -> dict:
    """Papers per year, stacked by material_class (full corpus)."""
    palette = _class_palette()
    papers = df.dropna(subset=["paper_id"]).copy()
    papers["cls"] = _collapse_class(papers["material_class"])
    # One (paper, class) contribution per paper-year: a paper counts once per
    # class it reports in a year, deduped so many rows do not inflate a bar.
    papers = papers.drop_duplicates(subset=["paper_id", "year", "cls"])
    counts = papers.groupby(["year", "cls"]).size().unstack(fill_value=0)
    order = [c for c in _CLASS_ORDER + [_OTHER_LABEL] if c in counts.columns]
    counts = counts.reindex(columns=order)

    fig, ax = plt.subplots(figsize=(9, 5))
    years = counts.index.astype(int).astype(str)
    bottom = np.zeros(len(counts))
    for cls in counts.columns:
        vals = counts[cls].to_numpy()
        ax.bar(years, vals, bottom=bottom, label=cls, color=palette[cls])
        bottom += vals
    ax.set_title("Hydrogen sorption literature in carbon nanomaterials")
    ax.set_xlabel("year")
    ax.set_ylabel("papers (counted once per class per year)")
    ax.tick_params(axis="x", rotation=90)
    ax.legend(title="material class", fontsize=8, ncol=2)
    fig.tight_layout()
    _save(fig, "fig1_corpus_map", out_dir)
    return {"papers": int(df["paper_id"].nunique()), "rows": len(df)}


def fig2_condition_space(df: pd.DataFrame, out_dir: Path) -> dict:
    """Temperature–pressure coverage, one point per measurement with both stated."""
    palette = _class_palette()
    sub = df.dropna(subset=["temperature_k", "pressure_bar"]).copy()
    sub = sub[pd.to_numeric(sub["pressure_bar"], errors="coerce") > 0]
    sub["cls"] = _collapse_class(sub["material_class"])
    fig, ax = plt.subplots(figsize=(9, 5))
    for cls in _legend_order(set(sub["cls"])):
        rows = sub[sub["cls"] == cls]
        ax.scatter(
            pd.to_numeric(rows["temperature_k"], errors="coerce"),
            pd.to_numeric(rows["pressure_bar"], errors="coerce"),
            label=cls, color=palette[cls], s=42, edgecolor="white",
            linewidth=0.4, alpha=0.85,
        )
    ax.set_yscale("log")
    ax.set_title("Coverage of the temperature–pressure measurement space")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("pressure (bar, log scale)")
    ax.legend(title="material class", fontsize=8, ncol=2)
    fig.tight_layout()
    _save(fig, "fig2_condition_space", out_dir)
    return {
        "plotted": len(sub),
        "null_T": int(df["temperature_k"].isna().sum()),
        "null_P": int(df["pressure_bar"].isna().sum()),
    }


def fig3_chahine(df: pd.DataFrame, out_dir: Path) -> dict:
    """Uptake vs BET at 77 K with the Chahine line (the core meta-analysis figure).

    Analysis subset + wt% target + 77 K + a BET area whose method is confirmed
    BET (§10.3). `total` uptakes are excluded (they are adsorbed + compressed
    gas, not what the rule bounds); `excess`/`unspecified` are kept.
    """
    palette = _class_palette()
    w = analysis_subset(df, require_wt_pct=True).copy()
    w["bet"] = confirmed_bet_area(w)
    w = w[(pd.to_numeric(w["temperature_k"], errors="coerce") == 77) & w["bet"].notna()]
    n_total = int((w["uptake_type"] == "total").sum())
    w = w[w["uptake_type"] != "total"]
    w["cls"] = _collapse_class(w["material_class"])
    w["uptake_wt_pct"] = pd.to_numeric(w["uptake_wt_pct"], errors="coerce")

    fig, ax = plt.subplots(figsize=(9, 5))
    for cls in _legend_order(set(w["cls"])):
        rows = w[w["cls"] == cls]
        ax.scatter(rows["bet"], rows["uptake_wt_pct"], label=cls,
                   color=palette[cls], s=42, edgecolor="white",
                   linewidth=0.4, alpha=0.85)
    x_max = float(w["bet"].max())
    xs = np.linspace(0, x_max, 100)
    ax.plot(xs, xs / 500.0, color="0.3", linestyle="--", linewidth=1.5,
            label="Chahine rule (1 wt% / 500 m$^2$/g)")
    ax.set_title("The Chahine rule across material classes (77 K)")
    ax.set_xlabel("BET surface area (m$^2$/g)")
    ax.set_ylabel("H$_2$ uptake (wt%, excess or unspecified)")
    ax.legend(title="material class", fontsize=8, ncol=2)
    fig.tight_layout()
    _save(fig, "fig3_chahine", out_dir)

    # OLS slope through the origin, all tiers vs A/B only (caption sensitivity).
    def slope(frame):
        x = frame["bet"].to_numpy(float)
        y = frame["uptake_wt_pct"].to_numpy(float)
        return float(np.sum(x * y) / np.sum(x * x)) if len(frame) else float("nan")

    ab = w[w["reproducibility_tier"].isin(["A", "B"])]
    return {
        "rows": len(w), "papers": int(w["paper_id"].nunique()),
        "excluded_total": n_total,
        "slope_all_wt_per_m2": slope(w),
        "slope_AB_wt_per_m2": slope(ab),
        "chahine_ref_wt_per_m2": 1.0 / 500.0,
    }


def fig4_doping(df: pd.DataFrame, out_dir: Path) -> dict:
    """Doped vs undoped uptake per unit BET area, faceted by temperature regime.

    Respecified from the v1.0 box plot, which the corpus could not support
    (manual §15 Fig 4). Phase D added a doped subset: there are now 16 doped
    rows at 77 K/1 bar across several papers rather than 4 from one. Per-m2
    normalisation puts doped and undoped on the same axis despite different
    surface areas; faceting by regime keeps 77 K and 298 K physics apart.
    """
    w = analysis_subset(df, require_wt_pct=True).copy()
    w["bet"] = confirmed_bet_area(w)
    w = w[w["bet"].notna() & (w["bet"] > 0)]
    w["uptake_wt_pct"] = pd.to_numeric(w["uptake_wt_pct"], errors="coerce")
    w["per_area"] = w["uptake_wt_pct"] / (w["bet"] / 1000.0)  # wt% per 1000 m2/g
    w["temp"] = pd.to_numeric(w["temperature_k"], errors="coerce")
    _dop = w["dopant_element"].astype(str).str.strip()
    w["doped"] = np.where(
        w["dopant_element"].notna() & (_dop != ""), "doped", "undoped",
    )
    regimes = [("77 K (cryogenic)", 77), ("298 K (ambient)", 298)]
    present = [(lab, t) for lab, t in regimes if (w["temp"] == t).any()]
    # Per-area normalisation is unstable at low BET (a modest uptake on a
    # small-area sample explodes), so a handful of points sit far above the bulk.
    # Cap the axis to keep the distributions legible and report the off-scale
    # count per group rather than dropping or rescaling those rows.
    cap = 8.0
    order = ["undoped", "doped"]
    pal = {"undoped": (0.6, 0.6, 0.6), "doped": sns.color_palette("colorblind")[2]}
    fig, axes = plt.subplots(1, len(present), figsize=(5 * len(present), 5),
                             sharey=True, squeeze=False)
    counts = {}
    for ax, (lab, t) in zip(axes[0], present):
        reg = w[w["temp"] == t]
        sns.boxplot(data=reg, x="doped", y="per_area", order=order, hue="doped",
                    hue_order=order, palette=pal, legend=False, ax=ax,
                    showfliers=False, width=0.5)
        sns.stripplot(data=reg, x="doped", y="per_area", order=order, ax=ax,
                      color="0.2", size=3.5, jitter=0.2, alpha=0.6)
        ax.set_ylim(0, cap)
        ax.set_title(lab)
        ax.set_xlabel("")
        ax.set_ylabel("H$_2$ uptake per area (wt% per 1000 m$^2$/g)")
        grp = {}
        for k in order:
            sub_k = reg[reg["doped"] == k]
            off = int((sub_k["per_area"] > cap).sum())
            grp[k] = {"n": int(len(sub_k)), "off_scale": off}
            if off:
                ax.annotate(f"+{off} > {cap:g}", xy=(order.index(k), cap),
                            xytext=(0, -12), textcoords="offset points",
                            ha="center", va="top", fontsize=8, color="0.3")
        counts[lab] = grp
    fig.suptitle("Doping effect on area-normalised uptake, by temperature regime")
    fig.tight_layout()
    _save(fig, "fig4_doping", out_dir)
    return {"counts": counts, "y_cap": cap,
            "note": "per-area unstable at low BET; single-paper dependence in caption"}


def fig5_tier_by_year(df: pd.DataFrame, out_dir: Path) -> dict:
    """Mean uptake by year-bin, split by reproducibility tier."""
    w = analysis_subset(df, require_wt_pct=True).copy()
    w["uptake_wt_pct"] = pd.to_numeric(w["uptake_wt_pct"], errors="coerce")
    w["year"] = pd.to_numeric(w["year"], errors="coerce")
    bins = [1994, 2000, 2005, 2010, 2015, 2020, 2026]
    labels = ["95–00", "01–05", "06–10", "11–15", "16–20", "21–"]
    w["bin"] = pd.cut(w["year"], bins=bins, labels=labels)
    grp = (
        w.groupby(["bin", "reproducibility_tier"], observed=True)["uptake_wt_pct"]
        .mean()
        .unstack()
    )
    tier_colors = {"A": sns.color_palette("colorblind")[2],
                   "B": sns.color_palette("colorblind")[0],
                   "C": sns.color_palette("colorblind")[1],
                   "D": sns.color_palette("colorblind")[3]}
    grp = grp.reindex(columns=[t for t in ["A", "B", "C", "D"] if t in grp.columns])
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(grp.index))
    width = 0.8 / max(len(grp.columns), 1)
    for i, tier in enumerate(grp.columns):
        ax.bar(x + i * width, grp[tier].to_numpy(), width, label=f"Tier {tier}",
               color=tier_colors.get(tier))
    ax.set_xticks(x + width * (len(grp.columns) - 1) / 2)
    ax.set_xticklabels(grp.index)
    ax.set_title("Mean H$_2$ uptake by year and reproducibility tier")
    ax.set_xlabel("publication year")
    ax.set_ylabel("mean uptake (wt%)")
    ax.legend(title="tier")
    fig.tight_layout()
    _save(fig, "fig5_tier_by_year", out_dir)
    bin_counts = w.groupby("bin", observed=True).size().to_dict()
    return {"bin_counts": {str(k): int(v) for k, v in bin_counts.items()}}


def fig6_pred_vs_measured(df: pd.DataFrame, out_dir: Path) -> dict:
    """Out-of-fold predicted vs measured uptake, colored by tier (the KEY figure).

    Each point is predicted by an XGBoost model that did **not** train on that
    point's paper (grouped CV), so the scatter is an honest generalization
    picture, not a memorized fit. No lab-sample overlay: the Perez lab's own
    samples are Raman/XPS-characterized and carry no H2 uptake measurement to
    place here (that overlay, manual §15 Fig 6, is left for when such data exist).
    """
    frame = _features.feature_frame(df)
    X, y, groups = _features.design_matrix(frame)
    pred = _ml.out_of_fold_predictions(X, y, groups, model_name="XGBoost")
    tier = frame["reproducibility_tier"].to_numpy()
    tier_colors = {"A": sns.color_palette("colorblind")[2],
                   "B": sns.color_palette("colorblind")[0]}
    fig, ax = plt.subplots(figsize=(7, 7))
    for t in ("B", "A"):
        mask = tier == t
        ax.scatter(y[mask], pred[mask], s=40, alpha=0.8, edgecolor="white",
                   linewidth=0.4, color=tier_colors[t], label=f"Tier {t}")
    lim = float(max(y.max(), pred.max())) * 1.05
    ax.plot([0, lim], [0, lim], color="0.3", ls="--", lw=1.5, label="y = x")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_aspect("equal")
    ax.set_title("Predicted vs measured H$_2$ uptake (grouped CV, XGBoost)")
    ax.set_xlabel("measured uptake (wt%)")
    ax.set_ylabel("predicted uptake (wt%)")
    ax.legend()
    fig.tight_layout()
    _save(fig, "fig6_pred_vs_measured", out_dir)
    from sklearn.metrics import mean_absolute_error, r2_score
    return {"n_rows": int(len(y)), "n_papers": int(len(set(groups))),
            "oof_r2": float(r2_score(y, pred)),
            "oof_mae": float(mean_absolute_error(y, pred))}


def fig7_shap(df: pd.DataFrame, out_dir: Path) -> dict:
    """SHAP mean-|value| feature importance for the XGBoost model."""
    frame = _features.feature_frame(df)
    X, y, _ = _features.design_matrix(frame)
    model = _ml.fit_full(X, y, "XGBoost")
    importance, _ = _ml.shap_summary(model, X)
    top = importance.head(10)[::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(range(len(top)), top.to_numpy(), color=sns.color_palette("colorblind")[0])
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top.index)
    ax.set_xlabel("mean |SHAP value| (wt%)")
    ax.set_title("Feature importance for predicted uptake (SHAP, XGBoost)")
    fig.tight_layout()
    _save(fig, "fig7_shap", out_dir)
    return {"top_features": list(importance.head(5).index)}


def _pareto_mask(bet: np.ndarray, uptake: np.ndarray) -> np.ndarray:
    """Non-dominated set maximising uptake while minimising BET: a point is
    Pareto-optimal if no other point has >= uptake at <= BET."""
    mask = np.ones(len(bet), dtype=bool)
    for i in range(len(bet)):
        dominated = (bet <= bet[i]) & (uptake >= uptake[i]) & (
            (bet < bet[i]) | (uptake > uptake[i])
        )
        if dominated.any():
            mask[i] = False
    return mask


def fig8_pareto(df: pd.DataFrame, out_dir: Path) -> dict:
    """Uptake vs BET with the Pareto-optimal frontier (most uptake per area).

    Over (BET, micropore volume) is deferred to Phase D's doping work (§15); the
    present axis is uptake vs BET, which is the materials-design trade-off the
    corpus can support: the frontier is the set achieving the most uptake for the
    least surface area.
    """
    frame = _features.feature_frame(df)
    bet = frame["bet_surface_area_m2_g"].to_numpy(float)
    up = frame[_features.TARGET].to_numpy(float)
    ok = np.isfinite(bet) & np.isfinite(up)
    bet, up = bet[ok], up[ok]
    pm = _pareto_mask(bet, up)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(bet[~pm], up[~pm], s=36, color=(0.7, 0.7, 0.7), alpha=0.7,
               edgecolor="white", linewidth=0.3, label="dominated")
    ax.scatter(bet[pm], up[pm], s=70, color=sns.color_palette("colorblind")[3],
               edgecolor="black", linewidth=0.5, label="Pareto-optimal", zorder=5)
    order = np.argsort(bet[pm])
    ax.plot(bet[pm][order], up[pm][order], color=sns.color_palette("colorblind")[3],
            lw=1.5, zorder=4)
    ax.set_title("Materials trade-off: most uptake for the least surface area")
    ax.set_xlabel("BET surface area (m$^2$/g)")
    ax.set_ylabel("H$_2$ uptake (wt%, 77 K)")
    ax.legend()
    fig.tight_layout()
    _save(fig, "fig8_pareto", out_dir)
    return {"n_points": int(ok.sum()), "n_pareto": int(pm.sum())}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="build in a temp dir and write nothing to figures/")
    args = parser.parse_args(argv)
    set_house_style()
    df = load_dataset()
    out_dir = Path(tempfile.mkdtemp()) if args.check else FIG_DIR
    results = {
        "fig1": fig1_corpus_map(df, out_dir),
        "fig2": fig2_condition_space(df, out_dir),
        "fig3": fig3_chahine(df, out_dir),
        "fig4": fig4_doping(df, out_dir),
        "fig5": fig5_tier_by_year(df, out_dir),
        "fig6": fig6_pred_vs_measured(df, out_dir),
        "fig7": fig7_shap(df, out_dir),
        "fig8": fig8_pareto(df, out_dir),
    }
    for name, info in results.items():
        print(f"{name}: {info}")
    print(f"wrote PNG+PDF for figures 1–8 to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
