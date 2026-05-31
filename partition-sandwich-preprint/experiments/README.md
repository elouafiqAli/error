# Empirical bracket experiments

Cheap-CPU companion experiments to *A Two-Sided Bayes-Error Bracket from
Partition-Conditional Entropy*. Each script materialises an architecture-induced
partition $\Pi$ on a real dataset, computes the bracket
$H_{\mathrm{bin}}^{-1}(H(f\mid\Pi)) \le \varepsilon^*_\Pi \le \tfrac12 H(f\mid\Pi)$
of Theorem 1, and emits a single figure plus a JSON manifest.

The preprint sources (`main.tex`, `main.md`) are intentionally **not** modified
by this folder; the figures are stand-alone artefacts.

## Setup

```bash
pip install -r requirements.txt
make all
```

Runtime is < 5 min on a laptop CPU (E2 dominates, ~2 min for k=1000 KMeans).

## Experiments

| ID | Script | Figure | Backs paragraph |
|----|--------|--------|-----------------|
| E5 | `e5_scatter.py`  | `figures/e5_achievable_region_scatter.pdf` | §3 achievable region $\widetilde A_2$; Cor. 2 uniform slack $w^*\approx 0.1610$ |
| E4 | `e4_duel.py`     | `figures/e4_duel_table.pdf`                | §1 (E3); §8 cross-architecture comparison at fixed cell budget |
| E1 | `e1_trees.py`    | `figures/e1_refinement_funnel.pdf`         | §5 refinement monotonicity (Prop. 4); §8.1 decision trees |
| E2 | `e2_vq_proxy.py` | `figures/e2_vq_zeroshot.pdf`               | §1 (E1, E2 — reject/certify cheaply); §8.2 vector quantisation |

E3 (MPNNs on `ogbn-arxiv` with GIN) requires PyTorch Geometric and a GPU; it is
deferred to a follow-up sprint.

## Verification gates (asserted by each script)

- **E5**: 0 bracket violations on 1000 random partitions; empirical max upper
  slack matches $w^* = \tfrac12 H_{\mathrm{bin}}(1/5) - 1/5$ to machine precision.
- **E4**: both architectures yield exactly $K=16$ cells; bracket holds for both.
- **E1**: per depth, lower $\le \varepsilon^* \le$ upper, training error $=
  \varepsilon^*$ (CART majority-vote leaves), $H(f\mid\Pi_d)$ monotone non-increasing.
- **E2**: per $k$, the downstream LR on one-hot cells matches $\varepsilon^*$
  within 1% — the partition is the entire story.

## Outputs

- `figures/*.pdf` — committed (the deliverable).
- `results/*.json` — per-experiment manifests (gitignored; regenerate via `make`).
- `data/adult.pkl` — cached UCI Adult dataset (gitignored).

## Datasets

UCI Adult Income (`ucimlrepo` ID=2, fallback to `sklearn.fetch_openml('adult')`).
~45k rows after dropna, one-hot + StandardScaler → 96-dim float32 features.
Binary target: income > 50K.

## Reproducibility

All scripts pin `random_state=0` (or `seed=20260531` for E5 to match `verify.jl`).
`make clean && make all` regenerates every figure deterministically.
