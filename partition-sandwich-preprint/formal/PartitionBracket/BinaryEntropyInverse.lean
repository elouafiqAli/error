/-
# Inverse binary entropy `HbinInv : [0,1] → [0, 1/2]`

The bracket `HbinInv (H(f|Π)) ≤ ε*_Π ≤ H(f|Π) / 2` needs the **small
branch** of the inverse of `Hbin`: the continuous strictly increasing
function `g : [0,1] → [0, 1/2]` with `Hbin (g H) = H` and `g (Hbin ε) = ε`
for `ε ∈ [0, 1/2]`.

The construction uses `Set.InjOn` of `Hbin` restricted to `[0, 1/2]`,
which is **strictly increasing** there.
-/

import PartitionBracket.BinaryEntropyAux
import Mathlib.Topology.Order.IntermediateValue

namespace PartitionBracket

open Real

/-- Small branch of `Hbin⁻¹`. Defined on all of `ℝ`; we only claim
properties on `[0,1]`. -/
noncomputable def HbinInv (h : ℝ) : ℝ := sorry  -- L4.1

theorem HbinInv_mem_Icc {h : ℝ} (h0 : 0 ≤ h) (h1 : h ≤ 1) :
    HbinInv h ∈ Set.Icc (0 : ℝ) (1/2) := by
  sorry  -- L4.2

theorem HbinInv_zero : HbinInv 0 = 0 := by sorry  -- L4.3

theorem HbinInv_one : HbinInv 1 = 1/2 := by sorry  -- L4.4

theorem Hbin_HbinInv {h : ℝ} (h0 : 0 ≤ h) (h1 : h ≤ 1) :
    Hbin (HbinInv h) = h := by sorry  -- L4.5

theorem HbinInv_Hbin {ε : ℝ} (hε0 : 0 ≤ ε) (hε : ε ≤ 1/2) :
    HbinInv (Hbin ε) = ε := by sorry  -- L4.6

theorem HbinInv_mono : MonotoneOn HbinInv (Set.Icc (0:ℝ) 1) := by
  sorry  -- L4.7

theorem HbinInv_convexOn : ConvexOn ℝ (Set.Icc (0:ℝ) 1) HbinInv := by
  sorry  -- L4.8

end PartitionBracket
