# PI Review Strategy — Paper B (Partition Brackets) → TMLR

**Audience.** The Paper B team (authors of `main.md` /
forthcoming `main.tex`). Posted ahead of the PI's adversarial
review pass so the team has time to harden the manuscript.

**Venue assumption.** *Transactions on Machine Learning
Research.* TMLR explicitly disclaims novelty as an acceptance
criterion — the bar is **(i) technical rigor**, **(ii) clarity
/ presentation**, and **(iii) importance to the community**.
Reproducibility is not strictly required but is a strong
positive signal and a published TMLR certification badge.

**Posture.** I will review this paper the way I would review a
hostile submission: every claim is guilty until proven, every
constant has to come from a named lemma, every figure has to
match a JSON manifest at a SHA. If you cannot answer a
question in this document in under 60 seconds with a file +
line number, the paper is not yet review-ready.

---

## 0. Self-readability triage (do this first, ~30 min)

Run the paper through these three filters before the PI sees
it. If any one fails, fix locally and re-loop; do not escalate
yet.

| Filter | Pass condition | Owner |
|---|---|---|
| **A. One-sitting read** | A peer outside the project can read §0 → §6 in ≤ 90 minutes and recite the bracket statement of each numbered claim from memory. | Any team member |
| **B. JSON-back-link** | Every numerical constant in the paper (e.g. "$h \approx 6.07 \times 10^{-3}$", "$\rho_{\mathcal{M}} = 1$", "$\approx 0.279$") has a one-line citation pointing to either a file+line in `verify_b_t{1,2}.py` / `audit/stress.py` or a JSON key path in `audit/external_audit/*.json` / `audit/external_audit_SUMMARY.json`. | Theory-side |
| **C. Mutation-screen mapping** | For every numbered claim T3/C-Sh/C-Va/C-Pi/T6/T7/T9/P10/L11, name *which* mutant in `audit/stress.py` would catch a wrong-constant typo in that claim. If no mutant covers it, mark the claim **EXPOSED** in your team copy. | Verifier-side |

The honest current state: filter A is fine, B is partial
(constants exist but cross-refs are inline-comment only),
C has K = 3 mutants covering 3 of ~9 numbered claims — every
other claim is **EXPOSED** in the Definition-0.2 sense. The
PI will press hard on filter C.

---

## 1. PI review checklist — by section

This is the *exact* table the PI will fill in. Every row has a
red flag the PI is hunting for; the team should pre-empt each
one with a sentence in the paper, a forward reference to
`audit/`, or an explicit OP-#.

### §0 + §0.5 (Notation + Property-testing contracts)

| # | What I will check | Red flag | Status |
|---|---|---|---|
| 0.1 | Every symbol is introduced before use. | Inverse $\varphi^{-1}$ used before its domain is pinned. | OK (Notation block pins it). |
| 0.2 | Def 0.1 5-tuple slots map *bijectively* to engineering instantiation. | Slot mismatch between $\sigma$ (math) and `(seed, derandomize)` (code). | OK after c381a4f. |
| 0.3 | Prop 0.3 modelling assumption (A-PRNG) is **named** in the proof prerequisites, not buried in a footnote. | "IID" claim is hand-waved. | OK after c381a4f. |
| 0.4 | Prop 0.4 covers the *actual estimators* in `verify_b_t2_mc.py`. | Hoeffding form would fail on plug-in $\hat\varepsilon^*_\Pi$. | OK after c381a4f (McDiarmid). |
| 0.5 | The 4× tolerance inflation is **derived**, not asserted. | "Why 4 and not 3 or 5?" with no answer. | **WEAK** — currently justified by the in-line comment at `verify_b_t2_mc.py` ll. 304–306 ("4 plug-ins"); the union bound is implicit. PI will ask for a one-sentence union-bound derivation in the prose of Prop 0.4's numerical instantiation. **ACTION-1.** |
| 0.6 | Mutation screen $K=3$ is honest about its gap. | Definition 0.2 calls $K=3$ "comprehensive" when it is not. | OK — Status callout explicitly says comprehensiveness is **open** (OP-mut). |

### §1 (Definitions)

