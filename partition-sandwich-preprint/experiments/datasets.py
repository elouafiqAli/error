"""
datasets.py — single source of truth for the UCI Adult Income dataset.

Cached under experiments/data/.  We use ucimlrepo when available;
fall back to sklearn.datasets.fetch_openml('adult').
"""

from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
DATA_DIR.mkdir(exist_ok=True)


def _fetch_adult_raw() -> tuple[pd.DataFrame, pd.Series]:
    try:
        from ucimlrepo import fetch_ucirepo
        adult = fetch_ucirepo(id=2)
        X = adult.data.features.copy()
        y = adult.data.targets.iloc[:, 0]
    except Exception:
        from sklearn.datasets import fetch_openml
        ds = fetch_openml("adult", version=2, as_frame=True)
        X = ds.data.copy()
        y = ds.target
    return X, y


def load_adult(cache: bool = True) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Returns:
        X : float ndarray (n, d)  — numeric + one-hot, standard-scaled
        y : int   ndarray (n,)    — 1 if income >50K else 0
        feature_names : list[str]
    """
    cache_path = DATA_DIR / "adult.pkl"
    if cache and cache_path.exists():
        with cache_path.open("rb") as f:
            return pickle.load(f)

    from sklearn.preprocessing import StandardScaler

    X_raw, y_raw = _fetch_adult_raw()

    # binary target series aligned to X_raw rows.
    y_series = (y_raw.astype(str).str.strip()
                .str.replace(".", "", regex=False)
                .str.contains(">50K")).astype(int)
    y_series.index = X_raw.index

    # drop rows with NaN; one-hot encode object columns; scale all.
    X_raw = X_raw.replace("?", np.nan).dropna()
    y = y_series.loc[X_raw.index].to_numpy()

    X_df = pd.get_dummies(X_raw, drop_first=True)
    feature_names = X_df.columns.tolist()
    X = StandardScaler().fit_transform(X_df.to_numpy(dtype=float))
    X = X.astype(np.float32)
    y = y.astype(np.int8)

    out = (X, y, feature_names)
    if cache:
        with cache_path.open("wb") as f:
            pickle.dump(out, f)
    return out


if __name__ == "__main__":
    X, y, names = load_adult()
    print(f"X: {X.shape}, y: {y.shape}, positives: {y.mean():.4f}")
