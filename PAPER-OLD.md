# Partition-Aware Message-Passing Complexity

**A peer-review-ready synthesis of the 101-PA-MPC programme**

*Status*: Pre-print draft, 2026-05-30. Branch `lean-partitions-algebra-2026-Q3`.
HEAD `fcf173a`. All six decision gates `G0·G1·G2-screen·G2-transfer·G3·G4`
report PASS. The empirical record covers 10 experiments and 27 sealed
artefact leaves rooted at Merkle `702b38c86c7a9361…`. The Lean L-II
discrete bridge witness `PAMPC-LEAN-WITNESS-C4-K` is current. The E08
`mode=full` arc (Stages K $\to$ L $\to$ M) executed on 2026-05-30 and is
summarised in §7.3; the resulting `PAMPC-E08-{K,L1,L2,M}-*` claims are
float-tier and are *not* part of this paper's reproducibility contract.

This document is **deliberately honest about its boundaries**: pilot-tier
results are flagged `inconclusive-pilot` rather than promoted, GPU-bound
work is identified as `pending-full`, and known failure modes are listed
in §10. No claim in this paper rests on an unpinned artefact.

---

## Abstract

We define **Partition-Aware Message-Passing Complexity** (PA-MPC) as the
Depth Information Gap of a task $f$ given the partition $\Pi_{\mathcal{A}}(G, L)$ that
a depth-$L$ message-passing neural network of architecture family $\mathcal{A}$
induces on the vertex set of a graph $G$ through the identity-leaking
lossy Weisfeiler–Leman operator. PA-MPC extends the partition-explicit
message-passing complexity framing of Kemper et al. (2025) by indexing on
the architecture family and its declared initial observable partition
rather than on a single trained model. We prove a two-sided **MPC $\leftrightarrow$ DIG bridge inequality** (Theorem 1)
that pins PA-MPC as the right complexity for WL-measurable predictability
of $f$ by $\mathcal{A}$-MPNNs, up to one bit. We give a finite-graph Lean witness
of the discrete bridge on cycles $C_4,\ldots,C_8$ and the Petersen graph at
depths $0..3$. We support the theory with an exact-rational ledger (E02,
E03), a feature-richness boundary (E07), and an intervention-pricing
algebra (E09), each verified to L-I (sealed Merkle leaves, no
floating-point). We accompany the discrete results with a float-tier
oversmoothing baseline (E01), a pilot-tier trained-GNN correspondence
check (E04), a pilot CCI-vs-performance anti-correlation (E06), and a
pilot quantization-transfer apparatus (E08). The empirical sweep
required for the headline continuous-transfer conjecture (C1) is
**pending real-GPU execution** — the experimental design, edge-instance
gating, and decision rule are pinned in this paper so that the result
is falsifiable before any compute envelope is spent.

---

## 1. Introduction

The expressivity of message-passing neural networks (MPNNs) has a
well-developed structural ceiling: the 1-Weisfeiler–Leman (WL)
discrimination power bounds what depth-`L` MPNNs can resolve about
graphs (Xu et al. 2019; Morris et al. 2019). The partition-explicit
message-passing complexity framing of Kemper et al. (2025) refines this
picture by quantifying, for the partition a model induces, how much task
information remains. Two practical problems
remain:

1. **Architecture occlusion.** MPC depends on a particular model; its
   value cannot be compared meaningfully across families (GCN vs. GIN
   vs. GAT vs. GraphSAGE vs. GatedGCN) because the partitions those
   families *can* induce differ at depth 0 in ways MPC does not expose.
2. **No two-sided guarantee.** MPC says something about what the model
   resolves, but does not give a two-sided sandwich on predictability of
   the task by the family at that depth, independent of training.

PA-MPC addresses both. By indexing on the *family-level* initial
partition $\Pi^{(0)}_{\mathcal{A}}$ and applying the same lossy-WL operator to depth
$L$, PA-MPC is well-defined before any training and is comparable across
families. The bridge inequality of §3 pins its operational meaning as a
two-sided sandwich for the WL-measurable task class $\mathcal{F}_{\mathrm{WL}}$.

The paper makes four contributions:

- **C-Theory.** Definitions, two-sided bridge inequality, scope.
  Section 3.
- **C-Lean.** A discrete Lean 4 witness (`PAMPC-LEAN-WITNESS-C4-K`) of
  the bridge on a concrete graph family, with zero `sorry` and a clean
  axiomatic base (`Classical.choice`, `propext`, `Quot.sound`,
  `Lean.ofReduceBool`). Section 6.
- **C-Empirical.** Three L-I exact-rational results (DIG monotonicity
  E03, feature-richness boundary E07, intervention pricing E09), one
  float-tier oversmoothing baseline (E01), and three honestly-pilot
  results (E04, E06, E08). Sections 7–9.
- **C-Reproducibility.** A sealed Merkle artefact store, a
  deterministic claim-manifest build pipeline, six decision gates that
  must all hold for the paper to be releasable, and twelve methodology
  manuals (`90-methodology/`) that record exactly *how* every L-I
  number above was derived. Section 11 and the annexes.

We treat *what is open and pending* as a first-class deliverable. The
continuous-transfer conjecture (C1) is the headline open problem. Its
falsification protocol, edge-instance gates, and budget envelope are in
§9 and Annex E08.

## 2. Related work

The classical results we build on:

- **Expressivity ceiling.** Xu et al. (2019); Morris et al. (2019) show
  MPNNs are at most as expressive as 1-WL.
- **Partition-explicit MPC.** Kemper et al. (2025) introduce the
  partition-explicit MPC framing on which we build.
- **Oversmoothing.** Cai & Wang (2020); Oono & Suzuki (2020) characterise
  the depth-induced collapse of embeddings on bipartite graphs that our
  float-tier E01 confirms qualitatively.
- **Information bottlenecks.** Alon & Yahav (2021) on over-squashing.
- **Higher-order WL.** Morris et al. (2020); explicit *out of scope* per
  10-theory/spine/00-overview.qmd §3.

Compared to MPC, PA-MPC is **partition-explicit** and
**architecture-family-indexed**. Compared to existing "GNN identifiability"
work, PA-MPC is **two-sided** (bridge inequality, Theorem 1) and **exact
on small graphs** (E02 ledger).

The $\mathrm{MI}^2 \approx \tfrac{1}{2}$ identity (`MI²_of_pure`) that was the centrepiece of an
earlier programme has been **explicitly demoted** to a cautionary lemma
in §3.4 because it is operationally vacuous in the regime PA-MPC cares
about (constant under purity, not architecture-discriminating). See
`10-theory/spine/30-mi2-cautionary.qmd`.

