"""
e3g_spectral_envelope.py
=========================

Phase 4b empirical companion to Lemma 6'' (`lem:mpnn-wl-spectral`).

For each (graph, depth-L) pair we measure on a fixed-init numpy GIN:

  (i)   per-graph spectral data:
          * worst-case degree   Delta = max_v |N(v)|
          * average degree      d_bar = (1/n) sum_v |N(v)|
          * adjacency Perron    lambda_max(A)
  (ii)  Lipschitz constants  L^c_l = L^m_l = ||W_l||_op  (sum-aggregator GIN,
        epsilon = 0)
  (iii) realised cell-spread at depth l = 0..L
          * D(l)        = max_{v sim_WL w} ||h(l)(v) - h(l)(w)||_2   (sup, (6''a))
          * delta_bar(l) = sum_v q_v  x(l)_v                          (mean, (6''b/c))
  (iv)  three closed-form envelopes (per delta_0 sweep)
          * (6')  delta_0 * prod_l ||W_l||_op * (1 + Delta)            -- worst-case degree
          * (6''c) delta_0 * prod_l ||W_l||_op * (1 + lambda_max(A))   -- Perron
          * (6''b) delta_0 * max_k | prod_l (||W_l|| + ||W_l|| * lambda_k(A)) |
                                                                       -- tight spectral

Output : ``results/e3g.json`` with one record per (dataset, L).
The Phase 4b audit row (A5b) goes LOW -> HIGH when this script's
per-graph (6''c) / (6') ratio is at least an order of magnitude
better than 1.0 on at least one real graph.

Runnable locally (CPU, ~minutes on the three Planetoid graphs) or via
``modal run modal_e3g.py`` for a clean reproducible container.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


# Reuse the existing planetoid loaders + WL refiner.
from e3_wl_bracket import load_cora, load_citeseer, load_pubmed, wl_refine
from e3e_robust_lemma import (
    wl_partition, gin_forward, op_norm, max_within_cell_diameter,
)


# ---------------------------------------------------- spectral quantities
def adjacency_csr(indptr: np.ndarray, indices: np.ndarray, n: int) -> sp.csr_matrix:
    data = np.ones(indices.shape[0], dtype=np.float64)
    return sp.csr_matrix((data, indices, indptr), shape=(n, n))


def perron_root(A: sp.csr_matrix) -> float:
    """Largest algebraic eigenvalue of the symmetric adjacency A."""
    # eigsh with which='LA' returns the largest algebraic eigenvalue.
    # For symmetric non-negative A this equals the Perron root.
    vals = spla.eigsh(A.astype(np.float64), k=1, which="LA",
                      return_eigenvectors=False, tol=1e-6, maxiter=2000)
    return float(vals[0])


def lambda_min(A: sp.csr_matrix) -> float:
    """Smallest algebraic eigenvalue of A (negative end of the spectrum)."""
    vals = spla.eigsh(A.astype(np.float64), k=1, which="SA",
                      return_eigenvectors=False, tol=1e-6, maxiter=2000)
    return float(vals[0])


# --------------------------------------------------- mass-weighted spread
def mass_weighted_within_cell_mean(
    H: np.ndarray, cells: np.ndarray, q: np.ndarray
) -> float:
    """sum_v q_v * x_v, with x_v = max_{w ~_WL v} ||H[v] - H[w]||_2.

    Implementation: per cell, compute the per-vertex sup-distance to its
    cellmates (this is the diameter when |C| >= 2, scaled by 1 not 1/2:
    x_v <= diameter(C)).  We use the cell diameter as a uniform upper
    bound on x_v for v in C (the bound the proof of (6''a) actually
    propagates).  The mass-weighted aggregate is then
    sum_C q(C) * diam(C).
    """
    total = 0.0
    n = H.shape[0]
    for c in np.unique(cells):
        idx = np.where(cells == c)[0]
        if idx.size < 2:
            continue
        sub = H[idx]
        diff = sub[:, None, :] - sub[None, :, :]
        d2 = np.einsum("ijk,ijk->ij", diff, diff)
        diam = float(np.sqrt(d2.max()))
        # q(C) = |C| / n  under the uniform vertex measure.
        total += (idx.size / n) * diam
    return total


# ----------------------------------------------------- experiment driver
def run_one(name: str, loader, L_max: int = 4, d_hidden: int = 32,
            seed: int = 0,
            deltas: tuple[float, ...] = (1e-3, 1e-2, 1e-1, 1.0)
            ) -> dict:
    print(f"\n=== {name} ===", flush=True)
    t0 = time.time()
    nm, n, indptr, indices, y, init = loader()
    deg = (indptr[1:] - indptr[:-1]).astype(np.int64)
    Delta = int(deg.max())
    d_bar = float(deg.mean())

    A = adjacency_csr(indptr, indices, n)
    print(f"  n={n}, |E|/2={A.nnz//2}, Delta={Delta}, d_bar={d_bar:.3f}", flush=True)
    t1 = time.time()
    lam_max = perron_root(A)
    lam_min = lambda_min(A)
    print(f"  lambda_max(A)={lam_max:.4f}, lambda_min(A)={lam_min:.4f}  "
          f"[eigsh in {time.time()-t1:.2f}s]", flush=True)

    # Fixed weights, reused across depths via prefix slicing.
    rng = np.random.default_rng(seed)
    weights = []
    for _ in range(L_max):
        W = rng.standard_normal((d_hidden, d_hidden)) * (1.0 / np.sqrt(d_hidden))
        b = np.zeros(d_hidden)
        weights.append((W, b))
    L_op = [op_norm(W) for W, _ in weights]
    eps_gin = 0.0
    print(f"  ||W_l||_op = {[f'{x:.3f}' for x in L_op]}", flush=True)

    # Base WL-consistent feature: one-hot of clipped degree, fixed.
    deg_clip = np.clip(deg, 0, d_hidden - 1)
    X_base = np.zeros((n, d_hidden), dtype=np.float64)
    X_base[np.arange(n), deg_clip] = 1.0

    per_depth: list[dict] = []
    for L in range(1, L_max + 1):
        print(f"  --- L={L} ---", flush=True)
        prod_W = float(np.prod(L_op[:L]))
        bound_deg = prod_W * (1.0 + Delta) ** L
        bound_per = prod_W * (1.0 + lam_max) ** L
        # Tight (6''b) bound: max over the spectrum.  We need a few extreme
        # eigenvalues to find max_k | prod_l (L_l)(1 + lambda_k) |.  Since
        # all L_l > 0 and prod is monotone in (1+lambda), the max over k is
        # attained at the eigenvalue maximising |1 + lambda_k|, which is
        # max(1 + lam_max, |1 + lam_min|) -- and since A is non-negative
        # lam_max >= 0 so (1 + lam_max) >= 1, while |1 + lam_min| <= 1 + |lam_min|.
        # For Perron-dominated graphs (lam_max >= |lam_min|), (6''b) collapses
        # to (6''c).  We report the looser of the two for honesty.
        spec_factor = max(1.0 + lam_max, abs(1.0 + lam_min))
        bound_spec = prod_W * spec_factor ** L

        # WL partition under the same init.
        cells = wl_partition(indptr, indices, init, L).astype(np.int64)
        K = int(np.unique(cells).size)
        singleton_frac = float((np.bincount(cells) == 1).mean())
        print(f"    Pi_L: K={K}, singleton_frac={singleton_frac:.3f}", flush=True)

        sweep: list[dict] = []
        for d0 in deltas:
            noise = rng.standard_normal(X_base.shape) * d0
            X0 = X_base + noise
            states = gin_forward(indptr, indices, X0, weights[:L], eps_gin,
                                 deltas_record=None)
            D0_meas = max_within_cell_diameter(X0, cells)
            delta_bar0 = mass_weighted_within_cell_mean(X0, cells,
                                                       q=np.full(n, 1.0/n))
            D_seq = [max_within_cell_diameter(H, cells) for _, H in states]
            dbar_seq = [mass_weighted_within_cell_mean(
                H, cells, q=np.full(n, 1.0/n)) for _, H in states]
            DL = D_seq[-1]
            dbarL = dbar_seq[-1]
            rec = {
                "delta_0_param": d0,
                "delta_0_meas": D0_meas,
                "delta_bar_0_meas": delta_bar0,
                "D_seq": D_seq,
                "delta_bar_seq": dbar_seq,
                "D_L": DL,
                "delta_bar_L": dbarL,
                # closed-form envelopes scaled by the measured delta_0 (sup):
                "bound_degree":  D0_meas * (1.0 + Delta) ** L * prod_W / prod_W,
                "bound_perron":  D0_meas * (1.0 + lam_max) ** L,
                "bound_spectral": D0_meas * spec_factor ** L,
                # rescaled to include the GIN Lipschitz product (for honesty):
                "bound_degree_full":  D0_meas * prod_W * (1.0 + Delta) ** L,
                "bound_perron_full":  D0_meas * prod_W * (1.0 + lam_max) ** L,
                "bound_spectral_full": D0_meas * prod_W * spec_factor ** L,
                # looseness ratios:
                "loose_degree":  (D0_meas * prod_W * (1.0 + Delta) ** L) / max(DL, 1e-30),
                "loose_perron":  (D0_meas * prod_W * (1.0 + lam_max) ** L) / max(DL, 1e-30),
                "loose_spectral": (D0_meas * prod_W * spec_factor ** L) / max(DL, 1e-30),
                # the per-graph (6''c) / (6') ratio (the key Phase-4b number):
                "perron_over_degree": ((1.0 + lam_max) / (1.0 + Delta)) ** L,
            }
            sweep.append(rec)
            print(f"    delta_0={d0:.0e}  D(L)={DL:.2e}  "
                  f"dbar(L)={dbarL:.2e}  "
                  f"bound_deg={rec['bound_degree_full']:.2e}  "
                  f"bound_perron={rec['bound_perron_full']:.2e}  "
                  f"ratio_perron/deg={rec['perron_over_degree']:.3e}",
                  flush=True)

        per_depth.append({
            "L": L,
            "K_cells": K,
            "singleton_frac": singleton_frac,
            "prod_W_op": prod_W,
            "bound_degree_unit_delta0": prod_W * (1.0 + Delta) ** L,
            "bound_perron_unit_delta0": prod_W * (1.0 + lam_max) ** L,
            "bound_spectral_unit_delta0": prod_W * spec_factor ** L,
            "perron_over_degree": ((1.0 + lam_max) / (1.0 + Delta)) ** L,
            "sweep": sweep,
        })

    elapsed = time.time() - t0
    print(f"  [done {name} in {elapsed:.1f}s]", flush=True)
    return {
        "dataset": name,
        "n": int(n),
        "m_edges_undirected": int(A.nnz // 2),
        "Delta": Delta,
        "d_bar": d_bar,
        "lambda_max_A": lam_max,
        "lambda_min_A": lam_min,
        "d_hidden": d_hidden,
        "L_op_per_round": L_op,
        "deltas": list(deltas),
        "per_depth": per_depth,
        "elapsed_s": elapsed,
    }


def main(out_path: Path | None = None) -> dict:
    out = {
        "experiment": "e3g_spectral_envelope",
        "phase": "P1 / Phase 4b",
        "schema_version": 1,
        "results": [],
    }
    out["results"].append(run_one("cora",     load_cora,     L_max=4))
    out["results"].append(run_one("citeseer", load_citeseer, L_max=4))
    out["results"].append(run_one("pubmed",   load_pubmed,   L_max=4))

    dest = out_path or (RESULTS / "e3g.json")
    dest.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {dest}")
    return out


if __name__ == "__main__":
    main()
