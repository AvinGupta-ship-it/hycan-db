"""
Pure data-cleaning helpers for HyCAN-DB.

``clean_dataset`` normalises a freshly loaded measurement table *without*
mutating the caller's DataFrame:
- strip leading/trailing whitespace from every string column;
- lowercase the ``doi`` column (DOIs are case-insensitive);
- fill a missing ``uptake_mmol_g`` from ``uptake_wt_pct`` (and vice versa) using
  the canonical conversion factors in :mod:`hycan.normalize`;
- standardise ``material_class`` capitalisation to the exact controlled-vocabulary
  spellings declared in :class:`hycan.schema.MeasurementEntry`.

Cleaning is intentionally separate from validation — ``scripts/validate_data.py``
validates the data exactly as loaded and does *not* call this module.
"""

from __future__ import annotations

import typing

import pandas as pd

from hycan.normalize import mmol_per_g_to_wt_pct, wt_pct_to_mmol_per_g
from hycan.schema import MaterialClass

# Lower-cased spelling -> canonical controlled-vocabulary spelling.
_MATERIAL_CLASS_LUT = {value.lower(): value for value in typing.get_args(MaterialClass)}


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of *df* (the input is never mutated)."""
    out = df.copy()

    # 1. Strip whitespace from every string-valued cell. The per-value
    #    isinstance guard makes this dtype-agnostic (works for both the legacy
    #    object dtype and pandas' newer dedicated string dtype).
    for col in out.columns:
        out[col] = out[col].map(lambda x: x.strip() if isinstance(x, str) else x)

    # 2. Lowercase DOIs.
    if "doi" in out.columns:
        out["doi"] = out["doi"].map(
            lambda x: x.lower() if isinstance(x, str) else x
        )

    # 3. Cross-fill the two uptake columns via the canonical conversions.
    if "uptake_wt_pct" in out.columns and "uptake_mmol_g" in out.columns:
        wt = pd.to_numeric(out["uptake_wt_pct"], errors="coerce")
        mmol = pd.to_numeric(out["uptake_mmol_g"], errors="coerce")

        fill_mmol = mmol.isna() & wt.notna()
        fill_wt = wt.isna() & mmol.notna()

        if fill_mmol.any():
            out.loc[fill_mmol, "uptake_mmol_g"] = wt[fill_mmol].map(
                wt_pct_to_mmol_per_g
            )
        if fill_wt.any():
            out.loc[fill_wt, "uptake_wt_pct"] = mmol[fill_wt].map(
                mmol_per_g_to_wt_pct
            )

    # 4. Standardise material_class capitalisation to the schema spellings.
    if "material_class" in out.columns:
        out["material_class"] = out["material_class"].map(
            lambda x: _MATERIAL_CLASS_LUT.get(x.strip().lower(), x)
            if isinstance(x, str)
            else x
        )

    return out
