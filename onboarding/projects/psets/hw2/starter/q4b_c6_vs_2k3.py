"""HW2 Q4.2 — C_6 vs 2 K_3 blind spot.

Build both graphs; run 1-WL to stability; verify the canonical
1-WL blind spot: the two graphs are non-isomorphic but 1-WL cannot
tell them apart.
"""
from __future__ import annotations

import numpy as np

from .q4a_wl_step import wl_step


def build_c6() -> np.ndarray:
    """Edge index of the 6-cycle C_6 (undirected, both directions)."""
    # TODO(student):
    # Nodes 0..5; edges i <-> (i+1) mod 6.
    # Return np.ndarray of shape (2, 12).
    raise NotImplementedError("build_c6 is not implemented")


def build_2k3() -> np.ndarray:
    """Edge index of two disjoint triangles 2 K_3 (undirected)."""
    # TODO(student):
    # Triangle 1 on nodes {0,1,2}; triangle 2 on nodes {3,4,5}.
    # Return np.ndarray of shape (2, 12).
    raise NotImplementedError("build_2k3 is not implemented")


def run_wl_to_stability(
    edge_index: np.ndarray, n: int, max_iter: int = 20
) -> np.ndarray:
    """Run 1-WL refinement until the color partition stops changing.

    Returns the stable color array.
    """
    # TODO(student):
    # colors = np.zeros(n, dtype=int)
    # for _ in range(max_iter):
    #     new_colors = wl_step(edge_index, n, colors)
    #     # equivalence classes are preserved iff the induced
    #     # partition is the same; detect via len(unique).
    #     if len(np.unique(new_colors)) == len(np.unique(colors)):
    #         return new_colors  # stable
    #     colors = new_colors
    # return colors
    raise NotImplementedError("run_wl_to_stability is not implemented")


def color_multiset(colors: np.ndarray) -> tuple[int, ...]:
    """Sorted tuple of counts per color — the canonical 1-WL signature."""
    _, counts = np.unique(colors, return_counts=True)
    return tuple(sorted(counts.tolist()))


def degree_distribution(edge_index: np.ndarray, n: int) -> tuple[int, ...]:
    """Sorted tuple of degrees — sanity check."""
    deg = np.zeros(n, dtype=int)
    for u in edge_index[0]:
        deg[u] += 1
    return tuple(sorted(deg.tolist()))


if __name__ == "__main__":
    c6 = build_c6()
    k3k3 = build_2k3()
    print("C_6  degree-dist :", degree_distribution(c6, 6))
    print("2K_3 degree-dist :", degree_distribution(k3k3, 6))
    sc6 = run_wl_to_stability(c6, 6)
    s23 = run_wl_to_stability(k3k3, 6)
    print("C_6  stable-colors:", sc6, "multiset:", color_multiset(sc6))
    print("2K_3 stable-colors:", s23, "multiset:", color_multiset(s23))
    print("Same multiset? ", color_multiset(sc6) == color_multiset(s23))
