"""HW3 Q2 unit tests — bracket endpoints."""
from __future__ import annotations

import pytest

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin
from onboarding.projects.psets.hw3.starter.q2_bracket import lower, upper


@pytest.mark.parametrize("h", [0.0, 0.1, 0.5, 0.9183, 1.0])
def test_upper_is_half_h(h):
    assert abs(upper(h) - h / 2.0) < 1e-12


@pytest.mark.parametrize("eps", [0.05, 0.10, 0.20, 0.30, 0.40])
def test_lower_is_hbin_inverse(eps):
    h = hbin(eps)
    # By construction lower(H_bin(ε)) = ε on the increasing branch.
    assert abs(lower(h) - eps) < 1e-9


def test_bracket_nonnegative_slack():
    for h in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
        assert upper(h) >= lower(h) - 1e-12