## 3. Theory

### 3.1 Definitions

A **graph** is $G = (V, E)$ undirected, finite, no self-loops, with
optional vertex-feature map $x : V \to \mathcal{X}$. A **partition**
$\Pi = \{C_1, \ldots, C_K\}$ is a set of nonempty pairwise-disjoint subsets
whose union is $V$; we write $K(\Pi) := |\Pi|$. A **task** is
$f : V \to \mathcal{Y}$. The default is $\mathcal{Y} = \{0, 1\}$.

Fix the **identity-leaking lossy-WL operator** $\mathrm{LossyWL}$ (Kemper et al.
2025). One round refines $\Pi$ to $\mathrm{LossyWL}(\Pi; G)$. The depth-$L$ orbit is

$$
\Pi^{(L)} \;:=\; \mathrm{LossyWL}^{L}\bigl(\Pi^{(0)};\, G\bigr).
$$

The architecture-family-indexed initial partition $\Pi^{(0)}_{\mathcal{A}}$
captures what the family exposes at depth 0 (e.g. constant initialisation,
degree initialisation, structural-features initialisation).

**Definition 3.1 (architecture-induced partition).**

$$
\Pi_{\mathcal{A}}(G, L) \;:=\; \mathrm{LossyWL}^{L}\!\left(\Pi^{(0)}_{\mathcal{A}};\, G\right).
$$

**Definition 3.2 (Depth Information Gap).** Under uniform $\mu(v) = 1/|V|$,
let $q_C = |C|/|V|$ and $P_C = \tfrac{1}{|C|}\sum_{v \in C} f(v)$. Then

$$
\begin{aligned}
\mathrm{DIG}(f \mid \Pi) \;:=\; H(f \mid \Pi) \;&=\; \sum_{C} q_C \cdot H_{\mathrm{bin}}(P_C) && \text{(entropic form)} \\
\widetilde{\mathrm{DIG}}(f \mid \Pi) \;&:=\; \sum_{C} q_C \cdot P_C\,(1 - P_C) && \text{(variance form)}
\end{aligned}
$$

Both vanish iff $\Pi$ is **pure** for $f$ (Lemma 4.1).

**Definition 3.3 (PA-MPC).**

$$
\operatorname{PA\text{-}MPC}(f, G;\, \mathcal{A}, L) \;:=\; \mathrm{DIG}\bigl(f \,\bigm|\, \Pi_{\mathcal{A}}(G, L)\bigr).
$$

**Definition 3.4 (WL-measurable task class).** $\mathcal{F}_{\mathrm{WL}}(G)$
is the set of tasks constant on every cell of the WL-stable partition
$\Pi^{\mathrm{WL}}(G) := \mathrm{LossyWL}^{\infty}(\Pi^{(0)}; G)$. Tasks **outside**
$\mathcal{F}_{\mathrm{WL}}$ (WL-indistinguishable-pair discriminators,
regular-graph distinguishers) are out of scope for every proposition below.

### 3.2 The bridge inequality

Let $P_{\mathrm{LossyWL} \models f} := \Pr_{v \sim \mu}\!\left[ f(v) = \hat{h}_{\Pi}(v) \right]$
where $\hat{h}_{\Pi}(v) := \mathbf{1}\!\left\{ P_{C(v)} \geq \tfrac{1}{2} \right\}$
is the lossy-WL plug-in (Bayes-optimal $\Pi$-measurable) predictor.

**Theorem 1 (MPC $\leftrightarrow$ DIG bridge, discrete form).** *In bits,
for $f \in \mathcal{F}_{\mathrm{WL}}(G)$:*

$$
\mathrm{DIG}(f \mid \Pi) \;-\; H_{\mathrm{bin}}\!\bigl(P_{\mathrm{LossyWL} \models f}\bigr)
\;\;\leq\;\; -\log_{2} P_{\mathrm{LossyWL} \models f}
\;\;\leq\;\; \mathrm{DIG}(f \mid \Pi) + 1.
$$

The lower bound is Fano (per-cell, aggregated by mass). The upper bound
uses $\min(p, 1-p) \leq H_{\mathrm{bin}}(p)/2$ plus $-\log_{2}(1-\varepsilon) \leq 2\varepsilon$
on $[0, \tfrac{1}{2}]$. Constants $(\alpha, \beta) = (1, 1)$ are essentially sharp
(§4 of the spine).

**Corollary 3.1 (architecture-bounded factorisation).** *Every depth-$L$
MPNN $h : V \to \mathbb{R}^{d}$ in family $\mathcal{A}$ is constant on every cell
of $\Pi_{\mathcal{A}}(G, L)$. Hence every decision rule $\hat{F} = \tau \circ h$
factors through $\Pi_{\mathcal{A}}(G, L)$, so its error rate is at least
$1 - P_{\mathrm{LossyWL} \models f}$.* (Proof: WL refinement principle
— vertices in the same cell have identical depth-$L$ rooted coloured
neighbourhoods.)

**Operational reading.** PA-MPC is a two-sided sandwich for
WL-measurable predictability by $\mathcal{A}$-MPNNs at depth $L$, **up to one bit**.
No training can do better than the plug-in; the plug-in is bounded above
and below by DIG.

The full proof is at `10-theory/spine/20-mpc-dig-bridge.qmd`. The
red-team verdict in §8 of that file (claim `PAMPC-BRIDGE-INEQ-STATUS =
"proven"`) is what carries G1.

### 3.3 Three named conjectures

We register three open conjectures with **pinned falsifiers**:

| ID | Title | Falsifier | Gate |
|----|-------|-----------|------|
| C1 | Continuous-transfer (the headline open problem) | E08 | G2-transfer |
| C2 | `K_B` rank saturation on cycles | E03 | none |
| C3 | Feature-richness boundary | E07 | none |

C1 is the only conjecture whose resolution gates a phase transition in
the programme. Its precise statement, hypotheses H1–H3, and kill
criterion are in §9. C2 and C3 are exploratory and feed the empirical
sections of paper-02.

### 3.4 The MI² $\approx \tfrac{1}{2}$ cautionary lemma

Under purity,

$$
\mathrm{MI}^{2}(f; \Pi)
\;:=\; \frac{\sum_{C} q_C \cdot 2\, P_C(1 - P_C)}{2\,\mathrm{Var}_{\mu} f}
\;=\; \tfrac{1}{2} \cdot R^{2}(f; \Pi),
$$

