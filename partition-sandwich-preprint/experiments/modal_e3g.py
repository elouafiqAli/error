"""
modal_e3g.py
=============

Modal container wrapper for ``e3g_spectral_envelope.py``.

Usage (from ``partition-sandwich-preprint/experiments``):

    modal run modal_e3g.py

The function runs the CPU experiment in a clean Debian/Python container,
streams logs back, and writes ``results/e3g.json`` to the local repo.
"""

from __future__ import annotations

import json
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
REPO_RESULTS = HERE / "results"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "numpy==1.26.4",
        "scipy==1.13.1",
    )
    .add_local_python_source(
        "e3_wl_bracket",
        "e3e_robust_lemma",
        "e3g_spectral_envelope",
        "common",
    )
)

app = modal.App("phase4b-e3g-spectral-envelope", image=image)


@app.function(
    cpu=4.0,
    memory=8192,
    timeout=60 * 60,
)
def run_e3g() -> dict:
    """Execute the e3g sweep inside the container and return the JSON dict."""
    from e3g_spectral_envelope import main as e3g_main
    return e3g_main(out_path=Path("/tmp/e3g.json"))


@app.local_entrypoint()
def main() -> None:
    REPO_RESULTS.mkdir(exist_ok=True)
    print("[modal] launching phase4b-e3g-spectral-envelope ...", flush=True)
    out = run_e3g.remote()
    dest = REPO_RESULTS / "e3g.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"[modal] wrote {dest}")
