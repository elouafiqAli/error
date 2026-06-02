# PLAN.md — operator on-ramp (preliminary, multi-iteration)

> **Purpose.** Take the operator from "first day in the department" to
> **can read the paper's abstract like a native, reproduce E3 on Cora
> end to end, and explain the bracket at a whiteboard to a peer**.
> We stop at **G2**. Anything beyond — senior-undergrad proof
> carpentry, Lean mechanisation, $\phi$-family generalisations — is
> the next track, tracked elsewhere.
>
> **Method.** fast.ai inversion. *Do first, name later.* Theory enters
> only when a plot or experiment fails without it. Python / numpy /
> sklearn / PyG are the default vocabulary. Lean and Julia are **BLUE
> (optional polish)** — they appear nowhere on the critical path.
>
> **Pedagogy verbs** (this plan's own, fast.ai-flavoured):
>
> - **Build** = the operator writes a 20-line script that *produces*
>   the construct, then reads its name. (Plot the envelope → read off
>   $w^*$ → *then* learn it is called Corollary 2.)
> - **Distinguish X vs Y** = a one-line difference; the *pair* is the
>   construct, not either side alone. Most confusions are pair-shaped.
> - **Mutate → fail → revert** = flip one sign or constant, watch the
>   verifier complain, restore. Builds intuition for which step the
>   verifier actually depends on. Cheapest insurance against
>   tick-the-box reading.
> - **False lead** = an approach that *almost* works; the operator
>   walks it, hits the wall, names the lesson. Immunises against
>   skim-reading.
>
> **Chocolate box** — supplementary resources the operator may dip
> into, none of which is canonical for this plan:
>
> - [`partition-sandwich-preprint/COMPANION.md`](../partition-sandwich-preprint/COMPANION.md)
>   — a bare "tick-the-box" reproduction checklist.
> - [`partition-sandwich-preprint/COMPANION-READER.md`](../partition-sandwich-preprint/COMPANION-READER.md)
>   — a *senior-undergrad* recite/prove/replicate ladder. Useful for
>   stealing the *shape* of a drill (e.g. "distinguish X vs Y"), not
>   as a syllabus the operator must complete.
> - [`partition-sandwich-preprint/VERIFICATION.md`](../partition-sandwich-preprint/VERIFICATION.md)
>   — the mechanised-verification ledger; row-to-JSON cross-check is
>   a fine warm-up after G1.
> - [`gnn.md`](../gnn.md) Ch 1–8 — reader prose around the WL operator
>   and the partition picture; cherry-pick by topic, do not read
>   linearly.
>
> The operator should treat this PLAN's critical path as canonical and
> use the chocolate box for snacks between gates, never as the meal.
>
> **Style of this document.** Three iteration passes are kept *visible*,
> not collapsed, so the operator sees the refinement of the plan as
> part of the pedagogy. Each pass augments the previous one.
>
> - **v1 — Intuition pass.** "Why does this paper exist? What does
>   $w^* \approx 0.1610$ mean? Can I see it in a plot?"
> - **v2 — Reproducibility pass.** "Can I rerun T1, T3, E1, E3, E6
>   from a cold checkout and reproduce the published numbers?"
> - **v3 — Translation pass.** "Can I read a paragraph of the paper
>   and point at the equivalent code / plot / theorem statement?"

---

## 0. Notation

```
[W] white   - mandatory; gate-blocking
[G] grey    - mandatory; same as white, distinct only when grouping
[Y] yellow  - skim once; two consecutive yellow skips = gate debt
[B] blue    - rigour polish; never gates
```

Gates: **G0** (entry literacy), **G1** (replication), **G2**
(translation).

Every item lists:
- a **construct** (the thing to touch / produce),
- a **demonstrator** (a Python snippet, a notebook cell, or a plot
  the operator must *create* — not a chapter to read),
- a **5-min checkpoint** (a yes/no question the operator can answer
  alone, ideally by pointing at a number on a plot).

---

## 1. Pre-0 prerequisites (Roman)

These pour into the PERT but are not paper work — they are shop-floor
literacy. **Lean and Julia are deliberately BLUE here.**

### I. **[W]** Read the abstract twice, mark every symbol you can't name

- **Construct**: a 1-page glossary that the operator writes themselves
  by listing every symbol of the abstract and giving each a plain-
  English line. Stuck symbols stay blank; gate G0 will check ≤ 2 blanks.
- **Demonstrator**: `onboarding/notes/00-abstract-symbols.md`. Required
  entries: $\varepsilon^*_\Pi$, $H(f \mid \Pi)$, $H_{\mathrm{bin}}$,
  $H_{\mathrm{bin}}^{-1}$, $w^*$, $\Pi^{\mathrm{WL}}_L$, $\Delta$,
  $\lambda_{\max}(A)$, $\tilde A_2$.
- **Checkpoint**: state in one sentence what *the paper is for*.
  (Acceptable answer: "Turn the 2019 1-WL ceiling into a number, then
  show that an optimisation-free predictor sits within $w^*$ of any
  trained MPNN.")

### II. **[W]** Tool floor — `python ≥ 3.11`, `numpy`, `matplotlib`, `scikit-learn`, `networkx`, `torch`, `torch-geometric`

- **Construct**: a virtualenv (or conda env) `onboarding/env/` with the
  packages above.
- **Demonstrator**: `onboarding/scripts/00-doctor.sh` that prints
  versions and exits non-zero if anything is missing.
- **Checkpoint**: `bash onboarding/scripts/00-doctor.sh` → exit 0.

### III. **[W]** Project tour — *what lives where*

- **Construct**: a four-line mental map: paper (`partition-sandwich-preprint/`),
  reader prose (`gnn.md` Ch 1–8 done, Ch 9–19 reference for theory),
  monograph macro-plan (`reader-monograph/PLAN.md`), and experiment
  ledger (`partition-sandwich-preprint/experiments/REPORTS.md`).
- **Demonstrator**: `onboarding/notes/00-tour.md` with one filename
  per artefact and one sentence about its role.
- **Checkpoint**: "Where does `main.pdf` get its bibliography from?"
  → `main.bib` via `bibtex` invoked by `Makefile`.

### IV. **[W]** Toy partition + binary entropy in 20 lines of Python

This is the *single most important pre-0 item*. If the operator skips
it, every later item collapses.

- **Construct**: a notebook that
  (1) defines a partition $\Pi$ of $\{0,\dots,99\}$ into 5 cells of
  random sizes;
  (2) generates a binary label $f$ with per-cell positive rates
  `[0.1, 0.3, 0.5, 0.7, 0.9]`;
  (3) computes `H(f | Π) = Σ q_i · H_bin(p_i)` and
  `ε*_Π = Σ q_i · min(p_i, 1-p_i)` *by hand* with `numpy`;
  (4) plots the **achievable region** $\{(H, \varepsilon)\}$ for a
  swept $p \in [0, 1]$ on a single cell, draws the **upper line**
  $\varepsilon \le H/2$ (Hellman–Raviv) and the **lower curve**
  $\varepsilon \ge H_{\mathrm{bin}}^{-1}(H)$ (Fano), then drops the
  point of the toy partition on top.
- **Demonstrator**: `onboarding/notebooks/01-toy-bracket.ipynb` saving
  `onboarding/plots/01-bracket-envelope.png`.
- **Checkpoint**: visually find $w^* \approx 0.1610$ on the plot
  (max vertical gap between the two envelopes). Note the $H$ at which
  it occurs ($H \approx 0.722$ bits, $\varepsilon = 1/5$).
- **Cross-link**: this is the operational version of Theorem 1 +
  Corollary 2 of `main.tex`. The operator must do this *before*
  reading any proof.

### V. **[W]** Toy graph + 1-WL in 30 lines of `networkx`

- **Construct**: build the 5-cycle $C_5$ and the disjoint union of
  two triangles $2K_3$. Run colour-refinement until stable. Show the
  cell counts.
- **Demonstrator**: `onboarding/notebooks/02-toy-wl.ipynb`. Print the
  partition after each round.
- **Checkpoint**: "Are $C_5$ and $2K_3$ 1-WL-distinguishable?"
  (Answer: yes — different cell-count vectors at depth 1.) "What
  about $C_6$ vs $2K_3$?" (Answer: no — same multiset, classic
  failure.)

### VI. **[Y]** SymPy + interval (bounding $w^*$ exactly)

- **Construct**: prove `0.1610 < w* < 0.1611` two ways: SymPy
  `Rational` symbolic evaluation, and `mpmath.mpi` interval rounding.
- **Demonstrator**: `onboarding/notebooks/03-wstar-exact.ipynb`.
- **Why YELLOW**: numerical proof is enough for the intuition pass;
  the operator's interval skills will be exercised again at G2 if
  they choose the Julia/Lean optional polish.

### VII. **[Y]** LaTeX/TMLR build literacy

- **Construct**: `pdflatex → bibtex → pdflatex × 2`; how `\label`/
  `\ref` cycles converge.
- **Demonstrator**: `make` in `partition-sandwich-preprint/`. Note
  page count. Edit one word; rebuild; confirm page count preserved.
- **Why YELLOW**: required only if the operator plans to edit the
  paper. Reading the paper does not need it.

### VIII. **[B]** Lean 4 kindergarten

- **Construct**: `elan default leanprover/lean4:v4.30.0`; `lake new
  toy_lean math`; one `ring` proof; `lake build`.
- **Why BLUE**: the operator can complete G0, G1, **and G2** without
  ever touching Lean. Lean enters only if they elect the formalisation
  contributor track post-G2.

### IX. **[B]** Julia + `IntervalArithmetic.jl` kindergarten

- **Construct**: `julia onboarding/julia/intervals.jl` reproducing
  three rows of the `verify.jl` interval table.
- **Why BLUE**: same as VIII. The `verify_t1_float.py` (Python) is
  on the critical path; the Julia interval check is a polish.

### X. **[B]** Git hygiene for research projects

- **Construct**: conventional-commit template from
  `.github/copilot-instructions.md` §4.
- **Why BLUE**: the operator can read every artefact without
  committing.

---

## 2. Iteration v1 — **Intuition pass** (gate G1's first half)

> Question the operator must be able to answer by end of v1:
> *"If I tell you the conditional entropy $H(f \mid \Pi)$ of a binary
> label given a partition, what is the tightest interval I can put
> around the per-cell Bayes error?"*
> Expected answer: $[H_{\mathrm{bin}}^{-1}(H),\; H/2]$, width at most
> $w^* \approx 0.1610$.

### 1. **[W]** Reproduce the abstract's two numbers in Python alone

- **Construct**: from the toy partition (item IV), reproduce
  $\varepsilon^*_\Pi$ and $H(f \mid \Pi)$ numerically. Draw the point.
  Sweep the per-cell positive rates over a grid and overlay 50 points
  on the achievable-region plot. Confirm they all fall in the strip.
- **Demonstrator**: `onboarding/notebooks/04-strip-50.ipynb`.
- **Checkpoint**: max vertical gap observed over the 50 points; does
  it ever exceed $w^* + 10^{-4}$?

### 2. **[W]** Read §1 (Introduction) of `main.tex` and re-cast the
"three confounds" decomposition (Prop. star-decomp) as **pseudocode**

- **Construct**: a one-page note explaining the structural / feature
  / head decomposition: a trained MPNN's risk =
  *partition-conditional Bayes error* +
  *feature refinement gain* +
  *head/optimisation slack*. Each summand a Python comment.
- **Demonstrator**: `onboarding/notes/05-three-confounds.md` with one
  pseudocode block of ≤ 20 lines.

### 3. **[Y]** Run `verify_t1_float.py` and stare at `verify_t1.json`

- **Construct**: from cold checkout, `python
  partition-sandwich-preprint/verify_t1_float.py`. Open
  `verify_t1.json`; locate the row with max upper slack; confirm it
  matches the $\approx 0.1610$ landmark.
- **Why YELLOW**: pleasant confidence boost. The operator already
  has the intuition from item 1; this is the *paper's own* version of
  it.

### 4. **[W]** Walk gnn.md Ch 1 and Ch 2 with a notebook

- **Construct**: read `gnn.md` Ch 1 (set partitions, 1-WL refinement)
  and Ch 2 (discrete information theory, partition entropy, Fano
  bridge). After each major lemma, type a 3-line Python sanity check
  in `onboarding/notebooks/06-gnn-ch1-ch2.ipynb`.
- **Demonstrator**: the notebook with ≥ 5 sanity checks, one per
  named result.

### 5. **[Y]** Walk gnn.md Ch 6 (Bayesian decision theory, purity,
metrology)