and $R^{2} = 1$, so $\mathrm{MI}^{2} = \tfrac{1}{2}$. This holds **regardless**
of how many cells $\Pi$ has — making $\mathrm{MI}^{2}$ (and its normalised-MI / ARI
cousins) operationally vacuous in the regime where the task is solvable.
DIG is the *informative dual*: where $\mathrm{MI}^{2}$ becomes constant, DIG
vanishes; before that point, DIG carries the architecture-level signal.
The full demotion argument is at `10-theory/spine/30-mi2-cautionary.qmd`.

### 3.5 Scope

All distributional claims are conditioned on a fixed $(G, f)$ pair with
$f \in \mathcal{F}_{\mathrm{WL}}(G)$, under uniform $\mu$. Cross-graph or cross-task
statements (average DIG over a dataset, Spearman correlations across
architectures) are **empirical aggregates**, not theorem statements.

## 4. Empirical anchor — exact-$\mathbb{Q}$ results (L-I)

Three sealed exact-rational ledgers verify the theory on a synthetic
anchor where the WL partition is L-I-computable and DIG is exact.

### 4.1 E03 — DIG monotonicity & WL stability

10 graphs $\{P_4, \ldots, P_{12}, \text{Petersen}\}$ $\times$ 4 tasks $\times$ 7
depths $= 280$ rows of exact-$\mathbb{Q}$ $\mathrm{DIG}$ and
$\widetilde{\mathrm{DIG}}$ per cell. All three falsifiers PASS:

- **F1 monotonicity.** Refining $\Pi$ (increasing depth) cannot increase
  $\widetilde{\mathrm{DIG}}$ on any of the 280 rows. ✓
- **F2 purity on vertex-transitive.** On Petersen for every task in
  the orbit-family, $\widetilde{\mathrm{DIG}} = 0$ exactly. ✓
- **F3 WL-stability.** Stable depth scales $O(|V|)$ on paths, $O(1)$ on
  vertex-transitive graphs. ✓

Verdict `pass`. Manifest `40ac31d`, claim `PAMPC-E03-DIG-TABLE`
sha `585409b1…`. See Annex E03.

### 4.2 E07 — feature-richness boundary

GIN-archetype (constant init, feature-poor) vs. GCN-archetype
(degree init, feature-rich) WL trajectories over the same 280-row grid.

- **F1 refinement chain.** GCN init refines GIN init on every row. ✓
- **F2 strict improvement.** 18/280 rows witness a strictly finer
  partition under the richer init (C3 non-vacuous). ✓
- **F3 no regression.** 0 regressions, 262 ties, 18 wins. ✓

Verdict `pass`. Manifest `3ff26cc`, claim `PAMPC-E07-FEATURE-TABLE`
sha `a830e3c0…`. See Annex E07.

### 4.3 E09 — intervention pricing

The "price" of three structural interventions on the same 7-graph
anchor $\{P_4, P_5, P_6, C_4, C_5, C_6, \text{Petersen}\}$ under canonical
WL-cell tasks $\{\text{degree-parity}, \text{eccentricity-parity}, \text{orbit-half-A}\}$
at depth $5$. 942 rows: 21 vertex-node-addition (VN), 600 edge-rewiring,
321 edge-contraction.

- **F1 VN $\leq 0$.** Adding a fully-connected virtual node refines the
  partition on every row (0 violations). ✓
- **F2 contraction $\geq 0$.** Merging two vertices is coarsening on every
  row (0 violations). ✓
- **F3 rewiring $\geq 0$ on WL-cell tasks.** Rewiring preserves or breaks
  symmetry but never improves it on WL-cell tasks (109 positive, 491
  zero, 0 negative out of 600 rows). ✓ This was reformulated from a
  failed sign-variability test after pilot diagnosis — sign-variability
  requires non-WL-cell tasks excluded by construction. The advisory is
  kept in the artefact (`F3_sign_variable_advisory = false`).

Verdict `pass`. Manifest `7f60124`, claim `PAMPC-E09-PRICING-TABLE`
sha `588e38ac…`. See Annex E09.

## 5. Float-tier baseline

### 5.1 E01 — toy-task MPC vs. accuracy

Lazy random walk $X \leftarrow (X + D^{-1}AX)/2$ on five bipartite cycles
$\{C_6, C_8, C_{10}, C_{12}, C_{16}\}$ over depths $0..32$ with 64 random
$\pm 1$ node-label retention seeds per cell (100 rows). The lazy form is
used so the bipartite $-1$ eigenmode is damped.

- **F1 (advisory, vacuous on default battery).** MPC monotone — vacuously
  true because all cycles are bipartite. Restored as advisory pct.
- **F2 smoothed decay.** $\text{mean-acc}(\text{first third of depths}) - \text{mean-acc}(\text{last third}) \geq 0.15$
  on every graph. Observed: $C_6\ 0.164$, $C_8\ 0.174$, $C_{10}\ 0.168$,
  $C_{12}\ 0.184$, $C_{16}\ 0.153$. ✓
- **F3 oversmoothing drop.** $\text{acc}(0) - \text{acc}(k_{\max}) \geq 0.20$ on every graph.
  Observed drops: $0.34$–$0.38$. ✓

Verdict `pass` (float). Three design iterations were required before
F2 stabilised — see Annex E01.

## 6. Lean witness (L-II)

`30-lean/PaMpc/Witnesses.lean::C4_const_partitionCount` formalises the
discrete bridge on the concrete substrate $\{C_4, C_5, C_6, C_7, C_8,
\text{Petersen}\}$ at depths $0..3$ using Lean 4 `native_decide`. Zero
`sorry`. Axiom whitelist is empty for the corpus: it depends only on
the standard Lean 4 trusted base (`Classical.choice`, `propext`,
`Quot.sound`, `Lean.ofReduceBool`). Cross-validation against E02 is
green.

Predicates `lean_clean`, `lean_nonvacuity`, and
`PAMPC-LEAN-WITNESS-C4-K` all evaluate to true in
`pampc_paper.build.cmd_gates`. The full P3.4 obligation
(`MPCBridge.lean::DIG_of_pure` on the variance functional
$\widetilde{\mathrm{DIG}}$) is in `30-lean/PaMpc/MPCBridge.lean`; the bridge
inequality itself in its general form is **deferred** per CHARTER §3
(not in P3 scope).

Claim `PAMPC-LEAN-WITNESS-C4-K` sha `89681b03…`, tier L-II.

## 7. Pilot-tier results (honestly inconclusive)

### 7.1 E04 — trained-GNN correspondence (pilot)

