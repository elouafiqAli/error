"""HW4 Q4 — triangle-count features."""
from __future__ import annotations

import numpy as np


def triangle_counts(edge_index: np.ndarray, n: int) -> np.ndarray:
    """Vector t[u] = number of triangles incident on u.

    A triangle on (u, v, w) requires three undirected edges:
        u ~ v,  v ~ w,  w ~ u.
    """
    # TODO(student):
    # 1) Build adjacency set:
    #    adj = [set() for _ in range(n)]
    #    for u, v in zip(edge_index[0], edge_index[1]):
    #        adj[int(u)].add(int(v))
    # 2) For each u: count pairs (v, w) in adj[u] with v < w and w in adj[v].
    #    That counts the number of triangles on u exactly.
    # 3) Return t as float array.
    raise NotImplementedError("triangle_counts is not implemented")
