"""Capstone M1 unit tests — read-only."""
from __future__ import annotations

import numpy as np
import pytest

from onboarding.projects.capstone.milestone1.partition import (
    Partition,
    label_partition,
    wl_partition,
)

# PyG-dependent tests skip cleanly if torch_geometric is missing.
pyg = pytest.importorskip("torch_geometric")
from torch_geometric.datasets import Planetoid  # noqa: E402


@pytest.fixture(scope="module")
def cora():
    return Planetoid(root="./data/cora", name="Cora")[0]


def test_partition_rejects_overlap():
    with pytest.raises(ValueError):
        Partition(cells=[np.array([0, 1]), np.array([1, 2])], n=3, _labels=np.array([0, 0, 0]))


def test_partition_rejects_undercover():
    with pytest.raises(ValueError):
        Partition(cells=[np.array([0, 1])], n=3, _labels=np.array([0, 0, 0]))


def test_partition_masses_sum_to_one():
    p = Partition(
        cells=[np.array([0, 1]), np.array([2, 3, 4])],
        n=5,
        _labels=np.array([0, 0, 1, 1, 1]),
    )
    assert abs(p.q.sum() - 1.0) < 1e-12


def test_label_partition_on_cora_has_7_cells(cora):
    p = label_partition(cora)
    assert p.m == 7
    assert np.allclose(p.e, 0.0, atol=1e-12)


def test_wl_partition_refines(cora):
    p1 = wl_partition(cora, depth=1)
    p2 = wl_partition(cora, depth=2)
    assert p1.m <= p2.m


def test_wl_partition_at_least_as_fine_as_classes(cora):
    """Sanity: with the trivial init (all zeros), depth=1 may or may
    not split labels; but depth=3 typically has more cells than the
    7 classes. This is the published behaviour for Cora."""
    p3 = wl_partition(cora, depth=3)
    assert p3.m >= 7
