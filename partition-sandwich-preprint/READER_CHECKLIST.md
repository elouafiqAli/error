# Reader Checklist — Partition-Conditional Entropy Bracket (Paper A)

**Audience.** Senior undergraduate (final-year CS, math, or stats) who has
taken: probability (joint/conditional, expectation, Markov & Jensen), a
first course in machine learning (decision trees, $k$-means, logistic
regression), and basic graph theory (adjacency matrix, BFS). No
measure theory required.

**Goal.** Be able to (a) state and re-derive the main theorem on a
napkin, (b) reproduce every experiment from the paper end-to-end, and
(c) explain the failure modes honestly to a peer.

**How to use this file.** Tick each box as you complete it. The
ordering is the recommended learning path; the "Skip if" tags identify
items that experienced readers may bypass.

---

## 0. Setup — get the artefacts running (1 sitting)

- [ ] Clone the repo and `cd partition-sandwich-preprint/`.
- [ ] Read `README.md` (≤ 10 min) and skim `experiments/REPORTS.md`
      header for the experiment list.
- [ ] Build the PDF: `make`. Confirm it produces `main.pdf` cleanly
      (`pdflatex → bibtex → pdflatex × 2`).
- [ ] Run the bracket verifier: `julia verify.jl` (IntervalArithmetic).
      Read the printed "max upper slack ≈ 0.16096" — that number must
      appear in your head every time you see Theorem 1.
- [ ] `python3 -m venv venv && source venv/bin/activate && pip install
      -r experiments/requirements.txt` (sklearn, numpy, scipy,
      matplotlib, joblib; optional: `torch-geometric`, `ogb` for E3).
- [ ] Run the cheapest experiment to confirm the toolchain:
      `python3 experiments/e1_cart_depth.py`. Look at the
      resulting `experiments/results/e1.json`.

---

## 1. Prerequisite probability & information theory (2–3 sittings)

Recommended companion: `gnn.md` Ch 9–11 in this repo
([reader-monograph/README.md](../reader-monograph/README.md)) covers
exactly this list, in 30–60 min per chapter, with worked exercises.

- [ ] **Binary entropy** $H_b(p) = -p\log_2 p - (1-p)\log_2(1-p)$:
      sketch its graph by hand. Confirm $H_b(0)=H_b(1)=0$,
      $H_b(1/2)=1$, concavity.
- [ ] **Conditional entropy** $H(Y\mid T)$ as an expectation over cells
      of a partition $T$. Write the one-line identity
      $H(Y\mid T) = \sum_t \Pr(T{=}t)\,H_b(\Pr(Y{=}1\mid T{=}t))$.
- [ ] **Bayes error** $\varepsilon^* = \mathbb E[\min(\eta, 1-\eta)]$
      where $\eta(x)=\Pr(Y{=}1\mid X{=}x)$. Convince yourself that no
      classifier beats this on the population.
- [ ] **Fano's inequality (binary form)**: $H_b(\varepsilon) \ge
      H(Y\mid T)$, i.e. error $\ge H_b^{-1}(H)$. Trace the proof from
      Han–Verdú via DPI on the indicator $\mathbf{1}\{Y=\hat Y\}$.
- [ ] **Hellman–Raviv (binary form)**: $\varepsilon^* \le \tfrac12
      H(Y\mid T)$. One-line proof: $\min(p,1-p) \le \tfrac12 H_b(p)$
      pointwise, then take expectation. **Reproduce this proof from
      memory.**
- [ ] **Joint sandwich** $H_b^{-1}(H) \le \varepsilon^* \le \tfrac12 H$.
      Compute the maximum gap (slack) by maximising $\tfrac12 H - H_b^{-1}(H)$
      over $H\in[0,1]$. Confirm the optimiser sits at
      $\varepsilon = 1/5$ and the maximum is $\approx 0.16096$.
- [ ] **Pinsker / KL row of the named-instances table**: derive the
      KL → Bayes bound from $D(p\|q) \ge 2(p-q)^2$.

**Optional but recommended.**

- [ ] Solve exercises 9.1–9.5 and 11.1–11.4 in `gnn.md`.
- [ ] Build the achievable region $\{(H,\varepsilon)\}$ by sampling
      random partitions in `numpy` and scatter-plotting them against
      the two boundaries. (This is essentially E5; do it from scratch
      first, then compare.)

---

## 2. Read the paper actively (1 sitting per section)

Recommended order: §1 → §2 → §8 (skim) → §4 → §6 → §3 → §7 → §11 →
§5 (verification) → §10 (proofs revisited).

- [ ] **§1 Introduction**: list the six contributions (C1–C6) on an
      index card. Identify which experiment instantiates each.
- [ ] **§2 Theorem 1 (partition-conditional bracket)**: read the
      statement, then **close the paper and rewrite it from memory.**
      Iterate until you can produce the four-step Step-1/2/3/4 outline
      from scratch (cell-wise → expectation → minimum-attaining
      predictor → slack constant).
- [ ] **§2 Proposition 1.5 (Achievable region)** — characterise the
      reachable $(H, \varepsilon)$ set; confirm Theorem 1's bracket
      is the tight envelope (lower = Fano boundary, upper =
      Hellman–Raviv ½$H$ line). This is the Phase-1a addition that
      makes the slack constant unimprovable *in the worst case over
      partitions*.
- [ ] **§2 Proposition 6 (Marginal-aware bracket)** — when the
      class prior $\pi_*$ is far from $1/2$, the worst-case slack
      tightens to $w^*(\pi_*) \le w^*$. Reproduce the closed-form
      $w^*(\pi_*)$ derivation and confirm E2b instantiates it on
      UCI Adult ($\pi_* \approx 0.25$).
- [ ] **§3 Corollaries (C-Π refinement, ε* monotonicity)**: verify the
      arithmetic example yourself with a $4{\times}2$ contingency
      table.
- [ ] **§3 Refinement-to-discreteness (Prop refine-discrete)** —
      take $\Pi$ all the way to singletons; verify the bracket
      collapses to $[0, \tfrac12 H(Y)]$ on the training distribution.
      This is the *theoretical* statement behind the E3 cardinality
      collapse you will observe empirically.
- [ ] **§? Proposition 7 (Population extension)** — read the full
      proof (Phase 1a addition). It is the $O(1/\sqrt n)$
      generalisation slack that predicts every small-$n$ failure
      mode in the experiments (E6-NAS digits-bin, E3 singletons).
      Master the Hoeffding + union-bound structure end-to-end.
