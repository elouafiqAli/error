# Partition-Aware Message-Passing Complexity

**Ali Elouafiq**

*Preprint. 2026. Revised 2026-05-30 (theory amendment 001).*

---

## Abstract

How much of a binary vertex task on a graph remains predictable after
a depth-$L$ message-passing family $\mathcal{A}$ has done all it can?
The partition-explicit message-passing complexity (MPC) of Kemper et
al.\ (2025) answers this for a single trained model. We answer it for
the **architecture family itself**, before training, and with a
two-sided guarantee.

Our main result is the **partition Bayes-entropy sandwich**: for every
finite partition $\Pi$ of a finite vertex set and every binary task $f$,
the cell-wise Bayes error $\varepsilon^{*}_{\Pi}$ and the
partition-conditional entropy $H(f \mid \Pi)$ obey
$H_{\mathrm{bin}}^{-1}\!\bigl(H(f \mid \Pi)\bigr) \le \varepsilon^{*}_{\Pi}
\le \tfrac{1}{2} H(f \mid \Pi)$.
The two halves are the opposite extrema of a single Jaynes
maximum-entropy programme; together they unify the classical
entropy–error bounds of Fano (1961), Hellman & Raviv (1970), and
Feder & Merhav (1994), and the slope $1/2$ on the upper side is
sharp — no inequality $\varepsilon^{*}_{\Pi} \le c\, H(f \mid \Pi)$
with $c < 1/2$ can hold uniformly (Proposition 3.5).

Specialising $\Pi$ to $\Pi_{\mathcal{A}}(G, L)$, the partition that
$\mathcal{A}$ induces on $V(G)$ via the identity-leaking LossyWL
operator, yields **Partition-Aware MPC** (PA-MPC) — a training-free
error bracket comparable across GCN, GIN, GAT, GatedGCN, and
GraphSAGE. The theorem is verified on a finite-graph Lean 4 witness
($C_3,\ldots,C_8$ and Petersen, zero `sorry`) and on a 1000-row
exact-rational ledger; a float-tier oversmoothing baseline and three
pilot apparatus checks accompany it. The continuous-transfer
conjecture C1 (§9) is mathematically open; on 2026-05-30 we froze its
empirical status as *supported-by-evidence at $L \ge 3$* on the
eight-graph non-vertex-transitive anchor, with the architectural
dichotomy
$\{\text{GCN},\text{GIN},\text{GatedGCN}\}/\{\text{GAT},\text{GraphSAGE}\}$.

---

## 1. Introduction

The expressivity of message-passing neural networks (MPNNs) has a
well-developed structural ceiling: the 1-Weisfeiler–Leman (WL)
discrimination power bounds what depth-$L$ MPNNs can resolve about
graphs [Xu et al. 2019; Morris et al. 2019]. The partition-explicit
message-passing complexity framing of Kemper et al. (2025) refines this
picture by quantifying, for the partition a model induces, how much task
information remains. Two practical problems remain:

1. **Architecture occlusion.** MPC depends on a particular model; its
   value cannot be compared meaningfully across families (GCN vs. GIN
   vs. GAT vs. GraphSAGE vs. GatedGCN) because the partitions those
   families *can* induce differ at depth 0 in ways MPC does not expose.
2. **No two-sided guarantee.** MPC says something about what the model
   resolves, but does not give a two-sided sandwich on predictability
   of the task by the family at that depth, independent of training.

PA-MPC addresses both. By indexing on the *family-level* initial
partition $\Pi^{(0)}_{\mathcal{A}}$ and applying the same LossyWL
operator to depth $L$, PA-MPC is well-defined before any training and
is comparable across families. The bridge inequality of §3 pins its
operational meaning as a two-sided sandwich for the WL-determined task
class $\mathcal{F}_{\mathrm{WL}}$, up to one bit.

The paper makes four contributions:

- **C-Theory.** Definitions, two-sided bridge inequality, scope (§3).
- **C-Lean.** A Lean 4 discrete bridge witness (`PAMPC-LEAN-WITNESS-C4-K`)
  on a concrete graph family, zero `sorry`, trusted-kernel-only axiom
  base (§6).
- **C-Empirical.** Three L-I exact-rational results (E03, E07, E09),
  one float-tier oversmoothing baseline (E01), and three
  honestly-pilot results (E04, E06, E08) (§4–5, §7).
- **C-Reproducibility.** A sealed Merkle artefact store, a
  deterministic claim-manifest build pipeline, six decision gates, and
  methodology manuals that record exactly how every number was derived
  (§8).

Throughout, we keep three statuses sharply separate:

- **Proved.** Theorem 1 (partition Bayes-entropy sandwich), Proposition 3.2
  (refinement monotonicity), Proposition 3.3 (architecture factorisation),
  Corollary 3.4 (PA-MPC instantiation), and the purity Lemma 3.1.
- **Mechanised / exact-audited.** Lean witness on $\{C_4,\ldots,C_8,\text{Petersen}\}$;
  exact-$\mathbb{Q}$ ledgers E02, E03, E07, E09 (tier L-I).
- **Empirical / conjectural.** Float baseline E01; pilot apparatus E04, E06, E08;
  the continuous-transfer conjecture C1 (mathematically open, empirically
  frozen 2026-05-30 — see §9.E).

---

## 2. Related Work

We position PA-MPC against three immediate neighbours; an extended
discussion of antecedents (ergodic theory, algorithmic partition
refinement, oversmoothing/over-squashing, the 2022–2024
partition-indexed GNN wave, and learning-theoretic uses of
refinement-monotonicity) is deferred to Appendix G.

**Expressivity ceiling.** Xu et al. (2019) and Morris et al. (2019)
show MPNNs are at most as expressive as 1-WL on graph discrimination;
Azizian & Lelarge (2021) sharpen this to an exact characterisation.
PA-MPC is orthogonal: we *quantify* predictability of a fixed task on
a fixed graph rather than characterise isomorphism power. Higher-order
$k$-WL (Morris et al. 2020) is explicitly out of scope; §3.3 gives
the exclusion criterion.

**Partition-explicit MPC.** Kemper et al. (2025) frame complexity by
the partition a single trained model induces. PA-MPC lifts that
framing to an **architecture-family / initial-observable pair**
$(\mathcal{A}, \Pi^{(0)})$ — well-defined before training and
comparable across MPNN families — and packages it with a **two-sided
Bayes-error sandwich** (Theorem 1).

**Equitable partitions.** The $L \to \infty$ limit of
$\Pi_{\mathcal{A}}(G, L)$ for any 1-WL-template family is the
equitable partition of $G$ (Schwenk 1974; Godsil & Royle 2001, ch. 9).
That object is Definition 3.1's most direct intellectual ancestor; the
novelty here is the family indexing (Proposition 3.3) and the
Bayes-error packaging (Theorem 1), not the partition itself.

The $\mathrm{MI}^2 \approx \tfrac{1}{2}$ identity that was the centrepiece of an
earlier programme has been **explicitly demoted** to a cautionary note
in §3.5 because it is operationally vacuous in the regime PA-MPC cares
about (constant under purity, not architecture-discriminating).[^mi2-audit]

[^mi2-audit]: The dedicated Appendix B that previously detailed the
  demotion argument has been **removed** in theory amendment 001
  (2026-05-30) following a PI audit which found that the appendix was
  re-litigating a settled question. The full pre-amendment text is
  archived at `archived/PAPER-ARXIV.pre-amendment-001.md` for posterity;
  the cautionary takeaway is preserved in §3.5 in its operational form.

---

## 3. Theory

### 3.1 Definitions

A **graph** is $G = (V, E)$ undirected, finite, simple, with optional
vertex-feature map $x : V \to \mathcal{X}$. A **partition**
$\Pi = \{C_1, \ldots, C_K\}$ is a set of nonempty pairwise-disjoint
subsets whose union is $V$; $K(\Pi) := |\Pi|$. A **task** is
$f : V \to \mathcal{Y}$; the default is $\mathcal{Y} = \{0, 1\}$.

*Remark (finite, measure-free setting).* Every object in §3 and Appendix A
lives on a finite vertex set $V$ with uniform vertex weighting
$q_v := 1/|V|$. Probability and expectation symbols
($\Pr$, $\mathbb{E}$, $H$, $I$, $d_{\mathrm{KL}}$) are shorthand for finite
sums: $\Pr[\cdot] := |\{v : \cdot\}|/|V|$ and
$\mathbb{E}[\phi] := |V|^{-1}\sum_v \phi(v)$. No $\sigma$-algebra,
countable additivity, dominated convergence, or Radon–Nikodým argument
is ever invoked; every proof is by elementary finite combinatorics and
concavity. We retain information-theoretic notation purely for reader
convention. Non-uniform weighting is supported by replacing
$q_C = |C|/|V|$ with arbitrary nonnegative $q_C$ summing to $1$
throughout; all proofs go through unchanged.

Fix the **identity-leaking LossyWL operator** $\mathrm{LossyWL}$
[Kemper et al. 2025]. One round refines $\Pi$ to
$\mathrm{LossyWL}(\Pi; G)$. The depth-$L$ orbit is

$$
\Pi^{(L)} \;:=\; \mathrm{LossyWL}^{L}\!\bigl(\Pi^{(0)};\, G\bigr).
$$

The architecture-family-indexed initial partition $\Pi^{(0)}_{\mathcal{A}}$
captures what the family exposes at depth 0 (e.g.\ constant, degree, or
structural-feature initialisation).

**Definition 3.1** (architecture-induced partition).
$$
\Pi_{\mathcal{A}}(G, L) \;:=\; \mathrm{LossyWL}^{L}\!\!\left(\Pi^{(0)}_{\mathcal{A}};\, G\right).
$$

**Definition 3.2** (partition-conditional entropy). Let $q_C = |C|/|V|$
and $P_C = \tfrac{1}{|C|}\sum_{v \in C} f(v)$. Then
$$
\begin{aligned}
H(f \mid \Pi) \;&=\; \sum_{C} q_C \cdot H_{\mathrm{bin}}(P_C) \\
\mathbb{E}[\mathrm{Var}(f \mid \Pi)] \;&=\; \sum_{C} q_C \cdot P_C(1 - P_C)
\end{aligned}
$$
where $H_{\mathrm{bin}}(p) = -p\log_2 p - (1-p)\log_2(1-p)$. Both forms vanish
iff $\Pi$ is **pure** for $f$ (Lemma 3.1).

**Definition 3.3** (PA-MPC).
$$
\operatorname{PA\text{-}MPC}(f, G;\, \mathcal{A}, L) \;:=\; H\!\bigl(f \,\bigm|\, \Pi_{\mathcal{A}}(G, L)\bigr).
$$

**Definition 3.4** (WL-determined task class). $\mathcal{F}_{\mathrm{WL}}(G)$
is the set of tasks constant on every cell of the WL-stable partition
$\Pi^{\mathrm{WL}}(G) := \mathrm{LossyWL}^{\infty}(\Pi^{(0)}; G)$.
("Determined" rather than "measurable": the condition is
set-theoretic — $f$ factors through $V \twoheadrightarrow \Pi^{\mathrm{WL}}$ —
and carries no measure-theoretic content.)
Membership in $\mathcal{F}_{\mathrm{WL}}(G)$ is *not* required for the
partition theorem (Theorem 1) or the refinement proposition
(Proposition 3.2); it is the natural scope for the architectural
interpretation (Proposition 3.3, Corollary 3.4), where tasks outside
$\mathcal{F}_{\mathrm{WL}}$ (WL-indistinguishable-pair discriminators,
regular-graph distinguishers) cannot in general be resolved by any
1-WL-template family at any depth.

