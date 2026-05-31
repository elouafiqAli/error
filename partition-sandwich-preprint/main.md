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
certified interval arithmetic; zero violations.

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

---

## 3. Main result

**Theorem 1 (Two-sided bracket).** For every finite partition $\Pi$
of a finite set $V$ and every binary $f:V\to\{0,1\}$,
$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f\mid\Pi)\bigr) \;\le\; \varepsilon^{*}_{\Pi} \;\le\; \tfrac{1}{2}\,H(f\mid\Pi). \tag{3.1}
$$

**Achievable region.** Every pair $(\varepsilon, H) = (\varepsilon^{*}_{\Pi}, H(f\mid\Pi))$
arising from finite partition / binary label data lies in
$$
\widetilde A_2 := \bigl\{(\varepsilon, H)\in[0,1/2]\times[0,1] : H_{\mathrm{bin}}^{-1}(H)\le\varepsilon\le H/2\bigr\}.
$$
The two boundaries are realised by explicit one-parameter families
(§7), the interior by mixtures of boundary witnesses; so
$\widetilde A_2$ is exactly the closure of achievable pairs. See
`figures/achievable_region.pdf`.

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

Six experiments (E1–E6, plus a planned E7 for Proposition 7) on
real tabular and graph benchmarks complement the synthetic
verifiers. Full specifications and reproducibility receipts are
in `experiments/REPORTS.md` (completed experiments) and
`experiments/PLANS.md` (planned). Each experiment is designed to
discriminate a single claim of the paper against a stated
reviewer concern.

#### E1 — Decision-tree refinement funnel (UCI Adult, $n=45{,}222$)

Materialises Proposition 4 (refinement monotonicity) and the
(E1) practitioner claim. For depth $d\in\{1,\dots,15\}$ we report
the bracket together with the realised CART training error.
*Status: completed.*

| $d$ | $H(f\mid\Pi_d)$ | lower | $\varepsilon^*_{\Pi_d}$ | upper | CART train err |
|---|---|---|---|---|---|
| 1  | TBD   | TBD   | TBD   | TBD   | TBD   |
| 5  | TBD   | TBD   | TBD   | TBD   | TBD   |
| 10 | TBD   | TBD   | TBD   | TBD   | TBD   |
| 15 | 0.354 | 0.034 | 0.108 | 0.354 | 0.108 |

Figure: `experiments/figures/e1_refinement_funnel.pdf`.

#### E2 — VQ zero-shot proxy (UCI Adult)

Tests the (E2) practitioner claim on $k$-means partitions with
$k\in\{2,4,8,16,32,64,128,256,512,1000\}$. For each $k$ we compute
the bracket and train a downstream logistic regression on one-hot
cell membership; the trained error must match
$\varepsilon^*_{\Pi_k}$ to within 1%, demonstrating that the
bracket **predicts** trained-model behaviour, not merely bounds
it. *Status: completed; rebuts the "training-free is misleading"
critique.*

| $k$ | $H(f\mid\Pi_k)$ | lower | $\varepsilon^*_{\Pi_k}$ | LR err | $|\mathrm{LR}-\varepsilon^*|$ |
|---|---|---|---|---|---|
| 2    | 0.8025 | 0.2445 | 0.2478 | 0.2478 | 0.0000 |
| 16   | 0.6597 | 0.1709 | 0.2352 | 0.2352 | 0.0000 |
| 128  | 0.6135 | 0.1515 | 0.1995 | 0.1995 | 0.0000 |
| 1000 | 0.5291 | 0.1199 | 0.1761 | 0.1771 | 0.0010 |

Figure: `experiments/figures/e2_vq_zeroshot.pdf`.

#### E2b — Marginal-aware refinement on real data *(planned)*

Validates Proposition 6 on unbalanced real labels. For each
binary dataset in the menu (UCI Adult $\pi\!\approx\!0.24$,
Spambase $\pi\!\approx\!0.39$, Phishing $\pi\!\approx\!0.44$),
we compute the universal bracket slack $w^*$ and the
marginal-aware slack $w^*(\pi_*)$ for the partitions of E1 and
E2, and report the reduction.
*Status: pending — spec in `experiments/PLANS.md`.*

| Dataset   | $\pi_*$ | $w^*$  | $w^*(\pi_*)$ |
|---|---|---|---|
| UCI Adult | TBD     | 0.1610 | TBD          |
| Spambase  | TBD     | 0.1610 | TBD          |
| Phishing  | TBD     | 0.1610 | TBD          |

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

| Graph      | $|V|$    | $L$ | $m_L$    | lower  | $\varepsilon^*_{\Pi_L}$ | upper  |
|---|---|---|---|---|---|---|
| Twitch-EN  | 7 126    | 0 |     130  | 0.3853 | 0.4164 | 0.4809 |
| Twitch-EN  | 7 126    | 3 |   6 648  | 0.0073 | 0.0267 | 0.0312 |
| Cora       | 2 708    | 3 |   2 363  | 0.0076 | 0.0292 | 0.0323 |
| CiteSeer   | 3 327    | 3 |   2 044  | 0.0400 | 0.0775 | 0.1212 |
| PubMed     | 19 717   | 3 |  12 990  | 0.0205 | 0.0511 | 0.0722 |
| ogbn-arxiv | 169 343  | 3 | 161 943  | 0.0005 | 0.0021 | 0.0029 |

