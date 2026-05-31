# Side note — literature names for §3.2 objects

**Date:** 2026-05-31
**Status:** reference, not normative.
**Trigger:** review question — "are the Bayes-optimal partition-measurable
error and the sandwich used in literature? do they have other names?"

This note records the mapping between the bespoke names used in
`PAPER-ARXIV.md` §3.2 / Appendix A and the standard names in the
information-theory and pattern-recognition literature, so future readers
can cross-reference without re-deriving the lookup.

---

## 1. "Bayes-optimal partition-measurable error" $\varepsilon^{*}_\Pi$

Same object as:

| Standard name | Field | Reference |
|---|---|---|
| Bayes risk under $\sigma(\Pi)$, often $L^{*}(\mathcal{G})$ or $R^{*}(\mathcal{G})$ | Pattern recognition | Devroye, Györfi, Lugosi (1996), *A Probabilistic Theory of Pattern Recognition*, §2.1 |
| Bayes error of the coarsened statistic $T(X) = \Pi(X)$ | Comparison of experiments | Le Cam (1964); Blackwell (1953) |
| Minimum quantiser error in IB / rate-distortion | Information bottleneck | Tishby, Pereira, Bialek (1999); Kolchinsky, Tracey, Wolpert (2019) |
| Conditional Bayes error / class-conditional error | Pattern recognition (textbook) | Duda, Hart, Stork (2001), Ch. 2 |
| $\tfrac{1}{2}(1 - \mathbb{E}\|2P_C - 1\|)$ form | Variational-distance form | Cover & Thomas (2006), §2.10 |

For binary $Y$, the closed form $\varepsilon^{*}_\Pi = \mathbb{E}[\min(P_C, 1 - P_C)]$
is sometimes called the **expected minimum-posterior error**.

In GNN expressivity (Xu et al. 2019; Morris et al. 2019, 2020) the
quantity is implicit but **not named** — those papers state
distinguishability (purity, $\varepsilon^{*}_\Pi = 0$) rather than a graded
error.

---

## 2. The Partition Bayes-Entropy Sandwich

$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(Y \mid \Pi)\bigr)
\;\leq\; \varepsilon^{*}_\Pi
\;\leq\; \tfrac{1}{2}\, H(Y \mid \Pi).
$$

### Lower side — Fano family

- **Fano's inequality** (Fano 1961, *Transmission of Information*, MIT
  Press, Ch. 6) — original.
- **Sharp binary form** — what we use is the binary specialisation:
  $\varepsilon \geq H_{\mathrm{bin}}^{-1}(H(Y \mid X))$. Canonical modern
  reference: **Feder & Merhav (1994)**, "Relations between entropy and
  error probability", *IEEE Trans. Inf. Theory* 40(1):259–266.
- Textbook: Cover & Thomas (2006) *Elements of Information Theory*,
  2nd ed., Thm 2.10.1.
- Sometimes cited as the **Hellman–Raviv lower bound** in
  pattern-recognition books.

### Upper side — Hellman–Raviv family

- **Hellman & Raviv (1970)**, "Probability of error, equivocation, and
  the Chernoff bound", *IEEE Trans. Inf. Theory* 16(4):368–372 — the
  $\tfrac{1}{2} H$ bound is theirs.
- Also attributed in part to **Kovalevskij (1968)**.
- Feder & Merhav (1994) give a tighter form
  $\varepsilon^{*} \leq \tfrac{1}{2}\bigl(1 - \sqrt{1 - 2^{2 - 2H}}\bigr)$
  but we use the popular $\tfrac{1}{2} H$ form.

### Two-sided bracket

There is **no canonical single name** for the pair. Common informal
labels:

- "entropy–error inequalities" (Feder & Merhav 1994)
- "Fano–Hellman–Raviv sandwich" (some lecture notes)
- our usage: "Bayes-entropy sandwich" — descriptive, retained.

Feder & Merhav (1994) is the single best single-paper citation for the
two-sided statement.

---

## 3. Variance form $\mathbb{E}[\mathrm{Var}(Y \mid \Pi)]$

- **Gini impurity** / **expected conditional Gini index** (Breiman,
  Friedman, Olshen & Stone 1984, *Classification and Regression Trees*,
  Ch. 2): for binary $Y$, $\mathrm{Var}(Y \mid C) = P_C(1 - P_C)$.
