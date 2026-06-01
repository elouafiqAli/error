# Copilot working agreement — `gnn_express`

This workspace hosts a multi-paper research program around the
*partition-conditional entropy bracket on the Bayes error*. The
governing document is
[`future-work/07-three-paper-arc-master-plan.md`](../future-work/07-three-paper-arc-master-plan.md);
the k-WL sequel plan is in
[`future-work/06-kwl-bracket-paper-roadmap.md`](../future-work/06-kwl-bracket-paper-roadmap.md).
Read both before any non-trivial change.

## Discipline mantra (non-negotiable)

> **Implement vigorously, concurrently; review constructively, audit
> adversarially; let no stone unturned; document progressively;
> commit at each gate, milestone, or feature.**

This is the standing operating rule for every coding turn in this
workspace.

## Operating principles

1. **Adversarial audit before celebration.** For every theorem,
   proof, lemma, or empirical claim, ask the four questions:
   - what does it *actually* say?
   - what's the *tightest* counter-example or kill condition?
   - what calibrated confidence does it deserve (`HIGH`, `MEDIUM`,
     `LOW`, `UNVERIFIED`)?
   - which adjacent claim does it falsify if pushed?

   Confidence calibration is recorded in
   [`future-work/07-three-paper-arc-master-plan.md`](../future-work/07-three-paper-arc-master-plan.md)
   §1 (theory audit table) — update it when claims move.

2. **Source of truth is `main.tex`, mirror is `main.md`.**
   - The TMLR/LaTeX manuscript at
     `partition-sandwich-preprint/main.tex` is the canonical paper.
   - The KaTeX markdown twin at
     `partition-sandwich-preprint/main.md` MUST be updated in lock-
     step. Never edit one without mirroring substantive changes to
     the other within the same logical task.
   - Run `make` in `partition-sandwich-preprint/` (which invokes
     `pdflatex → bibtex → pdflatex × 2`) and confirm a clean build
     before declaring a section done.

3. **Concurrent, parallel surgery on independent edits.** When
   multiple `F`-fixes / extensions touch disjoint regions of a
   file, batch them via `multi_replace_string_in_file`. Sequential
   single-edit calls are an anti-pattern for independent changes.

4. **Commit at every gate, milestone, or self-contained feature.**
   Conventional commit message template:
   ```
   paper-<a|b|c> Phase <N><letter>: <short summary>

   <one-paragraph what>
   <one-paragraph why / adversarial framing>
   <bullets of mechanical changes>
   ```
   The trace of Phase 1 in `git log` (commits `7936383` through
   `adb0da2`) is the canonical example.

5. **Zero new training when post-processing suffices.** Reuse
   existing JSON outputs in `partition-sandwich-preprint/experiments/results/`
   for falsification / verification / re-aggregation
   experiments (cf. `eK_falsification_protocol.py`). Touching a
   GPU is a last resort, not a default.

6. **Progressive documentation.** Every non-trivial decision lands
   in one of:
   - `future-work/` — multi-paper / strategic notes
   - `notes/paper-arxiv-review/` — per-section audits
   - `partition-sandwich-preprint/VERIFICATION.md` — mechanised
     verification status
   - inline `\emph{Status:}` lines for experiments
   Do not create new top-level documentation files unless the
   master plan calls for one.

7. **Stone-by-stone exhaustiveness.** No "TODO: prove later" left
   in published proofs. Either:
   - prove it inline, with all four bookkeeping steps explicit, or
   - downgrade the claim to a numbered conjecture / open problem
     with the failure mode named, or
   - cite the published reference that does the work and quote the
     specific theorem number.

   Proof sketches are acceptable only for results stated as
   "Folklore" or "well-known" with a citation.

## Repository conventions

- **Three-paper arc.** Paper A = `partition-sandwich-preprint/`
  (binary entropy bracket, this paper). Paper B (to be created at
  `partition-brackets-framework/`) = $\phi$-bracket meta-theorem
  with variance / noise / Markov-kernel instances. Paper C = k-WL
  / HDX trickle-down bracket.
- **Verification.** `verify.jl` (Julia, IntervalArithmetic) is the
  cross-check for Paper A's bracket; `verify_t{1,3,4}_*.py` are
  the Python counterparts. Any new theorem with closed-form
  endpoints SHOULD ship with a verifier.
- **Experiment naming.** `eN_<short>.py` writes to
  `experiments/results/eN.json` and figures to
  `experiments/figures/eN_*.pdf`. Post-hoc protocols use the
  letter prefix (`eK_*.py`).
- **Figure inclusion.** Every PDF in `experiments/figures/` that
  is referenced in a section MUST be `\includegraphics`'d
  (LaTeX) and `![](...)`'d (markdown). The Phase 1e commit fixed
  a regression where caption text mentioned figures but no
  graphics block included them.

## Forbidden patterns

- `\path{...}` or `\url{...}` inside a `\caption{}` (moving
  argument). Use `\texttt{...}` with escaped underscores instead.
- `\Eqref{...}` (undefined). Use `Equation~\eqref{...}`.
- Single-commit "everything" pushes. The atomic unit is a feature
  / fix / phase letter, not a milestone.
- Brute-forcing a failed approach. If pdflatex / a proof / an
  experiment fails twice the same way, diagnose root cause before
  the third attempt.
- Editing only `main.tex` or only `main.md` for content-bearing
  changes. The twin must stay in sync.

## When in doubt

Consult the master plan, calibrate confidence, write the
adversarial counter-claim, then act. If the action remains
ambiguous, surface a precise question to the user — never
"silently choose" between two non-equivalent research directions.
