"""
e3_wl_bracket.py — Experiment 3: MPNN / WL bracket on real graphs.

For each graph G and each WL depth L = 0..L_max, compute the WL cell
of each vertex and bracket the empirical risk of every admissible
depth-L MPNN by H(f|Π_L).

Datasets (in execution order, stop early if budget runs out):
  1 Twitch-EN  (smoke, ~7k vertices, native binary label)
  2 Cora       (2.7k, multi-class → binarised "Neural_Networks" vs rest)
  3 CiteSeer   (3.3k)
  4 PubMed     (19.7k)
  5 ogbn-arxiv (169k, headline)

No GPU; no model training. Only the WL partition is built.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from common import W_STAR, bracket_from_cells

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)
DATA_DIR = HERE / "data";   DATA_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------- WL refinement (sparse)
def wl_refine(colours: np.ndarray, indptr: np.ndarray,
              indices: np.ndarray) -> np.ndarray:
    """
    One WL refinement round.
    colours[v] : current colour of vertex v (uint64)
    indptr, indices : CSR adjacency
    """
    n = len(colours)
    new = np.empty(n, dtype=np.uint64)
    for v in range(n):
        nbr = colours[indices[indptr[v]:indptr[v + 1]]]
        # sorted tuple of neighbour colours → canonical key
        nbr_sorted = np.sort(nbr)
        h = hashlib.blake2b(digest_size=8)
        h.update(int(colours[v]).to_bytes(8, "little", signed=False))
        h.update(nbr_sorted.tobytes())
        new[v] = int.from_bytes(h.digest(), "little")
    # canonicalise to dense ids 0..m-1
    uniq, inverse = np.unique(new, return_inverse=True)
    return inverse.astype(np.uint64)


def wl_funnel(indptr: np.ndarray, indices: np.ndarray,
              init_colour: np.ndarray, labels: np.ndarray,
              L_max: int) -> list[dict]:
    rows = []
    colours = init_colour.astype(np.uint64).copy()
    # remap initial
    _, colours = np.unique(colours, return_inverse=True)
    colours = colours.astype(np.uint64)
    prev_m = -1
    for L in range(L_max + 1):
        br = bracket_from_cells(colours, labels)
        rows.append({"L": L, **br.as_dict()})
        # stop if partition stable
        if br.m == prev_m and L > 0:
            print(f"    WL stable at L={L} (m={br.m}); padding remaining")
            for L2 in range(L + 1, L_max + 1):
                rows.append({"L": L2, **br.as_dict()})
            break
        prev_m = br.m
        if L < L_max:
            colours = wl_refine(colours, indptr, indices)
    return rows


# ----------------------------------------------------- dataset loaders
def _csr_from_edge_index(edge_index: np.ndarray, n: int):
    """Convert PyG (2, E) edge_index to CSR indptr/indices (undirected)."""
    import scipy.sparse as sp
    src, dst = edge_index
    data = np.ones(len(src), dtype=np.int8)
    A = sp.coo_matrix((data, (src, dst)), shape=(n, n)).tocsr()
    return A.indptr.astype(np.int64), A.indices.astype(np.int64)


def load_twitch_en():
    from torch_geometric.datasets import Twitch
    ds = Twitch(root=str(DATA_DIR / "Twitch"), name="EN")
    g = ds[0]
    n = g.num_nodes
    indptr, indices = _csr_from_edge_index(g.edge_index.numpy(), n)
    y = g.y.numpy().astype(np.int8)   # native binary
    # initial colour: degree-binned
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)
    init = deg
    return "twitch_en", n, indptr, indices, y, init


def _planetoid(name: str, positive_class_idx: int = 0):
    from torch_geometric.datasets import Planetoid
    ds = Planetoid(root=str(DATA_DIR / name), name=name)
    g = ds[0]
    n = g.num_nodes
    indptr, indices = _csr_from_edge_index(g.edge_index.numpy(), n)
    y_multi = g.y.numpy()
    y = (y_multi == positive_class_idx).astype(np.int8)
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)
    return name.lower(), n, indptr, indices, y, deg


def load_cora():     return _planetoid("Cora",     positive_class_idx=3)
def load_citeseer(): return _planetoid("CiteSeer", positive_class_idx=0)
def load_pubmed():   return _planetoid("PubMed",   positive_class_idx=1)


def load_ogbn_arxiv():
    from ogb.nodeproppred import PygNodePropPredDataset
    ds = PygNodePropPredDataset(name="ogbn-arxiv", root=str(DATA_DIR / "ogb"))
    g = ds[0]
    n = g.num_nodes
    indptr, indices = _csr_from_edge_index(g.edge_index.numpy(), n)
    y_multi = g.y.numpy().squeeze()
    # binarise: cs.LG = label 16 in ogbn-arxiv 40-class scheme
    y = (y_multi == 16).astype(np.int8)
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)
    return "ogbn_arxiv", n, indptr, indices, y, deg


# ----------------------------------------------------- driver
ALL_DATASETS = [
    ("twitch_en", load_twitch_en,  5),
    ("cora",      load_cora,        5),
    ("citeseer",  load_citeseer,    5),
    ("pubmed",    load_pubmed,      4),
    ("ogbn_arxiv", load_ogbn_arxiv, 3),
]


def funnel_figure(name: str, rows: list[dict]) -> None:
    Ls    = np.array([r["L"]        for r in rows])
    lower = np.array([r["lower"]    for r in rows])
    eps   = np.array([r["eps_star"] for r in rows])
    upper = np.array([r["upper"]    for r in rows])
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.fill_between(Ls, lower, upper, alpha=0.25, color="C0",
                    label="bracket")
    ax.plot(Ls, eps,   "o-", color="C0", label=r"$\varepsilon^*_{\Pi_L}$")
    ax.plot(Ls, lower, "v:", color="C2", label=r"$H_{\rm bin}^{-1}(H)$")
    ax.plot(Ls, upper, "^:", color="C3", label=r"$H/2$")
    ax.set_xlabel("WL depth $L$")
    ax.set_ylabel("error")
    ax.set_title(f"E3: WL bracket funnel — {name}")
    ax.legend(fontsize=8, framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / f"e3_{name}_funnel.pdf")
    plt.close(fig)


def evaluate(name: str, loader, L_max: int) -> dict:
    print(f"  [{name}] loading...", flush=True)
    t0 = time.perf_counter()
    nm, n, indptr, indices, y, init = loader()
    t_load = time.perf_counter() - t0
    pi = float(y.mean())
    print(f"    n={n}  E={len(indices)//2}  π={pi:.3f}  loaded in {t_load:.1f}s")

    t0 = time.perf_counter()
    rows = wl_funnel(indptr, indices, init, y, L_max)
    t_wl = time.perf_counter() - t0
    print(f"    WL funnel in {t_wl:.1f}s")

    # Gates
    Hs   = np.array([r["H"] for r in rows])
    eps  = np.array([r["eps_star"] for r in rows])
    lows = np.array([r["lower"] for r in rows])
    ups  = np.array([r["upper"] for r in rows])
    widths = ups - lows
    g = {
        "monotone_H":        bool(np.all(np.diff(Hs)   <= 1e-9)),
        "monotone_eps":      bool(np.all(np.diff(eps)  <= 1e-9)),
        "bracket_holds":     bool(np.all((lows - 1e-9 <= eps) & (eps <= ups + 1e-9))),
        "width_le_W_STAR":   bool(np.all(widths <= W_STAR + 1e-9)),
    }
    for L, r in enumerate(rows):
        print(f"      L={L}  m={r['m']:6d}  H={r['H']:.4f}  "
              f"lower={r['lower']:.4f}  ε*={r['eps_star']:.4f}  upper={r['upper']:.4f}")

    funnel_figure(name, rows)
    return {"name": name, "n_V": n, "n_E": len(indices) // 2, "pi": pi,
            "depths": rows, "gates": g,
            "t_load_s": t_load, "t_wl_s": t_wl}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None,
                    help="subset of dataset names to run")
    args = ap.parse_args()

    chosen = [t for t in ALL_DATASETS
              if (args.only is None or t[0] in args.only)]

    results = []
    for name, loader, L_max in chosen:
        try:
            results.append(evaluate(name, loader, L_max))
        except Exception as e:
            print(f"  [{name}] FAILED: {e}")
            results.append({"name": name, "error": str(e)})

    summary = {
        "experiment": "E3 WL bracket on real graphs",
        "datasets": results,
        "all_gates_pass": all(
            r.get("gates", {}).get("bracket_holds", False)
            and r.get("gates", {}).get("monotone_H", False)
            for r in results if "error" not in r
        ),
    }
    out = RESULTS / "e3.json"
    out.write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nwrote {out}")

    # Per-dataset gate enforcement
    for r in results:
        if "error" in r: continue
        g = r["gates"]
        assert g["bracket_holds"], f"{r['name']}: bracket violated"
        assert g["monotone_H"],    f"{r['name']}: H not monotone"
        assert g["width_le_W_STAR"], f"{r['name']}: width > W_STAR"
    print("gates: PASS")


if __name__ == "__main__":
    main()
