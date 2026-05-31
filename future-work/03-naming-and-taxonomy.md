# 03 — Naming and Taxonomy

## Why "MPC" is the wrong umbrella

Kemper et al.'s **MPC** = *Message-Passing Complexity*: named after the
**mechanism** (synchronous neighbour aggregation) that induces the
partition, not after the partition itself. PA-MPC inherits that — the
"MP" is load-bearing because Definition 3.5 is literally
*"synchronous, permutation-invariant, identifier-free **local
neighbourhood** update."*

The moment you drop edges, sample subgraphs, count graphlets, or use a
kernel feature map, the inducing mechanism is no longer message
passing, and calling the resulting quantity "MPC" is a category error
— even though Theorem 1 still holds verbatim.

## The umbrella term

The thing that is invariant across all these paradigms is the
**partition** and the **conditional entropy of the task given that
partition**. The honest hierarchy:

```
Partition-Conditional Complexity (PCC)   ← the abstract quantity: H(f | Π)
├── PA-MPC          : Π induced by depth-L message passing  (paper-01)
├── PA-GC  (graphlet)  : Π induced by graphlet-orbit signatures
├── PA-KC  (kernel)    : Π induced by pre-image of a kernel feature map
├── PA-SC  (subgraph)  : Π induced by bag-of-subgraphs equivalence
├── PA-PEC (positional): Π induced by quantized positional encodings
├── PA-SPC (stochastic): Π induced by an edge/node-dropping policy
├── PA-DC  (diffusion) : Π induced by quantized RW/diffusion embedding
└── PA-kWLC           : Π induced by k-WL on V^k (= Conjecture C1')
```

## Locked naming convention (adopt now)

| Symbol | Name | Scope |
|---|---|---|
| **PCB** | Partition-Conditional **B**ayes-error bracket | the theorem (paradigm-free) |
| **PCC**$(f, \Pi) := H(f \mid \Pi)$ | Partition-Conditional Complexity | the scalar quantity |
| **PA-XC**$(f, G; \mathcal{A}, L)$ | family-indexed instantiation | one per paradigm |

Suffix table:

| Suffix | Paradigm | Inducing mechanism |
|---|---|---|
| **MPC** | Message-passing | LossyWL$^L(\Pi^{(0)}_{\mathcal{A}}; G)$ — paper-01 |
| **GC** | Graphlet | orbit-signature quotient up to size $k$ |
| **KC** | Kernel | pre-image of $\phi_{\mathcal{K}} : V \to \mathcal{H}$ |
| **SC** | Subgraph (ESAN/GNN-AK/SUN) | bag-of-subgraphs equivalence under policy $\pi$ |
| **PEC** | Positional encoding | quantized LapPE / RWPE / SignNet feature |
| **SPC** | Stochastic policy | DropEdge / GDC / RandomSubgraph — distributional Π |
| **kWLC** | $k$-WL | $k$-WL refinement on $V^k$ — Conjecture C1′ |
| **DC** | Diffusion/RW embedding | vector-quantized DeepWalk / node2vec |

## Rationale

- **"PCB" not "PAC"** — Valiant's PAC is already taken; collision is
  fatal in a learning-theory venue.
- **"PCC" as the scalar** — separates the *quantity* from the
  *bracket theorem* (PCB). Paper-01 conflates these under "PA-MPC";
  paper-02 needs them disambiguated to talk about cross-paradigm
  comparison.
- **"PA-XC" with suffix** — keeps the "Partition-Aware" lineage from
  paper-01 visible while making the inducing mechanism explicit in the
  name.

## Migration footnote (cheap, do this for paper-01 arXiv-v2)

Add a one-paragraph "Notation update" footnote between submission and
arXiv-v2 introducing PCB / PCC / PA-XC and explicitly demoting "MPC" to
the message-passing case. Costs nothing and earns the namespace before
paper-02 commits to it.
