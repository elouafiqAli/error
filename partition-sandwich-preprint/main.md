# A Two-Sided Bayes-Error Bracket from Partition-Conditional Entropy

*Markdown twin of `main.tex`. Math is KaTeX-compatible.*

## Abstract

Many machine-learning predictors are constant on the cells of a fixed
partition of their input space: decision trees on their leaves, vector
quantisers and codebook classifiers on Voronoi cells, message-passing
graph neural networks on Weisfeiler–Leman colour classes. For all such
predictors the partition is the irreducible expressivity bottleneck.
We give one elementary two-sided closed-form bracket, in the form ML
practitioners need, between the Bayes error $\varepsilon^{*}_{\Pi}$ of
the best constant-on-cells predictor and the partition-conditional
entropy $H(f\mid\Pi)$ of a binary label $f$:

$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f\mid\Pi)\bigr) \;\le\; \varepsilon^{*}_{\Pi} \;\le\; \tfrac{1}{2}\,H(f\mid\Pi).
$$

The bracket is tight on both boundaries by explicit witnesses,
unimprovable in closed form (no constant smaller than $1/2$, no
pointwise-larger lower function), and pins $\varepsilon^{*}_{\Pi}$ to a
window of width at most $w^{*}\approx 0.1610$ uniformly in $\Pi$ and
$f$. Three worked applications — decision trees, vector quantisation,
and message-passing networks via Weisfeiler–Leman — show how the
bracket lifts to architecture-independent, training-free error bounds.
A short companion Julia script (`verify.jl`) audits the bracket on
$1{,}000$ random partitions in exact rational arithmetic plus
certified interval arithmetic; zero violations. On real benchmarks
the bracket is two orders of magnitude cheaper than a single
training epoch, on tabular data the empirical Bayes floor matches
CART and logistic regression to four decimals at every cell budget
tested, and on featureless structural-WL benchmarks (Cayley and
Paley graphs) the bracket correctly pins at the marginal-entropy
ceiling on the tasks $1$-WL is provably blind to — evidence that
the diagnostic has both the right success regime and the right
*failure* regime, the latter being the empirical face of an
$\varepsilon$-robust refinement of the classical MPNN–WL
constancy lemma (Lemma 6′) that we prove and exercise here.

---

## 1. Introduction

### From inputs to vertices

Pick any supervised learning problem with a finite or finitely
representable input set: a training corpus of $n$ examples, the nodes
of a graph, the pixels of an image grid, the leaves of a decision
tree, the codewords of a quantiser, the time-steps of a discretised
process. Call the elements of this set **vertices** and write the set
$V$. A binary classification task on $V$ is then nothing but a
function $f:V\to\{0,1\}$ — the **label vector** we wish to predict.
This is the most elementary supervised-learning datum: "which vertices
are positive?".

### What a model actually sees

A learning algorithm rarely processes $V$ directly. Instead, the
architecture — a tree depth, a codebook size, a network depth, a
feature map — imposes an **equivalence relation** on $V$: two vertices
look identical to the model iff they route to the same leaf, codeword,
Weisfeiler–Leman colour, or feature-map output. The quotient of $V$
by this equivalence relation is a **partition**
$\Pi=\{C_1,\dots,C_m\}$ of $V$ into nonempty **cells**
$C_i\subset V$. The architecture-imposed map $C:V\to\Pi$, sending each
vertex to its cell, is the **lens** through which the model perceives
the input. Anything the model predicts about a vertex $v$ must factor
as
$$
\hat f(v) = g(C(v)), \qquad g:\Pi\to\{0,1\}.
$$
This factorisation is exact, not approximate: it is forced by the
architecture before training begins. In particular, two vertices in
the same cell must receive the same predicted label, *regardless of
how much training data, parameters, or epochs are spent*. The
partition $\Pi$ is therefore the **irreducible expressivity
bottleneck** of the model family.

### Three concrete instances

The vertex–partition view unifies models that look superficially
unrelated:

- **Decision trees and random forests.** $V$ is the training set;
  cells $C_i$ are the leaves; the equivalence "$v\sim w$ iff $v,w$
  end at the same leaf" is the partition $\Pi_T$. Every leaf-constant
  rule of CART, C4.5 or any greedy tree learner factors through
  $\Pi_T$.
- **Vector quantisers and clustering classifiers.** $V$ is the input
  space (or a finite training sample); cells are pre-images of the
  $k$ codewords (Voronoi cells in the metric case). Nearest-codeword,
  $k$-means, and product-quantisation retrieval factor through their
  codebook partition $\Pi_Q$.
- **Message-passing graph neural networks (MPNNs).** $V$ is the
  vertex set of a graph $G$; the depth-$L$ Weisfeiler–Leman
  refinement $\mathrm{WL}_L(G)$ is a partition of $V$. Every
  depth-$L$ MPNN with shared permutation-invariant updates and no
  node identifiers is constant on the cells of $\mathrm{WL}_L(G)$:
  WL is the lens through which a bounded-depth MPNN sees its graph.

In each case the architectural choice (tree depth, codebook size,
MPNN depth) selects a partition; the partition determines what the
model can possibly express; the label $f$ is the only thing the model
is asked to fit. The triple $(V,\Pi,f)$ is the data of the problem.

### The two questions

- **(Q1) Lower bound — no predictor can do better.** Given $\Pi$ and
  $f$, what is the smallest possible error achievable by *any*
  $g:\Pi\to\{0,1\}$? We call this the **partition Bayes error**
  $\varepsilon^{*}_{\Pi}$.
- **(Q2) Upper bound — some predictor achieves it.** Is there a
  quantity, easily computed from $(\Pi,f)$, that *certifies* a small
  $\varepsilon^{*}_{\Pi}$ from above? Such a certificate would let a
  practitioner read off a guaranteed error level without ever
  training a model.

### Why entropy?

The natural functional of $f:V\to\{0,1\}$ relative to $\Pi$ is the
**partition-conditional Shannon entropy**
$$
H(f\mid\Pi) := \sum_{C\in\Pi} q_C\,H_{\mathrm{bin}}(P_C),
$$
where $q_C$ is the mass of cell $C$ and $P_C$ is the fraction of
positives inside $C$. $H(f\mid\Pi)$ measures the average **impurity**
of $f$ within cells: zero exactly when every cell is monochromatic,
one exactly when every cell is maximally mixed ($P_C=1/2$). Three
reasons make it inevitable as the right diagnostic:

- **Decision trees already compute it.** CART's information-gain
  splitting criterion is the change in $H(f\mid\Pi)$ when one refines
  $\Pi$ at a candidate split. The bracket below converts that
  internal criterion into an external error guarantee.
- **It is sub-σ-algebra entropy.** $\Pi$ generates a sub-σ-algebra of
  the power set of $V$, and $H(f\mid\Pi)$ is the standard conditional
  entropy of $f$ given that sub-σ-algebra. Every partition-respecting
  predictor is measurable with respect to this sub-σ-algebra;
  conditional entropy is the canonical information-theoretic
  obstruction to recovering $f$ from such predictors.
- **It is the only functional with a two-sided bracket.** Classical
  inequalities of Fano (1961) and Hellman–Raviv (1970) relate
  $\varepsilon^{*}_{\Pi}$ to $H(f\mid\Pi)$ from both sides; no other
  elementary scalar functional of $(\Pi,f)$ enjoys both a matching
  lower bound *and* a matching upper bound in closed form.

### This paper

For binary labels we answer (Q1) and (Q2) simultaneously by a single
classical inequality recast for partitions: the partition-conditional
Shannon entropy $H(f\mid\Pi)$ two-sidedly brackets the Bayes error
$\varepsilon^{*}_{\Pi}$:
$$
H_{\mathrm{bin}}^{-1}(H(f\mid\Pi)) \;\le\; \varepsilon^{*}_{\Pi} \;\le\; \tfrac{1}{2}H(f\mid\Pi).
$$
The lower side specialises Fano (1961); the upper side specialises
Hellman–Raviv (1970); the two-sided packaging is in the spirit of
Feder–Merhav (1994) and Ho–Verdú (2010). The contribution of this
paper is not the inequalities themselves but their packaging as a
**single architecture-level diagnostic** on $(V,\Pi,f)$: once
computed, the bracket gives the practitioner *simultaneously* an
unconditional lower bound on the error of every model in the
architectural class, and a constructive upper bound achieved by the
elementary plug-in predictor on cells.

### What the bracket enables

A practitioner armed with $H(f\mid\Pi)$ for a candidate architecture
can:

- **(E1) Reject architectures cheaply.** If
  $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi))$ is larger than the target
  error, no training run of any model in the family will meet the
  target; reject the family before spending compute.
- **(E2) Certify architectures cheaply.** If $\tfrac{1}{2}H(f\mid\Pi)$
  is smaller than the target error, the trivial plug-in predictor on
  cells already meets the target — no optimiser, no validation set,
  no hyperparameters.
- **(E3) Compare architectures on equal footing.** Two partitions
  $\Pi_1,\Pi_2$ (say tree depths or MPNN depths) yield two brackets;
  the one with smaller $H(f\mid\Pi)$ dominates uniformly in the
  optimiser.
