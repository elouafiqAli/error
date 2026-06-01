"""
e3b_wl_structural.py — Experiment 3b: WL bracket on featureless
structural benchmarks where the WL hierarchy is the *binding* constraint.

Motivation.  E3 (Cora, CiteSeer, PubMed, ogbn-arxiv) is feature-driven
node classification: depth-3 1-WL on ogbn-arxiv produces ~96% singleton
cells, so the bracket collapses to ~0 by partition-cardinality, not by
any genuine "WL/MPNN expressivity" mechanism.  E3b reruns the bracket
on graphs and labels engineered so that

    (i) initial node features carry no label signal (constant or degree),
    (ii) 1-WL is provably blind to the label (so the bracket *must*
         remain pinned at the marginal-entropy ceiling for every depth L).

If the bracket tightens on these benchmarks, the implementation is buggy.
If it stays pinned at H_bin(pi)/2 (upper) and H_bin^{-1}(H_bin(pi)) = pi
(lower), the WL-as-MPNN-bottleneck story has its expected empirical face.

Benchmarks:
  B1 CSL-union     two 4-regular Cayley graphs C_n(S1) ⊔ C_n(S2), label
                   = graph-membership.  1-WL gives a single colour per
                   graph; label is constant per WL cell, so bracket
                   *saturates the lower side* (epsilon* = 0, H = 0).
                   This is the witness of the "bracket-collapse via WL
                   succeeding" regime — the opposite of E3.
  B2 CSL-orbit     single 4-regular Cayley C_n(S), label = vertex orbit
                   under cyclic rotation modulo k (k | n, k > 1).
                   Inside the orbit-quotient task, 1-WL is constant
                   (Cayley graphs are vertex-transitive); bracket must
                   sit at the marginal-entropy ceiling for every L.
  B3 Paley(q)      strongly regular Paley graph on q vertices (q prime,
                   q = 1 mod 4), label = quadratic-residue indicator.
                   1-WL gives a single colour class; bracket at
                   eps* = 1/2 H_bin(1/2) ceiling for every L.

Constant initial features throughout (h^{(0)}(v) = 0 for all v), so
the only thing WL can use is graph structure.  No GPU; no model.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from common import bracket_from_cells
from e3_wl_bracket import wl_funnel  # vectorised WL refinement reused

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)


# --------------------------------------------------------------- graphs
def _csr_undirected(rows: np.ndarray, cols: np.ndarray, n: int):
    """Build symmetric CSR (indptr, indices) from edge list."""
    u = np.concatenate([rows, cols])
    v = np.concatenate([cols, rows])
    # de-dup self-loops are not added; keep multi-edges out
    keep = u != v
    u = u[keep]; v = v[keep]
    order = np.lexsort((v, u))
    u = u[order]; v = v[order]
    # de-duplicate
    keep2 = np.concatenate([[True], (u[1:] != u[:-1]) | (v[1:] != v[:-1])])
    u = u[keep2]; v = v[keep2]
    indptr = np.zeros(n + 1, dtype=np.int64)
    np.add.at(indptr, u + 1, 1)
    np.cumsum(indptr, out=indptr)
    indices = v.astype(np.int64)
    return indptr, indices


def cayley_circulant(n: int, skips: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray]:
    """Undirected circulant graph C_n(S):  v ~ v+s (mod n) for s in S∪-S."""
    src = []
    dst = []
    for s in skips:
        for v in range(n):
            src.append(v); dst.append((v + s) % n)
    rows = np.asarray(src, dtype=np.int64)
    cols = np.asarray(dst, dtype=np.int64)
    return _csr_undirected(rows, cols, n)


def paley(q: int) -> tuple[np.ndarray, np.ndarray]:
    """Paley graph on F_q (q prime, q = 1 mod 4):
       v ~ w iff (v - w) is a nonzero quadratic residue mod q."""
    assert q % 4 == 1, "Paley needs q = 1 mod 4 for symmetry."
    qrs = set()
    for x in range(1, q):
        qrs.add((x * x) % q)
    qrs = sorted(qrs)
    src = []
    dst = []
    for v in range(q):
        for s in qrs:
            src.append(v); dst.append((v + s) % q)
    rows = np.asarray(src, dtype=np.int64)
    cols = np.asarray(dst, dtype=np.int64)
    return _csr_undirected(rows, cols, q)


def disjoint_union(A: tuple[np.ndarray, np.ndarray], nA: int,
                   B: tuple[np.ndarray, np.ndarray], nB: int):
    """CSR disjoint union of two graphs."""
    indptrA, indicesA = A
    indptrB, indicesB = B
    indices = np.concatenate([indicesA, indicesB + nA])
    indptr = np.concatenate([indptrA, indptrA[-1] + indptrB[1:]])
    return indptr, indices


# --------------------------------------------------------------- benchmarks
def bench_csl_union(L_max: int = 6) -> dict:
    """B1: two 4-regular circulants of equal order with different skips;
    binary label = which graph the vertex came from.

    Both graphs are 4-regular and vertex-transitive, so 1-WL *within*
    each graph collapses to one colour.  Across graphs WL may or may
    not separate the two colour classes by degree (here both are 4),
    so the partition is exactly {V_A, V_B} for every depth L >= 0.
    The label is constant on each cell, so eps* = 0 and H = 0 — the
    bracket saturates its lower-side endpoint and certifies that the
    *task* is WL-aligned.  This is the trivially-tight regime."""
    n = 41
    A = cayley_circulant(n, (1, 2))   # 4-regular
    B = cayley_circulant(n, (1, 5))   # 4-regular, non-isomorphic to A
    indptr, indices = disjoint_union(A, n, B, n)
    y = np.concatenate([np.zeros(n, dtype=np.int8),
                         np.ones(n, dtype=np.int8)])
    h0 = np.zeros(2 * n, dtype=np.uint64)   # constant initial features
    rows = wl_funnel(indptr, indices, h0, y, L_max)
    return {"name": "CSL_union(C_41(1,2)⊔C_41(1,5))",
            "n": int(2 * n), "pi": float(y.mean()),
            "marginal_entropy": _hbin(float(y.mean())),
            "rows": rows}


def bench_csl_orbit(L_max: int = 6) -> dict:
    """B2: single 4-regular Cayley graph; binary label = orbit-mod-k.

    Cayley(C_n, S) is vertex-transitive, so 1-WL produces one colour
    class for every L.  Bracket must remain at the marginal-entropy
    ceiling H_bin(pi)/2 with eps* = pi (the smaller of pi, 1-pi).
    This is the *vacuous* regime: the bound is correct but uninformative,
    exactly as the WL hierarchy predicts."""
    n = 60   # divisible by many k; vertex-transitive Cayley
    indptr, indices = cayley_circulant(n, (1, 5))   # 4-regular
    # Binary label: vertex index mod 2 (forces near-balanced label
    # that is *not* constant per orbit of the WL action).
    y = (np.arange(n) % 2).astype(np.int8)
    h0 = np.zeros(n, dtype=np.uint64)
    rows = wl_funnel(indptr, indices, h0, y, L_max)
    return {"name": "CSL_orbit(C_60(1,5), label=v mod 2)",
            "n": int(n), "pi": float(y.mean()),
            "marginal_entropy": _hbin(float(y.mean())),
            "rows": rows}


def bench_paley(L_max: int = 6, q: int = 13) -> dict:
    """B3: Paley graph on q vertices; binary label = QR indicator.

    Paley graphs are strongly regular, hence 1-WL-blind: every vertex
    has the same colour for every depth L.  Bracket stays at
    eps* = #QR / q ≈ 1/2, upper = H_bin(pi)/2 ≈ 1/2 for every L.

    Even though the *label* is non-trivial graph structure
    (quadratic-residue colouring), 1-WL cannot see it — the
    canonical witness of WL's structural blindness."""
    indptr, indices = paley(q)
    qrs = {(x * x) % q for x in range(1, q)}
    y = np.array([1 if v in qrs else 0 for v in range(q)], dtype=np.int8)
    h0 = np.zeros(q, dtype=np.uint64)
    rows = wl_funnel(indptr, indices, h0, y, L_max)
    return {"name": f"Paley({q}), label=QR-indicator",
            "n": int(q), "pi": float(y.mean()),
            "marginal_entropy": _hbin(float(y.mean())),
            "rows": rows}


