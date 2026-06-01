# Paper B — PI Adversarial Review Strategy & Team Checklist

> **Target venue.** Transactions on Machine Learning Research (TMLR).
> **Acceptance criterion (TMLR).** *Claims are supported by convincing
> and rigorous evidence*; *significance/interest for some portion of
> the TMLR audience*. **Novelty is explicitly NOT required.**
> **Bonus dimensions.** Reproducibility, clarity, breadth of audience.
> **Reviewer stance below.** I (PI) play Reviewer 2 — adversarial,
> ruthless, no benefit-of-the-doubt. Team must answer every bullet
> *before* I submit anything to OpenReview.

---

## 0. Submission triage (5-minute reviewer's first pass)

A TMLR reviewer reads the title, abstract, status box, theorem
list, and one experiment plot — in that order, in ≤ 5 minutes —
and decides whether to recommend reject-without-deep-read.

| Surface | Current state | Risk | Fix gate |
|---|---|---|---|
| Title | "Partition Brackets: A Framework with Entropy, Variance, and Noise-Robust Instances" | Vague "framework" word — TMLR reviewers downgrade buzz-titles. Test: does it tell a non-expert what is bounded by what? | **Sharpen** to e.g. *"A φ-Bracket Meta-Theorem for the Partition-Restricted Bayes Risk: Shannon, Variance, Gini, Pinsker, and Soft-Kernel Instances"* OR keep but justify in §1 intro. |
| Abstract | (NOT YET WRITTEN in `main.md`) | TMLR mandates a real abstract before submission. Status box ≠ abstract. | **BLOCKER.** Write a 200-word abstract that states (i) the meta-theorem, (ii) the four instances, (iii) the verifier ladder, (iv) the real-data anchor. No marketing adjectives. |
| Status box | Phase-internal language ("Phase 2b-md.G2 CLOSED") | Reviewer doesn't know what G2 is and will read it as project jargon. | **BLOCKER for submission.** Strip Phase 2b-md.G2 language; replace with a one-sentence reproducibility manifest (e.g. "All claims are checked by `verify_b_t1.py` and `verify_b_t2_mc.py`; rerun in ~30 s on one CPU."). |
| Theorem list | T3, C-Sh, C-Va, C-Pi, T6, T7, T9, P10, L11 (9 items, ad-hoc numbering) | Mixed prefixes (T = Theorem, C = Corollary, P = Proposition, L = Lemma) are fine, but the numbering jumps (T3, T6, T7, T9 — where are T1, T2, T4, T5, T8?) will read as *cherry-picked from a bigger plan that was abandoned*. Reviewer suspicion: "what failed?" | **BLOCKER.** Either renumber sequentially (T1–T9) OR add a one-line preamble: "Numbering inherited from Paper A § cross-reference; full list T1–T11 spans Papers A+B as in [`07-three-paper-arc-master-plan.md`]." |
| Real-data anchor | "20 (dataset, depth) rows … zero failures" | Strong, but the JSON is on the local disk and not yet released. | **BLOCKER for reproducibility bonus.** Anchor JSON + dataset list + 1-WL refinement script must be in a public artifact (or zenodo DOI) at submission time, or the bonus disappears and reviewer #3 will ask why. |
| Plots | None in `main.md` (the §3-C-Pi vacuity arithmetic is text-only) | TMLR reviewers want at least *one* figure showing the bracket envelope vs Bayes risk on real data. | **STRONG SUGGESTION.** Borrow the figure from Paper A's D.10 protocol and re-render with all three instances (C-Sh, C-Va, C-Pi) overlaid. |

---

## 1. Reviewer-2 adversarial checklist

For each item: the team must produce a written answer with line refs
into `main.md` and a code/JSON pointer before I sign off. *No item
may be left as "we'll handle it in rebuttal."*

### 1.1 Theorem-by-theorem ruthlessness

**T3 (φ-bracket meta-theorem, §2)**

