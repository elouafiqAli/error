"""Unit tests for shared.partition."""
from __future__ import annotations

import numpy as np
import pytest

from onboarding.projects.shared.partition import (
    Partition,
    wl_refine,
)


class _FakeData:
    """Mimic torch_geometric.data.Data without requiring torch."""

    def __init__(self, edge_index: np.ndarray, y: np.ndarray):
        self.edge_index = edge_index
        self.y = y
        self.num_nodes = len(y)


def test_partition_validates_coverage() -> None:
    n = 4
    p = Partition(
        cells=[np.array([0, 1]), np.array([2, 3])],
        n=n,
        _labels=np.array([0, 0, 1, 1]),
    )
    assert p.m == 2
    np.testing.assert_allclose(p.q, [0.5, 0.5])
    np.testing.assert_allclose(p.e, [0.0, 0.0])


def test_partition_rejects_gap() -> None:
    with pytest.raises(ValueError):
        Partition(cells=[np.array([0, 1])], n=4)


def test_partition_rejects_overlap() -> None:
    with pytest.raises(ValueError):
        Partition(
            cells=[np.array([0, 1, 2]), np.array([2, 3])],
            n=4,
        )


def test_bayes_error_in_cell() -> None:
    # cell {0,1,2} has labels [0, 0, 1] → e = 1 - 2/3 = 1/3
    p = Partition(
        cells=[np.array([0, 1, 2]), np.array([3])],
        n=4,
        _labels=np.array([0, 0, 1, 1]),
    )
    np.testing.assert_allclose(p.e, [1.0 / 3.0, 0.0], atol=1e-12)


def test_wl_refine_distinguishes_path_endpoints() -> None:
    # 4-node path 0-1-2-3 (undirected ⇒ 6 directed edges)
    ei = np.array(
        [[0, 1, 1, 2, 2, 3],
         [1, 0, 2, 1, 3, 2]]
    )
    colors0 = np.zeros(4, dtype=int)
    c1 = wl_refine(ei, 4, colors0)
    # After one round: endpoints (deg=1) vs middles (deg=2).
    assert c1[0] == c1[3]
    assert c1[1] == c1[2]
    assert c1[0] != c1[1]


def test_wl_partition_cycle_stays_uniform() -> None:
    from onboarding.projects.shared.partition import wl_partition

    # 6-cycle: every node has identical local neighbourhood.
    n = 6
    edges = []
    for u in range(n):
        edges.append((u, (u + 1) % n))
        edges.append(((u + 1) % n, u))
    ei = np.array(edges).T
    y = np.zeros(n, dtype=int)
    data = _FakeData(ei, y)
    for d in (0, 1, 3, 5):
        p = wl_partition(data, depth=d)
        assert p.m == 1, f"depth={d}: C_6 must remain 1-colored"
