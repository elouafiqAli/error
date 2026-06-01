"""
e3d_arch_full.py
================

D-Full: CUDA-optimised post-hoc architecture-vs-WL audit.

Extends D-Lite by:
  - 5 datasets (adds twitch_en + ogbn_arxiv)
  - 4 architectures (adds GraphSAGE)
  - 5 seeds
  - hidden=128 (up from 64), depth L=3, Adam 200 epochs lr=0.01 wd=5e-4
  - extended k-grid {16, 64, 256, 1024, min(k_WL, 4096)}
  - full-batch transductive training, fp32, single GPU
  - tf32 enabled on Ampere+ for speed

Designed for CUDA H200/A100; falls back to MPS/CPU for local smoke.

Public API:
  run_dataset(name) -> dict   # all (arch, seed) cells for one dataset
  run_all()        -> dict    # full 100-cell grid
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.cluster import MiniBatchKMeans
from torch_geometric.nn import GATConv, GCNConv, GINConv, SAGEConv

from common import bracket_from_cells
from e3d_data_full import (DATASET_ORDER, load, load_wl_ceilings)

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


# --------------------------------------------------- device
def pick_device() -> torch.device:
    if torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        torch.backends.cudnn.benchmark = True
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


# --------------------------------------------------- architectures
class GCN(nn.Module):
    def __init__(self, in_dim, hidden, L=3):
        super().__init__()
        self.convs = nn.ModuleList()
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            self.convs.append(GCNConv(dims[i], dims[i + 1], cached=True,
                                      add_self_loops=True, normalize=True))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, ei):
        h = x
        for i, c in enumerate(self.convs):
            h = c(h, ei)
            if i + 1 < len(self.convs):
                h = F.relu(h)
        return h

    def forward(self, x, ei):
        return self.head(self.embed(x, ei))


class GAT(nn.Module):
    def __init__(self, in_dim, hidden, L=3, heads=4):
        super().__init__()
        self.convs = nn.ModuleList()
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            last = (i == L - 1)
            self.convs.append(GATConv(
                dims[i], dims[i + 1] // (1 if last else heads),
                heads=(1 if last else heads),
                concat=(not last), add_self_loops=True))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, ei):
        h = x
        for i, c in enumerate(self.convs):
            h = c(h, ei)
            if i + 1 < len(self.convs):
                h = F.elu(h)
        return h

    def forward(self, x, ei):
        return self.head(self.embed(x, ei))


class GIN(nn.Module):
    def __init__(self, in_dim, hidden, L=3):
        super().__init__()
        self.convs = nn.ModuleList()
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            mlp = nn.Sequential(nn.Linear(dims[i], hidden), nn.ReLU(),
                                nn.Linear(hidden, dims[i + 1]))
            self.convs.append(GINConv(mlp, train_eps=True))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, ei):
        h = x
        for i, c in enumerate(self.convs):
            h = c(h, ei)
            if i + 1 < len(self.convs):
                h = F.relu(h)
        return h

    def forward(self, x, ei):
        return self.head(self.embed(x, ei))


class SAGE(nn.Module):
    def __init__(self, in_dim, hidden, L=3):
        super().__init__()
        self.convs = nn.ModuleList()
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            self.convs.append(SAGEConv(dims[i], dims[i + 1], aggr="mean"))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, ei):
        h = x
        for i, c in enumerate(self.convs):
            h = c(h, ei)
            if i + 1 < len(self.convs):
                h = F.relu(h)
        return h

    def forward(self, x, ei):
        return self.head(self.embed(x, ei))


ARCHS = {"GCN": GCN, "GAT": GAT, "GIN": GIN, "SAGE": SAGE}
ARCH_ORDER = ["GCN", "GAT", "GIN", "SAGE"]


# --------------------------------------------------- training
def train_one(arch_name, in_dim, x, ei, y, seed, *, hidden=128, L=3,
              epochs=200, lr=1e-2, weight_decay=5e-4, device):
    torch.manual_seed(seed); np.random.seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)

    model = ARCHS[arch_name](in_dim, hidden, L).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr,
                           weight_decay=weight_decay)

    model.train()
    t0 = time.perf_counter()
    last_loss = float("nan")
    for _ in range(epochs):
        opt.zero_grad(set_to_none=True)
        logits = model(x, ei)
        loss = F.cross_entropy(logits, y)
        loss.backward()
        opt.step()
        last_loss = float(loss.item())
    if device.type == "cuda":
        torch.cuda.synchronize()
    wall = time.perf_counter() - t0

    model.eval()
    with torch.no_grad():
        logits = model(x, ei)
        pred = logits.argmax(dim=1)
        Rhat = float((pred != y).float().mean().item())
        Z = model.embed(x, ei).cpu().numpy()
    return {"Rhat": Rhat, "train_loss_final": last_loss,
            "wall_train_s": wall, "Z": Z}


def kmeans_partition(Z, k, seed):
    k = max(2, min(k, Z.shape[0]))
    km = MiniBatchKMeans(n_clusters=k, random_state=seed, n_init=3,
                         max_iter=100,
                         batch_size=min(4096, Z.shape[0]))
    labels = km.fit_predict(Z)
    return labels.astype(np.uint64), int(np.unique(labels).size)


def _k_grid_for(k_wl, n):
    raw = sorted({16, 64, 256, 1024, min(k_wl, 4096)})
    return [k for k in raw if 2 <= k <= n]


# --------------------------------------------------- per-dataset driver
def run_dataset(name, *, seeds=(0, 1, 2, 3, 4), L=3, hidden=128,
                epochs=200, device=None, verbose=True):
    """Run all (arch, seed) cells for one dataset. Returns the dict
    that goes into the final JSON under 'datasets[]'."""
    if device is None:
        device = pick_device()
    data, y_bin, target = load(name)
    ceilings = load_wl_ceilings(L=L)
    ceil = ceilings[name]
    n = int(data.num_nodes)
    in_dim = int(data.x.size(1))
    pi = float(y_bin.mean())

    if verbose:
        print(f"=== {name} ===  n={n} |E|={data.edge_index.size(1)} "
              f"d_in={in_dim} pi={pi:.4f} "
              f"k_WL={ceil['m_WL']} eps_WL={ceil['eps_WL']:.4f} "
              f"device={device}", flush=True)

    x = data.x.to(device)
    ei = data.edge_index.to(device)
    y = torch.from_numpy(y_bin).long().to(device)

    k_grid = _k_grid_for(ceil["m_WL"], n)

    ds_out = {"name": name, "n": n, "in_dim": in_dim, "pi": pi,
              "target_class": int(target),
              "eps_WL": ceil["eps_WL"], "k_WL": ceil["m_WL"],
              "k_grid": k_grid,
              "runs": []}

    for arch in ARCH_ORDER:
        for seed in seeds:
            t_cell = time.perf_counter()
            tr = train_one(arch, in_dim, x, ei, y, seed,
                           hidden=hidden, L=L, epochs=epochs,
                           device=device)
            Z = tr.pop("Z")
            assert np.isfinite(Z).all(), f"Z non-finite {name}/{arch}/{seed}"
            assert 0.0 <= tr["Rhat"] <= 1.0
            Rhat = tr["Rhat"]
            k_runs = []
            for k in k_grid:
                cl, k_used = kmeans_partition(Z, k, seed)
                br = bracket_from_cells(cl, y_bin)
                eps_tr = float(br.eps_star)
                k_runs.append({
                    "k_requested": int(k),
                    "k_used": int(k_used),
                    "eps_trained": eps_tr,
                    "feature_gap_at_k": ceil["eps_WL"] - eps_tr,
                    "head_signal_at_k": eps_tr - Rhat,
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
                kref = k_runs[-1]  # the largest k -> closest to k_WL
                print(f"  {arch:4s} seed={seed}  Rhat={Rhat:.4f}  "
                      f"eps_tr(k={kref['k_requested']})="
                      f"{kref['eps_trained']:.4f}  "
                      f"feat_gap={kref['feature_gap_at_k']:+.4f}  "
                      f"wall={tr['wall_train_s']:.1f}s",
                      flush=True)
    # free GPU memory between datasets
    del x, ei, y
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return ds_out


def run_all(seeds=(0, 1, 2, 3, 4), L=3, hidden=128, epochs=200,
            datasets=None, device=None, out_path=None):
    if datasets is None:
        datasets = DATASET_ORDER
    if device is None:
        device = pick_device()
    out = {"experiment": "e3d_arch_full",
           "device": str(device),
           "depth_L": L, "hidden": hidden, "epochs": epochs,
           "seeds": list(seeds),
           "archs": ARCH_ORDER,
           "datasets_order": datasets,
           "datasets": []}
    t0 = time.perf_counter()
    for name in datasets:
        out["datasets"].append(
            run_dataset(name, seeds=seeds, L=L, hidden=hidden,
                        epochs=epochs, device=device))
    out["total_wall_s"] = time.perf_counter() - t0
    if out_path is None:
        out_path = RESULTS / "e3d_arch_full.json"
    Path(out_path).write_text(json.dumps(out, indent=2))
    print(f"\nWrote {out_path}  total_wall={out['total_wall_s']:.0f}s",
          flush=True)
    return out


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--datasets", nargs="*", default=None)
    p.add_argument("--seeds", nargs="*", type=int,
                   default=[0, 1, 2, 3, 4])
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--hidden", type=int, default=128)
    p.add_argument("--out", default=None)
    a = p.parse_args()
    run_all(seeds=tuple(a.seeds), epochs=a.epochs, hidden=a.hidden,
            datasets=a.datasets, out_path=a.out)
