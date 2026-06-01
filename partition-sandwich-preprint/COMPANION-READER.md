# Companion Reader — Guided Path to Reproducing the Paper

**Paper.** *A Partition-Conditional Entropy Bracket on the Bayes Error*
(`main.tex` / `main.md`).

**Relationship to [`COMPANION.md`](COMPANION.md).** The companion is a
bare checklist: "tick the box, you're done". This reader expands each
checkbox into a *macro-task* with a one-paragraph "why this matters"
and an explicit "you should now be able to distinguish X from Y" exit
test. Work through the parts in order; do not skip ahead to the
experiments before you have internalised Parts 1–3.

**Audience.** Senior undergraduate in CS / Math / EE. One course each
in probability, linear algebra, machine learning. Some UNIX, Python,
Git fluency. No measure theory assumed; we stay finite/discrete.

**Conventions.** "Recite" means *state aloud from memory in under 60
seconds, then write the precise statement on paper*. "Replicate" means
*run the artefact and reproduce the committed JSON / figure*. "Prove"
means *write a proof on the board with no peeking and no gaps*.

---

## Part 1 — Probability without measure theory

### Macro-task 1.1 — Random variables and statistics

- [ ] Recite the definitions of a discrete random variable $X$ with
      pmf $p_X$, joint pmf $p_{X,Y}$, marginal $p_X = \sum_y p_{X,Y}$,
      and conditional $p_{X\mid Y}(x\mid y) = p_{X,Y}(x,y)/p_Y(y)$.
- [ ] Recite the definition of a **statistic** $T:\mathcal X\to\mathcal T$
      and its **induced partition** $\{T^{-1}(t) : t\in T(\mathcal X)\}$.
- [ ] **Distinguish:** a statistic $T$ vs. the σ-algebra it generates
      vs. the partition it induces. (In our finite setting all three
      carry the same information; we use the *partition* picture.)
- [ ] **Exit test.** Given $X\in\{1,\ldots,6\}$ uniform and
      $T(x) = x \bmod 2$, write down the partition, the pmf of $T$,
      and the conditional pmf $p_{X\mid T}$.

### Macro-task 1.2 — Expectation, conditioning, and the tower rule

- [ ] Recite linearity of expectation and the **law of total
      expectation** $\mathbb E[X] = \mathbb E[\mathbb E[X\mid Y]]$.
- [ ] Prove the **tower property for statistics**:
      $\mathbb E[\mathbb E[X\mid T(Y)]\mid Y] = \mathbb E[X\mid T(Y)]$
      using only the definition of conditional expectation.
- [ ] **Distinguish:** conditioning on $Y$ vs. conditioning on $T(Y)$
      — the latter is *coarser* and gives a weaker bound on variance
      reduction. (This is the entire reason for the partition picture.)

### Macro-task 1.3 — Jensen, Hoeffding, bootstrap, Bonferroni

- [ ] Recite **Jensen's inequality** for convex / concave $f$ and
      state when it is tight.
- [ ] Recite **Hoeffding's inequality** for bounded $X_i\in[a,b]$,
      one-sided and two-sided, with the constant $2(b-a)^2$ in the
      exponent.
- [ ] Recite the **bootstrap percentile interval** for a statistic
      $\widehat\theta$ at level $1-\alpha$.
- [ ] Recite the **Bonferroni / union bound**: $K$ events each at
      level $\alpha/K$ control the simultaneous miscoverage at
      $\alpha$.
- [ ] **Distinguish:** Hoeffding (closed form, conservative) vs.
      bootstrap p95 (data-driven, asymptotic). The Paper-A experiment
      `e7_pop_concentration.py` shows the ratio is $\approx 2.72$ on
      UCI Adult — this is the empirical price of choosing Hoeffding.
- [ ] **Replicate:** run `python experiments/e7_pop_concentration.py`
      and verify the geometric mean ratio in
      `experiments/results/e7.json`.

---

## Part 2 — Information theory you actually use

### Macro-task 2.1 — Entropies

- [ ] Recite **Shannon entropy** $H(X) = -\sum p(x)\log_2 p(x)$ and
      **binary entropy** $H_{\mathrm{bin}}(p)$.
