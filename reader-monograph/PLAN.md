# Multi-Phase Plan — `gnn.md` Extension (Paper-2 Theory Toolkit)

**Prose target:** [`../gnn.md`](../gnn.md). New chapters are appended as Ch 9–16; the existing eight chapters are not edited.

**Owner:** Ali Elouafiq · **Started:** 2026-05-31 · **Horizon:** multi-session.

This file is the **operational contract** for drafting the reader. It pins
deliverables, definition-of-done (DoD), dependencies, and the per-chapter
construct ledger so any future session can resume cleanly.

---

## 0. Guiding constraints

1. **Scope.** Information theory + probability + measure-free conditioning, *as used by* Paper 2 and its cited references. No new partition combinatorics — defer to [gnn.md](../gnn.md).
2. **Style.** Operational σ(T) = "questions answered by statistic T". Finite/discrete first; remark on extensions only when a cited paper requires them.
3. **Provenance.** Every theorem traces to a reference in `references.bib`. Where a result is also stated in `PAPER-ARXIV.md` §3.2 / Appendix A, link both ways.
4. **Pedagogy.** Each chapter delivers: roadmap → defs/theorems with proofs → worked example → pathology → 5–8 exercises → 1–2 notebook refs.
5. **No emoji, no marketing prose, no time estimates.** Plain math + careful English.

---

## 1. Phase map and DoD

All chapter numbers below refer to **new chapters in `../gnn.md`**.

| Phase | Chapters | Notebooks | DoD |
|---|---|---|---|
| P0 | scaffold + Ch 9 seed | — | bib + reqs land; "End of monograph" marker moved to follow Ch 9; new chapters appear immediately under Ch 8 in `gnn.md` |
| P1 | 9, 10 | nb01–nb03 (stubs) | each ch ≥ 1500 words; ≥ 5 exercises with full solutions inline; cross-links to refs |
| P2 | 11, 12 | nb04–nb08 (stubs) | Ch 12 must reproduce the Jaynes–Lagrangian dual derivation of PAPER-ARXIV.md §3.2 verbatim and cite Appendix A (A.1)–(A.12) |
| P3 | 13, 14 | nb09–nb11 (stubs) | Gini↔Bayes ratio worked; HVS sinusoidal bound visualised; Massey lower bound on geometric |
| P4 | 15 | nb12 (stub) | "statistic T as σ-algebra surrogate" formalised; IB toy demo |
| P5 | 16 | nb13 (stub) | Prop 3.6 prior-aware sharpening reproduced with its trust-tier disclaimer; outlook section links to `future-work/` |
| P6 | — | nb01–nb13 executable | every notebook runs top-to-bottom on `requirements.txt`; saves plots to `plots/` |
| P7 | solutions/ | — | every exercise has a worked solution with cross-ref to chapter theorem numbers |
| P8 | build | — | `make pdf` produces a single PDF via Pandoc + KaTeX/LaTeX |

### Phase dependencies

```
P0 → P1 → P2 → P3 → P4 → P5
                              ↘
P0 → ───────────────────────────→ P6 (needs P1+P2+P3 for content references)
P0 → ─────────────────────────────────→ P7 (needs P1–P5)
P0 → ───────────────────────────────────────→ P8 (needs everything)
```

P6 (notebooks) can begin in parallel with P3 once Ch 5–8 land, since
nb04–nb08 are the heaviest visual artefacts (sandwich envelope).

---

## 2. Per-chapter construct ledger (Ch 9–16 of `../gnn.md`)

Each row lists the **named constructs** the chapter must define, the
**theorems** it must prove or cite-with-proof-sketch, and the **source
papers**. This is the contract that prevents scope creep. The eight
existing chapters (Ch 1–8) of `gnn.md` are not edited.

### Ch 9 — Probability without Measure Theory — σ(T) operationally
- Constructs: discrete RV recap, joint/marginal/conditional, expectation, indicator, statistic $T:\mathcal X\to\mathcal T$; the **operational** $\sigma(T)$ = "the set of questions about $X$ answered by knowing $T(X)$"; equivalence with the partition $\{T^{-1}(t) : t \in T(\mathcal X)\}$ (cross-link to Ch 1).
- Theorems: law of total probability; law of total expectation; tower property for statistics; data-processing inequality for $D_{KL}$ and $I$ in the discrete/measure-free form; conditioning reduces entropy as a corollary.
- Sources: Cover–Thomas Ch 2 + §2.8; Devroye–Györfi–Lugosi §1.
- Cross-link to gnn.md Ch 2 (§2.1 already defines $H$; we generalise to non-binary).

