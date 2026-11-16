"""Analysis-set construction for the v1.0 protocol (docs/v1_protocol.md §11.0,
RQ1). Built on the §3 isotherm machinery in :mod:`hycan.v1`.

The RQ1 primary set is one n_ex,max per sample (§11.0):

- contributing isotherms: coded 77 K ``basis_inferred = excess`` isotherms of
  probability-sample papers with ``nmax_status`` in {observed_max, plateau},
  ``basis_shape_conflict`` false, every usable point ``value_kind = measured``,
  and a §11.0-eligible BET area of at least 300 m² g⁻¹;
- per sample and laboratory, the geometric mean of its eligible isotherms'
  n_ex,max, with the count recorded;
- a sample measured by several laboratories within a paper enters once, at the
  median of the laboratory values, under the laboratory identifier
  ``<paper_id>-multilab``.

Keyword options carry the RQ1 sensitivity analyses that change the set;
``rq1_samples`` defaults are the primary analysis. (No row of the v1.0
dataset has ``duplicate_of`` set, so the §11.0 duplicate rule removes
nothing; ``eligible_isotherms`` refuses if one appears.)
"""

from __future__ import annotations

from statistics import geometric_mean, median

import pandas as pd

from . import v1

PRIMARY_STATUSES = ("observed_max", "plateau")


def _area_of(row: pd.Series) -> float | None:
    return v1.eligible_bet_area(row)


def eligible_isotherms(
    df: pd.DataFrame,
    papers: set[str],
    *,
    area_min: float | None = 300.0,
    statuses: tuple[str, ...] = PRIMARY_STATUSES,
    value_kinds: tuple[str, ...] = ("measured",),
    stated_only: bool = False,
    stated_lower_bound: bool = False,
    unknown_as_w2: bool = False,
) -> pd.DataFrame:
    """The contributing isotherms, one row each, with the §11.0 area and the
    measurement_id of the row at ``p_at_nmax_bar`` (``audit_mid``).

    ``stated_only`` keeps stated-excess isotherms only (RQ1 sensitivity (i));
    ``stated_lower_bound`` adds stated-excess ``lower_bound`` isotherms
    (sensitivity (ii)); ``unknown_as_w2`` converts unknown-convention wt% as
    W2 (sensitivity (vii))."""
    iso = v1.isotherm_table(df, unknown_as_w2=unknown_as_w2)
    stated = iso["basis_stated"].map(lambda x: bool(v1.as_bool(x)))
    keep = iso["nmax_status"].isin(list(statuses))
    if stated_lower_bound:
        keep |= (iso["nmax_status"] == "lower_bound") & stated
    if stated_only:
        keep &= stated
    iso = iso[
        keep
        & ~iso["basis_shape_conflict"].astype(bool)
        & iso["paper_id"].isin(sorted(papers))
    ]
    allowed = set(value_kinds)
    iso = iso[iso["value_kinds"].map(
        lambda s: set(str(s).split(";")) <= allowed if str(s) else False
    )]
    keys = df.apply(v1.isotherm_key, axis=1)
    out = []
    for _, e in iso.iterrows():
        g = df[keys == e["isotherm_key"]]
        use = g[g.apply(v1._usable_point_row, axis=1)]
        import math

        cands = [
            r for _, r in use.iterrows()
            if (w := v1.w1_wt_pct(r, unknown_as_w2)) is not None
            and math.isclose(float(r["pressure_bar"]), e["p_at_nmax_bar"],
                             rel_tol=0.0, abs_tol=1e-12)
            and math.isclose(w, e["n_ex_max_wt_pct"], rel_tol=1e-12)
        ]
        if not cands:
            raise ValueError(f"no row at p_at_nmax for {e['isotherm_key']}")
        row = max(cands, key=lambda r: r["measurement_id"])
        if v1.as_str(row.get("duplicate_of")):
            raise ValueError(
                f"{row['measurement_id']} has duplicate_of set; apply §11.0 by hand"
            )
        area = _area_of(row)
        if area_min is not None and (area is None or area < area_min):
            continue
        rec = e.to_dict()
        rec["a_bet_m2_g"] = area
        rec["audit_mid"] = row["measurement_id"]
        out.append(rec)
    return pd.DataFrame(out)


