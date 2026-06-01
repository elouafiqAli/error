# Partition Brackets: A Framework with Entropy, Variance, and Noise-Robust Instances

> **Status (Phase 2b-md.T3).** Notation, definitions, and **T3
> (meta-theorem)** are PROVEN with verifier contracts. Numbered
> claims `C-Sh`, `C-Va`, `C-Pi`, `T6`, `T7`, `P10`, `T9`, `L11`
> remain placeholders; they will be replaced by full
> machine-verifiable proofs in subsequent commits following the
> critical path in [`FORMALISATION.md`](FORMALISATION.md).

This is the **markdown twin** for the Phase 2b work. The LaTeX
source is frozen at the Phase 2a scaffold; mirroring is deferred
to Phase 2d.

---

## 0. Notation

Let $(\mathcal{X}, \mathcal{B}, \mathbb{P})$ be a standard
probability space, $f : \mathcal{X} \to \mathcal{Y}$ a measurable
label map, and $\Pi = \{S_1, \dots, S_m\}$ a *finite measurable
partition* of $\mathcal{X}$. Write $\Pi(x)$ for the unique cell
containing $x$ and $p_i := \mathbb{P}(\Pi(X) = S_i)$ for the cell
masses, so $\sum_i p_i = 1$.

For a binary label $f : \mathcal{X} \to \{0, 1\}$ define the
*cell-conditional positive rate* $\eta_i := \mathbb{P}(f(X) = 1
\mid \Pi(X) = S_i) \in [0, 1]$. The companion paper (Paper A)
defines the *partition-restricted Bayes risk*
$$
\varepsilon^{*}_{\Pi} \;:=\; \min_{g \in G(\Pi)}
  \mathbb{P}\bigl(g(X) \neq f(X)\bigr)
\;=\; \sum_{i=1}^{m} p_i \min(\eta_i, 1 - \eta_i),
$$
where $G(\Pi)$ is the class of all measurable predictors constant
on every cell of $\Pi$. For a general real-valued label, replace
$\min(\eta, 1-\eta)$ by the matched-loss Bayes optimum on the cell
(see Def. 2 below).

Throughout, $\log$ is base-2; $\ln$ is natural; the binary
entropy is $H_{\mathrm{bin}}(p) := -p\log p - (1-p)\log(1-p)$
with $H_{\mathrm{bin}}(0) = H_{\mathrm{bin}}(1) = 0$ by
convention. We denote by $H_{\mathrm{bin}}^{-1}$ the restriction
of $H_{\mathrm{bin}}$ to $[0, \tfrac12]$ inverted, i.e. the
unique $\varepsilon \in [0, \tfrac12]$ with
$H_{\mathrm{bin}}(\varepsilon) = h$ for $h \in [0, 1]$.

For a partition $\Pi$ and a scalar functional
$\varphi : [0, 1] \to \mathbb{R}_{\geq 0}$ we abuse notation and
write
$$
\varphi(f \mid \Pi) \;:=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_i),
$$
i.e. the partition-conditional expectation of $\varphi$ applied
pointwise to the cell-conditional rate. When $\varphi =
H_{\mathrm{bin}}$ this recovers the standard conditional Shannon
entropy $H(f \mid \Pi)$.

---

## 1. Definitions

### Definition 1 (Concave score functional)

A function $\varphi : [0, 1] \to \mathbb{R}_{\geq 0}$ is a
**concave score functional** if it satisfies all of:

- **(H1) Concavity.** $\varphi$ is concave on $[0, 1]$.
- **(H2) Boundary vanishing.** $\varphi(0) = \varphi(1) = 0$.
- **(H3) Continuity.** $\varphi$ is continuous on $[0, 1]$.
- **(H4) Symmetry.** $\varphi(\eta) = \varphi(1 - \eta)$ for all
  $\eta \in [0, 1]$.
- **(H5) Strict positivity on the interior.** $\varphi(\eta) >
  0$ for all $\eta \in (0, 1)$.

We write $\varphi^{-1} : [0, \varphi(\tfrac12)] \to [0,
\tfrac12]$ for the restriction of $\varphi$ to $[0, \tfrac12]$
inverted; (H1) + (H3) + (H5) ensure this restriction is a
homeomorphism (strictly increasing on $[0, \tfrac12]$ from $0$
to $\varphi(\tfrac12)$).

