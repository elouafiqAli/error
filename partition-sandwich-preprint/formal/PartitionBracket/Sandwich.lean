/-
# Theorem 1: two-sided bracket (`thm:sandwich`)

  `HbinInv (H(f | Π)) ≤ ε*_Π ≤ H(f | Π) / 2`.

* **Upper (Hellman–Raviv, 1970).** Pointwise `min(p, 1-p) ≤ Hbin p / 2`
  on `[0,1]`; sum with weights `qC`.
* **Lower (Fano, 1961).** Jensen on the concave `Hbin`, then apply the
  small-branch inverse `HbinInv`.
-/

import PartitionBracket.Partition
import PartitionBracket.BinaryEntropyInverse

namespace PartitionBracket

open Real Finset

variable {V : Type*} [Fintype V] [DecidableEq V] [Nonempty V]

namespace FinPart

variable (P : FinPart V) (f : V → Bool)

/-- **Hellman–Raviv pointwise bound.** -/
theorem hellmanRaviv_pointwise {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1) :
    min p (1 - p) ≤ (1/2) * Hbin p := by
  sorry  -- L5.1

/-- **Upper side** (Hellman–Raviv aggregated). -/
theorem bayesError_le_half_condEntropy :
    P.bayesError f ≤ P.condEntropy f / 2 := by
  sorry  -- L5.2

/-- **Lower side** (Fano via Jensen). -/
theorem HbinInv_condEntropy_le_bayesError :
    HbinInv (P.condEntropy f) ≤ P.bayesError f := by
  sorry  -- L6.1

/-- **Theorem 1 (`thm:sandwich`).** -/
theorem sandwich :
    HbinInv (P.condEntropy f) ≤ P.bayesError f ∧
    P.bayesError f ≤ P.condEntropy f / 2 :=
  ⟨HbinInv_condEntropy_le_bayesError P f,
   bayesError_le_half_condEntropy P f⟩

end FinPart

end PartitionBracket
