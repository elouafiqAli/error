# 08 — P1 Patch Plan (Paper A reframing around the quantitative WL ceiling)

**Status:** active long-horizon plan.
**Owner:** Paper A (`partition-sandwich-preprint/`).
**Master plan parent:** [07-three-paper-arc-master-plan.md](07-three-paper-arc-master-plan.md).
**Prereqs:** depends on P0-B1 (restore Prop 6 / Prop 7) and P0-B2/B3
(corrected E3d-arch with cardinality fix). See dependency map in §0.
**Discipline mantra (non-negotiable):** *Implement vigorously, concurrently;
review constructively, audit adversarially; let no stone unturned;
document progressively; commit at each gate, milestone, or feature.*

This plan covers eight content patches (A–H) supplied verbatim by the
review, broken into nine phases (Phase 0 added in revision r2 to
repair two synthesis errors flagged by the PI review of the
5/5 closure) with explicit gates, commit points, and
adversarial-audit hooks. Numbering is content-anchored; renumber
theorems / propositions only after P0-B1 lands.

**Revision r2 (PI review of 5/5 closure, incorporated).** Two
verdicts from the PI read of the just-committed Synthesis section
(commit `3212fdf`) force a plan adjustment, captured here in full:

- **S3 is wrong.** The ogbn-arxiv bracket tightness was attributed
  to $w^{*}(\pi{=}0.161)=0$ (marginal-aware Prop 6, which does not
  yet even *exist* in the manuscript). The realised slack is
  $0.0029-0.0021 = 0.0008 > 0$, directly refuting the $w^{*}=0$
  reading; E2b independently shows $w^{*}(\pi{=}0.248)=0.1392 \gg 0$
  in the same regime. The actual mechanism is **Prop 4.5
  cardinality collapse**: $H(f\mid\Pi)\to 0$ on ogbn-arxiv because
  $|\Pi|/|V|$ approaches $1$. The marginal-aware reading must be
  retracted from main.{tex,md} and the attribution corrected.
- **S1 over-states "regime-determined, not architecture-determined."**
  The PubMed at-fixed-$k$ rows show architecture-dependent
  variation, which undercuts F2′ (the practitioner-relevant
  architecture-comparison claim). S1 must be hedged: the *sign* of
  `feat_gap` is dominated by the $(k, k_{\mathrm{WL}})$ regime, but
  the *magnitude* at fixed $k$ retains architecture dependence.
