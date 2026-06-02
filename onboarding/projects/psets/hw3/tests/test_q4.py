"""HW3 Q4 unit tests — w* grid search."""
from __future__ import annotations

from onboarding.projects.psets.hw3.starter.q4_wstar import find_w_star


def test_eps_star_around_one_fifth():
    eps_star, w_star = find_w_star(grid=5000)
    assert 0.199 < eps_star < 0.201, eps_star


def test_w_star_around_0p1610():
    eps_star, w_star = find_w_star(grid=5000)
    assert 0.160 < w_star < 0.162, w_star


def test_finer_grid_converges():
    """A finer grid should not change ε* by more than 0.001."""
    eps1, w1 = find_w_star(grid=2000)
    eps2, w2 = find_w_star(grid=20000)
    assert abs(eps1 - eps2) < 0.001
    assert abs(w1 - w2) < 0.001