| # | Check | Red flag |
|---|---|---|
| 1.1 | (H1)–(H5) are *minimal*: each hypothesis is named in Step 5 of T3 as load-bearing for a specific inequality. | A hypothesis used in the proof but not listed in Def 1. **PI will diff Def 1's 5 hypotheses against T3 Step 5's "drop X kills Y" enumeration.** |
| 1.2 | (H1$'$) strict concavity is now disclosed in T3's "Hypotheses used" block. | Implicit appeal to strict monotonicity of $\varphi^{-1}$ without (H1$'$). |
| 1.3 | Pinsker/KL is *correctly* segregated as a failure-mode instance, not in the T3-compatible table. | Reader sees Pinsker next to Shannon and assumes T3 applies. |

### §2 (T3 meta-theorem)

| # | Check | Red flag |
|---|---|---|
| 2.1 | Step 1 (cell-wise reduction) uses *only* (H4) and is checkable per-cell. | Hidden use of (H2) or (H3). |
| 2.2 | Step 2 invokes Jensen with the correct random variable (rate, not loss). | Off-by-one in the convex-combination argument. |
| 2.3 | Step 3's smallness witness for $c_\varphi$ is *attained* (single cell at the supremum) or has a maximising sequence. | "Sharp" without a witness. |
| 2.4 | Step 4 sharpness witnesses are explicit, not "by symmetry". | One sentence sharpness sketch with no $m, p, \eta$ triple. |
| 2.5 | Step 5 failure modes name every inequality killed by every dropped hypothesis. | Missing "drop (H3)" case. **CHECK: (H3) continuity's failure mode is not enumerated in Step 5; only (H1), (H4), (H5), $c_\varphi=\infty$ are.** **ACTION-2.** |

### §3 (Instances: C-Sh, C-Va, C-Pi)

| # | Check | Red flag |
|---|---|---|
| 3.1 | C-Sh's identification with Paper A is symbol-for-symbol (verifier asserts $10^{-9}$ equality on a property cohort). | "Identical to Paper A's Theorem 1" without numerical evidence. |
| 3.2 | C-Va's bracket endpoints are *distinct*, and the prose explicitly says so (T6 caveat). | Reader confuses C-Va bracket with T6.MSE identity. OK after the explicit caveat in §4. |
| 3.3 | C-Pi vacuity threshold $H < 1 - 1/(2 \ln 2) \approx 0.279$ matches the D.10 anchor's empirical clipping rule. | Two different vacuity thresholds in prose vs anchor. OK — both currently say $\approx 0.279$. |
| 3.4 | C-Pi's "Bretagnolle–Huber sharper drop-in" claim is recorded as OP-BH (forward-reference) but currently §7 lists OP-MAE, OP-T5, OP-asym, OP-multi, OP-mut, A-PRNG, A-SHRINK — **OP-BH is referenced from §3 but missing from §7's list.** **ACTION-3.** |

### §4 (T6 regression)

| # | Check | Red flag |
|---|---|---|
| 4.1 | T6.MSE = identity, T6.MAE = upper-only, T6.MAE-lower = OP-MAE. | Reader infers a (false) two-sided bracket. |
| 4.2 | The "**not** a degenerate T3 bracket" caveat is prominent. | OK in current text. |

### §5 (T9 + T7)

| # | Check | Red flag |
|---|---|---|
| 5.1 | T9 reduces to T3 *on a lifted space* — the lift is constructive and the verifier B-T2 contract catches a mis-stated lift. | Hand-waved "by extension". OK. |
| 5.2 | T9 countable-alphabet extension is **explicitly** out of scope (OP-soft). But OP-soft is referenced from §5 and **missing from §7**. **ACTION-4.** |
| 5.3 | T7 only states the symmetric case; asymmetric noise is OP-asym. OK. |
| 5.4 | T7.bracket's denominator $1 - 2\rho > 0$ is non-vacuous for the verifier's $\rho \in \{0.05, 0.10, 0.20\}$. OK. |

### §6 (L11)

| # | Check | Red flag |
|---|---|---|
| 6.1 | L11 cites Paper A `lem:mpnn-wl-robust` and the $r_T$ table matches. | Constant mismatch between Paper A and Paper B's $r_T$. OK. |
| 6.2 | The COMBINE-second-arg-WLOG normalisation is *footnoted*, not hidden. OK. |
| 6.3 | sym-norm derivation uses Chung 1997 Lemma 1.7 — **the bibliography must contain this entry**. **ACTION-5.** |
| 6.4 | L11's verifier asserts on linear MPNN only; the *nonlinear* case is an upper estimate per the prose. PI will ask: what is the empirical slack on a nonlinear MPNN? Recommend a one-row sanity note pointing to a Paper A experiment. **ACTION-6.** |

### §7 (Open problems)

| # | Check | Red flag |
|---|---|---|
| 7.1 | Every OP-# referenced in §§1–6 appears in §7's list. **Currently OP-BH (§3) and OP-soft (§5) are missing — see ACTION-3 and ACTION-4.** |
| 7.2 | Each OP-# names the failure mode, the conjectured route, and the difficulty class. | "Open" with no further information. |

### §8 (Verifier contracts forward reference) and the wider repository

| # | Check | Red flag |
|---|---|---|
| 8.1 | Every claim's Verifier contract block exists. | Missing block. |
| 8.2 | The verifier function names in the prose actually exist in the codebase (`rg --type py 'def check_'`). | Stale function name after refactor. **ACTION-7.** |
| 8.3 | `audit/external_audit_SUMMARY.json` is the latest SHA and `all_pass = true`. | Out-of-date SUMMARY. (Audit at SHA `c381a4f` is in flight; refresh on completion.) **ACTION-8.** |
| 8.4 | `FORMAL_VERIFICATION_EXECUTION_PLAN.md` Lean roadmap is referenced from the introduction (or status banner) as the *certification* tier above property testing. **Currently only the §0.5 caveat references it.** Add one sentence to the top-of-paper status banner. **ACTION-9.** |

---

## 2. Adversarial questions the PI will ask in plenary

Prepare a one-paragraph answer to each. If you cannot answer
within one paragraph plus a single file:line citation, the
answer is not yet good enough.

**Q1 (rigor).** "Show me, line by line, that T3 Step 2's
appeal to a *strictly* increasing $\varphi^{-1}$ does not
secretly depend on differentiability of $\varphi$."

**Q2 (rigor).** "Why is the 4× inflation of the Hoeffding
halfwidth in Prop 0.4 the *right* constant rather than 3× or
5×? Walk me through the union bound."

**Q3 (rigor).** "T9 lifts via $\mathcal{X} \times \mathcal{Z}$
under measure $\mathbb{P}(dx) K(dz|x)$. Is this product
measurable? Does the lifted partition $\Pi_K$ generate a
sub-$\sigma$-algebra that actually equals the one used by
$G(K)$?"

**Q4 (importance).** "Why should TMLR care about this paper if
Paper A already proved the Shannon bracket and the binary
case? What does the meta-theorem buy that the special case
does not?"

**Q5 (importance).** "What does the Variance instance (C-Va)
give a practitioner that the law of total variance does not
already give them?"

**Q6 (rigor).** "Pinsker is admittedly vacuous below
$H \approx 0.279$. How many of the D.10 anchor rows fall in
the vacuous regime? Is the *clipped* envelope you publish
actually informative, or are you just reporting $\max(0,
\text{garbage})$?"

**Q7 (reproducibility).** "Give me one command and one SHA and
I will reproduce the six-tier audit on a clean machine in
under 30 minutes. Walk me through what happens if T3 fails
because Hypothesis bumped its API."

**Q8 (reproducibility).** "The mutation screen has K=3.
Convince me that a sign-flip in C-Pi's Pinsker constant
$\sqrt{(\ln 2)/2}$ would be caught. If not, why is that not a
silent mutant?"

**Q9 (presentation).** "I am a TMLR reviewer who has not read
Paper A. Page 1 should tell me exactly what is new here and
what is borrowed. Where on page 1 is that?"

**Q10 (presentation).** "Your status banner uses the phrase
'Phase 2b-md.G2 CLOSED'. A TMLR reviewer does not know what
that means. Strip all internal phase nomenclature from the
*manuscript* version (keep it in the repo docs)."

---

## 3. Action items (ordered by PI-blast-radius)

These are *blocking* for the TMLR submission, not nice-to-have.

| # | Action | Section | Owner | Effort | Blast radius |
|---|---|---|---|---|---|
| 1 | One-sentence union-bound derivation of the 4× factor in Prop 0.4's numerical instantiation. | §0.5 | Theory | 5 min | Closes Q2. |
| 2 | Add "Drop (H3) continuity" failure mode to T3 Step 5. | §2 | Theory | 10 min | Closes §2.5 audit. |
| 3 | Add **OP-BH** entry to §7 (Bretagnolle–Huber as sharper drop-in for C-Pi). | §7 | Theory | 5 min | Closes §3.4 audit. |
| 4 | Add **OP-soft** entry to §7 (countable-alphabet T9 extension under UI). | §7 | Theory | 5 min | Closes §5.2 audit. |
| 5 | Add Chung 1997 bibliography entry; cite as `\cite{chung1997spectral}` in §6 sym-norm derivation. | §6 + bib | Theory | 5 min | Closes §6.3. |
| 6 | One-line sanity row pointing nonlinear MPNN empirical slack to a Paper A experiment ID (`experiments/results/eX.json`). | §6 | Verifier | 15 min | Closes Q? on nonlinear tightness. |
| 7 | `rg --type py 'def check_' partition-brackets-framework/ > /tmp/verifier_fns.txt`, then `grep -oE 'check_[A-Za-z0-9_]+' main.md \| sort -u > /tmp/cited_fns.txt`, diff. Reconcile any drift. | §8 + verifiers | Verifier | 15 min | Closes Q7 partially. |
| 8 | Refresh `audit/external_audit_SUMMARY.json` to SHA `c381a4f` after the in-flight audit completes; commit. | audit | Driver | wait + 2 min | Closes §8.3. |
| 9 | One sentence in the top-of-paper status banner: "Mechanised certification roadmap (Lean/Mathlib) in `FORMAL_VERIFICATION_EXECUTION_PLAN.md`; this manuscript covers the property-testing tier." | top of main.md | Theory | 5 min | Closes §8.4. |
| 10 | Add JSON-back-link footnotes for the five most "magical" constants: $0.279$, $4.6\times 10^{-26}$, $7.8\times 10^{-16}$, $r_T$ table, $\rho_{\mathcal{M}} = 1$. | inline | Verifier | 30 min | Closes filter B. |
| 11 | Strip internal phase nomenclature ("Phase 2b-md.G2", "Phase 2d", "D.10") from the manuscript-facing text; keep in commits and notes. The audit banner can stay during draft circulation but **must be removed** before submission. | main.md banners | Theory | 20 min | Closes Q10. |
| 12 | One-page "What is new vs Paper A" paragraph at the *very* top of §1 (or as §0.4). For each numbered claim in Paper B, name what Paper A already covered (if anything) and what is genuinely new. TMLR reviewers will not read Paper A. | §1 | Theory | 60 min | Closes Q9 + addresses TMLR-importance criterion. |
| 13 | TMLR reproducibility appendix: one-page README in `audit/` titled `REPRODUCING.md` that gives the single command `bash audit/run_external_audit.sh`, lists the six tier outputs, names the SHA the manifests were generated at, and the Python + numpy + sympy + hypothesis versions tested. | audit/ | Driver | 30 min | TMLR reproducibility badge candidate. |

Total mechanical effort to "PI-review-ready" state:
approximately one afternoon of focused work, blocking on the
in-flight 21-minute audit refresh and (optionally) the Lean
roadmap remaining gated.

---

## 4. What I (PI) will **not** complain about

To save the team cycles, here is the list of things that look
weak but are actually *correct as published*:

- The mutation screen at $K = 3$ is explicitly disclosed as
  non-comprehensive (OP-mut). Reviewers who want $K \geq 30$
  can be answered with "Phase 3, in scope of Lean tier".
- C-Pi's 0-clipped envelope is the publishable convention,
  named as such; the bracket *is* genuinely vacuous below the
  threshold and the paper says so.
- T6.MAE is upper-only by design; OP-MAE is named.
- Paper A re-uses are cited verbatim with symbol-for-symbol
  identification (see C-Sh and L11).
- Property testing instead of Lean for the manuscript tier is
  defensible (it is what the paper actually does) — but the
  Lean roadmap must be visible (ACTION-9).

---

## 5. Submission-readiness gate

Paper B is submission-ready for TMLR when **all of**:

- [ ] Actions 1–9 closed (rigor + presentation).
- [ ] Actions 10–13 closed (importance + reproducibility).
- [ ] `audit/external_audit_SUMMARY.json` shows `all_pass: true`
  at the submission SHA.
- [ ] `main.tex` mirrors `main.md` for the §0.5 audit fixes
  (currently `main.tex` is frozen at Phase 2a; this is the
  blocking item for an actual TMLR upload — the audit-fix
  twin must land).
- [ ] One independent peer outside the project has read the
  full manuscript and answered the §1 audit checklist with no
  open flags.

When those boxes are ticked, escalate to the PI for the
*actual* adversarial pass. Until then, every reviewable
weakness above is a self-inflicted wound.