- **C2 (features beat WL) is NOT resolved by the closure.** The
  matched-$k$ rows (Cora $k/n=0.87$, CiteSeer $k/n=0.61$) are both
  inside the memorisation regime; "matched $k$" here means *both
  partitions near-memorise*, not *coarse enough to test
  expressivity*. State C2 conservatively as a
  **fixed-cell-budget** claim until the PATCH C $k\ll n$ redo
  (Phase 3b) lands. The current S7 verdict ("verified at matched
  $k$") is too strong and must be downgraded.
- **C3 strengthening is real but indirect.** $\sigma_{\hat R}$ is a
  *proxy* for the within-cell diameter $\delta_L$ that Lemma 6′/6″
  actually bounds. The airtight test is Phase 4b
  (PATCH D augmentation: measure $D(L)$ directly, compare to the
  $\lambda_{\max}(A)$ envelope). Until then C3 is *suggestive
  and consistent with theory*, not *confirmed*.
- **C1, C4 — confirmed at scale (100/100), but they are theorems.**
  Robustness demonstration, not new evidence. Re-write S7 rows to
  reflect this.

Phase 0 below codifies these corrections as the first, immediate,
P0-independent action of this plan.

**Revision r3 (P0 enumeration, incorporated).** The five P0
correctness-and-integrity items previously referenced abstractly as
"P0-B1, P0-B2, P0-B3" are now enumerated explicitly as Phases
**P0.1–P0.5** and elevated *ahead* of every PATCH phase. They are
the highest-priority work in this plan ("must close before any
submission"). See §2.0 below for the full ledger. The dependency
map in §0 is rewritten to reflect the explicit dependency edges
from P0.1–P0.5 into the PATCH phases.

**E3 reassessment is mandatory and lives inside P0.3 + P0.4.** The
entire E3 family (E3, E3b, E3c, E3d, E3d-arch, E3d-arch-full) was
last aggregated in commits up to `3212fdf` *without* the
`head_sig` sign fix (P0.3) and *without* the $k\ll n$ re-evaluation
(P0.4). Every E3 finding currently in main.{tex,md} must be re-read
after P0.3/P0.4 land; F1/F2/F3/F2′ either survive verbatim, are
restated, or are retracted. Phase 0 (synthesis hedge) is a
*stopgap*; the substantive E3 re-assessment is part of P0.3 + P0.4.

---

## §0 Dependency map (read this first)

```
[P0 — correctness & integrity; must close before any submission]

  P0.1 Prop 7 (finite-sample concentration; O(1/√n) rate)
  P0.2 Prop 6 (marginal-aware ceiling w*(π*) ≤ w*)
  P0.3 E3d-arch head_sig sign/interpretation fix
  P0.4 E3d-arch[-full] redo at k << n on Cora/CiteSeer (+ uniform caveat)
  P0.5 Population object ε*_Π,pop split + Prop 7 tie-in across E1–E3

[Phase 0 — stopgap synthesis hedges] (S3 retract, S1 hedge,
   C2/C3 downgrade in S7) — superseded in part by P0.3/P0.4

[PATCH phases — gated]

  Phase 1   PATCH A (abstract) + PATCH B (intro pivot)
              gated on: P0.1, P0.5
  Phase 2   PATCH F  (w* honesty)                       [P0-independent]
  Phase 3a  PATCH C theory (§8.3.1 (★) decomposition)
              gated on: P0.3, P0.5
  Phase 3b  PATCH C experiment (k≪n redo + decomp table)
              IS P0.4's experimental backbone; commit jointly
  Phase 4a  PATCH D theory (Lemma 6″)                   [P0-independent]
  Phase 4b  PATCH D experiment (D(L) vs λ_max(A))
              gated on: P0.4 run (re-uses same sweep)
  Phase 5   PATCH E  (related-work GNN-stability)       [P0-independent]
  Phase 6   PATCH H  (NAS reframing)                    gated on: P0.1
  Phase 7   PATCH G  (E1/E2 honest reframing)           [P0-independent]
  Phase 8   Lean 4 (Thm 1 + Cor 2; 6″a stretch)         [P0-independent]
```

**Rule.** P0.1–P0.5 are the **highest-priority work in the entire
plan** ("must close before any submission"). They execute on
Wavefront -1 (before everything else that depends on them).
Phase 0 is a stopgap for referee-visible synthesis errors and lands
immediately on Wavefront 0; it does NOT substitute for the
substantive E3 re-assessment, which lives in P0.3 + P0.4.
Phases 2, 5, 7, 8.1, 8.2, and Phase 4a are P0-independent and run
concurrently with P0.1–P0.5.

---

## §1 Audit table (calibrated confidence, update as evidence lands)

| ID  | Claim                                                                                   | Confidence pre-patch | Target post-patch | Falsifier                                            |
|-----|-----------------------------------------------------------------------------------------|----------------------|-------------------|------------------------------------------------------|
| A1  | $w^{*}=\tfrac12 H_{\mathrm{bin}}(1/5)-1/5\approx 0.1610$ is max width of binary region  | HIGH                 | HIGH              | Prop 1.5 reproof in `verify.jl`                      |
| A2  | Quantitative WL ceiling = $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi^{\mathrm{WL}}_L))$          | HIGH                 | HIGH              | Theorem 1 + Cor 7 substitution                       |
| A3  | Three-term decomposition $(\star)$ is an exact identity                                 | HIGH (Phase 3a closed: `prop:star-decomp` stated and proved in `sec:apps:star-decomp` of `main.tex` + mirrored in `main.md`; one-line algebraic-tautology check folded into `verify.jl` as `star_decomp_passed` over 10 000 random $\mathbb Q$ triples) | HIGH | One-line algebraic check; Lean target |
| A4  | Sign of $\Delta_{\mathrm{feat}}$ at matched $k$ (positive) on Cora/CiteSeer             | MEDIUM (matched-$k$ fixed-cell-budget reading retained from E3d-arch-full; resolution condition in `rem:resolution` confines the verdict to that statement — superseded by A4b for the expressivity reading) | MEDIUM (fixed-budget) | (no further test; A4b now carries expressivity) |
| A4b | C2 graduated: features carry label structure WL lacks, at $k\ll n$                      | HIGH (P0.4 closed: at $k=64$, GAT/GIN/SAGE on Cora and **all 4** archs on CiteSeer hit $\eps^{*}_{\Pi^Z_{64}} \le \eps_{\mathrm{WL}}$ with $k/|V|\le 0.024$, inside the $\kappa=0.1$ resolution condition of `rem:resolution`) | HIGH | E3d redo (closed); see `tab:e3d-arch-kll-n` |
| A5  | Lemma 6″c is orders tighter than 6′ on near-regular graphs                              | MEDIUM               | HIGH              | E3d augmentation, Phase 4 (theory committed in Phase 4a: `lem:mpnn-wl-spectral` in main.{tex,md}; empirical sweep deferred to Phase 4b) |
| A5b | C3 airtight: direct $D(L)$ measurement matches $\lambda_{\max}(A)$ envelope             | LOW (r2: $\sigma_{\hat R}$ is indirect proxy) | HIGH | Phase 4b $D(L)$ measurement                      |
| A5c | C3 indirect: GIN $\sigma_{\hat R}$ vs others scales with $\Delta_{\max}$                | HIGH (10.7× on ogbn-arxiv)   | HIGH         | 5/5 sweep, already observed                          |
| A6  | NAS pre-filter regime characterised by $n_{\mathrm{tr}}$ and non-memorising family      | MEDIUM               | HIGH              | Gated on Prop 7 (P0-B1)                              |
| A7  | Lemma 6′/6″ orthogonal to GNN-stability literature                                      | MEDIUM               | HIGH              | Literature sweep, Phase 5                            |
| A8  | E1/E2 are identities, not evidence                                                      | HIGH                 | HIGH              | Definitional; PATCH G                                |
| A9  | Lean 4 mechanisation of Thm 1 + Cor 2                                                   | UNVERIFIED           | HIGH (committed)  | Lean kernel accepts file                             |
| A10 | ogbn-arxiv bracket tightness is due to Prop 4.5 cardinality collapse, NOT $w^{*}=0$     | HIGH (r2: $0.0008$ realised slack refutes $w^{*}=0$) | HIGH | Phase 0 attribution fix                |
| A11 | At fixed $k$, $\hat R$ retains architecture dependence (PubMed; falsifies pure-regime reading) | HIGH (r2: PubMed at $k{=}4096$) | HIGH       | 5/5 sweep, already observed                          |
| A12 | Prop 7 explicit $O(1/\sqrt n)$ constant matches E7 $p_{95}$ within stated slack         | HIGH (P0.1 closed: $\kappa$-free bound covers $p_{95}$ on every row; proved $\kappa\!\approx\!194$ explained by $\eta_{\min}\!\to\!0$, not a mis-stated constant) | HIGH | `verify_prop7_constant.py` |
| A13 | Prop 6 closed form for $w^{*}(\pi_{*})$ matches E2b column to 4 decimals                | HIGH (P0.2 closed: `verify_prop6_marginal.py` PASS on L1 tab:marginal grid 4dp, L2 e2b.json `w_marg` 4dp on all 4 datasets, L3 brute-force argmax vs closed form $\le 10^{-4}$, threshold continuity) | HIGH | P0.2 verifier (closed) |
| A14 | E3d-arch `head_sig` sign/definition agree with prose and $\Delta_{\mathrm{head}}$       | HIGH (P0.3 closed: `head_sig := Rhat - eps*_tr`, all 9 + 20 cells flipped, prose rewritten) | HIGH | P0.3 sign fix (closed) |
| A15 | F1/F2/F3/F2′ survive E3d-arch redo at $k\ll n$ on Cora/CiteSeer                         | HIGH (P0.4 closed: F1″ closes C2 — GAT/GIN/SAGE on Cora and **all 4** archs on CiteSeer reach eps_tr ≤ eps_WL at $k=64$, $k/n\le 0.024$; F2″ GCN<GAT<GIN ordering preserved; F3″ head-slack $k$-dependent — F3′ confined to matched-$k$. Table `tab:e3d-arch-kll-n`.) | HIGH | P0.4 sweep (closed) |
| A16 | $\varepsilon^{*}_{\Pi}$ in E1–E3 disambiguated as empirical vs population              | HIGH (P0.5 closed: `rem:emp-pop` defines $\varepsilon^{*}_{\Pi,\mu}$, E1+E2+E3 captions all cite Prop 7 with the $O(1/\sqrt n)$ shift and the marginal-weighted form) | HIGH | P0.5 notation rewrite (closed) |

