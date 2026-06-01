/-
# Finite partitions, partition Bayes error, conditional entropy

A **partition** of `V` (a finite type) is encoded as an indexed family of
non-empty disjoint cells `cell : Fin m → Finset V` whose union is `V`.
For binary `f : V → Bool` we define:

* the **cell mass** `qC i = (cell i).card / V.card`,
* the **cell positive rate** `PC i = #{v ∈ cell i : f v = true} / (cell i).card`,
* the **partition Bayes error** `bayesError = ∑ i, qC i * min (PC i) (1 - PC i)`,
* the **partition-conditional entropy** `condEntropy = ∑ i, qC i * Hbin (PC i)`.

These match `main.tex` `\epsP` and `H(f | Π)` exactly under the uniform
vertex measure.

Note: we use `P` (not the LaTeX symbol `Π`) as the partition variable,
since `Π` is reserved syntax for dependent function types in Lean 4.
-/

import PartitionBracket.BinaryEntropyAux

namespace PartitionBracket

open Real Finset

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- A finite partition of `V`: a finite family of non-empty pairwise
disjoint cells whose union is the universe. -/
structure FinPart (V : Type*) [Fintype V] [DecidableEq V] where
  m        : ℕ
  cell     : Fin m → Finset V
  nonempty : ∀ i, (cell i).Nonempty
  disjoint : ∀ i j, i ≠ j → Disjoint (cell i) (cell j)
  cover    : (Finset.univ : Finset (Fin m)).biUnion cell = Finset.univ

namespace FinPart

variable (P : FinPart V) (f : V → Bool)

/-- Cell mass under the uniform measure: `|cell i| / |V|`. -/
noncomputable def qC (i : Fin P.m) : ℝ :=
  (P.cell i).card / (Fintype.card V : ℝ)

/-- Fraction of vertices in `cell i` with `f v = true`. -/
noncomputable def PC (i : Fin P.m) : ℝ :=
  ((P.cell i).filter (fun v => f v = true)).card / (P.cell i).card

/-- Partition Bayes error `ε*_Π = ∑ q_i · min(P_i, 1 - P_i)`. -/
noncomputable def bayesError : ℝ :=
  ∑ i, P.qC i * min (P.PC f i) (1 - P.PC f i)

/-- Partition-conditional entropy `H(f | Π) = ∑ q_i · H_bin(P_i)`. -/
noncomputable def condEntropy : ℝ :=
  ∑ i, P.qC i * Hbin (P.PC f i)

/-- Cell masses sum to 1. -/
theorem sum_qC : ∑ i, P.qC i = 1 := by
  sorry  -- L2.1

theorem qC_mem_Icc (i : Fin P.m) : P.qC i ∈ Set.Icc (0:ℝ) 1 := by
  sorry  -- L2.2

theorem PC_mem_Icc (i : Fin P.m) : P.PC f i ∈ Set.Icc (0:ℝ) 1 := by
  sorry  -- L2.3

theorem bayesError_nonneg : 0 ≤ P.bayesError f := by
  sorry  -- L2.4

theorem bayesError_le_half : P.bayesError f ≤ 1/2 := by
  sorry  -- L2.5

theorem condEntropy_nonneg : 0 ≤ P.condEntropy f := by
  sorry  -- L2.6

theorem condEntropy_le_one : P.condEntropy f ≤ 1 := by
  sorry  -- L2.7

end FinPart

end PartitionBracket
