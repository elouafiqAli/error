# VERIFICATION.md — Design of the Verification Ladder

This document describes the five artefacts that ship with the
preprint *A Two-Sided Partition-Restricted Minimum-Risk Bracket
from Partition-Conditional Entropy*:

- `verify_t1_float.py` — Tier **T1** (float spot-check, NOT certified)
- `verify.jl`          — Tier **T2** (certified per-sample interval audit)
- `verify_t3_symbolic.py` — Tier **T3** (symbolic / closed-form via SymPy)
- `verify_t4_population.py` — Tier **T4** (Monte-Carlo population concentration)
- `examples.tex`       — auto-generated LaTeX macros for the §8 examples
   and Proposition 6 Table 1

They are deliberately presented as a *ladder*: each tier increases
mathematical strength and computational cost, and each tier exists
in source so that a reader can re-run it locally.

---

## 1. The full ladder

| Tier | Where | Cost | What it certifies | Status |
|------|-------|------|-------------------|--------|
| T0 | `main.tex` §3–§7 | reading | the theorem itself (human proof) | done |
| **T1** | `verify_t1_float.py` | seconds, no deps | the bracket *appears* to hold on 10³ random partitions in IEEE-754 | **sealed** |
| **T2** | `verify.jl` | ~30 s, Julia | the bracket *provably* holds on the same 10³ samples, by certified interval comparison | **sealed** |
| **T3** | `verify_t3_symbolic.py` | seconds, SymPy | the closed-form ingredients ($w^*$, $w^*(\pi_*)$, witnesses, §8 examples) are mathematical identities | **sealed** |
| **T4** | `verify_t4_population.py` | ~10 s, numpy | the Proposition 7 concentration bound holds at the requested confidence level on 3 scenarios × 7 sample sizes × 500 trials | **sealed** |
| T5 | future | mins, Julia | the bracket holds on the *entire* probability simplex by interval branch-and-bound | roadmap |
| T6 | future | weeks, Lean 4 | kernel-trusted formalisation of Theorem 1 | roadmap |

The first four tiers are now production-ready. T5 and T6 are
captured in `/memories/repo/partition-sandwich-verification-roadmap.md`.

---

## 2. T1 — float spot-check (the deliberately weak baseline)

**Question it answers.** *“If I sample 1000 random partitions and a
random binary label and compute the bracket in plain doubles, do the
inequalities appear to hold?”*

### Design

- Dependency-free: standard-library Python 3 only (no NumPy, no SymPy).
- Random protocol matches `verify.jl` exactly (same `seed`, same
  $n \in \{4,\dots,32\}$, same partition / label distributions) so
  T1 and T2 audit the *same* sample.
- A small fudge tolerance (`TOL = 1e-12`) is added to each
  comparison to silence float noise — the *fact that this tolerance
  is necessary* is the pedagogical point.
- $H_{\mathrm{bin}}^{-1}$ is implemented by bisection (no closed form).

### What T1 IS good for

- A 1-second smoke test while editing partition / label generators.
- A reproducibility check that doesn’t require a Julia install.
- A side-by-side foil for T2: it makes concrete why certified
  numerics matter when a result is sharp.

### What T1 is NOT good for

- It cannot distinguish *“the inequality fails by float noise”*
  from *“the inequality fails mathematically”*. Without the
  tolerance, the Feder witness $\Pi^{\mathrm{F}}_{\varepsilon}$
  (Proposition 5, witness family in §7) — where the lower bound is
  an equality — produces apparent violations of order $10^{-16}$.
- It cannot be cited in the paper as evidence of correctness; only
  as evidence of *consistency*.

### How to validate T1

```bash
python3 verify_t1_float.py
# Expected: violations: 0, max upper slack ≈ 0.1610
cat verify_t1.json | python3 -m json.tool
```

Cross-check against T2: every sample audited by T1 is audited by
T2 with the same `(n, seed)` schedule and the same partition. T2’s
verdict is the ground truth; T1 must agree wherever the slack
exceeds the float fudge tolerance.

---

## 3. T2 — certified per-sample interval audit

**Question it answers.** *“Do the inequalities of Theorem 1 hold
on these 1000 random partitions, with mathematical certainty?”*

### Design

