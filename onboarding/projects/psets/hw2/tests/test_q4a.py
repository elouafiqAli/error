"""HW2 Q4.1 unit tests — read-only."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw2.starter.q4a_wl_step import wl_step


def test_k2_constant_stays_constant():
    # K_2: nodes 0, 1; one undirected edge.
    edge_index = np.array([[0, 1], [1, 0]])
    colors = np.array([0, 0])
    new_colors = wl_step(edge_index, n=2, colors=colors)
    # Both nodes have the same signature (same color, same neighbor multiset).
    assert len(np.unique(new_colors)) == 1


def test_p3_endpoints_split_from_middle():
    # P_3: 0 - 1 - 2. Endpoints have one neighbor, middle has two.
    edge_index = np.array([[0, 1, 1, 2], [1, 0, 2, 1]])
    colors = np.zeros(3, dtype=int)
    for _ in range(3):
        colors = wl_step(edge_index, n=3, colors=colors)
    # Endpoint colors should match each other; middle should differ.
    assert colors[0] == colors[2]
    assert colors[1] != colors[0]


def test_star_center_splits_from_leaves():
    # 6-node star: node 0 is connected to 1..5.
    edges_u = [0] * 5 + list(range(1, 6))
    edges_v = list(range(1, 6)) + [0] * 5
    edge_index = np.array([edges_u, edges_v])
    colors = np.zeros(6, dtype=int)
    for _ in range(3):
        colors = wl_step(edge_index, n=6, colors=colors)
    # Center (degree 5) splits from leaves (degree 1).
    assert colors[0] != colors[1]
    # All five leaves share a color.
    assert len(set(colors[1:].tolist())) == 1
