"""HW1 Q2 unit tests — read-only."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw1.starter.q2_bayes import bayes_error


def test_bayes_error_endpoints():
    assert bayes_error(0.0) == 0.0
    assert bayes_error(1.0) == 0.0


def test_bayes_error_half():
    assert bayes_error(0.5) == 0.5


def test_bayes_error_symmetry_and_bound():
    for p in np.linspace(0.0, 1.0, 101):
        e = bayes_error(p)
        assert 0.0 <= e <= 0.5
        assert abs(e - bayes_error(1 - p)) < 1e-15
