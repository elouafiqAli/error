"""HW2 Q2 unit tests — read-only."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin
from onboarding.projects.psets.hw2.starter.q2_cond_entropy import (
    cond_entropy,
)


def test_singletons_zero_entropy():
    labels = np.array([0, 1, 0, 1, 1])
    partition = [np.array([i]) for i in range(5)]
    assert abs(cond_entropy(partition, labels)) < 1e-12


def test_single_cell_global_bayes_error():
    # labels with 3 zeros, 2 ones → ε = 2/5 → H_bin(2/5)
    labels = np.array([0, 0, 0, 1, 1])
    partition = [np.arange(5)]
    expected = hbin(2 / 5)
    assert abs(cond_entropy(partition, labels) - expected) < 1e-12


def test_q1_toy_value():
    """Q1 toy: labels=[0,0,1,1,1,0], Π=[{0,1,2},{3,4},{5}].
    By hand: q=(3/6,2/6,1/6), e=(1/3,0,0).
    So H(Y|Π) = (1/2) * H_bin(1/3)."""
    labels = np.array([0, 0, 1, 1, 1, 0])
    partition = [np.array([0, 1, 2]), np.array([3, 4]), np.array([5])]
    expected = 0.5 * hbin(1.0 / 3.0)
    assert abs(cond_entropy(partition, labels) - expected) < 1e-12


def test_two_cell_mixed_purity():
    """labels=[0,0,1,1], partition=[{0,1},{2,3}]: pure, H(Y|Π)=0.
    labels=[0,1,0,1], partition=[{0,1},{2,3}]: each cell ε=0.5, H_bin(0.5)=1,
    q_C=0.5 each, so H(Y|Π)=1."""
    labels1 = np.array([0, 0, 1, 1])
    labels2 = np.array([0, 1, 0, 1])
    partition = [np.array([0, 1]), np.array([2, 3])]
    assert abs(cond_entropy(partition, labels1)) < 1e-12
    assert abs(cond_entropy(partition, labels2) - 1.0) < 1e-12
