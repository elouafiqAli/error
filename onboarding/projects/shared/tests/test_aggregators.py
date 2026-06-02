"""Unit tests for shared.aggregators — GIN-vs-rest contrast on C6 vs 2K3."""
from __future__ import annotations

import numpy as np

from onboarding.projects.shared.aggregators import (
    sum_partition,
    mean_partition,
    max_partition,
)


def _c6() -> np.ndarray:
    """6-cycle edge_index (directed both ways)."""
    n = 6
    e = []
    for u in range(n):
        e.append((u, (u + 1) % n))
        e.append(((u + 1) % n, u))
    return np.array(e).T


def _two_k3() -> np.ndarray:
    """Two disjoint triangles on {0,1,2} and {3,4,5} (directed both ways)."""
    e = []
    for a, b in [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]:
        e.append((a, b)); e.append((b, a))
    return np.array(e).T


def test_constant_feature_collapses_to_one_cell() -> None:
    x = np.ones(6)
    for fn in (sum_partition, mean_partition, max_partition):
        for ei in (_c6(), _two_k3()):
            cells = fn(ei, 6, x)
            assert len(cells) == 1


def test_sum_distinguishes_degree_at_least_indirectly() -> None:
    # On a 4-node path 0-1-2-3 with x = ones, sum aggregator splits
    # endpoints (sum=1) from middles (sum=2).
    n = 4
    e = []
    for a, b in [(0, 1), (1, 2), (2, 3)]:
        e.append((a, b)); e.append((b, a))
    ei = np.array(e).T
    cells = sum_partition(ei, n, np.ones(n))
    assert len(cells) == 2
