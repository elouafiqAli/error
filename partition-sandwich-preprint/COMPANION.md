# Paper Companion — Senior Undergraduate Reproduction Checklist

**Paper.** *A Partition-Conditional Entropy Bracket on the Bayes Error*
(`main.tex` / `main.md`, this directory).

**How to use this document.** Pure checklist. Tick each box as you go.
No explanations beyond the named concept/task. For every theory item,
the goal is: state it precisely from memory, sketch the proof in five
lines, and name one place it fails. For every reproduction item, the
goal is: run the artefact, read the output, and explain it in one
sentence.

**Estimated background.** Senior undergraduate in CS/Math/EE with one
course each in probability, linear algebra, and machine learning;
comfortable on a UNIX shell with Python and Git.

---

## Part 0 — Environment and source

- [ ] Clone the repository and `cd partition-sandwich-preprint/`.
- [ ] Install a TeX distribution that ships `pdflatex` + `bibtex`
      (TeX Live or MacTeX); verify with `pdflatex --version`.
- [ ] Build the paper: `make` in this directory; confirm `main.pdf`
      appears and matches the committed `main.tex`.
- [ ] Create a Python 3.11+ virtualenv; install
      `partition-sandwich-preprint/experiments/requirements.txt`
      and (separately) `pip install julia` only if you plan to run
      `verify.jl`.
- [ ] Install Julia 1.10+ with `IntervalArithmetic.jl`; from this
      directory run `julia --project=. verify.jl` and confirm
      `verify.json` matches the committed copy.
- [ ] Run the three Python verifiers and diff against committed JSON:
      `python verify_t1_float.py`, `python verify_t3_symbolic.py`,
      `python verify_t4_population.py`.
- [ ] Read `VERIFICATION.md` end-to-end; confirm you can map every
      theorem in the paper to its verifier (or to "proof only").

## Part 1 — Probability prerequisites

- [ ] Discrete random variables, joint / marginal / conditional pmfs.
- [ ] Expectation, variance, indicator functions, total probability /
      total expectation.
- [ ] Definition of a statistic $T:\mathcal X\to\mathcal T$ and the
      partition it induces (preimage classes).
- [ ] Data-processing inequality for KL divergence and mutual
      information; corollary: conditioning reduces entropy.
- [ ] Jensen's inequality for concave/convex $f$.
- [ ] Hoeffding's inequality (bounded random variables) — state the
      one-sided and two-sided forms; know the constant 2.
- [ ] Bootstrap percentile interval — definition, coverage caveat.
- [ ] Bonferroni / union-bound correction over $K$ events at level
      $\alpha$.

## Part 2 — Information theory prerequisites

- [ ] Shannon entropy $H(X)$ in bits; binary entropy $H_{\mathrm{bin}}$.
- [ ] Conditional entropy $H(X\mid Y)$; mutual information $I(X;Y)$;
      chain rule.
- [ ] Rényi entropies $R_\alpha$; min-entropy $R_\infty$; relation
      $\varepsilon_X = 1 - 2^{-R_\infty(X)}$ to the prior Bayes risk.
- [ ] **Fano's inequality** — both the "$\log M$" form and the
      Han–Verdú divergence form; necessary conditions for equality.
- [ ] **Hellman–Raviv inequality** $\varepsilon \le \tfrac12 H(X\mid Y)$
      — proof via per-symbol $\min(p, 1-p)\le \tfrac12 H_{\mathrm{bin}}(p)$.
- [ ] **Feder–Merhav region** — converse to Hellman–Raviv; the
      piecewise-extremal distribution $p_{\min}(\pi)$.
- [ ] Conditional Jensen inequality and the role of concavity of
      $H_{\mathrm{bin}}$.

## Part 3 — Bayes-error theory specific to this paper

- [ ] Definitions: prior Bayes risk $\varepsilon_X$; conditional Bayes
      risk $\varepsilon_{X\mid T}$; partition $\mathcal C = \{C_k\}$
      induced by $T$; per-cell mass $q_C$; per-cell Bayes error $e_C$.
- [ ] The **achievable region** $\tilde A_2$ in the $(H, \pi)$ plane
      and its convex hull.
- [ ] **Theorem 1 (sandwich).** State precisely: lower envelope via
      Hellman–Raviv applied per cell, upper envelope via the
      Jaynes max-entropy program; identify $h$, $h_{\mathrm{union}}$,
      $K_T$ in the statement.
- [ ] **Proposition 3.5 (non-improvement).** Why the closed-form
      bracket cannot be tightened uniformly; the witnessing families
      $\Pi_\alpha^{\mathrm{HR}}$ and $\Pi_\varepsilon^{\mathrm F}$.
- [ ] **Proposition 3.6 (prior-aware sharpening).** What "prior-aware"
      buys you and the trust-tier disclaimer.
- [ ] **Refinement monotonicity** ($\S 6$): refining a partition can
      only tighten the bracket; pathologies that look like violations
      but are not.
- [ ] **Sharpness witnesses** ($\S 8$): be able to construct one
      worked $(X, T)$ pair that achieves each envelope.
- [ ] **Aggregator constants** for MPNN/WL ($\S 9.3$): $r_T$ for
      sum, mean, sym-norm; the $\Delta_{\max}$ blow-up under sum.

## Part 4 — Proof carpentry (be able to reproduce on the board)

- [ ] Re-derive Hellman–Raviv from scratch in $\le 10$ lines.
- [ ] Re-derive the Jaynes-dual upper envelope of Theorem 1, naming
      every Lagrange multiplier.