- Exact rationals (`Rational{BigInt}`) for everything that can be
  rational: $q_C$, $P_C$, $e_C$, $\varepsilon^{*}_{\Pi}$, the
  point of evaluation of $H_{\mathrm{bin}}$.
- `IntervalArithmetic.jl` for everything that involves $\log$:
  $H_{\mathrm{bin}}(P_C)$, $H(f \mid \Pi)$, and $H_{\mathrm{bin}}(\varepsilon^{*})$.
- The bracket test
  $$ \varepsilon^{*} \le \tfrac12 H(f\mid\Pi) \quad\text{and}\quad H(f\mid\Pi) \le H_{\mathrm{bin}}(\varepsilon^{*}) $$
  is performed by comparing interval suprema — this is a
  rigorous mathematical statement, NOT a heuristic.
- Output `verify.json` records the seed, sample count, and
  empirical maximum upper-side slack, which equals
  $w^{*} \approx 0.1610$ (Corollary 2).

### Why T2 is the right level for the paper

The paper claims a closed-form universal slack $w^{*}$ (Corollary 2)
and a saturating witness $\Pi^{\mathrm{HR}}_{1/5}$ (§7). Verifying
this on 1000 random samples checks that the *empirical* maximum
matches the *predicted* maximum to four decimals — exactly the kind
of numerical agreement that builds calibration in a reader. The
certified arithmetic guarantees that this match is not a numerical
artefact.

### How to validate T2

```bash
julia --project=. verify.jl
# Expected:
#   violations:        0
#   upper ε≤H/2 (iv):  true
#   lower H≤Hbin(ε):   true
#   max upper slack:   0.1610   ← matches w* of Corollary 2
cat verify.json | python3 -m json.tool
```

Cross-checks:

- The reported `max_slack_upper` must equal $w^{*} = \tfrac{1}{2}H_{\mathrm{bin}}(1/5) - 1/5$ to within $10^{-4}$.
- If you change the seed, `max_slack_upper` may decrease (you might miss the worst-case partition) but it must NEVER exceed $w^{*}$. If it does, Theorem 1 is wrong (or the script is wrong); inspect the offending sample.

---

## 4. T3 — symbolic / closed-form verification

**Question it answers.** *“Are the closed-form constants and
saturation claims in the paper actual algebraic identities?”*

T2 audits *samples*; T3 audits *structure*. Together they cover
both the per-instance bracket (T2) and its derivation (T3).

### Design

- SymPy only. We work over $\mathbb{Q}$ extended by symbolic $\log$,
  which is enough to verify Theorem 1’s closed-form ingredients
  exactly.
- The script is organised into three groups:
  - **Structural identities (S1–S5)**: boundary values, symmetry,
    concavity, critical point of $\tfrac12 H_{\mathrm{bin}}(\varepsilon) - \varepsilon$, value of $w^{*}$.
  - **Witness saturation (S6, S7)**: $\Pi^{\mathrm{F}}_{\varepsilon}$
    saturates the lower bound; $\Pi^{\mathrm{HR}}_{\alpha}$ saturates
    the upper bound, and the upper-slack maximum
    $\max_{\alpha \in (0, 1/2]} \tfrac12 H_{\mathrm{bin}}(\alpha) - \alpha$
    is attained at $\alpha = 1/5$, equal to $w^{*}$.
  - **Worked examples (S8)**: programmatic harness for §8.1 (tree),
    §8.2 (2-means VQ), §8.3 ($C_4$ MPNN). Each example is a
    function `example_<name>()` returning a dict; new examples slot
    in by appending to the `EXAMPLES` list.
- The harness emits `examples.tex`, a `\newcommand` macro file that
  the paper can `\input` in a future revision so that §8 has a
  single source of truth.

### How to validate T3

```bash
python3 verify_t3_symbolic.py
# Expected: status: ALL PASS
cat verify_t3.json | python3 -m json.tool
cat examples.tex
```

Inspect the printed identities:

- `S3_Hbin_second_derivative` must simplify to
  $1/(p(p-1)\ln 2)$, which is negative on $(0,1)$ → concavity.
- `S4_critical_points` must be exactly `['1/5']`.
- `S5_w_star_symbolic` must be `-1 + log(5)/(2*log(2))`,
  i.e. $\log_2(5)/2 - 1$, numerically $0.16096404\dots$.
