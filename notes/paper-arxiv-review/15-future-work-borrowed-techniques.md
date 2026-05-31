# Future work — borrowed techniques from the 1994 entropy/error literature

**Date:** 2026-05-31
**Status:** future-work shelf; nothing applied to `PAPER-ARXIV.md` yet.
**Companions:** `13-bayes-entropy-sandwich-literature-note.md`,
`14-attribution-fix-proposal.md`.
**Trigger:** reviewer prompt — scrutinise the 1994 entropy/error papers
(Feder & Merhav; Han & Verdú; Hashlamoun et al.; Massey) and identify
what we can salvage for rigour, lucidity, and reviewer appeal.

This document captures what we *could* incorporate but haven't, so it
isn't lost when context rotates.

---

## Part A — Improvement chart (Feder–Merhav, Han–Verdú, Hashlamoun)

| # | Improvement | Source | Type | Effort | Payoff |
|---|---|---|---|---|---|
| **I-1** | Reframe Prop 3.2 proof as "convex hull contains the conditional point", citing Feder–Merhav Thm 1 proof structure. Both the sandwich and refinement-monotonicity become one unified one-line argument: $H(X\mid Y) = \int H(X\mid y)\,dP(y)$ is a convex combination of per-cell points, hence lies in the convex hull of the per-cell achievable region. | Feder–Merhav 1994, Thm 1 proof | Borrow technique + cite | Low (rewrite Appendix A §"Refinement monotonicity" in 4 lines) | High — unifies §3.2 spine; reveals structural elegance. |
| **I-2** | Restate Theorem 1 as a region statement: $(\varepsilon^{*}_\Pi, H(f\mid\Pi)) \in \tilde A_2 := \{(\varepsilon, H) : 2\varepsilon \leq H \leq h(\varepsilon)\}$. Optionally an inline figure / ASCII sketch of $\tilde A_2$. | Feder–Merhav 1994, Thm 1 | Borrow presentation | Low | Medium-high — sandwich becomes visual; reviewer-friendly. |
| **I-3** | Add closed-form analytic tightness witnesses to Appendix A: one-parameter family with $\alpha$-mass on $P_C = 1/2$ cells and $(1-\alpha)$-mass on pure cells; this saturates $\varepsilon = H/2$ for all $\alpha \in [0, 1]$. Complements the E02 single-row witness. | Feder–Merhav 1994, "tightness" remarks | Borrow construction | Low (3-line paragraph) | High — promotes "tight in one row" to "tight on a 1-parameter family". |
| **I-4** | Add Han–Verdú DPI-on-indicator proof as an alternative derivation in Appendix A: apply DPI for divergence to the deterministic processor $g(v) = \mathbf{1}\{\hat h_\Pi(v) = f(v)\}$ to get $d(\varepsilon^{*}_\Pi \,\|\, \varepsilon^{*}_{\text{prior}}) \leq I(f; \Pi)$. **One-line proof.** Provides a Lean-friendly mechanisation route via the divergence DPI primitive. | Han–Verdú 1994, Thm 2 / Thm 9 | Borrow technique + cite | Medium (new Appendix A subsection ~10 lines; requires defining $d(\cdot\,\|\,\cdot)$) | High — gives `PaMpc.BayesErrorBridge` a cleaner mechanisation route; also enables I-5. |
| **I-5** | Add a "prior-aware" sharper lower bound as Proposition 3.2b (or new Corollary 3.4(5)): when $f$ has imbalanced marginal on $V$, $$d(\varepsilon^{*}_\Pi \,\|\, \varepsilon^{*}_{\text{prior}}) \leq H(f) - H(f\mid\Pi) = I(f;\Pi).$$ Strict refinement of Theorem 1's lower side. Genuinely tighter than Fano on the imbalanced E02 rows. | Han–Verdú 1994, Thm 9 | New result via borrowed technique | Medium-high (new proposition, proof, mention in Appendix A; ideally one new E02 row demonstrating the gap empirically; Lean adjustment) | **High** — first genuine *quantitative* sharpening of our sandwich. Promotes the paper from "we packaged textbook inequalities" to "we proved a partition-aware sharpening". |
| **I-6** | Cite Feder–Merhav (1994) at the *statement* of Theorem 1 in §3.2, not just after the proof sketch. | Feder–Merhav 1994 | Cite | Trivial | Medium — places result genealogically at first sight. |
| **I-7** | Cite Hashlamoun, Varshney & Samarasooriya (1994) once in Appendix A "Tightness" subsection as: "tighter continuous-density bounds exist (Hashlamoun–Varshney–Samarasooriya 1994); they offer no improvement in our discrete-partition setting." | Hashlamoun et al. 1994 | Cite + dismiss | Trivial | Low-medium — pre-empts reviewer "have you considered HVS?". |
| **I-8** | Massey (1994): **see Part B below** — repurposed. | Massey 1994 | See Part B | — | — |
| **I-9** | Lift Lemma 3.1 (purity ⟺ zero conditional entropy) into the convex-hull language of I-2: $(0, 0)$ is the unique pure-corner of $\tilde A_2$. Cohesive with I-1 and I-2. | Feder–Merhav 1994 | Polish | Trivial | Low — cosmetic but cohesive. |
| **I-10** | In §3.3 Scope, add: "The two-sided bracket is the binary specialisation of the achievable $(\pi, H)$ region of Feder & Merhav (1994, Thm 1) for general $M$; for multi-class $f$ the upper side becomes $\Phi^{-1}(H)$ (Fano-tight) and the lower side becomes $\phi^{*}(\pi)$ (convex-hull-tight). Proposition 3.3 lifts unchanged; multi-class PA-MPC is a routine restatement, not a conjecture." | Feder–Merhav 1994 | Cite + scope clarification | Low | Medium — honest scope, no padded conjecture. |