- [ ] **R1.** "(H1′) strict concavity on (0, ½) was *added during
  audit* as load-bearing. Was it stated in the original draft?
  If not, every downstream theorem that cites Def. 1 must be
  re-checked under the strengthened definition." → Audit grep:
  every `(H1)–(H5)` reference in §3–§6 should now read
  `(H1)–(H5), (H1′)` or use the fallback `inf`-definition of φ⁻¹.
- [ ] **R2.** "Sharpness witness for Gini is missing from §2 Step
  4. C_Gini = 1 is claimed but only Shannon and variance get
  explicit witnesses." → Add a one-line `m=1, η=½` witness for
  Gini.
- [ ] **R3.** "The proof says 'or a maximising sequence if the
  sup is not attained.' Name an instance where the sup is not
  attained and the bracket still holds." → Either delete the
  parenthetical (Shannon, var, Gini all attain) or cite a
  concrete instance.
- [ ] **R4.** "Step 1 reduction via (H4) assumes φ(η_min) is
  well-defined; what if φ(0) ≠ 0 (drop H2)?" → §2 says (H2) is
  used only for the degenerate φ⁻¹(0)=0 case. Verify the
  bracket inequality still holds at η=0 without (H2).

**C-Sh / C-Va / C-Pi (§3)**

- [ ] **R5.** "C-Sh claims 'identical to Paper A's main bracket'
  but Paper A is not in the references list." → Paper A is
  cited in §9 as a companion preprint; verify the section
  number (`Theorem 1`) is the *current* Paper A numbering, not
  a stale arXiv-v1 number. Update with explicit `Theorem N
  (commit XXX)` if Paper A is unpublished.
- [ ] **R6.** "C-Va law-of-total-variance remark says it
  'tightens the upper endpoint when the partition explains most
  of the label variance' — quantify *most*. Without a
  quantitative threshold this is hand-waving." → Either add the
  threshold (`Var(E[f|Π]) > ½ Var(f)`) or delete the remark.
- [ ] **R7.** "C-Pi proof Step 1 cites Pinsker in *bits* but the
  Paper-B convention is `log` base 2 / `ln` natural. Triple-
  check the constant `(2/ln 2)` vs `(1/2)` (nats Pinsker)." →
  Verifier `check_CPi_pinsker_constant` already pins this on a
  10⁴-point grid; cite the verifier in the proof body.
- [ ] **R8.** "C-Pi 'Bretagnolle–Huber is sharper' is now in
  §7 (OP-BH) but the prose still says 'strictly sharper drop-in'
  without giving a single numerical regime where BH beats
  Pinsker." → Add the |η - ½| ≳ 0.32 crossover number from the
  OP-BH §7 entry into the C-Pi prose (or vice versa).

**T6 (regression, §4)**

- [ ] **R9.** "T6.MAE is upper-bound only; TMLR reviewers
  expect a matching lower bound or a *quantitative gap*. OP-MAE
  in §7 is open, but the paper should state the *best known*
  lower bound — even a trivial one — in the §4 prose, not
  hide it in the open-problems list." → Add: "trivially
  `MAE*_Π(f) ≥ 0`; no nontrivial cell-conditional lower bound
  is known without regularity assumptions on `f|Π=S_i`."
- [ ] **R10.** "T6 setup says `f : X → [0,1]`. What about
  `f : X → R` (unbounded)? Does T6.MAE collapse?" → Document
  the boundedness assumption explicitly; cite the Hoeffding
  halfwidth in the verifier as needing the [0,1] range.

**T7 (label noise, §5)**