- **Construct**: same recipe as item 4. Pay attention to *purity*
  (= $1 - 2 \cdot \min(p, 1-p)$) and the cell-purity diagnostic.
- **Why YELLOW**: helps E3 interpretation later; the bracket itself
  is fine without it.

### 5b. **[W]** **Distinguish drill** — the three Bayes-error objects

- **Construct**: write three one-liners that distinguish
  $\varepsilon_X$ (one number, the prior),
  $\varepsilon_{X\mid T}$ (one number, averaged over the statistic),
  and the per-cell vector $\{e_C\}_C$ (the granular object the
  bracket operates on).
- **Demonstrator**: `onboarding/notes/06b-three-objects.md`.
- **Checkpoint**: "Which of the three does Hellman–Raviv bound *on the
  left-hand side*?" (Answer: $\varepsilon_{X\mid T}$ — the averaged
  one; the per-cell version is bounded *pointwise* by $\tfrac12 H_{\mathrm{bin}}(e_C)$ first, then averaged.)

### G1 self-assessment — "Reproducer of the intuition" (10 questions)

Pass: 10 yes; ≤ 1 yellow skipped in v1.

1. `bash onboarding/scripts/00-doctor.sh` exits 0?
2. `notes/00-abstract-symbols.md` has ≤ 2 blank entries?
3. `notebooks/01-toy-bracket.ipynb` produces the envelope plot?
4. Did you read off $w^* \approx 0.1610$ from your own plot?
5. Did you note the $\varepsilon = 1/5$ extremiser?
6. `notebooks/02-toy-wl.ipynb` distinguishes $C_5$ vs $2K_3$ and
   *fails* on $C_6$ vs $2K_3$?