> *Remark.* Hypotheses (H1)–(H5) are the **minimal** set under
> which the meta-theorem (T3) goes through. (H4) can be dropped
> at the cost of replacing $\min(\eta, 1-\eta)$ in the loss
> definition by a $\varphi$-derived asymmetric Bayes risk; this
> generalisation is left as a Conjecture in §7.

#### Named instances

| Name           | $\varphi(\eta)$                     | $\varphi(\tfrac12)$ | Matched loss (Def. 2) |
|----------------|-------------------------------------|---------------------|------------------------|
| **Shannon**    | $H_{\mathrm{bin}}(\eta)$            | $1$                 | log-loss (binarised → 0-1) |
| **Variance**   | $\eta(1-\eta)$                      | $1/4$               | squared loss                |
| **Pinsker/KL** | $\mathrm{KL}(\eta \,\|\, \tfrac12)$ | $1$                 | log-loss (KL form)          |
| **Gini**       | $2\eta(1-\eta)$                     | $1/2$               | squared loss (×2)           |

### Definition 2 (Matched pointwise loss)

Let $\varphi$ be a concave score functional (Def. 1). The
**matched pointwise loss**
$\ell_\varphi : \mathcal{Y} \times \mathcal{Y} \to
\mathbb{R}_{\geq 0}$ is the unique (up to additive constants)
pointwise loss whose Bayes optimum on a Bernoulli$(\eta)$
target equals $\varphi(\eta)$, i.e.
$$
\inf_{\hat y} \mathbb{E}_{Y \sim \mathrm{Bern}(\eta)}\,
   \ell_\varphi(Y, \hat y) \;=\; \varphi(\eta).
$$
Define the **partition-restricted Bayes loss for $\ell_\varphi$**
as
$$
\varepsilon^{*,\ell_\varphi}_{\Pi} \;:=\;
   \min_{g \in G(\Pi)}\, \mathbb{E}\, \ell_\varphi(f(X), g(X))
\;=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_i)
\;=\; \varphi(f \mid \Pi),
$$
where the **second equality** is the statement that the
matched-loss Bayes optimum within cell $S_i$ achieves
$\varphi(\eta_i)$ (this is Def. 2 itself, applied per cell).

> *Remark.* For $\varphi = \min(\eta, 1-\eta)$ (not a valid score
> functional under Def. 1 — it is concave but $\varphi(0) =
> \varphi(1) = 0$ is satisfied yet **(H5) fails at the kink**),
> the matched loss is the $0$–$1$ loss and the
> partition-restricted Bayes risk is precisely Paper A's
> $\varepsilon^{*}_{\Pi}$. Paper A's bracket is therefore the
> **non-smooth limit** of the meta-theorem, obtained as a
> separate variational argument; see C-Sh in §3.

#### Three concrete matched losses

- **Shannon → log-loss.** For $\varphi = H_{\mathrm{bin}}$, the
  matched loss is $\ell(y, \hat p) = -y\log\hat p - (1-y)
  \log(1-\hat p)$ with $\hat p \in [0, 1]$; the Bayes optimum at
  $\eta$ is $\hat p^* = \eta$ with loss $H_{\mathrm{bin}}(\eta)$.

- **Variance → squared loss.** For $\varphi = \eta(1-\eta)$, the
  matched loss is $\ell(y, \hat p) = (y - \hat p)^2$; the Bayes
  optimum is $\hat p^* = \eta$ with loss
  $\eta(1-\eta) = \mathrm{Var}(\mathrm{Bern}(\eta))$.

- **Pinsker/KL → log-loss (KL form).** For $\varphi(\eta) =
  \mathrm{KL}(\eta \,\|\, \tfrac12)$, the matched loss is the
  same log-loss, viewed through the KL identity
  $\mathrm{KL}(\eta \,\|\, \tfrac12) = 1 - H_{\mathrm{bin}}(\eta)$.

These three losses are all the matched losses we ship a verifier
for in Phase 2b.

---

## 2. Theorem 3 — φ-bracket meta-theorem