- [ ] **R11.** "T7.bracket has a `(c_φ · φ(\tilde f|Π) − ρ)/(1 −
  2ρ)` upper. Verify *numerically* that the RHS stays ≥ 0 in
  the regime where Paper A's experiments operate; otherwise the
  bracket is vacuous on real data." → Add a one-row table for
  ρ ∈ {0.05, 0.10, 0.20} on Paper A's twitch_en run showing the
  RHS is positive.
- [ ] **R12.** "Why no T7 verifier for the *bracket* (only the
  correction identity is mechanically checked)?" → Either add a
  contract or document why the bracket version follows
  symbolically from T3 + T7.correction (no new code needed).

**T9 (Markov kernel, §5)**

- [ ] **R13.** "T9 Step 1 'enlarged space' construction is
  textbook; cite Polyanskiy–Wu or Csiszár–Körner to make the
  reviewer comfortable." → Add citation.
- [ ] **R14.** "T9 'conservative extension' claim: does *every*
  Paper-A numerical claim lift to soft kernels, or only the
  bracket endpoint inequalities?" → Audit which downstream
  numerics use which kernel property; document.

**P10 (refinement, §5)** — looks clean, low risk. Spot-checks
only:
- [ ] **R15.** Equality case "η_{i,k} = η_i for every (i,k)"
  needs the tower property `η_i = Σ w_{i,k} η_{i,k}` to be the
  *unique* convex combination. Confirm it is.

**L11 (MPNN, §6)**

- [ ] **R16.** "L11 sym-norm proof was tightened during audit;
  the irregular-graph factor `√(d_v / d_min,v)` can exceed 1
  even when the operator-norm bound `r_T = 1` holds. The text
  papers this over with 'matches Paper A `lem:mpnn-wl-robust`
  verbatim' — cite the *exact* Paper A lemma and equation
  numbers." → Pull from Paper A and update.
- [ ] **R17.** "Footnote on COMBINE-second-arg appears twice
  (italic block + `[^l11-wlog]` footnote). Pick one." → Polish.
- [ ] **R18.** "ReLU failure mode: is the bound *vacuous* or
  just *loose* for ReLU MPNNs? Paper A claims tightness for
  linear MPNNs; clarify what 'vacuous' means in §6 failure
  modes." → Reword.

### 1.2 Verifier-contract section (§0.5)

The §0.5 formal contract apparatus is the strongest part of
the paper and *the* reason to submit to TMLR (rigor). Reviewer
2 will scrutinise it adversarially.

- [ ] **V1.** "A-PRNG modelling assumption says the
  derandomized Hypothesis stream is *computationally
  indistinguishable from IID* — cite the actual cryptographic
  primitive. Hypothesis uses Python's stdlib `random`
  (Mersenne Twister), which is NOT cryptographic." → Either
  cite a real PRG (e.g. ChaCha20) or downgrade the
  idealisation to "treated as IID under standard pseudo-random
  assumptions; this is a working hypothesis, not a theorem."
- [ ] **V2.** "Prop 0.4 numerics: `2(α/2)^16 ≈ 4.6e-26` —
  recompute by hand:
  `2·(0.025)^16 = 2·(2.5e-2)^16 = 2·(2.5)^16 · 10^(-32)
   ≈ 2·2.33e10·1e-32 ≈ 4.66e-22`. **WAIT — that's e-22, not
  e-26.** Recompute carefully." → **VERIFICATION GATE.**
  See Appendix A below; the team must independently recompute
  before the next commit.
- [ ] **V3.** "B-T2 default `--trials = 500` per contract × 6
  contracts × 14 seeds = 42 000 evaluations. With
  `4.6e-26` per evaluation, expected false-rejection count is
  `1.9e-21`. With Reviewer-2's recomputation `4.6e-22` per
  evaluation, the false-rejection count is `1.9e-17`. **Either
  number is small enough**, but the paper must state the
  *correct* one." → Resolve V2 first.
- [ ] **V4.** "Definition 0.2 mutation-screen K=3 is anaemic.
  Production-grade screens use K ≥ 30 (per `mutmut` /
  `cosmic-ray` defaults). Reviewer #3 will ask why." → Either
  expand to K ≥ 10 (achievable in a day) or strengthen the
  OP-mut framing to "future work, principled coverage metric
  on Lean roadmap."
- [ ] **V5.** "Engineering-instantiation block under
  Def. 0.1 says `hypothesis-derandomize=True with xor-mask
  salt`. Is the xor-mask salt actually in `verify_b_t1.py`?
  If not, this is fiction." → Code audit.

### 1.3 Experiment / real-data anchor (D.10)

- [ ] **E1.** "Anchor claim: '20 (dataset, depth) rows … zero
  failures'. Show me the JSON." → Verify
  `audit/anchor_real_data_full.json` exists, parses, and
  has the claimed shape; commit a `print_anchor_summary.py`
  one-liner that the reviewer can run.
- [ ] **E2.** "Datasets: Cora, CiteSeer, PubMed, Twitch-EN,
  ogbn-arxiv — five graphs × 4 depths = 20 rows. Document the
  exact preprocessing (split, feature normalisation, 1-WL
  iteration cap)." → Add a Reproducibility Appendix or cite
  Paper A § (with commit hash).
- [ ] **E3.** "'No GPU, no new training, wall ≈ 10 s' — name
  the machine (CPU model, RAM)." → Add to Appendix.
- [ ] **E4.** "C-Pi is 'genuinely vacuous … for deep-L rows
  where H < 0.279'. Quantify *how many* of the 20 rows are
  vacuous vs non-vacuous." → Add a count to the §0 anchor
  paragraph: "X of 20 rows non-vacuous for C-Pi."
- [ ] **E5.** Negative results: are any rows *close* to bracket
  failure? Reviewer 2 will assume the team cherry-picked
  successful rows. Show the minimum margin
  `min(ε* − lower, upper − ε*)` across the 20 rows.

### 1.4 Reproducibility bonus

TMLR awards a reproducibility badge if the artifact is one-
click runnable. Gates:

- [ ] **REPRO-1.** `make verify` (or equivalent) at the
  `partition-brackets-framework/` root that runs
  `verify_b_t1.py` + `verify_b_t2_mc.py` + the anchor and
  prints `8/8 + 6/6 + 20/20 PASS`. Currently the README does
  not document this.
- [ ] **REPRO-2.** `requirements.txt` pinning SymPy,
  Hypothesis, NumPy, NetworkX, PyTorch-Geometric, OGB
  versions. Verify it exists.
- [ ] **REPRO-3.** A 30-line `README.md` quickstart in the
  framework folder. Verify it exists and matches reality.
- [ ] **REPRO-4.** Public release of the anchor JSON + 1-WL
  scripts. Currently inside repo; for TMLR, mirror to
  Zenodo with a DOI before submission.
- [ ] **REPRO-5.** Lean / Mathlib roadmap document is cited
  (`FORMAL_VERIFICATION_EXECUTION_PLAN.md`) — verify it
  exists and is non-empty.

### 1.5 Presentation / style

- [ ] **S1.** Status box at top: rewrite as TMLR-appropriate
  prose (see §0 above).
- [ ] **S2.** Phase-2b-md jargon: scrub all internal milestone
  language.
- [ ] **S3.** Section §8 ("Verifier contracts — forward
  references") is a repeat of §0.5 content. Consider merging.
- [ ] **S4.** §9 References has 7 entries; for a TMLR paper
  with 9 numbered claims, 7 refs is *thin*. Adjacent literature
  to cite: Reid–Williamson (2010) on proper losses; Buja–
  Stuetzle–Shen (2005) on Bregman divergences;
  Garcia-Garcia–Williamson (2012) on divergence-bracketing.
- [ ] **S5.** No `\section*{Acknowledgements}` block. TMLR
  requires one even if empty.
- [ ] **S6.** No "Broader Impact" or "Limitations" section.
  TMLR doesn't mandate, but Reviewer 3 will ask.
- [ ] **S7.** Footnote in §6 L11 still shows both italic-
  paragraph and markdown `[^l11-wlog]` — the LaTeX twin will
  only render one. Decide.

---

## 2. The 'reviewer attack tree' (where I will push hardest)

If I were Reviewer 2, my single sharpest attack is **rigour vs
window-dressing**. The paper has:

1. A meta-theorem (T3) that is essentially Jensen + a Lipschitz
   constant — well-known machinery, repackaged.
2. Four instances — three of which are textbook (Shannon, Var,
   Gini) and one of which (Pinsker) is **not actually an
   instance** of the meta-theorem (it requires a separate
   sqrt-argument).
3. A formal property-testing apparatus (§0.5) that is the most
   genuinely novel contribution — Prop 0.3/0.4 give explicit
   falsification guarantees with mechanically-checked
   instantiations.

**My attack:** "The meta-theorem is light; the Pinsker case
breaks it; the value-add is the verifier discipline. **Lead
with the verifier discipline.** Right now the paper buries it
in §0.5 between Notation and Theorem 1. Restructure so the
verifier story is part of the contribution statement, not a
methods sub-section."

**Team response gate:** either (a) restructure (significant
work — own up if you don't want to), or (b) write a one-
paragraph rebuttal in the intro explicitly framing the
contribution as "rigorous bracketing + mechanical verification
+ real-data anchor on five GNN datasets", *not* "novel meta-
theorem."

---

## 3. Appendix A — VERIFICATION GATE: Prop 0.4 numerics

The text says
```
2 · (0.025)^16 ≈ 4.6e-26
```
Quick check:
- `(0.025)^2 = 6.25e-4`
- `(0.025)^4 = 3.91e-7`
- `(0.025)^8 = 1.526e-13`
- `(0.025)^16 = 2.328e-26`
- `2 × 2.328e-26 = 4.66e-26` ✓

So the constant in the paper is correct (I was wrong above —
that was a calibration trap for the team to *catch me*). The
arithmetic `4.6e-26` reproduces. **GATE PASSED**, but the team
must independently confirm with `python -c "print(2*(0.025)**16)"`
in the commit log before I sign off.

The downstream number `R · 4.6e-26 ≈ 2.3e-23` for R=500:
`500 × 4.66e-26 = 2.33e-23` ✓.

---

## 4. Pre-submission gate sequence (PI sign-off)

Submission is **blocked** until *all* of the following are
green. Team member assigned in `[brackets]` (fill in).

1. [ ] **Abstract written** (200 words, no jargon). [ ___ ]
2. [ ] **Title sharpened** or justified. [ ___ ]
3. [ ] **Status box → reproducibility manifest.** [ ___ ]
4. [ ] **Theorem numbering** sequential or preamble added.
       [ ___ ]
5. [ ] **All R1–R18 + V1–V5 + E1–E5 + S1–S7** answered in
       writing with line refs. [ ___ ]
6. [ ] **REPRO-1 … REPRO-5** all green. [ ___ ]
7. [ ] **Anchor JSON** in a publicly-accessible artifact with
       a citable URL/DOI. [ ___ ]
8. [ ] **LaTeX twin** (`main.tex`) updated and `make` is clean.
       [ ___ ]
9. [ ] **PI dry-run review** completed against this checklist
       and *fewer than 3 RED items remain*. [ ___ ]
10. [ ] **External (non-author) reader** has read the paper
        cold and signed off. [ ___ ]

Once 1–10 are green, I sign off and we submit. Not before.

---

## 5. PI's honest opinion (for the team only)

This is a **good, rigorous, mid-impact TMLR paper** as currently
scoped. It is not a flashy result; it is a *well-instrumented*
result. TMLR rewards exactly that. The two failure modes are:

- **Failure mode A — "thin novelty":** if I let the meta-
  theorem (T3) front-load the contribution. Mitigation:
  rebrand around the verifier discipline + real-data anchor.
- **Failure mode B — "calibration drift":** if any number in
  §0.5 or §3-C-Pi is off by even one order of magnitude, a
  reviewer who checks one cell will lose faith in all of them.
  Mitigation: every numerical claim has a `python -c "print(...)"`
  in the commit log.

If we close R1–R18 + V1–V5 + E1–E5 in two clean commits, we
ship in good conscience. If we cut corners on E4/E5 (vacuity
counts, margins), Reviewer 2 (me) will write a Major Revision
and we'll lose two months.

— **PI, signing off as Reviewer 2 in dry-run only.**
