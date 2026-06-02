"""HW2 Q4.2 unit tests — read-only.

The canonical 1-WL blind spot: C_6 (6-cycle) and 2 K_3 (two
disjoint triangles) are 2-regular, have the same degree
distribution, AND produce the same 1-WL stable colour multiset.
"""
from __future__ import annotations

from onboarding.projects.psets.hw2.starter.q4b_c6_vs_2k3 import (
    build_2k3,
    build_c6,
    color_multiset,
    degree_distribution,
    run_wl_to_stability,
)


def test_both_are_2_regular():
    c6 = build_c6()
    k3k3 = build_2k3()
    assert degree_distribution(c6, 6) == (2, 2, 2, 2, 2, 2)
    assert degree_distribution(k3k3, 6) == (2, 2, 2, 2, 2, 2)


def test_blind_spot_same_multiset():
    c6 = build_c6()
    k3k3 = build_2k3()
    sc6 = run_wl_to_stability(c6, 6)
    s23 = run_wl_to_stability(k3k3, 6)
    assert color_multiset(sc6) == color_multiset(s23)


def test_blind_spot_one_cell_of_size_six():
    """Both stable colourings should be all-one-colour: every node
    has the same local neighbourhood multiset (two neighbours, each
    of colour 0 in the limit)."""
    c6 = build_c6()
    k3k3 = build_2k3()
    sc6 = run_wl_to_stability(c6, 6)
    s23 = run_wl_to_stability(k3k3, 6)
    assert color_multiset(sc6) == (6,)
    assert color_multiset(s23) == (6,)
