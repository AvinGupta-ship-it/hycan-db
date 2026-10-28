"""Computed fields of the v1.0 protocol (docs/v1_protocol.md §3, §10, §11.0).

The protocol governs. Where this module and the protocol differ, the protocol
is right and this module is corrected (protocol Appendix A).

Fields computed here are never entered by an extractor:

- ``w1_wt_pct``: the uptake in the W1 convention used by every analysis (§3);
- ``nmax_status``, ``n_ex_max_wt_pct``, ``p_at_nmax_bar``, ``p_last_bar``:
  the maximum excess of a 77 K excess isotherm (§3);
- ``basis_shape_conflict`` (§3);
- ``reporting_score`` and ``reporting_tier`` (§10.1);
- ``eligible_bet_area_m2_g``: a BET area that passes the §11.0 area rule;
- ``plausibility_flag`` (§10.2).

A row counts as coded under schema v2 once ``basis_stated`` is not null (data
dictionary, "Schema v2 Fields"). Computed fields are produced only for coded
rows; an uncoded row gets null, never a value that looks coded.

Choices the protocol leaves to the implementation, each stated where it is made:

- Several points at one pressure are averaged when a value at that pressure is
  needed (the value at p_last, or the interpolation at 0.7 * p_last).
- When the highest value occurs more than once, the last occurrence (highest
  pressure) is the maximum. "Followed by a lower point" is judged after it, and
  its pressure is ``p_at_nmax_bar``.
- A test that needs the value at 0.7 * p_last cannot be evaluated when
  0.7 * p_last is below the isotherm's first pressure, because the protocol
  allows interpolation, not extrapolation. Such an isotherm is not a plateau
  and has no basis-shape conflict.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd

from hycan.normalize import ml_stp_per_g_to_wt_pct, mmol_per_g_to_wt_pct

# --- §3 ---------------------------------------------------------------------

T77_MIN_K = 76.0
T77_MAX_K = 79.0
OBSERVED_MAX_MIN_P_LAST_BAR = 10.0
PLATEAU_MIN_P_LAST_BAR = 20.0
LOWER_BOUND_MIN_P_LAST_BAR = 20.0
CONFLICT_MIN_P_LAST_BAR = 60.0
DROP_MIN_RELATIVE = 0.01
RISE_LIMIT_RELATIVE = 0.03
INTERP_FRACTION = 0.7

NMAX_STATUSES = ("observed_max", "plateau", "lower_bound", "none")

# --- §10.1 ------------------------------------------------------------------

NAMED_AREA_METHODS = frozenset(
    {"BET", "Langmuir", "DFT", "alpha_s_plot", "t_plot", "geometric"}
)
STATED_PROBE_GASES = frozenset({"N2", "Ar", "CO2", "other"})
MIN_ISOTHERM_POINTS = 5
TIER_THRESHOLDS = (("A", 8), ("B", 6), ("C", 4), ("D", 0))
# Booleans the score reads. On a coded row each must be coded; a null one
# means the extraction is incomplete, and the score is withheld rather than
# guessed.
SCORE_REQUIRED_BOOLEANS = (
    "basis_stated",
    "temperature_inferred",
    "instrument_identified",
    "calibration_described",
    "replicates_reported",
)

# --- §11.0 and §10.2 --------------------------------------------------------

AREA_PROBE_GASES = frozenset({"N2", "Ar", "unspecified"})
SCREEN_RT_MIN_K = 273.0
SCREEN_RT_MAX_K = 303.0
SCREEN_RT_MAX_P_BAR = 100.0
SCREEN_RT_LIMIT_WT_PCT = 1.5
SCREEN_77K_CAP_WT_PCT = 10.0
SCREEN_77K_AREA_FACTOR = 2.0
SCREEN_77K_OFFSET_WT_PCT = 0.5
CHAHINE_AREA_PER_WT_PCT = 500.0


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _missing(x: object) -> bool:
    if x is None:
        return True
    if isinstance(x, float) and math.isnan(x):
        return True
    return isinstance(x, str) and x.strip() == ""


def as_bool(x: object) -> bool | None:
    """Read a boolean cell: CSV round-trips booleans as "True"/"False"."""
    if _missing(x):
        return None
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, str):
        s = x.strip().lower()
        if s == "true":
            return True
        if s == "false":
            return False
    raise ValueError(f"not a boolean: {x!r}")


def as_float(x: object) -> float | None:
    if _missing(x):
        return None
    return float(x)


def as_str(x: object) -> str | None:
    if _missing(x):
        return None
    return str(x).strip()


def is_coded(row: dict | pd.Series) -> bool:
    """A row is coded under schema v2 once basis_stated is not null."""
    return as_bool(row.get("basis_stated")) is not None


def is_77k(temperature_k: object) -> bool:
    """§3: a stated 76.0-79.0 K, or "liquid nitrogen" stored as 77.3 K."""
    t = as_float(temperature_k)
    return t is not None and T77_MIN_K <= t <= T77_MAX_K


# ---------------------------------------------------------------------------
# §3 wt% convention
# ---------------------------------------------------------------------------


def w2_to_w1(w2: float) -> float:
    """W1 = W2 / (1 - W2/100)."""
    if not 0 <= w2 < 100:
        raise ValueError(f"W2 must lie in [0, 100): {w2}")
    return w2 / (1.0 - w2 / 100.0)


def w1_to_w2(w1: float) -> float:
    """W2 = W1 / (1 + W1/100), the inverse of w2_to_w1."""
    if w1 < 0:
        raise ValueError(f"W1 must be non-negative: {w1}")
    return w1 / (1.0 + w1 / 100.0)


def w1_wt_pct(row: dict | pd.Series, unknown_as_w2: bool = False) -> float | None:
    """The uptake in W1 wt% (§3, §11.0).

    A value in mmol/g, then one in mL(STP)/g, is converted and takes precedence
    over the paper's wt%. Otherwise a W2 value is converted, and a W1 or
    unknown-convention value is used as reported. ``unknown_as_w2`` is RQ1
    sensitivity (vii), which treats every unknown-convention wt% as W2.
    """
    mmol = as_float(row.get("uptake_mmol_g"))
    if mmol is not None:
        return mmol_per_g_to_wt_pct(mmol)
    ml = as_float(row.get("uptake_ml_stp_g"))
    if ml is not None:
        return ml_stp_per_g_to_wt_pct(ml)
    wt = as_float(row.get("uptake_wt_pct"))
    if wt is None:
        return None
    convention = as_str(row.get("wt_pct_convention"))
    if convention == "W2" or (unknown_as_w2 and convention in (None, "unknown")):
        return w2_to_w1(wt)
    return wt


def half_unit(printed: str) -> float:
    """Half a unit in the last printed digit: "5.5" -> 0.05, "12" -> 0.5."""
    s = printed.strip()
    if "e" in s.lower():
        raise ValueError(f"exponent notation is not a printed rounding: {printed!r}")
    decimals = len(s.split(".", 1)[1]) if "." in s else 0
    return 0.5 * 10.0 ** (-decimals)


def convention_from_pair(
    wt_printed: str,
    other_printed: str,
    other_unit: str,
) -> str:
    """Which wt% convention a paired value supports, within printed rounding.

    ``other_unit`` is "mmol_g", "mg_g" or "ml_stp_g". Returns "W1" or "W2" when
    exactly one convention matches (§3 ``inferred_from_paired_units``),
    "ambiguous" when both match, and "inconsistent" when neither does (a §3
    unit-consistency failure).
    """
    factor = {
        "mmol_g": mmol_per_g_to_wt_pct(1.0),
        "mg_g": 0.1,
        "ml_stp_g": ml_stp_per_g_to_wt_pct(1.0),
    }[other_unit]
    wt = float(wt_printed)
    other = float(other_printed)
    w1 = other * factor
    tol_wt = half_unit(wt_printed)
    tol_w1 = half_unit(other_printed) * factor
    # A W2 bound inherits the W1 rounding through dW2/dW1 = 1/(1 + W1/100)^2 < 1,
    # so the W1 tolerance is a safe bound for it.
    matches_w1 = abs(wt - w1) <= tol_wt + tol_w1
    matches_w2 = abs(wt - w1_to_w2(w1)) <= tol_wt + tol_w1
    if matches_w1 and matches_w2:
        return "ambiguous"
    if matches_w1:
        return "W1"
    if matches_w2:
        return "W2"
    return "inconsistent"


# ---------------------------------------------------------------------------
# §3 maximum excess
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Point:
    pressure_bar: float
    value_wt_pct: float
    uncertainty_wt_pct: float = 0.0


@dataclass(frozen=True)
class NmaxResult:
    nmax_status: str
    n_ex_max_wt_pct: float | None
    p_at_nmax_bar: float | None
    p_last_bar: float | None
    rise_last_vs_07_relative: float | None


def _collapse(points: Sequence[Point]) -> tuple[np.ndarray, np.ndarray]:
    """Unique pressures, ascending, with the mean value at each."""
    by_p: dict[float, list[float]] = {}
    for pt in points:
        by_p.setdefault(pt.pressure_bar, []).append(pt.value_wt_pct)
    ps = np.array(sorted(by_p))
    vs = np.array([float(np.mean(by_p[p])) for p in ps])
    return ps, vs


def value_at(points: Sequence[Point], pressure_bar: float) -> float | None:
    """Linear interpolation within the isotherm's range; None outside it."""
    ps, vs = _collapse(points)
    if pressure_bar < ps[0] or pressure_bar > ps[-1]:
        return None
    return float(np.interp(pressure_bar, ps, vs))


