# `julia-theory/` — curriculum

> 12 Pluto notebooks across 4 units. Each notebook is self-contained,
> reactive, and centered on a primary slider. The unit arc takes the
> reader from the most primitive object (binary entropy) to the
> most paper-specific (the MPNN star decomposition).
>
> Reading time: ~30 min per notebook *if* you actually move the
> sliders. ~5 min if you scroll. The point is to deform the curve.

## Unit map at a glance

| Unit | Title | Notebooks | Punchline |
|---|---|---|---|
| I | Information-theory primitives | 01–03 | Hbin, the IT quantities, Fano vs HR |
| II | Bayes error & the two-sided bracket | 04–07 | the central object of the paper |
| III | Refinement, sharpness, tightness | 08–10 | why the bracket can't be tightened |
| IV | MPNN, WL, aggregators | 11–12 | the paper's killer-app machinery |

## Unit I — Information-theory primitives

The smallest possible objects, built three ways (numeric, symbolic,
visual). If a reader cannot move a slider on $H_{\mathrm{bin}}(p)$
and predict where the peak is, no later notebook lands. This unit is
the *gate*; everything else assumes it.

### 01 — Binary entropy `Hbin`

- **Primary slider**: $p \in [0, 1]$, 0.001 step.
- **Builds**: $H_{\mathrm{bin}}(p) = -p \log_2 p - (1-p) \log_2(1-p)$
  numerically; $H_{\mathrm{bin}}'(p) = \log_2 \tfrac{1-p}{p}$
  symbolically via `Symbolics.jl`; both as plots; the derivative as
  a numerical check on the symbolic one.
- **Investigates**:
  - symmetry $H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(1 - p)$,
  - concavity (the second derivative is negative on $(0,1)$),
  - $H_{\mathrm{bin}}(1/2) = 1$ bit,
  - $H_{\mathrm{bin}}'(1/2) = 0$ — the symbolic derivative tells the
    reader *why* the peak is at $1/2$ without hand-calculus.
- **Falsify cell**: replace $\log_2$ with $\log_3$; watch the peak
  height change from $1.0$ to $\log_3 2 \approx 0.631$; deduce that
  the choice of base is a units choice.
- **Edelman moment**: `Symbolics.derivative(H, p)` then `simplify` —
  one line, the textbook identity prints.
- **Status**: ✅ fleshed.

### 02 — Information quantities $H(X)$, $H(Y\mid X)$, $I(X;Y)$

- **Primary slider**: a $2\times 2$ joint distribution $P(X,Y)$
  parametrised on a 3-simplex (3 sliders, sum-to-one constraint).
- **Builds**: all the IT primitives from $P$; the chain rule
  $H(X,Y) = H(X) + H(Y\mid X)$; the symmetric MI
  $I(X;Y) = H(X) + H(Y) - H(X,Y)$.
- **Investigates**:
  - non-negativity of MI; tightness at independence,
  - $H(Y\mid X) = 0 \iff Y$ is a function of $X$,
  - the data-processing inequality on a 3-stage chain (small toy).
- **Falsify cell**: set $P(X=0, Y=0) = -0.1$; watch the IT quantities
  go nonsensical; learn that "probabilities" *as values* are the
  load-bearing precondition.
- **Status**: scaffolded.

### 03 — Fano vs Hellman–Raviv

- **Primary slider**: $p \in [0, 1]$, plus a discrete slider
  $K \in \{2, 3, 4, 5, 10\}$ for the number of classes.
- **Builds**: the Fano bound
  $H(Y\mid \hat Y) \le H_{\mathrm{bin}}(\varepsilon) + \varepsilon \log_2(K-1)$
  and the Hellman–Raviv bound
  $\varepsilon \le \tfrac12 H_{\mathrm{bin}}(\varepsilon)$ for $K=2$;
  plots both as bounds on $\varepsilon$.
- **Investigates**: HR is tighter than Fano on $K=2$; Fano dominates
  for $K \ge 3$ because Hellman–Raviv has *no* multi-class extension
  of the same shape.
- **Distinguish cell**: a one-paragraph X-vs-Y between the two
  inequalities — *what's being bounded*, *which way*, *by what*.
- **Status**: scaffolded.

## Unit II — Bayes error & the two-sided bracket

The unit the paper is named after. By the end the reader can produce
$w^* \approx 0.1610$ and $\varepsilon^* = 1/5$ from a slider, then read
Corollary 2 and recognise the constant.

### 04 — Bayes-error landscape on a 3-cell partition

