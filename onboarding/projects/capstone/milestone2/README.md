# Capstone M2 — Bracket computer

> **Stub.** README only; starter and tests will be fleshed out after
> M1 is validated.
>
> **Goal.** Implement the partition-conditional entropy bracket on
> top of M1's `Partition`: given $\{q_C, e_C\}$, compute
> $\sum_C q_C \cdot 2 \, \mathrm{Hbin}^{-1}(2 e_C)$ (upper envelope)
> and the matching lower envelope, plus the slack $w(\Pi)$.

**Points.** 25. **Tests.** 8 (planned).

## Planned deliverables

- `bracket.py` exposing `upper(p: Partition) -> float`,
  `lower(p: Partition) -> float`, `slack(p) -> float`, and
  `verify(p, model_error) -> bool`.
- `milestone_report.md` reproducing the abstract's $w^* \approx 0.1610$
  on a 5-cell uniform-mass family.
- Mutate → fail → revert: break one constant in `upper`, watch
  `verify` reject Cora's GCN error, restore.

## Rubric (planned)

| Item | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|
| `upper` / `lower` correct on label partition | 5 | 1 | 1 | 7 |
| `slack` matches T1 reference on 5-cell uniform | 5 | 2 | 1 | 8 |
| `verify` integrates with M1's `Partition` | 3 | 1 | 0 | 4 |
| Mutate → fail → revert + writeup | 2 | 2 | 2 | 6 |
| **Total** | **15** | **6** | **4** | **25** |