- [ ] **§? Proposition 3.5 / Unimprovability** — no closed-form
      improvement of the bracket is possible without extra
      assumptions; understand the Hellman–Raviv witnessing family
      $\Pi^{\mathrm{HR}}_\alpha$ and the Fano family
      $\Pi^{\mathrm F}_\varepsilon$ as joint sharpness witnesses.
- [ ] **§4 Mean-squared error and degenerate T3**: confirm
      Theorem 6.MSE collapses to the Bayes/variance identity when the
      label is binary (i.e. T3 is "degenerate" here, not a separate
      result).
- [ ] **§6 Lemma 6′ (ε-robust MPNN–WL constancy)**: identify the slack
      term (the L11 bound), then sketch the sym-norm vs sum-aggregation
      proof on a single page. The **aggregator-typed** wording
      (Phase 1b) makes the bound vary by aggregator: sum picks up the
      $\Delta_{\max}$ factor (loose by ~$10^7$ at $L=3$ on Cora);
      mean and sym-norm avoid it by construction. State all three
      bound forms; identify which aggregator each real architecture
      (GCN, GAT, GIN, SAGE) instantiates.
- [ ] **§7 Optimal-policy table**: locate OP-soft and OP-BH; confirm
      you can read off the bracket value from each policy.
- [ ] **§8 Experiments**: skim all eight. For each, write a one-line
      "what does this prove?" sentence in your notebook.
- [ ] **§11 Conclusion**: re-read the failure-mode paragraph until you
      can name both failure modes (cardinality collapse on near-discrete
      WL partitions; small-$n$ overfitting on the NAS pre-filter) and
      cite the theorem that predicts each (Prop 7 in both cases).

**Critical reading checkpoints (be adversarial):**

- [ ] What is the *tightest counter-example* to Theorem 1 you can
      construct? (Hint: look at the slack-maximiser at $\varepsilon=1/5$.)
- [ ] On which row of the named-instances table does the bound become
      vacuous? Why?
- [ ] Which experiment would **falsify** the theorem if it failed?
      (Answer: E5 achievable-region scatter — every empirical point
      MUST lie inside the bracket envelope. Confirm this is what E5
      tests.)

---

## 3. Reproduce the theory by hand (1–2 sittings)

- [ ] **Reproduce Theorem 1 proof on whiteboard** in 15 minutes,
      uninterrupted, without the paper.
- [ ] **Compute the slack constant** $w^* = \max_H (\tfrac12 H -
      H_b^{-1}(H))$ in `sympy` symbolically AND in `numpy` by
      grid-search; confirm both agree to $10^{-6}$.
- [ ] **Hand-derive C-Π (refinement corollary)** on a 3-cell vs
      6-cell example, computing $\varepsilon^*_\Pi$ from a known
      $\eta(x)$ on $V=\{1,\dots,12\}$.
- [ ] **Hand-derive Lemma 6′** for a path graph $P_4$ with two
      perturbed node features; confirm the bound matches by direct
      enumeration.
- [ ] **Optional**: port the Julia interval-arithmetic verifier
      (`verify.jl`) to one Python check using `mpmath` or
      `interval`. You should reproduce the same $\approx 0.16096$ slack
      number to 14 digits.

---

## 4. Reproduce the experiments end-to-end (3–5 sittings)

For each, the deliverable is: (a) the JSON in `experiments/results/`,
(b) the PDF in `experiments/figures/`, (c) a paragraph in your own
words explaining the result.

- [ ] **E1 — CART depth on UCI Adult**: `python3 e1_cart_depth.py`.
      Confirm CART training error matches $\varepsilon^*_{\Pi_d}$ to
      4 decimals at every depth $d=1,\dots,15$. **Why** does this
      have to hold? (Hint: per-leaf majority IS the in-cell Bayes
      classifier on the training distribution.)
- [ ] **E2 — Logistic-regression-on-cells**: `python3
      e2_logreg_cells.py`. Same exact match for every $k\le 256$.
- [ ] **E2b — Marginal-aware refinement (real data)**: instantiates
      Prop 6. Confirm the marginal-aware ceiling $w^*(\pi_*)$ is
      strictly below $w^*$ on UCI Adult and that the empirical max
      slack respects it.
- [ ] **E3 — WL partition on real graphs**: needs
      `torch-geometric` + `ogb`. Run the citation/social graph
      block. Verify the high-singleton-fraction numbers
      ($m_3/|V|=0.956$ on ogbn-arxiv). Read §8 "What the numbers say
      (honest reading)" to understand why this is reported as a
      cardinality-collapse sanity check, not a substantive bound.
- [ ] **E3a — depth ladder**: confirm bracket monotonicity in $L$ on
      the same graphs; the partition refines, the bracket shrinks
      (or stays put when WL stabilises).
- [ ] **E3b — Cayley/Paley featureless**: `python3
      e3b_structural_wl.py`. Confirm the bracket pins at the
      marginal-entropy ceiling — this is the *correct* outcome
      because $1$-WL is provably blind on these graphs.
- [ ] **E3d — In-vivo audit of Lemma 6′**: verify the
      $\varepsilon$-robust constancy bound is never violated across
      the (Cora, CiteSeer) $\times$ $\delta$ $\times$ $L$ grid.
      Quantify how loose it is (~$10^7$ at $L=3$ on Cora for
      sum-aggregation).
- [ ] **E3d-arch / E3d-arch-full — architecture-vs-WL audit**:
      `runpod/e3d_arch_ogbn_{train,kmeans}.py` (the experiment
      currently finishing on the RunPod pod). Compare GCN / GAT /
      GIN / SAGE at hidden 128, depth 3, 5 seeds across Cora,
      CiteSeer, PubMed, Twitch-EN, ogbn-arxiv. Confirm the
      feat\_gap sign pattern matches §F1′ predictions.
- [ ] **E3f — Richer-than-1-WL initialisation**: confirm that
      degree-init / spectral-init breaks $1$-WL equivalence on
      CiteSeer/PubMed; the bracket tightens accordingly.
- [ ] **E5 — Achievable-region scatter**: `python3
      e5_achievable_region.py`. Confirm empirical max slack agrees
      with analytic $0.16096$ to $\le 1$ ulp of `Float64`.
- [ ] **E6 — Cost comparison**: `python3 e6_cost.py`. Confirm
      bracket evaluation is $20$–$133\times$ cheaper than one CART
      fit. Be honest about the variance across replications.
- [ ] **E6-NAS — bracket as NAS pre-filter**: `python3
      e6_nas_v2.py`. Reproduce *both* the Adult success
      ($\tau=+0.48$) **and** the digits-bin failure ($\tau=+0.11$,
      CI crosses zero). Articulate, in your own words, why
      Proposition 7's $O(1/\sqrt n)$ slack predicts the failure at
      $n_{\rm tr}=1437$.
