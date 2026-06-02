# HW2 handout — partitions, conditional entropy, toy 1-WL

**Due:** 1.5 days after assignment. **Points:** 100.
**Prerequisite:** HW1 (you must have `hbin` working).

This PSet introduces the **partition** as a first-class object, the
**conditional entropy** $H(Y\mid \Pi)$ as the load-bearing entropy
quantity, and the **1-Weisfeiler–Leman** refinement that turns a
graph into a partition.

You will reuse `hbin` from HW1. Import it relatively from
`onboarding.projects.psets.hw1.starter.q1_hbin`.

Definitions used throughout:

- A **partition** $\Pi$ of $\{0, \ldots, n-1\}$ is a list of cells
  $C_1, \ldots, C_m$ that are pairwise disjoint and together cover
  $\{0, \ldots, n-1\}$.
- $q_C := |C| / n$ — cell mass.
- $e_C := 1 - \max_y \Pr(Y = y \mid C) = 1 - (\text{mode-count in } C) / |C|$ — per-cell Bayes error.
- $H(Y\mid \Pi) := \sum_C q_C \, H_{\mathrm{bin}}(e_C)$ — **the** conditional entropy used by the bracket.
- **1-WL refinement step**: $\mathrm{color}_{t+1}(u) = \mathrm{hash}(\mathrm{color}_t(u), \{\!\!\{\mathrm{color}_t(v) : v \sim u\}\!\!\})$.

---

## Q1 — Hand-compute $H(Y\mid \Pi)$ (20 pts)

### Q1.1 — Written (12 pts)

Consider the 6-node graph with labels $y = (0, 0, 1, 1, 1, 0)$ and
the partition

$$
\Pi = \{ \{0,1,2\}, \{3,4\}, \{5\} \}.
$$

a) (3 pts) Write $q_{C_1}, q_{C_2}, q_{C_3}$.
b) (3 pts) Write $e_{C_1}, e_{C_2}, e_{C_3}$. *Hint*: the mode of
   $\{0,0,1\}$ is 0 (count 2); of $\{1,1\}$ is 1; of $\{0\}$ is 0.
c) (3 pts) Compute $\varepsilon(\Pi) = \sum_C q_C \, e_C$ to 4
   decimals.
d) (3 pts) Compute $H(Y\mid \Pi) = \sum_C q_C \, H_{\mathrm{bin}}(e_C)$
   to 4 decimals.

### Q1.2 — Cross-check by code (8 pts)

Run [`starter/q1_hand_check.py`](starter/q1_hand_check.py) and
verify your hand-computed numbers match to `1e-12`. The starter
file *prints* the four numbers from $\Pi$ and $y$; no TODOs in this
file (it is a calibration check on your hand work).

---

## Q2 — `cond_entropy(partition, labels)` (20 pts)

In [`starter/q2_cond_entropy.py`](starter/q2_cond_entropy.py),
implement:

```python
def cond_entropy(partition: list[np.ndarray], labels: np.ndarray) -> float:
    """H(Y | Π) in bits, with the bracket convention."""
    # TODO(student):
    # 1) compute n = total number of nodes (sum of cell sizes)
    # 2) for each cell C: q_C = |C| / n
    # 3) for each cell C: e_C = 1 - (mode count of labels[C]) / |C|
    # 4) return sum(q_C * hbin(e_C) for C in partition)
```

The test (`tests/test_q2.py`) checks:

- Singleton-cell partition: each cell has $e_C = 0$, so
  $H(Y\mid\Pi) = 0$. (`8 pts`)
- One-cell partition: $e_C$ equals the global Bayes error,
  $H(Y\mid\Pi) = H_{\mathrm{bin}}(\varepsilon)$. (`6 pts`)
- The Q1 toy: matches your hand computation to `1e-12`. (`6 pts`)

---

## Q3 — Trace 1-WL by hand on $C_5$, $C_6$, $2K_3$ (20 pts)

The graphs:

- $C_5$ — 5-cycle, nodes $0$–$4$, edges $i \leftrightarrow (i+1) \mod 5$.
- $C_6$ — 6-cycle, nodes $0$–$5$, edges $i \leftrightarrow (i+1) \mod 6$.
- $2K_3$ — two disjoint triangles, nodes $0$–$5$, edges
  $\{01, 12, 02\}$ and $\{34, 45, 35\}$.

