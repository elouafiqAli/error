"""HW3 Q2 — plot the bracket envelope.

Run:
    python -m onboarding.projects.psets.hw3.starter.q2_plot
Output:
    plots/q2_bracket_envelope.png
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin
from .q1_hbin_inverse import hbin_inverse
from .q2_bracket import lower, upper


def main() -> None:
    # TODO(student):
    # 1) h_grid = np.linspace(0, 1, 401)
    # 2) ups = np.array([upper(h) for h in h_grid])
    # 3) los = np.array([lower(h) for h in h_grid])
    # 4) plt.fill_between(h_grid, los, ups, alpha=0.2, label="slack")
    # 5) plt.plot(h_grid, ups, label="upper = H/2")
    # 6) plt.plot(h_grid, los, label="lower = H_bin^{-1}(H)")
    # 7) plt.xlabel("H = H(Y | Π) [bits]"); plt.ylabel("ε(Π)")
    # 8) plt.legend(); plt.tight_layout()
    # 9) os.makedirs("plots", exist_ok=True)
    # 10) plt.savefig("plots/q2_bracket_envelope.png", dpi=150)
    raise NotImplementedError("Q2 plot is not implemented")


if __name__ == "__main__":
    main()
