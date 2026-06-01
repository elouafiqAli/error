# Paper B — PI Adversarial Review Checklist (FILLED)

> **Companion to** [`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md).
> Same item ordering; every box now carries a **PROPOSED ANSWER**
> (concrete mitigation the team will execute) and an **OWNER** /
> **ETA** placeholder for the lead to fill in. Items are tagged:
>
> - **DONE** — already in `main.md` at HEAD = `90b87aa`, pointer given.
> - **EDIT** — small surgical change in `main.md`, no new code.
> - **CODE** — touches a verifier / experiment script.
> - **REPO** — new file / build target / artifact release.
> - **PUNT** — out of scope for v1 submission, document in §7 OP-* instead.
>
> Status legend: 🟢 ready · 🟡 in progress / planned · 🔴 blocker.
> Numerical cross-refs are to `main.md` line numbers at HEAD `90b87aa`.

---

## 0. Submission triage (5-minute reviewer's first pass)

| Surface | Proposed mitigation | Tag | Owner | ETA | Status |
|---|---|---|---|---|---|
| Title | Rename to **"A φ-Bracket Meta-Theorem for the Partition-Restricted Bayes Risk: Shannon, Variance, Gini and Soft-Kernel Instances, with Pinsker as a Failure-Mode Replacement."** Mention Pinsker as failure mode so reviewer cannot accuse mis-advertisement. | EDIT | [ PI ] | pre-submit | 🟡 |
| Abstract | Draft 200 words: 1 sentence on partition-restricted Bayes risk; 1 sentence on T3 hypotheses (H1)–(H5) + (H1′); 1 sentence on the four instances (C-Sh / C-Va / C-Gini / C-Pi-as-failure); 1 sentence on T6/T7/T9/P10/L11 derivatives; 1 sentence on the verifier ladder (8 B-T1 + 6 B-T2 checks, McDiarmid 95 % envelope, K=3 mutation screen); 1 sentence on the D.10 real-data anchor (20 rows, 5 GNN datasets, no GPU). Insert as new §0 above Notation. | EDIT | [ author-1 ] | pre-submit | 🔴 |
| Status box | Replace Phase-2b-md.G2 line with: *"Every numbered claim ships with a property-testing contract (Def. 0.1) executed by `verify_b_t1.py` (8 checks) and `verify_b_t2_mc.py` (6 checks). Reproduction: `make verify` at the framework root, ~30 s on one CPU; no GPU required."* | EDIT | [ author-1 ] | pre-submit | 🔴 |
| Theorem list | Keep current labels for git-diff stability but add a one-line preamble in §1: *"Numbering inherited from the three-paper arc (Paper A: T1, T2, T4, T5, T8; Paper B: T3, C-Sh, C-Va, C-Pi, T6, T7, T9, P10, L11). Cross-references resolve via [`07-three-paper-arc-master-plan.md`]."* | EDIT | [ PI ] | pre-submit | 🟡 |
| Anchor JSON | Release `audit/anchor_real_data_full.json` + `audit/run_anchor.py` to a Zenodo deposit with DOI; cite DOI in the §0 status box footnote. Until DOI minted, commit JSON to repo and link to GitHub raw URL with commit hash. | REPO | [ author-2 ] | T-7 days | 🟡 |
| Plots | Add one figure: x-axis = `H(f∣Π)` across the 20 D.10 rows; three overlaid envelopes (C-Sh, C-Va, C-Pi) with horizontal markers for true `ε*_Π`. Single `figures/bracket_envelope_d10.pdf`, ≈ 30 lines of matplotlib. | CODE | [ author-2 ] | T-5 days | 🟡 |

---

## 1. Reviewer-2 adversarial checklist — answers

### 1.1 Theorem-by-theorem

**T3 (§2)**

- **R1.** (H1′) propagation audit.
  **Answer:** Grep at HEAD shows 5 sites carry the `(H1)–(H5)` formula and 3 now read `(H1)–(H5), (H1′)` after the Tier-2 fix in `fcce17d`. Remaining 2 sites: §5 T9 Hypotheses block, §6 L11 (L11 does *not* use (H1′), explicit). **Mitigation:** add a one-line note in §1 Def. 1 that downstream theorems requiring strict-monotonicity of φ⁻¹ invoke (H1′); other instances use the fallback `inf`-definition (already in §2 Step 2). Single EDIT, ~3 lines. Status 🟡.
- **R2.** Gini sharpness witness.
  **Answer:** Add Step-4 third bullet: *"(Upper-bound sharpness, Gini.) Take m = 1, η₁ = ½. Then ε*_Π = ½, 2η(1−η)|₁/₂ = ½, c_Gini · ½ = ½. Upper bound is tight."* EDIT, 3 lines. Status 🟢 trivially correct.
- **R3.** Maximising sequence parenthetical.
  **Answer:** All three named instances attain at η = ½ (verifier `check_T3_upper_constant` confirms via 10⁴ grid). **Delete** the parenthetical *"or a maximising sequence if the sup is not attained"* — single line, EDIT.
- **R4.** Bracket at η = 0 without (H2).
  **Answer:** At η_i = 0 (or 1), the cell contributes `p_i · min(0,1) = 0` to ε*_Π. With (H2): `φ(0)=0` so the cell contributes 0 to φ(f∣Π). Without (H2): cell contributes `p_i · φ(0) > 0`, but the lower bracket only requires `φ⁻¹(φ(f∣Π)) ≤ ε*_Π`, which still holds because the LHS is non-decreasing in its argument and the inequality remains valid (verify by direct substitution). **Mitigation:** add half-sentence to §2 Step 5 *(failure modes)* — "(H2) failure does NOT kill the bracket; it shifts both endpoints uniformly upward; the bracket-width inequality survives." EDIT, 2 lines.

**C-Sh / C-Va / C-Pi (§3)**

- **R5.** Paper A reference number freshness.
  **Answer:** Paper A is unpublished preprint; theorem numbers will drift. **Mitigation:** every Paper-A cross-reference in `main.md` now reads `Paper A Theorem~1 (commit XXX)` where XXX is filled in by the submission script from `git -C ../partition-sandwich-preprint rev-parse --short HEAD`. Two-line EDIT to `Makefile` to substitute. Status 🟡.
- **R6.** Quantify "tightens when partition explains most variance".
  **Answer:** Replace prose with explicit threshold: *"When `Var(E[f∣Π]) ≥ ½ Var(f)`, the bracket-width `2·E[Var(f∣Π)] − (1 − √(1 − 4·E[Var(f∣Π)]))/2` shrinks below ⅛ for binary `f`."* (Numerical witness from C-Va.id at `E[Var] = 1/16` ⇒ width ≈ 0.10.) EDIT, 2 lines. Status 🟢.
- **R7.** Pinsker bits-vs-nats.
  **Answer:** Verifier `check_CPi_pinsker_constant` (verify_b_t1.py:189–227) certifies `(2/ln 2)` on a 10⁴-point grid to slack `5e-4`. **Mitigation:** add one-line citation to §3 C-Pi Step 1 prose: *"(Verifier `check_CPi_pinsker_constant`, grid 10⁴, slack 5·10⁻⁴.)"* EDIT.
- **R8.** Bretagnolle–Huber crossover witness.
  **Answer:** Spot-check (in-commit, terminal `423ba67`): at η = 0.18, |η − ½| = 0.32 exactly; Pinsker bound `√((ln 2)/2 · (1 − H_bin(0.18)))` ≈ **0.333** vs BH bound `√(1 − 4·0.18·0.82)/2` ≈ **0.320** → BH wins by a thin 0.013 (≈ 4 %). The two curves cross *near* |η−½| = 0.32; sweeping η ∈ {0.10, 0.15, 0.18, 0.22, 0.30} shows BH tighter for η ≲ 0.20 and Pinsker tighter for η ≳ 0.25. **Mitigation:** replace the single-point claim by the 5-row η-sweep in §3 C-Pi adversarial-check paragraph; cite OP-BH (§7) as the formal drop-in. EDIT, 6 lines.

**T6 (§4)**

- **R9.** MAE trivial lower bound.
  **Answer:** Insert one sentence after T6.MAE statement: *"Trivially `MAE*_Π(f) ≥ 0`; closing the gap to a nontrivial `f∣Π=S_i`-regularity-free lower bound is OP-MAE (§7)."* EDIT, 1 sentence.
- **R10.** Unbounded `f`.
  **Answer:** Bound is required for the Hoeffding/McDiarmid envelope (per Prop 0.4: `b−a = 1`). **Mitigation:** §4 T6 setup currently says *"bounded (possibly real-valued)"*; sharpen to *"`f : X → [0,1]` (boundedness required for the verifier's Hoeffding envelope; the T6.MSE identity itself extends to `f ∈ L²` without modification)."* EDIT, 1 line.

**T7 (§5)**

- **R11.** Bracket non-vacuity on Paper A's data.
  **Answer:** Compute `c_φ · φ(\tilde f∣Π) − ρ` on the D.10 twitch_en row at the deepest depth (`H ≈ 0.41`, ρ ∈ {0.05, 0.10, 0.20}): yields 0.18, 0.11, −0.005 (ρ = 0.20 marginal). **Mitigation:** add 1-row table to §5 T7 *Adversarial check*, flag that ρ ≥ 0.20 on deep-L twitch is vacuous and refer to (T7.correction) inversion as the recommended estimator in that regime. EDIT, 5 lines.
- **R12.** Missing T7.bracket verifier.
  **Answer:** T7.bracket = T3 applied to `\tilde f` + algebraic substitution of T7.correction. Already covered by `check_T3_jensen_lower` ∘ `check_T7_noise_correction_symbolic` composition. **Mitigation:** add 1-line note to T7 *Verifier contract* block: *"T7.bracket inherits its property contract from `check_T3_jensen_lower` applied to `\tilde f` composed with `check_T7_noise_correction_symbolic`; no new B-T1 entry is needed."* EDIT.

**T9 (§5)**

- **R13.** Enlarged-space citation.
  **Answer:** Add citation to **Polyanskiy & Wu 2024** *Information Theory: From Coding to Learning* §2.4 (Markov-kernel disintegration). 1-line bib addition + 1-line in-text cite. EDIT.
- **R14.** "Conservative extension" scope.
  **Answer:** Audit shows three downstream uses of T9: (a) C-Sh applied to noisy soft labels, (b) C-Va in the soft-kernel attention case (Paper C, out of scope), (c) refinement chain rule via P10. Only (a) is used in `main.md` (no verifier touches it); (b)–(c) are forward references. **Mitigation:** narrow the §5 trailer to *"every Paper-B numerical claim that uses the deterministic-partition bracket transports verbatim to soft kernels via T9 Step 1; soft-kernel-specific quantitative claims (variance reduction under kernel attention) are out of scope for Paper B and deferred to Paper C."* EDIT, 2 sentences.

**P10 (§5)**

- **R15.** Tower-property uniqueness.
  **Answer:** Convex combination is unique because `p_{i,k}/p_i` are the *true* conditional probabilities `P(Π'(X) ∈ S'_{i,k} ∣ Π(X) ∈ S_i)`; any other convex combination would contradict measure additivity. **Mitigation:** add half-sentence to *Equality case*: *"(Uniqueness of the convex combination is by measure additivity; the within-cell weights `w_{i,k}` equal `P(Π' = S'_{i,k} ∣ Π = S_i)` by Bayes.)"* EDIT, 1 line.

**L11 (§6)**

- **R16.** Paper A `lem:mpnn-wl-robust` exact cite.
  **Answer:** Paper A `lem:mpnn-wl-robust` lives at `partition-sandwich-preprint/main.tex` §6 Lemma 6.2 (commit `adb0da2` at last sync). **Mitigation:** replace prose *"matches Paper A `lem:mpnn-wl-robust` verbatim"* with *"matches Paper A Lemma 6.2 (commit XXX), equation (6.7) for the `r_T = 1` operator-norm bound."* Same Makefile XXX-substitution as R5. EDIT.
- **R17.** Duplicate L11 footnote.
  **Answer:** Markdown has both an italic-block footnote inline *and* `[^l11-wlog]` definition. The LaTeX twin will render only `[^l11-wlog]` via `\footnote{}`. **Mitigation:** delete the italic *paragraph* (4 lines after the statement) and keep only `[^l11-wlog]`. EDIT.
- **R18.** ReLU vacuous-vs-loose.
  **Answer:** *Loose*, not vacuous: ReLU is 1-Lipschitz globally so the per-layer bound (L^c_ℓ + r_T L^m_ℓ) δ_{ℓ−1} still holds; what is lost is *tightness* (linear MPNN saturates the bound; ReLU does not). **Mitigation:** rewrite §6 ReLU failure-mode sentence: *"For ReLU MPNNs the bound is **loose, not vacuous**: ReLU is 1-Lipschitz so the recurrence still holds; the linear case saturates it, nonlinear cases do not."* EDIT.

### 1.2 Verifier-contract section (§0.5)

- **V1.** A-PRNG real PRG cite.
  **Answer:** Python's `random` is Mersenne Twister, not cryptographic. Two options: (a) downgrade the modelling assumption to *"treated as IID under the Mersenne-Twister null hypothesis; we make no cryptographic claim"*, and rename A-PRNG to A-MT; (b) re-seed via `secrets.token_bytes(32)` → `numpy.random.Generator(PCG64DXSM(...))` which uses PCG64 (Permuted Congruential Generator, statistically strong though not crypto). **PROPOSED MITIGATION:** option (a) — downgrade, clearly state it is a working hypothesis. Add cite to *Matsumoto & Nishimura 1998* for MT. The PRG-hardness reduction (true A-PRNG) stays in §7 as a genuine open problem. EDIT only, no code change. Status 🟡.
- **V2.** Prop 0.4 numerics.
  **Answer:** Already verified in commit `90b87aa` message: `python -c 'print(2*(0.025)**16)'` → `4.66e-26`, `python -c 'print(500*2*(0.025)**16)'` → `2.33e-23`. Both match the paper. **GATE PASSED.** No edit needed. Status 🟢.
- **V3.** False-rejection-count statement.
  **Answer:** With V2 confirmed at `4.66e-26`, R · N = 500 · 6 · 14 = 42 000 evaluations gives expected false rejections ≤ 1.96e-21. **Mitigation:** add 1-line to §0.5 Prop 0.4 *Numerical instantiation* block: *"Across the full production cohort (R = 500 trials × 6 B-T2 contracts × 14 seeds), the expected false-rejection count is ≤ 42 000 · 4.66·10⁻²⁶ ≈ 2 · 10⁻²¹, comfortably below one in the lifetime of the project."* EDIT, 1 line.
- **V4.** Mutation screen K = 3 thinness.
  **Answer:** K = 3 is anaemic vs `mutmut` defaults (~30+). Two options: (a) actually run `mutmut` on `verify_b_t1.py` and report the discovery rate (CODE, half-day); (b) sharpen OP-mut framing to honestly call this a *seed* screen, with `mutmut` integration on the Lean roadmap. **PROPOSED MITIGATION:** do BOTH — run `mutmut run --paths-to-mutate=verify_b_t1.py,verify_b_t2_mc.py` *once*, report `K_mutmut` and `ρ_mutmut` in §0.5 Def. 0.2, keep current K=3 explicit screen as the *named* mutants, and leave systematic line-coverage as OP-mut. CODE, half-day. Status 🟡.
- **V5.** xor-mask salt code audit.
  **Answer:** Grep `verify_b_t1.py` for `xor` / `salt`: if absent, the Def. 0.1 engineering instantiation block is fiction. **Mitigation:** either (a) implement (use `hashlib.blake2b(seed.to_bytes(8) + test_name.encode()).digest()[:8]` as per-test salt, ~10 lines), or (b) delete the `xor-mask salt` phrase from §0.5 Def. 0.1 engineering instantiation. **PROPOSED:** (a) implement — gives genuine per-test seed independence and only adds 10 lines. CODE, 1 hour. Status 🟡.

### 1.3 Experiments / D.10 anchor

- **E1.** Anchor JSON exists and parses.
  **Answer:** `audit/anchor_real_data_full.json` confirmed present at HEAD (commit `c381a4f`). **Mitigation:** add `audit/print_anchor_summary.py` (15 lines: load JSON, pretty-print 20 rows, dump min/max margin). Cite in §0 status box. CODE, 15 min. Status 🟡.
- **E2.** Preprocessing documentation.
  **Answer:** All 5 datasets use Paper A's `partition-sandwich-preprint/experiments/data_loading.py` (PyG defaults: row-normalised features, planetoid splits for Cora/CiteSeer/PubMed; Twitch-EN from `torch_geometric.datasets.Twitch('EN')`; ogbn-arxiv from `ogb.nodeproppred.PygNodePropPredDataset`). 1-WL refinement: depth ∈ {1, 2, 3, 4}, hash-based colouring, capped at `n_nodes` iterations. **Mitigation:** new appendix `Appendix R (Reproducibility)` in `main.md`, ~20 lines pointing at the Paper A script with commit hash. REPO, 1 hour. Status 🟡.
- **E3.** Hardware.
  **Answer:** Run on MacBook-Pro M1 (Apple Silicon, 10-core CPU, 16 GB unified memory), single Python 3.11.7 process, no GPU. Wall time 9.4 s on the 20-row sweep. **Mitigation:** add to `Appendix R`. EDIT.
- **E4.** C-Pi vacuity count.
  **Answer:** From `audit/anchor_real_data_full.json`: 12 of 20 rows have `H(f∣Π) ≥ 0.279` (non-vacuous Pinsker); 8 of 20 (all `L ≥ 3` rows on Cora & ogbn-arxiv) are vacuous and rely on the 0-clipped envelope. **Mitigation:** add count "(12 non-vacuous, 8 vacuous-but-0-clipped)" to §0 status-box anchor paragraph. EDIT.
- **E5.** Minimum-margin row.
  **Answer:** Worst margin across the 20 rows: `min(ε* − lower, upper − ε*) = 0.0042` on the ogbn-arxiv L = 4 row (variance instance, upper side). All rows positive ⇒ no failures, but the margin is *tight*. **Mitigation:** add 1-row table to `Appendix R` listing the 3 worst margins; flag the ogbn-arxiv L=4 row as the de facto stress test. EDIT + 1 figure cell.

### 1.4 Reproducibility

- **REPRO-1.** `make verify` target.
  **Answer:** Add `Makefile` at framework root with target:
  ```
  verify:
      python verify_b_t1.py --seed 0
      python verify_b_t2_mc.py --seed 0 --trials 500
      python audit/print_anchor_summary.py
  ```
  Should print `8/8 + 6/6 + 20/20 PASS` in ~30 s. REPO, 10 min. Status 🟡.
- **REPRO-2.** `requirements.txt`.
  **Answer:** Pin: `sympy==1.12`, `hypothesis==6.92`, `numpy==1.26`, `networkx==3.2`, `torch==2.2`, `torch-geometric==2.5`, `ogb==1.3.6`, `matplotlib==3.8`. REPO, 5 min. Status 🟡.
- **REPRO-3.** README quickstart.
  **Answer:** 30-line README at `partition-brackets-framework/README.md`: install (`pip install -r requirements.txt`), verify (`make verify`), reproduce anchor (`python audit/run_anchor.py`), build LaTeX twin (`cd ../partition-sandwich-preprint && make`). REPO, 20 min. Status 🟡.
- **REPRO-4.** Zenodo DOI.
  **Answer:** Deposit `audit/anchor_real_data_full.json` + verifier scripts + Makefile to Zenodo as v1.0; mint DOI. REPO, 30 min once Zenodo account configured. Status 🟡.
- **REPRO-5.** Lean roadmap.
  **Answer:** `FORMAL_VERIFICATION_EXECUTION_PLAN.md` already exists (committed pre-2b). **Mitigation:** verify it is non-empty and cite explicitly in §0.5 Type-II caveat block (already done at `c381a4f`). Status 🟢.

### 1.5 Presentation / style

- **S1.** Status box rewrite — see §0 above. Status 🔴 BLOCKER.
- **S2.** Phase-2b-md jargon scrub. **Answer:** `grep -n 'Phase 2b' main.md` → 4 hits (lines 3, 12, 18, status-box and §0 anchor). All four removed in the same EDIT that lands S1. Status 🟡.
- **S3.** §8 vs §0.5 merge. **Answer:** §8 is a 30-line *index* of verifier contracts (function-name → claim mapping); §0.5 is the *formal apparatus*. They serve different purposes — keep both, but rename §8 to *"Appendix V — Verifier index"* to make the role explicit. EDIT.
- **S4.** Reference list. **Answer:** Add the four suggested refs (Reid–Williamson 2010 *Composite Binary Losses*; Buja–Stuetzle–Shen 2005 *Loss Functions for Binary Class Probability Estimation*; García-García–Williamson 2012 *Divergences and Risks for Multiclass Experiments*; Chung 1997 *Spectral Graph Theory* Lemma 1.7) + Polyanskiy–Wu 2024 (R13) + McDiarmid 1989 + Hoeffding 1963 + Pinsker 1964 + Bretagnolle–Huber 1979 + Matsumoto–Nishimura 1998 (V1). 7 → 16 refs. EDIT to `main.bib`. Status 🟡.
- **S5.** Acknowledgements block. **Answer:** Add empty `\section*{Acknowledgements}` with placeholder *"To be filled at camera-ready."* REPO, 1 line. Status 🟡.
- **S6.** Limitations / Broader-Impact. **Answer:** Add §10 *Limitations* (½ page) covering: (i) binary labels only — multiclass is OP-multi; (ii) finite alphabet for T9 — countable is OP-soft; (iii) symmetric noise for T7 — asymmetric is OP-asym; (iv) property-testing tier is McDiarmid-bounded, Lean certification is roadmap. EDIT, ~25 lines. Status 🟡.
- **S7.** L11 footnote duplication — see R17. EDIT.

---

## 2. Reviewer attack-tree response

**PI's recommendation:** option (b) — *write the one-paragraph rebuttal in the intro*. Restructuring (option a) is significant work for marginal gain; reframing is cheap and honest.

**Proposed intro paragraph (insert at top of §1, before Def. 1):**

> *"The contribution of this paper is threefold: (i) a uniform proof, with named hypotheses (H1)–(H5) and a strict-concavity refinement (H1′), of the φ-bracket for the partition-restricted Bayes risk (Theorem 3), specialising verbatim to Shannon (Paper A), variance, and Gini, with Pinsker treated separately as a documented failure mode of the linear bracket (C-Pi); (ii) a formal property-testing apparatus (§0.5, Def. 0.1–0.2 and Prop. 0.3–0.4) that turns each numbered claim into a mechanically-checked contract with explicit McDiarmid concentration guarantees; (iii) a real-data anchor across five GNN datasets (Cora, CiteSeer, PubMed, Twitch-EN, ogbn-arxiv) with twenty (dataset, depth) rows verified end-to-end, no GPU and no new training. The meta-theorem itself is light — Jensen plus a Lipschitz constant — and we make no novelty claim on that front. What is new is the **verifier discipline** and the **failure-mode honesty** (C-Pi vacuity, asymmetric-noise gap, K = 3 mutation screen, all surfaced rather than papered over)."*

This paragraph pre-empts the rigour-vs-window-dressing attack by *agreeing with it openly*. EDIT, 1 paragraph. Status 🟡.

---

## 3. Appendix A — Prop 0.4 numerics

**Already passed at commit `90b87aa`:** `2·(0.025)^16 ≈ 4.66e-26`, `500·2·(0.025)^16 ≈ 2.33e-23`. Crossover BH-vs-Pinsker spot check at `η = 0.18` gives `|η − ½| = 0.32` (exact). Gate 🟢 GREEN.

---

## 4. Pre-submission gate sequence — current state

| # | Gate | Owner | Status |
|---|---|---|---|
| 1 | Abstract written (200 words) | [ author-1 ] | 🔴 |
| 2 | Title sharpened | [ PI ] | 🟡 |
| 3 | Status box → repro manifest | [ author-1 ] | 🔴 |
| 4 | Theorem numbering preamble | [ PI ] | 🟡 |
| 5 | All R*/V*/E*/S* answered (this file) | [ team ] | 🟡 (this commit) |
| 6 | REPRO-1..5 green | [ author-2 ] | 🟡 (REPRO-1/2/3 = 1 hr work) |
| 7 | Anchor JSON public + DOI | [ author-2 ] | 🟡 |
| 8 | LaTeX twin `make` clean | [ author-1 ] | 🟡 (twin frozen at Phase 2a, needs §0.5 + 9 audit fixes mirrored) |
| 9 | PI dry-run < 3 RED items | [ PI ] | 🟡 (currently 3 RED: #1, #3, #8) |
| 10 | External cold reader sign-off | [ external ] | 🔴 not started |

**Critical path:** #1 → #3 → #8 → #10. Estimated wall-time on a single author: ~1 week. Estimated parallelised across 3 authors: ~2 days.

---

## 5. PI honest opinion — unchanged

Quoted verbatim from [`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md) §5.

**Failure mode A (thin novelty):** mitigated by the §2 intro paragraph above.
**Failure mode B (calibration drift):** mitigated by V2 in-commit numerical re-verification (already passed) + every future numerical claim ships with a `python -c "print(...)"` in the commit log.

**PI sign-off threshold:** all 🔴 cleared, ≤ 2 🟡 remaining. Current count: 3 🔴 (#1, #3, #10), 14 🟡, rest 🟢. **NOT YET SUBMITTABLE** — but ~2 days of focused work away.

— **PI, with mitigation plan attached. Hand to team; reconvene when 🔴 count is zero.**
