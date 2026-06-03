# SYLLABUS — Operator + Graduate-Student Onboarding to the Partition-Conditional-Entropy-Bracket Programme

> **Audience.** Operator (BSc software engineer, 15 yr industry, no
> prior GNN / IT / Lean / Julia) OR graduate student wanting graded
> structure. The syllabus runs both tracks in lock-step.
>
> **Output state.** Reader can (i) read the abstract of
> [`PAPER-ARXIV.md`](PAPER-ARXIV.md) like a native, (ii) reproduce
> the Cora bracket scatter plot from scratch, (iii) explain *why*
> $w^\* \approx 0.1610$ at $\varepsilon^\* = 1/5$, and (iv) pick up
> an open experimental question and run it.
>
> **Duration.** 6 weeks at ~12 h/week (operator pace) or 4 weeks
> at ~20 h/week (full-time grad student). Self-paced. No deadlines.
>
> **Gating.** Three audit gates: G0 (vocabulary), G1 (theorem 1
> proven & verified), G2 (Cora reproduction + arch-vs-arch duel).

## How to read this syllabus

Each row is one **step** with: (a) what you read, (b) what you do,
(c) what you submit, (d) how you self-grade. The column **track**
indicates whether the step is on-ramp **`O`** (operator critical
path), homework **`H`** (graded PSets), capstone **`C`** (graded
milestones), or theory playground **`J`** (Julia/Pluto, ungraded).

The on-ramp `O` is **mandatory** for both audiences. `H`/`C` are
graded supplements for grad students; `J` is optional for any
reader who wants visual / symbolic depth.

## Colour-code legend (mandatory before skipping anything)

- **`[W]` WHITE / GREY** — mandatory; gate-blocking.
- **`[Y]` YELLOW** — skim once. Two consecutive skips = debt to be
  repaid at the next gate's self-assessment.
- **`[B]` BLUE** — pure rigour polish; skip freely.

---

## Week 0 — Setup (1 day, all tracks)

| # | Track | Step | Submit | Self-grade |
|---|-------|------|--------|------------|
| 0.1 | O,H,C | Clone repo; `conda create -n bracket python=3.11`; `pip install numpy matplotlib scipy pytest torch torch_geometric` | screenshot of `pytest --version` | does the command run? |
| 0.2 | O | Read [`onboarding/README.md`](onboarding/README.md) + [`onboarding/PLAN.md`](onboarding/PLAN.md) top to bottom (~20 min) | one paragraph in `writeup.md` stating which audience you are and your target gate | did you write it? |
| 0.3 | J | Install Julia 1.10; `julia --project=onboarding/julia-theory` then `using Pkg; Pkg.instantiate()` | first cell of NB01 renders | Pluto opens in browser? |
| 0.4 | H,C | Open the HW1 student notebook: `jupyter lab onboarding/projects/psets/hw1/hw1.ipynb` and verify cells 1–5 run green | screenshot of cell 5 | demo cells render? |
| 0.5 | H,C | One-time Modal auth for the GPU lane: `pip install modal && modal token new` | nothing | `~/.modal.toml` exists? |
| 0.6 | J | (optional) One-time Julia env: `cd onboarding/julia-theory && julia --project=. -e 'using Pkg; Pkg.instantiate()'` (~3 min, ~1.5 GB), then `julia --project=. -e 'using Pluto; Pluto.run()'` | NB01 opens in browser | reactive slider on `p` works? |

---

## Week 1 — Unit I: A single coin (Bayes error, binary entropy)

**Goal.** Build vocabulary for the *simplest* case (one biased coin,
no graph) so partitions in Week 2 land softly.