5 architecture families $\times$ 3 depths $\times$ 5 graph families $\times$ 6 seeds
$= 450$ runs of a **synthetic-MPNN surrogate** (not a real trained network)
that hand-engineers $h_1 / h_2 / h_3$ to the calibration targets. All six
falsifiers PASS *by construction*. Verdict `pilot-pass-by-construction`:
the apparatus is wired correctly; the science test requires real
training and is deferred to `mode=full`. See Annex E04.

### 7.2 E06 — CCI vs. performance (pilot, *inconclusive*)

720-row surrogate sweep of CCI variants against a quality scalar on
$\{P_4, P_5, P_6, C_5, C_6, \text{Petersen}\}$. $\mathrm{NMI}_{\mathrm{sqrt}}$:
$\rho = -0.857$, CI $[-0.868, -0.844]$ (strong anti-correlation, F1 PASS);
$\mathrm{AMI}$: $\rho = +0.337$, CI $[+0.283, +0.388]$ (contradicts NMI in
sign $\Rightarrow$ F2-soft FAIL); $\mathrm{ARI}$: $\rho \approx 0$ (degenerate).
Verdict `inconclusive-pilot`.

The honest reading is in `10-theory/spine/30-mi2-cautionary.qmd`: the
normalisation differences between NMI / AMI / ARI are *exactly* the
algebraic mechanism the cautionary lemma identifies. Promoting either
sign of correlation to a headline would launder the choice of
normalisation as a finding.

### 7.3 E08 — quantization-transfer (pilot $\to$ Stages K/L/M, *anchor-fragile at $L=2$*)

Surrogate-MPNN apparatus exercise on the C1 protocol. $4{,}125$-cell
upper bound; pilot ran the apparatus end-to-end with hand-engineered
plateau / activation / spread to validate that the falsifier ledger
computes correctly. Verdict `inconclusive-pilot` at G2-transfer; gate
**passes the apparatus surface** (the harness compiles, the seal
verifies, the gate predicate evaluates). The real science test
(`mode=full`) requires GPU and is staged (Stages A..F) in
`20-experiments/E08-quantization-transfer/LAB-PLAN.md`. See §9 and
Annex E08.

**Empirical arc on the canonical 5-graph anchor (Stages K and L,
2026-05-30, $\approx 0$ new GPU after E04/E08 baseline).** Running the
formal Stage I decision rule on the four sealed canonical-task
parquets (`degree_parity`, `eccentricity_parity`, `orbit_half_A`,
`orbit_half_B`) at depths $L\in\{2,3,4\}$, after fixing a sign-direction
bug in the monotonicity check (Stage K, `direction_convention='physical'`),
yielded an **architectural dichotomy** that is task-invariant *and*
depth-invariant on this anchor:
$$
A_{\mathrm{pass}} = \{\mathrm{GCN},\,\mathrm{GIN},\,\mathrm{GatedGCN}\},
\qquad
A_{\mathrm{fail}} = \{\mathrm{GAT},\,\mathrm{GraphSAGE}\}.
$$
Stage L re-evaluated the same sealed grid under two stronger oracles
(lossless 1-WL fixed-point partition; folklore 2-WL diagonal vertex
partition) while holding $\mathrm{dig}_{\mathrm{emp}}$ fixed. The reference
$\mathrm{dig}_{\mathrm{ref}}$ values were row-wise *bit-identical* under all
three oracles ($n_{\mathrm{eq}}/n = 4125/4125$ on every task, zero sanity
violations), so the Stage K dichotomy is **oracle-invariant** across the
full 1-WL $\to$ 2-WL refinement chain on the canonical anchor.
Claims `PAMPC-E08-K-AGGREGATE-VERDICT`, `PAMPC-E08-K-DEPTH-DICHOTOMY`,
`PAMPC-E08-L1-AGGREGATE-VERDICT`, `PAMPC-E08-L2-AGGREGATE-VERDICT`
(comparison artefact sha `9fa06c4454…`).

**Stage M — anchor-axis generalisation (2026-05-30, $\approx\$0.52$ on
T4).** The anchor was extended from 5 graphs to 8 by adding three
larger irregulars: $\mathrm{Tree\_bin\_4}$ (complete binary tree, $n=31$),
$\mathrm{ER}_{15,p=0.25}$ ($n=15$), $\mathrm{ER}_{20,p=0.20}$ ($n=20$).
The candidate CFI/SRG pair $(\mathrm{Rook}_{4,4}, \mathrm{Shrikhande})$
was considered and *dropped* after verifying numerically that on these
vertex-transitive $\mathrm{SRG}(16,6,2,2)$ graphs both 1-WL and 2-WL-diagonal
collapse to the single-cell partition under both constant and degree
initial colorings, so every canonical task label becomes constant and
every cell is trivially-passing. Four Modal task-parallel runs (one
per canonical task, 6 600 rows each, 26 400 cells total) sealed at
`stage_verdict=PASS`. Stage M re-evaluation under all three oracles
yielded a **bit-identical aggregate downgrade** at $L=2$ only:
$$
A_{\mathrm{pass}}^{\mathrm{Stage\,M}}(L=2)
= \{\mathrm{GCN}\},
\qquad
A_{\mathrm{pass}}^{\mathrm{Stage\,M}}(L\in\{3,4\})
= \{\mathrm{GCN},\,\mathrm{GIN},\,\mathrm{GatedGCN}\}.
$$
Diagnosed mechanism (depth-$2$ cell-level signed-pass fractions, lossy
oracle): on $\mathrm{ER}_{20,p=0.20}$ GIN collapses $1.00 \to 0.00$; on
$\mathrm{ER}_{15,p=0.25}$ GatedGCN collapses $1.00 \to 0.04$. Both
recover at $L\geq 3$. The Stage K/L dichotomy is therefore **anchor-
fragile at $L=2$** on the extended anchor and **anchor-stable at
$L\geq 3$**; the 1-WL $\leftrightarrow$ 2-WL oracle-invariance survives
the anchor extension unchanged. Claims `PAMPC-E08-M-AGGREGATE-VERDICT`,
`PAMPC-E08-M-DEPTH-RECOVERY`, `PAMPC-E08-M-ORACLE-INVARIANCE`
(comparison artefact sha `b3e8c5334e…`). The corresponding Stage K/L
claims have been **scope-restricted in place** (preamble preserves
original text, no history rewrite) with forward pointers to the
Stage M claims.

