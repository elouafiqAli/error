"""HW1 Q1.2 — binary entropy in bits.

Fill in the TODO. Do NOT import scipy.stats.entropy or similar — the
point is to write it yourself from the definition. Three lines of
real code is enough.

Convention: 0 log 0 = 0, so hbin(0) = hbin(1) = 0.
"""
from __future__ import annotations

import math


def hbin(p: float) -> float:
    """Binary entropy of a Bernoulli(p), in bits.

    Parameters
    ----------
    p : float
        Probability in [0, 1].

    Returns
    -------
    float
        -p log2(p) - (1-p) log2(1-p), with the 0 log 0 = 0 convention.

    Examples
    --------
    >>> hbin(0.0)
    0.0
    >>> hbin(0.5)
    1.0
    >>> abs(hbin(0.1) - 0.46899559358928133) < 1e-12
    True
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"hbin expects p in [0, 1], got {p}")
    # TODO(student): handle the p=0 and p=1 edge cases, then return
    # -p * log2(p) - (1-p) * log2(1-p). ~3 lines.
    raise NotImplementedError("hbin is not implemented")


if __name__ == "__main__":  # quick smoke
    for p in [0.0, 0.1, 0.5, 0.9, 1.0]:
        print(f"hbin({p}) = {hbin(p)}")
