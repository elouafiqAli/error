# Editorial improvement proposal for `PAPER-ARXIV.md`

This memo turns the chapter-by-chapter review into a concrete editorial action plan.

---

## A. Mandatory consistency fixes

### A1. Choose a single C1 narrative

The manuscript currently mixes two incompatible states:

- **State PENDING**
  - Abstract: C1 remains pending real-GPU execution.
  - Introduction: C1 is the headline open problem.
  - `§7.3`: the real science test is deferred / pending.

- **State FROZEN / SUPPORTED-BY-EVIDENCE**
  - `§9.E`: literal §9 rule applied on Stage M; empirical verdict sealed.
  - Conclusion: C1 frozen and supported-by-evidence at `L >= 3` on `anchor_8`.

Pick one state for this paper version.

#### Recommendation
Adopt **post-freeze mode** if the Stage M / literal-verdict artifacts are intended to stay. Then rewrite:
- Abstract
- Introduction
- `§7.3`
- `§9` title and framing
- Conclusion

so that C1 is described as:
- a conjecture mathematically,
- with a sealed empirical status as of 2026-05-30.

### A2. Elevate the substrate correction

The fact that the original vertex-transitive substrate is vacuous for `F_WL` tasks is not a side note; it is central to interpreting C1. It should be announced at the start of the empirical-status subsection, not buried.

---

## B. Recommended theorem refactor

## B1. Replace the current §3 spine with a four-step theorem chain

### Step 1 — Pure partition setup
Define for any finite partition `Pi` of a finite probability space and binary target `f`:
- cell masses `q_C`,
- class posteriors `P_C`,
- partition entropy `DIG(f | Pi)`,
- Bayes partition error `eps*_Pi`.

### Step 2 — Prove the pure partition theorem
**Theorem (Partition Bayes-entropy sandwich).**
For any finite partition `Pi` and binary task `f`,
`H_bin^{-1}(DIG(f|Pi)) <= eps*_Pi <= DIG(f|Pi)/2`.

This theorem does **not** need:
- graphs,
- WL,
- admissible architectures,
- `f in F_WL(G)`.

### Step 3 — Add the structural proposition
**Proposition (Architecture factorization).**
Every depth-`L` admissible MPNN of family `A` is constant on cells of `Pi_A(G,L)`.

This is where the WL/LossyWL assumptions belong.

### Step 4 — Instantiate to PA-MPC
**Corollary.**
For `Pi = Pi_A(G,L)`, PA-MPC bounds the irreducible partition-measurable error of every admissible depth-`L` predictor.

This separation is cleaner, more reusable, and easier to mechanize.

## B2. Add refinement monotonicity as a theorem, not an experiment

Suggested statement:

**Proposition (Refinement monotonicity).** If `Pi'` refines `Pi`, then
- `DIG(f|Pi') <= DIG(f|Pi)`,
- `eps*_{Pi'} <= eps*_{Pi}`.

This proposition would support E03 formally and convert E03 into an exact computation audit rather than a pseudo-theory section.

## B3. Define admissibility explicitly

Suggested contents of the definition:
- initial observables determined exactly by `Pi_A^(0)`;
- shared local update rule across vertices;
- permutation invariance over neighbor multisets;
- no extra vertex identifiers beyond the declared observables;
- depth-`L` output depends only on the depth-`L` rooted colored neighborhood generated from `Pi_A^(0)`.

This definition is needed for Corollary 3.1 to be a theorem-level statement.

---

## C. Proof-writing improvements

## C1. Simplify the lower-bound proof

Current wording: “per-cell Fano, aggregated by mass.”

Cleaner proof:
1. For each cell define `e_C = min(P_C,1-P_C)`.
2. Note `H_bin(P_C) = H_bin(e_C)` exactly.
3. Therefore `DIG = sum_C q_C H_bin(e_C)`.
4. By concavity of `H_bin`,
   `DIG <= H_bin(sum_C q_C e_C) = H_bin(eps*)`.
5. Invert on `[0,1/2]`.

This is both simpler and more obviously tailored to the binary partition setting.

## C2. Upgrade the architecture-factorization proof

Current proof of Corollary 3.1 is one sentence.

