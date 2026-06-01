"""
e3d_arch_ogbn_train.py
======================

Phase 1 of the two-phase RunPod split for the E3d-arch-full ogbn-arxiv slice
(see runpod/README.md for the operational story).

Loops the existing `train_one()` from `e3d_arch_full` over
{GCN, GAT, GIN, SAGE} × {0..4} on a chosen dataset (default: ogbn_arxiv),
and dumps the penultimate embeddings Z plus per-cell training metadata to
disk as compressed `.npz` files.

Output layout (all under --out-dir):

    meta.json                         # {n, in_dim, pi, target_class, eps_WL,
                                      #  k_WL, k_grid, archs, seeds, hidden,
                                      #  L, epochs, dataset, device, walls}
    y_bin.npy                         # uint8, shape (n,)
    Z_<arch>_<seed>.npz               # arch, seed, Rhat, train_loss_final,
                                      #  wall_train_s, Z (fp16 by default)

The output volume is intentionally CPU-/k-means-ready: pass the same
--out-dir to e3d_arch_ogbn_kmeans.py and it will produce a JSON in the
exact schema of e3d_arch_full.*.json.

Bit-equivalence to the in-process pipeline (e3d_arch_full.run_dataset) is
guaranteed because we import train_one directly and only persist its
outputs; k-means determinism is preserved by the seed already passed to
MiniBatchKMeans in the next phase.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch

# Make the parent experiments/ dir importable when launched from any cwd.
HERE = Path(__file__).resolve().parent
EXP = HERE.parent
if str(EXP) not in sys.path:
    sys.path.insert(0, str(EXP))

from e3d_arch_full import (ARCH_ORDER, pick_device, train_one)  # noqa: E402
from e3d_data_full import load, load_wl_ceilings  # noqa: E402


def _k_grid_for(k_wl: int, n: int) -> list[int]:
    raw = sorted({16, 64, 256, 1024, min(k_wl, 4096)})
    return [k for k in raw if 2 <= k <= n]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="ogbn_arxiv",
                   help="dataset key understood by e3d_data_full.load")
    p.add_argument("--seeds", nargs="*", type=int,
                   default=[0, 1, 2, 3, 4])
    p.add_argument("--archs", nargs="*", default=ARCH_ORDER,
                   help=f"subset of {ARCH_ORDER}")
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--hidden", type=int, default=128)
    p.add_argument("--depth-L", type=int, default=3)
    p.add_argument("--out-dir", required=True,
                   help="directory (on the RunPod volume) for .npz dumps")
    p.add_argument("--z-dtype", default="float16",
                   choices=["float16", "float32"],
                   help="dtype for Z dump (float16 halves disk + bracket "
                        "math is invariant)")
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    device = pick_device()
    print(f"[phase1] device={device}  out_dir={out_dir}", flush=True)

    data, y_bin, target = load(args.dataset)
    ceilings = load_wl_ceilings(L=args.depth_L)
    ceil = ceilings[args.dataset]
    n = int(data.num_nodes)
    in_dim = int(data.x.size(1))
    pi = float(y_bin.mean())
    k_grid = _k_grid_for(ceil["m_WL"], n)

    print(f"[phase1] {args.dataset}  n={n}  |E|={data.edge_index.size(1)}  "
          f"d_in={in_dim}  pi={pi:.4f}  k_WL={ceil['m_WL']}  "
          f"eps_WL={ceil['eps_WL']:.4f}  k_grid={k_grid}",
          flush=True)

    # Persist y_bin once.
    np.save(out_dir / "y_bin.npy", y_bin.astype(np.uint8))

    x = data.x.to(device)
    ei = data.edge_index.to(device)
    y = torch.from_numpy(y_bin).long().to(device)

    walls: list[dict] = []
    t0 = time.perf_counter()
    z_dtype = np.float16 if args.z_dtype == "float16" else np.float32
    for arch in args.archs:
        for seed in args.seeds:
            t_cell = time.perf_counter()
            tr = train_one(arch, in_dim, x, ei, y, seed,
                           hidden=args.hidden, L=args.depth_L,
                           epochs=args.epochs, device=device)
            Z = tr.pop("Z").astype(z_dtype, copy=False)
            assert np.isfinite(Z).all(), (
                f"Z non-finite {args.dataset}/{arch}/{seed}")
            assert 0.0 <= tr["Rhat"] <= 1.0
            out_path = out_dir / f"Z_{arch}_{seed}.npz"
            np.savez_compressed(
                out_path,
                Z=Z,
                arch=np.array(arch),
                seed=np.array(seed, dtype=np.int64),
                Rhat=np.array(tr["Rhat"], dtype=np.float64),
                train_loss_final=np.array(tr["train_loss_final"],
                                          dtype=np.float64),
                wall_train_s=np.array(tr["wall_train_s"],
                                      dtype=np.float64),
            )
            cell_wall = time.perf_counter() - t_cell
            walls.append({"arch": arch, "seed": int(seed),
                          "wall_train_s": tr["wall_train_s"],
                          "wall_cell_s": cell_wall,
                          "Rhat": tr["Rhat"],
                          "train_loss_final": tr["train_loss_final"]})
            print(f"  [phase1] {arch:5s} seed={seed}  Rhat={tr['Rhat']:.4f}"
                  f"  loss={tr['train_loss_final']:.4f}"
                  f"  train_wall={tr['wall_train_s']:.1f}s"
                  f"  cell_wall={cell_wall:.1f}s"
                  f"  -> {out_path.name} ({Z.nbytes/1e6:.1f} MB raw)",
                  flush=True)

    total_wall_s = time.perf_counter() - t0

    meta = {
        "phase": "phase1_train_dump_Z",
        "dataset": args.dataset,
        "n": n,
        "edges": int(data.edge_index.size(1)),
        "in_dim": in_dim,
        "pi": pi,
        "target_class": int(target),
        "eps_WL": ceil["eps_WL"],
        "k_WL": ceil["m_WL"],
        "k_grid": k_grid,
        "archs": list(args.archs),
        "seeds": list(args.seeds),
        "hidden": args.hidden,
        "depth_L": args.depth_L,
        "epochs": args.epochs,
        "device": str(device),
        "z_dtype": args.z_dtype,
        "total_wall_s": total_wall_s,
        "per_cell_walls": walls,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"[phase1] wrote meta.json + {len(args.archs)*len(args.seeds)} "
          f"Z_*.npz to {out_dir}  total_wall={total_wall_s:.0f}s",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
