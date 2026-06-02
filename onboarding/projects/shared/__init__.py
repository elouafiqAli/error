"""Shared canonical implementations for HW + Capstone notebooks.

This package is the *reference* (`pytest`-covered) implementation of
every primitive the notebooks ask the student to re-derive. The
notebooks remain the source of pedagogy; `shared/` is the source of
truth for unit tests and for Modal-side compute.
"""

from .partition import (
    Partition,
    label_partition,
    wl_refine,
    wl_partition,
)
from .bracket import (
    hbin,
    hbin_inverse,
    upper,
    lower,
    slack,
    verify,
    bracket_of,
)
from .aggregators import (
    sum_partition,
    mean_partition,
    max_partition,
)

__all__ = [
    "Partition",
    "label_partition",
    "wl_refine",
    "wl_partition",
    "hbin",
    "hbin_inverse",
    "upper",
    "lower",
    "slack",
    "verify",
    "bracket_of",
    "sum_partition",
    "mean_partition",
    "max_partition",
]