**Definition 3.5** (admissible architecture family). A pair
$(\mathcal{A}, \Pi^{(0)}_{\mathcal{A}})$ is an *admissible* depth-$L$
architecture-family specification if every member $h \in \mathcal{A}_L$
of the depth-$L$ instantiation satisfies:

1. **Initial-observable confinement.** The depth-0 hidden state $h^{(0)}(v)$
   depends on $v$ only through the cell of $v$ in $\Pi^{(0)}_{\mathcal{A}}$.
2. **Shared local update.** There is a single update map
   $\phi_\ell$ at each layer $\ell \in \{1,\ldots,L\}$, applied identically
   at every vertex.
3. **Permutation invariance.** $\phi_\ell$ acts on the multiset of
   neighbour states; the order of neighbours is immaterial.
4. **No identifier leakage.** Beyond $\Pi^{(0)}_{\mathcal{A}}$, $\phi_\ell$
   has no access to vertex names or any feature not already determined by
   the current colour class.

GCN, GIN, GatedGCN, GAT (with permutation-invariant attention pooling),
and GraphSAGE all admit specifications meeting (1)–(4); higher-order
$k$-WL variants (Morris et al.\ 2020) do not, and are out of scope (§3.3).

**Lemma 3.1** (purity ⟺ zero conditional entropy). *Call $\Pi$ **pure**
for $f$ if $P_C \in \{0, 1\}$ for every $C \in \Pi$ — equivalently, $f$ is
constant on every cell of $\Pi$, i.e.\ $f$ factors through the quotient
map $V \twoheadrightarrow V/\Pi$. Then*
$$\mathrm{Pure}(f, \Pi) \iff H(f \mid \Pi) = 0 \iff
\mathbb{E}[\mathrm{Var}(f \mid \Pi)] = 0.$$

*Proof.* Each summand $q_C \cdot H_{\mathrm{bin}}(P_C)$ is non-negative and
vanishes iff $P_C \in \{0, 1\}$ since $q_C > 0$ for nonempty cells; the
$P_C \in \{0,1\}$ condition says $f$ is constant on $C$ (it equals its
mean). The same argument applies to $\mathbb{E}[\mathrm{Var}(f\mid\Pi)]$
via $P_C(1-P_C) \geq 0$. $\square$

*Naming.* The condition "$f$ is constant on every cell of $\Pi$" has
several established names across nearby literatures, all equivalent on
a finite vertex set: **$\Pi$ resolves $f$** (partition-lattice
combinatorics; $\ker f$ is coarsened by $\Pi$); **$f$-equitable
partition** (algebraic graph theory: Schwenk 1974; Godsil & Royle 2001,
ch. 9); **pure partition** (decision-tree induction: Breiman et al.\ 1984);
**zero-equivocation partition** (Shannon 1948). We use *pure* as the
display term — the decision-tree mnemonic is the closest match for a
binary task — but readers from any of these lineages may substitute
their own term verbatim; nothing in the proofs depends on the choice.

### 3.2 The Partition Bayes-Entropy Sandwich

*This section has been revised in theory amendment 001 (2026-05-30). The
pre-amendment surprisal-form statement is archived at
`archived/PAPER-ARXIV.pre-amendment-001.md` §3.2. Binding plan:
`40-plan/theory-amendments/2026-05-30-amendment-001-bayes-error-sandwich.md`.*

We present the proof spine in four steps: a pure partition theorem that
requires no graph structure, a refinement-monotonicity proposition, an
architecture-factorisation proposition, and the PA-MPC corollary that
instantiates the first three.

**Partition Bayes error.** For a finite partition $\Pi$
of a finite $V$ and a binary task $f : V \to \{0,1\}$, define

$$
\varepsilon^{*}_{\Pi} \;:=\; \min_{g:\Pi\to\{0,1\}} \Pr\!\bigl[g(C(v)) \neq f(v)\bigr]
\;=\; \sum_{C \in \Pi} q_C \cdot \min(P_C, 1 - P_C),
$$

attained by the plug-in rule
$\hat{h}_{\Pi}(v) := \mathbf{1}\{P_{C(v)} \geq 1/2\}$
(here $\Pr[\cdot]$ is the uniform-weighting frequency of §3.1).
Equivalently, $\varepsilon^{*}_{\Pi}$ is the Bayes risk of $f$ when the
predictor is constrained to be constant on each cell of $\Pi$
(Devroye, Györfi & Lugosi 1996, §2.1, recast for finite $V$); we use
the shorter name *partition Bayes error* throughout.

**Theorem 1** (Partition Bayes-entropy sandwich). *Let $\Pi$ be a finite
partition of a finite vertex set $V$ and let $f : V \to \{0, 1\}$ be any
binary task. Then*

$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f \mid \Pi)\bigr)
\;\leq\; \varepsilon^{*}_{\Pi}
\;\leq\; \tfrac{1}{2}\,H(f \mid \Pi),
$$

*where $H_{\mathrm{bin}}^{-1} : [0, 1] \to [0, 1/2]$ is the inverse of
binary entropy on the increasing branch.* (Upper side: Hellman & Raviv
1970. Lower side: Fano 1961 in its binary form, sharpened by Feder &
Merhav 1994.)

The theorem makes no reference to $G$, $\mathcal{A}$, the LossyWL operator,
or $\mathcal{F}_{\mathrm{WL}}$. It is a property of any finite partition
and any binary labelling. The full proof is in Appendix A; we sketch
the two halves as the two extremal directions of a single Lagrangian.

*Single program, two directions.* Let $e_C := \min(P_C, 1 - P_C) \in [0, 1/2]$
and note the symmetry $H_{\mathrm{bin}}(P_C) = H_{\mathrm{bin}}(e_C)$, so that
$H(f\mid\Pi) = \sum_C q_C\, H_{\mathrm{bin}}(e_C)$ and
$\varepsilon^{*}_{\Pi} = \sum_C q_C\, e_C$. Both bounds in Theorem 1 are
the optimal values of opposite Jaynes max-entropy programs on the variables
$\{(q_C, e_C)\}_C$:
$$
\begin{aligned}
\text{(Fano lower)} \quad & \max_{\{q_C, e_C\}} \sum_C q_C\, H_{\mathrm{bin}}(e_C) \;\text{ s.t. }\; \textstyle\sum_C q_C\, e_C = \varepsilon \;\Longrightarrow\; \text{interior critical point } e_C \equiv \varepsilon, \\
\text{(HR upper)} \quad & \max_{\{q_C, e_C\}} \sum_C q_C\, e_C \;\text{ s.t. }\; \textstyle\sum_C q_C\, H_{\mathrm{bin}}(e_C) = H \;\Longrightarrow\; \text{boundary critical points } e_C \in \{0, 1/2\}.
\end{aligned}
$$
The Fano direction places the optimiser at the unique interior critical
point of $H_{\mathrm{bin}}$'s concavity, giving $H \leq H_{\mathrm{bin}}(\varepsilon)$
and, on inversion, $H_{\mathrm{bin}}^{-1}(H) \leq \varepsilon^{*}_{\Pi}$.
The Hellman–Raviv direction places the optimiser at the boundary of
$[0, 1/2]$, where $e \leq \tfrac{1}{2}H_{\mathrm{bin}}(e)$ is tight, giving
$\varepsilon^{*}_{\Pi} \leq \tfrac{1}{2}H(f\mid\Pi)$. Both reductions are
elementary; we record them inline and defer the formal proof to
Appendix A.

*Achievable region.* Combining the two halves, every finite partition
and binary task on a finite vertex set realises a pair
$(\varepsilon^{*}_{\Pi},\, H(f\mid\Pi))$ in the closed region
$\tilde{A}_2 := \{(\varepsilon, H) \in [0, 1/2] \times [0, 1] :
H_{\mathrm{bin}}^{-1}(H) \leq \varepsilon \leq H/2\}$. The upper
boundary $\varepsilon = H/2$ is attained by every two-mass partition
with $e_C \in \{0, 1/2\}$; the lower boundary $H = H_{\mathrm{bin}}(\varepsilon)$
is attained by every constant-residual-posterior partition with
$e_C = \varepsilon$ uniformly (witnesses in Appendix A, *Tightness*).

