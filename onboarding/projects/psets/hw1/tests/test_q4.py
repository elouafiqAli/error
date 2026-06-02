"""HW1 Q4 unit tests — read-only."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw1.starter.q4_mutate import (
    mutation_A,
    mutation_B,
    mutation_C,
)


GRID = np.linspace(0.0, 1.0, 10_001)


def test_mutation_A_finds_violations():
    r = mutation_A(GRID)
    assert r["violations"] > 0


def test_mutation_B_finds_violations():
    r = mutation_B(GRID)
    assert r["violations"] > 0


def test_mutation_C_holds_but_is_uninformative():
    r = mutation_C(GRID)
    assert r["violations"] == 0
    assert r["max_slack"] > 0.5
