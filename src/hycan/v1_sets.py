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
) -> pd.DataFrame:
    """The contributing isotherms, one row each, with the §11.0 area and the
    measurement_id of the row at ``p_at_nmax_bar`` (``audit_mid``)."""
    iso = v1.isotherm_table(df)
    iso = iso[
        iso["nmax_status"].isin(list(statuses))
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
            if (w := v1.w1_wt_pct(r)) is not None
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
