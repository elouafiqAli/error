"""HW1 Q2.2 — Bayes error of a Bernoulli coin.

One line of code. The unit test does the heavy lifting.
"""
from __future__ import annotations


def bayes_error(p: float) -> float:
    """Bayes error of a Bernoulli(p) coin under 0/1 loss.

    Parameters
    ----------
    p : float
        Probability of class 1, in [0, 1].

    Returns
    -------
    float
        min(p, 1 - p).
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"bayes_error expects p in [0, 1], got {p}")
    # TODO(student): one line. Use min().
    raise NotImplementedError("bayes_error is not implemented")
