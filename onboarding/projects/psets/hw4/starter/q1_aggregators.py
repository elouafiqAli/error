"""HW4 Q1 — three aggregator partitions."""
from __future__ import annotations

import numpy as np


def _neighbors(edge_index: np.ndarray, n: int) -> list[list[int]]:
    """Adjacency list (read once, reuse)."""
    nbrs: list[list[int]] = [[] for _ in range(n)]
    for u, v in zip(edge_index[0], edge_index[1]):
        nbrs[int(u)].append(int(v))
    return nbrs


def _partition_from_signatures(
    signatures: list[tuple], n: int
) -> list[np.ndarray]:
    """Cluster node indices by equal signature; return list of cells."""
    groups: dict[tuple, list[int]] = {}
    for u in range(n):
        groups.setdefault(signatures[u], []).append(u)
    return [np.array(g, dtype=int) for g in groups.values()]


def sum_partition(
    edge_index: np.ndarray, n: int, x: np.ndarray
) -> list[np.ndarray]:
    """Partition by (x_u, sum_{v ~ u} x_v) — sum aggregator."""
    # TODO(student):
    # 1) nbrs = _neighbors(edge_index, n)
    # 2) sigs = [(round(float(x[u]), 9), round(float(sum(x[v] for v in nbrs[u])), 9)) for u in range(n)]
    # 3) return _partition_from_signatures(sigs, n)
    raise NotImplementedError("sum_partition is not implemented")


def mean_partition(
    edge_index: np.ndarray, n: int, x: np.ndarray
) -> list[np.ndarray]:
    """Partition by (x_u, mean_{v ~ u} x_v)."""
    # TODO(student): like sum_partition but divide by len(nbrs[u]).
    #   Handle isolated nodes by setting mean to 0.0.
    raise NotImplementedError("mean_partition is not implemented")


def max_partition(
    edge_index: np.ndarray, n: int, x: np.ndarray
) -> list[np.ndarray]:
    """Partition by (x_u, max_{v ~ u} x_v)."""
    # TODO(student): like sum_partition but max instead of sum.
    #   Handle isolated nodes by setting max to 0.0.
    raise NotImplementedError("max_partition is not implemented")
