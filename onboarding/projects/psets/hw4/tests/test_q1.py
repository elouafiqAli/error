"""HW4 Q1 unit tests — aggregator basics."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw4.starter.q1_aggregators import (
    max_partition,
    mean_partition,
    sum_partition,
)


def _k2():
    return np.array([[0, 1], [1, 0]])


def test_sum_on_k2_constant():
    p = sum_partition(_k2(), n=2, x=np.array([1.0, 1.0]))
    assert len(p) == 1
    assert sorted(p[0].tolist()) == [0, 1]


def test_mean_on_k2_constant():
    p = mean_partition(_k2(), n=2, x=np.array([1.0, 1.0]))
    assert len(p) == 1


def test_max_on_k2_constant():
    p = max_partition(_k2(), n=2, x=np.array([1.0, 1.0]))
    assert len(p) == 1


def test_sum_distinguishes_different_x():
    """K_2 with x = [1, 2]: sum_u = x_neighbor differs so partition splits."""
    p = sum_partition(_k2(), n=2, x=np.array([1.0, 2.0]))
    assert len(p) == 2


def test_sum_p3_split_endpoints_vs_middle():
    """P_3: nodes 0,1,2 with edges 0-1-2; x = [1,1,1].
    Endpoint sees sum = 1 (one neighbor); middle sees sum = 2 (two neighbors).
    Should split into 2 cells."""
    ei = np.array([[0, 1, 1, 2], [1, 0, 2, 1]])
    p = sum_partition(ei, n=3, x=np.array([1.0, 1.0, 1.0]))
    assert len(p) == 2