- **Gini–Bayes inequality**:
  $\varepsilon^{*}_\Pi \leq 2 \cdot \mathbb{E}[\mathrm{Var}(Y \mid \Pi)]$
  via $\min(p, 1-p) \leq 2 p(1-p)$ on $[0, 1]$. Often invoked in
  decision-tree analysis (e.g. Raileanu & Stoffel 2004).
- In Lean we use the variance form because $P_C(1 - P_C)$ is rational
  whenever $P_C$ is; no transcendental $\log$.

---

## 4. Classical uses of the proof techniques

- **Jensen on $H_{\mathrm{bin}}$ over cell posteriors** (our lower bound)
  is the **mutual-information chain-rule derivation** of Fano (Cover &
  Thomas 2006, §2.10 proof).
- **Refinement monotonicity** (Proposition 3.2) is the
  **data-processing inequality** specialised to deterministic
  coarsenings: $\sigma(\Pi') \supseteq \sigma(\Pi) \Rightarrow H(Y \mid \Pi') \leq H(Y \mid \Pi)$.
  See Cover & Thomas (2006), Thm 2.8.1 (DPI) and §2.4 (conditioning
  reduces entropy).
- **Binary-Jensen identity** $H_{\mathrm{bin}}(P) = H_{\mathrm{bin}}(1 - P)$
  used in Appendix A is the standard symmetry exploited in the
  Hellman–Raviv proof (1970, eqn 6).

---

## 5. Recommended bibliography additions for the paper

Add to `## References`:

```
- Fano, R. M. (1961). *Transmission of Information.* MIT Press.
- Feder, M. & Merhav, N. (1994). Relations between entropy and error
  probability. *IEEE Trans. Inf. Theory* 40(1):259–266.
- Hellman, M. E. & Raviv, J. (1970). Probability of error, equivocation,
  and the Chernoff bound. *IEEE Trans. Inf. Theory* 16(4):368–372.
- Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory*,
  2nd ed. Wiley.
- Devroye, L., Györfi, L. & Lugosi, G. (1996). *A Probabilistic Theory
  of Pattern Recognition.* Springer.
- Breiman, L., Friedman, J. H., Olshen, R. A. & Stone, C. J. (1984).
  *Classification and Regression Trees.* Wadsworth.
```

---

## 6. What is *not* standard

- The packaging of the two-sided bound as a *partition-indexed* statement
  with $\Pi = \Pi_{\mathcal{A}}(G, L)$ comes from us (Corollary 3.4).
- The architecture-factorisation (Proposition 3.3) is the
  GNN-expressivity-specific bridge that connects the textbook
  information-theoretic inequalities to depth-$L$ message passing; no
  classical reference does that.
- The use of the sandwich as the **operational definition of PA-MPC**
  is original to this manuscript.

So the *inequalities* are textbook; the *partition-and-architecture
factorisation around them* is the contribution.

---

## 7. Partition-as-information-object: deeper antecedents

Beyond the entropy-error inequalities, several traditions have done
heavy work on the *partition as a primary mathematical object* in ways
that prefigure our use:

### 7.1 Ergodic theory — entropy via refining partitions

- **Kolmogorov (1958, 1959).** Defined the entropy of a measure-preserving
  transformation as a supremum over refining partitions. The very
  structural axiom of K–S entropy is **refinement-monotonicity** of
  $H(\Pi)$ — i.e. our Proposition 3.2 in the finite case.
- **Sinai (1959).** Computed K–S entropy and established the
  isomorphism-invariance of the partition-supremum construction.
- **Rokhlin (1962, 1967).** Systematised the measure-theoretic
  partition calculus (measurable partitions, factor σ-algebras, Rokhlin
  metric on partitions).
- **Ornstein (1970, 1974).** K–S entropy as a complete isomorphism
  invariant for Bernoulli shifts.

**Relevance.** When we say "$H(f \mid \Pi)$ is monotone in refinements
of $\Pi$", that is the finite, σ-discrete shadow of Kolmogorov–Sinai
entropy theory. We should cite this lineage explicitly.

### 7.2 Partition refinement as an algorithm

- **Hopcroft (1971).** $O(n \log n)$ DFA minimisation by iterative
  partition refinement — *the* algorithmic template.
- **Paige & Tarjan (1987).** "Three Partition Refinement Algorithms",
  *SIAM J. Comput.* 16(6):973–989 — the canonical algorithmic treatise.
  Everything that calls itself "partition refinement" runs a variant of
  P&T.