---

## §2 Phase ledger

Each phase has: **scope**, **inputs**, **outputs**, **gate** (what
must pass before commit), **commit template**, **adversarial review
checklist**, and **rollback plan**.

### §2.0 P0 phases (correctness & integrity — must close before submission)

Five enumerated P0 items. Execute on **Wavefront -1**, ahead of every
PATCH phase that depends on them. Each is its own commit.

#### P0.1 — State and prove Proposition 7 (finite-sample concentration)

- **Scope.** State \Cref{prop:finite-sample-concentration}
  formally: empirical bracket endpoints concentrate to the
  population bracket at $\Theta(1/\sqrt n)$ via Hoeffding (or
  McDiarmid on the partition cells, whichever the constant chases).
  Prove inline; record the explicit constant.
- **Audit.** E7 currently reports empirical $p_{95}$ at $\sim 10\times$
  inside the claimed bound. Confirm whether this slack is:
  (a) the $\kappa$-free simplification (acceptable; document it),
  (b) a mis-stated constant in the previous draft (must be fixed),
  or (c) a tighter regime not covered by Hoeffding (state
  separately).
- **Outputs.** New proposition + proof in main.{tex,md};
  E7 numbers re-derived against the proved constant; recompute
  `verify_t1_python.py` or add `verify_prop7.py`.
- **Gate.** (i) Proof reads cleanly; (ii) E7 $p_{95}$ ratio either
  matches the new constant or has a written, defended reason for
  the gap; (iii) `make` clean.
- **Commit.** `paper-a P0.1: state + prove Proposition 7 (Θ(1/√n), Hoeffding constant verified)`

