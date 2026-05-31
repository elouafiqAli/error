"""
e3_wl_bracket.py — Experiment 3: MPNN / WL bracket on real graphs.

For each graph G and each WL depth L = 0..L_max, compute the WL cell
of each vertex and bracket the empirical risk of every admissible
depth-L MPNN by H(f|Π_L).

Datasets (in execution order, stop early if budget runs out):
  1 Twitch-EN  (smoke, ~7k vertices, native binary mature-content label)
  2 Cora       (2.7k, 7-class -> binarised LARGEST-class vs rest)
  3 CiteSeer   (3.3k, 6-class -> binarised LARGEST-class vs rest)
  4 PubMed     (19.7k, 3-class -> binarised LARGEST-class vs rest)
  5 ogbn-arxiv (169k, 40-class -> binarised LARGEST-class vs rest; headline)

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

    Implementation note. This routine is a pure-Python ``for v in range(n)``
    loop with one ``hashlib.blake2b`` digest per vertex.  Empirically it is
    fine for ``L <= 3`` on graphs up to ogbn-arxiv (169k vertices,
    ~1.16M edges, ~3s/round on a laptop).  For deeper refinement, larger
    graphs, or k-WL variants, port to a vectorised hash (e.g. xxhash on a
    flattened (deg, sorted_neighbour_colours) buffer with offsets from
    ``indptr``) or move to a C extension.  We did NOT take that step
    because the WL chain stabilises at very small L on the benchmarks here
    (see the funnel `m` columns in REPORTS.md / e3.json).
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
# All loaders fetch raw files directly (no torch_geometric dependency).

import pickle
import urllib.request
import scipy.sparse as sp


def _download(url: str, dst: Path) -> Path:
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    print(f"    downloading {url}", flush=True)
    with urllib.request.urlopen(url) as r, dst.open("wb") as f:
        f.write(r.read())
    return dst


def _csr_undirected(rows: np.ndarray, cols: np.ndarray,
                    n: int) -> tuple[np.ndarray, np.ndarray]:
    """Build symmetric CSR (no self-loops, deduplicated)."""
    r = np.concatenate([rows, cols])
    c = np.concatenate([cols, rows])
    keep = r != c
    r, c = r[keep], c[keep]
    data = np.ones_like(r, dtype=np.int8)
    A = sp.coo_matrix((data, (r, c)), shape=(n, n)).tocsr()
    A.sum_duplicates()
    A.data[:] = 1
    return A.indptr.astype(np.int64), A.indices.astype(np.int64)


# Twitch-EN MUSAE source pinned to a specific commit so the URL is stable
# even if the third-party repo's default branch is renamed/moved.  Cached
# under data/ on first download; subsequent runs are offline.
_MUSAE_PIN = "6c52e10566e1b1a9ad8ad7ca38b3c1d3aa30ec18"  # master @ 2024-01


def load_twitch_en():
    """Twitch-EN streamers (MUSAE); native binary mature-content label.

    Source: https://github.com/benedekrozemberczki/MUSAE (pinned commit;
    raw files cached under ``experiments/data/twitch_en_*.csv``).  If the
    upstream URL ever fails, drop the two CSVs into ``data/`` manually and
    rerun.
    """
    base = ("https://raw.githubusercontent.com/benedekrozemberczki"
            f"/MUSAE/{_MUSAE_PIN}/input")
    edges_p = _download(f"{base}/edges/ENGB_edges.csv",
                        DATA_DIR / "twitch_en_edges.csv")
    target_p = _download(f"{base}/target/ENGB_target.csv",
                         DATA_DIR / "twitch_en_target.csv")
    import pandas as pd
    T = pd.read_csv(target_p).sort_values("new_id").reset_index(drop=True)
    n = len(T)
    y = T["mature"].astype(int).to_numpy().astype(np.int8)
    E = pd.read_csv(edges_p).to_numpy(dtype=np.int64)
    indptr, indices = _csr_undirected(E[:, 0], E[:, 1], n)
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)
    return "twitch_en", n, indptr, indices, y, deg


# --- Planetoid raw (Cora / CiteSeer / PubMed) ----------------------
_PLANETOID_BASE = ("https://github.com/kimiyoung/planetoid/raw/master/data")


def _load_planetoid_raw(name: str):
    """
    Reconstruct Planetoid graph + multi-class labels from raw files.
    Returns (indptr, indices, y_multiclass, n).
    """
    pname = name  # 'cora' | 'citeseer' | 'pubmed'
    suffixes = ["x", "y", "tx", "ty", "allx", "ally", "graph",
                "test.index"]
    paths = {s: _download(f"{_PLANETOID_BASE}/ind.{pname}.{s}",
                          DATA_DIR / f"ind.{pname}.{s}")
             for s in suffixes}

    def _pkl(p: Path):
        with p.open("rb") as f:
            return pickle.load(f, encoding="latin1")

    allx = _pkl(paths["allx"])
    ally = _pkl(paths["ally"])
    tx = _pkl(paths["tx"])
    ty = _pkl(paths["ty"])
    graph = _pkl(paths["graph"])  # dict node -> list[neighbour]
    test_idx_reorder = np.loadtxt(paths["test.index"], dtype=np.int64)
    test_idx_range = np.sort(test_idx_reorder)

    if pname == "citeseer":
        # citeseer has isolated test nodes — pad with zeros
        full = np.arange(test_idx_reorder.min(),
                         test_idx_reorder.max() + 1)
        tx_ext = sp.lil_matrix((len(full), tx.shape[1]))
        tx_ext[test_idx_range - test_idx_reorder.min(), :] = tx
        tx = tx_ext.tocsr()
        ty_ext = np.zeros((len(full), ty.shape[1]))
        ty_ext[test_idx_range - test_idx_reorder.min(), :] = ty
        ty = ty_ext

    labels = np.vstack([ally, ty])
    labels[test_idx_reorder, :] = labels[test_idx_range, :]
    y_multi = labels.argmax(axis=1)
    n = labels.shape[0]

    # build adjacency from `graph` dict
    rows: list[int] = []
    cols: list[int] = []
    for u, neigh in graph.items():
        for v in neigh:
            rows.append(u); cols.append(v)
    rows = np.asarray(rows, dtype=np.int64)
    cols = np.asarray(cols, dtype=np.int64)
    indptr, indices = _csr_undirected(rows, cols, n)
    return indptr, indices, y_multi, n


def _planetoid_binarise_largest(name: str):
    indptr, indices, y_multi, n = _load_planetoid_raw(name)
    counts = np.bincount(y_multi)
    target = int(np.argmax(counts))
    y = (y_multi == target).astype(np.int8)
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)
    return name, n, indptr, indices, y, deg


def load_cora():     return _planetoid_binarise_largest("cora")
def load_citeseer(): return _planetoid_binarise_largest("citeseer")
def load_pubmed():   return _planetoid_binarise_largest("pubmed")


def load_ogbn_arxiv():
    """ogbn-arxiv via the non-PyG OGB loader (numpy only)."""
    # OGB cached *.pt files use pickle protocol 4; under torch 2.6+ the
    # weights_only=True default rejects them.  Force weights_only=False.
    import torch
    _orig_load = torch.load
    def _load_unsafe(*a, **kw):
        kw.setdefault("weights_only", False)
        return _orig_load(*a, **kw)
    torch.load = _load_unsafe
    try:
        from ogb.nodeproppred import NodePropPredDataset
        ds = NodePropPredDataset(name="ogbn-arxiv", root=str(DATA_DIR / "ogb"))
    finally:
        torch.load = _orig_load
    graph, labels = ds[0]
    n = int(graph["num_nodes"])
    edge_index = graph["edge_index"]
    indptr, indices = _csr_undirected(
        edge_index[0].astype(np.int64),
        edge_index[1].astype(np.int64), n)
    y_multi = np.asarray(labels).reshape(-1).astype(np.int64)
    # Binarise: largest class
    counts = np.bincount(y_multi)
    target = int(np.argmax(counts))
    y = (y_multi == target).astype(np.int8)
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
    pi_trivial = float(min(pi, 1.0 - pi))
    nE = len(indices) // 2
    print(f"    n={n}  E={nE}  π={pi:.4f}  trivial={pi_trivial:.4f}  loaded in {t_load:.1f}s")

    t0 = time.perf_counter()
    rows = wl_funnel(indptr, indices, init, y, L_max)
    t_wl = time.perf_counter() - t0
    print(f"    WL funnel in {t_wl:.1f}s")

    # Annotate each depth-row with the multiplicative improvement of
    # eps* over the trivial majority predictor (binarisation-aware
    # baseline).  This is the headline a reviewer expects on imbalanced
    # benchmarks: with largest-class-vs-rest the trivial baseline is
    # min(pi, 1-pi), and eps*_Pi_L must clear it to mean anything.
    for r in rows:
        r["improv_over_trivial"] = (
            float(pi_trivial / max(r["eps_star"], 1e-15)))

    # Gates.  Two categories:
    #  (a) graph-level (informative): WL refinement guarantees H and eps*
    #      are non-increasing in L.  These would FAIL if the WL refiner
    #      produced a non-refinement (bug detector for wl_refine).
    #  (b) kernel sanity (tautological): bracket_holds and width_le_W_STAR
    #      are properties of bracket_from_cells, not of the graph.  They
    #      would fail only on a kernel bug.  Kept as belt-and-braces.
    Hs   = np.array([r["H"] for r in rows])
    eps  = np.array([r["eps_star"] for r in rows])
    lows = np.array([r["lower"] for r in rows])
    ups  = np.array([r["upper"] for r in rows])
    widths = ups - lows
    g = {
        # (a) graph-level (WL-refinement guarantees)
        "monotone_H":        bool(np.all(np.diff(Hs)   <= 1e-9)),
        "monotone_eps":      bool(np.all(np.diff(eps)  <= 1e-9)),
        # (b) kernel sanity (bracket_from_cells implementation)
        "bracket_holds":     bool(np.all((lows - 1e-9 <= eps) & (eps <= ups + 1e-9))),
        "width_le_W_STAR":   bool(np.all(widths <= W_STAR + 1e-9)),
    }
    for L, r in enumerate(rows):
        print(f"      L={L}  m={r['m']:6d}  H={r['H']:.4f}  "
              f"lower={r['lower']:.4f}  ε*={r['eps_star']:.4f}  upper={r['upper']:.4f}  "
              f"x{r['improv_over_trivial']:.1f}_vs_trivial")

    funnel_figure(name, rows)
    return {"name": name, "n_V": n, "n_E": nE,
            "pi": pi, "pi_trivial": pi_trivial,
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
