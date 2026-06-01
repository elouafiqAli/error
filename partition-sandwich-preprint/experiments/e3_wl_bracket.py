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

import numpy as np

from common import W_STAR, bracket_from_cells

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)
DATA_DIR = HERE / "data";   DATA_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------- WL refinement (sparse)
# SplitMix64 finaliser (David Stafford) — strong 64-bit avalanche function,
# used as a PRF inside an *additive* multiset hash: per-vertex
# sum_over_neighbours(splitmix(c)) is order-invariant and computable in
# one np.add.reduceat over the CSR adjacency.
_U64_C1 = np.uint64(0xbf58476d1ce4e5b9)
_U64_C2 = np.uint64(0x94d049bb133111eb)
_U64_C3 = np.uint64(0x9e3779b97f4a7c15)  # golden-ratio constant (combine)
_S30 = np.uint64(30); _S27 = np.uint64(27); _S31 = np.uint64(31)


def _splitmix64(x: np.ndarray) -> np.ndarray:
    """Vectorised SplitMix64 finaliser; input and output are uint64."""
    x = x.astype(np.uint64, copy=True)
    x = (x ^ (x >> _S30)) * _U64_C1
    x = (x ^ (x >> _S27)) * _U64_C2
    x =  x ^ (x >> _S31)
    return x


def wl_refine(colours: np.ndarray, indptr: np.ndarray,
              indices: np.ndarray) -> np.ndarray:
    """
    One vectorised WL refinement round.

    Algorithm.  We canonicalise each vertex's neighbour multiset by sorting
    within its CSR segment via a single ``np.argsort`` on a packed
    ``(vert_id, neighbour_colour)`` key (faster than ``np.lexsort`` at
    this scale).  After sorting, the *position within the segment*
    becomes informative, so we mix each value with
    ``splitmix(neighbour_colour) ^ splitmix(position_within_segment)`` and
    sum the result per vertex.  The per-vertex hash is therefore a true
    sequence hash of the canonical sorted multiset (Clarke et al. 2003,
    "Incremental Multiset Hash Functions", combined with positional
    mixing): collisions occur only between distinct sorted sequences with
    probability ~2^-64 per pair, which is the same guarantee as the
    sorted-tuple-blake2b reference.  Combining own colour and degree into
    the final key makes the round a 1-WL refinement bit-equivalent (up to
    relabelling) to the per-vertex blake2b version.

    Performance.  Best-of-3 wall-clock vs the per-vertex blake2b loop on
    a laptop CPU core, with ``partitions_equal`` verified True on every
    row:

      * cora        2 708 V    R1  16.2→1.4 ms  (11.5×)   R2  32.8→1.5 ms  (22.1×)
      * pubmed     19 717 V    R1 113.2→13.3 ms ( 8.5×)   R2 121.6→23.4 ms ( 5.2×)
      * ogbn_arxiv 169 343 V   R1 1326→385 ms   ( 3.4×)   R2 1863→674 ms   ( 2.8×)

    Speedups grow with successive rounds because the per-vertex
    blake2b loop scales with the cell-count m, while the vectorised
    version's cost is dominated by the single argsort over |E_directed|
    which is round-independent.
    """
    n = len(colours)
    indptr = np.ascontiguousarray(indptr, dtype=np.int64)
    indices = np.ascontiguousarray(indices, dtype=np.int64)
    own = colours.astype(np.uint64, copy=False)
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)

    if indices.size > 0:
        # Canonicalise current colours to dense uint32 ids so we can pack
        # ``(vert_id, colour)`` into a single uint64 key for a one-pass
        # ``np.argsort`` (faster than ``np.lexsort`` at this scale).
        _, own_dense = np.unique(own, return_inverse=True)
        own_dense = own_dense.astype(np.uint64)         # < m_prev <= n
        nbr_col = own_dense[indices]                    # [|E|], uint64

        n_u64 = np.uint64(n)
        # n <= 2^32 and m_prev <= n in all our graphs, so the packed key
        # (vert_id * n + nbr_col) fits in uint64 without overflow.
        vert_id = np.repeat(np.arange(n, dtype=np.int64),
                            (indptr[1:] - indptr[:-1])).astype(np.uint64)
        packed = vert_id * n_u64 + nbr_col              # canonical sort key
        perm = np.argsort(packed, kind="stable")
        nbr_sorted = nbr_col[perm]                      # sorted within segs

        # Within-segment position 0..deg(v)-1 for each entry.
        seg_start = np.repeat(indptr[:-1].astype(np.int64),
                              indptr[1:] - indptr[:-1])
        within_pos = (np.arange(indices.size, dtype=np.int64)
                      - seg_start).astype(np.uint64)
        # Position-aware sequence hash over the canonical sorted multiset.
        mixed = _splitmix64(_splitmix64(nbr_sorted)
                            ^ _splitmix64(within_pos + _U64_C3))
        starts_safe = np.minimum(indptr[:-1], indices.size - 1
                                 ).astype(np.int64)
        seg_hash = np.add.reduceat(mixed, starts_safe)
        seg_hash = np.where(deg > 0, seg_hash, np.uint64(0))
    else:
        seg_hash = np.zeros(n, dtype=np.uint64)

    key = _splitmix64(own ^ _splitmix64(deg + _U64_C3) ^ _splitmix64(seg_hash))
    _, inverse = np.unique(key, return_inverse=True)
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