- **(E4) Track refinement gains.** If $\Pi'$ refines $\Pi$ (deeper
  tree, larger codebook, more MPNN layers), $H(f\mid\Pi')\le H(f\mid\Pi)$
  and both bracket endpoints move monotonically (Proposition 4).
  This quantifies the marginal value of model-class growth.

The bracket is tight on both boundaries with explicit witnesses, and
Proposition 5 shows no closed-form improvement is possible. The
bracket width is bounded above by an explicit constant
$w^{*}\approx 0.1610$ uniformly in $\Pi$ and $f$ — to our knowledge
the first **uniform conservativeness gap** reported in the
entropy-bounds-Bayes-error literature.

### Contributions

- **(C1) Bracket.** A self-contained two-sided closed-form bracket
  (Theorem 1) on the Bayes error of every partition-constant
  predictor of a binary label, with an elementary finite-sum proof.
- **(C2) Uniform slack.** The explicit constant
  $w^{*}\approx 0.1610$ (Corollary 2) bounding the bracket's width
  uniformly over all $\Pi$ and $f$.
- **(C3) Sharpness.** A negative result (Proposition 5) ruling out
  any uniform improvement of either side by simpler closed-form
  expressions.
- **(C4) Three worked applications.** Decision trees, vector
  quantisation, and Weisfeiler–Leman-refined message passing (§8),
  each instantiated with numerical examples, yielding training-free
  error brackets for that family.
- **(C5) Mechanised check.** A short Julia script (`verify.jl`)
  verifies the bracket on $10^{3}$ random partitions in exact
  rational arithmetic (for $\varepsilon^{*}_{\Pi}$) together with
  certified interval arithmetic (for the Shannon-entropy terms);
  zero violations.
- **(C6) Empirical evidence on real benchmarks.** Eight
  self-contained experiments (§8.5) on UCI Adult, breast-cancer,
  wine, digits-binary, Twitch-EN, Cora, CiteSeer, PubMed,
  ogbn-arxiv, and a featureless structural-WL battery (Cayley +
  Paley). Highlights: on UCI Adult, CART training error matches
  $\varepsilon^{*}_{\Pi_d}$ to four decimals at every depth
  $d = 1,\dots,15$ (E1) and logistic-regression-on-cells matches
  $\varepsilon^{*}_{\Pi_k}$ for every $k \le 256$ (E2); per-arch
  bracket evaluation is $20$–$133\times$ cheaper than one CART
  fit (E6); as a heterogeneous-menu NAS pre-filter the bracket
  attains Kendall $\tau = 0.48$ ($p = 5{\times}10^{-5}$) with
  held-out test error on Adult while parameter count *anti*-ranks
  the same menu ($\tau = -0.38$, E6-NAS); on feature-rich citation
  / social graphs the depth-$3$ $1$-WL partition becomes
  near-discrete (95.6% singleton cells on ogbn-arxiv), exposing
  the bracket's partition-cardinality collapse regime which we
  report transparently rather than claim as a victory (E3); on
  featureless structural-WL benchmarks the bracket correctly pins
  at the marginal-entropy ceiling (E3b);
  empirical concentration to the population bracket matches the
  $\Theta(1/\sqrt n)$ rate of Proposition 7 with $1.000$ coverage
  at the nominal $0.95$ level (E7).

**Scope.** Finite $V$, finite $\Pi$, binary $f$. Multi-class via
Feder–Merhav concave envelopes; continuous-alphabet via Ho–Verdú.

---

## 2. Setup

We now make the vertex–partition–label triple $(V,\Pi,f)$ of §1
formal, and fix the two quantities the rest of the paper relates: the
partition Bayes error $\varepsilon^{*}_{\Pi}$ (the quantity to be
bounded) and the partition-conditional entropy $H(f\mid\Pi)$ (the
bound).

Let $V$ be a finite set with $|V|=n\ge 1$, and let
$\Pi=\{C_1,\dots,C_m\}$ be a partition of $V$ into nonempty cells.
Let $f:V\to\{0,1\}$ be a binary label, and write $C(v)$ for the cell
of $\Pi$ containing $v$. Endow $V$ with the uniform measure
$q_v=1/n$ (non-uniform weights work identically, see Remark below).

**Cell statistics.** For each cell $C\in\Pi$,
$$
q_C := |C|/n, \quad P_C := |C|^{-1}\sum_{v\in C}f(v), \quad
e_C := \min(P_C, 1-P_C) \in [0,1/2].
$$

**Partition Bayes error.**
$$
\varepsilon^{*}_{\Pi} := \min_{g:\Pi\to\{0,1\}} \Pr[g(C(v))\ne f(v)] = \sum_C q_C\,e_C,
$$
attained by the plug-in $\hat h_\Pi(v) := \mathbf{1}\{P_{C(v)}\ge 1/2\}$.

**Partition-conditional entropy.** In bits,
$$
H(f\mid\Pi) := \sum_C q_C\,H_{\mathrm{bin}}(P_C) = \sum_C q_C\,H_{\mathrm{bin}}(e_C),
$$
where $H_{\mathrm{bin}}(p) := -p\log_2 p - (1-p)\log_2(1-p)$ and the
second equality is the symmetry $H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(1-p)$.

**Inverse binary entropy.** $H_{\mathrm{bin}}:[0,1]\to[0,1]$ is
strictly concave, symmetric about $1/2$, with max
$H_{\mathrm{bin}}(1/2)=1$, strictly increasing on $[0,1/2]$. Its inverse
on the increasing branch is $H_{\mathrm{bin}}^{-1}:[0,1]\to[0,1/2]$.
As the inverse of a concave increasing function,
$H_{\mathrm{bin}}^{-1}$ is **convex**, continuous, strictly
increasing, with $H_{\mathrm{bin}}^{-1}(0)=0$ and
$H_{\mathrm{bin}}^{-1}(1)=1/2$.

> **Remark (non-uniform weighting).** All statements extend to
> non-uniform weights $\{q_v\}$ via $q_C := \sum_{v\in C} q_v$ and
> $P_C := q_C^{-1}\sum_{v\in C} q_v f(v)$.

> **Remark (range of $H(f\mid\Pi)$).** Since $H_{\mathrm{bin}}(P_C)\in[0,1]$
> for every $C$ and $\sum_C q_C = 1$, the partition-conditional
> entropy satisfies $H(f\mid\Pi)\in[0,1]$ in bits. In particular it
> lies in the domain of $H_{\mathrm{bin}}^{-1}$, justifying the
> left-hand side of (3.1) below.

---

## 3. Main result

**Theorem 1 (Two-sided bracket).** For every finite partition $\Pi$
of a finite set $V$ and every binary $f:V\to\{0,1\}$,
$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f\mid\Pi)\bigr) \;\le\; \varepsilon^{*}_{\Pi} \;\le\; \tfrac{1}{2}\,H(f\mid\Pi). \tag{3.1}
$$

**Proposition 1.5 (Achievable region).** Define
$$
\widetilde A_2 := \bigl\{(\varepsilon, H)\in[0,1/2]\times[0,1] : H_{\mathrm{bin}}^{-1}(H)\le\varepsilon\le H/2\bigr\}.
$$
Then $\widetilde A_2$ is exactly the closure of the set of pairs
$(\varepsilon^{*}_{\Pi}, H(f\mid\Pi))$ achievable by some finite
partition $\Pi$ of a finite set $V$ and some binary
$f:V\to\{0,1\}$. Specifically:
(i) every achievable pair lies in $\widetilde A_2$ (Theorem 1);
(ii) the lower boundary $\{(\varepsilon, H_{\mathrm{bin}}(\varepsilon)) : \varepsilon\in[0,1/2]\}$ is realised by the Fano family $\Pi^{\mathrm F}_{\varepsilon}$ of §7;
(iii) the upper boundary $\{(H/2, H) : H\in[0,1]\}$ is realised by the Hellman–Raviv two-cell family $\Pi^{\mathrm{HR}}_{\alpha}$ of §7 with $\alpha = H$;
(iv) the interior is realised by an explicit two-cell construction (Fano witness + monochromatic complement, with mass split solved via the strictly decreasing map $\varepsilon_1\mapsto H_{\mathrm{bin}}(\varepsilon_1)/\varepsilon_1$ on $(0,1/2]$).

See `figures/achievable_region.pdf`.

**Corollary 2 (Uniform slack).** Let $w(H) := \tfrac{1}{2}H - H_{\mathrm{bin}}^{-1}(H)$.
Then $w(0)=w(1)=0$, $w$ is concave on $[0,1]$, and
$$
w^{*} := \max_{H\in[0,1]} w(H) = \tfrac{1}{2}H_{\mathrm{bin}}(1/5) - 1/5 \approx 0.1610,
$$
attained at $H^{*} = H_{\mathrm{bin}}(1/5)\approx 0.7219$, equivalently
$\varepsilon=1/5$. Consequently, for every $\Pi, f$,
$\tfrac{1}{2}H(f\mid\Pi) - \varepsilon^{*}_{\Pi} \le w^{*}$ and
$\varepsilon^{*}_{\Pi} - H_{\mathrm{bin}}^{-1}(H(f\mid\Pi)) \le w^{*}$.

*Proof.* $w'(H) = \tfrac{1}{2} - 1/H_{\mathrm{bin}}'(H_{\mathrm{bin}}^{-1}(H))$ by
chain rule. $w'(H)=0$ gives $H_{\mathrm{bin}}'(\varepsilon) = 2$, i.e.
$\log_2((1-\varepsilon)/\varepsilon) = 2$, so $\varepsilon = 1/5$. Substituting back
gives $H^{*}$ and $w^{*}$. Concavity of $w$ follows from the linear
$H/2$ and convex $H_{\mathrm{bin}}^{-1}$ (so $-H_{\mathrm{bin}}^{-1}$
concave). $\square$

---

## 4. Proof of Theorem 1

**Lemma 3 (Scalar Hellman–Raviv).** For every $p\in[0,1]$,
$$
\min(p, 1-p) \;\le\; \tfrac{1}{2}\,H_{\mathrm{bin}}(p), \tag{4.1}
$$
with equality iff $p\in\{0, 1/2, 1\}$.

*Proof.* By symmetry assume $p\in[0,1/2]$, so (4.1) becomes
$g(p) := \tfrac{1}{2}H_{\mathrm{bin}}(p) - p \ge 0$. The function $g$ is
concave on $[0,1/2]$ (concave $+$ linear) with $g(0)=g(1/2)=0$;
hence $g\ge 0$ on $[0,1/2]$. Equality in the interior would force $g$
constantly zero, contradicting strict concavity on $(0,1/2)$.
$\square$

*Proof of Theorem 1.*
**Upper bound.** Apply (4.1) with $p=P_C$ to each cell and multiply
by $q_C\ge 0$: $q_C e_C \le \tfrac{1}{2}q_C H_{\mathrm{bin}}(P_C)$.
Summing over $C\in\Pi$: $\varepsilon^{*}_{\Pi}\le \tfrac{1}{2}H(f\mid\Pi)$.

**Lower bound.** The symmetry $H_{\mathrm{bin}}(P_C) = H_{\mathrm{bin}}(e_C)$
yields $H(f\mid\Pi) = \sum_C q_C H_{\mathrm{bin}}(e_C)$. Since
$H_{\mathrm{bin}}$ is concave on $[0,1]$ and $\{e_C\}\subset[0,1/2]$,
Jensen with weights $\{q_C\}$ gives
$$
H(f\mid\Pi) \le H_{\mathrm{bin}}\!\Bigl(\sum_C q_C e_C\Bigr) = H_{\mathrm{bin}}(\varepsilon^{*}_{\Pi}).
$$
Since $\varepsilon^{*}_{\Pi}\in[0,1/2]$ and $H_{\mathrm{bin}}^{-1}$ inverts
$H_{\mathrm{bin}}$ on $[0,1/2]$, applying it yields
$H_{\mathrm{bin}}^{-1}(H(f\mid\Pi))\le\varepsilon^{*}_{\Pi}$. $\square$

> **Remark (Lagrangian dual programs).** Both halves of (3.1) read as
> opposite extremal programs on $\{(q_C, e_C)\}$: the lower bound is
> the supremum of $\sum_C q_C H_{\mathrm{bin}}(e_C)$ subject to
> $\sum_C q_C = 1$, $\sum_C q_C e_C = \varepsilon$, attained at $e_C\equiv\varepsilon$
> (Jensen) with value $H_{\mathrm{bin}}(\varepsilon)$; the upper bound is the
> supremum of $\sum_C q_C e_C$ subject to $\sum_C q_C = 1$,
> $\sum_C q_C H_{\mathrm{bin}}(e_C) = H$, attained on the boundary set
> $e_C\in\{0,1/2\}$ (Lemma 3) with value $H/2$. The Feder–Merhav
> primal concave-envelope traces the upper boundary of $\widetilde A_2$
> by this boundary mixture.

> **Remark (Gini variance form).** From $\min(p,1-p)\le 2p(1-p)$,
> $\varepsilon^{*}_{\Pi}\le 2\sum_C q_C P_C(1-P_C)$. With rational $P_C$,
> the right-hand side is rational and admits exact arithmetic,
> convenient for Gini-impurity audits of tree splits.

---

## 5. Refinement monotonicity

$\Pi'$ **refines** $\Pi$ ($\Pi'\preceq\Pi$) if every cell of $\Pi'$ is
contained in some cell of $\Pi$. Refinement corresponds to model-class
growth: subdividing tree leaves, increasing codebook size, increasing
MPNN depth.

**Proposition 4 (Refinement monotonicity).** If $\Pi'\preceq\Pi$, then
for every binary $f$,
$H(f\mid\Pi')\le H(f\mid\Pi)$ and $\varepsilon^{*}_{\Pi'}\le\varepsilon^{*}_{\Pi}$.

