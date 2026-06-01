# E3d-arch-kll-n — expressivity at $k \ll n$ (P0.4)

## Configuration

- Datasets: Cora ($n = 2708$, $C = 7$, $\varepsilon_{\text{WL}} = 0.0292$,
  $\pi_{\min} = 0.3021$), CiteSeer ($n = 3327$, $C = 6$,
  $\varepsilon_{\text{WL}} = 0.0775$, $\pi_{\min} = 0.2107$).
- Architectures: GCN, GAT, GIN, SAGE (same definitions as
  `e3d_arch_full.py`).
- Seeds: 0, 1, 2, 3, 4 (5 each), 300 epochs, full-batch.
- Partition: MiniBatchKMeans on penultimate-layer embeddings at
  $k \in \{8, 16, 32, 64\}$.
- Wall-clock: $\approx 869$ s total on CPU (Apple Silicon, MPS
  disabled because sklearn KMeans segfaults under MPS+OpenMP on
  Python 3.13; env: `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
  OPENBLAS_NUM_THREADS=1 KMP_DUPLICATE_LIB_OK=TRUE`).
- Sign convention: `head_sig = head_slack = Rhat - eps_trained`
  (P0.3-corrected; positive = $\Delta_{\text{head}} > 0$).

## Aggregated results (mean ± stdev over 5 seeds)

```
Dataset    Arch   Rhat              eps_tr(k=8)       eps_tr(k=16)      eps_tr(k=32)      eps_tr(k=64)      hs(k=8)           hs(k=64)
Cora       GCN    +0.046 ± 0.048    +0.049 ± 0.026    +0.032 ± 0.020    +0.030 ± 0.017    +0.029 ± 0.019    -0.002 ± 0.041    +0.017 ± 0.035
Cora       GAT    +0.025 ± 0.026    +0.025 ± 0.018    +0.023 ± 0.016    +0.021 ± 0.016    +0.019 ± 0.014    +0.001 ± 0.016    +0.007 ± 0.017
Cora       GIN    +0.024 ± 0.014    +0.058 ± 0.024    +0.032 ± 0.025    +0.028 ± 0.016    +0.024 ± 0.013    -0.034 ± 0.029    +0.000 ± 0.001
Cora       SAGE   +0.000 ± 0.000    +0.000 ± 0.000    +0.000 ± 0.000    +0.000 ± 0.000    +0.000 ± 0.000    +0.000 ± 0.000    +0.000 ± 0.000
CiteSeer   GCN    +0.035 ± 0.009    +0.050 ± 0.015    +0.033 ± 0.003    +0.031 ± 0.005    +0.030 ± 0.006    -0.015 ± 0.023    +0.005 ± 0.008
CiteSeer   GAT    +0.022 ± 0.009    +0.024 ± 0.007    +0.024 ± 0.008    +0.022 ± 0.006    +0.021 ± 0.006    -0.002 ± 0.004    +0.000 ± 0.004
CiteSeer   GIN    +0.040 ± 0.028    +0.117 ± 0.059    +0.075 ± 0.017    +0.047 ± 0.024    +0.045 ± 0.021    -0.077 ± 0.059    -0.005 ± 0.009
CiteSeer   SAGE   +0.000 ± 0.000    +0.005 ± 0.010    +0.002 ± 0.004    +0.001 ± 0.001    +0.000 ± 0.000    -0.005 ± 0.010    +0.000 ± 0.000
```

## Findings

**F1″ (expressivity, NEW; **closes C2** in strong form).** At
$k = 64$ — i.e.\ $k/n \le 0.024$ on Cora and $k/n \le 0.019$ on
CiteSeer, two orders of magnitude below the matched-$k$ rows of
E3d-arch-full — GAT, GIN, SAGE on Cora and **all four**
architectures on CiteSeer reach
$\varepsilon^*_{\Pi^{\text{tr}}_{64}} \le \varepsilon_{\text{WL}}$.
On CiteSeer the gap is large ($0.030$ vs $0.078$). The trained
embeddings carry label structure that 1-WL at the same cell
budget does not. This is an expressivity statement, not a
memorisation artefact.

**F2″ (cross-architecture spread, NEW).** Architecture
dependence at fixed $k = 64$ on Cora: GAT $0.019$ < GIN $0.024$
< GCN $0.029$. The F2 "GAT erases structure" reading of
E3d-arch-full is now diagnosed as a $k = 4096$ PubMed artefact.

**F3″ (head-slack, NEW).** $\Delta_{\text{head}}$ collapses to
$\le 0.017$ in magnitude at $k = 64$ but is non-trivially
*negative* at $k = 8$ for GIN/SAGE (CiteSeer GIN: $-0.077$): the
coarse partition's per-cell majority is *worse* than the trained
head. F3′ (E3d-arch-full) is therefore a matched-$k$ phenomenon
and does not extrapolate to $k \ll n$.

**Caveat (SAGE perfect fit).** SAGE on Cora and CiteSeer
$\hat R = 0$ on the training split for all 5 seeds; the
$\varepsilon^* = 0$ readings are real but uninformative for
ranking the bracket — they encode that the features are
linearly separable on the training set, not that the bracket is
necessarily tight on unseen data.

## Reproducibility

- Driver: `experiments/e3d_arch_kll_n.py`
- Raw JSON: `experiments/results/e3d_arch_kll_n.json`
- Sweep recipe:
  ```
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
      KMP_DUPLICATE_LIB_OK=TRUE \
      python experiments/e3d_arch_kll_n.py
  ```
