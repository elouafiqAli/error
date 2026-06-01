/-
# `PartitionBracket`

Mechanisation of the main results of

    *A Two-Sided Bayes-Error Bracket from Partition-Conditional Entropy*
    (Elouafiq 2026, `partition-sandwich-preprint/main.tex`).

* `Sandwich.sandwich` ↔ `\thm{sandwich}` (Theorem 1, `main.tex \label{thm:sandwich}`).
* `UniformSlack.uniformSlack` ↔ `\cor{slack}` (Corollary 2, `main.tex \label{cor:slack}`).

See `README.md` for the claim-↔-theorem audit table.
-/

import PartitionBracket.BinaryEntropyAux
import PartitionBracket.BinaryEntropyInverse
import PartitionBracket.Partition
import PartitionBracket.Sandwich
import PartitionBracket.UniformSlack