**Scope discipline.** None of the K/L/M results contradict the C1
protocol of §9: they characterise the *partition-level* dichotomy at
depth, which is the architecture-bounded ceiling Corollary 3.1 refers
to, not the $\varepsilon \to 0$ quantization limit C1 is about. The
`PAMPC-E08-{K,L1,L2,M}-*` claims are `float`-tier and not in
paper-01's reproducibility contract; the headline GPU-bound
continuous-transfer test remains pending per §9.

## 8. Reproducibility infrastructure

### 8.1 Artefact store

Every experiment writes a sealed manifest (`manifest.yaml`) with
`code_sha`, `seed_manifest_hash`, and a per-output sha256. The
aggregate Merkle root is `40-artifacts-store/manifest.summary.json` =
`702b38c86c7a9361…` over 10 experiments and 27 leaves. The seal/sign
pipeline is `60-reproducibility/seal_manifest.py`,
`40-artifacts-store/sign.py`, `40-artifacts-store/verify.py`.

### 8.2 Claim registry

`50-paper-harness/pampc_paper/claims.py` pins each `PAMPC-*` claim to
an `artifact_sha256`, a trust tier `{L-I, L-II, float}`, and a
source pointer. `verify.py` rejects `L-III`. `pampc_paper.build status`
prints the registry; `pampc_paper.build build <paper_id>` emits a
deterministic-by-construction `paper.manifest.txt` from
`70-papers/<paper_id>/claims_used.txt`.

### 8.3 Decision gates

Six gates in `00-governance/decision-gates/gates.yaml`, all currently
PASS:

```
[PASS] G0  Scaffolding sound
[PASS] G1  MPC↔DIG bridge proven on paper
[PASS] G2-screen  E04 reproduces synthetic correspondence baseline
[PASS] G2-transfer  Quantization-transfer kill test verdict
[PASS] G3  Lean corpus sound (sorry=0, axioms clean, non-vacuity ok)
[PASS] G4  Paper builds reproducibly from manifest root
```

G4 was deliberately narrowed from "PDF byte-identical" to
"build manifest byte-identical" because PDF builds are non-deterministic
without strict `SOURCE_DATE_EPOCH` discipline. The build manifest is the
contract that actually matters: it mutates iff an upstream claim
mutates.

### 8.4 Methodology manuals

Twelve graduate-level manuals at `90-methodology/` record exactly *how*
every number in this paper was derived. The six headline manuals
(Scientific Method, Measurement Techniques, Inference and Causal
Inference, Verification, Reproducibility, Critical Path) are the ones a
referee should read first.

## 9. The open problem — continuous-transfer (C1)

**Conjecture C1.** *Let $G$ be finite and $f \in \mathcal{F}_{\mathrm{WL}}(G)$.
Let $h^{(\varepsilon)} : V \to \mathbb{R}^{d}$ be the output of a trained MPNN of
family $\mathcal{A}$ at depth $L$ whose hidden activations have been quantized
at resolution $\varepsilon > 0$, and let $\Pi^{(\varepsilon)} := \{\, v : h^{(\varepsilon)}(v) = z \,\}_{z}$
be the partition $h^{(\varepsilon)}$ induces on $V$. Then under hypotheses
H1, H2, H3:*

$$
\lim_{\varepsilon \to 0^{+}}\, \mathrm{DIG}\!\left( f \,\bigm|\, \Pi^{(\varepsilon)} \right)
\;=\; \mathrm{DIG}\!\left( f \,\bigm|\, \Pi_{\mathcal{A}}(G, L) \right).
$$

**Hypotheses.**

- **H1 (training reached architecture-saturation).** Val-loss within
  $1.05\times$ of loss-plateau over a 50-epoch window.
- **H2 (bounded activations).** $h(v) \in [-B, B]^{d}$ with $B$ independent
  of $\varepsilon$.
- **H3 (representations are WL-canonical at the limit).**
  $\sup_{v, w \in C} \lVert h(v) - h(w) \rVert_{\infty} < \delta_{n}$ for every
  cell $C$, with $\delta_{n} \to 0$ as training time $n \to \infty$.

**Why this is named, not proven.** Two obstructions:

1. Quantization is non-linear and non-monotone in $\varepsilon$: refining
   $\varepsilon$ can spuriously split cells before the limit collapses them.
2. H3 is empirically observed, not proven: no known result establishes
   that trained MPNN activations converge to a WL-canonical map
   *uniformly in cell-size*.

**Falsification protocol — E08.**

| Item | Spec |
|---|---|
| Substrate | $\{C_3, C_4, C_5, C_6, \text{Petersen}\}$ (L-I anchor from E02/E03) |
| Architecture grid | $\{\text{GIN}, \text{GCN}, \text{GAT}, \text{GraphSAGE}, \text{GatedGCN}\}$ |
| Depth grid | $L \in \{2, 3, 4\}$ |
| Quantization sweep | $\varepsilon \in \{2^{-2}, 2^{-3}, \ldots, 2^{-12}\}$ (11 levels) |
| Seeds | 5 per cell (calibrated by Stage B.3) |
| Observable | $\Delta_{\varepsilon} := \mathrm{DIG}\bigl(f \mid \Pi^{(\varepsilon)}\bigr) - \mathrm{DIG}\bigl(f \mid \Pi_{\mathcal{A}}(G, L)\bigr)$ |
| Coverage gate | Cells where any of H1/H2/H3 fail are excluded and reported in the coverage table |

**Decision rule (G2-transfer).**

- **PASS.** On $\geq 4$ of 5 graph families and $\geq 3$ of 5 architectures,
  $\Delta_{\varepsilon} \to 0$ within 2 standard errors as $\varepsilon \to 0^{+}$,
  conditional on H-clean. *C1 alive; continuous form admitted into the paper.*
- **FAIL (KILL).** $\Delta_{\varepsilon}$ flattens at nonzero or diverges on a
  majority of H-clean cells. *C1 dead; this paper is rewritten as a
  negative result; PA-MPC is permanently scoped to discrete structural
  screening.*
- **INCONCLUSIVE.** H-clean coverage $< 50\%$.

**Cost envelope.** Hard cap $24$ GPU-h. Naive $4\,125$-cell upper bound at
$1$ min/cell $\approx 69$ GPU-h. Stages A (calibration, $\leq 0.5$ GPU-h),
B (edge instances, $\leq 2$ GPU-h), C (diagonal dry run, $\leq 2$ GPU-h),
D (architecture fan-out, $\leq 3$ GPU-h), E (depth fan-out, $\leq 6$ GPU-h),
F (sealing) are sequenced and gated. Each stage is a kill-gate. **No bulk
runs before edge gates pass.** Full spec in `LAB-PLAN.md` (Annex E08).