# ---------------------------------------------------------------- main
def _hbin(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))


def main():
    t0 = time.perf_counter()
    out = {
        "experiment": "E3b WL bracket on structural benchmarks",
        "description": ("Featureless benchmarks where 1-WL is provably "
                        "blind (vertex-transitive Cayley + Paley) or "
                        "label-aligned (disjoint Cayley union).  "
                        "Bracket must either saturate the lower side "
                        "trivially (B1) or pin at the marginal-entropy "
                        "ceiling for every L (B2, B3).  No GPU; no "
                        "training; constant initial features throughout."),
        "benchmarks": [
            bench_csl_union(L_max=6),
            bench_csl_orbit(L_max=6),
            bench_paley(L_max=6, q=13),
            bench_paley(L_max=6, q=29),
        ],
        "wall_time_s": None,
    }
    out["wall_time_s"] = round(time.perf_counter() - t0, 3)

    # Print a compact summary
    for b in out["benchmarks"]:
        print(f"\n== {b['name']}  (n={b['n']}, pi={b['pi']:.3f},"
              f" H_marginal={b['marginal_entropy']:.3f}) ==")
        print(f"  {'L':>2} {'m':>5} {'H':>7} {'lower':>7}"
              f" {'eps*':>7} {'upper':>7}")
        for r in b["rows"]:
            print(f"  {r['L']:>2} {r['m']:>5} {r['H']:>7.4f}"
                  f" {r['lower']:>7.4f} {r['eps_star']:>7.4f}"
                  f" {r['upper']:>7.4f}")

    path = RESULTS / "e3b.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"\nwrote {path}  (wall={out['wall_time_s']}s)")


if __name__ == "__main__":
    main()