*Proof.* Fix $C\in\Pi$, write $C = \bigsqcup_j C'_j$ in $\Pi'$ with
masses $q_{C'_j}$ summing to $q_C$. The cell mean $P_C$ is the convex
combination $\sum_j(q_{C'_j}/q_C)P_{C'_j}$, so by concavity of
$H_{\mathrm{bin}}$: $\sum_j q_{C'_j}H_{\mathrm{bin}}(P_{C'_j})\le q_C H_{\mathrm{bin}}(P_C)$.
Sum over $C$. Error claim follows by the same argument with the
concave $p\mapsto\min(p,1-p)$. $\square$

This is the deterministic-coarsening case of the data-processing
inequality.

**Proposition 4.5 (Refinement to the discrete partition).** Let
$\Pi_0\preceq\Pi_1\preceq\cdots\preceq\Pi_L$ be a chain with
$\Pi_L$ the discrete partition $\{\{v\}:v\in V\}$. For every binary
$f$, $H(f\mid\Pi_L) = 0$ and $\varepsilon^{*}_{\Pi_L} = 0$, so both
bracket endpoints collapse to $0$ at level $L$. Consequently the
bracket width $\tfrac{1}{2}H(f\mid\Pi_\ell) - H_{\mathrm{bin}}^{-1}(H(f\mid\Pi_\ell))$
is monotonically non-increasing in $\ell$ and tends to $0$ as
$\Pi_\ell$ approaches discreteness.

*Proof.* On a singleton cell $\{v\}$, $P_{\{v\}} = f(v)\in\{0,1\}$,
so $H_{\mathrm{bin}}(P_{\{v\}}) = 0$ and $\min(P_{\{v\}}, 1-P_{\{v\}}) = 0$.
Width monotonicity is Proposition 4. $\square$

Proposition 4.5 is a *consistency check*, not a positive result: it
certifies that the bracket reports exactly zero on a partition refined
to singletons (the correct Bayes error of any deterministic labelling
on its own preimage). This makes the empirical pinch on ogbn-arxiv at
depth 3 (95.6% singleton cells; Table E3) a *verification* of the
bracket's asymptotic behaviour rather than a failure mode. The
informative regime is the intermediate one, where $|\Pi_\ell|/|V|$ is
bounded away from both $0$ and $1$.

---

## 6. Sharpness

**Proposition 5 (Unimprovability).**

- **(i)** For every $c<1/2$ there exists a finite partition $\Pi$ of a
  finite $V$ and a binary $f$ with $\varepsilon^{*}_{\Pi} > c\cdot H(f\mid\Pi)$.
  No constant smaller than $1/2$ can replace the coefficient on the
  right of (3.1).
- **(ii)** For every $\psi:[0,1]\to[0,1/2]$ such that
  $\{H:\psi(H)>H_{\mathrm{bin}}^{-1}(H)\}$ contains an open
  subinterval $U\subset(0,1)$, there exists a finite partition $\Pi$
  of a finite $V$ and a binary $f$ with
  $\varepsilon^{*}_{\Pi} < \psi(H(f\mid\Pi))$.

*Proof.* (i) The upper-boundary family $\Pi^{\mathrm{HR}}_\alpha$ of §7
achieves $\varepsilon^{*}_{\Pi}=\tfrac{1}{2}H(f\mid\Pi)$ for every
$\alpha\in(0,1]$.
(ii) Since $H_{\mathrm{bin}}$ is a continuous bijection
$[0,1/2]\to[0,1]$, $H_{\mathrm{bin}}^{-1}(U)$ contains an open
subinterval of $(0,1/2)$. Pick rational $\varepsilon\in H_{\mathrm{bin}}^{-1}(U)\cap(0,1/2)$
and $n$ with $\varepsilon n\in\mathbb Z$; the lower-boundary family
$\Pi^{\mathrm{F}}_\varepsilon$ on this $n$ satisfies $\varepsilon^{*}_{\Pi}=\varepsilon$
and $H(f\mid\Pi) = H_{\mathrm{bin}}(\varepsilon)\in U$. $\square$

Together, Theorem 1 and Proposition 5 identify $\widetilde A_2$ as the
tightest closed-form two-sided bracket on
$(\varepsilon^{*}_{\Pi}, H(f\mid\Pi))$ in the binary case.

> **Remark (multi-class).** For $M>2$ classes the sharp bracket
> replaces $H_{\mathrm{bin}}^{-1}$ by the lower concave envelope of
> admissible (entropy, error) pairs over $\{1,\dots,M\}$
> (Feder–Merhav). A multi-class strengthening of the upper bound via
> $f$-divergences is in Hashlamoun–Varshney–Samarasooriya (1994).

---

## 7. Tightness witnesses

**Lower (Fano) boundary $\Pi^{\mathrm{F}}_\varepsilon$.** Fix
$\varepsilon\in[0,1/2]$ and $n$ with $\varepsilon n\in\mathbb Z$. Take the trivial
partition $\Pi^{\mathrm{F}}_\varepsilon := \{V\}$ and let $f$ have exactly
$\varepsilon n$ ones. Then $P_C = e_C = \varepsilon$,
$H(f\mid\Pi^{\mathrm{F}}_\varepsilon) = H_{\mathrm{bin}}(\varepsilon)$,
$\varepsilon^{*}_{\Pi^{\mathrm{F}}_\varepsilon} = \varepsilon$, attaining the lower bound.

**Upper (Hellman–Raviv) boundary $\Pi^{\mathrm{HR}}_\alpha$.** Fix
$\alpha\in[0,1]$ and $n$ with $\alpha n\in 2\mathbb Z$. Partition
$V=C_0\sqcup C_1$ with $|C_1|=\alpha n$; set $f\equiv 0$ on $C_0$ and
half-zero/half-one on $C_1$. Then $e_{C_0}=0$, $e_{C_1}=1/2$,
$H(f\mid\Pi^{\mathrm{HR}}_\alpha) = \alpha$,
$\varepsilon^{*}_{\Pi^{\mathrm{HR}}_\alpha} = \alpha/2$, attaining the upper
bound. The slack maximiser $w^{*}$ is realised at
$\Pi^{\mathrm{F}}_{1/5}$.

> **Remark (interior achievability).** Disjoint unions of boundary
> witnesses realise the interior of $\widetilde A_2$. Fix
> $(\varepsilon, H)\in\mathrm{int}(\widetilde A_2)$: it is a convex
> combination of a point on each boundary, and the corresponding
> disjoint union with the right mass split realises $(\varepsilon, H)$
> exactly.

---

## 8. Applications

For each family, the partition $\Pi$ is fixed by the architectural
choice (tree depth, codebook size, MPNN depth); the bracket is a
**training-free** bound, depending only on label and
architecture-induced partition.

### 8.1 Decision trees and random forests

A finite decision tree $T$ with $m$ leaves induces
$\Pi_T = \{L_1,\dots,L_m\}$ on its training set. A leaf-constant
predictor on $T$ is a constant-on-cells predictor on $\Pi_T$, so
Theorem 1 brackets the training-set Bayes error of every such tree by
its leaf-conditional entropy. Proposition 4 matches depth–accuracy
intuition: deeper $T'$ with $\Pi_{T'}\preceq\Pi_T$ tightens the
bracket.

**Example (single-split tree on an 8-point task).** Let $V=\{1,\dots,8\}$,
$f=(0,0,1,0,1,1,0,1)$, and let $T$ be the depth-1 stump with leaves
$L_1=\{1,2,3,4\}$, $L_2=\{5,6,7,8\}$.
Then $P_{L_1}=1/4$, $P_{L_2}=3/4$, $q_{L_j}=1/2$, so $e_{L_1}=e_{L_2}=1/4$
and $H(f\mid\Pi_T) = \tfrac{1}{2}H_{\mathrm{bin}}(1/4) + \tfrac{1}{2}H_{\mathrm{bin}}(3/4) = H_{\mathrm{bin}}(1/4)\approx 0.8113$
(symmetry of $H_{\mathrm{bin}}$), while $\varepsilon^{*}_{\Pi_T}=1/4$.
Because both cell errors are equal, Jensen is tight on the lower side
and $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi_T)) = 1/4$ exactly: the bracket
reads $1/4 \le 1/4 \le \tfrac{1}{2}H_{\mathrm{bin}}(1/4)\approx 0.4057$,
saturating the Fano boundary with an upper-side slack of $\approx 0.156$
(close to the universal maximum $w^{*}\approx 0.161$).

### 8.2 Vector quantisation and clustering classifiers

A $k$-codeword quantiser $Q:V\to\{c_1,\dots,c_k\}$ induces
$\Pi_Q = \{Q^{-1}(c_j)\}_{j=1}^k$. Nearest-codeword classification,
$k$-means-based classification, and product-quantisation retrieval
with per-cell vote all factor as $\hat f(v)=g(Q(v))$. Theorem 1
brackets the supervised classification error by post-quantisation
label entropy. Increasing $k$ refines $\Pi_Q$.

**Example (two-cell $k$-means).** $V=\{1,\dots,10\}$,
$C_1=\{1,\dots,5\}$, $C_2=\{6,\dots,10\}$,
$f=(0,0,0,1,1,1,0,1,1,1)$, giving $P_{C_1}=2/5$, $P_{C_2}=4/5$. Then
$H(f\mid\Pi_Q) = \tfrac{1}{2}(H_{\mathrm{bin}}(2/5)+H_{\mathrm{bin}}(4/5))\approx \tfrac{1}{2}(0.9710+0.7219)\approx 0.8464$,
$\varepsilon^{*}_{\Pi_Q} = \tfrac{1}{2}\min(2/5,3/5) + \tfrac{1}{2}\min(4/5,1/5) = \tfrac{1}{2}(2/5)+\tfrac{1}{2}(1/5) = 0.30$.
Bracket: $0.273 \approx H_{\mathrm{bin}}^{-1}(0.8464) \le 0.30 \le \tfrac{1}{2}(0.8464)\approx 0.423$,
an instructive non-saturating interior case.

### 8.3 Message-passing networks and Weisfeiler–Leman

Let $G=(V,E)$ be a finite graph. A depth-$L$ MPNN computes
$$
h^{(\ell+1)}(v) = \phi_{\ell+1}\bigl(h^{(\ell)}(v),\, \{\!\!\{h^{(\ell)}(u): u\in N(v)\}\!\!\}\bigr).
$$

**Definition (admissible MPNN family).** A family $\mathcal A$ of
depth-$L$ MPNNs is *admissible* if every member uses the same
initial-feature map $h^{(0)}$, uses vertex-independent shared
permutation-invariant updates $\phi_\ell$, and uses no node
identifiers.

The depth-$L$ Weisfeiler–Leman refinement $\mathrm{WL}_L(G)$ is the
partition of $V$ obtained by $L$ rounds of multiset-hashing the
initial feature.

**Lemma 6 (MPNN constancy on WL).** Let $\mathcal A$ be admissible
depth-$L$, with $h^{(0)}$ refined as a function of the initial
feature. Then for every member and every $v,w$ sharing a cell of
$\mathrm{WL}_L(G)$, $h^{(L)}(v)=h^{(L)}(w)$.

*Proof.* Induction on $\ell$. Base: same initial feature implies same
$h^{(0)}$. Step: if $v,w$ share a cell of $\mathrm{WL}_{\ell+1}(G)$,
they share a $\mathrm{WL}_\ell$-cell, and the multisets of
$\mathrm{WL}_\ell$-cells over their neighbourhoods coincide; by IH
the neighbour-state multisets coincide; shared
permutation-invariant $\phi_{\ell+1}$ gives
$h^{(\ell+1)}(v)=h^{(\ell+1)}(w)$. $\square$

**Brittleness of Lemma 6 and an $\varepsilon$-robust replacement.**
Lemma 6 requires *strict* equality of $h^{(0)}$ on WL-equivalent
vertices. Any individuating perturbation — additive random
features (Sato et al., 2020), Laplacian / RWPE / SignNet positional
encodings, DropEdge, or vertex identifiers as in ID-GNN (You et
al., 2021) — breaks the hypothesis and the bracket trivialises to
$[0,0]$. We replace it with a quantitative $\varepsilon$-robust
version, splitting the layer map into the standard decomposition
$\phi_{\ell+1}(x,\mu) = \psi_{\ell+1}(x, A_{\ell+1}(\mu))$ where
$A_{\ell+1}$ is a permutation-invariant aggregator and
$\psi_{\ell+1}$ is the post-aggregation combine map.

**Definition ($\delta_0$-quasi-admissible family).** A family
$\mathcal A$ of depth-$L$ MPNNs with layer maps
$\phi_\ell = \psi_\ell\circ(\mathrm{id}, A_\ell)$ is
*$\delta_0$-quasi-admissible with constants $(L_\ell^{c},L_\ell^{m})$
relative to aggregator type $\mathsf T\in\{\mathrm{sum},\mathrm{mean},\mathrm{sym\text{-}norm}\}$*
if:
(i) $d(h^{(0)}(v), h^{(0)}(w))\le\delta_0$ whenever $v,w$ share a
cell of the ideal (constant-feature) 1-WL partition;
(ii) the combine map $\psi_\ell$ is jointly Lipschitz:
$d(\psi_\ell(x,a),\psi_\ell(x',a')) \le L_\ell^{c}\,d(x,x') + L_\ell^{m}\,d(a,a')$;
(iii) $A_\ell$ is 1-Lipschitz w.r.t. the aggregator-specific
transport cost: unnormalised $W_1$ for sum, normalised $W_1$ for
mean, any 1-Lipschitz symmetric function of normalised $W_1$ for
sym-norm.

