"""Unit tests for the reflect.py helper."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from onboarding.projects import reflect


def test_log_requires_start(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(reflect, "_state", {"notebook": None, "store": tmp_path / "x.jsonl"})
    with pytest.raises(RuntimeError):
        reflect.log("c", "claim", "HIGH")


def test_log_appends_entries(tmp_path: Path) -> None:
    store = tmp_path / "ref.jsonl"
    reflect.start(notebook="hw_test", store=store)
    reflect.log("hbin", "Hbin is concave on [0,1]", "HIGH")
    reflect.log("hr", "HR is tight at uniform binary", "MEDIUM")
    rows = reflect.dump(store)
    assert len(rows) == 2
    assert rows[0]["concept"] == "hbin"
    assert rows[1]["level"] == "MEDIUM"
    assert all(r["notebook"] == "hw_test" for r in rows)
    # JSONL well-formed
    for line in store.read_text().splitlines():
        json.loads(line)


def test_log_rejects_bogus_level(tmp_path: Path) -> None:
    reflect.start(notebook="hw_test", store=tmp_path / "r.jsonl")
    with pytest.raises(ValueError):
        reflect.log("x", "y", "MAYBE")  # type: ignore[arg-type]


def test_render_capstone_writes_notebook(tmp_path: Path) -> None:
    store = tmp_path / "r.jsonl"
    reflect.start(notebook="hw1", store=store)
    reflect.log("hbin", "concave", "HIGH")
    reflect.start(notebook="hw2", store=store)
    reflect.log("wl", "1-WL stuck on C6 vs 2K3", "MEDIUM")
    target = tmp_path / "out" / "m5.ipynb"
    reflect.render_capstone(store=store, target_path=target)
    assert target.exists()
    import nbformat as nbf
    nb = nbf.read(target, as_version=4)
    src = "\n".join(c.source for c in nb.cells)
    assert "hw1" in src and "hw2" in src
    assert "HIGH" in src and "MEDIUM" in src