#### P0.2 — State and prove Proposition 6 (marginal-aware ceiling)

- **Scope.** State \Cref{prop:marginal-aware-ceiling}:
  $w^{*}(\pi_{*}) \le w^{*}$, with the explicit closed form for
  $w^{*}(\pi_{*})$ over $\pi_{*}\in (0,1)$. Prove and prove the
  reduction $w^{*}(\pi_{*})\to w^{*}$ as $\pi_{*}\to 1/2$.
- **Outputs.** E2b table re-derived against the proved
  $w^{*}(\pi_{*})$ column; any mismatched row flagged and fixed.
  `verify_prop6.py` added.
- **Gate.** (i) E2b's $w^{*}(\pi_{*})$ column matches the
  formula to four decimals on every row; (ii) the $\pi_{*}\to 1/2$
  limit is exhibited numerically; (iii) `make` clean.
- **Commit.** `paper-a P0.2: state + prove Proposition 6 (w*(π*) ≤ w*, with closed form)`

#### P0.3 — E3d-arch `head_sig` sign / interpretation fix (B2)

- **Scope.** Decide on the *intended* claim for `head_sig`. Two
  options on the table:
  (i) `head_sig := ε*_Π^Z_k - ̂R` (positive = head extracts
      sub-cell structure beyond cluster Bayes; sign matches the
      original prose).
  (ii) `head_sig := ̂R - ε*_Π^Z_k` (positive = head slack;
      matches the (⋆) decomposition in PATCH C).
  Resolve in favour of (ii) for compatibility with PATCH C
  $\Delta_{\mathrm{head}}$, OR document why (i) is preserved and
  flip the sign in the post-hoc reader.
- **Outputs.** Updated definition + restated F3/F3′ in main.{tex,md}
  so the table, prose, and definition agree; reader file
  (`e3d_arch_full.5of5.summary.md`) re-computed with the chosen
  convention.
- **Gate.** (i) Definition, table caption, and prose all show the
  same sign convention; (ii) cross-reference to PATCH C
  $\Delta_{\mathrm{head}}$ is consistent.
- **Commit.** `paper-a P0.3: fix E3d-arch head_sig sign + restate F3/F3' uniformly`

#### P0.4 — E3d-arch[-full] redo at $k\ll n$ (B3) **— the empirical backbone**

- **Scope.** Re-run GCN/GAT/GIN/SAGE at $k\in\{8,16,32,64\}$
  (extend to 128 if budget allows) on Cora and CiteSeer
  (PubMed, Twitch-EN extension nice-to-have; ogbn-arxiv reuses
  5/5 cache rows that are already $k\ll n$ by virtue of $k/n=1/39$).
  Evaluate $\varepsilon_{\mathrm{WL}}$ and $\varepsilon^Z_k$ at
  the **same** $k$ (kills the cell-budget confound). Same
  $L=3, h=128, 200$ epochs, $5$ seeds per cell.
- **Outputs.** `experiments/results/e3d_arch_kll_n.json` +
  `e3d_arch_kll_n.summary.md` + new table in §8.3.1 (replacing
  the misleading $k\approx n$ rows of E3d-arch).
- **E3 reassessment (mandatory).** Re-read F1/F2/F3 against the
  new data:
  - F1 (bracket holds): expected to survive trivially.
  - F2 (features beat WL at matched $k$): now testable as an
    expressivity claim, not a memorisation artefact.
  - F2′ (architecture dependence at fixed $k$): re-check on the
    new sweep, not on the 5/5 cache.
  - F3/F3′ (head slack interpretation): depends on P0.3 sign fix.
  Each finding either *survives verbatim*, is *restated*, or is
  *retracted in writing*. No silent edits.
  Apply the cardinality-confound caveat **uniformly** — including
  Cora at $k/n=0.87$, which the previous draft exempted.
- **Gate.** (i) Every reported row has $k/n \le 0.1$ (or is
  explicitly labelled as a memorisation-regime sanity check);
  (ii) $\varepsilon_{\mathrm{WL}}$ and $\varepsilon^Z_k$ share
  the same $k$ on every row; (iii) F1–F3′ verdict table written;
  (iv) the Synthesis section in main.{tex,md} updated to cite
  the new E3d-arch table, not the old one.
- **Commit.** `paper-a P0.4: E3d-arch redo at k<<n; F1/F2/F3/F2' re-assessed against new sweep`

#### P0.5 — Population object $\varepsilon^{*,\mathrm{pop}}_{\Pi}$ + Prop 7 tie-in

- **Scope.** Define
  $\varepsilon^{*,\mathrm{pop}}_{\Pi} := \mathbb E[\min(\eta(C), 1-\eta(C))]$
  in §3 (or wherever $\varepsilon^{*}_{\Pi}$ is first introduced).
  Rewrite the practitioner-claim text of E1–E3 to distinguish
  empirical from population. Add a sentence in each of E1, E2, E3
  citing Proposition 7 for the empirical→population gap.
