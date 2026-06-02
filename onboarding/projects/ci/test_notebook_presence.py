"""Presence checks for every HW / capstone notebook.

The full execution check is done by `make all` / `make modal-verify`
via nbclient. This file's pytest scope is just *file-level* sanity:
the notebook exists, is valid JSON-notebook, and (where applicable)
has a sibling solution notebook.

Tests for notebooks that haven't been authored yet are marked xfail
with a STRICT=False so the suite stays green during scaffolding.
"""
from __future__ import annotations

from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent  # onboarding/projects/

_HW_NBS = [
    ("hw1", _ROOT / "psets" / "hw1" / "hw1.ipynb"),
    ("hw2", _ROOT / "psets" / "hw2" / "hw2.ipynb"),
    ("hw3", _ROOT / "psets" / "hw3" / "hw3.ipynb"),
    ("hw4", _ROOT / "psets" / "hw4" / "hw4.ipynb"),
]
_M_NBS = [
    ("m1", _ROOT / "capstone" / "milestone1" / "m1.ipynb"),
    ("m2", _ROOT / "capstone" / "milestone2" / "m2.ipynb"),
    ("m3", _ROOT / "capstone" / "milestone3" / "m3.ipynb"),
    ("m4", _ROOT / "capstone" / "milestone4" / "m4.ipynb"),
    ("m5", _ROOT / "capstone" / "milestone5" / "m5.ipynb"),
    ("m6", _ROOT / "capstone" / "milestone6" / "m6_advanced.ipynb"),
]


def _check(path: Path) -> None:
    import nbformat as nbf
    assert path.exists(), f"missing notebook: {path}"
    nb = nbf.read(path, as_version=4)
    assert nb.cells, f"empty notebook: {path}"


@pytest.mark.parametrize("name,path", _HW_NBS, ids=[n for n, _ in _HW_NBS])
def test_hw_notebook_exists(name: str, path: Path) -> None:
    if not path.exists():
        pytest.xfail(f"{name} notebook not yet authored")
    _check(path)


@pytest.mark.parametrize("name,path", _M_NBS, ids=[n for n, _ in _M_NBS])
def test_capstone_notebook_exists(name: str, path: Path) -> None:
    if not path.exists():
        pytest.xfail(f"{name} notebook not yet authored")
    _check(path)


def test_solution_notebook_siblings_visible() -> None:
    """Per OCW doctrine: solutions are in-tree (not gitignored)."""
    nb_paths = [p for _, p in _HW_NBS + _M_NBS if p.exists()]
    for nb in nb_paths:
        sol = nb.with_name(nb.stem + "_solution.ipynb")
        if not sol.exists():
            pytest.xfail(f"solution sibling not yet authored: {sol.name}")
        _check(sol)
