# HW1 — Binary entropy & Hellman–Raviv on a coin

> **Pitch.** Before touching partitions, graphs, or aggregators, the
> student must be fluent with the *single-coin* case: one Bernoulli
> random variable, one binary observation, one Hellman–Raviv bound.
> If the student is not fluent here, every downstream PSet collapses.
>
> **Time.** 1 day. **Points.** 100. **Difficulty.** Warm-up.
> **Prerequisite.** PLAN.md G0 (Roman items I, IV).

## Learning objectives

By the end, the student can:

1. Compute $H_{\mathrm{bin}}(p)$ by hand and in code; explain why it
   is symmetric about $1/2$ and maximised at $H_{\mathrm{bin}}(1/2)=1$ bit.
2. Compute the Bayes error $\varepsilon = \min(p, 1-p)$ of a coin and
   explain the trivial bound $\varepsilon \le 1/2$.
3. State and verify Hellman–Raviv,
   $\varepsilon \le \tfrac12 H_{\mathrm{bin}}(\varepsilon)$, for any
   $p \in [0,1]$.
4. Distinguish *pointwise tightness* from *averaged tightness*: which
   $p$ saturates? which $p$ produces maximum slack?
5. Mutate the Hellman–Raviv inequality (replace the $\tfrac12$ with
   $0.4$, or $H_{\mathrm{bin}}$ with $\log_2 e$); produce a
   counter-example $p$ on a plot; revert.

## Rubric

| Q | Topic | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|---|
| 1 | $H_{\mathrm{bin}}$ properties | 12 | 6 | 2 | 20 |
| 2 | Bayes error of a coin | 8 | 4 | 3 | 15 |
| 3 | Verify Hellman–Raviv on a grid | 18 | 8 | 4 | 30 |
| 4 | Mutate → fail → revert | 14 | 4 | 2 | 20 |
| 5 | Writeup & calibration | 8 | 3 | 4 | 15 |
| **Sum** | | **60** | **25** | **15** | **100** |

## Submission

```
psets/hw1/
├── starter/
│   ├── q1_hbin.py            # fill in TODOs
│   ├── q2_bayes.py
│   ├── q3_hr_verifier.py
│   └── q4_mutate.py
├── tests/                    # do not modify
│   ├── test_q1.py
│   ├── test_q2.py
│   ├── test_q3.py
│   └── test_q4.py
├── writeup.md                # NEW — see handout.md §5
└── plots/                    # NEW — q3 and q4 figures land here
```

Grader runs `pytest psets/hw1/tests/ -v` from repo root.

## Files in this folder

- [`handout.md`](handout.md) — the written problems.
- [`starter/`](starter) — fill in the `# TODO(student)` blocks.
- [`tests/`](tests) — read but do not modify.
- `writeup.md` — to be created by the student.