- **Primary slider**: 3-simplex sliders for $(q_1, q_2, q_3)$ plus
  per-cell sliders for $(e_1, e_2, e_3) \in [0, 1/2]^3$.
- **Builds**: $\varepsilon(\Pi) = \sum_C q_C \, e_C$ and
  $H(Y\mid \Pi) = \sum_C q_C \, H_{\mathrm{bin}}(e_C)$ as the
  pre-bracket objects.
- **Investigates**:
  - $\varepsilon$ is linear in each $e_C$; $H(Y\mid\Pi)$ is concave
    in each $e_C$;
  - what shapes can $(\varepsilon, H(Y\mid\Pi))$ achieve as we vary
    $\{e_C\}$ with $\{q_C\}$ fixed? — preview of Prop 3 (achievable
    region).
- **Status**: scaffolded.

### 05 — The bracket envelope

- **Primary slider**: $\varepsilon \in [0, 1/2]$, 0.001 step, on a
  5-cell uniform-mass family $q_C = 1/5$.
- **Builds**: the upper envelope
  $\sum_C q_C \cdot 2 H_{\mathrm{bin}}^{-1}(2 e_C)$ and the lower
  envelope $H_{\mathrm{bin}}(\varepsilon)$; the slack
  $w(\varepsilon) = \mathrm{upper}(\varepsilon) - \mathrm{lower}(\varepsilon)$.
- **Investigates**:
  - both endpoints meet at $\varepsilon = 0$ (zero error → zero
    entropy);
  - both endpoints meet at $\varepsilon = 1/2$ (totally noisy);
  - somewhere in between the slack peaks — *find it with the slider*.
- **Falsify cell**: change the upper envelope's $\tfrac12$ to $\tfrac13$;
  watch the upper drop below a known HR-saturating witness; restore.
- **Edelman moment**: `Hbin_inverse` defined via `IntervalArithmetic`
  to make the inverse provably correct on a grid.
- **Status**: scaffolded (centrepiece — flesh after 01).

### 06 — Uniform slack $w^*$ and the critical point $\varepsilon^* = 1/5$

- **Primary slider**: $\varepsilon \in (0, 1/2)$ + an "auto-locate"
  toggle that runs `Optim.jl`'s Brent's method to find $w^*$.
- **Builds**: the slack function $w(\varepsilon)$ as a univariate
  smooth function; symbolically derives the critical-point equation
  via `Symbolics.derivative`; numerically solves it.
- **Investigates**:
  - Brent's method converges to $\varepsilon^* \approx 0.2$ from any
    starting point in $(0.05, 0.45)$;
  - the closed-form critical-point equation
    $w'(\varepsilon^*) = 0$ matches the symbolic derivative;
  - $w^* \approx 0.1610$ — the slider reproduces Corollary 2's
    constant.
- **Bonus (appendix link)**: same computation with `Enzyme.jl`
  forward-mode AD instead of Symbolics; one line, same answer; the
  reader sees that there are multiple paths.
- **Status**: scaffolded.

### 07 — The achievable region $(\varepsilon, H(Y\mid\Pi))$

- **Primary slider**: 2D scatter parameter — number of cells $m$,
  number of Monte-Carlo samples $N$; renders the region.
- **Builds**: $N$ random partitions; for each, plots its
  $(\varepsilon, H(Y\mid\Pi))$ point in the plane; overlays the upper
  and lower envelopes.
- **Investigates**:
  - the scatter cloud fills the *region between the envelopes*, not
    a curve — Prop 3 made visual;
  - witnesses for the boundary live at the corners.
- **Status**: scaffolded.

## Unit III — Refinement, sharpness, tightness

This is the "why can't I tighten it" unit. Three notebooks; each
exhibits a witness family that an attempted improvement would have
to break.

### 08 — Refinement monotonicity

- **Primary slider**: a "split cell $C$ into two" widget; the reader
  picks $C$ and a split fraction $\alpha$.
- **Builds**: Π_{\mathrm{coarse}} \to \Pi_{\mathrm{fine}} step by
  step; tracks both bracket endpoints and their interval.
- **Investigates**:
  - the *interval* shrinks (refinement = more info = smaller bracket);
  - individual *endpoints* are NOT monotone — construct the
    counter-example where an endpoint increases (this is PLAN.md
    item 14d false lead, lived in code);
  - in the limit of refinement to the discrete partition (Prop 6),
    both endpoints meet at the realised error.
- **Status**: scaffolded.

### 09 — Tightness witnesses