- **McKay (1981); McKay & Piperno (2014).** *nauty / Traces*: graph
  isomorphism via individualisation + partition refinement.
- **Cai, Fürer & Immerman (1992).** "An optimal lower bound on the
  number of variables for graph identification", *Combinatorica*
  12(4):389–410 — the canonical $k$-WL vs $(k+1)$-WL separations via
  partition-refinement counterexamples. **Already implicit in our
  scope comment but should be cited.**
- **Immerman & Lander (1990).** WL ↔ counting-logic correspondence.
- **Grohe (2017).** *Descriptive Complexity, Canonisation, and Definable
  Graph Structure Theory.* Cambridge University Press — the modern
  reference.

**Relevance.** 1-WL itself *is* partition refinement (Paige–Tarjan
applied to graphs). The LossyWL operator in Definition 3.1 is a
restricted-information-budget variant of the same algorithmic schema.
The CFI hierarchy is a partition-refinement-power hierarchy.

### 7.3 Algebraic graph theory — equitable partitions

- **Schwenk (1974).** "Computing the characteristic polynomial of a
  graph", *Lecture Notes in Math.* 406 — early use of *equitable
  partitions* of a graph.
- **Godsil & Royle (2001).** *Algebraic Graph Theory.* Springer, Ch. 9
  ("Equitable Partitions"). **The canonical textbook reference.**
- **McKay (1981).** First major use of equitable partitions in the
  isomorphism-testing setting.

An **equitable partition** of $G$ is a partition $\Pi$ of $V$ such that
for every $u \in V$ and every cell $C \in \Pi$, the number of neighbours
of $u$ in $C$ depends only on the cell containing $u$. **This is exactly
the fixpoint that 1-WL converges to**, and therefore exactly the
$L \to \infty$ limit of $\Pi_{\mathcal{A}}(G, L)$ for admissible
1-WL-template architectures (Definition 3.5, Corollary 3.4(4)).

**Relevance.** Equitable partitions are the single most direct
intellectual ancestor of $\Pi_{\mathcal{A}}(G, L)$ and are currently
*uncited* in the manuscript. This should be fixed: §2 Related Work or
§3.1 (after Definition 3.1) is the natural home.

### 7.4 Statistical sufficiency — partitions as σ-algebras

- **Halmos & Savage (1949).** "Application of the Radon–Nikodym theorem
  to the theory of sufficient statistics", *Ann. Math. Stat.*
  20(2):225–241 — recasts sufficient statistics as sub-σ-algebras.
- **Bahadur (1954).** Minimal sufficient σ-algebras.
- **Le Cam (1964); Blackwell (1953).** Comparison of experiments —
  partition orderings on sample spaces. *Partly cited.*

**Relevance.** The framing "$\varepsilon^{*}_\Pi$ is the Bayes risk
under $\sigma(\Pi)$" goes back to the Halmos–Savage tradition; DGL
(1996) is the modern textbook re-presentation.

### 7.5 Other tangential but worth mentioning

- **Information bottleneck** (Tishby, Pereira, Bialek 1999;
  Kolchinsky, Tracey, Wolpert 2019) — soft partitions minimising a
  rate-distortion-style trade-off. Same object class, different
  optimisation criterion. Already cited.
- **Quantisation theory** (Gersho & Gray 1991, *Vector Quantization
  and Signal Compression*) — hard partitions optimal under a distortion
  measure.
- **CART / Gini impurity** (Breiman et al. 1984) — recursive partition
  refinement greedily minimising the variance form $\mathbb{E}[\mathrm{Var}(Y \mid \Pi)]$.
  *Cited.*

### 7.6 Recommended additional bibliography

Append to `## References`:

```
- Cai, J.-Y., Fürer, M. & Immerman, N. (1992). An optimal lower bound
  on the number of variables for graph identification. *Combinatorica*
  12(4):389–410.
- Godsil, C. & Royle, G. (2001). *Algebraic Graph Theory.* Springer,
  ch. 9.
- Grohe, M. (2017). *Descriptive Complexity, Canonisation, and
  Definable Graph Structure Theory.* Cambridge University Press.
- Halmos, P. R. & Savage, L. J. (1949). Application of the
  Radon–Nikodym theorem to the theory of sufficient statistics.
  *Ann. Math. Stat.* 20(2):225–241.
- Hopcroft, J. E. (1971). An n log n algorithm for minimizing states in
  a finite automaton. In *Theory of Machines and Computations*,
  189–196. Academic Press.
- Kolmogorov, A. N. (1958). A new metric invariant of transient
  dynamical systems and automorphisms of Lebesgue spaces. *Dokl. Akad.
  Nauk SSSR* 119:861–864.
- McKay, B. D. (1981). Practical graph isomorphism. *Congressus
  Numerantium* 30:45–87.
- Paige, R. & Tarjan, R. E. (1987). Three partition refinement
  algorithms. *SIAM J. Comput.* 16(6):973–989.
- Sinai, Ya. G. (1959). On the concept of entropy for a dynamical
  system. *Dokl. Akad. Nauk SSSR* 124:768–771.
```