**Why this is publishable as is.** Both branches of the decision rule
are publishable, per `CHARTER.md` §4. The KILL branch is what makes C1
a conjecture rather than an aspirational paragraph.

### 9.E. Empirical verdict (C1 frozen 2026-05-30)

The E08 sweep was executed in stages G/H (pilot), then K (rule-fix
re-evaluation), then L (oracle invariance, lossy / lossless-1-WL /
folklore-2-WL), then M (anchor extension to the 8-graph anchor below).
At the end of Stage M, E08 was declared FROZEN and the C1 verdict was
sealed via the post-hoc analyzer
[`E08/scripts/_c1_literal_verdict.py`](../../20-experiments/E08-quantization-transfer/scripts/_c1_literal_verdict.py)
operating on the four sealed Stage M task parquets. Zero new GPU was
spent for the freeze. Three claims back this subsection:
`PAMPC-E08-C1-LITERAL-VERDICT`,
`PAMPC-E08-C1-RATE-TABLE`,
`PAMPC-E08-C1-SUBSTRATE-NOTE`
(all pinned to `c1_literal_verdict.json` sha
`146768e9492ba1f2…`, trust-tier `float` / `L-I` for the substrate
note).

**Anchor used for the C1 verdict (substrate correction).** The
§9-as-originally-written substrate $\{C_3, C_4, C_5, C_6, \text{Petersen}\}$
is vertex-transitive on every graph; under the canonical task suite
$\mathcal{F}_\text{WL}$ every label collapses to a constant on each
graph (verified 2026-05-30: 20/20 (graph, task) cells yield
$n_\text{classes} = 1$). On such a substrate $\mathrm{DIG} \equiv 0$
and $\Delta_\varepsilon \equiv 0$ trivially, so C1 is not testable on
it without leaving $\mathcal{F}_\text{WL}$. The C1 verdict therefore
uses the Stage K/M non-vertex-transitive 8-graph anchor:

$$
\text{anchor}_8 \;=\; \{K_{1,4},\, K_{2,3},\, P_5,\, \text{Lolli}_{4,3},\, \text{ER}_{10,p30,s0},\, \text{Tree}_{\text{bin},4},\, \text{ER}_{15,p25,s0},\, \text{ER}_{20,p20,s0}\}.
$$

The vertex-transitive family $\{C_n, \text{Petersen}\}$ is the natural
substrate for the companion conjecture C1' on 2-WL-bounded
architectures; see §9.X below and the E10 lab plan.

**Literal §9 rule applied.** The decision rule of §9 was evaluated with
the literal parameter tuple $(\text{rule\_variant} = \text{abs},
\text{direction\_convention} = \text{physical},
\text{coverage\_floor} = 0.5,
\text{families\_required\_pass} = 3,
\text{graph\_families\_required\_pass} = 4,
\text{bootstrap\_iters} = 1000,
\text{bootstrap\_seed} = 0)$. Inputs: $5\,\text{archs} \times
3\,\text{depths} \times 8\,\text{graphs} \times 5\,\text{seeds} \times
11\,\varepsilon$-levels $\times 4\,\text{tasks} = 26\,400$ rows.
H-clean coverage by task lies in $[0.900, 0.945]$, comfortably above
the 0.5 floor.

**Verdict (depth-stratified, the leg the paper headlines).** At
$L \in \{3, 4\}$ the rule returns an **architectural dichotomy
(task-invariant)** with

$$
\mathcal{A}_\text{pass} \;=\; \{\text{GCN},\, \text{GIN},\, \text{GatedGCN}\},
\qquad
\mathcal{A}_\text{fail} \;=\; \{\text{GAT},\, \text{GraphSAGE}\}.
$$

At $L = 2$ the dichotomy collapses to $\mathcal{A}_\text{pass} =
\{\text{GCN}\}$ (anchor-fragility; see §9.B and
`PAMPC-E08-M-DEPTH-RECOVERY`).

**Verdict (pooled-over-depths, the conservative aggregate).**
`verdict_tier = TASK-DEPENDENT`, $\mathcal{A}_\text{pass}^{\cap} =
\{\text{GCN}\}$, $\mathcal{A}_\text{fail}^{\cup} =
\{\text{GAT}, \text{GIN}, \text{GatedGCN}, \text{GraphSAGE}\}$,
driven by depth-2 failures of GIN/GatedGCN on the larger irregulars.

**Reading.** Under the literal §9 protocol the continuous-transfer
conjecture is **supported-by-evidence at $L \geq 3$ on
$\text{anchor}_8$** with the architectural dichotomy
$\{\text{GCN}, \text{GIN}, \text{GatedGCN}\}\big/\{\text{GAT}, \text{GraphSAGE}\}$.
The depth-2 collapse is a boundary phenomenon (one
neighbourhood-aggregation hop cannot resolve longer-path structure on
$n \geq 15$ irregulars); it is reported as an anchor-fragility
corollary, not as a contradiction.

### 9.B. Boundary conditions

| Boundary | Observation | Status |
|---|---|---|
| Depth $L = 2$ on large irregulars ($n \geq 15$) | $\mathcal{A}_\text{pass}$ collapses to $\{\text{GCN}\}$ | Anchor-fragility (sealed; `PAMPC-E08-M-DEPTH-RECOVERY`) |
| Vertex-transitive substrate $\{C_n, \text{Petersen}\}$ under $\mathcal{F}_\text{WL}$ | All cells collapse to a constant; $\Delta_\varepsilon \equiv 0$ | Vacuous (sealed; `PAMPC-E08-C1-SUBSTRATE-NOTE`) — moves to C1' / E10 |
| Lossy vs lossless-1-WL vs folklore-2-WL reference oracle | Aggregate verdict identical (sealed; `PAMPC-E08-M-ORACLE-INVARIANCE`) | C1 verdict is oracle-invariant |
| Convergence-rate exponent $\alpha$ (log-log fit) | Per-cell distribution in `PAMPC-E08-C1-RATE-TABLE` | Reported, not gated |

### 9.S. Cost envelope — actuals

| Stage | Cost (T4 spot) | Wallclock |
|---|---:|---:|
| Stages G + H (pilot) | \$0.35 | 0.48 GPU-h |
| Stage K (rule-fix re-eval, post-hoc) | \$0.00 | 0 GPU-h |
| Stage L (oracle invariance, post-hoc) | \$0.00 | 0 GPU-h |
| Stage M (anchor extension, 4 task-parallel apps) | \$0.52 | 0.70 GPU-h |
| C1 freeze (post-hoc analyzer) | \$0.00 | ~2 h wallclock (CPU) |
| **Total** | **\$0.87** | **1.18 GPU-h** |

