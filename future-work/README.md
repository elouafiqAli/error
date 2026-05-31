# Future Work — PCB / PA-XC Sequel Programme

This folder captures the conceptual opportunities surfaced by re-reading
paper-01 (PA-MPC) and asking *"is Theorem 1 actually about message
passing?"* The short answer: no — it is paradigm-agnostic. These notes
plan the sequel.

## Index

| File | Content |
|---|---|
| [`01-theorem-scope-analysis.md`](01-theorem-scope-analysis.md) | Where the LossyWL coupling actually lives in paper-01, and why Theorem 1 / Propositions 3.2 / 3.5 / 3.6 are paradigm-free. |
| [`02-extension-paradigms.md`](02-extension-paradigms.md) | Ranked table of candidate paradigms (graphlets, kernels, subgraph GNNs, $k$-WL, PE, RW embeddings) with admissibility analysis. |
| [`03-naming-and-taxonomy.md`](03-naming-and-taxonomy.md) | Why "MPC" is the wrong umbrella; the PCB / PCC / PA-XC convention; suffix table. |
| [`04-stochastic-policies-edge-drop.md`](04-stochastic-policies-edge-drop.md) | Quenched vs annealed brackets for DropEdge / GDC / RandomSubgraph; the gap lemma (T2). |
| [`05-sequel-paper-plan.md`](05-sequel-paper-plan.md) | Working title, sectioning, four theoretical contributions (T1–T4), headline experiment E11, recycle/rewrite plan, risks, this-week action list. |

## Status

All notes are **exploratory** as of 2026-05-31. No `PAMPC-*` or `PCC-*`
claim IDs have been minted from this work; nothing here is part of
paper-01's reproducibility contract. The earliest binding artefact will
be the anchor_8 pre-flight check from [`05-sequel-paper-plan.md`](05-sequel-paper-plan.md)
§"This week".

## Provenance

Generated from a conversation on 2026-05-31 reviewing
[`../PAPER-ARXIV.md`](../PAPER-ARXIV.md). The conversation walked the
proof spine (§3.2, Appendix A), identified the single LossyWL-coupled
step (Proposition 3.3), and worked out the schema that generalises it.
