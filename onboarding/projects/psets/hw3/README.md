# HW3 — Build the T1 verifier from scratch on a 3-cell example

> **Stub.** README only; handout / starter / tests will be fleshed
> out after HW1+HW2 shapes are validated.
>
> **Pitch.** From HW2 the student has $H(Y\mid\Pi)$. Now build the
> *T1 verifier*: for a 3-cell uniform-mass partition with given
> $\{e_C\}_C$, compute the upper envelope
> $\sum_C q_C \cdot 2 \mathrm{Hbin}^{-1}(2 e_C)$, the lower envelope,
> and the slack $w(\Pi)$. Sweep $\varepsilon \in [0, 1/2]$ and
> reproduce $w^*$ at $\varepsilon^* = 1/5$.

**Time.** 2 days. **Points.** 100.

## Planned questions

| Q | Topic | Pts |
|---|---|---|
| 1 | Implement `hbin_inverse(h)` via bisection | 20 |
| 2 | Implement `bracket(partition)` returning `(lower, upper, slack)` | 25 |
| 3 | Reproduce $w^* \approx 0.1610$ at $\varepsilon^* = 1/5$ | 20 |
| 4 | Mutate → fail → revert: 3 mutations of `bracket` | 20 |
| 5 | Writeup + calibration | 15 |