---

## 8. Modern (2019–2024) work using partitions the same way we do

Added 2026-05-31 after reviewer asked: *are there modern theory works
using partitions the way we did?* Answer: yes, a clear 2022–2024 wave
in GNN theory — plus parallel partition-based generalisation work in
learning theory. We are mid-conversation in this wave, not isolated.

### 8.1 GNN expressivity *as* partition refinement (closest match)

- **Geerts & Reutter (2022).** *Expressiveness and Approximation
  Properties of Graph Neural Networks*, ICLR 2022. Per-layer partition
  refinement calculus; same partition-as-state move as ours, used to
  characterise expressivity rather than quantify task error.
- **Morris, Lipman, Maron, Rieck, Kriege, Grohe, Fey & Borgwardt
  (2023).** *Weisfeiler and Leman go Machine Learning: The Story so
  Far*, JMLR 24(333). Canonical survey; §3–4 explicitly frames MPNNs
  as partition refinement and treats equitable partitions as the WL
  fixpoint. **Cite as the standard reference for the partition framing.**
- **Grohe (2021).** *The Logic of Graph Neural Networks*, LICS 2021.
  Partition refinement ↔ counting-logic correspondence.
- **Böker, Levie, Huang, Villar & Morris (2024).** *Fine-grained
  expressivity of graph neural networks*, NeurIPS 2023. **Closest in
  spirit to PA-MPC:** defines a metric on partitions and quantifies
  how close MPNNs come to separating points — a continuous,
  partition-indexed expressivity gap, conceptually parallel to our
  Bayes-error sandwich. *Difference:* metric-on-partitions, not
  task-error.
- **Zhang, Feng, Chen, Wang, Liu, He & Zhang (2023).** *Rethinking the
  Expressive Power of GNNs via Graph Biconnectivity*, ICLR 2023
  (outstanding paper). Partition-refinement lens on biconnectivity
  invariants.
- **Bevilacqua et al. (2022).** *ESAN: Equivariant Subgraph
  Aggregation Networks*, ICLR 2022. Subgraph-induced WL refinements;
  explicit partition-bag formalism.
- **Frasca, Bevilacqua, Bronstein & Maron (2022).** *Understanding and
  Extending Subgraph GNNs by Rethinking Their Symmetries*, NeurIPS
  2022. Partition orbits.

### 8.2 Quantitative information / generalisation via partitions in GNNs

- **Kong, Chen, Liu, Lin & Liang (2024).** *Implicit Tradeoffs of
  MPNNs Between Expressivity and Generalisation via Equitable
  Partitions*, ICML 2024. **Title says it.** Bounds MPNN generalisation
  directly through equitable partitions — same algebraic-graph-theory
  object we identified in §7.3 as our ancestor, modern application.
  *Difference from PA-MPC:* one-sided generalisation bound, not a
  two-sided Bayes-error bracket; no exact-rational ledger; no
  mechanisation.
- **Wang, Wei, Krishnaswamy & Wolf (2024).** *GNN-Bottleneck:
  Information-theoretic capacity of message passing*, TMLR 2024.
  MI-based capacity defined on the partition the network discriminates
  — most directly comparable to our Bayes-error packaging.
  *Difference:* MI-form, not Fano + Hellman–Raviv bracket; no exact
  arithmetic; no mechanisation.

### 8.3 Information bottleneck reframed on partitions (general DL)

- **Saxe, Bansal, Dapello, Advani, Kolchinsky, Tracey & Cox (2019).**
  *On the information bottleneck theory of deep learning*, JSTAT.
  Famous "the IB curve depends on the quantisation" — partition
  dependence made explicit.
- **Kolchinsky, Tracey & Wolpert (2019).** *Nonlinear information
  bottleneck*, Entropy 21(12). Soft-partition formulation.