7. `notebooks/04-strip-50.ipynb` shows zero violations of the strip
   over 50 random rates?
8. Can you write the three-confounds decomposition as pseudocode?
9. Have you spent at least 30 minutes inside `gnn.md` Ch 2 typing
   sanity checks?
10. Logged wallclocks somewhere (`notes/timings.md`) so cache
    regressions are detectable on rerun?

---

## 3. Iteration v2 — **Reproducibility pass** (gate G1's second half +
runway to G2)

> Question by end of v2:
> *"Cora, CiteSeer, PubMed. Bracket vs realised GCN/GIN/GraphSAGE
> error. Where on the plot does each architecture land, and does the
> bracket bound the realised error in every case?"*

### 6. **[W]** Reproduce the paper PDF from cold

- **Construct**: `make` in `partition-sandwich-preprint/`. PDF page
  count matches the in-repo `main.pdf`.
- **Demonstrator**: `pdfinfo main.pdf | grep Pages`.

### 7. **[W]** Run T3 (`verify_t3_symbolic.py`) cold

- **Construct**: SymPy symbolic proofs of S1–S10 incl. Prop 6
  marginal-aware piecewise + Table 1 reproduction.
- **Demonstrator**: 10 / 10 ✓ on stdout, `verify_t3.json` written.
- **Checkpoint**: open `examples.tex` and quote `\wmarg20` (≈ 0.0916).

