"""HW2 Q1.2 — cross-check the Q1 hand computation.

This file is NOT a TODO. It prints the four numbers from the Q1 toy
so you can verify your hand work to 1e-12.

Run:
    python -m onboarding.projects.psets.hw2.starter.q1_hand_check
"""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin

LABELS = np.array([0, 0, 1, 1, 1, 0])
PARTITION = [np.array([0, 1, 2]), np.array([3, 4]), np.array([5])]


def _per_cell_quantities():
    n = len(LABELS)
    rows = []
    for k, cell in enumerate(PARTITION):
        ys = LABELS[cell]
        size = len(cell)
        q = size / n
        mode_count = np.bincount(ys).max()
        e = 1.0 - mode_count / size
        rows.append((k + 1, list(cell), size, q, e))
    return rows


def main() -> None:
    rows = _per_cell_quantities()
    print("Q1 toy — per-cell quantities")
    print("Cell | nodes        | size | q_C    | e_C")
    print("-----|--------------|------|--------|--------")
    for k, nodes, size, q, e in rows:
        print(f"  {k}  | {nodes!s:13} |  {size}   | {q:.4f} | {e:.4f}")
    eps = sum(q * e for _, _, _, q, e in rows)
    H = sum(q * hbin(e) for _, _, _, q, e in rows)
    print()
    print(f"ε(Π)       = {eps:.6f}")
    print(f"H(Y | Π)   = {H:.6f}   (bits)")


if __name__ == "__main__":
    main()