- [ ] Recite **conditional entropy** $H(X\mid Y)$ and **mutual
      information** $I(X;Y) = H(X) - H(X\mid Y)$.
- [ ] Recite the **chain rule** $H(X,Y) = H(X) + H(Y\mid X)$.
- [ ] Recite **Rényi entropies** $R_\alpha$ for $\alpha\in(0,\infty)$,
      $\alpha\ne 1$, and their two endpoints:
      $R_0 = \log|\mathrm{supp}\,X|$, $R_\infty = -\log\max_x p(x)$.
- [ ] **Distinguish:** Shannon $H$ (average surprise) vs. min-entropy
      $R_\infty$ (worst-case adversary) vs. collision entropy $R_2$
      (guessing on the second try). For Bayes risk the min-entropy
      is what matters: $\varepsilon_X = 1 - 2^{-R_\infty(X)}$.

### Macro-task 2.2 — The three classical inequalities

- [ ] Recite **Fano's inequality** in both forms:
      classical (with $\log(M-1)$) and Han–Verdú divergence form.
- [ ] Recite **Hellman–Raviv:** $\varepsilon \le \tfrac12 H(X\mid Y)$.
- [ ] Recite the **Feder–Merhav** upper envelope on $H$ given $\pi$
      and the piecewise-extremal distribution $p_{\min}(\pi)$.
- [ ] **Prove** Hellman–Raviv from $\min(p, 1-p)\le \tfrac12 H_{\mathrm{bin}}(p)$
      in at most ten lines.
- [ ] **Prove** the divergence form of Fano via the
      data-processing inequality on the indicator
      $\mathbf 1\{X = \widehat X\}$.
- [ ] **Distinguish:** Fano (lower bound on $\varepsilon$ via $H$)
      vs. Hellman–Raviv (upper bound on $\varepsilon$ via $H$). They
      are *opposite directions of the same sandwich*; the paper's
      Theorem 1 sharpens both endpoints with the partition $T$.

### Macro-task 2.3 — Reading list to cement Part 2

- [ ] Cover & Thomas, *Elements of Information Theory*, Ch 2 and 17.
- [ ] `fano-inequality.md` (Han–Verdú, full text in repo root).
- [ ] `feder.md` (Feder–Merhav, full text in repo root).

---

## Part 3 — The paper's core construction

### Macro-task 3.1 — Setup vocabulary

- [ ] Recite: prior Bayes risk $\varepsilon_X$; conditional Bayes
      risk $\varepsilon_{X\mid T}$ given a statistic $T$; the
      partition $\mathcal C = \{C_k\}$ induced by $T$; per-cell
      mass $q_C = \Pr[T(X)\in C]$; per-cell Bayes error $e_C$.
- [ ] **Distinguish:** $\varepsilon_X$ (one number, the prior) vs.
      $\varepsilon_{X\mid T}$ (one number, averaged over $T$) vs.
      the *vector* $\{e_C\}_C$ (the granular object the bracket
      operates on).
- [ ] **Distinguish:** the **achievable region** $\tilde A_2$ in the
      $(H, \pi)$ plane (geometric object) vs. the **bracket**
      (algebraic lower–upper pair on $\varepsilon_{X\mid T}$).

### Macro-task 3.2 — Theorem 1 (the sandwich)

- [ ] Read $\S$"Main result" (`main.tex` line ~472) in one sitting.
- [ ] Identify in the statement: the constants $h$, $h_{\mathrm{union}}$,
      $K_T$; the lower envelope (per-cell Hellman–Raviv plus tower);
      the upper envelope (Jaynes max-entropy dual).
- [ ] **Prove** the lower half from scratch on the board (apply
      Hellman–Raviv inside each $C_k$, then take expectation
      over $T$, then collect $H(X\mid T)$).
- [ ] **Prove** the upper half by writing the Jaynes Lagrangian with
      multipliers $(\lambda_C)$ for the cell-mass constraints and
      one $\mu$ for the entropy constraint; solve for the saddle.
