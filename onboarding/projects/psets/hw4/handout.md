# HW4 handout — aggregator inflation on the C₆ vs 2K₃ blind spot

**Due:** 2 days. **Points:** 100. **Prerequisites:** HW2 (`wl_step`),
HW3 (`hbin_inverse`).

In HW2 you showed that 1-WL cannot distinguish $C_6$ from $2K_3$
when starting from a constant colouring. **This PSet asks why no
permutation-invariant *aggregator* — sum, mean, max — can save
you either, and what feature engineering would.**

We'll work entirely on the two 6-node graphs from HW2. No GPU, no
real-dataset loading. Pedagogically: an aggregator $\sigma$ takes a
node $u$ and the multiset $\{x_v : v \sim u\}$ and produces a single
scalar $\sigma_u$. The "aggregator partition" groups nodes by the
pair $(x_u, \sigma_u)$ — equivalent to one round of message passing
with $\sigma$.

You will then **inflate** the bracket by computing it under each
aggregator-induced partition and visualising the gap.

---

## Q1 — Three aggregator partitions (25 pts)

In [`starter/q1_aggregators.py`](starter/q1_aggregators.py), implement:

```python
def sum_partition(edge_index, n, x):
    """Partition nodes by (x_u, sum(x_v for v ~ u))."""
    ...

def mean_partition(edge_index, n, x):
    """Partition nodes by (x_u, mean(x_v for v ~ u))."""
    ...

def max_partition(edge_index, n, x):
    """Partition nodes by (x_u, max(x_v for v ~ u))."""
    ...
```

Each returns a `list[np.ndarray]` (cells), suitable for HW2's
`cond_entropy`. The test (`tests/test_q1.py`) checks that on $K_2$
with `x = [1, 1]` each aggregator returns a one-cell partition.

(15 pts implementation, 10 pts test.)

---

## Q2 — Constant features: every aggregator collapses (25 pts)

### Q2.1 — Compute (15 pts)

For both $C_6$ and $2K_3$, set `x = np.ones(6)` and compute the
sum / mean / max partition. Verify all three return a **single
cell of size 6** on both graphs.

### Q2.2 — Reflection (10 pts)

In `writeup.md` §Q2.2:

a) Explain in two sentences *why* this happens. (Hint: degrees.)
b) State, in one sentence, the operational meaning: "no message-
   passing GNN with constant initial features can separate $C_6$
   from $2K_3$, regardless of aggregator choice."

The test (`tests/test_q2.py`) verifies the single-cell collapse.

---

## Q3 — Degree features: still blind (20 pts)

### Q3.1 — Implement (10 pts)

In [`starter/q3_degree_feature.py`](starter/q3_degree_feature.py),
compute degree features `x = deg(v)` for $C_6$ and $2K_3$.

Both graphs are 2-regular, so `x = np.full(6, 2.0)` in both cases.
This means **every aggregator collapses again** — verify.

### Q3.2 — Reflection (10 pts)

In `writeup.md` §Q3.2: explain why this proves the failure is not
about the features being trivial — *any* permutation-invariant
node-local feature on $\{C_6, 2K_3\}$ has the same property,
because both graphs have the same degree distribution.

(*Distinguish:* this is not the 1-WL blind spot itself; this is
the *aggregator-induced* blind spot, a consequence.)

The test (`tests/test_q3.py`) checks the partition equality.

---

## Q4 — Triangle-count feature breaks the tie (20 pts)

### Q4.1 — Implement (15 pts)

In [`starter/q4_triangle_feature.py`](starter/q4_triangle_feature.py),
compute `triangles(v) = number of triangles containing v`.

For $C_6$: every node sits on **0** triangles (no triangles in a
6-cycle).
For $2K_3$: every node sits on **1** triangle.

The features differ globally but are **constant within each graph**,
so within a single graph the aggregator still collapses to one cell.
**But the bracket H(Y|Π) computed over both graphs jointly distinguishes
them.**

### Q4.2 — Verify (5 pts)

In `writeup.md` §Q4.2 explain in one paragraph: triangle counts give
you a global invariant that separates the two graphs, but they do not
split *within* either graph. This is why genuine 1-WL **must** look at
multisets of neighbour colours (or 2-WL must look at edge tuples) —
constant features plus aggregation aren't enough.

The test (`tests/test_q4.py`) checks the triangle counts.

---

## Q5 — Writeup + calibration (10 pts)

Required entries: the three single-cell collapses; the triangle
count for both graphs; "no node-local permutation-invariant
aggregator can split $C_6$ from $2K_3$".
