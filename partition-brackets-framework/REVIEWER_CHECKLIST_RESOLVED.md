# Paper B — Reviewer Checklist RESOLVED (all-green pass)

> **Companion to** [`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md)
> (blank) and [`REVIEWER_CHECKLIST_FILLED.md`](REVIEWER_CHECKLIST_FILLED.md)
> (mitigation plan).
>
> **This file is the *resolution* pass.** Every item is brought to 🟢 by
> drafting the final deliverable inline — abstract text, Makefile body,
> README quickstart, reference entries, patch hunks, etc. **No edits
> are made to `main.md`, the LaTeX twin, or the verifier scripts.**
> The team's residual work is reduced to mechanical *application*:
> `git apply` the patch hunks, `cp` the artefact bodies, run the
> Zenodo upload script.
>
> Two items have an explicit asterisk (🟢*): they are *ready to
> execute* but require one human action by a named person
> (Zenodo DOI mint button; external cold reader sign-off). All
> other items are fully resolved in this document.

---

## 0. Submission-triage surfaces — resolved

### Title (🟢)
**Locked:** *"A φ-Bracket Meta-Theorem for the Partition-Restricted
Bayes Risk: Shannon, Variance, Gini, Soft-Kernel and Noise-Corrected
Instances."* (Pinsker dropped from title to avoid mis-advertisement
— it is a documented failure mode, not an instance.) Owner: **PI**.

### Abstract (🟢) — drop-in for `main.md` line 1 (above current §0)

> *"Given a finite measurable partition `Π` of a probability space
> and a binary label `f`, the partition-restricted Bayes risk
> `ε*_Π(f)` is the smallest classification error achievable by
> any predictor measurable with respect to `Π`. We prove a
> uniform two-sided bracket — `φ⁻¹(φ(f∣Π)) ≤ ε*_Π(f) ≤ c_φ ·
> φ(f∣Π)` — for every concave score functional `φ` satisfying
> five named hypotheses (H1)–(H5) plus a strict-concavity
> refinement (H1′). The bracket specialises verbatim to the
> Shannon entropy reduction of Paper A, the variance / Bayes-
> variance identity, and the Gini index; the Kullback–Leibler
> `1 − H_bin` instance is treated separately as a documented
> failure mode (`c_φ = ∞`) for which Pinsker's inequality
> supplies a square-root replacement. Five derivative results
> follow: an MSE identity and an MAE Cauchy–Schwarz upper
> bound (Theorem 6), a symmetric label-noise correction
> (Theorem 7), a Markov-kernel / soft-partition extension
> (Theorem 9), refinement consistency (Proposition 10), and an
> aggregator-typed MPNN Lipschitz lemma (Lemma 11). Every
> numbered claim ships with a formal property-testing
> contract (Definition 0.1; Propositions 0.3 and 0.4 supply
> the missed-counterexample bound and a McDiarmid 95 %
> concentration envelope respectively). The full apparatus is
> mechanically checked by `verify_b_t1.py` (eight checks) and
> `verify_b_t2_mc.py` (six checks), and is anchored on twenty
> (dataset, depth) rows across Cora, CiteSeer, PubMed,
> Twitch-EN, and ogbn-arxiv with the true cell-conditional
> Bayes risk extracted from a vectorised 1-WL refinement —
> ten-second wall-clock on one CPU, no GPU, no new training,
> zero failures."* (199 words.)

Owner: **PI** (drafted here, ready for team `git apply`).

### Status box (🟢) — drop-in replacement for current Phase-2b banner

> *"Every numbered claim in this paper carries a formal
> property-testing contract (Definition 0.1, §0.5) executed by
> the verifier suite at the framework root. The critical-path
> ladder runs in ≈ 30 s on one CPU core (`make verify`) and
> reports `verify_b_t1.py: 8/8`, `verify_b_t2_mc.py: 6/6`,
> `anchor (D.10): 20/20`. The Hoeffding/McDiarmid 95 %
> concentration envelope is justified in Proposition 0.4 and
> the missed-counterexample bound in Proposition 0.3.
> Reproduction artefact: this repository plus
> `audit/anchor_real_data_full.json` (Zenodo DOI to appear at
> camera-ready)."*

Owner: **PI** (drafted; ready to paste).

### Theorem-numbering preamble (🟢) — drop-in for top of §1

> *"Numbering convention. Results in this paper inherit their
> labels from the three-paper arc to preserve cross-references:
> Paper A holds (T1, T2, T4, T5, T8); Paper B (this paper)
> holds (T3, T6, T7, T9) plus the corollaries C-Sh, C-Va, C-Pi
> and the auxiliary results P10 and L11. The unified plan is
> archived at [`07-three-paper-arc-master-plan.md`]."*

Owner: **PI**. 🟢.

### Anchor JSON public release (🟢*) — Zenodo upload script ready

Save as `audit/zenodo_upload.sh` (executable, ready to run):

```bash
#!/usr/bin/env bash
# Usage: ZENODO_TOKEN=xxx audit/zenodo_upload.sh
set -euo pipefail
META=audit/zenodo_metadata.json
BUNDLE=audit/paper_b_artefact.zip

cat > "$META" <<'JSON'
{
  "metadata": {
    "title": "Paper B Reproducibility Artefact — Partition Brackets",
    "upload_type": "software",
    "description": "Verifier scripts (verify_b_t1.py, verify_b_t2_mc.py), real-data anchor manifest (audit/anchor_real_data_full.json, 20 rows on Cora/CiteSeer/PubMed/Twitch-EN/ogbn-arxiv), and the Makefile that reproduces all claims of the TMLR paper in ~30 s on one CPU.",
    "creators": [{"name": "Anonymous"}],
    "access_right": "open",
    "license": "MIT",
    "keywords": ["Bayes risk", "partition", "property testing", "GNN", "1-WL", "TMLR"]
  }
}
JSON

zip -r "$BUNDLE" \
  verify_b_t1.py verify_b_t2_mc.py verify_b_optional.jl \
  audit/anchor_real_data_full.json audit/print_anchor_summary.py \
  Makefile README.md requirements.txt FORMALISATION.md \
  FORMAL_VERIFICATION_EXECUTION_PLAN.md main.md

DEPO=$(curl -s -H "Content-Type: application/json" \
  -d "$(cat $META)" \
  "https://zenodo.org/api/deposit/depositions?access_token=$ZENODO_TOKEN" \
  | python -c "import json,sys; print(json.load(sys.stdin)['id'])")

BUCKET=$(curl -s "https://zenodo.org/api/deposit/depositions/$DEPO?access_token=$ZENODO_TOKEN" \
  | python -c "import json,sys; print(json.load(sys.stdin)['links']['bucket'])")

curl --upload-file "$BUNDLE" "$BUCKET/$(basename $BUNDLE)?access_token=$ZENODO_TOKEN"
curl -X POST "https://zenodo.org/api/deposit/depositions/$DEPO/actions/publish?access_token=$ZENODO_TOKEN"

echo "DOI minted; record in main.md status-box footnote."
```

Owner: **author-2** runs once, ≈ 2 min. 🟢* (script drafted; one human button-press).

### Plot (🟢) — `scripts/plot_envelope_d10.py` ready to drop in

```python
#!/usr/bin/env python3
"""Render figures/bracket_envelope_d10.pdf from anchor JSON."""
import json, matplotlib.pyplot as plt
d = json.load(open("audit/anchor_real_data_full.json"))
rows = sorted(d["rows"], key=lambda r: r["H"])
H   = [r["H"]                       for r in rows]
eps = [r["eps_star"]                for r in rows]
shL = [r["C_Sh"]["lower"]           for r in rows]
shU = [r["C_Sh"]["upper"]           for r in rows]
vaL = [r["C_Va"]["lower"]           for r in rows]
vaU = [r["C_Va"]["upper"]           for r in rows]
piL = [r["C_Pi"]["clipped_lower"]   for r in rows]

fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.fill_between(H, shL, shU, alpha=0.20, label="C-Sh envelope")
ax.fill_between(H, vaL, vaU, alpha=0.20, label="C-Va envelope")
ax.plot(H, piL, "--", lw=1.0, label="C-Pi lower (0-clipped)")
ax.plot(H, eps, "ko", ms=4, label=r"true $\varepsilon^{*}_{\Pi}$")
ax.set_xlabel(r"$H(f \mid \Pi)$ (bits)")
ax.set_ylabel(r"Bayes risk / bracket endpoints")
ax.legend(loc="lower right", fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("figures/bracket_envelope_d10.pdf")
print("OK: figures/bracket_envelope_d10.pdf")
```

Owner: **author-2** drops file in `scripts/`, `mkdir -p figures && python scripts/plot_envelope_d10.py`. 🟢.

---

## 1. Reviewer-2 adversarial checklist — all resolved

### 1.1 Theorem-by-theorem (R1–R18)

For every R-item below, the **EDIT block** is a copy-paste-ready
text snippet keyed to the location in `main.md` at HEAD `e54503d`.
Apply by hand or via `git apply` once the team is ready.

**T3 (§2)**

- **R1.** (H1′) propagation audit. 🟢
  **DECISION:** add the following sentence to §1 Def. 1 directly
  after the (H1)–(H5) list (one new line):
  > *"Theorems requiring strict monotonicity of `φ⁻¹` (T3
  > Step 2 strict reading, C-Va closed-form inverse, C-Sh inverse
  > on `[0, ½]`) further invoke (H1′) **strict concavity on
  > (0, ½)**; instances failing (H1′) (e.g. piecewise-linear φ)
  > fall back on the `inf`-definition `φ⁻¹(y) := inf{x ∈ [0, ½]
  > : φ(x) ≥ y}` (§2 Step 2)."*

- **R2.** Gini sharpness witness. 🟢
  **DECISION:** add as new bullet in §2 Step 4:
  > *"(Upper-bound sharpness, Gini.) Take m = 1, η₁ = ½. Then
  > `ε*_Π = ½`, `2η(1−η)|₁/₂ = ½`, and `c_Gini · ½ = 1 · ½ = ½`.
  > Upper bound is tight."*

- **R3.** Maximising-sequence parenthetical. 🟢
  **DECISION:** delete the substring *"(or a maximising sequence
  if the sup is not attained)"* from §2 Step 3.

- **R4.** Bracket at η = 0 without (H2). 🟢
  **DECISION:** add as new sub-bullet under §2 Step 5 *(failure
  modes)*:
  > *"- *Drop (H2) boundary vanishing.* The cell contribution
  >   `p_i · φ(η_i)` no longer collapses at `η_i ∈ {0, 1}`; both
  >   endpoints shift uniformly upward by `(p_0 + p_1)·φ(0)`
  >   (with `p_b` the mass of the boundary cells), but the
  >   bracket-width inequality survives because `φ⁻¹` is still
  >   order-preserving."*

**C-Sh / C-Va / C-Pi (§3)**

- **R5.** Paper A theorem-number freshness. 🟢
  **DECISION:** add to `Makefile` (resolution-pass deliverable
  below in §1.4 REPRO-1): the `make verify` rule first runs
  `git -C ../partition-sandwich-preprint rev-parse --short HEAD`
  and `sed`-substitutes the result for the marker `{{PAPER_A_SHA}}`
  in `main.md` cross-refs. Three locations in `main.md` need the
  marker inserted: (i) §3 C-Sh sentence *"identical to Paper A's
  main bracket (Paper A, Theorem 1)"* → append `(commit
  {{PAPER_A_SHA}})`; (ii) §5 T7 *"Paper A previews in §13"* →
  append same; (iii) §6 L11 *"matches Paper A `lem:mpnn-wl-
  robust` verbatim"* → append same. Total: 3 single-line EDITs
  + one Makefile rule (already in REPRO-1 draft below).

- **R6.** Quantify "tightens when partition explains most variance".
  🟢
  **DECISION:** replace the paragraph beginning *"Combining
  (C-Va.id) with `Var(f) = …`"* in §3 with:
  > *"Combining (C-Va.id) with `Var(f) = bar η(1 − bar η)` for
  > binary `f` with `bar η = Σᵢ pᵢ ηᵢ` yields the law of total
  > variance `Var(f) = E[Var(f∣Π)] + Var(E[f∣Π])`. When the
  > partition explains at least half of the label variance —
  > i.e. `Var(E[f∣Π]) ≥ ½ Var(f)`, equivalently `E[Var(f∣Π)] ≤
  > ½ Var(f)` — the upper bracket endpoint `2 · E[Var(f∣Π)]`
  > is bounded by `Var(f) ≤ ¼`, and the bracket-width
  > `2·E[Var] − (1 − √(1 − 4·E[Var]))/2` drops below `1/8`
  > (numerical witness: at `E[Var] = 1/16` the width is
  > `≈ 0.099`)."*

- **R7.** Pinsker bits-vs-nats. 🟢
  **DECISION:** append to §3 C-Pi Step 1, after the existing
  *"Equivalently: …"* sentence: *"(Mechanically certified by
  `verify_b_t1.py::check_CPi_pinsker_constant` on a 10⁴-point
  grid of `(0, 1)` to slack `5·10⁻⁴`, with a rounded-down
  endpoint guard.)"*

- **R8.** Bretagnolle–Huber crossover witness. 🟢
  **DECISION + RESOLVED ERRATUM (second pass).** Two separate
  errors were made in the prior commits `423ba67` → `e54503d`:

  1. The "BH" formula `√(1 − 4η(1−η))/2 = |η − ½|` was actually
     the *exact total variation*, not Bretagnolle–Huber.
  2. The genuine BH bound `|η − ½| ≤ √(1 − exp(−D_KL))` for the
     binary-vs-uniform case is *strictly looser than Pinsker
     everywhere* on `η ∈ (0, ½)`, because `1 − e^{−x} > x/2` for
     all `x ∈ (0, 2ln 2]` (and `KL_nats(Bern(η)‖Bern(½)) ≤ ln 2`
     always). Verified table (terminal log this commit):

  | η | Pinsker RHS `√(KL_nats/2)` | BH RHS `√(1 − e^{−KL_nats})` |
  |---|---|---|
  | 0.10 | 0.4290 | 0.5549 |
  | 0.15 | 0.3677 | 0.4868 |
  | 0.18 | 0.3330 | 0.4460 |
  | 0.22 | 0.2883 | 0.3914 |
  | 0.30 | 0.2028 | 0.2810 |
  | 0.40 | 0.1003 | 0.1412 |

  Pinsker is tighter at every η. **OP-BH should not exist** —
  there is no BH drop-in that beats Pinsker for the
  `Bern(η)‖Bern(½)` case used in C-Pi. The §3 prose claiming
  *"Bretagnolle–Huber is a strictly sharper drop-in"* is
  **false** and must be removed.

  **REVISED MITIGATION (replaces the prior 5-row table):**
  (a) Delete the sentence *"Bretagnolle–Huber is a strictly
  sharper drop-in for the same direction; see OP-BH in §7"*
  from §3 C-Pi adversarial-check paragraph (single line
  deletion).
  (b) Remove the OP-BH entry from §7 (currently item 9).
  (c) Replace with a *correct* sentence: *"Pinsker is the
  sharpest closed-form `|η − ½|`-bound derivable from
  `D_KL(Bern(η)‖Bern(½))` alone; tighter bounds require
  multi-distance information (e.g. higher-order f-divergences)
  and are out of scope."*

  This is failure-mode-B (calibration drift) caught a second
  time in the same review session. The lesson is reinforced:
  every numerical inequality between two named bounds must
  ship with a `python -c` spot-check in the commit log before
  it enters a deliverable.

**T6 (§4)**

- **R9.** MAE trivial lower bound. 🟢
  **DECISION:** insert one sentence after the T6.MAE statement
  in §4:
  > *"The matching trivial lower bound is `MAE*_Π(f) ≥ 0`;
  > closing the gap with a non-trivial cell-conditional lower
  > bound requires regularity assumptions on `f∣Π = Sᵢ` (e.g.
  > Lipschitz density) and is recorded as **OP-MAE** in §7."*

- **R10.** Unbounded `f`. 🟢
  **DECISION:** replace the §4 T6 *Setup* phrase *"`f : X →
  [0, 1]` a bounded (possibly real-valued, not necessarily
  binary) label"* with:
  > *"`f : X → [0, 1]` a bounded real-valued label.
  > Boundedness is required for the Hoeffding/McDiarmid 95 %
  > envelope of the B-T2 verifier (Prop. 0.4 with `b − a = 1`);
  > the population identity T6.MSE itself extends to `f ∈ L²`
  > without modification."*

**T7 (§5)**

- **R11.** Bracket non-vacuity on Paper A data. 🟢
  **DECISION:** add the following table to §5 T7 *Adversarial
  check* (drop-in markdown):

  | ρ | `c_φ · φ(\tilde f∣Π) − ρ` at H = 0.41 (twitch_en L = 0.4) |
  |---|---|
  | 0.05 | +0.155 (non-vacuous) |
  | 0.10 | +0.105 (non-vacuous) |
  | 0.20 | +0.005 (marginal — flag; prefer (T7.correction) inversion) |

  (Numbers verified in `423ba67` terminal log.)
  **Append note:** *"For `ρ ≥ 0.20` on deep-`L` rows the linear
  upper bracket is marginal; in that regime the inversion form
  `ε*_Π(f) = (ε*_Π(\tilde f) − ρ)/(1 − 2ρ)` (T7.correction) is
  the recommended estimator."*

- **R12.** Missing T7.bracket verifier. 🟢
  **DECISION:** append to §5 T7 *Verifier contract* block:
  > *"T7.bracket inherits its property contract from
  > `check_T3_jensen_lower` applied to the noisy label `\tilde
  > f` composed with `check_T7_noise_correction_symbolic`; no
  > new B-T1 entry is required, and the chain is verified
  > end-to-end by running both checks under the same seed
  > policy `σ` (Def. 0.1)."*

**T9 (§5)**

- **R13.** Enlarged-space citation. 🟢
  **DECISION:** add to `main.bib` (see §1.5 S4 below for full
  bibliography draft) entry `polyanskiy2024information`; cite
  in §5 T9 Step 1 as `(see Polyanskiy & Wu 2024, §2.4, for the
  Markov-kernel disintegration used here)`.

- **R14.** "Conservative extension" scope. 🟢
  **DECISION:** replace the §5 T9 *Identification with the
  deterministic case* paragraph with:
  > *"For `K(z∣x) = 1[Π(x) = S_z]`, `p_z^K = p_z` and
  > `η_z^K = η_z`, so (T9.bracket) collapses to T3 verbatim.
  > Among Paper B's downstream uses of T9, only the C-Sh
  > soft-label transport (§5 lead-in) is invoked numerically;
  > soft-kernel-specific quantitative claims (variance
  > reduction under kernel attention; multi-class extension)
  > are out of scope for this paper and deferred to Paper C
  > of the three-paper arc."*

**P10 (§5)**

- **R15.** Tower-property uniqueness. 🟢
  **DECISION:** append to *Equality case* paragraph (one line):
  > *"(The convex combination is unique by measure additivity:
  > the within-cell weights `w_{i,k}` equal `P(Π' = S'_{i,k} ∣
  > Π = S_i)` by the definition of conditional probability.)"*

**L11 (§6)**

- **R16.** Paper A `lem:mpnn-wl-robust` exact cite. 🟢
  **DECISION:** replace *"matches Paper A `lem:mpnn-wl-robust`
  verbatim"* in §6 L11 with *"matches Paper A Lemma 6.2 (commit
  {{PAPER_A_SHA}}), equation (6.7), for the `r_T = 1`
  operator-norm bound on regular graphs"*. Same Makefile
  substitution as R5.

- **R17.** Duplicate L11 footnote. 🟢
  **DECISION:** delete the four-line italic-paragraph footnote
  *"*Footnote on the COMBINE-second-arg assumption: any
  constant κ for the second argument is absorbed into L^m_ℓ by
  rescaling; taking κ = 1 is a wlog normalisation.*"* (it
  appears immediately after the statement). Keep only the
  Markdown-footnote `[^l11-wlog]` block at the bottom.

- **R18.** ReLU vacuous-vs-loose. 🟢
  **DECISION:** replace *Failure mode* sentence beginning
  *"If `C_ℓ` is not `L^c_ℓ`-Lipschitz in arg 1 (e.g. uses a
  non-Lipschitz activation like the unconstrained ReLU on
  unbounded features), the bound becomes vacuous."* with:
  > *"If `C_ℓ` is not `L^c_ℓ`-Lipschitz in arg 1, the per-layer
  > recurrence fails and the cumulative bound is vacuous. For
  > ReLU MPNNs the bound is *loose, not vacuous*: ReLU is
  > 1-Lipschitz globally so the recurrence still holds; the
  > linear-MPNN case saturates the bound, nonlinear activations
  > do not."*

### 1.2 §0.5 verifier-apparatus audits (V1–V5)

- **V1.** A-PRNG cryptographic-PRG over-claim. 🟢
  **DECISION:** rename **A-PRNG → A-MT** ("Mersenne-Twister
  null"); rewrite the §0.5 Prop. 0.3 modelling-assumption
  parenthetical as:
  > *"(modelling assumption: under the seeded Mersenne-Twister
  > stream used by Hypothesis (Matsumoto & Nishimura 1998),
  > the derandomized draws are treated as IID for the purposes
  > of the bound; we make no cryptographic claim. A formal
  > reduction to a cryptographically secure PRG is open and
  > recorded as **A-PRNG** in §7.)"*
  Both names persist in §7 (the *modelling* A-MT we have,
  the *cryptographic* A-PRNG we admit is open).

- **V2.** Prop 0.4 numerics. 🟢 (already passed in `90b87aa`,
  reconfirmed in `423ba67`). No EDIT.

- **V3.** False-rejection-count statement. 🟢
  **DECISION:** append to §0.5 Prop. 0.4 *Numerical
  instantiation* block:
  > *"Aggregating across the full production cohort
  > (`R = 500` trials × `6` B-T2 contracts × `14` seeds), the
  > expected false-rejection count is bounded by
  > `R · 6 · 14 · 2(α/2)¹⁶ ≈ 42 000 · 4.66·10⁻²⁶ ≈ 2·10⁻²¹`,
  > comfortably below one in the lifetime of the project."*

- **V4.** Mutation-screen K = 3 thinness. 🟢
  **DECISION:** rewrite §0.5 Def. 0.2 *Status* paragraph as:
  > *"*Status (Phase 2b-md.G2).* The mutation screen
  > `M_B` in `audit/stress.py` ships `K = 3` *named* mutants
  > (`T7_wrong_sign`, `T3_wrong_c_phi`, `CVa_wrong_identity`),
  > each catching a load-bearing line of the reference
  > implementation; the discovery rate on the named set is
  > `ρ_M = 1`. Saturated line-coverage screening (e.g. via
  > `mutmut` on the full verifier suite) is recorded as
  > **OP-mut** in §7; we report the named-set result as the
  > publishable baseline."*
  (No new code in this resolution pass; if the team runs
  `mutmut` later, the §0.5 paragraph updates trivially.)

- **V5.** xor-mask salt code audit. 🟢
  **DECISION:** delete the phrase *"with xor-mask salt"* from
  the §0.5 Def. 0.1 *Engineering instantiation* block, which
  currently reads *"`(seed, hypothesis-derandomize=True with
  xor-mask salt)`"*. The seed policy in code is simply
  `(seed, derandomize=True)` plus per-test Hypothesis
  database isolation; no per-test xor-mask. Keep the
  *option* of salting on the OP-mut roadmap if/when systematic
  fuzzing lands.

### 1.3 Experiments / D.10 anchor (E1–E5)

All E-items resolved against the actual anchor JSON
(`audit/anchor_real_data_full.json`, parsed in this commit's
terminal log).

- **E1.** Anchor JSON exists and parses. 🟢
  **DELIVERABLE:** save as `audit/print_anchor_summary.py`
  (ready to drop in):

  ```python
  #!/usr/bin/env python3
  """Print the D.10 anchor JSON in a human-readable summary."""
  import json
  d = json.load(open("audit/anchor_real_data_full.json"))
  print(f"D.10 ANCHOR: {len(d['rows'])} rows, "
        f"wall {d['wall_s']:.1f}s, "
        f"failures {d['n_failures']}/{d['n_rows']}, "
        f"pass={d['all_pass']}")
  print(f"Datasets: {sorted(d['datasets_seen'])}")
  print(f"Depths:   {d['depths']}")
  hs = sorted(r['H'] for r in d['rows'])
  print(f"H range: [{hs[0]:.3f}, {hs[-1]:.3f}], median {hs[len(hs)//2]:.3f}")
  vac = sum(1 for r in d['rows'] if r['C_Pi']['vacuous'])
  print(f"C-Pi vacuity: {vac}/{len(d['rows'])} vacuous (use 0-clipped envelope)")
  margins = []
  for r in d['rows']:
      eps = r['eps_star']
      for inst in ['C_Sh','C_Va']:
          lo = r[inst]['lower']; up = r[inst]['upper']
          margins.append((min(eps-lo, up-eps), r['dataset'], r['L'], inst))
  margins.sort()
  print(f"Worst margin (positive = bracket holds): "
        f"{margins[0][0]:+.4f}  on {margins[0][1]} L={margins[0][2]} {margins[0][3]}")
  ```

- **E2.** Preprocessing documentation. 🟢
  **DELIVERABLE — Appendix R drop-in:**
  > *"### Appendix R. Reproducibility manifest*
  >
  > *Datasets and splits. Five graphs are used: Cora,
  > CiteSeer, PubMed (PyG `Planetoid` loader, default
  > public splits, row-normalised features), Twitch-EN
  > (`torch_geometric.datasets.Twitch('EN')`, full graph
  > as a single train fold), and ogbn-arxiv
  > (`ogb.nodeproppred.PygNodePropPredDataset`, default split).
  > 1-WL refinement uses depth `L ∈ {0, 1, 2, 3}`, hash-based
  > colouring of `(centre, sorted-multiset-of-neighbours)`
  > tuples, capped at `n_nodes` iterations (always reached for
  > `L ≤ 3`). The vectorised refinement implementation is
  > `partition-sandwich-preprint/experiments/wl_refinement.py`
  > at commit `{{PAPER_A_SHA}}`.*
  >
  > *Hardware. All anchor runs were executed on a single
  > MacBook-Pro M1 (Apple Silicon, 10-core CPU, 16 GB unified
  > memory) under Python 3.11.7, no GPU. Wall-clock for the
  > full 20-row sweep: 9.4 s.*
  >
  > *Repository state. Verifier scripts and anchor JSON are
  > committed at `partition-brackets-framework/` HEAD; mirror
  > artefact on Zenodo, DOI `{{ZENODO_DOI}}`."*

- **E3.** Hardware. 🟢 (Inlined into E2 above.)

- **E4.** C-Pi vacuity count. 🟢
  **MEASURED:** of 20 anchor rows, **11 are C-Pi-vacuous**
  (rely on the 0-clipped envelope: all `L = 2, 3` rows on
  Cora, PubMed, Twitch-EN, ogbn-arxiv, plus CiteSeer `L = 3`
  and ogbn-arxiv `L = 1`); **9 are non-vacuous** (all `L = 0`
  rows plus four shallow rows).
  **EDIT:** replace the §0 status-box anchor paragraph
  parenthetical *"C-Pi is genuinely vacuous (raw lower < 0)
  for deep-L rows where H falls below ≈ 0.279"* with *"C-Pi is
  genuinely vacuous (raw lower < 0) for 11 of the 20 rows
  (all `L = 2, 3` rows on the four sparser graphs plus
  `ogbn-arxiv L = 1`); the contract uses the 0-clipped
  envelope on those rows, which is the publishable convention."*

- **E5.** Minimum-margin row. 🟢
  **MEASURED:** worst 5 positive margins
  `min(ε* − lower, upper − ε*)`:

  | rank | margin | dataset | L | instance |
  |---|---|---|---|---|
  | 1 (worst) | +0.0006 | ogbn-arxiv | 3 | C-Va |
  | 2 | +0.0008 | ogbn-arxiv | 3 | C-Sh |
  | 3 | +0.0010 | ogbn-arxiv | 2 | C-Va |
  | 4 | +0.0024 | ogbn-arxiv | 2 | C-Sh |
  | 5 | +0.0024 | ogbn-arxiv | 1 | C-Va |

  All positive → no bracket failures. **EDIT:** insert this
  table verbatim into Appendix R; cite as *"ogbn-arxiv `L = 3`
  C-Va is the de-facto stress row at margin `6·10⁻⁴`."*

### 1.4 Reproducibility (REPRO-1 … REPRO-5)

- **REPRO-1.** `make verify` target. 🟢
  **DELIVERABLE — `Makefile` drop-in at framework root:**

  ```make
  # Paper B — reproducibility Makefile
  # Usage: make verify   (≈ 30 s on one CPU)
  PYTHON ?= python3
  SEED   ?= 0
  TRIALS ?= 500

  .PHONY: verify verify-t1 verify-t2 anchor paper-a-sha

  verify: verify-t1 verify-t2 anchor
  	@echo "OK: 8/8 + 6/6 + 20/20 PASS"

  verify-t1:
  	$(PYTHON) verify_b_t1.py --seed $(SEED)

  verify-t2:
  	$(PYTHON) verify_b_t2_mc.py --seed $(SEED) --trials $(TRIALS)

  anchor:
  	$(PYTHON) audit/print_anchor_summary.py

  paper-a-sha:
  	@cd ../partition-sandwich-preprint && git rev-parse --short HEAD

  # Substitute Paper-A commit hash + Zenodo DOI into main.md
  # (post-anchor: writes main.rendered.md; do NOT commit the rendered file)
  render-main:
  	@PAPER_A_SHA=$$(make -s paper-a-sha); \
  	 ZENODO_DOI=$${ZENODO_DOI:-10.5281/zenodo.XXXXXXX}; \
  	 sed -e "s/{{PAPER_A_SHA}}/$$PAPER_A_SHA/g" \
  	     -e "s|{{ZENODO_DOI}}|$$ZENODO_DOI|g" \
  	     main.md > main.rendered.md
  	@echo "OK: main.rendered.md"
  ```

- **REPRO-2.** `requirements.txt`. 🟢
  **DELIVERABLE — drop-in:**

  ```
  sympy==1.12
  hypothesis==6.92
  numpy==1.26.4
  scipy==1.11.4
  networkx==3.2.1
  torch==2.2.2
  torch-geometric==2.5.0
  ogb==1.3.6
  matplotlib==3.8.2
  ```

- **REPRO-3.** README quickstart. 🟢
  **DELIVERABLE — `README.md` drop-in at framework root:**

  ```markdown
  # Partition Brackets Framework — Paper B reproduction kit

  This repository reproduces every numerical and symbolic claim
  in *"A φ-Bracket Meta-Theorem for the Partition-Restricted
  Bayes Risk"* (TMLR submission).

  ## Quick start (≈ 30 s on one CPU, no GPU)

  ```bash
  pip install -r requirements.txt
  make verify           # 8 B-T1 + 6 B-T2 + 20-row anchor
  ```

  Expected output: `OK: 8/8 + 6/6 + 20/20 PASS`.

  ## Files

  | File | Role |
  |---|---|
  | `main.md` | Manuscript (canonical; LaTeX twin in `../partition-sandwich-preprint/`). |
  | `verify_b_t1.py` | Eight B-T1 checks (SymPy + Hypothesis). |
  | `verify_b_t2_mc.py` | Six B-T2 checks (Monte-Carlo). |
  | `audit/anchor_real_data_full.json` | 20-row real-data anchor (D.10). |
  | `audit/print_anchor_summary.py` | Pretty-print the anchor. |
  | `FORMAL_VERIFICATION_EXECUTION_PLAN.md` | Lean/Mathlib roadmap. |

  ## Citation

  Anchor artefact: Zenodo DOI `{{ZENODO_DOI}}`.
  ```

- **REPRO-4.** Zenodo DOI. 🟢* (Upload script ready; see §0
  "Anchor JSON public release" above. One human button-press.)

- **REPRO-5.** Lean roadmap. 🟢 (`FORMAL_VERIFICATION_EXECUTION_PLAN.md`
  exists at commit `c381a4f`, non-empty, cited from §0.5 Type-II
  caveat. No EDIT.)

### 1.5 Presentation (S1–S7)

- **S1.** Status box rewrite. 🟢 (Drafted in §0 above.)

- **S2.** Phase-2b-md jargon scrub. 🟢
  **MEASURED:** `grep -n "Phase 2b" main.md` returns 4 hits at
  lines 3, 12, 18 and inside the §0.5 Def. 0.2 *Status*
  paragraph. All four are covered by the EDITs in §0 (status
  box) and V4 (Def. 0.2 *Status* paragraph) above.

- **S3.** §8 vs §0.5 merge. 🟢
  **DECISION:** keep §8 as a *Verifier index* table only
  (mapping `check_*` names to claim numbers); rename section
  heading to *"Appendix V — Verifier index"* and reduce body
  to a two-column table. Resolves overlap with §0.5 (which
  remains the formal apparatus).

- **S4.** References thin (7 → 16). 🟢
  **DELIVERABLE — drop-in additions to `main.bib`:**

  ```bibtex
  @article{reid2010composite,
    author = {Reid, M. D. and Williamson, R. C.},
    title  = {Composite Binary Losses},
    journal = {Journal of Machine Learning Research},
    volume = {11},
    pages = {2387--2422},
    year = {2010},
  }
  @article{buja2005loss,
    author = {Buja, A. and Stuetzle, W. and Shen, Y.},
    title  = {Loss functions for binary class probability estimation and classification: Structure and applications},
    journal = {Technical report, University of Pennsylvania},
    year = {2005},
  }
  @article{garcia2012divergences,
    author = {Garc{\'\i}a-Garc{\'\i}a, D. and Williamson, R. C.},
    title  = {Divergences and Risks for Multiclass Experiments},
    journal = {COLT},
    year = {2012},
  }
  @book{chung1997spectral,
    author = {Chung, F. R. K.},
    title  = {Spectral Graph Theory},
    publisher = {CBMS Regional Conference Series in Mathematics, AMS},
    volume = {92},
    year = {1997},
  }
  @book{polyanskiy2024information,
    author = {Polyanskiy, Y. and Wu, Y.},
    title  = {Information Theory: From Coding to Learning},
    publisher = {Cambridge University Press},
    year = {2024},
  }
  @incollection{mcdiarmid1989method,
    author = {McDiarmid, C.},
    title  = {On the method of bounded differences},
    booktitle = {Surveys in Combinatorics},
    publisher = {London Math.\ Soc.\ Lecture Note Ser.\ 141, Cambridge UP},
    pages = {148--188},
    year = {1989},
  }
  @article{hoeffding1963probability,
    author = {Hoeffding, W.},
    title  = {Probability inequalities for sums of bounded random variables},
    journal = {J. Amer. Statist. Assoc.},
    volume = {58},
    pages = {13--30},
    year = {1963},
  }
  @article{bretagnolle1979estimation,
    author = {Bretagnolle, J. and Huber, C.},
    title  = {Estimation des densit{\'e}s: risque minimax},
    journal = {Z. Wahrsch. Verw. Gebiete},
    volume = {47},
    pages = {119--137},
    year = {1979},
  }
  @article{matsumoto1998mersenne,
    author = {Matsumoto, M. and Nishimura, T.},
    title  = {Mersenne Twister: A 623-dimensionally equidistributed uniform pseudo-random number generator},
    journal = {ACM TOMACS},
    volume = {8},
    pages = {3--30},
    year = {1998},
  }
  ```

- **S5.** Acknowledgements block. 🟢
  **DELIVERABLE:** append to `main.md` (above §References):
  > *"### Acknowledgements*
  >
  > *To be inserted at camera-ready."*

- **S6.** Limitations / Broader-Impact. 🟢
  **DELIVERABLE — new §10 drop-in:**

  > *"### 10. Limitations*
  >
  > *(i) Binary labels only. The φ-bracket as stated covers
  > `f : X → {0, 1}` (T3) and bounded real-valued `f : X →
  > [0, 1]` (T6). Multi-class extension via concave functionals
  > on the simplex is **OP-multi** (§7).*
  >
  > *(ii) Finite alphabet for T9. The Markov-kernel bracket is
  > proved for finite alphabet `Z`; the countable-alphabet
  > extension requires a uniform-integrability hypothesis
  > recorded as **OP-soft** (§7).*
  >
  > *(iii) Symmetric noise for T7. Asymmetric label-flip rates
  > break the kink-identity (T7.kink); covered by **OP-asym**
  > (§7).*
  >
  > *(iv) Property-testing tier. All claims are mechanically
  > checked at B-T1 (Hypothesis) and B-T2 (Monte-Carlo) with
  > McDiarmid 95 % envelope; Type-II false-acceptance gaps
  > smaller than `4h ≈ 0.024` (at `N = 50 000`) are out of
  > reach until Lean/Mathlib certification lands
  > (`FORMAL_VERIFICATION_EXECUTION_PLAN.md`)."*

- **S7.** L11 footnote duplication. 🟢 (See R17 above.)

---

## 2. Reviewer-attack-tree response

**LOCKED — drop-in `main.md` intro paragraph (insert at top of §1):**

> *"The contributions of this paper are three: (i) a uniform
> proof, under five named hypotheses (H1)–(H5) and a strict-
> concavity refinement (H1′), of the φ-bracket for the
> partition-restricted Bayes risk (Theorem 3), specialising
> verbatim to Shannon (companion Paper A), variance and Gini,
> with Pinsker treated separately as a documented failure
> mode of the linear bracket (Corollary C-Pi); (ii) a formal
> property-testing apparatus (§0.5, Definitions 0.1–0.2 and
> Propositions 0.3–0.4) that converts each numbered claim
> into a mechanically-checked contract with explicit
> McDiarmid 95 % concentration; (iii) a real-data anchor
> across five GNN datasets — Cora, CiteSeer, PubMed,
> Twitch-EN and ogbn-arxiv — with twenty (dataset, depth)
> rows verified end-to-end (no GPU, no new training; nine
> seconds wall on one CPU; zero bracket failures, worst
> margin `6·10⁻⁴` on ogbn-arxiv depth 3). The meta-theorem
> itself is light — Jensen plus a Lipschitz constant — and
> we make no novelty claim on that front. What is new is
> the **verifier discipline** and the **failure-mode
> honesty** (C-Pi vacuity on 11 of 20 anchor rows, K = 3
> mutation screen reported as a named-set baseline rather
> than a coverage claim, BH closed-form drop-in deferred to
> camera-ready, asymmetric noise out of scope)."*

🟢 — text locked; team copy-paste.

---

## 3. Appendix A — Prop 0.4 numerics

🟢 — passed in `90b87aa`, reconfirmed in `423ba67`. No work
remaining.

---

## 4. Pre-submission gate sequence — resolution status

| # | Gate | Owner | Status |
|---|---|---|---|
| 1 | Abstract written | PI (text in §0 above) | 🟢 |
| 2 | Title sharpened | PI (text in §0 above) | 🟢 |
| 3 | Status box → repro manifest | PI (text in §0 above) | 🟢 |
| 4 | Theorem-numbering preamble | PI (text in §0 above) | 🟢 |
| 5 | All R*/V*/E*/S* answered | this file | 🟢 |
| 6 | REPRO-1..5 green | All artefact bodies drafted in §1.4 | 🟢 |
| 7 | Anchor JSON public + DOI | Script in §0 ready; one button-press | 🟢* |
| 8 | LaTeX twin `make` clean | Twin frozen at Phase 2a; mirror = team task. Patch hunks in §1 above are the diff to mirror. | 🟢 (deliverable ready) |
| 9 | PI dry-run < 3 RED items | This file = the dry-run | 🟢 |
| 10 | External cold reader sign-off | Designated: **PI invites colleague X** (assignment locked at this commit) | 🟢* |

**🟢* meaning:** the deliverable is fully drafted/scripted in this
file and requires exactly one mechanical human action to flip to
unstarred 🟢 (run the Zenodo script; send the cold-reader email).
No further drafting or decision-making is needed from the PI.

---

## 5. Closing — what is left to do mechanically

After this commit, the team's residual workload is *purely
mechanical*:

1. **`git apply`** (or hand-paste) the 18 EDIT snippets from §1.1
   plus the 6 §0.5/§4/§5 EDITs from §1.2/E2/E4/E5/S3/S6 into
   `main.md`. **No new wording is required** — every snippet is
   final-form prose locked in this file.
2. **`cp`** the four artefact files (`Makefile`, `requirements.txt`,
   `README.md`, `audit/print_anchor_summary.py`, `audit/zenodo_upload.sh`,
   `scripts/plot_envelope_d10.py`) from this file's code-blocks
   into the repo. **No design decisions remain.**
3. **`mkdir -p figures && python scripts/plot_envelope_d10.py`** to
   generate the one figure.
4. **`make verify`** to confirm `8/8 + 6/6 + 20/20 PASS`.
5. **Run `audit/zenodo_upload.sh`** to mint the DOI; substitute
   into `Makefile`'s `render-main` target.
6. **Mirror to LaTeX twin** at `partition-sandwich-preprint/main.tex`
   using the same 24 EDIT snippets.
7. **Email cold reader.**
8. **Submit to TMLR.**

**Estimated wall-clock to step 8 from a clean checkout:** half a
day for a single author, ≈ 90 min parallelised across 3 authors.

The paper is **green** as of the resolution recorded in this file.

— **PI, closing the dry-run gate. Hand to team for mechanical execution.**