- [ ] **E7 — Concentration to population bracket**:
      `python3 e7_concentration.py`. Confirm $1.000$ coverage at
      the nominal $0.95$ level and the $\Theta(1/\sqrt n)$ rate.
- [ ] **E-K — Falsification / verification protocol
      (property-testing style)**: `python3
      eK_falsification_protocol.py`. This is the
      **Kochenderfer-style ternary classifier** (each row of every
      prior experiment is labelled **falsified** / **verified** /
      **inconclusive** at threshold $\tau$ on the hypothesis
      "$\varepsilon^* \le \tau$"). Reproduce the headline counts
      (121 / 89 / 198 across 408 rows; E6 at $\tau=0.10$ fully
      falsified; E3 at $\tau=0.25$ scores 11/15 verified). This
      is the closest the paper comes to **property testing** in
      the formal sense: each prior experiment becomes a
      pass/fail/inconclusive *tester* for a Bayes-error claim. Be
      able to explain (a) why the ternary outcome is the honest
      one (the bracket bounds the claim from both sides, so the
      middle zone is genuinely undecidable), and (b) which
      experiments are most/least informative under this lens.

---

## 5. Verification gates (1 sitting)

- [ ] Re-run `julia verify.jl` and `python3 verify_t{1,3,4}_*.py`.
      All should print PASS with zero violations.
- [ ] `make` from `partition-sandwich-preprint/`: PDF must build
      cleanly with no `Reference … undefined` warnings on the
      second `pdflatex` pass.
- [ ] Run `python3 experiments/eK_falsification_protocol.py` (the
      post-hoc Kochenderfer protocol). Confirm the classification
      counts (121 falsified / 89 verified / 198 inconclusive across
      408 rows) match `experiments/results/eK.json`.

---

## 5b. Property-testing / falsification lens (E-K, important)

The bracket gives a **two-sided** bound, so every claim of the form
"$\varepsilon^* \le \tau$" admits three honest verdicts: **falsified**
(the lower endpoint $L > \tau$), **verified** (the upper endpoint
$U \le \tau$), or **inconclusive** ($L \le \tau < U$). This is the
paper's contribution to a *property-testing-style* reading of
experimental claims about Bayes risk.

- [ ] Re-read §E-K and the protocol script
      `experiments/eK_falsification_protocol.py`.
- [ ] For each prior experiment (E1, E2, E3, E3b, E3d, E5, E6,
      E6-NAS, E7), compute the verdict-triple at three thresholds
      $\tau \in \{0.10, 0.25, 0.40\}$. Tabulate on one page.
- [ ] Confirm: E6 at $\tau = 0.10$ is **fully falsified** (the
      bracket already rules out the claim before any training); E3
      at $\tau = 0.25$ scores 11/15 **verified** on the rows that
      are not in the singleton-collapse regime.
- [ ] Pick one **inconclusive** row and explain *why* it is
      inconclusive in two sentences. What additional data (sample
      size, finer partition, prior info) would move it into
      verified or falsified?
- [ ] Connect to formal property testing
      (Goldreich–Ron-style): the bracket is a **non-adaptive,
      sample-efficient, two-sided tester** for the property
      $\{\varepsilon^* \le \tau\}$ over the space of partitions; it
      has zero false positives for "falsified" (one-sided
      soundness: $L > \tau \Rightarrow \varepsilon^* > \tau$ on the
      training distribution) and zero false negatives for
      "verified" (one-sided completeness: $U \le \tau
      \Rightarrow \varepsilon^* \le \tau$); the inconclusive zone
      is the *tolerance band* of the tester, of width
      $\le w^* \approx 0.161$.
- [ ] State (in one sentence) why the tester is **not** a
      polynomial-time property tester in the Rubinfeld–Sudan sense
      (the partition has to be computed, not queried), and what
      sublinear or query-based extension would close that gap.
      This is open and lives in `future-work/`.

---

## 6. Understand the limitations (must do — not optional)

This section is what separates a *reader* from a *citer*. Mastery
means you can defend the paper against each of these objections.

- [ ] **L1 — Binary only.** State exactly which arguments fail under
      multi-class (Hint: the per-cell $\min(p,1-p)$ has no
      $K$-class generalisation that preserves the closed form;
      concave-envelope extensions cost the closed form). Read the
      "Scope" paragraph in §1.
- [ ] **L2 — Population vs sample.** The bracket bounds population
      Bayes risk on the train-set partition; on small $n$, the
      $O(1/\sqrt n)$ generalisation slack of Proposition 7
      dominates. Reproduce a small-$n$ failure on `digits` or any
      $n<2000$ tabular dataset.
- [ ] **L3 — Cardinality collapse.** When $|\Pi|\to n$ (singleton
      cells), the bracket collapses to "every training point is its
      own class" and bounds become tautological. Identify which
      datasets in E3 are in this regime ($m_3/|V|>0.85$).
- [ ] **L4 — Architecture-agnostic.** The bracket is over *partitions*,
      not over *trained models*. It says nothing about the
      optimiser, the loss surface, or generalisation under
      distribution shift. State three things the bracket
      explicitly does NOT predict.
- [ ] **L5 — WL constancy slack.** Lemma 6′ has a non-trivial slack
      from the L11 term that is loose by ~7 orders of magnitude at
      $L=3$ on Cora (dominated by $\Delta_{\max}=168$ factor for
      sum-aggregation). The bound is never violated but is also
      rarely tight.
- [ ] **L6 — NAS surrogate.** The bracket is NOT a universal NAS
      surrogate. It dominates parameter count, but on small data
      with overfitting-prone partition families (deep CART,
      large-$k$ k-means), zero-`lower` architectures must be
      filtered or paired with a held-out split.

---

## 7. Pedagogical exercises (graded difficulty)

(★ easy, ★★ moderate, ★★★ requires synthesis)

- [ ] ★ State Hellman–Raviv and Fano. Write the joint sandwich.
- [ ] ★ Compute $\varepsilon^*_\Pi$ for a $3{\times}2$ contingency
      table by hand.
- [ ] ★★ Construct a partition $\Pi$ on $V=\{1,\dots,10\}$ and a
      label $f$ such that the upper bound is tight
      ($\tfrac12 H = \varepsilon^*_\Pi$). When does that happen?
- [ ] ★★ Construct a partition for which the lower bound is tight
      ($H_b^{-1}(H) = \varepsilon^*_\Pi$). When does that happen?
- [ ] ★★ Show that refining $\Pi$ to $\Pi'$ (every cell of $\Pi'$ is
      a subset of a cell of $\Pi$) cannot increase $\varepsilon^*$.
