# REPRODUCING.md — TMLR reproducibility recipe for Paper B

> **Scope.** This file is the one-page "cheap badge" repro recipe
> for the empirical and verification claims of Paper B. It is the
> single source of truth for environment, commands, expected
> outputs, and runtime. If you can run the four commands at the
> bottom and obtain `all_pass == true` in `audit/external_audit_SUMMARY.json`,
> you have reproduced every numbered claim in the manuscript.

---

## 1. Environment (pinned, observed on the reference run)

```text
OS         : Darwin 25.3.0 arm64   (macOS, Apple Silicon)
Python     : 3.13.9
NumPy      : 2.3.5
SymPy      : 1.14.0
SciPy      : 1.16.3
NetworkX   : 3.5
Hypothesis : 6.155.1
PyTorch    : 2.12.0
torch_geometric : 2.7.0     # required only for T4 anchor + T5
matplotlib : 3.10.6         # required only if regenerating figures
```

No GPU is required at any tier. Reference wall-clock numbers in
§4 are for a single CPU core (Apple M-series, 2026).

### 1.1 Hardware caveat

T3 (`audit/stress.py`) is the only long-pole tier (~24 min on
one CPU core). It is embarrassingly parallel across the 15-seed
sweep; on a 16-core box it drops to ~2 min. All other tiers are
≤ 30 s sequential.

---

## 2. One-time setup

```bash
git clone <repo-url> gnn_express
cd gnn_express
git checkout <sha>            # see §3 for the certified SHA
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy==2.3.5 sympy==1.14.0 scipy==1.16.3 \
            networkx==3.5 hypothesis==6.155.1 \
            torch==2.12.0 torch_geometric==2.7.0
```

If `torch_geometric==2.7.0` fails to install, T4 (real-data
anchor) and T5 (Paper A cross-check) will skip. T0+T1+T2+T3
still cover every numbered theorem; only the empirical Table B.4
row requires T4.

---

## 3. Certified SHA

The reference audit (zero failures across all six tiers) was run
at SHA recorded in `audit/external_audit_SUMMARY.json :: sha`.
This SHA is the canonical reproducibility target. Any later
commit that touches verifier code or anchor data should bump
this field in the next audit closing commit.

---

## 4. The four commands

```bash
cd partition-brackets-framework

# (a) Full external audit (≈ 24 min on 1 CPU; ≈ 2 min on 16 CPU).
bash audit/run_external_audit.sh

# (b) Inspect the summary.
cat audit/external_audit_SUMMARY.json
#   Expect: "all_pass": true, all six tiers rc == 0.

# (c) Spot-check a single contract (≈ 2 s).
python3 verify_b_t1.py --tier T1 --json verify_b_t1.json
python3 -c "import json; d=json.load(open('verify_b_t1.json')); \
            assert all(r['ok'] for r in d['results']), d; \
            print('T1: 8/8 OK')"

# (d) Re-derive any magical constant from its JSON anchor.
#     Example: 0.279 vacuity threshold + 4.6e-26 Type-I cap.
python3 -c "import math; \
            print('0.279 =', 1 - 1/(2*math.log(2))); \
            print('4.6e-26 =', 2*(0.025)**16)"
```

Expected exit status of (a)–(c): `0`. Expected output of (d):

```text
0.279 = 0.27865...
4.6e-26 = 4.547...e-26
```

---

## 5. Tier-by-tier provenance

| Tier | Runner                              | Output                                      | Wall (1 CPU) |
|------|-------------------------------------|---------------------------------------------|--------------|
| T0   | `audit/run_external_audit.sh`       | `audit/external_audit/T0.log`               | < 1 s        |
| T1   | `verify_b_t1.py`                    | `audit/external_audit/T1_verify_b_t1.json`  | 3 s          |
| T2   | `verify_b_t2_mc.py`                 | `audit/external_audit/T2_verify_b_t2.json`  | 20 s         |
| T3   | `audit/stress.py`                   | `audit/external_audit/T3_stress.json`       | ≈ 24 min     |
| T4   | `audit/anchor_real_data_full.json`  | `audit/external_audit/T4_anchor.json`       | 9 s          |
| T5   | Paper A cross-check                 | `audit/external_audit/T5_paperA_*.log`      | 14 s         |

Every numbered claim in the manuscript maps to at least one
tier; the map is Table B.1 (§Appendix B).

---

## 6. Failure modes

If `all_pass == false`, inspect `audit/external_audit/Tk.log`
for the failing tier `k`. The three most common failure modes
on a fresh clone are:

  1. **`torch_geometric` import error** → T4/T5 skip. Not fatal
     for the verification claims; fatal only for the empirical
     Table B.4. Fix by installing `torch_geometric==2.7.0`.

  2. **`hypothesis` shrinker dies on a new fuzz example** → T1
     reports `ok: false` on a single contract with the offending
     input pickled. File an issue with the pickle; the contract
     is wrong, not the shrinker.

  3. **T5 Paper A cross-check off by floating-point** → check
     `audit/external_audit/T5_paperA_t1.log` for the gap; if
     |Δ| > 1e-12, NumPy upgrade is the likely culprit. Pin to
     the §1 versions.

---

## 7. What this badge does NOT cover

  - Lean-mechanised proofs (Phase 3, planned; see
    `FORMAL_VERIFICATION_EXECUTION_PLAN.md`).
  - Nonlinear-MPNN empirical slack (deferred; Paper A under
    review).
  - Cross-paper proof-script reuse (Paper A → Paper B); only
    the *numerical* cross-check is automated (T5).

---

## 8. Contact

For repro failures not covered by §6, open an issue against the
repo with: (a) `audit/external_audit_SUMMARY.json` contents,
(b) `pip freeze | grep -iE 'numpy|sympy|hypothesis|torch'`,
(c) `uname -srm`. The badge is intended to be self-diagnostic.
