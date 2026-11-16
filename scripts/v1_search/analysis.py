"""The §11 analyses of the v1.0 protocol, from the assembled dataset.

`rq1` builds the RQ1 primary set (hycan.v1_sets), fits the primary and
secondary models (hycan.v1_rq1) and writes, under references/v1_analysis/:

  - ``rq1_samples.csv`` — the analysis units (one n_ex,max per sample);
  - ``rq1.json`` — the primary ratio with both 95% intervals and the §11
    decision, the secondary slope, the exclusion ladder from all coded 77 K
    excess isotherms down to the primary set, and the distribution of
    ``p_at_nmax_bar`` with every value outside 10–60 bar listed.

`rq1-sens` runs the §11 RQ1 sensitivity analyses (i)–(xiii) and writes
``rq1_sensitivity.json``: (i)–(x) rerun the primary model on the changed set;
(xi) is leave-one-laboratory-out; (xii) the §7 design-weighted mean (weights
N_h/d_h from ``frame_counts.json`` and ``walk.json``); (xiii) the v0.1
specification, ``hycan.meta.chahine_mixedlm`` on ``hycan.meta.chahine_subset``
(unchanged since commit 45c669a), applied to all rows of the
probability-sample papers. Each variant that yields a decision records
whether it differs from the primary decision in ``rq1.json``.

`rq2` builds the RQ2 window set (hycan.v1_rq2), fits models (a)-(c) on the
probability sample and again on all §4-eligible papers (§7's pre-specified
secondary analysis), and writes ``rq2_samples.csv`` and ``rq2.json``.

`rq3` computes the interlaboratory CVs (hycan.v1_rq3) over all §4-eligible
papers and writes ``rq3_values.csv`` and ``rq3.json``.

`rq4` computes the §11 reporting-practice survey (hycan.v1_rq4) over the
probability sample and writes ``rq4_items.csv`` and ``rq4.json``.

`rq5` runs the §11 prediction baselines (hycan.v1_rq5) on the probability
sample and on all §4-eligible papers, and writes ``rq5_rows.csv`` and
``rq5.json``.

`rq1-mods` fits the §11 RQ1 moderators, each added alone to the primary
model and then all together on the complete cases, and writes
``rq1_moderators.json`` and the per-sample ``rq1_moderator_frame.csv``.
Material classes with fewer than 5 papers in the frame are merged into
``other``; categorical references are the most frequent level. All
exploratory, per §11.

    python3 scripts/v1_search/analysis.py rq1 [--processed ...] [--tree ...]
        [--out references/v1_analysis] [--boot 2000]
    python3 scripts/v1_search/analysis.py rq1-sens [same options]
    python3 scripts/v1_search/analysis.py rq1-mods [same options minus --boot]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hycan import v1, v1_rq1, v1_sets  # noqa: E402 — after the path shim


def dual_papers(tree: Path) -> set[str]:
    with (tree / "papers.csv").open(newline="", encoding="utf-8") as fh:
        return {r["paper_id"] for r in csv.DictReader(fh) if r["mode"] == "dual"}


def ladder(df: pd.DataFrame, dual: set[str]) -> dict:
    """Isotherms and papers lost at each §11/RQ1 step (the §11.0
    missing-data report for the primary set)."""
    iso = v1.isotherm_table(df)
    iso = iso[iso["paper_id"].isin(sorted(dual))]
    steps = {"coded_77k_excess_isotherms": iso}
    steps["nmax_observed_or_plateau"] = iso[
        iso["nmax_status"].isin(v1_sets.PRIMARY_STATUSES)
        & ~iso["basis_shape_conflict"].astype(bool)
    ]
    measured = v1_sets.eligible_isotherms(df, dual, area_min=None)
    steps["every_point_measured"] = measured
    steps["eligible_area_300"] = v1_sets.eligible_isotherms(df, dual)
    return {
        name: {"isotherms": len(t),
               "papers": int(t["paper_id"].nunique()) if len(t) else 0}
        for name, t in steps.items()
    }


def cmd_rq1(args) -> int:
    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    dual = dual_papers(tree)
    samples = v1_sets.rq1_samples(df, dual)
    out.mkdir(parents=True, exist_ok=True)
    samples.to_csv(out / "rq1_samples.csv", index=False, lineterminator="\n")

    primary = v1_rq1.fit_primary(samples, n_boot=args.boot)
    secondary = v1_rq1.fit_secondary(samples)
    iso = v1_sets.eligible_isotherms(df, dual)
    p = iso["p_at_nmax_bar"].astype(float)
    outside = iso[(p < 10) | (p > 60)]
    report = {
        "primary": primary,
        "secondary": secondary,
        "exclusion_ladder": ladder(df, dual),
        "p_at_nmax_bar": {
            "n": len(p),
            "quartiles": [float(x) for x in np.percentile(p, [25, 50, 75])],
            "min": float(p.min()), "max": float(p.max()),
            "outside_10_60_bar": [
                {"isotherm_key": r["isotherm_key"],
                 "p_at_nmax_bar": float(r["p_at_nmax_bar"])}
                for _, r in outside.iterrows()
            ],
        },
    }
    (out / "rq1.json").write_text(json.dumps(report, indent=2) + "\n",
                                  encoding="utf-8")
    print(f"samples {primary['n_samples']}, papers {primary['n_papers']}, "
          f"labs {primary['n_labs']}")
    print(f"ratio {primary['ratio']:.4f}, t CI {primary['ci95_t']}, "
          f"bootstrap CI {primary['ci95_bootstrap']}")
    print(f"decision: {primary['decision']} "
          f"(CI {primary['ci95_decision']}, margin {v1_rq1.MARGIN})")
    print(f"prediction interval: {primary['prediction_interval_95']}")
    print(f"secondary b = {secondary['b']:.4f} CI {secondary['ci95']}, "
          f"corrected {secondary['b_corrected_10pct']:.4f} / "
          f"{secondary['b_corrected_20pct']:.4f}")
    return 0


def paper_rows(tree: Path) -> list[dict]:
    with (tree / "papers.csv").open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _flagged(df: pd.DataFrame) -> pd.Series:
    return df["plausibility_flag"].map(lambda x: bool(v1.as_bool(x)))


def cmd_rq1_sens(args) -> int:
    from hycan import meta

    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    rows = paper_rows(tree)
    dual = {r["paper_id"] for r in rows if r["mode"] == "dual"}
    eligible_all = dual | {
        r["paper_id"] for r in rows if r["selection_route"] == "legacy_v0.1"
    }
    primary_decision = json.loads((out / "rq1.json").read_text())["primary"]["decision"]
    results = {}

    def run(name, frame=None, papers=dual, **options):
        samples = v1_sets.rq1_samples(df if frame is None else frame,
                                      papers, **options)
        if len(samples) < 3 or samples["lab_id"].nunique() < 2:
            results[name] = {"skipped": f"{len(samples)} samples"}
            return
        fit = v1_rq1.fit_primary(samples, n_boot=args.boot)
        fit["differs_from_primary"] = fit["decision"] != primary_decision
        results[name] = fit
        print(f"{name}: n={fit['n_samples']} ratio={fit['ratio']:.4f} "
              f"{fit['decision']}", flush=True)

    run("i_stated_excess_only", stated_only=True)
    run("ii_with_stated_lower_bounds", stated_lower_bound=True)
    run("iii_all_eligible_papers", papers=eligible_all)
    run("iv_without_plausibility_flagged", frame=df[~_flagged(df)])
    run("v_area_min_500", area_min=500.0)
    run("vi_all_positive_area", area_min=0.0)
    run("vii_unknown_wt_as_w2", unknown_as_w2=True)
    run("viii_tier_a_b_only",
        frame=df[df["reporting_tier"].isin(["A", "B"])])
    run("ix_no_composite_or_metal",
        frame=df[(df["material_class"] != "composite")
                 & df["metal_element"].map(lambda x: v1.as_str(x) is None)])
    run("x_with_fitted_interpolated",
        value_kinds=("measured", "fitted_interpolated"))

    samples = v1_sets.rq1_samples(df, dual)
    results["xi_leave_one_laboratory_out"] = v1_rq1.fit_lolo(samples)

    fc = json.loads(
        (ROOT / "references" / "v1_search" / "frame_counts.json").read_text())
    walk = json.loads(
        (ROOT / "references" / "v1_fulltext" / "walk.json").read_text())
    w_stratum = {h: fc[f"frame_{h}"] / walk[h]["taken"] for h in ("S1", "S2")}
    strata = {r["paper_id"]: r["stratum"] for r in rows if r["mode"] == "dual"}
    weighted = v1_rq1.fit_weighted(
        samples, samples["paper_id"].map(lambda p: w_stratum[strata[p]]),
        n_boot=args.boot)
    weighted["weights"] = w_stratum
    weighted["differs_from_primary"] = weighted["decision"] != primary_decision
    results["xii_design_weighted"] = weighted

    v01 = meta.chahine_mixedlm(df[df["paper_id"].isin(sorted(dual))])
    results["xiii_v01_specification"] = v01

    (out / "rq1_sensitivity.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8")
    lolo = results["xi_leave_one_laboratory_out"]
    print(f"lolo range [{lolo['min']['ratio']:.4f}, {lolo['max']['ratio']:.4f}]")
    print(f"design-weighted ratio {weighted['ratio']:.4f} "
          f"CI {weighted['ci95_bootstrap']} -> {weighted['decision']}")
    print(f"v0.1 spec wt% per 500 m2/g: {v01['wt_pct_per_500_m2']:.4f} "
          f"CI {v01['wt_pct_per_500_m2_ci95']}")
    differing = [k for k, v in results.items() if v.get("differs_from_primary")]
    print(f"variants differing from primary decision: {differing or 'none'}")
    return 0


def cmd_rq2(args) -> int:
    from hycan import v1_rq2

    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    rows = paper_rows(tree)
    dual = {r["paper_id"] for r in rows if r["mode"] == "dual"}
    eligible_all = dual | {
        r["paper_id"] for r in rows if r["selection_route"] == "legacy_v0.1"
    }
    out.mkdir(parents=True, exist_ok=True)
    samples = v1_rq2.rq2_samples(df, dual)
    samples.to_csv(out / "rq2_samples.csv", index=False, lineterminator="\n")
    report = {"primary": v1_rq2.fit_rq2(samples, n_boot=args.boot)}
    report["all_eligible_papers"] = v1_rq2.fit_rq2(
        v1_rq2.rq2_samples(df, eligible_all), n_boot=args.boot)
    (out / "rq2.json").write_text(json.dumps(report, indent=2) + "\n",
                                  encoding="utf-8")
    for scope, r in report.items():
        a = r["a_bet"]
        ratio = r["c_one_bar_ratio"]
        print(f"{scope}: n={a.get('n_samples')} "
              f"b={a['terms']['b_ln_a_bet']['estimate']:.4f} "
              f"CI {a['terms']['b_ln_a_bet']['ci95']}" if "terms" in a
              else f"{scope}: {a}", flush=True)
        print(f"  1-bar ratio {ratio['ratio']:.4f} CI {ratio['ci95_decision']}")
    return 0


def cmd_rq3(args) -> int:
    from hycan import v1_rq3

    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    rows = paper_rows(tree)
    eligible_all = {r["paper_id"] for r in rows if r["mode"] == "dual"} | {
        r["paper_id"] for r in rows if r["selection_route"] == "legacy_v0.1"
    }
    with (out / "material_identity_map.csv").open(
        newline="", encoding="utf-8"
    ) as fh:
        key_of = {r["material_identity"]: r["material_key"]
                  for r in csv.DictReader(fh)}
    values = v1_rq3.rq3_values(df, eligible_all, key_of)
    out.mkdir(parents=True, exist_ok=True)
    values.to_csv(out / "rq3_values.csv", index=False, lineterminator="\n")
    report = v1_rq3.fit_rq3(values)
    (out / "rq3.json").write_text(json.dumps(report, indent=2) + "\n",
                                  encoding="utf-8")
    for q, p in report["pooled"].items():
        if "skipped" in p:
            print(f"{q}: {p['skipped']}")
        else:
            print(f"{q}: {p['n_materials']} materials, df={p['df']}, "
                  f"CV {p['cv_pct']:.1f}% CI "
                  f"[{p['cv_ci95_pct'][0]:.1f}, {p['cv_ci95_pct'][1]:.1f}]")
    return 0


def cmd_rq4(args) -> int:
    from hycan import v1_rq4

    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    rows = paper_rows(tree)
    dual = {r["paper_id"] for r in rows if r["mode"] == "dual"}
    strata = {r["paper_id"]: r["stratum"] for r in rows if r["mode"] == "dual"}
    fc = json.loads(
        (ROOT / "references" / "v1_search" / "frame_counts.json").read_text())
    walk = json.loads(
        (ROOT / "references" / "v1_fulltext" / "walk.json").read_text())
    counts = {h: {"N": fc[f"frame_{h}"], "d": walk[h]["taken"]}
              for h in ("S1", "S2")}
    frame = v1_rq4.paper_items(df, dual)
    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out / "rq4_items.csv", index=False, lineterminator="\n")
    report = {"counts": counts, "items": v1_rq4.fit_rq4(frame, strata, counts)}
    (out / "rq4.json").write_text(json.dumps(report, indent=2) + "\n",
                                  encoding="utf-8")
    for item, r in report["items"].items():
        print(f"{item}: {r['n_yes']}/{r['n_domain']} p={r.get('p_hat', 0):.3f} "
              f"CI [{r['ci95'][0]:.3f}, {r['ci95'][1]:.3f}] ({r['ci_method']})")
    return 0


def cmd_rq5(args) -> int:
    from hycan import v1_rq5

    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    prows = paper_rows(tree)
    dual = {r["paper_id"] for r in prows if r["mode"] == "dual"}
    eligible_all = dual | {
        r["paper_id"] for r in prows if r["selection_route"] == "legacy_v0.1"
    }
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    for scope, papers in (("primary", dual),
                          ("all_eligible_papers", eligible_all)):
        rows = v1_rq5.rq5_rows(df, papers)
        x = v1_rq5.feature_matrix(rows)
        if scope == "primary":
            rows.to_csv(out / "rq5_rows.csv", index=False, lineterminator="\n")
        per_part, oof0 = [], None
        for r in range(v1_rq5.N_PARTITIONS):
            oof = v1_rq5.oof_predictions(rows, x, groups="paper_id",
                                         random_state=r, weighted=False)
            per_part.append(v1_rq5.score(oof))
            if r == 0:
                oof0 = oof
            print(f"{scope} partition {r} done", flush=True)
        rep = {
            "n_rows": len(rows), "n_papers": int(rows["paper_id"].nunique()),
            "by_paper": v1_rq5.summarize(per_part),
            "bootstrap_partition_0": v1_rq5.paper_bootstrap(
                oof0, n_boot=args.boot),
        }
        for name, kw in (("by_laboratory", {"groups": "lab_id",
                                            "weighted": False}),
                         ("row_weighted", {"groups": "paper_id",
                                           "weighted": True})):
            parts = [
                v1_rq5.score(v1_rq5.oof_predictions(
                    rows, x, random_state=r, **kw), weighted=kw["weighted"])
                for r in range(v1_rq5.N_PARTITIONS)
            ]
            rep[name] = v1_rq5.summarize(parts)
            print(f"{scope} {name} done", flush=True)
        report[scope] = rep
    (out / "rq5.json").write_text(json.dumps(report, indent=2) + "\n",
                                  encoding="utf-8")
    for scope, rep in report.items():
        for model in ("physical", "linear", "xgboost"):
            m = rep["by_paper"][model]["overall"]
            print(f"{scope} {model}: R2 {m['r2']['mean']:.3f} "
                  f"[{m['r2']['p2_5']:.3f}, {m['r2']['p97_5']:.3f}] "
                  f"MAE {m['mae']['mean']:.3f}")
    return 0


def cmd_rq1_mods(args) -> int:
    tree, out = Path(args.tree), Path(args.out)
    df = pd.read_csv(args.processed, low_memory=False)
    rows = paper_rows(tree)
    dual = {r["paper_id"] for r in rows if r["mode"] == "dual"}
    strata = {r["paper_id"]: r["stratum"] for r in rows if r["mode"] == "dual"}
    frame = v1_sets.moderator_frame(df, dual, strata)
    counts = frame.groupby("material_class")["paper_id"].nunique()
    small = set(counts[counts < 5].index)
    frame["material_class_m"] = frame["material_class"].map(
        lambda c: "other" if c in small else c)
    frame["stated01"] = frame["stated"].astype(float)
    frame["conv01"] = frame["conv_known"].astype(float)
    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out / "rq1_moderator_frame.csv", index=False,
                 lineterminator="\n")

    def ref(col: str) -> str:
        return str(frame[col].value_counts().idxmax())

    mods = {
        "method": (f"C(method, Treatment(reference='{ref('method')}'))",
                   ["method"]),
        "material_class": (
            f"C(material_class_m, Treatment(reference='{ref('material_class_m')}'))",
            ["material_class_m"]),
        "vmicro_frac": ("vmicro_frac", ["vmicro_frac"]),
        "year": ("year_c", ["year_c"]),
        "basis_stated": ("stated01", ["stated01"]),
        "convention_known": ("conv01", ["conv01"]),
        "stratum": ("C(stratum, Treatment(reference='S1'))", ["stratum"]),
        "reporting_score": ("reporting_score", ["reporting_score"]),
    }
    results = {"class_merge": {"merged_into_other": sorted(small),
                               "papers_per_class": {k: int(v)
                                                    for k, v in counts.items()}}}
    for name, (rhs, cols) in mods.items():
        results[name] = v1_rq1.fit_moderator(frame, rhs, cols)
        n = results[name].get("n_samples", 0)
        print(f"{name}: n={n}" if n else f"{name}: {results[name]}", flush=True)
    joint_rhs = " + ".join(rhs for rhs, _ in mods.values())
    joint_cols = sorted({c for _, cols in mods.values() for c in cols})
    results["joint_complete_cases"] = v1_rq1.fit_moderator(
        frame, joint_rhs, joint_cols)
    (out / "rq1_moderators.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8")
    j = results["joint_complete_cases"]
    print(f"joint: {j.get('n_samples', 0)} complete cases, "
          f"{j.get('n_papers', 0)} papers")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("rq1", "rq1-sens", "rq1-mods", "rq2", "rq3", "rq4", "rq5"):
        r = sub.add_parser(name)
        r.add_argument("--processed",
                       default=str(ROOT / "data" / "processed" /
                                   "measurements_v1.0_computed.csv"))
        r.add_argument("--tree", default=str(ROOT / "references" / "v1_extraction"))
        r.add_argument("--out", default=str(ROOT / "references" / "v1_analysis"))
        if name not in ("rq1-mods", "rq3", "rq4"):
            r.add_argument("--boot", type=int, default=v1_rq1.BOOT_N)
    args = ap.parse_args(argv)
    return {"rq1": cmd_rq1, "rq1-sens": cmd_rq1_sens, "rq1-mods": cmd_rq1_mods,
            "rq2": cmd_rq2, "rq3": cmd_rq3, "rq4": cmd_rq4,
            "rq5": cmd_rq5}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
