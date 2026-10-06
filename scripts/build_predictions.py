#!/usr/bin/env python3
"""Write data/processed/predictions_v0.1.csv (manual §4.6).

Out-of-fold predictions for the 77 K modeling subset: each row's prediction comes
from an XGBoost model trained under GroupKFold on papers other than its own, so
the residuals are an honest generalization artifact. Reproducible from a clean
clone: `python3 scripts/build_predictions.py`.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

from hycan.features import TARGET, design_matrix, feature_frame
from hycan.load import load_dataset
from hycan.ml import out_of_fold_predictions

OUT = Path("data/processed/predictions_v0.1.csv")


def build() -> pd.DataFrame:
    frame = feature_frame(load_dataset())
    X, y, groups = design_matrix(frame)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pred = out_of_fold_predictions(X, y, groups, model_name="XGBoost")
    out = frame[[
        "paper_id", "measurement_id", "material_class", "reproducibility_tier",
        "bet_surface_area_m2_g", "pressure_bar", TARGET,
    ]].copy()
    out = out.rename(columns={TARGET: "measured_wt_pct"})
    out["predicted_wt_pct"] = pred
    out["residual_wt_pct"] = out["measured_wt_pct"] - out["predicted_wt_pct"]
    return out


def main() -> int:
    out = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, lineterminator="\n")
    print(f"wrote {OUT}: {len(out)} rows, {out['paper_id'].nunique()} papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