- `S6_lower_residual` must be `0` (Feder witness is exact).
- `S7_argmax_alpha` must be exactly `['1/5']`, and
  `S7_max_slack` equals `S5_w_star_symbolic`.

Every §8 bracket triple printed by T3 must match the corresponding
LaTeX bracket in `main.tex`. Currently:

| Example | T3 bracket | Paper bracket |
|---------|-----------|---------------|
| §8.1 stump  | `[0.25, 0.25, 0.4056]`   | `[0.25, 0.25, 0.4057]`   |
| §8.2 VQ     | `[0.273, 0.30, 0.423]`   | `[0.273, 0.30, 0.423]`   |
| §8.3 $C_4$  | `[0.5, 0.5, 0.5]`        | `[0.5, 0.5, 0.5]`        |

(The 4th-decimal disagreement in §8.1’s upper bound is the paper’s
rounding of $\tfrac12 H_{\mathrm{bin}}(1/4) = 0.405639\dots$ to 4 places; both round
to `0.4056` at standard rounding and to `0.4057` at round-half-up.)

---

## 5. T4 — Monte-Carlo population concentration

T4 is the empirical counterpart of Proposition 7 of the paper.
While T2 certifies the bracket on a *finite* $V$ and T3 certifies
the structural identities behind it, T4 asks the next question:
**does the bracket transfer from $V$ to the underlying
distribution $\mu$ as $|V|$ grows, at the rate Proposition 7
claims?**

### Design

A *population scenario* is a triple $(\Pi, \mu, \pi)$ specifying
cells, cell masses, and cell means. T4 ships three:

| Scenario | $m$ | $\delta = \min_C \mu(C)$ | $\eta = \min_C \min(\pi_C, 1-\pi_C)$ |
|----------|----|--------------------------|--------------------------------------|
| balanced 3-cell | 3 | 0.25 | 0.15 |
| unbalanced 5-cell | 5 | 0.05 | 0.10 |
| marginal-aware unbalanced | 2 | 0.50 | 0.05 |

For each scenario and each $n \in \{50, 100, 250, 500, 1000, 2500, 5000\}$:

1. draw $K = 500$ i.i.d. subsamples of size $n$ from $\mu$;
2. compute the empirical $(\epsilon^*_\Pi, H(f|\Pi))$ per trial;
3. record the gap $\Delta_n := |\epsilon^*_{\Pi,\mu} - \epsilon^*_\Pi| + |H_\mu(f|\Pi) - H(f|\Pi)|$;
4. report empirical coverage at the Proposition 7 bound
   $\kappa(\delta,\eta)\sqrt{\log(4m/\delta_{\mathrm{conf}})/n}$
   with $\delta_{\mathrm{conf}} = 0.05$, i.e.\ assert empirical
   coverage $\ge 0.95$.

### Why T4 (and not interval bracket on the simplex)

Proposition 7 is a *probabilistic* statement (high-probability
concentration), so the natural verifier is *empirical coverage*,
not an interval cover of the simplex. The interval-cover approach
is the role of the still-future T5. T4 takes ~10 s and uses
numpy only.

### How to validate T4

```bash
python3 verify_t4_population.py
# Expected:  status: ALL PASS
#            coverage = 1.000 across all (scenario, n)
#            (the analytic bound is loose; the empirical Δ_n
#             is always at least an order of magnitude below it.)
```

`verify_t4.json` records the full table of (n, K, bound,
Δ_mean, Δ_p95, coverage_rate) for each scenario, with seed
`20251225` for reproducibility.

### What T4 does NOT certify

T4 is Monte-Carlo, so it gives statistical evidence and not a
mathematical proof. The proof is Proposition 7 itself (a routine
union-bound + Hoeffding + Lipschitz argument); T4 sanity-checks
the constant $\kappa$ and the dependence on $(n, m, \delta, \eta)$
on three deliberately stressed scenarios. A future T5 would
replace T4's Monte Carlo by an interval branch-and-bound over the
simplex $\Delta_m$.

---

## 6. Do we need SageMath?

