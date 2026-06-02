"""Unit tests for shared.bracket — Theorem 1 endpoints."""
from __future__ import annotations

import math

import numpy as np
import pytest

from onboarding.projects.shared.bracket import (
    hbin,
    hbin_inverse,
    upper,
    lower,
    slack,
    verify,
)


def test_hbin_endpoints() -> None:
    assert hbin(0.0) == 0.0
    assert hbin(1.0) == 0.0
    assert math.isclose(hbin(0.5), 1.0, abs_tol=1e-12)


def test_hbin_inverse_roundtrip() -> None:
    for p in np.linspace(0.0, 0.5, 33):
        h = hbin(p)
        assert math.isclose(hbin_inverse(h), p, abs_tol=1e-8)


def test_hbin_inverse_endpoints() -> None:
    assert hbin_inverse(0.0) == 0.0
    assert math.isclose(hbin_inverse(1.0), 0.5, abs_tol=1e-12)


@pytest.mark.parametrize("h", [0.0, 0.1, 0.5, 0.8, 1.0])
def test_bracket_orders(h: float) -> None:
    lo = lower(h)
    hi = upper(h)
    assert lo <= hi + 1e-12, f"bracket inversion at H={h}"


def test_wstar_optimum_near_1_over_5() -> None:
    """w* := max_H slack(H) ≈ 0.1610 attained at H* with lower(H*) = ε* ≈ 0.20.

    The first-order condition d/dH [H/2 - H_bin^{-1}(H)] = 0 gives
    H_bin'(ε*) = 2, i.e. log2((1-ε*)/ε*) = 2, i.e. ε* = 1/5.
    """
    hs = np.linspace(0.0, 1.0, 4001)
    ss = np.array([slack(h) for h in hs])
    idx = int(np.argmax(ss))
    h_star = hs[idx]
    eps_lower_at_star = lower(h_star)
    assert math.isclose(eps_lower_at_star, 0.20, abs_tol=2e-3), (
        f"w* attained at lower endpoint ε*≈{eps_lower_at_star}, expected 0.20"
    )
    assert math.isclose(ss[idx], 0.1610, abs_tol=1e-3)
    # Sanity: at H*, upper = ε* + w* and that equals H*/2.
    assert math.isclose(upper(h_star), eps_lower_at_star + ss[idx], abs_tol=1e-6)


def test_verify_holds_for_constant_e_partition() -> None:
    # If all e_C = ε and we feed H = q·Hbin(ε), then both endpoints
    # collapse: lower = ε, upper = Hbin(ε)/2 ≥ ε.
    for eps in (0.05, 0.20, 0.40):
        H = hbin(eps)
        assert verify(H, eps)
