Below are the P1 patches as drop-in text. I've kept the math at submission rigor, flagged exactly where each patch goes, and ended each with a **Rigor** note (what carries the proof / what must be checked) and a **Needs** note (experiment or formalization required to back the claim). Numbering: I refer to new results by content because your missing Prop 6/7 (P0-B1) will shift the global count — renumber after those are restored.

The unifying decision in PATCH A–C is the one I recommended: make the **quantitative WL ceiling + an exact three-term risk decomposition** the centerpiece, and demote trees/VQ to the unifying lens. PATCH C also supplies the *corrected* feature/head diagnostic that supersedes the inverted E3d-arch definition (P0-B2) and prescribes the $k\ll n$ re-run that fixes the cardinality confound (P0-B3) — you can't reframe around that section while it's broken.

---

## PATCH A — Replacement Abstract

*Placement: replaces the current Abstract verbatim.*

> Many machine-learning predictors are constant on the cells of a fixed partition of their input space: decision trees on leaves, vector quantisers on Voronoi cells, message-passing graph neural networks (MPNNs) on Weisfeiler–Leman colour classes. For every such family the partition is the irreducible expressivity bottleneck. Starting from the classical Fano (1961) and Hellman–Raviv (1970) inequalities, we package a two-sided closed-form bracket between the Bayes error $\varepsilon^{*}_{\Pi}$ of the best constant-on-cells predictor of a binary label $f$ and the partition-conditional entropy $H(f\mid\Pi)$,
> $$ H_{\mathrm{bin}}^{-1}\!\bigl(H(f\mid\Pi)\bigr) \le \varepsilon^{*}_{\Pi} \le \tfrac{1}{2}H(f\mid\Pi),$$
> tight on both boundaries, with maximal $\varepsilon$-width $w^{*}=\tfrac12 H_{\mathrm{bin}}(1/5)-1/5\approx 0.1610$ across the entire binary achievable region.
>
> The bracket is elementary; our contribution is what it buys for graph learning. (i) Substituting the depth-$L$ 1-WL partition turns the qualitative Xu–Morris ceiling ("no MPNN exceeds 1-WL") into a *quantitative* one: no depth-$L$ MPNN can drive transductive training error below $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi^{\mathrm{WL}}_L))$, and a training-free per-cell majority head already attains $\tfrac12 H(f\mid\Pi^{\mathrm{WL}}_L)$. (ii) We give an *exact* three-term decomposition of any trained MPNN's risk against this ceiling, separating structural ceiling, feature refinement, and head/optimisation slack — three confounds the standard "accuracy after training" comparison entangles. (iii) We prove an $\varepsilon$-robust constancy lemma (Lemma 6′) that survives positional encodings and bounded random features, together with a spectral refinement (Lemma 6″) replacing the worst-case degree $\Delta$ by the adjacency Perron root $\lambda_{\max}(A)\in[\bar d,\Delta]$, recovering the empirically observed degree-independence of mean/sym-norm aggregators.
>
> Empirically (§8.5): on coarse-partition feature-rich graphs (CiteSeer, PubMed) the WL bracket genuinely bounds realised error; on a heterogeneous architecture menu over UCI Adult it is a statistically significant training-free NAS pre-filter (Kendall $\tau=0.48$, $p=5\times10^{-5}$) while parameter count *anti*-ranks the same menu. We report the bracket's failure regimes — partition-cardinality collapse on near-discrete graphs, small-$n$ overfitting on the NAS pre-filter — with equal prominence, and locate both inside the finite-sample theorem (Proposition 7) that also gives the tool its bite on large data. Synthetic verification (`verify.jl`, $10^3$ partitions, exact rational + interval arithmetic) and a Lean 4 formalisation of Theorem 1 and Corollary 2 close the loop. **Scope.** Finite $V$, finite $\Pi$, binary $f$.

**Rigor.** The abstract now claims only what survives audit: the bracket is "elementary" (no novelty asserted for the inequality itself), the WL quantitative ceiling is the headline, and the empirical line names the *informative* benchmarks (CiteSeer/PubMed, Adult-NAS) rather than the tautological CART/LR matches. The "$w^*$ = maximal width of the achievable region" framing is defensible (binary Fano/HR curves *are* the region boundaries, Prop 1.5) and drops the "first ever" claim.

**Needs.** The Lean 4 line in the abstract is now a *commitment*, not "in preparation" — see PATCH on formalization in the Needs list at the end.

---

