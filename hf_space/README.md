---
title: D-Full GNN Bracket Audit
emoji: 📐
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: Partition-bracket audit of GNNs on 5 graphs
hf_oauth: false
---

# D-Full: Post-hoc partition-bracket architecture-vs-WL audit

Runs the **D-Full** experiment from the partition-sandwich paper
(`partition-sandwich-preprint/main.tex` §8.5, table `tab:e3d-arch`):

- **5 datasets**: `cora`, `citeseer`, `pubmed`, `twitch_en`, `ogbn_arxiv`
- **4 architectures**: GCN, GAT, GIN, GraphSAGE (3-layer, hidden 128)
- **5 seeds** (0..4) per cell — 100 cells total
- **ZeroGPU H200** for training (per-dataset `@spaces.GPU(duration=300)`)
- **MiniBatchKMeans** at `k ∈ {16, 64, 256, 1024, min(k_WL, 4096)}`
  on penultimate embeddings → partition `Πᵗʳᵃⁱⁿᵉᵈ_k`

For each cell we report
- `R̂` — training error of the trained 2-class head
- `ε*(Πᵗʳᵃⁱⁿᵉᵈ_k)` — empirical bracket on the k-means partition
- `feat_gap := ε_WL - ε*(Πᵗʳᵃⁱⁿᵉᵈ_k_WL)` — positive = features
  refine WL at matched cell budget
- `head_sig := ε*(Πᵗʳᵃⁱⁿᵉᵈ_k_WL) - R̂` — negative = trained head
  exploits sub-cell geometry

## How to deploy

```bash
# from the repo root
huggingface-cli login   # paste HF write token
hf repo create elouafiqAli/d-full-gnn-bracket --repo-type=space \
    --space_sdk=gradio
hf upload elouafiqAli/d-full-gnn-bracket hf_space . --repo-type=space
# In the Space settings, set Hardware = "ZeroGPU" (requires HF Pro).
```

## Local dry-run

```bash
cd hf_space && pip install -r requirements.txt && python app.py
# falls back to MPS/CPU when ZeroGPU isn't available
```

## Reproducing the paper table

After "Run ALL datasets sequentially" finishes, download
`results/e3d_arch_full.json`. The aggregate table in the paper is
mean ± std over seeds 0..4 per (dataset, arch) at the largest k in
the sweep (closest to `k_WL`).