### Ch 10 — The Rényi Family, Min-Entropy, and Generalised Fano
- Constructs: $R_\alpha$ for $\alpha>0,\alpha\ne1$; $R_0$ (log-support), $R_2$ (collision), $R_\infty = -\log\max p$; the prior Bayes risk relation $\varepsilon_X = 1 - 2^{-R_\infty(X)}$.
- Theorems: monotonicity in $\alpha$; $R_\alpha \to H$ as $\alpha\to 1$; Han–Verdú Thm 2 (divergence form of Fano via DPI on the indicator $\mathbf 1\{X=Y\}$); Thms 3–5 (Rényi replacement of $\log M$, dropping the equiprobable assumption); Thm 6 (input-entropy version with maximal $\rho$).
- Sources: `fano-inequality.md` (Han–Verdú); Cover–Thomas §17.

### Ch 11 — Hellman–Raviv, Feder–Merhav, and the Achievable Region
- Constructs: $\tfrac12 H$ upper bound; Feder–Merhav $\Phi(\pi) := h(\pi) + \pi \log(M-1)$ upper envelope on $H$ given $\pi$ and its converse (the piecewise extremal $p_{\min}(\pi)$); the **allowable region** $\{(H, \pi)\}$.
- Theorems: Hellman–Raviv Thm (proof via per-symbol $\min(p, 1-p) \le \tfrac12 H_{\mathrm{bin}}(p)$); Feder–Merhav Lemma 1 + Lemma 2 (region characterisation); piecewise extremal distributions $p_{\min}(\pi)$ for $\pi \in [0, 1/2]$ and $[1/2, 2/3]$ and beyond.
- Sources: `feder.md` (Feder–Merhav full text); Hellman–Raviv 1970; Kovalevskij 1968.

### Ch 12 — The Jaynes–Lagrangian Sandwich (adjusted theory, PAPER-ARXIV.md §3.2)
- Constructs: the *single program, two directions* derivation of §3.2 — reframing both halves of the sandwich as opposite Jaynes max-entropy programs on $\{(q_C, e_C)\}_C$; the achievable region $\tilde A_2$; the quantified slack $w(H) = \tfrac12 H - H_{\mathrm{bin}}^{-1}(H)$ with max $w^* \approx 0.161$ at $\varepsilon = 1/5$; Prop 3.5 non-improvement.
- Theorems: Theorem 1 (sandwich) reproved as the Lagrangian-dual companion of (A.1)–(A.7); Prop 3.5 (no closed-form improvement) with the Hellman–Raviv and Fano witnessing families $\Pi_\alpha^{\mathrm{HR}}$, $\Pi_\varepsilon^{\mathrm F}$ of Appendix A.
- Sources: `PAPER-ARXIV.md` §3.2 + Appendix A (A.1)–(A.9); `notes/paper-arxiv-review/13-bayes-entropy-sandwich-literature-note.md`.

### Ch 13 — Variance, Gini, and HVS Surrogates for the Bayes Error
- Constructs: conditional variance $\mathrm{Var}(Y\mid T)$; Gini index $P(1-P)$ as the rational-arithmetic surrogate used in the Lean witness; Hashlamoun–Varshney–Samarasooriya five-condition framework; the four canonical upper bounds: Bhattacharyya $\sqrt{p(1-p)}$, Equivocation $\tfrac12 H_{\mathrm{bin}}$, Bayesian-distance $2p(1-p)$, HVS sinusoidal $g_N$.
- Theorems: law of total variance; $\min(p,1-p) \le 2p(1-p)$ (Gini–Bayes); the HVS sinusoidal bound is everywhere-continuous and tighter than Bhattacharyya; ordering on a 1-D Gaussian mixture worked example.
- Sources: Breiman et al. 1984; `jir.md` (HVS); Raileanu–Stoffel 2004; PAPER-ARXIV.md Appendix A *variance-shadow* remark.

### Ch 14 — Guessing Entropy (Massey)
- Constructs: optimal guessing strategy $G$; $E[G]$; the relations $E[G] \ge \tfrac14 2^{H(X)} + 1$ and the geometric tightness; non-existence of an entropic upper bound on $E[G]$.
- Theorems: Massey Thms II + III, full proofs; consequence for the rhetorical structure of §3.2 (the positive-sharpness → negative-non-existence promotion used in Prop 3.5).
- Sources: `guess.md` (Massey 1994).

