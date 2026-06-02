# `onboarding/projects/` — graduate-student practical track

> **Where this sits.** The [PLAN.md](../PLAN.md) on-ramp ends at **G2**:
> the operator can read the abstract, reproduce E3 on Cora, and
> whiteboard the bracket. Most of that work is *individual items*
> (write a 20-line script, mutate a verifier, plot a curve).
>
> This folder adds two **structured-assessment** tracks on top, both
> *optional, both gated by G1*:
>
> 1. **`capstone/`** — a Udacity-style end-to-end nanodegree-style
>    project: one big build, 5 milestones, placeholders → working
>    pipeline → report. Roughly two solid weeks of part-time work.
> 2. **`psets/`** — four Stanford-style problem sets (HW1–HW4), each
>    1–2 days, with written and coding parts, starter files with
>    `# TODO` blocks, unit tests, and a per-question rubric.
>
> Both tracks are designed for a graduate student who wants to be
> *graded* — by a peer, an advisor, or themselves with a stopwatch
> and a rubric — rather than self-paced. They sit between G1 and any
> downstream track (proof carpentry / Lean / Paper B).

---

## 1. Why two tracks?

| | Capstone | PSets |
|---|---|---|
| Shape | one project, integrated | four independent assignments |
| Time | ~2 weeks part-time | ~1–2 days each |
| Output | a working pipeline + a written report | a `.py` per question + a `.pdf` writeup |
| Failure mode | architecture creep | tunnel vision on individual lemmas |
| Best for | someone joining the lab and needing a fluency demo | someone studying solo who wants tightly-bounded reps |

**A student does not need both.** Pick one. The capstone is closer
to fast.ai's ethos (Build → Distinguish → Name); the PSets are
closer to a course's ethos (problems with right and wrong answers,
graded). Both teach the same paper; neither replaces G2.

---

## 2. Design principles (apply to both tracks)

1. **Placeholders, not blanks.** Every starter file has a
   working *skeleton* — imports, function signatures, docstrings,
   smoke-test cells — with `# TODO(student)` blocks marking the
   load-bearing 5–20 lines the student writes. The skeleton runs
   (and fails informatively) before the student touches it.
2. **Unit tests ship with the assignment.** A student knows they
   are done when `pytest` is green. No "submit and hope".
3. **Reference outputs are public.** Each problem lists the
   *expected* number / plot shape / theorem name. This is not a
   contest; it is a competence ladder.
4. **Rubric is explicit, per-question.** Points per part, with a
   one-line description of what earns them. No mystery grading.
5. **Mutate → fail → revert is in the assignment**, not a side
   exercise. At least one question per PSet, and one per milestone,
   asks the student to break the thing on purpose and explain.
6. **Confidence calibration is in the rubric.** Every writeup
   ends with a `HIGH / MEDIUM / LOW / UNVERIFIED` self-assessment
   of every claim; mis-calibration costs points.
7. **Citation discipline.** Any number quoted from the preprint
   gets a `\eqref{...}` or `§N.M` pointer. "From the paper" alone
   loses points.

---

## 3. Track layouts

### 3.1 Capstone — `capstone/`

```
capstone/
├── README.md            # overview, rubric, milestone gates
├── milestone1/          # data + partition harness
├── milestone2/          # bracket computer
├── milestone3/          # train GCN, audit against bracket
├── milestone4/          # NAS pre-filter (E6 in miniature)
├── milestone5/          # report
└── tests/               # shared pytest fixtures + integration tests
```

**Gate model.** Each milestone has its own `README.md` with
deliverables, starter files, unit tests, and a rubric. Milestones
are sequential: M2 imports M1's `partition.py`; M3 imports M2's
`bracket.py`; etc. A milestone is "done" when its tests pass *and*
the milestone-report `.md` is committed.

**Total points:** 100 (M1 15, M2 25, M3 25, M4 20, M5 15).

### 3.2 Problem sets — `psets/`

```
psets/
├── README.md            # course-style preamble, late policy, rubric template
├── hw1/                 # binary entropy + Hellman–Raviv on a coin
├── hw2/                 # partitions, conditional entropy, toy 1-WL
├── hw3/                 # build the T1 verifier on a 3-cell example
├── hw4/                 # aggregator inflation r_T on Cora
└── solutions/           # GITIGNORED — instructor-only reference solutions
```

**Per-PSet structure:**

```
hwN/
├── README.md            # questions, rubric, expected outputs, late penalty
├── handout.md           # written problems (math, proofs, short answers)
├── starter/             # # TODO-stamped .py files
│   ├── problem1.py
│   ├── problem2.py
│   └── ...
├── tests/               # pytest, runs against student's starter/
│   └── test_problemN.py
└── data/                # tiny CSVs / pickled toy graphs
```

**Total points:** 100 per PSet. Weights inside a PSet vary.

---

## 4. Rubric philosophy

Each problem is graded on three axes:

| Axis | Weight | What it measures |
|---|---|---|
| **Correctness** | 60% | Unit tests pass; numbers match reference to declared precision. |
| **Pedagogy** | 25% | Writeup distinguishes the right pair, names the failure mode, cites the paper. |
| **Calibration** | 15% | Self-assessed confidence is honest. A `HIGH` claim that fails an adversarial reading costs more than an `UNVERIFIED` claim that turns out true. |

**Mis-calibration penalty.** If a student labels a claim `HIGH` and
the grader's adversarial check kills it, points lost = full
calibration weight × 2. If they label it `LOW` or `UNVERIFIED` and
it survives, no penalty (calibration was honest).

---

## 5. What is *not* graded here

- Proving Theorem 1 from scratch. (Verifier-level competence is
  enough for both tracks. Proof carpentry is downstream.)
- Lean / Julia / formal verification. (BLUE in PLAN.md; BLUE here.)
- Extending the bracket to $\phi$-families or k-WL. (Paper B / C.)
- Writing new theorems. (Research, not coursework.)

A capstone or PSet that *does* go there gets bonus points capped at
+5; do not chase them at the cost of the main rubric.

---

## 6. Status

- **Design version**: r1, 2026-06-02.
- **Author**: Claude (Copilot).
- **Fleshed-out**: `psets/hw1/` and `capstone/milestone1/`. Other
  milestones and PSets are stubbed with their README + rubric so the
  shape is fixed; the starter code is one iteration away.
- **Next call for the operator**: walk HW1 *and* M1 end-to-end with
  the placeholders. If both feel right, flesh out HW2-HW4 and
  M2-M5; if one feels wrong, revise the design before scaling.