## PATCH B — New introductory subsection: the central question

*Placement: insert as a new subsection immediately after "### The two questions" and before "### Why entropy?". This is the pivot that makes graphs the centerpiece.*

> ### The question a node-classification practitioner actually asks
>
> The Weisfeiler–Leman ceiling of Xu et al. (2019) and Morris et al. (2019) is the most-cited structural result in graph learning, but it is a *binary verdict*: a pair of graphs is either 1-WL-distinguishable or it is not. That is the right abstraction for graph-classification expressivity, and it is silent on the question a node-classification practitioner faces before training: *on my graph, with my label vector, how much can a depth-$L$ MPNN possibly recover?* Substituting the depth-$L$ 1-WL partition $\Pi^{\mathrm{WL}}_L$ into the bracket answers this in two numbers per $(\text{graph},L)$ pair — a Fano floor no depth-$L$ MPNN can break, and a constructive ceiling a training-free majority head attains — computed at the cost of the same 1-WL hash that already underlies every GIN implementation.
>
> Two consequences organise the rest of the paper. First, the bracket converts the Xu–Morris ceiling from "cannot distinguish" to "cannot drive training error below $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi^{\mathrm{WL}}_L))$", with the $w^{*}\approx 0.16$ slack of Corollary 2 as the exact, closed-form-irreducible gap between that floor and the plug-in ceiling. Second — and this is the diagnostic we most want to advance — the bracket *decomposes* the gap between a trained MPNN and its WL ceiling into a structural term (WL-side), a feature-refinement term, and a head/optimisation term (Proposition [Risk-Decomposition], §8.3). The current convention of comparing architectures by post-training accuracy entangles all three; the bracket separates the first cleanly from the other two, at no training cost on the structural term.

**Rigor.** This paragraph promises only what Cor 7 and the decomposition identity deliver; it does not claim generalization (the bracket is transductive/fitting, which §8.3 and Prop 7 must state explicitly — see PATCH C and the train/test caveat).

**Needs.** Nothing new; it forward-references results that PATCH C and your restored Prop 7 must contain.

---

## PATCH C — New result: exact risk decomposition against the WL ceiling (the corrected E3d-arch)

*Placement: new subsection §8.3.1, immediately after Corollary 7. This both elevates the decomposition to a formal result and fixes the inverted sign and the cardinality confound of the old E3d-arch. The old E3d-arch prose ("negative head_sig = head extracts sub-cell structure …") should be deleted and replaced by the experiment prescribed in **Needs**.*

> **An exact decomposition of trained risk against the WL ceiling.** Fix a depth-$L$ MPNN trained on $G$ with penultimate embeddings $Z\in\mathbb R^{n\times d}$ and thresholded readout $\hat f=\tau\circ Z$, realising transductive risk $\hat R$. Write $\Pi^{\mathrm{WL}}_L$ for the ideal (feature-free) depth-$L$ 1-WL partition and $\varepsilon_{\mathrm{WL}}:=\varepsilon^{*}_{\Pi^{\mathrm{WL}}_L}$ for its Bayes error; fix a cell budget $k$ and let $\Pi^{Z}_k$ be the $k$-cell partition obtained by clustering $Z$ (e.g. $k$-means), with Bayes error $\varepsilon^{Z}_k:=\varepsilon^{*}_{\Pi^{Z}_k}$. Then, identically,
> $$\hat R \;=\; \underbrace{\varepsilon_{\mathrm{WL}}}_{\text{structural ceiling}} \;-\; \underbrace{\bigl(\varepsilon_{\mathrm{WL}}-\varepsilon^{Z}_k\bigr)}_{\Delta_{\mathrm{feat}}\ \text{(feature refinement)}} \;+\; \underbrace{\bigl(\hat R-\varepsilon^{Z}_k\bigr)}_{\Delta_{\mathrm{head}}\ \text{(head / optimisation slack)}}, \tag{$\star$}$$
> and the structural term is itself bracketed, $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi^{\mathrm{WL}}_L))\le \varepsilon_{\mathrm{WL}}\le \tfrac12 H(f\mid\Pi^{\mathrm{WL}}_L)$, training-free.
>
> Each term is separately measurable. $\Delta_{\mathrm{feat}}>0$ certifies that real-valued node features refine the partition beyond what 1-WL structure alone permits at the same cell budget; $\Delta_{\mathrm{feat}}<0$ flags an architecture that *destroys* structural information (we observe this for attention on PubMed, §8.5). $\Delta_{\mathrm{head}}\ge 0$ would say the linear readout under-realises the label structure already present in its own embedding geometry; $\Delta_{\mathrm{head}}\le 0$ says the readout's half-space partition beats per-cell majority at budget $k$. *Neither sign is guaranteed in general* — $(\star)$ is an identity, and the two gaps are diagnostics, not theorems — which is precisely why they are informative: the decomposition attributes any trained–vs–ceiling gap to features, to optimisation, or to a finite-width approximation of the injective aggregator of Xu Theorem 3, *never* to expressivity.
>
> **Resolution condition.** The decomposition is meaningful only when the cell budget is bounded away from $n$: at $k\gtrsim n$ both $\varepsilon_{\mathrm{WL}}$ and $\varepsilon^{Z}_k$ collapse to per-vertex memorisation ($\to 0$ irrespective of embedding quality), and $\Delta_{\mathrm{feat}},\Delta_{\mathrm{head}}$ degenerate into small differences of memorisation artefacts. We therefore evaluate $(\star)$ at $k\ll n$ and report $k/n$ alongside every row; the informative regime is $|\Pi|/|V|$ bounded away from both $0$ and $1$, consistent with Proposition 4.5 and Proposition 7.

