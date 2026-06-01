#!/usr/bin/env bash
# Phase 2 bootstrap — run inside a RunPod CPU-only pod with the
# `ogbn-arxiv-Z` network volume mounted at /workspace/vol.
#
# Recommended pod: 8 vCPU + 16 GB RAM, no GPU.
# Bill: ~$0.05–0.15 for 60–100 minutes of wall.
#
# Usage:
#   cd /workspace && bash gnn_express/partition-sandwich-preprint/experiments/runpod/phase2_pod_bootstrap.sh
set -euo pipefail

REPO_DIR="${REPO_DIR:-/workspace/gnn_express}"
VOL_DIR="${VOL_DIR:-/workspace/vol}"
IN_DIR="${IN_DIR:-$VOL_DIR/ogbn_artifacts}"
OUT_JSON="${OUT_JSON:-$VOL_DIR/e3d_arch_full.ogbn_only.json}"
EXP_DIR="$REPO_DIR/partition-sandwich-preprint/experiments"

if [[ ! -f "$IN_DIR/meta.json" ]]; then
  echo "[phase2] ERROR: $IN_DIR/meta.json missing. Run Phase 1 first." >&2
  exit 1
fi

# Minimal deps: numpy + scikit-learn + torch (importable for module path,
# but no CUDA needed). On the CPU pod we don't reinstall torch_geometric;
# kmeans + bracket only need common.py and the kmeans_partition helper.
pip install --quiet --upgrade scikit-learn numpy || true

# OMP_NUM_THREADS=1 avoids a known sklearn/OpenMP pthread_mutex_init
# crash that surfaces on Apple Silicon and on some RunPod CPU images
# where libgomp + libiomp clash. Setting it serial costs ~20% k-means
# wall vs. parallel but guarantees deterministic, crash-free execution.
export OMP_NUM_THREADS=1

cd "$EXP_DIR"
python -u runpod/e3d_arch_ogbn_kmeans.py \
    --in-dir "$IN_DIR" \
    --out "$OUT_JSON" \
    2>&1 | tee "$VOL_DIR/phase2.log"

echo
echo "[phase2] complete. Pull the JSON to your laptop:"
echo "  runpodctl receive <CODE>   # see runpodctl send --help"
echo "or download via the RunPod web UI from:"
echo "  $OUT_JSON"
