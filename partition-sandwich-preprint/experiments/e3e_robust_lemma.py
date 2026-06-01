"""
e3e_robust_lemma.py
====================

Empirical stress test of Lemma 6' (epsilon-robust MPNN-WL constancy)
on real graphs and a real GIN operator.

Setup.  Pick a graph G with its 1-WL partition Pi_L (degree init).  Pick a
fixed, randomly-initialised L-layer GIN with the standard PyG GINConv
operator and an MLP per round.  Inject Gaussian perturbations
  h^(0)_v <- h^(0)_v + xi_v,   xi_v iid N(0, delta_0^2 I_d).
Forward-propagate.  Measure, at each round l = 0..L:

  D(l) := max_{v ~_WL w} || h^(l)(v) - h^(l)(w) ||_2.

Lemma 6' predicts
  D(l) <= delta_l := delta_0 * prod_{k=1..l} L_k * (1 + Delta_max),
where L_k = ||W_k||_op for the linear part of the k-th update and
Delta_max = max vertex degree.

We sweep delta_0 in {0, 1e-3, 1e-2, 1e-1, 1.0} and report:
  (i)   absolute D(L) vs delta_L (the bound);
  (ii)  the looseness ratio  delta_L / D(L)  (>= 1 by the lemma);
  (iii) the implied effective propagation factor
        gamma_eff(l) := (D(l) / D(0))^(1/l), comparable to L_k (1+Delta).

This is a *quantitative* check that (a) the lemma holds in vivo, and
(b) it is loose by a measurable, dataset-dependent factor on real
sparse graphs.  No training is performed.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


# --------------------------------------------------------- WL ground truth
from e3_wl_bracket import load_cora, load_citeseer, wl_refine


def wl_partition(indptr, indices, init_colour, L):
    colours = init_colour.astype(np.uint64).copy()
    _, colours = np.unique(colours, return_inverse=True)
    colours = colours.astype(np.uint64)
    for _ in range(L):
        colours = wl_refine(colours, indptr, indices)
    return colours


# ----------------------------- max within-cell pair-distance, vectorised
def max_within_cell_diameter(H: np.ndarray, cells: np.ndarray) -> float:
    """max_{v ~ w (same cell)} ||h(v) - h(w)||_2, computed cell-by-cell.

    O(sum_C |C|^2 * d) which is fine when cells are mostly small (the
    expected regime on real graphs at moderate L).
    """
    max_d = 0.0
    for c in np.unique(cells):
        idx = np.where(cells == c)[0]
        if idx.size < 2:
            continue
        sub = H[idx]                      # |C| x d
        # diameter via pairwise; |C| typically small on real graphs
        diff = sub[:, None, :] - sub[None, :, :]
        d2 = np.einsum("ijk,ijk->ij", diff, diff)
        m = float(np.sqrt(d2.max()))
        if m > max_d:
            max_d = m
    return max_d


# ----------------------------------------------------- GIN forward (numpy)
def gin_forward(indptr, indices, X0, weights, eps_gin, deltas_record):
    """Numpy GIN forward: h^{l+1}_v = ReLU(W_l ( (1+eps) h_v + sum_{u in N(v)} h_u )).

    weights : list of (W, b) tuples, each W shape (d_in, d_out).
    Returns list of (l, H_l) for l = 0..L.
    """
    H = X0
    states = [(0, H)]
    for ell, (W, b) in enumerate(weights, start=1):
        # neighbour aggregation: agg_v = sum_{u in N(v)} h_u
        # vectorised via segment sums on CSR
        agg = np.zeros_like(H)
        # row indices for indices array
        nnz = indices.shape[0]
        seg_lengths = indptr[1:] - indptr[:-1]
        row_of_nbr = np.repeat(np.arange(H.shape[0]), seg_lengths)
        np.add.at(agg, row_of_nbr, H[indices])
        z = (1.0 + eps_gin) * H + agg              # GIN combine
        H = np.maximum(0.0, z @ W + b)             # ReLU MLP
        states.append((ell, H))
    return states


def op_norm(W: np.ndarray) -> float:
    """Spectral norm ||W||_2."""
    s = np.linalg.svd(W, compute_uv=False)
    return float(s[0])


# ----------------------------------------------------- experiment driver
def run_one(name: str, loader, L: int = 3, d_hidden: int = 32,
            seed: int = 0,
            deltas: tuple[float, ...] = (0.0, 1e-3, 1e-2, 1e-1, 1.0)
            ) -> dict:
    print(f"\n=== {name} ===", flush=True)
    nm, n, indptr, indices, y, init = loader()
    deg = (indptr[1:] - indptr[:-1]).astype(np.int64)
    Delta_max = int(deg.max())
    print(f"  n={n}, Delta_max={Delta_max}, L={L}, d_hidden={d_hidden}")

    # Build WL partition Pi_L using raw-degree init (matches E3)
    cells = wl_partition(indptr, indices, init, L)
    K = int(np.unique(cells).size)
    print(f"  Pi_L has K={K} cells "
          f"(singleton fraction {(np.bincount(cells)==1).mean():.3f})")

    # Initial feature: lift integer degree to a one-hot in d_hidden (truncated)
    # then add Gaussian noise of std delta_0 per coordinate.
    rng = np.random.default_rng(seed)
    d_in = d_hidden
    deg_clip = np.clip(deg, 0, d_in - 1)
    X_base = np.zeros((n, d_in), dtype=np.float64)
    X_base[np.arange(n), deg_clip] = 1.0           # exactly WL-consistent

    # Fixed GIN weights (Xavier-like); same across all delta_0 sweeps so
    # the only varying input is the noise level.
    weights = []
    for ell in range(L):
        W = rng.standard_normal((d_hidden, d_hidden)) * (1.0 / np.sqrt(d_hidden))
        b = np.zeros(d_hidden)
        weights.append((W, b))
    L_op = [op_norm(W) for W, _ in weights]
    eps_gin = 0.0
    prod_Lk = float(np.prod(L_op))
    bound_factor_per_round = [Lk * (1.0 + Delta_max) for Lk in L_op]
    # Lemma 6' predicted slack at depth l, per unit delta_0
    pred_unit = [1.0]
    for f in bound_factor_per_round:
        pred_unit.append(pred_unit[-1] * f)
    print(f"  L_op per round = {L_op}")
    print(f"  predicted unit-delta_0 envelope D(l)/delta_0 <= "
          f"{[f'{p:.2e}' for p in pred_unit]}")

    sweep = []
    for d0 in deltas:
        noise = rng.standard_normal(X_base.shape) * d0
        X0 = X_base + noise
        states = gin_forward(indptr, indices, X0, weights, eps_gin,
                             deltas_record=None)
        # Lemma 6' is stated for delta_0 := sup_{v ~ w} ||h^(0)(v) - h^(0)(w)||.
        # Measure it empirically from the realised X0, not from the per-coord
        # std parameter (which would understate it by sqrt(2*d_hidden) under
        # iid Gaussian noise).
        D0 = max_within_cell_diameter(X0, cells)
        rec = {"delta_0_param": d0,
               "delta_0": float(D0),
               "D": [max_within_cell_diameter(H, cells) for _, H in states],
               "delta_l_bound": [D0 * p for p in pred_unit],
               "looseness": [],
               "gamma_eff": []}
        for ell in range(L + 1):
            D = rec["D"][ell]
            B = rec["delta_l_bound"][ell]
            rec["looseness"].append(
                None if D <= 1e-12 else (B / D))
            if ell == 0 or rec["D"][0] <= 1e-12:
                rec["gamma_eff"].append(None)
            else:
                rec["gamma_eff"].append(
                    (rec["D"][ell] / rec["D"][0]) ** (1.0 / ell))
        sweep.append(rec)
        print(f"  delta_0_param={d0:.0e}  delta_0_meas={D0:.3e}  "
              f"D(L)={rec['D'][-1]:.3e}  "
              f"bound={rec['delta_l_bound'][-1]:.3e}  "
              f"loose_ratio={rec['looseness'][-1]}")

    return {"dataset": name, "n": n, "Delta_max": Delta_max, "L": L,
            "d_hidden": d_hidden, "K_cells": K,
            "L_op_per_round": L_op,
            "predicted_unit_envelope": pred_unit,
            "deltas": list(deltas),
            "sweep": sweep}


def main():
    out = {"experiment": "e3e_robust_lemma", "results": []}
    out["results"].append(run_one("cora", load_cora, L=3, d_hidden=32))
    out["results"].append(run_one("citeseer", load_citeseer, L=3, d_hidden=32))
    (RESULTS / "e3e.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {RESULTS / 'e3e.json'}")


if __name__ == "__main__":
    main()