- **Outputs.** Notation paragraph in §3; E1–E3 claim text updated.
- **Gate.** Every E1–E3 sentence asserting "the bracket bounds
  ..." specifies which object is being bounded (empirical or
  population).
- **Commit.** `paper-a P0.5: define ε*_Π,pop; rewrite E1–E3 with empirical/population split tied to Prop 7`

---

### Phase 0 — Synthesis corrections (r2 stopgap) **[Wavefront 0, P0-independent]**

Referee-visible errors introduced by the S1/S3/S7 synthesis in
commit `3212fdf`. Repair before any new patch lands.

- **Scope.**
  - **S3 retraction.** Delete the marginal-aware
    $w^{*}(\pi{=}0.161)=0$ reading from main.{tex,md}. Replace with
    the Prop 4.5 cardinality-collapse attribution
    ($H(f\mid\Pi)\to 0$ as $|\Pi|/|V|\to 1$). State the realised
    slack $0.0029-0.0021=0.0008>0$ explicitly as the falsifier of
    the previous (incorrect) reading.
  - **S1 hedge.** Restate as: *the sign of $\mathtt{feat\_gap}$ is
    regime-determined; the magnitude at fixed $k$ remains
    architecture-dependent (PubMed, $k=4096$, shows non-trivial
    spread across GCN/GAT/GIN/SAGE).* Preserves F2′.
  - **C2 downgrade in S7.** Replace "verified at matched $k$,
    falsified at $k\ll k_{\mathrm{WL}}$" with: "verified as a
    **fixed-cell-budget** statement only; the matched-$k$ rows
    (Cora $k/n=0.87$, CiteSeer $k/n=0.61$) sit inside the
    memorisation regime and do not test expressivity. The
    expressivity claim is **pending Phase 3b** ($k\ll n$ redo)."
  - **C3 hedge in S7.** Replace "quantitatively verified" with:
    "suggestive and consistent with Lemma 6′/6″ via the
    $\sigma_{\hat R}$ proxy; **airtight confirmation pending
    Phase 4b** (direct $D(L)$ measurement vs $\lambda_{\max}(A)$
    envelope)." The $10.7\times$ headline stays; only the verdict
    word changes.
  - **C1/C4 hedge in S7.** Add "— these are theorems; 100/100 is
    robustness-at-scale, not new evidence."
- **Inputs.** Current main.{tex,md} (post `3212fdf`), this revision
  table.
- **Outputs.** main.{tex,md} updated in lock-step; one-paragraph
  erratum block added to
  [partition-sandwich-preprint/VERIFICATION.md](../partition-sandwich-preprint/VERIFICATION.md)
  recording the S3 retraction and the C2/C3 hedges as audit-trail.
- **Gate.** (i) `grep -n "0.161" main.md main.tex` returns no
  marginal-aware $w^{*}=0$ claim; (ii) `make` clean; (iii)
  audit-table rows A4, A5b, A10, A11 reflected in the manuscript
  text, not just this plan.
- **Commit.**
  ```
  paper-a Phase 0: synthesis corrections (S3 retract, S1 hedge, C2/C3 downgrade)

  Repairs three issues flagged by the PI review of the 5/5 closure
  synthesis (commit 3212fdf):
  - S3: ogbn-arxiv bracket tightness attributed to Prop 4.5
    cardinality collapse, not w*(0.161)=0 (marginal-aware reading
    retracted; realised slack 0.0008>0 falsifies w*=0; Prop 6 not
    yet stated so the claim was uncheckable anyway).
  - S1: sign of feat_gap is regime-determined; magnitude at fixed
    k retains architecture dependence (PubMed at k=4096) —
    preserves F2'.
  - S7: C2 downgraded to fixed-cell-budget claim (matched-k rows
    sit in memorisation regime, Cora k/n=0.87, CiteSeer 0.61);
    expressivity claim deferred to Phase 3b. C3 hedged to
    "suggestive via sigma proxy"; airtight test deferred to
    Phase 4b D(L) vs lambda_max(A). C1/C4 re-labelled as
    robustness-at-scale, not new evidence.

  Erratum recorded in VERIFICATION.md.
  ```
- **Adversarial checklist.**
  - [ ] S3 text no longer mentions $w^{*}(\pi)$ or marginal-aware
    Prop 6 (Prop 6 doesn't exist yet — a manuscript that
    references it would be incoherent).
  - [ ] S1 text names PubMed at fixed $k$ as the falsifier of the
    pure-regime reading.
  - [ ] S7 verdict column for C2 contains the word
    "fixed-cell-budget" (not "matched-$k$").
  - [ ] S7 verdict column for C3 contains "suggestive" or
    "consistent with", not "confirmed".
  - [ ] VERIFICATION.md erratum entry exists.
- **Rollback.** All edits are in two contiguous Synthesis regions
  (one per file); `git revert` is safe.

