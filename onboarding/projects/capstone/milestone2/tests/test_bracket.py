"""M2 bracket — unit tests.

These tests do NOT exercise the Partition class (which has its own
M1 tests). They test the bracket math standalone via raw H values,
plus one integration test that builds a Partition by hand.
"""
from __future__ import annotations

from math import log2

import numpy as np
import pytest

from onboarding.projects.capstone.milestone2.bracket import (
    bracket_of,
    hbin,
    hbin_inverse,
    lower,
    slack,
    upper,
    verify,
)


# --- hbin / hbin_inverse self-consistency ---------------------------------


def test_hbin_endpoints():
    assert hbin(0.0) == 0.0
    assert hbin(1.0) == 0.0
    assert abs(hbin(0.5) - 1.0) < 1e-12


def test_hbin_inverse_round_trip():
    for eps in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
        h = hbin(eps)
        eps_back = hbin_inverse(h)
        assert abs(eps_back - eps) < 1e-9, (eps, h, eps_back)


# --- Bracket endpoints on raw H ------------------------------------------


def test_upper_is_H_over_two():
    for h in [0.0, 0.1, 0.5, 0.9183, 1.0]:
        assert abs(upper(h) - h / 2.0) < 1e-12


def test_lower_is_hbin_inverse():
    for h in [0.0, 0.1, 0.5, 0.9183, 1.0]:
        assert abs(lower(h) - hbin_inverse(h)) < 1e-12


def test_bracket_contains_eps_for_uniform_e():
    """If every cell has the same e_C ≡ ε, then ε(Π) = ε and
    H(Y|Π) = H_bin(ε), so lower = H_bin^{-1}(H_bin(ε)) = ε and the
    bracket collapses to a point at ε."""
    for eps in [0.1, 0.2, 0.3, 0.4]:
        h = hbin(eps)
        assert abs(lower(h) - eps) < 1e-9
        # Upper is H/2 = H_bin(eps)/2 ≥ ε always; slack = H/2 - ε.
        assert upper(h) >= eps - 1e-12


def test_slack_max_is_w_star():
    """The bracket's max slack: w* = max_ε (H_bin(ε)/2 - ε)
    over ε ∈ [0, 1/2]. By the paper, w* ≈ 0.1610 at ε* = 1/5."""
    eps_grid = np.linspace(0.001, 0.499, 2000)
    slacks = np.array([hbin(e) / 2.0 - e for e in eps_grid])
    idx = int(np.argmax(slacks))
    w_star = float(slacks[idx])
    eps_star = float(eps_grid[idx])
    assert 0.20 < eps_star < 0.21, eps_star  # ε* ≈ 0.2 = 1/5
    assert 0.160 < w_star < 0.162, w_star    # w* ≈ 0.1610


# --- verify() predicate ---------------------------------------------------


def test_verify_inside_bracket():
    assert verify(0.5, 0.2) is True  # ε = 0.2 inside [0.11..., 0.25]


def test_verify_outside_bracket():
    # ε = 0.5 outside [0.11..., 0.25]
    assert verify(0.5, 0.5) is False


# --- Integration with Partition (M1) -------------------------------------


def test_bracket_of_partition_uses_q_and_e():
    """Build a Partition by hand without going through __post_init__'s
    validation; bracket_of should return numbers consistent with q.e."""
    pytest.importorskip("torch_geometric")
    from onboarding.projects.capstone.milestone1.partition import Partition

    cells = [np.array([0, 1, 2]), np.array([3, 4])]
    labels = np.array([0, 0, 1, 1, 1])
    try:
        p = Partition(cells=cells, n=5, _labels=labels)
    except NotImplementedError:
        pytest.skip("Partition.__post_init__ not implemented (M1 not done)")
    row = bracket_of(p)
    # Per-cell e: cell 0 = 1/3, cell 1 = 0. q = (3/5, 2/5).
    expected_eps = (3 / 5) * (1 / 3) + (2 / 5) * 0
    expected_H = (3 / 5) * hbin(1 / 3) + 0
    assert abs(row["eps"] - expected_eps) < 1e-9
    assert abs(row["H"] - expected_H) < 1e-9
    assert row["lower"] <= row["eps"] + 1e-9
    assert row["eps"] <= row["upper"] + 1e-9