**Rigor.** $(\star)$ is an exact algebraic identity (verify: the three bracketed terms sum to $\hat R$), so it cannot be wrong — the content is in the measurability and interpretation of the terms, both stated conservatively. The two sign statements are explicitly *not* claimed as guaranteed; this is the fix for P0-B2, where the old text asserted a sign that the definition and data contradict. The structural-term bracket is just Cor 7 applied to $\Pi^{\mathrm{WL}}_L$. The "resolution condition" is the fix for P0-B3: it forbids reading $(\star)$ at $k\approx n$, which is exactly where the old E3d-arch read Cora ($k/n=0.87$).

**Needs (experiment, blocking the centerpiece).** Re-run the GCN/GAT/GIN/SAGE sweep computing $(\star)$ at **$k\in\{8,16,32,64,128\}$ with $k/n\le 0.1$ on every dataset** (Cora, CiteSeer, PubMed, Twitch-EN; ogbn-arxiv if GPU budget allows). Report $\hat R$, $\varepsilon_{\mathrm{WL}}$, $\varepsilon^Z_k$, $\Delta_{\mathrm{feat}}$, $\Delta_{\mathrm{head}}$, and $k/n$. The three findings (features refine WL; attention can erase structure; head slack) must be re-established *in this regime* or retracted. Eval must use the *same* $k$ for $\varepsilon_{\mathrm{WL}}$ and $\varepsilon^Z_k$ so feat_gap is not confounded by a cell-count mismatch (the current PubMed/Twitch caveat disappears once $k$ matches).

---

## PATCH D — New result: spectral / average-degree refinement of Lemma 6′

*Placement: new "Lemma 6″" immediately after Lemma 6′, before Corollary 7. This is the genuinely new theory (P1-Task 7) and the answer to "Lemma 6′ is loose by $10^6$."*

