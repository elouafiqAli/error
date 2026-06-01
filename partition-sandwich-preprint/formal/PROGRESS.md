# Lean mechanisation: progress ledger

Discharge log for every `sorry` in `PartitionBracket/`. Update **in
the same commit** that closes the `sorry`. Numbering matches the
`-- L<phase>.<id>` annotations inside the `.lean` files.

## Phase L3 — `BinaryEntropyAux.lean` (Mathlib wrappers)

| ID    | Theorem                | Status | Commit |
|-------|------------------------|--------|--------|
| L3.1  | `Hbin_nonneg`          | 🟡 sorry |        |
| L3.2  | `Hbin_le_one`          | 🟡 sorry |        |
| L3.3  | `Hbin_one_sub`         | 🟡 sorry |        |
| L3.4  | `Hbin_half`            | 🟡 sorry |        |
| L3.5  | `Hbin_concaveOn`       | 🟡 sorry |        |

## Phase L4 — `BinaryEntropyInverse.lean`

| ID    | Theorem            | Status | Commit |
|-------|--------------------|--------|--------|
| L4.1  | `HbinInv` def       | 🟡 sorry |        |
| L4.2  | `HbinInv_mem_Icc`  | 🟡 sorry |        |
| L4.3  | `HbinInv_zero`     | 🟡 sorry |        |
| L4.4  | `HbinInv_one`      | 🟡 sorry |        |
| L4.5  | `Hbin_HbinInv`     | 🟡 sorry |        |
| L4.6  | `HbinInv_Hbin`     | 🟡 sorry |        |
| L4.7  | `HbinInv_mono`     | 🟡 sorry |        |
| L4.8  | `HbinInv_convexOn` | 🟡 sorry |        |

## Phase L2 — `Partition.lean`

| ID    | Theorem                  | Status | Commit |
|-------|--------------------------|--------|--------|
| L2.1  | `FinPart.sum_qC`         | 🟡 sorry |        |
| L2.2  | `FinPart.qC_mem_Icc`     | 🟡 sorry |        |
| L2.3  | `FinPart.PC_mem_Icc`     | 🟡 sorry |        |
| L2.4  | `FinPart.bayesError_nonneg`     | 🟡 sorry |        |
| L2.5  | `FinPart.bayesError_le_half`    | 🟡 sorry |        |
| L2.6  | `FinPart.condEntropy_nonneg`    | 🟡 sorry |        |
| L2.7  | `FinPart.condEntropy_le_one`    | 🟡 sorry |        |

## Phase L5 — `Sandwich.lean` upper

| ID    | Theorem                                | Status | Commit |
|-------|----------------------------------------|--------|--------|
| L5.1  | `FinPart.hellmanRaviv_pointwise`       | 🟡 sorry |        |
| L5.2  | `FinPart.bayesError_le_half_condEntropy`| 🟡 sorry |        |

## Phase L6 — `Sandwich.lean` lower (Fano)

| ID    | Theorem                                       | Status | Commit |
|-------|-----------------------------------------------|--------|--------|
| L6.1  | `FinPart.HbinInv_condEntropy_le_bayesError`   | 🟡 sorry |        |

## Phase L7 — `UniformSlack.lean`

| ID    | Theorem                  | Status | Commit |
|-------|--------------------------|--------|--------|
| L7.1  | `w_concaveOn`            | 🟡 sorry |        |
| L7.2  | `w_max`                  | 🟡 sorry |        |
| L7.3  | `wstar_bounds`           | 🟡 sorry |        |
| L7.4  | `FinPart.upper_slack`    | 🟡 sorry |        |
| L7.5  | `FinPart.lower_slack`    | 🟡 sorry |        |

## Phase L8 — Final integration

* unhedge abstract: PATCH A line "*Lean 4 formalisation … is in preparation*"
  → "*Lean 4 formalised; see `formal/`*".
* `VERIFICATION.md` r11: link to `formal/`, list axioms used.
* `.github/workflows/lean.yml` green on `main`.