def rise_last_vs_07(points: Sequence[Point]) -> float | None:
    """(value at p_last) / (value at 0.7 * p_last) - 1, or None if unevaluable."""
    ps, vs = _collapse(points)
    p_last = float(ps[-1])
    v_last = float(vs[-1])
    v_07 = value_at(points, INTERP_FRACTION * p_last)
    if v_07 is None or v_07 <= 0:
        return None
    return v_last / v_07 - 1.0


def nmax(points: Iterable[Point]) -> NmaxResult:
    """Classify one isotherm's maximum excess (§3).

    ``points`` are the isotherm's adsorption points: one sample, 77 K,
    ``basis_inferred = excess``, uptake in W1 wt%. The caller selects them.
    """
    pts = [
        p for p in points if p.pressure_bar is not None and p.value_wt_pct is not None
    ]
    if not pts:
        return NmaxResult("none", None, None, None, None)
    pts.sort(key=lambda p: p.pressure_bar)
    p_last = pts[-1].pressure_bar
    top = max(p.value_wt_pct for p in pts)
    i_top = max(i for i, p in enumerate(pts) if p.value_wt_pct == top)
    peak = pts[i_top]
    threshold = max(DROP_MIN_RELATIVE * top, peak.uncertainty_wt_pct)
    dropped = any(
        p.pressure_bar > peak.pressure_bar and top - p.value_wt_pct > threshold
        for p in pts[i_top + 1 :]
    )
    rise = rise_last_vs_07(pts)
    if p_last >= OBSERVED_MAX_MIN_P_LAST_BAR and dropped:
        status = "observed_max"
    elif (
        p_last >= PLATEAU_MIN_P_LAST_BAR
        and rise is not None
        and rise < RISE_LIMIT_RELATIVE
    ):
        status = "plateau"
    elif p_last >= LOWER_BOUND_MIN_P_LAST_BAR:
        status = "lower_bound"
    else:
        status = "none"
    if status == "none":
        return NmaxResult(status, None, None, p_last, rise)
    return NmaxResult(status, top, peak.pressure_bar, p_last, rise)


