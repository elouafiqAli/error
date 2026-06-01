/-
# Corollary 2: uniform slack (`cor:slack`)

Let `w(H) := H/2 - HbinInv H`. Then:
1. `w 0 = w 1 = 0`,
2. `w` is concave on `[0,1]`,
3. `w` attains its maximum at `H* = Hbin(1/5)` with value
       `w* = (1/2) · Hbin(1/5) - 1/5`,
4. `w* ∈ Ioo 0.1610 0.1611`.

Consequence: for every partition `P` and binary label `f`,
  `P.condEntropy f / 2 - P.bayesError f ≤ w*` and
  `P.bayesError f - HbinInv (P.condEntropy f) ≤ w*`.
-/

import PartitionBracket.Sandwich

namespace PartitionBracket

open Real

/-- Bracket width `w(H) = H/2 - HbinInv H`. -/
noncomputable def w (H : ℝ) : ℝ := H / 2 - HbinInv H

theorem w_zero : w 0 = 0 := by
  unfold w; simp [HbinInv_zero]

theorem w_one : w 1 = 0 := by
  unfold w; rw [HbinInv_one]; norm_num

/-- Unique maximiser `H* = Hbin (1/5)`. -/
noncomputable def Hstar : ℝ := Hbin (1/5)

/-- Maximal bracket width. -/
noncomputable def wstar : ℝ := (1/2) * Hbin (1/5) - 1/5

theorem w_concaveOn : ConcaveOn ℝ (Set.Icc (0:ℝ) 1) w := by
  sorry  -- L7.1

theorem w_max :
    ∀ H ∈ Set.Icc (0:ℝ) 1, w H ≤ wstar ∧ w Hstar = wstar := by
  sorry  -- L7.2

/-- **Numeric bound on `wstar`.** -/
theorem wstar_bounds : 0.1610 < wstar ∧ wstar < 0.1611 := by
  sorry  -- L7.3

variable {V : Type*} [Fintype V] [DecidableEq V] [Nonempty V]

/-- **Corollary 2 (`cor:slack`), upper side.** -/
theorem FinPart.upper_slack (P : FinPart V) (f : V → Bool) :
    P.condEntropy f / 2 - P.bayesError f ≤ wstar := by
  sorry  -- L7.4

/-- **Corollary 2 (`cor:slack`), lower side.** -/
theorem FinPart.lower_slack (P : FinPart V) (f : V → Bool) :
    P.bayesError f - HbinInv (P.condEntropy f) ≤ wstar := by
  sorry  -- L7.5

/-- **Corollary 2 (`cor:slack`).** Uniform slack on both sides. -/
theorem FinPart.uniformSlack (P : FinPart V) (f : V → Bool) :
    P.condEntropy f / 2 - P.bayesError f ≤ wstar ∧
    P.bayesError f - HbinInv (P.condEntropy f) ≤ wstar :=
  ⟨P.upper_slack f, P.lower_slack f⟩

end PartitionBracket