### 8. **[W]** Run E1 (decision-tree refinement funnel)

- **Construct**: pick the E1 driver from
  `partition-sandwich-preprint/experiments/`. Run on Adult or wine.
  Produce the funnel plot: bracket width vs depth.
- **Demonstrator**: PNG saved under `onboarding/plots/e1-funnel.png`
  reproducing the published figure shape (need not be byte-identical).
- **Checkpoint**: at what depth does the bracket close to within
  $w^*$?

### 9. **[W]** Run E3 — the headline experiment — on **Cora alone first**

- **Construct**: follow `experiments/REPORTS.md` §"E3 — WL refinement
  bracket on real graphs". Use the existing driver. Cora only at this
  stage to keep wallclock < 30 min on CPU.
- **Demonstrator**: scatter of realised GCN error vs bracket
  $[H_{\mathrm{bin}}^{-1}(H_{\mathrm{WL}}),\; H_{\mathrm{WL}}/2]$ for
  WL depth $L \in \{1,2,3,4\}$.
- **Checkpoint**: does the realised error of a 2-layer GCN sit
  *within* the depth-2 bracket?

### 10. **[Y]** Extend E3 to CiteSeer + PubMed

- **Construct**: same driver, larger datasets. Possibly switch on
  GPU.
- **Why YELLOW**: Cora alone is enough to claim G1; CiteSeer/PubMed
  raise the operator from "knows it works on one dataset" to "knows
  the bracket is genuinely a bound, not a fluke".

