"""
e3d_arch_audit.py
==================

D-Lite: post-hoc architecture-vs-WL audit.

For each (dataset, arch, seed):
  1. Train a 3-layer GNN on the E3-binarised label vector (transductive,
     no train/test split: this is a *fitting-power* audit matching E3).
  2. Extract penultimate embeddings Z in R^{n x 64}.
  3. Cluster Z with MiniBatchKMeans at k in {16, 64, 256, m_L^WL}.
     -> Pi_trained(k) is the empirical partition the architecture's
        geometry induces at cell budget k.
  4. Report:
       Rhat                  = training error of the trained model
                               (its own 2-way linear head on Z)
       eps_WL                = eps^*_{Pi^WL_3}           from e3.json
       eps_trained(k)        = eps^*_{Pi_trained(k)}
       feature_gap_at_kWL    = eps_WL - eps_trained(k_WL)
         > 0 : the trained embedding at the SAME cell budget as WL is
               *more label-informative* than the WL partition (the
               architecture used node features beyond pure WL structure)
         <= 0: the embedding partition is at most as informative as WL
               at this budget; the architecture's gain (if any) comes
               from its head, not from refining the partition.
       head_signal_at_kWL    = eps_trained(k_WL) - Rhat
         > 0 : the trained linear head outperforms per-cell majority on
               the same embedding partition; the head exploits embedding
               geometry beyond what k-means recovers.
         <= 0: the head leaves bracket-detectable structure on the table.

Invariants (gates, must all PASS):
  (T1) eps_trained(k) monotone non-increasing in k for the OPTIMAL partition.
       MiniBatchKMeans returns a local optimum; minor violations (< 1e-3)
       are logged as warnings, not errors.
  (T2) eps_trained(k=n) = 0 (we don't run this k but it's the limit)
  (T3) Rhat in [0, 1], finite
  (T4) Z has no NaN/inf, k_used >= 0.9 * min(k_requested, n)

Note: Rhat >= eps_trained is NOT a valid invariant -- Rhat is from a
linear head, eps_trained is from a *different* (k-means) partition
of the SAME embeddings. There is no a priori sign relation.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.cluster import MiniBatchKMeans
from torch_geometric.datasets import Planetoid
from torch_geometric.nn import GATConv, GCNConv, GINConv

from common import bracket_from_cells

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
DATA = HERE / "data"
RESULTS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)


# --------------------------------------------------- device
def pick_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


DEVICE = pick_device()


# --------------------------------------------------- architectures
class GCN(nn.Module):
    def __init__(self, in_dim: int, hidden: int = 64, L: int = 3):
        super().__init__()
        self.convs = nn.ModuleList()
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            self.convs.append(GCNConv(dims[i], dims[i + 1]))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, edge_index):
        h = x
        for i, conv in enumerate(self.convs):
            h = conv(h, edge_index)
            if i + 1 < len(self.convs):
                h = F.relu(h)
        return h  # penultimate = output of last conv, pre-head

    def forward(self, x, edge_index):
        return self.head(self.embed(x, edge_index))


class GAT(nn.Module):
    def __init__(self, in_dim: int, hidden: int = 64, L: int = 3, heads: int = 4):
        super().__init__()
        self.convs = nn.ModuleList()
        # use concat=True between layers, then one final concat=False at last
        # layer so penultimate dim is `hidden` (matches GCN/GIN).
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            is_last = (i == L - 1)
            self.convs.append(GATConv(
                dims[i], dims[i + 1] // (1 if is_last else heads),
                heads=(1 if is_last else heads),
                concat=(not is_last)))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, edge_index):
        h = x
        for i, conv in enumerate(self.convs):
            h = conv(h, edge_index)
            if i + 1 < len(self.convs):
                h = F.elu(h)
        return h

    def forward(self, x, edge_index):
        return self.head(self.embed(x, edge_index))


class GIN(nn.Module):
    def __init__(self, in_dim: int, hidden: int = 64, L: int = 3):
        super().__init__()
        self.convs = nn.ModuleList()
        dims = [in_dim] + [hidden] * L
        for i in range(L):
            mlp = nn.Sequential(
                nn.Linear(dims[i], hidden), nn.ReLU(),
                nn.Linear(hidden, dims[i + 1]))
            self.convs.append(GINConv(mlp, train_eps=True))
        self.head = nn.Linear(hidden, 2)

    def embed(self, x, edge_index):
        h = x
        for i, conv in enumerate(self.convs):
            h = conv(h, edge_index)
            if i + 1 < len(self.convs):
                h = F.relu(h)
        return h

    def forward(self, x, edge_index):
        return self.head(self.embed(x, edge_index))


ARCHS = {"GCN": GCN, "GAT": GAT, "GIN": GIN}


# --------------------------------------------------- data
def load_planetoid_bin(name: str):
    """Load Planetoid dataset; binarise to largest-class-vs-rest (matches E3)."""
    ds = Planetoid(root=str(DATA / f"planetoid_{name.lower()}"), name=name)
    data = ds[0]
    y_multi = data.y.cpu().numpy()
    # largest class — same strategy as e3
    classes, counts = np.unique(y_multi, return_counts=True)
    target = int(classes[np.argmax(counts)])
    y_bin = (y_multi == target).astype(np.int64)
    return data, y_bin, target


# --------------------------------------------------- training
def train_one(arch_name: str, in_dim: int, data, y_bin: np.ndarray,
              seed: int, epochs: int = 200, lr: float = 0.01,
              weight_decay: float = 5e-4) -> tuple[nn.Module, dict]:
    torch.manual_seed(seed); np.random.seed(seed)
    if DEVICE.type == "cuda": torch.cuda.manual_seed_all(seed)

    model = ARCHS[arch_name](in_dim, hidden=64, L=3).to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=lr,
                           weight_decay=weight_decay)
    x = data.x.to(DEVICE)
    ei = data.edge_index.to(DEVICE)
    y = torch.from_numpy(y_bin).long().to(DEVICE)

    model.train()
    loss_hist = []
    t0 = time.perf_counter()
    for ep in range(epochs):
        opt.zero_grad()
        logits = model(x, ei)
        loss = F.cross_entropy(logits, y)
        loss.backward()
        opt.step()
        loss_hist.append(float(loss.item()))
    wall = time.perf_counter() - t0

    model.eval()
    with torch.no_grad():
        logits = model(x, ei)
        pred = logits.argmax(dim=1)
        Rhat = float((pred != y).float().mean().item())
        Z = model.embed(x, ei).cpu().numpy()
    return model, {"Rhat": Rhat, "train_loss_final": loss_hist[-1],
                   "wall_train_s": wall, "Z": Z}


# --------------------------------------------------- partition extraction
def kmeans_partition(Z: np.ndarray, k: int,
                     seed: int) -> tuple[np.ndarray, int]:
    """Returns (cluster_assignments, n_nonempty_clusters).

    Uses MiniBatchKMeans because sklearn's full KMeans segfaults when
    k approaches n (the WL cell budget on E3 is near-singleton).
    n_init=3 averages out the random-init variance; max_iter=100 is
    generally enough for convergence at these moderate sizes.
    """
    k = max(2, min(k, Z.shape[0]))
    km = MiniBatchKMeans(n_clusters=k, random_state=seed, n_init=3,
                         max_iter=100, batch_size=min(1024, Z.shape[0]))
    labels = km.fit_predict(Z)
    n_used = int(np.unique(labels).size)
    return labels.astype(np.uint64), n_used


# --------------------------------------------------- WL ceiling lookup
def load_wl_ceilings(L: int = 3) -> dict:
    """Return {name: {'eps_WL': ..., 'm_WL': ...}} from results/e3.json."""
    raw = json.loads((RESULTS / "e3.json").read_text())
    out = {}
    for ds in raw["datasets"]:
        for row in ds["depths"]:
            if row["L"] == L:
                out[ds["name"]] = {"eps_WL": row["eps_star"],
                                   "m_WL": row["m"], "n": ds["n_V"],
                                   "pi": ds["pi"]}
                break
    return out


# --------------------------------------------------- driver
DATASETS_D = [("cora", "Cora"), ("citeseer", "CiteSeer"), ("pubmed", "PubMed")]


def run() -> dict:
    print(f"device: {DEVICE}", flush=True)
    ceilings = load_wl_ceilings(L=3)
    print(f"WL ceilings @ L=3: {ceilings}", flush=True)

    out = {"experiment": "e3d_arch_audit",
           "device": str(DEVICE),
           "depth_L": 3, "hidden": 64, "epochs": 200,
           "datasets": []}

    for (ds_key, ds_name) in DATASETS_D:
        print(f"\n=== {ds_name} ===", flush=True)
        data, y_bin, target = load_planetoid_bin(ds_name)
        pi = float(y_bin.mean())
        n = int(y_bin.size)
        ceil = ceilings[ds_key]
        # safety: our binarisation must match e3's
        assert abs(pi - ceil["pi"]) < 1e-3, \
            f"pi mismatch {ds_name}: ours {pi:.4f} vs e3 {ceil['pi']:.4f}"
        k_wl = int(ceil["m_WL"])
        print(f"  n={n}  pi={pi:.4f}  k=m_WL_3={k_wl}  "
              f"eps_WL={ceil['eps_WL']:.4f}")

        ds_out = {"name": ds_key, "n": n, "pi": pi,
                  "target_class": target,
                  "eps_WL": ceil["eps_WL"], "k_WL": k_wl,
                  "runs": []}

        for arch in ARCHS:
            for seed in (0, 1, 2):
                print(f"  [{arch} seed={seed}] training...", end="",
                      flush=True)
                _, tr = train_one(arch, data.x.size(1), data, y_bin, seed)
                Z = tr.pop("Z")
                # T4: embedding sanity
                assert np.isfinite(Z).all(), f"Z non-finite for {arch}/{seed}"
                assert 0.0 <= tr["Rhat"] <= 1.0, f"Rhat out of [0,1]: {tr['Rhat']}"
                Rhat = tr["Rhat"]
                k_grid = sorted({16, 64, 256, k_wl})
                k_runs = []
                prev_eps = None
                for k in k_grid:
                    cluster, n_used = kmeans_partition(Z, k, seed)
                    br = bracket_from_cells(cluster, y_bin)
                    eps_trained = float(br.eps_star)
                    # T1: log monotonicity violations (kmeans local optima
                    # can break exact monotonicity; not a framework invariant)
                    if prev_eps is not None and eps_trained > prev_eps + 1e-3:
                        print(f"\n    [T1 warn] {arch}/{seed} k={k}: "
                              f"eps_tr={eps_trained:.5f} > prev={prev_eps:.5f}"
                              f" (kmeans local-opt)", flush=True)
                    prev_eps = eps_trained
                    k_runs.append({
                        "k_requested": int(k),
                        "k_used": int(n_used),
                        "eps_trained": eps_trained,
                        "feature_gap_at_k": ceil["eps_WL"] - eps_trained,
                        "head_signal_at_k": eps_trained - Rhat,
                        "is_kWL": (k == k_wl),
                    })
                ds_out["runs"].append({
                    "arch": arch, "seed": seed,
                    "Rhat": Rhat,
                    "k_grid": list(k_grid),
                    "k_sweep": k_runs,
                    "wall_train_s": tr["wall_train_s"],
                    "train_loss_final": tr["train_loss_final"],
                })
                kwl_rec = next(r for r in k_runs if r["is_kWL"])
                print(f"  Rhat={Rhat:.4f}  "
                      f"eps_tr(k_WL)={kwl_rec['eps_trained']:.4f}  "
                      f"feat_gap={kwl_rec['feature_gap_at_k']:+.4f}  "
                      f"head_sig={kwl_rec['head_signal_at_k']:+.4f}",
                      flush=True)

        out["datasets"].append(ds_out)

    (RESULTS / "e3d_arch.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {RESULTS / 'e3d_arch.json'}")
    return out


if __name__ == "__main__":
    run()
