"""
e4_duel.py — Experiment 4: cross-architecture duel on a fixed cell budget.

Fix the architectural budget to K = 16 cells.  Compare:
  - Π_tree : DecisionTreeClassifier(max_leaf_nodes=K).apply(X)
  - Π_vq   : KMeans(n_clusters=K).fit_predict(X)
on UCI Adult.  Both architectures induce a partition with exactly K
cells; the bracket places them on the same information-theoretic
footing, regardless of optimizer.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier

from common import bracket_from_cells
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

K_BUDGET = 16
SEED = 0


def main() -> None:
    X, y, _ = load_adult()

    # --- tree partition ----------------------------------------------------
    t0 = time.perf_counter()
    tree = DecisionTreeClassifier(max_leaf_nodes=K_BUDGET, random_state=SEED)
    tree.fit(X, y)
    tree_cells = tree.apply(X)
    t_tree = time.perf_counter() - t0
    br_tree = bracket_from_cells(tree_cells, y)

    # --- k-means partition -------------------------------------------------
    t0 = time.perf_counter()
    km = KMeans(n_clusters=K_BUDGET, random_state=SEED, n_init=10)
    vq_cells = km.fit_predict(X)
    t_vq = time.perf_counter() - t0
    br_vq = bracket_from_cells(vq_cells, y)

    rows = [
        ("Decision tree (max_leaf_nodes=16)", br_tree, t_tree),
        ("k-means (k=16)",                    br_vq,   t_vq),
    ]

    # --- figure: 2-row summary table ---------------------------------------
    fig, ax = plt.subplots(figsize=(7.6, 2.4))
    ax.axis("off")
    headers = [
        "Architecture", "cells m",
        r"$H(f\mid\Pi)$",
        r"lower $H_{\mathrm{bin}}^{-1}$",
        r"$\varepsilon^{*}_{\Pi}$",
        r"upper $H/2$",
        "fit time (s)",
    ]
    cells = []
    for name, br, dt in rows:
        cells.append([
            name, f"{br.m}",
            f"{br.H:.4f}",
            f"{br.lower:.4f}",
            f"{br.eps_star:.4f}",
            f"{br.upper:.4f}",
            f"{dt:.2f}",
        ])
    tbl = ax.table(cellText=cells, colLabels=headers,
                   loc="center", cellLoc="center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(9)
    tbl.scale(1.0, 1.6)
    ax.set_title(
        rf"Cross-architecture duel on UCI Adult, $K={K_BUDGET}$ cell budget",
        pad=12,
    )
    fig.tight_layout()
    out_pdf = FIGURES / "e4_duel_table.pdf"
    fig.savefig(out_pdf)
    plt.close(fig)

    summary = {
        "experiment": "E4 cross-architecture duel",
        "dataset": "UCI Adult", "n": int(X.shape[0]), "d": int(X.shape[1]),
        "K_budget": K_BUDGET, "seed": SEED,
        "tree": {**br_tree.as_dict(), "fit_time_s": t_tree},
        "vq":   {**br_vq.as_dict(),   "fit_time_s": t_vq},
        "figure": str(out_pdf.relative_to(HERE)),
    }
    (RESULTS / "e4.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

    # verification gates
    assert br_tree.m == K_BUDGET, f"tree induced {br_tree.m} cells, want {K_BUDGET}"
    assert br_vq.m   == K_BUDGET, f"vq induced {br_vq.m} cells, want {K_BUDGET}"
    for name, br, _ in rows:
        assert br.lower - 1e-9 <= br.eps_star <= br.upper + 1e-9, \
            f"{name}: bracket fails {br}"


if __name__ == "__main__":
    main()
