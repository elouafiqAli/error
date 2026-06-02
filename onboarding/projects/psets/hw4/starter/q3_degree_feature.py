"""HW4 Q3 — degree features for C_6 and 2K_3.

Both graphs are 2-regular, so the degree feature is constant — and
no aggregator can split a graph with constant features into more
than one cell on a regular graph.
"""
from __future__ import annotations

import numpy as np


def degree_feature(edge_index: np.ndarray, n: int) -> np.ndarray:
    """Vector x[u] = number of neighbours of u."""
    # TODO(student): ~3 lines.
    # deg = np.zeros(n)
    # for u in edge_index[0]:
    #     deg[int(u)] += 1.0
    # return deg
    raise NotImplementedError("degree_feature is not implemented")