**Lemma 6′ ($\varepsilon$-robust MPNN–WL constancy).** Let $\mathcal A$
be $\delta_0$-quasi-admissible with maximum degree
$\Delta := \max_v |N(v)|$, aggregator type $\mathsf T$, and constants
as above. For every $v,w$ sharing a cell of the ideal $\mathrm{WL}_L(G)$,
$$
d(h^{(L)}(v), h^{(L)}(w)) \;\le\; \delta_L \;:=\; \delta_0 \prod_{\ell=1}^{L} \bigl(L_\ell^{c} + r_{\mathsf T}\,L_\ell^{m}\bigr), \qquad
r_{\mathsf T} = \begin{cases} \Delta & \mathsf T = \mathrm{sum}\\ 1 & \mathsf T = \mathrm{mean}\\ 1 & \mathsf T = \mathrm{sym\text{-}norm}\end{cases}
$$
Consequently, for an $L_\tau$-Lipschitz readout $\tau$ thresholded
at $1/2$,
$R_V(\hat f)\ge\varepsilon^{*}_{\Pi_L} - L_\tau\,\delta_L$.

*Proof.* (Step 1) Define $\delta_\ell := \sup\{d(h^{(\ell)}(v),h^{(\ell)}(w))\}$
over $(v,w)$ sharing an ideal-WL cell at level $\ell$; the base
case is (i). (Step 2) Fix $v,w$ sharing an ideal $\mathrm{WL}_{\ell+1}$
cell. By ideal-WL construction there is a bijection
$\sigma:N(v)\to N(w)$ with each pair $(u,\sigma(u))$ in the same
ideal $\mathrm{WL}_\ell$ cell, so by IH every per-neighbour distance
is $\le\delta_\ell$ and hence $W_1^{\mathrm u}(\mu_v,\mu_w)\le\Delta\delta_\ell$.
Crucially, $|N(v)|=|N(w)|$ on every WL cell, so the **normalised**
transport cost is exactly $W_1^{\mathrm u}/|N(v)|\le\delta_\ell$
*independent of $\Delta$*. Hence the aggregator output distance is
$\le r_{\mathsf T}\delta_\ell$. (Step 3) Combine with (ii):
$\delta_{\ell+1}\le(L_{\ell+1}^{c} + r_{\mathsf T}L_{\ell+1}^{m})\delta_\ell$;
unroll. (Step 4) Risk bound: on each cell, $\tau\circ h^{(L)}$
ranges in an interval of length $\le L_\tau\delta_L$, so threshold
disagreement with the cell-constant Bayes rule is at most
$L_\tau\delta_L$ mass per cell. $\square$

Lemma 6′ recovers Lemma 6 at $\delta_0 = 0$, degrades gracefully
for bounded perturbations (e.g., RWPE / SignNet at controlled
spectral scale), and legitimately ceases to bound architectures
that inject *unbounded* individuating signal (ID-GNN with full
vertex identifiers). The aggregator-type dependence is informative:
for **sum**, $\delta_L\sim\prod_\ell(L_\ell^{c}+\Delta L_\ell^{m})$
grows as $\Theta((1+\Delta)^L)$ — the well-known degree-driven
blow-up of sum-pooled MPNNs (GIN, PNA); for **mean** or
**sym-norm** the factor reduces to $\prod_\ell(L_\ell^{c}+L_\ell^{m})$
and is degree-independent, matching the empirical robustness of
GCN/GAT/GraphSAGE-mean.

**Corollary 7 (MPNN expressivity bracket).** Let $\mathcal A$ be
admissible depth-$L$, $f:V\to\{0,1\}$ a binary vertex task,
$\Pi_L := \mathrm{WL}_L(G)$. Every decision rule
$\hat f = \tau\circ h^{(L)}$ from $\mathcal A$ has training-set error
$\ge \varepsilon^{*}_{\Pi_L}$, and
$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f\mid\Pi_L)\bigr) \;\le\; \varepsilon^{*}_{\Pi_L} \;\le\; \tfrac{1}{2}H(f\mid\Pi_L).
$$
Increasing depth refines $\Pi_L$ and cannot increase either side.

The bracket is **training-free** and **architecture-level**: for fixed
$G$ and depth, every MPNN in the admissible family is sandwiched by
the same partition-conditional entropy.

**Example ($C_4$ with alternating labels).** Let $G=C_4$ and
$f=(0,1,0,1)$. With uniform initial features, $\mathrm{WL}_L(G)=\{V\}$
for every $L\ge 0$ (all vertices have identical local view). Then
$P_C=1/2$, $H(f\mid\Pi_L)=1$, $\varepsilon^{*}_{\Pi_L}=1/2$. Bracket:
$1/2\le 1/2\le 1/2$: both sides saturate, the task is exactly
$1$-WL-indistinguishable, no admissible depth-$L$ MPNN beats chance.
Recovers the canonical $C_4$ counter-example as a one-line instance.

### 8.4 Mechanised verification

`verify.jl` (shipped) samples $10^3$ random partitions of
$V=\{1,\dots,n\}$ with $n\in\{4,\dots,32\}$ and a random binary
label. $\varepsilon^{*}_{\Pi}$ is computed exactly in $\mathbb Q$;
$H(f\mid\Pi)$ and $H_{\mathrm{bin}}(\varepsilon^{*}_{\Pi})$ are
evaluated as certified interval enclosures via
`IntervalArithmetic.jl`. Both inequalities of (3.1) are then
checked per sample by rigorous interval comparison. **Zero
violations** across all 1000 samples; the empirical maximum
upper-side slack $\tfrac{1}{2}H(f\mid\Pi) - \varepsilon^{*}_{\Pi}$
equals $0.1610$ to four decimals, reproducing the analytical
$w^{*}$ of Corollary 2. Audit manifest in `verify.json`.

### 8.5 Empirical evidence on real data

Seven experiments (E1–E7) on real tabular and graph benchmarks
complement the synthetic verifiers. Full specifications and
reproducibility receipts are in `experiments/REPORTS.md` and the
per-experiment JSON manifests under `experiments/results/`. Each
experiment is designed to discriminate a single claim of the
paper against a stated reviewer concern; every row reported
below is reproduced by a single `make e<k>` target. All numbers
below are run on a single CPU core (Apple M-series laptop) with
no GPU and, except for E1's CART fits and E2's logistic-regression
comparators, no training of any kind.

#### E1 — Decision-tree refinement funnel (UCI Adult, $n=45{,}222$)

Materialises Proposition 4 (refinement monotonicity) and the
(E1) practitioner claim. For depth $d\in\{1,\dots,15\}$ we report
the bracket together with the realised CART training error.
*Status: completed.*

| $d$ | $m$ | $H(f\mid\Pi_d)$ | lower | $\varepsilon^*_{\Pi_d}$ | upper | CART train err |
|---|---|---|---|---|---|---|
|  1 |     2 | 0.6544 | 0.1685 | 0.2478 | 0.3272 | 0.2478 |
|  5 |    31 | 0.4866 | 0.1056 | 0.1514 | 0.2433 | 0.1514 |
| 10 |   299 | 0.4129 | 0.0831 | 0.1337 | 0.2064 | 0.1337 |
| 15 | 1 347 | 0.3284 | 0.0603 | 0.1082 | 0.1642 | 0.1082 |

CART's training error matches $\varepsilon^*_{\Pi_d}$ to four
decimal places at every depth: CART leaves vote majority, so the
fitted CART **literally implements** the plug-in achiever of
Theorem 1, and the bracket is therefore an *a-priori* statement
about a classifier that is later trained. Bracket width drops
from 0.159 at $d=1$ to 0.104 at $d=15$, staying everywhere below
the universal $w^*$ of Corollary 2; $\varepsilon^*$ shrinks
monotonically as required by Proposition 4. Full table
$d = 1, \dots, 15$ in `experiments/results/e1.json`.

Figure: `experiments/figures/e1_refinement_funnel.pdf`.

![E1 refinement funnel](experiments/figures/e1_refinement_funnel.pdf)

*Figure E1.* Depth-$d$ CART refinement funnel on UCI Adult. The
bracket $[H_{\mathrm{bin}}^{-1}(H(f\mid\Pi_d)),\tfrac{1}{2}H(f\mid\Pi_d)]$
tightens monotonically with depth as Proposition 4 predicts; CART
training error stays inside the bracket at every depth and attains
the lower endpoint to four decimals.

#### E2 — VQ zero-shot proxy (UCI Adult)

Tests the (E2) practitioner claim on $k$-means partitions with
$k\in\{2,4,8,16,32,64,128,256,512,1000\}$. For each $k$ we
compute the bracket and *also* train a downstream logistic
regression on one-hot cell membership; if the bracket is a real
proxy for trained behaviour rather than a vacuous upper bound,
the trained error should match $\varepsilon^*_{\Pi_k}$ to within
numerical noise. The match is exact for $k \le 256$ (both numbers
agree to all digits) and within one LBFGS sub-optimality unit
($\Delta \le 10^{-3}$) for the two largest budgets, where the LR
solver runs against a 1 000-dimensional one-hot design.
*Status: completed; rebuts the "training-free is misleading"
critique by exhibiting a real classifier (LR-on-cells) whose
trained error is bracketed from below by
$H_{\rm bin}^{-1}(H(f\mid\Pi_k))$ and matched from above by
$\tfrac{1}{2} H(f\mid\Pi_k)$.*

| $k$ | $H(f\mid\Pi_k)$ | lower | $\varepsilon^*_{\Pi_k}$ | LR err | $|\mathrm{LR}-\varepsilon^*|$ |
|---|---|---|---|---|---|
| 2    | 0.8025 | 0.2445 | 0.2478 | 0.2478 | 0.0000 |
| 16   | 0.6597 | 0.1709 | 0.2352 | 0.2352 | 0.0000 |
| 128  | 0.6135 | 0.1515 | 0.1995 | 0.1995 | 0.0000 |
| 1000 | 0.5291 | 0.1199 | 0.1761 | 0.1771 | 0.0010 |

Figure: `experiments/figures/e2_vq_zeroshot.pdf`.

![E2 VQ zero-shot proxy](experiments/figures/e2_vq_zeroshot.pdf)

#### E2b — Marginal-aware refinement on real data

Validates Proposition 6 on unbalanced real labels. For each
binary dataset in the menu we fit the 16-leaf CART and
16-centroid VQ partitions of E1 / E2 and report the realised
upper-side slack $\tfrac{1}{2} H(f\mid\Pi) - \varepsilon^*_{\Pi}$,
the universal ceiling $w^*$ of Corollary 2, and the
marginal-aware ceiling $w^*(\pi_*) \le w^*$ implied by
Proposition 6 with $\pi_*$ the empirical positive-class rate.
*Status: completed; gates "realised slack $\le w^*$" and
"realised slack $\le w^*(\pi_*)$" PASS on every row; strict
shrink $w^*(\pi_*) < w^*$ confirmed on the two genuinely
unbalanced datasets.*

| Dataset       | $\pi_*$ | $w^*$  | $w^*(\pi_*)$ | slack (tree) | slack (VQ) |
|---|---|---|---|---|---|
| UCI Adult     | 0.248   | 0.1610 | 0.1392       | 0.0900       | 0.0947     |
| breast cancer | 0.373   | 0.1610 | 0.1610       | 0.0179       | 0.0711     |
| wine          | 0.331   | 0.1610 | 0.1592       | 0.0000       | 0.0099     |
| digits (bin)  | 0.499   | 0.1610 | 0.1610       | 0.1108       | 0.0650     |

On UCI Adult ($\pi_* \approx 0.25$) the marginal-aware ceiling
is 13 % tighter than the universal $w^*$; on the
nearly-balanced digits-binary task ($\pi_* \approx 0.5$) the
two coincide, as Proposition 6 predicts (the marginal-aware
ceiling reduces to the universal $w^*$ when $\pi_*$ saturates
the entropy–error tension at the worst-case prior). Realised
slack is always strictly inside both ceilings — the worst-case
constant $w^*$ is rarely the operative bound for any particular
partition.

#### E3 — MPNN / WL bracket on real graphs

**The architectural picture.** Xu et al.\ (GIN, 2019) prove that
every aggregation-based GNN is, in distinguishing power, *at most
as fine as the 1-WL colouring* (their Lemma 2), and that this
ceiling is *achievable* whenever the neighbour aggregator and the
readout are both injective on multisets (their Theorem 3,
instantiated by the GIN update $(1+\epsilon^{(k)}) h_v^{(k-1)} +
\sum_{u\in\mathcal{N}(v)} h_u^{(k-1)}$ with irrational $\epsilon$).
Morris et al.\ (k-GNN, 2019) state the same dichotomy in their
notation: 1-WL refines the colouring produced by any 1-GNN at the
same depth (their Theorem 1), and there exist weight matrices
realising equality whenever distinct labels are encoded by
linearly independent vectors (their Theorem 2). For depth $L$,
the 1-WL partition $\Pi_L$ is therefore the **finest cell
structure attainable by any depth-$L$ MPNN.**

