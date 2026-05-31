# 05 — Sequel Paper Plan

## Working title

**"Partition-Conditional Complexity: A Paradigm-Agnostic Bayes-Error
Sandwich for Learning on Graphs"**

Subtitle option: *"Beyond Message Passing — Graphlet, Kernel,
Stochastic-Policy, and Positional-Encoding Instantiations"*

## The reframing move

Paper-01 (PA-MPC) is positioned as *one instantiation*. Paper-02's
contribution is the **inversion of the dependency**: Theorem 1 was
never about message passing; it was about a finite partition and a
binary task. The sequel makes that abstraction first-class and shows it
is not vacuous — it discriminates between paradigms on the *same*
anchor.

- Paper-01 asks: *"can family $\mathcal{A}$ at depth $L$ resolve task
  $f$?"*
- Paper-02 asks: *"**which observation paradigm resolves $f$ most
  efficiently per unit of inductive bias spent?**"*

The second question is the one practitioners actually have, and no
existing framework answers it cross-paradigm. WL-style expressivity
hierarchies compare *within* the partition-refinement lineage;
kernel-vs-GNN comparisons are empirical-only; subgraph-GNN bounds are
paradigm-internal. The PCB sandwich gives a **common currency**.

## Sectioning skeleton

```
1. Introduction — "Theorem 1 was the seed; the tree is paradigm-agnostic."
2. PCB Restated — Theorem 1 cited, not re-proved; PCC notation; the
                  one-line admissibility schema (Def 2.1).
3. The Admissibility Schema (the real theoretical contribution)
   3.1 Generalised admissibility predicate (Def 3.5 → Def 2.1 abstracted)
   3.2 Architecture-factorisation lemma in schema form
   3.3 Stochastic extension (quenched vs annealed brackets)
   3.4 Out-of-scope predicate: identifier-leaking families
4. Instantiation I — PA-GC (graphlets)            ← Pržulj GDV, GSN
5. Instantiation II — PA-KC (graph kernels)       ← WL-subtree, SP, graphlet kernels
6. Instantiation III — PA-SPC (stochastic policies) ← DropEdge, GDC, expander rewiring
7. Instantiation IV — PA-PEC (positional)         ← LapPE, RWPE, SignNet (quantized)
8. Cross-Paradigm Comparison Experiment (E11–E14)
   — same anchor_8, same f, four brackets side-by-side
9. Conjecture C1′ resolution attempt (paper-02's headline open problem)
10. Limitations, scope, registered conjectures.
```

## Four theoretical contributions (the load-bearing ones)

These are what stop the sequel from being a corollary-farm.

### T1 — Abstract admissibility schema

Definition 3.5 of paper-01 has four clauses that conflate two distinct
things: (i) **closure under the partition operator** (clauses 1, 2, 3)
and (ii) **identifier non-leakage** (clause 4). Separating them gives
a clean predicate other paradigms can satisfy:

> *A paradigm $\mathcal{P}$ is **PCB-admissible at scale $L$** if it
> specifies (a) a finite index set $X$, (b) an initial partition
> $\Pi^{(0)}_{\mathcal{P}}$ of $X$, (c) a refinement operator
> $R_{\mathcal{P}}$ on $\Pi(X)$, and (d) a predictor class
> $\mathcal{H}_{\mathcal{P}, L}$ each member of which is constant on
> cells of $R_{\mathcal{P}}^L(\Pi^{(0)}_{\mathcal{P}})$.*

This is the **one definition** Proposition 3.3 generalises to. It is
short, falsifiable, and trivially auditable for any candidate paradigm.
The contribution is that *the same* sandwich theorem applies to every
$\mathcal{P}$ satisfying it.

### T2 — Quenched/annealed gap lemma

For stochastic-policy paradigms (PA-SPC), the annealed bracket is
uniformly tighter than the quenched bracket, and the gap is exactly
$\mathbb{E}_\omega I(f; \Pi^{(\omega)}) - I(f; \overline{\Pi})$ where
$\overline{\Pi}$ is the meet. Full statement and novelty-risk note in
[`04-stochastic-policies-edge-drop.md`](04-stochastic-policies-edge-drop.md).

### T3 — Cross-paradigm comparison theorem

For two PCB-admissible paradigms $\mathcal{P}_1, \mathcal{P}_2$
inducing partitions $\Pi_1, \Pi_2$ on the same $V$, the brackets are
comparable via the meet/join in the partition lattice: if
$\Pi_1 \preceq \Pi_2$ (1 refines 2), then $\mathrm{PCC}_1 \le
\mathrm{PCC}_2$ and the sandwich for $\mathcal{P}_1$ dominates. The
non-trivial case is **incomparable** partitions — there the *meet*
$\Pi_1 \wedge \Pi_2$ gives a strictly tighter common bracket that
neither paradigm achieves alone. This is the formal statement of
"ensembling paradigms can only help," and it has not (to our
knowledge) been proved in the GNN literature at this level of
generality.

### T4 — Identifier-leakage as the dichotomy invariant