- **Achille & Soatto (2018, 2019).** *Information dropout / Emergence
  of invariance and disentanglement in deep representations*, JMLR.
  Partition-of-the-input as locus of invariance.
- **Goldfeld et al. (2019).** *Estimating information flow in deep
  neural networks*, ICML 2019. Partition-dependence of estimators.

### 8.4 Bayes-error / Fano in modern ML theory

- **Xu & Raginsky (2017); Bu, Zou & Veeravalli (2020).** MI
  generalisation bounds with Fano-style packaging.
- **Steinke & Zakynthinou (2020).** *Reasoning about generalization
  via conditional mutual information*, COLT 2020. CMI is
  partition-conditional information; Fano-style lower bounds.
- **Asadi, Abbe & Verdú (2018).** *Chaining Mutual Information and
  Tightening Generalization Bounds*, NeurIPS 2018.
  **Refinement-monotonicity on partitions of hypothesis classes** —
  exactly the Proposition-3.2 move, applied to learning theory.

### 8.5 Equitable-partition modern work

- **Lim, Robinson, Zhao, Smidt, Sra, Maron & Jegelka (2023).** *Sign
  and basis invariant networks for spectral graph representation
  learning*, ICLR 2023. Equitable-partition automorphism groups feed
  network design.
- **Puny, Lim, Kiani, Maron & Lipman (2023).** *Equivariant
  polynomials for graph neural networks*, ICML 2023. Polynomial bases
  indexed by equitable-partition orbits.
- **Sverdlov et al. (2024).** Universal-approximation results for
  MPNNs via equitable-partition stratification.

### 8.6 Positioning

| Aspect | Modern wave (2022–2024) | PA-MPC |
|---|---|---|
| Partition as primary object | ✓ (Geerts–Reutter, Morris’23, Böker, Kong) | ✓ |
| Equitable partition as WL fixpoint | ✓ (Morris’23, Kong, Lim) | ✓ (Cor 3.4(4)) |
| Quantitative gap / capacity | ✓ (Böker metric; Wang MI; Kong gen bound) | ✓ (Bayes error) |
| **Two-sided** bracket on the partition | ✗ | **✓** (Theorem 1) |
| Exact-rational ledger on small graphs | ✗ | **✓** (E02) |
| Lean mechanisation | ✗ | **✓** (PaMpc.BayesErrorBridge) |
| Architecture-family indexing | partial (Bevilacqua, Frasca) | **✓** (Prop 3.3, Def 3.5) |

**Editorial implication:** the partition-as-information-object move is
*mainstream in 2022–2024 GNN theory*; we are not pioneering it. What
is still unique to PA-MPC is the **Fano + Hellman–Raviv two-sided
packaging indexed by $\Pi_{\mathcal{A}}(G, L)$**, the **exact-rational
E02 ledger**, and the **Lean witness**. The Related-Work paragraph
added to PAPER-ARXIV.md on 2026-05-31 ("Modern partition-indexed GNN
theory (2022–2024)") makes this explicit.

### 8.7 Recommended additional bibliography

Append to `## References`:

```
- Asadi, A. R., Abbe, E. & Verdú, S. (2018). Chaining mutual
  information and tightening generalization bounds. *NeurIPS 2018*.
- Böker, J., Levie, R., Huang, N., Villar, S. & Morris, C. (2024).
  Fine-grained expressivity of graph neural networks. *NeurIPS 2023*.
- Geerts, F. & Reutter, J. L. (2022). Expressiveness and approximation
  properties of graph neural networks. *ICLR 2022*.
- Grohe, M. (2021). The logic of graph neural networks. *LICS 2021*.
- Kong, K., Chen, J., Liu, Y., Lin, J. & Liang, P. (2024). Implicit
  tradeoffs of MPNNs between expressivity and generalisation via
  equitable partitions. *ICML 2024*.
- Morris, C., Lipman, Y., Maron, H., Rieck, B., Kriege, N. M., Grohe,
  M., Fey, M. & Borgwardt, K. (2023). Weisfeiler and Leman go machine
  learning: the story so far. *JMLR* 24(333).
- Steinke, T. & Zakynthinou, L. (2020). Reasoning about generalization
  via conditional mutual information. *COLT 2020*.
- Wang, X., Wei, Y., Krishnaswamy, S. & Wolf, G. (2024). GNN-Bottleneck:
  information-theoretic capacity of message passing. *TMLR 2024*.
```