### Phase 1 — Abstract + intro pivot (PATCH A, PATCH B)

- **Scope.** Replace abstract verbatim (PATCH A). Insert new
  subsection "The question a node-classification practitioner
  actually asks" after "### The two questions", before
  "### Why entropy?" (PATCH B).
- **Inputs.** PATCH A and B verbatim; current
  `partition-sandwich-preprint/main.{tex,md}`.
- **Outputs.** Both files updated in lock-step.
- **Gate.** (i) `make` clean; (ii) `verify.jl` green;
  (iii) Prop 7 must already exist in the manuscript (P0-B1) — the
  abstract's "Proposition 7" reference becomes a dangling
  `\ref` otherwise.
- **Commit.**
  ```
  paper-a Phase 1: reframe abstract + intro around quantitative WL ceiling

  PATCH A replaces the abstract with the WL-quantitative-ceiling
  centrepiece, drops the unverifiable "first" claim on w*, names
  the informative empirical benchmarks (CiteSeer/PubMed, Adult-NAS),
  commits to Lean 4 mechanisation of Thm 1 + Cor 2.

  PATCH B inserts a new pivot subsection making the practitioner
  question explicit and forward-referencing the three-term
  risk decomposition.
  ```
- **Adversarial checklist.**
  - [ ] Every numeric claim in the abstract has a defended source.
  - [ ] No verb stronger than the proof supports
    ("bounds" not "predicts"; "is" not "explains").
  - [ ] Lean commitment is real, not aspirational (link to Phase 8).
- **Rollback.** `git revert` is safe; phase touches only two
  contiguous regions per file.

### Phase 2 — $w^{*}$ honesty (PATCH F) **[P0-independent, run first]**

- **Scope.** Replace the §1 "uniform conservativeness gap" sentence
  + add footnote at Corollary 2 (PATCH F).
- **Inputs.** PATCH F verbatim.
- **Outputs.** main.{tex,md} updated; literature note appended to
  [notes/paper-arxiv-review/13-bayes-entropy-sandwich-literature-note.md](../notes/paper-arxiv-review/13-bayes-entropy-sandwich-literature-note.md)
  listing each source checked (Feder–Merhav 1994, Ho–Verdú 2010,
  Sason–Verdú 2018, Harremoës–Topsøe, Prasad).
- **Gate.** Literature sweep completed; if prior statement of
  $0.1610$ found, cite explicitly.
- **Commit.**
  ```
  paper-a Phase 2: w* framed as max width of achievable region (PATCH F)
  ```
- **Adversarial checklist.**
  - [ ] Footnote text matches PATCH F exactly.
  - [ ] Literature note records *negative* findings as well as
    positive (silence != absence).

### Phase 3 — Risk-decomposition theorem + E3d-arch redo (PATCH C) **[GATED ON P0-B2/B3]**

This phase has two sub-phases that MUST be committed separately.

#### Phase 3a — Theory only

- **Scope.** Insert §8.3.1 "An exact decomposition of trained risk
  against the WL ceiling" with the identity $(\star)$, the
  "resolution condition", and the deletion of the old E3d-arch
  prose that asserts the inverted sign (P0-B2 fix).
- **Inputs.** PATCH C theory block, current §8.3 (Corollary 7) as
  anchor.
- **Outputs.** main.{tex,md} updated; old paragraph
  ("negative head_sig = head extracts sub-cell structure …")
  deleted with `git diff` showing the removal.
- **Gate.** (i) $(\star)$ checked symbolically (the three bracketed
  terms must sum to $\hat R$ — a one-line check, write it as a
  comment in `verify.jl`); (ii) `make` clean.
- **Commit.**
  ```
  paper-a Phase 3a: §8.3.1 exact three-term risk decomposition against WL ceiling
  ```

#### Phase 3b — Experiment redo at $k\ll n$

- **Scope.** Re-run GCN/GAT/GIN/SAGE sweep over Cora, CiteSeer,
  PubMed, Twitch-EN at $k\in\{8,16,32,64,128\}$ with $k/n\le 0.1$
  on every dataset (ogbn-arxiv stretch goal — reuse the 5/5 cache
  if available).
- **Inputs.** Existing e3d_arch_full.5of5 cache + new sweep
  driver that fixes the cell-budget mismatch
  (eval $\varepsilon_{\mathrm{WL}}$ and $\varepsilon^Z_k$ at the
  *same* $k$).
- **Outputs.** `experiments/results/e3d_arch_decomp.json` +
  `experiments/results/e3d_arch_decomp.summary.md` + table in §8.3.1.
- **Gate.** (i) $k/n$ reported on every row; (ii) any
  $k\approx n$ row rejected by the resolution condition is
  *named* in the caption, not silently dropped; (iii) the three
  findings (features refine WL; attention can erase structure;
  head slack) are either reaffirmed in this regime OR retracted
  with a written falsifier.
