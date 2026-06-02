### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Aggregator triple r_T = (Δmax, 1, 1) — the E3 punchline"
#> tags = ["mpnn", "unit-4", "aggregators"]

using Markdown, InteractiveUtils

# ╔═╡ a000000b-0001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a000000b-0002
md"""
# Notebook 11 — Aggregator triple $r_T = (\Delta_{\max}, 1, 1)$

> **Unit IV, item 1.** E3's punchline made tactile. The three
> MPNN aggregators (sum, mean, sym-norm) inflate the upper envelope
> by different constants. Sum inflates by $\Delta_{\max}$; on Cora
> with $\Delta_{\max} = 168$ that's **7 orders of magnitude
> honest looseness**.
"""

# ╔═╡ a000000b-0003
md"## 1. Slider — the maximum degree"

# ╔═╡ a000000b-0004
@bind Δmax Select([1, 2, 4, 8, 16, 32, 64, 128, 168, 256])

# ╔═╡ a000000b-0005
md"## 2. The three constants"

# ╔═╡ a000000b-0006
# TODO(reader): r_sum(Δ) = Δ; r_mean(Δ) = 1; r_symnorm(Δ) = 1.
# Build a table that prints all three at the current Δmax.

# ╔═╡ a000000b-0007
md"## 3. Inflated upper envelope, three curves"

# ╔═╡ a000000b-0008
# TODO(reader): for ε ∈ [0, 0.5], plot
#   r_sum(Δmax) * upper(ε)
#   r_mean(Δmax) * upper(ε)
#   r_symnorm(Δmax) * upper(ε)
# on the same axes. Use log scale on y if Δmax is large.

# ╔═╡ a000000b-0009
md"""
## 4. The distinguish drill

**Honest looseness** = "the bound is loose by design; the cause is
named in the paper" — *sum on Cora is loose because* $\Delta_{\max} = 168$.

**A bug** = "the bound is violated" — *never happens on the published
artefacts*; if it does on your code, you have a bug.

- TODO(reader): write two more lines distinguishing the two for a
  toy 3-cell example.

## 5. Cora reference

The published number: on Cora's label partition, the sum-aggregator
upper envelope is $\approx 10^7$ times the mean-aggregator upper.
The bracket is *never violated*; it is *honestly loose* — which is
why E3 uses mean/sym-norm aggregators, not sum.

## 6. Next — Notebook 12: ε-robust MPNN–WL constancy
"""

# ╔═╡ Cell order:
# ╠═a000000b-0001
# ╟─a000000b-0002
# ╟─a000000b-0003
# ╠═a000000b-0004
# ╟─a000000b-0005
# ╠═a000000b-0006
# ╟─a000000b-0007
# ╠═a000000b-0008
# ╟─a000000b-0009