### Execution order

1. **First pass — safe editorial:** I-1, I-2, I-3, I-6, I-7, I-9, I-10.
   No new math; only rephrasing + citations. Worth doing as a single
   editorial sweep when next visiting §3.2 / Appendix A.
2. **Second pass — genuinely new technical content:** I-4 then I-5.
   These are the substantive improvements. I-5 in particular is the one
   that materially upgrades the contribution claim.
3. **Skip outright:** none (I-8 was redirected to Part B).

### Risks / blockers

- **I-4 & I-5 introduce binary divergence $d(\cdot\,\|\,\cdot)$ into the
  body.** That requires a one-line definition. Acceptable; reviewers
  expect divergence in this corner of the literature.
- **I-5 requires an empirical demonstration row in E02.** Without it,
  the proposition floats. Decide: ship I-5 as Proposition 3.2b with
  empirical demo, or as a §3.4 named conjecture C4 with a designed but
  un-executed experiment.
- **Lean changes for I-4 / I-5.** `PaMpc.BayesErrorBridge` would need
  a divergence-DPI lemma. Mathlib has `kullbackLeiblerDivergence` and
  related; verify before committing.

---

## Part B — Massey (1994) reconsidered

Initial dismissal in `13-bayes-entropy-sandwich-literature-note.md` was
too quick. The *result* doesn't apply to binary, but the *technique*
and the *style* are both worth borrowing.

### B.1 The Jaynes max-entropy argument as a *unifying* lens

Massey's three-line core:

> The set of distributions with $\sum_i i\,p_i = A$ is convex; entropy is
> concave on it; the calculus-of-variations argument (Jaynes 1957) shows
> the maximiser is geometric.

The same template gives **both** halves of our Theorem 1, from a single
Lagrangian.

**Lower side (Fano direction).** Fix $\varepsilon^{*}_\Pi = \varepsilon$.
The set of $(q_C, P_C)$ achieving this is convex; $H(f\mid\Pi) =
\sum_C q_C\,h(P_C)$ is concave on it. Lagrangian:

$$
\mathcal{L} = \sum_C q_C\,h(e_C) - \lambda \sum_C q_C\,e_C - \mu \sum_C q_C
$$

