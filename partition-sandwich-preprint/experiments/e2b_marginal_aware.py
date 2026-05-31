"""
e2b_marginal_aware.py — Experiment 2b: marginal-aware bracket slack.

Targets reviewer concern: "w* ≈ 0.161 is worst-case; what is it on
real data once you know the label marginal π*?"

For each binary dataset (Adult, Spambase, Phishing) and each of two
architectures (CART @ 16 leaves, k-means @ k=16) we compute:
  - the realised upper-side slack  ½ H(f|Π) - ε*(Π)
  - the universal worst-case slack W_STAR ≈ 0.161
  - the marginal-aware slack w*(π*) from the piecewise closed form
    (Proposition 6 in main.tex).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from common import W_STAR, bracket_from_cells, hbin, hbin_inv
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)
DATA_DIR = HERE / "data";   DATA_DIR.mkdir(exist_ok=True)

K_LEAVES = 16
SEED = 0
THRESHOLD = 0.5 * hbin(1.0 / 5.0)   # ≈ 0.3610: regime boundary


def marginal_aware_slack(pi_star: float) -> float:
    """w*(π*) from Proposition 6: piecewise closed form."""
    if pi_star >= THRESHOLD:
        return W_STAR
    return pi_star - hbin_inv(2.0 * pi_star)


# ----------------------------------------------------------- loaders
def _openml_xy(name: str, version: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    import pandas as pd
    cache = DATA_DIR / f"{name}.pkl"
    if cache.exists():
        import pickle
        with cache.open("rb") as f:
            return pickle.load(f)
    ds = fetch_openml(name, version=version, as_frame=True)
    X = ds.data.copy()
    # Numeric only; one-hot any objects
    X = pd.get_dummies(X, drop_first=True).astype(float).to_numpy()
    X = StandardScaler().fit_transform(X).astype(np.float32)
    y_raw = ds.target
    # binarise: positive class = most common non-zero string, fallback to first unique
    y = np.asarray(y_raw).astype(str)
    classes = sorted(set(y))
    # For 2-class openml sets, take the lexicographically larger as positive
    pos = classes[-1]
    y = (y == pos).astype(np.int8)
    out = (X, y)
    import pickle
    with cache.open("wb") as f:
        pickle.dump(out, f)
    return out


def load_spambase() -> tuple[np.ndarray, np.ndarray]:
    return _openml_xy("spambase", version=1)


def load_phishing() -> tuple[np.ndarray, np.ndarray]:
    return _openml_xy("PhishingWebsites", version=1)


# ----------------------------------------------------------- driver
def evaluate(X: np.ndarray, y: np.ndarray) -> dict:
    pi = float(y.mean())
    pi_star = min(pi, 1.0 - pi)
    w_marg = marginal_aware_slack(pi_star)

    # CART
    tree = DecisionTreeClassifier(max_leaf_nodes=K_LEAVES, random_state=SEED)
    tree.fit(X, y)
    leaf = tree.apply(X)
    br_t = bracket_from_cells(leaf, y)
    slack_t = br_t.upper - br_t.eps_star

    # k-means
    km = KMeans(n_clusters=K_LEAVES, n_init=10, random_state=SEED).fit(X)
    br_q = bracket_from_cells(km.labels_, y)
    slack_q = br_q.upper - br_q.eps_star

    return {
        "pi": pi, "pi_star": pi_star,
        "w_star": W_STAR, "w_marg": w_marg,
        "tree": {"H": br_t.H, "eps_star": br_t.eps_star,
                 "lower": br_t.lower, "upper": br_t.upper,
                 "slack_realised": slack_t},
        "vq":   {"H": br_q.H, "eps_star": br_q.eps_star,
                 "lower": br_q.lower, "upper": br_q.upper,
                 "slack_realised": slack_q},
    }


def main() -> None:
    loaders = [
        ("adult",    lambda: (load_adult()[0], load_adult()[1])),
        ("spambase", load_spambase),
        ("phishing", load_phishing),
    ]
    rows = []
    for name, ld in loaders:
        t0 = time.perf_counter()
        X, y = ld()
        res = evaluate(X, y)
        dt = time.perf_counter() - t0
        rows.append({"name": name, "n": int(len(y)),
                     "t_s": dt, **res})
        print(f"  {name:10s}  n={len(y):6d}  π*={res['pi_star']:.3f}  "
              f"w*={W_STAR:.3f}  w*(π*)={res['w_marg']:.3f}  "
              f"slack_tree={res['tree']['slack_realised']:.3f}  "
              f"slack_vq={res['vq']['slack_realised']:.3f}  [{dt:.2f}s]")

    # Gates
    all_le_wstar = all(
        r["tree"]["slack_realised"] <= W_STAR + 1e-9
        and r["vq"]["slack_realised"] <= W_STAR + 1e-9
        for r in rows
    )
    all_le_wmarg = all(
        r["tree"]["slack_realised"] <= r["w_marg"] + 1e-9
        and r["vq"]["slack_realised"] <= r["w_marg"] + 1e-9
        for r in rows
    )
    # strict shrinkage on at least one dataset with π* < threshold
    strict_shrink = any(r["w_marg"] < W_STAR - 1e-6 for r in rows)

    summary = {
        "experiment": "E2b marginal-aware slack",
        "K_LEAVES": K_LEAVES, "W_STAR": W_STAR, "THRESHOLD": THRESHOLD,
        "datasets": rows,
        "gates": {
            "all_slack_le_w_star": all_le_wstar,
            "all_slack_le_w_marg": all_le_wmarg,
            "strict_shrink_on_some": strict_shrink,
        },
    }
    out = RESULTS / "e2b.json"
    out.write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nwrote {out}")

    # ----- figure
    names = [r["name"] for r in rows]
    w_marg = [r["w_marg"] for r in rows]
    slack_t = [r["tree"]["slack_realised"] for r in rows]
    slack_q = [r["vq"]["slack_realised"] for r in rows]
    x = np.arange(len(names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.axhline(W_STAR, color="0.5", linestyle="--",
               label=r"universal $w^* \approx 0.161$")
    ax.bar(x - width/2, w_marg, width, color="C0", alpha=0.6,
           label=r"marginal-aware $w^*(\pi_*)$")
    ax.scatter(x - width/2 - 0.0, slack_t, marker="o", color="C3", s=60,
               label="realised slack (CART)")
    ax.scatter(x + width/2, slack_q, marker="s", color="C2", s=60,
               label="realised slack (k-means)")
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylabel("upper-side slack")
    ax.set_title("Marginal-aware slack shrinks the bracket on real binary labels")
    ax.legend(fontsize=8, loc="upper right", framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "e2b_marginal_slack.pdf")
    plt.close(fig)

    assert all_le_wstar, "violation: realised slack exceeds W_STAR"
    assert all_le_wmarg, "violation: realised slack exceeds marginal-aware slack"
    print("gates: PASS")


if __name__ == "__main__":
    main()