### 11. **[Y]** Run E6 NAS (UCI Adult, training-free arch ranking)

- **Construct**: training-free pre-filter ranks an arch menu by
  bracket midpoint; compare to the realised post-training ranking;
  report Kendall $\tau$.
- **Demonstrator**: reproduce the abstract's headline $\tau = 0.48$,
  $p = 5 \times 10^{-5}$ (or close, given run noise).
- **Why YELLOW**: this *is* the killer app of the paper, but Cora
  E3 (item 9) is already a load-bearing G1 pillar; one of {10, 11}
  is enough to clear G1, both is ideal.

### 11b. **[W]** **Mutate → fail → revert** on T1

- **Construct**: in a *throwaway* copy of `verify_t1_float.py`, flip
  the sign in the upper-bracket comparison (`<=` → `>=` or change
  `0.5` to `0.4`). Re-run. Watch the verifier emit `violations > 0`
  and a max upper slack that no longer matches $0.1610$. Then
  `git checkout` the file.
- **Demonstrator**: a 5-line `onboarding/notes/07b-mutate.md` naming
  (a) the mutation, (b) the violation it produced, (c) which step in
  the published proof the verifier was actually depending on.
- **Checkpoint**: "Which line of the verifier corresponds to the
  $\tfrac12 H(f\mid\Pi)$ upper envelope?" (the operator must point at
  it.)
- **Why WHITE**: without this, the operator believes the verifier
  rather than understanding what it checks.

### 11c. **[Y]** **False lead** — the "Rényi sharpening" trap

- **Construct**: try to sharpen the upper envelope by replacing
  $H_{\mathrm{bin}}$ with $R_2$ (collision entropy is smaller, so the
  bound *looks* tighter). In a notebook, sweep a 2-cell partition;
  show that the proposed "upper" bound *crosses below* a known
  Hellman–Raviv-saturating family. Conclude: the proposed sharpening
  *violates* the witness, hence is not a valid upper bound.
- **Demonstrator**: `onboarding/notebooks/11c-renyi-trap.ipynb`.
- **Why YELLOW**: skippable, but pairs with item 11b. If both 11c and
  11 are skipped, debt is incurred.
- **Lesson the operator must write down**: "Tightness witnesses are
  the verification you owe before announcing an improvement."

### G1 final self-assessment (10 questions)

Pass: 10 yes, ≤ 1 yellow skipped *across v1 and v2 combined*.

1. PDF rebuild matches?
2. T3 symbolic 10 / 10?
3. E1 funnel plot reproduced?
4. E3 on Cora reproduced with the scatter?
5. Did the GCN error sit inside the bracket?
6. Did you run *at least one* of {CiteSeer, PubMed} extension or
   E6 NAS?
7. Can you read the Kendall $\tau$ off the published table without
   re-deriving it?
8. Did you log wallclocks for E1, E3, E6 (item 1 of `notes/timings.md`
   already exists)?
9. Did the **mutate-fail-revert** drill (item 11b) actually fail the
   verifier? Did you name the dependent step?
10. Have you written a 3-paragraph self-report in
    `notes/07-g1-debrief.md` explaining (a) what the bracket bounds,
    (b) what the realised error is, (c) what $w^*$ means physically?

---

