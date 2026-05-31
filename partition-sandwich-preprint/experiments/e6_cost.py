"""
e6_cost.py — Experiment 6 (paper §8.5): bracket vs one training epoch.

Quantifies the O(|V|) remark of §1: one bracket call is orders of
magnitude cheaper than a single CART / KMeans / LR training step on
the same partition.

For each dataset of the menu:
  1. Load (X, y).
  2. Build a k-means partition at k=16 (cell vector C).
  3. Time, median of 11 runs:
       T_bracket : bracket_from_cells(C, y)
       T_CART    : DecisionTreeClassifier(max_leaf_nodes=16).fit(X, y)
       T_kmeans  : KMeans(n_clusters=16).fit_predict(X)
       T_LR      : LogisticRegression(max_iter=1).fit(OHE(C), y)
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from common import bracket_from_cells
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)
DATA_DIR = HERE / "data";   DATA_DIR.mkdir(exist_ok=True)

K = 16
N_REPS = 11
SEED = 0


def _openml_xy_cached(name: str, version: int, binarise) -> tuple[np.ndarray, np.ndarray]:
    cache = DATA_DIR / f"{name}.pkl"
    if cache.exists():
        with cache.open("rb") as f:
            return pickle.load(f)
    import pandas as pd
    ds = fetch_openml(name, version=version, as_frame=True)
    X = pd.get_dummies(ds.data.copy(), drop_first=True).astype(float).to_numpy()
    X = StandardScaler().fit_transform(X).astype(np.float32)
    y = binarise(ds.target).astype(np.int8)
    with cache.open("wb") as f:
        pickle.dump((X, y), f)
    return X, y


def load_spambase():
    return _openml_xy_cached(
        "spambase", 1,
        lambda t: (np.asarray(t).astype(str) == "1").astype(int))


def load_magic():
    return _openml_xy_cached(
        "MagicTelescope", 1,
        lambda t: (np.asarray(t).astype(str) == "g").astype(int))


def load_mnist_bin():
    cache = DATA_DIR / "mnist_bin.pkl"
    if cache.exists():
        with cache.open("rb") as f:
            return pickle.load(f)
    ds = fetch_openml("mnist_784", version=1, as_frame=False)
    X = StandardScaler().fit_transform(ds.data.astype(float)).astype(np.float32)
    y_digits = np.asarray(ds.target).astype(int)
    y = (y_digits >= 5).astype(np.int8)   # 0-4 vs 5-9
    with cache.open("wb") as f:
        pickle.dump((X, y), f)
    return X, y


def median_time(fn, reps: int = N_REPS) -> float:
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts))


def evaluate(name: str, X: np.ndarray, y: np.ndarray) -> dict:
    print(f"  {name:10s}  n={len(y):6d}  d={X.shape[1]:4d}  ...", flush=True)

    # Build partition once
    km_part = KMeans(n_clusters=K, n_init=10, random_state=SEED).fit(X)
    C = km_part.labels_

    # warm-up
    bracket_from_cells(C, y)
    DecisionTreeClassifier(max_leaf_nodes=K, random_state=SEED).fit(X, y)

    t_bracket = median_time(lambda: bracket_from_cells(C, y))
    t_cart    = median_time(lambda: DecisionTreeClassifier(
        max_leaf_nodes=K, random_state=SEED).fit(X, y))
    t_kmeans  = median_time(lambda: KMeans(
        n_clusters=K, n_init=1, random_state=SEED).fit(X))
    ohe = OneHotEncoder(sparse_output=True)
    Ce = ohe.fit_transform(C.reshape(-1, 1))
    t_lr = median_time(lambda: LogisticRegression(
        max_iter=1, solver="lbfgs").fit(Ce, y))

    # smoke check bracket still correct
    br = bracket_from_cells(C, y)
    assert br.lower <= br.eps_star <= br.upper + 1e-12

    res = {
        "name": name, "n": int(len(y)), "d": int(X.shape[1]), "k": K,
        "t_bracket_ms": 1e3 * t_bracket,
        "t_cart_ms":    1e3 * t_cart,
        "t_kmeans_ms":  1e3 * t_kmeans,
        "t_lr_epoch_ms": 1e3 * t_lr,
        "ratios": {
            "cart":   t_bracket / max(t_cart, 1e-12),
            "kmeans": t_bracket / max(t_kmeans, 1e-12),
            "lr":     t_bracket / max(t_lr, 1e-12),
        },
        "bracket": br.as_dict(),
    }
    print(f"    bracket={res['t_bracket_ms']:.3f}ms  "
          f"cart={res['t_cart_ms']:.1f}ms  "
          f"kmeans={res['t_kmeans_ms']:.1f}ms  "
          f"lr={res['t_lr_epoch_ms']:.1f}ms  "
          f"ratio_cart={res['ratios']['cart']:.2e}")
    return res


def main() -> None:
    loaders = [
        ("spambase", load_spambase),
        ("magic",    load_magic),
        ("adult",    lambda: (load_adult()[0], load_adult()[1])),
        ("mnist_bin", load_mnist_bin),
    ]
    rows = []
    for name, ld in loaders:
        X, y = ld()
        rows.append(evaluate(name, X, y))

    gates = {
        "all_bracket_50x_cheaper_than_cart": all(
            r["t_bracket_ms"] < r["t_cart_ms"] / 50.0 for r in rows
        ),
    }
    summary = {
        "experiment": "E6 cost: bracket vs one training epoch",
        "K": K, "N_REPS": N_REPS, "datasets": rows, "gates": gates,
    }
    out = RESULTS / "e6_cost.json"
    out.write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nwrote {out}")

    # figure: grouped log-y bar
    names = [r["name"] for r in rows]
    series = [
        ("bracket", [r["t_bracket_ms"] for r in rows], "C0"),
        ("CART",    [r["t_cart_ms"]    for r in rows], "C3"),
        ("KMeans",  [r["t_kmeans_ms"]  for r in rows], "C2"),
        ("LR (1ep)",[r["t_lr_epoch_ms"]for r in rows], "C1"),
    ]
    x = np.arange(len(names))
    width = 0.2
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    for i, (lab, vals, c) in enumerate(series):
        ax.bar(x + (i - 1.5) * width, vals, width, label=lab, color=c, alpha=0.85)
    ax.set_yscale("log")
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylabel("time per call (ms, log scale)")
    ax.set_title("One bracket call ≪ one training epoch across 4 orders of magnitude in |V|")
    ax.legend(fontsize=8, framealpha=0.95)
    ax.grid(alpha=0.25, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "e6_cost_ratio.pdf")
    plt.close(fig)

    assert gates["all_bracket_50x_cheaper_than_cart"], \
        "gate violation: bracket not 50× cheaper than CART somewhere"
    print("gates: PASS")


if __name__ == "__main__":
    main()
