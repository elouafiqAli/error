"""
e3d_arch_ogbn_kmeans.py
=======================

Phase 2 of the two-phase RunPod split for the E3d-arch-full ogbn-arxiv
slice. Reads Z_<arch>_<seed>.npz + meta.json + y_bin.npy from a directory
populated by e3d_arch_ogbn_train.py and assembles a JSON in the *exact*
schema of e3d_arch_full.twitch_only.json (so it merges cleanly with the
existing 4/5 file).

Bit-equivalence: imports `kmeans_partition` and `bracket_from_cells` from
`e3d_arch_full` and `common` respectively; only difference vs. the in-
process pipeline is that Z is loaded from disk (possibly in fp16, which
sklearn upcasts to fp32 internally — the bracket statistic depends only
on the discrete cluster IDs, which are identical to fp32 within sklearn's
deterministic seeded MiniBatchKMeans).

Designed to run on a CPU-only RunPod tier (8 vCPU, 16 GB RAM is plenty)
or locally on a Mac.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
if str(EXP) not in sys.path:
    sys.path.insert(0, str(EXP))

from common import bracket_from_cells  # noqa: E402
from e3d_arch_full import kmeans_partition  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--in-dir", required=True,
                   help="directory written by e3d_arch_ogbn_train.py")
    p.add_argument("--out", required=True,
                   help="destination JSON path (will mirror "
                        "e3d_arch_full.twitch_only.json schema)")
    p.add_argument("--archs", nargs="*", default=None,
                   help="optional subset filter")
    p.add_argument("--seeds", nargs="*", type=int, default=None,
                   help="optional subset filter")
    args = p.parse_args()

    in_dir = Path(args.in_dir)
    meta = json.loads((in_dir / "meta.json").read_text())
    y_bin = np.load(in_dir / "y_bin.npy")
    assert y_bin.shape == (meta["n"],), \
        f"y_bin shape {y_bin.shape} != ({meta['n']},)"

    archs = args.archs or meta["archs"]
    seeds = args.seeds or meta["seeds"]
    k_grid = meta["k_grid"]

    print(f"[phase2] dataset={meta['dataset']}  n={meta['n']}  "
          f"k_WL={meta['k_WL']}  eps_WL={meta['eps_WL']:.4f}  "
          f"k_grid={k_grid}",
          flush=True)
    print(f"[phase2] cells = {len(archs)} archs x {len(seeds)} seeds = "
          f"{len(archs)*len(seeds)}",
          flush=True)

    runs: list[dict] = []
    t0 = time.perf_counter()
    for arch in archs:
        for seed in seeds:
            t_cell = time.perf_counter()
            npz_path = in_dir / f"Z_{arch}_{seed}.npz"
            with np.load(npz_path, allow_pickle=False) as bundle:
                Z = bundle["Z"].astype(np.float32, copy=False)
                Rhat = float(bundle["Rhat"])
                train_loss_final = float(bundle["train_loss_final"])
                wall_train_s = float(bundle["wall_train_s"])

            k_runs = []
            for k in k_grid:
                cl, k_used = kmeans_partition(Z, k, seed)
                br = bracket_from_cells(cl, y_bin)
                eps_tr = float(br.eps_star)
                k_runs.append({
                    "k_requested": int(k),
                    "k_used": int(k_used),
                    "eps_trained": eps_tr,
                    "feature_gap_at_k": meta["eps_WL"] - eps_tr,
                    "head_signal_at_k": eps_tr - Rhat,
                })
            runs.append({
                "arch": arch,
                "seed": int(seed),
                "Rhat": Rhat,
                "train_loss_final": train_loss_final,
                "wall_train_s": wall_train_s,
                "wall_cell_s": time.perf_counter() - t_cell,
                "k_sweep": k_runs,
            })
            kref = k_runs[-1]
            print(f"  [phase2] {arch:5s} seed={seed}  Rhat={Rhat:.4f}  "
                  f"eps_tr(k={kref['k_requested']})={kref['eps_trained']:.4f}  "
                  f"feat_gap={kref['feature_gap_at_k']:+.4f}  "
                  f"cell_wall={runs[-1]['wall_cell_s']:.1f}s",
                  flush=True)

    total_wall_s = time.perf_counter() - t0

    out = {
        "experiment": "e3d_arch_full",
        "phase2_provenance": {
            "phase1_dir": str(in_dir),
            "phase1_meta": {k: meta[k] for k in
                            ("dataset", "device", "epochs", "hidden",
                             "depth_L", "z_dtype", "total_wall_s")},
        },
        "device": "cpu (phase2 k-means)",
        "depth_L": meta["depth_L"],
        "hidden": meta["hidden"],
        "epochs": meta["epochs"],
        "seeds": list(seeds),
        "archs": list(archs),
        "datasets": [
            {
                "name": meta["dataset"],
                "n": meta["n"],
                "in_dim": meta["in_dim"],
                "pi": meta["pi"],
                "target_class": meta["target_class"],
                "eps_WL": meta["eps_WL"],
                "k_WL": meta["k_WL"],
                "k_grid": k_grid,
                "runs": runs,
            }
        ],
        "total_wall_s": total_wall_s,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(f"[phase2] wrote {out_path}  "
          f"({len(runs)} runs, total wall {total_wall_s:.0f}s)",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
