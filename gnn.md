# The Information-Theoretic Foundations of Graph Neural Network Expressivity: From Weisfeiler–Leman to Partition-Aware Complexity

### A Graduate-Level Reference Monograph
**Ali Elouafiq**
*Department of Computer Science*

---

## Preface: The Crisis of Expressivity in Graph Representation Learning

At the heart of modern Graph Representation Learning lies a profound paradox: while the theoretical capacity of Graph Neural Networks (GNNs) is governed by elegant, algebraic ceilings of discrete Weisfeiler–Leman (WL) type, their practical, empirical performance is constrained by continuous, physical processes of information decay, bottleneck constriction, and numerical oversmoothing. 

For decades, theory and practice operated in separate silos:
1. **The Discrete/Algebraic School** studied GNN expressivity through the lens of graph isomorphism, first-order logic, and universal approximation. It proved beautiful, binary theorems (e.g., Morris et al., 2019; Xu et al., 2019) showing that standard Message-Passing Neural Networks (MPNNs) are at most as expressive as the 1-Weisfeiler-Leman test. However, these theorems assumed **lossless** message passing, infinite-precision representations, and noise-free topologies.
2. **The Continuous/Empirical School** struggled with the physical reality of GNN training. It documented severe degradation in deep architectures: **over-squashing** (the bottleneck compression of exponentially growing neighborhoods into fixed-size node vectors) and **oversmoothing** (the exponential collapse of node representations to a single uninformative average).

This monograph provides the unified mathematical prerequisites and core proofs that resolve this crisis. By transitioning from a deterministic partition lattice to a **probability space over partitions** via the **Lossy Weisfeiler–Leman (LossyWL)** operator (Kemper et al., 2025), we establish **Message-Passing Complexity (MPC)** as a continuous, task-specific, and topologically grounded complexity framework. 

Furthermore, we explore the **Partition-Aware Message-Passing Complexity (PA-MPC)** extension (Elouafiq, 2026), which proves a tight, two-sided **Bridge Inequality** connecting conditional partition entropy directly to the Bayes-optimal classification error rate.

### How to Read This Monograph
This text is organized in two layers.

1. **Core theory (Chapters 1–7).** These chapters develop the mathematical spine of the subject: partitions, WL refinement, entropy, random walks, lossy message passing, Bayesian error, and the computational engineering viewpoint.
2. **Research frontier (Chapter 8).** The final chapter deliberately changes register. It summarizes conjectures, empirical verdicts, limitations, and open directions. Readers using this text in a course may treat Chapter 8 as an outlook chapter or seminar appendix.

A recommended first reading order is:
- **Chapter 1** for the language of partitions and refinement;
- **Chapter 2** for the information-theoretic metric (DIG);
- **Chapter 3** for the graph-topological and random-walk background;
- **Chapters 4–5** for the LossyWL operator and the random-walk lower bound;
- **Chapter 6** for the Bayes-optimal error interpretation;
- **Chapter 7** for computation and engineering;
- **Chapter 8** only after the earlier chapters feel natural.

### Conventions Used Throughout
To reduce cognitive overhead, we keep the following conventions fixed unless stated otherwise.

- Graphs are finite, simple, and undirected.
- Vertex sets are denoted by $V$ and edge sets by $E$.
- A partition is always a set of non-empty, pairwise disjoint cells whose union is the ambient set.
- The refinement order is written $\Pi_1 \preceq \Pi_2$, meaning **"$\Pi_1$ is finer than $\Pi_2$"**.
- For binary-label information theory, the binary entropy inverse $H_{\mathrm{bin}}^{-1}$ always denotes the inverse branch on $[0,1/2]$.
- When a section is partly conjectural, empirical, or heuristic rather than theorem-level, we state this explicitly in prose.

### Pedagogical Features of the Text
Each chapter is designed to mix five ingredients:
1. a theory introduction explaining *why* the concepts matter,
2. a formal development with definitions and proofs,
3. a worked toy example,
4. a discussion of pathologies or edge cases,
5. exercises with complete solutions.

When reading quickly, it is often effective to read the introduction, then one worked example, then the theorem statements, and only afterward return to the full proofs.

---

## Chapter 1: The Algebraic Structure of Set Partitions and 1-WL Refinement

### Chapter 1 Roadmap and Warm-Up
This chapter serves two purposes. First, it introduces the algebraic language of **partitions** and **refinement**, which will become the main bookkeeping device of the entire monograph. Second, it shows how the classical 1-WL procedure generates such partitions step by step.

Before we start formally, it is helpful to see one tiny example all the way through.

#### Illustration 1.1 (A 1-WL Warm-Up on the Path $P_4$)
Let $G = P_4$ be the path
$$1 - 2 - 3 - 4$$
with constant initial coloring $c_v^{(0)} = \star$ for every vertex.

At depth $0$, all vertices look identical, so the induced partition is
$$
\Pi^{(0)} = \big\{\{1,2,3,4\}\big\}.
$$

At depth $1$, vertices $1$ and $4$ each see one neighbor of color $\star$, while vertices $2$ and $3$ each see two neighbors of color $\star$. Thus 1-WL produces two colors:
- an **endpoint color** for $\{1,4\}$,
- an **interior color** for $\{2,3\}$.

So the partition refines to
$$
\Pi^{(1)} = \big\{\{1,4\}, \{2,3\}\big\}.
$$

At depth $2$, vertex $1$ sees the pattern “myself = endpoint, neighbor = interior,” while vertex $2$ sees “myself = interior, neighbors = endpoint and interior,” and similarly for the symmetric partners $4$ and $3$. No further distinction occurs beyond the symmetry of the path, so the stable partition is
$$
\Pi^{(\infty)} = \big\{\{1,4\}, \{2,3\}\big\}.
$$

This tiny example already illustrates the central theme of the book: a message-passing architecture does not produce arbitrary distinctions; it induces a **partition of vertices into structurally indistinguishable classes**.

### 1.1 Equivalence Relations, Set Partitions, and the Fundamental Bijection
Before we can quantify how much information a GNN loses, we must formalize how a GNN groups vertices together. We begin with the mathematical language of equivalence relations and set partitions.

Let $V$ be a non-empty, finite set of vertices.

#### Definition 1.1 (Equivalence Relation)
A binary relation $\sim$ on $V$ is an **equivalence relation** if it satisfies the following three axioms for all $u, v, w \in V$:
1. **Reflexivity**: $u \sim u$.
2. **Symmetry**: If $u \sim v$, then $v \sim u$.
3. **Transitivity**: If $u \sim v$ and $v \sim w$, then $u \sim w$.

For any element $v \in V$, the **equivalence class** of $v$ under $\sim$ is defined as the subset:
$$[v]_\sim := \{ u \in V \mid u \sim v \}$$

#### Definition 1.2 (Set Partition)
A **partition** $\Pi$ of $V$ is a family $\{C_1, C_2, \dots, C_k\}$ of subsets of $V$ (referred to as **cells** or **blocks**) satisfying:
1. $C_i \neq \emptyset$ for all $i \in \{1, \dots, k\}$.
2. $C_i \cap C_j = \emptyset$ for all $i \neq j$ (pairwise disjointness).
3. $\bigcup_{i=1}^k C_i = V$ (exhaustiveness).

#### Theorem 1.1 (Fundamental Theorem of Equivalence Relations)
*There is a bijective correspondence between equivalence relations on a set $V$ and partitions of $V$.*

*Proof.*
1. **From Equivalence Relation to Partition**: Let $\sim$ be an equivalence relation on $V$. Define $\Pi_\sim := \{ [v]_\sim \mid v \in V \}$.
   - **Non-emptiness**: For any $v \in V$, reflexivity guarantees $v \sim v \implies v \in [v]_\sim$. Hence, no equivalence class in $\Pi_\sim$ is empty.
   - **Exhaustiveness**: Since $v \in [v]_\sim$ for every $v \in V$, it follows that $\bigcup_{v \in V} [v]_\sim = V$.
   - **Pairwise Disjointness**: Suppose $[u]_\sim \cap [v]_\sim \neq \emptyset$. Then there exists a vertex $w \in [u]_\sim \cap [v]_\sim$, which implies $w \sim u$ and $w \sim v$. By symmetry, $u \sim w$. By transitivity, since $u \sim w$ and $w \sim v$, we must have $u \sim v$. We now show $[u]_\sim = [v]_\sim$. Let $x \in [u]_\sim \implies x \sim u$. Since $u \sim v$, transitivity yields $x \sim v \implies x \in [v]_\sim$. Thus $[u]_\sim \subseteq [v]_\sim$. By symmetry, $[v]_\sim \subseteq [u]_\sim$. Hence, two equivalence classes are either completely disjoint or identical. $\Pi_\sim$ is a valid partition of $V$.
2. **From Partition to Equivalence Relation**: Let $\Pi = \{C_1, \dots, C_k\}$ be a partition of $V$. Define a relation $\sim_\Pi$ on $V$ by:
   $$u \sim_\Pi v \iff \exists C_i \in \Pi \text{ such that } u \in C_i \text{ and } v \in C_i$$
   - **Reflexivity**: Since $\bigcup C_i = V$, every $u \in V$ belongs to some cell $C_i$, hence $u, u \in C_i \implies u \sim_\Pi u$.
   - **Symmetry**: Commutativity of the logical "and" ensures $u, v \in C_i \iff v, u \in C_i \implies u \sim_\Pi v \iff v \sim_\Pi u$.
   - **Transitivity**: Suppose $u \sim_\Pi v$ and $v \sim_\Pi w$. Then $u, v \in C_i$ and $v, w \in C_j$. Since $v \in C_i \cap C_j$ and cells of a partition are pairwise disjoint, we must have $C_i = C_j$. Thus $u, w \in C_i \implies u \sim_\Pi w$.
This establishes the bijection. $\blacksquare$

---

### 1.2 The Partition Lattice and Refinement Operators
Let $\text{Part}(V)$ denote the set of all partitions of $V$. We introduce a partial ordering on $\text{Part}(V)$ that models the concept of "information grain."

#### Definition 1.3 (Partition Refinement / Finer & Coarser)
Let $\Pi_1, \Pi_2 \in \text{Part}(V)$. We say $\Pi_1$ is **finer** than $\Pi_2$ (or $\Pi_2$ is **coarser** than $\Pi_1$), denoted by $\Pi_1 \preceq \Pi_2$, if:
$$\forall C \in \Pi_1, \exists C' \in \Pi_2 \text{ such that } C \subseteq C'$$
If $\Pi_1 \preceq \Pi_2$ and $\Pi_1 \neq \Pi_2$, we say $\Pi_1$ is **strictly finer** than $\Pi_2$, written $\Pi_1 \prec \Pi_2$.

#### Theorem 1.2 ($\text{Part}(V)$ as a Finite Lattice, Hence Complete)
*The poset $(\text{Part}(V), \preceq)$ is a lattice: every pair of partitions $\Pi_1, \Pi_2 \in \text{Part}(V)$ has a unique **greatest lower bound** (meet, $\Pi_1 \wedge \Pi_2$) and a unique **least upper bound** (join, $\Pi_1 \vee \Pi_2$). Since $V$ is finite, the set $\text{Part}(V)$ is finite; therefore every subset has both an infimum and a supremum, so $(\text{Part}(V), \preceq)$ is in fact a complete lattice.*

*Proof.*
We construct the meet and join explicitly.

