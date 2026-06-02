# HW1 handout

**Due:** 1 day after assignment. **Late budget:** 2 days, drawn from
the global 6-day pool. **Points:** 100. **Submit:** see
[`README.md`](README.md) §Submission.

Throughout this PSet, $H_{\mathrm{bin}}: [0,1] \to [0,1]$ denotes the
binary entropy *in bits*:
$$
H_{\mathrm{bin}}(p) = -p \log_2 p - (1-p) \log_2 (1-p),
$$
with the convention $0 \log_2 0 = 0$.

The Bayes error of a Bernoulli$(p)$ coin is $\varepsilon(p) := \min(p, 1-p)$.

The Hellman–Raviv inequality (for a single Bernoulli) is
$$
\varepsilon(p) \;\le\; \tfrac12 \, H_{\mathrm{bin}}(\varepsilon(p)) \quad \forall p \in [0,1]. \tag{HR}
$$

You will *use the paper's own statement and numbering*: any quote
goes with a `(\eqref{...} or §N.M)` pointer.

---

## Q1 — Binary entropy properties (20 pts)

### Q1.1 — Written (8 pts)

Prove the following four properties of $H_{\mathrm{bin}}$, each in
**at most 4 lines**. Do not cite Mathlib or any library — derive
from the definition.

a) (2 pts) $H_{\mathrm{bin}}(0) = H_{\mathrm{bin}}(1) = 0$.
b) (2 pts) $H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(1-p)$.
c) (2 pts) $H_{\mathrm{bin}}(1/2) = 1$.
d) (2 pts) $H_{\mathrm{bin}}$ is strictly concave on $(0, 1)$. (You
   may quote that $-x \log x$ is strictly concave.)

### Q1.2 — Coding (12 pts)

In [`starter/q1_hbin.py`](starter/q1_hbin.py), implement:

```python
def hbin(p: float) -> float:
    """Binary entropy in bits. hbin(0) = hbin(1) = 0 by convention."""
    # TODO(student): 3 lines.
```

The unit test (`tests/test_q1.py`) checks:

- `hbin(0) == hbin(1) == 0`
- `hbin(0.5) == 1.0` to within `1e-12`
- `hbin(p) == hbin(1 - p)` for 100 random `p ∈ (0, 1)`
- the value of `hbin(0.1)` matches `0.46899559358928133` to `1e-12`

**Anti-pattern penalty (–4 pts):** importing `scipy.stats.entropy` or
similar. The point is to write it yourself.

---

## Q2 — Bayes error of a coin (15 pts)

### Q2.1 — Written (7 pts)

a) (3 pts) Show that for $p \in [0,1]$, the optimal *deterministic*
   classifier is "predict $\arg\max_y \Pr[Y=y]$", and its expected
   error is $\min(p, 1-p)$.
b) (2 pts) Show that any *randomised* classifier has at least the
   same error. (This is the easy direction; one sentence suffices.)
c) (2 pts) Compute $\varepsilon(0.3)$ and explain in one line why
   $\varepsilon(0.7)$ has the same value.

### Q2.2 — Coding (8 pts)

Implement `bayes_error(p)` in
[`starter/q2_bayes.py`](starter/q2_bayes.py). One line of code.
The unit test checks $\varepsilon \le 1/2$ and $\varepsilon(p) =
\varepsilon(1-p)$ on a grid.

---

## Q3 — Verify Hellman–Raviv on a grid (30 pts)

### Q3.1 — Written (10 pts)

a) (4 pts) Show that (HR) holds with **equality** at $p = 0$ and
   $p = 1$ (trivially) and *fails to saturate* anywhere in $(0, 1)$.
   *Hint:* compare both sides at $p = 1/2$.
b) (4 pts) Define the slack $s(p) := \tfrac12 H_{\mathrm{bin}}(\varepsilon(p)) - \varepsilon(p)$. Show that $s$ is
   symmetric about $1/2$ and attains its maximum somewhere in
   $(0, 1/2)$. (You do **not** need to compute the maximiser
   analytically — that is Q3.3.)
c) (2 pts) State, in one sentence, what the existence of nonzero
   $s$ means physically: *why* is the Hellman–Raviv bound loose for
   the single-coin case?

### Q3.2 — Coding: the verifier (12 pts)

In [`starter/q3_hr_verifier.py`](starter/q3_hr_verifier.py),
implement:

```python
def hr_violations(grid: np.ndarray, atol: float = 1e-12) -> dict:
    """For each p in grid, check whether bayes_error(p) <= 0.5 * hbin(bayes_error(p)).

    Returns
    -------
    {
        "n":          len(grid),
        "violations": int,                # count of p with LHS > RHS + atol
        "max_slack":  float,              # max over grid of (RHS - LHS)
        "argmax_p":   float,              # the p attaining max_slack
    }
    """
    # TODO(student): ~10 lines.
```

The unit test runs the verifier on `np.linspace(0, 1, 10_001)` and
checks:

- `violations == 0`
- `max_slack > 0.10` (the bound is genuinely loose)
- `max_slack < 0.20`
- `0 < argmax_p < 0.5`

### Q3.3 — Coding: the plot (8 pts)

Also in `q3_hr_verifier.py`, implement `plot_envelope(out_path)`
that produces `plots/hw1_q3_envelope.png` with:

- x-axis: $p \in [0, 1]$ (10 001 points)
- two curves: $\varepsilon(p)$ (LHS) and
  $\tfrac12 H_{\mathrm{bin}}(\varepsilon(p))$ (RHS)
- vertical line at `argmax_p`
- legend, axis labels, title

The test checks that the file exists and is non-empty. Visual
quality is graded by the writeup (Q5).

---

## Q4 — Mutate → fail → revert (20 pts)

### Q4.1 — Coding (14 pts)

In [`starter/q4_mutate.py`](starter/q4_mutate.py), implement
**three** mutated verifiers, each one differing from Q3.2 by **one
constant**:

```python
def mutation_A(p):  """Replace 1/2 with 0.4. Should find violations."""
def mutation_B(p):  """Replace H_bin with log2(e) ≈ 1.4427. Should find violations."""
def mutation_C(p):  """Use Bayes error of a 3-class uniform (= 2/3). Should hold (uninformative)."""
```

For each, return the same dict as Q3.2.

The unit test checks:

- `mutation_A` reports `violations > 0`
- `mutation_B` reports `violations > 0`
- `mutation_C` reports `violations == 0` and `max_slack > 0.5`

### Q4.2 — Written (6 pts)

In `writeup.md` §Q4, for each mutation, write **two lines**:

a) *Which step of the published proof does the mutation break?*
   (You may cite the paper's Lemma / Theorem numbers.)
b) *What is the smallest $p$ at which the mutation produces a
   violation, to 3 decimals?* (Read it off your verifier's grid.)

---

## Q5 — Writeup & calibration (15 pts)

Create `writeup.md` with sections §Q1 through §Q4 (one per problem),
each containing your written answers, and a final §Calibration that
lists every nontrivial claim in your writeup and assigns one of
`HIGH / MEDIUM / LOW / UNVERIFIED`. **At least 5 entries.**

Example calibration entry:

> **HIGH** — *"`max_slack` over the grid is 0.1610 to 4 decimals"* —
> verified by `pytest psets/hw1/tests/test_q3.py::test_max_slack` on
> commit `<sha>`.

> **MEDIUM** — *"`argmax_p ≈ 0.2`"* — observed on grid of 10 001
> points; not analytically derived.

Mis-calibration penalty is double weight (see top-level
[`README.md`](../../README.md) §4).