def basis_shape_conflict(
    result: NmaxResult, basis_stated: bool | None, basis_inferred: str | None
) -> bool | None:
    """§3: an inferred-excess isotherm still rising steeply at >= 60 bar."""
    if basis_stated is None or basis_inferred is None:
        return None
    if basis_stated or basis_inferred != "excess":
        return False
    return (
        result.nmax_status != "observed_max"
        and result.p_last_bar is not None
        and result.p_last_bar >= CONFLICT_MIN_P_LAST_BAR
        and result.rise_last_vs_07_relative is not None
        and result.rise_last_vs_07_relative > RISE_LIMIT_RELATIVE
    )


def point_uncertainty(row: dict | pd.Series) -> float:
    """§3: the recorded uncertainty, digitization uncertainty for figure points."""
    if as_str(row.get("extraction_method")) == "figure_digitized":
        u = as_float(row.get("digitization_uncertainty_wt_pct"))
    else:
        u = as_float(row.get("uncertainty_wt_pct"))
    return u if u is not None else 0.0


def isotherm_key(row: dict | pd.Series) -> str:
    """Rows sharing an isotherm_id within a paper form one isotherm; a row with
    no isotherm_id is a one-point isotherm of its own (§3 lower bound)."""
    iso = as_str(row.get("isotherm_id"))
    if iso is None:
        return f"{row['paper_id']}|row:{row['measurement_id']}"
    return f"{row['paper_id']}|{iso}"


def _usable_point_row(row: pd.Series) -> bool:
    """§11.0 row filters other than value_kind, which RQ1 applies per isotherm."""
    return (
        as_str(row.get("measurement_mode")) == "isothermal"
        and as_str(row.get("uptake_bound")) in ("exact", "approximate")
        and as_str(row.get("isotherm_branch")) != "desorption"
        and not as_bool(row.get("pressure_unstated"))
        and as_float(row.get("pressure_bar")) is not None
    )