### Q3.1 — Written (16 pts)

For each of the three graphs, starting from the trivial colouring
$\mathrm{color}_0 \equiv 0$:

a) (4 pts each, 12 pts total) Show the colour assignment after
   $t = 1, 2, 3$ rounds of 1-WL. (Express each round as a tuple
   `(c, multiset)` and use small integers as the renaming.) The
   colourings will stabilise quickly.
b) (4 pts) State, in one line each, whether 1-WL **distinguishes**
   the pair $(C_6, 2 K_3)$. ("Distinguishes" = the multisets of
   stable colours over nodes differ.)

### Q3.2 — Bonus B [0–3 pts] *for strong students*

In one paragraph, explain *why* 1-WL fails on the $C_6$ vs $2 K_3$
pair, in terms of *local neighbourhoods*. This is the canonical
1-WL blind spot.

---

## Q4 — Implement 1-WL refinement; verify the blind spot (25 pts)

### Q4.1 — Coding: `wl_step` (12 pts)

In [`starter/q4a_wl_step.py`](starter/q4a_wl_step.py), implement
**one round** of 1-WL refinement.

```python
def wl_step(edge_index: np.ndarray, n: int, colors: np.ndarray) -> np.ndarray:
    """One round of 1-WL color refinement.

    Parameters
    ----------
    edge_index : np.ndarray, shape (2, m)
        Each column (u, v) is a directed edge. (Undirected graphs
        appear with both directions.)
    n : int
        Number of nodes.
    colors : np.ndarray, length n, dtype int
        Current colors.

    Returns
    -------
    np.ndarray, length n, dtype int
        New colors in [0, K_new).
    """
    # TODO(student):
    # 1) for each node u: build sorted tuple of neighbor colors
    # 2) build signature[u] = (colors[u], tuple_of_neighbor_colors)
    # 3) map distinct signatures to dense ints (use a dict)
    # 4) return the new color array
```

The test checks:

- `wl_step` on $K_2$ with colors `[0, 0]` produces 1 distinct color
  (still constant after refining). (`3 pts`)
- `wl_step` 3 times on `[0, 0, 0]` over $P_3$ (path 0–1–2) splits
  the endpoint vs middle node. (`4 pts`)
- `wl_step` 3 times on a 6-node graph with one node of higher
  degree splits it from the rest. (`5 pts`)

### Q4.2 — Coding: $C_6$ vs $2 K_3$ blind spot (13 pts)

In [`starter/q4b_c6_vs_2k3.py`](starter/q4b_c6_vs_2k3.py):

a) (3 pts) Build edge_index for $C_6$ and $2 K_3$. Both are
   6-regular… wait, both are 2-regular. (Verify: each node has
   exactly 2 neighbours in both.)
b) (5 pts) Run 1-WL to stability on both. Use `wl_step` from Q4.1.
   Return the multiset of stable colours (as a sorted tuple of
   counts).
c) (5 pts) Verify the multisets are **identical** — this is the
   blind spot. Then verify the partitions they induce are
   **isomorphic but the graphs are not**.

The test checks:

- The two graphs have the same number of nodes, same degree
  distribution. (`3 pts`)
- The stable-colour multisets are equal. (`5 pts`)
- The *induced partitions* both have exactly 1 cell of size 6.
  (`5 pts`)

---

## Q5 — Writeup & calibration (15 pts)

Create `writeup.md` with §Q1, §Q2, §Q3, §Q4 sections containing your
written answers plus a §Calibration section listing every
nontrivial claim with `HIGH / MEDIUM / LOW / UNVERIFIED`.

Required calibration entries (at least 5 total):

1. Your value of $H(Y\mid\Pi)$ for the Q1 toy.
2. The Q3.1 1-WL colour assignments on the three graphs.
3. The Q3.1.b answer about whether 1-WL distinguishes $(C_6, 2K_3)$.
4. The Q4.2.c verification.
5. One claim of *your choice* about the blind spot's significance.

Mis-calibration penalty is double weight (top-level
[`README.md`](../../README.md) §4).