- [ ] ★★★ Prove the slack constant $\approx 0.16096$ analytically by
      solving the first-order condition. Identify the optimiser
      $\varepsilon=1/5$ from scratch.
- [ ] ★★★ Construct a 6-node graph where $1$-WL gives a single cell
      but $2$-WL gives 3 cells. Compute the bracket for both
      partitions and observe the refinement.
- [ ] ★★★ Replicate the E6-NAS protocol on a NEW tabular dataset
      from the UCI repository. Report ALL five gates honestly,
      including the ones that fail.
- [ ] ★★★ Re-run the **E-K falsification/verification protocol** on
      a held-out experiment of your own design. Produce the
      verdict-triple at three thresholds and identify at least one
      *inconclusive* row whose status would flip under a 10× larger
      $n$ (predicted by Proposition 7).
- [ ] ★★ Derive the marginal-aware slack $w^*(\pi_*)$ of
      Proposition 6 in closed form and plot it as a function of
      $\pi_* \in (0, 1/2]$. Confirm $w^*(1/2) = w^* \approx
      0.161$ and $w^*(\pi_*) \to 0$ as $\pi_* \to 0$.

---

## 8. Recommended companion reading

In order of importance for *this* paper:

- [ ] `gnn.md` Ch 9–11 (probability without measure, Rényi/Fano,
      Hellman–Raviv & Feder–Merhav).
- [ ] Cover & Thomas, *Elements of Information Theory*, Ch 2 (entropy
      basics).
- [ ] Devroye, Györfi, Lugosi, *A Probabilistic Theory of Pattern
      Recognition*, §1–§2 (Bayes risk, $k$-nearest-neighbour).
- [ ] Feder & Merhav 1994 (the original achievable-region paper —
      `feder.md` in this repo).
- [ ] Han & Verdú 1994 / 2000 (Fano via Rényi — `fano-inequality.md`
      in this repo).
- [ ] Xu et al. 2019, *How Powerful are Graph Neural Networks?* (GIN
      paper, for the WL background — `background/arXiv-1810.00826v3/`).
- [ ] Morris et al. 2019, *Weisfeiler and Leman go neural* (k-GNN —
      `background/arXiv-1810.02244v5/`).

---

## 9. Self-test (final exam)

Set a 90-minute timer and answer these on paper without looking at
the manuscript. Score yourself.

- [ ] State Theorem 1 verbatim, with the slack constant.
- [ ] Sketch the 4-step proof.
- [ ] Compute $\varepsilon^*_\Pi$ for a partition you draw on the
      spot.
- [ ] Predict whether the bracket will be tight on (a) deep CART on
      UCI Adult, (b) $1$-WL on a feature-rich citation graph, (c)
      $1$-WL on Cayley. Justify each from the theorem, not from the
      experiments.
- [ ] Name three things the bracket does NOT bound and explain why
      each is out of scope.
- [ ] Sketch the E6-NAS protocol from memory, including the five
      gates and the two-dataset failure pattern.
- [ ] State the three E-K verdicts (falsified / verified /
      inconclusive) and define each in terms of the bracket
      endpoints $(L, U)$ and threshold $\tau$. Name the property
      being tested.
- [ ] State Proposition 6 (marginal-aware bracket) and write down
      $w^*(\pi_*)$ at $\pi_* = 1/4$ from memory.
- [ ] State Proposition 7 (population extension) and identify the
      $O(1/\sqrt n)$ slack term as the predictor of E6-NAS's
      digits-bin failure.

---

## 10. Macro tasks — the "I really get it" rubric

The micro-tasks above are *necessary but not sufficient*. Mastery is
measured by the macro tasks below: each one forces you to **integrate
across chapters / sections / experiments**. The format throughout is:

> *Should be able to …* followed by an *acceptance test* (the
> deliverable you produce that proves you can).

### 10.1 Distinguish concepts (sharpen the boundary)

For each pair, write **half a page** in your own words, with at least
one worked example *and* at least one counter-example that lives on
the wrong side of the boundary.

- [ ] **D1.** $\varepsilon^*$ (population Bayes risk) **vs**
      $\hat\varepsilon^*_\Pi$ (empirical, partition-induced).
      *Acceptance*: name two regimes where they differ by more than
      $0.1$ (small-$n$, singleton-rich) and one where they agree
      to $10^{-4}$ (E1 CART on UCI Adult, $d \le 8$).
- [ ] **D2.** $H(Y\mid T)$ (conditional entropy, the upper-bound
      input) **vs** $I(Y;T)$ (mutual information, the
      Tishby–Zaslavsky / IB quantity). *Acceptance*: prove
      $H(Y\mid T) + I(Y;T) = H(Y)$ and explain why the bracket
      uses the **complement** of $I$, not $I$ itself.
- [ ] **D3.** Fano lower bound $H_b^{-1}(H)$ **vs** Hellman–Raviv
      upper bound $\tfrac12 H$. *Acceptance*: draw both on one axis
      against $H \in [0,1]$; mark the slack-maximiser at
      $H \approx 0.722$ where the gap reaches $w^* \approx 0.161$.
- [ ] **D4.** $1$-WL **vs** $k$-WL ($k \ge 2$). *Acceptance*:
      exhibit one graph pair distinguishable by $2$-WL but not by
      $1$-WL (the canonical CSL$(8,3)$ vs CSL$(8,5)$ Cayley pair);
      explain why the bracket can therefore be loose for $1$-WL on
      these graphs but tight (= zero slack) for $2$-WL.
- [ ] **D5.** Sum-aggregation **vs** mean / sym-norm aggregation.
      *Acceptance*: reproduce the $\Delta_{\max}^L$ vs $1$ Lipschitz
      table of Ch 18 in gnn.md; pick GIN and GCN, compute the
      depth-$3$ ε-robust bound on Cora and explain the ~$10^7$
      ratio.