> **Lemma 6″ (spectral refinement of the sum-aggregator envelope).** Adopt the hypotheses of Lemma 6′ with sum aggregation and layer-wise Lipschitz constants $(L^{c}_\ell,L^{m}_\ell)\ge 0$. For each vertex $v$ and level $\ell$ define the within-WL-cell potential
> $$x^{(\ell)}_v \;:=\; \max_{w\,\sim_{\mathrm{WL}_\ell}\,v} d\bigl(h^{(\ell)}(v),h^{(\ell)}(w)\bigr),\qquad x^{(0)}_v\le \delta_0,$$
> and let $A$ be the adjacency matrix of $G$. Then, componentwise,
> $$x^{(L)} \;\le\; \delta_0\,\Bigl[\textstyle\prod_{\ell=1}^{L}\bigl(L^{c}_\ell I + L^{m}_\ell A\bigr)\Bigr]\mathbf 1, \tag{6″a}$$
> and the mass-weighted within-cell spread $\bar\delta_L:=\sum_v q_v\,x^{(L)}_v$ obeys
> $$\bar\delta_L \;\le\; \delta_0\,\Bigl\|\textstyle\prod_{\ell=1}^{L}\bigl(L^{c}_\ell I + L^{m}_\ell A\bigr)\Bigr\|_{\mathrm{op}} \;=\; \delta_0\,\max_{k}\Bigl|\textstyle\prod_{\ell=1}^{L}\bigl(L^{c}_\ell + L^{m}_\ell\lambda_k\bigr)\Bigr|, \tag{6″b}$$
> where $\{\lambda_k\}$ is the spectrum of $A$. For connected non-bipartite $G$ (Perron root dominating, $\lambda_{\max}(A)\ge|\lambda_{\min}(A)|$),
> $$\bar\delta_L \;\le\; \delta_0\,\prod_{\ell=1}^{L}\bigl(L^{c}_\ell + L^{m}_\ell\,\lambda_{\max}(A)\bigr),\qquad \bar d \;\le\; \lambda_{\max}(A) \;\le\; \Delta. \tag{6″c}$$
> Consequently, for an $L_\tau$-Lipschitz readout thresholded at $1/2$ and a cell-margin condition (per-cell readout confidence $\ge\gamma$ from the threshold),
> $$R_V(\hat f) \;\ge\; \varepsilon^{*}_{\Pi_L} \;-\; \frac{L_\tau\,\bar\delta_L}{\gamma}. \tag{6″d}$$
>
> *Proof.* The Lemma 6′ recursion, instantiated for sum aggregation with the bijection $\sigma:N(v)\to N(w)$ between ideal-WL-cellmates, gives $d(h^{(\ell+1)}(v),h^{(\ell+1)}(w))\le L^{c}_{\ell+1}\,x^{(\ell)}_v + L^{m}_{\ell+1}\sum_{u\in N(v)} x^{(\ell)}_u$, since $w\sim_{\mathrm{WL}_\ell}v$ and each $\sigma(u)\sim_{\mathrm{WL}_\ell}u$. Maximising over $w$ yields $x^{(\ell+1)} \le (L^{c}_{\ell+1}I + L^{m}_{\ell+1}A)\,x^{(\ell)}$ entrywise; the matrix is entrywise non-negative, so iteration preserves the inequality, giving (6″a). All factors are polynomials in $A$ and hence commute, so the product is order-independent and symmetric; (6″b) follows from $\tfrac1n\mathbf 1^\top P(A)\mathbf 1\le \|P(A)\|_{\mathrm{op}}$ and $\|P(A)\|_{\mathrm{op}}=\max_k|P(\lambda_k)|$. (6″c) uses $P(\lambda)=\prod_\ell(L^c_\ell+L^m_\ell\lambda)$ increasing and positive on $[\,|\lambda_{\min}|,\lambda_{\max}]$ under the stated regularity, together with the Rayleigh bounds $\bar d=\mathbf 1^\top A\mathbf 1/n\le\lambda_{\max}(A)$ and $\lambda_{\max}(A)\le\Delta$. (6″d): under the margin condition a vertex disagrees with the cell-Bayes rule only if $L_\tau x^{(L)}_v>\gamma$; by Markov the flipped mass is $\le L_\tau\bar\delta_L/\gamma$. $\square$
>
> Lemma 6″ recovers the Lemma 6′ envelope when $\lambda_{\max}(A)$ is replaced by its upper bound $\Delta$, and recovers Lemma 6 at $\delta_0=0$. The operative constant is the **adjacency Perron root**, not the maximum degree: for the near-regular degree profiles of real citation graphs $\lambda_{\max}(A)\ll\Delta$, so (6″c) is many orders tighter than (6′) on exactly the graphs where (6′) was vacuous. The aggregator dichotomy persists in sharpened form — sum amplifies by $\prod_\ell(L^c_\ell+L^m_\ell\lambda_{\max}(A))$, mean/sym-norm by $\prod_\ell(L^c_\ell+L^m_\ell)$ — and the residual gap to the empirical per-layer amplification $\gamma_{\mathrm{eff}}$ is the vector-cancellation effect (non-aligned neighbour differences), which a Lipschitz argument cannot capture and which a second-moment / concentration analysis is required to close.

**Rigor.** Every step is elementary and checkable: (6″a) is a non-negative-matrix monotone iteration; commutativity (all factors polynomial in symmetric $A$) makes the product spectrally diagonalisable, giving the exact operator norm in (6″b); the degree sandwich is two one-line Rayleigh-quotient facts. The only *new hypothesis* is the cell-margin $\gamma$ in (6″d), which I have stated explicitly because the original Lemma 6′ Step 4 ("disagreement mass $\le L_\tau\delta_L$") was hand-waved at this exact point — your refinement should make the margin assumption a labelled hypothesis, not silent. Do **not** claim a tighter *sup*-diameter bound (the sup is genuinely governed by $\Delta$ via high-degree vertices); the refinement is honestly a *mass-average* statement, which is also what the risk in (6″d) needs.

