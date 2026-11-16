"""The v1.0 figures (protocol §14), from the committed §11 outputs.

Each figure is built from ``references/v1_analysis`` and the assembled
dataset only, so rerunning the analyses and then this script regenerates
every panel. Figures land in ``figures/v1/`` as PDF and 300-dpi PNG;
captions are in ``figures/v1/CAPTIONS.md`` (hand-written, no counts).
A figure whose inputs are missing is skipped with a message.

    python3 scripts/v1_search/figures.py [--out figures/v1]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ANA = ROOT / "references" / "v1_analysis"

RULE = 1.0 / 500.0  # the Chahine rule: 1 wt% per 500 m2/g
MARGIN = (1 / 1.15, 1.15)

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
    "legend.fontsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "figure.dpi": 100, "savefig.dpi": 300, "axes.spines.top": False,
    "axes.spines.right": False,
})


def save(fig, out: Path, name: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(out / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {name}")


def fig_rq1_ratio(out: Path) -> None:
    samples = pd.read_csv(ANA / "rq1_samples.csv")
    rq1 = json.loads((ANA / "rq1.json").read_text())["primary"]
    a = samples["a_bet_m2_g"].to_numpy(float)
    n = samples["n_ex_max_w1_wt_pct"].to_numpy(float)
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    grid = np.geomspace(a.min() * 0.8, a.max() * 1.2, 100)
    lo, hi = rq1["prediction_interval_95"]
    ax.fill_between(grid, grid * RULE * lo, grid * RULE * hi,
                    color="0.85", lw=0, label="95% prediction interval")
    ax.plot(grid, grid * RULE, "k--", lw=1,
            label="Chahine rule (1 wt%/500 m$^2$ g$^{-1}$)")
    ax.plot(grid, grid * RULE * rq1["ratio"], "-", color="#b2182b", lw=1.2,
            label=f"pooled ratio {rq1['ratio']:.2f}")
    ax.plot(a, n, "o", ms=3.5, mfc="#2166ac", mec="white", mew=0.4, alpha=0.85)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([500, 1000, 2000, 4000])
    ax.set_xticklabels(["500", "1000", "2000", "4000"])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel("BET area (m$^2$ g$^{-1}$)")
    ax.set_ylabel("n$_{ex,max}$ (W1 wt%)")
    ax.legend(frameon=False, loc="upper left", handlelength=1.6)
    save(fig, out, "fig_v1_rq1_ratio")


def fig_rq1_sensitivity(out: Path) -> None:
    rq1 = json.loads((ANA / "rq1.json").read_text())["primary"]
    sens = json.loads((ANA / "rq1_sensitivity.json").read_text())
    rows = [("primary", rq1)]
    labels = {
        "i_stated_excess_only": "(i) stated excess only",
        "ii_with_stated_lower_bounds": "(ii) + stated lower bounds",
        "iii_all_eligible_papers": "(iii) all eligible papers",
        "iv_without_plausibility_flagged": "(iv) without flagged rows",
        "v_area_min_500": "(v) A$_{BET}$ ≥ 500",
        "vi_all_positive_area": "(vi) all A$_{BET}$ > 0",
        "vii_unknown_wt_as_w2": "(vii) unknown wt% as W2",
        "viii_tier_a_b_only": "(viii) tier A/B only",
        "ix_no_composite_or_metal": "(ix) no composite/metal",
        "x_with_fitted_interpolated": "(x) + fitted-interpolated",
        "xii_design_weighted": "(xii) design-weighted",
    }
    for key, label in labels.items():
        if key in sens and "ratio" in sens[key]:
            rows.append((label, sens[key]))
    fig, ax = plt.subplots(figsize=(4.4, 0.28 * len(rows) + 1.0))
    ax.axvspan(*MARGIN, color="0.92", lw=0)
    ax.axvline(1.0, color="0.6", lw=0.8, ls=":")
    for i, (label, r) in enumerate(reversed(rows)):
        ci = r.get("ci95_decision") or r.get("ci95_bootstrap")
        n = r.get("n_samples", "")
        color = "#b2182b" if label == "primary" else "#2166ac"
        ax.plot(ci, [i, i], "-", color=color, lw=1.2)
        ax.plot(r["ratio"], i, "o", ms=4, color=color)
        ax.annotate(f"n={n}", (1.01, i), xycoords=("axes fraction", "data"),
                    fontsize=7, color="0.4", va="center",
                    annotation_clip=False)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([label for label, _ in reversed(rows)])
    ax.set_xlabel("ratio of n$_{ex,max}$ to A$_{BET}$/500 (95% CI)")
    lolo = sens.get("xi_leave_one_laboratory_out")
    if lolo:
        ax.set_title(
            f"leave-one-laboratory-out range "
            f"[{lolo['min']['ratio']:.3f}, {lolo['max']['ratio']:.3f}]",
            fontsize=8, color="0.3")
    save(fig, out, "fig_v1_rq1_sensitivity")


def fig_rq2_one_bar(out: Path) -> None:
    samples = pd.read_csv(ANA / "rq2_samples.csv")
    rq2 = json.loads((ANA / "rq2.json").read_text())["primary"]
    a = samples["a_bet_m2_g"].to_numpy(float)
    n = samples["n_w1_wt_pct"].to_numpy(float)
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    grid = np.geomspace(a.min() * 0.8, a.max() * 1.2, 100)
    ax.plot(grid, grid * RULE, "k--", lw=1, label="Chahine rule")
    if "terms" in rq2["a_bet"]:
        b = rq2["a_bet"]["terms"]["b_ln_a_bet"]["estimate"]
        aa = rq2["a_bet"]["terms"]["Intercept"]["estimate"]
        # The fit is ln n = a + b ln A + c ln P; drawn at P = 1 bar (ln P = 0).
        ax.plot(grid, np.exp(aa + b * np.log(grid)), "-", color="#b2182b",
                lw=1.2, label=f"fit, b = {b:.2f}")
    ax.plot(a, n, "o", ms=3.5, mfc="#2166ac", mec="white", mew=0.4, alpha=0.85)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([300, 500, 1000, 2000, 4000])
    ax.set_xticklabels(["300", "500", "1000", "2000", "4000"])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel("BET area (m$^2$ g$^{-1}$)")
    ax.set_ylabel("uptake at 0.9–1.2 bar (W1 wt%)")
    ax.legend(frameon=False, loc="upper left", handlelength=1.6)
    save(fig, out, "fig_v1_rq2_one_bar")


def fig_rq3_materials(out: Path) -> None:
    values = pd.read_csv(ANA / "rq3_values.csv")
    rq3 = json.loads((ANA / "rq3.json").read_text())
    quantities = [("a_bet", "A$_{BET}$ (m$^2$ g$^{-1}$)"),
                  ("n_ex_max", "n$_{ex,max}$ (wt%)"),
                  ("n_1bar", "n at 1 bar (wt%)"),
                  ("ratio", "ratio to A$_{BET}$/500")]
    mats = sorted(rq3["materials"])
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 0.4 * len(mats) + 1.2),
                             sharey=True, sharex=True)
    ticks = [0.8, 0.9, 1.0, 1.1, 1.25]
    for ax, (q, label) in zip(axes, quantities):
        ax.axvline(1.0, color="0.75", lw=0.8, ls=":")
        for i, m in enumerate(mats):
            vals = values[(values["material_key"] == m)
                          & (values["quantity"] == q)]["value"].to_numpy(float)
            if len(vals) < 2:
                continue  # one laboratory: no dispersion to show
            gm = float(np.exp(np.mean(np.log(vals))))
            ax.plot(vals / gm, [i] * len(vals), "o", ms=3.5, mfc="#2166ac",
                    mec="white", mew=0.4, alpha=0.85)
        ax.set_xscale("log")
        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{t:g}" for t in ticks], fontsize=7)
        ax.xaxis.set_minor_formatter(plt.NullFormatter())
        ax.set_xlabel(label, fontsize=8)
    axes[0].set_yticks(range(len(mats)))
    axes[0].set_yticklabels(mats, fontsize=7)
    fig.supxlabel("laboratory value / material geometric mean", fontsize=8,
                  y=-0.04)
    save(fig, out, "fig_v1_rq3_materials")


def fig_rq4_items(out: Path) -> None:
    rq4 = json.loads((ANA / "rq4.json").read_text())["items"]
    labels = {
        "a": "basis stated for every value", "b": "wt% convention stated",
        "c": "uncertainty or replicate", "d": "instrument + calibration",
        "e": "BET range or criteria", "f": "sample mass",
        "g": "degassing conditions", "h": "≥ 1 row flagged (§10.2)",
        "i": "H$_2$ purity", "j": "free-volume gas + T",
    }
    items = [(k, v) for k, v in rq4.items() if "p_hat" in v]
    fig, ax = plt.subplots(figsize=(4.2, 0.3 * len(items) + 0.8))
    for i, (k, r) in enumerate(reversed(items)):
        ax.plot(r["ci95"], [i, i], "-", color="#2166ac", lw=1.2)
        ax.plot(r["p_hat"], i, "o", ms=4, color="#2166ac")
        ax.annotate(f"{r['n_yes']}/{r['n_domain']}",
                    (1.02, i), fontsize=7, color="0.4", va="center",
                    annotation_clip=False)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([labels[k] for k, _ in reversed(items)])
    ax.set_xlim(0, 1)
    ax.set_xlabel("weighted share of eligible papers (Korn–Graubard 95% CI)")
    save(fig, out, "fig_v1_rq4_items")


def fig_rq5_models(out: Path) -> None:
    rq5 = json.loads((ANA / "rq5.json").read_text())["primary"]
    regimes = [("overall", "overall"), ("le_1p2_bar", "≤ 1.2 bar"),
               ("ge_10_bar", "≥ 10 bar")]
    models = [("physical", "physical"), ("linear", "linear"),
              ("xgboost", "XGBoost")]
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    width = 0.25
    colors = {"physical": "0.55", "linear": "#2166ac", "xgboost": "#b2182b"}
    for mi, (m, mlabel) in enumerate(models):
        xs = np.arange(len(regimes)) + (mi - 1) * width
        means = [rq5["by_paper"][m][r]["r2"]["mean"] for r, _ in regimes]
        los = [rq5["by_paper"][m][r]["r2"]["p2_5"] for r, _ in regimes]
        his = [rq5["by_paper"][m][r]["r2"]["p97_5"] for r, _ in regimes]
        ax.bar(xs, means, width, color=colors[m], label=mlabel)
        ax.errorbar(xs, means, yerr=[np.array(means) - los,
                                     np.array(his) - np.array(means)],
                    fmt="none", ecolor="0.2", lw=0.8, capsize=2)
    ax.set_xticks(range(len(regimes)))
    ax.set_xticklabels([label for _, label in regimes])
    ax.set_ylabel("pooled out-of-fold R$^2$")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.legend(frameon=False, loc="upper right", ncols=1)
    save(fig, out, "fig_v1_rq5_models")


FIGURES = {
    "fig_v1_rq1_ratio": (fig_rq1_ratio,
                         ["rq1_samples.csv", "rq1.json"]),
    "fig_v1_rq1_sensitivity": (fig_rq1_sensitivity,
                               ["rq1.json", "rq1_sensitivity.json"]),
    "fig_v1_rq2_one_bar": (fig_rq2_one_bar, ["rq2_samples.csv", "rq2.json"]),
    "fig_v1_rq3_materials": (fig_rq3_materials,
                             ["rq3_values.csv", "rq3.json"]),
    "fig_v1_rq4_items": (fig_rq4_items, ["rq4.json"]),
    "fig_v1_rq5_models": (fig_rq5_models, ["rq5.json"]),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "figures" / "v1"))
    args = ap.parse_args(argv)
    out = Path(args.out)
    for name, (fn, inputs) in FIGURES.items():
        missing = [f for f in inputs if not (ANA / f).exists()]
        if missing:
            print(f"skip {name}: missing {missing}")
            continue
        fn(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
