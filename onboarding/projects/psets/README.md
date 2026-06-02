# `psets/` — Stanford-style problem sets

> **Format.** Four problem sets, each scoped to 1–2 days of part-time
> work. Each PSet has a `handout.md` (written problems), a `starter/`
> directory (Python files with `# TODO(student)` blocks), and a
> `tests/` directory (pytest). The student is "done" when tests are
> green *and* `writeup.md` is committed in the PSet folder.

## Course-style preamble

- **Prerequisites.** [`onboarding/PLAN.md`](../../PLAN.md) **G0**
  passed (Roman items I–V). Students who have not built the toy
  bracket envelope plot (PLAN item IV) will struggle on HW1 Q3 and
  every subsequent PSet.
- **Collaboration policy.** Discuss problems verbally with one peer;
  write code and writeups alone. Cite the peer in `writeup.md` §0.
- **Late policy.** Each student gets a budget of 2 late days per
  PSet, drawn from a global pool of 6 across the four PSets.
- **Honor.** Do not look at `solutions/` (gitignored). Looking at
  `tests/` is fine — they are part of the assignment.
- **Calibration.** Every claim in `writeup.md` gets
  `HIGH / MEDIUM / LOW / UNVERIFIED`. See top-level
  [`README.md`](../README.md) §4 for the penalty.

## PSets at a glance

| # | Title | Topic | Days | Points |
|---|---|---|---|---|
| HW1 | Binary entropy & Hellman–Raviv on a coin | pure probability / IT warm-up | 1 | 100 |
| HW2 | Partitions, conditional entropy, toy 1-WL | the partition vocabulary | 1.5 | 100 |
| HW3 | Build the T1 verifier from scratch | the sandwich on 3 cells | 2 | 100 |
| HW4 | Aggregator inflation $r_T = (\Delta_{\max}, 1, 1)$ on Cora | the E3 punchline | 2 | 100 |

HW1 is a *warm-up* — pencil-and-paper math plus 30 LOC. HW4 is the
heaviest — it asks the student to reproduce a paper-level result on
a real dataset.

## Submission

Each PSet expects exactly:

```
psets/hwN/
├── starter/                # touched — TODOs filled in
├── tests/                  # NOT touched
├── writeup.md              # NEW — written answers + calibration
└── plots/                  # NEW — any figures the writeup cites
```

Commit on a personal branch named `student/<name>/psetN`. The grader
runs `pytest psets/hwN/tests/` from repo root.

## Per-PSet rubric template

| Q | Topic | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|---|
| 1 | … | 18 | 7 | 5 | 30 |
| 2 | … | 18 | 8 | 4 | 30 |
| 3 | … | 12 | 5 | 3 | 20 |
| 4 | … | 12 | 5 | 3 | 20 |
| **Sum** | | **60** | **25** | **15** | **100** |

Per-question weights vary; the column totals are constant.

## Status

- **HW1**: fleshed out — `handout.md`, `starter/`, `tests/`, rubric.
- **HW2–HW4**: stubbed — `README.md` with topic + rubric, awaiting
  flesh after the HW1 shape is validated.
