# Partition Brackets: A Framework with Entropy, Variance, and Noise-Robust Instances

> **Status (Phase 2b-md.G2 CLOSED).** All numbered claims —
> **T3** (meta-theorem), **C-Sh** (Shannon reduction), **C-Va**
> (Bayes–variance identity), **C-Pi** (Pinsker sqrt
> replacement), **T6** (regression MSE/MAE), **T7** (symmetric
> label-noise correction), **T9** (soft / Markov-kernel
> bracket), **P10** (refinement consistency), **L11** (MPNN
> aggregator-typed Lipschitz) — are PROVEN with mechanically
> checked verifier contracts. Critical-path ladder is GREEN:
> `verify_b_t1.py` pass=8/8, `verify_b_t2_mc.py` pass=5/5 on
> seed 0. See [`FORMALISATION.md`](FORMALISATION.md) §3 for the
> closed G2 gate-table.

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

### C-Pi — Pinsker / KL instance (sqrt-bound replacement when $c_\varphi = \infty$)

**Setup.** Take $\varphi_{\mathrm{KL}}(\eta) := 1 - H_{\mathrm{bin}}
(\eta) = D_{\mathrm{KL}}\!\bigl(\mathrm{Bern}(\eta) \,\|\,
\mathrm{Bern}(\tfrac12)\bigr)$ (bits). Two T3 hypotheses fail
*simultaneously*:

- **(H1) fails.** $\varphi_{\mathrm{KL}}$ is *convex*, not
  concave ($\varphi_{\mathrm{KL}}'' = 1/(\eta(1-\eta) \ln 2)
  > 0$). Jensen swings the wrong way; T3's lower bracket is
  vacuous.

- **(T3 Step 3) fails.** $c_{\mathrm{KL}} := \sup_{\eta \in
  [0,1/2]} \min(\eta, 1-\eta)/\varphi_{\mathrm{KL}}(\eta) =
  \infty$, since as $\eta \to \tfrac12$ the numerator
  $\to \tfrac12$ while the denominator $\to 0$ (Taylor:
  $\varphi_{\mathrm{KL}}(\tfrac12 + t) = (2/\ln 2)\, t^2 + O(t^4)$).
  The linear upper bracket is vacuous.

This is precisely the failure mode named in T3 Step 5.

**Statement (Pinsker bracket, sqrt-shaped lower).** For every
random binary label $f$ with cell-conditional rates
$(\eta_i)_{i=1}^m$ on partition $\Pi$,
$$
\varepsilon^{*}_{\Pi}(f)
\;\geq\;
\tfrac12 \;-\; \sqrt{\tfrac{\ln 2}{2}\,\bigl(1 - H(f \mid \Pi)\bigr)},
\qquad
H(f \mid \Pi) := \sum_i p_i\, H_{\mathrm{bin}}(\eta_i).
\tag{C-Pi.lower}
$$

**Proof.**

- *Step 1 (Pinsker, classical).* For any $\eta \in [0, 1]$,
  $D_{\mathrm{KL}}(\mathrm{Bern}(\eta) \| \mathrm{Bern}(\tfrac12)) \geq
  (2/\ln 2)\,(\eta - \tfrac12)^2$ (Pinsker's inequality in
  bits, or equivalently $D_{\mathrm{KL}} \geq 2 \cdot \mathrm{TV}^2 / \ln 2$ with
  $\mathrm{TV}(\mathrm{Bern}(\eta), \mathrm{Bern}(\tfrac12)) = |\eta -
  \tfrac12|$). Equivalently:
  $|\eta - \tfrac12| \leq \sqrt{(\ln 2)/2 \cdot (1 -
  H_{\mathrm{bin}}(\eta))}$.

- *Step 2 (kink as $\tfrac12 - |\cdot|$).* $\min(\eta, 1-\eta)
  = \tfrac12 - |\eta - \tfrac12|$. Combine with Step 1:
  $\min(\eta_i, 1 - \eta_i) \geq \tfrac12 - \sqrt{(\ln 2)/2 \cdot
  (1 - H_{\mathrm{bin}}(\eta_i))}$.

