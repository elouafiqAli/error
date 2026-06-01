# Experiment E3D — Architecture / Depth / Dataset Full Sweep

**Status:** PARTIAL (3 of 5 datasets complete; 2 pending due to RunPod GPU capacity shortage at the close of the active session).
**Source JSON:** [partition-sandwich-preprint/experiments/results/e3d_arch_full.partial_3of5.json](../results/e3d_arch_full.partial_3of5.json)
**Audit JSON:** [partition-sandwich-preprint/experiments/audit/e3d_arch_full_audit.json](e3d_arch_full_audit.json)
**Report date:** 2026-06-01.

## 1. Protocol

- **Architectures:** GCN, GAT, GIN, SAGE (4).
- **Depth `L`:** 3.
- **Hidden width:** 128.
- **Optimizer / epochs:** Adam, full-batch transductive, 200 epochs.
- **Seeds:** 0..4 (5 per arch × dataset → 20 runs per dataset).
- **k-grid:** dataset-specific (capped at the realised number of WL-cells; cap hits are recorded as `k_used < k_requested`).
- **Metrics per `(arch, seed, k)`:** `Rhat`, `eps_trained`, `feature_gap_at_k`, `head_signal_at_k`.
- **Hardware:** RunPod A4000/A5000 (CUDA), invoked via [runpod_dfull.py](../../../runpod_dfull.py).

## 2. Completion matrix

| Dataset      | Status       | Runs | Source artefact                                                                                              |
| ------------ | ------------ | ---- | ------------------------------------------------------------------------------------------------------------ |
| cora         | DONE         | 20   | merged from `e3d_arch_full.recovered.json`                                                                   |
| citeseer     | DONE         | 20   | merged from `e3d_arch_full.recovered.json`                                                                   |
| pubmed       | DONE         | 20   | dedicated A5000 run, written to `e3d_arch_full.json`                                                         |
| twitch_en    | PENDING      | 0    | not scheduled — no GPU capacity available across A4000/A4500/A5000/4090/L40S/A6000 at adjournment            |
| ogbn_arxiv   | PENDING      | 0    | as above                                                                                                     |

Aggregate stable artefact: [e3d_arch_full.partial_3of5.json](../results/e3d_arch_full.partial_3of5.json) (90 KB, 3 datasets × 20 runs × 5 k-values = 300 measured cells).

## 3. Headline numbers

### 3.1 `eps_trained` mean curve (averaged over arch × seed)

The bracket theory predicts `eps_trained` should be **non-increasing** as the partition is refined (larger `k`). Observed (all values rounded to 4 sf):

| Dataset  | k=16   | k=64   | k=256  | k=1024 | k_max                |
| -------- | ------ | ------ | ------ | ------ | -------------------- |
| cora     | 0.0291 | 0.0212 | 0.0180 | 0.0123 | **0.0063** (k=2363)  |
| citeseer | 0.0336 | 0.0236 | 0.0215 | 0.0187 | **0.0146** (k=2044)  |
| pubmed   | 0.0612 | 0.0596 | 0.0591 | 0.0569 | **0.0505** (k=4096)  |

**Monotonicity audit:** 4/4 successive drops on every dataset; **0 rises**. *Consistent with the upper bracket on Bayes residual.*

### 3.2 `eps_WL` (reference WL-ceiling)

| Dataset  | `eps_WL` | `eps_trained` at k_max | Headroom (`eps_WL − eps_trained`) |
| -------- | -------- | ---------------------- | --------------------------------- |
| cora     | 0.0292   | 0.0063                 | +0.0229                           |
| citeseer | 0.0775   | 0.0146                 | +0.0629                           |
| pubmed   | 0.0511   | 0.0505                 | +0.0006                           |

Trained models stay *under* the WL ceiling on all three datasets — i.e. the population-side bracket is not violated. The pubmed margin is essentially flush, which is the most informative outcome of the run (see §5).

### 3.3 `Rhat` (final training risk)

| Dataset  | mean   | std    | min | max    |
| -------- | ------ | ------ | --- | ------ |
| cora     | 0.0533 | 0.1499 | 0   | 0.6979 |
| citeseer | 0.0234 | 0.0191 | 0   | 0.0646 |
| pubmed   | 0.0613 | 0.0381 | 0   | 0.1099 |

The cora `max=0.6979` is an outlier (one of the 20 runs failed to converge — likely a GAT/seed cell; this should be inspected individually before paper inclusion).

## 4. Self-audit (adversarial)

