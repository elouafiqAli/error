# HW2 — Partitions, conditional entropy, toy 1-WL

> **Stub.** README only; handout / starter / tests will be fleshed
> out after HW1 shape is validated.
>
> **Pitch.** Lift the single-coin vocabulary (HW1) to *partitions*.
> Build a `Partition` dataclass on a 5-node toy graph; compute
> $H(Y \mid \Pi)$ by hand and in code; trace 1-WL by hand on $C_5$,
> $C_6$, and $2 K_3$, and show in code where 1-WL fails to
> distinguish $C_6$ from $2 K_3$ (the canonical 1-WL blind spot).

**Time.** 1.5 days. **Points.** 100.

## Planned questions

| Q | Topic | Pts |
|---|---|---|
| 1 | Hand-compute $H(Y \mid \Pi)$ on a 5-node toy | 20 |
| 2 | Implement `cond_entropy(partition, labels)` | 20 |
| 3 | Trace 1-WL by hand on $C_5$, $C_6$, $2 K_3$ | 20 |
| 4 | Implement 1-WL refinement step; verify $C_6$ vs $2 K_3$ blind spot | 25 |
| 5 | Writeup + calibration | 15 |