- [ ] **Replicate:** open `verify.jl`, locate the `@testset` for
      Theorem 1, and re-run `julia --project=. verify.jl`. Confirm
      the interval-arithmetic certificate is non-trivial (the
      printed interval does not cross zero).

### Macro-task 3.3 — Proposition 3.5 (non-improvement)

- [ ] Recite: there is no closed-form, prior-free improvement that
      tightens both envelopes simultaneously at all $(\pi, H)$.
- [ ] Identify the **witnessing families** $\Pi_\alpha^{\mathrm{HR}}$
      (saturates the upper envelope) and $\Pi_\varepsilon^{\mathrm F}$
      (saturates the lower envelope).
- [ ] **Distinguish:** "no improvement" (Prop 3.5, prior-free) vs.
      "prior-aware sharpening" (Prop 3.6, when the prior is partially
      known) — the latter is *not* a contradiction of the former.

### Macro-task 3.4 — Refinement monotonicity (§6)

- [ ] Recite: if $T'$ refines $T$ then the bracket on
      $\varepsilon_{X\mid T'}$ is contained in the bracket on
      $\varepsilon_{X\mid T}$.
- [ ] **Prove** it using only the tower property and concavity of
      $H_{\mathrm{bin}}$.
- [ ] **Distinguish:** a *true* monotonicity violation
      (would break Theorem 1) vs. an *apparent* violation caused by
      bracket endpoints being non-monotone (the latter is fine and
      visualised in the §7 sharpness witnesses).

### Macro-task 3.5 — Aggregator constants for MPNN / WL (§9.3)

- [ ] Recite the triple $r_T = (\Delta_{\max}, 1, 1)$ for
      $T\in\{\mathrm{sum}, \mathrm{mean}, \mathrm{sym\text{-}norm}\}$
      in the L11 statement.
- [ ] **Distinguish:** sum aggregation (degree-coupled blow-up
      $\Delta_{\max}$) vs. mean / sym-norm (degree-normalised, no
      blow-up). On Cora the Paper-A harvest shows $\Delta_{\max}=168$
      driving up to 7 orders of magnitude looseness — *the bound is
      never violated*, it is just honestly loose.
- [ ] **Replicate:** run `python experiments/e3e_robust_lemma.py`;
      confirm `experiments/results/e3e.json :: bound_never_violated == true`
      and the worst-looseness row matches §9.3's caption.

---

## Part 4 — Proof carpentry recitations

The four "board-level" proofs you must be able to write under exam
conditions. Each macro-task below is one whiteboard session.

- [ ] **Carpentry 4.1.** Hellman–Raviv from scratch (10 lines).
- [ ] **Carpentry 4.2.** The Jaynes-dual upper envelope of Theorem 1,
      naming every Lagrange multiplier.
- [ ] **Carpentry 4.3.** The union-bound budget $\tau = K_T \cdot h$
      and the prose paragraph in §0.5 of `main.md` explaining why
      $4\times$ (not $3\times$, not $5\times$) is the right
      Bonferroni multiplier here.
- [ ] **Carpentry 4.4.** Refinement monotonicity via the tower
      property and concavity of $H_{\mathrm{bin}}$.

For each: rehearse three times on consecutive days; ask a peer to
poke at the weakest step.

---

## Part 5 — Mechanised verification

### Macro-task 5.1 — Read the verifiers as a *spec*

- [ ] Open `verify.jl`. Each `@testset` corresponds to one theorem;
      list the mapping in a notebook.
- [ ] Open `verify_t1_float.py`, `verify_t3_symbolic.py`,
      `verify_t4_population.py`. For each, identify: the theorem
      checked, the witness family, the tolerance / precision.
- [ ] **Distinguish:** interval arithmetic (Julia, rigorous) vs.
      symbolic verification (SymPy, exact but limited to closed
      forms) vs. floating-point witness sweeps (NumPy, fast but
      relies on dense grids). Each catches a different failure mode.

### Macro-task 5.2 — Mutate, fail, revert

- [ ] Flip one sign in a verifier; re-run; confirm the test fails;
      revert. (Mandatory: this builds intuition for which steps
      the verifier actually depends on.)
- [ ] Read `VERIFICATION.md` end-to-end; reconcile every claim
      table row with the `*.json` file it points to.

---

## Part 6 — Experiments, one at a time

Per experiment: run the script, open the JSON, open the figure,
*write one sentence* mapping the figure to the JSON.

- [ ] `e1_trees.py` — decision-tree / random-forest sandwich.
- [ ] `e2_vq_proxy.py` + `e2b_marginal_aware.py` — VQ baseline and
      the marginal-aware sharpening. **Distinguish:** when does
      marginal awareness actually move the bracket?
- [ ] `e3_wl_bracket.py` + `e3a_decomposition.py` +
      `e3b_wl_structural.py` — WL bracket and its additive
      decomposition.
- [ ] `e3d_arch_audit.py` / `e3d_arch_full.py` — architecture sweep
      (long-pole; GPU; current run on RunPod for OGBN). For
      reproduction on a laptop, run `e3d_arch_audit.py` only.
- [ ] `e3e_robust_lemma.py` — the L11 honest-looseness witness
      (see Macro-task 3.5).
- [ ] `e3f_richer_init.py` — sensitivity to initialisation.
- [ ] `e4_duel.py`, `e5_scatter.py` — pairwise duels and scatter
      visualisations.
- [ ] `e6_cost.py`, `e6_nas.py`, `e6_nas_v2.py` — cost vs. bracket
      under neural architecture search.
- [ ] `e7_pop_concentration.py` — UCI Adult bootstrap (see
      Macro-task 1.3).
- [ ] `eK_falsification_protocol.py` — Kochenderfer-style
      falsification screen on all of the above; confirm the 408-row
      classification $121 / 89 / 198$ (falsified / verified /
      inconclusive).

---

## Part 7 — Adversarial audit ritual

For every theorem and every experiment, answer in writing:

- [ ] What does it *actually* say? (Beware informal slippage.)
- [ ] What is the tightest counter-example or kill condition?
- [ ] What calibrated confidence does it deserve —
      `HIGH` / `MEDIUM` / `LOW` / `UNVERIFIED`?
- [ ] Which adjacent claim does it falsify if pushed?

Then:

- [ ] Cross-check your answers against the audit table in
      `future-work/07-three-paper-arc-master-plan.md` §1.
- [ ] **Distinguish:** an honest looseness (Carpentry 4.3, Macro-task
      3.5) vs. a bug. Honest looseness is *flagged in the prose*,
      survives all verifiers, and has a named cause.

---

## Part 8 — Definition of "done"

You can claim reproduction when, without notes, you can:

- [ ] State Theorem 1 and sketch both halves of the proof in ten
      minutes on a whiteboard.
- [ ] Re-run `make` + `verify.jl` + the three Python verifiers +
      every script in `experiments/` on a clean checkout; all
      artefacts match committed JSON / PDF figures.
- [ ] Name one experiment whose looseness is large and explain why
      it is *honest* rather than a bug.
- [ ] Name two open problems from
      `future-work/05-sequel-paper-plan.md` or
      `future-work/06-kwl-bracket-paper-roadmap.md` and identify
      which theorem each one would extend.
- [ ] Explain, in one sentence each, the difference between this
      paper (Paper A) and its sibling
      `partition-brackets-framework/` (Paper B): A binarises the
      bracket via $H_{\mathrm{bin}}$; B abstracts to a $\phi$-bracket
      meta-theorem covering variance, noise, and Markov kernels.

---

## Part 9 — Bonus rigour drills (skim-proofing)

The checklists above are *minimum competence*. The drills below are
designed to keep you from "tick-the-box" reading. Each drill asks you
to recover a result from a *different angle* than the paper presents
it, or to walk a path that *almost* works and then explain why it
doesn't. If you cannot do a drill, you have skimmed the underlying
section.

### Bonus 9.1 — Random variables from three angles

- [ ] **Reproduce** the binomial pmf in three independent ways:
      (a) combinatorial $\binom{n}{k}p^k(1-p)^{n-k}$;
      (b) sum of $n$ iid Bernoullis via convolution;
      (c) characteristic-function product $(pe^{it}+1-p)^n$ inverted.
      Confirm all three agree at $n=5, p=1/3$.
- [ ] **Reproduce** the Gaussian density from
      (a) the central limit theorem applied to standardised
      Bernoullis;
      (b) the entropy-maximisation program with fixed mean and
      variance (a Jaynes warm-up for Macro-task 3.2);
      (c) the heat-equation Green's function.
- [ ] **False lead.** Try to derive Hellman–Raviv by tilting the
      proof of Fano (start with the indicator, apply DPI, take the
      *upper* bound). Show that the bound you get is
      $\varepsilon \le 1 - 2^{-H(X\mid Y)}$, which is *strictly
      weaker* than $\varepsilon \le \tfrac12 H(X\mid Y)$ on
      $H \le 1$. Lesson: opposite-direction bounds need
      opposite-direction tools (Jensen on a *concave* upper bound,
      not DPI).
- [ ] **Common mistake.** Many students "prove" the tower property
      via $\mathbb E[X\mid T(Y)] = \mathbb E[\mathbb E[X\mid Y]\mid T(Y)]$
      and then drop the inner conditioning. State precisely what
      goes wrong when $T$ is *not* a function of $Y$ alone (e.g.
      $T$ depends on an exogenous coin flip).

### Bonus 9.2 — Information theory in matrix form

- [ ] **Reproduce** mutual information $I(X;Y)$ as the
      Frobenius-style inner product
      $\sum_{x,y} P_{XY}(x,y) \log \frac{P_{XY}(x,y)}{P_X(x) P_Y(y)}$
      and rewrite it as
      $\mathrm{tr}(P_{XY} \log(P_{XY} \oslash (p_X p_Y^\top)))$,
      where $\oslash$ is elementwise division.
- [ ] **Reproduce** the data-processing inequality
      $I(X;Z) \le I(X;Y)$ for a Markov chain
      $X \to Y \to Z$ using *only* the matrix form: $Z$'s joint
      with $X$ is $P_{XY} K$ where $K$ is the $Y\to Z$ stochastic
      kernel; apply log-sum inequality column-wise.
- [ ] **Reproduce** Fano via the confusion matrix: write the joint
      $(\widehat X, X)$ as a matrix $M$ with diagonal mass
      $1 - \varepsilon$; bound $H(X\mid \widehat X)$ from above
      using the off-diagonal mass and conclude.
- [ ] **Reproduce** Hellman–Raviv per-cell as a sum over the
      partition $\mathcal C$: $\varepsilon_{X\mid T} =
      \sum_C q_C e_C \le \tfrac12 \sum_C q_C H_{\mathrm{bin}}(e_C)$,
      then invoke concavity of $H_{\mathrm{bin}}$ to land at
      $\tfrac12 H(X\mid T)$. **Distinguish** this two-step derivation
      from the one-step version on the un-partitioned $H(X\mid Y)$.
- [ ] **False lead.** Try to sharpen the upper envelope of
      Theorem 1 by replacing $H_{\mathrm{bin}}$ with the *Rényi*
      $R_2$ inside each cell (collision entropy is smaller, so the
      bound *looks* tighter). Show that the resulting envelope
      *violates* the witnessing family $\Pi_\alpha^{\mathrm{HR}}$
      and is therefore not a valid upper bound. Lesson: tightness
      witnesses are the verification you owe before announcing an
      improvement.

### Bonus 9.3 — Reproducing the sandwich from scratch (no paper)

- [ ] **Reproduce** Theorem 1 on a fresh notepad with the paper
      closed: start from the partition $\mathcal C$, write the
      per-cell Hellman–Raviv, take expectation under $q_C$, apply
      Jensen, recognise $H(X\mid T)$. Then turn the page and check.
- [ ] **Reproduce** Prop 3.5 by *finding* the witnessing families
      yourself: parametrise a one-parameter family on the upper
      envelope that interpolates between Hellman–Raviv saturation
      and Fano saturation. Confirm by direct substitution.
- [ ] **Common mistake.** Students often "improve" Prop 3.5 by
      assuming a *uniform* prior. Show that under uniformity the
      bracket *does* tighten (this is Prop 3.6's prior-aware
      sharpening) — but that the improvement disappears as soon as
      the prior is even slightly perturbed. Lesson: prior-free
      claims are a different game.
- [ ] **False lead.** Try to prove refinement monotonicity by
      *adding* cells one at a time and showing the bracket
      shrinks at each step. Show that this fails when the new cell
      is added with mass $q_C \approx 0$ but $e_C = 1/2$: the
      *endpoints* of the bracket are non-monotone even though the
      *bracket itself* contains the previous one. Lesson: the
      object that is monotone is the *interval*, not its
      individual ends.

### Bonus 9.4 — Aggregator-typed Lemma 11 in matrix form

- [ ] **Reproduce** the L11 sum-aggregator constant by writing one
      MPNN layer as $X^{(\ell+1)} = \sigma(A X^{(\ell)} W^{(\ell)})$
      with $A$ the adjacency; differentiate w.r.t. an input
      perturbation $\delta$; identify $\|A\|_\infty = \Delta_{\max}$
      as the worst-case row sum.
- [ ] **Reproduce** the mean-aggregator constant by replacing $A$
      with $D^{-1}A$ where $D$ is the degree diagonal; show
      $\|D^{-1}A\|_\infty = 1$ exactly.
- [ ] **Reproduce** the sym-norm constant by using
      $D^{-1/2}AD^{-1/2}$ and bounding via spectral radius
      $\le 1$.
- [ ] **Distinguish:** the three constants share the *form* of the
      L11 bound but live on different operator norms ($\infty$,
      $\infty$, $2$). Naming the wrong norm is the most common
      error in this section.
- [ ] **Common mistake.** Re-deriving L11 for sum aggregation
      *without* the $\Delta_{\max}$ factor by silently assuming
      bounded degree. Show that on Cora ($\Delta_{\max} = 168$)
      this mistake hides 5 of the 7 orders of magnitude of
      looseness reported by `e3e_robust_lemma.py`.

### Bonus 9.5 — Population extension (Prop 7) in matrix form

- [ ] **Reproduce** the Hoeffding bound on per-cell error
      estimates: let $\widehat e_C$ be the empirical Bayes error on
      $n_C$ samples in cell $C$; bound
      $\Pr[|\widehat e_C - e_C| > t] \le 2\exp(-2 n_C t^2)$.
- [ ] **Reproduce** the union-bound budget over $K_T$ cells:
      $\Pr[\max_C |\widehat e_C - e_C| > t] \le 2 K_T \exp(-2 n_C t^2)$.
- [ ] **Reproduce** the $O(1/\sqrt n)$ slack by inverting the
      bound at level $\alpha$: $t = \sqrt{\log(2 K_T / \alpha) / (2 n_C)}$.
- [ ] **False lead.** Try to replace Hoeffding by Chebyshev for the
      per-cell concentration. Show that the resulting rate is
      $O(1/\sqrt[4]{n})$, which would predict E6-NAS digits-bin
      failure at $n_{\mathrm{tr}} \approx 2000$ rather than the
      observed $1437$. Lesson: tail-bound sharpness propagates
      linearly into experimental predictions.
- [ ] **Common mistake.** Bootstrap p95 *is not* a Hoeffding-style
      confidence interval; it is a percentile of the resampled
      distribution. Conflating the two leads to under-conservative
      intervals when the underlying statistic has heavy tails.

### Bonus 9.6 — Mechanised verification, adversarially

- [ ] **Reproduce** an interval-arithmetic certificate by hand for
      one small instance ($K_T = 2$, $\pi = 1/3$): compute the
      bracket endpoints as intervals with explicit rounding mode
      and show non-containment of zero.
- [ ] **False lead.** Replace `IntervalArithmetic.jl` with naive
      floating-point and re-run; show that the certificate
      *passes* on $K_T = 2$ but *silently fails* at $K_T = 8$ where
      catastrophic cancellation eats the slack. Lesson: rigorous
      arithmetic matters even when the numbers look harmless.
- [ ] **Common mistake.** Re-running `verify.jl` after editing a
      tolerance without re-running `verify_t1_float.py` (which uses
      a different tolerance). All four verifiers must be re-run
      together to update the verification surface.
- [ ] **Drill.** Pick any one verifier and write down, in plain
      English, *what would have to change in the paper* if its
      assertion flipped. If you cannot answer, you do not yet know
      what the verifier verifies.

### Bonus 9.7 — Experimental epistemics

- [ ] **Reproduce** the Kochenderfer ternary verdict on a *single*
      experiment row by hand: compute the predicted bound, the
      observed value, the tolerance band $\tau \le w^*$; classify
      as falsified / verified / inconclusive.
- [ ] **Reproduce** the headline $121 / 89 / 198$ across all 408
      rows by running `eK_falsification_protocol.py` and checking
      the breakdown in `experiments/results/eK.json`.
- [ ] **False lead.** Try to declare an inconclusive row as
      "verified at a wider tolerance". Show that this violates
      one-sided soundness: a wider tolerance lets falsified rows
      slip through as verified. Lesson: tolerance is fixed *before*
      the verdict, never after.
- [ ] **Common mistake.** Re-running an experiment with a different
      random seed and reporting the better number. The discipline
      rule is: every numerical claim in the paper must hold under
      the *first* seed; subsequent seeds are sanity checks, not
      cherry-picking opportunities.
- [ ] **Drill.** Pick one experiment and design an *adversarial*
      perturbation that would push its result from "verified" to
      "falsified". If no such perturbation exists, you have not
      found the failure mode and the result is over-claimed.

### Bonus 9.8 — Cross-paper triangulation

- [ ] **Reproduce** the binary $H_{\mathrm{bin}}$ bracket of Paper A
      as a special case of Paper B's $\phi$-bracket meta-theorem
      with $\phi = H_{\mathrm{bin}}$. Identify which Paper-B
      hypotheses become trivial in this specialisation.
- [ ] **Distinguish:** Paper A's bracket on $\varepsilon$ vs.
      Paper B's bracket on a generic $\phi$ (variance, noise,
      Markov-kernel mixing). Paper A is the *anchor instance*;
      Paper B is the *abstraction*. Either alone is half the story.
