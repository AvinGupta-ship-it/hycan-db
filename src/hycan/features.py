"""Feature matrix for the baseline model (manual §14.3).

The model predicts H2 uptake (wt%) from structure and conditions, on the 77 K
modeling subset the manual defines: §12.3-filtered, Tier A/B, wt% present, a
method-confirmed BET area, and -- as in the Chahine figure and meta-analysis --
`total`-uptake rows excluded (a different quantity from the excess/unspecified
uptake the rest of the subset reports).

Features: BET area (method-confirmed only, §10.3), micropore / ultramicropore /
total pore volume, pressure, and material_class one-hot. Target: uptake_wt_pct.

**Doping is deliberately not a feature** (§14.3): the doped subset is small,
split across two concentration units and several condition sets, and at the
77 K/1 bar benchmark is dominated by one or two papers, so an encoded doping
variable would be mostly a paper identifier in disguise. Its absence is a stated
limitation, not an oversight.
"""

from __future__ import annotations

import pandas as pd

from hycan.load import analysis_subset, confirmed_bet_area

NUMERIC_FEATURES = [
    "bet_surface_area_m2_g",
    "micropore_volume_cm3_g",
    "ultramicropore_volume_cm3_g",
    "total_pore_volume_cm3_g",
    "pressure_bar",
]
TARGET = "uptake_wt_pct"
GROUP = "paper_id"


def feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Return the 77 K Tier-A/B modeling rows with features, target and group.

    ``bet_surface_area_m2_g`` is overwritten with the method-confirmed area, so a
    value that is not known to be BET becomes NaN rather than silently entering
    as a feature (§10.3).
    """
    w = analysis_subset(df, require_wt_pct=True).copy()
    w["bet_surface_area_m2_g"] = confirmed_bet_area(w)
    for col in NUMERIC_FEATURES + [TARGET]:
        w[col] = pd.to_numeric(w[col], errors="coerce")
    w = w[
        (w["temperature_k"].astype(float) == 77)
        & w["bet_surface_area_m2_g"].notna()
        & w[TARGET].notna()
        & (w["uptake_type"] != "total")
        & w["reproducibility_tier"].isin(["A", "B"])
    ]
    keep = [GROUP, "measurement_id", "material_class", TARGET,
            "reproducibility_tier"] + NUMERIC_FEATURES
    return w[keep].reset_index(drop=True)


def design_matrix(frame: pd.DataFrame):
    """Return (X, y, groups) from a feature_frame.

    X holds the numeric features plus one-hot material_class columns. Numeric
    features keep their NaNs: XGBoost handles them natively; the linear and
    random-forest baselines impute (see ml.py), with the imputation stated.
    """
    cats = pd.get_dummies(frame["material_class"], prefix="mat", dtype=float)
    X = pd.concat([frame[NUMERIC_FEATURES], cats], axis=1)
    y = frame[TARGET].to_numpy(float)
    groups = frame[GROUP].to_numpy()
    return X, y, groups