Empirically, paper-01's E08 Stage K/L/M dichotomy is
$\{\text{GCN, GIN, GatedGCN}\}$ vs $\{\text{GAT, GraphSAGE}\}$. The
clean explanation under the schema: GAT's learned attention weights
and GraphSAGE's sampled neighbourhoods are *softly identifier-leaking*
under finite training. Paper-02 can formalise this and predict —
**before running the experiment** — that PA-PEC with unquantized PEs
and PA-SPC with realisation-dependent policies will exhibit analogous
$L=2$ fragility on the same anchor. A pre-registered prediction is
what turns "another instantiation" into science.

## Headline experiment — E11 (cross-paradigm comparison)

Same `anchor_8` as paper-01. Same canonical task suite. Five paradigms
(PA-MPC, PA-GC, PA-KC, PA-SPC, PA-PEC) computed *on the same rows*.
The PCB bracket for each → a single 8×5 heatmap showing where each
paradigm sits in the achievable region $\tilde{A}_2$. This is the
figure the paper is built around.

Tier breakdown:

- **L-I exact-rational** for PA-MPC, PA-GC, PA-KC (deterministic
  partitions, finite $V$, exact $\mathbb{Q}$ ledger possible);
- **L-I conditional on quantization** for PA-PEC;
- **L-I in expectation** for PA-SPC (Monte-Carlo over policy with
  exact-$\mathbb{Q}$ per draw).

**No GPU required for the core figure.** The C1′ experiment (E10/E12,
$k$-WL) is the only float-tier piece and can be staged like E08 was in
paper-01.

## Recycle vs rewrite

**Recycle wholesale from paper-01:**

- Theorem 1, Propositions 3.2 / 3.5 / 3.6 (cite, do not restate proofs)
- The achievable-region diagram $\tilde{A}_2$ and the width-bound
  $w^* \approx 0.161$
- The reproducibility infrastructure (Merkle root, claim registry,
  gates)
- The honest-narrowings template from §10

**Rewrite from scratch:**

- §2 (Related Work) — pivot from "MPNN expressivity" to
  "partition-indexed learning paradigms"; the Geerts–Reutter /
  Böker et al. / Morris et al. 2023 / Bouritsas et al. / ESAN / SignNet
  / DropEdge clusters are now *peers*, not background.
- The admissibility predicate (Def 3.5 → schema form, T1)
- Proposition 3.3 in schema form (it generalises, but the proof needs
  re-organisation)
- The §9 protocol template — paper-02 needs **five** parallel
  C1-style conjectures, one per paradigm, with a shared decision rule.

## Risks and pre-registered failure modes

Three things could kill the sequel; better to flag them now.

1. **PA-GC and PA-MPC partitions could turn out to be identical on
   anchor_8.** If graphlet signatures up to size $k$ generate exactly
   the WL-stable partition on the eight test graphs, the
   cross-paradigm comparison figure is empty. **Mitigation:**
   pre-compute on anchor_8 *before committing*; if degenerate, extend
   the anchor with graphs known to separate WL from graphlet
   (Cai–Fürer–Immerman pairs are wrong here — they collapse both —
   but expander / random-regular pairs separate them).
2. **The annealed/quenched gap lemma might already exist in the
   dropout-regularisation literature.** Required focused literature
   pass before claiming T2 as novel. The form sketched in
   [`04-stochastic-policies-edge-drop.md`](04-stochastic-policies-edge-drop.md)
   looks close to the Jensen-gap arguments in Gal & Ghahramani (2016)
   and recent DropEdge analyses; if it's there, demote T2 to a
   re-statement-with-application and elevate T1 / T3.
3. **C1′ might fail in the same way C1 nearly did** (vertex-transitive
   substrate vacuity). The substrate correction in §9.E of paper-01 is
   the template; bake the lesson into E10's design before scheduling
   GPU.

## This week — concrete actions to make the sequel real

1. **Lock the taxonomy.** Add a one-paragraph "Notation update"
   footnote to paper-01 (between submission and arXiv-v2) introducing
   PCB / PCC / PA-XC and explicitly demoting "MPC" to the
   message-passing case. Costs nothing and earns the namespace.
2. **File the paper-02 README** at `notes/paper-02-pcb/00-plan.md`
   mirroring `notes/paper-arxiv-review/00-plan.md`. Pin T1–T4 and E11
   as the four load-bearing contributions.
3. **Pre-flight check on anchor_8.** Compute PA-GC ($k \in \{3,4,5\}$)
   and PA-KC (WL-subtree, shortest-path) partitions on anchor_8 by
   hand / sympy in a notebook. If they don't separate from PA-MPC,
   extend the anchor *now*, before the paper-02 commitments are
   pinned.
4. **Decide the registry policy.** Either paper-02 inherits the
   `PAMPC-*` claim namespace (cheap, mildly misleading) or it mints
   `PCC-*` claims (clean, more bookkeeping). **Recommendation:**
   `PCC-*` — the rename only buys you something if it shows up in the
   artefact store.

## One-line pitch

The sequel is not *"PA-MPC for graphlets"*; it is **"the partition was
always the protagonist; here is what the cast looks like when you give
them all the same script."** That framing is what makes it a paper-02
and not a long appendix.