- [ ] **D6.** Refinement $\Pi' \preceq \Pi$ **vs** independent
      partition. *Acceptance*: prove that $\varepsilon^*_{\Pi'}
      \le \varepsilon^*_\Pi$ for refinement, then construct a pair
      of independent partitions where neither bracket dominates the
      other.
- [ ] **D7.** Bayes risk **vs** training error of an actual
      classifier. *Acceptance*: write the two-line argument that
      CART training error on a partition $\Pi$ equals $\hat\varepsilon^*_\Pi$
      *exactly* (per-leaf majority is the in-cell Bayes rule on
      the train measure). Identify where this stops holding
      (regularised trees, early stopping).
- [ ] **D8.** Property testing in the Goldreich–Ron sense
      (E-K, this paper) **vs** Rubinfeld–Sudan sublinear testing.
      *Acceptance*: state both definitions, identify the
      sample-complexity gap, and write the one open question that
      would close it.
- [ ] **D9.** Closed-form bracket (Theorem 1) **vs** marginal-aware
      bracket (Proposition 6). *Acceptance*: derive both at
      $\pi_* = 0.236$ (UCI Adult) and explain the $\sim 80\times$
      slack tightening.
- [ ] **D10.** Theoretical slack $w^*$ (worst case over partitions)
      **vs** observed slack on a single run (data-dependent).
      *Acceptance*: pick one experiment (E5) and produce a
      scatter-plot histogram of observed slacks; mark the
      theoretical ceiling $w^*$ and the marginal-aware ceiling
      $w^*(\hat\pi_*)$.

### 10.2 Replicate (build it yourself, then compare)

You should be able to **reconstruct each artefact from primitives**
before comparing to the repo. The order is: simplest first, most
expensive last.

- [ ] **R1 — the slack constant from scratch.** In one Python file,
      no library beyond `numpy`: grid-search $H \in [0,1]$ on
      $10^6$ points, evaluate $\tfrac12 H - H_b^{-1}(H)$ (use
      bisection for the inverse), report the max. *Acceptance*:
      $w^* = 0.16096404...$ to 8 digits.
- [ ] **R2 — Theorem 1 by simulation.** Generate $10^6$ random
      partitions of $V = \{1,\dots,n\}$ with $|\Pi| \in [2, 32]$
      and random Bernoulli labels; for each, compute $L, U,
      \hat\varepsilon^*$; assert $L \le \hat\varepsilon^* \le U$
      always. *Acceptance*: zero violations.
- [ ] **R3 — Hellman–Raviv saturation.** Construct
      $\Pi^{\mathrm{HR}}_\alpha$ on $V = \{1,\dots,4\}$
      (Exercise 17.5 in gnn.md). *Acceptance*: verify $U =
      \varepsilon^*$ iff $\alpha \in \{0, 1/2, 1\}$.
- [ ] **R4 — Fano-boundary witness.** Construct the corresponding
      Fano-family witness $\Pi^{\mathrm{F}}_\varepsilon$ where the
      *lower* endpoint is tight. *Acceptance*: $L = \varepsilon^*$
      to $10^{-6}$.
- [ ] **R5 — 1-WL by hand on a 6-node graph.** *Acceptance*:
      independent agreement with `networkx`'s
      `weisfeiler_lehman_graph_hash`.
- [ ] **R6 — Lemma 6′ depth-1 bound on $P_4$.** *Acceptance*:
      enumerate all depth-1 MPNN outputs at $\varepsilon = 0.01$,
      confirm the bound $2 \beta L_{\mathrm{AGG}} \varepsilon$ is
      respected and quantify looseness.
- [ ] **R7 — bootstrap percentile CI.** From scratch, no
      `scipy.stats.bootstrap`: $B = 1000$ bootstrap resamples
      on a toy distribution, report 95% CI. *Acceptance*: width
      within $5\%$ of `scipy.stats.bootstrap`'s output.
- [ ] **R8 — E1 from scratch.** *Acceptance*: per-depth training
      error matches $\hat\varepsilon^*_{\Pi_d}$ to $10^{-4}$.
- [ ] **R9 — E5 achievable region.** *Acceptance*: scatter agrees
      with `experiments/results/e5.json` to plotting precision.
- [ ] **R10 — E-K ternary verdicts.** *Acceptance*: counts on the
      408 rows agree with `eK.json` (121/89/198).

### 10.3 Prove from scratch (no peeking)

For each, set a **15-minute whiteboard timer**, no notes. If you
miss a step, mark the gap and re-attempt the next day.

- [ ] **P1.** Hellman–Raviv (binary form), 3 lines.
- [ ] **P2.** Fano (binary form) via DPI on the error indicator.
- [ ] **P3.** Slack constant $w^* \approx 0.161$ via first-order
      condition; solve for $\varepsilon^\dagger = 1/5$.
- [ ] **P4.** Refinement monotonicity $\Pi' \preceq \Pi \Rightarrow
      \varepsilon^*_{\Pi'} \le \varepsilon^*_\Pi$.
- [ ] **P5.** Marginal-aware slack $w^*(\pi_*)$ (Prop 6) — both
      regimes ($\pi_* \ge 1/5$ interior; $\pi_* < 1/5$ pinned).
- [ ] **P6.** Lemma 6′ (ε-robust constancy) by induction on depth,
      for sym-norm aggregation.
- [ ] **P7.** Prop 7 (population extension) via Hoeffding + union
      bound; identify the $O(1/\sqrt n)$ slack.
- [ ] **P8.** Theorem-1 ↔ E-K equivalence: every Bayes-risk claim
      admits a ternary verdict with one-sided soundness and
      completeness (Prop 20.2 in gnn.md).

### 10.4 Recite (the "café napkin" test)

You meet a colleague at a café. They ask, *off the top of your
head*, no notes, no laptop. You should be able to answer each in
**under two minutes**.

- [ ] **N1.** "What does Theorem 1 say, and what is the slack
      constant?"
- [ ] **N2.** "Why is $\min(p, 1-p) \le \tfrac12 H_b(p)$?"
- [ ] **N3.** "Why does refining a partition only shrink the
      bracket?"
- [ ] **N4.** "Why does the bracket fail on ogbn-arxiv with depth-3
      $1$-WL?" (Cardinality collapse + cell-count almost equals $n$.)
- [ ] **N5.** "Why does sum-aggregation make the WL constancy bound
      loose?" ($\Delta_{\max}^L$ Lipschitz amplification.)
- [ ] **N6.** "What is the marginal-aware slack at $\pi_* = 0.25$?"
      ($\approx 0.005$.)
- [ ] **N7.** "What is the verdict triple in E-K and how is each
      defined?" ($L > \tau$ / $U \le \tau$ / else.)
- [ ] **N8.** "Why is your tester not Rubinfeld–Sudan sublinear?"
      (Computes the partition; reads $O(n)$.)
- [ ] **N9.** "Name three things the bracket does NOT bound."
      (Optimiser quality, distribution shift, model robustness.)
- [ ] **N10.** "Why did E6-NAS succeed on UCI Adult but fail on
      digits-bin?" ($n_{\mathrm{tr}} = 36{,}177$ vs $1{,}437$;
      Prop 7 slack overwhelms the bracket.)

### 10.5 Recite the canon (be familiar with the citations)

For each, you should be able to state the result and *why* this
paper depends on it. **Do not skim the citation; read at least the
abstract and theorem statement of each.**

- [ ] Fano 1961, *Transmission of Information* §2.11 (Fano
      inequality, original form).
- [ ] Hellman & Raviv 1970, *Probability of Error, Equivocation,
      and the Chernoff Bound* (the $\tfrac12 H$ upper bound, exact
      statement).
- [ ] Han & Verdú 1994, *Generalizing the Fano Inequality* (Rényi
      generalisation, used in Ch 10 of gnn.md).
- [ ] Feder & Merhav 1994, *Relations between Entropy and Error
      Probability* (the achievable region, Ch 11 anchor).
- [ ] Cover & Thomas 2006, *Elements of Information Theory* Ch 2
      (entropy basics) and §13 (universal source coding background
      to Han–Verdú).
- [ ] Hoeffding 1963, *Probability Inequalities for Sums of Bounded
      Random Variables* (the concentration tool of Prop 7).
- [ ] Efron 1979, *Bootstrap Methods* + Bickel & Freedman 1981
      (bootstrap consistency for E7).
- [ ] Goldreich, Goldwasser, Ron 1998, *Property Testing and its
      Connection to Learning and Approximation* (the formal
      framework for E-K).
- [ ] Rubinfeld & Sudan 1996, *Robust Characterizations of
      Polynomials with Applications to Program Testing* (the
      sublinear-testing precedent the bracket does **not** yet
      reach; open problem).
- [ ] Xu, Hu, Leskovec, Jegelka 2019, *How Powerful are GNNs?*
      (GIN / WL equivalence; the C2 connection).
- [ ] Morris et al. 2019, *Weisfeiler and Leman go Neural* ($k$-WL
      hierarchy; the sequel paper plan in `future-work/`).
- [ ] Kipf & Welling 2017 (GCN sym-norm aggregator).
- [ ] Hamilton, Ying, Leskovec 2017 (GraphSAGE mean aggregator).
- [ ] Veličković et al. 2018 (GAT attention aggregator).
- [ ] Devroye, Györfi, Lugosi 1996, *A Probabilistic Theory of
      Pattern Recognition* Ch 1–2 (Bayes risk, the textbook
      foundation).
- [ ] Tishby & Zaslavsky 2015, *Deep Learning and the Information
      Bottleneck Principle* (mutual-information view; Ch 15 in
      gnn.md compares).
- [ ] Massey 1994, *Guessing and Entropy* (Ch 14 in gnn.md; the
      alternative scalar to Bayes risk).
- [ ] Blackwell 1953, *Equivalent Comparisons of Experiments*
      (refinement order on partitions; Ch 15 in gnn.md).

---

## 11. Bonus tracks — multi-angle mastery (recommended, not required)

These are the **"don't skim"** tasks. Each one forces you to look at
the same object from at least three different angles. If you can do
3 of the 5 tracks below, you have moved from "knows the paper" to
"could write the next one".

### 11.1 Random variables — three angles

- [ ] **Sample-space angle.** Construct a single probability space
      $(\Omega, \mathcal F, P)$ on which $X, Y, T$ all live as
      *measurable functions*. *Acceptance*: write down $\Omega$,
      $\mathcal F$, and $P$ for the partition-induced setup of
      Theorem 1.
- [ ] **Distribution angle.** Re-derive the same quantities working
      only with the *joint distribution* $P_{X,Y,T}$, never naming
      $\Omega$. *Acceptance*: cross-check that both yield the same
      $H(Y \mid T)$ on a $4{\times}2$ contingency table.
- [ ] **Generator angle.** Prove the partition $T$ generates a
      sub-$\sigma$-algebra $\sigma(T) \subset \mathcal F$ and that
      $\mathbb E[Y \mid \sigma(T)] = \mathbb E[Y \mid T]$.
      *Acceptance*: 5-line proof, no measure-theoretic machinery
      beyond Ch 9 of gnn.md.
- [ ] **Bonus: reproduce three distributions from scratch.** Derive
      the PMF of $\mathrm{Bin}(n, p)$, $\mathrm{Mult}(n; p_1,
      \dots, p_K)$, $\mathrm{Hyper}(N, K, n)$ from first
      principles (count favourable outcomes; normalise).
      *Acceptance*: code and table match `scipy.stats` to $10^{-10}$.

### 11.2 Information theory — three angles + a matrix form

- [ ] **Combinatorial angle.** Re-derive $H_b(p)$ as the
      Shannon–McMillan rate of a Bernoulli source via the
      method of types (Cover & Thomas §11.1).
- [ ] **Variational angle.** Re-derive $H(Y \mid T) = H(Y) - I(Y; T)$
      as a Lagrangian (Tishby IB) and compare to the bracket: the
      bracket bounds $\varepsilon^*$ via $H(Y \mid T)$, the IB
      tunes the *trade-off* with rate $I(X; T)$. Both share the
      same $H(Y \mid T)$ axis.
- [ ] **Matrix angle (bonus).** Express the partition map as a
      stochastic matrix $\mathbf M \in \{0,1\}^{|V|\times|\Pi|}$
      (one-hot cell indicator) and the label vector as
      $\mathbf y \in \{0,1\}^{|V|}$. Show that the in-cell class
      probability vector is $\mathbf p = (\mathbf M^\top \mathbf 1)^{-1}
      \mathbf M^\top \mathbf y$ (Hadamard inverse on the cell counts).
      *Acceptance*: vectorised `numpy` implementation that
      matches the loop-based version of E1 to $10^{-12}$.
- [ ] **Bonus: Jensen's inequality from scratch.** Prove for a
      convex $\varphi$ and a probability vector $\mathbf q$:
      $\varphi(\mathbf q^\top \mathbf x) \le \mathbf q^\top
      \varphi(\mathbf x)$. *Acceptance*: 5-line induction.
- [ ] **Bonus: the data processing inequality** in matrix form.
      Let $\mathbf P$ and $\mathbf Q$ be two stochastic matrices.
      Show $I(Y; \mathbf P \mathbf Q X) \le I(Y; \mathbf P X)$ for
      Markov chain $Y \to \mathbf P X \to \mathbf P \mathbf Q X$.
      *Acceptance*: bridge via mutual-information chain rule.

### 11.3 Graph theory — three angles

- [ ] **Combinatorial angle.** Re-derive the 1-WL stable
      partition by hand on $K_4 \setminus e$ ($4$ vertices, $5$
      edges minus one). *Acceptance*: state the final colour
      classes; explain the role of edge symmetry.
- [ ] **Linear-algebra angle.** Show $1$-WL is upper-bounded by
      the partition induced by the adjacency spectrum (cospectral
      mates are 1-WL indistinguishable iff their adjacency
      eigenspaces coincide). *Acceptance*: state and verify on the
      Schwenk pair (two cospectral non-isomorphic 8-node graphs).
- [ ] **Sheaf angle (advanced bonus).** Frame WL refinement as
      successive pullbacks of a cellular-sheaf section; the stable
      colouring is the *coequaliser* of the depth-$L$ propagation
      diagram. *Acceptance*: half-page diagram + commentary;
      this is purely conceptual, no formal proof required.

### 11.4 Bayes risk — three angles

- [ ] **Decision-theoretic angle.** Express $\varepsilon^*$ as the
      optimal risk under the $0$–$1$ loss; identify the Bayes
      rule.
- [ ] **Information-theoretic angle.** Bracket it between
      $H_b^{-1}(H)$ and $\tfrac12 H$ (Theorem 1).
- [ ] **Variance angle (bonus).** For binary $Y$, $\mathrm{Var}(Y)
      = \pi_*(1-\pi_*) \ge \varepsilon^*$ always. Identify when
      this is tight (trivial partition) and when loose
      (high-purity refinement). *Acceptance*: $\le 5$-line proof
      and one numerical example.

### 11.5 Property testing — three angles

- [ ] **Statistical-test angle.** Frame E-K as a ternary
      hypothesis test on the population claim
      $\varepsilon^* \le \tau$. Identify Type-I / Type-II error
      analogues; observe that the bracket *eliminates* both at the
      cost of an inconclusive zone.
- [ ] **Goldreich–Ron angle.** Frame E-K as a property tester for
      $\mathcal P_\tau = \{ \varepsilon^*_\Pi \le \tau \}$; state
      soundness + completeness + tolerance (Prop 20.2 in gnn.md).
- [ ] **Algorithmic angle (bonus).** Implement the **sublinear
      open variant** of Exercise 20.4: $m = O(k^2 \log(k/\delta) /
      \Delta^2)$ uniform-vertex samples, Hoeffding on per-cell
      counts, ternary verdict on the noisy bracket. *Acceptance*:
      empirical coverage $\ge 1 - \delta$ across $1000$
      simulations.

---

## 12. Anti-patterns, dead ends, and "thinks-it-works-but-doesn't" (read this carefully)

This section lists approaches that **look promising** but fail in
specific ways. Knowing each failure mode in advance saves weeks. The
discipline is: every time you would take one of these paths,
**first** write down the failure mode in your notebook; *then*
decide whether to proceed.

### 12.1 Theory anti-patterns

- [ ] **A1 — "Just generalise to $K$-class."** Looks easy; replace
      $\min(p, 1-p)$ with $1 - \max_k p_k$. **Why it fails**:
      the analogue of $\min(p,1-p) \le \tfrac12 H_b(p)$ for
      multi-class is *not* a closed-form scalar function of
      $H(Y \mid T)$; the tightest known bound is Kovalevsky's
      concave envelope, which has no closed form for $K \ge 3$.
      You can still write an upper bound, but you lose the
      $w^* \approx 0.161$ universal constant. **Lesson**: binary
      is not a placeholder for "we'll do general later"; it is the
      *only* regime where the bracket has a single scalar slack
      constant. Do **not** claim a multi-class generalisation in
      your paper.
- [ ] **A2 — "Use mutual information $I(Y; T)$ instead of
      $H(Y\mid T)$."** Symmetric, intuitive. **Why it fails**:
      $I(Y; T) = H(Y) - H(Y\mid T)$, so the bracket on $I$ is
      just the bracket on $H$ shifted by $H(Y)$ — same content,
      worse interpretation (the slack constant is no longer
      pinned to a fixed point on the $H$-axis). **Lesson**: the
      bracket lives natively on the *conditional-entropy axis*,
      not the mutual-information axis. Choosing the right scalar
      makes the constant interpretable.
- [ ] **A3 — "Improve the slack with KL divergence."** Pinsker
      gives $D(p\|q) \ge 2(p-q)^2$, so $|p-q| \le \sqrt{D/2}$.
      **Why this is not an improvement**: Pinsker bounds the
      *predictor's regret*, not the Bayes risk. The pointwise
      $\min(p,1-p) \le \tfrac12 H_b(p)$ is already tight at
      $p \in \{0, 1/2, 1\}$; no scalar improvement in $H$ alone
      is possible (Theorem 17.6 in gnn.md). **Lesson**: don't
      conflate regret bounds with Bayes-risk bounds.
- [ ] **A4 — "Use Rényi entropy $H_\alpha$ to tighten."** For
      $\alpha \ne 1$, Han–Verdú gives a *family* of Fano-style
      lower bounds. **Why it fails as an improvement**: the
      family is tight at $\alpha = 1$ (Shannon) for the binary
      case; choosing other $\alpha$ trades off cleanly only when
      the alphabet is large or the prior is highly skewed.
      Marginal-aware Prop 6 is the *operational* equivalent for
      this paper.
- [ ] **A5 — "Strict equality MPNN/WL constancy."** Folklore but
      vacuous: real GNNs have noise (positional encodings,
      dropout, random init), so the strict-equality lemma is
      never invoked in practice. **Why this is a trap**: a
      reviewer can always point to a noise term and dismiss the
      bound. **Lesson**: always state the ε-robust form
      (Lemma 6′) with the aggregator-typed Lipschitz constant.
- [ ] **A6 — "Refine $\Pi$ to a singleton partition for a
      perfect bracket."** Looks like a free win:
      $\varepsilon^*_{\Pi^\delta} = 0$. **Why it fails**: the
      bracket is now on the *training distribution* only; the
      population gap is $O(1/\sqrt n)$ (Prop 7). On any
      meaningfully-sized graph this kills any predictive
      content. **Lesson**: cardinality collapse is real and
      observed (E3 on ogbn-arxiv, $m_3/|V| = 0.956$).
- [ ] **A7 — "Theorem 1 is a generalisation bound."** **It is
      not.** It bounds the *training-distribution* Bayes risk on
      the train-set partition. Prop 7 + finite-sample
      concentration is what lifts it to a generalisation
      statement. **Lesson**: don't quote Theorem 1 as a
      generalisation bound in talks; quote Theorem 1 + Prop 7
      together.

### 12.2 Empirical anti-patterns

- [ ] **A8 — "Use the bracket as a NAS surrogate everywhere."**
      Works beautifully on UCI Adult ($\tau = +0.48$); fails on
      digits-bin ($\tau = +0.11$, CI crosses zero). **Why**:
      Prop 7's $O(1/\sqrt n)$ slack overwhelms the bracket at
      $n_{\mathrm{tr}} = 1437$. **Lesson**: gate any NAS use on
      $n_{\mathrm{tr}} \ge 5000$ (cf. Exercise 19.2 in gnn.md);
      below that, fall back to held-out validation. The paper
      reports both halves of this honestly — do the same.
- [ ] **A9 — "Compare bracket to test accuracy."** *Wrong axis.*
      The bracket bounds $\varepsilon^* = 1 - \mathrm{Acc}^*$
      where $\mathrm{Acc}^*$ is the *optimal* accuracy on the
      train distribution. Test accuracy is bounded by
      $\mathrm{Acc}^* - O(1/\sqrt n)$ (Prop 7) but not equal.
      **Lesson**: always compare to *training-distribution Bayes
      proxy*, not held-out test error. Use E1 (CART training
      error) as the apples-to-apples comparator.
- [ ] **A10 — "Aggregate the bracket across datasets / seeds /
      depths into a single scalar."** Tempting; loses signal.
      **Why**: the slack distribution is **bimodal** — most rows
      sit at $\le 0.05$, a few outliers near $w^* \approx 0.161$
      (E3b structural rows). Mean-aggregation hides this.
      **Lesson**: always report the **distribution** (histogram,
      max, median) and never just the mean.
- [ ] **A11 — "Use the bracket on regression targets."** The
      bracket is binary-only. The MSE row of Theorem 6 (T3) is
      *degenerate* for binary $Y$ (collapses to the
      Bayes/variance identity); for continuous targets, the
      analogue is a separate result not yet in this paper.
      **Lesson**: do not silently re-use the binary code on
      continuous targets. If you need regression, that is
      Paper B (variance instances of the φ-bracket).
- [ ] **A12 — "Plot $\varepsilon^*$ vs depth $L$ and conclude WL
      converges."** Looks convincing; but the curve is the
      *bracket lower endpoint*, which monotonically shrinks just
      because $|\Pi|$ grows with $L$ (cardinality collapse, not
      WL convergence). **Lesson**: gate any WL-convergence
      claim on a *cardinality-controlled* depth ladder (E3a),
      not raw $L$.
- [ ] **A13 — "Sum-aggregation is fine on ogbn-arxiv because the
      bound is never violated."** Technically true, but the
      bound is loose by $\sim 10^7$ (Cora, $L=3$); the bound
      having no empirical bite is **worse**, not better, than a
      tighter-but-occasionally-violated bound. **Lesson**: tight
      bounds with rare violations beat loose bounds that always
      hold; report the looseness factor next to every bound.
- [ ] **A14 — "Use the empirical $\hat\pi_*$ in Prop 6 without a
      CI."** The marginal-aware $w^*(\pi_*)$ is plugged with
      $\hat\pi_*$, which has its own $O(1/\sqrt n)$ slack.
      **Why this matters**: at $\pi_* = 0.236 \pm 0.01$, the
      slack constant changes from $0.002$ to $0.005$ — a $2.5\times$
      relative shift. **Lesson**: report $w^*(\pi_*)$ with the
      bootstrap CI on $\hat\pi_*$ propagated through.

### 12.3 Pipeline anti-patterns

- [ ] **A15 — "Compute the bracket on raw float features without
      any cell-binning."** The cells $|\Pi|$ become $n$ (every
      vector unique). Cardinality collapse instantly. **Lesson**:
      always partition first (CART, $k$-means, WL), then bracket.
