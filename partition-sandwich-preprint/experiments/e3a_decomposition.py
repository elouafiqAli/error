"""
e3a_decomposition.py
=====================

Structural-vs-memorisation decomposition (Angle A), cell-size x purity
fingerprint (Angle B), and coarsened-initial-colour rerun (Angle C, "E3c")
for the depth-L 1-WL bracket on the E3 benchmark suite.

Why this exists.  Reviewers correctly observe that on ogbn-arxiv the
depth-3 1-WL partition is near-discrete (m_3 / |V| = 0.956), so the
bracket's pinch is structural overfitting rather than a victory of the
bound.  Rather than just admitting the regime in prose, this script
*quantifies* it via three new per-benchmark statistics that the WL / MPNN
literature does not currently report:

  (A)  sigma(tau, rho) := (L_mem(rho) - L_star(tau)) / L_mem(rho)
       where  L_star(tau) := min { L : eps_star_{Pi_L} <= tau }
              L_mem(rho)  := min { L : m_L / |V|       >= rho }
       sigma -> 1: task is structurally learnable by 1-WL well before
       memorisation kicks in.  sigma <= 0: the bracket's apparent pinch
       is dominated by per-vertex memorisation.

  (B)  Per-cell scatter (|C|, min(p_C, 1-p_C)) at a chosen depth,
       exposing the cell-size x purity distribution that eps_star and
       H(f | Pi_L) integrate over.  Singletons collapse to the (1, 0)
       point and become visually separable from large pure cells.

  (C)  E3c: rerun the funnel with a *coarsened* initial colour
       h0_v = clip(floor(log2(deg_v + 1)), 0, K-1), K in {4, 8, 16}.
       Raw-integer-degree init is near-injective on the degree-skewed
       citation graphs; the coarsened init bounds the partition
       cardinality so the bracket measures structural informativeness of
       1-WL on the benchmark rather than the degree fingerprint.

All three are CPU-only.  Reuses ``e3_wl_bracket.wl_funnel`` and the
existing dataset loaders.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from common import bracket_from_cells
from e3_wl_bracket import (
    ALL_DATASETS,
    wl_funnel,
    wl_refine,
)

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGURES = HERE / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


# ------------------------------------------------------- Angle A: sigma index
def saturation_depths(rows: list[dict], n: int,
                      taus: tuple[float, ...],
                      rhos: tuple[float, ...]) -> dict:
    """L*(tau), L_mem(rho), sigma(tau, rho) from a funnel."""
    Ls = np.array([r["L"] for r in rows])
    eps = np.array([r["eps_star"] for r in rows])
    m = np.array([r["m"] for r in rows])
    frac = m / n

    def first_below(arr, thr):
        idx = np.where(arr <= thr)[0]
        return int(Ls[idx[0]]) if idx.size else None

    def first_above(arr, thr):
        idx = np.where(arr >= thr)[0]
        return int(Ls[idx[0]]) if idx.size else None

    L_star = {f"{t:g}": first_below(eps, t) for t in taus}
    L_mem = {f"{r:g}": first_above(frac, r) for r in rhos}

    sigma = {}
    for t in taus:
        for r in rhos:
            ls = L_star[f"{t:g}"]
            lm = L_mem[f"{r:g}"]
            if ls is None or lm is None or lm == 0:
                sigma[f"tau={t:g},rho={r:g}"] = None
            else:
                sigma[f"tau={t:g},rho={r:g}"] = float((lm - ls) / lm)
    return {"L_star": L_star, "L_mem": L_mem, "sigma": sigma}


# --------------------------------------------- Angle B: cell-size x purity
def cell_purity_scatter(colours: np.ndarray,
                        labels: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return per-cell (size, impurity) where impurity = min(p, 1-p)."""
    cells, inv = np.unique(colours, return_inverse=True)
    K = cells.size
    sizes = np.bincount(inv, minlength=K).astype(np.int64)
    ones = np.bincount(inv, weights=labels.astype(np.float64), minlength=K)
    p1 = ones / np.maximum(sizes, 1)
    impurity = np.minimum(p1, 1.0 - p1)
    return sizes, impurity