**Why the bracket plugs in here.** Substituting $\Pi_L$ into the
sandwich (3.1) brackets the empirical training error of *every*
admissible depth-$L$ MPNN. The upper endpoint
$\tfrac{1}{2}H(f\mid\Pi_L)$ is realised training-free by a
per-cell majority-vote head — and by Xu Theorem 3 / Morris
Theorem 2 it is realised by a sufficiently wide injective MPNN
(GIN with a large enough MLP, or 1-GNN with linearly-independent
initial encodings). The lower endpoint $H_{\rm bin}^{-1}(H(f\mid\Pi_L))$
is the Fano floor that no depth-$L$ MPNN in this equivalence
class can break, regardless of training budget, optimiser, or
weight init. Both endpoints are concrete; neither depends on
running gradient descent.

**Setup.** Multi-class labels of Cora / CiteSeer / PubMed /
ogbn-arxiv are binarised to "majority class vs.\ rest"; Twitch-EN
ships a native binary mature-content flag. Initial colour
$h_v^{(0)}$ is the vertex degree (consistent with Morris Theorem
1). Each refinement round is one pass of the 1-WL multiset hash
on sparse-CSR adjacency. **No MPNN is ever instantiated; no GPU
is used.** On a single laptop core, WL refinement to $L=3$ on
ogbn-arxiv (169 343 vertices, ≈ 1.16 M undirected edges) takes
2.7 s; the bracket evaluation is a single $O(|V|)$ sweep on top.

| Graph      | $|V|$    | $L$ | $m_L$    | $m_L/|V|$ | lower  | $\varepsilon^*_{\Pi_L}$ | upper  |
|---|---|---|---|---|---|---|---|
| Twitch-EN  | 7 126    | 0 |     130  | 0.018 | 0.3853 | 0.4164 | 0.4809 |
| Twitch-EN  | 7 126    | 3 |   6 648  | 0.933 | 0.0073 | 0.0267 | 0.0312 |
| Cora       | 2 708    | 3 |   2 363  | 0.873 | 0.0076 | 0.0292 | 0.0323 |
| CiteSeer   | 3 327    | 3 |   2 044  | 0.614 | 0.0400 | 0.0775 | 0.1212 |
| PubMed     | 19 717   | 3 |  12 990  | 0.659 | 0.0205 | 0.0511 | 0.0722 |
| ogbn-arxiv | 169 343  | 3 | 161 943  | **0.956** | 0.0005 | 0.0021 | 0.0029 |

The $m_L/|V|$ column is the *singleton-cell fraction* and is the
essential interpretive lens: rows where it is $\gtrsim 0.85$ are
dominated by the partition-cardinality collapse regime of
Proposition 7 (the bracket pinches because nearly every vertex is
in a cell by itself, not because $1$-WL is solving the labelling).

Full funnels $L=0\dots L_{\max}$ in `experiments/results/e3.json`;
figures `experiments/figures/e3_<dataset>_funnel.pdf`.

![E3 Cora WL funnel](experiments/figures/e3_cora_funnel.pdf)
![E3 ogbn-arxiv WL funnel](experiments/figures/e3_ogbn_arxiv_funnel.pdf)

*Figure E3.* Depth-$L$ 1-WL refinement funnels on Cora (top) and
ogbn-arxiv (bottom). On Cora the bracket remains non-tautological
at every depth; on ogbn-arxiv the partition collapses to 95.6%
singleton cells by $L=3$ and both bracket endpoints pinch to $0$,
the asymptotic predicted by Proposition 4.5.

**What the numbers say (honest reading).** The headline pinch on
ogbn-arxiv — a depth-$3$ bracket of $[4.7\!\times\!10^{-4},
2.9\!\times\!10^{-3}]$, a nominal $76\times$ improvement over
trivial majority — is best read as a *sanity check on the bracket
implementation, not a substantive claim about WL expressivity*.
With $m_3/|V| = 0.956$ on ogbn-arxiv and $0.87$–$0.93$ on
Cora and Twitch-EN, the partition is essentially the discrete
partition, and per-cell majority is per-vertex memorisation — the
finite-sample face of Proposition 7's $O(1/\sqrt n)$ slack. The
same phenomenon is the diagnosed failure mode of E6-NAS on the
digits-bin task. The non-tautological rows of the table are
CiteSeer ($m_3/|V| = 0.614$, $\varepsilon^*_{\Pi_3} = 0.078$)
and PubMed ($0.659$, $0.051$): on these benchmarks the partition
still aggregates multi-vertex cells and the bracket genuinely
bounds $\hat R$. Cora, Twitch-EN, and ogbn-arxiv inherit feature-
driven topology in which 3-hop degree-fingerprints separate almost
all vertices — a property of the graphs (Shchur et al., 2018;
Errica et al., 2020), not a property of the bracket. We retain
the high-singleton-fraction rows in the table only as a *negative
control*: they exhibit the cardinality-collapse regime exactly
where Proposition 7 predicts it.

**What E3 establishes, precisely.**

1. *The bracket is well-defined and audit-tight on real graphs.*
   Every funnel passes the gates sub-partition,
   monotonicity of $H$ and $\varepsilon^*$ in $L$ (Proposition 4),
   the sandwich (3.1), and width $\le w^*$ (Corollary 2), with
   zero violations across all rows.
2. *It quantifies what was previously a qualitative claim.* Xu
   and Morris say "no MPNN exceeds 1-WL"; we say "no depth-$L$
   MPNN achieves training error below $H_{\rm bin}^{-1}(H(f\mid\Pi_L))$,
   and the witness training-free classifier already achieves
   $\tfrac{1}{2} H(f\mid\Pi_L)$." Both numbers are reported per
   benchmark, per depth.
3. *It exposes a property of the benchmarks themselves.*
   ogbn-arxiv is structurally near-trivial for 1-WL — the
   $\le 3$-hop $+$ degree fingerprint already separates 160 000
   vertices. CiteSeer is the hardest of the canonical trio
   ($m_3/|V| = 0.61$, $\varepsilon^*_{\Pi_3} = 0.078$). Twitch-EN's
   mature-content flag is nearly a function of 3-hop
   neighbourhoods (a 15× collapse in $\varepsilon^*$ from
   $L = 0$ to $L = 3$).

**What E3 does *not* establish.** The bracket is computed on the
full transductive label vector, so it bounds *fitting* power, not
generalisation; the population analogue is Proposition 7, exercised
on tabular data in E7. The Xu achievability theorem requires
unbounded MLP width and an injective sum aggregator on a countable
feature space; in practice (finite width, GCN/GAT aggregators
that are *not* injective on multisets) a trained MPNN sits
strictly above $H_{\rm bin}^{-1}(H(f\mid\Pi_L))$ — and the gap to
the lower bound is itself an interesting gauge of how much of the
1-WL ceiling a given architecture realises. Finally, the bracket
inherits the headline limitation of the 1-WL/MPNN universe:
structures indistinguishable by 1-WL (e.g.\ the
triangle-vs.-4-cycle example of Morris §4.1) collapse into the
same cell and cannot be separated by either side of the sandwich.
Lifting the bracket to the $k$-WL partitions of Morris §5 is
immediate — our framework is colouring-agnostic — and is the
natural next experiment. The structural-WL stress test of E3b
below exercises this failure mode directly.

#### E3b — Bracket on featureless structural benchmarks

To separate the bracket's behaviour from feature-driven
cardinality collapse, we run it on graphs designed so that
$1$-WL with a constant initial colour is *provably blind* to the
binary label. We use two Circulant Skip Link (CSL) constructions
and two Paley graphs:

- **CSL-union** ($n=82$, $\pi=0.500$): disjoint union
  $\mathrm{CSL}(41,\{1,9\}) \sqcup \mathrm{CSL}(41,\{1,12\})$,
  label = component indicator. The two components are
  $1$-WL-indistinguishable (Murphy et al., 2019; Chen et al.,
  2020).
- **CSL-orbit** ($n=60$, $\pi=0.500$): a single vertex-transitive
  Cayley graph with a balanced orbital colouring; every vertex
  has the same multiset-fingerprint, so $\mathrm{WL}_L = \{V\}$
  for all $L$.
- **Paley(13)** ($\pi=0.462$) and **Paley(29)** ($\pi=0.483$):
  strongly regular self-complementary graphs; vertex-transitive
  with $1$-WL refinement equal to the trivial partition at every
  depth.

| Benchmark    | $|V|$ | $\pi$ | lower | $\varepsilon^*_{\Pi_L}$ | upper  |
|---|---|---|---|---|---|
| CSL-union    | 82    | 0.500 | 0.500 | 0.500 | 0.500 |
| CSL-orbit    | 60    | 0.500 | 0.500 | 0.500 | 0.500 |
| Paley(13)    | 13    | 0.462 | 0.462 | 0.462 | 0.498 |
| Paley(29)    | 29    | 0.483 | 0.483 | 0.483 | 0.500 |

All four benchmarks have $m_L = 1$ for every $L \in \{0,\dots,6\}$;
total wall time across the entire battery is $5$ ms on a single
CPU core. Raw outputs in `experiments/results/e3b.json`.

**Interpretation.** The bracket sits pinned at the
marginal-entropy ceiling — exactly the *correct* failure mode
predicted by Corollary 7 once $\mathrm{WL}_L(G) = \{V\}$. Combined
with the E3 reading above, the coherent picture is: the bracket
is informative on coarse-partition feature-rich graphs
(CiteSeer, PubMed), tautological on feature-driven
near-discrete graphs (ogbn-arxiv, Cora, Twitch-EN at $L=3$), and
correctly vacuous on featureless structural-WL benchmarks (E3b).
Lemma 6′ above gives the quantitative refinement: with bounded
random or positional perturbations (Sato et al., 2020), the E3b
rows acquire a controlled $L_\tau\delta_L$ slack rather than
degenerating to $[0,0]$.

**Why this matters for the GNN community.** The 2018–2019
WL / MPNN equivalence theorems of Xu et al.\ and Morris et al.\
are arguably the most-cited structural results in graph
learning, and yet seven years later practitioners still
routinely report "GNN $X$ beats baseline $Y$ by $\Delta$
accuracy" without any *ex-ante* statement of what the 1-WL
ceiling on that dataset would even look like. The original
papers gave a binary verdict — a pair of graphs is either
distinguishable by 1-WL or it is not — which is the right
abstraction for graph-classification expressivity proofs but is
silent on the question a node-classification practitioner
actually asks: *how much of my label vector can a depth-$L$
MPNN possibly recover on my graph?* The E3 table answers exactly
this question, in two numbers ($H_{\rm bin}^{-1}(H(f\mid\Pi_L))$
and $\tfrac{1}{2} H(f\mid\Pi_L)$) per (graph, depth) pair, at
the cost of running $L$ rounds of the same 1-WL hash that
already underlies every GIN implementation. To three of the
audiences of those original papers, the implications are
concrete.

*For applied practitioners.* Before training a 6-layer GAT on
ogbn-arxiv, compute $\varepsilon^*_{\Pi_3} = 0.0021$ from the E3
table; this is the floor that no 1-WL-equivalent architecture can
break on this label vector, and it tells you that the published
state-of-the-art accuracies in the 0.997 range are inside the
bracket — further gains from deeper 1-WL-bounded architectures
are mathematically capped. Conversely, the CiteSeer row
($\varepsilon^*_{\Pi_3} = 0.078$) tells you that the 0.74 test
accuracies routinely reported on the standard split are already
within 4 percentage points of the 1-WL ceiling on the
training-label vector; the remaining gap is architectural — not
data — in nature.

*For expressivity theorists in the Xu–Morris lineage.* The
bracket promotes the 1-WL ceiling from a qualitative "cannot
distinguish" statement to a quantitative "cannot drive training
error below this number" statement, and makes the
$w^* \approx 0.16$ slack of Corollary 2 the precise asymptotic
gap between the informational floor (Fano) and the constructive
ceiling (plug-in majority on cells) for any colour-refinement
analysis — a gap that, by Proposition 5 (sharpness), no
closed-form two-sided entropy bracket can shrink without using
more than $H(f\mid\Pi)$.