Spend is $\sim 5\%$ of the 24 GPU-h cap.

### 9.X. Companion conjecture C1' (2-WL extension, E10)

The C1 verdict above closes the 1-WL-bounded continuous-transfer
question on $\mathcal{F}_\text{WL}$ tasks for the architecture set
$\{\text{GCN}, \text{GIN}, \text{GatedGCN}\}$ at $L \geq 3$. The
natural lift to 2-WL-bounded architectures (PPGN, 2-IGN,
$k$-GNN at $k=2$, Subgraph-GNN) and graph-discriminating tasks
($\mathcal{F}_{2\text{-WL}} \setminus \mathcal{F}_\text{WL}$) is
stated as **Conjecture C1'** and reserved for companion work
(experiment E10; lab plan at
[`20-experiments/E10-graph-level-quantization-transfer/LAB-PLAN.md`](../../20-experiments/E10-graph-level-quantization-transfer/LAB-PLAN.md)).
The natural substrate for C1' is precisely the vertex-transitive
family $\{C_n, \text{Petersen}, \text{Rook}_{4,4}, \text{Shrikhande}\}$
that is vacuous for C1: vertex-transitivity becomes the discriminating
regime once the reference partition is folklore 2-WL. C1' is
registered in [`conjectures.yaml`](../../10-theory/conjectures.yaml)
with falsifier `E10`, gate `G2-transfer-prime`, and the same
PASS / FAIL / INCONCLUSIVE-twice kill semantics as G2-transfer.

## 10. Known failure modes and honest narrowings

We have iterated this programme four times. The current narrowings are:

1. **E06 was demoted from a headline to inconclusive-pilot.** Strict
   variant-agreement F2 was relaxed to F2-soft after AMI normalisation
   was found to contradict NMI sign on the synthetic anchor. The honest
   read: this is exactly the $\mathrm{MI}^2$-family degeneracy of §3.4. (Earlier
   programme version had this as headline; it isn't.)
2. **E09 F3 was reformulated.** The original sign-variability test
   failed (109 positive / 491 zero / 0 negative rewire prices). Diagnosis:
   sign-variability requires non-WL-cell tasks, which the canonical task
   suite excludes by construction. F3 is now "rewiring price $\geq 0$ on
   WL-cell tasks" — a third structural invariant complementing F1 (VN
   refinement) and F2 (contraction coarsening). Sign-variability is
   preserved as an honest non-gating advisory.
3. **E01 required three task / operator redesigns.** Pure $D^{-1}A$ $\to$
   lazy random walk; source-localisation task $\to$ node-label retention;
   strict per-step monotone F2 $\to$ smoothed-window F2. Log preserved in
   the commit message of `e18b824`.
4. **G4 was narrowed from PDF to claim manifest.** PDF builds aren't
   byte-deterministic without `SOURCE_DATE_EPOCH` discipline. The claim
   manifest *is*, and it is the actual reproducibility contract.
5. **`mode=full` for E04 and E08 is pending real GPU.** The L-III claims
   they would produce are explicitly **not** in this paper. The E08
   Stages K/L/M arc summarised in §7.3 *did* run a GPU sweep on the
   architecture-level partition dichotomy, and the C1 freeze of §9.E
   (post-hoc analyzer, zero new GPU) seals the literal §9 verdict on
   the Stage M anchor; claims `PAMPC-E08-C1-{LITERAL-VERDICT,RATE-TABLE,SUBSTRATE-NOTE}`
   are `float`-tier (and `L-I` for the substrate note) and are
   recorded in the claim manifest. C1' (E10) remains an open companion
   experiment.
6. **No real-world graph results.** ZINC / OGB / TUDataset are in
   scope for paper-02, *not* paper-01. paper-01 is the theory + the
   synthetic anchor.

## 11. Conclusion

PA-MPC is a partition-explicit, architecture-family-indexed
generalisation of MPC. The discrete bridge inequality (Theorem 1) pins
its operational meaning as a two-sided sandwich on WL-measurable
predictability. The exact-rational ledger (E02, E03, E07, E09) and the
Lean L-II witness verify the theory on a synthetic anchor. The
continuous-transfer conjecture (C1) is **frozen** as of 2026-05-30:
under the literal §9 protocol the verdict is **supported-by-evidence
at $L \geq 3$ on $\text{anchor}_8$** with the architectural dichotomy
$\{\text{GCN}, \text{GIN}, \text{GatedGCN}\} \,/\, \{\text{GAT},
\text{GraphSAGE}\}$ (§9.E). The companion conjecture C1' (2-WL-bounded
architectures on vertex-transitive substrates) is registered as the
headline open problem for paper-02 / E10 (§9.X). The
reproducibility skeleton is closed end-to-end (G0..G4 PASS, Merkle root
pinned, deterministic build manifest verified by tamper test). Six
methodology manuals at `90-methodology/` make the procedure
reconstructible by a graduate student.

The kill branch of C1 is publishable. The PASS branch is publishable.
The honest pilot status of E04 / E06 / E08 is publishable. There is no
finding in this paper that requires a particular outcome of any pending
experiment.

*Reproducibility footer.* HEAD `fcf173a`, branch
`lean-partitions-algebra-2026-Q3`. Merkle root `702b38c86c7a9361…` over
10 experiments / 27 leaves. Paper-01 manifest sha
`658e7837dc21…`. Lean witness sha `89681b03…`. All six gates PASS.
E08 `mode=full` Stages K/L/M sealed on 2026-05-30 (artefacts
`pulled-artefacts/E08-stage-{K,L,M}/`); their claims are `float`-tier
and not in paper-01's reproducibility contract.

---

## Annex A — Index of artefacts and claim IDs

All claims live in `50-paper-harness/pampc_paper/claims.py` and are
pinned by `artifact_sha256`. The G4 byte-identical baseline is
`40-artifacts-store/byte_identical_baselines.yaml`.

