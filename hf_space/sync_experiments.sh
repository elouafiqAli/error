# sync hf_space/experiments/ from the canonical source.
# Run before deploying to keep Space code in lock-step with the paper repo.
set -euo pipefail
cd "$(dirname "$0")"
SRC=../partition-sandwich-preprint/experiments
mkdir -p experiments/results
cp "$SRC"/e3d_arch_full.py experiments/
cp "$SRC"/e3d_data_full.py experiments/
cp "$SRC"/common.py experiments/
cp "$SRC"/e3_wl_bracket.py experiments/
cp "$SRC"/results/e3.json experiments/results/
echo "synced experiments/ from $SRC"
