"""HW3 Q4 — grid search for w* and ε*."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin


def find_w_star(grid: int = 5000) -> tuple[float, float]:
    """Find (ε*, w*) by 1-D grid search over ε ∈ (0, 1/2).

    By Theorem 1, when e_C is constant ≡ ε, the lower bound is tight
    at ε itself: lower(H_bin(ε)) = ε. So the maximum slack along
    the "lower-tight ridge" is
        slack(ε) = H_bin(ε)/2 - ε
    Maximise this over ε ∈ (0, 1/2).

    Returns
    -------
    (eps_star, w_star) : tuple of floats
    """
    # TODO(student):
    # eps_grid = np.linspace(1.0 / grid, 0.5 - 1.0 / grid, grid)
    # slacks = np.array([hbin(e) / 2.0 - e for e in eps_grid])
    # idx = int(np.argmax(slacks))
    # return float(eps_grid[idx]), float(slacks[idx])
    raise NotImplementedError("find_w_star is not implemented")