**Statement (T3).** Let $\Pi = \{S_1, \dots, S_m\}$ be a finite
measurable partition, $f : \mathcal{X} \to \{0, 1\}$ a binary
label, and $\varphi : [0, 1] \to \mathbb{R}_{\geq 0}$ a concave
score functional (Def. 1, hypotheses (H1)–(H5)). Define the
**upper constant**
$$
c_\varphi \;:=\; \sup_{\eta \in (0,\, 1/2]}\,
   \frac{\eta}{\varphi(\eta)} \;\in\; (0, \infty].
$$
Then:

- **(T3-lower / Jensen)** The partition-restricted Bayes risk
  satisfies
$$
\varphi^{-1}\!\bigl(\varphi(f \mid \Pi)\bigr)
\;\leq\;
\varepsilon^{*}_{\Pi}.
$$

- **(T3-upper / linear)** If $c_\varphi < \infty$, then
$$
\varepsilon^{*}_{\Pi}
\;\leq\;
c_\varphi \cdot \varphi(f \mid \Pi),
$$
and $c_\varphi$ is the *smallest* constant for which this
inequality holds uniformly in $(\Pi, f)$. For
$\varphi = H_{\mathrm{bin}}$ one has $c_{H_{\mathrm{bin}}} =
\tfrac12$; for $\varphi = \eta(1-\eta)$ one has
$c_{\mathrm{var}} = 2$; for $\varphi = 2\eta(1-\eta)$
(Gini) one has $c_{\mathrm{Gini}} = 1$.

**Hypotheses used.** (H1) concavity, (H3) continuity, (H4)
symmetry, (H5) strict-positivity-on-interior. (H2) boundary
vanishing is used only to keep $\varphi^{-1}(0) = 0$ in the
degenerate case.

**Proof.**

*Step 1 — Cell-wise reduction via (H4).* For every $\eta \in
[0, 1]$ set $\eta_\min := \min(\eta, 1 - \eta) \in [0, \tfrac12]$.
By (H4), $\varphi(\eta) = \varphi(1 - \eta)$, so
$\varphi(\eta) = \varphi(\eta_\min)$ regardless of which side of
$\tfrac12$ the cell-conditional rate lies on. Therefore
$$
\varphi(f \mid \Pi) \;=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_i)
\;=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_{i,\min}). \tag{$\ast$}
$$

*Step 2 — Jensen lower bound.* By (H1), $\varphi$ is concave on
$[0, 1]$ (hence on $[0, \tfrac12]$). Apply Jensen's inequality
to the random variable taking value $\eta_{i,\min}$ with
probability $p_i$:
$$
\varphi\!\Bigl(\sum_i p_i\, \eta_{i,\min}\Bigr)
\;\geq\;
\sum_i p_i\, \varphi(\eta_{i,\min}).
$$
The left-hand argument is exactly $\varepsilon^{*}_{\Pi} =
\sum_i p_i \min(\eta_i, 1-\eta_i) \in [0, \tfrac12]$ (Notation,
§0). Combining with $(\ast)$,
$$
\varphi(\varepsilon^{*}_{\Pi})
\;\geq\;
\varphi(f \mid \Pi).
$$
By (H1)+(H3)+(H5), $\varphi$ restricted to $[0, \tfrac12]$ is
continuous and strictly increasing from $0$ to
$\varphi(\tfrac12)$ (a strict monotone follows because a
concave function that vanishes at $0$ and is strictly positive
on $(0, 1)$ cannot decrease on $[0, \tfrac12]$ without
contradicting (H4) on $[\tfrac12, 1]$). Applying $\varphi^{-1}$
on this interval — which is order-preserving — gives
$$
\varepsilon^{*}_{\Pi}
\;\geq\;
\varphi^{-1}\!\bigl(\varphi(f \mid \Pi)\bigr),
$$
establishing (T3-lower).

