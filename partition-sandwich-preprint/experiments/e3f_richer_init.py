"""
e3f_richer_init.py
===================

Push CiteSeer and PubMed past raw 1-WL with a *cheap* refinement of
the initial colour that is provably between 1-WL and 2-WL on sparse
graphs (Maron et al., 2019; Geerts, 2020):

  h0(v) := canonical(deg(v),  sorted multiset of deg(u) for u in N(v))

This is the "neighbourhood-degree fingerprint" or "1-hop degree
sequence" augmentation.  It is strictly stronger than degree-init
1-WL (which only sees deg(v)) and strictly weaker than 2-FWL (which
sees the full join-structure of vertex pairs), at cost O(|E| log d).

We compare four init schemes on CiteSeer and PubMed:
  (i)   const : h0 = 0          (structural-WL baseline)
  (ii)  deg   : h0 = deg(v)     (the original E3 setup)
  (iii) logdeg: K=8 log-degree bin (matches E3c K=8)
  (iv)  nbrdeg: degree + sorted neighbour-degree multiset (this file)

Reports per (graph, init, L) the bracket and the sigma(0.05, 0.5)
index of E3c.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from common import bracket_from_cells
from e3_wl_bracket import (
    load_citeseer, load_pubmed, wl_funnel, wl_refine,
)
from e3a_decomposition import saturation_depths, coarsened_init

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def nbr_degree_init(indptr: np.ndarray, indices: np.ndarray) -> np.ndarray:
    """h0(v) = canonical(deg(v), sorted multiset of deg(u) for u in N(v))."""
    n = indptr.size - 1
    deg = (indptr[1:] - indptr[:-1]).astype(np.int64)
    # For each vertex, fetch its neighbour-degrees, sort, build a byte key.
    # Use a packed tuple: (deg(v), tuple(sorted(deg(N(v))))).
    keys = []
    for v in range(n):
        nb = indices[indptr[v]:indptr[v + 1]]
        nb_deg = np.sort(deg[nb])
        # pack as bytes for hashing via np.unique
        keys.append(bytes(np.concatenate(([deg[v]], nb_deg)).astype(np.int32)))
    _, inv = np.unique(np.array(keys, dtype=object), return_inverse=True)
    return inv.astype(np.uint64)


def run_one(name: str, loader, L_max: int = 5) -> dict:
    print(f"\n=== {name} ===", flush=True)
    _, n, indptr, indices, y, init_deg = loader()
    pi = float(y.mean())
    deg = (indptr[1:] - indptr[:-1]).astype(np.int64)

    inits = {
        "const":   np.zeros(n, dtype=np.uint64),
        "deg":     init_deg.astype(np.uint64),
        "logdeg8": coarsened_init(deg, 8),
    }
    t0 = time.perf_counter()
    inits["nbrdeg"] = nbr_degree_init(indptr, indices)
    print(f"  nbrdeg init built in {time.perf_counter()-t0:.2f}s "
          f"({np.unique(inits['nbrdeg']).size} unique classes)")

    out = {"name": name, "n": n, "pi": pi, "L_max": L_max, "inits": {}}
    for label, h0 in inits.items():
        rows = wl_funnel(indptr, indices, h0, y, L_max)
        sig = saturation_depths(rows, n,
                                taus=(0.01, 0.05, 0.10),
                                rhos=(0.5, 0.75, 0.9))
        out["inits"][label] = {
            "n_init_classes": int(np.unique(h0).size),
            "depths": rows,
            "sigma": sig,
        }
        print(f"  init={label:8s} "
              f"K0={int(np.unique(h0).size):>6d}  "
              f"m2/n={rows[min(2, L_max)]['m']/n:.3f}  "
              f"eps*(L=3)={rows[min(3, L_max)]['eps_star']:.4f}  "
              f"L*(0.05)={sig['L_star']['0.05']}")
    return out


def main():
    out = {"experiment": "e3f_richer_init", "results": []}
    out["results"].append(run_one("citeseer", load_citeseer, L_max=5))
    out["results"].append(run_one("pubmed",   load_pubmed,   L_max=5))
    (RESULTS / "e3f.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {RESULTS / 'e3f.json'}")


if __name__ == "__main__":
    main()
