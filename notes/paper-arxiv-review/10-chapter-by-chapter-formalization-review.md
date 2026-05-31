# Chapter-by-chapter formalization review of `PAPER-ARXIV.md`

This note follows the paper section-by-section, identifies the major theorem/proof content, and records concrete ways to strengthen the formalization. It is informed by the background theorem patterns in:

- `background/arXiv-1810.00826v3/*.tex`
- `background/arXiv-1810.02244v5/main.tex`

---

## Abstract

### What the abstract currently does
- Defines PA-MPC at a high level.
- States the central theorem and its sandwich form.
- Mentions Lean witness, exact-rational ledgers, pilot experiments, and C1.

### Formal/editorial strengths
- The central theorem is stated explicitly.
- Trust-tier language is unusually honest.

### Main issues
1. **Overloaded scope**: theorem, formal verification, exact experiments, float-tier pilots, and an open conjecture are all compressed into one paragraph.
2. **Temporal inconsistency on C1**:
   - the abstract says the continuous-transfer conjecture remains pending real-GPU execution,
   - but later `§9.E` says it is frozen and supported-by-evidence on `anchor_8`.
3. **The theorem statement is mixed with implementation/status metadata**, which weakens the conceptual headline.

### Recommended enhancement
- Split the abstract into four sentences only:
  1. problem and definition,
  2. theorem,
  3. proof/verification status,
  4. empirical/open-problem status.
- Choose **one** C1 status and propagate it everywhere.

---

## 1. Introduction

### Current theorem/proof role
- Introduces the gap relative to WL expressivity work.
- States the two claimed gaps PA-MPC fills.
- Lists contributions.

### Strong points
- Good motivation for architecture-indexing rather than model-indexing.
- Contributions are explicitly grouped into theory / Lean / empirical / reproducibility.

### Under-formalized points
1. **Architecture family specification is conceptually central but not defined early enough.**
2. **The theorem-vs-evidence-vs-conjecture boundary is not yet sharp enough.**
3. **C1 status again conflicts with later sections** (intro calls it the headline open problem; `§9.E` calls it frozen with evidence).

### Recommended enhancement
- Introduce, in the introduction itself, one compact formal sentence:
  - an architecture family contributes only an initial observable partition and a message-passing admissibility class.
- End the introduction with a three-way division:
  - **proved**: Theorem 1 and corollaries,
  - **mechanized/verified on anchors**: Lean and exact ledgers,
  - **empirical status only**: E01/E04/E06/E08 and C1.

---

## 2. Related Work

### Current theorem/proof role
- Positions PA-MPC relative to WL expressivity, MPC, oversmoothing, over-squashing, and higher-order WL.

### Strong points
- Correctly places the paper downstream of WL expressivity literature.
- Notes that the contribution is quantification rather than isomorphism characterization.

### Under-formalized points
1. The comparison to Xu et al. and Morris et al. is conceptually right, but the paper does **not yet exploit their proof architecture**.
2. The relation to Kemper et al. is important, but the paper should distinguish more cleanly:
   - what is imported from LossyWL/MPC,
   - what is new here (family indexing + Bayes sandwich + witnesses).

### Recommended enhancement
- Add a short paragraph explicitly mapping your theorem chain to the background theorem chains:
  - Xu/Morris: structural refinement/equivalence,
  - this paper: partition-information sandwich once the partition is fixed.
- This makes the novelty mathematically legible.

---

## 3. Theory

This is the core of the manuscript.

### 3.1 Definitions

#### Current major proof ingredients introduced
- architecture-induced partition `Pi_A(G,L)`
- DIG and surrogate DIG
- PA-MPC
- WL-measurable task class
- purity lemma

#### Strong points
- DIG is introduced cleanly via cell-level Bernoulli posteriors.
- The surrogate variance form is useful for Lean-facing witness work.
- Purity lemma is concise and correct.

#### Main formalization gaps
1. **`LossyWL` is not specified enough inside the paper.**
   - A citation alone is okay for exposition, but not enough for a theorem spine that later relies on factorization through `Pi_A(G,L)`.
2. **`admissible architecture-family specification` is invoked in Theorem 1 but never formally defined.**
3. **`F_WL(G)` is introduced too early for the theorem actually proved.**
   - The Bayes sandwich is true for any partition and any binary task.
4. **Uniform measure is hard-coded**, although the theorem is naturally measure-theoretic and would be cleaner for arbitrary `mu`.

#### Recommended enhancement
Add a compact admissibility definition, e.g.:
- shared local update maps across vertices,
- permutation invariance over neighbor multisets,
- no access to identifiers beyond the declared initial observable partition,
- depth-`L` outputs depend only on the depth-`L` rooted colored neighborhood induced by `Pi_A^(0)`.

Also consider splitting the definitions into:
- **pure partition-information definitions**, and
- **graph/WL-specific instantiation definitions**.

