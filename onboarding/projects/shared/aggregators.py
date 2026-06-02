"""Canonical aggregator-induced partitions (sum / mean / max).

Companion to `shared.partition.wl_refine`. These are the three
aggregators audited in HW4 / capstone M4; each maps a 1-feature
node attribute `x` to a signature partition and demonstrates the
GIN injectivity contrast on C6 vs 2K3.
"""
from __future__ import annotations

import numpy as np


def _neighbors(edge_index: np.ndarray, n: int) -> list[list[int]]:
    nbrs: list[list[int]] = [[] for _ in range(n)]
    for u, v in zip(edge_index[0], edge_index[1]):
        nbrs[int(u)].append(int(v))
    return nbrs


def _partition_from_signatures(
    signatures: list[tuple], n: int
) -> list[np.ndarray]:
    groups: dict[tuple, list[int]] = {}
    for u in range(n):
        groups.setdefault(signatures[u], []).append(u)
    return [np.array(g, dtype=int) for g in groups.values()]


def _round(x: float, digits: int = 9) -> float:
    return round(float(x), digits)


def sum_partition(
    edge_index: np.ndarray, n: int, x: np.ndarray
) -> list[np.ndarray]:
    """Partition by (x_u, sum_{v ~ u} x_v) — sum aggregator (GIN-like)."""
    nbrs = _neighbors(edge_index, n)
    sigs = [
        (_round(x[u]), _round(sum(x[v] for v in nbrs[u])))
        for u in range(n)
    ]
    return _partition_from_signatures(sigs, n)


def mean_partition(
    edge_index: np.ndarray, n: int, x: np.ndarray
) -> list[np.ndarray]:
    """Partition by (x_u, mean_{v ~ u} x_v) — GCN-like.

    Isolated nodes get mean = 0.0.
    """
    nbrs = _neighbors(edge_index, n)
    sigs = []
    for u in range(n):
        if nbrs[u]:
            m = sum(x[v] for v in nbrs[u]) / len(nbrs[u])
        else:
            m = 0.0
        sigs.append((_round(x[u]), _round(m)))
    return _partition_from_signatures(sigs, n)


def max_partition(
    edge_index: np.ndarray, n: int, x: np.ndarray
) -> list[np.ndarray]:
    """Partition by (x_u, max_{v ~ u} x_v) — GraphSAGE-max-like.

    Isolated nodes get max = 0.0.
    """
    nbrs = _neighbors(edge_index, n)
    sigs = []
    for u in range(n):
        if nbrs[u]:
            m = max(x[v] for v in nbrs[u])
        else:
            m = 0.0
        sigs.append((_round(x[u]), _round(m)))
    return _partition_from_signatures(sigs, n)