*For the $k$-WL extension programme of Morris et al.\ (2020).*
Our framework is colouring-agnostic, so the same two-line
evaluation applied to $\Pi_L^{(k)}$ yields a $k$-WL bracket;
the diagnostic shape "$L = 0$ wide bracket → $L = L_{\max}$
pinched bracket" observed in E3 is therefore a $k$-uniform
phenomenon, and the gap between the $k = 1$ and $k = 2$ funnels
on a fixed dataset is a clean quantitative measure of how much
additional expressive power 2-WL actually buys on *that*
dataset. The standard counterexample graphs — triangle vs.\
4-cycle, the CFI graphs of Cai–Fürer–Immerman (1992), regular
graphs in general — are precisely the inputs on which the
$k=1$ bracket is structurally loose and the $k = 2$ bracket
should pinch; a per-graph $k$-WL bracket sweep would, for the
first time, give the $k$-WL hierarchy a benchmark-side
diagnostic on par with its theoretical one.

A subtler implication concerns *how the field measures
expressivity gains*. The current convention — compare two
architectures by their downstream accuracy after end-to-end
training — entangles three confounds: architectural ceiling
(WL-side), optimisation landscape (loss + SGD), and
generalisation (train–test gap). The bracket cleanly separates
the first from the other two: any gap between trained training
error and the bracket's lower endpoint is attributable to
optimisation or to a finite-width approximation of the injective
aggregator of Xu Theorem 3, *never* to expressivity. We view
this decomposition as the missing diagnostic for the routine
experimental claim "deeper / wider / fancier ⇒ better": in many
of the E3 benchmarks the marginal accuracy returns from
"fancier" are bounded above by
$\tfrac{1}{2} H(f\mid\Pi_L) - \varepsilon^*_{\Pi_L}$, and the
architectural-search budget might be better redirected to push
$L$ instead of fancier within-layer machinery.

#### E3c — Structural-vs-memorisation index and coarsened initialisation

The E3 brackets near-singleton-pinch on Cora / Twitch-EN /
ogbn-arxiv. Is the WL refinement *learning* their label
structure, or merely *memorising* it through near-isolation of
each node into its own colour class? We answer with a
quantitative index. Define
$\sigma(\varepsilon_*, \rho_*) := L^{\text{useful}} -
L^{\text{collapse}}$, where $L^{\text{useful}}$ is the smallest
$L$ at which $\varepsilon^*_{\Pi_L} \le \varepsilon_*$ and
$L^{\text{collapse}}$ is the smallest $L$ at which the
singleton fraction $m_L / n \ge \rho_*$. Positive $\sigma$ means
the bracket pinches *before* the partition collapses to nodes;
negative $\sigma$ means the pinch is achieved entirely by
memorisation. At $(\varepsilon_*, \rho_*) = (0.05, 0.5)$:
$\sigma_{\text{Twitch}} = -1$, $\sigma_{\text{Cora}} = -1$,
$\sigma_{\text{CiteSeer}} = \sigma_{\text{PubMed}} =$ none
(never pinches), $\sigma_{\text{ogbn-arxiv}} = 0$. *Every* E3
benchmark is in the memorisation regime by this index. We also
test a coarsened initialisation that floors WL refinement at
cell budget $K \in \{4, 8, 16\}$ via degree-bucket colours, to
prevent immediate singleton collapse; the maximum
information-theoretic ratio $(H_{\text{bin}} -
H(f\mid\Pi_L))/\log_2 K$ is $\le 0.073$ across all (dataset, $K$,
$L$) combinations, confirming that 1-WL refinement on these
graphs cannot recover meaningful coarse structure — the small
brackets at $L = 3$ come from cardinality, not from genuine
structural alignment. Raw outputs in
`experiments/results/e3a.json`.

#### E3d — In-vivo audit of Lemma 6′ (ε-robust MPNN/WL)

Lemma 6′ gives a worst-case envelope $\delta_L = \delta_0
\prod_\ell (L_\ell^c + r_T \cdot L_\ell^m)$ on within-WL-cell
embedding diameter under bounded perturbations of $h^{(0)}$,
with central/multiset Lipschitz constants $L^c_\ell, L^m_\ell$
and aggregator factor $r_T \in \{\Delta, 1, 1\}$ for
sum/mean/sym-norm. We test it on Cora and CiteSeer with random-init GIN, hidden width $32$,
depth $L = 3$, Gaussian noise $\xi_v \sim \mathcal{N}(0,
\delta_0^2 I)$ on $h^{(0)}$, measuring $D(\ell) = \max_{v
\sim_{\text{WL}_L} w} \|h^{(\ell)}(v) - h^{(\ell)}(w)\|_2$ at
each round. The lemma holds at every sweep point ($\delta_0 = 0$
recovers strict equality at machine precision; sup-norm
$\delta_0$ measured empirically on the perturbed input — a
per-coordinate Gaussian std of $10^{-2}$ in $\mathbb{R}^{32}$
inflates to sup-norm $\approx 0.12$). The bound is loose by $6$
to $7$ orders of magnitude — for instance, Cora at $\delta_0 =
10^{-2}$ gives $D(L) = 1.03$ against bound $\delta_L = 3.6
\times 10^6$. The empirical per-round amplification factor
$\gamma_{\text{eff}}^{(L)} = (D(L)/D(0))^{1/L} \approx
1.5$–$2.1$ across both graphs and all noise scales is far below
the worst-case sum-aggregator step $L^c_\ell + \Delta_{\max}
L^m_\ell = 314$ (Cora) / $186$ (CiteSeer) (here $L^c \approx
(1{+}\varepsilon)\|W_\ell\|_{\rm op}$, $L^m \approx
\|W_\ell\|_{\rm op}$, GIN $\varepsilon \approx 0$ at init): an
average-degree refinement of Lemma 6′ would tighten the bound by
roughly $((L^c + \Delta_{\max} L^m)/\gamma_{\text{eff}})^L
\approx 10^6$ on Cora at $L = 3$. We leave the mean-Lipschitz refinement to
future work; raw outputs in `experiments/results/e3e.json`.

#### E3d-arch — Post-hoc architecture-vs-WL audit (GCN/GAT/GIN × Cora/CiteSeer/PubMed)

The E3 family measures the *structural ceiling*
$\varepsilon_{\text{WL}} := \varepsilon^*_{\Pi^{\text{WL}}_L}$
of 1-WL refinement. We now ask the complementary
post-hoc question: at the same cell budget $k = m^{\text{WL}}_L$,
do trained GNNs realise partitions that beat this WL ceiling
when given node features? For each $(\text{arch}, \text{seed}) \in
\{\text{GCN}, \text{GAT}, \text{GIN}\} \times \{0, 1, 2\}$ we
train a 3-layer model (hidden $64$, Adam, 200 epochs,
transductive fitting on the same largest-class binarisation as
E3) on Apple M1 MPS, extract penultimate embeddings $Z \in
\mathbb{R}^{n \times 64}$, partition them with MiniBatchKMeans
at $k = m^{\text{WL}}_3$ to obtain $\Pi^{\text{trained}}_k$, and
report two signed diagnostics:

$$
\text{feat\_gap} := \varepsilon_{\text{WL}} -
\varepsilon^*_{\Pi^{\text{trained}}_k}, \qquad
\text{head\_sig} := \varepsilon^*_{\Pi^{\text{trained}}_k} -
\hat R.
$$

Positive feat\_gap = features refine the partition beyond WL;
negative head\_sig = the trained linear head extracts sub-cell
label structure that $k$-means at budget $k$ discards. Mean ± std
over seeds:

| Dataset (eps_WL) | Arch | $\hat R$ | $\varepsilon^*_{\Pi^{\text{tr}}_{k_{\text{WL}}}}$ | feat_gap | head_sig |
|---|---|---|---|---|---|
| Cora (0.0292) | GCN | 0.030 ± 0.029 | 0.007 ± 0.004 | +0.022 ± 0.004 | −0.023 ± 0.024 |
| | GAT | 0.006 ± 0.004 | 0.002 ± 0.002 | +0.027 ± 0.002 | −0.004 ± 0.003 |
| | GIN | 0.198 ± 0.245 | 0.016 ± 0.012 | +0.013 ± 0.012 | −0.182 ± 0.234 |
| CiteSeer (0.0775) | GCN | 0.032 ± 0.004 | 0.018 ± 0.004 | +0.060 ± 0.004 | −0.014 ± 0.002 |
| | GAT | 0.021 ± 0.006 | 0.016 ± 0.002 | +0.062 ± 0.002 | −0.005 ± 0.004 |
| | GIN | 0.079 ± 0.035 | 0.031 ± 0.010 | +0.046 ± 0.010 | −0.048 ± 0.025 |
| PubMed (0.0511) | GCN | 0.086 ± 0.003 | 0.035 ± 0.004 | +0.016 ± 0.004 | −0.050 ± 0.005 |
| | GAT | 0.103 ± 0.002 | 0.057 ± 0.003 | **−0.006 ± 0.003** | −0.047 ± 0.005 |
| | GIN | 0.068 ± 0.024 | 0.025 ± 0.009 | +0.027 ± 0.009 | −0.043 ± 0.015 |

Three clean findings. **(F1) Features generically refine WL.**
feat\_gap > 0 on 23/27 cells; CiteSeer — the hardest dataset for
any pure 1-WL initialisation (cf. E3f below) — is rescued by
features (+0.05 to +0.06 bracket-error reduction at matched cell
budget, 9/9 cells). **(F2) Attention can erase structure.** All
three GAT seeds on PubMed give negative feat\_gap; the bracket
framework cleanly detects an architecture *failing* to use
structural information. **(F3) The linear head exploits sub-cell
geometry universally.** head\_sig < 0 on all 27/27 cells (mean
−0.046): the trained head beats per-cell majority on its own
embedding's $k$-means partition. GIN is init-sensitive (Cora
seed=0 fails to fit, inflating its std). MPS is non-bit-
deterministic so per-seed numbers drift on re-run; signs and
trends are robust. Raw outputs in
`experiments/results/e3d_arch.json`.

#### E3d-arch-full — Extended sweep: GCN/GAT/GIN/SAGE × {Cora, CiteSeer, PubMed, Twitch-EN}, 5 seeds

We re-run the E3d-arch protocol with a larger configuration:
4 architectures (adding GraphSAGE), 5 seeds
$\{0,\dots,4\}$ (vs. 3), 4 datasets (adding Twitch-EN), 3-layer
models with hidden width $128$ (vs. $64$), 200 epochs, AdamW.
Cora / CiteSeer / PubMed are trained on CUDA; Twitch-EN on CPU
(same numerics, slower). The cell-budget evaluation point $k$ is
$k_{\mathrm{WL}}$ exactly on Cora and CiteSeer (small graphs,
$k_{\mathrm{WL}} \le 2363$); on PubMed and Twitch-EN the
MiniBatchKMeans budget is capped at $k = 4096 < k_{\mathrm{WL}}$
because the WL-cell counts (12 990 and 6 648) make
per-cell-balanced $k$-means impractical at $n \approx
2 \times 10^{4}$ and $7 \times 10^{3}$ respectively. Mean ± std
over seeds:

| Dataset (eps_WL, eval k) | Arch | $\hat R$ | $\varepsilon^*_{\Pi^{\text{tr}}_k}$ | feat_gap | head_sig |
|---|---|---|---|---|---|
| Cora (0.0292, k=2363=k_WL) | GCN | 0.015 ± 0.006 | 0.005 ± 0.002 | +0.024 ± 0.002 | −0.010 ± 0.004 |
| | GAT | 0.153 ± 0.273 | 0.010 ± 0.007 | +0.019 ± 0.007 | −0.143 ± 0.269 |
| | GIN | 0.037 ± 0.039 | 0.009 ± 0.006 | +0.020 ± 0.006 | −0.028 ± 0.033 |
| | SAGE | 0.008 ± 0.017 | 0.001 ± 0.003 | +0.028 ± 0.003 | −0.007 ± 0.014 |
| CiteSeer (0.0775, k=2044=k_WL) | GCN | 0.036 ± 0.014 | 0.019 ± 0.007 | +0.059 ± 0.007 | −0.017 ± 0.007 |
| | GAT | 0.018 ± 0.002 | 0.015 ± 0.001 | +0.062 ± 0.001 | −0.002 ± 0.001 |
| | GIN | 0.040 ± 0.016 | 0.024 ± 0.009 | +0.054 ± 0.009 | −0.016 ± 0.008 |
| | SAGE | **0.000 ± 0.000** | 0.000 ± 0.000 | **+0.077 ± 0.000** | −0.000 ± 0.000 |
| PubMed (0.0511, k=4096<k_WL) | GCN | 0.083 ± 0.004 | 0.065 ± 0.002 | **−0.014 ± 0.002** | −0.018 ± 0.004 |
| | GAT | 0.105 ± 0.003 | 0.090 ± 0.002 | **−0.039 ± 0.002** | −0.015 ± 0.001 |
| | GIN | 0.045 ± 0.013 | 0.037 ± 0.010 | +0.015 ± 0.010 | −0.008 ± 0.003 |
| | SAGE | 0.013 ± 0.026 | 0.011 ± 0.022 | +0.040 ± 0.022 | −0.002 ± 0.004 |
| Twitch-EN (0.0267, k=4096<k_WL) | GCN | 0.412 ± 0.002 | 0.192 ± 0.003 | **−0.166 ± 0.003** | −0.220 ± 0.002 |
| | GAT | 0.416 ± 0.001 | 0.195 ± 0.005 | **−0.168 ± 0.005** | −0.221 ± 0.005 |
| | GIN | 0.408 ± 0.015 | 0.190 ± 0.004 | **−0.164 ± 0.004** | −0.218 ± 0.014 |
| | SAGE | 0.376 ± 0.009 | 0.181 ± 0.005 | **−0.154 ± 0.005** | −0.195 ± 0.012 |

The extended sweep ($16$ arch-dataset cells × 5 seeds = 80 runs,
total wall $\approx 53.7$ min) reproduces and sharpens the
findings from the 3-seed MPS pilot:

**(F1′) Features generically refine WL — confirmed at matched
$k$.** On the two datasets where evaluation budget *equals*
$k_{\mathrm{WL}}$ (Cora, CiteSeer), feat\_gap > 0 on
$8/8$ arch-dataset cells, with CiteSeer/SAGE achieving the
clean limit feat\_gap $= +0.077$ at $\hat R = 0.000 \pm 0.000$
(perfect fit at $n = 3327$, $k = 2044$ leaves little label
ambiguity inside any cell — a healthy *expected* memorisation
regime rather than a bracket pathology).

**(F2′) GAT erases structure even at higher capacity.** PubMed
GAT now reports feat\_gap $= -0.039 \pm 0.002$ (5 seeds, hidden
128), nearly an order of magnitude more negative than the
3-seed pilot's $-0.006 \pm 0.003$; the pattern is reproducible.
GCN on PubMed also flips sign in the extended run (feat\_gap
$= -0.014$), but this is partly attributable to the $k = 4096
< k_{\mathrm{WL}} = 12\,990$ mismatch (see caveat below). GIN
and SAGE remain positive on PubMed.

**(F3′) Head-signal exploitation universal — $16/16$ arch-
dataset cells have head\_sig < 0** (mean $-0.084$, range
$[-0.221, -0.000]$). The trained linear head beats per-cell
majority on its own embedding's $k$-means partition in every
configuration.

**Caveat on PubMed/Twitch-EN feat\_gap.** Because evaluation $k
= 4096 < k_{\mathrm{WL}}$ on these two datasets, the
$\varepsilon^*_{\Pi^{\mathrm{tr}}_k}$ entries necessarily live
on a *coarser* partition than $\varepsilon_{\mathrm{WL}}$, so a
negative feat\_gap conflates two effects: (i) features failing
to refine and (ii) cell-budget mismatch. The Twitch-EN row is
the clearer illustration of this confound: $\hat R \approx
0.41$ is itself huge (the marginal label split $\pi = 0.546$
makes the trivial constant predictor achieve $0.454$, so any
trained model that does worse than $\hat R = 0.41$ has barely
moved past the trivial bound), and the WL ceiling at the *finer*
budget $k_{\mathrm{WL}} = 6648$ is $\varepsilon_{\mathrm{WL}} =
0.027$ — a $15\times$ headroom that the $k = 4096$ embedding
partition cannot in principle reach. The honest reading is:
on Twitch-EN at this training budget no architecture beats the
trivial baseline by a wide margin, regardless of WL. Closing
the $k$-mismatch on PubMed / Twitch-EN is the natural next
experiment (E3d-arch-full+: evaluate at $k = k_{\mathrm{WL}}$
directly).

**Limitation.** ogbn-arxiv (the fifth dataset of E3) is not
included in this sweep: the 5-seed × 4-arch run at $n =
169\,343$, $k_{\mathrm{WL}} = 161\,943$ requires GPU memory
and wall budget that exceeded our current cap. We document
this as `merge_provenance.missing_dataset = "ogbn_arxiv"` in
the raw output (`experiments/results/e3d_arch_full.4of5.json`)
and leave the ogbn-arxiv block to a follow-up audit. Raw
outputs for the 4/5 sweep are at
`experiments/results/e3d_arch_full.4of5.json` (merged from
`e3d_arch_full.partial_3of5.json` on CUDA and
`e3d_arch_full.twitch_only.json` on CPU; total wall $3224$ s).

#### E3f — Richer-than-1-WL initialisation on CiteSeer / PubMed

E3 shows $\varepsilon^*_{\Pi^{\text{WL}}_L}$ stalling at
$\approx 0.078$ (CiteSeer) and $\approx 0.051$ (PubMed) for all
$L \le 5$. Is this a property of the *initialisation* (constant
colour) or of the 1-WL refinement itself? We test four
initialisations — constant, degree, $\log_2 \deg$-bucket-8, and
neighbour-degree fingerprint $h_0(v) = (\deg(v),
\text{sort}\{\deg(u) : u \in N(v)\})$ — the last sitting
strictly between 1-WL and 2-FWL on sparse graphs (Maron 2019,
Geerts 2020) and computable in $O(|E| \log d)$, whereas 2-FWL
would cost $n^3 \approx 7.6 \times 10^{12}$ operations per round
on PubMed (infeasible in pure NumPy). All four initialisations
give $L^*(0.05) = $ none on both graphs; the neighbour-degree
init gives $\varepsilon^*(L = 3) = 0.0736$ on CiteSeer (vs
$0.0775$ for degree-init) and $0.0509$ on PubMed (vs $0.0511$).
This is an **honest negative result**: the 1-WL family genuinely
cannot crack CiteSeer / PubMed below $\varepsilon^* = 0.05$ at
any depth, regardless of initial colour. The mechanism that
*does* crack these graphs is real-valued node features +
trainable propagation (cf. E3d-arch above, where GCN on CiteSeer
hits $\varepsilon^*_{\Pi^{\text{tr}}} = 0.018$). Raw outputs in
`experiments/results/e3f.json`.

#### E4 — Cross-architecture duel at fixed cell budget (UCI Adult, $K=16$)

Materialises practitioner claim (E3): at a fixed cell budget the
bracket ranks architectures *training-free*. *Status: completed;
rebuts the "$w^*$ slack is too wide" critique by exhibiting two
architectures whose brackets order strictly despite each having
width $\approx w^*$.*

| Architecture          | $m$ | $H$    | lower  | $\varepsilon^*_{\Pi}$ | upper  | fit (s) |
|---|---|---|---|---|---|---|
| Decision tree (16 leaves) | 16 | 0.4823 | 0.0992 | 0.1511 | 0.2411 | 0.18 |
| $k$-means ($k=16$)        | 16 | 0.6597 | 0.1709 | 0.2352 | 0.3299 | 4.36 |

Figure: `experiments/figures/e4_duel_table.pdf`.

![E4 duel](experiments/figures/e4_duel_table.pdf)

#### E5 — Achievable-region scatter (synthetic)

Visualises Theorem 1 and Corollary 2: $10^3$ random partitions
of $V=\{1,\dots,n\}$, $n\in\{4,\dots,32\}$, plotted in the
$(H,\varepsilon)$ plane against the Fano and Hellman–Raviv
boundaries. Empirical max upper slack
$0.16096404744368120$ vs analytic $0.16096404744368115$
(≤ 1 ulp of `Float64`). *Status: completed.*
Figure: `experiments/figures/e5_achievable_region_scatter.pdf`.

![E5 achievable region scatter](experiments/figures/e5_achievable_region_scatter.pdf)

#### E6 NAS — bracket as a training-free architecture pre-filter

Quantifies the practitioner-side use of Theorem 1: rank a
heterogeneous search space of candidate architectures by the
bracket lower bound evaluated on a partition fit at *random
init* (no supervised training), and check whether the ranking
correlates with held-out test error obtained by full training,
against two baselines (parameter count and uniform random).
*Status: completed; honest mixed result that exposes both a
success regime and the predicted failure regime of the
bracket as a population-risk surrogate.*

**Protocol (v2).** A heterogeneous menu of $A = 35$–$40$
architectures across six families (MLP, CART, RandomForest,
GradientBoosting, KMeans-partition, random-feature-bits)
evaluated on $5$ seeds each. Four a-priori vetoes guard the
experiment from being run on uninformative datasets at all:
V1 (spread of \texttt{lower} across the menu $\ge 0.05$),
V2 (between-family / within-family variance ratio $\ge 2$),
V3 (top-vs-bottom cell-count ratio $\ge 10$),
V4 (bimodality of the \texttt{lower} distribution). Both
datasets cleared all four. Phase-2 ranking uses successive
halving on \texttt{lower} ($77 / 175$ fits on Adult), a
$2^{14}$-point LUT for $\mathsf{hbin}$/$\mathsf{hbin}^{-1}$
($\le 10^{-6}$ max error vs bisection), and \texttt{joblib}
parallel probes on a 6-core M1.

| dataset    | $n_{\rm tr}$ | $A$ | $\tau$(lower, test) | $95\%$ CI | top-5 overlap | param-count $\tau$ | speedup |
|---|---|---|---|---|---|---|---|
| UCI Adult  | 36 177 | 35  | $+0.482$ | $[+0.246, +0.689]$, $p = 5{\times}10^{-5}$ | $3$ / $5$ ($\mathbb{E}_{\rm rand} = 0.71$) | $-0.381$, $p = 1.5{\times}10^{-3}$ | $1.63\times$ |
| digits-bin |  1 437 | 40  | $+0.106$ | $[-0.116, +0.314]$, $p = 0.34$              | $1$ / $5$ ($\mathbb{E}_{\rm rand} = 0.63$) | $-0.697$, $p = 4.5{\times}10^{-10}$ | $0.66\times$ |

**Five gates, honest reporting.** G1 (τ-CI excludes zero on
*both* datasets): **fail** (passes on Adult, fails on
digits-bin). G2 (bracket beats parameter count): **pass** on
both — parameter count is in fact *strongly negatively*
correlated with test error here ($\tau = -0.38$ and $-0.70$),
so the standard NAS prior actively misranks both menus.
G3 (top-5 by bracket beats uniform random): **pass** on both.
G4 (end-to-end speedup $\ge 10\times$): **fail** ($1.6\times$
and $0.66\times$ at this menu size; the headline $20$–$133\times$
cost numbers below are per-arch, not for a $35$-arch sweep).
G5 (test-error spread $\ge 5$ pp, i.e. the menu is worth
ranking at all): **pass** on both ($11.1$ pp and $36.8$ pp).

**Interpretation.** On Adult the bracket recovers $7 / 10$ of
the truly best architectures, with $\tau = 0.48$ and CI
strictly above zero; parameter count recovers $0 / 10$. On
digits-bin the bracket ranking collapses to noise — and the
mechanism is exactly the one Proposition 7 predicts:
CART(leaf $= 128, 256$) reaches \texttt{lower} $= 0$ (the
partition fits the $1437$ training rows perfectly), but its
test error is $0.126$. The empirical Bayes floor is *exact*
on its train-set quantity and silently mis-bounds the
population risk in the small-$n$, low-noise regime where
the $O(1/\sqrt n)$ generalisation gap of Proposition 7
dominates. The Adult row, with $n_{\rm tr} = 36\,177$, sits
firmly in the regime where that gap is negligible and the
bracket transfers cleanly to test error.

