"""Capstone M2 — the binary-entropy bracket on Bayes error.

The paper's Theorem 1 (binary entropy bracket) says: for any
partition Π of the input space and any labelling Y,

    H_bin^{-1}(H(Y | Π))  ≤  ε(Π)  ≤  H(Y | Π) / 2,

where
    H(Y | Π) = Σ_C q_C * H_bin(e_C)   (the bracket's cond entropy)
    ε(Π)    = Σ_C q_C * e_C            (the bracket's Bayes error)
    q_C     = |C| / n,  e_C = 1 - mode_count(C) / |C|.

The lower bound (Fano in its sharp binary form) and the upper bound
(Hellman–Raviv) are jointly tight in the maximum-slack sense:

    w* := max_{ε ∈ [0, 1/2]} ( ε - H_bin^{-1}(H_bin(ε)) ) ?  NO.

Actually w* is the GAP at the worst point along the trajectory of a
fixed-H bracket: given H ∈ [0, 1], the achievable ε satisfies
H_bin^{-1}(H) ≤ ε ≤ H/2, so slack(H) = H/2 - H_bin^{-1}(H), and
w* = max_H slack(H) ≈ 0.1610 attained at ε* = 1/5.

This module exposes:
    hbin(p)             — binary entropy in bits
    hbin_inverse(h)     — inverse of hbin on the increasing branch [0, 1/2]
    upper(p_or_h)       — H/2 endpoint of the bracket
    lower(p_or_h)       — H_bin^{-1}(H) endpoint
    slack(p_or_h)       — upper - lower
    verify(p_or_h, eps, tol=1e-9) — predicate: lower ≤ eps ≤ upper + tol

`p_or_h` may be either a Partition (M1) or a raw H value in bits.
"""
from __future__ import annotations

from math import log2
from typing import Union

import numpy as np

from onboarding.projects.capstone.milestone1.partition import Partition


# --------------------------------------------------------------------------- #
# Binary entropy and its inverse on the increasing branch.
# --------------------------------------------------------------------------- #
def hbin(p: float) -> float:
    """H_bin(p) = -p log2 p - (1-p) log2 (1-p), in bits.

    Returns 0 at the boundaries.
    """
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * log2(p) + (1.0 - p) * log2(1.0 - p))


def hbin_inverse(h: float, tol: float = 1e-12) -> float:
    """Inverse of H_bin on the increasing branch [0, 1/2].

    H_bin is strictly increasing from 0 to 1 on [0, 1/2], so the
    inverse is well-defined for h ∈ [0, 1]. We bisect to `tol`.
    """
    if h <= 0.0:
        return 0.0
    if h >= 1.0:
        return 0.5
    lo, hi = 0.0, 0.5
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if hbin(mid) < h:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------- #
# Bracket endpoints. Accept Partition or raw H.
# --------------------------------------------------------------------------- #
def _to_H(p_or_h: Union[Partition, float]) -> float:
    if isinstance(p_or_h, Partition):
        # Use the cached q and e arrays set by Partition.__post_init__.
        return float(np.sum(p_or_h.q * np.array([hbin(e) for e in p_or_h.e])))
    return float(p_or_h)


def upper(p_or_h: Union[Partition, float]) -> float:
    """Hellman–Raviv upper bound: ε(Π) ≤ H(Y|Π) / 2."""
    return _to_H(p_or_h) / 2.0


def lower(p_or_h: Union[Partition, float]) -> float:
    """Sharp binary Fano lower bound: ε(Π) ≥ H_bin^{-1}(H(Y|Π))."""
    return hbin_inverse(_to_H(p_or_h))


def slack(p_or_h: Union[Partition, float]) -> float:
    """Bracket width: upper - lower."""
    return upper(p_or_h) - lower(p_or_h)


def verify(
    p_or_h: Union[Partition, float], eps: float, tol: float = 1e-9
) -> bool:
    """Predicate: is `eps` within the bracket [lower, upper]?

    `tol` softens floating-point edge cases. The bracket SHOULD
    hold for any genuine Bayes-error / cond-entropy pair, so a
    `False` return is evidence of a measurement bug.
    """
    return lower(p_or_h) - tol <= eps <= upper(p_or_h) + tol


# --------------------------------------------------------------------------- #
# Bracket-on-partition helper: bind a Partition to its (eps, H, bracket).
# --------------------------------------------------------------------------- #
def bracket_of(p: Partition) -> dict:
    """Return a row {eps, H, lower, upper, slack} for a Partition."""
    H = _to_H(p)
    eps = float(np.sum(p.q * p.e))
    lo = hbin_inverse(H)
    hi = H / 2.0
    return {
        "eps": eps,
        "H": H,
        "lower": lo,
        "upper": hi,
        "slack": hi - lo,
    }
