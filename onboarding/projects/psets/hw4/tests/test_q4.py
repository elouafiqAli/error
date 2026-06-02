"""HW4 Q4 — triangle counts globally separate C_6 from 2K_3."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw2.starter.q4b_c6_vs_2k3 import (
    build_2k3,
    build_c6,
)
from onboarding.projects.psets.hw4.starter.q4_triangle_feature import (
    triangle_counts,
)


def test_c6_no_triangles():
    """6-cycle contains no triangles."""
    assert np.allclose(triangle_counts(build_c6(), 6), 0.0)


def test_2k3_each_node_on_one_triangle():
    """In two disjoint triangles, each node is on exactly 1 triangle."""
    assert np.allclose(triangle_counts(build_2k3(), 6), 1.0)


def test_triangle_distinguishes_two_graphs():
    """The two count vectors differ — a global invariant."""
    tc6 = triangle_counts(build_c6(), 6)
    t23 = triangle_counts(build_2k3(), 6)
    assert not np.allclose(tc6, t23)