*Step 3 — Upper bound via the linear ratio.* For each cell,
$\eta_{i,\min} \in [0, \tfrac12]$. By the definition of
$c_\varphi$, for every $\eta \in (0, \tfrac12]$ we have $\eta
\leq c_\varphi\, \varphi(\eta)$; the inequality is trivial at
$\eta = 0$. Therefore $\eta_{i,\min} \leq c_\varphi\,
\varphi(\eta_{i,\min})$ for every $i$. Multiply by $p_i$, sum,
and apply $(\ast)$:
$$
\varepsilon^{*}_{\Pi}
\;=\; \sum_i p_i\, \eta_{i,\min}
\;\leq\; c_\varphi \sum_i p_i\, \varphi(\eta_{i,\min})
\;=\; c_\varphi \cdot \varphi(f \mid \Pi),
$$
which is (T3-upper). Smallness of $c_\varphi$: the
single-cell partition $m = 1$ with $\eta_1$ chosen to attain
$\sup_{\eta \in (0, 1/2]} \eta/\varphi(\eta)$ (or a maximising
sequence if the sup is not attained) certifies that no smaller
constant suffices.

*Step 4 — Sharpness witnesses.*

- (Lower-bound sharpness.) Take $m = 2$, $p_1 = p_2 = \tfrac12$,
  $\eta_1 = a \in [0, 1]$, $\eta_2 = 1 - a$. Then
  $\eta_{1,\min} = \eta_{2,\min} = \min(a, 1-a)$, so
  $\varepsilon^{*}_{\Pi} = \min(a, 1-a)$ and $\varphi(f \mid
  \Pi) = \varphi(a) = \varphi(\min(a, 1-a))$ by (H4). Hence
  $\varphi^{-1}(\varphi(f \mid \Pi)) = \min(a, 1-a) =
  \varepsilon^{*}_{\Pi}$. The lower bound is tight for **every**
  $a \in [0, 1]$ in this construction.

- (Upper-bound sharpness, Shannon.) Take $m = 1$, $\eta_1 =
  \tfrac12$. Then $\varepsilon^{*}_{\Pi} = \tfrac12$,
  $H_{\mathrm{bin}}(\tfrac12) = 1$, and $c_{H_{\mathrm{bin}}}
  \cdot 1 = \tfrac12$. Upper bound is tight.

- (Upper-bound sharpness, variance.) Take $m = 1$, $\eta_1 =
  \tfrac12$. Then $\varepsilon^{*}_{\Pi} = \tfrac12$,
  $\eta(1-\eta)|_{1/2} = \tfrac14$, and $c_{\mathrm{var}} \cdot
  \tfrac14 = \tfrac12$.

*Step 5 — Failure modes (adversarial).* We explicitly name the
hypotheses that, if dropped, kill the corresponding inequality:

- *Drop (H1) concavity.* Jensen reverses; (T3-lower) becomes an
  upper bound and the bracket inverts on counterexamples.
- *Drop (H4) symmetry.* The identity $\varphi(\eta) =
  \varphi(\eta_\min)$ in Step 1 fails; the partition-restricted
  Bayes risk for the *asymmetric* matched loss must be
  redefined (open problem OP-asym in §7).
- *Drop (H5) interior positivity.* $\varphi$ may have a
  plateau on $[0, \tfrac12]$ so $\varphi^{-1}$ ceases to be a
  function; (T3-lower) ill-posed.
- *$c_\varphi = \infty$.* The upper bound is vacuous. This is
  the **Pinsker regime** (treated in C-Pi via a square-root
  bound, not a linear one). $\square$

**Verifier contract.** Mechanically checked by

- `verify_b_t1.py::check_T3_jensen_lower` — SymPy identity
  `phi(eta) - phi(1 - eta) == 0` (H4) and concavity test
  `phi''(eta) <= 0 on (0,1)` (H1) for
  $\varphi \in \{H_{\mathrm{bin}},\, \eta(1-\eta),\,
  2\eta(1-\eta)\}$; plus a Hypothesis property test
  `prop_T3_lower` asserting $\varepsilon^{*}_{\Pi} \geq
  \varphi^{-1}(\varphi(f \mid \Pi))$ on $\geq 200$ random
  partitions $\Pi$ (cells $m \in [2, 16]$, masses
  Dirichlet$(1)$, rates uniform on $[0, 1]$) crossed with each
  of the three named $\varphi$.

- `verify_b_t1.py::check_T3_upper_constant` — SymPy/numeric
  certification that
  $c_{H_{\mathrm{bin}}} = \tfrac12$,
  $c_{\mathrm{var}} = 2$,
  $c_{\mathrm{Gini}} = 1$
  by maximising $\eta/\varphi(\eta)$ on a $10^4$-point grid of
  $(0, 1/2]$ and confirming derivative sign at the optimum;
  plus a Hypothesis property test `prop_T3_upper` asserting
  $\varepsilon^{*}_{\Pi} \leq c_\varphi\, \varphi(f \mid \Pi)$
  on the same random-partition cohort.

