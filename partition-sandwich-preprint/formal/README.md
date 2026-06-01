# `PartitionBracket` — Lean 4 mechanisation

Mechanisation of the main results of

> *A Two-Sided Bayes-Error Bracket from Partition-Conditional Entropy*
> (Elouafiq 2026, `../main.tex`)

in [Lean 4](https://leanprover.github.io/) + [Mathlib](https://leanprover-community.github.io/).

## Status

| Paper claim                                                     | Lean theorem                              | File                                | Status        |
|-----------------------------------------------------------------|-------------------------------------------|-------------------------------------|---------------|
| `thm:sandwich`, upper side (Hellman–Raviv)                      | `FinPart.bayesError_le_half_condEntropy`  | `Sandwich.lean`                     | 🟡 stub (L5)  |
| `thm:sandwich`, lower side (Fano)                               | `FinPart.HbinInv_condEntropy_le_bayesError`| `Sandwich.lean`                    | 🟡 stub (L6)  |
| `thm:sandwich`, statement                                       | `FinPart.sandwich`                        | `Sandwich.lean`                     | ✅ statement   |
| `cor:slack`, concavity of `w`                                   | `w_concaveOn`                             | `UniformSlack.lean`                 | 🟡 stub (L7.1)|
| `cor:slack`, maximum at `1/5`                                   | `w_max`                                   | `UniformSlack.lean`                 | 🟡 stub (L7.2)|
| `cor:slack`, numeric `w* ≈ 0.1610`                              | `wstar_bounds`                            | `UniformSlack.lean`                 | 🟡 stub (L7.3)|
| `cor:slack`, statement                                          | `FinPart.uniformSlack`                    | `UniformSlack.lean`                 | ✅ statement   |

Legend: ✅ proved · 🟡 stub (`sorry`) · ⛔ not yet stated.

This table mirrors the audit table in `../future-work/08-p1-patch-plan.md`
§1 and is updated **at every commit** that discharges a `sorry`.

## File map

```
PartitionBracket.lean                        # umbrella import
PartitionBracket/
├── BinaryEntropyAux.lean                    # Hbin in bits (rescale Mathlib's Real.binEntropy)
├── BinaryEntropyInverse.lean                # HbinInv on the small branch [0, 1/2]
├── Partition.lean                           # FinPart, bayesError, condEntropy
├── Sandwich.lean                            # Theorem 1
└── UniformSlack.lean                        # Corollary 2
```

## Build

Requires `elan` (Lean version manager).

```bash
cd formal
lake exe cache get      # fetch precompiled Mathlib (5–30 min the first time)
lake build              # builds PartitionBracket and all dependencies
```

A green `lake build` with **no `sorry` warnings** is the gate for promoting
the abstract's "*mechanisation … is in preparation*" to "*mechanised*".

## Provenance / discipline

* Each `sorry` is annotated `-- L<phase>.<id>` matching `formal/PROGRESS.md`.
* One commit per discharged `sorry`, message template
  `paper-a Phase L<n>.<id>: <theorem name>`.
* Mathlib pinned to `v4.30.0` in `lakefile.toml` and `lean-toolchain`.
* CI: `.github/workflows/lean.yml` runs `lake build` on every PR
  touching `formal/`.

## Adversarial check-list (kept as the audit gate)

When a `sorry` is discharged, the reviewer must verify:

1. **Definitions match paper.** `Hbin`, `HbinInv`, `bayesError`,
   `condEntropy` use the paper's conventions (uniform vertex measure,
   binary `{0,1}` labels, base-2 entropy).
2. **No hidden axioms.** `#print axioms <thm>` lists at most
   `propext`, `Classical.choice`, `Quot.sound`.
3. **No `sorry` in the dependency closure.** `lake build` is clean
   and `grep -r "sorry" PartitionBracket/` is empty.
4. **Numeric bound is honest.** `wstar_bounds` is an actual proved
   `0.1610 < wstar ∧ wstar < 0.1611`, not a `decide`-on-rational
   approximation.

## License

MIT, same as the parent preprint.
