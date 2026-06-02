# Capstone M1 — Data + partition harness

> **Goal.** Get Cora loaded, and build two partitions of its node
> set: (a) the *label* partition (one cell per class, 7 cells), and
> (b) the *1-WL* color-refinement partition at depth $L \in \{1, 2, 3\}$.
> Compute, for each partition, the per-cell mass $q_C$ and the
> per-cell Bayes error $e_C$ — these are the two ingredients M2's
> bracket computer needs.
>
> **Points.** 15. **Time.** ~1 day. **Tests.** 6.

## Learning objectives

By the end, the student can:

1. Load a citation graph from PyG and report its $n$, $m$, number
   of classes, and degree statistics.
2. Define a `Partition` data structure that stores cells, masses
   $q_C$, and per-cell Bayes errors $e_C$, and validates the
   measure-theoretic invariants (cells disjoint, cover, sum-to-one).
3. Build the *label* partition.
4. Run 1-WL color refinement at depths $L = 1, 2, 3$ and build the
   corresponding 1-WL partitions.
5. Distinguish: **label partition** (one cell per class, $e_C = 0$
   *by construction* — the cell *is* the class) vs **1-WL
   partition** (cells are color-orbits, $e_C \in [0, 1/2]$ depends
   on label heterogeneity within the orbit).

## Deliverables

- `partition.py` with TODOs filled in. **Do not edit the public
  signatures** — `tests/` depend on them.
- `milestone_report.md` (~1 page) with:
  - dataset stats (n, m, classes, $\Delta_{\max}$),
  - cell counts per partition,
  - a histogram (PNG in `plots/`) of $e_C$ for the depth-2 1-WL
    partition,
  - a one-paragraph **Distinguish** entry: label vs 1-WL partition.

## Rubric

| Item | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|
| `Partition` dataclass + invariants | 3 | 1 | 0 | 4 |
| `label_partition` | 2 | 1 | 0 | 3 |
| `wl_partition(L)` for $L \in \{1,2,3\}$ | 3 | 1 | 0 | 4 |
| `milestone_report.md` + histogram | 1 | 1 | 2 | 4 |
| **Total** | **9** | **4** | **2** | **15** |

## Starter signatures

See [`partition.py`](partition.py). The student fills in the bodies
of:

- `Partition.__post_init__` (invariant checks),
- `label_partition(data)`,
- `wl_refine(edge_index, n, init_colors)` (one 1-WL step),
- `wl_partition(data, depth)`.

## Tests

```
pytest onboarding/projects/capstone/milestone1/tests/ -v
```

Six tests:

1. `Partition` rejects overlapping cells.
2. `Partition` rejects cells that do not cover.
3. `Partition.q.sum()` equals 1 to `1e-12`.
4. `label_partition` on Cora has exactly 7 cells, each `e_C == 0`.
5. `wl_partition(depth=1)` produces ≥ 1-WL-refined cells (#cells ≥ #classes).
6. `wl_partition(depth=L+1).#cells >= wl_partition(depth=L).#cells`
   (refinement is monotone).
