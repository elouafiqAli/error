# Capstone M4 — NAS pre-filter (E6 in miniature)

> **Stub.** README only; starter and tests will be fleshed out after
> M3 is validated.
>
> **Goal.** Take a hand-curated menu of 6 architectures (GCN-2,
> GCN-3, GIN-2, GIN-3, GraphSAGE-2, MLP-2); rank by bracket midpoint
> on the 1-WL(L=2) partition *before* training; train all 6; compare
> ranks via Kendall $\tau$ and a permutation p-value. Reproduce a
> $\tau \ge 0.3$ result (abstract reports $\tau = 0.48$ on a larger
> menu).

**Points.** 20. **Tests.** 5 (planned).

## Planned deliverables

- `nas.py` exposing `rank_by_bracket(menu, partition)`,
  `train_and_rank(menu)`, `kendall_tau_with_pvalue(rank_a, rank_b)`.
- `milestone_report.md` with the rank table and the Kendall $\tau$
  with a permutation p-value (10 000 perms).
- False lead drill: try a *different* partition (label-only) and
  show that the ranking correlation collapses — argue why.

## Rubric (planned)

| Item | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|
| `rank_by_bracket` + `train_and_rank` correct | 5 | 1 | 1 | 7 |
| Kendall τ + permutation p-value | 3 | 1 | 1 | 5 |
| Achieves τ ≥ 0.3 on the menu | 3 | 1 | 0 | 4 |
| False-lead drill writeup | 1 | 2 | 1 | 4 |
| **Total** | **12** | **5** | **3** | **20** |