- [ ] **A16 — "Skip the Julia verifier because the Python
      check passes."** The Julia verifier uses
      `IntervalArithmetic` for *certified* slack; the Python
      verifier uses `float64`. **Why both matter**: differences
      occasionally surface at the $10^{-16}$ level; for a
      machine-checked claim, only the Julia verifier is the
      ground truth. **Lesson**: run both; certify only the Julia
      output.
- [ ] **A17 — "Re-run E5 with a different RNG to check
      reproducibility."** Fine, but the **slack constant** is
      RNG-independent ($w^* = 0.16096...$ is a closed-form
      analytic value). **Lesson**: distinguish RNG-dependent
      outputs (scatter pattern) from RNG-independent invariants
      (the slack constant). Only the former needs reproducibility
      seeds.
- [ ] **A18 — "Commit only at the milestone."** The repo
      discipline (`.github/copilot-instructions.md`) is **commit
      at every gate, milestone, or feature**. Multi-day work that
      lives in a single commit loses bisectability and
      audit-trail. **Lesson**: small atomic commits; the
      `git log` should read as a narrative.

### 12.4 Reading anti-patterns

- [ ] **A19 — "Read Theorem 1 once, then move on."** Mastery
      requires you to *rewrite the four-step proof from memory*
      until you can do it under 5 minutes. **Lesson**: schedule
      three spaced repetitions over a week.