**Needs (experiment).** In the E3d redo, additionally report (i) $\lambda_{\max}(A)$, $\bar d$, $\Delta$ for each graph; (ii) the (6″c) bound vs the (6′) bound vs measured $\bar\delta_L$ and the sup $D(L)$. Expectation to confirm: (6″c) sits orders below (6′) (closing most of the reported $10^6$ gap) and the *residual* looseness vs measured spread is the cancellation factor. State the residual honestly rather than projecting the full $10^6$ closure.

**Needs (formal verification, optional but high-value).** (6″a) and the non-negative-matrix monotonicity are clean Lean 4 targets (`Matrix`, entrywise order, `Finset.sum`); a kernel-checked (6″a) would be a strong differentiator. The spectral step (6″b) needs `Matrix.IsHermitian` spectral theory and is heavier — defer.

---

## PATCH E — Related-work paragraph differentiating Lemma 6′/6″ from GNN-stability

*Placement: append to §9 under "MPNN expressivity".*

> **Stability vs robust constancy.** A substantial literature bounds how GNN *outputs* change under *graph* perturbation — graphon-sampling and edge-rewiring stability (Gama–Bruna–Ribeiro and successors), spectral-filter robustness certificates (Kenlay et al.), and the oversquashing analyses that trace sensitivity decay to degree and spectral-gap quantities (Alon–Yahav; Topping et al.; Di Giovanni et al.). Lemma 6′/6″ are orthogonal in object and direction. The perturbation is to the *initial features* $h^{(0)}$ (positional encodings, random features, ID signals), not to the graph; the bounded quantity is the *within-WL-cell embedding diameter*, not output drift; and the use is to certify an $\varepsilon$-robust version of the MPNN–WL *constancy* lemma feeding a Bayes-error *lower* bound, rather than a Lipschitz output-stability guarantee. The aggregator dichotomy of 6″ — sum amplification governed by the adjacency Perron root $\lambda_{\max}(A)$, mean/sym-norm degree-independent — is the constancy-side analogue of the degree-driven sensitivity that the oversquashing literature studies on the output side.

**Rigor.** The differentiation rests on three concrete axes (perturbed object, bounded quantity, inferential direction) that are individually defensible; it does not claim the stability literature is wrong or subsumed.

**Needs (literature verification — do not submit without it).** Confirm exact titles/years and, critically, that no existing paper already bounds a *WL-cell-conditional* feature-perturbation diameter. Run targeted searches on "Lipschitz constant graph neural network", "GNN stability graphon", "oversquashing spectral gap degree", "random feature GNN expressivity Sato", "positional encoding stability". If any prior bound is a relabelling of 6′, reposition 6″ as the contribution and 6′ as a recalled special case.

---

## PATCH F — $w^*$ honesty reframing

*Placement: replace the sentence in §1 "to our knowledge the first **uniform conservativeness gap** …" and add the footnote at Corollary 2.*

> The bracket width is bounded above by an explicit constant $w^{*}\approx 0.1610$ uniformly in $\Pi$ and $f$ — the maximal $\varepsilon$-extent of the binary achievable region of Feder–Merhav (1994), whose closed form $\tfrac12 H_{\mathrm{bin}}(1/5)-1/5$ we record here.[^wstar]

> [^wstar]: In the binary case the Fano lower curve and the Hellman–Raviv upper line are *exactly* the boundaries of the achievable region (Proposition 1.5), so $w^{*}$ is the genuine maximal width of the realisable $(\varepsilon,H)$ set, not merely the gap between two bounds. We make no priority claim for the constant itself, which is a direct calculus consequence of standard inequalities.

**Rigor.** Trades an unverifiable "first" for a precise, true statement (max width of the region) with the correct attribution. The footnote pre-empts the obvious referee objection ("this is trivial").

**Needs (literature verification).** Check Feder–Merhav (1994), Ho–Verdú (2010), Sason–Verdú (2018), Harremoës–Topsøe, and Prasad-type sharpenings for any prior explicit statement of $0.1610$ / $\varepsilon=1/5$. Cite if found; the footnote already concedes non-priority so this is low-risk.

---

## PATCH G — E1/E2 honest reframing

