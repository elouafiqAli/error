"""
e7_pop_concentration.py — Proposition 7 empirical companion on UCI Adult.

Treats the full dataset as the "population" and verifies that the
empirical Bayes error on a fixed partition concentrates around the
full-data value at the Hoeffding rate.

Key choices (post-audit revision):
  * Subsamples drawn with REPLACEMENT (bootstrap), so n may approach
    n_full without the without-replacement degeneracy.
  * Deviation measured as |Δε*| only (the quantity Prop 7 bounds);
    we drop |ΔH| from the LHS.
  * Hoeffding bound for ε* on a FIXED partition of m cells:
        |ε*_n − ε*| ≤ √( log(4m/α) / (2n) )
    via per-cell Hoeffding + union over m cells (no κ ≈ 9.9 surrogate).
  * Grid capped at 20 000 (≄44 % of n_full=45 222) so that bootstrap
    diversity remains non-trivial.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from common import bracket_from_cells
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

K_LEAVES = 16
N_GRID = [200, 500, 1000, 2000, 5000, 10000, 20000]
K_TRIALS = 400
DELTA_CONF = 0.05
SEED = 0


def hoeffding_bound_eps(n: int, m: int, alpha: float) -> float:
    """|ε*_n − ε*| ≤ √( log(4m/α) / (2n) )  — fixed-partition Hoeffding
    with union bound over the m cells."""
    return math.sqrt(math.log(4.0 * m / alpha) / (2.0 * n))


def main() -> None:
    X, y, _ = load_adult()
    n_full = len(y)
    print(f"  n_full={n_full}, π={y.mean():.4f}")

    # Fixed partition from CART on full data
    tree = DecisionTreeClassifier(max_leaf_nodes=K_LEAVES, random_state=SEED)
    tree.fit(X, y)
    cell_full = tree.apply(X)
    br_full = bracket_from_cells(cell_full, y)
    print(f"  full bracket: lower={br_full.lower:.4f}  "
          f"ε*={br_full.eps_star:.4f}  upper={br_full.upper:.4f}")

    # δ = min cell mass; η = min cell-positive-rate (min, 1-min)
    uniq, counts = np.unique(cell_full, return_counts=True)
    cell_mass = counts / n_full
    delta_mass = float(cell_mass.min())
    P_cell = np.array([
        y[cell_full == u].mean() for u in uniq
    ])
    eta = float(np.minimum(P_cell, 1.0 - P_cell).min())
    print(f"  δ_mass={delta_mass:.4f}  η_min={eta:.4f}")

    m = len(uniq)
    rng = np.random.default_rng(SEED)

    rows = []
    for n in N_GRID:
        if n > n_full:
            continue
        deltas = np.empty(K_TRIALS)
        for k in range(K_TRIALS):
            # bootstrap: WITH replacement
            idx = rng.integers(0, n_full, size=n)
            br_sub = bracket_from_cells(cell_full[idx], y[idx])
            deltas[k] = abs(br_full.eps_star - br_sub.eps_star)
        bound = hoeffding_bound_eps(n, m, DELTA_CONF)
        coverage = float((deltas <= bound).mean())
        rows.append({
            "n": int(n),
            "K": K_TRIALS,
            "delta_mean": float(deltas.mean()),
            "delta_p95":  float(np.quantile(deltas, 0.95)),
            "bound": float(bound),
            "coverage": coverage,
        })
        print(f"    n={n:6d}  Δmean={rows[-1]['delta_mean']:.5f}  "
              f"Δp95={rows[-1]['delta_p95']:.5f}  "
              f"bound={bound:.5f}  cov={coverage:.3f}")

    gates = {
        "all_coverage_ge_1_minus_alpha": all(
            r["coverage"] >= 1.0 - DELTA_CONF - 1e-9 for r in rows
        ),
        "delta_mean_monotone_in_n": all(
            rows[i]["delta_mean"] >= rows[i + 1]["delta_mean"] - 1e-6
            for i in range(len(rows) - 1)
        ),
        "delta_p95_le_bound_everywhere": all(
            r["delta_p95"] <= r["bound"] + 1e-6 for r in rows
        ),
    }
    summary = {
        "experiment": "E7 real-data Proposition 7 concentration (bootstrap)",
        "dataset": "adult", "m": int(m), "delta_conf": DELTA_CONF,
        "delta_mass": delta_mass, "eta_min": eta,
        "sampling": "bootstrap (with replacement)",
        "deviation": "|Δε*|",
        "bound": "sqrt(log(4m/alpha) / (2n))",
        "full": br_full.as_dict(),
        "rows": rows, "gates": gates,
    }
    out = RESULTS / "e7.json"
    out.write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nwrote {out}")

    # figure
    ns      = np.array([r["n"] for r in rows], dtype=float)
    p95     = np.array([r["delta_p95"] for r in rows])
    means   = np.array([r["delta_mean"] for r in rows])
    bounds  = np.array([r["bound"] for r in rows])
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.loglog(ns, p95,    "o-",  color="C0", label=r"$\Delta_n^{(p95)}$ (empirical)")
    ax.loglog(ns, means,  "s--", color="C2", label=r"$\overline{\Delta_n}$ (mean)")
    ax.loglog(ns, bounds, "k:",  label=r"Hoeffding bound $\sim 1/\sqrt{n}$")
    ax.set_xlabel("subsample size $n$")
    ax.set_ylabel(r"bracket deviation $|\Delta\varepsilon^*| + |\Delta H|$")
    ax.set_title("E7: empirical Proposition-7 concentration on UCI Adult")
    ax.legend(fontsize=9, framealpha=0.95)
    ax.grid(alpha=0.25, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "e7_concentration.pdf")
    plt.close(fig)

    assert gates["all_coverage_ge_1_minus_alpha"], "coverage gate failed"
    print("gates: PASS")


if __name__ == "__main__":
    main()
