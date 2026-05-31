# paper-02-empirical — Scope (re-scoped 2026-05-30)

**Working title:** *Partition-Adapted MPC: Empirical evidence on MPC substrates.*
**Status:** scope locked; manuscript not yet drafted. Drafting is gated on at least `S1.report` (G7-float-discipline-S1 PASS).
**Trust posture:** T3 / R3 (per [verifiability-discipline.md](../../00-governance/verifiability-discipline.md)). Every numeric claim ships with bootstrap CI under the `S-ladder-standard-v1` rule and the F1–F5 envelope.

## 1. What this paper claims

> The C1 structural law (DIG → 0 under partition agreement at L ≥ 3 on A_pass
> architectures) survives — or fails — on the MPC NeurIPS 2025 substrates:
> r-regular (S1), ZINC subgraphs (S2), LRGB peptides (S3). Each substrate is a
> pre-registered, sha-pinned test with a binary verdict and a CI-bracketed
> effect size.

The companion paper, [paper-01-pampc-core](../paper-01-pampc-core/), holds the
T1/T2 structural law. paper-02 is the **empirical bridge from PA-MPC to MPC**;
it does not re-prove the law, it tests its transport.

## 2. What this paper does NOT claim

- ❌ Any T3 number is cited as a T1/T2 result. (Gateway rule, [trust-tiers.md](../../00-governance/trust-tiers.md).)
- ❌ Any S-rung that doesn't PASS gets quietly re-run with new seeds. (F4 forbids it.)
- ❌ The C-ladder retros (C2_2/C3_1/C4_1) are "fixed" or "extended". They stay sealed at tag `c-ladder-sealed-2026-05-30`.
- ❌ CIN, GIN-VN+, or other architectures outside the explicit S-rung architecture sets are surveyed. (Cost > $20/rung cap.)

## 3. Section plan (locked)

| § | Title | Source | Tier |
|---|---|---|---|
| 0 | Bridge from the sealed C-ladder | `PAMPC-E08-C1-LITERAL-VERDICT/RATE-TABLE/SUBSTRATE-NOTE` | ⟨T3-sealed⟩ |
| 1 | Theory anchor (mirrors paper-01) | `PAMPC-BRIDGE-INEQ-STATUS`, `PAMPC-BRIDGE-BAYES-ERROR-SANDWICH`, `PAMPC-LEAN-WITNESS-C4-K`, `PAMPC-LEAN-WITNESS-BAYES-ERROR-C4` | T1/T2 |
| 2.1 | S1 — r-regular keep + transfer | `PAMPC-S1-DECISION-VERDICT/DIG-TABLE` | T3 / R3 |
| 2.2 | S2 — ZINC subgraphs ring + regression (conditional) | `PAMPC-S2-DECISION-VERDICT/DIG-TABLE` | T3 / R3 |
| 2.3 | S3 — LRGB long-range transfer (conditional) | `PAMPC-S3-DECISION-VERDICT/DIG-TABLE` | T3 / R3 |
| 3 | Synthesis: does C1 transport to MPC substrates? | — | review |
| A | Sealed predecessor results (E01/E04/E06/E08) | `claims_archived.txt` | ⟨T3-sealed⟩ |

## 4. Decision rule (pre-committed)

The verdict in §§2.1–2.3 is the `S-ladder-standard-v1` rule registered in
[`pampc_paper.float_discipline.RULES`](../../50-paper-harness/pampc_paper/float_discipline.py):

> PASS iff `median DIG < 0.05` AND `95 % CI for median ρ ⊂ (-1, -0.5)` AND LOO-invariant across seeds.

Any other framing (e.g. "PASS in 2 of 3 substrates is enough") is forbidden by F4.

## 5. Conditional structure

S2 is drafted only if S1 verdict ≠ FAIL. S3 is drafted only if S2 verdict ≠ FAIL.
If S1 = FAIL, paper-02 publishes a **single-rung negative result** (which is
itself a publishable finding, per the pre-pivot honesty discipline).

## 6. Build contract

- Builds via `pampc-paper build paper-02-empirical` once all consumed claim ids are pinned.
- G4 (byte-identical PDF from manifest root) gates submission.
- G7-float-discipline-S{n} must PASS for the S{n} section to be admissible.

## 7. Provenance

- Pre-pivot manifest: [`claims_archived.txt`](claims_archived.txt) (kept for diff against pre-2026-05-30 state).
- Active manifest: [`claims_used.txt`](claims_used.txt).
- Pivot rationale: [40-plan/mpc-substrate-pivot/PIVOT-MEMO.md](../../../40-plan/mpc-substrate-pivot/PIVOT-MEMO.md).
- Theory state: [10-theory/THEORY-CHECKPOINT-2026-05-30.md](../../10-theory/THEORY-CHECKPOINT-2026-05-30.md).
