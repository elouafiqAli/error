"""HW1 Q1 unit tests — read-only."""
from __future__ import annotations

import math

import numpy as np
import pytest

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin


def test_hbin_endpoints():
    assert hbin(0.0) == 0.0
    assert hbin(1.0) == 0.0


def test_hbin_half_is_one_bit():
    assert abs(hbin(0.5) - 1.0) < 1e-12


def test_hbin_symmetry():
    rng = np.random.default_rng(seed=42)
    for p in rng.uniform(low=1e-6, high=1 - 1e-6, size=100):
        assert abs(hbin(p) - hbin(1 - p)) < 1e-12


def test_hbin_reference_value():
    # -0.1 log2 0.1 - 0.9 log2 0.9
    assert abs(hbin(0.1) - 0.46899559358928133) < 1e-12


def test_hbin_rejects_out_of_range():
    with pytest.raises(ValueError):
        hbin(-0.01)
    with pytest.raises(ValueError):
        hbin(1.01)
