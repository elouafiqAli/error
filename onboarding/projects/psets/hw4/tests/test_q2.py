"""HW4 Q2 — constant features collapse to one cell on C_6 and 2K_3."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw2.starter.q4b_c6_vs_2k3 import (
    build_2k3,
    build_c6,
)
from onboarding.projects.psets.hw4.starter.q1_aggregators import (
    max_partition,
    mean_partition,
    sum_partition,
)


def test_c6_constant_collapses_all_aggregators():
    """C_6 with x = 1: all aggregators yield one cell of size 6."""
    g = build_c6()
    x = np.ones(6)
    assert len(sum_partition(g, 6, x)) == 1
    assert len(mean_partition(g, 6, x)) == 1
    assert len(max_partition(g, 6, x)) == 1


def test_2k3_constant_collapses_all_aggregators():
    g = build_2k3()
    x = np.ones(6)
    assert len(sum_partition(g, 6, x)) == 1
    assert len(mean_partition(g, 6, x)) == 1
    assert len(max_partition(g, 6, x)) == 1
