#!/usr/bin/env python3
"""anchor_real_data_full.py — D.10: cell-level real-data anchor for
Paper B's C-Sh AND C-Va AND C-Pi instances on five graph datasets.

Lifts the honest limitation of D.9 (anchor_real_data.py): the earlier
script could only verify the Shannon instance because Paper A's
e3.json stores only summary `(H, eps_star)` per (dataset, depth).
D.10 closes the gap by re-running the 1-WL refinement here and
extracting cell-level (q_C, P_C) directly, so all three Paper B
T3 instances (Shannon, variance, Pinsker) can be anchored against
the SAME real partition and the SAME real Bayes error.

Discipline mantra. Zero new training. The WL refinement is a pure
graph-structural computation; the labels come from the dataset.
The script invokes Paper A's own loaders and WL kernel
(`partition-sandwich-preprint/experiments/e3_wl_bracket.py`), then
applies Paper B's C-Sh / C-Va / C-Pi closed forms.

Contract per (dataset, depth):
    * Shannon  (C-Sh): H_bin^{-1}(H) <= eps_star <= H / 2
    * Variance (C-Va): (1 - sqrt(1 - 4 Phi_V)) / 2 <= eps_star <= 2 Phi_V
                       where Phi_V := sum_C q_C * eta_C(1 - eta_C)
    * Pinsker  (C-Pi): max(0, 1/2 - 1/2 sqrt(ln4 * (1 - H))) <= eps_star
                       (replaces Shannon lower when H is small)

The Pinsker lower can be vacuous (negative before clipping); we
record both the raw value and the clipped envelope.

Output: audit/anchor_real_data_full.json with per-row brackets and a
top-level `all_pass` boolean. Exit code 0 iff every row passes every
applicable contract.

Usage:
    python3 audit/anchor_real_data_full.py [--datasets cora citeseer ...]
                                           [--depths 0 1 2 3]
                                           [--manifest audit/anchor_real_data_full.json]
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time
from typing import Any

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
PAPER_A_EXP = ROOT.parent / "partition-sandwich-preprint" / "experiments"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PAPER_A_EXP))

# Paper B primitives (machine-checked at v0.1.0-paperB-G2 + audit/stress.py).
from verify_b_t1 import _h_bin, _h_bin_inv_on_lower_half  # noqa: E402

# Paper A real-data loaders + WL refinement.
try:
    from e3_wl_bracket import (  # noqa: E402
        wl_refine,
        load_cora,
        load_citeseer,
        load_pubmed,
        load_twitch_en,
        load_ogbn_arxiv,
    )
except Exception as e:
    print(f"FATAL: could not import Paper A loaders: {e}", file=sys.stderr)
    sys.exit(2)


LOADERS = {
    "cora": load_cora,
    "citeseer": load_citeseer,
    "pubmed": load_pubmed,
    "twitch_en": load_twitch_en,
    "ogbn_arxiv": load_ogbn_arxiv,
}

# Tolerances.
TOL_BRACKET = 1.0e-9   # eps^* must lie inside [lower, upper], modulo float noise


# ----- Paper B C-Sh / C-Va / C-Pi closed forms -----------------------------
def c_sh(H: float, eps_star: float) -> dict[str, Any]:
    lo = _h_bin_inv_on_lower_half(H)
    up = 0.5 * H
    return {
        "lower": lo,
        "upper": up,
        "ok": (lo <= eps_star + TOL_BRACKET) and (eps_star <= up + TOL_BRACKET),
    }


def c_va(eta: np.ndarray, q: np.ndarray, eps_star: float) -> dict[str, Any]:
    """C-Va: phi(eta) = eta(1-eta). T3 lower via phi^{-1} on [0, 1/2],
    T3 upper via c_phi = 2."""
    phi = float(np.sum(q * eta * (1.0 - eta)))
    # phi^{-1} on [0, 1/2]: solve eta(1-eta) = phi  =>  eta = (1 - sqrt(1 - 4 phi))/2
    arg = 1.0 - 4.0 * phi
    arg = max(arg, 0.0)  # numerical floor (phi <= 1/4 always, but clamp)
    lo = 0.5 * (1.0 - math.sqrt(arg))
    up = 2.0 * phi
    return {
        "phi_V": phi,
        "lower": lo,
        "upper": up,
        "ok": (lo <= eps_star + TOL_BRACKET) and (eps_star <= up + TOL_BRACKET),
    }


def c_pi(H: float, eps_star: float) -> dict[str, Any]:
    """C-Pi: Pinsker lower 1/2 - 1/2 sqrt(ln4 (1-H)). Vacuous if negative."""
    arg = math.log(4.0) * (1.0 - max(0.0, min(1.0, H)))
    raw_lower = 0.5 - 0.5 * math.sqrt(max(0.0, arg))
    clipped = max(0.0, raw_lower)
    # contract: clipped lower must envelope eps_star (vacuous when 0)
    ok = clipped <= eps_star + TOL_BRACKET
    return {
        "raw_lower": raw_lower,
        "clipped_lower": clipped,
        "vacuous": raw_lower < 0.0,
        "ok": ok,
    }


# ----- helpers -------------------------------------------------------------
def _cells_at_depth(indptr, indices, init_colour, depth: int) -> np.ndarray:
    """Run wl_refine `depth` times from init_colour; return per-vertex cell id."""
    colours = init_colour.astype(np.uint64).copy()
    _, colours = np.unique(colours, return_inverse=True)
    colours = colours.astype(np.uint64)
    for _ in range(depth):
        colours = wl_refine(colours, indptr, indices)
    _, dense = np.unique(colours, return_inverse=True)
    return dense.astype(np.int64)


def _cell_stats(cell_ids: np.ndarray, labels: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (q, P, eta) per cell. eta_C := min(P_C, 1 - P_C)."""
    n = labels.shape[0]
    m = int(cell_ids.max()) + 1
    sums = np.bincount(cell_ids, weights=labels.astype(np.float64), minlength=m)
    counts = np.bincount(cell_ids, minlength=m).astype(np.float64)
    P = sums / counts
    q = counts / n
    eta = np.minimum(P, 1.0 - P)
    return q, P, eta


