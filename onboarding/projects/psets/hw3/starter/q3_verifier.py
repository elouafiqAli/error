"""HW3 Q3 — random-sample verifier of Theorem 1."""
from __future__ import annotations

import numpy as np

from onboarding.projects.psets.hw1.starter.q1_hbin import hbin
from .q2_bracket import lower, upper


def random_partition_stats(
    rng: np.random.Generator, m: int, n: int
) -> tuple[float, float]:
    """Sample a random partition profile; return (ε, H).

    Parameters
    ----------
    rng : np.random.Generator
    m   : number of cells (>= 2)
    n   : total population size (used for q_i sampling)
    """
    # TODO(student):
    # 1) sizes = rng.multinomial(n, [1/m]*m)
    #    while np.any(sizes == 0):
    #        sizes = rng.multinomial(n, [1/m]*m)  # avoid empty cells
    # 2) q = sizes / n
    # 3) e = rng.uniform(0.0, 0.5, size=m)
    # 4) eps = float(np.sum(q * e))
    # 5) H = float(np.sum(q * np.array([hbin(ei) for ei in e])))
    # 6) return eps, H
    raise NotImplementedError("random_partition_stats is not implemented")


def verify_bracket(
    num_samples: int = 10_000,
    m_max: int = 5,
    n: int = 200,
    seed: int = 0,
) -> bool:
    """Run the verifier; return True if all samples satisfy the bracket."""
    # TODO(student):
    # rng = np.random.default_rng(seed)
    # for _ in range(num_samples):
    #     m = int(rng.integers(2, m_max + 1))
    #     eps, H = random_partition_stats(rng, m, n)
    #     lo = lower(H); hi = upper(H)
    #     assert lo - 1e-9 <= eps <= hi + 1e-9, (eps, H, lo, hi)
    # return True
    raise NotImplementedError("verify_bracket is not implemented")