| # | Track | Step | Read | Do | Submit |
|---|-------|------|------|----|--------|
| 1.1 `[W]` | O | Read [`gnn.md`](gnn.md) Ch 1.1–1.3 (Bayes risk, binary classifier) | sketch: a biased coin, $P(Y=1) = p$, optimal predictor $\hat y$ | one-pager |
| 1.2 `[W]` | H | **HW1 Q1** — implement `hbin(p)` in [`hw1/starter/q1_hbin.py`](onboarding/projects/psets/hw1/starter/q1_hbin.py) | pytest pass | code + writeup §Q1 |
| 1.3 `[W]` | H | **HW1 Q2** — implement `bayes_error(p)` | pytest pass | code + writeup §Q2 |
| 1.4 `[Y]` | H | **HW1 Q3** — Hellman–Raviv verifier on a 100-point grid | pytest pass | code + plot |
| 1.5 `[W]` | H | **HW1 Q4** — mutate-fail-revert drill (break hbin by removing `1-p` term, see one test fail, revert) | nothing | writeup §Q4 ≤1 paragraph |
| 1.6 `[Y]` | J | **NB01** — open [`julia-theory/notebooks/01_binary_entropy.jl`](onboarding/julia-theory/notebooks/01_binary_entropy.jl), play with the slider; symbolic-differentiate $H_\text{bin}$; change log base 2→e→3→10 | screenshot of `H'_bin` plot | Pluto cell green? |
| 1.7 `[W]` | O,H | **HW1 calibration table** with mis-cal penalty 2× | `writeup.md` §Calibration | follow rubric |

**Gate G0 (Vocabulary) — self-assessment (10 Q in [`onboarding/PLAN.md`](onboarding/PLAN.md) §G0).** Must score 8/10 to advance.

---

## Week 2 — Unit II: Partitions and conditional entropy

**Goal.** Lift Week 1's single coin to a *partition* of nodes; meet
1-WL and the canonical $(C_6, 2K_3)$ blind spot.

| # | Track | Step | Read | Do | Submit |
|---|-------|------|------|----|--------|
| 2.1 `[W]` | O | [`gnn.md`](gnn.md) Ch 1.4–1.6 + Ch 2.1 (partition, $q_C$, $e_C$, $\varepsilon(\Pi)$, $H(Y\mid\Pi)$) | one-pager defining each symbol in your own words | one-pager |
| 2.2 `[W]` | H | **HW2 Q1** — hand-compute $H(Y\mid\Pi)$ on 6-node toy; cross-check via [`hw2/starter/q1_hand_check.py`](onboarding/projects/psets/hw2/starter/q1_hand_check.py) | match to 1e-12 | writeup §Q1 |
| 2.3 `[W]` | H | **HW2 Q2** — implement `cond_entropy(partition, labels)` | pytest pass | code |
| 2.4 `[W]` | H | **HW2 Q3** — hand-trace 1-WL on $C_5$, $C_6$, $2K_3$ (3 rounds each) | colour assignments | writeup §Q3 |
| 2.5 `[W]` | H | **HW2 Q4** — implement `wl_step`; verify $(C_6, 2K_3)$ produce identical stable-colour multisets | pytest pass | code + plot |
| 2.6 `[Y]` | J | **NB02** — `cond_entropy` as a reactive Pluto cell (slider over cell mass + per-cell error) | screenshot | works? |
| 2.7 `[Y]` | C | **M1** — start [`capstone/milestone1/`](onboarding/projects/capstone/milestone1/): implement `Partition.__post_init__`, `label_partition`, `wl_refine`, `wl_partition(L)` | 6 PyG-dependent tests pass | code |
| 2.8 `[W]` | O,H | **HW2 calibration** | writeup §Cal | rubric |

**Re-plan checkpoint.** After Week 2: did anything in Unit I feel
under-built? Edit the syllabus (this file) as an iteration entry,
not silently.

---

## Week 3 — Unit III: The bracket (Theorem 1)

**Goal.** The headline. Implement Theorem 1 from scratch, prove
$w^\* \approx 0.1610$ both numerically and symbolically.