ISOTHERM_COLUMNS = (
    "isotherm_key",
    "paper_id",
    "sample_id",
    "measuring_lab_id",
    "n_points",
    "nmax_status",
    "n_ex_max_wt_pct",
    "p_at_nmax_bar",
    "p_last_bar",
    "basis_stated",
    "basis_shape_conflict",
    "value_kinds",
)


def isotherm_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per coded 77 K isotherm with ``basis_inferred = excess``.

    Raises ValueError when an isotherm mixes samples, temperatures outside the
    77 K window, or bases, because that is an extraction error, not data.
    """
    rows = []
    coded = df[df.apply(is_coded, axis=1)] if len(df) else df
    if coded.empty:
        return pd.DataFrame(columns=ISOTHERM_COLUMNS)
    keys = pd.Series([isotherm_key(r) for _, r in coded.iterrows()], index=coded.index)
    for key, g in coded.groupby(keys, sort=True):
        temps_77 = g["temperature_k"].map(is_77k)
        if not temps_77.any():
            continue
        if not temps_77.all():
            raise ValueError(f"isotherm {key} mixes 77 K and other temperatures")
        if g["sample_id"].nunique() != 1:
            raise ValueError(f"isotherm {key} mixes samples")
        stated = {as_bool(v) for v in g["basis_stated"]}
        inferred = {as_str(v) for v in g["basis_inferred"]}
        if len(stated) != 1 or len(inferred) != 1:
            raise ValueError(f"isotherm {key} mixes bases")
        b_stated, b_inferred = stated.pop(), inferred.pop()
        if b_inferred != "excess":
            continue
        use = g[g.apply(_usable_point_row, axis=1)]
        pts = []
        for _, r in use.iterrows():
            w1 = w1_wt_pct(r)
            if w1 is not None:
                pts.append(Point(float(r["pressure_bar"]), w1, point_uncertainty(r)))
        res = nmax(pts)
        rows.append(
            {
                "isotherm_key": key,
                "paper_id": g["paper_id"].iloc[0],
                "sample_id": g["sample_id"].iloc[0],
                "measuring_lab_id": as_str(g["measuring_lab_id"].iloc[0]),
                "n_points": len(pts),
                "nmax_status": res.nmax_status,
                "n_ex_max_wt_pct": res.n_ex_max_wt_pct,
                "p_at_nmax_bar": res.p_at_nmax_bar,
                "p_last_bar": res.p_last_bar,
                "basis_stated": b_stated,
                "basis_shape_conflict": basis_shape_conflict(res, b_stated, b_inferred),
                "value_kinds": ";".join(
                    sorted({as_str(v) or "" for v in use["value_kind"]})
                ),
            }
        )
    return pd.DataFrame(rows, columns=list(ISOTHERM_COLUMNS))


# ---------------------------------------------------------------------------
# §10.1 reporting-completeness score
# ---------------------------------------------------------------------------


def reporting_items(row: dict | pd.Series) -> dict[str, bool] | None:
    """The nine §10.1 items for one row, or None if the row cannot be scored.

    None means the row is uncoded, or a boolean the score reads is still null.
    On a coded row, a null numeric or text field means the paper does not
    state it.
    """
    if not is_coded(row):
        return None
    flags = {name: as_bool(row.get(name)) for name in SCORE_REQUIRED_BOOLEANS}
    if any(v is None for v in flags.values()):
        return None
    volume = any(
        as_float(row.get(f)) is not None
        for f in (
            "total_pore_volume_cm3_g",
            "micropore_volume_cm3_g",
            "micropore_volume_co2_cm3_g",
        )
    )
    point_count = as_float(row.get("isotherm_point_count"))
    return {
        "1_basis_stated": flags["basis_stated"],
        "2_temperature_stated": not as_bool(row.get("temperature_unstated"))
        and not flags["temperature_inferred"],
        "3_pressure_stated": not as_bool(row.get("pressure_unstated")),
        "4_area_method_and_gas": as_str(row.get("surface_area_method"))
        in NAMED_AREA_METHODS
        and as_str(row.get("surface_area_probe_gas")) in STATED_PROBE_GASES,
        "5_pore_volume_with_method": volume
        and as_str(row.get("pore_volume_method")) not in (None, "unspecified"),
        "6_degassing": as_float(row.get("degas_temperature_c")) is not None
        and (
            as_float(row.get("degas_duration_h")) is not None
            or as_float(row.get("degas_end_pressure_pa")) is not None
        ),
        "7_instrument_and_calibration": flags["instrument_identified"]
        and flags["calibration_described"],
        "8_uncertainty_or_replicates": flags["replicates_reported"]
        or as_float(row.get("uncertainty_wt_pct")) is not None,
        "9_isotherm_points": point_count is not None
        and point_count >= MIN_ISOTHERM_POINTS,
    }


def reporting_score(row: dict | pd.Series) -> int | None:
    items = reporting_items(row)
    return None if items is None else sum(items.values())


def reporting_tier(score: int | None) -> str | None:
    if score is None:
        return None
    for tier, floor in TIER_THRESHOLDS:
        if score >= floor:
            return tier
    raise AssertionError("unreachable")


# ---------------------------------------------------------------------------
# §11.0 area rule and §10.2 plausibility screen
# ---------------------------------------------------------------------------


def eligible_bet_area(row: dict | pd.Series) -> float | None:
    """The BET area if it passes the §11.0 area rule, else None."""
    area = as_float(row.get("bet_surface_area_m2_g"))
    if (
        area is None
        or area <= 0
        or as_str(row.get("surface_area_method")) != "BET"
        or as_str(row.get("surface_area_probe_gas")) not in AREA_PROBE_GASES
        or as_str(row.get("area_same_sample")) != "yes"
    ):
        return None
    return area


def h2_density_g_cm3(temperature_k: float, pressure_bar: float) -> float:
    """Density of normal hydrogen (CoolProp, Leachman et al. 2009), g/cm3."""
    from CoolProp.CoolProp import PropsSI

    return (
        PropsSI("D", "T", temperature_k, "P", pressure_bar * 1e5, "Hydrogen") / 1000.0
    )


def plausibility_flag(row: dict | pd.Series) -> bool | None:
    """§10.2. True = flagged, False = screened and not flagged, None = not
    screenable (or the row is uncoded or not isothermal)."""
    if not is_coded(row) or as_str(row.get("measurement_mode")) != "isothermal":
        return None
    uptake = w1_wt_pct(row)
    t = as_float(row.get("temperature_k"))
    p = as_float(row.get("pressure_bar"))
    basis = as_str(row.get("basis_inferred"))
    if uptake is None or t is None or basis is None:
        return None
    extra = 0.0
    if basis == "total":
        v_total = as_float(row.get("total_pore_volume_cm3_g"))
        if v_total is None or p is None:
            return None
        extra = 100.0 * h2_density_g_cm3(t, p) * v_total
    if is_77k(t):
        area = eligible_bet_area(row)
        if uptake > SCREEN_77K_CAP_WT_PCT + extra:
            return True
        if area is not None:
            bound = (
                SCREEN_77K_AREA_FACTOR * area / CHAHINE_AREA_PER_WT_PCT
                + SCREEN_77K_OFFSET_WT_PCT
            )
            if uptake > bound + extra:
                return True
        return False
    if (
        SCREEN_RT_MIN_K <= t <= SCREEN_RT_MAX_K
        and p is not None
        and p <= SCREEN_RT_MAX_P_BAR
    ):
        return uptake > SCREEN_RT_LIMIT_WT_PCT + extra
    return None


# ---------------------------------------------------------------------------
# Dataset-level
# ---------------------------------------------------------------------------

COMPUTED_ROW_FIELDS = (
    "w1_wt_pct",
    "eligible_bet_area_m2_g",
    "reporting_score",
    "reporting_tier",
    "plausibility_flag",
    "nmax_status",
    "p_at_nmax_bar",
    "p_last_bar",
    "basis_shape_conflict",
)


def add_computed_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``df`` with the computed fields appended.

    Isotherm-level fields are given to every row of the isotherm. Uncoded rows
    get null in every computed field.
    """
    out = df.copy()
    coded = [is_coded(r) for _, r in out.iterrows()]
    out["w1_wt_pct"] = [
        w1_wt_pct(r) if c else None for (_, r), c in zip(out.iterrows(), coded)
    ]
    out["eligible_bet_area_m2_g"] = [
        eligible_bet_area(r) if c else None for (_, r), c in zip(out.iterrows(), coded)
    ]
    scores = [reporting_score(r) for _, r in out.iterrows()]
    out["reporting_score"] = pd.array(scores, dtype="Int64")
    out["reporting_tier"] = [reporting_tier(s) for s in scores]
    out["plausibility_flag"] = pd.array(
        [plausibility_flag(r) for _, r in out.iterrows()], dtype="boolean"
    )
    iso = isotherm_table(out)
    keys = [isotherm_key(r) for _, r in out.iterrows()]
    lookup = iso.set_index("isotherm_key") if len(iso) else None
    for field in ("nmax_status", "p_at_nmax_bar", "p_last_bar", "basis_shape_conflict"):
        if lookup is None:
            out[field] = None
        else:
            out[field] = [
                lookup.at[k, field] if (c and k in lookup.index) else None
                for k, c in zip(keys, coded)
            ]
    return out
