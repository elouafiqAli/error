# Capstone — Bracket-audited GNN pipeline (Udacity-style)

> **Pitch.** Over five milestones, the student builds a complete
> end-to-end pipeline: load a citation graph → build a partition →
> compute the partition-conditional entropy bracket → train a small
> GCN → audit the trained model against the bracket → use the
> bracket as a training-free architecture pre-filter → write a
> calibrated report. By M5 the student has *all of the moving parts*
> of the paper's E1, E3, and E6 experiments running on their own
> machine, with their own code.
>
> **Time.** ~2 weeks part-time. **Points.** 100.
> **Prerequisite.** PLAN.md G1 passed. HW1 strongly recommended.

## Why a capstone?

The PSets build *vocabulary*. The capstone builds *fluency*. The
student finishes with one repository, on one branch, that can be
demoed at a whiteboard in 20 minutes — the kind of artefact that
gets you hired into the lab.

## Milestones

| # | Title | Output | Pts | Tests |
|---|---|---|---|---|
| M1 | Data + partition harness | `partition.py` + label / 1-WL partitions on Cora | 15 | 6 |
| M2 | Bracket computer | `bracket.py` + verifier on M1's partitions | 25 | 8 |
| M3 | Train + audit GCN | `train.py` + scatter plot vs bracket | 25 | 6 |
| M4 | NAS pre-filter | `nas.py` + Kendall-τ ranking on a 6-arch menu | 20 | 5 |
| M5 | Report | `REPORT.md` + final plots, calibrated | 15 | rubric |

**Gate model.** Each milestone has its own `README.md`, starter files,
and pytest. A milestone is "done" when:

1. Its tests pass.
2. Its `milestone_report.md` is committed.
3. The student has run the integration test (in `tests/`) and the
   downstream milestone still imports cleanly.

Skipping a milestone is allowed; you forfeit its points and *all*
later milestones that depend on it (M2→M3→M4→M5 chain).

## Repository layout

```
capstone/
├── README.md                 # this file
├── milestone1/
│   ├── README.md
│   ├── partition.py          # student fills TODOs
│   └── tests/
├── milestone2/
│   ├── README.md
│   ├── bracket.py
│   └── tests/
├── milestone3/
│   ├── README.md
│   ├── train.py
│   ├── audit.py
│   └── tests/
├── milestone4/
│   ├── README.md
│   ├── nas.py
│   └── tests/
├── milestone5/
│   ├── README.md
│   └── REPORT_TEMPLATE.md
└── tests/                    # integration tests across milestones
    └── test_end_to_end.py
```

## Dataset

**Cora** (PyG `Planetoid('Cora')`). The student is *not* asked to
download anything by hand — PyG handles it. A budget GPU (or CPU,
slowly) is enough; nothing in the capstone needs more than 30
seconds of GCN training.

## Rubric

| Milestone | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|
| M1 (15) | 9 | 4 | 2 | 15 |
| M2 (25) | 15 | 6 | 4 | 25 |
| M3 (25) | 15 | 6 | 4 | 25 |
| M4 (20) | 12 | 5 | 3 | 20 |
| M5 (15) | — | 10 | 5 | 15 |
| **Total** | **51** | **31** | **18** | **100** |

M5 has no correctness points because the writeup itself *is* the
graded artefact; it is checked against the per-claim calibration
rubric in [`../README.md`](../README.md) §4.

## Status

- **M1**: fleshed out — `README.md`, `partition.py`, 6 tests.
- **M2–M5**: stubbed — `README.md` only, awaiting flesh after M1
  shape is validated.
