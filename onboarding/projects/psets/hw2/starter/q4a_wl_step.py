"""HW2 Q4.1 — one round of 1-WL color refinement.

This is the lift of the toy 1-WL you traced by hand in Q3 into
code. Q4.2 will use it.
"""
from __future__ import annotations

import numpy as np


def wl_step(
    edge_index: np.ndarray, n: int, colors: np.ndarray
) -> np.ndarray:
    """One round of 1-WL color refinement.

    Parameters
    ----------
    edge_index : np.ndarray, shape (2, m)
        Directed edges. For an undirected graph include both
        directions: (u, v) and (v, u).
    n : int
        Number of nodes.
    colors : np.ndarray, length n, dtype int
        Current node colors.

    Returns
    -------
    np.ndarray, length n, dtype int
        New colors in [0, K_new). Two nodes receive the same new
        color iff they had the same old color AND the same SORTED
        multiset of neighbor colors.

    Notes
    -----
    - Sort the neighbor-color multiset BEFORE hashing — a python
      tuple is hashable, but order matters for tuple equality.
    - Use a dict {signature: dense_int} to remap.
    """
    # TODO(student):
    # 1) Build a list `neigh[u]` of neighbor colors for each u.
    #    Walk edge_index columns; append colors[v] to neigh[u].
    # 2) Build signature[u] = (colors[u], tuple(sorted(neigh[u]))).
    # 3) Build sig_to_int: dict[signature, int] by iterating signatures.
    # 4) Return np.array([sig_to_int[sig] for sig in signatures], dtype=int).
    raise NotImplementedError("wl_step is not implemented")