def render_purity_scatter(name: str, L: int, sizes: np.ndarray,
                          impurity: np.ndarray, n: int) -> None:
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    # singletons get a small jitter on y for visibility
    jitter = (impurity == 0) & (sizes == 1)
    color = np.where(jitter, "C7", "C0")
    # for legibility marker area ~ cell weight (size / n)
    area = np.clip(40 * np.sqrt(sizes / max(n, 1)), 3.0, 200.0)
    ax.scatter(sizes, impurity, s=area, alpha=0.55,
               c=color, edgecolors="none")
    ax.set_xscale("log")
    ax.set_xlabel("cell size |C| (log)")
    ax.set_ylabel(r"impurity $\min(p_C, 1-p_C)$")
    ax.set_title(f"E3 cell scatter: {name}, L={L}  "
                 f"(K={sizes.size}, singletons={int((sizes==1).sum())})")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / f"e3a_purity_{name}_L{L}.pdf")
    plt.close(fig)


# --------------------------------------------- Angle C: coarsened init
def coarsened_init(deg: np.ndarray, K: int) -> np.ndarray:
    """h0_v = clip(floor(log2(deg + 1)), 0, K-1)."""
    return np.clip(np.floor(np.log2(deg + 1)).astype(np.int64),
                   0, K - 1).astype(np.uint64)


# ----------------------------------------------------------------- driver
def run() -> dict:
    taus = (0.01, 0.05, 0.10)
    rhos = (0.50, 0.75, 0.90)
    out = {"experiment": "e3a_decomposition",
           "taus": list(taus), "rhos": list(rhos),
           "datasets": []}

    for name, loader, L_max in ALL_DATASETS:
        print(f"\n=== {name} ===", flush=True)
        t0 = time.perf_counter()
        nm, n, indptr, indices, y, init = loader()
        t_load = time.perf_counter() - t0
        print(f"  loaded in {t_load:.1f}s   n={n}  pi={float(y.mean()):.4f}")

        # ---- (A) sigma index from native (degree) funnel
        rows_native = wl_funnel(indptr, indices, init, y, L_max)
        sigma_native = saturation_depths(rows_native, n, taus, rhos)

        # ---- (B) scatter at chosen depth = min(L_max, 2)
        L_show = min(L_max, 2)
        colours = init.astype(np.uint64).copy()
        _, colours = np.unique(colours, return_inverse=True)
        colours = colours.astype(np.uint64)
        for _ in range(L_show):
            colours = wl_refine(colours, indptr, indices)
        sizes, imp = cell_purity_scatter(colours, y)
        render_purity_scatter(name, L_show, sizes, imp, n)
        n_singleton = int((sizes == 1).sum())
        n_largepure = int(((sizes >= 16) & (imp <= 0.05)).sum())
        n_largemix = int(((sizes >= 16) & (imp > 0.05)).sum())

        # ---- (C) coarsened-init reruns at K in {4, 8, 16}
        # only meaningful for graphs where the native init is degree
        # (== identity over uint64); we apply uniformly for comparability
        # because all the E3 datasets use degree as h0.
        deg = (indptr[1:] - indptr[:-1]).astype(np.int64)
        coarsened = {}
        for K in (4, 8, 16):
            init_c = coarsened_init(deg, K)
            rows_c = wl_funnel(indptr, indices, init_c, y, L_max)
            sig_c = saturation_depths(rows_c, n, taus, rhos)
            # peak information ratio I(f; Pi_L) / log2(|Pi_L|)
            # using I(f; Pi_L) = H_bin(pi) - H(f | Pi_L)
            pi = float(y.mean())
            H_bin = (-pi * np.log2(pi) - (1 - pi) * np.log2(1 - pi)
                     if 0.0 < pi < 1.0 else 0.0)
            info_ratio = []
            for r in rows_c:
                Hc = r["H"]  # H(f | Pi_L) in bits
                K_part = max(r["m"], 1)
                denom = np.log2(K_part) if K_part > 1 else 1.0
                info_ratio.append((H_bin - Hc) / denom)
            coarsened[str(K)] = {
                "depths": rows_c,
                "sigma": sig_c,
                "max_info_ratio": float(max(info_ratio)),
                "argmax_L": int(np.argmax(info_ratio)),
            }

        out["datasets"].append({
            "name": name,
            "n": n,
            "pi": float(y.mean()),
            "L_max": L_max,
            "native": {
                "depths": rows_native,
                "sigma": sigma_native,
            },
            "scatter_L": L_show,
            "scatter_summary": {
                "K": int(sizes.size),
                "n_singletons": n_singleton,
                "n_large_pure_ge16_imp_le0.05": n_largepure,
                "n_large_mix_ge16_imp_gt0.05": n_largemix,
                "frac_singletons": n_singleton / max(sizes.size, 1),
            },
            "coarsened": coarsened,
        })

    (RESULTS / "e3a.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {RESULTS / 'e3a.json'}")
    return out


if __name__ == "__main__":
    run()