| # | Track | Step | Read | Do | Submit |
|---|-------|------|------|----|--------|
| 3.1 `[W]` | O | [`PAPER-ARXIV.md`](PAPER-ARXIV.md) §3 Theorem 1 statement + Fig caption + the two extremal characterisations (e=0/1/2 for upper; e=const for lower) | annotate the printout; flag every undefined symbol | annotated PDF |
| 3.2 `[W]` | H | **HW3 Q1** — implement `hbin_inverse` via bisection | pytest pass | code |
| 3.3 `[W]` | H | **HW3 Q2** — `upper`, `lower`, envelope plot to `plots/q2_bracket_envelope.png` | plot saved | code + plot |
| 3.4 `[W]` | H | **HW3 Q3** — random-sample verifier on 2000 synthetic profiles | all pass `lower ≤ ε ≤ upper` | code |
| 3.5 `[W]` | H | **HW3 Q4** — grid-search $w^\*, \varepsilon^\*$; verify $w^\* \in (0.160, 0.162)$, $\varepsilon^\* \in (0.199, 0.201)$ | numbers | writeup §Q4 |
| 3.6 `[Y]` | H | **HW3 Q4.3** — false-lead drill: explain why $\varepsilon^\* \neq \arg\max H_\text{bin}$ | one paragraph | writeup §Q4.3 |
| 3.7 `[Y]` | C | **M2** — read [`capstone/milestone2/bracket.py`](onboarding/projects/capstone/milestone2/bracket.py); explain `hbin_inverse` + each unit test in your own words; apply `bracket_of()` to your M1 partitions on Cora | table of (eps, H, lo, hi, slack) per partition | writeup |
| 3.8 `[Y]` | J | **NB05** — interactive bracket envelope with `IntervalArithmetic` (safe `Hbin_inverse`) | Pluto running | screenshot |
| 3.9 `[Y]` | J | **NB06** — closed-form derivation of $w^\*$ with `Symbolics.jl` (set $H'_\text{bin}(\varepsilon)/2 = 1$, solve); cross-check with `Optim.brent`; cross-check derivative with `Enzyme` | symbolic + numeric agree to 1e-9 | screenshot |
| 3.10 `[W]` | O,H | **HW3 calibration** | writeup §Cal | rubric |

**Gate G1 (Theorem 1 understood) — self-assessment (10 Q in [`onboarding/PLAN.md`](onboarding/PLAN.md) §G1).** Must score 8/10. The G1 questions ask: state Theorem 1 verbatim; produce a 1-line numerical example; identify which side fails when $e_C$ are constant; locate $w^\*, \varepsilon^\*$ to 3 decimals.

---

## Week 4 — Unit IV: Why no aggregator can save you

**Goal.** Connect Theorem 1 to architecture choice. Show that no
sum/mean/max aggregator with node-local features can separate the
1-WL blind-spot pair, and that the bracket *quantifies* the gap.

| # | Track | Step | Read | Do | Submit |
|---|-------|------|------|----|--------|
| 4.1 `[W]` | O | [`PAPER-ARXIV.md`](PAPER-ARXIV.md) §4 (the 'no MPNN exceeds 1-WL' restatement) + Cor 3.3 (architecture corollary) | one-pager paraphrasing the corollary | one-pager |
| 4.2 `[W]` | H | **HW4 Q1** — implement `sum_partition`, `mean_partition`, `max_partition` | pytest pass | code |
| 4.3 `[W]` | H | **HW4 Q2** — verify constant features collapse all three aggregators on both $C_6$ and $2K_3$ to a single cell | pytest pass | code + writeup §Q2.2 |
| 4.4 `[W]` | H | **HW4 Q3** — verify degree features still collapse | pytest pass | code + writeup §Q3.2 |
| 4.5 `[W]` | H | **HW4 Q4** — implement `triangle_counts`; verify $C_6$ gets 0s, $2K_3$ gets 1s (global separator) | pytest pass | code |
| 4.6 `[Y]` | J | **NB07** — `arch_duel.jl`: plot bracket slack vs achieved error for GCN/GIN/GAT on a synthetic 6-node graph | Pluto running | screenshot |
| 4.7 `[W]` | O,H | **HW4 calibration + Distinguish drill** ('aggregator-induced' vs '1-WL' blind spot) | writeup | rubric |

---

## Week 5 — Unit V: End-to-end on Cora

**Goal.** Reproduce a real result. Cora is small enough to fit a
laptop, large enough to be non-trivial.

| # | Track | Step | Read | Do | Submit |
|---|-------|------|------|----|--------|
| 5.1 `[W]` | O | [`PAPER-ARXIV.md`](PAPER-ARXIV.md) §5 (experiments) + [`partition-sandwich-preprint/experiments/REPORTS.md`](partition-sandwich-preprint/experiments/REPORTS.md) for E3 | annotated | annotated PDF |
| 5.2 `[W]` | C | **M3** — `train.py` (2-layer GCN on Cora reaching ≥75% test accuracy) | log | writeup |
| 5.3 `[W]` | C | **M3** — `audit.py` (bracket-vs-realised-error scatter; one dot per partition depth) → `plots/m3_scatter.png` | plot | writeup |
| 5.4 `[Y]` | C | **M3 tests** — 6 pytest sanity checks (model has correct shape, bracket holds on trained labels, scatter saved) | pytest pass | code |
| 5.5 `[Y]` | J | **NB08 + NB09 + NB10** — Cora visualisations: degree histogram, label confusion, partition-depth animation | Pluto running | screenshot |

---

## Week 6 — Unit VI: Pick a question, run it

**Goal.** Operator graduates to *contributor*. Pick one open
question from [`future-work/`](future-work/), design a duel
experiment, defend it.

| # | Track | Step | Do | Submit |
|---|-------|------|----|--------|
| 6.1 `[W]` | C | **M4** — `nas.py` arch menu (6 GNN variants); compute bracket + realised error; rank by Kendall-τ | code + table |
| 6.2 `[Y]` | C | **M4 test** — verify τ ≥ 0.3 on the 6-arch menu | pytest pass | code |
| 6.3 `[W]` | C | **M5** — `REPORT_TEMPLATE.md`: 10-section report on a chosen open question (suggested: 'does the bracket predict overfitting?' or 'how does the bracket behave on heterophilic graphs?') | report | rubric |
| 6.4 `[W]` | C | **Capstone end-to-end test** — `pytest capstone/tests/test_end_to_end.py` (synthetic graph, M1→M2→M3 pipeline) | pytest pass | code |
| 6.5 `[Y]` | J | **NB11 + NB12** — sequel previews ($k$-WL bracket, HDX trickle-down) | optional | screenshot |
| 6.6 `[W]` | O,C | **Calibration retrospective** — review every LOW/UNVERIFIED claim across all weeks; promote or demote | calibration table | rubric |

**Gate G2 (Reproduce + duel) — self-assessment (10 Q in [`onboarding/PLAN.md`](onboarding/PLAN.md) §G2).** Must score 8/10. The G2 questions ask: name the 4 highest-slack partitions on Cora and explain why; produce one architecture-vs-architecture comparison with a falsifiable prediction; list 3 open questions the bracket cannot answer.

---

## Rubric — total assessment

| Component | Track | Weight |
|---|---|---|
| HW1–HW4 PSets | H | 40% (10% each) |
| Capstone M1–M5 | C | 50% (10% each) |
| Calibration discipline (mis-cal penalty 2×) | O,H,C | 10% folded into above |
| Julia notebooks | J | 0% — ungraded enrichment |
| Gate self-assessments | O | hard gates, not scored |

All grading uses the **60% Correctness / 25% Pedagogy / 15% Calibration**
split (see each PSet's README). Pedagogy points reward *clear writeup,
explicit Distinguish/False-lead drills, and worked-out adversarial
counter-claims*, not pretty prose.

## Distinguish — what this syllabus is NOT

- **Not** a textbook on graph theory. We assume comfort with
  adjacency matrices and basic graph algorithms.
- **Not** a deep-learning course. We use PyTorch Geometric as a
  loader; we do not study optimisation theory.
- **Not** a Lean / formal-methods course. Lean exposure is
  optional and lives in [`partition-sandwich-preprint/formal/`](partition-sandwich-preprint/formal/).
- **Not** a paper-writing course. We write *reports*, not papers.

## False leads to avoid

1. **"I'll read the whole paper first, then do the PSets."** No.
   The paper assumes vocabulary the PSets teach. Read §1 + §3
   Theorem 1 statement; do HW1+HW2; then return to §3 proof.
2. **"Julia is the One True Path."** No. Python+PyG dominate the
   ecosystem. Julia notebooks are a *visualisation playground*,
   not a production target.
3. **"I'll just train more / on more data."** No. The bracket is
   an *information-theoretic* statement: more data doesn't change
   $\varepsilon^\*_\Pi$. The lesson is to change $\Pi$ (= the
   architecture), not the optimiser.
4. **"I'll skip calibration; the math is clean enough."** No.
   Every gate scores calibration with 2× mis-cal penalty.

## Mantras (post on the wall)

> Implement vigorously, concurrently; review constructively,
> audit adversarially; let no stone unturned; document
> progressively; commit at each gate, milestone, or feature.

> Do first, name later. Theory only enters when an experiment, a
> plot, or an intuition literally fails without it.

> The bracket is not an inequality — it is a *quantitative budget*
> on architecture disagreement, $w^\* \approx 0.1610$ at worst.

---

## Iteration log

- **r2.1** (2026-06-29) — Paper-A coverage audit + remediation. The
  Phase-D notebook scaffolds passed unit-tests and executed end-to-
  end, but a coverage review identified seven gaps between the
  scaffolds and *deep mastery of Paper A*: Lemma 3.1 (binary-entropy
  minimality) was uncited, Xu/Morris provenance for the C₆-vs-2K₃
  blind spot was absent, the HR-vs-Fano endpoint naming was
  implicit, Prop 3.5 sharpness witnesses were missing, Appendix A
  had no step-by-step audit, the aggregator inflation $r_T$ was
  named without computation, the M1 gate only checked cell-count
  monotonicity (not the real Prop 3.2 entropy/ε* monotonicity), and
  M3/M4/M5 did not name the E04 experiment, Cor 3.4, Def 3.5, or
  the open conjectures C1+C1′. r2.1 closes all seven by editing the
  existing scaffolds in place (HW1 prelude, HW2 Q2.5+Q4.5, HW3
  HR/Fano rename + Q4.5 sharpness, HW3 new `proof_walk.ipynb` for
  Appendix A.1–A.7, HW4 Q5 with `r_T`, M1 gate replaced with real
  Prop 3.2 check on Cora, M3/M4/M5 intros now name E04/Cor 3.4/Def
  3.5/C1+C1′). The Julia track is integrated **by cross-reference,
  not duplication**: every Python HW intro now points to its
  Pluto-reactive companion in `julia-theory/notebooks/`. Pytest
  baseline preserved (47 passed, 1 xfailed). Optional Julia env
  setup added as Week 0.6.
- **r2** (2026-06-03) — ratified the tutorial-first notebook doctrine
  ([`projects/REDESIGN-r2.md`](projects/REDESIGN-r2.md)). HWs and
  capstones are now driven from `.ipynb` files generated by
  `scaffold/*.py`; the underlying `psets/hwN/starter/*.py` paths
  below are still valid (the notebook embeds them and the test
  suite imports them). M3 + M4 now mandate a real Modal T4 GPU
  invocation from inside the notebook (Week 5–Week 6). Add
  `pip install modal && modal token new` to Week 0.
  Grading: `GRADE=1 pytest psets/hwN` (the default scope hides
  student-facing tests; see [`projects/conftest.py`](projects/conftest.py)).
- **r1** (2026-06-02) — initial dictation while D2 onboarding work
  was in flight (HW1+HW2+HW3+HW4+M1+M2 fleshed; M3+M4+M5 and
  NB02–NB12 pending). Sources: [`onboarding/PLAN.md`](onboarding/PLAN.md) r4,
  [`onboarding/DEVELOPMENT-PLAN.md`](onboarding/DEVELOPMENT-PLAN.md) r1,
  [`PAPER-ARXIV.md`](PAPER-ARXIV.md) §§1–5.
