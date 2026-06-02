"""HW3 Q3 unit tests — random-sample verifier."""
from __future__ import annotations

from onboarding.projects.psets.hw3.starter.q3_verifier import (
    verify_bracket,
)


def test_verify_bracket_passes():
    """2000 random partition profiles must all satisfy Theorem 1."""
    assert verify_bracket(num_samples=2000, m_max=5, n=200, seed=0) is True


def test_verify_bracket_alt_seed():
    """Robust under a different RNG seed."""
    assert verify_bracket(num_samples=500, m_max=5, n=50, seed=42) is True