- [ ] **A20 — "Skim the limitations section."** This is the
      most-cited section by reviewers. **Lesson**: each
      limitation L1–L6 (§6 above) is **must-know**, not
      optional.
- [ ] **A21 — "Cite Prop 3.6 in a Lean-formalised theorem."**
      Prop 3.6 is paper-tier (not Lean-formalised). Either
      restrict to $P_f = 1/2$ (§2.4 Bridge, Theorem 12.5 in
      gnn.md, full Lean), re-derive in Lean, or annotate with
      `trust-tier: paper`. **Lesson**: never silently rely on
      paper-tier results in machine-checked theorems.
- [ ] **A22 — "Treat E-K verdicts as binary by collapsing
      inconclusive → reject."** Reintroduces $O(w^*) \approx
      30\%$ false-positive rate for falsification (Exercise 20.6
      in gnn.md). **Lesson**: ternary verdicts are calibrated
      honesty; do not collapse for a cleaner table.

---

## 13. Final synthesis (one sitting, after everything above)

- [ ] **S1.** Write a 1500-word **review article** for an
      undergraduate audience that explains the paper *without*
      reciting it. Cover: motivation, theorem, proof sketch, one
      reproduced experiment, two limitations, one open direction.
- [ ] **S2.** Produce a **single slide** ($\le 6$ bullets, one
      figure) that you could present at a journal club. It
      should include the slack constant $w^* \approx 0.161$, the
      bracket, one experimental headline, and one honest failure
      mode.
- [ ] **S3.** **Teach one peer** the proof of Theorem 1 in 30
      minutes; have them rewrite it for you in their own words.
      This is the only test that catches gaps in your understanding
      that exercises do not.

---

If you scored ≥ 80%, you have mastered Paper A. Welcome aboard.
