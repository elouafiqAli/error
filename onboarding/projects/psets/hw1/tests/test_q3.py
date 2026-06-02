"""HW1 Q3 unit tests — read-only."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from onboarding.projects.psets.hw1.starter.q3_hr_verifier import (
    hr_violations,
    plot_envelope,
)


def _report():
    grid = np.linspace(0.0, 1.0, 10_001)
    return hr_violations(grid)


def test_no_violations():
    r = _report()
    assert r["violations"] == 0


def test_max_slack_is_loose_but_bounded():
    r = _report()
    assert 0.10 < r["max_slack"] < 0.20


def test_argmax_inside_left_half():
    r = _report()
    assert 0.0 < r["argmax_p"] < 0.5


def test_plot_envelope_writes_file(tmp_path: Path):
    out = tmp_path / "envelope.png"
    plot_envelope(out)
    assert out.exists()
    assert out.stat().st_size > 0