(using $h(P_C) = h(e_C)$ by binary symmetry). Stationarity:
$h'(e_C) = \lambda$ for all $C$ with $q_C > 0$; combined with the
constraint, the maximiser **concentrates** on a single $e_C = \varepsilon$,
giving $H_{\max} = h(\varepsilon)$. Invert: $\varepsilon \geq h^{-1}(H)$.

**Upper side (Hellman–Raviv direction).** Same Lagrangian, opposite
sign on $\lambda$: maximise $\sum_C q_C\,e_C$ subject to fixed $H$.
Since $e \leq h(e)/2$ is strict everywhere except $e \in \{0, 1/2\}$,
the maximiser lives at **the boundary** of the feasible set:
cells with $e_C = 0$ (pure) and $e_C = 1/2$ ($P_C = 1/2$). Mixing them
yields the I-3 one-parameter tightness family.

**Methodological pay-off.** Both halves of Theorem 1 are the *same*
Lagrangian, optimised in opposite directions, with extremals at
**interior** (Fano) vs **boundary** (Hellman–Raviv) of the feasible
set. This is a *cleaner* exposition than two separate proofs. The
Massey idiom makes it explicit; Feder–Merhav implies it via their
$\Phi$ / $\phi^{*}$ envelopes.

**Improvement proposal (call it I-11):** rewrite §3.2 proof sketch as
"one Lagrangian, two directions" — at most a 4-line paragraph; gives
the reader the intuition for *why* the bracket is sharp on both sides.
Cite Massey (1994) and Jaynes (1957) for the technique, Feder–Merhav
(1994) for the explicit envelopes.

### B.2 Massey-style negative result

Massey's §III ("Lack of an Entropic Upper Bound") is a *parallel*
section to §II ("Lower Bound") that proves a non-existence statement
by explicit construction.

**We have an analogous negative statement worth making numbered:**

> **Proposition 3.2c (no closed-form improvement of Hellman–Raviv on
> binary partitions).** *No function $U : [0, 1] \to [0, 1/2]$
> strictly below $H/2$ exists such that $\varepsilon^{*}_\Pi \leq U(H(f\mid\Pi))$
> holds for every binary partition $(\Pi, f)$. In particular, the I-3
> family saturates $\varepsilon = H/2$ for every $\alpha \in [0, 1]$.*

**Improvement proposal (I-12):** promote the I-3 construction from
"tightness remark" to a stated non-existence proposition à la Massey
§III. Doing so converts a positive sharpness claim into the stronger
*"the bound is unimprovable"*, which is what reviewers actually want
to know.

This is a small textual change but a large rhetorical upgrade.

### B.3 Stylistic lessons from Massey's writing

Massey's paper is ~1 page total. Four lessons worth importing into our
style guide:

1. **Brevity discipline.** Each result is one paragraph. The
   Lemma/Theorem-free style ("It follows that …") moves faster than
   our current "**Theorem 1.** *Let … then.* *Proof sketch.* … $\square$"
   pattern. Worth applying selectively to §4–§7 (experimental sections
   where the formal scaffolding is over-engineered).

2. **Quantified slack.** Massey writes "conservative by at most a
   factor of $4/e$". For every bound we state, we should attach a
   *quantified slack*:
   - Upper side: $\tfrac{1}{2}H$ vs $\min(p, 1-p)$ slack is at most
     $\tfrac{1}{2}h(p) - \min(p, 1-p)$; max attained at
     $p = 1 - 1/\sqrt 2 \approx 0.293$ with slack $\approx 0.086$.
   - Lower side: $h^{-1}(H)$ vs $\varepsilon$ slack is at most
     $\varepsilon - h^{-1}(h(\varepsilon)\cdot\alpha)$ for the
     $\alpha$-mixture family; max attained at $\alpha = 1/2$.

   Stating these explicitly costs three lines and signals rigour.
   **Improvement proposal (I-13).**

