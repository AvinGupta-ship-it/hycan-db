"""Dataset loading and the canonical analysis filter (manual §12.3).

Every notebook, figure and model loads the working dataset through
``load_dataset`` and restricts it with ``analysis_subset`` *before* it
aggregates, fits, or plots. The filter lives here, in one function, because the
manual's §12.3 is explicit that four hand-written copies across four notebooks
will not agree -- and a statistic taken over the unfiltered 521 rows silently
mixes four incompatible kinds of number.

The §12.3 exclusions, applied as a **union** (the sets overlap, so the counts do
not sum):

1. ``measurement_mode != "isothermal"`` -- temperature-cycle weight differences
   and TPD desorption integrals are not uptake at a condition.
2. ``uptake_bound != "exact"`` -- a value stated only as "below 0.2 wt%" or
   "close to 1 wt%" is not a measurement of that number.
3. ``temperature_unstated`` or ``pressure_unstated`` -- no condition to plot or
   bound against. These round-trip through CSV as the strings ``"True"`` /
   ``"False"`` (manual §B.3), so they are coerced here rather than trusted.
4. No uptake field populated -- characterization-only rows carry area and pore
   data and nothing to aggregate.

``analysis_subset`` does **not** drop rows that lack ``uptake_wt_pct``
specifically: ten HYC-0024 rows report hydrogen only volumetrically and two
HYC-0020 rows carry ``uptake_mmol_g`` that no one has converted, and all twelve
are legitimate conditioned measurements. A wt%-based figure or model must drop
them on the *target* column, which is what ``require_wt_pct=True`` does -- the
distinction the manual draws between filtering and target selection.

The BET-as-feature rule (manual §10.3, §14.3: do not treat
``bet_surface_area_m2_g`` as a BET area where ``surface_area_method`` says
otherwise) is a feature-construction concern, not a row filter, and lives with
the features, not here. ``confirmed_bet_area`` is provided for callers that need
it.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from hycan.validate import _ANY_UPTAKE_FIELDS

DEFAULT_DATASET = Path("data/raw/measurements_v0.1.csv")

# A CSV has no boolean type; pandas reads these flags back as strings. Treat the
# truthy spellings as True and everything else (including NaN and "False") as
# False.
_TRUE_STRINGS = frozenset({"true", "1", "yes"})


def _is_true(series: pd.Series) -> pd.Series:
    """Coerce a CSV boolean column to a real boolean mask (manual §B.3)."""

    def one(value) -> bool:
        if isinstance(value, bool):
            return value
        if pd.isna(value):
            return False
        return str(value).strip().lower() in _TRUE_STRINGS

    return series.map(one)


def load_dataset(path: Path | str = DEFAULT_DATASET) -> pd.DataFrame:
    """Load the working dataset.

    Deliberately does **not** pass ``keep_default_na=False``: that flag makes
    every empty optional field read as the literal string and look populated
    (manual §6.7, §B.4).
    """
    return pd.read_csv(path)


def _has_any_uptake(df: pd.DataFrame) -> pd.Series:
    """Row mask: at least one uptake field is populated.

    Uses the same field set as ``validate._ANY_UPTAKE_FIELDS`` so this filter and
    the validator never disagree about what "reports an uptake" means. A measured
    zero counts as a measurement (``notna`` matches ``validate._present`` here).
    """
    mask = pd.Series(False, index=df.index)
    for field in _ANY_UPTAKE_FIELDS:
        if field in df.columns:
            mask = mask | df[field].notna()
    return mask


def analysis_subset(df: pd.DataFrame, require_wt_pct: bool = False) -> pd.DataFrame:
    """Return the rows that may enter an aggregation, per manual §12.3.

    Parameters
    ----------
    df:
        The dataset as returned by :func:`load_dataset`.
    require_wt_pct:
        When True, additionally drop rows with no ``uptake_wt_pct`` -- the
        target column for every wt%-based figure and the model. Defaults to
        False, which returns the full §12.3 survivor set (including the twelve
        conditioned rows whose uptake is volumetric or unconverted).
    """
    mode = df["measurement_mode"].fillna("isothermal")
    bound = df["uptake_bound"].fillna("exact")
    keep = (
        (mode == "isothermal")
        & (bound == "exact")
        & ~_is_true(df["temperature_unstated"])
        & ~_is_true(df["pressure_unstated"])
        & _has_any_uptake(df)
    )
    out = df[keep].copy()
    if require_wt_pct:
        out = out[out["uptake_wt_pct"].notna()].copy()
    return out


def confirmed_bet_area(df: pd.DataFrame) -> pd.Series:
    """BET surface area, but only where ``surface_area_method`` confirms it.

    Manual §10.3: ``bet_surface_area_m2_g`` carries values that are not known to
    be BET (31 rows across HYC-0005 and HYC-0012, ``surface_area_method =
    unspecified``). Uptake-per-m2 and the Chahine comparison may use an area only
    where the method is BET; elsewhere this returns NaN.
    """
    area = pd.to_numeric(df["bet_surface_area_m2_g"], errors="coerce")
    return area.where(df["surface_area_method"] == "BET")