## 4. Iteration v3 — **Translation pass** (gate G2)

> Question by end of v3:
> *"Open `main.tex` at any random theorem statement. Point at the
> code / plot / Lean stub that mechanises it (or argue there is
> none yet)."*

### 12. **[W]** Build the paper-to-artefact map

- **Construct**: a 4-column table (paper claim · code/plot · Lean
  identifier if any · status) for the abstract's 4 contributions:
  the bracket, the three-confounds decomposition, the
  $\varepsilon$-robust constancy lemma, the spectral refinement.
- **Demonstrator**: `onboarding/notes/08-map.md`.
- **Checkpoint**: identify the Lean theorem that is the literal
  transcript of Theorem 1. (Answer: `FinPart.sandwich` in
  `partition-sandwich-preprint/formal/PartitionBracket/Sandwich.lean`.)
  Lean knowledge is *not* required — the table column may say
  "exists, sorry-stubbed" without further commentary.

### 13. **[W]** Translation drill 1 — Hellman–Raviv aggregated

- **Construct**: take §3 of `main.tex` (the upper-side proof). Write
  20 lines of Python that *evaluates* the bound on a random partition
  family and asserts it. Do not re-derive anything.
- **Demonstrator**: `onboarding/notebooks/09-hr-eval.ipynb`.
- **Checkpoint**: state in one sentence which Mathlib identifier
  (`Real.binEntropy`, `binEntropy_le_log_two`, …) is the closed-form
  workhorse. The operator may discover it via `grep` in
  `partition-sandwich-preprint/formal/PartitionBracket/`.

### 14. **[W]** Translation drill 2 — Lemma 6 (ε-robust constancy)

- **Construct**: read the lemma statement; reproduce its Python proxy
  via `experiments/e3e_robust_lemma.py`; plot ε vs the max
  within-cell pair distance.
- **Demonstrator**: `onboarding/plots/14-eps-robust.png`.
- **Checkpoint**: does the lemma's bound hold tightly, loosely, or
  fail on the chosen dataset? Write 2 lines.

### 14b. **[W]** **Aggregator triple distinguish** — the E3 punchline

- **Construct**: from `e3e_robust_lemma.py`'s output table, identify
  the constants $r_T = (\Delta_{\max}, 1, 1)$ for $T \in
  \{\mathrm{sum}, \mathrm{mean}, \mathrm{sym\text{-}norm}\}$. Note
  that on Cora $\Delta_{\max} = 168$ drives the sum-aggregator
  bound up to 7 orders of magnitude looseness — **the bound is
  never violated, it is just honestly loose**.
- **Demonstrator**: `onboarding/notes/08b-aggregator-triple.md`
  listing the three constants, and naming which architectures
  (GIN, GCN, GraphSAGE) use which aggregator.
- **Checkpoint**: **Distinguish** "honest looseness" (the bound is
  loose by design; the cause is named in the paper) vs. "a bug" (the
  bound is violated). Write the two-line distinction.

### 14c. **[W]** **Calibrated confidence drill** — the audit ritual

- **Construct**: for each of the four contributions on the
  paper-to-artefact map (item 12), assign one of
  `HIGH` / `MEDIUM` / `LOW` / `UNVERIFIED` and **justify in one line
  each** (which verifier, which experiment, which proof step).
- **Demonstrator**: an extra column in `notes/08-map.md`.
- **Checkpoint**: cross-check against the audit table in
  [`future-work/07-three-paper-arc-master-plan.md`](../future-work/07-three-paper-arc-master-plan.md) §1.
  Differences are not errors — they are calibration disagreements
  the operator must defend in writing.

### 14d. **[Y]** **False lead** — the "refinement = monotone endpoints"
trap

- **Construct**: try to prove refinement monotonicity by *adding*
  cells one at a time and showing the bracket *endpoints* shrink at
  each step. In a notebook, construct a counter-example: add a cell
  of mass $q_C \approx 0$ with $e_C = 1/2$. Show that one endpoint
  goes *up*, even though the interval as a whole still contains the
  previous one.
- **Demonstrator**: `onboarding/notebooks/14d-monotone-trap.ipynb`.
- **Lesson**: "The object that is monotone is the *interval*, not
  its individual ends."
