"""HW2 Q2 — H(Y | Π) on the bracket convention.

Reuses hbin from HW1. Fill in the TODO. ~5 lines of real code.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin


def cond_entropy(
    partition: Sequence[np.ndarray], labels: np.ndarray
) -> float:
    """Conditional entropy H(Y | Π) of labels under a partition.

    Convention (from the paper): per-cell Bayes error
        e_C = 1 - max_y P(Y = y | C)
    and the bracket's conditional entropy is the q-weighted sum of
    binary entropies of e_C:
        H(Y | Π) = Σ_C q_C * H_bin(e_C)        (in bits)
    where q_C = |C| / n.

    Parameters
    ----------
    partition : sequence of np.ndarray
        Each cell is a 1-D int array of node indices.
    labels : np.ndarray
        Length-n int array of class labels.

    Returns
    -------
    float
        H(Y | Π) in bits. 0 when every cell is pure.
    """
    n = sum(len(c) for c in partition)
    if n == 0:
        return 0.0
    # TODO(student):
    # 1) for each cell C:
    #      q = len(C) / n
    #      ys = labels[C]
    #      mode_count = np.bincount(ys).max()
    #      e = 1.0 - mode_count / len(C)
    #      accumulate q * hbin(e)
    # 2) return the accumulated sum.
    raise NotImplementedError("cond_entropy is not implemented")