def rq1_samples(
    df: pd.DataFrame,
    papers: set[str],
    **options,
) -> pd.DataFrame:
    """One analysis unit per sample (§11.0): columns ``paper_id``,
    ``sample_id``, ``lab_id``, ``n_isotherms``, ``n_labs``,
    ``n_ex_max_w1_wt_pct``, ``a_bet_m2_g``."""
    iso = eligible_isotherms(df, papers, **options)
    if iso.empty:
        return pd.DataFrame(columns=[
            "paper_id", "sample_id", "lab_id", "n_isotherms", "n_labs",
            "n_ex_max_w1_wt_pct", "a_bet_m2_g",
        ])
    per_lab = []
    for (pid, sid, lab), g in iso.groupby(
        ["paper_id", "sample_id", "measuring_lab_id"], dropna=False, sort=True
    ):
        areas = sorted(set(g["a_bet_m2_g"]))
        if len(areas) != 1:
            raise ValueError(f"{pid} {sid}: isotherms carry different areas {areas}")
        per_lab.append({
            "paper_id": pid, "sample_id": sid, "lab_id": lab,
            "n_isotherms": len(g),
            "value": geometric_mean(g["n_ex_max_wt_pct"]),
            "a_bet_m2_g": areas[0],
        })
    out = []
    frame = pd.DataFrame(per_lab)
    for (pid, sid), g in frame.groupby(["paper_id", "sample_id"], sort=True):
        if len(g) == 1:
            r = g.iloc[0]
            out.append({
                "paper_id": pid, "sample_id": sid, "lab_id": r["lab_id"],
                "n_isotherms": int(r["n_isotherms"]), "n_labs": 1,
                "n_ex_max_w1_wt_pct": r["value"], "a_bet_m2_g": r["a_bet_m2_g"],
            })
        else:
            areas = sorted(set(g["a_bet_m2_g"]))
            if len(areas) != 1:
                raise ValueError(f"{pid} {sid}: laboratories carry different areas")
            out.append({
                "paper_id": pid, "sample_id": sid, "lab_id": f"{pid}-multilab",
                "n_isotherms": int(g["n_isotherms"].sum()), "n_labs": len(g),
                "n_ex_max_w1_wt_pct": median(g["value"]),
                "a_bet_m2_g": areas[0],
            })
    return pd.DataFrame(out)


def moderator_frame(
    df: pd.DataFrame, papers: set[str], strata: dict[str, str], **options
) -> pd.DataFrame:
    """The RQ1 samples with the §11 moderator columns, one row per sample.

    Moderators come from the sample's contributing isotherms and their rows at
    ``p_at_nmax_bar`` (``audit_mid``): ``method`` is the rows' measurement
    method, or ``mixed``; ``material_class`` must be unique; ``vmicro_frac``
    is the mean of the distinct row values of V_micro/V_total where both come
    from an N₂ isotherm (``pore_volume_probe_gas = N2``, strictly — §11's
    "both from the N₂ isotherm"); ``year_c`` is the paper year minus 2010;
    ``stated`` is
    True when every contributing isotherm is stated excess; ``conv_known`` is
    True when every contributing row's ``wt_pct_convention_source`` is not
    ``none``; ``stratum`` is the paper's §7 stratum; ``reporting_score`` is
    the mean over contributing rows.
    """
    iso = eligible_isotherms(df, papers, **options)
    samples = rq1_samples(df, papers, **options)
    byid = df.set_index("measurement_id")
    out = []
    for (pid, sid), g in iso.groupby(["paper_id", "sample_id"], sort=True):
        rows = byid.loc[list(g["audit_mid"])]
        methods = {v1.as_str(m) or "unknown" for m in rows["measurement_method"]}
        classes = {v1.as_str(c) for c in rows["material_class"]}
        if len(classes) != 1:
            raise ValueError(f"{pid} {sid}: mixed material_class {sorted(classes)}")
        fracs = []
        for _, r in rows.iterrows():
            vm, vt = v1.as_float(r["micropore_volume_cm3_g"]), v1.as_float(
                r["total_pore_volume_cm3_g"])
            if (v1.as_str(r["pore_volume_probe_gas"]) == "N2"
                    and vm is not None and vt is not None and vt > 0):
                fracs.append(vm / vt)
        years = {v1.as_float(y) for y in rows["year"]}
        scores = [v1.as_float(s) for s in rows["reporting_score"]]
        out.append({
            "paper_id": pid, "sample_id": sid,
            "method": methods.pop() if len(methods) == 1 else "mixed",
            "material_class": classes.pop(),
            "vmicro_frac": sum(set(fracs)) / len(set(fracs)) if fracs else None,
            "year_c": (years.pop() - 2010.0) if len(years) == 1 else None,
            "stated": bool(g["basis_stated"].map(
                lambda x: bool(v1.as_bool(x))).all()),
            "conv_known": bool(all(
                v1.as_str(s) not in (None, "none")
                for s in rows["wt_pct_convention_source"])),
            "stratum": strata.get(pid),
            "reporting_score": (sum(s for s in scores if s is not None)
                                / len(scores)) if scores else None,
        })
    return samples.merge(pd.DataFrame(out), on=["paper_id", "sample_id"],
                         how="left", validate="one_to_one")