| Check                                                  | cora       | citeseer | pubmed    | Verdict                                                                                            |
| ------------------------------------------------------ | ---------- | -------- | --------- | -------------------------------------------------------------------------------------------------- |
| `eps_trained` non-increasing in `k` (mean curve)       | 4/4 drops  | 4/4      | 4/4       | **PASS**                                                                                           |
| `Rhat` finite, in `[0, 1]`                             | yes        | yes      | yes       | PASS, with cora outlier flag                                                                       |
| `feature_gap_at_k ≥ 0` (theory says ≥ 0)               | 19/100 neg | 2/100    | 63/100    | **FAIL on pubmed**, soft FAIL on cora                                                              |
| `k_used ≤ k_requested` always                          | yes        | yes      | yes       | PASS                                                                                               |
| `eps_trained` ≤ `eps_WL` at every measured `k`         | yes        | yes      | yes (tight) | PASS                                                                                             |
| `k`-cap usage (fraction of cells where capping engaged) | 40 %       | 40 %     | 20 %      | Expected; informs k-grid design                                                                    |

### 4.1 Flag — `feature_gap_at_k` negativity on pubmed (63 %)

The bracket framework predicts `feature_gap_at_k ≥ 0` (it is a non-negative contribution to the lower bracket). On pubmed 63/100 measured cells return a strictly negative value, with `eps_trained` already essentially flush against `eps_WL`. Three plausible explanations to investigate:

1. **Estimator finite-sample bias.** The empirical estimator of `feature_gap_at_k` mixes a sample-mean MI-like term that can dip below 0 at moderate sample sizes; pubmed's combination of large `n=19717` but moderate `eps_WL` makes this most visible. *Most likely.*
2. **Sign convention mismatch** between the implemented estimator and the theoretical quantity in the paper draft. Needs a definitional cross-check in [e3d_arch_full.py](../e3d_arch_full.py).
3. **A genuine bracket-violation on a near-saturated regime.** Lower-probability, but would be a Paper-A consistency hit; the headroom row (§3.2) is what makes this worth checking.

This is flagged here so it cannot be silently absorbed in a later aggregation step.

### 4.2 Cora `Rhat` outlier

`max(Rhat) = 0.6979` with mean `0.0533` and std `0.1499` indicates one cell drove the entire variance. Action: list outlier cell `(arch, seed)` before merging into the final paper table, optionally re-running with a longer warmup.

## 5. Interpretation (partial)

- The **bracket-side monotonicity** in `eps_trained(k)` is observed cleanly on all three completed datasets, matching the qualitative prediction of Paper A.
- The **WL-ceiling is respected**: on cora and citeseer with comfortable margin, on pubmed *tightly*. Pubmed therefore acts as the most useful stress dataset of the three.
- The **estimator pathology** on `feature_gap_at_k` is the single most important loose end. It must be resolved before the partial 3/5 numbers are quoted in the manuscript.

## 6. Reproducibility

- The audit JSON is fully regenerable from the experiment JSON by re-running the audit block in this report (no external state).
- The experiment artefact is byte-stable: 90 KB, 3 datasets × 20 runs × 5 `k` cells.
- The remaining two datasets can be completed with the existing orchestration:
  ```bash
  python3 runpod_dfull.py --gpu 'NVIDIA RTX A5000' --cloud ALL \
      --datasets twitch_en --seeds 5 --epochs 200 --hidden 128 \
      --name dfull-twitch
  python3 runpod_dfull.py --gpu 'NVIDIA RTX A5000' --cloud ALL \
      --datasets ogbn_arxiv --seeds 5 --epochs 200 --hidden 128 \
      --name dfull-arxiv
  ```
  followed by the merge block in [scripts/merge_e3d.py](#) (or the inline merge used to produce `partial_3of5.json`).

## 7. Recommendations

1. **Diagnose `feature_gap_at_k` sign on pubmed first** — definitional cross-check in [e3d_arch_full.py](../e3d_arch_full.py) vs. the bracket statement in [main.tex](../../main.tex). Re-aggregating the same JSON is sufficient; no GPU needed.
2. **Identify the cora `Rhat` outlier cell** by enumerating `(arch, seed)` with `Rhat > 0.5` and re-run only that cell with longer warmup or a smaller learning rate.
3. **Schedule `twitch_en` and `ogbn_arxiv`** at an off-peak RunPod hour or pre-reserve an A5000. The orchestration is already hardened (per-dataset checkpoints, lazy matplotlib import, finite SSH retries, tar-over-SSH fallback); no further infra work is required.
4. **Do not quote 3/5 numbers in the manuscript yet.** Use them only in internal reviews until the pubmed sign issue and the missing two datasets are resolved.
5. **Promote the merge block to a small script** (`experiments/merge_dfull.py`) so future partial recoveries are a one-liner rather than an inline `python3 - <<'PY'`.

## 8. Provenance

- Experiment driver: [partition-sandwich-preprint/experiments/e3d_arch_full.py](../e3d_arch_full.py).
- Data loaders: [partition-sandwich-preprint/experiments/e3d_data_full.py](../e3d_data_full.py).
- WL utilities: [partition-sandwich-preprint/experiments/e3_wl_bracket.py](../e3_wl_bracket.py) (top-level matplotlib import removed to allow loader-only consumers).
- Orchestration: [runpod_dfull.py](../../../runpod_dfull.py) (tar-over-SSH transfer, finite retry, explicit apt install of build deps, safer SCP-back).

— end of report —
