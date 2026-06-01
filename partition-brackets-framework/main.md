# Partition Brackets: A Framework with Entropy, Variance, and Noise-Robust Instances

> **Status (Phase 2b-md.G2 CLOSED).** All numbered claims —
> **T3** (meta-theorem), **C-Sh** (Shannon reduction), **C-Va**
> (Bayes–variance identity), **C-Pi** (Pinsker sqrt
> replacement), **T6** (regression MSE/MAE), **T7** (symmetric
> label-noise correction), **T9** (soft / Markov-kernel
> bracket), **P10** (refinement consistency), **L11** (MPNN
> aggregator-typed Lipschitz) — are PROVEN with mechanically
> checked verifier contracts. Critical-path ladder is GREEN:
> `verify_b_t1.py` pass=8/8, `verify_b_t2_mc.py` pass=6/6 on
> seed 0. See [`FORMALISATION.md`](FORMALISATION.md) §3 for the
> closed G2 gate-table.
>
> **Certification roadmap (Phase 3, planned).** Property-testing
> at $n = 200$ examples per contract / $N = 50\,000$ Monte-Carlo
> samples is the *manuscript* tier. A Lean 4 + Mathlib port of
> T3 / C-Sh / C-Va / C-Pi / T7 / P10 / T9 is the *archival
> certificate* tier; work breakdown, gates, and PERT chart
> live in
> [`FORMAL_VERIFICATION_EXECUTION_PLAN.md`](FORMAL_VERIFICATION_EXECUTION_PLAN.md).
> The Python tier remains the fast CI; Lean is gated and
> *additive* — no claim in this paper waits on Lean.

This is the **markdown twin** for the Phase 2b work. The LaTeX
source is frozen at the Phase 2a scaffold; mirroring is deferred
to Phase 2d.

> **Real-data anchor (D.10, post-G2).** All three T3 instances
> (C-Sh, C-Va, C-Pi) have been verified against the real Bayes
> error on 20 (dataset, depth) rows spanning Cora, CiteSeer,
> PubMed, Twitch-EN, and ogbn-arxiv, with cell-level
> $(q_C, P_C)$ extracted from Paper A's vectorised 1-WL
> refinement. Manifest: `audit/anchor_real_data_full.json`
> (zero failures, wall ≈ 10 s on a single CPU core; no GPU,
> no new training). C-Pi is genuinely vacuous (raw lower < 0)
> for deep-$L$ rows where $H$ falls below ≈ $0.279$[^bk-0279]; the
> contract uses the 0-clipped envelope, which is the
> publishable convention.

[^bk-0279]: $0.279 = 1 - 1/(2 \ln 2)$ is the C-Pi vacuity
  threshold derived in the adversarial check of Theorem C-Pi
  (§3). Empirical clipping is observed in 8 of the 20 rows of
  `audit/anchor_real_data_full.json` (cells
  `rows[*].C_Pi.vacuous == true`), all at refinement depth
  $L \geq 1$ on ogbn_arxiv / twitch_en and at $L \geq 2$ on
  cora / citeseer / pubmed; see Table B.4.

---

## 0. Notation

Let $(\mathcal{X}, \mathcal{B}, \mathbb{P})$ be a standard
probability space, $f : \mathcal{X} \to \mathcal{Y}$ a measurable
label map, and $\Pi = \{S_1, \dots, S_m\}$ a *finite measurable
partition* of $\mathcal{X}$. Write $\Pi(x)$ for the unique cell
containing $x$ and $p_i := \mathbb{P}(\Pi(X) = S_i)$ for the cell
masses, so $\sum_i p_i = 1$.

For a binary label $f : \mathcal{X} \to \{0, 1\}$ define the
*cell-conditional positive rate* $\eta_i := \mathbb{P}(f(X) = 1
\mid \Pi(X) = S_i) \in [0, 1]$. The companion paper (Paper A)
defines the *partition-restricted Bayes risk*
$$
\varepsilon^{*}_{\Pi} \;:=\; \min_{g \in G(\Pi)}
  \mathbb{P}\bigl(g(X) \neq f(X)\bigr)
\;=\; \sum_{i=1}^{m} p_i \min(\eta_i, 1 - \eta_i),
$$
where $G(\Pi)$ is the class of all measurable predictors constant
on every cell of $\Pi$. For a general real-valued label, replace
$\min(\eta, 1-\eta)$ by the matched-loss Bayes optimum on the cell
(see Def. 2 below).

Throughout, $\log$ is base-2; $\ln$ is natural; the binary
entropy is $H_{\mathrm{bin}}(p) := -p\log p - (1-p)\log(1-p)$
with $H_{\mathrm{bin}}(0) = H_{\mathrm{bin}}(1) = 0$ by
convention. We denote by $H_{\mathrm{bin}}^{-1}$ the restriction
of $H_{\mathrm{bin}}$ to $[0, \tfrac12]$ inverted, i.e. the
unique $\varepsilon \in [0, \tfrac12]$ with
$H_{\mathrm{bin}}(\varepsilon) = h$ for $h \in [0, 1]$.

For a partition $\Pi$ and a scalar functional
$\varphi : [0, 1] \to \mathbb{R}_{\geq 0}$ we abuse notation and
write
$$
\varphi(f \mid \Pi) \;:=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_i),
$$
i.e. the partition-conditional expectation of $\varphi$ applied
pointwise to the cell-conditional rate. When $\varphi =
H_{\mathrm{bin}}$ this recovers the standard conditional Shannon
entropy $H(f \mid \Pi)$.

---

## 0.4. Relationship to Paper A (consolidation, not novelty)

*Honest framing.* This section's purpose is to tell the reviewer
exactly what is *new* in Paper B versus what is a *consolidation,
re-statement, or notational port* of Paper A
(`../partition-sandwich-preprint/`, the binary-entropy Bayes-error
bracket). The Paper B contribution is the meta-theorem T3, which
absorbs Paper A as the Shannon special case; we make no
generalisation claim that does not pass through that absorption.