- **Primary slider**: $\alpha \in [0, 1]$ parametrising the
  Hellman–Raviv-saturating family $\Pi_\alpha^{\mathrm{HR}}$ and the
  Jensen-saturating family $\Pi_\alpha^{\mathrm{J}}$.
- **Builds**: both witness families; for each $\alpha$ plots its
  $(\varepsilon, H(Y\mid\Pi))$ on the achievable-region scatter
  from notebook 07.
- **Investigates**:
  - $\Pi_\alpha^{\mathrm{HR}}$ traces the *upper* envelope as $\alpha$
    sweeps;
  - $\Pi_\alpha^{\mathrm{J}}$ traces the *lower* envelope as $\alpha$
    sweeps;
  - the union of the two traces *is* the boundary of the achievable
    region — Prop 7 made visual.
- **Status**: scaffolded.

### 10 — Unimprovability (Prop 7)

- **Primary slider**: a proposed improved upper envelope
  $\mathrm{upper}'(\varepsilon) = \beta \cdot \mathrm{upper}(\varepsilon)$
  for $\beta \in (0, 1)$.
- **Builds**: overlays the proposed improvement on the
  Hellman–Raviv witness from notebook 09.
- **Investigates**: for any $\beta < 1$, there is an $\alpha$ at
  which $\mathrm{upper}'$ crosses *below* the witness — i.e. the
  attempted improvement *violates a known feasible partition*. The
  slider produces the contradiction live.
- **Status**: scaffolded.

## Unit IV — MPNN, WL, aggregators

The paper's killer-app unit. Two notebooks: the aggregator triple
(the E3 punchline) and the robust constancy lemma.

### 11 — Aggregator triple $r_T = (\Delta_{\max}, 1, 1)$

- **Primary slider**: $\Delta_{\max} \in \{1, 2, 4, 8, 16, 32, 64, 128, 256\}$
  (the maximum graph degree).
- **Builds**: the three aggregator-inflation constants for sum,
  mean, and symmetric-norm; plots the inflated upper envelope
  $r_T(\Delta_{\max}) \cdot \mathrm{upper}(\Pi)$ for each.
- **Investigates**:
  - sum scales linearly with $\Delta_{\max}$; mean and sym-norm are
    constant in $\Delta_{\max}$;
  - on Cora ($\Delta_{\max} = 168$) sum is **7 orders of magnitude
    looser** than mean — the bound is never violated, just *honestly
    loose*. This is the E3 punchline lived in a slider.
- **Distinguish cell**: "honest looseness" vs "a bug" — a 3-line
  X-vs-Y. (Same distinguish-drill as PLAN.md item 14b, in Julia.)
- **Status**: scaffolded.

### 12 — $\varepsilon$-robust MPNN–WL constancy (Lemma 6)

- **Primary slider**: $\varepsilon \in [0, 1]$ — the within-cell
  feature distortion budget.
- **Builds**: a toy graph (e.g. $C_6$ with 1-WL color refinement);
  for each cell of the WL partition, perturbs node features by
  $\le \varepsilon$ in $\ell_\infty$; runs a 2-layer GIN-style
  aggregation; reports which cells remain constant.
- **Investigates**: the threshold $\varepsilon$ above which a cell
  stops being constant — Lemma 6 made tactile.
- **Status**: scaffolded.

## Appendix (optional, lands after the main 12 are fleshed)

- **A — Matrix calculus for the bracket** (Edelman/Johnson style).
  Compute $\partial w / \partial e_C$ and $\partial w / \partial q_C$
  symbolically; verify with Enzyme; visualise the gradient field on
  the simplex.
- **B — Differential entropy and the continuous bracket**. Optional
  extension of Unit I.
- **C — The Lagrangian of $w^*$**. Solve the optimisation $\max_\Pi w(\Pi)$
  subject to $\sum_C q_C = 1, e_C \in [0, 1/2]$ via KKT; recover
  $\varepsilon^* = 1/5$ from the dual.

## Reading sequence

```
01 ──► 02 ──► 03
 │
 ▼
04 ──► 05 ──► 06 ──► 07
 │            │
 ▼            ▼
08 ──► 09 ──► 10
              │
              ▼
              11 ──► 12
```

The dependency arrows are real: each notebook reuses functions and
visual idioms defined in its parents. The Project.toml is shared, so
the package compile cost is paid once.

## A note on grading

There is none. No tests, no rubric, no submission. If you finish
the curriculum and *feel* the bracket is no longer abstract, the
curriculum has done its job. That is the only metric.
