# Capstone M5 — Calibrated report

> **Stub.** README + REPORT_TEMPLATE.md will be fleshed out after
> M4 is validated.
>
> **Goal.** Write a 4-page report (markdown, with KaTeX) that walks
> a reader from the abstract through to the M4 NAS table, with every
> non-trivial claim labelled `HIGH / MEDIUM / LOW / UNVERIFIED` and
> backed by either a test, a plot, or a citation. The report is the
> demoable artefact: it is what the student would show an advisor.

**Points.** 15. **Tests.** none — graded by rubric.

## Planned structure of `REPORT_TEMPLATE.md`

1. **§1 — One-paragraph pitch.** What is the bracket; why audit a
   GNN with it.
2. **§2 — Dataset & partitions.** Cora stats; label vs 1-WL(L=2)
   cells; histogram (from M1).
3. **§3 — Bracket reproduction.** $w^* \approx 0.1610$ on the 5-cell
   family (from M2); slack on the 1-WL(L=2) partition (from M2).
4. **§4 — GCN audit.** Training curve; scatter plot of realised
   error inside the bracket (from M3).
5. **§5 — NAS pre-filter.** Kendall $\tau$ table; one paragraph on
   when the pre-filter helps and when it fails (from M4).
6. **§6 — Distinguish entries.** At least 3 X-vs-Y pairs the
   student found load-bearing.
7. **§7 — Mutate → fail → revert log.** Which mutations the student
   ran; what they learned.
8. **§8 — False leads.** What the student tried that did not work;
   why.
9. **§9 — Calibration table.** Every nontrivial claim in §1–§8 in
   one row, with HIGH / MEDIUM / LOW / UNVERIFIED.
10. **§10 — Next.** One paragraph: what would the student do with
    another week.

## Rubric (planned)

| Item | Pedagogy | Calibration | Total |
|---|---|---|---|
| §1–§5 content & flow | 4 | 1 | 5 |
| §6 distinguish (≥ 3 pairs) | 2 | 1 | 3 |
| §7 mutate log (≥ 2 entries) | 1 | 1 | 2 |
| §8 false leads (≥ 1 entry) | 1 | 1 | 2 |
| §9 calibration table | 2 | 1 | 3 |
| **Total** | **10** | **5** | **15** |