*Placement: replace the lead framing of E1 and E2. The tables stay; the spin changes.*

> *(E1 lead, replacing "CART's training error matches … later trained.")* CART leaves vote per-cell majority, so a fitted CART **is** the plug-in achiever of Theorem 1 on $\Pi_d$: the four-decimal agreement between CART training error and $\varepsilon^{*}_{\Pi_d}$ is an *identity*, not an empirical finding. E1 is therefore a consistency check — it confirms the implementation and shows the bracket is an *a-priori* statement about a classifier that is only later trained — and the substantive content is the monotone tightening of the bracket with depth (Proposition 4) and that the realised width stays below $w^{*}$ at every depth.

> *(E2 lead, replacing the "if the bracket is a real proxy …" sentence.)* Logistic regression on one-hot cell membership, at convergence, reproduces the per-cell majority vote, so the exact match for $k\le 256$ is again definitional rather than evidential; the two largest budgets differ only by LBFGS sub-optimality on a $1000$-dimensional design. E2 confirms that the bracket endpoints are realised by a genuine (if trivial) trained classifier and that nothing in the optimisation escapes the sandwich.

**Rigor.** States plainly that E1/E2 are identities. This is strictly safer than the current text, which a referee will (correctly) read as presenting a tautology as validation.

**Needs.** Update the abstract (done in PATCH A — "matches to four decimals" removed from the evidence list).

---

## PATCH H — E6-NAS reframing as the genuine practitioner result

*Placement: replace the E6-NAS "Takeaway for practitioners" paragraph.*

> **Takeaway.** The bracket is not a universal NAS surrogate; it is a training-free pre-filter with a sharply characterised success regime. On UCI Adult ($n_{\mathrm{tr}}=36{,}177$) it recovers $7/10$ of the truly best architectures with $\tau=0.48$ and a CI strictly above zero, while parameter count — the standard NAS prior — *anti*-ranks the same menu ($\tau=-0.38$); on every metric on every dataset tested, the bracket dominates parameter count. The regime in which this holds is *large $n$ with a partition family that does not memorise*: on digits-bin ($n_{\mathrm{tr}}=1{,}437$) the ranking collapses to noise because deep-CART and large-$k$ partitions reach $\texttt{lower}=0$ by fitting the training rows, exactly the $O(1/\sqrt n)$ finite-sample face of Proposition 7. The practitioner rule is correspondingly precise: on sufficiently large data, rank by the bracket lower endpoint and ignore parameter count; on small data with overfitting-prone families, either discard the zero-$\texttt{lower}$ architectures or pair the bracket with a held-out split — the same theorem (Proposition 7) that bounds the transfer error on Adult predicts its failure on digits-bin.

**Rigor.** Frames the mixed result as a *characterised regime* (the honest and stronger framing) rather than a hedge, and ties both halves to the one missing theorem you must restore.

**Needs.** This paragraph is load-bearing on **Proposition 7**, which does not yet exist (P0-B1). PATCH H cannot stand until Prop 7 is stated and proved — so although you asked for P1 first, the NAS reframing is gated on that one P0 item. Everything else here is P0-independent.

---

### Consolidated "Needs" checklist (experiments + formalization to back these patches)

1. **E3d-arch redo at $k\ll n$** (PATCH C) — *blocking the centerpiece.* Same-$k$ evaluation of $(\star)$; re-establish or retract F1/F2/F3.
2. **E3d (Lemma 6″) augmentation** (PATCH D) — report $\lambda_{\max}(A),\bar d,\Delta$ and the 6″c-vs-6′-vs-measured comparison; quantify residual cancellation honestly.
3. **Literature verification** for Lemma 6′/6″ vs GNN-stability (PATCH E) and for $w^*$ priority (PATCH F) — both must be done before submission; both are framed to survive a "no priority" outcome.
4. **Lean 4**: commit Theorem 1 + Corollary 2 (abstract now promises it); (6″a) monotone non-negative-matrix iteration is a clean stretch target.
5. **Gated on P0**: PATCH H needs Proposition 7 written first; PATCH A/B/C's "transductive/fitting, not generalization" honesty needs Prop 7 to land the population story.

Want me to draft candidate statements + proofs for the missing **Proposition 6** ($w^*(\pi_*)$ marginal-aware ceiling) and **Proposition 7** (finite-sample concentration) next? Those are the two things half these patches lean on, and Prop 7 in particular I can write to match the E7 Hoeffding numbers so you can check it directly.