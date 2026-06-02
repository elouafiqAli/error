"""HW1 Q3.2 + Q3.3 — Hellman–Raviv verifier and envelope plot.

This is the warm-up for the T1 verifier you will build in HW3. The
shape (loop over a grid, count violations, report max slack) is the
same; only the inequality changes.
"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import numpy as np

# Relative imports from the same starter/ package — student fills in
# q1_hbin and q2_bayes first.
from .q1_hbin import hbin
from .q2_bayes import bayes_error


class HRReport(TypedDict):
    n: int
    violations: int
    max_slack: float
    argmax_p: float


def hr_violations(grid: np.ndarray, atol: float = 1e-12) -> HRReport:
    """Check the Hellman–Raviv inequality on a grid of p-values.

    For each ``p`` in ``grid``, compute
        lhs = bayes_error(p)
        rhs = 0.5 * hbin(bayes_error(p))
    and report:
      - violations: count of grid points with lhs > rhs + atol
      - max_slack:  max over the grid of (rhs - lhs)
      - argmax_p:   the p attaining max_slack

    Parameters
    ----------
    grid : np.ndarray
        1-D array of p-values in [0, 1].
    atol : float
        Tolerance for the violation check (default 1e-12).

    Returns
    -------
    HRReport
        Dict with keys n, violations, max_slack, argmax_p.
    """
    # TODO(student): ~10 lines.
    #
    # Hints:
    #  - vectorise: build `eps = np.array([bayes_error(p) for p in grid])`
    #    and `rhs = 0.5 * np.array([hbin(e) for e in eps])`,
    #  - or stay scalar in a loop — both pass the test.
    #  - argmax_p = grid[np.argmax(rhs - eps)].
    raise NotImplementedError("hr_violations is not implemented")


def plot_envelope(out_path: Path) -> None:
    """Plot epsilon(p) and 0.5 * hbin(epsilon(p)) over p in [0, 1].

    Writes a PNG to out_path. Required elements:
      - two curves
      - vertical dashed line at argmax_p
      - legend, axis labels, title

    Parameters
    ----------
    out_path : Path
        Where to write the PNG.
    """
    # TODO(student): ~15 lines using matplotlib.
    raise NotImplementedError("plot_envelope is not implemented")


if __name__ == "__main__":
    grid = np.linspace(0.0, 1.0, 10_001)
    report = hr_violations(grid)
    print(report)
    out = Path(__file__).resolve().parents[2] / "plots" / "hw1_q3_envelope.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    plot_envelope(out)
    print(f"wrote {out}")
