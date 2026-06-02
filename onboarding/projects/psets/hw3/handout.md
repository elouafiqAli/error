# HW3 handout — T1 verifier from scratch

**Due:** 2 days. **Points:** 100. **Prerequisite:** HW1 (`hbin`).

You will *implement the binary-entropy bracket of Theorem 1 yourself*,
without depending on M2's reference `bracket.py`, and then **verify
the bound numerically** by random sampling. This is the canonical
"calibrate by adversarial generation" pattern that recurs throughout
the paper.

Theorem 1 (recap):

$$
H_{\mathrm{bin}}^{-1}(H(Y\mid\Pi)) \;\leq\; \varepsilon(\Pi) \;\leq\; \tfrac{1}{2}\, H(Y\mid\Pi),
$$

where $H(Y\mid\Pi) = \sum_C q_C \, H_{\mathrm{bin}}(e_C)$ and
$\varepsilon(\Pi) = \sum_C q_C \, e_C$.

You will reuse `hbin` from HW1 only. Everything else you build.

---

## Q1 — `hbin_inverse(h)` via bisection (25 pts)

### Q1.1 — Implement (15 pts)

In [`starter/q1_hbin_inverse.py`](starter/q1_hbin_inverse.py),
implement bisection on the **increasing branch** $[0, 1/2]$.

### Q1.2 — Round-trip test (5 pts)

The test (`tests/test_q1.py`) checks
$| \, H_{\mathrm{bin}}^{-1}(H_{\mathrm{bin}}(\varepsilon)) - \varepsilon \, | < 10^{-9}$
for $\varepsilon \in \{0.05, 0.10, 0.20, 0.30, 0.40, 0.50\}$.

### Q1.3 — Distinguish (5 pts)

In `writeup.md` §Q1.3 explain in two sentences why you cannot just
solve $H_{\mathrm{bin}}(p) = h$ symbolically for $p$. (Hint: what
class of function is $H_{\mathrm{bin}}$, and what does "transcendental
equation" mean here?)

---

## Q2 — Bracket endpoints and envelope plot (25 pts)

### Q2.1 — `upper(h)` and `lower(h)` (5 pts)

In [`starter/q2_bracket.py`](starter/q2_bracket.py):

```python
def upper(h: float) -> float:
    # TODO(student): return h / 2.
    ...

def lower(h: float) -> float:
    # TODO(student): return hbin_inverse(h).  Reuse from Q1.
    ...
```

### Q2.2 — Envelope plot (15 pts)

In [`starter/q2_plot.py`](starter/q2_plot.py), plot the two curves
$h \mapsto h/2$ and $h \mapsto H_{\mathrm{bin}}^{-1}(h)$ on $h \in [0,1]$,
shade the slack region in between, and save to
`plots/q2_bracket_envelope.png`.

### Q2.3 — Visual reflection (5 pts)

In `writeup.md` §Q2.3, answer in two sentences:

a) Where is the slack widest?
b) Where is it zero?

---

## Q3 — Random-sample verifier (25 pts)

### Q3.1 — Implement `random_partition_stats(rng, m, n)` (12 pts)

In [`starter/q3_verifier.py`](starter/q3_verifier.py): sample a random
partition profile (cell masses $q_1, \dots, q_m$ and per-cell errors
$e_1, \dots, e_m$) and return $(\varepsilon, H)$.

```python
def random_partition_stats(rng, m, n) -> tuple[float, float]:
    # TODO(student):
    # 1) sample cell sizes via rng.multinomial(n, [1/m]*m); recompute q_i = size_i / n.
    # 2) sample per-cell errors e_i ~ Uniform[0, 1/2] (since e_C ≤ 1/2 by Bayes).
    # 3) compute ε = Σ q_i e_i and H = Σ q_i H_bin(e_i).
    # 4) return (ε, H).
    ...
```

### Q3.2 — `verify_bracket(num_samples=10_000)` (8 pts)

```python
def verify_bracket(num_samples=10_000, m_max=5, n=200, seed=0):
    # TODO(student):
    # for trial in range(num_samples):
    #   m = rng.integers(2, m_max + 1)
    #   eps, H = random_partition_stats(rng, m, n)
    #   assert lower(H) - 1e-9 <= eps <= upper(H) + 1e-9
    # return True
```

### Q3.3 — Falsifier (5 pts)

In `writeup.md` §Q3.3, name **two** ways the bracket *could* be
violated by a buggy implementation. (Hint: think about what could
make $e_i > 1/2$ slip through, or what happens if you forget the
$q_i$ weights.)

The test runs `verify_bracket(num_samples=2000)` and asserts True.

---

## Q4 — Grid-search $w^\ast$ and $\varepsilon^\ast$ (15 pts)

### Q4.1 — Implement (10 pts)

In [`starter/q4_wstar.py`](starter/q4_wstar.py):

```python
def find_w_star(grid=5000) -> tuple[float, float]:
    # TODO(student):
    # eps_grid = np.linspace(1/grid, 1/2 - 1/grid, grid)
    # H_grid = np.array([hbin(e) for e in eps_grid])
    # slacks = H_grid / 2.0 - eps_grid    # = upper - lower (eps acts as lower)
    # idx = np.argmax(slacks)
    # return float(eps_grid[idx]), float(slacks[idx])
```

The test (`tests/test_q4.py`) checks $\varepsilon^\ast \in (0.199, 0.201)$
and $w^\ast \in (0.160, 0.162)$. Tighter bounds are extra credit.

### Q4.2 — Two-decimal estimate (3 pts)

In `writeup.md` §Q4.2 write $\varepsilon^\ast$ and $w^\ast$ to 4
decimals. (Hint: paper gives $1/5$ and $\approx 0.1610$.)

### Q4.3 — False lead (2 pts)

The grid-search returns $\varepsilon^\ast$, but a slick reading of
Theorem 1 might suggest $\varepsilon^\ast = 1/4$ (because that maximises
$H_{\mathrm{bin}}(e)$ on $[0, 1/2]$? no — that maximum is at 1/2).
In `writeup.md` §Q4.3 explain in two sentences why the *slack-maximum*
is not at the same place as the *entropy-maximum*. (This is the
canonical false lead — many students conflate the two.)

---

## Q5 — Writeup + calibration (10 pts)

Same convention as HW1/HW2. Mis-calibration penalty doubled.

Required entries: $\varepsilon^\ast$, $w^\ast$, "the bracket holds
under random sampling", at least one HIGH and one LOW.
