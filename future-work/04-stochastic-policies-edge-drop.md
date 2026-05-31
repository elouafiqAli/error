# 04 — Stochastic Policies and Edge-Drop Constructs (PA-SPC)

Edge-dropping (DropEdge, GDC sparsification, RandomSubgraph,
ESAN-style stochastic policies, expander-graph rewiring) is the most
interesting non-message-passing paradigm because the partition is
**distributional**, not deterministic: each draw $\omega$ from the
policy gives a (possibly different) partition $\Pi^{(\omega)}$.

Two clean ways to apply the PCB sandwich, corresponding to two
different operational readings.

## Option A — Quenched / per-realisation

Apply Theorem 1 inside the expectation:

$$
\mathbb{E}_\omega\!\left[H_{\mathrm{bin}}^{-1}(H(f\mid\Pi^{(\omega)}))\right]
\;\le\; \mathbb{E}_\omega[\varepsilon^{*}_{\Pi^{(\omega)}}]
\;\le\; \tfrac{1}{2}\,\mathbb{E}_\omega[H(f\mid\Pi^{(\omega)})].
$$

This is the right bracket for a model that **commits to one draw at
inference time**. The natural name is **PA-SPC** — *Partition-Aware
Stochastic-Policy Complexity* — with admissibility clause (5) added to
Definition 3.5:

> *(5) The policy $\omega \mapsto \Pi^{(\omega)}$ is
> permutation-equivariant and independent of vertex identifiers.*

## Option B — Annealed / ensemble-averaged

First average the partition (i.e. take the **meet** of
$\{\Pi^{(\omega)}\}_\omega$ in the partition lattice, or equivalently
the partition induced by the random feature
$v \mapsto (\Pi^{(\omega)}(v))_\omega$), then apply Theorem 1 once.
This is the right bracket for an **ensemble predictor** (test-time
averaging à la DropEdge inference).

Proposition 3.2 (refinement monotonicity) gives for free that the
annealed bracket is *tighter* than the quenched one — averaging
refines.

## T2 — Quenched/Annealed Gap Lemma (candidate new result)

For PA-SPC paradigms, the annealed bracket is uniformly tighter than
the quenched bracket, and the gap is exactly:

$$
\mathbb{E}_\omega\,I(f; \Pi^{(\omega)}) \;-\; I(f; \overline{\Pi})
\;\geq\; 0,
$$

where $\overline{\Pi}$ is the meet of $\{\Pi^{(\omega)}\}_\omega$ in
the partition lattice (equivalently, the partition induced by the
tuple-valued random feature).

**Why it matters.** This is the formal statement of "ensemble inference
is bracket-tighter than single-draw inference for any stochastic-policy
GNN", and it gives a clean information-theoretic guide to DropEdge /
GDC inference policy.

**Novelty risk.** The form looks suspiciously close to Jensen-gap
arguments in Gal & Ghahramani (2016) and more recent DropEdge analyses.
**Required pre-flight literature pass** before claiming T2 as novel
(see [`05-sequel-paper-plan.md`](05-sequel-paper-plan.md) Risks §2). If
it is already there, demote T2 to a re-statement-with-application and
elevate T1 / T3.

## E11 sub-experiment for PA-SPC

On anchor_8 with the canonical task suite, DropEdge with $p \in \{0.1,
0.2, 0.5\}$:

- Monte-Carlo over $N = 1000$ policy draws per $(G, f, p)$ cell.
- Exact-$\mathbb{Q}$ computation of $H(f \mid \Pi^{(\omega)})$ per draw
  (the per-draw partition is deterministic given the realisation).
- Report both quenched and annealed brackets per cell.
- Falsifier F-SPC: annealed bracket width $\leq$ quenched bracket width
  on every cell (T2 prediction).

Cost: zero GPU; everything is exact-rational over partition-lattice
arithmetic.

## Bonus paradigm: structural perturbations are also PA-SPC

Edge-rewiring (graph augmentation), random node-feature masking, and
expander-graph rewiring are all instances of the same schema. Paper-01
§E09 already prices three of them (virtual-node, edge-rewire,
edge-contract) under a deterministic intervention; PA-SPC is the
distributional generalisation. E09's L-I ledger can be reused as the
seed for the deterministic baseline.
