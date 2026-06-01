# Sequel paper roadmap — *Quantitative $k$-WL via a Trickle-Down Bracket*

Draft, 2026-06-01. Distinct from `05-sequel-paper-plan.md`: that one
is the broad menu of follow-up directions; this one is a single
committed plan for one TCS-flavoured sequel.

---

## Step 0 — What this paper is *not*

- Not a v2 of `partition-sandwich-preprint/`. Preprint stays as the
  ML-practitioner-facing TMLR/arXiv submission.
- Not a survey of "ways to apply the bracket." One anchor angle.
- Not a paper about train/test/population risk. Structural only.

## Step 1 — Angle selection

- **Primary anchor: HDX / $k$-WL.** Morris $k$-WL is the most-cited
  GNN expressivity construct; no quantitative diagnostic exists for
  it; the bracket is the natural candidate; HDX is its mathematical
  home (up-down walks, Garland, trickle-down).
- **Supporting anchor: Property Testing.** Provides the
  correctness/optimality vocabulary (tolerant tester, query
  complexity, Blais / Fischer–Fortnow lower bounds).
- Wigderson framing used in §1 / §7 only, as positioning glue.
- BFA, PGM, Kochenderfer: explicitly deferred to a *third* paper.

## Step 2 — One-sentence thesis

> The partition-conditional entropy bracket lifts the $k$-WL
> expressivity hierarchy from a binary distinguishability statement
> into a quantitative, two-sided, tolerant-tester-tight diagnostic on
> each $(k\text{-WL skeleton},\;\text{label})$ pair, with the slack
> constant $w^\* \approx 0.16$ identified as the optimal gap for any
> single-statistic Boolean tester.

This sentence is the load-bearing wall. Every section earns its place
by serving it.

## Step 3 — The one new theorem

**T-A (primary, trickle-down bracket).** For a graph $G$ and binary
label $f$, with $\Pi^{(k)}_L$ the depth-$L$ $k$-WL partition,
$$H(f \mid \Pi^{(k)}_L) \;\le\; \lambda_k(G,L)\cdot H(f\mid\Pi^{(k+1)}_L),$$
where $\lambda_k(G,L)\in[0,1]$ is the second eigenvalue of the
$(k+1)$-up / $k$-down random walk on the WL skeleton at depth $L$
(Oppenheim trickle-down on the WL complex).

**Fallbacks if T-A fails Step 4 or Step 9:**

- **T-B.** $H(f|\Pi)$ is an optimal single-statistic tolerant tester
  for "$f$ is $\Pi$-constant" with gap $w^\*$; matching lower bound.
- **T-C.** Hypercontractive bracket
  $\varepsilon^\*_{\Pi_J}\le\tfrac12(1-\rho^{|J^c|/2}\|f\|_2)$ via $T_\rho$
  on $f^{\le J}$.

## Step 4 — Empirical pre-check (BEFORE writing)

Compute on a small library — CFI($n$) for $n\in\{4,8,16\}$,
Paley($q$) for $q\in\{13,17,29\}$, CSL(41,$\{1,9\}$), Petersen,
random 3-regular on $|V|=20$:

1. $\Pi^{(k)}_L$ for $k=1,2$ and $L\in\{0,1,2,3\}$.
2. $H(f|\Pi^{(k)}_L)$ for $\sim 100$ random binary labels.
3. Up-down walk on the $k$-skeleton; $\lambda_k$ as second eigenvalue.
4. Verify $H(f|\Pi^{(k)}_L) \le \lambda_k \cdot H(f|\Pi^{(k+1)}_L)$.

Output: `step4_trickle_check.json` with a yes/no verdict per row.
~50 lines of Python + NumPy. **Do not start §3 LaTeX until this clears.**

## Step 5 — Venue

- **Primary target: COLT** (9 pp). Audience tolerates HDX/BFA
  without remedial exposition.
- Stretch: ITCS/STOC (10 pp pure TCS).
- Fallback: TMLR (unlimited, ML-friendly).

## Step 6 — Section outline (9 pp)

| § | Title                                       | pp  |
|---|---------------------------------------------|-----|
| 1 | Introduction (+ headline figure)            | 1.0 |
| 2 | Preliminaries ($k$-WL, up-down, $H$)        | 0.5 |
| 3 | Theorem T-A + proof + three corollaries     | 2.5 |
| 4 | Property-testing optimality (T-B corollary) | 1.0 |
| 5 | Three combinatorial experiments             | 2.5 |
| 6 | Related work                                | 0.5 |
| 7 | Discussion + Wigderson framing              | 0.5 |
|   | Appendix: full proofs, Lean note            | —   |

**Excluded by design:** NAS, decision trees, vector quantisation,
train/test, real ML benchmarks beyond binarised structural graphs.

## Step 7 — Locked experiments (no population risk)