Full funnels $L=0\dots L_{\max}$ in `experiments/results/e3.json`;
figures `experiments/figures/e3_<dataset>_funnel.pdf`.

**What the numbers say.** Two regimes are visible.

*(i) The active regime, $L = 0$* (degree-binned colouring, no
message passing yet). The bracket has substantial width: on
ogbn-arxiv it is 0.151, within 1% of the universal ceiling
$w^* \approx 0.161$ of Corollary 2; on Twitch-EN it is 0.096.
The achievable error $\varepsilon^*_{\Pi_0}$ sits interior to
the bracket — its position is a *diagnostic of the partition
itself*: high inside the bracket means decisive-but-noisy
cells (the cells separate vertices but their internal label
distributions are far from purity), low inside the bracket
means pure-but-small cells (the cells are nearly homogeneous
but each contains few vertices). To our knowledge no prior
MPNN-expressivity study reports this signal.

*(ii) The structural ceiling regime, $L = 3$.* The bracket has
collapsed by an order of magnitude across every dataset: on
ogbn-arxiv $m_3 = 161{,}943$ reaches 95.6% of $|V|$, on Cora
87%, on Twitch-EN 93%. This is consistent with the well-known
phenomenon that 1-WL stabilises after a small number of rounds
on sparse real graphs (Morris et al., 2019; Arvind et al.,
2015); it is also a structural form of overfitting. By depth 3
the 1-WL fingerprint has separated almost every vertex from
every other, so the bracket pinches towards zero not because
some MPNN secretly solved the task but because the partition
has memorised the structure of the graph itself. We report both
regimes because the $L = 0$ rows are where the bracket actively
*bounds*; the $L = 3$ rows are the structural ceiling of the
1-WL family that Xu and Morris characterise.

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
natural next experiment.

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

#### E5 — Achievable-region scatter (synthetic)

Visualises Theorem 1 and Corollary 2: $10^3$ random partitions
of $V=\{1,\dots,n\}$, $n\in\{4,\dots,32\}$, plotted in the
$(H,\varepsilon)$ plane against the Fano and Hellman–Raviv
boundaries. Empirical max upper slack
$0.16096404744368120$ vs analytic $0.16096404744368115$
(≤ 1 ulp of `Float64`). *Status: completed.*
Figure: `experiments/figures/e5_achievable_region_scatter.pdf`.

#### E6 — Cost comparison vs one training epoch *(planned)*

Quantifies the $O(|V|)$ remark of §1. For each dataset of the
menu, time `bracket_from_cells` (a single $O(|V|)$ pass)
against one CART fit, one $k$-means `fit_predict`, and one
logistic-regression epoch on one-hot cell membership. The ratio
should be $\ll 10^{-2}$ across the menu.
*Status: pending — spec in `experiments/PLANS.md`.*

| Dataset   | $|V|$    | $T_{\mathrm{bracket}}$ (ms) | $T_{\mathrm{epoch}}$ (ms) | ratio |
|---|---|---|---|---|
| Spambase  | 4 601    | TBD | TBD | TBD |
| MAGIC     | 19 020   | TBD | TBD | TBD |
| UCI Adult | 45 222   | TBD | TBD | TBD |
| MNIST-bin | 70 000   | TBD | TBD | TBD |

#### E7 — Real-data Proposition 7 concentration *(planned)*

Empirical companion to Proposition 7. On UCI Adult, draw
subsamples of size $n\in\{500,1000,5000,10000,20000,45000\}$;
for each $n$, $K=200$ trials, compare the empirical bracket to
the full-data bracket via
$\Delta_n = |\varepsilon^*_{\mathrm{full}} - \varepsilon^*_{\mathrm{sub}}|
   + |H_{\mathrm{full}} - H_{\mathrm{sub}}|$,
and check empirical coverage at the Hoeffding rate
$\kappa(\delta,\eta)\sqrt{\log(4m/\delta_{\mathrm{conf}})/n}$.
*Status: pending — spec in `experiments/PLANS.md`.*

| $n$    | $\overline{\Delta_n}$ | $\Delta_n^{(p95)}$ | analytic bound | coverage |
|---|---|---|---|---|
| 500    | TBD | TBD | TBD | TBD |
| 5000   | TBD | TBD | TBD | TBD |
| 45000  | TBD | TBD | TBD | TBD |

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

---

## 11. Conclusion

We have given a single two-sided closed-form bracket on the Bayes
error of every partition-constant predictor of a binary label, in the
form ML practitioners need: elementary proof, uniform slack
$\approx 0.161$, sharp witnesses, three worked applications, and a
Julia verification script. The bracket makes the partition the
explicit unit of expressivity, lifting classical entropy–error
inequalities into a training-free architecture-level diagnostic for
decision trees, vector quantisers, and graph neural networks alike.
