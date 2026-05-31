# 02 — Extension Paradigms

Concrete candidates for applying the PCB sandwich beyond message
passing, ranked by how cleanly they slot into the schema from
[`01-theorem-scope-analysis.md`](01-theorem-scope-analysis.md).

## Ranked table

| Paradigm | Partition operator | Fits Theorem 1? | Fits Corollary 3.4? | Notes |
|---|---|---|---|---|
| **Graphlet-degree vectors** (Pržulj GDV / GSN, Bouritsas et al.) | quotient by graphlet-orbit count signature | ✓ verbatim | ✓ — admissibility (1)–(4) all clean if the count map is the initial observable | Refinement step is "intersect with 1-WL one round"; sandwich immediate. **Strongest drop-in candidate.** |
| **Graph kernels** (WL subtree, graphlet, shortest-path) | pre-image of the kernel feature map on $V$ | ✓ | ✓ for WL-subtree (= the LossyWL chain already); — for graphlet/SP only the lower side is operational without an admissible family | The two-sided sandwich becomes a kernel-feature-conditional Bayes-error bracket — a genuinely new reading of these kernels. |
| **Spectral / positional encodings** (LapPE, RWPE, SignNet) | quantize the PE vector → finite partition | ✓ | ✓ once PEs are quantized (admissibility clause 4 forces a finite alphabet); fails for raw real-valued PEs | Same C1-style quantization argument as paper-01 §9 applies; this is the natural sibling to C1 for PE families. |
| **Subgraph GNNs** (ESAN, GNN-AK, SUN, DSS-GNN) | partition by bag-of-subgraphs equivalence | ✓ | ✓ after generalising Definition 3.5(4) from "no vertex identifiers" to "no identifier beyond the policy-equivariant subgraph index" — a one-line edit | Strictly finer than 1-WL on some pairs; the upper bound gets non-trivially tighter, the framework is unchanged. |
| **$k$-WL / $k$-GNN / PPGN / 2-IGN** | $k$-WL refinement on $V^k$ | ✓ (take $V \leftarrow V(G)^k$ in Theorem 1) | ✗ as stated — paper explicitly excludes via Definition 3.5(4); but this is **Conjecture C1′** in §9.X, registered as the headline open problem for paper-02 | Theorem 1 is already correct over $V^k$; only Corollary 3.4 needs re-derivation with a $k$-tuple admissibility predicate. |
| **Random-walk / diffusion embeddings** (DeepWalk, node2vec, GDC) | vector-quantize the embedding | ✓ | ✓ post-quantization | Same shape as the PE extension. |
| **Equitable-partition / orbit-based methods** | the operator's fixpoint *is* the equitable partition | ✓ | ✓ — this is the $L \to \infty$ limit already in Corollary 3.4(4) | Not a new paradigm, just the limit case the paper already names (Schwenk 1974). |
| **Edge / link / graph-level tasks** | reinterpret $V$ as $E(G)$ or as the dataset of graphs | ✓ | ✓ with the obvious admissibility analogue | Theorem 1 only ever assumes a finite set and a binary label on it. |
| **Stochastic-policy paradigms** (DropEdge, GDC, RandomSubgraph) | per-realisation random partition | ✓ in expectation | ✓ with quenched/annealed admissibility predicate | See dedicated note [`04-stochastic-policies-edge-drop.md`](04-stochastic-policies-edge-drop.md). |

## Priority for paper-02

The cross-paradigm comparison figure (E11 in
[`05-sequel-paper-plan.md`](05-sequel-paper-plan.md)) needs **at least
three independently-induced partitions** on the same anchor_8 to be
non-trivial. The recommended slate:

1. **PA-MPC** — already done (paper-01 carries this).
2. **PA-GC** (graphlets, $k \in \{3,4,5\}$) — deterministic, L-I-able,
   strongest expected separation from PA-MPC on irregulars.
3. **PA-KC** (WL-subtree + shortest-path kernels) — deterministic,
   L-I-able, sanity check that WL-subtree collapses to PA-MPC.
4. **PA-SPC** (DropEdge with policy $p \in \{0.1, 0.2, 0.5\}$) —
   distributional, L-I in expectation, demonstrates T2.
5. **PA-PEC** (quantized LapPE, $k = 4$ eigenvectors, 8-bit) —
   deterministic post-quantization, demonstrates the C1-analogue.

PA-kWLC (= C1′) is reserved as paper-02's headline open problem
(E10/E12), parallel to how paper-01 carries C1.