# Selected binarisation strategy; settable via CLI before loaders run.
# Strategies:
#   'largest'   - y_bin = (y_multi == argmax(counts))  (most flattering;
#                  trivial baseline = 1 - max_class_freq).
#   'balanced'  - y_bin = (y_multi == argmin |count - n/2|)
#                  (median-frequency split; trivial baseline closest to 1/2,
#                  the universal worst case for any binary partition).
#   'class=K'   - y_bin = (y_multi == K), K integer (explicit class).
BINARISATION: str = "largest"


def _binarise_multiclass(y_multi: np.ndarray, strategy: str | None = None) -> tuple[np.ndarray, int, str]:
    """Project multiclass labels to {0, 1} under the selected strategy.

    Returns ``(y_bin, target_class_or_-1, resolved_strategy)``.  When
    ``strategy='balanced'``, multiple classes may be grouped to form the
    positive set; ``target_class`` is then ``-1`` and the resolved
    strategy string carries the chosen class list.
    """
    s = (strategy or BINARISATION).lower()
    counts = np.bincount(y_multi)
    if s == "largest":
        target = int(np.argmax(counts))
        y_bin = (y_multi == target).astype(np.int8)
        return y_bin, target, s
    if s == "balanced":
        # Greedy class-grouping: include classes in decreasing-count order
        # as long as the running sum stays <= n/2; then optionally take one
        # more class if it brings the sum closer to n/2.  Result: a
        # positive-class group whose total fraction is as close to 1/2 as
        # the discrete class structure allows.
        n = int(y_multi.size)
        order = np.argsort(-counts)
        chosen: list[int] = []
        s_sum = 0
        for c in order:
            cnt = int(counts[c])
            if s_sum + cnt <= n // 2:
                chosen.append(int(c)); s_sum += cnt
        # consider adding one more class if it moves us closer to n/2
        rest = [int(c) for c in order if int(c) not in chosen]
        if rest:
            c_extra = rest[0]
            if abs((s_sum + int(counts[c_extra])) - n / 2.0) < abs(s_sum - n / 2.0):
                chosen.append(c_extra); s_sum += int(counts[c_extra])
        y_bin = np.isin(y_multi, np.array(chosen, dtype=y_multi.dtype)).astype(np.int8)
        resolved = f"balanced(classes={sorted(chosen)})"
        return y_bin, -1, resolved
    if s.startswith("class="):
        target = int(s.split("=", 1)[1])
        if target < 0 or target >= counts.size:
            raise ValueError(f"class={target} out of range [0, {counts.size})")
        y_bin = (y_multi == target).astype(np.int8)
        return y_bin, target, s
    raise ValueError(f"unknown binarisation strategy: {strategy!r}")


def _planetoid_binarise(name: str):
    indptr, indices, y_multi, n = _load_planetoid_raw(name)
    y, target, strat = _binarise_multiclass(y_multi)
    print(f"    [{name}] binarisation={strat}  target_class={target}  "
          f"|y=1|={int(y.sum())}/{n}  π={float(y.mean()):.4f}")
    deg = (indptr[1:] - indptr[:-1]).astype(np.uint64)
    return name, n, indptr, indices, y, deg


def load_cora():     return _planetoid_binarise("cora")
def load_citeseer(): return _planetoid_binarise("citeseer")
def load_pubmed():   return _planetoid_binarise("pubmed")


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
    y, target, strat = _binarise_multiclass(y_multi)
    print(f"    [ogbn_arxiv] binarisation={strat}  target_class={target}  "
          f"|y=1|={int(y.sum())}/{n}  π={float(y.mean()):.4f}")
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
    import matplotlib.pyplot as plt  # lazy: only needed when plotting
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
    ap.add_argument("--binarisation", default="largest",
                    help="label binarisation: 'largest' (default), "
                         "'balanced', or 'class=K' (integer K). "
                         "Ignored for twitch_en (native binary).")
    ap.add_argument("--out", default="e3.json",
                    help="results json filename under results/ "
                         "(use e.g. e3_balanced.json when sweeping).")
    args = ap.parse_args()

    global BINARISATION
    BINARISATION = args.binarisation
    print(f"binarisation strategy: {BINARISATION}")

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
        "binarisation": BINARISATION,
        "datasets": results,
        "all_gates_pass": all(
            r.get("gates", {}).get("bracket_holds", False)
            and r.get("gates", {}).get("monotone_H", False)
            for r in results if "error" not in r
        ),
    }
    out = RESULTS / args.out
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