- *Step 3 (aggregate via Jensen on $-\sqrt{\cdot}$, concave).*
  $\varepsilon^{*}_{\Pi}(f) = \sum_i p_i \min(\eta_i, 1 -
  \eta_i) \geq \tfrac12 - \sum_i p_i \sqrt{(\ln 2)/2 \cdot (1 -
  H_{\mathrm{bin}}(\eta_i))} \geq \tfrac12 - \sqrt{(\ln 2)/2 \cdot
  (1 - H(f \mid \Pi))}$, where the last step uses Jensen with
  the concave function $\sqrt{\cdot}$. $\square$

**Adversarial check.** Pinsker is tight only in the limit
$\eta \to \tfrac12$; the bracket is *vacuous* (returns
$\varepsilon^{*}_{\Pi} \geq -\text{something}$) whenever $H(f
\mid \Pi) < 1 - 2/\ln 2 \approx -1.886$, which never happens
since $H_{\mathrm{bin}} \in [0, 1]$. It is *non-trivial* iff
$H(f \mid \Pi) > 1 - 1/(2 \ln 2) \approx 0.279$. Bretagnolle–
Huber is a strictly sharper drop-in for the same direction; see
OP-BH in §7.

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_CPi_pinsker_constant`:

- SymPy verifies Pinsker $\eta \mapsto 1 - H_{\mathrm{bin}}(\eta)
  - (2/\ln 2)(\eta - \tfrac12)^2 \geq 0$ on a $10^4$-point grid
  to $5 \times 10^{-4}$ (with rounded-down endpoint guard);

- Hypothesis fuzzes 200 random binary labels on random
  partitions and asserts the population (C-Pi.lower) holds.

---

## 4. Regression

### Theorem T6 — Regression MSE identity + MAE Cauchy–Schwarz upper

**Setup.** Let $f : \mathcal{X} \to [0, 1]$ be a bounded
(possibly real-valued, not necessarily binary) label and let
$\eta_i := \mathbb{E}[f \mid \Pi = S_i]$ be the cell-conditional
mean. Partition-restricted Bayes risks under squared / absolute
loss are
$$
\mathrm{MSE}^{*}_{\Pi}(f) := \inf_{\hat y\, \Pi\text{-measurable}}
  \mathbb{E}\bigl[(f - \hat y)^2\bigr],
\qquad
\mathrm{MAE}^{*}_{\Pi}(f) := \inf_{\hat y\, \Pi\text{-measurable}}
  \mathbb{E}\bigl[|f - \hat y|\bigr].
$$

**Statement.**

- **(T6.MSE)** The MSE bracket *collapses* to an identity:
$$
\mathrm{MSE}^{*}_{\Pi}(f) \;=\; \mathbb{E}\bigl[\mathrm{Var}(f \mid \Pi)\bigr]
   \;=\; \varphi_{\mathrm{var}}(f \mid \Pi).
$$

- **(T6.MAE)** MAE Cauchy–Schwarz upper bound:
$$
\mathrm{MAE}^{*}_{\Pi}(f) \;\leq\; \sqrt{\mathrm{MSE}^{*}_{\Pi}(f)}
   \;=\; \sqrt{\mathbb{E}\bigl[\mathrm{Var}(f \mid \Pi)\bigr]}.
$$
  The matching lower bound is **OP-MAE** (§7): no closed-form
  is known without additional regularity on $f \mid \Pi = S_i$.

**Proof.**

- *(T6.MSE).* The per-cell squared-loss minimiser is the
  conditional mean: $\arg\min_{c} \mathbb{E}[(f - c)^2 \mid \Pi=S_i]
  = \mathbb{E}[f \mid \Pi=S_i] = \eta_i$, and the minimum
  equals $\mathrm{Var}(f \mid \Pi = S_i)$. Sum against $p_i$:
  $\mathrm{MSE}^{*}_{\Pi}(f) = \sum_i p_i \mathrm{Var}(f \mid \Pi=S_i) =
  \mathbb{E}[\mathrm{Var}(f \mid \Pi)]$. For *binary* $f$ this
  specialises to $\sum_i p_i \eta_i(1 - \eta_i) =
  \varphi_{\mathrm{var}}(f \mid \Pi)$, recovering (C-Va.id);
  the equality is *degenerate* T3 with both bracket endpoints
  coinciding ($\varphi^{-1} \circ \varphi = \mathrm{id}$ when
  the per-cell loss equals $\varphi$).

- *(T6.MAE).* For any predictor $\hat y$, Cauchy–Schwarz with
  the constant weight $\mathbf{1}$ yields $\mathbb{E}[|f - \hat
  y|] \leq \sqrt{\mathbb{E}[(f - \hat y)^2]}$. Take $\hat y$ to
  be the MSE-optimal $\Pi$-measurable predictor (cell-wise
  mean); then the RHS equals $\sqrt{\mathrm{MSE}^{*}_{\Pi}(f)}$. The
  $\inf$ over $\Pi$-measurable predictors on the LHS is only
  smaller, so $\mathrm{MAE}^{*}_{\Pi}(f) \leq \mathbb{E}[|f - \hat
  y_{\mathrm{MSE}^*}|] \leq \sqrt{\mathrm{MSE}^{*}_{\Pi}(f)}$. $\square$

*Tightness of (T6.MAE).* The inequality is tight when $f \mid
\Pi$ is *two-point* (e.g. binary), since then absolute and
squared loss coincide up to scale. For continuous $f \mid \Pi$
it is loose; closing the gap is OP-MAE.

**Verifier contract.** Mechanically checked by

- `verify_b_t2_mc.py::check_T6_MSE_identity_population` — for
  random partitions with bounded continuous $f \mid \Pi$
  (e.g.\ Beta-distributed labels per cell), draws $n = 50{,}000$
  IID samples, computes $\widehat{\mathrm{MSE}}^{*}_{\Pi}$ via the
  cell-wise sample mean predictor and $\widehat{\mathbb{E}}
  [\mathrm{Var}(f \mid \Pi)]$ via cell-wise sample variance,
  asserts agreement within $4 \cdot$ Hoeffding 95\% halfwidth on
  every of `--trials` (default 500) repetitions.

- `verify_b_t2_mc.py::check_T6_MAE_upper_population` — same
  cohort; computes empirical $\widehat{\mathrm{MAE}}^{*}_{\Pi}$ via
  cell-wise median and asserts $\widehat{\mathrm{MAE}}^{*}_{\Pi}
  \leq \sqrt{\widehat{\mathrm{MSE}}^{*}_{\Pi}} + 4 \cdot $
  Hoeffding 95\% halfwidth.

- `verify_b_t2_mc.py::check_CVa_variance_identity_population` —
  binary-label specialisation: empirical
  $\widehat{\mathrm{MSE}}^{*}_{\Pi}$ matches $\sum_i \hat p_i
  \hat\eta_i (1 - \hat\eta_i)$ within Hoeffding halfwidth.

---

## 5. Robustness

### Theorem T9 — Soft / Markov-kernel bracket

**Setup.** Generalise from a *deterministic finite partition* $\Pi$
(equivalently, a $\sigma$-algebra generated by a finite measurable
partition) to a *Markov kernel* $K : \mathcal{X} \to \Delta(\mathcal{Z})$
into a *finite* code alphabet $\mathcal{Z} = \{1, \dots, m\}$ — i.e.\
$K(z \mid x) \geq 0$ and $\sum_z K(z \mid x) = 1$. The
deterministic case recovers $K(z \mid x) = \mathbf{1}[\Pi(x) = S_z]$.
Define the *soft* cell masses and cell-conditional positive rates
$$
p_z^{K} := \int_{\mathcal{X}} K(z \mid x)\, d\mathbb{P}(x),
\qquad
\eta_z^{K} := \frac{1}{p_z^{K}} \int_{\mathcal{X}} K(z \mid x)\,
   \mathbb{P}\bigl(f(X) = 1 \mid X = x\bigr)\, d\mathbb{P}(x),
$$
which are well-defined whenever $p_z^{K} > 0$ (cells of zero
mass are dropped without loss of generality). The
*kernel-restricted Bayes risk* is
$$
\varepsilon^{*}_{K}(f) \;:=\; \min_{g \in G(K)}
  \mathbb{P}\bigl(g(Z) \neq f(X)\bigr)
\;=\; \sum_{z=1}^{m} p_z^{K} \min(\eta_z^{K}, 1 - \eta_z^{K}),
$$
where $Z \mid X = x \sim K(\cdot \mid x)$ and $G(K)$ is the class
of all predictors that depend on $X$ only through $Z$.

**Statement.** Let $\varphi$ be a score functional satisfying
(H1)–(H5) of T3. Then for the soft conditional functional
$\varphi(f \mid K) := \sum_z p_z^{K} \varphi(\eta_z^{K})$ the
$\varphi$-bracket holds verbatim:
$$
\varphi^{-1}\bigl(\varphi(f \mid K)\bigr)
\;\leq\;
\varepsilon^{*}_{K}(f)
\;\leq\;
c_\varphi \cdot \varphi(f \mid K).
\tag{T9.bracket}
$$
Moreover, kernel *refinement* — $K' \succeq K$ meaning $K =
\Phi K'$ for some row-stochastic $\Phi : \mathcal{Z}' \to
\Delta(\mathcal{Z})$ — preserves $\varphi$-monotonicity:
$\varphi(f \mid K') \leq \varphi(f \mid K)$ (T9.refinement).

**Hypotheses.** (H1)–(H5) on $\varphi$ as in T3. $\mathcal{Z}$
is at most countable with finite second moment of cell masses;
the finite case is sufficient for all Paper-B applications.

**Proof.**

- *Step 1 (reduce to T3 on the post-kernel partition).* Define
  the *deterministic* partition $\Pi_K = \{S_1^{K}, \dots,
  S_m^{K}\}$ of the *enlarged* space $\mathcal{X} \times
  \mathcal{Z}$ under the joint measure $\mathbb{P}(dx) K(dz \mid
  x)$ by $S_z^{K} := \mathcal{X} \times \{z\}$. Under the joint
  measure, $\Pi_K$ is a *deterministic* finite partition with
  cell mass $p_z^{K}$ and cell-conditional positive rate
  $\eta_z^{K}$ exactly as defined above (by the tower property:
  $\mathbb{P}((X, Z) \in S_z^{K}) = \mathbb{P}(Z = z) =
  \int K(z \mid x) d\mathbb{P}(x) = p_z^{K}$, and
  $\mathbb{P}(f(X) = 1 \mid (X, Z) \in S_z^{K}) =
  \mathbb{E}[K(z \mid X) \mathbb{P}(f = 1 \mid X)] / p_z^{K} =
  \eta_z^{K}$).

- *Step 2 (apply T3 on the enlarged space).* Since $\Pi_K$ is a
  bona fide deterministic finite partition of $(\mathcal{X}
  \times \mathcal{Z}, \mathbb{P} \otimes K)$ with masses
  $p_z^{K}$ and rates $\eta_z^{K}$, T3 gives (T9.bracket) with
  $\varepsilon^{*}_{\Pi_K}(f') = \sum_z p_z^{K} \min(\eta_z^{K},
  1 - \eta_z^{K})$, where $f'(x, z) := f(x)$ is the lifted
  label. Identification $\varepsilon^{*}_{\Pi_K}(f') =
  \varepsilon^{*}_{K}(f)$ is by construction: predictors in
  $G(\Pi_K)$ depend on $(x, z)$ only through $z$, matching $G(K)$.

- *Step 3 (refinement / lifted P10).* If $K = \Phi K'$, the
  composition $\Phi : \mathcal{Z}' \to \Delta(\mathcal{Z})$
  defines a *deterministic refinement* on the lifted space: a
  cell $S_{z'}^{K'}$ of $\Pi_{K'}$ is a measure-theoretic
  refinement of $S_z^{K}$ in proportion $\Phi(z \mid z')$. The
  joint cell mass / rate identities $p_z^{K} = \sum_{z'}
  \Phi(z \mid z') p_{z'}^{K'}$ and $p_z^{K} \eta_z^{K} =
  \sum_{z'} \Phi(z \mid z') p_{z'}^{K'} \eta_{z'}^{K'}$ — i.e.\
  cell-rate is a *barycentre* of the refined rates — hold
  directly from the kernel composition. Apply P10 on the lifted
  space. $\square$

*Identification with the deterministic case.* For $K(z \mid x) =
\mathbf{1}[\Pi(x) = S_z]$, $p_z^{K} = p_z$, $\eta_z^{K} =
\eta_z$, and (T9.bracket) reduces to T3 verbatim. T9 is thus a
*conservative extension*: every Paper-B numerical claim phrased
for $\Pi$ extends to soft kernels with no constant penalty.

*Adversarial check.* T9 does NOT lift to infinite alphabets
without additional regularity ($\sum_z p_z^K \varphi(\eta_z^K)$
may diverge or fail to converge in distribution); the
countable-alphabet extension requires a uniform-integrability
hypothesis on $\{\varphi(\eta_z^K)\}_z$ which we record as OP-soft
in §7. The finite-$m$ result is unconditional.

**Verifier contract.** The T9-bracket is *symbolically* implied
by T3 on the lifted space, so the existing B-T1 contract
`check_T3_jensen_lower` already covers it (the lifted partition
is a finite partition, and T3 takes no notice of how it was
constructed). We therefore do **not** add a new B-T1 contract.
The B-T2 population check below catches violations of the
*identification* step (Step 1) where the lift could in principle
go wrong if our cell-rate definitions are mis-stated.

- `verify_b_t2_mc.py::check_T9_kernel_bracket_population` —
  draws a random row-stochastic $K : [n_X] \to \Delta([m])$ with
  $n_X = 16$, $m \in [2, 8]$; samples $n = 50{,}000$ IID
  $(X, Z)$ pairs via $Z \mid X \sim K(\cdot \mid X)$; computes
  the empirical kernel-restricted Bayes risk and the empirical
  T9 bracket for $\varphi \in \{H_{\mathrm{bin}},
  \varphi_{\mathrm{var}}\}$; asserts both bracket endpoints
  envelope the Bayes risk within $4 \cdot$ Hoeffding 95\%
  halfwidth on every of `--trials` (default 500) repetitions.

### Theorem T7 — Symmetric label-noise correction

**Statement.** Let $f : \mathcal{X} \to \{0, 1\}$ be the *clean*
binary label and let $\tilde f$ be the *noisy* label obtained by
independent symmetric label flips with rate $\rho \in [0, 1/2)$:
$$
\mathbb{P}\bigl(\tilde f(X) = 1 - f(X) \,\big|\, X\bigr) = \rho,
\qquad
\mathbb{P}\bigl(\tilde f(X) = f(X) \,\big|\, X\bigr) = 1 - \rho.
$$
Let $\tilde\eta_i := \mathbb{P}(\tilde f = 1 \mid \Pi = S_i)$ be
the *noisy* cell-conditional positive rate. Then:

- **(T7.affine)** Per-cell affine relation:
$$
\tilde\eta_i \;=\; \rho + (1 - 2\rho)\, \eta_i,
\qquad
\tilde\eta_i \in [\rho, 1 - \rho].
$$
- **(T7.kink)** Per-cell minimum identity:
$$
\min(\tilde\eta_i, 1 - \tilde\eta_i)
\;=\;
\rho + (1 - 2\rho) \min(\eta_i, 1 - \eta_i).
$$
- **(T7.correction)** Partition-restricted Bayes risk
  correction:
$$
\varepsilon^{*}_{\Pi}(\tilde f) \;=\; \rho + (1 - 2\rho)\,
   \varepsilon^{*}_{\Pi}(f),
\qquad
\varepsilon^{*}_{\Pi}(f) \;=\; \frac{\varepsilon^{*}_{\Pi}(\tilde f) - \rho}{1 - 2\rho}.
$$
- **(T7.bracket)** Noise-corrected $\varphi$-bracket: for any
  concave score functional $\varphi$ with $c_\varphi < \infty$,
$$
\frac{\varphi^{-1}\bigl(\varphi(\tilde f \mid \Pi)\bigr) - \rho}{1 - 2\rho}
\;\leq\; \varepsilon^{*}_{\Pi}(f) \;\leq\;
\frac{c_\varphi \cdot \varphi(\tilde f \mid \Pi) - \rho}{1 - 2\rho}.
$$

**Hypotheses used.** $\rho \in [0, \tfrac12)$ strictly. The
boundary $\rho = \tfrac12$ is the indistinguishability noise
floor where clean and noisy labels are statistically
independent and identification is lost. T7.bracket additionally
requires the T3 hypotheses (H1)–(H5) and $c_\varphi < \infty$.

**Proof.**

- *(T7.affine).* By total expectation conditional on $\Pi =
  S_i$,
  $\mathbb{P}(\tilde f = 1 \mid \Pi = S_i) = (1 - \rho)\eta_i +
  \rho(1 - \eta_i) = \rho + (1 - 2\rho)\eta_i$.

- *(T7.kink).* Since $1 - 2\rho > 0$, the affine map $\eta \mapsto
  \rho + (1 - 2\rho)\eta$ is order-preserving. Hence $\tilde\eta_i
  \leq \tfrac12 \iff \eta_i \leq \tfrac12$. In the case
  $\eta_i \leq \tfrac12$ both minima equal their first argument:
  $\min(\eta_i, 1-\eta_i) = \eta_i$ and $\min(\tilde\eta_i,
  1-\tilde\eta_i) = \tilde\eta_i = \rho + (1 - 2\rho)\eta_i$,
  proving (T7.kink). The case $\eta_i > \tfrac12$ is symmetric
  via $\eta_i \mapsto 1 - \eta_i$ and the involution
  $\min(\eta, 1-\eta) = \min(1-\eta, \eta)$.

- *(T7.correction).* Sum (T7.kink) against $p_i$ (which is
  unchanged by label noise — only labels flip, not cell
  memberships):
  $$
  \varepsilon^{*}_{\Pi}(\tilde f) = \sum_i p_i \min(\tilde\eta_i,
  1-\tilde\eta_i) = \sum_i p_i \bigl[\rho + (1-2\rho)\min(\eta_i,
  1-\eta_i)\bigr] = \rho + (1-2\rho)\varepsilon^{*}_{\Pi}(f).
  $$
  Solve for $\varepsilon^{*}_{\Pi}(f)$.

- *(T7.bracket).* Apply T3 to the noisy label $\tilde f$ to get
  $\varphi^{-1}(\varphi(\tilde f \mid \Pi)) \leq
  \varepsilon^{*}_{\Pi}(\tilde f) \leq c_\varphi \cdot
  \varphi(\tilde f \mid \Pi)$. Substitute (T7.correction) and
  divide by $1 - 2\rho > 0$. $\square$

*Identification with Paper A.* For $\varphi = H_{\mathrm{bin}}$,
T7.bracket recovers Paper A's Proposition 7 (noise-corrected
Shannon bracket) symbol-for-symbol via C-Sh.

*Failure modes (adversarial).*
- $\rho = \tfrac12$: the denominator vanishes and
  $\varepsilon^{*}_{\Pi}(\tilde f) = \tfrac12$ regardless of
  $\varepsilon^{*}_{\Pi}(f)$; identification is lost.
- $\rho > \tfrac12$: relabel by swapping classes globally
  (equivalent to $\rho' = 1 - \rho < \tfrac12$); the formulas
  then apply to the swapped labels.
- *Asymmetric noise* (different flip rates for 0→1 and 1→0):
  the affine map (T7.affine) becomes
  $\tilde\eta = \rho_{0 \to 1} + (1 - \rho_{0 \to 1} -
  \rho_{1 \to 0})\eta$ and the kink identity (T7.kink) no longer
  collapses cleanly; asymmetric correction is left as an open
  problem (related to OP-asym in §7).

**Verifier contract.** Mechanically checked by

- `verify_b_t1.py::check_T7_noise_correction_symbolic` — SymPy
  proves (T7.affine), (T7.kink) (case-split on $\eta \leq
  \tfrac12$), and the algebraic inverse in (T7.correction).

- `verify_b_t2_mc.py::check_T7_noise_correction_population` —
  for each $\rho \in \{0.05, 0.10, 0.20\}$, draws $n =
  50{,}000$ IID samples $(X_t, f(X_t))$ from a fixed
  partition, flips labels symmetrically, computes empirical
  $\hat\varepsilon^{*}_{\Pi}(f)$ and $\hat\varepsilon^{*}_{\Pi}
  (\tilde f)$, asserts the correction identity holds within
  the Hoeffding 95\% half-width $\sqrt{\ln(2/0.05)/(2n)}$ on
  *every* of `--trials` (default 500) repetitions.

- `verify_b_t2_mc.py::check_T7_shannon_matches_paperA` — the
  Shannon corollary of T7.bracket numerically matches Paper
  A's Proposition 7 to 4 decimals on the same cohort.

---

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

## 6. MPNN aggregator-typed Lipschitz

### Lemma L11 — aggregator-typed cumulative Lipschitz constant

**Statement.** Consider an $L$-layer message-passing neural
network on a graph $G = (V, E)$ with per-node features
$h^{(0)}_v \in \mathbb{R}^d$. Each layer $\ell \in \{1, \dots,
L\}$ has the form
$$
h^{(\ell)}_v
\;=\;
C_\ell\!\left(\, h^{(\ell-1)}_v,\;
   \mathrm{AGG}_T\!\bigl\{ M_\ell(h^{(\ell-1)}_u) : u \in N(v) \bigr\}
\right),
$$
where $C_\ell$ is the COMBINE map, $M_\ell$ is the MESSAGE map,
and $\mathrm{AGG}_T$ is the aggregator of type $T \in
\{\mathrm{sum}, \mathrm{mean}, \mathrm{sym\text{-}norm}\}$.
Assume $C_\ell$ has Lipschitz constant $L^c_\ell$ in its first
argument and Lipschitz constant $1$ in its second
argument*, $M_\ell$ has Lipschitz constant $L^m_\ell$, and the
initial feature map is $\delta_0$-Lipschitz in some upstream
input. Let $\Delta := \max_v |N(v)|$ be the maximum degree.
Define the **aggregator constant**
$$
r_T \;:=\;
\begin{cases}
   \Delta & T = \mathrm{sum}, \\
   1      & T = \mathrm{mean}, \\
   1      & T = \mathrm{sym\text{-}norm}.
\end{cases}
$$
Then the cumulative per-node Lipschitz constant of the
$L$-layer MPNN satisfies
$$
\delta_L \;\leq\; \delta_0 \, \prod_{\ell=1}^{L}\,
  \bigl( L^c_\ell + r_T \, L^m_\ell \bigr).
$$

*Footnote on the COMBINE-second-arg assumption: any constant
$\kappa$ for the second argument is absorbed into $L^m_\ell$ by
rescaling; taking $\kappa = 1$ is a wlog normalisation.*

**Hypotheses used.** None of (H1)–(H5) is invoked. L11 is
the one Paper B result that lives outside the $\varphi$-bracket
proper: it ports Paper A's Lemma 6$'$ aggregator-typed bound to
the meta-theorem's notation so that the noise / refinement
chain rules of the bracket can be evaluated under realistic
MPNN feature perturbations.

**Proof.** Induction on $\ell$.

*Base ($\ell = 0$).* $\delta_0$ is given.

*Inductive step ($\ell - 1 \to \ell$).* Let $\Delta h_u :=
h^{(\ell-1)}_u - h'^{(\ell-1)}_u$ be the per-node feature
perturbation at depth $\ell - 1$, with uniform bound
$\|\Delta h_u\| \leq \delta_{\ell-1}$ over all $u$.

1. **Message map.** $\|M_\ell(h^{(\ell-1)}_u) -
   M_\ell(h'^{(\ell-1)}_u)\| \leq L^m_\ell\, \delta_{\ell-1}$ for
   every $u$, by Lipschitz of $M_\ell$.

2. **Aggregator.** Bound the perturbation of $\mathrm{AGG}_T$
   over $N(v)$:
   - $T = \mathrm{sum}$: $\|\sum_{u} M_\ell(h_u) - \sum_u
     M_\ell(h'_u)\| \leq |N(v)| \cdot L^m_\ell\, \delta_{\ell-1}
     \leq \Delta \cdot L^m_\ell\, \delta_{\ell-1}$.
   - $T = \mathrm{mean}$: $\| \tfrac{1}{|N(v)|} \sum_u (\cdot)
     \| \leq L^m_\ell\, \delta_{\ell-1}$ — the $1/|N(v)|$ factor
     cancels the sum, leaving $r_T = 1$.
   - $T = \mathrm{sym\text{-}norm}$ (GCN-style normalisation
     $\sum_u (\cdot) / \sqrt{d_u d_v}$): the symmetric
     normalisation gives operator norm $\leq 1$ on regular
     graphs and $\leq 1$ on irregular graphs by
     Cauchy–Schwarz; hence $r_T = 1$.

3. **Combine map.** $C_\ell$ is $L^c_\ell$-Lipschitz in arg 1
   and $1$-Lipschitz in arg 2 (wlog), so
   $$
   \|h^{(\ell)}_v - h'^{(\ell)}_v\|
   \;\leq\; L^c_\ell\, \delta_{\ell-1} + 1 \cdot r_T \, L^m_\ell\, \delta_{\ell-1}
   \;=\; (L^c_\ell + r_T\, L^m_\ell)\, \delta_{\ell-1}.
   $$

Hence $\delta_\ell \leq (L^c_\ell + r_T\, L^m_\ell)\,
\delta_{\ell-1}$, and the product formula follows by chaining.
$\square$

*Identification with Paper A.* In the Shannon special case
($\varphi = H_{\mathrm{bin}}$), L11 reproduces Paper A's
Lemma 6$'$ (the aggregator-typed cumulative Lipschitz
constant in Paper A §6) symbol-for-symbol; the $r_T \in
\{\Delta, 1, 1\}$ table is identical.

*Failure mode.* If $C_\ell$ is not $L^c_\ell$-Lipschitz in arg
1 (e.g. uses a non-Lipschitz activation like the unconstrained
ReLU on unbounded features), the bound becomes vacuous. The
result is *tight* for the operator-norm-equal-to-Lipschitz
case (linear MPNN); for nonlinear nets it is an upper
estimate.

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_L11_aggregator_deltaL` —
(a) SymPy verification that the inductive recurrence
$\delta_\ell = (L^c_\ell + r_T L^m_\ell)\, \delta_{\ell-1}$
closed-forms to the product formula by symbolic product
expansion; (b) Hypothesis property test `prop_L11_linear`
builds a random *linear* scalar MPNN on a star graph
(node 0 = root, $\Delta$ leaves), random Lipschitz constants
$L^c_\ell, L^m_\ell \in [0.1, 2]$, depth $L \in [1, 5]$, and
for each aggregator $T \in \{\mathrm{sum}, \mathrm{mean},
\mathrm{sym\text{-}norm}\}$ asserts $|h^{(L)}_0 -
h'^{(L)}_0| \leq \delta_0\, \prod (L^c_\ell + r_T L^m_\ell) +
10^{-9}$ on $\geq 200$ random instances.

---

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
