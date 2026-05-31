# 01 — Theorem Scope Analysis

**Question.** Is Theorem 1 of paper-01 (PA-MPC) actually about message
passing, or about something more general?

**Answer.** It is paradigm-agnostic. LossyWL only enters one definition
(3.1) and one corollary (3.4); the sandwich itself never touches a
graph, an architecture, or WL.

## Where the LossyWL coupling lives

Reading [`../PAPER-ARXIV.md`](../PAPER-ARXIV.md) §3.2 against §3.3:

- **Theorem 1** is stated for "any finite partition $\Pi$ of a finite
  vertex set $V$ and any binary task $f : V \to \{0,1\}$". The paper
  says verbatim: *"The theorem makes no reference to $G$, $\mathcal{A}$,
  the LossyWL operator, or $\mathcal{F}_{\mathrm{WL}}$"*.
- **Proposition 3.2** (refinement monotonicity) — pure partition
  lattice; no graph structure.
- **Proposition 3.5** (sharpness) — finite combinatorics on $[0, 1]$.
- **Proposition 3.6** (prior-aware sharpening) — data-processing on the
  binary error indicator.
- **Proposition 3.3 + Corollary 3.4** — *this* is the only
  LossyWL-coupled step, and even there the coupling is mediated entirely
  by Definition 3.5's four admissibility clauses (initial-observable
  confinement, shared local update, permutation invariance, no
  identifier leakage). LossyWL is just the operator that pushes the
  initial partition forward.

## Minimal substitution to port the sandwich

To apply Theorem 1 to another paradigm, swap in:

1. A well-defined **family-level initial partition**
   $\Pi^{(0)}_{\mathcal{A}}$ of whatever index set the paradigm reads
   (vertices, $k$-tuples, edges, subgraphs, graphs).
2. A **refinement operator** $\mathcal{R}_{\mathcal{A}}$ that plays
   LossyWL's structural role.
3. An analogue of Proposition 3.3: *"every depth-$L$ predictor of
   family $\mathcal{A}$ is constant on cells of
   $\mathcal{R}_{\mathcal{A}}^L(\Pi^{(0)}_{\mathcal{A}})$."*

Theorem 1 then applies verbatim. The 8-graph anchor and the Lean witness
are the only LossyWL-tied infrastructure in paper-01.

## What does *not* port automatically

Two genuine obstructions, both already named in paper-01:

1. **Identifier-leaking architectures** (random node IDs à la RNI,
   position-aware GNNs like P-GNN, anything that reads raw vertex
   names) violate Definition 3.5(4). Theorem 1 still holds for any
   partition they happen to induce, but Proposition 3.3 fails, so
   Corollary 3.4(1) (the operational lower-bound reading) does not.
2. **Continuous-state architectures before quantization.** This is the
   obstruction Conjecture C1 in §9 tries to close for the LossyWL case.
   The same obstruction reappears for PE-based and diffusion-based
   paradigms — each gets its own C1-style transfer conjecture.

## Honest summary

The framework is doing two separable things:

- a **partition → Bayes-error sandwich** (Theorem 1 + Propositions 3.2,
  3.5, 3.6) that is pure finite combinatorics and applies to *any*
  learning paradigm that reads a graph through a finite partition of
  its index set;
- an **architecture-factorisation lemma** (Proposition 3.3) that is the
  only LossyWL/MPNN-specific bridge, and which has a clean analogue for
  each paradigm provided you fix a family-level initial observable and
  forbid identifier leakage.

Paper-01 chose to narrow itself to LossyWL in order to keep the Lean
witness, the L-I ledger, and the C1 protocol all within one operator
family — not because the theorem requires it.