Better proof template, following Xu/Morris:
- Induct on depth.
- Base case: same cell in `Pi_A^(0)` means same initial observable state.
- Step: if previous-layer hidden states agree cellwise and updates are shared + permutation invariant, then the next-layer states agree.
- Conclude that outputs are constant on cells of `Pi_A(G,L)`.

This would turn a plausible claim into a reusable theorem component.

## C3. Separate theorem statements from status commentary

Avoid embedding too much artifact/status prose directly inside theorem sections. Put trust-tier and witness status in small boxed notes or in a theorem-status table.

---

## D. Section-by-section editorial restructure

## D1. Suggested main-text order

1. Abstract
2. Introduction
3. Related work
4. Theory
   - Definitions
   - Partition theorem
   - Architecture factorization
   - PA-MPC corollaries
   - Scope remarks
5. Exact finite-anchor audits
6. Lean witness
7. Float/pilot experiments
8. Reproducibility infrastructure
9. Conjecture C1 and protocol
10. Empirical status of C1 (if post-freeze mode)
11. Limitations
12. Conclusion

This removes conjecture registry clutter from the core proof section.

## D2. Suggested abstract skeleton

A possible editorial skeleton:

1. *Definition sentence.*
   “We define partition-aware message-passing complexity (PA-MPC) as ...”
2. *Theorem sentence.*
   “For any finite partition and binary task, the partition Bayes error satisfies ... ; instantiating with the LossyWL-induced depth partition yields the PA-MPC bridge for admissible depth-`L` MPNNs.”
3. *Verification sentence.*
   “We provide a finite-anchor Lean witness and exact-rational computational audits ...”
4. *Empirical sentence.*
   Either:
   - pending/open mode, or
   - frozen empirical-status mode,
   but not both.

## D3. Suggested introduction skeleton

- Paragraph 1: problem and existing WL ceiling.
- Paragraph 2: why model-indexed MPC is insufficient.
- Paragraph 3: core theorem in one sentence.
- Paragraph 4: what is proved vs audited vs empirical.
- Paragraph 5: roadmap.

---

## E. Specific constructs that should be made more formal

## E1. `LossyWL`
At minimum, provide the exact property used later:
- refinement of the observable partition by depth,
- compatibility with admissible message-passing families,
- stable partition notion.

## E2. `F_WL(G)`
Clarify that it is needed for the **architectural interpretation of what can be represented**, not for the partition sandwich theorem itself.

## E3. Trust tiers
The tier system is useful, but the paper should distinguish two orthogonal dimensions:
- **mathematical status**: theorem / conjecture / empirical claim,
- **verification status**: paper proof / Lean / exact computation / float.

A 2-axis table would be much clearer than a single label stream.

---

## F. Concrete “must-add” propositions

### F1. Refinement monotonicity
As above.

### F2. Zero-gap equivalence
Already present as Lemma 3.1; keep it.

### F3. Optional stable-partition proposition
If valid under your imported LossyWL facts:
- `Pi_A(G,L)` refines monotonically toward a stable partition,
- once stable, PA-MPC no longer changes with depth.

This would turn parts of E03 from empirical observation into theorem-backed illustration.

---

## G. Final priority list

### Highest priority
1. Resolve the C1 contradiction globally.
2. Define admissibility.
3. Split Theorem 1 into partition theorem + architecture proposition.
4. Add refinement monotonicity theorem.

### Medium priority
5. Move conjecture registry out of the middle of Theory.
6. Rewrite Appendix A with the Jensen proof.
7. Add theorem/mechanization status table.

### Lower priority but high value
8. Tighten abstract and introduction.
9. Compress reproducibility logistics in main text.
10. Turn some experiment sections into appendical support if venue pressure requires it.

---

## H. Bottom-line editorial verdict

The paper already has a strong core theorem and unusually honest artifact governance. The main weaknesses are **not** in the theorem idea; they are in **formal modularity and narrative consistency**. If you:
- isolate the pure partition theorem,
- formalize architecture admissibility and factorization separately,
- promote monotonicity to a theorem,
- and resolve the C1 chronology/status conflicts,

then the paper will read much more like a clean theorem paper with audited computational support, rather than a theorem paper and a lab notebook partially interleaved.