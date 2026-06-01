/-
# Binary entropy: convenience wrappers over Mathlib

We use the binary entropy in **bits** (base 2), matching the paper:
`Hbin p = -p log₂ p - (1-p) log₂ (1-p)`,
with `0 log₂ 0 = 0`, `Hbin 0 = Hbin 1 = 0`, `Hbin (1/2) = 1`.

Mathlib's `Real.binEntropy` uses natural log; we rescale by `Real.log 2`.

This file isolates every Mathlib API touch-point so a Mathlib bump only
edits one file.
-/

import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Analysis.Convex.Jensen

namespace PartitionBracket

open Real

/-- Binary entropy in **bits** (paper convention `H_bin`). -/
noncomputable def Hbin (p : ℝ) : ℝ := Real.binEntropy p / Real.log 2

/-- `H_bin(0) = 0`. -/
theorem Hbin_zero : Hbin 0 = 0 := by
  simp [Hbin]

/-- `H_bin(1) = 0`. -/
theorem Hbin_one : Hbin 1 = 0 := by
  simp [Hbin]

/-- Non-negativity of `H_bin` on `[0,1]`. -/
theorem Hbin_nonneg {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1) : 0 ≤ Hbin p :=
  div_nonneg (Real.binEntropy_nonneg h0 h1) (Real.log_nonneg one_le_two)

/-- Upper bound: `H_bin ≤ 1` (in fact for all `p`, but only used on `[0,1]`). -/
theorem Hbin_le_one (p : ℝ) : Hbin p ≤ 1 := by
  unfold Hbin
  rw [div_le_one (Real.log_pos one_lt_two)]
  exact Real.binEntropy_le_log_two

/-- Symmetry: `H_bin(1-p) = H_bin(p)`. -/
theorem Hbin_one_sub (p : ℝ) : Hbin (1 - p) = Hbin p := by
  unfold Hbin
  congr 1
  have h := Real.binEntropy_two_inv_add (2⁻¹ - p)
  have e1 : (2⁻¹ : ℝ) + (2⁻¹ - p) = 1 - p := by ring
  have e2 : (2⁻¹ : ℝ) - (2⁻¹ - p) = p := by ring
  rw [e1, e2] at h
  exact h

/-- `H_bin(1/2) = 1`. -/
theorem Hbin_half : Hbin (1/2) = 1 := by
  unfold Hbin
  have h2 : (1/2 : ℝ) = 2⁻¹ := by norm_num
  rw [h2, Real.binEntropy_eq_log_two.mpr rfl]
  exact div_self (Real.log_pos one_lt_two).ne'

/-- Concavity of `H_bin` on `[0,1]`. -/
theorem Hbin_concaveOn : ConcaveOn ℝ (Set.Icc (0:ℝ) 1) Hbin := by
  have hc : (0:ℝ) ≤ (Real.log 2)⁻¹ :=
    inv_nonneg.mpr (Real.log_nonneg one_le_two)
  have h := Real.strictConcave_binEntropy.concaveOn.smul hc
  convert h using 1
  funext p
  simp [Hbin, div_eq_inv_mul]

end PartitionBracket
