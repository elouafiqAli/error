"""Shared — Partition dataclass + canonical 1-WL builders.

This module is the *reference implementation* used by the test
suite and by capstone milestones. The HW notebooks re-derive these
builders themselves; nothing in `shared/` is meant to be a TODO for
the student.

Convention throughout this capstone:
  - Nodes are indexed 0..n-1.
  - Labels are integers in 0..K-1.
  - A Partition is a list of disjoint subsets of {0..n-1} that
    together cover the whole node set.
  - q_C = |C| / n   (uniform prior over nodes)
  - e_C = 1 - max_y P(Y = y | C)
        = 1 - (max class count in C) / |C|
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

# PyG imports are deferred to keep `pytest --collect-only` fast even
# without torch installed. Tests that exercise PyG will skip if it is
# not importable.
try:
    import torch
    from torch_geometric.datasets import Planetoid
    from torch_geometric.data import Data
    _PYG_OK = True
except ImportError:
    _PYG_OK = False
    Data = object  # type: ignore[assignment,misc]


# --- Partition dataclass ---------------------------------------------------


@dataclass
class Partition:
    """A partition of {0, ..., n-1} carrying cell masses and Bayes errors.

    Attributes
    ----------
    cells : list of np.ndarray
        Each cell is a 1-D int array of node indices. Cells must be
        pairwise disjoint and together cover {0, ..., n-1}.
    n : int
        Total number of nodes.
    q : np.ndarray
        Length-len(cells) array of cell masses q_C = |C| / n.
    e : np.ndarray
        Length-len(cells) array of per-cell Bayes errors.
    """

    cells: Sequence[np.ndarray]
    n: int
    q: np.ndarray = field(init=False)
    e: np.ndarray = field(init=False)
    _labels: np.ndarray | None = None  # set by builders; used to compute e

    def __post_init__(self) -> None:
        # Validate: each cell a 1-D int array; pairwise disjoint; covers {0..n-1}.
        flat_parts = []
        for i, c in enumerate(self.cells):
            arr = np.asarray(c, dtype=int)
            if arr.ndim != 1:
                raise ValueError(f"cell {i} is not 1-D")
            flat_parts.append(arr)
        if flat_parts:
            flat = np.concatenate(flat_parts)
        else:
            flat = np.empty(0, dtype=int)
        if flat.size != self.n:
            raise ValueError(
                f"cells cover {flat.size} nodes; expected n={self.n}"
            )
        uniq = np.unique(flat)
        if uniq.size != self.n or uniq.min() != 0 or uniq.max() != self.n - 1:
            raise ValueError(
                "cells must form a partition of {0..n-1}"
            )
        self.q = np.array([len(c) / self.n for c in self.cells], dtype=float)
        self.e = np.array(
            [self._bayes_error_of(np.asarray(c, dtype=int)) for c in self.cells],
            dtype=float,
        )

    def _bayes_error_of(self, cell: np.ndarray) -> float:
        """Per-cell Bayes error 1 - max_y P(Y = y | C).

        If self._labels is None, returns 0.0 (caller is responsible
        for setting labels before invariants are computed).
        """
        if self._labels is None:
            return 0.0
        if len(cell) == 0:
            return 0.0
        ys = self._labels[cell]
        counts = np.bincount(ys)
        return 1.0 - counts.max() / len(cell)

    @property
    def m(self) -> int:
        return len(self.cells)


# --- Builders --------------------------------------------------------------


def load_cora(root: str = "./data/cora") -> Data:
    """Load the Cora dataset via PyG."""
    if not _PYG_OK:
        raise RuntimeError("PyTorch Geometric is not installed.")
    return Planetoid(root=root, name="Cora")[0]


def label_partition(data) -> Partition:
    """Build the label partition: one cell per class.

    Each cell C_y = {nodes with label y}. By construction every cell
    has e_C = 0 (because P(Y = y | C_y) = 1).
    """
    y = data.y.numpy() if hasattr(data.y, "numpy") else np.asarray(data.y)
    K = int(y.max()) + 1
    cells = [np.where(y == k)[0] for k in range(K)]
    cells = [c for c in cells if len(c) > 0]
    return Partition(cells=cells, n=len(y), _labels=y)


def wl_refine(
    edge_index: np.ndarray, n: int, colors: np.ndarray
) -> np.ndarray:
    """One step of 1-WL color refinement.

    Parameters
    ----------
    edge_index : np.ndarray
        Shape (2, m); each column (u, v) is a directed edge.
    n : int
        Number of nodes.
    colors : np.ndarray
        Length-n integer array of current colors.

    Returns
    -------
    np.ndarray
        Length-n integer array of new colors. The map
        node -> (old_color, sorted_multiset_of_neighbor_colors)
        is rehashed to a dense integer range [0, K_new).
    """
    nbrs: list[list[int]] = [[] for _ in range(n)]
    for u, v in zip(edge_index[0], edge_index[1]):
        nbrs[int(u)].append(int(v))
    sigs: list[tuple] = []
    for u in range(n):
        nb = tuple(sorted(int(colors[v]) for v in nbrs[u]))
        sigs.append((int(colors[u]), nb))
    table: dict[tuple, int] = {}
    out = np.empty(n, dtype=int)
    for u, s in enumerate(sigs):
        if s not in table:
            table[s] = len(table)
        out[u] = table[s]
    return out


def wl_partition(data, depth: int) -> Partition:
    """1-WL partition at refinement depth `depth` (>= 0).

    depth=0 means "all nodes one color" — the trivial 1-cell partition.
    depth=L means L rounds of `wl_refine`.
    """
    if depth < 0:
        raise ValueError("depth must be >= 0")
    n = int(data.num_nodes)
    y = data.y.numpy() if hasattr(data.y, "numpy") else np.asarray(data.y)
    edge_index = (
        data.edge_index.numpy() if hasattr(data.edge_index, "numpy")
        else np.asarray(data.edge_index)
    )
    colors = np.zeros(n, dtype=int)
    for _ in range(depth):
        colors = wl_refine(edge_index, n, colors)
    cells = [np.where(colors == c)[0] for c in np.unique(colors)]
    return Partition(cells=cells, n=n, _labels=y)