#### New theorem that should likely be added here
**Proposition (refinement monotonicity).** If `Pi'` refines `Pi`, then
- `DIG(f | Pi') <= DIG(f | Pi)`,
- `eps*_{Pi'} <= eps*_{Pi}`.

This is currently relegated to experiment E03, but it is a theorem, not an empirical phenomenon.

### 3.2 The Bridge Inequality

#### Current major theorem steps
For a fixed partition `Pi`:
1. define cell posterior `P_C`, cell mass `q_C`, and Bayes cell error `min(P_C,1-P_C)`;
2. define `eps*_Pi = sum_C q_C min(P_C,1-P_C)`;
3. prove lower bound through an entropy inequality and inversion;
4. prove upper bound by the pointwise scalar inequality `min(p,1-p) <= H_bin(p)/2`;
5. derive architecture factorization corollary.

#### What is mathematically strong
- The theorem is operationally meaningful.
- The upper bound is pleasantly simple and tight at balanced cells.
- The no-additive-slack presentation is clean.

#### Key formalization improvement
The current Theorem 1 is best viewed as **two separate statements**:

1. **Pure partition theorem**:
   for any finite partition and any binary task,
   `H_bin^{-1}(DIG) <= eps* <= DIG/2`.

2. **Architecture corollary**:
   if an admissible depth-`L` MPNN factors through `Pi_A(G,L)`, then every such predictor has error at least `eps*`.

This split would mirror the theorem layering of the background papers and remove unnecessary WL-specific assumptions from the entropy theorem.

#### Cleaner proof route for the lower bound
The present text says “per-cell Fano, aggregated by mass.” A cleaner route is:
- define `e_C := min(P_C,1-P_C)`;
- observe exactly that `H_bin(P_C) = H_bin(e_C)` for every cell;
- therefore `DIG = sum_C q_C H_bin(e_C)`;
- use concavity/Jensen:
  `sum_C q_C H_bin(e_C) <= H_bin(sum_C q_C e_C) = H_bin(eps*)`;
- invert on `[0,1/2]`.

This is simpler than invoking Fano and is exact in the binary partition setting.

#### Corollary 3.1 needs promotion to a proper proposition-level dependency
Right now the proof is just:
> vertices in the same cell have identical depth-`L` rooted coloured neighborhoods, hence identical MPNN outputs.

This is plausible, but it should be formalized in the style of Xu/Morris:
- same partition cell -> same depth-`L` rooted colored neighborhood;
- admissible message-passing updates are permutation invariant and shared;
- inductively same neighborhoods give same hidden states.

That proposition is the real bridge from structural partitions to prediction lower bounds.

#### Suggested theorem reorganization inside §3
- **Theorem 1 (partition Bayes-entropy sandwich)**
- **Proposition 3.2 (partition refinement monotonicity)**
- **Proposition 3.3 (architecture factorization through `Pi_A(G,L)`)**
- **Corollary 3.4 (PA-MPC lower/upper bounds for depth-`L` admissible families)**

That order is substantially cleaner.

### 3.3 Three Named Conjectures

#### Current role
- registry of open problems with falsifiers and gates.

#### Comment
- Good governance, but this section is **not part of the theorem spine**.
- Moving it after the empirical or reproducibility sections would reduce cognitive interruption inside Theory.

### 3.4 The `MI^2 ~ 1/2` cautionary note

#### Current role
- warns against a degenerate normalization.

#### Comment
- The point is intellectually valid, but it currently interrupts the theorem flow.
- Better as:
  - a remark after a proved proposition, or
  - an appendix note.

### 3.5 Scope

#### Main formalization note
- This is where `f in F_WL(G)` should be discussed carefully.
- The **partition sandwich theorem itself does not need this scope restriction**.
- The scope restriction belongs to the **architectural interpretation**, not the pure entropy theorem.

---

## 4. Exact-Rational Ledger (L-I)

### Current theorem/proof role
- computational confirmation on exact small anchors.

### Strong points
- Trust-tiering is explicit.
- The ledger language is disciplined.

### Main formalization issue
- Several claims here are really **theorems that should move to §3**, especially monotonicity under refinement.
- E03 should demonstrate computation/implementation correctness, not serve as the primary support for a monotonicity fact.

### Recommended enhancement
Reframe Section 4 as:
- “exact finite-anchor illustrations / audits of the theory,”
not
- “verification of the theory” when the item is mathematically provable already.

---

## 5. Float-Tier Baseline

### Current role
- qualitative oversmoothing baseline.

### Comment
- Fine as a baseline section.
- No major theorem-formalization issue beyond keeping it clearly outside the proof spine.

### Editorial enhancement
- Shorten and explicitly mark as motivational/qualitative evidence.

---

## 6. Lean Witness (L-II)

### Current theorem/proof role
- mechanized witness for a shadow of the bridge on finite anchors.

### Strong points
- Honest statement of what is mechanized and what is deferred.

### Main formalization issue
- The paper should align the theorem naming more tightly with the mechanized content.
- If only the variance-kernel shadow and integer lower-side companion are mechanized, the main text should avoid sounding as if the full Theorem 1 is machine-checked.