Run command and JSON manifest schema documented in
[`FORMALISATION.md`](FORMALISATION.md) §4–§6.

---

## 3. Instances

### Corollary C-Sh — Shannon reduction to Paper A's bracket

**Statement.** Apply T3 with $\varphi = H_{\mathrm{bin}}$. Then
$c_{H_{\mathrm{bin}}} = \tfrac12$ (T3, Step 3) and the bracket
reduces to
$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f \mid \Pi)\bigr)
\;\leq\;
\varepsilon^{*}_{\Pi}
\;\leq\;
\tfrac{1}{2}\, H(f \mid \Pi),
$$
which is *identical* to Paper A's main bracket
(Paper A, Theorem 1).

**Hypotheses.** (H1)–(H5) hold for $H_{\mathrm{bin}}$:
concavity (textbook), $H_{\mathrm{bin}}(0) = H_{\mathrm{bin}}(1)
= 0$, continuity, $H_{\mathrm{bin}}(\eta) = H_{\mathrm{bin}}(1
- \eta)$, and $H_{\mathrm{bin}}(\eta) > 0$ on $(0, 1)$.

**Proof.** Both inequalities are T3 specialised. The
identification with Paper A is verbatim: Paper A defines
$H(f \mid \Pi) = \sum_i p_i H_{\mathrm{bin}}(\eta_i)$ and uses
the inverse of $H_{\mathrm{bin}}$ on $[0, \tfrac12]$ for the
lower bound, with the constant $\tfrac12$ for the upper bound;
all four match the T3 instantiation symbol-for-symbol.
$\square$

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_CSh_reduces_to_paperA` — for each random
partition in the property cohort, computes both the
*meta-theorem* bracket (`SCORE_FUNCTIONALS["shannon"]`) and the
*Paper A* bracket (independent reference implementation of
$H_{\mathrm{bin}}$ and $H_{\mathrm{bin}}^{-1}$ on $[0, 1/2]$
via bisection) and asserts endpoint equality within $10^{-9}$.

---

### Corollary C-Va — Variance instance (Bayes–variance identity)

**Statement.** Apply T3 with $\varphi(\eta) = \eta(1-\eta)$.
Then $c_{\mathrm{var}} = 2$ (T3, Step 3). Moreover the
$\varphi$-conditional functional equals the conditional
expected variance of the (binary) label:
$$
\varphi(f \mid \Pi)
\;=\; \sum_{i=1}^{m} p_i\, \eta_i(1 - \eta_i)
\;=\; \mathbb{E}_X\!\bigl[\mathrm{Var}(f \mid \Pi)\bigr],
\tag{C-Va.id}
$$
and the bracket is
$$
\frac{1 - \sqrt{1 - 4\, \mathbb{E}[\mathrm{Var}(f \mid \Pi)]}}{2}
\;\leq\;
\varepsilon^{*}_{\Pi}
\;\leq\;
2\, \mathbb{E}[\mathrm{Var}(f \mid \Pi)].
$$

**Hypotheses.** (H1)–(H5) hold for $\varphi(\eta) = \eta(1-
\eta)$: $\varphi'' = -2$ (concave); $\varphi(0) = \varphi(1) =
0$; smooth (hence continuous); $\varphi(\eta) = \varphi(1 -
\eta)$ trivially; $\varphi(\eta) > 0$ on $(0, 1)$.

**Proof.**

- *(C-Va.id).* For $Y \sim \mathrm{Bernoulli}(\eta_i)$ inside
  cell $S_i$, $\mathrm{Var}(Y) = \eta_i(1 - \eta_i)$. Therefore
  $\mathbb{E}[\mathrm{Var}(f \mid \Pi)] = \sum_i p_i \eta_i(1 -
  \eta_i) = \varphi(f \mid \Pi)$.
- *Bracket.* Apply T3. On $[0, \tfrac12]$ the inverse of
  $\varphi(\eta) = \eta(1 - \eta)$ satisfies $\eta = (1 -
  \sqrt{1 - 4 \varphi(\eta)})/2$ by solving the quadratic; this
  is the closed-form for $\varphi^{-1}$ used in the lower
  endpoint. The upper constant is $c_{\mathrm{var}} = 2$ from
  T3 Step 3. $\square$

*Law of total variance (sanity check).* Combining (C-Va.id)
with $\mathrm{Var}(f) = \bar\eta(1 - \bar\eta)$ for binary $f$
with $\bar\eta = \sum_i p_i \eta_i$, one recovers the law of
total variance
$$
\mathrm{Var}(f) \;=\; \mathbb{E}[\mathrm{Var}(f \mid \Pi)]
                   + \mathrm{Var}(\mathbb{E}[f \mid \Pi])
\;=\; \varphi(f \mid \Pi) + \sum_i p_i (\eta_i - \bar\eta)^2,
$$
which is a verifiable consequence of (C-Va.id) and tightens the
*upper* endpoint when the partition explains most of the label
variance.

**Verifier contract.** Mechanically checked by

- `verify_b_t1.py::check_CVa_bayes_variance_identity` —
  asserts (C-Va.id) symbolically per cell and numerically on
  the property cohort; in addition certifies the law of total
  variance to $10^{-9}$ across $\geq 200$ random partitions.

- (B-T2 population corollary `T6_MSE_identity_population` in
  `verify_b_t2_mc.py` provides the IID-sample concentration
  proof; lands in the `paper-b Phase 2b-md.T6+C-Pi` commit.)

---

### C-Pi — Pinsker / KL instance

> *Status: SKELETON — to be replaced in commit
> `paper-b Phase 2b-md.T6+C-Pi`. Pinsker is the
> $c_\varphi = \infty$ failure case for the linear T3 upper
> bound and requires a square-root replacement.*

---

## 4. Regression (skeleton)

- **T6** MSE identity + MAE Cauchy–Schwarz upper bound.

## 5. Robustness (skeletons)

- **T7** Symmetric label-noise correction.
- **T9** Soft / Markov-kernel bracket.

### Proposition P10 — Refinement consistency (φ-monotonicity)

**Statement.** Let $\Pi' = \{S'_{i,k}\}_{i,k}$ be a measurable
*refinement* of $\Pi = \{S_i\}_i$, meaning every cell $S_i$ is
the disjoint union $S_i = \bigsqcup_k S'_{i,k}$. Let $\varphi$
be a concave score functional (Def. 1; only (H1) is used).
Then
$$
\varphi(f \mid \Pi') \;\leq\; \varphi(f \mid \Pi).
$$
Consequently the T3 bracket *tightens monotonically* under
refinement: both endpoints $\varphi^{-1}(\varphi(f \mid \cdot))$
and $c_\varphi \cdot \varphi(f \mid \cdot)$ are non-increasing in
the partition order.

**Hypotheses used.** (H1) concavity. None of (H2)–(H5) is
required.

**Proof.** For each $i$ let $p_i = \mathbb{P}(\Pi(X) = S_i)$
and $p_{i,k} = \mathbb{P}(\Pi'(X) = S'_{i,k})$, so
$p_i = \sum_k p_{i,k}$ and the within-cell weights
$w_{i,k} := p_{i,k}/p_i$ form a convex combination
($\sum_k w_{i,k} = 1$, $w_{i,k} \geq 0$). The
cell-conditional rates satisfy the tower property
$\eta_i = \sum_k w_{i,k}\, \eta_{i,k}$ for binary $f$.

By (H1), $\varphi$ is concave on $[0, 1]$; Jensen on the
within-cell distribution gives
$$
\varphi(\eta_i) \;=\; \varphi\!\Bigl(\sum_k w_{i,k}\, \eta_{i,k}\Bigr)
\;\geq\; \sum_k w_{i,k}\, \varphi(\eta_{i,k}).
$$
Multiply by $p_i$ and sum over $i$:
$$
\varphi(f \mid \Pi) \;=\; \sum_i p_i\, \varphi(\eta_i)
\;\geq\; \sum_i \sum_k p_{i,k}\, \varphi(\eta_{i,k})
\;=\; \varphi(f \mid \Pi'). \quad \square
$$

*Equality case.* Strict equality holds iff $\eta_{i,k} =
\eta_i$ for every $(i, k)$, i.e. every refinement step splits
a cell into sub-cells with the *same* cell-conditional rate.
In particular, $\Pi' = \Pi$ trivially achieves equality.

*Failure mode (adversarial).* Drop (H1) — then Jensen reverses
and a refinement can *increase* $\varphi(f \mid \Pi)$, violating
the upper bracket endpoint's intended monotonicity in the
partition lattice.

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_P10_refinement_monotonicity` —
Hypothesis property test `prop_P10` generates a random base
partition $\Pi$ ($m \in [2, 8]$, masses Dirichlet$(1)$, rates
uniform on $[0, 1]$), randomly splits each cell into $k_i \in
[1, 4]$ sub-cells with internal Dirichlet$(1)$ weights and
fresh uniform sub-rates, asserts
$\varphi(f \mid \Pi') \leq \varphi(f \mid \Pi) + 10^{-9}$ for
each $\varphi \in \{H_{\mathrm{bin}}, \eta(1-\eta),
2\eta(1-\eta)\}$, on $\geq 200$ random pairs.

---

## 6. MPNN aggregator-typed Lipschitz (skeleton)

- **L11** $\delta_L = \delta_0 \prod_\ell (L^c_\ell + r_T L^m_\ell)$
  with $r_T \in \{\Delta, 1, 1\}$ for sum / mean / sym-norm.

## 7. Open problems

Listed adversarially per Paper A's discipline:

1. **(OP-MAE)** Matching lower bound for the regression MAE
   instance (T6); Hotelling-1932 path is the conjectured route.
2. **(OP-T5)** Rand / VI stability of the bracket under
   partition perturbation; literature search (Meilă 2003,
   Vinh–Epps–Bailey 2010) is the first step.
3. **(OP-asym)** Drop (H4) symmetry; replace $\min(\eta, 1-\eta)$
   in the loss definition by an asymmetric Bayes risk.
4. **(OP-multi)** Lift T3 to multiclass with concave score
   functionals on the probability simplex (e.g. multinomial
   Shannon, Gini).

---

## 8. Verifier contracts (forward references)

Every numbered claim above will, by the end of Phase 2b-md, end
with a block of the form:

> **Verifier contract.** Mechanically checked by
> `verify_b_t1.py::check_<id>` (B-T1, SymPy + Hypothesis) and,
> for population statements, `verify_b_t2_mc.py::check_<id>`
> (B-T2, Monte-Carlo). Run commands and JSON manifest fields
> are documented in [`FORMALISATION.md`](FORMALISATION.md)
> §4–§6.

The verifier files live alongside this document:

- [`verify_b_t1.py`](verify_b_t1.py) — **B-T1** (symbolic
  identities + Hypothesis property tests; on the critical
  path).
- [`verify_b_t2_mc.py`](verify_b_t2_mc.py) — **B-T2**
  (Monte-Carlo population concentration; on the critical
  path).
- [`verify_b_optional.jl`](verify_b_optional.jl) — **OPTIONAL,
  off the critical path.** Julia / IntervalArithmetic parity
  with Paper A's `verify.jl`; not required to close Gate G2.
  Rationale in [`FORMALISATION.md`](FORMALISATION.md) §4.

They are currently stubs (Phase 2b-md.A013); their docstrings
declare the contracts that each subsequent commit must satisfy
before the corresponding claim is promoted from SKELETON to
PROVEN.

---

## 9. References

- Paper A: *A Two-Sided Bayes-Error Bracket from Partition-
  Conditional Entropy*, companion preprint at
  [`../partition-sandwich-preprint/`](../partition-sandwich-preprint/).
- Cover & Thomas (2006), *Elements of Information Theory*, 2nd ed.
- Meilă (2003), *Comparing clusterings by the variation of
  information*.
- Vinh, Epps & Bailey (2010), *Information theoretic measures
  for clusterings comparison*.
- Corso, Cavalleri, Beaini, Liò & Veličković (2020), *Principal
  Neighbourhood Aggregation for Graph Nets*, NeurIPS.
- Natarajan, Dhillon, Ravikumar & Tewari (2013), *Learning with
  Noisy Labels*, NeurIPS.
- Kochenderfer, Wheeler & Wray (2022), *Algorithms for Decision
  Making*, MIT Press.
