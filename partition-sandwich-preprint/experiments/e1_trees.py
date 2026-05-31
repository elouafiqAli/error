"""
e1_trees.py — Experiment 1: decision-tree refinement funnel.

Train DecisionTreeClassifier on UCI Adult at depths d = 1..15.
For each depth, extract the leaf partition Π_d and compute:
  - lower bracket : H_bin^{-1}(H(f | Π_d))
  - upper bracket : H(f | Π_d) / 2
  - training error of the fitted tree.

Visualises Theorem 1 + Proposition 4 (refinement monotonicity).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from common import bracket_from_cells
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

DEPTHS = list(range(1, 16))
SEED = 0


def main() -> None:
    X, y, _ = load_adult()

    rows = []
    prev_H = float("inf")
    for d in DEPTHS:
        tree = DecisionTreeClassifier(max_depth=d, random_state=SEED)
        tree.fit(X, y)
        cells = tree.apply(X)
        br = bracket_from_cells(cells, y)
        train_err = float(np.mean(tree.predict(X) != y))
        rows.append({
            "depth": d, **br.as_dict(),
            "train_err": train_err,
            "n_leaves": int(tree.get_n_leaves()),
        })
        # data-dependent gates:
        #   - CART majority-vote per leaf MUST equal eps* exactly
        #     (tighter than the audit-noted tautology train_err >= eps*).
        #   - H non-increasing in depth (refinement monotonicity, Prop 4).
        assert abs(train_err - br.eps_star) < 1e-9, \
            f"depth {d}: train_err {train_err} != eps* {br.eps_star}"
        assert br.H <= prev_H + 1e-9, \
            f"depth {d}: H non-monotone {prev_H} -> {br.H}"
        prev_H = br.H

    depths = np.array([r["depth"] for r in rows])
    lower  = np.array([r["lower"]  for r in rows])
    upper  = np.array([r["upper"]  for r in rows])
    eps_st = np.array([r["eps_star"] for r in rows])
    terr   = np.array([r["train_err"] for r in rows])

    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.fill_between(depths, lower, upper, alpha=0.20, color="C0",
                    label=r"bracket $[H_{\mathrm{bin}}^{-1}(H),\ H/2]$")
    ax.plot(depths, lower, "C0-", lw=1.4, label="lower (Fano)")
    ax.plot(depths, upper, "C0--", lw=1.4, label="upper (HR)")
    ax.plot(depths, eps_st, "C2o-", lw=1.6, ms=5,
            label=r"$\varepsilon^{*}_{\Pi_d}$ (plug-in)")
    ax.plot(depths, terr, "C3x-", lw=1.6, ms=6,
            label="CART training error")
    ax.set_xlabel("Tree depth $d$")
    ax.set_ylabel("Error / bracket value")
    ax.set_title("Refinement funnel on UCI Adult (depths 1..15)")
    ax.set_xticks(depths)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out_pdf = FIGURES / "e1_refinement_funnel.pdf"
    fig.savefig(out_pdf)
    plt.close(fig)

    summary = {
        "experiment": "E1 decision-tree refinement funnel",
        "dataset": "UCI Adult", "seed": SEED,
        "depths": DEPTHS,
        "rows": rows,
        "figure": str(out_pdf.relative_to(HERE)),
    }
    (RESULTS / "e1.json").write_text(json.dumps(summary, indent=2))
    print(f"E1: {len(rows)} depths processed; figure → {out_pdf.name}")
    print(f"     final depth d={rows[-1]['depth']}: "
          f"lower={rows[-1]['lower']:.4f} eps*={rows[-1]['eps_star']:.4f} "
          f"train_err={rows[-1]['train_err']:.4f} upper={rows[-1]['upper']:.4f}")


if __name__ == "__main__":
    main()