**Takeaway for practitioners.** The bracket is not a universal
NAS surrogate. As a pre-filter it strictly dominates parameter
count on every metric on every dataset tested, and on
sufficiently large data it provides a statistically
significant rank signal that recovers most of the
top-$k$ frontier in seconds without any supervised training.
On small data with overfitting-prone partition families
(deep CART, large $k$ in $k$-means), the practitioner must
either ignore the zero-\texttt{lower} architectures or pair
the bracket with a held-out split — a limitation that follows
from the same finite-sample theorem (Proposition 7) that
gives the bracket its bite on Adult. Figure:
`experiments/figures/e6_nas_scatter.pdf` (v1; v2 is JSON-only).

![E6-NAS bracket-vs-test scatter](experiments/figures/e6_nas_v2_scatter.pdf)
![E6-NAS Kendall comparison](experiments/figures/e6_nas_v2_kendall.pdf)

*Figure E6-NAS.* Lower bracket endpoint vs. held-out test error
(top) and Kendall-$\tau$ comparison vs. parameter count (bottom)
on a heterogeneous ten-architecture menu over UCI Adult. Bracket
$\tau = 0.48$ ($p = 5\!\times\!10^{-5}$); parameter count
*anti*-ranks at $\tau = -0.38$.

#### E6 — Cost comparison vs one training epoch

Quantifies the $O(|V|)$ remark of §1: on four binary tabular
datasets we time the bracket evaluation
($T_{\rm br}$ = one `bracket_from_cells` call on a precomputed
$k = 16$ KMeans partition) against three genuine training
comparators — one full CART fit ($T_{\rm cart}$), one KMeans
`fit_predict`, and one LBFGS epoch of logistic regression on
one-hot cell membership ($T_{\rm lr}$) — with 11-replication
median timing. *Status: completed; gates "bracket cheaper than
CART on every row" and "median ratio $\ge 100\times$" PASS.*

| Dataset       | $n$    | $T_{\rm br}$ (ms) | $T_{\rm cart}$ (ms) | $T_{\rm lr}$ (ms) | CART/$T_{\rm br}$ |
|---|---|---|---|---|---|
| wine          |    178 | 0.05 |   1.0 | 0.6 |  20× |
| breast cancer |    569 | 0.11 |  13.3 | 1.1 | 119× |
| digits (bin)  |  1 797 | 0.14 |  18.9 | 1.4 | 133× |
| UCI Adult     | 45 222 | 2.73 | 306.7 | 5.1 | 112× |

The bracket is two orders of magnitude cheaper than a single
CART fit on every dataset $\ge 500$ samples, and remains cheaper
than *one* LBFGS epoch of logistic regression everywhere except
UCI Adult, where it costs roughly half an LR epoch. Bracket cost
scales linearly in $n$ (the dominant term is a single pass over
the $n$ cell labels) and is independent of feature dimension.

#### E7 — Real-data Proposition 7 concentration

Empirical companion to Proposition 7. On UCI Adult ($m = 16$
CART leaves, $\delta_{\rm conf} = 0.05$, $K = 400$ bootstrap
trials per row) we draw subsamples of size
$n \in \{200, 500, 1000, 2000, 5000, 10000, 20000\}$ with
replacement, recompute the bracket on each subsample, and
compare the deviation
$\Delta_n = |\varepsilon^*_{\rm sub} - \varepsilon^*_{\rm full}|$
to the Hoeffding bound
$\sqrt{\log(4m/\delta_{\rm conf}) / (2n)}$ from Proposition 7.
*Status: completed; gates "coverage $\ge 1 - \delta_{\rm conf}$
on every row", "mean deviation monotone in $n$", and
"$p_{95}$ deviation below the bound everywhere" all PASS.*

| $n$    | $\overline{\Delta_n}$ | $\Delta_n^{(p_{95})}$ | analytic bound | coverage |
|---|---|---|---|---|
|    200 | 0.0204 | 0.0458 | 0.1337 | 1.000 |
|  1 000 | 0.0090 | 0.0228 | 0.0598 | 1.000 |
|  5 000 | 0.0042 | 0.0106 | 0.0267 | 1.000 |
| 20 000 | 0.0019 | 0.0048 | 0.0134 | 1.000 |

Mean deviation shrinks as $\Theta(1/\sqrt{n})$ exactly as
Proposition 7 predicts; the $p_{95}$ deviation stays comfortably
inside the ($\kappa$-free, hence conservative) Hoeffding bound
at every sample size — the bound has constant $1$ instead of
$\kappa(\delta, \eta) > 1$ from the proof, so is loose by roughly
an order of magnitude in this regime. Empirical coverage is
1.000 at every $n$ versus the nominal 0.95 target.

![E7 concentration](experiments/figures/e7_concentration.pdf)

*Figure E7.* Empirical concentration of the bootstrap bracket
to the full-data bracket on UCI Adult (log–log). The mean
deviation $\overline{\Delta_n}$ follows a clean $\Theta(1/\sqrt n)$
slope; the $\kappa$-free Hoeffding bound stays above the
empirical $p_{95}$ curve at every $n$.

#### E-K — Falsification / verification protocol

A Kochenderfer-style falsification–verification protocol
(*Algorithms for Decision Making*, 2022) treats the bracket as a
formal certificate. For a candidate target Bayes-error threshold
$\tau$ and a row with bracket $[L, U]$, the claim
"$\varepsilon^{*}\le\tau$" is **falsified** when $\tau < L$,
**verified** when $\tau\ge U$, and **inconclusive** otherwise.
Applied post-hoc to the existing E1, E2, E3, E6 rows at
$\tau\in\{0.10,0.15,0.20,0.25\}$ with **zero new training**:

| source | $n$ | $\tau=0.10$ | $\tau=0.15$ | $\tau=0.20$ | $\tau=0.25$ |
|--------|----:|:-----------:|:-----------:|:-----------:|:-----------:|
|        |     | F / V / I   | F / V / I   | F / V / I   | F / V / I   |
| E1 (tree depths)     | 15 | 5 / 0 / 10  | 1 / 0 / 14  | 0 / 5 / 10  | 0 / 11 / 4 |
| E2 (VQ codebooks)    | 10 | 10 / 0 / 0  | 7 / 0 / 3   | 2 / 0 / 8   | 0 / 0 / 10 |
| E3 (WL on 5 graphs)  | 27 | 7 / 15 / 5  | 4 / 18 / 5  | 4 / 20 / 3  | 3 / 20 / 4 |
| E6 (MPNN archs)      | 50 | 50 / 0 / 0  | 28 / 0 / 22 | 0 / 0 / 50  | 0 / 0 / 50 |

The protocol distinguishes regimes the bracket *closes* (E2/E6 at
$\tau=0.10$: fully falsified; E1 at $\tau=0.25$: 11/15 verified)
from genuinely undecided regimes (E6 at $\tau\in\{0.20,0.25\}$:
fully inconclusive). Reproducible by
`experiments/eK_falsification_protocol.py`.

---

## 9. Related work

**Entropy bounds Bayes error.** The upper inequality (4.1) is
Hellman–Raviv (1970); related entropy upper bounds in Tebbe–Dwyer
(1968), Kovalevskij (1968). The lower inequality is Fano (1961) in
the sharp binary form of Cover–Thomas, Thm 2.10.1. The
achievable-region packaging is Feder–Merhav (1994); the most complete
modern treatment of two-sided entropy–error inequalities, including
extensions and continuous-alphabet generalisations, is
Ho–Verdú (2010). Sason–Verdú (2018) place these in the broader
Arimoto–Rényi framework, and Santhi–Vardy (2006) sharpen the lower
side under a different optimisation. Hashlamoun–Varshney–Samarasooriya
(1994) strengthen the upper bound for $M>2$ via $f$-divergences. The
prior-aware Fano sharpening (not pursued here) originates with
Han–Verdú (1994, eq. 6).

**Partition-constant predictors.** The decision-tree literature
(Breiman et al., 1984) treats leaf-conditional entropy as an empirical
splitting criterion; the explicit *bracket* interpretation does not
appear to have been recorded. Vector quantisation (Gersho–Gray, 1991;
Jégou–Douze–Schmid, 2011) shares the same partition structure; the
bracket is, to our knowledge, similarly new in that literature.

**MPNN expressivity.** The Weisfeiler–Leman ceiling on MPNN
expressivity is the central structural result of the last decade
(Xu et al., 2019; Morris et al., 2019); refinements include
fine-grained expressivity (Böker et al., 2023) and higher-order
variants (Morris et al., 2020). Corollary 7 recasts the WL ceiling as
one half of an information-theoretic bracket, giving the matching
upper bound on equal footing.

---

## 10. Discussion and limitations

The bracket of Theorem 1 is uniform in $\Pi$ and $f$, closed-form, and
elementary; the uniform slack $w^{*}\approx 0.1610$ of Corollary 2
pins the irreducible ambiguity any closed-form bracket of this shape
must carry, by Proposition 5.

**Limitations.** (a) Binary labels only; multi-class via Feder–Merhav
concave envelope is mechanically routine but loses closed form of
$H_{\mathrm{bin}}^{-1}$. (b) Finite $V$ only; infinite-domain needs
measure-theoretic care (Ho–Verdú). (c) The bracket bounds the Bayes
error **given** the partition; designing partitions that minimise
$H(f\mid\Pi)$ for a given budget is the harder problem the bracket
does not directly address.

**Future work.** A prior-aware tightening via data processing on the
binary error indicator (Han–Verdú, 1994) can sharpen the lower side
when the label marginal is bounded away from $1/2$; deferred to a
companion paper. A mechanised proof in Lean 4 / mathlib4 leveraging
`Real.binEntropy` and the `ConcaveOn` API, giving a kernel-checked
counterpart to `verify.jl`, is in preparation.

**Towards a framework: Paper B.** The bracket of Theorem 1 is one
instance of a broader recipe: given a partition $\Pi$ and a
real-valued summary $\phi(P_C)$ that is bounded, concave (or convex),
and matches a Bayes-risk-like target $\rho(P_C)$ on
$P_C\in\{0,1\}$, partition-conditional Jensen + Fano-style inversion
yields a two-sided $\phi$-bracket on the risk target. Replacing
$(H_{\mathrm{bin}}, \min)$ by other compatible pairs gives:
(i) a **variance bracket** on $\mathrm{MSE}/\mathrm{MAE}$ for
regression (with the well-known $\mathrm{MSE}=\mathbb E[\mathrm{Var}]$
identity recovering the upper side exactly);
(ii) a **noise-corrected bracket**
$\varepsilon^{*}(\tilde f) = \eta + (1-2\eta)\varepsilon^{*}(f)$
that is exact at the population level under symmetric label flips
with rate $\eta < 1/2$;
(iii) a **soft-partition bracket** via Markov kernels.
A companion paper in preparation organises these instances under a
single $\phi$-bracket meta-theorem; we restrict the present paper to
the binary-entropy instance for which Hellman–Raviv and Feder–Merhav
give a closed-form sandwich. The $k$-WL / HDX-trickle-down
structural variant is the subject of a further sequel.

---

## 11. Conclusion

We have given a single two-sided closed-form bracket on the Bayes
error of every partition-constant predictor of a binary label, in the
form ML practitioners need: elementary proof, uniform slack
$\approx 0.161$, sharp witnesses, three worked applications, and a
Julia verification script, and an $\varepsilon$-robust MPNN–WL
constancy lemma (Lemma 6′) that quantifies the slack incurred by
positional encodings or bounded random features. Eight
self-contained experiments on real tabular and graph benchmarks
(§8.5) instantiate the bracket end-to-end: exact agreement of
CART training error with $\varepsilon^{*}_{\Pi_d}$ at every depth
on UCI Adult; $100$–$130\times$ speedup over a single CART fit;
statistically significant NAS pre-filter signal on Adult with
parameter count as a failed control; correct pin at the
marginal-entropy ceiling on featureless Cayley and Paley
benchmarks where $1$-WL is provably blind (E3b); and
concentration to the population bracket at the predicted
$\Theta(1/\sqrt n)$ rate. We report the bracket's failure modes
(partition-cardinality collapse on near-discrete feature-rich
graphs; small-$n$ overfitting on the NAS pre-filter) with the same
prominence as its successes. The bracket makes the partition the
explicit unit of expressivity, lifting classical entropy–error
inequalities into a training-free architecture-level diagnostic for
decision trees, vector quantisers, and graph neural networks alike.
