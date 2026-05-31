# Implementation summary to apply to `PAPER-ARXIV.md`

## Chosen editorial mode

Adopt **post-freeze mode** for C1.

That means the paper will consistently state:
- C1 is still a conjecture mathematically,
- but its empirical status under the literal §9 protocol is frozen as of 2026-05-30,
- with support-by-evidence at `L >= 3` on `anchor_8`.

## Theory edits to apply

1. Add an explicit definition of **admissible architecture-family specification**.
2. Split the core theorem chain into:
   - a pure partition-information theorem,
   - a refinement-monotonicity proposition,
   - an architecture-factorization proposition,
   - an instantiated PA-MPC corollary.
3. Clarify that the partition theorem itself does not require `f in F_WL(G)`.
4. Rewrite Appendix A lower-bound proof using the exact identity
   `H_bin(P_C) = H_bin(min(P_C,1-P_C))` plus Jensen/concavity.

## Narrative edits to apply

1. Make Abstract / Introduction / §7.3 / §9 / Conclusion consistent about C1.
2. Keep theory, mechanization, exact-rational audits, and float empirical results explicitly separated.
3. Reframe E03 monotonicity as an exact audit of a theorem already stated in §3.