def _row(name: str, L: int, q: np.ndarray, P: np.ndarray, eta: np.ndarray) -> dict[str, Any]:
    n = int(q.size and round(1.0 / max(q.min(), 1e-300)))  # not used; placeholder
    # Real quantities:
    eps_star = float(np.sum(q * eta))
    H = float(np.sum(q * np.fromiter(
        (_h_bin(float(p)) for p in P), dtype=np.float64, count=P.size,
    )))
    sh = c_sh(H, eps_star)
    va = c_va(eta, q, eps_star)
    pi = c_pi(H, eps_star)
    all_ok = sh["ok"] and va["ok"] and pi["ok"]
    return {
        "dataset": name,
        "L": L,
        "n_cells": int(q.size),
        "H": H,
        "eps_star": eps_star,
        "C_Sh": sh,
        "C_Va": va,
        "C_Pi": pi,
        "status": "pass" if all_ok else "fail",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--datasets", nargs="*", default=list(LOADERS.keys()),
                    choices=list(LOADERS.keys()))
    ap.add_argument("--depths", type=int, nargs="*", default=[0, 1, 2, 3])
    ap.add_argument("--manifest", default=str(HERE / "anchor_real_data_full.json"))
    args = ap.parse_args(argv)

    all_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    t0 = time.time()

    for name in args.datasets:
        loader = LOADERS[name]
        print(f"=== {name} ===", flush=True)
        try:
            ld = loader()
        except Exception as e:
            print(f"  SKIP loader failed: {type(e).__name__}: {e}", file=sys.stderr)
            skipped.append({"dataset": name, "error": f"{type(e).__name__}: {e}"})
            continue
        # loader returns either (name, n, indptr, indices, y, deg) tuple
        # or a dict; normalise:
        if isinstance(ld, dict):
            n = ld["n"]; indptr = ld["indptr"]; indices = ld["indices"]
            y = ld["y"]; deg = ld["deg"]
        else:
            _, n, indptr, indices, y, deg = ld
        init = deg.astype(np.uint64)
        for L in args.depths:
            cells = _cells_at_depth(indptr, indices, init, L)
            q, P, eta = _cell_stats(cells, y)
            row = _row(name, L, q, P, eta)
            status = row["status"]
            print(f"  L={L} m={row['n_cells']} eps*={row['eps_star']:.4f} "
                  f"C-Sh:{row['C_Sh']['ok']} C-Va:{row['C_Va']['ok']} "
                  f"C-Pi:{row['C_Pi']['ok']}{'  (Pi vacuous)' if row['C_Pi']['vacuous'] else ''} "
                  f"{status.upper()}")
            all_rows.append(row)

    wall = time.time() - t0
    n_total = len(all_rows)
    n_fail = sum(1 for r in all_rows if r["status"] != "pass")
    manifest = {
        "experiment": "D.10 real-data cell-level anchor (Paper B C-Sh + C-Va + C-Pi)",
        "datasets_requested": args.datasets,
        "datasets_seen": sorted({r["dataset"] for r in all_rows}),
        "skipped": skipped,
        "depths": args.depths,
        "wall_s": wall,
        "n_rows": n_total,
        "n_failures": n_fail,
        "all_pass": n_fail == 0,
        "tolerances": {"TOL_BRACKET": TOL_BRACKET},
        "rows": all_rows,
    }
    out = pathlib.Path(args.manifest)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, default=float))

    print(f"\nwrote {out}")
    print(f"datasets: {manifest['datasets_seen']}  rows: {n_total}  failures: {n_fail}  wall: {wall:.1f}s")
    if skipped:
        print(f"skipped: {[s['dataset'] for s in skipped]}")
    print("OVERALL:", "PASS" if manifest["all_pass"] else "FAIL")
    return 0 if manifest["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
