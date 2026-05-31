"""
common.py — shared primitives for the bracket experiments.

Mirrors the entropy / Bayes-error kernel of verify_t1_float.py so that
the empirical experiments (E1, E2, E4, E5) and the float verifier
remain a single source of truth.  No new mathematics is introduced
here; this is plumbing for the §8 bracket on partitions induced by
real ML pipelines.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


# ---------------------------------------------------------------- entropy
def hbin(p: float) -> float:
    """Binary entropy in bits.  Endpoints handled exactly."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def hbin_inv(h: float, tol: float = 1e-15, max_iter: int = 200) -> float:
    """Bisection inverse of Hbin on [0, 1/2].  Same routine as T1."""
    h = max(0.0, min(1.0, h))
    lo, hi = 0.0, 0.5
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        if hbin(mid) < h:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ----------------------------------------------------------- bracket core
@dataclass
class Bracket:
    n: int
    m: int            # number of cells
    H: float          # H(f | Π)
    eps_star: float   # ε*(Π)
    lower: float      # Hbin^{-1}(H)
    upper: float      # H / 2

    @property
    def width(self) -> float:
        return self.upper - self.lower

    def as_dict(self) -> dict:
        return {
            "n": self.n, "m": self.m, "H": self.H,
            "eps_star": self.eps_star,
            "lower": self.lower, "upper": self.upper,
            "width": self.width,
        }


def bracket_from_cells(cell_ids: Sequence[int],
                       labels: Sequence[int]) -> Bracket:
    """
    Compute the bracket from per-sample cell ids and binary labels.

    cell_ids[i] ∈ {0,…,m-1}: the partition cell of vertex i.
    labels[i]   ∈ {0, 1}    : the binary task label of vertex i.
    """
    cell_ids = np.asarray(cell_ids)
    labels = np.asarray(labels, dtype=float)
    n = len(labels)
    assert len(cell_ids) == n and n > 0

    # remap cell ids to a dense range to allow KMeans / unused labels
    uniq, inverse = np.unique(cell_ids, return_inverse=True)
    m = len(uniq)
    sums = np.bincount(inverse, weights=labels, minlength=m)
    counts = np.bincount(inverse, minlength=m).astype(float)
    P = sums / counts
    q = counts / n
    e = np.minimum(P, 1.0 - P)
    eps_star = float(np.sum(q * e))
    H = float(np.sum(q * np.array([hbin(float(p)) for p in P])))
    return Bracket(n=n, m=int(m), H=H, eps_star=eps_star,
                   lower=hbin_inv(H), upper=0.5 * H)


def plug_in_predictions(cell_ids: Sequence[int],
                        labels: Sequence[int]) -> np.ndarray:
    """Per-cell majority-vote predictions; achieves ε*(Π) exactly."""
    cell_ids = np.asarray(cell_ids)
    labels = np.asarray(labels, dtype=float)
    uniq, inverse = np.unique(cell_ids, return_inverse=True)
    sums = np.bincount(inverse, weights=labels, minlength=len(uniq))
    counts = np.bincount(inverse, minlength=len(uniq)).astype(float)
    P = sums / counts
    cell_pred = (P >= 0.5).astype(int)
    return cell_pred[inverse]


# ------------------------------------------------------------- constants
W_STAR = 0.5 * hbin(1.0 / 5.0) - 1.0 / 5.0   # ≈ 0.16096404744368102
H_STAR = hbin(1.0 / 5.0)                     # ≈ 0.7219280948873623
EPS_W_STAR = 1.0 / 5.0