- [ ] **False lead.** Try to extend Paper A's bracket to multi-class
      Bayes error by replacing $H_{\mathrm{bin}}$ with full
      Shannon $H$. Show that the per-cell Hellman–Raviv inequality
      *changes shape* (the $\tfrac12$ becomes a piecewise function
      of the class count) and that the upper envelope no longer
      admits a closed form. Lesson: binarising is *not* a cosmetic
      restriction; it is the choice that makes the bracket
      closed-form.
- [ ] **Drill.** Read `future-work/06-kwl-bracket-paper-roadmap.md`
      §1; identify one open problem that the methods of Part 4
      could plausibly attack and one that they cannot. Justify
      both claims.

### Bonus 9.9 — Anti-patterns checklist (do not do these)

- [ ] Do not skim the proofs and "trust the verifier" — the
      verifiers check *closed-form witnesses*, not the proof
      structure that produced them.
- [ ] Do not announce a sharpening before testing it on the
      witnessing families $\Pi_\alpha^{\mathrm{HR}}$ and
      $\Pi_\varepsilon^{\mathrm F}$. Most "improvements" die
      against one of these two.
- [ ] Do not conflate refinement monotonicity (interval inclusion)
      with endpoint monotonicity (numerical decrease). They are
      different and only the former is true.
- [ ] Do not increase a tolerance to upgrade an inconclusive verdict
      to verified. This breaks soundness.
- [ ] Do not run experiments without first stating the prediction
      the paper makes for that experiment. Without a prediction,
      the experiment is decoration.
- [ ] Do not edit `main.tex` and `main.md` separately. They must
      stay in sync; the repository discipline rule is non-
      negotiable.

---

*End of reader. If you can tick every box here without skipping
Part 3, Part 4, or Part 9, you have reproduced the paper to the
standard expected of a co-author — and you have inoculated yourself
against the most common reproduction failure modes.*