- **Commit.**
  ```
  paper-a Phase 3b: E3d-arch redo at k<<n, populates §8.3.1 table
  ```
- **Adversarial checklist.**
  - [ ] No row evaluated at $k/n>0.1$ is used as evidence.
  - [ ] Sign claims for $\Delta_{\mathrm{feat}}$ / $\Delta_{\mathrm{head}}$
    are stated as observations, not theorems.
  - [ ] Cell-budget mismatch from the 5/5 sweep is named as the
    falsifier of the original E3d-arch reading.

### Phase 4 — Lemma 6″ (spectral refinement, PATCH D)

#### Phase 4a — Theory only

- **Scope.** Insert Lemma 6″ between Lemma 6′ and Corollary 7
  (statement + proof, both forms 6″a/b/c/d).
- **Gate.** (i) Independent re-derivation of (6″b) on a $4\times 4$
  toy adjacency in `verify.jl`; (ii) cell-margin hypothesis
  $\gamma$ named as a *labelled* assumption (not silent); (iii)
  `make` clean.
- **Commit.**
  ```
  paper-a Phase 4a: Lemma 6″ — adjacency-Perron-root refinement of 6′
  ```

#### Phase 4b — Empirical augmentation

- **Scope.** Augment E3d with per-graph $\lambda_{\max}(A), \bar d, \Delta$,
  the (6″c) bound, the (6′) bound, and measured $\bar\delta_L$ and $\sup D(L)$.
- **Gate.** (6″c) sits orders below (6′) on the near-regular
  graphs; residual gap to measured $\bar\delta_L$ is reported as
  the *cancellation factor*, not closed.
- **Commit.**
  ```
  paper-a Phase 4b: empirical confirmation of Lemma 6″c (Perron-root tightening)
  ```
- **Adversarial checklist.**
  - [ ] No claim that 6″ closes the full $10^6$ gap; residual is named.
  - [ ] Sup-diameter is NOT claimed to be tightened (only mass-average).

### Phase 5 — Related work (PATCH E) **[P0-independent, run concurrently with Phase 2]**

- **Scope.** Append "Stability vs robust constancy" paragraph to §9.
- **Gate.** Literature sweep (titles, years, exact bound forms) for
  Gama–Bruna–Ribeiro, Kenlay et al., Alon–Yahav, Topping et al.,
  Di Giovanni et al., Sato, positional-encoding stability papers.
  If any prior bound is a relabelling of 6′ → reposition 6″ as
  contribution and 6′ as recalled case.
- **Output.** Paragraph appended; bibtex entries verified; results
  recorded in [notes/paper-arxiv-review/](../notes/paper-arxiv-review/).
- **Commit.**
  ```
  paper-a Phase 5: related work — Lemma 6′/6″ vs GNN-stability literature
  ```

### Phase 6 — E6-NAS reframing (PATCH H) **[GATED ON P0-B1: Prop 7 must exist]**

- **Scope.** Replace E6-NAS "Takeaway for practitioners" paragraph
  with the regime-characterised version that ties success
  (Adult, large $n$) and failure (digits-bin, small $n$) to a
  single theorem (Prop 7).
- **Gate.** (i) Prop 7 is in the manuscript with proof;
  (ii) the $O(1/\sqrt n)$ constant in Prop 7 is consistent with the
  measured Adult $\tau$ CI and the digits-bin collapse;
  (iii) the practitioner rule is stated as a *conditional* on
  $n$ and family non-memorisation.
- **Commit.**
  ```
  paper-a Phase 6: E6-NAS reframed as regime-characterised pre-filter (PATCH H)
  ```

### Phase 7 — E1/E2 honest reframing (PATCH G) **[P0-independent]**

- **Scope.** Replace E1 lead and E2 lead with the
  "identity, not evidence" framings; tables stay.
- **Gate.** Abstract no longer cites E1/E2 "four-decimal match"
  as evidence (PATCH A already removes this — verify after Phase 1).
- **Commit.**
  ```
  paper-a Phase 7: E1/E2 reframed as consistency checks, not evidence (PATCH G)
  ```

### Phase 8 — Lean 4 mechanisation **[blocking the abstract commitment]**

- **Scope.** Mechanise Theorem 1 and Corollary 2 in Lean 4.
  Stretch: mechanise Lemma 6″a (non-negative-matrix monotone
  iteration — clean `Matrix`/`Finset.sum`/entrywise order target).
- **Gate.** (i) Lean kernel accepts the file
  (`lake build` clean); (ii) statements match the LaTeX up to
  notation; (iii) `partition-sandwich-preprint/VERIFICATION.md`
  updated.
- **Commit (per result, not batched).**
  ```
  paper-a Phase 8.1: Lean 4 — Theorem 1 (Fano lower endpoint)
  paper-a Phase 8.2: Lean 4 — Corollary 2 (w* bound)
  paper-a Phase 8.3: Lean 4 — Lemma 6″a (stretch; non-negative-matrix monotone iteration)
  ```