### Recommended enhancement
Add a micro-table:
- theorem/proposition name,
- status = paper proof / Lean full / Lean finite witness / deferred.

That would make the proof status transparent.

---

## 7. Pilot-Tier Results

### Current role
- apparatus and pilot analyses.

### Strong points
- Extremely honest reporting.

### Main issue: status conflict with §9
- `§7.3` says the headline C1 test remains pending,
- while `§9.E` says the literal §9 rule has been applied and C1 is supported-by-evidence at `L >= 3`.

This is the biggest cross-chapter inconsistency in the manuscript.

### Recommended enhancement
Choose one of two editorial modes:

1. **Pre-freeze paper mode**
   - C1 remains open/pending.
   - remove or move `§9.E` to a future-work note.

2. **Post-freeze paper mode**
   - rewrite Abstract, Introduction, `§7.3`, `§9`, and Conclusion so that C1 has an explicit empirical status.

At the moment the manuscript mixes both modes.

---

## 8. Reproducibility Infrastructure

### Current role
- seal, manifest, claim registry, gates, methodology.

### Strong points
- The governance framework is unusually rigorous.

### Comment
- This material is valuable, but heavy for the main text.
- Depending on venue, much of it might belong in appendices or a reproducibility statement.

### Formalization enhancement
- Keep the claim-tier registry, but separate the **mathematical status** from the **artifact status**.
- Example dimensions:
  - theorem proved,
  - mechanized,
  - exact computation audited,
  - float empirical,
  - conjectural.

---

## 9. The Open Problem — Continuous-Transfer (C1)

### Current role
- conjecture statement, decision rule, then later empirical verdict.

### Strengths
- Very strong falsification protocol.
- Good emphasis on publishability of both PASS and KILL branches.

### Major editorial/formalization problems
1. **Section title says open problem**, but `§9.E` gives a frozen empirical verdict.
2. **Original substrate is admitted to be vacuous**, which is a major scientific correction and should be elevated in prominence.
3. **The distinction between architectural dichotomy and literal C1 verdict is subtle and easy to lose.**

### Recommended enhancement
Split §9 into two separate sections:

- **9. Conjecture C1 and protocol**
  - statement, hypotheses, decision rule, cost cap.

- **10. Empirical status of C1 as of 2026-05-30**
  - substrate correction,
  - literal verdict,
  - boundary conditions,
  - actual spend.

This would remove the “open problem but already frozen” clash.

### Formal enhancement
The paper should state explicitly that C1 is **not** a theorem claim. The wording should separate:
- mathematical theorem status,
- empirical support status.

---

## 10. Known Limitations and Honest Narrowings

### Comment
- This is one of the strongest sections in the paper.
- It improves credibility.

### Editorial enhancement
- Move the biggest limitation — the C1 substrate vacuity correction — forward into the C1 section itself and cross-reference here, not vice versa.

---

## 11. Conclusion

### Current role
- recaps theorem, witnesses, and C1 status.

### Main issue
- Must be synchronized with whichever C1 narrative the paper adopts.

### Recommended enhancement
Use a rigid three-part conclusion:
1. theorem proved,
2. what is mechanized / exact-audited,
3. what remains empirical / conjectural.

---

## Appendix A — Proof of Theorem 1

### Current proof skeleton
- setup with `q_C`, `P_C`, `eps*`
- upper bound via scalar inequality
- lower bound via “per-cell Fano” aggregated over cells
- invert binary entropy

### Strong points
- The proof is short.
- Tightness examples are helpful.

### Formalization enhancements
1. Replace “per-cell Fano” with the more transparent binary-Jensen derivation.
2. Add a one-line exact identity:
   - `DIG = sum_C q_C H_bin(e_C)` with `e_C = min(P_C,1-P_C)`.
3. If desired, separate theorem and proof into:
   - scalar inequality lemma,
   - Jensen lemma,
   - sandwich theorem.

That decomposition will also make mechanization easier.

---

## Appendices C-F

### Comment
- Valuable as audit/documentation appendices.
- Appendix C should be updated so its claim index includes the later C1-freeze claims if those remain in scope.

### Minor editorial note
- Ensure all references to reproducibility contracts, PDF determinism, and byte-identity use the same narrowed wording everywhere.

---

## Highest-priority formalization upgrades across the whole paper

1. **Resolve the C1 status contradiction globally.**
2. **Define admissible architecture family explicitly.**
3. **Split the current Theorem 1 package into a pure partition theorem and an architecture factorization theorem.**
4. **Promote monotonicity under refinement to a theorem.**
5. **Tighten Corollary 3.1 with an induction-style proof modeled on Xu/Morris.**
6. **Sharpen the proved / mechanized / exact-audited / float / conjectural distinctions.**
7. **Reduce theorem clutter in the abstract and introduction.**

These changes would materially improve both mathematical clarity and editorial coherence.