- **Why YELLOW**: skippable, but if 14d AND 11c are both skipped, the
  operator has skipped both false-lead drills and the gate fails.

### 15. **[Y]** Read the active session checkpoint

- **Construct**: open
  [`/memories/session/lean-mechanisation-checkpoint.md`](../../memories/session/lean-mechanisation-checkpoint.md).
  Summarise in `onboarding/notes/09-handover.md` (≤ 10 bullets) what
  phases of the Lean mechanisation are done, what is WIP, what comes
  next.
- **Why YELLOW**: only matters if the operator will pick up Lean
  contribution. If they will not, blue out.

### 16. **[B]** Lean kindergarten exit ticket

- **Construct**: if (and only if) item VIII was done, write a 1-line
  `theorem` in `onboarding/lean-toy/MyStub.lean` that types-check
  with `sorry` for *any* claim from the paper.
- **Why BLUE**: pure polish.

### 17. **[B]** Julia interval kindergarten exit ticket

- **Construct**: same recipe with `verify.jl`-style interval check
  on the $w^*$ landmark.
- **Why BLUE**: pure polish.

### G2 self-assessment (10 questions)

Pass: 10 yes; ≤ 1 yellow skipped across v3.

1. `notes/08-map.md` exists with 4 contributions mapped *and* a
   calibrated-confidence column (item 14c)?
2. Can you point at the Lean identifier for Theorem 1 (Sandwich)
   and Corollary 2 (UniformSlack)?
3. `notebooks/09-hr-eval.ipynb` produces a non-trivial number
   matching the published value to 3 decimals?
4. `plots/14-eps-robust.png` exists and matches the qualitative shape
   of the published figure?
5. Can you **distinguish** "honest looseness" vs. "a bug" using the
   $r_T = (\Delta_{\max}, 1, 1)$ aggregator triple (item 14b)?
6. Did you run *at least one* false-lead drill (11c or 14d) and
   write the lesson in your own words?
7. Did you read the active session checkpoint OR justify the blue
   skip in `notes/skipped.md`?
8. Have you reconciled `VERIFICATION.md` row-by-row with the JSON
   files it points to?
9. Have you logged the new wallclocks alongside the G1 ones in
   `notes/timings.md`?
10. Have you decided whether your next session is research /
    proof-track or replication / new-experiments? Either is fine;
    ambiguity is not.

---

## 5. PERT — critical path is WHITE only

```
                       Pre-0                          Iteration v1 → v2 → v3
                                                      (intuition · replication · translation)

   I (W) abstract glossary ──┐
                             │
   II (W) python env ────────┼──► [G0]
                             │       │
   III (W) repo tour ────────┤       ├──► 1 (W) reproduce abstract numbers ─┐
                             │       │                                       │
   IV (W) toy bracket ───────┤       ├──► 2 (W) three confounds pseudo ─────┤
                             │       │                                       │
   V (W) toy 1-WL ───────────┤       ├──► 3 (Y) T1 verifier ────────────────┤
                             │       │                                       │
   VI (Y) sympy/intervals ───┤       ├──► 4 (W) gnn.md Ch 1–2 sanity ───────┤
                             │       │                                       │
   VII (Y) LaTeX build ──────┤       ├──► 5 (Y) gnn.md Ch 6 purity ─────────┤
                             │       │                                       ├──► [G1]
   VIII (B) Lean ────────────┘       ├──► 6 (W) reproduce PDF cold ─────────┤
   IX  (B) Julia                     │                                       │
   X   (B) git                       ├──► 7 (W) T3 verifier ────────────────┤
                                     │                                       │
                                     ├──► 8 (W) E1 funnel ──────────────────┤
                                     │                                       │
                                     ├──► 9 (W) E3 on Cora ─────────────────┤
                                     │                                       │
                                     ├──►10 (Y) E3 on CiteSeer/PubMed ──────┤
                                     │                                       │
                                     └──►11 (Y) E6 NAS ─────────────────────┘
                                                                             │
                                                                             ▼
                                                            12 (W) paper-to-artefact map
                                                            13 (W) HR translation drill
                                                            14 (W) Lemma 6 translation drill
                                                            15 (Y) read Lean checkpoint
                                                            16 (B) Lean polish
                                                            17 (B) Julia polish
                                                                             │
                                                                             ▼
                                                                           [G2]
```

