"""
e3d_arch_kll_n.py
=================

P0.4 driver: E3d-arch redo at k << n on Cora and CiteSeer.

Purpose. The original E3d-arch / E3d-arch-full tables evaluate
eps^*_{Pi^trained_k} at k = k_WL, which on Cora / CiteSeer gives
k/n in {0.87, 0.61} -- squarely inside Proposition 4.5's
cardinality-collapse regime where eps^*_Pi -> 0 trivially for
ANY partition with cells <~ n. Conclusions about "features beat
WL" or "head extracts sub-cell structure" drawn from that
regime cannot distinguish expressivity from memorisation.

This driver re-runs the same protocol but pins k to a small
budget grid {8, 16, 32, 64}, so k/n in {0.003 - 0.024} on both
datasets. At this scale eps^*_Pi is bounded well away from 0
by the marginal pi, and the bracket comparison is a clean
*expressivity* test:
  - feat_gap > 0 means the trained features carry label
    structure that the 1-WL partition does NOT, even when
    the cell budget is much smaller than k_WL.
  - head_sig := Rhat - eps^*_Pi > 0 means the head fails to
    reach the per-cell majority floor (head slack); < 0 means
    the head extracts continuous-Z structure beyond what k-means
    at budget k can recover.

Reuses architectures and training loop from e3d_arch_full.py.

Output:  results/e3d_arch_kll_n.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch

from common import bracket_from_cells
from e3d_arch_full import (ARCH_ORDER, kmeans_partition, pick_device,
                           train_one)
from e3d_data_full import load, load_wl_ceilings

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

K_GRID = (8, 16, 32, 64)
DATASETS = ("cora", "citeseer")
SEEDS = (0, 1, 2, 3, 4)


def run_dataset(name, *, seeds=SEEDS, k_grid=K_GRID, L=3, hidden=128,
                epochs=200, device=None, verbose=True):
    if device is None:
        device = pick_device()
    data, y_bin, target = load(name)
    ceil = load_wl_ceilings(L=L)[name]
    n = int(data.num_nodes)
    in_dim = int(data.x.size(1))
    pi = float(y_bin.mean())

    if verbose:
        print(f"=== {name} ===  n={n}  d_in={in_dim}  pi={pi:.4f}  "
              f"k_WL={ceil['m_WL']}  eps_WL={ceil['eps_WL']:.4f}  "
              f"device={device}", flush=True)
        print(f"  k_grid = {list(k_grid)}  "
              f"(k/n in [{min(k_grid)/n:.4f}, {max(k_grid)/n:.4f}])",
              flush=True)

    x = data.x.to(device)
    ei = data.edge_index.to(device)
    y = torch.from_numpy(y_bin).long().to(device)

    # Also evaluate the WL ceiling at the SAME small k grid -- this is
    # the matched-cell-budget comparison the paper actually wants.
    # We approximate eps^*_{Pi^WL restricted to k cells} by k-means
    # in the WL one-hot space; but simpler: report eps^*_WL at the
    # full WL granularity (lower bound on any matched-k WL ceiling),
    # and rely on monotonicity Prop 4 (refinement lowers eps^*).
    # In the matched-k regime the right comparison object is
    # eps^*_{Pi^trained_k} vs the *Bayes* (asymptotic) eps^* of the
    # corresponding graph WL hierarchy at depth L=3, which we proxy
    # by the trivial floor pi_min := min(pi, 1-pi).
    pi_min = float(min(pi, 1.0 - pi))

    ds_out = {"name": name, "n": n, "in_dim": in_dim, "pi": pi,
              "pi_min": pi_min,
              "target_class": int(target),
              "eps_WL_full": ceil["eps_WL"],
              "k_WL_full": ceil["m_WL"],
              "k_grid": list(k_grid),
              "k_over_n": [k / n for k in k_grid],
              "runs": []}

    for arch in ARCH_ORDER:
        for seed in seeds:
            t_cell = time.perf_counter()
            tr = train_one(arch, in_dim, x, ei, y, seed,
                           hidden=hidden, L=L, epochs=epochs,
                           device=device)
            Z = tr.pop("Z")
            assert np.isfinite(Z).all()
            Rhat = tr["Rhat"]
            k_runs = []
            for k in k_grid:
                cl, k_used = kmeans_partition(Z, k, seed)
                br = bracket_from_cells(cl, y_bin)
                eps_tr = float(br.eps_star)
                # New sign convention (P0.3): head_sig = Rhat - eps_tr.
                # Positive = head slack above the per-cell majority floor.
                head_slack = Rhat - eps_tr
                # feat_gap = eps_WL_full - eps_trained_k. NOTE this is
                # NOT a matched-k comparison on the WL side -- eps_WL is
                # the WL ceiling at k = k_WL >> k. So at small k we
                # expect feat_gap to be NEGATIVE by Prop 4 monotonicity
                # alone (the trained k-cell partition is much coarser
                # than the WL k_WL-cell partition). The honest small-k
                # comparison is between eps^*_Pi^trained_k and the
                # marginal floor pi_min (which the bracket must respect
                # for any partition).
                k_runs.append({
                    "k_requested": int(k),
                    "k_used": int(k_used),
                    "eps_trained": eps_tr,
                    "Rhat": Rhat,
                    "head_slack": head_slack,
                    "eps_minus_pi_min": eps_tr - pi_min,
                    "feat_gap_vs_eps_WL_full": ceil["eps_WL"] - eps_tr,
                })
            ds_out["runs"].append({
                "arch": arch, "seed": int(seed),
                "Rhat": Rhat,
                "train_loss_final": tr["train_loss_final"],
                "wall_train_s": tr["wall_train_s"],
                "wall_cell_s": time.perf_counter() - t_cell,
                "k_sweep": k_runs,
            })
            if verbose:
                kref = k_runs[-1]  # largest k = 64
                print(f"  {arch:4s} seed={seed}  Rhat={Rhat:.4f}  "
                      f"eps_tr(k={kref['k_requested']})="
                      f"{kref['eps_trained']:.4f}  "
                      f"head_slack={kref['head_slack']:+.4f}  "
                      f"wall={tr['wall_train_s']:.1f}s",
                      flush=True)

    del x, ei, y
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return ds_out


def run_all(*, datasets=DATASETS, seeds=SEEDS, k_grid=K_GRID,
            L=3, hidden=128, epochs=200, device=None, out_path=None):
    if device is None:
        device = pick_device()
    if out_path is None:
        out_path = RESULTS / "e3d_arch_kll_n.json"
    out_path = Path(out_path)
    out = {"experiment": "e3d_arch_kll_n",
           "device": str(device),
           "depth_L": L, "hidden": hidden, "epochs": epochs,
           "seeds": list(seeds),
           "archs": list(ARCH_ORDER),
           "k_grid": list(k_grid),
           "datasets_order": list(datasets),
           "head_sig_convention": "head_slack := Rhat - eps^*_{Pi^trained_k}; "
                                  "positive => head fails to reach per-cell "
                                  "majority floor",
           "datasets": []}
    t0 = time.perf_counter()
    for name in datasets:
        out["datasets"].append(
            run_dataset(name, seeds=seeds, k_grid=k_grid, L=L,
                        hidden=hidden, epochs=epochs, device=device))
        out["total_wall_s"] = time.perf_counter() - t0
        out_path.write_text(json.dumps(out, indent=2))
        print(f"  [checkpoint] wrote {out_path}", flush=True)
    print(f"\nDone.  total_wall = {out['total_wall_s']:.1f}s",
          flush=True)
    return out


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--datasets", nargs="*", default=list(DATASETS))
    p.add_argument("--seeds", nargs="*", type=int, default=list(SEEDS))
    p.add_argument("--k_grid", nargs="*", type=int, default=list(K_GRID))
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--hidden", type=int, default=128)
    p.add_argument("--out", default=None)
    a = p.parse_args()
    run_all(datasets=tuple(a.datasets), seeds=tuple(a.seeds),
            k_grid=tuple(a.k_grid), epochs=a.epochs, hidden=a.hidden,
            out_path=a.out)