- **Rollback.** Lean directory is isolated; failed mechanisation
  is allowed only if the abstract is amended to remove the
  commitment in the same commit.

---

## §3 Concurrent wavefronts (which phases parallelise)

Wavefront -1 (highest priority — correctness & integrity, must close before submission):
- P0.1 (Prop 7)
- P0.2 (Prop 6)
- P0.3 (head_sig sign)
- P0.4 (k≪n redo + E3 reassessment) — longest pole
- P0.5 (population vs empirical split)

P0.1, P0.2, P0.5 parallelise freely (disjoint manuscript regions);
P0.3 + P0.4 commit jointly (sign fix lands in the redo). P0.5
should land *before* Phase 1 abstract rewrite.

Wavefront 0 (start NOW — referee-visible stopgap):
- Phase 0 (synthesis corrections; superseded in part by P0.3/P0.4 later)

Wavefront 1 (start immediately after Phase 0, no P0 dependency):
- Phase 2 (PATCH F, $w^*$ honesty)
- Phase 4a (Lemma 6″ theory — P0-independent)
- Phase 5 (PATCH E, related work)
- Phase 7 (PATCH G, E1/E2 reframing)
- Phase 8.1 / 8.2 (Lean 4 Thm 1 + Cor 2 — independent of LaTeX content)

Wavefront 2 (after P0-B2/B3 lands):
- Phase 3a (theory)
- Phase 4a (Lemma 6″ theory)
Wavefront 3 (after P0-B1 lands AND Phase 3a):
- Phase 1 (abstract + intro pivot)
- Phase 6 (NAS reframing)

Wavefront 4 (after Phase 3a/4a):
- Phase 3b (E3d-arch redo experiment)
- Phase 4b (Lemma 6″ empirical augmentation)
- Phase 8.3 (Lean 4 6″a — gated on 4a)

Within a wavefront, batch independent edits to disjoint regions via
`multi_replace_string_in_file`. Sequential single-edit calls for
independent changes are an anti-pattern (per
`.github/copilot-instructions.md` §3).

---

## §4 Standing rules for this plan

1. **Twin discipline.** Every patch lands in `main.tex` and `main.md`
   in the same logical task. The KaTeX markdown twin is not a
   second-class artefact.
2. **Build gate.** `cd partition-sandwich-preprint && make` must
   succeed at every commit — no undefined refs, no missing cites.
3. **Audit before celebration.** Every phase has an adversarial
   checklist that runs *before* the commit, not after.
4. **No new training unless explicitly demanded.** Phase 3b and
   Phase 4b *do* require fresh runs (the resolution condition fix
   cannot be post-hoc-derived from the 5/5 cache). Everything else
   is post-processing of existing JSON.
5. **Stone-by-stone exhaustiveness.** No "TODO: prove later" lands
   in the manuscript. Either prove inline, downgrade to a named
   conjecture, or cite the published reference.
6. **Verification.** Every closed-form endpoint added (Lemma 6″c,
   risk decomposition $(\star)$) gets a `verify.jl` (or
   `verify_*.py`) check.
7. **Renumbering.** Theorem / proposition / lemma numbers are
   *not* fixed until P0-B1 lands; use content-anchored
   cross-references in the interim
   (`\Cref{thm:bracket}`, not `\Cref{thm:1}`).
8. **Confidence calibration.** Update §1's audit table at the end
   of every phase. A claim that moves from MEDIUM to HIGH without
   an experiment or proof is suspect.

---

## §5 Definition of done

The plan is complete when:
- [ ] **P0.1–P0.5 closed** (Prop 7, Prop 6, head_sig sign, k≪n redo + E3 reassessment, population object).
- [ ] Phase 0 synthesis corrections landed (stopgap; superseded by P0.3/P0.4 where they overlap).
- [ ] All eight patches (A–H) are in `main.{tex,md}`.
- [ ] §1 audit table has no UNVERIFIED rows.
- [ ] `make` is clean; `verify.jl` is green; `lake build` is green
  (for Phase 8 commitments).
- [ ] `VERIFICATION.md` reflects the new Lean targets.
- [ ] Every commit message follows the conventional template.
- [ ] No phase has been merged that violates its gate.
- [ ] The "Needs" checklist in the review (E3d redo, 6″ augmentation,
  literature verification, Lean 4 commitment) is fully discharged or
  has an explicit, justified deferment in `future-work/`.

---

## §6 Open question deferred to user

The review ends offering to draft candidate statements + proofs for
the missing **Proposition 6** ($w^{*}(\pi_{*})$ marginal-aware
ceiling) and **Proposition 7** (finite-sample concentration).
Several phases here (1, 3, 6) lean on Prop 7; Phase 6 is hard-gated
on it. **Recommendation:** accept the offer and execute Prop 6 / 7
draft as P0-B1 before starting Wavefront 3. Surface this back to the
user at the start of execution.