**Critical path (white only):**
`I → II → III → IV → V → G0 → 1 → 2 → 4 → 6 → 7 → 8 → 9 → G1 → 12 → 13 → 14 → G2`

Yellow may be skimmed once. Blue may be skipped entirely.

---

## 6. Colour & pruning rules (formal)

For every gate G ∈ {G0, G1, G2}, denote by $Y(G)$ the multiset of
yellow items skipped since the previous gate (or the start, for G0).
Gate passes only if:

1. Every WHITE item on the critical path is `done`.
2. $|Y(G)| \le 1$. Two consecutive yellow skips = automatic debt;
   repay one before re-attempting.
3. Self-assessment ≥ 10 / 10.

Blue items never gate. They are a parking lot for the operator who
wants to be more rigorous; revisit them as warm-ups when a research
session begins.

---

## 7. What this plan deliberately does **not** cover

So future authors of `onboarding/` know where the boundary is:

- **Deep theory of $\phi$-bracket families** (Paper B). Defer to
  [`future-work/05-sequel-paper-plan.md`](../future-work/05-sequel-paper-plan.md).
- **k-WL / HDX trickle-down constructions** (Paper C). Defer to
  [`future-work/06-kwl-bracket-paper-roadmap.md`](../future-work/06-kwl-bracket-paper-roadmap.md).
- **GNN training pipelines from scratch** (SGD theory, optimisers,
  Adam, LR schedules). The paper's headline contribution is
  *training-free*. The operator needs `torch_geometric`'s defaults
  only — not optimiser theory.
- **`reader-monograph/` Ch 9–16 / `gnn.md` Ch 9–19 derivations.**
  Those are for the *reader of the paper*, not the *operator of the
  experiments*. Open them after G2.
- **Beyond G2.** No "G3, G4, …" defined here. After G2 the operator
  graduates to the project's main discipline mantra.

---

## 8. Iteration log

| Pass | Date | Author | Change vs previous |
|---|---|---|---|
| v0 (deleted) | 2026-06-02 | Claude | Lean/Julia on the critical path; too tool-heavy. Operator: "too focused on Lean". |
| v1 (deleted) | 2026-06-02 | Claude | Lean/Julia → BLUE. fast.ai inversion. Three iteration passes. gnn.md Ch 1, 2, 6 added. E3 Cora on critical path. |
| v2 (superseded) | 2026-06-02 | Claude | Adversarial re-read; added mutate-fail-revert, false-lead drills, distinguish-pair format, calibrated-confidence audit, aggregator triple. **Mis-step:** re-anchored G2 as "ramp into COMPANION-READER Part 1" — elevated one chocolate-box resource to canonical syllabus. Operator corrected. |
| v3 (this) | 2026-06-02 | Claude | **Restored own pedagogy** as canon: G2 promises = read abstract / reproduce E3 / explain at whiteboard. COMPANION-READER demoted to a chocolate-box entry alongside COMPANION, VERIFICATION, gnn.md. Kept the v2 drills (mutate-fail-revert, false-leads, distinguish, calibrated confidence, aggregator triple) on their own pedagogical merit — they are fast.ai-native, not COMPANION-READER's invention. Removed all "borrowed from COMPANION-READER" annotations. |

Future passes should land here when the operator runs the plan once
and reports back what was confusing.

---

## 9. Status

- **Plan version**: r4 (intuition-first, own-pedagogy-canonical).
- **Author**: Claude (Copilot), 2026-06-02.
- **Next concrete deliverable on the operator's side**:
  `onboarding/notes/00-abstract-symbols.md` (item I). Do not
  pre-populate the scripts/notebooks; **the act of creating them is
  the construct**.
- **Beyond G2** (deliberately *not* in this plan): proof carpentry,
  Lean mechanisation, $\phi$-bracket generalisations. The operator
  picks one of those tracks after G2; this plan does not prescribe
  which.