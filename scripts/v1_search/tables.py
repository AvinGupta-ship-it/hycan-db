"""The v1.0 manuscript tables (protocol §14), generated from committed
artifacts only. Writes ``manuscript/v1/tables.md``; the manuscript cites
these tables rather than hand-typing counts.

    python3 scripts/v1_search/tables.py [--out manuscript/v1/tables.md]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ANA = ROOT / "references" / "v1_analysis"


def j(path: Path) -> dict:
    return json.loads(path.read_text())


def fr(x: float, nd: int = 3) -> str:
    return f"{x:.{nd}f}"


def ci(pair, nd: int = 3) -> str:
    return f"[{pair[0]:.{nd}f}, {pair[1]:.{nd}f}]"


def t_prisma(out: list[str]) -> None:
    p = j(ROOT / "references" / "v1_prisma" / "prisma_counts.json")
    out.append("## Table 1 — study flow (PRISMA 2020 counts)\n")
    out.append("| Stage | Count |")
    out.append("|---|---|")
    ident = p["identification"]
    out.append(f"| Records from OpenAlex | {ident['openalex']['records']} |")
    out.append(f"| Records from Semantic Scholar | "
               f"{ident['semantic_scholar']['records']} |")
    out.append(f"| Duplicates removed at merge | "
               f"{ident['duplicates_removed']['total']} |")
    out.append(f"| Merged unique records | {ident['merged']} |")
    scr = p["screening"]
    out.append(f"| Excluded by double title/abstract screen | "
               f"{scr['excluded_by_both']['total']} |")
    out.append(f"| Sampling frame | {scr['frame']['total']} "
               f"(S1 {scr['frame']['S1']}, S2 {scr['frame']['S2']}) |")
    w = p["walk"]
    for h in ("S1", "S2"):
        out.append(
            f"| {h}: drawn / not retrieved / duplicate / assessed / "
            f"ineligible / eligible | {w['drawn'][h]} / "
            f"{w['not_retrieved'][h]} / {w['frame_duplicate'][h]} / "
            f"{w['assessed'][h]} / {w['excluded'][h]} / {w['eligible'][h]} |")
    r = p["author_review"]
    out.append(f"| Author's review of full-text exclusions (§6) | "
               f"{r['reviewed']} reviewed, {r['confirmed']} confirmed, "
               f"{r['reversed']} reversed |")
    v = p["v01_papers"]
    out.append(
        f"| v0.1 corpus (other methods) | {v['papers']}: {v['drawn']} drawn "
        f"({v['drawn_eligible']} eligible), {v['eligible']} eligible not "
        f"drawn, {v['excluded']} excluded, "
        f"{len(v['not_retrieved'])} not retrieved |")
    a = p["analysed"]
    out.append(
        f"| Analysed | RQ1 {a['rq1_primary']['papers']} papers / "
        f"{a['rq1_primary']['samples']} samples; RQ2 "
        f"{a['rq2_primary']['papers']} papers / {a['rq2_primary']['samples']} "
        f"samples; RQ3 {a['rq3']['materials_with_2plus_labs']} materials; "
        f"RQ4 {a['rq4']['papers']} papers; RQ5 {a['rq5_primary']['papers']} "
        f"papers / {a['rq5_primary']['rows']} rows |")
    out.append("")


def t_dataset(out: list[str]) -> None:
    df = pd.read_csv(ROOT / "data" / "processed" /
                     "measurements_v1.0_computed.csv", low_memory=False)
    with (ROOT / "references" / "v1_extraction" / "papers.csv").open(
        newline="", encoding="utf-8"
    ) as fh:
        papers = list(csv.DictReader(fh))
    modes = {}
    for r in papers:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    tiers = df["reporting_tier"].value_counts().to_dict()
    out.append("## Table 2 — the v1.0 dataset\n")
    out.append("| Property | Value |")
    out.append("|---|---|")
    out.append(f"| Rows | {len(df)} |")
    out.append(f"| Papers with rows | {df['paper_id'].nunique()} |")
    out.append(f"| Papers by extraction mode | "
               f"{', '.join(f'{k} {v}' for k, v in sorted(modes.items()))} |")
    out.append(f"| Samples | {df.groupby(['paper_id', 'sample_id']).ngroups} |")
    out.append(f"| Measuring laboratories | {df['measuring_lab_id'].nunique()} |")
    out.append(f"| Publication years | {int(df['year'].min())}"
               f"–{int(df['year'].max())} |")
    out.append(f"| Reporting tiers | "
               f"{', '.join(f'{k} {tiers.get(k, 0)}' for k in 'ABCD')} |")
    out.append(f"| Rows flagged by the §10.2 screen | "
               f"{int((df['plausibility_flag'] == True).sum())} |")  # noqa: E712
    out.append("")


def t_agreement(out: list[str]) -> None:
    dual = j(ROOT / "references" / "v1_extraction" / "agreement_dual.json")["summary"]
    out.append("## Table 3 — independent-extraction agreement (dual-mode papers)\n")
    out.append("| Quantity | Value |")
    out.append("|---|---|")
    out.append(f"| Papers | {dual['papers']} |")
    out.append(f"| Matched row pairs | {dual['matched_pairs']} |")
    out.append(f"| Row-detection agreement | {fr(dual['row_detection_agreement'])} |")
    u = dual["numeric"]["uptake_wt_pct"]
    out.append(f"| Uptake (wt%) within tolerance | "
               f"{fr(u['share_within_tolerance'])} of {u['n_both_present']} |")
    b = dual["numeric"]["bet_surface_area_m2_g"]
    out.append(f"| BET area within tolerance | "
               f"{fr(b['share_within_tolerance'])} of {b['n_both_present']} |")
    t = dual["numeric"]["temperature_k"]
    p = dual["numeric"]["pressure_bar"]
    out.append(f"| Temperature within tolerance | "
               f"{fr(t['share_within_tolerance'])} of {t['n_both_present']} |")
    out.append(f"| Pressure within tolerance | "
               f"{fr(p['share_within_tolerance'])} of {p['n_both_present']} |")
    bi = dual["categorical"]["basis_inferred"]
    bs = dual["categorical"]["basis_stated"]
    out.append(f"| basis_stated agreement (kappa) | "
               f"{fr(bs['exact_agreement'])} ({fr(bs['kappa'])}) |")
    out.append(f"| basis_inferred agreement (kappa) | "
               f"{fr(bi['exact_agreement'])} ({fr(bi['kappa'])}) |")
    cm = dual["curve_sample_mapping"]
    out.append(f"| Curve-to-sample mapping agreement | "
               f"{fr(cm['agreement'])} of {cm['curves']} curves |")
    out.append("")


def t_audit(out: list[str]) -> None:
    score = j(ROOT / "references" / "v1_audit" / "score.json")
    out.append("## Table 4 — the §12 author audit (deviation D1 format)\n")
    out.append("| Audit stratum | Rows with an error | 95% CI |")
    out.append("|---|---|---|")
    for s in ("a", "b", "c"):
        st = score["strata"][s]
        out.append(f"| {s} | {st['row_errors']}/{st['n']} | "
                   f"{ci(st['ci95'])} |")
    out.append(f"| overall (weighted) | "
               f"{fr(score['overall']['weighted_row_error_rate'], 4)} | — |")
    out.append("")


def t_rq1(out: list[str]) -> None:
    rq1 = j(ANA / "rq1.json")
    p, s = rq1["primary"], rq1["secondary"]
    out.append("## Table 5 — RQ1: the Chahine rule at n_ex,max\n")
    out.append("| Quantity | Value |")
    out.append("|---|---|")
    out.append(f"| Samples / papers / laboratories | "
               f"{p['n_samples']} / {p['n_papers']} / {p['n_labs']} |")
    out.append(f"| Geometric-mean ratio to A_BET/500 | {fr(p['ratio'])} |")
    out.append(f"| 95% CI (t, L−1 df) | {ci(p['ci95_t'])} |")
    out.append(f"| 95% CI (laboratory bootstrap) | {ci(p['ci95_bootstrap'])} |")
    out.append(f"| Decision against [1/1.15, 1.15] | **{p['decision']}** |")
    out.append(f"| 95% prediction interval (new sample, new laboratory) | "
               f"{ci(p['prediction_interval_95'])} |")
    v = p["variances"]
    out.append(f"| Variance components (lab / paper / sample, ln scale) | "
               f"{fr(v['laboratory'], 4)} / {fr(v['paper'], 6)} / "
               f"{fr(v['sample'], 4)} |")
    out.append(f"| Secondary ln–ln slope b | {fr(s['b'])} {ci(s['ci95'])} |")
    out.append(f"| b corrected for 10% / 20% area error | "
               f"{fr(s['b_corrected_10pct'])} / {fr(s['b_corrected_20pct'])} |")
    lad = rq1["exclusion_ladder"]
    steps = " → ".join(f"{k} {v['isotherms']}" for k, v in lad.items())
    out.append(f"| Exclusion ladder (isotherms) | {steps} |")
    q = rq1["p_at_nmax_bar"]
    out.append(f"| p at n_ex,max (bar): quartiles, range, outside 10–60 | "
               f"{fr(q['quartiles'][0], 1)}/{fr(q['quartiles'][1], 1)}/"
               f"{fr(q['quartiles'][2], 1)}, {fr(q['min'], 1)}–{fr(q['max'], 1)}, "
               f"{len(q['outside_10_60_bar'])} of {q['n']} |")
    out.append("")


def t_rq1_sens(out: list[str]) -> None:
    sens = j(ANA / "rq1_sensitivity.json")
    out.append("## Table 6 — RQ1 sensitivity analyses\n")
    out.append("| Variant | n | Ratio | Decision 95% CI | Decision |")
    out.append("|---|---|---|---|---|")
    for key, v in sens.items():
        if "ratio" in v and "ci95_decision" in v:
            out.append(f"| {key.replace('_', ' ')} | {v['n_samples']} | "
                       f"{fr(v['ratio'])} | {ci(v['ci95_decision'])} | "
                       f"{v['decision']} |")
        elif "ratio" in v:  # design-weighted: bootstrap CI only
            out.append(f"| {key.replace('_', ' ')} | {v['n_samples']} | "
                       f"{fr(v['ratio'])} | {ci(v['ci95_bootstrap'])} | "
                       f"{v['decision']} |")
    lolo = sens["xi_leave_one_laboratory_out"]
    out.append(f"| xi leave-one-laboratory-out | {lolo['n_labs']} labs | "
               f"range {fr(lolo['min']['ratio'])}–{fr(lolo['max']['ratio'])} "
               f"| — | — |")
    v01 = sens["xiii_v01_specification"]
    out.append(f"| xiii v0.1 specification (wt% per 500 m² g⁻¹) | "
               f"{v01['n_obs']} rows | {fr(v01['wt_pct_per_500_m2'])} | "
               f"{ci(v01['wt_pct_per_500_m2_ci95'])} | outside ±15% |")
    out.append("")


def t_rq1_mods(out: list[str]) -> None:
    mods = j(ANA / "rq1_moderators.json")
    out.append("## Table 7 — RQ1 moderators (exploratory)\n")
    out.append("| Moderator | n | Term | Estimate (ln scale) | 95% CI |")
    out.append("|---|---|---|---|---|")
    for name, m in mods.items():
        if name == "class_merge" or "terms" not in m:
            continue
        for term, t in m["terms"].items():
            if term == "Intercept":
                continue
            short = term
            if "[T." in term:
                short = term.split("[T.")[-1].rstrip("]")
            out.append(f"| {name.replace('_', ' ')} | {m['n_samples']} | "
                       f"{short} | {fr(t['estimate'])} | {ci(t['ci95'])} |")
    out.append("")
    merged = mods["class_merge"]["merged_into_other"]
    out.append(f"Classes merged into `other` (fewer than 5 papers): "
               f"{', '.join(merged)}.\n")


def t_rq2(out: list[str]) -> None:
    rq2 = j(ANA / "rq2.json")
    out.append("## Table 8 — RQ2: the rule at 0.9–1.2 bar\n")
    out.append("| Scope | Model | n | Estimate | 95% CI |")
    out.append("|---|---|---|---|---|")
    for scope in ("primary", "all_eligible_papers"):
        r = rq2[scope]
        a = r["a_bet"]
        out.append(f"| {scope.replace('_', ' ')} | (a) b on ln A_BET | "
                   f"{a['n_samples']} | "
                   f"{fr(a['terms']['b_ln_a_bet']['estimate'])} | "
                   f"{ci(a['terms']['b_ln_a_bet']['ci95'])} |")
        bn = r["b_vmicro_n2"]
        if "terms" in bn:
            out.append(f"| {scope.replace('_', ' ')} | (b) b on ln V_micro(N₂) | "
                       f"{bn['n_samples']} | "
                       f"{fr(bn['terms']['b_ln_vmicro']['estimate'])} | "
                       f"{ci(bn['terms']['b_ln_vmicro']['ci95'])} |")
        bc = r["b_vmicro_co2"]
        if "terms" in bc:
            out.append(f"| {scope.replace('_', ' ')} | (b) b on ln V_micro(CO₂) | "
                       f"{bc['n_samples']} | "
                       f"{fr(bc['terms']['b_ln_vmicro']['estimate'])} | "
                       f"{ci(bc['terms']['b_ln_vmicro']['ci95'])} |")
        else:
            out.append(f"| {scope.replace('_', ' ')} | (b) b on ln V_micro(CO₂) "
                       f"| — | {bc['skipped']} | — |")
        c = r["c_one_bar_ratio"]
        out.append(f"| {scope.replace('_', ' ')} | (c) 1-bar ratio to A_BET/500 "
                   f"| {c['n_samples']} | {fr(c['ratio'])} | "
                   f"{ci(c['ci95_decision'])} |")
        comp = r["comparison_same_samples"]
        if "ml_aic" in comp:
            out.append(f"| {scope.replace('_', ' ')} | ML AIC, A_BET vs "
                       f"V_micro(N₂), same {comp['n_samples']} samples | "
                       f"{comp['n_samples']} | "
                       f"{fr(comp['ml_aic']['a_bet'], 1)} vs "
                       f"{fr(comp['ml_aic']['b_vmicro_n2'], 1)} | — |")
    out.append("")


def t_rq3(out: list[str]) -> None:
    rq3 = j(ANA / "rq3.json")
    out.append("## Table 9 — RQ3: interlaboratory CVs (log scale, ≈ %)\n")
    out.append("| Material | A_BET | n_ex,max | n at 1 bar | ratio |")
    out.append("|---|---|---|---|---|")

    def cell(m, q):
        v = rq3["materials"].get(m, {}).get(q)
        if not v:
            return "—"
        return (f"{v['cv_pct']:.1f} ({v['n_labs']}L) "
                f"[{v['cv_ci95_pct'][0]:.1f}, {v['cv_ci95_pct'][1]:.1f}]")

    for m in sorted(rq3["materials"]):
        out.append(f"| {m} | {cell(m, 'a_bet')} | {cell(m, 'n_ex_max')} | "
                   f"{cell(m, 'n_1bar')} | {cell(m, 'ratio')} |")
    pooled = rq3["pooled"]

    def pcell(q):
        v = pooled[q]
        if "skipped" in v:
            return v["skipped"]
        return (f"{v['cv_pct']:.1f} (df {v['df']}) "
                f"[{v['cv_ci95_pct'][0]:.1f}, {v['cv_ci95_pct'][1]:.1f}]")

    out.append(f"| **pooled** | {pcell('a_bet')} | {pcell('n_ex_max')} | "
               f"{pcell('n_1bar')} | {pcell('ratio')} |")
    out.append("")


def t_rq4(out: list[str]) -> None:
    rq4 = j(ANA / "rq4.json")["items"]
    names = {
        "a": "uptake basis stated for every value",
        "b": "wt% convention explicitly stated",
        "c": "numerical uncertainty or replicates",
        "d": "instrument and calibration (§10.1 item 7)",
        "e": "BET P/P₀ range or consistency criteria",
        "f": "sample mass for the H₂ measurement",
        "g": "degassing conditions",
        "h": "≥ 1 row flagged by the §10.2 screen",
        "i": "H₂ purity",
        "j": "free-volume calibration gas and temperature",
    }
    out.append("## Table 10 — RQ4: reporting practice "
               "(§7 design-weighted shares)\n")
    out.append("| Item | Yes/domain | Weighted share | 95% CI | "
               "≤2015 | ≥2016 |")
    out.append("|---|---|---|---|---|---|")
    for k, label in names.items():
        r = rq4[k]
        per = r["by_period"]

        def ps(d):
            return fr(d["p_hat"], 2) if "p_hat" in d else "—"

        out.append(f"| ({k}) {label} | {r['n_yes']}/{r['n_domain']} | "
                   f"{fr(r['p_hat'], 3)} | {ci(r['ci95'])} | "
                   f"{ps(per['le_2015'])} | {ps(per['ge_2016'])} |")
    out.append("")


def t_rq5(out: list[str]) -> None:
    rq5 = j(ANA / "rq5.json")
    out.append("## Table 11 — RQ5: prediction baselines "
               "(pooled out-of-fold R², mean over 20 partitions)\n")
    out.append("| Scope | Model | Overall | ≤1.2 bar | ≥10 bar | "
               "Overall MAE (wt%) |")
    out.append("|---|---|---|---|---|---|")
    for scope in ("primary", "all_eligible_papers"):
        r = rq5[scope]["by_paper"]
        for m in ("physical", "linear", "xgboost"):
            row = r[m]

            def rr(reg):
                s = row[reg]["r2"]
                return f"{s['mean']:.3f} [{s['p2_5']:.3f}, {s['p97_5']:.3f}]"

            out.append(f"| {scope.replace('_', ' ')} | {m} | {rr('overall')} | "
                       f"{rr('le_1p2_bar')} | {rr('ge_10_bar')} | "
                       f"{row['overall']['mae']['mean']:.3f} |")
    p = rq5["primary"]
    out.append("")
    out.append(
        f"Primary scope: {p['n_rows']} rows, {p['n_papers']} papers. "
        f"By-laboratory grouping and 1/(rows per paper) weighting give the "
        f"same ordering (rq5.json). Paper-bootstrap 95% CIs on partition 0: "
        + "; ".join(
            f"{m} overall R² "
            f"{ci(p['bootstrap_partition_0'][m]['overall']['r2_ci95'])}"
            for m in ("physical", "linear", "xgboost")) + ".\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "manuscript" / "v1" /
                                         "tables.md"))
    args = ap.parse_args(argv)
    out: list[str] = [
        "# HyCAN-DB v1.0 — generated tables",
        "",
        "Generated by `scripts/v1_search/tables.py` from the committed",
        "analysis outputs; regenerate rather than edit. Every count in the",
        "manuscript traces to a cell here or to the named JSON.",
        "",
    ]
    for fn in (t_prisma, t_dataset, t_agreement, t_audit, t_rq1, t_rq1_sens,
               t_rq1_mods, t_rq2, t_rq3, t_rq4, t_rq5):
        fn(out)
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {path} ({len(out)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
