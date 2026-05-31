# Fix proposal — attribute §3.2 / Appendix A to classical literature

**Date:** 2026-05-31
**Status:** proposal; default Option A applied to `PAPER-ARXIV.md` on this
date. Switch by undoing and selecting B or C.
**Companion:** `13-bayes-entropy-sandwich-literature-note.md`.

The reviewer asked whether $\varepsilon^{*}_\Pi$ and the sandwich are
named in the literature. Answer: yes (Fano 1961; Hellman & Raviv 1970;
Feder & Merhav 1994; Devroye–Györfi–Lugosi 1996), but the *partitioned*
framing and the *PA-MPC* corollary are ours. The paper currently makes
no attribution, which a reviewer is likely to flag. Three options below;
the recommendation is **Option A**.

---

## Option A — concise inline attribution (recommended, **applied**)

**Where:** one sentence after Theorem 1 in §3.2; one sentence in
Appendix A near (A.2) and (A.6); six bibliography entries.

**Why preferred:** smallest editorial footprint, signals scholarship,
keeps the spine readable, leaves room for the contribution claim
(Corollary 3.4) to stand out.

**Diffs (applied 2026-05-31):**

§3.2, immediately after the upper/lower bound sketch:

> *Provenance.* The upper bound is the Hellman–Raviv inequality (Hellman
> & Raviv 1970); the lower bound is Fano's inequality in its sharp
> binary form (Fano 1961; Cover & Thomas 2006, Thm 2.10.1), with the
> sharpest two-sided packaging due to Feder & Merhav (1994). Under
> $\sigma(\Pi)$, $\varepsilon^{*}_\Pi$ is the Bayes risk of $f$ given the
> coarsened feature in the sense of Devroye–Györfi–Lugosi (1996, §2.1).
> The contribution of Theorem 1 is not the inequalities themselves but
> their **partition-indexed packaging** — applied in Corollary 3.4 to
> $\Pi_{\mathcal{A}}(G, L)$, this is the bridge from textbook
> information theory to depth-$L$ message-passing expressivity.

Appendix A, after (A.2):

> ((A.1)–(A.2) is the **Hellman–Raviv (1970) upper bound** on Bayes
> error in its binary form; see also Cover & Thomas (2006), §2.10.)

Appendix A, after (A.6):

> ((A.3)–(A.6) is **Fano's inequality** in its sharp binary form (Fano
> 1961; Feder & Merhav 1994). The deterministic-coarsening case of the
> **data-processing inequality** (Cover & Thomas 2006, Thm 2.8.1) gives
> Proposition 3.2 as a corollary; we keep the elementary
> Jensen-on-$H_{\mathrm{bin}}$ proof for self-containedness.)

Appendix A, end of variance discussion (if any), add:

> The variance form $\mathbb{E}[\mathrm{Var}(f \mid \Pi)]$ coincides
> with the **expected conditional Gini impurity** (Breiman et al. 1984)
> for binary $f$, and $\varepsilon^{*}_\Pi \leq 2 \cdot \mathbb{E}[\mathrm{Var}(f \mid \Pi)]$
> is the **Gini–Bayes inequality**; we use the variance form in Lean
> because $P_C(1 - P_C) \in \mathbb{Q}$ when $P_C \in \mathbb{Q}$.

References (append, in alphabetical order):

```
- Breiman, L., Friedman, J. H., Olshen, R. A. & Stone, C. J. (1984).
  *Classification and Regression Trees.* Wadsworth.
- Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory*,
  2nd ed. Wiley.
- Devroye, L., Györfi, L. & Lugosi, G. (1996). *A Probabilistic Theory
  of Pattern Recognition.* Springer.
- Fano, R. M. (1961). *Transmission of Information.* MIT Press.
- Feder, M. & Merhav, N. (1994). Relations between entropy and error
  probability. *IEEE Trans. Inf. Theory* 40(1):259–266.
- Hellman, M. E. & Raviv, J. (1970). Probability of error, equivocation,
  and the Chernoff bound. *IEEE Trans. Inf. Theory* 16(4):368–372.
```

---

## Option B — historical paragraph in §3.2

**Where:** a separate "Historical note" paragraph between Theorem 1 and
Proposition 3.2.

**Why one might prefer it:** lets the reader see the whole genealogy in
one place; useful if this paper is read by reviewers unfamiliar with the
information-theory literature.

**Trade-off:** breaks the proof spine's rhythm (Thm 1 → Prop 3.2 →
Prop 3.3 → Cor 3.4). The reviewer Editorial Improvement Proposal
(`11-editorial-improvement-proposal.md`) explicitly recommended **not**
inserting paragraphs between spine results.

Sketch:

> *Historical note.* The two inequalities in Theorem 1 each have long
> pedigrees. The upper bound $\varepsilon^{*} \leq \tfrac{1}{2} H(Y \mid X)$
> is due to Hellman & Raviv (1970), with antecedents in Kovalevskij
> (1968). The lower bound originates in Fano (1961) and was sharpened
> in the binary case by Feder & Merhav (1994), who present the pair as
> a two-sided bracket (their Thm 1 and §III). The use of $\sigma(\Pi)$
> as the conditioning σ-algebra is standard in the
> Devroye–Györfi–Lugosi (1996) treatment of Bayes risk over coarsened
> features. The novelty of Theorem 1, then, lies neither in the upper
> nor the lower side, but in instantiating the bracket at
> $\Pi = \Pi_{\mathcal{A}}(G, L)$ (Corollary 3.4) and proving — via
> Proposition 3.3 — that any depth-$L$ admissible message-passing
> predictor is $\sigma(\Pi)$-measurable.

---

## Option C — footnote-only attribution

**Where:** a footnote at the title of Theorem 1.

**Why one might prefer it:** absolute minimum body-text disruption.

**Trade-off:** Markdown footnotes render unreliably on arXiv-HTML and
GitHub previews; reviewers often miss footnotes. Loses the chance to
**actively claim** the partition-indexed framing as the contribution.

Sketch:

> **Theorem 1** (Partition Bayes-entropy sandwich).[^fano-hr]
>
> [^fano-hr]: Upper: Hellman & Raviv (1970). Lower: Fano (1961),
> binary-sharp form in Feder & Merhav (1994).

---

## Decision matrix

| Criterion | A (inline) | B (paragraph) | C (footnote) |
|---|---|---|---|
| Scholarly attribution | ✔ | ✔✔ | ✔ |
| Preserves spine rhythm | ✔ | ✘ | ✔✔ |
| Claims our contribution | ✔ | ✔✔ | ✘ |
| Renders cleanly on arXiv-HTML | ✔ | ✔ | ✘ |
| Editorial cost | low | medium | minimal |

**Default applied:** A.

To switch to B or C: revert the §3.2 and Appendix A edits of 2026-05-31,
then paste the corresponding sketch above.

---

## Addendum (2026-05-31) — naming of $\varepsilon^{*}_\Pi$

The first round of attribution fixes left the bespoke phrase
"**Bayes-optimal partition-measurable error**" in place at the first
definition (§3.2 line ~235) and in Appendix A (line ~929). Reviewer
asked: are there standard alternatives?

### Options

| #   | Name                                                  | Pedigree            | Precision                 | Community recognition | Fit with paper          |
| --- | ----------------------------------------------------- | ------------------- | ------------------------- | --------------------- | ----------------------- |
| 1   | Bayes-optimal partition-measurable error (original)   | bespoke             | high                      | low                   | parallel to PA-MPC      |
| 2   | Conditional Bayes error                               | pattern-rec, common | medium (which σ-algebra?) | **high** in ML        | ambiguous               |
| 3   | Expected minimum-posterior error                      | descriptive         | high                      | none                  | clunky                  |
| 4   | Bayes risk under $\sigma(\Pi)$ / $L^{*}(\sigma(\Pi))$ | DGL 1996 §2.1       | **highest**               | medium                | notation-heavy          |
| 5   | **Partition Bayes error**                             | hybrid, transparent | high                      | medium-high           | **best fit**            |
| 6   | Coarsened Bayes risk                                  | Le Cam / Blackwell  | medium                    | low in ML             | "coarsened" too general |

### Decision: Option 5 — *partition Bayes error*

Rationale:
1. **Lexical consistency.** §3.2 is titled "Partition Bayes-Entropy
   Sandwich"; "partition Bayes error" makes the noun phrases align
   (*partition* × {*entropy*, *error*}).
2. **Community recognition.** "Bayes error" is universal in ML; the
   one-word qualifier *partition* says exactly what's conditioned on.
3. **Precision retained** without dragging σ-algebras into every formula.
4. **One gloss at first use** anchors it to the DGL convention:

   > Equivalently, $\varepsilon^{*}_\Pi$ is the Bayes risk of $f$ under
   > the $\sigma$-algebra $\sigma(\Pi)$ generated by the partition
   > (Devroye, Györfi & Lugosi 1996, §2.1); we use the shorter name
   > *partition Bayes error* throughout.

### Diff applied (2026-05-31)

- §3.2 paragraph header: "Bayes-optimal partition-measurable error" →
  "Partition Bayes error", with the DGL gloss appended.
- §3.2 Operational-reading paragraph: "partition-level Bayes error" →
  "partition Bayes error".
- Appendix A Setup line: "be the Bayes-optimal partition-measurable
  error" → "be the partition Bayes error (§3.2)".

The symbol $\varepsilon^{*}_\Pi$ is unchanged.

### Alternatives kept on the shelf

If a future revision wants to maximise stats/IT-community recognition
over GNN-community recognition, switch to Option 4 (*Bayes risk under
$\sigma(\Pi)$*, write $L^{*}(\Pi)$ instead of $\varepsilon^{*}_\Pi$).
This would require: rename symbol throughout; reword §3.2 paragraph;
update Lean module names. Not recommended unless a reviewer specifically
asks.

Option 2 (*conditional Bayes error*) was rejected because in
pattern-recognition usage it conditions on the full feature vector $X$,
not on a coarsening; using it here would invite the wrong default
reading.
