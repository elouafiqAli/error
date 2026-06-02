"""Modal app — GPU-centered, invocable from notebook cells.

Usage from a notebook cell (after `pip install modal && modal token new`):

    import modal
    from onboarding.projects.modal_app import app, ping, train_gcn, nas_sweep

    with app.run():
        print(ping.remote())                       # CPU smoke test
        result = train_gcn.remote(epochs=200)      # GPU
        sweep  = nas_sweep.remote(architectures=["gcn", "gin", "sage"])

Every GPU function caches the Planetoid datasets in the persistent
`modal.Volume("cora")` so re-runs do not re-download.

This module is *import-safe without Modal installed*: when `modal`
cannot be imported we expose stub functions that raise on `.remote()`
but allow `from modal_app import train_gcn` to succeed (which is
what unit tests need).
"""
from __future__ import annotations

import os
from typing import Any

try:
    import modal
    _MODAL_OK = True
except ImportError:
    _MODAL_OK = False


# --------------------------------------------------------------------------- #
# Modal app + image definition.
# --------------------------------------------------------------------------- #
if _MODAL_OK:
    image = (
        modal.Image.debian_slim(python_version="3.11")
        .pip_install(
            "torch==2.3.0",
            "torch-geometric==2.5.3",
            "numpy>=1.24",
            "scikit-learn>=1.3",
        )
    )
    app = modal.App("gnn-express-capstone", image=image)
    cora_vol = modal.Volume.from_name("cora", create_if_missing=True)
    DATA_ROOT = "/data"
else:
    image = None
    app = None
    cora_vol = None
    DATA_ROOT = "./data"


# --------------------------------------------------------------------------- #
# CPU smoke test — verifies Modal wiring without spending GPU dollars.
# --------------------------------------------------------------------------- #
if _MODAL_OK:
    @app.function(cpu=1, timeout=60)
    def ping() -> str:
        return "pong"
else:
    def ping() -> str:  # type: ignore[misc]
        return "pong (local; modal not installed)"


# --------------------------------------------------------------------------- #
# GPU training — Cora node classification with a 2-layer GCN.
# --------------------------------------------------------------------------- #
def _train_gcn_impl(
    epochs: int = 200,
    hidden: int = 64,
    lr: float = 0.01,
    weight_decay: float = 5e-4,
    seed: int = 0,
    data_root: str | None = None,
) -> dict[str, Any]:
    """Train a 2-layer GCN on Cora; return val/test accuracy + logits."""
    import torch
    import torch.nn.functional as F
    from torch_geometric.datasets import Planetoid
    from torch_geometric.nn import GCNConv

    torch.manual_seed(seed)
    root = data_root or DATA_ROOT
    dataset = Planetoid(root=root, name="Cora")
    data = dataset[0]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = data.to(device)

    class GCN(torch.nn.Module):
        def __init__(self, in_dim: int, hidden: int, out_dim: int) -> None:
            super().__init__()
            self.conv1 = GCNConv(in_dim, hidden)
            self.conv2 = GCNConv(hidden, out_dim)

        def forward(self, x, edge_index):
            x = F.relu(self.conv1(x, edge_index))
            x = F.dropout(x, p=0.5, training=self.training)
            return self.conv2(x, edge_index)

    model = GCN(dataset.num_features, hidden, dataset.num_classes).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    def _acc(mask):
        model.eval()
        with torch.no_grad():
            pred = model(data.x, data.edge_index).argmax(dim=-1)
        return float((pred[mask] == data.y[mask]).float().mean().item())

    for epoch in range(epochs):
        model.train()
        opt.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        opt.step()

    return {
        "device": str(device),
        "epochs": epochs,
        "val_acc": _acc(data.val_mask),
        "test_acc": _acc(data.test_mask),
        "loss_final": float(loss.item()),
    }


if _MODAL_OK:
    @app.function(
        gpu="T4",
        timeout=600,
        volumes={DATA_ROOT: cora_vol},
    )
    def train_gcn(**kwargs: Any) -> dict[str, Any]:
        return _train_gcn_impl(**kwargs)