- **X1.** $k$-WL trickle-down funnel on combinatorial families
  (CFI, Paley, CSL, Kneser, Cayley, Petersen). Headline figure:
  predicted-vs-realised trickle-down scatter, $y=x$ overlay.
- **X2.** Boolean function library on the achievable region.
  $n\le 12$, exact. Parity / Maj / Tribes / Recursive-Maj / Address /
  Dictator / random junta. Headline figure: each class traces a
  distinct curve in $(H,\varepsilon)$ space; **constructs** the
  achievable region.
- **X3.** Mechanised verification at scale: $10^6$ random partitions,
  $|V|$ up to $10^4$, exact-rational $\varepsilon^\*$, interval $H$,
  both bracket sides + trickle-down. Paired with Lean 4 proofs of the
  two scalar lemmas (Hellman–Raviv per cell; Jensen on $H_2$) using
  `Real.binEntropy` and the `ConcaveOn` API.

## Step 8 — Artefact accounting

**Reuse from preprint:**

- `verify.jl` skeleton → extend to $10^6$ partitions + trickle-down.
- $k$-WL code from E3b (CSL, Paley).
- Achievable-region plotting from E5.
- Hellman–Raviv scalar lemma.

**Build new:**

- $k$-skeleton constructor for $k=2,3$ on $|V|\le 50$.
- Up-down walk eigenvalues (dense, `numpy.linalg.eigh`).
- Boolean library exact $H,\varepsilon^\*$ for $n\le 12$.
- Lean 4 proof file `KWLBracket.lean`.

**Relative effort buckets:** T-A proof (medium-large); X1 (medium);
X2 (small); X3 (small-medium); Lean (medium); writing (medium).

## Step 9 — Pre-committed kill criteria

- **K1.** Step-4 empirical check fails → fall back to T-B only,
  reposition as a Property-Testing paper, TMLR not COLT.
- **K2.** $\lambda_k\equiv 1$ on the families of interest (vacuous
  trickle-down) → switch anchor to T-C (hypercontractive form).
- **K3.** Literature sweep finds T-A already proved (search:
  $k$-WL ∩ HDX, WL ∩ Garland, GI ∩ trickle-down, recent
  Dinur–Kaufman / Liu–Mohanty–Yang) → reposition as "first
  application to $k$-WL," scope down to a workshop note.

## Step 10 — Writing order

1. Theorem statement + proof in LaTeX (load-bearing wall).
2. §5 experiments (numbers must exist before prose around them).
3. §2 preliminaries (notation that matches the proof).
4. §6 related work (after the proof is stable).
5. §1 introduction (last; advertises an existing artefact).
6. Abstract.
7. §7 discussion (one focused pass).

## Step 11 — Naming / artefacts

- Title (draft): *A Trickle-Down Bracket on the $k$-WL Skeleton*.
- Alt: *Quantitative $k$-WL: A Two-Sided Bracket and its Slack Constant*.
- Repo: `kwl-bracket/` (sibling to `partition-sandwich-preprint/`).
- Verification: `verify-kwl.jl` + `KWLBracket.lean`.
- Cross-citation: preprint = elementary $k=1$ case; this paper
  cited from preprint's "Future work" once it lands.

## Step 12 — Immediate next actions

1. **Literature sweep** (Step 9 / K3). Search $k$-WL ∩ HDX, WL ∩
   Garland, GI ∩ trickle-down. ~20 papers, ~2 hours of reading.
   Output: a one-page note here in `future-work/` confirming or
   killing T-A's novelty.
2. **Step-4 empirical check.** Output: `step4_trickle_check.json`
   plus verdict.
3. *Only if both pass:* open `kwl-bracket/`, copy preprint
   `Makefile` and `verify.jl` skeleton, draft T-A in LaTeX, begin
   Step 10.

---

## Pitfall → angle defusion map (preserved from analysis)

| Pitfall in preprint                  | Angle that defuses it (this paper or future) |
|---|---|
| Fano repackaging                     | BFA hypercontractivity (deferred to paper 3) |
| CART/LR tautology in E1/E2           | Property Testing reframing (this paper, §4)  |
| E3 cardinality collapse              | Wigderson structure/pseudorandomness (§7)    |
| Lemma 6′ exponential blow-up         | Kochenderfer safe envelope (deferred)        |
| Sharpness vs Han–Verdú               | HDX trickle-down quantitative (this paper)   |
| $w^\*=0.16$ is large                 | PT optimal-tolerance reframing (§4)          |
| E6-NAS population leak               | Falsification reframe (deferred)             |
| Binary only                          | HDX on $(k-1)$-skeleton + PGM (deferred)     |
| Interior achievability hand-wave     | Boolean library constructive (X2)            |
| Verify $n\le 32$                     | $10^6$ + Lean (X3)                            |

---

## Status

- 2026-06-01: draft written; nothing started.
- Next: execute Step 12.1 + Step 12.2.