### Ch 15 — Comparison of Experiments, Sufficiency, and the Information Bottleneck
- Constructs: deterministic statistic $T(X)$; coarsening preorder $T \preceq T'$ iff $T$ is a function of $T'$; the **operational σ(T)** as a Blackwell-sufficiency surrogate; Tishby IB Lagrangian $\mathcal L = I(T; X) - \beta I(T; Y)$; LossyWL as a discrete IB on graph statistics (cross-link to gnn.md Ch 4).
- Theorems: monotonicity of $H(Y\mid T)$, $\varepsilon^*_T$, and any $f$-divergence in the coarsening preorder (one corollary of Ch 9 DPI); existence of a $\beta$-optimal $T$ in the discrete case (sketch); IB equation for the discrete case.
- Sources: Le Cam 1964; Blackwell 1953; Tishby–Pereira–Bialek 1999; Kolchinsky–Tracey–Wolpert 2019; background `arXiv-2505.18410v2`.

### Ch 16 — Prior-Aware Sharpening and Open Threads
- Constructs: marginal Bayes error $\varepsilon^*_\varnothing$; binary KL divergence $d_{\mathrm{KL}}$; Prop 3.6 statement; trust-tier disclaimer (Prop 3.6 is *paper-only hand proof*, no Lean witness).
- Theorems: Prop 3.6 $d_{\mathrm{KL}}(\varepsilon^*_\Pi \| \varepsilon^*_\varnothing) \le I(f; \Pi)$ reproduced as a corollary of Ch 9 DPI applied to $f \to \Pi \to Z$; reduction to Theorem 1 when $P_f = 1/2$.
- Sources: `PAPER-ARXIV.md` Prop 3.6 + Appendix A (A.10)–(A.12); `future-work/05-sequel-paper-plan.md`; outlook pointers into `notes/paper-arxiv-review/15-future-work-borrowed-techniques.md`.

---

## 3. Notebook ledger

| ID | File | Belongs to | What it shows |
|---|---|---|---|
| nb01 | `notebooks/nb01_binary_entropy_inverse.ipynb` | Ch 2 | $H_{\mathrm{bin}}$ and its inverse on $[0,1/2]$ |
| nb02 | `notebooks/nb02_kl_divergence_geometry.ipynb` | Ch 2 | $D_{KL}$ contours on 2-simplex |
| nb03 | `notebooks/nb03_renyi_family.ipynb` | Ch 3 | $R_\alpha$ vs $\alpha$ for a few distributions |
| nb04 | `notebooks/nb04_dpi_monte_carlo.ipynb` | Ch 4 | DPI verified numerically over random channels |
| nb05 | `notebooks/nb05_bayes_risk_simulation.ipynb` | Ch 5 | $\varepsilon^*$ vs class overlap |
| nb06 | `notebooks/nb06_fano_envelope.ipynb` | Ch 6 | Lower envelope of $\pi$ vs $H$ |
| nb07 | `notebooks/nb07_hellman_raviv_envelope.ipynb` | Ch 7 | Upper envelope; Feder–Merhav exact region |
| nb08 | `notebooks/nb08_sandwich_two_sided.ipynb` | Ch 8 | Combined sandwich plot |
| nb09 | `notebooks/nb09_gini_vs_bayes.ipynb` | Ch 9 | $\min(p,1-p)$ vs $2p(1-p)$ |
| nb10 | `notebooks/nb10_bhattacharyya_vs_hvs.ipynb` | Ch 10 | All four upper bounds on a 1D Gaussian-mixture |
| nb11 | `notebooks/nb11_guessing_entropy.ipynb` | Ch 11 | Massey bound vs geometric tightness |
| nb12 | `notebooks/nb12_information_bottleneck_toy.ipynb` | Ch 13 | Toy IB curve on a 4×4 joint |
| nb13 | `notebooks/nb13_pampc_bridge_demo.ipynb` | Ch 14 | Sandwich applied to a synthetic graph statistic |

---

## 4. Risks and mitigations

- **Risk:** scope drift into partition combinatorics. **Mitigation:** Ch 12 is explicit that σ(T) is the *operational surrogate*; cite gnn.md whenever partitions would otherwise enter.
- **Risk:** measure-theory creep. **Mitigation:** finite/discrete is the default; continuous extensions only when a cited result demands them, and always with a clear "skip for measure-free reading" tag.
- **Risk:** redundancy with gnn.md. **Mitigation:** the per-chapter ledger above lists no WL constructs; Ch 14 is the only place Paper 2 vocabulary enters.
- **Risk:** notebooks rot. **Mitigation:** P6 pins `requirements.txt`; P8's optional `make pdf` re-executes them.
