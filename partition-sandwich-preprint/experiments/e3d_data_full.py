"""
e3d_data_full.py
================

D-Full data loaders. Each returns a torch_geometric Data object plus the
binarised label vector and the WL ceiling row from e3.json.

The five datasets:
  - cora, citeseer, pubmed  : native bag-of-words features (Planetoid)
  - twitch_en               : no native features -> 9-dim
                              (degree-bucket one-hot + normalised degree)
  - ogbn_arxiv              : native 128-dim word2vec features

Binarisation strategy: largest class vs rest (same as e3 baseline).
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import torch
from torch_geometric.data import Data
from torch_geometric.datasets import Planetoid

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
RESULTS = HERE / "results"
DATA.mkdir(exist_ok=True)


def _binarise_largest(y_multi: np.ndarray) -> tuple[np.ndarray, int]:
    classes, counts = np.unique(y_multi, return_counts=True)
    target = int(classes[np.argmax(counts)])
    return (y_multi == target).astype(np.int64), target


def _load_planetoid(name_cap: str):
    ds = Planetoid(root=str(DATA / f"planetoid_{name_cap.lower()}"),
                   name=name_cap)
    data = ds[0]
    y_bin, target = _binarise_largest(data.y.cpu().numpy())
    return data, y_bin, target


def _load_twitch_en():
    """Twitch-EN MUSAE -- structural only, build 9-dim degree features."""
    import sys
    sys.path.insert(0, str(HERE))
    from e3_wl_bracket import load_twitch_en as _lt  # reuse CSR loader
    name, n, indptr, indices, y, _deg = _lt()
    # CSR -> edge_index (undirected, both directions already in indices)
    src = np.repeat(np.arange(n, dtype=np.int64),
                    indptr[1:] - indptr[:-1])
    dst = indices.astype(np.int64)
    edge_index = torch.from_numpy(np.stack([src, dst])).long()
    deg = (indptr[1:] - indptr[:-1]).astype(np.float64)
    # 8-bin log2(deg+1) one-hot + normalised degree
    bucket = np.clip(np.floor(np.log2(deg + 1.0)).astype(np.int64), 0, 7)
    onehot = np.zeros((n, 8), dtype=np.float32)
    onehot[np.arange(n), bucket] = 1.0
    deg_n = (deg / max(deg.max(), 1.0)).astype(np.float32)
    x = np.concatenate([onehot, deg_n[:, None]], axis=1)
    data = Data(x=torch.from_numpy(x).float(),
                edge_index=edge_index)
    data.num_nodes = n
    return data, y.astype(np.int64), -1


def _load_ogbn_arxiv():
    import sys
    sys.path.insert(0, str(HERE))
    # use the e3 loader's monkeypatch to get raw arrays + features
    _orig_load = torch.load
    def _load_unsafe(*a, **kw):
        kw.setdefault("weights_only", False)
        return _orig_load(*a, **kw)
    torch.load = _load_unsafe
    try:
        from ogb.nodeproppred import NodePropPredDataset
        ds = NodePropPredDataset(name="ogbn-arxiv",
                                 root=str(DATA / "ogb"))
    finally:
        torch.load = _orig_load
    graph, labels = ds[0]
    n = int(graph["num_nodes"])
    ei = graph["edge_index"].astype(np.int64)
    # symmetrise
    ei_sym = np.concatenate([ei, ei[[1, 0]]], axis=1)
    edge_index = torch.from_numpy(ei_sym).long()
    x = torch.from_numpy(graph["node_feat"].astype(np.float32))
    y_multi = np.asarray(labels).reshape(-1).astype(np.int64)
    y_bin, target = _binarise_largest(y_multi)
    data = Data(x=x, edge_index=edge_index)
    data.num_nodes = n
    return data, y_bin, target


LOADERS = {
    "cora":       lambda: _load_planetoid("Cora"),
    "citeseer":   lambda: _load_planetoid("CiteSeer"),
    "pubmed":     lambda: _load_planetoid("PubMed"),
    "twitch_en":  _load_twitch_en,
    "ogbn_arxiv": _load_ogbn_arxiv,
}

DATASET_ORDER = ["cora", "citeseer", "pubmed", "twitch_en", "ogbn_arxiv"]


def load_wl_ceilings(L: int = 3) -> dict:
    """Return {name: {eps_WL, m_WL, n, pi}} from e3.json @ depth L."""
    raw = json.loads((RESULTS / "e3.json").read_text())
    out = {}
    for ds in raw["datasets"]:
        for row in ds["depths"]:
            if row["L"] == L:
                out[ds["name"]] = {
                    "eps_WL": row["eps_star"],
                    "m_WL":   row["m"],
                    "n":      ds["n_V"],
                    "pi":     ds["pi"],
                }
                break
    return out


def load(name: str):
    """Return (Data, y_bin np.int64, target_class). Caches on disk."""
    return LOADERS[name]()


if __name__ == "__main__":
    # smoke
    for n in DATASET_ORDER:
        try:
            data, y, tgt = load(n)
            print(f"{n:12s}  n={data.num_nodes:>7d}  "
                  f"|E|={data.edge_index.size(1):>9d}  "
                  f"d_in={data.x.size(1):>4d}  "
                  f"pi={float(y.mean()):.4f}  target={tgt}")
        except Exception as e:
            print(f"{n:12s}  FAIL: {e}")