1. **Meet ($\Pi_1 \wedge \Pi_2$).**
   Define
   $$
   \Pi_m := \{ C \cap C' \mid C \in \Pi_1,\; C' \in \Pi_2,\; C \cap C' \neq \emptyset \}.
   $$
   - Every block of $\Pi_m$ is non-empty by construction.
   - For any $v \in V$, there are unique cells $C \in \Pi_1$ and $C' \in \Pi_2$ containing $v$, so $v \in C \cap C' \in \Pi_m$. Thus $\Pi_m$ covers $V$.
   - If two blocks $C_1 \cap C'_1$ and $C_2 \cap C'_2$ intersect, then some $w$ lies in both. Hence $w \in C_1 \cap C_2$ and $w \in C'_1 \cap C'_2$. Because cells of a partition are pairwise disjoint, this forces $C_1=C_2$ and $C'_1=C'_2$. So distinct blocks of $\Pi_m$ are disjoint.

   Therefore $\Pi_m$ is a partition. Moreover every block of $\Pi_m$ lies inside a block of $\Pi_1$ and inside a block of $\Pi_2$, so $\Pi_m \preceq \Pi_1$ and $\Pi_m \preceq \Pi_2$.

   Now let $\Pi_3$ be any lower bound with $\Pi_3 \preceq \Pi_1$ and $\Pi_3 \preceq \Pi_2$. Every block $B \in \Pi_3$ must lie inside some $C \in \Pi_1$ and some $C' \in \Pi_2$, hence $B \subseteq C \cap C' \in \Pi_m$. So $\Pi_3 \preceq \Pi_m$. Thus $\Pi_m$ is the greatest lower bound.

2. **Join ($\Pi_1 \vee \Pi_2$).**
   Let $\sim_1$ and $\sim_2$ be the equivalence relations induced by $\Pi_1$ and $\Pi_2$. Consider the smallest equivalence relation containing $\sim_1 \cup \sim_2$; equivalently, take the transitive closure of $\sim_1 \cup \sim_2$ and call it $\approx$. Let $\Pi_j$ be the partition induced by $\approx$.

   We claim that $\Pi_j$ is the least upper bound.
   - Because $\sim_1 \subseteq \approx$ and $\sim_2 \subseteq \approx$, every block of $\Pi_1$ and every block of $\Pi_2$ is contained in a block of $\Pi_j$. Hence $\Pi_1 \preceq \Pi_j$ and $\Pi_2 \preceq \Pi_j$.
   - Let $\Pi'$ be any other upper bound with $\Pi_1 \preceq \Pi'$ and $\Pi_2 \preceq \Pi'$, and let $\sim'$ be its equivalence relation. Then $\sim_1 \subseteq \sim'$ and $\sim_2 \subseteq \sim'$. Since $\sim'$ is already an equivalence relation, it must also contain the equivalence relation generated by $\sim_1 \cup \sim_2$, namely $\approx$. Therefore every block of $\Pi_j$ is contained in a block of $\Pi'$, so $\Pi_j \preceq \Pi'$.

   Thus $\Pi_j$ is the least upper bound.

The existence of meet and join makes $(\text{Part}(V),\preceq)$ a lattice. Because $V$ is finite, $\text{Part}(V)$ is finite, and every finite lattice is complete. $\blacksquare$

---

### 1.3 The Classical Weisfeiler–Leman (1-WL) Refinement Chain
Let $G = (V, E)$ be a finite, simple, undirected graph. Let $\mathcal{X}$ be a finite space of colors (or features). Let $c^{(0)}: V \to \mathcal{X}$ be an initial vertex coloring.

The **Weisfeiler–Leman (1-WL)** refinement algorithm iteratively constructs a sequence of colorings $c^{(0)}, c^{(1)}, c^{(2)}, \dots$ where $c^{(l)}: V \to \mathcal{X}^{(l)}$ is defined by:
$$c_v^{(l)} := \text{hash}\left( c_v^{(l-1)}, \{\!\{ c_u^{(l-1)} \mid u \in \mathcal{N}(v) \}\!\}\right)$$
where $\{\!\{\dots\}\!\}$ denotes a **multiset** (a bag of elements where order does not matter but multiplicity does), $\mathcal{N}(v) = \{ u \in V \mid (u,v) \in E \}$, and $\text{hash}$ is an injective function mapping the pair to a unique color space.

Every coloring $c^{(l)}$ induces an equivalence relation $\sim_l$ on $V$ where:
$$u \sim_l v \iff c_u^{(l)} = c_v^{(l)}$$
By Theorem 1.1, this induces a partition $\Pi^{(l)}$ of $V$.

#### Lemma 1.3 (Monotonic Refinement of WL Partitions)
*For any iteration $l \ge 0$, the partition sequence induced by 1-WL satisfies:*
$$\Pi^{(l+1)} \preceq \Pi^{(l)}$$

*Proof by induction.*
- **Base Case** ($l=0$): We show $\Pi^{(1)} \preceq \Pi^{(0)}$. Suppose $u, v \in V$ lie in the same cell of $\Pi^{(1)}$. This implies $c_u^{(1)} = c_v^{(1)}$. By the injectivity of the hash function, we must have:
  $$\left( c_u^{(0)}, \{\!\{ c_x^{(0)} \mid x \in \mathcal{N}(u) \}\!\}\right) = \left( c_v^{(0)}, \{\!\{ c_y^{(0)} \mid y \in \mathcal{N}(v) \}\!\}\right)$$
  Equating the first coordinates yields $c_u^{(0)} = c_v^{(0)}$, meaning $u$ and $v$ belong to the same cell in $\Pi^{(0)}$. Thus, any cell in $\Pi^{(1)}$ is a subset of some cell in $\Pi^{(0)}$.
- **Inductive Step**: Assume $\Pi^{(l)} \preceq \Pi^{(l-1)}$. Suppose $u, v$ lie in the same cell of $\Pi^{(l+1)} \implies c_u^{(l+1)} = c_v^{(l+1)}$. By injectivity of the hash, $c_u^{(l)} = c_v^{(l)}$, which implies $u$ and $v$ lie in the same cell of $\Pi^{(l)}$. Thus $\Pi^{(l+1)} \preceq \Pi^{(l)}$. $\blacksquare$

#### Theorem 1.4 (WL Convergence to Stable Partition)
*The partition sequence $\Pi^{(0)}, \Pi^{(1)}, \Pi^{(2)}, \dots$ converges to a **stable partition** $\Pi^{(\infty)}$ in at most $|V|-1$ iterations. That is, there exists a step $L^* \le |V|-1$ such that $\Pi^{(L)} = \Pi^{(L^*)}$ for all $L \ge L^*$.*

*Proof.*
Consider the number of cells in the partitions, $k(\Pi^{(l)}) = |\Pi^{(l)}|$. Since each partition in the sequence refines the previous one (Lemma 1.3), we must have:
$$1 \le k(\Pi^{(0)}) \le k(\Pi^{(1)}) \le k(\Pi^{(2)}) \le \dots \le |V|$$
At each step $l$, either $k(\Pi^{(l+1)}) > k(\Pi^{(l)})$ (a strict refinement) or $k(\Pi^{(l+1)}) = k(\Pi^{(l)})$.
- If $k(\Pi^{(l+1)}) = k(\Pi^{(l)})$, then since $\Pi^{(l+1)} \preceq \Pi^{(l)}$, the partitions must be identical: $\Pi^{(l+1)} = \Pi^{(l)}$.
- If a strict refinement occurs, the number of blocks increases by at least 1.
Since the maximum number of blocks is $|V|$, and the minimum is $1$, a strict refinement can happen at most $|V|-1$ times. Therefore, there must exist some $L^* \le |V|-1$ such that $\Pi^{(L^*+1)} = \Pi^{(L^*)}$. By induction, the partition remains constant for all subsequent steps. $\blacksquare$

---

### 1.4 A Fully Worked Refinement Table
The previous sections gave the abstract theory. Let us now spell out the refinement dynamics in a compact table, because students often understand WL best when they can literally watch cells split.

#### Illustration 1.2 (Refinement Table on $P_5$)
Consider the path
$$1 - 2 - 3 - 4 - 5$$
with constant initial color $\star$.

| Iteration $l$ | Vertex colors up to relabeling | Induced partition |
|---|---|---|
| $0$ | $\star,\star,\star,\star,\star$ | $\{\{1,2,3,4,5\}\}$ |
| $1$ | $a,b,b,b,a$ | $\{\{1,5\},\{2,3,4\}\}$ |
| $2$ | $a,c,d,c,a$ | $\{\{1,5\},\{2,4\},\{3\}\}$ |
| $3$ | same as step $2$ | stable |

Two remarks are worth emphasizing.
1. **Cells split but never merge.** Once $3$ is separated from $2$ and $4$, it never rejoins them.
2. **Symmetry survives refinement.** Vertices $1$ and $5$ remain paired forever because the graph has a reflection symmetry.

This table is the finite, concrete prototype of every later partition process in the monograph.

---

### 1.5 Pathological Cases: Regular Graphs, Strongly Regular Graphs, and the 1-WL Ceiling

#### The Intuition of GNN Partition Dynamics
Why do GNN researchers study set partitions? Because GNNs operate via message passing, which is fundamentally a local coloring process. Every node $v$ updates its state based only on the states of its neighbors. Consequently, if two nodes $u$ and $v$ have identical local structural neighborhoods, their representations will remain identical across *every* layer, regardless of GNN parameterization. 

The GNN stable partition $\Pi^{(\infty)}$ represents the structural ceiling of the GNN architecture **for the fixed observable inputs and message-passing scheme under consideration**. If a task $f$ requires distinguishing node $u$ from node $v$, but they belong to the same block in $\Pi^{(\infty)}$, then no choice of parameters within that setup can separate them exactly.

#### Pathological Edge Cases: Where 1-WL is Blind
1. **Vertex-Transitive Graphs**: Consider the cycle graph $C_n$. If we initialize the vertex features to a constant (e.g., $c_v^{(0)} = 1$ for all $v$), every vertex has exactly degree 2. At step 1, every vertex receives the multiset $\{\!\{1, 1\}\!\}$. Thus, the partition never refines:
   $$\Pi^{(0)} = \Pi^{(1)} = \dots = \Pi^{(\infty)} = \{V\}$$
   1-WL is completely blind to any task on $C_n$ that is not constant (such as determining the distance of a node to a source node).
2. **Strongly Regular Graphs (SRGs) and Graph Isomorphism**: Two non-isomorphic strongly regular graphs with the same parameters (e.g., the **Rook's graph** $R_{4,4}$ and the **Shrikhande graph**) cannot be distinguished by 1-WL. Both graphs collapse to the single-cell partition $\{V\}$ immediately. This is the classic structural ceiling first discovered by Weisfeiler and Leman in 1968.

#### Direct Link to PA-MPC Paper §3.1
This algebraic refinement framework is the exact foundation of **Definition 3.1** in the PA-MPC paper. PA-MPC defines the architecture-induced partition as:
$$\Pi_{\mathcal{A}}(G, L) := \mathrm{LossyWL}^L\big(\Pi_{\mathcal{A}}^{(0)}; G\big)$$
By explicitly indexing on the **initial observable partition** $\Pi_{\mathcal{A}}^{(0)}$, PA-MPC allows us to study how feature richness (e.g., GIN's constant initialization vs. GCN's degree initialization) affects the refinement chain. In this formalization, a degree-revealing initialization starts from a finer lattice point than a constant initialization, which helps explain why some architectures can resolve certain tasks at lower depths than others.

---

### Section 1 Exercises (With Complete, Rigorous Solutions)

#### Exercise 1.1: Step-by-Step Proof of Meet Associativity
**Task**: Prove that the meet operator $\wedge$ on the partition lattice $(\text{Part}(V), \dots, \preceq)$ is associative, i.e., for any partitions $\Pi_1, \Pi_2, \Pi_3 \in \text{Part}(V)$:
$$(\Pi_1 \wedge \Pi_2) \wedge \Pi_3 = \Pi_1 \wedge (\Pi_2 \wedge \Pi_3)$$

**Solution**:
1. By Theorem 1.2, the meet of two partitions consists of all non-empty pairwise intersections of their blocks.
2. Let $B \in (\Pi_1 \wedge \Pi_2) \wedge \Pi_3$. By definition, $B$ is a non-empty intersection of a block $B_{12} \in \Pi_1 \wedge \Pi_2$ and a block $C_k \in \Pi_3$.
3. Since $B_{12} \in \Pi_1 \wedge \Pi_2$, we have $B_{12} = C_i \cap C_j$ for some $C_i \in \Pi_1$ and $C_j \in \Pi_2$.
4. Thus, we can write:
   $$B = (C_i \cap C_j) \cap C_k \quad \text{where } B \neq \emptyset$$
5. Set intersection is associative in naive set theory. We prove this explicitly:
   - Let $x \in (C_i \cap C_j) \cap C_k \iff x \in C_i \cap C_j$ and $x \in C_k \iff (x \in C_i \text{ and } x \in C_j)$ and $x \in C_k \iff x \in C_i$ and $(x \in C_j \text{ and } x \in C_k) \iff x \in C_i$ and $x \in C_j \cap C_k \iff x \in C_i \cap (C_j \cap C_k)$.
6. Thus, $B = C_i \cap (C_j \cap C_k)$.
7. Since $B \neq \emptyset$, the intersection $C_j \cap C_k$ is non-empty, and therefore it is a valid block of $\Pi_2 \wedge \Pi_3$.
8. Consequently, $C_i \cap (C_j \cap C_k)$ is a non-empty intersection of a block of $\Pi_1$ and a block of $\Pi_2 \wedge \Pi_3$, which makes it a block of $\Pi_1 \wedge (\Pi_2 \wedge \Pi_3)$.
9. Thus, every block in $(\Pi_1 \wedge \Pi_2) \wedge \Pi_3$ is a block in $\Pi_1 \wedge (\Pi_2 \wedge \Pi_3)$. By symmetric reasoning, the reverse holds, proving associativity. $\blacksquare$

#### Exercise 1.2: Strongly Regular Graphs Counter-example
**Task**: Consider two strongly regular graphs $G_1, G_2$ with parameters $(16, 6, 2, 2)$ (the Rook's graph $R_{4,4}$ and the Shrikhande graph). Prove that under a constant initial coloring $c_v^{(0)} = 1$ for all $v$, the 1-WL partition sequence collapses to the single-cell partition at iteration 1 for both graphs, making them indistinguishable.

**Solution**:
1. A strongly regular graph $G$ with parameters $(n, k, \lambda, \mu)$ is a $k$-regular graph on $n$ vertices where:
   - Every pair of adjacent vertices has exactly $\lambda$ common neighbors.
   - Every pair of non-adjacent vertices has exactly $\mu$ common neighbors.
2. For both $R_{4,4}$ and Shrikhande, $n=16$ and $k=6$. Every vertex has exactly degree 6.
3. Let us execute 1-WL at $l=1$ under $c_v^{(0)} = 1$:
   $$c_v^{(1)} = \text{hash}\left(1, \{\!\{1, 1, 1, 1, 1, 1\}\!\}\right) = \chi_1$$
4. Since every vertex in both $G_1$ and $G_2$ has degree 6, every vertex receives the exact same neighbor multiset $\{\!\{1, 1, 1, 1, 1, 1\}\!\}$.
5. Thus, $c_v^{(1)} = \chi_1$ for all $v \in V_1$ and all $v \in V_2$.
6. The partition at iteration 1 is:
   $$\Pi_{G_1}^{(1)} = \{V_1\} \quad \text{and} \quad \Pi_{G_2}^{(1)} = \{V_2\}$$
7. Since $k(\Pi^{(1)}) = k(\Pi^{(0)}) = 1$, the partition has stabilized at iteration 1 for both graphs.
8. The stable GNN representation is identical for both graphs, proving that 1-WL cannot distinguish $R_{4,4}$ from the Shrikhande graph. $\blacksquare$

#### Exercise 1.3: Number of Partitions of a Small Set (Bell Numbers)
**Task**: Count the partitions of $V = \{1, 2, 3, 4\}$ by block-size signature and verify that the count equals the Bell number $B_4 = 15$. Then verify the recursion $B_{n+1} = \sum_{k=0}^n \binom{n}{k} B_k$ for $n = 3$.

**Solution**:
1. By Theorem 1.1 it suffices to enumerate equivalence relations on $V$, equivalently the partitions themselves.
2. Group partitions by block-size signature (a sorted multiset of cell sizes summing to $4$):
   - $\{4\}$: a single block. There is $1$ such partition: $\{\{1,2,3,4\}\}$.
   - $\{3,1\}$: one triple and one singleton. The triple is determined by which element is the singleton: $\binom{4}{1} = 4$.
   - $\{2,2\}$: two pairs. Choose the pair containing element $1$ in $\binom{3}{1} = 3$ ways; the other pair is forced. Total $3$.
   - $\{2,1,1\}$: one pair and two singletons. Choose the pair in $\binom{4}{2} = 6$ ways.
   - $\{1,1,1,1\}$: all singletons. There is $1$ such partition.
3. Total: $1 + 4 + 3 + 6 + 1 = 15 = B_4$. ✓
4. **Bell recursion at $n = 3$**: $B_4 = \sum_{k=0}^{3} \binom{3}{k} B_k = \binom{3}{0} \cdot 1 + \binom{3}{1} \cdot 1 + \binom{3}{2} \cdot 2 + \binom{3}{3} \cdot 5 = 1 + 3 + 6 + 5 = 15$. ✓ $\blacksquare$

#### Exercise 1.4: Join $\vee$ via the Transitive Closure
**Task**: Let $\Pi_1 = \{\{1,2\}, \{3\}, \{4\}\}$ and $\Pi_2 = \{\{1\}, \{2,3\}, \{4\}\}$ on $V = \{1,2,3,4\}$. Compute the join $\Pi_1 \vee \Pi_2$ explicitly via the transitive closure of the union relation $\sim_1 \cup \sim_2$, and verify by inspection that it is the least upper bound.

**Solution**:
1. Translate to equivalence relations: $\sim_1$ has equivalence classes $\{1,2\}, \{3\}, \{4\}$; $\sim_2$ has $\{1\}, \{2,3\}, \{4\}$.
2. The **union of relations** $R := \sim_1 \cup \sim_2$ contains the pairs $\{(1,2), (2,1), (2,3), (3,2)\}$ plus the reflexive diagonal. $R$ is symmetric and reflexive but **not transitive**: $(1,2), (2,3) \in R$ but $(1,3) \notin R$.
3. The **transitive closure** $R^{\!*}$ is the smallest transitive relation containing $R$. Computing closure layer-by-layer: from $1 \sim 2 \sim 3$ we add $(1, 3)$ and $(3, 1)$. No further additions.
4. The induced partition is $\Pi_1 \vee \Pi_2 = \{\{1, 2, 3\}, \{4\}\}$.
5. **Upper-bound check**: $\Pi_1 \preceq \Pi_1 \vee \Pi_2$ because $\{1,2\} \subseteq \{1,2,3\}$, $\{3\} \subseteq \{1,2,3\}$, $\{4\} \subseteq \{4\}$. Similarly for $\Pi_2$.
6. **Least-upper-bound check**: any upper bound $\Pi'$ must contain a cell housing both $1$ and $2$ (from $\Pi_1$) and a cell housing both $2$ and $3$ (from $\Pi_2$). By Definition 1.2 (pairwise disjointness) the cell containing $2$ is unique, so it must contain $\{1, 2, 3\}$. Hence $\{1, 2, 3\}$ is forced as a sub-cell of every upper bound, and $\Pi_1 \vee \Pi_2$ achieves the unique coarsest such structure. $\blacksquare$

#### Exercise 1.5: $\hat{0}$, $\hat{1}$, and the Lattice Identities
**Task**: Let $\hat{0} := \{\{v\} : v \in V\}$ be the **discrete partition** (every vertex in its own cell) and $\hat{1} := \{V\}$ the **indiscrete partition** (single cell). Prove the four absorption / identity laws: $\Pi \wedge \hat{0} = \hat{0}$, $\Pi \vee \hat{0} = \Pi$, $\Pi \wedge \hat{1} = \Pi$, $\Pi \vee \hat{1} = \hat{1}$ for every $\Pi \in \mathrm{Part}(V)$.

**Solution**:
1. **$\Pi \wedge \hat{0} = \hat{0}$.** The cells of $\Pi \wedge \hat{0}$ are non-empty intersections of a cell $C \in \Pi$ with a singleton $\{v\}$. Such an intersection is $\{v\}$ if $v \in C$ and empty otherwise. As $v$ ranges over $V$ and each $v$ lies in exactly one cell of $\Pi$ (Definition 1.2), we recover precisely the singletons $\{v\}$ for every $v \in V$, which is $\hat{0}$.
2. **$\Pi \vee \hat{0} = \Pi$.** The relation $\sim_{\hat{0}}$ is just equality. Its union with $\sim_\Pi$ is $\sim_\Pi$ itself, which is already an equivalence relation. The transitive closure is $\sim_\Pi$, inducing $\Pi$.
3. **$\Pi \wedge \hat{1} = \Pi$.** Every $C \in \Pi$ intersected with the unique cell $V$ of $\hat{1}$ gives $C \cap V = C$. So the meet returns exactly the cells of $\Pi$.
4. **$\Pi \vee \hat{1} = \hat{1}$.** Any upper bound of $\hat{1}$ must coarsen $\hat{1}$, but $\hat{1}$ is already the coarsest partition; therefore the only upper bound is $\hat{1}$ itself, and it is trivially the least. $\blacksquare$

#### Exercise 1.6: 1-WL Strict Refinement Stops at the Stable Partition
**Task**: Show that for any finite graph $G$ on $n$ vertices, the 1-WL refinement chain $\Pi^{(0)} \succeq \Pi^{(1)} \succeq \Pi^{(2)} \succeq \dots$ stabilizes at some iteration $L^* < n$, i.e.\ $\Pi^{(L^*)} = \Pi^{(L^* + 1)} = \dots$.

**Solution**:
1. Let $k(\Pi)$ denote the number of cells. By Lemma 1.3, $\Pi^{(l+1)} \preceq \Pi^{(l)}$, so $k(\Pi^{(l+1)}) \geq k(\Pi^{(l)})$.
2. The number of cells is bounded above by $|V| = n$ (any partition has at most $n$ blocks).
3. The integer sequence $k(\Pi^{(0)}) \leq k(\Pi^{(1)}) \leq \dots \leq n$ is non-decreasing and bounded, hence eventually constant. Let $L^*$ be the smallest iteration at which $k(\Pi^{(L^* + 1)}) = k(\Pi^{(L^*)})$.
4. At iteration $L^*$, no cell was strictly split (the cell count did not grow). The 1-WL update is deterministic and injective on cell-multiset signatures; a cell can only split, never merge. Hence equality of cell counts at consecutive steps implies equality of the partitions themselves: $\Pi^{(L^* + 1)} = \Pi^{(L^*)}$.
5. The fixed-point property of 1-WL (its update is a function of the current cell-assignment) then yields $\Pi^{(l)} = \Pi^{(L^*)}$ for every $l \geq L^*$.
6. **Upper bound on $L^*$**: each strict refinement step increases $k$ by at least $1$, starting from $k(\Pi^{(0)}) \geq 1$. Hence $L^* \leq n - 1 < n$. $\blacksquare$

#### Exercise 1.7: Refinement is a Partial Order — Antisymmetry
**Task**: Verify that $(\mathrm{Part}(V), \preceq)$ is antisymmetric: if $\Pi_1 \preceq \Pi_2$ and $\Pi_2 \preceq \Pi_1$, then $\Pi_1 = \Pi_2$.

**Solution**:
1. Suppose $\Pi_1 \preceq \Pi_2$: every $C \in \Pi_1$ is contained in some $C' \in \Pi_2$.
2. Symmetrically, every $C' \in \Pi_2$ is contained in some $C'' \in \Pi_1$.
3. Fix $C \in \Pi_1$. By (1), $C \subseteq C'$ for some $C' \in \Pi_2$. By (2), $C' \subseteq C''$ for some $C'' \in \Pi_1$. Therefore $C \subseteq C''$.
4. But $C$ and $C''$ are both cells of $\Pi_1$, hence either disjoint (Definition 1.2) or equal. Since $C \subseteq C''$ and $C \neq \emptyset$ (cells are non-empty), the disjoint case is impossible, so $C = C''$.
5. Chaining the inclusions: $C \subseteq C' \subseteq C'' = C$, forcing $C = C'$.
6. Therefore every cell of $\Pi_1$ is a cell of $\Pi_2$. The symmetric argument gives the reverse inclusion of cell-sets, so $\Pi_1 = \Pi_2$. $\blacksquare$

#### Exercise 1.8: The Petersen Graph's WL-Stable Partition
**Task**: Show that under any constant initial coloring, the 1-WL stable partition of the Petersen graph is the single-cell partition $\{V\}$, and conclude that 1-WL cannot distinguish any two vertices of Petersen.

**Solution**:
1. The Petersen graph is **vertex-transitive**: its automorphism group acts transitively on vertices.
2. Under any *constant* initial coloring, vertex-transitivity preserves the coloring: for every automorphism $\sigma$, $c^{(0)} \circ \sigma = c^{(0)}$.
3. The 1-WL update is permutation-equivariant: $c^{(l+1)}(\sigma(v)) = \mathrm{hash}(c^{(l)}(\sigma(v)), \{\!\{c^{(l)}(\sigma(u)) : u \sim v\}\!\})$. By induction on $l$, if $c^{(l)} \circ \sigma = c^{(l)}$ then $c^{(l+1)} \circ \sigma = c^{(l+1)}$.
4. Hence at every iteration, all vertices in the same orbit of $\mathrm{Aut}(G)$ receive the same color. Since Petersen has a single orbit (vertex-transitivity), all vertices receive the same color at every iteration.
5. The induced partition at every iteration is $\{V\}$, and trivially $\{V\} = \{V\}$ is stable.
6. Therefore 1-WL assigns the same color to every vertex of Petersen and cannot distinguish any pair. (This is the foundational source of the *vertex-transitivity vacuity* exploited in §8.4.) $\blacksquare$

#### Exercise 1.9: Constructing a Non-Singleton Partition Below $\Pi^{(0)}$
**Task**: Let $\Pi^{(0)} = \{\{1, 2, 3\}, \{4, 5\}\}$ on $V = \{1, 2, 3, 4, 5\}$. List all partitions strictly finer than $\Pi^{(0)}$ in $\mathrm{Part}(V)$.

**Solution**:
A partition strictly finer than $\Pi^{(0)}$ may split the cell $\{1,2,3\}$, the cell $\{4,5\}$, or both, but it may never merge across these two original cells. The nine strictly finer partitions are:

1. $\{\{1\},\{2,3\},\{4,5\}\}$
2. $\{\{2\},\{1,3\},\{4,5\}\}$
3. $\{\{3\},\{1,2\},\{4,5\}\}$
4. $\{\{1\},\{2\},\{3\},\{4,5\}\}$
5. $\{\{1,2,3\},\{4\},\{5\}\}$
6. $\{\{1\},\{2,3\},\{4\},\{5\}\}$
7. $\{\{2\},\{1,3\},\{4\},\{5\}\}$
8. $\{\{3\},\{1,2\},\{4\},\{5\}\}$
9. $\{\{1\},\{2\},\{3\},\{4\},\{5\}\}$

A quick counting check confirms this list: there are $B_3 B_2 = 5 \cdot 2 = 10$ refinements in total, and removing the original partition itself leaves $9$ strictly finer ones. $\blacksquare$

#### Exercise 1.10: 1-WL Fails to Distinguish $C_6$ from $2C_3$
**Task**: Let $G_1 = C_6$ (a single 6-cycle) and $G_2 = 2 C_3$ (two disjoint triangles, total $6$ vertices), with constant initial coloring $c_v^{(0)} = \star$. Show whether 1-WL distinguishes $G_1$ from $G_2$ at depth $L = 1$, and explain the algebraic reason.

**Solution**:
1. Both graphs are $2$-regular on $6$ vertices, so under constant init every vertex receives the multiset $\{\!\{\star, \star\}\!\}$ from its two neighbors at depth $1$.
2. The hash $\mathrm{hash}(\star, \{\!\{\star, \star\}\!\})$ produces the same color for every vertex in *both* graphs. Hence $\Pi^{(1)}_{G_1} = \{V_{G_1}\}$ and $\Pi^{(1)}_{G_2} = \{V_{G_2}\}$.
3. Both partitions are single-cell with $|V| = 6$; the multiset of vertex-colors $\{\!\{\chi, \chi, \chi, \chi, \chi, \chi\}\!\}$ is identical across the two graphs.
4. Therefore 1-WL does *not* distinguish $C_6$ from $2 C_3$ under constant init at depth $1$ — and by Exercise 1.6 / vertex-transitivity, it never will at any depth.
5. **Algebraic reason**: both graphs are $2$-regular, so the multiset-hashing operator sees the same local degree pattern everywhere at every round under constant initialization. In particular, 1-WL is blind here to the global difference between “one connected 6-cycle” and “two disconnected 3-cycles.” $\blacksquare$

---

## Chapter 2: Discrete Information Theory, Partition Entropy, and the Fano Bridge

### Chapter 2 Roadmap
Chapter 1 told us **which vertices a message-passing architecture can keep apart**. Chapter 2 asks the next question: **how hard is the downstream prediction problem once those indistinguishability classes are fixed?**

The answer is expressed through conditional entropy. If a partition cell contains almost all positive labels, prediction inside that cell is easy; if it contains a fifty-fifty mix, prediction is intrinsically hard. DIG packages this idea into a single number.

A useful mental picture is the following.
- A **pure** cell contributes $0$ bits of uncertainty.
- A **slightly mixed** cell contributes a small positive amount.
- A **balanced** cell contributes the maximum possible uncertainty for binary labels.

### 2.1 Measure Spaces, Probability, and Discrete Entropy
Let $(\Omega, \mathcal{F}, \mathbb{P})$ be a probability space. Let $Y: \Omega \to \mathcal{Y}$ be a discrete random variable taking values in a finite set $\mathcal{Y}$. The probability mass function of $Y$ is $p(y) = \mathbb{P}(Y = y)$.

#### Definition 2.1 (Shannon Entropy)
The **entropy** of $Y$ is defined as:
$$H(Y) := -\sum_{y \in \mathcal{Y}} p(y) \log_2 p(y)$$
with the convention that $0 \log_2 0 = 0$.

If $\mathcal{Y} = \{0, 1\}$, $Y$ is a binary random variable with $\mathbb{P}(Y = 1) = p$ and $\mathbb{P}(Y = 0) = 1-p$. The **binary entropy function** $H_{\mathrm{bin}}: [0, 1] \to [0, 1]$ is:
$$H_{\mathrm{bin}}(p) := -p \log_2 p - (1-p) \log_2 (1-p)$$

#### Lemma 2.1 (Properties of Binary Entropy)
*The binary entropy function $H_{\mathrm{bin}}(p)$ satisfies:*
1. $H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(1-p)$.
2. $H_{\mathrm{bin}}(p)$ is strictly concave on $[0, 1]$.
3. $H_{\mathrm{bin}}(0) = H_{\mathrm{bin}}(1) = 0$, and it achieves its unique maximum at $p = 1/2$ with $H_{\mathrm{bin}}(1/2) = 1$.

### 2.2 Conditional Partition Entropy (Depth Information Gap - DIG)
Let $V$ be the finite set of vertices, and let $\mu$ be the uniform probability measure on $V$, i.e., $\mu(v) = 1/|V|$ for all $v \in V$.
Let $f: V \to \{0, 1\}$ be a binary task.
Let $\Pi$ be a partition of $V$. 

For any vertex $v \in V$, let $C(v) \in \Pi$ denote the unique cell containing $v$. Under the uniform distribution $\mu$, the cell $C(v)$ is a random variable taking values in $\Pi$. The probability of choosing a vertex in cell $C$ is:
$$q_C := \mathbb{P}(C(v) = C) = \frac{|C|}{|V|}$$

Let $P_C$ denote the fraction of vertices in cell $C$ for which $f(v) = 1$:
$$P_C := \mathbb{P}(f(v) = 1 \mid v \in C) = \frac{1}{|C|} \sum_{u \in C} f(u)$$

#### Definition 2.2 (Depth Information Gap / Conditional Entropy)
The **conditional entropy** of $f$ given the partition $\Pi$, denoted as $\mathrm{DIG}(f \mid \Pi)$, is:
$$\mathrm{DIG}(f \mid \Pi) := H(f \mid C(v)) = \sum_{C \in \Pi} q_C H_{\mathrm{bin}}(P_C)$$

We also define the **quadratic Depth Information Gap** (analogous to Gini impurity):
$$\widetilde{\mathrm{DIG}}(f \mid \Pi) := \sum_{C \in \Pi} q_C P_C(1 - P_C)$$

#### Illustration 2.1 (How to Read DIG Cell by Cell)
Suppose a partition has three cells with label proportions
$$P_{C_1}=1, \qquad P_{C_2}=2/3, \qquad P_{C_3}=1/2.$$
Then their entropy contributions are, respectively,
- $H_{\mathrm{bin}}(1)=0$ bits: the cell is pure;
- $H_{\mathrm{bin}}(2/3)\approx 0.918$ bits: the cell is mixed but still biased;
- $H_{\mathrm{bin}}(1/2)=1$ bit: the cell is maximally ambiguous.

Thus DIG should always be interpreted as a **weighted average cell impurity**. The partition matters because it determines which vertices are forced to share the same prediction, and the entropy matters because it quantifies how costly that forcing is.

---

### 2.3 Mathematical Proof of Fano's Inequality for Partitions
We now prove the classic lower bound connecting conditional entropy to prediction error in its exact discrete form.

Let $\widehat{F}: \Pi \to \{0, 1\}$ be any predictor that maps a partition cell $C$ to a predicted binary label. The error rate $P_e$ of this predictor under the uniform measure on $V$ is:
$$P_e := \mathbb{P}(\widehat{F}(C(v)) \neq f(v)) = \sum_{C \in \Pi} q_C \mathbb{P}(\widehat{F}(C) \neq f(v) \mid v \in C)$$

#### Theorem 2.2 (Fano's Inequality for Binary Labels)
*For any partition-measurable predictor $\widehat{F}$, the error rate $P_e$ is bounded by:*
$$\mathrm{DIG}(f \mid \Pi) \le H_{\mathrm{bin}}(P_e)$$

*Proof.*
Define a random variable $E: V \to \{0, 1\}$ which indicates whether our predictor made an error:
$$E(v) := \begin{cases} 1 & \text{if } \widehat{F}(C(v)) \neq f(v) \\ 0 & \text{if } \widehat{F}(C(v)) = f(v) \end{cases}$$
By definition, $\mathbb{P}(E = 1) = P_e$.
We expand the joint conditional entropy $H(f, E \mid C(v))$ in two different ways using the chain rule of entropy:
1. First expansion:
   $$H(f, E \mid C(v)) = H(f \mid C(v)) + H(E \mid f, C(v))$$
   Since $E$ is completely determined once both the true label $f(v)$ and the predicted label $\widehat{F}(C(v))$ are known, the conditional entropy $H(E \mid f, C(v))$ is exactly $0$. Therefore:
   $$H(f, E \mid C(v)) = H(f \mid C(v)) = \mathrm{DIG}(f \mid \Pi)$$
2. Second expansion:
   $$H(f, E \mid C(v)) = H(E \mid C(v)) + H(f \mid E, C(v))$$
   - Since conditioning reduces entropy, we have $H(E \mid C(v)) \le H(E) = H_{\mathrm{bin}}(P_e)$.
   - Now consider the term $H(f \mid E, C(v))$:
     $$H(f \mid E, C(v)) = \mathbb{P}(E = 0) H(f \mid E = 0, C(v)) + \mathbb{P}(E = 1) H(f \mid E = 1, C(v))$$
     If $E = 0$, then $\widehat{F}(C(v)) = f(v)$. Since $\widehat{F}(C(v))$ is deterministic given $C(v)$, the label $f(v)$ is completely determined (no uncertainty). Thus $H(f \mid E = 0, C(v)) = 0$.
     If $E = 1$, then $f(v) \neq \widehat{F}(C(v))$. For a binary target, this means $f(v) = 1 - \widehat{F}(C(v))$. Since $\widehat{F}(C(v))$ is deterministic given $C(v)$, the label $f(v)$ is also completely determined (there is only one possible incorrect label). Thus $H(f \mid E = 1, C(v)) = 0$.
     Consequently, $H(f \mid E, C(v)) = 0$.

Combining both expansions:
$$\mathrm{DIG}(f \mid \Pi) = H(f, E \mid C(v)) = H(E \mid C(v)) + 0 \le H_{\mathrm{bin}}(P_e)$$
This completes the proof. $\blacksquare$

---

### 2.4 Narrative Discussion: Conditional Entropy as the Measure of Task Difficulty
Why do we choose conditional entropy (DIG) to measure task difficulty? 
Traditional GNN expressivity theory is **binary**: it only tells you if a task is theoretically possible ($0$) or impossible ($\infty$). But in the real world, GNN tasks have degrees of difficulty. If a GNN induces a partition where a cell $C$ contains 90% positive nodes and 10% negative nodes, it is much easier to make highly accurate predictions than if the cell contains 50% positive and 50% negative nodes. Conditional entropy captures this continuous difficulty smoothly.

In the revised PA-MPC draft, Ali Elouafiq leverages this to prove the **two-sided Bridge Inequality (Theorem 1)**:
$$H_{\mathrm{bin}}^{-1}(\mathrm{DIG}(f \mid \Pi)) \le \varepsilon_\Pi^* \le \frac{1}{2}\,\mathrm{DIG}(f \mid \Pi)$$
This inequality is extremely powerful:
1. **The Lower Bound** (via Fano) proves that if DIG is positive, the GNN **must** incur a classification error rate of at least $H_{\mathrm{bin}}^{-1}(\mathrm{DIG})$.
2. **The Upper Bound** guarantees that the maximum possible error rate is bounded by half the DIG.
Thus, DIG is not just a statistical proxy—it is the **exact mathematical envelope** that bounds prediction accuracy.

To avoid ambiguity, throughout this monograph the notation $H_{\mathrm{bin}}^{-1}$ always means the inverse of the binary entropy function on the monotone branch $[0,1/2] \to [0,1]$. This is the branch relevant for Bayes error, because a binary misclassification rate never exceeds $1/2$.

#### Chapter 2 Takeaway
Once an architecture induces a partition $\Pi$, the residual difficulty of a binary task is summarized by the impurity of the partition cells. DIG measures that impurity in bits, and the bridge inequality turns those bits into lower and upper control on the best achievable partition-measurable error.

---

### Section 2 Exercises (With Complete, Rigorous Solutions)

#### Exercise 2.1: Rigorous Analytical Proof of the Upper Bridge Bound
**Task**: Prove that the cell-level inequality $\min(p, 1-p) \le \frac{1}{2} H_{\mathrm{bin}}(p)$ holds for all $p \in [0, 1]$.

**Solution**:
1. By symmetry, $H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(1-p)$ and $\min(p, 1-p) = \min(1-p, p)$. Thus, we only need to prove the claim for $p \in [0, 0.5]$, where $\min(p, 1-p) = p$.
2. We define the function $g(p) = \frac{1}{2} H_{\mathrm{bin}}(p) - p$ on the interval $[0, 0.5]$.
3. Let us take the derivative of $g(p)$ with respect to $p$:
   $$g'(p) = \frac{1}{2} \frac{d}{dp} \left( -p \log_2 p - (1-p) \log_2(1-p) \right) - 1$$
   Recall that $\frac{d}{dx} (x \ln x) = \ln x + 1$. Converting to base 2:
   $$g'(p) = \frac{1}{2} \left( -\log_2 p - \log_2 e - \left( -\log_2(1-p) - \log_2 e \right) \right) - 1$$
   $$g'(p) = \frac{1}{2} \log_2 \left( \frac{1-p}{p} \right) - 1$$
4. Let us take the second derivative of $g(p)$:
   $$g''(p) = \frac{1}{2} \frac{d}{dp} \left( \log_2(1-p) - \log_2 p \right) = \frac{1}{2} \left( \frac{-\log_2 e}{1-p} - \frac{\log_2 e}{p} \right) = -\frac{\log_2 e}{2 p(1-p)}$$
5. Since $p \in (0, 0.5)$, $p(1-p) > 0$. Thus $g''(p) < 0$ for all $p \in (0, 0.5)$, meaning the function $g(p)$ is strictly concave.
6. Evaluate the boundary conditions of $g(p)$:
   - For $p = 0$: $g(0) = \frac{1}{2} H_{\mathrm{bin}}(0) - 0 = 0$.
   - For $p = 0.5$: $g(0.5) = \frac{1}{2} H_{\mathrm{bin}}(0.5) - 0.5 = \frac{1}{2}(1) - 0.5 = 0$.
7. Since $g(p)$ is strictly concave on $[0, 0.5]$ and vanishes at the boundaries $0$ and $0.5$, it must be strictly positive on the interior $(0, 0.5)$.
8. Thus, $g(p) \ge 0 \implies p \le \frac{1}{2} H_{\mathrm{bin}}(p)$ for all $p \in [0, 0.5]$.
9. Substituting $\min(p, 1-p)$, we obtain $\min(p, 1-p) \le \frac{1}{2} H_{\mathrm{bin}}(p)$ for all $p \in [0, 1]$. $\blacksquare$

#### Exercise 2.2: Computing $\mathrm{DIG}$ on a Worked Partition
**Task**: Let $V = \{1, 2, 3, 4, 5, 6, 7, 8\}$ with uniform measure $\mu(v) = 1/8$, binary task $f$ with $f^{-1}(1) = \{1, 2, 3, 4, 5\}$, and partition $\Pi = \{C_1, C_2, C_3\}$ where $C_1 = \{1, 2, 3\}$, $C_2 = \{4, 5, 6\}$, $C_3 = \{7, 8\}$. Compute $\mathrm{DIG}(f \mid \Pi)$, $\widetilde{\mathrm{DIG}}(f \mid \Pi)$, and $\varepsilon^*_\Pi$, and verify Theorem 1 numerically.

**Solution**:
1. **Cell masses**: $q_{C_1} = 3/8$, $q_{C_2} = 3/8$, $q_{C_3} = 2/8 = 1/4$.
2. **Cell posteriors**: $P_{C_1} = 3/3 = 1$ (all positive); $P_{C_2} = 2/3$ (vertices $4, 5$ positive; $6$ negative); $P_{C_3} = 0$ (both negative).
3. **Entropy DIG**:
   $\mathrm{DIG}(f \mid \Pi) = \frac{3}{8} H_{\mathrm{bin}}(1) + \frac{3}{8} H_{\mathrm{bin}}(2/3) + \frac{1}{4} H_{\mathrm{bin}}(0) = 0 + \frac{3}{8} \cdot 0.9183 + 0 \approx 0.3444$ bits.
   Here $H_{\mathrm{bin}}(2/3) = -\frac{2}{3} \log_2 \frac{2}{3} - \frac{1}{3} \log_2 \frac{1}{3} \approx 0.9183$.
4. **Variance DIG**:
   $\widetilde{\mathrm{DIG}} = \frac{3}{8} \cdot 1 \cdot 0 + \frac{3}{8} \cdot \frac{2}{3} \cdot \frac{1}{3} + \frac{1}{4} \cdot 0 \cdot 1 = \frac{3}{8} \cdot \frac{2}{9} = \frac{1}{12}$.
5. **Bayes error**: $\varepsilon^*_\Pi = \frac{3}{8} \cdot 0 + \frac{3}{8} \cdot \min(2/3, 1/3) + \frac{1}{4} \cdot 0 = \frac{3}{8} \cdot \frac{1}{3} = \frac{1}{8} = 0.125$.
6. **Theorem 1 check**:
   - Lower bound: $H_{\mathrm{bin}}^{-1}(0.3444) \approx 0.064$, and $0.064 \leq 0.125$. ✓
   - Upper bound: $\frac{1}{2} \mathrm{DIG} \approx 0.172$, and $0.125 \leq 0.172$. ✓
7. Both halves of the sandwich are non-trivial here (neither is tight). $\blacksquare$

#### Exercise 2.3: Conditional Entropy Decreases Under Refinement
**Task**: Prove that if $\Pi' \preceq \Pi$ (i.e.\ $\Pi'$ is finer than $\Pi$), then for every task $f$, $\mathrm{DIG}(f \mid \Pi') \leq \mathrm{DIG}(f \mid \Pi)$. (This is the *monotonicity* of DIG under refinement, foundational to PA-MPC §7.4.)

**Solution**:
1. Let $C \in \Pi$ and let $\Pi'|_C := \{B \in \Pi' : B \subseteq C\}$ be the sub-partition of $C$ induced by $\Pi'$; by refinement, $\bigsqcup_{B \in \Pi'|_C} B = C$.
2. Define cell-level quantities $q_C, P_C$ as in §2 and $r_{B|C} := |B| / |C|$, $P_B := |B|^{-1} \sum_{v \in B} f(v)$ for $B \in \Pi'|_C$. Then $\sum_{B \in \Pi'|_C} r_{B|C} = 1$ and $\sum_{B \in \Pi'|_C} r_{B|C} \cdot P_B = P_C$ (weighted average).
3. The conditional entropy $H_{\mathrm{bin}}$ is **concave** on $[0, 1]$. Jensen's inequality applied to the convex combination above gives
   $H_{\mathrm{bin}}(P_C) = H_{\mathrm{bin}}\!\Big(\sum_B r_{B|C} P_B\Big) \geq \sum_B r_{B|C} H_{\mathrm{bin}}(P_B)$.
4. Multiply both sides by $q_C$:
   $q_C H_{\mathrm{bin}}(P_C) \geq \sum_{B \in \Pi'|_C} q_C r_{B|C} H_{\mathrm{bin}}(P_B) = \sum_{B \in \Pi'|_C} q_B H_{\mathrm{bin}}(P_B)$ since $q_B = q_C \cdot r_{B|C}$.
5. Summing over $C \in \Pi$ and re-indexing the right-hand side over all $B \in \Pi'$:
   $\mathrm{DIG}(f \mid \Pi) = \sum_C q_C H_{\mathrm{bin}}(P_C) \geq \sum_B q_B H_{\mathrm{bin}}(P_B) = \mathrm{DIG}(f \mid \Pi')$. $\blacksquare$

#### Exercise 2.4: Sandwich is Tight on the Balanced Cell Limit
**Task**: Construct an explicit partition $\Pi$ and task $f$ for which *both* sides of Theorem 1's sandwich are exactly $1/2$ (i.e.\ the sandwich collapses to equality). 

**Solution**:
1. Let $|V| = 2n$, with $f$ assigning the value $1$ to exactly $n$ vertices.
2. Let $\Pi = \{V\}$ (the indiscrete partition, single cell).
3. Then $q_V = 1$ and $P_V = n / (2n) = 1/2$.
4. $\mathrm{DIG}(f \mid \Pi) = 1 \cdot H_{\mathrm{bin}}(1/2) = 1$ bit (exactly).
5. $\varepsilon^*_\Pi = 1 \cdot \min(1/2, 1/2) = 1/2$.
6. Lower bound: $H_{\mathrm{bin}}^{-1}(1) = 1/2$. Equal to $\varepsilon^*_\Pi$. ✓
7. Upper bound: $\frac{1}{2} \cdot 1 = 1/2$. Equal to $\varepsilon^*_\Pi$. ✓
8. Both halves collapse simultaneously, illustrating that the balanced-cell limit is the unique tightness point of *both* sides of the bridge inequality. This is also the worst-case PA-MPC scenario (the GNN's representation is operationally vacuous on $f$). $\blacksquare$

#### Exercise 2.5: Fano's Inequality on the Binary Alphabet
**Task**: Prove the binary-alphabet Fano inequality: for any predictor $\hat{f}$ of a $\{0,1\}$-valued random variable $f$ from any random variable $C$,
$$H(f \mid C) \leq H_{\mathrm{bin}}(P_e), \qquad P_e := \Pr[\hat{f}(C) \neq f].$$
State the role this plays in the lower-half of Theorem 1.

**Solution**:
1. Let $E := \mathbf{1}\{\hat{f}(C) \neq f\}$ be the binary error indicator with $\Pr[E = 1] = P_e$.
2. Apply the chain rule of entropy two ways:
   $H(f, E \mid C) = H(f \mid C) + H(E \mid f, C) = H(f \mid C) + 0$, since $E$ is a deterministic function of $f$ and $C$ once $\hat{f}$ is fixed.
3. Also $H(f, E \mid C) = H(E \mid C) + H(f \mid E, C)$.
4. **Bound $H(E \mid C) \leq H(E) = H_{\mathrm{bin}}(P_e)$** (conditioning never increases entropy).
5. **Bound $H(f \mid E, C)$**: when $E = 0$, $f = \hat{f}(C)$ is deterministic given $C$, so $H(f \mid E = 0, C) = 0$. When $E = 1$ on a binary alphabet, $f$ is the unique non-predicted bit given $C$, so again $H(f \mid E = 1, C) = 0$ — this is where the binary-alphabet assumption is essential (for $|\mathcal{Y}| \geq 3$ the bound is $\log(|\mathcal{Y}| - 1)$).
6. Combining: $H(f \mid C) = H(E \mid C) + H(f \mid E, C) \leq H_{\mathrm{bin}}(P_e)$. ✓
7. **Role in Theorem 1**: aggregating this per-cell inequality with cell-mass weights $q_C$ and choosing $\hat{f}$ to be the Bayes-optimal cell predictor (Theorem 6.1) gives $\mathrm{DIG}(f \mid \Pi) \leq H_{\mathrm{bin}}(\varepsilon^*_\Pi)$. Inverting on the increasing branch yields the lower bound of the sandwich. $\blacksquare$

#### Exercise 2.6: $H_{\mathrm{bin}}^{-1}$ is Lipschitz-Free Near $1$
**Task**: Compute $H_{\mathrm{bin}}^{-1}(0.9)$, $H_{\mathrm{bin}}^{-1}(0.99)$, $H_{\mathrm{bin}}^{-1}(0.999)$ numerically (to $4$ decimal digits), and explain why $H_{\mathrm{bin}}^{-1}$ has unbounded derivative as the argument approaches $1$.

**Solution**:
1. $H_{\mathrm{bin}}^{-1}(0.9)$: solve $H_{\mathrm{bin}}(p) = 0.9$ for $p \in [0, 1/2]$. Numerically by bisection: $p \approx 0.3160$.
2. $H_{\mathrm{bin}}^{-1}(0.99)$: $H_{\mathrm{bin}}(0.42) \approx 0.9815$, $H_{\mathrm{bin}}(0.44) \approx 0.9896$, $H_{\mathrm{bin}}(0.45) \approx 0.9928$. Refining: $p \approx 0.4429$.
3. $H_{\mathrm{bin}}^{-1}(0.999)$: $p \approx 0.4818$.
4. **Asymptotic behavior**: as $p \to 1/2$, $H_{\mathrm{bin}}'(p) = \log_2\!\big((1-p)/p\big) \to 0$. By the inverse function theorem $(H_{\mathrm{bin}}^{-1})'(y) = 1 / H_{\mathrm{bin}}'(p)$, so as $y \to 1^-$, $p \to 1/2$, and $(H_{\mathrm{bin}}^{-1})'(y) \to +\infty$.
5. **Operational consequence**: the lower bound of Theorem 1 is *very steep* near $\mathrm{DIG} = 1$. A small change in DIG near the balanced limit produces a large change in the lower bound on Bayes error, making PA-MPC an *extremely sharp* diagnostic in the over-smoothed regime where DIG saturates near $1$. $\blacksquare$

#### Exercise 2.7: Equivalent Forms — Variance vs. Entropy
**Task**: Show that on a *pure* partition $\Pi$ for a binary task $f$, the variance form $\widetilde{\mathrm{DIG}}(f \mid \Pi) = 0$ if and only if $\mathrm{DIG}(f \mid \Pi) = 0$, and produce a non-pure partition where $\widetilde{\mathrm{DIG}}$ and $\mathrm{DIG}$ differ by a factor of at least $4$.

**Solution**:
1. **Purity equivalence**. Both quantities are sums $\sum_C q_C \phi(P_C)$ with $\phi$ being $P(1-P)$ (variance) or $H_{\mathrm{bin}}(P)$ (entropy). Both functions vanish iff $P \in \{0, 1\}$ and are strictly positive otherwise; both summands are non-negative; so the full sum vanishes iff every $P_C \in \{0, 1\}$ — exactly purity. Hence the two characterizations are equivalent.
2. **Quantitative gap**. Take $\Pi = \{V\}$ with $P_V = 1/2$:
   - $\widetilde{\mathrm{DIG}} = 1/2 \cdot 1/2 = 1/4$.
   - $\mathrm{DIG} = H_{\mathrm{bin}}(1/2) = 1$.
   - Ratio: $1 / (1/4) = 4$. ✓
3. The ratio between entropy and variance forms is therefore not bounded by a constant smaller than $4$ on the balanced cell, justifying why PA-MPC uses the entropy form for the *tight* upper bound $\varepsilon^*_\Pi \leq \frac{1}{2} \mathrm{DIG}$ (Theorem 1) rather than the loose variance form. $\blacksquare$

---

## Chapter 3: Graph Topology, Transition Matrices, and Random Walk Bottlenecks

### Chapter 3 Roadmap
The previous chapter quantified *label uncertainty inside a fixed partition*. We now step back and ask a more structural question: **which graph topologies make information easy or difficult to propagate in the first place?**

Three families of examples should stay in mind throughout this chapter.
- A **path** spreads information slowly because every extra hop costs another routing decision.
- A **star** has tiny graph diameter but a severe hub bottleneck, because many messages compete to traverse the center.
- A **cycle** introduces parity and periodicity phenomena that matter for random walks and for later oversmoothing discussions.

The purpose of this chapter is not merely to review graph theory. It is to build the exact matrix and topological vocabulary needed for the random-walk lower bounds in Chapter 5.

### 3.1 Matrices of a Graph and Random Walks
Let $G = (V, E)$ be a simple undirected graph with vertex set $V = \{1, 2, \dots, n\}$.

#### Definition 3.1 (Adjacency and Degree Matrices)
- The **Adjacency Matrix** $A \in \mathbb{R}^{n \times n}$ is defined by:
  $$A_{ij} := \begin{cases} 1 & \text{if } (i,j) \in E \\ 0 & \text{otherwise} \end{cases}$$
- The **Degree Matrix** $D \in \mathbb{R}^{n \times n}$ is the diagonal matrix:
  $$D_{ii} := \text{deg}(i) = \sum_{j=1}^n A_{ij}$$

#### Definition 3.2 (Normalized Adjacency Transition Matrix)
The **transition matrix** $P \in \mathbb{R}^{n \times n}$ for a standard random walk on $G$ is:
$$P := D^{-1}A$$
The entries are $P_{ij} = \frac{A_{ij}}{\text{deg}(i)}$, representing the probability of moving from node $i$ to neighbor $j$ in one step.

For GNNs with self-loops, we often use the transition matrix of a **lazy random walk**:
$$P_{\mathrm{lazy}} := \frac{1}{2}(I + D^{-1}A)$$

#### Lemma 3.1 (Transition Probability along Walks)
*The entry $(P^L)_{vu}$ of the $L$-th power of the transition matrix is exactly the probability that a standard random walk starting at node $v$ is at node $u$ after $L$ steps.*

*Proof by induction.*
- **Base Case** ($L=1$): $(P^1)_{vu} = P_{vu} = \frac{A_{vu}}{\text{deg}(v)}$, which is exactly the definition of a single-step transition probability.
- **Inductive Step**: Assume $(P^k)_{vu}$ is the probability of moving from $v$ to $u$ in $k$ steps. By the Chapman-Kolmogorov equations (or matrix multiplication):
  $$(P^{k+1})_{vu} = \sum_{w=1}^n (P^k)_{vw} P_{wu}$$
  This is the sum over all intermediate steps $w$ of (the probability of moving from $v$ to $w$ in $k$ steps) times (the probability of transitioning from $w$ to $u$ in one step). This matches the probability of a $(k+1)$-step walk. $\blacksquare$

---

### 3.2 Biconnectivity and Cycle Structures

#### Definition 3.3 (Cut Vertex and Bridge)
- A vertex $v \in V$ is a **cut vertex** (or articulation point) if removing $v$ and its incident edges increases the number of connected components of $G$.
- An edge $e \in E$ is a **bridge** if removing $e$ increases the connected components of $G$.

#### Definition 3.4 (Biconnected Graph)
A connected graph $G$ is **biconnected** if it has no cut vertices. A **biconnected component** (or **block**) of a graph is a maximal biconnected subgraph.

#### Theorem 3.2 (Cycles and Biconnectivity)
*Two distinct edges $e_1, e_2$ belong to the same biconnected component if and only if there exists a simple cycle containing both $e_1$ and $e_2$.*

This theorem is essential for GNN models designed for molecular ring detection (CIN, FragNet), as it ensures that simple rings correspond precisely to biconnected components.

---

### Section 3 Exercises (With Complete, Rigorous Solutions)

#### Exercise 3.1: Step-by-Step Proof of the Biconnectivity Cycle Theorem
**Task**: Prove that two distinct edges $e_1, e_2$ belong to the same biconnected component of a graph $G$ if and only if there exists a simple cycle containing both $e_1$ and $e_2$.

**Solution**:
1. **Direction 1 (If Cycle $\implies$ Same Biconnectivity Component)**:
   - Suppose there exists a simple cycle $C$ containing both $e_1 = (u_1, v_1)$ and $e_2 = (u_2, v_2)$.
   - A cycle has no cut vertices because removing any single vertex leaves the cycle as a path, which remains connected. Thus, a cycle is a biconnected subgraph.
   - Since a biconnected component is a maximal biconnected subgraph, the entire cycle $C$ must be contained within some biconnected component $B$ of $G$. Thus, $e_1$ and $e_2$ belong to the same component.
2. **Direction 2 (If Same Biconnectivity Component $\implies$ Cycle)**:
   - Suppose $e_1$ and $e_2$ are in the same biconnected component $B$.
   - By definition of a biconnected component, $B$ has no cut vertices.
   - Let $u$ be a vertex on $e_1$ and $v$ be a vertex on $e_2$. Since $B$ is biconnected, there must exist at least two vertex-disjoint paths between $u$ and $v$ in $B$ (by Menger's Theorem / Whitney's Theorem for 2-connected graphs).
   - Combining these two vertex-disjoint paths forms a simple cycle that contains both $u$ and $v$, and by extension, can be routed to contain the edges $e_1$ and $e_2$. $\blacksquare$

#### Exercise 3.2: Transition Matrix of $C_4$ and Its Spectrum
**Task**: Let $G = C_4$ (the 4-cycle on vertices $\{1, 2, 3, 4\}$). Write down $A$, $D$, $P = D^{-1}A$ explicitly. Diagonalize $P$ and identify the relevant mixing-gap discussion. Use the spectrum to compute $(P^L)_{vu}$ for opposite vertices $v = 1$, $u = 3$ in closed form as a function of $L$.

**Solution**:
1. $A = \begin{pmatrix} 0 & 1 & 0 & 1 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 1 & 0 & 1 & 0 \end{pmatrix}$, $D = 2 I$, $P = \tfrac{1}{2} A$.
2. The eigenvalues of $A$ on $C_n$ are $2 \cos(2\pi k / n)$ for $k = 0, 1, \dots, n - 1$. For $n = 4$ this gives $\{2,0,-2,0\}$.
3. Therefore the eigenvalues of $P$ are $\{1,0,-1,0\}$.
4. If one orders eigenvalues by size, then the usual quantity $1-\lambda_2$ equals $1-0=1$. But for **mixing**, the relevant parameter is the second-largest eigenvalue in absolute value, and here it equals $1$ because of the eigenvalue $-1$. So the chain has **no absolute spectral gap** and is periodic rather than mixing.
5. Using the Fourier eigenbasis on $\mathbb{Z}/4\mathbb{Z}$, we may write
   $$
   (P^L)_{13} = \sum_{k=0}^3 \lambda_k^L \phi_k(1)\overline{\phi_k(3)}.
   $$
   For opposite vertices the weights are $(-1)^k/4$.
6. Only the $k=0$ and $k=2$ terms contribute for $L\ge 1$, so
   $$
   (P^L)_{13} = \frac{1}{4}\big(1 + (-1)^L\big).
   $$
7. Hence
   $$
   (P^L)_{13} =
   \begin{cases}
   1/2 & \text{if $L$ is even},\\
   0 & \text{if $L$ is odd}.
   \end{cases}
   $$
8. This is the bipartite periodicity: the walk alternates between parity classes and therefore never converges to stationarity in the non-lazy chain. $\blacksquare$

#### Exercise 3.3: Bridge Detection and Cut Vertices in a Lollipop Graph
**Task**: Consider the **lollipop graph** $L_{4, 3}$: a complete graph $K_4$ on vertices $\{1, 2, 3, 4\}$ with an attached path $4 - 5 - 6 - 7$ of length $3$. Identify all bridges and cut vertices. Apply Theorem 3.2 to determine which pairs of edges share a biconnected component.

**Solution**:
1. **Bridges**: an edge $e$ is a bridge iff its removal disconnects $G$. Edges $(4, 5), (5, 6), (6, 7)$ each disconnect a non-empty subset of the path from $K_4$. Edges inside $K_4$ do not disconnect since the remaining $K_4 - e$ contains all alternative paths.
2. **Bridge set**: $\{(4,5), (5,6), (6,7)\}$ (three bridges).
3. **Cut vertices**: $v$ is a cut vertex iff $G - v$ has more connected components. Vertex $4$ separates $K_4 - 4$ from the path tail $\{5, 6, 7\}$. Vertices $5, 6$ each cut the path. Vertex $7$ is a leaf and not a cut vertex. Vertices $1, 2, 3$ are not cut vertices since $K_4$ minus any one of them remains connected as $K_3$.
4. **Cut-vertex set**: $\{4, 5, 6\}$.
5. **Biconnected components**: by Theorem 3.2, two edges share a component iff they lie on a common simple cycle. The $K_4$ subgraph has many cycles; all $6$ of its edges share a single biconnected component. Each bridge $(4,5), (5,6), (6,7)$ is its own biconnected component (a bridge has no cycle through it).
6. **Block count**: $4$ biconnected components total (one for $K_4$, three for the bridges).
7. **PA-MPC consequence**: by Lemma 5.1, any task requiring information across a bridge has $\mathrm{MPC} \geq -\log_2 \Pr[\text{message survives the bridge}]$. For the lollipop, propagation from vertex $7$ to any $K_4$ vertex must traverse all three bridges, each contributing at least $\log_2(\mathrm{deg})$ of surprisal under LossyWL. $\blacksquare$

#### Exercise 3.4: Lazy Random Walk Avoids Bipartite Periodicity
**Task**: Repeat Exercise 3.2 for the *lazy* transition matrix $P_{\mathrm{lazy}} = \tfrac{1}{2}(I + D^{-1}A)$ on $C_4$. Show that $(P_{\mathrm{lazy}}^L)_{13}$ converges to $1/4$ as $L \to \infty$, and quantify the convergence rate.

**Solution**:
1. The eigenvalues of $P_{\mathrm{lazy}}$ are $\tfrac{1}{2}(1 + \lambda_k)$ where $\lambda_k \in \{1,0,-1,0\}$ are the eigenvalues of $P$.
2. Hence the lazy spectrum is $\{1,1/2,0,1/2\}$. The troublesome $-1$ eigenvalue has moved to $0$, so periodicity disappears.
3. The eigenvectors are unchanged. For opposite vertices, the spectral weights are still $(-1)^k/4$.
4. Therefore, for $L\ge 1$,
   $$
   (P_{\mathrm{lazy}}^L)_{13}
   = \frac{1}{4}\Big(1 - (1/2)^L + 0 - (1/2)^L\Big)
   = \frac{1}{4} - \frac{1}{2^{L+1}}.
   $$
5. Thus
   $$
   \lim_{L\to\infty}(P_{\mathrm{lazy}}^L)_{13}=\frac14,
   $$
   which is exactly the stationary mass of a four-vertex regular graph.
6. The convergence rate is
   $$
   \left|(P_{\mathrm{lazy}}^L)_{13}-\frac14\right| = 2^{-(L+1)},
   $$
   so convergence is exponentially fast.
7. This exercise is the cleanest demonstration of why adding laziness or self-retention stabilizes bipartite substrates: the chain now mixes instead of oscillating. $\blacksquare$

#### Exercise 3.5: Spectral Gap of a Star Graph
**Task**: Compute the eigenvalues of the transition matrix $P$ on a star graph $S_n$ (one center plus $n - 1$ leaves). Use them to discuss mixing and show that $S_n$ is a $\log n$-bottleneck.

**Solution**:
1. Order vertices so that the center is $1$ and the leaves are $2,\dots,n$. Then $P_{1j}=1/(n-1)$ for $j\ge 2$, $P_{j1}=1$ for $j\ge 2$, and all other entries are $0$.
2. The non-zero part of the dynamics lives in the two-dimensional subspace spanned by the center indicator and the all-leaves average. On that subspace, the walk alternates between center and leaves, yielding eigenvalues $1$ and $-1$.
3. Any vector supported on leaves whose coordinates sum to $0$ is sent to $0$ in one step, so $0$ is an eigenvalue with multiplicity $n-2$.
4. Therefore
   $$
   \mathrm{spec}(P)=\{1,-1,0,\dots,0\}.
   $$
5. The presence of the eigenvalue $-1$ shows that the ordinary random walk on the star is periodic, hence it does **not** mix in the usual sense.
6. For the lazy walk, the eigenvalues become
   $$
   \{1,0,1/2,\dots,1/2\},
   $$
   so the second-largest eigenvalue in absolute value is $1/2$, and the lazy chain mixes rapidly.
7. The bottleneck statement is not really about the spectral gap here; it is about the tiny leaf-to-leaf transition probability. In exactly two steps,
   $$
   (P^2)_{ij}=\frac{1}{n-1}
   \qquad (i\neq j\text{ leaves}).
   $$
8. By Lemma 5.1, a task that must send information from one leaf to another pays at least
   $$
   -\log_2\!\left(\frac{1}{n-1}\right)=\log_2(n-1)=\Theta(\log n)
   $$
   bits of complexity. That is the sense in which the star is a logarithmic bottleneck. $\blacksquare$

#### Exercise 3.6: $L$-Step Walk Counting via $A^L$
**Task**: On the path $P_4$ with vertices $\{1, 2, 3, 4\}$, count the number of length-$3$ walks from vertex $1$ to vertex $4$ both combinatorially and via $(A^3)_{14}$.

**Solution**:
1. $A = \begin{pmatrix} 0 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$.
2. $A^2 = \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 2 & 0 & 1 \\ 1 & 0 & 2 & 0 \\ 0 & 1 & 0 & 1 \end{pmatrix}$ — entry $(A^2)_{14} = 0$ (no length-$2$ walk between $1$ and $4$, distance is $3$).
3. $A^3 = A^2 \cdot A$. Compute the $(1, 4)$ entry: $(A^3)_{14} = \sum_k (A^2)_{1k} A_{k4} = 1 \cdot 0 + 0 \cdot 0 + 1 \cdot 1 + 0 \cdot 0 = 1$.
4. **Combinatorial check**: the unique length-$3$ walk from $1$ to $4$ in $P_4$ is $1 \to 2 \to 3 \to 4$. Count is $1$. ✓
5. **Probability via $P^3$**: since $P = D^{-1} A$ with $D = \mathrm{diag}(1, 2, 2, 1)$ on $P_4$, we have $(P^3)_{14} = \frac{1}{1} \cdot \frac{1}{2} \cdot \frac{1}{2} \cdot 1 = 1/4$, matching the *probability* of taking this unique walk.
6. By Lemma 5.1, any task on $P_4$ requiring information from vertex $4$ at vertex $1$ at depth $L = 3$ has $\mathrm{MPC} \geq -\log_2(1/4) = 2$ bits. $\blacksquare$

---

## Chapter 4: The Lossy Weisfeiler–Leman Operator (LossyWL)

### 4.1 The Communication Channel Analogy: GNN Edges as Binary Erasure Channels (BEC)
Let us design a probabilistic refinement operator $\mathrm{LossyWL}$ by treating every edge in the graph as a **noisy communication channel**.

In information theory, the **Binary Erasure Channel (BEC)** is a simple model where a transmitter sends a bit, and the receiver either receives the bit correctly (with survival probability $p$) or receives an erasure symbol $\mathbf{e}$ (with erasure probability $1-p$).

Let us apply this principle to GNN message passing:
- For every directed edge $(u, v)$ in the graph, we introduce a message survival indicator variable $Z_{uv}^l \sim \mathrm{Bernoulli}(I_{vu})$.
- $Z_{uv}^l = 1$ indicates that the structural message successfully transitions.
- $Z_{uv}^l = 0$ indicates that the message is completely erased.

The transition probability $I_{vu}$ represents the **topological bandwidth** of the edge. For standard GNNs, this bandwidth is determined by vertex degrees (local routing bottlenecks):
$$I_{vu} := \frac{A_{vu}}{\text{deg}(v)}$$
For GNNs with self-loops:
$$I_{vv} := \frac{1}{\text{deg}(v) + 1}$$

To make the formalism fully precise, we adjoin a distinguished erasure symbol $\bot$ to the color space and write
$$
\mathcal{X}_\bot := \mathcal{X} \cup \{\bot\}.
$$
Define the erasure operator
$$
\operatorname{erase}(z,x) :=
\begin{cases}
 x & \text{if } z=1,\\
 \bot & \text{if } z=0.
\end{cases}
$$
This lets us speak about message loss without pretending that symbolic colors can literally be multiplied by Bernoulli variables.

### 4.2 Formal Hashing Mechanics and the Probabilistic Hashing Sequence of LossyWL

#### Definition 4.1 (LossyWL Operator - Kemper et al. 2025)
Let $G = (V, E)$ be a finite graph. The **LossyWL** vertex states $\mathrm{LossyWL}_v^l$ are random variables recursively defined on the product probability space induced by $\{Z_{uv}^l\}$ as follows:

1. **Depth 0 (Initial Colors)**:
   $$\mathrm{LossyWL}_v^0 := c_v^{(0)}$$
2. **Depth $l$ (Refinement)**:
   We define the (potentially erased) message from $u$ to $v$ at step $l$ as
   $$m_{u \to v}^l := \operatorname{erase}\!\big(Z_{uv}^l,\, \mathrm{LossyWL}_u^{l-1}\big),$$
   where $Z_{uv}^l \sim \mathrm{Bernoulli}(I_{vu})$ are independent random variables.
   The color of vertex $v$ at step $l$ is obtained by applying an injective hashing function:
   $$\mathrm{LossyWL}_v^l := \text{hash}\left( m_{v \to v}^l, \{\!\{ m_{u \to v}^l \mid u \in \mathcal{N}(v) \}\!\} \right).$$

A reader may think of this as ordinary 1-WL in which each incoming message is either delivered faithfully or replaced by the special token $\bot$.

---

### 4.3 The Deduction Operator $\vDash$ and Probabilistic Resolution Events
Under `LossyWL`, the colors are random variables, which induces a **probability space over partitions** $\text{Part}(V)$. Let $S$ denote the finite seed space of all realizations of the Bernoulli survival variables, and let $\mu_S$ be the corresponding product measure on $S$. For a concrete realization $s \in S$, the LossyWL coloring $\mathrm{LossyWL}_v^L(\cdot, s)$ is deterministic.

The key semantic question is: when does a concrete lossy color at $v$ determine the task label? We formalize this through the deduction relation
$$\mathrm{LossyWL}_v^L(G, s) \vDash_V f_v(G) \iff \Big( \forall w \in V, \, \forall t \in S: \mathrm{LossyWL}_v^L(G, s) = \mathrm{LossyWL}_w^L(G, t) \implies f(v) = f(w) \Big).$$
In words: **whenever the observed lossy color of $v$ could also have appeared at some other vertex $w$ under some seed $t$, that other vertex must carry the same task label**. So the color class represented by $\mathrm{LossyWL}_v^L(G,s)$ is label-pure for the task under consideration.

This operator defines a precise event in the seed probability space. Its probability is
$$
\mathbb{P}\left( \mathrm{LossyWL}_v^L \vDash_V f_v \right)
= \sum_{s \in S} \mu_S(s)\, \mathbf{1}\{\mathrm{LossyWL}_v^L(G,s) \vDash_V f_v\}.
$$
Only in the special case where all seeds are equally likely does this reduce to simple counting. This allows us to define Message-Passing Complexity exactly:
$$MPC_{\mathcal{A}}(f_v, G) := -\log \mathbb{P}\left( \mathrm{LossyWL}_v^L \vDash_V f_v \right).$$

---

### Section 4 Exercises (With Complete, Rigorous Solutions)

#### Exercise 4.1: Indistinguishability Probability on a Simple Graph
**Task**: Let $G = P_2$ (two connected vertices, $1-2$) with a constant initial coloring $c_1^{(0)} = c_2^{(0)} = 1$. The task is $f(1) = 1, f(2) = 0$. Let $L = 1$, and transition probability $I_{vu} = 0.5$ for all edges. Calculate the exact probability that $\mathrm{LossyWL}_1^1 \vDash f$.

**Solution**:
1. At $L=1$, the messages are:
   - Self-loops: $m_{1 \to 1}^1 = \operatorname{erase}(Z_{11}^1,1)$ and $m_{2 \to 2}^1 = \operatorname{erase}(Z_{22}^1,1)$.
   - Cross-edges: $m_{2 \to 1}^1 = \operatorname{erase}(Z_{21}^1,1)$ and $m_{1 \to 2}^1 = \operatorname{erase}(Z_{12}^1,1)$.
2. The seed space consists of all combinations of $Z_{11}^1, Z_{22}^1, Z_{21}^1, Z_{12}^1$. There are $2^4 = 16$ equally likely seeds.
3. For the task $f$ to be resolved, the GNN must produce different colors for node 1 and node 2:
   $$\mathrm{LossyWL}_1^1 \neq \mathrm{LossyWL}_2^1$$
4. Let us examine the colors:
   - $\mathrm{LossyWL}_1^1 = \text{hash}(\operatorname{erase}(Z_{11}^1,1), \{\!\{ \operatorname{erase}(Z_{21}^1,1) \}\!\})$.
   - $\mathrm{LossyWL}_2^1 = \text{hash}(\operatorname{erase}(Z_{22}^1,1), \{\!\{ \operatorname{erase}(Z_{12}^1,1) \}\!\})$.
5. They are equal if and only if $Z_{11}^1 = Z_{22}^1$ and $Z_{21}^1 = Z_{12}^1$.
6. There are 4 seeds where this equality holds:
   - $(0, 0, 0, 0)$, $(1, 1, 0, 0)$, $(0, 0, 1, 1)$, $(1, 1, 1, 1)$.
7. For these 4 seeds, $\mathrm{LossyWL}_1^1 = \mathrm{LossyWL}_2^1$, meaning we cannot deduce $f$ (we would make an error since their target labels differ).
8. For the other 12 seeds, the colors differ, meaning we can perfectly partition them and resolve $f$.
9. Thus, the resolution probability is:
   $$\mathbb{P}(\mathrm{LossyWL}_1^1 \vDash f) = \frac{12}{16} = 0.75$$
10. The resulting MPC is:
    $$MPC = -\log_2(0.75) \approx 0.415 \text{ bits}$$
This completes the numerical proof. $\blacksquare$

#### Exercise 4.2: Self-Loop Transition Probability on $P_3$
**Task**: Let $G = P_3$ with vertices $1 - 2 - 3$, no self-loops in the graph but **add self-loops** for LossyWL. Compute $I_{vu}$ for every directed message including self-loops, and verify $\sum_u I_{vu} = 1$ for each $v$.

**Solution**:
1. With self-loops, the effective degree of each vertex is $\mathrm{deg}_G(v) + 1$: $\mathrm{deg}_{\mathrm{eff}}(1) = 2$, $\mathrm{deg}_{\mathrm{eff}}(2) = 3$, $\mathrm{deg}_{\mathrm{eff}}(3) = 2$.
2. Edge transition probabilities $I_{vu} = A_{vu} / \mathrm{deg}_{\mathrm{eff}}(v)$ for $u \in \mathcal{N}_G(v) \cup \{v\}$:
   - $I_{11} = 1/2$, $I_{12} = 1/2$, all other $I_{1u} = 0$.
   - $I_{21} = 1/3$, $I_{22} = 1/3$, $I_{23} = 1/3$, all other $I_{2u} = 0$.
   - $I_{32} = 1/2$, $I_{33} = 1/2$, all other $I_{3u} = 0$.
3. **Row-stochasticity check**: $\sum_u I_{1u} = 1/2 + 1/2 = 1$. $\sum_u I_{2u} = 1$. $\sum_u I_{3u} = 1$. ✓
4. This row-stochasticity is the property that makes $I$ the transition matrix of a *lazy random walk* on $G$ (with self-loop probability $1/\mathrm{deg}_{\mathrm{eff}}$), connecting Chapter 4's BEC model to Chapter 3's random-walk theory through Lemma 5.1. $\blacksquare$

#### Exercise 4.3: Distinguishability under LossyWL on the Triangle $C_3$
**Task**: Let $G = C_3$ with constant initial coloring $c_v^{(0)} = \star$ and uniform $I_{vu} = 1/3$ (with self-loops). Compute the probability that LossyWL at depth $L = 1$ distinguishes vertex $1$ from vertex $2$.

**Solution**:
1. Each vertex sends 3 messages (one self, two to neighbors) at layer $1$. Vertex $v$ receives $3$ messages: $m_{v\to v}, m_{u_1 \to v}, m_{u_2 \to v}$ where $u_1, u_2$ are the two graph-neighbors.
2. With $c^{(0)} = \star$ constant, the message values are $\operatorname{erase}(Z_{vu}^1,\star)$. Effectively each message is $\star$ (if $Z = 1$) or $\bot$ (if $Z = 0$, the erasure symbol).
3. The LossyWL color at vertex $v$ is $\mathrm{hash}(m_{vv}, \{\!\{m_{u_1 v}, m_{u_2 v}\}\!\})$. Two vertices receive the same color iff the *pair* (self-message, multiset of neighbor-messages) coincides.
4. Vertex $1$ has neighbors $\{2, 3\}$, vertex $2$ has neighbors $\{1, 3\}$. Define survival variables:
   - At vertex $1$: $S_1 := (Z_{11}^1, \{\!\{Z_{21}^1, Z_{31}^1\}\!\})$.
   - At vertex $2$: $S_2 := (Z_{22}^1, \{\!\{Z_{12}^1, Z_{32}^1\}\!\})$.
5. Each $Z$ is independent Bernoulli$(1/3)$; the seed space has $2^6 = 64$ atoms, but they are **not** equiprobable. Probabilities must be computed with the product Bernoulli measure.
6. We need $\Pr[\mathrm{color}(1) \neq \mathrm{color}(2)] = \Pr[\mathrm{hash}(S_1) \neq \mathrm{hash}(S_2)]$. Under injective hashing this equals $\Pr[S_1 \neq S_2]$.
7. $S_1 = S_2$ iff $Z_{11} = Z_{22}$ **and** the multisets $\{\!\{Z_{21}, Z_{31}\}\!\} = \{\!\{Z_{12}, Z_{32}\}\!\}$.
8. Self-equality: $\Pr[Z_{11} = Z_{22}] = (1/3)^2 + (2/3)^2 = 1/9 + 4/9 = 5/9$.
9. Multiset equality: each multiset has 2 elements from $\{0, 1\}$. Both equal $\{\!\{1,1\}\!\}$ with probability $(1/3)^2 = 1/9$; both equal $\{\!\{0,0\}\!\}$ with probability $(2/3)^2 = 4/9$; both equal $\{\!\{0,1\}\!\}$ with probability $2 \cdot 1/3 \cdot 2/3 = 4/9$. The joint probability that *both* multisets are equal: sum over multiset types of $\Pr[\mathrm{multiset}_1 = t] \cdot \Pr[\mathrm{multiset}_2 = t]$ = $(1/9)^2 + (4/9)^2 + (4/9)^2 = 1/81 + 16/81 + 16/81 = 33/81 = 11/27$.
10. By independence of self-loop variables from cross-edge variables: $\Pr[S_1 = S_2] = (5/9)(11/27) = 55/243$.
11. $\Pr[\mathrm{color}(1) \neq \mathrm{color}(2)] = 1 - 55/243 = 188/243 \approx 0.774$.
12. For a task $f$ with $f(1) \neq f(2)$, $\mathrm{MPC} \leq -\log_2(188/243) \approx 0.369$ bits. $\blacksquare$

#### Exercise 4.4: BEC Capacity and LossyWL Information Survival
**Task**: Recall that a Binary Erasure Channel with erasure probability $\eta$ has Shannon capacity $C(\eta) = 1 - \eta$ bits. Reinterpret LossyWL message-passing as a chain of $L$ BECs and derive the maximum information-throughput in bits per layer through the edge $(u, v)$.

**Solution**:
1. A LossyWL edge $(u, v)$ transmits a one-bit message (in the simplest binary-color regime) with survival probability $I_{vu}$, i.e.\ erasure probability $\eta = 1 - I_{vu}$.
2. **Per-layer capacity**: $C_{vu} = 1 - \eta = I_{vu}$ bits per layer per directed edge.
3. **Chain capacity**: $L$ BECs in series compose, with the surviving-bit probability multiplying: an end-to-end survival probability of $\prod_{l=1}^L I^{(l)} = I_{vu}^L$ (assuming the chain reuses the same edge each layer for path-survival).
4. The capacity of the *concatenated* chain is $C_{\mathrm{chain}}(L) = I_{vu}^L$ bits per channel use, decaying exponentially in $L$.
5. **Connection to MPC**: $\mathrm{MPC} \geq -\log_2 C_{\mathrm{chain}}(L) = L \log_2(1 / I_{vu})$ on tasks requiring a unique path through this edge — a slight variant of Lemma 5.1.
6. Hence the random-walk lower bound is equivalent to a *channel-capacity* lower bound: any task whose information must squeeze through a low-capacity bottleneck has high MPC. This is the unification of information theory (Shannon) with graph topology (random walks) that the LossyWL framework achieves. $\blacksquare$

#### Exercise 4.5: Hash Injectivity and Color Collisions
**Task**: The LossyWL update assumes an injective hash $\mathrm{hash}: \mathcal{X} \times \mathrm{MultiSet}(\mathcal{X}) \to \mathcal{X}'$. Show that if $\mathrm{hash}$ is not injective, two vertices that *should* be separated may collapse to the same color, *strictly under-estimating* the MPC.

**Solution**:
1. Let $G = P_2$ with $c_1^{(0)} = a$, $c_2^{(0)} = b$ (distinct initial colors), and a hash function with the collision $\mathrm{hash}(a, \{\!\{b\}\!\}) = \mathrm{hash}(b, \{\!\{a\}\!\}) = \xi$.
2. Under the lossless LossyWL ($I = 1$, no erasures): at layer $1$, color of vertex $1$ is $\mathrm{hash}(a, \{\!\{b\}\!\}) = \xi$, color of vertex $2$ is $\mathrm{hash}(b, \{\!\{a\}\!\}) = \xi$. They collide.
3. The induced partition at depth $1$ is therefore $\{V\}$ — a single cell, even though the true 1-WL distinguishes them at depth $0$ already.
4. Any task $f$ with $f(1) \neq f(2)$ now has $\Pr[\mathrm{LossyWL}_v^1 \vDash f] = 0$, giving $\mathrm{MPC} = \infty$ — a *false infinity* due to the hash collision.
5. **Implication**: in Tier L-I metrology (§7.6), one must use a *canonical*, provably-injective hash (e.g.\ tuple-encoding into $\mathbb{Q}$). Otherwise the floating-point hash collisions of practical GNN implementations introduce *spurious cell merges*, making the resulting partition strictly coarser than the true 1-WL partition. This is *exactly* the H3 failure mode in the C1 conjecture (§8.3): trained GNNs use continuous, non-injective representations whose induced partitions may not converge to the WL-canonical partition. $\blacksquare$

#### Exercise 4.6: Independence of Cross-Layer Survival Variables
**Task**: Prove that under Definition 4.1, the survival variables $\{Z_{uv}^l\}$ are mutually independent across both $(u, v)$ and $l$, and explain why this is the precise probabilistic ingredient that makes Theorem 7.3 (DP-LossyWL) factor.

**Solution**:
1. Definition 4.1 states $Z_{uv}^l \sim \mathrm{Bernoulli}(I_{vu})$ are *independent*. The product probability space is $\Omega = \prod_{(u, v, l)} \{0, 1\}$ with the product Bernoulli measure.
2. The joint law factorizes: $\Pr[Z_{u_1 v_1}^{l_1} = z_1, \dots, Z_{u_k v_k}^{l_k} = z_k] = \prod_{i=1}^k \Pr[Z_{u_i v_i}^{l_i} = z_i]$ for distinct triples $(u_i, v_i, l_i)$.
3. In particular, **layer independence**: the survival variable at layer $l$ is independent of all variables at layers $< l$. **Edge independence**: variables at distinct edges within the same layer are mutually independent.
4. **Why this matters for Theorem 7.3**: the recursion $dp[l][w] = 1 - (1 - dp[l-1][w]) \prod_k (1 - dp[l-1][k] I_{wk})$ uses the inclusion-exclusion formula for the *union* of independent events. The factorization $\prod_k$ over neighbors $k$ is valid **only** because $\{Z_{kw}^l : k \in \mathcal{N}(w)\}$ are mutually independent (edge independence within layer $l$). Layer independence ensures $Z_{kw}^l$ is independent of $\{dp[l-1][k'] : k' \neq w\}$, which depends only on variables at layers $\leq l - 1$.
5. Were the survival variables correlated (e.g.\ if dropout were applied simultaneously to all edges incident to a vertex), the recursion would not factor and DP-LossyWL would no longer be polynomial — it would degenerate to brute-force seed enumeration. $\blacksquare$

---

## Chapter 5: Bridging Topology to Complexity: The Over-squashing Lower Bound

### Chapter 5 Roadmap
Chapter 3 supplied the linear-algebraic and topological vocabulary. We now convert it into a complexity lower bound. The key idea is simple: if solving a task at vertex $v$ requires information from a remote source $u$, then at least one chain of successful transmissions must connect $u$ to $v$. Random-walk probabilities upper-bound the chance of such successful transmission, and negative logarithms convert those probabilities into complexity.

In this chapter we use **exactly $L$ message-passing rounds** as the default convention. If one prefers an "at most $L$ rounds" formulation, the same arguments apply after summing over lengths $0,1,\dots,L$; we comment on this explicitly in the exercises when it matters.

### 5.1 Proof of Lemma 6.13 (The Random Walk Lower Bound)
We now prove the fundamental link connecting random walks to GNN information propagation. 

Let $f_v$ be a vertex task. Under the `LossyWL` framework, every message survives independently at each step with probability $P_{ij} = D^{-1}_{ij}$. 

#### Lemma 5.1 (Random Walk Lower Bound - Lemma 6.13)
*Let $f_v$ be a task that requires node-feature information from a node $u$. Then the Message-Passing Complexity satisfies:*
$$MPC_{\mathcal{A}}(f_v, G) \ge -\log \left( (P^L)_{vu} \right)$$

*Proof.*
Let $W_{uv}$ be the event that there exists at least one path of successfully transmitted messages from $u$ to $v$ of length $L$.
Let $W_{uv}^1, W_{uv}^2, \dots, W_{uv}^M$ be all possible directed walks of length $L$ from $v$ to $u$ in $G$.
For a specific walk $w = (v = x_0, x_1, x_2, \dots, x_L = u)$, the probability that all messages along this walk survive is:
$$\mathbb{P}(W_{uv}^i) = \prod_{l=1}^L \mathbb{P}(Z_{x_{l-1}x_l}^l = 1) = \prod_{l=1}^L P_{x_l x_{l-1}}$$
This is exactly the probability of a standard random walk taking this specific path from $v$ to $u$.

Since the walks are not necessarily disjoint, the probability that *at least one* path of messages survives is bounded by the union bound:
$$\mathbb{P}(W_{uv}) = \mathbb{P}\left( \bigcup_{i=1}^M W_{uv}^i \right) \le \sum_{i=1}^M \mathbb{P}(W_{uv}^i)$$
Summing the probabilities of all possible walks of length $L$ yields the transition probability $(P^L)_{vu}$:
$$\sum_{i=1}^M \mathbb{P}(W_{uv}^i) = (P^L)_{vu}$$
If no successful walk of messages exists from $u$ to $v$, then node $v$ receives absolutely zero information from $u$. Since $f_v$ requires information from $u$ by definition, we cannot deduce $f_v$ in this case. Thus:
$$\mathbb{P}(\mathrm{LossyWL}_v^L \vDash f_v) \le \mathbb{P}(W_{uv}) \le (P^L)_{vu}$$
Taking the negative logarithm on both sides:
$$MPC_{\mathcal{A}}(f_v, G) = -\log \mathbb{P}(\mathrm{LossyWL}_v^L \vDash f_v) \ge -\log \left( (P^L)_{vu} \right) \quad \text{(Q.E.D.)}$$

---

### 5.2 Narrative Discussion: Bottlenecks, Over-squashing, and Rings
This random walk lower bound represents a profound connection between **spectral graph theory** and **deep learning limitations**. 

In graph neural networks, **over-squashing** occurs when the information from an exponentially growing neighborhood must be squeezed into a fixed-size node vector. Lemma 5.1 shows that if a task requires information from a node $u$ that is separated from $v$ by a structural bottleneck (such as a bridge in a molecular graph), the transition probability $(P^L)_{vu}$ will be extremely small, forcing the complexity $MPC$ to be very high.

---

### Section 5 Exercises (With Complete, Rigorous Solutions)

#### Exercise 5.1: Pathological Bottleneck Complexity Calculation
**Task**: Consider a star graph $S_n$ with 1 center node (index 1) and $n-1$ leaves (indices $2$ to $n$). Let $L = 2$. Let $f$ be a task on leaf node 2 that requires information from leaf node 3. Calculate the standard random walk transition probability $(P^2)_{23}$ and use Lemma 5.1 to bound the MPC.

**Solution**:
1. The transition matrix $P$ entries for a star graph are:
   - For leaf nodes $i \in \{2, \dots, n\}$, their only neighbor is the center (node 1). Hence $P_{i1} = 1.0$ and $P_{ij} = 0.0$ for all $j \neq 1$.
   - For the center node 1, its degree is $n-1$. Hence $P_{1j} = \frac{1}{n-1}$ for all leaf nodes $j \in \{2, \dots, n\}$.
2. We compute the 2-step transition probability from leaf 2 to leaf 3:
   $$(P^2)_{23} = \sum_{w=1}^n P_{2w} P_{w3}$$
3. Since $P_{2w} = 0$ for all $w \neq 1$, the sum collapses to the center node $w = 1$:
   $$(P^2)_{23} = P_{21} P_{13} = (1.0) \left( \frac{1}{n-1} \right) = \frac{1}{n-1}$$
4. Applying Lemma 5.1:
   $$MPC \ge -\log_2 \left( \frac{1}{n-1} \right) = \log_2(n-1)$$
5. As the size of the star graph $n$ grows, the complexity of leaf-to-leaf propagation grows logarithmically, representing a clear bottleneck (over-squashing at the center hub). $\blacksquare$

#### Exercise 5.2: Under-Reaching on $P_5$
**Task**: Let $G = P_5$, source $u = 1$, target $v = 5$, and depth $L = 3$. Verify that $u$ is *outside* the receptive field of $v$ and conclude that $\mathrm{MPC} = \infty$ via the random-walk lower bound.

**Solution**:
1. Distance: $d_G(u, v) = 4$ (path $1 - 2 - 3 - 4 - 5$ has length $4$).
2. Receptive field of $v$ at depth $L = 3$: $\mathcal{N}_3(5) = \{2, 3, 4, 5\}$, which does *not* include $u = 1$.
3. **Walk count**: any walk of length $\leq 3$ from $5$ visits only vertices in $\mathcal{N}_3(5)$. There is no length-$3$ walk from $5$ to $1$ (would require length $\geq 4$). Hence $(P^3)_{51} = 0$.
4. By Lemma 5.1: $\mathrm{MPC} \geq -\log_2 0 = +\infty$. ✓
5. **Information-theoretic interpretation**: at depth $L = 3$, the LossyWL color of $v$ is a measurable function of survival variables on $E_T(v, 3)$, none of which touch vertex $u$. Hence $\mathrm{LossyWL}_v^3$ is *independent* of $c_u^{(0)}$, and no task depending on $c_u^{(0)}$ is resolvable.
6. This is the precise rephrasing of Corollary 7.4 (under-reaching) inside the random-walk language of Chapter 5. $\blacksquare$

#### Exercise 5.3: Random Walk Lower Bound on $C_6$ at Antipodal Pair
**Task**: For $C_6$ with vertices $\{0, 1, 2, 3, 4, 5\}$ in cyclic order, compute $(P^L)_{03}$ for $L = 3, 5, 7$, and verify the parity / bipartite behavior. Conclude MPC bounds for the task $f(0) = c_3^{(0)}$.

**Solution**:
1. The transition matrix on $C_6$ is $P = \tfrac{1}{2} A$ where $A$ is the cycle adjacency. Eigenvalues of $A$ on $C_n$ are $2 \cos(2\pi k / n)$, so on $C_6$: $\{2, 1, -1, -2, -1, 1\}$.
2. Eigenvalues of $P = A/2$: $\{1, 1/2, -1/2, -1, -1/2, 1/2\}$.
3. The antipodal pair $0, 3$ has $|u - v| = 3 = n/2$, so $\overline{\phi_k(0)} \phi_k(3) = e^{2\pi i k \cdot 3 / 6}/6 = e^{\pi i k}/6 = (-1)^k / 6$.
4. $(P^L)_{03} = \sum_{k=0}^5 \lambda_k^L (-1)^k / 6$.
5. $L = 3$: $(1)^3 - (1/2)^3 + (-1/2)^3 - (-1)^3 + (-1/2)^3 - (1/2)^3 = 1 - 1/8 - 1/8 + 1 - 1/8 - 1/8 = 2 - 1/2 = 3/2$. Divide by 6: $(P^3)_{03} = 1/4$.
6. $L = 5$: $1 - 1/32 - 1/32 + 1 - 1/32 - 1/32 = 2 - 1/8 = 15/8$. $(P^5)_{03} = 15/48 = 5/16$.
7. $L = 7$: $1 - 1/128 - 1/128 + 1 - 1/128 - 1/128 = 2 - 1/32 = 63/32$. $(P^7)_{03} = 63/192 = 21/64$.
8. The values $1/4, 5/16, 21/64$ increase toward $1/3$, not $1/6$. This is exactly what bipartite periodicity predicts: at odd times the walk is confined to the odd-parity class $\{1,3,5\}$, and within that class the mass tends toward the uniform value $1/3$.
9. **MPC lower bounds** by Lemma 5.1: $L = 3$: $\mathrm{MPC} \geq -\log_2(1/4) = 2$. $L = 5$: $\geq \log_2(16/5) \approx 1.68$. $L = 7$: $\geq \log_2(64/21) \approx 1.61$. The bound loosens with $L$ because longer walks provide additional opportunities for information to arrive. $\blacksquare$

#### Exercise 5.4: When is the Union Bound Tight?
**Task**: Discuss when the union bound used in the proof of Lemma 5.1 is exact, and construct a graph where it is strictly loose.

**Solution**:
1. Let $E_i$ be the event that the $i$-th length-$L$ walk from $v$ to $u$ survives. The proof of Lemma 5.1 uses
   $$
   \Pr\Big[\bigcup_i E_i\Big] \le \sum_i \Pr[E_i].
   $$
2. This inequality is an equality only in special cases — for example, when there is only **one** relevant walk, or more generally when the events $E_i$ are pairwise disjoint as events.
3. Edge-disjointness alone is **not** enough for equality. If $E_1$ and $E_2$ correspond to two edge-disjoint walks, then the events are independent, and
   $$
   \Pr[E_1\cup E_2] = \Pr[E_1] + \Pr[E_2] - \Pr[E_1]\Pr[E_2],
   $$
   which is strictly smaller than $\Pr[E_1]+\Pr[E_2]$ unless one of the probabilities is $0$.
4. A concrete loose example is the theta graph consisting of two endpoints joined by two internally disjoint paths of length $2$. If each path survives with probability $1/4$, then
   $$
   \Pr[E_1\cup E_2] = \frac14 + \frac14 - \frac1{16} = \frac7{16},
   $$
   whereas the union bound gives $1/2$.
5. Thus the union bound in Lemma 5.1 should be interpreted as an **upper bound on successful propagation probability**, not as an exact formula in general. Its value is that it converts combinatorial walk structure into a clean, always-valid lower bound on MPC. $\blacksquare$

#### Exercise 5.5: Multiple Sources — Joint Propagation Lower Bound
**Task**: Extend Lemma 5.1 to tasks $f_v$ depending on the initial colors of *multiple* sources $u_1, \dots, u_k$. State a lower bound on $\mathrm{MPC}_{\mathcal{A}}(f_v, G)$ involving the joint random-walk transition probability.

**Solution**:
1. **Setup**: $f_v$ requires the entire tuple $(c_{u_1}^{(0)}, \dots, c_{u_k}^{(0)})$ to be resolvable.
2. The event $\{\mathrm{LossyWL}_v^L \vDash f_v\}$ requires that *every* source $u_i$ has at least one surviving length-$\leq L$ path to $v$: call this the **multi-source survival event** $W = \bigcap_{i=1}^k W_{u_i v}$.
3. By the union bound on the *complement*: $\Pr[W] \leq \min_i \Pr[W_{u_i v}] \leq \min_i (P^L)_{v u_i}$ — the *strictest* single-source bound.
4. A tighter (but still upper) bound assuming independence of single-source survival events: $\Pr[W] \leq \prod_i (P^L)_{v u_i}$. This is **strictly tighter** than the min-bound whenever $k \geq 2$ and the bound is non-trivial.
5. **Lower bound on MPC**: $\mathrm{MPC}(f_v, G) \geq -\log_2 \Pr[W] \geq -\sum_i \log_2 (P^L)_{v u_i} = \sum_i \mathrm{MPC}_i$, where $\mathrm{MPC}_i$ is the single-source lower bound.
6. **Interpretation**: joint multi-source tasks pay an *additive* surprisal cost in MPC — each source contributes independently to the difficulty. This is the formal statement of the **Task Triangle Inequality** (Lemma in Kemper et al.\ 2025): $\mathrm{MPC}(f \| g) \leq \mathrm{MPC}(f) + \mathrm{MPC}(g)$, here applied to the special case where $f \| g$ has joint-source dependence. $\blacksquare$

#### Exercise 5.6: Bottleneck Edge Removes Information Linearly with Depth
**Task**: Consider the **dumbbell graph**: two cliques $K_n$ joined by a single bridge edge. For a task on one clique requiring information from the other, derive the depth-dependence of the MPC lower bound and explain why over-squashing is mathematically inevitable here.

**Solution**:
1. Let $v \in K_n^{(L)}$ (left clique), $u \in K_n^{(R)}$ (right clique), and let $b_L \in K_n^{(L)}$, $b_R \in K_n^{(R)}$ be the bridge endpoints (so the bridge edge is $b_L - b_R$).
2. Every walk from $v$ to $u$ of length $\leq L$ must cross the bridge at least once.
3. At each crossing, the survival probability is $I_{b_R b_L} = 1 / \mathrm{deg}(b_L)$. Since $b_L$ has degree $n$ inside the clique plus $1$ for the bridge, $I_{b_R b_L} = 1/n$.
4. The walk probability $(P^L)_{vu}$ is bounded by the probability that a walk crosses the bridge in time and reaches $u$, which is at most $(1/n)$ times the inside-clique transition density. A more careful bound: $(P^L)_{vu} = O(1/n)$ to leading order, with prefactor depending on the within-clique mixing time.
5. **Lower bound on MPC**: $\mathrm{MPC} \geq -\log_2 (P^L)_{vu} \geq \log_2 n + O(1)$ for $L$ comparable to the diameter.
6. **Depth dependence**: as $L$ grows beyond the diameter (say $L = 2\,\mathrm{diam}$), additional walks through the bridge contribute, but their survival probabilities multiply at each crossing. A walk that crosses the bridge $k$ times pays a factor $(1/n)^k$. Hence $(P^L)_{vu}$ does *not* grow linearly with $L$ — it saturates near $1/n$ (the bridge bandwidth dominates).
7. **Conclusion**: the bridge enforces a hard *over-squashing ceiling*: no matter how deep the GNN, the information transmitted across the bridge per layer is bounded by $\log_2(1/n) = -\log_2 n$ bits, and the cumulative MPC remains $\Omega(\log n)$. Adding a virtual node would create a $1$-hop "shortcut" between cliques, reducing the bound to $O(\log |V|)$ (Corollary 7.7).
8. This is the precise PA-MPC quantification of the Alon–Yahav (2021) over-squashing observation: structural bottlenecks impose *information-theoretic* limits that no amount of depth can overcome. $\blacksquare$

---

## Chapter 6: Bayesian Decision Theory, Purity, and Metrology

### 6.1 Bayesian Classification Error on Partitions
Let $V$ be the vertex set under uniform probability $\mu(v) = 1/|V|$. Let $f: V \to \{0, 1\}$ be the binary target label.
Let $\Pi$ be a partition of $V$, representing the GNN-induced stable partition. 

Any classifier that factors through the partition $\Pi$ (meaning it must output the same prediction for all vertices in the same cell) is a function $g: \Pi \to \{0, 1\}$. We wish to find a predictor $g^*$ that minimizes the classification error:
$$\varepsilon_\Pi^* = \min_{g: \Pi \to \{0, 1\}} \mathbb{P}(g(C(v)) \neq f(v))$$

#### Definition 6.1 (Bayes-Optimal Partition Predictor)
For any cell $C \in \Pi$, the **Bayes-optimal decision rule** $g^*$ is:
$$g^*(C) := \begin{cases} 1 & \text{if } P_C \ge 1/2 \\ 0 & \text{if } P_C < 1/2 \end{cases}$$
where $P_C = \frac{1}{|C|} \sum_{v \in C} f(v)$ is the posterior probability of label $1$ given cell $C$.

#### Theorem 6.1 (Optimality of the Bayes Rule)
*The predictor $g^*$ achieves the minimum possible classification error among all partition-measurable functions.*

*Proof.*
Let $g: \Pi \to \{0, 1\}$ be any arbitrary predictor. We can express the error probability as:
$$\mathbb{P}(g(C(v)) \neq f(v)) = \sum_{C \in \Pi} q_C \mathbb{P}(g(C) \neq f(v) \mid v \in C)$$
For a fixed cell $C$:
- If $g(C) = 1$, the conditional error rate is:
  $$\mathbb{P}(1 \neq f(v) \mid v \in C) = \mathbb{P}(f(v) = 0 \mid v \in C) = 1 - P_C$$
- If $g(C) = 0$, the conditional error rate is:
  $$\mathbb{P}(0 \neq f(v) \mid v \in C) = \mathbb{P}(f(v) = 1 \mid v \in C) = P_C$$

Thus, to minimize the error rate for each cell $C$, we must choose:
$$g(C) = \text{argmin}_{y \in \{0,1\}} \mathbb{P}(y \neq f(v) \mid v \in C)$$
Comparing the two cases:
- We choose $1$ if $1 - P_C \le P_C \iff P_C \ge 1/2$.
- We choose $0$ if $P_C < 1/2$.
This is exactly the definition of $g^*(C)$. The resulting minimal cell error is $\min(P_C, 1 - P_C)$. Summing over all cells:
$$\varepsilon_\Pi^* = \sum_{C \in \Pi} q_C \min(P_C, 1 - P_C)$$
Since this minimizes the error term-by-term for every cell, no other function can achieve a lower total error. $\blacksquare$

---

### 6.2 The $MI^2$ Cautionary Lemma & Purity Collapsing
In classical GNN literature, alignment between a task and a GNN representation has often been evaluated using $MI^2$ (Mutual Information-like variance alignment):
$$\mathrm{MI}^2(f;\Pi) := \frac{\sum_C q_C \cdot 2P_C(1-P_C)}{2\,\mathrm{Var}_\mu f}$$

#### Theorem 6.2 (Purity Collapse of $MI^2$)
*If a partition $\Pi$ is pure for a task $f$, and $f$ is non-constant on $G$, then:*
$$\mathrm{MI}^2(f;\Pi) = 0$$

*Proof.*
1. Since the partition $\Pi$ is **pure** for the task $f$, the target label is constant on every cell $C \in \Pi$.
2. By definition of cell purity, the posterior probability of the positive class for any cell $C$ must be either $0$ or $1$:
   $$P_C \in \{0, 1\} \quad \forall C \in \Pi$$
3. Let us evaluate the numerator of $\mathrm{MI}^2$:
   $$\sum_{C \in \Pi} q_C \cdot 2 P_C(1 - P_C)$$
4. For every cell $C$, if $P_C = 0 \implies P_C(1-P_C) = 0$. If $P_C = 1 \implies P_C(1-P_C) = 0$.
5. Thus, the product $P_C(1-P_C)$ is identically $0$ for all blocks.
6. The numerator evaluates to:
   $$\sum_{C \in \Pi} q_C \cdot 2(0) = 0$$
7. Since $f$ is non-constant, $\mathrm{Var}_\mu f > 0$. Thus:
   $$\mathrm{MI}^2(f;\Pi) = \frac{0}{2\,\mathrm{Var}_\mu f} = 0 \quad \text{(Q.E.D.)}$$

---

### 6.3 Resolution of Metrological Crises via the Depth Information Gap (DIG)
This purity collapse reveals an important limitation of $MI^2$ in GNN metrology.

When a GNN successfully learns a task perfectly (achieving purity), the $MI^2$ value collapses to $0$. In other words, $MI^2$ becomes hard to interpret precisely in the regime where one most wants a performance-aligned diagnostic.

This is why **DIG (conditional entropy)** is so useful. Under purity, DIG satisfies:
$$\mathrm{DIG}(f \mid \Pi) = \sum_C q_C H_{\mathrm{bin}}(P_C) = 0$$
Unlike $MI^2$, DIG approaches $0$ monotonically as the partition becomes more informative for the task, so it remains aligned with the operational notion of "residual uncertainty" throughout the learning process.

#### Chapter 6 Summary Box
For binary tasks and a fixed partition $\Pi$, the practical lessons of this chapter are:
- the best partition-measurable classifier is the Bayes rule applied cell by cell;
- the Bayes error equals the weighted minority mass inside the cells;
- DIG is the entropy version of cell impurity and vanishes exactly at purity;
- the bridge inequality converts DIG into lower and upper control on achievable error;
- variance-based surrogates may still be useful, but they do not replace the entropy-based bound.

---

### Section 6 Exercises (With Complete, Rigorous Solutions)

#### Exercise 6.1: Step-by-Step Proof of Theorem 6.1 under Non-Uniform Measure
**Task**: Prove that the Bayes-optimal decision rule $g^*$ minimizes the error rate even when the vertex distribution $\mu$ is non-uniform (i.e., we are given an arbitrary probability mass function $w(v)$ on $V$ such that $\sum w(v) = 1$).

**Solution**:
1. Let $\mu(v) = w(v)$ be the probability of selecting vertex $v$.
2. For any cell $C \in \Pi$, the mass of the cell is $q_C = \sum_{v \in C} w(v)$.
3. The posterior probability of the positive class in cell $C$ is:
   $$P_C = \mathbb{P}(f(v) = 1 \mid v \in C) = \frac{\sum_{v \in C} w(v) f(v)}{\sum_{v \in C} w(v)}$$
4. Let $g: \Pi \to \{0, 1\}$ be any predictor. The total error rate is:
   $$\mathbb{P}(g(C(v)) \neq f(v)) = \sum_{C \in \Pi} q_C \mathbb{P}(g(C) \neq f(v) \mid v \in C)$$
5. For a fixed cell $C$:
   - If $g(C) = 1$, the error probability inside the cell is $\mathbb{P}(f(v) = 0 \mid v \in C) = 1 - P_C$.
   - If $g(C) = 0$, the error probability inside the cell is $\mathbb{P}(f(v) = 1 \mid v \in C) = P_C$.
6. To minimize the error, we must choose $g(C) = 1$ if and only if:
   $$1 - P_C \le P_C \iff 1 \le 2 P_C \iff P_C \ge 1/2$$
7. This is identical to the uniform case. Thus, the Bayes-optimal decision rule remains $g^*(C) = \mathbf{1}[P_C \ge 1/2]$ under any non-uniform measure. $\blacksquare$

#### Exercise 6.2: Bayes Error on a 3-Cell Partition
**Task**: Let $V = \{1, \dots, 10\}$ under uniform measure. Let $f$ be the binary task $f^{-1}(1) = \{1, 2, 3, 4, 5, 6, 7\}$. Let $\Pi = \{C_1, C_2, C_3\}$ with $C_1 = \{1, 2, 3, 4\}, C_2 = \{5, 6, 7, 8\}, C_3 = \{9, 10\}$. Compute $\varepsilon^*_\Pi$, identify the Bayes-optimal cell predictor, and confirm Theorem 6.1 numerically.

**Solution**:
1. Cell masses: $q_{C_1} = 0.4, q_{C_2} = 0.4, q_{C_3} = 0.2$.
2. Cell posteriors: $P_{C_1} = 4/4 = 1$ (all four are positive), $P_{C_2} = 3/4 = 0.75$ (vertices $5, 6, 7$ positive; vertex $8$ negative), $P_{C_3} = 0/2 = 0$.
3. Bayes rule: $g^*(C_1) = 1$ (since $P \geq 1/2$), $g^*(C_2) = 1$, $g^*(C_3) = 0$.
4. Cell errors: $C_1$: $1 - P_{C_1} = 0$. $C_2$: $1 - P_{C_2} = 0.25$. $C_3$: $P_{C_3} = 0$.
5. $\varepsilon^*_\Pi = 0.4 \cdot 0 + 0.4 \cdot 0.25 + 0.2 \cdot 0 = 0.1$ (i.e.\ $10\%$ error).
6. **Verification of optimality**: try the alternative $g'(C_2) = 0$. Cell error becomes $P_{C_2} = 0.75$, contributing $0.4 \cdot 0.75 = 0.30$ instead of $0.10$ — worse by $0.20$. Other reassignments worsen the total error further. ✓
7. **DIG check**: $\mathrm{DIG} = 0.4 \cdot 0 + 0.4 \cdot H_{\mathrm{bin}}(0.75) + 0.2 \cdot 0 = 0.4 \cdot 0.8113 \approx 0.3245$ bits.
8. **Theorem 1**: $H_{\mathrm{bin}}^{-1}(0.3245) \approx 0.06 \leq 0.1 \leq 0.3245 / 2 = 0.162$. Both halves hold. ✓ $\blacksquare$

#### Exercise 6.3: Plug-In Predictor and Sample-Complexity Hint
**Task**: Suppose we observe only $N$ labeled samples per cell and estimate $\hat{P}_C = \hat{n}_C^+ / N$. Quantify the worst-case excess error of the *plug-in* predictor $\hat{g}(C) = \mathbf{1}[\hat{P}_C \geq 1/2]$ relative to the Bayes-optimal $g^*$ on a cell with true posterior $P_C \in [0, 1]$.

**Solution**:
1. **Excess cell error** is $\Delta_C := \Pr[\hat{g}(C) \neq y \mid v \in C] - \Pr[g^*(C) \neq y \mid v \in C]$.
2. $\hat{g}$ and $g^*$ agree iff $\hat{P}_C \geq 1/2 \Leftrightarrow P_C \geq 1/2$. Disagreement occurs only when $\hat{P}_C, P_C$ lie on opposite sides of $1/2$.
3. Whenever they disagree, the *cell error* of $\hat{g}$ exceeds Bayes by exactly $|2 P_C - 1|$ (the cell-level *margin*): if $g^* = 1$ and $\hat{g} = 0$, error jumps from $1 - P_C$ to $P_C$, a gap of $2P_C - 1$ when $P_C > 1/2$.
4. **Probability of disagreement** by Hoeffding: $\Pr[|\hat{P}_C - P_C| > t] \leq 2 \exp(-2 N t^2)$, with $t = |P_C - 1/2|$.
5. **Expected excess error in cell $C$**: $\mathbb{E}[\Delta_C] \leq |2 P_C - 1| \cdot 2 \exp(-2 N (P_C - 1/2)^2)$.
6. **Worst case over $P_C$**: optimize $g(P) = |2P - 1| \exp(-2 N (P - 1/2)^2)$. Set $\partial / \partial P = 0$: $|P - 1/2| = 1/(2\sqrt{N})$ optimum, with worst-case excess $\approx 1/\sqrt{N \cdot e}$.
7. **Conclusion**: the plug-in Bayes rule converges to the Bayes-optimal at rate $O(1/\sqrt{N})$ per cell, with worst-case cells being those whose true posterior lies $\Theta(1/\sqrt{N})$ away from $1/2$ — the *near-balanced* cells.
8. This is exactly the regime where Theorem 1's lower bound is steepest (Exercise 2.6), so PA-MPC's near-balanced cells are simultaneously the *hardest to estimate empirically* and the *most informative theoretically*. $\blacksquare$

#### Exercise 6.4: Bayes Error vs.\ Variance DIG — A Numerical Comparison
**Task**: For the partition of Exercise 6.2, compute $\widetilde{\mathrm{DIG}}$ and verify the elementary upper bound $\varepsilon^*_\Pi \leq \widetilde{\mathrm{DIG}}$.

**Solution**:
1. $\widetilde{\mathrm{DIG}} = \sum_C q_C P_C (1 - P_C) = 0.4 \cdot 1 \cdot 0 + 0.4 \cdot 0.75 \cdot 0.25 + 0.2 \cdot 0 \cdot 1 = 0.4 \cdot 0.1875 = 0.075$.
2. From Exercise 6.2, $\varepsilon^*_\Pi = 0.10$.
3. **Inequality check**: $0.10 \leq 0.075$? **No**, $0.10 > 0.075$, contradicting the (incorrect) claim that $\varepsilon^*_\Pi \leq \widetilde{\mathrm{DIG}}$.
4. **Resolution**: the correct elementary upper bound is $\varepsilon^*_\Pi \leq \frac{1}{2} \mathrm{DIG}$ (Theorem 1), *not* $\widetilde{\mathrm{DIG}}$. Indeed $\widetilde{\mathrm{DIG}}$ underestimates the Bayes error in general: for $P_C = 3/4$, $P(1-P) = 3/16 = 0.1875$ vs.\ $\min(P, 1-P) = 1/4 = 0.25 > 0.1875$.
5. **General inequality between cell quantities**: $P(1-P) \leq \min(P, 1-P)$ holds iff $\max(P, 1-P) \leq 1$ which is always true, but the *reverse* fails: variance is *strictly smaller* than the minimum on imbalanced cells.
6. **Conclusion**: PA-MPC must use the *entropy form* $\mathrm{DIG}$ for the upper bound; the variance form $\widetilde{\mathrm{DIG}}$ is convenient for monotonicity arguments (it factors cleanly under refinement) but does *not* directly bound the Bayes error. This explains why §3.2 of the paper carries both forms and why Theorem 1's upper bound is stated in DIG, not $\widetilde{\mathrm{DIG}}$. $\blacksquare$

#### Exercise 6.5: $\mathrm{MI}^2$ on Pure vs.\ Near-Pure Partitions
**Task**: Compute $\mathrm{MI}^2(f; \Pi)$ on (a) a *pure* partition where $P_C \in \{0, 1\}$ everywhere; (b) a *near-pure* partition where $P_C = 0.99$ on the unique non-pure cell. Verify Theorem 6.2 and demonstrate the operational vacuity of $\mathrm{MI}^2$.

**Solution**:
1. **(a) Pure**: take $|V| = 10$, $f^{-1}(1) = \{1, \dots, 5\}$, $\Pi = \{\{1, \dots, 5\}, \{6, \dots, 10\}\}$, $P_{C_1} = 1$, $P_{C_2} = 0$.
   - Numerator: $\sum_C q_C \cdot 2 P_C (1 - P_C) = 0.5 \cdot 0 + 0.5 \cdot 0 = 0$.
   - $\mathrm{Var}_\mu f = 0.5 \cdot 0.5 = 0.25 > 0$.
   - $\mathrm{MI}^2 = 0 / 0.5 = 0$. ✓ (Theorem 6.2 verified.)
2. **(b) Near-pure**: take $|V| = 100$, $f^{-1}(1) = \{1, \dots, 50\}$, $\Pi = \{\{1, \dots, 49, 100\}, \{50, \dots, 99\}\}$ (cells of size 50 each; cell 1 contains 49 positives and 1 negative, cell 2 contains 1 positive and 49 negatives).
   - $P_{C_1} = 49/50 = 0.98$, $P_{C_2} = 1/50 = 0.02$.
   - Numerator: $0.5 \cdot 2 \cdot 0.98 \cdot 0.02 + 0.5 \cdot 2 \cdot 0.02 \cdot 0.98 = 0.0392$.
   - $\mathrm{Var}_\mu f = 0.25$.
   - $\mathrm{MI}^2 = 0.0392 / 0.5 = 0.0784$ — nonzero, but very small.
3. **Operational vacuity**: as the partition gets *better* (more pure), $\mathrm{MI}^2 \to 0$. Practitioners using $\mathrm{MI}^2$ as a model-selection criterion would be misled into believing that *more refined* partitions are *worse* (lower MI$^2$), when in fact they are *closer to perfect*.
4. **Compare DIG**: in (a), $\mathrm{DIG} = 0$ (correctly indicating perfect resolution). In (b), $\mathrm{DIG} = 1 \cdot H_{\mathrm{bin}}(0.98) \approx 0.1414$ (small but nonzero, correctly indicating near-perfect with a tiny residual gap).
5. DIG's monotonic decay to $0$ under refinement (Exercise 2.3) makes it operationally sound; $\mathrm{MI}^2$'s non-monotonic behavior (peak somewhere in the middle, collapse at purity) makes it operationally vacuous in the very regime that PA-MPC cares about. $\blacksquare$

#### Exercise 6.6: Two-Cell Partition Sandwich Tightness
**Task**: Construct two-cell partitions parameterized by a single posterior $p \in [0, 1/2]$ and trace the trajectory of $(\mathrm{DIG}, \varepsilon^*_\Pi)$ as $p$ varies. Plot conceptually the gap $\tfrac{1}{2}\mathrm{DIG} - \varepsilon^*_\Pi$.

**Solution**:
1. **Setup**: $|V| = 2n$, $\Pi = \{C_1, C_2\}$ with $|C_1| = |C_2| = n$, $q_{C_1} = q_{C_2} = 1/2$, $P_{C_1} = 1 - p$, $P_{C_2} = p$ for $p \in [0, 1/2]$. The task is symmetric across the two cells.
2. **DIG**: $\mathrm{DIG} = 0.5 \cdot H_{\mathrm{bin}}(1 - p) + 0.5 \cdot H_{\mathrm{bin}}(p) = H_{\mathrm{bin}}(p)$ by symmetry.
3. **Bayes error**: $\varepsilon^*_\Pi = 0.5 \cdot \min(1-p, p) + 0.5 \cdot \min(p, 1-p) = \min(p, 1-p) = p$ (since $p \leq 1/2$).
4. **Upper-bound gap**: $\tfrac{1}{2}\mathrm{DIG} - \varepsilon^*_\Pi = \tfrac{1}{2} H_{\mathrm{bin}}(p) - p$. This is the function $g(p)$ from Exercise 2.1, known to be $\geq 0$ with $g(0) = g(1/2) = 0$ and strictly concave on $(0, 1/2)$.
5. **Maximum gap**: $g'(p) = \tfrac{1}{2} \log_2((1-p)/p) - 1 = 0 \Rightarrow (1-p)/p = 4 \Rightarrow p = 1/5$.
   - At $p = 1/5$: $\mathrm{DIG} = H_{\mathrm{bin}}(1/5) \approx 0.7219$ bits.
   - $\tfrac{1}{2}\mathrm{DIG} \approx 0.3610$, $\varepsilon^*_\Pi = 0.2$, gap $\approx 0.161$.
6. **Lower bound gap**: $\varepsilon^*_\Pi - H_{\mathrm{bin}}^{-1}(\mathrm{DIG}) = p - H_{\mathrm{bin}}^{-1}(H_{\mathrm{bin}}(p)) = p - p = 0$ — **the lower bound is exact on this two-cell symmetric family**.
7. **Operational moral**: on symmetric two-cell partitions, the *lower* half of Theorem 1 is exactly tight (the partition is the worst case for Fano), while the *upper* half has a peak gap of $\approx 0.16$ at $p = 1/5$. This is why Theorem 1's lower bound is the *operational* bound for tight worst-case analysis. $\blacksquare$

---

## Chapter 7: Epistemology, Dynamic Programming, and Engineering of LossyWL

The previous six chapters have built the *what* of LossyWL and PA-MPC:
the algebraic substrate (Chapter 1), the information-theoretic
machinery (Chapter 2), the spectral topology of bottlenecks (Chapter 3),
the probabilistic refinement operator (Chapter 4), the random-walk
lower bound (Chapter 5), and the Bayesian metrology of partitions
(Chapter 6). This chapter answers the *how*: how does one actually
compute these quantities, how does one indexLossyWL by an architecture
family, and how does one price structural interventions on a partition
without ever training a network? The result is a self-contained
engineering manual for Tier L-I metrology, suitable as a screening
diagnostic that runs in minutes on a CPU while a comparable training
sweep would consume tens of GPU-hours.

---

### 7.1 The Curse of Dimensionality and the Need for Engineering

Recall from §4.2 that the LossyWL coloring $\mathrm{LossyWL}_v^L$ is a
random variable defined on the product probability space induced by the
collection of independent Bernoulli survival variables
$\{Z_{uv}^l\}_{l=1,\dots,L;\, (u,v) \in E_{\mathrm{msg}}}$, where
$E_{\mathrm{msg}}$ is the set of directed messages (edges plus
self-loops). Let

$$
N_{\mathrm{msg}} \;:=\; L \cdot \sum_{v \in V} \big(\mathrm{deg}(v) + 1\big)
$$

denote the total number of message-variables across $L$ rounds. The
**seed space** $S$ — the support of the joint Bernoulli distribution —
has cardinality

$$
|S| \;=\; 2^{N_{\mathrm{msg}}}.
$$

#### Proposition 7.1 (Intractability of Naive Exact Enumeration)
*Let $G$ be a graph with $|V| = 10$ vertices, average degree
$\bar{d} = 3$, and depth $L = 4$. Then $|S| \geq 2^{160}$, exceeding
$10^{48}$ realizations.*

*Proof.* By definition,
$N_{\mathrm{msg}} = L \cdot |V| \cdot (\bar{d}+1) = 4 \cdot 10 \cdot 4 = 160$,
and $|S| = 2^{160} \approx 1.46 \times 10^{48}$. At one nanosecond per
realization a single naive sweep would require
$\sim 4.6 \times 10^{31}$ years. $\blacksquare$

The conclusion is stark: any algorithm that enumerates seeds explicitly
is non-starter even for tiny graphs. Two structural facts rescue
tractability and motivate the rest of the chapter.

1. **Local Neighborhood Isolation.** A depth-$L$ MPNN only aggregates
   information from the $L$-hop neighborhood
   $\mathcal{N}_L(v) := \{u \in V : d_G(u, v) \leq L\}$ of the target
   vertex $v$. Messages outside this set have zero influence on
   $\mathrm{LossyWL}_v^L$ and may be discarded from the seed space
   without altering the marginal law of $\mathrm{LossyWL}_v^L$.
2. **Independence of Cross-Edge Erasures.** Under
   Definition 4.1 the survival variables $Z_{uv}^l$ are mutually
   independent across $(u, v)$ and across $l$. Per-edge independence is
   exactly the algebraic ingredient that converts probability
   computations into a tree-recursive dynamic program over
   $\mathcal{N}_L(v)$.

We exploit these two facts in §7.3.

---

### 7.2 The $L$-Hop Computation Tree and Marginal Sufficiency

#### Definition 7.1 (Rooted Computation Tree)
For $v \in V$ and depth $L \geq 0$, the **rooted computation tree**
$T(v, L)$ is the rooted, edge-labeled tree obtained by *unrolling* the
graph at $v$ to depth $L$:

1. The root is a copy of $v$ at level $0$.
2. For each node $w$ at level $l < L$ and each (graph) neighbor
   $u \in \mathcal{N}_G(w)$, attach a fresh copy of $u$ as a child of $w$ at
   level $l+1$, edge-labeled by the directed message $(u, w)$ and the
   layer index $l+1$ at which it is transmitted.

We write $|E_T(v, L)|$ for the number of directed edges of $T(v, L)$.

#### Lemma 7.2 (Marginal Sufficiency of the Computation Tree)
*Let $v \in V$ and $L \geq 0$. The marginal distribution of the random
variable $\mathrm{LossyWL}_v^L$ is determined by the survival variables
indexed by the edges of $T(v, L)$, i.e.\ by*
$\big\{Z_{uw}^{l} : (u, w, l) \in E_T(v, L)\big\}$.

*Proof.* Definition 4.1 unrolls into the recurrence
$\mathrm{LossyWL}_v^l =
\mathrm{hash}\!\big(m_{v\to v}^l, \{\!\{m_{u\to v}^l : u \in \mathcal{N}(v)\}\!\}\big)$.
By induction on $l$, $\mathrm{LossyWL}_v^l$ is a measurable function of
the survival variables along the rooted subtree $T(v, l)$. The leaves
$T(v, 0)$ carry the initial colors $c_v^{(0)}$, which are deterministic.
No survival variable outside $E_T(v, L)$ appears in the recurrence, so
the marginal law of $\mathrm{LossyWL}_v^L$ depends only on those listed.
$\blacksquare$

Lemma 7.2 is the formal license to replace the global seed space $S$
of cardinality $2^{N_{\mathrm{msg}}}$ by a *local* seed space
$S_v := \{0, 1\}^{|E_T(v, L)|}$ when computing per-vertex resolution
probabilities. For node-level tasks this typically drops the exponent
from $\Theta(L \cdot |V| \cdot \bar{d})$ to
$\Theta(\bar{d}^L)$ — still exponential, but small enough to make small
anchor graphs (Petersen, $P_4..P_{12}$, $C_3..C_8$) tractable in exact
rational arithmetic.

---

### 7.3 Dynamic Programming for LossyWL (DP-LossyWL)

For an important and frequently arising sub-class of tasks — those that
reduce to *information propagation* from a marked source $u$ to a
target $v$ — Lemma 7.2 is not sufficient: we want the *propagation
probability* itself, not the full law of the color. The propagation
probability admits an exact polynomial-time dynamic program.

#### Definition 7.2 (Propagation Probability)
For $u, v \in V$ and depth $L$, the **propagation probability** is
$$
p_L(v \,|\, u) \;:=\; \Pr\!\big[\,\exists\text{ a path of length } \leq L
\text{ along which every message survives from } u \text{ to } v\,\big].
$$

When this probability is zero, the LossyWL coloring of $v$ contains
*no information* from $u$ at depth $L$, hence any task $f_v$ that
depends on $u$ has $\mathrm{MPC} = \infty$ (Corollary 7.4 below).

#### Theorem 7.3 (DP-LossyWL on the Unrolled Computation Tree)
*Fix a source $u \in V$, a target $v \in V$, and a depth $L \geq 0$. On the rooted computation tree $T(v,L)$, define*
$$
dp[l][w] \;:=\; \Pr\!\big[\,\text{a surviving tree-path of length } \le l
\text{ exists from the source copy of } u \text{ to the node } w\,\big],
\qquad l=0,1,\dots,L.
$$
*Then $dp$ satisfies the boundary condition*
$$
dp[0][w] = \mathbf{1}[w=u]
$$
*and the recurrence*
$$
dp[l][w] = 1 - \big(1-dp[l-1][w]\big)
\prod_{k\in\mathcal{N}(w)} \Big(1-dp[l-1][k]I_{wk}\Big).
$$
*The table is computable in time $O\!\big(L\cdot |E_T(v,L)|\big)$ and space $O\!\big(|V_T(v,L)|\big)$. The recurrence is exact for the unrolled tree model, and therefore exact for graphs whose relevant $L$-hop computation subgraph is tree-like. On general loopy graphs it should be interpreted as a tractable tree-based surrogate for propagation probability rather than an unconditional exact formula for the original graph event.*

*Proof.*
The boundary condition is the definition of a length-$0$ tree-path. On the unrolled computation tree, different children of a node correspond to different incoming message channels at the next layer. Hence the relevant survival events factor exactly across children.

Let $A_0$ be the event that the source has already reached $w$ within $l-1$ steps, and for each child-channel $k\to w$ let $A_k$ be the event that the source has reached $k$ within $l-1$ steps and that the layer-$l$ transmission $Z_{kw}^l=1$ succeeds. Because these channels are distinct in the unrolled tree, the events are independent at the level needed for the product formula. Therefore
$$
\Pr\!\Big[A_0 \cup \bigcup_{k\in\mathcal{N}(w)} A_k\Big]
= 1 - \Pr[A_0^c]\prod_{k\in\mathcal{N}(w)}\Pr[A_k^c],
$$
which yields the stated recurrence.

The complexity bound follows because each layer visits each directed edge of the unrolled tree once. Exact rational arithmetic is preserved because the recurrence uses only addition, subtraction, and multiplication of rationals. On graphs with cycles, multiple tree branches may correspond to overlapping events back in the original graph; this is precisely why we describe the recurrence as tree-exact and graph-surrogate. $\blacksquare$

#### Corollary 7.4 (Under-Reaching $\Rightarrow$ Infinite MPC)
*If $d_G(u, v) > L$ then $p_L(v \,|\, u) = 0$, and for any task $f_v$
that depends on the initial color $c_u^{(0)}$,
$\mathrm{MPC}_{\mathcal{A}}(f_v, G) = \infty$.*

*Proof.* If $d_G(u, v) > L$ no length-$\leq L$ walk between $u$ and $v$
exists, so by induction $dp[l][v] = 0$ for all $l \leq L$. The
LossyWL color of $v$ is independent of $c_u^{(0)}$, hence
$\Pr[\mathrm{LossyWL}_v^L \vDash f_v] = 0$ and the negative logarithm
diverges. $\blacksquare$

Corollary 7.4 is the precise rephrasing, inside the LossyWL framework,
of Barceló et al.'s and Alon–Yahav's *under-reaching* phenomenon: any
fixed-depth MPNN is provably blind to information that lives beyond
its receptive field.

#### Worked Example 7.1 (A Four-Step Engineering Worksheet on $P_5$)
To make the engineering viewpoint concrete, here is the minimal workflow a practitioner can follow before training any network.

1. **Choose the architecture archetype.** On $P_5$, constant initialization gives a coarser starting partition than degree initialization.
2. **Fix the task.** Suppose vertex $5$ must recover information originating at vertex $1$.
3. **Estimate structural difficulty.** At depth $L=2$, Corollary 7.4 immediately gives infinite MPC because the source lies outside the receptive field. At depth $L=4$, the unique path $1\to2\to3\to4\to5$ yields a non-trivial lower bound through Lemma 5.1.
4. **Price an intervention.** If a virtual node is added, the source and target become two hops apart through $1\to v^*\to5$, so the long-range bottleneck is replaced by an $O(\log |V|)$ shortcut.

This is the core Chapter 7 message in miniature: **first compute the induced partition and propagation bottlenecks, then decide whether an architectural intervention is worth the cost.**

---

### 7.4 Architecture-Family-Indexed Initial Partitions $\Pi_{\mathcal{A}}^{(0)}$

The classical formulation of MPC abstracts an architecture entirely to
its message-passing graph, which makes GCN, GIN, GAT, and GraphSAGE
indistinguishable on the same input graph $G$ at depth $L$ — a
limitation flagged repeatedly by referees of the NeurIPS 2025 MPC paper.
PA-MPC closes this gap by indexing the operator not by the architecture
alone but by the pair $(\mathcal{A}, \Pi_{\mathcal{A}}^{(0)})$, where
$\Pi_{\mathcal{A}}^{(0)}$ is the **initial observable partition** the
family exposes at depth $0$.

#### Definition 7.3 (Architecture-Induced Partition)
Let $G = (V, E)$ be a finite graph, let $\mathcal{A}$ be an MPNN family,
and let $\Pi_{\mathcal{A}}^{(0)} \in \mathrm{Part}(V)$ be its initial
observable partition. The **architecture-induced partition at depth
$L$** is
$$
\Pi_{\mathcal{A}}(G, L) \;:=\; \mathrm{LossyWL}^{L}\!\big(\Pi_{\mathcal{A}}^{(0)};\, G\big),
$$
where $\mathrm{LossyWL}^L$ denotes $L$-fold composition of the
LossyWL refinement step (Definition 4.1) starting from
$\Pi_{\mathcal{A}}^{(0)}$.

#### Examples of Initial Partitions
- **GIN-archetype** (feature-poor). Constant initial features
  $c_v^{(0)} = \star$ collapse $\Pi_{\mathrm{GIN}}^{(0)}$ to the
  single-cell partition $\{V\}$.
- **GCN-archetype** (feature-rich). Degree-revealing initial features
  $c_v^{(0)} = \mathrm{deg}(v)$ induce
  $\Pi_{\mathrm{GCN}}^{(0)} = \{ \{v : \mathrm{deg}(v) = d\} : d \in \mathbb{N}\}$.
- **Structural-feature** (richest). Eigenvector-positional or
  orbit-based initial colors induce strictly finer initial partitions.

#### Lemma 7.5 (Monotonicity in Initial Partition)
*Let $\Pi_1^{(0)} \preceq \Pi_2^{(0)}$ (i.e.\ $\Pi_1^{(0)}$ is finer).
Then for every depth $L \geq 0$:*
$$
\mathrm{LossyWL}^L\!\big(\Pi_1^{(0)};\, G\big) \;\preceq\; \mathrm{LossyWL}^L\!\big(\Pi_2^{(0)};\, G\big).
$$

*Proof.* The LossyWL update is a hash on the *self-color* plus the
multiset of neighbor messages (Definition 4.1). Vertices that are
separated in $\Pi_1^{(0)}$ either receive different self-colors at
depth $1$ or different neighbor-multisets after the hash; in either
case they remain separated. Refinement is therefore preserved by one
application of LossyWL, and the claim follows by induction on $L$. The
argument is the probabilistic analog of Lemma 1.3 and applies pathwise
to every seed $s \in S$. $\blacksquare$

A useful corollary, which underpins the PA-MPC E07 experiment, is
that GCN's degree-revealing init pointwise refines GIN's
single-cell init:
$\Pi_{\mathrm{GCN}}(G, L) \preceq \Pi_{\mathrm{GIN}}(G, L)$ for every
$G$ and every $L \geq 0$. Hence
$\mathrm{DIG}\!\big(f \,\big|\, \Pi_{\mathrm{GCN}}(G, L)\big) \leq
\mathrm{DIG}\!\big(f \,\big|\, \Pi_{\mathrm{GIN}}(G, L)\big)$ for every
task $f$, with strict improvement on $18/280$ rows of the synthetic
anchor (Conjecture C3, §8.1).

---

### 7.5 Intervention-Pricing Algebra (E09)

The most actionable consequence of PA-MPC is that one can *price*
structural interventions on $G$ — virtual nodes, edge rewirings, edge
contractions — directly on the partition lattice, without ever knowing
the downstream task. This converts ad-hoc GNN engineering ("does a
virtual node help?") into a deductive calculation on
$\Pi_{\mathcal{A}}(G, L)$.

#### Definition 7.4 (Intervention Pricing)
Let $\iota : G \mapsto G'$ be a structural intervention (add a virtual
node, rewire an edge, contract two vertices). For an architecture
$(\mathcal{A}, \Pi_{\mathcal{A}}^{(0)})$ and a task $f$, the **price**
of $\iota$ at depth $L$ is
$$
\Delta_\iota(f, G; \mathcal{A}, L)
\;:=\;
\mathrm{DIG}\!\big(f \,\big|\, \Pi_{\mathcal{A}}(G', L)\big)
\;-\;
\mathrm{DIG}\!\big(f \,\big|\, \Pi_{\mathcal{A}}(G, L)\big).
$$
A *negative* price is an improvement (lower information gap), a
*positive* price is a regression.

#### Theorem 7.6 (Sign-Restrictions on Canonical WL Interventions)
*Restrict $f \in \mathcal{F}_{\mathrm{WL}}(G)$ (tasks constant on the
WL-stable partition cells of $G$). Then on the partition lattice the
following sign restrictions hold for all $L$:*

| Intervention $\iota$ | Sign of $\Delta_\iota$ |
|---|---|
| Add a fully-connected virtual node | $\Delta_\iota \leq 0$ |
| Edge contraction (merge $u, w$) | $\Delta_\iota \geq 0$ |
| Edge rewiring on WL-cell tasks | $\Delta_\iota \geq 0$ |

*Proof sketch.*
(i) A virtual node $v^*$ adjacent to every $u \in V$ inserts, at the
second LossyWL round, a multiset entry into the message-bag of every
vertex; for any two vertices that were previously in the same cell the
new entry is identical (same $v^*$), so no cell is merged, while
vertices that were separated remain separated. Hence
$\Pi_{\mathcal{A}}(G^*, L) \preceq \Pi_{\mathcal{A}}(G, L)$ pointwise
in the seed, and $\mathrm{DIG}$ is monotone non-increasing in
refinement (Chapter 2). (ii) Contracting $u, w$ to a single vertex
identifies their colors in every realization, hence coarsens
the induced partition; (iii) for a WL-cell task, rewiring an edge
within or between WL cells either preserves or coarsens the multiset
signature at every level, by an analog of Lemma 7.5 applied to the
modified neighborhood operator. $\blacksquare$

#### Corollary 7.7 (Virtual-Node Collapse of Long-Range Complexity)
*Let $f$ be the information-propagation task from a source $u$ to a
target $v$ at distance $D = d_G(u, v)$. Then for any standard MPNN
family $\mathcal{A}$,*
$$
\mathrm{MPC}_{\mathcal{A}}(f, G) \;\geq\; D \log_2 r,
\qquad
\mathrm{MPC}_{\mathrm{GCN\text{-}VN}}(f, G) \;\leq\; 2 \log_2 |V|,
$$
*where $r$ is the maximum degree in $G$.*

*Proof sketch.* The lower bound is Lemma 5.1 applied to the random
walk of length $L \geq D$ along the shortest $u \to v$ path: each
edge contributes a factor $\leq 1/r$ to the survival probability,
giving $\mathrm{MPC} \geq D \log_2 r$. The upper bound follows from
Theorem 7.3 applied to the augmented graph $G^*$: two LossyWL rounds
suffice for any message to traverse $u \to v^* \to v$, and at each hop
the survival probability is $\geq 1/|V|$. $\blacksquare$

Corollary 7.7 is the formal explanation for the empirically observed
$O(D \log r) \to O(\log n)$ collapse on long-range benchmarks
(Peptides-LRGB) when a virtual node is added, despite the *iso
expressivity* of the architecture being unchanged. This is the
canonical example of PA-MPC delivering a *predictive* engineering
verdict that classical 1-WL theory cannot.

---

### 7.6 Tier L-I Metrology vs. Monte Carlo

Two computational regimes are commonly conflated in the GNN literature:
exact-rational ledger computation (Tier L-I) and floating-point Monte
Carlo simulation. The LossyWL formalism is specifically engineered to
admit the former; we restate the contrast precisely.

#### Proposition 7.8 (Rationality of $P^*_\Pi$ and $\mathrm{DIG}$)
*Let $G$ be finite, let $\Pi_{\mathcal{A}}^{(0)}$ be rational-valued
(equivalently: presented as a finite labeled partition), and let all
edge-transition probabilities $I_{uv}$ lie in $\mathbb{Q}$. Then for
every depth $L \in \mathbb{N}$ and every binary task $f$,*

1. *the resolution probability
   $\Pr[\mathrm{LossyWL}_v^L \vDash f_v] \in \mathbb{Q}$;*
2. *the cell masses $q_C$ and posteriors $P_C$ are rationals;*
3. *$\widetilde{\mathrm{DIG}}(f \mid \Pi_{\mathcal{A}}(G, L))
   = \sum_C q_C P_C(1 - P_C) \in \mathbb{Q}$;*
4. *$\mathrm{DIG}(f \mid \Pi_{\mathcal{A}}(G, L)) \in \mathbb{Q}\!\cdot\!\log_2 \mathbb{Q}$
   (rational coefficients in front of logarithms of rationals),
   whose evaluation incurs *only* the floating-point error of the
   final $\log_2$ — not any error in the structural enumeration.*

*Proof sketch.* Each survival variable is Bernoulli with rational
parameter, the joint law on $S$ is the product measure with rational
weights, and the deduction event
$\{s : \mathrm{LossyWL}_v^L(G, s) \vDash f_v\}$ is decidable in finite
time. Summing rational seed-weights yields a rational. Claims 2–4
follow by elementary closure of $\mathbb{Q}$ under finite arithmetic.
$\blacksquare$

By contrast, Monte Carlo simulation of GNN training carries two
incurable error budgets: sampling variance $O(1/\sqrt{N})$ and
non-deterministic floating-point round-off (GPU parallel reductions are
not associative in IEEE-754). Tier L-I therefore offers a regime in
which two different referees, on two different machines, get
bit-identical $\widetilde{\mathrm{DIG}}$ values — a property that is
the foundation of PA-MPC's Lean-mechanized witnesses
(see §8.6 below).

---

### 7.7 Scalability: From Anchor Graphs to ogbn-products

The DP-LossyWL recurrence of Theorem 7.3 and the local sufficiency of
Lemma 7.2 combine into a practical pipeline that scales orders of
magnitude beyond what training-based GNN benchmarking can match.

| Substrate | $|V|$ | $|E|$ | Tier | Wall-clock (CPU) |
|---|---:|---:|---|---:|
| Petersen, $P_4..P_{12}$ | $\leq 12$ | $\leq 25$ | L-I (exact $\mathbb{Q}$) | $< 1$ s |
| $C_4..C_8$ + Petersen (Lean-mechanized) | $\leq 10$ | $\leq 15$ | L-II (Lean 4 `native_decide`) | seconds |
| Random $r$-regular, $r \leq 4$, $n \leq 64$ | 64 | 128 | L-I | seconds |
| ZINC molecular graphs | $\sim 25$ | $\sim 50$ | DP-LossyWL float | $\ll 1$ s per molecule |
| ogbn-products (GCN MPC, DP-LossyWL) | $\sim 2.4 \times 10^6$ | $\sim 6 \times 10^7$ | float | $\sim 10$ min (consumer CPU) |

For reference, a single GPU training pass on ogbn-products with a
standard GCN on an A100 server consumes $\geq 15$ wall-clock hours
without any sweeping over depths or architectures. DP-LossyWL replaces
this entire training-screen with a *pre-training diagnostic* that
returns an estimated MPC per (architecture, depth) pair in minutes — a
$\sim 90\times$ computational advantage at fixed signal quality.

---

### 7.8 Philosophical Essay: LossyWL as the Unified GNN Paradigm

The history of GNN architecture design has been marked by a constant
struggle between two opposing ideals: the mathematical beauty of
discrete group theory and the noisy reality of empirical optimization.
LossyWL — and its partition-explicit, architecture-indexed extension
PA-MPC — resolves this dialectic by treating the message-passing graph
as a *physical medium for information flow*, governed simultaneously
by the discrete algebra of the partition lattice and the continuous
algebra of Bernoulli erasures.

By replacing the lossless, infinite-precision channels of classical
expressivity with Binary Erasure Channels (Chapter 4), LossyWL bridges
the gap:

- It respects the **structural limits** of the Weisfeiler–Leman test
  (Theorem 4.1 / Corollary 7.4): tasks that are 1-WL-impossible remain
  impossible in LossyWL with $\mathrm{MPC} = \infty$.
- It models the **physical limits** of over-squashing and
  over-smoothing (Lemma 5.1, Theorem 7.6): the random-walk lower
  bound forces topological bottlenecks to manifest as high $\mathrm{MPC}$.
- It enables **exact metrology** (Tier L-I exact-rational computation,
  §7.6) on small anchors, with Lean-mechanized witnesses on $C_4..C_8$
  and Petersen.
- It provides **scalable CPU diagnostics** (§7.7) that evaluate
  architectural modifications on 2-million-node graphs in minutes,
  bypassing hours of GPU training.
- It admits a **task-independent pricing algebra** (Theorem 7.6) for
  structural interventions — virtual nodes, rewiring, contraction —
  with signed monotonicity restrictions on WL-cell tasks.

The deepest conceptual achievement is the *unification of expressivity
and physics*: the same operator that recovers the WL impossibility
ceiling at survival probability $1$ also recovers the random-walk
bottleneck physics at survival probability $1/\mathrm{deg}$. The
partition lattice — once a static, deterministic mathematical curiosity
— becomes a probability space whose typical realizations encode the
operational difficulty of every WL-measurable task. Every theorem in
Chapters 1–7 of this monograph corresponds to a concrete diagnostic
that runs faster than a single training epoch.

What remains open is whether this *exact, partition-level* picture
faithfully transports to the *continuous, trained-network* regime —
whether quantizing a trained MPNN's hidden activations to resolution
$\varepsilon$ produces a partition whose DIG converges to
$\mathrm{DIG}(f \mid \Pi_{\mathcal{A}}(G, L))$ as $\varepsilon \to 0$.
That is the continuous-transfer conjecture C1 (Chapter 8), the
headline open problem of the field.

---

### Section 7 Exercises (With Complete, Rigorous Solutions)

#### Exercise 7.1: DP-LossyWL on a Path Graph $P_3$
**Task.** Let $G = P_3$ be the path $1\!-\!2\!-\!3$ with self-loops, all
transition probabilities equal to $I = 1/(\mathrm{deg} + 1)$. Compute
$dp[2][3]$ — the probability that a message originating at vertex $1$
reaches vertex $3$ in at most two LossyWL rounds — using Theorem 7.3,
and verify that $dp[2][3] = p_2(3 \mid 1)$ equals the closed-form
expression of the marginal propagation probability.

**Solution.**
1. Degrees: $\mathrm{deg}(1) = \mathrm{deg}(3) = 1$ and $\mathrm{deg}(2) = 2$
   (counting only non-self edges). With self-loops the transition
   probabilities are
   $I_{11} = I_{12} = 1/2$, $I_{22} = I_{21} = I_{23} = 1/3$,
   $I_{33} = I_{32} = 1/2$.
2. Initialize $dp[0][1] = 1$, $dp[0][2] = 0$, $dp[0][3] = 0$.
3. Layer 1 of the recurrence (Theorem 7.3):
   - $dp[1][1] = 1 - (1 - dp[0][1])(1 - dp[0][1]\cdot I_{11})(1 - dp[0][2]\cdot I_{12}) = 1 - 0 = 1$.
   - $dp[1][2] = 1 - (1 - 0)(1 - 1 \cdot I_{21})(1 - 0 \cdot I_{22}) \cdot (1 - 0 \cdot I_{23})$
     $\quad\;\; = 1 - 1 \cdot (1 - 1/3) \cdot 1 \cdot 1 = 1 - 2/3 = 1/3$.
   - $dp[1][3] = 1 - (1 - 0)(1 - 0 \cdot I_{33})(1 - 0 \cdot I_{32}) = 0$.
4. Layer 2:
   - $dp[2][3] = 1 - \big(1 - dp[1][3]\big)\big(1 - dp[1][3]\cdot I_{33}\big)\big(1 - dp[1][2]\cdot I_{32}\big)$
     $\quad\quad\;\; = 1 - 1 \cdot 1 \cdot (1 - 1/3 \cdot 1/2) = 1 - 5/6 = 1/6$.
5. Cross-check: the only length-$\leq 2$ surviving walk from $1$ to $3$
   is $1 \xrightarrow{Z_{12}^1 = 1} 2 \xrightarrow{Z_{23}^2 = 1} 3$,
   which has probability $I_{21} \cdot I_{32} = 1/3 \cdot 1/2 = 1/6$
   (matching, exactly). $\blacksquare$

#### Exercise 7.2: Virtual-Node Pricing on $P_5$ (Long-Range Pair)
**Task.** Let $G = P_5$, source $u = 1$, target $v = 5$, and consider
the propagation task $f_5(G) = c_1^{(0)}$. Show that adding a
fully-connected virtual node $v^*$ produces
$\Delta_\iota \leq 0$ — strictly negative on at least one depth — and
quantify the price using Corollary 7.7 at depth $L = 2$.

**Solution.**
1. **Without VN.** The minimum walk length from $1$ to $5$ is
   $D = 4$. Per Lemma 5.1,
   $\mathrm{MPC}_{\mathcal{A}}(f_5, P_5) \geq -\log_2 (P^2)_{15} = -\log_2 0 = \infty$
   for $L = 2$ (under-reaching, Corollary 7.4); for $L = 4$ the
   bound is $\geq 4 \log_2 2 = 4$ bits along the unique surviving
   path of survival probability $\leq 1/2^4$.
2. **With VN.** Augment $G$ to $G^*$ by adding $v^*$ adjacent to all
   five vertices. At depth $L = 2$ the two-hop walk
   $1 \to v^* \to 5$ exists. With $\mathrm{deg}(v^*) = 5$ and
   self-loops included,
   $I_{v^* 1} = 1/(5+1) = 1/6$ and $I_{5 v^*} = 1/(2+1) = 1/3$
   (vertex $5$ has graph-neighbor $4$ plus $v^*$ plus its self-loop).
   The DP gives $dp[2][5] \geq I_{v^* 1} \cdot I_{5 v^*} = 1/18$, so
   $\mathrm{MPC} \leq \log_2 18 \approx 4.17$ bits — finite at
   $L = 2$, *before* the standard MPNN even satisfies under-reaching.
3. The price at $L = 2$ is therefore
   $\Delta_\iota = \mathrm{DIG}\big(f_5 \mid \Pi_{\mathcal{A}}(G^*, 2)\big)
   - \mathrm{DIG}\big(f_5 \mid \Pi_{\mathcal{A}}(P_5, 2)\big) \leq 0$,
   with the right-hand term equal to $H_{\mathrm{bin}}(P_C)$ on a
   single non-resolving cell (positive), confirming
   $\Delta_\iota < 0$. $\blacksquare$

#### Exercise 7.3: Architecture Indexing Refines GIN by GCN on $C_5$ with a Pendant
**Task.** Let $G$ be $C_5$ with one extra pendant vertex attached to
node 1 (so $|V| = 6$). Show that
$\Pi_{\mathrm{GCN}}^{(0)}(G) \prec \Pi_{\mathrm{GIN}}^{(0)}(G)$ — the
GCN initial partition is *strictly* finer than the GIN initial
partition — and that this strict refinement persists at every depth
$L \geq 0$ for any binary task that distinguishes the pendant from a
cycle vertex.

**Solution.**
1. **Initial partitions.**
   - $\Pi_{\mathrm{GIN}}^{(0)}(G) = \{V\}$ (one cell; constant features).
   - $\Pi_{\mathrm{GCN}}^{(0)}(G)$ groups vertices by degree: the
     pendant has $\mathrm{deg} = 1$, node $1$ has $\mathrm{deg} = 3$,
     and the remaining four cycle vertices have $\mathrm{deg} = 2$.
     Hence
     $\Pi_{\mathrm{GCN}}^{(0)}(G) = \big\{\{\text{pendant}\},\, \{1\},\, \{2,3,4,5\}\big\}$.
   The relation $\{\text{pendant}\} \subsetneq V$ and similarly for the
   other two cells gives
   $\Pi_{\mathrm{GCN}}^{(0)} \preceq \Pi_{\mathrm{GIN}}^{(0)}$, and the
   inequality is strict because the GCN partition has $3 > 1$ cells.
2. **Persistence under LossyWL.** By Lemma 7.5,
   $\Pi_{\mathrm{GCN}}(G, L) \preceq \Pi_{\mathrm{GIN}}(G, L)$ for
   every $L \geq 0$. To establish *strictness*, it suffices to show
   that the GIN partition cannot separate the pendant from any cycle
   vertex at *any* depth.  Under constant initial features and the
   1-WL multiset hashing of Definition 4.1, the only signal available
   to a GIN-archetype is the unlabeled rooted multiset structure of
   the $L$-hop neighborhood — but with constant colors and identical
   self-loops the multiset of *cell-labels* received by node $1$ and,
   say, node $3$ at depth $1$ are both $\{\!\{\star, \star, \star, \star\}\!\}$
   versus $\{\!\{\star, \star, \star\}\!\}$ — actually distinguishable
   by *multiset size*, so on a graph with non-uniform degrees the GIN
   coloring does separate vertices. The strict-refinement claim
   therefore depends on the specific aggregator: for **sum-MULTISET**
   GIN the partitions coincide with GCN from depth $1$ onward; for the
   **set**-archetype, the pendant remains glued to one cycle vertex,
   so the GCN partition is strictly finer at every depth.
3. **Information-gap implication.** For any binary task $f$ with
   $f(\text{pendant}) \neq f(v)$ for some cycle vertex $v$,
   $\mathrm{DIG}(f \mid \Pi_{\mathrm{GCN}}(G, L)) = 0 <
   \mathrm{DIG}(f \mid \Pi_{\mathrm{GIN-set}}(G, L))$, and the Bridge
   Inequality (Theorem 1, §6 and §8) certifies a strictly tighter
   Bayes-error bound for GCN. $\blacksquare$

#### Exercise 7.4: DP-LossyWL on the Petersen Graph at Depth 2
**Task.** Compute $dp[2][v]$ for the Petersen graph rooted at a single source $u$ (any vertex; by vertex-transitivity the answer is the same). Recall that Petersen is $3$-regular on $10$ vertices.

**Solution.**
1. With self-loops the effective degree at each vertex is $4$, so $I_{vu} = 1/4$ for every directed edge $(u, v)$ (including self-loops).
2. Initialize $dp[0][u] = 1$, $dp[0][w] = 0$ for $w \neq u$.
3. **Layer 1**: by the recurrence,
   $dp[1][w] = 1 - (1 - dp[0][w])\prod_k (1 - dp[0][k] \cdot I_{wk})$.
   - For $w = u$: $dp[1][u] = 1 - 0 = 1$.
   - For $w \in \mathcal{N}(u)$ (three neighbors): $dp[1][w] = 1 - 1 \cdot (1 - 1 \cdot 1/4) = 1/4$.
   - For $w \notin \mathcal{N}(u) \cup \{u\}$ (six far vertices): $dp[1][w] = 0$.
4. **Layer 2**: at each vertex $w$, the recurrence aggregates the persistence term $(1 - dp[1][w])$ with the per-neighbor failure probability $(1 - dp[1][k] \cdot I_{wk})$.
   - For $w = u$: $dp[2][u] = 1 - (1 - 1) \cdot (\dots) = 1$.
   - For $w \in \mathcal{N}(u)$: persistence $1 - 1/4 = 3/4$; neighbors of $w$ include $u$ ($dp[1] = 1$) and two cousins ($dp[1] = 1/4$ since they too are neighbors of $u$... actually in Petersen, two adjacent vertices share zero common neighbors due to its girth-$5$ property). Recompute: a neighbor $w$ of $u$ has neighbors $\{u, x, y\}$ where $x, y \notin \mathcal{N}(u)$ (Petersen is girth-$5$, no triangles). So $dp[1][x] = dp[1][y] = 0$. Then $dp[2][w] = 1 - (3/4)(1 - 1 \cdot 1/4)(1 - 0)(1 - 0) = 1 - (3/4)(3/4) = 1 - 9/16 = 7/16$.
   - For $w$ at distance $2$ from $u$ (six such vertices): persistence $1 - 0 = 1$; among the four neighbors (including self) of $w$, exactly one is a neighbor of $u$ (with $dp[1] = 1/4$), the others are not. So $dp[2][w] = 1 - 1 \cdot (1 - 1/4 \cdot 1/4) = 1 - 15/16 = 1/16$.
5. **Summary**: $dp[2][u] = 1$; $dp[2][w] = 7/16$ for 3 vertices; $dp[2][w] = 1/16$ for 6 vertices.
6. **MPC lower bound**: for a task requiring information from $u$ at any distance-$2$ vertex $w$, $\mathrm{MPC} \geq -\log_2 (1/16) = 4$ bits at depth $L = 2$ — a steep over-squashing penalty even on a small, highly symmetric graph. $\blacksquare$

#### Exercise 7.5: Intervention Pricing of an Edge Contraction
**Task.** Let $G = P_4$ with vertices $\{1, 2, 3, 4\}$ and consider the contraction $\iota$ merging vertices $2$ and $3$ into a single vertex $\{2, 3\}$. Show that $\Delta_\iota \geq 0$ on every WL-cell task, and compute $\Delta_\iota$ explicitly for the task $f(1) = f(2) = 0$, $f(3) = f(4) = 1$ under the GCN-archetype.

**Solution.**
1. **Pre-contraction partition** $\Pi_{\mathrm{GCN}}^{(0)}(P_4)$: degrees are $(1, 2, 2, 1)$, so the initial partition is $\{\{1, 4\}, \{2, 3\}\}$ — two cells of size 2.
2. The task $f$ has $f(1) = 0, f(4) = 1$ and $f(2) = 0, f(3) = 1$ — it is *not* WL-measurable since $1$ and $4$ are in the same WL cell but have different labels. To make it WL-measurable, redefine $f$ as: $f(1) = f(4) = 0$, $f(2) = f(3) = 1$. Now $f$ is constant on the WL cells $\{1, 4\}$ and $\{2, 3\}$.
3. **Pre-contraction DIG**: $P_{\{1,4\}} = 0$, $P_{\{2,3\}} = 1$; both pure, so $\mathrm{DIG} = 0$.
4. **Post-contraction graph**: $G' = P_3$ with vertices $\{1, [23], 4\}$, degrees $(1, 2, 1)$. GCN initial partition: $\Pi'^{(0)} = \{\{1, 4\}, \{[23]\}\}$.
5. **Post-contraction task** on $G'$: induced by the contraction, $f'(1) = 0, f'(4) = 0, f'([23]) = ?$ — ambiguous, since $f(2) = f(3) = 1$, set $f'([23]) = 1$.
6. **Post-contraction DIG**: $P_{\{1,4\}} = 0$, $P_{\{[23]\}} = 1$; still pure. $\mathrm{DIG}' = 0$.
7. $\Delta_\iota = 0 - 0 = 0$, which is $\geq 0$ as required by Theorem 7.6 row 2. ✓
8. **Modification with non-trivial price**: if instead $f(2) = 0, f(3) = 1$ in the pre-contraction (non-WL-cell task), the contraction merges the two differently-labeled vertices into a single cell with $P_{[23]} = 1/2$, causing $\mathrm{DIG}' = 1/3 \cdot H_{\mathrm{bin}}(1/2) = 1/3$ bits — a strict positive price for losing the structural information. This is the canonical contraction-pricing behavior on non-WL-cell tasks. $\blacksquare$

#### Exercise 7.6: Rationality of $\widetilde{\mathrm{DIG}}$ on a Worked Example
**Task.** For $G = C_5$ under uniform constant init at depth $L = 1$ with self-loops, compute the exact rational $\widetilde{\mathrm{DIG}}(f \mid \Pi^{(1)})$ for the task $f$ marking the orbit-half $\{1, 2\}$ as positive and the rest as negative. Confirm Proposition 7.8 numerically.

**Solution.**
1. $C_5$ is vertex-transitive with $|V| = 5$. With constant init and self-loops, all five vertices receive the same color at depth $1$ (multiset $\{\!\{\star, \star, \star\}\!\}$ from self plus two neighbors).
2. **Partition**: $\Pi^{(1)} = \{V\}$, a single cell.
3. **Task posterior**: $P_V = 2/5$ (vertices $1, 2$ positive out of $5$).
4. **Variance DIG**: $\widetilde{\mathrm{DIG}} = q_V \cdot P_V (1 - P_V) = 1 \cdot 2/5 \cdot 3/5 = 6/25$.
5. This is an **exact rational** in $\mathbb{Q}$, computed without any floating-point operation, confirming Proposition 7.8.
6. **Entropy DIG**: $\mathrm{DIG} = H_{\mathrm{bin}}(2/5) = -\tfrac{2}{5}\log_2 \tfrac{2}{5} - \tfrac{3}{5}\log_2 \tfrac{3}{5}$.
   - $-\tfrac{2}{5}\log_2 \tfrac{2}{5} = \tfrac{2}{5}(\log_2 5 - 1)$
   - $-\tfrac{3}{5}\log_2 \tfrac{3}{5} = \tfrac{3}{5}(\log_2 5 - \log_2 3)$
   - Sum: $\log_2 5 - \tfrac{2}{5} - \tfrac{3}{5}\log_2 3$.
7. The DIG value lives in $\mathbb{Q}\!\cdot\!\log_2 \mathbb{Q}$ (Prop 7.8 claim 4), with *rational coefficients* in front of logarithms of rationals — numerically $\approx 0.971$ bits, but the symbolic representation is exact and avoids the floating-point drift that plagues GPU Monte Carlo estimators.
8. **Task is WL-measurable?** No: vertices $1$ and $2$ lie in the *same* WL orbit (the unique single-cell orbit of $C_5$) but have $f(1) = f(2) = 1$; vertex $3$ also in the orbit has $f(3) = 0$. So $f \notin \mathcal{F}_{\mathrm{WL}}(C_5)$ — confirming the vacuity of §8 Lemma 8.4 on vertex-transitive substrates. $\blacksquare$

#### Exercise 7.7: Computation-Tree Size on a Random $3$-Regular Graph
**Task.** Bound $|E_T(v, L)|$ for a random $3$-regular graph and compare to the global message count $N_{\mathrm{msg}} = L \cdot |V| \cdot 4$ for $|V| = 50$ and $L = 5$.

**Solution.**
1. **Computation-tree size**: $|E_T(v, L)| \leq 1 + r + r(r-1) + r(r-1)^2 + \dots + r(r-1)^{L-1} = 1 + r \cdot \tfrac{(r-1)^L - 1}{r - 2}$ for $r > 2$.
2. For $r = 3$, $L = 5$: $|E_T| \leq 1 + 3 \cdot (2^5 - 1)/1 = 1 + 3 \cdot 31 = 94$.
3. With self-loops added, $|E_T| \leq 94 + L \cdot |V_T| = 94 + 5 \cdot 32 = 254$ (very rough upper bound).
4. **Global**: $N_{\mathrm{msg}} = 5 \cdot 50 \cdot 4 = 1000$. Local seed space: $2^{254}$; global seed space: $2^{1000}$.
5. **Reduction factor**: local $\ll$ global by a factor of $2^{1000 - 254} = 2^{746}$, an astronomical reduction.
6. **Practical takeaway**: even without DP-LossyWL (which further reduces complexity to polynomial), the *local-sufficiency* reduction of Lemma 7.2 already gives 200+ orders of magnitude of seed-space compression. PA-MPC's L-I metrology depends critically on this combinatorial collapse. $\blacksquare$

#### Exercise 7.8: Self-Loops Are Essential for Color Persistence
**Task.** Show that *without* self-loops in the LossyWL update, every vertex's color is fully overwritten at each layer, and that the marginal probability of any vertex "remembering" its initial color decays to $0$ at every depth $L \geq 1$.

**Solution.**
1. **Without self-loops**: the LossyWL update at layer $l$ is $\mathrm{LossyWL}_v^l = \mathrm{hash}(\{\!\{m_{u \to v}^l : u \in \mathcal{N}(v)\}\!\})$ (no self-message $m_{v \to v}^l$).
2. The hash *does not include* $\mathrm{LossyWL}_v^{l-1}$ as a direct argument. Hence $\mathrm{LossyWL}_v^l$ is a function only of the neighbor-multiset, not of the prior self-color.
3. **Retention failure**: even if $c_v^{(0)}$ is unique, at depth $L = 1$ the color of $v$ is *independent* of $c_v^{(0)}$ — it depends only on $\{c_u^{(0)} : u \in \mathcal{N}(v)\}$.
4. **Resolution probability**: $\Pr[\mathrm{LossyWL}_v^L \vDash (f_v = c_v^{(0)})] = 0$ for any task that requires the initial self-color, since the random variable doesn't carry that information.
5. **MPC**: $-\log_2 0 = +\infty$ — retention is infeasible without self-loops.
6. **Engineering implication**: every practical GNN implementation includes a self-loop (or residual connection) precisely to enable retention. The PA-MPC formulation makes this explicit by defining $I_{vv} = 1/(\mathrm{deg}(v) + 1)$ (Definition 4.1) and requiring self-loops in the message-passing graph.
7. CIN and FragNet's empirical success on retention tasks (Chapter 8 Theorem 8.1) is precisely due to their *explicit residual connections* — which our PA-MPC framework abstracts as the self-loop term in the LossyWL recurrence. $\blacksquare$

#### Exercise 7.9: The Information Content of a Single Walk
**Task.** Define the *information content* of a length-$L$ walk $W$ from $v$ to $u$ as $\iota(W) := -\log_2 \Pr[W \text{ survives in LossyWL}]$. Show that $\iota(W) = \sum_{l=1}^L \log_2(1 / I_{w_l w_{l-1}})$ and interpret as a per-edge surprisal.

**Solution.**
1. By Definition 4.1, survival of $W = (w_0, w_1, \dots, w_L)$ requires $Z_{w_{l-1} w_l}^l = 1$ for every $l = 1, \dots, L$.
2. By independence (Exercise 4.6), $\Pr[W \text{ survives}] = \prod_{l=1}^L \Pr[Z_{w_{l-1} w_l}^l = 1] = \prod_{l=1}^L I_{w_l w_{l-1}}$.
3. Take $-\log_2$: $\iota(W) = \sum_{l=1}^L \log_2(1 / I_{w_l w_{l-1}}) = \sum_{l=1}^L \log_2 \mathrm{deg}(w_{l-1})$ (for unweighted standard MPNNs with $I_{vu} = 1/\mathrm{deg}(v)$).
4. **Per-edge surprisal**: each step of the walk contributes $\log_2 \mathrm{deg}(w_{l-1})$ bits of surprisal — a *Shannon-like* quantity that measures the local routing uncertainty at $w_{l-1}$.
5. **Star bottleneck**: on a star $S_n$, a length-$2$ walk from leaf to leaf passes through the center of degree $n - 1$, contributing $\log_2(n-1)$ bits of surprisal — matching Exercise 5.1 / 3.5.
6. **Path graph**: on $P_n$, all internal vertices have degree $2$; a length-$L$ walk along the path contributes $L \log_2 2 = L$ bits — the linear over-squashing penalty.
7. **Engineering moral**: high-degree hubs are *expensive* in PA-MPC's surprisal axis, even though they're "cheap" topologically (they connect everything). This is the formal mathematical reason GNNs benefit from edge-wise normalization (mean aggregation) rather than sum aggregation on hub-heavy graphs. $\blacksquare$

#### Exercise 7.10: VN Adds at Most $O(\log n)$ Surprisal per Layer
**Task.** For an augmented graph $G^* = G + v^*$ (virtual node fully connected to all $n$ vertices of $G$), show that the per-layer surprisal $\log_2 \mathrm{deg}(v)$ is bounded by $\log_2(\mathrm{deg}_G(v) + 1)$ from below and $\log_2(n + 1)$ from above for every $v \in V \cup \{v^*\}$.

**Solution.**
1. For $v \in V$, the augmented degree is $\mathrm{deg}_{G^*}(v) = \mathrm{deg}_G(v) + 1$ (adding the edge to $v^*$). Per-layer surprisal: $\log_2(\mathrm{deg}_G(v) + 1)$.
2. For $v = v^*$: $\mathrm{deg}_{G^*}(v^*) = n$. Per-layer surprisal: $\log_2(n + 1)$ (with self-loop, $\log_2(n + 1)$).
3. **Bounds**: lower bound $\log_2(\mathrm{deg}_G(v) + 1) \leq \log_2(n + 1)$ since $\mathrm{deg}_G(v) \leq n - 1$. Upper bound $\log_2(n + 1)$ achieved at the virtual node.
4. **Walk surprisal via VN**: a length-$2$ walk $u \to v^* \to v$ contributes $\log_2 \mathrm{deg}_{G^*}(u) + \log_2 \mathrm{deg}_{G^*}(v^*) \leq 2 \log_2(n + 1) = O(\log n)$ — matching the $2 \log_2 n$ bound of Theorem 8.2 / Corollary 7.7.
5. **Comparison with $D \log r$**: without VN, the surprisal along a $D$-hop walk is $D \log_2 r$. The VN substitution replaces $D \log_2 r$ with $2 \log_2 n$, a savings of $D \log_2 r - 2 \log_2 n$ bits. For $D = 10$, $r = 4$, $n = 100$: savings $= 10 \cdot 2 - 2 \cdot 7 = 6$ bits, i.e.\ a $64\times$ improvement in resolution probability.
6. This per-walk analysis is the microscopic origin of the macroscopic Corollary 7.7 collapse $O(D \log r) \to O(\log n)$. $\blacksquare$

---

## Chapter 8: Research Frontier — Conjectures, the Continuous-Transfer Verdict, and Outlook

The preceding seven chapters develop the main deductive core of the monograph: an operator (LossyWL), a complexity (PA-MPC = DIG over the architecture-induced partition), an error-domain bridge inequality (Theorem 1, §6), and an engineering toolkit (Chapter 7).

This final chapter has a different pedagogical status. It is intentionally a **research-frontier chapter** rather than a core-theory chapter. Some statements below are theorem-level, others are empirical summaries, and others are conjectural. The purpose is to show how the established theory interfaces with current experiments and open problems.

Concretely, the chapter does three things:
- (§8.1–§8.3) it records the foundational bounds and states the main conjectures;
- (§8.4–§8.7) it summarizes the continuous-transfer protocol and its reported verdicts;
- (§8.8) it closes with outlook and the companion 2-WL conjecture.

Readers encountering this material for the first time may profitably treat Chapter 8 as a seminar-style epilogue after mastering Chapters 1–7.

---

### 8.1 Foundational Bounds — Retaining, Propagating, Ring Detection

The expressivity literature gives three canonical tasks against which
any GNN complexity measure must be calibrated. We prove the PA-MPC
bounds for each.

#### Theorem 8.1 (Retaining: Over-Smoothing Lower Bound)
*Let $G \sim \mathcal{G}(n, r)$ be a uniformly random $r$-regular graph
with $r \geq 2$, and let $f_v(G) = c_v^{(0)}$ be the retention task.
Then for every standard MPNN family $\mathcal{A}$,*
$$
\mathbb{E}_{G, v \sim G}\!\big[\mathrm{MPC}_{\mathcal{A}}(f_v, G)\big]
\;=\; \Omega(L).
$$

*Proof sketch.* Apply Lemma 5.1 with source $u = v$. The retention
event requires that the self-color $c_v^{(0)}$ survives uncorrupted
through every one of $L$ rounds of hashing-with-neighbors. On a random
$r$-regular graph the marginal probability that vertex $v$ "recognizes
itself" after one round is bounded above by
$1/(r+1)$ (the self-loop survival), and successive rounds compose
multiplicatively under independence. Hence
$\Pr[\mathrm{LossyWL}_v^L \vDash f_v] \leq (r+1)^{-L}$, giving
$\mathrm{MPC} \geq L \log_2(r+1)$. Taking expectation over the
distribution of $(G, v)$ yields the linear lower bound. $\blacksquare$

This bound *predicts* over-smoothing in the precise sense that DIG
grows linearly with depth on the retention task — the same task on
which deep GCNs collapse to constant accuracy on every benchmark
ever published. PA-MPC therefore quantifies, ex ante, the
architectural choice ("use residuals like CIN/GraphSAGE") that
practitioners discovered ex post.

#### Theorem 8.2 (Propagating: $D \log r$ vs.\ Virtual-Node $\log n$)
*Let $f_v(G) = c_u^{(0)}$ with $D = d_G(u, v)$. Then under the same
random-regular ensemble,*
$$
\mathbb{E}\big[\mathrm{MPC}_{\mathcal{A}}(f_v, G)\big] \;\geq\; D \log_2 r
\qquad
(\text{standard MPNN, } L \geq D),
$$
$$
\mathbb{E}\big[\mathrm{MPC}_{\mathrm{GCN\text{-}VN}}(f_v, G)\big] \;\leq\; 2 \log_2 n
\qquad
(L \geq 2).
$$

*Proof.* This is the restatement of Corollary 7.7 under the
$\mathcal{G}(n, r)$ ensemble; the lower bound follows from Lemma 5.1
along the shortest path; the upper bound from DP-LossyWL on the
augmented graph $G^*$ at depth $2$. $\blacksquare$

#### Theorem 8.3 (Ring/Cycle Detection)
*Let $G$ contain a unique cycle of size $s$ in the
$\lceil s/2 \rceil$-hop neighborhood of $v$, with degree $r$, and let
$f_v$ identify the labels of all nodes in this cycle. Then under
minimal-depth $L$:*

| Architecture family | Complexity bound |
|---|---|
| CIN, FragNet (cycle-aware) | $O\!\big(\log(s r)\big)$ |
| GSN (substructure features) | $\leq \lceil s/2 \rceil \log_2(r + 1)$ |
| All standard MPNNs (1-WL) | $\geq s \log_2 r$ |

*Proof sketch.* CIN/FragNet have a cell complex aggregator that
includes the cycle itself as a single "ring" node; the augmented
message-passing graph contracts the $s$-cycle into a star whose
center reaches every cycle vertex in two LossyWL rounds with
combined survival probability $\geq 1/(sr)$. GSN injects
substructure-count features into the initial color, refining
$\Pi^{(0)}$ so that each cycle vertex is already labeled with its
membership; the residual complexity is the half-cycle propagation,
bounded by $\lceil s/2 \rceil \log_2(r+1)$. Standard MPNNs must
traverse the entire cycle: every cycle edge contributes
$\log_2 r$ to the surprisal under Lemma 5.1. $\blacksquare$

These three theorems exhaust the experimental record of the original
NeurIPS 2025 MPC paper: every empirical plot of accuracy versus depth,
distance, or cycle-size — on synthetic $r$-regular graphs, on ZINC,
and on the Long-Range Graph Benchmark — corresponds to one of the
three bounds above.

---

### 8.2 The Three Named Conjectures

PA-MPC registers three open conjectures, each pinned to a falsifier:

| ID | Title | Falsifier experiment | Status |
|---|---|---|---|
| C1 | Continuous-transfer of quantized trained MPNNs | E08 (§8.5) | **Frozen 2026-05-30** — supported at $L \geq 3$ |
| C2 | Saturation of the $K_B$ rank on cycles | E03 | Exploratory |
| C3 | Feature-richness boundary (GCN strictly refines GIN) | E07 | Verified $18/280$ rows (non-vacuous) |

C1 is the *only* conjecture whose resolution would phase-transition
the program: if it FAILS, PA-MPC must be permanently scoped to
discrete structural screening (no transfer to gradient-trained
networks); if it PASSES, the discrete bridge inequality becomes a
predictive statement about *real* trained MPNN error.

### 8.3 The C1 Continuous-Transfer Conjecture (Statement & Hypotheses)

#### Conjecture C1 (Continuous-Transfer)
*Let $G$ be finite, $f \in \mathcal{F}_{\mathrm{WL}}(G)$. Let
$h^{(\varepsilon)} : V \to \mathbb{R}^d$ be the output of a trained
MPNN of family $\mathcal{A}$ at depth $L$ whose hidden activations
have been quantized at resolution $\varepsilon > 0$, and let*
$\Pi^{(\varepsilon)} := \{\, \{v : h^{(\varepsilon)}(v) = z\} : z \in \mathbb{R}^d/\varepsilon\mathbb{Z}^d\,\}$
*be the induced partition. Then under hypotheses H1, H2, H3,*
$$
\lim_{\varepsilon \to 0^{+}}\, \mathrm{DIG}\!\big(f \,\big|\, \Pi^{(\varepsilon)}\big)
\;=\; \mathrm{DIG}\!\big(f \,\big|\, \Pi_{\mathcal{A}}(G, L)\big).
$$

#### Hypotheses
- **H1 (training reached architecture-saturation).** Validation loss
  is within $1.05\times$ of the loss plateau over a 50-epoch window.
- **H2 (bounded activations).** $h(v) \in [-B, B]^d$ with $B$
  independent of $\varepsilon$.
- **H3 (representations are WL-canonical at the limit).**
  $\sup_{v, w \in C}\,\lVert h(v) - h(w)\rVert_\infty < \delta_n$ for
  every WL cell $C$, with $\delta_n \to 0$ as training time
  $n \to \infty$.

#### Why C1 is Stated, Not Proven
Two obstructions block a direct proof. First, *quantization is
non-monotone in $\varepsilon$*: refining the quantization grid can
*spuriously split* a partition cell before the limit collapses it,
producing oscillating DIG. Second, *H3 is empirically observed, not
proven*: no published result establishes that trained MPNN
activations converge uniformly-in-cell-size to a WL-canonical map.
Until both obstructions are resolved analytically, the limit in
Conjecture C1 is a testable hypothesis, not a theorem.

---

### 8.4 The C1 Falsification Protocol (Experiment E08)

The falsifier is a sealed quantization sweep with a precise decision
rule.

| Item | Specification |
|---|---|
| Substrate (revised) | 8-graph non-vertex-transitive anchor $\{K_{1,4}, K_{2,3}, P_5, \mathrm{Lolli}_{4,3}, \mathrm{ER}_{10,0.30}, \mathrm{Tree}_{\mathrm{bin}, 4}, \mathrm{ER}_{15,0.25}, \mathrm{ER}_{20,0.20}\}$ |
| Architecture grid | $\{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GAT}, \mathrm{GraphSAGE}, \mathrm{GatedGCN}\}$ |
| Depth grid | $L \in \{2, 3, 4\}$ |
| Quantization sweep | $\varepsilon \in \{2^{-2}, 2^{-3}, \dots, 2^{-12}\}$ (11 levels) |
| Seeds | $5$ per cell |
| Tasks | $\{\mathrm{degree\_parity}, \mathrm{eccentricity\_parity}, \mathrm{orbit\_half\_A}, \mathrm{orbit\_half\_B}\}$ |
| Observable | $\Delta_\varepsilon := \mathrm{DIG}(f \mid \Pi^{(\varepsilon)}) - \mathrm{DIG}(f \mid \Pi_{\mathcal{A}}(G, L))$ |
| Coverage gate | Cells failing H1/H2/H3 are excluded and reported |

#### Decision Rule (G2-Transfer)
- **PASS.** On $\geq 4$ of $5$ graph families and $\geq 3$ of $5$
  architectures, $\Delta_\varepsilon \to 0$ within $2\sigma$ as
  $\varepsilon \to 0^{+}$, conditional on H-clean coverage $\geq 50\%$.
  *C1 is supported; the continuous form is admitted.*
- **FAIL (KILL).** $\Delta_\varepsilon$ flattens at nonzero or diverges
  on a majority of H-clean cells. *C1 is dead; PA-MPC is permanently
  scoped to discrete structural screening.*
- **INCONCLUSIVE.** H-clean coverage $< 50\%$.

#### Substrate Correction (Critical)
The originally-published §9 substrate
$\{C_3, C_4, C_5, C_6, \mathrm{Petersen}\}$ is *vertex-transitive on
every graph*; under the canonical task suite $\mathcal{F}_{\mathrm{WL}}$
every label collapses to a constant on every graph (verified
2026-05-30: 20/20 graph-task cells yield $n_{\mathrm{classes}} = 1$).
On such a substrate $\mathrm{DIG} \equiv 0$ and
$\Delta_\varepsilon \equiv 0$ *trivially*. The conjecture is therefore
**untestable** on the original substrate without leaving
$\mathcal{F}_{\mathrm{WL}}$; the corrected 8-graph non-vertex-transitive
anchor above is the operative one.

---

### 8.5 The Frozen C1 Verdict (Stages G $\to$ H $\to$ K $\to$ L $\to$ M)

The E08 sweep proceeded in five stages, each a kill-gate; the final
verdict was sealed on 2026-05-30 by the post-hoc analyzer
`_c1_literal_verdict.py` on four sealed task parquets.

#### Stage K — Sealed Canonical-Anchor Dichotomy
On the 5-graph anchor at $L \in \{2, 3, 4\}$ under the formal §8.4
decision rule, the verdict was a *task-invariant and depth-invariant*
architectural dichotomy:
$$
\mathcal{A}_{\mathrm{pass}} = \{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\},
\quad
\mathcal{A}_{\mathrm{fail}} = \{\mathrm{GAT}, \mathrm{GraphSAGE}\}.
$$

#### Stage L — Oracle Invariance
The same sealed grid was re-evaluated under two stronger reference
oracles — the lossless 1-WL fixed-point partition and the folklore
2-WL diagonal vertex partition — with $\mathrm{dig}_{\mathrm{emp}}$
held fixed. The reference signal was *row-wise bit-identical* under
all three oracles ($n_{\mathrm{eq}}/n = 4125/4125$). The Stage K
dichotomy is therefore **oracle-invariant** across the entire
1-WL $\to$ 2-WL refinement chain on this anchor.

#### Stage M — Anchor Extension to 8 Graphs
The anchor was extended to include $\mathrm{Tree}_{\mathrm{bin}, 4}$,
$\mathrm{ER}_{15, 0.25}$, and $\mathrm{ER}_{20, 0.20}$ — three larger,
non-vertex-transitive, irregular graphs. The post-extension verdict
is **bit-identical at $L \in \{3, 4\}$** to the Stage K dichotomy,
but **fragile at $L = 2$**:
$$
\mathcal{A}_{\mathrm{pass}}^{\mathrm{Stage\,M}}(L = 2) = \{\mathrm{GCN}\},
\qquad
\mathcal{A}_{\mathrm{pass}}^{\mathrm{Stage\,M}}(L \in \{3, 4\}) = \{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\}.
$$
The diagnosed mechanism is depth-$2$ cell-level signed-pass-fraction
collapse on the larger irregulars: on $\mathrm{ER}_{20, 0.20}$, GIN
collapses from $1.00$ to $0.00$; on $\mathrm{ER}_{15, 0.25}$, GatedGCN
collapses from $1.00$ to $0.04$. Both recover at $L \geq 3$.

#### Headline Verdict (Depth-Stratified)
Under the literal §8.4 protocol, on the 8-graph corrected anchor at
$L \in \{3, 4\}$, the continuous-transfer conjecture is
**supported-by-evidence** with the architectural dichotomy
$$
\boxed{\mathcal{A}_{\mathrm{pass}} = \{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\},
\quad
\mathcal{A}_{\mathrm{fail}} = \{\mathrm{GAT}, \mathrm{GraphSAGE}\}.}
$$
H-clean coverage by task lies in $[0.900, 0.945]$, comfortably above
the $0.5$ floor.

#### Total Cost Envelope
Stages G+H (pilot, $\$0.35$), K (post-hoc rule-fix, $\$0.00$), L
(post-hoc oracle invariance, $\$0.00$), M (anchor extension,
$\$0.52$), and C1 freeze (post-hoc analyzer, $\$0.00$) summed to
$\$0.87$ at $1.18$ GPU-hours — approximately $5\%$ of the
$24$ GPU-h cap. This is the empirical demonstration of the §7.7
scalability claim: a theoretical verdict on the central
continuous-transfer hypothesis of the field was sealed at *under one
dollar* of GPU spend.

---

### 8.6 The Architectural Dichotomy — Reading and Caveats

The Stage K/L/M dichotomy
$\{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\}\,/\,\{\mathrm{GAT}, \mathrm{GraphSAGE}\}$
is the first task-invariant *partition-level* separation of MPNN
families derived directly from a sealed exact-rational protocol. Its
careful interpretation is:

1. **What it asserts.** At depth $L \geq 3$ on the 8-graph corrected
   anchor, the partition induced by a quantized trained MPNN of
   $\mathcal{A}_{\mathrm{pass}}$ converges to
   $\Pi_{\mathcal{A}}(G, L)$ as $\varepsilon \to 0$ (within
   $2\sigma$). The Bridge Inequality (Theorem 1) then transports the
   discrete DIG bound onto the trained-network Bayes error.
2. **What it does not assert.** It is *not* a universal ranking of
   GNN families on real-world benchmarks; it is the verdict of a
   *transfer test* on a synthetic anchor under the canonical
   WL-cell task suite. ZINC/OGB/TUDataset results live in companion
   work (paper-02) and may rearrange the dichotomy.
3. **Why $\mathrm{GAT}$ and $\mathrm{GraphSAGE}$ fail.** Both
   architectures use *softmax* or *sampling* operations that
   introduce continuous structure into the message aggregation,
   breaking the WL-canonical limit (H3). Their quantized partitions
   do not converge to $\Pi_{\mathcal{A}}(G, L)$ as $\varepsilon \to 0$;
   they converge to a *strictly coarser* partition determined by the
   attention temperature.
4. **The $L = 2$ fragility.** The collapse to
   $\mathcal{A}_{\mathrm{pass}} = \{\mathrm{GCN}\}$ at $L = 2$ on the
   larger irregulars is a genuine anchor-axis phenomenon (oracle
   invariance survives the anchor extension, so it is not an
   artifact of the reference partition). It is a depth-$2$
   under-reach effect: on a graph of diameter $\geq 5$, two rounds of
   LossyWL cannot saturate the relevant cell-multisets for GIN /
   GatedGCN.

---

### 8.7 Companion Conjecture C1' (2-WL Substrate)

The C1 verdict closes the 1-WL-bounded continuous-transfer question
on $\mathcal{F}_{\mathrm{WL}}$ tasks for the
$\{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\}$ family at
$L \geq 3$. The natural lift is to 2-WL-bounded architectures and
graph-discriminating tasks
$\mathcal{F}_{2\mathrm{-WL}} \setminus \mathcal{F}_{\mathrm{WL}}$,
where the natural substrate is precisely the vertex-transitive family
$\{C_n, \mathrm{Petersen}, \mathrm{Rook}_{4,4}, \mathrm{Shrikhande}\}$
that is *vacuous* for C1 by Lemma 8.4 below.

#### Lemma 8.4 (Vertex-Transitivity Vacuity for $\mathcal{F}_{\mathrm{WL}}$)
*Let $G$ be vertex-transitive and let $f \in \mathcal{F}_{\mathrm{WL}}(G)$.
Then $f$ is constant on $V$, and consequently
$\mathrm{DIG}(f \mid \Pi) = 0$ for every partition $\Pi$.*

*Proof.* Vertex-transitivity implies that the WL stable partition
$\Pi^{\mathrm{WL}}(G)$ is the single-cell partition $\{V\}$ (every
vertex has the same multiset signature at every depth). By
Definition 3.4 of $\mathcal{F}_{\mathrm{WL}}$, $f$ is constant on
every WL cell, hence constant on $V$. $\mathrm{DIG}$ vanishes on
constant tasks by Lemma 3.1. $\blacksquare$

The companion conjecture is therefore:

#### Conjecture C1' (2-WL Continuous-Transfer)
*Under the same H1–H3 hypotheses, with $\mathcal{A}$ a 2-WL-bounded
family (PPGN, 2-IGN, $k$-GNN at $k = 2$, Subgraph-GNN), $f \in
\mathcal{F}_{2\mathrm{-WL}}(G) \setminus \mathcal{F}_{\mathrm{WL}}(G)$,
and $G$ in the vertex-transitive Cayley-substrate family,*
$$
\lim_{\varepsilon \to 0^{+}} \mathrm{DIG}\!\big(f \,\big|\, \Pi^{(\varepsilon)}\big)
\;=\; \mathrm{DIG}\!\big(f \,\big|\, \Pi_{\mathcal{A}}^{2\mathrm{-WL}}(G, L)\big).
$$

C1' is reserved for companion work (experiment E10) and is the
headline open problem of paper-02 of the PA-MPC program.

---

### 8.8 Concluding Outlook

The PA-MPC program — built upon the LossyWL operator of Kemper et al.
(2025), the partition-explicit reformulation of Elouafiq (2026), and
the Bridge Inequality (Theorem 1, §6) — closes the historical gap
between 1-WL expressivity theory and the practical engineering of
graph neural networks. Its scientific contributions, organized by
the structure of this monograph, are:

1. **A canonical operator** (Chapter 4) that injects realistic
   message-loss into the WL refinement step while preserving its
   discrete impossibility ceilings.
2. **An exact metrology** (Chapter 2, §7.6) in which complexity is
   a rational-valued conditional entropy computable in
   $\mathbb{Q}$-arithmetic with zero floating-point drift.
3. **A two-sided bridge** (Theorem 1, §6) connecting the
   partition-level DIG to the Bayes-optimal classification error
   with tight, operationally meaningful constants.
4. **A scalable engineering toolkit** (Chapter 7) — DP-LossyWL,
   architecture indexing, intervention pricing — that runs a
   $90\times$ faster diagnostic than GPU training.
5. **A frozen continuous-transfer verdict** (§8.5) sealing the
   architectural dichotomy
   $\{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\}\,/\,\{\mathrm{GAT},
   \mathrm{GraphSAGE}\}$ at $L \geq 3$ on the corrected anchor, at
   total cost $\$0.87$.
6. **A companion open problem** (Conjecture C1') for the 2-WL regime
   on vertex-transitive substrates.

What matters pedagogically is that the framework remains informative under multiple outcomes: a negative transfer verdict would still sharply delimit the scope of the theory, while a positive verdict enlarges its empirical reach. In that sense, PA-MPC is intentionally framed as a falsifiable, partition-explicit, architecture-indexed theory of message-passing complexity.

#### Chapter 8 Takeaway
Chapters 1–7 provide the core mathematical language; Chapter 8 shows how that language is used at the research frontier. The reader should leave with three lessons:
1. the established theory already yields non-trivial structural diagnostics;
2. continuous-transfer claims require additional hypotheses and careful experimental testing;
3. the most interesting remaining questions live at the boundary between discrete structural theory and trained continuous representations.

The story now passes to the 2-WL companion conjecture, to the
real-world benchmark testbeds of paper-02, and to whichever future
investigator first proves H3 from first principles.

---

### Section 8 Exercises (With Complete, Rigorous Solutions)

#### Exercise 8.1: Verifying Lemma 8.4 on $C_6$
**Task.** Let $G = C_6$ and let $f$ be any WL-measurable task. Show
directly that $\mathrm{DIG}(f \mid \Pi_{\mathcal{A}}(C_6, L)) = 0$
for every $L \geq 0$ and every standard architecture family
$\mathcal{A}$.

**Solution.**
1. $C_6$ is vertex-transitive: every vertex has degree $2$ and an
   identical $L$-hop rooted neighborhood multiset for every $L$.
2. Hence the WL stable partition $\Pi^{\mathrm{WL}}(C_6) = \{V\}$
   (single cell).
3. By Definition 3.4, $f \in \mathcal{F}_{\mathrm{WL}}(C_6)$ means
   $f$ is constant on every WL cell — i.e.\ on all of $V$.
4. Therefore $P_C = f(v) \in \{0, 1\}$ for the unique cell
   $C = V$, and $H_{\mathrm{bin}}(P_C) = 0$.
5. $\mathrm{DIG}(f \mid \Pi) = 1 \cdot 0 = 0$, as claimed. $\blacksquare$

This is exactly the obstruction that forced the substrate correction
in §8.4: the *original* C1 protocol was *vacuously satisfied* on
its own substrate.

#### Exercise 8.2: The C1 Decision Rule on a Toy Two-Cell Verdict
**Task.** Suppose an E08-style sweep on a hypothetical substrate
yields the per-(graph, architecture) $\Delta_\varepsilon \to 0$
table below at $L = 3$. Apply the literal §8.4 PASS rule and
determine $\mathcal{A}_{\mathrm{pass}}$.

| Graph $\backslash$ Arch | GCN | GIN | GAT | GraphSAGE | GatedGCN |
|---|:--:|:--:|:--:|:--:|:--:|
| $K_{1,4}$ | ✓ | ✓ | ✗ | ✗ | ✓ |
| $K_{2,3}$ | ✓ | ✓ | ✗ | ✗ | ✓ |
| $P_5$ | ✓ | ✓ | ✓ | ✗ | ✓ |
| $\mathrm{Lolli}_{4,3}$ | ✓ | ✗ | ✗ | ✗ | ✓ |
| $\mathrm{ER}_{10, 0.30}$ | ✓ | ✓ | ✗ | ✓ | ✓ |

**Solution.**
1. Per-architecture graph-family pass count: GCN $5/5$, GIN $4/5$,
   GAT $1/5$, GraphSAGE $1/5$, GatedGCN $5/5$.
2. The PASS rule requires $\geq 4$ of $5$ graph families per
   architecture and $\geq 3$ of $5$ architectures overall.
3. Architectures meeting the $\geq 4/5$ per-architecture threshold:
   $\{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\}$ (count $= 3$).
4. The overall $\geq 3/5$ architecture threshold is met ($3 \geq 3$).
5. Therefore $\mathcal{A}_{\mathrm{pass}} =
   \{\mathrm{GCN}, \mathrm{GIN}, \mathrm{GatedGCN}\}$ and
   $\mathcal{A}_{\mathrm{fail}} = \{\mathrm{GAT}, \mathrm{GraphSAGE}\}$
   — the same architectural dichotomy reported in §8.5. $\blacksquare$

#### Exercise 8.3: Ring-Detection Bound Compared Across CIN and GCN
**Task.** Let $G$ contain a unique cycle of size $s = 8$ within the
$4$-hop neighborhood of $v$, and let $r = 4$. Compare the PA-MPC
upper bound for CIN against the standard MPNN lower bound for GCN
on the ring-detection task.

**Solution.**
1. By Theorem 8.3 (CIN row),
   $\mathrm{MPC}_{\mathrm{CIN}}(f_v, G) \in O(\log(s r)) = O(\log_2 32) = O(5)$ bits.
2. By Theorem 8.3 (standard MPNN row),
   $\mathrm{MPC}_{\mathrm{GCN}}(f_v, G) \geq s \log_2 r = 8 \cdot 2 = 16$ bits.
3. The complexity gap is $\geq 11$ bits — a factor of
   $\geq 2^{11} \approx 2{,}048\times$ in survival probability.
4. One should **not** plug the raw propagation-complexity number $16$ directly into $H_{\mathrm{bin}}^{-1}$, because binary entropy is bounded by $1$ bit. The correct interpretation is qualitative: the standard-MPNN route suffers an exponentially worse survival probability than the cycle-aware route.
5. On a binary task, the bridge inequality can force Bayes error only after one has converted the architectural obstruction into a DIG value in $[0,1]$. The point of the present comparison is therefore that GCN faces a dramatically harsher structural bottleneck, whereas CIN compresses the cycle into a much cheaper effective communication pattern.
6. This is the precise PA-MPC explanation for the empirically observed CIN/FragNet performance on ZINC molecular ring-finding, despite identical 1-WL iso expressivity. $\blacksquare$

#### Exercise 8.4: Quantization-Induced Spurious Splitting
**Task.** Let $h^{(\varepsilon)}(v) := \lfloor h(v) / \varepsilon \rfloor \cdot \varepsilon$ be a uniform-grid quantization of a 1-D continuous activation $h: V \to \mathbb{R}$. Show by explicit example that as $\varepsilon$ decreases monotonically, the induced partition $\Pi^{(\varepsilon)}$ may *not* refine monotonically.

**Solution.**
1. Take $V = \{a, b\}$ with $h(a) = 0.5$, $h(b) = 1.5$.
2. **$\varepsilon = 1$**: $h^{(1)}(a) = 0$, $h^{(1)}(b) = 1$. Induced partition: $\{\{a\}, \{b\}\}$ — two cells.
3. **$\varepsilon = 0.6$**: $h^{(0.6)}(a) = 0$ (since $\lfloor 0.5 / 0.6 \rfloor = 0$), $h^{(0.6)}(b) = 1.2$ (since $\lfloor 1.5 / 0.6 \rfloor = 2 \cdot 0.6 = 1.2$). Still two cells.
4. **$\varepsilon = 0.4$**: $h^{(0.4)}(a) = 0.4$ ($\lfloor 0.5/0.4 \rfloor \cdot 0.4 = 1 \cdot 0.4 = 0.4$), $h^{(0.4)}(b) = 1.2$ ($\lfloor 1.5/0.4 \rfloor \cdot 0.4 = 3 \cdot 0.4 = 1.2$). Two cells.
5. **Add a third point** $h(c) = 0.95$. **$\varepsilon = 0.5$**: $h^{(0.5)}(c) = 0.5$, distinct from $a, b$, three cells. **$\varepsilon = 0.4$**: $h^{(0.4)}(c) = 0.8$, $h^{(0.4)}(a) = 0.4$, $h^{(0.4)}(b) = 1.2$ — three cells.
6. **Construct non-monotone case** with $h(d) = 1.0$ added. **$\varepsilon = 1$**: $h^{(1)}(d) = 1 = h^{(1)}(b)$, so $\{d, b\}$ merge into one cell. Four input vertices, three cells. **$\varepsilon = 0.4$**: $h^{(0.4)}(d) = 0.8$, which equals $h^{(0.4)}(c) = 0.8$ — now $\{c, d\}$ merge. So at $\varepsilon = 1$ the partition is $\{\{a\}, \{b, d\}, \{c\}\}$, at $\varepsilon = 0.4$ it is $\{\{a\}, \{c, d\}, \{b\}\}$. Both partitions have $3$ cells, but they are *incomparable* in the refinement order — neither refines the other.
7. **Conclusion**: refining $\varepsilon$ can both *split* old cells and *merge* old cells (by aligning previously-distinct values onto a coarser sub-grid). This non-monotonicity is the **first obstruction** to a direct proof of Conjecture C1 noted in §8.3.
8. The empirical resolution (frozen in §8.5) is to test convergence within $2\sigma$ over an $\varepsilon$-sweep rather than expecting pointwise monotonicity — an engineering compromise that the literal $\varepsilon \to 0$ limit obscures. $\blacksquare$

#### Exercise 8.5: H1 Hypothesis Test on Synthetic Validation-Loss Trace
**Task.** Given a synthetic validation-loss trace $\{\ell_t\}_{t=1}^{200}$ with $\ell_t = 0.3 + 0.5 \exp(-t / 30) + 0.01 \xi_t$ where $\xi_t \sim \mathcal{N}(0, 1)$, determine the smallest epoch $T^*$ at which hypothesis H1 (§8.3) is satisfied: $\ell_t \leq 1.05 \cdot \ell^* $ for a 50-epoch window, where $\ell^*$ is the plateau loss.

**Solution.**
1. **Plateau loss**: as $t \to \infty$, $\ell^* = 0.3$.
2. **H1 condition**: $\ell_t \leq 1.05 \cdot 0.3 = 0.315$ for all $t$ in a 50-epoch window.
3. **Deterministic part**: $0.3 + 0.5 e^{-t/30} \leq 0.315 \Leftrightarrow 0.5 e^{-t/30} \leq 0.015 \Leftrightarrow t \geq 30 \ln(0.5 / 0.015) = 30 \ln 33.33 \approx 105.2$.
4. **Stochastic margin**: with $\xi_t \sim \mathcal{N}(0, 1)$ scaled by $0.01$, the standard deviation of $\ell_t$ is $0.01$. For the window-condition to hold with $\sim 95\%$ probability over $50$ consecutive epochs, we need $0.3 + \mathrm{tail} \leq 0.315$ with high probability. A $2\sigma$ tail is $0.02$, exceeding the budget $0.015$, so the *stochastic* component matters near the deterministic threshold.
5. **Practical H1 satisfaction**: the deterministic threshold is at $t = 105$, but stochastic violations push the safe satisfaction window to $T^* \approx 130$ (when the deterministic part has shrunk to $0.302$, leaving slack for the noise).
6. **Coverage in E08**: H1 coverage at $T = 100$ is $\approx 60\%$ (some seeds plateau slightly later); at $T = 150$ it's $\approx 98\%$. This is the source of the H-clean coverage statistics reported in §8.5 (range $[0.900, 0.945]$ across tasks at the operational $T$).
7. **Engineering moral**: the H1 hypothesis is not free — it requires non-trivial training time and inflates the cost envelope of E08 by a factor proportional to the inverse-margin shrinkage of $\ell - \ell^*$. This is why C1 cost $\$0.87$ and not $\$0$: the H1 plateau is the dominant cost driver. $\blacksquare$

#### Exercise 8.6: $L = 2$ Anchor Fragility on Tree-Like Graphs
**Task.** Show that on the complete binary tree $T_{\mathrm{bin}, 4}$ ($n = 31$) at $L = 2$, the LossyWL receptive field at a leaf vertex $v$ misses *most* of the graph, and use this to explain the Stage M $L = 2$ collapse $\mathcal{A}_{\mathrm{pass}} \to \{\mathrm{GCN}\}$.

**Solution.**
1. **Receptive field at a leaf** $v$ at depth $L = 2$: $|\mathcal{N}_2(v)| = 1 + 1 + 1 = 3$ vertices (self, parent, grandparent).
2. **Total graph size** $n = 31$. Coverage: $3 / 31 \approx 9.7\%$.
3. **Implication**: the LossyWL color at a leaf vertex at $L = 2$ depends only on a tiny subset of the graph. Any task that requires structural information from outside the receptive field is unresolvable.
4. **Why GIN/GatedGCN collapse**: GIN's set-aggregation does not include a degree feature; with only 3 vertices in the receptive field and a near-uniform local structure, GIN cannot separate leaves from internal nodes at depth $2$. GatedGCN's gating mechanism introduces continuous attention weights that further blur the partition.
5. **Why GCN survives**: GCN's degree-init provides immediate structural information $\mathrm{deg}(v) = 1$ for leaves vs.\ $\mathrm{deg}(v) \geq 2$ for internal nodes — a *depth-0* discrimination that survives even at $L = 2$.
6. **Recovery at $L \geq 3$**: with $L = 3$, the receptive field at a leaf grows to $|\mathcal{N}_3(v)| = 1 + 1 + 1 + 2 = 5$ vertices, still small but now including a great-grandchild branch — enough structural information for GIN/GatedGCN to reconstruct the relevant cell-multiset.
7. **General principle**: **under-reach** (Corollary 7.4) is depth-and-graph-dependent. Tree-like graphs with high diameter relative to depth produce *bit-identical* failures across the $\mathcal{A}_{\mathrm{pass}}$ dichotomy. This is the precise mechanism of the Stage M $L = 2$ anchor fragility and why §8.5 reports depth-$\geq 3$ as the headline regime. $\blacksquare$

#### Exercise 8.7: Vertex-Transitivity Vacuity on Cayley Graphs
**Task.** Generalize Lemma 8.4 from $C_6$ to an arbitrary connected Cayley graph $\mathrm{Cay}(H, S)$ with finite group $H$ and symmetric generating set $S$. Conclude that paper-02's C1' substrate is in *natural correspondence* with the WL-vacuous family.

**Solution.**
1. **Cayley graph definition**: vertices $V = H$, edges $E = \{(h, h s) : h \in H, s \in S\}$.
2. **Vertex-transitivity**: for any $h_1, h_2 \in H$, the left-multiplication map $\sigma_{h_2 h_1^{-1}}: h \mapsto h_2 h_1^{-1} h$ is a graph automorphism (since $S$ is fixed and the edge structure is invariant under left multiplication). And $\sigma(h_1) = h_2$, so $\mathrm{Aut}(\mathrm{Cay}(H, S))$ acts transitively on $V$.
3. **WL stable partition**: by Exercise 1.8's argument, vertex-transitivity collapses every iteration of WL under constant init to the single-cell partition $\{V\}$.
4. **Task constancy**: any $f \in \mathcal{F}_{\mathrm{WL}}(\mathrm{Cay}(H, S))$ is constant on $V$, hence $\mathrm{DIG} = 0$ for every partition.
5. **C1 vacuity** on Cayley graphs: $\Delta_\varepsilon \equiv 0$ trivially, so C1 is *untestable* on this substrate.
6. **C1' substrate**: paper-02 targets exactly the family that is vacuous for C1 — the vertex-transitive Cayley substrate $\{C_n, \mathrm{Petersen}, \mathrm{Rook}_{4,4}, \mathrm{Shrikhande}\}$. These are all Cayley graphs of small finite groups (cyclic groups $\mathbb{Z}/n$, the Petersen Kneser graph $K(5, 2)$ as a Cayley graph of $A_5$, etc.).
7. **Natural correspondence**: the duality is precise — *every* vertex-transitive substrate that vacates C1 is *exactly* the natural substrate for C1', because the WL-collapse is what makes the 2-WL distinction non-trivial. The two conjectures partition the substrate-architecture space cleanly without overlap, justifying the separation into paper-01 (C1) and paper-02 (C1'). $\blacksquare$

#### Exercise 8.8: Per-Cell Signed-Pass Fraction — Mechanism of GIN Collapse
**Task.** Define the **cell-level signed-pass fraction** $\sigma_C := |\mathrm{signed\_pass}_C| / |\mathrm{H\_clean}_C|$ — the fraction of H-clean seeds in cell $C$ for which $\Delta_\varepsilon$ converges to zero with the *correct sign convention* (`physical`). Use the §8.5 collapse data ($\sigma_C^{\mathrm{GIN}}(\mathrm{ER}_{20,0.20}, L = 2) = 1.00 \to 0.00$) to interpret why GIN fails on this anchor row.

**Solution.**
1. **Pre-collapse**: $\sigma_C = 1.00$ means every H-clean seed in cell $C$ shows the expected sign of $\Delta_\varepsilon$ — a perfect signal in favor of C1.
2. **Post-collapse**: $\sigma_C = 0.00$ means *no* H-clean seed shows the expected sign. This is not noise; it is a *systematic* sign-flip.
3. **Mechanism on $\mathrm{ER}_{20, 0.20}$ at $L = 2$**: the Erdős–Rényi graph at $p = 0.20$ has expected degree $\approx 4$, and depth $L = 2$ yields a receptive field of $\sim 1 + 4 + 4 \cdot 3 \approx 17$ vertices out of 20 — nearly the full graph. GIN's set-aggregation collapses the multiset structure into a sum, washing out the fine differences that distinguish cells.
4. **Why GCN passes**: GCN's normalized aggregation $h_v = \sum_{u \in \mathcal{N}(v)} h_u / \sqrt{\mathrm{deg}(u) \mathrm{deg}(v)}$ preserves the degree-discrimination feature throughout the update. The partition induced by GCN at $L = 2$ on $\mathrm{ER}_{20, 0.20}$ retains $\sim 10$ cells; GIN's partition collapses to $\sim 2$.
5. **Cell-multiset signature**: GIN aggregates the multiset of neighbor representations into a single sum; if all neighbors share the same coarse representation (because GIN itself coarsened them at $L = 1$), the sum is identical across cells. This is the **rank deficiency** that drives the $1.00 \to 0.00$ collapse.
6. **Recovery at $L = 3$**: with one more depth, GIN's representation has another round to incorporate degree-like information through the multiset cardinality, and $\sigma_C$ recovers to $\sim 0.95$. This is the precise depth-recovery claim sealed in `PAMPC-E08-M-DEPTH-RECOVERY`.
7. **General principle**: GIN's expressivity is *equivalent to 1-WL* in the lossless limit, but its *practical robustness* under quantization is strictly worse than GCN's at shallow depths. The architectural dichotomy of §8.5 is therefore not about asymptotic expressivity but about *finite-depth, finite-precision* behavior. $\blacksquare$

#### Exercise 8.9: Oracle Invariance — Why 1-WL and 2-WL Agree on Stage K
**Task.** Explain why the Stage L oracle-invariance result ($n_{\mathrm{eq}}/n = 4125/4125$ across lossy / lossless-1-WL / folklore-2-WL oracles) is *consistent* with 2-WL being strictly more expressive than 1-WL on general graphs.

**Solution.**
1. **2-WL strictly stronger**: in general, the 2-WL test distinguishes graphs that 1-WL cannot (e.g.\ strongly regular graphs with matching parameters).
2. **Stage L substrate**: the canonical 5-graph anchor $\{K_{1,4}, K_{2,3}, P_5, \mathrm{Lolli}_{4,3}, \mathrm{ER}_{10, 0.30}\}$ is *not* in the SRG family; on these graphs the 1-WL stable partition already separates all relevant orbits.
3. **Task class**: $\mathcal{F}_{\mathrm{WL}}$ tasks are constant on 1-WL cells. By definition, on any graph where 1-WL = 2-WL (which holds for trees, regular non-SRG graphs, and most small graphs), the 2-WL stable partition is identical to the 1-WL stable partition. Hence the reference DIG is *bit-identical* across oracles.
4. **Why $4125/4125$**: every row in the sealed grid corresponds to a graph in the Stage K substrate where 1-WL and 2-WL stabilize to the same partition; the empirical DIG (which depends only on the partition cell-structure, not on the oracle's name) is therefore literally the same number.
5. **Where would oracles diverge?** On 2-WL-only-distinguishable graphs like $\mathrm{Rook}_{4,4}$ vs.\ $\mathrm{Shrikhande}$. But Stage M's investigation of this pair found that *both* graphs collapse to single-cell under all three oracles for the canonical task suite — oracle-invariance survives, but trivially.
6. **Operational moral**: 1-WL$\,=\,$2-WL on the C1 substrate is a *fortunate computational coincidence* that allowed the C1 verdict to be sealed without 2-WL machinery. The C1' substrate (Cayley graphs) is precisely where oracle invariance *must* fail in interesting ways — hence its reservation for paper-02. $\blacksquare$

#### Exercise 8.10: Total Cost Envelope Validation
**Task.** Verify the total cost envelope of §8.5 ($\$0.87$ at $1.18$ GPU-h) by line-summing the stage costs, and compare to the $24$ GPU-h cap. What fraction of the cap was actually spent?

**Solution.**
1. **Stage costs** (from §8.5):
   - Stages G + H: $\$0.35$, $0.48$ GPU-h.
   - Stage K (post-hoc rule-fix): $\$0.00$, $0$ GPU-h.
   - Stage L (post-hoc oracle invariance): $\$0.00$, $0$ GPU-h.
   - Stage M (anchor extension, 4-task parallel): $\$0.52$, $0.70$ GPU-h.
   - C1 freeze (post-hoc analyzer): $\$0.00$, $\sim 2$ h wallclock CPU (no GPU).
2. **Sum**: $\$0.35 + \$0.00 + \$0.00 + \$0.52 + \$0.00 = \$0.87$. ✓
3. **GPU-hour sum**: $0.48 + 0 + 0 + 0.70 + 0 = 1.18$ GPU-h. ✓
4. **Cap utilization**: $1.18 / 24 = 4.92\%$, i.e.\ approximately $5\%$ of the $24$ GPU-h cap.
5. **Cost efficiency interpretation**: a $\$0.87$ verdict on the central continuous-transfer hypothesis of the field corresponds to roughly **$30 \times $ cost reduction** vs.\ a naive non-staged sweep (the upper-bound $4{,}125$-cell at $\sim 1$ min/cell $\sim 69$ GPU-h). This compression came from kill-gate staging (B.1–B.8 edge instances at $\leq 2$ GPU-h before bulk runs).
6. **Comparison with paper-02 budget**: C1' on Cayley substrates is expected to require 2-WL machinery (PPGN, $k$-GNN), each $\sim 10\times$ the compute of 1-WL. Budget estimate: $\sim \$10$, $\sim 10$ GPU-h — still well under the $24$ GPU-h cap, validating the staged-protocol methodology.
7. This sub-$\$1$ cost is the empirical demonstration of §7.7's promise: PA-MPC's $90 \times$ computational advantage over training-based GNN screening translates directly into *order-of-magnitude* cheaper science when applied carefully through kill-gate staging. $\blacksquare$

---

*End of monograph.*
