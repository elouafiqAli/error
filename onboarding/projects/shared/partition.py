"""Capstone M1 — Data + partition harness.

Fill in the TODOs. Do not change public signatures — the test suite
depends on them. The skeleton runs (raising NotImplementedError)
before you start.

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
        # TODO(student): validate cells.
        #   1) Each cell is a 1-D int array.
        #   2) Cells are pairwise disjoint.
        #   3) Union covers {0..n-1} exactly once.
        #   On failure, raise ValueError with a useful message.
        #
        # Then set:
        #   self.q = np.array([len(c) / self.n for c in self.cells])
        #   self.e = np.array([self._bayes_error_of(c) for c in self.cells])
        #
        # Hint: use np.concatenate + np.sort + np.unique.
        raise NotImplementedError("Partition.__post_init__ is not implemented")

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


def label_partition(data: Data) -> Partition:
    """Build the label partition: one cell per class.

    Each cell C_y = {nodes with label y}. By construction every cell
    has e_C = 0 (because P(Y = y | C_y) = 1).

    Returns a Partition with self._labels set to data.y.numpy().
    """
    # TODO(student): ~5 lines.
    #   1) y = data.y.numpy()
    #   2) cells = [np.where(y == k)[0] for k in range(y.max() + 1)]
    #   3) p = Partition(cells=cells, n=len(y), _labels=y)
    #   4) return p
    #
    # Note: __post_init__ runs after __init__, so set _labels via the
    # constructor (it is a keyword-only arg above).
    raise NotImplementedError("label_partition is not implemented")


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
    # TODO(student): ~10 lines.
    #   1) For each node u, collect sorted tuple of neighbor colors.
    #   2) Build signature[u] = (colors[u], tuple_of_neighbor_colors).
    #   3) Map distinct signatures to dense ints (use a dict).
    #   4) Return the new color array.
    raise NotImplementedError("wl_refine is not implemented")


def wl_partition(data: Data, depth: int) -> Partition:
    """1-WL partition at refinement depth `depth` (>= 0).

    depth=0 means "all nodes one color" — the trivial partition with
    one cell. depth=L means L rounds of wl_refine.
    """
    if depth < 0:
        raise ValueError("depth must be >= 0")
    # TODO(student): ~10 lines.
    #   1) n = data.num_nodes; y = data.y.numpy()
    #   2) edge_index = data.edge_index.numpy()
    #   3) colors = np.zeros(n, dtype=int)
    #   4) for _ in range(depth): colors = wl_refine(edge_index, n, colors)
    #   5) cells = [np.where(colors == c)[0] for c in np.unique(colors)]
    #   6) return Partition(cells=cells, n=n, _labels=y)
    raise NotImplementedError("wl_partition is not implemented")