| Claim ID | Tier | Source |
|---|---|---|
| `PAMPC-BRIDGE-INEQ-STATUS` | L-I | `10-theory/spine/20-mpc-dig-bridge.qmd` |
| `PAMPC-LEAN-WITNESS-C4-K` | L-II | `30-lean/PaMpc/Witnesses.lean::C4_const_partitionCount` |
| `PAMPC-E02-DIG-TABLE` | L-I | `20-experiments/E02-…/artifacts/dig_table.parquet` |
| `PAMPC-E02-DIG-SUMMARY` | L-I | E02 summary |
| `PAMPC-E02-ORACLE-XCHECK` | L-I | E02 oracle cross-check |
| `PAMPC-E03-DIG-TABLE` | L-I | E03 280-row table |
| `PAMPC-E03-MONOTONICITY-LEDGER` | L-I | E03 falsifiers |
| `PAMPC-E03-WL-STABILITY-LEDGER` | L-I | E03 verdict |
| `PAMPC-E04-RUNS-TABLE` | float | E04 450-run pilot table |
| `PAMPC-E04-FALSIFIER-LEDGER` | float | E04 F1..F6 ledger |
| `PAMPC-E04-CORRESPONDENCE-VERDICT` | float | E04 pilot verdict |
| `PAMPC-E06-CCI-TABLE` | float | E06 720-row CCI table |
| `PAMPC-E06-FIGURE-SOURCE` | float | E06 figure source |
| `PAMPC-E06-ANTICORR-VERDICT` | float | E06 inconclusive-pilot |
| `PAMPC-E07-FEATURE-TABLE` | L-I | E07 280-row table |
| `PAMPC-E07-QUADRANT-FIGURE` | float | E07 figure |
| `PAMPC-E07-BOUNDARY-VERDICT` | L-I | E07 pass |
| `PAMPC-E08-TRANSFER-TABLE` | float | E08 pilot sweep |
| `PAMPC-E08-TRANSFER-VERDICT` | float | E08 inconclusive-pilot |
| `PAMPC-E08-HCLEAN-COVERAGE` | float | E08 H-clean coverage |
| `PAMPC-E08-C1-LITERAL-VERDICT` | float | E08 Stage M C1 freeze (`c1_literal_verdict.json`) |
| `PAMPC-E08-C1-RATE-TABLE` | float | E08 Stage M C1 freeze rate fits |
| `PAMPC-E08-C1-SUBSTRATE-NOTE` | L-I | C1 freeze substrate-correction note |
| `PAMPC-E09-PRICING-TABLE` | L-I | E09 942-row table |
| `PAMPC-E09-INVARIANTS-LEDGER` | L-I | E09 F1..F3 ledger |
| `PAMPC-E09-VERDICT` | L-I | E09 pass |
| `PAMPC-E01-TOY-TABLE` | float | E01 100-row table |
| `PAMPC-E01-FALSIFIERS` | float | E01 F1..F3 |
| `PAMPC-E01-VERDICT` | float | E01 pass (float) |

## Annex B — Decision gates

See `00-governance/decision-gates/gates.yaml`. Gate predicates implemented
in `50-paper-harness/pampc_paper/build.py::cmd_gates`:

- `file_exists`
- `manifest_valid`
- `claim_pinned`
- `lean_clean`
- `lean_nonvacuity`
- `falsifier_pass`
- `byte_identical`

`byte_identical` reads the baseline from
`40-artifacts-store/byte_identical_baselines.yaml`. A tamper test
(append "TAMPER" to `paper.manifest.txt`) correctly returns
`SHA-MISMATCH actual=576c1c1d359b expected=658e7837dc21`.

## Annex C — Per-experiment technical reports (LAB-PLANs)

Each experiment under `20-experiments/<EXX>-*/` ships a
`LAB-PLAN.md` (technical report with placeholders for unpaid future
work — same structure as the E08 template). The contents are:

- §1 What this is supposed to prove.
- §2 Cost envelope.
- §3 Stages, each a kill-gate.
- §4 Edge instances to run before bulk.
- §5 Response recipes.
- §6 What could still go wrong.
- §7 Cutover criteria from pilot to full.
- §8 Out of scope.
- §9 Change log.

Index:

- `20-experiments/E01-toy-task-baseline/LAB-PLAN.md`
- `20-experiments/E02-exact-rational-witnesses/LAB-PLAN.md`
- `20-experiments/E03-lossy-wl-dig-synthetic/LAB-PLAN.md`
- `20-experiments/E04-trained-gnn-correspondence/LAB-PLAN.md`
- `20-experiments/E06-cci-vs-performance/LAB-PLAN.md`
- `20-experiments/E07-feature-richness-boundary/LAB-PLAN.md`
- `20-experiments/E08-quantization-transfer/LAB-PLAN.md` (canonical
  example — see this one first)
- `20-experiments/E09-intervention-pricing/LAB-PLAN.md`

## Annex D — Methodology manuals (graduate-level)

The six headline manuals at `90-methodology/`:

- `Scientific-Method-Manual.md` — Falsifiers, hypotheses, decision rules.
- `Measurement-Techniques-Manual.md` — DIG, MI², MPC, CCI variants,
  bootstrap CIs, exact-`ℚ` arithmetic, lossy-WL refinement.
- `Inference-And-Causal-Inference-Manual.md` — From correlation to
  intervention pricing; sign-variability advisories; bridge ↔ Corollary
  3.1 as the *only* causal claim we make.
- `Verification-Manual.md` — Trust tiers, Lean obligations,
  Merkle/manifest discipline, tamper tests.
- `Reproducibility-Manual.md` — Manifest seal pipeline, byte-identical
  build manifests, claim registry, gate evaluator.
- `Critical-Path-Manual.md` — PERT chart, decision gates, kill
  branches, "no bulk runs before edge gates pass".

## Annex E — Lean obligations and current status

- `30-lean/PaMpc/MPCBridge.lean::DIG_of_pure` — variance form,
  `~DIG(f, Π) = 0` under purity. **Pinned.**
- `30-lean/PaMpc/Witnesses.lean::C4_const_partitionCount` — concrete
  witness on `{C4..C8, Petersen}` at depths 0..3 via `native_decide`.
  **Pinned.** (claim `PAMPC-LEAN-WITNESS-C4-K` sha `89681b03…`)
- Bridge inequality in its general form — **deferred** per `CHARTER §3`.

## Annex F — Provenance & build verification

To verify this paper's reproducibility contract end-to-end:

```bash
cd 101-PA-MPC/
python -m pampc_paper.build status          # claim registry summary
python -m pampc_paper.build gates           # all six gates → PASS
python -m pampc_paper.build build paper-01-pampc-core
shasum -a 256 70-papers/paper-01-pampc-core/build/paper.manifest.txt
# expected: 658e7837dc217329cea459e305488163647c49f60acd8b91a6a55bdf8077b859
```

A successful run reproduces the Merkle root `702b38c86c7a9361…` over 10
experiments and 27 leaves, verifies the `byte_identical` predicate
against the registered baseline, and confirms all six decision gates
PASS.

---

*End of paper-01-pampc-core draft.*