3. **Abstract carries the theorem.** Massey's abstract states the
   entire result *and* its tightness factor. Our abstract is narrative.
   A Massey-style information-dense first paragraph would help
   reviewers triage on first glance. Candidate rewrite:

   > *PA-MPC, defined as the partition-conditional entropy
   > $H(f\mid\Pi_{\mathcal{A}}(G,L))$, brackets the Bayes error
   > $\varepsilon^{*}$ of any admissible depth-$L$ message-passing
   > predictor by $h^{-1}(\text{PA-MPC}) \leq \varepsilon^{*} \leq
   > \tfrac{1}{2}\,\text{PA-MPC}$, with both sides sharp. We verify the
   > bracket exactly on 1000 small graphs (E02), mechanise the variance
   > shadow in Lean, and …*

   **Improvement proposal (I-14):** abstract rewrite. Independent of
   the §3 edits; can be applied any time.

4. **Counterexamples as first-class.** Massey makes §III parallel to
   §II in section weight. We have non-existence remarks scattered;
   promoting one (I-12) to a numbered result follows the same template.

### B.4 Where Massey's *result* (not just technique) could enter

For multi-class extension (currently out of scope), $E[G(f\mid\Pi)]$ —
the expected number of guesses to identify $f(v)$ ordered by posterior
— is genuinely richer than $\varepsilon^{*}_\Pi$ for $K \geq 3$:

- $\varepsilon^{*}_\Pi$ collapses all residual ambiguity to a single
  scalar.
- $E[G(f\mid\Pi)]$ captures *the structure* of the residual ranking.

Massey's $E[G] \geq (1/4)2^{H} + 1$ would give a partition-indexed
guessing-complexity bound. Honest framing: **interesting if we ever do
multi-class PA-MPC; not currently in scope.**

**Improvement proposal (I-15, conditional):** if multi-class PA-MPC
becomes scope, pair the Feder–Merhav multi-class bracket (I-10) with
the Massey guessing bound as twin operational measures.

### B.5 Summary: Massey-derived improvement proposals

| # | What | Effort | Payoff | Apply when |
|---|---|---|---|---|
| **I-11** | "One Lagrangian, two directions" reframing of Theorem 1 proof | Low | High | Next §3.2 editorial sweep |
| **I-12** | Promote I-3 family to numbered "no closed-form improvement" proposition | Low | Medium-high | With I-3 |
| **I-13** | Quantified slack annotations on every bound | Low-medium | Medium | With I-2 |
| **I-14** | Massey-style information-dense abstract rewrite | Low (1 paragraph) | Medium-high | Independent; any time |
| **I-15** | $E[G(f\mid\Pi)]$ as multi-class operational companion | High (out of current scope) | High (if multi-class scope opens) | Future work; conditional |

---

## Part C — Suggested execution sequence (consolidated)

Recommended ordering when next visiting the paper:

1. **Editorial sweep:** I-1, I-2, I-3, I-6, I-7, I-9, I-10, I-11, I-12,
   I-13. All low-effort; together they upgrade rigour and presentation
   without new mathematical content.
2. **Abstract:** I-14, independently.
3. **New technical content:** I-4 (alternative proof via DPI),
   then I-5 (prior-aware sharper lower bound). Requires Lean changes
   and an E02 demo row; should be planned in concert with experiment
   ledger updates.
4. **Conditional / multi-class:** I-15 only if multi-class PA-MPC enters
   scope.

---

## References (full bibliographic anchors)

- **Feder, M. & Merhav, N.** (1994). Relations between entropy and
  error probability. *IEEE Trans. Inf. Theory* 40(1):259–266.
- **Han, T. S. & Verdú, S.** (1994). Generalizing the Fano inequality.
  *IEEE Trans. Inf. Theory* 40(4):1247–1251.
- **Hashlamoun, W. A., Varshney, P. K. & Samarasooriya, V. N. S.**
  (1994). A tight upper bound on the Bayesian probability of error.
  *IEEE Trans. Pattern Anal. Mach. Intell.* 16(2):220–224.
- **Massey, J. L.** (1994). Guessing and entropy. *Proc. IEEE ISIT
  1994*, p. 204.
- **Jaynes, E. T.** (1957). Information theory and statistical
  mechanics. *Physical Review* 106(4):620–630.
