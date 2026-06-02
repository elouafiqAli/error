# HW4 — Aggregator inflation $r_T = (\Delta_{\max}, 1, 1)$ on Cora

> **Stub.** README only; handout / starter / tests will be fleshed
> out after HW1–HW3 shapes are validated.
>
> **Pitch.** The capstone-without-the-capstone. Take Cora; identify
> $\Delta_{\max} = 168$; for sum / mean / sym-norm aggregators,
> compute the inflated upper envelope $r_T \cdot \mathrm{upper}(\Pi)$;
> reproduce the 7-orders-of-magnitude honest-looseness gap that
> motivates the paper's choice of mean / sym-norm aggregators in E3.

**Time.** 2 days. **Points.** 100.

## Planned questions

| Q | Topic | Pts |
|---|---|---|
| 1 | Compute $\Delta_{\max}$ on Cora, CiteSeer, PubMed | 15 |
| 2 | Implement `inflated_upper(partition, aggregator)` for the three aggregators | 30 |
| 3 | Reproduce the 7-orders honest-looseness gap for sum-on-Cora | 20 |
| 4 | **Distinguish** "honest looseness" vs "a bug": construct one of each on a toy 3-cell example | 20 |
| 5 | Writeup + calibration | 15 |
