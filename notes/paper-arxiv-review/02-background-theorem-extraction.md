# Background theorem extraction from arXiv TeX sources

## Sources read fully

- `background/arXiv-1810.00826v3/{intro,preliminary,framework,method,theory,experiments,conclusion,appendix}.tex`
- `background/arXiv-1810.02244v5/main.tex`

## A. arXiv-1810.00826v3 — *How Powerful are Graph Neural Networks?*

### Core theorem chain

1. **Upper-bound theorem (`method.tex`, Lemma `theorem:upper`)**
   - Any aggregation-based GNN is **at most as powerful as 1-WL** in distinguishing graphs.
   - Proof pattern:
     - If WL does not separate two graphs up to depth `k`, then both graphs have the same multiset of WL labels at every depth `<= k`.
     - By induction, equal WL labels imply equal GNN hidden states.
     - Therefore graph-level readout sees the same multiset of node embeddings and cannot separate the graphs.

2. **Matching-power theorem (`method.tex`, Theorem `theorem:condition`)**
   - If node-update aggregation on neighbor multisets is injective, node-update merge is injective, and graph-level readout is injective, then the GNN is **as powerful as 1-WL** on graphs distinguished by 1-WL.
   - Proof pattern:
     - Inductively construct an injective map from WL labels to hidden states.
     - Use injectivity closure under composition.
     - Distinct WL color multisets imply distinct node-embedding multisets, then distinct graph embeddings.

3. **Countability lemma (`method.tex`, Lemma `theorem:countability`)**
   - If inputs come from a countable feature universe and multisets are bounded-size, hidden-state spaces remain countable.
   - Used to justify exact injective coding arguments.

4. **Universal multiset representation (`method.tex`, Lemma `theorem:sum`)**
   - Sum aggregation can encode bounded-size multisets injectively.
   - Any multiset function factors as `phi(sum_x f(x))`.
   - This is the key constructive reason sum-aggregation + MLP can match WL.

5. **Root-plus-neighborhood injectivity (`method.tex`, Corollary `lemma:gin-wl`)**
   - `(center, multiset(neighbors))` can be encoded injectively by `(1+eps)f(c) + sum_x f(x)` for many `eps`.
   - This yields the GIN update rule.

6. **Negative result for shallow aggregators (`theory.tex`, Lemma `theorem:mlp`)**
   - 1-layer perceptrons are not universal multiset function approximators.
   - Gives explicit multisets that always collide.

7. **Characterization of mean / max (`theory.tex`, Corollaries `theorem:mean` and `theorem:max-pooling`)**
   - Mean identifies distributions/proportions, not exact multisets.
   - Max identifies underlying sets, not multiplicities.

### Editorial lessons useful for `PAPER-ARXIV.md`

- The theorem chain is **modular**: upper bound -> sufficient conditions -> constructive architecture -> failure modes.
- Each theorem carries only the assumptions it needs.
- The appendix proofs use explicit induction on iterations and explicit factorization through labels/multisets.
- Formal claims and empirical claims are sharply separated.

## B. arXiv-1810.02244v5 — *Weisfeiler and Leman Go Neural: Higher-order Graph Neural Networks*

### Core theorem chain

1. **Refinement theorem (Theorem 1 in the appendix)**
   - WL coloring refines the feature partition induced by a 1-GNN:
     - if two vertices have the same WL color at depth `t`, they must have the same GNN feature at depth `t`.
   - Proof pattern:
     - Induction on depth.
     - Same previous colors and same multiset of neighbor colors imply same aggregated features.

2. **Matching theorem (Theorem 2 in the appendix)**
   - There exist weights such that a 1-GNN matches 1-WL exactly.
   - Proof pattern is more constructive than Xu et al.:
     - Replace the standard update by an equivalent refinement form.
     - Build matrices whose row classes encode WL color classes.
     - Use row-independence modulo equality and explicit sign/ReLU constructions.

3. **Higher-order lift (Propositions 3 and 4)**
   - The same refine/match pattern extends from 1-GNN / 1-WL to set-based `k`-GNN / set-based `k`-WL.

### Editorial lessons useful for `PAPER-ARXIV.md`

- When a paper claims that an architecture factors through a partition, it helps to state a **separate refinement/factorization proposition** and prove it by induction.
- Explicit definitions of equivalence/refinement relations make later theorems cleaner.
- Proof obligations are easier to mechanize when the theorem is split into:
  - a purely combinatorial refinement statement,
  - then a model-specific corollary.

## C. Immediate carry-over opportunities for `PAPER-ARXIV.md`

1. Split the current Theorem 1 package into:
   - a **purely information-theoretic partition theorem**, and
   - a separate **architecture factorization theorem/corollary**.

2. State explicitly the admissibility conditions on an architecture family, mirroring the refinement-style hypotheses in the background papers.

3. Promote monotonicity under partition refinement from experiment-only evidence to a theorem.

4. Keep theorem statements assumption-minimal; e.g. the Bayes-error sandwich itself does **not** need `f \in F_WL(G)`.

5. Use the background papers as stylistic models for:
   - theorem/proof layering,
   - induction-based factorization claims,
   - sharper separation of theory vs experiment vs open conjecture.
