"""HW3 Q1 — bisection inverse of binary entropy on [0, 1/2]."""
from __future__ import annotations

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin


def hbin_inverse(h: float, tol: float = 1e-12) -> float:
    """Bisect H_bin on the increasing branch [0, 1/2].

    H_bin: [0, 1/2] -> [0, 1] is strictly increasing, so the inverse
    is well-defined for any h ∈ [0, 1]. Bisect to absolute tolerance
    `tol`.

    Returns 0.0 at h = 0 and 0.5 at h = 1.
    """
    # TODO(student):
    # 1) clamp h: if h <= 0 return 0.0; if h >= 1 return 0.5
    # 2) lo, hi = 0.0, 0.5
    # 3) while hi - lo > tol:
    #        mid = 0.5 * (lo + hi)
    #        if hbin(mid) < h: lo = mid
    #        else:             hi = mid
    # 4) return 0.5 * (lo + hi)
    raise NotImplementedError("hbin_inverse is not implemented")