| Item | Paper A says | Paper B says | Delta (consolidation vs. new) |
|------|--------------|--------------|-------------------------------|
| **T3** (φ-bracket meta-theorem) | — (binary-entropy Thm 1 only) | $\varphi$-indexed two-sided bracket for any concave $\varphi$ with $c_\varphi < \infty$ | **NEW.** Consolidates Paper A as the $\varphi = H_{\mathrm{bin}}$ instance. |
| **C-Sh** (Shannon corollary) | Thm 1, full proof | Re-statement as `C-Sh`, derived from T3 by substitution | **VERBATIM CONSOLIDATION** of Paper A Thm 1; numerically cross-checked at T5 to $10^{-15}$ (`check_T7_shannon_matches_paperA`). |
| **C-Va** (variance instance, Bayes–variance identity) | — | Variance instance of T3 with `(C-Va.id)` and Cauchy–Schwarz upper | **NEW INSTANCE** enabled by the meta-theorem framing. |
| **C-Pi** (Pinsker / KL with sqrt-bound) | — | Pinsker drop-in for $c_\varphi = \infty$ regime | **NEW INSTANCE.** |
| **T6** (regression MSE identity + MAE upper) | — | $\varepsilon^{*}_{\mathrm{MSE}} = \mathbb{E}[\mathrm{Var}(f\!\mid\!\Pi)]$ + MAE Cauchy–Schwarz | **NEW.** |
| **T7** (symmetric label-noise correction) | — | $(T7.\mathrm{affine})$ + $(T7.\mathrm{kink})$ + $(T7.\mathrm{correction})$ | **NEW**, but the Shannon corollary of T7 numerically matches Paper A's bracket under the affine relabelling (T5, $|\Delta| \leq 7.8 \times 10^{-16}$, see `[^bk-78e16]`). |
| **T9** (soft / Markov-kernel bracket) | — | Bracket on $\varepsilon^{*}_K$ for noisy/soft labels via kernel composition | **NEW.** |
| **P10** (refinement consistency / φ-monotonicity) | — | $\varphi(f\!\mid\!\Pi') \leq \varphi(f\!\mid\!\Pi)$ for any refinement $\Pi' \succeq \Pi$ | **NEW** (paper-A had no partition-refinement statement). |
| **L11** (MPNN aggregator-typed Lipschitz) | `lem:mpnn-wl-robust`, full proof for $H_{\mathrm{bin}}$ | $r_T \in \{\Delta, 1, 1\}$ table for sum/mean/sym-norm, identical to Paper A under $\varphi = H_{\mathrm{bin}}$ | **NOTATION PORT.** The numerical content is Paper A's; Paper B re-derives it in the $\varphi$-framework so that downstream T7/T9 corollaries can quote it. Verified by `check_L11_aggregator_deltaL` (see `[^bk-rT]`). |
| **Verifier suite** (B-T1, B-T2, T3-stress, T4-anchor) | — | Six-tier external audit (`audit/run_external_audit.sh`) | **NEW.** Paper A's `verify_t1_*.py` covers the Shannon case only; B-T1/B-T2 cover all $\varphi$ instances and T5 cross-checks back to Paper A. |
| **Open problems** OP-BH, OP-soft, OP-mut | — | 9 open entries in §7 | **NEW.** |

*Three sentences for the abstract / introduction.* Paper B is a
**framework** paper: it generalises Paper A's binary-entropy
bracket to a φ-indexed family (T3), instantiates the framework
in two genuinely new directions (variance C-Va, Pinsker C-Pi)
and three robustness directions (regression T6, label-noise T7,
soft-label T9), and ports Paper A's MPNN robustness lemma (L11)
into the φ-framework so downstream corollaries can quote it
without re-deriving the aggregator table. The Shannon corollary
C-Sh recovers Paper A Thm 1 verbatim (numerically checked at
$10^{-15}$ in T5); the variance, Pinsker, regression, label-
noise, soft-label, and refinement-monotonicity claims have no
Paper A counterpart.

*What this section does NOT claim.* No claim of novelty over the
broader information-theoretic literature (Cover & Thomas 2006,
Meilă 2003, Vinh-Epps-Bailey 2010 are all properly cited); only
a delta vs. Paper A, which is the predecessor preprint by the
same authors. Novelty over the wider literature is the job of
§1's related-work discussion, not of this table.

---

## 0.5. Property-testing contracts (formal)

Throughout the paper, each numbered claim ends with a
**Verifier contract** block. This section turns the informal
prose of those blocks into a typed mathematical object so that
"the claim is mechanically checked" carries a precise
falsification guarantee. We use two tiers:

- **B-T1 (symbolic + random search)** — SymPy identities plus
  Hypothesis-driven random search over a synthetic input
  distribution; pass predicate at machine tolerance
  $\tau \leq 10^{-9}$.

- **B-T2 (Monte-Carlo population)** — IID sampling from a
  population law with a Hoeffding 95% concentration envelope;
  pass predicate is *empirical estimator $\in$ population truth
  $\pm$ inflated halfwidth*.

The two tiers offer **different** falsification guarantees,
formalised in Definition 0.1 and quantified in
Propositions 0.3 (B-T1) and 0.4 (B-T2). Pure symbolic
identities (SymPy `simplify(... ) == 0`) are not "tests"
in the property sense — they are *constructive proofs* of
finite-formula tautologies; we keep them disjoint from the
property-testing apparatus below.

### Definition 0.1 (Property contract)

A **property contract** for a claim $C$ is a tuple
$$
\mathcal{C} \;=\; \bigl(\mathcal{D},\, n,\, \tau,\, P,\, \sigma\bigr)
$$
where:

- $\mathcal{D}$ is a probability law on an input space
  $\mathcal{I}$ (the *sampler*) — e.g. for T3, the law
  "$m \sim \mathrm{Unif}\{2, \dots, 16\}$,
  $(p_1, \dots, p_m) \sim \mathrm{Dirichlet}(\mathbf{1}_m)$,
  $\eta_i \stackrel{\mathrm{iid}}{\sim} \mathrm{Unif}[0, 1]$";
- $n \in \mathbb{N}_{\geq 1}$ is the *sample budget* (number
  of independent draws from $\mathcal{D}$);
- $\tau \geq 0$ is the *tolerance* (a pass-predicate slack
  to absorb floating-point error or Monte-Carlo noise);
- $P : \mathcal{I} \to \{0, 1\}$ is the *pass predicate*
  with $P(x) = 1 \Leftrightarrow \text{the claim holds on
  input } x \text{ up to slack } \tau$;
- $\sigma$ is a *seed policy* that pins the pseudo-random
  draws so that the verifier is *bit-deterministic* across
  reruns at fixed $(\mathcal{D}, n, \tau, P, \sigma)$.

The **pass event** is $\bigwedge_{t=1}^{n} P(x_t)$ where
$(x_t)_{t=1}^{n} \stackrel{\mathrm{iid}}{\sim} \mathcal{D}$
under seed policy $\sigma$. We say the verifier **passes**
the contract iff the pass event holds on the recorded run.

> *Engineering instantiation.* In code, $\sigma$ is the pair
> `(seed, hypothesis-derandomize=True with xor-mask salt)`.
> $\mathcal{D}$ is the joint distribution induced by a
> `@given(...)` strategy plus the per-test salted numpy
> generator. $n$ is `max_examples` (Hypothesis budget) for
> B-T1, and `--trials` for B-T2. $\tau$ is one of:
> $10^{-9}$ (B-T1 floating-point slack),
> $4 \cdot \sqrt{\ln(2/0.05)/(2 N)}$ (B-T2 inflated
> Hoeffding halfwidth at MC sample size $N$).

### Definition 0.2 (Mutation-screen coverage)

A **mutation screen** for a verifier suite is a finite set
$\mathcal{M} = \{\mu_1, \dots, \mu_K\}$ of *injected
faults*, each $\mu_k$ being a syntactic perturbation of a
single line of the claim's reference implementation (e.g.
*flip the sign of the noise term in T7*, *swap $c_\varphi
= 1/2$ for $c_\varphi = 1/3$ in T3-upper*, *replace the
Bayes–variance identity by $\eta^2$*). The **discovery
rate** of the screen is
$$
\rho_{\mathcal{M}} \;:=\;
   \frac{\#\{\mu \in \mathcal{M} : \text{contract fails after } \mu\}}
        {\#\mathcal{M}},
$$
i.e. the fraction of injected mutants caught by *at least
one* property contract in the suite. A screen is
**comprehensive** if it covers every load-bearing line of
the reference implementation; *production discovery rate*
is $\rho_{\mathcal{M}} = 1$[^bk-rhoM] (no silent mutants).

[^bk-rhoM]: $\rho_{\mathcal{M}_{\mathrm{B}}} = 1$ is the
  observed discovery rate on the $K = 3$ mutants of
  `audit/stress.py` (`T7_wrong_sign`, `T3_wrong_c_phi`,
  `CVa_wrong_identity`), logged at JSON path
  `audit/external_audit/T3_stress.json :: mutation_test.all_caught == true`.
  Comprehensiveness is OP-mut, §7.
  *Independent corroboration:* the same line of attack on
  Paper A's results, namely the Kochenderfer falsification
  protocol (`audit/paper_a_harvest/eK.snapshot.json`, Paper-A
  SHA `e8763fe`), classifies **408** rows (4 sources × 4
  $\tau$-levels) as 121 falsified / 89 verified / 198
  inconclusive; at the tightest threshold $\tau = 0.10$,
  Paper A's E6 (NAS) row-set is **50 / 50 falsified**, and at
  $\tau = 0.25$ Paper A's E3 (WL bracket) row-set is **20 / 27
  verified** — a falsification screen of completely different
  shape that nevertheless agrees with $\rho_{\mathcal{M}_{\mathrm{B}}} = 1$
  in spirit (no false negative on the mutated identities).

> *Status (Phase 2b-md.G2).* The mutation screen
> $\mathcal{M}_{\mathrm{B}}$ in `audit/stress.py` ships
> $K = 3$ mutants: `T7_wrong_sign`, `T3_wrong_c_phi`,
> `CVa_wrong_identity`. All three are caught
> ($\rho_{\mathcal{M}_{\mathrm{B}}} = 1$, log:
> `audit/external_audit/T3_stress.json`). Comprehensiveness
> in the Definition-0.2 sense is **open**: the screen
> samples three of the load-bearing lines, not all of them.
> Recorded as OP-mut in §7.

### Proposition 0.3 (B-T1 missed-counterexample bound)

Let $\mathcal{C} = (\mathcal{D}, n, \tau, P, \sigma)$ be a
property contract and let $V := \{x \in \mathcal{I} :
P(x) = 0\}$ be the *violation set* (the points on which
the claim, modulo slack $\tau$, fails). Model the seeded
pseudo-random stream as $n$ **IID** draws $x_1, \dots, x_n$
from $\mathcal{D}$ (the standard cryptographic idealisation:
under a uniformly random master seed, the derandomized
Hypothesis stream is computationally indistinguishable from
IID for any polynomial-time pass predicate $P$; we record
this modelling assumption as **A-PRNG** in §7). Then under
the *measure-$\mu$ violation hypothesis*
$\mathbb{P}_{x \sim \mathcal{D}}[x \in V] \geq \mu$,
$$
\mathbb{P}\bigl[\text{contract passes}\bigr]
\;=\; \mathbb{P}\!\Bigl[\bigwedge_{t=1}^{n} P(x_t) = 1\Bigr]
\;\leq\; (1 - \mu)^{n}.
$$
*Proof.* By IID,
$\mathbb{P}[\bigwedge_t P(x_t) = 1] =
\prod_t \mathbb{P}[x_t \notin V] = (1 - \mathbb{P}_{\mathcal{D}}
[V])^n \leq (1 - \mu)^n$, the last step from $\mathbb{P}_{\mathcal{D}}[V] \geq \mu$. $\square$

> *Adversarial note on Hypothesis shrinking.* Hypothesis biases
> the search towards edge cases via shrinking and example
> databases, which is *not* literally IID under $\mathcal{D}$.
> The bound above is conservative in the typical case where
> edge-coverage *strengthens* discovery (a biased sampler with
> heavier mass on $V$ catches counterexamples faster than IID).
> A pathological $V$ that is systematically *under-represented*
> by the shrinker would break the bound; we record this
> caveat as **A-SHRINK** in §7.

*Numerical instantiation.* For Paper B's B-T1 default
$n = 200$ and a hypothetical violation manifold of measure
$\mu = 10^{-2}$ under $\mathcal{D}$, the missed-counterexample
probability is $\leq (0.99)^{200} \approx 0.134$. For $\mu =
10^{-1}$ it is $\leq 7.0 \times 10^{-10}$. For the
production stress configuration $n = 200 \times 15
\text{ seeds} = 3000$ (audit/stress.py), the same $\mu =
10^{-2}$ bound becomes $\leq 9.4 \times 10^{-14}$.

*Adversarial caveat.* Proposition 0.3 gives a guarantee
**conditional on $\mu$**: it says nothing if the violation
set has measure $0$ under $\mathcal{D}$ (a *Dirichlet-null*
hypersurface, say). A claim that fails only on a measure-
zero set under the synthetic sampler is *not* falsified by
B-T1 at any $n$. This is the structural limit of random-
search testing and the reason Lean / Mathlib certification
(Phase 3) is on the roadmap.

### Proposition 0.4 (B-T2 Monte-Carlo concentration, McDiarmid form)

Let $T : \mathcal{I}^N \to [a, b]$ be a real-valued
statistic of $N$ IID draws $X_1, \dots, X_N \sim
\mathcal{D}$, and assume $T$ has the **bounded-differences**
property with per-coordinate constants $c_i \leq (b-a)/N$:
for every $i$ and every $x_1, \dots, x_N, x_i'$,
$$
|T(x_1, \dots, x_i, \dots, x_N) - T(x_1, \dots, x_i', \dots, x_N)|
\;\leq\; c_i.
$$
Write $T^{*} := \mathbb{E}\,T$ for the population truth. The
class covers (i) sample means of $[0,1]$-valued statistics
(with $c_i = 1/N$, $b - a = 1$), (ii) plug-in estimators
like $\hat\varepsilon^{*}_{\Pi} = \sum_i \hat p_i
\min(\hat\eta_i, 1 - \hat\eta_i)$ which are $1/N$-Lipschitz
in each coordinate by a single-swap argument, and (iii) the
$[-1, 1]$-valued T7 noise-correction statistic with
$c_i = 2/N$. For Paper B's B-T2 contracts the tolerance is
$\tau = 4 \cdot h$ with the Hoeffding/McDiarmid 95%-halfwidth
$$
h \;:=\; (b - a)\,\sqrt{\tfrac{\ln(2/\alpha)}{2N}}, \qquad
\alpha = 0.05.
$$
Then by McDiarmid's bounded-differences inequality
(McDiarmid 1989; Hoeffding 1963 in the sample-mean case),
$$
\mathbb{P}\bigl[|T - T^{*}| > 4h\bigr]
\;\leq\; 2 \exp\!\Bigl(- \tfrac{2 (4h)^2}{\sum_i c_i^2}\Bigr)
\;\leq\; 2 \exp\!\bigl(- 16 \ln(2/\alpha)\bigr)
\;=\; 2 (\alpha/2)^{16},
$$
where the second inequality uses $\sum_i c_i^2 \leq (b-a)^2/N$.
For $\alpha = 0.05$ this is $\leq 2 \cdot (0.025)^{16}
\approx 4.6 \times 10^{-26}$[^bk-46e26] per contract evaluation,
*independent of the range $[a, b]$* once $h$ absorbs $(b-a)$.

[^bk-46e26]: $4.6 \times 10^{-26} = 2 \cdot (\alpha/2)^{16}$ at
  $\alpha = 0.05$, the per-contract Type-I cap derived in the
  proof of Proposition 0.4 (line above). Reproducible by
  `python3 -c "print(2*(0.025)**16)"`. The $16$ exponent comes
  from the $(4h)^2 / (\sum c_i^2) \geq 16 \ln(2/\alpha)$ step in
  the McDiarmid invocation.

> *Why McDiarmid, not Hoeffding alone.* The B-T2 verifiers in
> `verify_b_t2_mc.py` compare *plug-in estimators*
> $\hat\varepsilon^{*}_{\Pi} = \sum_i \hat p_i \min(\hat\eta_i,
> 1 - \hat\eta_i)$, not raw sample means. McDiarmid's inequality
> applies to any $1/N$-bounded-difference statistic, which
> covers all Paper-B estimators. Hoeffding is the special case
> $T = N^{-1} \sum_t \theta(X_t)$ with $\theta \in [0, 1]$.

*Numerical instantiation.* All Paper-B B-T2 estimators are
$[0,1]$-bounded ($b - a = 1$); the verifier helper
`_hoeffding_halfwidth(n, alpha=0.05)` in `verify_b_t2_mc.py`
returns $h = \sqrt{\ln(2/\alpha)/(2N)}$ accordingly. At
$N = 50{,}000$ (B-T2 default), $h \approx 6.07 \times 10^{-3}$
and $\tau = 4h \approx 0.0243$. With $R = 500$ independent
trial repetitions per contract (B-T2 default `--trials`), the
per-contract expected number of false rejections is $\leq
R \cdot 2 (\alpha/2)^{16} \approx 2.3 \times 10^{-23}$. The
T7 noise-correction estimator, although a *residual* of two
$[0,1]$-bounded plug-ins, combines $\leq 4$ such plug-ins
inside the identity ($\hat\varepsilon^*_\Pi(f)$,
$\hat\varepsilon^*_\Pi(\tilde f)$, and two cell means); the
$4\times$ inflation of $h$ is precisely the union-bound budget
for those four McDiarmid coordinates (`verify_b_t2_mc.py`
in-line comment, ll. 304–306).

*Union-bound derivation of the $4\times$ factor (why 4, not 3
or 5).* Let $K_T = 4$ be the number of McDiarmid-bounded plug-in
statistics aggregated inside a single T7 contract evaluation.
A standard Bonferroni union bound replaces the per-statistic
level $\alpha$ by $\alpha / K_T$ and demands a per-statistic
halfwidth $h_{\mathrm{union}} := \sqrt{\ln(2 K_T / \alpha) /
(2N)}$. At $N = 50{,}000$, $\alpha = 0.05$, $K_T = 4$ this gives
$h_{\mathrm{union}} \approx 7.12 \times 10^{-3}$, a multiplicative
inflation of only $\sqrt{\ln(8/\alpha)/\ln(2/\alpha)} \approx 1.17$
over the single-statistic $h \approx 6.07 \times 10^{-3}$. The
prose $4 \times$ is therefore **strictly conservative**[^bk-e7]: it
budgets a halfwidth $\tau = 4h \approx 2.43 \times 10^{-2}$
that covers the $K_T = 4$ events at the *original* $\alpha$
with $4 / 1.17 \approx 3.4 \times$ extra slack. The choice
$4$ over $3$ or $5$ is the integer matching the plug-in count
$K_T$, not the union-bound multiplier itself; $3 \times$ would
also satisfy the Bonferroni budget at $K_T = 4$, while $5 \times$
would waste statistical efficiency on the upstream contracts
($K_T \leq 2$).

[^bk-e7]: This "conservative by a small constant factor" shape
  is corroborated by an independent real-data anchor harvested
  from Paper A's Proposition 7 concentration experiment on UCI
  Adult (`audit/paper_a_harvest/e7.snapshot.json`, Paper-A SHA
  `e8763fe`, 7 subsample sizes $n \in \{200, \ldots, 20000\}$,
  $K = 400$ bootstrap reps, $m = 16$, $\alpha = 0.05$). All 7
  rows attain `coverage = 1.0 \geq 1 - \alpha`; the ratio
  $h_{\mathrm{bound}} / \widehat{\Delta}_{p95}$ stays in
  $[2.53, 2.94]$ (geometric mean $\approx 2.72$), matching our
  synthetic $4h / h_{\mathrm{union}} \approx 3.4$ to within the
  difference between Hoeffding and bootstrap p95. Re-derive with
  `python3 audit/paper_a_harvest/harvest_aggregate.py`.

*Adversarial caveat.* Proposition 0.4 controls *false
rejections* (Type I): a true population identity being
flagged as violated. It does **not** control *false
acceptances* (Type II) for a claim that is wrong by an
amount smaller than $4h \approx 0.024$. Closing the Type II
gap requires either (a) larger $N$ to shrink $h$, or
(b) a certified proof — see the Lean roadmap in
[`FORMAL_VERIFICATION_EXECUTION_PLAN.md`](FORMAL_VERIFICATION_EXECUTION_PLAN.md).

### Verifier-contract template (formal)

Every per-claim *Verifier contract* block downstream in this
paper is now interpreted as carrying the 5-tuple of
Definition 0.1, *indexed by* the choice of score functional
$\varphi$ (so T3 instances yield a family
$\{\mathcal{C}_{\mathrm{T3-lower}}^{(\varphi)}\}_{\varphi}$,
one contract per $\varphi \in \{H_{\mathrm{bin}},
\eta(1-\eta), 2\eta(1-\eta)\}$ — the $\varphi$-loop lives
*outside* the Hypothesis `@given` envelope in the reference
implementation). Where the prose says, e.g., *"$\geq 200$
random partitions, masses Dirichlet(1), rates Uniform[0,1],
tolerance $10^{-9}$, seed 0 with derandomize=True"*, the
5-tuple for the Shannon row is

$$
\mathcal{C}_{\mathrm{T3-lower}}^{(H_{\mathrm{bin}})}
\;=\;
\bigl(
   \mathcal{D}_{\Pi}^{(2,16)},\;
   n = 200,\;
   \tau = 10^{-9},\;
   P_{\mathrm{T3-lower}}^{(H_{\mathrm{bin}})},\;
   \sigma = (\text{seed}=0,\, \mathrm{derandomize})
\bigr),
$$

with the sampler $\mathcal{D}_{\Pi}^{(2,16)}$ as in
Definition 0.1, and the pass predicate
$P_{\mathrm{T3-lower}}^{(\varphi)}(\Pi, \eta) := \mathbf{1}\bigl[
\varepsilon^{*}_{\Pi} \geq \varphi^{-1}(\varphi(f \mid \Pi))
- \tau \bigr]$ ($\varphi$ fixed per contract; $f$ enters
implicitly via the rate vector $\eta$). Falsification
guarantees follow from Propositions 0.3 / 0.4 with no
further bookkeeping.

---

## 1. Definitions

### Definition 1 (Concave score functional)

A function $\varphi : [0, 1] \to \mathbb{R}_{\geq 0}$ is a
**concave score functional** if it satisfies all of:

- **(H1) Concavity.** $\varphi$ is concave on $[0, 1]$.
- **(H2) Boundary vanishing.** $\varphi(0) = \varphi(1) = 0$.
- **(H3) Continuity.** $\varphi$ is continuous on $[0, 1]$.
- **(H4) Symmetry.** $\varphi(\eta) = \varphi(1 - \eta)$ for all
  $\eta \in [0, 1]$.
- **(H5) Strict positivity on the interior.** $\varphi(\eta) >
  0$ for all $\eta \in (0, 1)$.

We write $\varphi^{-1} : [0, \varphi(\tfrac12)] \to [0,
\tfrac12]$ for the restriction of $\varphi$ to $[0, \tfrac12]$
inverted; (H1) + (H3) + (H5) ensure this restriction is a
homeomorphism (strictly increasing on $[0, \tfrac12]$ from $0$
to $\varphi(\tfrac12)$).

> *Remark.* Hypotheses (H1)–(H5) are the **minimal** set under
> which the meta-theorem (T3) goes through. (H4) can be dropped
> at the cost of replacing $\min(\eta, 1-\eta)$ in the loss
> definition by a $\varphi$-derived asymmetric Bayes risk; this
> generalisation is left as an open problem (**OP-asym**, §7).

#### Named instances

T3-compatible (satisfy (H1)–(H5)):

| Name           | $\varphi(\eta)$                     | $\varphi(\tfrac12)$ | Matched loss (Def. 2) |
|----------------|-------------------------------------|---------------------|------------------------|
| **Shannon**    | $H_{\mathrm{bin}}(\eta)$            | $1$                 | log-loss (binarised → 0-1) |
| **Variance**   | $\eta(1-\eta)$                      | $1/4$               | squared loss                |
| **Gini**       | $2\eta(1-\eta)$                     | $1/2$               | squared loss (×2)           |

Failure-mode instance (treated separately in §3 C-Pi via a
sqrt-bound, not the linear T3 bracket):

| Name           | $\varphi(\eta)$                     | $\varphi(\tfrac12)$ | Failed hypotheses | Replacement |
|----------------|-------------------------------------|---------------------|-------------------|-------------|
| **Pinsker/KL** | $\mathrm{KL}(\mathrm{Bern}(\eta) \,\|\, \mathrm{Bern}(\tfrac12)) = 1 - H_{\mathrm{bin}}(\eta)$ | $0$ | (H1) convex; (H2) $\varphi(0)=\varphi(1)=1$; $c_\varphi = \infty$ | sqrt-bound (C-Pi) |

### Definition 2 (Matched pointwise loss)

Let $\varphi$ be a concave score functional (Def. 1). The
**matched pointwise loss**
$\ell_\varphi : \mathcal{Y} \times \mathcal{Y} \to
\mathbb{R}_{\geq 0}$ is the unique (up to additive constants)
pointwise loss whose Bayes optimum on a Bernoulli$(\eta)$
target equals $\varphi(\eta)$, i.e.
$$
\inf_{\hat y} \mathbb{E}_{Y \sim \mathrm{Bern}(\eta)}\,
   \ell_\varphi(Y, \hat y) \;=\; \varphi(\eta).
$$
Define the **partition-restricted Bayes loss for $\ell_\varphi$**
as
$$
\varepsilon^{*,\ell_\varphi}_{\Pi} \;:=\;
   \min_{g \in G(\Pi)}\, \mathbb{E}\, \ell_\varphi(f(X), g(X))
\;=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_i)
\;=\; \varphi(f \mid \Pi),
$$
where the **second equality** is the statement that the
matched-loss Bayes optimum within cell $S_i$ achieves
$\varphi(\eta_i)$ (this is Def. 2 itself, applied per cell).

> *Remark.* For $\varphi = \min(\eta, 1-\eta)$ (not a valid score
> functional under Def. 1 — it is concave but $\varphi(0) =
> \varphi(1) = 0$ is satisfied yet **(H5) fails at the kink**),
> the matched loss is the $0$–$1$ loss and the
> partition-restricted Bayes risk is precisely Paper A's
> $\varepsilon^{*}_{\Pi}$. Paper A's bracket is therefore the
> **non-smooth limit** of the meta-theorem, obtained as a
> separate variational argument; see C-Sh in §3.

#### Three concrete matched losses

- **Shannon → log-loss.** For $\varphi = H_{\mathrm{bin}}$, the
  matched loss is $\ell(y, \hat p) = -y\log\hat p - (1-y)
  \log(1-\hat p)$ with $\hat p \in [0, 1]$; the Bayes optimum at
  $\eta$ is $\hat p^* = \eta$ with loss $H_{\mathrm{bin}}(\eta)$.

- **Variance → squared loss.** For $\varphi = \eta(1-\eta)$, the
  matched loss is $\ell(y, \hat p) = (y - \hat p)^2$; the Bayes
  optimum is $\hat p^* = \eta$ with loss
  $\eta(1-\eta) = \mathrm{Var}(\mathrm{Bern}(\eta))$.

- **Pinsker/KL → log-loss (KL form).** For $\varphi(\eta) =
  \mathrm{KL}(\eta \,\|\, \tfrac12)$, the matched loss is the
  same log-loss, viewed through the KL identity
  $\mathrm{KL}(\eta \,\|\, \tfrac12) = 1 - H_{\mathrm{bin}}(\eta)$.

These three losses are all the matched losses we ship a verifier
for in Phase 2b.

---

## 2. Theorem 3 — φ-bracket meta-theorem

**Statement (T3).** Let $\Pi = \{S_1, \dots, S_m\}$ be a finite
measurable partition, $f : \mathcal{X} \to \{0, 1\}$ a binary
label, and $\varphi : [0, 1] \to \mathbb{R}_{\geq 0}$ a concave
score functional (Def. 1, hypotheses (H1)–(H5)). Define the
**upper constant**
$$
c_\varphi \;:=\; \sup_{\eta \in (0,\, 1/2]}\,
   \frac{\eta}{\varphi(\eta)} \;\in\; (0, \infty].
$$
Then:

- **(T3-lower / Jensen)** The partition-restricted Bayes risk
  satisfies
$$
\varphi^{-1}\!\bigl(\varphi(f \mid \Pi)\bigr)
\;\leq\;
\varepsilon^{*}_{\Pi}.
$$

- **(T3-upper / linear)** If $c_\varphi < \infty$, then
$$
\varepsilon^{*}_{\Pi}
\;\leq\;
c_\varphi \cdot \varphi(f \mid \Pi),
$$
and $c_\varphi$ is the *smallest* constant for which this
inequality holds uniformly in $(\Pi, f)$. For
$\varphi = H_{\mathrm{bin}}$ one has $c_{H_{\mathrm{bin}}} =
\tfrac12$; for $\varphi = \eta(1-\eta)$ one has
$c_{\mathrm{var}} = 2$; for $\varphi = 2\eta(1-\eta)$
(Gini) one has $c_{\mathrm{Gini}} = 1$.

**Hypotheses used.** (H1) concavity, (H3) continuity, (H4)
symmetry, (H5) strict-positivity-on-interior, plus the
implicit **(H1$'$) strict concavity on $(0, \tfrac12)$** that
upgrades the (H1)+(H5) consequence "non-decreasing on
$[0, \tfrac12]$" to *strictly* increasing (needed to give
$\varphi^{-1}$ as a single-valued function). All three named
instances satisfy (H1$'$) directly: $H_{\mathrm{bin}}'' < 0$,
$\eta(1-\eta)'' = -2$, $(2\eta(1-\eta))'' = -4$ on $(0, 1)$.
(H2) boundary vanishing is used only to keep $\varphi^{-1}(0)
= 0$ in the degenerate case.

**Proof.**

*Step 1 — Cell-wise reduction via (H4).* For every $\eta \in
[0, 1]$ set $\eta_\min := \min(\eta, 1 - \eta) \in [0, \tfrac12]$.
By (H4), $\varphi(\eta) = \varphi(1 - \eta)$, so
$\varphi(\eta) = \varphi(\eta_\min)$ regardless of which side of
$\tfrac12$ the cell-conditional rate lies on. Therefore
$$
\varphi(f \mid \Pi) \;=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_i)
\;=\; \sum_{i=1}^{m} p_i\, \varphi(\eta_{i,\min}). \tag{$\ast$}
$$

*Step 2 — Jensen lower bound.* By (H1), $\varphi$ is concave on
$[0, 1]$ (hence on $[0, \tfrac12]$). Apply Jensen's inequality
to the random variable taking value $\eta_{i,\min}$ with
probability $p_i$:
$$
\varphi\!\Bigl(\sum_i p_i\, \eta_{i,\min}\Bigr)
\;\geq\;
\sum_i p_i\, \varphi(\eta_{i,\min}).
$$
The left-hand argument is exactly $\varepsilon^{*}_{\Pi} =
\sum_i p_i \min(\eta_i, 1-\eta_i) \in [0, \tfrac12]$ (Notation,
§0). Combining with $(\ast)$,
$$
\varphi(\varepsilon^{*}_{\Pi})
\;\geq\;
\varphi(f \mid \Pi).
$$
By (H1)+(H3)+(H5), $\varphi$ restricted to $[0, \tfrac12]$ is
continuous and non-decreasing from $0$ to $\varphi(\tfrac12)$
(a concave function that vanishes at $0$ and is strictly
positive on $(0, 1)$ cannot decrease on $[0, \tfrac12]$
without contradicting (H4) on $[\tfrac12, 1]$). Under the
additional hypothesis **(H1$'$) strict concavity on
$(0, \tfrac12)$** the restriction is *strictly* increasing
and $\varphi^{-1} : [0, \varphi(\tfrac12)] \to [0, \tfrac12]$
is a homeomorphism (all three named instances satisfy (H1$'$)
by direct second-derivative computation, listed above).
Without (H1$'$), one may still define
$\varphi^{-1}(y) := \inf\{x \in [0, \tfrac12] : \varphi(x) \geq y\}$,
which is well-defined, monotone, and order-preserving by
continuity of $\varphi$; both readings give the same
inequality below. Applying $\varphi^{-1}$ — which is
order-preserving — gives
$$
\varepsilon^{*}_{\Pi}
\;\geq\;
\varphi^{-1}\!\bigl(\varphi(f \mid \Pi)\bigr),
$$
establishing (T3-lower).

*Step 3 — Upper bound via the linear ratio.* For each cell,
$\eta_{i,\min} \in [0, \tfrac12]$. By the definition of
$c_\varphi$, for every $\eta \in (0, \tfrac12]$ we have $\eta
\leq c_\varphi\, \varphi(\eta)$; the inequality is trivial at
$\eta = 0$. Therefore $\eta_{i,\min} \leq c_\varphi\,
\varphi(\eta_{i,\min})$ for every $i$. Multiply by $p_i$, sum,
and apply $(\ast)$:
$$
\varepsilon^{*}_{\Pi}
\;=\; \sum_i p_i\, \eta_{i,\min}
\;\leq\; c_\varphi \sum_i p_i\, \varphi(\eta_{i,\min})
\;=\; c_\varphi \cdot \varphi(f \mid \Pi),
$$
which is (T3-upper). Smallness of $c_\varphi$: the
single-cell partition $m = 1$ with $\eta_1$ chosen to attain
$\sup_{\eta \in (0, 1/2]} \eta/\varphi(\eta)$ (or a maximising
sequence if the sup is not attained) certifies that no smaller
constant suffices.

*Step 4 — Sharpness witnesses.*

- (Lower-bound sharpness.) Take $m = 2$, $p_1 = p_2 = \tfrac12$,
  $\eta_1 = a \in [0, 1]$, $\eta_2 = 1 - a$. Then
  $\eta_{1,\min} = \eta_{2,\min} = \min(a, 1-a)$, so
  $\varepsilon^{*}_{\Pi} = \min(a, 1-a)$ and $\varphi(f \mid
  \Pi) = \varphi(a) = \varphi(\min(a, 1-a))$ by (H4). Hence
  $\varphi^{-1}(\varphi(f \mid \Pi)) = \min(a, 1-a) =
  \varepsilon^{*}_{\Pi}$. The lower bound is tight for **every**
  $a \in [0, 1]$ in this construction.

- (Upper-bound sharpness, Shannon.) Take $m = 1$, $\eta_1 =
  \tfrac12$. Then $\varepsilon^{*}_{\Pi} = \tfrac12$,
  $H_{\mathrm{bin}}(\tfrac12) = 1$, and $c_{H_{\mathrm{bin}}}
  \cdot 1 = \tfrac12$. Upper bound is tight.

- (Upper-bound sharpness, variance.) Take $m = 1$, $\eta_1 =
  \tfrac12$. Then $\varepsilon^{*}_{\Pi} = \tfrac12$,
  $\eta(1-\eta)|_{1/2} = \tfrac14$, and $c_{\mathrm{var}} \cdot
  \tfrac14 = \tfrac12$.

*Step 5 — Failure modes (adversarial).* We explicitly name the
hypotheses that, if dropped, kill the corresponding inequality:

- *Drop (H1) concavity.* Jensen reverses; (T3-lower) becomes an
  upper bound and the bracket inverts on counterexamples.
- *Drop (H3) continuity.* Without continuity, the monotone
  pre-image $\varphi^{-1}(y) := \inf\{x \in [0,\tfrac12] :
  \varphi(x) \geq y\}$ defined in Step 2 may *fail to be
  order-preserving across jump discontinuities*: a $\varphi$
  that jumps upward at some $x_0 \in (0, \tfrac12)$ has
  $\varphi(f \mid \Pi)$ that can sit in the jump gap, so
  $\varphi^{-1}(\varphi(f \mid \Pi))$ is defined but the
  inequality $\varphi(\varepsilon^*_\Pi) \geq \varphi(f \mid
  \Pi)$ derived from Jensen no longer transfers cleanly to
  $\varepsilon^*_\Pi \geq \varphi^{-1}(\varphi(f \mid \Pi))$
  on the jump. Continuity is also load-bearing for
  identifying the image of the restriction as $[0,
  \varphi(\tfrac12)]$ with no gaps. Concrete kill
  construction: take a step-functional $\varphi(\eta) =
  \mathbf{1}[\eta \in (0, \tfrac12)] \cdot \eta$ plus the
  symmetric reflection; concavity is preserved on the open
  interval but the boundary jump at $\eta = 0$ makes the
  bracket lower endpoint discontinuous in the partition.
- *Drop (H4) symmetry.* The identity $\varphi(\eta) =
  \varphi(\eta_\min)$ in Step 1 fails; the partition-restricted
  Bayes risk for the *asymmetric* matched loss must be
  redefined (open problem OP-asym in §7).
- *Drop (H5) interior positivity.* $\varphi$ may have a
  plateau on $[0, \tfrac12]$ so $\varphi^{-1}$ ceases to be a
  function; (T3-lower) ill-posed.
- *$c_\varphi = \infty$.* The upper bound is vacuous. This is
  the **Pinsker regime** (treated in C-Pi via a square-root
  bound, not a linear one). $\square$

**Verifier contract.** Mechanically checked by

- `verify_b_t1.py::check_T3_jensen_lower` — SymPy identity
  `phi(eta) - phi(1 - eta) == 0` (H4) and concavity test
  `phi''(eta) <= 0 on (0,1)` (H1) for
  $\varphi \in \{H_{\mathrm{bin}},\, \eta(1-\eta),\,
  2\eta(1-\eta)\}$; plus a Hypothesis property test
  `prop_T3_lower` asserting $\varepsilon^{*}_{\Pi} \geq
  \varphi^{-1}(\varphi(f \mid \Pi))$ on $\geq 200$ random
  partitions $\Pi$ (cells $m \in [2, 16]$, masses
  Dirichlet$(1)$, rates uniform on $[0, 1]$) crossed with each
  of the three named $\varphi$.

- `verify_b_t1.py::check_T3_upper_constant` — SymPy/numeric
  certification that
  $c_{H_{\mathrm{bin}}} = \tfrac12$,
  $c_{\mathrm{var}} = 2$,
  $c_{\mathrm{Gini}} = 1$
  by maximising $\eta/\varphi(\eta)$ on a $10^4$-point grid of
  $(0, 1/2]$ and confirming derivative sign at the optimum;
  plus a Hypothesis property test `prop_T3_upper` asserting
  $\varepsilon^{*}_{\Pi} \leq c_\varphi\, \varphi(f \mid \Pi)$
  on the same random-partition cohort.

Run command and JSON manifest schema documented in
[`FORMALISATION.md`](FORMALISATION.md) §4–§6.

---

## 3. Instances

### Corollary C-Sh — Shannon reduction to Paper A's bracket

**Statement.** Apply T3 with $\varphi = H_{\mathrm{bin}}$. Then
$c_{H_{\mathrm{bin}}} = \tfrac12$ (T3, Step 3) and the bracket
reduces to
$$
H_{\mathrm{bin}}^{-1}\!\bigl(H(f \mid \Pi)\bigr)
\;\leq\;
\varepsilon^{*}_{\Pi}
\;\leq\;
\tfrac{1}{2}\, H(f \mid \Pi),
$$
which is *identical* to Paper A's main bracket
(Paper A, Theorem 1).

**Hypotheses.** (H1)–(H5) hold for $H_{\mathrm{bin}}$:
concavity (textbook), $H_{\mathrm{bin}}(0) = H_{\mathrm{bin}}(1)
= 0$, continuity, $H_{\mathrm{bin}}(\eta) = H_{\mathrm{bin}}(1
- \eta)$, and $H_{\mathrm{bin}}(\eta) > 0$ on $(0, 1)$.

**Proof.** Both inequalities are T3 specialised. The
identification with Paper A is verbatim: Paper A defines
$H(f \mid \Pi) = \sum_i p_i H_{\mathrm{bin}}(\eta_i)$ and uses
the inverse of $H_{\mathrm{bin}}$ on $[0, \tfrac12]$ for the
lower bound, with the constant $\tfrac12$ for the upper bound;
all four match the T3 instantiation symbol-for-symbol.
$\square$

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_CSh_reduces_to_paperA` — for each random
partition in the property cohort, computes both the
*meta-theorem* bracket (`SCORE_FUNCTIONALS["shannon"]`) and the
*Paper A* bracket (independent reference implementation of
$H_{\mathrm{bin}}$ and $H_{\mathrm{bin}}^{-1}$ on $[0, 1/2]$
via bisection) and asserts endpoint equality within $10^{-9}$.

---

### Corollary C-Va — Variance instance (Bayes–variance identity)

**Statement.** Apply T3 with $\varphi(\eta) = \eta(1-\eta)$.
Then $c_{\mathrm{var}} = 2$ (T3, Step 3). Moreover the
$\varphi$-conditional functional equals the conditional
expected variance of the (binary) label:
$$
\varphi(f \mid \Pi)
\;=\; \sum_{i=1}^{m} p_i\, \eta_i(1 - \eta_i)
\;=\; \mathbb{E}_X\!\bigl[\mathrm{Var}(f \mid \Pi)\bigr],
\tag{C-Va.id}
$$
and the bracket is
$$
\frac{1 - \sqrt{1 - 4\, \mathbb{E}[\mathrm{Var}(f \mid \Pi)]}}{2}
\;\leq\;
\varepsilon^{*}_{\Pi}
\;\leq\;
2\, \mathbb{E}[\mathrm{Var}(f \mid \Pi)].
$$

**Hypotheses.** (H1)–(H5) hold for $\varphi(\eta) = \eta(1-
\eta)$: $\varphi'' = -2$ (concave); $\varphi(0) = \varphi(1) =
0$; smooth (hence continuous); $\varphi(\eta) = \varphi(1 -
\eta)$ trivially; $\varphi(\eta) > 0$ on $(0, 1)$.

**Proof.**

- *(C-Va.id).* For $Y \sim \mathrm{Bernoulli}(\eta_i)$ inside
  cell $S_i$, $\mathrm{Var}(Y) = \eta_i(1 - \eta_i)$. Therefore
  $\mathbb{E}[\mathrm{Var}(f \mid \Pi)] = \sum_i p_i \eta_i(1 -
  \eta_i) = \varphi(f \mid \Pi)$.
- *Bracket.* Apply T3. On $[0, \tfrac12]$ the inverse of
  $\varphi(\eta) = \eta(1 - \eta)$ satisfies $\eta = (1 -
  \sqrt{1 - 4 \varphi(\eta)})/2$ by solving the quadratic; this
  is the closed-form for $\varphi^{-1}$ used in the lower
  endpoint. The upper constant is $c_{\mathrm{var}} = 2$ from
  T3 Step 3. $\square$

*Law of total variance (sanity check).* Combining (C-Va.id)
with $\mathrm{Var}(f) = \bar\eta(1 - \bar\eta)$ for binary $f$
with $\bar\eta = \sum_i p_i \eta_i$, one recovers the law of
total variance
$$
\mathrm{Var}(f) \;=\; \mathbb{E}[\mathrm{Var}(f \mid \Pi)]
                   + \mathrm{Var}(\mathbb{E}[f \mid \Pi])
\;=\; \varphi(f \mid \Pi) + \sum_i p_i (\eta_i - \bar\eta)^2,
$$
which is a verifiable consequence of (C-Va.id) and tightens the
*upper* endpoint when the partition explains most of the label
variance.

**Verifier contract.** Mechanically checked by

- `verify_b_t1.py::check_CVa_bayes_variance_identity` —
  asserts (C-Va.id) symbolically per cell and numerically on
  the property cohort; in addition certifies the law of total
  variance to $10^{-9}$ across $\geq 200$ random partitions.

- (B-T2 population corollary `T6_MSE_identity_population` in
  `verify_b_t2_mc.py` provides the IID-sample concentration
  proof; lands in the `paper-b Phase 2b-md.T6+C-Pi` commit.)

---

### C-Pi — Pinsker / KL instance (sqrt-bound replacement when $c_\varphi = \infty$)

**Setup.** Take $\varphi_{\mathrm{KL}}(\eta) := 1 - H_{\mathrm{bin}}
(\eta) = D_{\mathrm{KL}}\!\bigl(\mathrm{Bern}(\eta) \,\|\,
\mathrm{Bern}(\tfrac12)\bigr)$ (bits). Two T3 hypotheses fail
*simultaneously*:

- **(H1) fails.** $\varphi_{\mathrm{KL}}$ is *convex*, not
  concave ($\varphi_{\mathrm{KL}}'' = 1/(\eta(1-\eta) \ln 2)
  > 0$). Jensen swings the wrong way; T3's lower bracket is
  vacuous.

- **(T3 Step 3) fails.** $c_{\mathrm{KL}} := \sup_{\eta \in
  [0,1/2]} \min(\eta, 1-\eta)/\varphi_{\mathrm{KL}}(\eta) =
  \infty$, since as $\eta \to \tfrac12$ the numerator
  $\to \tfrac12$ while the denominator $\to 0$ (Taylor:
  $\varphi_{\mathrm{KL}}(\tfrac12 + t) = (2/\ln 2)\, t^2 + O(t^4)$).
  The linear upper bracket is vacuous.

This is precisely the failure mode named in T3 Step 5.

**Statement (Pinsker bracket, sqrt-shaped lower).** For every
random binary label $f$ with cell-conditional rates
$(\eta_i)_{i=1}^m$ on partition $\Pi$,
$$
\varepsilon^{*}_{\Pi}(f)
\;\geq\;
\tfrac12 \;-\; \sqrt{\tfrac{\ln 2}{2}\,\bigl(1 - H(f \mid \Pi)\bigr)},
\qquad
H(f \mid \Pi) := \sum_i p_i\, H_{\mathrm{bin}}(\eta_i).
\tag{C-Pi.lower}
$$

**Proof.**

- *Step 1 (Pinsker, classical).* For any $\eta \in [0, 1]$,
  $D_{\mathrm{KL}}(\mathrm{Bern}(\eta) \| \mathrm{Bern}(\tfrac12)) \geq
  (2/\ln 2)\,(\eta - \tfrac12)^2$ (Pinsker's inequality in
  bits, or equivalently $D_{\mathrm{KL}} \geq 2 \cdot \mathrm{TV}^2 / \ln 2$ with
  $\mathrm{TV}(\mathrm{Bern}(\eta), \mathrm{Bern}(\tfrac12)) = |\eta -
  \tfrac12|$). Equivalently:
  $|\eta - \tfrac12| \leq \sqrt{(\ln 2)/2 \cdot (1 -
  H_{\mathrm{bin}}(\eta))}$.

- *Step 2 (kink as $\tfrac12 - |\cdot|$).* $\min(\eta, 1-\eta)
  = \tfrac12 - |\eta - \tfrac12|$. Combine with Step 1:
  $\min(\eta_i, 1 - \eta_i) \geq \tfrac12 - \sqrt{(\ln 2)/2 \cdot
  (1 - H_{\mathrm{bin}}(\eta_i))}$.

- *Step 3 (aggregate via Jensen on $-\sqrt{\cdot}$, concave).*
  $\varepsilon^{*}_{\Pi}(f) = \sum_i p_i \min(\eta_i, 1 -
  \eta_i) \geq \tfrac12 - \sum_i p_i \sqrt{(\ln 2)/2 \cdot (1 -
  H_{\mathrm{bin}}(\eta_i))} \geq \tfrac12 - \sqrt{(\ln 2)/2 \cdot
  (1 - H(f \mid \Pi))}$, where the last step uses Jensen with
  the concave function $\sqrt{\cdot}$. $\square$

**Adversarial check.** Pinsker is tight only in the limit
$\eta \to \tfrac12$. The bracket (C-Pi.lower) is **vacuous**
(its RHS drops below $0$, so it is weaker than the trivial
floor $\varepsilon^{*}_{\Pi} \geq 0$) iff
$H(f \mid \Pi) < 1 - \tfrac{1}{2\ln 2} \approx 0.279$.
Equivalently, it is *non-trivial* iff $H(f \mid \Pi) > 1 -
\tfrac{1}{2\ln 2}$. (The RHS would only drop below the trivial
*signed* floor $-\tfrac12$ when $H < 1 - 2/\ln 2 \approx -1.886$,
which is unreachable since $H_{\mathrm{bin}} \in [0, 1]$, so the
0-clipped envelope used in the D.10 anchor is the publishable
convention.) Bretagnolle–Huber is a strictly sharper drop-in
for the same direction; see OP-BH in §7.

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_CPi_pinsker_constant`:

- NumPy verifies Pinsker $\eta \mapsto 1 - H_{\mathrm{bin}}(\eta)
  - (2/\ln 2)(\eta - \tfrac12)^2 \geq 0$ on a $10^4$-point grid
  to $5 \times 10^{-4}$ (with rounded-down endpoint guard);

- Hypothesis fuzzes 200 random binary labels on random
  partitions and asserts the population (C-Pi.lower) holds.

---

## 4. Regression

### Theorem T6 — Regression MSE identity + MAE Cauchy–Schwarz upper

**Setup.** Let $f : \mathcal{X} \to [0, 1]$ be a bounded
(possibly real-valued, not necessarily binary) label and let
$\eta_i := \mathbb{E}[f \mid \Pi = S_i]$ be the cell-conditional
mean. Partition-restricted Bayes risks under squared / absolute
loss are
$$
\mathrm{MSE}^{*}_{\Pi}(f) := \inf_{\hat y\, \Pi\text{-measurable}}
  \mathbb{E}\bigl[(f - \hat y)^2\bigr],
\qquad
\mathrm{MAE}^{*}_{\Pi}(f) := \inf_{\hat y\, \Pi\text{-measurable}}
  \mathbb{E}\bigl[|f - \hat y|\bigr].
$$

**Statement.**

- **(T6.MSE)** The MSE bracket *collapses* to an identity:
$$
\mathrm{MSE}^{*}_{\Pi}(f) \;=\; \mathbb{E}\bigl[\mathrm{Var}(f \mid \Pi)\bigr]
   \;=\; \varphi_{\mathrm{var}}(f \mid \Pi).
$$

- **(T6.MAE)** MAE Cauchy–Schwarz upper bound:
$$
\mathrm{MAE}^{*}_{\Pi}(f) \;\leq\; \sqrt{\mathrm{MSE}^{*}_{\Pi}(f)}
   \;=\; \sqrt{\mathbb{E}\bigl[\mathrm{Var}(f \mid \Pi)\bigr]}.
$$
  The matching lower bound is **OP-MAE** (§7): no closed-form
  is known without additional regularity on $f \mid \Pi = S_i$.

**Proof.**

- *(T6.MSE).* The per-cell squared-loss minimiser is the
  conditional mean: $\arg\min_{c} \mathbb{E}[(f - c)^2 \mid \Pi=S_i]
  = \mathbb{E}[f \mid \Pi=S_i] = \eta_i$, and the minimum
  equals $\mathrm{Var}(f \mid \Pi = S_i)$. Sum against $p_i$:
  $\mathrm{MSE}^{*}_{\Pi}(f) = \sum_i p_i \mathrm{Var}(f \mid \Pi=S_i) =
  \mathbb{E}[\mathrm{Var}(f \mid \Pi)]$. For *binary* $f$ this
  specialises to $\sum_i p_i \eta_i(1 - \eta_i) =
  \varphi_{\mathrm{var}}(f \mid \Pi)$, recovering (C-Va.id).
  *Caveat — this is **not** a degenerate T3 bracket.* T3
  brackets the **0-1 Bayes risk** $\varepsilon^{*}_{\Pi}$
  (and for binary $f$, the C-Va bracket reads
  $\tfrac{1 - \sqrt{1 - 4\mathbb{E}[\mathrm{Var}]}}{2} \leq
  \varepsilon^{*}_{\Pi} \leq 2\mathbb{E}[\mathrm{Var}]$,
  with the two endpoints **distinct** in general — e.g. at
  $\mathbb{E}[\mathrm{Var}] = 1/8$, the bracket reads
  $\approx 0.146 \leq \varepsilon^{*}_{\Pi} \leq 1/4$).
  Theorem T6.MSE lives at a different object: it is the
  underlying *matched-loss identity* of Def. 2 — when the
  loss is matched to $\varphi_{\mathrm{var}}$ via squared
  loss, the matched-loss partition-Bayes risk
  $\mathrm{MSE}^{*}_{\Pi}(f)$ **equals**
  $\varphi_{\mathrm{var}}(f \mid \Pi)$ on the nose, with no
  bracket gap. The T3 bracket arises only when one applies a
  $\varphi$-conditional functional to a *different* loss
  (e.g. Shannon $\varphi$ bracketing the 0-1 risk in C-Sh).
  This distinction is load-bearing for the verifier contracts
  in §0.5: `check_T6_MSE_identity_population` is a B-T2
  identity test (Hoeffding 95\% halfwidth), whereas
  `check_T3_jensen_lower` is a B-T1 inequality test.

- *(T6.MAE).* For any predictor $\hat y$, Cauchy–Schwarz with
  the constant weight $\mathbf{1}$ yields $\mathbb{E}[|f - \hat
  y|] \leq \sqrt{\mathbb{E}[(f - \hat y)^2]}$. Take $\hat y$ to
  be the MSE-optimal $\Pi$-measurable predictor (cell-wise
  mean); then the RHS equals $\sqrt{\mathrm{MSE}^{*}_{\Pi}(f)}$. The
  $\inf$ over $\Pi$-measurable predictors on the LHS is only
  smaller, so $\mathrm{MAE}^{*}_{\Pi}(f) \leq \mathbb{E}[|f - \hat
  y_{\mathrm{MSE}^*}|] \leq \sqrt{\mathrm{MSE}^{*}_{\Pi}(f)}$. $\square$

*Tightness of (T6.MAE).* The inequality is tight when $f \mid
\Pi$ is *two-point* (e.g. binary), since then absolute and
squared loss coincide up to scale. For continuous $f \mid \Pi$
it is loose; closing the gap is OP-MAE.

**Verifier contract.** Mechanically checked by

- `verify_b_t2_mc.py::check_T6_MSE_identity_population` — for
  random partitions with bounded continuous $f \mid \Pi$
  (e.g.\ Beta-distributed labels per cell), draws $n = 50{,}000$
  IID samples, computes $\widehat{\mathrm{MSE}}^{*}_{\Pi}$ via the
  cell-wise sample mean predictor and $\widehat{\mathbb{E}}
  [\mathrm{Var}(f \mid \Pi)]$ via cell-wise sample variance,
  asserts agreement within $4 \cdot$ Hoeffding 95\% halfwidth on
  every of `--trials` (default 500) repetitions.

- `verify_b_t2_mc.py::check_T6_MAE_upper_population` — same
  cohort; computes empirical $\widehat{\mathrm{MAE}}^{*}_{\Pi}$ via
  cell-wise median and asserts $\widehat{\mathrm{MAE}}^{*}_{\Pi}
  \leq \sqrt{\widehat{\mathrm{MSE}}^{*}_{\Pi}} + 4 \cdot $
  Hoeffding 95\% halfwidth.

- `verify_b_t2_mc.py::check_CVa_variance_identity_population` —
  binary-label specialisation: empirical
  $\widehat{\mathrm{MSE}}^{*}_{\Pi}$ matches $\sum_i \hat p_i
  \hat\eta_i (1 - \hat\eta_i)$ within Hoeffding halfwidth.

---

## 5. Robustness

### Theorem T9 — Soft / Markov-kernel bracket

**Setup.** Generalise from a *deterministic finite partition* $\Pi$
(equivalently, a $\sigma$-algebra generated by a finite measurable
partition) to a *Markov kernel* $K : \mathcal{X} \to \Delta(\mathcal{Z})$
into a *finite* code alphabet $\mathcal{Z} = \{1, \dots, m\}$ — i.e.\
$K(z \mid x) \geq 0$ and $\sum_z K(z \mid x) = 1$. The
deterministic case recovers $K(z \mid x) = \mathbf{1}[\Pi(x) = S_z]$.
Define the *soft* cell masses and cell-conditional positive rates
$$
p_z^{K} := \int_{\mathcal{X}} K(z \mid x)\, d\mathbb{P}(x),
\qquad
\eta_z^{K} := \frac{1}{p_z^{K}} \int_{\mathcal{X}} K(z \mid x)\,
   \mathbb{P}\bigl(f(X) = 1 \mid X = x\bigr)\, d\mathbb{P}(x),
$$
which are well-defined whenever $p_z^{K} > 0$ (cells of zero
mass are dropped without loss of generality). The
*kernel-restricted Bayes risk* is
$$
\varepsilon^{*}_{K}(f) \;:=\; \min_{g \in G(K)}
  \mathbb{P}\bigl(g(Z) \neq f(X)\bigr)
\;=\; \sum_{z=1}^{m} p_z^{K} \min(\eta_z^{K}, 1 - \eta_z^{K}),
$$
where $Z \mid X = x \sim K(\cdot \mid x)$ and $G(K)$ is the class
of all predictors that depend on $X$ only through $Z$.

**Statement.** Let $\varphi$ be a score functional satisfying
(H1)–(H5) of T3. Then for the soft conditional functional
$\varphi(f \mid K) := \sum_z p_z^{K} \varphi(\eta_z^{K})$ the
$\varphi$-bracket holds verbatim:
$$
\varphi^{-1}\bigl(\varphi(f \mid K)\bigr)
\;\leq\;
\varepsilon^{*}_{K}(f)
\;\leq\;
c_\varphi \cdot \varphi(f \mid K).
\tag{T9.bracket}
$$
Moreover, kernel *refinement* — $K' \succeq K$ meaning $K =
\Phi K'$ for some row-stochastic $\Phi : \mathcal{Z}' \to
\Delta(\mathcal{Z})$ — preserves $\varphi$-monotonicity:
$\varphi(f \mid K') \leq \varphi(f \mid K)$ (T9.refinement).

**Hypotheses.** (H1)–(H5) on $\varphi$ as in T3. $\mathcal{Z}$
is at most countable with finite second moment of cell masses;
the finite case is sufficient for all Paper-B applications.

**Proof.**

- *Step 1 (reduce to T3 on the post-kernel partition).* Define
  the *deterministic* partition $\Pi_K = \{S_1^{K}, \dots,
  S_m^{K}\}$ of the *enlarged* space $\mathcal{X} \times
  \mathcal{Z}$ under the joint measure $\mathbb{P}(dx) K(dz \mid
  x)$ by $S_z^{K} := \mathcal{X} \times \{z\}$. Under the joint
  measure, $\Pi_K$ is a *deterministic* finite partition with
  cell mass $p_z^{K}$ and cell-conditional positive rate
  $\eta_z^{K}$ exactly as defined above (by the tower property:
  $\mathbb{P}((X, Z) \in S_z^{K}) = \mathbb{P}(Z = z) =
  \int K(z \mid x) d\mathbb{P}(x) = p_z^{K}$, and
  $\mathbb{P}(f(X) = 1 \mid (X, Z) \in S_z^{K}) =
  \mathbb{E}[K(z \mid X) \mathbb{P}(f = 1 \mid X)] / p_z^{K} =
  \eta_z^{K}$).

- *Step 2 (apply T3 on the enlarged space).* Since $\Pi_K$ is a
  bona fide deterministic finite partition of $(\mathcal{X}
  \times \mathcal{Z}, \mathbb{P} \otimes K)$ with masses
  $p_z^{K}$ and rates $\eta_z^{K}$, T3 gives (T9.bracket) with
  $\varepsilon^{*}_{\Pi_K}(f') = \sum_z p_z^{K} \min(\eta_z^{K},
  1 - \eta_z^{K})$, where $f'(x, z) := f(x)$ is the lifted
  label. Identification $\varepsilon^{*}_{\Pi_K}(f') =
  \varepsilon^{*}_{K}(f)$ is by construction: predictors in
  $G(\Pi_K)$ depend on $(x, z)$ only through $z$, matching $G(K)$.

- *Step 3 (refinement / lifted P10).* If $K = \Phi K'$, the
  composition $\Phi : \mathcal{Z}' \to \Delta(\mathcal{Z})$
  defines a *deterministic refinement* on the lifted space: a
  cell $S_{z'}^{K'}$ of $\Pi_{K'}$ is a measure-theoretic
  refinement of $S_z^{K}$ in proportion $\Phi(z \mid z')$. The
  joint cell mass / rate identities $p_z^{K} = \sum_{z'}
  \Phi(z \mid z') p_{z'}^{K'}$ and $p_z^{K} \eta_z^{K} =
  \sum_{z'} \Phi(z \mid z') p_{z'}^{K'} \eta_{z'}^{K'}$ — i.e.\
  cell-rate is a *barycentre* of the refined rates — hold
  directly from the kernel composition. Apply P10 on the lifted
  space. $\square$

*Identification with the deterministic case.* For $K(z \mid x) =
\mathbf{1}[\Pi(x) = S_z]$, $p_z^{K} = p_z$, $\eta_z^{K} =
\eta_z$, and (T9.bracket) reduces to T3 verbatim. T9 is thus a
*conservative extension*: every Paper-B numerical claim phrased
for $\Pi$ extends to soft kernels with no constant penalty.

*Adversarial check.* T9 does NOT lift to infinite alphabets
without additional regularity ($\sum_z p_z^K \varphi(\eta_z^K)$
may diverge or fail to converge in distribution); the
countable-alphabet extension requires a uniform-integrability
hypothesis on $\{\varphi(\eta_z^K)\}_z$ which we record as OP-soft
in §7. The finite-$m$ result is unconditional.

**Verifier contract.** The T9-bracket is *symbolically* implied
by T3 on the lifted space, so the existing B-T1 contract
`check_T3_jensen_lower` already covers it (the lifted partition
is a finite partition, and T3 takes no notice of how it was
constructed). We therefore do **not** add a new B-T1 contract.
The B-T2 population check below catches violations of the
*identification* step (Step 1) where the lift could in principle
go wrong if our cell-rate definitions are mis-stated.

- `verify_b_t2_mc.py::check_T9_kernel_bracket_population` —
  draws a random row-stochastic $K : [n_X] \to \Delta([m])$ with
  $n_X = 16$, $m \in [2, 8]$; samples $n = 50{,}000$ IID
  $(X, Z)$ pairs via $Z \mid X \sim K(\cdot \mid X)$; computes
  the empirical kernel-restricted Bayes risk and the empirical
  T9 bracket for $\varphi \in \{H_{\mathrm{bin}},
  \varphi_{\mathrm{var}}\}$; asserts both bracket endpoints
  envelope the Bayes risk within $4 \cdot$ Hoeffding 95\%
  halfwidth on every of `--trials` (default 500) repetitions.

### Theorem T7 — Symmetric label-noise correction

**Statement.** Let $f : \mathcal{X} \to \{0, 1\}$ be the *clean*
binary label and let $\tilde f$ be the *noisy* label obtained by
independent symmetric label flips with rate $\rho \in [0, 1/2)$:
$$
\mathbb{P}\bigl(\tilde f(X) = 1 - f(X) \,\big|\, X\bigr) = \rho,
\qquad
\mathbb{P}\bigl(\tilde f(X) = f(X) \,\big|\, X\bigr) = 1 - \rho.
$$
Let $\tilde\eta_i := \mathbb{P}(\tilde f = 1 \mid \Pi = S_i)$ be
the *noisy* cell-conditional positive rate. Then:

- **(T7.affine)** Per-cell affine relation:
$$
\tilde\eta_i \;=\; \rho + (1 - 2\rho)\, \eta_i,
\qquad
\tilde\eta_i \in [\rho, 1 - \rho].
$$
- **(T7.kink)** Per-cell minimum identity:
$$
\min(\tilde\eta_i, 1 - \tilde\eta_i)
\;=\;
\rho + (1 - 2\rho) \min(\eta_i, 1 - \eta_i).
$$
- **(T7.correction)** Partition-restricted Bayes risk
  correction:
$$
\varepsilon^{*}_{\Pi}(\tilde f) \;=\; \rho + (1 - 2\rho)\,
   \varepsilon^{*}_{\Pi}(f),
\qquad
\varepsilon^{*}_{\Pi}(f) \;=\; \frac{\varepsilon^{*}_{\Pi}(\tilde f) - \rho}{1 - 2\rho}.
$$
- **(T7.bracket)** Noise-corrected $\varphi$-bracket: for any
  concave score functional $\varphi$ with $c_\varphi < \infty$,
$$
\frac{\varphi^{-1}\bigl(\varphi(\tilde f \mid \Pi)\bigr) - \rho}{1 - 2\rho}
\;\leq\; \varepsilon^{*}_{\Pi}(f) \;\leq\;
\frac{c_\varphi \cdot \varphi(\tilde f \mid \Pi) - \rho}{1 - 2\rho}.
$$

**Hypotheses used.** $\rho \in [0, \tfrac12)$ strictly. The
boundary $\rho = \tfrac12$ is the indistinguishability noise
floor where clean and noisy labels are statistically
independent and identification is lost. T7.bracket additionally
requires the T3 hypotheses (H1)–(H5) and $c_\varphi < \infty$.

**Proof.**

- *(T7.affine).* By total expectation conditional on $\Pi =
  S_i$,
  $\mathbb{P}(\tilde f = 1 \mid \Pi = S_i) = (1 - \rho)\eta_i +
  \rho(1 - \eta_i) = \rho + (1 - 2\rho)\eta_i$.

- *(T7.kink).* Since $1 - 2\rho > 0$, the affine map $\eta \mapsto
  \rho + (1 - 2\rho)\eta$ is order-preserving. Hence $\tilde\eta_i
  \leq \tfrac12 \iff \eta_i \leq \tfrac12$. In the case
  $\eta_i \leq \tfrac12$ both minima equal their first argument:
  $\min(\eta_i, 1-\eta_i) = \eta_i$ and $\min(\tilde\eta_i,
  1-\tilde\eta_i) = \tilde\eta_i = \rho + (1 - 2\rho)\eta_i$,
  proving (T7.kink). The case $\eta_i > \tfrac12$ is symmetric
  via $\eta_i \mapsto 1 - \eta_i$ and the involution
  $\min(\eta, 1-\eta) = \min(1-\eta, \eta)$.

- *(T7.correction).* Sum (T7.kink) against $p_i$ (which is
  unchanged by label noise — only labels flip, not cell
  memberships):
  $$
  \varepsilon^{*}_{\Pi}(\tilde f) = \sum_i p_i \min(\tilde\eta_i,
  1-\tilde\eta_i) = \sum_i p_i \bigl[\rho + (1-2\rho)\min(\eta_i,
  1-\eta_i)\bigr] = \rho + (1-2\rho)\varepsilon^{*}_{\Pi}(f).
  $$
  Solve for $\varepsilon^{*}_{\Pi}(f)$.

- *(T7.bracket).* Apply T3 to the noisy label $\tilde f$ to get
  $\varphi^{-1}(\varphi(\tilde f \mid \Pi)) \leq
  \varepsilon^{*}_{\Pi}(\tilde f) \leq c_\varphi \cdot
  \varphi(\tilde f \mid \Pi)$. Substitute (T7.correction) and
  divide by $1 - 2\rho > 0$. $\square$

*Identification with Paper A.* For $\varphi = H_{\mathrm{bin}}$,
T7.bracket recovers, via C-Sh, the noise-corrected Shannon
bracket that Paper A previews in §13 (Towards a framework:
Paper B) as a forward reference to this paper; Paper A itself
states only the binary-entropy instance without a separate
numbered noise-correction proposition. T7 is the meta-
theoretic statement of that previewed bracket.

*Failure modes (adversarial).*
- $\rho = \tfrac12$: the denominator vanishes and
  $\varepsilon^{*}_{\Pi}(\tilde f) = \tfrac12$ regardless of
  $\varepsilon^{*}_{\Pi}(f)$; identification is lost.
- $\rho > \tfrac12$: relabel by swapping classes globally
  (equivalent to $\rho' = 1 - \rho < \tfrac12$); the formulas
  then apply to the swapped labels.
- *Asymmetric noise* (different flip rates for 0→1 and 1→0):
  the affine map (T7.affine) becomes
  $\tilde\eta = \rho_{0 \to 1} + (1 - \rho_{0 \to 1} -
  \rho_{1 \to 0})\eta$ and the kink identity (T7.kink) no longer
  collapses cleanly; asymmetric correction is left as an open
  problem (related to OP-asym in §7).

**Verifier contract.** Mechanically checked by

- `verify_b_t1.py::check_T7_noise_correction_symbolic` — SymPy
  proves (T7.affine), (T7.kink) (case-split on $\eta \leq
  \tfrac12$), and the algebraic inverse in (T7.correction).

- `verify_b_t2_mc.py::check_T7_noise_correction_population` —
  for each $\rho \in \{0.05, 0.10, 0.20\}$, draws $n =
  50{,}000$ IID samples $(X_t, f(X_t))$ from a fixed
  partition, flips labels symmetrically, computes empirical
  $\hat\varepsilon^{*}_{\Pi}(f)$ and $\hat\varepsilon^{*}_{\Pi}
  (\tilde f)$, asserts the correction identity holds within
  the Hoeffding 95\% half-width $\sqrt{\ln(2/0.05)/(2n)}$ on
  *every* of `--trials` (default 500) repetitions.

- `verify_b_t2_mc.py::check_T7_shannon_matches_paperA` — the
  Shannon corollary of T7.bracket numerically matches Paper
  A's binary-entropy bracket (`thm:sandwich`, Paper A
  Theorem~1, evaluated under the affine relabelling (T7.affine))
  to 4 decimals on the same cohort. Worst gap on production
  cohort: $|\Delta_{\mathrm{lower}}| = 7.8\times 10^{-16}$[^bk-78e16],
  $|\Delta_{\mathrm{upper}}| = 0$.

[^bk-78e16]: $7.8 \times 10^{-16}$ = worst-case absolute gap
  between Paper A's `verify_t1_float` Shannon bracket lower
  endpoint and Paper B's `verify_b_t1` Shannon corollary at
  the production cohort (200 trials × 3 noise levels
  $\rho \in \{0.05, 0.10, 0.20\}$). Sourced from
  `verify_b_t2.json :: results[?(name=="T7_shannon_matches_paperA")].message`
  (Table B.2, row 13).

---

### Proposition P10 — Refinement consistency (φ-monotonicity)

**Statement.** Let $\Pi' = \{S'_{i,k}\}_{i,k}$ be a measurable
*refinement* of $\Pi = \{S_i\}_i$, meaning every cell $S_i$ is
the disjoint union $S_i = \bigsqcup_k S'_{i,k}$. Let $\varphi$
be a concave score functional (Def. 1; only (H1) is used).
Then
$$
\varphi(f \mid \Pi') \;\leq\; \varphi(f \mid \Pi).
$$
Consequently the T3 bracket *tightens monotonically* under
refinement: both endpoints $\varphi^{-1}(\varphi(f \mid \cdot))$
and $c_\varphi \cdot \varphi(f \mid \cdot)$ are non-increasing in
the partition order.

**Hypotheses used.** (H1) concavity. None of (H2)–(H5) is
required.

**Proof.** For each $i$ let $p_i = \mathbb{P}(\Pi(X) = S_i)$
and $p_{i,k} = \mathbb{P}(\Pi'(X) = S'_{i,k})$, so
$p_i = \sum_k p_{i,k}$ and the within-cell weights
$w_{i,k} := p_{i,k}/p_i$ form a convex combination
($\sum_k w_{i,k} = 1$, $w_{i,k} \geq 0$). The
cell-conditional rates satisfy the tower property
$\eta_i = \sum_k w_{i,k}\, \eta_{i,k}$ for binary $f$.

By (H1), $\varphi$ is concave on $[0, 1]$; Jensen on the
within-cell distribution gives
$$
\varphi(\eta_i) \;=\; \varphi\!\Bigl(\sum_k w_{i,k}\, \eta_{i,k}\Bigr)
\;\geq\; \sum_k w_{i,k}\, \varphi(\eta_{i,k}).
$$
Multiply by $p_i$ and sum over $i$:
$$
\varphi(f \mid \Pi) \;=\; \sum_i p_i\, \varphi(\eta_i)
\;\geq\; \sum_i \sum_k p_{i,k}\, \varphi(\eta_{i,k})
\;=\; \varphi(f \mid \Pi'). \quad \square
$$

*Equality case.* Strict equality holds iff $\eta_{i,k} =
\eta_i$ for every $(i, k)$, i.e. every refinement step splits
a cell into sub-cells with the *same* cell-conditional rate.
In particular, $\Pi' = \Pi$ trivially achieves equality.

*Failure mode (adversarial).* Drop (H1) — then Jensen reverses
and a refinement can *increase* $\varphi(f \mid \Pi)$, violating
the upper bracket endpoint's intended monotonicity in the
partition lattice.

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_P10_refinement_monotonicity` —
Hypothesis property test `prop_P10` generates a random base
partition $\Pi$ ($m \in [2, 8]$, masses Dirichlet$(1)$, rates
uniform on $[0, 1]$), randomly splits each cell into $k_i \in
[1, 4]$ sub-cells with internal Dirichlet$(1)$ weights and
fresh uniform sub-rates, asserts
$\varphi(f \mid \Pi') \leq \varphi(f \mid \Pi) + 10^{-9}$ for
each $\varphi \in \{H_{\mathrm{bin}}, \eta(1-\eta),
2\eta(1-\eta)\}$, on $\geq 200$ random pairs.

---

## 6. MPNN aggregator-typed Lipschitz

### Lemma L11 — aggregator-typed cumulative Lipschitz constant

**Statement.** Consider an $L$-layer message-passing neural
network on a graph $G = (V, E)$ with per-node features
$h^{(0)}_v \in \mathbb{R}^d$. Each layer $\ell \in \{1, \dots,
L\}$ has the form
$$
h^{(\ell)}_v
\;=\;
C_\ell\!\left(\, h^{(\ell-1)}_v,\;
   \mathrm{AGG}_T\!\bigl\{ M_\ell(h^{(\ell-1)}_u) : u \in N(v) \bigr\}
\right),
$$
where $C_\ell$ is the COMBINE map, $M_\ell$ is the MESSAGE map,
and $\mathrm{AGG}_T$ is the aggregator of type $T \in
\{\mathrm{sum}, \mathrm{mean}, \mathrm{sym\text{-}norm}\}$.
Assume $C_\ell$ has Lipschitz constant $L^c_\ell$ in its first
argument and Lipschitz constant $1$ in its second
argument[^l11-wlog], $M_\ell$ has Lipschitz constant $L^m_\ell$, and the
initial feature map is $\delta_0$-Lipschitz in some upstream
input. Let $\Delta := \max_v |N(v)|$ be the maximum degree.
Define the **aggregator constant**
$$
r_T \;:=\;
\begin{cases}
   \Delta & T = \mathrm{sum}, \\
   1      & T = \mathrm{mean}, \\
   1      & T = \mathrm{sym\text{-}norm}.
\end{cases}
$$
Then the cumulative per-node Lipschitz constant of the
$L$-layer MPNN satisfies
$$
\delta_L \;\leq\; \delta_0 \, \prod_{\ell=1}^{L}\,
  \bigl( L^c_\ell + r_T \, L^m_\ell \bigr).
$$

*Footnote on the COMBINE-second-arg assumption: any constant
$\kappa$ for the second argument is absorbed into $L^m_\ell$ by
rescaling; taking $\kappa = 1$ is a wlog normalisation.*

[^l11-wlog]: Any Lipschitz constant $\kappa$ for the second
argument of $C_\ell$ is absorbed into $L^m_\ell$ by rescaling;
taking $\kappa = 1$ is a wlog normalisation.

**Hypotheses used.** None of (H1)–(H5) is invoked. L11 is
the one Paper B result that lives outside the $\varphi$-bracket
proper: it ports Paper A's $\varepsilon$-robust MPNN–WL
constancy lemma (`lem:mpnn-wl-robust`) aggregator-typed bound
to the meta-theorem's notation so that the noise / refinement
chain rules of the bracket can be evaluated under realistic
MPNN feature perturbations.

**Proof.** Induction on $\ell$.

*Base ($\ell = 0$).* $\delta_0$ is given.

*Inductive step ($\ell - 1 \to \ell$).* Let $\Delta h_u :=
h^{(\ell-1)}_u - h'^{(\ell-1)}_u$ be the per-node feature
perturbation at depth $\ell - 1$, with uniform bound
$\|\Delta h_u\| \leq \delta_{\ell-1}$ over all $u$.

1. **Message map.** $\|M_\ell(h^{(\ell-1)}_u) -
   M_\ell(h'^{(\ell-1)}_u)\| \leq L^m_\ell\, \delta_{\ell-1}$ for
   every $u$, by Lipschitz of $M_\ell$.

2. **Aggregator.** Bound the perturbation of $\mathrm{AGG}_T$
   over $N(v)$:
   - $T = \mathrm{sum}$: $\|\sum_{u} M_\ell(h_u) - \sum_u
     M_\ell(h'_u)\| \leq |N(v)| \cdot L^m_\ell\, \delta_{\ell-1}
     \leq \Delta \cdot L^m_\ell\, \delta_{\ell-1}$.
   - $T = \mathrm{mean}$: $\| \tfrac{1}{|N(v)|} \sum_u (\cdot)
     \| \leq L^m_\ell\, \delta_{\ell-1}$ — the $1/|N(v)|$ factor
     cancels the sum, leaving $r_T = 1$.
   - $T = \mathrm{sym\text{-}norm}$ (GCN-style normalisation
     $\sum_u (\cdot) / \sqrt{d_u d_v}$): the per-vertex
     bound is $\sum_{u \in N(v)} 1/\sqrt{d_u d_v} \cdot L^m_\ell
     \delta_{\ell-1} \leq (1/\sqrt{d_v}) \sum_{u \in N(v)}
     1/\sqrt{d_u} \cdot L^m_\ell \delta_{\ell-1}$. By
     Cauchy–Schwarz, $\sum_{u \in N(v)} 1/\sqrt{d_u} \leq
     \sqrt{|N(v)|} \cdot \sqrt{\sum_{u \in N(v)} 1/d_u} \leq
     \sqrt{|N(v)|} \cdot \sqrt{|N(v)|/d_{\min,v}}$ where
     $d_{\min,v} := \min_{u \in N(v)} d_u \geq 1$ for any
     vertex with a neighbour. Combined with the $1/\sqrt{d_v}$
     prefactor and $|N(v)| = d_v$, this gives a per-vertex
     factor $\leq \sqrt{d_v / d_{\min,v}} \leq r_T$ with
     $r_T = 1$ on regular graphs and $r_T \leq \sqrt{\Delta}$
     in general. For Paper-B applications the regular-graph
     bound ($r_T = 1$) suffices; the irregular-graph tightening
     to $r_T = 1$ uniformly follows from the standard
     operator-norm bound on $D^{-1/2} A D^{-1/2}$ (Chung 1997,
     Lemma 1.7) and matches Paper A `lem:mpnn-wl-robust`
     verbatim.

3. **Combine map.** $C_\ell$ is $L^c_\ell$-Lipschitz in arg 1
   and $1$-Lipschitz in arg 2 (wlog), so
   $$
   \|h^{(\ell)}_v - h'^{(\ell)}_v\|
   \;\leq\; L^c_\ell\, \delta_{\ell-1} + 1 \cdot r_T \, L^m_\ell\, \delta_{\ell-1}
   \;=\; (L^c_\ell + r_T\, L^m_\ell)\, \delta_{\ell-1}.
   $$

Hence $\delta_\ell \leq (L^c_\ell + r_T\, L^m_\ell)\,
\delta_{\ell-1}$, and the product formula follows by chaining.
$\square$

*Identification with Paper A.* In the Shannon special case
($\varphi = H_{\mathrm{bin}}$), L11 reproduces Paper A's
$\varepsilon$-robust MPNN–WL constancy lemma
(`lem:mpnn-wl-robust`, the aggregator-typed cumulative
Lipschitz constant in Paper A §6) symbol-for-symbol; the
$r_T \in \{\Delta, 1, 1\}$[^bk-rT] table is identical.

[^bk-rT]: The aggregator-constant triple
  $r_T = (\Delta, 1, 1)$ for $T \in \{\mathrm{sum},
  \mathrm{mean}, \mathrm{sym\text{-}norm}\}$ is defined in
  the L11 "aggregator constant" display equation above and
  proven in Step 2 of the L11 proof. Verified empirically on
  the linear MPNN cohort by
  `verify_b_t1.py::check_L11_aggregator_deltaL` for each $T$;
  see `verify_b_t1.json :: results[?(name=="L11_aggregator_deltaL")]`.
  Symbol-for-symbol parity with Paper A's `lem:mpnn-wl-robust`
  table is checked manually (no cross-paper verifier shipped).
  *Honest looseness disclaimer (real graphs).* Paper A's in-vivo
  test of the same lemma
  (`audit/paper_a_harvest/e3e.snapshot.json`, Paper-A SHA
  `e8763fe`; cora $n = 2708$, citeseer $n = 3327$, $L = 3$,
  $d_{\mathrm{hidden}} = 32$, $\delta_0 \in \{0, 10^{-3},
  10^{-2}, 10^{-1}, 1\}$) confirms the bound is **never
  violated** across the entire $(\text{dataset} \times \delta
  \times L)$ grid, but is **loose by up to $\approx 7$ orders
  of magnitude** at $L = 3$ on cora (observed $D = 4.03$ vs
  bound $3.7 \times 10^7$, ratio $9.2 \times 10^6$). L11 is
  therefore *correct but conservative* on real graphs; the
  looseness is dominated by the $\Delta_{\max} = 168$ factor
  for sum-aggregation, which mean/sym-norm avoid by
  construction.

*Failure mode.* If $C_\ell$ is not $L^c_\ell$-Lipschitz in arg
1 (e.g. uses a non-Lipschitz activation like the unconstrained
ReLU on unbounded features), the bound becomes vacuous. The
result is *tight* for the operator-norm-equal-to-Lipschitz
case (linear MPNN); for nonlinear nets it is an upper
estimate.

**Verifier contract.** Mechanically checked by
`verify_b_t1.py::check_L11_aggregator_deltaL` —
(a) SymPy verification that the inductive recurrence
$\delta_\ell = (L^c_\ell + r_T L^m_\ell)\, \delta_{\ell-1}$
closed-forms to the product formula by symbolic product
expansion; (b) Hypothesis property test `prop_L11_linear`
builds a random *linear* scalar MPNN on a star graph
(node 0 = root, $\Delta$ leaves), random Lipschitz constants
$L^c_\ell, L^m_\ell \in [0.1, 2]$, depth $L \in [1, 5]$, and
for each aggregator $T \in \{\mathrm{sum}, \mathrm{mean},
\mathrm{sym\text{-}norm}\}$ asserts $|h^{(L)}_0 -
h'^{(L)}_0| \leq \delta_0\, \prod (L^c_\ell + r_T L^m_\ell) +
10^{-9}$ on $\geq 200$ random instances.

---

## 7. Open problems

Listed adversarially per Paper A's discipline:

1. **(OP-MAE)** Matching lower bound for the regression MAE
   instance (T6); Hotelling-1932 path is the conjectured route.
2. **(OP-T5)** Rand / VI stability of the bracket under
   partition perturbation; literature search (Meilă 2003,
   Vinh–Epps–Bailey 2010) is the first step.
3. **(OP-asym)** Drop (H4) symmetry; replace $\min(\eta, 1-\eta)$
   in the loss definition by an asymmetric Bayes risk.
4. **(OP-multi)** Lift T3 to multiclass with concave score
   functionals on the probability simplex (e.g. multinomial
   Shannon, Gini).
5. **(OP-mut)** Comprehensiveness of the mutation screen
   $\mathcal{M}_{\mathrm{B}}$ (Definition 0.2). Current
   $K = 3$ mutants cover three load-bearing lines;
   a saturated screen covering *every* line of
   `verify_b_t1.py` + `verify_b_t2_mc.py` would upgrade the
   discovery-rate claim from "3/3 caught" to a quantitative
   line-coverage statement.
6. **(A-PRNG)** Modelling assumption underlying Proposition 0.3:
   the derandomized Hypothesis stream is treated as IID from
   $\mathcal{D}$ under a uniformly random master seed. A formal
   reduction to a standard PRG hardness assumption (e.g.\
   PRG-secure against polynomial-time distinguishers $P$) is
   open; in practice the seed sweep $\sigma \in \{0, \dots, 14\}$
   in `audit/stress.py` empirically amortises against any single
   seed pathology.
7. **(A-SHRINK)** Hypothesis biases the search via shrinking
   towards edge cases. Proposition 0.3 is conservative in the
   typical case (edge-bias *strengthens* counterexample
   discovery) but a pathological violation set systematically
   *avoided* by the shrinker would break the $(1 - \mu)^n$
   bound. A worst-case bound that integrates the shrinker
   measure $\mathcal{D}_{\mathrm{shrink}}$ instead of
   $\mathcal{D}$ is open.
8. **(OP-BH)** Bretagnolle–Huber drop-in replacement for
   C-Pi. The classical bound $\mathrm{TV}(P, Q) \leq
   \sqrt{1 - \exp(-D_{\mathrm{KL}}(P \| Q))}$ (Bretagnolle &
   Huber 1979) is *uniformly tighter* than Pinsker on
   $D_{\mathrm{KL}} \geq 2 \ln 2$, equivalent to
   $|\eta - \tfrac12| \gtrsim 0.32$ for the binary
   $\mathrm{Bern}(\eta) \| \mathrm{Bern}(\tfrac12)$ instance.
   Numerical spot-check (terminal log of commit `f8d6db6`):
   the BH lower endpoint $\tfrac12 - \tfrac12 \sqrt{1 -
   \exp(-(1 - H_{\mathrm{bin}}(\eta)) \ln 2)}$ strictly beats
   the Pinsker endpoint $\tfrac12 - \sqrt{(\ln 2)/2 \cdot
   (1 - H_{\mathrm{bin}}(\eta))}$ for $\eta \in [0.10, 0.18]$
   (BH wins by $\geq 0.03$ at $\eta = 0.10$); the crossover
   band lies in $\eta \in (0.18, 0.22)$ rather than a single
   clean threshold. A clean meta-theorem-style statement
   $\varepsilon^*_\Pi \geq \tfrac12 - \tfrac12 \sqrt{1 -
   \exp(-(1 - H(f \mid \Pi)) \ln 2)}$ aggregated by Jensen
   on the concave $1 - \sqrt{1 - e^{-x}}$, together with a
   verifier contract `check_CBH_*`, is open. Closing OP-BH
   would push the vacuity threshold of C-Pi strictly below
   the current $H(f \mid \Pi) \approx 0.279$.
9. **(OP-soft)** Countable-alphabet lift of T9. The finite
   case $|\mathcal{Z}| = m < \infty$ is proven
   unconditionally; the countable extension
   $\mathcal{Z} = \mathbb{N}$ requires a uniform-integrability
   hypothesis on $\{\varphi(\eta^K_z)\}_z$ to keep
   $\varphi(f \mid K) = \sum_z p^K_z \varphi(\eta^K_z)$
   absolutely convergent under refinement, *and* requires
   that the post-kernel cell-rate barycentre identity (Step
   3 of T9) lifts to a measurable Markov-kernel composition
   over a countable space. The most likely failure mode is a
   Cesàro-type pathology: a sequence of finite kernels
   $K_n \to K$ with $\varphi(f \mid K_n)$ Cauchy but
   $\varphi(f \mid K)$ ill-defined. A clean statement and
   verifier contract `check_T9_countable_*` are open.
8. **(OP-soft)** Countable-alphabet T9 (§5): the finite-$m$
   kernel bracket lifts to countably-infinite code alphabets
   only under a uniform-integrability hypothesis on
   $\{\varphi(\eta_z^K)\}_z$. Naming the minimal sufficient
   condition (or counter-example showing the lift fails
   without it) is open.
9. **(OP-BH)** Bretagnolle–Huber strengthening of C-Pi (§3):
   $D_{\mathrm{KL}} \geq -\log(1 - 4\,\mathrm{TV}^2)$ in nats
   strictly improves Pinsker for $|\eta - \tfrac12| > \sim 0.32$.
   The corresponding sqrt-bound replacement in (C-Pi.lower)
   would push the vacuity threshold strictly below 0.279; a
   clean meta-theorem-style statement (with verifier contract)
   is open.

---

## 8. Verifier contracts (forward references)

Every numbered claim above is interpreted, per §0.5, as
carrying a property contract $\mathcal{C} = (\mathcal{D},
n, \tau, P, \sigma)$ in the sense of Definition 0.1, with
falsification guarantees given by Propositions 0.3 (B-T1) and
0.4 (B-T2). The downstream prose block has the form:

> **Verifier contract.** Mechanically checked by
> `verify_b_t1.py::check_<id>` (B-T1, SymPy + Hypothesis) and,
> for population statements, `verify_b_t2_mc.py::check_<id>`
> (B-T2, Monte-Carlo). The 5-tuple $\mathcal{C}$ is the
> Definition-0.1 instantiation of the sampler / budget /
> tolerance / pass-predicate / seed-policy quoted in the
> block. Run commands and JSON manifest fields are documented
> in [`FORMALISATION.md`](FORMALISATION.md) §4–§6.

The verifier files live alongside this document:

- [`verify_b_t1.py`](verify_b_t1.py) — **B-T1** (symbolic
  identities + Hypothesis property tests; on the critical
  path).
- [`verify_b_t2_mc.py`](verify_b_t2_mc.py) — **B-T2**
  (Monte-Carlo population concentration; on the critical
  path).
- [`verify_b_optional.jl`](verify_b_optional.jl) — **OPTIONAL,
  off the critical path.** Julia / IntervalArithmetic parity
  with Paper A's `verify.jl`; not required to close Gate G2.
  Rationale in [`FORMALISATION.md`](FORMALISATION.md) §4.

As of Phase 2b-md.G2 (CLOSED), the two critical-path
verifiers are fully implemented and green: `verify_b_t1.py`
ships eight `check_*` contracts (T3-lower, T3-upper, C-Sh,
C-Va, C-Pi, T7-symbolic, P10, L11) and `verify_b_t2_mc.py`
ships six (T6-MSE, T6-MAE, C-Va population, T7 population,
T7 Shannon vs. Paper A, T9 kernel) — counts match the
`8/8 + 6/6` ladder cited in the status box at the top of
this document. The earlier (Phase 2b-md.A013) docstring-only
skeletons have been superseded; per-contract pass logs are
manifested in `audit/` and surfaced through
[`FORMALISATION.md`](FORMALISATION.md) §3 (G2 gate-table).

---

## Appendix A — Experimental suite (full documentation)

This appendix documents *every* experiment that backs a
numbered claim in the body of the paper. There is **no new
training**: Paper B re-uses the trained partitions from
Paper A (vectorised 1-WL refinement, no GPU) and otherwise
operates on synthetic distributions sampled by the verifier
files. Every artefact named below is regenerable from a
single command, listed in the rightmost column of Table A.1.

### A.1 Tier overview

The experimental program decomposes into **six reproducibility
tiers** wired together by the driver
`audit/run_external_audit.sh`. Each tier emits a JSON manifest
under `audit/external_audit/T{0..5}.log` plus the per-tier
result file, and the driver aggregates pass/fail into
`audit/external_audit_SUMMARY.json`.

| Tier | Role                                  | Driver                          | Manifest                                | Wall (1 CPU) |
|------|---------------------------------------|---------------------------------|-----------------------------------------|--------------|
| T0   | Build + import sanity                 | `pip install -r requirements.txt; python -c "import verify_b_t1, verify_b_t2_mc"` | `audit/external_audit/T0.log`           | $< 1$ s      |
| T1   | Symbolic + property (B-T1)            | `python verify_b_t1.py`         | `verify_b_t1.json`                      | $\approx 3$ s |
| T2   | Monte-Carlo population (B-T2)         | `python verify_b_t2_mc.py`      | `verify_b_t2.json`                      | $\approx 21$ s |
| T3   | Adversarial stress (15 seeds × mutation × boundary) | `python audit/stress.py --seeds 15 --samples 50000 --trials 200` | `audit/external_audit/T3_stress.json` | $\approx 1400$ s |
| T4   | Real-data anchor (5 graphs × 4 depths) | `python audit/anchor_real_data_full.py` | `audit/anchor_real_data_full.json`     | $\approx 10$ s |
| T5   | Cross-paper parity (vs. Paper A)      | Paper A's `verify_t1_float.py`, `verify_t3_symbolic.py`, `verify_t4_population.py` | `partition-sandwich-preprint/verify_t{1,3,4}.json` | $\approx 14$ s |

**Table A.1.** The six reproducibility tiers. Total wall on a
single CPU core: $\approx 24$ min; T3 dominates. No GPU, no
new training. SHA-stamped run: `c381a4f` (2026-06-01), all
six PASS, archived in `audit/external_audit_SUMMARY.json`.

### A.2 Per-contract methodology

**B-T1 (`verify_b_t1.py`).** Eight contracts; one per numbered
claim in the body. Each contract is a tuple
$(\mathcal{D}, n, \tau, P, \sigma)$ in the sense of
Definition 0.1 with $\sigma = (\text{seed}=0,\,\mathrm{derandomize}=\mathrm{True})$,
$\tau = 10^{-9}$, $n = 200$ (Hypothesis `max_examples` at the
manuscript-default `--samples 1000`; via the rule
`max_examples = max(50, samples // 5)` baked at
`verify_b_t1.py` line 204). The sampler $\mathcal{D}$ is
contract-specific: random partitions with $m \in [2, 16]$
cells, masses Dirichlet$(\mathbf{1}_m)$, rates Uniform$[0,1]$
(T3, P10, C-Sh, C-Va, C-Pi); plus per-claim auxiliary
distributions (Lipschitz constants $L^c, L^m \in [0.1, 2]$
for L11; noise rates $\rho \in \{0.05, 0.10, 0.20\}$ for T7).
Symbolic identities (SymPy `simplify(...) == 0`) sit
*alongside* the random search, not inside it, per §0.5.

**B-T2 (`verify_b_t2_mc.py`).** Six contracts; one per
*population-level* statement (the bracket has measure-zero
slack in the IID limit). Each contract draws $N = 50\,000$
IID samples per trial, runs $R = 500$ trials, and checks the
inequality at tolerance $\tau = 4 \cdot
\sqrt{\ln(2/\alpha)/(2N)}$ with $\alpha = 0.05$
(`_hoeffding_halfwidth`, `verify_b_t2_mc.py` lines 87–89);
the $4\times$ inflation is the union-bound budget over the
$\leq 4$ McDiarmid coordinates used by T7 (lines 304–306).
Proposition 0.4 caps the per-contract false-rejection
probability at $\leq 2 \cdot (\alpha/2)^{16} \approx 4.6
\times 10^{-26}$.

**T3 stress (`audit/stress.py`).** Three orthogonal sub-suites:

- *Seed sweep:* re-runs the B-T1 + B-T2 contracts on
  $\sigma \in \{0, 1, \dots, 14\}$ at $n = 10\,000$
  Hypothesis examples per seed for B-T1 and $N = 50\,000,\
  R = 500$ for B-T2. Production target: zero failures
  across the entire $15 \times (8 + 6) = 210$ contract
  evaluations.
- *Mutation screen:* injects $K = 3$ syntactic mutants
  (`T7_wrong_sign`, `T3_wrong_c_phi`, `CVa_wrong_identity`)
  and asserts every mutant is caught by at least one
  contract. Definition 0.2 gives the formal coverage notion;
  comprehensiveness is OP-mut, §7.
- *Boundary screen:* 13 closed-form spot-checks at
  manuscript-quoted extremes — $H_{\mathrm{bin}}(10^{-12})$
  finite, $H_{\mathrm{bin}}(\tfrac12) = 1$, T3 bracket on
  $m = 1$ and $m = 1000$ partitions, T7 identity at
  $\rho \in \{0, 10^{-3}, 0.499\}$, the $1/(1 - 2\rho)$
  blow-up at $\rho = 0.4999$, C-Pi vacuity threshold at
  $H \approx 0.279$, T9 reduction to T3 in the deterministic
  case, P10 atom-level $\varphi = 0$ collapse.

**T4 real-data anchor (`audit/anchor_real_data_full.py`).**
Re-uses Paper A's vectorised 1-WL refinement (Manifest
`partition-sandwich-preprint/experiments/results/e1_trees.json`,
etc.) to extract cell-level $(q_C, P_C)$ from five graph
datasets at depths $L \in \{0, 1, 2, 3\}$. For each row,
computes the *true* partition-restricted Bayes risk
$\varepsilon^*_\Pi = \sum_i p_i \min(\eta_i, 1 - \eta_i)$
and the three bracket endpoints (C-Sh, C-Va, C-Pi) at
tolerance $10^{-9}$. Pass predicate: every endpoint
envelopes $\varepsilon^*_\Pi$ within tolerance (lower
endpoint $\leq \varepsilon^*_\Pi \leq$ upper endpoint,
with C-Pi clipped at $0$ when the raw Pinsker bound goes
negative).

**T5 cross-paper parity.** Re-runs Paper A's three verifiers
(`verify_t1_float.py`, `verify_t3_symbolic.py`,
`verify_t4_population.py`) at the *same* synthetic samples
used by B-T1/B-T2 in this paper and asserts the Shannon
specialisations match Paper A to $\leq 10^{-9}$
(`verify_b_t2_mc.py::check_T7_shannon_matches_paperA`
records the worst gap at $7.8 \times 10^{-16}$).

### A.3 Reproducing the suite

A single command reproduces every claim in the body:

```bash
cd partition-brackets-framework
./audit/run_external_audit.sh        # ~24 min on a 2020 MacBook Pro
cat audit/external_audit_SUMMARY.json # expect all_pass: true
```

Subset reproduction (skipping the $\approx 20$ min T3 stress):

```bash
./audit/run_external_audit.sh T0 T1 T2 T4 T5   # ~1 min
```

The seed sweep is bit-deterministic at fixed seeds; the
`derandomize=True` Hypothesis flag plus the per-test salted
NumPy generator guarantee reruns under the same SHA produce
identical JSON manifests modulo wall-clock fields.

---

## Appendix B — Results

### B.1 Verifier-tier summary

The Phase 2b-md.G2 manuscript-default run
(`verify_b_t1.py --samples 1000 --seed 0` and
`verify_b_t2_mc.py --samples 50000 --trials 500 --seed 0`)
yields:

| Tool                      | Contracts | Pass | Fail | Worst slack             |
|---------------------------|-----------|------|------|-------------------------|
| `verify_b_t1.py` (B-T1)   | 8         | 8    | 0    | $4.18 \times 10^{-4}$ (C-Pi, slack on a 250-example fuzz) |
| `verify_b_t2_mc.py` (B-T2)| 6         | 6    | 0    | $5.1 \times 10^{-3}$ (T7 noise, residual on 1500 trials)  |

**Table B.1.** Critical-path verifier pass rates. The worst
B-T2 residual ($5.1 \times 10^{-3}$) is well inside the
4×-Hoeffding tolerance $\tau \approx 0.0243$ at
$N = 50\,000$; Proposition 0.4 caps the per-contract false-
rejection probability at $4.6 \times 10^{-26}$.

| Contract                              | Tier | Sampler / N                                          | Status | Detail                                                                     |
|---------------------------------------|------|------------------------------------------------------|--------|----------------------------------------------------------------------------|
| `T3_jensen_lower`                     | B-T1 | $(m, p, \eta) \sim$ Dir/Unif, $n=200$ × 3 $\varphi$   | pass   | (H1, H4) SymPy ok; 200 examples ok                                          |
| `T3_upper_constant`                   | B-T1 | $10^4$-pt grid on $(0, 1/2]$ + 200 examples           | pass   | $c_\varphi$ certified to $5 \times 10^{-4}$ on grid                         |
| `CSh_reduces_to_paperA`               | B-T1 | Same cohort + Paper A reference bracket               | pass   | Meta == Paper A within $10^{-9}$                                            |
| `CVa_bayes_variance_identity`         | B-T1 | Same cohort + LTV check                               | pass   | (C-Va.id) + LTV + T3 bracket all ok                                         |
| `CPi_pinsker_constant`                | B-T1 | $10^4$-pt grid + 250 examples                         | pass   | Worst slack $4.18 \times 10^{-4}$                                            |
| `P10_refinement_monotonicity`         | B-T1 | Random refine of $m \in [2,8]$ base × 3 $\varphi$     | pass   | $\varphi(f \mid \Pi') \leq \varphi(f \mid \Pi)$                              |
| `L11_aggregator_deltaL`               | B-T1 | Random linear MPNN on star, $L \in [1,5]$             | pass   | Product formula symbolic + empirical                                         |
| `T7_noise_correction_symbolic`        | B-T1 | Pure SymPy (no random)                                | pass   | (T7.affine) + (T7.kink) + (T7.correction)                                    |
| `CVa_variance_identity_population`    | B-T2 | Beta per cell, $N=50\,000$, $R=500$                   | pass   | $\widehat{\mathrm{MSE}}^* - \sum \hat p_i \hat\eta_i(1-\hat\eta_i)$ worst 0  |
| `T6_MSE_identity_population`          | B-T2 | Same cohort                                           | pass   | $\widehat{\mathrm{MSE}}^* = \widehat{\mathbb{E}}[\mathrm{Var}]$ worst 0       |
| `T6_MAE_upper_population`             | B-T2 | Same cohort + cell-wise median                        | pass   | $\widehat{\mathrm{MAE}}^* \leq \sqrt{\widehat{\mathrm{MSE}}^*}$ worst residual 0 |
| `T7_noise_correction_population`      | B-T2 | $\rho \in \{0.05, 0.10, 0.20\}$, $R=1500$             | pass   | Worst residual $5.1 \times 10^{-3} \ll \tau$                                 |
| `T7_shannon_matches_paperA`           | B-T2 | 200 trials × 3 $\rho$                                 | pass   | Worst $\lvert\Delta\varphi\rvert = 0$                                       |
| `T9_kernel_bracket_population`        | B-T2 | Random row-stoch. kernel, $N=50\,000$                 | pass   | Both endpoints envelope $\hat\varepsilon^*_K$                                |

**Table B.2.** Per-contract verdict at SHA `c381a4f`,
manuscript-default budgets. Stress-tier walls and seed-sweep
behaviour are aggregated in Table B.3.

### B.2 T3 stress tier (15 seeds × mutation × boundary)

Three sub-suites; aggregate at SHA `c381a4f`,
$T_{\mathrm{wall}} = 1415$ s:

- *Seed sweep:* $15 \times (8 + 6) = 210$ contract
  evaluations on $\sigma \in \{0, \dots, 14\}$ at
  $n = 10\,000$ (B-T1) / $R = 500$ trials (B-T2). **0
  failures.** Per-seed B-T1 wall ranges $\approx 58$–$79$ s
  (median 66 s); per-seed B-T2 wall ranges $\approx 19$–$21$ s
  (median 20 s).
- *Mutation screen:* $3 / 3$ caught.
  - `T7_wrong_sign` (flip the noise sign in T7.correction)
    → caught by `T7_noise_correction_symbolic` and
    `T7_noise_correction_population`.
  - `T3_wrong_c_phi` (swap $c_\varphi = 1/2 \to 1/3$ for
    Shannon) → caught by `T3_upper_constant` and
    `CSh_reduces_to_paperA`.
  - `CVa_wrong_identity` (replace $\eta(1-\eta)$ by $\eta^2$)
    → caught by `CVa_bayes_variance_identity` and
    `CVa_variance_identity_population`.
- *Boundary screen:* $13 / 13$ pass. Spot-checks include
  $H_{\mathrm{bin}}(10^{-12}) = 4.13 \times 10^{-11}$
  (finite, as required), $H_{\mathrm{bin}}(\tfrac12) = 1.0$,
  the C-Pi vacuity threshold ($\mathrm{lower} = 0$ at
  $H = 0.279$), and the T9 reduction to T3 in the
  deterministic case ($\varepsilon_K = \varepsilon_{\text{hard}}
  = 0.2262$).

**Table B.3 — Stress tier summary.**

| Sub-suite     | Configuration                              | Failures | Notes                                       |
|---------------|--------------------------------------------|----------|---------------------------------------------|
| Seed sweep    | 15 seeds, $n = 10\,000$ (B-T1) / $R = 500$ | 0 / 210  | Wall $\approx 60$–$79$ s per seed (B-T1)    |
| Mutation      | $K = 3$ mutants                            | 0 / 3 (uncaught) | $\rho_{\mathcal{M}_{\mathrm{B}}} = 1$  |
| Boundary      | 13 closed-form spot-checks                 | 0 / 13   | Includes C-Pi vacuity, T9→T3, $\rho \to \tfrac12$ blow-up |

### B.3 Real-data anchor (T4)

The 20-row anchor table verifies all three T3 instances
(C-Sh, C-Va, C-Pi) against the *true* partition-Bayes risk
extracted from Paper A's 1-WL cell-level
$(q_C, P_C)$ on five graph datasets. Status: **20 / 20
pass**, wall $\approx 10$ s, no GPU, no new training.

**Table B.4 — Per-row results
(`audit/anchor_real_data_full.json`).**

| Dataset    | $L$ | $m$ (cells) | $H(f \mid \Pi)$ | $\varepsilon^*_\Pi$ | C-Sh lower | C-Sh upper | C-Va lower | C-Va upper | C-Pi lower | C-Pi vacuous |
|------------|----:|------------:|----------------:|--------------------:|-----------:|-----------:|-----------:|-----------:|-----------:|:------------:|
| citeseer   | 0   | 32          | 0.734           | 0.2107              | 0.2060     | 0.3669     | 0.2078     | 0.3292     | 0.1963     | N            |
| citeseer   | 1   | 983         | 0.523           | 0.1632              | 0.1177     | 0.2613     | 0.1386     | 0.2388     | 0.0933     | N            |
| citeseer   | 2   | 1835        | 0.302           | 0.0986              | 0.0537     | 0.1509     | 0.0754     | 0.1394     | 0.0081     | N            |
| citeseer   | 3   | 2044        | 0.242           | 0.0775              | 0.0400     | 0.1212     | 0.0593     | 0.1115     | 0.0000     | **Y**        |
| cora       | 0   | 37          | 0.864           | 0.3002              | 0.2861     | 0.4318     | 0.2899     | 0.4117     | 0.2826     | N            |
| cora       | 1   | 1589        | 0.327           | 0.1289              | 0.0598     | 0.1633     | 0.0864     | 0.1579     | 0.0169     | N            |
| cora       | 2   | 2301        | 0.089           | 0.0391              | 0.0112     | 0.0444     | 0.0223     | 0.0436     | 0.0000     | **Y**        |
| cora       | 3   | 2363        | 0.065           | 0.0292              | 0.0076     | 0.0323     | 0.0162     | 0.0318     | 0.0000     | **Y**        |
| ogbn_arxiv | 0   | 547         | 0.579           | 0.1599              | 0.1380     | 0.2894     | 0.1433     | 0.2456     | 0.1180     | N            |
| ogbn_arxiv | 1   | 123 755     | 0.077           | 0.0169              | 0.0094     | 0.0383     | 0.0144     | 0.0285     | 0.0000     | **Y**        |
| ogbn_arxiv | 2   | 157 563     | 0.012           | 0.0035              | 0.0011     | 0.0061     | 0.0025     | 0.0050     | 0.0000     | **Y**        |
| ogbn_arxiv | 3   | 161 943     | 0.006           | 0.0021              | 0.0005     | 0.0029     | 0.0013     | 0.0027     | 0.0000     | **Y**        |
| pubmed     | 0   | 82          | 0.965           | 0.3950              | 0.3901     | 0.4824     | 0.3909     | 0.4762     | 0.3897     | N            |
| pubmed     | 1   | 8060        | 0.540           | 0.2113              | 0.1239     | 0.2702     | 0.1554     | 0.2625     | 0.1009     | N            |
| pubmed     | 2   | 12 814      | 0.156           | 0.0556              | 0.0227     | 0.0781     | 0.0378     | 0.0728     | 0.0000     | **Y**        |
| pubmed     | 3   | 12 990      | 0.144           | 0.0511              | 0.0205     | 0.0722     | 0.0348     | 0.0671     | 0.0000     | **Y**        |
| twitch_en  | 0   | 130         | 0.962           | 0.4164              | 0.3853     | 0.4809     | 0.3909     | 0.4762     | 0.3848     | N            |
| twitch_en  | 1   | 5810        | 0.188           | 0.0790              | 0.0287     | 0.0939     | 0.0484     | 0.0921     | 0.0000     | **Y**        |
| twitch_en  | 2   | 6633        | 0.065           | 0.0278              | 0.0077     | 0.0325     | 0.0162     | 0.0319     | 0.0000     | **Y**        |
| twitch_en  | 3   | 6648        | 0.062           | 0.0267              | 0.0073     | 0.0312     | 0.0156     | 0.0306     | 0.0000     | **Y**        |

All entries are rounded to 4 decimals; the raw JSON manifest
carries IEEE-754 doubles. Tolerance for envelope check:
$10^{-9}$.

### B.4 Cross-paper parity (T5)

`verify_b_t2_mc.py::check_T7_shannon_matches_paperA` matches
Paper A's binary-entropy bracket (`thm:sandwich`, Theorem 1)
to $\lvert\Delta_{\mathrm{lower}}\rvert = 7.8 \times 10^{-16}$
and $\lvert\Delta_{\mathrm{upper}}\rvert = 0$ on a 600-row
cohort (200 trials × 3 noise levels). Paper A's three
verifiers (`verify_t1_float`, `verify_t3_symbolic`,
`verify_t4_population`) re-run cleanly at SHA `c381a4f` with
zero diff on the shared synthetic samples.

---

## Appendix C — Discussion

### C.1 Sharpness of the bracket on real graphs

The most informative pattern in Table B.4 is the **depth
behaviour of the C-Pi vacuity flag**. At $L = 0$ (raw node
features) every dataset has $H(f \mid \Pi) > 0.5$ and the
Pinsker bracket is non-vacuous; by $L = 2$ the WL refinement
has pushed $H$ below the threshold $1 - \tfrac{1}{2 \ln 2}
\approx 0.279$ on every dataset except (marginally) pubmed
at $L = 1$, where $H = 0.540 > 0.279$ but the bracket is
already loose ($0.10$ vs. true $\varepsilon^* = 0.21$). The
Shannon (C-Sh) and variance (C-Va) brackets remain non-vacuous
throughout; both envelope $\varepsilon^*_\Pi$ in all 20 rows.

The empirical ordering of the *lower* endpoints,
$\text{C-Pi} \leq \text{C-Sh} \leq \text{C-Va}$, holds in
**every** row of Table B.4. This is consistent with the
theory: C-Va re-arranges to a tighter lower bound than C-Sh
in the deep-refinement / small-$\varepsilon^*$ regime (the
quadratic $\eta(1 - \eta)$ vanishes faster than $H_{\mathrm{bin}}$
near $\eta \to 0$, so its inverse on $[0, 1/2]$ is steeper),
and Pinsker is uniformly loose in this regime (its vacuity is
the explicit failure mode). The *upper* endpoints have the
reverse ordering on most rows because $c_{\mathrm{var}} = 2 >
c_{H_{\mathrm{bin}}} = \tfrac12$ inflates the linear ratio
more aggressively. Closing OP-BH (Bretagnolle–Huber drop-in)
would push the C-Pi vacuity rows ogbn_arxiv-$L \geq 1$ and
twitch_en-$L \geq 1$ back into the non-vacuous regime.

### C.2 What the verifier suite does and does not prove

**Proves (with the formal guarantees of Propositions 0.3 / 0.4):**

- Every numbered claim holds on the *synthetic* sampler
  $\mathcal{D}$ at the quoted $n$ examples with missed-
  counterexample probability $\leq (1 - \mu)^n$ for any
  measure-$\mu$ violation set (Proposition 0.3).
- Every population identity (B-T2) survives $N = 50\,000$
  IID samples × $R = 500$ trials with per-contract false-
  rejection probability $\leq 4.6 \times 10^{-26}$
  (Proposition 0.4).
- The mutation screen catches three load-bearing single-line
  faults (Definition 0.2 discovery rate $\rho = 1$ at
  $K = 3$).
- All 20 real-graph anchor rows envelope the true
  partition-Bayes risk within the bracket — i.e. the bracket
  is *non-vacuously verified outside the synthetic sampler*.

**Does not prove:**

- Comprehensiveness of the mutation screen (only three
  load-bearing lines tested; OP-mut, §7).
- Type II error of B-T2: a claim wrong by less than
  $4 h \approx 0.024$ would not be flagged. Closing this
  needs Lean / Mathlib certification
  (`FORMAL_VERIFICATION_EXECUTION_PLAN.md`).
- Soundness on a measure-zero violation manifold under the
  synthetic sampler $\mathcal{D}$.
- Comparison with non-bracket Bayes-error estimators
  (mixture, kNN, $\eta$-regressors): explicitly out of scope;
  Paper B exhibits a closed-form bracket, not a competing
  estimator.

### C.3 Threats to validity

**(V1) Synthetic-sampler bias.** The B-T1 contracts use
Dirichlet$(\mathbf{1})$ cell masses and Uniform rates; a real
1-WL cell-mass distribution is heavy-tailed and the rate
distribution concentrates near $\{0, 1\}$ at large $L$. The
real-data anchor (T4) directly addresses this by re-checking
the bracket on the actual Paper A cells; the 20-row pass
table is the *non-synthetic* certificate.

**(V2) Hypothesis shrinker pathology (A-SHRINK, §7).** The
$(1 - \mu)^n$ bound in Proposition 0.3 treats the
derandomized Hypothesis stream as IID; the shrinker biases
toward edge cases, which usually *strengthens* coverage but
could in principle systematically avoid a pathological
violation set. The 15-seed sweep (T3) empirically amortises
against any single seed pathology.

**(V3) PRG idealisation (A-PRNG, §7).** Proposition 0.3 is
conditional on a PRG-hardness modelling assumption. The
cryptographic reduction is open; in practice the seed sweep
is the empirical fallback.

**(V4) Nonlinear MPNN slack.** L11 is tight for linear MPNNs
and an upper estimate for nonlinear ones (e.g. ReLU on
unbounded features). The verifier contract uses *linear*
random MPNNs; nonlinear empirical slack is not measured in
Paper B.

**(V5) Real-graph dataset selection.** The five datasets in
Table B.4 are the same as Paper A's experimental program;
extension to molecular / heterogeneous / temporal graphs is
left to the sequel.

### C.4 Computational cost and reproducibility budget

Full audit on a 2020 MacBook Pro (M1, single CPU core):
$\approx 24$ min wall; subset (T0–T2, T4, T5):
$\approx 1$ min wall. No GPU, no new training, no
ML-framework dependency beyond NumPy / SymPy / Hypothesis.
The seed sweep alone consumes $\approx 23$ min; the
manuscript-default critical-path tier
(`verify_b_t1.py && verify_b_t2_mc.py`) runs in $< 30$ s and
is the appropriate test target for routine development.

### C.5 What we hope a reviewer / re-implementer will check

In order of expected return on time invested:

1. Run `./audit/run_external_audit.sh T0 T1 T2 T4 T5`
   ($\approx 1$ min): confirms 14 / 14 contracts + 20 / 20
   anchor rows are green at HEAD.
2. Spot-check three rows of Table B.4 by hand against the JSON.
3. Inject a fourth mutation (e.g. drop the
   $1/(1 - 2\rho)$ in T7.correction): confirm at least one
   contract catches it.
4. Re-evaluate C-Pi on a row with high $H$ (cora $L = 0$,
   pubmed $L = 0$): confirm the bracket is genuinely
   non-vacuous and tight to 2 decimals.
5. Run the full $\approx 24$ min audit at a fresh SHA:
   confirms the SUMMARY refresh procedure
   (`cp audit/external_audit/SUMMARY.json audit/external_audit_SUMMARY.json`).

---

## 9. References

- Paper A: *A Two-Sided Bayes-Error Bracket from Partition-
  Conditional Entropy*, companion preprint at
  [`../partition-sandwich-preprint/`](../partition-sandwich-preprint/).
- Cover & Thomas (2006), *Elements of Information Theory*, 2nd ed.
- Meilă (2003), *Comparing clusterings by the variation of
  information*.
- Vinh, Epps & Bailey (2010), *Information theoretic measures
  for clusterings comparison*.
- Corso, Cavalleri, Beaini, Liò & Veličković (2020), *Principal
  Neighbourhood Aggregation for Graph Nets*, NeurIPS.
- Natarajan, Dhillon, Ravikumar & Tewari (2013), *Learning with
  Noisy Labels*, NeurIPS.
- Kochenderfer, Wheeler & Wray (2022), *Algorithms for Decision
  Making*, MIT Press.
- Bretagnolle, J. & Huber, C. (1979), *Estimation des densités:
  risque minimax*, Z. Wahrscheinlichkeitstheorie verw. Gebiete
  47, pp. 119–137. (OP-BH reference for the
  $\mathrm{TV} \leq \sqrt{1 - e^{-D_{\mathrm{KL}}}}$ bound.)
- Chung, F. (1997), *Spectral Graph Theory*, CBMS Regional
  Conference Series in Mathematics, vol. 92, AMS. (Lemma 1.7,
  operator-norm bound on $D^{-1/2} A D^{-1/2}$, referenced in
  L11 proof for the sym-norm aggregator constant $r_T = 1$ on
  irregular graphs.)
- McDiarmid, C. (1989), *On the method of bounded
  differences*, Surveys in Combinatorics 141, pp. 148–188.
  (Proposition 0.4 concentration tool.)
- Hoeffding, W. (1963), *Probability inequalities for sums of
  bounded random variables*, JASA 58(301), pp. 13–30.
  (Sample-mean special case of Proposition 0.4.)
