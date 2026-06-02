"""Local CPU mirror of modal_app — exact same training functions.

When `modal` is not installed (e.g. CI runner, offline use), the
HW + capstone notebooks fall back to these CPU implementations so
the *gate* assertions still fire — just slower.
"""
from __future__ import annotations

from typing import Any

from onboarding.projects.modal_app import (
    _train_gcn_impl,
    _nas_sweep_impl,
)


def ping() -> str:
    return "pong (local)"


def train_gcn(**kwargs: Any) -> dict[str, Any]:
    return _train_gcn_impl(**kwargs)


def nas_sweep(**kwargs: Any) -> dict[str, Any]:
    return _nas_sweep_impl(**kwargs)


__all__ = ["ping", "train_gcn", "nas_sweep"]