else:
    def train_gcn(**kwargs: Any) -> dict[str, Any]:  # type: ignore[misc]
        raise RuntimeError(
            "modal not installed; use local_bench.train_gcn for the CPU mirror"
        )


# --------------------------------------------------------------------------- #
# GPU NAS pre-filter — small architecture menu, Kendall-τ against bracket.
# --------------------------------------------------------------------------- #
_DEFAULT_ARCHS = ("mlp", "gcn", "gin", "sage")


def _nas_sweep_impl(
    architectures: tuple[str, ...] = _DEFAULT_ARCHS,
    epochs: int = 100,
    seed: int = 0,
    data_root: str | None = None,
) -> dict[str, Any]:
    """Train each architecture once on Cora; return accuracy table.

    Light on purpose — M4's job is to show that the partition-bracket
    *prefilters* architectures correctly, not to win the benchmark.
    """
    import torch
    import torch.nn.functional as F
    from torch_geometric.datasets import Planetoid
    from torch_geometric.nn import GCNConv, GINConv, SAGEConv

    torch.manual_seed(seed)
    root = data_root or DATA_ROOT
    dataset = Planetoid(root=root, name="Cora")
    data = dataset[0]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = data.to(device)

    def _make(arch: str, in_dim: int, hidden: int, out_dim: int):
        if arch == "mlp":
            return torch.nn.Sequential(
                torch.nn.Linear(in_dim, hidden),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden, out_dim),
            )
        if arch == "gcn":
            class _M(torch.nn.Module):
                def __init__(s):
                    super().__init__()
                    s.c1 = GCNConv(in_dim, hidden); s.c2 = GCNConv(hidden, out_dim)
                def forward(s, x, ei): return s.c2(F.relu(s.c1(x, ei)), ei)
            return _M()
        if arch == "gin":
            class _M(torch.nn.Module):
                def __init__(s):
                    super().__init__()
                    mlp1 = torch.nn.Sequential(torch.nn.Linear(in_dim, hidden), torch.nn.ReLU(), torch.nn.Linear(hidden, hidden))
                    mlp2 = torch.nn.Sequential(torch.nn.Linear(hidden, hidden), torch.nn.ReLU(), torch.nn.Linear(hidden, out_dim))
                    s.c1 = GINConv(mlp1); s.c2 = GINConv(mlp2)
                def forward(s, x, ei): return s.c2(F.relu(s.c1(x, ei)), ei)
            return _M()
        if arch == "sage":
            class _M(torch.nn.Module):
                def __init__(s):
                    super().__init__()
                    s.c1 = SAGEConv(in_dim, hidden); s.c2 = SAGEConv(hidden, out_dim)
                def forward(s, x, ei): return s.c2(F.relu(s.c1(x, ei)), ei)
            return _M()
        raise ValueError(f"unknown arch: {arch}")

    results: dict[str, dict[str, float]] = {}
    for arch in architectures:
        model = _make(arch, dataset.num_features, 64, dataset.num_classes).to(device)
        opt = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
        for _ in range(epochs):
            model.train()
            opt.zero_grad()
            if arch == "mlp":
                out = model(data.x)
            else:
                out = model(data.x, data.edge_index)
            loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            out = model(data.x) if arch == "mlp" else model(data.x, data.edge_index)
            pred = out.argmax(dim=-1)
            test_acc = float((pred[data.test_mask] == data.y[data.test_mask]).float().mean().item())
        results[arch] = {"test_acc": test_acc}
    return {"device": str(device), "results": results}


if _MODAL_OK:
    @app.function(
        gpu="T4",
        timeout=1200,
        volumes={DATA_ROOT: cora_vol},
    )
    def nas_sweep(**kwargs: Any) -> dict[str, Any]:
        return _nas_sweep_impl(**kwargs)
else:
    def nas_sweep(**kwargs: Any) -> dict[str, Any]:  # type: ignore[misc]
        raise RuntimeError(
            "modal not installed; use local_bench.nas_sweep for the CPU mirror"
        )


__all__ = ["app", "ping", "train_gcn", "nas_sweep"]