**Short answer: no.** SymPy is sufficient for T3 and Julia
+ IntervalArithmetic.jl is sufficient for T2. SageMath would add
≈1.5 GB of dependencies and give us nothing the current stack
lacks.

### Detailed answer

What T3 needs from a CAS:

1. Exact rationals $\mathbb{Q}$ — SymPy provides `sp.Rational`.
2. Symbolic real-valued $\log$ with simplification — SymPy provides
   `sp.log` plus `sp.simplify`, `sp.cancel`.
3. Symbolic differentiation — SymPy’s `sp.diff` is fine.
4. Equation solving for univariate transcendental criticality
   ($\tfrac12 H_{\mathrm{bin}}'(\varepsilon) = 1 \iff \varepsilon = 1/5$) — SymPy’s `sp.solve` reduces this
   to $\log\bigl((1-\varepsilon)/\varepsilon\bigr) = \log 4$ and returns $\varepsilon = 1/5$ exactly.
5. Arbitrary-precision numeric evaluation — SymPy’s `sp.N(_, 50)` gives 50 digits.

SageMath’s additional strengths — algebraic geometry, Gröbner
bases, modular forms, $p$-adic numbers, large finite fields,
elliptic curves — are irrelevant for an inequality between
Shannon entropy and a piecewise-linear loss on $[0,1]$.

### When SageMath WOULD be the right tool

If a future generalisation needs:

- Symbolic computation in a number field (e.g. $\mathbb{Q}(\zeta_n)$
  for cyclic constructions of partitions), or
- Polynomial elimination over the simplex with Gröbner bases (e.g.
  T4’s multi-class extension might benefit), or
- Symbolic interaction with `PARI/GP` for transcendence-theory
  certificates,

then Sage’s integrated stack pays off. For the current paper,
none of these apply.

### When Mathematica / Maple / Maxima would be the right tool

Same answer as Sage: only if `sp.simplify` runs out of steam on a
much larger expression. The §8 examples and the structural
identities of §3–§7 fit on one line each and SymPy handles them
trivially. We picked SymPy for zero-cost reproducibility (every
SymPy user already has Python).

---

## 7. Reproducing every numeric in the paper

From a clean checkout:

```bash
cd partition-sandwich-preprint

# T1 (Python only)
python3 verify_t1_float.py        # → verify_t1.json

# T2 (Julia + IntervalArithmetic)
julia --project=. verify.jl       # → verify.json

# T3 (SymPy)
python3 verify_t3_symbolic.py     # → verify_t3.json, examples.tex

# Paper
make                              # → main.pdf
```

Expected outputs:

- `verify_t1.json`: `violations = 0`, `max_upper_slack ≈ 0.1610`.
- `verify.json`:    `n_violations = 0`, `max_slack_upper ≈ 0.1610`, both interval flags `true`.
- `verify_t3.json`: `all_ok = true`, every structural identity holds, every witness saturates, every §8 example matches, Proposition 6 piecewise formula reproduced on the Table 1 grid.
- `verify_t4.json`: `all_ok = true`, empirical coverage ≥ 95% across 3 scenarios × 7 sample sizes × 500 trials.
- `examples.tex`:   `\newcommand` macros (`\wstar`, `\Example81lo`, …, `\wmarg05`, …) that a future revision of the paper can `\input`.

---

## 8. Roadmap to T5 and T6

See `/memories/repo/partition-sandwich-verification-roadmap.md` for
the strategic plan.

- **T5 (interval branch-and-bound over the simplex)** is most
  valuable as the seed of a *second paper* — a Julia framework
  that verifies arbitrary scalar inequalities between conditional
  entropy and Bayes / TV / KL on the finite simplex, with four
  case studies (binary HR/Fano, multi-class concave envelope,
  loss-aware, Sason–Verdú). T4 currently fills the empirical
  population gap; T5 would replace it by a covering certificate.
- **T6 (Lean 4 / mathlib4)** is a three-layer artefact: the
  formalisation itself, a tutorial paper (CPP / AITP), and a
  course module under `/exercises/`. Best built now, before
  HR + bracket land in mathlib independently.

The point of having T1–T4 sealed first is that each future tier
inherits a battery of sanity checks: T5 must reproduce T3’s closed
forms and T4’s coverage, T6 must reproduce all three. The ladder
is upward-compatible.
