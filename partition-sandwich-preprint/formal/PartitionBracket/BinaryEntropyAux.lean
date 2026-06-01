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
theorem Hbin_nonneg {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1) : 0 ≤ Hbin p := by
  sorry  -- L3.1

/-- Upper bound: `H_bin ≤ 1` on `[0,1]`. -/
theorem Hbin_le_one {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1) : Hbin p ≤ 1 := by
  sorry  -- L3.2

/-- Symmetry: `H_bin(1-p) = H_bin(p)`. -/
theorem Hbin_one_sub (p : ℝ) : Hbin (1 - p) = Hbin p := by
  sorry  -- L3.3

/-- `H_bin(1/2) = 1`. -/
theorem Hbin_half : Hbin (1/2) = 1 := by
  sorry  -- L3.4

/-- Concavity of `H_bin` on `[0,1]`. -/
theorem Hbin_concaveOn : ConcaveOn ℝ (Set.Icc (0:ℝ) 1) Hbin := by
  sorry  -- L3.5

end PartitionBracket
