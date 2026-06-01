# Three-paper arc master plan

Draft 2026-06-01. Supersedes nothing; cross-references
`05-sequel-paper-plan.md` and `06-kwl-bracket-paper-roadmap.md`.

This document records (i) a meticulous theory audit of the
additions proposed in the recent conversation, (ii) the fork
decision (extend vs. new paper), and (iii) a 7-phase long-horizon
plan.

---

## Part 1 — Theory audit results

Re-derived each non-trivial claim from scratch. Final
confidences (probability the claim survives a rigorous TCS
reviewer):

| Claim | Final confidence | Notes |
|---|---|---|
| T1 variance bracket $p(1-p)\le\min(p,1-p)\le 2p(1-p)$ | 0.98 | Trivial proof. Additive slack $\le 1/4$ vs entropy $\le 0.161$ — entropy strictly tighter additively. |
| T2 Pinsker $H_2^{-1}(H)\ge \tfrac12 - \tfrac12\sqrt{\ln 4\cdot(1-H)}$ | 0.95 | Standard binary Pinsker. |
| T3 meta-theorem $\phi$-bracket | 0.92 | True; requires explicit hypothesis: $\phi$ concave, $\phi(0)=0$, $\phi^{-1}$ defined on image for Jensen-sharp lower side. |
| T4 noise correction $\varepsilon^\*(\tilde f) = \eta + (1-2\eta)\varepsilon^\*(f)$ | 0.95 pop / 0.80 finite | Holds **exactly** at the population level — no proviso needed (my prior claim of $\min_C\|P_C-1/2\| > \eta$ was wrong). Finite-sample sign flips are the standard concentration concern. |
| T5 Rand-index partition stability | **0.40** | Unverified. Drop unless proven. |
| T6 refinement-to-discreteness pinch | 0.99 | Trivial. |
| T7 regression bracket | 0.95 reformulated / 0.50 as originally stated | Honest form: MSE = $\mathbb E[\mathrm{Var}]$ identity (no bracket); MAE Cauchy–Schwarz upper only. |
| T8 soft-partition / Markov-kernel bracket | 0.90 | Holds with explicit definition $\varepsilon^\*_K := \sum_C q_C^K \min(P_C^K, 1-P_C^K)$. |
| T9 Lemma 6′ exponential blow-up | 0.95 | Correct for *sum* aggregator; trivialised for *mean*; depends on aggregator type — paper's blanket statement needs splitting. |

**Material corrections to prior turns:**

- **T4**: the noise correction is exact at the population level. No
  proviso. The proviso I asserted earlier is a finite-sample
  artefact, already covered by Prop 7's concentration framework.
- **T5**: dropped from confirmed list. Must be proved or disproved
  before being used in either paper.
- **T7**: reformulated. MSE case is an *identity*, not a bracket.
- **T3**: hypothesis $\phi^{-1}$ on image needed for the Jensen-sharp
  lower side. Variance instance: $\phi^{-1}(v)=\tfrac12-\tfrac12\sqrt{1-4v}$.

---

## Part 2 — Fork decision: three papers

Resolved: **three-paper arc**, executed sequentially.

### Paper A — *current preprint, surgical pass only*

- Title (unchanged): *A Two-Sided Bayes-Error Bracket from
  Partition-Conditional Entropy*.
- Scope (unchanged): binary, finite, three applications, $H_2$.
- Add: formalism fixes F1–F5; small Proposition X2 (refinement
  consistency); one experiment E-K (falsification/verification
  protocol applied to existing data); one forward-reference to
  Paper B in §10.
- Target: TMLR.
- Effort: small (1 focused pass).

### Paper B — *new, the framework paper*

- Working title: *Partition Brackets: A Framework with Entropy,
  Variance, and Noise-Robust Instances*.
- Thesis: the partition is the universal expressivity bottleneck;
  the bracket is a *recipe* with multiple instantiations and
  robustness properties.
- Anchor theorem: T3 ($\phi$-bracket meta-theorem) + T4 (noise
  correction) + T8 (soft partitions) + T7-reformulated (regression).
- Worked example: T9-corrected Lemma 6′ replaced by a clean
  aggregator-typed family of bounds; quantized NN as the
  partition-as-bottleneck demonstration (G3-trimmed).
- Target: COLT (stretch: ITCS); fallback TMLR long.
- Effort: medium (months).

### Paper C — *the $k$-WL / HDX paper, already planned*

- See `06-kwl-bracket-paper-roadmap.md` (this doc unchanged).
- Begins after Paper B submission.

**Why three papers, not one bloated paper:** Paper A's thesis is
"elementary closed-form bracket on Bayes error"; Paper B's thesis
is "framework of brackets with robustness"; Paper C's thesis is
"quantitative $k$-WL hierarchy diagnostic." These are three
different theses with three different audiences (ML practitioners
/ TCS-flavoured ML theorists / pure TCS). Bundling them dilutes
all three.

**Why not extend Paper A and skip Paper B:** Paper B's theory
(noise correction, soft partitions, meta-theorem with proofs)
is at least one chapter of work, breaks Paper A's elementary
narrative, and would land Paper A on a venue Paper A is not
optimised for. Better to ship A, then ship B.

---

## Part 3 — Phased plan with gates

### Phase 0 — Strategy lock (now)

- Output: this document.
- Gate: user sign-off on three-paper structure.

### Phase 1 — Paper A surgical pass

- F1: split Lemma 6′ Lipschitz by aggregator (sum / mean /
  sym-norm) into three sub-lemmas with corrected $\delta_L$.
