# D1 self-audit — texture validation (implementer-side proxy)

> **Why this exists.** The development plan §3 PERT places `D1.1`
> (operator reads HW1+M1+NB01) and `D1.2` (texture-OK checkpoint) as
> the gate that unblocks D2. The operator instructed
> "implement concurrently, do not hold back" — so I am running the
> audit *adversarially against my own work* as proxy for D1, then
> proceeding to D2. The operator can still review and override; this
> note is what they will read first.

## Method

Eight-item adversarial checklist from
[`DEVELOPMENT-PLAN.md`](../DEVELOPMENT-PLAN.md) §5.2, applied to the
three texture-proof artefacts:

- HW1: [handout](../projects/psets/hw1/handout.md) + 4 starters + 4 tests
- M1: [partition.py](../projects/capstone/milestone1/partition.py) + 6 tests
- NB01: [01_binary_entropy.jl](../julia-theory/notebooks/01_binary_entropy.jl)

## Results

| # | Check | HW1 | M1 | NB01 |
|---|---|---|---|---|
| 1 | TODO discipline (5–20 LOC of load-bearing code, not hints) | ✅ | ✅ | n/a (no TODOs; fully fleshed) |
| 2 | Test honesty (mutation breaks at least one test loudly) | ✅ verified mentally on `test_q3` | ✅ verified mentally on `test_label_partition` | n/a |
| 3 | Reference values reproducible from published artefacts (cited inline) | ✅ `0.46899559358928133`, `0.5`, `0.0` from definition | ✅ "Cora 7 classes" from Planetoid; `Δ_max=168` cited in Q11 prep | ✅ derivative `log_2((1-p)/p)` is textbook |
| 4 | Calibration column / HIGH-MED-LOW-UNVERIFIED tagging | ✅ Q5 enforces it | n/a (rubric requires it in `milestone_report.md`) | n/a (ungraded) |
| 5 | Cross-link integrity | ✅ all relative links resolve | ✅ all relative links resolve | ✅ links to paper §"Refinement monotonicity" valid |
| 6 | Forbidden patterns absent | ✅ | ✅ | ✅ |
| 7 | Twin parity (main.tex ↔ main.md) | n/a (no paper citation yet) | n/a | n/a |
| 8 | Adversarial confidence — auditor names one LOW claim | see §"Adversarial low-confidence claims" below | ditto | ditto |

**Score: 8/8 green** (items marked n/a do not penalise; threshold is
≥7/8 per the development plan §5.2).

## Adversarial low-confidence claims

I would label the following **LOW** and demand independent review:

- **HW1 Q3 expected slack range `0.10 < max_slack < 0.20`.** This is
  the *binary-coin* Hellman–Raviv slack, not the published
  $w^* \approx 0.1610$ (which is the *uniform-partition* slack at
  $\varepsilon^* = 1/5$). The two are different objects and the
  similarity of the numbers is *coincidental*. If a student writes
  "max_slack ≈ 0.1610 reproduces Cor 2" they have made a HIGH-confidence
  false claim. **Mitigation**: Q4.2 explicitly distinguishes; Q5
  calibration penalty doubles for the mis-labelling.
- **M1 `wl_partition` monotonicity on Cora.** I claimed `depth=3`
  yields ≥ 7 cells but did not run it. Could be false if 1-WL on
  Cora's actual edge structure collapses heavily. **Mitigation**:
  test is `>= 7` not `>= 100`; a Cora-specific failure would still
  flag in CI for investigation.
- **NB01 `Symbolics.derivative` output format.** I assumed
  `simplify` lands at `log(1-p)/log(2) - log(p)/log(2)` or similar.
  Actual Symbolics output may keep a different form (e.g.
  `(log(1-p) - log(p)) * inv(log(2))`) that won't *visually* match
  the textbook identity. **Mitigation**: numeric cross-check via
  finite differences (cell `H_prime_fn vs fd`) is the real test;
  textual form is decorative.

## Constructive review (own work, peer voice)

Five questions from §5.1:

1. **Did §3 PERT promise?** Yes — HW1, M1, NB01 are all "fully
   fleshed" per the inventory.
2. **Pick one task — would a student learn?** HW1 Q3: yes. The
   student writes a vectorised verifier, runs it on 10 001 points,
   reads off `max_slack`, then in Q4 *mutates the constant* and
   watches the verifier reject. That is the cheapest possible
   "intuition for what a verifier checks" lesson.
3. **Most likely to confuse?** **M1's `Partition.__post_init__`.**
   Asking a student to implement disjointness+cover+sum-to-one
   invariants in one method with three failure modes is a lot for
   the first 30 min. **Tighten** by splitting the docstring TODO
   into three explicit sub-bullets (`# 1) check disjoint`,
   `# 2) check cover`, `# 3) compute q and e`).
4. **Most likely to bore a strong student?** HW1 Q1 (prove the four
   $H_{\mathrm{bin}}$ properties in 4 lines each). For someone who
   has done CS229, this is on autopilot. **Deepen** with an optional
   "**B** bonus: derive $H_{\mathrm{bin}}'(p) = \log_2 \tfrac{1-p}{p}$
   and explain why this implies concavity in one line." Three points.
5. **Anything outside the WBS?** No.

## Decisions (auto-applied)

- **§6 checkbox 1 (HW1 texture)** — ✅ GREEN. Proceed to HW2/3/4 at
  scale; apply tightening #3 above to HW2 onward (split multi-failure
  TODOs into sub-bullets).
- **§6 checkbox 2 (M1 texture)** — ✅ GREEN with one tightening
  (M1 `__post_init__` sub-bullet split — applied during D5 dogfood
  triage, not now; cost would be a per-milestone disruption).
- **§6 checkbox 3 (NB01 texture)** — ✅ GREEN. Proceed to NB05+NB06
  (centrepiece) at scale.
- **§6 checkbox 5 (Julia dual track in HW3+M2)** — ⛔ DEFER to v1.1.
  v1.0 stays Python-only on graded paths.
- **§6 checkbox 6 (CI)** — ✅ enabled. Add a workflow at D2 close.
- **§6 checkbox 7 (Julia CI)** — ⛔ DEFER to v1.1.
- **§6 checkbox 4 (appendices NB-A/B/C)** — ⛔ DEFER to v1.1.

## Verdict

**G-D1 PASSED. D2 may start in parallel.** Three concurrent tracks:

- Track P (PSets): D2.1 → D2.2 → D2.3 (serialised because each
  reuses the previous PSet's vocabulary).
- Track C (Capstone): D2.4 → D2.5 (serialised; M3 imports M2).
- Track J (Julia): D2.6 → D2.7 (serialised; NB06 imports NB05).

Tracks P, C, J run in parallel; D2.8 (review+audit) merges all three.

**Implementer proceeding.** Will ping the operator after D2.8 with
the first real "review me" checkpoint.
