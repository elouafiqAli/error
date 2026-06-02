"""HW3 Q1 unit tests — hbin_inverse round trip."""
from __future__ import annotations

import pytest

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin
from onboarding.projects.psets.hw3.starter.q1_hbin_inverse import (
    hbin_inverse,
)


@pytest.mark.parametrize("eps", [0.05, 0.10, 0.20, 0.30, 0.40, 0.50])
def test_round_trip(eps):
    h = hbin(eps)
    eps_back = hbin_inverse(h)
    assert abs(eps_back - eps) < 1e-9, (eps, h, eps_back)


def test_boundaries():
    assert hbin_inverse(0.0) == 0.0
    assert abs(hbin_inverse(1.0) - 0.5) < 1e-9


def test_monotone():
    """hbin_inverse should be non-decreasing in h."""
    prev = -1.0
    for h in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        v = hbin_inverse(h)
        assert v >= prev - 1e-12
        prev = v
