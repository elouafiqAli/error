"""HW4 Q3 — degree features are constant on 2-regular graphs."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw2.starter.q4b_c6_vs_2k3 import (
    build_2k3,
    build_c6,
)
from onboarding.projects.psets.hw4.starter.q1_aggregators import (
    sum_partition,
)
from onboarding.projects.psets.hw4.starter.q3_degree_feature import (
    degree_feature,
)


def test_degree_is_two_on_c6():
    assert np.allclose(degree_feature(build_c6(), 6), 2.0)


def test_degree_is_two_on_2k3():
    assert np.allclose(degree_feature(build_2k3(), 6), 2.0)


def test_degree_feature_still_collapses():
    """Even using degree as the feature, sum aggregator collapses."""
    for g_fn in (build_c6, build_2k3):
        g = g_fn()
        x = degree_feature(g, 6)
        p = sum_partition(g, 6, x)
        assert len(p) == 1