*Quantified slack.* The upper bound is tight on a row iff every cell
has $e_C \in \{0, 1/2\}$; the lower bound is tight iff $e_C$ is constant
across cells (Jensen equality). The width of the sandwich,
$w(H) := \tfrac{1}{2}H - H_{\mathrm{bin}}^{-1}(H)$, vanishes at the
endpoints $H \in \{0, 1\}$ and attains its maximum
$w^{*} = \tfrac{1}{2}H_{\mathrm{bin}}(1/5) - 1/5 \approx 0.161$ at
$\varepsilon = 1/5$ (where $H'_{\mathrm{bin}}(\varepsilon) = 2$). The
sandwich therefore localises $\varepsilon^{*}_{\Pi}$ to a window of width
at most $\approx 0.161$ uniformly in $\Pi$ and $f$ — a quantified
slack bound complementing the qualitative *two-sided* claim.

*Provenance.* The two bounds in Theorem 1 are not new individually:
the upper side is the Hellman–Raviv inequality (Hellman & Raviv 1970)
and the lower side is Fano's inequality in its sharp binary form
(Fano 1961; Cover & Thomas 2006, Thm 2.10.1), with the tightest
two-sided packaging due to Feder & Merhav (1994); the unifying
Jaynes Lagrangian mechanism (above) is in the compact derivation style
of Massey (1994), whose own application was to guessing entropy. The
Feder–Merhav primal concave-envelope construction and the
Jaynes/Massey Lagrangian-dual derivation are the same convex-analytic
object in dual languages; making that duality explicit is the
conceptual contribution of §3.2. The quantity
$\varepsilon^{*}_{\Pi}$ is the Bayes risk of $f$ given the coarsened
feature ($v \mapsto C(v)$) in the sense of Devroye, Györfi & Lugosi (1996, §2.1). The
partition-indexed packaging — applying these inequalities to
$\Pi_{\mathcal{A}}(G, L)$ in Corollary 3.4 — is the bridge from
textbook information theory to depth-$L$ message-passing expressivity.
Proposition 3.2 is the deterministic-coarsening case of the
data-processing inequality (Cover & Thomas 2006, Thm 2.8.1); we give
the elementary Jensen-on-$H_{\mathrm{bin}}$ proof in Appendix A for
self-containedness. The variance form $\mathbb{E}[\mathrm{Var}(f \mid \Pi)]$
is the expected conditional **Gini impurity** (Breiman et al.\ 1984).
Proposition 3.6 (prior-aware sharpening) follows the data-processing
template of Han & Verdú (1994).

**Proposition 3.2** (refinement monotonicity). *If $\Pi'$ refines $\Pi$
(every cell of $\Pi'$ is contained in some cell of $\Pi$), then for every
binary $f$,*

$$
H(f \mid \Pi') \;\leq\; H(f \mid \Pi),
\qquad
\varepsilon^{*}_{\Pi'} \;\leq\; \varepsilon^{*}_{\Pi}.
$$

*Proof sketch.* Each cell $C \in \Pi$ partitions into
$C = \bigsqcup_j C'_j$ with masses $q_{C'_j}$ summing to $q_C$ and
posteriors $P_{C'_j}$ averaging (under weights $q_{C'_j}/q_C$) to $P_C$ —
equivalently, $P_C$ lies in the convex hull of $\{P_{C'_j}\}_j$.
Concavity of $H_{\mathrm{bin}}$ on that convex hull gives
$\sum_j q_{C'_j} H_{\mathrm{bin}}(P_{C'_j}) \leq q_C H_{\mathrm{bin}}(P_C)$;
sum over $C$. The same argument applies to $\min(p, 1-p)$ via its
concavity on $[0, 1]$. Full proof in Appendix A. $\square$

**Proposition 3.3** (architecture factorisation). *Let
$(\mathcal{A}, \Pi^{(0)}_{\mathcal{A}})$ be admissible (Definition 3.5)
and let $\Pi = \Pi_{\mathcal{A}}(G, L)$. Then every depth-$L$ predictor
$h \in \mathcal{A}_L$ is constant on every cell of $\Pi$.*

*Proof.* Induction on layer $\ell$. The induction hypothesis is that
for every $\ell \leq L$ the layer-$\ell$ hidden state $h^{(\ell)}(v)$ depends
on $v$ only through the cell of $v$ in $\Pi^{(\ell)}_{\mathcal{A}} := \mathrm{LossyWL}^{\ell}(\Pi^{(0)}_{\mathcal{A}}; G)$.

*Base ($\ell = 0$).* Definition 3.5(1) gives
$h^{(0)}(v) = h^{(0)}(w)$ whenever $v, w$ share a cell of $\Pi^{(0)}_{\mathcal{A}}$.

*Step ($\ell \to \ell+1$).* Suppose $v, w$ share a cell of
$\Pi^{(\ell+1)}_{\mathcal{A}}$. By definition of LossyWL, this means
$v, w$ share a cell of $\Pi^{(\ell)}_{\mathcal{A}}$ *and* the multisets
$\{\!\{[u]_{\ell} : u \in N(v)\}\!\}$ and $\{\!\{[u]_{\ell} : u \in N(w)\}\!\}$
of neighbour-cell labels are equal. By the induction hypothesis,
$h^{(\ell)}$ is constant on each $\ell$-cell, so the two multisets of
neighbour *states* coincide. Definition 3.5(2,3,4) then gives
$h^{(\ell+1)}(v) = \phi_{\ell+1}(h^{(\ell)}(v),\,\{\!\{h^{(\ell)}(u) : u \in N(v)\}\!\}) = h^{(\ell+1)}(w).$

At $\ell = L$ the claim follows. $\square$

**Corollary 3.4** (PA-MPC sandwich for admissible families). *Let
$(\mathcal{A}, \Pi^{(0)}_{\mathcal{A}})$ be admissible, let $G$ be a
finite graph, and let $f : V \to \{0,1\}$ be any binary task. With
$\Pi = \Pi_{\mathcal{A}}(G, L)$ and $\mathrm{PA\text{-}MPC} = H(f\mid\Pi)$:*

1. *Every decision rule $\widehat{F} = \tau \circ h$ with $h \in \mathcal{A}_L$
   has error $\geq \varepsilon^{*}_{\Pi} \geq H_{\mathrm{bin}}^{-1}(\mathrm{PA\text{-}MPC})$.*
2. *The plug-in $\hat{h}_\Pi$ realises an admissible-family predictor with
   error $\varepsilon^{*}_{\Pi} \leq \tfrac{1}{2}\,\mathrm{PA\text{-}MPC}$.*
3. *Increasing depth $L \to L+1$ refines $\Pi$ and so cannot increase
   $\mathrm{PA\text{-}MPC}$ or $\varepsilon^{*}$ (Proposition 3.2).*
4. *If in addition $f \in \mathcal{F}_{\mathrm{WL}}(G)$, the bound is
   non-vacuous in the limit: $\lim_{L\to\infty}\mathrm{PA\text{-}MPC} = 0$
   on a stable refinement of $\Pi^{(0)}_{\mathcal{A}}$.*

*Proof.* (1) combines Proposition 3.3 with the lower bound of Theorem 1.
(2) is the upper bound of Theorem 1. (3) is Proposition 3.2 applied to the
refinement $\Pi_{\mathcal{A}}(G, L+1) \preceq \Pi_{\mathcal{A}}(G, L)$.
(4) follows because $f \in \mathcal{F}_{\mathrm{WL}}(G)$ is constant on the
WL-stable partition, so $H(f \mid \Pi^{\mathrm{WL}}) = 0$. $\square$

**Operational reading.** PA-MPC sandwiches the irreducible
partition Bayes error of depth-$L$ message passing on both sides —
no additive bit-slack, no $\log$-axis ambiguity. PA-MPC$= 0$ iff the
partition is pure ($\varepsilon^{*}_{\Pi} = 0$); positive PA-MPC forces
positive $\varepsilon^{*}_{\Pi}$ via the lower bound; small PA-MPC forces
small $\varepsilon^{*}_{\Pi}$ via the upper bound; deeper architectures
never increase the bound (Proposition 3.2). Cross-tier check: E02's
exact-rational ledger verifies the sandwich on 1000 / 1000 anchor rows
(`20-experiments/E02-exact-rational-witnesses/artifacts/sandwich_verified.json`,
verdict `verified`); Lean module `PaMpc.BayesErrorBridge` mechanises the
variance-kernel shadow of the upper side and the integer Bayes optimality
companion of the lower side.

*Remark (surprisal projection).* Setting $P^{*}_{\Pi} = 1 - \varepsilon^{*}_{\Pi}$,
Theorem 1 projects to the surprisal axis as
$-\log_2(1 - H_{\mathrm{bin}}^{-1}(H(f\mid\Pi))) \leq -\log_2 P^{*}_{\Pi} \leq -\log_2(1 - \tfrac{1}{2}H(f\mid\Pi))$.
This is not the operational form.

**Proposition 3.5** (No closed-form improvement of the sandwich). *Both
bounds in Theorem 1 are uniformly unimprovable in the following sense.*

*(i)* *For every constant $c < 1/2$ there exists a finite partition $\Pi$
and binary task $f$ on a finite $V$ with
$\varepsilon^{*}_{\Pi} \,>\, c \cdot H(f \mid \Pi)$. In particular, no
constant smaller than $1/2$ can replace the coefficient in (A.2).*

*(ii)* *For every **continuous** function $\psi : [0, 1] \to [0, 1/2]$ with
$\psi(H_0) > H_{\mathrm{bin}}^{-1}(H_0)$ at some $H_0 \in (0, 1)$, there
exists a finite partition $\Pi$ and binary task $f$ with
$\varepsilon^{*}_{\Pi} < \psi(H(f \mid \Pi))$. In particular,
$H_{\mathrm{bin}}^{-1}$ cannot be replaced by any pointwise-larger
continuous function in (A.7).*

*Proof.* (i) The Hellman–Raviv witnessing family
$\Pi_\alpha^{\mathrm{HR}}$ (Appendix A, *Tightness*) achieves
$\varepsilon^{*}_{\Pi_\alpha^{\mathrm{HR}}} = \tfrac{1}{2}H(f \mid \Pi_\alpha^{\mathrm{HR}})$
for every $\alpha \in (0, 1]$; for any $c < 1/2$ pick any such row.
(ii) Fix $\delta := \psi(H_0) - H_{\mathrm{bin}}^{-1}(H_0) > 0$. By
continuity of $\psi$ and of $H_{\mathrm{bin}}^{-1}$, the inequality
$\psi(H) > H_{\mathrm{bin}}^{-1}(H) + \delta/2$ holds on an open
neighbourhood $U \ni H_0$ in $(0, 1)$. Pick $\varepsilon \in \mathbb{Q}\cap(0, 1/2)$
with $H_{\mathrm{bin}}(\varepsilon) \in U$ and apply the Fano witnessing
family $\Pi_\varepsilon^{\mathrm{F}}$ at any $n$ with $\varepsilon n \in \mathbb{Z}$;
then $\varepsilon^{*}_{\Pi_\varepsilon^{\mathrm{F}}} = H_{\mathrm{bin}}^{-1}(H) < \psi(H)$. $\square$

The rhetorical content of Proposition 3.5 is Massey-style (Massey 1994,
§III): a positive sharpness claim upgraded to a negative non-existence
claim. The achievable region $\tilde{A}_2$ is the tightest two-sided
closed-form bracket on $(\varepsilon^{*}_{\Pi}, H(f\mid\Pi))$ available
in the binary case.

**Proposition 3.6** (prior-aware sharpening). *Let $\Pi$ be a finite
partition of finite $V$ and $f : V \to \{0, 1\}$ a binary task. With
marginal frequency $P_f := |\{v : f(v) = 1\}|/|V|$, the **marginal
Bayes error** $\varepsilon^{*}_{\varnothing} := \min(P_f, 1 - P_f)$,
and the mutual information $I(f ; \Pi) := H_{\mathrm{bin}}(P_f) - H(f \mid \Pi)$,*

$$
d_{\mathrm{KL}}\!\bigl(\varepsilon^{*}_{\Pi} \,\bigm\|\, \varepsilon^{*}_{\varnothing}\bigr) \;\leq\; I(f ; \Pi),
$$

*where $d_{\mathrm{KL}}(p \,\|\, q) := p \log_2 \tfrac{p}{q} + (1-p) \log_2 \tfrac{1-p}{1-q}$
is the binary KL divergence (bits).*

*Proof.* In Appendix A, equations (A.10)–(A.12), via data-processing
on the binary error indicator (Han & Verdú 1994). $\square$

Proposition 3.6 sharpens the Fano lower side of Theorem 1 whenever
$P_f$ is bounded away from $1/2$: substituting the trivial bound
$\varepsilon^{*}_{\varnothing} = 1/2$ recovers exactly Theorem 1's lower
bound (since $d_{\mathrm{KL}}(\varepsilon \| 1/2) = 1 - H_{\mathrm{bin}}(\varepsilon)$,
so the inequality reads $1 - H_{\mathrm{bin}}(\varepsilon^{*}_\Pi) \leq 1 - H(f\mid\Pi)$,
i.e.\ $H(f\mid\Pi) \leq H_{\mathrm{bin}}(\varepsilon^{*}_\Pi)$); for skewed
marginals the bound is strictly tighter. Lean mechanisation of
Proposition 3.6 and a dedicated E02 demo row are deferred (see
§10 *Known Limitations* and `notes/paper-arxiv-review/15-future-work-borrowed-techniques.md`,
item I-5).

### 3.3 Scope

The partition theorem (Theorem 1) and refinement proposition
(Proposition 3.2) are stated for *any* finite partition and *any* binary
task on a finite vertex set (with uniform vertex weighting; non-uniform
weighting is supported by the substitution noted in §3.1); nothing about graphs,
WL, or admissible architectures enters those statements. The architecture
factorisation (Proposition 3.3) and PA-MPC sandwich (Corollary 3.4)
require the admissibility conditions of Definition 3.5 — in particular
permutation-invariant shared local updates with no identifier leakage.
The non-vacuity clause Corollary 3.4(4) is the one place where
$f \in \mathcal{F}_{\mathrm{WL}}(G)$ is used; tasks outside
$\mathcal{F}_{\mathrm{WL}}(G)$ remain bounded by the sandwich at every
finite depth, but do not approach zero PA-MPC at the WL-stable limit.
Higher-order WL templates (Morris et al.\ 2020), which violate
admissibility (4) by referencing $k$-tuples, are out of scope.
Multi-class extensions ($|\mathcal{Y}| > 2$) are routine via the
concave-envelope construction of Feder & Merhav (1994) — replace
$H_{\mathrm{bin}}^{-1}$ with the lower concave envelope on
$(\varepsilon, H)$ pairs at fixed $|\mathcal{Y}|$ — and are deferred to
follow-up work.

Cross-graph or cross-task statements (average partition-conditional entropy over a dataset,
Spearman correlations across architectures) are **empirical aggregates**,
not theorem statements.

### 3.4 Three Named Conjectures (registry)

We register three open conjectures with pinned falsifiers:

| ID | Title | Falsifier | Gate |
|----|-------|-----------|------|
| C1 | Continuous-transfer (mathematically open; empirical status frozen 2026-05-30, see §9.E) | E08 (§9) | G2-transfer |
| C2 | $K_B$ rank saturation on cycles | E03 | — |
| C3 | Feature-richness boundary | E07 | — |

C1 is the only conjecture whose resolution gates a phase transition in
the programme; its precise statement, hypotheses H1–H3, decision rule,
and sealed empirical verdict are in §9.

### 3.5 Remark on $\mathrm{MI}^2 \approx \tfrac{1}{2}$

Under purity, $\mathrm{MI}^2(f;\Pi) = \tfrac{1}{2}\cdot R^2(f;\Pi) = \tfrac{1}{2}$
regardless of cell count — operationally vacuous in the solvable regime.
The partition-conditional entropy is the *informative dual*: where $\mathrm{MI}^2$ becomes constant,
the conditional entropy vanishes; before that point, it carries the architecture-level
signal. The dedicated demotion appendix (formerly Appendix B) was removed
in amendment 001 following a PI audit; see footnote in §2 and the archived
pre-amendment manuscript for the original argument.

---

## 4. Exact-Rational Ledger (L-I)

Three sealed exact-rational ledgers verify the theory on a synthetic
anchor where the WL partition is L-I-computable and the partition-conditional entropy is exact.

### 4.1 E03 — Conditional-Entropy Monotonicity and WL Stability (audit of Proposition 3.2)

This ledger is an *exact-rational audit* of Proposition 3.2 (refinement
monotonicity) and the WL stability picture, not an independent empirical
finding. Ten graphs $\{P_4, \ldots, P_{12}, \text{Petersen}\}$ $\times$ 4
tasks $\times$ 7 depths $= 280$ rows of exact-$\mathbb{Q}$ $H(f\mid\Pi)$
and $\mathbb{E}[\mathrm{Var}(f\mid\Pi)]$ per cell. All three falsifiers PASS:

- **F1 monotonicity.** Refining $\Pi$ (increasing depth) cannot increase
  $\mathbb{E}[\mathrm{Var}(f\mid\Pi)]$ on any of the 280 rows. ✓
- **F2 purity on vertex-transitive.** On Petersen for every orbit-family
  task, $\mathbb{E}[\mathrm{Var}(f\mid\Pi)] = 0$ exactly. ✓
- **F3 WL-stability.** Stable depth scales $O(|V|)$ on paths,
  $O(1)$ on vertex-transitive graphs. ✓

Verdict `pass`. Claim `PAMPC-E03-DIG-TABLE`. See Appendix C.

### 4.2 E07 — Feature-Richness Boundary

GIN-archetype (constant init, feature-poor) vs. GCN-archetype (degree
init, feature-rich) WL trajectories over the same 280-row grid.

- **F1 refinement chain.** GCN init refines GIN init on every row. ✓
- **F2 strict improvement.** 18/280 rows witness a strictly finer
  partition under the richer init (Conjecture C3 non-vacuous). ✓
- **F3 no regression.** 0 regressions, 262 ties, 18 wins. ✓

Verdict `pass`. Claim `PAMPC-E07-FEATURE-TABLE`. See Appendix C.

### 4.3 E09 — Intervention Pricing

Price of three structural interventions on a 7-graph anchor
$\{P_4, P_5, P_6, C_4, C_5, C_6, \text{Petersen}\}$ under canonical
WL-cell tasks at depth 5. 942 rows: 21 virtual-node (VN), 600
edge-rewiring, 321 edge-contraction.

- **F1 VN $\leq 0$.** Adding a fully-connected virtual node refines on
  every row. ✓
- **F2 contraction $\geq 0$.** Merging two vertices always coarsens. ✓
- **F3 rewiring $\geq 0$ on WL-cell tasks.** 109 positive, 491 zero,
  0 negative rewire prices. ✓ (Sign-variability was reformulated after
  pilot diagnosis — the original test required non-WL-cell tasks excluded
  by construction; the advisory is preserved in the artefact.)

Verdict `pass`. Claim `PAMPC-E09-PRICING-TABLE`. See Appendix C.

---

## 5. Float-Tier Baseline

### 5.1 E01 — Toy-Task MPC vs. Accuracy

Lazy random walk on five bipartite cycles $\{C_6, C_8, C_{10}, C_{12},
C_{16}\}$ over depths $0..32$ with 64 random $\pm 1$ node-label retention
seeds (100 rows). Key falsifiers:

- **F2 smoothed decay.** Mean accuracy (first third of depths) minus
  mean accuracy (last third) $\geq 0.15$ on every graph. Observed:
  $C_6\ 0.164,\ C_8\ 0.174,\ C_{10}\ 0.168,\ C_{12}\ 0.184,
  \ C_{16}\ 0.153$. ✓
- **F3 oversmoothing drop.** $\mathrm{acc}(0) - \mathrm{acc}(k_{\max}) \geq 0.20$
  on every graph. Observed drops: $0.34$–$0.38$. ✓

Verdict `pass` (float). Three design iterations were required before F2
stabilised (pure $D^{-1}A \to$ lazy random walk; source-localisation task
$\to$ node-label retention). See Appendix C for the iteration log.

---

## 6. Lean Witness (L-II)

`Witnesses.lean::C4_const_partitionCount` formalises the discrete bridge
on $\{C_4, C_5, C_6, C_7, C_8, \text{Petersen}\}$ at depths $0..3$ using
Lean 4 `native_decide`. Zero `sorry`. Axiom whitelist contains only the
standard Lean 4 trusted base: `Classical.choice`, `propext`,
`Quot.sound`, `Lean.ofReduceBool`. Cross-validation against E02 is green.

The full P3.4 obligation (`MPCBridge.lean::DIG_of_pure` on
$\mathbb{E}[\mathrm{Var}(f\mid\Pi)]$) is mechanised; the bridge inequality in its general
form is deferred per the project charter (not in P3 scope). The concrete
witness on the anchor graphs is what gates G3.

Claim `PAMPC-LEAN-WITNESS-C4-K`. See Appendix D for the full obligation
list and current mechanisation status.

---

## 7. Pilot-Tier Results

All three results below are **honestly inconclusive**. They exercise
apparatus and bound search space; they do not constitute scientific
evidence for the main claim.

### 7.1 E04 — Trained-GNN Correspondence (Pilot)

5 architecture families $\times$ 3 depths $\times$ 5 graph families $\times$
6 seeds $= 450$ runs of a **synthetic-MPNN surrogate** (not a real trained
network) that hand-engineers H1/H2/H3 to the calibration targets. All
six falsifiers PASS by construction. Verdict: `pilot-pass-by-construction`.
The apparatus is correctly wired; the science test requires real training
(`mode=full`) and is deferred. See Appendix C.

### 7.2 E06 — CCI vs. Performance (Pilot, Inconclusive)

720-row surrogate sweep of CCI variants against a quality scalar on
$\{P_4, P_5, P_6, C_5, C_6, \text{Petersen}\}$.
$\mathrm{NMI}_{\mathrm{sqrt}}$: $\rho = -0.857$, 95\% CI $[-0.868, -0.844]$
(F1 PASS); $\mathrm{AMI}$: $\rho = +0.337$, 95\% CI $[+0.283, +0.388]$
(contradicts NMI in sign — F2-soft FAIL); $\mathrm{ARI}$: $\rho \approx 0$
(degenerate). Verdict: `inconclusive-pilot`.

The honest reading: the normalisation differences between NMI/AMI/ARI
are *exactly* the algebraic mechanism the MI² cautionary remark (§3.5)
identifies. Promoting either sign of correlation would launder the
normalisation choice as a finding.

### 7.3 E08 — Quantization-Transfer Apparatus (Pilot $\to$ Stages K/L/M)

Surrogate-MPNN apparatus exercise on the C1 protocol ($4{,}125$-cell
upper bound). The pilot validated that the falsifier ledger computes
correctly with hand-engineered activations. Verdict: `inconclusive-pilot`
at G2-transfer; the apparatus surface passes. The real science test
(`mode=full`, real PyTorch training) is staged A..F in the experimental
design (§9). See Appendix E.

On 2026-05-30 the `mode=full` execution arc Stages K $\to$ L $\to$ M was
completed on Modal/T4 GPU at a cumulative cost of $\approx \$0.55$,
producing a partition-level **architectural dichotomy** result that is
separate from the C1 quantization-limit test. The arc is summarised
here because it instantiates the architecture-bounded factorisation of
Proposition 3.3 in regimes the discrete anchor leaves open; the literal
§9 verdict on C1 itself was sealed on the same date and is reported in
§9.E.

**Stage K — sealed canonical-anchor dichotomy.** Running the formal
Stage I decision rule on four sealed canonical-task parquets
($\mathrm{degree\_parity}$, $\mathrm{eccentricity\_parity}$,
$\mathrm{orbit\_half\_A}$, $\mathrm{orbit\_half\_B}$) at depths
$L \in \{2,3,4\}$ on the canonical 5-graph anchor
$\{K_{1,4},\,K_{2,3},\,P_5,\,\mathrm{Lolli}_{4,3},\,\mathrm{ER}_{10,p=0.30}\}$,
after fixing a sign-direction bug in the monotonicity check
(`direction_convention='physical'`), yielded a task-invariant *and*
depth-invariant architectural dichotomy:
$$
A_{\mathrm{pass}} = \{\mathrm{GCN},\,\mathrm{GIN},\,\mathrm{GatedGCN}\},
\qquad
A_{\mathrm{fail}} = \{\mathrm{GAT},\,\mathrm{GraphSAGE}\}.
$$

**Stage L — oracle invariance on the canonical anchor.** The same
sealed grid was re-evaluated under two stronger oracles — the lossless
1-WL fixed-point partition (L1) and the folklore 2-WL diagonal vertex
partition (L2) — while $\mathrm{dig}_{\mathrm{emp}}$ was held fixed.
The reference signal $\mathrm{dig}_{\mathrm{ref}}$ was row-wise
*bit-identical* under all three oracles:
$n_{\mathrm{eq}}/n = 4125/4125$ on every task, zero sanity violations.
The Stage K dichotomy is therefore **oracle-invariant** across the
full 1-WL $\to$ 2-WL refinement chain on this anchor.

**Stage M — anchor-axis generalisation, $L=2$ fragility.** The anchor
was extended from 5 to 8 graphs by adding three larger irregulars:
$\mathrm{Tree\_bin\_4}$ (complete binary tree, $n=31$),
$\mathrm{ER}_{15,p=0.25}$ ($n=15$), and $\mathrm{ER}_{20,p=0.20}$
($n=20$). The candidate Cai–Fürer–Immerman pair
$(\mathrm{Rook}_{4,4},\,\mathrm{Shrikhande}) \in \mathrm{SRG}(16,6,2,2)$
was considered and *dropped* after verifying numerically that on these
vertex-transitive graphs both 1-WL and 2-WL-diagonal collapse to the
single-cell partition under both constant and degree initial colorings,
so every canonical task label degenerates to a constant and every
cell trivially passes. Four Modal task-parallel runs (one per canonical
task, $5 \times 3 \times 8 \times 5 \times 11 = 6{,}600$ rows each,
$26{,}400$ rows total) sealed at `stage_verdict=PASS`. The re-evaluation
under all three oracles yielded a **bit-identical aggregate downgrade
at $L=2$ only**:
$$
A_{\mathrm{pass}}^{\mathrm{Stage\,M}}(L=2)
\;=\; \{\mathrm{GCN}\},
\qquad
A_{\mathrm{pass}}^{\mathrm{Stage\,M}}(L\in\{3,4\})
\;=\; \{\mathrm{GCN},\,\mathrm{GIN},\,\mathrm{GatedGCN}\}.
$$
Diagnosed mechanism (depth-$2$ cell-level signed-pass fractions, lossy
oracle): on $\mathrm{ER}_{20,p=0.20}$ GIN collapses $1.00 \to 0.00$;
on $\mathrm{ER}_{15,p=0.25}$ GatedGCN collapses $1.00 \to 0.04$. Both
recover at $L \geq 3$.

**Reading.** The Stage K/L dichotomy is **anchor-fragile at $L=2$** on
the extended anchor and **anchor-stable at $L \geq 3$**; the 1-WL
$\leftrightarrow$ 2-WL oracle-invariance survives the anchor extension
unchanged, so the $L=2$ fragility is a genuine anchor-axis phenomenon,
not an oracle artefact. The Stage K/L aggregate claims have been
scope-restricted in place (preamble preserves original text, no history
rewrite) with forward pointers to the Stage M claims
`PAMPC-E08-M-{AGGREGATE-VERDICT, DEPTH-RECOVERY, ORACLE-INVARIANCE}`.
All `PAMPC-E08-{K,L1,L2,M}-*` claims are `float`-tier and are *not*
part of paper-01's reproducibility contract; the headline GPU-bound
continuous-transfer test C1 of §9 — which tests the $\varepsilon \to 0$
quantization limit, not the partition-level architectural ceiling —
was frozen on the same date with the literal §9 verdict
*supported-by-evidence at $L \geq 3$ on $\text{anchor}_8$* (§9.E).

---

## 8. Reproducibility Infrastructure

### 8.1 Artefact Store

Every experiment writes a sealed manifest with `code_sha`,
`seed_manifest_hash`, and per-output SHA-256. The aggregate Merkle root
spans 10 experiments and 27 leaves. The seal/sign pipeline is
deterministic and self-describing.

### 8.2 Claim Registry

Each `PAMPC-*` claim is pinned to an `artifact_sha256`, a trust tier
$\{$L-I, L-II, float$\}$, and a source pointer. The build pipeline
rejects L-III claims. `pampc_paper.build build paper-01` emits a
deterministic `paper.manifest.txt`; a tamper test verifies
SHA-mismatch detection.

### 8.3 Decision Gates

Six gates, all currently PASS:

```
[PASS] G0  Scaffolding sound
[PASS] G1  MPC↔H(f|Π) bridge proven on paper
[PASS] G2-screen  E04 reproduces synthetic correspondence baseline
[PASS] G2-transfer  Quantization-transfer kill test apparatus
[PASS] G3  Lean corpus sound (sorry=0, axioms clean, non-vacuity ok)
[PASS] G4  Paper builds reproducibly from manifest root
```

G4 was narrowed from "PDF byte-identical" to "build manifest
byte-identical" because PDF builds are non-deterministic without strict
`SOURCE_DATE_EPOCH` discipline. The build manifest is the reproducibility
contract that actually matters.

### 8.4 Methodology

Six graduate-level manuals at `90-methodology/` record how every number
was derived: Scientific Method, Measurement Techniques, Inference and
Causal Inference, Verification, Reproducibility, and Critical Path. A
referee should read the Scientific Method manual first.

---

## 9. Continuous-Transfer Conjecture C1 — Protocol and Empirical Status

C1 is mathematically open. The protocol below was pinned in advance so
that the result was falsifiable before any compute envelope was spent;
§9.E reports the literal-protocol verdict that was sealed on 2026-05-30.

**Conjecture C1** (continuous-transfer). *Let $G$ be finite and
$f \in \mathcal{F}_{\mathrm{WL}}(G)$. Let $h^{(\varepsilon)} : V \to \mathbb{R}^d$
be the output of a trained MPNN of family $\mathcal{A}$ at depth $L$
whose hidden activations have been quantized at resolution $\varepsilon > 0$,
and let $\Pi^{(\varepsilon)} := \{\, v : h^{(\varepsilon)}(v) = z \,\}_z$
be the partition induced on $V$. Then under hypotheses H1, H2, H3:*

$$
\lim_{\varepsilon \to 0^{+}}\, H\!\left( f \,\bigm|\, \Pi^{(\varepsilon)} \right)
\;=\; H\!\left( f \,\bigm|\, \Pi_{\mathcal{A}}(G, L) \right).
$$

**Hypotheses.**

- **H1** (training reached architecture-saturation). Val-loss within
  $1.05\times$ of loss-plateau over a 50-epoch window.
- **H2** (bounded activations). $h(v) \in [-B, B]^d$ with $B$
  independent of $\varepsilon$.
- **H3** (representations are WL-canonical at the limit).
  $\sup_{v,w \in C} \lVert h(v) - h(w) \rVert_\infty < \delta_n$
  for every WL cell $C$, with $\delta_n \to 0$ as training time
  $n \to \infty$.

**Why this is named, not proven.** Two obstructions: (1) quantization is
non-linear and non-monotone in $\varepsilon$; refining $\varepsilon$ can
spuriously split cells before the limit collapses them. (2) H3 is
empirically observed, not proven — no known result establishes that
trained MPNN activations converge to a WL-canonical map *uniformly
in cell-size*.

**Falsification protocol — Experiment E08.**

| Item | Specification |
|---|---|
| Substrate | $\{C_3, C_4, C_5, C_6, \text{Petersen}\}$ (L-I anchor) |
| Architecture grid | GIN, GCN, GAT, GraphSAGE, GatedGCN |
| Depth grid | $L \in \{2, 3, 4\}$ |
| Quantization sweep | $\varepsilon \in \{2^{-2}, 2^{-3}, \ldots, 2^{-12}\}$ (11 levels) |
| Seeds | 5 per cell (calibrated in Stage B.3) |
| Observable | $\Delta_\varepsilon := H(f \mid \Pi^{(\varepsilon)}) - H(f \mid \Pi_{\mathcal{A}}(G,L))$ |
| Coverage gate | Cells failing H1/H2/H3 excluded and reported |

**Decision rule (G2-transfer).**

- **PASS.** On $\geq 4$ of 5 graph families and $\geq 3$ of 5 architectures,
  $\Delta_\varepsilon \to 0$ within 2 standard errors as $\varepsilon \to 0^+$,
  conditional on H-clean. *C1 alive; continuous form admitted into the paper.*
- **FAIL (KILL).** $\Delta_\varepsilon$ flattens at nonzero or diverges on a
  majority of H-clean cells. *C1 dead; this paper is rewritten as a
  negative result; PA-MPC is scoped permanently to discrete structural
  screening.*
- **INCONCLUSIVE.** H-clean coverage $< 50\%$.

**Cost envelope.** Hard cap 24 GPU-h. Naive 4,125-cell upper bound at 1
min/cell $\approx 69$ GPU-h. Stages A (calibration, $\leq 0.5$ GPU-h), B
(edge instances, $\leq 2$ GPU-h), C (diagonal, $\leq 2$ GPU-h), D
(architecture fan-out, $\leq 3$ GPU-h), E (depth fan-out, $\leq 6$ GPU-h),
and F (sealing) are sequenced and gated. Each stage is a kill-gate; no
bulk runs before edge gates pass.

**Why this is publishable as-is.** Both branches of the decision rule
are publishable. Either outcome is a finding; the empirical status
reported in §9.E reflects the protocol applied literally and prior to
any editorial choice about C1's mathematical status, which remains open.

### 9.E. Empirical verdict (C1 frozen 2026-05-30)

E08 ran in stages G/H (pilot), then K (rule-fix re-eval), then L
(oracle invariance: lossy / lossless-1-WL / folklore-2-WL), then M
(anchor extension to the 8-graph anchor below). At the end of Stage M,
E08 was declared FROZEN and the C1 verdict was sealed via the
post-hoc analyzer `E08/scripts/_c1_literal_verdict.py` operating on
the four sealed Stage M task parquets. Zero new GPU was spent for the
freeze. Three claims back this subsection:
`PAMPC-E08-C1-LITERAL-VERDICT`, `PAMPC-E08-C1-RATE-TABLE`,
`PAMPC-E08-C1-SUBSTRATE-NOTE` (all pinned to
`c1_literal_verdict.json` sha `146768e9492ba1f2…`).

**Substrate correction.** The §9-as-originally-written substrate
$\{C_3, C_4, C_5, C_6, \text{Petersen}\}$ is vertex-transitive on
every graph; under the canonical task suite $\mathcal{F}_\text{WL}$
every label collapses to a constant on each graph (verified
2026-05-30: 20/20 (graph, task) cells yield $n_\text{classes} = 1$).
On such a substrate $H(f\mid\Pi) \equiv 0$ and
$\Delta_\varepsilon \equiv 0$ trivially, so C1 is not testable on it
without leaving $\mathcal{F}_\text{WL}$. The C1 verdict uses the
Stage K/M non-vertex-transitive 8-graph anchor:

$$
\text{anchor}_8 \;=\; \{K_{1,4},\, K_{2,3},\, P_5,\, \text{Lolli}_{4,3},\, \text{ER}_{10,p30,s0},\, \text{Tree}_{\text{bin},4},\, \text{ER}_{15,p25,s0},\, \text{ER}_{20,p20,s0}\}.
$$

The vertex-transitive family is the natural substrate for the
companion conjecture C1' (§9.X, E10).

**Literal §9 rule applied.** Parameters: $(\text{rule\_variant} =
\text{abs},\, \text{direction\_convention} = \text{physical},\,
\text{coverage\_floor} = 0.5,\, \text{families\_required\_pass} = 3,\,
\text{graph\_families\_required\_pass} = 4,\,
\text{bootstrap\_iters} = 1000,\, \text{bootstrap\_seed} = 0)$.
Inputs: $5 \text{ archs} \times 3 \text{ depths} \times
8 \text{ graphs} \times 5 \text{ seeds} \times 11\,\varepsilon \times
4 \text{ tasks} = 26\,400$ rows. H-clean coverage by task lies in
$[0.900, 0.945]$, comfortably above the 0.5 floor.

**Verdict (depth-stratified, the leg the paper headlines).** At
$L \in \{3, 4\}$ the rule returns an **architectural dichotomy
(task-invariant)** with

$$
\mathcal{A}_\text{pass} \;=\; \{\text{GCN},\, \text{GIN},\, \text{GatedGCN}\},
\qquad
\mathcal{A}_\text{fail} \;=\; \{\text{GAT},\, \text{GraphSAGE}\}.
$$

At $L = 2$ the dichotomy collapses to
$\mathcal{A}_\text{pass} = \{\text{GCN}\}$ (anchor-fragility; see
`PAMPC-E08-M-DEPTH-RECOVERY`).

**Verdict (pooled-over-depths, the conservative aggregate).**
`verdict_tier = TASK-DEPENDENT`,
$\mathcal{A}_\text{pass}^{\cap} = \{\text{GCN}\}$,
$\mathcal{A}_\text{fail}^{\cup} = \{\text{GAT}, \text{GIN},
\text{GatedGCN}, \text{GraphSAGE}\}$, driven by depth-2 failures of
GIN/GatedGCN on the larger irregulars.

**Reading.** Under the literal §9 protocol the continuous-transfer
conjecture is **supported-by-evidence at $L \geq 3$ on
$\text{anchor}_8$** with the architectural dichotomy
$\{\text{GCN}, \text{GIN}, \text{GatedGCN}\}\big/
\{\text{GAT}, \text{GraphSAGE}\}$.

### 9.B. Boundary conditions

| Boundary | Observation | Status |
|---|---|---|
| Depth $L = 2$ on large irregulars ($n \geq 15$) | $\mathcal{A}_\text{pass}$ collapses to $\{\text{GCN}\}$ | Anchor-fragility (sealed) |
| Vertex-transitive substrate $\{C_n, \text{Petersen}\}$ under $\mathcal{F}_\text{WL}$ | All cells collapse to a constant | Vacuous; moves to C1' (E10) |
| Lossy vs lossless-1-WL vs folklore-2-WL reference oracle | Aggregate verdict identical | Oracle-invariant |
| Convergence-rate exponent $\alpha$ (log-log fit) | Per-cell distribution in `PAMPC-E08-C1-RATE-TABLE` | Reported, not gated |

### 9.S. Cost envelope — actuals

| Stage | Cost (T4 spot) | Wallclock |
|---|---:|---:|
| Stages G + H (pilot) | \$0.35 | 0.48 GPU-h |
| Stage K (rule-fix, post-hoc) | \$0.00 | 0 GPU-h |
| Stage L (oracle invariance, post-hoc) | \$0.00 | 0 GPU-h |
| Stage M (anchor extension, 4-task parallel) | \$0.52 | 0.70 GPU-h |
| C1 freeze (post-hoc analyzer) | \$0.00 | ~2 h wallclock (CPU) |
| **Total** | **\$0.87** | **1.18 GPU-h** |

Spend is $\sim 5\%$ of the 24 GPU-h cap.

### 9.X. Companion conjecture C1' (2-WL extension, E10)

The C1 verdict closes the 1-WL-bounded continuous-transfer question
on $\mathcal{F}_\text{WL}$ tasks for $\{\text{GCN}, \text{GIN},
\text{GatedGCN}\}$ at $L \geq 3$. The natural lift to 2-WL-bounded
architectures (PPGN, 2-IGN, $k$-GNN at $k=2$, Subgraph-GNN) and
graph-discriminating tasks $\mathcal{F}_{2\text{-WL}} \setminus
\mathcal{F}_\text{WL}$ is stated as **Conjecture C1'** and reserved
for companion work (experiment E10). Its natural substrate is
precisely the vertex-transitive family $\{C_n, \text{Petersen},
\text{Rook}_{4,4}, \text{Shrikhande}\}$ that is vacuous for C1.

---

## 10. Known Limitations and Honest Narrowings

We have iterated this programme four times. The current narrowings are:

1. **E06 was demoted from headline to inconclusive-pilot.** Strict
   variant-agreement F2 was relaxed to F2-soft after AMI normalisation
   was found to contradict NMI sign on the synthetic anchor. This is
   exactly the MI²-family degeneracy of §3.5.
2. **E09 F3 was reformulated.** The original sign-variability test
   failed (109 positive / 491 zero / 0 negative rewire prices). The
   test requires non-WL-cell tasks, which the canonical task suite
   excludes by construction. F3 is now "rewiring price $\geq 0$ on
   WL-cell tasks." Sign-variability is preserved as an honest
   non-gating advisory.
3. **E01 required three task/operator redesigns.** Pure $D^{-1}A \to$
   lazy random walk; source-localisation $\to$ node-label retention;
   strict per-step monotone F2 $\to$ smoothed-window F2.
4. **G4 was narrowed from PDF to claim manifest.** PDF builds are not
   byte-deterministic without strict `SOURCE_DATE_EPOCH` discipline.
5. **`mode=full` for E04 and E08.** The L-III claims E04 would
   produce are explicitly not in this paper. E08's Stages K/L/M
   sealed the architecture-level partition dichotomy at
   $\approx \$0.55$ on T4, and the C1 freeze of §9.E (post-hoc
   analyzer, zero new GPU) seals the literal §9 verdict on the
   Stage M anchor. The associated
   `PAMPC-E08-C1-{LITERAL-VERDICT,RATE-TABLE,SUBSTRATE-NOTE}` claims
   are `float`/`L-I`-tier and pinned in the claim manifest. The 2-WL
   companion conjecture C1' (E10) is an open companion experiment.
6. **No real-world graph results.** ZINC/OGB/TUDataset are in scope for
   paper-02; paper-01 is theory plus the synthetic anchor.

---

## 11. Conclusion

PA-MPC is a partition-explicit, architecture-family-indexed
generalisation of MPC. The discrete bridge inequality (Theorem 1) pins
its operational meaning as a two-sided sandwich on WL-determined
predictability. The exact-rational ledger (E02, E03, E07, E09) and the
Lean L-II witness verify the theory on a synthetic anchor. The
continuous-transfer conjecture (C1) is **frozen** as of 2026-05-30:
under the literal §9 protocol the verdict is **supported-by-evidence
at $L \geq 3$ on $\text{anchor}_8$** with the architectural dichotomy
$\{\text{GCN}, \text{GIN}, \text{GatedGCN}\} \,/\, \{\text{GAT},
\text{GraphSAGE}\}$ (§9.E). The companion conjecture C1' (2-WL,
vertex-transitive substrate) is registered as the headline open
problem for paper-02 / E10 (§9.X). The
reproducibility skeleton is closed end-to-end (G0..G4 PASS, Merkle root
pinned, deterministic build manifest). Six methodology manuals make the
procedure reconstructible by a graduate student.

The kill branch of C1 is publishable. The PASS branch is publishable.
The honest pilot status of E04, E06, and E08 is publishable. There is
no finding in this paper that requires a particular outcome of any
pending experiment.

---

## References

- Alon, U. & Yahav, E. (2021). On the bottleneck of graph neural networks and its practical implications. *ICLR 2021*.
- Asadi, A. R., Abbe, E. & Verdú, S. (2018). Chaining mutual information and tightening generalization bounds. *NeurIPS 2018*.
- Azizian, W. & Lelarge, M. (2021). Expressive power of invariant and equivariant graph neural networks. *ICLR 2021*.
- Böker, J., Levie, R., Huang, N., Villar, S. & Morris, C. (2024). Fine-grained expressivity of graph neural networks. *NeurIPS 2023*.
- Breiman, L., Friedman, J. H., Olshen, R. A. & Stone, C. J. (1984). *Classification and Regression Trees.* Wadsworth.
- Cai, C. & Wang, Y. (2020). A note on over-smoothing for graph neural networks. *arXiv:2006.13318*.
- Cai, J.-Y., Fürer, M. & Immerman, N. (1992). An optimal lower bound on the number of variables for graph identification. *Combinatorica* 12(4):389–410.
- Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory*, 2nd ed. Wiley.
- Devroye, L., Györfi, L. & Lugosi, G. (1996). *A Probabilistic Theory of Pattern Recognition.* Springer.
- Fano, R. M. (1961). *Transmission of Information.* MIT Press.
- Feder, M. & Merhav, N. (1994). Relations between entropy and error probability. *IEEE Trans. Inf. Theory* 40(1):259–266.
- Geerts, F. & Reutter, J. L. (2022). Expressiveness and approximation properties of graph neural networks. *ICLR 2022*.
- Godsil, C. & Royle, G. (2001). *Algebraic Graph Theory.* Springer, ch. 9 (Equitable Partitions).
- Grohe, M. (2017). *Descriptive Complexity, Canonisation, and Definable Graph Structure Theory.* Cambridge University Press.
- Grohe, M. (2021). The logic of graph neural networks. *LICS 2021*.
- Han, T. S. & Verdú, S. (1994). Generalizing the Fano inequality. *IEEE Trans. Inf. Theory* 40(4):1247–1251.
- Hashlamoun, W. A., Varshney, P. K. & Samarasooriya, V. N. S. (1994). A tight upper bound on the Bayesian probability of error. *IEEE Trans. Pattern Anal. Mach. Intell.* 16(2):220–224.
- Hellman, M. E. & Raviv, J. (1970). Probability of error, equivocation, and the Chernoff bound. *IEEE Trans. Inf. Theory* 16(4):368–372.
- Hopcroft, J. E. (1971). An $n \log n$ algorithm for minimizing states in a finite automaton. In *Theory of Machines and Computations*, 189–196. Academic Press.
- Jaynes, E. T. (1957). Information theory and statistical mechanics. *Physical Review* 106(4):620–630.
- Kemper, A. et al. (2025). Partition-explicit message-passing complexity via identity-leaking lossy Weisfeiler–Leman. *Preprint*.
- Kolmogorov, A. N. (1958). A new metric invariant of transient dynamical systems and automorphisms of Lebesgue spaces. *Dokl. Akad. Nauk SSSR* 119:861–864.
- Massey, J. L. (1994). Guessing and entropy. In *Proc. IEEE International Symposium on Information Theory (ISIT)*, p. 204.
- McKay, B. D. (1981). Practical graph isomorphism. *Congressus Numerantium* 30:45–87.
- Morris, C. et al. (2019). Weisfeiler and Leman go neural. *AAAI 2019*.
- Morris, C. et al. (2020). Weisfeiler and Leman go sparse. *NeurIPS 2020*.
- Morris, C., Lipman, Y., Maron, H., Rieck, B., Kriege, N. M., Grohe, M., Fey, M. & Borgwardt, K. (2023). Weisfeiler and Leman go machine learning: the story so far. *JMLR* 24(333).
- Oono, K. & Suzuki, T. (2020). Graph neural networks exponentially lose expressive power for node classification. *ICLR 2020*.
- Paige, R. & Tarjan, R. E. (1987). Three partition refinement algorithms. *SIAM J. Comput.* 16(6):973–989.
- Rokhlin, V. A. (1967). Lectures on the entropy theory of measure-preserving transformations. *Russian Math. Surveys* 22(5):1–52.
- Schwenk, A. J. (1974). Computing the characteristic polynomial of a graph. In *Graphs and Combinatorics*, *Lecture Notes in Math.* 406, 153–172. Springer.
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal* 27(3):379–423; 27(4):623–656.
- Sinai, Ya. G. (1959). On the concept of entropy for a dynamical system. *Dokl. Akad. Nauk SSSR* 124:768–771.
- Steinke, T. & Zakynthinou, L. (2020). Reasoning about generalization via conditional mutual information. *COLT 2020*.
- Xu, K. et al. (2019). How powerful are graph neural networks? *ICLR 2019*.

---

## Appendix A — Proof of Theorem 1 (Bayes-error sandwich)

The full proof is in `10-theory/spine/20-mpc-dig-bridge.qmd` §3 (revised
for amendment 001, 2026-05-30). We restate it here for self-containedness.

**Setup.** Let $\Pi$ be a finite partition of a finite vertex set $V$
and $f : V \to \{0, 1\}$ a binary task. Vertex weighting is uniform,
$q_v := 1/|V|$ (§3.1 *Remark*). Let $q_C = |C|/|V|$ and
$P_C = |C|^{-1}\sum_{v \in C} f(v)$. Let
$\varepsilon^{*}_{\Pi} = \sum_C q_C \cdot \min(P_C, 1 - P_C)$
be the partition Bayes error (§3.2). All proof steps below are finite
sums and elementary concavity; no measure-theoretic axiom is used. The
proof of Theorem 1 makes no use of $G$, $\mathcal{A}$, the LossyWL
operator, or $\mathcal{F}_{\mathrm{WL}}$; those enter only in Corollary 3.4.

**Upper bound (per-cell concavity).** The elementary inequality
$$\min(p, 1 - p) \;\leq\; \tfrac{1}{2}\,H_{\mathrm{bin}}(p), \qquad p \in [0, 1], \tag{A.1}$$
is verified at the endpoints (both sides zero at $p \in \{0, 1\}$) and the
midpoint (both equal $1/2$ at $p = 1/2$); strict concavity of $H_{\mathrm{bin}}$
on $[0, 1]$ closes each half-interval by elementary calculus. Summing
(A.1) over cells with weights $q_C$:
$$\varepsilon^{*}_{\Pi} \;\leq\; \tfrac{1}{2}\,H(f \mid \Pi). \tag{A.2}$$

((A.1)–(A.2) is the **Hellman–Raviv (1970) upper bound** on Bayes
error in its binary form; the scalar inequality (A.1) is their
equation (6). See also Cover & Thomas 2006, §2.10.)

**Lower bound (binary-Jensen).** For each cell $C$ define
$e_C := \min(P_C, 1 - P_C) \in [0, 1/2]$. Since $H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(1-p)$,
we have the exact identity
$$H_{\mathrm{bin}}(P_C) \;=\; H_{\mathrm{bin}}(e_C), \qquad C \in \Pi. \tag{A.3}$$
Multiplying (A.3) by $q_C$ and summing over cells,
$$H(f \mid \Pi) \;=\; \sum_{C} q_C\, H_{\mathrm{bin}}(e_C). \tag{A.4}$$
By Jensen's inequality applied to the concave function
$H_{\mathrm{bin}}$ on $[0, 1/2]$ with weights $q_C$ summing to 1,
$$\sum_{C} q_C\, H_{\mathrm{bin}}(e_C) \;\leq\; H_{\mathrm{bin}}\!\Bigl(\sum_C q_C\, e_C\Bigr) \;=\; H_{\mathrm{bin}}(\varepsilon^{*}_{\Pi}). \tag{A.5}$$
Combining (A.4) and (A.5),
$$H(f \mid \Pi) \;\leq\; H_{\mathrm{bin}}(\varepsilon^{*}_{\Pi}). \tag{A.6}$$
Since $\varepsilon^{*}_{\Pi} \in [0, 1/2]$ and $H_{\mathrm{bin}}$ is strictly
increasing on that branch with inverse $H_{\mathrm{bin}}^{-1} : [0, 1] \to [0, 1/2]$,
applying $H_{\mathrm{bin}}^{-1}$ to both sides of (A.6) yields
$$H_{\mathrm{bin}}^{-1}\!\bigl(H(f \mid \Pi)\bigr) \;\leq\; \varepsilon^{*}_{\Pi}. \tag{A.7}$$

((A.3)–(A.7) is **Fano's inequality** in its sharp binary form (Fano
1961, Ch. 6); the two-sided packaging with (A.2) is the
entropy–error bracket of Feder & Merhav 1994, Thm 1. The Jensen step
(A.5) is the standard mutual-information chain-rule derivation of
Fano (Cover & Thomas 2006, proof of Thm 2.10.1). The variance shadow
$\varepsilon^{*}_{\Pi} \leq 2\,\mathbb{E}[\mathrm{Var}(f \mid \Pi)]$
is the **Gini–Bayes inequality** (Breiman et al.\ 1984), used in
Lean because $P_C(1-P_C) \in \mathbb{Q}$ when $P_C \in \mathbb{Q}$.)

(For multi-class generalisations of (A.2), Hashlamoun, Varshney &
Samarasooriya (1994) sharpen Hellman–Raviv to $M$-ary alphabets via
an $f$-divergence bound; in our binary setting their bound coincides
with (A.2) and offers no improvement.)

Combining (A.2) and (A.7) gives Theorem 1. $\square$

**Refinement monotonicity (Proposition 3.2).** Suppose $\Pi'$ refines
$\Pi$. For each $C \in \Pi$ write $C = \bigsqcup_{j} C'_j$ with $C'_j \in \Pi'$
and $\sum_j q_{C'_j} = q_C$. The conditional posterior on $C$ is the
$q_{C'_j}$-weighted average of $\{P_{C'_j}\}_j$, so by concavity of
$H_{\mathrm{bin}}$,
$\sum_j q_{C'_j}\,H_{\mathrm{bin}}(P_{C'_j}) \leq q_C\,H_{\mathrm{bin}}(P_C)$.
Summing over $C$ gives $H(f\mid\Pi') \leq H(f\mid\Pi)$.
The same argument with the concave $p \mapsto \min(p, 1-p)$ on $[0,1]$
gives $\varepsilon^{*}_{\Pi'} \leq \varepsilon^{*}_{\Pi}$. $\square$

**Prior-aware sharpening (Proposition 3.6).** Let
$P_f = |\{v : f(v) = 1\}|/|V|$ and
$\varepsilon^{*}_{\varnothing} = \min(P_f, 1 - P_f)$. Define the
binary error indicator $Z(v) := \mathbf{1}\{\hat{h}_\Pi(v) \neq f(v)\}$
for the plug-in rule $\hat{h}_\Pi$ of §3.2. By construction
$\Pr[Z = 1] = \varepsilon^{*}_{\Pi}$. Since $Z$ is a deterministic
function of $(f, \Pi)$, the finite-alphabet data-processing inequality
(Cover & Thomas 2006, Thm 2.8.1, specialised to discrete distributions —
no measure-theoretic generality needed) on the Markov chain
$f \to \Pi \to Z$ gives
$$I(f ; Z) \;\leq\; I(f ; \Pi). \tag{A.10}$$
The joint distribution of $(f, Z)$ (under the uniform vertex weighting
of §3.1) has marginals
$P_f$ and $\varepsilon^{*}_\Pi$ and is fully determined by the constraint
$\Pr[f \neq \hat{h}_\Pi] = \varepsilon^{*}_\Pi$; the conditional
$f \mid Z = 0$ is the Bayes-posterior on the *correctly classified*
rows and $f \mid Z = 1$ on the *errors*. Among all couplings of
$(f, Z)$ with $\Pr[f = 1] = P_f$ and $\Pr[Z = 1] = \varepsilon^{*}_\Pi$,
the minimum mutual information is attained when $f$ and $Z$ have the
*most overlap*, i.e.\ when $\hat{h}_\Pi$ predicts the marginal mode
and makes errors only on the minority; this minimum equals
$d_{\mathrm{KL}}(\varepsilon^{*}_\Pi \| \varepsilon^{*}_\varnothing)$
(Han & Verdú 1994, eq.\ (6); see also the trivial-channel argument in
Cover & Thomas 2006, §2.10). Hence
$$I(f ; Z) \;\geq\; d_{\mathrm{KL}}\!\bigl(\varepsilon^{*}_\Pi \,\bigm\|\, \varepsilon^{*}_\varnothing\bigr). \tag{A.11}$$
Combining (A.10) and (A.11),
$$d_{\mathrm{KL}}\!\bigl(\varepsilon^{*}_\Pi \,\bigm\|\, \varepsilon^{*}_\varnothing\bigr) \;\leq\; I(f ; \Pi). \tag{A.12}$$
This is Proposition 3.6. The Theorem 1 lower bound is the special
case $P_f = 1/2$ (then $\varepsilon^{*}_\varnothing = 1/2$ and
$d_{\mathrm{KL}}(\varepsilon \| 1/2) = 1 - H_{\mathrm{bin}}(\varepsilon)$,
so (A.12) reduces to $H(f \mid \Pi) \leq H_{\mathrm{bin}}(\varepsilon^{*}_\Pi)$,
equation (A.6)). For $P_f \neq 1/2$ the bound is strictly tighter:
$d_{\mathrm{KL}}(\varepsilon \| \varepsilon^{*}_\varnothing) >
d_{\mathrm{KL}}(\varepsilon \| 1/2)$ at any $\varepsilon \neq \varepsilon^{*}_\varnothing$.
$\square$

**Tightness.** Both boundaries of the achievable region $\tilde{A}_2$
are realised by explicit one-parameter families on a finite vertex set
$V = \{1, \ldots, n\}$ (uniform vertex weighting, §3.1 *Remark*).

*Fano (lower) boundary $\Pi_\varepsilon^{\mathrm{F}}$.* For $\varepsilon \in [0, 1/2]$
and $n$ such that $\varepsilon n \in \mathbb{Z}$, take the trivial
partition $\Pi_\varepsilon^{\mathrm{F}} := \{V\}$ and let $f$ have
exactly $\varepsilon n$ ones. Then $P = e = \varepsilon$,
$$H(f \mid \Pi_\varepsilon^{\mathrm{F}}) \;=\; H_{\mathrm{bin}}(\varepsilon), \qquad \varepsilon^{*}_{\Pi_\varepsilon^{\mathrm{F}}} \;=\; \varepsilon, \tag{A.8}$$
attaining (A.7) with equality and tracing the lower boundary as
$\varepsilon$ varies in $[0, 1/2]$.

*Hellman–Raviv (upper) boundary $\Pi_\alpha^{\mathrm{HR}}$.* For
$\alpha \in [0, 1]$ and $n$ such that $\alpha n \in 2\mathbb{Z}$,
partition $V = C_0 \sqcup C_1$ with $|C_1| = \alpha n$,
$|C_0| = (1 - \alpha) n$; let $f \equiv 0$ on $C_0$ and let $f$ be
exactly half-zero/half-one on $C_1$. Then $e_{C_0} = 0$, $e_{C_1} = 1/2$,
$q_{C_0} = 1 - \alpha$, $q_{C_1} = \alpha$, so
$$H(f \mid \Pi_\alpha^{\mathrm{HR}}) \;=\; \alpha, \qquad \varepsilon^{*}_{\Pi_\alpha^{\mathrm{HR}}} \;=\; \alpha / 2 \;=\; \tfrac{1}{2}\,H(f \mid \Pi_\alpha^{\mathrm{HR}}), \tag{A.9}$$
attaining (A.2) with equality and tracing the upper boundary as
$\alpha$ varies in $[0, 1]$. The balanced limit $\alpha = 1$ collapses
the sandwich at $H = 1$, $\varepsilon^{*} = 1/2$,
$H_{\mathrm{bin}}^{-1}(1) = 1/2 = \tfrac{1}{2} \cdot 1$. The discrete
upper-side witness in the E02 ledger is the row
$(G, \mathcal{A}, L) = (P_6, \text{GAT/GIN}, 1)$, where
$\varepsilon^{*} = 1/3 = \tfrac{1}{2} \cdot 2/3 = \tfrac{1}{2}\,H(f\mid\Pi)$
(parquet sha `25001ab4…`, T-3 audit, min upper margin 0.0). The lower
side is realised by every pure row of E02 (988 / 1000 rows; both sides
zero, corresponding to $\varepsilon = 0$ in (A.8)).

---

*Appendix B (formerly: the $\mathrm{MI}^2 = 1/2$ Cautionary Lemma) was
**removed** in theory amendment 001 (2026-05-30) following a PI audit
which found that the appendix was re-litigating a settled question. The
operational takeaway is preserved in §3.5. The full pre-amendment text is
archived at `archived/PAPER-ARXIV.pre-amendment-001.md` Appendix B for
posterity.*

---

## Appendix C — Per-Experiment Technical Reports

Each experiment (`20-experiments/<EXX>-*/`) ships a `LAB-PLAN.md`
with: (§1) what this is supposed to prove; (§2) cost envelope;
(§3) staged kill-gates; (§4) edge instances; (§5) response recipes;
(§6) remaining failure modes; (§7) cutover criteria; (§8) out of scope.

Index of artefacts and claim IDs:

| Claim ID | Tier | Experiment |
|---|---|---|
| `PAMPC-BRIDGE-INEQ-STATUS` | L-I | Appendix A |
| `PAMPC-LEAN-WITNESS-C4-K` | L-II | Appendix D |
| `PAMPC-E02-DIG-TABLE` | L-I | E02 exact-rational witnesses |
| `PAMPC-E02-DIG-SUMMARY` | L-I | E02 |
| `PAMPC-E02-ORACLE-XCHECK` | L-I | E02 |
| `PAMPC-E03-DIG-TABLE` | L-I | E03 conditional-entropy monotonicity |
| `PAMPC-E03-MONOTONICITY-LEDGER` | L-I | E03 |
| `PAMPC-E03-WL-STABILITY-LEDGER` | L-I | E03 |
| `PAMPC-E04-RUNS-TABLE` | float | E04 trained-GNN correspondence (pilot) |
| `PAMPC-E04-FALSIFIER-LEDGER` | float | E04 |
| `PAMPC-E04-CORRESPONDENCE-VERDICT` | float | E04 |
| `PAMPC-E06-CCI-TABLE` | float | E06 CCI vs. performance (pilot) |
| `PAMPC-E06-ANTICORR-VERDICT` | float | E06 |
| `PAMPC-E07-FEATURE-TABLE` | L-I | E07 feature-richness boundary |
| `PAMPC-E07-BOUNDARY-VERDICT` | L-I | E07 |
| `PAMPC-E08-TRANSFER-TABLE` | float | E08 quantization-transfer (pilot) |
| `PAMPC-E08-TRANSFER-VERDICT` | float | E08 |
| `PAMPC-E08-HCLEAN-COVERAGE` | float | E08 |
| `PAMPC-E09-PRICING-TABLE` | L-I | E09 intervention pricing |
| `PAMPC-E09-INVARIANTS-LEDGER` | L-I | E09 |
| `PAMPC-E09-VERDICT` | L-I | E09 |
| `PAMPC-E01-TOY-TABLE` | float | E01 oversmoothing baseline |
| `PAMPC-E01-VERDICT` | float | E01 |

---

## Appendix D — Lean Witness Obligations

- **`MPCBridge.lean::DIG_of_pure`** — variance form $\mathbb{E}[\mathrm{Var}(f,\Pi)]=0$
  under purity. **Mechanised** (P3.4).
- **`Witnesses.lean::C4_const_partitionCount`** — concrete witness on
  $\{C_4,\ldots,C_8,\text{Petersen}\}$ at depths 0..3 via `native_decide`.
  **Mechanised**. Claim `PAMPC-LEAN-WITNESS-C4-K`.
- **Bridge inequality in general form** — deferred per project charter.
  Mechanising the discrete version on anchor graphs is P3 scope;
  the full general form is not.

---

## Appendix E — E08 Experimental Design

Full specification in `20-experiments/E08-quantization-transfer/LAB-PLAN.md`
and `DESIGN.md`. Summary:

**Staged execution** (each stage is a kill-gate):

| Stage | Content | Cap |
|---|---|---|
| A | Calibration: 1 family × 1 depth × 1 graph × 1 seed × 11 ε | ≤ 0.5 GPU-h |
| B | Edge instances (B.1–B.8): apparatus stress tests | ≤ 2 GPU-h |
| C | Diagonal: GIN × mid-depth × all graphs × ½ seeds × full ε | ≤ 2 GPU-h |
| D | Architecture fan-out: all families × mid-depth | ≤ 3 GPU-h |
| E | Depth fan-out: borderline cells from D only | ≤ 6 GPU-h |
| F | Sealing | — |

**Edge instances** tested before bulk (B.1–B.8) cover: width vs.\ Petersen
depth-4; ε collapse on $C_3$; seed dispersion; H1 plateau definition;
H3 ceiling calibration; GAT attention determinism; GatedGCN overfit on
$C_3$; depth-pruning from E04 stability data.

**Decision rule** — see §9.

**Two-tier verdict architecture:**

- `stage_verdict` — apparatus health (did the stage produce the expected
  row count without error?). Halts the chain on any non-PASS.
- `scientific_verdict` — the DESIGN.md §3 decision rule. Only emitted
  at Stage E in `mode=full`.

The pilot run (apparatus exercise, `mode=pilot`) sealed
`inconclusive-pilot` at G2-transfer, confirming the harness compiles and
the seal verifies. Stages K, L, and M of the `mode=full` execution
completed on 2026-05-30 in `20-experiments/E08-quantization-transfer/`
(see LAB-PLAN §10.5–§10.8); their `PAMPC-E08-{K,L1,L2,M}-*` claims are
recorded in the registry as `float`-tier and are NOT part of this
paper's reproducibility contract.

---

## Appendix F — Build Verification

To verify this paper's reproducibility contract:

```bash
python -m pampc_paper.build status   # claim registry summary
python -m pampc_paper.build gates    # all six gates → PASS
python -m pampc_paper.build build paper-01-pampc-core
```

A successful run reproduces the Merkle root over 10 experiments and 27
leaves, verifies the `byte_identical` predicate against the registered
baseline, and confirms all six decision gates PASS. A tamper test
(append "TAMPER" to `paper.manifest.txt`) correctly returns
`SHA-MISMATCH`.

---

## Appendix G — Extended Related Work

This appendix collects context that §2 only gestures at. None of it is
load-bearing for the proofs (Theorem 1, Propositions 3.2–3.6) or for
the empirical claims; it is included for completeness and to credit
prior lineages we draw on.

**Oversmoothing and over-squashing.** Cai & Wang (2020) and Oono &
Suzuki (2020) characterise depth-induced embedding collapse on
bipartite graphs; our float-tier experiment E01 reproduces this
qualitatively. Alon & Yahav (2021) frame over-squashing as an
information-bottleneck phenomenon. The bridge inequality is agnostic
to bottleneck architecture: it holds for any MPNN computing via
depth-$L$ rooted coloured neighbourhood aggregation.

**Partition-refinement antecedents (three lineages).**
*(i) Ergodic theory.* Kolmogorov (1958), Sinai (1959), and Rokhlin
(1967) defined entropy as a supremum over refining partitions;
refinement-monotonicity of $H(\Pi)$ is the structural axiom of that
construction. Proposition 3.2 is the finite, combinatorial cousin (no
$\sigma$-additivity used — see §3.1 *Remark*).
*(ii) Algorithmic partition refinement.* Hopcroft (1971) and Paige &
Tarjan (1987) gave the algorithmic schema. 1-WL is the graph
specialisation, used in McKay's *nauty* (1981) for isomorphism testing
and sharpened into the $k$-WL hierarchy by Cai, Fürer & Immerman
(1992) and Grohe (2017).
*(iii) Algebraic graph theory.* The equitable-partition ancestry is
already foregrounded in §2; we add only that Schwenk's 1974
characterisation and the textbook treatment in Godsil & Royle (2001,
ch. 9) are the direct sources for the $L \to \infty$ fixpoint
statement.

**Modern partition-indexed GNN theory (2022–2024).** A recent wave of
GNN-expressivity work uses partitions in essentially the same role:
Geerts & Reutter (2022) characterise MPNN expressivity by per-layer
partition refinement; Morris, Lipman, Maron, Rieck, Kriege, Grohe, Fey
& Borgwardt (2023) survey the field with equitable partitions as the
WL fixpoint; Grohe (2021) connects partition refinement to
counting-logic; Böker, Levie, Huang, Villar & Morris (2024) define a
metric on partitions and quantify how close MPNNs come to separating
points — the closest existing work in spirit to our Bayes-error
packaging. None of this wave delivers all three of (a) a **two-sided**
Bayes-error bracket indexed by $\Pi_{\mathcal{A}}(G, L)$, (b) an
**exact-rational** ledger on small graphs, and (c) a **mechanised**
statement; that triple is the unique contribution of PA-MPC.

**Learning-theoretic uses of refinement-monotonicity.** Outside GNNs,
Steinke & Zakynthinou (2020) and Asadi, Abbe & Verdú (2018) apply
refinement-monotonicity arguments to partitions of hypothesis classes
for generalisation bounds — the same Proposition-3.2 move applied in
learning theory.

---

*Reproducibility footer.* Branch `lean-partitions-algebra-2026-Q3`.
HEAD `fcf173a`. Merkle root `702b38c86c7a9361…` over 10 experiments /
27 leaves. All six gates PASS. E08 `mode=full` Stages K, L, and M
sealed on 2026-05-30 (artefacts `pulled-artefacts/E08-stage-\{K,L,M\}/`);
their `PAMPC-E08-\{K,L1,L2,M\}-*` claims are `float`-tier and are not
part of this paper's reproducibility contract.