- F2: full proof of Lemma 6′ for each aggregator case.
- F3: promote achievable-region characterisation to numbered
  Proposition with explicit interior construction.
- F4: full proof of Prop 7 (population extension), explicit
  arithmetic in the union bound and Cauchy–Schwarz steps.
- F5: one-line statement $H(f\mid\Pi)\le 1$ in §2.
- X2: insert "Bracket consistency under refinement chains"
  Proposition near Prop 4; rewrite E3 narrative around it.
- E-K: implement falsification/verification protocol on
  existing E1+E2+E6 data; one new table.
- §10: add a one-paragraph forward reference to Paper B.
- **Gate G1**: full coherence read-through; no scope creep
  beyond the above.
- Output: `partition-sandwich-preprint/main.tex` v2.

### Phase 2 — Paper B theory development

- **2.1** Resolve T5 (Rand / VI stability):
  - Search literature (Meila 2003, Vinh-Epps-Bailey 2010).
  - Attempt proof via $V(\Pi,\tilde\Pi)$ Lipschitz bound on
    $H(f\mid\cdot)$.
  - If no clean proof in two weeks of focused work, replace
    with a counterexample or drop T5 from Paper B.
- **2.2** Reformulate T7 (regression):
  - State MSE identity cleanly.
  - State Cauchy–Schwarz MAE upper bound cleanly.
  - Investigate matching MAE lower bound (Hotelling 1932 path).
- **2.3** Develop T8 (soft / Markov-kernel partitions) with
  explicit definition of $\varepsilon^\*_K$ and clean re-derivation
  of the bracket; instantiate on attention soft routing.
- **2.4** Polish T3 (meta-theorem) with explicit hypothesis
  list, three named instances (entropy, variance, Pinsker), and
  Jensen-sharp lower bound where applicable.
- **2.5** Repair T9 (Lemma 6′) properly: aggregator-typed
  Lipschitz constants, trust-region certificate, replaces
  Paper A's Lemma 6′ in spirit.
- Output: `paper-b-theory/proofs.md` with all propositions
  fully verified.
- **Gate G2**: at least 3 of {T5, T7, T8, T3-clean, T9-clean}
  must have full proofs. If fewer, Paper B downscopes to a
  short note for TMLR rather than a COLT submission.

### Phase 3 — Paper B experiments (zero population risk)

- **E8** variance bracket vs entropy bracket on all existing
  partitions. ~30 LOC. Reuses Paper A data.
- **E9** label-noise stress test (validate T4). UCI Adult,
  $\eta\in\{0.05,0.10,0.20\}$. ~50 LOC.
- **E10** refinement-pinch under T6 framing. Reuses E3 WL
  funnels with new overlay.
- **E11** quantized NN bracket on MNIST-bin. Single new
  architecture experiment for the partition-as-bottleneck
  claim. ~200 LOC.
- **E-X3** bracket-as-Lyapunov along $k$-means EM and CART
  greedy splitting. ~80 LOC.
- Output: `paper-b-experiments/` with 5 JSON manifests + figures.
- **Gate G3**: at least 4/5 experiments produce a positive result.
  Negative results reported transparently; majority positives
  required for a coherent claim.

### Phase 4 — Paper B writing

- Section budget for 9 pp COLT (12 pp TMLR fallback):
  - §1 Intro (1.0): thesis = framework, not single inequality.
  - §2 Setup (0.5): cite Paper A for binary entropy instance.
  - §3 $\phi$-bracket meta-theorem (1.5).
  - §4 Three instances: entropy, variance, Pinsker (1.0).
  - §5 Robustness: noise (T4), soft (T8), partition stability
    if T5 resolved (2.0).
  - §6 Partition-as-bottleneck principle (1.0), quantized NN.
  - §7 Experiments E8–E11 + X3 (1.5).
  - §8 Discussion + benefits to PT/Kochenderfer (0.5).
- Output: `paper-b/main.tex`.
- **Gate G4**: full read-through; coherence with thesis.

### Phase 5 — Paper A submission

- Submit Paper A v2 to TMLR.
- arXiv v2.
- Update preprint README with forward-reference to Paper B.

### Phase 6 — Paper B submission

- Submit Paper B to COLT (or ITCS / TMLR by then).
- arXiv v1.

### Phase 7 — Paper C kickoff

- Execute `06-kwl-bracket-paper-roadmap.md` Step 12 onward.

---

## Risk register

| Risk | Phase | Mitigation |
|---|---|---|
| T5 has no clean proof | 2.1 | Downscope Paper B to short note. |
| Paper B too thin without G3 examples | 2 / 3 | Quantized NN suffices as G3 demonstration; defer MoE/SAE. |
| E11 produces null result (quantized NN bracket pins like ogbn-arxiv) | 3 | Report transparently; reframe as "shows the partition-cardinality-collapse regime is a property of the architecture, not a defect of the bracket." Honest negative is a publishable result. |
| Paper A formalism pass creeps in scope | 1 | Strict G1 gate; F1–F5 + X2 + E-K only, no more. |
| Conflicting reviewer demands across A and B | 5 / 6 | Single corresponding author can pre-empt by ensuring Paper B's intro explicitly explains why it is not Paper A v3. |

---

## Status

- 2026-06-01: plan written; not started.
- Next action upon user sign-off: Phase 1 (Paper A surgical pass),
  starting with F5 (the one-liner), then F3 (low-risk
  promotion), then F4 (full Prop 7 proof), then F1+F2 (Lemma 6′
  rewrite), then X2, then E-K.
- All Phase 1 work happens in `partition-sandwich-preprint/`.
- Phase 2+ work happens in new sibling directories.
