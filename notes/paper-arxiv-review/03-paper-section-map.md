# PAPER-ARXIV section map and proof spine

## Section inventory

- `Abstract`
- `1. Introduction`
- `2. Related Work`
- `3. Theory`
  - `3.1 Definitions`
  - `3.2 The Bridge Inequality`
  - `3.3 Three Named Conjectures`
  - `3.4 MI^2 cautionary note`
  - `3.5 Scope`
- `4. Exact-Rational Ledger`
- `5. Float-Tier Baseline`
- `6. Lean Witness`
- `7. Pilot-Tier Results`
- `8. Reproducibility Infrastructure`
- `9. The Open Problem — Continuous-Transfer (C1)`
- `10. Known Limitations and Honest Narrowings`
- `11. Conclusion`
- `Appendix A`: proof of Theorem 1
- `Appendices C-F`: experiment / Lean / design / build notes

## Current proof spine in the manuscript

### Core formal chain actually present

1. **Definition 3.1** — architecture-induced partition
2. **Definition 3.2** — DIG and surrogate DIG
3. **Definition 3.3** — PA-MPC
4. **Definition 3.4** — WL-measurable task class
5. **Lemma 3.1** — purity iff DIG = 0 iff surrogate DIG = 0
6. **Theorem 1** — Bayes-error sandwich
7. **Corollary 3.1** — any depth-`L` family member factors through the partition
8. **Corollary 3.2** — optional surprisal-axis restatement

### Major missing links / under-formalized links

1. **Admissibility of `(A, Pi_A^(0))` is not formally defined.**
2. **LossyWL is referenced but not formally specified enough for theorem use.**
3. **Theorem 1 has stronger assumptions than necessary.**
   - The partition-entropy/Bayes sandwich is true for any finite partition and binary task.
4. **Corollary 3.1 depends on a model-factorization proposition that is only sketched.**
5. **Monotonicity under refinement is used experimentally (E03) but not proved in the theory section.**
6. **The paper interleaves theorem statements, empirical ledgers, and conjecture governance very early.**

## Recommended revised proof spine

1. **Definition block**
   - graph, task, measure, partition, cell statistics
   - admissible architecture family
   - LossyWL-induced depth partition

2. **Pure partition-information theorem**
   - For any finite partition `Pi` and binary task `f`, define
     - `DIG(f | Pi)`
     - `eps*_Pi`
   - prove
     - `H_bin^{-1}(DIG) <= eps* <= DIG/2`

3. **Refinement / monotonicity proposition**
   - If `Pi'` refines `Pi`, then
     - `DIG(f | Pi') <= DIG(f | Pi)`
     - `eps*_{Pi'} <= eps*_{Pi}`

4. **Architecture factorization proposition**
   - Any admissible depth-`L` MPNN is constant on cells of `Pi_A(G,L)`

5. **PA-MPC corollary**
   - Substitute `Pi = Pi_A(G,L)` into the partition theorem

6. **Scope proposition / remark**
   - explain where `F_WL(G)` is needed and where it is not

This revised order would make the proof chain parallel the clean theorem layering seen in the background arXiv papers.