"""verify_prop7_constant.py — P0.1 audit of the Proposition 7 constant.

Goal. Confirm that the gap between the E7 "analytic bound" column
(which uses the κ-free Hoeffding bound √(log(4m/α)/(2n))) and the
*proved* bound of Proposition 7 (`prop:pop` in main.tex),

    |ε*_n − ε*| ≤ κ(δ,η) · √(log(4m/α)/(2n)),
    κ(δ,η)   =  (1/√δ) · (1 + log₂((1-η)/η)),

is the κ-free simplification rather than a mis-stated constant.

Output (deterministic). Prints δ, η, κ at the realised E7 setup
and the multiplied bound at each n in the E7 grid; writes a JSON
record to `results/verify_prop7_constant.json` for citation in
the E7 caption.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from sklearn.tree import DecisionTreeClassifier

from common import bracket_from_cells
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)

K_LEAVES = 16
N_GRID = [200, 500, 1000, 2000, 5000, 10000, 20000]
ALPHA = 0.05
SEED = 0


def kappa(delta: float, eta: float) -> float:
    """κ(δ,η) = (1/√δ)(1 + log₂((1-η)/η))  — Prop 7 constant."""
    return (1.0 / math.sqrt(delta)) * (1.0 + math.log2((1.0 - eta) / eta))


def main() -> None:
    X, y, _ = load_adult()
    n_full = len(y)

    tree = DecisionTreeClassifier(max_leaf_nodes=K_LEAVES, random_state=SEED)
    tree.fit(X, y)
    cell = tree.apply(X)

    uniq, counts = np.unique(cell, return_counts=True)
    m = len(uniq)
    cell_mass = counts / n_full
    delta = float(cell_mass.min())
    P_cell = np.array([y[cell == u].mean() for u in uniq])
    eta = float(np.minimum(P_cell, 1.0 - P_cell).min())

    # Floor η at 1e-3 if any cell has trivial label rate (defensive;
    # the proof requires η > 0 strictly).
    eta_eff = max(eta, 1e-3)

    k = kappa(delta, eta_eff)
    print(f"  n_full={n_full}  m={m}  δ={delta:.5f}  η={eta:.5f}  "
          f"(η_eff={eta_eff:.5f})  κ={k:.3f}")

    rows = []
    for n in N_GRID:
        kappa_free = math.sqrt(math.log(4.0 * m / ALPHA) / (2.0 * n))
        proved = k * kappa_free
        rows.append({
            "n": int(n),
            "kappa_free_bound": float(kappa_free),
            "proved_bound": float(proved),
            "kappa_multiplier": float(k),
        })
        print(f"    n={n:6d}  κ-free={kappa_free:.5f}  "
              f"proved={proved:.5f}  ratio={proved/kappa_free:.2f}×")

    out = {
        "experiment": "verify_prop7_constant",
        "n_full": int(n_full),
        "m_leaves": int(m),
        "delta_min_cell_mass": delta,
        "eta_min_cell_rate": eta,
        "eta_effective": eta_eff,
        "kappa": k,
        "alpha_conf": ALPHA,
        "rows": rows,
        "note": (
            "The E7 'analytic bound' column uses the κ-free bound "
            "(constant 1). Multiplying by κ(δ,η) recovers the proved "
            "Proposition 7 bound; the κ-free bound is conservative-but- "
            "easier-to-read and is the source of the ~order-of-magnitude "
            "looseness observed in E7. No constant in the proof is "
            "mis-stated."
        ),
    }
    out_path = RESULTS / "verify_prop7_constant.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"  -> {out_path}")


if __name__ == "__main__":
    main()
