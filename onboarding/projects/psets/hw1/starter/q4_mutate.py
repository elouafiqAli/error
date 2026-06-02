"""HW1 Q4 — mutate the Hellman–Raviv verifier, watch it fail.

Three mutations. Each differs from q3_hr_verifier.hr_violations by
ONE constant or function. The mutations are intentionally wrong;
the goal is to see how the verifier responds and to map each failure
back to a step in the published proof.
"""
from __future__ import annotations

import math

import numpy as np

from .q1_hbin import hbin
from .q2_bayes import bayes_error
from .q3_hr_verifier import HRReport


def mutation_A(grid: np.ndarray, atol: float = 1e-12) -> HRReport:
    """Mutation A: replace 0.5 with 0.4 in the upper bound.

    Check: bayes_error(p) <= 0.4 * hbin(bayes_error(p))

    Expected: violations > 0 for some p strictly inside (0, 1).
    """
    # TODO(student): copy hr_violations and change 0.5 to 0.4.
    raise NotImplementedError("mutation_A is not implemented")


def mutation_B(grid: np.ndarray, atol: float = 1e-12) -> HRReport:
    """Mutation B: replace hbin by the constant log2(e) ≈ 1.4427.

    Check: bayes_error(p) <= 0.5 * log2(e)

    Expected: violations > 0 — the bound stops depending on
    bayes_error and so cannot hug the small-error regime.
    """
    # TODO(student): copy hr_violations and substitute log2(e) for hbin.
    raise NotImplementedError("mutation_B is not implemented")


def mutation_C(grid: np.ndarray, atol: float = 1e-12) -> HRReport:
    """Mutation C: pretend Bayes error is 2/3 (a uniform 3-class prior),
    keep the binary-entropy upper bound.

    Check: 2/3 <= 0.5 * hbin(2/3)  — should hold trivially?

    Expected: violations == 0 because the RHS now ignores p entirely,
    AND max_slack > 0.5 because the LHS is constant.

    This is the "uninformative" mutation: a verifier that always
    passes is not necessarily useful.
    """
    # TODO(student): return a report where lhs = 2/3 and rhs = 0.5 * hbin(2/3).
    raise NotImplementedError("mutation_C is not implemented")