- [ ] Re-derive the union-bound budget $\tau = K_T \cdot h$ and the
      $4\times$ vs $3\times$ choice (§0.5 of the prose).
- [ ] Prove refinement monotonicity using only the tower property
      and concavity of $H_{\mathrm{bin}}$.
- [ ] Construct an adversarial $T$ that makes the upper envelope
      tight; explain why no other $T$ does better at that prior.

## Part 5 — Mechanised verification (reproduce)

- [ ] Open `verify.jl` and identify which theorem each `@test`
      block corresponds to.
- [ ] Re-run `julia --project=. verify.jl`; confirm interval-
      arithmetic certificates pass and `verify.json` is bit-identical
      to the committed file.
- [ ] Open `verify_t1_float.py`, `verify_t3_symbolic.py`,
      `verify_t4_population.py`; for each, identify the theorem,
      the witness family, and the tolerance.
- [ ] Mutate one sign in any verifier; confirm the test fails;
      revert.
- [ ] Read the four-tier stress harness used by the broader project
      (`audit/run_external_audit.sh` in `partition-brackets-framework`)
      and explain in one sentence what each tier checks.

## Part 6 — Experiments (reproduce)

For each experiment below: run the script, locate the corresponding
JSON in `experiments/results/`, locate the figure in
`experiments/figures/`, and verify the figure caption against the
JSON.

- [ ] `e1_trees.py` — decision-tree / random-forest sandwich.
- [ ] `e2_vq_proxy.py` and `e2b_marginal_aware.py` — vector
      quantisation; understand why the marginal-aware variant
      sharpens.
- [ ] `e3_wl_bracket.py` — Weisfeiler–Leman bracket on graph
      classification.
- [ ] `e3a_decomposition.py`, `e3b_wl_structural.py` — additive
      decomposition of the bracket on WL.
- [ ] `e3d_arch_audit.py` / `e3d_arch_full.py` — architecture sweep
      (long-pole; GPU recommended; current run is on RunPod).
- [ ] `e3e_robust_lemma.py` — L11 honest-looseness witness
      (Cora / Citeseer; bound never violated, looseness up to
      $\sim 7$ orders of magnitude; understand the
      $\Delta_{\max} = 168$ sum-aggregation cause).
- [ ] `e3f_richer_init.py` — sensitivity to initialisation richness.
- [ ] `e4_duel.py`, `e5_scatter.py` — pairwise duel and scatter
      visualisations.
- [ ] `e6_cost.py`, `e6_nas.py`, `e6_nas_v2.py` — cost vs bracket
      under neural architecture search.
- [ ] `e7_pop_concentration.py` — UCI Adult, $K = 400$ bootstrap
      reps, 7 subsample sizes; verify ratio
      bound$/\widehat\Delta_{p95} \in [2.53, 2.94]$ (geomean $2.72$).
- [ ] `eK_falsification_protocol.py` — Kochenderfer-style
      falsification screen; verify the 408-row classification
      $121/89/198$ (falsified/verified/inconclusive).

## Part 7 — Adversarial audit (the discipline rule)

For every theorem and every experiment, answer in writing:

- [ ] What does the statement *actually* say (no informal slippage)?
- [ ] What is the tightest counter-example or kill condition?
- [ ] What calibrated confidence does it deserve
      (`HIGH` / `MEDIUM` / `LOW` / `UNVERIFIED`)?
- [ ] Which adjacent claim does it falsify if pushed?

Then:

- [ ] Match your answers against the audit table in
      `future-work/07-three-paper-arc-master-plan.md` §1.

## Part 8 — Reading list (in order)

- [ ] Cover & Thomas, *Elements of Information Theory*, Ch 2, 17.
- [ ] Devroye, Györfi, Lugosi, *A Probabilistic Theory of Pattern
      Recognition*, Ch 1, 2.
- [ ] Hellman & Raviv (1970), *Probability of error, equivocation,
      and the Chernoff bound*.
- [ ] Feder & Merhav (1994), *Relations between entropy and error
      probability* (see `feder.md` in repo root for full text).
- [ ] Han & Verdú (1994), *Generalising the Fano inequality*
      (see `fano-inequality.md`).
- [ ] Jaynes (1957), *Information theory and statistical mechanics*.
- [ ] Xu, Hu, Leskovec, Jegelka (2019), *How Powerful are Graph
      Neural Networks?* (`background/arXiv-1810.00826v3/`).
- [ ] Morris et al. (2019), *Weisfeiler and Leman go neural*
      (`background/arXiv-1810.02244v5/`).
- [ ] This paper's `notes/paper-arxiv-review/13-bayes-entropy-
      sandwich-literature-note.md`.

## Part 9 — Definition of "done"

You can claim reproduction of this paper when, without notes:

- [ ] You can state Theorem 1 and sketch both halves of the proof
      in ten minutes.
- [ ] You can re-run `make`, `verify.jl`, the three Python
      verifiers, and every script in `experiments/` on a clean
      checkout; all artefacts match committed JSON / PDF figures.
- [ ] You can name one experiment whose looseness is large and
      explain why it is *honest* rather than a bug.
- [ ] You can name two open problems from
      `future-work/05-sequel-paper-plan.md` (or
      `06-kwl-bracket-paper-roadmap.md`) and say which theorem in
      this paper each one would extend.

---

*End of checklist. If a box resists ticking for more than one work
session, file an issue or open a discussion thread before guessing
your way past it.*
