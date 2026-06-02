# `onboarding/` — operator on-ramp to the partition-bracket programme

**Audience.** *Operator*: software engineer, BSc, ~15 yr industry
experience. Reads code fluently, reads research papers slowly, has not
yet touched GNNs, information theory, Lean, or Julia.

**End state (after gate G2).** The operator can:

1. **Read the abstract of [`partition-sandwich-preprint/main.tex`](../partition-sandwich-preprint/main.tex)
   like a native** — every symbol ($\varepsilon^*_\Pi$, $H(f \mid \Pi)$,
   $H_{\mathrm{bin}}^{-1}$, $w^* \approx 0.1610$, $\Pi^{\mathrm{WL}}_L$)
   has a 1-sentence operational meaning *and* a Python toy demonstrating
   it.
2. **Reproduce the headline experiment E3** (WL bracket on Cora /
   CiteSeer / PubMed / ogbn-arxiv) on their own laptop / a single GPU
   box, including the bracket-vs-realised-error scatter plot.
3. **Explain the 2019 Xu–Morris insight** ("no MPNN exceeds 1-WL") and
   *why* the bracket turns it from a qualitative ceiling into a
   quantitative number ($w^* \approx 0.1610$ slack, always).
4. **Pick up an experiment design and run a comparative arch-vs-arch
   duel** (E4 / E6) without supervision.

Everything else — Lean mechanisation, Julia interval verifiers, deep
information-theoretic re-derivations — is **optional rigour** the
operator may pick up later via the project's main mantra
([`.github/copilot-instructions.md`](../.github/copilot-instructions.md))
and the macro plan in
[`reader-monograph/PLAN.md`](../reader-monograph/PLAN.md).

## Spirit

fast.ai inversion: **do first, name later.** Theory only enters when an
experiment, a plot, or an intuition literally fails without it. Mathlib,
Lean, and Julia are *tools*, not gates. If we can grasp a construct by
throwing a stone like a projectile (one Python plot, one `numpy`
oneliner, one Cora subgraph) — we do that. We do not derive what we can
*use*.

## Companion artefacts

| Artefact | Read it when… |
|---|---|
| [`gnn.md`](../gnn.md) Ch 1–2, Ch 6 | iteration **v1** (partitions, entropy, Bayes risk) |
| [`gnn.md`](../gnn.md) Ch 4, Ch 7 | iteration **v2** (WL operator, refinement engineering) |
| [`partition-sandwich-preprint/main.tex`](../partition-sandwich-preprint/main.tex) abstract + §1 | iteration **v1** day 1 |
| [`partition-sandwich-preprint/experiments/REPORTS.md`](../partition-sandwich-preprint/experiments/REPORTS.md) | iteration **v2** (E1 → E3 → E6) |
| [`reader-monograph/PLAN.md`](../reader-monograph/PLAN.md) | **after G2** only |
| [`partition-sandwich-preprint/formal/`](../partition-sandwich-preprint/formal/) | **after G2** only, and only if the operator wants to formalise |

## Colour code (read this before you skip anything)

- **WHITE / GREY** — mandatory; gate-blocking.
- **YELLOW** — skim once. Two consecutive yellow skips = debt that must
  be repaid before the next gate's self-assessment, else the gate fails.
- **BLUE** — pure rigour polish; never affects experiments, intuition,
  or reproducibility. Skip freely.

## Cap

This on-ramp stops at **G2**. After G2 the operator is no longer an
operator — they are a contributor.

For the full plan see [`PLAN.md`](PLAN.md).

## Sibling tracks

The on-ramp is the canonical critical path; two parallel tracks are
optional add-ons for graduate students who want graded structure or
theory visualisation.

| Folder | What it is | When to start |
|---|---|---|
| [`PLAN.md`](PLAN.md) | the on-ramp, G0–G2 | day 0 |
| [`projects/`](projects/) | Stanford-style PSets (HW1–HW4) + Udacity-style capstone (M1–M5), graded | after G1 |
| [`julia-theory/`](julia-theory/) | 12 Pluto notebooks visualising every theory object in the paper, ungraded | whenever an equation feels opaque |
| [`DEVELOPMENT-PLAN.md`](DEVELOPMENT-PLAN.md) | meta-plan for building out the onboarding suite | implementer / contributor only |
| [`notes/`](notes/) | running development logs, audits, reviews | implementer / contributor only |
