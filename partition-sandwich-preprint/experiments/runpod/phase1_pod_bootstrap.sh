#!/usr/bin/env bash
# Phase 1 bootstrap — run inside a RunPod GPU pod with the
# `ogbn-arxiv-Z` network volume mounted at /workspace/vol.
#
# Recommended pod: 1× L4 24 GB (or RTX 3090 24 GB).
# Bill: ~$0.05–0.10 for 5–15 minutes of wall.
#
# Usage (paste into the RunPod web shell after the pod boots):
#   cd /workspace && bash gnn_express/partition-sandwich-preprint/experiments/runpod/phase1_pod_bootstrap.sh
set -euo pipefail

REPO_DIR="${REPO_DIR:-/workspace/gnn_express}"
VOL_DIR="${VOL_DIR:-/workspace/vol}"
OUT_DIR="${OUT_DIR:-$VOL_DIR/ogbn_artifacts}"
EXP_DIR="$REPO_DIR/partition-sandwich-preprint/experiments"
DATASET="${DATASET:-ogbn_arxiv}"

mkdir -p "$OUT_DIR"

# 1. Confirm pytorch + CUDA are alive.
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'n/a')"

# 2. Install Python deps if pod image doesn't already ship them.
pip install --quiet --upgrade ogb torch_geometric scikit-learn || true

# 3. Pre-warm the ogbn-arxiv download into the volume (cached across reboots).
python - <<'PY'
import os
from pathlib import Path
root = Path(os.environ.get("VOL_DIR", "/workspace/vol")) / "data" / "ogb"
root.mkdir(parents=True, exist_ok=True)
from ogb.nodeproppred import NodePropPredDataset
NodePropPredDataset(name="ogbn-arxiv", root=str(root))
print("[bootstrap] ogbn-arxiv cached at", root)
PY

# 4. Run Phase 1: train all 20 cells, dump Z + meta.json + y_bin.npy.
#    The experiments scripts default to data/ under EXP_DIR; soft-link
#    the volume cache so we don't re-download.
ln -sfn "$VOL_DIR/data" "$EXP_DIR/data"

cd "$EXP_DIR"
python -u runpod/e3d_arch_ogbn_train.py \
    --dataset "$DATASET" \
    --seeds 0 1 2 3 4 \
    --epochs 200 \
    --hidden 128 \
    --out-dir "$OUT_DIR" \
    --z-dtype float16 \
    2>&1 | tee "$OUT_DIR/phase1.log"

echo
echo "[bootstrap] Phase 1 complete. Volume contents:"
ls -lh "$OUT_DIR"
echo
echo "Next: STOP this pod (do not terminate). Spin a CPU-only pod with"
echo "the same volume mounted, then run phase2_pod_bootstrap.sh."
